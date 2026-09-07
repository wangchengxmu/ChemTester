---
id: chem.electrolytes
layer: 2
title: Electrolytes and Dissociation
source: Ch11.02
dependencies: [ionic_bonding, covalent_bonding]
stability: high
confidence: high
---

## Concept

Electrolytes are substances that produce ions when dissolved, enabling electrical conductivity. Classification depends on degree of dissociation.

## Core Formulas

#### Dissociation Equations
```
NaCl(s) ¡ú Na?(aq) + Cl?(aq)     (complete, strong)
HC2H3O2(aq) ? H?(aq) + C2H3O2?(aq)  (partial, weak)
C6H12O6(s) ¡ú C6H12O6(aq)        (no ions, nonelectrolyte)
```

### Ion Count
```
i = number of ions per formula unit
NaCl: i = 2
CaCl2: i = 3
Na2SO4: i = 3
```

## Decision Tree

```
Is substance an electrolyte?
©À©¤ Ionic compound?
©¦   ©À©¤ Soluble ¡ú Strong electrolyte
©¦   ©¸©¤ Insoluble ¡ú Weak/none (limited dissolution)
©À©¤ Molecular acid?
©¦   ©À©¤ Strong acid (HCl, HNO3, H2SO4) ¡ú Strong electrolyte
©¦   ©¸©¤ Weak acid ¡ú Weak electrolyte
©À©¤ Molecular base?
©¦   ©À©¤ Strong base (NaOH, KOH) ¡ú Strong electrolyte
©¦   ©¸©¤ Weak base ¡ú Weak electrolyte
©¸©¤ Other molecular compound?
    ©¸©¤ Nonelectrolyte (sugar, alcohol)
```

## Classification Table

| Type | % Dissociation | Conductivity | Examples |
|------|----------------|--------------|----------|
| Strong electrolyte | ~100% | High | NaCl, HCl, NaOH |
| Weak electrolyte | <100% | Low | HC2H3O2, NH3 |
| Nonelectrolyte | 0% | None | C6H12O6, C2H5OH |

## Key Constraints
- Solubility ¡Ù electrolyte strength
- Weak electrolytes exist in equilibrium with undissociated molecules
- Conductivity depends on ion concentration

## Problem Archetypes
1. Classify substance as electrolyte type
2. Write dissociation equations
3. Predict conductivity of solution
4. Calculate ion concentration from formula

## L3 Tools
- `classify_electrolyte(compound)` ¡ú classification
- `dissociation_equation(formula)` ¡ú equation string
- `ion_count(formula)` ¡ú number of ions
- `predict_conductivity(compound, concentration)` ¡ú level

## L4 Reference

## L5 Examples
See `../L5_examples/electrochemical_analysis/ for worked examples.

## Implementations

- Implementation: `../L3_functions/electrolyte_tools.py`

## L3 Tool Call Directives

**Source:** `electrolyte_tools.py`

Electrolyte Tools - L3 Implementation

### Available functions:
- `classify_electrolyte(formula: str)` → str — Classify substance as strong electrolyte, weak electrolyte, or nonelectrolyte.
- `dissociation_equation(formula: str)` → str — Generate dissociation equation for an electrolyte.
- `ion_count(formula: str)` → int — Count the number of ions produced per formula unit.
- `parse_ionic_formula(formula: str)` → Optional[Tuple[str, str]] — Parse ionic formula into cation and anion.
- `get_ion_charges(cation: str, anion: str)` → Optional[Tuple[int, int]] — Get typical charges for ions.
- `is_soluble(cation: str, anion: str)` → bool — Check if an ionic compound is soluble.
- `format_ion(ion: str, charge: int)` → str — Format ion with superscript charge.
- `ion_pairing_tendency(cations: list, solvent: str)` → list — Rank ions by ion-pairing tendency with a given anion.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
