---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch01
layer: 2
title: 1.2: The Environment and the Five Environmental Sphere
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 1.2: The Environment and the Five Environmental Sphere

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 01]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/01%3A_Sustainability_and_the_Environment/1.02%3A_The_Environment_and_the_Five_Environmental_Sphere

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

---

## L3 Tool Call Directives

**Source:** environmental_chemistry_tools.py
Half-life, bioconcentration/accumulation, hazard quotient, decay kinetics, COD/BOD, dilution.

### Available functions:
- half_life(k, half_life, order) ¡ú dict ¡ª Interconvert t? and k (first-order: t? = ln2/k)
- ioconcentration_factor(BCF, log_BCF) ¡ú dict ¡ª Interconvert BCF and log??(BCF)
- ioaccumulation_factor(BAF, log_BAF) ¡ú dict ¡ª Interconvert BAF and log??(BAF)
- hazard_quotient(exposure_conc, reference_dose) ¡ú dict ¡ª HQ = E/RfD
- isk_characterization(hazard_quotient) ¡ú dict ¡ª Risk level: <1 low, 1-10 moderate, ¡Ý10 high
- lc50_to_ld50(lc50, body_weight_kg, water_consumption_L_day) ¡ú dict ¡ª Approximate LC50¡úLD50 conversion
- decay_concentration(C0, k, t) ¡ú dict ¡ª First-order: C = C?e^(?kt), fraction remaining
- cod_bod_ratio(COD, BOD) ¡ú dict ¡ª Biodegradability: <2 high, 2-4 moderate, ¡Ý4 low
- dilution_factor(C_source, Q_source, C_ambient, Q_ambient) ¡ú dict ¡ª C_mix and dilution factor

### Common errors:
- ? Confusing BCF (lab bioconcentration) with BAF (field bioaccumulation including diet)
- ? Using HQ ¡Ý 10 as "acceptable" ¡ª ¡Ý10 means high/unacceptable risk
