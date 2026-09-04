---
id: stoich.composition_formula_determination
layer: 2
title: Composition Analysis and Formula Determination
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/formula_determination_tools.py
  - ../L4_reference/reference/formula-determination-reference.md
  - ../L5_examples/stoichiometry/formula-determination/
cross_links:
  - ./atomic_identity_formula_and_nomenclature.md
  - ./amount_mole_mass_particle_conversion.md
status: active
---

## Problem intent
Route percent-composition, empirical-formula, and molecular-formula determination tasks.

## Canonical equations
- \(w_i(\%) = (m_i/m_{total})\times100\%\)
- Empirical ratio normalization from elemental moles.
- \(k = M_{molecular}/M_{empirical}\) and molecular subscripts = empirical subscripts \(\times k\).

## Decision stub
1. If given composition data, convert all elements to molar amounts.
2. Normalize by smallest amount.
3. Resolve near-fractional ratios with integer scaling.
4. If molecular mass provided, compute multiplier \(k\) and scale empirical formula.

## Pass-3 fill targets
- Fraction-tolerance policy (e.g., 1.33, 1.5, 1.67 patterns).
- Validation rules for non-integer multiplier anomalies.
- Worked examples with noisy input data.

## L3 Tool Call Directives


**Source:** `atomic_composition_tools.py`

L3 tool module for atomic composition tools

### Available functions:
- `average_atomic_mass(isotopes: list[tuple[float, float]])` → float — isotopes: [(mass, fractional_abundance), ...]
- `empirical_formula(element_mole_dict: dict[str, float])` → dict — N/A
- `charge_balance_ok(cation_charge: int, anion_charge: int, stoich: tuple[int, int])` → bool — N/A
- `simple_ionic_name(cation: str, cation_charge: int, anion: str)` → str — N/A
- `percent_composition(formula: str, target_element: str, atomic_masses: dict | None)` → float — Calculate mass percent of target_element in formula string.
- `molar_mass_from_formula(formula: str, atomic_masses: dict | None)` → float — Calculate molar mass from formula string. Handles parentheses like Ca3(PO4)2.
- `molarity(mass_g: float, molar_mass_gmol: float, volume_L: float)` → float — Calculate molarity from mass, molar mass, and solution volume.
- `empirical_formula_from_percent(percent_dict: dict[str, float], atomic_masses: dict | None)` → dict — Determine empirical formula from mass percentages.
- `parse_formula(f)` → any — Parse formula, return list of (element, count).
- `parse_group(s, pos)` → any — Parse formula from pos, return (mass, next_pos).

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
