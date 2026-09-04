---
id: uv_vis_spectroscopy
layer: 2
title: UV-Visible Spectroscopy
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/uv_vis_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./spectroscopic_methods.md
  - ./electronic_structure.md
source: Instrumental Analysis (LibreTexts)
---

## Context

UV-Visible spectroscopy measures the absorption of ultraviolet and visible light by molecules. It's one of the most widely used analytical techniques for quantitative analysis, determining concentrations of compounds that absorb in this region. Applications range from environmental monitoring to pharmaceutical analysis.

---

## Fundamental Principles

### Beer-Lambert Law

```
A = εbc
```

Where:
- A = absorbance (dimensionless)
- ε = molar absorptivity (M⁻¹cm⁻¹)
- b = path length (cm)
- c = concentration (M)

### Transmittance Relationship

```
A = -log(T) = log(I₀/I)
```

Where:
- T = transmittance = I/I₀
- I₀ = incident light intensity
- I = transmitted light intensity

### Absorbance and Transmittance Conversions

| Absorbance | % Transmittance | Interpretation |
|------------|-----------------|----------------|
| 0 | 100% | No absorption |
| 0.301 | 50% | 50% light absorbed |
| 1.0 | 10% | 90% light absorbed |
| 2.0 | 1% | 99% light absorbed |

---

## Electronic Transitions

### Types of Transitions

| Transition | Region | Example Compounds |
|------------|--------|-------------------|
| σ → σ* | Vacuum UV | Alkanes |
| n → σ* | UV (150-250 nm) | Alcohols, amines, halides |
| π → π* | UV-Vis (180-300 nm) | Alkenes, aromatics |
| n → π* | UV-Vis (250-350 nm) | Carbonyls, nitro compounds |

### Chromophores

Groups that absorb UV-Vis light:

| Chromophore | λmax (nm) | εmax (M⁻¹cm⁻¹) |
|-------------|-----------|----------------|
| C=C | 175 | 15,000 |
| C≡C | 175 | 8,000 |
| C=O (ketone) | 280 | 20 |
| C=O (aldehyde) | 290 | 20 |
| NO₂ | 270 | 20 |
| Benzene | 255 | 200 |
| Naphthalene | 275 | 5,600 |
| Anthracene | 355 | 9,000 |

### Auxochromes

Groups that modify chromophore absorption:
- **Bathochromic shift (red shift)**: λmax increases
- **Hypsochromic shift (blue shift)**: λmax decreases
- **Hyperchromic effect**: ε increases
- **Hypochromic effect**: ε decreases

---

## Quantitative Analysis

### Calibration Curve

1. Prepare standards of known concentration
2. Measure absorbance at λmax
3. Plot A vs c (should be linear)
4. Use equation: c = (A - intercept) / slope

### Standard Addition Method

For complex matrices:
```
Csample = (Asample / Astd_add) × Cstd_add
```

### Dilution Factor

If sample is diluted:
```
C_original = C_measured × dilution_factor
```

---

## Instrumentation

### Components

| Component | Function |
|-----------|----------|
| Light source | Tungsten (visible), D₂ (UV) |
| Monochromator | Selects wavelength |
| Cuvette | Sample holder (glass/plastic/quartz) |
| Detector | Measures transmitted light |

### Single-Beam vs Double-Beam

| Type | Advantages | Disadvantages |
|------|------------|---------------|
| Single-beam | Simple, lower cost | Requires blank measurement |
| Double-beam | Compensates for source drift | More complex |

### Cuvette Selection

| Material | UV Range | Visible Range |
|----------|----------|---------------|
| Quartz | ✅ (190+ nm) | ✅ |
| Glass | ❌ | ✅ |
| Plastic | ❌ (limited) | ✅ |

---

## Problem-Solving Examples

### Example 1: Beer-Lambert Calculation

**Problem**: A compound has ε = 15,000 M⁻¹cm⁻¹ at 280 nm. What concentration gives A = 0.75 in a 1 cm cuvette?

**Solution:**
```
A = εbc
c = A / (εb) = 0.75 / (15,000 × 1) = 5.0 × 10⁻⁵ M
```

### Example 2: Transmittance to Absorbance

**Problem**: Convert 35% T to absorbance.

**Solution:**
```
A = -log(T) = -log(0.35) = 0.456
```

### Example 3: Concentration from Calibration

**Problem**: A calibration curve has slope = 12,500 M⁻¹ and intercept = 0.02. An unknown has A = 0.425. Find its concentration.

**Solution:**
```
c = (A - intercept) / slope
c = (0.425 - 0.02) / 12,500
c = 3.24 × 10⁻⁵ M
```

---

## Decision Flow

1. **Choose cuvette material:**
   - λ < 300 nm? → Quartz
   - λ > 300 nm? → Glass or plastic OK

2. **Choose wavelength:**
   - Use λmax for maximum sensitivity
   - Avoid wavelengths where solvent absorbs

3. **Calibration method:**
   - Simple matrix? → External standard
   - Complex matrix? → Standard addition

---

## Implementations and Data
- UV-Vis tools: [L3 code](../L3_functions/uv_vis_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)

## L3 Tool Call Directives

**Source:** `uv_vis_tools.py`

Beer-Lambert law, absorbance/transmittance conversions, calibration curves, standard addition, dilution calculations, two-component analysis.

### Available functions:
- `absorbance(epsilon, path_length, concentration)` → float — A = εbc
- `absorbance_from_transmittance(T)` → float — A = -log₁₀(T); T is 0-1
- `transmittance_from_absorbance(A)` → float — T = 10^(-A)
- `percent_transmittance_from_absorbance(A)` → float — %T = 10^(-A) × 100
- `concentration_from_absorbance(A, epsilon, path_length=1.0)` → float — c = A/(εb)
- `molar_absorptivity(A, path_length, concentration)` → float — ε = A/(bc)
- `calibration_curve_params(concentrations, absorbances)` → Tuple[float, float, float] — (slope, intercept, R²)
- `concentration_from_calibration(A, slope, intercept=0.0)` → float — c = (A - intercept)/slope
- `standard_addition_concentration(sample_absorbance, spiked_absorbance, spike_concentration)` → float — Csample
- `dilution_factor(final_volume, initial_volume)` → float — DF = Vf/Vi
- `original_concentration(measured_conc, dilution_factor)` → float — C₀ = Cₘ × DF
- `concentration_two_components(A1, A2, ε1_c1, ε1_c2, ε2_c1, ε2_c2, path_length=1.0)` → Tuple — (c1, c2) via Cramer's rule

### Common errors:
- ❌ Confusing transmittance (0-1) with percent transmittance (0-100%)
- ❌ Optimal absorbance range 0.1–1.0 — values outside have higher relative error
- ❌ Standard addition: spiked absorbance must be higher than sample absorbance
