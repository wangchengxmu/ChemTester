---
id: chem.gas_pressure
layer: 2
title: Gas Pressure and Measurement
source: Ch08.01-08.02
dependencies: []
stability: high
confidence: high
---

## Concept

Pressure is force per unit area. Gas pressure results from molecular collisions with container walls.

## Core Formulas

### Pressure Definition
```
P = F/A
```

### Hydrostatic Pressure
```
p = h¦Ñg

Where:
- h = height of fluid column (m)
- ¦Ñ = density of fluid (kg/m3)
- g = acceleration due to gravity (9.81 m/s2)
```

### Pressure Unit Conversions
```
1 atm = 101,325 Pa = 760 torr = 760 mm Hg
1 atm = 1.01325 bar = 14.7 psi
1 torr ¡Ö 1 mm Hg
```

## Decision Tree

```
Need to convert pressure units?
©À©¤ Identify given unit and target unit
©À©¤ Use conversion factors from table
©¸©¤ Verify with dimensional analysis

Reading a manometer?
©À©¤ Open-end: P_gas = P_atm + h (if gas higher)
©À©¤ Open-end: P_gas = P_atm - h (if gas lower)
©¸©¤ Closed-end: P_gas = h (directly)
```

## Key Constants
- Standard pressure: 1 atm = 101.325 kPa
- Mercury density: 13.6 g/cm3
- Water density: 1.00 g/cm3

## Problem Archetypes
1. Convert between pressure units
2. Calculate hydrostatic pressure from column height
3. Determine gas pressure from manometer reading

## L3 Tools
- `convert_pressure(value, from_unit, to_unit)` ¡ú converted value
- `hydrostatic_pressure(height, density, g)` ¡ú pressure
- `manometer_pressure(type, h, P_atm)` ¡ú gas pressure

## L4 Reference

## L5 Examples
See `../L5_examples/phase_diagrams/ for worked examples.

## Implementations

- Implementation: `../L3_functions/gas_pressure_tools.py`

## L3 Tool Call Directives

**Source:** `gas_pressure_tools.py`
Gas pressure unit conversion, manometer readings, and hydrostatic pressure calculations.

### Available functions:
- `convert_pressure(value, from_unit, to_unit)` → float — Convert between Pa, kPa, atm, bar, torr, mmHg, psi, inHg
- `hydrostatic_pressure(height, density, g)` → float — Calculate P = ρgh in pascals
- `manometer_pressure(manometer_type, height, P_atm, density)` → float — Calculate gas pressure from manometer ('closed'/'open_higher'/'open_lower')
- `standard_pressure(unit)` → float — Get 1 atm in specified unit
- `pressure_at_depth(depth, P_surface, density, g)` → float — Calculate pressure at depth in fluid

### Common errors:
- ❌ Confusing open-end manometer cases (gas > atm → add ρgh; gas < atm → subtract)
- ❌ Using water density (1000) when mercury (13600) is intended
