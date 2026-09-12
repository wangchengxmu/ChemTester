import json
from pathlib import Path


def test_active_solubility_scope_is_consistent():
    root = Path(__file__).resolve().parents[1]
    registry = json.loads((root / "chem-memory/L2_principles/chemtester_compact_problem_solving_skill.registry.json").read_text(encoding="utf-8"))
    entry = next(e for e in registry["entries"] if e["capability_id"] == "coupled_solubility_acid_base_regression")
    step = entry["steps"][2]
    for guard in ("1:1 salt", "single anion-protonation", "no common-ion", "competing complexation", "activity-coefficient", "equilibrium free", "full coupled balances"):
        assert guard in step
    for relative in (
        ".agents/skills/chem-aqueous-equilibria/references/coupled_solubility_acid_base_regression.md",
        "chem-memory/L2_principles/chemtester_gap_skills/coupled_solubility_acid_base_regression.md",
    ):
        assert "3. " + step in (root / relative).read_text(encoding="utf-8")
