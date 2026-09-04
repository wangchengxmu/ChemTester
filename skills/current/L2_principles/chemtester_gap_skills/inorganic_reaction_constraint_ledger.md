# Constraint-first inorganic reaction and coefficient audit

**Retrieve with:** inorganic process equation audit, verbal product constraint, single gas reaction constraint, coefficient scope audit, inorganic product identity

**Use when:** An inorganic reaction or multi-process equation-selection problem requires product identification, balancing, coefficient-derived statements, or enforcement of verbal constraints such as phase, product count, compound type, or the identity and number of gases.

## Procedure

1. Translate every verbal condition into a pre-balance constraint ledger, including phases, product count and type, oxidation environment, and allowed gas classes; normalize translated language so one simple gaseous substance means exactly one elemental gas, then call reaction_constraint_tools.audit_gas_product_constraints and require accepted=true.
2. Interpret a stated 1:1 ionic compound as one cation unit per anion unit. For a group-4 oxo cation MO2+ with sulfate, use the 1:1 oxosulfate MOSO4 rather than the 1:2 normal sulfate M(SO4)2; when this is coupled to acid-protonated nitride and one elemental gas, derive and atom-audit the constrained family before computing coefficients.
3. Propose products consistent with every constraint, reject any equation that introduces a forbidden extra product even if its atoms can be balanced, then balance atoms and charge, reduce to the smallest whole-number vector, and label reactant-side, product-side, and full-equation coefficient sets.
4. For each process, compute every requested sum, difference, product, ratio, primality, or coefficient occurrence from that normalized ledger without carrying values between processes.
5. Evaluate every statement independently against the same constraint and coefficient ledgers, then check option-set uniqueness before selecting a single-best or catch-all response.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/inorganic_reaction_constraint_ledger.md
- chem-memory/L2_principles/equation_writing_and_balancing.md
- chem-memory/L3_functions/equation_balancing_tools.py
- chem-memory/L3_functions/reaction_constraint_tools.py
- https://webbook.nist.gov/cgi/cbook.cgi?ID=B6000546
- https://pubchem.ncbi.nlm.nih.gov/compound/6452562

## Guards

- Atom balance alone does not validate product identities or satisfy verbal product constraints.
- An equation that releases two gases cannot satisfy a one-gas condition, and an elemental-gas constraint rejects compound gases such as SO2 even when only one gas formula appears.
- A stated 1:1 ionic product rejects a normal 1:2 sulfate when the chemistry instead specifies a divalent oxo cation paired with sulfate.
- Normalize coefficients before computing any aggregate, and do not infer one process statement from another process's equation or coefficient ledger.
