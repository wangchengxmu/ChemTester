# L2 Topic: Surface Chemistry

**Source**: Surface Science (Nix), Ch3
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Surface chemistry deals with phenomena occurring at interfaces, particularly adsorption of gases on solid surfaces.

### Key Features
1. **Langmuir isotherm** - Monolayer adsorption model
2. **Surface coverage (θ)** - Fraction of occupied sites
3. **Equilibrium constant (b)** - Temperature-dependent
4. **Kinetic derivation** - From rates of adsorption/desorption

---

## Core Principles

### Langmuir Isotherm
```
θ = bP / (1 + bP)
```

| Variable | Meaning | Units |
|----------|---------|-------|
| θ | Surface coverage | fraction (0-1) |
| P | Gas pressure | atm or Pa |
| b | Equilibrium constant | atm⁻¹ or Pa⁻¹ |

### Temperature Dependence
```
b ∝ exp(-ΔH_ads / RT)
```
- Exothermic adsorption: b decreases with T
- Endothermic: b increases with T

---

## Decision Trees

### Checking Langmuir Validity
```
Is adsorption monolayer? 
├── Yes → Langmuir applicable
└── No → Use BET isotherm

Is ΔH_ads constant with coverage?
├── Yes → Langmuir valid
└── No → Use Freundlich isotherm
```

### Interpreting Coverage
```
θ ≈ 1? → Near saturation
θ ≈ 0.5? → bP = 1
θ << 1? → θ ≈ bP (linear regime)
```

---

## Key Tables

### Isotherm Comparison

| Isotherm | Application | Key Feature |
|----------|-------------|-------------|
| Langmuir | Monolayer | Constant ΔH |
| BET | Multilayer | P/P₀ < 1 |
| Freundlich | Heterogeneous | Variable ΔH |
| Temkin | Heterogeneous | Linear ΔH decrease |

### Langmuir Assumptions

| # | Assumption | Implication |
|---|------------|-------------|
| 1 | Localized sites | Discrete adsorption |
| 2 | Constant ΔH | Independent of θ |
| 3 | Monolayer | Maximum θ = 1 |
| 4 | No interactions | Non-cooperative |

---

## Connected Topics

- **Upstream**: [chemical_equilibrium.md](chemical_equilibrium.md)
- **Related**: [catalysis.md](catalysis.md)
- **Downstream**: [surface_kinetics.md](surface_kinetics.md)

---

## L3 Tools Required

1. `surface_chemistry_tools.py` - Langmuir calculations

---

## L4 References (TODO)

- [x] Langmuir equation
- [ ] BET equation
- [ ] Freundlich parameters

---

## L5 Worked Examples (TODO)

- [ ] Coverage calculation
- [ ] Linear regression analysis

## L3 Tool Call Directives

**Source:** `surface_chemistry_tools.py`

Langmuir isotherm calculations: coverage, pressure, constant determination, temperature dependence, linear analysis.

### Available functions:
- `langmuir_coverage(P, b)` → dict — θ = bP/(1+bP) with regime classification
- `langmuir_pressure(theta, b)` → dict — P = θ/(b(1-θ)) for desired coverage
- `langmuir_constant(theta, P)` → dict — b = θ/(P(1-θ)) from experimental data
- `langmuir_temperature_effect(b1, T1, T2, delta_H)` → dict — b₂/b₁ = exp(ΔH/R × (1/T₁ - 1/T₂))
- `langmuir_linear_analysis(P_data, V_data)` → dict — Linear regression for V_mono and b (P/V vs P plot)
- `langmuir_linear_form(P, V, V_mono, b)` → dict — Verify linear form P/V = 1/(V_mono×b) + P/V_mono

### Common errors:
- ❌ θ outside (0,1) in langmuir_pressure/langmuir_constant — physically impossible
- ❌ Using wrong units for ΔH_ads — must be J/mol (negative for exothermic adsorption)
