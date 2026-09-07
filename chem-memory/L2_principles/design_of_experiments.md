# L2 Topic: Design of Experiments (DOE)

**Source**: LibreTexts Analytical Chemistry; Chemometrics
**Created**: 2026-03-18
**Status**: Pass-1

---

## Concept Overview

Design of Experiments (DOE) is a systematic approach to planning experiments that efficiently investigates the effects of multiple factors and their interactions. It minimizes the number of experiments while maximizing information gained.

### Key Features
1. **Factorial designs**: Study multiple factors simultaneously
2. **Screening designs**: Identify important factors
3. **Optimization designs**: Find optimal conditions
4. **Response surface methodology**: Model complex relationships

---

## Core Principles

### Terminology

| Term | Definition |
|------|------------|
| Factor | Variable that affects response |
| Level | Value of a factor |
| Response | Measured outcome |
| Treatment | Combination of factor levels |
| Replicate | Repeated experiment under same conditions |
| Randomization | Order of runs randomized |
| Blocking | Group runs to control variability |

### Factorial Designs

**Full Factorial (2^k):**
| Factors | Runs | Interactions |
|---------|------|--------------|
| 2 | 4 | 1 (AB) |
| 3 | 8 | 4 (AB, AC, BC, ABC) |
| 4 | 16 | 11 |
| 5 | 32 | 26 |

**Fractional Factorial (2^(k-p)):**
| Design | Resolution | Confounding |
|--------|------------|-------------|
| 2^(3-1) | III | Main effects with 2-factor |
| 2^(4-1) | IV | Main effects clear |
| 2^(5-1) | V | Main + 2-factor clear |

### Design Matrix Examples

**2² Factorial:**
| Run | A | B | AB |
|-----|---|---|----|
| 1 | - | - | + |
| 2 | + | - | - |
| 3 | - | + | - |
| 4 | + | + | + |

**2³ Factorial:**
| Run | A | B | C | AB | AC | BC | ABC |
|-----|---|---|---|----|----|----|----|
| 1 | - | - | - | + | + | + | - |
| 2 | + | - | - | - | - | + | + |
| 3 | - | + | - | - | + | - | + |
| 4 | + | + | - | + | - | - | - |
| 5 | - | - | + | + | - | - | + |
| 6 | + | - | + | - | + | - | - |
| 7 | - | + | + | - | - | + | - |
| 8 | + | + | + | + | + | + | + |

### Response Surface Designs

**Central Composite Design (CCD):**
- Factorial points (2^k)
- Axial points (2k) at ±α
- Center points (n₀)

**Box-Behnken Design:**
- Edge midpoints only
- No corner or axial points
- More efficient for 3+ factors

---

## Decision Trees

### Design Selection
```
Number of factors?
├── 1 → One-factor-at-a-time (not recommended)
├── 2-4 → Full factorial or CCD
├── 5-7 → Fractional factorial (Resolution IV+)
└── 8+ → Plackett-Burman or definitive screening
```

### Goal-Based Selection
```
Goal?
├── Screening → Fractional factorial, P-B
├── Optimization → CCD, Box-Behnken
├── Robustness → Taguchi, fractional factorial
└── Mechanism → Full factorial
```

---

## Key Formulas

### Effect Calculation
$$\text{Effect}_A = \frac{2}{N} \sum_{i=1}^{N} x_{A,i} \cdot y_i$$

Where $x_{A,i}$ is the coded level (-1 or +1)

### Main Effect
$$E_A = \bar{y}_{A+} - \bar{y}_{A-}$$

### Interaction Effect
$$E_{AB} = \frac{1}{2}(E_A|_{B+} - E_A|_{B-})$$

### ANOVA F-statistic
$$F = \frac{MS_{factor}}{MS_{error}}$$

### Signal-to-Noise Ratio (Taguchi)
$$S/N = -10 \log_{10}\left(\frac{1}{n}\sum_{i=1}^{n} \frac{1}{y_i^2}\right)$$

---

## Factorial Design Effect Estimation

For a 2^k design with coded levels (-1, +1):

**Coded regression model:**
$$y = \beta_0 + \sum_i \beta_i x_i + \sum_{i<j} \beta_{ij} x_i x_j + \cdots + \epsilon$$

**Coefficient estimation:**
$$\beta_j = \frac{1}{N} \sum_{i=1}^{N} c_{j,i} \cdot y_i$$

