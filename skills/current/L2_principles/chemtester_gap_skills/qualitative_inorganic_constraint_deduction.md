# Qualitative inorganic reaction-network deduction

**Retrieve with:** qualitative inorganic reaction constraints, unknown solution pairwise deduction, precipitate gas excess reagent, mixed reagent sample identification

**Use when:** Unlabeled aqueous samples, including prepared mixtures, must be identified from linked precipitate, gas, redox, and directed excess-reagent observations.

## Procedure

1. Define sample domains, stock-use, concentration, internal-stability constraints, and latent product and gas variables.
2. For each observation, build the complete relation over sample compositions, product identity, gas identity, and directed excess behavior; include all compatible composite-mixture candidates.
3. Join relations that share samples or claim the same product, then enforce global stock-use and stability constraints until arc consistency reaches a fixed point.
4. Backtrack only if domains remain non-singleton; record the surviving global-assignment count and exact elimination reason after every join.
5. Return all solutions, the forced-component intersection, possible-component union, explicit alternatives, and a minimum contradictory subset when no solution exists.

## Preferred Support

- L2_principles/qualitative_inorganic_constraint_deduction.md
- L2_principles/reaction_classification_and_patterns.md
- L2_principles/solubility_equilibria.md
- L2_principles/coordination_chemistry.md
- L4_reference/solubility_products.csv
- L4_reference/electrode_potentials.csv

## Guards

- Do not assign an identity before its complete local candidate relation is represented.
- Treat same-precipitate claims as equality of product identity, not merely equality of color.
- Preserve the stated direction of excess-reagent and sequential-addition tests.
- Do not force an exact assignment when the joined system has zero or multiple solutions.
