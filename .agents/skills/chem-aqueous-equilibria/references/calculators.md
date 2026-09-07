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

## Optional Dependencies

`numpy`.
Only the functions that import these packages require them. A `requirements.txt` records the package names; versions are not pinned or certified by this export.
Use an existing suitable environment or explain a missing dependency; do not silently install software.

## Function Index

Read `--describe` for full signatures and contracts; this index is not a substitute.

### acid_base_constants_tools

- `acid_base_constants_tools.Ka_Kb_relationship`: Calculate Ka from Kb or vice versa.
- `acid_base_constants_tools.compare_acid_strengths`: Compare relative acid strengths.
- `acid_base_constants_tools.conjugate_base_strength`: Calculate Kb of conjugate base.
- `acid_base_constants_tools.is_strong_acid`: Determine if acid is strong based on Ka.
- `acid_base_constants_tools.is_strong_base`: Determine if base is strong based on Kb.
- `acid_base_constants_tools.percent_ionization`: Calculate percent ionization of a weak acid.
- `acid_base_constants_tools.validate_approximation`: Check if small x approximation is valid.
- `acid_base_constants_tools.weak_acid_pH`: Calculate pH of weak acid solution.
- `acid_base_constants_tools.weak_base_pH`: Calculate pH of weak base solution.

### acid_base_tools

- `acid_base_tools.calculate_pka_conjugate`: Calculate pKb from pKa (in water at 25degC). pKa + pKb = 14.
- `acid_base_tools.hsab_classify`: Classify acid as hard, soft, or borderline based on hardness parameter.
- `acid_base_tools.hsab_compatibility`: Predict acid-base adduct stability: hard-hard, soft-soft preferred.

### buffer_calculator

- `buffer_calculator.buffer_after_strong_acid`: Calculate new pH after adding strong acid to buffer.
- `buffer_calculator.buffer_after_strong_base`: Calculate new pH after adding strong base to buffer.
- `buffer_calculator.buffer_capacity_approximate`: Approximate buffer capacity near pKa.
- `buffer_calculator.buffer_capacity_exact`: Calculate exact buffer capacity using the Van Slyke equation.
- `buffer_calculator.buffer_concentrations_from_ratio`: Calculate acid and base concentrations from total concentration and ratio.
- `buffer_calculator.buffer_pH_with_activity`: Calculate buffer pH with activity correction.
- `buffer_calculator.buffer_range`: Calculate effective buffer range.
- `buffer_calculator.carbonate_buffer`: Calculate pH of carbonate buffer.
- `buffer_calculator.citrate_buffer`: Calculate pH of citrate buffer.
- `buffer_calculator.debye_huckel_activity`: Calculate activity coefficient using Debye-Hückel limiting law.
- `buffer_calculator.design_buffer`: Design a buffer to achieve target pH.
- `buffer_calculator.dilution_effect`: Estimate pH change upon dilution.
- `buffer_calculator.grams_needed`: Calculate grams of compound needed.
- `buffer_calculator.henderson_hasselbalch`: Calculate buffer pH using Henderson-Hasselbalch equation.
- `buffer_calculator.ionic_strength`: Calculate ionic strength of a solution.
- `buffer_calculator.is_effective_buffer`: Check if pKa is suitable for target pH.
- `buffer_calculator.phosphate_buffer`: Calculate pH of phosphate buffer (H2PO4-/HPO42-).
- `buffer_calculator.polyprotic_buffer_pH`: Calculate pH for polyprotic buffer system (H2A/HA-/A2-).
- `buffer_calculator.prepare_buffer_by_mixing`: Calculate masses needed to prepare buffer by mixing acid and base salts.
- `buffer_calculator.prepare_buffer_by_neutralization`: Calculate volumes needed to prepare buffer by partial neutralization.

### equilibrium_constant_tools

- `equilibrium_constant_tools.Kc_to_Kp`: Convert Kc to Kp.
- `equilibrium_constant_tools.Kp_to_Kc`: Convert Kp to Kc.
- `equilibrium_constant_tools.Q_expression_string`: Generate Q expression string.
- `equilibrium_constant_tools.calculate_Kc`: Calculate Kc from equilibrium concentrations.
- `equilibrium_constant_tools.calculate_Qp`: Calculate Qp from partial pressures.
- `equilibrium_constant_tools.concentration_from_Kc`: Calculate unknown equilibrium concentration from Kc.
- `equilibrium_constant_tools.interpret_K`: Interpret the meaning of K value.

### equilibrium_tools

- `equilibrium_tools.equilibrium_concentrations`: Solve ICE table to find equilibrium concentrations given K and initial conditions.
- `equilibrium_tools.equilibrium_constant`: Calculate Kc from equilibrium concentrations using signed stoichiometry.
- `equilibrium_tools.equilibrium_expression`: Generate equilibrium constant expression.
- `equilibrium_tools.equilibrium_from_composition`: Calculate K and equilibrium concentrations from initial conditions and extent of reaction.
- `equilibrium_tools.equilibrium_from_rates`: Calculate equilibrium constant from rate constants.
- `equilibrium_tools.ice_table`: Calculate Kc from ICE table data.
- `equilibrium_tools.is_homogeneous`: Check if equilibrium is homogeneous (same phase).
- `equilibrium_tools.kc_from_kp`: Convert Kp to Kc: Kc = Kp / (RT)^delta_n
- `equilibrium_tools.kp_from_kc`: Convert Kc to Kp: Kp = Kc * (RT)^delta_n
- `equilibrium_tools.omit_from_expression`: Determine if species should be omitted from Q expression.
- `equilibrium_tools.predict_direction`: Predict reaction direction from Q and K comparison.
- `equilibrium_tools.rate_equality_condition`: Check if forward and reverse rates are equal.
- `equilibrium_tools.reaction_quotient`: Calculate reaction quotient Q from concentrations.
- `equilibrium_tools.reaction_quotient_v2`: Calculate reaction quotient Q using the same stoichiometry format as equilibrium_constant.

### ph_calculations_tools

- `ph_calculations_tools.H3O_from_pH`: Calculate [H3O+] from pH.
- `ph_calculations_tools.Ka_from_pKa`: Calculate Ka from pKa.
- `ph_calculations_tools.Kb_from_pKb`: Calculate Kb from pKb.
- `ph_calculations_tools.OH_from_pOH`: Calculate [OH-] from pOH.
- `ph_calculations_tools.classify_by_pH`: Classify solution by pH value.
- `ph_calculations_tools.pH_from_H3O`: Calculate pH from hydronium ion concentration.
- `ph_calculations_tools.pH_to_pOH`: Convert pH to pOH.
- `ph_calculations_tools.pKa_from_Ka`: Calculate pKa from Ka.
- `ph_calculations_tools.pKb_from_Kb`: Calculate pKb from Kb.
- `ph_calculations_tools.pOH_from_OH`: Calculate pOH from hydroxide ion concentration.
- `ph_calculations_tools.pOH_to_pH`: Convert pOH to pH.
- `ph_calculations_tools.significant_figures_pH`: Report pH with appropriate significant figures.
- `ph_calculations_tools.weak_acid_Ka_from_pH`: Calculate Ka from pH and concentration for a weak acid.
- `ph_calculations_tools.weak_acid_pH`: Calculate pH of a weak acid solution.
- `ph_calculations_tools.weak_base_pH`: Calculate pH of a weak base solution using unit activity coefficients.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
