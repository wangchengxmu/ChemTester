---
id: green_metrics
layer: 2
title: Green Metrics (E-factor, PMI, Atom Economy, RME)
parent: ../L1_ontology/chemistry-core-map.md#entry-280
stability: high
confidence: high
last_verified: 2026-03-24
source: Anastas & Warner, Sheldon (Chem. Ind.), Manahan (LibreTexts)
---

# Green Chemistry Metrics

## Core Concept

Quantitative metrics measure the environmental performance of chemical processes, enabling comparison and improvement.

---

## Key Metrics

### 1. Atom Economy (AE)
$$\text{AE (\%)} = \frac{\text{MW(product)}}{\sum \text{MW(reactants)}} \times 100$$
- Simple, based on stoichiometry alone
- **Limitation:** doesn't reflect actual solvent/waste

### 2. E-factor (Sheldon, 1992)
$$\text{E-factor} = \frac{\text{total waste (kg)}}{\text{product (kg)}}$$
- Includes solvents, reagents, losses — everything except product
- **Industry benchmarks:**
  - Oil refining: 0.1
  - Bulk chemicals: 1-5
  - Fine chemicals: 5-50
  - Pharmaceuticals: 25-100+

### 3. Process Mass Intensity (PMI)
$$\text{PMI} = \frac{\text{total mass in process}}{\text{mass of product}} = \text{E-factor} + 1$$

- GlaxoSmithKline (GSK) metric of choice
- Lower is better

### 4. Reaction Mass Efficiency (RME)
$$\text{RME (\%)} = \frac{\text{actual mass of product}}{\text{total mass of reactants}} \times 100$$

- Combines AE with yield
- More realistic than AE alone

### 5. Carbon Efficiency (CE)
$$\text{CE (\%)} = \frac{\text{carbon in product}}{\text{carbon in reactants}} \times 100$$

### 6. Effective Mass Yield (EMY)
$$\text{EMY (\%)} = \frac{\text{mass of product}}{\text{mass of non-benign reagents}} \times 100$$

- Excludes water, NaCl, and other benign materials

---

## Relationships
$$\text{PMI} = \text{E-factor} + 1$$
$$\text{RME} = \text{AE} \times \text{Yield (\%)}$$

---

## Example Calculation

**Reaction:** 58.5 g NaCl + 98.1 g H₂SO₄ → 120.4 g NaHSO₄ + 36.5 g HCl

- AE = 120.4 / (58.5 + 98.1) = 76.8%
- If yield is 85%: RME = 76.8% × 0.85 = 65.3%
- If 500 g solvent used: E-factor = (500 + 23.8) / 102.3 ≈ 5.1

---

## Links

- L3: `../L3_functions/green_chemistry_tools.py`
- L4: `../L4_reference/green_chemistry_reference.csv`
