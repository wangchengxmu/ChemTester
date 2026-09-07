from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
import json
import math
from numbers import Real
from pathlib import Path
import re
from typing import Any

from scripts.chemistry_expert.chemistry_evidence import (
    MAX_EVIDENCE_CHARS,
    evidence_sections,
    evidence_warning,
)
from scripts.design.generated_runtime_support import (
    RetrievedDocument,
    ToolCallResult,
    ToolCatalog,
    ToolSpec,
    safe_read_text,
    tokenize,
)


GENERIC_SEARCH_TERMS = {
    "a",
    "an",
    "and",
    "answer",
    "calculate",
    "chemistry",
    "correct",
    "determine",
    "find",
    "for",
    "from",
    "in",
    "is",
    "of",
    "on",
    "or",
    "problem",
    "question",
    "select",
    "statement",
    "the",
    "to",
    "use",
    "what",
    "which",
    "with",
}


def load_support_policy(
    *,
    repo_root: Path,
    config: dict[str, Any],
) -> dict[str, Any]:
    inline = dict(config.get("support_policy") or {})
    raw_path = str(config.get("support_policy_path") or "").strip()
    if not raw_path:
        return inline
    path = Path(raw_path)
    if not path.is_absolute():
        path = repo_root / path
    loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Support policy must be a JSON object: {path}")
    return {**loaded, **inline}


def _meaningful_tokens(text: str) -> list[str]:
    tokens = [token for token in tokenize(text) if token not in GENERIC_SEARCH_TERMS]
    return tokens or tokenize(text)


def _normalized_phrase(text: str) -> str:
    return " ".join(_meaningful_tokens(text))


def _non_finite_numeric_path(
    value: Any,
    *,
    path: str = "value",
    _seen: set[int] | None = None,
) -> str | None:
    """Return the first path containing a non-finite numeric value."""
    if isinstance(value, bool):
        return None
    if isinstance(value, Real):
        try:
            return path if not math.isfinite(value) else None
        except (TypeError, ValueError):
            return path
        except OverflowError:
            return None if isinstance(value, int) else path

    seen = _seen if _seen is not None else set()
    if isinstance(value, dict):
        marker = id(value)
        if marker in seen:
            return None
        seen.add(marker)
        for key, item in value.items():
            found = _non_finite_numeric_path(
                item,
                path=f"{path}.{key}",
                _seen=seen,
            )
            if found:
                return found
        return None
    if isinstance(value, (list, tuple, set, frozenset)):
        marker = id(value)
        if marker in seen:
            return None
        seen.add(marker)
        for index, item in enumerate(value):
            found = _non_finite_numeric_path(
                item,
                path=f"{path}[{index}]",
                _seen=seen,
            )
            if found:
                return found
    return None


def _combined_item_count(parameters: list[str], kwargs: dict[str, Any]) -> int:
    """Count items across configured list-like input parameters."""
    count = 0
    for parameter in parameters:
        value = kwargs.get(parameter)
        if isinstance(value, (list, tuple, set, frozenset)):
            count += len(value)
    return count


@dataclass(slots=True)
class KnowledgeChunk:
    path: str
    title: str
    heading: str
    text: str
    tokens: list[str]


