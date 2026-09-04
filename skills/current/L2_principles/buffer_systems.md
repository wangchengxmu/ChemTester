---
id: acid_base.buffer_systems
layer: 2
title: Buffer Systems - Mechanism, Calculations, and Design
stability: high
confidence: high
sources:
  - url: https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_2e_(OpenStax)/14%3A_Acid-Base_Equilibria
    book_id: libretexts-chemistry-2e-openstax
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/buffer_calculator.py
  - ../L3_functions/buffer_calculators.py
  - ../L4_reference/buffer/protocol-buffer-design-and-prep.md
  - ../L4_reference/reference/equilibrium-constants-and-reference-datasets.md
  - ../L5_examples/buffer/case-phosphate-50mM-ph74.md
cross_links:
  - ./quantitative_measurement_and_uncertainty.md
  - ./acid_base_constants.md
  - ./titrations.md
---

## Context

Buffer solutions resist pH changes when small amounts of acid or base are added. They are essential tools in chemistry for maintaining stable pH conditions in reactions, biological systems, and analytical procedures.

## Core Model

### Definition and Mechanism

A **buffer system** consists of:
- A **weak acid** and its **conjugate base**, OR
- A **weak base** and its **conjugate acid**

The equilibrium between these components resists pH changes under small perturbations.

### Buffer Composition Examples

| Buffer Type | Components | Example |
|-------------|------------|---------|
| Acidic buffer | Weak acid + its salt | CH₃COOH + CH₃COO⁻ |
| Basic buffer | Weak base + its salt | NH₃ + NH₄⁺ |
| Biological | Weak acid + conjugate base | H₂CO₃ + HCO₃⁻ |

---

## Henderson-Hasselbalch Equation

### Derivation

For a weak acid HA dissociating:
```
HA ⇌ H⁺ + A⁻
Ka = [H⁺][A⁻] / [HA]
```

Rearranging:
```
[H⁺] = Ka × [HA] / [A⁻]

Taking -log of both sides:
pH = pKa + log([A⁻] / [HA])
```

### The Henderson-Hasselbalch Equation

```
pH = pKa + log([base] / [acid])
```

Or equivalently:
```
pH = pKa + log([A⁻] / [HA])
```

### Key Insights

1. **Pair match heuristic:** Best practical region near `pKa ± 1`
2. **Ratio controls pH:** The ratio [base]/[acid] determines the pH
3. **Concentration affects capacity:** Total concentration [HA] + [A⁻] determines buffer capacity

---

## Buffer Capacity

### Definition

**Buffer capacity (β)** is the amount of strong acid or base that can be added before the pH changes significantly.

```
β = dCb / dpH = -dCa / dpH
```

Where:
- dCb = moles of base added per liter
- dCa = moles of acid added per liter
- dpH = resulting pH change

### Maximum Buffer Capacity

**Maximum capacity occurs when:**
```
[HA] = [A⁻]
pH = pKa
```

At this point:
```
β_max = 2.303 × C_total / 4 = 0.576 × C_total
```

Where C_total = [HA] + [A⁻]

### Buffer Range

**Effective buffer range:** `pKa ± 1`

Outside this range, the buffer loses effectiveness:
- pH < pKa - 1: [HA] >> [A⁻], little conjugate base available
- pH > pKa + 1: [A⁻] >> [HA], little weak acid available

---

## Buffer Preparation Methods

### Method 1: Mix Weak Acid + Its Salt

```
Add sodium acetate (CH₃COONa) to acetic acid (CH₃COOH)
```

### Method 2: Mix Weak Base + Its Salt

```
Add ammonium chloride (NH₄Cl) to ammonia (NH₃)
```

### Method 3: Partial Neutralization

```
Neutralize part of weak acid with strong base:
CH₃COOH + NaOH → CH₃COONa + H₂O
(Use stoichiometry to control ratio)
```

---

## Decision Flow for Buffer Design

1. **Choose candidate conjugate pair** with pKa near target pH
2. **Compute required base/acid ratio** for target pH using Henderson-Hasselbalch
3. **Evaluate robustness** (pair match + expected perturbation)
4. **Pull pKa/reference constants** from L4 reference
5. **Execute preparation workflow** from L4 protocol
6. **Compare against prior L5 cases**

---

## Problem-Solving Routes

### 1. Calculate Buffer pH

**Problem:** Given concentrations of weak acid and conjugate base, find pH.

**Solution:** Use Henderson-Hasselbalch equation
```
pH = pKa + log([A⁻] / [HA])
```

