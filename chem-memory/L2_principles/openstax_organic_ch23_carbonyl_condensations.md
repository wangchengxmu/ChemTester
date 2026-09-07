---
id: organic.openstax_ch23
layer: 2
title: Carbonyl Condensation Reactions
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Carbonyl Condensation Reactions

## Key Principles

### What Is a Condensation Reaction?

A carbonyl condensation reaction is one in which **two carbonyl compounds** join together with the **loss of a small molecule** (usually water). The defining feature is the formation of a new C–C bond between the α-carbon of one carbonyl and the carbonyl carbon of another.

**General pattern:**
```
Cα of molecule A + C=O of molecule B → Cα–C bond + loss of small molecule
```

**Key contrast with α-substitution:**
- **α-substitution:** Replace an α-H with another group (the carbonyl framework stays the same size)
- **Condensation:** Two carbonyl molecules combine (the carbon framework grows)

### The Universal Mechanism: Enolate Nucleophile + Carbonyl Electrophile

Nearly all condensation reactions follow this sequence:
1. **Enolate formation:** One carbonyl forms an enolate (nucleophile)
2. **Nucleophilic attack:** Enolate attacks a second carbonyl (electrophile)
3. **Protonation:** Forms a β-hydroxy carbonyl (aldol) or β-keto ester (Claisen)
4. **Dehydration (often):** Elimination of water to form an α,β-unsaturated carbonyl

### Classification Table

| Reaction Type | Reactants | Initial Product | Final Product (after dehydration) |
|---|---|---|---|
| Aldol | 2 aldehydes | β-hydroxy aldehyde | α,β-unsaturated aldehyde |
| Crossed aldol | 2 different carbonyls | Mixed β-hydroxy | Mixed α,β-unsaturated |
| Claisen | 2 esters | β-keto ester | — (usually not dehydrated) |
| Mixed Claisen | Ester + ketone | β-diketone or β-keto ester | — |
| Dieckmann | Diester (intramolecular) | Cyclic β-keto ester | — |
| Knoevenagel | Aldehyde + active methylene | β-hydroxy | α,β-unsaturated (often decarboxylates) |

## Mechanisms

### 1. Aldol Reaction (Base-Catalyzed)

**Simple aldol:** Two identical aldehydes (usually acetaldehyde) react.

**Mechanism:**
1. **Enolate formation:** OH⁻ abstracts an α-proton from aldehyde 1 → enolate
2. **Nucleophilic attack:** Enolate attacks the carbonyl carbon of aldehyde 2 → alkoxide
3. **Protonation:** Alkoxide picks up a proton from water → **β-hydroxy aldehyde** (aldol product)
4. **Dehydration (optional):** The β-hydroxy aldehyde can lose water (E1cb mechanism) → **α,β-unsaturated aldehyde** (if heated or under basic conditions)

**Acid-catalyzed aldol:**
1. Protonate carbonyl → more electrophilic
2. Enol formation (loss of α-H)
3. Enol attacks protonated carbonyl
4. Deprotonation → β-hydroxy carbonyl
5. Protonation of OH → dehydration

**Reversibility:**
- The aldol reaction is **reversible** under both acid and base conditions
- The retro-aldol (reverse) is important biochemically (e.g., glucose metabolism)
- Equilibrium usually favors starting materials unless the product is stabilized (conjugated, cyclic)

### 2. Crossed Aldol Reaction

**Problem:** Two different carbonyl compounds → four possible products (self-condensation of A, self-condensation of B, A+B twice, B+A twice)

**Solution:** Use one component as the **nucleophile** (enolate) and one as the **electrophile** (carbonyl).

**Strategy 1: Enolate of A + unreactive electrophile B**
- Make enolate of A with LDA (irreversible)
- Add electrophile B (usually an aldehyde or ketone without α-H, or with only one type of α-H)
- Works best when B has **no α-hydrogens** (e.g., benzaldehyde, formaldehyde, p-nitrobenzaldehyde)
- Reason: B can't form an enolate, so it can only act as an electrophile

**Strategy 2: Slow addition**
- Slowly add A to a solution of B with base
- If B is in large excess and B's enolate is less reactive, A's enolate reacts with B

**Strategy 3: Enolate of A + B (both reactive)**
- Use **LDA** to irreversibly form enolate of A at -78°C
- Then add B (the electrophile)
- This prevents equilibration and self-condensation

