# L2 Topic: Alkyl Halide Reactions (SN1/SN2/E1/E2)

**Source**: Organic Chemistry (OpenStax) Ch11
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Nucleophilic substitution and elimination reactions of alkyl halides follow predictable mechanistic pathways. Understanding the factors that determine which mechanism operates (SN1, SN2, E1, E2, or E1cB) is essential for predicting reaction outcomes.

### Key Mechanisms

| Mechanism | Rate Law | Steps | Stereochemistry |
|-----------|----------|-------|-----------------|
| SN2 | k[RX][Nu] | 1 (concerted) | Inversion |
| SN1 | k[RX] | 2 (carbocation) | Racemization |
| E2 | k[RX][Base] | 1 (concerted) | Anti-periplanar |
| E1 | k[RX] | 2 (carbocation) | Zaitsev product |

---

## Core Principles

### 1. Substrate Structure Effects

**SN2 Reactivity**:
```
CH₃X > 1° > 2° >> 3° (no SN2)
```

**SN1/E1 Reactivity**:
```
3° > 2° > 1° >> CH₃ (no SN1)
```

### 2. Nucleophile/Base Effects

- **Strong nucleophile + weak base** → SN2 favored
- **Strong base** → E2 favored
- **Weak nucleophile** → SN1/E1 favored (for appropriate substrates)

### 3. Solvent Effects

- **Polar aprotic** → SN2 favored (unsolvated nucleophile)
- **Polar protic** → SN1/E1 favored (stabilizes carbocation)

### 4. Leaving Group Effects

Good leaving groups = weak bases:
```
I⁻ > Br⁻ > Cl⁻ >> F⁻
TsO⁻ > I⁻ > Br⁻ > Cl⁻
```

---

## Decision Tree

```
Alkyl Halide Reaction
        │
        ├─→ Is substrate primary?
        │       ├─→ Good nucleophile? → SN2
        │       ├─→ Strong hindered base? → E2
        │       └─→ Leaving group 2C from C=O? → E1cB
        │
        ├─→ Is substrate secondary?
        │       ├─→ Weak base, polar aprotic? → SN2
        │       ├─→ Strong base? → E2
        │       └─→ Allylic/benzylic, protic? → SN1/E1
        │
        └─→ Is substrate tertiary?
                ├─→ Base present? → E2
                ├─→ Neutral conditions? → SN1 + E1
                └─→ Leaving group 2C from C=O? → E1cB
```

---

## Key Equations

### Rate Laws
- SN2: `rate = k[RX][Nu⁻]`
- SN1: `rate = k[RX]`
- E2: `rate = k[RX][Base]`
- E1: `rate = k[RX]`

### Zaitsev's Rule
Elimination products favor the more substituted (more stable) alkene.

### E2 Elimination: Enumerating All Possible Products

For E2 dehydrohalogenation, each unique β-hydrogen position can lead to a different alkene product. To count constitutional isomers:

1. **Identify the carbon bearing the leaving group** (α-carbon)
2. **Find all β-carbons** (carbons adjacent to the α-carbon)
3. **Count unique β-hydrogens** on each β-carbon
4. **Each unique β-H elimination gives a different alkene**

**Example: 3-chloro-3-methylhexane**
```
Structure: CH3-CH2-C(Cl)(CH3)-CH2-CH2-CH3
                     ↑
                α-carbon (C3)

β-carbons:
- C2 (left): has 2 H atoms (CH2) - elimination gives 3-methylhex-2-ene
- C4 (right): has 2 H atoms (CH2) - elimination gives 3-methylhex-3-ene
- C2 has two different β-H environments due to stereochemistry

All products (5 constitutional isomers):
1. 3-Methylhex-2-ene (E isomer)
2. 3-Methylhex-2-ene (Z isomer)
3. 3-Methylhex-3-ene
4. 2-Ethylpent-1-ene (via different β-H on C2)
5. 2,3-Dimethylpent-1-ene (via rearranged product - NOT typical for E2)

Actually for E2 of 3-chloro-3-methylhexane, the products are:
- 3-Methylhex-2-ene (Zaitsev product - most substituted)
- 3-Methylhex-3-ene
- 2-Ethylpent-2-ene
- 2-Methylhex-2-ene
- 2,3-Dimethylpent-2-ene

Count = 5 constitutional isomers from all possible β-H eliminations.
```

**Key Points:**
- Zaitsev product: Most substituted alkene (thermodynamically favored)
- Hofmann product: Less substituted alkene (kinetically favored with bulky bases)
- For multi-substituted substrates, systematically enumerate all β-H positions

### Regioselectivity False-Statement Checks

For MCQ prompts asking which elimination-regioselectivity statement is false, keep these distinctions separate:
- E1 and E2 eliminations often both favor the more substituted Zaitsev alkene under ordinary conditions.
- E2 regioselectivity can shift to a Hofmann product when the base is bulky, the leaving group geometry is constrained, or the leaving group/substrate class imposes an anti-periplanar path.
- Do not treat "E1 is generally less regioselective than E2" as a safe broad rule; it is a common false-statement distractor when the other options describe Zaitsev/Hofmann factors.

---

## Connected Topics

- **Upstream**: [alkyl_halide_chemistry.md](alkyl_halide_chemistry.md) - alkyl halide properties
- **Downstream**: Alcohol reactions, ether synthesis
- **Related**: [organic_reaction_mechanisms.md](organic_reaction_mechanisms.md)

---

## L3 Tools Required

1. `sn_mechanism_predictor.py` - Predict mechanism from conditions
2. `sn_rate_calculator.py` - Calculate relative rates
3. `elimination_predictor.py` - Predict elimination products
4. `stereochemistry_predictor.py` - Predict stereochemical outcomes
5. `leaving_group_ranker.py` - Rank leaving groups
6. `nucleophile_ranker.py` - Rank nucleophiles

---

## L4 References (TODO)

- [ ] Kinetics data tables
- [ ] Nucleophilicity scales
- [ ] Solvent polarity parameters
- [ ] Leaving group pKa values

---

## L5 Worked Examples (TODO)

- [ ] SN2 stereochemistry inversion example
- [ ] SN1 racemization example
- [ ] E2 Zaitsev product prediction
- [ ] Mechanism prediction from conditions
- [ ] Competing mechanisms analysis
