---
id: microscopy.reference
layer: 4
title: Microscopy Parameters Reference
stability: high
source: LibreTexts Instrumental Analysis + Standard Tables
---

# Microscopy Parameters Reference

## 1. Electron Wavelengths at Common Voltages

| Voltage (kV) | Non-relativistic λ (pm) | Relativistic λ (pm) | Error (%) |
|--------------|-------------------------|---------------------|-----------|
| 50 | 5.49 | 5.36 | 2.4% |
| 80 | 4.34 | 4.18 | 3.8% |
| 100 | 3.88 | 3.70 | 4.9% |
| 120 | 3.55 | 3.35 | 6.0% |
| 200 | 2.74 | 2.51 | 9.2% |
| 300 | 2.24 | 1.96 | 14.3% |
| 400 | 1.94 | 1.64 | 18.3% |
| 1000 | 1.23 | 0.87 | 41.4% |

**Rule of thumb**: Use relativistic correction for V > 100 kV

---

## 2. SEM Typical Parameters

### 2.1 Operating Voltages

| Application | Voltage Range | Notes |
|-------------|---------------|-------|
| Biological (coated) | 5-15 kV | Minimize beam damage |
| Biological (uncoated) | 1-5 kV | Low voltage, surface imaging |
| Materials (metals) | 15-30 kV | Standard conditions |
| High resolution | 25-40 kV | Small interaction volume |
| Low vacuum/Environmental | 10-30 kV | Variable pressure mode |

### 2.2 Resolution vs Voltage

| Voltage (kV) | Theoretical Resolution (nm) | Practical Resolution (nm) |
|--------------|----------------------------|---------------------------|
| 5 | ~33 | 5-10 |
| 10 | ~24 | 3-5 |
| 20 | ~17 | 1-3 |
| 30 | ~14 | 0.8-1.5 |

*(Assumes α = 0.01 rad, practical limits from lens aberrations)*

### 2.3 Working Distance Effects

| Working Distance | Depth of Field | Resolution | Use Case |
|------------------|----------------|------------|----------|
| Short (5-10 mm) | Low | High | High magnification |
| Medium (10-15 mm) | Medium | Good | General purpose |
| Long (15-25 mm) | High | Lower | Rough samples, EDS |

---

## 3. TEM Typical Parameters

### 3.1 Resolution by Instrument Type

| Instrument Type | Voltage (kV) | Cs (mm) | Resolution (nm) |
|-----------------|--------------|---------|-----------------|
| Conventional | 100 | 2.0 | 0.3-0.5 |
| High resolution | 200 | 1.0 | 0.15-0.20 |
| Field emission | 200 | 0.5 | 0.10-0.12 |
| Cs-corrected | 200 | <0.1 | <0.08 |
| Aberration-corrected | 300 | ~0 | <0.05 |

### 3.2 Sample Thickness Guidelines

| Voltage (kV) | Light elements (Z<20) | Medium (20<Z<50) | Heavy (Z>50) |
|--------------|----------------------|------------------|--------------|
| 100 | 100-200 nm | 50-100 nm | 20-50 nm |
| 200 | 200-500 nm | 100-200 nm | 50-100 nm |
| 300 | 300-800 nm | 150-300 nm | 80-150 nm |

---

## 4. AFM Parameters

### 4.1 Cantilever Spring Constants

| Mode | k (N/m) | Resonant Freq (kHz) | Application |
|------|---------|---------------------|-------------|
| Contact | 0.01-1 | 10-100 | Soft samples, liquid |
| Tapping | 1-100 | 50-500 | General, biological |
| Non-contact | 1-50 | 200-500 | UHV, high resolution |

### 4.2 Tip Parameters

| Tip Type | Radius (nm) | Material | Aspect Ratio |
|----------|-------------|----------|--------------|
| Standard | 5-20 | Si, Si₃N₄ | ~1:1 |
| High resolution | 1-5 | Si | ~1:1 |
| Super-sharp | <1 | CNT, W spike | >10:1 |
| Colloidal | 20-10000 | SiO₂, PS | N/A |

