---
id: chem.kinetic_theory_effusion
layer: 2
title: Effusion, Diffusion, and Kinetic Molecular Theory
source: Ch08.05-08.06
dependencies: [ideal_gas_law]
stability: high
confidence: high
---

## Concept

Kinetic molecular theory explains gas behavior at the molecular level. Effusion and diffusion rates depend on molecular speed.

## Core Formulas

### Graham's Law of Effusion
```
rate?/rate? = ¡Ì(M?/M?)

Where M = molar mass (g/mol)
```

### Average Kinetic Energy
```
KE_avg = (3/2)RT = (3/2)kT

Where k = R/NA = Boltzmann constant
```

### Root Mean Square Speed
```
u_rms = ¡Ì(3RT/M)

Where M = molar mass in kg/mol
```

### Other Speeds
```
Most probable speed: u_mp = ¡Ì(2RT/M)
Average speed: u_avg = ¡Ì(8RT/¦ÐM)
```

## Decision Tree

```
Comparing effusion rates?
©À©¤ Use Graham's Law: rate?/rate? = ¡Ì(M?/M?)
©¸©¤ Lighter gas effuses faster

Finding molecular speed?
©À©¤ rms speed ¡ú u_rms = ¡Ì(3RT/M)
©À©¤ average speed ¡ú u_avg = ¡Ì(8RT/¦ÐM)
©¸©¤ most probable ¡ú u_mp = ¡Ì(2RT/M)

Molar mass from effusion?
©¸©¤ Compare known and unknown: M? = M?(rate?/rate?)2
```

## KMT Postulates
1. Gas particles in constant random motion
2. Particles have negligible volume
3. No intermolecular forces
4. Collisions are elastic
5. KE ¡Ø temperature

## Problem Archetypes
1. Compare effusion rates of two gases
2. Calculate rms speed at given temperature
3. Find molar mass from effusion data
4. Compare speeds at different temperatures

## L3 Tools
- `grahams_law(M1, M2, rate1, rate2)` ¡ú missing value
- `rms_speed(T, M)` ¡ú u_rms
- `average_speed(T, M)` ¡ú u_avg
- `most_probable_speed(T, M)` ¡ú u_mp

## L4 Reference

## L5 Examples
See `../L5_examples/phase_diagrams/ for worked examples.

## Implementations

- Implementation: `../L3_functions/kinetic_theory_tools.py`

## L3 Tool Call Directives

**Source:** `kinetic_theory_tools.py`

Kinetic molecular theory calculations: Graham's law of effusion, molecular speeds (rms, average, most probable), and kinetic energy.

### Available functions:
- `grahams_law(M1, M2, rate1, rate2, time1, time2)` → float — rate1/rate2 = √(M2/M1); pass None for unknown
- `rms_speed(T, M)` → float — u_rms = √(3RT/M) in m/s; M in g/mol, T in K
- `average_speed(T, M)` → float — u_avg = √(8RT/πM) in m/s
- `most_probable_speed(T, M)` → float — u_mp = √(2RT/M) in m/s
- `kinetic_energy_per_mole(T)` → float — KE = (3/2)RT in J/mol
- `kinetic_energy_per_molecule(T)` → float — KE = (3/2)kT in J/molecule
- `compare_speeds(T, M1, M2)` → Dict — Compare all speeds for two gases

### Common errors:
- ❌ Using temperature in °C instead of Kelvin (MUST convert first)
- ❌ Confusing rate vs time (rate ∝ 1/time; lighter gas has higher rate, shorter time)
- ❌ Forgetting that u_rms > u_avg > u_mp for same gas (different formulas)
