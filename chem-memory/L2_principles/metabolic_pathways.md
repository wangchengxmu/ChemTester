# L2 Topic: Metabolic Pathways

**Source**: Organic Chemistry (OpenStax) Ch29
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Metabolic pathways are the organized series of chemical reactions that occur in cells to maintain life. They follow the same organic chemistry principles as laboratory reactions.

### Key Features
1. **Catabolism vs Anabolism**: Breakdown vs synthesis
2. **Energy coupling**: ATP, NADH, FADH2
3. **Regulation**: Enzyme control points
4. **Integration**: Pathways interconnect

---

## Core Principles

### 29.1: Metabolism Overview
- **Catabolism**: Exergonic, releases energy
- **Anabolism**: Endergonic, requires energy
- **ATP**: Universal energy currency

### 29.2-29.3: Fatty Acid Catabolism
- Triacylglycerol hydrolysis
- β-Oxidation: 4-step cycle
- ATP yield calculation

### 29.4: Fatty Acid Biosynthesis
- Malonyl CoA as building block
- NADPH as reductant
- Fatty acid synthase complex

### 29.5: Glycolysis
- Glucose → 2 Pyruvate
- Net: 2 ATP, 2 NADH
- 10 enzyme-catalyzed steps

### 29.6: Pyruvate Metabolism
- Aerobic: → Acetyl CoA
- Anaerobic: → Lactate or Ethanol

### 29.7: Citric Acid Cycle
- Acetyl CoA → 2 CO2
- Yields: 3 NADH, 1 FADH2, 1 GTP

### 29.8: Gluconeogenesis
- Synthesis of glucose
- Bypasses irreversible glycolysis steps

### 29.9: Protein Catabolism
- Deamination (remove NH2)
- Carbon skeleton enters CAC

---

## Decision Trees

### Energy Source Selection
```
Need quick energy? → Glucose (glycolysis)
Need sustained energy? → Fatty acids (β-oxidation)
Low glucose, need brain fuel? → Gluconeogenesis
```

### β-Oxidation Calculation
```
Fatty acid with n carbons:
- Rounds = n/2 - 1
- Acetyl CoA = n/2
- ATP ≈ 10 × n/2 + 2.5 × rounds + 1.5 × rounds
```

---

## Key Tables

### β-Oxidation Yield (Common Fatty Acids)
| Fatty Acid | Carbons | Rounds | Acetyl CoA | ~ATP |
|------------|---------|--------|------------|------|
| Palmitic | 16 | 7 | 8 | 106 |
| Stearic | 18 | 8 | 9 | 120 |
| Oleic | 18 | 8 | 9 | 118 |
| Arachidic | 20 | 9 | 10 | 134 |

### Glycolysis vs Gluconeogenesis
| Feature | Glycolysis | Gluconeogenesis |
|---------|------------|-----------------|
| Net ATP | +2 | -6 |
| Location | Cytosol | Cytosol + Mitochondria |
| Regulation | Activated by AMP | Activated by acetyl CoA |

---

## Connected Topics

- **Upstream**: [lipids.md](lipids.md) (fatty acids)
- **Upstream**: [amino_acids.md](amino_acids.md) (proteins)
- **Related**: Carbohydrates, Energy metabolism

---

## L3 Tools Required

1. `metabolic_pathway_tools.py` - ATP yields, pathway calculations

---

## L4 References (TODO)

- [ ] Complete ATP yield tables
- [ ] Enzyme regulation points
- [ ] Pathway integration data

---

## L5 Worked Examples (TODO)

- [ ] β-Oxidation calculation examples
- [ ] Glycolysis step-by-step
- [ ] Gluconeogenesis bypass reactions

## L3 Tool Call Directives

**Source:** `metabolic_pathway_tools.py`
Metabolic pathway ATP yields: beta-oxidation, glycolysis, TCA cycle, gluconeogenesis.

### Available functions:
- `fatty_acid_atp_yield(n_carbons, saturated, n_double_bonds)` → dict — ATP yield from beta-oxidation
- `beta_oxidation_rounds(n_carbons)` → int — Number of beta-oxidation rounds (n/2 - 1)
- `acetyl_coa_from_fatty_acid(n_carbons)` → int — Number of acetyl CoA produced (n/2)
- `glycolysis_products(glucose_molecules)` → dict — Net products from glycolysis
- `citric_acid_cycle_yield(acetyl_coa_molecules)` → dict — Products per acetyl CoA from CAC
- `total_atp_from_glucose(aerobic)` → dict — Complete ATP breakdown for glucose oxidation
- `gluconeogenesis_energy_cost()` → dict — Energy cost to synthesize one glucose

### Common errors:
- ❌ Not subtracting FADH₂ for each double bond in unsaturated fatty acids
- ❌ Forgetting the -2 ATP activation cost for fatty acids
