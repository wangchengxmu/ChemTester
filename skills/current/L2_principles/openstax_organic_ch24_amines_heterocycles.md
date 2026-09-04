---
id: organic.openstax_ch24
layer: 2
title: Amines and Heterocyclic Chemistry
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Amines and Heterocyclic Chemistry

## Key Principles

### Amine Classification and Nomenclature

| Classification | Structure | Example |
|---|---|---|
| Primary (1°) | RNH₂ | Methylamine |
| Secondary (2°) | R₂NH | Dimethylamine |
| Tertiary (3°) | R₃N | Trimethylamine |
| Quaternary (4°) | R₄N⁺ X⁻ | Tetramethylammonium chloride |

**IUPAC:** "-amine" suffix (alkanamine), or "amino-" prefix for substituents on larger chains.

**Common names:** Aniline (PhNH₂), pyridine, pyrrole, etc. are retained IUPAC names.

### Amine Basicity

Basicity is the single most important property for understanding amine chemistry. The pKa of the conjugate acid (pKaH) measures basicity — higher pKaH = stronger base.

#### Basicity Trends in Water

| Amine | pKaH (in H₂O) | Notes |
|---|---|---|
| NH₃ | 9.25 | Reference |
| CH₃NH₂ | 10.64 | Electron-donating CH₃ increases basicity |
| (CH₃)₂NH | 10.73 | Maximal inductive effect |
| (CH₃)₃N | 9.79 | **Solvation penalty outweighs inductive effect** |
| PhNH₂ (aniline) | 4.63 | **Resonance delocalization** of lone pair into ring |
| (CH₃)₃N⁺ (ammonium) | — | Not basic (no lone pair) |

**Why R₂NH > RNH₂ > R₃N in water:**
- **Inductive effect:** More alkyl groups = more electron donation = higher basicity
- **Solvation effect:** Ammonium ions are stabilized by hydrogen bonding with water. NH₄⁺ has 4 H-bonds; RNH₃⁺ has 3; R₂NH₂⁺ has 2; R₃NH⁺ has 1
- The solvation penalty for R₃NH⁺ (only 1 H-bond) outweighs the inductive benefit of three alkyl groups
- **Net result:** Secondary amines are the strongest bases in water

**In the gas phase (no solvation):**
- R₃N > R₂NH > RNH₂ > NH₃ (inductive effect dominates without solvation)

#### Aniline and Aromatic Amine Basicity

**Aniline is much less basic (pKaH = 4.6) than aliphatic amines (pKaH ~10-11)** because:
- The nitrogen lone pair is delocalized into the aromatic ring (resonance)
- Seven resonance structures stabilize the aniline form
- Protonation destroys this resonance stabilization
- The energy cost of losing resonance ≈ the energy gain of forming N–H bond

**Substituent effects on aniline basicity:**

| Substituent (para) | pKaH | Effect | Reason |
|---|---|---|---|
| –NH₂ | 5.98 | ↑↑ | Strong electron-donating, resonance |
| –OCH₃ | 5.34 | ↑ | Electron-donating, resonance |
| –CH₃ | 5.10 | ↑ | Electron-donating, inductive |
| –H | 4.63 | Reference | — |
| –Cl | 3.98 | ↓ | Electron-withdrawing, inductive |
| –CN | 1.74 | ↓↓ | Strong electron-withdrawing, resonance |
| –NO₂ | 1.00 | ↓↓↓ | Very strong electron-withdrawing |

**Ortho substituents:** Can have additional steric effects that hinder solvation of the conjugate acid, further reducing basicity (e.g., o-nitroaniline is much less basic than p-nitroaniline).

### Amine Nucleophilicity

**Nucleophilicity ≠ Basicity.** Nucleophilicity depends on:
1. **Basicity** (stronger base → generally more nucleophilic)
2. **Steric hindrance** (bulky groups slow attack)
3. **Solvation** (poorly solvated anions are more reactive)

