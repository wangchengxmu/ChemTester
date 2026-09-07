# Constraint-first inorganic reaction, coefficient, and transformation audit

**Retrieve with:** inorganic process equation audit, phase-aware reaction equation, verbal product constraint, single gas reaction constraint, coefficient scope audit, inorganic product identity, transformation bond audit

**Use when:** An inorganic reaction or multi-process equation-selection problem requires product identification, balancing, coefficient-derived quantities, enforcement of verbal constraints such as phase, product count, compound type, or gas identity and count, or exact evaluation of whether a structural feature was created or merely retained.

## Procedure

1. Translate every verbal condition into a pre-balance ledger of phases, product count and type, oxidation environment, gas classes, and required structural changes. Establish chemically credible products from the conditions before treating an atom-balanced equation as established; use an optional checker only if it is actually exposed in the active catalog.
2. Interpret a stated 1:1 ionic compound as one cation unit per anion unit. For a group-4 oxo cation MO2+ with sulfate, use the 1:1 oxosulfate MOSO4 rather than the 1:2 normal sulfate M(SO4)2; when this is coupled to acid-protonated nitride and one elemental gas, derive and atom-audit the constrained family before computing coefficients.
3. Propose products consistent with every constraint, reject any equation that introduces a forbidden extra product even if its atoms can be balanced, then balance atoms and charge and reduce the full equation to the smallest whole-number coefficient vector.
4. Label reactant-side, product-side, and full-equation coefficient sets. For each process, compute every requested sum, difference, product, ratio, primality, or coefficient occurrence only from the normalized set named by the wording and never carry values between processes.
5. For transformation claims, distinguish bonds or groups newly formed by the operation from structural features already present and merely retained.
6. Evaluate every statement independently against the same constraint, coefficient, and transformation ledgers, then check option-set uniqueness before selecting a single-best or catch-all response.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/inorganic_reaction_constraint_ledger.md
- chem-memory/L2_principles/equation_writing_and_balancing.md
- chem-memory/L3_functions/equation_balancing_tools.py
- https://webbook.nist.gov/cgi/cbook.cgi?ID=B6000546
- https://pubchem.ncbi.nlm.nih.gov/compound/6452562

## Guards

- Atom balance alone does not validate guessed product identities or satisfy verbal product constraints.
- An equation that releases two gases cannot satisfy a one-gas condition, and an elemental-gas constraint rejects compound gases such as SO2 even when only one gas formula appears.
- A stated 1:1 ionic product rejects a normal 1:2 sulfate when the chemistry instead specifies a divalent oxo cation paired with sulfate.
- The mathematical product of all coefficients includes both sides unless the wording explicitly restricts the scope.
- Normalize coefficients before computing any coefficient aggregate, and do not infer one process statement from another process's equation or coefficient ledger.
- Retention of an existing structural feature is not evidence that the stated transformation generated it.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.
