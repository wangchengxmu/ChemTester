---
id: chemometrics.multivariate_regression
layer: 2
title: Multivariate Linear Regression
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/multivariate_regression.R
cross_links:
  - ./principal_component_analysis.md
  - ./cluster_analysis.md
  - ./calibration_curves.md
source: Chemometrics Using R (Harvey), Ch11.4, Ch11.7
---

## Context
Multivariate linear regression extends simple linear regression to situations with multiple dependent variables and/or multiple independent variables. In chemometrics, it enables simultaneous determination of multiple analytes in complex mixtures using spectroscopic or other multivariate measurements.

## Core Principle

### Matrix Formulation
For multivariate calibration with:
- n samples
- k analytes (independent variables)
- j wavelengths (dependent variables)

```
[A]_{n×j} = [C]_{n×k} × [εb]_{k×j}
```

Where:
- **A** = absorbance matrix (n samples × j wavelengths)
- **C** = concentration matrix (n samples × k analytes)
- **εb** = calibration matrix (k analytes × j wavelengths)

### Why Multivariate?
**Problem**: Single wavelength can't distinguish overlapping spectra

```
Absorbance
  │    Analyte 1 (blue)
  │  ●●●●●●●●●●●●
  │           Analyte 2 (red)
  │        ●●●●●●●●●●●●
  │  Mixture (black)
  │  ●●●●●●●●●●●●●●●●●●
  └─────────────────────→ Wavelength
```

**Solution**: Use multiple wavelengths simultaneously

## Calibration Process

### Step 1: Prepare Standards
Create n standard solutions with known concentrations of k analytes:

```
Concentration Matrix [C]_{n×k}
           Analyte 1  Analyte 2  Analyte 3
Sample 1    0.100      0.000      0.000
Sample 2    0.000      0.100      0.000
Sample 3    0.000      0.000      0.100
Sample 4    0.050      0.050      0.000
Sample 5    0.050      0.000      0.050
...         ...        ...        ...
Sample n    0.033      0.033      0.033
```

### Step 2: Measure Spectra
Measure absorbance at j wavelengths for all standards:

```
Absorbance Matrix [A]_{n×j}
           λ₁    λ₂    λ₃   ...   λⱼ
Sample 1   0.45  0.32  0.18 ...   0.05
Sample 2   0.12  0.38  0.41 ...   0.22
Sample 3   0.08  0.15  0.28 ...   0.35
...        ...   ...   ...  ...   ...
Sample n   0.28  0.29  0.31 ...   0.20
```

### Step 3: Solve for Calibration Matrix
From Beer's Law in matrix form:
```
[A] = [C] × [εb]
```

Solve using matrix algebra:
```
[εb] = ([C]^T [C])^(-1) [C]^T [A]
```

This is the **classical least squares (CLS)** approach.

### Step 4: Predict Unknown Concentrations
For unknown sample with measured spectrum [A]_unknown:

```
[C]_unknown = [A]_unknown × [εb]^T × ([εb] [εb]^T)^(-1)
```

## Matrix Operations Explained

### Transpose
```
Original matrix [C]_{3×2}:    Transpose [C]^T_{2×3}:
  C₁₁  C₁₂                      C₁₁  C₂₁  C₃₁
  C₂₁  C₂₂                      C₁₂  C₂₂  C₃₂
  C₃₁  C₃₂
```

### Matrix Multiplication
For **[C]^T [C]**:

```
[C]^T_{k×n} × [C]_{n×k} = [Result]_{k×k}

Each element: Result_ij = Σ (C^T)_{il} × C_{lj}
                         l=1 to n
```

### Matrix Inverse
For square matrix **M**, the inverse **M^(-1)** satisfies:
```
M × M^(-1) = I (identity matrix)
```

## Inverse Least Squares (ILS)

### Alternative Formulation
Instead of solving for εb, predict concentrations directly from spectra:

```
[C] = [A] × [B]
```

Where **B** is the regression coefficient matrix.

**Advantages**:
- Can use subset of wavelengths
- Doesn't require all analytes in standards
- More flexible for real samples

**Disadvantages**:
- Requires many calibration samples
- Sensitive to collinearity in spectra

## Validation

### Evaluating Calibration Quality

#### 1. Compare εb to Pure Spectra
```
Plot εb for each analyte vs. wavelength
Should match shape of pure component spectrum
```

**Example**:
```
εb for Cu²⁺: Matches Cu²⁺ spectrum ✓
εb for Cr³⁺: Matches Cr³⁺ spectrum ✓
εb for Co²⁺: Matches Co²⁺ spectrum ✓
```

#### 2. Prediction of Test Samples
```
Prepare independent test samples
Predict concentrations
Calculate prediction error:

RMSEP = √[Σ(C_predicted - C_actual)² / n]
```

#### 3. Residual Analysis
```
Residual = A_measured - A_predicted

Check for:
- Random distribution (good)
- Systematic patterns (model problems)
```

## Number of Calibration Samples

### Requirements
**Minimum**: n > k (more samples than analytes)

**Recommended**: n ≥ 3k to 5k

**Why?**
- Avoid overfitting
- Capture variability
- Enable validation

### Experimental Design
**Good calibration sets**:
- Include pure components
- Include binary mixtures
- Include ternary mixtures
- Span concentration range
- Cover expected sample space

