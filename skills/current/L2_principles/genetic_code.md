---
id: biochemistry.genetic_code
layer: 2
title: Genetic Code
parent: ../L1_ontology/chemistry-core-map.md#entry-153
stability: very_high
confidence: very_high
last_verified: 2026-03-16
source: Jakubowski & Flatt, Ch1.4
---

# Genetic Code

## Core Concept

The genetic code is the correspondence between nucleotide triplets (codons) and amino acids.

---

## Code Properties

### 1. Triplet Code
- Each codon = 3 nucleotides
- 4â?= 64 possible codons
- 61 sense codons (encode amino acids)
- 3 stop codons (terminate translation)

### 2. Degenerate (Redundant)
- Multiple codons encode same amino acid
- Exception: Methionine (AUG), Tryptophan (UGG) have single codons
- Degeneracy mostly at third position (wobble)

### 3. Universal
- Same code used by nearly all organisms
- Minor exceptions in mitochondria, some protozoa
- Strong evidence for common ancestry

### 4. Unambiguous
- Each codon specifies only one amino acid
- No codon encodes multiple amino acids

### 5. Non-overlapping
- Codons read in succession
- Each nucleotide part of only one codon

### 6. No Gaps
- Reading is continuous
- No nucleotides skipped

---

## Start and Stop Codons

### Start Codons

| Codon | Amino Acid | Notes |
|-------|------------|-------|
| **AUG** | Methionine (Met, M) | Primary start codon |
| GUG | Valine | Alternative in prokaryotes |
| UUG | Leucine | Alternative in prokaryotes |

- Start codon defines reading frame
- First Met often removed post-translationally

### Stop Codons

| Codon | Name | Notes |
|-------|------|-------|
| **UAA** | Ochre | Most common in E. coli |
| **UAG** | Amber | First discovered |
| **UGA** | Opal | Can encode selenocysteine |

- No tRNA for stop codons
- Release factors terminate translation

---

## Standard Genetic Code Table

```
First Position (5' end)
     â?   Second Position        Third Position
     â?   U      C      A      G      â?     âââââââââââââââââââââââââââââââââââ?   U â?UUU Phe UCU Ser UAU Tyr UGU Cys â?U
     â?UUC Phe UCC Ser UAC Tyr UGC Cys â?C
     â?UUA Leu UCA Ser UAA STOP UGA STOPâ?A
     â?UUG Leu UCG Ser UAG STOP UGG Trp â?G
     âââââââââââââââââââââââââââââââââââ?   C â?CUU Leu CCU Pro CAU His CGU Arg â?U
     â?CUC Leu CCC Pro CAC His CGC Arg â?C
     â?CUA Leu CCA Pro CAA Gln CGA Arg â?A
     â?CUG Leu CCG Pro CAG Gln CGG Arg â?G
     âââââââââââââââââââââââââââââââââââ?   A â?AUU Ile ACU Thr AAU Asn AGU Ser â?U
     â?AUC Ile ACC Thr AAC Asn AGC Ser â?C
     â?AUA Ile ACA Thr AAA Lys AGA Arg â?A
     â?AUG Met ACG Thr AAG Lys AGG Arg â?G
     âââââââââââââââââââââââââââââââââââ?   G â?GUU Val GCU Ala GAU Asp GGU Gly â?U
     â?GUC Val GCC Ala GAC Asp GGC Gly â?C
     â?GUA Val GCA Ala GAA Glu GGA Gly â?A
     â?GUG Val GCG Ala GAG Glu GGG Gly â?G
     âââââââââââââââââââââââââââââââââââ?```

---

## Special Amino Acids

### Selenocysteine (Sec, U)
- Encoded by UGA (normally stop)
- Requires SECIS element in mRNA
- Found in: glutathione peroxidase, deiodinases
- Present in: Archaea, Eubacteria, Animals

### Pyrrolysine (Pyl, O)
- Encoded by UAG (normally stop)
- Found in: methanogenic archaea
- Synthesized from two lysine molecules

---

## Wobble Hypothesis

Third position of codon has more flexibility in base pairing:

| Anticodon Base | Codon Bases Recognized |
|----------------|------------------------|
| C | G only |
| A | U only |
| U | A or G |
| G | U or C |
| I (Inosine) | U, C, or A |

**Implication:** Fewer tRNAs needed than codons (61 sense codons â?~45 tRNAs)

---

## Codon Usage Bias

- Organisms prefer certain codons over synonyms
- Reflects tRNA abundance
- Important for heterologous protein expression

**Example:** E. coli prefers CGG for Arg; humans prefer AGA

---

## Key Equations

### Codon Degeneracy

```
Degeneracy = Number of codons encoding amino acid

Example: Leucine has 6 codons (UUA, UUG, CUU, CUC, CUA, CUG)
         Degeneracy = 6
```

### Information Capacity

```
Number of sequences = 4^n
where n = sequence length

For gene of 1000 bp: 4^1000 possible sequences
```

---

## Constraints

1. **Reading frame must be maintained:** Indels cause frameshifts
2. **Start codon required:** Translation must begin at AUG
3. **Stop codon required:** Translation must terminate
4. **Case sensitivity:** Codons usually written uppercase

---

## Related Topics

- `central_dogma.md` - Information flow
- `mutations.md` - Changes to codons
- `dna_sequencing.md` - Reading sequences

---

## L3 Tools

- `codon_to_amino_acid()` - Translate single codon
- `amino_acid_to_codons()` - Find all codons for amino acid
- `translate_mrna()` - Full translation

---

## L4 Data

- Complete codon table
- Codon usage tables by organism


## Implementations

- Implementation: `../L3_functions/genetic_tools.py`
