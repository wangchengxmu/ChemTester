---
id: benchmark.redox_solubility_equilibrium_disambiguation
layer: 2
title: Benchmark Redox, Solubility, and Equilibrium Constant Disambiguation
up_links:
  - ../L1_ontology/chemistry-core-map.md
  - ./nernst_equation.md
  - ./benchmark_analytical_assay_disambiguation.md
---

# Benchmark Redox, Solubility, and Equilibrium Constant Disambiguation

Use this note for benchmark rows that ask for a standard equilibrium constant
assembled from solubility products and electrochemical potentials. These rows
often need a log-space Hess-law calculation rather than broad option intuition.

## Combining Ksp and Redox Terms

For a solid sulfide dissolution coupled to oxidation by nitrate:

1. Write the net ionic reaction before selecting an option.
2. Convert each precipitation/dissolution step directly into a log K term.
3. Convert each redox step with `log10 K = n Ecell / 0.05916` at 298 K.
4. Add log K terms only after the half-reactions are scaled to the net equation.

For copper sulfide rows that provide `E(Cu2+/Cu)` and `E(Cu+/Cu)`, first derive:

```text
E(Cu2+/Cu+) = 2 E(Cu2+/Cu) - E(Cu+/Cu)
```

For the reaction:

```text
3 Cu2S(s) + 4 NO3- + 16 H+ -> 6 Cu2+ + 3 S(s) + 4 NO + 8 H2O
```

the log expression is:

```text
log K = 3 log Ksp(Cu2S)
      + 6 [E(NO3-/NO) - E(S/S2-)] / 0.05916
      + 6 [E(NO3-/NO) - E(Cu2+/Cu+)] / 0.05916
```

This calculation should be compared to the logarithms of the visible options.
Do not choose an "all other options" distractor until numeric options have been
parsed and compared in log space.

## Coupled Lead Chromate and Hydroxide Equilibria

For benchmark rows that dissolve excess `PbCrO4(s)` in pure water while
`Pb(OH)2(s)` can precipitate, do not treat the chromate solubility as a single
`sqrt(Ksp)` calculation. Express all chromium species from `K1`, `K2`, `K3`,
`K5`, `Kw`, and `[H+]`, express dissolved lead from `K4 / [OH-]^2`, then solve
the charge balance:

```text
[H+] + 2[Pb2+] = [OH-] + [HCrO4-] + 2[CrO4^2-] + 2[Cr2O7^2-]
```

The requested chromium solubility is the total elemental chromium:

```text
[H2CrO4] + [HCrO4-] + [CrO4^2-] + 2[Cr2O7^2-]
```

If the prompt asks for `n = aV` for precipitated `Pb(OH)2(s)`, compute
`a = total chromium - dissolved [Pb2+]` after the charge-balance solution.
This distinguishes the precipitation coefficient from total solubility or
from the hydroxide Ksp alone.

## Source Basis

- Chemistry memory electrochemistry examples: Nernst equation and standard
  cell-potential relationship to equilibrium constants.
- Chemistry memory precipitation/dissolution note: Ksp expressions for ionic
  solids.
- SUPERChem text-only benchmark rows can combine these two surfaces with
  evaluator-only answers; keep source explanations out of the performer path.
