---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch12
layer: 2
title: 12: The Biosphere and the Role of Green Chemistry in Feeding a Hungry World
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 12: The Biosphere and the Role of Green Chemistry in Feeding a Hungry World

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 12]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/12%3A_The_Biosphere_and_the_Role_of_Green_Chemistry_in_Feeding_a_Hungry_World

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

**Source:** `green_chemistry_tools.py`

Green chemistry metrics: atom economy, E-factor, PMI, RME, GWP, carbon efficiency, solvent recovery, and multi-step synthesis yields.

### Available functions:
- `atom_economy(mw_product, mw_reactants)` → dict — Returns {'atom_economy_pct': value}; AE = MW(product)/ΣMW(reactants) × 100
- `e_factor(total_waste_kg, product_kg)` → dict — Returns {'e_factor', 'pmi'}; E = waste/product, PMI = E + 1
- `process_mass_intensity(total_input_mass, product_mass)` → dict — Returns {'pmi', 'e_factor'}; PMI = total_input/product
- `reaction_mass_efficiency(mw_product, mw_reactants, yield_pct)` → dict — Returns {'rme_pct'}; RME = AE × yield
- `gwp_calculator(emissions, time_horizon=100)` → dict — Global warming potential; emissions={'CO2': kg, 'CH4': kg, ...}
- `overall_yield_multistep(yields)` → dict — Multi-step synthesis; yields as fractions [0.9, 0.85, ...]
- `carbon_efficiency(carbon_in_product, carbon_in_reactants)` → dict — CE = (C_product/C_reactants) × 100
- `solvent_recovery_rate(mass_solvent_recovered, mass_solvent_used)` → dict — Recovery rate percentage
- `energy_efficiency(theoretical_energy, actual_energy)` → dict — Efficiency percentage
- `toxicity_reduction(old_toxicity, new_toxicity)` → dict — Reduction percentage

### Common errors:
- ❌ Passing yield as percentage (50) instead of fraction (0.5) in overall_yield_multistep
- ❌ Forgetting that PMI = E-factor + 1 (they're related)
- ❌ Not checking that mw_reactants is a list, not a single value
