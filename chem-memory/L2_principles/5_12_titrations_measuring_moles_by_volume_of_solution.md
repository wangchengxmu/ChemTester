---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch05
layer: 2
title: 5.12: Titrations - Measuring Moles by Volume of Solution
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 5.12: Titrations - Measuring Moles by Volume of Solution

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 05]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/05%3A_Chemical_Reactions-_Making_Materials_Safely_and_Sustainable/5.12%3A_Titrations_-_Measuring_Moles_by_Volume_of_Solution

## Key Concepts

Search this book
- Downloads expand_more
- Download Page (PDF)
- Download Full Book (PDF)
- Resources expand_more
- Periodic Table
- Physics Constants
- Scientific Calculator
- Reference expand_more
- Reference & Cite
- Tools expand_more
- Help expand_more
- Get Help
- Feedback
- Readability
##
## Error
This action is not available.
-
## Links
- L1: ../L1_ontology/chemistry-core-map.md

## L3 Tool Call Directives

**Source:** `titration_tools.py`

Acid-base titration calculations: equivalence volume, pH curves, indicator selection, weak acid equivalence pH.

### Available functions:
- `equivalence_volume(analyte_mol, titrant_conc, stoichiometry=1)` → float — Volume of titrant at equivalence (L)
- `titration_pH_strong_strong(V_titrant, V_analyte, C_analyte, C_titrant, analyte_is_acid=True)` → float — pH during strong-strong titration
- `half_equivalence_pH(pKa)` → float — pH = pKa at half-equivalence
- `equivalence_pH_weak_acid(V_analyte, C_analyte, Ka)` → float — pH at weak acid equivalence (conjugate base hydrolysis)
- `indicator_range(indicator)` → Tuple[float, float] — pH range for common indicators
- `select_indicator(equivalence_pH)` → str — Best indicator name for given equivalence pH
- `titration_curve_points(V_analyte, C_acid, C_base, Ka=None, is_weak_acid=False)` → Dict — Key curve points

### Common errors:
- ❌ Using mL instead of L for volumes in equivalence_volume
- ❌ Selecting indicator outside the equivalence pH range (use select_indicator)
- ❌ Forgetting weak acid + strong base gives pH > 7 at equivalence
