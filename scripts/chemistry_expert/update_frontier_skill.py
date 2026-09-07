from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SKILL_PATH = Path(
    "chem-memory/L2_principles/chemtester_compact_problem_solving_skill.md"
)
DEFAULT_REGISTRY_PATH = Path(
    "chem-memory/L2_principles/chemtester_compact_problem_solving_skill.registry.json"
)
DEFAULT_TOPIC_DIR = Path(
    "chem-memory/L2_principles/chemtester_gap_skills"
)
DEFAULT_RECEIPT_DIR = Path(
    "outputs/chemistry_expert/heartbeat_explore/frontier_skill_receipts"
)
MAX_TOPIC_CHARS = 12_000
MAX_TOPIC_LINES = 220
MAX_EVIDENCE_PER_ENTRY = 5

FORBIDDEN_MODEL_FACING_PATTERNS = (
    re.compile(r"\bbenchmark\b", re.IGNORECASE),
    re.compile(r"generated[_ -]?frontier", re.IGNORECASE),
    re.compile(r"\bwave[0-9]+\b", re.IGNORECASE),
    re.compile(r"answer[_ -]?key", re.IGNORECASE),
    re.compile(r"correct answer", re.IGNORECASE),
    re.compile(r"expected answer", re.IGNORECASE),
    re.compile(r"source solution", re.IGNORECASE),
    re.compile(r"\b(?:problem|item)[_ -]?id\b", re.IGNORECASE),
)


