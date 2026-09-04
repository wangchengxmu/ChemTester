---
id: chem.lewis_structures
layer: 2
title: Lewis Symbols and Structures
source: Ch07.03
dependencies: [electron_configurations]
stability: high
confidence: high
---

## Concept

Lewis structures show valence electrons as dots (lone pairs) or lines (bonds). Used to predict bonding and molecular structure.

## Core Formulas

### Valence Electron Count
```
Total valence e? = ¦²(valence e? per atom)
                - charge (if cation)
                + |charge| (if anion)
```

### Octet Rule
```
Most atoms want 8 valence electrons (H wants 2)
```

### Bond Types
```
Single bond:  1 pair shared (2 e?)
Double bond:  2 pairs shared (4 e?)
Triple bond:  3 pairs shared (6 e?)
```

## Decision Tree (Lewis Structure)

```
1. Count total valence electrons
2. Draw skeleton (least EN in center, H never central)
3. Connect atoms with single bonds
4. Complete octets on terminal atoms (except H)
5. Place remaining electrons on central atom
6. Need octet on central atom?
   ©À©¤ Yes, and have remaining e? ¡ú Add lone pairs
   ©¸©¤ No, but need more e? ¡ú Form multiple bonds
```

## Octet Rule Exceptions

1. **Odd-electron molecules**: Free radicals (NO, NO?)
2. **Electron-deficient**: Be (4 e?), B (6 e?) in compounds
3. **Hypervalent**: n¡Ý3 elements can exceed octet (PCl?, SF?)

## Key Constraints
- H always has 2 electrons (duet)
- Halogens usually have 3 lone pairs + 1 bond
- Oxygen usually has 2 lone pairs + 2 bonds
- Nitrogen usually has 1 lone pair + 3 bonds
- Carbon usually has 4 bonds, no lone pairs

## Problem Archetypes
1. Draw Lewis structure for molecule/ion
2. Count bonding and lone pairs
3. Identify octet exceptions
4. Determine if multiple bonds needed

## L3 Tools
- `count_valence_electrons(atoms, charge)` ¡ú total
- `lewis_structure(molecule)` ¡ú structure dict
- `is_octet_exception(molecule)` ¡ú bool, exception_type

## L4 Reference

## L5 Examples
See `../L5_examples/intermolecular_forces/ for worked examples.

## Implementations

- Implementation: `../L3_functions/lewis_structures_tools.py`

## L3 Tool Call Directives

**Source:** `lewis_structures_tools.py`

Lewis structure construction: valence electron counting, octet rule checking, and bonding predictions.

### Available functions:
- `count_valence_electrons(atoms, charge=0)` → int — Total valence electrons; atoms is list of element symbols
- `typical_bonds(element)` → int — Returns typical bond count (C=4, N=3, O=2, H/F/Cl/Br/I=1)
- `octet_rule_violation(atoms, bonds, lone_pairs)` → list — Returns [(index, element, electrons, 'type')] for violations
- `is_octet_exception(element)` → Tuple[bool, str] — Returns (True, 'electron-deficient'|'hypervalent') or (False, None)
- `lewis_structure_summary(formula)` → dict — Parses formula, returns atoms, valence_electrons, central_atom
- `bonds_needed_for_octet(element, current_electrons=0)` → int — Electrons needed to complete octet
- `duet_rule(atom, electrons)` → bool — True if H has exactly 2 electrons

### Common errors:
- ❌ Forgetting to adjust for charge (subtract for cations, add for anions)
- ❌ Not recognizing B/Be as electron-deficient (stable with <8 electrons)
- ❌ Forgetting H never satisfies octet (follows duet rule with 2 electrons)
