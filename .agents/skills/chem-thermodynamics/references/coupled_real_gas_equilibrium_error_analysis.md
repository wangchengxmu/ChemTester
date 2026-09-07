# Coupled real-gas equilibrium and ideal-model error analysis

## Applicability

Use when an equilibrium composition, remaining phase, or reaction extent at fixed total pressure must be compared between ideal-gas and componentwise van der Waals models, especially when inert gases are present.

## Procedure

1. Form the standard reaction enthalpy and entropy, compute the standard Gibbs energy at the stated temperature, and obtain the dimensionless equilibrium constant; omit a pure condensed phase only while it remains present.
2. Parameterize every amount by reaction extent and common volume. For a stated separate-component van der Waals convention, set c_i=n_i/V, compute p_i=RTc_i/(1-b_i c_i)-a_i c_i^2, and enforce the total-pressure sum.
3. For thermodynamic real-gas equilibrium use activities f_i/f_standard with a consistent fugacity model. Use p_i/p_standard only as an ideal approximation or explicitly imposed pressure-quotient model; label that approximation, solve jointly for extent and volume, then compare the ideal model.
4. Convert both solutions to the requested mass, volume, or extent and compare their absolute difference before classifying its order of magnitude.
5. Check the correction scale with B_i=b_i-a_i/(RT) and Z_i-1 approximately B_i p_i/(RT); investigate any extent shift much larger than the underlying EOS deviations.

## Boundaries

- Include inert species in pressure and volume closure even though they are absent from the reaction quotient.
- Do not substitute total pressure for species activity. A componentwise EOS pressure sum is a stated modeling convention, not a general mixture rule; do not silently change an imposed model or claim exact equilibrium without fugacity support.
- Keep pressure activities dimensionless and use one consistent unit system for R, a, b, pressure, and volume.
- Require positive free volumes and inventory-bounded extents; if a condensed reactant is exhausted, switch to the appropriate phase regime.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
