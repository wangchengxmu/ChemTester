# Protecting Group Strategies

> **L2 Principle File** — Graduate-level reference on protecting groups in organic synthesis
> **Links to:** [L1 Chemistry Core Map](../L1_ontology/chemistry-core-map.md) | **See also:** [Retrosynthetic Analysis](retrosynthetic_analysis.md)

---

## Table of Contents

1. [Principles of Protection/Deprotection](#1-principles-of-protectiondeprotection)
2. [Alcohol Protection](#2-alcohol-protection)
3. [Amine Protection](#3-amine-protection)
4. [Carbonyl Protection](#4-carbonyl-protection)
5. [Carboxylic Acid Protection](#5-carboxylic-acid-protection)
6. [Phosphate Protection](#6-phosphate-protection)
7. [Orthogonal Protection Schemes](#7-orthogonal-protection-schemes)
8. [Deprotection Conditions Summary Tables](#8-deprotection-conditions-summary-tables)
9. [Greener Alternatives](#9-greener-alternatives)
10. [Worked Examples](#10-worked-examples)

---

## 1. Principles of Protection/Deprotection

### 1.1 Chemoselectivity

**Definition:** The ability to selectively protect or deprotect one functional group in the presence of others without affecting sensitive functionalities.

**Key Considerations:**

| Factor | Impact on Selectivity |
|--------|----------------------|
| Steric hindrance | Bulky groups protect slower, deprotect harder |
| Electronic effects | Electron-rich/deficient sites react at different rates |
| Reaction conditions | pH, temperature, solvent, catalyst choice |
| Kinetic vs thermodynamic control | Fast reacting vs most stable product |

**Selectivity Hierarchy (general reactivity order):**

```
Primary alcohol > Secondary alcohol > Tertiary alcohol
Primary amine > Secondary amine
Aldehyde > Ketone
```

**Exploiting Reactivity Differences:**

- **TMS vs TBDMS:** TMS silyl ethers are 10-100× more labile to hydrolysis
- **Primary vs secondary alcohols:** Use bulky reagents (TBDPSCl) for selective primary protection
- **1,2- vs 1,3-diols:** Cyclic acetals form preferentially with 1,2-diols (5-membered) over 1,3-diols (6-membered)

### 1.2 Orthogonal Sets

**Definition:** A collection of protecting groups that can be removed independently under different conditions without affecting the others.

**Classic Orthogonal Sets:**

**Set 1: Acid/Base/Fluoride Orthogonality**
```
Acid-labile:    Boc, THP, Tr, MOM (mild acid)
Base-labile:    Ac, Bz, Fmoc (mild base)
Fluoride-labile: TBDMS, TBDPS, TIPS, TMS
Hydrogenolysis:  Bn, Cbz
```

**Set 2: Peptide Synthesis Orthogonal Set**
```
N-terminal:    Fmoc (base: piperidine)
Side-chain:    t-Bu (acid: TFA)
Sulfur:        Trt (acid: TFA, milder)
Other:         Alloc (Pd(0) deprotection)
```

**Set 3: Carbohydrate Synthesis**
```
Anomeric:      Various glycosyl donors
2-OH:          Esters (participating) or ethers (non-participating)
3,4,6-OH:      Bn (hydrogenolysis), Bz (base), TBDMS (F-)
```

### 1.3 Stability Windows

**Concept:** Each protecting group has a "window" of conditions under which it is stable, defined by pH range, temperature tolerance, and compatibility with common reagents.

**Stability Matrix (Relative):**

| PG | Acid (mild) | Acid (strong) | Base (mild) | Base (strong) | Nucleophiles | Redox |
|----|-------------|---------------|-------------|---------------|--------------|-------|
| TMS | Unstable | Unstable | Stable | Unstable | Sensitive | Stable |
| TBDMS | Stable | Unstable | Stable | Moderate | Stable | Stable |
| TBDPS | Stable | Moderate | Stable | Stable | Stable | Stable |
| Ac | Stable | Stable | Unstable | Unstable | Sensitive | Stable |
| Bn | Stable | Stable | Stable | Stable | Stable | Unstable (H₂) |
| Boc | Unstable | Unstable | Stable | Stable | Stable | Stable |
| Fmoc | Stable | Stable | Unstable | Unstable | Stable | Stable |

**Stability Under Common Conditions:**

```
Acid Stability (to TFA, pH 2-4):
    TMS < THP < Boc < Tr < MOM < PMB < TBDMS < TBDPS < Bn < Ac < Bz

Base Stability (to NaOH, Et3N, DBU):
    Fmoc < Ac < Bz < Piv < TMS < TBDMS < TIPS < TBDPS < Bn < MOM < THP

Fluoride Stability:
    TMS << TBDMS < TIPS < TBDPS (TMS most labile)

Redox Stability:
    Reducing: Bn, Cbz, PMB sensitive to H₂/Pd
    Oxidizing: Most silyl ethers stable; dithianes sensitive
```

### 1.4 Tactical Considerations

**Protection Timing:**

1. **Early vs Late Protection**
   - Early: Protect immediately after introduction of sensitive group
   - Late: Protect only before the step requiring protection
   - Trade-off: Early protection adds steps but prevents side reactions

2. **Global vs Selective Protection**
   - Global: Protect all groups of same type simultaneously
   - Selective: Protect specific sites based on reactivity differences

3. **Temporary vs Persistent Protection**
   - Temporary: Removed soon after the critical step
   - Persistent: Carried through multiple steps

**Choosing a Protecting Group — Decision Tree:**

```
1. What functional groups must survive deprotection?
   └─→ Eliminate groups with incompatible deprotection conditions

2. What reaction conditions will the protected substrate encounter?
   └─→ Ensure stability window covers all planned conditions

3. Are multiple orthogonal protections needed?
   └─→ Select orthogonal set with appropriate deprotection order

4. What is the deprotection sequence?
   └─→ Plan so later deprotections don't affect earlier ones

5. Are there stereochemical considerations?
   └─→ Consider participating vs non-participating groups
```

**Common Mistakes to Avoid:**

- Using Boc when strong base is required later
- Using acetate when basic hydrolysis is planned
- Using benzyl when hydrogenation affects other groups (alkenes, nitro)
- Using TMS for multi-step sequences (too labile)
- Overlooking migration (e.g., silyl migration in diols)

---

## 2. Alcohol Protection

### 2.1 Silyl Ethers

**General Formula:** R₃Si-OR'

**Reactivity Trend (protection):**
```
TMS > TBDMS ≈ TIPS > TBDPS
(bulky = slower protection, more selective)
```

**Reactivity Trend (deprotection):**
```
TMS >> TBDMS > TIPS > TBDPS
(TMS most labile to hydrolysis and fluoride)
```

#### Trimethylsilyl (TMS)

| Property | Details |
|----------|---------|
| Reagent | TMSCl, HMDS (hexamethyldisilazane), TMSOTf |
| Base | Et₃N, imidazole, pyridine |
| Solvent | DMF, CH₂Cl₂ |
| Conditions | RT, 0.5-2 h |
| Deprotection | Mild acid (pH 4-5), TBAF, KF, aqueous workup |
| Stability | Very labile — moisture sensitive |
| Use | Temporary protection, GC/MS derivatization |

**Formation:**
```
ROH + TMSCl + Et₃N → ROSiMe₃ + Et₃NH⁺Cl⁻
ROH + HMDS + cat. TMSOTf → ROSiMe₃ + NH₃
```

**Deprotection:**
```
ROSiMe₃ + H₂O (pH 4-5) → ROH + Me₃SiOH
ROSiMe₃ + TBAF → ROH + Me₃SiF + TBA⁺
```

#### tert-Butyldimethylsilyl (TBDMS)

| Property | Details |
|----------|---------|
| Reagent | TBDMSCl, TBDMSOTf |
| Base | Imidazole, DMAP, Et₃N |
| Solvent | DMF, CH₂Cl₂ |
| Conditions | RT, 2-12 h (Cl); 0°C to RT, 0.5-2 h (OTf) |
| Deprotection | TBAF (THF), HF·pyridine, AcOH/H₂O, HF |
| Stability | Good for multi-step sequences |

**Selectivity:**
- TBDMSCl/imidazole/DMF: Primary > secondary (kinetic control)
- Can protect primary in presence of secondary

**Formation:**
```
ROH + TBDMSCl + imidazole (DMF) → ROTBDMS
ROH + TBDMSOTf + 2,6-lutidine (CH₂Cl₂, 0°C) → ROTBDMS (faster, milder)
```

**Deprotection:**
```
ROTBDMS + TBAF (THF) → ROH + TBDMSF + TBA⁺
ROTBDMS + HF·pyridine → ROH + TBDMSF
ROTBDMS + AcOH/H₂O (4:1, 35°C) → ROH (mild, selective)
```

#### tert-Butyldiphenylsilyl (TBDPS)

| Property | Details |
|----------|---------|
| Reagent | TBDPSCl, TBDPSOTf |
| Base | Imidazole, DMAP, pyridine |
| Solvent | DMF, CH₂Cl₂ |
| Conditions | RT, 2-24 h |
| Deprotection | TBAF (slower than TBDMS), HF·pyridine |
| Stability | Excellent — more stable than TBDMS to acid/base |
| Selectivity | Highest for primary alcohols |

**Advantages over TBDMS:**
- More stable to acidic and basic conditions
- More crystalline products (better purification)
- Greater selectivity for primary alcohols

**Deprotection Rate:**
```
TBDPS is ~10× slower to TBAF than TBDMS
Useful for orthogonal: TBDMS removed, TBDPS survives
```

#### Triisopropylsilyl (TIPS)

| Property | Details |
|----------|---------|
| Reagent | TIPSCl, TIPSOTf |
| Base | Imidazole, 2,6-lutidine |
| Solvent | DMF, CH₂Cl₂ |
| Conditions | RT or reflux, 4-24 h (slow) |
| Deprotection | TBAF (slow), HF·pyridine |
| Stability | Excellent — very bulky, very stable |
| Selectivity | Highest — primary alcohols only under normal conditions |

**Use Cases:**
- When TBDPS stability is insufficient
- Protection of primary alcohols in presence of secondary/tertiary
- Longest synthetic sequences

### 2.2 Acetals and Ketals

**General:** Cyclic protecting groups formed from diols and aldehydes/ketones.

#### Acetonide (Isopropylidene)

| Property | Details |
|----------|---------|
| Reagent | Acetone, 2,2-dimethoxypropane (DMP) |
| Catalyst | p-TsOH, CSA, PPTS (acid) |
| Solvent | Acetone, CH₂Cl₂, DMF |
| Conditions | RT, 2-12 h |
| Deprotection | Acidic hydrolysis (aq. HCl, AcOH/H₂O) |
| Stability | Stable to base, moderate acid |

**Formation Mechanism:**
```
1,2- or 1,3-diol + (CH₃)₂C(OMe)₂ + H⁺ → cyclic acetal + 2 MeOH
```

**Regioselectivity:**
- 1,2-diols → 5-membered ring (kinetically favored)
- 1,3-diols → 6-membered ring (thermodynamically favored)
- Cis-diols react faster than trans

**Special Cases:**
- Carbohydrates: 4,6-O-benzylidene, 4,6-O-isopropylidene common
- Cyclic acetals can direct stereochemistry in subsequent reactions

#### Benzylidene Acetal

| Property | Details |
|----------|---------|
| Reagent | Benzaldehyde dimethyl acetal, PhCHO/Bronsted acid |
| Catalyst | CSA, p-TsOH, TMSOTf |
| Solvent | CH₂Cl₂, DMF |
| Conditions | RT, 2-24 h |
| Deprotection | Acidic hydrolysis, hydrogenolysis (benzylic C-O cleavage) |
| Special | Can be regioselectively opened to give mono-Bn ether |

**Regioselective Opening:**
```
Benzylidene + NaCNBH₃/HCl → 6-O-Bn (for pyranosides)
Benzylidene + DIBAL-H → 4-O-Bn (alternative regioselectivity)
```

### 2.3 Ethers

#### Benzyl (Bn)

| Property | Details |
|----------|---------|
| Reagent | BnBr, BnCl |
| Base | NaH, KH, NaOH (phase transfer) |
| Solvent | DMF, THF, DMSO |
| Conditions | 0°C to RT, 2-12 h |
| Deprotection | H₂/Pd-C, H₂/Pd(OH)₂ (Pearlman's), Birch reduction |
| Stability | Excellent to acid, base, mild oxidants |

**Formation (Williamson Ether Synthesis):**
```
ROH + NaH → RO⁻Na⁺ + H₂
RO⁻Na⁺ + BnBr → ROBn + NaBr
```

**Alternative Conditions:**
- Ag₂O/BnBr (for hindered alcohols)
- NaOH/BnBr/Bu₄N⁺I⁻ (phase transfer, aqueous)

**Deprotection Methods:**
```
1. H₂, Pd-C (10%), EtOH or EtOAc, RT, 1-12 h
   — Most common, mild

2. H₂, Pd(OH)₂/C (Pearlman's catalyst)
   — Faster, often used for sensitive substrates

3. Birch: Na, NH₃(l), t-BuOH
   — Dissolving metal reduction, for acid-sensitive substrates

4. Lewis acid: BCl₃, BBr₃ (CH₂Cl₂, -78°C)
   — For substrates incompatible with hydrogenation
```

**Cautions:**
- Bn is hydrogenolyzed; other reducible groups (alkenes, nitro, Cbz) affected
- Bn migration under acidic conditions possible

#### p-Methoxybenzyl (PMB)

| Property | Details |
|----------|---------|
| Reagent | PMBCl, PMBBr, PMBtrichloroacetimidate |
| Base | NaH, i-Pr₂NEt |
| Solvent | DMF, CH₂Cl₂ |
| Conditions | RT, 2-12 h |
| Deprotection | DDQ, CAN, H₂/Pd-C, TFA |
| Stability | Similar to Bn, but acid-labile (p-methoxy) |

**Selective Deprotection:**
```
PMB can be removed in presence of Bn using:
- DDQ (CH₂Cl₂/H₂O): PMB removed, Bn stable
- CAN (MeCN/H₂O): PMB removed, Bn stable
- TFA (mild acid): PMB removed slowly, Bn stable

PMB and Bn both removed by H₂/Pd-C
```

**Formation via Trichloroacetimidate:**
```
ROH + PMB-N=C(OH)CCl₃ + cat. TFA → RO-PMB + Cl₃CCONH₂
```

#### Methoxymethyl (MOM)

| Property | Details |
|----------|---------|
| Reagent | MOMCl (chloromethyl methyl ether), MOMBr |
| Base | i-Pr₂NEt (DIPEA), NaH |
| Solvent | CH₂Cl₂, THF |
| Conditions | 0°C to RT, 1-4 h |
| Deprotection | Lewis acid (TMSBr, BBr₃), strong acid (HCl, H₂SO₄) |
| Stability | Good to base, moderate to acid |

**Caution:** MOMCl is a known carcinogen (bis(chloromethyl)ether impurity). Handle with care.

**Alternative Reagents:**
- Dimethoxymethane + P₂O₅ (safer)
- MOM-trichloroacetimidate + TFA

#### 2-Methoxyethoxymethyl (MEM)

| Property | Details |
|----------|---------|
| Reagent | MEMCl |
| Base | i-Pr₂NEt |
| Solvent | CH₂Cl₂ |
| Conditions | 0°C to RT, 1-4 h |
| Deprotection | Lewis acids (TiCl₄, ZnBr₂), strong acid |
| Stability | More stable than MOM to acid |
| Special | Chelates to Lewis acids (useful for directing groups) |

#### Tetrahydropyranyl (THP)

| Property | Details |
|----------|---------|
| Reagent | DHP (dihydropyran) |
| Catalyst | p-TsOH, PPTS, CSA |
| Solvent | CH₂Cl₂, Et₂O |
| Conditions | RT, 0.5-4 h |
| Deprotection | Mild acid (AcOH/H₂O, MeOH/PPTS) |
| Stability | Good to base, labile to mild acid |

**Advantages:**
- Very easy introduction (one-step, catalytic)
- Good for temporary protection

**Disadvantages:**
- Creates a new stereocenter (mixture of diastereomers for chiral alcohols)
- Can complicate NMR analysis

**Formation:**
```
ROH + DHP + H⁺ → RO-THP (mixture of anomers)
```

#### Trityl (Tr, Triphenylmethyl)

| Property | Details |
|----------|---------|
| Reagent | TrCl (triphenylmethyl chloride), TrOTf |
| Base | Pyridine, Et₃N, DMAP |
| Solvent | CH₂Cl₂, pyridine |
| Conditions | RT, 1-6 h |
| Deprotection | Very mild acid (AcOH, pH 4-5), hydrogenolysis |
| Stability | Very acid-labile, base-stable |
| Selectivity | Primary alcohols only (bulky) |

**Use Cases:**
- Selective primary alcohol protection
- When extremely mild acid deprotection needed
- Carbohydrate synthesis (primary OH protection)

**Deprotection Mechanism:**
```
RO-Tr + H⁺ → ROH + Tr⁺ (stable triphenylmethyl cation)
Tr⁺ (purple/violet color)
```

### 2.4 Esters

#### Acetate (Ac)

| Property | Details |
|----------|---------|
| Reagent | Ac₂O, AcCl, Ac imidazole, acetic anhydride |
| Base | Pyridine, Et₃N, DMAP (catalytic) |
| Solvent | CH₂Cl₂, pyridine, THF |
| Conditions | 0°C to RT, 0.5-2 h |
| Deprotection | Base: K₂CO₃/MeOH, NH₃/MeOH, LiOH/THF-H₂O |
| Stability | Good to acid, labile to base |

**Formation:**
```
ROH + Ac₂O + DMAP (cat.) + Et₃N → ROAc + AcO⁻ + Et₃NH⁺
```

**Deprotection:**
```
ROAc + K₂CO₃/MeOH → ROH + KOAc + MeOH
ROAc + NH₃/MeOH → ROH + NH₄OAc
ROAc + LiOH/THF-H₂O → ROH + LiOAc
```

**Selectivity:**
- Primary > secondary > tertiary (kinetic)
- Can be enzymatically selective (lipases, esterases)

#### Benzoate (Bz)

| Property | Details |
|----------|---------|
| Reagent | BzCl, Bz₂O |
| Base | Pyridine, Et₃N, DMAP |
| Solvent | CH₂Cl₂, pyridine |
| Conditions | 0°C to RT, 0.5-4 h |
| Deprotection | Base (stronger than acetate) |
| Stability | More stable to base than Ac, same acid stability |

**Deprotection:**
```
ROBz + NaOH/MeOH-H₂O → ROH + NaOBz
ROBz + K₂CO₃/MeOH (reflux) → ROH
```

**Advantages over Acetate:**
- More crystalline (easier purification)
- UV active (detection)
- Slightly more stable (allows differential deprotection)

#### Pivaloate (Piv)

| Property | Details |
|----------|---------|
| Reagent | PivCl, Piv₂O |
| Base | Pyridine, DMAP |
| Solvent | CH₂Cl₂ |
| Conditions | RT, 2-12 h |
| Deprotection | Strong base (NaOH, KOH), LiAlH₄ |
| Stability | Most base-stable common ester |

**Special Properties:**
- Bulky — slower acylation, higher selectivity for less hindered OH
- Very stable to base (requires harsh conditions for deprotection)
- Cannot migrate (unlike acetate)

### 2.5 Carbonates

#### tert-Butyl Carbonate (Boc)

| Property | Details |
|----------|---------|
| Reagent | Boc₂O (di-tert-butyl dicarbonate) |
| Base | DMAP, Et₃N |
| Solvent | CH₂Cl₂, THF |
| Conditions | RT, 2-12 h |
| Deprotection | Acid: TFA, HCl/dioxane |
| Stability | Base-stable, acid-labile |

**Formation:**
```
ROH + Boc₂O + DMAP → RO-C(O)O-t-Bu + t-BuOCO₂⁻
```

**Deprotection:**
```
RO-C(O)O-t-Bu + TFA → ROH + CO₂ + t-Bu⁺ (isobutylene)
```

**Comparison to Amino-Boc:**
- Alcohol Boc less commonly used
- Similar acid lability to amine Boc

#### Benzyloxycarbonyl (Cbz)

| Property | Details |
|----------|---------|
| Reagent | CbzCl (benzyl chloroformate) |
| Base | Pyridine, NaHCO₃ |
| Solvent | CH₂Cl₂, THF-H₂O (biphasic) |
| Conditions | 0°C to RT, 1-4 h |
| Deprotection | Hydrogenolysis: H₂/Pd-C |
| Stability | Acid-stable, base-stable |

**Deprotection:**
```
RO-C(O)O-CH₂Ph + H₂/Pd-C → ROH + CO₂ + toluene
```

---

## 3. Amine Protection

### 3.1 Carbamates

**General Structure:** R-NH-C(O)-OR'

Carbamates balance stability and deprotection convenience, making them the most widely used amine protecting groups.

#### tert-Butoxycarbonyl (Boc)

| Property | Details |
|----------|---------|
| Reagent | Boc₂O (di-tert-butyl dicarbonate) |
| Base | Et₃N, DMAP, NaHCO₃ (aq) |
| Solvent | CH₂Cl₂, THF, dioxane, H₂O/organic |
| Conditions | RT, 1-12 h |
| Deprotection | TFA (neat or in CH₂Cl₂), HCl/dioxane, HCl/EtOAc |
| Stability | Base-stable, acid-labile |

**Formation:**
```
RNH₂ + Boc₂O + Et₃N → RNHBoc + Et₃NH⁺ + t-BuOCO₂⁻
RNH₂ + Boc₂O + NaOH/NaHCO₃ (aq) → RNHBoc (biphasic)
```

**Deprotection:**
```
RNHBoc + TFA (neat or CH₂Cl₂) → RNH₃⁺TFA⁻ + CO₂ + isobutylene
RNHBoc + HCl/dioxane → RNH₃⁺Cl⁻ + CO₂ + isobutylene

Neutralization: RNH₃⁺ + NaHCO₃ → RNH₂ + CO₂ + H₂O + Na⁺
```

**Typical Conditions:**
- TFA/CH₂Cl₂ (1:1 to 9:1), 0.5-2 h, RT
- HCl (4M) in dioxane, 1-4 h, RT
- TFA with scavengers (Et₃SiH, H₂O) to trap carbocations

**Advantages:**
- Easy introduction and removal
- Base-stable (compatible with many reactions)
- Volatile byproducts (easy workup)
- Crystalline products often obtained

**Disadvantages:**
- Acid-labile (incompatible with strong acid conditions)
- t-Butyl cation can cause side reactions (use scavengers)

#### Benzyloxycarbonyl (Cbz, Z)

| Property | Details |
|----------|---------|
| Reagent | CbzCl (benzyl chloroformate) |
| Base | NaHCO₃, NaOH (aqueous), NaOH/Schotten-Baumann |
| Solvent | CH₂Cl₂/H₂O (biphasic), THF/H₂O |
| Conditions | 0°C, 1-4 h (exothermic) |
| Deprotection | Hydrogenolysis: H₂/Pd-C, H₂/Pd(OH)₂ |
| Stability | Acid-stable, base-stable |

**Formation:**
```
RNH₂ + CbzCl + 2 NaOH (aq) → RNHCbz + NaCl + H₂O + NaHCO₃
(biphasic: organic phase + aqueous NaOH, 0°C)
```

**Deprotection:**
```
RNHCbz + H₂ (1 atm) + Pd-C → RNH₂ + CO₂ + toluene

Conditions: MeOH, EtOH, or EtOAc, RT, 1-12 h
```

**Advantages:**
- Very stable to acid and base
- Compatible with Boc (orthogonal: Boc removed by acid, Cbz by H₂)
- Mild deprotection

**Disadvantages:**
- Hydrogenation conditions may affect other groups
- Over-reduction possible (especially with other reducible groups)
- CbzCl is lachrymator and moisture-sensitive

#### 9-Fluorenylmethyloxycarbonyl (Fmoc)

| Property | Details |
|----------|---------|
| Reagent | Fmoc-Cl, Fmoc-OSu (active ester) |
| Base | Na₂CO₃, NaHCO₃ (aqueous), NaOH |
| Solvent | Dioxane/H₂O, THF/H₂O, CH₂Cl₂ |
| Conditions | 0°C to RT, 1-4 h |
| Deprotection | Base: piperidine (20% in DMF), DBU, morpholine |
| Stability | Acid-stable, base-labile |

**Formation:**
```
RNH₂ + Fmoc-OSu + NaHCO₃ → R-NH-Fmoc + HOsu + Na⁺
(Fmoc-OSu preferred: less epimerization)
```

**Deprotection Mechanism:**
```
1. Base abstracts acidic fluorene proton (pKa ~23)
2. Elimination yields dibenzofulvene (DBF)
3. DBF trapped by amine (piperidine) to give adduct

R-NH-Fmoc + piperidine → RNH₂ + DBF-piperidine adduct
```

**Deprotection Conditions:**
- 20-25% piperidine in DMF, RT, 10-30 min
- 2% DBU in CH₂Cl₂ (faster)
- Alternative: morpholine, diethylamine

**Advantages:**
- Orthogonal to Boc (acid-labile) and Cbz (H₂)
- UV active (detection and monitoring)
- Deprotection monitored by DBF absorption (300 nm)

**Disadvantages:**
- Base-labile (incompatible with strong bases)
- DBF can react with nucleophiles (must be scavenged)
- Expensive reagents

**Primary Use:** Solid-phase peptide synthesis (SPPS) with Fmoc/t-Bu strategy

#### Allyloxycarbonyl (Alloc)

| Property | Details |
|----------|---------|
| Reagent | Alloc-Cl (allyl chloroformate) |
| Base | Pyridine, NaHCO₃ |
| Solvent | CH₂Cl₂, THF/H₂O |
| Conditions | 0°C to RT, 1-4 h |
| Deprotection | Pd(0) catalyzed: Pd(PPh₃)₄, dimedone or morpholine as scavenger |
| Stability | Acid-stable, base-stable, H₂-stable (Pd poison) |

**Deprotection Mechanism:**
```
R-NH-Alloc + Pd(0) → π-allyl-Pd complex + RNH⁻
π-allyl-Pd complex + scavenger (nucleophile) → allyl scavenger + Pd(0)

Typical scavengers: dimedone, morpholine, phenylsilane
```

**Conditions:**
```
R-NH-Alloc + Pd(PPh₃)₄ (0.1 eq) + PhSiH₃ (2 eq) in THF, RT, 1-2 h
→ RNH₂ + propene + PhSiH₂OH
```

**Advantages:**
- Orthogonal to Boc, Cbz, Fmoc
- Compatible with acid and base
- Very selective deprotection

**Uses:**
- Peptide synthesis (orthogonal protection)
- Complex molecule synthesis (multiple orthogonal groups)

### 3.2 Amides

**General:** R-NH-C(O)-R'

Amides are very stable protecting groups, requiring harsh conditions for removal. Use when extreme stability is needed.

#### Acetamide (Ac)

| Property | Details |
|----------|---------|
| Reagent | Ac₂O, AcCl, Ac imidazole |
| Base | Pyridine, Et₃N |
| Solvent | CH₂Cl₂, pyridine |
| Conditions | RT, 1-12 h |
| Deprotection | Harsh: 6N HCl reflux, KOH/EtOH reflux, hydrazine |
| Stability | Very stable to most conditions |

**Deprotection:**
```
R-NH-Ac + 6N HCl (reflux) → RNH₃⁺Cl⁻ + AcOH
R-NH-Ac + KOH/EtOH (reflux) → RNH₂ + AcO⁻
R-NH-Ac + NH₂NH₂ (hydrazine) → RNH₂ + AcNHNH₂
```

**Use Cases:**
- When maximum stability needed
- Rare in modern synthesis (too harsh deprotection)

#### Trifluoroacetamide (TFA)

| Property | Details |
|----------|---------|
| Reagent | TFAA (trifluoroacetic anhydride) |
| Base | Pyridine, Et₃N |
| Solvent | CH₂Cl₂ |
| Conditions | 0°C to RT, 0.5-2 h |
| Deprotection | Mild base: K₂CO₃/MeOH, NH₃/MeOH |
| Stability | Moderate (less than acetamide) |

**Advantages:**
- Electron-withdrawing CF₃ makes carbonyl more electrophilic
- Easier deprotection than acetamide
- Can be deprotected under mild conditions

### 3.3 Sulfonamides

**General:** R-NH-SO₂-Ar or R-NH-SO₂-R'

Sulfonamides are very stable and often used for permanent protection or as activating groups.

#### Tosyl (Ts, p-Toluenesulfonyl)

| Property | Details |
|----------|---------|
| Reagent | TsCl (tosyl chloride) |
| Base | Pyridine, NaOH (aqueous) |
| Solvent | CH₂Cl₂, pyridine, H₂O/organic |
| Conditions | 0°C to RT, 2-12 h |
| Deprotection | Very harsh: Na/liq NH₃, HBr/AcOH reflux, Mg/MeOH |
| Stability | Excellent to acid, base, mild reductants |

**Formation:**
```
RNH₂ + TsCl + 2 pyridine → RNHTs + pyridinium chloride
```

**Deprotection:**
```
RNHTs + Na/NH₃(l) → RNH₂ + ArSO₂Na (Birch-like)
RNHTs + HBr/AcOH (reflux) → RNH₃⁺Br⁻ + TsOH
RNHTs + Mg/MeOH → RNH₂ (reductive)
```

**Uses:**
- Permanent protection in synthesis
- Activating group for nucleophilic substitution (amine to leaving group)
- Gabriel synthesis (phthalimide is related)

#### Nosyl (Ns, 2-Nitrobenzenesulfonyl)

| Property | Details |
|----------|---------|
| Reagent | NsCl (2-nitrobenzenesulfonyl chloride) |
| Base | Pyridine, Et₃N |
| Solvent | CH₂Cl₂ |
| Conditions | 0°C to RT, 1-4 h |
| Deprotection | Thiophenol/K₂CO₃, mercaptoethanol/base |
| Stability | Good, but deprotectable under mild conditions |

**Key Feature: Deprotection via Smiles Rearrangement**
```
RNH-Ns + PhS⁻ → [RS⁻ attacks NO₂, rearrangement] → RNH₂ + ArSO₂SPh
```

**Conditions:**
```
RNH-Ns + PhSH + K₂CO₃ (DMF) → RNH₂ + other products
```

**Advantages over Ts:**
- Much easier deprotection
- Orthogonal to Ts
- Used in Fukuyama amine synthesis

### 3.4 Imines

**General:** R-N=CR'R''

Imines are formed from amines and aldehydes/ketones. They are useful for temporary protection and can direct reactions.

#### Benzylidene Imine

| Property | Details |
|----------|---------|
| Reagent | Benzaldehyde |
| Conditions | Dean-Stark (remove H₂O), molecular sieves |
| Deprotection | Acidic hydrolysis (aq. HCl) |
| Stability | Moderate (can hydrolyze during workup) |

**Formation:**
```
RNH₂ + PhCHO → R-N=CHPh + H₂O (remove water)
```

**Use Cases:**
- Temporary protection (amine as imine)
- Directing group for ortho-lithiation
- Amine activation for certain reactions

### 3.5 N-Alkyl

**General:** R-NH-R'

Alkylation of amines gives very stable protection, but removal is difficult.

#### Benzyl (Bn)

| Property | Details |
|----------|---------|
| Reagent | BnBr, BnCl (alkylation) or reductive amination |
| Base | NaHCO₃, NaBH₃CN (reductive amination) |
| Deprotection | Hydrogenolysis: H₂/Pd-C; Birch: Na/NH₃ |

**Formation:**
```
RNH₂ + PhCHO + NaBH₃CN → R-NH-CH₂Ph (reductive amination)
```

**Deprotection:**
```
R-NH-CH₂Ph + H₂/Pd-C → RNH₂ + toluene
(Secondary amine product, may need further dealkylation)
```

**Note:** N-Benzyl is more difficult to remove than O-benzyl. Complete dealkylation to primary amine may require multiple hydrogenolysis cycles or Birch reduction.

---

## 4. Carbonyl Protection

### 4.1 Acetals and Ketals

**General Structure:**
- Acetal: R₂C(OR')₂ (from aldehyde)
- Ketal: R₂C(OR')₂ (from ketone)

Acetals/ketals are stable to base but labile to acid. They are the most common carbonyl protecting groups.

#### Dimethyl Acetal/Ketal

| Property | Details |
|----------|---------|
| Reagent | MeOH + acid (or Me₂C(OMe)₂) |
| Catalyst | p-TsOH, CSA, TMSOTf |
| Conditions | Dean-Stark (remove H₂O), molecular sieves |
| Deprotection | Aqueous acid (HCl, AcOH/H₂O) |
| Stability | Good to base, acid-labile |

**Formation:**
```
RCHO + 2 MeOH + H⁺ (cat.) → RCH(OMe)₂ + H₂O
R₂C=O + Me₂C(OMe)₂ + H⁺ → R₂C(OMe)₂ + acetone
```

**Deprotection:**
```
RCH(OMe)₂ + H₂O/H⁺ → RCHO + 2 MeOH
```

#### Ethylene Acetal/Ketal (1,3-Dioxolane)

| Property | Details |
|----------|---------|
| Reagent | Ethylene glycol |
| Catalyst | p-TsOH, CSA, PPTS |
| Conditions | Dean-Stark (remove H₂O), molecular sieves, toluene reflux |
| Deprotection | Aqueous acid (AcOH/H₂O, acetone/H₃O⁺) |
| Stability | Good to base, moderate acid |

**Formation:**
```
R₂C=O + HOCH₂CH₂OH + H⁺ (cat.) → R₂C(OCH₂)₂ + H₂O
```

**Advantages:**
- Cyclic acetal is more stable than acyclic
- Ethylene glycol is cheap
- Common protecting group in synthesis

**Regioselectivity Issues:**
- Unsymmetrical ketones can give mixtures
- However, for most ketones, single product forms

**Use in Synthesis:**
- Protects carbonyl during Grignard, Wittig, other reactions
- Acetal carbon is prochiral — can direct stereochemistry

#### 1,3-Dioxane (from 1,3-Propanediol)

| Property | Details |
|----------|---------|
| Reagent | 1,3-Propanediol |
| Catalyst | p-TsOH |
| Stability | Similar to dioxolane, slightly more stable |

**Difference from Dioxolane:**
- 6-membered ring (vs 5-membered)
- Slightly more stable to acid
- Different conformational preferences

### 4.2 Dithianes

**General Structure:** R₂C(SR')₂ — sulfur analogs of acetals

**Key Property:** Acid-stable, deprotected by mercuric or alkylating agents

#### 1,3-Dithiane

| Property | Details |
|----------|---------|
| Reagent | 1,3-Propanedithiol |
| Catalyst | BF₃·Et₂O, TMSOTf |
| Conditions | CH₂Cl₂, 0°C to RT, 2-12 h |
| Deprotection | Hg(II) salts, NCS, NBS, iodine oxidants |
| Stability | Acid-stable, base-stable |

**Formation:**
```
R₂C=O + HS(CH₂)₃SH + H⁺ → R₂C(S(CH₂)₃) + H₂O
```

**Deprotection Methods:**

1. **Mercury(II) Method:**
```
R₂C(SR)₂ + HgCl₂ + H₂O → R₂C=O + 2 RSHgCl
HgO + 2 HCl → HgCl₂ + H₂O (regeneration)
```

2. **N-Halosuccinimide:**
```
R₂C(SR)₂ + NCS + H₂O → R₂C=O + RSSR + succinimide
```

3. **Iodine Oxidation:**
```
R₂C(SR)₂ + I₂ + H₂O → R₂C=O + 2 RI + 2 HI
```

**Special Use: Umpolung (Corey-Seebach Reaction)**

The dithiane group allows reversal of carbonyl polarity:
```
Normal: RCHO → R⁻ (α-carbon) + CHO⁺ (carbonyl)
Umpolung: Dithiane → R-CH(SR)₂-Li → R⁻-CH-SR₂ (nucleophilic carbonyl equivalent)

R-CH(SR)₂-Li + R'-X → R-CH(R')(SR)₂ → deprotect → R-CH(R')-CHO
```

**Advantages:**
- Acid-stable (unlike acetals)
- Allows umpolung chemistry
- Stable to many reaction conditions

**Disadvantages:**
- Mercaptan odor
- Heavy metal deprotection (environmental concern)
- Sulfur can poison Pd catalysts

### 4.3 Oximes

**General Structure:** R₂C=N-OH

Oximes are derivatives of carbonyls with hydroxylamine. They are relatively stable and have unique properties.

| Property | Details |
|----------|---------|
| Reagent | NH₂OH·HCl (hydroxylamine hydrochloride) |
| Base | NaOAc, pyridine, NaOH |
| Solvent | EtOH, pyridine, H₂O/organic |
| Conditions | RT to reflux, 1-12 h |
| Deprotection | Hydrolysis (acidic), reduction, oxidation |

**Formation:**
```
R₂C=O + NH₂OH·HCl + base → R₂C=NOH + H₂O + base·HCl
```

**Deprotection Methods:**

1. **Acidic Hydrolysis:**
```
R₂C=NOH + H₃O⁺ → R₂C=O + NH₂OH
```

2. **Reductive Cleavage:**
```
R₂C=NOH + TiCl₃ or Zn/AcOH → R₂C=O + NH₃
```

3. **Oxidative Cleavage:**
```
R₂C=NOH + [O] → R₂C=O + NO₂⁻ or other N-products
```

**Special Properties:**
- E/Z isomerism (syn/anti)
- Can be reduced to primary amines: R₂C=NOH → R₂CH-NH₂
- Beckmann rearrangement: R₂C=NOH → R-C(=O)-NHR (with acid)

### 4.4 Hydrazones

**General Structure:** R₂C=N-NR'₂

Hydrazones are formed from hydrazines and carbonyls. They are used for protection, but also have special applications.

| Property | Details |
|----------|---------|
| Reagent | NH₂NH₂ (hydrazine), PhNHNH₂ (phenylhydrazine) |
| Solvent | EtOH, AcOH |
| Conditions | RT to reflux, 0.5-4 h |
| Deprotection | Hydrolysis (acidic), oxidative, reductive |

**Formation:**
```
R₂C=O + NH₂NH₂ → R₂C=N-NH₂ + H₂O
```

**Deprotection Methods:**

1. **Acidic Hydrolysis:**
```
R₂C=N-NH₂ + H₃O⁺ → R₂C=O + NH₂NH₂
```

2. **Oxidative (with Cu(II)):**
```
R₂C=N-NH₂ + Cu(II) → R₂C=O + N₂ + Cu(I)
```

**Special Uses:**

1. **Shapiro Reaction (tosylhydrazones):**
```
R₂C=N-NHTs + 2 R'Li → R'₂N-N(Ts)Li + R-CHLi-R
R-CHLi-R + electrophile → alkene after elimination
```

2. **Wolff-Kishner Reduction:**
```
R₂C=O → hydrazone → heat/base → R₂CH₂ (reduction to alkane)
```

---

## 5. Carboxylic Acid Protection

### 5.1 Esters

**General:** R-CO₂R'

Esters are the most common carboxylic acid protecting groups, with varying stability based on the alcohol component.

#### Methyl Ester

| Property | Details |
|----------|---------|
| Formation | CH₂N₂ (diazomethane), MeOH + DCC, MeI + Ag₂O |
| Conditions | RT, minutes (CH₂N₂) or reflux (MeOH/DCC) |
| Deprotection | LiOH/THF-H₂O, NaOH/MeOH, BBr₃ |
| Stability | Moderate base stability |

**Formation Methods:**

1. **Diazomethane (most common):**
```
RCOOH + CH₂N₂ → RCOOMe + N₂ (RT, minutes)
CAUTION: CH₂N₂ is toxic and explosive
```

2. **Fischer Esterification:**
```
RCOOH + MeOH + H⁺ (cat., reflux) → RCOOMe + H₂O
Equilibrium — use Dean-Stark or excess MeOH
```

3. **DCC Coupling:**
```
RCOOH + MeOH + DCC → RCOOMe + DCU (dicyclohexylurea)
```

**Deprotection:**
```
RCOOMe + LiOH/THF-H₂O → RCOOLi + MeOH
```

#### Ethyl Ester

| Property | Details |
|----------|---------|
| Formation | EtOH + DCC, EtOH + H⁺ (reflux) |
| Deprotection | LiOH/THF-H₂O, NaOH/EtOH-H₂O |
| Stability | Similar to methyl |

**Advantage over Me:** Slightly more stable to base; useful when methyl esters hydrolyze too quickly.

#### tert-Butyl Ester

| Property | Details |
|----------|---------|
| Formation | Isobutylene + H⁺, Boc₂O + DMAP, t-BuOH + DCC |
| Deprotection | TFA, HCl/dioxane |
| Stability | Base-stable, acid-labile |

**Formation:**
```
RCOOH + isobutylene + H₂SO₄ (cat.) → RCOO-t-Bu
RCOOH + Boc₂O + DMAP → RCOO-t-Bu + CO₂
```

**Deprotection:**
```
RCOO-t-Bu + TFA → RCOOH + isobutylene + CO₂
```

**Advantages:**
- Orthogonal to methyl/ethyl esters (acid-labile vs base-labile)
- Compatible with strong bases
- Volatile byproducts (easy workup)

**Uses:**
- Peptide synthesis (side-chain protection for Asp, Glu)
- Base-sensitive molecules

#### Benzyl Ester

| Property | Details |
|----------|---------|
| Formation | BnBr + base (Ag₂O, Cs₂CO₃), DCC/BnOH |
| Deprotection | H₂/Pd-C, HBr/AcOH, Na/liq NH₃ |
| Stability | Good to acid, base; labile to hydrogenolysis |

**Formation:**
```
RCOO⁻ + BnBr + Cs₂CO₃ → RCOOBn + CsBr + CsHCO₃
```

**Deprotection:**
```
RCOOBn + H₂/Pd-C → RCOOH + toluene
```

**Advantages:**
- Orthogonal to t-Bu (hydrogenolysis vs acid)
- Used in peptide synthesis (Cbz/Bn strategy)

#### Allyl Ester

| Property | Details |
|----------|---------|
| Formation | Allyl bromide + base, allyl alcohol + DCC |
| Deprotection | Pd(0) catalyzed (Pd(PPh₃)₄ + nucleophile) |
| Stability | Acid-stable, base-stable |

**Deprotection (similar to Alloc):**
```
RCOO-allyl + Pd(0) + nucleophile → RCOOH + allyl-nucleophile
Nucleophiles: dimedone, morpholine, PhSiH₃
```

**Advantages:**
- Orthogonal to most other esters
- Mild deprotection
- Compatible with acid and base

#### Silyl Esters

| Property | Details |
|----------|---------|
| Formation | RCOOH + R₃SiCl + base |
| Examples | TMS ester, TES ester, TBS ester |
| Deprotection | Aqueous workup (TMS), fluoride, mild acid |
| Stability | TMS very labile, TBS more stable |

**Use Cases:**
- Temporary protection (TMS)
- When volatility is needed
- Mass spectrometry derivatization

### 5.2 Orthoesters

**General Structure:** RC(OR')₃

Orthoesters are more stable than esters and useful for specific applications.

| Property | Details |
|----------|---------|
| Formation | RCOOR' + R'OH + acid, or from nitrile |
| Deprotection | Acidic hydrolysis (stepwise: orthoester → ester → acid) |
| Stability | More stable to base than esters |

**Special Use:**
- Protects acid while being stable to many conditions
- Can serve as esterification reagent
- Used in carbohydrate chemistry

### 5.3 Amides

**General:** R-CO-NR'₂

Amides are the most stable carboxylic acid derivatives, requiring harsh conditions for hydrolysis.

| Property | Details |
|----------|---------|
| Formation | RCOCl + amine, or coupling reagents |
| Deprotection | Harsh: 6N HCl reflux, NaOH fusion |
| Stability | Very stable to most conditions |

**Use Cases:**
- Permanent protection
- When extreme stability needed
- Not commonly used for protection (too harsh deprotection)

**Exception:** Weinreb amide (R-CO-N(OMe)Me)
- Used as acylating agent, not typically for protection
- Reacts with Grignards to give ketones

---

## 6. Phosphate Protection

Phosphate protecting groups are essential in oligonucleotide synthesis. The phosphorus center can be protected at multiple positions.

### 6.1 Phosphoramidites

**General Structure:** (RO)₂P-NR'₂

Phosphoramidites are the standard building blocks for solid-phase oligonucleotide synthesis.

| Property | Details |
|----------|---------|
| P(III) oxidation state | Reactive toward coupling |
| Protecting groups | DMTr (4,4'-dimethoxytrityl) on 5'-OH |
| Base protection | Bz, ib (isobutyryl) for exocyclic amines |
| Coupling activator | Tetrazole, 5-ethylthio-1H-tetrazole (ETT) |

**Standard Phosphoramidite Building Blocks:**

```
5'-O-DMTr-nucleoside-3'-O-(2-cyanoethyl-N,N-diisopropylphosphoramidite)

Where:
- DMTr: acid-labile 5'-protection (removed each cycle)
- Cyanoethyl: phosphate protection (removed at end with base)
- Diisopropylamine: leaving group in coupling
```

**Coupling Cycle:**
```
1. Deprotection: DMTr removed with 3% TCA or DCA (dichloroacetic acid)
2. Coupling: Phosphoramidite + tetrazole → phosphite triester
3. Oxidation: I₂/H₂O/pyridine → phosphate triester
4. Capping: Ac₂O + NMI → caps unreacted 5'-OH
5. Repeat
```

### 6.2 Phosphotriesters

**General Structure:** (RO)₃P=O

Phosphate triesters are protected phosphates, used in both synthesis and as final prodrugs.

#### 2-Cyanoethyl

| Property | Details |
|----------|---------|
| Removal | β-elimination with base (DBU, NH₃) |
| Stability | Stable to acid, base-labile |
| Use | Standard in phosphoramidite synthesis |

**Deprotection Mechanism:**
```
(RO)₂P(O)-O-CH₂-CH₂-CN + base → 
(RO)₂P(O)O⁻ + CH₂=CH-CN (acrylonitrile)
```

#### Methyl

| Property | Details |
|----------|---------|
| Removal | Thiophenoxide (PhS⁻), strong nucleophiles |
| Stability | Good |
| Use | Alternative to cyanoethyl |

#### Phenyl

| Property | Details |
|----------|---------|
| Removal | Oxidative (I₂, NBS), hydrogenolysis |
| Stability | Good |
| Use | Special applications |

### 6.3 H-Phosphonates

**Alternative Approach:** H-phosphonate method uses P(III) intermediates that are oxidized differently.

```
Nucleoside-H-phosphonate + activator → H-phosphonate diester
Oxidation: Various (I₂, S₈ for phosphorothioates)
```

**Advantages:**
- Different backbone modifications possible
- Phosphorothioates for antisense applications

---

## 7. Orthogonal Protection Schemes

### 7.1 Peptide Synthesis Strategy

#### Fmoc/t-Bu Strategy (Standard SPPS)

**Principle:** Fmoc removed by base (piperidine) each cycle; t-Bu groups stable to base, removed at end with TFA.

```
Orthogonal Set:
- α-Amino: Fmoc (20% piperidine in DMF)
- Side chains: t-Bu or related acid-labile groups
  - Asp, Glu: Ot-Bu (TFA labile)
  - Ser, Thr, Tyr: t-Bu (TFA labile)
  - Lys: Boc (TFA labile)
  - His: Trt (TFA labile)
  - Asn, Gln, Arg, Cys: various acid-labile groups
  - Cys (disulfide): Trt or Acm (orthogonal to TFA)
```

**Deprotection Sequence:**
```
1. Each cycle: Fmoc removed with piperidine (base)
2. Final: TFA removes all t-Bu, Boc, Trt groups
   Side products scavenged (Et₃SiH, H₂O, thiols)
```

**Advantages:**
- Mild deprotection conditions (no strong acid until end)
- Compatible with acid-sensitive modifications
- Side-chain protection stable during synthesis

#### Boc/Bn Strategy (Historical/Merrifield)

**Principle:** Boc removed by TFA each cycle; Bn groups stable to TFA, removed at end with HF.

```
Orthogonal Set:
- α-Amino: Boc (TFA labile)
- Side chains: Bn, Bz (HF or strong acid labile)
  - Asp, Glu: OBn (HF labile)
  - Ser, Thr: Bn (HF labile)
  - Lys: 2-Cl-Z (Cbz with Cl) or Fmoc (orthogonal)
  - Cys: MeBn (HF labile) or Acm
```

**Deprotection Sequence:**
```
1. Each cycle: Boc removed with TFA
2. Final: HF (anhydrous) removes all Bn, Bz groups
   Requires special HF apparatus (dangerous)
```

**Disadvantages:**
- HF is dangerous (requires special equipment)
- Boc removal uses TFA, which can affect some groups
- Largely replaced by Fmoc/t-Bu

### 7.2 Carbohydrate Synthesis

**Challenge:** Carbohydrates have multiple hydroxyl groups with similar reactivity. Selective protection is critical.

**Common Orthogonal Set:**

```
Anomeric position: Various (see below)
2-OH: Participating group (for stereochemistry) or non-participating
3,4,6-OH: Combination of Bn, Bz, TBDMS, etc.

Typical strategy:
1. Per-O-acetylation (protect all OH)
2. Selective anomeric activation (glycosyl donor)
3. Regioselective deprotection
4. Stepwise glycosylation
```

**Anomeric Protecting Groups:**

| Group | Removal | Use |
|-------|---------|-----|
| Ac | Base | Temporary; easily converted to donor |
| Bn | H₂/Pd-C | Stable; non-participating |
| Bz | Base | Participating (gives 1,2-trans) |
| THP | Acid | Temporary; anomeric mixture |
| Tr | Acid | Bulky; primary selective |

**Participating vs Non-Participating:**

```
Participating (esters at C-2): Direct 1,2-trans stereochemistry
  - Ac, Bz, pivaloyl
  - Neighboring group participation from C-2 ester

Non-Participating (ethers at C-2): 1,2-cis possible
  - Bn, TBDMS
  - No neighboring group participation
```

**Example Orthogonal Strategy (Glucose):**

```
Starting: Glucose
1. Per-O-acetylation → Glc(OAc)₅
2. Anomeric activation → trichloroacetimidate donor
3. Regioselective 6-OH deprotection (hydrazine acetate)
4. Protect 6-OH as TBDMS (selective)
5. Glycosylate acceptor
6. Remove TBDMS (TBAF)
7. Further functionalization
```

### 7.3 Multi-Functional Molecules

**Example: Synthesis of a Peptidomimetic with Multiple Functional Groups**

```
Target: Contains amino, hydroxyl, carboxyl, and thiol groups

Strategy:
1. Amino: Boc (acid-labile)
2. Hydroxyl: TBDMS (fluoride-labile)
3. Carboxyl: t-Bu ester (acid-labile, orthogonal to TBDMS)
4. Thiol: Trt (acid-labile, but milder than Boc/t-Bu)
   or Acm (iodine-labile, orthogonal)

Deprotection sequence:
1. Remove TBDMS with TBAF (preserves acid-labile groups)
2. Remove Trt with TFA (mild, preserves t-Bu)
3. Remove Boc and t-Bu with TFA (stronger, longer)
4. Remove Acm with I₂ (if used)

Alternative: 
Use Alloc for amino group — Pd(0) orthogonal deprotection
```

**Example: Amine + Alcohol + Acid**

```
Orthogonal Set:
- Amine: Fmoc (base: piperidine)
- Alcohol: TBDMS (fluoride: TBAF)  
- Acid: Allyl ester (Pd(0) deprotection)

All three are mutually orthogonal.
```

---

## 8. Deprotection Conditions Summary Tables

### 8.1 Acid Deprotection

| Protecting Group | Conditions | Products | Notes |
|-----------------|------------|----------|-------|
| Boc | TFA (neat or CH₂Cl₂), 0.5-2 h | Amine + CO₂ + isobutylene | Add scavengers (Et₃SiH) |
| t-Bu ester | TFA, 1-4 h | Acid + isobutylene | Similar to Boc |
| Tr (trityl) | AcOH/H₂O, pH 4, or TFA (dilute) | Alcohol + trityl cation | Very mild; purple color |
| THP | AcOH/H₂O (4:1), 35-50°C | Alcohol | Mild conditions |
| MOM | 6N HCl, or BBr₃, TMSBr | Alcohol + formaldehyde | Strong acid or Lewis acid |
| PMB | TFA (slow), or DDQ, CAN | Alcohol + aldehyde | DDQ, CAN selective over Bn |
| Boc (alcohol) | TFA | Alcohol + CO₂ | Less common than amine-Boc |
| Acetal/Ketal | Aq. HCl, AcOH/H₂O, PPTS/MeOH | Carbonyl + diol | Equilibrium with water |
| Dithiane | **Stable to acid** | — | Use Hg(II) or NCS instead |

**Acid Stability Ranking (most to least stable):**

```
Bn < PMB < TBDPS < TBDMS < MOM < Tr < THP < Boc < TMS
(most stable)                                    (least stable)
```

### 8.2 Base Deprotection

| Protecting Group | Conditions | Products | Notes |
|-----------------|------------|----------|-------|
| Fmoc | 20% piperidine/DMF, 10-30 min | Amine + DBF adduct | UV monitoring at 300 nm |
| Ac (ester) | K₂CO₃/MeOH, 1-4 h, RT | Alcohol + acetate | Mild |
| Bz (ester) | NaOH/MeOH-H₂O, or K₂CO₃/MeOH reflux | Alcohol + benzoate | Stronger than Ac |
| Piv (ester) | NaOH reflux, or LiAlH₄ | Alcohol | Very stable |
| TFA (amide) | K₂CO₃/MeOH, NH₃/MeOH | Amine | Easier than Ac-amide |
| Cyanoethyl (phosphate) | DBU, NH₃/MeOH | Phosphate + acrylonitrile | β-elimination |
| Fmoc (alcohol) | Piperidine/DMF | Alcohol | Less common |

**Base Stability Ranking (most to least stable):**

```
TBDPS > TBDMS > TIPS > TMS > Bn > MOM > Ac > Bz > Fmoc
(most stable)                                    (least stable)
```

### 8.3 Redox Deprotection

| Protecting Group | Conditions | Products | Notes |
|-----------------|------------|----------|-------|
| Bn (ether) | H₂, Pd-C (10%), EtOH, RT | Alcohol + toluene | Common, mild |
| Bn (ether) | Birch: Na/NH₃(l), t-BuOH | Alcohol + toluene | For H₂-incompatible |
| Bn (N-alkyl) | H₂, Pd-C (slower than O-Bn) | Amine + toluene | May need forcing |
| Cbz | H₂, Pd-C | Amine + CO₂ + toluene | Simultaneous removal |
| PMB | H₂, Pd-C or DDQ, CAN | Alcohol + aldehyde | DDQ/CAN selective |
| Dithiane | NCS, NBS, I₂/H₂O | Carbonyl | Via sulfenyl halide |
| Oxime | TiCl₃, Zn/AcOH | Carbonyl | Reductive |
| Ns (nosyl) | PhSH, K₂CO₃ | Amine | Smiles rearrangement |

### 8.4 Hydrogenolysis

| Protecting Group | Conditions | Products | Notes |
|-----------------|------------|----------|-------|
| Bn (O-ether) | H₂, Pd-C, 1 atm, RT | Alcohol + toluene | Standard |
| Bn (N-alkyl) | H₂, Pd-C, longer time | Amine + toluene | Secondary amine product |
| Cbz | H₂, Pd-C | Amine + CO₂ + toluene | Also removes Bn, PMB |
| PMB | H₂, Pd-C | Alcohol + p-methoxytoluene | Same conditions as Bn |
| Benzylidene | H₂, Pd-C (cleaves benzylic C-O) | Diol + toluene | Ring opening |

**Catalyst Choice:**

```
Pd-C (10%): Standard, most common
Pd(OH)₂/C (Pearlman's): More active, for difficult substrates
Pd black: Very active, may overreduce
Rh/Al₂O₃: Alternative selectivity
```

### 8.5 Fluoride Deprotection

| Protecting Group | Conditions | Products | Notes |
|-----------------|------------|----------|-------|
| TMS | TBAF (1M THF), RT, 5-30 min | Alcohol + TMSF | Very fast |
| TBDMS | TBAF, THF, RT, 0.5-2 h | Alcohol + TBDMSF | Standard |
| TBDPS | TBAF, THF, longer time | Alcohol + TBDPSF | Slower than TBDMS |
| TIPS | TBAF, RT, 2-12 h | Alcohol + TIPS fluoride | Slowest silyl |
| TES | TBAF, RT | Alcohol | Similar to TBDMS |

**Alternative Fluoride Sources:**

```
TBAF (tetrabutylammonium fluoride): Standard, 1M in THF
TBAF·3H₂O: Milder, less basic
HF·pyridine: Stronger, for difficult cases
KF (with 18-crown-6): Alternative
```

**Selectivity:**

```
TMS >> TBDMS > TIPS > TBDPS
TMS can be removed with TBAF in presence of TBDMS, TBDPS
TBDMS can be removed with TBAF in presence of TBDPS (slower rate)
Acidic conditions: TMS >> TBDMS (TMS removed, TBDMS stable)
```

### 8.6 Photolysis

| Protecting Group | Wavelength | Products | Notes |
|-----------------|------------|----------|-------|
| NVOC (nitroveratryloxycarbonyl) | 365 nm | Amine + byproducts | Light-directed synthesis |
| NPEOC (nitrophenethyloxycarbonyl) | 300-350 nm | Amine + byproducts | Similar to NVOC |
| o-Nitrobenzyl esters | 350 nm | Acid + o-nitrosobenzaldehyde | Photocaged compounds |
| Coumarin derivatives | 400-450 nm | Deprotection | Visible light |

**Applications:**

```
- Light-directed peptide synthesis (photolithography)
- "Caged" compounds (neuroscience, photoactivated reagents)
- Spatial control in polymer synthesis
- 3D printing of biomaterials
```

### 8.7 Transition Metal Catalyzed Deprotection

| Protecting Group | Conditions | Products | Notes |
|-----------------|------------|----------|-------|
| Alloc | Pd(PPh₃)₄ (0.1 eq), PhSiH₃, THF, RT | Amine + propene | Mild, selective |
| Allyl ester | Pd(PPh₃)₄, dimedone or morpholine | Acid + allyl nucleophile | Orthogonal |
| Ns (nosyl) | Thiophenol, K₂CO₃ | Amine | Via Smiles |

---

## 9. Greener Alternatives

### 9.1 Avoiding Protecting Groups

**Principle:** The best protecting group is none at all. Modern synthesis aims to minimize protection/deprotection steps.

**Strategies:**

1. **Chemoselective Reagents**
   - Use reagents that react selectively with one functional group
   - Example: Oxazolidinone auxiliaries for enolate chemistry (no N-protection needed)

2. **Inherent Reactivity Differences**
   - Exploit natural reactivity differences between functional groups
   - Example: Grignard reagents react faster with carbonyls than esters

3. **Tandem/Cascade Reactions**
   - Design reactions where intermediates are immediately consumed
   - Example: Tandem Michael-aldol reactions

4. **Dynamic Covalent Chemistry**
   - Use reversible reactions that self-correct
   - Example: Imine formation that equilibrates

**Example: Classic Synthesis vs Protecting-Group-Free**

```
Classic (with protection):
ROH → ROTBDMS → reaction → deprotect → product (3 steps)

Protecting-group-free:
ROH + selective reagent → product (1 step)
```

### 9.2 Traceless Protection

**Principle:** Protecting groups that leave no trace after deprotection, or are converted to innocuous byproducts.

**Examples:**

1. **BOC:** Deprotection gives CO₂ and isobutylene (volatile)
2. **Fmoc:** Deprotection gives DBF adduct (removable)
3. **Silicon-based groups:** Converted to silanols/fluorides (non-toxic)

**Advanced Traceless Strategies:**

1. **Traceless Linkers for Solid Phase:**
   - Silyl linkers: cleaved by fluoride, leaves no residue
   - Safety-catch linkers: activated only when needed

2. **Self-Immolative Protecting Groups:**
   - Removal triggers cascade that releases the protected group
   - Example: p-aminobenzyl carbamates

### 9.3 Enzymatic Methods

**Advantages:**
- Highly selective (regio-, stereo-, chemoselective)
- Mild conditions (aqueous, neutral pH, RT)
- Environmentally benign

**Disadvantages:**
- Limited substrate scope
- Enzyme cost and stability
- Scale-up challenges

**Examples:**

1. **Lipase-Catalyzed Deprotection**
   - PPL (porcine pancreatic lipase): Selective ester hydrolysis
   - CAL-B (Candida antarctica lipase B): Broad substrate scope
   - Selective for primary vs secondary esters

2. **Esterase-Catalyzed Reactions**
   - Pig liver esterase (PLE): Selective hydrolysis
   - Horse liver esterase (HLE): Similar applications

3. **Penicillin Acylase**
   - Selective amide hydrolysis
   - Used in β-lactam antibiotic synthesis

4. **Kinase-Based Phosphate Deprotection**
   - Enzymatic phosphate ester hydrolysis
   - Biocompatible conditions

**Example: Enzymatic Selective Deprotection**

```
Substrate: Primary acetate + secondary acetate
Reagent: Lipase (CAL-B) in phosphate buffer
Result: Primary acetate hydrolyzed, secondary remains

Chemical method would require multiple steps for same selectivity
```

### 9.4 Green Solvents and Reagents

**Problem:** Traditional deprotection often uses hazardous reagents (HF, Na/NH₃, strong acids).

**Alternatives:**

| Traditional | Greener Alternative |
|-------------|---------------------|
| HF (for Bn, some silyl) | TBAF (for silyl), H₂/Pd (for Bn) |
| Na/NH₃ (Birch) | Electrochemical reduction |
| Strong acid (TFA neat) | Solid-supported acid (recyclable) |
| Diazomethane (toxic, explosive) | TMSCHN₂ (safer) |
| Mercuric salts (dithiane) | NCS, NBS (less toxic) |

**Solvent Considerations:**

```
Traditional: CH₂Cl₂, DMF, THF (concerns: toxicity, VOC)
Greener: 2-MeTHF, cyclopentyl methyl ether, EtOAc, EtOH
Water: Increasingly used with surfactants, phase-transfer
```

---

## 10. Worked Examples

### Example 1: Selective Protection of 1,2-Diol

**Problem:** Protect 1,2-diol selectively over a 1,3-diol.

**Solution:** Use acetone/DMP to form acetonide (kinetic control).

```
HO-CH₂-CH(OH)-CH₂-CH₂-CH₂OH + acetone + p-TsOH (cat.)
→ 1,2-O-isopropylidene (5-membered, kinetically favored)

Conditions: Acetone, molecular sieves, RT, 2 h
Result: 1,2-acetonide formed selectively; 1,3-diol remains unprotected
```

**Mechanism:**
- 1,2-diol forms 5-membered cyclic acetal faster (kinetic)
- 1,3-diol would form 6-membered (slower)
- Under kinetic conditions, 1,2-acetonide predominates

### Example 2: Orthogonal Deprotection in Peptide Synthesis

**Problem:** Synthesize tripeptide with Lys side chain, then selectively deprotect.

**Approach:** Fmoc/t-Bu strategy with orthogonal Lys side-chain protection.

```
Building blocks:
1. Fmoc-Ala-OH
2. Fmoc-Lys(Alloc)-OH (Alloc orthogonal to Fmoc/t-Bu)
3. Fmoc-Gly-OH

Solid-phase synthesis:
1. Load Fmoc-Gly on resin
2. Deprotect Fmoc (piperidine)
3. Couple Fmoc-Lys(Alloc)
4. Deprotect Fmoc
5. Couple Fmoc-Ala
6. Deprotect Fmoc

Selective deprotection:
1. Remove Alloc (Pd(PPh₃)₄, PhSiH₃) → free Lys side chain
2. Functionalize Lys side chain (e.g., acylation)
3. Cleave from resin with TFA → removes all t-Bu, Boc, and resin linkage

Result: Tripeptide with selectively functionalized Lys side chain
```

### Example 3: Removal of Benzyl Ethers in Presence of Alkene

**Problem:** Remove Bn ethers without reducing an alkene.

**Solution:** Use Birch reduction (Na/NH₃) instead of hydrogenation.

```
Substrate: R-O-Bn (with sensitive alkene)
Conditions: Na (2 eq), NH₃(l), t-BuOH, -78°C, 1 h
Result: R-OH + toluene (alkene preserved)

Mechanism: Single electron transfer to benzene ring, not alkene
```

**Alternative:** BCl₃ (Lewis acid) can also remove Bn without H₂.
```
R-O-Bn + BCl₃ (CH₂Cl₂, -78°C to RT) → R-OH + BnCl
```

### Example 4: Protecting Group Strategy for Prostaglandin Synthesis

**Problem:** Prostaglandin has multiple functional groups: alcohol, ketone, acid, alkene.

**Strategy:**

```
Functional groups:
- Two secondary alcohols (1,2-diol)
- One ketone
- One carboxylic acid
- Two alkenes (sensitive)

Protection strategy:
1. 1,2-diol → acetonide (acetone, acid)
2. Ketone → ethylene ketal (HOCH₂CH₂OH, acid)
3. Carboxylic acid → methyl ester (CH₂N₂)
4. Alkenes → no protection needed

Stability check:
- Acetonide: stable to base, mild acid
- Ketal: stable to base, mild acid  
- Methyl ester: stable to mild acid, base-labile
- Alkenes: stable to most conditions except H₂

Deprotection sequence:
1. Hydrolyze methyl ester (LiOH/THF-H₂O) — acetonide, ketal stable
2. Remove ketal (AcOH/H₂O) — acetonide stable (different stability)
3. Remove acetonide (AcOH/H₂O, stronger conditions)

Result: Prostaglandin core with all groups revealed
```

### Example 5: Silyl Group Migration

**Problem:** Silyl ethers can migrate under basic or acidic conditions.

**Scenario:**
```
Starting material: R-CH(TBDMS)-CH₂-OH (secondary TBDMS, primary OH)
Base treatment: Migration occurs
R-CH(TBDMS)-CH₂-OH → R-CH(OH)-CH₂-OTBDMS

Problem if migration unwanted: Wrong product
```

**Solutions:**
1. Use more stable silyl group (TBDPS instead of TBDMS)
2. Use non-silyl protection (Bn, Ac)
3. Avoid basic conditions (use acidic or neutral)

**Mechanism:**
```
Base-catalyzed: RO⁻ attacks Si, pentavalent intermediate, migration
Acid-catalyzed: Protonation of O-Si, migration to better nucleophile
```

### Example 6: Peptide Synthesis — Cysteine Protection Strategies

**Problem:** Cysteine thiol is reactive and can form disulfides.

**Protection Options:**

| PG | Removal | Orthogonal? |
|----|---------|-------------|
| Trt (trityl) | TFA (mild) | Orthogonal to Fmoc, removed during final TFA |
| Acm (acetamidomethyl) | I₂, Hg(II), Tl(III) | Orthogonal to TFA, removed later |
| t-Bu (tert-butyl) | TFA | Not orthogonal (same as other t-Bu) |
| StBu (S-tert-butyl) | DTT, TCEP (reductive) | Orthogonal |
| Mob (p-methoxybenzyl) | TFA, stronger than Trt | Not orthogonal to TFA |

**Disulfide Formation Strategy:**

```
Option 1: Oxidative folding
- Synthesize with Cys(Trt)
- TFA cleavage gives free Cys
- Air oxidation or DMSO oxidation forms disulfide

Option 2: Orthogonal Cys protection
- Cys(Acm) + Cys(Trt)
- TFA removes Trt → free Cys
- I₂ removes Acm → second free Cys
- I₂ also forms disulfide (one-pot)
- Result: Specific disulfide bond

Option 3: Multiple orthogonal groups
- Cys(Acm), Cys(StBu), Cys(Trt)
- Sequential deprotection for multiple disulfides
```

### Example 7: Glycosylation with Participating Group

**Problem:** Control stereochemistry at anomeric center during glycosylation.

**Solution:** Use participating protecting group at C-2.

```
Donor: Per-O-benzylated glucosyl trichloroacetimidate
       (non-participating at C-2)

Result: Mixture of α and β glycosides

Donor: Per-O-benzoylated glucosyl trichloroacetimidate
       (participating at C-2: benzoate ester)

Mechanism:
1. Activation of anomeric position (TMSOTf)
2. Neighboring group participation from C-2 benzoate
3. Dioxolenium ion intermediate
4. Nucleophile attacks from opposite face (trans to participating group)

Result: Predominantly or exclusively β-glycoside (1,2-trans)
```

**Stereochemical Outcome:**

```
Participating group (ester) → 1,2-trans (β for gluco, α for galacto)
Non-participating (ether) → mixture (kinetic control)
```

### Example 8: Three-Component Orthogonal Protection

**Problem:** Protect amine, alcohol, and carboxylic acid orthogonally.

**Strategy:**

```
Substrate: H₂N-R-OH-COOH

Protection:
1. Amine: Fmoc (piperidine-labile)
2. Alcohol: TBDMS (fluoride-labile)  
3. Carboxylic acid: Allyl ester (Pd-labile)

Deprotection:
1. Fmoc: 20% piperidine/DMF, RT, 20 min
   - TBDMS stable
   - Allyl ester stable
2. TBDMS: TBAF/THF, RT, 1 h
   - Allyl ester stable (F⁻ doesn't affect)
3. Allyl: Pd(PPh₃)₄, PhSiH₃, THF, RT, 2 h
   - All others already removed

Result: Complete orthogonality, each group removed independently
```

### Example 9: Differential Protection of Primary vs Secondary Alcohols

**Problem:** Protect primary alcohol selectively over secondary.

**Method 1: Bulky Reagent**
```
Substrate: HO-CH₂-CH(OH)-R

Conditions: TBDMSCl (1 eq), imidazole, DMF, RT, 2 h
Result: HO-CH₂-CH(OTBDMS)-R (secondary protected)
        Because secondary is less hindered for equatorial attack

Alternative: TBDPSCl, imidazole
Result: Primary alcohol protected (TBDPS too bulky for secondary)
```

**Method 2: Kinetic vs Thermodynamic**
```
Kinetic protection:
- TMSCl (excess), Et₃N, short reaction time
- Both protected, but primary faster

Selective deprotection:
- AcOH/H₂O, mild conditions
- Primary TMS removed faster
- Secondary TMS remains
```

### Example 10: Total Synthesis Strategy — Erythronolide B

**Problem:** Macrolide synthesis with multiple stereocenters and functional groups.

**Key Protecting Group Strategy:**

```
Functional groups in seco-acid precursor:
- Multiple secondary alcohols
- One ketone
- Terminal carboxylic acid

Strategy:
1. Ketone: Protect as ketal (ethylene glycol)
   - Stable during subsequent steps
   - Removed after macrolactonization

2. Hydroxyls: Differentiate by stereochemistry and position
   - C-3: TBDMS (removed early)
   - C-5: TBDPS (stable, removed later)
   - C-6: MOM (acid-labile, orthogonal to silyl)
   - C-11: TBDMS (same as C-3)
   - C-12: TBDPS (same as C-5)
   - C-13: TBDMS

3. Carboxylic acid: Protect as thioester for macrolactonization
   - converted to seco-acid before cyclization

Deprotection sequence (after macrolactonization):
1. Remove ketal (AcOH/H₂O)
2. Remove MOM (TMSBr)
3. Remove TBDMS (TBAF) — TBDPS stable
4. Remove TBDPS (TBAF, longer time)

Result: Erythronolide B
```

### Example 11: Alloc as Orthogonal Amine Protection

**Problem:** Protect amine that must survive both acid and base treatments.

**Solution:** Alloc (Pd-labile).

```
Substrate: H₂N-R-X, where X is acid- and base-sensitive

Protection:
- Alloc-Cl, NaHCO₃, CH₂Cl₂/H₂O, 0°C
- Product: Alloc-NH-R-X

Stability:
- TFA (acid): Stable
- Piperidine (base): Stable
- LiAlH₄: Stable
- Grignard: Stable

Deprotection:
- Pd(PPh₃)₄ (0.1 eq), PhSiH₃ (2 eq), THF, RT
- Alloc-NH-R-X → H₂N-R-X + propene

Applications:
- Peptide synthesis (orthogonal to Fmoc/Boc)
- Complex natural product synthesis
- When Alloc is the only option
```

### Example 12: Photolabile Protecting Groups for Spatial Control

**Problem:** Deprotect specific regions of a surface-bound molecule.

**Solution:** NVOC (nitroveratryloxycarbonyl).

```
Application: Light-directed peptide synthesis on chip

Process:
1. Entire surface coated with NVOC-protected amine
2. UV light (365 nm) through mask illuminates specific regions
3. Illuminated regions: NVOC removed, free amine exposed
4. Couple Fmoc-amino acid to exposed regions
5. Deprotect Fmoc (piperidine)
6. Repeat with different masks for each amino acid

Advantages:
- Spatial control (photolithography)
- Combinatorial synthesis
- DNA microarray analogy

Photolysis mechanism:
- UV absorption by nitro group
- Intramolecular redox
- Release of free amine + o-nitrosobenzaldehyde derivative
```

### Example 13: Solid-Phase Synthesis — Wang Resin Strategy

**Problem:** Attach carboxylic acid to resin, synthesize, cleave under mild conditions.

**Solution:** Wang resin (acid-labile linker).

```
Linker: p-alkoxybenzyl alcohol linker
Attachment: R-COOH + Wang resin + DIC/DMAP → R-COO-CH₂-Ph-O-CH₂-polystyrene

Synthesis:
- Fmoc-AA1-OH coupled to resin-bound acid
- Standard Fmoc-SPPS cycles
- Build peptide chain

Cleavage:
- TFA (95% in CH₂Cl₂) or TFA + scavengers
- Acid-labile benzylic ether cleaved
- R-COOH released + peptide

Mechanism: Benzylic cation formation, stabilized by p-alkoxy

Advantages:
- Mild cleavage (TFA, RT)
- Compatible with Fmoc chemistry
- C-terminal acid product
```

### Example 14: Enzymatic Selective Deprotection

**Problem:** Hydrolyze primary acetate in presence of secondary acetate.

**Solution:** Lipase-catalyzed hydrolysis.

```
Substrate: AcO-CH₂-CH(OAc)-R (primary and secondary acetates)

Chemical hydrolysis (K₂CO₃/MeOH):
- Both acetates hydrolyzed
- No selectivity

Enzymatic hydrolysis (CAL-B, phosphate buffer, pH 7, RT):
- Primary acetate hydrolyzed selectively
- Secondary acetate remains
- Product: HO-CH₂-CH(OAc)-R

Mechanism:
- Lipase active site accommodates primary acetate
- Secondary acetate too hindered for hydrolysis
- Excellent regioselectivity

Advantages:
- High selectivity
- Mild conditions (aqueous, neutral pH)
- No protecting groups needed

Scale-up:
- Enzyme can be immobilized and recycled
- Organic cosolvent (t-BuOH) improves substrate solubility
```

### Example 15: Dithiane Umpolung — Three-Component Coupling

**Problem:** Form carbon-carbon bond at a carbonyl carbon (normally electrophilic).

**Solution:** Convert aldehyde to dithiane, use as nucleophile.

```
Step 1: Form dithiane
R-CHO + HS(CH₂)₃SH + BF₃·Et₂O → R-CH(S(CH₂)₃) (1,3-dithiane)

Step 2: Deprotonate
R-CH(S(CH₂)₃) + n-BuLi → R-C(Li)(S(CH₂)₃) (nucleophilic!)

Step 3: Alkylate
R-C(Li)(S(CH₂)₃) + R'-X → R-C(R')(S(CH₂)₃)

Step 4: Second alkylation (if desired)
R-C(R')(S(CH₂)₃) + n-BuLi → R-C(R')(Li)(S(CH₂)₃)
R-C(R')(Li)(S(CH₂)₃) + R''-X → R-C(R')(R'')(S(CH₂)₃)

Step 5: Deprotect
R-C(R')(R'')(S(CH₂)₃) + HgCl₂/H₂O → R-C(R')(R'')-CHO (aldehyde)
     or + NCS/H₂O → aldehyde

Result: Aldehyde carbon has been alkylated (normally impossible)
        Umpolung achieved: carbonyl carbon as nucleophile

Applications:
- Synthesis of complex aldehydes
- Corey-Seebach reaction
- Natural product synthesis
```

---

## Quick Reference Tables

### Table 1: Common Protecting Groups at a Glance

| Functional Group | Most Common PG | Alternative PGs |
|-----------------|----------------|-----------------|
| Primary alcohol | TBDMS, Bn | TBDPS, Ac, THP, Tr |
| Secondary alcohol | TBDMS, Ac | TBDPS, Bn, Bz |
| Tertiary alcohol | TMS (temp) | Limited options |
| 1,2-Diol | Acetonide | Benzylidene |
| Primary amine | Boc, Cbz, Fmoc | Alloc, Ac, Ts |
| Secondary amine | Boc, Cbz | Alloc, Ts |
| Aldehyde | Acetal, dithiane | Oxime, hydrazone |
| Ketone | Ketal, dithiane | Oxime, hydrazone |
| Carboxylic acid | Me ester, t-Bu ester | Bn ester, allyl ester |
| Thiol | Trt, Acm | StBu, Bn |
| Phosphate | Cyanoethyl, Me | Phenyl |

### Table 2: Orthogonal Sets for Complex Synthesis

| Set | Group 1 | Group 2 | Group 3 | Group 4 |
|-----|---------|---------|---------|---------|
| Peptide (Fmoc) | Fmoc (base) | t-Bu (TFA) | Trt (TFA) | Acm (I₂) |
| Peptide (Boc) | Boc (TFA) | Bn (HF) | 2-Cl-Z (HF) | Acm (I₂) |
| Carbohydrate | TBDMS (F⁻) | Bn (H₂) | Bz (base) | Lev (hydrazine) |
| General 1 | Fmoc (base) | TBDMS (F⁻) | Allyl (Pd) | — |
| General 2 | Boc (TFA) | TBDPS (F⁻) | Bn (H₂) | — |
| General 3 | Alloc (Pd) | Fmoc (base) | t-Bu (TFA) | — |

### Table 3: Protecting Group Selection Guide

**For Acidic Conditions:**
```
Stable: Bn, TBDPS, TBDMS, Bz, Ac, Cbz
Labile: Boc, THP, Tr, MOM, PMB, t-Bu
```

**For Basic Conditions:**
```
Stable: Bn, TBDPS, TBDMS, TIPS, Boc, Cbz
Labile: Fmoc, Ac, Bz, TMS
```

**For Hydrogenation:**
```
Stable: Boc, TBDMS, TBDPS, Ac, Fmoc, TMS
Labile: Bn, Cbz, PMB
```

**For Fluoride:**
```
Stable: Bn, Ac, Bz, Boc, Cbz, Fmoc
Labile: TMS, TBDMS, TIPS, TBDPS
```

---

## References and Further Reading

1. **Greene's Protective Groups in Organic Synthesis** (5th ed.) — Wuts, P.G.M. — The definitive reference
2. **Strategic Applications of Named Reactions in Organic Synthesis** — Kürti, L.; Czakó, B.
3. **Organic Synthesis: The Disconnection Approach** — Warren, S.
4. **March's Advanced Organic Chemistry** (7th ed.) — Smith, M.B.

**Online Resources:**
- Organic Chemistry Portal (protecting group database)
- Reaxys (reaction database with protecting group information)
- SciFinder (literature search)

---

*Last updated: 2026-03-31*
*Part of the chem-memory knowledge system (L2 principles)*
