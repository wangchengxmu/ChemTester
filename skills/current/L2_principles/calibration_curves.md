---
id: chemometrics.calibration_curves
layer: 2
title: Calibration Curves and Linear Regression
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/calibration_regression.R
cross_links:
  - ./multivariate_regression.md
  - ./analytical_method_design.md
  - ./uv_vis_spectroscopy.md
source: Chemometrics Using R (Harvey), Ch8.1, Ch8.5
---

## Context
Calibration curves establish the relationship between an instrument's response (signal) and analyte concentration. Linear regression analysis determines the best-fit line through calibration data, providing the mathematical model needed to convert measured signals into concentrations for unknown samples.

## Core Principle

### Calibration Equation
The fundamental relationship for a calibration curve:

```
S = k_A × C_A + S_blank
```

Where:
- **S** = measured signal
- **C_A** = analyte concentration
- **k_A** = sensitivity (slope)
- **S_blank** = blank signal (intercept)

### Linear Model
In standard regression notation:

```
y = β_0 + β_1 x
```

Where:
- **y** = signal (dependent variable)
- **x** = concentration (independent variable)
- **β_0** = y-intercept
- **β_1** = slope

### Assumptions of Linear Regression
1. **Errors in y only**: Indeterminate errors affect signal, not concentration
2. **Normal distribution**: Errors are normally distributed
3. **Independence**: Errors are independent of concentration
4. **Homoscedasticity**: Constant variance across concentration range

## Method of Least Squares

### Objective
Find b₀ and b₁ that minimize the sum of squared residuals:

```
Minimize: R = Σ(y_i - ŷ_i)²
          i=1 to n
```

Where:
- **y_i** = measured signal for standard i
- **ŷ_i** = predicted signal = b₀ + b₁x_i
- **r_i** = residual = y_i - ŷ_i

### Calculating Slope and Intercept

#### Slope (b₁)
```
b₁ = [n Σx_i y_i - (Σx_i)(Σy_i)]
    ─────────────────────────────
    [n Σx_i² - (Σx_i)²]
```

#### Intercept (b₀)
```
b₀ = [Σy_i - b₁ Σx_i]
    ─────────────────
           n
```

### Example Calculation

**Calibration Data**:
| Conc (x) | Signal (y) | x×y | x² |
|----------|-----------|-----|-----|
| 0.000 | 0.00 | 0.000 | 0.000 |
| 0.100 | 12.36 | 1.236 | 0.010 |
| 0.200 | 24.83 | 4.966 | 0.040 |
| 0.300 | 35.91 | 10.773 | 0.090 |
| 0.400 | 48.79 | 19.516 | 0.160 |
| 0.500 | 60.42 | 30.210 | 0.250 |

**Sums**:
- Σx_i = 1.500
- Σy_i = 182.31
- Σx_i y_i = 66.701
- Σx_i² = 0.550

**Calculate**:
```
b₁ = [6 × 66.701 - 1.500 × 182.31] / [6 × 0.550 - (1.500)²]
   = 120.706

b₀ = [182.31 - 120.706 × 1.500] / 6
   = 0.209
```

**Calibration equation**: `S = 120.71 × C_A + 0.21`

## Uncertainty in Regression

### Standard Deviation About Regression
Measures scatter of points around the line:

```
s_r = √[Σ(y_i - ŷ_i)² / (n - 2)]
```

**Interpretation**: Average deviation of points from regression line

### Standard Deviations of Parameters

#### Slope uncertainty
```
s_b₁ = √[n × s_r²] / [n Σx_i² - (Σx_i)²]
     = √[s_r² / Σ(x_i - x̄)²]
```

#### Intercept uncertainty
```
s_b₀ = √[s_r² Σx_i²] / [n Σx_i² - (Σx_i)²]
```

### Confidence Intervals

#### For parameters
```
β₁ = b₁ ± t × s_b₁
β₀ = b₀ ± t × s_b₀
```

Where t is from t-distribution with (n-2) degrees of freedom

**Example** (95% CI, 4 df, t = 2.78):
```
β₁ = 120.7 ± 2.78 × 0.965 = 120.7 ± 2.7
β₀ = 0.21 ± 2.78 × 0.292 = 0.2 ± 0.8
```

#### For predicted concentration
When analyzing an unknown sample:

```
C_A = (S_samp - b₀) / b₁
```

**Standard deviation**:
```
s_CA = (s_r / b₁) × √[(1/m) + (1/n) + (S̄_samp - S̄_std)² / (b₁² Σ(x_i - x̄)²)]
```

Where:
- **m** = number of replicate measurements of sample
- **n** = number of calibration standards
- **S̄_samp** = average signal for sample
- **S̄_std** = average signal for standards

