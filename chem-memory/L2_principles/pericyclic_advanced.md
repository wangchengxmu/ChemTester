# Pericyclic Reactions — Advanced Reference

> **Level:** L2 (Graduate) | **Last updated:** 2026-03-31  
> **Prerequisites:** L1 chemistry-core-map, undergraduate organic chemistry  
> **Scope:** Woodward-Hoffmann theory, cycloadditions, electrocyclic reactions, sigmatropic rearrangements, group transfer, orbital analysis, computational methods

---

## 1. Overview & Woodward-Hoffmann Rules

### 1.1 Definition

A **pericyclic reaction** is a concerted reaction in which bond-making and bond-breaking occur synchronously through a single cyclic transition state. No intermediates are formed. Key features:

- **Concerted** — single transition state (TS)
- **Cyclic** — electron flow proceeds in a closed loop
- **Highly stereospecific** — outcome determined by orbital topology

### 1.2 The Woodward-Hoffmann Rules

The orbital symmetry of the transition state determines whether the reaction is **allowed** (thermally or photochemically) or **forbidden**.

#### Classification by Component Count

| Reaction Type | Notation | Bonding Change |
|---|---|---|
| Cycloaddition | [m+n] | Formation of two σ bonds from π components |
| Electrocyclic | (nπe) | Ring closure/opening converting π ↔ σ bonds |
| Sigmatropic | [i,j] | Migration of a σ bond across a π framework |
| Group Transfer | [m+n] | Transfer of a group between π systems |
| Cheletropic | — | Addition/elimination of a group to/from a single atom |

#### The Selection Rules

For a pericyclic reaction involving **q** electrons in total:

| q (total electrons) | Thermal | Photochemical |
|---|---|---|
| 4n | **suprafacial/suprafacial** (or antara/antara) forbidden; allowed via suprafacial/antarafacial | **suprafacial/suprafacial** allowed |
| 4n + 2 | **suprafacial/suprafacial** allowed | **suprafacial/suprafacial** forbidden |

In practice: **thermal 4n systems require antarafacial component** (geometrically constrained for small rings); **photochemical 4n systems flip the selection rule**.

#### Aromatic Transition State Theory (Dewar-Zimmerman)

An equivalent formulation: the transition state is **Hückel aromatic** (Möbius aromatic) → allowed (forbidden).

- **Hückel topology** (even number of phase inversions, including 0): 4n+2 electrons → aromatic → **thermal allowed**
- **Möbius topology** (odd number of phase inversions): 4n electrons → aromatic → **thermal allowed**

### 1.3 Orbital Correlation Diagrams

For any pericyclic reaction, construct the orbital correlation between reactant and product frontier orbitals. The reaction is allowed if occupied orbitals of reactants correlate with occupied orbitals of products (no symmetry-imposed barrier).

---

## 2. Cycloadditions

### 2.1 General

Cycloadditions are [m+n] reactions where m and n π-electrons from two (or more) components combine to form a cyclic product with two new σ bonds. The classification:

- **Suprafacial (s)** on a component: new bonds form on the same face of the π system
- **Antarafacial (a)** on a component: new bonds form on opposite faces

The notation [πm_s + πn_s] denotes suprafacial on both components.

### 2.2 [4+2] Cycloaddition — Diels-Alder Reaction

#### Overview

```
Diene (4π) + Dienophile (2π) → Cyclohexene
```

**Thermally allowed** (6π = 4(1)+2, suprafacial on both components). One of the most important reactions in organic synthesis.

**SMILES example:**  
`C=CC=C` + `C#C` → cyclohexene (but-1,3-diene + ethyne)

#### Regioselectivity

Controlled by orbital coefficients at the terminal positions of the diene and dienophile:

- **Normal electron demand (NED):** Electron-rich diene + electron-poor dienophile (e.g., EWG on dienophile). FMO: HOMO(diene)–LUMO(dienophile) interaction dominant.
  - Largest coefficients of HOMO(diene) at C1 and C4; largest coefficients of LUMO(dienophile) at the termini adjacent to EWG.
  - **Regio rule:** "ortho" or "para" alignment of EWG and EDG → **ortho product favored** for unsymmetrical systems.
  
- **Inverse electron demand (IED):** Electron-poor diene + electron-rich dienophile (e.g., cyano-diene + enol ether). FMO: LUMO(diene)–HOMO(dienophile).

**Example:**  
Butadiene + acrolein (`C=CC=C` + `O=CC=C`):  
- HOMO(butadiene) coefficients: C1 > C4 (both large, similar)  
- LUMO(acrolein) coefficients: β-carbon > α-carbon (relative to CHO)  
- **Ortho product** (CHO adjacent to C2 of cyclohexene) is major

#### Stereoselectivity — Endo vs Exo (Alder Endo Rule)

The **endo approach** places the electron-withdrawing substituent of the dienophile under the diene π system, maximizing **secondary orbital interactions** (see §6.1).

```
Endo:  suprafacial, substituent points toward diene π system → KINETIC product
Exo:   suprafacial, substituent points away → THERMODYNAMIC product
```

