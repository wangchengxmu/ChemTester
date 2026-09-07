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

`numpy`, `scipy`.
Only the functions that import these packages require them. A `requirements.txt` records the package names; versions are not pinned or certified by this export.
Use an existing suitable environment or explain a missing dependency; do not silently install software.

## Function Index

Read `--describe` for full signatures and contracts; this index is not a substitute.

### integrated_rate_law_tools

- `integrated_rate_law_tools.calculate_r_squared`: Calculate R-squared for linear fit.
- `integrated_rate_law_tools.first_order_concentration`: Calculate concentration for first-order reaction.
- `integrated_rate_law_tools.first_order_half_life`: Calculate half-life for first-order reaction.
- `integrated_rate_law_tools.first_order_time`: Calculate time to reach concentration for first-order reaction.
- `integrated_rate_law_tools.half_life`: Calculate half-life for any order.
- `integrated_rate_law_tools.identify_order_from_data`: Identify reaction order from concentration vs time data.
- `integrated_rate_law_tools.second_order_concentration`: Calculate concentration for second-order reaction.
- `integrated_rate_law_tools.second_order_half_life`: Calculate half-life for second-order reaction.
- `integrated_rate_law_tools.second_order_time`: Calculate time to reach concentration for second-order reaction.
- `integrated_rate_law_tools.zero_order_concentration`: Calculate concentration for zero-order reaction.
- `integrated_rate_law_tools.zero_order_half_life`: Calculate half-life for zero-order reaction.
- `integrated_rate_law_tools.zero_order_time`: Calculate time to reach concentration for zero-order reaction.

### rate_law_solver

- `rate_law_solver.consecutive_first_order`: Calculate concentrations for consecutive first-order reactions.
- `rate_law_solver.determine_order_and_constant`: Automatically determine reaction order and rate constant from data.
- `rate_law_solver.determine_rate_constant_first_order`: Determine k from concentration-time data for first-order reaction.
- `rate_law_solver.determine_rate_constant_second_order`: Determine k from concentration-time data for second-order reaction.
- `rate_law_solver.determine_rate_constant_zero_order`: Determine k from concentration-time data for zero-order reaction.
- `rate_law_solver.half_life_first_order`: Calculate half-life for a first-order reaction.
- `rate_law_solver.half_life_second_order`: Calculate half-life for a second-order reaction.
- `rate_law_solver.half_life_zero_order`: Calculate half-life for a zero-order reaction.
- `rate_law_solver.integrated_first_order`: Calculate concentration vs time for first-order reaction.
- `rate_law_solver.integrated_second_order_equal`: Calculate concentration for second-order A + B -> products with [A]0 = [B]0.
- `rate_law_solver.integrated_second_order_one_reactant`: Calculate concentration vs time for second-order reaction (A -> products).
- `rate_law_solver.integrated_second_order_unequal`: Calculate concentrations for second-order A + B -> products with [A]0 != [B]0.
- `rate_law_solver.integrated_zero_order`: Calculate concentration vs time for zero-order reaction.
- `rate_law_solver.parallel_first_order`: Calculate concentrations for parallel first-order reactions.
- `rate_law_solver.reversible_first_order`: Calculate concentrations for reversible first-order reaction.
- `rate_law_solver.time_to_fraction_first_order`: Calculate time to reach a certain fraction of initial concentration.
- `rate_law_solver.time_to_fraction_second_order`: Calculate time to reach a certain fraction of initial concentration.
- `rate_law_solver.time_to_fraction_zero_order`: Calculate time to reach a certain fraction of initial concentration.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
