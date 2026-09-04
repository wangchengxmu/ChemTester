# Coupled real-gas equilibrium and ideal-model error analysis

**Retrieve with:** van der Waals reaction equilibrium, ideal versus real gas error, inert gas equilibrium pressure, coupled EOS reaction extent

**Use when:** Use when an equilibrium composition, remaining phase, or reaction extent at fixed total pressure must be compared between ideal-gas and componentwise van der Waals models, especially when inert gases are present.

## Procedure

1. Form the standard reaction enthalpy and entropy, compute the standard Gibbs energy at the stated temperature, and obtain the dimensionless equilibrium constant; omit a pure condensed phase only while it remains present.
2. Parameterize every amount by reaction extent and common volume. For a stated separate-component van der Waals convention, set c_i=n_i/V, compute p_i=RTc_i/(1-b_i c_i)-a_i c_i^2, and enforce the total-pressure sum.
3. Enforce the dimensionless equilibrium relation using component pressures, or fugacities only when explicitly required, and solve jointly for extent and volume on the feasible branch; repeat with a_i=b_i=0 for the ideal comparison.
4. Convert both solutions to the requested mass, volume, or extent and compare their absolute difference before classifying its order of magnitude.
5. Check the correction scale with B_i=b_i-a_i/(RT) and Z_i-1 approximately B_i p_i/(RT); investigate any extent shift much larger than the underlying EOS deviations.

## Preferred Support

- chem-memory/L2_principles/reaction_equilibrium_thermo.md
- chem-memory/L2_principles/non_ideal_gases.md
- chem-memory/L2_principles/gas_mixtures.md
- chem-memory/L2_principles/chemtester_gap_skills/real_gas_compressibility_state_selection.md
- chem-memory/L3_functions/non_ideal_gas_tools.py

## Guards

- Include inert species in pressure and volume closure even though they are absent from the reaction quotient.
- Do not substitute total pressure for component pressure or silently introduce fugacity and mixture rules beyond the stated model.
- Keep pressure activities dimensionless and use one consistent unit system for R, a, b, pressure, and volume.
- Require positive free volumes and inventory-bounded extents; if a condensed reactant is exhausted, switch to the appropriate phase regime.
