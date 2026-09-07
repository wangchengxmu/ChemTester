---
id: green_solvents
layer: 2
title: Green Solvents (Water, scCO₂, Ionic Liquids, Switchable Solvents)
parent: ../L1_ontology/chemistry-core-map.md#entry-281
stability: high
confidence: high
last_verified: 2026-03-24
source: Manahan (LibreTexts), Lucia (LibreTexts)
---

# Green Solvents

## Core Concept

Solvent selection is a major factor in process sustainability. Green solvents minimize environmental, health, and safety impacts while maintaining reaction efficiency.

---

## Solvent Selection Hierarchy

1. **No solvent** (neat, mechanochemistry)
2. **Water** (benign, cheap, but limited solubility)
3. **Ethanol, 2-propanol** (low toxicity, biodegradable)
4. **Supercritical CO₂** (renewable, recyclable, gas at ambient)
5. **Ionic liquids** (negligible vapor pressure, tunable)
6. **Switchable solvents** (change properties on demand)

---

## Water as Solvent
- **Advantages:** non-toxic, non-flammable, cheap
- **Challenges:** low solubility of organic compounds, hydrolysis
- **Successful reactions:** Diels-Alder, cycloadditions, pericyclic
- **"On water" effect:** some reactions accelerated at organic-water interface

---

## Supercritical CO₂ (scCO₂)
### Critical Point: T_c = 31.1°C, P_c = 73.8 bar
- **Properties:** gas-like diffusivity, liquid-like density
- **Advantages:** non-toxic, non-flammable, easily removed
- **Limitation:** non-polar — poor solvent for polar compounds
- **Applications:** extraction (caffeine, essential oils), dry cleaning, polymer processing
- **Co-solvents:** add ethanol/modifiers for polar compounds

---

## Ionic Liquids (ILs)
### Definition: salts melting below 100°C (often RT)
- **Structure:** organic cation + inorganic/organic anion
- **Cations:** imidazolium, pyridinium, pyrrolidinium, ammonium, phosphonium
- **Anions:** PF₆⁻, BF₄⁻, Tf₂N⁻, acetate, halides

### Key Properties
- Negligible vapor pressure → no VOC emissions
- High thermal stability (200-400°C)
- Tunable solvation properties
- High viscosity

### Applications
- Solvents for catalysis (Heck, Suzuki, hydrogenation)
- Electrolytes for batteries and supercapacitors
- CO₂ capture

---

## Switchable Solvents
### Principle: solvent properties change reversibly with trigger (CO₂, pH)
- **Example:** DBU + alcohol → ionic liquid (with CO₂) → reverts (with N₂)
- **Advantage:** easy separation, solvent recovery

---

## Biosolvents
- Derived from biomass
- Examples: γ-valerolactone (GVL), 2-methyltetrahydrofuran (2-MeTHF), limonene, cyrene

---

## Links

- L3: `../L3_functions/green_chemistry_tools.py`
- L4: `../L4_reference/green_chemistry_reference.csv`
