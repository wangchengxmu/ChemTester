---
id: alkene.chemistry
layer: 2
title: Alkene Chemistry - Structure, Reactivity, and Synthesis
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/alkene_tools.py
  - ../L4_reference/reference/alkene-reactions-reference.md
cross_links:
  - ./organic_functional_groups.md
  - ./organic_reaction_mechanisms.md
  - ./stereochemistry_chirality.md
source: Organic Chemistry (OpenStax), Ch07-08
---

## Context
Alkenes are unsaturated hydrocarbons containing carbon-carbon double bonds (C=C). The double bond consists of one σ bond and one π bond, making alkenes significantly more reactive than alkanes. Alkene chemistry is foundational to organic synthesis and industrial chemistry.

## Structure and Properties

### Electronic Structure of the Double Bond
- **σ bond**: sp²-sp² overlap, strong, along bond axis
- **π bond**: p-p overlap, weaker, above and below bond plane
- **Bond energy**: C=C ~611 kJ/mol (vs C-C ~347 kJ/mol)
- **Bond length**: C=C ~134 pm (vs C-C ~154 pm)
- **Geometry**: Trigonal planar, ~120° bond angles

### Degree of Unsaturation (Index of Hydrogen Deficiency)
For formula CₙHₓ:
```
DoU = (2n + 2 - x) / 2

Each degree represents:
- 1 double bond, OR
- 1 ring, OR
- 1 triple bond = 2 DoU
```

| Formula | DoU | Interpretation |
|---------|-----|----------------|
| C₅H₁₂ | 0 | Saturated (alkane) |
| C₅H₁₀ | 1 | 1 double bond OR 1 ring |
| C₅H₈ | 2 | 2 double bonds, 1 triple, 2 rings, or 1 double + 1 ring |

## Nomenclature

### IUPAC Rules for Alkenes
1. Find longest chain containing the double bond
2. Number from end nearest the double bond
3. Name as "alkene" with position number
4. For substituents, use standard alkyl names

### Examples
| Structure | IUPAC Name |
|-----------|------------|
| CH₂=CH-CH₂-CH₃ | But-1-ene |
| CH₃-CH=CH-CH₃ | But-2-ene |
| (CH₃)₂C=CH₂ | 2-Methylprop-1-ene |

## Stereochemistry: E/Z Designation

### Cis-Trans vs E/Z
- **Cis**: Same side (limited to simple cases)
- **Trans**: Opposite sides (limited to simple cases)
- **E (entgegen)**: Higher priority groups opposite
- **Z (zusammen)**: Higher priority groups same side

### Cahn-Ingold-Prelog Priority Rules
1. Higher atomic number = higher priority
2. If tied, look at next atoms outward
3. Multiple bonds count as multiple single bonds

### E/Z Examples
```
Z-isomer (cis-like):      E-isomer (trans-like):
    CH₃   H                    CH₃   CH₃
      \ /                        \ /
       C=C                        C=C
      / \                        / \
    CH₃   H                    H     H
```

## Alkene Stability

### Stability Order
| Type | Relative Stability | Reason |
|------|-------------------|--------|
| Tetrasubstituted | Most stable | Most hyperconjugation |
| Trisubstituted | High | Good hyperconjugation |
| trans-Disubstituted | Moderate | Less steric strain |
| cis-Disubstituted | Moderate | Some steric strain |
| Monosubstituted | Less stable | Limited hyperconjugation |
| Unsubstituted (ethene) | Least stable | No hyperconjugation |

### Heat of Hydrogenation Data
| Alkene | ΔH°hydrogenation (kJ/mol) |
|--------|---------------------------|
| Ethene | -137 |
| Propene | -125 |
| But-1-ene | -127 |
| cis-But-2-ene | -119 |
| trans-But-2-ene | -115 |
| 2-Methylpropene | -119 |

## Electrophilic Addition Reactions

### General Mechanism
1. **Step 1**: Electrophile attacks π bond → carbocation intermediate
2. **Step 2**: Nucleophile attacks carbocation → product

```
    H⁺                   H
     |                    |
C=C  →  C-C⁺  →  C-C-Nu
              |
             Nu⁻
```

