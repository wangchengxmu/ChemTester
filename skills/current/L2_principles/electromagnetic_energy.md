---
id: chem.electromagnetic_energy
layer: 2
title: Electromagnetic Energy and Light
source: LibreTexts Chemistry 2e Ch06.01
status: active
created: 2026-03-11
last_verified: 2026-03-11
---

# Electromagnetic Energy and Light

## Problem type
Calculate wavelength, frequency, and energy of electromagnetic radiation; apply photoelectric effect.

## Decision tree

1. **What is asked?**
   - Wavelength from frequency → Use c = λν
   - Frequency from wavelength → Use c = λν
   - Photon energy → Use E = hν or E = hc/λ
   - Photoelectric effect → Use E_k = hν - φ

2. **Units?**
   - λ in m (convert nm: 1 nm = 10⁻⁹ m)
   - ν in Hz (s⁻¹)
   - E in J

3. **Spectral region?**
   - Compare wavelength to EM spectrum

## Core formulas

### Wave equation
```
c = λ × ν
where:
  c = speed of light = 2.998 × 10⁸ m/s
  λ = wavelength (m)
  ν = frequency (Hz)
```

### Photon energy
```
E = h × ν = h × c / λ
where:
  E = energy (J)
  h = Planck's constant = 6.626 × 10⁻³⁴ J·s
```

### Photoelectric effect
```
E_k = h × ν - φ
where:
  E_k = kinetic energy of ejected electron
  φ = work function (minimum energy to remove electron)
```

## Key constants

| Constant | Value |
|----------|-------|
| Speed of light (c) | 2.998 × 10⁸ m/s |
| Planck's constant (h) | 6.626 × 10⁻³⁴ J·s |
| h × c | 1.986 × 10⁻²⁵ J·m |

## EM Spectrum

| Region | λ (nm) | Energy |
|--------|--------|--------|
| Radio | > 10⁶ | Very low |
| Microwave | 10³ - 10⁶ | Low |
| Infrared | 700 - 10³ | Low |
| Visible | 400 - 700 | Moderate |
| UV | 10 - 400 | High |
| X-ray | 0.01 - 10 | Very high |

## Common patterns
1. Calculate λ from ν (or vice versa)
2. Calculate photon energy from λ
3. Determine if photoelectric effect occurs
4. Identify spectral region

## Links

### L3 Implementation
- `../L3_functions/electromagnetic_energy_tools.py` (TODO)

### L4 Reference

### L5 Examples
- `../L5_examples/quantum-mechanics/ (TODO)

## Source trace
- `../sources/ingestion/source-electronic-structure-stepwise.md` section 6.01