CORE_WORKFLOW = (
    "1. Inspect the full question, units, answer surface, and any companion vision evidence.",
    "2. Decide whether local support would materially reduce uncertainty. Do not call tools merely to increase tool-use counts.",
    "3. For exact calculations, search tools by operation and named inputs; call only a matching documented tool and verify units.",
    "4. For named concepts, properties, mechanisms, or reference facts, search knowledge with a short concept-specific query.",
    "5. If targeted support is missing, stop retrieval unless the active capability contract declares one alternate evidence path; never loop or force weak context.",
    "6. Treat tool or knowledge output as candidate evidence, not authority: verify argument roles, units, physical bounds, and consistency with the derivation before using it.",
    "7. For online routes, preserve the model's explicit final answer after evidence adjudication; an unrequested parser or conflicting tool result must not overwrite it.",
    "8. Preserve the requested final-answer format and keep answer provenance auditable.",
)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_under(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def relative_posix(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def clean_values(values: Iterable[str], *, limit: int, field: str) -> list[str]:
    cleaned: list[str] = []
    for value in values:
        text = " ".join(str(value).strip().split())
        if not text:
            continue
        if len(text) > limit:
            raise ValueError(f"{field} item exceeds {limit} characters")
        if text not in cleaned:
            cleaned.append(text)
    return cleaned


def validate_model_facing(entry: dict[str, Any]) -> None:
    values: list[str] = [
        str(entry["capability_id"]),
        str(entry["title"]),
        str(entry["use_when"]),
    ]
    for field in ("retrieval_terms", "steps", "resources", "guards"):
        values.extend(str(item) for item in entry.get(field, []))
    joined = "\n".join(values)
    for pattern in FORBIDDEN_MODEL_FACING_PATTERNS:
        if pattern.search(joined):
            raise ValueError(
                "Model-facing skill text contains forbidden benchmark or answer leakage "
                f"pattern: {pattern.pattern}"
            )


def load_clean_run(
    *,
    repo_root: Path,
    run_path: str | Path,
    variant_set: str,
) -> tuple[Path, dict[str, Any]]:
    resolved = resolve_under(repo_root, run_path)
    allowed_roots = (
        (repo_root / "outputs/chemistry_expert/heartbeat_explore").resolve(),
        (
            repo_root
            / "outputs/chemistry_expert/retrospective_open_benchmarks"
        ).resolve(),
    )
    if not any(
        resolved == allowed_root or allowed_root in resolved.parents
        for allowed_root in allowed_roots
    ):
        raise ValueError(
            "Run path is outside approved chemistry evidence roots: "
            f"{resolved}"
        )
    payload = json.loads(resolved.read_text(encoding="utf-8-sig"))
    summary = dict(payload.get("summary") or {})
    if int(summary.get("evaluated") or 0) <= 0:
        raise ValueError("Cannot promote a skill from an unevaluated run")
    if int(summary.get("frontier_gap_count") or 0) != 0:
        raise ValueError(
            "Cannot promote a skill until blocking frontier_gap_count is zero"
        )
    if summary.get("queued_event_path"):
        raise ValueError("Cannot promote a skill while a queue event remains unresolved")
    if summary.get("anti_leakage_redaction") is not True:
        raise ValueError("Clean run is missing the anti-leakage redaction assertion")
    actual_variant = str(summary.get("variant_set") or payload.get("variant_set") or "")
    if actual_variant != variant_set:
        raise ValueError(
            f"Variant mismatch: expected {variant_set!r}, found {actual_variant!r}"
        )
    return resolved, payload


def load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": "chemtester-compact-skill-registry/v1",
            "updated_at": None,
            "entries": [],
        }
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if payload.get("schema_version") != "chemtester-compact-skill-registry/v1":
        raise ValueError(f"Unsupported compact skill registry: {path}")
    payload["entries"] = list(payload.get("entries") or [])
    return payload


def compact_index_text(value: str, *, limit: int) -> str:
    text = " ".join(value.strip().split())
    if len(text) <= limit:
        return text
    shortened = text[: limit - 3].rsplit(" ", 1)[0].rstrip(" ,;:")
    return (shortened or text[: limit - 3]).rstrip() + "..."


def topic_index_path(capability_id: str, *, topic_prefix: str) -> str:
    return f"{topic_prefix.rstrip('/')}/{capability_id}.md"


def render_topic(entry: dict[str, Any]) -> str:
    lines = [
        f"# {entry['title']}",
        "",
        f"**Retrieve with:** {', '.join(entry['retrieval_terms'])}",
        "",
        f"**Use when:** {entry['use_when']}",
        "",
        "## Procedure",
        "",
        *[
            f"{index}. {step}"
            for index, step in enumerate(entry["steps"], start=1)
        ],
    ]
    if entry["resources"]:
        lines.extend(
            [
                "",
                "## Preferred Support",
                "",
                *[f"- {resource}" for resource in entry["resources"]],
            ]
        )
    if entry["guards"]:
        lines.extend(
            [
                "",
                "## Guards",
                "",
                *[f"- {guard}" for guard in entry["guards"]],
            ]
        )
    rendered = "\n".join(lines).rstrip() + "\n"
    if len(rendered) > MAX_TOPIC_CHARS:
        raise ValueError(
            f"Rendered topic skill exceeds detail limit: {len(rendered)} > "
            f"{MAX_TOPIC_CHARS} characters"
        )
    line_count = len(rendered.splitlines())
    if line_count > MAX_TOPIC_LINES:
        raise ValueError(
            f"Rendered topic skill exceeds detail limit: {line_count} > "
            f"{MAX_TOPIC_LINES} lines"
        )
    return rendered


def render_skill(
    entries: list[dict[str, Any]],
    *,
    topic_prefix: str = "L2_principles/chemtester_gap_skills",
) -> str:
    lines = [
        "# ChemTester Compact Chemistry Skill",
        "",
        "Use this guide as a high-signal entrance into local chemistry knowledge and tools.",
        "When an entry applies, search its linked detail document before using the procedure.",
        "Irrelevant retrieval must not override sound chemistry reasoning.",
        "",
        "## Core Workflow",
        "",
        *CORE_WORKFLOW,
        "",
        "## Active Capability Index",
        "",
    ]
    if not entries:
        lines.append("No verified gap-specific capability has been promoted yet.")
    for entry in sorted(entries, key=lambda item: str(item["capability_id"])):
        capability_id = str(entry["capability_id"])
        detail_path = topic_index_path(
            capability_id,
            topic_prefix=topic_prefix,
        )
        lines.extend(
            [
                f"### {entry['title']}",
                f"**Use when:** {compact_index_text(entry['use_when'], limit=150)}",
                f"**Details:** `{detail_path}`",
                (
                    "**Search:** "
                    + compact_index_text(entry["retrieval_terms"][0], limit=60)
                ),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_skill_tree(
    entries: list[dict[str, Any]],
    *,
    topic_prefix: str = "L2_principles/chemtester_gap_skills",
) -> tuple[str, dict[str, str]]:
    index = render_skill(entries, topic_prefix=topic_prefix)
    topics = {
        topic_index_path(
            str(entry["capability_id"]),
            topic_prefix=topic_prefix,
        ): render_topic(entry)
        for entry in entries
    }
    return index, topics


def rebuild_skill_tree(
    *,
    repo_root: Path,
    skill_path: str | Path = DEFAULT_SKILL_PATH,
    registry_path: str | Path = DEFAULT_REGISTRY_PATH,
    topic_dir: str | Path = DEFAULT_TOPIC_DIR,
) -> dict[str, Any]:
    resolved_skill = resolve_under(repo_root, skill_path)
    resolved_registry = resolve_under(repo_root, registry_path)
    resolved_topic_dir = resolve_under(repo_root, topic_dir)
    memory_root = (repo_root / "chem-memory").resolve()
    if memory_root not in resolved_topic_dir.parents:
        raise ValueError("Topic skill directory must be under chem-memory")
    registry = load_registry(resolved_registry)
    entries = list(registry["entries"])
    for entry in entries:
        validate_model_facing(entry)
    topic_prefix = relative_posix(memory_root, resolved_topic_dir)
    rendered, topics = build_skill_tree(entries, topic_prefix=topic_prefix)
    for relative_path, text in topics.items():
        write_text(memory_root / relative_path, text)
    write_text(resolved_skill, rendered)
    return {
        "skill_path": relative_posix(repo_root, resolved_skill),
        "skill_sha256": sha256_path(resolved_skill),
        "topic_dir": relative_posix(repo_root, resolved_topic_dir),
        "topic_paths": sorted(topics),
        "entry_count": len(entries),
        "rendered_char_count": len(rendered),
        "rendered_line_count": len(rendered.splitlines()),
    }


def promote_skill(
    *,
    repo_root: Path,
    cycle_id: str,
    variant_set: str,
    run_path: str | Path,
    capability_id: str,
    title: str,
    retrieval_terms: Iterable[str],
    use_when: str,
    steps: Iterable[str],
    resources: Iterable[str] = (),
    guards: Iterable[str] = (),
    skill_path: str | Path = DEFAULT_SKILL_PATH,
    registry_path: str | Path = DEFAULT_REGISTRY_PATH,
    topic_dir: str | Path = DEFAULT_TOPIC_DIR,
    receipt_dir: str | Path = DEFAULT_RECEIPT_DIR,
) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{2,63}", cycle_id):
        raise ValueError("cycle_id must be 3-64 ASCII letters, digits, '_' or '-'")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,63}", capability_id):
        raise ValueError(
            "capability_id must be 3-64 lowercase letters, digits, '_' or '-'"
        )
    resolved_run, _ = load_clean_run(
        repo_root=repo_root,
        run_path=run_path,
        variant_set=variant_set,
    )
    resolved_skill = resolve_under(repo_root, skill_path)
    resolved_registry = resolve_under(repo_root, registry_path)
    resolved_topic_dir = resolve_under(repo_root, topic_dir)
    resolved_receipt_dir = resolve_under(repo_root, receipt_dir)
    memory_root = (repo_root / "chem-memory").resolve()
    if memory_root not in resolved_topic_dir.parents:
        raise ValueError("Topic skill directory must be under chem-memory")

    entry = {
        "capability_id": capability_id,
        "title": " ".join(title.strip().split()),
        "retrieval_terms": clean_values(
            retrieval_terms,
            limit=100,
            field="retrieval_terms",
        ),
        "use_when": " ".join(use_when.strip().split()),
        "steps": clean_values(steps, limit=2_000, field="steps"),
        "resources": clean_values(resources, limit=500, field="resources"),
        "guards": clean_values(guards, limit=1_000, field="guards"),
    }
    if not entry["title"] or len(entry["title"]) > 100:
        raise ValueError("title must contain 1-100 characters")
    if not entry["use_when"] or len(entry["use_when"]) > 1_000:
        raise ValueError("use_when must contain 1-1000 characters")
    if not 1 <= len(entry["retrieval_terms"]) <= 6:
        raise ValueError("Provide 1-6 retrieval terms")
    if not 1 <= len(entry["steps"]) <= 5:
        raise ValueError("Provide 1-5 procedure steps")
    if len(entry["resources"]) > 6:
        raise ValueError("Provide no more than 6 preferred resources")
    if len(entry["guards"]) > 4:
        raise ValueError("Provide no more than 4 guards")
    validate_model_facing(entry)

    registry = load_registry(resolved_registry)
    entries = list(registry["entries"])
    existing_index = next(
        (
            index
            for index, candidate in enumerate(entries)
            if candidate.get("capability_id") == capability_id
        ),
        None,
    )
    timestamp = now_iso()
    evidence = {
        "variant_set": variant_set,
        "run_path": relative_posix(repo_root, resolved_run),
        "run_sha256": sha256_path(resolved_run),
        "verified_at": timestamp,
    }
    if existing_index is None:
        entry["created_at"] = timestamp
        entry["updated_at"] = timestamp
        entry["evidence"] = [evidence]
        entries.append(entry)
    else:
        current = dict(entries[existing_index])
        prior_evidence = list(current.get("evidence") or [])
        prior_evidence = [
            item
            for item in prior_evidence
            if not (
                item.get("variant_set") == variant_set
                and item.get("run_path") == evidence["run_path"]
            )
        ]
        entry["created_at"] = current.get("created_at") or timestamp
        entry["updated_at"] = timestamp
        entry["evidence"] = (prior_evidence + [evidence])[-MAX_EVIDENCE_PER_ENTRY:]
        entries[existing_index] = entry

    topic_prefix = relative_posix(memory_root, resolved_topic_dir)
    rendered, topics = build_skill_tree(entries, topic_prefix=topic_prefix)
    registry.pop("max_entries", None)
    registry.update(
        {
            "updated_at": timestamp,
            "entries": entries,
        }
    )
    for relative_path, text in topics.items():
        write_text(memory_root / relative_path, text)
    write_text(resolved_skill, rendered)
    write_json(resolved_registry, registry)

    receipt_path = resolved_receipt_dir / f"{cycle_id}.json"
    existing_receipt: dict[str, Any] = {}
    if receipt_path.exists():
        existing_receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
        if existing_receipt.get("evidence_run_path") != evidence["run_path"]:
            raise ValueError(
                "A cycle receipt already exists for a different evidence run"
            )
    capability_ids = sorted(
        {
            *list(existing_receipt.get("capability_ids") or []),
            capability_id,
        }
    )
    receipt = {
        "schema_version": "chemtester-frontier-skill-receipt/v1",
        "cycle_id": cycle_id,
        "updated_at": timestamp,
        "status": "updated",
        "variant_set": variant_set,
        "evidence_run_path": evidence["run_path"],
        "evidence_run_sha256": evidence["run_sha256"],
        "skill_path": relative_posix(repo_root, resolved_skill),
        "skill_sha256": sha256_path(resolved_skill),
        "registry_path": relative_posix(repo_root, resolved_registry),
        "registry_sha256": sha256_path(resolved_registry),
        "topic_dir": relative_posix(repo_root, resolved_topic_dir),
        "topic_paths": sorted(topics),
        "capability_ids": capability_ids,
        "entry_count": len(entries),
        "rendered_char_count": len(rendered),
        "rendered_line_count": len(rendered.splitlines()),
    }
    write_json(receipt_path, receipt)
    receipt["receipt_path"] = relative_posix(repo_root, receipt_path)
    return receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Promote or update one compact chemistry capability after a clean "
            "generated-frontier rerun."
        )
    )
    parser.add_argument("--cycle-id", required=True)
    parser.add_argument("--variant-set", required=True)
    parser.add_argument("--run-path", required=True)
    parser.add_argument("--capability-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--retrieval-term", action="append", required=True)
    parser.add_argument("--use-when", required=True)
    parser.add_argument("--step", action="append", required=True)
    parser.add_argument("--resource", action="append", default=[])
    parser.add_argument("--guard", action="append", default=[])
    parser.add_argument("--skill-path", default=str(DEFAULT_SKILL_PATH))
    parser.add_argument("--registry-path", default=str(DEFAULT_REGISTRY_PATH))
    parser.add_argument("--topic-dir", default=str(DEFAULT_TOPIC_DIR))
    parser.add_argument("--receipt-dir", default=str(DEFAULT_RECEIPT_DIR))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    receipt = promote_skill(
        repo_root=ROOT,
        cycle_id=args.cycle_id,
        variant_set=args.variant_set,
        run_path=args.run_path,
        capability_id=args.capability_id,
        title=args.title,
        retrieval_terms=args.retrieval_term,
        use_when=args.use_when,
        steps=args.step,
        resources=args.resource,
        guards=args.guard,
        skill_path=args.skill_path,
        registry_path=args.registry_path,
        topic_dir=args.topic_dir,
        receipt_dir=args.receipt_dir,
    )
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
