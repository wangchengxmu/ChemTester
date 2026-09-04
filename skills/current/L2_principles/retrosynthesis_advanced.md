# Retrosynthetic Analysis — Advanced Reference

> **Level:** L2 — Graduate organic chemistry concept reference  
> **Purpose:** Dense, lookup-oriented retrosynthesis planning guide  
> **Related:** L1 `chemistry-core-map.md` → L3 tool-backed synthesis planners

---

## 1. Core Principles

### 1.1 Disconnection

A **disconnection** is the reverse of a synthetic bond-forming step. Given target molecule **T**, we imagine breaking a bond to generate simpler precursors **A** and **B**:

```
T ──► A + B   (retrograde arrow "⇒")
```

Key rules:
- Every disconnection must map to a known **forward reaction** with acceptable yields and selectivity.
- Prefer disconnections that **simultaneously** establish correct oxidation state and stereochemistry.
- Rank disconnections by strategic value (see §2); not all bonds are equal.

### 1.2 Synthons and Synthetic Equivalents

| Term | Definition |
|------|-----------|
| **Synthon** | Idealized ionic fragment representing the two halves of a disconnection. May be charge-separated (d⁺/d⁻) or radical. |
| **Synthetic equivalent** | The real reagent that delivers the synthon. Often differs significantly from the idealized synthon. |

**Example:** Disconnecting an ester to "acyl cation + alkoxide" synthons. The synthetic equivalent of the acyl cation synthon is an acid chloride (or anhydride), not a literal acyl cation.

```
R-COOR'  ⇒  R-CO⁺  +  ⁻OR'
         fwd:  R-COCl  +  R'OH  / base
```

**Synthon polarity table** (common fragments):

| Synthon | Polarity | Typical Equivalent(s) |
|---------|----------|-----------------------|
| R-CH₂⁻ | d⁻ | RCH₂MgBr, RCH₂Li, RCH₂TMS (peterson) |
| R-CO⁺ | d⁺ | RCOCl, RCOOR', (RCO)₂O, RCHO (aldol acceptor) |
| R-CH=CH⁺ | d⁺ | RCH₂CH₂OH → oxidation to aldehyde (Wittig target), or β-halo carbonyl |
| ⁻CH₂COOR' | d⁻ | CH₂(COOR')₂ (malonate), CH₃COCH₂COOR' (acetoacetate), LiCH₂COOR' |

### 1.3 Transform-Based vs Target-Based Analysis

| | **Transform-Based** | **Target-Based** |
|---|---|---|
| **Entry point** | Known reaction → apply reverse | Molecular features of target → pattern match |
| **Method** | Database/template search | Symmetry, functional group pattern, strategic bonds |
| **Strength** | Exhaustive for known transforms | Creative, can discover non-obvious routes |
| **Weakness** | Limited to known chemistry | Requires deep chemical intuition |
| **Tool** | RetroSim, template-based CASP | Manual analysis, expert systems |

**Practical approach:** Hybrid. Use target-based reasoning to identify strategic bonds, then validate with known transforms.

### 1.4 Retrosynthetic Planning Heuristics

1. **Maximize convergency** — aim for >2 fragments converging rather than a long linear sequence.
2. **FGI last** — install sensitive functional groups as late as possible.
3. **Protecting groups as a last resort** — redesign the route before adding protecting groups.
4. **Redox economy** — avoid oxidation → reduction → oxidation sequences.
5. **Scaffold first, decoration later** — establish the carbon skeleton before installing substituents.
6. **Timing of stereochemistry** — set stereocenters via the bond-forming step when possible (substrate control > auxiliary > resolution).

---

## 2. Strategic Bonds & Difunctional Relationships

The strategic bond is the one whose disconnection gives the greatest simplification. The most useful organizing principle is the **difunctional relationship** — the relative position of two functional groups that reveals the bond-forming strategy.

### 2.1 1,2-Difunctional Relationships

```
X─C─C─Y   (1,2)
```

| Pattern | Disconnection | Forward Reaction | Notes |
|---------|--------------|-------------------|-------|
| 1,2-diol | C─C | Pinacol coupling (reductive), epoxide opening | Diol from aldehyde dimerization |
| α-hydroxy carbonyl | C─C | Aldol addition (cyanohydrin variant) | Self-condensation of aldehydes |
| α-amino carbonyl | C─C | Mannich reaction | Imine + enolate |
| 1,2-diketone | C─C | Benzil coupling, acyloin condensation | |
| Vicinal dibromide | C─C | Alkene + Br₂ (addition) | Simple but non-strategic |

### 2.2 1,3-Difunctional Relationships

```
X─C─C─C─Y   (1,3)
```

| Pattern | Disconnection | Forward Reaction | Notes |
|---------|--------------|-------------------|-------|
| β-hydroxy carbonyl | C─C (α–β) | **Aldol reaction** | Most fundamental 1,3 pattern |
| β-keto ester | C─C | **Claisen condensation** | Ketone + ester |
| β-amino carbonyl | C─C | **Mannich reaction** | Ketone + iminium |
| 1,3-diol | C─C | Aldol + reduction, or allylation → hydroboration | Redox approach |
| β-keto nitrile / β-keto phosphonate | C─C | Knoevenagel / HWE variants | |

**Key transforms for 1,3:**
- **Aldol** (donor enolate + acceptor carbonyl): RCHO + R'CH₂CHO → RCH(OH)CH(R')CHO
- **Claisen** (ester enolate + ester): RCOOR' + R''COOR' → RCOCH(R'')COOR'
- **Mannich** (enolate + iminium): R₂C=O + CH₂=NR₂⁺ → R₂C(OH)CH₂NR₂

### 2.3 1,4-Difunctional Relationships

```
X─C─C─C─C─Y   (1,4)
```

| Pattern | Disconnection | Forward Reaction | Notes |
|---------|--------------|-------------------|-------|
| γ,δ-unsaturated carbonyl | C─C (β–γ) | **Michael addition** | Conjugate addition of nucleophile |
| 1,4-diketone | C─C | Michael + aldol cascade | Michael acceptor + 1,3-dicarbonyl |
| 1,4-dicarbonyl | C─C | Stork enamine alkylation + hydrolysis | |
| 1,4-diol | C─C | Allylation (crotyl) + dihydroxylation | |

**Michael addition patterns:**
- Soft nucleophiles: enamines, thiols, stabilized enolates (malonate, β-keto ester)
- Hard nucleophiles: organocuprates, lithium enolates (with Cu catalysis)
- Asymmetric: Cu-BOX, phase-transfer, organocatalysis (MacMillan, Hayashi)

### 2.4 1,5-Difunctional Relationships

```
X─C─C─C─C─C─Y   (1,5)
```

