---
id: skill.amount_conversion
layer: 3
title: Skill — Amount Conversion
up_links:
  - ../../L2_principles/amount_mole_mass_particle_conversion.md
down_links:
  - ../code/amount_conversion_tools.py
  - ../../L4_database/reference/amount-conversion-reference.md
  - ../../L5_examples/stoichiometry/amount-conversion/README.md
status: active
source_topics:
  - stoich.amount_conversion
---

Implemented functions (Pass-3):
- `mass_to_moles`
- `moles_to_mass`
- `moles_to_particles`
- `particles_to_moles`
- `convert_amount` (generic bridge among mass/moles/particles)
- `sigfig_round`

Guardrails:
- Reject non-positive molar mass
- Require molar mass for any mass-domain conversion
- Validate quantity types (`mass_g`, `moles`, `particles`)
