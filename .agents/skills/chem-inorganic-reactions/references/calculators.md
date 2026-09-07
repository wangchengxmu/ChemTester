# Optional Calculators

These are selected existing implementations, not independently certified chemistry.
Read a function's complete description, units, domain, and return type before calling it.
Legacy embedded empirical tables are approximate unless independently source-checked for the claim.
Do not equate an implementation's self-reported validation with independent verification.

## Invocation

Resolve scripts relative to this skill folder, not the caller's working directory.
Use the available Python 3.10+ environment. No provider key, Codex SDK, MCP service, or ChemTester checkout is required.

```text
python <skill-folder>/scripts/calculate.py --list
python <skill-folder>/scripts/calculate.py --describe module.function
python <skill-folder>/scripts/calculate.py --call module.function --arguments-json '{"parameter": 1.0}'
```

Replace the placeholder with an ID and arguments from its description.
A JSON error and nonzero exit code mean no usable result. Never reinterpret an error as an answer.

## Function Index

Read `--describe` for full signatures and contracts; this index is not a substitute.

### atomic_composition_tools

- `atomic_composition_tools.average_atomic_mass`: isotopes: [(mass, fractional_abundance), ...]
- `atomic_composition_tools.empirical_formula_from_percent`: Determine empirical formula from mass percentages.
- `atomic_composition_tools.molar_mass_from_formula`: Calculate molar mass from formula string. Handles parentheses like Ca3(PO4)2.
- `atomic_composition_tools.molarity`: Calculate molarity from mass, molar mass, and solution volume.
- `atomic_composition_tools.percent_composition`: Calculate mass percent of target_element in formula string.

### electrolysis_tools

- `electrolysis_tools.charge_from_current_time`: Calculate total charge passed.
- `electrolysis_tools.compare_galvanic_vs_electrolytic`: Determine if cell is galvanic or electrolytic.
- `electrolysis_tools.current_for_mass`: Calculate current needed to produce given mass in given time.
- `electrolysis_tools.electrons_transferred`: Calculate moles of electrons from charge.
- `electrolysis_tools.gas_volume_at_stp`: Calculate gas volume at STP (22.4 L/mol).
- `electrolysis_tools.mass_from_electrolysis`: Calculate mass of product from electrolysis using Faraday's law.
- `electrolysis_tools.minimum_voltage_for_electrolysis`: Calculate minimum voltage needed for electrolysis.
- `electrolysis_tools.moles_from_electrolysis`: Calculate moles of product from electrolysis.
- `electrolysis_tools.time_for_mass`: Calculate time needed to produce given mass by electrolysis.

### equation_balancing_tools

- `equation_balancing_tools.balance_by_inspection`: Balance equation using systematic coefficient search.
- `equation_balancing_tools.balance_redox_half_reaction`: Balance a one-reactant/one-product redox half-reaction.
- `equation_balancing_tools.check_balance`: Check if equation is balanced.
- `equation_balancing_tools.complete_to_net_ionic`: Remove spectator ions from complete ionic equation.
- `equation_balancing_tools.count_atoms`: Count atoms in a chemical formula with coefficient.
- `equation_balancing_tools.format_equation`: Format a balanced equation dict as a readable string.
- `equation_balancing_tools.molecular_to_ionic`: Convert molecular equation to complete ionic equation.
- `equation_balancing_tools.parse_formula`: Parse a chemical formula into element counts.

### nernst_equation

- `nernst_equation.cell_potential_from_K`: Calculate standard cell potential from equilibrium constant.
- `nernst_equation.cell_potential_from_half_reactions`: Calculate cell potential from half-reaction potentials.
- `nernst_equation.concentration_cell_potential`: Calculate potential of a concentration cell.
- `nernst_equation.equilibrium_constant_from_potential`: Calculate equilibrium constant K from standard cell potential.
- `nernst_equation.free_energy_from_potential`: Calculate Gibbs free energy change from cell potential.
- `nernst_equation.nernst_equation`: Calculate cell potential using the Nernst equation.
- `nernst_equation.nernst_equation_25C`: Calculate cell potential at 25degC using simplified Nernst equation.
- `nernst_equation.nernst_factor`: Calculate the Nernst factor (RT/F x ln(10) = 0.05916 V at 25degC).
- `nernst_equation.ph_from_hydrogen_electrode`: Calculate pH from hydrogen electrode potential.
- `nernst_equation.potential_from_free_energy`: Calculate cell potential from Gibbs free energy change.
- `nernst_equation.potential_from_ph`: Calculate hydrogen electrode potential at given pH.
- `nernst_equation.reaction_quotient`: Calculate reaction quotient Q from concentrations.
- `nernst_equation.standard_free_energy_from_potential`: Calculate standard Gibbs free energy change from standard cell potential.
- `nernst_equation.temperature_correction_factor`: Calculate temperature correction for the Nernst equation.

### periodic_trends_tools

- `periodic_trends_tools.bond_type_prediction`: Predict bond type between two elements based on electronegativity.
- `periodic_trends_tools.classify_element`: Classify element as metal, nonmetal, or metalloid.
- `periodic_trends_tools.compare_electronegativity`: Compare electronegativities of two elements.
- `periodic_trends_tools.oxide_type`: Predict if element oxide is acidic, basic, or amphoteric.
- `periodic_trends_tools.predict_atomic_radius_trend`: Predict which element has larger atomic radius.
- `periodic_trends_tools.predict_ionization_energy_trend`: Predict which element has higher ionization energy.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
