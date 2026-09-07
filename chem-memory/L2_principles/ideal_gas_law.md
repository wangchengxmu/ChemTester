---
id: chem.ideal_gas_law
layer: 2
title: The Ideal Gas Law and Applications
source: Ch08.03-08.04
dependencies: [gas_laws, stoichiometric_conversion]
stability: high
confidence: high
---

## Concept

The ideal gas law relates pressure, volume, temperature, and amount of gas in one equation.

## Core Formulas

### Ideal Gas Law
```
PV = nRT

Where:
- P = pressure (atm)
- V = volume (L)
- n = moles of gas
- R = 0.08206 L¡¤atm/(mol¡¤K)
- T = temperature (K)
```

### Gas Constant Values
```
R = 0.08206 L¡¤atm/(mol¡¤K)
R = 8.314 J/(mol¡¤K) = 8.314 kPa¡¤L/(mol¡¤K)
R = 62.36 L¡¤torr/(mol¡¤K)
```

### Standard Molar Volume
```
At STP (273.15 K, 1 atm):
Vm = 22.4 L/mol

At SATP (298.15 K, 1 bar):
Vm = 24.8 L/mol
```

### Gas Density and Molar Mass
```
Density: d = PM/RT
Molar Mass: M = dRT/P
```

## Decision Tree

```
Using ideal gas law?
©À©¤ Know P, V, T ¡ú n = PV/RT
©À©¤ Know P, n, T ¡ú V = nRT/P
©À©¤ Know V, n, T ¡ú P = nRT/V
©À©¤ Know P, V, n ¡ú T = PV/nR
©¸©¤ Find density ¡ú d = PM/RT

Given gas at STP?
©¸©¤ Use Vm = 22.4 L/mol for quick calculation
```

## Key Constraints
- Temperature must be in Kelvin
- Units must match R value chosen
- Ideal behavior assumed (low P, high T)

## Problem Archetypes
1. Calculate any variable from others (P, V, n, T)
2. Find density or molar mass from gas data
3. Stoichiometry involving gases
4. Compare gases under different conditions

## L3 Tools
- `ideal_gas_law(P, V, n, T, R)` ¡ú missing variable
- `molar_volume(conditions)` ¡ú Vm
- `gas_density(P, M, T)` ¡ú density
- `molar_mass_from_gas(d, P, T)` ¡ú M
- `gas_stoichiometry()` ¡ú volume/mole conversions

## L4 Reference

## L5 Examples
See `../L5_examples/phase_diagrams/ for worked examples.

## Implementations

## L3 Tool Call Directive

When solving gas law and gas stoichiometry problems, call the appropriate L3 function:

**ideal_gas_law** (`L3_functions/ideal_gas_law_tools.py`):
- Use when: Solve PV=nRT for any one variable given the other three.
- Parameters: `P=None, V=None, n=None, T=None, R=None` (omit or set to None the unknown)
- Units: P in atm, V in L, T in K, R=0.08206 (default)

**gas_stoichiometry** (`L3_functions/ideal_gas_law_tools.py`):
- Use when: Convert gas volume to moles (or vice versa) using stoichiometric coefficients for gas-phase reactions.
- Parameters: `gas_volume`, `gas_moles_coeff`, `target_coeff` (stoichiometric coefficient of gas and target)

**moles_at_stp** / **volume_at_stp** (`L3_functions/ideal_gas_law_tools.py`):
- Use when: Convert volume to moles (or vice versa) at standard temperature and pressure.
- Parameters: `V` (L) or `n` (mol)

**gas_density** (`L3_functions/ideal_gas_law_tools.py`):
- Use when: Calculate gas density from molar mass and conditions.
- Parameters: `P`, `M` (molar mass), `T`

**molar_mass_from_gas** (`L3_functions/ideal_gas_law_tools.py`):
- Use when: Determine molar mass of a gas from density, P, and T.
- Parameters: `d`, `P`, `T`

**Critical notes:**
- Always convert temperatures to Kelvin (K = °C + 273.15).
- For gas stoichiometry problems: first use ideal_gas_law to get moles, then use mole ratio, then convert back to volume/mass as needed.
- Combine with `limiting_reactant_tools.py` for limiting reagent problems involving gases.

- Implementation: `../L3_functions/ideal_gas_law_tools.py`

## L3 Tool Call Directives

**Source:** `ideal_gas_law_tools.py`

Core ideal gas law calculations: PV=nRT, density, molar mass, and gas stoichiometry.

### Available functions:
- `ideal_gas_law(P, V, n, T, R=0.08206)` → float — Solve PV=nRT; pass None for unknown
- `molar_volume(T=273.15, P=1.0, R=0.08206)` → float — Calculate V_m = RT/P in L/mol
- `gas_density(P, M, T, R=0.08206)` → float — Calculate d = PM/RT in g/L
- `molar_mass_from_gas(d, P, T, R=0.08206)` → float — Calculate M = dRT/P in g/mol
- `moles_at_stp(V)` → float — Convert volume (L) to moles at STP using 22.4 L/mol
- `volume_at_stp(n)` → float — Convert moles to volume (L) at STP using 22.4 L/mol
- `gas_stoichiometry(gas_volume, gas_moles_coeff, product_moles_coeff, molar_mass=None, conditions='STP')` → dict — Returns {'product_moles', 'product_mass'}

### Common errors:
- ❌ Using temperature in °C instead of Kelvin (MUST convert first)
- ❌ Using wrong R constant for pressure units (atm → 0.08206, kPa → 8.314, torr → 62.36)
- ❌ Confusing STP (0°C, 22.4 L/mol) with SATP (25°C, 24.8 L/mol)
