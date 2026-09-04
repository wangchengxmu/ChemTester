# L2 Topic: Conjugated Compounds and Diels-Alder

**Source**: Organic Chemistry (OpenStax) Ch14
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Conjugated dienes have alternating single and double bonds with delocalized π electrons. This leads to unique reactivity patterns including 1,2- vs 1,4-addition and the Diels-Alder cycloaddition reaction.

### Key Features
1. **Stability**: Conjugated dienes more stable than isolated
2. **Addition**: Both 1,2- and 1,4-products form
3. **Diels-Alder**: [4+2] cycloaddition to make cyclohexenes
4. **UV spectroscopy**: λmax indicates conjugation extent

---

## Core Principles

### 14.1: Stability of Conjugated Dienes
- Delocalization of π electrons
- Bond length equalization
- Lower heat of hydrogenation

### 14.2-14.3: Electrophilic Addition
- **Allylic carbocation** intermediate
- **1,2-addition**: Kinetic product
- **1,4-addition**: Thermodynamic product
- Temperature controls product ratio

### 14.4-14.5: Diels-Alder Reaction
- **[4+2] cycloaddition**
- Diene (4π electrons) + Dienophile (2π electrons)
- Concerted, pericyclic mechanism
- Stereospecific (cis-addition)
- Endo selectivity

### 14.7-14.8: UV Spectroscopy
- λmax increases with conjugation
- Wood's rule for λmax estimation
- Extended conjugation → visible colors

---

## Decision Trees

### Predicting Addition Products
```
Conjugated diene + electrophile:
    ↓
Low temperature (-80°C) → 1,2-product (kinetic)
    ↓
High temperature (40°C) → 1,4-product (thermodynamic)
```

### Diels-Alder Reactivity
```
Diene requirements:
- Must be in s-cis conformation
- Cyclic dienes highly reactive

Dienophile requirements:
- Electron-withdrawing groups increase reactivity
- Cis-dienophiles give cis-substituents in product
```

---

## Key Tables

### Diels-Alder Reactive Dienophiles
| Dienophile | Electron-Withdrawing Group | Reactivity |
|------------|---------------------------|------------|
| Maleic anhydride | 2 × C=O | Very high |
| Benzoquinone | 2 × C=O | High |
| Acrolein | CHO | High |
| Methyl acrylate | COOCH₃ | High |
| Acrylonitrile | CN | High |
| Ethylene | None | Low |

### UV λmax Values
| Compound | λmax (nm) |
|----------|-----------|
| Ethylene | 171 |
| 1,3-Butadiene | 217 |
| 1,3,5-Hexatriene | 258 |
| β-Carotene | ~450 |

---

## Connected Topics

- **Upstream**: [alkene_chemistry.md](alkene_chemistry.md)
- **Downstream**: Aromatic compounds (Ch15)
- **Related**: [spectroscopy.md](spectroscopy.md) (UV spectroscopy)

---

## L3 Tools Required

1. `diels_alder_tools.py` - Diels-Alder predictions
2. `uv_spectroscopy_tools.py` - UV λmax calculations
3. `kinetic_thermodynamic_tools.py` - Product predictions

---

## L4 References (TODO)

- [ ] Complete Wood's rule tables
- [ ] Dienophile reactivity data
- [ ] Endo/exo energy differences

---

## L5 Worked Examples (TODO)

- [ ] Diels-Alder product prediction
- [ ] UV λmax calculation
- [ ] Kinetic vs thermodynamic product ratio
