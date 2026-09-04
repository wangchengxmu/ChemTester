---
id: chemometrics.significance_testing
layer: 2
title: Significance Testing in Chemistry
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch07
---

## Core Concepts

Significance testing (hypothesis testing) determines whether differences between results are statistically significant or due to random error.

## The Significance Testing Process

### Four-Step Framework

1. **State hypotheses:**
   - Null hypothesis (H0): No significant difference
   - Alternative hypothesis (HA): Significant difference exists

2. **Choose confidence level:**
   - Common: 95% (α = 0.05)
   - α = 1 - (confidence% / 100)

3. **Calculate test statistic:**
   - Compare to critical value
   - Determine p-value

4. **Make decision:**
   - Reject H0 or fail to reject H0
   - Accept HA if H0 rejected

## Types of Hypothesis Tests

### One-Tailed vs. Two-Tailed Tests

**Two-tailed test:** Tests for difference in either direction
```
H0: X̄ = μ
HA: X̄ ≠ μ
```
- More conservative
- Used when direction not specified
- Rejection regions at both tails

**One-tailed test:** Tests for difference in specific direction
```
H0: X̄ = μ
HA: X̄ > μ  (or HA: X̄ < μ)
```
- More powerful for detecting directional effects
- Used when direction matters
- Single rejection region

## Common Statistical Tests

### 1. t-Tests

#### One-Sample t-Test
Compare sample mean to known value.

```
t = (X̄ - μ) / (s / √n)
```

Degrees of freedom: df = n - 1

**Example:** Is measured concentration different from certified value?

#### Two-Sample t-Test
Compare two sample means.

```
t = (X̄1 - X̄2) / √(s1²/n1 + s2²/n2)
```

**Assumptions:**
- Normally distributed populations
- Independent samples
- Equal variances (use pooled variance if true)

**Example:** Compare two analytical methods.

#### Paired t-Test
Compare paired measurements.

```
t = D̄ / (sD / √n)
```

where D̄ is mean difference between pairs.

**Example:** Before/after measurements on same samples.

### 2. F-Test

Compare two variances.

```
F = s1² / s2²  (larger variance as numerator)
```

**Applications:**
- Test equal variance assumption for t-test
- Compare method precision
- ANOVA calculations

### 3. Chi-Square Test

Compare observed vs. expected frequencies.

```
χ² = Σ(Oi - Ei)² / Ei
```

**Applications:**
- Goodness of fit tests
- Test for normality
- Contingency tables

## Understanding Errors

### Type I Error (False Positive)
- Rejecting H0 when it's true
- Probability = α
- Example: Concluding methods differ when they don't

### Type II Error (False Negative)
- Failing to reject H0 when it's false
- Probability = β
- Example: Failing to detect real difference

### Power of Test
```
Power = 1 - β
```

**Factors affecting power:**
- Sample size (larger n → higher power)
- Effect size (larger difference → higher power)
- Variability (lower s → higher power)
- Significance level (higher α → higher power)

**Trade-off:** Decreasing α increases β.

## P-Values

**Definition:** Probability of observing result as extreme or more extreme, assuming H0 is true.

**Interpretation:**
- p < 0.05: Statistically significant at 95% confidence
- p < 0.01: Highly significant
- p < 0.001: Very highly significant

**Important:** Small p-value does not mean large effect size!

## Confidence Intervals and Significance

A 95% confidence interval that does not contain the null hypothesis value is equivalent to rejecting H0 at α = 0.05.

**Example:**
- 95% CI for difference: (2.1, 5.3)
- H0: difference = 0
- Since 0 is not in CI, reject H0

## Applications in Chemistry

### Method Validation
- Compare new method to reference method
- Test for bias (systematic error)
- Evaluate method precision

### Quality Control
- Compare to specification limits
- Detect process shifts
- Validate calibration curves

### Experimental Comparisons
- Compare treatments or conditions
- Evaluate sample differences
- Test for contamination

## R Implementation

```r
# One-sample t-test
t.test(data, mu = known_value)

# Two-sample t-test
t.test(data1, data2)
t.test(data1, data2, var.equal = TRUE)  # pooled

# Paired t-test
t.test(before, after, paired = TRUE)

# F-test for equal variances
var.test(data1, data2)

# Shapiro-Wilk normality test
shapiro.test(data)

# Chi-square test
chisq.test(observed, p = expected)

# Get p-value from t-statistic
pt(t_value, df, lower.tail = FALSE)
```

## Interpreting Results

### When to Reject H0

1. p-value < α
2. Test statistic > critical value
3. Confidence interval excludes null value

### Important Caveats

1. **Statistical significance ≠ practical significance**
   - Large samples can detect tiny differences
   - Consider effect size and practical relevance

2. **p-value is not probability H0 is true**
   - It's probability of data given H0

3. **Multiple testing problem**
   - More tests → more Type I errors
   - Use correction (Bonferroni, FDR)

4. **Assumptions matter**
   - Normality
   - Independence
   - Equal variances (for some tests)

## Common Pitfalls

1. **p-hacking:** Running many tests until finding significant result
2. **HARKing:** Hypothesizing After Results Known
3. **Ignoring effect size:** Small p with tiny effect
4. **Violating assumptions:** Non-normal data, unequal variances
5. **Multiple comparisons:** Not correcting for multiple tests

## Key Formulas Summary

| Test | Statistic | df | Use Case |
|------|-----------|----|----|
| One-sample t | t = (X̄-μ)/(s/√n) | n-1 | Compare to known value |
| Two-sample t | t = (X̄1-X̄2)/SE | n1+n2-2 | Compare two groups |
| Paired t | t = D̄/(sD/√n) | n-1 | Paired measurements |
| F-test | F = s1²/s2² | n1-1, n2-1 | Compare variances |

## L3 Tool Call Directive

**Always use L3 tools instead of manual calculation.** Call functions from `chemometrics_tools.py`:

- **One-sample t-test**: `t_test(data, true_value, alpha=0.05)` — returns dict with mean, std, n, df, t_calc, t_critical, p_value.
- **Two-sample t-test**: `two_sample_t_test(sample1, sample2, alpha=0.05)` — returns dict with means, stds, F_calc, t_calc, t_critical, p_value, df.
- **One-way ANOVA**: `one_way_anova(group_data)` where group_data is a dict like `{"A": [1.6,2.9,...], "B": [4.6,...]}` — returns SS_between, SS_within, MS_between, MS_within, F, F_critical, p_value.
- **Error propagation**: `propagation_uncertainty(result_value, operations, uncertainties)` for simple formulas, or `propagation_uncertainty_expression(result_value, partial_derivatives, uncertainties)` for complex expressions.

## Connection to Other Topics

- **Normal Distribution** (L2_probability_distributions.md): Basis for t-tests
- **Calibration** (L2_calibration_regression.md): Test for linearity, slope significance
- **ANOVA** (L2_anova_experimental_design.md): Extension of t-tests for multiple groups
- **PCA** (L2_principal_component_analysis.md): Test significance of components

## See Also

- Harvey, Chemometrics Using R, Chapter 7
- Nuzzo, R. "Scientific Method: Statistical Errors," Nature, 2014, 506, 150-152
- L3_code_examples/significance_tests_in_R.R
