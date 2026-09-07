---
id: chem.formal_charges_resonance
layer: 2
title: Formal Charges and Resonance
source: Ch07.04
dependencies: [lewis_structures]
stability: high
confidence: high
---

## Concept

Formal charge helps evaluate Lewis structures. Resonance describes molecules with multiple valid Lewis structures.

## Core Formulas

### Formal Charge
```
FC = valence electrons - lone pair electrons - ?(bonding electrons)
```

### Formal Charge Guidelines
```
1. FC = 0 on all atoms is best
2. Smaller |FC| is better
3. Adjacent opposite-sign FC is preferred
4. Negative FC on more electronegative atom
```

### Resonance
```
- Multiple valid Lewis structures with same atom arrangement
- Actual structure = average (resonance hybrid)
- Bond properties are averaged
```

## Decision Tree (Best Lewis Structure)

```
For each candidate structure:
1. Calculate FC on each atom
2. Sum of FC = total charge?
   ©À©¤ No ¡ú Invalid structure
   ©¸©¤ Yes ¡ú Compare to other candidates
       ©À©¤ Lower |FC| wins
       ©À©¤ Fewer atoms with FC ¡Ù 0 wins
       ©¸©¤ Negative on more EN wins
```

## Key Constraints
- Sum of formal charges must equal total charge
- Formal charge ¡Ù actual charge (bookkeeping only)
- Resonance forms must have identical atom positions
- Bond order in resonance hybrid = average

## Problem Archetypes
1. Calculate formal charges for a structure
2. Choose best Lewis structure from candidates
3. Draw resonance structures
4. Predict bond order in resonance hybrid

## L3 Tools
- `formal_charge(valence_e, lone_pairs, bonding_e)` ¡ú FC
- `best_lewis_structure(candidates)` ¡ú best_structure
- `resonance_forms(molecule)` ¡ú list of structures
- `average_bond_order(resonance_forms, bond)` ¡ú bond_order

## L4 Reference

## L5 Examples
See `../L5_examples/intermolecular_forces/ for worked examples.

## Implementations

- Implementation: `../L3_functions/formal_charge_tools.py`

## L3 Tool Call Directives

**Source:** `formal_charge_tools.py`

Formal Charges and Resonance Tools - L3 Implementation

### Available functions:
- `formal_charge(valence_electrons: int, lone_pairs: int, bonding_electrons: int)` → int — Calculate formal charge on an atom.
- `formal_charge_from_structure(element: str, lone_pairs: int, bonds: int)` → int — Calculate formal charge from structural information.
- `best_lewis_structure(candidates: List[Dict])` → Dict — Select the best Lewis structure from candidates.
- `resonance_equivalent(structure1: Dict, structure2: Dict)` → bool — Check if two structures are resonance forms.
- `average_bond_order(resonance_forms: List[Dict], atom1_idx: int, atom2_idx: int)` → float — Calculate average bond order from resonance forms.
- `sum_formal_charges(formal_charges: List[int])` → int — Calculate total charge from formal charges.
- `validate_formal_charges(formal_charges: List[int], expected_charge: int)` → bool — Validate that formal charges sum to expected molecular charge.
- `fc_minimization_preferred(fc1: List[int], fc2: List[int])` → bool — Determine if first FC distribution is preferred over second.
- `score(structure)` → 

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
