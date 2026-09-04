---
id: chem.colloids
layer: 2
title: Colloids and Dispersions
source: Ch11.05
dependencies: []
stability: high
confidence: high
---

## Concept

Colloids are mixtures with particle sizes between solutions and suspensions (1-1000 nm). They exhibit unique properties like the Tyndall effect.

## Classification by Particle Size

| Type | Particle Size | Settles? | Filterable? | Tyndall Effect |
|------|--------------|----------|-------------|----------------|
| Solution | < 1 nm | No | No | No |
| Colloid | 1-1000 nm | No | No | Yes |
| Suspension | > 1000 nm | Yes | Yes | Yes |

## Types of Colloids

| Name | Dispersed Phase | Dispersing Medium | Example |
|------|----------------|-------------------|---------|
| Sol | Solid | Liquid | Paint, ink |
| Gel | Liquid | Solid | Gelatin, jelly |
| Emulsion | Liquid | Liquid | Milk, mayonnaise |
| Foam | Gas | Liquid | Whipped cream, soap suds |
| Solid foam | Gas | Solid | Styrofoam |
| Aerosol | Solid/Liquid | Gas | Smoke, fog |
| Solid aerosol | Solid | Gas | Smoke |
| Liquid aerosol | Liquid | Gas | Fog, mist |

## Key Properties

### Tyndall Effect
- Light scattering by colloidal particles
- Beam of light visible through colloid
- NOT observed in true solutions

### Brownian Motion
- Random motion of colloidal particles
- Result of collisions with solvent molecules
- Prevents settling

### Stability Factors
1. **Brownian motion** - kinetic stability
2. **Electrical charge** - particles repel each other
3. **Solvation layers** - solvent molecules surround particles

## Decision Tree

```
Identifying mixture type?
©À©¤ Filter through paper?
©¦   ©À©¤ Residue left ¡ú Suspension
©¦   ©¸©¤ No residue ¡ú Solution or Colloid
©À©¤ Shine light through?
©¦   ©À©¤ Beam visible ¡ú Colloid
©¦   ©¸©¤ Beam invisible ¡ú Solution
©¸©¤ Let stand 24 hours?
    ©À©¤ Settles out ¡ú Suspension
    ©¸©¤ Remains mixed ¡ú Solution or Colloid
```

## Key Constraints
- Colloid particles are too small to see individually
- Too large to pass through cell membranes unchanged
- Cannot be separated by ordinary filtration
- Can be separated by ultrafiltration or centrifugation

## Problem Archetypes
1. Classify mixture by particle size
2. Identify colloid type from phases
3. Explain Tyndall effect
4. Distinguish colloid from solution/suspension

## L3 Tools
- `classify_by_size(particle_size_nm)` ¡ú mixture type
- `identify_colloid_type(dispersed, dispersing)` ¡ú colloid name
- `tyndall_effect_test(particle_size)` ¡ú bool
- `brownian_motion_check(particle_size, temperature)` ¡ú significance

## L4 Reference

## L5 Examples
See `../L5_examples/buffer/ for worked examples.

## Implementations

- Implementation: `../L3_functions/colloid_tools.py`

## L3 Tool Call Directives

**Source:** `colloid_tools.py`

Colloid Tools - L3 Implementation

### Available functions:
- `classify_by_particle_size(size_nm: float)` → str — Classify mixture type by particle size.
- `identify_colloid_type(dispersed: str, dispersing: str)` → str — Identify colloid type from dispersed and dispersing phases.
- `tyndall_effect_test(particle_size_nm: float)` → bool — Determine if mixture will show Tyndall effect.
- `settling_behavior(particle_size_nm: float)` → str — Predict settling behavior based on particle size.
- `filtration_behavior(particle_size_nm: float)` → str — Predict filtration behavior based on particle size.
- `get_colloid_examples(colloid_type: str)` → list — Get examples of a specific colloid type.
- `compare_mixture_types()` → dict — Return comparison table of mixture types.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters
