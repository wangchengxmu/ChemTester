---
id: chemistry.fugacity_activity
layer: 2
title: Fugacity and Activity for Non-Ideal Systems
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch7, Ch9
last_verified: 2026-03-15
---

## Core Concept

Fugacity and activity correct thermodynamic expressions for non-ideal behavior.

### Fugacity (Gases)

- **Definition**: f = φp where φ is the fugacity coefficient
- **Chemical potential**: μ = μ° + RT ln(f/f°)
- **Ideal limit**: φ → 1 as p → 0

### Activity (Solutions)

- **Definition**: a = γx where γ is the activity coefficient
- **Chemical potential**: μ = μ° + RT ln(a)
- **Ideal limit**: γ → 1 (ideal solution)

## Key Formulas

```
# Fugacity from equation of state
ln(f/p) = ∫₀^p (Z-1)/p dp  where Z = pV_m/(RT) is compressibility factor

# Activity coefficient from Gibbs excess energy
RT ln γ_i = (∂G^E/∂n_i)_T,p,n_j

# Chemical potential in mixture
μ_i = μ_i° + RT ln(a_i) = μ_i° + RT ln(γ_i x_i)

# Standard states
# - Gases: 1 bar ideal gas
# - Solids/liquids: pure substance at 1 bar
# - Solutes: 1 molal ideal solution (Henry's law)
```

## Activity Coefficient Models

- **Raoult's law**: a_i = x_i (ideal)
- **Henry's law**: a_i = m_i/m° (dilute solutes)
- **Debye-Hückel**: ln(γ±) = -A|z₊z₋|√I (electrolytes)

## Problem-Solving Routes

1. **Calculate fugacity** → Integrate from EoS or use correlation
2. **Find activity** → From vapor pressure measurement or γ model
3. **Correct equilibrium constant** → Use activities instead of concentrations
4. **Determine γ from data** → Fit to model or measure directly

## Links to L3 Tools

- `../L3_functions/fugacity_calculations.py` - Fugacity from EoS
- `../L3_functions/activity_coefficients.py` - γ models

## Links to L4 Data

- `../L4_reference/fugacity_data.md` - Fugacity coefficients for gases
- `../L4_reference/activity_coefficient_data.md` - Activity coefficient parameters

## Links to L5 Examples

- `../L5_examples/fugacity_activity_examples.md` - Worked examples
