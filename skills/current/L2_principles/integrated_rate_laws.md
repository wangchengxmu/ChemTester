---
id: chem.integrated_rate_laws
layer: 2
title: Integrated Rate Laws and Half-Life
source: Ch12.04
dependencies: [rate_laws]
stability: high
confidence: high
---

## Concept

Integrated rate laws relate concentration to time, allowing calculation of concentrations at specific times or time to reach certain concentrations.

## Core Formulas

### First-Order (rate = k[A])
```
[A]t = [A]? Â¡Ã e^(-kt)
ln[A]t = -kt + ln[A]?
t?/? = 0.693/k
```

### Second-Order (rate = k[A]2)
```
1/[A]t = kt + 1/[A]?
t?/? = 1/(k[A]?)
```

### Zero-Order (rate = k)
```
[A]t = -kt + [A]?
t?/? = [A]?/(2k)
```

## Summary Table

| Order | Rate Law | Integrated | Half-life | Linear Plot |
|-------|----------|------------|-----------|-------------|
| 0 | rate = k | [A]t = -kt + [A]? | [A]?/(2k) | [A] vs t |
| 1 | rate = k[A] | ln[A]t = -kt + ln[A]? | 0.693/k | ln[A] vs t |
| 2 | rate = k[A]2 | 1/[A]t = kt + 1/[A]? | 1/(k[A]?) | 1/[A] vs t |

## Decision Tree

```
Using integrated rate laws?
Â©Ã€Â©Â¤ Know order?
Â©Â¦   Â©Ã€Â©Â¤ First Â¡Ãº ln[A]t = -kt + ln[A]?
Â©Â¦   Â©Ã€Â©Â¤ Second Â¡Ãº 1/[A]t = kt + 1/[A]?
Â©Â¦   Â©Â¸Â©Â¤ Zero Â¡Ãº [A]t = -kt + [A]?
Â©Ã€Â©Â¤ Finding half-life?
Â©Â¦   Â©Ã€Â©Â¤ First Â¡Ãº t?/? = 0.693/k
Â©Â¦   Â©Ã€Â©Â¤ Second Â¡Ãº t?/? = 1/(k[A]?)
Â©Â¦   Â©Â¸Â©Â¤ Zero Â¡Ãº t?/? = [A]?/(2k)
Â©Â¸Â©Â¤ Identifying order from data?
    Â©Â¸Â©Â¤ Plot [A], ln[A], 1/[A] vs t
    Â©Â¸Â©Â¤ Linear plot indicates order
```

## Key Constraints
- First-order half-life independent of concentration
- Second/zero-order half-life depends on initial concentration
- Order must be known before applying integrated law

## Problem Archetypes
1. Calculate concentration at time t
2. Calculate time to reach certain concentration
3. Calculate half-life
4. Determine reaction order from concentration/time data
5. Calculate rate constant from half-life

## L3 Tools
- `first_order_concentration(C0, k, t)` Â¡Ãº Ct
- `second_order_concentration(C0, k, t)` Â¡Ãº Ct
- `zero_order_concentration(C0, k, t)` Â¡Ãº Ct
- `half_life(order, k, C0)` Â¡Ãº t_half
- `time_to_concentration(order, C0, Ct, k)` Â¡Ãº t
- `identify_order_from_data(time_data, conc_data)` Â¡Ãº order

## L4 Reference

## L5 Examples
See `../L5_examples/kinetics_examples.md for worked examples.

## Implementations

- Implementation: `../L3_functions/integrated_rate_law_tools.py`

## L3 Tool Call Directives

**Source:** ate_law_solver.py
Integrated rate law solvers, half-life, rate constant determination, complex mechanisms.

### Available functions:
- half_life_first_order(k: float) ¡ú float ¡ª t? = ln(2)/k
- half_life_second_order(k: float, initial_conc: float) ¡ú float ¡ª t? = 1/(k[A]?)
- half_life_zero_order(k: float, initial_conc: float) ¡ú float ¡ª t? = [A]?/(2k)
- integrated_zero_order(k, A0, t) ¡ú ndarray ¡ª [A] = [A]? - kt
- integrated_first_order(k, A0, t) ¡ú ndarray ¡ª [A] = [A]?¡¤e^(-kt)
- integrated_second_order_one_reactant(k, A0, t) ¡ú ndarray ¡ª 1/[A] = 1/[A]? + kt
- integrated_second_order_equal(k, A0, B0, t) ¡ú ndarray ¡ª Requires [A]? = [B]?
- integrated_second_order_unequal(k, A0, B0, t) ¡ú Tuple[ndarray, ndarray] ¡ª ([A], [B]) for [A]? ¡Ù [B]?
- determine_rate_constant_zero_order(t, A) ¡ú Tuple[float, float] ¡ª (k, R2)
- determine_rate_constant_first_order(t, A) ¡ú Tuple[float, float] ¡ª (k, R2)
- determine_rate_constant_second_order(t, A) ¡ú Tuple[float, float] ¡ª (k, R2)
- determine_order_and_constant(t, A) ¡ú Dict ¡ª Auto-detects best order (0/1/2)
- 	ime_to_fraction_zero_order(k, A0, fraction) ¡ú float ¡ª Time to reach fraction
- 	ime_to_fraction_first_order(k, fraction) ¡ú float ¡ª Time to reach fraction
- 	ime_to_fraction_second_order(k, A0, fraction) ¡ú float ¡ª Time to reach fraction
- consecutive_first_order(k1, k2, A0, t) ¡ú Tuple[ndarray, ndarray, ndarray] ¡ª A¡úB¡úC concentrations
- parallel_first_order(k1, k2, A0, t) ¡ú Tuple[ndarray, ndarray, ndarray] ¡ª Parallel A¡úB/C
- eversible_first_order(kf, kr, A0, B0, t) ¡ú Tuple[ndarray, ndarray] ¡ª A?B concentrations

### Common errors:
- ? Using integrated_second_order_equal when [A]? ¡Ù [B]? (raises ValueError)
- ? Confusing t parameter units (must match k units)

---

## L3 Tool Call Directives

**Source:** integrated_rate_law_tools.py
Integrated rate laws (0th, 1st, 2nd order), half-life, order identification from data.

### Available functions:
- irst_order_concentration(C0, k, t) ¡ú float ¡ª [A]t = C?e^(?kt)
- irst_order_time(C0, Ct, k) ¡ú float ¡ª t = ln(C?/Ct)/k
- irst_order_half_life(k) ¡ú float ¡ª t? = 0.693/k
- second_order_concentration(C0, k, t) ¡ú float ¡ª 1/[A]t = 1/C? + kt
- second_order_time(C0, Ct, k) ¡ú float ¡ª t = (1/Ct ? 1/C?)/k
- second_order_half_life(C0, k) ¡ú float ¡ª t? = 1/(kC?)
- zero_order_concentration(C0, k, t) ¡ú float ¡ª [A]t = C? ? kt (floors at 0)
- zero_order_time(C0, Ct, k) ¡ú float ¡ª t = (C? ? Ct)/k
- zero_order_half_life(C0, k) ¡ú float ¡ª t? = C?/(2k)
- half_life(order, k, C0) ¡ú float ¡ª General half-life for any order (C0 needed for 0th, 2nd)
- identify_order_from_data(times, concentrations) ¡ú tuple[int, float] ¡ª Auto-detect order via linear regression

### Common errors:
- ? Forgetting C0 is required for 2nd-order and 0th-order half-life but not 1st-order
- ? Wrong k units: 1st=time?1, 2nd=M?1¡¤time?1, 0th=M¡¤time?1
