---
id: chem.limiting_reactant_yield
layer: 2
title: Limiting Reactant and Theoretical Yield
source: LibreTexts Chemistry 2e Ch04.04
status: active
created: 2026-03-10
last_verified: 2026-03-10
---

# Limiting Reactant and Theoretical Yield

## Problem type
Identify limiting reactant, calculate theoretical yield, or determine percent yield.

## Decision tree

1. **What is asked?**
   - Identify limiting reactant → Compare ratios
   - Calculate theoretical yield → Use limiting reactant
   - Calculate percent yield → Use actual/theoretical
   - Find excess remaining → Subtract consumed amount

2. **Limiting reactant method?**
   - Ratio comparison: compare provided ratio to stoichiometric ratio
   - Product comparison: calculate product from each reactant, take lesser

3. **Yield calculation?**
   - Percent yield = (actual / theoretical) × 100%
   - Atom economy = (mass product / mass reactants) × 100%

## Core formulas

### Ratio comparison method
```
provided_ratio = mol_A_given / mol_B_given
stoichiometric_ratio = coeff_A / coeff_B

If provided_ratio < stoichiometric_ratio → A is limiting
If provided_ratio > stoichiometric_ratio → B is limiting
```

### Product comparison method
```
mol_product_from_A = mol_A × (coeff_product / coeff_A)
mol_product_from_B = mol_B × (coeff_product / coeff_B)

Limiting = reactant giving lesser product amount
```

### Theoretical yield
```
theoretical = mol_limiting × (coeff_product/coeff_limiting) × M_product
```

### Percent yield
```
percent_yield = (actual / theoretical) × 100%
```

### Excess remaining
```
excess_remaining = initial - consumed
consumed = mol_limiting × (coeff_excess/coeff_limiting)
```

## Constraints
- Actual yield ≤ theoretical yield (percent ≤ 100%)
- Compare ratios, not absolute amounts
- Must use balanced equation

## Common patterns
- Given masses of two reactants → find limiting, then theoretical yield
- Given actual yield → calculate percent yield
- Given percent yield → back-calculate actual or theoretical

## Links

### L3 Implementation
- `../L3_functions/limiting_reactant_tools.py` ✅
- `../L3_functions/limiting_reactant_tools.py` (optional)

### L4 Reference
- `../L4_reference/limiting-reactant-reference.md` ✅

### L5 Examples
- `../L5_examples/stoichiometry/limiting-reactant/ (needs examples)

## L3 Tool Call Directive

When solving limiting reactant, percent yield, or excess reactant problems, call the appropriate L3 function:

**identify_limiting_by_ratio** (`L3_functions/limiting_reactant_tools.py`):
- Use when: Given moles of two reactants and their stoichiometric coefficients, determine which limits.
- Parameters: `mol_A`, `mol_B`, `coeff_A`, `coeff_B`
- Example: `identify_limiting_by_ratio(mol_A=0.5, mol_B=0.8, coeff_A=2, coeff_B=1)`

**theoretical_yield_moles** (`L3_functions/limiting_reactant_tools.py`):
- Use when: Calculate moles of product from limiting reactant.
- Parameters: `mol_limiting`, `coeff_limiting`, `coeff_product`

**theoretical_yield_mass** (`L3_functions/limiting_reactant_tools.py`):
- Use when: Calculate mass of product from limiting reactant.
- Parameters: `mol_limiting`, `coeff_limiting`, `coeff_product`, `molar_mass_product`

**percent_yield** (`L3_functions/limiting_reactant_tools.py`):
- Use when: Given actual and theoretical yield, calculate percent yield.
- Parameters: `actual_yield`, `theoretical_yield`

**excess_remaining_moles** (`L3_functions/limiting_reactant_tools.py`):
- Use when: Calculate moles of excess reactant remaining after reaction.
- Parameters: `mol_excess_initial`, `mol_limiting`, `coeff_excess`, `coeff_limiting`

**mass_to_mass** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Full stoichiometric mass-to-mass conversion including mole ratio.
- Parameters: `mass_A`, `molar_mass_A`, `molar_mass_B`, `coeff_A`, `coeff_B`

**limiting_reactant** (`L3_functions/stoichiometric_conversion_tools.py`):
- Use when: Determine limiting reactant from a dict of reactant moles and full stoichiometry.
- Parameters: `reactants_dict` (e.g. `{"A": 0.5, "B": 0.8}`), `stoichiometry` (e.g. `{"A": 2, "B": 1, "product": 1}`)

**Critical notes:**
- Always convert masses to moles first using `mass_to_moles(mass, molar_mass)` or `moles_from_mass(mass_g, molar_mass)` from stoichiometric_conversion_tools.
- For solution-phase reactions, use `solution_moles(molarity, volume_L)` to get moles.
- For gas-phase reactions at STP, use `moles_at_stp(V)` from ideal_gas_law_tools.

## Source trace
- `../sources/ingestion/source-stoichiometry-chemical-reactions-stepwise.md` section 4.04
