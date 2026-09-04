---
id: chem.reaction_mechanisms
layer: 2
title: Reaction Mechanisms and Rate-Determining Steps
source: Ch12.06-12.07
dependencies: [rate_laws]
stability: high
confidence: high
---

## Concept

Reaction mechanisms describe the sequence of elementary steps by which reactants become products. The slowest step (rate-determining step) controls the overall rate.

## Core Concepts

### Elementary Steps
Single molecular events with rate laws derived from molecularity.

| Molecularity | Example | Rate Law |
|--------------|---------|----------|
| Unimolecular | A ¡ú products | rate = k[A] |
| Bimolecular | A + B ¡ú products | rate = k[A][B] |
| Termolecular | A + B + C ¡ú products | rate = k[A][B][C] |

### Rate-Determining Step (RDS)
- Slowest step in mechanism
- Determines overall rate law
- Analogy: bottleneck in production line

## Decision Tree

```
Analyzing reaction mechanism?
©À©¤ Elementary step rate law?
©¦   ©¸©¤ Write directly from stoichiometry
©À©¤ Overall rate law?
©¦   ©¸©¤ Based on RDS (slowest step)
©À©¤ Is mechanism valid?
©¦   ©À©¤ Sum of steps = overall equation
©¦   ©¸©¤ Rate law matches experiment
©¸©¤ Catalyst present?
    ©¸©¤ Alternative pathway with lower Ea
```

## Key Constraints
- Elementary step rate law ¡Ù overall reaction rate law
- Intermediates should not appear in overall rate law
- Overall rate law must match experimental observations
- Catalyst lowers Ea, provides alternative pathway

## Catalysis

| Type | Definition | Example |
|------|------------|---------|
| Homogeneous | Same phase as reactants | H?(aq) catalyzing ester hydrolysis |
| Heterogeneous | Different phase | Pt(s) catalyzing hydrogenation |

```
Catalyst effects:
- Lowers activation energy
- Provides alternative mechanism
- Does NOT change equilibrium position
- Regenerated in reaction
```

## Problem Archetypes
1. Write rate law for elementary step
2. Derive overall rate law from mechanism
3. Identify rate-determining step
4. Propose mechanism consistent with rate law
5. Compare catalyzed vs uncatalyzed mechanisms

## L3 Tools
- `elementary_rate_law(step)` ¡ú rate law
- `overall_rate_law(mechanism)` ¡ú rate law
- `identify_rds(mechanism, experimental_rate_law)` ¡ú step
- `catalyzed_rate(k_uncat, Ea_cat, Ea_uncat, T)` ¡ú k_cat

## L4 Reference

## L5 Examples
See `../L5_examples/kinetics_examples.md for worked examples.

## Implementations

- Implementation: `../L3_functions/mechanism_tools.py`

## L3 Tool Call Directives

**Source:** `transition_state_tools.py`

⚠️ Stub file — no public functions implemented yet.

### Available functions:
- *(none — file is empty)*
