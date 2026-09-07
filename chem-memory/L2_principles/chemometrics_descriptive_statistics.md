---
id: chemometrics.descriptive_statistics
layer: 2
title: Descriptive Statistics for Chemistry
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch04
---

## Core Concepts

Descriptive statistics summarize and describe the properties of a dataset quantitatively, providing measures of central tendency and spread.

### Measures of Central Tendency

**Mean (Ȳ):** The numerical average of all observations.
```
Ȳ = Σ(Yi) / n
```
- Sensitive to outliers
- Appropriate for normally distributed data

**Median (Ỹ):** The middle value when data is sorted.
- For odd n: Ỹ = Y((n+1)/2)
- For even n: Ỹ = [Y(n/2) + Y(n/2+1)] / 2
- Robust to outliers
- Better for skewed distributions

### Measures of Spread (Variation)

**Variance (s²):** Average squared deviation from mean.
```
s² = Σ(Yi - Ȳ)² / (n - 1)
```

**Standard Deviation (s):** Square root of variance.
```
s = √[Σ(Yi - Ȳ)² / (n - 1)]
```
- Same units as mean
- Most common measure of spread

**Range (w):** Difference between maximum and minimum.
```
w = Ymax - Ymin
```
- Simple but sensitive to outliers

**Interquartile Range (IQR):** Range of middle 50% of data.
```
IQR = FU - FL
```
- FU: Upper quartile (75th percentile)
- FL: Lower quartile (25th percentile)
- Robust to outliers

**Median Absolute Deviation (MAD):** Median of absolute deviations from median.
```
MAD = median(|Yi - Ỹ|)
```
- Most robust measure of spread

## Robust vs. Non-Robust Statistics

### Non-Robust Statistics (Sensitive to Outliers)
- Mean
- Variance
- Standard deviation
- Range

### Robust Statistics (Resistant to Outliers)
- Median
- IQR
- MAD

**When to use robust statistics:**
- Data with suspected outliers
- Skewed distributions
- Exploratory data analysis
- When outlier detection is important

**When to use non-robust statistics:**
- Normally distributed data
- No outliers suspected
- When all data points are valid
- For inferential statistics (t-tests, etc.)

## Applications in Chemistry

### Analytical Method Validation
- Report mean ± standard deviation for replicate measurements
- Use IQR to identify outliers in method development
- Compare robust and non-robust measures to detect problems

### Quality Control
- Track mean and standard deviation over time (control charts)
- Use median and MAD for robust process monitoring
- IQR-based outlier detection for specification limits

### Sample Characterization
- Summarize composition data (e.g., M&M weights, penny masses)
- Compare sample batches using descriptive statistics
- Identify systematic errors from distribution shape

## R Implementation

```r
# Central tendency
mean(data)
median(data)

# Spread
var(data)           # variance
sd(data)            # standard deviation
range(data)         # min and max
IQR(data)           # interquartile range
mad(data)           # median absolute deviation

# Robust summary
summary(data)       # five-number summary + mean
```

## Key Formulas Summary

| Statistic | Formula | Robust? |
|-----------|---------|---------|
| Mean | Ȳ = Σ(Yi)/n | No |
| Median | Middle value | Yes |
| Variance | s² = Σ(Yi-Ȳ)²/(n-1) | No |
| Std Dev | s = √(s²) | No |
| Range | Ymax - Ymin | No |
| IQR | FU - FL | Yes |
| MAD | median(\|Yi-Ỹ\|) | Yes |

## L3 Tool Call Directive

**Always use L3 tools instead of manual calculation.** Call functions from `chemometrics_tools.py`:

- **Mean, median, range, std, variance**: `descriptive_stats(data)` — returns dict with mean, median, std, var, range. Uses sample standard deviation (ddof=1).
- **Confidence interval**: `confidence_interval(data, confidence=0.95)` — returns dict with mean, std, ci_lower, ci_upper, t_value.

## Connection to Other Topics

- **Normal Distribution** (L2_probability_distributions.md): Mean and standard deviation define normal distribution
- **Significance Testing** (L2_significance_testing.md): Use mean and standard deviation for t-tests
- **Cluster Analysis** (L2_cluster_analysis.md): Distance measures based on mean and variance
- **PCA** (L2_principal_component_analysis.md): Based on variance decomposition

## See Also

- Harvey, Chemometrics Using R, Chapter 4
- L3_code_examples/descriptive_statistics_in_R.R
