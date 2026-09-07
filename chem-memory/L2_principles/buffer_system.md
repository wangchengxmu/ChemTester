---
id: acid_base.buffer_system
layer: 2
title: Buffer System (Mechanism + Rules)
stability: high
confidence: high
sources:
  - url: https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/14%3A_Acid-Base_Equilibria
    book_id: libretexts-chemistry-2e-openstax
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/buffer_calculator.py
  - ../L3_functions/buffer_calculators.py
  - ../L4_reference/buffer/protocol-buffer-design-and-prep.md
  - ../L4_reference/reference/equilibrium-constants-and-reference-datasets.md
  - ../L5_examples/buffer/case-phosphate-50mM-ph74.md
cross_links:
  - ./quantitative_measurement_and_uncertainty.md
---

## Context
Buffer systems are pH-control tools. They bridge equilibrium theory (L2), numerical design tools (L3), practical preparation constraints (L4), and real formulation examples (L5).

## Core model
A weak acid/base pair with its conjugate partner resists pH change under small perturbations.

- Henderson–Hasselbalch (idealized): `pH = pKa + log10([base]/[acid])`
- Pair match heuristic: best practical region near `pKa ± 1`
- Ratio controls target pH; total concentration influences capacity

## Decision flow
1. Choose candidate conjugate pair with pKa near target pH.
2. Compute required base/acid ratio for target pH.
3. Evaluate robustness (pair match + expected perturbation).
4. Pull pKa/reference constants from [L4 reference](../L4_reference/reference/equilibrium-constants-and-reference-datasets.md).
5. Execute preparation workflow in [L4 protocol](../L4_reference/buffer/protocol-buffer-design-and-prep.md).
6. Compare against prior [L5 cases](../L5_examples/buffer/case-phosphate-50mM-ph74.md).

## Direct implementations
- Solver interface: [L3 skill](../L3_functions/buffer_calculator.py)
- Calculators: [L3 code](../L3_functions/buffer_calculators.py)

## Limits
- Concentration-based formulas deviate at high ionic strength/activity effects.
- Large strong acid/base additions can invalidate small-perturbation approximations.

