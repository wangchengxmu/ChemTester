---
id: conformational.analysis
layer: 2
title: Conformational Analysis
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/conformation_tools.py
  - ../L4_reference/reference/conformation-energy-tables.md
cross_links:
  - ./alkane_nomenclature.md
  - ./stereochemistry_chirality.md
---

## Context
Conformational analysis is the study of the different spatial arrangements (conformations) a molecule can adopt by rotation about single bonds. Unlike isomers, conformers interconvert rapidly at room temperature. Understanding conformational energy helps predict molecular stability and reactivity.

## Key Concepts

### Definitions
- **Conformation**: 3D arrangement of atoms obtained by rotation about single bonds
- **Conformer (rotamer)**: A specific conformation
- **Conformational isomers**: Different conformations of the same molecule

### Energy and Stability
- Conformations have different energies
- Lower energy = more stable = more populated
- Energy differences typically 1-15 kJ/mol
- At room temperature, rapid interconversion occurs

## Ethane Conformations

### Staggered vs Eclipsed
```
Staggered (more stable)     Eclipsed (less stable)
     H    H                      H  H
      \  /                        \/
       C-C                        C-C
      /  \                        /\
     H    H                      H  H
```

### Energy Profile
```
Energy
  │    Eclipsed     Eclipsed
  │      ∧           ∧
  │     ╱ ╲         ╱ ╲
  │    ╱   ╲       ╱   ╲
  │   ╱     ╲     ╱     ╲
  │  ╱       ╲   ╱       ╲
  │Staggered  ╲ ╱Staggered ╲
  └──────────────────────────→ Dihedral angle
    0°   60°  120° 180°  240°
```

### Ethane Values
- **Torsional strain**: ~12 kJ/mol (3 eclipsing interactions)
- Each H-H eclipsing interaction: ~4 kJ/mol

## Butane Conformations

### Key Conformations
| Conformation | Dihedral Angle | Relative Energy |
|--------------|----------------|-----------------|
| Anti | 180° | Lowest (reference) |
| Gauche | ±60° | +3.8 kJ/mol |
| Eclipsed (CH₃-H) | 120° | ~+14 kJ/mol |
| Eclipsed (CH₃-CH₃) | 0° | ~+19 kJ/mol |

### Gauche Interaction
- Two methyl groups 60° apart
- Steric repulsion between methyl groups
- Higher energy than anti

### Anti Conformation
- Largest groups 180° apart
- Minimum steric repulsion
- Most stable

## Types of Strain

### Strain Energy Components
| Strain Type | Cause | Magnitude |
|-------------|-------|-----------|
| Torsional | Eclipsing interactions | ~4 kJ/mol per pair |
| Steric (van der Waals) | Atoms too close | Variable |
| Angle strain | Bond angles ≠ ideal | Large in small rings |
| Ring strain | Combined in cyclic systems | See cycloalkanes |

### Steric Strain Examples
- Gauche butane: 3.8 kJ/mol
- 1,3-diaxial interactions in cyclohexane: ~8 kJ/mol per interaction

## Cyclohexane Conformations

### Chair Conformation
- **Most stable** cyclohexane conformation
- All C-C-C angles = 109.5° (ideal tetrahedral)
- All bonds staggered
- Zero ring strain

### Axial and Equatorial Positions
```
        Axial (a)
          │
    H ─── C ─── H (equatorial)
          │
       (ring)
```

- **Axial**: Perpendicular to ring plane
- **Equatorial**: In ring plane
- 3 axial up, 3 axial down (alternating)
- 3 equatorial up, 3 equatorial down (alternating)

### Ring Flip
- Chair interconverts to another chair
- All axial → equatorial (and vice versa)
- Activation energy: ~45 kJ/mol
- Rapid at room temperature (~10⁵ flips/second)