**Confidence interval**:
```
μ_CA = C_A ± t × s_CA
```

## Residual Analysis

### Purpose
Validate regression assumptions by examining residuals

### Residual Plots
```
Residual (y_i - ŷ_i)
  │
  │    ●     ●
  │  ●   ● ●   ●   Random scatter → Good ✓
  │●       ●     ●
  │  ●   ●     ●
  └─────────────────────→ Concentration
```

### Interpretation Patterns

| Pattern | Indicates | Action |
|---------|-----------|--------|
| Random scatter | Good fit, assumptions met | Accept model |
| Funnel shape | Variance increases with concentration | Use weighted regression |
| Curved pattern | Non-linear relationship | Use polynomial or non-linear |
| Outliers | Bad measurement or unusual sample | Investigate, possibly remove |

### Example: Good Residual Plot
```
Residual
  │
  │      ●     ●
  │  ●       ●
  │●     ●     ●     ← Random, no trend
  │  ●     ●
  │    ●     ●
  └─────────────────→ Conc
  -0.2             +0.2
```

### Example: Problematic Residual Plot
```
Residual
  │            ●    ●
  │         ●       ●   ← Funnel shape: variance increases
  │      ●   ●           with concentration
  │   ●   ●
  │ ●  ●
  └─────────────────→ Conc
```

## R Implementation

### Basic Linear Regression
```r
# Create data
concentration <- c(0.000, 0.100, 0.200, 0.300, 0.400, 0.500)
signal <- c(0.00, 12.36, 24.83, 35.91, 48.79, 60.42)

# Fit linear model
model <- lm(signal ~ concentration)

# View summary
summary(model)

# Extract parameters
b0 <- coef(model)[1]  # intercept
b1 <- coef(model)[2]  # slope
```

### Regression Statistics
```r
# Standard errors
summary(model)$coefficients[, "Std. Error"]

# R-squared
summary(model)$r.squared

# Residual standard error
summary(model)$sigma
```

### Prediction
```r
# Predict concentration for unknown sample
S_samp <- 29.33
C_A <- (S_samp - b0) / b1
# Result: 0.241

# Confidence interval for prediction
# (requires more advanced calculations)
predict(model, newdata = data.frame(concentration = C_A),
        interval = "confidence")
```

### Residual Analysis
```r
# Get residuals
residuals <- resid(model)

# Residual plot
plot(concentration, residuals,
     xlab = "Concentration", ylab = "Residual",
     main = "Residual Plot")
abline(h = 0, col = "red")

# Standardized residuals
std_resid <- residuals / summary(model)$sigma

# Normal Q-Q plot
qqnorm(std_resid)
qqline(std_resid)
```

### Plotting Calibration Curve
```r
# Plot data and regression line
plot(concentration, signal,
     xlab = "Concentration (M)",
     ylab = "Signal",
     main = "Calibration Curve",
     pch = 19, col = "blue")

# Add regression line
abline(model, col = "red")

# Add confidence interval (advanced)
# See example in Harvey text for detailed code
```

## Weighted Regression

### When to Use
**Problem**: Heteroscedasticity (variance changes with concentration)
- Common in analytical chemistry
- Higher concentrations often have larger absolute variance

### Method
Weight each point by inverse variance:

```
w_i = 1 / s_i²
```

Where s_i² is the variance at concentration i

### R Implementation
```r
# Weights based on inverse variance
weights <- 1 / variance_at_each_concentration

# Weighted regression
model_wt <- lm(signal ~ concentration, weights = weights)
```

## Evaluating Calibration Quality

### Key Metrics

| Metric | Calculation | Good Value |
|--------|-------------|------------|
| R² (R-squared) | 1 - (SS_res/SS_tot) | >0.99 |
| RSD (relative std dev) | s_r / S̄ × 100% | <5% |
| LOD (limit of detection) | 3 × s_blank / b₁ | Application-dependent |
| LOQ (limit of quantitation) | 10 × s_blank / b₁ | Application-dependent |
| Residuals | Should be random | No pattern |

### Correlation Coefficient vs. R²
```
R² = (correlation coefficient)²

Example:
r = 0.999 → R² = 0.998
```

**Note**: R² alone is insufficient! Always examine residuals.

## Calibration Strategies

### External Standards
**Most common**:
- Prepare separate standards
- Measure signals
- Create calibration curve
- Apply to unknowns

**When to use**: Simple matrices, no interferences

### Standard Additions
**For matrix effects**:
- Spike sample with known additions
- Plot signal vs. addition
- Extrapolate to find original concentration

**When to use**: Complex matrix, unknown interferences

#### Standard Addition Methods for Dilution Correction

When adding spike volumes to a sample, the total volume changes. Two methods handle this:

**Method 1 - Simple (no dilution correction)**
- Plot: Signal (S) vs Spike Volume (V_spike)
- Use when: V_spike << V_sample (spike volume < 1% of sample volume)
- x-intercept: `x₀ = -C_sample × V_sample / C_spike`
- Sample concentration: `C_sample = |x₀| × C_spike / V_sample`

**Method 2 - Dilution-Corrected (Harvey recommended for significant spikes)**
- Plot: S × (V_sample + V_spike) vs V_spike
- Use when: V_spike is significant (>1% of sample volume)
- The transformation accounts for dilution of the original analyte
- Same formulas for x-intercept and C_sample as Method 1

**Derivation**:
```
Signal = k × C_total = k × (C_sample × V_sample + C_spike × V_spike) / V_total

Where V_total = V_sample + V_spike

S × V_total = k × (C_sample × V_sample + C_spike × V_spike)

Plot S × V_total vs V_spike:
  slope = k × C_spike
  intercept = k × C_sample × V_sample
  
At S × V_total = 0:
  V_spike = -C_sample × V_sample / C_spike = x-intercept
```

**Example** (Harvey Ch5.008):
- 5.00 mL sample, 600 ppb spike standard
- V_spike: 0, 0.10, 0.20, 0.30 mL
- Signals: 15.0, 45.0, 75.0, 105.0

Simple method:
```
Slope = 300 ppb/mL, intercept = 15.0
x-intercept = -15/300 = -0.050 mL
C_sample = 0.050 × 600 / 5.0 = 6.0 ppb
```

Dilution-corrected method:
```
Transform: S×V_total = 75, 229.5, 390, 556.5 (for V_spike = 0, 0.10, 0.20, 0.30)
Slope = 1605 mL·ppb/mL, intercept = 72
x-intercept = -72/1605 = -0.0449 mL
C_sample = 0.0449 × 600 / 5.0 = 5.4 ppb
```

**Note**: The dilution-corrected method gives a lower concentration (5.4 ppb vs 6.0 ppb) because it accounts for the dilution of the original analyte when spike volumes are added. For this example where spike volumes are 2-6% of sample volume, the difference is ~10%.

### Single-Point Standard Addition
For problems with exactly 1 sample measurement and 1 spiked measurement (no multi-point calibration needed):

**Formula**:
```
C_sample = (S_sample × C_spike × V_spike) / (S_spiked × V_total − S_sample × V_sample)
```

Where:
- **V_total** = final volume of the spiked flask (e.g. if 50 mL sample + 1 mL spike diluted to 50 mL, V_total = 50; if just mixed, V_total = 51)
- **V_sample** = volume of sample aliquot in the measurement flask
- **V_spike** = volume of standard added
- **C_spike** = concentration of the standard solution (use EXACTLY what the problem states — M, ppm, ppb, etc.)

**Critical solver notes**:
1. Always read the standard concentration from the problem text carefully — it may be given as molarity (e.g. 1.0 × 10⁻⁴ M), ppm, or other units
2. Account for ALL dilution steps if an aliquot is taken from a larger preparation flask
3. Determine V_total from the problem: "diluted to X mL" → V_total = X; "added to" with no further dilution → V_total = V_sample + V_spike
4. If the problem asks for weight percent or other derived quantity, convert from the original solution concentration after finding C_sample

**Important for weight percent / mass fraction conversions:**
- After finding C_sample (in ppm or mg/L), convert to mass: mass_analyte = C_sample × V_total_flask
- weight_percent = (mass_analyte / mass_sample) × 100%
- Make sure V_total_flask is the ORIGINAL preparation flask volume, not the measurement flask
- Units must be consistent: if C is in ppm (mg/L), then mass = C × V(L) gives mg

**Example** (Harvey Ch5.003):
- 50.0 mL sample: signal = 11.5
- 50.0 mL sample + 1.00 mL of 10.0 ppm standard: signal = 23.1
- V_total = 51.0 mL (no further dilution stated)
- C_sample = (11.5 × 10.0 × 1.0) / (23.1 × 51.0 − 11.5 × 50.0) = 115 / 603.1 ≈ 0.191 ppm

### Internal Standards
**For instrument variation**:
- Add reference compound to all samples
- Use ratio of signals
- Corrects for instrument drift

**When to use**: Sample preparation variability, injection volume uncertainty

## Limit of Detection and Quantitation

### Definitions

**Limit of Detection (LOD)**:
```
LOD = 3 × s_blank / b₁
```
Lowest concentration that can be detected (but not quantified accurately)

**Limit of Quantitation (LOQ)**:
```
LOQ = 10 × s_blank / b₁
```
Lowest concentration that can be quantified with acceptable precision

### Practical Determination
**Method 1**: From blank measurements
```r
s_blank <- sd(blank_measurements)
LOD <- 3 * s_blank / b1
LOQ <- 10 * s_blank / b1
```

