---
id: crystal.structures
layer: 2
title: Crystal Structures
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/crystal_structures_tools.py
  - ../L3_functions/crystal_structures_tools.py
  - ../L4_reference/reference/crystallography-data.md
  - ../L5_examples/crystal_structures/
source:
  - Averill, Ch12
---

[Source: Averill, Ch12]

## Context

Crystalline solids have their components arranged in a regular, repeating pattern extending in all three dimensions. The smallest repeating unit that describes the entire crystal is the unit cell. Understanding crystal structures enables calculation of densities, prediction of properties, and design of materials.

## Core Concepts

### 1. Unit Cells

**Definition:** The smallest repeating unit that, when stacked in three dimensions, produces the entire crystal lattice.

**Seven crystal systems** based on edge lengths (a, b, c) and angles (α, β, γ):
| System | Edges | Angles | Example |
|--------|-------|--------|---------|
| Cubic | a = b = c | α = β = γ = 90° | NaCl, diamond |
| Tetragonal | a = b ≠ c | α = β = γ = 90° | TiO₂ |
| Orthorhombic | a ≠ b ≠ c | α = β = γ = 90° | Sulfur |
| Hexagonal | a = b ≠ c | α = β = 90°, γ = 120° | Graphite |
| Rhombohedral | a = b = c | α = β = γ ≠ 90° | Calcite |
| Monoclinic | a ≠ b ≠ c | α = γ = 90° ≠ β | Gypsum |
| Triclinic | a ≠ b ≠ c | α ≠ β ≠ γ ≠ 90° | K₂Cr₂O₇ |

### 2. Cubic Unit Cells

Three types, all with 90° angles and equal edge lengths:

| Type | Atoms per Unit Cell | Packing Efficiency | Coordination Number |
|------|--------------------|--------------------|--------------------|
| Simple Cubic (SC) | 1 | 52% | 6 |
| Body-Centered Cubic (BCC) | 2 | 68% | 8 |
| Face-Centered Cubic (FCC) | 4 | 74% | 12 |

**Counting atoms in unit cells:**
- Corner atom: contributes 1/8 to each unit cell (shared by 8)
- Edge atom: contributes 1/4 to each unit cell (shared by 4)
- Face atom: contributes 1/2 to each unit cell (shared by 2)
- Body center: contributes 1 (not shared)

### 3. Close Packing

**Hexagonal Close-Packed (HCP):**
- ABAB... stacking sequence
- Coordination number: 12
- Packing efficiency: 74%
- Examples: Mg, Zn, Ti

**Cubic Close-Packed (CCP) = FCC:**
- ABCABC... stacking sequence
- Coordination number: 12
- Packing efficiency: 74%
- Examples: Cu, Al, Ag, Au

**Note:** HCP and CCP have the same packing efficiency but different layer stacking.

### 4. Density Calculations

**From unit cell parameters:**
```
ρ = (n × M) / (V_cell × N_A)
```
Where:
- n = atoms per unit cell
- M = molar mass (g/mol)
- V_cell = unit cell volume (cm³)
- N_A = Avogadro's number

**For cubic cells:**
```
V_cell = a³ (a = edge length)
```

**For close-packed structures:**
```
a = 2r × √2 (for FCC, where r = atomic radius)
a = 4r / √3 (for BCC)
```

### 5. Ionic Crystal Structures

**NaCl (rock salt) structure:**
- FCC arrangement of Cl⁻
- Na⁺ in all octahedral holes
- CN = 6:6
- Many alkali halides

**CsCl structure:**
- Simple cubic
- Cs⁺ at body center, Cl⁻ at corners
- CN = 8:8

**ZnS (zinc blende) structure:**
- FCC arrangement of S²⁻
- Zn²⁺ in half the tetrahedral holes
- CN = 4:4

## Decision Flow

### Determining Crystal Structure from Density

1. Calculate unit cell volume from edge length
2. Use density formula to find n (atoms per unit cell)
3. Match n to unit cell type:
   - n ≈ 1 → Simple cubic
   - n ≈ 2 → BCC
   - n ≈ 4 → FCC

### Predicting Coordination Number

