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

### crystal_structures_tools

- `crystal_structures_tools.atoms_per_area_cubic`: Count atoms per unit area on crystal face.
- `crystal_structures_tools.bravais_lattice_types`: Return all Bravais lattice types organized by crystal system.
- `crystal_structures_tools.cubic_lattice_radius`: Calculate atomic radius from cubic unit cell edge length.
- `crystal_structures_tools.drude_resistivity`: Calculate electrical resistivity using the Drude model.
- `crystal_structures_tools.edge_length_from_radius`: Calculate unit cell edge length from atomic radius.
- `crystal_structures_tools.identify_crystal_system`: Identify crystal system from lattice parameters.
- `crystal_structures_tools.ionic_radius_ratio_rule`: Predict coordination number from radius ratio.
- `crystal_structures_tools.packing_fraction`: Calculate packing fraction for different crystal structures.
- `crystal_structures_tools.unit_cell_volume_cubic`: Calculate volume of cubic unit cell.

### crystallography_tools

- `crystallography_tools.atomic_radius_from_lattice`: Calculate atomic radius from lattice parameter for cubic structures.
- `crystallography_tools.atoms_per_unit_cell`: Return number of atoms per unit cell for common structures.
- `crystallography_tools.braggs_angle`: Calculate Bragg angle from wavelength and d-spacing.
- `crystallography_tools.braggs_law`: Apply Bragg's law: nlambda = 2d sin(θ)
- `crystallography_tools.coordination_number`: Return coordination number for common crystal structures.
- `crystallography_tools.crystal_density`: Calculate crystal density from unit cell parameters.
- `crystallography_tools.d_spacing_cubic`: Calculate d-spacing for cubic system.
- `crystallography_tools.d_spacing_from_bragg`: Calculate d-spacing from Bragg's law.
- `crystallography_tools.d_spacing_general`: Calculate d-spacing for any crystal system.
- `crystallography_tools.d_spacing_hexagonal`: Calculate d-spacing for hexagonal system.
- `crystallography_tools.d_spacing_monoclinic`: Calculate d-spacing for monoclinic system.
- `crystallography_tools.d_spacing_orthorhombic`: Calculate d-spacing for orthorhombic system.
- `crystallography_tools.d_spacing_tetragonal`: Calculate d-spacing for tetragonal system.
- `crystallography_tools.diffraction_angles_for_planes`: Calculate diffraction angles for multiple crystal planes.
- `crystallography_tools.get_xray_wavelength`: Get X-ray wavelength for common sources.
- `crystallography_tools.higher_order_angles`: Calculate Bragg angles for higher-order reflections.
- `crystallography_tools.identify_crystal_system_from_params`: Identify crystal system from lattice parameters.
- `crystallography_tools.intercepts_to_miller`: Convert intercepts to Miller indices.
- `crystallography_tools.is_reflection_possible`: Check if reflection is possible given n, lambda, and d.
- `crystallography_tools.lattice_parameter_from_radius`: Calculate lattice parameter from atomic radius for cubic structures.
- `crystallography_tools.miller_to_intercepts`: Convert Miller indices to intercepts.
- `crystallography_tools.packing_fraction`: Return packing fraction (efficiency) for common crystal structures.
- `crystallography_tools.path_difference`: Calculate path difference between rays from adjacent planes.
- `crystallography_tools.unit_cell_volume`: Calculate unit cell volume for any crystal system.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
