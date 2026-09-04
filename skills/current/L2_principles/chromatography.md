---
id: chromatography
layer: 2
title: Chromatography - Separation Science
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/chromatography_tools.py
  - ../L4_reference/reference/electrochemical-analysis-data.md
cross_links:
  - ./solution_chemistry.md
  - ./gas_behavior_and_kinetic_theory.md
source: Instrumental Analysis (LibreTexts)
---

## Context

Chromatography is a family of analytical techniques used to separate mixtures into individual components. It's based on differential partitioning between a mobile phase and a stationary phase. Applications range from pharmaceutical analysis to environmental monitoring to proteomics.

---

## Fundamental Principles

### Partition Theory

Components separate based on differential affinity for stationary vs mobile phase:

```
K = Cs / Cm
```
Where:
- K = partition coefficient
- Cs = concentration in stationary phase
- Cm = concentration in mobile phase

### Retention Time

```
tR = tM × (1 + k)
```
Where:
- tR = retention time
- tM = dead time (mobile phase travel time)
- k = retention factor

### Retention Factor (Capacity Factor)

```
k = (tR - tM) / tM
```

**Good separation**: 1 < k < 10

---

## Gas Chromatography (GC)

### Principles
- Mobile phase: inert gas (He, N₂, H₂)
- Stationary phase: liquid coated on solid support
- Separation based on volatility and polarity

### Key Parameters

| Parameter | Effect |
|-----------|--------|
| Column temperature | Lower T = longer retention, better separation |
| Carrier gas velocity | Optimal velocity minimizes H |
| Column length | Longer = more plates, better separation |
| Film thickness | Thicker = more retention |

### Van Deemter Equation

```
H = A + B/u + Cu
```

| Term | Contribution | Optimized By |
|------|--------------|--------------|
| A | Eddy diffusion | Smaller particle size |
| B | Longitudinal diffusion | Higher velocity |
| C | Mass transfer | Lower velocity |

### Optimal Linear Velocity

```
u_opt = √(B/C)
```

---

## Liquid Chromatography (HPLC)

### Principles
- Mobile phase: liquid (often gradient)
- Stationary phase: bonded silica
- Higher pressure required than GC

### Types

| Type | Stationary Phase | Separation Basis |
|------|------------------|------------------|
| Normal phase | Polar (SiO₂) | Polarity |
| Reverse phase | Non-polar (C18) | Hydrophobicity |
| Ion exchange | Charged | Charge |
| Size exclusion | Porous | Molecular size |

### Gradient Elution

```
% B = initial + (rate × time)
```

Gradient improves resolution for complex mixtures.

---

## Resolution and Efficiency

### Resolution Equation

```
Rs = (tR2 - tR1) / (0.5 × (w1 + w2))
```

**Baseline separation**: Rs ≥ 1.5

### Alternative Resolution Equation

```
Rs = (√N / 4) × (α - 1)/α × k/(1 + k)
```

Where:
- N = number of theoretical plates
- α = selectivity factor = k2/k1
- k = average retention factor

### Number of Theoretical Plates

```
N = 16 × (tR / w)²
```
Or using peak width at half height:
```
N = 5.54 × (tR / w½)²
```

---

## Harvey Textbook Problem-Solving (ch12)

### Theoretical Plates (Harvey convention)

**IMPORTANT**: When solving Harvey textbook problems, use `theoretical_plates(tR, w, convention="4")`.

Harvey uses **N = 4(tR/w)²** (not 16). The w values given are baseline peak widths.

```
N_Harvey = 4 × (tR / w)²
```

This differs from the USP convention (N = 16(tR/w)²). Always check which convention a problem expects.

### Resolution

```
Rs = 2(tR2 - tR1) / (w1 + w2)
```

This is the standard formula using baseline peak widths.

### Purnell Resolution Equation (ch12_006)

```
Rs = (√N / 4) × (α - 1)/α × k/(1 + k)
```

This is the fundamental resolution equation relating plates, selectivity, and retention.

### Kovats Retention Index