where $c_{j,i}$ is the contrast column for effect $j$.

**Uncoding to real units:**
$$x_i^* = \frac{x_i - x_{mid}}{x_{step}}, \quad x_{mid} = \frac{x_{high} + x_{low}}{2}$$

## Response Surface Methodology (RSM)

### Second-Order Model
$$y = \beta_0 + \sum_i \beta_i x_i + \sum_i \beta_{ii} x_i^2 + \sum_{i<j} \beta_{ij} x_i x_j + \epsilon$$

### Central Composite Design (CCD)
- **Factorial portion**: 2^k corner points
- **Axial (star) points**: 2k points at distance ±α from center
- **Center points**: n₀ replicates (estimate pure error and curvature)
- Total runs: 2^k + 2k + n₀
- α = 2^(k/4) for rotatability (e.g., α = 1.414 for k=2, α = 1.682 for k=3)

### Box-Behnken Design (BBD)
- Only edge midpoints of the cube (3 levels per factor: -1, 0, +1)
- No corner points → fewer extreme combinations
- Total runs: 2k(k-1) + n₀
- Efficient for 3–7 factors

### RSM Optimization
1. **Steepest ascent**: Follow gradient from factorial design toward optimum
2. **CCD/BBD**: Fit quadratic model near suspected optimum
3. **Canonical analysis**: Transform to stationary point (max, min, saddle)
4. **Ridge analysis**: Follow constrained optimum paths

## Taguchi Methods

### Philosophy
- Emphasize **robustness** (reduce variability) rather than just optimize mean
- Distinguish **control factors** (design parameters) from **noise factors** (uncontrollable)
- Use **orthogonal arrays** (L4, L8, L9, L12, L16, L18, L27, L32) to efficiently assign factors

### Signal-to-Noise Ratios
| Goal | S/N Type | Formula |
|------|----------|---------|
| Larger-the-better | $S/N_{LTB}$ | $-10\log_{10}\left(\frac{1}{n}\sum 1/y_i^2\right)$ |
| Smaller-the-better | $S/N_{STB}$ | $-10\log_{10}\left(\frac{1}{n}\sum y_i^2\right)$ |
| Nominal-the-best | $S/N_{NTB}$ | $10\log_{10}\left(\bar{y}^2/s^2\right)$ |

### Crossed Array Design
- **Inner array**: Control factor assignments (orthogonal array)
- **Outer array**: Noise factor combinations
- Each inner array run is tested across all outer array conditions
- Response = S/N ratio computed across noise conditions

### Common Orthogonal Arrays
| Array | Max factors | Runs | Levels |
|-------|------------|------|--------|
| L4 | 3 | 4 | 2 |
| L8 | 7 | 8 | 2 |
| L9 | 4 | 9 | 3 |
| L12 | 11 | 12 | 2 |
| L16 | 15 | 16 | 2 |
| L18 | 8 (1@2, 7@3) | 18 | mixed |
| L27 | 13 | 27 | 3 |

## Simplex Optimization

### Fixed-Size Simplex Algorithm
1. Start with k+1 vertices (k factors) forming a regular simplex
2. Evaluate response at all vertices
3. **Reflect** worst vertex through centroid of remaining vertices
4. If new vertex is best → **expand**; if worst → **contract**; otherwise accept
5. Repeat until convergence (responses stabilize or simplex oscillates)

### Modified Simplex (Nelder-Mead)
- Variable-size simplex: expands when going downhill, contracts when not
- Handles both minima and maxima
- Handles constraints via penalty functions

### Comparison: Simplex vs Factorial
| Feature | Simplex | Factorial |
|---------|---------|-----------|
| Path | Sequential (moves toward optimum) | All at once |
| Factor knowledge | Local (follows gradient) | Global (all interactions) |
| Missing optimum | Possible in ridges | Unlikely with enough runs |
| Run efficiency | Good for many factors | Better for few factors |
| Model building | No explicit model | Fits regression model |

## Mixture Designs

Used when factors are **proportions** that sum to 1 (e.g., solvent compositions).

### Simplex-Lattice Design
- {q, m} design: q components, m equally spaced levels
- Points at (a₁/m, a₂/m, ..., a_q/m) where Σaᵢ = m

