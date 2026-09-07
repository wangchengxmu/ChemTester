---
id: chemistry.legendre_transforms
layer: 2
title: Legendre Transforms and Thermodynamic Potentials
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch5.3
source_url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/05%3A_Thermodynamic_Potentials/5.03%3A_Enthalpy_Helmholtz_Energy_and_Gibbs_Energy
last_verified: 2026-03-15
---

## Core Concept

**Source**: DeVoe Ch5.3 (verbatim)

> "A Legendre transform of a dependent variable is made by subtracting one or more products of conjugate variables. In the total differential dU = TdS - pdV, T and S are conjugates (that is, they comprise a conjugate pair), and -p and V are conjugates."

## Definitions (from source Eq 5.3.1-5.3.3)

| Potential | Definition | Equation # |
|-----------|------------|------------|
| Enthalpy | H ≡ U + pV | Eq 5.3.1 |
| Helmholtz energy | A ≡ U - TS | Eq 5.3.2 |
| Gibbs energy | G ≡ U - TS + pV = H - TS | Eq 5.3.3 |

## Natural Variables (from source)

> "The independent variables in this equation [dU = TdS - pdV], S and V, are called the natural variables of U."

| Potential | Natural Variables | Total Differential |
|-----------|-------------------|-------------------|
| U | S, V | dU = TdS - pdV |
| H | S, p | dH = TdS + Vdp |
| A | T, V | dA = -SdT - pdV |
| G | T, p | dG = -SdT + Vdp |

## Total Differentials (from source Eq 5.3.4-5.3.6)

```
dH = dU + pdV + Vdp       (Eq 5.3.4)
dA = dU - TdS - SdT       (Eq 5.3.5)
dG = dU - TdS - SdT + pdV + Vdp  (Eq 5.3.6)
```

## Conjugate Variables

From source: "T and S are conjugates, and -p and V are conjugates."

## Heat Relations (from source Eq 5.3.7-5.3.9)

```
dH = đq   (closed system, constant p, dw' = 0)  Eq 5.3.7
ΔH = q    (closed system, constant p, w' = 0)   Eq 5.3.8
dU = đq   (closed system, constant V, dw' = 0)  Eq 5.3.9
```

## Key Rules (from source)

1. "These definitions are used whether or not the system has only two independent variables."

2. "The enthalpy, Helmholtz energy, and Gibbs energy are state functions (because the quantities used to define them are state functions) and are extensive (because U, S, and V are extensive)."

3. "In a process at constant pressure (dp = 0) with expansion work only (dw' = 0), the enthalpy change under these conditions is equal to the heat."

## Problem-Solving Routes

1. **Calculate H, A, G from U** → Apply definitions with known p, V, T, S
2. **Find natural variables** → Identify independent variables in total differential
3. **Relate to heat** → Use dH = đq at constant p, or dU = đq at constant V

## Links to L3 Tools

- `../L3_functions/thermodynamic_potentials.py` - Calculate H, A, G

## Links to L4 Data


## Links to L5 Examples

- `../L5_examples/thermal_analysis/ - Worked examples