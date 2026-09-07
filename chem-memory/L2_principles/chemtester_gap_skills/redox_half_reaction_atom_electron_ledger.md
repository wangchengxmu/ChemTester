# Atom-scaled redox half-reaction electron ledger

**Retrieve with:** balance acidic half reaction, redox electron count, molecular redox product scaling, atom charge balance audit

**Use when:** A half-reaction must be balanced in acidic or basic medium, especially when a polyatomic reactant forms a molecular product containing multiple atoms of the redox-active element.

## Procedure

1. First balance the redox-active element, including any factor required by a diatomic or polyatomic product; do not calculate electrons on an unscaled skeleton.
2. For a one-reactant to one-product half-reaction, call equation_balancing_tools.balance_redox_half_reaction with formulas, charges, and medium; require its structured atom and charge audit to report balanced before using the electron count.
3. Balance oxygen with water and hydrogen with hydrogen ion in acidic medium; for basic medium, complete the acidic form first and then neutralize hydrogen ion with hydroxide.
4. Place electrons on the side that makes total charge equal, and independently verify the count as oxidation-state change per atom multiplied by the number of transformed atoms.
5. Recount every element and net charge on both sides, reduce to the smallest valid integer coefficients, and only then map electron side and count to an answer choice.

## Preferred Support

- chem-memory/L2_principles/electrochemistry.md
- chem-memory/L2_principles/organic_redox.md
- chem-memory/L2_principles/equation_writing_and_balancing.md
- chem-memory/L3_functions/equation_balancing_tools.py

## Guards

- Multiply a per-atom oxidation-number change by every transformed atom in the balanced skeleton.
- Electrons appear on the reactant side for a reduction and on the product side for an oxidation.
- Never infer the electron count before balancing the redox-active element.
- A valid half-reaction must conserve both atoms and net charge.
