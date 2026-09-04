---
id: organic.openstax_ch18
layer: 2
title: Ethers and Epoxides; Thiols and Sulfides
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Ethers and Epoxides; Thiols and Sulfides

## Key Principles

### Ether Properties
- **Structure**: R-O-R' (two organic groups bonded to oxygen)
- **Polarity**: Moderate (C-O dipole)
- **Stability**: Generally unreactive, good solvents
- **Acid stability**: Stable to bases, most acids
- **Hazard**: Form explosive peroxides on storage (especially cyclic ethers like THF)

### Epoxide Properties
- **Structure**: Three-membered cyclic ether (oxirane)
- **Ring strain**: High (~114 kJ/mol) → very reactive
- **Reactivity**: Undergo ring-opening with many nucleophiles
- **Stereochemistry**: Can give specific stereoisomers

### Thiols and Sulfides
- **Thiols (R-SH)**: Sulfur analogs of alcohols
- **Sulfides (R-S-R')**: Sulfur analogs of ethers
- **Properties**: Lower boiling points than alcohols (no H-bonding)
- **Odor**: Strong, distinctive (garlic, skunk)
- **Oxidation**: Thiols → disulfides; sulfides → sulfoxides → sulfones

## Mechanisms

### 1. Williamson Ether Synthesis
```
R-O⁻ + R'-X → R-O-R' + X⁻ (SN2)
```

**Requirements**:
- Alkoxide ion (R-O⁻) + alkyl halide/tosylate
- **Primary alkyl halide** preferred (SN2)
- Secondary halides: elimination competes
- Tertiary halides: elimination only

**Alkoxide preparation**:
```
R-OH + NaH → R-O⁻ Na⁺ + H₂
R-OH + Na → R-O⁻ Na⁺ + ½ H₂
```

**Design principle**: Use the more hindered alkoxide with less hindered halide
- Example: t-butyl methyl ether
  - Use t-butoxide + methyl iodide ✓
  - NOT methoxide + t-butyl chloride (E2 dominates)

### 2. Alkoxymercuration-Demercuration
```
Alkene + R-OH + Hg(OAc)₂ → Alkoxymercury intermediate
Alkoxymercury + NaBH₄ → Ether (Markovnikov)
```

**Features**:
- Markovnikov addition of alcohol to alkene
- No carbocation rearrangement
- Works for most ethers (except di-tertiary)
- Alternative to Williamson when SN2 conditions problematic

### 3. Acid-Catalyzed Ether Cleavage
```
R-O-R' + HX → R-X + R'-OH (excess HX → both become halides)
```

**Mechanism depends on substitution**:
- **Primary/secondary**: SN2 at less hindered carbon
- **Tertiary**: SN1 at tertiary carbon (carbocation intermediate)

**Order of HX reactivity**: HI > HBr > HCl

### 4. Epoxide Formation

**Method A: Peroxyacid epoxidation**
```
Alkene + RCO₃H → Epoxide
```
- m-CPBA commonly used
- Syn addition of oxygen
- Retains alkene stereochemistry

**Method B: Halohydrin cyclization**
```
Alkene + X₂, H₂O → Halohydrin
Halohydrin + Base → Epoxide
```
- Intramolecular SN2
- Anti addition of OH and X, then ring closure

### 5. Acid-Catalyzed Epoxide Opening
```
Epoxide + H⁺ → Protonated epoxide
Protonated epoxide + Nu⁻ → trans product
```

**Regiochemistry**:
- Primary + secondary carbons: **Attack at less substituted** (SN2-like)
- Tertiary carbon present: **Attack at more substituted** (SN1-like character)
- **Stereochemistry**: Anti (backside attack)

**Mechanistic subtlety**: 
- Transition state has both SN2 and SN1 character
- Nucleophile attacks from backside (SN2)
- But attacks more substituted carbon if tertiary (carbocation character)

### 6. Base-Catalyzed Epoxide Opening
```
Epoxide + Nu⁻ → Alkoxy product
```

**Regiochemistry**: Attack at **less substituted** carbon (pure SN2)
**Stereochemistry**: Anti (backside attack)

**Common nucleophiles**:
- OH⁻ → diol
- RO⁻ → alkoxy alcohol
- RNH₂ → amino alcohol
- RMgX → alcohol (extends carbon chain by 2)

### 7. Thiol Chemistry

**Formation**:
```
R-X + SH⁻ → R-SH (SN2)
```

**Oxidation**:
```
2 R-SH + [O] → R-S-S-R (disulfide)
```
- Disulfide formation important in protein structure
- Mild oxidants: I₂, O₂

**Acidity**: Thiols more acidic than alcohols (pKa ~10 vs ~16)
- S larger, more polarizable
- Thiolate (RS⁻) good nucleophile

### 8. Sulfide Chemistry

**Formation**:
```
R-X + R'-S⁻ → R-S-R' (SN2)
```

**Oxidation sequence**:
```
R-S-R → R-S(O)-R (sulfoxide) → R-SO₂-R (sulfone)
```
- H₂O₂ or peracids as oxidants
- Sulfoxides are chiral if R ≠ R'

## Selectivity Rules

### Williamson Ether Synthesis: Choosing Partners
```
Target: R-O-R'

If one group is tertiary:
  → Do NOT use tertiary halide (E2)
  → Use tertiary alkoxide + primary halide

If both groups primary/secondary:
  → Either direction works
  → Choose based on availability
```

### Epoxide Opening: Acid vs Base
```
Acid-catalyzed:
  - Tertiary carbon present → attack tertiary
  - Primary/secondary only → attack less substituted
  - Anti stereochemistry

Base-catalyzed:
  - Always attack less substituted carbon (SN2)
  - Anti stereochemistry
```

### Epoxide Opening with Grignard Reagents
```
Epoxide + RMgX → Alcohol (after workup)
```
- Extends chain by 2 carbons
- Ethylene oxide gives primary alcohol
- Attack at less substituted carbon

## Common Exam Patterns

### Pattern 1: Williamson Synthesis Design
**Question**: How to prepare a specific ether?

**Decision tree**:
1. Is one group tertiary? Use that group as alkoxide
2. Both primary/secondary? Either works
3. Use primary halide partner (SN2)

**Example**: t-butyl cyclohexyl ether
- Use t-butoxide + cyclohexyl halide (not cyclohexoxide + t-butyl halide)

### Pattern 2: Epoxide Opening Regiochemistry
**Question**: Predict product of epoxide + HX or epoxide + base

**Rules**:
| Conditions | Nucleophile attacks: |
|------------|----------------------|
| Acid + unsymmetrical (no tertiary) | Less substituted carbon |
| Acid + tertiary present | More substituted carbon |
| Base/Nu⁻ | Always less substituted |

**Example**: 2-methyl-1,2-epoxypropane + HCl
- Tertiary carbon → Cl attacks tertiary
- Product: 2-chloro-2-methyl-1-propanol

### Pattern 3: Epoxide Stereochemistry
**Question**: Show stereochemistry of ring opening

**Rules**:
- Always **anti** addition (backside attack)
- For cyclic epoxides: trans products
- Retain stereochemistry at carbon NOT attacked

**Example**: cis-2,3-epoxybutane + HBr
- Product: meso-2,3-dibromobutane (anti opening of both possibilities)

### Pattern 4: Synthesis via Epoxides
**Question**: How to synthesize specific alcohol from epoxide?

**Strategy**:
1. Identify target alcohol
2. Look for -CH₂-CH(OH)- pattern (epoxide opening)
3. Choose nucleophile:
   - R-MgX adds alkyl group
   - H⁻/LiAlH₄ adds H
   - OH⁻ gives diol

**Example**: 1-butanol from epoxide
- Ethylene oxide + CH₃CH₂MgBr → 1-butanol (after workup)

### Pattern 5: Thiol Oxidation/Disulfide
**Question**: Products of thiol oxidation/reduction

**Oxidation** (thiol to disulfide):
```
2 R-SH + I₂ → R-S-S-R + 2 HI
```

**Reduction** (disulfide to thiol):
```
R-S-S-R + 2 H⁻ → 2 R-SH
```

Biological significance: Disulfide bonds stabilize protein tertiary structure

### Pattern 6: Crown Ethers
**Question**: What does crown ether complex?

**Principle**: Match crown ether cavity size to cation diameter

| Crown Ether | Cavity Size | Best Cation |
|-------------|-------------|-------------|
| 12-crown-4 | 1.2 Å | Li⁺ |
| 15-crown-5 | 1.7 Å | Na⁺ |
| 18-crown-6 | 2.6 Å | K⁺ |

**Effect**: Solubilizes ionic compounds in organic solvents

### Pattern 7: Epoxide Synthesis from Alkenes
**Question**: Choose epoxidation method

| Method | Conditions | Notes |
|--------|------------|-------|
| m-CPBA | Neutral | Works for most alkenes |
| Halohydrin | Br₂/H₂O then base | Gives epoxide with anti stereochemistry |
| Sharpless | Ti, tartrate | Enantioselective for allylic alcohols |

### Pattern 8: Acidic Cleavage of Ethers
**Question**: Products of ether + HX

**Analysis**:
- Identify more substituted carbon (or both carbons)
- With excess HI or HBr: both groups become halides
- With limited HX: alcohol + halide possible

**Example**: Diisopropyl ether + excess HI
- Product: 2 equivalents of 2-iodopropane
