# Phase-aware metal-ligand and redox speciation

**Retrieve with:** phase-aware reaction equation, inorganic product identity, coefficient scope audit, transformation bond audit

**Use when:** An inorganic reaction or equation-selection problem requires product identification, balancing, coefficient-derived quantities, or exact evaluation of structural transformation claims.

## Procedure

1. Establish credible products from conditions and chemical constraints before treating an atom-balanced equation as chemically established.
2. Balance atoms and charge, then reduce the full equation to the smallest whole-number coefficient vector.
3. Label reactant-side, product-side, and full-equation coefficient sets; apply sums, products, or ratios only to the set explicitly named by the wording.
4. For transformation claims, distinguish bonds or groups newly formed by the operation from features already present and merely retained.
5. Audit every statement against the same equation and transformation ledger, then check uniqueness before selecting a single-best or catch-all response.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/competing_complex_speciation.md
- chem-memory/L2_principles/equation_writing_and_balancing.md
- chem-memory/L3_functions/equation_balancing_tools.py

## Guards

- Atom balance alone does not validate guessed product identities.
- The mathematical product of all coefficients includes both sides unless the wording explicitly restricts the scope.
- Normalize coefficients before computing any coefficient aggregate.
- Retention of an existing structural feature is not evidence that the stated transformation generated it.
