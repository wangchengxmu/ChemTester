---
id: chem.dissolution_process
layer: 2
title: The Dissolution Process and Solution Formation
source: Ch11.01
dependencies: [intermolecular_forces, thermochemistry]
stability: high
confidence: high
---

## Concept

Solutions form when solute particles become uniformly distributed in a solvent. Dissolution involves energy changes from breaking and forming intermolecular interactions.

## Core Formulas

### Enthalpy of Solution
```
ΔH_soln = ΔH_solute + ΔH_solvent + ΔH_mix

Where:
- ΔH_solute = energy to separate solute particles (endothermic, +)
- ΔH_solvent = energy to separate solvent particles (endothermic, +)
- ΔH_mix = energy from solute-solvent interactions (exothermic, -)
```

### Entropy Consideration
```
Spontaneous dissolution favored by:
1. Negative ΔH_soln (exothermic)
2. Positive ΔS (increased disorder)
3. ΔG = ΔH - TΔS < 0
```

## Decision Tree

```
Will dissolution occur?
├─ Check intermolecular forces
│   ├─ Similar forces (polar-polar, nonpolar-nonpolar) → Likely soluble
│   └─ Dissimilar forces → Likely insoluble
├─ Check energy balance
│   ├─ ΔH_mix > ΔH_solute + ΔH_solvent → Exothermic, favored
│   └─ ΔH_mix < ΔH_solute + ΔH_solvent → Endothermic
└─ Consider entropy
    └─ Always increases (favors dissolution)
```

## Key Constraints
- "Like dissolves like" rule
- Ideal solutions: ΔH_soln ≈ 0
- Temperature affects solubility differently for different substances

## Problem Archetypes
1. Predict if dissolution is spontaneous
2. Identify endo/exothermic dissolution
3. Rank solubilities in different solvents

## L3 Tools
- `predict_solubility(solute, solvent)` → prediction
- `dissolution_energy(components)` → ΔH_soln
- `ideal_solution_check(mix)` → bool

## L4 Reference

## L5 Examples
See `../L5_examples/buffer/ for worked examples.
## Data Reference
- L4 Data: L4_reference/acid_base_constants.csv — Ka, Kb, pKa, pKb for common acids/bases
- L4 Data: L4_reference/solubility_products.csv — Ksp values for 30 sparingly soluble salts
- L4 Data: L4_reference/formation_constants.csv — Kf values for 24 metal complexes
