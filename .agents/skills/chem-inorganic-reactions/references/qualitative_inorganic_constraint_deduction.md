# Qualitative inorganic reaction-network deduction

## Applicability

Unlabeled aqueous samples, including prepared mixtures, must be identified from linked precipitate, gas, redox, and directed excess-reagent observations.

## Procedure

1. Define sample domains, stock-use, concentration, internal-stability constraints, and latent product and gas variables.
2. For each observation, build the complete relation over sample compositions, product identity, gas identity, and directed excess behavior; include all compatible composite-mixture candidates.
3. Join relations that share samples or claim the same product, then enforce global stock-use and stability constraints until arc consistency reaches a fixed point.
4. Backtrack only if domains remain non-singleton; record the surviving global-assignment count and exact elimination reason after every join.
5. Return all solutions, the forced-component intersection, possible-component union, explicit alternatives, and a minimum contradictory subset when no solution exists.

## Boundaries

- Do not assign an identity before its complete local candidate relation is represented.
- Treat same-precipitate claims as equality of product identity, not merely equality of color.
- Preserve the stated direction of excess-reagent and sequential-addition tests.
- Do not force an exact assignment when the joined system has zero or multiple solutions.
- Use only available documented support; otherwise apply the explicit derivation or label missing empirical evidence unresolved. A library filename is not an executable tool.

Only calculators listed in this package's calculator reference are callable here.
Other filenames in a procedure are historical pointers, not installed dependencies.
For missing empirical support, obtain an authoritative source or state the uncertainty.
