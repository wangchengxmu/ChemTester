---
id: organic.openstax_ch16
layer: 2
title: Electrophilic Aromatic Substitution (EAS)
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - ../L4_reference/eas_directing_effects_table.md
---

# Electrophilic Aromatic Substitution (EAS)

## Key Principles

### Aromatic Stability Dictates Mechanism
- Benzene has 150 kJ/mol (36 kcal/mol) aromatic stabilization energy
- EAS **substitutes** rather than **adds** to preserve aromaticity
- Addition would destroy aromatic stability → endergonic
- Substitution retains aromaticity → exergonic overall

### Rate Comparison
- Aromatic rings are **less reactive** than alkenes toward electrophiles
- Alkene: Br2 adds instantly at room temp
- Benzene: Requires catalyst (FeBr3) for bromination
- Higher activation energy due to aromatic stabilization

### General EAS Mechanism
1. **Electrophile generation** (catalyst polarizes reagent)
2. **Electrophilic attack** → resonance-stabilized carbocation (arenium ion)
3. **Deprotonation** → restores aromaticity

## Mechanisms

### Bromination (FeBr3 catalyzed)
```
Step 1: FeBr3 polarizes Br2 → FeBr4⁻ Br⁺
Step 2: Br⁺ attacks benzene → arenium ion intermediate (3 resonance forms)
Step 3: Loss of H⁺ → bromobenzene, FeBr3 regenerated
```
- Arenium ion is doubly allylic with 3 resonance structures
- Intermediate is less stable than starting benzene

### Nitration (HNO3/H2SO4)
- Electrophile: NO2⁺ (nitronium ion)
- Generated from HNO3 + H2SO4
- Products: Nitrobenzene + water

### Sulfonation (H2SO4 or SO3)
- Electrophile: SO3 or H2SO4
- Reversible reaction
- Lower temperatures favor sulfonation
- Higher temperatures reverse (desulfonation)

### Friedel-Crafts Alkylation (RCl/AlCl3)
```
R-Cl + AlCl3 → R⁺ + AlCl4⁻ (carbocation electrophile)
R⁺ attacks benzene → alkylbenzene
```
**Limitations:**
1. Only alkyl halides work (no aryl/vinyl halides)
2. Cannot use on deactivated rings (with EWGs)
3. Cannot use on rings with basic amino groups (protonated)
4. **Polyalkylation** common (alkyl group activates ring)
5. **Carbocation rearrangements** possible with primary halides

### Friedel-Crafts Acylation (RCOCl/AlCl3)
```
R-CO-Cl + AlCl3 → R-C⁺=O (acyl cation, resonance stabilized)
Acyl cation attacks benzene → ketone
```
**Advantages over alkylation:**
- **No rearrangement** (acyl cation is resonance stabilized)
- **No polyacylation** (acyl group deactivates ring)
- Acyl cation: R-C≡O⁺ ↔ R⁺=C=O

## Selectivity & Regiochemistry Rules

### Substituent Effects Summary

| Effect | Activating | Deactivating |
|--------|-----------|--------------|
| o,p-directing | -OH, -NH2, -OR, -alkyl, -phenyl | -F, -Cl, -Br, -I |
| m-directing | **NONE** | -NO2, -CN, -CHO, -COR, -CO2R, -COOH, -SO3H |

### Three Categories of Substituents

1. **Ortho/Para Directors - ACTIVATING**
   - Alkyl groups: Inductive electron donation
   - -OH, -NH2, -OR: Strong resonance donation > weak inductive withdrawal
   - Stabilize o/p arenium ion intermediates via resonance or inductive effects

2. **Ortho/Para Directors - DEACTIVATING (Halogens only)**
   - -F, -Cl, -Br, -I
   - Strong inductive withdrawal > weak resonance donation
   - Lone pair donation stabilizes o/p intermediates only

3. **Meta Directors - DEACTIVATING**
   - All have positively polarized atom (δ+) directly attached to ring
   - -NO2, -CN, -CHO, -COR, -COOH, -CO2R, -SO3H, -NR3⁺
   - o/p intermediates have unfavorable resonance form placing + charge adjacent to EWG

### Directing Effect Explanation

