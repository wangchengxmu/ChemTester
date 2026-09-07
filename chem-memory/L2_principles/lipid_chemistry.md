# L2 Topic: Lipid Chemistry

**Source**: Human Biology (Wakim and Grewal), Ch3.6
**Created**: 2026-03-13
**Status**: Complete (Pass-4)

---

## Concept Overview

Lipids are biomolecules soluble in nonpolar solvents, Includes fatty acids, triglycerides, phospholipids, and steroids.

### Key Features
1. **Fatty acids** - Building blocks of lipids
2. **Saturation** - Saturated vs unsaturated chains
3. **Melting points** - Depend on chain structure
4. **Iodine value** - Measure of unsaturation

---

## Core Principles

### Fatty Acid Classification

| Type | Double Bonds | State at 25°C | Example |
|------|--------------|----------------|---------|
| Saturated | 0 | Solid | Stearic (C18:0) |
| Monounsaturated | 1 | Liquid | Oleic (C18:1) |
| Polyunsaturated | ≥2 | Liquid (cold) | Linoleic (C18:2) |

### Naming Convention
- C{n}:{m} where n = carbons, m = double bonds
- Example: Arachidonic acid = C20:4

### Melting Point Rules
- More saturation → Higher MP
- More double bonds → Lower MP
- Longer chains → Higher MP

---

## Decision Trees

### Classifying Fatty Acids
```
Number of double bonds?
├── 0? → Saturated
├── 1? → Monounsaturated
└── ≥2? → Polyunsaturated
```

### Predicting Physical State
```
Saturated + long chain? → Solid at room temp
Unsaturated? → Liquid at room temp
High polyunsaturation? → Liquid even when cold
```

---

## L3 Tools

1. `lipid_chemistry_tools.py` - Fatty acid analysis

## L3 Tool Call Directives

**Source:** `lipid_chemistry_tools.py`

Fatty acid analysis: saturation classification, melting point estimation, iodine value interpretation, and energy calculations.

### Available functions:
- `fatty_acid_info(notation)` → dict — Returns name, carbons, double_bonds, mp, saturation_type; accepts 'C18:1' or 'Oleic'
- `classify_saturation(n_double_bonds)` → dict — Returns type ('saturated'|'monounsaturated'|'polyunsaturated') and state description
- `melting_point_estimate(n_carbons, n_double_bonds)` → dict — Estimated MP: +4°C per carbon, -25°C per double bond
- `iodine_value_interpret(value)` → dict — Classifies: <50 low, 50-100 moderate, 100-150 high, >150 very high (drying oils)
- `triglyceride_energy(fatty_acids)` → dict — Returns energy_density (~9 kcal/g) and estimated MW from fatty acid list

### Common errors:
- ❌ Confusing notation: C18:1 means 18 carbons with 1 double bond (not 18:1 ratio)
- ❌ Forgetting that one double bond drops MP by ~25°C (C18:0 MP=70°C vs C18:1 MP=13°C)
- ❌ Not recognizing that iodine value is a proxy for unsaturation (more I₂ absorbed = more double bonds)

## Connected Topics

- **Upstream**: [organic_functional_groups.md](organic_functional_groups.md)
- **Related**: [amino_acid_properties.md](amino_acid_properties.md)
