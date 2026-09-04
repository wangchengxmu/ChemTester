---
id: phase-transitions
layer: L2
topic: thermodynamics
source: DeVoe Ch8
depends: [material_equilibrium, phase_diagrams]
tags: [thermodynamics, phase-transition, clapeyron, critical-point, triple-point]
down_links:
  - ../L3_functions/phase_diagrams_tools.py
  - ../L3_functions/phase_diagram_tools.py
---

# Phase Transitions

## Concept Overview
Phase transitions are equilibrium processes in which a pure substance transfers between coexisting phases at constant temperature and pressure. The chapter covers equilibrium conditions, phase diagrams, molar transition quantities, and quantitative relations for coexistence curves.

## Key Principles

### Equilibrium Conditions for Multiphase Systems (DeVoe 8.1)
For a system of a single substance in two or more uniform phases without internal partitions, at equilibrium:
- **Thermal equilibrium**: T is uniform across all phases
- **Mechanical equilibrium**: p is uniform across all phases
- **Transfer equilibrium**: μ is uniform across all phases

**Derivation**: Maximize entropy of the isolated system. Using dU = TdS − pdV + μdn for each phase, the condition dS = 0 for any infinitesimal virtual displacement requires all three equalities.

**Simple argument for transfer equilibrium**: At constant T, p, G decreases during spontaneous process. Transfer from phase of higher μ to lower μ is spontaneous. No transfer when μ is equal → equilibrium.

### Molar Transition Quantities (DeVoe 8.3)
For transfer of amount n from phase α to phase β at constant T, p:
```
Δ_trs H = H_m(β) − H_m(α)     (molar enthalpy of transition)
Δ_trs S = S_m(β) − S_m(α)     (molar entropy of transition)
Δ_trs G = μ(β) − μ(α) = 0     (always zero at equilibrium!)
```

**Key relation** (from ΔG = ΔH − TΔS = 0):
```
Δ_trs S = Δ_trs H / T_trs
```

**Standard molar transition quantities**: Δ_vap H° = H_m°(g) − H_m(liquid). Note the gas standard state is hypothetical (ideal gas at p°). Requires correction from real equilibrium transition data.

**Calorimetric measurement** (DeVoe 8.3.2): Electrical work in constant-p adiabatic calorimeter; temperature stays constant during phase transition.

### Types of Phase Transitions
| Symbol | Process | Typical ΔH (kJ/mol) |
|--------|---------|---------------------|
| Δ_fus H | solid → liquid | 2–30 |
| Δ_vap H | liquid → gas | 20–45 |
| Δ_sub H | solid → gas | Δ_fus H + Δ_vap H |

At the triple point: Δ_fus H + Δ_vap H = Δ_sub H

### Classification (Ehrenfest)
**First-order transitions:**
- Discontinuity in V, S, H (first derivatives of G)
- Latent heat: q_p = ΔH_trans ≠ 0
- Governed by Clapeyron equation

**Second-order transitions:**
- Continuous in V and S; discontinuity in C_p, α, κ_T (second derivatives of G)
- No latent heat

### Critical Phenomena
- Critical point: liquid-gas distinction disappears
- Near critical point: C_p → ∞, κ_T → ∞
- Not valid to approximate V_m(g) >> V_m(condensed) near critical point

### Trouton's Rule (approximate)
For many nonpolar liquids at the normal boiling point:
```
ΔS_vap ≈ 88 J/(mol·K)
```
Exceptions: hydrogen-bonded liquids (water ~109), helium (~20).

## Coexistence Curves (DeVoe 8.4)

### Clapeyron Equation (exact)
For two coexisting phases α and β:
```
dp/dT = Δ_trs S / Δ_trs V = Δ_trs H / (T · Δ_trs V)
```
No approximations. The slope depends on sign of Δ_trs V:
- Vaporization/sublimation: positive slope (both ΔH, ΔV > 0)
- Fusion: slope depends on whether substance expands or contracts on melting

**Integration for fusion** (Δ_fus V ≈ const, Δ_fus H ≈ const):
```
T₂ ≈ T₁ · exp[Δ_fus V · (p₂ − p₁) / Δ_fus H]
```

### Clausius-Clapeyron Equation (approximate)
For vaporization/sublimation, where V_m(g) >> V_m(condensed) and gas ≈ ideal:
```
dp/dT ≈ p · Δ_trs H / (RT²)
```

**Alternative forms**:
```
d ln(p/p°) / dT ≈ Δ_trs H / (RT²)
d ln(p/p°) ≈ −(Δ_trs H/R) · d(1/T)
d ln(p/p°) / d(1/T) ≈ −Δ_trs H/R
```

**Integrated form** (Δ_trs H ≈ const):
```
ln(p₂/p₁) ≈ −(Δ_trs H/R)(1/T₂ − 1/T₁)
```

A plot of ln(p/p°) vs 1/T has slope ≈ −Δ_vap H/R.

### Antoine Equation (empirical)
```
ln(p/bar) = a − b/(T + c)
```
More accurate than Clausius-Clapeyron over limited ranges.

## Special Topics (DeVoe 8.1.4–8.1.5)

### Barometric Formula
For a tall column of ideal gas at equilibrium in gravitational field:
```
p(h) = p(0) · exp(−Mgh/RT)
```
or equivalently: dp = −ρg dh (general hydrostatic relation).

### Pressure in a Liquid Droplet
For a spherical droplet of radius r with surface tension γ:
```
p_liquid = p_gas + 2γ/r
```
(Kelvin equation derivation from dU including surface work term γdA_s.)

## L3 Tools
- `L3_functions/phase_equilibrium_tools.py` — Clapeyron/Clausius-Clapeyron calculations, phase boundary computations
- `L3_functions/gibbs_free_energy_tools.py` — transition Gibbs energy checks

## L4 Data
- Triple points and critical points in `L4_data/thermodynamic_tables/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch8 (Phase Transitions and Equilibria of Pure Substances). LibreTexts: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/08%3A_Phase_Transitions_and_Equilibria_of_Pure_Substances

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook
