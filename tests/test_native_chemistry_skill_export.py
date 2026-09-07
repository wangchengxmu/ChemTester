import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts.chemistry_expert import export_native_chemistry_skills as exporter


@pytest.fixture
def fixture_root(tmp_path):
    root = tmp_path / "source"
    config = {
        "schema_version": "chemtester-native-skill-packaging/v1",
        "registry": "chem-memory/L2_principles/chemtester_compact_problem_solving_skill.registry.json",
        "support_policy": "configs/chemistry_support_policy.json",
        "tools_root": "chem-memory/L3_functions",
        "skills": [{"name": "chem-example", "display_name": "Example Chemistry",
                    "description": "Use for synthetic example calculations, not empirical claims.",
                    "short_description": "Synthetic chemistry test procedures",
                    "capabilities": ["example"], "modules": ["example_tools"],
                    "workflow": ["Check units and applicability."]}],
    }
    registry = {"schema_version": exporter.REGISTRY_SCHEMA, "entries": [
        {"capability_id": "example", "title": "Example", "use_when": "A synthetic example is needed.",
         "steps": ["Double the value."], "guards": ["Do not confuse execution with validation."],
         "resources": ["L2_principles/legacy.md", "https://example.org/source"],
         "evidence": [{"prediction": "DO_NOT_EXPORT_RECORD"}]}],
         "retired_entries": [{"title": "DO_NOT_EXPORT_RETIRED"}]}
    policy = {"schema_version": exporter.POLICY_SCHEMA, "tools": {
        "core_modules": ["example_tools"], "retired_tool_ids": ["example_tools.retired"],
        "quarantine_patterns": ["answer_key"], "contracts": {}}}
    data = {exporter.CONFIG: json.dumps(config), config["registry"]: json.dumps(registry),
            config["support_policy"]: json.dumps(policy),
            "chem-memory/L3_functions/example_tools.py": '''def double(value: float):
    """Double a synthetic value."""
    return value * 2

def retired(value):
    """Retired interface."""
    return value

def undocumented(value):
    return value

def test_helper():
    """Not a public chemistry tool."""
    return True

def answer_key():
    """Not an allowed function."""
    return 0

def variadic(*values):
    """Requires a positional API."""
    return values
'''}
    for relative, text in data.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    path = root / exporter.TEMPLATE
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(exporter.ROOT / exporter.TEMPLATE, path)
    return root, config, registry, policy


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "unknown", "schema", "module"])
def test_partition_fails_closed(fixture_root, mutation):
    _, config, registry, policy = fixture_root
    config = copy.deepcopy(config)
    if mutation == "missing":
        config["skills"][0]["capabilities"] = []
    elif mutation == "duplicate":
        config["skills"][0]["capabilities"] *= 2
    elif mutation == "unknown":
        config["skills"][0]["capabilities"].append("unknown")
    elif mutation == "schema":
        config["schema_version"] = "v99"
    else:
        config["skills"][0]["modules"] = ["unapproved"]
    with pytest.raises(ValueError):
        exporter.validate_partition(config, registry, policy)


def test_build_is_deterministic_and_excludes_evidence(fixture_root):
    root, _, _, _ = fixture_root
    first = exporter.build(root)
    assert first == exporter.build(root)
    files, manifest = first
    payload = b"\n".join(files.values())
    assert b"DO_NOT_EXPORT_RECORD" not in payload
    assert b"DO_NOT_EXPORT_RETIRED" not in payload
    assert b"L2_principles/legacy.md" not in payload
    assert manifest["source_resources"]["example"][0] == "L2_principles/legacy.md"
    assert manifest["capability_count"] == manifest["skill_count"] == 1
    catalog = json.loads(files["chem-example/scripts/catalog.json"])
    assert list(catalog["tools"]) == ["example_tools.double"]
    assert "example_tools.variadic" in manifest["calculator_interface_omissions"]


def test_export_check_and_local_edit_protection(fixture_root, tmp_path):
    root, _, _, _ = fixture_root
    output = tmp_path / "installed" / "skills"
    exporter.export(root, output)
    assert exporter.export(root, output, check=True)["mode"] == "check"
    skill = output / "chem-example/SKILL.md"
    skill.write_text("user edits", encoding="utf-8")
    with pytest.raises(ValueError, match="local edits"):
        exporter.export(root, output)
    assert skill.read_text() == "user edits"


def test_export_never_removes_unrecognized_files(fixture_root, tmp_path):
    root, _, _, _ = fixture_root
    output = tmp_path / "installed" / "skills"
    exporter.export(root, output)
    extra = output / "chem-example/custom.md"
    extra.write_text("keep", encoding="utf-8")
    with pytest.raises(ValueError, match="will not remove"):
        exporter.export(root, output)
    assert extra.read_text() == "keep"


def test_export_preserves_other_skills(fixture_root, tmp_path):
    root, _, _, _ = fixture_root
    output = tmp_path / "installed" / "skills"
    other = output / "other-skill/SKILL.md"
    other.parent.mkdir(parents=True)
    other.write_text("other instructions", encoding="utf-8")
    exporter.export(root, output)
    assert other.read_text() == "other instructions"


def test_calculator_is_portable(fixture_root, tmp_path):
    root, _, _, _ = fixture_root
    output = tmp_path / "installed" / "skills"
    exporter.export(root, output)
    command = [sys.executable, str(output / "chem-example/scripts/calculate.py"),
               "--call", "example_tools.double", "--arguments-json", '{"value": 3}']
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["result"] == 6