**Ortho/Para Directors:**
- o/p attack gives arenium ion with positive charge directly on substituted carbon
- Alkyl: stabilized by hyperconjugation/inductive donation
- -OH, -NH2: stabilized by resonance donation from heteroatom lone pairs

**Meta Directors:**
- o/p attack gives unfavorable resonance form: + charge on carbon adjacent to EWG
- Meta attack avoids this destabilization
- Meta intermediate has 3 favorable resonance forms vs 2 for o/p

### Relative Reactivity Order

**Activators:** -NH2 > -OH > -OR > -alkyl > -phenyl

**Deactivators:** -NO2 > -CN > -SO3H > -CHO > -COR > -COOH > -F > -Cl > -Br > -I

## Common Exam Patterns & Traps

### Pattern 1: Predict Major Product
```
Toluene + HNO3/H2SO4 → ?
Answer: o- and p-nitrotoluene (alkyl is o,p-directing activator)
```

### Pattern 2: Multiple Substitutions
```
p-methylphenol + Br2 → ?
Answer: 2,6-dibromo-4-methylphenol
-OH activates o/p positions; bromination at both ortho positions
```

### Pattern 3: Friedel-Crafts Limitations
```
Nitrobenzene + CH3Cl/AlCl3 → ?
Answer: NO REACTION (nitro group deactivates ring too much)
```

### Pattern 4: Carbocation Rearrangement
```
Benzene + 1-chlorobutane/AlCl3 → ?
Answer: Mixture of butylbenzene AND sec-butylbenzene
Primary carbocation rearranges to more stable secondary
```

### Trap 1: Halogen Confusion
- Halogens are deactivating but o,p-directing
- NOT meta directors despite being electron-withdrawing

### Trap 2: Steric Effects
- Bulky groups give more para product even if ortho positions available
- Example: tert-butylbenzene bromination → almost exclusively para

### Trap 3: Acid-Base with Amines
```
Aniline + CH3Cl/AlCl3 → ?
Trap: -NH2 is protonated by AlCl3 → -NH3⁺ (deactivating meta director)
Workaround: Protect amine as amide (acetanilide) first
```

### Trap 4: Polysubstitution
- Alkylation gives polysubstitution (activating product)
- Acylation gives monosubstitution (deactivating product)

### Trap 5: Synthesis Order — Wrong First Step Gives Wrong Isomer
When building a multi-substituted benzene, the ORDER of EAS steps matters critically.

**Rule: Install the group whose directing effect you need FIRST.**
- If you need a meta-director and an ortho/para-director on the same ring, install the **activating (o/p) group first**, then add the meta-director at the correct position. Wait — that's wrong.
- **Correct rule: Install the group that directs to the position you want FIRST.**

**Example — 4-bromoacetophenone from benzene:**
- ❌ WRONG: FC acylation first (acetyl is meta-directing) → acetophenone → bromination gives **3-bromoacetophenone** (meta)
- ✅ CORRECT: Bromination first → bromobenzene (Br is o/p-directing) → FC acylation gives mostly **4-bromoacetophenone** (para)

**Key patterns:**
| Target | Correct first step | Why |
|--------|-------------------|-----|
| p-BrC₆H₄COMe | Br₂/FeBr₃, then CH₃COCl/AlCl₃ | Br is o/p-directing → acetyl goes para |
| m-nitroacetophenone | CH₃COCl/AlCl₃, then HNO₃/H₂SO₄ | Acetyl is meta-directing → NO₂ goes meta |
| p-nitrophenol | Protect OH, NO₂ first, deprotect | If OH unprotected, it directs ortho/para; but NO₃⁺ needed at para → need to control |

**Decision checklist for multi-step benzene synthesis:**
1. Identify ALL substituents on the target and their relative positions
2. For each substituent, classify: activating/deactivating? o/p or meta?
3. Work backwards (retrosynthesis): which group must be installed LAST?
   - The last group's directing effect is irrelevant (no further substitution)
   - The SECOND-to-last group's directing effect determines where the last group goes
4. Choose the order so that each newly-installed group directs the next to the right position
5. Check for FC limitations: no FC on strongly deactivated rings (NO₂, etc.)

### Decision Framework
1. Identify existing substituent on ring
2. Classify: activating/deactivating?
3. Determine directing effect: o/p or meta?
4. Check for special limitations (Friedel-Crafts, steric)
5. Draw possible products, rank by stability
