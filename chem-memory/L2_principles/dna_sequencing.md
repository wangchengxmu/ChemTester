---
id: biochemistry.dna_sequencing
layer: 2
title: DNA Sequencing
parent: ../L1_ontology/chemistry-core-map.md#entry-156
stability: high
confidence: high
last_verified: 2026-03-16
source: Jakubowski & Flatt, Ch1.4
---

# DNA Sequencing

## Core Concept

DNA sequencing determines the order of nucleotides in a DNA molecule.

---

## Sanger Sequencing (Dideoxy Method)

### Principle

1. Use DNA polymerase to synthesize complementary strand
2. Include dideoxynucleotides (ddNTPs) that terminate chain
3. ddNTPs lack 3'-OH, preventing further extension
4. Separate fragments by size using electrophoresis
5. Read sequence from fragment lengths

### Components

| Component | Purpose |
|-----------|---------|
| Template DNA | Sequence to determine |
| Primer | Starting point for synthesis |
| dNTPs | Normal building blocks |
| ddNTPs | Chain terminators |
| DNA polymerase | Synthesis enzyme |

### Original Method (4 Lanes)

```
Lane A: ddATP → fragments ending with A
Lane T: ddTTP → fragments ending with T
Lane C: ddCTP → fragments ending with C
Lane G: ddGTP → fragments ending with G
```

Read from bottom (shortest) to top (longest)

### Modern Method (Fluorescent)

- Each ddNTP labeled with different fluorophore
- Single capillary electrophoresis
- Automated detection
- Read length: ~700-1000 bases

---

## Sequence Reading (Example)

Given chromatogram peaks (shortest to longest):

```
Position:  1  2  3  4  5  6  7  8  9
Fragment:  A  T  G  C  A  T  G  C  A
```

Sequence (5' → 3'): ATGCATGCA

---

## Real-Time Sequencing

### Zero-Mode Waveguides (PacBio)

- Tiny chambers (20 zeptoliters)
- DNA polymerase tethered at bottom
- Fluorescent dNTPs added
- Detect incorporation in real time
- Long reads (10-50 kb)

### Nanopore Sequencing

- DNA passes through membrane pore
- Each base blocks current differently
- Measure current changes
- Very long reads (>100 kb possible)
- Portable devices (MinION)

---

## Key Equations

### ddNTP Concentration for Optimal Termination

```
[ddNTP]/[dNTP] ratio typically 1:100 to 1:10

Higher ratio → shorter fragments
Lower ratio → longer fragments
```

### Read Coverage

```
Coverage = (Total bases sequenced) / (Genome size)

Example: 
100 Mb sequenced / 10 Mb genome = 10× coverage
```

---

## Comparison of Methods

| Feature | Sanger | Illumina | PacBio | Nanopore |
|---------|--------|----------|--------|----------|
| Read length | 700-1000 bp | 150-300 bp | 10-50 kb | >100 kb |
| Accuracy | >99.9% | >99% | ~90% | ~85-95% |
| Throughput | Low | Very high | Medium | Medium |
| Cost/base | High | Low | Medium | Low |
| Applications | Validation | Genomes | Long reads | Field work |

---

## Applications

| Application | Method |
|-------------|--------|
| Single gene sequencing | Sanger |
| Whole genome sequencing | Illumina |
| Structural variants | PacBio, Nanopore |
| Metagenomics | Illumina |
| Clinical diagnostics | Various |

---

## Sequence Quality

### Phred Quality Score

```
Q = -10 × log₁₀(P)

where P = probability of incorrect base call

Q10: 90% accuracy (1 in 10 wrong)
Q20: 99% accuracy (1 in 100 wrong)
Q30: 99.9% accuracy (1 in 1000 wrong)
Q40: 99.99% accuracy (1 in 10,000 wrong)
```

### Common Quality Thresholds

- Q30: Standard for most applications
- Q20: Acceptable for some applications
- Q40+: Required for clinical diagnostics

---

## Constraints

1. **Read length limits:** Each method has maximum read length
2. **Template preparation:** Requires purified DNA
3. **Error rates:** Vary by method, some need confirmation
4. **Cost considerations:** Method choice depends on application

---

## Related Topics

- `pcr.md` - Amplifying DNA for sequencing
- `genetic_code.md` - Interpreting sequences

---

## L3 Tools

- `reverse_complement()` - Get complementary strand
- `gc_content()` - Sequence composition
- `find_sequence()` - Search for motifs
