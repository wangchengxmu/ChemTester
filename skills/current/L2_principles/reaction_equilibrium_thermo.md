---
id: reaction-equilibrium
layer: L2
topic: thermodynamics
source: DeVoe Ch11
depends: [gibbs_free_energy, thermodynamic_potentials, equilibrium_constant]
tags: [thermodynamics, equilibrium, equilibrium-constant, le-chatelier, vant-hoff]
---

# Reaction Equilibrium

## Concept Overview
Chemical equilibrium is the state where forward and reverse reaction rates are equal, characterized by the equilibrium constant K. The position of equilibrium depends on temperature, pressure, and composition via Le Chatelier's principle.

## Key Principles

### Standard Reaction Gibbs Energy
```
Δ_rG° = Σᵢ νᵢ Δ_fG°_i = −RT ln K
```
where νᵢ are stoichiometric coefficients (positive for products, negative for reactants).

### Equilibrium Constant Expressions
| Type | Expression | Notes |
|------|-----------|-------|
| K (thermodynamic) | Πᵢ a_i^{νᵢ} | Dimensionless, uses activities |
| K_p | Πᵢ (pᵢ/p°)^{νᵢ} | For gas-phase reactions |
| K_c | Πᵢ (cᵢ/c°)^{νᵢ} | For solution reactions |
| K_x | Πᵢ x_i^{νᵢ} | For ideal liquid mixtures |

### Relation between K_p and K_c (ideal gases)
```
K_p = K_c (RT/p°)^{Δν}
```
where Δν = Σ νᵢ(gas)

### van't Hoff Equation (temperature dependence)
```
d(ln K)/dT = Δ_rH°/(RT²)
```
Integrating (Δ_rH° constant):
```
ln(K₂/K₁) = −Δ_rH°/R · (1/T₂ − 1/T₁)
```

### Reaction Quotient and Direction
```
Q = Πᵢ a_i^{νᵢ} (at any composition)
Q < K → reaction proceeds forward
Q > K → reaction proceeds backward
Q = K → at equilibrium
```

### Le Chatelier's Principle
- **Temperature ↑:** equilibrium shifts in endothermic direction
- **Pressure ↑ (for gases):** equilibrium shifts toward fewer moles of gas
- **Adding reactant:** equilibrium shifts toward products

### Equilibrium Calculations
For a reaction aA + bB ⇌ cC + dD:
1. Set up ICE table (Initial, Change, Equilibrium)
2. Express K in terms of one unknown (extent of reaction ξ)
3. Solve for ξ (often requires quadratic or iterative solution)
4. For weak acids/bases: use approximations when applicable

## L3 Tools
- `L3_functions/equilibrium_tools.py` — ICE table solver, K from ΔG°, van't Hoff analysis
- See existing `equilibrium_constant`, `equilibrium_calculations` L2s

## L4 Data
- Standard formation data (Δ_fH°, Δ_fG°, S°) in `L4_data/thermodynamic_tables/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch11 (Reaction Equilibrium).

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook
