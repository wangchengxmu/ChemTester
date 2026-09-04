---
id: chem.molecular_geometry_vsepr
layer: 2
title: Molecular Geometry and VSEPR Theory
source: Ch07.06
dependencies: [lewis_structures, covalent_bonding]
stability: high
confidence: high
---

## Concept

VSEPR theory predicts 3D molecular shape by minimizing electron pair repulsions.

## Core Formulas

### Electron-Pair Geometries
```
| Regions | Geometry           | Angles      |
|---------|--------------------|-------------| 
| 2       | Linear             | 180¡ã        |
| 3       | Trigonal planar    | 120¡ã        |
| 4       | Tetrahedral        | 109.5¡ã      |
| 5       | Trigonal bipyramidal | 90¡ã, 120¡ã |
| 6       | Octahedral         | 90¡ã         |
```

### Molecular Structure (from lone pairs)
```
| e? pairs | lone pairs | Molecular Structure |
|----------|------------|---------------------|
| 2        | 0          | Linear              |
| 3        | 0          | Trigonal planar     |
| 3        | 1          | Bent                |
| 4        | 0          | Tetrahedral         |
| 4        | 1          | Trigonal pyramidal  |
| 4        | 2          | Bent                |
| 5        | 0          | Trigonal bipyramidal|
| 5        | 1          | Seesaw              |
| 5        | 2          | T-shaped            |
| 5        | 3          | Linear              |
| 6        | 0          | Octahedral          |
| 6        | 1          | Square pyramidal    |
| 6        | 2          | Square planar       |
```

### Dipole Moment
```
¦Ì = Q ¡Á r
(¦Ì = dipole moment, Q = charge, r = distance)
```

### Repulsion Order
```
LP-LP > LP-BP > BP-BP
(lone pair > triple bond > double bond > single bond)
```

## Decision Tree

```
1. Draw Lewis structure
2. Count regions of electron density around central atom
   (single/double/triple bond = 1 region, lone pair = 1 region)
3. Determine electron-pair geometry
4. Count lone pairs on central atom
5. Determine molecular structure
6. Assess polarity:
   ©À©¤ All bonds nonpolar? ¡ú Nonpolar molecule
   ©À©¤ Symmetric bond dipoles cancel? ¡ú Nonpolar
   ©¸©¤ Bond dipoles don't cancel? ¡ú Polar
```

## Polarity Rules
```
Polar molecule requires:
1. At least one polar bond
2. Bond dipoles that don't cancel

Symmetric nonpolar: CO?, CH?, BF?, CCl?
Asymmetric polar: H?O, NH?, CHCl?
```

## Key Constraints
- Double/triple bonds count as ONE region
- Lone pairs occupy more space than bonds
- In trigonal bipyramidal, LP goes equatorial
- In octahedral with 2 LP, they go opposite

## Problem Archetypes
1. Predict electron-pair geometry
2. Predict molecular structure
3. Determine bond angles
4. Determine molecular polarity

## L3 Tools
- `electron_pair_geometry(regions)` ¡ú geometry_name
- `molecular_structure(regions, lone_pairs)` ¡ú structure_name
- `predict_bond_angles(regions, lone_pairs)` ¡ú angles
- `is_polar(bond_dipoles, geometry)` ¡ú bool
- `dipole_moment(Q, r)` ¡ú ¦Ì

## L4 Reference

## L5 Examples
See `../L5_examples/crystal_structures/ for worked examples.

## Implementations

- Implementation: `../L3_functions/molecular_geometry_tools.py`

## L3 Tool Call Directives

**Source:** `molecular_geometry_tools.py`
VSEPR geometry prediction, bond angles, hybridization, dipole moments.

### Available functions:
- `electron_pair_geometry(regions)` → str — Geometry name for 2–6 electron regions (linear/octahedral etc.)
- `molecular_structure(regions, lone_pairs)` → str — Molecular shape from regions and lone pairs
- `hybridization(regions)` → str — Hybridization type (sp/sp2/sp3/sp3d/sp3d2)
- `predict_bond_angles(regions, lone_pairs)` → list[float] — Approximate bond angles in degrees
- `is_polar_molecule(bond_dipoles, geometry)` → bool — True if net dipole ≠ 0
- `dipole_moment(charge, distance)` → float — Dipole in Debye (charge·distance × 4.803)
- `central_atom_position(geometry)` → str — Central atom position description

### Common errors:
- ❌ Passing regions > 6 or < 2 — not supported
- ❌ Bond dipoles not as [(x,y,z), ...] tuples — must be 3D vectors
- ❌ Confusing electron pair regions with molecular regions (subtract lone pairs)

## L3 Tool Call Directives

**Source:** `vsepr_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
