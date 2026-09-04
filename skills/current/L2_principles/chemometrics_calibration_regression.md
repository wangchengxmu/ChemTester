---
id: chemometrics.calibration_regression
layer: 2
title: Calibration and Linear Regression in Chemistry
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch08
---

## Core Concepts

Calibration curves establish the relationship between analyte concentration and measured signal, enabling quantitative analysis.

## Linear Regression Model

### Beer's Law Application

```
A = εbC + Sblank
```

Where:
- A = Absorbance (signal)
- ε = Molar absorptivity
- b = Path length
- C = Concentration
- Sblank = Blank signal

### General Linear Model

```
y = β0 + β1x
```

Where:
- y = Measured signal
- x = Known concentration
- β0 = y-intercept (blank signal)
- β1 = Slope (sensitivity)

### Least Squares Estimation

Find b0 and b1 that minimize sum of squared residuals:

```
Minimize: Σ(yi - (b0 + b1xi))²
```

**Slope:**
```
b1 = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²
```

**Intercept:**
```
b0 = ȳ - b1x̄
```

## Uncertainty in Regression

### Standard Error of Estimate

```
sy/x = √[Σ(yi - ŷi)² / (n - 2)]
```

Measures scatter of points around regression line.

### Standard Errors of Parameters

**Slope:**
```
sb1 = sy/x / √[Σ(xi - x̄)²]
```

**Intercept:**
```
sb0 = sy/x × √[Σxi² / (nΣ(xi - x̄)²)]
```

### Confidence Intervals for Parameters

```
b1 ± t(α/2, n-2) × sb1
b0 ± t(α/2, n-2) × sb0
```

## Quality of Fit

### Correlation Coefficient (r)

```
r = Σ(xi - x̄)(yi - ȳ) / √[Σ(xi - x̄)² Σ(yi - ȳ)²]
```

Range: -1 ≤ r ≤ 1

### Coefficient of Determination (R²)

```
R² = 1 - SSres / SStot
```

Where:
- SSres = Σ(yi - ŷi)² (residual sum of squares)
- SStot = Σ(yi - ȳ)² (total sum of squares)

Range: 0 ≤ R² ≤ 1

**Interpretation:** Proportion of variance explained by model.

## Calibration Curve Evaluation

### Sensitivity
- Slope (b1) of calibration curve
- Higher slope = better sensitivity
- Units: signal/concentration

### Dynamic Range
- Linear range of calibration
- Upper and lower limits of linearity
- Often determined by R² > 0.995

### Detection Limit (LOD)

```
LOD = 3 × sblank / b1
```

Or from calibration:

```
LOD = 3.3 × sy/x / b1
```

### Quantitation Limit (LOQ)

```
LOQ = 10 × sblank / b1
```

Or from calibration:

```
LOQ = 10 × sy/x / b1
```

## Prediction Using Calibration

### Concentration from Signal

```
Csample = (Asample - b0) / b1
```

### Uncertainty in Predicted Concentration

```
sC = (sy/x / b1) × √[1/m + 1/n + (Asample - ȳ)² / (b1²Σ(xi - x̄)²)]
```

Where m = number of replicate measurements of sample.

**Confidence interval:**

```
Csample ± t(α/2, n-2) × sC
```

## Regression Diagnostics

### Residual Analysis

**Residual plots reveal:**
- Non-linearity (curved pattern)
- Non-constant variance (fan shape)
- Outliers (isolated points)
- Missing terms (systematic patterns)

### Assumptions of Linear Regression

1. **Linearity:** Relationship is linear
2. **Independence:** Errors are independent
3. **Normality:** Errors are normally distributed
4. **Equal variance:** Errors have constant variance (homoscedasticity)

### Testing Assumptions

```r
# Residual plot
plot(fitted(model), residuals(model))

# Q-Q plot for normality
qqnorm(residuals(model))
qqline(residuals(model))

# Scale-location plot
plot(fitted(model), sqrt(abs(residuals(model))))
```

## Weighted Regression

When variance is not constant across range:

```
Minimize: Σwi(yi - (b0 + b1xi))²
```

**Common weighting schemes:**
- wi = 1/si² (inverse variance)
- wi = 1/xi (counts data)
- wi = 1/xi² (concentration-dependent variance)

## Applications in Chemistry

### Spectrophotometry
- Beer's law calibration
- Multi-wavelength analysis
- Matrix-matched standards

### Chromatography
- Peak area vs. concentration
- Internal standard method
- Response factor determination

### Electrochemistry
- Calibration curves for ion-selective electrodes
- Standard addition method
- Potentiometric titrations

## R Implementation

```r
# Linear regression
model <- lm(signal ~ concentration, data = calibration)

# View summary
summary(model)

# Extract coefficients
coef(model)

# Confidence intervals for coefficients
confint(model, level = 0.95)

# Predict concentration with uncertainty
predict(model, newdata, interval = "confidence")

# Residual diagnostics
par(mfrow = c(2, 2))
plot(model)

# Weighted regression
model_w <- lm(signal ~ concentration, weights = 1/variance)

# Prediction
predicted_conc <- (signal - coef(model)[1]) / coef(model)[2]

# Prediction with uncertainty
predict(model, newdata, interval = "prediction")
```

## Key Formulas Summary

| Parameter | Formula | Purpose |
|-----------|---------|---------|
| Slope | b1 = Σ(xi-x̄)(yi-ȳ)/Σ(xi-x̄)² | Sensitivity |
| Intercept | b0 = ȳ - b1x̄ | Blank signal |
| R² | 1 - SSres/SStot | Goodness of fit |
| sy/x | √[Σ(yi-ŷi)²/(n-2)] | Scatter about line |
| LOD | 3.3 × sy/x / b1 | Detection limit |
| LOQ | 10 × sy/x / b1 | Quantitation limit |

## Common Issues and Solutions

| Problem | Symptom | Solution |
|---------|---------|----------|
| Non-linearity | Curved residual plot | Polynomial fit, transform data |
| Heteroscedasticity | Fan-shaped residuals | Weighted regression |
| Outliers | Large residuals | Investigate, consider robust regression |
| Poor precision | Large sy/x | Improve method, increase replicates |

## Connection to Other Topics

- **Significance Testing** (L2_significance_testing.md): Test if slope significantly different from zero
- **Multivariate Regression** (L2_multivariate_regression.md): Extension to multiple analytes
- **PCA** (L2_principal_component_analysis.md): Alternative approach for multivariate data
- **Experimental Design** (L2_experimental_design.md): Design calibration experiments

## See Also

- Harvey, Chemometrics Using R, Chapter 8
- L3_code_examples/calibration_curves_in_R.R
