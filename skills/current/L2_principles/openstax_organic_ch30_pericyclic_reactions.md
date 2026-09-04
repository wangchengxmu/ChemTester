---
id: organic.openstax_ch30
layer: 2
title: Pericyclic Reactions
up_links:
  - ../L1_ontology/organic_chemistry.md
---

# Pericyclic Reactions

## Key Principles

### What Makes a Reaction Pericyclic?

A pericyclic reaction is a concerted reaction (no intermediates) in which bonds are formed and broken in a single cyclic transition state. Key characteristics:
- **Concerted:** All bond-making and bond-breaking happens simultaneously in one step
- **Cyclic transition state:** Electrons flow in a continuous loop
- **No intermediates:** Unlike SN1, E1, or addition reactions with carbocations
- **Stereospecific:** Stereochemistry of the reactants is faithfully transmitted to products
- **Highly selective:** Governed by orbital symmetry rules (Woodward-Hoffmann)

### Types of Pericyclic Reactions

| Type | What Changes | Example |
|---|---|---|
| Electrocyclic | σ ↔ π bonds in one molecule | Ring opening/closing |
| Cycloaddition | Two π systems → two new σ bonds (ring formation) | Diels-Alder |
| Sigmatropic | σ bond migrates across a π system | Cope, Claisen rearrangement |
| Group transfer | σ bond moves between molecules | Ene reaction |

### Woodward-Hoffmann Rules: The Master Framework

The orbital symmetry of the highest occupied molecular orbital (HOMO) in the transition state determines whether a pericyclic reaction is allowed or forbidden. The rules depend on:

1. **Number of electrons** in the cyclic transition state (4n or 4n+2)
2. **Thermal vs photochemical** conditions

| Electron Count | Thermal | Photochemical |
|---|---|---|
| 4n | Antiaromatic TS → **Forbidden** | Excited state → **Allowed** |
| 4n+2 | Aromatic TS → **Allowed** | Excited state → **Forbidden** |

Where n = 1, 2, 3, ... so 4n = 4, 8, 12, ... and 4n+2 = 2, 6, 10, 14, ...

### Why Aromaticity Matters in Transition States

The cyclic transition state of a pericyclic reaction can be analyzed using Frost circle (polygon-in-circle) diagrams. If the transition state is aromatic (4n+2 electrons), it is stabilized and the reaction is thermally allowed. If it is antiaromatic (4n electrons), it is destabilized and thermally forbidden.

## Mechanisms

### 1. Electrocyclic Reactions

**Definition:** A reaction in which a σ bond is formed (or broken) at the ends of a conjugated π system, converting between an open-chain polyene and a cyclic product.

#### Conrotation vs Disrotation

The stereochemical mode of ring closure/opening determines the reaction outcome:

**Conrotation (con-rotatory):** The two terminal groups rotate in the **same direction** (both clockwise or both counterclockwise).

**Disrotation (dis-rotatory):** The two terminal groups rotate in **opposite directions** (one clockwise, one toward).

#### Selection Rules for Electrocyclic Reactions

| π Electrons | Thermal Mode | Photochemical Mode | Example |
|---|---|---|---|
| 4 (butadiene ↔ cyclobutene) | Conrotatory | Disrotatory | cis,trans-1,3,5-hexatriene → cyclohexadiene |
| 6 (hexatriene ↔ cyclohexadiene) | Disrotatory | Conrotatory | 1,3-cyclohexadiene → 1,3,5-hexatriene |

General rule:
- **4n electrons:** thermal = conrotatory, photochemical = disrotatory
- **4n+2 electrons:** thermal = disrotatory, photochemical = conrotatory

#### Worked Examples

**Example 1: Thermal ring closure of (2E,4Z)-hexatriene**
- 6 π electrons = 4n+2 (n=1)
- Thermal → disrotatory
- Both CH₃ groups move outward → **trans-5,6-dimethyl-1,3-cyclohexadiene**

**Example 2: Photochemical ring closure of butadiene**
- 4 π electrons = 4n (n=1)
- Photochemical → disrotatory
- Both terminal groups rotate opposite → product depends on starting stereochemistry

