---
id: non.octahedral.geometries
layer: 2
title: Non-Octahedral Geometries - Tetrahedral and Square Planar
up_links:
  - ../L1_ontology/chemistry-core-map.md
  - ./crystal_field_theory.md
down_links:
  - ../L3_functions/crystal_field_calculator.py
source: CHM 320: Advanced Inorganic Chemistry (LibreTexts), Chapter 8
---

## Context

While octahedral geometry is the most common for 6-coordinate metal complexes, 4-coordinate complexes adopt either tetrahedral or square planar geometries. The d-orbital splitting patterns differ significantly from the octahedral case.

---

## Tetrahedral Geometry

### d-Orbital Splitting Pattern

In tetrahedral geometry, the splitting pattern is **opposite** to octahedral:

| Set | Orbitals | Energy | Relative to Barycenter |
|-----|----------|--------|------------------------|
| **t_2** | d_xy, d_xz, d_yz | **Higher** | +0.4Δ_t |
| **e** | d_x²-y², d_z² | **Lower** | -0.6Δ_t |

```
        ↑ t_2 (3 orbitals) at +0.4Δ_t
        |
   Δ_t  |
        |
        ↓ e (2 orbitals) at -0.6Δ_t
```

### Comparison to Octahedral

| Property | Octahedral | Tetrahedral |
|----------|------------|-------------|
| Upper set | e_g (2 orbitals) | t_2 (3 orbitals) |
| Lower set | t_2g (3 orbitals) | e (2 orbitals) |
| Splitting magnitude | Δ_o | Δ_t = 4/9 Δ_o |

**Key relationship:**
```
Δ_t ≈ (4/9) Δ_o
```

### Why Smaller Splitting?

1. Ligands don't point directly at any d-orbital
2. Weaker electrostatic interaction
3. Less orbital overlap

### Consequences

**Almost always high-spin:**
- Δ_t is small (only 4/9 of octahedral)
- Pairing energy P usually exceeds Δ_t
- Low-spin tetrahedral complexes are extremely rare

---

## Square Planar Geometry

### d-Orbital Splitting Pattern

Square planar geometry has **four distinct energy levels**:

| Orbital | Energy (relative to Δ_o) | Description |
|---------|--------------------------|-------------|
| d_x²-y² | +1.34Δ_o | Highest - points directly at ligands |
| d_xy | +0.23Δ_o | Second highest |
| d_z² | -0.43Δ_o | Below barycenter |
| d_xz, d_yz | -0.52Δ_o each | Lowest - non-bonding |

```
d_x²-y²  ────────── +1.34Δ_o  (highest)
d_xy     ────────── +0.23Δ_o
───────────────────  barycenter
d_z²     ────────── -0.43Δ_o
d_xz,dyz ────────── -0.52Δ_o  (lowest, 2 orbitals)
```

### Derivation from Octahedral

Square planar can be thought of as an octahedron with:
- Two axial ligands removed (along z-axis)
- Results from Jahn-Teller distortion or strong field ligands

### When Does Square Planar Occur?

1. **d^8 metals with strong-field ligands**
   - Ni(II), Pd(II), Pt(II), Au(III)
   - Example: [Ni(CN)_4]^2-, PtCl_2(NH_3)_2

2. **4d and 5d metals**
   - Larger Δ_o favors square planar over tetrahedral

3. **Steric factors**
   - Large ligands may favor square planar arrangement

---

## LFSE Calculations for Different Geometries

### Tetrahedral LFSE Formula

```
LFSE_t = [(0.4 × #t_2 electrons) - (0.6 × #e electrons)] × Δ_t
```

Or in terms of Δ_o:
```
LFSE_t = [(0.178 × #t_2 e^-) - (0.267 × #e e^-)] × Δ_o
```

### Square Planar LFSE Formula

```
LFSE_sp = [(1.34 × n_x²-y²) + (0.23 × n_xy) - (0.43 × n_z²) - (0.52 × n_xz,dyz)] × Δ_o
```

### Example: d^8 Configuration

**Tetrahedral (high-spin):**
```
e^4 t_2^4
LFSE = [(0.4 × 4) - (0.6 × 4)] × Δ_t = [1.6 - 2.4] × Δ_t = -0.8 Δ_t
In Δ_o terms: -0.356 Δ_o
```

**Square Planar (low-spin):**
```
d_xz,dyz^4 d_z²^2 d_xy^2 d_x²-y²^0
LFSE = [0 + 0 - 0.86 - 2.08] × Δ_o = -2.44 Δ_o
```

**Result:** Square planar is strongly favored for low-spin d^8.

---

## Geometry Prediction Guidelines

### Tetrahedral vs Square Planar

| Factor | Favors Tetrahedral | Favors Square Planar |
|--------|-------------------|---------------------|
| Metal | 3d metals | 4d, 5d metals |
| d^n config | High-spin d^5-d^7 | d^8 low-spin |
| Ligands | Weak field | Strong field (CN^-, CO) |
| Sterics | Large ligands | Small ligands |

### Quick Rules

1. **d^10** → Always tetrahedral (no LFSE in any geometry)
2. **d^8 + strong field** → Square planar
3. **d^8 + weak field** → Often tetrahedral
4. **4d, 5d metals** → Usually square planar for d^8
5. **High-spin d^5, d^6, d^7** → Tetrahedral favored

---

## Jahn-Teller Effect

### Definition
A geometric distortion in non-linear molecules that reduces symmetry and energy when degenerate orbitals are unevenly occupied.

### Common Cases

| Configuration | Geometry | Distortion |
|--------------|----------|------------|
| d^9 (Cu^2+) | Octahedral | Elongated along z-axis |
| High-spin d^4 | Octahedral | Elongated |
| Low-spin d^7 | Octahedral | Elongated |

### Consequences
- Removes degeneracy
- Lowers total energy
- Can produce square planar geometry (extreme elongation)

---

## Summary Table: Three Common Geometries

| Property | Octahedral | Tetrahedral | Square Planar |
|----------|------------|-------------|---------------|
| Coordination number | 6 | 4 | 4 |
| d-orbital sets | 2 | 2 | 4 |
| Upper set | e_g (2) | t_2 (3) | d_x²-y² (1) |
| Lower set | t_2g (3) | e (2) | d_xz,dyz (2) |
| Relative Δ | Δ_o | 4/9 Δ_o | ≈1.3 Δ_o |
| Spin state | HS or LS | Almost always HS | LS for d^8 |
| Common metals | All | Zn^2+, Co^2+ | Ni^2+, Pd^2+, Pt^2+ |

---

## Related Topics
- [[crystal_field_theory]] - Octahedral complexes
- [[coordination_chemistry]] - Isomers and nomenclature
- [[symmetry_group_theory]] - Point groups
- [[organometallic_chemistry]] - Metal-carbon bonds

## L3 Implementation
→ `../L3_functions/crystal_field_calculator.py`

## L4 Reference Data
→ `../L4_reference/lfse_values.md`

## L5 Examples
→ `../L5_examples/crystal_structures/
