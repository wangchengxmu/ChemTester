---
name: chem-inorganic-reactions
description: "Use for inorganic reaction-network deduction, coordination composition and symmetry, redox balancing, periodic-property lookup, and condition-dependent metal speciation. Not for unit-cell geometry or aqueous buffer calculations."
---

# Inorganic Reactions

## Workflow

1. Maintain an explicit ledger of atoms, charge, electrons, oxidation state, ligands, and phase for each reaction stage.
2. Use all independent composition, gas, color, symmetry, and condition constraints; do not force a familiar species from one clue.
3. Require a cited table for exact empirical ordering. Distinguish bookkeeping oxidation state from physical charge and ligand-field assumptions from measured spin states.

## Load Only Relevant Procedures

Open the matching reference below only when its applicability fits the task.
Use another skill for a separate subproblem; do not load this entire library by default.

- [Inorganic Gas Trap Stoichiometry](references/inorganic_gas_trap_stoichiometry.md): Gas-analysis or inorganic decomposition tasks pass products through drying, carbon dioxide absorption, red-hot copper, or STP volume and pressure measurements.
- [Qualitative inorganic reaction-network deduction](references/qualitative_inorganic_constraint_deduction.md): Unlabeled aqueous samples, including prepared mixtures, must be identified from linked precipitate, gas, redox, and directed excess-reagent observations.
- [Exact tabulated periodic-property disambiguation](references/exact_tabulated_periodic_property_disambiguation.md): An element-ranking or multiple-choice task depends on an exact named periodic-property scale, especially for transition metals or candidate ties.
- [Condition-coupled spin, electron-configuration, and exact-geometry audit](references/pressure_coupled_spin_orbital_geometry.md): A coordination or organometallic problem couples electron-count rules, magnetic state, valence-orbital occupation, or an exact geometry claim across pressure, temperature, or another ligand-field perturbation.
- [Coordination-complex composition, topology, and stereochemical symmetry audit](references/coordination_salt_composition_symmetry_speciation.md): A mono- or polynuclear coordination-complex problem asks about composition or reaction balance, donor geometry or orbital types, chelate-ring sizes, local Δ/Λ configurations, metal-site equivalence, molecular symmetry, or stability claims.
- [F-block scorpionate condition and coordination audit](references/f_block_scorpionate_condition_speciation.md): An f-block coordination problem combines an element-identification clue, a poly(pyrazolyl)borate reagent, reaction conditions, and a requested metal, oxidation state, ligand set, or coordination number.
- [Atom-scaled redox half-reaction electron ledger](references/redox_half_reaction_atom_electron_ledger.md): A half-reaction must be balanced in acidic or basic medium, especially when a polyatomic reactant forms a molecular product containing multiple atoms of the redox-active element.
- [Constraint-first inorganic reaction, coefficient, and transformation audit](references/inorganic_reaction_constraint_ledger.md): An inorganic reaction or multi-process equation-selection problem requires product identification, balancing, coefficient-derived quantities, enforcement of verbal constraints such as phase, product count, compound type, or gas identity and count, or exact evaluation of whether a structural feature was created or merely retained.

## Optional Calculators

Read [calculator scope and availability](references/calculators.md) only if a numerical or structural operation would help.
Select and invoke a documented function yourself. No dispatcher, model router, or automatic tool loop is required.

## Evidence And Output

- Start from the user's actual structures, conditions, and requested quantity. If evidence is missing, ask for it or state a bounded assumption.
- Treat these procedures as conditional reasoning aids, not authority over the current evidence. Preserve equations, units, scope, and uncertainty.
- A successful calculator call is not independent scientific validation. Verify consequential empirical constants, safety claims, and exceptional chemistry against authoritative sources.
- Do not read benchmark answers, previous predictions, or evaluation logs to answer a question. Keep the model answer separate from a benchmark key and scientific adjudication.
- Missing optional references are a support limitation, not evidence that a reasoned answer is wrong. Do not invent the missing source.