**Example 3: Cyclobutene ring opening**
- 4 π electrons
- Thermal → conrotatory: if substituents are cis on the ring, one rotates in, one rotates out → **trans-1,3-butadiene**
- Photochemical → disrotatory: both groups rotate same side → **cis-1,3-butadiene**

### 2. Cycloaddition Reactions

**Definition:** Two π systems combine to form a new ring by forming two new σ bonds. Described as [m+n] where m and n are the number of π electrons from each component.

#### Diels-Alder Reaction ([4+2] Cycloaddition)

This is the most important cycloaddition in organic chemistry.

**Requirements:**
- **Diene:** 4 π electrons, must be in **s-cis** conformation
- **Dienophile:** 2 π electrons, typically electron-poor (has EWGs)
- **Thermally allowed** (6 electrons = 4n+2)
- **Concerted:** Both bonds form simultaneously

**Diene requirements:**
- Must be in **s-cis** conformation (cisoid)
- s-trans dienes cannot react (orbitals don't overlap)
- Cyclopentadiene is locked in s-cis → excellent diene
- Butadiene exists as ~96% s-trans at room temperature but can rotate to s-cis

**Dienophile activation:**
- Electron-withdrawing groups (EWGs) lower the LUMO: –CHO, –COR, –COOR, –CN, –NO₂
- The more EWGs, the faster the reaction
- Maleic anhydride is a very reactive dienophile
- Ethylene itself is a very poor dienophile

**Regioselectivity (ortho/para rule):**

For a 1-substituted diene + electron-poor dienophile:

```
    H         EWG          H       EWG
     \       /              \       /
      C = C                  C = C
     /       \              /       \
    R         H            H         H
    
    1-substituted        normal (unsubstituted)
    diene               dienophile
```

The major product has the substituents **ortho** (adjacent) to each other in the ring. This can be understood via FMO analysis: the largest coefficients on the HOMO (diene) and LUMO (dienophile) overlap best when the substituents end up adjacent.

For a 2-substituted diene + monosubstituted dienophile, the substituents end up **meta** to each other.

**Stereochemistry (endo rule):**
- The **endo** product is the kinetic product (faster formation)
- The **exo** product is the thermodynamic product (more stable)
- Endo selectivity arises from secondary orbital interactions in the transition state
- At low temperature → endo; at high temperature → may approach exo (thermodynamic control)

**Stereospecificity:**
- **cis** on the dienophile → **cis** in the product
- **trans** on the dienophile → **trans** in the product
- This is because the reaction is concerted and suprafacial on both components

**Stereochemistry table:**

| Diene | Dienophile | Product Configuration |
|---|---|---|
| Unsubstituted | cis-disubstituted | cis relationship maintained |
| Unsubstituted | trans-disubstituted | trans relationship maintained |
| Endo approach | — | Substituents under the ring bridge |

#### [2+2] Cycloaddition

- **4 electrons total** (4n with n=1)
- **Thermally forbidden** for suprafacial-suprafacial
- **Photochemically allowed**
- One component absorbs light → goes to excited state → different orbital symmetry
- Example: ketene + imine → β-lactam (Staudinger synthesis), thermally allowed because ketene uses a different orbital

### 3. Sigmatropic Rearrangements

**Definition:** A reaction in which a σ bond migrates across a conjugated π system. Described as [i,j] where i and j are the number of atoms the σ bond moves across.

#### [3,3] Sigmatropic Rearrangements

**Cope Rearrangement:**
- 1,5-diene → isomeric 1,5-diene
- 6 electrons in the transition state = 4n+2 → thermally allowed
- Chair-like transition state is preferred over boat
- Product stereochemistry depends on the chair conformation
- Example: 1,5-hexadiene ↔ 1,5-hexadiene (degenerate for simple case)

**Claisen Rearrangement:**
- Allyl vinyl ether → γ,δ-unsaturated carbonyl
- [3,3] sigmatropic rearrangement
- Chair transition state
- Followed by keto-enol tautomerization
- **Ireland modification:** Use enolate with silyl enol ether, better control of E/Z geometry
- **Johnson-Claisen:** Orthoester version (allyl alcohol + triethyl orthoacetate)

#### [1,5] and [1,3] Sigmatropic Shifts

| Shift | Electrons | Thermal | Photochemical | Common Example |
|---|---|---|---|---|
| [1,3] H shift | 4 | Forbidden | Allowed | Rare, photochemical only |
| [1,5] H shift | 6 | Allowed | Forbidden | Common in cyclopentadiene |
| [1,7] H shift | 8 | Forbidden | Allowed | Photochemical |

**[1,5] H shift rules:**
- Hydrogen migrates **suprafacially** (same face of the π system)
- The new C–H bond is formed on the same side as the old one broke
- This is why: suprafacial [1,5] with 6 electrons is thermally allowed

**Carbon sigmatropic shifts:**
- [1,2] alkyl shifts: not pericyclic (carbocation rearrangement)
- [1,5] C shifts: thermally allowed, suprafacial
- [3,3] C shifts: Cope rearrangement

### 4. FMO (Frontier Molecular Orbital) Analysis

FMO analysis provides a deeper understanding of pericyclic reactions by examining the interactions between the HOMO of one component and the LUMO of another.

#### For Diels-Alder:

**Normal electron demand:**
- Electron-rich diene (high HOMO) + electron-poor dienophile (low LUMO)
- Key interaction: HOMO(diene) → LUMO(dienophile)
- EWGs on dienophile lower its LUMO → better interaction → faster reaction

**Inverse electron demand:**
- Electron-poor diene + electron-rich dienophile
- Key interaction: LUMO(diene) → HOMO(dienophile)
- Less common but important with heterodienophiles

#### Phase Matching:

For a pericyclic reaction to be allowed, the phases of the interacting orbitals must match at the points where bonds are being formed:
- **In-phase overlap** = bonding interaction = allowed
- **Out-of-phase overlap** = antibonding interaction = forbidden

### 5. Ene Reaction

**Definition:** An alkene with an allylic hydrogen (the "ene") reacts with an electron-poor alkene (the "enophile") in a concerted process.

- Formally a [2+2+2] or analyzed differently
- Not strictly a cycloaddition but often grouped with pericyclic reactions
- Transfers the allylic H to the enophile while forming a new σ bond between the two
- The enophile typically has an EWG (like in Diels-Alder)

**Examples:**
- Propene + formaldehyde → but-3-en-1-ol (simple ene)
- Maleic anhydride + alkene → adduct (Lewis acid-catalyzed)

## Selectivity Rules

### Electrocyclic Reaction Decision Table

| Input | π Electrons | Condition | Mode | Result |
|---|---|---|---|---|
| Butadiene | 4 | Heat | Conrotatory | Trans if cis-cyclobutene |
| Butadiene | 4 | hv | Disrotatory | Cis if cis-cyclobutene |
| Hexatriene | 6 | Heat | Disrotatory | Depends on substitution |
| Hexatriene | 6 | hv | Conrotatory | Depends on substitution |

### Cycloaddition Selection Rules

| Reaction | Electrons | Thermal | Photochemical |
|---|---|---|---|
| [4+2] Diels-Alder | 6 | ✅ Allowed | ❌ Forbidden (but possible via different excited state) |
| [2+2] | 4 | ❌ Forbidden | ✅ Allowed |
| [4+4] | 8 | ❌ Forbidden | ✅ Allowed |
| [6+4] | 10 | ✅ Allowed | ❌ Forbidden |
| [1,3]-dipolar cycloaddition | 6 | ✅ Allowed | ❌ Forbidden |

### Sigmatropic Shift Rules

| Shift | Electrons | Thermal Mode | Photochemical Mode |
|---|---|---|---|
| [1,3] H | 4 | Suprafacial forbidden | Allowed |
| [1,5] H | 6 | Suprafacial allowed | Forbidden |
| [1,7] H | 8 | Antara allowed | Suprafacial allowed |
| [3,3] C | 6 | Chair TS (suprafacial) | Allowed |

### Diels-Alder Endo vs Exo

| Feature | Endo | Exo |
|---|---|---|
| Kinetic/thermodynamic | Kinetic | Thermodynamic |
| Stability | Less stable | More stable |
| Rate | Faster (secondary orbital interactions) | Slower |
| Preference | Low temperature | High temperature |
| Stereochemistry | EWGs under the bridge | EWGs away from bridge |

## Common Exam Patterns

### Pattern 1: Electrocyclic Stereochemistry

**Question:** "What is the product when (Z)-1,3,5-hexatriene undergoes thermal electrocyclic ring closure?"

**Answer:** 6 π electrons = disrotatory (thermal). Both terminal groups rotate outward (disrotatory). If the terminal substituents are on the same face, disrotatory motion puts them on opposite faces → trans product. The product is **trans-5,6-dimethyl-1,3-cyclohexadiene** (for substituted cases).

### Pattern 2: Diels-Alder Regiochemistry

**Question:** "Predict the major product of the Diels-Alder reaction between 1-methoxybutadiene and methyl acrylate."

**Answer:** 
- Methoxy is electron-donating on the diene (1-position)
- Ester is electron-withdrawing on the dienophile
- **Ortho product:** The methoxy and ester end up adjacent (1,2-relationship) in the cyclohexene ring
- Reason: FMO coefficient analysis shows maximum overlap when substituents are adjacent

### Pattern 3: Diels-Alder Endo/Exo

**Question:** "Cyclopentadiene + maleic anhydride: is the product endo or exo?"

**Answer:** **Endo** is the kinetic product (formed at room temperature). The anhydride group sits under the norbornene bridge. Endo selectivity arises from favorable secondary orbital overlap between the anhydride C=O π* and the diene π system in the transition state.

### Pattern 4: Cope Rearrangement

**Question:** "What is the product of the Cope rearrangement of 1,5-dimethyl-1,5-hexadiene?"

**Answer:** 
- Chair transition state → the product is (E,Z)- or (E,E)-2,6-octadiene depending on the starting stereochemistry
- The chair TS is strongly preferred over boat
- For meso-1,5-dimethyl substrate: leads to a specific stereochemical outcome

### Pattern 5: Claisen Rearrangement

**Question:** "What product is formed when allyl phenyl ether is heated to 200°C?"

**Answer:** 
- [3,3] sigmatropic Claisen rearrangement
- Phenyl oxygen bond breaks, allyl group migrates
- Product: o-allylphenol (ortho-substituted)
- The ortho position is favored because the 6-membered chair TS directs the allyl group to the ortho position

### Pattern 6: Allowed/Forbidden Predictions

**Question:** "Is a thermal [2+2] cycloaddition of two ethylene molecules allowed?"

**Answer:** **No.** 4 electrons (4n, n=1) in a suprafacial-suprafacial cycloaddition is thermally forbidden by the Woodward-Hoffmann rules. The transition state would be antiaromatic. Photochemically, it is allowed.

### Pattern 7: Photochemical vs Thermal

**Question:** "How would you convert cis-3,4-dimethylcyclobutene to cis,trans-2,4-hexadiene?"

**Answer:** 
- Ring opening of cyclobutene (4 π electrons)
- Thermal → conrotatory → gives trans,trans or cis,trans depending on stereochemistry
- For **cis,trans** product specifically, need to consider the starting stereochemistry and the rotation mode
- If the two methyl groups are cis on the ring: thermal conrotation → one methyl goes up, one down → trans in the diene at one end, cis at the other → **cis,trans-2,4-hexadiene**

### Key Mnemonics

- **4n thermal = con; 4n+2 thermal = dis** (for electrocyclic)
- **Photochemical always reverses the rule**
- **Diels-Alder = 4+2 = 6 electrons = allowed thermally**
- **[2+2] thermal = forbidden; photochemical = allowed**
- **Endo = Kinetic; Exo = Equilibrium**
- **s-cis diene = can react; s-trans = cannot**
- **"Cope" = 1,5-diene rearrangement; "Claisen" = allyl vinyl ether rearrangement**
- **Chair always wins** for [3,3] sigmatropic rearrangements
