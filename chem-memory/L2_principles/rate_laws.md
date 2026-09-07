---
id: chem.rate_laws
layer: 2
title: Rate Laws and Reaction Orders
source: Ch12.03
dependencies: [reaction_rates]
stability: high
confidence: high
---

## Concept

Rate laws describe how reaction rate depends on reactant concentrations. Rate laws must be determined experimentally and cannot be predicted from stoichiometry.

## Core Formulas

### Differential Rate Law
```
rate = k[A]^m[B]^n

Where:
- k = rate constant (temperature-dependent)
- m = order with respect to A
- n = order with respect to B
- Overall order = m + n
```

### Rate Constant Units

| Overall Order | Units of k |
|---------------|------------|
| 0 | M¡¤s?1 |
| 1 | s?1 |
| 2 | M?1¡¤s?1 |
| 3 | M?2¡¤s?1 |

General: L^(x-1)¡¤mol^(1-x)¡¤s?1 for order x

## Method of Initial Rates

```
To find order m in A:
1. Keep [B] constant
2. Compare trials where [A] changes
3. rate?/rate? = ([A]?/[A]?)^m
4. Solve for m

Then find k from: k = rate/([A]^m[B]^n)
```

## Decision Tree

```
Working with rate laws?
©À©¤ Writing rate law?
©¦   ©¸©¤ rate = k[A]^m[B]^n (orders from experiment)
©À©¤ Finding orders?
©¦   ©¸©¤ Use method of initial rates
©À©¤ Finding k?
©¦   ©¸©¤ k = rate/([A]^m[B]^n)
©¸©¤ Finding rate?
    ©¸©¤ rate = k[A]^m[B]^n
```

## Key Constraints
- Orders are NOT stoichiometric coefficients
- Orders can be 0, 1, 2, fractions, or negative
- k is independent of concentration, depends on temperature
- Rate law determined by experiment only

## Problem Archetypes
1. Write rate law given orders
2. Determine orders from initial rate data
3. Calculate rate constant with correct units
4. Calculate rate at given concentrations

## L3 Tools
- `rate_law(orders, concentrations, k)` ¡ú rate
- `determine_order(rate_data)` ¡ú orders
- `rate_constant(rate, concentrations, orders)` ¡ú k
- `rate_constant_units(overall_order)` ¡ú units string

## L4 Reference

## L5 Examples
See `../L5_examples/kinetics_examples.md for worked examples.

## Implementations
- Implementation: `../L3_functions/rate_law_solver.py`

- Implementation: `../L3_functions/rate_law_tools.py`
