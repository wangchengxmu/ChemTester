---
id: organic.openstax_ch08
layer: 2
title: Alkenes - Reactions and Synthesis
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Alkenes - Reactions and Synthesis

## Key Principles

### Addition Reaction Overview
Alkenes undergo **addition reactions** where the π bond breaks and new σ bonds form:
- Π bond electrons are nucleophilic (electron-rich)
- Electrophiles attack the double bond
- Carbocation or cyclic intermediates common
- Stereochemistry: syn (same face) or anti (opposite faces)

### Markovnikov's Rule
**Statement**: In addition of HX to an unsymmetrical alkene, H adds to the carbon with more hydrogens (less substituted), X adds to the carbon with fewer hydrogens (more substituted).

**Modern interpretation**: The electrophile adds to give the more stable carbocation intermediate.

**Stability order**: 3° > 2° > 1° > methyl

### Regiochemistry Summary Table

| Reaction | Regiochemistry | Mechanism | Stereochemistry |
|----------|---------------|-----------|-----------------|
| HX addition | Markovnikov | Carbocation | Mixture (via planar carbocation) |
| H₂O/H⁺ (acid) | Markovnikov | Carbocation | Mixture |
| Oxymercuration | Markovnikov | Mercurinium ion | Anti (mostly) |
| Hydroboration-oxidation | Anti-Markovnikov | Concerted | Syn |
| HX + peroxides | Anti-Markovnikov | Radical | Mixture |
| X₂ addition | N/A (symmetric) | Halonium ion | Anti |
| HO-X (halohydrin) | OH to more substituted | Halonium ion | Anti |
| H₂/Pd | N/A | Surface catalysis | Syn |
| Hydroboration | B to less substituted | Concerted | Syn |

## Mechanisms

### 1. Electrophilic Addition of HX
```
Step 1: Alkene + HX → Carbocation (rate-determining)
Step 2: Carbocation + X⁻ → Alkyl halide
```
- Carbocation stability determines regiochemistry
- May rearrange (hydride or alkyl shift)
- Possible carbocation rearrangements: 1,2-H shift, 1,2-alkyl shift

### 2. Halogen Addition (X₂)
```
Step 1: Alkene + X₂ → Halonium ion + X⁻
Step 2: X⁻ attacks halonium ion (SN2-like) → trans-dihalide
```
- **Anti stereochemistry**: X⁻ attacks from opposite side
- Cyclic halonium ion prevents rotation
- No carbocation → no rearrangements

### 3. Halohydrin Formation (X₂ + H₂O)
```
Step 1: Alkene + X₂ → Halonium ion + X⁻
Step 2: H₂O attacks halonium ion → Halohydrin
```
- **Regiochemistry**: OH adds to more substituted carbon
- Water is nucleophile (not X⁻) due to high concentration
- Anti stereochemistry

### 4. Oxymercuration-Demercuration
```
Step 1: Alkene + Hg(OAc)₂ → Mercurinium ion
Step 2: H₂O attacks → Organomercury intermediate
Step 3: NaBH₄ → Demercuration → Alcohol
```
- **Markovnikov product** (no rearrangement)
- Anti addition of Hg and OH
- Demercuration replaces Hg with H

### 5. Hydroboration-Oxidation
```
Step 1: BH₃ adds to alkene → Alkylborane (R₃B)
Step 2: H₂O₂, OH⁻ → Oxidation → Alcohol
```
- **Concerted, one-step** addition of B and H
- **Anti-Markovnikov**: B adds to less substituted carbon
- **Syn stereochemistry**: B and H add from same face
- No carbocation → no rearrangements
- Bulky boranes (disiamylborane) used for terminal alkynes

### 6. Hydrogenation
```
Alkene + H₂ + Pd/C → Alkane
```
- **Syn addition**: Both H add from same face (surface catalysis)
- Heterogeneous catalysis
- Alkene adsorbed on catalyst surface
- Heats of hydrogenation indicate relative stability

### 7. Epoxidation
```
Alkene + RCO₃H (peroxyacid) → Epoxide
```
- **Syn addition** of oxygen
- One-step, concerted mechanism
- m-CPBA commonly used
- Epoxides are strained, reactive

### 8. Dihydroxylation
**Syn dihydroxylation** (OsO₄):
```
Alkene + OsO₄ → Cyclic osmate → NaHSO₃ → cis-diol
```
- Syn addition of two OH groups
- OsO₄ toxic, expensive → use catalytic with NMO