- Endo is typically favored kinetically (lower ΔH‡) but may be thermodynamically less stable
- Under thermal conditions, endo/exo ratios depend on temperature (higher T → more exo)
- Lewis acid catalysis can increase endo selectivity

#### Stereospecificity

**cis-Dienophile → cis-substituted cyclohexene**  
**trans-Dienophile → trans-substituted cyclohexene** (requires transoid dienophile to approach; geometrically constrained, often requires acyclic trans-alkenes with electron-withdrawing groups to lock conformation)

#### Frontier Molecular Orbital (FMO) Analysis

For NED Diels-Alder:

```
HOMO(diene):     ψ2 = 0.60 ψ1 - 0.37 ψ2 + 0.37 ψ3 - 0.60 ψ4  (simplified)
LUMO(dienophile): ψ* = α + β carbon coefficients (EWG increases β coefficient)
```

The energy gap ΔE = E_LUMO(dienophile) - E_HOMO(diene) determines reaction rate. Smaller gap → faster reaction.

#### Diene Reactivity

| Diene | Reactivity (NED) | Notes |
|---|---|---|
| Cyclopentadiene | Very high | Fixed s-cis, high-lying HOMO |
| Danishefsky's diene | High | Electron-rich, gives enones after hydrolysis |
| 1,3-Butadiene | Moderate | Requires s-cis conformation |
| Furan | Low (reversible) | 6π aromaticity loss; used in DA-retro-DA strategies |

#### Dienophile Reactivity (NED)

Rate enhancement by electron-withdrawing groups: CHO > COR > COOR > CN > CO₂R > Ph > H

Lewis acid coordination to carbonyl oxygen further lowers LUMO.

### 2.3 [2+2] Cycloaddition

#### Thermal [2+2]

Thermally **forbidden** under suprafacial/suprafacial approach (4π total). However, **suprafacial/antarafacial** [2+2] is allowed but geometrically very constrained.

**Ketene [2+2] cycloadditions** are an important exception:
```
R2C=C=O (ketene) + C=C → cyclobutanone
```
Ketenes have orthogonal π systems (π_C=C and π_C=O), allowing a stepwise or formally allowed [π2s + π2a] pathway.

**SMILES:** `C=C=O` + `C=CC` → oxetanone / cyclobutanone derivative

#### Photochemical [2+2]

**Photochemically allowed** (suprafacial/suprafacial, 4π). One component is excited:

```
[C=C]* + C=C → cyclobutane (via excited state)
```

Applications:
- **Paternò-Büchi reaction:** Carbonyl + alkene → oxetane (n→π* excitation on carbonyl)
- **[2+2] photocycloaddition of enones:** Used extensively in natural product synthesis

**Stereochemical outcome:** The excited alkene approaches suprafacially on both components → **stereospecific**. Configuration of the ground-state alkene is retained.

### 2.4 [3+2] Cycloaddition — 1,3-Dipolar Cycloadditions

**Thermally allowed** (6π = 4n+2, suprafacial on both components).

#### Classification of 1,3-Dipoles

| Dipole | Structure (SMILES-like) | Type |
|---|---|---|
| Nitrone | `[CH2=N+(-O-)]` | allyl anion-type |
| Nitrile oxide | `[-C≡N+-O-]` | propargyl-type |
| Azide | `[-N=N+=N-]` | linear |
| Diazo compound | `[R2C=N+=N-]` | propargyl-type |
| Ozone | `O=O+-O-` | allyl anion-type |

**FMO analysis:**  
- With electron-poor dipolarophile: HOMO(dipole)–LUMO(dipolarophile)  
- With electron-rich dipolarophile: LUMO(dipole)–HOMO(dipolarophile)

**Regioselectivity** follows frontier orbital coefficient matching (same principles as Diels-Alder).

### 2.5 [4+3] Cycloaddition

**Thermally allowed** (7π... actually this involves a 4π diene + 3π oxyallyl cation, proceeding through a stepwise or concerted mechanism). The oxyallyl cation is a 2π+1π system; total electron count is 6π if counting the charged system properly.

In practice, [4+3] cycloadditions are often **stepwise** (Mannich-type) or proceed through a **concerted asynchronous** pathway.