| Pattern | Disconnection | Forward Reaction | Notes |
|---------|--------------|-------------------|-------|
| 1,5-dicarbonyl | C─C | **Michael + aldol (Robinson annulation)** | Ring-forming cascade |
| δ-lactone / δ-lactam | C─C | Ring-closing metathesis, aldol-lactonization | |
| 1,5-diene | C─C | Ring-closing metathesis (RCM) | Template: diene + Grubbs catalyst |

The 1,5-relationship is often **ring-forming** — both Robinson annulation and RCM exploit 1,5-geometry.

### 2.5 1,6-Difunctional Relationships

```
X─C─C─C─C─C─C─Y   (1,6)
```

| Pattern | Disconnection | Forward Reaction | Notes |
|---------|--------------|-------------------|-------|
| 1,6-dicarbonyl | C─C | Acylation of enolate with ω-halo carbonyl + intramolecular aldol | Often Dieckmann-type |
| 1,6-diene | C─C | Ring-closing metathesis → cyclohexene | 6-membered ring preference |
| δ,ε-unsaturated ketone | C─C | Extended Michael (remote) | Less reliable |

### 2.6 Strategic Bond Selection — Decision Flow

```
Identify functional groups in target
        │
        ▼
Map all difunctional relationships (1,2 through 1,6)
        │
        ▼
Rank by:
  1. Ring-forming potential (5-6 membered preferred)
  2. Convergence (branch point)
  3. Stereocontrol opportunity
  4. Known reliable transform
        │
        ▼
Disconnect highest-ranked bond
        │
        ▼
Repeat on each fragment until available SM or commercial
```

---

## 3. Functional Group Interconversions (FGI)

### 3.1 Oxidation State Ladders

Carbons can exist across a continuum of oxidation states. Effective retrosynthesis uses these ladders to plan FGI sequences with **minimum redox steps**.

**Common oxidation state ladder (by carbon type):**

```
ALKANE → 1° ALCOHOL → ALDEHYDE → CARBOXYLIC ACID
   0        +I            +II          +III

      OR: ALKANE → ALKENE → EPOXIDE → 1,2-DIOL → α-HYDROXY ALDEHYDE
```

**Ketone ladder:**
```
2° ALCOHOL → KETONE → α,β-UNSATURATED KETONE → 1,4-DICARBONYL
    0          +I              +I (conjugated)        +I each
```

**FGI shortcuts (multi-step in one):**
| Target | From | Method |
|--------|------|--------|
| Aldehyde | Alcohol | PCC, Swern, Dess-Martin, TEMPO/NaOCl |
| Aldehyde | Alkene | Ozonolysis (reductive workup), OsO₄/NaIO₄ |
| Acid | Alcohol | Jones, PDC, KMnO₄ |
| Ketone | Alkene | Ozonolysis (reductive), Wacker oxidation |
| Alcohol | Alkene | Hydroboration (anti-Markovnikov), oxymercuration (Markovnikov) |
| Alkane | Alkyl halide | LiAlH₄, Pd/C-H₂ |
| Alkene | Alkyl halide | E2 (strong base), elimination |

### 3.2 Protecting Group Considerations

**Cardinal rule:** Only use protecting groups when there is no alternative.

**Common protecting groups and their removal:**

| Group Protected | Protecting Group | Removal Conditions | Orthogonal To |
|----------------|-----------------|-------------------|---------------|
| 1°/2° alcohol | TBDMS (TBS) | TBAF, HF·py | Ac, PMB, Bn |
| 1°/2° alcohol | TIPS | TBAF (slower than TBS) | TBS, Ac |
| 1°/2° alcohol | Acetyl (Ac) | K₂CO₃/MeOH, NaOH | TBS, PMB |
| 1°/2° alcohol | PMB | DDQ, CAN | TBS, Ac, Bn |
| 1°/2° alcohol | Benzyl (Bn) | H₂/Pd-C, Na/NH₃ | Ac, TBS, PMB |
| Diol | Acetonide | AcOH/H₂O, PPTS/MeOH | TBS, Bn |
| Amine | Boc | TFA, HCl/dioxane | Cbz, Fmoc |
| Amine | Cbz | H₂/Pd-C, Birch | Boc, Fmoc |
| Amine | Fmoc | Piperidine/DMF | Boc, Cbz |
| Carboxylic acid | Methyl ester | LiOH, NaOH, LiI | t-Bu ester |
| Carboxylic acid | t-Butyl ester | TFA, HCl | Methyl ester |
| Aldehyde/ketone | Ethylene acetal | PPTS/H₂O, TFA/H₂O | Most PGs |
| Aldehyde/ketone | 1,3-dioxolane | Hg(OAc)₂ (old), PPTS (mild) | |

**Orthogonal deprotection strategy example:**
```
Boc-NH → TFA (selective, leaves Cbz intact)
Cbz-NH → H₂/Pd-C (selective, leaves Boc intact)
TBS-O → TBAF (selective, leaves Ac intact)
Ac-O → K₂CO₃/MeOH (selective, leaves TBS intact)
```

### 3.3 Latent Functional Groups

A **latent functional group** is one that can be revealed by a single, clean transformation:

| Latent Group | Revealed As | Conditions |
|-------------|-------------|------------|
| Alkene | 1,2-Diol | OsO₄/NMO or KMnO₄ |
| Alkene | Aldehyde + aldehyde | Ozonolysis (reductive) |
| Alkene | Halohydrin | NBS/H₂O |
| Epoxide | 1,2-Diol | Acidic or basic hydrolysis |
| Nitrile | Carboxylic acid | Hydrolysis (acid or base) |
| Nitrile | Aldehyde | DIBAL-H (partial reduction) |
| Nitro | Amine | H₂/Pd-C, SnCl₂, Zn/HCl |
| Alkyne | trans-Alkene | Na/NH₃ |
| Alkyne | cis-Alkene | Lindlar catalyst |
| Alkyne | 1,2-Diketone | KMnO₄ or RuO₄ |

---

## 4. C–C Bond Disconnections

### 4.1 Aldol Disconnection

**Pattern:** β-hydroxy carbonyl ⇒ aldehyde/ketone + aldehyde/ketone

```
    OH                 O               O
    │                  ║               ║
R─C─C─R'    ⇒    R─C─H  +  H─C─R'
    │   (1,3)       (acceptor)     (donor)
    H
```

**Variants:**

