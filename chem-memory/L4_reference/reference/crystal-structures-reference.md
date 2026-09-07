# Crystal Structures Reference
[Source: Averill, Ch12]

## Seven Crystal Systems

| System | Edge Lengths | Angles | Examples |
|--------|--------------|--------|----------|
| Cubic | a = b = c | α = β = γ = 90° | NaCl, diamond |
| Tetragonal | a = b ≠ c | α = β = γ = 90° | TiO₂, Sn |
| Orthorhombic | a ≠ b ≠ c | α = β = γ = 90° | Sulfur, KNO₃ |
| Hexagonal | a = b ≠ c | α = β = 90°, γ = 120° | Graphite, Zn |
| Rhombohedral | a = b = c | α = β = γ ≠ 90° | Calcite, Bi |
| Monoclinic | a ≠ b ≠ c | α = γ = 90° ≠ β | Gypsum, KClO₃ |
| Triclinic | a ≠ b ≠ c | α ≠ β ≠ γ ≠ 90° | K₂Cr₂O₇ |

## Cubic Unit Cells

| Type | Atoms/Cell | Packing Efficiency | CN | Examples |
|------|------------|-------------------|-----|----------|
| Simple Cubic (SC) | 1 | 52% | 6 | Po |
| Body-Centered Cubic (BCC) | 2 | 68% | 8 | Fe, Cr, W |
| Face-Centered Cubic (FCC) | 4 | 74% | 12 | Cu, Al, Ag, Au |

## Close Packing Structures

| Structure | Stacking | Atoms/Cell | Packing | CN | Examples |
|-----------|----------|------------|---------|-----|----------|
| HCP | ABAB... | 2 | 74% | 12 | Mg, Zn, Ti |
| CCP (FCC) | ABCABC... | 4 | 74% | 12 | Cu, Al, Ni |

## Radius Ratio Rules

| Radius Ratio (r⁺/r⁻) | Coordination | Geometry | Structure Type |
|----------------------|--------------|----------|----------------|
| > 0.732 | 8 | Cubic | CsCl |
| 0.414 - 0.732 | 6 | Octahedral | NaCl |
| 0.225 - 0.414 | 4 | Tetrahedral | ZnS |
| < 0.225 | 2-3 | Linear/Triangular | Limited |

## Ionic Radii (pm)

### Cations
| Ion | Radius (pm) | Ion | Radius (pm) |
|-----|-------------|-----|-------------|
| Li⁺ | 90 | Mg²⁺ | 86 |
| Na⁺ | 116 | Ca²⁺ | 114 |
| K⁺ | 152 | Sr²⁺ | 132 |
| Rb⁺ | 166 | Ba²⁺ | 149 |
| Cs⁺ | 181 | Al³⁺ | 68 |
| Ag⁺ | 129 | Fe²⁺ | 92 |
| Cu⁺ | 91 | Fe³⁺ | 79 |

### Anions
| Ion | Radius (pm) |
|-----|-------------|
| O²⁻ | 126 |
| S²⁻ | 170 |
| F⁻ | 119 |
| Cl⁻ | 167 |
| Br⁻ | 182 |
| I⁻ | 206 |

## Common Ionic Structures

### NaCl (Rock Salt)
- Cl⁻ in FCC arrangement
- Na⁺ in all octahedral holes
- CN = 6:6
- Examples: NaCl, KBr, MgO, CaO

### CsCl
- Simple cubic
- Cs⁺ at body center, Cl⁻ at corners
- CN = 8:8
- Examples: CsCl, CsBr, CsI

### ZnS (Zinc Blende)
- S²⁻ in FCC
- Zn²⁺ in half tetrahedral holes
- CN = 4:4
- Examples: ZnS, CuCl, GaAs

### CaF₂ (Fluorite)
- Ca²⁺ in FCC
- F⁻ in all tetrahedral holes
- CN = 8:4
- Examples: CaF₂, SrF₂, BaF₂

## Key Formulas

### Atoms per Unit Cell
```
Total = corner×(1/8) + edge×(1/4) + face×(1/2) + body×(1)
```

### Density Calculation
```
ρ = (n × M)/(a³ × N_A)
```
- n = atoms per unit cell
- M = molar mass (g/mol)
- a = edge length (cm)
- N_A = 6.022×10²³

### Edge Length from Radius

**FCC:**
```
a = 2r√2 = 2.828r
```

**BCC:**
```
a = 4r/√3 = 2.309r
```

**SC:**
```
a = 2r
```

### Unit Cell Volume
**Cubic:**
```
V = a³
```

**General:**
```
V = abc × √(1 - cos²α - cos²β - cos²γ + 2cosα·cosβ·cosγ)
```

## Metal Crystal Structures

| Metal | Structure | a (pm) | Atomic Radius (pm) |
|-------|-----------|--------|-------------------|
| Al | FCC | 404 | 143 |
| Cu | FCC | 361 | 128 |
| Au | FCC | 408 | 144 |
| Ag | FCC | 409 | 144 |
| Fe (α) | BCC | 287 | 124 |
| Cr | BCC | 288 | 125 |
| W | BCC | 316 | 137 |
| Mg | HCP | 321, 521 | 160 |
| Zn | HCP | 266, 495 | 137 |

## Packing Efficiency Calculation

**FCC Example:**
```
PE = (4 atoms × 4/3 πr³) / a³ × 100%
   = (4 × 4/3 πr³) / (2r√2)³ × 100%
   ≈ 74%
```

## Related Topics
- [solid-state-reference.md](solid-state-reference.md)
- [band-theory-reference.md](band-theory-reference.md)
