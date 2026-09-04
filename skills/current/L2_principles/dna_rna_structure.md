# L2 Topic: DNA and RNA Structure

**Source**: Fundamentals of Biochemistry (Jakubowski/Flatt)
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

DNA and RNA are nucleic acids that store and transmit genetic information. Their structure determines their function in heredity, protein synthesis, and gene regulation.

### Key Features
1. **Nucleotide structure**: Base + sugar + phosphate
2. **DNA double helix**: Antiparallel strands, base pairing
3. **RNA structure**: Usually single-stranded, diverse functions
4. **DNA replication**: Semi-conservative mechanism

---

## Core Principles

### Nucleotide Components

| Component | DNA | RNA |
|-----------|-----|-----|
| Sugar | Deoxyribose | Ribose |
| Bases | A, G, C, T | A, G, C, U |
| 2' position | H | OH |
| Stability | More stable | Less stable |

### Base Pairing Rules

| Pair | Hydrogen Bonds | Type |
|------|----------------|------|
| A-T (DNA) | 2 | Watson-Crick |
| A-U (RNA) | 2 | Watson-Crick |
| G-C | 3 | Watson-Crick |
| G-U | 2 | Wobble (RNA) |

### DNA Double Helix Parameters

| Parameter | B-DNA | A-DNA | Z-DNA |
|-----------|-------|-------|-------|
| Helix sense | Right | Right | Left |
| Base pairs/turn | 10.5 | 11 | 12 |
| Rise per bp (Ã) | 3.4 | 2.6 | 3.7 |
| Pitch (Ã) | 35.7 | 28.6 | 44.6 |
| Diameter (Ã) | 20 | 23 | 18 |
| Conformation | Most common | Dehydrated | GC-rich |

### DNA Melting (Denaturation)

$$T_m = \frac{\Delta H^\circ}{\Delta S^\circ + R \ln(C_t/4)}$$

For estimation:
$$T_m \approx 2(A+T) + 4(G+C) \text{ Â°C}$$

### Supercoiling

$$Lk = Tw + Wr$$

Where:
- Lk = Linking number (topological invariant)
- Tw = Twist (helical winding)
- Wr = Writhe (supercoiling)

---

## Decision Trees

### DNA vs RNA Identification
```
Has ribose?
âââ Yes â?RNA
âââ No (deoxyribose) â?DNA
```

### Melting Temperature Estimation
```
Short oligo (<20 bp)?
âââ Yes â?Use 2-4 rule: Tm = 2(A+T) + 4(G+C)
âââ No â?Use nearest-neighbor method
```

---

## Key Formulas

### DNA Concentration from Absorbance
$$C = \frac{A_{260}}{\epsilon \cdot l}$$

Where Îµ for dsDNA â?6,600 Mâ»Â¹cmâ»Â?(per bp)

### Molecular Weight of DNA
$$MW = n \times 660 \text{ g/mol}$$

Where n = number of base pairs

### GC Content
$$\%GC = \frac{G + C}{A + T + G + C} \times 100\%$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `gc_content` | Calculate GC percentage |
| `tm_estimate` | Estimate melting temperature |
| `molecular_weight_dna` | Calculate MW of oligonucleotide |
| `reverse_complement` | Generate reverse complement |
| `complementarity_check` | Find complementary regions |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `nucleotide_properties.csv` | MW, absorbance, pKa |
| `nearest_neighbor_tm.csv` | Thermodynamic parameters |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| Tm calculation | Oligonucleotide design |
| GC content analysis | Genome characterization |

---

**Cross-links:**
- genetic_code.md
- transcription.md
- nucleic_acid_chemistry.md


## Implementations

- Implementation: `../L3_functions/dna_tools.py`

## L3 Tool Call Directives

**Source:** `dna_tools.py`
DNA/RNA sequence analysis: GC content, melting temperature, molecular weight, translation.

### Available functions:
- `gc_content(sequence)` → float — Calculate GC content percentage
- `tm_estimate(sequence, na_conc)` → float — Estimate melting temperature using Wallace rule
- `molecular_weight_dna(sequence, single_stranded)` → float — Calculate molecular weight in g/mol
- `complement(sequence, rna)` → str — Get complementary sequence (DNA or RNA)
- `reverse_complement(sequence, rna)` → str — Get reverse complement sequence
- `check_palindrome(sequence)` → bool — Check for palindromic (restriction enzyme) sequence
- `codon_table()` → Dict[str, str] — Get standard genetic code dictionary
- `translate_dna(dna_sequence, frame)` → str — Translate DNA to amino acid sequence

### Common errors:
- ❌ Using Wallace rule for long sequences (only valid for <14 nt oligonucleotides)
- ❌ Forgetting U replaces T in RNA output

## L3 Tool Call Directives

**Source:** `dna_tools.py`
DNA/RNA sequence analysis: GC content, melting temperature, molecular weight, translation.

### Available functions:
- `gc_content(sequence)` → float — Calculate GC content percentage
- `tm_estimate(sequence, na_conc)` → float — Estimate melting temperature using Wallace rule
- `molecular_weight_dna(sequence, single_stranded)` → float — Calculate molecular weight in g/mol
- `complement(sequence, rna)` → str — Get complementary sequence (DNA or RNA)
- `reverse_complement(sequence, rna)` → str — Get reverse complement sequence
- `check_palindrome(sequence)` → bool — Check for palindromic (restriction enzyme) sequence
- `codon_table()` → Dict[str, str] — Get standard genetic code dictionary
- `translate_dna(dna_sequence, frame)` → str — Translate DNA to amino acid sequence

### Common errors:
- ❌ Using Wallace rule for long sequences (only valid for <14 nt oligonucleotides)
- ❌ Forgetting U replaces T in RNA output
