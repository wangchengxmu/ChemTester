---
id: organic.openstax_ch19
layer: 2
title: Aldehydes and Ketones - Nucleophilic Addition
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - ../L4_reference/carbonyl_reactivity_table.md
---

# Aldehydes and Ketones - Nucleophilic Addition

## Key Principles

### Carbonyl Structure
- sp2 hybridized carbon
- Planar trigonal geometry
- Electrophilic carbon (partial + charge)
- Nucleophilic oxygen (partial - charge)

### Reactivity Hierarchy
**Aldehydes > Ketones** for nucleophilic addition

**Reasons:**
1. **Steric:** Aldehydes have one large group; ketones have two
2. **Electronic:** Aldehydes have less inductive stabilization of partial + charge

**Aromatic aldehydes < Aliphatic aldehydes**
- Resonance donation from ring reduces electrophilicity

### General Nucleophilic Addition Mechanism

```
Step 1: Nu⁻ attacks carbonyl carbon (angle ~105° from oxygen)
        → sp2 to sp3 hybridization
        → Tetrahedral alkoxide intermediate

Step 2: Protonation of alkoxide
        → Alcohol product
```

**Alternative pathway:**
- Carbonyl oxygen protonated first (acid catalysis)
- Then nucleophile attacks more electrophilic carbonyl

## Mechanisms

### Hydride Reduction (NaBH4, LiAlH4)

**Sodium borohydride (NaBH4):**
- Mild reducing agent
- Works in protic solvents (MeOH, EtOH)
- Reduces aldehydes and ketones

**Lithium aluminum hydride (LiAlH4):**
- Strong reducing agent
- Requires anhydrous conditions
- Reduces aldehydes, ketones, esters, acids, amides

**Mechanism:**
```
R2C=O + :H⁻ (from reductant) → R2CH-O⁻ →[H3O⁺] R2CH-OH
```
- Hydride acts as nucleophile
- Aldehyde → primary alcohol
- Ketone → secondary alcohol

### Grignard Addition

**General reaction:**
- Aldehyde + R'MgX → secondary alcohol
- Ketone + R'MgX → tertiary alcohol
- Formaldehyde + R'MgX → primary alcohol

**Mechanism:**
```
Step 1: Mg²⁺ coordinates to carbonyl oxygen (Lewis acid)
Step 2: R'⁻ attacks carbonyl carbon
Step 3: Alkoxide intermediate forms
Step 4: H3O⁺ workup → alcohol
```

**Irreversible:** R'⁻ is too poor a leaving group

### Cyanohydrin Formation

**Reaction:** R2C=O + HCN → R2C(OH)CN

**Mechanism:**
```
Step 1: CN⁻ attacks carbonyl carbon
Step 2: Protonation of alkoxide → cyanohydrin
```

**Application:** Adds one carbon, can be hydrolyzed to α-hydroxy acid

### Imine Formation

**Reaction:** R2C=O + R'NH2 → R2C=NR' + H2O

**Mechanism (acid catalyzed):**
```
Step 1: Nucleophilic attack by amine
Step 2: Proton transfer
Step 3: Protonation of -OH as leaving group
Step 4: Loss of water
Step 5: Deprotonation → imine
```

**Requirements:**
- Primary amine
- Acid catalyst (pH 4-5 optimal)
- Remove water to drive equilibrium

### Enamine Formation

**Reaction:** Ketone + secondary amine → enamine

**Structure:** R2C=CR-NR'2 (amine attached to alkene)

**Mechanism:** Similar to imine formation
- Secondary amine cannot form imine (no N-H to lose)
- Proton lost from α-carbon instead

### Acetal Formation

**Reaction:** RCHO + 2 R'OH → RCH(OR')2 + H2O

**Mechanism (acid catalyzed):**
```
Step 1: Protonation of carbonyl oxygen
Step 2: Alcohol attack → hemiacetal
Step 3: Protonation of hemiacetal -OH
Step 4: Loss of water → oxocarbenium ion
Step 5: Second alcohol attack → acetal
```

**Reversibility:** Acid + water regenerates aldehyde/ketone

**Use:** Protecting group for aldehydes/ketones

### Wittig Reaction

**Reaction:** R2C=O + Ph3P=CR'2 → R2C=CR'2 + Ph3PO

