---
id: atomic_absorption_spectroscopy
layer: 2
title: Atomic Absorption and Atomic Fluorescence Spectroscopy
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/electronic_spectroscopy_tools.py
cross_links:
  - ./spectroscopic_methods.md
  - ./electrochemistry.md
source: Skoog Instrumental Analysis Ch9 (LibreTexts)
---

## Context

Atomic Absorption Spectroscopy (AAS) and Atomic Fluorescence Spectroscopy (AFS) are elemental analysis techniques based on absorption and emission of light by free atoms. AAS is widely used for trace metal analysis in environmental, clinical, and industrial samples. AFS offers enhanced sensitivity for specific elements.

---

## Atomic Absorption Spectroscopy (AAS)

### Fundamental Principles

Absorption of light by ground-state atoms in the gas phase:

```
A = ε × b × N
```

Where:
- A = absorbance
- ε = absorption coefficient
- b = path length
- N = number of absorbing atoms

### Beer's Law for Atoms

```
A = log(I₀/I) = k × c
```

Concentration is proportional to absorbance for dilute solutions.

### Instrumentation

#### 1. Radiation Sources

**Hollow Cathode Lamp (HCL)**
- Primary source for most elements
- Cathode made of analyte element
- Emits sharp line spectrum
- One lamp per element (usually)

**Electrodeless Discharge Lamp (EDL)**
- Used for volatile elements (As, Se, Te)
- Higher intensity than HCL
- Better for refractory elements

#### 2. Atomizers

**Flame Atomizer (FAAS)**
| Flame Type | Temperature | Application |
|------------|-------------|-------------|
| Air-Acetylene | 2300°C | Most elements |
| N₂O-Acetylene | 2900°C | Refractory elements |
| Air-Propane | 1900°C | Alkali metals |

**Graphite Furnace (GFAAS)**
- Electrothermal atomization
- Higher sensitivity (100-1000× flame)
- Smaller sample volume (μL vs mL)
- Longer analysis time

#### 3. Monochromator

- Isolates analytical wavelength
- Typically Czerny-Turner design
- Bandpass: 0.1-2 nm

#### 4. Detector

- Photomultiplier tube (PMT)
- Converts light to electrical signal

### Flame AAS Process

1. **Nebulization**: Sample converted to aerosol
2. **Desolvation**: Solvent evaporates
3. **Vaporization**: Solid particles vaporize
4. **Atomization**: Molecules dissociate to atoms
5. **Excitation/Ionization**: Some atoms excited/ionized

### Graphite Furnace Temperature Program

| Step | Temperature | Purpose |
|------|-------------|---------|
| Drying | 100-150°C | Remove solvent |
| Pyrolysis | 300-1500°C | Remove matrix |
| Atomization | 2000-3000°C | Atomize analyte |
| Clean-out | 2500-3000°C | Remove residue |

### Quantitative Analysis

#### Calibration Curve Method

```
A = m × c + b
```

Linear range typically 0-0.5 AU.

#### Standard Addition Method

For matrix effects:

```
A = k(cₓ + cₛ)
```

Where:
- cₓ = unknown concentration
- cₛ = added standard concentration

Plot A vs cₛ; extrapolate to A = 0 to find -cₓ

### Interferences

#### Spectral Interferences

| Type | Cause | Correction |
|------|-------|------------|
| Line overlap | Another element absorbs | Use alternate wavelength |
| Molecular absorption | Molecules absorb | Background correction |
| Light scattering | Particles scatter light | Background correction |

#### Background Correction Methods

1. **Deuterium Lamp Method**
   - D₂ lamp provides continuum
   - Background absorbs continuum
   - Difference gives atomic signal

2. **Zeeman Effect Method**
   - Magnetic field splits lines
   - σ components for background
   - π component for atomic signal

3. **Smith-Hieftje Method**
   - High current pulses broaden lines
   - Self-reversal measures background

#### Chemical Interferences

| Type | Effect | Correction |
|------|--------|------------|
| Compound formation | Reduced atomization | Releasing agents |
| Ionization | Ground state loss | Ionization suppressors |
| Volatility | Incomplete atomization | Matrix modifiers |