**Method 2**: From calibration curve
```r
s_r <- summary(model)$sigma
LOD <- 3.3 * s_r / b1
LOQ <- 10 * s_r / b1
```

## Practical Guidelines

### Number of Standards
**Minimum**: 5-6 standards
**Recommended**: 8-10 standards
**Include**: Blank (zero concentration)

### Concentration Range
- Cover expected sample range
- Include samples at extremes
- Working range: where response is linear
- Don't extrapolate beyond calibration range!

### Replicates
**Standards**: Measure each standard once (or duplicate)
**Samples**: Measure 2-3 replicates
**Why**: Improve precision, detect outliers

### Quality Control
- Include QC samples at low, medium, high concentrations
- Monitor over time
- Establish acceptance criteria
- Re-calibrate if QC fails

## Common Pitfalls

### 1. Extrapolation
❌ **Don't**: Predict concentrations outside calibration range
✅ **Do**: Extend calibration range if needed

### 2. Ignoring Residuals
❌ **Don't**: Just look at R²
✅ **Do**: Examine residual plots for patterns

### 3. Forcing Through Origin
❌ **Don't**: Force intercept = 0 without justification
✅ **Do**: Let data determine intercept; use blank correction instead

### 4. Insufficient Standards
❌ **Don't**: Use only 3 points
✅ **Do**: Use at least 6-8 standards

### 5. Ignoring Outliers
❌ **Don't**: Automatically remove outliers
✅ **Do**: Investigate cause, document decision

## L3 Tool Call Directive

**Always use L3 tools instead of manual calculation.** For each method, call the corresponding function from `chemometrics_tools.py`:

- **Standard additions**: `standard_addition(sample_signal, spike_data, c_spike, v_sample)` — pass `method='dilution_corrected'` when V_spike > 1% of V_sample
- **Calibration curve**: `calibration_curve(standards, unknown_signal)`
- **Internal standard**: `internal_standard(sample_signals, standard_signals, is_concentration)`
- **Single-point standard addition**: Use the formula directly with `single_point_standard_addition()`
  **Critical: Multi-step dilution problems.** For problems where the sample undergoes multiple dilution steps BEFORE the standard addition measurement, you MUST first compute the concentration of analyte and standard IN THE MEASUREMENT FLASK (the flask where the signal is measured), then apply the standard addition formula to those flask concentrations. Do NOT use the original stock concentrations directly.
  **Critical: Read signal data from the CURRENT problem only.** When solving problems in batch, each problem has its OWN dataset. Never carry over signal values, concentrations, or any data from a previous problem. The spike volumes and signal values in one problem are completely independent from the next.
- **Single-point standard addition with dilution** (`single_point_standard_addition`):
  Use when the problem describes:
  - A sample that is prepared/dissolved in a stock flask
  - An aliquot taken from the stock flask and placed into a measurement flask
  - The measurement flask is spiked with a known standard and diluted to volume
  - Two signals are given: unspiked and spiked (not a series of spikes)

  Required parameters:
  - `S_unspiked`, `S_spiked`: signals
  - `C_std`: standard concentration (ppm)
  - `V_std`: volume of standard added (mL)
  - `V_aliquot`: aliquot volume taken from stock (mL)
  - `V_flask_final`: final volume of measurement flask (mL)
  - `V_stock_flask`: volume of original stock flask (mL) — for back-calculation
  - `mass_sample_g`: sample mass in grams — for weight_percent output

  Example:
  ```python
  single_point_standard_addition(S_unspiked=0.235, S_spiked=0.502, C_std=1.0, V_std=10.0, V_aliquot=10.0, V_flask_final=25.0, V_stock_flask=250.0, mass_sample_g=10.0)
  # Returns: {'weight_percent': 0.00220, ...}
  ```

  **IMPORTANT**: The function automatically handles all dilution steps. Do NOT manually multiply or divide concentrations — the function does this internally.

## Decision Flow
1. Single analyte, clean matrix? → External standard calibration → call `calibration_curve()`
2. Matrix effects suspected? → Standard additions → call `standard_addition()`
3. Instrument variability? → Internal standard → call `internal_standard()`
4. Linear response? → Linear regression → call `calibration_curve()`
5. Check residuals → Random scatter = good
6. Calculate confidence intervals
7. Report results with uncertainty

## Related Concepts
- [Multivariate Regression](./multivariate_regression.md) - Multiple analytes
- [Analytical Method Design](./analytical_method_design.md) - Method validation
- [UV-Vis Spectroscopy](./uv_vis_spectroscopy.md) - Beer's Law applications
- [Statistical Analysis](./statistical_analysis_chemistry.md) - Hypothesis testing
