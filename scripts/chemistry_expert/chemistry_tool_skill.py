from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Callable

from scripts.chemistry_expert.update_frontier_skill import render_topic
from scripts.chemistry_expert.chemistry_evidence import (
    MAX_EVIDENCE_CHARS,
    evidence_sections,
    evidence_warning,
    select_evidence_documents,
)

from scripts.design.generated_runtime_support import (
    GenericProblem,
    MemoryIndex,
    RetrievedDocument,
    ToolCallResult,
    ToolCatalog,
    ToolSpec,
    json_preview,
)


ToolArgumentBinder = Callable[[ToolSpec], dict[str, Any]]


def model_tool_skill_trace(answer: Any) -> dict[str, Any]:
    for step in list(getattr(answer, "agent_trace", []) or []):
        if step.get("agent") == "model_tool_skill" and isinstance(step.get("trace"), dict):
            return dict(step["trace"])
    return {
        "schema_version": "chemtester-model-tool-skill-trace/v1",
        "enabled": False,
        "status": "missing",
        "model_call_count": 0,
        "model_selected_tool_count": 0,
        "model_selected_tool_ids": [],
        "events": [],
    }


@dataclass(slots=True)
class ToolSkillRun:
    retrieved_docs: list[RetrievedDocument] = field(default_factory=list)
    tool_calls: list[ToolCallResult] = field(default_factory=list)
    trace: dict[str, Any] = field(default_factory=dict)


