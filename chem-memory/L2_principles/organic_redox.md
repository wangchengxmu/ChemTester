---
id: organic.redox
layer: 2
title: Oxidation and Reduction in Organic Chemistry
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/reaction_mechanism_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./alcohol_chemistry.md
  - ./alkene_chemistry.md
  - ./carbonyl_chemistry.md
source: Organic Chemistry (OpenStax), Ch10.8
---

## Context
Oxidation and reduction in organic chemistry differ from inorganic redox in that electrons are often transferred as hydride ions (H⁻) or in conjunction with proton transfer. Understanding oxidation levels helps classify reactions and predict reactivity patterns.

## Definitions

### Organic Oxidation
Decreases electron density on carbon by:
- **Forming bonds** to more electronegative atoms (O, N, X)
- **Breaking bonds** to less electronegative atoms (H)

### Organic Reduction
Increases electron density on carbon by:
- **Forming bonds** to less electronegative atoms (H)
- **Breaking bonds** to more electronegative atoms (O, N, X)

### Summary Table

| Process | Bond Formed | Bond Broken |
|---------|-------------|-------------|
| Oxidation | C-O, C-N, C-X | C-H |
| Reduction | C-H | C-O, C-N, C-X |

## Oxidation Level Calculation

### Formula
```
Oxidation Level = (# C-O, C-N, C-X bonds) - (# C-H bonds)
```

Higher value = more oxidized state

### Examples

| Compound | C-H | C-O | C-N | C-X | Oxidation Level |
|----------|-----|-----|-----|-----|-----------------|
| Methane, CH₄ | 4 | 0 | 0 | 0 | -4 |
| Ethane, C₂H₆ | 6 | 0 | 0 | 0 | -6 |
| Ethene, C₂H₄ | 4 | 0 | 0 | 0 | -4 |
| Ethyne, C₂H₂ | 2 | 0 | 0 | 0 | -2 |
| Methanol, CH₃OH | 3 | 1 | 0 | 0 | -2 |
| Ethanol, C₂H₅OH | 5 | 1 | 0 | 0 | -4 |
| Formaldehyde, HCHO | 2 | 1 | 0 | 0 | -1 |
| Acetaldehyde, CH₃CHO | 3 | 1 | 0 | 0 | -2 |
| Acetone, (CH₃)₂CO | 6 | 1 | 0 | 0 | -4 |
| Formic acid, HCOOH | 1 | 2 | 0 | 0 | +1 |
| Acetic acid, CH₃COOH | 3 | 2 | 0 | 0 | -1 |
| CO₂ | 0 | 4 | 0 | 0 | +4 |
| Chloromethane, CH₃Cl | 3 | 0 | 0 | 1 | -2 |

## Oxidation Level Hierarchy

### General Ordering (lowest to highest)
```
Alkane < Alkene/Alkyne < Alcohol < Aldehyde/Ketone < Carboxylic Acid < CO₂
```

### Visual Representation
```
         CO₂ (highest oxidation)
           ↑
    Carboxylic acids
           ↑
   Aldehydes/Ketones
           ↑
       Alcohols
           ↑
   Alkenes/Alkynes
           ↑
      Alkanes (lowest oxidation)
```

## Classifying Reactions

### Oxidation Reactions
| Transformation | Bonds Changed | Classification |
|----------------|---------------|----------------|
| CH₄ → CH₃Cl | C-H broken, C-Cl formed | Oxidation |
| Alkene + Br₂ → 1,2-Dibromide | Two C-Br formed | Oxidation |
| Alcohol → Aldehyde | C-H broken, C-O formed | Oxidation |
| Aldehyde → Carboxylic acid | C-H broken, C-O formed | Oxidation |
| Alkene → Epoxide | Two C-O formed | Oxidation |

### Reduction Reactions
| Transformation | Bonds Changed | Classification |
|----------------|---------------|----------------|
| R-Cl → R-H (via Grignard) | C-Cl broken, C-H formed | Reduction |
| Aldehyde → Alcohol | C-O broken, C-H formed | Reduction |
| Ketone → Alcohol | C-O broken, C-H formed | Reduction |
| Alkene → Alkane | Two C-H formed | Reduction |
| Carboxylic acid → Alcohol | C-O broken, C-H formed | Reduction |

