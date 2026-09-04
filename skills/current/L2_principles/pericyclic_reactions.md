# L2 Topic: Pericyclic Reactions

**Source**: Organic Chemistry (OpenStax) Ch30
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Pericyclic reactions are concerted reactions that proceed through a cyclic transition state with no intermediates. They are governed by orbital symmetry conservation.

### Key Features
1. **Concerted**: All bonds form/break simultaneously
2. **Cyclic transition state**: No intermediates
3. **Orbital symmetry**: Must be conserved
4. **Predictable stereochemistry**: Governed by selection rules

---

## Core Principles

### 30.1: Frontier Orbitals
- HOMO and LUMO control reactivity
- In-phase overlap required for bond formation
- Symmetry conservation

### 30.2-30.4: Electrocyclic Reactions
- Cyclization of conjugated Ï systems
- Conrotatory vs disrotatory
- Thermal vs photochemical rules

### 30.5-30.6: Cycloadditions
- [n + m] notation
- Suprafacial vs antarafacial
- Diels-Alder [4+2] most common

### 30.7-30.8: Sigmatropic Rearrangements
- [i, j] notation
- Cope and Claisen rearrangements
- Hydrogen shifts

### 30.9: Selection Rules (TECA)
**Thermal + Even â?Conrotatory/Antarafacial**

---

## Decision Trees

### Electrocyclic Stereochemistry
```
Number of Ï electrons:
    â?4n (even)? â?Thermal: Conrotatory, Photochemical: Disrotatory
4n+2 (odd)? â?Thermal: Disrotatory, Photochemical: Conrotatory
```

### Cycloaddition Allowedness
```
Total Ï electrons:
    â?4n? â?Thermal: Antarafacial, Photochemical: Suprafacial
4n+2? â?Thermal: Suprafacial, Photochemical: Antarafacial
```

---

## Key Tables

### TECA Summary Table
| Conditions | Electron pairs | Stereochemistry |
|------------|----------------|-----------------|
| Thermal | Even (4n) | Antara-con |
| Thermal | Odd (4n+2) | Supra-dis |
| Photochemical | Even (4n) | Supra-dis |
| Photochemical | Odd (4n+2) | Antara-con |

### Common Pericyclic Reactions
| Reaction Type | Electrons | Thermal Allowed? |
|---------------|-----------|------------------|
| Electrocyclic (4Ï) | 4 | Conrotatory |
| Electrocyclic (6Ï) | 6 | Disrotatory |
| [4+2] Cycloaddition | 6 | Yes (suprafacial) |
| [2+2] Cycloaddition | 4 | No (antarafacial needed) |
| [3,3] Sigmatropic | 6 | Yes (suprafacial) |
| [1,5] H shift | 6 | Yes (suprafacial) |

---

## Connected Topics

- **Upstream**: [conjugated_compounds.md](conjugated_compounds.md) (Diels-Alder)
- **Upstream**: Molecular orbital theory
- **Related**: Reaction mechanisms

---

## L3 Tools Required

1. `pericyclic_tools.py` - Selection rules, stereochemistry predictions

---

## L4 References (TODO)

- [ ] Complete orbital symmetry diagrams
- [ ] Cope/Claisen examples
- [ ] Woodward-Hoffmann rules

---

## L5 Worked Examples (TODO)

- [ ] Electrocyclic ring closure
- [ ] Diels-Alder stereochemistry
- [ ] Cope rearrangement


## Implementations

- Implementation: `../L3_functions/diels_alder_tools.py`

## L3 Tool Call Directives

**Source:** pericyclic_tools.py
L3 Tool: Pericyclic Reaction Tools

### Available functions:
- electrocyclic_stereochemistry(n_electrons, thermal) → dict — Predict electrocyclic ring closure stereochemistry.
- cycloaddition_allowed(n_electrons, thermal) → dict — Determine if cycloaddition is symmetry-allowed.
- sigmatropic_allowed(i, j, thermal) → dict — Determine if [i,j]-sigmatropic is allowed.
- teca_predict(n_electron_pairs, thermal) → dict — TECA mnemonic for pericyclic predictions.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