### Monosubstituted Cyclohexane
- **Equatorial substituent preferred** (more stable)
- Axial substituent experiences 1,3-diaxial interactions
- A-value = Energy difference (axial - equatorial)

### A-Values (kJ/mol)
| Substituent | A-Value | Preference |
|-------------|---------|------------|
| -CH₃ | 7.3 | Strongly equatorial |
| -CH₂CH₃ | 7.5 | Strongly equatorial |
| -OH | 4.0 | Moderately equatorial |
| -F | 1.0 | Slightly equatorial |
| -Cl | 2.0 | Moderately equatorial |
| -C(CH₃)₃ | 23 | Very strongly equatorial |

## Cycloalkane Ring Strain

### Ring Strain Energy
| Ring | Strain (kJ/mol) | Major Cause |
|------|-----------------|-------------|
| Cyclopropane | 115 | Angle + torsional |
| Cyclobutane | 110 | Angle + torsional |
| Cyclopentane | 26 | Torsional |
| Cyclohexane | 0 | None |
| Cycloheptane | 26 | Torsional |
| Cyclooctane | 40 | Torsional + transannular |

### Baeyer Strain Theory (Historical)
- Predicted cyclopentane as most stable
- Incorrect - didn't account for non-planar conformations
- Cyclohexane avoids strain via chair conformation

## Disubstituted Cyclohexanes

### Cis vs Trans
- **Cis**: Both substituents on same side of ring
- **Trans**: Substituents on opposite sides

### Stability Rules
1. For 1,2- and 1,4-disubstituted: trans with both equatorial is most stable
2. For 1,3-disubstituted: cis with both equatorial is most stable
3. If one substituent must be axial, put the smaller one axial

## Decision Flow
1. Draw molecule with rotatable bonds identified
2. For acyclic: identify staggered conformations
3. For cyclic: draw chair conformation
4. Place substituents: prefer equatorial
5. Calculate relative energies using A-values
6. Predict equilibrium distribution

## Implementations and Data
- Conformation analyzer: [L3 code](../L3_functions/conformation_tools.py)
- Energy tables: [L4 reference](../L4_reference/reference/conformation-energy-tables.md)

## L3 Tool Call Directives

**Source:** `conformation_tools.py`

Conformational Analysis Tools - L3 Implementation

### Available functions:
- `calculate_ethane_barrier()` → float — Calculate the rotational barrier for ethane.
- `calculate_butane_energy(dihedral_angle: float)` → float — Calculate the energy of a butane conformation.
- `get_a_value(substituent: str)` → float — Get the A-value for a cyclohexane substituent.
- `predict_cyclohexane_conformation(substituent: str)` → str — Predict the preferred conformation of monosubstituted cyclohexane.
- `calculate_disubstituted_cyclohexane_energy(positions: Tuple[int, int], stereochemistry: str, substituents: Tuple[str, str])` → float — Calculate the energy of a disubstituted cyclohexane.
- `get_ring_strain(ring_size: int)` → float — Get the ring strain energy for a cycloalkane.
- `explain_ring_strain(ring_size: int)` → str — Explain the source of ring strain for a cycloalkane.
- `calculate_1_3_diaxial_interactions(substituent: str)` → float — Calculate the 1,3-diaxial strain for a substituent in axial position.
- `conformation_energy_profile(molecule: str)` → Dict[str, float] — Get energy profile for conformations of a simple molecule.
- `ring_flip_positions()` → Dict[str, str] — Describe the ring flip process in cyclohexane.
- `calculate_equilibrium_distribution(energy_difference: float, temperature: float)` → Tuple[float, float] — Calculate the equilibrium distribution between two conformers.
- `test_ethane_barrier()` →  — Test ethane rotational barrier calculation
- `test_a_values()` →  — Test A-value lookup
- `test_ring_strain()` →  — Test ring strain calculation
- `test_conformation_prediction()` →  — Test conformation prediction
- `test_equilibrium()` →  — Test equilibrium distribution calculation

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
