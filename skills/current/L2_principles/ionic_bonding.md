---
id: chem.ionic_bonding
layer: 2
title: Ionic Bonding and Ion Formation
source: Ch07.01
dependencies: [electron_configurations, periodic_trends]
stability: high
confidence: high
---

## Concept

Ionic bonding results from electrostatic attraction between oppositely charged ions (cations and anions).

## Core Formulas

### Ion Charge Prediction
```
Group 1, 2: cation charge = group number
Groups 13-17: cation charge = group number - 10
Anion charge = electrons needed to fill valence shell
```

### Ionic Compound Formula
```
Formula = simplest ratio giving charge neutrality
Example: Al?O? ¡ú (2 ¡Á +3) + (3 ¡Á -2) = 0
```

### Lattice Energy
```
¦¤H_lattice = energy to separate 1 mole of ionic solid into gaseous ions
NaCl(s) ¡ú Na?(g) + Cl?(g)    ¦¤H = 769 kJ/mol
```

## Decision Tree

```
Is it a metal + nonmetal?
©À©¤ Yes ¡ú Ionic bonding likely
©¦   ©À©¤ Predict cation charge from group
©¦   ©À©¤ Predict anion charge (fill valence)
©¦   ©¸©¤ Balance charges for formula
©¸©¤ No ¡ú Consider covalent bonding
```

## Key Constraints
- Total positive charge = total negative charge
- Lattice energy increases with ion charge and decreases with ion size
- Cations lose electrons (smaller than parent atom)
- Anions gain electrons (larger than parent atom)

## Problem Archetypes
1. Predict ion charge from element/group
2. Write formula from ion names
3. Compare lattice energies
4. Write electron configurations of ions

## L3 Tools
- `predict_ion_charge(element, group, period)` ¡ú charge
- `ionic_formula(cation, anion)` ¡ú formula
- `ion_electron_config(element, charge)` ¡ú config string

## L4 Reference

## L5 Examples
See `../L5_examples/crystal_structures/ for worked examples.

## Implementations
- Implementation: `../L3_functions/born_haber_tools.py`

- Implementation: `../L3_functions/ionic_bonding_tools.py`

## L3 Tool Call Directives


**Source:** `born_haber_tools.py`

L3 tool module for born haber tools

### Available functions:
- `calculate_born_haber_cycle(compound: str, ionization_energies: list[float], electron_affinities: list[float], sublimation_energy: Optional[float], bond_dissociation_energy: Optional[float], atomization_energy: Optional[float], lattice_energy: Optional[float], formation_enthalpy: Optional[float])` → dict — Calculate a full Born-Haber cycle for an ionic compound.
- `calculate_lattice_energy(compound: str, ionization_energies: list[float], electron_affinities: list[float], sublimation_energy: Optional[float], bond_dissociation_energy: Optional[float], formation_enthalpy: Optional[float])` → float — Derive lattice energy from the Born-Haber cycle.
- `calculate_formation_enthalpy(compound: str, ionization_energies: list[float], electron_affinities: list[float], lattice_energy: float, sublimation_energy: Optional[float], bond_dissociation_energy: Optional[float])` → float — Derive formation enthalpy from the Born-Haber cycle.
- `test_nacl_lattice_energy()` → any — N/A
- `test_mgo_formation_enthalpy()` → any — N/A
- `test_known_compound_data()` → any — N/A
- `test_calculate_lattice_energy()` → any — N/A
- `test_calculate_formation_enthalpy()` → any — N/A

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters

**Source:** `ionic_bonding_tools.py`

Ion charge prediction, ionic formula generation, and lattice energy comparisons.

### Available functions:
- `predict_ion_charge(element, group=None)` → int|list — Returns ion charge(s); transition metals return list
- `ionic_formula(cation, cation_charge, anion, anion_charge)` → str — Generates formula with parentheses for polyatomics
- `ion_electron_config(element, charge)` → str — Returns noble gas shorthand config for ion
- `compare_lattice_energy(compound1, compound2)` → str — Compares (cat_charge, an_charge, distance) tuples
- `is_ionic_compound(element1, element2)` → bool — Predicts if metal + nonmetal

### Common errors:
- ❌ Forgetting polyatomic ions need parentheses when multiplied (Ca(NO₃)₂ not CaNO₃₂)
- ❌ Using negative charges for cations (pass positive values for cations)
- ❌ Confusing lattice energy trend: U ∝ (Z+×Z-)/r (higher charges + smaller distance = higher U)
