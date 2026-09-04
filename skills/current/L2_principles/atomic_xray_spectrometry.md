---
id: atomic_xray_spectrometry
layer: 2
title: Atomic X-Ray Spectrometry (XRF and XRD)
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - 
cross_links:
  - ./crystallography.md
  - ./atomic_absorption_spectroscopy.md
source: Skoog Instrumental Analysis Ch12 (LibreTexts)
---

## Context

X-ray spectrometry includes X-ray Fluorescence (XRF) for elemental analysis and X-ray Diffraction (XRD) for crystal structure determination. These non-destructive techniques are essential in materials science, geology, archaeology, and quality control.

---

## Part 1: X-Ray Fluorescence (XRF)

### Fundamental Principles

#### X-ray Generation

When inner shell electrons are ejected, outer electrons fill vacancies:

```
Kα: L → K transition
Kβ: M → K transition
Lα: M → L transition
```

#### Characteristic X-ray Energy

**Moseley's Law:**
```
√ν = a(Z - b)
E = hν
```

Where:
- ν = X-ray frequency
- Z = atomic number
- a, b = constants

#### Energy-Wavelength Relationship

```
E(keV) = 12.398/λ(Å)
```

### XRF Process

1. Primary X-rays eject inner shell electrons
2. Vacancy created in inner shell
3. Outer electron fills vacancy
4. Characteristic X-ray emitted
5. Energy identifies element

### Instrumentation

#### Wavelength Dispersive XRF (WDXRF)

- Crystal analyzer separates wavelengths by diffraction
- High resolution
- Better for light elements
- Sequential analysis

**Bragg's Law:**
```
nλ = 2d sinθ
```

#### Energy Dispersive XRF (EDXRF)

- Semiconductor detector measures energy
- Simultaneous multi-element
- Faster analysis
- Lower resolution

### Quantitative Analysis

#### Fundamental Parameters Method

```
I_i = I_0 × C_i × (μ_i/μ_total) × (1 - exp(-μ_total × ρ × t))
```

Where:
- I_i = intensity for element i
- C_i = concentration
- μ = mass absorption coefficients

#### Matrix Effects

| Effect | Description | Correction |
|--------|-------------|------------|
| Absorption | Primary X-rays absorbed | Mathematical correction |
| Enhancement | Secondary fluorescence | Empirical correction |
| Particle size | Heterogeneity | Grinding, fusion |

### Detection Limits

| Atomic Number | Detection Limit |
|---------------|-----------------|
| Na-Ca (Z=11-20) | 10-100 ppm |
| Ti-Zn (Z=22-30) | 1-10 ppm |
| Sr-Zr (Z=38-40) | 1-5 ppm |
| Heavy elements | 1-10 ppm |

### Applications

- Mining and geology
- Metal analysis
- Environmental monitoring
- Art and archaeology
- Pharmaceutical (heavy metals)

---

## Part 2: X-Ray Diffraction (XRD)

### Fundamental Principles

#### Bragg's Law

```
nλ = 2d sinθ
```

Where:
- n = order of diffraction
- λ = X-ray wavelength
- d = interplanar spacing
- θ = Bragg angle

#### Miller Indices

Crystal planes designated by (hkl):
```
d_hkl = a/√(h² + k² + l²)  (cubic)
```

### XRD Instrumentation

#### Powder Diffractometer

- Bragg-Brentano geometry
- Cu Kα radiation (λ = 1.5418 Å)
- 2θ scan

#### Components

1. **X-ray tube**
   - Cu, Mo, Co targets
   - 20-60 kV, 10-50 mA

2. **Goniometer**
   - Precise angle measurement
   - θ-2θ or θ-θ geometry

3. **Detector**
   - Scintillation counter
   - Solid-state detector

### Phase Identification

**Peak positions** → d-spacings → Crystal structure
**Peak intensities** → Phase amounts (quantitative)

### Pattern Matching

1. Measure 2θ and intensities
2. Calculate d-spacings
3. Compare to databases (ICDD PDF)
4. Identify phases

### Quantitative Analysis

#### Internal Standard Method

```
C_i = (I_i/I_s) × K × C_s
```

#### Rietveld Refinement

Full-pattern fitting for:
- Phase quantification
- Crystal structure refinement
- Lattice parameters

### Applications

- Phase identification
- Crystallinity measurement
- Lattice parameter determination
- Stress/strain analysis
- Texture analysis

---

## Problem-Solving Examples

### Example 1: Bragg Angle Calculation

**Problem**: Calculate the Bragg angle for the (111) reflection of NaCl using Cu Kα radiation (λ = 1.5418 Å). NaCl has a = 5.64 Å.

**Solution:**
```
d_111 = a/√(1² + 1² + 1²) = 5.64/√3 = 3.256 Å

nλ = 2d sinθ (n = 1)
sinθ = λ/(2d) = 1.5418/(2 × 3.256) = 0.237
θ = 13.7°
2θ = 27.4°
```

### Example 2: XRF Calibration

**Problem**: Standard gives I_Fe = 5000 cps for 1% Fe. Unknown gives 2000 cps. Find Fe concentration.

**Solution:**
```
C_unknown = (I_unknown/I_standard) × C_standard
C_unknown = (2000/5000) × 1% = 0.4%
```

### Example 3: Wavelength-Energy Conversion

**Problem**: Mo Kα has λ = 0.7107 Å. Calculate its energy in keV.

**Solution:**
```
E(keV) = 12.398/λ(Å) = 12.398/0.7107 = 17.44 keV
```

### Example 4: Crystallite Size (Scherrer Equation)

**Problem**: A peak at 2θ = 30° has FWHM = 0.5° (Cu Kα). Calculate crystallite size.

**Solution:**
```
Scherrer equation: D = Kλ/(β cosθ)

K = 0.9 (shape factor)
λ = 1.5418 Å
β = 0.5° × π/180 = 0.00873 rad
θ = 15°

D = 0.9 × 1.5418/(0.00873 × cos15°)
D = 1.387/(0.00873 × 0.966)
D = 165 Å = 16.5 nm
```

---

## Decision Flow

1. **Choose technique:**
   - Need elemental analysis? → XRF
   - Need phase identification? → XRD
   - Both needed? → Combined XRF/XRD

2. **Select XRF mode:**
   - Light elements (Na-Ca)? → WDXRF
   - Many elements simultaneously? → EDXRF
   - Field analysis? → Portable XRF

3. **Select XRD mode:**
   - Powder sample? → Powder diffractometer
   - Single crystal? → Single-crystal diffractometer
   - Thin film? → Grazing incidence XRD

---

## Quick Reference - Characteristic X-rays

| Element | Kα (keV) | Kα (Å) |
|---------|----------|--------|
| Fe | 6.40 | 1.937 |
| Cu | 8.04 | 1.542 |
| Mo | 17.44 | 0.711 |
| Ag | 22.16 | 0.560 |

---

## Comparison Table

| Parameter | WDXRF | EDXRF | XRD |
|-----------|-------|-------|-----|
| Information | Elemental | Elemental | Structural |
| Resolution | High | Moderate | High |
| Speed | Slow | Fast | Moderate |
| Light elements | Better | Limited | N/A |
| Sample prep | Moderate | Minimal | Moderate |

---

## Cross-References
- Crystallography: [crystallography.md](./crystallography.md)
- Atomic Absorption: [atomic_absorption_spectroscopy.md](./atomic_absorption_spectroscopy.md)
