---
id: chem.bond_strengths
layer: 2
title: Bond Strengths and Lattice Energy
source: Ch07.05
dependencies: [ionic_bonding, covalent_bonding]
stability: high
confidence: high
---

## Concept

Bond strength measured by energy required to break bonds. Lattice energy measures ionic bond strength.

## Core Formulas

### Bond Energy (Covalent)
```
D(X-Y) = ¦¤H for XY(g) ¡ú X(g) + Y(g)
```

### Reaction Enthalpy from Bond Energies
```
¦¤H = ¦²D(bonds broken) - ¦²D(bonds formed)
```

### Lattice Energy (Ionic)
```
¦¤H_lattice = C(Z?)(Z?) / R?

Where:
- C = constant (crystal structure)
- Z?, Z? = ion charges
- R? = interionic distance
```

### Born-Haber Cycle
```
¦¤H¡ãf = ¦¤H¡ãs + ?D + IE + EA - ¦¤H_lattice

Where:
- ¦¤H¡ãs = sublimation energy
- D = bond dissociation energy  
- IE = ionization energy
- EA = electron affinity
```

## Decision Tree

```
Estimating reaction enthalpy?
©À©¤ Have ¦¤H_f values? ¡ú Use Hess's Law
©¸©¤ Have bond energies? ¡ú Use ¦²D(broken) - ¦²D(formed)

Comparing lattice energies?
©À©¤ Higher charges ¡ú Higher lattice energy
©À©¤ Smaller ions ¡ú Higher lattice energy
©¸©¤ Same structure ¡ú Compare Z?Z?/R?
```

## Trends
```
Bond strength: Triple > Double > Single
Bond length:   Triple < Double < Single

Lattice energy increases with:
- Higher ion charges
- Smaller ion sizes
```

## Key Constraints
- Bond energies are averages (approximation)
- Lattice energies typically 600-4000 kJ/mol
- Covalent bond energies typically 150-400 kJ/mol
- Higher lattice energy ¡ú more stable ionic compound

## Problem Archetypes
1. Calculate ¦¤H from bond energies
2. Compare lattice energies
3. Born-Haber cycle calculations
4. Predict stability from bond/lattice energy

## L3 Tools
- `reaction_enthalpy_from_bonds(bonds_broken, bonds_formed)` ¡ú ¦¤H
- `lattice_energy_compare(Z1, Z2, r1, r2)` ¡ú ratio
- `born_haber_lattice(¦¤H_f, ¦¤H_s, D, IE, EA)` ¡ú ¦¤H_lattice

## L4 Reference
See `../L4_reference/bond_dissociation_energies.csv` for bond energy tables.

## L5 Examples
See `../L5_examples/intermolecular_forces/ for worked examples.


## Implementations

- Implementation: `../L3_functions/bond_strengths_tools.py`

## L3 Tool Call Directives


**Source:** `bond_strengths_tools.py`

L3 tool module for bond strengths tools

### Available functions:
- `get_bond_energy(atom1: str, atom2: str, bond_order: int)` → float — Get average bond energy for a bond.
- `reaction_enthalpy_from_bonds(bonds_broken: List[Tuple[str, str, int]], bonds_formed: List[Tuple[str, str, int]])` → float — Calculate reaction enthalpy from bond energies.
- `lattice_energy_ionic(z_cation: int, z_anion: int, distance_pm: float, reference_U, reference_z, reference_r)` → float — Estimate lattice energy from ion properties using Coulomb proportionality.
- `compare_lattice_energies(compounds: List[Dict])` → tuple — Compare lattice energies of multiple compounds.
- `born_haber_lattice(delta_h_f: float, delta_h_s: float, bond_d: float, ie: float, ea: float)` → float — Calculate lattice energy from Born-Haber cycle.
- `bond_strength_order(bonds: List[Tuple[str, str, int]])` → tuple — Rank bonds by strength.
- `multiple_bond_effect(atom1: str, atom2: str)` → dict — Show effect of multiple bonds on bond properties.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
