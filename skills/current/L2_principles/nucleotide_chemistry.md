# L2 Topic: Nucleotide Chemistry

**Source**: Biochemistry fundamentals
**Created**: 2026-03-13
**Status**: Complete (Pass-4)

---

## Concept Overview

Nucleotides are the building blocks of nucleic acids (DNA and RNA), consisting of a nitrogenous base, sugar, and phosphate group.

### Key Features
1. **Purines** - Two-ring bases (A, G)
2. **Pyrimidines** - Single-ring bases (C, T, U)
3. **Base pairing** - Watson-Crick rules
4. **DNA vs RNA** - Sugar and base differences

---

## Core Principles

### Base Classification

| Type | Bases | Rings |
|------|-------|-------|
| Purines | Adenine, Guanine | 2 |
| Pyrimidines | Cytosine, Thymine, Uracil | 1 |

### Base Pairing Rules

| Pair | H-bonds | In |
|------|---------|-----|
| A-T | 2 | DNA |
| A-U | 2 | RNA |
| G-C | 3 | Both |

### DNA vs RNA

| Feature | DNA | RNA |
|---------|-----|-----|
| Sugar | Deoxyribose | Ribose |
| Unique base | Thymine (T) | Uracil (U) |
| Structure | Double helix | Single strand |

---

## L3 Tools

1. `nucleotide_chemistry_tools.py` - Base pairing, classification

---

## Connected Topics

- **Upstream**: [organic_functional_groups.md](organic_functional_groups.md)
- **Related**: [amino_acid_properties.md](amino_acid_properties.md)

## L3 Tool Call Directives

**Source:** nucleotide_chemistry_tools.py
L3 Tool: Nucleotide Chemistry Tools

### Available functions:
- base_info(name) → dict — Get nucleotide base properties.
- base_pairing(base1, base2) → dict — Check if two bases form a valid pair.
- nucleoside_info(name) → dict — Get nucleoside properties.
- purine_or_pyrimidine(name) → dict — Classify base as purine or pyrimidine.
- dna_vs_rna_bases() → dict — Compare DNA and RNA bases.

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
