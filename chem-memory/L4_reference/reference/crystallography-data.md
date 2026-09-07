---
id: crystallography.data
layer: 4
title: Crystallography Reference Data
up_links:
  - ../../L2_principles/crystallography.md
source:
  - LibreTexts Chemistry
  - Standard crystallographic tables
---

## Crystal Systems Reference

### Seven Crystal Systems

| System | Edge Lengths | Angles | Required Parameters | Bravais Lattices |
|--------|--------------|--------|---------------------|------------------|
| Cubic | a = b = c | α = β = γ = 90° | 1 (a) | P, I, F |
| Tetragonal | a = b ≠ c | α = β = γ = 90° | 2 (a, c) | P, I |
| Orthorhombic | a ≠ b ≠ c | α = β = γ = 90° | 3 (a, b, c) | P, I, F, C |
| Hexagonal | a = b ≠ c | α = β = 90°, γ = 120° | 2 (a, c) | P |
| Rhombohedral | a = b = c | α = β = γ ≠ 90° | 2 (a, α) | P (R) |
| Monoclinic | a ≠ b ≠ c | α = γ = 90°, β ≠ 90° | 4 (a, b, c, β) | P, C |
| Triclinic | a ≠ b ≠ c | α ≠ β ≠ γ | 6 (a, b, c, α, β, γ) | P |

### d-Spacing Formulas

**Cubic:**
```
d_hkl = a / √(h² + k² + l²)
```

**Tetragonal:**
```
1/d² = (h² + k²)/a² + l²/c²
```

**Orthorhombic:**
```
1/d² = h²/a² + k²/b² + l²/c²
```

**Hexagonal:**
```
1/d² = (4/3)[(h² + hk + k²)/a²] + l²/c²
```

**Rhombohedral:**
```
1/d² = [(h² + k² + l²) sin²α + 2(hk + kl + hl)(cos²α - cosα)] / [a²(1 - 3cos²α + 2cos³α)]
```

**Monoclinic:**
```
1/d² = [h²/a² + k²sin²β/b² + l²/c² - 2hl cosβ/(ac)] / sin²β
```

### Unit Cell Volume Formulas

| System | Volume Formula |
|--------|---------------|
| Cubic | V = a³ |
| Tetragonal | V = a²c |
| Orthorhombic | V = abc |
| Hexagonal | V = (√3/2)a²c ≈ 0.866 × a²c |
| Monoclinic | V = abc sin(β) |
| Rhombohedral | V = a³√(1 - 3cos²α + 2cos³α) |
| Triclinic | V = abc√(1 - cos²α - cos²β - cos²γ + 2cosα cosβ cosγ) |

---

## Common Crystal Structures

### Cubic Structures

| Structure | Atoms/Cell | Coordination | Packing Fraction | Examples |
|-----------|------------|--------------|------------------|----------|
| Simple Cubic (SC) | 1 | 6 | 0.524 (52.4%) | Po |
| Body-Centered Cubic (BCC) | 2 | 8 | 0.680 (68.0%) | Fe, W, Cr, Na |
| Face-Centered Cubic (FCC) | 4 | 12 | 0.740 (74.0%) | Cu, Al, Au, Ag, Ni |
| Diamond | 8 | 4 | 0.340 (34.0%) | C, Si, Ge |

### Atomic Radius Relationships

| Structure | Formula | Derivation |
|-----------|---------|------------|
| Simple Cubic | r = a/2 | Atoms touch along edge |
| BCC | r = a√3/4 | Atoms touch along body diagonal |
| FCC | r = a√2/4 | Atoms touch along face diagonal |

### Close Packing

| Structure | Stacking | Coordination | Packing |
|-----------|----------|--------------|---------|
| HCP | ABAB... | 12 | 74% |
| FCC (CCP) | ABCABC... | 12 | 74% |

---

## X-ray Sources

| Target | Kα Wavelength (Å) | Common Uses |
|--------|------------------|-------------|
| Cu | 1.5418 | General powder diffraction |
| Mo | 0.7107 | Single crystal, small molecules |
| Cr | 2.2910 | Stress analysis |
| Co | 1.7903 | Steel analysis |
| Fe | 1.9373 | Stress analysis |

---

## Physical Constants

| Constant | Value | Units |
|----------|-------|-------|
| Avogadro's Number (N_A) | 6.02214076 × 10²³ | mol⁻¹ |
| 1 Å | 10⁻¹⁰ | m |
| 1 Å³ | 10⁻²⁴ | cm³ |

---

## Miller Indices Quick Reference

### Special Planes (Cubic)

| Miller Indices | Plane Description |
|----------------|-------------------|
| (100) | Face perpendicular to x-axis |
| (010) | Face perpendicular to y-axis |
| (001) | Face perpendicular to z-axis |
| (110) | Face diagonal plane |
| (111) | Body diagonal (octahedral) plane |
| (210) | General plane |

### Conversion Rules

1. **Intercepts → Miller indices:**
   - Find intercepts (in units of a, b, c)
   - Take reciprocals
   - Clear fractions → smallest integers

2. **Miller indices → Intercepts:**
   - Take reciprocal of each index
   - Multiply by lattice parameters

---

## Example Calculations

### Example 1: d-spacing for (111) in FCC Cu (a = 3.615 Å)

```
d_111 = a / √(1² + 1² + 1²)
d_111 = 3.615 / √3
d_111 = 3.615 / 1.732
d_111 = 2.087 Å
```

### Example 2: Bragg angle for Cu Kα (λ = 1.5418 Å), d = 2.0 Å

```
sin(θ) = nλ / (2d)
sin(θ) = 1 × 1.5418 / (2 × 2.0)
sin(θ) = 0.3855
θ = arcsin(0.3855) = 22.67°
```

### Example 3: Density of FCC Ni

Given: a = 3.524 Å, M = 58.69 g/mol

```
V = a³ = 43.78 Å³ = 43.78 × 10⁻²⁴ cm³
n = 4 atoms (FCC)

ρ = (4 × 58.69) / (43.78 × 10⁻²⁴ × 6.022 × 10²³)
ρ = 234.76 / 26.37
ρ = 8.90 g/cm³
```