1. Calculate radius ratio: r(smaller)/r(larger)
2. Use radius ratio rules:
   - > 0.732 → CN = 8 (cubic)
   - 0.414 - 0.732 → CN = 6 (octahedral)
   - 0.225 - 0.414 → CN = 4 (tetrahedral)
   - < 0.225 → CN = 2 or 3

## Quantitative Relationships

**Packing efficiency:**
```
PE = (Volume of atoms in unit cell / Volume of unit cell) × 100%
```

**For FCC:**
```
PE = (4 × (4/3)πr³) / (2√2 × r)³ × 100% ≈ 74%
```

**Relation between density and unit cell:**
```
ρ = (n × M) / (a³ × N_A)
```

## Edge Cases

- **Polonium:** Only element with simple cubic structure
- **Allotropes:** Same element, different structures (diamond vs graphite)
- **Polymorphs:** Same compound, different crystal forms
- **Defects:** Real crystals have vacancies, interstitials, dislocations

## Implementations and Data

- Tool implementation: [L3 code](../L3_functions/crystal_structures_tools.py)
- Solver wrapper: [L3 skill](../L3_functions/crystal_structures_tools.py)
- Reference database: [L4 crystal data](../L4_reference/reference/crystallography-data.md)
- Worked examples: [L5 examples](../L5_examples/crystal_structures/)

## Related Topics

- [solid_state_chemistry.md](solid_state_chemistry.md) - Types of solids
- [band_theory.md](band_theory.md) - Electronic structure
- [ionic_bonding.md](ionic_bonding.md) - Ionic crystal formation

## L3 Tool Call Directives

**Source:** `crystal_structures_tools.py`
Crystal structure calculations: lattice parameters, packing fractions, radius ratios.

### Available functions:
- `cubic_lattice_radius(edge_length, cell_type)` → float — Calculate atomic radius from cubic unit cell edge length
- `edge_length_from_radius(radius, cell_type)` → float — Calculate edge length from atomic radius
- `identify_crystal_system(a, b, c, alpha, beta, gamma)` → str — Identify crystal system from lattice parameters
- `bravais_lattice_types()` → dict — List all 14 Bravais lattice types
- `ionic_radius_ratio_rule(cation_radius, anion_radius)` → str — Predict coordination geometry from radius ratio
- `unit_cell_volume_cubic(edge_length)` → float — Calculate cubic unit cell volume
- `atoms_per_area_cubic(cell_type)` → int — Get atoms per unit cell for cubic lattices
- `drude_resistivity(lattice_constant_A, valence_electrons, tau_s)` → float — Estimate resistivity using Drude model
- `packing_fraction(cell_type)` → float — Calculate packing efficiency (SC/BCC/FCC/HCP)

### Common errors:
- ❌ Using wrong formula for BCC (2 atoms) vs FCC (4 atoms) per unit cell
- ❌ Confusing edge length with atomic diameter in simple cubic

## L3 Tool Call Directives

**Source:** `crystal_structures_tools.py`
Crystal structure calculations: lattice parameters, packing fractions, radius ratios.

### Available functions:
- `cubic_lattice_radius(edge_length, cell_type)` → float — Calculate atomic radius from cubic unit cell edge length
- `edge_length_from_radius(radius, cell_type)` → float — Calculate edge length from atomic radius
- `identify_crystal_system(a, b, c, alpha, beta, gamma)` → str — Identify crystal system from lattice parameters
- `bravais_lattice_types()` → dict — List all 14 Bravais lattice types
- `ionic_radius_ratio_rule(cation_radius, anion_radius)` → str — Predict coordination geometry from radius ratio
- `unit_cell_volume_cubic(edge_length)` → float — Calculate cubic unit cell volume
- `atoms_per_area_cubic(cell_type)` → int — Get atoms per unit cell for cubic lattices
- `drude_resistivity(lattice_constant_A, valence_electrons, tau_s)` → float — Estimate resistivity using Drude model
- `packing_fraction(cell_type)` → float — Calculate packing efficiency (SC/BCC/FCC/HCP)

### Common errors:
- ❌ Using wrong formula for BCC (2 atoms) vs FCC (4 atoms) per unit cell
- ❌ Confusing edge length with atomic diameter in simple cubic
