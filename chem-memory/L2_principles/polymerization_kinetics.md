---
id: chem.polymerization_kinetics
layer: 2
title: Polymerization Kinetics
source: Polymer Chemistry (Schaller), Ch3
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/polymer_chemistry_tools.py
  - ../L3_functions/polymer_chemistry.py
  - ../L3_functions/polymer_tools.py
---

# Polymerization Kinetics

[Source: Polymer Chemistry (Schaller), Ch3]

## Core Concept

Polymerization kinetics describes the rate and extent of polymer formation. Different mechanisms (step-growth vs chain-growth) have fundamentally different kinetic behaviors.

## Key Equations

### Carothers Equation (Step-Growth)

$$\bar{X}_n = \frac{1}{1-p}$$

where:
- $\bar{X}_n$ = number-average degree of polymerization
- $p$ = fractional conversion of functional groups

**Stoichiometric Imbalance**:
$$\bar{X}_n = \frac{1+r}{1+r-2rp}$$

where $r$ = ratio of functional groups

### Flory Distribution (Step-Growth)

$$w_x = x(1-p)^2 p^{x-1}$$

where $w_x$ = weight fraction of chains with $x$ units

### Number-Average Molecular Weight

$$\bar{M}_n = \sum x_i M_i = M_0 \bar{X}_n$$

### Weight-Average Molecular Weight

$$\bar{M}_w = \sum w_i M_i$$

### Polydispersity Index

$$PDI = \frac{\bar{M}_w}{\bar{M}_n}$$

- For step-growth: PDI → 2 as p → 1
- For chain-growth: PDI varies (1.5-2 for living, 2+ for radical)

## Problem Types

1. **Calculate DP** from conversion using Carothers equation
2. **Find required conversion** for target molecular weight
3. **Calculate PDI** from Mn and Mw
4. **Predict molecular weight distribution**

## L3 Tools

- `../L3_functions/polymer_chemistry.py` - Carothers equation, conversion calculations

## Related Topics

- → `step_growth_polymerization.md` for mechanism details
- → `chain_growth_polymerization.md` for radical/ionic methods

## L3 Tool Call Directives

**Source:** polymer_chemistry.py
Polymer Chemistry - L3 Implementation

### Available functions:
- carothers_dp(conversion) → float — Calculate degree of polymerization from conversion (Carothers equation).
- carothers_conversion(target_dp) → float — Calculate required conversion for target degree of polymerization.
- stoichiometric_imbalance_dp(conversion, r_ratio) → float — Calculate DP with stoichiometric imbalance.
- number_average_mw(dp, monomer_mw) → float — Calculate number-average molecular weight.
- polydispersity_index(mw, mn) → float — Calculate polydispersity index.
- flory_weight_fraction(x, conversion) → float — Calculate weight fraction for chains with x units (Flory distribution).
- fox_equation_tg(w_a, tg_a, tg_b) → float — Calculate copolymer Tg using Fox equation.
- crystallinity_from_density(sample_density, amorphous_density, crystalline_density) → float — Calculate percent crystallinity from density measurements.
- viscosity_mw_relation(molecular_weight, critical_mw, k_value) → float — Calculate relative viscosity from molecular weight.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
