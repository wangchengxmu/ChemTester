---
id: benchmark.carbocation_stability_disambiguation
layer: 2
title: Benchmark Carbocation Stability Disambiguation
up_links:
  - ../L1_ontology/organic_chemistry.md
  - ./alkene_chemistry.md
---

# Benchmark Carbocation Stability Disambiguation

Use this note for benchmark rows that ask for qualitative carbocation
stability orderings among substituted methyl cations. Rank by the ability of
the directly attached substituent to donate electron density into the empty
p orbital, then by hyperconjugation or inductive effects, and penalize strong
electron-withdrawing resonance groups.

## Ordering Heuristics

- Lone-pair resonance donation from an adjacent heteroatom can dominate simple
  alkyl hyperconjugation. Alpha-hydroxy and alpha-alkoxy carbocations are
  oxocarbenium-like and are much more stable than an ethyl carbocation.
- In qualitative benchmark options that distinguish hydroxymethyl and
  alkoxymethyl cations by `+R` donation, treat the hydroxy-substituted cation
  as at least as strongly resonance-stabilized as the alkoxy-substituted
  cation unless the prompt gives solvent, protonation, or substituent constants
  that change the comparison.
- Alkyl groups stabilize carbocations by hyperconjugation and `+I`; a nearby
  halogen lowers that stabilization through `-I`, so `CH3CH2+` is more stable
  than `CH2(+)CH2Cl` when no anchimeric participation is specified.
- Carbonyl, aldehyde, and nitro groups adjacent to the cation are net
  destabilizing in simple ordering rows because their `-M` and `-I` effects
  withdraw electron density from the electron-deficient center. Nitro is
  usually the strongest destabilizer among those options.

## Applying The Rule

For simple substituted methyl-cation ranking rows, first group the candidates:

1. Adjacent lone-pair donors such as hydroxy or alkoxy substituents.
2. Alkyl-stabilized cations.
3. Alkyl cations weakened by nearby inductive electron withdrawal, such as a
   beta-halogen substituent.
4. Cations alpha to carbonyl, formyl, nitro, or similar electron-withdrawing
   groups.

Within the electron-withdrawing group, stronger `-M`/`-I` substituents make
the carbocation less stable. This is a substituent-effect rule, not a
problem-id rule. If the prompt gives explicit thermochemical data, solvent
stabilization, neighboring-group participation, or protonation state, use those
data instead of this generic ordering heuristic.
