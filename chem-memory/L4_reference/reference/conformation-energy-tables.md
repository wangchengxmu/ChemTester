# Conformational Analysis Reference
[Source: Organic Chemistry OpenStax, Ch03-04]

## Torsional Strain Energies

### Eclipsing Interactions
| Interaction | Energy (kJ/mol) |
|-------------|----------------|
| H-H | 4.0 |
| H-CH₃ | 6.0 |
| CH₃-CH₃ | 11.0 |
| H-CH₂CH₃ | 7.0 |
| CH₃-CH₂CH₃ | 13.0 |

## Ethane Conformations

| Conformation | Dihedral Angle | Energy (kJ/mol) |
|--------------|----------------|-----------------|
| Staggered | 60°, 180°, 300° | 0 (reference) |
| Eclipsed | 0°, 120°, 240° | 12.0 |

**Rotational Barrier**: 12 kJ/mol

## Butane Conformations

| Conformation | Dihedral Angle | Energy (kJ/mol) | Stability |
|--------------|----------------|-----------------|-----------|
| Anti | 180° | 0.0 | Most stable |
| Gauche | ±60° | 3.8 | Stable |
| Eclipsed (CH₃-H) | ±120° | 14.0 | Unstable |
| Eclipsed (CH₃-CH₃) | 0° | 19.0 | Least stable |

## A-Values (Cyclohexane)

### Definition
A-value = Energy difference between axial and equatorial positions
- Positive A-value = equatorial preferred
- Larger A-value = stronger preference

### A-Value Table
| Substituent | A-Value (kJ/mol) | Preference |
|-------------|------------------|------------|
| H | 0.0 | None |
| F | 1.0 | Slight equatorial |
| CN | 0.8 | Slight equatorial |
| I | 1.7 | Slight equatorial |
| Cl, Br | 2.0 | Moderate equatorial |
| COOH | 2.9 | Moderate equatorial |
| OCH₃ | 2.5 | Moderate equatorial |
| OH | 4.0 | Moderate equatorial |
| NH₂ | 5.0 | Moderate equatorial |
| CH₃ | 7.3 | Strong equatorial |
| CH₂CH₃ | 7.5 | Strong equatorial |
| CH(CH₃)₂ | 8.8 | Strong equatorial |
| Ph | 12.5 | Very strong equatorial |
| C(CH₃)₃ | 23.0 | Very strong equatorial |

## Ring Strain Energies

| Ring Size | Strain (kJ/mol) | Major Cause |
|-----------|-----------------|-------------|
| Cyclopropane | 115 | Angle + torsional |
| Cyclobutane | 110 | Angle + torsional |
| Cyclopentane | 26 | Torsional |
| Cyclohexane | 0 | None (chair) |
| Cycloheptane | 26 | Torsional |
| Cyclooctane | 40 | Torsional + transannular |

## 1,3-Diaxial Interactions

| Substituent | Strain per Interaction (kJ/mol) | Total (2 interactions) |
|-------------|--------------------------------|------------------------|
| H | 0.0 | 0.0 |
| CH₃ | 3.8 | 7.6 |
| CH₂CH₃ | 4.0 | 8.0 |
| OH | 2.1 | 4.2 |
| Cl | 1.0 | 2.0 |

## Cyclohexane Chair Conformation

### Key Features
- All C-C-C angles = 109.5° (ideal tetrahedral)
- All bonds staggered
- Zero ring strain
- Two types of positions: axial and equatorial

### Axial vs Equatorial
| Feature | Axial | Equatorial |
|---------|-------|------------|
| Orientation | Perpendicular to ring plane | In ring plane |
| Steric hindrance | 1,3-diaxial interactions | Less hindered |
| Stability (substituted) | Less stable | More stable |

### Ring Flip
- Chair ↔ Chair interconversion
- All axial → equatorial positions
- All equatorial → axial positions
- Barrier: ~45 kJ/mol
- Rate: ~10⁵ flips/second at 25°C

## Disubstituted Cyclohexanes

### Stability Rules
| Substitution Pattern | Most Stable Isomer |
|---------------------|-------------------|
| 1,2-disubstituted | Trans (both equatorial possible) |
| 1,3-disubstituted | Cis (both equatorial possible) |
| 1,4-disubstituted | Trans (both equatorial possible) |

### Energy Calculation
- Sum A-values for axial substituents
- Lower energy = more stable
- Consider both possible chair conformations

## Conformation Energy Profile

### Ethane
```
Energy (kJ/mol)
  │
12├─────┐     ┌─────┐     ┌─────
  │     │     │     │     │
  │     │     │     │     │
 0├─────┴─────┴─────┴─────┴─────→ Dihedral angle
   0°   60°  120° 180° 240° 300°
   E    S     E    S     E    S
```

### Butane
```
Energy (kJ/mol)
  │
19├──┐                    ┌──
  │  │                    │
14├──┤      ┌──┐  ┌──┐   ┌──┤
  │  │      │  │  │  │   │  │
 4├──┤  ┌───┤  ├──┤  ├───┤  ├──
  │  │  │   │  │  │  │   │  │
 0├──┴──┴───┴──┴──┴───┴──┴──┴──→
   0°  60° 120° 180° 240° 300°
   E    G    E     A    E    G

E = Eclipsed, G = Gauche, A = Anti
```

## Equilibrium Distribution

### Boltzmann Distribution
```
K = exp(-ΔG/RT)

Where:
K = equilibrium constant
ΔG = free energy difference (kJ/mol)
R = 8.314 × 10⁻³ kJ/(mol·K)
T = temperature (K)
```

### Example: Methylcyclohexane (A = 7.3 kJ/mol)
At 298 K:
- Fraction equatorial = 95%
- Fraction axial = 5%

## Decision Tree: Predicting Major Conformation

```
1. Draw chair conformation
2. Place substituent(s)
   │
   ├─ Monosubstituted?
   │   └─ Place substituent equatorial (lower energy)
   │
   └─ Disubstituted?
       │
       ├─ Calculate energy for both chair conformations
       │   - Sum A-values for axial substituents
       │
       └─ Lower total energy = major conformation
```