**Example:**
```
Buffer with [CH₃COOH] = 0.10 M and [CH₃COO⁻] = 0.15 M
pKa(CH₃COOH) = 4.76

pH = 4.76 + log(0.15/0.10)
pH = 4.76 + log(1.5)
pH = 4.76 + 0.18
pH = 4.94
```

### 2. Calculate pH After Adding Acid/Base

**Problem:** Buffer with [HA] and [A⁻]; add strong acid or base; find new pH.

**Method:**
1. Calculate moles of each component
2. Add/subtract moles based on reaction
3. Recalculate concentrations
4. Apply Henderson-Hasselbalch

**Example:**
```
100 mL of 0.10 M CH₃COOH / 0.10 M CH₃COO⁻ buffer
Add 1.0 mL of 1.0 M HCl

Initial moles: HA = 0.010 mol, A⁻ = 0.010 mol
Added HCl: 0.001 mol H⁺

Reaction: A⁻ + H⁺ → HA
New moles: HA = 0.011 mol, A⁻ = 0.009 mol
New volume: 101 mL

[HA] = 0.011/0.101 = 0.109 M
[A⁻] = 0.009/0.101 = 0.089 M

pH = 4.76 + log(0.089/0.109) = 4.76 - 0.089 = 4.67
```

### 3. Design a Buffer

**Problem:** Prepare buffer at target pH with given capacity.

**Method:**
1. Choose weak acid with pKa ≈ target pH
2. Calculate required ratio: `[A⁻]/[HA] = 10^(pH - pKa)`
3. Choose total concentration for capacity
4. Calculate individual concentrations

**Example:**
```
Design pH 5.0 buffer with total concentration 0.20 M

Step 1: Choose CH₃COOH (pKa = 4.76)

Step 2: Calculate ratio
10^(5.0 - 4.76) = 10^0.24 = 1.74

Step 3: Solve for concentrations
[A⁻]/[HA] = 1.74
[HA] + [A⁻] = 0.20 M

[A⁻] = 1.74[HA]
[HA] + 1.74[HA] = 0.20
2.74[HA] = 0.20
[HA] = 0.073 M
[A⁻] = 0.127 M
```

### 4. Determine Buffer Capacity

**Problem:** How much acid/base can be added before pH changes significantly?

**Method:**
Calculate β or determine from concentration.

**Rule of thumb:** Buffer can typically neutralize ~10-20% of total buffer concentration before pH changes by 1 unit.

---

## Common Buffer Systems

| Buffer | pKa | Effective pH Range | Applications |
|--------|-----|-------------------|--------------|
| Acetate | 4.76 | 3.8-5.8 | Biochemistry, electrophoresis |
| Phosphate | 7.21 (pKa2) | 6.2-8.2 | Biological systems, HPLC |
| Tris | 8.06 | 7.1-9.1 | Molecular biology |
| Carbonate | 10.33 | 9.3-11.3 | Alkaline buffers |
| Citrate | 3.13, 4.76, 6.40 | 2.1-7.4 | Wide range applications |
| Borate | 9.24 | 8.2-10.2 | Gel electrophoresis |

---

## Limits and Considerations

### Activity Effects

- Concentration-based formulas deviate at high ionic strength
- Activity coefficients should be used for accurate work
- Debye-Hückel theory can correct for ionic strength effects

### Dilution Effects

- Diluting buffer changes pH slightly
- Henderson-Hasselbalch uses concentrations, not moles
- More significant for buffers with high [base]/[acid] ratios

### Temperature Effects

- pKa values are temperature-dependent
- Tris buffer: ΔpKa/ΔT ≈ -0.031 per °C
- Critical for precise pH control

### Large Additions

- Large strong acid/base additions can invalidate small-perturbation approximations
- Buffer capacity may be exceeded
- pH may change dramatically

---

## Cross-Links

- **Acid-base constants** (Ka, Kb) → See `acid_base_constants.md`
- **Titration curves** → See `titrations.md`
- **Equilibrium calculations** → See `equilibrium_calculations.md`

---

## Direct Implementations

- **Solver interface:** [L3 skill](../L3_functions/buffer_calculator.py)
- **Calculators:** [L3 code](../L3_functions/buffer_calculators.py)
- **Reference data:** [L4 reference](../L4_reference/reference/equilibrium-constants-and-reference-datasets.md)
- **Preparation protocol:** [L4 protocol](../L4_reference/buffer/protocol-buffer-design-and-prep.md)
- **Example case:** [L5 case](../L5_examples/buffer/case-phosphate-50mM-ph74.md)

---

## References

- LibreTexts Chemistry 2e (OpenStax), Chapter 14: Acid-Base Equilibria
- Harris, Quantitative Chemical Analysis
- Skoog, West, Holler, Crouch, Analytical Chemistry
