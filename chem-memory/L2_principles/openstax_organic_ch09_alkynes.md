---
id: organic.openstax_ch09
layer: 2
title: Alkynes - An Introduction to Organic Synthesis
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Alkynes - An Introduction to Organic Synthesis

## Key Principles

### Alkyne Structure
- **sp hybridization**: 180° bond angles, linear geometry
- **Triple bond**: One σ bond + two π bonds
- **Bond length**: C≡C = 120 pm (shortest C-C bond)
- **Bond strength**: ~965 kJ/mol (strongest C-C bond)

### Acidity of Terminal Alkynes
**Terminal alkynes are uniquely acidic among hydrocarbons**:
- Acetylene (HC≡CH): pKa = 25
- Ethylene (H₂C=CH₂): pKa = 44
- Methane (CH₄): pKa ≈ 60

**Why are terminal alkynes acidic?**
- sp-hybridized carbon has 50% s-character
- s orbitals are closer to nucleus, lower energy
- Negative charge on sp carbon is more stable
- Acetylide anion is relatively stable

**Deprotonation**: Use strong base with pKa > 25
- NaNH₂ (NH₂⁻, from NH₃, pKa = 35) ✓
- NaH ✓
- n-BuLi ✓
- NaOH (H₂O, pKa = 15.7) ✗

### Alkylation of Acetylide Anions
Acetylide anions are good nucleophiles for SN2 reactions:
```
RC≡C⁻ + R'-X → RC≡C-R' (alkyne product)
```
**Constraints**:
- Works with **primary alkyl halides** (SN2)
- Fails with secondary/tertiary (E2 competes)
- Internal alkynes can be built stepwise

## Mechanisms

### 1. Addition of HX
```
Step 1: Alkene-like addition → Vinylic carbocation
Step 2: Second HX addition → Dihalide
```
- **Markovnikov regiochemistry** (both additions)
- Trans stereochemistry common in first addition
- Vinylic carbocations are less stable than alkyl carbocations
- Secondary vinylic carbocation ≈ primary alkyl carbocation in stability

**Product sequence**: Alkyne → vinyl halide → geminal dihalide

### 2. Addition of X₂
```
Alkyne + X₂ → Trans-dihaloalkene (can add second X₂)
```
- Anti addition through halonium-like intermediate
- Trans stereochemistry in first addition
- Can stop at dihaloalkene or continue to tetrhalide

### 3. Hydration of Alkynes

**Method A: Hg²⁺-catalyzed (Markovnikov)**
```
Alkyne + H₂O, HgSO₄, H₂SO₄ → Enol → Ketone
```
- Markovnikov addition
- Terminal alkyne → methyl ketone
- Internal alkyne → mixture of ketones
- **Enol-keto tautomerism** occurs spontaneously

**Method B: Hydroboration-oxidation (Anti-Markovnikov)**
```
Terminal alkyne + disiamylborane → Vinylborane
Vinylborane + H₂O₂/OH⁻ → Enol → Aldehyde
```
- Anti-Markovnikov hydration
- Terminal alkyne → **aldehyde** (not ketone)
- Bulky borane prevents double addition

**Complementary results**:
| Terminal Alkyne | Hg²⁺/H₂O | Hydroboration-oxidation |
|-----------------|----------|-------------------------|
| RC≡CH | Methyl ketone (RCOCH₃) | Aldehyde (RCHO) |

### 4. Reduction of Alkynes

**Method A: Catalytic hydrogenation (Pd/C)**
```
Alkyne + 2 H₂, Pd/C → Alkane
```
- Complete reduction, no selectivity

**Method B: Lindlar catalyst (cis-alkene)**
```
Alkyne + H₂, Lindlar catalyst → cis-alkene
```
- **Lindlar catalyst**: Pd/CaCO₃, poisoned with Pb(OAc)₂ and quinoline
- **Syn addition** → cis (Z) alkene
- Stops at alkene stage
- Used in vitamin A synthesis

**Method C: Dissolving metal reduction (trans-alkene)**
```
Alkyne + Na or Li, NH₃(l), −33°C → trans-alkene
```
- **Trans-alkene** product
- Mechanism: electron transfers and protonations
- Anti addition (via more stable trans vinylic anion)

