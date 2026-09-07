---
id: chem.tunneling_data
layer: 4
title: Quantum Tunneling Reference Data
source: Quantum States of Atoms and Molecules (Zielinski et al.); Standard references
status: active
created: 2026-03-21
---

# Quantum Tunneling Reference Data

## 1. Typical Barrier Parameters

### Chemical Reaction Barriers

| Reaction Type | Barrier Height (kJ/mol) | Barrier Width (Å) | Notes |
|---------------|------------------------|-------------------|-------|
| Proton transfer (H-bond) | 20-50 | 0.5-1.0 | Low barrier, significant tunneling |
| Proton transfer (enzyme) | 10-30 | 0.4-0.8 | Enzyme active sites enhance tunneling |
| Electron transfer | 10-100 | 5-15 | Through space/solvent |
| Hydrogen abstraction | 30-80 | 0.8-1.2 | Heavy atom motion coupled |
| C-C bond formation | 100-200 | 1.0-1.5 | High barrier, tunneling negligible |
| Ammonia inversion | 24 | 0.4 | Classic tunneling example |
| α-decay (nuclear) | 20-30 MeV | 10-30 fm | Nuclear tunneling |

### Scanning Tunneling Microscopy (STM)

| Parameter | Typical Value | Notes |
|-----------|--------------|-------|
| Work function (Au) | 5.1-5.5 eV | Barrier height ~5 eV |
| Work function (Pt) | 5.6-6.0 eV | |
| Work function (Si) | 4.6-5.2 eV | |
| Tip-sample distance | 3-10 Å | Barrier width |
| Tunneling current | 0.1-10 nA | Exponential with distance |
| Decay constant (Au) | ~1 Å⁻¹ | dI/dz ≈ 1 nA/Å |

---

## 2. Transmission Coefficients (Reference Values)

### Electron Tunneling (m = mₑ)

| V₀ (eV) | E (eV) | Width (Å) | T (exact) | Notes |
|---------|--------|-----------|-----------|-------|
| 2.0 | 1.0 | 5.0 | 2.35×10⁻² | STM-like conditions |
| 2.0 | 1.0 | 10.0 | 5.55×10⁻⁴ | Double width |
| 5.0 | 1.0 | 5.0 | 1.27×10⁻⁵ | Higher barrier |
| 5.0 | 4.0 | 5.0 | 4.75×10⁻² | Near barrier top |
| 1.0 | 0.5 | 3.0 | 1.12×10⁻¹ | Thin barrier |

### Proton Tunneling (m = 1.0078 amu)

| V₀ (kJ/mol) | E (kJ/mol) | Width (Å) | T (WKB) | Notes |
|-------------|------------|-----------|---------|-------|
| 20 | 0 | 0.5 | 4.9×10⁻⁹ | Low barrier |
| 20 | 0 | 1.0 | 2.4×10⁻¹⁷ | Double width |
| 50 | 0 | 0.5 | 2.2×10⁻²³ | Higher barrier |
| 50 | 25 | 0.5 | 1.5×10⁻¹¹ | Half barrier height |

### Deuteron Tunneling (m = 2.0141 amu)

| V₀ (kJ/mol) | E (kJ/mol) | Width (Å) | T (WKB) | KIE (H/D) |
|-------------|------------|-----------|---------|-----------|
| 20 | 0 | 0.5 | 2.2×10⁻¹³ | ~2×10⁴ |
| 50 | 0 | 0.5 | ~0 | Enormous |

---

## 3. Kinetic Isotope Effects (KIE) from Tunneling

### Experimental H/D KIE Values

| Reaction | Temperature (K) | Observed KIE | Classical Prediction | Tunneling Contribution |
|----------|-----------------|--------------|---------------------|------------------------|
| H abstraction by CH₃• | 298 | 7.1 | 6-7 | Moderate |
| H abstraction by •OH | 298 | 1.4 | 1.2 | Small |
| Proton transfer in enzyme | 298 | 50-100 | 7-10 | Dominant |
| Aromatic proton exchange | 298 | 5-10 | 5-7 | Moderate |
| Hydride transfer (NADH) | 298 | 3-5 | 2-3 | Moderate |
| Ammonia inversion | 200 | 1.2 | ~1 | Small (barrier too low) |

### Swain-Schaad Exponents

For tunneling analysis: (k_H/k_T) = (k_H/k_D)^n

| Mechanism | Expected n | Interpretation |
|-----------|------------|----------------|
| Classical | ~1.44 | Zero-point energy only |
| Semi-classical tunneling | 1.5-2.0 | Moderate tunneling |
| Deep tunneling | >3.0 | Dominant tunneling |
| Coupled motion | Variable | Complex |

---

## 4. Decay Constants (κ)

### Definition
κ = √(2m(V₀-E))/ℏ

