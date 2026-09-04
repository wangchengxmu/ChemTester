---
id: organic.openstax_ch22
layer: 2
title: Carbonyl Alpha-Substitution and Enolate Chemistry
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Carbonyl Alpha-Substitution and Enolate Chemistry

## Key Principles

### The Alpha Position: Reactivity Hotspot

The carbon directly adjacent to a carbonyl group (α-carbon) is uniquely reactive because:
- The α-C–H bond is weakened by resonance stabilization of the resulting enolate (pKa depression)
- The carbonyl group stabilizes the conjugate base through delocalization of negative charge onto oxygen
- This makes α-hydrogens ~10^25 times more acidic than typical sp³ C–H bonds

### pKa Reference Table: α-Hydrogen Acidity

| Carbonyl Type | α-H pKa (DMSO) | Relative Acidity | Key Base to Use |
|---|---|---|---|
| 1,3-Diketone | ~9 | Very acidic | NaOEt, K₂CO₃ |
| β-Keto ester | ~11 | Very acidic | NaOEt, K₂CO₃ |
| Aldehyde | ~17 | Moderate | LDA |
| Ketone | ~20 | Moderate | LDA |
| Ester | ~25 | Weak | LDA |
| Amide | ~30 | Very weak | LDA, NaNH₂ |
| Carboxylic acid | N/A (O–H) | — | — |

Note: Aldehyde α-H's are more acidic than ketone α-H's because the carbonyl is less sterically hindered and provides better stabilization. However, aldehydes are tricky to work with because they self-condense readily.

### Keto-Enol Tautomerism

Every carbonyl with an α-hydrogen exists in equilibrium with its enol form:

$$\text{Ketone} \rightleftharpoons \text{Enol}$$

- **Simple ketones:** ~10⁻⁴ enol at equilibrium (negligible)
- **1,3-Dicarbonyls:** significant enol content (~20-80%) due to conjugation + H-bonding
- **Phenol** is the enol form of cyclohexadienone (essentially 100% enol)

The enol is nucleophilic at the α-carbon and electrophilic at the OH. This dual reactivity underpins most α-substitution chemistry.

## Enolate Formation: Kinetic vs Thermodynamic Control

This is the single most important concept in enolate chemistry. When a carbonyl has two different α-positions, the base and conditions determine which enolate forms.

### Kinetic Enolate (LDA)

- **Base:** Lithium diisopropylamide (LDA), i-Pr₂NLi
- **Conditions:** -78°C, THF solvent, 1.0 equiv LDA
- **Selectivity:** Deprotonates the **less substituted**, more accessible α-position
- **Mechanism:** Irreversible deprotonation under kinetic control
- **Why:** The less hindered proton is more accessible to the bulky LDA base; low temperature prevents equilibration
- **Enolate geometry:** Predominantly **(E)-enolate** with LDA in THF due to chelation control

### Thermodynamic Enolate (NaOEt, NaHMDS with heat)

- **Base:** Sodium ethoxide (NaOEt) or NaHMDS with warming
- **Conditions:** 25°C (or higher), often in the parent alcohol as solvent
- **Selectivity:** Deprotonates the **more substituted** α-position
- **Mechanism:** Reversible deprotonation; equilibrium favors the more stable enolate
- **Why:** The more substituted enolate has a lower-energy C=C (more alkyl substitution stabilizes the double bond)
- **Enolate geometry:** Predominantly **(Z)-enolate** for steric reasons with Na⁺ counterion

### Comparison Table

| Feature | Kinetic (LDA) | Thermodynamic (NaOEt) |
|---|---|---|
| Temperature | -78°C | 25°C+ |
| Base | Bulky, strong | Small, strong |
| Proton removed | Less hindered | More hindered |
| Reversibility | Irreversible | Reversible |
| Enolate geometry | Usually E | Usually Z |
| Counterion effect | Li⁺ (tight) | Na⁺ (looser) |

### Counterion Effects on Enolate Geometry

The metal cation profoundly affects enolate geometry:

