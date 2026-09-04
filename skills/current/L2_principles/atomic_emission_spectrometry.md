---
id: atomic_emission_spectrometry
layer: 2
title: Atomic Emission Spectrometry (AES)
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/electronic_spectroscopy_tools.py
cross_links:
  - ./atomic_absorption_spectroscopy.md
  - ./spectroscopic_methods.md
source: Skoog Instrumental Analysis Ch10 (LibreTexts)
---

## Context

Atomic Emission Spectrometry (AES) measures radiation emitted by excited atoms returning to lower energy states. The most important technique is Inductively Coupled Plasma-Optical Emission Spectrometry (ICP-OES), which offers multi-element capability, wide linear dynamic range, and excellent detection limits.

---

## Fundamental Principles

### Thermal Excitation

Atoms are excited by collisions with high-energy particles in hot sources:

```
N* / N₀ = (g*/g₀) × exp(-E/kT)
```

Where:
- N* = population of excited state
- N₀ = population of ground state
- g = statistical weights
- E = excitation energy
- k = Boltzmann constant
- T = temperature

### Emission Intensity

```
I = k × N* × hν × A
```

Where:
- I = emission intensity
- A = transition probability
- hν = photon energy
- k = geometric factor

### Boltzmann Distribution

At higher temperatures, more atoms are excited:
- T = 3000 K: ~1% atoms excited
- T = 6000 K: ~10% atoms excited
- T = 10000 K: ~50% atoms excited

---

## Excitation Sources

### Flame Emission

| Flame | Temperature | Application |
|-------|-------------|-------------|
| Air-C₂H₂ | 2300°C | Alkali, alkaline earth |
| N₂O-C₂H₂ | 2900°C | Limited elements |

**Advantages:** Simple, inexpensive
**Disadvantages:** Few elements, poor sensitivity

### Arc and Spark

| Type | Temperature | Sample |
|------|-------------|--------|
| DC Arc | 4000-5000 K | Solids |
| AC Spark | 4000-5000 K | Solids |

**Applications:** Qualitative analysis, metals analysis

### Inductively Coupled Plasma (ICP)

**Temperature:** 6000-10000 K

**Advantages:**
- Multi-element capability
- Wide linear range (5 orders)
- Low detection limits (ppb)
- Minimal chemical interferences
- Good for refractory elements

**Disadvantages:**
- Expensive instrumentation
- High operating costs (Ar gas)
- Spectral interferences common

---

## ICP-OES Instrumentation

### Plasma Torch

Three concentric quartz tubes with argon flow:

| Zone | Temperature | Function |
|------|-------------|----------|
| Induction zone | ~10000 K | RF coupling |
| Analytical zone | 6000-7000 K | Atomization/excitation |
| Preheating zone | ~5000 K | Sample desolvation |

### RF Generator

- Frequency: 27.12 or 40.68 MHz
- Power: 1-2 kW
- Creates oscillating magnetic field

### Sample Introduction

1. **Nebulizer** - Creates aerosol
   - Pneumatic (most common)
   - Ultrasonic (higher efficiency)
   
2. **Spray Chamber** - Selects fine droplets
   - Cyclonic
   - Scott-type

3. **Desolvation System** - Optional
   - Removes solvent before plasma

### Spectrometers

#### Sequential (Monochromator)

- One element at a time
- Czerny-Turner design
- High resolution

#### Simultaneous (Polychromator)

- Multiple elements at once
- Fixed wavelengths (Paschen-Runge)
- Faster analysis

#### Array Detectors (ICP-OES)

- CCD or CID detectors
- Full spectrum capture
- Flexible wavelength selection

### Viewing Modes

| Mode | Advantages | Disadvantages |
|------|------------|---------------|
| Radial | Better for high concentrations | Higher detection limits |
| Axial | 5-10× better sensitivity | Matrix effects, self-absorption |

---

## Spectral Interferences

### Types

| Interference | Cause | Example |
|--------------|-------|---------|
| Direct overlap | Lines at same λ | As 228.812 / Cd 228.802 |
| Background shift | Continuum emission | High salt matrices |
| Wing overlap | Broad lines | Al lines near Fe |

