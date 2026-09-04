---
id: chemistry.equilibrium_constant
layer: 2
title: Thermodynamic Equilibrium Constant
parent: chemistry.core_map
stability: high
confidence: high
source: DeVoe Thermodynamics and Chemistry, Ch11.8
source_url: https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/DeVoes_Thermodynamics_and_Chemistry/11%3A_Reactions_and_Other_Chemical_Processes/11.08%3A_The_Thermodynamic_Equilibrium_Constant
last_verified: 2026-03-15
---

## Core Concept

The thermodynamic equilibrium constant K relates to the standard Gibbs energy of reaction.

## Key Equations (from source)

### Chemical Potential with Activity (Eq 11.8.1)
```
μ_i = μ_i° + RT ln a_i + z_i F φ
```

### Reaction Quotient (Eq 11.8.6)
```
Q_rxn = ∏ a_i^ν_i
```
Where ν_i is positive for products, negative for reactants.

### Thermodynamic Equilibrium Constant (Eq 11.8.9)
```
K = ∏ (a_i)_eq^ν_i
```

### Relation to Standard Gibbs Energy (Eq 11.8.10-11.8.11)
```
Δ_rG° = -RT ln K      Eq 11.8.10
K = exp(-Δ_rG°/RT)    Eq 11.8.11
```

## Key Rules (from source)

1. "The value of Δ_rG° depends only on T and the choice of the standard states of the reactants and products. This being so, Eq. 11.8.11 shows that the value of K for a given reaction depends only on T and the choice of standard states. No other condition, neither pressure nor composition, can affect the value of K."

2. "We also see from Eq. 11.8.11 that K is less than 1 if Δ_rG° is positive and greater than 1 if Δ_rG° is negative."

3. "At a fixed temperature, reaction equilibrium is attained only if and only if the value of Q_rxn becomes equal to the value of K at that temperature."

## Gibbs-Helmholtz Relation (Eq 11.8.20)
```
Δ_rG = Δ_rH - TΔ_rS
```

## Standard States

From source context:
- **Gases**: Pure gas behaving ideally at p° = 1 bar
- **Solutes**: Based on mole fraction, concentration, or molality
- **Pure solids/liquids**: Pure substance at p° = 1 bar

## Problem-Solving Routes

1. **Calculate K from ΔG°** → Use K = exp(-Δ_rG°/RT)
2. **Calculate ΔG° from K** → Use Δ_rG° = -RT ln K
3. **Determine equilibrium position** → Compare Q_rxn to K
4. **Predict reaction direction** → Q < K: forward; Q > K: reverse

## Links to L3 Tools

- `../L3_functions/equilibrium_constant_tools.py` - K calculations

## Links to L4 Data

- `../L4_reference/thermodynamic_data.csv` - Standard ΔG° values

## Links to L5 Examples

- `../L5_examples/acid_base_examples.md - Worked examples

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives

**Source:** `equilibrium_constant_tools.py`

Equilibrium Constant Tools - L3 Implementation

### Available functions:
- `calculate_Kc(equilibrium_concentrations: Dict[str, float], products: Dict[str, int], reactants: Dict[str, int])` → float — Calculate Kc from equilibrium concentrations.
- `Kc_to_Kp(Kc: float, delta_n: int, T: float)` → float — Convert Kc to Kp.
- `Kp_to_Kc(Kp: float, delta_n: int, T: float)` → float — Convert Kp to Kc.
- `interpret_K(K: float)` → str — Interpret the meaning of K value.
- `Q_expression_string(products: Dict[str, int], reactants: Dict[str, int])` → str — Generate Q expression string.
- `calculate_Qp(partial_pressures: Dict[str, float], products: Dict[str, int], reactants: Dict[str, int])` → float — Calculate Qp from partial pressures.
- `concentration_from_Kc(Kc: float, known_concs: Dict[str, float], unknown_species: str, coeff: int, products: Dict[str, int], reactants: Dict[str, int])` → float — Calculate unknown equilibrium concentration from Kc.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
