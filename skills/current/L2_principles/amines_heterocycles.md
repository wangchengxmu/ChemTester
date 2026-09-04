# L2 Topic: Amines and Heterocycles

**Source**: Organic Chemistry (OpenStax) Ch24
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Amines are organic derivatives of ammonia (NH3) with one or more H atoms replaced by organic groups. They are the most important nitrogen-containing functional groups in organic chemistry and biology.

### Key Features
1. **Basicity**: Lone pair accepts protons
2. **Nucleophilicity**: N is good nucleophile
3. **Synthesis**: Multiple routes to amines
4. **Diazonium chemistry**: Key for arylamine transformations

---

## Core Principles

### 24.1-24.2: Structure and Classification
- **Primary (1°)**: RNH2
- **Secondary (2°)**: R2NH
- **Tertiary (3°)**: R3N
- **Quaternary**: R4N+

sp3 hybridization, pyramidal geometry

### 24.3-24.4: Basicity
- Aliphatic: pKa ~10-11 (stronger bases)
- Aromatic: pKa ~4-5 (resonance delocalization)
- Heterocyclic: varies (pyridine pKa 5.2, pyrrole pKa -0.3)

### 24.6: Amine Synthesis
Key methods:
1. SN2 alkylation (overalkylation problem)
2. Gabriel synthesis (clean primary amines)
3. Azide reduction (clean primary amines)
4. Reductive amination (from carbonyls)
5. Nitro reduction (for arylamines)
6. Hofmann rearrangement (lose one C)
7. Curtius rearrangement (lose one C)

### 24.7-24.8: Amine Reactions
- Salt formation with acids
- Acylation (amide formation)
- Diazonium chemistry (Sandmeyer, azo coupling)

### 24.9: Heterocyclic Amines
- Pyridine, pyrrole, imidazole
- Biological importance (DNA bases)

---

## Decision Trees

### Choosing Amine Synthesis Method
```
Target: Primary amine
    ↓
From alkyl halide? → Gabriel or Azide reduction
From carbonyl? → Reductive amination
From carboxylic acid? → Hofmann or Curtius (lose 1 C)

Target: Secondary/tertiary amine
    ↓
Reductive amination (best control)
```

### Basicity Prediction
```
Aliphatic vs Aromatic?
    ↓
Aromatic (arylamine) → Much less basic (resonance)
Aliphatic → More basic
    ↓
1°, 2°, 3°?
2° > 1° > 3° (steric hindrance on 3°)
```

---

## Key Tables

### Amine Basicity (pKa of conjugate acid)
| Amine | pKa |
|-------|-----|
| Ammonia | 9.3 |
| Methylamine | 10.6 |
| Dimethylamine | 10.7 |
| Trimethylamine | 9.8 |
| Aniline | 4.6 |
| Pyridine | 5.2 |
| Pyrrole | -0.3 |

### Sandmeyer Reactions
| Reagent | Product |
|---------|---------|
| CuCl | Ar-Cl |
| CuBr | Ar-Br |
| CuCN | Ar-CN |
| H2O | Ar-OH |
| H3PO2 | Ar-H |
| KI | Ar-I |

---

## Connected Topics

- **Upstream**: [alkyl_halide_reactions.md](alkyl_halide_reactions.md) (SN2)
- **Upstream**: Carbonyl chemistry (Ch19-23)
- **Related**: Amino acids, proteins

---

## L3 Tools Required

1. `amine_tools.py` - Basicity, synthesis routes
2. `diazonium_tools.py` - Sandmeyer, azo coupling

---

## L4 References (TODO)

- [ ] Complete basicity tables
- [ ] Heterocycle pKa values
- [ ] Diazonium stability data

---

## L5 Worked Examples (TODO)

- [ ] Reductive amination examples
- [ ] Sandmeyer reaction products
- [ ] Hofmann rearrangement calculations

## L3 Tool Call Directives

**Source:** `amine_tools.py`
Amine basicity, classification, and reaction product prediction.

### Available functions:
- `amine_basicity(amine)` → dict — Get pKb, basicity rank, conjugate acid pKa, and explanation
- `amine_classification(amine)` → dict — Classify amine as 1°/2°/3°/aromatic
- `reductive_amination_product(carbonyl, amine)` → dict — Predict product of reductive amination
- `sandmeyer_product(diazonium, reagent)` → dict — Predict Sandmeyer reaction product (CuCl/CuBr/CuCN/KI)
- `hofmann_rearrangement(amide)` → dict — Predict Hofmann rearrangement product (amide → amine)

### Common errors:
- ❌ Confusing pKa (conjugate acid) with pKb for basicity comparison
- ❌ Forgetting that aryl amines are less basic due to resonance delocalization

## L3 Tool Call Directives

**Source:** `amine_tools.py`
Amine basicity, classification, and reaction product prediction.

### Available functions:
- `amine_basicity(amine)` → dict — Get pKb, basicity rank, conjugate acid pKa, and explanation
- `amine_classification(amine)` → dict — Classify amine as 1°/2°/3°/aromatic
- `reductive_amination_product(carbonyl, amine)` → dict — Predict product of reductive amination
- `sandmeyer_product(diazonium, reagent)` → dict — Predict Sandmeyer reaction product (CuCl/CuBr/CuCN/KI)
- `hofmann_rearrangement(amide)` → dict — Predict Hofmann rearrangement product (amide → amine)

### Common errors:
- ❌ Confusing pKa (conjugate acid) with pKb for basicity comparison
- ❌ Forgetting that aryl amines are less basic due to resonance delocalization
