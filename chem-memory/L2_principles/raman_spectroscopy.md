---
id: raman_spectroscopy
layer: 2
title: Raman Spectroscopy
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/ir_spectroscopy_tools.py
cross_links:
  - ./spectroscopy.md
  - ./molecular_luminescence.md
source: Skoog Instrumental Analysis Ch18 (LibreTexts)
---

## Context

Raman spectroscopy is a vibrational technique based on inelastic scattering of monochromatic light. It provides complementary information to IR spectroscopy and is particularly useful for aqueous samples, symmetric vibrations, and non-polar bonds. Surface-enhanced Raman (SERS) enables single-molecule detection.

---

## Fundamental Principles

### Light Scattering

When light interacts with molecules:

| Type | Energy Change | Frequency | Probability |
|------|---------------|-----------|-------------|
| Rayleigh | None | ν₀ | 99.999% |
| Stokes Raman | Loss | ν₀ - ν_vib | 0.001% |
| Anti-Stokes Raman | Gain | ν₀ + ν_vib | 0.0001% |

### Raman Effect

Inelastic scattering due to molecular vibration:

```
ν_Raman = |ν₀ - ν_scattered| = ν_vib
```

### Selection Rule

Raman active if polarizability changes during vibration:
```
(∂α/∂Q) ≠ 0
```

Where α = polarizability, Q = normal coordinate

### Comparison with IR

| Property | Raman | IR |
|----------|-------|-----|
| Selection rule | Δα ≠ 0 | Δμ ≠ 0 |
| Strong bands | Symmetric | Asymmetric |
| Water interference | Weak | Strong |
| Sample preparation | Minimal | Often required |
| Wavelength range | 50-4000 cm⁻¹ | 600-4000 cm⁻¹ |

---

## Raman Intensity

### Basic Equation

```
I_Raman ∝ I₀ × ν⁴ × (dα/dQ)²
```

Where:
- I₀ = incident intensity
- ν = excitation frequency
- dα/dQ = polarizability derivative

### Frequency Dependence

Higher excitation frequency gives stronger Raman signal:
- 532 nm laser: 4× stronger than 785 nm (for same power)
- 785 nm laser: preferred for fluorescent samples

### Stokes vs Anti-Stokes Ratio

```
I_anti-Stokes/I_Stokes = (ν₀ + ν_vib)⁴/(ν₀ - ν_vib)⁴ × exp(-hν_vib/kT)
```

Anti-Stokes intensity decreases with:
- Lower temperature
- Higher vibrational frequency

---

## Instrumentation

### Light Sources

| Laser | Wavelength | Application |
|-------|------------|-------------|
| Ar⁺ | 488, 514 nm | High sensitivity |
| Nd:YAG | 532 nm | General purpose |
| Diode | 785 nm | Fluorescent samples |
| HeNe | 633 nm | Balance of sensitivity/fluorescence |
| Nd:YAG (IR) | 1064 nm (FT-Raman) | Fluorescent samples |

### Spectrometers

#### Dispersive Raman

- Grating-based
- CCD detector
- High resolution

#### FT-Raman

- Michelson interferometer
- Near-IR laser (1064 nm)
- Avoids fluorescence
- Lower sensitivity

### Sampling Configurations

| Configuration | Advantages |
|---------------|------------|
| 180° backscatter | Most common, easy alignment |
| 90° scattering | Solution studies |
| Microscope | Small samples, mapping |
| Fiber optic | Remote sensing |

---

## Types of Raman Spectroscopy

### Normal Raman

- Standard Raman scattering
- Detection limit: ~1% (10,000 ppm)
- Limited by fluorescence

### Surface-Enhanced Raman (SERS)

**Enhancement factor: 10⁶ - 10¹⁴**

Mechanisms:
1. **Electromagnetic:** Localized surface plasmons
2. **Chemical:** Charge transfer complexes

Substrates:
- Colloidal Au or Ag nanoparticles
- Roughened metal surfaces
- Nanostructured films

### Resonance Raman (RR)

When excitation wavelength matches electronic transition:
- Enhancement: 10³ - 10⁵
- Selective enhancement of chromophore vibrations
- Useful for heme proteins, carotenoids

### Coherent Anti-Stokes Raman (CARS)

