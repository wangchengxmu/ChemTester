---
id: biochem.protein_structure
layer: 2
title: Protein Structure
source: LibreTexts Biochemistry (Jakubowski and Flatt), Ch4
status: active
created: 2026-03-18
down_links:
  - ../L3_functions/protein_structure_tools.py
  - ../L3_functions/protein_structure.py
  - ../L3_functions/protein_tools.py
---

# L2 Topic: Protein Structure

**Source**: LibreTexts Biochemistry (Jakubowski and Flatt), Ch4
**Created**: 2026-03-18
**Status**: Scaffold (Pass-1)

---

## Concept Overview

Protein structure is organized hierarchically into four levels: primary, secondary, tertiary, and quaternary. Understanding these structural levels is essential for predicting protein function, stability, and interactions.

### Key Features
1. **Primary structure**: Linear sequence of amino acids
2. **Secondary structure**: Local regular structures (α-helices, β-sheets)
3. **Tertiary structure**: Overall 3D folding of a single polypeptide
4. **Quaternary structure**: Assembly of multiple polypeptide subunits

---

## Core Principles

### Secondary Structure

| Type | H-bond Pattern | Residues/Turn | Pitch (Å) | φ/ψ Angles |
|------|---------------|---------------|-----------|------------|
| α-helix | i �?i+4 | 3.6 | 5.4 | -57°, -47° |
| 3₁₀ helix | i �?i+3 | 3.0 | 6.0 | -50°, -26° |
| π-helix | i �?i+5 | 4.4 | 5.0 | -57°, -70° |
| β-sheet (parallel) | Inter-strand | �?| 3.5/residue | -119°, 113° |
| β-sheet (antiparallel) | Inter-strand | �?| 3.3/residue | -139°, 135° |

### α-Helix Properties
- **Dipole moment**: All amides oriented N→C, creating macroscopic dipole (n × 3.5 Debye)
- **Side chains**: Extend outward from helix axis; staggered at 100° increments
- **Core**: Packed tightly; NO central cavity
- **Helical wheel**: Shows amphipathic character (hydrophobic/hydrophilic faces)

### β-Sheet Properties
- **Pleated sheet**: Alternating side chain orientations (above/below plane)
- **Parallel vs antiparallel**: Different H-bond angles; antiparallel more stable
- **β-barrels**: Form pores or enzyme active sites

### Tertiary Structure

**Noncovalent Interactions Stabilizing Tertiary Structure:**

| Interaction | Type | Energy (kJ/mol) |
|------------|------|-----------------|
| Salt bridges | Ion-ion | 20-40 |
| H-bonds | Dipole-dipole | 8-20 |
| Hydrophobic | Induced dipole | 4-8 |
| π-cation | Aromatic-cation | 5-10 |
| Aromatic-aromatic | Stacking | 4-8 |

**Side Chain Distribution in Folded Proteins:**
- Nonpolar (Val, Leu, Ile, Met, Phe): ~83% buried
- Charged (Asp, Glu, His, Arg, Lys): ~54% buried (surprised!)
- Polar uncharged (Asn, Gln, Ser, Thr, Tyr): ~63% buried

### Protein Domains

**Domains** are independent folding units within a protein:
- Self-stabilizing and often fold independently
- Fundamental units of tertiary structure
- Often correspond to functional modules
- Can be shuffled during evolution (domain swapping)

### pKa Modulation in Folded Proteins

Three major effects alter pKa of ionizable side chains:

1. **Born Effect (Dehydration)**: Buried charges less stable in low-dielectric interior
   - Coulomb's law: F = Q₁Q�?(4πεr²)
   - Dielectric constant of water (ε �?80) vs protein interior (ε �?4)

2. **Coulombic Interactions**: Nearby charges shift pKa
   - Opposite charges stabilize charged form (raise pKa for acids)
   - Like charges destabilize charged form (lower pKa for acids)

3. **Hydrogen Bonding**: H-bonds to charged groups stabilize specific states

### Quaternary Structure

**Symmetry Types in Oligomeric Proteins:**