**Example for 3 analytes**:
```
- 3 pure standards (one per analyte)
- 3 binary mixture series (pairs)
- 1 ternary mixture series
- Total: 15-25 standards
```

## R Implementation

### Classical Least Squares (CLS)
```r
# Prepare calibration data
C_cal <- as.matrix(concentration_data)  # n × k matrix
A_cal <- as.matrix(absorbance_data)     # n × j matrix

# Solve for calibration matrix
# Method 1: Using matrix operations
epsilon_b <- solve(t(C_cal) %*% C_cal) %*% t(C_cal) %*% A_cal

# Method 2: Using lm() for each wavelength
epsilon_b <- matrix(nrow = k, ncol = j)
for (i in 1:j) {
  model <- lm(A_cal[,i] ~ C_cal - 1)  # -1 for no intercept
  epsilon_b[,i] <- coef(model)
}

# Predict unknown concentrations
A_unknown <- as.matrix(unknown_spectrum)
C_unknown <- A_unknown %*% t(epsilon_b) %*% solve(epsilon_b %*% t(epsilon_b))
```

### Inverse Least Squares (ILS)
```r
# Using lm() for each analyte
C_pred <- matrix(nrow = n_test, ncol = k)
for (i in 1:k) {
  model <- lm(C_cal[,i] ~ A_cal)
  C_pred[,i] <- predict(model, newdata = data.frame(A_test))
}
```

### Using R Packages
```r
# chemometrics package
library(chemometrics)

# Partial Least Squares (PLS)
library(pls)
pls_model <- plsr(concentration ~ absorbance, ncomp = 3, 
                  data = calibration_data)
C_pred <- predict(pls_model, newdata = test_data)
```

## Comparison of Methods

| Method | Requirements | Advantages | Disadvantages |
|--------|-------------|------------|---------------|
| CLS | All analytes known | Interpretable εb | Need all analytes |
| ILS | Many samples | Flexible | Collinearity issues |
| PCR | PCA on spectra | Handles collinearity | Less interpretable |
| PLS | Response variable | Optimal for prediction | More complex |

## When to Use Multivariate Regression

### Appropriate Situations
✅ **Use multivariate when**:
- Multiple analytes present
- Overlapping spectral signals
- Complex matrices
- High-throughput screening

### Not Necessary
❌ **Simple calibration sufficient when**:
- Single analyte
- No spectral overlap
- Clean matrix
- One wavelength sufficient

## Partial Least Squares (PLS)

### Concept
Combines features of PCA and regression:
- Reduces dimensionality (like PCA)
- Predicts concentrations (like regression)
- Maximizes covariance between spectra and concentrations

### Why PLS?
**Advantages over CLS/ILS**:
- Handles collinear variables
- Works with fewer calibration samples
- Better prediction for complex mixtures
- Robust to noise

### PLS Components
```
Find latent variables (LVs) that:
1. Capture variance in X (spectra)
2. Correlate with Y (concentrations)
3. Are orthogonal (uncorrelated)
```

### R Implementation
```r
library(pls)

# Fit PLS model
pls_model <- plsr(C ~ A, ncomp = 5, data = cal_data,
                  validation = "CV")

# Determine optimal number of components
plot(RMSEP(pls_model), main = "PLS Model Selection")

# Predict
C_pred <- predict(pls_model, newdata = test_data, 
                  ncomp = optimal_ncomp)
```

## Validation Strategies

### Cross-Validation
**Leave-one-out (LOO)**:
- Remove one sample
- Calibrate on remaining
- Predict removed sample
- Repeat for all samples

**k-Fold**:
- Divide into k subsets
- Use k-1 for calibration, 1 for validation
- Rotate k times

### External Validation
**Best practice**:
1. Split data: calibration set (70%) + test set (30%)
2. Build model on calibration set
3. Validate on test set
4. Report RMSEP, R², bias

## Practical Considerations

### Wavelength Selection
**Full spectrum vs. selected wavelengths**:

**Full spectrum**:
- Uses all information
- Automatic with PLS/PCR

**Selected wavelengths**:
- Faster
- More interpretable
- Risk of losing information

### Data Preprocessing
**Common preprocessing**:
1. **Centering**: Subtract mean (always do)
2. **Scaling**: Divide by std dev (when different scales)
3. **Derivatives**: Remove baseline effects
4. **SNV**: Standard normal variate (scatter correction)

### Outliers
**Detection**:
- Leverage (influence on model)
- Residuals (model fit)
- Mahalanobis distance

**Action**:
- Investigate cause
- Remove if truly anomalous
- Keep if part of natural variation

## Decision Flow
1. Multiple analytes in samples? → Multivariate regression
2. All analytes known and in standards? → Consider CLS
3. Complex mixture or unknown interferences? → Consider PLS
4. Limited calibration samples? → Use PLS
5. Need interpretable spectra? → Use CLS or PCR
6. Validate with independent test set
7. Check prediction accuracy meets requirements

## Related Concepts
- [Principal Component Analysis](./principal_component_analysis.md) - Dimensionality reduction
- [Cluster Analysis](./cluster_analysis.md) - Sample grouping
- [Calibration Curves](./calibration_curves.md) - Univariate calibration
- [UV-Vis Spectroscopy](./uv_vis_spectroscopy.md) - Spectral applications
