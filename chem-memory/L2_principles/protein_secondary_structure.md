---
id: biochem.protein_secondary_structure
layer: 2
title: Protein Secondary Structure
source: Fundamentals of Biochemistry (Jakubowski and Flatt), Ch4
status: active
created: 2026-03-13
down_links:
  - ../L3_functions/protein_structure_tools.py
  - ../L3_functions/protein_structure.py
---

# L2 Topic: Protein Secondary Structure

**Source**: Fundamentals of Biochemistry (Jakubowski and Flatt), Ch4
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Protein secondary structure consists of regular, repetitive structures stabilized by hydrogen bonds between backbone amide H and carbonyl O atoms.

### Key Features
1. **Alpha helices** - Most common, 3.6 residues/turn
2. **Beta sheets** - Parallel and antiparallel strands
3. **3₁₀ and π helices** - Less common helical types
4. **Turns and loops** - Connect secondary structure elements

---

## Core Principles

### Helix Parameters

| Helix Type | n (res/turn) | Pitch (Å) | Rise (Å/res) | H-bond |
|------------|--------------|-----------|--------------|--------|
| Alpha (α) | 3.6 | 5.4 | 1.5 | i → i+4 |
| 3₁₀ | 3.0 | 6.0 | 2.0 | i → i+3 |
| Pi (π) | 4.4 | 4.1 | 1.2 | i → i+5 |

### Phi/Psi Angles

| Structure | φ (phi) | ψ (psi) |
|-----------|---------|---------|
| Alpha helix | -57° | -47° |
| 3₁₀ helix | -50° | -26° |
| π helix | -55° | -70° |
| β-sheet (parallel) | -119° | +113° |
| β-sheet (antiparallel) | -139° | +135° |

### Helix Dipole
- Each peptide bond has ~3.5 Debye dipole
- Total dipole = n × 3.5 Debye
- Creates significant electric field

---

## Decision Trees

### Identifying Helix Type
```
H-bond pattern?
├── i → i+3? → 3₁₀ helix
├── i → i+4? → Alpha helix
└── i → i+5? → π helix
```

### Predicting Secondary Structure
```
Chou-Fasman rules:
1. Helix: Pα > 1.03 AND Pα > Pβ
2. Sheet: Pβ > 1.05 AND Pβ > Pα
3. Coil: Neither condition met
```

---

## Key Tables

### Chou-Fasman Propensities (selected)

| AA | Pα | Pβ | Preference |
|----|-----|-----|------------|
| Ala | 1.42 | 0.83 | Helix |
| Glu | 1.51 | 0.37 | Helix |
| Val | 1.06 | 1.70 | Sheet |
| Ile | 1.08 | 1.60 | Sheet |
| Pro | 0.57 | 0.55 | Breaker |
| Gly | 0.57 | 0.75 | Flexible |

### Beta Sheet Comparison

| Property | Parallel | Antiparallel |
|----------|----------|--------------|
| H-bonds | Bent | Linear |
| Stability | Lower | Higher |
| Side chains | Both hydrophobic | Alternating |

---

## Connected Topics

- **Upstream**: [amino_acid_properties.md](amino_acid_properties.md)
- **Downstream**: [protein_folding.md](protein_folding.md)
- **Related**: [enzyme_kinetics.md](enzyme_kinetics.md)

---

## L3 Tools

- `../L3_functions/protein_structure_tools.py` - Secondary structure calculations
- `../L3_functions/protein_tools.py` - Chou-Fasman prediction, Ramachandran analysis

---

## L4 References (TODO)

- [x] Helix parameters
- [x] Chou-Fasman propensities
- [ ] Ramachandran plot regions

---

## L5 Worked Examples (TODO)

- [ ] Helix length calculation
- [ ] Dipole moment estimation
- [ ] Secondary structure prediction
