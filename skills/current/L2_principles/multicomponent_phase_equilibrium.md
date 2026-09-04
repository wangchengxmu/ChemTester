---
id: multicomponent-phase-equilibrium
layer: L2
topic: thermodynamics
source: DeVoe Ch13
depends: [material_equilibrium, mixtures_partial_molar, nonideal_mixtures]
tags: [thermodynamics, vle, lle, ternary, lever-rule, distillation]
down_links:
  - ../L3_functions/phase_equilibria_tools.py
  - ../L3_functions/phase_equilibrium_tools.py
---

# Multicomponent Phase Equilibrium

## Concept Overview
Multicomponent phase equilibrium deals with systems containing two or more components distributed across multiple phases. Key applications include vapor-liquid equilibrium (VLE), liquid-liquid extraction, and ternary phase diagrams.

## Key Principles

### Binary VLE (Vapor-Liquid Equilibrium)
At equilibrium: yᵢ φᵢ p = xᵢ γᵢ fᵢ* (modified Raoult's law)

For ideal mixtures (φᵢ = 1, γᵢ = 1):
```
p = x_A p_A* + x_B p_B*  (total pressure)
y_i = x_i p_i*/p  (vapor composition)
```

**T-x-y and P-x-y diagrams** show bubble-point and dew-point curves.

### Lever Rule
In a two-phase region, the fraction of each phase:
```
n_α/n_total = (z_B − x_B)/(y_B − x_B)
n_β/n_total = (y_B − z_B)/(y_B − x_B)
```
where z_B is overall composition.

### Raoult's Law for Binary VLE
```
y_B p = x_B γ_B p_B*
y_A p = x_A γ_A p_A*
```
For ideal: γ_A = γ_B = 1

### Gibbs Phase Rule (multicomponent)
```
F = C − P + 2
```
Binary VLE (C=2, P=2): F = 2 → specify T and one composition variable
Ternary LLE (C=3, P=2): F = 3

### Ternary Phase Diagrams
- Triangular coordinates (Gibbs triangle)
- Tie lines connect equilibrium phase compositions
- Plait point: critical point where two liquid phases become identical
- Applications: liquid-liquid extraction design

### Azeotropes in Binary Systems
- **Positive deviation (γ > 1):** minimum-boiling azeotrope
- **Negative deviation (γ < 1):** maximum-boiling azeotrope
- Azeotropes cannot be separated by simple distillation

### Steam Distillation
For immiscible liquids:
```
p = p_A* + p_B* (total vapor pressure)
T_distill < min(T_boil_A, T_boil_B)
```

## L3 Tools
- `L3_functions/vle_tools.py` — bubble/dew point calculations, VLE diagrams, azeotrope detection

## L4 Data
- Antoine equation parameters in `L4_data/vapor_pressure_data/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch13 (Multicomponent Phase Equilibrium).

## L3 Tool Call Directives

**Source:** phase_equilibrium_tools.py
Phase Equilibrium Tools - Clapeyron, Clausius-Clapeyron, phase rule.

### Available functions:
- clapeyron_dp_dt(dh, dv, T) → float — Clapeyron equation: dP/dT = DeltaH / (T·DeltaV).
- clausius_clapeyron(T1, P1, T2, dh_vap) → float — Clausius-Clapeyron: ln(P2/P1) = -DeltaH_vap/R · (1/T2 - 1/T1). Returns P2.
- gibbs_phase_rule(components, phases) → int — Gibbs phase rule: F = C - P + 2.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
