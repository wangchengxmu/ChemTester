# Qualitative Inorganic Constraint Deduction

Use this procedure for unlabeled aqueous samples identified from several
precipitation, color, gas-evolution, redox, and excess-reagent observations.
The objective is a single globally compatible reaction network, not a series of
independent color matches.

## 1. Normalize the Sample Domains

For every stock solution, record:

- original reagent and concentration;
- ions or molecular species initially supplied;
- permitted sample composition: singleton, mixture, or both;
- whether a stock may be reused;
- whether a prepared mixture can react before later tests.

Keep original-reagent provenance separate from species present after mixing.
An equilibrium complex or precipitate is not an additional stock reagent.

Define one variable `X_i` per unknown sample. Its domain is the complete set of
allowed singleton and mixture compositions. Add global constraints for stock
non-reuse, mixture size, concentration, and internal sample stability.

Introduce latent variables for observed products and gases. For example,
`P_23` is the precipitate identity in the `2+3` test. If another observation
states that it produces the same solid, encode `P_23 = P_24`; do not compare
the two color words independently.

## 2. Exhaust Candidates Per Observation

Create one ledger row for every observation. Before assigning sample labels,
list all chemically plausible mechanisms from the candidate stocks. A row is
not complete when it contains only examples or the mechanism eventually
selected.

| Field | Record |
|---|---|
| samples and addition order | `i + j`, `excess i`, or sequential `i + j + k` |
| initial species | ions, acids, bases, ligands, oxidants, reductants |
| candidate transformation | precipitation, acid-base, complexation, redox, hydrolysis |
| visible products | solid identity/color, gas, solution color |
| final state | persistent solid, dissolved complex, or clear solution |
| required stock pair(s) | every pair or mixture able to produce the event |
| exclusions | pairs contradicted by solubility, color, pH, or mass balance |

Represent the completed row as a candidate relation:

`C_ij = {(composition_i, composition_j, mechanism, products, final_state)}`.

When a sample may contain two stocks, include composite explanations in which
one component pair creates the solid and another component pair creates the
gas or color. Record the primitive reaction motifs once, then represent their
mixture explanations as a Cartesian product rather than silently dropping
them or printing thousands of repeated tuples.

For each row, report:

- the complete primitive mechanism list;
- the number of expanded sample-composition candidates;
- concentration or equilibrium exclusions;
- candidates retained after addition-order and internal-stability checks.

Use compound identity before color. Typical high-information signatures include:

- acid plus carbonate: `CO2` evolution;
- metal ion plus carbonate: carbonate or hydroxide precipitation, sometimes
  with `CO2` from hydrolysis;
- silver halide precipitation and ligand-dependent dissolution;
- metal hydroxide precipitation and acid, ligand, or amphoteric dissolution;
- oxidant-reductant pairs that create iodine, changed oxidation states, or gas.

## 3. Rank Evidence Without Discarding Alternatives

Treat evidence in this order:

1. directed excess-reagent or sequential-addition behavior;
2. gas identity and stoichiometric source;
3. compound-specific solubility or complexation;
4. redox feasibility under the stated pH and concentrations;
5. precipitate color;
6. absence of a visible change.

Color is rarely unique. Preserve every candidate that remains feasible, and
note when a verbal color could describe a transient species or mixed solid.

## 4. Solve the Global Constraint System

Treat every completed observation row as a relation over sample compositions,
product identities, gas identities, and addition direction. Consolidate by
relational joins:

1. join observations that explicitly share the same product or intermediate;
2. join the resulting relation with observations sharing the most constrained
   sample;
3. apply global stock-use and internal-stability constraints;
4. repeat until generalized arc consistency reaches a fixed point;
5. if domains are still non-singleton, branch on the smallest remaining domain
   and backtrack.

For a network containing pair and sequential tests, the operation has the
form:

`Solutions = C_12 JOIN C_13 JOIN ... JOIN C_456 JOIN GlobalConstraints`.

The join must match sample compositions and latent product identities, not
merely intersect reagent-name lists.

For each tentative assignment:

1. expand all components in both samples;
2. predict the initial event;
3. apply the named excess or later addition in the stated direction;
4. verify gas, solid identity, color, and final clarity;
5. enforce stock-use and mixture-preparation constraints;
6. reject the assignment immediately when any hard observation fails.

After all rows are evaluated, retain every tied global solution:

- forced components are the intersection across all solutions;
- possible components are the union across all solutions;
- mutually exclusive alternatives remain as explicit branches.

Show an elimination trace. After each newly applied observation, record the
remaining global-assignment count and the exact constraint that removed each
branch. Do not announce a sample identity before every alternative in its
candidate relation has either survived or received an explicit rejection.

If the solution count becomes zero, compute a minimum contradictory subset by
removing one observation at a time and re-solving. This identifies the smallest
set of statements that cannot be true together.

## 5. Distinguish Exact, Ambiguous, and Inconsistent Cases

- **Exact:** one assignment satisfies every hard observation.
- **Ambiguous:** several assignments satisfy every hard observation.
- **Inconsistent:** no assignment satisfies every hard observation.

For an inconsistent case, report the minimum contradictory subset and the
specific reaction that fails. Do not invent an unsupported reaction, reverse
an excess-reagent direction, or select an option merely because it appears in
several local explanations. If a problem was transformed from an experiment,
compare it with the original protocol during later provenance adjudication,
not while constructing the initial reaction network.

## Output Contract

Return:

1. the complete primitive candidate set for every observation;
2. each observation relation, including latent products and addition direction;
3. expanded-candidate counts after every relational join;
4. the sample assignment or every tied assignment;
5. forced components, possible components, and mutually exclusive alternatives;
6. every assumption needed for the result;
7. the final global-solution count and exact, ambiguous, or inconsistent status;
8. the minimum contradictory observation subset when the count is zero.

Map the reagent union to option letters only after the chemistry is complete.
