# Organometallic Chemistry — Advanced Reference

> Graduate-level reference. Assumes working knowledge of organic mechanisms and basic inorganic chemistry.

---

## 1. Oxidation States, Electron Counting, and the 18-Electron Rule

### 1.1 Oxidation State Assignment

The oxidation state (OS) of a metal in a complex is assigned by:
1. Removing all ligands as **closed-shell, neutral fragments** (or as anions with their full charge).
2. The residual charge on the metal is its OS.

**Rules of thumb:**
- Neutral 2e donors (CO, PR₃, C₂H₄, NHC, C₅H₅⁻): OS contribution = 0
- Anionic 2e donors (Cl⁻, Br⁻, I⁻, CH₃⁻, H⁻): OS contribution = –1
- η⁵-C₅H₅ (Cp) is treated as Cp⁻: OS contribution = –1
- η⁶-C₆H₆ is treated as neutral benzene: OS contribution = 0

| Complex | Metal OS | Calculation |
|---|---|---|
| [Fe(CO)₅] | 0 | Fe⁰ + 5×(CO) |
| [W(CO)₆] | 0 | W⁰ + 6×(CO) |
| [Mn(CO)₅Cl] | +1 | Mn⁺¹ + 5×(CO) + Cl⁻ |
| Cp₂Fe (ferrocene) | +2 | Fe²⁺ + 2×Cp⁻ |
| Pd(PPh₃)₄ | 0 | Pd⁰ + 4×PPh₃ |
| Cp₂ZrCl₂ | +4 | Zr⁴⁺ + 2×Cp⁻ + 2×Cl⁻ |

### 1.2 Electron Counting — Two Methods

#### Covalent (Neutral-Ligand) Method
Count all ligands as neutral, sharing their electrons:
- 2e donors: CO, PR₃, CH₂=CH₂, H• (radical), Cl• (radical), C₅H₅•
- The metal contributes its group number electrons.

**Example: [Mn(CO)₅Cl]**  
Mn (group 7) = 7e; 5×CO = 10e; Cl• = 1e → **18e** ✓

#### Ionic (Donor-Pair) Method
Ligands donate their full lone pair; the metal's electron count = group number – OS.
- 2e donors: CO, PR₃, Cl⁻, H⁻, C₅H₅⁻

**Example: [Mn(CO)₅Cl]**  
OS(Mn) = +1, so Mn contributes 7 – 1 = 6e; 5×CO = 10e; Cl⁻ = 2e → **18e** ✓

### 1.3 Ligand Electron Contributions

| Ligand Type | Examples | Electrons Donated | hapticity |
|---|---|---|---|
| 2e, L-type | CO, PR₃, CN⁻, NHC, pyridine, H₂ | 2 | η¹ |
| 1e, X-type radical | Cl•, Br•, CH₃• | 1 | η¹ |
| 2e, X-type anionic | Cl⁻, CH₃⁻, H⁻, acetylacetonate⁻ | 2 | η¹ |
| η²-olefin | CH₂=CH₂, norbornene | 2 | η² |
| η³-allyl | C₃H₅⁻ | 4 | η³ |
| η⁴-diene | butadiene | 4 | η⁴ |
| η⁵-cyclopentadienyl | Cp⁻, Cp*⁻ | 6 | η⁵ |
| η⁶-arene | benzene, mesitylene | 6 | η⁶ |

### 1.4 The 18-Electron Rule

Stable complexes tend to have 18 valence electrons (filled s + p + d shell). This is the analog of the octet rule for transition metals.

