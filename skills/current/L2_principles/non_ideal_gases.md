---
id: chem.non_ideal_gases
layer: 2
title: Non-Ideal Gas Behavior and van der Waals Equation
source: Ch08.07
dependencies: [ideal_gas_law]
stability: high
confidence: high
---

## Concept

Real gases deviate from ideal behavior at high pressure and low temperature due to molecular volume and intermolecular forces.

## Core Formulas

### Compressibility Factor
```
Z = PV_m/(RT) = PV/(nRT)

Z = 1: ideal gas
Z < 1: attractive forces dominate
Z > 1: molecular volume dominates
```

### van der Waals Equation
```
(P + n2a/V2)(V - nb) = nRT

Where:
- a = correction for intermolecular attraction
- b = correction for molecular volume
```

### Solving van der Waals
```
For pressure: P = nRT/(V-nb) - n2a/V2
For volume: solve cubic equation numerically
```

## Decision Tree

```
Is gas behavior ideal?
©À©¤ Low P, high T ¡ú Yes, use PV = nRT
©¸©¤ High P or low T ¡ú No, use van der Waals

Choosing van der Waals calculation?
©À©¤ Find P ¡ú P = nRT/(V-nb) - n2a/V2
©À©¤ Find V ¡ú Solve cubic or use numerical method
©¸©¤ Find T or n ¡ú Rearrange and solve

Comparing ideal vs real?
©¸©¤ Calculate Z to quantify deviation
```

## van der Waals Constants

| Gas | a (L2¡¤atm/mol2) | b (L/mol) |
|-----|-----------------|-----------|
| N? | 1.39 | 0.0391 |
| O? | 1.36 | 0.0318 |
| CO? | 3.59 | 0.0427 |
| H?O | 5.46 | 0.0305 |
| He | 0.0342 | 0.0237 |

## Key Constraints
- a larger for gases with stronger attractions
- b larger for larger molecules
- van der Waals reduces to ideal at low P, high T

## Problem Archetypes
1. Calculate compressibility factor Z
2. Compare ideal vs real gas pressure
3. Use van der Waals to find P, V, or T
4. Predict when deviations occur

## L3 Tools
- `compressibility_factor(P, V, n, T)` ¡ú Z
- `van_der_waals_pressure(n, V, T, a, b)` ¡ú P
- `van_der_waals_volume(n, P, T, a, b)` ¡ú V
- `ideal_vs_real_comparison()` ¡ú comparison dict

## L4 Reference

## L5 Examples
See `../L5_examples/liquid_properties/ for worked examples.

## Implementations

- Implementation: `../L3_functions/non_ideal_gas_tools.py`

## L3 Tool Call Directives

**Source:** `non_ideal_gas_tools.py`
Van der Waals equation, compressibility factor, critical properties, deviation analysis.

### Available functions:
- `compressibility_factor(P, V, n, T, R=0.08206)` → float — Z = PV/(nRT); Z=1 ideal, <1 attractive dominate, >1 repulsive
- `van_der_waals_pressure(n, V, T, a, b, R=0.08206)` → float — P = nRT/(V-nb) - n²a/V²
- `van_der_waals_volume(n, P, T, a, b, R=0.08206, tolerance=0.001)` → float — Numerical Newton's method solution
- `ideal_vs_real(n, V, T, a, b, R=0.08206)` → dict — Compare ideal vs real pressure with deviation %
- `get_vdw_constants(gas)` → tuple — (a, b) for common gases (N2, CO2, H2O, etc.)
- `deviation_from_ideal(P, V, n, T, R=0.08206)` → dict — Z value + behavior interpretation

### Common errors:
- ❌ Unit mismatch: R defaults to L·atm/(mol·K); use R=8.314 for kPa
- ❌ Volume ≤ n·b in van der Waals — physically impossible, function clamps
- ❌ Forgetting to convert ΔHvap units when combining with VDW calculations

## L3 Tool Call Directives

**Source:** `van_der_waals_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