**Trends:**
- R₂NH > RNH₂ > R₃N > NH₃ (in polar protic solvents, steric effect)
- In polar aprotic solvents: R₃N becomes relatively more nucleophilic
- **Amide nitrogen** (RCONH₂) is a very poor nucleophile (lone pair delocalized into C=O)
- **Pyridine** is a good nucleophile for coordination metals but a poor nucleophile for SN2

## Mechanisms

### 1. Amine Synthesis Methods

#### Gabriel Synthesis
- **Starting material:** Phthalimide
- **Reagents:** KOH → deprotonate → K⁺ phthalimide; then add primary alkyl halide (SN2)
- **Hydrolysis:** Hydrazine (NH₂NH₂) or NaOH/heat → releases the primary amine
- **Scope:** **Primary amines only** (requires primary alkyl halide for SN2)
- **Advantage:** Clean, no overalkylation (the phthalimide nitrogen can only be alkylated once)
- **Does NOT work for:** secondary/tertiary halides (SN2 required), aryl halides (too unreactive)

#### Reduction Methods

| Starting Material | Reagent | Product | Notes |
|---|---|---|---|
| Nitro compound (ArNO₂) | H₂/Pd or Sn/HCl or Fe/HCl | Aniline (ArNH₂) | Classic method for aromatic amines |
| Nitrile (RCN) | LiAlH₄ or H₂/Ni | Primary amine (RCH₂NH₂) | Adds one carbon |
| Amide (RCONH₂) | LiAlH₄ | Amine (RCH₂NH₂) | From primary amide → primary amine |
| Oxime (R₂C=NOH) | LiAlH₄ | Primary amine (R₂CHNH₂) | Reductive amination alternative |
| Azide (RN₃) | LiAlH₄ or H₂/Pd | Primary amine (RNH₂) | Staudinger or catalytic hydrogenation |
| Iminium ion | NaBH₃CN | Amine | Reductive amination |

#### Hofmann Rearrangement
- **Starting material:** Primary amide (RCONH₂)
- **Reagents:** Br₂ + NaOH (or NaOBr)
- **Product:** Primary amine with **one fewer carbon** (RNH₂ from RCONH₂, loses CO₂)
- **Mechanism:**
  1. Base deprotonates amide → N⁻
  2. N⁻ attacks Br₂ → N-bromoamide
  3. Base deprotonates → bromamide anion → rearrangement (R migration to N) with loss of Br⁻
  4. Isocyanate intermediate (RN=C=O)
  5. Hydrolysis → carbamic acid → CO₂ + primary amine
- **Key:** The R group migrates with retention of configuration (if chiral)
- **Contrast with Curtius rearrangement:** Acyl azide → isocyanate → amine (similar, but different reagents)

#### Reductive Amination
- **General:** Aldehyde/ketone + amine + reducing agent → alkylated amine
- **Steps:**
  1. Amine + carbonyl → imine (or iminium ion)
  2. Reduction → amine
- **Reagents:** NaBH₃CN (cyanoborohydride, selective for iminium at pH 6-7) or NaBH(OAc)₃
- **Scope:** Primary or secondary amines; works with aldehydes and ketones
- **Advantage:** One-pot alkylation of amines without overalkylation issues

### 2. Hofmann Elimination

**Definition:** Elimination of a quaternary ammonium hydroxide to form the **least substituted** alkene (anti-Zaitsev).

**Steps:**
1. Amine + excess CH₃I → quaternary ammonium iodide (exhaustive methylation)
2. Ag₂O + H₂O → quaternary ammonium hydroxide
3. Heat → **E2 elimination** with the bulky leaving group N(CH₃)₃

**Key feature: anti-Zaitsev (Hofmann product)**
- The bulky N(CH₃)₃ leaving group is the largest leaving group in elimination reactions
- The base is hydroxide (small but constrained by sterics)
- The transition state for forming the more substituted alkene is too crowded with the bulky N(CH₃)₃ group
- Therefore, the **less substituted** alkene forms preferentially

**With other bulky bases:**
- t-BuOK + ammonium salt → Hofmann elimination (less substituted alkene)
- This is a general trend: **bulky base + bulky leaving group → Hofmann product**

### 3. Diazonium Salt Chemistry

**Formation:** Aniline + NaNO₂ + HCl (0-5°C) → benzene diazonium chloride (PhN₂⁺Cl⁻)

**Why low temperature?** Diazonium salts are unstable and decompose above ~5°C (explosive when dry).

#### Sandmeyer Reaction
- **CuCl** → **aryl chloride** (ArCl)
- **CuBr** → **aryl bromide** (ArBr)
- **CuCN** → **aryl nitrile** (ArCN) — can be hydrolyzed to carboxylic acid
- **Mechanism:** Radical pathway via Cu(I)/Cu(II) redox cycle

#### Diazonium Replacement Reactions

| Reagent | Product | Conditions |
|---|---|---|
| H₂O, heat | Phenol (ArOH) | Warm aqueous |
| H₃PO₂ (hypophosphorous acid) | Benzene (ArH) | Replacement by H |
| CuCl | Aryl chloride | Sandmeyer |
| CuBr | Aryl bromide | Sandmeyer |
| CuCN | Aryl nitrile | Sandmeyer |
| KI | Aryl iodide | Direct displacement |
| Cu powder | Biaryl (Ar–Ar) | Gomberg-Bachmann coupling |
| BF₄⁻, heat | Aryl fluoride | Schiemann reaction |

