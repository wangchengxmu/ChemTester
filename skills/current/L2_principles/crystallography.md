---
id: crystallography
layer: 2
title: Crystallography and X-ray Diffraction
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/crystallography_tools.py
  - ../L4_reference/reference/crystallography-data.md
  - ../L5_examples/crystallography/
source:
  - LibreTexts Chemistry (Bragg's Law, X-ray Crystallography, Miller Indices)
  - LibreTexts Surface Science (Miller Indices)
  - LibreTexts Inorganic Chemistry (Interplanar Spacing)
---

## Context

Crystallography is the science of determining the arrangement of atoms in crystalline solids. X-ray diffraction (XRD) is the primary experimental technique, based on the interaction of X-rays with the periodic electron density in crystals. The fundamental relationship governing diffraction is Bragg's law, which connects the diffraction angle to the spacing between crystal planes.

## Core Concepts

### 1. Bragg's Law

**Fundamental Equation:**
```
nλ = 2d sin(θ)
```

Where:
- **n** = order of reflection (integer: 1, 2, 3, ...)
- **λ** = wavelength of X-ray (typically 0.5-2.5 Å)
- **d** = interplanar spacing (distance between parallel planes, in Å)
- **θ** = Bragg angle (angle between incident ray and crystal plane)

**Derivation from path difference:**
- Two X-rays reflecting from adjacent planes
- Path difference = BG + GF = 2d sin(θ)
- For constructive interference: path difference = nλ

**Rearranged forms:**
| Solve for | Formula |
|-----------|---------|
| Angle | θ = arcsin(nλ / 2d) |
| d-spacing | d = nλ / (2 sin(θ)) |
| Wavelength | λ = 2d sin(θ) / n |

**Constraints:**
- Valid only for 0 < sin(θ) ≤ 1
- Reflection possible only when nλ ≤ 2d
- Maximum angle: θ ≤ 90°

### 2. Miller Indices (hkl)

**Definition:** A notation system using three integers (hkl) to describe crystal planes and directions.

**Procedure to find Miller indices:**
1. Find intercepts on x, y, z axes (in units of lattice parameters a, b, c)
2. Take reciprocals of intercepts
3. Clear fractions to get smallest integers
4. Express as (hkl)

**Special cases:**
- Plane parallel to axis → intercept = ∞ → reciprocal = 0
- Negative intercept → negative Miller index (written with bar: h̄)

**Notation conventions:**
| Symbol | Meaning |
|--------|---------|
| (hkl) | Single plane or set of parallel planes |
| {hkl} | Family of equivalent planes |
| [hkl] | Crystal direction |
| ⟨hkl⟩ | Family of equivalent directions |

**Common planes in cubic system:**
| Plane | Intercepts | Miller Indices |
|-------|------------|----------------|
| Face perpendicular to x | a, ∞, ∞ | (100) |
| Face perpendicular to y | ∞, b, ∞ | (010) |
| Face perpendicular to z | ∞, ∞, c | (001) |
| Face diagonal | a, b, ∞ | (110) |
| Body diagonal | a, a, a | (111) |

### 3. Interplanar Spacing (d-spacing)

**Cubic system:**
```
d_hkl = a / √(h² + k² + l²)
```

**Tetragonal system:**
```
1/d² = (h² + k²)/a² + l²/c²
```

**Orthorhombic system:**
```
1/d² = h²/a² + k²/b² + l²/c²
```

**Hexagonal system:**
```
1/d² = (4/3)[(h² + hk + k²)/a²] + l²/c²
```

### 4. Unit Cell Volume

| System | Volume Formula |
|--------|---------------|
| Cubic | V = a³ |
| Tetragonal | V = a²c |
| Orthorhombic | V = abc |
| Hexagonal | V = (√3/2)a²c |
| Monoclinic | V = abc sin(β) |
| Rhombohedral | V = a³√(1 - 3cos²α + 2cos³α) |
| Triclinic | V = abc√(1 - cos²α - cos²β - cos²γ + 2cosα cosβ cosγ) |

### 5. Crystal Density

**From unit cell parameters:**
```
ρ = (n × M) / (V × N_A)
```

Where:
- ρ = density (g/cm³)
- n = number of atoms per unit cell
- M = molar mass (g/mol)
- V = unit cell volume (cm³)
- N_A = Avogadro's number (6.022 × 10²³ mol⁻¹)

**For compounds:**
```
ρ = (Z × M_formula) / (V × N_A)
```

Where Z = number of formula units per unit cell.

### 6. X-ray Sources

| Target | Kα Wavelength (Å) |
|--------|------------------|
| Cu | 1.5418 |
| Mo | 0.7107 |
| Cr | 2.2910 |
| Co | 1.7903 |
| Fe | 1.9373 |

## Decision Flow

### Choosing the d-spacing formula

1. Identify crystal system from lattice parameters
2. Apply appropriate formula based on symmetry:
   - Cubic → simplest: d = a/√(h²+k²+l²)
   - Tetragonal → two parameters: a, c
   - Orthorhombic → three parameters: a, b, c
   - Hexagonal → special formula with 4/3 factor

### Solving Bragg's law problems

1. Identify known variables (λ, d, θ, n)
2. Check constraint: nλ ≤ 2d
3. Apply appropriate rearranged form
4. For multiple orders (n=1,2,3...), calculate successive angles

### Converting Miller indices

1. **Intercepts → Miller indices:** Take reciprocals, clear fractions
2. **Miller indices → Intercepts:** Invert (h,k,l) and multiply by (a,b,c)

## Quantitative Relationships

**Packing fractions and atomic radii:**

| Structure | Atoms/Cell | Atomic Radius | Coordination |
|-----------|------------|---------------|--------------|
| Simple Cubic | 1 | r = a/2 | CN = 6 |
| BCC | 2 | r = a√3/4 | CN = 8 |
| FCC | 4 | r = a√2/4 | CN = 12 |
| HCP | 2 | r = a/2 | CN = 12 |

**Path difference between adjacent planes:**
```
Δ = 2d sin(θ)
```

## Edge Cases

- **First-order reflection (n=1):** Most common, typically assumed if not specified
- **Higher-order reflections:** Same plane, different angles
- **Forbidden reflections:** Due to glide planes or screw axes
- **Amorphous materials:** No sharp diffraction peaks
- **Powder vs single crystal:** Different diffraction patterns

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/crystallography_tools.py)
- Reference database: [L4 crystallography data](../L4_reference/reference/crystallography-data.md)
- Worked examples: [L5 examples](../L5_examples/crystallography/)