| Type | Enolate Source | Acceptor | Product | Notes |
|------|---------------|----------|---------|-------|
| Classical | LDA / metal enolate | Aldehyde | β-Hydroxy carbonyl | May need kinetic/thermodynamic control |
| Mukaiyama | Silyl enol ether | Aldehyde (Lewis acid) | β-Silyloxy carbonyl | Excellent stereocontrol with chiral Lewis acids |
| Evans | N-acyl oxazolidinone | Aldehyde | β-Hydroxy acyl oxazolidinone | Auxiliary-controlled, high diastereoselectivity |
| Directed | Metal enolate (preformed) | Aldehyde | Varies | Predictable Z/E enolate geometry |

**Stereochemical models:**
- **Zimmerman-Traxler transition state** (chair, six-membered):
  - Z-enolate + aldehyde → **anti** aldol product
  - E-enolate + aldehyde → **syn** aldol product
- **Evans syn-aldol:** Z-boron enolate from N-acyloxazolidinone → syn

### 4.2 Michael (Conjugate) Disconnection

**Pattern:** γ-functionalized carbonyl ⇒ enolate (donor) + α,β-unsaturated carbonyl (acceptor)

```
    R                    R
    │                    ║
R─C─C─C═C  ⇒  R⁻  +  C═C─C═O
            (donor)    (Michael acceptor)
```

**Acceptors:** α,β-unsaturated ketones, esters, nitriles, nitro compounds, sulfones

**Donors:**

| Donor Type | Conditions | Notes |
|-----------|-----------|-------|
| Stabilized enolate | Malonate, acetoacetate, β-keto ester | Mild bases (piperidine, Et₃N) |
| Enamine | Stork approach: secondary amine + ketone | Acidic workup releases product |
| Organocuprate | R₂CuLi, RCu(CN)Li | Adds at β-position, 1,4-selective |
| Lithium enolate + Cu(I) | LDA then CuI | Good for non-stabilized enolates |
| Organocatalytic | Proline derivatives (Jørgensen, Hayashi) | Enamine/Iminium activation |

**Asymmetric Michael addition — key methods:**
- Cu-BOX / Cu-PyBox complexes with enolates
- Phase-transfer catalysis (Maruoka catalyst, Cinchona alkaloids)
- Bifunctional thiourea catalysts (Takemoto)
- Organocatalysis: MacMillan imidazolidinone (iminium activation), proline (enamine)

### 4.3 Claisen Disconnection

**Pattern:** β-keto ester ⇒ ester + ester (or ester + ketone)

```
    O     O                O
    ║     ║                ║
R─C─C─OR'  ⇒  R─C─OR'  +  H─C─OR'
        (1,3)
```

**Variants:**

| Type | Reactants | Product | Conditions |
|------|----------|---------|-----------|
| Claisen condensation | 2 × ester | β-keto ester | NaOEt, then acid workup |
| Crossed Claisen | Ester + non-enolizable ester | β-keto ester | NaH, then add non-enolizable ester |
| Dieckmann condensation | Diester | β-keto ester (cyclic) | NaOEt (intramolecular) |
| Acetoacetic ester synthesis | Ethyl acetoacetate + alkyl halide | Alkylated acetoacetate | NaOEt, then RX |
| Malonic ester synthesis | Diethyl malonate + alkyl halide | Alkylated malonate | NaOEt, then RX |
| Carroll rearrangement | β-keto allyl ester | γ,δ-unsaturated ketone | Heat (300°C) or Pd(0) |

### 4.4 Mannich Disconnection

**Pattern:** β-amino carbonyl ⇒ carbonyl + amine + formaldehyde (or imine)

```
    OH                O
    │                 ║
R─C─C─NR₂  ⇒  R─C─R'  +  CH₂═NR₂⁺
  (β-amino carbonyl)   (iminium ion)
```

**Forward conditions:**
- Three-component: carbonyl + formaldehyde + secondary amine (acidic)
- Preformed iminium: carbonyl + iminium salt (Lewis acid)
- Asymmetric: proline catalysis, MacMillan catalyst, BINOL-phosphoric acids

### 4.5 Knoevenagel Disconnection

**Pattern:** α,β-unsaturated carbonyl (with EWG) ⇒ aldehyde + active methylene compound

```
          EWG              EWG
          │                │
R─CH═C─EWG  ⇒  R─CHO  +  H₂C─EWG
```

**EWGs:** CN, COOR, CHO, COR, NO₂, SO₂R

**Catalysts:** Piperidine, ammonium acetate, TiCl₄/pyridine, L-proline

**Distinguish from aldol:** Knoevenagel → dehydration is typically spontaneous due to strong EWG.

### 4.6 Wittig / Horner-Wadsworth-Emmons Disconnection

**Pattern:** Alkene ⇒ carbonyl + phosphonium ylide (Wittig) or phosphonate carbanion (HWE)

```
R─CH═CH─R'  ⇒  R─CHO  +  Ph₃P═CH─R'    (Wittig)
           or  R─CHO  +  (RO)₂P(O)CH₂R' (HWE)
```

**Selectivity:**

| Reagent | Alkene Geometry | Notes |
|---------|----------------|-------|
| Non-stabilized ylide (R = alkyl) | **Z**-predominant | Li salt-free conditions favor Z |
| Semi-stabilized ylide (R = Ar, vinyl) | Mixture | Often E-predominant |
| Stabilized ylide (R = COOR, CN) | **E**-predominant | |
| HWE (phosphonate) | **E**-predominant | More reliable, easier workup |
| Still-Gennari (CF₃CH₂O)₂P(O) | **Z**-selective | Fluorinated phosphonate |
| Ando variant | **Z**-selective | |

**HWE advantages over Wittig:**
- Byproduct is water-soluble phosphate (easy purification)
- More consistent E-selectivity
- Tolerates many functional groups

### 4.7 Julia Olefination

**Pattern:** Alkene ⇒ carbonyl + phenyl sulfone

```
R─CH═CH─R'  ⇒  R─CHO  +  R'─CH₂─SO₂Ph
```

**Steps:** Alkylation of sulfone anion with carbonyl-derived electrophile → reductive elimination (Na(Hg), SmI₂, or via sulfone→sulfonate→elimination).

**Variants:**

| Variant | Reagent | Geometry | Notes |
|---------|---------|----------|-------|
| Classical Julia | PhSO₂CH₂R + R'CHO → β-hydroxy sulfone → Na/Hg | E | Harsh conditions |
| Julia-Kocienski | 1-phenyl-1H-tetrazol-5-yl sulfone (PT-sulfone) | E | Milder, widely used |
| Modified Julia (one-pot) | NaHMDS + aldehyde, then reductant | E | Convenient |

### 4.8 Peterson Olefination

**Pattern:** Alkene ⇒ carbonyl + α-silyl carbanion

```
R─CH═CH─R'  ⇒  R─CHO  +  R'─CH₂─SiMe₃
```

