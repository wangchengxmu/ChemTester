#!/usr/bin/env python3
"""Validate counts, integrity, restrictions, and credential hygiene."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENT_ROOT = ROOT / "data" / "skill_development"
EVALUATION_ROOT = ROOT / "data" / "evaluation" / "acceptance_v1"
SKILL_ROOT = ROOT / "skills" / "current"
SECRET_PATTERNS = (
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9]{40,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
)
ABSOLUTE_PATH_PATTERN = re.compile(
    r"(?i)(?:[A-Z]:[\\/]+(?:Users|SynologyDrive)[\\/]|/(?:Users|home)/[^/]+/)"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def validate_development() -> None:
    manifest = load_json(DEVELOPMENT_ROOT / "manifest.json")
    records_path = DEVELOPMENT_ROOT / "canonical_families_3086.jsonl"
    records = load_jsonl(records_path)
    assert len(records) == manifest["record_count"] == 3086
    assert sha256(records_path) == manifest["records_sha256"]
    assert len({record["problem_id"] for record in records}) == 3086

    withheld = [record for record in records if record["content_status"] == "withheld"]
    included = [record for record in records if record["content_status"] != "withheld"]
    assert len(withheld) == manifest["content_withheld_count"] == 319
    assert len(included) == manifest["content_included_count"] == 2767
    for record in withheld:
        assert "gpqa" in record["source_repository"].casefold() or "gpqa" in record[
            "dataset"
        ].casefold()
        assert "problem" not in record
        assert len(record["question_sha256"]) == 64
        assert len(record["benchmark_key_sha256"]) == 64


def validate_evaluation() -> None:
    manifest = load_json(EVALUATION_ROOT / "manifest.json")
    records_path = EVALUATION_ROOT / "questions_and_keys_400.jsonl"
    records = load_jsonl(records_path)
    assert len(records) == manifest["record_count"] == 400
    assert sha256(records_path) == manifest["records_sha256"]
    assert len({record["item_id"] for record in records}) == 400
    assert all(not record["source_key"].startswith("diagnostic_") for record in records)
    assert sum(manifest["source_counts"].values()) == 400

    expected_assets = manifest["asset_hashes"]
    actual_assets = sorted(path for path in (EVALUATION_ROOT / "assets").rglob("*") if path.is_file())
    assert len(actual_assets) == manifest["asset_count"] == 50
    for path in actual_assets:
        relative = path.relative_to(EVALUATION_ROOT).as_posix()
        assert relative in expected_assets
        assert sha256(path) == expected_assets[relative]


def validate_skills() -> None:
    manifest = load_json(SKILL_ROOT / "snapshot_manifest.json")
    assert manifest["file_count"] == len(manifest["files"])
    for relative, expected_hash in manifest["files"].items():
        path = SKILL_ROOT / relative
        assert path.is_file(), relative
        assert sha256(path) == expected_hash, relative


def validate_hygiene() -> None:
    failures: list[str] = []
    validator_sources = {
        Path("scripts/export_publication_bundle.py"),
        Path("scripts/validate_release.py"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() == ".png":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(ROOT)
        if relative not in validator_sources and ABSOLUTE_PATH_PATTERN.search(text):
            failures.append(f"absolute path: {path.relative_to(ROOT)}")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            failures.append(f"credential candidate: {path.relative_to(ROOT)}")
    assert not failures, "\n".join(failures[:20])


def main() -> int:
    validate_development()
    validate_evaluation()
    validate_skills()
    validate_hygiene()
    summary = load_json(ROOT / "bundle_summary.json")
    assert summary["development_record_count"] == 3086
    assert summary["development_content_withheld_count"] == 319
    assert summary["evaluation_record_count"] == 400
    assert summary["evaluation_asset_count"] == 50
    print("ChemTester release validation passed.")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
