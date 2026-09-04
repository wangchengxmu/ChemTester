---
id: atomic.theory_subatomic_structure
layer: 2
title: Atomic Theory and Subatomic Structure
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/atomic_composition_tools.py
  - ../L4_reference/reference/subatomic-particle-reference.md
  - ../L5_examples/composition_nomenclature/case-weighted-average-atomic-mass.md
cross_links:
  - ./atomic_identity_formula_and_nomenclature.md
---

## Context
This principle captures the model foundation: atoms as structured entities (protons, neutrons, electrons) and composition laws from atomic theory.

## Core rules
- Atomic number (Z) defines element identity.
- Mass number (A) = protons + neutrons.
- Isotopes: same Z, different A.
- Average atomic mass is weighted by isotopic abundance.

## Formula
- `M_avg = Σ(m_i × f_i)` with `Σf_i = 1`

## Decision flow
1. Determine whether task is identity, isotope, or composition averaging.
2. Use weighted-average calculation path for isotopic datasets.
3. Pass composition outputs to formula/naming principle when needed.

## Implementations and data
- Calculation helpers: [L3 code](../L3_functions/atomic_composition_tools.py)
- Particle/notation lookup: [L4 reference](../L4_reference/reference/subatomic-particle-reference.md)
- Worked example: [L5 example](../L5_examples/composition_nomenclature/case-weighted-average-atomic-mass.md)