def test_actual_build_complete_and_source_hashes_match():
    files, manifest = exporter.build(exporter.ROOT)
    config = json.loads((exporter.ROOT / exporter.CONFIG).read_bytes())
    registry = json.loads((exporter.ROOT / config["registry"]).read_bytes())
    assert manifest["capability_count"] == len(registry["entries"])
    assert manifest["skill_count"] == 12
    assert all(exporter.digest((exporter.ROOT / path).read_bytes()) == digest
               for path, digest in manifest["sources"].items())
    assert all(exporter.digest(files[path]) == digest for path, digest in manifest["files"].items())
    for entry in registry["entries"]:
        assert sum(path.endswith(f"/references/{entry['capability_id']}.md") for path in files) == 1


def test_native_skill_frontmatter(tmp_path):
    validator_path = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    if not validator_path.exists():
        pytest.skip("Codex skill-creator validator is not installed on this machine")
    output = tmp_path / "packaged" / "skills"
    exporter.export(exporter.ROOT, output)
    for folder in output.iterdir():
        # Validator uses the platform default encoding; force a UTF-8 locale in its CLI instead.
        result = subprocess.run([sys.executable, "-X", "utf8", str(validator_path), str(folder)],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stdout + result.stderr


@pytest.fixture(scope="module")
def installed_native(tmp_path_factory):
    output = tmp_path_factory.mktemp("portable_native") / "skills"
    exporter.export(exporter.ROOT, output)
    return output


NATIVE_CONFIG = json.loads((exporter.ROOT / exporter.CONFIG).read_bytes())


@pytest.mark.parametrize("skill", [item["name"] for item in NATIVE_CONFIG["skills"] if item["modules"]])
def test_every_advertised_callable_imports_portably(installed_native, skill):
    script = r'''
import importlib.util, inspect, json, pathlib, sys
base = pathlib.Path(sys.argv[1]) / "scripts"
sys.path.insert(0, str(base / "tools"))
catalog = json.loads((base / "catalog.json").read_bytes())["tools"]
modules = {}
for tool_id in catalog:
    module, function = tool_id.split(".")
    if module not in modules:
        spec = importlib.util.spec_from_file_location("native_import_" + module, base / "tools" / (module + ".py"))
        loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
        modules[module] = loaded
    fn = getattr(modules[module], function)
    assert callable(fn), tool_id
    inspect.get_annotations(fn, eval_str=True)
print(json.dumps({"checked": len(catalog)}))
'''
    result = subprocess.run([sys.executable, "-X", "utf8", "-c", script, str(installed_native / skill)],
                            cwd=installed_native.parent, capture_output=True, text=True, timeout=45)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("skill,tool,arguments,expected", [
    ("chem-thermodynamics", "enthalpy_tools.heat_phase_change", {"moles": 2, "delta_H_phase": 10}, 20),
    ("chem-aqueous-equilibria", "acid_base_constants_tools.Ka_Kb_relationship", {"Ka": 1e-5}, None),
    ("chem-kinetics-reactors", "integrated_rate_law_tools.first_order_concentration", {"C0": 1, "k": .1, "t": 0}, 1),
    ("chem-organic-mechanisms", "functional_group_tools.get_naming_priority", {"group_name": "alcohol"}, None),
    ("chem-spectroscopy", "mass_spec_tools.fragment_mass", {"molecular_ion": 100, "lost_mass": 18}, 82),
    ("chem-inorganic-reactions", "atomic_composition_tools.molarity", {"mass_g": 18, "molar_mass_gmol": 18, "volume_L": .5}, 2),
    ("chem-analytical-quantitation", "density_tools.calculate_density", {"mass": 10, "volume": 2}, 5),
    ("chem-crystal-structures", "crystal_structures_tools.cubic_lattice_radius", {"edge_length": 4, "cell_type": "simple_cubic"}, 2),
    ("chem-safety-references", "hazardous_waste_compatibility.lookup_hazardous_waste_compatibility", {"group_a": 1, "group_b": 2}, None),
    ("chem-biomolecular-analysis", "chemometrics_tools.chromatography_resolution", {"tR1": 10, "tR2": 12, "w1": 1, "w2": 1}, 2),
    ("chem-biomolecular-analysis", "chemometrics_tools.confidence_interval", {"data": [1, 2, 3]}, None),
])
def test_synthetic_calculator_smoke(installed_native, skill, tool, arguments, expected):
    result = subprocess.run([sys.executable, "-X", "utf8", str(installed_native / skill / "scripts/calculate.py"),
                             "--call", tool, "--arguments-json", json.dumps(arguments)],
                            cwd=installed_native.parent, capture_output=True, text=True, timeout=45)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["scientific_validity"] == "not_independently_verified"
    if expected is not None:
        assert payload["result"] == pytest.approx(expected)


@pytest.mark.parametrize("arguments", [{"edge_length": 4, "cell_type": "sc"},
                                     {"edge_length": 0, "cell_type": "simple_cubic"}])
def test_lattice_bad_inputs_fail_instead_of_returning_zero(installed_native, arguments):
    result = subprocess.run([sys.executable, str(installed_native / "chem-crystal-structures/scripts/calculate.py"),
                             "--call", "crystal_structures_tools.cubic_lattice_radius",
                             "--arguments-json", json.dumps(arguments)],
                            cwd=installed_native.parent, capture_output=True, text=True, timeout=45)
    assert result.returncode == 1
    assert json.loads(result.stdout)["ok"] is False
