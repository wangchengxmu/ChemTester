---
id: soil_chemistry.expanded
layer: 2
title: Soil Chemistry
parent: ../L1_ontology/chemistry-core-map.md#entry-241
stability: high
confidence: high
last_verified: 2026-03-24
source: NCERT Ch14, Sparks Environmental Soil Chemistry, USDA NRCS
---

# Soil Chemistry

## Core Concept

Soil chemistry studies the composition, chemical reactions, and nutrient dynamics of soils, including ion exchange, nutrient cycling, pH buffering, contaminant fate, and remediation strategies.

---

## Soil Composition

**Ideal mineral soil:** 45% mineral, 5% organic matter, 25% water, 25% air

### Mineral Components
- **Sand (2.0–0.05 mm):** low surface area, low CEC
- **Silt (0.05–0.002 mm):** moderate properties
- **Clay (<0.002 mm):** high surface area, high CEC, dominant chemical reactivity

### Clay Minerals & CEC
| Clay Type | CEC (cmolₑ/kg) | Dominant Bonding |
|-----------|----------------|------------------|
| Kaolinite (1:1) | 3–15 | pH-dependent |
| Montmorillonite (2:1) | 80–120 | Permanent negative charge |
| Vermiculite (2:1) | 100–200 | Both |
| Illite (2:1) | 10–40 | Both |

---

## Cation Exchange Capacity (CEC)

$$CEC = \sum (\text{exchangeable cations}) \quad (\text{cmol}_c/\text{kg})$$

$$CEC_{eff} = CEC_{perm} + CEC_{pH-dep}$$

**Base saturation:** $BS = \frac{\sum(\text{base cations})}{CEC} \times 100\%$

**Typical values:** Sandy soils 1–5, Loam 5–15, Clay 10–50 cmolₑ/kg

---

## Nutrient Cycles

### Nitrogen Cycle
- **Mineralization:** Organic N → NH₄⁺ (ammonification)
- **Nitrification:** NH₄⁺ → NO₂⁻ → NO₃⁻ (Nitrosomonas, Nitrobacter)
- **Denitrification:** NO₃⁻ → NO₂⁻ → NO → N₂O → N₂ (anoxic, Pseudomonas)
- **N fixation:** N₂ → NH₃ (Rhizobium, industrial Haber-Bosch)

### Phosphorus Cycle
- **Forms:** H₂PO₄⁻ (pH 5–7, most available), HPO₄²⁻ (pH 7–9)
- **Immobilization:** P sorption to Fe/Al oxides (acidic) or Ca compounds (alkaline)
- **Problem:** P runoff → eutrophication (irreversible loss from agricultural P perspective)

### Potassium
- **Forms:** Solution K⁺, exchangeable K⁺, fixed K⁺, mineral K
- **CEC governs:** exchangeable K availability

---

## Soil pH and Buffering

**pH ranges:** Strongly acid (<5.0), Acid (5.0–6.0), Slightly acid (6.0–6.5), Neutral (6.5–7.3), Alkaline (>7.3)

**Aluminum toxicity** at pH < 5.5: Al³⁺ released from clay minerals, damages roots

**Buffer systems:** Carbonate (pH 6.2–8.3), Al³⁺/Al(OH)₃ (pH 4.0–5.5), Exchange sites

**Lime requirement (LR):**
$$LR = \text{CEC} \times (\text{target pH} - \text{current pH}) \times \text{buffer factor}$$

---

## Pesticide Fate

### Sorption (Kd, Koc)
$$K_d = \frac{C_s}{C_w} \quad (\text{L/kg})$$
$$K_{oc} = \frac{K_d}{f_{oc}} \quad (\text{normalized to organic carbon})$$

### Degradation Pathways
- **Biodegradation:** microbial, most important in soils
- **Photodegradation:** surface, UV-driven
- **Hydrolysis:** pH-dependent, water-mediated
- **Chemical oxidation:** Mn/Fe oxides

### Leaching Potential
- High Koc → low leaching (strongly sorbed)
- Low Koc, high water solubility → high leaching (contaminant mobile)
- **GUS index:** Groundwater Ubiquity Score for leaching assessment

---

## Soil Remediation

### Bioremediation
- **Biostimulation:** add nutrients/O₂ to enhance native degraders
- **Bioaugmentation:** introduce specialized microbial strains
-适用于: petroleum hydrocarbons, pesticides, chlorinated solvents

### Phytoremediation
- **Phytoextraction:** hyperaccumulators concentrate metals (e.g., Thlaspi for Zn, Pb)
- **Phytodegradation:** plants metabolize organics
- **Rhizofiltration:** roots remove contaminants from water

### Soil Washing
- Physical separation + chemical extraction
- Surfactants, chelating agents (EDTA), acids
- Effective for heavy metals and hydrophobic organics

---

## L3 Tools
→ `../L3_functions/environmental_tools.py` — `partition_coefficient()`
## L4 Data
→ `../L4_reference/environmental_data.csv`
## L5 Examples
→ `../L5_examples/environmental_examples.md`