### Reference Values

| Particle | Mass (amu) | V₀-E (kJ/mol) | κ (Å⁻¹) | κ (m⁻¹) |
|----------|------------|---------------|---------|---------|
| Electron | 5.49×10⁻⁴ | 50 | 0.114 | 1.14×10⁹ |
| Electron | 5.49×10⁻⁴ | 100 | 0.161 | 1.61×10⁹ |
| Proton | 1.0078 | 10 | 4.54 | 4.54×10¹⁰ |
| Proton | 1.0078 | 50 | 10.15 | 1.02×10¹¹ |
| Deuteron | 2.0141 | 10 | 6.42 | 6.42×10¹⁰ |
| Deuteron | 2.0141 | 50 | 14.36 | 1.44×10¹¹ |
| α-particle | 4.00 | 100 | 28.7 | 2.87×10¹¹ |

---

## 5. Tunneling Rate Corrections

### Bell Correction Factors (κ_Bell)

For proton transfer, V₀ = 30 kJ/mol, a = 0.6 Å:

| T (K) | κ_Bell | Interpretation |
|-------|--------|----------------|
| 100 | 5.2 | Strong tunneling |
| 150 | 2.8 | Significant tunneling |
| 200 | 1.9 | Moderate tunneling |
| 250 | 1.5 | Small tunneling |
| 298 | 1.3 | Minor tunneling |
| 400 | 1.2 | Negligible tunneling |

### Wigner Correction (κ_Wigner)

κ_Wigner = 1 + (ℏω‡/24kBT)²

For ω‡ = 2000 cm⁻¹ (imaginary frequency):

| T (K) | ℏω‡/kT | κ_Wigner |
|-------|--------|----------|
| 100 | 28.8 | 35.5 |
| 200 | 14.4 | 9.6 |
| 298 | 9.6 | 4.8 |
| 400 | 7.2 | 3.2 |

---

## 6. Classical Turning Points for QHO

For a harmonic oscillator, classical turning points: x_t = √((2v+1)ℏ/(mω))

### CO Molecule (ν = 2170 cm⁻¹, μ = 6.86 amu)

| v | Energy (cm⁻¹) | x_t (pm) | P(forbidden) |
|---|---------------|----------|--------------|
| 0 | 1085 | 32.5 | 0.157 |
| 1 | 3255 | 56.3 | 0.112 |
| 2 | 5425 | 73.5 | 0.095 |
| 3 | 7595 | 87.7 | 0.086 |

### H₂ Molecule (ν = 4401 cm⁻¹, μ = 0.50 amu)

| v | Energy (cm⁻¹) | x_t (pm) | P(forbidden) |
|---|---------------|----------|--------------|
| 0 | 2200 | 31.5 | 0.157 |
| 1 | 6602 | 54.6 | 0.112 |
| 2 | 11003 | 71.2 | 0.095 |

---

## 7. Nuclear Alpha Decay Data

### Gamow Factor

The transmission probability for α-decay involves the Gamow factor:
G = 2πZ_dZ_αe²/(ℏv)

### Example: ²³⁸U → ²³⁴Th + α

| Parameter | Value |
|-----------|-------|
| Barrier height | 27 MeV |
| α energy | 4.27 MeV |
| Barrier width (inner) | ~9 fm |
| Barrier width (outer) | ~30 fm |
| Tunneling probability | ~10⁻³⁸ |
| Half-life | 4.5×10⁹ years |

---

## 8. STM Parameters

### Tunneling Current Formula

I ∝ exp(-2κd) where κ = √(2mφ)/ℏ

For φ = 5 eV (gold): κ ≈ 1.0 Å⁻¹

| d (Å) | Relative I |
|-------|------------|
| 3 | 0.0025 |
| 5 | 4.5×10⁻⁵ |
| 7 | 8.2×10⁻⁷ |
| 10 | 4.5×10⁻⁹ |

**Practical implication:** Current changes by ~1 order of magnitude per Å distance change.

---

## 9. Physical Constants Used

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Planck constant | h | 6.626×10⁻³⁴ | J·s |
| Reduced Planck constant | ℏ | 1.055×10⁻³⁴ | J·s |
| Electron mass | mₑ | 9.109×10⁻³¹ | kg |
| Atomic mass unit | amu | 1.661×10⁻²⁷ | kg |
| Boltzmann constant | kB | 1.381×10⁻²³ | J/K |
| Electron charge | e | 1.602×10⁻¹⁹ | C |
| Electron-volt | eV | 1.602×10⁻¹⁹ | J |

---

## Related Files

- L2: `../L2_principles/quantum_tunneling.md` — Principles and formulas
- L3: `../L3_implementation/code/tunneling_calculator.py` — Calculator functions
- L5: `../L5_examples/tunneling_worked_problems.md` — Worked examples
