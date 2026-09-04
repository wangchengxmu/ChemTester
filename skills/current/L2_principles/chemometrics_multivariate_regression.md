---
id: chemometrics.multivariate_regression
layer: 2
title: Multivariate Linear Regression
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch11.4
---

## Core Concepts

Multivariate linear regression extends simple linear regression to multiple dependent variables and/or multiple independent variables, enabling simultaneous analysis of multiple analytes.

## Multivariate Beer's Law

### Single Analyte (Univariate)

```
A = ÎµbC + Ablank
```

One wavelength, one analyte.

### Multiple Analytes (Multivariate)

**Matrix form:**
```
[A]nÃj = [C]nÃk Ã [Îµb]kÃj
```

Where:
- [A] = Absorbance matrix (n samples Ã j wavelengths)
- [C] = Concentration matrix (n samples Ã k analytes)
- [Îµb] = Molar absorptivity Ã pathlength (k analytes Ã j wavelengths)

**Key insight:** Each wavelength provides information about all analytes.

## Calibration for Multiple Analytes

### Standard Solutions

Prepare n standard solutions, each containing known concentrations of k analytes.

**Requirements:**
- n â?k (at least as many standards as analytes)
- j â?k (at least as many wavelengths as analytes)
- Standards should span concentration ranges

### Calibration Matrix

**Concentration matrix [C]:**
- n rows (standards)
- k columns (analytes)
- Known values

**Absorbance matrix [A]:**
- n rows (standards)
- j columns (wavelengths)
- Measured values

### Solving for Calibration Coefficients

From Beer's Law:
```
[A]nÃj = [C]nÃk Ã [Îµb]kÃj
```

**Matrix algebra solution:**

1. **Pre-multiply by [C]T:**
```
[C]TkÃn Ã [A]nÃj = [C]TkÃn Ã [C]nÃk Ã [Îµb]kÃj
```

2. **Pre-multiply by inverse:**
```
([C]TkÃn Ã [C]nÃk)^(-1) Ã [C]TkÃn Ã [A]nÃj = [Îµb]kÃj
```

This is the **least squares solution** for [Îµb].

## Prediction of Unknown Concentrations

### From Sample Spectrum

Measure absorbance at j wavelengths: [A]1Ãj

**Calculate concentrations:**

From Beer's Law:
```
[A]nÃj = [C]nÃk Ã [Îµb]kÃj
```

**Solve for [C]:**

1. **Post-multiply by [Îµb]T:**
```
[A]nÃj Ã [Îµb]TjÃk = [C]nÃk Ã [Îµb]kÃj Ã [Îµb]TjÃk
```

2. **Post-multiply by inverse:**
```
[A]nÃj Ã [Îµb]TjÃk Ã ([Îµb]kÃj Ã [Îµb]TjÃk)^(-1) = [C]nÃk
```

## Classical Least Squares (CLS)

### Assumptions

1. **Known components:** All analytes identified
2. **Linear additivity:** Signals are additive
3. **No interactions:** Analytes don't affect each other's spectra

### Advantages

- Simple to implement
- Full spectral information used
- Good for well-characterized systems

### Limitations

- Requires knowledge of all components
- Assumes additivity holds
- Sensitive to baseline shifts

## Inverse Least Squares (ILS)

Also known as P-matrix method or Multiple Linear Regression (MLR).

### Model

```
[C]nÃk = [A]nÃj Ã [P]jÃk
```

Where [P] contains regression coefficients.

### Calibration

Solve directly for [P]:
```
[P]jÃk = ([A]TjÃn Ã [A]nÃj)^(-1) Ã [A]TjÃn Ã [C]nÃk
```

### Advantages

- Can handle unknown interferents
- Fewer assumptions required

### Limitations

- Risk of overfitting (j > n)
- Requires many calibration samples
- Wavelength selection critical

## Principal Component Regression (PCR)

Combines PCA with regression.

### Steps

1. **Perform PCA on [A]:**
```
[A]nÃj = [S]nÃk Ã [L]kÃj
```

