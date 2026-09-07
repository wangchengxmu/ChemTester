---
id: statistical.analysis.chemistry
layer: 2
title: Statistical Analysis in Analytical Chemistry
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/chemometrics_tools.py
  - ../L4_reference/chemometrics_data.csv
cross_links:
  - ./quantitative_measurement_and_uncertainty.md
  - ./analytical_method_design.md
source: Analytical Chemistry 2.1 (Harvey), Ch04
---

## Context
Statistical analysis is essential for evaluating analytical data, assessing uncertainty, and making valid conclusions. This topic covers the statistical tools used in analytical chemistry to characterize data, compare results, and estimate confidence.

## Descriptive Statistics

### Measures of Central Tendency
| Measure | Formula | Use |
|---------|---------|-----|
| Mean (x̄) | Σxᵢ/n | Average value |
| Median | Middle value | Robust to outliers |
| Mode | Most frequent | For discrete data |

### Measures of Dispersion
| Measure | Formula | Use |
|---------|---------|-----|
| Range | max - min | Simple spread |
| Standard deviation (s) | √[Σ(xᵢ-x̄)²/(n-1)] | Sample variability |
| Variance (s²) | s² | Square of std dev |
| Relative std dev (RSD) | (s/x̄) × 100% | Normalized precision |
| Coefficient of variation (CV) | Same as RSD | Alternative name |

### Standard Deviation Calculations
```
Sample standard deviation:
s = √[Σ(xᵢ - x̄)² / (n-1)]

Population standard deviation:
σ = √[Σ(xᵢ - μ)² / N]
```

## Distribution of Data

### Normal Distribution
```
Frequency
  │       ___
  │      /   \
  │     /     \
  │    /       \
  │___/         \___
  └─────────────────→ Value
    μ-3σ μ-σ μ μ+σ μ+3σ
```

- **68.3%** of data within ±1σ
- **95.5%** of data within ±2σ
- **99.7%** of data within ±3σ

### Standard Normal Distribution (z-score)
```
z = (x - μ) / σ
```

### Testing for Normality
- **Normal probability plot**: Data vs. z-scores
- **Shapiro-Wilk test**: Formal hypothesis test
- **Histogram**: Visual check for bell curve

## Confidence Intervals

### Confidence Interval for Mean
```
CI = x̄ ± t × (s/√n)
```

Where:
- t = t-value from t-distribution (depends on df and confidence level)
- s = sample standard deviation
- n = number of measurements

### t-Values for Common Confidence Levels
| df | 90% | 95% | 99% |
|----|-----|-----|-----|
| 1 | 6.31 | 12.71 | 63.66 |
| 2 | 2.92 | 4.30 | 9.92 |
| 5 | 2.02 | 2.57 | 4.03 |
| 10 | 1.81 | 2.23 | 3.17 |
| 20 | 1.72 | 2.09 | 2.85 |
| ∞ | 1.64 | 1.96 | 2.58 |

## Hypothesis Testing

### Steps in Hypothesis Testing
1. State null hypothesis (H₀) and alternative (Hₐ)
2. Choose significance level (α, typically 0.05)
3. Calculate test statistic
4. Compare to critical value or calculate p-value
5. Accept or reject H₀

### t-Tests

**One-sample t-test** (compare mean to known value):
```
t = (x̄ - μ) / (s/√n)
```

**Two-sample t-test** (compare two means):
```
t = (x̄₁ - x̄₂) / s_pooled × √(1/n₁ + 1/n₂)
```

Where s_pooled = √[(s₁²(n₁-1) + s₂²(n₂-1)) / (n₁+n₂-2)]

### F-Test (compare variances)
```
F = s₁² / s₂²  (larger variance in numerator)
```

### Chi-Square Test (goodness of fit)
```
χ² = Σ(Oᵢ - Eᵢ)² / Eᵢ
```

## Outlier Detection

### Q-Test
```
Q = |suspect - nearest| / range
```

Compare Q to Q_critical (depends on n and confidence level)

### Grubbs' Test
```
G = |suspect - x̄| / s
```

Compare G to G_critical

### Dixon's Q-Test Critical Values
| n | Q_critical (95%) |
|---|------------------|
| 3 | 0.970 |
| 4 | 0.829 |
| 5 | 0.710 |
| 6 | 0.625 |
| 7 | 0.570 |
| 8 | 0.526 |
| 9 | 0.493 |
| 10 | 0.466 |

## Analysis of Variance (ANOVA)

### One-Way ANOVA
Used to compare means of three or more groups.

```
F = MS_between / MS_within

Where:
MS_between = SS_between / df_between
MS_within = SS_within / df_within
```

### ANOVA Table
| Source | SS | df | MS | F |
|--------|-----|----|----|---|
| Between | SS_b | k-1 | MS_b | F |
| Within | SS_w | N-k | MS_w | |
| Total | SS_t | N-1 | | |

## Regression Analysis

### Linear Regression (Least Squares)
```
y = mx + b

Where:
m (slope) = [nΣxy - ΣxΣy] / [nΣx² - (Σx)²]
b (intercept) = [Σy - mΣx] / n
```

### Correlation Coefficient
```
r = [nΣxy - ΣxΣy] / √[(nΣx² - (Σx)²)(nΣy² - (Σy)²)]
```

- r = +1: perfect positive correlation
- r = -1: perfect negative correlation
- r = 0: no linear correlation

### Standard Error of Estimate
```
s_y/x = √[Σ(yᵢ - ŷᵢ)² / (n-2)]
```

### Calibration Uncertainty
For unknown concentration determined from calibration curve:
```
s_x = (s_y/x / m) × √[(1/m) + (1/n) + (ȳ_unk - ȳ)² / (m × s_x²)]
```

## Detection Limit Statistics

### IUPAC Definition
- **LOD**: Concentration giving signal = blank mean + 3σ_blank
- **LOQ**: Concentration giving signal = blank mean + 10σ_blank

### Hubaux-Vos Method
Uses calibration statistics:
```
LOD = 3.3 × s_y/x / m
LOQ = 10 × s_y/x / m
```

## Decision Flow
1. Collect data, check for outliers
2. Calculate descriptive statistics
3. Test for normality
4. Calculate confidence intervals
5. Apply hypothesis tests as needed
6. Report results with uncertainty

## Implementations and Data
- Statistical analysis tools: [L3 code](../L3_functions/chemometrics_tools.py)
- Statistical tables: [L4 reference](../L4_reference/chemometrics_data.csv)