**Examples of non-enolizable electrophiles:**
| Compound | Why No Enolization |
|---|---|
| Formaldehyde (HCHO) | No α-carbon |
| Benzaldehyde (PhCHO) | No α-H (benzylic H is not acidic enough under mild conditions) |
| Aromatic ketones (ArCOCH₃) | Can enolize but slowly |
| p-Nitrobenzaldehyde | Electron-withdrawing makes carbonyl very electrophilic; no α-H |

### 3. Intramolecular Aldol (Aldol Cyclization)

**Advantages:** Intramolecular reactions are much faster than intermolecular ones (entropic advantage). This avoids the crossed-aldol problem entirely.

**Ring formation rules:**
- Forms 5- and 6-membered rings preferentially
- 3-membered rings: too strained
- 4-membered rings: possible but slow
- 7-membered rings: possible but slower
- 8+: very slow, entropically disfavored

**Example: 2,7-octanedione → intramolecular aldol**
- Enolate at C2 attacks C7 carbonyl → 6-membered ring
- NOT C7 enolate attacking C2 (would give same ring) — regioselectivity determined by which enolate forms more easily
- Dehydration → 3-methyl-2-cyclohexenone

**Regioselectivity in unsymmetrical diketones:**
- The enolate forms preferentially at the **less substituted** side (kinetic) or more substituted side (thermodynamic)
- Attack occurs at the carbonyl that gives the **more substituted** (more stable) double bond after dehydration

### 4. Claisen Condensation

**Simple Claisen:** Two identical esters react.

**Mechanism:**
1. **Deprotonation:** Ethoxide (EtO⁻) abstracts an α-proton from ester 1 → enolate
2. **Nucleophilic attack:** Enolate attacks the carbonyl of ester 2 → tetrahedral intermediate
3. **Expulsion of leaving group:** Ethoxide is expelled → β-keto ester
4. **Deprotonation:** The β-keto ester is much more acidic (pKa ~11) than the starting ester (pKa ~25), so it is deprotonated by ethoxide → stable enolate
5. **Acid workup:** Gives the β-keto ester product

**Key requirements:**
- **At least one ester must have two α-hydrogens** (to form the enolate AND to allow deprotonation of the product)
- The base must be the same alkoxide as the ester alkoxide (to avoid transesterification)
- Example: Ethyl acetate + NaOEt → ethyl acetoacetate

