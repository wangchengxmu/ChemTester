---
id: organic.openstax_ch20
layer: 2
title: Carboxylic Acids and Nitriles
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - ../L4_reference/acidity_table.md
---

# Carboxylic Acids and Nitriles

## Key Principles

### Carboxylic Acid Structure
- Functional group: -COOH (carboxyl group)
- Planar sp2 carbon with carbonyl and hydroxyl
- Strong hydrogen bonding → high boiling points
- Carboxylate anion resonance stabilized

### Acidity of Carboxylic Acids
- Typical pKa: 4-5 (much stronger than alcohols, pKa ~16)
- Why? Resonance stabilization of carboxylate anion

```
R-COOH  ⇌  R-COO⁻  +  H⁺
        |
    O⁻——C=O  ↔  O=C——O⁻
    (resonance delocalizes negative charge)
```

### Nitrile Structure
- Functional group: -C≡N
- Linear sp hybridized carbon
- Strongly polarized C≡N bond
- Electrophilic carbon (like carbonyl)

## Mechanisms

### Dissociation and Acidity

**Resonance stabilization:**
- Negative charge shared equally between both oxygens
- More stable than alkoxide (charge on single oxygen)

**Inductive effects:**
- Electron-withdrawing groups increase acidity
- Electron-donating groups decrease acidity
- Effect decreases with distance from carboxyl

### Substituent Effects on Acidity

**Electron-withdrawing groups → stronger acid (lower pKa)**
- Inductive withdrawal stabilizes carboxylate
- Examples: -F, -Cl, -Br, -NO2, -CN, -CHO

**Electron-donating groups → weaker acid (higher pKa)**
- Destabilizes carboxylate by increasing electron density
- Examples: -CH3, -OH, -OCH3

**Distance effect:**
```
Cl-CH2-CH2-COOH  pKa = 4.52
Cl-CH2-COOH      pKa = 4.05
Cl-COOH          pKa = 2.86
```

**Benzoic acid substituent effects:**
- EWG on ring → stronger acid (stabilizes carboxylate)
- EDG on ring → weaker acid
- Same trend as EAS reactivity!

### Preparation of Carboxylic Acids

**1. Oxidation of Primary Alcohols**
```
R-CH2OH →[oxidant] R-CHO →[oxidant] R-COOH
```
- KMnO4, CrO3/H2SO4, Dess-Martin periodinane
- Aldehydes are intermediates

**2. Oxidation of Aldehydes**
```
R-CHO + [O] → R-COOH
```
- KMnO4, CrO3, Ag2O (Tollens'), Ag(NH3)2⁺

**3. Oxidation of Alkylbenzenes**
```
Ar-CH2R →[KMnO4] Ar-COOH
```
- Primary and secondary alkyl groups oxidize
- Tertiary alkyl groups unaffected

**4. Hydrolysis of Nitriles**
```
R-CN + H2O →[H⁺ or OH⁻] R-COOH + NH3
```
- Two-step: nitrile → amide → acid
- Nitriles from SN2 of CN⁻ on alkyl halides

**5. Grignard + CO2**
```
R-MgBr + CO2 → R-COO⁻Mg⁺ →[H3O⁺] R-COOH
```
- Adds one carbon
- Works for primary, secondary, tertiary

### Nitrile Chemistry

**Preparation:**
1. SN2 of CN⁻ on primary/secondary alkyl halides
2. Dehydration of amides (SOCl2 or P2O5)

**Reactions:**

**1. Hydrolysis to Carboxylic Acid**
```
R-CN + 2H2O →[H⁺ or OH⁻] R-COOH + NH3
```
- Acid or base catalyzed
- Goes through amide intermediate

**2. Reduction to Primary Amine**
```
R-CN + 2H₂ →[LiAlH4] R-CH2-NH2
```
- Complete reduction of C≡N to CH2-NH2

**3. Grignard Addition → Ketone**
```
R-CN + R'MgBr → R-C(=NMgBr)-R' →[H3O⁺] R-CO-R'
```
- Imine intermediate hydrolyzes to ketone
- Only ONE addition (unlike carbonyl)

## Selectivity & Regiochemistry Rules

### Acidity Trends

**Relative acid strength:**
```
CCl3COOH > CHCl2COOH > CH2ClCOOH > CH3COOH
(trichloroacetic)   (dichloro)    (monochloro)   (acetic)
 pKa 0.7            pKa 1.3       pKa 2.9        pKa 4.76
```

**Position of substituent matters:**
- α-position effect >> β-position effect >> γ-position effect
- Halogens at α-carbon have greatest effect

### Synthetic Route Selection

**From alkyl halide to acid:**
| Alkyl halide type | Best route |
|-------------------|------------|
| Primary | CN⁻ displacement → hydrolysis OR Grignard + CO2 |
| Secondary | Grignard + CO2 preferred |
| Tertiary | Grignard + CO2 only option |
| Aryl/benzyl | Oxidation (if alkyl present) |

**Avoid rearrangements:**
- Cyanide route: SN2, no rearrangement
- Grignard route: Check for acidic protons elsewhere

## Common Exam Patterns & Traps

### Pattern 1: Rank Acidity
```
Which is more acidic: CH3COOH or FCH2COOH?
Answer: FCH2COOH (inductive withdrawal stabilizes carboxylate)
```

### Pattern 2: Predict pKa from Structure
```
p-NO2-benzoic acid vs p-CH3-benzoic acid?
Answer: p-NO2 is more acidic (EWG, pKa ~3.4 vs ~4.3)
```

### Pattern 3: Synthesis from Alkyl Halide
```
Convert 1-bromopropane to butanoic acid
1. Mg, ether → propylmagnesium bromide
2. CO2
3. H3O⁺ → butanoic acid (4 carbons)
```

### Pattern 4: Nitrile Hydrolysis Mechanism
```
R-CN + OH⁻ → R-C(=NH)O⁻ → R-C(O)NH2 → R-COO⁻ + NH3
(Attack at C, proton transfers, tautomerization)
```

### Trap 1: Carboxylic Acids Are Not Alcohols
- pKa ~4-5, not ~16
- Resonance stabilization makes carboxylate much more stable
- Do NOT confuse acidity trends

### Trap 2: Distance of EWG Matters
```
Cl-CH2-COOH: pKa = 2.86
Cl-CH2-CH2-COOH: pKa = 4.05
β-position has much smaller effect than α-position
```

### Trap 3: Nitrile to Ketone vs Amine
- Grignard + nitrile → ketone (one addition)
- LiAlH4 + nitrile → amine (two additions)
- Don't confuse these reactions!

### Trap 4: Aromatic Acidity Trends Match EAS
- Substituent that deactivates ring → stronger acid
- Substituent that activates ring → weaker acid
- Same explanation: electron withdrawal/donation

### Trap 5: Grignard Preparation Limitations
- Cannot make Grignard from compound with acidic H
- Must protect -OH, -NH, -C≡CH before Grignard
- CO2 must be dry

### Decision Framework for Acid Strength

1. Identify substituents on acid
2. Classify each: EWG or EDG?
3. Note position relative to carboxyl
4. EWGs at α-position have largest effect
5. Multiple EWGs have additive effects
6. Rank accordingly

### Decision Framework for Synthesis

1. Starting material type (alkyl halide, alcohol, etc.)
2. Number of carbons needed (increase, decrease, same?)
3. Check for rearrangement risks
4. Choose appropriate reagent:
   - Increase by 1 carbon: CN⁻ or Grignard + CO2
   - From alcohol: oxidation
   - From alkylbenzene: KMnO4 oxidation
5. Consider protecting groups if needed