**Anti dihydroxylation** (epoxide hydrolysis):
```
Alkene → Epoxide → H₃O⁺ → trans-diol
```
- Two steps: epoxidation, then acid-catalyzed ring opening

### 9. Ozonolysis
```
Alkene + O₃ (−78°C) → Molozonide → Ozonide
Ozonide + Zn, AcOH → Carbonyl compounds
```
- **Cleaves C=C bond**
- Alkene becomes two carbonyl groups
- Terminal alkene → aldehyde (with Zn reduction)
- Internal alkene → ketones/aldehydes depending on substitution
- Ozone workup with DMS (no Zn) also gives carbonyls

## Selectivity Rules

### Choosing Hydration Method

| Goal | Method | Reason |
|------|--------|--------|
| Markovnikov alcohol | Oxymercuration | No rearrangement, reliable |
| Anti-Markovnikov alcohol | Hydroboration-oxidation | Syn addition, less substituted |
| Avoid carbocation rearrangement | Either oxymercuration or hydroboration | No carbocation intermediate |

### Carbocation Rearrangement Decision
**Will rearrangement occur?**
- Look for: 2° carbocation that can become 3°
- Look for: Possibility of ring expansion to more stable ring
- Check for: Adjacent groups that can migrate

**Avoid rearrangement by**:
- Oxymercuration (no carbocation)
- Hydroboration (no carbocation)

### Stereoselectivity Decision Tree
```
Need syn addition?
  → Hydroboration, hydrogenation, OsO₄ dihydroxylation, epoxidation

Need anti addition?
  → Halogenation (X₂), halohydrin formation, acid-catalyzed epoxide opening

No stereochemical preference?
  → Simple HX addition, acid-catalyzed hydration
```

## Common Exam Patterns

### Pattern 1: Predict Addition Product
**Given**: Alkene + reagent
**Task**: Draw product with correct regiochemistry and stereochemistry

**Example**: 2-methyl-2-butene + BH₃, then H₂O₂/OH⁻
**Answer**: 3-methyl-2-butanol (anti-Markovnikov, syn)

### Pattern 2: Carbocation Rearrangement
**Given**: Alkene that forms 2° carbocation
**Task**: Predict if rearrangement occurs, show rearranged product

**Signs of rearrangement**:
- 2° → 3° possible
- Ring expansion (cyclobutyl → cyclopentyl)
- 1,2-hydride or alkyl shift

### Pattern 3: Ozonolysis Structure Determination
**Given**: Ozonolysis products
**Task**: Determine original alkene structure

**Method**: Remove O from each carbonyl, connect the carbons

**Example**: Ozonolysis gives acetone + acetaldehyde
**Answer**: 2-methyl-2-butene

### Pattern 4: Choose Synthesis Route
**Given**: Target alcohol, choose alkene precursor

**Example**: Synthesize 2-pentanol
**Options**:
- From 1-pentene via oxymercuration (Markovnikov) ✓
- From 2-pentene via hydroboration (mixture possible)

### Pattern 5: Stereochemistry Problems
**Given**: Cycloalkene + reagent
**Task**: Predict stereochemistry of product

**Examples**:
- Cyclohexene + Br₂ → trans-1,2-dibromocyclohexane (anti)
- Cyclohexene + OsO₄ → cis-1,2-cyclohexanediol (syn)
- Cyclohexene + m-CPBA → epoxide (syn), then H₃O⁺ → trans-diol (anti overall)

### Pattern 6: Hydroboration Regiochemistry
**Common mistake**: Applying Markovnikov rule to hydroboration

**Remember**: Hydroboration gives **anti-Markovnikov** addition
- B adds to less substituted carbon
- After oxidation: OH on less substituted carbon

### Pattern 7: Relative Alkene Stability
**Given**: Heats of hydrogenation
**Task**: Rank alkene stability

**Rules**:
- More substituted = more stable
- Trans > cis (E > Z) due to sterics
- Conjugated > isolated
- Cyclic constraints affect stability

**Stability order**: tetrasubstituted > trisubstituted > trans-disubstituted > cis-disubstituted > monosubstituted > unsubstituted

### Pattern 8: Synthesis Problems
**Common alkene synthesis methods**:
1. Dehydration of alcohols (H₂SO₄, heat) → Zaitsev product
2. Dehydrohalogenation of alkyl halides (strong base) → Zaitsev or Hofmann
3. Wittig reaction (carbonyl + Ph₃P=CHR)
4. Elimination reactions (E1, E2)

**Dehydration regioselectivity**: Zaitsev rule (more substituted alkene favored)