#### Azo Coupling
- Diazonium salt + activated aromatic compound → **azo dye** (Ar–N=N–Ar')
- The coupling partner must be strongly activated (phenol, aniline, naphthol)
- Coupling occurs **para** to the activating group (or ortho if para is blocked)
- The azo group is brightly colored (conjugated N=N chromophore)

## Heterocyclic Chemistry

### Classification by Saturation

| Type | Description | Examples |
|---|---|---|
| Aromatic | Planar, 6π electrons (Hückel), fully unsaturated | Pyridine, pyrrole, furan, thiophene |
| Non-aromatic | Saturated or partially unsaturated | Piperidine, tetrahydrofuran |
| Anti-aromatic | 4n π electrons, unstable | Cyclobutadiene (rare in nature) |

### The Aromatic Heterocycles: A Unified Framework

All five-membered and six-membered aromatic heterocycles follow Hückel's rule (4n+2 π electrons) but contribute electrons differently.

#### Five-Membered Rings (6π, 4 from C=C + 2 from heteroatom)

| Heterocycle | Heteroatom | Aromaticity Source | pKaH (conjugate acid) | Basicity |
|---|---|---|---|---|
| Pyrrole | NH | Lone pair in the ring (part of 6π) | -3.8 | Essentially non-basic |
| Furan | O | Lone pair in the ring | -0.4 | Non-basic |
| Thiophene | S | Lone pair in the ring | — | Non-basic |

**Critical concept:** In five-membered aromatic heterocycles, the heteroatom contributes its lone pair to the aromatic sextet. This means:
- The lone pair is NOT available for protonation → very low basicity
- The ring is electron-rich → very reactive toward electrophilic aromatic substitution (EAS)
- Reactivity order: **furan > pyrrole > thiophene > benzene**

#### Six-Membered Rings (6π, 3 from C=C + 1 from heteroatom, heteroatom lone pair NOT in ring)

| Heterocycle | Heteroatom | Lone Pair | pKaH | Basicity |
|---|---|---|---|---|
| Pyridine | N | NOT in ring (sp², in plane) | 5.25 | Weakly basic |
| Pyrimidine | 2 N | Neither in ring | 1.30 | Very weakly basic |

**Critical concept:** In pyridine, the nitrogen lone pair is in an sp² orbital perpendicular to the π system (in the plane of the ring). This means:
- The lone pair IS available for protonation → pyridine is basic
- The nitrogen is electron-withdrawing (inductive) → pyridine is **deactivated** toward EAS
- EAS on pyridine requires harsh conditions and gives meta products

### Electrophilic Aromatic Substitution on Heterocycles

#### Reactivity Toward EAS

| Heterocycle | Reactivity vs Benzene | Preferred Position | Directing Effect |
|---|---|---|---|
| Furan | ~10⁶ × more reactive | C2 > C3 | Both positions possible |
| Pyrrole | ~10⁵ × more reactive | C2 > C3 | C2 preferred |
| Thiophene | ~10³ × more reactive | C2 > C3 | C2 preferred |
| Pyridine | ~10⁻⁸ × less reactive | C3 | Meta director |
| Benzene | Reference | — | — |

**Why C2 > C3 for five-membered rings:**
- Electrophilic attack at C2 generates a resonance structure that places positive charge on the heteroatom (which is more electronegative and can stabilize it better)
- Attack at C3 does not generate this stabilizing resonance structure
- The difference is significant: C2 is typically 5-10× more reactive than C3

**Pyridine reactivity:**
- Very deactivated (nitrogen withdraws electrons inductively)
- Requires **extreme conditions** (e.g., fuming H₂SO₄ at 300°C for nitration)
- Gives **meta** products (N is meta-directing, analogous to nitrobenzene)
- Better to use nucleophilic aromatic substitution (NAS) instead

### Important Heterocyclic Reactions

#### Pyrrole
- **Acid-sensitive:** Protonation destroys aromaticity → polymerizes in acid
- **Vilsmeier-Haack formylation:** POCI₃ + DMF → 2-formylpyrrole
- **Friedel-Crafts:** Works with mild Lewis acids; avoid strong protic acids
- **Knorr pyrrole synthesis:** α-amino ketone + β-keto ester → pyrrole

#### Pyridine
- **N-oxide formation:** Pyridine + m-CPBA → pyridine N-oxide (activates the ring toward EAS)
- **Nucleophilic substitution:** Pyridine reacts with strong nucleophiles (NaNH₂) at C2 (Chichibabin reaction)
- **Reduction:** NaBH₄/CrCl₃ or catalytic hydrogenation → piperidine

#### Indole
- **Fischer indole synthesis:** Phenylhydrazone + acid catalyst → indole (via [3,3] sigmatropic rearrangement)
- **Reactivity:** Electrophilic substitution at **C3** (not C2, unlike pyrrole!) because the benzene ring changes the electronic distribution
- **Very important biologically:** tryptophan, serotonin, melatonin

### Key Synthesis Methods for Heterocycles

| Heterocycle | Synthesis Method | Key Reagents |
|---|---|---|
| Pyrrole | Paal-Knorr | 1,4-dicarbonyl + primary amine |
| Pyrrole | Knorr | α-amino ketone + β-keto ester |
| Indole | Fischer indole | Phenylhydrazone + ZnCl₂ (or other acid) |
| Pyridine | Hantzsch | Aldehyde + 2 eq β-keto ester + NH₃ |
| Furan | Paal-Knorr | 1,4-dicarbonyl + acid catalyst |
| Thiophene | Paal-Knorr | 1,4-dicarbonyl + P₂S₅ or Lawesson's reagent |
| Imidazole | Debus-Radziszewski | 1,2-dicarbonyl + aldehyde + ammonia |
| Pyrimidine | Biginelli | Aldehyde + β-keto ester + urea |

### Amine Protection Strategies

When you need to temporarily protect an amine during a reaction:

| Protecting Group | Install | Remove | Stability |
|---|---|---|---|
| Acetyl (Ac) | Ac₂O or AcCl | NaOH/H₂O or LiAlH₄ | Base-labile |
| Boc (t-butoxycarbonyl) | Boc₂O, base | TFA or HCl | Acid-labile |
| Cbz (benzyloxycarbonyl) | Cbz-Cl, base | H₂/Pd | H₂-labile |
| Phthalimide | Phthalic anhydride, heat | NH₂NH₂ | Hydrazine-labile |
| Tosyl (Ts) | TsCl, pyridine | Na/NH₃ (Birch) | Very stable |

## Common Exam Patterns

### Pattern 1: Predicting Amine Basicity

**Question:** "Rank these amines from most basic to least basic: aniline, ammonia, trimethylamine, dimethylamine."

**Answer:** In water: dimethylamine (pKaH 10.73) > ammonia (9.25) > trimethylamine (9.79) > aniline (4.63). Wait — actually: dimethylamine > trimethylamine > ammonia > aniline. The key point is aniline is always the weakest due to resonance delocalization.

### Pattern 2: Choosing an Amine Synthesis

**Question:** "How would you make 1-butanamine from 1-bromobutane?"

**Answer:** 
- **Gabriel synthesis:** Phthalimide + KOH → potassium phthalimide; then add 1-bromobutane (SN2); then hydrazine → 1-butanamine
- **Alternative:** Convert to nitrile (NaCN, SN2) → reduce with LiAlH₄

### Pattern 3: Hofmann vs Zaitsev Elimination

**Question:** "Treatment of (CH₃)₃CN(CH₃)₃⁺ OH⁻ with heat gives which alkene?"

**Answer:** Hofmann elimination → the least substituted alkene. The product is (CH₃)₂C=CH₂ (isobutylene, 1-methylpropene), not (CH₃)₂CHCH=CH₂ (which would be Zaitsev).

### Pattern 4: Diazonium Chemistry

**Question:** "How would you convert aniline to benzoic acid?"

**Answer:**
1. NaNO₂ + HCl, 0-5°C → diazonium salt
2. CuCN → benzonitrile (Sandmeyer)
3. H₃O⁺, heat → hydrolysis → benzoic acid

Or alternatively:
1. Diazonium salt
2. CuCN → benzonitrile
3. NaOH, heat → benzoate; then acidify

### Pattern 5: Heterocycle EAS Position

**Question:** "Where does bromination of pyrrole occur?"

**Answer:** At **C2** (the position adjacent to nitrogen). The 2-position is favored because the intermediate carbocation from C2 attack is stabilized by a resonance structure with positive charge on nitrogen. If C2 is already substituted, bromination occurs at C3.

### Pattern 6: Pyridine vs Pyrrole Basicity

**Question:** "Why is pyridine basic but pyrrole is not?"

**Answer:** In pyridine, the nitrogen lone pair is in an sp² orbital in the plane of the ring (NOT part of the π system), so it is available for protonation. In pyrrole, the nitrogen lone pair is part of the aromatic 6π electron system, so protonating it would destroy aromaticity — a huge energetic penalty.

### Pattern 7: Fischer Indole Synthesis

**Question:** "What product is formed from the Fischer indole synthesis of acetophenone phenylhydrazone?"

**Answer:** Acetophenone phenylhydrazone (from acetophenone + phenylhydrazine) undergoes acid-catalyzed [3,3] sigmatropic rearrangement → cyclization → loss of NH₃ → **2-methylindole**. The methyl group from acetophenone ends up at the C3 position of indole.

### Key Mnemonics

- **"Aniline is weakly basic because the lone pair plays in the ring"** (resonance)
- **"Pyrrole is non-basic because the lone pair IS the ring"** (aromaticity)
- **"Pyridine: lone pair in plane → basic; pyrrole: lone pair in π → aromatic"**
- **"C2 before C3"** for five-membered heterocycle EAS
- **"Furan > pyrrole > thiophene > benzene"** for EAS reactivity
- **"Pyridine is electron-poor, meta-directing, deactivated"**
- **"Indole: C3 for EAS"** (exception to C2 rule)
- **"Hofmann = less substituted alkene; Zaitsev = more substituted"**
- **"Sandmeyer: Cu gives you Cl, Br, or CN"**
- **"Gabriel = primary amine from primary halide"**
