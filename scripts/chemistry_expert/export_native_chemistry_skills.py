"""Reproducibly package chemistry procedures for native Codex skill discovery."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONFIG = "configs/native_chemistry_skills.json"
TEMPLATE = "scripts/chemistry_expert/native_skill_calculate.py"
MANIFEST_NAME = "native_chemistry_skills.manifest.json"
MANIFEST_SCHEMA = "chemtester-native-skill-export/v1"
REGISTRY_SCHEMA = "chemtester-compact-skill-registry/v1"
POLICY_SCHEMA = "chemtester-curated-support-policy/v1"
DEPENDS = {"atomic_composition_tools": ["unit_conversion_tools"],
           "equilibrium_constant_tools": ["equilibrium_tools"]}
OPTIONAL_DEPENDENCIES = {"buffer_calculator": ["numpy"],
                         "rate_law_solver": ["numpy", "scipy"],
                         "chemometrics_tools": ["numpy", "scipy", "scikit-learn"]}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True, sort_keys=True) + "\n").encode("utf-8")


def validate_partition(config: dict, registry: dict, policy: dict) -> None:
    if config.get("schema_version") != "chemtester-native-skill-packaging/v1":
        raise ValueError("Unsupported packaging schema")
    if registry.get("schema_version") != REGISTRY_SCHEMA:
        raise ValueError("Unsupported registry schema")
    if policy.get("schema_version") != POLICY_SCHEMA:
        raise ValueError("Unsupported support policy schema")
    entries = registry.get("entries", [])
    ids = [item["capability_id"] for item in entries]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Registry requires unique, nonempty capabilities")
    skills = config["skills"]
    names = [skill["name"] for skill in skills]
    if len(names) != len(set(names)) or any(not re.fullmatch(r"chem-[a-z0-9-]+", name) for name in names):
        raise ValueError("Skill names must be unique chem-* slugs")
    counts = Counter(item for skill in skills for item in skill["capabilities"])
    if set(counts) != set(ids) or any(count != 1 for count in counts.values()):
        raise ValueError(f"Capability partition mismatch: missing={sorted(set(ids)-set(counts))}, "
                         f"unknown={sorted(set(counts)-set(ids))}, "
                         f"duplicated={sorted(key for key, value in counts.items() if value != 1)}")
    allowed = set(policy["tools"]["core_modules"])
    for skill in skills:
        if not skill["capabilities"] or not skill["description"] or not skill["workflow"]:
            raise ValueError(f"Empty skill: {skill['name']}")
        if not 25 <= len(skill["short_description"]) <= 64:
            raise ValueError(f"UI description length: {skill['name']}")
        if len(skill["modules"]) != len(set(skill["modules"])) or not set(skill["modules"]) <= allowed:
            raise ValueError(f"Unsupported or repeated modules: {skill['name']}")


def calculator_catalog(module: str, data: bytes, policy: dict, omissions: dict | None = None) -> dict:
    tree = ast.parse(data.decode("utf-8-sig"))
    retired = set(policy["tools"].get("retired_tool_ids", []))
    patterns = [re.compile(value, re.I) for value in policy["tools"].get("quarantine_patterns", [])]
    result = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue
        tool_id = f"{module}.{node.name}"
        description = ast.get_docstring(node) or ""
        if tool_id in retired or node.name.startswith("test_") or not description.strip():
            continue
        if any(pattern.search(f"{tool_id} {description}") for pattern in patterns):
            continue
        if node.args.posonlyargs or node.args.vararg:
            if omissions is not None:
                omissions[tool_id] = "Positional-only or variadic interface is not supported by the keyword-only JSON adapter."
            continue
        result[tool_id] = {
            "signature": f"{node.name}({ast.unparse(node.args)})",
            "summary": description.splitlines()[0],
            "description": description,
            "contract": policy["tools"].get("contracts", {}).get(tool_id, {}),
            "scientific_validity": "not_independently_verified",
        }
    if not result:
        raise ValueError(f"No active documented calculators: {module}")
    return result


def procedure(entry: dict) -> str:
    # Explicit field allowlist: never serialize evidence, retired entries, or runs.
    lines = [f"# {entry['title']}", "", "## Applicability", "", entry["use_when"], "",
             "## Procedure", ""]
    lines.extend(f"{i}. {step}" for i, step in enumerate(entry["steps"], 1))
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {guard}" for guard in entry.get("guards", []))
    urls = [resource for resource in entry.get("resources", []) if re.fullmatch(r"https?://\S+", resource)]
    if urls:
        lines.extend(["", "## Source Leads", "", "Verify these sources for the present claim; a citation alone is not validation.", ""])
        lines.extend(f"- [Source {i}]({url})" for i, url in enumerate(urls, 1))
    lines.extend(["", "Only calculators listed in this package's calculator reference are callable here.",
                  "Other filenames in a procedure are historical pointers, not installed dependencies.",
                  "For missing empirical support, obtain an authoritative source or state the uncertainty.", ""])
    return "\n".join(lines)


def skill_markdown(skill: dict, entries: dict, tool_count: int) -> str:
    lines = ["---", f"name: {skill['name']}", f"description: {json.dumps(skill['description'])}",
             "---", "", f"# {skill['display_name']}", "", "## Workflow", ""]
    lines.extend(f"{i}. {step}" for i, step in enumerate(skill["workflow"], 1))
    lines.extend(["", "## Load Only Relevant Procedures", "",
                  "Open the matching reference below only when its applicability fits the task.",
                  "Use another skill for a separate subproblem; do not load this entire library by default.", ""])
    for capability in skill["capabilities"]:
        entry = entries[capability]
        lines.append(f"- [{entry['title']}](references/{capability}.md): {entry['use_when']}")
    if tool_count:
        lines.extend(["", "## Optional Calculators", "",
                      "Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.",
                      "Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required."])
    lines.extend(["", "## Evidence And Output", "",
                  "- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.",
                  "- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.",
                  "- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.",
                  "- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.",
                  "- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.", ""])
    return "\n".join(lines)


def calculator_reference(modules: list[str], tools: dict, dependencies: list[str]) -> str:
    lines = ["# Optional Calculators", "", "These are selected existing implementations, not independently certified chemistry.",
             "Read a function's complete description, units, domain, and return type before calling it.",
             "Legacy embedded empirical tables are approximate unless independently source-checked for the claim.",
             "Do not equate an implementation's self-reported validation with independent verification.", "",
             "## Invocation", "", "Resolve scripts relative to this skill folder, not the caller's working directory.",
             "Use the available Python 3.10+ environment. No provider key, Codex SDK, MCP service, or ChemTester checkout is required.", "",
             "```text", "python <skill-folder>/scripts/calculate.py --list",
             "python <skill-folder>/scripts/calculate.py --describe module.function",
             'python <skill-folder>/scripts/calculate.py --call module.function --arguments-json \'{"parameter": 1.0}\'',
             "```", "", "Replace the placeholder with an ID and arguments from its description.",
             "A JSON error and nonzero exit code mean no usable result. Never reinterpret an error as an answer.", ""]
    if dependencies:
        lines.extend(["## Optional Dependencies", "", ", ".join(f"`{name}`" for name in dependencies) + ".",
                      "Only the functions that import these packages require them. A `requirements.txt` records the package names; versions are not pinned or certified by this export.",
                      "Use an existing suitable environment or explain a missing dependency; do not silently install software.", ""])
    lines.extend(["## Function Index", "", "Read `--describe` for full signatures and contracts; this index is not a substitute.", ""])
    for module in modules:
        lines.extend([f"### {module}", ""])
        lines.extend(f"- `{key}`: {value['summary']}" for key, value in sorted(tools.items()) if key.startswith(module + "."))
        lines.append("")
    lines.extend(["Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.", ""])
    return "\n".join(lines)


def build(root: Path) -> tuple[dict[str, bytes], dict]:
    sources: dict[str, bytes] = {}

    def read(relative: str) -> bytes:
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError(f"Source escapes repository: {relative}")
        if relative not in sources:
            sources[relative] = path.read_bytes()
        return sources[relative]

    config = json.loads(read(CONFIG))
    # Packaging is deliberately limited to these sources, never question or run files.
    if config["registry"] != "chem-memory/L2_principles/chemtester_compact_problem_solving_skill.registry.json" or config["support_policy"] != "configs/chemistry_support_policy.json" or config["tools_root"] != "chem-memory/L3_functions":
        raise ValueError("Unexpected canonical source location")
    registry = json.loads(read(config["registry"]))
    policy = json.loads(read(config["support_policy"]))
    validate_partition(config, registry, policy)
    for tool_id, contract in config.get("calculator_contracts", {}).items():
        existing = policy["tools"].setdefault("contracts", {}).setdefault(tool_id, {})
        if set(existing) & set(contract):
            raise ValueError(f"Native contracts must not override existing gates: {tool_id}")
        existing.update(contract)
    contract_fields = {"max_items_combined", "result_type", "required_result_keys", "allowed_values", "positive_parameters"}
    for tool_id, contract in policy["tools"].get("contracts", {}).items():
        if set(contract) - contract_fields or contract.get("result_type", "object") != "object":
            raise ValueError(f"Unsupported calculator contract: {tool_id}")
    entries = {entry["capability_id"]: entry for entry in registry["entries"]}
    template = read(TEMPLATE)
    files: dict[str, bytes] = {}
    summaries = []
    omissions: dict[str, str] = {}
    exported_ids: set[str] = set()
    for skill in config["skills"]:
        prefix = skill["name"]
        catalog = {}
        bundled_modules = set(skill["modules"])
        for module in skill["modules"]:
            bundled_modules.update(DEPENDS.get(module, []))
            data = read(f"{config['tools_root']}/{module}.py")
            catalog.update(calculator_catalog(module, data, policy, omissions))
        for module in sorted(bundled_modules):
            files[f"{prefix}/scripts/tools/{module}.py"] = read(f"{config['tools_root']}/{module}.py")
        exported_ids.update(catalog)
        for capability in skill["capabilities"]:
            files[f"{prefix}/references/{capability}.md"] = procedure(entries[capability]).encode("utf-8")
        files[f"{prefix}/SKILL.md"] = skill_markdown(skill, entries, len(catalog)).encode("utf-8")
        ui = "interface:\n" + "\n".join(f"  {key}: {json.dumps(value)}" for key, value in {
            "display_name": skill["display_name"], "short_description": skill["short_description"],
            "default_prompt": f"Use ${prefix} for the relevant chemistry subproblem, loading only the necessary references."
        }.items()) + "\n"
        files[f"{prefix}/agents/openai.yaml"] = ui.encode("utf-8")
        dependencies = sorted({dep for module in bundled_modules for dep in OPTIONAL_DEPENDENCIES.get(module, [])})
        if catalog:
            files[f"{prefix}/scripts/calculate.py"] = template
            files[f"{prefix}/scripts/catalog.json"] = json_bytes({"schema_version": "native-chemistry-calculators/v1", "tools": catalog})
            files[f"{prefix}/references/calculators.md"] = calculator_reference(skill["modules"], catalog, dependencies).encode("utf-8")
        if dependencies:
            files[f"{prefix}/requirements.txt"] = ("\n".join(dependencies) + "\n").encode("utf-8")
        summaries.append({"name": prefix, "capabilities": skill["capabilities"], "calculator_count": len(catalog),
                          "advertised_modules": skill["modules"], "bundled_modules": sorted(bundled_modules),
                          "optional_dependencies": dependencies})
    if set(config.get("calculator_contracts", {})) - exported_ids:
        raise ValueError("Native calculator contract names an unexported function")
    for relative, data in files.items():
        if relative.endswith(".md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", data.decode("utf-8")):
                if target.startswith(("https://", "http://", "#")):
                    continue
                if (Path(relative).parent / target).as_posix() not in files:
                    raise ValueError(f"Broken package link: {relative} -> {target}")
    # Detect concurrent canonical edits before any package is written.
    for relative, data in sources.items():
        if (root / relative).read_bytes() != data:
            raise ValueError(f"Source changed during export: {relative}")
    manifest = {"schema_version": MANIFEST_SCHEMA, "capability_count": len(entries), "skill_count": len(summaries),
                "exporter_sha256": digest(Path(__file__).read_bytes()),
                "sources": {relative: digest(data) for relative, data in sorted(sources.items())},
                "files": {relative: digest(data) for relative, data in sorted(files.items())}, "skills": summaries,
                "source_resources": {key: entry.get("resources", []) for key, entry in entries.items()},
                "calculator_interface_omissions": omissions,
                "scope": "Procedures and active calculators only; source corpus retained. No historical answers, evidence records, model routing, or evaluation data exported."}
    return files, manifest


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def export(root: Path, output: Path, *, check: bool = False) -> dict:
    files, manifest = build(root)
    manifest_path = output.parent / MANIFEST_NAME
    old = json.loads(manifest_path.read_bytes()) if manifest_path.exists() else {}
    if old and old.get("schema_version") != MANIFEST_SCHEMA:
        raise ValueError("Unrecognized existing export manifest")
    stale = set(old.get("files", {})) - set(files)
    if stale:
        raise ValueError(f"Export would leave stale files; explicit retirement required: {sorted(stale)}")
    for relative, data in files.items():
        path = output / relative
        if not path.resolve().is_relative_to(output.resolve()):
            raise ValueError(f"Destination escapes skill root: {relative}")
        if path.exists() and path.read_bytes() != data:
            if check or digest(path.read_bytes()) != old.get("files", {}).get(relative):
                raise ValueError(f"Package differs or has local edits: {relative}")
        elif check and not path.is_file():
            raise ValueError(f"Missing package file: {relative}")
    for skill in manifest["skills"]:
        folder = output / skill["name"]
        if folder.exists():
            for path in folder.rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.relative_to(output).as_posix() not in files:
                    raise ValueError(f"Unexpected file; will not remove: {path}")
    if check:
        if old != manifest:
            raise ValueError("Export manifest is out of date")
    else:
        for relative, data in files.items():
            path = output / relative
            if not path.exists() or path.read_bytes() != data:
                atomic_write(path, data)
        atomic_write(manifest_path, json_bytes(manifest))
    return {"skills": manifest["skill_count"], "capabilities": manifest["capability_count"],
            "calculators": sum(item["calculator_count"] for item in manifest["skills"]),
            "files": len(files), "mode": "check" if check else "export", "output": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".agents" / "skills")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(export(ROOT, args.output.resolve(), check=args.check)))
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f"Export failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
