---
id: chemometrics.principal_component_analysis
layer: 2
title: Principal Component Analysis (PCA)
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch11.3
---

## Core Concepts

Principal Component Analysis (PCA) reduces data dimensionality by creating new variables (principal components) that capture maximum variance in the data.

## How PCA Works

### Geometric Intuition

1. **Original data:** Samples plotted in n-dimensional space (one dimension per variable)

2. **Find first PC:**
   - Rotate axes to find direction of maximum variance
   - This becomes the first principal component (PC1)

3. **Find subsequent PCs:**
   - Each PC is orthogonal (perpendicular) to previous PCs
   - Each captures remaining variance

4. **Result:**
   - Few PCs explain most variance
   - Noise captured in later PCs

### Mathematical Framework

**Data Matrix:**
```
[D]nÃp
```
n = samples, p = variables

**Decomposition:**
```
[D]nÃp = [S]nÃk Ã [L]kÃp
```

Where:
- [S] = Scores matrix (n Ã k)
- [L] = Loadings matrix (k Ã p)
- k = number of principal components

### Scores and Loadings

**Scores:**
- Position of samples along each PC axis
- One score per sample per PC
- Related to sample properties (e.g., concentrations)

**Loadings:**
- Cosines of angles between PCs and original axes
- One loading per variable per PC
- Related to variable importance (e.g., molar absorptivities)

## Variance Explained

### Scree Plot

Shows variance explained by each PC:
- PC1 explains most variance
- Subsequent PCs explain less
- "Elbow" indicates where signal ends and noise begins

### Cumulative Variance

```
Cumulative variance = Î£(variance explained by PCi) / total variance
```

**Rule of thumb:**
- PCs should explain >95% cumulative variance
- Later PCs likely represent noise

### Example: 24 Samples, 16 Wavelengths

| PC | Standard Deviation | Proportion of Variance | Cumulative Proportion |
|----|-------------------|------------------------|----------------------|
| PC1 | 3.3134 | 0.6862 (68.62%) | 0.6862 |
| PC2 | 2.1901 | 0.2998 (29.98%) | 0.9859 (98.59%) |
| PC3 | 0.4256 | 0.0113 (1.13%) | 0.9973 (99.73%) |

**Interpretation:**
- PC1 and PC2 explain 98.59% of variance
- Only 2 components needed to model data
- Remaining 14 PCs represent noise

## Scores Plots

### Interpretation

**Pattern recognition:**
- Clusters indicate similar samples
- Outliers appear isolated
- Gradients show continuous variation

**Triangular pattern:**
- Suggests mixture of components
- Vertices = pure components
- Edges = binary mixtures
- Interior = ternary mixtures

### Example: 24 Spectral Samples

**Scores plot (PC1 vs. PC2):**
- Triangular distribution observed
- Three vertices (samples 1, 2, 3) = pure components
- Points along edges = binary mixtures
- Interior points = ternary mixtures

## Loadings Plots

### Interpretation

**Loading values:**
- High positive loading: Strong positive correlation with PC
- High negative loading: Strong negative correlation with PC
- Near zero: Little contribution to PC

### Biplot (Scores + Loadings)

Combines scores plot with loading vectors:
- Arrows show variable contributions
- Arrow direction: Which PCs variable influences
- Arrow length: Magnitude of contribution
- Samples grouped near arrow: Strongly influenced by that variable

### Example: Wavelength Loadings

**For spectral data:**
- Loadings related to molar absorptivities
- Compare loadings to pure component spectra
- Identify which wavelengths characterize each component

**Findings:**
- 672.7-868.7 nm: Associated with CuÂ²â?- 380.5-613.3 nm: Associated with CrÂ³â?- Middle wavelengths: Associated with CoÂ²â?
## Beer's Law Connection

**Beer's Law in matrix form:**
```
[A]nÃj = [C]nÃk Ã [Îµb]kÃj
```

Where:
- [A] = Absorbance matrix (n samples Ã j wavelengths)
- [C] = Concentration matrix (n samples Ã k analytes)
- [Îµb] = Molar absorptivity Ã pathlength matrix

**PCA decomposition:**
```
[D]nÃj = [S]nÃk Ã [L]kÃj
```

**Analogy:**
- Scores [S] â?Concentrations [C]
- Loadings [L] â?Molar absorptivities [Îµb]

## Data Preprocessing for PCA

### Mean Centering

```
xcentered = x - xÌ
```

Essential: Removes offset, focuses on variation

### Standardization

```
z = (x - xÌ) / s
```

Use when variables on different scales

### Other Preprocessing

- **Log transformation:** Right-skewed data
- **Smoothing:** Noisy spectra
- **Derivatives:** Remove baseline effects

## Choosing Number of Components

### Methods

