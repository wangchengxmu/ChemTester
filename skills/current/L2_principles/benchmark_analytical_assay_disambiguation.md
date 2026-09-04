---
id: benchmark.analytical_assay_disambiguation
layer: 2
title: Benchmark Analytical Assay Disambiguation
up_links:
  - ../L1_ontology/chemistry-core-map.md
---

# Benchmark Analytical Assay Disambiguation

Use this note for benchmark multiple-choice rows that hide a pH, concentration,
or composition answer inside a wet-chemistry assay. Do not choose the closest
option from broad intuition when the prompt provides dilution, aliquot,
titration, precipitation, or oxidation data.

## Ammonium Sulfide Reagent Assays

For an ammonium sulfide reagent prepared from hydrogen sulfide and ammonia, a
distillation/collection assay can determine total ammonia and total sulfide
before the pH calculation.

If an original sample volume `V_sample` is diluted to `V_stock`, and an aliquot
`V_aliquot` of the stock is assayed, use:

```text
dilution_factor = V_stock / V_sample
```

When sulfuric acid is added to the distillation flask and the residual acid is
back-titrated with NaOH to a methyl-red endpoint:

```text
total_ammonia =
  (2 * C_H2SO4 * V_H2SO4 - C_NaOH1 * V_NaOH1)
  * dilution_factor / V_aliquot
```

When distilled sulfide is trapped as CdS, then oxidized by bromine to sulfate,
one mole of H2S produces ten acid equivalents in the receiving flask:

```text
total_sulfide =
  (C_NaOH2 * V_NaOH2 / 10)
  * dilution_factor / V_aliquot
```

Solve the charge balance using the visible equilibrium constants:

```text
[NH4+] + [H+] = [HS-] + 2[S2-] + [OH-]
Ka(NH4+) = Kw / Kb(NH3)
```

Use the total-ammonia distribution between NH4+ and NH3 and the total-sulfide
distribution among H2S, HS-, and S2-. Then choose the visible option nearest to
the computed pH.

## Source Notes

- Acid-base distribution and charge-balance method follows standard analytical
  chemistry treatment of weak-acid/weak-base mixtures.
- Cadmium sulfide precipitation followed by bromine oxidation to sulfate gives
  the assay stoichiometry used above; the calculation is parameterized by the
  visible titration volumes and concentrations.
