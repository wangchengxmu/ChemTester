# L2 Topic: Retrosynthetic Analysis

**Source**: LibreTexts Organic Chemistry; Logic of Organic Synthesis (Rao)
**Created**: 2026-03-18
**Status**: Scaffold (Pass-1)

---

## Concept Overview

Retrosynthetic analysis is a problem-solving technique for planning organic syntheses. It works backward from a target molecule (TM) through strategic bond disconnections to identify simple, available starting materials. This logical approach was developed by E.J. Corey and is fundamental to modern synthetic planning.

### Key Features
1. **Disconnection**: Breaking bonds retrosynthetically to generate simpler precursors
2. **Synthons**: Idealized fragments representing reactive intermediates
3. **Synthetic tree**: All possible routes from TM to starting materials
4. **Convergent vs linear**: Strategic approaches affecting overall yield

---

## Core Principles

### The Retrosynthetic Approach

**Forward Synthesis:**
```
Starting Materials â?Intermediates â?Target Molecule
```

**Retrosynthetic Analysis:**
```
Target Molecule â?Disconnection â?Simpler Precursors â?Starting Materials
```

**Key Notation:**
- `â` indicates retrosynthetic step (reverse of synthesis)
- `â` indicates synthetic step (forward reaction)

### Types of Disconnections

| Disconnection Type | Bond Broken | Forward Reaction |
|-------------------|-------------|------------------|
| C-C bond | Carbon-carbon | Coupling, addition |
| C-X bond | Carbon-heteroatom | Substitution, addition |
| C=C bond | Alkene | Addition, elimination (reverse) |
| C=O bond | Carbonyl | Addition, condensation |

### Synthons and Synthetic Equivalents

**Synthon**: Idealized fragment with implied reactivity (may not exist as stable species)

**Synthetic Equivalent**: Real compound that provides the synthon

| Synthon | Synthetic Equivalent | Reactivity |
|---------|---------------------|------------|
| Râ?(electrophile) | R-X, R-OTf | Alkyl halides, tosylates |
| Râ?(nucleophile) | R-MgX, R-Li | Grignard, organolithium |
| RCHO (acyl cation) | RCOCl, RCOOR' | Acyl halides, esters |
| RCOâ?(acyl anion) | R-Câ¡N, R-MgCOR | Cyanohydrin equivalents |
| â»CHâ?COR | CHâCOR + base | Enolate formation |

### Strategic Bond Selection

**Criteria for Choosing Disconnection Sites:**

1. **Functional groups**: Disconnect adjacent to reactive sites
2. **Ring systems**: Open rings at strategic positions
3. **Symmetry**: Exploit molecular symmetry
4. **Stability**: Generate stable intermediates
5. **Availability**: Lead to commercially available starting materials

### One-Group and Two-Group Disconnections

**One-Group Disconnections:**
- Single functional group transformation
- Example: Alcohol â?Carbonyl (reduction)

**Two-Group Disconnections:**
- Disconnection involving two functional groups
- Example: Î²-hydroxy carbonyl â?Aldehyde + enolate (aldol)

---

## Synthetic Strategies

### Linear Synthesis

```
A â?B â?C â?D â?Target
```
- Sequential steps (consequential)
- Overall yield = (yield per step)^n
- For 5 steps at 90% each: 0.9â?= 59% overall

### Convergent Synthesis

```
A â?B â?C â?           ââ Target
D â?E â?F â?```
- Parallel branches converge
- Higher overall yield for same number of steps
- For 5 steps (3+2) at 90% each: 0.9Â³ Ã 0.9Â² = 73% overall

### Yield Comparison

| Strategy | Steps | Yield/Step | Overall Yield |
|----------|-------|------------|---------------|
| Linear | 5 | 90% | 59% |
| Convergent | 5 (3+2) | 90% | 73% |
| Linear | 10 | 90% | 35% |
| Convergent | 10 (5+5) | 90% | 59% |

### Common Disconnection Patterns

**1. Alcohol Disconnections:**
```
R-CHâOH â?R-CHO (aldehyde reduction)
RâCHOH â?R-CO-R (ketone reduction)
RâCOH â?R-CO-R + R-MgX (Grignard addition)
```

**2. Alkene Disconnections:**
```
R-CH=CH-R â?R-CHO + R-CHâ?PPhâ?(Wittig)
R-CH=CHâ?â?R-Câ¡CH (partial reduction)
```

**3. Carbonyl Disconnections:**
```
R-CO-CHâ?R â?R-CO-X + R-MgX (Grignard)
R-CO-CHâ?CHâ?R â?R-CO-CHâ?+ R-CHO (aldol)
Î²-hydroxy carbonyl â?Aldehyde + ketone enolate
```

