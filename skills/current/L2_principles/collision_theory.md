---
id: chem.collision_theory
layer: 2
title: Collision Theory and the Arrhenius Equation
source: Ch12.05
dependencies: [kinetic_theory_effusion]
stability: high
confidence: high
---

## Concept

Collision theory explains reaction rates in terms of molecular collisions. Reactions occur when molecules collide with correct orientation and sufficient energy (¡Ý Ea).

## Core Formulas

### Arrhenius Equation
```
k = A ¡Á e^(-Ea/RT)

Where:
- k = rate constant
- A = frequency factor (collision freq ¡Á orientation factor)
- Ea = activation energy (J/mol)
- R = 8.314 J/(mol¡¤K)
- T = temperature (K)
```

### Linear Form
```
ln k = -Ea/R ¡Á (1/T) + ln A

Plot ln k vs 1/T ¡ú slope = -Ea/R
```

### Two-Point Form
```
ln(k?/k?) = Ea/R ¡Á (1/T? - 1/T?)

Or rearranged:
Ea = -R ¡Á (ln k? - ln k?)/(1/T? - 1/T?)
```

## Decision Tree

```
Working with Arrhenius equation?
©À©¤ Finding k at different T?
©¦   ©¸©¤ k? = k? ¡Á e^[(Ea/R)(1/T? - 1/T?)]
©À©¤ Finding Ea from k vs T data?
©¦   ©À©¤ Two temperatures ¡ú two-point form
©¦   ©¸©¤ Multiple temperatures ¡ú plot ln k vs 1/T
©À©¤ Finding A?
©¦   ©¸©¤ A = k ¡Á e^(Ea/RT)
©¸©¤ Explaining rate changes?
    ©¸©¤ Higher T ¡ú more molecules with E > Ea
```

## Key Constraints
- Ea is always positive for elementary reactions
- A typically ranges from 10? to 1013 s?1 for unimolecular reactions
- Rate approximately doubles for every 10 K increase in temperature

## Temperature Dependence

```
At higher temperature:
- Greater fraction of molecules have E > Ea
- More effective collisions per unit time
- Larger k ¡ú faster reaction
```

## Problem Archetypes
1. Calculate k at different temperature
2. Calculate activation energy from rate constants
3. Calculate frequency factor A
4. Compare rates at different temperatures
5. Determine Ea from graphical analysis

## L3 Tools
- `arrhenius_k(A, Ea, T)` ¡ú k
- `activation_energy(k1, T1, k2, T2)` ¡ú Ea
- `frequency_factor(k, Ea, T)` ¡ú A
- `rate_at_temperature(k1, T1, Ea, T2)` ¡ú k2
- `temperature_for_rate(k, A, Ea)` ¡ú T

## L4 Reference

## L5 Examples
See `../L5_examples/kinetics_examples.md for worked examples.

## Implementations
- Implementation: `../L3_functions/arrhenius_tools.py`

- Implementation: `../L3_functions/gas_phase_dynamics_tools.py`

## L3 Tool Call Directives


**Source:** `arrhenius_tools.py`

L3 tool module for arrhenius tools

### Available functions:
- `arrhenius_k(A: float, Ea: float, T: float)` → float — Calculate rate constant using Arrhenius equation.
- `activation_energy(k1: float, T1: float, k2: float, T2: float)` → float — Calculate activation energy from rate constants at two temperatures.
- `frequency_factor(k: float, Ea: float, T: float)` → float — Calculate frequency factor from rate constant.
- `rate_at_temperature(k1: float, T1: float, Ea: float, T2: float)` → float — Calculate rate constant at a different temperature.
- `temperature_for_rate(k_target: float, A: float, Ea: float)` → float — Calculate temperature needed for a specific rate constant.
- `compare_rates(Ea: float, T1: float, T2: float)` → float — Compare rates at two temperatures.
- `arrhenius_plot_slope(Ea: float)` → float — Get slope for Arrhenius plot (ln k vs 1/T).
- `activation_energy_from_slope(slope: float)` → float — Calculate activation energy from Arrhenius plot slope.
- `fraction_with_energy(Ea: float, T: float)` → float — Calculate fraction of molecules with energy >= Ea.
- `catalyzed_rate_constant(k_uncat: float, Ea_uncat: float, Ea_cat: float, T: float)` → float — Calculate catalyzed rate constant.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