**Stereocontrol:**
- **Syn β-hydroxysilane → acid** → gives **E**-alkene
- **Anti β-hydroxysilane → acid** → gives **Z**-alkene
- **Syn β-hydroxysilane → base** → gives **Z**-alkene
- **Anti β-hydroxysilane → base** → gives **E**-alkene

---

## 5. Aromatic Strategies

### 5.1 Electrophilic Aromatic Substitution (EAS) Planning

**EAS directing effects table:**

| Substituent | Ortho/Para or Meta | Activating/Deactivating | Relative Rate |
|------------|---------------------|------------------------|---------------|
| −NH₂, −NHR | o/p | Strongly activating | >10⁶ |
| −OH, −OR | o/p | Strongly activating | ~10⁶ |
| −NHCOR | o/p | Moderately activating | ~10³ |
| −R (alkyl) | o/p | Weakly activating | ~10 |
| −Ph | o/p | Weakly activating | ~10 |
| −X (halogen) | o/p | Weakly deactivating | ~0.1 |
| −COR, −COOR | m | Moderately deactivating | ~10⁻² |
| −SO₃H, −CN | m | Strongly deactivating | ~10⁻⁷ |
| −NO₂, −NR₃⁺ | m | Very strongly deactivating | ~10⁻⁸ |

**Planning rules:**
1. **Introduce the strongest activating group first** — it directs subsequent substitutions.
2. **Meta directors must be introduced last** — they block further EAS.
3. **Bulky groups favor para** — steric hindrance at ortho.
4. **Use sequential protection/deprotection** when directing effects conflict.
5. ** ipso substitution** — replace a directing group after it has served its purpose (e.g., sulfonation → desulfonation, amino → diazonium → replacement).

### 5.2 Directed Ortho Metalation (DoM)

**Strategy:** Install a **directing metalation group (DMG)** that enables lithiation at the ortho position.

**Common DMGs (in order of effectiveness):**

| DMG | Base | Ortho Selectivity | Notes |
|-----|------|-------------------|-------|
| −OCONEt₂ | s-BuLi/TMEDA | Excellent | Carbamate (Weinreb) |
| −OMe | n-BuLi | Good | Anisole series |
| −NMe₂ | s-BuLi | Excellent | Aniline derivative |
| −CONR₂ | LDA or s-BuLi | Excellent | Amide DMG |
| −SO₂NR₂ | s-BuLi | Excellent | Sulfonamide |
| −F | LDA | Good | Unique: F as DMG |

**DoM planning paradigm:**
```
Install DMG → ortho-lithiation → electrophile quench → transform DMG
```

Example sequence:
```
Ph-F  →  LDA, −78°C  →  ortho-F lithiation  →  DMF  →  ortho-formyl fluorobenzene
       →  F can be further transformed or removed
```

### 5.3 Ipso Substitution

**Definition:** Substitution at the position already occupied by a group (rather than ortho/para/meta).

| Reaction | Ipso Group | Replacement With | Conditions |
|----------|-----------|-----------------|------------|
| Desulfonation | −SO₃H | −H | Dilute H₂SO₄, heat |
| Balz-Schiemann | −N₂⁺BF₄⁻ | −F | Heat |
| Sandmeyer | −N₂⁺Cl⁻ | −Cl, −Br, −CN, −I | CuX |
| Gattermann | −N₂⁺ | −CN | CuCN, HCl |
| Dakin-West type | Various | Various | Context-dependent |

### 5.4 Birch Reduction

**Transform:** Aromatic ring → **1,4-cyclohexadiene** (non-conjugated)

```
         Na, NH₃(l), t-BuOH
  Ar─X   ──────────────────────►  1,4-cyclohexadiene with X
```

**Regiochemistry:**

| Substituent | Position of double bonds | Product |
|------------|------------------------|---------|
| Electron-donating (EDG) | Away from substituent | Substituent on saturated carbons |
| Electron-withdrawing (EWG) | Toward substituent | Substituent on unsaturated carbons |

**Strategic use:**
- Provides **cyclohexenone** after hydrolysis of enol ether (from methoxy aromatics)
- Access to **ortho-alkyl phenols** via Birch → alkylation → rearomatization
- Key step in steroid and alkaloid synthesis

---

## 6. Heterocycle-Focused Retrosynthesis

### 6.1 Common Heterocycles — Key Disconnections

#### Pyridines

```
Pyridine  ⇒  1,5-dicarbonyl + NH₃ (Hantzsch synthesis)
         or  Chichibabin → amination
         or  N-oxide activation → substitution
```

**Key strategy:** Build from 1,5-dicarbonyl (Paal-Knorr analogy) or functionalize preformed pyridine via N-oxide.

#### Pyrroles, Furans, Thiophenes

**Paal-Knorr synthesis:**

```
1,4-dicarbonyl + amine    → pyrrole
1,4-dicarbonyl + acid      → furan  (H₂SO₄)
1,4-dicarbonyl + P₄S₁₀    → thiophene
```

**Knorr pyrrole:** β-keto ester + α-amino ketone → pyrrole

#### Indoles

**Fischer indole synthesis:**

```
Phenylhydrazine + carbonyl compound  →  indole
                                 (acid, heat → [3,3]-sigmatropic)
```

**Key disconnect:** Indole ⇒ aniline/phenylhydrazine + ketone/aldehyde

**Other routes:** Bischler-Möhlau, Reissert, Larock (Pd-catalyzed annulation of o-iodoaniline + alkyne).

#### Pyrimidines

```
Pyrimidine  ⇒  β-dicarbonyl + amidine
Purine      ⇒  pyrimidine + C1 (formate, formamide)
```

#### Piperidines

```
Piperidine  ⇒  1,5-difunctionalized C5 chain + N-source
           or  Diels-Alder of azadiene (less common)
           or  Reduction of pyridine (H₂/Pd, Birch, transfer)
           or  Cyclization of δ-amino nitrile/ketone
```

### 6.2 Strategy: "Decorate the Ring" vs "Build the Ring"

| Approach | When to Use | Example |
|----------|------------|---------|
| **Decorate** | Ring is commercially available or easily made | Functionalize pyridine, benzene, pyrrole |
| **Build** | Substituent pattern cannot be achieved by ring decoration | Hantzsch pyridine, Fischer indole, Paal-Knorr |

**Decision heuristic:**
1. Is the heterocycle commercially available? → Decorate.
2. Can the substitution pattern be achieved by sequential functionalization? → Decorate.
3. If not → Build the ring from acyclic precursors.

### 6.3 N-Heterocyclic Carbene (NHC) Precursors

Imidazolium salts and triazolium salts are made from:
- Imidazole → alkylation (MeI, BnBr) → imidazolium salt
- 1,2,4-triazole → alkylation → triazolium salt

---

