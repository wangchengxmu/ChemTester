---
id: organic.openstax_ch21
layer: 2
title: Carboxylic Acid Derivatives and Acyl Substitution
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Carboxylic Acid Derivatives and Acyl Substitution

## Key Principles

### The Four Major Derivatives

All carboxylic acid derivatives share a common structural motif: an acyl group (R–C=O) bonded to a leaving group (LG):

```
    O
    ||
 R–C–LG
```

| Derivative | Leaving Group (LG) | General Formula | Reactivity |
|---|---|---|---|
| Acid chloride | Cl⁻ | RCOCl | Most reactive |
| Acid anhydride | RCOO⁻ | (RCO)₂O | Very reactive |
| Thioester | RS⁻ | RCOSR' | Moderately reactive |
| Ester | RO⁻ | RCOOR' | Less reactive |
| Amide | NH₂⁻ (or NHR⁻, NR₂⁻) | RCONR₂ | Least reactive |
| Carboxylate | None (stabilized) | RCOO⁻ | Not reactive (stable) |

### Reactivity Order: The Fundamental Hierarchy

**Most reactive → Least reactive:**

```
Acid chloride > Anhydride > Thioester > Ester > Amide > Carboxylate
```

This ordering is determined by:
1. **Leaving group ability:** Better leaving groups = more reactive
2. **Resonance donation:** Stronger resonance donation to the carbonyl = less electrophilic carbonyl carbon = less reactive
3. **Inductive effects:** Electron-withdrawing groups increase carbonyl electrophilicity

### Why This Order Exists