- Nonlinear four-wave mixing
- Signal at anti-Stokes frequency
- No fluorescence interference
- Microscopy applications

### Tip-Enhanced Raman (TERS)

- Combines AFM with SERS
- Nanometer spatial resolution
- Single-molecule detection

---

## Applications

### Functional Group Identification

| Vibration | Raman Shift (cm⁻¹) | Strength |
|-----------|-------------------|----------|
| C≡C stretch | 2100-2260 | Strong |
| C=C stretch | 1600-1680 | Strong |
| C=O stretch | 1680-1820 | Weak-moderate |
| C-C stretch | 800-1200 | Variable |
| S-S stretch | 500-550 | Strong |
| C-S stretch | 600-700 | Strong |

### Material Identification

- Polymorphism in pharmaceuticals
- Carbon nanomaterials (D, G bands)
- Gemstone identification
- Art conservation

### Biological Applications

- Protein secondary structure
- Nucleic acid conformation
- Cell imaging
- Bacterial identification

### Quantitative Analysis

```
I_Raman = k × c
```

Calibration methods:
- External standards
- Internal standards
- Multivariate calibration

---

## Problem-Solving Examples

### Example 1: Wavenumber Calculation

**Problem**: A Raman shift is observed at 532.5 nm using 488 nm excitation. Calculate the Raman shift in cm⁻¹.

**Solution:**
```
ν₀ = 1/λ₀ = 1/488×10⁻⁷ cm = 20492 cm⁻¹
ν_scattered = 1/λ = 1/532.5×10⁻⁷ cm = 18779 cm⁻¹
Δν = ν₀ - ν_scattered = 20492 - 18779 = 1713 cm⁻¹
```

### Example 2: Enhancement Factor

**Problem**: Normal Raman signal is 100 counts for 0.1 M analyte. SERS signal is 100000 counts for 10⁻⁶ M analyte. Calculate enhancement factor.

**Solution:**
```
EF = (I_SERS/I_normal) × (c_normal/c_SERS)
EF = (100000/100) × (0.1/10⁻⁶)
EF = 1000 × 100000 = 10⁸
```

### Example 3: Stokes/Anti-Stokes Temperature

**Problem**: Stokes intensity is 1000, anti-Stokes is 50 for a 500 cm⁻¹ band. Estimate temperature.

**Solution:**
```
I_AS/I_S = exp(-hν/kT)
50/1000 = exp(-(6.626×10⁻³⁴ × 3×10¹⁰ × 500)/(1.38×10⁻²³ × T))
0.05 = exp(-7.2×10⁻²²/T)
ln(0.05) = -7.2×10⁻²²/T
T = 7.2×10⁻²²/3.0 = 2.4×10² K = 240 K
```

### Example 4: Band Assignment

**Problem**: A compound shows strong Raman bands at 2225, 1600, and 530 cm⁻¹. Identify likely functional groups.

**Solution:**
- 2225 cm⁻¹: C≡C or C≡N stretch (symmetric, Raman active)
- 1600 cm⁻¹: C=C aromatic or conjugated
- 530 cm⁻¹: S-S stretch

Compound likely contains nitrile or alkyne + aromatic + disulfide

---

## Decision Flow

1. **Choose laser wavelength:**
   - Non-fluorescent? → 532 nm (highest sensitivity)
   - Some fluorescence? → 633 or 785 nm
   - High fluorescence? → 1064 nm FT-Raman

2. **Select technique:**
   - Trace analysis? → SERS
   - Chromophore present? → Resonance Raman
   - Microscopy needed? → Raman microscope

3. **Sample preparation:**
   - Solid? → Direct analysis
   - Solution? → Cuvette or capillary
   - Fluorescent? → Try longer wavelength

---

## Quick Reference

| Band | Raman Shift (cm⁻¹) | Notes |
|------|-------------------|-------|
| D (disordered carbon) | ~1350 | Diamond not present |
| G (graphitic carbon) | ~1580 | Sp² carbon |
| 2D (graphene) | ~2700 | Number of layers |

---

## Cross-References
- Infrared Spectroscopy: [spectroscopy.md](./spectroscopy.md)
- Molecular Luminescence: [molecular_luminescence.md](./molecular_luminescence.md)