| Counterion | Geometry Trend | Rationale |
|---|---|---|
| Li⁺ | E-enolate (with LDA in THF) | Chelation with THF creates a rigid transition state |
| Li⁺ | Z-enolate (in non-polar solvents) | Tight ion pairing, monomeric |
| Na⁺/K⁺ | Z-enolate | Larger ion pair allows equilibration to more stable Z |
| Mg²⁺ | E-enolate | Chelation with carbonyl oxygen |

This matters enormously because **enolate geometry controls aldol stereochemistry** (see Zimmerman-Traxler model).

## Mechanisms

### 1. Alpha-Halogenation

**Base-Catalyzed (ketones/aldehydes):**
1. Base abstracts α-H → enolate
2. Enolate attacks halogen (Br₂, Cl₂) → α-halo carbonyl
3. The α-halo product is more acidic → can over-halogenate

**Acid-Catalyzed (ketones/aldehydes):**
1. Carbonyl protonated → more electrophilic
2. Enol attacks halogen
3. Deprotonation gives α-halo product
4. Slower, but can be stopped at mono-halogenation more easily

**Hell-Volhard-Zelinsky (HVZ) — Carboxylic Acids:**
- **Reagents:** PBr₃ + Br₂
- **Why PBr₃?** Carboxylic acids don't enolize readily. PBr₃ converts the acid to an acid bromide (R–C(O)Br), which has much more acidic α-H's
- The acid bromide enolizes, brominates at α-position, then reacts with Br⁻ to regenerate acid bromide, finally hydrolysis gives α-bromo acid
- **Works for:** mono- and poly-bromination at the α-position
- **Does NOT work for:** formic acid (no α-H), fully substituted α-carbons

### 2. Enolate Alkylation

**General scheme:**
1. Form enolate with strong base (LDA)
2. Add alkyl halide (SN2)
3. Quench

**Critical rules for the electrophile:**
- **Primary alkyl halides ONLY** (methyl, primary) — SN2 requires accessible backside
- **Secondary alkyl halides:** mostly give E2 elimination with the basic enolate
- **Tertiary halides:** no reaction (E2 dominates completely)
- **Allylic/benzylic halides:** SN2 works, but also SN1/E1 pathways compete
- **Epoxides:** work well (ring-opening alkylation)
- **α,β-unsaturated carbonyl halides:** give Michael addition instead

**Common problems:**
- **Polyalkylation:** After the first alkylation, the product still has acidic α-H's and can form a new enolate. Use 1.0 equiv base and control stoichiometry, or use a removable activating group.
- **Enolate proton exchange:** If the electrophile is slow to react, the enolate may deprotonate the starting material (scrambling). Use a non-nucleophilic base.

### 3. Enamine Alkylation (Stork Enamine Synthesis)

Enamines solve the polyalkylation problem because the nitrogen can't be alkylated a second time.

