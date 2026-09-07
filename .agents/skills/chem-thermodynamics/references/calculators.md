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

### enthalpy_tools

- `enthalpy_tools.delta_H_rxn_from_formation`: Calculate standard enthalpy of reaction from formation enthalpies.
- `enthalpy_tools.heat_exchange_poly`: Calculate heat removed/added for a mixture with polynomial Cp, per component.
- `enthalpy_tools.heat_of_combustion_per_gram`: Calculate heat released per gram of fuel.
- `enthalpy_tools.heat_of_combustion_per_volume`: Calculate heat released per volume of liquid fuel.
- `enthalpy_tools.heat_phase_change`: Calculate heat for phase change.
- `enthalpy_tools.hess_from_reactions`: Calculate unknown enthalpy using Hess's Law.
- `enthalpy_tools.hess_law_combine`: Apply Hess's Law to combine reaction enthalpies.
- `enthalpy_tools.integrated_cp_poly`: Integrate polynomial heat capacity Cp = A + BT + CT² + DT³ from T1 to T2.
- `enthalpy_tools.multiply_reaction`: Multiply reaction by factor (multiply DeltaH by factor).
- `enthalpy_tools.reverse_reaction`: Reverse a reaction (multiply DeltaH by -1).
- `enthalpy_tools.total_heat_with_phase_change`: Calculate total heat for temperature change through phase transition.

### gas_laws_tools

- `gas_laws_tools.avogadros_law`: Apply Avogadro's Law: V1/n1 = V2/n2 (constant P, T).
- `gas_laws_tools.boyles_law`: Apply Boyle's Law: P1V1 = P2V2 (constant T, n).
- `gas_laws_tools.celsius_to_kelvin`: Convert Celsius to Kelvin.
- `gas_laws_tools.charles_law`: Apply Charles's Law: V1/T1 = V2/T2 (constant P, n).
- `gas_laws_tools.combined_gas_law`: Apply Combined Gas Law: P1V1/T1 = P2V2/T2 (constant n).
- `gas_laws_tools.dalton_law_partial_pressures`: Calculate all partial pressures from mole amounts and total pressure.
- `gas_laws_tools.gay_lussacs_law`: Apply Gay-Lussac's Law: P1/T1 = P2/T2 (constant V, n).
- `gas_laws_tools.kelvin_to_celsius`: Convert Kelvin to Celsius.
- `gas_laws_tools.mole_fraction`: Calculate mole fraction from component moles and total moles.
- `gas_laws_tools.partial_pressure_dalton`: Calculate partial pressure from mole fraction and total pressure.

### gibbs_free_energy_tools

- `gibbs_free_energy_tools.G_from_equilibrium_constant`: Calculate standard free energy change from equilibrium constant.
- `gibbs_free_energy_tools.equilibrium_constant_from_G`: Calculate equilibrium constant from standard free energy change.
- `gibbs_free_energy_tools.gibbs_free_energy`: Calculate Gibbs free energy change.
- `gibbs_free_energy_tools.lookup_Gf`: Look up standard Gibbs free energy of formation.
- `gibbs_free_energy_tools.maximum_work`: Calculate maximum useful work from a spontaneous process.
- `gibbs_free_energy_tools.spontaneity_from_G`: Determine spontaneity from DeltaG.
- `gibbs_free_energy_tools.standard_G_from_formation`: Calculate standard free energy change from formation values.
- `gibbs_free_energy_tools.temperature_spontaneity_range`: Determine temperature range for spontaneity.

### ideal_gas_law_tools

- `ideal_gas_law_tools.gas_density`: Calculate density of a gas.
- `ideal_gas_law_tools.gas_stoichiometry`: Calculate product amounts from gas volume stoichiometry.
- `ideal_gas_law_tools.ideal_gas_law`: Apply the ideal gas law: PV = nRT.
- `ideal_gas_law_tools.mass_at_stp`: Calculate mass of gas at STP from volume.
- `ideal_gas_law_tools.molar_mass_from_gas`: Calculate molar mass from gas density.
- `ideal_gas_law_tools.molar_volume`: Calculate molar volume of ideal gas at given conditions.
- `ideal_gas_law_tools.moles_at_stp`: Calculate moles of gas at STP (22.4 L/mol).
- `ideal_gas_law_tools.volume_at_stp`: Calculate volume of gas at STP (22.4 L/mol).

### thermodynamic_data_tools

- `thermodynamic_data_tools.calculate_hess_law`: Calculate reaction enthalpy via Hess's law: Σ nDeltaHdegf(products) - Σ nDeltaHdegf(reactants).
- `thermodynamic_data_tools.calculate_reaction_entropy`: DeltaSdegrxn = Σ nSdeg(products) - Σ nSdeg(reactants). Returns J/(mol·K).
- `thermodynamic_data_tools.calculate_reaction_gibbs`: DeltaGdegrxn = Σ nDeltaGdegf(products) - Σ nDeltaGdegf(reactants). Returns kJ/mol.
- `thermodynamic_data_tools.lookup_formation_enthalpy`: DeltaHdegf in kJ/mol for the given species.
- `thermodynamic_data_tools.lookup_formation_gibbs`: DeltaGdegf in kJ/mol for the given species.
- `thermodynamic_data_tools.lookup_heat_capacity`: Cp in J/(mol·K) for the given species.
- `thermodynamic_data_tools.lookup_standard_entropy`: Sdeg in J/(mol·K) for the given species.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