**Strong obeyers:** Group 6–10 mid-row metals with π-acceptor ligands (CO, PR₃).
**Exceptions:**
- d⁸ square-planar complexes: [RhCl(PPh₃)₃] (Wilkinson's, 16e), Pd(II) complexes, Pt(II) complexes — stabilized by the large crystal field splitting of the square-planar geometry.
- Early metals (Groups 3–5): often electron-deficient, e.g., Cp₂TiCl₂ (16e), Cp₂ZrCl₂ (16e).
- High-spin complexes with weak-field ligands.
- Bulky ligands that prevent coordination saturation (steric protection).

**Practical utility:** Predicting ligand substitution behavior. 18e complexes are substitutionally inert (dissociative); 16e complexes are coordinatively unsaturated and reactive toward oxidative addition and ligand binding.

---

## 2. Main Group Organometallics

### 2.1 Grignard Reagents (RMgX)

**Preparation:** R–X + Mg → RMgX (ether, reflux). Active Mg surface critical; iodine or 1,2-dibromoethane as initiator. R = primary > secondary >> tertiary. Aryl/vinyl halides require activated Mg (Rieke magnesium) or sonication.

**Structure:** Schlenk equilibrium in ether:
```
2 RMgX  ⇌  R₂Mg + MgX₂
```
Higher-order aggregates (dimers, trimers) via Mg–X bridging. THF solvation breaks aggregates, increasing reactivity.

**Reactivity:**
- Strong nucleophile/base (pKₐ of conjugate acid ~45–50).
- Adds to carbonyls (aldehydes, ketones, esters → tertiary alcohols), epoxides, nitriles.
- **Cannot** add to carboxylic acids (acid-base deprotonation dominates).
- With CO₂ → carboxylic acids.
- **Cross-coupling (Kumada):** RMgX + R'–X → R–R' (Ni or Pd catalysis).

**Limitations:** Incompatible with protic/acidic protons (–OH, –NH, –CO₂H), electrophilic functional groups (–CHO, –C≡N, –NO₂). Low chemoselectivity limits complex molecule applications.

### 2.2 Organolithium Reagents (RLi)

**Preparation:** Direct lithium-halogen exchange (R–Br + n-BuLi → RLi + n-BuBr) or transmetalation from Sn, Hg.

**Structure:** Aggregates in ethereal solvents (tetramers in Et₂O, hexamers in hydrocarbon). Solvent-coordinated monomers in THF.

**Reactivity:** More basic and nucleophilic than Grignards (pKₐ of conjugate acid ~50–55).
- Li–halogen exchange (Br > I >> Cl; ipso substitution preferred).
- Directed ortho metalation (DoM): coordination to a directing group (e.g., OMe, CONR₂) followed by deprotonation at ortho position.
- **Gilman reagents (R₂CuLi):** Less basic, undergo 1,4-addition (conjugate addition) to α,β-unsaturated carbonyls; add to acid chlorides; Sₙ2' reactions.

### 2.3 Organozinc Reagents (R₂Zn, RZnX)

**Preparation:** Oxidative addition of Zn(0) to organic halides (direct), or transmetalation (R–Li + ZnX₂ → RZnX + LiX).

**Properties:** Much less reactive than Grignards/organolithiums — compatible with many functional groups (esters, nitriles, ketones). Moderate nucleophilicity.

**Applications:**
- **Negishi coupling:** RZnX + R'–X → R–R' (Pd catalysis). Highly chemoselective; tolerates esters, amides, nitriles, ketones.
- **Reformatsky reaction:** α-haloester + Zn → zinc enolate, which adds to carbonyls → β-hydroxyesters.
- Organozinc halides (RZnX) are more reactive than dialkylzincs (R₂Zn) in cross-coupling.

### 2.4 Organoboron Compounds

**Preparation:**
- **Hydroboration:** BH₃·THF + alkene → R₃B (anti-Markovnikov, syn addition). Disiamylborane (Sia₂BH), 9-BBN for regioselectivity.
- **Miyaura borylation:** Ar–X + B₂pin₂ → Ar–Bpin (Pd catalysis, Pd(dppf)Cl₂, KOAc, dioxane).
- **Matteson homologation:** boronic ester + CH₂Cl₂ + base → homologated boronic ester.

**Structure:** Trigonal planar boron, sp². Boronic esters (R–B(OR')₂) are air-stable, crystalline solids.

**Reactivity:**
- **Suzuki coupling:** Ar–B(OR)₂ + Ar'–X → Ar–Ar' (Pd catalysis). Broadest scope of all cross-couplings. Mechanism: transmetalation of the boronate complex (formed from Ar–B + OH⁻) to Pd(II).
- **Petasis reaction:** Boronic acid + amine + carbonyl → allylic/propargylic amine.
- **Chan–Lam coupling:** Ar–B(OH)₂ + Ar'NH₂ → ArN(H)Ar' (Cu catalysis, oxidative).
- **Matteson homologation:** iterative stereospecific chain elongation.

**Stereochemistry:** Suzuki coupling proceeds with **retention of configuration** at both partners.

### 2.5 Organosilicon Compounds

**Preparation:** Hydrosilylation (H–SiR₃ + alkene/alkyne → R–SiR₃, Pt or Rh catalysis). Grignard + ClSiR₃. Fleming–Tamao oxidation (R–SiR₃ → R–OH).

**Key reactions:**
- **Hiyama coupling:** Ar–SiR₃ + Ar'–X → Ar–Ar' (Pd catalysis, fluoride activation). The fluoride (TBAF, CsF) generates a hypervalent pentacoordinate silicate [Ar–SiR₃F]⁻, which undergoes transmetalation. Requires an electron-withdrawing group on silicon (e.g., –OSiMe₃, –F) for activation.
- **Hosomi–Sakurai reaction:** allylsilanes + aldehydes/ketones under Lewis acid catalysis (TiCl₄, BF₃·OEt₂) → homoallylic alcohols. γ-Selectivity (attack at the allylic terminus).
- **Brook rearrangement:** [1,2]-silyl shift from carbon to oxygen under basic conditions.
- **Fleming–Tamao oxidation:** R–SiR₃ → R–OH via H₂O₂/NaOH/KF (retention of configuration).

---

## 3. Transition Metal Complexes and Metal–Ligand Bonding

### 3.1 Important Ligand Classes

#### Carbon Monoxide (CO)
- Strong σ-donor + strong π-acceptor (backbonding into CO π*).
- IR spectroscopy: ν(CO) inversely correlates with backbonding extent. Lower ν(CO) = more electron density on metal.
- Bridging CO (μ₂-CO): ν ~1850 cm⁻¹ vs terminal ν ~2000–2100 cm⁻¹.
- Toxicity: CO complexes release CO upon exposure to light or oxidants.

#### Phosphines (PR₃)
- σ-donor strength: PMe₃ > P(p-tol)₃ > PPh₃ > P(OPh)₃ > PF₃.
- π-accepting ability: PF₃ > P(OPh)₃ > PPh₃ > PMe₃.
- **Tolman electronic parameter (TEP):** ν(CO) of Ni(CO)₃L — measures electron-donating ability.
- **Tolman cone angle:** sterics. PBu₃ (182°) > PPh₃ (145°) > PMe₃ (118°) > PH₃ (87°).
- Bulky, electron-rich phosphines (PCy₃, PtBu₃) promote reductive elimination.
- Bidentate phosphines: dppe, dppp, dppf, Xantphos, BINAP.

#### Cyclopentadienyl (Cp, C₅H₅⁻)
- 6e donor (η⁵), aromatic. Cp* (pentamethylcyclopentadienyl) is bulkier and more electron-donating.
- Stabilizes high and low oxidation states. "Piano-stool" geometry for CpMLₙ complexes.
- Enables half-sandwich and sandwich complexes (ferrocene).

#### N-Heterocyclic Carbenes (NHCs)
- Strong σ-donor, negligible π-accepting → very strong overall donor.
- Structural types: imidazol-2-ylidene (IMes, IPr), imidazolin-2-ylidene (SIMes), triazolylidene.
- Advantages over phosphines: stronger M–C bond, resistant to oxidation, modular synthesis.
- Applications: Grubbs 2nd gen catalysts, PEPPSI-type Pd precatalysts, Ru/Ir hydrogenation catalysts.

### 3.2 The Dewar–Chatt–Duncanson Model

Describes metal–olefin bonding as a synergistic combination:

1. **σ-donation:** The filled π-orbital of the alkene donates electron density into an empty metal d-orbital (or hybrid).
2. **π-backdonation:** A filled metal d-orbital donates electron density into the empty π* orbital of the alkene.

```
  Metal ←σ donation← Alkene π (filled)
  Metal →π backbonding→ Alkene π* (empty)
```

**Consequences:**
- Strong backdonation lengthens and weakens the C=C bond (lower ν(C=C) in IR).
- Extreme backdonation can lead to oxidative addition of the alkene (metallacyclopropane formation).
- Electron-rich metals and electron-poor alkenes enhance backdonation.
- The same model applies to metal–CO, metal–CO₂, and metal–isocyanide bonding.

**Relevance to catalysis:** Alkene coordination via DCD activates the π-bond toward nucleophilic attack (Wacker oxidation) or migratory insertion (olefin polymerization, hydroformylation).

---

## 4. Fundamental Organometallic Reactions

### 4.1 Oxidative Addition

**General:** Mⁿ + X–Y → Mⁿ⁺²(X)(Y). Metal oxidation state increases by 2; two new M–X bonds form.

**Mechanisms:**
- **Concerted (3-center, 2-electron):** Common for square-planar d⁸ Pd(0)/Pt(0). Stereospecific (retention at both centers for cis; inversion at both for trans). H–H, C–X, Si–H, B–H, O–H.
- **Sₙ2 type:** At carbon of alkyl halides by electron-rich metals. Inversion at carbon. Limited to primary/secondary halides.
- **Radical (SET):** With alkyl halides (especially tertiary), via single-electron transfer. Non-stereospecific. Common for Ni(0).
- **σ-bond metathesis / oxidative addition of H₂:** Concerted for early metals (no formal oxidation state change).

**Reactivity trends:**
- H–I > H–Br > H–Cl > H–F; C–I > C–Br > C–Cl >> C–F (except for electron-poor metals).
- More electron-rich metals react faster.
- Chelating ligands (e.g., dppe) can favor cis-oxidative addition products.

### 4.2 Reductive Elimination

**General:** Mⁿ(X)(Y) → Mⁿ⁻² + X–Y. Reverse of oxidative addition. Decreases oxidation state by 2.

**Key factors:**
- **Oxidation state:** Higher OS favors reductive elimination. Pd(II) > Pd(0) (thermodynamically).
- **Steric congestion:** Bulky ligands promote reductive elimination (relieving steric strain).
- **Geometry:** cis arrangement of X and Y is required. Trans isomers must isomerize first.
- **Electron-donating ligands:** Enhance reductive elimination rates.
- **Order of ease:** C–C ≈ C–H > C–N > C–O > C–X (halogens).

### 4.3 Migratory Insertion

**General:** X and Y ligands (cis) on a metal combine to form a new ligand X–Y, reducing hapticity or coordination number by 1.

**Olefin insertion (migratory insertion into M–X):**
```
M–R  +  CH₂=CH₂  →  M–CH₂CH₂R
```
- Migrating group R (usually alkyl, aryl, H) moves to the coordinated olefin.
- **Regiochemistry:** Markovnikov (R goes to more substituted carbon) for electron-rich metals; anti-Markovnikov for electron-poor metals.
- **Stereospecificity:** Syn addition of M–R across the C=C.

**CO insertion (migratory insertion into M–R → acyl):**
```
M–R  +  CO  →  M–C(O)R
```
- Follows carbonyl coordination. Alkyl migrates to coordinated CO.
- Key step in hydroformylation, methanol carbonylation, and Pd-catalyzed carbonylations.

### 4.4 β-Hydride Elimination

**General:** M–CH₂CH₂R → M–H + CH₂=CHR. Requires a β-hydrogen, syn-periplanar geometry of M–C–C–H.

**Requirements:**
- β-H must be present (no β-H = no elimination, e.g., neopentyl, methyl).
- Syn-coplanar arrangement of M, Cα, Cβ, Hβ.
- Open coordination site on the metal.
- Metal in appropriate oxidation state (usually d⁶–d⁸).

**Strategic use:**
- Chain-walking catalysis (Ni, Pd).
- Wacker oxidation (Pd-catalyzed).
- Can be a pathway for catalyst decomposition.

**Prevention:** Use ligands without β-H (CH₂SiMe₃, –C(Me)₃), chelating groups that prevent syn-periplanar geometry, or substrates lacking β-H.

### 4.5 Transmetalation

**General:** Transfer of an organic group from one metal (M') to another (M):
```
M–X  +  R–M'  →  M–R  +  M'–X
```

**Key factors:**
- The transmetalating group is usually more electronegative/ionic (B, Sn, Zn, Si, Mg).
- The receiving metal (usually Pd, Ni) must have an open coordination site.
- Base often assists by activating the organometallic reagent (e.g., OH⁻ forming a boronate in Suzuki).
- Stereospecific: configuration is preserved at the transferring carbon.

---

## 5. Cross-Coupling Catalysis

### General Catalytic Cycle
```
  LₙM(0)  --oxidative addition-->  LₙM(II)(Ar)(X)
                                          |
  LₙM(0)  <--reductive elimination--  LₙM(II)(Ar)(Ar')
                                          ^
                                    transmetalation
                                          |
                                      Ar'–M'
```

### 5.1 Suzuki–Miyaura Coupling

**Reaction:** Ar–B(OR)₂ + Ar'–X → Ar–Ar'  
**Catalyst:** Pd(PPh₃)₄, Pd(dppf)Cl₂, Pd(OAc)₂ + phosphine; or Ni-based systems.  
**Base:** K₂CO₃, Cs₂CO₃, K₃PO₄, NaOH (forms boronate ArB(OR)₃⁻ for transmetalation).  
**Solvent:** Dioxane/H₂O, toluene/EtOH/H₂O, THF/H₂O.  

**Mechanism highlights:**
1. Oxidative addition of Ar'–X to Pd(0).
2. Base-mediated boronate formation: Ar–B(OR)₂ + OH⁻ → [Ar–B(OR)₂(OH)]⁻ (activated nucleophile).
3. Transmetalation: transfer of Ar to Pd(II), displacing X⁻.
4. Reductive elimination: Ar–Ar' bond formation, regeneration of Pd(0).

**Scope:** Aryl–aryl, aryl–alkenyl, alkyl–alkyl (Ni-catalyzed), heteroaryl couplings. Broadest functional group tolerance of all cross-couplings. Boronic acids/esters are stable, nontoxic, commercially available.

**Limitations:** Homocoupling (protodeboronation), ortho-substituted substrates can be slow, boronic acid instability (protodeboronation of heteroaryl boronic acids).

### 5.2 Negishi Coupling

**Reaction:** RZnX + R'–X → R–R'  
**Catalyst:** Pd(PPh₃)₄, Pd(dba)₂ + phosphine; NiCl₂(dppp).  
**No base required.**  

**Scope:** Aryl–aryl, aryl–alkyl, alkyl–alkyl (including secondary alkyls). Excellent functional group tolerance (esters, amides, nitriles, ketones survive). Organozinc reagents are more reactive than boron and less basic than Grignards.

**Limitations:** Air/moisture sensitivity of organozinc reagents. Limited commercial availability. Competing β-hydride elimination for alkyl–alkyl couplings (mitigated by Ni catalysis with appropriate ligands).

### 5.3 Stille Coupling

**Reaction:** RSnBu₃ + R'–X → R–R'  
**Catalyst:** Pd(PPh₃)₄, Pd₂(dba)₃ + AsPh₃ (often AsPh₃ gives superior rates).  
**Additive:** CuI or LiCl (accelerates transmetalation).  

**Scope:** Aryl–aryl, aryl–alkenyl, enyne synthesis. Extremely tolerant of functional groups. Mild conditions. Stannanes are stable and storable.

**Limitations:** Tin toxicity (organotin compounds are highly toxic and persistent). Homocoupling side reactions. Stoichiometric tin waste. Removal of tin byproducts is challenging.

### 5.4 Heck Reaction

**Reaction:** Ar–X + CH₂=CH–R → Ar–CH=CH–R (substituted alkene)  
**Catalyst:** Pd(OAc)₂ + P(o-tol)₃, Herrmann–Beller palladacycle.  
**Base:** Et₃N, NaOAc, K₂CO₃.  

**Mechanism (simplified):**
1. Oxidative addition of Ar–X to Pd(0).
2. Alkene coordination and migratory insertion (Ar adds to less substituted carbon).
3. **β-Hydride elimination:** syn elimination gives the substituted alkene and Pd(II)–H.
4. Base-mediated reductive elimination of HX, regenerating Pd(0).

**Regioselectivity:** Branched (α-product) favored with electron-rich alkenes and bulky ligands; linear (β-product) favored with electron-deficient alkenes. Ligand control is critical.

**Scope:** Aryl/vinyl halides/triflates + activated/unactivated alkenes. Intramolecular Heck → carbocycles, heterocycles.

### 5.5 Sonogashira Coupling

**Reaction:** Ar–X + HC≡C–R → Ar–C≡C–R  
**Catalyst:** Pd(PPh₃)₂Cl₂ or Pd(PPh₃)₄ (Pd). CuI as co-catalyst.  
**Base:** Et₃N, piperidine, diisopropylamine (also serves as solvent).  

**Mechanism:**
1. Oxidative addition of Ar–X to Pd(0).
2. Cu-assisted: terminal alkyne + base → Cu–acetylide (CuI + RC≡CH + base → RC≡C–Cu).
3. Transmetalation: Cu–acetylide → Pd–acetylide.
4. Reductive elimination: diarylalkyne.

**Copper-free variant:** Use Pd complexes with bulky electron-rich phosphines (e.g., XPhos, SPhos). Important for substrates that undergo Glaser coupling under Cu conditions.

### 5.6 Buchwald–Hartwig Amination

**Reaction:** Ar–X + HNR₂ → Ar–NR₂  
**Catalyst:** Pd₂(dba)₃ or Pd(OAc)₂ + bulky biaryl phosphine ligand (XPhos, SPhos, BrettPhos, RuPhos).  
**Base:** NaOtBu, Cs₂CO₃, K₃PO₄.  

**Mechanism:**
1. Oxidative addition of Ar–X to LnPd(0).
2. Amine deprotonation (by base) → amide.
3. Ligand substitution (X⁻ displaced by amide).
4. Reductive elimination: C–N bond formation.

**Scope:** Primary and secondary amines, anilines, amides, sulfonamides. Aryl chlorides/bromides/triflates. Electrophilic amination using hydroxylamines.

**Key ligand contribution:** Bulky biaryl phosphines (Buchwald ligands) promote reductive elimination of the challenging C–N bond and prevent catalyst decomposition via β-hydride elimination or Pd black formation.

### 5.7 Kumada Coupling

**Reaction:** R–MgX + R'–X → R–R'  
**Catalyst:** Ni(acac)₂, NiCl₂(dppp), Pd(PPh₃)₄.  
**No additional base.**  

**Scope:** First cross-coupling (1967, Kumada; 1972, Corriu). Aryl/alkenyl Grignards with aryl/vinyl halides. High reactivity allows coupling of less activated partners.

**Limitations:** Grignard reagents are highly basic/nucleophilic → limited functional group tolerance. Homocoupling (Wurtz-type). Sensitive to protic and electrophilic functional groups.

### Cross-Coupling Summary Table

| Coupling | Organo- Reagent | Metal Source | Base | Key Advantage | Key Limitation |
|---|---|---|---|---|---|
| Suzuki | B(OR)₂ | B₂pin₂, ArB(OH)₂ | Yes (OH⁻) | Broadest scope, nontoxic | Protodeboronation |
| Negishi | ZnX | RZnX | No | Excellent FG tolerance | Air-sensitive reagents |
| Stille | SnBu₃ | RSnBu₃ | No | Very mild conditions | Tin toxicity |
| Heck | Alkene | C=C | Yes (amine) | C=C bond formation | Regiocontrol |
| Sonogashira | Alkyne | HC≡CR | Yes (amine) | Alkyne synthesis | Glaser homocoupling |
| Buchwald–Hartwig | Amine | HNR₂ | Yes (tBuO⁻) | C–N bond formation | Sensitive to sterics |
| Kumada | MgX | RMgX | No | High reactivity | Poor FG tolerance |

---

## 6. Olefin and Alkyne Metathesis

### 6.1 Olefin Metathesis — Mechanism

**Chauvin mechanism** (metal carbene chain reaction):

```
M=CHR  +  CH₂=CH₂  ⇌  [cyclobutane transition state]  ⇌  M=CH₂  +  CH₂=CHR
```

1. [2+2] cycloaddition of metal alkylidene with olefin → metallacyclobutane.
2. Cycloreversion → new metal alkylidene + new olefin.

### 6.2 Catalyst Systems

#### Grubbs Catalysts (Ru-based)
- **Grubbs 1st gen:** (PCy₃)₂Cl₂Ru=CHPh. Tolerates many functional groups; moderate activity.
- **Grubbs 2nd gen:** (IMes)(PCy₃)Cl₂Ru=CHPh. NHC replaces one PCy₃ → dramatically increased activity and stability. Catalyst of choice for many applications.
- **Grubbs–Hoveyda (3rd gen):** Chelating benzylidene ether; thermally stable, recyclable, can operate at elevated temperatures.

#### Schrock Catalysts (Mo-based)
- Mo(NAr)(CHCMe₂Ph)(OR')₂ (e.g., Mo(N-2,6-iPr₂C₆H₃)(CHCMe₂Ph)(OCMe(CF₃)₂)₂).
- Much more active than Ru catalysts for sterically demanding substrates.
- Extremely air/moisture sensitive (pyrophoric).
- **Schrock–Hoveyda Mo catalysts with chiral biphenolate ligands** → asymmetric olefin metathesis.

#### Comparison
| Property | Grubbs (Ru) | Schrock (Mo/W) |
|---|---|---|
| Functional group tolerance | Excellent | Moderate |
| Activity (sterically hindered) | Moderate | High |
| Air/moisture stability | Good | Very poor |
| Asymmetric capability | Limited | Excellent |

### 6.3 Types of Olefin Metathesis

- **Cross-metathesis (CM):** Two terminal alkenes → cross-product. Statistical mixture unless one alkene is in excess or one is type II (internal, sterically hindered).
- **Ring-closing metathesis (RCM):** Diene → cycloalkene. Ring size controlled by chain length and dilution. Catalyzed by Grubbs 2nd gen. Backbone of macrocycle synthesis.
- **Ring-opening metathesis polymerization (ROMP):** Strained cycloalkene (norbornene, cyclobutene) → polymer. Living ROMP with Schrock catalysts.
- **Ring-opening cross-metathesis (ROCM):** Strained ring + terminal alkene → functionalized diene.
- **Enyne metathesis:** Alkene + alkyne → 1,3-diene. Syn or anti pathway depending on metal and substitution.

### 6.4 Alkyne Metathesis

**Catalysts:** Mo-based (Schrock-type) with silanols; W-based systems. Mechanism: metal alkylidyne (M≡CR) + alkyne → metallacyclobutadiene → new alkyne + new metal alkylidyne.

**Applications:** Macrocycle synthesis, dynemicin core, annulene synthesis. Less developed than olefin metathesis due to catalyst sensitivity.

---

## 7. C–H Activation

### 7.1 General Considerations

C–H bond dissociation energies: 85–110 kcal/mol. Direct activation without prefunctionalization is atom-economical but requires:
- A metal center capable of C–H cleavage.
- A thermodynamic or kinetic driving force (chelation, reductive elimination, β-hydride elimination, etc.).

### 7.2 Directed C–H Activation

A coordinating directing group (DG) binds the metal, bringing it into proximity of a specific C–H bond.

**Common directing groups:** Pyridine, amides, oxazolines, carboxylic acids (as carboxylates), ketones (via enolization), imines, ureas, 8-aminoquinoline, picolinamide.

**General mechanism:**
```
Substrate-DG + LₙM → DG-coordinated M complex → C–H activation (cyclometallation)
→ functionalization (oxidative addition, insertion, reductive elimination)
```

**Palladium(II) systems (Pd(OAc)₂):**
- Pd(II)-catalyzed arylation (Fujiwara–Moritani): Ar–H + Ar'–X → Ar–Ar' (with oxidant).
- Pd(II)-catalyzed acetoxylation, alkoxylation, amination.
- **Mechanism:** Pd(II) C–H activation (concerted metalation–deprotonation, CMD) → Pd(II)–Ar + HOAc → oxidation to Pd(IV) or external electrophile trapping → reductive elimination.

**Ruthenium systems (RuCl₂(p-cymene))₂):**
- C–H alkenylation, alkylation, arylation.
- Often proceeds through Ru(0)/Ru(II) or Ru(II)/Ru(IV) cycles.
- Carboxylate-assisted CMD mechanism.

**Iridium systems (Cp*Ir(III)):**
- **Bidentate directing groups (8-aminoquinoline, picolinamide)** give high regioselectivity.
- Cp*Ir(III) catalyzes C–H borylation (with B₂pin₂), amidation, alkylation.
- Ir(I)/Ir(III) cycles for undirected borylation.

### 7.3 Undirected C–H Activation

No directing group; selectivity driven by electronic or steric factors.

**Key examples:**
- **Iridium-catalyzed C–H borylation** (Cp*Ir(cod) or [Ir(COD)OMe]₂ + bipyridine): Ir(I) → Ir(III) oxidative addition into C–H; borylation via σ-bond metathesis with B₂pin₂. Regioselectivity: steric control (borylation at least hindered position: meta > ortho > para for electron-rich arenes).
- **Palladium-catalyzed C–H functionalization** with transient directing groups (e.g., imines formed in situ from aldehydes and amino acid auxiliaries).
- **Photoredox C–H functionalization:** H-atom abstraction by radical species followed by radical capture on metal.

### 7.4 Mechanistic Pathways for C–H Activation

| Pathway | Description | Common Metals |
|---|---|---|
| CMD (Concerted Metalation–Deprotonation) | Metal inserts into C–H with internal base | Pd(II), Ru(II) |
| Oxidative addition | M(0) + C–H → M(II)(H)(C) | Ir(I), Rh(I), Pd(0) |
| σ-Bond metathesis | 4-center transition state | Early metals, d⁰ |
| Electrophilic substitution (SEAr) | Electrophilic metal attacks aromatic ring | Pd(II) (hard substrates) |
| H-atom abstraction | Radical C–H cleavage | Fe, Cu (photoredox) |

---

## 8. Asymmetric Organometallic Catalysis

### 8.1 Chiral Ligand Classes

#### Bisphosphines
- **BINAP (2,2'-bis(diphenylphosphino)-1,1'-binaphthyl):** Axial chirality. Atropisomeric. Applications: Noyori asymmetric hydrogenation, Takaya hydrogenation.
- **DuPhos, BPE (bisphospholane):** C₂-symmetric, small bite angle. Rh-catalyzed hydrogenation of dehydroamino acids.
- **MeO-BIPHEP, SegPhos:** Tunable dihedral angles. High enantioselectivity in Rh/Ir hydrogenation.
- **DIPAMP:** Historic ligand (Monsanto L-DOPA process).

#### Phosphinooxazolines (PHOX)
- P,N-bidentate, modular. Applications: Ir-catalyzed allylic substitution, Pd-catalyzed α-arylation.

#### NHCs (Chiral)
- Chiral imidazolin-2-ylidenes (e.g., chiral SIMes derivatives). Applications: Cu-catalyzed β-borylation, Rh-catalyzed hydrogenation.

#### Salen and Porphyrins
- Mn(salen) for Jacobsen epoxidation. Co(salen) for hydrolytic kinetic resolution.

#### Chiral Dienes
- (E,E)- or (E,Z)-1,3-dienes (e.g., VAPOL, VAPHA-derived). Rh-catalyzed asymmetric conjugate addition, 1,4-addition of arylboronic acids.

### 8.2 Key Asymmetric Transformations

**Asymmetric hydrogenation (Noyori):**
- Ru(BINAP)(OAc)₂ or Ru(BINAP)Cl₂ + H₂ → reduction of β-keto esters, α,β-unsaturated carboxylic acids.
- **Diamine-ligand bifunctional catalysis:** Ru–BINAP–diamine → H₂ heterolytic cleavage (Ru–H, N–H), 6-membered transition state delivers H⁻ and H⁺ to substrate. Up to >99.9% ee.

**Asymmetric allylic substitution (Tsuji–Trost):**
- Pd(PPh₃)₄ + chiral phosphine/oxazoline ligand.
- Allylic acetate/carbonate + nucleophile (malonate, amine) → substituted product with control of regiochemistry and enantioselectivity.
- Ionizable leaving groups preferred (carbonate > acetate > halide).

**Asymmetric conjugate addition:**
- Rh(acac)(C₂H₄)₂ + chiral phosphine (BINAP, Ph-BPE) + ArB(OH)₂ → 1,4-addition to enones. β-Aryl carbonyl compounds with high ee.

**Asymmetric olefin metathesis:**
- Mo-based Schrock catalysts with chiral biphenolate/silanolate ligands → enantioselective RCM, desymmetrization.
- Ru-based catalysts with chiral NHCs (Grubbs–Hoveyda type) → moderate ee.

**Asymmetric C–H activation:**
- Chiral carboxylic acids as co-catalysts (mono-N-protected amino acids, MPAA: Ac-Phe-OH, Ac-Leu-OH) with Pd(OAc)₂ → enantioselective C–H arylation/alkylation.
- Chiral cyclopentadienyl ligands (Cp* derivatives with chiral substituents) on Rh/Co/Ir.

---

## 9. Worked Examples with Mechanisms

### Example 1: Electron Counting — [RhCl(PPh₃)₃] (Wilkinson's Catalyst)

**Ionic method:**  
OS(Rh) = +1 (Cl⁻ gives –1, 3×PPh₃ = 0, overall neutral → Rh = +1)  
Rh⁺ = group 9 – 1 = 8e  
3×PPh₃ = 6e; 1×Cl⁻ = 2e  
Total = 8 + 6 + 2 = **16e** (square planar d⁸ exception)

**Covalent method:**  
Rh = 9e; 3×PPh₃ = 6e; Cl• = 1e  
Total = 9 + 6 + 1 = **16e** ✓

This 16e complex readily binds a substrate (alkene, H₂), explaining its catalytic activity.

---

### Example 2: Suzuki Coupling — 4-Bromoacetophenone + Phenylboronic Acid

```
Pd(PPh₃)₄  →  Pd(0)(PPh₃)₂  (dissociation)

Step 1: Oxidative addition
Pd(0)(PPh₃)₂ + Br–C₆H₄–COMe  →  trans-(PPh₃)₂Pd(II)(C₆H₄COMe)(Br)

Step 2: Isomerization
trans → cis (required for reductive elimination)

Step 3: Transmetalation
cis-(PPh₃)₂Pd(C₆H₄COMe)(Br) + PhB(OH)₃⁻ (from PhB(OH)₂ + OH⁻)
→ cis-(PPh₃)₂Pd(C₆H₄COMe)(Ph) + B(OH)₃ + Br⁻

Step 4: Reductive elimination
cis-(PPh₃)₂Pd(C₆H₄COMe)(Ph)  →  C₆H₄COMe–Ph  +  Pd(0)(PPh₃)₂

Product: 4-phenylacetophenone
```

---

### Example 3: Heck Reaction — Iodobenzene + n-Butyl Acrylate

```
Pd(OAc)₂ + 2P(o-tol)₃ → Pd(0)(P(o-tol)₃)₂ (reduction in situ)

Step 1: Oxidative addition
Pd(0)L₂ + Ph–I → trans-L₂Pd(II)(Ph)(I) → cis-L₂Pd(II)(Ph)(I)

Step 2: Olefin coordination
cis-L₂Pd(Ph)(I) + CH₂=CHCO₂(n-Bu) → cis-L₂Pd(Ph)(I)(η²-CH₂=CHCO₂nBu)

Step 3: Migratory insertion (syn)
Ph migrates to terminal (less substituted) carbon of acrylate:
→ L₂Pd(I)(CH₂CH(Ph)CO₂nBu)

Step 4: β-Hydride elimination (syn)
L₂Pd(I)(CH₂CH(Ph)CO₂nBu) → (E)-PhCH=CHCO₂nBu + L₂Pd(II)(H)(I)

Step 5: Reductive elimination
L₂Pd(H)(I) + Et₃N → L₂Pd(0) + Et₃NH⁺I⁻

Product: (E)-n-butyl cinnamate
```

---

### Example 4: Stille Coupling — Vinyltributylstannane + 4-Iodotoluene

```
Pd(PPh₃)₄ → Pd(0)(PPh₃)₂ (active species)

Step 1: Oxidative addition
Pd(0)(PPh₃)₂ + p-CH₃C₆H₄–I → cis-(PPh₃)₂Pd(II)(C₆H₄CH₃)(I)

Step 2: Transmetalation (CuI-assisted)
cis-(PPh₃)₂Pd(C₆H₄CH₃)(I) + CH₂=CHSnBu₃
→ cis-(PPh₃)₂Pd(C₆H₄CH₃)(CH=CH₂) + Bu₃SnI

Step 3: Reductive elimination
cis-(PPh₃)₂Pd(C₆H₄CH₃)(CH=CH₂) → p-tolyl–CH=CH₂ + Pd(0)(PPh₃)₂

Product: 4-vinyltoluene (styrene derivative)
```

---

### Example 5: Ring-Closing Metathesis (RCM) — Diethyl Diallylmalonate

```
Substrate: CH₂=CH–CH₂–C(CO₂Et)₂–CH₂–CH=CH₂

Catalyst: Grubbs 2nd gen (IMes)(PCy₃)Cl₂Ru=CHPh

Step 1: Initiation
(PCy₃) dissociation → (IMes)Cl₂Ru=CHPh (14e, active)

Step 2: Metathesis with first alkene
(IMes)Cl₂Ru=CHPh + CH₂=CH–CH₂–[C] → [metallacyclobutane]
→ (IMes)Cl₂Ru=CH–CH₂–CH₂–[C] + PhCH=CH₂ (styrene, byproduct)

Step 3: Cyclization (intramolecular metathesis)
(IMes)Cl₂Ru=CH–CH₂–CH₂–[C] + CH₂=CH–CH₂–[C] (same molecule, second alkene)
→ [metallacyclobutane] → (IMes)Cl₂Ru=CH₂ + cyclopentene product

Product: 3,3-diethoxycarbonylcyclopentene
Ring size: 5-membered (favored)
```

---

### Example 6: Negishi Coupling — Alkyl–Alkyl (n-Hexylzinc Bromide + 1-Bromooctane)

```
Catalyst: Pd₂(dba)₃ + PCy₃ (bulky electron-rich phosphine prevents β-H elimination)

Step 1: Oxidative addition
Pd(0)L₂ + C₈H₁₇–Br → L₂Pd(II)(C₈H₁₇)(Br)

Step 2: Transmetalation
L₂Pd(C₈H₁₇)(Br) + n-C₆H₁₃ZnBr → L₂Pd(C₈H₁₇)(C₆H₁₃) + ZnBr₂

Step 3: Reductive elimination
L₂Pd(C₈H₁₇)(C₆H₁₃) → n-C₁₄H₃₀ (tetradecane) + Pd(0)L₂

Key: PCy₃'s bulk promotes rapid reductive elimination before β-H elimination can occur.
Product: tetradecane
```

---

### Example 7: Buchwald–Hartwig Amination — 4-Bromoanisole + Morpholine

```
Catalyst: Pd₂(dba)₃ (2.5 mol%) + XPhos (6 mol%)
Base: NaOtBu, Solvent: toluene, 100°C

Step 1: Generation of L₁Pd(0) or L₂Pd(0)
Pd₂(dba)₃ + 4 XPhos → 2 (XPhos)₂Pd(0)

Step 2: Oxidative addition
(XPhos)Pd(0) + p-CH₃OC₆H₄–Br → (XPhos)Pd(II)(C₆H₄OMe)(Br)

Step 3: Deprotonation and coordination of amine
Morpholine + NaOtBu → morpholinide (N⁻)
(XPhos)Pd(C₆H₄OMe)(Br) + morpholinide → (XPhos)Pd(C₆H₄OMe)(N-morpholine) + Br⁻

Step 4: Reductive elimination
(XPhos)Pd(C₆H₄OMe)(N-morpholine) → p-CH₃OC₆H₄–N(morpholine) + Pd(0)(XPhos)

Product: N-(4-methoxyphenyl)morpholine
```

---

### Example 8: Hydroformylation — 1-Hexene + CO/H₂ (Rh Catalyst)

```
Catalyst precursor: Rh(acac)(CO)₂ + excess PPh₃ → HRh(CO)(PPh₃)₃

Cycle:
1. Olefin coordination: HRh(CO)(PPh₃)₂ + CH₂=CH–C₄H₉ → HRh(CO)(PPh₃)₂(η²-hexene)
2. Migratory insertion (hydride migrates to coordinated alkene):
   → Rh(CO)(PPh₃)₂(CH₂CH₂C₆H₁₃)  [linear alkyl, anti-Markovnikov with PPh₃]
   [OR branched: Rh(CO)(PPh₃)₂(CH(CH₃)C₅H₁₁) with less ligand]
3. CO coordination: → Rh(CO)₂(PPh₃)₂(alkyl)
4. Migratory insertion (alkyl migrates to CO → acyl):
   → Rh(CO)(PPh₃)₂(C(O)CH₂CH₂C₆H₁₃)
5. Oxidative addition of H₂: → Rh(H)₂(CO)(PPh₃)₂(C(O)alkyl)
6. Reductive elimination: → heptanal (C₇H₁₄O) + HRh(CO)(PPh₃)₂

Ligand effects: Excess PPh₃ favors linear:branched > 10:1. Bulky phosphites favor branched.
```

---

### Example 9: Directed C–H Activation — Pd-Catalyzed Arylation of 2-Phenylpyridine

```
Substrate: 2-phenylpyridine (pyridine N as directing group)
Arylating agent: Ph–I
Catalyst: Pd(OAc)₂ (10 mol%)
Additive: AgOAc (oxidant/silver salt), K₂CO₃
Solvent: DMF, 120°C

Mechanism:
1. DG coordination: 2-phenylpyridine + Pd(OAc)₂ → N-coordinated Pd(II) complex
2. CMD cyclometallation: Pd inserts into ortho C–H (of the phenyl ring) via acetate-assisted
   deprotonation → 5-membered palladacycle + HOAc
3. Oxidative addition: palladacycle + Ph–I → Pd(IV)(C)(C₆H₅)(I)(OAc)
4. Reductive elimination: → 2-(2-phenylphenyl)pyridine + Pd(II)(I)(OAc)
5. Anion exchange with AgOAc: → Pd(OAc)₂ (regenerated)

Product: 2-(2-biphenylyl)pyridine (ortho-arylated product at the phenyl ring)
```

---

### Example 10: Wacker Oxidation — Ethylene → Acetaldehyde

```
Catalyst: PdCl₂, CuCl₂
Oxidant: O₂ (air)
Medium: aqueous HCl

Mechanism:
1. Coordination: PdCl₄²⁻ + C₂H₄ → [PdCl₃(C₂H₄)]⁻ + Cl⁻
2. Nucleophilic attack (anti): H₂O attacks coordinated ethylene (Markovnikov):
   → [PdCl₂(CH₂CH₂OH)]⁻ + 2Cl⁻
3. β-Hydride elimination: → PdCl₂ + CH₃CHO (acetaldehyde)
4. Pd(0) reoxidation: Pd(0) + 2CuCl₂ → PdCl₂ + 2CuCl
5. Cu(I) reoxidation: 2CuCl + 2HCl + ½O₂ → 2CuCl₂ + H₂O

Net: C₂H₄ + ½O₂ → CH₃CHO
```

---

### Example 11: Sonogashira Coupling — 4-Iodobenzonitrile + Phenylacetylene

```
Catalyst: Pd(PPh₃)₂Cl₂ (2 mol%) + CuI (4 mol%)
Base: Et₃N (solvent), RT

Step 1: Reduction to Pd(0)
Pd(II) + amine → Pd(0)L₂ + oxidized amine

Step 2: Oxidative addition
Pd(0)L₂ + NC–C₆H₄–I → L₂Pd(II)(C₆H₄CN)(I)

Step 3: Copper acetylide formation
PhC≡CH + Et₃N + CuI → PhC≡C–Cu + Et₃NH⁺I⁻

Step 4: Transmetalation
L₂Pd(C₆H₄CN)(I) + PhC≡C–Cu → L₂Pd(C₆H₄CN)(C≡CPh) + CuI

Step 5: Reductive elimination
L₂Pd(C₆H₄CN)(C≡CPh) → NC–C₆H₄–C≡C–Ph + Pd(0)L₂

Product: 4-(phenylethynyl)benzonitrile
```

---

### Example 12: Noyori Asymmetric Hydrogenation — Methyl Acetoacetate

```
Catalyst: Ru(S)-BINAP(OAc)₂ (or Ru(S)-BINAPCl₂ + NEt₃)
H₂ pressure: 50–100 atm, MeOH, RT

Substrate: CH₃C(O)CH₂CO₂CH₃

Mechanism (bifunctional):
1. H₂ addition to Ru(II) → Ru(II)(H)₂ (cis dihydride)
2. β-Keto ester coordinates via carbonyl to Ru and H-bond to Ru–H
3. Hydride transfer from Ru–H to carbonyl C (stereodetermining step, dictated by BINAP chirality)
4. Proton transfer from coordinated solvent/OH to carbonyl O
5. Product release: methyl (R)-3-hydroxybutanoate (>99% ee with (S)-BINAP)

Key: Six-membered transition state with simultaneous H⁻ (from Ru) and H⁺ (from H-bond donor) delivery.
```

---

### Example 13: Hiyama Coupling — 4-Bromoacetophenone + (Trimethylsilyl)benzene

```
Catalyst: Pd(PPh₃)₄ (3 mol%)
Activator: TBAF (1.5 equiv, generates pentacoordinate fluorosilicate)
Base: K₂CO₃
Solvent: DMF, 80°C

Step 1: Oxidative addition
Pd(0)L₂ + Br–C₆H₄–COMe → L₂Pd(II)(C₆H₄COMe)(Br)

Step 2: Silicon activation
Ph–SiMe₃ + F⁻ (from TBAF) → [Ph–SiMe₃F]⁻ (pentacoordinate silicate)

Step 3: Transmetalation
L₂Pd(C₆H₄COMe)(Br) + [Ph–SiMe₃F]⁻ → L₂Pd(C₆H₄COMe)(Ph) + Br⁻ + FSiMe₃

Step 4: Reductive elimination
L₂Pd(C₆H₄COMe)(Ph) → 4-phenylacetophenone + Pd(0)L₂

Note: Without electron-withdrawing groups on Si (e.g., –OSiMe₃), transmetalation is very slow.
Enhanced by adding CsF or using vinyl/aryl silanols.
```

---

### Example 14: Ir-Catalyzed C–H Borylation — Mesitylene

```
Catalyst: [Ir(COD)OMe]₂ (1.5 mol%) + dtbpy (4,4'-di-tert-butyl-2,2'-bipyridine, 6 mol%)
Boron source: B₂pin₂ (1.2 equiv)
Solvent: THF, 80°C

Substrate: 1,3,5-trimethylbenzene (mesitylene)

Mechanism:
1. Active catalyst: (dtbpy)Ir(COD) → (dtbpy)Ir(I)(COD) → (dtbpy)Ir(I)(Bpin) after B₂pin₂ reaction
2. Oxidative addition of C–H (sterically controlled):
   (dtbpy)Ir(I)(Bpin) + Ar–H → (dtbpy)Ir(III)(H)(Ar)(Bpin)
   The least hindered C–H (between methyl groups) is attacked
3. Reductive elimination: (dtbpy)Ir(III)(H)(Ar)(Bpin) → Ar–Bpin + (dtbpy)Ir(I)(H)
4. σ-Bond metathesis: (dtbpy)Ir(I)(H) + B₂pin₂ → (dtbpy)Ir(I)(Bpin) + HBpin

Product: 2,4,6-trimethylphenylboronic acid pinacol ester
Regioselectivity: exclusively borylation at the 2-position (least hindered)
```

---

### Example 15: Enyne Metathesis (Alkyne + Alkene → 1,3-Diene)

```
Substrate: allyloxybenzene + terminal alkyne (e.g., 1-hexyne)
Catalyst: Grubbs 2nd gen, (IMes)(PCy₃)Cl₂Ru=CHPh

Mechanism (syn-Enyne Metathesis):
1. Initiation: PCy₃ dissociation → (IMes)Cl₂Ru=CHPh (14e)
2. Cross-metathesis with terminal alkyne:
   Ru=CHPh + HC≡CC₄H₉ → [Ru metallacyclobutene] → Ru=CH–C₄H₉ + PhC≡CH
3. [2+2] Cycloaddition with alkene:
   Ru=CH–C₄H₉ + PhOCH₂CH=CH₂ → [metallacyclobutane]
4. Cycloreversion → 1,3-diene:
   → PhOCH₂CH=CH–CH=CHC₄H₉ + Ru=CH₂

Product: (E,Z)-1-phenoxy-3-hexen-1-yne derivative (1,3-diene)
Stereoselectivity depends on catalyst choice and substitution pattern.
```

---

## Quick Reference: Cross-Coupling Compatibility

| Functional Group | Suzuki | Negishi | Stille | Heck | Sonogashira | Buchwald-Hartwig | Kumada |
|---|---|---|---|---|---|---|---|
| Ester | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Ketone | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✗ |
| Nitrile | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✗ |
| Aldehyde | ~ | ✓ | ✓ | ~ | ~ | ~ | ✗ |
| Free OH | ~ | ~ | ~ | ~ | ~ | ✗ | ✗ |
| Free NH | ~ | ~ | ~ | ~ | ~ | ✓ | ✗ |
| Nitro | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✗ |

✓ = compatible, ~ = depends on conditions, ✗ = generally incompatible

---

## Key Textbooks and References

1. Hartwig, J. F. *Organotransition Metal Chemistry: From Bonding to Catalysis* (2nd ed.). University Science Books.
2. Crabtree, R. H. *The Organometallic Chemistry of the Transition Metals* (7th ed.). Wiley.
3. Miyaura, N.; Suzuki, A. *Chem. Rev.* **1995**, *95*, 2457–2483 (Suzuki coupling review).
4. Fu, G. C. *Acc. Chem. Res.* **2008**, *41*, 1555–1564 (alkyl–alkyl Negishi coupling).
5. Grubbs, R. H. *Handbook of Metathesis* (2nd ed.). Wiley-VCH.
6. Dyker, G. *Angew. Chem. Int. Ed.* **1999**, *38*, 1698–1712 (C–H activation review).
7. Noyori, R. *Angew. Chem. Int. Ed.* **2002**, *41*, 2008–2022 (asymmetric hydrogenation, Nobel Lecture).
