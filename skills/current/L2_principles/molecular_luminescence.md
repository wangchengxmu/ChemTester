---
id: molecular_luminescence
layer: 2
title: Molecular Luminescence Spectrometry
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/electronic_spectroscopy_tools.py
cross_links:
  - ./uv_vis_spectroscopy.md
  - ./spectroscopic_methods.md
source: Skoog Instrumental Analysis Ch15 (LibreTexts)
---

## Context

Molecular luminescence includes fluorescence and phosphorescence - emission of radiation from electronically excited molecules. Fluorescence offers exceptional sensitivity (10-1000× better than absorption) and selectivity, making it valuable for trace analysis in clinical, environmental, and pharmaceutical applications.

---

## Types of Luminescence

### Fluorescence

- **Mechanism:** Singlet → Singlet transition (S₁ → S₀)
- **Lifetime:** 10⁻⁹ to 10⁻⁶ seconds
- **Spin state:** No change (ΔS = 0)

### Phosphorescence

- **Mechanism:** Triplet → Singlet transition (T₁ → S₀)
- **Lifetime:** 10⁻³ to 10² seconds
- **Spin state:** Change (ΔS = 1)
- **Longer wavelength than fluorescence**

### Delayed Fluorescence

- Emission from S₁ after T₁ → S₁ intersystem crossing
- Same wavelength as prompt fluorescence
- Longer lifetime than prompt fluorescence

---

## Jablonski Diagram

```
       S₂ ───────────────
         │ ↘ IC
       S₁ ───────────────
         │ ↘ ISC    │ F
         │          │ ↓
       T₁ ───────────────
         │          │ P
         │          │ ↓
       S₀ ───────────────
         
IC = Internal Conversion
ISC = Intersystem Crossing
F = Fluorescence
P = Phosphorescence
```

### Key Processes

| Process | Transition | Timescale |
|---------|------------|-----------|
| Absorption | S₀ → S₁, S₂ | 10⁻¹⁵ s |
| Vibrational relaxation | S₁(v*) → S₁(v=0) | 10⁻¹² s |
| Internal conversion | S₂ → S₁ | 10⁻¹² s |
| Fluorescence | S₁ → S₀ | 10⁻⁹-10⁻⁶ s |
| Intersystem crossing | S₁ → T₁ | 10⁻⁸ s |
| Phosphorescence | T₁ → S₀ | 10⁻³-10² s |

---

## Fluorescence Intensity

### Basic Equation

```
I_F = 2.303 × K × I₀ × ε × b × c × Φ_F
```

For dilute solutions (A < 0.05):
```
I_F ∝ c
```

Where:
- I_F = fluorescence intensity
- K = instrumental constant
- I₀ = source intensity
- ε = molar absorptivity
- b = path length
- c = concentration
- Φ_F = quantum yield

### Quantum Yield

```
Φ_F = (photons emitted)/(photons absorbed) = k_F/(k_F + k_NR)
```

Where:
- k_F = fluorescence rate constant
- k_NR = non-radiative rate constant

**Maximum Φ_F = 1** (all absorbed photons re-emitted)

### Inner Filter Effect

At high concentrations, fluorescence deviates from linearity:

1. **Primary inner filter:** Absorption of excitation light
2. **Secondary inner filter:** Reabsorption of emission

**Correction:**
```
I_corrected = I_observed × antilog[(A_ex + A_em)/2]
```

---

## Stokes Shift

Emission occurs at longer wavelength than absorption due to energy loss:

```
Stokes shift = λ_em - λ_ex
```

**Typical values:** 10-200 nm

**Importance:** Allows separation of excitation and emission

---

## Factors Affecting Fluorescence

### Molecular Structure

**Fluorescent compounds typically have:**
- Rigid conjugated π-system
- Low-energy π* → π transitions
- Electron-donating groups
- Planar structure

| Effect | Examples |
|--------|----------|
| Enhance fluorescence | -OH, -NH₂, -OR |
| Quench fluorescence | -NO₂, -COOH, -Br, -I |
| Increase rigidity | Fused rings (anthracene) |

### Structural Examples

| Compound | Φ_F | Reason |
|----------|-----|--------|
| Fluorescein | 0.93 | Rigid, conjugated |
| Phenol | 0.14 | Less conjugated |
| Benzene | 0.07 | No rigidity |
| Naphthalene | 0.55 | Rigid, conjugated |

### Environmental Factors

| Factor | Effect |
|--------|--------|
| Temperature | Higher T → lower Φ_F (more collisional quenching) |
| Viscosity | Higher viscosity → higher Φ_F |
| pH | Affects ionizable groups |
| Heavy atoms | Decrease Φ_F (heavy atom effect) |
| Oxygen | Quenches fluorescence |

---

## Quenching Mechanisms

### Dynamic (Collisional) Quenching

**Stern-Volmer Equation:**
```
F₀/F = 1 + k_q × τ₀ × [Q] = 1 + K_SV × [Q]
```

