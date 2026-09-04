# L2 Topic: s-Block Elements (Groups 1-2)

**Source**: Petrucci General Chemistry, Ch21.1-21.3
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

The s-block elements are the most reactive groups in the periodic table. They include:
- **Group 1**: Alkali metals (Li, Na, K, Rb, Cs)
- **Group 2**: Alkaline earth metals (Be, Mg, Ca, Sr, Ba)

### Key Features
1. **Never found free in nature** - must be isolated
2. **Form +1 ions (Group 1) + +2 ions (Group 2)
3. **Low melting points** - decreases down groups
4. **Strong reducing agents** - strongest known

---

## Core Principles

### Group 1: Alkali Metals
- **Valence**: nsÂ¹ configuration
- **Reactions**: HâO, halogens, Oâ? Nâ?(Li only), Hâ?- **Oxides**: LiâO, NaâOâ?(peroxide), K/Rb/Cs â?superoxides (MOâ?
- **Isolation**: Electrolysis of molten chlorides

### Group 2 Trends
| Property | Trend |
|-----------|-------|
| Atomic radius | Increases |
| Ionization energy | Decrease |
| Melting point | Decrease |
| Density | Increase |
| Reducing power | Li strongest in solution |

### Group 2 Reactions
| Element | With Nâ?| With Oâ?|
|--------|--------|----------|
| Li | Yes | LiâO |
| Na | No | NaâOâ?|
| K | No | KOâ?|
| Rb | No | RbOâ?|
| Cs | No | CsOâ?|

### Group 2: Alkaline Earth Metals
- **Valence**: nsÂ² configuration
- **Reactions**: HâO, halogens, Oâ? Nâ?(all except Be), Hâ?- **Oxides**: All form MO (Ba forms BaOâ?peroxide)
- **Isolation**: Electrolysis or molten chlorides

### Group 2 Trends
| Property | Trend |
|-----------|-------|
| Atomic radius | Increase |
| Ionization energy | Decrease |
| Melting point | Variable |
| Hydroxide solubility | Increases |
| Carbonate solubility | Decreases |
| Sulfate solubility | Decreases |

### Group 2 vs Group 1 Differences
| Aspect | Group 1 | Group 2 |
|--------|--------|--------|
| Charge | +1 | +2 |
| Reactivity with Nâ?| Li only | Mg-Ba |
| Oxide products | Varied | Mostly MO |
| Amphotericity | None | BeO |

---

## Decision Trees

### Predicting Oxide Product
```
Element in Group 1?
    â?Li? â?LiâO (oxide)
Na? â?NaâOâ?(peroxide)
K, Rb, Cs? â?MOâ?(superoxide)
```

### Predicting Nitride Formation
```
Group 1?
    â?Li? â?YES (LiâN)
Others? â?NO
```

```
Group 2?
    â?Be? â?NO
Mg-Ba? â?YES (MâNâ?
```

---

## Key Tables

### Group 1 Properties
| Element | Atomic # | MP (Â°C) | EÂ° (V) | IEâ?(kJ/mol) |
|---------|----------|---------|----------|--------------|
| Li | 3 | 180.5 | -3.04 | 520 |
| Na | 11 | 97.8 | -2.71 | 496 |
| K | 19 | 63.5 | -2.93 | 419 |
| Rb | 37 | 39.3 | -2.98 | 403 |
| Cs | 55 | 28.5 | -3.03 | 376 |

### Group 2 Properties
| Element | Atomic # | MP (Â°C) | EÂ° (V) | IEâ?(kJ/mol) |
|---------|----------|---------|----------|--------------|
| Be | 4 | 1287 | -1.85 | 900 |
| Mg | 12 | 650 | -2.37 | 738 |
| Ca | 20 | 842 | -2.87 | 590 |
| Sr | 38 | 777 | -2.90 | 549 |
| Ba | 56 | 727 | -2.91 | 503 |

---

## Connected Topics

- **Upstream**: [periodic_trends.md](periodic_trends.md)
- **Related**: Main-group chemistry

---

## L3 Tools Required

1. `s_block_tools.py` - Oxide products, reactivity patterns

---

## L4 References (TODO)

- [ ] Group 1/2 property tables
- [ ] Hydration energies
- [ ] Solubility data

---

## L5 Worked Examples (TODO)

- [ ] Predicting oxide products
- [ ] Predicting reaction products
- [ ] Comparing alkali vs alkaline earth reactions


## Implementations

- Implementation: `../L3_functions/s_block_elements_tools.py`

## L3 Tool Call Directives

**Source:** `s_block_elements_tools.py` | `s_block_tools.py`
s-Block element properties, reactions, trends, flame tests, oxide chemistry, solubility.

### Available functions (s_block_elements_tools):
- `alkali_metal_property(element, property_name)` → float — Get alkali metal property (IE, EA, radius, density, etc.)
- `alkaline_earth_property(element, property_name)` → float — Get alkaline earth metal property
- `group_1_reaction(element, reactant)` → str — Predict Group 1 reaction product (with O₂, H₂O, halogens, N₂, H₂)
- `group_2_reaction(element, reactant)` → str — Predict Group 2 reaction product
- `diagonal_relationship(element1, element2)` → bool — Check diagonal relationship (Li/Mg, Be/Al)
- `flame_test_color(element)` → str — Predict flame test color for s-block element
- `s_block_trend(property_type)` → str — Describe periodic trend (IE, EA, radius, reactivity, etc.)
- `compare_alkali_alkaline_earth()` → dict — Compare Group 1 vs Group 2 properties

### Available functions (s_block_tools):
- `oxide_product(element)` → dict — Predict oxide product and type (normal/peroxide/superoxide)
- `reacts_with_nitrogen(element)` → dict — Check if s-block element reacts with N₂ at room temperature
- `hydration_energy_ranking(group)` → dict — Rank hydration energies (more exothermic for smaller ions)
- `solubility_trend(compound_type)` → dict — Describe solubility trends (hydroxides, sulfates, carbonates)
- `is_amphoteric(element)` → dict — Check if element forms amphoteric oxide/hydroxide (Be, Al)

### Common errors:
- ❌ Assuming all Group 1 oxides are normal oxides (Na forms peroxide, K/Rb/Cs form superoxide)
- ❌ Forgetting that Be and Mg do NOT react with water at room temperature
