---
id: stoich.amount_conversion
layer: 2
title: Amount Conversion (Mole-Mass-Particle)
source: LibreTexts Chemistry 2e Ch03
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/amount_conversion_tools.py
  - ../L4_reference/reference/amount-conversion-reference.md
  - ../L5_examples/stoichiometry/amount-conversion/
cross_links:
  - ./quantitative_measurement_and_uncertainty.md
  - ./atomic_identity_formula_and_nomenclature.md
status: active
---

## Problem intent
Route problems that ask for conversion among mass, moles, particles, and formula/molar mass.

## Canonical equations
- \(n = m/M\)
- \(m = nM\)
- \(N = nN_A\), \(n = N/N_A\)

## Decision stub
1. Identify source quantity domain (mass / amount / particle count).
2. Identify target domain.
3. Determine required bridge constants (molar mass, Avogadro constant).
4. Execute minimum conversion chain with unit cancellation.

## Pass-3 fill targets
- Error handling for missing/ambiguous molar mass.
- Significant-figure propagation rules.
- Multi-step conversion edge cases.

## L3 Tool Call Directives


**Source:** `amount_conversion_tools.py`

L3 tool module for amount conversion tools

### Available functions:
- `mass_to_moles(mass_g: float, molar_mass_g_per_mol: float)` → float — N/A
- `moles_to_mass(moles: float, molar_mass_g_per_mol: float)` → float — N/A
- `moles_to_particles(moles: float)` → float — N/A
- `particles_to_moles(particles: float)` → float — N/A
- `convert_amount(value: float, from_type: str, to_type: str, molar_mass_g_per_mol: float | None)` → float — Generic converter among: mass_g, moles, particles.
- `dilution_volume(M1: float, M2: float, V2: float)` → float — Calculate V1 needed for dilution: M1*V1 = M2*V2.
- `dilution_final_conc(M1: float, V1: float, V2: float)` → float — Calculate final concentration after dilution: M2 = M1*V1/V2.
- `sigfig_round(value: float, sigfigs: int)` → float — N/A

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