### Markovnikov's Rule
- "The rich get richer": H adds to carbon with more H atoms
- More substituted carbocation is favored
- Explained by carbocation stability (3° > 2° > 1°)

### Regioselectivity Summary
| Alkene + Reagent | Major Product | Rule |
|------------------|---------------|------|
| Propene + HBr | 2-Bromopropane | Markovnikov |
| Propene + H₂O/H⁺ | Propan-2-ol | Markovnikov |

## Carbocation Stability and Rearrangements

### Stability Order
```
3° > 2° > 1° > methyl

         CH₃
          |
CH₃-C⁺-CH₃  >  CH₃-CH⁺-CH₃  >  CH₃-CH₂⁺  >  CH₃⁺
 (tertiary)      (secondary)    (primary)   (methyl)
```

### Carbocation Rearrangements
- **Hydride shift**: H migrates with electron pair
- **Alkyl shift**: Alkyl group migrates with electron pair
- Always toward more stable carbocation

```
Example - Hydride Shift:
CH₃-CH₂-CH⁺-CH₃  →  CH₃-CH⁺-CH₂-CH₃
  (secondary)          (tertiary after shift)
```

## Major Alkene Reactions

### 1. Hydrohalogenation (HX Addition)
```
C=C + HX → C-C-X
```
- Reagents: HCl, HBr, HI
- Markovnikov regioselectivity
- Carbocation mechanism

### 2. Halogenation (X₂ Addition)
```
C=C + X₂ → X-C-C-X (vicinal dihalide)
```
- Reagents: Br₂, Cl₂
- Anti addition stereochemistry
- Halonium ion intermediate

### 3. Halohydrin Formation
```
C=C + X₂ + H₂O → X-C-C-OH
```
- X adds first (electrophile)
- OH adds to more substituted carbon
- Anti addition

### 4. Hydration (H₂O Addition)
**Acid-catalyzed (Markovnikov):**
```
C=C + H₂O/H⁺ → C-C-OH
```

**Oxymercuration-demercuration:**
- Markovnikov product
- No rearrangements

**Hydroboration-oxidation:**
- Anti-Markovnikov product
- Syn addition

**Detailed Hydroboration-Oxidation Mechanism:**
1. **Step 1 - Hydroboration**: BH₃ adds to the alkene
   - Boron attaches to LESS substituted carbon (anti-Markovnikov)
   - H attaches to MORE substituted carbon
   - Syn addition (both add from same face)
   - Four-center transition state (no carbocation intermediate)

2. **Step 2 - Oxidation**: H₂O₂/OH⁻ replaces B with OH
   - Retains the anti-Markovnikov regiochemistry
   - Overall: OH ends up on less substituted carbon

**Examples of Hydroboration-Oxidation:**
| Alkene | Product | Why? |
|--------|---------|------|
| Propene | 1-Propanol | OH on less substituted C1 |
| 1-Butene | 1-Butanol | OH on terminal carbon |
| 2-Methyl-2-butene | 3-Methyl-2-butanol | Wait - this is incorrect! |
| 3-Methyl-1-butene | 3-Methyl-2-butanol | OH on C1 (less substituted) |

**Reverse Problem: Finding the Alkene from the Alcohol**
To find the starting alkene for a given hydroboration product:
1. Identify the carbon bearing the OH group
2. This carbon was the LESS substituted carbon of the double bond
3. The other carbon of the double bond was one position toward the more substituted end

**Example**: What alkene gives 3-methyl-2-butanol via hydroboration?
- 3-Methyl-2-butanol has OH on C2
- In hydroboration, OH goes to less substituted carbon
- So the double bond was between C1 and C2 (less substituted end)
- Starting alkene: 3-Methyl-1-butene

### 5. Hydrogenation
```
C=C + H₂ (catalyst) → C-C
```
- Catalysts: Pd, Pt, Ni
- Syn addition
- Heat of hydrogenation indicates stability

**IMPORTANT: Hydrogenation does NOT cause carbocation rearrangements.**
- Hydrogenation is a concerted addition of H₂ across the double bond via a surface-catalyzed mechanism
- No carbocation intermediate is formed
- The carbon skeleton remains unchanged - substituents stay in place
- Examples:
  - Methylenecyclopentane + H₂ → Methylcyclopentane (NOT dimethylcyclopentane)
  - 2-Methyl-2-pentene + H₂ → 2-Methylpentane (skeleton unchanged)
  - Any alkene + H₂ → corresponding alkane with same carbon framework

