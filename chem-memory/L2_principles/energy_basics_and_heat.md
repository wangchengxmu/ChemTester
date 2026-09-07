---
id: chem.energy_basics
layer: 2
title: Energy Basics and Heat Transfer
source: LibreTexts Chemistry 2e Ch05.01
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Energy Basics and Heat Transfer

## Problem type
Calculate heat transfer, work, or energy changes in physical and chemical processes.

## Decision tree

1. **What is asked?**
   - Calculate heat (q) → Use specific heat formula
   - Calculate temperature change → Rearrange q = mcΔT
   - Convert units → J, cal, Cal conversions
   - Work calculation → w = -PΔV

2. **Type of process?**
   - Endothermic → q > 0 (absorbs heat)
   - Exothermic → q < 0 (releases heat)

3. **Phase involved?**
   - Temperature change → Use specific heat
   - Phase change → Use enthalpy of fusion/vaporization

## Core formulas

### Heat transfer
```
q = m × c × ΔT
where:
  q = heat (J)
  m = mass (g)
  c = specific heat capacity (J/g·°C)
  ΔT = T_final - T_initial (°C or K)
```

### Heat capacity
```
C = q / ΔT  (J/°C or J/K)
C = m × c   (total heat capacity)
```

### Work (pressure-volume)
```
w = -P × ΔV  (J)
where:
  P = pressure (Pa or atm)
  ΔV = V_final - V_initial
  Negative sign: work BY system is negative
```

### Unit conversions
```
1 cal = 4.184 J (exact)
1 Cal = 1 kcal = 4184 J
1 L·atm = 101.325 J
```

## Key constants

| Substance | Specific Heat (J/g·°C) |
|-----------|----------------------|
| Water (l) | 4.184 |
| Water (s) | 2.09 |
| Water (g) | 2.01 |
| Ice | 2.03 |
| Aluminum | 0.897 |
| Iron | 0.449 |
| Copper | 0.385 |
| Gold | 0.129 |

## Constraints
- q > 0 for endothermic (heat absorbed)
- q < 0 for exothermic (heat released)
- ΔT = T_final - T_initial (can be negative)
- Use absolute temperature (K) for gas calculations

## Common patterns
- Metal cooling in water → heat lost by metal = heat gained by water
- Temperature change → q = mcΔT
- Unit conversion → apply conversion factors

## Links

### L3 Implementation
- `../L3_functions/energy_basics_tools.py` (TODO)

### L4 Reference

### L5 Examples
- `../L5_examples/thermal_analysis/ (TODO)

## Source trace
- `../sources/ingestion/source-thermochemistry-stepwise.md` section 5.01
## Data Reference
- L3 Tool: 	hermodynamic_lookup_tools.lookup_thermodynamic_data(formula) — ΔHf°, ΔGf°, S°, Cp for 58+ compounds
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dH(reactants, products) — reaction enthalpy from formation data
- L3 Tool: 	hermodynamic_lookup_tools.calculate_reaction_dG(reactants, products) — reaction Gibbs energy
- L4 Data: L4_reference/thermodynamic_data.csv — Full table with NIST/CRC values
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST-JANAF, NIST WebBook

---

## L3 Tool Call Directives

**Source:** energy_basics_tools.py
Heat transfer (q=mcΔT), unit conversions (J/cal/Cal), PV work, heat capacity.

### Available functions:
- heat_transfer(mass, specific_heat, delta_T) → float — q = mcΔT (J); +absorbed, −released
- inal_temperature(initial_T, heat, mass, specific_heat) → float — T_f from heat addition
- specific_heat_from_heat(mass, heat, delta_T) → float — c = q/(mΔT)
- joules_to_calories(joules) → float — 1 cal = 4.184 J
- calories_to_joules(calories) → float
- joules_to_nutritional_cal(joules) → float — 1 Cal = 1 kcal = 4184 J
- 
utritional_cal_to_joules(Cal) → float
- pressure_volume_work(pressure_atm, delta_V_L) → float — w = −PΔV (J)
- heat_capacity(mass, specific_heat) → float — C = mc (J/°C)
- heat_from_heat_capacity(C, delta_T) → float — q = CΔT

Also see SPECIFIC_HEATS dict: water_liquid=4.184, aluminum=0.897, iron=0.449, copper=0.385, etc.

### Common errors:
- ❌ Confusing Cal (nutritional, kcal) with cal (small calorie) — 1000× difference
- ❌ Wrong sign for PV work: expansion (ΔV>0) gives w<0 (system does work)
