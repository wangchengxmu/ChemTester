---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch06
layer: 2
title: 6.4: Functional Groups
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 6.4: Functional Groups

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 06]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/06%3A_he_Wonderful_World_of_Carbon-_Organic_Chemistry_and_Biochemicals/6.04%3A_New_Page

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

**Source:** `functional_group_tools.py`
Functional group identification, naming priority, electron effects, and property prediction.

### Available functions:
- `identify_functional_groups(smiles_or_formula)` → List[str] — Identify functional groups from SMILES/formula string
- `get_naming_priority(group_name)` → int — Get IUPAC naming priority (higher = suffix)
- `determine_principal_group(groups)` → str — Determine principal group for IUPAC naming
- `get_suffix(group_name)` → str — Get IUPAC suffix (e.g., 'ol', 'oic acid')
- `get_prefix(group_name)` → str — Get IUPAC prefix (e.g., 'hydroxy', 'nitro')
- `classify_electron_effect(group_name)` → str — Classify as 'withdrawing'/'donating'/'neutral'
- `predict_boiling_point_trend(groups)` → str — Predict boiling point trend from functional groups
- `predict_solubility(groups, carbons)` → str — Predict water solubility based on polarity and carbon count
- `functional_group_summary()` → dict — Complete reference table of all functional groups

### Common errors:
- ❌ Confusing electron-withdrawing (NO₂, CN) with electron-donating (OH, NH₂) groups
- ❌ Not accounting for H-bonding groups when predicting solubility cutoffs