```
RI = 100 × [n + (log(tR_unknown') - log(tR_n)) / (log(tR_(n+1)) - log(tR_n))]
```

Where:
- tR' = tR - tM (adjusted retention time)
- n = carbon number of the n-alkane eluting before the unknown
- n+1 = carbon number of the n-alkane eluting after the unknown

The unknown elutes between n-alkanes with n and n+1 carbons.

### Plate Height

```
H = L / N
```
Where L = column length

---

## L3 Tool Call Directive

**Always use L3 tools instead of manual calculation.** Call functions from `chromatography_tools.py`:

- **Theoretical plates**: `theoretical_plates(tR, w, convention="4")` — use `convention="4"` for Harvey textbook problems (N = 4(tR/w)²). Use `convention="16"` (default) for other textbooks (N = 16(tR/w)²).
- **Resolution**: `resolution_from_times(tR1, tR2, w1, w2)` — Rs = 2(tR2-tR1)/(w1+w2).
- **Retention factor**: `retention_factor(tR, tM)` — k = (tR-tM)/tM.
- **Selectivity factor**: `selectivity_factor(tR1, tR2, tM)` — α = (tR2-tM)/(tR1-tM).
- **Plate height**: `plate_height(column_length, N)` — H = L/N.
- **Purnell equation**: `purnell_resolution(N, alpha, k)` — Rs = √N/4 × (α-1)/α × k/(1+k).
- **Kovats retention index**: `kovats_ri(tR_unknown, tR_n, tR_np1, tM, n_carbon)` — RI = 100 × (n + log(tR'_unknown)/log(tR'_(n+1)/tR'_n)).

## Quantitative Analysis

### Peak Area

```
Area = ∫ signal dt ≈ height × width × correction factor
```

### Calibration Methods

| Method | Description |
|--------|-------------|
| External standard | Compare to standard curve |
| Internal standard | Add known compound as reference |
| Standard addition | Spike sample with analyte |

### Internal Standard Calculation

```
Cx = (Ax / Ais) × Cis × RF
```
Where:
- Cx = analyte concentration
- Ax = analyte peak area
- Ais = internal standard area
- Cis = internal standard concentration
- RF = response factor

---

## Problem-Solving Examples

### Example 1: Calculate Resolution

**Problem**: Peak 1 has tR = 5.2 min, w = 0.3 min. Peak 2 has tR = 6.1 min, w = 0.35 min. Calculate resolution.

**Solution:**
```
Rs = (6.1 - 5.2) / (0.5 × (0.3 + 0.35))
Rs = 0.9 / 0.325
Rs = 2.77
```

**Interpretation**: Rs > 1.5, baseline separation achieved.

### Example 2: Van Deemter Minimum

**Problem**: For a column with A = 0.01 cm, B = 0.5 cm²/s, C = 0.03 s, find optimal velocity.

**Solution:**
```
u_opt = √(B/C) = √(0.5 / 0.03) = √(16.7) = 4.1 cm/s
```

### Example 3: Theoretical Plates

**Problem**: A peak elutes at 12.5 min with width 0.4 min. Calculate N for a 30 m column.

**Solution:**
```
N = 16 × (12.5 / 0.4)² = 16 × 976.6 = 15,625 plates
H = L/N = 30,000 mm / 15,625 = 1.92 mm/plate
```

---

## Decision Flow

1. **Choose chromatography type:**
   - Volatile compounds? → GC
   - Non-volatile/polar? → HPLC
   - Ions? → Ion chromatography
   - Proteins? → Size exclusion or affinity

2. **Optimize resolution:**
   - Increase N (longer column, smaller particles)
   - Increase α (change stationary phase)
   - Adjust k (change temperature or mobile phase)

3. **Quantitative analysis:**
   - Simple matrix? → External standard
   - Complex matrix? → Internal standard
   - Unknown matrix effects? → Standard addition

---

## Implementations and Data
- Chromatography tools: [L3 code](../L3_functions/chromatography_tools.py)
- Reference tables: [L4 reference](../L4_reference/reference/electrochemical-analysis-data.md)