**4. Aromatic Disconnections:**
```
Ar-R â?Ar-H + Râ?source (Friedel-Crafts)
Ar-OH â?Ar-H (via diazonium)
Ar-NHâ?â?Ar-H (via nitration, reduction)
```

---

## Synthetic Tree Construction

### Process

1. **Identify target molecule** (TM)
2. **List all possible disconnections**
3. **For each disconnection, draw precursors**
4. **Repeat for each precursor** until reaching simple starting materials
5. **Evaluate each route** for feasibility and yield

### Evaluation Criteria

| Criterion | Question |
|-----------|----------|
| Feasibility | Is the forward reaction known? |
| Selectivity | Will the reaction be selective? |
| Yield | What is the expected yield? |
| Availability | Are starting materials available? |
| Safety | Are any reagents hazardous? |
| Cost | Is the route economical? |

---

## Decision Trees

### Choosing Disconnection Site
```
Is there a functional group? â?Disconnect adjacent to it
Is there a ring? â?Consider ring-opening retro-Diels-Alder
Is there symmetry? â?Disconnect at symmetric bond
Is there a C-C bond Î² to carbonyl? â?Aldol disconnection
Is there an alcohol? â?Consider carbonyl reduction
```

### Selecting Synthon Type
```
Need nucleophile (Râ?? â?Use Grignard, organolithium, enolate
Need electrophile (Râ?? â?Use alkyl halide, tosylate
Need acyl electrophile? â?Use acyl chloride, ester
Need acyl nucleophile? â?Use cyanohydrin, dithiane
```

### Linear vs Convergent Strategy
```
Target has two similar halves? â?Convergent
Long linear chain? â?Consider convergent at midpoint
Complex functionality? â?Break into functional modules
>6 linear steps? â?Definitely use convergent
```

---

## Key Tables

### Common Synthon-Synthetic Equivalent Pairs

| Synthon | Charge Type | Synthetic Equivalent | Typical Reaction |
|---------|-------------|---------------------|------------------|
| Râ?| Electrophile | R-X, R-OTs | SN1, SN2 |
| Râ?| Nucleophile | R-MgX, R-Li | Nucleophilic addition |
| RCOâ?| Electrophile | RCOCl, (RCO)âO | Acylation |
| RCOâ?| Nucleophile | R-Câ¡N, dithiane | Nucleophilic acyl addition |
| â»CHâCOR | Nucleophile | Enolate | Aldol, alkylation |
| âºCHâCOR | Electrophile | Î±-halo carbonyl | Alkylation (reverse) |

### Protecting Group Considerations in Retrosynthesis

| Situation | Protecting Group Strategy |
|-----------|--------------------------|
| Multiple reactive sites | Consider orthogonal protection |
| Need later transformation | Use selectively removable group |
| Acidic workup planned | Use base-stable protection |
| Basic conditions planned | Use acid-stable protection |

---

## Cross-Links

- **protecting_groups.md**: Protecting group selection
- **organic_reaction_mechanisms.md**: Forward reaction mechanisms
- **alkene_chemistry.md**: Alkene formation and reactions
- **carbonyl_chemistry.md**: Carbonyl disconnections
- **alkyl_halide_reactions.md**: C-X bond formation

---

## References

1. LibreTexts Organic Chemistry: Retrosynthetic Analysis
2. Rao, R.B. Logic of Organic Synthesis
3. Corey, E.J. & Cheng, X. (1989). The Logic of Chemical Synthesis
4. Warren, S. (1982). Organic Synthesis: The Disconnection Approach


## Implementations

- Implementation: `../L3_functions/retrosynthesis_tools.py`

## L3 Tool Call Directives

**Source:** `retrosynthesis_tools.py`

Linear and convergent synthesis yield calculations, synthon matching, and coupling method lookup.

### Available functions:
- `linear_yield(yields)` → float — Overall yield = Π(step yields)
- `convergent_yield(branch_yields, final_yield=0.9)` → float — Convergent synthesis overall yield
- `compare_strategies(n_steps, step_yield, n_branches)` → Dict — Linear vs convergent comparison
- `synthon_matcher(synthon_type)` → Dict — Find synthetic equivalents for a synthon (e.g. 'R+')
- `find_coupling_method(substrate1, substrate2)` → List[Dict] — Coupling reactions for substrate types

### Common errors:
- ❌ Assuming convergent is always better — only when branches reduce sequential steps
- ❌ Not accounting for coupling step yield in convergent synthesis


## L3 Tools
- - `../L3_functions/retrosynthesis_tools.py` — plan_retrosynthesis(), identify_disconnection_targets()
- - `../L3_functions/reaction_sequence_tracker.py` — track_sequence(), predict_product()
- - `../L3_functions/rdkit_structure_tools.py` — parse_molecule(), analyze_functional_groups()
