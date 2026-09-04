---
id: life_cycle_assessment
layer: 2
title: Life Cycle Assessment (LCA) Basics
parent: ../L1_ontology/chemistry-core-map.md#entry-283
stability: high
confidence: high
last_verified: 2026-03-24
source: Manahan (LibreTexts), ISO 14040/14044
---

# Life Cycle Assessment (LCA)

## Core Concept

LCA is a systematic methodology for evaluating the environmental impacts of a product or process from "cradle to grave" — from raw material extraction through manufacturing, use, and disposal.

---

## ISO 14040 Framework

### Four Phases

1. **Goal & Scope Definition**
   - System boundaries (cradle-to-gate, cradle-to-grave, gate-to-gate)
   - Functional unit (what is being compared)
   - Reference flow

2. **Life Cycle Inventory (LCI)**
   - Quantify all inputs (materials, energy) and outputs (emissions, waste)
   - Data from literature, industry, databases (ecoinvent, GaBi)

3. **Life Cycle Impact Assessment (LCIA)**
   - Classify inventory data into impact categories
   - Characterization (e.g., CO₂ → GWP in kg CO₂-eq)

4. **Interpretation**
   - Sensitivity analysis
   - Identify significant issues
   - Conclusions and recommendations

---

## Key Impact Categories

| Category | Unit | Example Indicator |
|----------|------|-------------------|
| Global Warming Potential (GWP) | kg CO₂-eq | CO₂, CH₄, N₂O |
| Acidification Potential (AP) | kg SO₂-eq | SO₂, NOₓ |
| Eutrophication Potential (EP) | kg PO₄-eq | NO₃⁻, PO₄³⁻ |
| Ozone Depletion Potential (ODP) | kg CFC-11-eq | CFCs, HCFCs |
| Photochemical Ozone Creation (POCP) | kg C₂H₄-eq | VOCs |
| Human Toxicity | kg 1,4-DCB-eq | Heavy metals, PAHs |
| Abiotic Depletion | kg Sb-eq | Fossil fuels, minerals |

---

## GWP Characterization Factors (100-year)

| Gas | GWP₁₀₀ |
|-----|--------|
| CO₂ | 1 |
| CH₄ | 28 |
| N₂O | 265 |
| CF₄ | 6630 |
| HFC-134a | 1300 |

---

## LCA System Boundaries

- **Cradle-to-gate:** raw materials → factory exit
- **Cradle-to-grave:** raw materials → use → disposal/recycling
- **Gate-to-gate:** factory process only

---

## LCA in Chemistry
- Comparing synthetic routes
- Evaluating solvent choices
- Bio-based vs petrochemical feedstocks
- Assessing new materials (bioplastics vs conventional plastics)

---

## Links

- L3: `../L3_functions/green_chemistry_tools.py`
- L4: `../L4_reference/green_chemistry_reference.csv`