**Why it works (driving force):**
- The β-keto ester product is deprotonated under the reaction conditions (it's much more acidic)
- This deprotonation is irreversible under the reaction conditions
- This pulls the equilibrium toward product (essentially irreversible)
- **This is why Claisen is irreversible while aldol is reversible**

### 5. Mixed Claisen Condensation

**Problem:** Two different esters → multiple products

**Solution (analogous to crossed aldol):**
- Use LDA to form enolate of one ester irreversibly
- Then add the second ester (electrophile)
- Or use a non-enolizable ester (like benzoate or tert-butyl acetate) as the electrophile
- Or use a ketone enolate + ester (ketone enolate is more nucleophilic)

**Ketone + Ester (Mixed Claisen):**
- LDA deprotonates the ketone → enolate
- Add ester → nucleophilic attack → β-diketone
- This is preferred because ketone enolates are more reactive than ester enolates

### 6. Dieckmann Condensation

**Definition:** Intramolecular Claisen condensation of a diester.

**Requirements:**
- Forms 5- or 6-membered rings (same as intramolecular aldol)
- The diester must have the right chain length

| Diester | Ring Size | Product |
|---|---|---|
| Diethyl adipate (C6) | 5-membered | 2-carbethoxycyclopentanone |
| Diethyl pimelate (C7) | 6-membered | 2-carbethoxycyclohexanone |
| Diethyl glutarate (C5) | 4-membered | Poor yield |
| Diethyl suberate (C8) | 7-membered | Moderate yield |

**Mechanism:** Same as Claisen but intramolecular. Enolate formation → nucleophilic attack on the other ester carbonyl within the same molecule → tetrahedral intermediate → expulsion of ethoxide → β-keto ester.

**Important note:** The Dieckmann can only occur at one specific ester (the one that becomes the enolate). If the diester is symmetrical, there's no regioselectivity issue. If unsymmetrical, the more acidic α-position forms the enolate.

### 7. Retro-Aldol Reaction

**Definition:** The reverse of the aldol reaction — cleavage of a β-hydroxy carbonyl into two carbonyl compounds.

**Mechanism (base-catalyzed):**
1. Deprotonation of α-H → enolate
2. C–C bond cleavage → two fragments (enolate + carbonyl)
3. Protonation of enolate → second carbonyl

**Requirements:**
- Must have a β-hydroxy carbonyl (or equivalent)
- The Cα–Cβ bond must be cleavable
- The products must be reasonably stable carbonyl compounds

**Biochemical importance:**
- Glycolysis: fructose-1,6-bisphosphate → DHAP + G3P (aldolase-catalyzed retro-aldol)
- Central to sugar metabolism

### 8. Knoevenagel Condensation

**Definition:** Reaction of an aldehyde or ketone with an **active methylene compound** (very acidic CH₂ group) under basic conditions, often followed by dehydration.

**Active methylene compounds:**
| Compound | pKa | Reason for Acidity |
|---|---|---|
| Malonic ester (CH₂(CO₂Et)₂) | ~13 | Two ester groups |
| Acetoacetic ester | ~11 | Ketone + ester |
| Diethyl malonate | ~13 | Two ester groups |
| Meldrum's acid | ~5 | Very acidic |
| Cyanoacetic ester | ~9 | Ester + CN |

**Mechanism:**
1. Base deprotonates the active methylene compound → carbanion (very stable)
2. Carbanion attacks the aldehyde carbonyl → alkoxide
3. Protonation → β-hydroxy compound
4. Dehydration → α,β-unsaturated product

**Catalyst:** Usually a weak base (piperidine, pyridine) or amine; sometimes TiCl₄ or other Lewis acids.

### 9. Doebner Modification

The Doebner modification combines the Knoevenagel condensation with **decarboxylation** in one pot:

1. Malonic acid + aldehyde + pyridine (amine base) + piperidine
2. Knoevenagel condensation occurs → α,β-unsaturated dicarboxylic acid derivative
3. Heating causes **decarboxylation** → α,β-unsaturated carboxylic acid

**Advantage over standard Knoevenagel:** Directly gives α,β-unsaturated acids without isolated intermediate.

### 10. Decarboxylation of β-Keto Esters

**General principle:** β-Keto esters (and β-keto acids) readily decarboxylate upon heating with acid.

**Mechanism:**
1. Protonation of the carbonyl oxygen (acid)
2. Six-membered cyclic transition state: the carboxylic acid proton transfers to the enolate while CO₂ leaves
3. The enol tautomerizes to the ketone

```
    O                 O
    ||                ||
 R-C-CH₂-C-OEt  →  R-C-CH₃  +  CO₂  +  EtOH
    |                 |
    O                 H
```

**Why β-keto esters decarboxylate but γ-keto esters don't:**
- The six-membered cyclic transition state is only possible when the carboxyl group is β to the carbonyl
- γ-Keto esters would need a 7-membered transition state → much less favorable

## Aldol Stereochemistry: The Zimmerman-Traxler Model

### The Six-Membered Chair Transition State

The Zimmerman-Traxler model predicts the stereochemistry of aldol products based on a **six-membered chair transition state** for lithium enolates.

### Key Elements:

1. **Metal chelation:** The lithium cation bridges between the enolate oxygen and the carbonyl oxygen, creating a rigid six-membered ring

2. **Enolate geometry determines product stereochemistry:**
   - **Z-enolate** → **syn** aldol product (OH and R group on the same side)
   - **E-enolate** → **anti** aldol product (OH and R group on opposite sides)

3. **Chair conformation:** The transition state adopts a chair; the substituents prefer equatorial positions

### Stereochemistry Summary Table

| Enolate Geometry | Relationship to OH | Product Configuration |
|---|---|---|
| Z-enolate (Li, THF) | syn | R and OH on same face |
| E-enolate (Li, THF) | anti | R and OH on opposite faces |

### Practical Implications

- To get **syn** aldol: use conditions that give Z-enolate (e.g., LDA with additive, or specific boron enolates)
- To get **anti** aldol: use conditions that give E-enolate (e.g., LDA in THF, or specific titanium enolates)
- **Boron enolates** (from Bu₂BOTf + Et₃N) give excellent stereocontrol
- **Evans oxazolidinones** provide enantioselective aldol reactions

## Selectivity Rules

### Aldol: Self vs Cross

| Situation | Strategy |
|---|---|
| Two identical carbonyls | Simple aldol (one product) |
| One has no α-H + one with α-H | Crossed aldol: enolate of enolizable one attacks non-enolizable one |
| Both have α-H | LDA to form one enolate, then add the other |
| Want specific regioselectivity | Use LDA at -78°C (kinetic control) |

### Claisen: Self vs Mixed

| Situation | Strategy |
|---|---|
| Two identical esters | Simple Claisen (one product) |
| One has no α-H (e.g., ArCO₂Et) | Mixed Claisen: enolate of enolizable ester attacks non-enolizable |
| Ketone + ester | LDA enolate of ketone, then add ester |
| Two different enolizable esters | LDA enolate of one, then add the other |

### Intramolecular Ring Size Preference

| Ring Size | Relative Rate | Practical Yield |
|---|---|---|
| 3 | Very slow | Poor |
| 4 | Slow | Poor to moderate |
| 5 | Fast | Good |
| 6 | Fastest | Excellent |
| 7 | Moderate | Moderate |
| 8+ | Slow | Poor |

### Dehydration vs No Dehydration

| Reaction | Spontaneous Dehydration? | Conditions for Dehydration |
|---|---|---|
| Aldol (aldehydes) | Often yes (conjugation stabilizes) | Heat or base |
| Aldol (ketones) | Usually no (less driving force) | Explicit heating, acid |
| Claisen | No (β-keto ester is stable) | — |
| Knoevenagel | Yes (conjugated product very stable) | Often spontaneous |

## Common Exam Patterns

### Pattern 1: Predicting Aldol Products

**Question:** "What is the aldol product of 3-pentanone?"

**Answer:** 
- Enolate forms at either α-position (symmetrical molecule, so same product)
- Attack on another 3-pentanone molecule
- Product: 5-hydroxy-4,4-dimethyl-3-heptanone
- Dehydration (with heat): 4,4-dimethyl-3-hepten-5-one
- However: ketone aldols are slower and often don't dehydrate spontaneously

### Pattern 2: Crossed Aldol Strategy

**Question:** "How would you synthesize PhCH(OH)CH₂CHO from benzaldehyde and acetaldehyde?"

**Answer:**
- Benzaldehyde has no α-H → can only be electrophile
- Acetaldehyde forms the enolate (nucleophile)
- Problem: acetaldehyde also self-condenses
- Solution: Add LDA to acetaldehyde → form enolate, then add benzaldehyde → PhCH(OH)CH₂CHO (the desired product)
- Or: Slowly add acetaldehyde to excess benzaldehyde with base

### Pattern 3: Claisen Product Identification

**Question:** "What is the Claisen condensation product of ethyl propanoate?"

**Answer:**
- Two ethyl propanoate molecules react with NaOEt
- Enolate of one attacks carbonyl of the other
- Product: ethyl 2-methyl-3-oxopentanoate (a β-keto ester with a methyl substituent at the α-position)

### Pattern 4: Dieckmann Ring Size

**Question:** "What ring size does the Dieckmann condensation of diethyl pimelate give?"

**Answer:** Diethyl pimelate has the ester groups at the termini of a 7-carbon chain. The Dieckmann cyclization forms a 6-membered ring (2-carbethoxycyclohexanone). General formula: a diester with (n+2) carbons in the chain gives an n-membered ring.

### Pattern 5: Aldol Stereochemistry

**Question:** "A Z-enolate of a ketone reacts with an aldehyde. What is the stereochemical relationship between the newly formed hydroxyl group and the α-substituent?"

**Answer:** **Syn** (same side). Z-enolates give syn aldol products via the Zimmerman-Traxler chair transition state where the α-substituent and incoming aldehyde approach equatorially.

### Pattern 6: Knoevenagel Product

**Question:** "What is the product of benzaldehyde + diethyl malonate with piperidine?"

**Answer:**
1. Piperidine deprotonates malonate → carbanion
2. Attacks benzaldehyde → β-hydroxy malonate
3. Dehydration → diethyl benzylidenemalonate (PhCH=C(CO₂Et)₂)
4. This is an α,β-unsaturated diester

### Pattern 7: Retro-Aldol Cleavage

**Question:** "What are the products when 4-hydroxy-2-butanone undergoes retro-aldol?"

**Answer:**
- CH₃COCH(OH)CH₃ → cleavage of the bond between C2 and C3
- Products: formaldehyde (HCHO) + acetone (CH₃COCH₃)
- Or: the enolate of acetone + formaldehyde (depending on conditions)

### Key Mnemonics

- **Aldol = Aldehyde + Alcohol (β-hydroxy)** 
- **Claisen = Condensation of esters → β-keto ester**
- **Dieckmann = Di-ester Claisen (intramolecular)**
- **Knoevenagel = "Known-evenly-gel" = aldehyde + active methylene → α,β-unsaturated**
- **"If it has no alpha-H, it can only be the electrophile"** (critical for crossed reactions)
- **Z-enolate → syn; E-enolate → anti** (Zimmerman-Traxler)
- **β-keto esters decarboxylate** (6-membered ring transition state)
- **5 and 6 are the magic ring sizes** for intramolecular reactions
