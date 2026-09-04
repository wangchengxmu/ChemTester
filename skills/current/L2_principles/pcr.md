---
id: biochemistry.pcr
layer: 2
title: PCR (Polymerase Chain Reaction)
parent: ../L1_ontology/chemistry-core-map.md#entry-155
stability: high
confidence: high
last_verified: 2026-03-16
source: Jakubowski & Flatt, Ch1.4
---

# PCR (Polymerase Chain Reaction)

## Core Concept

PCR amplifies specific DNA sequences exponentially, enabling analysis of minute amounts of DNA.

---

## Components

| Component | Purpose | Typical Concentration |
|-----------|---------|----------------------|
| **Template DNA** | Sequence to amplify | 1 ng - 1 μg |
| **Forward primer** | Binds 5' end of target | 0.1-1 μM |
| **Reverse primer** | Binds 3' end (complementary) | 0.1-1 μM |
| **dNTPs** | Building blocks | 200 μM each |
| **Taq polymerase** | Heat-stable DNA polymerase | 0.5-2 U/50 μL |
| **MgCl₂** | Cofactor for polymerase | 1.5-2.5 mM |
| **Buffer** | Optimal pH and salts | 1× |

---

## Thermal Cycling

### Three Steps Per Cycle

| Step | Temperature | Duration | Purpose |
|------|-------------|----------|---------|
| **Denaturation** | 94-98°C | 15-30 s | Separate DNA strands |
| **Annealing** | 50-65°C | 15-30 s | Primers bind to template |
| **Extension** | 72°C | 30-60 s/kb | DNA synthesis |

### Initial Denaturation
- 94-98°C for 2-5 min
- Ensures template is fully single-stranded

### Final Extension
- 72°C for 5-10 min
- Completes partial products

### Number of Cycles
- Typically 25-35 cycles
- More cycles = more product, but also more nonspecific products

---

## Amplification Mathematics

### Exponential Growth

```
N = N₀ × 2^n

where:
N = number of copies after n cycles
N₀ = initial number of target molecules
n = number of cycles
```

### Example

```
Starting material: 1 copy
Cycles: 30

N = 1 × 2^30 = 1,073,741,824 copies (~10^9)
```

### Practical Yield

```
At 20 cycles: ~10^6 copies (sufficient for most applications)
At 30 cycles: ~10^9 copies (maximal yield)
```

---

## Primer Design Rules

| Parameter | Recommended Range | Rationale |
|-----------|-------------------|-----------|
| **Length** | 18-25 nucleotides | Balance specificity and Tm |
| **Tm** | 55-65°C | Compatible with cycling |
| **Tm difference** | < 5°C between primers | Synchronized annealing |
| **GC content** | 40-60% | Stable but not too stable |
| **3' end** | End with G or C | "GC clamp" improves extension |
| **Avoid** | Long runs of single base | Mispriming |
| **Avoid** | Self-complementarity | Hairpins |
| **Avoid** | Primer-dimer potential | Competes with target |

---

## Melting Temperature (Tm) Estimation

### Simple Method (Wallace Rule)

```
Tm = 4(G + C) + 2(A + T)

Valid for: 14-20 bp primers
```

### Nearest-Neighbor Method (More Accurate)

```
Tm = ΔH / (ΔS + R × ln(C/4)) - 273.15

where:
ΔH = enthalpy of duplex formation
ΔS = entropy of duplex formation
R = gas constant (1.987 cal/mol·K)
C = primer concentration
```

### Salt Correction

```
Tm(corrected) = Tm + 16.6 × log10([Na+])

For [Na+] in mol/L
```

---

## Product Size Calculation

```
Product size = |reverse_primer_position - forward_primer_position| + 1

Note: Both positions are on the same strand, measuring from 5' to 3'
```

---

## Types of PCR

| Type | Application |
|------|-------------|
| **Standard PCR** | Basic amplification |
| **qPCR (Real-time)** | Quantification |
| **RT-PCR** | RNA analysis (reverse transcription first) |
| **Multiplex PCR** | Multiple targets simultaneously |
| **Nested PCR** | Increased specificity (two rounds) |

---

## Common Problems

| Problem | Cause | Solution |
|---------|-------|----------|
| No product | Poor primer design | Redesign primers, optimize Tm |
| Multiple bands | Nonspecific binding | Increase annealing temperature |
| Smearing | Too many cycles | Reduce cycles to 25-30 |
| Primer dimers | Primer self-complementarity | Redesign primers |

---

## Constraints

1. **Template length:** Very long templates (>10 kb) require special polymerases
2. **GC-rich regions:** May require additives (DMSO, betaine)
3. **Sequence accuracy:** Taq has no proofreading (use Pfu for cloning)

---

## Key Equations Summary

```
Amplification: N = N₀ × 2^n
Tm (simple): Tm = 4(G+C) + 2(A+T)
Product size: size = |pos_rev - pos_fwd| + 1
```

---

## Related Topics

- `dna_sequencing.md` - Reading DNA sequences
- `molecular_cloning.md` - Using PCR products

---

## L3 Tools

- `primer_tm()` - Calculate melting temperature
- `pcr_product_size()` - Calculate product length
- `gc_content()` - Calculate GC percentage
