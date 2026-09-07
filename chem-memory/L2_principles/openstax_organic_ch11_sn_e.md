---
id: organic.openstax_ch11
layer: 2
title: SN and E Reactions of Alkyl Halides
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - ../L4_reference/sn_e_decision_matrix.md
---

# SN and E Reactions of Alkyl Halides

## Key Principles

### Four Major Mechanisms

| Mechanism | Type | Molecular | Rate Law |
|-----------|------|-----------|----------|
| SN2 | Substitution | Bi | rate = k[RX][Nu⁻] |
| SN1 | Substitution | Uni | rate = k[RX] |
| E2 | Elimination | Bi | rate = k[RX][Base] |
| E1 | Elimination | Uni | rate = k[RX] |

### Competition Between Pathways
- Same substrate can undergo multiple reactions
- Product distribution depends on:
  - Substrate structure
  - Nucleophile/base strength
  - Solvent polarity
  - Temperature

## Mechanisms

### SN2 Mechanism

**Features:**
- One step, concerted
- Backside attack (180° from leaving group)
- Inversion of configuration (Walden inversion)
- Transition state: pentacoordinated carbon

**Rate equation:** rate = k[RX][Nu⁻]

**Stereochemistry:** Complete inversion (R → S or S → R)

```
     Nu⁻                Nu
      ↓                 |
R——C——X  →  [Nu---C---X]‡  →  R——C + X⁻
     |                  |
     R'                 R'
              (umbrella flip)
```

**Substrate reactivity:** CH3 > 1° > 2° >> 3° (NO SN2 on tertiary)

### SN1 Mechanism

**Features:**
- Two steps with carbocation intermediate
- Rate-determining step: loss of leaving group
- Carbocation is planar → attack from both sides
- Racemization (with possible inversion excess)

**Rate equation:** rate = k[RX]

**Carbocation stability:** 3° > 2° > 1° > CH3⁺
- Allylic and benzylic carbocations especially stable

```
Step 1: R-X → R⁺ + X⁻  (slow, rate-determining)
Step 2: R⁺ + Nu⁻ → R-Nu  (fast)
```

**Carbocation rearrangements:**
- Hydride shift: H⁻ migrates to stabilize carbocation
- Alkyl shift: R group migrates
- Always toward more stable carbocation

### E2 Mechanism

**Features:**
- One step, concerted
- Requires anti-periplanar geometry
- H and X must be trans to each other
- Strong base required

**Rate equation:** rate = k[RX][Base]

**Zaitsev's Rule:** More substituted alkene is major product
- Exception: Bulky base (t-BuOK) → Hoffman product

**Anti-periplanar requirement:**
```
    H              Base
     \              |
      C——C    →  C=C  + Base-H  + X⁻
     /   \
    X     R
```

**Cyclohexane systems:**
- Leaving group must be axial (not equatorial)
- Trans diaxial arrangement required

### E1 Mechanism

**Features:**
- Two steps with carbocation intermediate
- Same first step as SN1
- Base removes β-H after carbocation forms
- Often competes with SN1

**Rate equation:** rate = k[RX]

**Products:** Follow Zaitsev's rule (most substituted alkene)

```
Step 1: R-X → R⁺ + X⁻  (slow, RDS)
Step 2: Base + R⁺ → Alkene + Base-H⁺  (fast)
```

### E1cB Mechanism (Special Case)

**Features:**
- Elimination via carbanion intermediate
- When β-carbon has acidic hydrogen (e.g., adjacent to C=O)
- Poor leaving group + acidic H

```
Step 1: Base removes acidic H → carbanion (fast)
Step 2: Carbanion expels leaving group → alkene (slow, RDS)
```

## Selectivity & Regiochemistry Rules

### SN2 vs SN1 Decision Factors

| Factor | Favors SN2 | Favors SN1 |
|--------|-----------|------------|
| Substrate | CH3, 1°, 2° | 3°, allylic, benzylic |
| Nucleophile | Strong, negatively charged | Weak, neutral |
| Solvent | Polar aprotic (DMF, DMSO) | Polar protic (H2O, ROH) |
| Leaving group | Good (I⁻, Br⁻, TsO⁻) | Good leaving group |