class CuratedMemoryIndex:
    """Chunk-level retrieval over canonical, benchmark-neutral knowledge."""

    def __init__(
        self,
        memory_root: str | Path,
        *,
        policy: dict[str, Any] | None = None,
    ) -> None:
        self.memory_root = Path(memory_root).resolve()
        self.policy = dict(policy or {})
        knowledge = dict(self.policy.get("knowledge") or {})
        self.include_dirs = tuple(
            str(item)
            for item in knowledge.get(
                "include_dirs",
                ["L1_ontology", "L2_principles", "L4_reference"],
            )
        )
        self._include_dir_keys = {
            item.replace("\\", "/").strip("/").casefold()
            for item in self.include_dirs
        }
        self.exclude_patterns = [
            re.compile(str(item), flags=re.IGNORECASE)
            for item in knowledge.get(
                "exclude_path_patterns",
                [
                    r"(^|/)benchmark[_-]",
                    r"(^|/)generated[_-]frontier",
                    r"(^|/)wave[0-9]+",
                ],
            )
        ]
        self.min_score = float(knowledge.get("min_score", 3.0))
        self.min_query_coverage = float(
            knowledge.get("min_query_coverage", 0.3)
        )
        self.min_anchor_hits = max(
            1,
            int(knowledge.get("min_anchor_hits", 2)),
        )
        self.max_chunk_chars = max(800, int(knowledge.get("max_chunk_chars", 3200)))
        self._managed_topics_configured = "managed_topics_registry" in knowledge
        self._managed_topics_valid = not self._managed_topics_configured
        self._managed_topic_ids: set[str] = set()
        if self._managed_topics_configured:
            self._managed_topic_ids = self._load_managed_topic_ids(
                knowledge.get("managed_topics_registry")
            )
        self._quarantined_documents: dict[str, dict[str, Any]] = {}
        self._resource_warnings: dict[str, list[dict[str, Any]]] = {}
        if "quarantine_manifest" in knowledge:
            self._load_quarantine_manifest(knowledge.get("quarantine_manifest"))
        self.chunks: list[KnowledgeChunk] = []
        self.documents: list[tuple[str, str, str]] = []
        self._document_frequency: Counter[str] = Counter()
        self._metadata: dict[str, dict[str, Any]] = {}

    def build(self) -> "CuratedMemoryIndex":
        self.chunks.clear()
        self.documents.clear()
        self._document_frequency.clear()
        self._metadata.clear()
        if not self.memory_root.exists():
            return self

        for root_name in self.include_dirs:
            root = self.memory_root / root_name
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
                    continue
                if not self.allows_document(path):
                    continue
                rel = self._normalize_memory_relative_path(path)
                if rel is None:
                    continue
                text = safe_read_text(path)
                if not text.strip():
                    continue
                file_chunks = self._split_document(rel, path.stem, text)
                if not file_chunks:
                    self._metadata[rel] = {
                        "support_tier": "citation_only",
                        "source_layer": root_name,
                        "chunk_count": 0,
                        "resource_warnings": [{
                            "path": rel,
                            "warning": evidence_warning(text) or "no_complete_evidence_packet",
                        }],
                    }
                    continue
                title = file_chunks[0].title
                self.documents.append((rel, title, text))
                self.chunks.extend(file_chunks)
                metadata = {
                    "support_tier": "canonical",
                    "source_layer": root_name,
                    "chunk_count": len(file_chunks),
                }
                self._metadata[rel] = metadata

        for chunk in self.chunks:
            self._document_frequency.update(set(chunk.tokens))
        return self

    def search(self, query: str, *, top_k: int = 6) -> list[RetrievedDocument]:
        query_tokens = _meaningful_tokens(query)
        if not query_tokens or not self.chunks:
            return []
        query_set = set(query_tokens)
        query_phrase = _normalized_phrase(query)
        total_chunks = len(self.chunks)
        anchors = self._rarest_known_tokens(
            query_set,
            self._document_frequency,
        )
        scored: list[tuple[float, KnowledgeChunk]] = []

        for chunk in self.chunks:
            chunk_counts = Counter(chunk.tokens)
            overlap = query_set & set(chunk_counts)
            if not overlap:
                continue
            coverage = len(overlap) / max(1, len(query_set))
            required_anchor_hits = min(self.min_anchor_hits, len(anchors))
            if anchors and len(anchors & overlap) < required_anchor_hits:
                continue
            if coverage < self.min_query_coverage:
                continue
            score = 0.0
            for token in overlap:
                frequency = self._document_frequency.get(token, 0)
                inverse_document_frequency = math.log(
                    (total_chunks + 1.0) / (frequency + 1.0)
                ) + 1.0
                score += inverse_document_frequency * min(2, chunk_counts[token])
            title_tokens = set(_meaningful_tokens(f"{chunk.title} {chunk.heading}"))
            if len(query_set) > 3 and not (query_set & title_tokens):
                continue
            score += 1.5 * len(query_set & title_tokens)
            score += 2.0 * (len(overlap) / max(1, len(query_set)))
            chunk_phrase = _normalized_phrase(
                f"{chunk.title} {chunk.heading} {chunk.text[:2000]}"
            )
            if query_phrase and query_phrase in chunk_phrase:
                score += 4.0
            if score >= self.min_score:
                scored.append((score, chunk))

        scored.sort(key=lambda item: (-item[0], item[1].path, item[1].heading))
        results: list[RetrievedDocument] = []
        seen_paths: set[str] = set()
        for score, chunk in scored:
            if chunk.path in seen_paths:
                continue
            seen_paths.add(chunk.path)
            results.append(
                RetrievedDocument(
                    path=chunk.path,
                    title=(
                        f"{chunk.title} > {chunk.heading}"
                        if chunk.heading and chunk.heading != chunk.title
                        else chunk.title
                    ),
                    score=round(score, 4),
                    snippet=chunk.text,
                )
            )
            if len(results) >= max(1, top_k):
                break
        return results

    def allows_document(self, path: str | Path) -> bool:
        """Return whether a memory-relative document is eligible for retrieval."""
        rel = self._normalize_memory_relative_path(path)
        if rel is None:
            return False
        if any(pattern.search(rel) for pattern in self.exclude_patterns):
            return False
        rel_key = rel.casefold()
        if not Path(rel).parts or Path(rel).parts[0].casefold() not in self._include_dir_keys:
            return False
        if Path(rel).suffix.lower() not in {".md", ".txt"}:
            return False
        if rel_key in self._quarantined_documents:
            return False
        gap_prefix = "L2_principles/chemtester_gap_skills/"
        if (
            self._managed_topics_configured
            and rel.casefold().startswith(gap_prefix.casefold())
            and rel.lower().endswith(".md")
        ):
            return (
                self._managed_topics_valid
                and Path(rel).stem.casefold() in self._managed_topic_ids
            )
        return True

    def metadata_for_path(self, path: str | Path) -> dict[str, Any]:
        raw_path = str(path).split("#", 1)[0]
        rel = self._normalize_memory_relative_path(raw_path)
        if rel is None or not self.allows_document(rel):
            return {}
        metadata = deepcopy(self._metadata.get(rel, {}))
        rel_key = rel.casefold()
        if rel_key in self._resource_warnings:
            metadata.setdefault("resource_warnings", []).extend(
                deepcopy(self._resource_warnings[rel_key])
            )
        return metadata

    def _normalize_memory_relative_path(self, path: str | Path) -> str | None:
        if not isinstance(path, (str, Path)):
            return None
        raw_path = str(path)
        if not raw_path.strip():
            return None
        candidate_text = raw_path.replace("\\", "/")
        candidate = Path(candidate_text)
        memory_root = self.memory_root.resolve()
        try:
            resolved = (
                candidate.resolve(strict=False)
                if candidate.is_absolute()
                else (memory_root / candidate).resolve(strict=False)
            )
            relative = resolved.relative_to(memory_root)
        except (OSError, RuntimeError, ValueError):
            return None
        normalized = relative.as_posix()
        return normalized if normalized and normalized != "." else None

    def _load_managed_topic_ids(self, configured_path: Any) -> set[str]:
        try:
            if not isinstance(configured_path, (str, Path)):
                raise ValueError("registry path must be a string or path")
            registry_path = Path(configured_path)
            memory_root = self.memory_root.resolve()
            if not registry_path.is_absolute():
                registry_path = memory_root / registry_path
            registry_path = registry_path.resolve(strict=False)
            registry_path.relative_to(memory_root)
            payload = json.loads(registry_path.read_text(encoding="utf-8-sig"))
            entries = payload["entries"]
            if not isinstance(payload, dict) or not isinstance(entries, list):
                raise ValueError("registry must contain an entries list")
            capability_ids: set[str] = set()
            for entry in entries:
                if not isinstance(entry, dict):
                    raise ValueError("registry entries must be objects")
                capability_id = entry.get("capability_id")
                if not isinstance(capability_id, str) or not capability_id.strip():
                    raise ValueError("registry entries require capability_id")
                capability_ids.add(capability_id.strip().casefold())
        except (OSError, RuntimeError, TypeError, ValueError, KeyError):
            self._managed_topics_valid = False
            return set()
        self._managed_topics_valid = True
        return capability_ids

    def _load_quarantine_manifest(self, configured_path: Any) -> None:
        try:
            if not isinstance(configured_path, (str, Path)):
                raise ValueError("manifest path must be a string or path")
            manifest_path = Path(configured_path)
            repo_root = self.memory_root.resolve().parent
            if not manifest_path.is_absolute():
                manifest_path = repo_root / manifest_path
            manifest_path = manifest_path.resolve(strict=False)
            manifest_path.relative_to(repo_root)
            payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
            if not isinstance(payload, dict):
                raise ValueError("manifest must be a JSON object")
            if payload.get("schema_version") != "chemtester-support-quarantine/v1":
                raise ValueError("unsupported quarantine manifest schema_version")
            documents = payload.get("documents")
            resource_warnings = payload.get("resource_warnings")
            if not isinstance(documents, list) or not isinstance(resource_warnings, list):
                raise ValueError(
                    "manifest requires documents and resource_warnings lists"
                )

            quarantined: dict[str, dict[str, Any]] = {}
            for document in documents:
                if not isinstance(document, dict):
                    raise ValueError("quarantined documents must be objects")
                path = document.get("path")
                sha256 = document.get("sha256")
                reason = document.get("reason")
                normalized = self._normalize_memory_relative_path(path)
                if (
                    not isinstance(path, str)
                    or not isinstance(sha256, str)
                    or not sha256.strip()
                    or not isinstance(reason, str)
                    or not reason.strip()
                    or normalized is None
                ):
                    raise ValueError(
                        "quarantined documents require safe path, sha256, and reason"
                    )
                normalized_key = normalized.casefold()
                if normalized_key in quarantined:
                    raise ValueError(f"duplicate quarantined path: {normalized}")
                record = deepcopy(document)
                record["path"] = normalized
                quarantined[normalized_key] = record

            warnings_by_path: dict[str, list[dict[str, Any]]] = {}
            for warning in resource_warnings:
                if not isinstance(warning, dict):
                    raise ValueError("resource warnings must be objects")
                path = warning.get("path")
                warning_name = warning.get("warning")
                normalized = self._normalize_memory_relative_path(path)
                if (
                    not isinstance(path, str)
                    or not isinstance(warning_name, str)
                    or not warning_name.strip()
                    or normalized is None
                ):
                    raise ValueError(
                        "resource warnings require safe path and warning"
                    )
                record = deepcopy(warning)
                record["path"] = normalized
                warnings_by_path.setdefault(normalized.casefold(), []).append(record)
        except (OSError, RuntimeError, TypeError, ValueError, KeyError) as exc:
            raise ValueError(f"Invalid quarantine manifest: {configured_path}") from exc
        self._quarantined_documents = quarantined
        self._resource_warnings = warnings_by_path

    def _split_document(
        self,
        rel: str,
        fallback_title: str,
        text: str,
    ) -> list[KnowledgeChunk]:
        body = self._strip_frontmatter(text)
        document_title = next(
            (
                line.lstrip("#").strip()
                for line in body.splitlines()
                if line.strip().startswith("#")
            ),
            fallback_title,
        )
        chunks: list[KnowledgeChunk] = []
        for section_heading, part in evidence_sections(body):
            if evidence_warning(part, max_chars=min(self.max_chunk_chars, MAX_EVIDENCE_CHARS)):
                continue
            searchable = f"{document_title} {section_heading} {part}"
            chunks.append(
                KnowledgeChunk(
                    path=rel,
                    title=document_title,
                    heading=section_heading,
                    text=part,
                    tokens=_meaningful_tokens(searchable),
                )
            )
        return chunks

    @staticmethod
    def _strip_frontmatter(text: str) -> str:
        lines = text.splitlines()
        if lines and lines[0].strip() == "---":
            for index in range(1, min(len(lines), 100)):
                if lines[index].strip() == "---":
                    return "\n".join(lines[index + 1 :])
        return text

    @staticmethod
    def _rarest_known_tokens(
        query_tokens: set[str],
        document_frequency: Counter[str],
    ) -> set[str]:
        known = [
            token
            for token in query_tokens
            if document_frequency.get(token, 0) > 0
        ]
        known.sort(
            key=lambda token: (
                document_frequency[token],
                -len(token),
                token,
            )
        )
        anchor_count = min(4, max(2, math.ceil(len(known) / 3)))
        return set(known[:anchor_count])


