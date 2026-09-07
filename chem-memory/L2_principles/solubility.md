---
id: chem.solubility
layer: 2
title: Solubility and Henry's Law
source: Ch11.03
dependencies: [dissolution_process, gas_pressure]
stability: high
confidence: high
---

## Concept

Solubility is the maximum amount of solute that can dissolve in a solvent at equilibrium. Depends on temperature, pressure, and molecular interactions.

## Core Formulas

### Henry's Law (Gas Solubility)
```
C = kH ¡Á P

Where:
- C = concentration of dissolved gas (M)
- kH = Henry's law constant (M/atm)
- P = partial pressure of gas (atm)
```

### Temperature Effects
```
For most solids: solubility increases with temperature
For gases: solubility decreases with temperature
```

## Decision Tree

```
Predicting solubility?
©À©¤ Gas in liquid?
©¦   ©À©¤ Use Henry's Law
©¦   ©¸©¤ Higher pressure ¡ú higher solubility
©À©¤ Solid in liquid?
©¦   ©À©¤ Check "like dissolves like"
©¦   ©¸©¤ Temperature effect varies
©¸©¤ Liquid in liquid?
    ©¸©¤ Check polarity similarity
```

## Solubility Rules (Ionic Compounds)

| Rule | Soluble | Exceptions |
|------|---------|------------|
| Group 1 ions | Always soluble | None |
| NH4? | Always soluble | None |
| NO3? | Always soluble | None |
| Cl? | Mostly soluble | Ag?, Pb2?, Hg?2? |
| SO42? | Mostly soluble | Ba2?, Pb2?, Ca2? |
| OH? | Mostly insoluble | Group 1, NH4?, Ba2? |
| CO32?, PO43? | Mostly insoluble | Group 1, NH4? |

## Key Constraints
- Saturated = at equilibrium with undissolved solute
- Supersaturated = metastable, exceeds solubility
- Henry's law applies to dilute solutions only

## Problem Archetypes
1. Predict if compound is soluble
2. Calculate gas solubility with Henry's Law
3. Compare solubility at different temperatures
4. Determine if solution is saturated

## L3 Tool Call Directives

When solving solubility problems, ALWAYS use these tools. Do NOT calculate manually.

### henrys_law(kH, P) → float
- Returns dissolved gas concentration (M) from Henry's law constant and pressure
- kH is the Henry's law constant — check units! Common formats:
  - M/atm (direct concentration): use `C = kH * P`
  - atm·L/mol (inverse form): use `C = P / kH`
- If kH is not given, use `get_henry_constant(gas, temperature)` to look it up

### henrys_law_gas_volume(moles_gas, T=298.15, P=1.0) → float
- Converts moles of gas to volume at specified T and P
- **CRITICAL:** Use the ACTUAL temperature of the gas, NOT 298.15 by default
- If the problem states the gas is at 20°C, pass `T=293.15` NOT `T=298.15`
- If the problem says "at STP" (0°C), use `T=273.15, P=1.0`
- **Common error:** Using default T=298 when the problem specifies a different temperature

### henrys_law_pressure(kH, C) → float
- Inverse of Henry's law: find partial pressure from dissolved concentration

### Other tools:
- `predict_ionic_solubility(cation, anion)` → dict with prediction
- `saturation_status(mass_solute, volume_L, solubility_g_per_100mL)` → str
- `get_henry_constant(gas, temperature=25)` → float

### Common caller errors to avoid:
1. ❌ Using default T=298.15 when problem states a different temperature → Read problem carefully
2. ❌ Confusing kH units (M/atm vs atm·L/mol) → Check which form the constant uses
3. ❌ Using STP volume (22.4 L/mol) for non-STP conditions → Use correct T and P

## L4 Reference

## L5 Examples
See `../L5_examples/buffer/ for worked examples.

## Implementations

- Implementation: `../L3_functions/solubility_tools.py`

---

**Source:** `solubility_equilibria_tools.py`

Ksp calculations, molar solubility for different salt stoichiometries, ion product Q, precipitation prediction, common ion effect.

### Available functions:
- `Ksp_expression(cation, cation_coeff, anion, anion_coeff)` → str — Generate Ksp expression string
- `molar_solubility_11(Ksp)` → float — s = √Ksp (1:1 salt MX)
- `molar_solubility_12(Ksp)` → float — s = ∛(Ksp/4) (1:2 salt MX₂)
- `molar_solubility_21(Ksp)` → float — s = ∛(Ksp/4) (2:1 salt M₂X)
- `Ksp_from_solubility_11(s)` → float — Ksp = s²
- `Ksp_from_solubility_12(s)` → float — Ksp = 4s³
- `ion_product(cation_conc, anion_conc, cation_coeff=1, anion_coeff=1)` → float — Q = [cation]^a[anion]^b
- `predict_precipitation(Q, Ksp)` → str — 'unsaturated'/'precipitation occurs'/'saturated'
- `solubility_common_ion(Ksp, common_ion_conc, salt_type='11')` → float — Reduced solubility with common ion
- `precipitate_amount(initial_conc, final_conc, volume, molar_mass)` → float — Mass of precipitate (g)

### Common errors:
- ❌ Using wrong salt type (11/12/21) — check stoichiometry from formula
- ❌ Confusing Q vs Ksp comparison direction — Q > Ksp means precipitation