**Complementary reduction summary**:
| Method | Product | Stereochemistry |
|--------|---------|-----------------|
| Pd/C, H₂ | Alkane | Complete reduction |
| Lindlar, H₂ | cis-alkene | Syn |
| Na/NH₃ or Li/NH₃ | trans-alkene | Anti |

### 5. Keto-Enol Tautomerism
```
Enol ⇌ Keto form
```
- **Enol**: -OH on sp² carbon (ene + ol)
- **Keto**: C=O
- Equilibrium strongly favors keto form
- Catalyzed by acid or base
- Important in alkyne hydration mechanism

## Selectivity Rules

### Choosing Reduction Method
```
Need alkane? → Pd/C, excess H₂

Need cis-alkene? → Lindlar catalyst, 1 equiv H₂

Need trans-alkene? → Na/NH₃ or Li/NH₃
```

### Choosing Hydration Method
```
Want ketone from terminal alkyne? → HgSO₄/H₂O

Want aldehyde from terminal alkyne? → Hydroboration-oxidation

Internal alkyne? → Either method gives ketone(s); mixture if unsymmetrical
```

### Alkylation Constraints
- Primary halides work (SN2)
- Methyl and primary allylic/benzylic work well
- Secondary halides: elimination dominates
- Tertiary halides: elimination only
- Vinyl and aryl halides: no reaction (C-X bond too strong)

## Common Exam Patterns

### Pattern 1: Terminal Alkyne Deprotonation
**Question**: Which base will deprotonate a given terminal alkyne?
**Method**: Compare alkyne pKa (25) to conjugate acid pKa of base

| Base | Conjugate Acid pKa | Will Deprotonate? |
|------|-------------------|-------------------|
| NaH | H₂ (35) | Yes ✓ |
| NaNH₂ | NH₃ (35) | Yes ✓ |
| n-BuLi | butane (~50) | Yes ✓ |
| NaOH | H₂O (15.7) | No ✗ |
| NaOCH₃ | CH₃OH (15.6) | No ✗ |

### Pattern 2: Synthesis via Alkylation
**Question**: How to synthesize a specific alkyne?
**Approach**: Retrosynthetic analysis
1. Identify smaller alkyne fragment
2. Determine which carbon came from alkyl halide
3. Use acetylide anion SN2 with primary halide

**Example**: Synthesize 2-pentyne
```
HC≡CH → NaNH₂ → HC≡C⁻
HC≡C⁻ + CH₃CH₂CH₂-Br → CH₃CH₂CH₂C≡CH (1-pentyne)
1-pentyne → NaNH₂ → ⁻C≡CCH₂CH₂CH₃
⁻C≡CCH₂CH₂CH₃ + CH₃-I → CH₃C≡CCH₂CH₂CH₃ (2-pentyne)
```

### Pattern 3: Reduction Product Prediction
**Question**: Given alkyne + reagent, predict product

| Reagent | Product Type | Stereochemistry |
|---------|--------------|-----------------|
| H₂, Pd/C | Alkane | — |
| H₂, Lindlar | cis-alkene | Syn |
| Na, NH₃ | trans-alkene | Anti |

### Pattern 4: Hydration Product Prediction
**Question**: Internal vs terminal alkyne hydration

**Terminal alkyne (RC≡CH)**:
- HgSO₄/H₂O → Methyl ketone (RCOCH₃)
- Hydroboration/oxidation → Aldehyde (RCHO)

**Internal alkyne (RC≡CR')**:
- Both methods → ketone(s)
- If R ≠ R': mixture of two ketones

### Pattern 5: Tautomerism
**Question**: Show keto-enol equilibrium
- Enol form has -OH attached to C=C
- Keto form has C=O
- More substituted enol = more stable

### Pattern 6: Multi-step Synthesis
**Question**: Convert alkane to cis-alkene or trans-alkene

**General approach**:
1. Halogenate alkane (radical)
2. Eliminate to alkyne (E2, strong base)
3. Reduce selectively:
   - cis: Lindlar
   - trans: Na/NH₃

### Pattern 7: Disiamylborane Specificity
**Question**: Why use disiamylborane instead of BH₃ for terminal alkynes?
**Answer**: 
- BH₃ can add twice to terminal alkyne (messy)
- Bulky disiamylborane adds only once
- Clean conversion to aldehyde after oxidation
