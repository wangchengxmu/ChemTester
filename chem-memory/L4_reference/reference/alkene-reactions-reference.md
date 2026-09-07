# Alkene Reactions Reference
[Source: Organic Chemistry OpenStax, Ch07-08]

## Heat of Hydrogenation Data

| Alkene | ΔH°hydrogenation (kJ/mol) | Stability Rank |
|--------|---------------------------|----------------|
| Ethene | -137 | 6 (least stable) |
| Propene | -125 | 5 |
| But-1-ene | -127 | 5 |
| cis-But-2-ene | -119 | 4 |
| trans-But-2-ene | -115 | 3 |
| 2-Methylpropene | -119 | 2 |
| 2-Methylbut-2-ene | -113 | 1 |
| 2,3-Dimethylbut-2-ene | -111 | 1 (most stable) |

## Alkene Stability Order

| Type | Relative Stability | Reason |
|------|-------------------|--------|
| Tetrasubstituted | Most stable | Maximum hyperconjugation |
| Trisubstituted | High | Good hyperconjugation |
| trans-Disubstituted | Moderate | Less steric strain |
| cis-Disubstituted | Moderate | Some steric strain |
| Monosubstituted | Less stable | Limited hyperconjugation |
| Unsubstituted | Least stable | No hyperconjugation |

## Electrophilic Addition Reactions Summary

| Reaction | Reagent(s) | Product | Regioselectivity | Stereochemistry |
|----------|------------|---------|------------------|-----------------|
| Hydrohalogenation | HX | Alkyl halide | Markovnikov | Via carbocation |
| Halogenation | X₂ | Vicinal dihalide | - | Anti addition |
| Halohydrin | X₂, H₂O | Halohydrin | OH to more sub. C | Anti addition |
| Hydration (acid) | H₂O, H⁺ | Alcohol | Markovnikov | Via carbocation |
| Oxymercuration | Hg(OAc)₂, H₂O, NaBH₄ | Alcohol | Markovnikov | No rearrangement |
| Hydroboration | BH₃, H₂O₂, OH⁻ | Alcohol | Anti-Markovnikov | Syn addition |
| Hydrogenation | H₂, Pd/Pt/Ni | Alkane | - | Syn addition |
| Epoxidation | RCO₃H | Epoxide | - | Syn addition |
| Dihydroxylation (syn) | OsO₄ or cold KMnO₄ | 1,2-diol | - | Syn addition |
| Ozonolysis | O₃, (CH₃)₂S | Carbonyls | - | Cleavage |

## Markovnikov vs Anti-Markovnikov

### Markovnikov Rule
- H adds to carbon with MORE H atoms
- More substituted carbocation intermediate
- Favored by: HX addition, acid-catalyzed hydration

### Anti-Markovnikov
- H adds to carbon with FEWER H atoms
- No carbocation intermediate
- Favored by: Hydroboration-oxidation

| Alkene | Markovnikov Product | Anti-Markovnikov Product |
|--------|---------------------|-------------------------|
| Propene + HBr | 2-Bromopropane | 1-Bromopropane |
| Propene + H₂O/H⁺ | Propan-2-ol | Propan-1-ol |
| 1-Butene + HBr | 2-Bromobutane | 1-Bromobutane |

## Syn vs Anti Addition

| Reaction | Type | Mechanism |
|----------|------|-----------|
| Hydrogenation | Syn | H adds from same side of catalyst |
| Halogenation | Anti | Halonium ion intermediate |
| Halohydrin | Anti | Halonium ion intermediate |
| Hydroboration | Syn | Concerted addition |
| Epoxidation | Syn | Concerted addition |
| OsO₄ dihydroxylation | Syn | Cyclic osmate intermediate |

## E/Z Configuration

### Cahn-Ingold-Prelog Rules for E/Z
1. Assign priorities to groups on each C of C=C
2. Higher atomic number = higher priority
3. If first atoms same, look outward
4. Multiple bonds count as multiple single bonds

### Assignment
| Priority Arrangement | Configuration |
|---------------------|---------------|
| High priorities on same side | Z (zusammen) |
| High priorities on opposite sides | E (entgegen) |

## Carbocation Rearrangements

### Types
| Type | Process | Example |
|------|---------|---------|
| Hydride shift | H⁻ migrates | 2° → 3° carbocation |
| Alkyl shift | R⁻ migrates | 1° → 2° or 3° |

### Driving Force
- Always toward more stable carbocation
- 3° > 2° > 1° > methyl

## Elimination Reactions

### E1 vs E2
| Feature | E1 | E2 |
|---------|-----|-----|
| Steps | Two | One |
| Intermediate | Carbocation | None |
| Rate law | k[RX] | k[RX][Base] |
| Base | Weak OK | Strong required |
| Stereochemistry | No preference | Anti-periplanar |
| Rearrangement | Possible | No |

### Zaitsev vs Hofmann
| Rule | Product | Condition |
|------|---------|-----------|
| Zaitsev | More substituted alkene | Small base, standard conditions |
| Hofmann | Less substituted alkene | Bulky base (t-BuOK) |

## Degree of Unsaturation (DoU)

### Formula
```
DoU = (2C + 2 + N - H - X) / 2

C = carbons, H = hydrogens, N = nitrogens, X = halogens
```

### Interpretation
| DoU | Possibilities |
|-----|---------------|
| 0 | Saturated (alkane) |
| 1 | One double bond OR one ring |
| 2 | Two double bonds, one triple, two rings, etc. |
| 3 | Three double bonds, one triple + one ring, etc. |

### Examples
| Formula | DoU | Possible Structures |
|---------|-----|---------------------|
| C₅H₁₂ | 0 | Alkane (pentane isomers) |
| C₅H₁₀ | 1 | Alkene OR cycloalkane |
| C₆H₆ | 4 | Benzene |
| C₄H₆ | 2 | Diene, alkyne, or cycloalkene |

## Reaction Decision Flowchart

```
Alkene + Reagent
    │
    ├─ H₂ + metal → Alkane (syn)
    │
    ├─ HX → Alkyl halide (Markovnikov)
    │
    ├─ X₂ → Vicinal dihalide (anti)
    │
    ├─ X₂ + H₂O → Halohydrin (anti, OH to more sub. C)
    │
    ├─ H₂O + H⁺ → Alcohol (Markovnikov, rearrangement possible)
    │
    ├─ Hg(OAc)₂, H₂O → Alcohol (Markovnikov, no rearrangement)
    │
    ├─ BH₃, H₂O₂ → Alcohol (Anti-Markovnikov, syn)
    │
    ├─ RCO₃H → Epoxide (syn)
    │
    └─ O₃ → Carbonyl compounds (cleavage)
```
