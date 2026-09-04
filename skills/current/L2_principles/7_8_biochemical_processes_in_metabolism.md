---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch07
layer: 2
title: 7.8: Biochemical Processes in Metabolism
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 7.8: Biochemical Processes in Metabolism

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 07]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/07%3A_Chemistry_of_Life_and_Green_Chemistry/7.08%3A_New_Page

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

**Source:** `metabolism_tools.py`
Bioenergetics: glycolysis, TCA cycle, complete glucose oxidation, fatty acid oxidation, RQ.

### Available functions:
- `glycolysis_atp_yield(glucose_molecules, aerobic, shuttle)` → dict — ATP yield from glycolysis (shuttle: malate-aspartate or glycerol-3-phosphate)
- `tca_cycle_atp_yield(acetyl_coa)` → dict — ATP yield from TCA cycle per acetyl CoA
- `complete_glucose_oxidation(shuttle, glucose_molecules)` → dict — Full accounting: glycolysis + pyruvate + TCA
- `fatty_acid_oxidation(n_carbons, saturated, n_double_bonds)` → dict — Beta-oxidation ATP yield with activation cost
- `respiratory_quotient(substrate)` → float — RQ = CO₂/O₂ for glucose (1.0), fat (0.7), protein (0.8)

### Common errors:
- ❌ Using wrong shuttle type (malate-aspartate gives 2.5 ATP/NADH; glycerol-3-P gives 1.5)
- ❌ Forgetting -2 ATP activation cost in fatty acid oxidation