| Factor | Acid Chloride | Anhydride | Ester | Amide |
|---|---|---|---|---|
| Leaving group basicity | Cl⁻ (very weak base) | RCOO⁻ (moderate) | RO⁻ (moderate-strong) | NH₂⁻ (strong base) |
| Resonance donation to C=O | None (Cl doesn't donate) | Moderate | Moderate | Strong (N is good donor) |
| C=O electrophilicity | Very high | High | Moderate | Low |
| Overall reactivity | Very high | High | Moderate | Low |

**Key insight:** Cl⁻ is an excellent leaving group (weak base, stable anion) and doesn't donate electron density to the carbonyl. In contrast, NH₂⁻ is a terrible leaving group (strong base) and strongly donates into the carbonyl via resonance.

### The Nucleophilic Acyl Substitution Mechanism

All interconversions between carboxylic acid derivatives proceed through the same two-step mechanism:

**Step 1: Nucleophilic addition** to the carbonyl → tetrahedral intermediate
**Step 2: Elimination** of the leaving group → new derivative

```
    O                 O⁻               O
    ||                |                ||
 R–C–LG  +  Nu⁻  →  R–C–LG  →  R–C–LG  →  R–C–Nu  +  LG⁻
    |                 |                |
    Nu⁻              Nu               Nu
    (attack)      (tetrahedral      (collapse,
                   intermediate)     LG leaves)
```

**Rate-determining step:** Usually Step 1 (addition to carbonyl), especially for more reactive derivatives where Step 2 (collapse) is fast.

**Thermodynamic control:** The equilibrium position depends on the relative stability of the products vs reactants. You can always convert a more reactive derivative to a less reactive one, but not the reverse (without additional energy input).

### The Reactivity Ladder: What Can Convert to What

```
Acid chloride  →  Anhydride  →  Ester  →  Amide
     (can go down the ladder)          (can't go up)
```

- **Acid chloride** can be converted to anything below it (anhydride, ester, amide, carboxylic acid)
- **Anhydride** can be converted to ester, amide, carboxylic acid
- **Ester** can be converted to amide (with ammonia/amine) or carboxylic acid (hydrolysis) — but amide formation from ester is slow
- **Amide** is the thermodynamic sink — hard to convert to anything else
- **Carboxylic acid** is the thermodynamic sink for hydrolysis

**To go UP the ladder** (e.g., carboxylic acid → acid chloride), you need special reagents:

## Mechanisms

### 1. Formation of Acid Chlorides

**From carboxylic acid:**

| Reagent | Reaction | Byproducts | Notes |
|---|---|---|---|
| SOCl₂ (thionyl chloride) | RCOOH + SOCl₂ → RCOCl + SO₂↑ + HCl↑ | SO₂ gas, HCl gas | Most common, clean (gases escape) |
| PCl₃ (phosphorus trichloride) | 3 RCOOH + PCl₃ → 3 RCOCl + H₃PO₃ | H₃PO₃ | For acid-sensitive substrates |
| PCl₅ (phosphorus pentachloride) | RCOOH + PCl₅ → RCOCl + POCl₃ + HCl | POCl₃ | Less common |
| Oxalyl chloride (COCl)₂ | RCOOH + (COCl)₂ → RCOCl + CO₂↑ + CO↑ + HCl↑ | Gases | Very mild, used in peptide synthesis |

**Mechanism with SOCl₂:**
1. Carboxylic acid OH attacks SOCl₂ → chlorosulfite intermediate + Cl⁻
2. Cl⁻ attacks the carbonyl → tetrahedral intermediate
3. Collapse → RCOCl + SO₂ + Cl⁻ (SO₂ leaves as gas)
4. Cl⁻ attacks another molecule

**Advantage of SOCl₂:** All byproducts are gases (SO₂, HCl), so the product is pure after evaporation.

### 2. Fischer Esterification

**Reaction:** Carboxylic acid + alcohol ⇌ ester + water

**Conditions:** Catalytic acid (H₂SO₄ or HCl), heat, excess alcohol

**Mechanism (acid-catalyzed):**
1. **Protonation** of carbonyl oxygen → more electrophilic carbonyl
2. **Nucleophilic attack** by alcohol → tetrahedral intermediate
3. **Proton transfer:** OH₂⁺ → H₂O leaving group
4. **Elimination** of water → protonated ester
5. **Deprotonation** → ester

**Equilibrium considerations:**
- This is a **reversible** reaction (Le Chatelier's principle applies)
- To drive forward: use excess alcohol (or excess carboxylic acid), or remove water (Dean-Stark trap, molecular sieves)
- To drive reverse (ester hydrolysis): use excess water

**Reactivity order of alcohols:**
- **Methanol > 1° > 2° > 3°** (steric effects on nucleophilic attack)
- Tertiary alcohols are very slow (E1 dehydration competes)

**Selectivity:** If a molecule has both a carboxylic acid and an alcohol, **intramolecular** esterification (lactone formation) can occur preferentially.

### Product-Class Shortcut for Acid Chlorides

For benchmark product-class questions, first identify whether an acid chloride or acyl chloride is the starting carboxylic-acid derivative. Acid chlorides are highly reactive acyl donors: the nucleophile adds to the carbonyl, chloride leaves, and the nucleophile becomes the group attached to the acyl carbon.

Common product classes:
- Acid chloride + alcohol, phenol, or alkoxide -> ester + HCl or salt.
- Acid chloride + ammonia or amine -> amide + HCl or ammonium salt.
- Acid chloride + water -> carboxylic acid + HCl.
- Acid chloride + carboxylate -> acid anhydride.

Do not classify acid chloride plus alcohol as aldehyde formation. Aldehydes can be intermediates in special reductions of acid chlorides, but ordinary acyl substitution by an alcohol gives an ester.

### 3. Ester Hydrolysis

#### Acid-Catalyzed Hydrolysis
- **Reagents:** H₃O⁺, heat
- **Product:** Carboxylic acid + alcohol
- **Mechanism:** Reverse of Fischer esterification
- **Conditions:** Reflux in aqueous acid
- **Equilibrium:** Must drive forward with excess water

#### Base-Catalyzed Hydrolysis (Saponification)
- **Reagents:** NaOH or KOH, heat, aqueous
- **Product:** Carboxylate salt + alcohol
- **Mechanism:**
  1. OH⁻ attacks carbonyl → tetrahedral intermediate
  2. Collapse → carboxylate + alkoxide (RO⁻)
  3. RO⁻ is deprotonated by water → alcohol + OH⁻
- **Key difference from acid hydrolysis:** This is **irreversible** because the carboxylate ion is a very poor electrophile (stable anion, won't reform the ester)
- **Soap making:** Triglycerides + NaOH → glycerol + sodium carboxylates (soap)

**Acid vs base hydrolysis comparison:**

| Feature | Acid (H₃O⁺) | Base (OH⁻) |
|---|---|---|
| Product | Carboxylic acid | Carboxylate salt |
| Reversibility | Reversible | Irreversible |
| Mechanism | AAc1 or AAc2 | BAc2 |
| Rate | Moderate | Fast |
| Workup needed | None for acid | Acidify to get acid |

### 4. Transesterification

**Reaction:** Ester + alcohol → different ester (with acid catalyst)

**Conditions:** Catalytic acid (H₂SO₄, TsOH), excess of the new alcohol, heat

**Mechanism:** Same as Fischer esterification, but starting from ester instead of carboxylic acid:
1. Protonate ester carbonyl
2. New alcohol attacks → tetrahedral intermediate
3. Original alkoxide leaves → new ester

**Driving force:** Use large excess of the desired alcohol (Le Chatelier)

**Base-catalyzed transesterification:**
- Possible with alkoxide (RO⁻) as base
- RO⁻ attacks ester → tetrahedral intermediate → new alkoxide leaves
- This creates a new alkoxide, so the base is catalytic only if the alcohol is the same as the leaving group

**Applications:**
- Biodiesel production: triglycerides + methanol → methyl esters (with base catalyst)
- Polymer chemistry: exchanging ester groups

### 5. Anhydride Formation

**From acid chloride:**
- RCOCl + R'COO⁻ → (RCO)(R'CO)O (mixed anhydride)
- Or: 2 RCOCl + RCOO⁻ → (RCO)₂O (symmetrical anhydride)

**From carboxylic acid (dehydration):**
- 2 RCOOH → (RCO)₂O + H₂O
- **Reagents:** P₂O₅ (phosphorus pentoxide) or acetic anhydride (as dehydrating agent)
- Driven by removal of water

**Mixed anhydrides:** Useful in synthesis because the two acyl groups have different reactivities, allowing selective reactions.

### 6. Amide Formation

**From acid chloride (most common):**
- RCOCl + 2 R'NH₂ → RCONHR' + R'NH₃⁺Cl⁻
- **Why 2 equivalents of amine?** One equivalent neutralizes the HCl produced
- Works for primary and secondary amines
- Very efficient, high yielding

**From carboxylic acid (direct coupling):**
- **DCC coupling (dicyclohexylcarbodiimide):** RCOOH + R'NH₂ + DCC → RCONHR' + DCU (dicyclohexylurea)
- Widely used in peptide synthesis
- Side reaction: N-acylurea formation (rearrangement)

**Other coupling agents:**
| Reagent | Notes |
|---|---|
| EDC/HOBt | Water-soluble, mild, peptide synthesis |
| HATU | Very reactive, used in solid-phase peptide synthesis |
| CDI (carbonyldiimidazole) | Mild, generates imidazole as byproduct |

**From ester + amine:**
- Possible but slow; requires heating and often excess amine
- Not the preferred method

### 7. Reduction of Carboxylic Acid Derivatives

**LiAlH₄ (Lithium Aluminum Hydride):**
- **Most powerful** reducing agent for carbonyl compounds
- Reduces ALL carboxylic acid derivatives to **primary alcohols**

| Starting Material | Product with LiAlH₄ | Notes |
|---|---|---|
| Acid chloride | Primary alcohol | Via aldehyde (too fast to isolate) |
| Anhydride | 2 equivalents of primary alcohol | Each acyl group reduced |
| Ester | Primary alcohol | RCOOR' → RCH₂OH + R'OH |
| Amide | Amine (or alcohol) | Depends on substitution |
| Primary amide | Primary amine | RCONH₂ → RCH₂NH₂ |
| Secondary amide | Secondary amine | RCONHR' → RCH₂NHR' |
| Tertiary amide | Tertiary amine | RCONR'₂ → RCH₂NR'₂ |
| Carboxylic acid | Primary alcohol | Must be activated first (LiAlH₄ reacts with COOH) |
| Nitrile | Primary amine | RCN → RCH₂NH₂ |

**NaBH₄ (Sodium Borohydride):**
- **Milder** than LiAlH₄
- Reduces aldehydes and ketones → alcohols
- Does NOT reduce carboxylic acids, esters, amides (usually)
- **Exception:** NaBH₄ CAN reduce acid chlorides and anhydrides (more reactive)
- NaBH₄ + LiCl → more reactive (can reduce esters)

**Rosenmund Reduction:**
- **Reaction:** Acid chloride → aldehyde (stop at aldehyde, don't reduce further)
- **Conditions:** H₂, Pd catalyst poisoned with BaSO₄ and quinoline (Lindlar-type poison)
- The poisoned catalyst reduces the acid chloride to aldehyde but not to alcohol
- **Scope:** Works for aromatic and aliphatic acid chlorides
- **Limitation:** Sensitive to over-reduction; careful control needed

**DIBAL-H (Diisobutylaluminum Hydride):**
- Reduces esters to **aldehydes** at low temperature (-78°C)
- Mechanism: forms a tetrahedral intermediate that, upon aqueous workup, releases the aldehyde
- Also reduces nitriles to aldehydes (via imine intermediate)
- Key: must be at low temperature and careful workup

**Reduction summary table:**

| Reagent | Ester → | Amide → | Acid Chloride → | Nitrile → |
|---|---|---|---|---|
| LiAlH₄ | Primary alcohol | Amine | Primary alcohol | Primary amine |
| NaBH₄ | No reaction | No reaction | Primary alcohol | No reaction |
| DIBAL-H | Aldehyde (-78°C) | Aldehyde | Aldehyde | Aldehyde |
| LiAlH₄ then H₂O | — | — | — | — |
| Rosenmund (H₂/Pd/BaSO₄) | — | — | Aldehyde | — |

### 8. Amide Resonance and Its Consequences

**The amide resonance structure:**

```
    O              O⁻
    ||             |
 R–C–N–R'    ↔   R–C=N⁺–R'
```

**Consequences of amide resonance:**
1. **C–N bond has partial double bond character** (~40% double bond, ~60% single bond)
2. **Planar geometry:** The amide nitrogen is sp² hybridized (trigonal planar)
3. **Restricted rotation:** The C–N bond does NOT rotate freely at room temperature (rotation barrier ~15-20 kcal/mol)
4. **Reduced basicity:** The nitrogen lone pair is delocalized → amides are very weak bases
5. **Reduced reactivity:** The carbonyl carbon is less electrophilic because the nitrogen donates electron density
6. **Length:** C–N bond in amides is shorter than a typical C–N single bond (1.33 Å vs 1.47 Å)

### 9. Lactones and Lactams

**Definition:** Intramolecular esters (lactones) and intramolecular amides (lactams).

**Nomenclature:** Named by the ring size using Greek letters or carbon count.

| Ring Size | Lactone Name | Lactam Name | Stability |
|---|---|---|---|
| 3-membered | α-lactone (very rare) | α-lactam (unstable) | Poor |
| 4-membered | β-lactone (rare) | β-lactam (penicillin core) | Moderate (β-lactam important in antibiotics) |
| 5-membered | γ-lactone | γ-lactam | Good |
| 6-membered | δ-lactone | δ-lactam (piperidone) | Very good |
| 7+ | ε-lactone | ε-lactam | Variable |

**β-Lactam antibiotics:** The four-membered β-lactam ring is highly strained, making it very reactive toward nucleophilic attack by bacterial transpeptidases (the target enzyme). This reactivity is the basis of penicillin, cephalosporin, and related antibiotics.

**Lactone/lactam formation from hydroxy/amino acids:**
- Intermolecular Fischer esterification or amide formation → lactone/lactam
- 5- and 6-membered rings form readily
- Larger rings: more difficult (dilution technique helps)

## Selectivity Rules

### Choosing the Right Derivative for a Transformation

| Target | Best Starting Material | Method |
|---|---|---|
| Amide from acid | Acid chloride | RCOCl + 2 RNH₂ |
| Ester from acid | Direct (Fischer) | RCOOH + R'OH, H⁺ |
| Acid chloride from acid | Direct | SOCl₂ |
| Anhydride from acid | Acid chloride + carboxylate | RCOCl + RCOO⁻ |
| Aldehyde from acid | Acid chloride → Rosenmund | RCOCl + H₂/Pd/BaSO₄ |
| Aldehyde from ester | Ester + DIBAL-H | -78°C, then H₂O |
| Alcohol from ester | Ester + LiAlH₄ | Then H₂O |
| Alcohol from acid | Acid + LiAlH₄ | Then H₂O |
| Amine from amide | Amide + LiAlH₄ | RCONH₂ → RCH₂NH₂ |

### Hydrolysis Conditions

| Derivative | Acid Hydrolysis | Base Hydrolysis |
|---|---|---|
| Acid chloride | Instant (water) | Instant (NaOH) |
| Anhydride | Fast | Fast |
| Ester | Moderate (reflux) | Fast (NaOH, reflux) |
| Amide | Slow (prolonged heating) | Moderate (NaOH, prolonged heating) |

### Protection: Ester vs Amide as Protecting Groups

| Feature | Ester | Amide |
|---|---|---|
| Stability to base | Poor (hydrolyzed) | Moderate |
| Stability to acid | Moderate | Good |
| Stability to nucleophiles | Poor (transesterification) | Good |
| Ease of formation | Easy (Fischer) | Moderate (acid chloride) |
| Ease of removal | Base hydrolysis | Strong acid or base |

### Chemoselectivity in Reductions

| Reagent | Reduces | Does NOT Reduce |
|---|---|---|
| LiAlH₄ | Everything (acid Cl, anhydride, ester, amide, aldehyde, ketone, epoxide) | C=C, benzene, nitro |
| NaBH₄ | Aldehyde, ketone, acid chloride | Ester, amide, carboxylic acid, C=C |
| DIBAL-H | Ester → aldehyde (at -78°C) | At higher temps → alcohol |
| Rosenmund | Acid chloride → aldehyde | Ester, amide |
| H₂/Pd | C=C, C≡C, aldehyde, ketone (sometimes) | Carboxylic acid derivatives |

## Common Exam Patterns

### Pattern 1: Predicting Acyl Substitution Products

**Question:** "What is the product when acetyl chloride reacts with ammonia?"

**Answer:** Acetamide (CH₃CONH₂). The chloride is replaced by the amine. Use 2 equivalents of NH₃ (one reacts, one neutralizes HCl).

### Pattern 2: Fischer Esterification Equilibrium

**Question:** "How would you drive the Fischer esterification of benzoic acid with ethanol to completion?"

**Answer:**
- Use excess ethanol (shift equilibrium right)
- Remove water (Dean-Stark trap, molecular sieves)
- Both strategies apply Le Chatelier's principle

### Pattern 3: Hydrolysis Product Identification

**Question:** "What products are formed when ethyl butanoate is treated with NaOH, then acidified?"

**Answer:** 
1. NaOH (saponification): sodium butanoate + ethanol
2. Acidify: butanoic acid + ethanol

### Pattern 4: Choosing Reducing Agent

**Question:** "How would you convert methyl benzoate to benzaldehyde?"

**Answer:** DIBAL-H at -78°C in THF, then careful aqueous workup. LiAlH₄ would give benzyl alcohol (over-reduction). Rosenmund works on acid chlorides, not esters.

### Pattern 5: Amide Resonance Questions

**Question:** "Why do amides have restricted rotation about the C–N bond?"

**Answer:** The nitrogen lone pair is delocalized into the carbonyl π* orbital (resonance), giving the C–N bond partial double bond character. Breaking this partial double bond requires ~15-20 kcal/mol, making rotation slow at room temperature. NMR shows two distinct signals for N-substituents at low temperature.

### Pattern 6: Reactivity Order Applications

**Question:** "Which is more reactive toward nucleophilic attack: acetic anhydride or ethyl acetate?"

**Answer:** Acetic anhydride is more reactive. In the reactivity hierarchy, anhydrides are above esters. The acetate leaving group (CH₃COO⁻) is a better leaving group than ethoxide (EtO⁻), and the anhydride carbonyl is more electrophilic.

### Pattern 7: Multi-Step Synthesis Planning

**Question:** "Design a synthesis of N-methylbenzamide from benzoic acid."

**Answer:**
1. Benzoic acid + SOCl₂ → benzoyl chloride
2. Benzoyl chloride + CH₃NH₂ (2 eq) → N-methylbenzamide + CH₃NH₃⁺Cl⁻
- Alternative: Coupling reagent (DCC) + methylamine (less common in practice)

### Pattern 8: Lactone/Lactam Formation

**Question:** "What lactone is formed from 4-hydroxybutanoic acid?"

**Answer:** γ-Butyrolactone (5-membered ring, γ-lactone). The hydroxyl and carboxylic acid groups are separated by 3 carbons, forming a 5-membered ring upon intramolecular esterification.

### Key Mnemonics

- **"CAnTEA"** for reactivity: **C**hloride > **A**nhydride > **T**hioester > **E**ster > **A**mide (descending reactivity)
- **"SOCl₂ = SO₂ + HCl (gases leave, clean reaction)"**
- **"LiAlH₄ reduces everything; NaBH₄ is picky"**
- **"DIBAL-H = aldehydes from esters at -78°C"**
- **"Rosenmund = acid chloride to aldehyde (poisoned Pd)"**
- **"Amide resonance: C–N is part double bond, planar, no rotation"**
- **"β-lactam = 4-membered ring = strained = reactive = antibiotics"**
- **"γ = 5-membered, δ = 6-membered"** for lactone/lactam ring size
- **"Saponification = base hydrolysis of ester = soap"**
- **"Acid hydrolysis = reversible; base hydrolysis = irreversible"**
