---
id: chem.non_ideal_gases
layer: 2
title: Non-Ideal Gas Behavior and van der Waals Equation
source: OpenStax Chemistry 2e, section 9.6
dependencies: [ideal_gas_law]
stability: high
confidence: high
---

## Equation Of State

For amount n, total volume V and temperature T:

```
Z = PV/(nRT)
(P + n^2*a/V^2)*(V - n*b) = nRT
P = nRT/(V - n*b) - n^2*a/V^2
```

At sufficiently low density the correction terms become small. Z below one
indicates net attractive deviations; Z above one indicates net repulsive
deviations. Van der Waals is an approximate model, not a universal high-pressure
replacement for experimental data or a validated equation of state.

## van der Waals Constants

These values use a in L^2*atm/mol^2 and b in L/mol.

| Gas | a | b |
| --- | ---: | ---: |
| N2 | 1.39 | 0.0391 |
| O2 | 1.36 | 0.0318 |
| CO2 | 3.59 | 0.0427 |
| H2O | 5.46 | 0.0305 |
| He | 0.0342 | 0.0237 |

Source: [OpenStax Chemistry 2e, Table 9.3](https://openstax.org/books/chemistry-2e/pages/9-6-non-ideal-gas-behavior).
Use the supplied parameter set when one is specified. Otherwise identify the
reference and units of any adopted constants; do not silently treat them as
given measurements.

## Fixed-Volume Enthalpy Change

For a closed system with fixed n and V and only pressure-volume work,
Delta U = Q_V. From H = U + PV:

```
Delta H = Q_V + V*(P2 - P1)
Delta H = Q_V + n*R*V*(T2 - T1)/(V - n*b)
```

The attraction contribution cancels only when n, V and a are unchanged.
The covolume factor does not cancel. Temperature-dependent parameters or
additional work modes require revisiting these assumptions.

## Units And Physical Guards

- Use absolute temperature and pressure, with positive n and V.
- Require V > n*b. Reject a clamped result outside that domain.
- R = 0.082057 L*atm/(mol*K) is compatible with the table above.
- For R = 8.31446 L*kPa/(mol*K), convert a from atm to kPa first.
- 1 L*atm = 101.325 J; 1 L*kPa = 1 J. Convert heat and PV to the same
  energy units exactly once.
- Volume solutions may have multiple roots; select a stable physical phase
  consistent with the problem, not merely the first numerical root.

## Computational Support

Search the curated catalog for the required operation and verify the advertised
signature before calling. The source module `L3_functions/non_ideal_gas_tools.py`
contains pressure, volume and constant-lookup functions, but a source-file link
does not mean that the function is enabled in the active tool allowlist.
Check convergence, units and equation residuals before using any result.
