---
id: aromatic.chemistry
layer: 2
title: Aromatic Chemistry - Benzene and Aromatic Compounds
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - - `../L3_functions/rdkit_structure_tools.py` — aromatic_substitution_planner()
  - - `../L3_functions/pericyclic_tools.py` — cycloaddition analysis
  - ../L3_functions/pericyclic_tools.py
  - ../L4_reference/reference/alkene-reactions-reference.md
cross_links:
  - ./organic_reaction_mechanisms.md
  - ./conformational_analysis.md
source: Organic Chemistry (OpenStax), Ch15-16
---

## Context
Aromatic compounds contain planar, cyclic, conjugated systems with (4n+2) π electrons (Hückel's rule). Benzene is the prototypical aromatic compound, exhibiting unusual stability due to resonance. Electrophilic aromatic substitution is the dominant reaction type.

## Aromaticity

### Hückel's Rule
A compound is aromatic if it:
1. Is cyclic
2. Is planar
3. Is fully conjugated (p orbital on every atom in ring)
4. Has (4n + 2) π electrons (n = 0, 1, 2, ...)

### Hückel Numbers
| n | π Electrons | Examples |
|---|-------------|----------|
| 0 | 2 | Cyclopropenyl cation |
| 1 | 6 | Benzene, pyridine, cyclopentadienyl anion |
| 2 | 10 | Naphthalene, cyclooctatetraene dianion |
| 3 | 14 | Anthracene, phenanthrene |

### Aromatic vs Anti-aromatic
- **Aromatic**: (4n+2) π electrons, stable
- **Anti-aromatic**: 4n π electrons, unstable
- **Non-aromatic**: Not fully conjugated or not planar

## Benzene Structure

### Molecular Orbital Description
- Six sp² carbons, each with p orbital
- Six π electrons fill three bonding MOs
- Delocalization energy: ~150 kJ/mol

### Resonance Structures
```
    ⎡⎤       ⎣⎦
    ⎢⎥  ↔  ⎥⎥
    ⎣⎦       ⎡⎤
```
- All C-C bonds equivalent (139 pm)
- Not alternating single/double

## Nomenclature of Aromatic Compounds

### Monosubstituted Benzenes
| Substituent | Common Name | IUPAC Name |
|-------------|-------------|------------|
| -CH₃ | Toluene | Methylbenzene |
| -OH | Phenol | Hydroxybenzene |
| -NH₂ | Aniline | Aminobenzene |
| -COOH | Benzoic acid | Benzenecarboxylic acid |

### Disubstituted Benzenes
| Position | Prefix |
|----------|--------|
| 1,2- | ortho- (o-) |
| 1,3- | meta- (m-) |
| 1,4- | para- (p-) |

## Electrophilic Aromatic Substitution (EAS)

### General Mechanism
1. **Electrophile formation**: Reagent generates E⁺
2. **Attack**: E⁺ adds to ring → arenium ion (σ complex)
3. **Deprotonation**: Base removes H⁺ → restores aromaticity

```
    E⁺        E                  E
    +   →  [  ⊕  ]  →   
              H                  H
```

### Major EAS Reactions

| Reaction | Reagent | Electrophile | Product |
|----------|---------|--------------|---------|
| Halogenation | X₂, FeX₃ | X⁺ | Aryl halide |
| Nitration | HNO₃, H₂SO₄ | NO₂⁺ | Nitrobenzene |
| Sulfonation | H₂SO₄, SO₃ | SO₃ | Benzenesulfonic acid |
| Friedel-Crafts alkylation | R-X, AlCl₃ | R⁺ | Alkylbenzene |
| Friedel-Crafts acylation | RCOCl, AlCl₃ | RCO⁺ | Alkyl aryl ketone |
| Alkylation (alkene) | Alkene, H⁺, AlCl₃ | Carbocation | Alkylbenzene |

### Directing Effects of Substituents

**Ortho/Para Directors (activating or deactivating):**
| Substituent | Effect | Reason |
|-------------|--------|--------|
| -OH, -OR | Strongly activating | Resonance donation |
| -NH₂, -NHR, -NR₂ | Strongly activating | Resonance donation |
| -R (alkyl) | Activating | Hyperconjugation |
| -Ph | Activating | Resonance |
| -X (halogens) | Weakly deactivating | Inductive withdrawal + resonance donation |

**Meta Directors (deactivating):**
| Substituent | Effect | Reason |
|-------------|--------|--------|
| -NO₂ | Strongly deactivating | Resonance + inductive withdrawal |
| -CN | Deactivating | Inductive + resonance withdrawal |
| -COOH, -COR | Deactivating | Resonance withdrawal |
| -SO₃H | Deactivating | Resonance withdrawal |
| -NR₃⁺ | Strongly deactivating | Positive charge |

### Reactivity Order

**Activating groups:**
```
-NH₂ > -OH > -OR > -R > -X
```

**Deactivating groups:**
```
-NO₂ > -CN > -COOH > -X
```

## Multiple Substitutions

### Predicting Products
1. Identify the more activating group
2. Apply directing effect
3. Consider steric effects (ortho positions can be hindered)

### Example: Toluene Nitration
- -CH₃ is ortho/para director
- Products: o-nitrotoluene (60%) + p-nitrotoluene (35%) + m-nitrotoluene (5%)

## Limitations of Friedel-Crafts Reactions

1. **Cannot use with deactivated rings** (meta directors)
2. **Cannot use with -NH₂ groups** (complex with AlCl₃)
3. **Rearrangements possible** (carbocation mechanism)
4. **Polyalkylation** (alkyl groups are activating)

### Solutions
- Use acylation instead of alkylation (no rearrangement)
- Protect amines as amides before reaction

## Other Aromatic Reactions

### Side-Chain Reactions
| Reaction | Reagent | Product |
|----------|---------|---------|
| Free radical halogenation | X₂, heat or light | Benzyl halide |
| Oxidation of alkyl side chains | KMnO₄, heat | Benzoic acid |

### Nucleophilic Aromatic Substitution
- Requires strong electron-withdrawing groups ortho/para
- Or benzyne mechanism (high temperatures)

## Polycyclic Aromatic Hydrocarbons (PAHs)

### Examples
| Compound | Structure | Aromaticity |
|----------|-----------|-------------|
| Naphthalene | Two fused rings | 10 π e⁻, aromatic |
| Anthracene | Three fused rings (linear) | 14 π e⁻, aromatic |
| Phenanthrene | Three fused rings (angular) | 14 π e⁻, aromatic |

## Reaction Summary Table

| Reaction | Conditions | Regioselectivity |
|----------|------------|------------------|
| Halogenation | X₂, FeX₃ | Based on substituent |
| Nitration | HNO₃, H₂SO₄ | Based on substituent |
| Sulfonation | H₂SO₄ or SO₃ | Based on substituent |
| FC Alkylation | R-X, AlCl₃ | o/p for activators, meta for deactivators |
| FC Acylation | RCOCl, AlCl₃ | Same as alkylation |
| Side-chain oxidation | KMnO₄, heat | Converts alkyl to COOH |

## Decision Flow
1. Check aromaticity (Hückel's rule)
2. For substitution: identify existing substituents
3. Determine directing effect (o/p vs meta)
4. Consider activating/deactivating effects
5. Predict major product(s)

## Implementations and Data
- Aromatic reaction predictor: [L3 code](../L3_functions/pericyclic_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/alkene-reactions-reference.md)
