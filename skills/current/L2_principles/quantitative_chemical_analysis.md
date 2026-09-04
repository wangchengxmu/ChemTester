---
id: chem.quantitative_analysis
layer: 2
title: Quantitative Chemical Analysis
source: LibreTexts Chemistry 2e Ch04.05
status: active
created: 2026-03-10
last_verified: 2026-03-28
down_links:
  - ../L3_functions/quantitative_analysis_tools.py
---

# Quantitative Chemical Analysis

## Problem type
Determine analyte concentration or composition via titration, gravimetric analysis, or combustion analysis.

## Decision tree

1. **Analysis method?**
   - Titration → Volume + molarity + stoichiometry
   - Gravimetric → Precipitate mass + stoichiometry
   - Combustion → CO2/H2O masses → empirical formula

2. **Titration type?**
   - Acid-base → mole ratio from equation
   - Redox → electron balance
   - Precipitation → product stoichiometry

3. **Gravimetric type?**
   - Precipitation → isolate, dry, weigh precipitate
   - Combustion → weigh absorbed products

## Core formulas

### Titration
```
mol_titrant = M_titrant × V_titrant(L)
mol_analyte = mol_titrant × (coeff_analyte / coeff_titrant)
M_analyte = mol_analyte / V_analyte(L)

Shortcut: M = mmol / mL
```

### Gravimetric
```
mass_analyte = mass_precipitate × (1/M_precip) × (mol_analyte/mol_precip) × M_analyte
mass_percent = (mass_analyte / mass_sample) × 100%
```

### Combustion analysis
```
mol_C = mass_CO2 × (1/44.01) × 1
mol_H = mass_H2O × (1/18.02) × 2

Empirical formula = simplest whole-number ratio of C:H
```

## Constraints
- Equivalence point ≈ end point (good titration)
- Precipitate must be pure, dry, known composition
- Combustion assumes complete conversion C→CO2, H→H2O

## Common patterns
- Titration: find unknown concentration from known titrant
- Gravimetric: find mass percent of component
- Combustion: find empirical formula of hydrocarbon

## Links

### L3 Implementation
- `../L3_functions/titration_tools.py` (TODO)
- `../L3_functions/quantitative_analysis_tools.py` (TODO)
- `../L3_functions/quantitative_analysis_tools.py` (TODO)

### L4 Reference
- `../L4_reference/quantitative-analysis-reference.md` (TODO)

### L5 Examples
- `../L5_examples/analytical_validation_examples.md (TODO)

## Source trace
- `../sources/ingestion/source-stoichiometry-chemical-reactions-stepwise.md` section 4.05

## L3 Tool Call Directives

**Source:** quantitative_analysis_tools.py
Titration, gravimetric, and combustion analysis calculations.

### Available functions:
- 	itration_molarity(M_titrant, V_titrant_mL, V_analyte_mL, coeff_ratio) → float — Analyte molarity from titration
- 	itration_moles(M_titrant, V_titrant_L) → float — Moles of titrant
- gravimetric_mass_analyte(mass_precipitate, molar_mass_precipitate, molar_mass_analyte, mol_ratio) → float — Mass of analyte (g)
- gravimetric_mass_percent(mass_precipitate, molar_mass_precipitate, molar_mass_analyte, mol_ratio, mass_sample) → float — Mass percent (0-100)
- combustion_moles_from_CO2(mass_CO2) → float — Moles of C from CO₂ (MW=44.01)
- combustion_moles_from_H2O(mass_H2O) → float — Moles of H from H₂O (MW=18.02, ×2)
- combustion_empirical_formula(mass_CO2, mass_H2O, mass_sample=None, other_elements=None) → str — Empirical formula string

### Common errors:
- ❌ Wrong coeff_ratio direction; ratio = (coeff_analyte / coeff_titrant) from balanced equation
- ❌ Forgetting mol_ratio in gravimetric calc (mol analyte / mol precipitate)
