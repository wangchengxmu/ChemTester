# L2 Topic: Organocatalysis

**Source**: Catalytic Asymmetric Synthesis (Punniyamurthy), Ch10; LibreTexts Organic Chemistry
**Created**: 2026-03-20
**Status**: Pass-1
**Parent**: asymmetric_synthesis.md

---

## Concept Overview

Organocatalysis uses small organic molecules (no metals) to catalyze enantioselective reactions. Advantages: low toxicity, operational simplicity, air/moisture stability, inexpensive catalysts.

### Catalyst Classes

| Catalyst Type | Example | Activation Mode |
|---------------|---------|-----------------|
| Chiral proline | L-proline | Enamine / iminium / bifunctional |
| Proline derivatives | 5-methylproline, pyrrolidine carboxylic acids | Modified enamine |
| Chiral diamines | (S)-diphenylethylenediamine | Enamine |
| Chiral thioureas | Takemoto, Jacobsen | H-bond donor |
| Chiral alkaloids | Cinchona, quinidine | Bifunctional |
| Chiral phosphoric acids | BINOL-PA | Brønsted acid |

---

## Proline Catalysis

### Reactivity Modes of L-Proline

L-Proline is the "simplest enzyme" — bifunctional acid-base catalyst with secondary amine (nucleophile/base) and carboxylic acid (acid).

**Three activation pathways:**
1. **Enamine catalysis**: Proline forms enamine with ketone/aldehyde donor → nucleophilic attack on electrophile
2. **Iminium catalysis**: Proline forms iminium with α,β-unsaturated aldehyde → lowers LUMO, enables conjugate addition
3. **Bifunctional**: Carboxylic acid H-bonds to activate electrophile while amine activates nucleophile

### Proline-Catalyzed Aldol Reaction

$$\text{Aldehyde/Ketone} + \text{Aldehyde} \xrightarrow{\text{L-proline (20-30 mol\%)}} \beta\text{-hydroxy carbonyl}$$

**Mechanism** (Zimmerman-Traxler-like):
1. L-Proline reacts with carbonyl donor → enamine
2. Enamine attacks *re*-face of aldehyde (si-face blocked by sterics)
3. Iminium hydrolysis → β-hydroxy ketone + regenerated proline

**Selectivity**: Typically 80-99% ee, syn/anti controlled by catalyst structure

**Key example**: Robinson annulation via intramolecular aldol (1970s, first proline-catalyzed reaction)

### Proline-Catalyzed Mannich Reaction

Three-component: aldehyde + ketone + imine → β-amino carbonyl

- L-Proline gives **syn** product
- 5-Methylproline (3R,5R) gives **anti** product
- Position of COOH on pyrrolidine ring controls syn/anti stereochemistry

### Proline-Catalyzed Michael Reaction

Acetone/cyclopentanone + nitrostyrene → Michael adducts
- Direct enamine activation of ketone donor
- Chiral diamines improve ee vs simple proline

---

## Thiourea Catalysis

Thioureas activate electrophiles via dual H-bond donation to carbonyl nitro, or imine groups.

**Takemoto catalyst**: Chiral thiourea-tertiary amine bifunctional catalyst for Michael additions
**Key example**: Synthesis of (R)-(−)-baclofen via asymmetric Michael reaction of 1,3-dicarbonyl to nitroolefins (ee up to 93%)

### H-Bond Activation Model

Thiourea N-H groups H-bond to electrophile oxygen/nitrogen → lowers LUMO, fixes geometry
Adjacent amine base deprotonates nucleophile or activates via ion pair

---

## Alkaloid-Based Organocatalysis

Cinchona alkaloids (quinine, quinidine, cinchonidine) used as:
- Phase-transfer catalysts
- Bifunctional H-bond donors
- Chiral base catalysts

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `predict_proline_aldol_stereochemistry` | syn/anti and re/si face prediction |
| `ee_from_proline_catalysis` | Estimate ee based on substrate structure |

## L4 Data Needed

- Proline catalyst variants and typical ee ranges
- Thiourea catalyst library with electrophile scope

## L5 Examples Needed

- Hajos-Parrish-Eder-Sauer-Wiechert reaction (Robinson annulation)
- Synthesis of (R)-(−)-baclofen via thiourea catalysis

---

**Cross-links:**
- asymmetric_synthesis.md (parent)
- carbonyl_chemistry.md
- stereochemistry_chirality.md
