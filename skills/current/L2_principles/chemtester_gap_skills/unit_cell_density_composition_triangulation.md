# Unit-cell density and composition constraint triangulation

**Retrieve with:** crystal density formula mass, unit cell Z molar mass, MOF solvent composition, metal oxide mass fraction

**Use when:** A crystalline coordination compound or porous framework identity must be inferred from cell parameters, density, Z, elemental ratios, included solvent or guests, and a decomposition-product composition.

## Procedure

1. Convert lattice lengths to a consistent unit, obtain the crystal-system cell volume, and infer formula-unit molar mass from M = rho*V*N_A/Z with V in cm^3.
2. Construct complete charge-balanced candidate formula units from linker, guest, and elemental-ratio evidence; include coordinated or occluded solvent when its elements are observed.
3. Round-trip each candidate with the framework-density calculation and compare discrepancies against the precision of the crystallographic measurements.
4. Calculate metal fractions for chemically plausible oxidation products, treating rounded percentages as corroborating tolerance bands rather than unique identifiers.
5. Select the identity satisfying all independent constraints, then map it to the requested answer format.

## Preferred Support

- chem-memory/L2_principles/crystallography.md
- chem-memory/L3_functions/crystallography_tools.py
- chem-memory/L2_principles/mof_synthesis_characterization.md
- chem-memory/L3_functions/mof_tools.py

## Guards

- Treat Z as formula units per cell, not an atom count.
- Convert cubic angstroms to cubic centimeters with 1e-24, or convert picometers before calculating volume.
- Do not omit solvent or guest mass when elemental evidence includes its atoms.
- Do not let one rounded oxide percentage override a precise cell-density and formula-mass match.