## Related Topics

- [crystal_structures.md](crystal_structures.md) - Unit cells and packing
- [solid_state_chemistry.md](solid_state_chemistry.md) - Types of solids
- [band_theory.md](band_theory.md) - Electronic structure of solids

## L3 Tool Call Directives

**Source:** `crystallography_tools.py`

X-ray diffraction calculations: Bragg's law, Miller indices, d-spacing for all crystal systems, unit cell volume, and crystal density.

### Available functions:
- `braggs_law(n, wavelength, d_spacing, angle_deg)` → Dict — Solve nλ = 2d sin(θ); pass two of wavelength/d_spacing/angle
- `braggs_angle(n, wavelength, d_spacing)` → float|None — Returns θ in degrees, or None if reflection not possible
- `d_spacing_from_bragg(n, wavelength, angle_deg)` → float — Calculate d-spacing from Bragg's law
- `d_spacing_cubic(a, h, k, l)` → float — d = a/√(h²+k²+l²) for cubic system
- `d_spacing_tetragonal(a, c, h, k, l)` → float — d-spacing for tetragonal system
- `d_spacing_orthorhombic(a, b, c, h, k, l)` → float — d-spacing for orthorhombic system
- `d_spacing_hexagonal(a, c, h, k, l)` → float — d-spacing for hexagonal system
- `d_spacing_general(crystal_system, params, h, k, l)` → float — Universal d-spacing for any crystal system
- `unit_cell_volume(cell_type, a, b, c, alpha, beta, gamma)` → float — Volume in Å³
- `crystal_density(n_atoms, atomic_mass, volume_angstrom3)` → float — Density in g/cm³
- `atoms_per_unit_cell(cell_type)` → int — Z for SC(1), BCC(2), FCC(4)
- `coordination_number(structure_type)` → int — CN for SC(6), BCC(8), FCC(12)
- `packing_fraction(structure_type)` → float — SC(0.52), BCC(0.68), FCC(0.74)
- `intercepts_to_miller(intercepts)` → Tuple[int,int,int] — Convert intercepts to (hkl)
- `miller_to_intercepts(h, k, l, a, b, c)` → Tuple[float,float,float] — Convert (hkl) to intercepts

### Common errors:
- ❌ Forgetting that reflection requires nλ ≤ 2d (check is_reflection_possible first)
- ❌ Using angles in radians instead of degrees (functions expect degrees)
- ❌ Invalid Miller indices: h=k=l=0 is not allowed

## L3 Tool Call Directives

**Source:** `xray_crystallography_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
