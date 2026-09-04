---
id: alcohol.chemistry
layer: 2
title: Alcohol Chemistry - Structure, Properties, and Reactions
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/functional_group_tools.py
  - ../L4_reference/reference/alkene-reactions-reference.md
cross_links:
  - ./alkene_chemistry.md
  - ./carbonyl_chemistry.md
  - ./organic_reaction_mechanisms.md
source: Organic Chemistry (OpenStax), Ch17
---

## Context
Alcohols contain the hydroxyl functional group (-OH) bonded to an sp³ hybridized carbon. They are versatile compounds in organic chemistry, serving as solvents, reagents, and intermediates in synthesis. Phenols are a special class where the OH is attached to an aromatic ring.

## Structure and Classification

### Classification by Substitution
| Type | Structure | Example |
|------|-----------|---------|
| Primary (1°) | R-CH₂-OH | Ethanol |
| Secondary (2°) | R₂CH-OH | Propan-2-ol |
| Tertiary (3°) | R₃C-OH | 2-Methylpropan-2-ol |

### Physical Properties
- **Hydrogen bonding**: Alcohols form H-bonds → higher boiling points
- **Solubility**: Small alcohols water-soluble; decreases with chain length
- **Acidity**: pKa ~16-18 (similar to water)

### Acidity Order
```
Methanol > Primary > Secondary > Tertiary
```
- More substituted = less acidic (steric hindrance to solvation)

## Nomenclature

### IUPAC Rules
1. Find longest chain containing OH group
2. Number from end nearest OH
3. Suffix: "-ol" with position number

### Examples
| Common Name | IUPAC Name |
|-------------|------------|
| Ethyl alcohol | Ethanol |
| Isopropyl alcohol | Propan-2-ol |
| tert-Butyl alcohol | 2-Methylpropan-2-ol |

## Synthesis of Alcohols

### 1. From Alkenes
| Method | Reagent | Product Type |
|--------|---------|--------------|
| Acid-catalyzed hydration | H₂O, H⁺ | Markovnikov |
| Oxymercuration | Hg(OAc)₂, H₂O | Markovnikov, no rearrangement |
| Hydroboration-oxidation | BH₃, H₂O₂/OH⁻ | Anti-Markovnikov |

### 2. Reduction of Carbonyl Compounds
| Substrate | Reagent | Product |
|-----------|---------|---------|
| Aldehyde | NaBH₄ or LiAlH₄ | Primary alcohol |
| Ketone | NaBH₄ or LiAlH₄ | Secondary alcohol |
| Carboxylic acid | LiAlH₄ | Primary alcohol |
| Ester | LiAlH₄ (2 equiv) | Primary alcohol + alcohol |

### 3. Grignard Reactions
```
R-MgX + HCHO → R-CH₂-OH (primary alcohol, +1 C)
R-MgX + R'-CHO → R-CH(R')-OH (secondary alcohol)
R-MgX + R₂C=O → R-C(R₂)-OH (tertiary alcohol)
```

### 4. From Epoxides
```
R-MgX + epoxide → alcohol (ring opening)
LiAlH₄ + epoxide → alcohol (hydride opening)
```

## Reactions of Alcohols

### 1. Dehydration (Elimination)
```
R-OH → R-C=C-R' (alkene)
```
- Reagents: H₂SO₄, heat
- Mechanism: E1 (carbocation intermediate)
- Zaitsev product favored

### 2. Substitution Reactions

**SN1 (tertiary alcohols):**
```
R₃C-OH + HX → R₃C-X + H₂O
```
- Carbocation intermediate
- H⁺ protonates OH to make good leaving group

**SN2 (primary, secondary):**
- Convert to tosylate first: R-OH → R-OTs
- Then nucleophilic substitution

### 3. Oxidation Reactions

**Primary alcohols:**
```
R-CH₂-OH → R-CHO → R-COOH
```
- PCC: stops at aldehyde
- Na₂Cr₂O₇, H⁺: goes to carboxylic acid

**Secondary alcohols:**
```
R₂CH-OH → R₂C=O (ketone)
```
- Na₂Cr₂O₇, H⁺ or PCC

**Tertiary alcohols:**
- No oxidation (no α-hydrogen)

### 4. Conversion to Other Functional Groups
| Reaction | Reagent | Product |
|----------|---------|---------|
| To alkyl halide | HX, PBr₃, SOCl₂ | R-X |
| To ester | R'COCl, pyridine | R-OCO-R' |
| To ether | R'X, base | R-O-R' (Williamson) |
| To tosylate | TsCl, pyridine | R-OTs |

## Phenols

### Structure and Properties
- OH attached directly to aromatic ring
- **More acidic than alcohols** (pKa ~10)
- Acidity explained by resonance stabilization of phenoxide

### Resonance Stabilization
```
        ⁻O           ⁻           ⁻
         |           |           |
    O→←Ph  ↔  O←Ph⁺  ↔  O←Ph⁺
```

### Reactions
| Reaction | Reagent | Product |
|----------|---------|---------|
| Electrophilic aromatic substitution | Br₂, HNO₃, etc. | Ortho/para products |
| Kolbe reaction | CO₂, NaOH, then H⁺ | Salicylic acid |
| Reimer-Tiemann | CHCl₃, NaOH | o-Hydroxybenzaldehyde |

## Protection of Alcohols

### Common Protecting Groups
| Protecting Group | Formation | Removal |
|------------------|-----------|---------|
| TBDMS ether | TBDMSCl, imidazole | F⁻ (TBAF) |
| THP ether | DHP, H⁺ | H⁺, H₂O |
| Acetate | Ac₂O, pyridine | Base, hydrolysis |

## Reaction Summary Table

| Transformation | Reagent(s) | Notes |
|----------------|------------|-------|
| Alcohol → Alkene | H₂SO₄, heat | E1, Zaitsev |
| Alcohol → Alkyl halide | HX, PBr₃, SOCl₂ | Depends on structure |
| 1° Alcohol → Aldehyde | PCC | Mild oxidation |
| 1° Alcohol → Carboxylic acid | Na₂Cr₂O₇, H⁺ | Strong oxidation |
| 2° Alcohol → Ketone | Na₂Cr₂O₇ or PCC | |
| Alkene → Alcohol | H₂O/H⁺ or BH₃/H₂O₂ | Markovnikov or anti- |
| Carbonyl → Alcohol | NaBH₄ or LiAlH₄ | Reduction |

## Decision Flow
1. Classify alcohol (1°, 2°, 3°)
2. For substitution: SN1 vs SN2 based on structure
3. For oxidation: choose reagent based on desired product
4. For synthesis: choose appropriate reduction or addition method
5. Consider protection for multi-step synthesis

## Implementations and Data
- Alcohol reaction predictor: [L3 code](../L3_functions/functional_group_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/alkene-reactions-reference.md)
