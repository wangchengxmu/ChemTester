---
id: chem.reaction_rates
layer: 2
title: Chemical Reaction Rates and Rate Expressions
source: Ch12.01
dependencies: [stoichiometry]
stability: high
confidence: high
---

## Concept

Reaction rate is the change in concentration of reactants or products per unit time. Rates are determined experimentally by measuring concentration changes over time.

## Core Formulas

### Basic Rate Expression
```
rate = -¦¤[reactant]/¦¤t = +¦¤[product]/¦¤t
```

### Relative Rates (from stoichiometry)
```
For: aA + bB ¡ú cC + dD

rate = -(1/a)(¦¤[A]/¦¤t) = -(1/b)(¦¤[B]/¦¤t) = +(1/c)(¦¤[C]/¦¤t) = +(1/d)(¦¤[D]/¦¤t)
```

### Average vs Instantaneous Rate
```
Average rate = ¦¤[ ]/¦¤t  (over time interval)
Instantaneous rate = d[ ]/dt  (at specific time, slope of tangent)
Initial rate = rate at t = 0
```

## Decision Tree

```
Calculating reaction rate?
©À©¤ From concentration data?
©¦   ©À©¤ Average rate ¡ú ¦¤[ ]/¦¤t
©¦   ©¸©¤ Instantaneous ¡ú slope of tangent on [ ] vs t plot
©À©¤ From other species rate?
©¦   ©¸©¤ Use stoichiometric coefficients
©¸©¤ Need expression?
    ©¸©¤ rate = ¡À(1/coeff) ¡Á ¦¤[species]/¦¤t
```

## Key Constraints
- Reactant rates are negative (decreasing)
- Product rates are positive (increasing)
- Rate is always reported as positive value
- Units: M/s or M¡¤min?1 or M¡¤h?1

## Problem Archetypes
1. Calculate average rate from concentration data
2. Express relative rates from reaction stoichiometry
3. Find instantaneous rate from graph tangent
4. Convert between different rate expressions

## L3 Tools
- `average_rate(C1, C2, t1, t2)` ¡ú rate
- `relative_rate_expression(equation)` ¡ú expressions
- `instantaneous_rate(concentration_data, t)` ¡ú rate

## L4 Reference

## L5 Examples
See `../L5_examples/kinetics_examples.md for worked examples.

## Implementations

- Implementation: `../L3_functions/reaction_rate_tools.py`

## L3 Tool Call Directives

**Source:** `gas_phase_dynamics_tools.py`

Gas-phase reaction dynamics: collision theory, transition state theory, rate constants, kinetic isotope effects, and diffusion-controlled reactions.

### Available functions:
- `relative_velocity(T, mu_amu)` → float — Average relative velocity v_rel = √(8kT/πμ); μ in amu
- `collision_frequency(T, P, sigma_collision_m2, mu_amu)` → float — Collisions per molecule per second
- `collision_frequency_molar(T, P, sigma_collision_m2, mu_amu)` → float — Molar collision frequency
- `collision_cross_section(d1_m, d2_m)` → float — σ = π(d₁+d₂)²/4 from molecular diameters
- `collision_theory_rate_constant(T, sigma_m2, mu_amu, E_a=0)` → float — k = σv_rel×exp(-Ea/RT) in m³/(molecule·s)
- `steric_factor(k_experimental, k_collision)` → float — P = k_exp/k_collision (typically 0.01-1)
- `tst_rate_constant(T, delta_H_double_dagger, delta_S_double_dagger, transmission_coeff=1.0)` → float — TST rate k = κ(k_BT/h)exp(ΔS‡/R)exp(-ΔH‡/RT)
- `eyring_equation(T, delta_G_double_dagger)` → float — k = (k_BT/h)exp(-ΔG‡/RT)
- `activation_parameters_from_rates(T1, k1, T2, k2)` → Dict — Returns ΔH‡, ΔS‡, ΔG‡ from Eyring plot
- `pre_exponential_factor_tst(T, delta_S_double_dagger)` → float — A = (k_BT/h)exp(ΔS‡/R)
- `mean_free_path(T, P, sigma_collision)` → float — λ = kT/(√2×P×σ)
- `diffusion_controlled_rate_constant(T, eta_Pa_s, r1_m, r2_m)` → float — k_D in L/(mol·s) via Stokes-Einstein
- `is_diffusion_controlled(k_observed, k_diffusion)` → bool — True if k_obs ≥ 0.5×k_diff
- `primary_kinetic_isotope_effect(m_light, m_heavy, T, E0_light, E0_heavy)` → float — KIE ≈ √(m_heavy/m_light)×exp((E0_heavy-E0_light)/RT)
- `tunneling_correction_wigner(T, nu_TS_cm)` → float — κ = 1 + (hν‡/kT)²/24
- `get_collision_diameter(molecule)` → float — Look up collision diameter for common gases

### Common errors:
- ❌ Using J/mol for activation energy with R=8.314 (consistent units required)
- ❌ Forgetting to convert m³/(molecule·s) to L/(mol·s) by multiplying by AVOGADRO×1000
- ❌ Not converting wavenumber (cm⁻¹) to Hz for tunneling correction (handled internally)

---

**Source:** `reaction_rate_tools.py`

Average rate, instantaneous rate, relative rate expressions, and stoichiometric rate conversions.

### Available functions:
- `average_rate(C1, C2, t1, t2, reactant=True)` → float — Average rate |ΔC|/Δt
- `relative_rate_expression(coefficients)` → Dict[str, str] — Rate expressions per species (reactants negative, products positive)
- `convert_rate(rate, species1, coeff1, species2, coeff2)` → float — Convert rate between species via stoichiometry
- `instantaneous_rate(concentrations, times, t_target)` → float — Estimate d[A]/dt at target time
- `rate_from_stoichiometry(rate_known, coeff_known, coeff_unknown)` → float — Rate conversion by |coeff_unknown|/|coeff_known|
- `initial_rate_method(rates, concentrations)` → float — Initial rate from first data point

### Common errors:
- ❌ Forgetting sign convention: reactants negative, products positive in coefficients dict
- ❌ Not taking absolute value of coefficients when converting rates
