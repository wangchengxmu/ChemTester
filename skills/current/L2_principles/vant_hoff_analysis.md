---
id: chemistry.vant_hoff_analysis
layer: 2
title: van't Hoff Analysis for Temperature Dependence
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch11
last_verified: 2026-03-15
---

## Core Concept

The van't Hoff equation relates equilibrium constant temperature dependence to reaction enthalpy.

## Key Formulas

```
# van't Hoff equation
d ln K / dT = ΔH° / (RT²)

# Integrated form (constant ΔH°)
ln(K₂/K₁) = -(ΔH°/R)(1/T₂ - 1/T₁)

# Alternative form
d ln K / d(1/T) = -ΔH°/R

# From ΔG° = -RT ln K
ln K = -ΔG°/(RT) = -ΔH°/(RT) + ΔS°/R
```

## Analysis Methods

1. **van't Hoff plot**: ln K vs 1/T → slope = -ΔH°/R
2. **From ΔG° at different T**: Extract ΔH° and ΔS°
3. **Temperature dependence**: Predict K at new T

## Assumptions

- Constant ΔH° (independent of T)
- Valid for small temperature ranges
- For large ranges: integrate ΔH°(T) = ΔH° + ∫ΔC_p dT

## Problem-Solving Routes

1. **Find ΔH° from K(T)** → Plot ln K vs 1/T
2. **Predict K at new T** → Apply integrated equation
3. **Determine ΔS°** → From intercept (ln K at 1/T → 0)
4. **Correct for ΔC_p** → Integrate temperature dependence

## Links to L3 Tools

- `../L3_functions/vant_hoff.py` - van't Hoff analysis
- `../L3_functions/equilibrium_temperature.py` - K at different T

## Links to L4 Data

- `../L4_reference/thermodynamic_data.md` - ΔH°, ΔS° values

## Links to L5 Examples

- `../L5_examples/vant_hoff_examples.md` - Worked examples
