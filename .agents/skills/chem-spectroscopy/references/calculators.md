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

### mass_spec_tools

- `mass_spec_tools.exact_mass`: Calculate exact mass using isotope masses.
- `mass_spec_tools.fragment_mass`: Calculate fragment mass from loss.
- `mass_spec_tools.identify_fragment_loss`: Identify the fragment lost from molecular ion.
- `mass_spec_tools.m_plus_one_intensity`: Calculate expected M+1 peak intensity.
- `mass_spec_tools.m_plus_two_intensity`: Calculate expected M+2 peak intensity.
- `mass_spec_tools.molecular_weight`: Calculate molecular weight from formula.
- `mass_spec_tools.nominal_mass`: Calculate nominal mass (integer mass of most abundant isotopes).

### nmr_splitting_tools

- `nmr_splitting_tools.coupling_relationship`: Identify coupled proton groups from coupling constants.
- `nmr_splitting_tools.intensity_ratios`: Calculate intensity ratios using n + 1 rule (Pascal's triangle).
- `nmr_splitting_tools.multiplet_name`: Return multiplet name from number of peaks.
- `nmr_splitting_tools.neighbors_from_multiplet`: Calculate number of neighboring protons from multiplet name.
- `nmr_splitting_tools.predict_spectrum_group`: Predict NMR signal for a group of equivalent protons.
- `nmr_splitting_tools.spectrum_group`: Alias for predict_spectrum_group - for solver compatibility.
- `nmr_splitting_tools.splitting_pattern`: Return multiplet name and intensity ratios for given neighbors.

### nmr_tools

- `nmr_tools.chemical_shift_to_freq`: Convert chemical shift (ppm) to frequency offset (Hz).
- `nmr_tools.coupling_constant`: Return J coupling constant in Hz (pass-through for unit consistency).
- `nmr_tools.multiplicity`: Predict signal multiplicity from n equivalent neighbors (n+1 rule).

### uv_vis_tools

- `uv_vis_tools.absorbance`: Calculate absorbance from Beer-Lambert law.
- `uv_vis_tools.absorbance_from_transmittance`: Calculate absorbance from transmittance.
- `uv_vis_tools.calibration_curve_params`: Calculate calibration curve parameters by linear regression.
- `uv_vis_tools.concentration_from_absorbance`: Calculate concentration from absorbance.
- `uv_vis_tools.concentration_from_calibration`: Calculate concentration from calibration curve.
- `uv_vis_tools.concentration_two_components`: Calculate concentrations of two components from absorbances at two wavelengths.
- `uv_vis_tools.diluted_concentration`: Calculate concentration after dilution.
- `uv_vis_tools.dilution_factor`: Calculate dilution factor.
- `uv_vis_tools.is_absorbance_valid`: Check if absorbance is in optimal range.
- `uv_vis_tools.molar_absorptivity`: Calculate molar absorptivity.
- `uv_vis_tools.original_concentration`: Calculate original concentration from diluted measurement.
- `uv_vis_tools.percent_transmittance_from_absorbance`: Calculate percent transmittance from absorbance.
- `uv_vis_tools.recommended_dilution`: Calculate recommended dilution factor to achieve target absorbance.
- `uv_vis_tools.standard_addition_concentration`: Calculate sample concentration by standard addition.
- `uv_vis_tools.transmittance_from_absorbance`: Calculate transmittance from absorbance.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
