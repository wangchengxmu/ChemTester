---
id: chem.calorimetry
layer: 2
title: Calorimetry and Heat Measurement
source: LibreTexts Chemistry 2e Ch05.02
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Calorimetry and Heat Measurement

## Problem type
Measure heat of reaction using calorimetry data; determine enthalpy change.

## Decision tree

1. **What type of calorimeter?**
   - Coffee cup (constant pressure) → ΔH = q_p
   - Bomb calorimeter (constant volume) → ΔU = q_v

2. **What is asked?**
   - Heat of reaction → Use q = -mcΔT or q = -C_cal × ΔT
   - Enthalpy per mole → Divide by moles
   - Calorimeter constant → Use known reaction

3. **Known quantities?**
   - Mass and specific heat → q = mcΔT
   - Calorimeter constant → q = C_cal × ΔT

## Core formulas

### Heat balance
```
q_system + q_surroundings = 0
q_rxn = -q_solution (coffee cup)
q_rxn = -q_cal (bomb calorimeter)
```

### Coffee cup calorimetry (constant pressure)
```
q_solution = m_solution × c_solution × ΔT
q_rxn = -q_solution
ΔH = q_rxn / n  (per mole)
```

### Bomb calorimetry (constant volume)
```
q_cal = C_cal × ΔT
q_rxn = -q_cal
ΔU = q_rxn  (internal energy change)
```

### Relationship between ΔH and ΔU
```
ΔH = ΔU + Δ(PV) = ΔU + Δn_gas × R × T
where Δn_gas = moles of gaseous products - moles of gaseous reactants
```

## Constraints
- Coffee cup: constant pressure, measures ΔH
- Bomb calorimeter: constant volume, measures ΔU
- Assume solution density ≈ water (1 g/mL) if not given
- Assume c_solution ≈ c_water (4.184 J/g·°C) for dilute solutions

## Common patterns
1. Dissolution → measure temperature change, calculate ΔH_soln
2. Neutralization → measure heat, calculate ΔH_neut
3. Combustion → use bomb calorimeter, calculate ΔH_comb

## Example calculation

**Problem**: 50.0 mL of 0.10 M HCl mixed with 50.0 mL of 0.10 M NaOH. Temperature rises 2.5°C. Calculate ΔH_neut.

**Solution**:
```
m_solution = 100.0 g (assuming density 1 g/mL)
q_solution = 100.0 g × 4.184 J/g·°C × 2.5°C = 1046 J
q_rxn = -1046 J

Moles HCl = 0.050 L × 0.10 mol/L = 0.0050 mol
ΔH_neut = -1046 J / 0.0050 mol = -209,200 J/mol = -209 kJ/mol
```

## Links

### L3 Implementation
- `../L3_functions/calorimetry_tools.py` (TODO)

### L4 Reference
- `../L4_reference/reference/thermal-analysis-data.md` (TODO)

### L5 Examples
- `../L5_examples/thermal_analysis/ (TODO)

## Source trace
- `../sources/ingestion/source-thermochemistry-stepwise.md` section 5.02

## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook

## L3 Tool Call Directives


**Source:** `calorimetry_tools.py`

L3 tool module for calorimetry tools

### Available functions:
- `coffee_cup_heat_rxn(mass_solution, specific_heat, delta_T, density, volume_mL)` → any — Calculate heat of reaction from coffee cup calorimetry.
- `enthalpy_per_mole(q_rxn, moles)` → any — Calculate molar enthalpy change.
- `coffee_cup_delta_H(volume_mL, molarity, specific_heat, delta_T, density)` → any — Complete coffee cup calorimetry: calculate DeltaH per mole of reaction.
- `moles_from_molarity(M, V_L)` → any — Calculate moles from molarity and volume.
- `bomb_calorimeter_heat(C_cal, delta_T)` → any — Calculate heat from bomb calorimeter data.
- `calorimeter_constant(q_known, delta_T)` → any — Calculate calorimeter constant from known reaction.
- `delta_H_from_delta_U(delta_U, delta_n_gas, T)` → any — Convert internal energy change to enthalpy change.
- `delta_U_from_delta_H(delta_H, delta_n_gas, T)` → any — Convert enthalpy change to internal energy change.
- `mixing_final_T(m1, c1, T1, m2, c2, T2)` → any — Calculate final temperature when mixing two substances.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