## 7. Stereochemical Control in Retrosynthesis

### 7.1 Chiral Pool Strategy

**Concept:** Start from naturally occurring chiral molecules (amino acids, sugars, hydroxy acids, terpenes) and use their existing stereocenters.

**Common chiral pool starting materials:**

| Source | Available Stereochemistry | Key Use |
|--------|--------------------------|---------|
| L-amino acids | α-center, sometimes β | Amino alcohols, Evans auxiliaries |
| D-Glucose | 4 stereocenters | Polyol synthesis, cyclitols |
| L-Tartaric acid | 2 centers (meso or chiral) | Sharpless ligands, resolution |
| (−)-Menthol | 3 centers | Chiral auxiliaries |
| (S)-(−)-Citronellal | 2 centers | Monoterpenes, cyclohexenones |
| (R)-Carvone | 2 centers, enone | Robinson annulation substrates |
| Quinic acid | 4 centers | Shikimic acid derivatives |

**Advantages:** No asymmetric catalyst needed, enantiomerically pure.  
**Disadvantages:** Limited to available structures, may require lengthy manipulation.

### 7.2 Asymmetric Catalysis — Key Methods

| Reaction | Catalyst Type | Representative Example |
|----------|--------------|----------------------|
| Hydrogenation | Rh/(R,R)-DiPAMP, Ru-BINAP | Noyori hydrogenation of β-keto esters |
| Epoxidation | Sharpless (Ti-tartrate), Jacobsen (Mn-salen) | Allylic alcohols, unfunctionalized alkenes |
| Dihydroxylation | Sharpless AD-mix (DHQ/DHQD) | OsO₄/K₃Fe(CN)₆ with Cinchona ligands |
| Epoxide opening | Jacobsen Co-salen | Hydrolytic kinetic resolution (HKR) |
| Cyclopropanation | Cu-BOX, Rh₂(S-DOSP)₄ | Alkenes + diazo compounds |
| Aldol | Proline, MacMillan, Zn-prophenol | Direct aldol, Mukaiyama aldol |
| Michael | Proline derivatives, Cu-BOX | Enamine/Iminium activation |
| Allylic alkylation | Pd-PHOX, Ir-phosphoramidite | Trost asymmetric allylic alkylation |
| Conjugate addition | Cu-BOX + dialkylzinc | 1,4-addition to enones |
| Ring-opening | Chiral Lewis acids | Epoxides, aziridines |

### 7.3 Evans Auxiliaries (Oxazolidinones)

**Structure:** Derived from (S)- or (R)-phenylalanine, valine, or phenylglycine.

**Standard sequence:**
```
1. Acylation of oxazolidinone with acid chloride → N-acyl oxazolidinone
2. Diastereoselective alkylation (enolate + R-X) → α-substituted product
3. Cleavage: LiOH/H₂O₂ → acid, or LiBH₄ → alcohol, or LiAlH₄ → aldehyde
```

**Stereochemical outcome (Evans model):**
- Enolate adopts **Z**-geometry (chelated to metal)
- Alkylation occurs from the **face opposite** the oxazolidinone substituent
- Predictable and reliable (>95:5 dr typical)

**Extensions:**
- **Evans syn-aldol:** Z-boron enolate from N-acyloxazolidinone + aldehyde → syn-β-hydroxy
- **Evens anti-aldol:** Use of MgBr₂ with specific enolate geometry
- **Asymmetric acylation** via mixed anhydrides

### 7.4 Sharpless Asymmetric Epoxidation (SAE)

**Applicability:** Primary and secondary **allylic alcohols**.

**Reagents:**
- **SAE (−):** Ti(OiPr)₄ + (−)-DET + TBHP → epoxide with predictable absolute configuration
- **SAE (+):** Ti(OiPr)₄ + (+)-DET + TBHP → enantiomeric epoxide

**Predictive model (Sharpless mnemonic):**
```
Draw the allylic alcohol with OH at bottom.
  ─ If using (+)-DET: epoxide oxygen comes from "top-right" (→ upper face)
  ─ If using (−)-DET: epoxide oxygen comes from "bottom-left" (→ lower face)
```

**Sharpless Asymmetric Dihydroxylation (SAD):**
- AD-mix-α (DHQ derivatives) → diol from **top face**
- AD-mix-β (DHQD derivatives) → diol from **bottom face**

**Sharpless Asymmetric Aminohydroxylation (SAA):**
- Less general, gives β-amino alcohols from alkenes

---

## 8. Ring Synthesis

### 8.1 Dieckmann Condensation (Intramolecular Claisen)

**Pattern:** Cyclic β-keto ester from diester

```
[─(CH₂)n─COOR]₂  →  NaOEt  →  cyclic β-keto ester (n+1 or n+2 ring)
```

**Ring size preference:** 5-, 6-membered rings favored. 3-, 4- strained. 7+ possible but slower.

**Strategy:** Disconnect the β-keto ester C─C bond → open-chain diester.

### 8.2 Diels-Alder Reaction

**Pattern:** Cyclohexene from diene + dienophile

```
    ╱╲         ╱╲
   │  │  +    ║   ║    →    [4+2] cycloaddition
    ╲╱         ╲╱
   diene    dienophile
```

**Retrosynthetic disconnection:** Find the **six-membered ring** with a double bond and trace the "endo" relationship:
- Positions 1,2,3,4 → diene
- Positions 5,6 → dienophile

**Regioselectivity (electron-rich diene + electron-poor dienophile):**
- Normal electron demand: electron-rich diene + electron-poor dienophile
- Inverse electron demand: electron-poor diene + electron-rich dienophile

**Endo rule:** Kinetic endo product predominates (secondary orbital interactions).  
**Stereochemistry:** **Suprafacial** on both components — trans relationships on the dienophile are preserved as cis in the product.

**Hetero-Diels-Alder:**
- Carbonyl as dienophile → dihydropyran
- Imino dienophile → tetrahydropyridine
- Thiocarbonyl → thiapyran

### 8.3 Robinson Annulation

**Pattern:** Cyclohexenone from cyclic ketone + methyl vinyl ketone (MVK)

```
        O                  O
       ║          MVK      ║        O
  ╱──C──╲   ──────────►  ╱──C──╲  ──►  cyclohexenone
  ╲     ╱   (1) Michael   ╲     ╱  (2) Aldol
   ╲───╱                 ╲───╱    condensation
   cyclohexanone         1,5-diketone
```

**Two-step sequence:** Michael addition → intramolecular aldol condensation

**Retrosynthetic disconnect:** 
```
Cyclohexenone ⇒ cyclic ketone + MVK (or equivalent α,β-unsaturated ketone)
```

