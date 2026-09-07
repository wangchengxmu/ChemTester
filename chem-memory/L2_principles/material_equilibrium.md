---
id: material-equilibrium
layer: L2
topic: thermodynamics
source: DeVoe Ch7
depends: [thermodynamic_potentials, gibbs_free_energy, spontaneity_criteria]
tags: [thermodynamics, equilibrium, phase-rule, clapeyron, gibbs-duhem]
---

# Material Equilibrium

## Concept Overview
Material equilibrium concerns equilibrium between phases and between substances in chemical reactions. The Gibbs phase rule determines the number of independent intensive variables (degrees of freedom) in a heterogeneous system.

## Key Principles

### Conditions for Phase Equilibrium
For phases α and β in contact:
```
T^α = T^β  (thermal equilibrium)
p^α = p^β  (mechanical equilibrium)
μᵢ^α = μᵢ^β  (material equilibrium for each component i)
```

### Phase Rule (Gibbs)
```
F = C − P + 2
```
- F = degrees of freedom (number of intensive variables that can be independently varied)
- C = number of components (chemically independent constituents)
- P = number of phases

### Clapeyron Equation
For a first-order phase transition:
```
dp/dT = ΔS_trans/ΔV_trans = ΔH_trans/(T·ΔV_trans)
```

### Clausius-Clapeyron Equation
For liquid-vapor or solid-vapor equilibrium (assuming vapor is ideal gas and ΔH_vap is constant):
```
ln(p₂/p₁) = −ΔH_vap/R · (1/T₂ − 1/T₁)
```
Or in integrated form:
```
ln(p) = −ΔH_vap/(RT) + C
```

### Gibbs-Duhem Equation
Relates changes in chemical potential of components:
```
Σᵢ nᵢ dμᵢ + SdT − Vdp = 0
```
At constant T, p: Σᵢ xᵢ dμᵢ = 0

### Phase Stability
A single phase is stable if:
```
(∂²G/∂x²)_{T,p} > 0
```
When this is violated, phase separation occurs (binodal/spinodal curves).

## L3 Tools
- `L3_functions/phase_equilibrium_tools.py` — Clapeyron calculations, phase rule, binodal/spinodal analysis

## L4 Data
- Vapor pressure and transition enthalpy data in `L4_data/vapor_pressure_data/`

## Source
DeVoe, *Thermodynamics and Chemistry*, Ch7 (Material Equilibrium).

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook
