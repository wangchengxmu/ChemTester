---
id: materials.crystal_structure_data
layer: 4
title: Crystal Structure Reference Data
parent: ../L2_principles/solid_state_chemistry.md
stability: high
last_verified: 2026-03-16
source: Oxtoby et al., Unit 6: Materials
---

# Crystal Structure Reference Data

## Common Crystal Structures

### Ionic Crystals (NaCl Structure)

| Compound | Lattice Constant a (Å) | Density (g/cm³) | Coordination |
|----------|------------------------|-----------------|--------------|
| NaCl | 5.640 | 2.165 | 6:6 |
| KCl | 6.293 | 1.988 | 6:6 |
| LiF | 4.028 | 2.635 | 6:6 |
| MgO | 4.212 | 3.58 | 6:6 |
| CaO | 4.811 | 3.35 | 6:6 |

### CsCl Structure (Body-Centered Cubic)

| Compound | Lattice Constant a (Å) | Density (g/cm³) |
|----------|------------------------|-----------------|
| CsCl | 4.123 | 3.99 |
| CsBr | 4.286 | 4.44 |
| CsI | 4.566 | 4.51 |

### Zinc Blende (ZnS) Structure

| Compound | Lattice Constant a (Å) | Band Gap (eV) |
|----------|------------------------|---------------|
| ZnS | 5.410 | 3.54 |
| ZnSe | 5.668 | 2.70 |
| GaAs | 5.653 | 1.42 |
| InP | 5.869 | 1.35 |

---

## Metallic Crystal Structures

### Face-Centered Cubic (FCC)

| Metal | Lattice Constant a (Å) | Atomic Radius (Å) | Density (g/cm³) |
|-------|------------------------|-------------------|-----------------|
| Al | 4.050 | 1.43 | 2.70 |
| Cu | 3.615 | 1.28 | 8.96 |
| Ag | 4.086 | 1.44 | 10.5 |
| Au | 4.078 | 1.44 | 19.3 |
| Ni | 3.524 | 1.25 | 8.90 |
| Pt | 3.923 | 1.39 | 21.5 |

### Body-Centered Cubic (BCC)

| Metal | Lattice Constant a (Å) | Atomic Radius (Å) | Density (g/cm³) |
|-------|------------------------|-------------------|-----------------|
| Fe (α) | 2.867 | 1.24 | 7.87 |
| Cr | 2.885 | 1.25 | 7.19 |
| W | 3.165 | 1.37 | 19.3 |
| Mo | 3.147 | 1.36 | 10.2 |
| V | 3.028 | 1.31 | 6.11 |

### Hexagonal Close-Packed (HCP)

| Metal | a (Å) | c (Å) | c/a ratio | Density (g/cm³) |
|-------|-------|-------|-----------|-----------------|
| Mg | 3.209 | 5.211 | 1.624 | 1.74 |
| Zn | 2.665 | 4.947 | 1.856 | 7.14 |
| Ti | 2.951 | 4.683 | 1.587 | 4.51 |
| Co | 2.507 | 4.070 | 1.623 | 8.86 |
| Cd | 2.979 | 5.618 | 1.886 | 8.65 |

---

## Semiconductors

### Band Gaps

| Material | Crystal Structure | Band Gap (eV) | Type |
|----------|-------------------|---------------|------|
| Si | Diamond | 1.11 | Indirect |
| Ge | Diamond | 0.67 | Indirect |
| GaAs | Zinc Blende | 1.42 | Direct |
| InP | Zinc Blende | 1.35 | Direct |
| GaN | Wurtzite | 3.36 | Direct |
| ZnO | Wurtzite | 3.37 | Direct |
| CdTe | Zinc Blende | 1.49 | Direct |
| InSb | Zinc Blende | 0.17 | Direct |

### Effective Masses (relative to electron mass m₀)

| Material | mₑ*/m₀ | mₕ*/m₀ |
|----------|---------|---------|
| Si | 0.26 | 0.39 |
| Ge | 0.12 | 0.29 |
| GaAs | 0.067 | 0.50 |
| InP | 0.080 | 0.60 |

---

## Packing Efficiency

| Structure | Packing Fraction | Coordination Number |
|-----------|------------------|---------------------|
| Simple Cubic | 0.52 | 6 |
| BCC | 0.68 | 8 |
| FCC | 0.74 | 12 |
| HCP | 0.74 | 12 |

---

## Lattice Energy (Born-Landé Equation)

```
U = -N_A × M × z⁺ × z⁻ × e² / (4πε₀r₀) × (1 - 1/n)

where:
M = Madelung constant
z⁺, z⁻ = ion charges
r₀ = equilibrium distance
n = Born exponent (typically 5-12)
```

### Madelung Constants

| Crystal Structure | Madelung Constant (M) |
|-------------------|----------------------|
| NaCl | 1.7476 |
| CsCl | 1.7627 |
| ZnS (zinc blende) | 1.6381 |
| CaF₂ (fluorite) | 2.519 |
| TiO₂ (rutile) | 2.408 |

---

## Related L2 Topics

- `solid_state_chemistry.md` - Principles
- `crystal_structures.md` - Structure types
- `band_theory.md` - Electronic properties
