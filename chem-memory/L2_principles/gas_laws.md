---
id: chem.gas_laws
layer: 2
title: The Gas Laws (Boyle, Charles, Gay-Lussac, Avogadro)
source: Ch08.02
dependencies: [gas_pressure]
stability: high
confidence: high
---

## Concept

Gas laws describe relationships between pressure, volume, temperature, and amount of gas.

## Core Formulas

### Boyle's Law (constant T, n)
```
P?V? = P?V?
P ¡Ø 1/V
```

### Charles's Law (constant P, n)
```
V?/T? = V?/T?
V ¡Ø T (temperature in Kelvin)
```

### Gay-Lussac's/Amontons's Law (constant V, n)
```
P?/T? = P?/T?
P ¡Ø T (temperature in Kelvin)
```

### Avogadro's Law (constant P, T)
```
V?/n? = V?/n?
V ¡Ø n
```

### Combined Gas Law
```
P?V?/T? = P?V?/T?
```

## Decision Tree

```
Which variables are constant?
©À©¤ T and n constant ¡ú Boyle's Law (P?V? = P?V?)
©À©¤ P and n constant ¡ú Charles's Law (V?/T? = V?/T?)
©À©¤ V and n constant ¡ú Gay-Lussac's (P?/T? = P?/T?)
©À©¤ P and T constant ¡ú Avogadro's Law (V?/n? = V?/n?)
©¸©¤ Only n constant ¡ú Combined Gas Law (P?V?/T? = P?V?/T?)
```

## Key Constraints
- Temperature MUST be in Kelvin
- Pressure units must be consistent
- Volume units must be consistent

## Problem Archetypes
1. Find new pressure, volume, or temperature after change
2. Compare gas properties before/after change
3. Use combined gas law for multi-variable changes

## L3 Tool Call Directives

When solving gas law problems, ALWAYS use these Python tools. Do NOT calculate manually.

### combined_gas_law(P1, V1, T1, P2, V2, T2, n=None, R=0.08206) → float
- Pass exactly 5 of {P1, V1, T1, P2, V2, T2}; the missing one is solved
- **CRITICAL:** If moles (n) is known from the problem, ALWAYS pass `n` parameter
- Without `n`, the tool assumes constant moles (P1V1/T1 = P2V2/T2)
- With `n`, it uses ideal gas law: PV = nRT for the missing variable
- If n=1.0 mol is stated, pass `n=1.0` explicitly — do NOT omit it
- Temperatures MUST be in Kelvin (use `celsius_to_kelvin()` first)

### Other gas law functions (pass 3 of 4, missing one is solved):
- `boyles_law(P1, V1, P2, V2)` — constant T, n
- `charles_law(V1, T1, V2, T2)` — constant P, n
- `gay_lussacs_law(P1, T1, P2, T2)` — constant V, n
- `avogadros_law(V1, n1, V2, n2)` — constant P, T

### Unit conversion
- `celsius_to_kelvin(celsius)` — ALWAYS convert °C to K before calling gas law functions
- `kelvin_to_celsius(kelvin)` — convert back if answer needed in °C

### Common caller errors to avoid:
1. ❌ Calling combined_gas_law without n when moles are given → Use n parameter
2. ❌ Using °C instead of K → Always convert first
3. ❌ Mixing pressure units → Use consistent units (all atm or all kPa)

## L4 Reference

## L5 Examples
See `../L5_examples/phase_diagrams/ for worked examples.

## Implementations

- Implementation: `../L3_functions/gas_laws_tools.py`
