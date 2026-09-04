---
id: chem.colligative_properties
layer: 2
title: Colligative Properties of Solutions
source: Ch11.04
dependencies: [solubility, ideal_gas_law]
stability: high
confidence: high
---

## Concept

Colligative properties depend only on the concentration of solute particles, not their identity. Include vapor pressure lowering, boiling point elevation, freezing point depression, and osmotic pressure.

## Core Formulas

### Concentration Units
```
Mole fraction: X_A = n_A / n_total
Molality: m = moles solute / kg solvent
```

### Raoult's Law (Vapor Pressure Lowering)
```
P_solution = X_solvent ¡Á P¡ã_solvent
¦¤P = X_solute ¡Á P¡ã_solvent
```

### Boiling Point Elevation
```
¦¤T_b = K_b ¡Á m ¡Á i

Where:
- K_b = ebullioscopic constant (¡ãC¡¤kg/mol)
- m = molality
- i = van't Hoff factor
```

### Freezing Point Depression
```
¦¤T_f = K_f ¡Á m ¡Á i

Where:
- K_f = cryoscopic constant (¡ãC¡¤kg/mol)
- m = molality
- i = van't Hoff factor
```

### Osmotic Pressure
```
¦° = M ¡Á R ¡Á T ¡Á i

Where:
- ¦° = osmotic pressure (atm)
- M = molarity (mol/L)
- R = 0.08206 L¡¤atm/(mol¡¤K)
- T = temperature (K)
- i = van't Hoff factor
```

## Constants for Common Solvents

| Solvent | K_b (¡ãC/m) | K_f (¡ãC/m) | Normal BP | Normal FP |
|---------|------------|------------|-----------|-----------|
| Water | 0.512 | 1.86 | 100¡ãC | 0¡ãC |
| Benzene | 2.53 | 5.12 | 80.1¡ãC | 5.5¡ãC |
| Ethanol | 1.22 | 1.99 | 78.4¡ãC | -114¡ãC |

## van't Hoff Factor (i)

| Substance Type | i (ideal) | i (actual, dilute) |
|----------------|-----------|-------------------|
| Nonelectrolyte | 1 | 1.0 |
| NaCl | 2 | 1.9 |
| CaCl2 | 3 | 2.7 |
| FeCl3 | 4 | 3.4 |

## Decision Tree

```
Solving colligative property problem?
©À©¤ Vapor pressure?
©¦   ©¸©¤ Use Raoult's Law
©À©¤ Boiling point?
©¦   ©¸©¤ ¦¤T_b = K_b ¡Á m ¡Á i; T_b = T_b¡ã + ¦¤T_b
©À©¤ Freezing point?
©¦   ©¸©¤ ¦¤T_f = K_f ¡Á m ¡Á i; T_f = T_f¡ã - ¦¤T_f
©À©¤ Osmotic pressure?
©¦   ©¸©¤ ¦° = M ¡Á R ¡Á T ¡Á i
©¸©¤ Find molar mass?
    ©¸©¤ Use any colligative property to find moles
```

## Key Constraints
- Nonvolatile solutes only for boiling/freezing point
- Ideal solution behavior assumed
- Electrolytes need van't Hoff factor correction
- Dilute solutions for ideal behavior

## Problem Archetypes
1. Calculate mole fraction and molality
2. Find vapor pressure of solution
3. Calculate boiling/freezing point changes
4. Calculate osmotic pressure
5. Determine molar mass from colligative properties
6. Apply van't Hoff factor for electrolytes

## L3 Tools
- `mole_fraction(components)` ¡ú X values
- `molality(moles, kg_solvent)` ¡ú m
- `vapor_pressure_lowering(X_solvent, P0)` ¡ú P_solution
- `boiling_point_elevation(m, Kb, i)` ¡ú ¦¤T_b
- `freezing_point_depression(m, Kf, i)` ¡ú ¦¤T_f
- `osmotic_pressure(M, T, i)` ¡ú ¦°
- `molar_mass_colligative(¦¤T, K, mass, kg_solvent)` ¡ú M
- `vanthoff_factor(formula, actual=False)` ¡ú i

## L4 Reference

## L5 Examples
See `../L5_examples/buffer/ for worked examples.

## Implementations

- Implementation: `../L3_functions/colligative_properties_tools.py`

## L3 Tool Call Directives

**Source:** `colligative_properties_tools.py`

Colligative Properties Tools - L3 Implementation

### Available functions:
- `vapor_pressure_lowering(X_solvent: float, P0: float)` → float — Calculate vapor pressure of solution using Raoult's Law.
- `vapor_pressure_depression(X_solute: float, P0: float)` → float — Calculate vapor pressure depression.
- `boiling_point_elevation(m: float, Kb: float, i: int)` → float — Calculate boiling point elevation.
- `freezing_point_depression(m: float, Kf: float, i: int)` → float — Calculate freezing point depression.
- `new_boiling_point(m: float, Kb: float, Tb_pure: float, i: int)` → float — Calculate new boiling point of solution.
- `new_freezing_point(m: float, Kf: float, Tf_pure: float, i: int)` → float — Calculate new freezing point of solution.
- `osmotic_pressure(M: float, T: float, i: int)` → float — Calculate osmotic pressure.
- `molar_mass_from_fp_depression(mass_solute: float, mass_solvent_kg: float, delta_T: float, Kf: float, i: int)` → float — Determine molar mass from freezing point depression.
- `molar_mass_from_bp_elevation(mass_solute: float, mass_solvent_kg: float, delta_T: float, Kb: float, i: int)` → float — Determine molar mass from boiling point elevation.
- `molar_mass_from_osmotic_pressure(mass_solute: float, volume_L: float, Pi: float, T: float, i: int)` → float — Determine molar mass from osmotic pressure.
- `vanthoff_factor(formula: str, actual: bool)` → float — Get van't Hoff factor for a compound.
- `get_solvent_constants(solvent: str)` → dict — Get colligative property constants for a solvent.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
