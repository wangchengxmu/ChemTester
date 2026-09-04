---
id: biochemistry.molecular_cloning
layer: 2
title: Molecular Cloning
parent: ../L1_ontology/chemistry-core-map.md#entry-157
stability: high
confidence: high
last_verified: 2026-03-16
source: Jakubowski & Flatt, Ch1.4
---

# Molecular Cloning

## Core Concept

Molecular cloning inserts a DNA fragment into a vector for propagation and expression.

---

## Restriction Enzymes

### Types of Cuts

| Type | Cut Pattern | Example |
|------|-------------|---------|
| **Sticky end (5' overhang)** | Staggered cut with 5' overhang | EcoRI: G^AATTC |
| **Sticky end (3' overhang)** | Staggered cut with 3' overhang | KpnI: GGTAC^C |
| **Blunt end** | Straight cut, no overhang | SmaI: CCC^GGG |

### Recognition Site Properties

- Usually palindromic (read same on both strands)
- Length typically 4-8 bp
- Longer sites = rarer cuts

---

## Cloning Process

### Step 1: Digestion

```
Insert DNA + Vector DNA + Restriction enzyme → Fragments with compatible ends
```

### Step 2: Ligation

```
Insert + Vector + DNA ligase + ATP → Recombinant DNA
```

### Step 3: Transformation

```
Recombinant DNA + Competent cells → Transformed cells
```

### Step 4: Selection

```
Plate on antibiotic medium → Only cells with vector survive
```

### Step 5: Screening

```
Test colonies for insert (PCR, restriction digest, sequencing)
```

---

## Vector Types

| Vector | Size Capacity | Application |
|--------|---------------|-------------|
| **Plasmid** | < 10 kb | General cloning |
| **Bacteriophage (λ)** | 10-25 kb | Library construction |
| **Cosmid** | 35-45 kb | Large inserts |
| **BAC** | 100-300 kb | Genomic libraries |
| **YAC** | 200-2000 kb | Eukaryotic libraries |

---

## Selection Markers

| Marker | Mechanism |
|--------|-----------|
| **Antibiotic resistance** | ampicillin, kanamycin, tetracycline |
| **Blue-white screening** | lacZ gene disruption |
| **Nutritional markers** | Complement auxotrophic mutants |

### Blue-White Screening

```
Vector: lacZ gene (β-galactosidase)
Insert site: Within lacZ
Substrate: X-gal (turns blue if lacZ intact)

Blue colonies: No insert (vector religated)
White colonies: Insert present (lacZ disrupted)
```

---

## Key Equations

### Ligation Efficiency

```
Ratio of insert:vector = 3:1 to 10:1 (molar)

Higher ratio favors insert incorporation
Lower ratio favors vector religation
```

### Transformation Efficiency

```
Efficiency = (Colony count × Dilution factor) / (Amount of DNA in μg)

Typical: 10⁶-10⁹ CFU/μg DNA
```

---

## Common Restriction Enzymes

| Enzyme | Recognition | Cut Position | Type |
|--------|-------------|--------------|------|
| EcoRI | GAATTC | G^AATTC | 5' sticky |
| HindIII | AAGCTT | A^AGCTT | 5' sticky |
| BamHI | GGATCC | G^GATCC | 5' sticky |
| NotI | GCGGCCGC | GC^GGCCGC | 5' sticky |
| SmaI | CCCGGG | CCC^GGG | Blunt |
| PstI | CTGCAG | CTGCA^G | 3' sticky |

---

## Constraints

1. **Site availability:** Must have restriction sites flanking insert
2. **Size limits:** Vectors have maximum capacity
3. **Directional cloning:** May need two different enzymes
4. **Frame preservation:** For expression, insert must be in correct reading frame

---

## Related Topics

- `pcr.md` - Amplifying inserts
- `dna_sequencing.md` - Verifying clones

---

## L3 Tools

- `find_restriction_sites()` - Locate cut sites
- `fragment_size()` - Calculate restriction fragment sizes
- `ligation_molar_ratio()` - Calculate amounts for ligation
