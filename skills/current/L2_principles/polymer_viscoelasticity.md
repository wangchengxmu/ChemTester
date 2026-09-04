---
id: chem.polymer_viscoelasticity
layer: 2
title: Polymer Viscoelasticity
source: Polymer Physics (Steimel), Ch13
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/polymer_physics.py
  - ../L3_functions/polymer_tools.py
---

# Polymer Viscoelasticity

[Source: Polymer Physics (Steimel), Ch13]

## Core Concept

Polymers exhibit both viscous (liquid-like) and elastic (solid-like) behavior. The relative contribution depends on time scale and temperature.

## Key Concepts

### Storage and Loss Moduli

- **Storage modulus (G')**: Elastic response (energy stored)
- **Loss modulus (G'')**: Viscous response (energy dissipated)

$$G^* = G' + iG''$$

### Complex Viscosity

$$\eta^* = \frac{G^*}{i\omega} = \frac{\sqrt{G'^2 + G''^2}}{\omega}$$

## Key Equations

### Maxwell Model (Stress Relaxation)

$$G(t) = G_0 \exp(-t/\tau)$$

where τ is the relaxation time.

### Time-Temperature Superposition

$$a_T = \exp\left[\frac{E_a}{R}\left(\frac{1}{T} - \frac{1}{T_{ref}}\right)\right]$$

### Williams-Landel-Ferry (WLF) Equation

$$\log a_T = \frac{-C_1(T - T_{ref})}{C_2 + (T - T_{ref})}$$

## Viscoelastic Regimes

| Region | Behavior | G' vs G'' |
|--------|----------|-----------|
| Glassy | Solid | G' >> G'' |
| Transition | Both important | G' ≈ G'' |
| Rubbery plateau | Solid-like | G' > G'' |
| Terminal flow | Liquid-like | G'' > G' |

## Problem Types

1. **Calculate relaxation modulus** from Maxwell model
2. **Shift data** using time-temperature superposition
3. **Determine G' and G''** from oscillatory data
4. **Identify viscoelastic regime** from frequency sweep

## L3 Tools

- `../L3_functions/polymer_physics.py` - Viscoelasticity calculations (Maxwell model, WLF shift, complex modulus/viscosity, Arrhenius shift)

## Related Topics

- → `polymer_chain_models.md` for molecular basis
- → `polymer_properties.md` for Tg relationship
