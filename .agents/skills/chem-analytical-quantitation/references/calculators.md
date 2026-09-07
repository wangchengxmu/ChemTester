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

### amount_conversion_tools

- `amount_conversion_tools.convert_amount`: Generic converter among: mass_g, moles, particles.
- `amount_conversion_tools.dilution_final_conc`: Calculate final concentration after dilution: M2 = M1*V1/V2.
- `amount_conversion_tools.dilution_volume`: Calculate V1 needed for dilution: M1*V1 = M2*V2.

### density_tools

- `density_tools.buoyancy_correction`: Apply air buoyancy correction to a mass measurement.
- `density_tools.calculate_density`: Calculate density (g/mL or g/cm3) from mass (g) and volume (mL).
- `density_tools.calculate_specific_gravity`: Calculate specific gravity (dimensionless).
- `density_tools.mass_from_density`: Calculate mass from density and volume.
- `density_tools.volume_from_density`: Calculate volume from density and mass.

### solution_concentration_tools

- `solution_concentration_tools.dilution`: Calculate dilution using M1V1 = M2V2.
- `solution_concentration_tools.mass_percent`: Calculate mass percentage.
- `solution_concentration_tools.molality`: Calculate molality of a solution.
- `solution_concentration_tools.molality_to_molarity`: Convert molality to molarity.
- `solution_concentration_tools.molarity`: Calculate molarity of a solution.
- `solution_concentration_tools.molarity_from_moles`: Calculate molarity from moles and volume.
- `solution_concentration_tools.molarity_to_molality`: Convert molarity to molality.
- `solution_concentration_tools.mole_fraction`: Calculate mole fractions for all components.
- `solution_concentration_tools.parts_per_to_molarity`: Convert ppm to molarity for aqueous solutions.
- `solution_concentration_tools.ppm_ppb`: Convert between ppm and ppb.

### stoichiometric_conversion_tools

- `stoichiometric_conversion_tools.empirical_formula`: Determine empirical formula from percent composition.
- `stoichiometric_conversion_tools.ideal_gas_moles`: Calculate moles from ideal gas law: n = PV/RT
- `stoichiometric_conversion_tools.limiting_reactant`: Identify limiting reactant and theoretical yield.
- `stoichiometric_conversion_tools.mass_from_moles`: Alias for moles_to_mass.
- `stoichiometric_conversion_tools.mass_to_mass`: Convert mass of substance A to mass of substance B.
- `stoichiometric_conversion_tools.mass_to_moles`: Convert mass to moles.
- `stoichiometric_conversion_tools.mole_to_mole`: Convert moles of substance A to moles of substance B.
- `stoichiometric_conversion_tools.moles_from_mass`: Alias for mass_to_moles.
- `stoichiometric_conversion_tools.moles_to_mass`: Convert moles to mass.
- `stoichiometric_conversion_tools.moles_to_particles`: Convert moles to number of particles using Avogadro's number.
- `stoichiometric_conversion_tools.particles_to_moles`: Convert number of particles to moles using Avogadro's number.
- `stoichiometric_conversion_tools.percent_yield`: Calculate percent yield.
- `stoichiometric_conversion_tools.solution_molarity`: Calculate molarity from moles and volume.
- `stoichiometric_conversion_tools.solution_moles`: Calculate moles from solution molarity and volume.
- `stoichiometric_conversion_tools.stoichiometric_calculation`: Full stoichiometric calculation: moles of given → mass of target.

### unit_conversion_tools

- `unit_conversion_tools.calculate_molar_mass`: Calculate molar mass (g/mol) from a chemical formula (e.g. 'H2O', 'C6H12O6', 'Ca(OH)2').
- `unit_conversion_tools.convert_concentration`: Convert concentration between M, mM, muM, g/L, %w/v, ppm, ppb.
- `unit_conversion_tools.convert_energy`: Convert energy between J, kJ, cal, kcal, eV, L·atm.
- `unit_conversion_tools.convert_length`: Convert length between m, cm, mm, nm, pm, Å, in.
- `unit_conversion_tools.convert_mass`: Convert mass between g, kg, mg, lb, oz, amu.
- `unit_conversion_tools.convert_pressure`: Convert pressure between atm, Pa, kPa, bar, mmHg, torr.
- `unit_conversion_tools.convert_temperature`: Convert temperature between C, K, F.
- `unit_conversion_tools.convert_volume`: Convert volume between L, mL, m3, cm3, gal, fl_oz.
- `unit_conversion_tools.ideal_gas_law`: Solve PV = nRT for the unknown variable.
- `unit_conversion_tools.mass_to_moles`: Convert mass (g) to moles.
- `unit_conversion_tools.moles_to_mass`: Convert moles to mass (g).

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
