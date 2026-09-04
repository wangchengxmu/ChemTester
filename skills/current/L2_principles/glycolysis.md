# L2 Topic: Glycolysis

**Source**: Fundamentals of Biochemistry (Jakubowski/Flatt)
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

Glycolysis is the metabolic pathway that converts glucose to pyruvate, producing ATP and NADH. It occurs in the cytoplasm and is the first step of cellular respiration.

### Key Features
1. **10 enzymatic reactions**: Glucose → 2 Pyruvate
2. **Energy investment**: 2 ATP consumed
3. **Energy production**: 4 ATP + 2 NADH generated
4. **Net yield**: 2 ATP + 2 NADH per glucose

---

## Core Principles

### The 10 Steps

| Step | Enzyme | Reaction | ATP/NADH |
|------|--------|----------|----------|
| 1 | Hexokinase | G → G-6-P | -1 ATP |
| 2 | Phosphoglucose isomerase | G-6-P → F-6-P | - |
| 3 | Phosphofructokinase (PFK) | F-6-P → F-1,6-BP | -1 ATP |
| 4 | Aldolase | F-1,6-BP → DHAP + G3P | - |
| 5 | Triose phosphate isomerase | DHAP → G3P | - |
| 6 | GAPDH | G3P → 1,3-BPG | +1 NADH × 2 |
| 7 | Phosphoglycerate kinase | 1,3-BPG → 3-PG | +1 ATP × 2 |
| 8 | Phosphoglycerate mutase | 3-PG → 2-PG | - |
| 9 | Enolase | 2-PG → PEP | - |
| 10 | Pyruvate kinase | PEP → Pyruvate | +1 ATP × 2 |

### Energy Summary

| Phase | ATP | NADH |
|-------|-----|------|
| Investment (1-3) | -2 | 0 |
| Payoff (6-10) | +4 | +2 |
| **Net** | **+2** | **+2** |

### Regulation Points

| Enzyme | Regulator | Effect |
|--------|-----------|--------|
| Hexokinase | G-6-P | Inhibition |
| PFK-1 | ATP, Citrate | Inhibition |
| PFK-1 | AMP, ADP, F-2,6-BP | Activation |
| Pyruvate kinase | ATP, Alanine | Inhibition |
| Pyruvate kinase | F-1,6-BP | Feed-forward activation |

### Anaerobic Fates

| Condition | Product | Enzyme |
|-----------|---------|--------|
| Muscle (low O₂) | Lactate | Lactate dehydrogenase |
| Yeast | Ethanol + CO₂ | Pyruvate decarboxylase, ADH |

---

## Key Formulas

### Net ATP Yield (Aerobic)
$$\text{ATP}_{glycolysis} = 2 \text{ (substrate-level)} + 5 \text{ (NADH oxidation)} = 7 \text{ ATP}$$

Using modern P/O ratios (2.5 ATP/NADH)

### PFK Rate Equation
$$v = \frac{V_{max}[F6P][ATP]}{K_m^{F6P}K_m^{ATP} + K_m^{ATP}[F6P] + K_m^{F6P}[ATP](1 + \frac{[ATP]}{K_i}) + [F6P][ATP]}$$

---

## L3 Implementations Needed

| Function | Purpose |
|----------|---------|
| `glycolysis_atp_yield` | Calculate net ATP |
| `pfk_rate` | Model PFK kinetics |
| `glucose_fate` | Determine aerobic vs anaerobic |

## L4 Data Needed

| Table | Content |
|-------|---------|
| `glycolysis_enzymes.csv` | Km, Vmax, effectors |
| `glycolysis_intermediates.csv` | Structures, ΔG° |

## L5 Examples Needed

| Example | Topic |
|---------|-------|
| ATP yield calculation | Complete accounting |
| Regulation analysis | PFK kinetics |

---

**Cross-links:**
- metabolic_pathways.md
- tca_cycle.md
- enzyme_kinetics.md