**Extensions:**
- **Double Robinson annulation:** Build bicyclic systems (hydrindanone, decalone)
- **Wieland-Miescher ketone:** Classic Robinson annulation product (2-methyl-1,3-cyclohexanedione + MVK)

### 8.4 Ring-Closing Metathesis (RCM)

**Pattern:** Cycloalkene from diene

```
    ╱╲   ╱╲          Grubbs 2nd gen       ╱╲
──C═C──C═C──   ───────────────────►   ──C═C──  +  CH₂═CH₂
  1  2   3  4                            1     4
```

**Ring size guide:**

| Ring Size | Feasibility | Notes |
|-----------|------------|-------|
| 5 | Excellent | Most reliable |
| 6 | Excellent | Highly favorable |
| 7 | Good | Grubbs II preferred |
| 8–12 | Good to moderate | Entropic penalty increases |
| >12 | Moderate | Can work with high dilution |
| 3, 4 | Poor | Ring strain, avoid |

**Catalysts:**
- **Grubbs 1st gen:** (PCy₃)₂Cl₂Ru=CHPh — general purpose
- **Grubbs 2nd gen:** (IMes)(PCy₃)Cl₂Ru=CHPh — more active, functional group tolerant
- **Hoveyda-Grubbs:** Chelating isopropoxybenzylidene — air-stable, recyclable
- **Z-selective:** Grubbs catalysts with NHC modifications (Schrock, Hoveyda)

**Cross metathesis (CM):** Intermolecular variant. Predictability by catalyst/substrate matching (Grubbs metathesis guide).

### 8.5 [2+2+2] Cycloaddition

**Pattern:** Benzene or substituted arene from three alkynes

```
R─C≡C─H  +  HC≡C─R'  +  HC≡C─R''   →   [2+2+2]  →  substituted arene
```

**Catalysts:** Co(I), Rh(I), Ni(0), Ru(0) complexes

**Applications:**
- Pyridine synthesis: diyne + nitrile (Co or Rh catalysis)
- Benzene from alkyne trimerization
- Carbocycle construction with regiocontrol

### 8.6 Other Ring-Forming Reactions

| Reaction | Ring Size | Key Bonds Formed | Notes |
|----------|-----------|-----------------|-------|
| Intramolecular aldol | 3–7 | C─C | 5,6-membered preferred |
| Intramolecular Michael | 5–7 | C─C | Common in alkaloid synthesis |
| Intramolecular alkylation | 3–7 | C─C | Via enolate + halide |
| Pauson-Khand | 5 | 2×C─C + C─C═O | Alkyne + alkene + CO, Co₂(CO)₈ |
| Nazarov cyclization | 5 | C─C | Pentadienyl cation → cyclopentenone |
| Ritter-type cyclization | 5,6 | C─N | Nitrile + carbocation |
| Intramolecular Heck | 5,6 | C─C (aryl-vinyl) | Pd-catalyzed, forms exo-trig |

---

## 9. Synthesis Planning & Target Complexity Analysis

### 9.1 Molecular Complexity Metrics

| Metric | Definition | Use |
|--------|-----------|-----|
| **Longest Linear Sequence (LLS)** | Number of steps in the longest linear path from SMs to target | Primary efficiency measure |
| **Step count (total)** | Sum of all steps including convergent branches | Overall resource estimate |
| **Convergence factor** | (Steps if linear) / (Actual steps) | >1.5 = good convergence |
| **Atom economy** | (MW of product) / (MW of all reactants) | Green chemistry metric |
| **Redox economy** | Number of unnecessary oxidation state changes | Lower = better |
| **Protecting group count** | Number of PG installations/removals | Lower = better design |
| **Yield-adjusted step count** | Effective steps = −log(overall yield) / log(0.9) | Accounts for yield |

### 9.2 LLS Estimation — Quick Guide

```
Overall yield = 90% per step → LLS of 10 steps → 35% overall yield
Overall yield = 80% per step → LLS of 10 steps → 11% overall yield
Overall yield = 70% per step → LLS of 10 steps →  3% overall yield
```

**Rule of thumb:** A viable synthesis needs overall yield >5%. LLS >15 steps requires exceptional per-step yields (>90%).

### 9.3 Convergence Planning

```
Linear:  A → B → C → D → E → F → G → H → Target  (8 steps LLS)

Convergent:
       A → B → C ─┐
                   ├→ E → F → Target  (5 steps LLS, 7 total)
       D → G ─────┘
```

**Target:** LLS ≤ 10–12 for practical synthesis. Convergence factor ≥ 1.5.

### 9.4 Synthetic Route Evaluation Checklist

- [ ] All functional groups accounted for in retrosynthesis
- [ ] Stereochemistry at every chiral center has a control strategy
- [ ] Protecting group count minimized
- [ ] No redox unnecessary (no OX → RED → OX cycles)
- [ ] Toxic/reagent availability checked
- [ ] Scale-up feasibility (no column chromatography as sole purification)
- [ ] Convergent where possible
- [ ] LLS ≤ target threshold
- [ ] All intermediates are stable and characterizable

---

## 10. Computer-Aided Retrosynthesis

### 10.1 AiZynthFinder

- **Type:** Template-based, open-source (Python)
- **Approach:** Extends search tree from target using reaction templates (RetroTransformer)
- **Search:** Monte Carlo Tree Search (MCTS) or best-first
- **Scoring:** Stock availability (e.g., eMolecules, PubChem), cost, step count
- **Use case:** Rapid exploration of synthetic routes, integration with custom template libraries
- **Limitation:** Quality depends on template library coverage

### 10.2 RetroSim

- **Type:** Template-based (local similarity approach)
- **Approach:** For a given target, find the most similar known reaction in a database (RMG database by default)
- **Key innovation:** Local similarity matching (not exact SMARTS) → broader coverage
- **Output:** Top-ranked precursor molecules from database precedent
- **Use case:** Finding practical, literature-precedented disconnections

### 10.3 Neural / Machine Learning Approaches

| System | Approach | Strengths | Weaknesses |
|--------|----------|-----------|-----------|
| **Retro* (Coley et al.)** | Neural-guided MCTS (Seq2Seq + policy/value nets) | Explores novel routes | May suggest impractical chemistry |
| **Graph2Edits** | Graph-edit approach | Handles complex edits | Training data dependent |
| **Molecular Transformer** | Seq2Seq (Transformer) | High accuracy on USPTO | Template-level only |
| **LocalRetro** | Template-free, local subgraph matching | Generalizable | Less precise on complex cases |
| **G2Retro** | Graph generation | Handles diverse reactions | Limited interpretability |
| **SynSpace / ASKCOS** (MIT) | Neural + template hybrid | Practical, used in pharma | Requires large compute |
| **IBM RXN for Chemistry** | Seq2Seq + atom mapping | Web-accessible, user-friendly | Limited customizability |