class CuratedToolCatalog:
    """Metadata-aware view of the full tool library with quarantine support."""

    def __init__(
        self,
        tools_root: str | Path,
        *,
        policy: dict[str, Any] | None = None,
    ) -> None:
        self.tools_root = Path(tools_root)
        self.policy = dict(policy or {})
        tools_policy = dict(self.policy.get("tools") or {})
        self.core_modules = {
            str(item) for item in tools_policy.get("core_modules", [])
        }
        self.active_tiers = {
            str(item)
            for item in tools_policy.get(
                "active_tiers",
                ["core", "specialist"],
            )
        }
        self.quarantine_patterns = [
            re.compile(str(item), flags=re.IGNORECASE)
            for item in tools_policy.get(
                "quarantine_patterns",
                [r"(^|_)benchmark(_|$)", r"frontier", r"answer[_-]?key"],
            )
        ]
        self.hide_undocumented = bool(tools_policy.get("hide_undocumented", True))
        retired = tools_policy.get("retired_tool_ids", [])
        if not isinstance(retired, list) or any(
            not isinstance(value, str) or not re.fullmatch(r"[A-Za-z_]\w*\.[A-Za-z_]\w*", value)
            for value in retired
        ) or len(set(retired)) != len(retired):
            raise ValueError("retired_tool_ids must contain unique module.function identifiers")
        self.retired_tool_ids = set(retired)
        self.min_score = float(tools_policy.get("min_score", 3.0))
        self.max_per_module = max(1, int(tools_policy.get("max_per_module", 2)))
        raw_contracts = tools_policy.get("contracts") or {}
        if not isinstance(raw_contracts, dict):
            raw_contracts = {}
        self.contracts = {
            str(tool_id): deepcopy(contract)
            for tool_id, contract in raw_contracts.items()
            if isinstance(contract, dict)
        }
        self.base_catalog = ToolCatalog(self.tools_root)
        self.tools: list[ToolSpec] = []
        self.quarantined_tool_count = 0
        self.retired_tool_count = 0
        self._by_id: dict[str, ToolSpec] = {}
        self._metadata: dict[str, dict[str, Any]] = {}
        self._document_frequency: Counter[str] = Counter()

    def build(self) -> "CuratedToolCatalog":
        self.base_catalog.build()
        self.tools.clear()
        self._by_id.clear()
        self._metadata.clear()
        self._document_frequency.clear()
        self.quarantined_tool_count = 0
        self.retired_tool_count = 0

        for tool in self.base_catalog.tools:
            # Permanent public-interface removal, including internal helpers/tests.
            if tool.id in self.retired_tool_ids:
                self.retired_tool_count += 1
                continue
            quarantined = any(
                pattern.search(f"{tool.module}.{tool.function} {tool.description}")
                for pattern in self.quarantine_patterns
            )
            undocumented = not tool.description.strip()
            if quarantined or (self.hide_undocumented and undocumented):
                self.quarantined_tool_count += 1
                continue
            tier = "core" if tool.module in self.core_modules else "specialist"
            if tier not in self.active_tiers:
                self.quarantined_tool_count += 1
                continue
            self.tools.append(tool)
            self._by_id[tool.id] = tool
            metadata = {
                "support_tier": tier,
                "reliability": "curated-core" if tier == "core" else "provisional",
                "validation_scope": "Allowlisted implementation; result contracts do not establish scientific correctness.",
                "required_parameters": list(tool.required_params),
                "applicability": self._first_sentence(tool.description),
                "limitations": (
                    "Use only when the visible question supplies every required input "
                    "with compatible units and the function matches the requested quantity."
                ),
            }
            contract = self.contracts.get(tool.id)
            if contract is not None:
                metadata["contract"] = deepcopy(contract)
            self._metadata[tool.id] = metadata
            self._document_frequency.update(set(self._tool_tokens(tool)))
        return self

    def find(self, module: str, function: str) -> ToolSpec | None:
        return self._by_id.get(f"{module}.{function}")

    def search(self, query: str, *, top_k: int = 6) -> list[ToolSpec]:
        query_tokens = _meaningful_tokens(query.replace("_", " ").replace(".", " "))
        if not query_tokens:
            return []
        query_set = set(query_tokens)
        total_tools = max(1, len(self.tools))
        scored: list[tuple[float, ToolSpec]] = []
        for tool in self.tools:
            tool_tokens = self._tool_tokens(tool)
            tool_set = set(tool_tokens)
            overlap = query_set & tool_set
            if not overlap:
                continue
            identifier_tokens = set(
                _meaningful_tokens(
                    f"{tool.module.replace('_', ' ')} "
                    f"{tool.function.replace('_', ' ')}"
                )
            )
            identifier_hits = query_set & identifier_tokens
            if not identifier_hits:
                continue
            if len(query_set) > 3 and len(identifier_hits) < 2:
                continue
            required_input_tokens = self._required_input_tokens(tool)
            if (
                len(query_set) > 4
                and required_input_tokens
                and not (query_set & required_input_tokens)
                and len(identifier_hits) < 3
            ):
                continue
            score = 0.0
            for token in overlap:
                frequency = self._document_frequency.get(token, 0)
                score += math.log((total_tools + 1.0) / (frequency + 1.0)) + 1.0
            function_tokens = set(_meaningful_tokens(tool.function.replace("_", " ")))
            module_tokens = set(_meaningful_tokens(tool.module.replace("_", " ")))
            score += 2.0 * len(query_set & function_tokens)
            score += 0.75 * len(query_set & module_tokens)
            score += 2.0 * (len(overlap) / max(1, len(query_set)))
            if self._metadata[tool.id]["support_tier"] == "core":
                score += 1.0
            if len(tool.required_params) > 6:
                score -= 0.5
            if score >= self.min_score:
                scored.append((score, tool))

        scored.sort(key=lambda item: (-item[0], item[1].id))
        selected: list[ToolSpec] = []
        module_counts: Counter[str] = Counter()
        for score, tool in scored:
            if module_counts[tool.module] >= self.max_per_module:
                continue
            metadata = self._metadata[tool.id]
            metadata["last_search_score"] = round(score, 4)
            selected.append(tool)
            module_counts[tool.module] += 1
            if len(selected) >= max(1, top_k):
                break
        return selected

    def execute(self, tool: ToolSpec, kwargs: dict[str, Any]) -> ToolCallResult:
        if tool.id in self.retired_tool_ids:
            return ToolCallResult(
                tool_id=tool.id, kwargs=kwargs, error="Tool removed from the public catalog",
                metadata=self._classified_metadata(
                    {}, classification="retired_tool", execution_succeeded=False,
                ),
            )
        missing = [name for name in tool.required_params if name not in kwargs]
        metadata = self.metadata_for(tool)
        if missing:
            return ToolCallResult(
                tool_id=tool.id,
                kwargs=kwargs,
                error=f"Missing required parameter(s): {', '.join(missing)}",
                metadata=self._classified_metadata(
                    metadata,
                    classification="invalid_input",
                    execution_succeeded=False,
                ),
            )
        input_error = self._input_contract_error(tool, kwargs)
        if input_error is not None:
            return ToolCallResult(
                tool_id=tool.id,
                kwargs=kwargs,
                error=input_error,
                metadata=self._classified_metadata(
                    metadata,
                    classification="invalid_input",
                    execution_succeeded=False,
                ),
            )
        result = self.base_catalog.execute(tool, kwargs)
        result.metadata["curation"] = metadata
        if result.error is not None:
            self._set_classification(
                result,
                classification="tool_error",
                evidence_valid=False,
                execution_succeeded=False,
                result_contract_valid=None,
            )
            return result

        if (
            isinstance(result.result, dict)
            and (
                result.result.get("error")
                or result.result.get("success") is False
                or result.result.get("ok") is False
            )
        ):
            result.error = str(
                result.result.get("error")
                or "Tool returned an unsuccessful result payload."
            )
        if result.error is not None:
            self._set_classification(
                result,
                classification="evidence_invalid",
                evidence_valid=False,
                execution_succeeded=True,
                result_contract_valid=False,
            )
            return result

        if result.result is None:
            result.error = "Tool returned None; evidence-invalid result."
            self._set_classification(
                result,
                classification="evidence_invalid",
                evidence_valid=False,
                execution_succeeded=True,
                result_contract_valid=False,
            )
            return result

        non_finite_path = _non_finite_numeric_path(result.result, path="result")
        if non_finite_path is not None:
            result.error = (
                "Tool returned a non-finite numeric value at "
                f"{non_finite_path}; evidence-invalid result."
            )
            self._set_classification(
                result,
                classification="evidence_invalid",
                evidence_valid=False,
                execution_succeeded=True,
                result_contract_valid=False,
            )
            return result

        result_error = self._result_contract_error(tool, result.result)
        if result_error is not None:
            result.error = result_error
            self._set_classification(
                result,
                classification="evidence_invalid",
                evidence_valid=False,
                execution_succeeded=True,
                result_contract_valid=False,
            )
            return result

        self._set_classification(
            result,
            classification="usable",
            evidence_valid=None,
            usable=True,
            execution_succeeded=True,
            result_contract_valid=True,
            scientific_validity="not_independently_verified",
        )
        return result

    def metadata_for(self, tool: ToolSpec | str) -> dict[str, Any]:
        tool_id = tool if isinstance(tool, str) else tool.id
        return deepcopy(self._metadata.get(tool_id, {}))

    def _contract_for(self, tool: ToolSpec | str) -> dict[str, Any]:
        tool_id = tool if isinstance(tool, str) else tool.id
        contract = self.contracts.get(tool_id)
        return deepcopy(contract) if contract is not None else {}

    def _input_contract_error(
        self,
        tool: ToolSpec,
        kwargs: dict[str, Any],
    ) -> str | None:
        non_finite_path = _non_finite_numeric_path(kwargs, path="kwargs")
        if non_finite_path is not None:
            return (
                "Input contains a non-finite numeric value at "
                f"{non_finite_path}; execution rejected."
            )

        max_items = self._contract_for(tool).get("max_items_combined")
        if max_items is None:
            return None
        if not isinstance(max_items, dict):
            return f"Invalid max_items_combined contract for tool {tool.id}."
        parameters = max_items.get("parameters")
        maximum = max_items.get("maximum")
        if (
            not isinstance(parameters, list)
            or not parameters
            or isinstance(maximum, bool)
            or not isinstance(maximum, int)
            or maximum < 0
        ):
            return f"Invalid max_items_combined contract for tool {tool.id}."
        parameter_names = [str(parameter) for parameter in parameters]
        combined_count = _combined_item_count(parameter_names, kwargs)
        if combined_count > maximum:
            return (
                "Input contract violation: max_items_combined for "
                f"parameters {parameter_names} is {combined_count}, "
                f"above maximum {maximum}; execution rejected."
            )
        return None

    def _result_contract_error(self, tool: ToolSpec, result: Any) -> str | None:
        contract = self._contract_for(tool)
        expected_type = contract.get("result_type")
        if expected_type is not None:
            type_matches = {
                "number": isinstance(result, Real) and not isinstance(result, bool),
                "object": isinstance(result, dict),
                "array": isinstance(result, list),
            }
            if expected_type not in type_matches:
                return f"Invalid result_type contract for tool {tool.id}."
            if not type_matches[expected_type]:
                actual_type = type(result).__name__
                return (
                    "Result contract violation: expected result_type "
                    f"'{expected_type}', got '{actual_type}'."
                )

        required_keys = contract.get("required_result_keys") or []
        if required_keys:
            if not isinstance(result, dict):
                return (
                    "Result contract violation: required_result_keys "
                    "can only be checked on an object result."
                )
            missing = [str(key) for key in required_keys if key not in result]
            if missing:
                return (
                    "Result contract violation: missing required output key(s): "
                    f"{', '.join(missing)}."
                )
        return None

    @staticmethod
    def _classified_metadata(
        metadata: dict[str, Any],
        *,
        classification: str,
        evidence_valid: bool | None = False,
        usable: bool = False,
        execution_succeeded: bool | None = None,
        result_contract_valid: bool | None = None,
        scientific_validity: str | None = None,
    ) -> dict[str, Any]:
        return {
            "curation": deepcopy(metadata),
            "classification": classification,
            "evidence_valid": evidence_valid,
            "usable": usable,
            "execution_succeeded": execution_succeeded,
            "result_contract_valid": result_contract_valid,
            "scientific_validity": scientific_validity,
        }

    @staticmethod
    def _set_classification(
        result: ToolCallResult,
        *,
        classification: str,
        evidence_valid: bool | None,
        usable: bool = False,
        execution_succeeded: bool | None = None,
        result_contract_valid: bool | None = None,
        scientific_validity: str | None = None,
    ) -> None:
        result.metadata["classification"] = classification
        result.metadata["evidence_valid"] = evidence_valid
        result.metadata["usable"] = usable
        result.metadata["execution_succeeded"] = execution_succeeded
        result.metadata["result_contract_valid"] = result_contract_valid
        result.metadata["scientific_validity"] = scientific_validity

    @staticmethod
    def _tool_tokens(tool: ToolSpec) -> list[str]:
        return _meaningful_tokens(
            f"{tool.module.replace('_', ' ')} "
            f"{tool.function.replace('_', ' ')} {tool.description[:1600]}"
        )

    @staticmethod
    def _first_sentence(text: str) -> str:
        compact = " ".join(str(text).split())
        match = re.search(r"^(.+?[.!?])(?:\s|$)", compact)
        return (match.group(1) if match else compact)[:300]

    @staticmethod
    def _required_input_tokens(tool: ToolSpec) -> set[str]:
        aliases = {
            "chemical_class_a": "materials",
            "chemical_class_b": "materials",
            "delta_h": "enthalpy",
            "delta_s": "entropy",
            "t": "temperature",
            "temp": "temperature",
            "n": "moles",
            "v": "volume",
            "p": "pressure",
        }
        tokens: set[str] = set()
        for raw_name in tool.required_params:
            lowered = str(raw_name).lower()
            alias = aliases.get(lowered)
            if alias:
                tokens.add(alias)
            tokens.update(
                token
                for token in _meaningful_tokens(lowered.replace("_", " "))
                if len(token) > 1
            )
        return tokens