### Correction Methods

1. **Background correction**
   - Measure near analyte wavelength
   - Interpolate baseline

2. **Inter-element correction (IEC)**
   ```
   C_corrected = C_measured - k × I_interferent
   ```

3. **Alternative wavelength**
   - Choose interference-free line
   - May sacrifice sensitivity

4. **High resolution spectrometer**
   - Separate overlapping lines
   - Δλ < 0.01 nm

---

## Quantitative Analysis

### Calibration

**External Standards:**
```
I = m × c + b
```

**Internal Standard:**
```
I_analyte / I_IS = f(c)
```

Best for compensating drift and matrix effects.

### Linear Dynamic Range

ICP-OES: 10⁴ - 10⁵ concentration range
- Multiple wavelengths extend range
- High concentration line + low concentration line

### Detection Limits

| Element | ICP-OES (μg/L) | ICP-MS (μg/L) |
|---------|----------------|---------------|
| Na | 0.2 | 0.005 |
| Ca | 0.02 | 0.02 |
| Fe | 0.3 | 0.005 |
| Pb | 1 | 0.001 |
| As | 2 | 0.001 |

---

## Problem-Solving Examples

### Example 1: Boltzmann Population

**Problem**: Calculate the ratio of excited to ground state atoms for Na 589 nm at 5000 K.

**Solution:**
```
E = hc/λ = (6.626×10⁻³⁴ × 3×10⁸)/(589×10⁻⁹) = 3.37×10⁻¹⁹ J
N*/N₀ = (g*/g₀) × exp(-E/kT)
      = 2 × exp(-3.37×10⁻¹⁹/(1.38×10⁻²³ × 5000))
      = 2 × exp(-4.88)
      = 2 × 0.0076
      = 0.015 = 1.5%
```

### Example 2: Internal Standard Calculation

**Problem**: Using Y as internal standard at 371 nm, calculate Ca concentration.

| Solution | Ca (373 nm) | Y (371 nm) | Ca/Y ratio |
|----------|-------------|------------|------------|
| Standard 1 ppm | 1200 | 5000 | 0.24 |
| Standard 5 ppm | 6000 | 5000 | 1.20 |
| Unknown | 3600 | 5000 | 0.72 |

**Solution:**
```
Slope = (1.20 - 0.24)/(5 - 1) = 0.24/ppm
c_unk = (0.72 - 0.24)/0.24 = 2.0 ppm
```

Or by linear regression: c_unk = 3.0 ppm

### Example 3: Interference Correction

**Problem**: As 188.979 nm interfered by Al 188.979 nm. IEC factor = 0.004. Measured As = 10 μg/L, Al = 500 μg/L. Find true As.

**Solution:**
```
As_corrected = As_measured - k × Al
             = 10 - 0.004 × 500
             = 10 - 2 = 8 μg/L
```

---

## Decision Flow

1. **Choose technique:**
   - Multi-element needed? → ICP-OES or ICP-MS
   - Few elements, high conc? → Flame AAS
   - Ultra-trace? → ICP-MS
   - Solids analysis? → Spark OES

2. **Select wavelengths:**
   - Check for interferences
   - Choose appropriate sensitivity
   - Consider internal standard

3. **Address interferences:**
   - Spectral overlap? → IEC or alternate λ
   - High matrix? → Dilution or internal standard
   - Background? → Background correction

---

## Comparison of Techniques

| Parameter | Flame AAS | ICP-OES | ICP-MS |
|-----------|-----------|---------|--------|
| Multi-element | No | Yes | Yes |
| Linear range | 2 orders | 5 orders | 9 orders |
| Detection limit | ppm | ppb | ppt |
| Cost | Low | High | Very high |
| Speed | Fast | Fast | Fast |
| Interferences | Chemical | Spectral | Mass |

---

## Cross-References
- Atomic Absorption: [atomic_absorption_spectroscopy.md](./atomic_absorption_spectroscopy.md)
- Atomic Mass Spectrometry: [atomic_mass_spectrometry.md](./atomic_mass_spectrometry.md)
