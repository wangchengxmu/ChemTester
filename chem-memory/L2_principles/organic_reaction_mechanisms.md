---
id: organic.reaction_mechanisms
layer: 2
title: Organic Reaction Mechanisms
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/reaction_mechanism_tools.py
  - ../L4_reference/reference/reaction-mechanism-reference.md
cross_links:
  - ./organic_functional_groups.md
  - ./stereochemistry_chirality.md
---

## Context
A reaction mechanism describes in detail exactly what takes place at each stage of a chemical transformation—which bonds are broken and in what order, which bonds are formed and in what order, and what the relative rates are for each step. Understanding mechanisms enables prediction of reaction outcomes.

## Types of Organic Reactions

### Classification by Transformation
| Type | Description | General Pattern |
|------|-------------|-----------------|
| Addition | Two molecules combine | A + B → AB |
| Elimination | One molecule splits | AB → A + B |
| Substitution | One group replaces another | AB + C → AC + B |
| Rearrangement | Atoms reorganize | A → A' (isomer) |

### Classification by Mechanism
| Type | Key Feature | Example |
|------|-------------|---------|
| Polar reactions | Electron pair movement | Nucleophilic substitution |
| Radical reactions | Odd electron species | Halogenation of alkanes |
| Pericyclic reactions | Cyclic electron flow | Diels-Alder reaction |

## Curved Arrow Notation

### Arrow Meaning
- **Curved arrow**: Shows movement of electron pair
- **Arrow tail**: Source of electrons (nucleophile or lone pair)
- **Arrow head**: Destination (electrophile or forming bond)

### Common Patterns
```
Nucleophilic attack:    Nu:⁻ → C⁺ (or Cδ⁺)
Bond breaking:          A-B → A⁺ + B:⁻ (heterolytic)
                        A-B → A· + B· (homolytic)
Bond formation:         A· + B· → A-B
Lone pair donation:     :N → C⁺
```

## Polar Reactions

### Key Concepts
- **Electrophile**: Electron-deficient species (accepts electrons)
- **Nucleophile**: Electron-rich species (donates electrons)
- **Polarizability**: Ability to distribute charge unevenly

### Common Electrophiles
| Species | Type | Reactivity |
|---------|------|------------|
| H⁺ | Proton | Very reactive |
| R-X | Alkyl halide | Moderate |
| R-CHO | Aldehyde | Moderate |
| R-CO-R | Ketone | Moderate |
| R-COOH | Carboxylic acid | Lower |

### Common Nucleophiles
| Species | Type | Strength |
|---------|------|----------|
| HO⁻, RO⁻ | Anions | Strong |
| CN⁻, N₃⁻ | Anions | Strong |
| NH₃, H₂O | Neutral | Moderate |
| I⁻, Br⁻ | Halides | Good nucleophiles, weak bases |

## Radical Reactions

### Chain Reaction Mechanism
1. **Initiation**: Formation of radicals
   - Example: `Cl₂ → 2Cl·` (with light or heat)

2. **Propagation**: Chain-carrying steps
   - `Cl· + CH₄ → HCl + CH₃·`
   - `CH₃· + Cl₂ → CH₃Cl + Cl·`

3. **Termination**: Radical combination
   - `Cl· + Cl· → Cl₂`
   - `CH₃· + CH₃· → C₂H₆`
   - `Cl· + CH₃· → CH₃Cl`

### Radical Stability
- Order: 3° > 2° > 1° > methyl
- More substituted = more stable radical

## Energy Diagrams

### Key Features
```
Energy
  │
  │        TS (transition state)
  │       ╱ ╲
  │      ╱   ╲
  │  Reactants  ╲
  │              ╲ Products
  └───────────────────→ Reaction coordinate
```

### Important Quantities
| Term | Definition | Sign |
|------|------------|------|
| ΔH | Enthalpy change | - for exothermic |
| ΔG | Free energy change | - for spontaneous |
| Ea | Activation energy | Always positive |
| ΔH‡ | Enthalpy of activation | Related to Ea |

### Hammond Postulate
- Transition state resembles species closest in energy
- For exothermic: TS resembles reactants (early)
- For endothermic: TS resembles products (late)

## Reaction Intermediates

### Common Intermediates
| Intermediate | Structure | Stability Order |
|--------------|-----------|-----------------|
| Carbocation | R₃C⁺ | 3° > 2° > 1° > methyl |
| Carbanion | R₃C:⁻ | methyl > 1° > 2° > 3° |
| Radical | R₃C· | 3° > 2° > 1° > methyl |
| Carbene | R₂C: | Singlet vs triplet |

### Carbocation Stability (Hyperconjugation)
- More adjacent C-H bonds = more stable
- Resonance dramatically increases stability

## Rate Determination

### Rate Laws
- **Unimolecular**: Rate = k[reactant]
- **Bimolecular**: Rate = k[reactant1][reactant2]

### Determining Mechanism from Rate
| Rate Law | Implication |
|----------|-------------|
| Rate = k[RX] | SN1 (carbocation intermediate) |
| Rate = k[RX][Nu] | SN2 (concerted) |

## Decision Flow
1. Identify reactants: nucleophile/electrophile or radical sources
2. Determine reaction type (polar vs radical)
3. Draw curved arrows showing electron movement
4. Identify intermediates and transition states
5. Consider stereochemical outcomes
6. Check for competing mechanisms

## Implementations and Data
- Mechanism predictor: [L3 code](../L3_functions/reaction_mechanism_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/reaction-mechanism-reference.md)

## Data Reference
- L4 Data: L4_reference/bond_dissociation_energies.csv — BDE values for 30 common bonds

## L3 Tool Call Directives

**Source:** `reaction_mechanism_tools.py`
SN1/SN2/E1/E2 prediction, intermediate stability, rate laws, curved arrow notation.

### Available functions:
- `predict_mechanism_sn1_sn2(substrate, nucleophile, solvent)` → MechanismType — SN1/SN2 prediction
- `predict_elimination_mechanism(substrate, base, temperature)` → MechanismType — E1/E2 prediction
- `predict_carbocation_stability(carbon_type)` → tuple[str, int] — Stability desc + relative energy (kJ/mol)
- `predict_radical_stability(radical_type)` → tuple[str, int] — Radical stability ranking
- `predict_carbanion_stability(carbanion_type)` → tuple[str, int] — Carbanion stability (opposite trend to carbocation)
- `identify_electrophile(species)` → dict — Type and strength
- `identify_nucleophile(species)` → dict — Type, strength, base_strength
- `calculate_rate_law(mechanism)` → str — Rate expression (SN1: k[RX], SN2: k[RX][Nu], etc.)
- `draw_curved_arrows(step_type)` → list[str] — Arrow notation for reaction steps
- `predict_hammond_postulate(transition_state, reaction_energy)` → str — TS character (early/late)
- `reaction_mechanism_summary()` → dict — Summary of SN1/SN2/E1/E2 properties
- `radical_chain_steps()` → dict — Initiation/propagation/termination steps

### Common errors:
- ❌ Passing substrate type as full name instead of 'primary'/'secondary'/'tertiary'/'methyl'
- ❌ Forgetting carbocation rearrangements (hydride/alkyl shifts) in SN1/E1
- ❌ Confusing nucleophile strength with base strength (e.g., I⁻ is good Nu but weak base)
- ❌ E2 requires anti-periplanar geometry — stereochemistry matters
