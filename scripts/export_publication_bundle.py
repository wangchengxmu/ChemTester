#!/usr/bin/env python3
"""Export a reviewable ChemTester data-and-skill publication bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any


DEVELOPMENT_SCHEMA = "chemtester-skill-development-family/v1"
DEVELOPMENT_MANIFEST_SCHEMA = "chemtester-skill-development-manifest/v1"
EVALUATION_SCHEMA = "chemtester-evaluation-question/v1"
EVALUATION_MANIFEST_SCHEMA = "chemtester-evaluation-manifest/v1"
LOCAL_PATH_PATTERN = re.compile(r"^(?:[A-Za-z]:[\\/]|/Users/|/home/)")
TEXT_SKILL_SUFFIXES = {".json", ".jsonl", ".md", ".py", ".txt", ".yaml", ".yml"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="ChemTester checkout containing outputs/ and chem-memory/.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Empty or new directory that will receive data/ and skills/.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_bytes(payload.encode("utf-8"))


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for record in records
    )
    path.write_bytes(payload.encode("utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def sanitize_local_paths(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: sanitize_local_paths(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_local_paths(item) for item in value]
    if isinstance(value, str) and LOCAL_PATH_PATTERN.match(value):
        normalized = value.replace("\\", "/")
        return f"local-source-redacted/{normalized.rsplit('/', 1)[-1]}"
    return value


def normalize_text_file(path: Path) -> bool:
    if path.suffix.casefold() not in TEXT_SKILL_SUFFIXES:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(normalized.encode("utf-8"))
    return True


def is_gpqa_item(item: dict[str, Any]) -> bool:
    problem = item.get("problem") or {}
    metadata = problem.get("metadata") or {}
    labels = (
        item.get("dataset"),
        metadata.get("dataset"),
        metadata.get("hf_repo"),
    )
    return any("gpqa" in str(label).casefold() for label in labels if label)


def export_development_set(project_root: Path, output_root: Path) -> dict[str, Any]:
    source_root = (
        project_root
        / "outputs"
        / "chemistry_expert"
        / "retrospective_open_benchmarks"
    )
    manifest_path = source_root / "manifest.json"
    status_path = source_root / "latest_status.json"
    deduplication_path = source_root / "deduplication_audit.json"
    semantic_path = source_root / "semantic_deduplication_audit.json"

    manifest = load_json(manifest_path)
    status = load_json(status_path)
    deduplication = load_json(deduplication_path)
    semantic = load_json(semantic_path)

    if status.get("completed") != status.get("total_items"):
        raise ValueError("The retrospective development loop is not complete.")
    indices = status.get("completed_canonical_indices") or []
    if len(indices) != status.get("total_items"):
        raise ValueError("Canonical-index count does not match latest_status.total_items.")
    if deduplication.get("unique_item_count") != status.get("total_items"):
        raise ValueError("Deduplication unique count does not match active total.")

    records: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    repository_counts: Counter[str] = Counter()
    withheld_counts: Counter[str] = Counter()
    seen_problem_ids: set[str] = set()

    for index in indices:
        source_item = manifest["items"][index]
        problem = source_item.get("problem") or {}
        metadata = problem.get("metadata") or {}
        problem_id = source_item["problem_id"]
        if problem_id in seen_problem_ids:
            raise ValueError(f"Duplicate canonical problem_id: {problem_id}")
        seen_problem_ids.add(problem_id)

        dataset = str(source_item.get("dataset") or metadata.get("dataset") or "unknown")
        repository = str(metadata.get("hf_repo") or "unknown")
        source_counts[dataset] += 1
        repository_counts[repository] += 1

        record: dict[str, Any] = {
            "schema_version": DEVELOPMENT_SCHEMA,
            "canonical_index": index,
            "problem_id": problem_id,
            "variant_set": source_item.get("variant_set"),
            "dataset": dataset,
            "source_repository": repository,
            "source_question_id": source_item.get("source_question_id"),
            "problem_signature": source_item.get("problem_signature"),
            "source_run_sha256": source_item.get("source_run_sha256"),
            "source_run_created_at": source_item.get("source_run_created_at"),
            "duplicate_problem_ids": source_item.get("duplicate_problem_ids") or [],
        }

        if is_gpqa_item(source_item):
            reason = "upstream-gpqa-no-online-example-disclosure"
            withheld_counts[reason] += 1
            record.update(
                {
                    "content_status": "withheld",
                    "content_withheld_reason": reason,
                    "question_sha256": canonical_hash(problem.get("question")),
                    "benchmark_key_sha256": canonical_hash(
                        {
                            "answer": problem.get("answer"),
                            "expected_answer": problem.get("expected_answer"),
                            "options": problem.get("options"),
                        }
                    ),
                }
            )
        else:
            record.update(
                {
                    "content_status": "included-private-preview",
                    "problem": sanitize_local_paths(problem),
                }
            )
        records.append(record)

    target = output_root / "data" / "skill_development"
    records_path = target / "canonical_families_3086.jsonl"
    write_jsonl(records_path, records)
    release_manifest = {
        "schema_version": DEVELOPMENT_MANIFEST_SCHEMA,
        "description": (
            "Canonical question families used for retrospective external-memory and skill "
            "development. This is not model-weight training data."
        ),
        "record_count": len(records),
        "content_included_count": sum(
            record["content_status"] == "included-private-preview" for record in records
        ),
        "content_withheld_count": sum(
            record["content_status"] == "withheld" for record in records
        ),
        "withheld_reason_counts": dict(sorted(withheld_counts.items())),
        "dataset_counts": dict(sorted(source_counts.items())),
        "source_repository_counts": dict(sorted(repository_counts.items())),
        "raw_archival_item_count": manifest.get("item_count"),
        "duplicate_items_skipped": deduplication.get("duplicate_item_count"),
        "duplicate_group_count": deduplication.get("duplicate_group_count"),
        "deduplication_schema": deduplication.get("schema_version"),
        "semantic_deduplication_schema": semantic.get("schema_version"),
        "semantic_auto_approved_pair_count": semantic.get("auto_approved_pair_count"),
        "semantic_borderline_pair_count": semantic.get("borderline_pair_count"),
        "semantic_applied_pair_count": semantic.get("approved_pair_count"),
        "records_sha256": sha256_file(records_path),
        "source_artifact_hashes": {
            "manifest.json": sha256_file(manifest_path),
            "latest_status.json": sha256_file(status_path),
            "deduplication_audit.json": sha256_file(deduplication_path),
            "semantic_deduplication_audit.json": sha256_file(semantic_path),
        },
    }
    write_json(target / "manifest.json", release_manifest)
    return release_manifest


def export_evaluation_set(project_root: Path, output_root: Path) -> dict[str, Any]:
    source_root = (
        project_root / "outputs" / "chemistry_expert" / "acceptance" / "sealed_v1"
    )
    performer_path = source_root / "performer_manifest.json"
    evaluator_path = source_root / "evaluator_gold.json"
    seal_path = source_root / "seal.json"
    performer = load_json(performer_path)
    evaluator = load_json(evaluator_path)
    seal = load_json(seal_path)

    expected_performer_sha = seal.get("performer_manifest_sha256")
    expected_evaluator_sha = seal.get("evaluator_gold_sha256")
    if sha256_file(performer_path) != expected_performer_sha:
        raise ValueError("Performer manifest no longer matches the immutable seal.")
    if sha256_file(evaluator_path) != expected_evaluator_sha:
        raise ValueError("Evaluator reference no longer matches the immutable seal.")

    benchmark_keys = evaluator.get("items") or {}
    gating_items = [item for item in performer.get("items") or [] if not item.get("diagnostic")]
    if len(gating_items) != 400 or seal.get("gating_item_count") != 400:
        raise ValueError("Expected exactly 400 sealed gating items.")

    records: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    for item in gating_items:
        item_id = item["item_id"]
        if item_id not in benchmark_keys:
            raise ValueError(f"Missing benchmark key for {item_id}")
        key = benchmark_keys[item_id]
        if key.get("diagnostic"):
            raise ValueError(f"Gating item marked diagnostic in evaluator reference: {item_id}")
        source_counts[item["source_key"]] += 1
        records.append(
            {
                "schema_version": EVALUATION_SCHEMA,
                "item_id": item_id,
                "source_key": item["source_key"],
                "source_question_id": item.get("source_question_id"),
                "problem": sanitize_local_paths(item["problem"]),
                "provenance": sanitize_local_paths(item.get("provenance") or {}),
                "benchmark_key": {
                    "answer": key.get("answer"),
                    "correct_option_text": key.get("correct_option_text"),
                    "question_hash": key.get("question_hash"),
                },
            }
        )

    target = output_root / "data" / "evaluation" / "acceptance_v1"
    records_path = target / "questions_and_keys_400.jsonl"
    write_jsonl(records_path, records)
    shutil.copy2(seal_path, target / "original_seal.json")

    assets_source = source_root / "assets"
    assets_target = target / "assets"
    if assets_target.exists():
        shutil.rmtree(assets_target)
    shutil.copytree(assets_source, assets_target)
    asset_files = sorted(path for path in assets_target.rglob("*") if path.is_file())

    release_manifest = {
        "schema_version": EVALUATION_MANIFEST_SCHEMA,
        "description": "The 400 gating items from the formerly sealed ChemTester acceptance suite.",
        "record_count": len(records),
        "diagnostic_items_excluded": performer.get("diagnostic_item_count"),
        "source_counts": dict(sorted(source_counts.items())),
        "records_sha256": sha256_file(records_path),
        "asset_count": len(asset_files),
        "asset_hashes": {
            path.relative_to(target).as_posix(): sha256_file(path) for path in asset_files
        },
        "original_seal": seal,
        "publication_effect": (
            "Publication ends the suite's secrecy. Results produced after public disclosure must "
            "be labeled post-release and must not be pooled with pre-release controlled results."
        ),
    }
    write_json(target / "manifest.json", release_manifest)
    return release_manifest


def copy_skill_snapshot(project_root: Path, output_root: Path) -> dict[str, Any]:
    target_root = output_root / "skills" / "current"
    sources = {
        "L2_principles": project_root / "chem-memory" / "L2_principles",
        "L3_functions": project_root / "chem-memory" / "L3_functions",
    }
    if target_root.exists():
        shutil.rmtree(target_root)
    for name, source in sources.items():
        shutil.copytree(
            source,
            target_root / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.tmp"),
        )

    files = sorted(path for path in target_root.rglob("*") if path.is_file())
    normalized_text_file_count = sum(normalize_text_file(path) for path in files)
    snapshot = {
        "schema_version": "chemtester-public-skill-snapshot/v1",
        "file_count": len(files),
        "normalized_text_file_count": normalized_text_file_count,
        "binary_or_non_utf8_file_count": len(files) - normalized_text_file_count,
        "files": {
            path.relative_to(target_root).as_posix(): sha256_file(path) for path in files
        },
    }
    write_json(target_root / "snapshot_manifest.json", snapshot)
    return snapshot


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    output_root = args.output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    development = export_development_set(project_root, output_root)
    evaluation = export_evaluation_set(project_root, output_root)
    skills = copy_skill_snapshot(project_root, output_root)
    summary = {
        "schema_version": "chemtester-publication-bundle/v1",
        "development_record_count": development["record_count"],
        "development_content_withheld_count": development["content_withheld_count"],
        "evaluation_record_count": evaluation["record_count"],
        "evaluation_asset_count": evaluation["asset_count"],
        "skill_file_count": skills["file_count"],
    }
    write_json(output_root / "bundle_summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
