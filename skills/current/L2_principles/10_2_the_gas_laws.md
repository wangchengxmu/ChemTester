---
id: green_chemistry_and_the_ten_commandments_of_sustainability_manahan_ch10
layer: 2
title: 10.2: The Gas Laws
source: Green Chemistry and the Ten Commandments of Sustainability (Manahan)
stability: medium
confidence: medium
last_verified: 2026-03-24
---

# 10.2: The Gas Laws

## Source
[Source: Green Chemistry and the Ten Commandments of Sustainability (Manahan), Chapter 10]
URL: https://chem.libretexts.org/Bookshelves/Environmental_Chemistry/Green_Chemistry_and_the_Ten_Commandments_of_Sustainability_(Manahan)/10%3A_Blue_Skies_for_a_Green_Environment/10.02%3A_New_Page

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

**Source:** `gas_laws_tools.py`

Core gas law calculations (Boyle, Charles, Gay-Lussac, Avogadro, Combined) with temperature conversions and Dalton's law for partial pressures.

### Available functions:
- `boyles_law(P1, V1, P2, V2)` → float — Apply P₁V₁ = P₂V₂ at constant T,n; pass None for unknown
- `charles_law(V1, T1, V2, T2)` → float — Apply V₁/T₁ = V₂/T₂ at constant P,n; T in Kelvin
- `gay_lussacs_law(P1, T1, P2, T2)` → float — Apply P₁/T₁ = P₂/T₂ at constant V,n; T in Kelvin
- `avogadros_law(V1, n1, V2, n2)` → float — Apply V₁/n₁ = V₂/n₂ at constant P,T
- `combined_gas_law(P1, V1, T1, P2, V2, T2, n=None, R=0.08206)` → float — Apply P₁V₁/T₁ = P₂V₂/T₂; pass None for unknown
- `celsius_to_kelvin(celsius)` → float — Convert °C to K (adds 273.15)
- `kelvin_to_celsius(kelvin)` → float — Convert K to °C (subtracts 273.15)
- `partial_pressure_dalton(mole_fraction, total_pressure)` → float — Calculate P_i = X_i × P_total
- `mole_fraction(moles_component, total_moles)` → float — Calculate X_i = n_i / n_total
- `dalton_law_partial_pressures(moles_dict, total_pressure)` → dict — Returns {'P_species': value} for all components

### Common errors:
- ❌ Using temperature in °C instead of Kelvin (MUST convert first with celsius_to_kelvin)
- ❌ Passing more than one None argument (exactly one unknown is required)
- ❌ Inconsistent pressure units within a problem (use all atm or all kPa)
