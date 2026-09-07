# L2 Topic: Amino Acid Properties

**Source**: Fundamentals of Biochemistry (Jakubowski and Flatt), Ch3
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Amino acids are the building blocks of proteins. Their properties determine protein structure, function, and behavior in solution.

### Key Features
1. **20 standard amino acids** with unique side chains
2. **pKa values** for ionizable groups determine charge
3. **Isoelectric point (pI)** - pH of zero net charge
4. **Hydrophobicity scales** predict protein folding

---

## Core Principles

### Amino Acid Categories
| Category | Amino Acids | Key Feature |
|----------|-------------|-------------|
| Nonpolar | G, A, V, L, I, M, P, F, W | Hydrophobic |
| Polar uncharged | S, T, C, N, Q | H-bond capable |
| Acidic | D, E | Negative charge at pH 7 |
| Basic | K, R, H | Positive charge at pH 7 |

### pI Calculation Rules
```
No ionizable side chain: pI = (pKa_NH3+ + pKa_COOH) / 2
Acidic (D, E): pI = (pKa_COOH + pKa_sidechain) / 2
Basic (K, R, H): pI = (pKa_NH3+ + pKa_sidechain) / 2
```

### Hydrophobicity Interpretation
- **KD > 2**: Strongly hydrophobic (I, V, L, F, C)
- **KD < -3**: Strongly hydrophilic (R, K, D, E)

---

## Decision Trees

### Determining Amino Acid Category
```
Side chain has ionizable group?
├── Has COOH? → Acidic (D, E)
├── Has NH3+/Guanidino/Imidazole? → Basic (K, R, H)
└── No ionizable group?
    ├── Has heteroatoms (O, N, S)? → Polar (S, T, C, N, Q)
    └── Hydrocarbons only? → Nonpolar (G, A, V, L, I, M, P, F, W)
```

### Predicting pI Range
```
Acidic (D, E): pI < 7 (typically 2.8-3.2)
Neutral: pI ~6 (typically 5.5-6.5)
Basic (K, R, H): pI > 7 (typically 7.6-10.8)
```

---

## Key Tables

### Ionizable Side Chains
| Amino Acid | Group | pKa |
|------------|-------|-----|
| Asp | -COOH | 3.9 |
| Glu | -COOH | 4.3 |
| His | Imidazole | 6.0 |
| Cys | -SH | 8.3 |
| Tyr | -OH | 10.1 |
| Lys | -NH3+ | 10.5 |
| Arg | Guanidino | 12.5 |

### Terminal Groups
| Group | pKa Range |
|-------|-----------|
| α-COOH | 2.0-2.4 |
| α-NH3+ | 9.0-10.5 |

---

## Connected Topics

- **Upstream**: [organic_functional_groups.md](organic_functional_groups.md)
- **Downstream**: [protein_structure.md](protein_structure.md)
- **Related**: [enzyme_kinetics.md](enzyme_kinetics.md)

---

## L3 Tools

- `../L3_functions/amino_acid_tools.py` - Amino acid properties

---

## L4 References (TODO)

- [x] pKa values for all 20 amino acids
- [x] Kyte-Doolittle hydrophobicity scale
- [x] Hopp-Woods hydrophilicity scale

---

## L5 Worked Examples (TODO)

- [ ] pI calculation for each category
- [ ] Net charge at various pH values

## L3 Tool Call Directives


**Source:** `amino_acid_tools.py`

L3 tool module for amino acid tools

### Available functions:
- `amino_acid_info(code: str)` → dict — Get amino acid properties by code.
- `isoelectric_point(aa: str)` → dict — Calculate isoelectric point for an amino acid.
- `net_charge(aa: str, pH: float)` → dict — Calculate net charge of amino acid at given pH.
- `hydrophobicity_score(aa: str, scale: str)` → dict — Get hydrophobicity value for amino acid.
- `codon_table(aa: str)` → dict — Get codons for amino acid(s).
- `most_hydrophobic()` → dict — Find the most hydrophobic amino acid by Kyte-Doolittle scale.
- `most_hydrophilic()` → dict — Find the most hydrophilic amino acid by Kyte-Doolittle scale.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
