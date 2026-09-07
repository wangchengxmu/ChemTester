# L2 Topic: Transcription and Translation

**Source**: Fundamentals of Biochemistry (Jakubowski/Flatt)
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

Transcription and translation are the central processes of gene expression, converting DNA sequences to proteins. Understanding these processes is essential for molecular biology and biotechnology.

### Key Features
1. **Transcription**: DNA → RNA (RNA polymerase)
2. **Translation**: RNA → Protein (ribosome)
3. **Genetic code**: Triplet codons specify amino acids
4. **Regulation**: Multiple control points

---

## Core Principles

### Transcription Stages

| Stage | Description | Key Factors |
|-------|-------------|-------------|
| Initiation | RNA pol binds promoter | σ factor (prokaryotes), TFs (eukaryotes) |
| Elongation | RNA synthesis 5'→3' | NTP addition, proofreading |
| Termination | RNA release | Rho-dependent, intrinsic (prokaryotes) |

### Translation Stages

| Stage | Description | Energy |
|-------|-------------|--------|
| Initiation | Ribosome assembly on mRNA | 1 GTP |
| Elongation | Amino acid addition | 2 GTP per AA |
| Termination | Release at stop codon | 1 GTP |

### Genetic Code

| Feature | Property |
|---------|----------|
| Codons | 64 (61 sense, 3 stop) |
| Start | AUG (Met) |
| Stop | UAA, UAG, UGA |
| Degeneracy | Most AAs have multiple codons |
| Universality | Nearly universal across life |

### Energy Requirements

| Process | ATP/GTP per AA |
|---------|----------------|
| Aminoacyl-tRNA charging | 2 ATP |
| Translation initiation | 1 GTP |
| Translation elongation | 2 GTP |
| Translation termination | 1 GTP |
| **Total per AA** | **~4 ATP equivalents** |

---

## Key Formulas

### Transcription Rate
$$\text{Rate} \approx 40-80 \text{ nucleotides/sec (prokaryotes)}$$
$$\text{Rate} \approx 20-40 \text{ nucleotides/sec (eukaryotes)}$$

### Translation Rate
$$\text{Rate} \approx 15-20 \text{ amino acids/sec (prokaryotes)}$$
$$\text{Rate} \approx 2-5 \text{ amino acids/sec (eukaryotes)}$$

### mRNA to Protein Ratio
$$\text{Proteins per mRNA} = \frac{\text{translation rate}}{\text{mRNA decay rate}}$$

### Protein Synthesis Time
$$t = \frac{n_{AA}}{\text{elongation rate}} + t_{initiation}$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `transcribe_dna` | DNA → mRNA sequence |
| `translate_rna` | mRNA → protein sequence |
| `codon_usage_table` | Codon frequency analysis |
| `protein_synthesis_cost` | ATP/GTP calculation |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `genetic_code.csv` | Codon → AA mapping |
| `codon_usage.csv` | Species-specific codon frequencies |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| Gene expression calculation | Transcription + translation |
| Energy budget | ATP cost per protein |

---

**Cross-links:**
- dna_rna_structure.md
- genetic_code.md
- protein_structure.md
