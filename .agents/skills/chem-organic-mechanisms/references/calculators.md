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

### functional_group_tools

- `functional_group_tools.classify_electron_effect`: Classify whether a group is electron-withdrawing or donating.
- `functional_group_tools.determine_principal_group`: Determine the principal functional group for naming.
- `functional_group_tools.functional_group_summary`: Get a summary table of all functional groups.
- `functional_group_tools.get_naming_priority`: Get the naming priority of a functional group.
- `functional_group_tools.get_prefix`: Get the IUPAC prefix for a functional group.
- `functional_group_tools.get_suffix`: Get the IUPAC suffix for a functional group.
- `functional_group_tools.identify_functional_groups`: Identify functional groups present in a molecule.
- `functional_group_tools.predict_boiling_point_trend`: Predict boiling point trend based on functional groups.
- `functional_group_tools.predict_solubility`: Predict water solubility based on functional groups.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
