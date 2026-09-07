---
id: metallurgy.overview
layer: 2
title: Metals and Metallurgy — Extraction, Processing, and Properties
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_tools/metallurgy_tools.py
cross_links:
  - ./electrochemistry.md
  - ./transition_metal_chemistry.md
  - ./band_theory.md
  - ./modern_materials.md
source: Chemistry: The Central Science, Brown et al., Chapter 23
---

## Context

Metallurgy is the science of extracting metals from ores and processing them for use. It encompasses **mineral processing**, **chemical extraction** (pyrometallurgy, hydrometallurgy, electrometallurgy), and **physical metallurgy** (alloying, heat treatment). This node focuses on extraction and processing fundamentals with quantitative tools.

---

## Occurrence of Metals

### Ore Types

| Type | Description | Examples |
|------|-------------|----------|
| Native | Pure metal | Au, Ag, Cu, Pt |
| Oxide | Metal oxides | Hematite (Fe₂O₃), Bauxite (Al₂O₃·2H₂O), Magnetite (Fe₃O₄), Rutile (TiO₂) |
| Sulfide | Metal sulfides | Pyrite (FeS₂), Galena (PbS), Sphalerite (ZnS), Chalcopyrite (CuFeS₂) |
| Carbonate | Metal carbonates | Siderite (FeCO₃), Malachite (Cu₂CO₃(OH)₂), Dolomite (CaMg(CO₃)₂) |
| Halide | Metal halides | Halite (NaCl), Sylvite (KCl), Fluorite (CaF₂) |

### Abundance and Economic Factors

- **Most abundant metals in crust**: Al (8.1%), Fe (5.0%), Ca (3.6%), Na (2.8%), K (2.6%)
- **Ore grade**: minimum metal percentage economically extractable
- **Reserve-to-production ratio**: years of supply at current rate

---

## Pyrometallurgy

### Overview

Uses **high temperatures** to drive chemical reactions that extract metals from ores.

### Key Processes

**1. Roasting**: Converts sulfides to oxides
- 2ZnS + 3O₂ → 2ZnO + 2SO₂
- 2FeS₂ + 11O₂ → 2Fe₂O₃ + 4SO₂
- Often produces SO₂ (must be captured for sulfuric acid)

**2. Smelting**: Reduces metal oxides using carbon (coke) at high T
- Fe₂O₃ + 3CO → 2Fe + 3CO₂
- SnO₂ + 2C → Sn + 2CO
- Cu₂S + O₂ → 2Cu + SO₂

**3. Blast Furnace (Iron)**:
- Charge: iron ore (Fe₂O₃), coke (C), limestone (CaCO₃)
- Reactions at different heights:
  - Bottom (2000°C): C + O₂ → CO₂; CO₂ + C → 2CO
  - Middle (900°C): Fe₂O₃ + 3CO → 2Fe + 3CO₂
  - Limestone: CaCO₃ → CaO + CO₂; CaO + SiO₂ → CaSiO₃ (slag)
- Product: **pig iron** (~4% C, plus Si, Mn, P, S impurities)

**4. Steelmaking (Basic Oxygen Furnace)**:
- 2% C (steel) vs 4% C (pig iron)
- O₂ blown through molten pig iron:
  - C + O₂ → CO₂ (decarburization)
  - Si + O₂ → SiO₂; Mn + O₂ → MnO (removed as slag)
  - P + O₂ → P₂O₅; CaO + P₂O₅ → Ca₃(PO₄)₂ (slag)

### Thermodynamics of Smelting

**Ellingham diagrams** plot ΔG°(T) for metal oxide formation:
- More negative ΔG° → more stable oxide → harder to reduce
- Carbon reduction works when: 2C + O₂ → 2CO has more negative ΔG° than M + O₂ → MO at the operating T
- This is why carbon can reduce FeO but not Al₂O₃, MgO, or TiO₂ at practical temperatures

---

## Hydrometallurgy

### Overview

Uses **aqueous solutions** to extract metals from ores. Lower energy than pyrometallurgy.

### Key Processes

**1. Leaching**: Dissolving metal from ore using acid/base
- Acid leaching: CuO + 2H⁺ → Cu²⁺ + H₂O (sulfuric acid on oxide ores)
- Cyanide leaching: 4Au + 8CN⁻ + O₂ + 2H₂O → 4[Au(CN)₂]⁻ + 4OH⁻
- Alkaline leaching: Al₂O₃ + 2NaOH + 3H₂O → 2Na[Al(OH)₄] (Bayer process)

**2. Bayer Process (Aluminum extraction)**:
1. Bauxite (Al₂O₃·2H₂O) digested with hot NaOH
2. Al(OH)₄⁻ separated from Fe₂O₃ (insoluble "red mud")
3. Al(OH)₃ precipitated by cooling/seeding
4. Calcined: 2Al(OH)₃ → Al₂O₃ + 3H₂O

**3. Solvent Extraction**: Selective transfer of metal between aqueous and organic phases

**4. Electrowinning**: Metal deposited from solution by electrolysis
- Cu²⁺ + 2e⁻ → Cu(s) at cathode

### Leaching Calculations

**Mass balance**:
m_recovered = C · V (concentration × volume of leach solution)

**Recovery efficiency**:
η = (mass extracted / mass in ore) × 100%

---

## Electrometallurgy

### Overview

Uses **electrolysis** for extraction and purification of metals.

### Hall-Héroult Process (Aluminum)

- Al₂O₃ dissolved in molten cryolite (Na₃AlF₆) at ~1000°C
- Cathode: 2Al³⁺ + 6e⁻ → 2Al(l)
- Anode: 3O²⁻ → 3/2 O₂(g) + 6e⁻ (consumes carbon anode: C + O₂ → CO₂)
- Overall: 2Al₂O₃ + 3C → 4Al + 3CO₂
- Energy: ~13–15 kWh/kg Al (very energy-intensive)

### Electrorefining

- Impure metal anode → pure metal cathode
- Example: Cu refining
  - Anode: Cu → Cu²⁺ + 2e⁻
  - Cathode: Cu²⁺ + 2e⁻ → Cu (99.99% pure)
  - Impurities (Fe, Ni, Zn) remain in solution; Au, Ag, Pt collect as "anode slime"

### Faraday's Law Applied

m = (M · I · t) / (n · F)

where M = molar mass, I = current, t = time, n = electrons transferred, F = 96485 C/mol.

---

## Alloying and Physical Metallurgy

### Common Alloy Systems

| Alloy | Composition | Properties | Uses |
|-------|------------|------------|------|
| Stainless steel | Fe + >10.5% Cr, ±Ni | Corrosion resistance | Cutlery, medical instruments |
| Brass | Cu + Zn (5-40%) | Gold appearance, machinable | Plumbing, musical instruments |
| Bronze | Cu + Sn (5-12%) | Harder than brass, marine corrosion | Bearings, sculpture |
| Solder | Sn-Pb or Sn-Ag-Cu | Low melting point | Electronics |
| Duralumin | Al + Cu + Mg + Mn | High strength/weight | Aircraft |
| Titanium alloys | Ti + Al + V | High strength, biocompatible | Aerospace, implants |
| Nitinol | Ni + Ti (50:50) | Shape memory | Stents, actuators |

### Heat Treatment

| Treatment | Process | Effect |
|-----------|---------|--------|
| Annealing | Heat + slow cool | Relieves stress, softens |
| Quenching | Heat + rapid cool | Forms martensite (hard, brittle) |
| Tempering | Reheat quenched steel | Reduces brittleness, maintains hardness |
| Case hardening | Surface carbon enrichment | Hard surface, tough core |
