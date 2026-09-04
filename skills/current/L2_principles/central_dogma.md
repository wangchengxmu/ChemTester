---
id: biochemistry.central_dogma
layer: 2
title: Central Dogma of Biology
parent: ../L1_ontology/chemistry-core-map.md#entry-152
stability: high
confidence: very_high
last_verified: 2026-03-16
source: Jakubowski & Flatt, Ch1.4
---

# Central Dogma of Biology

## Core Concept

The central dogma describes the flow of genetic information in biological systems:

```
DNA ──replication──> DNA
 │
 └──transcription──> RNA
                       │
                       └──translation──> Protein
```

---

## Three Core Processes

### 1. DNA Replication

**Purpose:** Duplicate genetic material before cell division

**Key Features:**
- **Semi-conservative:** Each daughter DNA has one old strand, one new strand
- **Template-based:** Each strand serves as template for complementary strand
- **High fidelity:** Error rate ~1 in 10⁷-10⁸ bases (proofreading by polymerase)

**Direction:** Always 5' → 3' synthesis

### 2. Transcription

**Purpose:** Convert DNA sequence to RNA

**Key Features:**
- RNA polymerase reads DNA template strand
- Produces mRNA (messenger RNA)
- In eukaryotes: occurs in nucleus, requires splicing of introns
- In prokaryotes: occurs in cytoplasm, no splicing needed

**Template strand:** Also called minus (-) strand, sense strand
**Coding strand:** Same sequence as mRNA (with T→U)

### 3. Translation

**Purpose:** Convert mRNA sequence to protein

**Key Features:**
- Occurs on ribosomes
- tRNA molecules bring amino acids
- Codon-anticodon pairing determines sequence
- Requires energy (GTP)

**Components:**
- mRNA (template)
- Ribosomes (machinery)
- tRNA (adapters)
- Amino acids (building blocks)

---

## Exceptions to Central Dogma

| Process | Description | Examples |
|---------|-------------|----------|
| **Reverse transcription** | RNA → DNA | Retroviruses (HIV), retrotransposons |
| **RNA replication** | RNA → RNA | RNA viruses |
| **Direct translation** | DNA → Protein | In vitro systems |

---

## Prokaryotes vs Eukaryotes

| Feature | Prokaryotes | Eukaryotes |
|---------|-------------|------------|
| Location | Cytoplasm | Nucleus (transcription), Cytoplasm (translation) |
| Coupling | Transcription-translation coupled | Separated processes |
| mRNA processing | None | Splicing, 5' cap, 3' poly-A tail |
| Ribosomes | 70S | 80S |

---

## Key Equations

### Information Content

```
Number of codons = 4^n
where n = number of nucleotides per codon

For triplet code: 4³ = 64 codons
```

### Gene Size Estimation

```
Protein length (aa) × 3 = Gene length (bp) [without introns]
```

---

## Constraints

1. **Directionality:** All synthesis is 5' → 3'
2. **Reading frame:** Must start at correct position
3. **Stop codons:** Terminate translation
4. **Post-translational modification:** Protein may be modified after synthesis

---

## Related Topics

- `genetic_code.md` - Codon-amino acid relationships
- `mutations.md` - Changes to genetic sequence
- `pcr.md` - Laboratory DNA replication
- `dna_sequencing.md` - Reading DNA sequences

---

## L3 Tools

- `transcribe_dna()` - DNA → mRNA
- `translate_mrna()` - mRNA → protein
- `find_orfs()` - Find protein-coding regions

---

## L5 Examples

- Translating a gene sequence
- Predicting mRNA from DNA template
