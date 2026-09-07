# L2 Topic: Halogens and Noble Gases (Groups 17-18)

**Source**: Petrucci General Chemistry, Ch22.2-22.3
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

The halogens and noble gases complete the p-block, representing the most electronegative elements and the least reactive (historically "inert") elements.

### Group 17: Halogens
- **Elements**: F, Cl, Br, I, At
- **Character**: Highly reactive nonmetals
- **Key trend**: Reactivity decreases down group
- **Uses**: Disinfectants, pharmaceuticals, plastics (PVC)

### Group 18: Noble Gases
- **Elements**: He, Ne, Ar, Kr, Xe, Rn
- **Character**: Least reactive (historically "inert")
- **Key trend**: Reactivity increases down group
- **Uses**: Lighting, cryogenics, anesthesia

---

## Core Principles

### Halogen Trends
| Property | Trend |
|----------|-------|
| Electronegativity | Decreases (F highest at 4.0) |
| Bond strength (X-X) | Cl > Br > F > I |
| Oxidizing power | Decreases (F₂ strongest in gas) |
| Physical state | Gas → Liquid → Solid |

### Halogen Anomalies
- **F-F bond weak**: Lone pair repulsion
- **F EA < Cl EA**: Electron repulsion in small atom
- **Cl strongest oxidant in water**: Hydration energy effect

### Noble Gas Trends
| Property | Trend |
|----------|-------|
| Ionization energy | Decreases |
| Reactivity | Increases (only Xe, Kr form compounds) |
| Boiling point | Increases |

### Noble Gas Compounds
- **He, Ne, Ar**: No stable compounds (IE too high)
- **Kr**: KrF₂ only
- **Xe**: XeF₂, XeF₄, XeF₆, XeO₃, XeO₄, XeO₆⁴⁻
- **Rn**: RnF₂ (predicted more, but radioactive)

---

## Decision Trees

### Predicting Halogen Reaction
```
With metal? → MXn (ionic or covalent)
With H₂? → HX (hydrogen halide)
With H₂O? → HX + HOX (disproportionation, NOT F₂)
With other halogen? → Interhalogen (heavier is central)
```

### Predicting Noble Gas Compound
```
He, Ne, Ar? → No compounds
Kr? → KrF₂ (with F₂ under forcing conditions)
Xe? → Fluorides (XeF₂, XeF₄, XeF₆), oxides (XeO₃, XeO₄)
```

---

## Key Tables

### Halogen Properties
| Element | State | Electronegativity | X-X Bond |
|---------|-------|-------------------|----------|
| F | Gas | 4.0 | 159 kJ/mol |
| Cl | Gas | 3.2 | 244 kJ/mol |
| Br | Liquid | 3.0 | 193 kJ/mol |
| I | Solid | 2.7 | 151 kJ/mol |

### Noble Gas Reactivity
| Element | IE (kJ/mol) | Known Compounds |
|---------|-------------|-----------------|
| He | 2372 | None |
| Ne | 2081 | None |
| Ar | 1521 | None |
| Kr | 1351 | KrF₂ |
| Xe | 1170 | XeF₂, XeF₄, XeF₆, XeO₃, XeO₄ |

---

## Connected Topics

- **Upstream**: [p_block_elements.md](p_block_elements.md)
- **Related**: Main-group chemistry, periodic trends

---

## L3 Tools Required

1. `halogen_tools.py` - Oxidizing power, interhalogen prediction
2. `noble_gas_tools.py` - Compound formation prediction

---

## L4 References (TODO)

- [ ] Halogen bond energy tables
- [ ] Noble gas compound stability data
- [ ] Interhalogen structures

---

## L5 Worked Examples (TODO)

- [ ] Predicting interhalogen formulas
- [ ] Xe compound stoichiometry
- [ ] Oxidizing power comparisons

## L3 Tool Call Directives

**Source:** `halogen_tools.py`
Halogen oxidizing power, interhalogen compounds, noble gas compound formation.

### Available functions:
- `oxidizing_power(element, phase)` → dict — Compare halogen oxidizing power (gas vs aqueous rankings differ!)
- `interhalogen_formula(halogen1, halogen2)` → dict — Predict interhalogen formula (heavier = central)
- `forms_noble_gas_compound(element)` → dict — Check if noble gas forms compounds and list examples
- `max_halogen_oxidation(metal, halogen)` → dict — Predict relative oxidation state of metal with halogen
- `halogen_disproportionates(element)` → dict — Check if halogen disproportionates in water (F₂ does NOT)

### Common errors:
- ❌ Assuming gas-phase and aqueous oxidizing power rankings are the same (Cl₂ > F₂ in water!)
- ❌ Predicting F₂ disproportionation (F₂ does not disproportionate, too electronegative)
