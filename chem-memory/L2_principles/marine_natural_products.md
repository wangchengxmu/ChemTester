---
id: marine_natural_products
layer: 2
title: Marine Natural Products
parent: ../L1_ontology/chemistry-core-map.md#entry-287
stability: high
confidence: high
last_verified: 2026-03-24
source: Roberts & Caserio Ch30, marine natural products literature
---

# Marine Natural Products

## Core Concept

Marine organisms (sponges, tunicates, algae, bryozoans, mollusks) produce structurally unique natural products adapted to the competitive marine environment. Many possess potent biological activities.

---

## Why Marine Natural Products Are Unique
- **Saltwater environment:** halogenation (Br, Cl, I) common
- **Soft-bodied organisms:** chemical defense instead of physical
- **Symbiosis:** many "marine" compounds produced by symbiotic microorganisms
- **Extreme conditions:** deep sea, thermal vents → unusual chemistry

---

## Major Compound Classes

### 1. Bryostatins (Bryozoan)
- **Source:** Bugula neritina (marine bryozoan, actually symbiont)
- **Structure:** 26-membered macrolactone
- **Activity:** protein kinase C activator, anticancer clinical trials

### 2. Ecteinascidins (Tunicate)
- **Source:** Ecteinascidia turbinata
- **Example:** Trabectedin (Yondelis) — FDA-approved for soft tissue sarcoma
- **Mechanism:** DNA minor groove binding, blocks transcription

### 3. Dolastatins (Mollusk)
- **Source:** Dolabella auricularia (sea hare)
- **Example:** Monomethyl auristatin E (MMAE) — used in ADC drugs (Adcetris)
- **Mechanism:** tubulin polymerization inhibitor

### 4. Halichondrins (Sponge)
- **Source:** Halichondria okadai
- **Example:** Eribulin (Halaven) — FDA-approved for breast cancer
- **Structure:** complex polyether macrolide

### 5. Cytarabine (Sponge)
- **Source:** Cryptotethya crypta (Caribbean sponge)
- **First marine-derived anticancer drug (FDA 1969)**
- **Nucleoside analog** for leukemia

### 6. Ziconotide (Cone Snail)
- **Source:** Conus magus (venomous cone snail)
- **FDA-approved (2004) for severe chronic pain**
- **Mechanism:** N-type calcium channel blocker (ω-conotoxin)

### 7. Marine Polyketides & Terpenes
- **Discodermolide** (sponge): tubulin stabilizer
- **Spongistatin** (sponge): extremely potent anticancer
- **Salinosporamide A** (Salinispora bacteria): proteasome inhibitor

---

## Supply Challenges
- Many marine organisms cannot be cultured
- Aquaculture development
- **Total synthesis** as alternative (e.g., discodermolide)
- **Semi-synthesis** from aquacultured precursors
- Heterologous expression in engineered microbes

---

## Source Context & Cross-References
- No dedicated marine natural products chapter on LibreTexts
- Related content in Roberts & Caserio Ch30 (general natural products classification)
- Marine NP chemistry primarily from primary research literature and specialized texts
- Cross-reference: `natural_product_classes.md` for classification framework
- Cross-reference: `biosynthetic_pathways.md` for shared biosynthetic origins

---

## Links

- L3: `../L3_functions/natural_products_tools.py`
- L4: `../L4_reference/natural_products_reference.csv`

---

## [Source: Wikipedia, Marine Natural Products]
### Key Marine Natural Product Classes
- **Bryostatins**: From Bugula neritina; anticancer (clinical trials); supply challenges led to aquaculture and total synthesis efforts.
- **Ecteinascidins**: From Ecteinascidia turbinata; trabectedin (Yondelis) FDA-approved for soft tissue sarcoma (2007).
- **Dolastatins**: From Dolabella auricularia; derivatives: monomethyl auristatin E (MMAE) used in ADCs (Adcetris, Polivy).
- **Halichondrins**: From Halichondria okadai; eribulin (Halaven) FDA-approved for metastatic breast cancer (2010); synthesized by Eisai.
- **Ziconotide (Prialt)**: From Conus magus; ω-conotoxin MVIIA; FDA-approved 2004 for severe chronic pain; blocks N-type Ca²⁺ channels.

## L3 Tool Call Directives

**Source:** natural_products_tools.py
L3 Tool: Natural Products Tools

### Available functions:
- terpene_carbon_count(isoprene_units) → dict — Calculate terpene carbon count from isoprene units.
- mevalonate_pathway_cost(target_carbons) → dict — Calculate acetyl-CoA and ATP cost for terpenoid biosynthesis via MVA pathway.
- overall_synthesis_yield(step_yields) → dict — Calculate overall yield for multi-step total synthesis.
- mw_from_formula(formula) → dict — Parse simple molecular formula and calculate MW.
- degree_of_unsaturation(formula) → dict — Calculate degrees of unsaturation (rings + double bonds + triple bonds counted as 2).

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
