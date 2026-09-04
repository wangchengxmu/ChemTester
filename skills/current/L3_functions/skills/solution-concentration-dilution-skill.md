---
id: skill.solution_concentration_dilution
layer: 3
title: Skill — Solution Concentration & Dilution
up_links:
  - ../../L2_principles/solution_concentration_and_dilution.md
down_links:
  - ../code/solution_concentration_tools.py
  - ../../L4_database/reference/solution-concentration-reference.md
  - ../../L5_examples/stoichiometry/solution-concentration/README.md
status: active
source_topics:
  - stoich.solution_concentration_dilution
---

Implemented functions (Pass-3 slice):
- `molarity_from_moles`
- `moles_from_molarity`
- `dilution_v1` (C1V1=C2V2 with dilution guard)
- `percent_w_w`
- `ppm_from_mass_ratio`
- `ppb_from_mass_ratio`
- `ppm_mg_per_l_to_mg_per_l` (with/without density)

Guardrails:
- Reject non-positive solution mass/volume
- Reject invalid dilution requests (`C2 > C1`)
- Explicitly annotate aqueous density approximation when used