**Practical guidance:**
- Use CASP tools for **inspiration and validation**, not as replacements for chemical judgment
- Template-based tools (AiZynthFinder, RetroSim) are more **reliable** (known chemistry)
- Neural tools are more **creative** but may suggest infeasible routes
- Always verify suggestions with literature precedent and mechanistic reasoning

---

## 11. Worked Examples

### Example 1: Ibuprofen (Simple Pharmaceutical)

**Target:** (S)-2-(4-isobutylphenyl)propanoic acid

```
      COOH
       │
  H₃C─C─H
       │
  ─────╱╲─────
  │    │    │
  │    │    │
  │         CH₂
  │         │
  └──CH₂─CH(CH₃)₂
```

**Retrosynthetic tree:**
```
Ibuprofen
  │  [FGI: nitration → reduction → Sandmeyer]
  │
  ├─► 4-isobutyl-α-methylbenzyl alcohol  (FGI: oxidation → acid)
  │     │  [C─C: alkylation]
  │     │
  │     └─► 4-bromo-isopropylbenzene + MeMgBr/CO₂
  │           │  [C─C: Friedel-Crafts alkylation]
  │           │
  │           └─► Isopropylbenzene (cumene) + isobutylene/AlCl₃
  │                 │  [commercial SM]
  │                 └─► Cumene (commercial)
  │
  └─► Alternative: asymmetric hydrogenation of 2-(4-isobutylphenyl)acrylic acid
        │  [Ru-BINAP, H₂]
        │
        └─► 4-isobutylbenzaldehyde + malonic acid (Knoevenagel)
```

**Forward (industrial Boots process):**
1. Friedel-Crafts acylation of isobutylbenzene with acetic anhydride → p-isobutylacetophenone
2. 1,2-aryl migration (Darzens-type) with NaCN/HCl → ibuprofen nitrile
3. Hydrolysis → ibuprofen

### Example 2: Methyl Jasmonate (1,3-Pattern + E-Geometry)

**Target:** Methyl (1R,2R)-3-oxo-2-(2Z)-2-pentenyl-cyclopentaneacetate

```
        O          COOMe
        ║           │
    ╱──C──╲     H─C─H
   │       │       │
   │   CH═CH        │
   │       │       H
    ╲─────╱
  (cyclopentanone with Z-pentenyl and CH₂COOMe)
```

**Retrosynthesis:**
```
Methyl jasmonate
  │  [C─C: Michael addition to cyclopentenone]
  │
  └─► Cyclopentenone + Z-pentenyl cuprate + CH₂(COOMe)₂
        │                 │
        │                 └─► 1-pentyne → Lindlar → (Z)-1-pentene → functionalization
        │
        └─► Cyclopentadiene → selective reduction
```

### Example 3: (R)-Warfarin (Coumarin, 1,3-Disconnection)

**Target:** 4-hydroxy-3-(3-oxo-1-phenylbutyl)-2H-chromen-2-one

```
Retrosynthesis:
Warfarin
  │  [C─C: Michael addition]
  │
  └─► 4-hydroxycoumarin + benzylideneacetone (PhCH═CHCOCH₃)
        │                      │
        │                      └─► [Aldol: benzaldehyde + acetone]
        │
        └─► [Knoevenagel: salicylaldehyde + ethyl acetoacetate]
```

### Example 4: Propranolol (Pharmaceutical, β-Blocker)

**Target:** 1-(naphthalen-1-yloxy)-3-(isopropylamino)propan-2-ol

```
Propranolol
  │  [C─O + C─N: epoxide opening]
  │
  └─► 1-naphthol + glycidyl isopropylamine (epoxide)
        │
        └─► 1-naphthol (commercial) + epichlorohydrin + isopropylamine
              [epichlorohydrin + isopropylamine → glycidylamine]
              [then: 1-naphthol + glycidylamine → SN2 opening]
```

### Example 5: Wieland-Miescher Ketone (Robinson Annulation)

**Target:** 8a-Methyl-4,4a,5,6,7,8-hexahydronaphthalene-2(3H)-one

```
Wieland-Miescher ketone
  │  [Robinson annulation: disconnect C1-C6 bond]
  │
  └─► 2-methyl-1,3-cyclohexanedione + methyl vinyl ketone (MVK)
        │                              │
        │                              └─► [commercial or from acetone → Mannich]
        │
        └─► [Michael addition, then intramolecular aldol]
```

**Forward:** 
1. L-Proline catalyzed Robinson annulation (List, 2000): 2-methyl-1,3-cyclohexanedione + MVK → Wieland-Miescher ketone (96% ee)

### Example 6: Caffeine (Heterocycle Building)

**Target:** 1,3,7-Trimethyl-3,7-dihydro-1H-purine-2,6-dione

```
Caffeine
  │  [N-methylation: disconnect N-methyl groups]
  │
  └─► Theobromine (3,7-dimethylxanthine) + Mel → caffeine
        │  [N-methylation at N1]
        │
        └─► 3-Methylxanthine + Mel → theobromine
              │  [ring construction]
              │
              └─► Theophylline synthesis from urea + cyanoacetic acid
                    (Traube synthesis)
                    urea + cyanoacetic acid → cyanoacetylurea → nitrosation → reduction → ring closure → theophylline
```

**Traube synthesis:**
```
Urea + cyanoacetic acid → 6-amino-1,3-dimethyluracil → nitrosation → reduction → ring closure with formic acid → xanthine
```

### Example 7: Oseltamivir (Tamiflu, Complex Pharmaceutical)

**Target:** Ethyl (3R,4R,5S)-4-acetamido-5-amino-3-(pentan-3-yloxy)cyclohex-1-ene-1-carboxylate

```
Oseltamivir
  │  [Key disconnection: Diels-Alder approach (Shibasaki, Corey)]
  │
  └─► 1,3-butadiene derivative + ethyl acrylate derivative
        │  [C─N: azide displacement]
        │
        └─► Cyclohexene carboxylate → azide → reduction → amine
              │  [C─O: SN2 with pentan-3-ol]
              │
              └─► Epoxide opening with 3-pentanol
```

**Notable approaches:**
- **Shibasaki:** Catalytic asymmetric Diels-Alder with a chiral Lewis acid
- **Corey:** Diels-Alder with a chiral auxiliary (Roche ester-derived dienophile)
- **Fukuyama:** Starting from shikimic acid (chiral pool) — shortest route

### Example 8: (R)-Muscone (Macrocyclic Ketone)

**Target:** (R)-3-Methylcyclopentadecanone

