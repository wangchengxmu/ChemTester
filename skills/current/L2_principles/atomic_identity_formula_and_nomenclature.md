---
id: composition.atomic_formula_nomenclature
layer: 2
title: Atomic Identity, Formula Logic, and Nomenclature
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/atomic_composition_tools.py
  - ../L3_functions/atomic_composition_tools.py
  - ../L4_reference/composition_nomenclature/routine-formula-and-name-validation.md
  - ../L4_reference/reference/composition-common-ions-and-charges.md
  - ../L4_reference/reference/composition-nomenclature-decision-table.md
  - ../L5_examples/composition_nomenclature/case-fecl3-naming-charge-check.md
  - ../L5_examples/composition_nomenclature/case-empirical-formula-from-moles-example.md
  - ../L5_examples/composition_nomenclature/case-ionic-charge-balance-ca3po42-example.md
cross_links:
  - ./buffer_system.md
---

## Context
This principle controls representation integrity: how atomic identity, formulas, composition constraints, and names are translated consistently.

## Core equations and constraints

1. **Average atomic mass**
   - `M_avg = Σ(m_i × f_i)` where `Σf_i = 1`

2. **Empirical formula derivation**
   - Convert measured composition to mole ratios.
   - Normalize by smallest mole value.
   - Scale to nearest integer ratio if needed.

3. **Charge neutrality for ionic compounds**
   - `Σ(z_i × n_i) = 0`

4. **Naming constraint**
   - Naming step is valid only after composition and charge constraints pass.

## Decision flow (solver)

1. Determine problem subtype:
   - isotope/atomic mass
   - formula derivation
   - ionic composition + naming
2. Run corresponding L3 computation.
3. Validate constraints:
   - fraction sum check
   - near-integer mole ratio check
   - charge neutrality check
4. Apply naming decision table from [L4 nomenclature table](../L4_reference/reference/composition-nomenclature-decision-table.md).
5. Provide final answer with validation trace.

## Edge cases
- Mole ratios close to half/third fractions (need scaling before rounding).
- Variable-charge metals require Roman numeral disambiguation.
- Polyatomic ions should be treated as grouped units in neutrality checks.

## Implementations and data
- Tool implementation: [L3 code](../L3_functions/atomic_composition_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/atomic_composition_tools.py)
- Common ions and charges: [L4 ion table](../L4_reference/reference/composition-common-ions-and-charges.md)
- Naming logic table: [L4 decision table](../L4_reference/reference/composition-nomenclature-decision-table.md)
- Worked examples: [L5 Ch02 examples](../L5_examples/composition_nomenclature/)

For acid-base context integration, follow [L2 buffer system](buffer_system.md).