Where:
- F₀ = fluorescence without quencher
- F = fluorescence with quencher
- k_q = bimolecular quenching constant
- τ₀ = lifetime without quencher
- K_SV = Stern-Volmer constant

### Static Quenching

Formation of non-fluorescent complex:
```
F₀/F = 1 + K_a × [Q]
```

Where K_a = association constant

### Combined Quenching

```
F₀/F = (1 + K_SV[Q])(1 + K_a[Q])
```

Upward curvature in Stern-Volmer plot indicates combined mechanisms.

---

## Instrumentation

### Components

1. **Light Source**
   - Xenon arc lamp (continuum)
   - LED (monochromatic)
   - Laser (high intensity, monochromatic)

2. **Excitation Monochromator**
   - Selects excitation wavelength

3. **Sample Cell**
   - Quartz (all wavelengths)
   - Four transparent faces

4. **Emission Monochromator**
   - Selects emission wavelength

5. **Detector**
   - Photomultiplier tube (PMT)
   - Photodiode array (for spectra)

### Geometries

| Geometry | Application |
|----------|-------------|
| 90° (L-format) | Standard |
| Front-face | Opaque samples |
| 180° | Fiber optic probes |

### Spectrofluorometer vs Fluorometer

| Feature | Spectrofluorometer | Fluorometer |
|---------|-------------------|-------------|
| Wavelength selection | Monochromators | Filters |
| Flexibility | High | Low |
| Cost | High | Low |
| Sensitivity | Good | Excellent |

---

## Applications

### Direct Fluorescence

- Vitamins (riboflavin, vitamin A)
- Drugs (quinine, tetracyclines)
- Environmental pollutants (PAHs)

### Derivatization

- Amino acids with fluorescamine
- Amines with dansyl chloride
- Carbonyls with DNPH

### Metal Complexes

- Al³⁺ with 8-hydroxyquinoline
- Mg²⁺ with 8-hydroxyquinoline
- Ca²⁺ with calcein

### Fluorescence Quenching

- Oxygen sensing
- Chloride sensing (SPQ)
- Metal ions

---

## Phosphorescence

### Room Temperature Phosphorescence (RTP)

Requires:
- Rigid matrix (solid substrate)
- Heavy atom perturbation
- Oxygen-free environment

### Low Temperature Phosphorescence

At 77 K (liquid N₂):
- Reduced collisional deactivation
- Enhanced phosphorescence

### Instrumentation

Similar to fluorescence but with:
- Phosphoroscope (rotating chopper)
- Time-resolved detection
- Longer measurement times

---

## Problem-Solving Examples

### Example 1: Quantum Yield Calculation

**Problem**: A compound absorbs 10⁶ photons and emits 4.5×10⁵ photons. Calculate Φ_F.

**Solution:**
```
Φ_F = (photons emitted)/(photons absorbed)
Φ_F = 4.5×10⁵ / 10⁶ = 0.45 = 45%
```

### Example 2: Stern-Volmer Analysis

**Problem**: Fluorescence intensity decreases from 500 to 200 units when 0.01 M quencher is added. Calculate K_SV.

**Solution:**
```
F₀/F = 500/200 = 2.5
K_SV = (F₀/F - 1)/[Q] = (2.5 - 1)/0.01 = 150 M⁻¹
```

### Example 3: Calibration

**Problem**: Standard calibration gives slope 12000 FU/ppm. A sample gives 36000 FU. Find concentration.

**Solution:**
```
c = signal/slope = 36000/12000 = 3 ppm
```

### Example 4: Inner Filter Correction

**Problem**: A sample has A_ex = 0.15 and A_em = 0.10. Observed intensity is 450. Calculate corrected intensity.

**Solution:**
```
I_corrected = I_obs × antilog[(0.15 + 0.10)/2]
            = 450 × antilog[0.125]
            = 450 × 1.33
            = 600 FU
```

---

## Decision Flow

1. **Choose technique:**
   - Native fluorescence? → Direct method
   - No fluorescence? → Derivatization
   - Selectivity issue? → Phosphorescence or time-resolved

2. **Select wavelength:**
   - Run excitation spectrum
   - Choose excitation λ_max
   - Run emission spectrum
   - Choose emission λ_max

3. **Optimize conditions:**
   - pH adjustment
   - Temperature control
   - Oxygen removal (if needed)

---

## Quick Reference

| Parameter | Typical Value |
|-----------|---------------|
| Stokes shift | 10-200 nm |
| Quantum yield | 0-1 |
| Lifetime (fluorescence) | 1-100 ns |
| Lifetime (phosphorescence) | 1 ms-10 s |
| Detection limit | pg-ng |

---

## Cross-References
- UV-Vis Spectroscopy: [uv_vis_spectroscopy.md](./uv_vis_spectroscopy.md)
- Spectroscopic Methods: [spectroscopic_methods.md](./spectroscopic_methods.md)