**Formation:**
- **Reagents:** Secondary amine (usually pyrrolidine) + catalytic TsOH
- **Mechanism:** Carbonyl + amine → hemiaminal → elimination of water → enamine
- **Water removal:** Azeotropic distillation with toluene, or Dean-Stark trap
- **Key:** Secondary amines only (tertiary can't form enamines; primary give imines)

**Alkylation:**
- The enamine carbon is nucleophilic (less than enolate but sufficient for reactive electrophiles)
- Works with: **alkyl halides (primary), acyl halides, α-halo ketones, epoxides**
- Does NOT work well with: unactivated secondary/tertiary halides
- The reaction proceeds through an iminium ion intermediate

**Hydrolysis:**
- Dilute aqueous acid hydrolyzes the iminium back to the carbonyl
- Net result: α-alkylated ketone/aldehyde

**Advantages over direct enolate alkylation:**
1. No polyalkylation (the nitrogen blocks further reaction)
2. Mild, neutral conditions
3. Compatible with acid-sensitive functional groups
4. Good for sensitive substrates

**Limitations:**
- Requires relatively reactive electrophiles (enamines are less nucleophilic than enolates)
- Acidic workup may not be compatible with all substrates
- Cyclohexanone derivatives work best (6-membered ring transition states)

### 4. Acetoacetic Ester Synthesis

**Starting material:** Ethyl acetoacetate (CH₃COCH₂CO₂Et)

**Step 1: Deprotonation**
- Base: NaOEt (the α-H between two carbonyls is very acidic, pKa ~11)
- Forms the stabilized enolate

**Step 2: Alkylation**
- Add primary alkyl halide (SN2)
- Mono-alkylation is the standard; dialkylation is possible with excess base/RX

**Step 3: Hydrolysis and Decarboxylation**
- Heat with aqueous NaOH (saponification of ester)
- Then acidify and heat → decarboxylation
- Product: **substituted methyl ketone** (RCH₂COCH₃)

**Decarboxylation mechanism:**
1. Beta-keto acid formed upon acidification
2. Six-membered cyclic transition state: enol + CO₂
3. The carbonyl group facilitates decarboxylation by stabilizing the enol intermediate

**What you can make:**
| Alkylation Pattern | Product |
|---|---|
| Mono-alkyl (RCH₂COCH₃) | 2-substituted acetone |
| Di-alkyl (RR'CHCOCH₃) | 2,2-disubstituted acetone |
| Di-alkyl (different RX added sequentially) | unsymmetrical 2,2-disubstituted |

### 5. Malonic Ester Synthesis

**Starting material:** Diethyl malonate (CH₂(CO₂Et)₂)

**Steps are identical to acetoacetic ester synthesis:**
1. NaOEt deprotonation (pKa ~13)
2. Alkylate with primary halide
3. Hydrolysis + heat → decarboxylation

**Product:** **substituted carboxylic acid** (RCH₂CO₂H)

**Key difference from acetoacetic ester:**
- Acetoacetic ester → ketones
- Malonic ester → carboxylic acids

**Dialkylation:** Add second equivalent of base, then second alkyl halide → disubstituted acetic acid

**Applications:**
- Synthesis of α-substituted carboxylic acids
- Cyclic acids via intramolecular alkylation (forming rings)
- Building blocks for larger molecules

### 6. Michael Addition

**Definition:** Conjugate (1,4-) addition of a nucleophile to an α,β-unsaturated carbonyl compound.

**Michael donor:** Enolate (soft nucleophile), malonate enolate, β-keto ester enolate, cuprate reagents

**Michael acceptor:** α,β-unsaturated ketone, ester, aldehyde, nitrile, nitro compound

**Mechanism:**
1. Enolate attacks the β-carbon (not the carbonyl carbon)
2. This is a 1,4-addition; forms an enolate intermediate
3. Protonation gives the 1,4-addition product

**Why conjugate addition?**
- "Soft" nucleophiles (enolates, cuprates) prefer soft electrophiles (the β-carbon)
- "Hard" nucleophiles (organolithiums, Grignards) prefer hard electrophiles (carbonyl carbon, 1,2-addition)

**Selectivity rules:**
| Nucleophile | Hard/Soft | Preference |
|---|---|---|
| RLi | Hard | 1,2-addition to carbonyl |
| RMgX | Borderline | Mixed, often 1,2 |
| R₂CuLi | Soft | 1,4-addition (Michael) |
| Enolate | Soft | 1,4-addition (Michael) |
| NaBH₄/CeCl₃ | Hard | 1,2-addition |
| LiAlH₄ | Hard | 1,2-addition |

**Robinson Annulation:**
- A two-step sequence combining **Michael addition + intramolecular aldol condensation**
- Michael addition of an enolate to methyl vinyl ketone (MVK) → 1,5-diketone
- Base treatment → intramolecular aldol → α,β-unsaturated cyclic ketone
- Forms **six-membered rings** preferentially
- Net result: builds a new six-membered ring with a cyclohexenone core
- Widely used in steroid and terpene synthesis

## Selectivity Rules

### Enolate Regioselectivity: Summary Decision Tree

```
Does the carbonyl have two different α-positions?
├── No → regioselectivity not an issue
└── Yes → Which enolate do you want?
    ├── Less substituted (kinetic) → LDA, -78°C, THF
    └── More substituted (thermodynamic) → NaOEt, 25°C, ROH solvent
```

### 1,2- vs 1,4-Addition Decision Tree

```
α,β-unsaturated carbonyl + nucleophile:
├── Hard nucleophile (Li, Mg, NaBH₄) → 1,2-addition (unless Cu⁺ added)
├── Soft nucleophile (enolate, cuprate) → 1,4-addition (Michael)
├── Organocuprate (R₂CuLi) → specifically 1,4
└── Reversible conditions (e.g., NaOMe/MeOH) → thermodynamic 1,4
```

### Alkylation Compatibility

| Electrophile | Enolate Alkylation | Enamine Alkylation | Notes |
|---|---|---|---|
| MeI, EtI, primary RX | ✅ | ✅ | Best substrates |
| Allylic halides | ✅ | ✅ | SN2 works well |
| Benzylic halides | ⚠️ | ✅ | SN1 may compete |
| Secondary halides | ❌ (E2) | ❌ | Elimination dominates |
| Tertiary halides | ❌ | ❌ | E2 only |
| Epoxides | ✅ | ✅ | Ring-opening |
| Acyl halides | ❌ (Claisen) | ✅ | Enamines give acylation |
| α,β-unsat. halides | ❌ (Michael) | ❌ | Michael addition instead |

## Common Exam Patterns

### Pattern 1: Choosing Base and Conditions

**Question:** "How would you selectively deprotonate the methyl group of 2-methylcyclohexanone?"

**Answer:** LDA, -78°C, THF → kinetic enolate at the less substituted (methyl) side.

### Pattern 2: Acetoacetic Ester vs Malonic Ester

**Question:** "Design a synthesis of 2-pentanone starting from ethyl acetoacetate."

**Answer:**
1. NaOEt, EtOH → deprotonate
2. CH₃CH₂CH₂Br → alkylate
3. NaOH, H₂O, heat → hydrolyze
4. H₃O⁺, heat → decarboxylate
5. Product: CH₃CH₂CH₂COCH₃ (2-pentanone) ✅

### Pattern 3: Michael vs Aldol

**Question:** "Does cyclohexanone enolate react with methyl vinyl ketone via aldol or Michael?"

**Answer:** Michael addition (1,4-), because enolates are soft nucleophiles and the β-carbon is the soft electrophilic site. The aldol product is the kinetic product but usually reversible; Michael is thermodynamic.

### Pattern 4: Stork Enamine Sequence

**Question:** "How would you mono-alkylate cyclohexanone at the 2-position using an enamine?"

**Answer:**
1. Pyrrolidine + TsOH, toluene, reflux (Dean-Stark) → enamine
2. CH₃I → alkylation
3. H₃O⁺, H₂O → hydrolysis
4. Product: 2-methylcyclohexanone

### Pattern 5: HVZ Reaction

**Question:** "How would you make 2-bromopropanoic acid?"

**Answer:** PBr₃ (catalytic), Br₂, heat → Hell-Volhard-Zelinsky bromination of propanoic acid at the α-position.

### Pattern 6: Robinson Annulation Product

**Question:** "What is the product when cyclohexanone reacts with methyl vinyl ketone under basic conditions?"

**Answer:**
1. Michael addition → 2-(3-oxobutyl)cyclohexanone
2. Intramolecular aldol → bicyclic intermediate
3. Dehydration → 2-decalone (specifically, the α,β-unsaturated ketone)

### Pattern 7: Polyalkylation Avoidance

**Question:** "Why does acetoacetic ester synthesis give clean monoalkylation while direct enolate alkylation often gives mixtures?"

**Answer:** The β-keto ester can be deprotonated, alkylated once, then the product is a monoalkylated β-keto ester. Further deprotonation is possible, but careful stoichiometry (1 equiv base, 1 equiv RX) controls the reaction. With direct enolate alkylation of simple ketones, the product is also enolizable, leading to polyalkylation unless a bulky base or directing group is used.

### Key Mnemonics

- **LDA = Low temp, Deprotonates Accessible** (kinetic)
- **NaOEt = Normal temp, Offers Equilibrium** (thermodynamic)
- **HVZ: PBr₃ makes the bromide, then Br₂ brominates the bromide**
- **Acetoacetic → Acetone-derived (ketone product); Malonic → Acid product**
- **Soft nucleophile + soft electrophile = Michael (1,4)**
- **Robinson = Ring-building via Michael + Aldol**