**Common Releasing Agents:**
- Lanthanum (for phosphate interference)
- EDTA (complexes interfering ions)

**Ionization Suppressors:**
- Cesium or potassium salts
- Provide excess electrons

---

## Atomic Fluorescence Spectroscopy (AFS)

### Principles

Emission of radiation after excitation by external source:

```
I_F = k × I₀ × c
```

Where:
- I_F = fluorescence intensity
- I₀ = source intensity
- c = concentration
- k = proportionality constant

### Types of Atomic Fluorescence

| Type | Transition | Characteristic |
|------|------------|----------------|
| Resonance | Same wavelength | Most common |
| Stokes | Longer wavelength | Energy loss |
| Anti-Stokes | Shorter wavelength | Thermal energy gain |

### Advantages Over AAS

1. **Higher sensitivity** for some elements
2. **Better linearity** over wider range
3. **Multi-element capability**
4. **No source modulation needed**

### Applications

- Hydride generation AFS for As, Se, Sb, Bi
- Cold vapor AFS for Hg
- Extremely low detection limits (sub-ppb)

---

## Detection Limits

| Element | Flame AAS | GFAAS | AFS |
|---------|-----------|-------|-----|
| Pb | 10 μg/L | 0.2 μg/L | 1 μg/L |
| Cd | 1 μg/L | 0.02 μg/L | 0.1 μg/L |
| Hg | 500 μg/L | 2 μg/L | 0.001 μg/L |
| As | 50 μg/L | 0.5 μg/L | 0.01 μg/L |

---

## Problem-Solving Examples

### Example 1: Standard Addition

**Problem**: A sample gives absorbance 0.250. After adding 2 ppm standard, absorbance is 0.450. Find the sample concentration.

**Solution:**
```
Using single-point standard addition:
cₓ = A₁ × cₛ / (A₂ - A₁)
cₓ = 0.250 × 2 ppm / (0.450 - 0.250)
cₓ = 0.500 / 0.200
cₓ = 2.5 ppm
```

### Example 2: Graphite Furnace Program

**Problem**: Design a temperature program for Pb in blood using GFAAS.

**Solution:**
| Step | T (°C) | Ramp (s) | Hold (s) |
|------|--------|----------|----------|
| Dry | 110 | 10 | 20 |
| Pyrolysis | 600 | 10 | 15 |
| Atomization | 1800 | 0 | 5 |
| Clean | 2500 | 1 | 3 |

Note: Matrix modifier (Pd/Mg) used to stabilize Pb

### Example 3: Sensitivity Calculation

**Problem**: A 1 ppm Pb standard gives A = 0.15. Calculate the characteristic concentration (concentration giving 0.0044 AU).

**Solution:**
```
Sensitivity = A/c = 0.15 AU/ppm
c₀ = 0.0044 AU / (0.15 AU/ppm) = 0.029 ppm = 29 μg/L
```

---

## Decision Flow

1. **Choose technique:**
   - Routine metals? → Flame AAS
   - Trace levels? → GFAAS
   - Hg, As, Se? → AFS or cold vapor
   - Multi-element? → ICP-OES or ICP-MS

2. **Select atomizer:**
   - High concentration (> ppm)? → Flame
   - Low concentration (ppb)? → Graphite furnace
   - Complex matrix? → Standard addition

3. **Address interferences:**
   - High salt content? → Background correction
   - Refractory compounds? → Releasing agents
   - Easily ionized? → Ionization suppressor

---

## Quick Reference

| Parameter | Flame AAS | GFAAS |
|-----------|-----------|-------|
| Sample volume | 2-5 mL | 10-50 μL |
| Analysis time | 10-30 s | 2-5 min |
| Detection limits | ppm | ppb |
| Precision | 0.5-2% | 1-5% |
| Linear range | 2-3 orders | 2 orders |

---

## Cross-References
- Spectroscopic methods: [spectroscopic_methods.md](./spectroscopic_methods.md)
- Electroanalytical methods: [electrochemistry.md](./electrochemistry.md)
