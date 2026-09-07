---
id: chemometrics.probability_distributions
layer: 2
title: Probability Distributions in Chemistry
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch05-06
---

## Core Concepts

Probability distributions describe how individual measurements are distributed about a central value. Understanding the underlying distribution is crucial for selecting appropriate statistical methods.

## Types of Distributions

### 1. Normal (Gaussian) Distribution

**Mathematical Definition:**
```
P(x) = (1/√(2πσ²)) × e^[-(x-μ)²/(2σ²)]
```

**Parameters:**
- μ (mu): Population mean
- σ (sigma): Population standard deviation

**Properties:**
- Symmetrical around mean
- 68.26% of data within μ ± 1σ
- 95.45% of data within μ ± 2σ
- 99.73% of data within μ ± 3σ
- Area under curve = 1 (normalized)

**When to expect:**
- Replicate measurements of same sample
- Measurement errors (random)
- Natural phenomena (heights, concentrations)

**Z-score:**
```
z = (x - μ) / σ
```
Converts any normal distribution to standard normal (μ=0, σ=1)

### 2. Binomial Distribution

**Definition:** Probability of k successes in n independent trials.

```
P(k) = (n choose k) × p^k × (1-p)^(n-k)
```

**Parameters:**
- n: Number of trials
- p: Probability of success per trial
- k: Number of successes

**Applications in Chemistry:**
- Counting particles or defects
- Binary outcomes (pass/fail tests)
- Radioactive decay events
- Quality control sampling

**Mean and Variance:**
- Mean: μ = np
- Variance: σ² = np(1-p)

### 3. Poisson Distribution

**Definition:** Probability of k events in a fixed interval.

```
P(k) = (λ^k × e^(-λ)) / k!
```

**Parameter:**
- λ (lambda): Expected number of events

**Applications:**
- Counting rare events
- Photon counting in spectroscopy
- Defects per unit area
- Contamination particles

**Properties:**
- Mean = Variance = λ
- Approaches normal for large λ

### 4. Uniform Distribution

**Definition:** Equal probability across range [a, b].

```
P(x) = 1/(b-a) for a ≤ x ≤ b
```

**Applications:**
- Random number generation
- Sampling from discrete populations
- Dilution series design

## Central Limit Theorem

**Statement:** The distribution of sample means approaches normal as sample size increases, regardless of the population distribution.

**Implications:**
- Sample means are normally distributed even if individual measurements are not
- Foundation for inferential statistics
- Enables use of z-scores and t-tests

**Rule of thumb:**
- n ≥ 30 for most distributions
- n ≥ 15 for moderately skewed distributions
- n ≥ 5 for symmetric distributions

## Confidence Intervals from Normal Distribution

For normally distributed data, confidence interval for mean:

```
CI = Ȳ ± t(α/2, n-1) × (s/√n)
```

Or using z-score for large n:

```
CI = Ȳ ± z(α/2) × (σ/√n)
```

**Common z-values:**
- 90% CI: z = 1.645
- 95% CI: z = 1.96
- 99% CI: z = 2.576

## Probability Calculations

### Example: Finding Probability Above a Value

Given: μ = 5.5833 ppb Pb, σ = 0.0558 ppb Pb

Question: What is P(X > 5.650 ppb)?

```
z = (5.650 - 5.5833) / 0.0558 = 1.195
P(z > 1.195) ≈ 0.116 (11.6%)
```

### Example: Finding Probability Within Range

Question: What is P(5.580 < X < 5.625)?

```
z_upper = (5.625 - 5.5833) / 0.0558 = 0.747
z_lower = (5.580 - 5.5833) / 0.0558 = -0.059

P(z > 0.747) = 0.2275
P(z < -0.059) = 0.4765

P(-0.059 < z < 0.747) = 1 - 0.2275 - 0.4765 = 0.296 (29.6%)
```

## R Implementation

```r
# Normal distribution
pnorm(x, mean, sd)           # P(X < x)
qnorm(p, mean, sd)           # x for given probability
dnorm(x, mean, sd)           # probability density
rnorm(n, mean, sd)           # random samples

# Binomial distribution
dbinom(k, n, p)              # P(X = k)
pbinom(k, n, p)              # P(X ≤ k)

# Poisson distribution
dpois(k, lambda)             # P(X = k)
ppois(k, lambda)             # P(X ≤ k)

# Calculate z-score
z_score = (x - mean(data)) / sd(data)

# Probability from z-score
pnorm(z_score, lower.tail = FALSE)  # upper tail
```

## Assessing Normality

### Visual Methods
- Histogram: Should be symmetric bell-shape
- Q-Q plot: Points should follow diagonal line
- Boxplot: Symmetric with whiskers of similar length

### Statistical Tests
- Shapiro-Wilk test: `shapiro.test(data)`
- Kolmogorov-Smirnov test: `ks.test(data, "pnorm", mean, sd)`

## Applications in Chemistry

### Analytical Chemistry
- Uncertainty in measurements
- Method validation statistics
- Detection limit calculations
- Calibration curve uncertainty

### Spectroscopy
- Signal noise distribution
- Baseline fluctuations
- Photon counting statistics

### Quality Assurance
- Control chart limits
- Acceptance sampling
- Specification limits

## Key Concepts Summary

| Distribution | Parameters | Mean | Variance | Use Case |
|--------------|------------|------|----------|----------|
| Normal | μ, σ | μ | σ² | Measurement errors |
| Binomial | n, p | np | np(1-p) | Pass/fail tests |
| Poisson | λ | λ | λ | Rare events |
| Uniform | a, b | (a+b)/2 | (b-a)²/12 | Random sampling |

## Connection to Other Topics

- **Descriptive Statistics** (L2_descriptive_statistics.md): Mean and variance define distributions
- **Significance Testing** (L2_significance_testing.md): Based on normal distribution
- **Uncertainty Analysis** (L2_uncertainty_analysis.md): Confidence intervals from distributions
- **PCA** (L2_principal_component_analysis.md): Assumes normally distributed data

## See Also

- Harvey, Chemometrics Using R, Chapter 5-6
- L3_code_examples/distribution_analysis_in_R.R
