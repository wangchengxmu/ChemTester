---
id: chem.covalent_bonding
layer: 2
title: Covalent Bonding and Electronegativity
source: Ch07.02
dependencies: [periodic_trends]
stability: high
confidence: high
---

## Concept

Covalent bonds form when atoms share electrons. Bond polarity depends on electronegativity difference.

## Core Formulas

### Bond Formation Energy
```
H?(g) ¡ú 2H(g)    ¦¤H = +436 kJ/mol (breaking)
2H(g) ¡ú H?(g)    ¦¤H = -436 kJ/mol (forming)
```

### Electronegativity Difference vs Bond Type
```
| ¦¤EN | Bond Type |
|-----|-----------|
| 0   | Pure covalent (nonpolar) |
| 0.1-0.4 | Mostly covalent |
| 0.5-1.9 | Polar covalent |
| ¡Ý 2.0 | Ionic |
```

### Bond Dipole Direction
```
¦Ä+ -----> ¦Ä-
(Less EN)   (More EN)
```

## Decision Tree

```
Two nonmetals bonding?
©À©¤ Yes ¡ú Covalent bond
©¦   ©À©¤ Calculate ¦¤EN
©¦   ©À©¤ ¦¤EN ¡Ö 0 ¡ú Pure covalent
©¦   ©À©¤ 0 < ¦¤EN < 2 ¡ú Polar covalent
©¦   ©¦   ©¸©¤ ¦Ä+ on less EN atom, ¦Ä- on more EN
©¦   ©¸©¤ ¦¤EN ¡Ý 2 ¡ú Consider ionic
©¸©¤ No ¡ú Likely ionic (metal + nonmetal)
```

## Key Constraints
- Bond breaking = endothermic (requires energy)
- Bond forming = exothermic (releases energy)
- Electronegativity increases left¡úright, decreases down group
- F is most electronegative (EN = 4.0)

## Problem Archetypes
1. Classify bond type from ¦¤EN
2. Identify ¦Ä+ and ¦Ä- atoms
3. Rank bonds by polarity
4. Compare bond energies

## L3 Tools
- `classify_bond_type(EN1, EN2)` ¡ú bond_type
- `bond_polarity(EN1, EN2)` ¡ú (delta_EN, direction)
- `bond_dipole_direction(atom1, atom2, EN1, EN2)` ¡ú (delta_plus, delta_minus)

## L4 Reference

## L5 Examples
See `../L5_examples/intermolecular_forces/ for worked examples.

## Implementations

- Implementation: `../L3_functions/covalent_bonding_tools.py`

## L3 Tool Call Directives

**Source:** `covalent_bonding_tools.py`

Covalent Bonding Tools - L3 Implementation

### Available functions:
- `get_electronegativity(element: str)` → float — Get electronegativity value for an element.
- `classify_bond_type(element1: str, element2: str)` → dict — Classify bond type based on electronegativity difference.
- `bond_polarity(element1: str, element2: str)` → tuple — Get bond polarity information.
- `get_bond_energy(element1: str, element2: str, bond_order: int)` → float — Get average bond energy for a bond.
- `compare_bond_polarity(bonds: list)` → list — Rank bonds by polarity.
- `percent_ionic_character(element1: str, element2: str)` → float — Calculate approximate percent ionic character.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
