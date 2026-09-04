# Kinetics and Trends in Kinetic Lability

**Source:** CHM 320 Advanced Inorganic Chemistry, Chapter 11

## Overview

Kinetic lability describes how rapidly ligands exchange in coordination complexes. Understanding substitution mechanisms is essential for predicting reaction rates and designing synthetic pathways.

## Key Concepts

### Lability vs Inertness

**Labile Complexes:** Fast ligand exchange (t₁/₂ < 1 minute)
**Inert Complexes:** Slow ligand exchange (t₁/₂ > 1 minute)

**General Trends:**
- d⁰, d¹, d², d⁹, d¹⁰: Typically labile
- d³, low-spin d⁴, d⁵, d⁶: Typically inert (Cr³⁺, Co³⁺ classic examples)

### Substitution Mechanisms

#### Stoichiometric Mechanisms (Identity of Intermediate)

**Associative (A):** Incoming ligand bonds first, creating higher-coordinate intermediate
```
MLₙX + Y ⇌ MLₙXY (intermediate) → MLₙY + X
```
- Typical for square planar d⁸ complexes (Pt²⁺, Pd²⁺)

**Dissociative (D):** Leaving group leaves first, creating lower-coordinate intermediate
```
MLₙX ⇌ MLₙ + X → MLₙ + Y → MLₙY
```
- Less common for octahedral complexes

**Interchange (I):** Concerted process, no detectable intermediate
```
MLₙX + Y → [Y···MLₙ···X]‡ → MLₙY + X
```
- Most common for octahedral complexes

#### Intimate Mechanisms (Rate-Determining Step)

**Associatively-activated (a):** Rate depends on entering ligand (rate changes >10-fold with different Y)
- Rate law: rate = k[complex][Y]

**Dissociatively-activated (d):** Rate independent of entering ligand (rate changes <10-fold with different Y)
- Rate law: rate = k[complex]

### Mechanism Notation

Combined notation: Stoichiometric subscript + Intimate subscript

| Mechanism | Intermediate | Rate depends on Y? |
|-----------|--------------|-------------------|
| Aₐ | Higher CN | Yes |
| Aₐ | Higher CN | No |
| Dₐ | Lower CN | Yes |
| Dₐ | Lower CN | No |
| Iₐ | None | Yes |
| Iₐ | None | No |

### Eigen-Wilkins Mechanism

For octahedral complexes, a **pre-equilibrium** forms an encounter complex:

```
ML₅X + Y ⇌ (ML₅X·Y)  [K_E, fast]  ← encounter complex
(ML₅X·Y) → ML₅Y + X   [k₂, rate-limiting]
```

**Rate Law:** rate = k₂K_E[ML₅X][Y] = k_obs[ML₅X][Y]

**Key Features:**
- Explains why rate laws appear different at high vs low [Y]
- Encounter complex forms via diffusion (Coulomb attraction)
- Rate determined by reorganization within encounter complex

### Trans Effect

**Definition:** The ability of a ligand to influence substitution rates of ligands trans to it in square planar complexes

**Strong Trans-Directing Ligands:**
CO > CN⁻ > C₂H₄ > PR₃ > H⁻ > CH₃⁻ > SC(NH₂)₂ > Ph⁻ > I⁻ > SCN⁻ > Br⁻ > Cl⁻ > py > NH₃ > OH⁻ > H₂O

**Mechanistic Explanation:**

1. **σ-Donor Effect:** Strong σ-donors compete for the same metal orbital as trans ligand, weakening trans bond

2. **π-Acceptor Effect:** π-acceptors (CO, CN⁻, PR₃) stabilize trigonal bipyramidal intermediate with trans ligand in equatorial position

**Applications:**
- Synthesis of cis-platin: Start with [PtCl₄]²⁻, add NH₃ (Cl trans to Cl is more labile)
- Avoids trans-platin formation

### Redox Mechanisms

#### Outer Sphere Electron Transfer

Electron transfer without breaking coordination sphere

**Marcus Theory:**
- Barrier arises from solvent and bond length reorganization
- Rate depends on:
  - ΔG° (driving force)
  - Distance between reactants
  - Reorganization energy (λ)

**Rate constant:** k = A exp(-ΔG‡/RT)

**Marcus Inverted Region:** At very large driving force, rate decreases (Nobel Prize: Rudolph Marcus, 1992)

#### Inner Sphere Electron Transfer

Electron transfer through bridging ligand

**Mechanism:**
1. Formation of bridged intermediate
2. Electron transfer through bridge
3. Bridge cleavage

**Example:**
```
[Co(NH₃)₅Cl]²⁺ + Cr²⁺ → [Co(NH₃)₅(μ-Cl)Cr]⁴⁺ → Co²⁺ + CrCl²⁺ + 5NH₃
```

**Evidence for mechanism:** Cl⁻ transfers to Cr (detected in product)

## Rate Predictions

| Metal Configuration | Expected Lability |
|--------------------|-------------------|
| d⁰, d¹, d² | Labile |
| d³ (Cr³⁺) | Inert |
| d⁴ low-spin | Inert |
| d⁵ low-spin | Inert |
| d⁶ low-spin (Co³⁺) | Inert |
| d⁷, d⁸, d⁹ | Labile |
| d¹⁰ | Labile |

## Related Concepts

- **L2/thermodynamics_stability.md** - Thermodynamic vs kinetic stability
- **L2/crystal_field_theory.md** - CFSE and inertness
- **L2/coordination_chemistry.md** - Ligand properties
- **L2/electrode_potentials.md** - Redox potentials

## Problem-Solving Approaches

1. **Identify mechanism type:** Check rate dependence on [Y]
2. **Predict lability:** Use d-electron configuration and CFSE
3. **Design synthesis:** Use trans effect to direct substitution
4. **Calculate rates:** Apply Marcus theory for electron transfer

## Formulas

- **Rate law (associative):** rate = k[MLₙX][Y]
- **Rate law (dissociative):** rate = k[MLₙX]
- **Eigen-Wilkins:** rate = k₂K_E[ML₅X][Y]
- **Marcus rate:** k = κ_el k_nu exp(-ΔG‡/RT)

## Notes

- Thermodynamic stability ≠ kinetic inertness
- Inert complexes are valuable for isolation and characterization
- Labile complexes equilibrate rapidly to thermodynamically favored products
- Trans effect is primarily kinetic (affects rates, not equilibrium)