1. **Scree plot:** Look for elbow
2. **Cumulative variance:** Retain PCs explaining >95%
3. **Kaiser criterion:** Retain PCs with eigenvalue > 1
4. **Cross-validation:** Predictive ability

### Practical Considerations

- More components = more noise included
- Too few components = lose important information
- Balance parsimony vs. explanatory power

## R Implementation

```r
# Perform PCA
pca <- prcomp(data, scale. = TRUE)  # scale. = TRUE standardizes

# Summary of results
summary(pca)

# Variance explained
var_explained <- pca$sdev^2 / sum(pca$sdev^2)

# Scree plot
plot(pca, type = "l", main = "Scree Plot")

# Scores
scores <- pca$x

# Loadings
loadings <- pca$rotation

# Scores plot
plot(scores[,1], scores[,2],
     xlab = "PC1", ylab = "PC2",
     main = "Scores Plot")

# Biplot
biplot(pca, scale = 0)

# Using ggplot2
library(ggplot2)
scores_df <- data.frame(PC1 = scores[,1], PC2 = scores[,2])
ggplot(scores_df, aes(x = PC1, y = PC2)) +
  geom_point() +
  labs(title = "PCA Scores Plot")

# Number of components for 95% variance
cumvar <- cumsum(var_explained)
n_components <- which(cumvar >= 0.95)[1]
```

## Applications in Chemistry

### Spectroscopy
- Identify components in mixtures
- Reduce spectral dimensionality
- Detect outliers

### Metabolomics
- Pattern recognition
- Biomarker discovery
- Sample classification

### Quality Control
- Process monitoring
- Detect batch variations
- Identify outlier samples

### Chromatography
- Peak alignment
- Data compression
- Pattern recognition

## Interpreting PCA Results

### Step-by-Step Guide

1. **Examine scree plot:**
   - How many PCs needed?
   - Clear separation between signal and noise?

2. **Check variance explained:**
   - Is cumulative variance acceptable?
   - Are you capturing enough information?

3. **Analyze scores plots:**
   - Are there clusters? Outliers?
   - What patterns do you see?

4. **Interpret loadings:**
   - Which variables contribute to each PC?
   - Can you assign chemical meaning?

5. **Relate to known chemistry:**
   - Do results make sense chemically?
   - Can you identify components?

## Key Concepts Summary

| Concept | Description | Interpretation |
|---------|-------------|----------------|
| Principal Component | New axis capturing variance | Linear combination of original variables |
| Scores | Sample positions on PCs | Sample properties (e.g., concentrations) |
| Loadings | Variable contributions | Variable importance (e.g., absorptivities) |
| Variance explained | Information captured by PC | Quality of dimension reduction |
| Biplot | Scores + loadings together | Sample-variable relationships |

## Common Pitfalls

1. **Not centering data:** Mean centering is essential
2. **Over-interpreting PCs:** May not have chemical meaning
3. **Ignoring preprocessing:** Scale differences dominate
4. **Too many components:** Include noise
5. **Assuming causation:** PCs show correlation, not causation

## Connection to Other Topics

- **Cluster Analysis** (L2_cluster_analysis.md): Use PCA scores for clustering
- **Multivariate Regression** (L2_multivariate_regression.md): PCR (PCA + regression)
- **Calibration** (L2_calibration_regression.md): Multivariate calibration
- **Data Preprocessing** (L2_data_preprocessing.md): Essential for PCA

## See Also

- Harvey, Chemometrics Using R, Chapter 11.3
- L3_code_examples/pca_in_R.R


## Implementations
- Implementation: `../L3_functions/pca_analysis.py`

- Implementation: `../L3_functions/chemometrics_pca.py`

---

## L3 Tool Call Directives

**Source:** chemometrics_pca.py
Principal Component Analysis: mean-centering, standardization, PCA fit/transform, diagnostics.

### Available functions:
- mean_center(X) �� ndarray �� Subtract column means from data matrix
- standardize(X) �� tuple[ndarray, ndarray] �� Z-score standardization (returns scaled X, std array)
- pca_fit(X, n_components) �� dict �� Fit PCA model (scores, loadings, eigenvalues, explained variance)
- pca_transform(X_new, pca_result) �� ndarray �� Project new data onto existing PCA model
- ariance_explained(pca_result, component) �� float �� Fraction of variance explained by component
- pca_reconstruct(pca_result, scores_subset) �� ndarray �� Reconstruct data from selected components
- hotelling_t2(pca_result, n_components) �� ndarray �� Hotelling T2 statistic per sample
- q_residuals(X, pca_result, n_components) �� ndarray �� Q-residuals (reconstruction error) per sample

### Common errors:
- ? Fitting PCA on unstandardized data when variables have different units/scales
- ? Using too many components (overfitting) �� check cumulative variance explained