### Neither Oxidation Nor Reduction
| Transformation | Bonds Changed | Classification |
|----------------|---------------|----------------|
| Alkene + HBr → Alkyl bromide | C-H and C-Br formed | Neither |
| Alcohol → Ether (Williamson) | C-O formed | Neither |
| Alkene + H₂O → Alcohol | C-H and C-O formed | Neither |

## Common Oxidizing Agents

### By Functional Group Transformation

| Substrate | Product | Reagent | Notes |
|-----------|---------|---------|-------|
| 1° Alcohol | Aldehyde | PCC | Mild, stops at aldehyde |
| 1° Alcohol | Carboxylic acid | Na₂Cr₂O₇, H⁺ | Stronger oxidant |
| 2° Alcohol | Ketone | Na₂Cr₂O₇ or PCC | |
| Alkene | Epoxide | mCPBA | Peracid |
| Alkene | Diol | OsO₄, then NaHSO₃ | Syn addition |
| Aldehyde | Carboxylic acid | Ag₂O (Tollens) | Silver mirror test |
| Aldehyde | Carboxylic acid | KMnO₄ | |

## Common Reducing Agents

### By Functional Group Transformation

| Substrate | Product | Reagent | Notes |
|-----------|---------|---------|-------|
| Aldehyde | 1° Alcohol | NaBH₄ or LiAlH₄ | |
| Ketone | 2° Alcohol | NaBH₄ or LiAlH₄ | |
| Carboxylic acid | 1° Alcohol | LiAlH₄ | Stronger needed |
| Ester | 1° Alcohol | LiAlH₄ (2 equiv) | |
| Alkene | Alkane | H₂, Pd/C | Hydrogenation |
| Alkyne | Alkene | H₂, Lindlar | Cis product |
| Alkyne | Alkene | Na, NH₃(l) | Trans product |
| Acid chloride | Aldehyde | LiAlH(Ot-Bu)₃ | Selective |

## Oxidation in Biological Systems

### Key Coenzymes

| Coenzyme | Role | Reduced Form |
|----------|------|--------------|
| NAD⁺ | Electron acceptor | NADH + H⁺ |
| NADP⁺ | Electron acceptor | NADPH + H⁺ |
| FAD | Electron acceptor | FADH₂ |
| Coenzyme Q | Electron carrier | CoQH₂ |

### Biological Oxidation Examples
- Alcohol dehydrogenase: Ethanol → Acetaldehyde (NAD⁺ → NADH)
- Aldehyde dehydrogenase: Acetaldehyde → Acetic acid
- β-Oxidation: Fatty acids → Acetyl-CoA

## Decision Flow

1. **Calculate oxidation level:**
   - Count C-O, C-N, C-X bonds (positive contribution)
   - Count C-H bonds (negative contribution)
   - Higher number = more oxidized

2. **Compare oxidation levels:**
   - Only valid for same number of carbons

3. **Classify reaction:**
   - Reactant → Product with higher oxidation level = Oxidation
   - Reactant → Product with lower oxidation level = Reduction
   - Same level = Neither

4. **Choose reagent:**
   - For oxidation: Select based on desired product and selectivity
   - For reduction: Match reducing agent to substrate

## Problem-Solving Examples

### Example 1: Compare Oxidation Levels
Rank: Propene, 2-propanol, acetone, propane

**Solution:**
- Propane: 8 C-H, 0 C-O → Level = -8
- Propene: 6 C-H, 0 C-O → Level = -6
- 2-Propanol: 7 C-H, 1 C-O → Level = -6
- Acetone: 6 C-H, 1 C-O → Level = -4

**Order (increasing):** Propane < Propene = 2-Propanol < Acetone

### Example 2: Classify Reaction
CH₃CH₂OH → CH₃CHO (ethanol to acetaldehyde)

**Analysis:**
- Ethanol: 5 C-H, 1 C-O → Level = -4
- Acetaldehyde: 3 C-H, 1 C-O → Level = -2
- Level increases: -4 → -2

**Answer:** Oxidation

## Implementations and Data
- Oxidation level calculator: [L3 code](../L3_functions/reaction_mechanism_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)

## L3 Tool Call Directives

**Source:** `redox_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
