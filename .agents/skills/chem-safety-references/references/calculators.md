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

### hazardous_waste_compatibility

- `hazardous_waste_compatibility.lookup_chemical_storage_compatibility`: Look up an EPA hazardous-waste compatibility chart class pair.
- `hazardous_waste_compatibility.lookup_hazardous_waste_compatibility`: Look up EPA-600/2-80-076 hazards for two reactivity groups.

Private helpers and retired/test functions present in original module source are not advertised or callable through this interface.
