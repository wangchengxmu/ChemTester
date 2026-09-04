# Role-scoped physical quantity binding

**Retrieve with:** step-growth polymerization time, Carothers second-order kinetics, functional-group concentration basis, polyesterification rate law

**Use when:** A quantitative chemistry problem supplies a concentration that could denote molecules, reactive groups, or the concentration variable of an integrated rate law, especially in step-growth kinetics.

## Procedure

1. Label every concentration by species and basis, then write the governing rate law and the units of its rate constant before converting anything.
2. For stoichiometric bifunctional step growth, obtain conversion from Xn=1/(1-p), so p=1-1/Xn.
3. For equal-concentration second-order kinetics, set ct=c0(1-p)=c0/Xn and use t=(1/ct-1/c0)/k=(Xn-1)/(k*c0), optionally through second_order_time.
4. Use the problem-supplied initial concentration directly when it is the concentration variable of the stated or standard integrated law; apply a functionality factor only when a different molecular or group basis is explicitly defined and the rate constant uses that same basis.
5. Check units and back-substitute the result into 1+k*c0*t=Xn.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/role_scoped_quantity_binding.md
- chem-memory/L2_principles/polymerization_kinetics.md
- chem-memory/L3_functions/polymer_chemistry.py
- chem-memory/L3_functions/integrated_rate_law_tools.py

## Guards

- Do not multiply a supplied concentration by monomer functionality from the monomer label alone.
- Never combine a molecule-based concentration with a functional-group-based rate constant or rate law.
- Treat successful tool execution as evidence only; verify argument basis, units, and back-substitution.