### 4.3 Force Detection Limits

| Parameter | Value | Units |
|-----------|-------|-------|
| Minimum force | 10⁻¹² | N (pN) |
| Typical contact force | 10⁻⁹-10⁻⁶ | N (nN-μN) |
| Vertical resolution | 0.01 | nm |
| Lateral resolution | 0.1-1 | nm |

---

## 5. STM Parameters

### 5.1 Operating Conditions

| Parameter | Typical Range | Notes |
|-----------|---------------|-------|
| Bias voltage | 0.01-2 V | Sample-tip polarity determines direction |
| Tunneling current | 0.01-10 nA | Lower = gentler |
| Tip-sample distance | 0.4-1.0 nm | Not directly measured |
| Scan speed | 10-1000 nm/s | Depends on resolution needed |

### 5.2 Decay Constants by Material

| Material | Work Function φ (eV) | κ (nm⁻¹) |
|----------|---------------------|----------|
| Au | 5.1 | 10.3 |
| Pt | 5.6 | 10.8 |
| W | 4.5 | 9.7 |
| Si | 4.8 | 10.0 |
| Graphite | 4.6 | 9.8 |

*κ = √(2mφ)/ℏ ≈ 10 nm⁻¹ for typical metals*

### 5.3 Resolution

| Type | Typical | Best |
|------|---------|------|
| Vertical | 0.01 nm | 0.001 nm |
| Lateral | 0.1 nm | 0.05 nm |
| Atomic | Yes | Individual atoms visible |

---

## 6. Optical Microscopy Parameters

### 6.1 Numerical Aperture by Objective Type

| Objective | NA (dry) | NA (oil) | Resolution (nm, 550 nm light) |
|-----------|----------|----------|------------------------------|
| 10× | 0.25 | - | 1100 |
| 20× | 0.40 | - | 690 |
| 40× | 0.65 | 0.95 | 290 |
| 60× | 0.80 | 1.0 | 275 |
| 100× | 0.90 | 1.4 | 196 |

### 6.2 Depth of Field

| NA | DOF at 550 nm (nm) |
|----|-------------------|
| 0.25 | 4400 |
| 0.40 | 1700 |
| 0.65 | 650 |
| 0.95 | 300 |
| 1.4 | 140 |

---

## 7. Physical Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Planck constant | h | 6.62607015 × 10⁻³⁴ | J·s |
| Reduced Planck | ℏ | 1.054571817 × 10⁻³⁴ | J·s |
| Electron mass | m_e | 9.1093837015 × 10⁻³¹ | kg |
| Electron charge | e | 1.602176634 × 10⁻¹⁹ | C |
| Speed of light | c | 2.99792458 × 10⁸ | m/s |
| Electron rest energy | m_e c² | 510.998950 | keV |
| Atomic mass unit | u | 1.66053906660 × 10⁻²⁷ | kg |

---

## 8. Unit Conversions

| From | To | Multiply by |
|------|-----|-------------|
| eV | J | 1.602 × 10⁻¹⁹ |
| nm | Å | 10 |
| pm | Å | 0.01 |
| N/m | pN/nm | 1 |
| kV | V | 1000 |

---

## 9. Wavelength Quick Reference

### Light

| Color | λ (nm) | Energy (eV) |
|-------|--------|-------------|
| Violet | 400 | 3.10 |
| Blue | 470 | 2.64 |
| Green | 550 | 2.25 |
| Yellow | 580 | 2.14 |
| Red | 700 | 1.77 |

### Electrons

| Voltage | λ (pm) | Use Case |
|---------|--------|----------|
| 10 kV | 12.2 | Low-voltage SEM |
| 30 kV | 7.1 | Standard SEM |
| 100 kV | 3.7 | TEM |
| 200 kV | 2.5 | High-res TEM |
| 300 kV | 2.0 | Ultra-high res TEM |