### 6. Hydroxylation
**Syn hydroxylation (OsO₄ or KMnO₄, cold):**
```
C=C → HO-C-C-OH (cis-1,2-diol)
```

**Anti hydroxylation (epoxidation then hydrolysis):**
```
C=C → C-O-C (epoxide) → HO-C-C-OH (trans-1,2-diol)
```

### 7. Ozonolysis
```
C=C + O₃ → (reductive workup) → 2 C=O compounds
```
- Cleaves double bond
- Useful for structure determination

### 8. Cyclopropanation
```
C=C + :CH₂ (carbene) → cyclopropane
```
- Simmons-Smith reagent: CH₂I₂ + Zn(Cu)
- Syn addition

## Synthesis of Alkenes

### Elimination Reactions

**E1 Mechanism:**
1. Ionization to carbocation
2. Base removes β-H
- Favored by: weak base, polar solvent, good leaving group

**E2 Mechanism:**
1. Concerted elimination
- Favored by: strong base, high temperature
- Anti-periplanar geometry required

### Zaitsev's Rule
- More substituted alkene is favored (more stable)
- Exception: bulky base favors less substituted (Hofmann product)

### Preparation Methods
| Method | Reaction Type | Major Product |
|--------|---------------|---------------|
| Dehydration of alcohols | E1 | Zaitsev product |
| Dehydrohalogenation | E2 | Zaitsev or Hofmann |
| Cracking of alkanes | Thermal | Mixture |

## Reaction Summary Table

| Reaction | Reagent(s) | Product | Stereochemistry |
|----------|------------|---------|-----------------|
| Hydrohalogenation | HX | Alkyl halide | Markovnikov |
| Halogenation | X₂ | Vicinal dihalide | Anti |
| Halohydrin formation | X₂, H₂O | Halohydrin | Anti |
| Hydration (acid) | H₂O, H⁺ | Alcohol | Markovnikov |
| Oxymercuration | Hg(OAc)₂, H₂O | Alcohol | Markovnikov, no rearrangement |
| Hydroboration | BH₃, H₂O₂/OH⁻ | Alcohol | Anti-Markovnikov, syn |
| Hydrogenation | H₂, Pd/Pt/Ni | Alkane | Syn |
| Epoxidation | RCO₃H | Epoxide | Syn |
| Ozonolysis | O₃, (CH₃)₂S | Carbonyls | - |

## Decision Flow
1. Identify alkene substitution pattern
2. Determine if stereoisomers (E/Z) are relevant
3. For reactions: identify electrophile/nucleophile
4. Consider regioselectivity (Markovnikov vs anti-Markovnikov)
5. Consider stereoselectivity (syn vs anti)
6. Check for possible rearrangements

## L3 Tool Call Directive

When predicting alkene reaction products, call the appropriate L3 function:

**Alkene reaction predictor** (`L3_functions/alkene_tools.py`):
- Use when: Predict the product(s) of an alkene reaction given the alkene structure and reagent.
- Parameters: Varies — inspect `alkene_tools.py` for specific function signatures.

**Critical notes:**
- Alkene reactions are product-prediction problems. If no suitable L3 function covers the specific reaction, use the L2 knowledge above (reaction table and decision flow) to reason through the mechanism and predict products.
- Key factors: substitution pattern (mono/di/tri/tetra), regioselectivity (Markovnikov vs anti-Markovnikov), stereoselectivity (syn vs anti).
- For acid-catalyzed hydration: Markovnikov addition (H adds to less substituted carbon).
- For hydroboration-oxidation: anti-Markovnikov, syn addition.
- For halogenation (Br₂/Cl₂): anti addition via halonium ion.
- For oxymercuration-demercuration: Markovnikov without rearrangement.

## Implementations and Data
- Alkene reaction predictor: [L3 code](../L3_functions/alkene_tools.py)
- Reaction reference tables: [L4 reference](../L4_reference/reference/alkene-reactions-reference.md)
