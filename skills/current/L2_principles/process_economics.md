---
id: chem.process_economics
layer: 2
title: Process Economics
source: Foundations of Chemical and Biological Engineering I (Verret), Ch6
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/process_economics_tools.py
  - ../L3_functions/process_economics.py
---

# Process Economics

[Source: Foundations of Chemical and Biological Engineering I (Verret), Ch6]

## Core Concept

Process economics evaluates the financial viability of chemical processes. Engineers must consider capital costs, operating costs, and revenue to determine profitability.

## Key Equations

### Net Present Value (NPV)

$$NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}$$

where:
- $CF_t$ = Cash flow at time $t$
- $r$ = Discount rate
- $n$ = Project lifetime

### Return on Investment (ROI)

$$ROI = \frac{\text{Annual Profit}}{\text{Total Investment}} \times 100\%$$

### Payback Period

$$\text{Payback} = \frac{\text{Capital Investment}}{\text{Annual Cash Flow}}$$

### Capital Cost Estimation

$$C_{new} = C_{ref} \left(\frac{S_{new}}{S_{ref}}\right)^n$$

where $n$ ï¿½?0.6 for most equipment (six-tenths rule)

## Cost Categories

| Category | Examples | Typical % of Total |
|----------|----------|-------------------|
| Capital (CAPEX) | Equipment, installation | 30-50% |
| Operating (OPEX) | Raw materials, labor, utilities | 50-70% |
| Fixed | Insurance, taxes, depreciation | 10-20% |

## Problem Types

1. **Calculate NPV** from cash flows
2. **Estimate capital cost** using scaling factors
3. **Compare alternatives** using economic criteria
4. **Determine break-even** production rate

## Related Topics

- ï¿½?`process_safety.md` for safety costs
- ï¿½?`green_engineering.md` for sustainability metrics


## Implementations

- Implementation: `../L3_functions/process_economics.py`

## L3 Tool Call Directives

**Source:** process_economics.py
Process Economics - L3 Implementation

### Available functions:
- net_present_value(cash_flows, discount_rate) â†’ float â€” Calculate Net Present Value.
- return_on_investment(annual_profit, total_investment) â†’ float â€” Calculate Return on Investment.
- payback_period(capital_investment, annual_cash_flow) â†’ float â€” Calculate simple payback period.
- scale_cost(reference_cost, reference_size, new_size, exponent) â†’ float â€” Scale equipment cost using six-tenths rule.
- annualized_cost(capital_cost, lifetime_years, discount_rate) â†’ float â€” Calculate annualized capital cost.
- break_even_analysis(fixed_cost, variable_cost, selling_price) â†’ float â€” Calculate break-even production quantity.
- compare_alternatives(npv_list) â†’ dict â€” Compare multiple investment alternatives.
- npv(cash_flows, discount_rate) â†’ float â€” Alias for net_present_value.
- roi(annual_profit, total_investment) â†’ float â€” Alias for return_on_investment.
- payback(capital_investment, annual_cash_flow) â†’ float â€” Alias for payback_period.
- break_even(fixed_cost, variable_cost, selling_price) â†’ float â€” Alias for break_even_analysis.

### Common errors:
- âŒ Passing wrong parameter types or missing required arguments

---

**Source:** process_economics_tools.py
Core chemical engineering calculations: conversion, yield, selectivity, material balance, green chemistry metrics.

### Available functions:
- conversion(reactant_in: float, reactant_out: float) ¡ú float ¡ª Fractional conversion (0-1)
- yield_calc(product_moles: float, limiting_reactant_moles: float) ¡ú float ¡ª Reaction yield fraction
- selectivity(product_moles: float, byproduct_moles: float) ¡ú float ¡ª Product selectivity fraction
- material_balance(inputs: List[float], outputs: List[float]) ¡ú Dict ¡ª Closure check (total_in, total_out, difference, closure_pct)
- tom_economy(mw_products: float, mw_reactants: float) ¡ú float ¡ª Atom economy percentage
- e_factor(mass_waste: float, mass_product: float) ¡ú float ¡ª E-factor (waste/product)
- pmi(mass_total_input: float, mass_product: float) ¡ú float ¡ª Process Mass Intensity
- space_time_yield(mass_product: float, reactor_volume: float, time_hours: float) ¡ú float ¡ª STY in kg/(L¡¤h)
- 	urnover_frequency(moles_product: float, moles_catalyst: float, time_hours: float) ¡ú float ¡ª TOF in h?1
- 	urnover_number(moles_product: float, moles_catalyst: float) ¡ú float ¡ª TON (dimensionless)

### Common errors:
- ? Conversion > 1.0 means input error in moles; conversion ¡Ü 1 (fractional)
- ? Yield cannot exceed conversion; check limiting reagent identification
- ? atom_economy uses MW of desired product(s) only, not all products
