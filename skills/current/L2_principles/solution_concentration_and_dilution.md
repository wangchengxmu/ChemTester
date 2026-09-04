---
id: stoich.solution_concentration_dilution
layer: 2
title: Solution Concentration and Dilution
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/solution_concentration_tools.py
  - ../L4_reference/reference/solution-concentration-reference.md
  - ../L5_examples/stoichiometry/solution-concentration/
cross_links:
  - ./quantitative_measurement_and_uncertainty.md
  - ./amount_mole_mass_particle_conversion.md
status: active
---

## Problem intent
Route molarity, dilution, and non-molar concentration unit conversion tasks.

## Canonical equations
- \(C = n/V\), \(n = CV\)
- \(C_1V_1 = C_2V_2\) (only when solute amount is conserved)
- \(%m/m\), \(%v/v\), \(%m/v\), ppm, ppb definitions.

## Decision stub
1. Classify concentration representation (molar, percent, trace).
2. Normalize units and identify whether density is required.
3. Use solute-conservation branch for dilution-only cases.
4. Validate physical plausibility and report units clearly.

## Multi-Step Dilution Tracking

When a problem describes multiple sequential dilutions followed by a measurement:

1. **Trace each dilution step separately:**
   - Step 1: "10g sample → 250mL flask" → C_original = mass_analyte / 0.250 L
   - Step 2: "10mL aliquot → 25mL flask" → C_in_flask = C_original × (V_aliquot / V_original) × (V_original / V_flask) = C_original × V_aliquot / V_flask
   - Step 3: "10mL aliquot + 5mL standard → diluted to 25mL" → C_analyte_in_flask = C_original × V_aliquot / V_flask_final, C_standard_in_flask = C_std × V_std / V_flask_final

2. **Key rule:** When an aliquot is taken from one flask and put into another, the analyte amount (moles or mass) is conserved, but concentration changes based on the FINAL volume of the new flask.

3. **For standard addition with dilution:**
   - C_analyte_in_flask = C_sample × V_sample_portion / V_final_flask
   - C_standard_in_flask = C_std × V_std_added / V_final_flask
   - Signal ∝ C_analyte + C_standard (both in the same flask)
   - Use these flask concentrations in the standard addition formula

4. **Common mistake:** Using the ORIGINAL solution concentration directly instead of the DILUTED concentration in the measurement flask. Always compute the concentration IN THE FLASK WHERE THE SIGNAL IS MEASURED.

## Pass-3 fill targets
- Density-dependent conversion decision tree.
- Dilution limitations when reaction/association occurs.
- Trace concentration rounding and reporting conventions.

## L3 Tool Call Directives

**Source:** solution_concentration_tools.py
Concentration units, conversions, and dilution calculations.

### Available functions:
- mole_fraction(components: Dict[str, float]) → Dict[str, float] — Mole fractions for all components
- molality(moles_solute: float, kg_solvent: float) → float — mol/kg
- molarity(moles_solute: float, L_solution: float) → float — mol/L
- molarity_from_moles(moles: float, volume: float, unit='L') → float — Auto-converts mL→L
- molality_to_molarity(m, density, molar_mass_solute, molar_mass_solvent=18.015) → float
- molarity_to_molality(M, density, molar_mass_solute) → float
- mass_percent(mass_solute: float, mass_solution: float) → float
- ppm_ppb(concentration: float, unit='ppm') → float — Convert ppm↔ppb
- dilution(M1, V1, M2=None, V2=None) → float — M₁V₁ = M₂V₂; one of M2/V2 must be None
- parts_per_to_molarity(ppm: float, molar_mass: float, density=1.0) → float — ppm→M for aqueous

### Common errors:
- ❌ Confusing molarity (solution volume) vs molality (solvent mass)
- ❌ Both M2 and V2 provided to dilution (exactly one must be None)
