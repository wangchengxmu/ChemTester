# L2 Topic: Carbohydrate Chemistry

**Source**: Human Biology (Wakim and Grewal), Ch3.5
**Created**: 2026-03-13
**Status**: Complete (Pass-4)

---

## Concept Overview

Carbohydrates are the most common class of biochemical compounds, built from monosaccharide monomers.

### Key Features
1. **Monosaccharides** - 6-carbon simple sugars
2. **Disaccharides** - Two monosaccharides linked
3. **Polysaccharides** - Long-chain polymers
4. **Energy storage** - 4 kcal/g

---

## Core Principles

### Classification

| Type | Units | Examples |
|------|-------|----------|
| Monosaccharide | 1 | Glucose, Fructose, Galactose |
| Disaccharide | 2 | Sucrose, Lactose, Maltose |
| Polysaccharide | Many | Starch, Glycogen, Cellulose |

### Energy Density
- Carbohydrates: **4 kcal/g**
- Lipids: **9 kcal/g** (2.25× more)

### Glycosidic Bonds
- α-linkages: Human-digestible (starch, glycogen)
- β-linkages: Human-indigestible (cellulose = fiber)

---

## Decision Trees

### Identifying Carbohydrate Type
```
Number of monosaccharide units?
├── 1? → Monosaccharide (glucose, fructose)
├── 2? → Disaccharide (sucrose, lactose)
└── Many? → Polysaccharide (starch, cellulose)
```

### Digestibility
```
Type of glycosidic bond?
├── α-linkage? → Digestible (starch, glycogen)
└── β-linkage? → Indigestible (cellulose, fiber)
```

---

## L3 Tools

1. `carbohydrate_chemistry_tools.py` - Carbohydrate analysis

---

## Connected Topics

- **Upstream**: [organic_functional_groups.md](organic_functional_groups.md)
- **Related**: [lipid_chemistry.md](lipid_chemistry.md)

## L3 Tool Call Directives


**Source:** `carbohydrate_chemistry_tools.py`

L3 tool module for carbohydrate chemistry tools

### Available functions:
- `disaccharide_info(name: str)` → dict — Get disaccharide composition and properties.
- `polysaccharide_info(name: str)` → dict — Get polysaccharide composition and properties.
- `monosaccharide_info(name: str)` → dict — Get monosaccharide properties.
- `fiber_recommendation(age: int, gender: str)` → dict — Get daily fiber recommendation.
- `energy_comparison()` → dict — Compare energy density of carbohydrates vs lipids.
- `glycosidic_bond_digestibility(bond_type: str)` → dict — Determine if glycosidic bond is digestible by humans.
- `glycogen_storage_info()` → dict — Get information about glycogen storage in humans.

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