### E2 vs E1 Decision Factors

| Factor | Favors E2 | Favors E1 |
|--------|-----------|-----------|
| Base | Strong base | Weak base |
| Substrate | Any with β-H | 3° preferred |
| Solvent | Any | Polar protic |
| Temperature | Higher favors E2 | Lower allows E1 |

### Substitution vs Elimination

| Condition | Primary Substrate | Secondary Substrate | Tertiary Substrate |
|-----------|------------------|--------------------|--------------------|
| Strong Nu, weak base | SN2 | SN2 | SN1/E1 |
| Strong base | E2 (minor SN2) | E2 major | E2 |
| Weak Nu, polar protic | SN2 (slow) | SN1/E1 mix | SN1/E1 |
| Bulky base | E2 (Hoffman) | E2 (Hoffman) | E2 |
| High temperature | More elimination | More elimination | More elimination |

### Leaving Group Ability
**Best to worst:** I⁻ > Br⁻ > Cl⁻ >> F⁻
**Tosylate (TsO⁻):** Excellent leaving group

### Nucleophile Strength
**In polar aprotic solvents:**
- Strong: I⁻, Br⁻, RS⁻, CN⁻, OH⁻, RO⁻
- Moderate: Cl⁻, RCOO⁻
- Weak: H2O, ROH

**In polar protic solvents:**
- Solvation reduces nucleophilicity
- I⁻ > Br⁻ > Cl⁻ > F⁻ (opposite of basicity)

### Zaitsev vs Hoffman Products

**Zaitsev (thermodynamic):**
- More substituted alkene
- Favored with strong, unhindered bases
- More stable due to hyperconjugation

**Hoffman (kinetic):**
- Less substituted alkene
- Favored with bulky bases (t-BuOK, LDA)
- Less steric hindrance in transition state

## Common Exam Patterns & Traps

### Pattern 1: Predict Mechanism from Conditions
```
2-bromo-2-methylpropane + H2O → ?
Answer: SN1 + E1 mixture (tertiary, weak nucleophile, protic solvent)
```

### Pattern 2: SN2 Stereochemistry
```
(R)-2-bromobutane + NaOH → ?
Answer: (S)-2-butanol (complete inversion)
```

### Pattern 3: E2 in Cyclohexanes
```
trans-1-bromo-2-methylcyclohexane + NaOEt → ?
Must check: Is Br axial? Is anti-H available?
```

### Pattern 4: Carbocation Rearrangement
```
3-bromo-3-methylpentane + H2O → ?
Carbocation may rearrange before nucleophile attack
```

### Trap 1: Tertiary Substrates Cannot Do SN2
- No matter how strong the nucleophile
- Steric hindrance prevents backside attack
- E2 or SN1/E1 only

### Trap 2: SN1 Gives Racemic Mixture
- Not pure racemic often
- Slight inversion excess from ion pairing
- Draw both enantiomers as products

### Trap 3: Anti-Periplanar Requirement
- E2 requires anti geometry
- In cyclohexanes: leaving group must be axial
- Equatorial leaving groups do NOT undergo E2

### Trap 4: Solvent Effects on Nucleophilicity
- Polar aprotic: nucleophilicity follows basicity
- Polar protic: large anions better nucleophiles
- I⁻ is best nucleophile in protic solvents

### Trap 5: Temperature Effect
- Higher temperature favors elimination over substitution
- Elimination has higher activation energy
- Both E2 and E1 increase at elevated temperature

### Decision Framework

1. **Identify substrate type:** 1°, 2°, 3°
2. **Identify nucleophile/base strength**
3. **Check solvent:** protic vs aprotic
4. **Consider temperature**
5. **Apply decision matrix:**
   - Primary + strong Nu → SN2 (or E2 with bulky base)
   - Tertiary + weak Nu → SN1/E1
   - Tertiary + strong base → E2
   - Secondary → depends on conditions
6. **Draw appropriate stereochemistry**
7. **Check for rearrangements (SN1/E1)**
