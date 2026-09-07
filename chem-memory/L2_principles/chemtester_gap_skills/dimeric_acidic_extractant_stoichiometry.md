# Dimeric acidic-extractant stoichiometry and precision audit

**Retrieve with:** dimeric acidic extractant slope analysis, distribution ratio ligand stoichiometry, solvent extraction equilibrium constant, extractant dimer concentration exponent

**Use when:** Liquid-liquid extraction data at two or more extractant concentrations and acidities must be used to infer a neutral metal complex, write the extraction reaction, calculate its equilibrium constant, or audit numbered statements.

## Procedure

1. Use charge balance first: if singly charged A- is the only anionic ligand in a neutral extracted complex of M raised to z+, its deprotonated-ligand coefficient is z.
2. Let n be the number of H2A2 dimers consumed and write M raised to z+ plus n H2A2 as extracted complex M(A)z(HA)(2n-z) plus z H+; then D equals K times the dimer activity raised to n divided by hydrogen-ion activity raised to z.
3. For two conditions, calculate n from [ln(D1/D2) - z ln(H2/H1)] divided by ln(C1/C2), then map the near-integer n to the chemically admissible ligand counts without confusing dimer and monomer equivalents.
4. Calculate K independently from each condition as D times [H+] raised to z divided by [H2A2] raised to n, retaining guard digits and checking cross-condition consistency.
5. Evaluate reaction-coefficient sums, numerical inequalities, and reporting-precision statements separately; assign significant figures from the stated input precision, not from the scatter between K estimates.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/dimeric_acidic_extractant_stoichiometry.md

## Guards

- A radioactivity-count ratio represents the distribution ratio only when aliquot volumes and counting response are comparable.
- Use equilibrium free-extractant concentration when extraction materially depletes the extractant; tracer-metal conditions often justify the initial concentration approximation.
- Do not interpret the dimer concentration exponent as the number of monomeric HA ligands.
- Do not round the slope before applying charge balance and aggregation-state constraints, and do not use replicate disagreement alone to reduce the significant figures supplied by the measurements.