2. **Regression on scores:**
```
[C]nÃk = [S]nÃm Ã [B]mÃk
```

Where m â?k (number of PCs used).

### Advantages

- Handles collinearity
- Noise reduction (fewer PCs)
- Dimensionality reduction

## Partial Least Squares (PLS)

Most popular multivariate calibration method.

### Concept

Finds latent variables that:
- Capture variance in [A]
- Correlate with [C]

### Algorithm

Iteratively extract components:
1. Find direction in [A] space that maximizes covariance with [C]
2. Calculate scores and loadings
3. Deflate matrices
4. Repeat

### Advantages

- Handles collinearity
- Uses concentration information
- Often better predictions than PCR

### Variants

- **PLS-1:** One analyte at a time
- **PLS-2:** Multiple analytes simultaneously

## Model Validation

### Cross-Validation

**Leave-one-out (LOO):**
- Remove one sample
- Calibrate on remaining n-1
- Predict left-out sample
- Repeat for all samples

**k-fold:**
- Divide data into k groups
- Leave out one group
- Calibrate on remaining
- Repeat k times

### Metrics

**Root Mean Square Error of Calibration (RMSEC):**
```
RMSEC = â[Î£(Cactual - Cpred)Â² / n]
```

**Root Mean Square Error of Cross-Validation (RMSECV):**
```
RMSECV = â[Î£(Cactual - Cpred)Â² / n]
```

**Coefficient of Determination (RÂ²):**
```
RÂ² = 1 - Î£(Cactual - Cpred)Â² / Î£(Cactual - CÌ)Â²
```

### Optimal Number of Components

Balance:
- Too few: Underfitting, lose information
- Too many: Overfitting, fit noise

Plot RMSECV vs. number of components, choose minimum.

## Wavelength Selection

### Why Select Wavelengths?

- Remove uninformative regions
- Reduce noise
- Improve prediction
- Simpler models

### Methods

1. **Knowledge-based:**
   - Use known absorption bands
   - Avoid interferent regions

2. **Statistical:**
   - Forward selection
   - Backward elimination
   - Genetic algorithms

3. **Interval methods:**
   - iPLS (interval PLS)
   - Test spectral regions

## R Implementation

```r
# Classical Least Squares
# Calibration
C_matrix <- as.matrix(standards_conc)
A_matrix <- as.matrix(standards_abs)
epsilon_b <- solve(t(C_matrix) %*% C_matrix) %*% t(C_matrix) %*% A_matrix

# Prediction
C_pred <- A_sample %*% t(epsilon_b) %*% solve(epsilon_b %*% t(epsilon_b))

# PLS using pls package
library(pls)
model <- plsr(concentration ~ spectra, ncomp = 10, data = calibration,
              validation = "LOO")

# Summary
summary(model)

# RMSEP
RMSEP(model)

# Scores plot
plot(model, plottype = "scores")

# Loadings plot
plot(model, plottype = "loadings")

# Prediction
pred <- predict(model, newdata = test_spectra, ncomp = 5)

# Cross-validation
model_cv <- plsr(concentration ~ spectra, ncomp = 15,
                 data = calibration, validation = "CV")

# Plot RMSECV
plot(RMSEP(model_cv), legendpos = "topright")

# PCR
pcr_model <- pcr(concentration ~ spectra, ncomp = 10, data = calibration)

# Compare methods
compare_models <- data.frame(
  Method = c("PCR", "PLS"),
  RMSECV = c(min(RMSEP(pcr_model)), min(RMSEP(model)))
)
```

## Applications in Chemistry

### UV-Vis Spectroscopy
- Multiple analyte determination
- Pharmaceutical analysis
- Environmental monitoring

### NIR Spectroscopy
- Agricultural products
- Food analysis
- Pharmaceutical quality control

### IR Spectroscopy
- Polymer analysis
- Gas mixtures
- Reaction monitoring

### Chromatography
- Deconvolution of overlapping peaks
- Quantitative analysis
- Impurity profiling