| Symmetry | Description | Examples |
|----------|-------------|----------|
| Cyclic (C�? | n-fold rotation axis | Dimers, trimers, tetramers |
| Dihedral (D�? | n-fold + perpendicular 2-fold axes | Hemoglobin, ferritin |
| Cubic | Tetrahedral, octahedral, icosahedral | Viral capsids, ferritin |

- **Homomeric**: Identical subunits
- **Heteromeric**: Different subunits
- Chirality prevents inversion/mirror symmetry in proteins

---

## Decision Trees

### Predicting Secondary Structure from Sequence
```
Proline present? �?Likely turn/bend
Glycine-rich? �?Flexible loop
Alternating polar/nonpolar? �?β-sheet (amphipathic)
Continuous hydrophobic? �?Transmembrane α-helix
Chou-Fasman propensity > 1.0? �?Favor that structure
```

### Determining if Side Chain is Buried
```
Nonpolar side chain? �?Likely buried
Charged side chain? �?Often surface-exposed
Check sequence context and protein size
```

### Quaternary Structure Prediction
```
Hydrophobic surface patches? �?Likely oligomerization
Symmetrical sequence repeats? �?Symmetrical assembly
C-terminus accessible? �?Possible domain swapping
```

---

## Key Tables

### Amino Acid Propensities for Secondary Structure (Chou-Fasman)

| Amino Acid | P(α) | P(β) | Preference |
|------------|------|------|------------|
| Ala | 1.45 | 0.97 | α-helix |
| Glu | 1.53 | 0.26 | α-helix |
| Leu | 1.34 | 1.22 | α-helix |
| Met | 1.20 | 1.67 | β-sheet |
| Val | 1.14 | 1.65 | β-sheet |
| Ile | 1.00 | 1.60 | β-sheet |
| Pro | 0.59 | 0.62 | Breaks |
| Gly | 0.53 | 0.81 | Flexible |
| Tyr | 0.61 | 1.29 | β-sheet |

### pKa Values in Proteins vs Model Compounds

| Group | pKa (model) | pKa range (proteins) | Buried % |
|-------|------------|---------------------|----------|
| Asp | 3.9 | 0.5 - 9.2 | 56% |
| Glu | 4.3 | 2.1 - 8.8 | 48% |
| His | 6.5 | 2.4 - 9.2 | 72% |
| Cys | 8.6 | 2.5 - 11.1 | 90% |
| Tyr | 9.8 | 6.1 - 12.1 | 67% |
| Lys | 10.4 | 5.7 - 12.1 | 34% |

---

## Cross-Links

- **amino_acid_properties.md**: Detailed pKa, hydrophobicity scales
- **enzyme_kinetics.md**: Structure-function relationships in enzymes
- **biomolecules.md**: Protein classification and function
- **hydrogen_bonding.md**: Physical basis of H-bonds
- **hydrophobic_effect.md**: Thermodynamics of protein folding

---

## References

1. LibreTexts Biochemistry (Jakubowski and Flatt), Ch4: The Three-Dimensional Structure of Proteins
2. Pace, C.N. (2001). Biochemistry 40:310. Side chain burial statistics
3. Chou, P.Y. & Fasman, G.D. (1974). Secondary structure prediction parameters


## Implementations
- Implementation: `../L3_functions/protein_structure.py`

- Implementation: `../L3_functions/protein_structure_tools.py`

## L3 Tool Call Directives

**Source:** `protein_structure_tools.py`
Helix geometry, Chou-Fasman secondary structure prediction, Ramachandran analysis.

### Available functions:
- `helix_length(n_residues, helix_type='alpha')` → dict — Length in Å (rise: α=1.5, 3₁₀=2.0, π=1.2 Å/residue)
- `helix_turns(n_residues, helix_type='alpha')` → dict — Turns (α=3.6, 3₁₀=3.0, π=4.4 residues/turn)
- `helix_dipole(n_residues)` → dict — μ = n × 3.5 Debye
- `helix_h_bonds(n_residues, helix_type='alpha')` → dict — H-bonds (α: i→i+4, 3₁₀: i→i+3, π: i→i+5)
- `compare_helix_types(n_residues)` → dict — Compare all three helix types side by side
- `chou_fasman_predict(sequence)` → dict — Per-residue H/E/C prediction + avg propensities
- `ramachandran_check(phi, psi)` → dict — Region (alpha_helix/beta_sheet/etc.) + allowed status

### Common errors:
- ❌ Using non-standard 1-letter AA codes — must be uppercase (A-Z, 20 standard)
- ❌ Forgetting Ramachandran angles are in degrees, not radians
- ❌ Chou-Fasman only predicts single-residue propensity — doesn't account for propensities