**Example:**  
Furan + oxyallyl cation (from α,α'-dibromoketone + Fe(CO)₅) → 8-oxabicyclo[3.2.1]oct-6-en-3-one

### 2.6 [2+2+2] Cycloaddition

**Thermally allowed** (6π, Hückel aromatic transition state). Three π bonds → benzene ring or derivative.

Catalyzed by transition metals (Co, Ni, Rh, Ru):

```
3 × C≡C → benzene ring  (Co-catalyzed)
C≡C + C≡C + C=O → pyranone (Rh-catalyzed)
```

**Stereochemistry:** Transition metal template controls regioselectivity; otherwise, a mixture of regioisomers is common.

---

## 3. Electrocyclic Reactions

### 3.1 General

Ring closure (or ring opening) of a conjugated polyene involving changes in π and σ bonds. The reaction is classified by the number of π electrons (4n or 4n+2) and the mode of ring closure (conrotatory or disrotatory).

### 3.2 Selection Rules

| Electrons | Thermal Mode | Photochemical Mode |
|---|---|---|
| 4n | **Conrotatory** | **Disrotatory** |
| 4n + 2 | **Disrotatory** | **Conrotatory** |

### 3.3 Conrotatory Ring Closure

Both terminal lobes rotate in the **same direction** (both clockwise or both counterclockwise).

**Example: 1,3,5-Hexatriene → Cyclohexa-1,3-diene** (6π = 4n+2, thermal → disrotatory)

Wait—correction:  
- **4n electrons (thermal → conrotatory):** butadiene → cyclobutene
- **4n+2 electrons (thermal → disrotatory):** hexatriene → cyclohexadiene

#### Butadiene → Cyclobutene (4π, thermal, conrotatory)

```
SMILES: C=CC=C  →  C1CCC1

Thermal: conrotatory
  (E,E)-dimethylbutadiene → trans-3,4-dimethylcyclobutene (via conrotation)
  (E,Z)-dimethylbutadiene → cis-3,4-dimethylcyclobutene (via conrotation)
```

**Stereochemical prediction:**
- Trans-trans diene → conrotatory closure → **trans** dimethyl cyclobutene
- Trans-cis diene → conrotatory closure → **cis** dimethyl cyclobutene

#### Photochemical butadiene → cyclobutene (disrotatory)

The stereochemistry **flips** relative to thermal:
- Trans-trans diene → disrotatory closure → **cis** dimethyl cyclobutene

### 3.4 Disrotatory Ring Closure

Both terminal lobes rotate in **opposite directions** (one clockwise, one counterclockwise).

#### Hexatriene → Cyclohexadiene (6π, thermal, disrotatory)

```
SMILES: C=CC=CC=C  →  C1=CCC=CC1

Thermal: disrotatory
Photochemical: conrotatory
```

**Stereochemistry:**  
With substituents at the termini:
- (E,E)-dimethylhexatriene → thermal disrotatory → **cis**-1,2-dimethylcyclohexadiene (substituents on same face)
- (E,Z)-mixed → depends on specific geometry

### 3.5 Ring Opening

The same selection rules apply in reverse. The stereochemistry of the ring-opened product reveals the mode of opening.

**Biomolecular example:**  
Vitamin D synthesis: photochemical electrocyclic ring opening of 7-dehydrocholesterol → previtamin D₃ (6π, photochemical → conrotatory)

### 3.6 Summary Table

| System | n (electrons) | Thermal | Photochemical |
|---|---|---|---|
| Butadiene ↔ Cyclobutene | 4 | Conrotatory | Disrotatory |
| Hexatriene ↔ Cyclohexadiene | 6 | Disrotatory | Conrotatory |
| Octatetraene ↔ Cyclooctatriene | 8 | Conrotatory | Disrotatory |
| Decapentaene ↔ Cyclodecatetraene | 10 | Disrotatory | Conrotatory |

---

## 4. Sigmatropic Rearrangements

### 4.1 General

Migration of a σ bond adjacent to one or more π systems. Notation [i,j]: a σ bond migrates across a framework of i+j atoms (or i and j atoms, depending on convention).

**Total electrons** = σ bond electrons + π electrons traversed = 2 + (i+j-2) = i+j electrons (for C–C σ bonds).

#### Selection Rules for [i,j] Sigmatropic Rearrangements

The migrating group can move **suprafacially** (s) or **antarafacially** (a) with respect to the π system.

| Total electrons | Thermal allowed |
|---|---|
| 4n | s,a or a,s (one component antarafacial) |
| 4n+2 | s,s or a,a (both same topology) |

### 4.2 [1,3] Sigmatropic Rearrangement

**6 electrons** total (but in practice, the migration of H or C across a 3-carbon framework). Wait—let me recalculate.

For [1,j]: total electrons = 1 (σ bond) + j (π electrons of the allyl system). For [1,3]: 1 + 3 = 4 electrons... No.

**Convention:** [i,j] sigmatropic: i atoms in the migrating group, j atoms in the π system. Total π electrons counted = j for a j-carbon allyl system plus the migrating σ bond = depends on exact formalism.

**Practical approach:** Use the Dewar-Zimmerman method or simply apply:

- **[1,3]-H shift:** 4 electrons total → thermally requires **antarafacial** migration → **geometrically impossible for H** (can't invert in 3-atom span) → **thermally forbidden**  
- **[1,3]-C shift:** Similarly thermally forbidden for suprafacial migration; antarafacial is geometrically very strained

**[1,3]-suprafacial shifts are thermally forbidden and photochemically allowed.**

### 4.3 [1,5] Sigmatropic Rearrangement

**6 electrons total** → thermally **suprafacial allowed**.

```
1,5-H shift in pentadienyl system:
CH2=CH-CH=CH-CH3  →  CH3-CH=CH-CH=CH2  (H migration)
```

**Stereochemistry:** The hydrogen migrates **suprafacially** — retention of configuration at the migrating center. The stereochemistry at the termini is controlled by the suprafacial requirement.

This is an important reaction in the biosynthesis of terpenes (e.g., the conversion of provitamin D intermediates).

### 4.4 [3,3] Sigmatropic Rearrangements

**6 electrons** → thermally allowed, suprafacial on both components. Extremely important class.

#### Cope Rearrangement

1,5-diene ↔ 1,5-diene (isomerization)

```
SMILES: C=CC-CC=C  →  C=CC-CC=C  (degenerate for 1,5-hexadiene)
```

**Transition state:** A **chair-like** six-membered ring (favoured) or **boat-like** (disfavored, ~5-10 kcal/mol higher).

- **Chair TS:** All substituents equatorial → lower energy
- **Boat TS:** Axial interactions → higher energy

**Substituent effects:**
- Electron-donating groups at C3 stabilise the TS (radical-like character)
- Aza-Cope: N at position 3 → lower barrier due to nitrogen's ability to stabilise partial charges

**Oxy-Cope rearrangement:**  
3-hydroxy-1,5-diene rearrangement; the OH at C3 dramatically lowers the barrier (ΔΔG‡ ≈ −5 to −7 kcal/mol) because the product is a δ-keto-alkene after tautomerisation. The **anion-accelerated oxy-Cope** (deprotonated OH) lowers the barrier to <10 kcal/mol (room temperature).

**SMILES:** `C=CC(O)CC=C` (3-hydroxy-1,5-hexadiene) → after rearrangement + tautomerisation → `O=C-CCC=C-C` (hex-5-en-1-one derivative)

#### Claisen Rearrangement

Allyl vinyl ether → γ,δ-unsaturated carbonyl

```
SMILES: C=C-O-C=C  →  O=C-C-C=C-C  (allyl vinyl ether → pent-4-enal)
```

**Transition state:** Chair-like, analogous to Cope.

**Ireland-Claisen:**  
Ester enolate + allylic alcohol → after rearrangement → β,γ-unsaturated acid.  
The enolate geometry (E or Z) controls stereochemistry:
- **E-enolate (Z-OSiR₃, using LDA/silyl chloride):** Z-product (E-alkene)  
- **Z-enolate (E-OSiR₃):** E-product (Z-alkene)  

**Johnson-Claisen:**  
Allylic alcohol + triethyl orthoacetate → β,γ-unsaturated ester

**Carroll Rearrangement (Carroll-Claisen):**  
β-Ketoester allylic ester → β-keto acid + γ,δ-unsaturated ketone (after decarboxylation)

**Eschenmoser-Claisen:**  
Allylic alcohol + N,N-dimethylacetamide dimethyl acetal → γ,δ-unsaturated amide

#### [3,3] Stereochemical Summary

- **Chair TS** → pseudo-equatorial arrangement of large substituents
- **Predict stereochemistry** by drawing the chair TS with all substituents
- **Irreversibility** (Claisen) vs reversibility (Cope) affects product distribution

### 4.5 [2,3] Sigmatropic Rearrangement

**6 electrons** (σ bond + 4 π electrons) → thermally allowed, suprafacial on both components.

#### Wittig Rearrangement

[2,3]-sigmatropic rearrangement of allyl ethers:

```
SMILES: C=C-C-O-CH2-Ph  →  C(-O-)=CH-CH2-CH2-Ph  (simplified)
```

Deoxygenation leads to the carbanion at the α-carbon of the ether, which undergoes [2,3]-shift. Stereochemistry is predictable via a five-membered cyclic TS (envelope geometry).

#### Mislow-Evans Rearrangement

[2,3]-sigmatropic rearrangement of allylic sulfoxides:

```
R-S(=O)-CH2-CH=CH2  →  R-S-CH2-CH=CH-CH3  (allyl sulfenate → allyl sulfoxide)
```

Important in sulfoxide chemistry; highly stereospecific. The chirality at sulfur is inverted.

#### [2,3]-Wittig Rearrangement of Ammonium Ylides

Stevens rearrangement alternative; [2,3]-pathway is favoured over [1,2] when a suitable allyl/benzyl group is present.

### 4.6 [5,5] Sigmatropic Rearrangement

**10 electrons** → thermally allowed (suprafacial/suprafacial, since 10 = 4(2)+2).

Rare but observed in:
- Rearrangements of 1,5,9-decatriene systems
- Some biosynthetic pathways

### 4.7 椅式过渡态 (Chair Transition State)

The **chair transition state** is the preferred geometry for [3,3] sigmatropic rearrangements:

```
        Axial substituents (pseudo-equatorial in TS)
       /                                      \
      /                                        \
   C3 --- C4                                   
  /         \  (TS geometry)                   
C2           C5                               
  \         /                                  
   C1 --- C6                                   
       \                                      /
        \                                    /
```

- All large substituents occupy **pseudo-equatorial** positions
- The chair TS has ~C₂ symmetry
- Boat TS is typically >5 kcal/mol higher and only significant when chair is sterically blocked
- **A-values** can be used to estimate steric preference: t-Bu > i-Pr > Et > Me > H

---

## 5. Group Transfer Reactions

### 5.1 Ene Reaction

The ene reaction involves transfer of an allylic hydrogen (the "ene") to an electron-deficient alkene (the "enophile") with concomitant migration of the double bond and formation of a new C–C bond.

```
SMILES: C/C=C\CH2  +  O=C=O  →  O=C(O)CC=C  (isobutene + CO2 → acid)
```

**Electron count:** 6 electrons → thermally allowed (Hückel aromatic TS).

**Characteristics:**
- Requires an allylic hydrogen (cis to the enophile for suprafacial transfer)
- Stereospecific: geometry of both ene and enophile is preserved
- **Lewis acid catalysis** enhances enophile reactivity (lowers LUMO)

**Examples:**
- Alder-ene reaction: maleic anhydride + ene
- Singlet oxygen ene reaction: ¹O₂ + allylic C–H → allylic hydroperoxide
- Metal-catalyzed ene (e.g., Me₃Al, SnCl₄, Lewis acids)

### 5.2 [1,5] Group Transfer

Transfer of a σ-bonded group (H, SiR₃, etc.) across a pentadienyl system.

### 5.3 Carbene Transfer

Singlet carbenes can undergo concerted addition to alkenes → cyclopropanes. This is formally a [2+1] cycloaddition.

```
:CH2  +  C=C  →  cyclopropane
```

**Singlet carbenes:** Concerted, stereospecific (suprafacial → cis-alkene gives cis-cyclopropane).  
**Triplet carbenes:** Stepwise (diradical), non-stereospecific.

---

## 6. Advanced Topics

### 6.1 Secondary Orbital Interactions (SOI)

In the Diels-Alder endo transition state, the π* orbitals of the dienophile substituent (e.g., C=O of an acrylate) interact with the π system of the diene:

```
     [π* of C=O]
          ↕ (stabilizing overlap)
     [π  of diene]
```

**Effects:**
- Lowers the activation energy of the **endo** approach by ~1-3 kcal/mol
- Does not affect the thermodynamic stability of the product
- More significant with strongly π-accepting substituents (C=O, CN, NO₂)
- Predicted by **Houk's model** (secondary orbital overlap in the TS)

**Computational validation:** Houk (1985) showed via ab initio calculations that removing the secondary orbital interaction (by using saturated substituents) eliminates the endo preference.

### 6.2 Substituent Effects

#### Electronic Effects on Diels-Alder

- **EDG on diene** → raises HOMO → faster NED reaction
- **EWG on dienophile** → lowers LUMO → faster NED reaction
- **Hammett correlations:** ρ values for dienophile substituents are typically positive (electron-withdrawing accelerates)
- **Frontier orbital energy gap** is the dominant factor; substituent effects on activation energy can be correlated with ΔE_FMO

#### Steric Effects

- 1-substituted dienes: Substituent can be pseudo-equatorial (favoured) or pseudo-axial (disfavoured) in the endo/exo TS
- 2-substituted dienes: Steric effects on approach geometry
- Steric bulk can override endo preference → exo product dominates with very bulky substituents

#### Substituent Effects on Cope/Claisen

- **Electron-withdrawing groups** at C1 or C5 of the 1,5-diene destabilise the TS (no developing charge, mainly radical character → EWG destabilises)
- **3-hydroxy group (oxy-Cope):** Acceleration due to product stabilisation (keto form after tautomerisation), not TS stabilisation per se
- **Alkoxy groups at C3:** Modest acceleration via polar effects

### 6.3 Solvent Effects

- **Non-polar solvents** (toluene, benzene, CH₂Cl₂): Standard for pericyclic reactions; minimal solvent participation
- **Lewis acids:** Reduce activation barriers by 5-15 kcal/mol for DA reactions; do NOT change the mechanism (still concerted, but more asynchronous)
- **High pressure:** Favours reactions with negative ΔV‡ (volume of activation); most cycloadditions have ΔV‡ < 0 → accelerated by high pressure
- **Water as solvent:** Accelerates Diels-Alder reactions significantly (hydrophobic effect → enforced hydrophobic association + hydrogen bonding to carbonyl oxygen of dienophile)
- **Microwave irradiation:** Thermal effect mainly; can also induce "non-thermal" effects in some reports (controversial)

### 6.4 Asynchronicity

Many pericyclic reactions are **asynchronous** — the two bond-forming events do not occur simultaneously:

- Diels-Alder with strong EWG on dienophile: Bond to the β-carbon (farther from EWG) forms first → asynchronous TS
- Increasing asynchronicity → more charge-transfer character → greater solvent and substituent effects
- **Limit:** At extreme asynchronicity, the reaction becomes stepwise (zwitterionic or diradical intermediate)

---

## 7. Computational Methods

### 7.1 Benchmarking Pericyclic Reactions

| Method | Typical Error (kcal/mol) | Notes |
|---|---|---|
| B3LYP/6-31G(d) | 3-5 | Popular but underestimates barriers |
| M06-2X/6-311+G(d,p) | 2-3 | Good for thermochemistry + kinetics |
| ωB97X-D/def2-TZVP | 1-2 | Includes dispersion; recommended |
| DLPNO-CCSD(T)/CBS | <1 | Gold standard; computationally expensive |
| CBS-QB3 | 1-2 | Composite method; efficient |
| SCS-MP2 | 2-3 | Better than plain MP2 for pericyclics |

### 7.2 Key Computational Studies

- **Houk (1974-present):** FMO analysis, secondary orbital interactions, DA stereoselectivity
- **Ess & Houk (2015):** Conical intersections in photochemical pericyclic reactions
- **Herges (1994):** Möbius aromatic transition states
- **Grimme:** Dispersion-corrected DFT for steric effects in endo/exo selectivity

### 7.3 Practical Guidelines

1. **Geometry optimisation:** Use B3LYP/6-31G(d) or M06-2X/6-31G(d) for TS searches
2. **Frequency calculation:** Confirm exactly one imaginary frequency; animate it to verify it corresponds to the desired reaction coordinate
3. **IRC (Intrinsic Reaction Coordinate):** Follow the imaginary frequency to connect TS to correct reactant and product minima
4. **Single-point energy:** Use a higher-level method (ωB97X-D/def2-TZVP or DLPNO-CCSD(T)/CBS) on the DFT geometries
5. **Solvation:** SMD or CPCM model for solution-phase energies
6. **NBO analysis:** Quantify secondary orbital interactions, charge transfer
7. **Activation strain model (Distortion/Interaction):** Decompose ΔE‡ into distortion energy (strain to reach TS geometry) and interaction energy (stabilising orbital interactions in the TS)

### 7.4 Activation Strain Model (ASM) for Pericyclic Reactions

```
ΔE‡ = ΔE_distortion + ΔE_interaction

ΔE_distortion = ΔE_dist(diene) + ΔE_dist(dienophile)  [energy cost to deform]
ΔE_interaction = ΔE_elec + ΔE_steric + ΔE_orb          [stabilisation in TS]
```

This model explains why some reactions are allowed (large, negative ΔE_interaction from orbital overlap) and helps quantify substituent effects.

---

## 8. Worked Examples

### Example 1: Diels-Alder — Butadiene + Maleic Anhydride

**Reaction:**  
`C=CC=C` + `O=C1OC(=O)C=CC1=O` → endo-cyclohex-4-ene-1,2-dicarboxylic anhydride

**Analysis:**
1. 4π (diene) + 2π (dienophile) = 6π total
2. 6π = 4(1) + 2 → thermally allowed, suprafacial/suprafacial
3. Maleic anhydride is electron-poor (two C=O, electron-withdrawing) → NED regime
4. Endo approach favoured: secondary orbital interaction between anhydride π* and diene π system
5. **Product:** endo adduct (kinetic); exo is thermodynamically more stable but formed more slowly

### Example 2: Diels-Alder Regioselectivity — 1-Methoxybutadiene + Acrylonitrile

**Reaction:**  
`COC=CC=C` + `N#CC=C` → ?

**Analysis:**
1. Methoxy is EDG → raises diene HOMO (NED regime with acrylonitrile as EWG dienophile)
2. HOMO(diene) largest coefficients: C1 (adjacent to OMe) > C4
3. LUMO(dienophile) largest coefficient: β-carbon (terminal, away from CN)
4. Regiochemistry: C1(diene) bonds to β-C(dienophile), C4(diene) to α-C(dienophile)
5. **Product:** 1-methoxy-4-cyano-cyclohex-3-ene (para-like alignment of EDG and EWG... actually it's meta: CN is meta to OMe on the ring — wait, the "ortho" and "para" nomenclature refers to the relative positions. For NED with EDG on diene and EWG on dienophile, the "ortho" product has EWG adjacent to EDG in the ring.)

Let me re-express: **The CN group ends up adjacent (1,2-relationship) to the OMe group on the cyclohexene ring.** This is the "ortho" product, which is the major regioisomer.

### Example 3: [2+2] Photochemical — Cyclopentenone + Alkene

**Reaction:**  
`O=C1CCCC1=C` + `C=CC` → bicyclo[3.2.0]heptan-2-one

**Analysis:**
1. UV excitation of cyclopentenone (n→π* at ~330 nm) → excited enone
2. 4π total in the excited state → suprafacial/suprafacial photochemical [2+2]
3. Enone C=C and alkene C=C form two new σ bonds
4. **Stereospecific:** cis-alkene → cis-fused ring junction; trans-alkene → trans-fused
5. Regioselectivity: The β-carbon of the enone typically bonds to the less substituted alkene carbon (due to excited-state orbital coefficients)

### Example 4: Electrocyclic — (E,E)-2,4-Hexadiene → cis-3,4-Dimethylcyclobutene

**Reaction:**  
`C/C=C/C=C/C` → `C1CC(C)C(C)C1` (cis-3,4-dimethylcyclobutene)

**Analysis:**
1. 4π system (two double bonds) = 4n where n=1
2. Thermal → **conrotatory** ring closure
3. Both methyl groups rotate in the same direction
4. Starting from (E,E): conrotation brings the inner methyl groups toward each other → **cis** relationship on the cyclobutene
5. **Product:** cis-3,4-dimethylcyclobutene
6. Photochemical would give the **trans** isomer (disrotatory)

### Example 5: Electrocyclic — (E,Z,E)-2,4,6-Octatriene → trans-5,6-Dimethylcyclohexadiene

**Reaction:**  
`C/C=C\C=C/C=C/C` → cyclohexadiene derivative

**Analysis:**
1. 6π system = 4(1)+2
2. Thermal → **disrotatory** ring closure
3. The outer groups rotate in opposite directions
4. For (E,Z,E)-2,4,6-octatriene: disrotation brings the C2 and C7 substituents to the same face
5. **Product:** cis-5,6-dimethylcyclohexa-1,3-diene (or trans, depending on exact geometry — need to draw)

Actually, the stereochemical outcome depends on whether the two outer lobes rotate inward or outward. With (E,Z,E), disrotation can give either cis or trans. The *preferred* mode places substituents outward (trans).

### Example 6: Cope Rearrangement — 1,5-Hexadiene

**Reaction:**  
`C=CC-CC=C` → `C=CC-CC=C` (degenerate)

**Analysis:**
1. 6π electrons (allyl + allyl) = 4(1)+2 → thermally allowed
2. **Chair TS** favoured: ~32 kcal/mol barrier (experiment); 33-35 kcal/mol (DFT)
3. **Boat TS**: ~5 kcal/mol higher
4. The reaction is degenerate for unsubstituted 1,5-hexadiene
5. With substituents: the more stable 1,5-diene isomer predominates

### Example 7: Oxy-Cope — 3-Hydroxy-1,5-hexadiene

**Reaction:**  
`C=CC(O)CC=C` → after rearrangement and tautomerisation → `O=CCCCC=C` (hex-5-en-2-one)

**Analysis:**
1. Standard Cope rearrangement of 3-hydroxy-1,5-hexadiene (ΔG‡ ≈ 33 kcal/mol, slow at RT)
2. After rearrangement → 3-hydroxy-1,5-hexadiene isomer (enol of hex-5-en-2-one)
3. Rapid keto-enol tautomerisation → hex-5-en-2-one (irreversible pull)
4. **Anion-accelerated oxy-Cope:** Deprotonate OH (ΔG‡ ≈ 18-20 kcal/mol, fast at RT)
5. Acceleration mechanism: negative charge delocalisation into the forming C–C bond in the TS

### Example 8: Claisen Rearrangement — Allyl Phenyl Ether → o-Allylphenol

**Reaction:**  
`C=C-C-O-C1=CC=CC=C1` → `OC1=CC(CC=C)=CC=C1` (2-allylphenol)

**Analysis:**
1. 6π electrons → thermally allowed, suprafacial/suprafacial
2. Chair TS: allyl group and phenyl ring adopt chair-like geometry
3. Pericyclic [3,3] shift of allyl group from O to ortho position
4. **Regioselectivity:** ortho > para (kinetic: ortho TS is lower energy due to less distortion of the aromatic ring)
5. **Temperature:** Typically 180-250°C for simple allyl aryl ethers; lower for activated systems

### Example 9: [2,3]-Wittig Rearrangement

**Reaction:**  
`C=C-C-O-CH2-Ph` → [2,3]-shift → `C(-O-Ph)=CH-CH2-CH2-Ph`

**Analysis:**
1. 6 electrons (σ bond + 4π electrons of allyl system) → thermally allowed
2. Deprotonation of benzylic position generates carbanion
3. Five-membered cyclic TS (envelope geometry)
4. **Stereospecific:** The configuration of the allyl double bond is preserved (E → E)
5. Competes with [1,2]-Wittig ( Stevens rearrangement); [2,3] is favoured with allylic substrates

### Example 10: Mislow-Evans Rearrangement — Allyl p-Tolyl Sulfoxide

**Reaction:**  
`C=C-C-S(=O)(c1ccc(cc1)CH3)` → allyl sulfoxide isomer

**Analysis:**
1. 6 electrons → thermally allowed, suprafacial/suprafacial
2. Five-membered cyclic TS
3. The chirality at sulfur is **inverted** in the product
4. Highly stereospecific: the alkene geometry determines the new stereocenter
5. Application: dynamic kinetic resolution of allylic sulfoxides

### Example 11: 1,3-Dipolar Cycloaddition — Nitrone + Alkene

**Reaction:**  
`[CH2=N+(O-)]` (C,N-diphenylnitrone) + `C=CC(C)C` (2-methylpropene) → isoxazolidine

**Analysis:**
1. 4π (nitrone) + 2π (alkene) = 6π → thermally allowed, suprafacial/suprafacial
2. NED regime (nitrone HOMO is relatively high; alkene is not particularly EWG)
3. **Regioselectivity:** With unsymmetrical nitrone + unsymmetrical alkene, the major product follows FMO coefficient matching
4. **Stereoselectivity:** Endo approach favoured for cyclic nitrones (secondary orbital interaction with the N–O π system)
5. **Product:** Isoxazolidine, which can be reduced to β-amino alcohol (N–O bond cleavage)

### Example 12: Ene Reaction — Propene + Singlet Oxygen

**Reaction:**  
`C=CC` + `¹O₂` → hydroperoxide

**Analysis:**
1. 6 electrons (ene: 2σ + 2π + enophile: 2π) → thermally allowed
2. Singlet oxygen acts as enophile (electron-poor, diradicaloid)
3. Suprafacial transfer of allylic H to O₂, with migration of C=C bond
4. **Product:** Allylic hydroperoxide (Schenck ene reaction)
5. **Stereochemistry:** H is transferred suprafacially → **syn** relationship of new C–O and C=C bonds
6. Important in: photo-oxygenation of natural products, lipid peroxidation models

### Example 13: Diels-Alder with Inverse Electron Demand

**Reaction:**  
1,2,4-Triazine + enamine → pyridine + N₂ (via retro-Diels-Alder)

**Analysis:**
1. Electron-poor diene (triazine, due to N atoms) + electron-rich dienophile (enamine) = IED
2. FMO: LUMO(triazine)–HOMO(enamine) dominant
3. Initial [4+2] cycloadduct formed, then **retro-Diels-Alder** with loss of N₂
4. **Net transformation:** triazine + enamine → substituted pyridine
5. Very useful for pyridine synthesis; developed by Boger and others

### Example 14: Electrocyclic Ring Opening — trans-Cyclooctene Derivative

**Reaction:**  
trans-Cyclooctene (if it could be isolated and then opened) — actually this is about **cis,trans-cyclooctadiene → cis,cis,trans-cyclooctatriene** (8π, thermal, conrotatory)

**Analysis:**
1. 8π system = 4(2) → thermal conrotatory
2. Conrotatory ring opening of the cyclobutene-like moiety within the larger ring
3. The product must accommodate the conrotatory stereochemistry within the ring constraint
4. **Application:** Biosynthesis of vitamin D₃ involves electrocyclic ring opening of previtamin D₃ (via photochemical ring opening)

**Corrected example — Vitamin D biosynthesis:**  
7-Dehydrocholesterol (a 5,7-diene in the B ring) absorbs UVB → **photochemical 6π electrocyclic ring opening** (conrotatory) → previtamin D₃ → thermal [1,7]-H shift → vitamin D₃

### Example 15: [4+3] Cycloaddition — Furan + Oxyallyl Cation

**Reaction:**  
Furan (`C1=COC=C1`) + oxyallyl cation (from 2,4-dibromopentan-3-one + Zn) → 8-oxabicyclo[3.2.1]oct-6-en-3-one

**Analysis:**
1. 4π (furan) + 2π + 1π (oxyallyl) = 7 electrons... 
2. More accurately: the oxyallyl cation contributes 4π electrons (allyl cation, 2π), but with the charge... the actual electron count is debated
3. **Practical reality:** Often stepwise (Mannich-type addition of furan to oxyallyl, then ring closure)
4. **Regioselectivity:** The more nucleophilic C2/C5 of furan bonds to the less substituted terminus of oxyallyl
5. **Endo selectivity:** Observed, analogous to Diels-Alder
6. **Applications:** Synthesis of tropane alkaloids, construction of 7-membered rings via ring expansion

---

## Quick Reference Tables

### Table A: Pericyclic Selection Rules Summary

| Reaction | Electrons | Thermal | Photochemical |
|---|---|---|---|
| [4+2] Cycloaddition | 6 | **s,s allowed** | s,s forbidden |
| [2+2] Cycloaddition | 4 | s,s **forbidden** (s,a allowed) | **s,s allowed** |
| Electrocyclic (4n) | 4,8,... | **Conrotatory** | Disrotatory |
| Electrocyclic (4n+2) | 6,10,... | **Disrotatory** | Conrotatory |
| [1,3]-Sigmatropic | 4 | s,a (geometrically hard) | s,s |
| [1,5]-Sigmatropic | 6 | **s,s allowed** | — |
| [3,3]-Sigmatropic | 6 | **s,s allowed** | — |
| [2,3]-Sigmatropic | 6 | **s,s allowed** | — |
| [5,5]-Sigmatropic | 10 | **s,s allowed** | — |

### Table B: Key Computational Parameters

| Property | Typical DFT Method | Typical Level |
|---|---|---|
| TS geometry | B3LYP/6-31G(d) or M06-2X/6-31G(d) | DFT |
| Single-point energy | ωB97X-D/def2-TZVP | DFT-D |
| High accuracy | DLPNO-CCSD(T)/CBS | CCSD(T) |
| Solvation | SMD(chloroform) | Implicit |
| Barrier accuracy | ±2 kcal/mol (ωB97X-D) | — |

---

## Cross-References

- **L1:** `chem-memory/L1_ontology/chemistry-core-map.md` → Pericyclic Reactions node
- **L3:** Computational scripts for TS optimisation (TBD)
- **L4:** Detailed substituent effect tables (TBD)
- **L5:** Named reaction databases (TBD)

---

*This file is a living reference. Update as new computational benchmarks or synthetic applications emerge.*
