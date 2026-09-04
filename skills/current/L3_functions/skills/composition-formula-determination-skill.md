---
id: skill.composition_formula_determination
layer: 3
title: Skill — Composition & Formula Determination
up_links:
  - ../../L2_principles/composition_and_formula_determination.md
down_links:
  - ../code/formula_determination_tools.py
  - ../../L4_database/reference/formula-determination-reference.md
  - ../../L5_examples/stoichiometry/formula-determination/README.md
status: active
source_topics:
  - stoich.composition_formula_determination
---

Implemented functions (Pass-3):
- `percent_to_moles`
- `empirical_formula_subscripts`
- `molecular_formula_subscripts`

Internal helpers:
- ratio integerization via near-integer multiplier search
- subscript reduction by gcd

Guardrails:
- Missing atomic masses raise explicit errors
- Negative percentages rejected
- Non-integer molecular multipliers beyond tolerance are rejected