```
(R)-Muscone
  │  [Ring closure: acyloin or RCM approach]
  │
  ├─► Approach A: Acyloin condensation
  │     Br(CH₂)₁₂CO(CH₂)₂CH(Br)CH₃  →  Na  →  acyloin → oxidation → muscone
  │       │
  │       └─► [alkylation of ω-bromo ester with chiral electrophile]
  │
  ├─► Approach B: RCM
  │     CH₂═CH(CH₂)₁₁CO(CH₂)CH═C(CH₃)₂  →  Grubbs II  →  oxidation → muscone
  │       │
  │       └─► [alkylation with vinyl groups, RCM, oxidation of enol ether]
  │
  └─► Approach C: Ring expansion from cyclododecanone
        Cyclododecanone + diazomethane → homologated ketone → Baeyer-Villiger → lactone → 
        reaction with organometallic → muscone
```

### Example 9: Camphor (Bicyclic, Chiral Pool)

**Target:** (1R,4R)-1,7,7-Trimethylbicyclo[2.2.1]heptan-2-one

```
Camphor
  │  [FGI: oxidation]
  │
  └─► Borneol (from natural camphor tree or α-pinene)
        │  [Wagner-Meerwein rearrangement from pinene]
        │
        └─► (−)-α-Pinene → H₂SO₄ → rearrangement → camphene → hydrolysis → isoborneol → oxidation → camphor
```

**Key:** Natural abundance of (1R,4R)-camphor from camphor tree. Chiral pool approach.

### Example 10: Paclitaxel (Taxol) Core — B-Ring Construction

**Target:** Taxane AB ring system fragment (8-membered B-ring)

```
AB-Ring fragment
  │  [C─C: oxy-Cope rearrangement → transannular aldol]
  │
  └─► Divinylcyclohexane → oxy-Cope → 8-membered ring enolate → aldol → B-ring
        │
        └─► [Constructed from Robinson annulation product + vinyl Grignard]
```

**Holton approach:**
```
10-deacetylbaccatin III (from yew needles) → side chain attachment (β-lactam method)
```

### Example 11: Aspidospermidine Core (Alkaloid, Ring Synthesis)

**Target:** Pentacyclic aspidosperma alkaloid core

```
Aspidospermidine
  │  [Key: Fischer indole + Michael cascade]
  │
  └─► Tryptamine derivative + secologanin → Pictet-Spengler → strictosidine → 
        transformations → aspidospermidine (biosynthetic-like)
  
  Alternative (Stork, 1968):
  └─► 2-(3-indolyl)ethylamine + cyclopentanone derivative → 
        imine → Mannich → intramolecular Michael → pentacycle
```

### Example 12: L-DOPA (Pharmaceutical, Aromatic Strategy)

**Target:** (S)-2-Amino-3-(3,4-dihydroxyphenyl)propanoic acid

```
L-DOPA
  │  [Chiral pool: start from L-tyrosine or asymmetric synthesis]
  │
  ├─► Chiral pool: L-tyrosine → enzymatic/chemical hydroxylation → L-DOPA
  │
  └─► Asymmetric hydrogenation:
        3,4-dihydroxyphenylacrylic acid → Rh-BINAP, H₂ → L-DOPA
        │
        └─► 3,4-dimethoxybenzaldehyde + malonic acid (Knoevenagel) → cinnamic acid → demethylation
```

### Example 13: Epothilone B Side Chain (Olefin Strategy)

**Target:** (E)-configured thiazole side chain: (E)-2-methyl-4-thiazolebutenoic acid

```
Side chain
  │  [C─C: HWE olefination for E-geometry]
  │
  └─► Thiazole-4-carboxaldehyde + (EtO)₂P(O)CH(Me)COOMe → HWE → E-alkene
        │
        └─► Thiazole-4-carboxaldehyde: from cysteine + α-bromoketone
```

### Example 14: Quinoxaline Derivative (Heterocycle Assembly)

**Target:** 2,3-Diphenylquinoxaline

```
2,3-Diphenylquinoxaline
  │  [C─N: condensation]
  │
  └─► Benzil + o-phenylenediamine  → condensation → quinoxaline
        │                              │
        └─► [C═C disconnect benzil]: 2 × benzoin → 2 × benzaldehyde
              │
              └─► Benzaldehyde (commercial) → benzoin condensation (CN⁻) → benzil (oxidation)
```

### Example 15: Biaryl Coupling — Valsartan Fragment

**Target:** 2'-Cyano-biphenyl-4-carboxylic acid

```
Biphenyl fragment
  │  [C─C: Suzuki-Miyaura coupling]
  │
  └─► 2-Cyanophenylboronic acid + methyl 4-bromobenzoate → Pd(PPh₃)₄, base → coupling
        │                                                    → ester hydrolysis → acid
        │
        ├─► 2-Cyanophenylboronic acid: 2-bromobenzonitrile → B(OH)₂ (Miayura borylation)
        │
        └─► Methyl 4-bromobenzoate: 4-bromobenzoic acid + MeOH, H₂SO₄
```

---

## Quick Reference Cards

### Most Common Disconnections (by frequency of use)

| Rank | Disconnection | Relationship | Forward Reaction |
|------|--------------|-------------|-----------------|
| 1 | Carbonyl α–β C─C | 1,3 | Aldol |
| 2 | Conjugate C─C | 1,4 | Michael |
| 3 | Ester C─C | 1,3 | Claisen |
| 4 | C═C | Olefin | Wittig/HWE |
| 5 | Diene + dienophile C═C | Ring 6 | Diels-Alder |
| 6 | Amine α–β C─C | 1,3 | Mannich |
| 7 | Aryl–aryl C─C | Biaryl | Suzuki |
| 8 | Alkyl C–C | 1,2 | Alkylation of enolate |
| 9 | Ring closure C═C | Variable | RCM |
| 10 | Aromatic C–C | C–C on ring | Friedel-Crafts |

### Protecting Group Decision Tree

```
Need to protect? 
  → Can you reorder synthesis to avoid it? [Yes → avoid PG]
  → [No → need PG]
     → Which groups coexist? [map orthogonal set]
     → Is the PG temporary? [choose mild installation/removal]
     → Scale considerations? [avoid column-only deprotection]
```

### Stereocontrol Priority

1. **Substrate control** (free) — use existing stereocenters
2. **Reagent control** (chiral reagent, stoichiometric) — e.g., CBS reduction
3. **Catalyst control** (asymmetric catalysis) — e.g., Noyori, Sharpless
4. **Auxiliary control** (chiral auxiliary) — e.g., Evans oxazolidinone
5. **Resolution** (last resort) — enzymatic or chemical resolution

---

*This reference is a living document. Cross-reference with L3 tools for structure verification, and L4/L5 for specific reaction conditions and literature precedent.*
