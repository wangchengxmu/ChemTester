# Tanabe-Sugano Diagrams

## Overview

Tanabe-Sugano diagrams predict electronic transition energies for transition metal complexes. They work for both:
- Spin-allowed and spin-forbidden transitions
- Strong field (low-spin) and weak field (high-spin) complexes

**Source:** CHM 320 Chapter 9.3 (LibreTexts)

---

## Background Theory

### Crystal Field Splitting Energy
Within Crystal Field Theory, the interaction of metal and ligand arises from electrostatic repulsion. In an octahedral complex:
- d_x²-y² and d_z² are raised in energy relative to d_xy, d_xz, d_yz
- This energy split is called Δ_oct
- Tetrahedral splitting: Δ_t ≈ (4/9)Δ_oct

### Racah Parameters
Parameters describing electron-electron repulsion:
- **A:** Roughly constant for all metal centers (often ignored)
- **B:** Bond strength parameter (electron repulsion)
- **C:** Usually approximated as C ≈ B/4

#### Nephelauxetic Ratio
```
β = B_complex / B_free ion
```
Measures the reduction in electron-electron repulsion due to metal-ligand bonding.

---

## Reading Tanabe-Sugano Diagrams

### Axes
- **X-axis:** Δ_oct/B (ligand field strength, scaled by Racah parameter)
- **Y-axis:** E/B (transition energy, scaled by Racah parameter)

### Key Features

1. **Each line = one electronic state**
   - Lines show how state energy changes with ligand field strength
   - Term symbols labeled on each line

2. **Vertical discontinuity (d^4-d^7 only)**
   - Marks high-spin → low-spin transition
   - At this point: Δ_oct = P (pairing energy)
   - Left side: high-spin
   - Right side: low-spin

3. **Ground state = horizontal line at E/B = 0**

---

## Available Diagrams (d^2 - d^8)

| d^n | Ground State | Key Features |
|-----|--------------|--------------|
| d^2 | ^3T_1g | No spin crossover |
| d^3 | ^4A_2g | No spin crossover |
| d^4 | ^5E_g (HS) → ^3T_1g (LS) | Spin crossover |
| d^5 | ^6A_1g (HS) → ^2T_2g (LS) | Spin crossover |
| d^6 | ^5T_2g (HS) → ^1A_1g (LS) | Spin crossover |
| d^7 | ^4T_1g (HS) → ^2E_g (LS) | Spin crossover |
| d^8 | ^3A_2g | No spin crossover |

---

## Step-by-Step Usage

### Step 1: Determine d-configuration
```
d^n = atomic d electrons - oxidation state
```

### Step 2: Get spectroscopic data
- Measure UV-Vis spectrum
- Identify λ_max for transitions (strong = spin-allowed, weak = spin-forbidden)

### Step 3: Convert to wavenumbers
```
ν̃ (cm^-1) = 10^7 / λ_max (nm)
```

### Step 4: Calculate energy ratios
```
Ratio = E_n / E_1 (relative to lowest allowed transition)
```

### Step 5: Find Δ_oct/B on diagram
- Slide ruler perpendicular to x-axis
- Find position where E/B ratios match experimental ratios

### Step 6: Calculate Δ_oct
```
Δ_oct = (Δ_oct/B) × B
where B = E_measured / (E/B from diagram)
```

---

## Worked Example: Cr³⁺ Complex

### Problem
A Cr³⁺ complex has transitions at:
- 431.03 nm (strong)
- 781.25 nm (strong)
- 1,250 nm (strong)

Find Δ_oct.

### Solution

**Step 1:** Cr has 6 electrons, Cr³⁺ has 3 → d³ configuration

**Step 2:** Use d³ Tanabe-Sugano diagram

**Step 3:** Convert to wavenumbers:
```
ν̃_1 = 10^7/1250 = 8,000 cm^-1
ν̃_2 = 10^7/781.25 = 13,600 cm^-1
ν̃_3 = 10^7/431.03 = 23,200 cm^-1
```

**Step 4:** Identify transitions and calculate ratios:
| Transition | Energy (cm^-1) | Ratio to lowest |
|------------|----------------|-----------------|
| ^4T_2g ← ^4A_2g | 8,000 | 1.0 |
| ^4T_1g ← ^4A_2g | 13,600 | 1.7 |
| ^4T_1g ← ^4A_2g | 23,200 | 2.9 |

**Step 5:** Find Δ_oct/B:
Looking at d³ diagram, E/B ratios match at Δ_oct/B = 10

**Step 6:** Calculate B:
```
B = E_measured / (E/B from diagram)
B = 8,000 / 10 = 800 cm^-1
```

**Step 7:** Calculate Δ_oct:
```
Δ_oct = 10 × 800 = 8,000 cm^-1
```

---

## Selection Rules

### Spin-Allowed Transitions
- ΔS = 0 (no spin change)
- More intense bands

### Spin-Forbidden Transitions
- ΔS ≠ 0 (spin changes)
- Weak bands, but can appear due to spin-orbit coupling

### Laporte Rule
- g ↔ g transitions forbidden in centrosymmetric complexes
- Intensity gained through vibronic coupling

---

## Applications

### 1. Determining Δ_oct from Spectrum
Primary use - extract crystal field splitting from experimental data

### 2. Predicting Colors
Different ligands → different Δ_oct → different colors

### 3. Understanding Spectrochemical Series
Use nephelauxetic ratio to compare ligand effects:
```
Stronger field → larger Δ_oct/B on x-axis
```

### 4. Spin State Determination
For d^4-d^7: determine if high-spin or low-spin from transition pattern

---

## Limitations

1. **Assumes octahedral symmetry**
   - Real complexes may have distortions

2. **Ignores Jahn-Teller effects**
   - Can cause additional splitting

3. **Parameter B varies**
   - B_complex ≠ B_free ion
   - Must use nephelauxetic ratio

4. **Only for dn configurations**
   - Not applicable to d^0, d^1, d^9, d^10 (no diagrams needed)

---

## Related Topics
- [[crystal_field_theory]] - LFSE and Δ_oct concepts
- [[magnetic_properties]] - Spin states and magnetism
- [[electronic_spectroscopy]] - UV-Vis spectroscopy of complexes
- [[symmetry_group_theory]] - Term symbols from group theory

## References
- Tanabe, Sugano (1954). J. Phys. Soc. Japan 9: 753-766, 766-779
- Tanabe, Sugano (1956). J. Phys. Soc. Japan 11: 864-877
- CHM 320 Chapter 9.3 (LibreTexts)

## L4 Reference Data
→ `../L4_reference/tanabe_sugano_parameters.csv`

## L5 Examples
→ `../L5_examples/tanabe_sugano_examples.md

## L3 Tool Call Directives

**Source:** `tanabe_sugano_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
