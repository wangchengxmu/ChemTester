---
id: ref.limiting_reactant
layer: 4
title: Limiting Reactant and Yield Reference
source: LibreTexts Chemistry 2e Ch04.04
status: scaffold
created: 2026-03-10
---

# Limiting Reactant and Yield Reference

## Key equations

### Limiting reactant identification
**Method 1: Ratio comparison**
- `provided_ratio = mol_A_given / mol_B_given`
- `stoichiometric_ratio = coeff_A / coeff_B`
- If provided_ratio < stoichiometric_ratio → A limiting

**Method 2: Product comparison**
- `mol_product_from_A = mol_A × (coeff_product / coeff_A)`
- `mol_product_from_B = mol_B × (coeff_product / coeff_B)`
- Limiting = smaller product amount

### Yield calculations
- `theoretical_yield = mol_limiting × (coeff_product/coeff_limiting) × M_product`
- `percent_yield = (actual_yield / theoretical_yield) × 100%`
- `atom_economy = (M_product / Σ M_reactants) × 100%`

### Excess remaining
- `consumed = mol_limiting × (coeff_excess / coeff_limiting)`
- `excess_remaining = initial - consumed`

## Decision table
| Situation | Method |
|-----------|--------|
| Given masses of 2+ reactants | Find limiting first |
| Given moles directly | Ratio comparison |
| Need product amount | Product comparison |
| Given actual yield | Calculate percent yield |
| Need excess remaining | Subtract consumed |

## Source trace
- `../sources/ingestion/source-stoichiometry-chemical-reactions-stepwise.md` section 4.04
