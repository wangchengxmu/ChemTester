# Role-scoped temperatures and online answer provenance

**Retrieve with:** gas law multiple temperatures, manometer liquid temperature, online answer provenance, uncalled deterministic override

**Use when:** A calculation supplies quantities with different physical roles, or an online model answer is converted into structured output after retrieval or tool use.

## Procedure

1. Assign every temperature, pressure, concentration, mass, and volume an explicit physical role before binding equations or tool arguments; textual proximity is not sufficient.
2. For a gas-manometer calculation, assign the gas-sample temperature to T in PV=nRT and use the liquid temperature only to select or interpret manometer-fluid density.
3. Treat retrieved knowledge and explicitly successful tool calls as supporting evidence. Check argument roles, units, physical bounds, and agreement with an independent derivation.
4. For online routes, record numeric values from the model's explicit final-answer line after evidence adjudication. Restrict legacy specialized synthesis to offline deterministic routes.

## Preferred Support

- chem-memory/L2_principles/gas_law_manometer_unit_conversion_support.md
- .agents/skills/chemistry-tool-runtime/SKILL.md

## Guards

- Do not bind a quantity merely because it is nearest an apparatus noun.
- Do not let a successful tool status substitute for validation of its arguments or scientific result.
- Never label an uncalled heuristic as tool evidence or let any post-processing overwrite a valid online-model final answer.