**Reagent:** Phosphorus ylide (Ph3P⁺-C⁻R'2)

**Mechanism:**
```
Step 1: Nucleophilic attack by ylide carbanion
Step 2: Betaine intermediate
Step 3: Oxaphosphetane formation
Step 4: Elimination of Ph3PO → alkene
```

**Advantages:**
- Forms alkenes specifically
- Double bond position known
- Stereochemistry: Z-alkene often favored with stabilized ylides

### Wolff-Kishner Reduction

**Reaction:** R2C=O → R2CH2 (alkane)

**Reagents:** NH2NH2, KOH, heat

**Mechanism:**
```
Ketone + hydrazine → hydrazone
Hydrazone + base → carbanion → N2 loss → alkane
```

**Use:** Complete reduction of carbonyl to methylene

## Selectivity & Regiochemistry Rules

### Aldehyde vs Ketone Reactivity

When both present in same molecule:
- Nucleophile attacks aldehyde preferentially
- Less steric hindrance
- More electrophilic

### Conjugate Addition (α,β-Unsaturated)

**1,2-addition:** Direct attack on carbonyl
**1,4-addition (conjugate):** Attack at β-carbon

**Factors favoring 1,4-addition:**
- Soft nucleophiles (R2CuLi, RS⁻)
- Extended conjugation
- Steric hindrance at carbonyl

**Factors favoring 1,2-addition:**
- Hard nucleophiles (RLi, RMgX, H⁻)
- Less steric hindrance

### Protecting Group Strategy

**When to protect:**
- Multiple functional groups interfere
- Need selective reaction

**Acetal as protecting group:**
- Stable to bases, Grignard, hydride
- Removed by acid + water
- Does NOT protect ketones from organocuprates

## Common Exam Patterns & Traps

### Pattern 1: Grignard Product Prediction
```
Benzaldehyde + CH3MgBr → ?
Answer: 1-phenylethanol (secondary alcohol)
```

### Pattern 2: Reduction Products
```
NaBH4 reduces: aldehydes, ketones
LiAlH4 reduces: aldehydes, ketones, esters, acids, amides
```

### Pattern 3: Wittig Stereochemistry
```
Stabilized ylide (EWG on carbon) → E-alkene major
Unstabilized ylide → Z-alkene major
```

### Pattern 4: Protecting Group
```
Convert ketone to acetal, do Grignard elsewhere, then deprotect
```

### Trap 1: Over-reduction
- NaBH4 only reduces aldehydes and ketones
- LiAlH4 also reduces esters and acids
- Check starting material carefully

### Trap 2: Grignard Reactivity
- Cannot use Grignard if compound has:
  - -OH, -NH, -SH (acidic protons)
  - C=O, C≡N (other electrophilic sites)
- Must protect or use alternative

### Trap 3: Hemiacetal vs Acetal
- Hemiacetal: one alcohol added (unstable)
- Acetal: two alcohols added (stable protecting group)
- Hemiacetals form spontaneously; acetals need acid catalyst

### Trap 4: Imine pH Requirement
- Too acidic: amine protonated, no nucleophile
- Too basic: carbonyl not activated
- Optimal pH 4-5

### Trap 5: Wolff-Kishner vs Clemmensen
- Wolff-Kishner: basic conditions (KOH, hydrazine, heat)
- Clemmensen: acidic conditions (Zn(Hg), HCl)
- Choose based on acid/base sensitive groups

### Decision Framework for Nucleophilic Addition

1. Identify nucleophile type:
   - H⁻ (reduction) → alcohol
   - R⁻ (Grignard) → alcohol
   - N-nucleophile → imine/enamine
   - O-nucleophile → hemiacetal/acetal
   - CN⁻ → cyanohydrin

2. Identify carbonyl type:
   - Aldehyde → more reactive
   - Ketone → less reactive
   - α,β-unsaturated → consider 1,2 vs 1,4

3. Check conditions:
   - Acid or base catalysis?
   - Need for protecting groups?
   - Reversibility issues?

4. Predict stereochemistry:
   - Planar carbonyl → new chiral center?
   - Wittig stereochemistry rules

5. Consider workup:
   - Acidic workup needed after Grignard, hydride
   - Neutral conditions for some reactions
