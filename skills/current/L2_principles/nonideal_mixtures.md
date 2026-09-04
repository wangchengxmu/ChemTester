---
id: nonideal-mixtures-activity
layer: L2
topic: thermodynamics
source: DeVoe Ch10
depends: [mixtures_partial_molar, debye_huckel]
tags: [thermodynamics, activity, fugacity, excess-properties, henry-law, raoult]
---

# Nonideal Mixtures: Activity and Fugacity

## Concept Overview
Real mixtures deviate from ideal behavior due to intermolecular interactions. Activity coefficients quantify these deviations and are essential for modeling phase equilibria and reaction equilibria in nonideal systems.

## Key Principles

### Raoult's Law (ideal solvent behavior)
```
p_i = x_i p_i*  (for solvent at x_i → 1)
```

### Henry's Law (dilute solute behavior)
```
p_B = k_{H,B} x_B  (for solute at x_B → 0)
```
Henry's law constant k_{H,B} depends on T and the specific solute-solvent pair.

### Activity Coefficients
**Convention I (symmetric, Raoult's law basis):**
```
a_i = γᵢ xᵢ,  γᵢ → 1 as xᵢ → 1
```
Used for all components in mixtures of similar substances.

**Convention II (unsymmetric, Henry's law basis):**
```
Solvent: a_A = γ_A x_A,  γ_A → 1 as x_A → 1
Solute: a_B = γ_{x,B} x_B,  γ_{x,B} → 1 as x_B → 0
```
Used for dilute solutions.

### Excess Properties
Difference between real and ideal mixture properties:
```
X^E = X − X^id
G^E = G − Σᵢ nᵢ(μᵢ* + RT ln xᵢ)
G^E = Σᵢ nᵢ RT ln γᵢ  (Convention I)
```

**Common excess Gibbs energy models:**
- **Two-suffix Margules (1-parameter):** G^E/(nRT) = A x_A x_B
- **Three-suffix Margules (2-parameter):** G^E/(nRT) = x_A x_B (A_{21} x_A + A_{12} x_B)
- **Van Laar:** G^E/(nRT) = A_{12}A_{21}x_Ax_B / (A_{12}x_A + A_{21}x_B)
- **Wilson, NRTL, UNIQUAC:** more sophisticated models for strongly nonideal systems

### Azeotropes
When γ_A = γ_B, the mixture boils at constant composition:
- Minimum boiling azeotrope (γ > 1, positive deviation)
- Maximum boiling azeotrope (γ < 1, negative deviation)

### Debye-Hückel Theory (electrolyte solutions)
For dilute electrolyte solutions, mean ionic activity coefficient:
```
ln γ± = −A|z₊z₋|√I  (Debye-Hückel limiting law)
```
where I = ½ Σᵢ mᵢ zᵢ² (ionic strength), A ≈ 1.171 (kg/mol)^(1/2) at 25°C in water.

**Extended Debye-Hückel:**
```
ln γ± = −A|z₊z₋|√I / (1 + Ba√I)
```

## L3 Tools
- `L3_functions/nonideal_mixture_tools.py` — activity coefficient models, VLE calculations
- See existing `debye_huckel` L2

## L4 Data
- Margules parameters, azeotrope data in `L4_data/solution_data/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch10 (Nonideal Mixtures).

## L3 Tool Call Directives

**Source:** nonideal_mixture_tools.py
Nonideal Mixture Tools - Activity coefficients, Raoult's/Henry's law, azeotropes.

### Available functions:
- raoult_pv(x, pvap_pure) → float — Raoult's law: P_i = x_i · P_i*.
- henry_law(c, kh) → float — Henry's law: P = k_H · c.
- margules_one_suffix(x1, A12) → float — One-suffix Margules activity coefficient for component 1.
- bubble_point_temperature(xs, Psat_func, P_total, tol) →  — Simple bubble point calculation via iterative search.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments

---

**Source:** le_tools.py
Vapor-liquid equilibrium: bubble point, dew point, relative volatility.

### Available functions:
- ubble_pressure(xs, Psat_func, T) �� float �� ��(x?��P????); Psat_func(i, T) callable
- dew_pressure(ys, Psat_func, T) �� float �� 1/��(y?/P????)
- elative_volatility(Psat1: float, Psat2: float) �� float �� �� = P????/P????

### Common errors:
- ? Psat_func must be a callable, not a list of values
- ? xs/ys must sum to ~1.0 for physically meaningful results
