---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch11
layer: 2
title: 11.4: Environmental Hazards of the Geosphere
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 11.4: Environmental Hazards of the Geosphere

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 11]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/11%3A_The_Geosphere_and_a_Green_Earth/11.04%3A_New_Page

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

**Source:** `environmental_tools.py`
Environmental chemistry: Henry's law, BOD, partition coefficients, greenhouse forcing, atom economy.

### Available functions:
- `henry_law_volatilization(kh_atm_l_mol, c_water, wind_speed, depth, temperature)` → dict — Estimate volatilization using two-film model
- `bod_calc(bod5, ultimate_bod, k_rate, temperature, time_days)` → dict — Calculate BOD using first-order kinetics with temp correction
- `partition_coefficient(log_kow, foc, mode)` → dict — Calculate Koc, Kd, BCF from octanol-water partition
- `greenhouse_forcing(co2_ppm, ch4_ppb, n2o_ppb, baseline_co2, baseline_ch4, baseline_n2o)` → dict — IPCC simplified radiative forcing
- `atom_economy(product_mw, reactant_mws, product_formula, reactant_formulas)` → dict — Calculate atom economy, E-factor, PMI

### Common errors:
- ❌ Using Henry's constant without temperature correction (H' = H/RT)
- ❌ Not applying temperature correction k_T = k₂₀ × 1.047^(T-20) for BOD rate constant

## L3 Tool Call Directives

**Source:** `environmental_tools.py`
Environmental chemistry: Henry's law, BOD, partition coefficients, greenhouse forcing, atom economy.

### Available functions:
- `henry_law_volatilization(kh_atm_l_mol, c_water, wind_speed, depth, temperature)` → dict — Estimate volatilization using two-film model
- `bod_calc(bod5, ultimate_bod, k_rate, temperature, time_days)` → dict — Calculate BOD using first-order kinetics with temp correction
- `partition_coefficient(log_kow, foc, mode)` → dict — Calculate Koc, Kd, BCF from octanol-water partition
- `greenhouse_forcing(co2_ppm, ch4_ppb, n2o_ppb, baseline_co2, baseline_ch4, baseline_n2o)` → dict — IPCC simplified radiative forcing
- `atom_economy(product_mw, reactant_mws, product_formula, reactant_formulas)` → dict — Calculate atom economy, E-factor, PMI

### Common errors:
- ❌ Using Henry's constant without temperature correction (H' = H/RT)
- ❌ Not applying temperature correction k_T = k₂₀ × 1.047^(T-20) for BOD rate constant
