---
id: carbonyl.chemistry
layer: 2
title: Carbonyl Chemistry - Aldehydes, Ketones, and Derivatives
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/functional_group_tools.py
  - ../L4_reference/reference/alkene-reactions-reference.md
cross_links:
  - ./alcohol_chemistry.md
  - ./organic_reaction_mechanisms.md
  - ./acid_base_constants.md
source: Organic Chemistry (OpenStax), Ch19-23
---

## Context
Carbonyl compounds contain the C=O functional group and are among the most important in organic chemistry. The carbonyl group is polar (Cδ⁺-Oδ⁻), making it susceptible to nucleophilic attack. Aldehydes, ketones, carboxylic acids, and their derivatives form the basis of much organic synthesis.

## Structure and Reactivity

### The Carbonyl Group
- **Bond polarity**: Cδ⁺-Oδ⁻ (oxygen more electronegative)
- **Bond length**: ~122 pm (C=O)
- **Hybridization**: sp² on carbon, trigonal planar
- **Resonance**: Partial double bond character in amides

### Reactivity Order (Most to Least Reactive)
```
Acid chlorides > Anhydrides > Aldehydes > Ketones > Esters > Amides
```

### Factors Affecting Reactivity
| Factor | Effect |
|--------|--------|
| Steric hindrance | More hindered = less reactive |
| Electronic effects | EWG = more reactive; EDG = less reactive |
| Leaving group ability | Better leaving group = more reactive |

## Aldehydes and Ketones

### Structure
- **Aldehydes**: R-CHO (at least one H on carbonyl carbon)
- **Ketones**: R-CO-R' (two alkyl/aryl groups)

### Nomenclature
| Type | Suffix | Example |
|------|--------|---------|
| Aldehyde | -al | Ethanal, Benzaldehyde |
| Ketone | -one | Propanone, Butan-2-one |

### Synthesis
| Method | Starting Material | Product |
|--------|-------------------|---------|
| Oxidation of 1° alcohols | R-CH₂-OH | R-CHO (PCC) |
| Oxidation of 2° alcohols | R₂CH-OH | R₂C=O |
| Ozonolysis of alkenes | R-C=C-R' | R-CHO + R'-CHO |
| Hydration of alkynes | R-C≡C-H | R-CO-CH₃ |

## Nucleophilic Addition to Aldehydes/Ketones

### General Mechanism
1. Nucleophile attacks carbonyl carbon
2. Tetrahedral intermediate forms
3. Protonation of oxygen

```
    O                    O⁻                OH
    ||        Nu⁻       |      H⁺        |
R-C    →    R-C-Nu  →  R-C-Nu
    |                    |                 |
    R                    R                 R
```

### Common Nucleophilic Additions

| Nucleophile | Product | Application |
|-------------|---------|-------------|
| H⁻ (NaBH₄, LiAlH₄) | Alcohol | Reduction |
| R⁻ (Grignard) | Alcohol (after workup) | C-C bond formation |
| H₂O | Hydrate (gem-diol) | Usually minor |
| ROH | Hemiacetal → Acetal | Protecting groups |
| NH₃, amines | Imine/enamine | Characterization |
| CN⁻ | Cyanohydrin | C-C bond formation |
| PPh₃ (Wittig) | Alkene | C=C formation |

### Acetal Formation
```
Aldehyde/Ketone + 2 ROH ⇌ Acetal + H₂O
```
- Acid catalyzed
- Reversible (useful as protecting group)
- Hemiacetal is intermediate

### Imine Formation
```
R₂C=O + R'-NH₂ → R₂C=N-R' + H₂O
```
- Acid catalyzed
- Used for amine synthesis (reductive amination)

## Carboxylic Acids and Derivatives

### Structure
- **Carboxylic acid**: R-COOH
- **Acid chloride**: R-COCl
- **Anhydride**: R-CO-O-CO-R'
- **Ester**: R-COOR'
- **Amide**: R-CONH₂

### Acidity of Carboxylic Acids
- **pKa ≈ 4-5** (much more acidic than alcohols)
- Reason: Resonance stabilization of carboxylate anion

### Synthesis
| Method | Starting Material | Product |
|--------|-------------------|---------|
| Oxidation of 1° alcohols | R-CH₂-OH | R-COOH |
| Oxidation of aldehydes | R-CHO | R-COOH |
| Grignard + CO₂ | R-MgX + CO₂ | R-COOH |
| Hydrolysis of nitriles | R-CN | R-COOH |

## Nucleophilic Acyl Substitution

### General Mechanism
1. Nucleophile attacks carbonyl
2. Tetrahedral intermediate
3. Leaving group departs

```
    O                    O⁻               O
    ||        Nu⁻       |      -LG⁻      ||
R-C-LG  →  R-C-Nu  →  R-C-Nu
                              |
                              Nu
```

### Interconversion of Derivatives
```
Acid chloride → Anhydride → Ester → Amide
    ↓              ↓          ↓       ↓
  (more reactive)          (less reactive)
```
- Can only go down in reactivity
- Each step requires appropriate nucleophile

### Hydrolysis Reactions
| Derivative | Hydrolysis Conditions | Product |
|------------|----------------------|---------|
| Acid chloride | H₂O | Carboxylic acid |
| Anhydride | H₂O | 2 Carboxylic acids |
| Ester | H₂O, H⁺ or OH⁻ | Carboxylic acid + alcohol |
| Amide | H₂O, H⁺ or OH⁻, heat | Carboxylic acid + amine |

## Enolate Chemistry

### α-Hydrogen Acidity
- α-Hydrogens are acidic due to resonance stabilization
- **pKa ≈ 19-20** for ketones
- **pKa ≈ 25** for esters

### Enolate Formation
```
R-CH₂-CO-R' + base → R-CH⁻-CO-R' (enolate)
                      |
```

### Important Enolate Reactions

**1. Aldol Condensation**
```
2 R-CH₂-CHO → R-CH(OH)-CH(R)-CHO → R-CH=CH-CHO (α,β-unsaturated)
```

**2. Claisen Condensation (esters)**
```
2 R-CH₂-COOR' → R-CH(COOR')-CH₂-COOR'
```

**3. Alkylation**
```
Enolate + R'-X → R-CH(R')-CO-R'
```

**4. Michael Addition**
```
Enolate + α,β-unsaturated carbonyl → 1,4-addition product
```

## Carbonyl Reaction Summary

| Reaction Type | Substrate | Reagent | Product |
|---------------|-----------|---------|---------|
| Reduction | Aldehyde | NaBH₄ | 1° Alcohol |
| Reduction | Ketone | NaBH₄ | 2° Alcohol |
| Reduction | Ester | LiAlH₄ | 1° Alcohol |
| Grignard | Aldehyde | R-MgX | 2° Alcohol |
| Grignard | Ketone | R-MgX | 3° Alcohol |
| Grignard | Ester | 2 R-MgX | 3° Alcohol |
| Wittig | Aldehyde/Ketone | Ph₃P=CHR | Alkene |
| Acetal formation | Aldehyde/Ketone | ROH, H⁺ | Acetal |
| Aldol | Aldehyde | base | β-hydroxy aldehyde |
| Claisen | Ester | base | β-keto ester |

## Decision Flow
1. Identify carbonyl type (aldehyde/ketone vs derivative)
2. For nucleophilic addition: consider sterics and electronics
3. For acyl substitution: consider leaving group ability
4. For enolate chemistry: check for α-hydrogen
5. Consider protecting groups for multi-step synthesis

## Implementations and Data
- Carbonyl reaction predictor: [L3 code](../L3_functions/functional_group_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/alkene-reactions-reference.md)
