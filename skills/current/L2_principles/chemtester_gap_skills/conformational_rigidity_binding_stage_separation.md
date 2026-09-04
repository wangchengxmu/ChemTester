# Separate conformational access from conditional binding stabilization

**Retrieve with:** ligand rigidity bioactive conformation, cyclization conformational preorganization, binding affinity conformational entropy, negative-polarity scaffold comparison

**Use when:** A medicinal-chemistry comparison asks how cyclization or scaffold rigidity affects conformational access, productive recognition, affinity, selectivity, or interaction strength, especially in a negative-polarity multiple-choice task.

## Procedure

1. Lock the requested polarity before judging the choices, and restate whether the task seeks the true or false claim.
2. Separate free-ligand conformational access from conditional stabilization of a bound complex; these are different stages and can change in different directions.
3. Treat rigidity as narrowing the accessible ensemble. Infer better binding only when that ensemble is known to include a target-compatible bioactive geometry; otherwise rigidity can reduce the chance of reaching one.
4. Truth-value every choice under the same comparison scope, reject unconditional causal overclaims, and emit the requested answer token with a concise rationale.

## Guards

- Do not infer target complementarity from rigidity or cyclization alone.
- Do not equate fewer conformations with automatically favorable binding entropy or affinity; geometry, strain, enthalpy, and solvation can offset it.
- For negative-polarity questions, independently audit every choice before selecting one.
