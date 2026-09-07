# L2 Topic: Asymmetric Epoxidation

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch5.2-5.3; LibreTexts
**Created**: 2026-03-20
**Status**: Pass-1
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Asymmetric epoxidation introduces an oxygen atom across a C=C bond to form chiral epoxides with high enantioselectivity. Epoxides are versatile intermediates for ring-opening to diols, amino alcohols, and other functional groups.

### Major Methods

| Method | Substrate | Catalyst | Typical ee |
|--------|-----------|----------|-----------|
| Sharpless (Ti-tartrate) | Allylic alcohols | Ti(OiPr)₄ + DET/TET + t-BuOOH | 90-99% |
| Jacobsen-Katsuki (Mn-salen) | Unfunctionalized alkenes | Mn(III)-salen + oxidant | 88-97% |
| Shi (organocatalytic) | Unfunctionalized alkenes | Fructose-derived ketone + oxone | 85-99% |
| Lanthanoid | α,β-Unsaturated carbonyls | Ln-BINOL + peroxide | 80-99% |
| Nb-catalyzed | Allylic alcohols | Nb(salan) + H₂O₂ | 83-95% |

---

## Sharpless Asymmetric Epoxidation (Ti-Tartrate)

### Reaction
$$\text{Allylic alcohol} \xrightarrow{\text{Ti(OiPr)₄, (R\text{ or }S)\text{-DET/TET}, t\text{-BuOOH}}} \text{chiral epoxy alcohol}$$

### Stereochemistry Prediction Model

The Ti-tartrate-allylic alcohol complex forms a chiral pocket. The allylic alcohol coordinates to Ti, and the peroxy group delivers oxygen from one face.

**Rules**:
- **L-(+)-DET**: oxygen delivered from bottom face → (2S,3S) epoxide (for E-allylic alcohols)
- **D-(−)-DET**: oxygen delivered from top face → (2R,3R) epoxide
- **L-(+)-DIPT**: same sense as L-(+)-DET
- **D-(−)-DIPT**: same sense as D-(−)-DET

### Mechanism
1. Ti(OiPr)₄ + tartrate → dimeric Ti-tartrate complex
2. t-BuOOH displaces isopropoxide → Ti-peroxo species
3. Allylic alcohol coordinates to Ti
4. Oxygen transfer to C=C with face selectivity determined by tartrate chirality
5. Product released, catalyst regenerated

### Applications
- **(S)-Propranolol**: β-blocker synthesis via epoxy alcohol intermediate (90% ee)
- **(+)-Disparlure**: Gypsy moth sex pheromone (95% ee)
- Selective oxidation of allylic double bonds in polyene systems (geraniol → 95% ee)

---

## Jacobsen-Katsuki Epoxidation (Mn-Salen)

### Catalyst Synthesis
Mn(OAc)₂ + chiral Schiff base (from 1,2-diamine + salicylaldehyde) → Mn(III)-salen complex

### Reaction
$$\text{Alkene} \xrightarrow{\text{Mn-salen (5-10 mol\%), NaOCl or mCPBA}} \text{chiral epoxide}$$

### Mechanism
- Mn(III) → Mn(V)=O (high-valent metal-oxo)
- Concerted (side-on approach) or radical stepwise pathway depending on substrate electronics
- **Side-on perpendicular approach** of alkene to Mn=O determines enantioselectivity

### Scope
- Trisubstituted alkenes: 88-95% ee
- Styrene derivatives: 80-90% ee (with N-morpholine N-oxide + mCPBA)
- **cis**-Cinnamic esters: 97% ee (taxol side chain precursor)

---

## Shi Epoxidation (Organocatalytic)

### Reaction
$$\text{Alkene} \xrightarrow{\text{Fructose-derived ketone (20-30 mol\%), oxone}} \text{chiral epoxide}$$

### Mechanism
1. Ketone + oxone → dioxirane (active oxidant)
2. Dioxirane transfers oxygen to alkene via spiro transition state
3. Ketone regenerated

### Scope
- Trisubstituted alkenes: excellent ee
- cis/Terminal alkenes: glucose-derived ketone variants needed
- α,β-Unsaturated esters: electron-withdrawing acetate ketone catalyst

---

## Niobium-Catalyzed Epoxidation

- Nb(salan) + aq. H₂O₂ or UHP
- **Environmentally attractive**: atom-economical, water as byproduct
- First example of enantioselective epoxidation using aq. H₂O₂ as terminal oxidant

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `predict_sharpless_epoxide_config` | From allylic alcohol + tartrate → predict (R/S) of epoxide |
| `predict_jacobsen_ee` | Estimate ee from substrate structure |

## L5 Examples Needed

- Taxol side chain from cis-cinnamic ester via Jacobsen epoxidation
- (S)-Naproxen precursor from Sharpless epoxidation sequence

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- ethers_epoxides.md (epoxide ring-opening chemistry)
- stereochemistry_chirality.md
