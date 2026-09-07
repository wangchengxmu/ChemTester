---
id: chem.equation_balancing
layer: 2
title: Equation Writing and Balancing
source: LibreTexts Chemistry 2e Ch04.01
status: active
created: 2026-03-10
last_verified: 2026-03-10
---

# Equation Writing and Balancing

## Problem type
Balance a chemical equation or write balanced equation from narrative description.

## Decision tree

1. **Input format?**
   - Narrative → Write formulas first, then balance
   - Unbalanced equation → Balance directly

2. **Equation type?**
   - Molecular → Balance coefficients only
   - Ionic → Balance, then convert to complete/net ionic

3. **Balancing method?**
   - Inspection (simple equations)
   - Algebraic (complex equations)
   - Fractional coefficients → multiply by LCM

## Core rules

### Balancing by inspection
1. Write correct formulas (never change subscripts)
2. Count atoms of each element on both sides
3. Adjust coefficients to balance (one element at a time)
4. Check polyatomic ions as units if unchanged
5. Reduce to smallest whole-number coefficients

### Ionic equation conversion
1. Write balanced molecular equation
2. Dissociate all soluble ionic compounds → complete ionic
3. Remove spectator ions → net ionic

## Constraints
- Conservation of atoms: each element balanced
- Conservation of charge: total charge balanced
- Smallest whole-number coefficients (convention)
- Subscripts define identity (never change during balancing)

## Common patterns
- Combustion: CxHy + O2 → CO2 + H2O (balance C, then H, then O)
- Odd/even problem: use fractional coefficient, then multiply

## Links

### L3 Implementation
- `../L3_functions/equation_balancing_tools.py` (TODO)
- `../L3_functions/equation_balancing_tools.py` (TODO)

### L4 Reference

### L5 Examples
- `../L5_examples/stoichiometry/equation-balancing/ (TODO)

## Source trace
- `../sources/ingestion/source-stoichiometry-chemical-reactions-stepwise.md` section 4.01
---

## L3 Tool Call Directives

**Source:** equation_balancing_tools.py
Chemical equation parsing, balancing, molar mass, and ionic equation conversion.

### Available functions:
- parse_formula(formula) → dict — Element counts: "Al2(SO4)3" → {Al:2, S:3, O:12}
- count_atoms(formula, coefficient) → dict — Atom counts with stoichiometric coefficient
- check_balance(reactants, products) → tuple[bool, dict] — Verify balance with element counts
- alance_by_inspection(reactant_formulas, product_formulas, max_coeff) → dict — Balance equation via coefficient search
- molecular_to_ionic(molecular_eq, solubility_rules) → dict — Convert molecular to complete ionic equation
- complete_to_net_ionic(complete_ionic_eq) → dict — Remove spectator ions
- ormat_equation(balanced_eq) → str — Format as readable string: "2 H2 + O2 → 2 H2O"

### Common errors:
- ❌ Forgetting coefficients must be integers (smallest whole numbers)
- ❌ Assuming all aqueous salts are soluble — check solubility rules for solid precipitates