## Key Formulas Summary

| Method | Model | Calibration | Prediction |
|--------|-------|-------------|------------|
| CLS | [A] = [C][Îµb] | [Îµb] = ([C]T[C])^(-1)[C]T[A] | [C] = [A][Îµb]T([Îµb][Îµb]T)^(-1) |
| ILS | [C] = [A][P] | [P] = ([A]T[A])^(-1)[A]T[C] | [C] = [A][P] |
| PCR | [C] = [S][B] | PCA + regression | Scores Ã coefficients |
| PLS | Latent variables | Maximize covariance | Scores Ã coefficients |

## Common Pitfalls

1. **Insufficient standards:** Need enough for all analytes
2. **Collinear concentrations:** Standards not independent
3. **Overfitting:** Too many components
4. **Poor wavelength selection:** Include noise regions
5. **Ignoring validation:** Must validate predictions

## Model Comparison

| Method | Advantages | Disadvantages | Best For |
|--------|------------|---------------|----------|
| CLS | Simple, interpretable | Requires all components known | Well-characterized systems |
| ILS | Handles unknowns | Overfitting risk | Limited wavelengths |
| PCR | Handles collinearity | Doesn't use [C] info | Noisy data |
| PLS | Best predictions | More complex | General use |

## Connection to Other Topics

- **PCA** (L2_principal_component_analysis.md): PCR uses PCA
- **Calibration** (L2_calibration_regression.md): Extension to multiple analytes
- **Cluster Analysis** (L2_cluster_analysis.md): Identify sample groups
- **Data Preprocessing** (L2_data_preprocessing.md): Essential for multivariate data

## See Also

- Harvey, Chemometrics Using R, Chapter 11.4
- Martens & Naes, Multivariate Calibration
- L3_code_examples/multivariate_regression_in_R.R


## Implementations

- Implementation: `../L3_functions/chemometrics_mlr.py`

## L3 Tool Call Directives


**Source:** `chemometrics_mlr.py`

L3 tool module for chemometrics mlr

### Available functions:
- `cls_fit(C: NDArray[np.floating], A: NDArray[np.floating])` → dict — Fit Classical Least Squares (CLS) calibration model.
- `cls_predict(A: NDArray[np.floating], K: Union[NDArray[np.floating], Dict])` → NDArray[np.floating] — Predict concentrations from spectra using CLS model.
- `pls_fit(X: NDArray[np.floating], Y: NDArray[np.floating], n_components: int, max_iter: int, tol: float)` → dict — Fit Partial Least Squares (PLS) regression model using NIPALS algorithm.
- `pls_predict(X: NDArray[np.floating], model: Dict[str, Union[NDArray[np.floating], int, None]], n_components: Optional[int])` → NDArray[np.floating] — Predict Y values from X using fitted PLS model.
- `pls_vip(model: Dict[str, Union[NDArray[np.floating], int, None]])` → NDArray[np.floating] — Calculate Variable Importance in Projection (VIP) scores.
- `cross_validate(model_func: Callable, X: NDArray[np.floating], Y: NDArray[np.floating], k: int)` → dict — Perform k-fold cross-validation for model assessment.
- `optimal_components(X: NDArray[np.floating], Y: NDArray[np.floating], max_components: int, k: int)` → dict — Find optimal number of PLS components by cross-validation.
- `rmse(actual: NDArray[np.floating], predicted: NDArray[np.floating])` → float — Calculate Root Mean Square Error.
- `mae(actual: NDArray[np.floating], predicted: NDArray[np.floating])` → float — Calculate Mean Absolute Error.
- `r_squared(actual: NDArray[np.floating], predicted: NDArray[np.floating])` → float — Calculate coefficient of determination R2.
- `bias(actual: NDArray[np.floating], predicted: NDArray[np.floating])` → float — Calculate bias (mean prediction error).

### Common errors:
- ❌ Passing wrong parameter types (strings where numbers expected)
- ❌ Forgetting required parameters
