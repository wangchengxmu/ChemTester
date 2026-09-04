---
id: chem.electron_configurations
layer: 2
title: Electron Configurations
source: LibreTexts Chemistry 2e Ch06.04
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Electron Configurations

## Problem type
Write electron configurations; determine valence electrons; identify element from configuration.

## Decision tree

1. **What is asked?**
   - Write configuration → Use aufbau order
   - Valence electrons → Count outer shell electrons
   - Identify element → Match to periodic table
   - Orbital diagram → Apply Hund's rule

2. **Main group or transition?**
   - Main group: s and p block
   - Transition: d block
   - Inner transition: f block

3. **Exceptions?**
   - Cr, Cu family: half-filled or filled d more stable

## Core rules

### Aufbau principle
Fill orbitals from lowest to highest energy:
```
1s → 2s → 2p → 3s → 3p → 4s → 3d → 4p → 5s → 4d → 5p → 6s → 4f → 5d → 6p → 7s
```

### Orbital capacity
| Orbital | Max electrons |
|---------|---------------|
| s | 2 |
| p | 6 |
| d | 10 |
| f | 14 |

### Hund's rule
- Maximize unpaired electrons in degenerate orbitals
- All unpaired electrons have same spin

### Pauli exclusion principle
- Max 2 electrons per orbital
- Must have opposite spins

## Noble gas notation

Use noble gas core to abbreviate:
- Na: [Ne] 3s¹
- Fe: [Ar] 4s² 3d⁶
- Br: [Ar] 4s² 3d¹⁰ 4p⁵

## Notable exceptions

| Element | Expected | Actual |
|---------|----------|--------|
| Cr | [Ar] 4s² 3d⁴ | [Ar] 4s¹ 3d⁵ |
| Cu | [Ar] 4s² 3d⁹ | [Ar] 4s¹ 3d¹⁰ |
| Mo | [Kr] 5s² 4d⁴ | [Kr] 5s¹ 4d⁵ |
| Ag | [Kr] 5s² 4d⁹ | [Kr] 5s¹ 4d¹⁰ |

## Valence electrons
- Main group: s + p electrons in outermost shell
- Group 1: 1 valence e⁻
- Group 2: 2 valence e⁻
- Groups 13-18: 3-8 valence e⁻

## Common patterns
1. Write full electron configuration
2. Write noble gas configuration
3. Count valence electrons
4. Identify element from configuration
5. Draw orbital diagram

## Links

### L3 Implementation
- `../L3_functions/electron_configuration_tools.py` (TODO)

### L4 Reference

### L5 Examples
- `../L5_examples/quantum-mechanics/ (TODO)

## Source trace
- `../sources/ingestion/source-electronic-structure-stepwise.md` section 6.04
## L3 Tool Call Directives

**Source:** `slater_rules_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
