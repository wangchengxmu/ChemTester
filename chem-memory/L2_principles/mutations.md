---
id: biochemistry.mutations
layer: 2
title: Mutations
parent: ../L1_ontology/chemistry-core-map.md#entry-154
stability: high
confidence: high
last_verified: 2026-03-16
source: Jakubowski & Flatt, Ch1.4
---

# Mutations

## Core Concept

Mutations are changes in DNA sequence that can affect protein structure and function.

---

## Mutation Types

### Point Mutations (Single Nucleotide)

| Type | DNA Change | Protein Effect | Example |
|------|------------|----------------|---------|
| **Silent** | Codon changed, same amino acid | None | UAU → UAC (both Tyr) |
| **Missense** | Different amino acid | Variable | UAU → UGU (Tyr → Cys) |
| **Nonsense** | Codon becomes stop | Truncated protein | UAU → UAG (Tyr → STOP) |

### Missense Subtypes

- **Conservative:** Similar amino acid (e.g., Leu → Ile)
- **Non-conservative:** Different properties (e.g., Leu → Asp)

### Frameshift Mutations

| Type | Mechanism | Effect |
|------|-----------|--------|
| **Insertion** | 1-2 nucleotides added | Shifts reading frame |
| **Deletion** | 1-2 nucleotides removed | Shifts reading frame |

- Changes all downstream codons
- Usually creates premature stop codon
- Often results in non-functional protein

### Larger Mutations

| Type | Description |
|------|-------------|
| **Deletion** | Large segment removed |
| **Duplication** | Segment copied |
| **Inversion** | Segment reversed |
| **Translocation** | Segment moved to different location |

---

## Mutation Effects

### On Protein Function

| Effect | Description | Example |
|--------|-------------|---------|
| **Loss of function** | Protein non-functional | Cystic fibrosis (ΔF508) |
| **Gain of function** | New or enhanced activity | Oncogenes |
| **Neutral** | No effect on function | Silent mutations |
| **Conditional** | Effect only under certain conditions | Temperature-sensitive mutants |

### On Phenotype

- **Dominant:** One copy sufficient for phenotype
- **Recessive:** Both copies needed
- **Incomplete dominance:** Heterozygote is intermediate

---

## Mutation Rate

```
Spontaneous mutation rate: ~10⁻⁹ to 10⁻¹⁰ per base per replication
Error rate after proofreading: ~1 in 10⁷-10⁸ bases
```

**Factors increasing mutation rate:**
- Radiation (UV, X-rays)
- Chemical mutagens
- DNA replication errors
- Defective repair mechanisms

---

## Key Equations

### Classification

```
Given: ref_codon, mut_codon

IF len(ref_codon) ≠ len(mut_codon):
    → Frameshift
ELIF codon_to_aa(ref_codon) == codon_to_aa(mut_codon):
    → Silent
ELIF codon_to_aa(mut_codon) == STOP:
    → Nonsense
ELSE:
    → Missense
```

### Conservative vs Non-conservative

```
Amino acid similarity groups:
- Nonpolar: G, A, V, L, I, M, F, W, P
- Polar: S, T, C, Y, N, Q
- Positive: K, R, H
- Negative: D, E

Conservative: same group
Non-conservative: different group
```

---

## Disease Examples

| Disease | Mutation Type | Gene/Protein |
|---------|---------------|--------------|
| Sickle cell anemia | Missense | HBB (Glu6Val) |
| β-Thalassemia | Nonsense | HBB |
| Tay-Sachs | Frameshift | HEXA |
| Cystic fibrosis | Deletion (3 bp) | CFTR (ΔF508) |
| Huntington's | Expansion | HTT (CAG repeats) |

---

## Constraints

1. **Reading frame:** Frameshifts affect all downstream codons
2. **Stop codons:** Nonsense creates premature termination
3. **Amino acid properties:** Conservative changes less disruptive

---

## Related Topics

- `genetic_code.md` - Codon-amino acid relationships
- `central_dogma.md` - Information flow

---

## L3 Tools

- `classify_mutation()` - Determine mutation type
- `hamming_distance()` - Count differences between sequences
- `protein_effect()` - Predict effect on protein

---

## L5 Examples

- Classifying a point mutation
- Predicting protein truncation
