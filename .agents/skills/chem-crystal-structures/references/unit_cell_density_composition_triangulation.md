# Unit-cell density and composition constraint triangulation

## Applicability

A crystalline coordination compound or porous framework identity must be inferred from cell parameters, density, Z, elemental ratios, included solvent or guests, and a decomposition-product composition.

## Procedure

1. Convert lattice lengths to a consistent unit, obtain the crystal-system cell volume, and infer formula-unit molar mass from M = rho*V*N_A/Z with V in cm^3.
2. Construct complete charge-balanced candidate formula units from linker, guest, and elemental-ratio evidence; include coordinated or occluded solvent when its elements are observed.
3. Round-trip each candidate with the framework-density calculation and compare discrepancies against the precision of the crystallographic measurements.
4. Calculate metal fractions for chemically plausible oxidation products, treating rounded percentages as corroborating tolerance bands rather than unique identifiers.
5. Select the identity satisfying all independent constraints, then map it to the requested answer format.

## Boundaries

- Treat Z as formula units per cell, not an atom count.
- Convert cubic angstroms to cubic centimeters with 1e-24, or convert picometers before calculating volume.
- Do not omit solvent or guest mass when elemental evidence includes its atoms.
- Do not let one rounded oxide percentage override a precise cell-density and formula-mass match.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
