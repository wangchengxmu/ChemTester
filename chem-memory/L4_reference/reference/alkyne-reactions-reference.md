# Alkyne Reactions Reference
[Source: Organic Chemistry OpenStax, Ch09]

## Bond Comparison: Single, Double, Triple

| Bond Type | Length (pm) | Energy (kJ/mol) | Hybridization | Geometry |
|-----------|-------------|-----------------|---------------|----------|
| C-C | 154 | 347 | sp³ | Tetrahedral |
| C=C | 134 | 611 | sp² | Trigonal planar |
| C≡C | 120 | 839 | sp | Linear |

## Terminal Alkyne Acidity

| Compound | pKa | Can Deprotonate Terminal Alkyne? |
|----------|-----|--------------------------------|
| Terminal alkyne (R-C≡C-H) | ~25 | - |
| NH₃ | 38 | No |
| H₂O | 15.7 | No |
| ROH | 16 | No |
| NaNH₂ | - | Yes (stronger base) |
| NaH | - | Yes (stronger base) |
| n-BuLi | - | Yes (stronger base) |

## Alkyne Reactions Summary

| Reaction | Reagent(s) | Product | Stereochemistry |
|----------|------------|---------|-----------------|
| Complete hydrogenation | H₂, Pd/C | Alkane | Syn (2 equiv H₂) |
| Partial hydrogenation (Lindlar) | H₂, Lindlar's Pd | cis-Alkene | Syn |
| Partial hydrogenation (Na/NH₃) | Na, NH₃(l) | trans-Alkene | Anti |
| Hydrohalogenation (1 equiv) | HX | Vinyl halide | Markovnikov |
| Hydrohalogenation (2 equiv) | 2 HX | Geminal dihalide | Markovnikov |
| Halogenation (1 equiv) | X₂ | Vicinal dihalide | Anti |
| Halogenation (2 equiv) | 2 X₂ | Tetrahalide | Anti |
| Hydration (Hg²⁺) | H₂O, HgSO₄, H⁺ | Ketone | Markovnikov |
| Hydration (BH₃) | BH₃, H₂O₂, OH⁻ | Aldehyde (terminal) | Anti-Markovnikov |
| Deprotonation | NaNH₂ | Acetylide anion | - |

## Hydrogenation Products

### Complete Reduction
```
R-C≡C-R' + 2H₂ (Pd/C) → R-CH₂-CH₂-R'
```

### Partial Reduction (Lindlar) → cis-Alkene
```
R-C≡C-R' + H₂ (Lindlar's) → R-C=C-R' (cis)
```

### Partial Reduction (Na/NH₃) → trans-Alkene
```
R-C≡C-R' + Na/NH₃ → R-C=C-R' (trans)
```

## Hydration Products

### Mercury(II)-catalyzed
| Alkyne Type | Product |
|-------------|---------|
| Terminal (R-C≡C-H) | Methyl ketone (R-CO-CH₃) |
| Internal symmetric | Ketone |
| Internal asymmetric | Mixture of ketones |

### Hydroboration-Oxidation
| Alkyne Type | Product |
|-------------|---------|
| Terminal (R-C≡C-H) | Aldehyde (R-CH₂-CHO) |
| Internal | Ketone |

## Acetylide Chemistry

### Formation
```
R-C≡C-H + NaNH₂ → R-C≡C-Na⁺ + NH₃
```

### Alkylation
```
R-C≡C-Na⁺ + R'-X → R-C≡C-R' + NaX
```

**Suitable alkyl halides**:
- Methyl halides (CH₃I, CH₃Br) ✓
- Primary alkyl halides ✓
- Secondary alkyl halides ✗ (elimination competes)
- Tertiary alkyl halides ✗ (elimination dominates)

### Nucleophilic Addition
```
R-C≡C-Na⁺ + RCHO → R-C≡C-CH(OH)-R (alcohol after workup)
R-C≡C-Na⁺ + R₂C=O → R-C≡C-CR₂(OH) (alcohol after workup)
```

## Alkyne Synthesis

### From Alkenes
```
Alkene + X₂ → Vicinal dihalide
Vicinal dihalide + 2 NaNH₂ → Alkyne + 2 NaX + 2 NH₃
```

### From Vicinal Dihalides
```
R-CHX-CHX-R' + 2 NaNH₂ → R-C≡C-R'
```

### From Alkylation
```
HC≡C-H → HC≡C-Na⁺ → HC≡C-R (R-X, SN2)
```

## Alkyne Nomenclature

### IUPAC Rules
1. Find longest chain containing triple bond
2. Number from end nearest triple bond
3. Use suffix "-yne"
4. For multiple triple bonds: -diyne, -triyne

### Examples
| Structure | IUPAC Name | Common Name |
|-----------|------------|-------------|
| HC≡CH | Ethyne | Acetylene |
| HC≡C-CH₃ | Propyne | Methylacetylene |
| CH₃-C≡C-CH₃ | But-2-yne | Dimethylacetylene |
| HC≡C-CH₂-CH₃ | But-1-yne | Ethylacetylene |

### Enynes (both double and triple bonds)
- Number to give lowest possible locants
- If tied, double bond gets lower number
- Example: pent-1-en-4-yne

## Reaction Decision Flowchart

```
Alkyne
    │
    ├─ Terminal? ─────────────────────────────┐
    │   │                                      │
    │   ├─ Yes → Can form acetylide            │
    │   │         └─ Alkylation with R-X       │
    │   │                                      │
    │   └─ No (internal)                       │
    │                                          │
    ├─ Reduction                               │
    │   │                                      │
    │   ├─ H₂, Pd/C → Alkane                   │
    │   ├─ H₂, Lindlar → cis-Alkene            │
    │   └─ Na, NH₃ → trans-Alkene              │
    │                                          │
    ├─ Addition                                │
    │   │                                      │
    │   ├─ HX → Vinyl halide → Geminal dihalide│
    │   ├─ X₂ → Dihaloalkene → Tetrahalide     │
    │   └─ H₂O (Hg²⁺) → Ketone                 │
    │                                          │
    └─ Synthesis                               │
        │                                      │
        ├─ From alkene: X₂, then NaNH₂         │
        └─ From acetylide: R-X (SN2)           │
```

## Key Differences: Alkenes vs Alkynes

| Feature | Alkene | Alkyne |
|---------|--------|--------|
| Hybridization | sp² | sp |
| Geometry | Trigonal planar | Linear |
| Bond angle | 120° | 180° |
| π bonds | 1 | 2 |
| Addition equivalents | 1 | Up to 2 |
| Terminal acidity | No | Yes (pKa ~25) |
| Partial reduction | - | cis or trans alkene |