### Simplex-Centroid Design
- All vertex (pure components): q points
- All binary centroids: C(q,2) points
- All ternary centroids: C(q,3) points
- ... up to overall centroid: 1 point
- Total: 2^q - 1 points

## Validation and Quality Metrics

### Model Adequacy
- **R²**: Proportion of variance explained (target > 0.90)
- **Adjusted R²**: Penalizes for number of terms
- **Predicted R²**: Cross-validated prediction ability
- **Lack of fit**: Compare model error to pure error from replicates

### Practical Guidelines
- Always include **center point replicates** (≥3) to estimate pure error
- **Randomize** run order to avoid systematic bias
- **Block** when uncontrollable factors change (different days, operators)
- Verify model predictions with **confirmation runs** before adoption

---

## Harvey Textbook Problem-Solving (ch14)

### Factorial Effects - CRITICAL INSTRUCTIONS

**When solving Harvey ch14 problems, ALWAYS use `calculate_effects(responses, factor_names=[...])` with the actual factor names from the problem statement.**

**DO NOT assume factors are A/B/C. Always read the problem to identify which factor corresponds to which column.**

#### Examples:

| Problem | Factor Names | Usage |
|---------|--------------|-------|
| ch14_005 | A, B, C (standard) | `factor_names=["A","B","C"]` |
| ch14_011 | X (temperature), Y (catalyst), Z (concentration) | `factor_names=["X","Y","Z"]` |
| ch14_012 | X (benzocaine), Y (lactose), Z (moisture) | `factor_names=["X","Y","Z"]` |

### Standard Order for 2³ Design (Yates Order)

| Run | Col 0 | Col 1 | Col 2 |
|-----|-------|-------|-------|
| 1 | - | - | - |
| 2 | + | - | - |
| 3 | - | + | - |
| 4 | + | + | - |
| 5 | - | - | + |
| 6 | + | - | + |
| 7 | - | + | + |
| 8 | + | + | + |

**Column 0 corresponds to the first factor listed in the problem.** For example:
- If factors are X, Y, Z: Col 0 = X, Col 1 = Y, Col 2 = Z
- If factors are A, B, C: Col 0 = A, Col 1 = B, Col 2 = C

### Effect Calculation Pattern

For a 2³ design, effects are calculated as:
- Main effects: Average of responses where factor is (+) minus average where factor is (-)
- Interaction effects: Product of corresponding columns

---

## L3 Tool Call Directive

**Always use L3 tools instead of manual calculation.** Call functions from `doe_tools.py`:

- **Factorial effects**: `calculate_effects(responses, factor_names=None)` — computes main effects and interactions for 2^k factorial designs. ALWAYS pass `factor_names` matching the problem's factor labels (e.g., `["X","Y","Z"]` or `["A","B","C"]`).
- **Full factorial design matrix**: `full_factorial_design(k)` — generates 2^k design in standard Yates order.
- **Coded regression**: `coded_regression(responses, factor_names=None)` — regression model from factorial design.
- **Box-Behnken design**: `box_behnken_design(k)` — generates Box-Behnken matrix.
- **CCD design**: `central_composite_design(k)` — generates central composite design.

**IMPORTANT**: Read the problem to identify factor names. DO NOT assume A/B/C. Map column 0 to the first factor mentioned, column 1 to the second, etc.

## L3 Implementations

Available in `L3_functions/doe_tools.py`:
- `full_factorial_design(k)` — Generate 2^k design matrix
- `fractional_factorial(k, p, generator)` — Generate 2^(k-p) design
- `calculate_effects(responses, factor_names=[...])` — Main and interaction effects (**use factor_names from problem!**)
- `anova_table(design, responses)` — ANOVA for factorial designs
- `ccd_design(k, alpha, center_reps)` — Central composite design
- `box_behnken_design(k, center_reps)` — Box-Behnken design
- `simplex_optimize(objective, x0, step)` — Simplex optimization
- `taguchi_sn(ratios, goal)` — Signal-to-noise calculation

## L4 Reference Data

- `L4_reference/doe_orthogonal_arrays.csv` — Standard Taguchi arrays
- `L4_reference/doe_generators.csv` — Fractional factorial generators

## L5 Examples

- `L5_examples/doe_examples.md` — Worked examples from Harvey Ch14

---

**Cross-links:**
- quality_assurance_control.md (G19)
- method_validation.md (G20)
- chemometrics_principal_component_analysis.md
- analytical_method_design.md