class ChemistryToolSkill:
    """Provider-neutral model-directed access to chemistry memory and tools."""

    ACTIONS = {"search_knowledge", "search_tools", "call_tool", "finish"}
    V2_ROUTER_TERMS_TO_IGNORE = {
        "answer",
        "audit",
        "based",
        "calculate",
        "calculation",
        "chemical",
        "chemistry",
        "choice",
        "compare",
        "correct",
        "determine",
        "exact",
        "given",
        "identify",
        "option",
        "problem",
        "question",
        "requested",
        "result",
        "role",
        "scope",
        "select",
        "separate",
        "statement",
        "using",
        "value",
        "visible",
        "none", "above", "other", "all", "the", "and", "for", "from",
        "with", "which", "this", "that", "under", "following", "derived",
    }
    CALCULATION_SIGNALS = (
        "calculate",
        "compute",
        "convert",
        "evaluate numerically",
        "how many",
        "how much",
        "numerical value",
        "solve for",
    )
    REFERENCE_SIGNALS = (
        "database value",
        "experimental value",
        "literature value",
        "look up",
        "reference table",
        "tabulated",
    )

    def __init__(
        self,
        *,
        memory_index: MemoryIndex,
        tool_catalog: ToolCatalog,
        policy: dict[str, Any] | None = None,
    ) -> None:
        self.memory_index = memory_index
        self.tool_catalog = tool_catalog
        self.policy = dict(policy or {})
        self.capability_contracts = dict(self.policy.get("capability_contracts") or {})
        self.router_version = str(self.policy.get("router_version") or "v1").strip().lower()
        self.activation = str(self.policy.get("activation") or "all_questions").strip().lower()
        self.max_rounds = max(1, int(self.policy.get("max_rounds", 3)))
        self.initial_tool_count = max(0, int(self.policy.get("initial_tool_count", 0)))
        self.search_tool_count = max(1, int(self.policy.get("search_tool_count", 4)))
        self.knowledge_top_k = max(1, int(self.policy.get("knowledge_top_k", 2)))
        raw_action_max_tokens = int(self.policy.get("action_max_tokens", 0))
        self.action_max_tokens = (
            max(32, raw_action_max_tokens)
            if raw_action_max_tokens > 0
            else None
        )
        self.max_result_chars = max(200, int(self.policy.get("max_result_chars", 3000)))
        self.compact_skill_max_chars = max(
            500,
            int(self.policy.get("compact_skill_max_chars", 12000)),
        )
        self.compact_skill_max_capabilities = max(
            1,
            int(self.policy.get("compact_skill_max_capabilities", 1)),
        )
        self.compact_skill_min_anchor_coverage = min(
            1.0,
            max(0.0, float(self.policy.get("compact_skill_min_anchor_coverage", 0.65))),
        )
        self.compact_skill_min_anchor_hits = max(
            1,
            int(self.policy.get("compact_skill_min_anchor_hits", 2)),
        )
        self.compact_skill_min_margin = max(
            0.0,
            float(self.policy.get("compact_skill_min_margin", 0.10)),
        )
        self.exact_linked_skill_documents = max(
            0,
            int(self.policy.get("exact_linked_skill_documents", 0)),
        )
        self.planner_for_tool_signals = bool(
            self.policy.get("planner_for_tool_signals", True)
        )
        self.planner_for_reference_signals = bool(
            self.policy.get("planner_for_reference_signals", True)
        )
        self.compact_skill_path, self.compact_skill_text = self._load_compact_skill()
        (
            self.compact_skill_registry_path,
            self.compact_skill_registry_entries,
        ) = self._load_compact_skill_registry()
        self._v2_registry_router_entries = self._prepare_v2_router_entries()
        self._last_compact_skill_selection: dict[str, Any] = {}
        self._last_router_decision: dict[str, Any] = {}
        self._evidence_warnings: list[dict[str, str]] = []
        self.compact_skill_sha256 = (
            hashlib.sha256(self.compact_skill_text.encode("utf-8")).hexdigest()
            if self.compact_skill_text
            else None
        )

    def run(
        self,
        *,
        client: Any,
        question: str,
        problem: GenericProblem | None,
        initial_docs: list[RetrievedDocument],
        initial_tool_calls: list[ToolCallResult],
        candidate_tools: list[ToolSpec],
        bind_arguments: ToolArgumentBinder,
        evidence_context: dict[str, Any] | None = None,
    ) -> ToolSkillRun:
        docs, self._evidence_warnings = select_evidence_documents(initial_docs)
        calls = list(initial_tool_calls)
        router_decision = self.route_question(
            question=question,
            problem=problem,
            evidence_context=evidence_context,
        )
        if self._uses_v2_router():
            linked_docs = self.linked_documents_for_question(
                question=question,
                problem=problem,
            )
            docs, omitted = select_evidence_documents(docs + linked_docs)
            self._evidence_warnings.extend(omitted)
            if not router_decision["planner_required"]:
                return ToolSkillRun(
                    retrieved_docs=docs,
                    tool_calls=calls,
                    trace={
                        "schema_version": "chemtester-model-tool-skill-trace/v1",
                        "enabled": True,
                        "router_version": "v2",
                        "router_decision": router_decision,
                        "status": f"routed_{router_decision['route']}",
                        "model_call_count": 0,
                        "model_selected_tool_count": 0,
                        "model_selected_tool_ids": [],
                        "knowledge_document_count": len(docs),
                        "evidence_warnings": list(self._evidence_warnings),
                        "active_tool_count": len(self.tool_catalog.tools),
                        "quarantined_tool_count": int(
                            getattr(self.tool_catalog, "quarantined_tool_count", 0)
                        ),
                        "compact_skill_path": self.compact_skill_path,
                        "compact_skill_loaded": bool(self.compact_skill_text),
                        "compact_skill_sha256": self.compact_skill_sha256,
                        "compact_skill_selection": dict(
                            self._last_compact_skill_selection
                        ),
                        "events": [],
                    },
                )
        advertised = self._unique_tools(candidate_tools[: self.initial_tool_count])
        events: list[dict[str, Any]] = []
        seen_actions: set[str] = set()
        status = "max_rounds"
        fallback_used = False
        pending_fallback = ""
        fallback_enabled = self._uses_v2_router() and (
            router_decision.get("empty_knowledge_fallback") == "search_tools"
        )

        # The declared alternate search costs at most one additional action.
        for round_number in range(1, self.max_rounds + 2):
            if round_number > self.max_rounds + int(fallback_used):
                break
            prompt = self._action_prompt(
                question=question,
                problem=problem,
                docs=docs,
                calls=calls,
                tools=advertised,
                events=events,
                evidence_context=evidence_context,
            )
            try:
                response = str(
                    client.complete_text(
                        prompt,
                        system_prompt=self._system_prompt(),
                        max_tokens=self.action_max_tokens,
                    )
                ).strip()
            except Exception as exc:
                events.append(
                    {
                        "round": round_number,
                        "status": "model_error",
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                status = "model_error"
                break

            action = self._parse_action(response)
            event: dict[str, Any] = {
                "round": round_number,
                "raw_response": response[: self.max_result_chars],
            }
            if action is None:
                event["status"] = "invalid_action"
                events.append(event)
                status = "invalid_action"
                continue

            event["action"] = action
            action_key = json.dumps(
                {key: value for key, value in action.items() if key != "reason"},
                ensure_ascii=True, sort_keys=True, default=str,
            )
            if action_key in seen_actions and action.get("action") != "finish":
                event["status"] = "repeated_action"
                events.append(event)
                status = "repeated_action"
                break
            seen_actions.add(action_key)

            action_name = str(action["action"])
            if pending_fallback and action_name not in {pending_fallback, "finish"}:
                event["status"] = status = "fallback_contract_violation"
                events.append(event)
                break
            pending_fallback = ""
            if action_name == "finish":
                event["status"] = "finished"
                events.append(event)
                status = "finished"
                break

            if action_name == "search_knowledge":
                query = str(action.get("query") or question).strip()
                top_k = self._bounded_int(
                    action.get("top_k"),
                    default=self.knowledge_top_k,
                    maximum=3,
                )
                raw_found = self.memory_index.search(query, top_k=top_k)
                before_count = len(docs)
                docs, omitted = select_evidence_documents(docs + raw_found)
                self._evidence_warnings.extend(omitted)
                accepted_paths = {doc.path for doc in docs}
                found = [doc for doc in raw_found if doc.path in accepted_paths
                         and evidence_warning(doc.snippet) is None]
                added = len(docs) - before_count
                event.update(
                    {
                        "status": "ok",
                        "query": query,
                        "result_paths": [doc.path for doc in found],
                        "new_document_count": added,
                        "evidence_warnings": omitted,
                    }
                )
                events.append(event)
                if self._uses_v2_router() and not found:
                    if fallback_enabled and not fallback_used:
                        fallback_used = True
                        pending_fallback = "search_tools"
                        event["status"] = "alternate_evidence_path"
                        event["next_action"] = pending_fallback
                        continue
                    event["status"] = status = "no_targeted_evidence"
                    break
                continue

            if action_name == "search_tools":
                query = str(action.get("query") or question).strip()
                top_k = self._bounded_int(
                    action.get("top_k"),
                    default=self.search_tool_count,
                    maximum=6,
                )
                found = self.tool_catalog.search(query, top_k=top_k)
                advertised = self._unique_tools([*advertised, *found])
                event.update(
                    {
                        "status": "ok",
                        "query": query,
                        "result_tool_ids": [tool.id for tool in found],
                    }
                )
                events.append(event)
                if self._uses_v2_router() and not found:
                    event["status"] = status = "no_targeted_evidence"
                    break
                continue

            tool_id = str(action.get("tool_id") or "").strip()
            tool = self._tool_by_id(tool_id, advertised)
            if tool is None:
                event.update({"status": "unknown_tool", "tool_id": tool_id})
                events.append(event)
                status = "unknown_tool"
                continue

            arguments = action.get("arguments")
            if not isinstance(arguments, dict):
                arguments = {}
            # V2 arguments must be selected explicitly after inspecting physical
            # roles; a proximity-based legacy binder is not evidence of a role.
            bound = {} if self._uses_v2_router() else dict(bind_arguments(tool) or {})
            bound.update({str(key): value for key, value in arguments.items()})
            kwargs = {name: bound[name] for name in tool.params if name in bound}
            call = self.tool_catalog.execute(tool, kwargs)
            call.metadata["selection"] = {
                "selector": "model_tool_skill",
                "round": round_number,
                "reason": str(action.get("reason") or "").strip(),
                "model_argument_names": sorted(str(key) for key in arguments),
                "auto_bound_argument_names": sorted(
                    name for name in kwargs if name not in arguments
                ),
                "argument_provenance": action.get("argument_provenance", {}),
            }
            calls.append(call)
            event.update(
                {
                    "status": "ok" if call.error is None else "tool_error",
                    "tool_id": tool.id,
                    "kwargs": kwargs,
                    "result": (
                        json_preview(call.result, limit=self.max_result_chars)
                        if call.error is None
                        else None
                    ),
                    "error": call.error,
                }
            )
            events.append(event)

        model_calls = len(
            [
                event
                for event in events
                if event.get("raw_response") is not None
            ]
        )
        selected_calls = [
            call
            for call in calls[len(initial_tool_calls) :]
            if call.metadata.get("selection", {}).get("selector") == "model_tool_skill"
        ]
        return ToolSkillRun(
            retrieved_docs=docs,
            tool_calls=calls,
            trace={
                "schema_version": "chemtester-model-tool-skill-trace/v1",
                "enabled": True,
                "router_version": "v2" if self._uses_v2_router() else "v1",
                "router_decision": router_decision,
                "status": status,
                "model_call_count": model_calls,
                "model_selected_tool_count": len(selected_calls),
                "usable_tool_result_count": sum(
                    call.error is None and call.result is not None for call in selected_calls
                ),
                "model_selected_tool_ids": [call.tool_id for call in selected_calls],
                "knowledge_document_count": len(docs),
                "evidence_warnings": list(self._evidence_warnings),
                "active_tool_count": len(self.tool_catalog.tools),
                "quarantined_tool_count": int(
                    getattr(self.tool_catalog, "quarantined_tool_count", 0)
                ),
                "compact_skill_path": self.compact_skill_path,
                "compact_skill_loaded": bool(self.compact_skill_text),
                "compact_skill_sha256": self.compact_skill_sha256,
                "compact_skill_selection": dict(self._last_compact_skill_selection),
                "events": events,
                "alternate_evidence_path_used": fallback_used,
            },
        )

    def _action_prompt(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
        docs: list[RetrievedDocument],
        calls: list[ToolCallResult],
        tools: list[ToolSpec],
        events: list[dict[str, Any]],
        evidence_context: dict[str, Any] | None,
    ) -> str:
        docs, omitted = select_evidence_documents(docs)
        compact_skill = self.compact_skill_for_question(
            question=question,
            problem=problem,
        )
        payload: dict[str, Any] = {
            "question": question,
            "options": list(problem.options) if problem and problem.options else [],
            "structured_givens": dict(problem.given) if problem and problem.given else {},
            "companion_evidence": dict(evidence_context or {}),
            "compact_chemistry_skill": compact_skill,
            "support_requirement": self._support_requirement(problem, docs, calls),
            "knowledge": [self._document_descriptor(doc) for doc in docs[:6]],
            "evidence_warnings": list(self._evidence_warnings) + omitted,
            "router_decision": dict(self._last_router_decision),
            "tool_results": [
                {
                    "tool_id": call.tool_id,
                    "kwargs": call.kwargs,
                    "result": (
                        json_preview(call.result, limit=900)
                        if call.error is None
                        else None
                    ),
                    "error": call.error,
                }
                for call in calls[-8:]
            ],
            "available_tools": [self._tool_descriptor(tool) for tool in tools[:12]],
            "prior_actions": [
                {
                    key: value
                    for key, value in event.items()
                    if key not in {"raw_response", "result"}
                }
                for event in events[-6:]
            ],
        }
        return (
            "Choose whether one high-value evidence action is needed for this redacted chemistry problem.\n"
            "The expected answer and source solution are not available.\n\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2, default=str)}\n\n"
            "If support_requirement says evidence_required_before_finish or targeted_evidence_requested, do not "
            "return finish until at least one "
            "search_knowledge, search_tools, or call_tool action has produced relevant evidence or no targeted "
            "evidence action is possible after trying.\n"
            "If relevant retrieved knowledge names a module.function lookup, search the tool catalog for that "
            "capability and call a matching tool before finish. Do not claim that no compatible tool is available "
            "unless search_tools has been attempted after retrieving that guidance. Do not replace a missing "
            "empirical table cell with generic chemical reasoning.\n"
            "For V2 call_tool actions, provide every required argument explicitly. Name its physical role "
            "and units in argument_provenance; identify a visible value or state its derivation. "
            "Do not assume a parameter will be filled from the nearest number in the question.\n"
            "Return one JSON object only. Valid forms:\n"
            '{"action":"search_knowledge","query":"specific chemistry concept or property","top_k":2,"reason":"why"}\n'
            '{"action":"search_tools","query":"specific requested calculation and named inputs","top_k":4,"reason":"why"}\n'
            '{"action":"call_tool","tool_id":"module.function","arguments":{"parameter":1.0},"reason":"why"}\n'
            '{"action":"finish","reason":"existing evidence is sufficient or no useful tool is available"}'
        )

    def _system_prompt(self) -> str:
        if self._uses_v2_router():
            return (
                "You operate ChemTester Skill Router V2. The deterministic router has already decided "
                "that a targeted evidence action may be useful. Select at most one specific knowledge "
                "or tool action per round; do not answer the chemistry question in this step. Finish when "
                "the requested evidence has been obtained or when no exact match is available. Call a "
                "tool only when its applicability, required inputs, units, and requested output match the "
                "visible problem. Retrieved text and tool outputs are candidate evidence and may be wrong. "
                "When an event declares next_action=search_tools after empty knowledge retrieval, "
                "make that single alternate search or finish; do not repeat knowledge search. "
                "Never infer an expected answer from benchmark identity, option order, row identifiers, or "
                "prior runs. Return compact valid JSON only."
            )
        return (
            "You operate the ChemTester chemistry support skill. Select evidence actions; do not answer "
            "the chemistry question in this step. Finish immediately when the base model can answer reliably "
            "without external support, except that published benchmark frontier problems with no retrieved "
            "documents and no tool output need at least one targeted evidence action before finish. Search only "
            "when a specific missing fact or calculation could change "
            "the answer. Call a tool only when its applicability, required inputs, units, and requested output "
            "match the visible problem. Treat paired vision observations as evidence, not as an answer key. "
            "Never infer "
            "an expected answer from benchmark identity, option order, row identifiers, or prior waves. "
            "Retrieved text and tool outputs are candidate evidence and may be irrelevant or wrong; reject "
            "mismatched support. Call only listed tools or search the curated catalog first. Return compact "
            "valid JSON only."
        )

    def _support_requirement(
        self,
        problem: GenericProblem | None,
        docs: list[RetrievedDocument],
        calls: list[ToolCallResult],
    ) -> dict[str, Any]:
        if self._uses_v2_router():
            decision = dict(self._last_router_decision)
            route = str(decision.get("route") or "")
            tool_evidence_present = any(call.error is None and call.result is not None for call in calls)
            knowledge_evidence_present = bool(select_evidence_documents(docs)[0])
            evidence_present = (
                tool_evidence_present
                if route in {"tool", "skill_tool"}
                else knowledge_evidence_present
            )
            alternate_tool_support = decision.get("empty_knowledge_fallback") == "search_tools"
            if alternate_tool_support and tool_evidence_present:
                evidence_present = True
            if decision.get("planner_required") and not evidence_present:
                return {
                    "status": "targeted_evidence_requested",
                    "reason": decision.get("reason"),
                    "preferred_actions": (
                        ["search_tools"]
                        if route in {"tool", "skill_tool"}
                        else ["search_knowledge"]
                    ),
                }
            return {"status": "evidence_optional"}
        if docs or calls or problem is None:
            return {"status": "evidence_optional"}
        metadata = getattr(problem, "metadata", {}) or {}
        source = str(getattr(problem, "source", "") or metadata.get("source", "")).lower()
        if source == "published-benchmark-heldout":
            return {
                "status": "evidence_required_before_finish",
                "reason": "published benchmark frontier item currently has no retrieved local chemistry support or tool result",
                "preferred_actions": ["search_knowledge", "search_tools"],
            }
        return {"status": "evidence_optional"}

    def _load_compact_skill(self) -> tuple[str | None, str]:
        raw_path = str(self.policy.get("compact_skill_path") or "").strip()
        if not raw_path:
            return None, ""
        path = Path(raw_path)
        if not path.is_absolute():
            memory_root = Path(getattr(self.memory_index, "memory_root", "."))
            path = memory_root / path
        try:
            resolved = path.resolve()
            text = resolved.read_text(encoding="utf-8-sig").strip()
        except (OSError, UnicodeError):
            return str(path), ""
        return str(resolved), text

    def _load_compact_skill_registry(self) -> tuple[str | None, list[dict[str, Any]]]:
        raw_path = str(self.policy.get("compact_skill_registry_path") or "").strip()
        if raw_path:
            path = Path(raw_path)
            if not path.is_absolute():
                memory_root = Path(getattr(self.memory_index, "memory_root", "."))
                path = memory_root / path
        elif self.compact_skill_path:
            path = Path(self.compact_skill_path).with_suffix(".registry.json")
        else:
            return None, []
        try:
            resolved = path.resolve()
            payload = json.loads(resolved.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return str(path), []
        entries = payload.get("entries") if isinstance(payload, dict) else []
        return str(resolved), [dict(entry) for entry in entries if isinstance(entry, dict)]

    def route_question(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
        evidence_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not self._uses_v2_router():
            decision = {
                "route": "legacy_planner",
                "planner_required": True,
                "reason": "legacy all-question model-directed support",
                "selected_capability_ids": [],
                "tool_signal": False,
                "reference_signal": False,
            }
            self._last_router_decision = decision
            return dict(decision)

        self.compact_skill_for_question(question=question, problem=problem)
        selection = dict(self._last_compact_skill_selection)
        selected_ids = list(selection.get("selected_capability_ids") or [])
        visible_text = self._visible_problem_text(question=question, problem=problem)
        reference_task = self._reference_task(question)
        tool_signal = self._has_calculation_signal(visible_text)
        reference_signal = bool(reference_task) or self._has_reference_signal(visible_text)
        selected_contracts = [self.capability_contracts.get(cid, {}) for cid in selected_ids]
        tool_signal = tool_signal or any(c.get("evidence") == "tool" for c in selected_contracts)
        reference_signal = reference_signal or any(c.get("evidence") == "reference" for c in selected_contracts)
        vision_only = bool(evidence_context) and not selected_ids and not tool_signal and not reference_task

        if reference_task and self.planner_for_reference_signals:
            route = "knowledge_search"
            planner_required = True
            reason = "chemical compatibility hazards require pair-specific reference evidence, independently of skill selection"
        elif tool_signal and self.planner_for_tool_signals:
            route = "skill_tool" if selected_ids else "tool"
            planner_required = True
            reason = "visible numeric or conversion request may benefit from a matching deterministic tool"
        elif reference_signal and self.planner_for_reference_signals and not vision_only:
            route = "knowledge_search"
            planner_required = True
            reason = "a reference fact is needed even when a procedure is available"
        elif selected_ids:
            route = "skill"
            planner_required = False
            reason = "one capability passed applicability, independent-anchor and score-margin gates"
        else:
            route = "direct"
            planner_required = False
            reason = "no capability or evidence action passed the adaptive activation gates"

        decision = {
            "route": route,
            "router_revision": "v2.1.1",
            "score_semantics": "lexical heuristic, not a calibrated confidence probability",
            "planner_required": planner_required,
            "reason": reason,
            "selected_capability_ids": selected_ids,
            "selected_capabilities": list(
                selection.get("selected_capabilities") or []
            ),
            "top_score": selection.get("top_score"),
            "second_score": selection.get("second_score"),
            "score_margin": selection.get("score_margin"),
            "tool_signal": tool_signal,
            "reference_signal": reference_signal,
            "reference_task": reference_task,
            "empty_knowledge_fallback": (
                "search_tools" if reference_task or any(
                    c.get("empty_knowledge_fallback") == "search_tools" for c in selected_contracts
                ) else None
            ),
            "suggested_operations": [c["operation"] for c in selected_contracts if c.get("operation")],
            "vision_context_present": bool(evidence_context),
        }
        self._last_router_decision = decision
        return dict(decision)

    def linked_documents_for_question(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
    ) -> list[RetrievedDocument]:
        if not self._uses_v2_router() or self.exact_linked_skill_documents <= 0:
            return []
        self.compact_skill_for_question(question=question, problem=problem)
        selected_ids = list(
            dict.fromkeys(
                self._last_compact_skill_selection.get("selected_capability_ids") or []
            )
        )
        if not selected_ids:
            return []

        memory_root = Path(getattr(self.memory_index, "memory_root", ".")).resolve()
        results: list[RetrievedDocument] = []
        seen_paths: set[str] = set()
        scores = dict(self._last_compact_skill_selection.get("capability_scores") or {})
        entries = {
            str(entry.get("capability_id") or ""): entry
            for entry in self.compact_skill_registry_entries
        }
        for capability_id in selected_ids:
            entry = entries.get(capability_id, {})
            resources = sorted(
                (str(value) for value in entry.get("resources") or []),
                key=lambda value: (
                    "chemtester_gap_skills" not in value.replace("\\", "/"),
                    value,
                ),
            )
            for resource in resources:
                normalized = resource.replace("\\", "/").lstrip("./")
                if normalized.startswith("chem-memory/"):
                    normalized = normalized[len("chem-memory/") :]
                if not normalized.startswith(("L2_principles/", "L4_reference/")):
                    continue
                candidate = (memory_root / normalized).resolve()
                try:
                    candidate.relative_to(memory_root)
                except ValueError:
                    continue
                if candidate.suffix.lower() not in {".md", ".txt"} or not candidate.is_file():
                    continue
                rel = candidate.relative_to(memory_root).as_posix()
                if rel in seen_paths:
                    continue
                allows_document = getattr(self.memory_index, "allows_document", None)
                if callable(allows_document) and not allows_document(candidate):
                    continue
                try:
                    text = candidate.read_text(encoding="utf-8-sig").strip()
                except (OSError, UnicodeError):
                    continue
                if not text:
                    continue
                if text == render_topic(entry).strip():
                    # The full registry procedure is already in the answer prompt.
                    continue
                title = next(
                    (
                        line.lstrip("#").strip()
                        for line in text.splitlines()
                        if line.strip().startswith("#")
                    ),
                    candidate.stem,
                )
                snippet = self._linked_section(text, question=question, entry=entry)
                if not snippet:
                    self._evidence_warnings.append({
                        "path": rel, "title": title,
                        "warning": evidence_warning(text) or "no_complete_relevant_evidence_packet",
                    })
                    continue
                results.append(
                    RetrievedDocument(
                        path=rel,
                        title=title,
                        score=round(float(scores.get(capability_id, 0.0)), 4),
                        snippet=snippet,
                    )
                )
                seen_paths.add(rel)
                break
            if len(results) >= self.exact_linked_skill_documents:
                break
        return results

    def _uses_v2_router(self) -> bool:
        return self.router_version in {"v2", "skill_router_v2", "skill-router-v2"}

    @classmethod
    def _visible_problem_text(
        cls,
        *,
        question: str,
        problem: GenericProblem | None,
    ) -> str:
        parts = [str(question)]
        if problem is not None:
            parts.extend(str(option) for option in list(problem.options or []))
            if problem.given:
                parts.append(json.dumps(problem.given, ensure_ascii=False, default=str))
        return "\n".join(parts)

    @classmethod
    def _has_calculation_signal(cls, text: str) -> bool:
        lowered = text.lower()
        explicit_request = any(signal in lowered for signal in cls.CALCULATION_SIGNALS)
        numeric_input = bool(
            re.search(r"(?<![a-z])[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?", lowered)
        )
        equation_request = "balance" in lowered and "equation" in lowered
        return equation_request or (explicit_request and numeric_input)

    @classmethod
    def _has_reference_signal(cls, text: str) -> bool:
        lowered = text.lower()
        return any(signal in lowered for signal in cls.REFERENCE_SIGNALS)

    @staticmethod
    def _reference_task(question: str) -> str | None:
        # Stem-only task intent, never option letters, item IDs or benchmark pairs.
        text = question.lower()
        pair = re.search(r"\b(?:with|between|and)\b", text)
        interaction = re.search(r"\b(?:mix(?:ed|ing|tures?)?|combin(?:e|ed|ing)|contact|stor(?:e|ed|age)|compatib\w*|incompatib\w*)\b", text)
        hazard = re.search(r"\b(?:hazards?|risks?|safe(?:ty|ly)?|danger\w*|compatib\w*|incompatib\w*)\b", text)
        chemistry = re.search(r"\b(?:chemicals?|acids?|bases?|oxid\w*|reduc\w*|peroxides?|hydrocarbons?|aldehydes?|alcohols?|amines?|solvents?|metals?|salts?|sulfides?|cyanides?|reactiv\w*|flammab\w*|combustib\w*|organic|inorganic|reagents?|substances?)\b", text)
        return "chemical_compatibility" if pair and interaction and hazard and chemistry else None

    def compact_skill_for_question(
        self,
        *,
        question: str,
        problem: GenericProblem | None,
    ) -> str:
        text = str(self.compact_skill_text or "").strip()
        if not text:
            self._last_compact_skill_selection = {
                "mode": "empty",
                "selected_chars": 0,
                "selected_capabilities": [],
            }
            return ""
        if self._uses_v2_router():
            return self._v2_compact_skill_for_question(
                text=text,
                question=question,
                problem=problem,
            )
        if len(text) <= self.compact_skill_max_chars:
            selected = self._compact_skill_sections(text)[1]
            self._last_compact_skill_selection = {
                "mode": "full",
                "full_chars": len(text),
                "selected_chars": len(text),
                "selected_capabilities": [title for title, _body in selected],
                "selected_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
            return text

        visible_parts = [question]
        if problem is not None:
            visible_parts.extend(str(option) for option in list(problem.options or []))
            if problem.given:
                visible_parts.append(json.dumps(problem.given, ensure_ascii=False, default=str))
        query_forms = self._compact_token_forms("\n".join(visible_parts))
        preamble, sections = self._compact_skill_sections(text)
        registry_by_title = {
            self._compact_title_key(str(entry.get("title") or "")): entry
            for entry in self.compact_skill_registry_entries
            if entry.get("title")
        }
        ranked: list[tuple[float, int, str, str]] = []
        for index, (title, body) in enumerate(sections):
            entry = registry_by_title.get(self._compact_title_key(title), {})
            score = self._compact_section_score(
                query_forms=query_forms,
                title=title,
                body=body,
                registry_entry=entry,
            )
            ranked.append((score, index, title, body))
        ranked.sort(key=lambda item: (-item[0], item[1]))

        selected_blocks: list[str] = []
        selected_titles: list[str] = []
        prefix = preamble.strip()
        if len(prefix) > self.compact_skill_max_chars:
            prefix = prefix[: self.compact_skill_max_chars].rstrip()
        used_chars = len(prefix)
        for _score, _index, title, body in ranked:
            separator_chars = 2 if prefix or selected_blocks else 0
            block = body.strip()
            if used_chars + separator_chars + len(block) > self.compact_skill_max_chars:
                continue
            selected_blocks.append(block)
            selected_titles.append(title)
            used_chars += separator_chars + len(block)

        selected_text = "\n\n".join(part for part in [prefix, *selected_blocks] if part).strip()
        if not selected_text:
            selected_text = text[: self.compact_skill_max_chars].rstrip()
        self._last_compact_skill_selection = {
            "mode": "query_aware_sections",
            "full_chars": len(text),
            "selected_chars": len(selected_text),
            "selected_capabilities": selected_titles,
            "selected_sha256": hashlib.sha256(selected_text.encode("utf-8")).hexdigest(),
            "registry_path": self.compact_skill_registry_path,
        }
        return selected_text

    @staticmethod
    def _compact_skill_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
        matches = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", text))
        if not matches:
            return text.strip(), []
        preamble = text[: matches[0].start()].strip()
        sections: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            sections.append((match.group(1).strip(), text[match.start() : end].strip()))
        return preamble, sections

    @staticmethod
    def _compact_title_key(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", value.lower())

    def _v2_compact_skill_for_question(
        self,
        *,
        text: str,
        question: str,
        problem: GenericProblem | None,
    ) -> str:
        visible_text = self._visible_problem_text(question=question, problem=problem)
        query_tokens = self._v2_router_tokens(visible_text)
        normalized_query = self._normalized_router_phrase(visible_text)
        ranked: list[dict[str, Any]] = []

        for prepared in self._v2_registry_router_entries:
            index = int(prepared["index"])
            entry = prepared["entry"]
            capability_id = str(prepared["capability_id"])
            title = str(prepared["title"])
            contract = self.capability_contracts.get(capability_id, {})
            stem = question + (json.dumps(problem.given, default=str) if problem and problem.given else "")
            if any(not re.search(pattern, stem, re.I) for pattern in contract.get("required_patterns", [])):
                continue
            best_score = 0.0
            best_coverage = 0.0
            best_hits = 0
            best_exact = False
            best_phrase = ""
            for phrase, phrase_tokens, normalized_phrase in prepared["phrases"]:
                hits = len(query_tokens & phrase_tokens)
                coverage = hits / len(phrase_tokens)
                exact = bool(normalized_phrase and f" {normalized_phrase} " in f" {normalized_query} ")
                score = coverage + 0.04 * min(hits, 6) + (0.25 if exact else 0.0)
                if (score, hits, exact) > (best_score, best_hits, best_exact):
                    best_score = score
                    best_coverage = coverage
                    best_hits = hits
                    best_exact = exact
                    best_phrase = phrase
            ranked.append(
                {
                    "index": index,
                    "capability_id": capability_id,
                    "title": title,
                    "entry": entry,
                    "score": round(best_score, 6),
                    "coverage": round(best_coverage, 6),
                    "anchor_hits": best_hits,
                    "exact_phrase": best_exact,
                    "matched_phrase": best_phrase,
                }
            )

        ranked.sort(key=lambda item: (-item["score"], item["index"]))
        top = ranked[0] if ranked else None
        second = ranked[1] if len(ranked) > 1 else None
        top_score = float(top["score"]) if top else 0.0
        second_score = float(second["score"]) if second else 0.0
        margin = top_score - second_score
        top_eligible = bool(
            top
            and float(top["coverage"]) >= self.compact_skill_min_anchor_coverage
            and int(top["anchor_hits"]) >= self.compact_skill_min_anchor_hits
            and (bool(top["exact_phrase"]) or margin >= self.compact_skill_min_margin)
        )

        selected: list[dict[str, Any]] = []
        if top_eligible and top is not None:
            selected.append(top)
            for candidate in ranked[1:]:
                if len(selected) >= self.compact_skill_max_capabilities:
                    break
                if not candidate["exact_phrase"]:
                    continue
                if float(candidate["coverage"]) < self.compact_skill_min_anchor_coverage:
                    continue
                if int(candidate["anchor_hits"]) < self.compact_skill_min_anchor_hits:
                    continue
                selected.append(candidate)

        selected_ids = [str(item["capability_id"]) for item in selected]
        selected_titles = [str(item["title"]) for item in selected]
        selection_base = {
            "mode": "skill_router_v2",
            "full_chars": len(text),
            "selected_capabilities": selected_titles,
            "selected_capability_ids": selected_ids,
            "capability_scores": {
                str(item["capability_id"]): float(item["score"])
                for item in selected
            },
            "top_score": round(top_score, 6),
            "second_score": round(second_score, 6),
            "score_margin": round(margin, 6),
            "top_coverage": float(top["coverage"]) if top else 0.0,
            "top_anchor_hits": int(top["anchor_hits"]) if top else 0,
            "top_exact_phrase": bool(top["exact_phrase"]) if top else False,
            "matched_phrase": str(top["matched_phrase"]) if top_eligible and top else "",
            "minimum_anchor_coverage": self.compact_skill_min_anchor_coverage,
            "minimum_anchor_hits": self.compact_skill_min_anchor_hits,
            "minimum_margin": self.compact_skill_min_margin,
            "registry_path": self.compact_skill_registry_path,
        }
        if not selected:
            self._last_compact_skill_selection = {
                **selection_base,
                "selected_chars": 0,
                "selected_sha256": None,
            }
            return ""

        blocks = [self._render_v2_registry_entry(item["entry"]) for item in selected]
        header = (
            "# Routed Chemistry Procedure\n\n"
            "Apply only the procedure whose applicability statement matches the visible problem. "
            "Reject it if species, conditions, requested quantity, units, or assumptions differ. "
            "Treat linked support and tools as candidate evidence, not authority."
        )
        selected_text = "\n\n".join([header, *blocks]).strip()
        if len(selected_text) > self.compact_skill_max_chars:
            # Never supply a half-procedure whose final guards were chopped off.
            self._last_compact_skill_selection = {
                **selection_base, "selected_capability_ids": [], "selected_capabilities": [],
                "selected_chars": 0, "selected_sha256": None,
                "abstention_reason": "complete_procedure_exceeds_budget",
            }
            return ""
        self._last_compact_skill_selection = {
            **selection_base,
            "selected_chars": len(selected_text),
            "selected_sha256": hashlib.sha256(
                selected_text.encode("utf-8")
            ).hexdigest(),
        }
        return selected_text

    def _prepare_v2_router_entries(self) -> list[dict[str, Any]]:
        prepared: list[dict[str, Any]] = []
        for index, entry in enumerate(self.compact_skill_registry_entries):
            capability_id = str(entry.get("capability_id") or "").strip()
            title = str(entry.get("title") or capability_id).strip()
            phrase_records: list[tuple[str, set[str], str]] = []
            for phrase in [
                title,
                *[str(value) for value in entry.get("retrieval_terms") or []],
            ]:
                phrase_tokens = self._v2_router_tokens(phrase)
                if not phrase_tokens:
                    continue
                phrase_records.append(
                    (
                        phrase,
                        phrase_tokens,
                        self._normalized_router_phrase(phrase),
                    )
                )
            prepared.append(
                {
                    "index": index,
                    "entry": entry,
                    "capability_id": capability_id,
                    "title": title,
                    "phrases": phrase_records,
                }
            )
        return prepared

    @classmethod
    def _v2_router_tokens(cls, value: str) -> set[str]:
        # Count a word once. Consonant fingerprints previously doubled anchor hits.
        tokens = set()
        for token in re.findall(r"[a-z0-9]+", value.lower()):
            if token in cls.V2_ROUTER_TERMS_TO_IGNORE or token.isdigit():
                continue
            if len(token) < 3 and token not in {"pi", "ph", "ir", "uv", "mw"}:
                continue
            if token != "smiles":
                for suffix in ("izations", "ization", "ations", "ation", "ments", "ment", "ing", "ies", "ed", "es", "s"):
                    if token.endswith(suffix) and len(token) - len(suffix) >= 4:
                        token = token[:-len(suffix)]
                        break
            tokens.add(token)
        return tokens

    def _linked_section(self, text: str, *, question: str, entry: dict[str, Any]) -> str:
        query = self._v2_router_tokens(question)
        terms = self._v2_router_tokens(" ".join(entry.get("retrieval_terms", [])))
        preferred = self.capability_contracts.get(entry.get("capability_id"), {}).get("linked_headings", [])
        sections = []
        for index, (title, section) in enumerate(evidence_sections(text)):
            if evidence_warning(section):
                continue
            heading = self._v2_router_tokens(title)
            body = self._v2_router_tokens(section)
            score = 4 * len(query & heading) + len(query & body) + len(terms & heading)
            if any(phrase.lower() in title.lower() for phrase in preferred):
                score += 100
            sections.append((score, index, section))
        best = sorted((s for s in sections if s[0] > 0), key=lambda item: (-item[0], item[1]))[:2]
        if not best:
            return ""
        chosen = []
        for candidate in best:
            if any(candidate[2] in previous[2] for previous in chosen):
                continue
            if sum(len(s[2]) for s in chosen) + 2 * len(chosen) + len(candidate[2]) <= MAX_EVIDENCE_CHARS:
                chosen.append(candidate)
        return "\n\n".join(s[2] for s in sorted(chosen, key=lambda item: item[1]))

    @staticmethod
    def _normalized_router_phrase(value: str) -> str:
        return " ".join(re.findall(r"[a-z0-9]+", str(value).lower()))

    @staticmethod
    def _render_v2_registry_entry(entry: dict[str, Any]) -> str:
        title = str(entry.get("title") or entry.get("capability_id") or "Capability")
        lines = [f"## {title}"]
        use_when = str(entry.get("use_when") or "").strip()
        if use_when:
            lines.append(f"Applicability: {use_when}")
        steps = [str(value).strip() for value in entry.get("steps") or [] if str(value).strip()]
        if steps:
            lines.append("Procedure:")
            lines.extend(f"{index}. {step}" for index, step in enumerate(steps, start=1))
        guards = [str(value).strip() for value in entry.get("guards") or [] if str(value).strip()]
        if guards:
            lines.append("Guards:")
            lines.extend(f"- {guard}" for guard in guards)
        resources = [
            str(value).strip()
            for value in entry.get("resources") or []
            if str(value).strip()
        ]
        if resources:
            lines.append("Linked support:")
            lines.extend(f"- {resource}" for resource in resources[:4])
        return "\n".join(lines)

    @classmethod
    def _compact_token_forms(cls, value: str) -> set[str]:
        stopwords = {
            "about", "after", "also", "answer", "asks", "benchmark", "before",
            "between", "chemical", "chemistry", "from", "have", "into", "make",
            "more", "question", "reaction", "should", "than", "that", "their",
            "these", "this", "those", "which", "with", "would",
        }
        forms: set[str] = set()
        suffixes = (
            "izations", "ization", "ational", "ations", "ation", "ments", "ment",
            "izers", "izer", "izing", "ized", "able", "ible", "ally", "ing", "ies",
            "ied", "ed", "es", "s",
        )
        for raw_token in re.findall(r"[a-z0-9]+", value.lower()):
            if len(raw_token) < 3 or raw_token in stopwords:
                continue
            stem = raw_token
            for suffix in suffixes:
                if stem.endswith(suffix) and len(stem) - len(suffix) >= 4:
                    stem = stem[: -len(suffix)]
                    break
            forms.add(stem)
            consonants = re.sub(r"[aeiouy]", "", stem)
            if len(stem) >= 6 and len(consonants) >= 3:
                forms.add(consonants)
        return forms

    @classmethod
    def _compact_section_score(
        cls,
        *,
        query_forms: set[str],
        title: str,
        body: str,
        registry_entry: dict[str, Any],
    ) -> float:
        title_matches = query_forms & cls._compact_token_forms(title)
        body_matches = query_forms & cls._compact_token_forms(body)
        retrieval_matches = query_forms & cls._compact_token_forms(
            " ".join(str(term) for term in registry_entry.get("retrieval_terms") or [])
        )
        procedure_text = " ".join(
            [
                str(registry_entry.get("use_when") or ""),
                *[str(step) for step in registry_entry.get("steps") or []],
                *[str(guard) for guard in registry_entry.get("guards") or []],
            ]
        )
        procedure_matches = query_forms & cls._compact_token_forms(procedure_text)
        return float(
            8 * len(title_matches)
            + 4 * len(retrieval_matches)
            + 2 * len(body_matches)
            + len(procedure_matches)
        )

    def _tool_descriptor(self, tool: ToolSpec) -> dict[str, Any]:
        descriptor = {
            "tool_id": tool.id,
            "description": tool.description[:600],
            "parameters": [
                {
                    "name": name,
                    "required": name in tool.required_params,
                }
                for name in tool.params
            ],
        }
        if hasattr(self.tool_catalog, "metadata_for"):
            descriptor["curation"] = self.tool_catalog.metadata_for(tool)
        return descriptor

    def _document_descriptor(self, doc: RetrievedDocument) -> dict[str, Any]:
        descriptor = {
            "path": doc.path,
            "title": doc.title,
            "score": doc.score,
            "snippet": doc.snippet if evidence_warning(doc.snippet) is None else "",
        }
        warning = evidence_warning(doc.snippet)
        if warning:
            descriptor["resource_warning"] = warning
        if hasattr(self.memory_index, "metadata_for_path"):
            descriptor["curation"] = self.memory_index.metadata_for_path(doc.path)
        return descriptor

    @classmethod
    def _parse_action(cls, response: str) -> dict[str, Any] | None:
        text = str(response or "").strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text)
        decoder = json.JSONDecoder()
        for match in re.finditer(r"\{", text):
            try:
                payload, _end = decoder.raw_decode(text[match.start() :])
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict):
                continue
            action = str(payload.get("action") or "").strip().lower()
            if action not in cls.ACTIONS:
                continue
            payload["action"] = action
            return payload
        return None

    def _tool_by_id(self, tool_id: str, advertised: list[ToolSpec]) -> ToolSpec | None:
        for tool in advertised:
            if tool.id == tool_id:
                return tool
        if "." not in tool_id:
            return None
        module, function = tool_id.rsplit(".", 1)
        return self.tool_catalog.find(module, function)

    @staticmethod
    def _unique_tools(tools: list[ToolSpec]) -> list[ToolSpec]:
        result: list[ToolSpec] = []
        seen: set[str] = set()
        for tool in tools:
            if tool.id in seen:
                continue
            seen.add(tool.id)
            result.append(tool)
        return result

    @staticmethod
    def _append_unique_docs(
        docs: list[RetrievedDocument],
        additions: list[RetrievedDocument],
    ) -> int:
        seen = {doc.path for doc in docs}
        added = 0
        for doc in additions:
            if doc.path in seen:
                continue
            docs.append(doc)
            seen.add(doc.path)
            added += 1
        return added

    @staticmethod
    def _bounded_int(value: Any, *, default: int, maximum: int) -> int:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            parsed = default
        return min(max(parsed, 1), maximum)
