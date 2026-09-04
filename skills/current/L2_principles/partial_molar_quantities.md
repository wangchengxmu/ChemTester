---
id: chemistry.partial_molar_quantities
layer: 2
title: Partial Molar Quantities
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch9
last_verified: 2026-03-15
---

## Core Concept

Partial molar quantities describe how extensive properties change with composition.

### Definition

For extensive property X:
X_i = (∂X/∂n_i)_T,p,n_j≠i

### Chemical Potential

μ_i = (∂G/∂n_i)_T,p,n_j≠i = G̅_i (partial molar Gibbs energy)

## Key Formulas

```
# Total property from partial molar
X = Σ n_i X̄_i

# Gibbs-Duhem equation
Σ x_i dμ_i = 0  (at constant T, p)

# Apparent molar volume
V_φ = (V - n₁V₁*)/n₂

# Mixing quantities
ΔV_mix = V - Σ n_i V_i* = Σ n_i(V̄_i - V_i*)
ΔH_mix = H - Σ n_i H_i* = Σ n_i(H̄_i - H_i*)
```

## Important Relations

- **Partial molar volume**: V̄_i = (∂V/∂n_i)_T,p,n_j≠i
- **Partial molar enthalpy**: H̄_i = (∂H/∂n_i)_T,p,n_j≠i
- **Partial molar entropy**: S̄_i = (∂S/∂n_i)_T,p,n_j≠i

## Problem-Solving Routes

1. **Calculate partial molar quantity** → From derivative or intercept method
2. **Apply Gibbs-Duhem** → Find one partial from another
3. **Determine mixing quantities** → Compare to pure component values
4. **Find chemical potential** → From Gibbs energy measurement

## Links to L3 Tools

- `../L3_functions/partial_molar.py` - Partial molar calculations
- `../L3_functions/gibbs_duhem.py` - Gibbs-Duhem integration

## Links to L4 Data

- `../L4_reference/partial_molar_data.md` - Partial molar volumes, enthalpies

## Links to L5 Examples

- `../L5_examples/partial_molar_examples.md` - Worked examples
