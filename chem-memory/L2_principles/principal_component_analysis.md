---
id: chemometrics.pca
layer: 2
title: Principal Component Analysis (PCA)
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/pca_analysis.R
cross_links:
  - ./cluster_analysis.md
  - ./multivariate_regression.md
  - ./uv_vis_spectroscopy.md
source: Chemometrics Using R (Harvey), Ch11.3, Ch11.6
---

## Context
Principal Component Analysis (PCA) is a multivariate statistical technique used to reduce the dimensionality of complex datasets while preserving maximum variance. It transforms original variables into new orthogonal axes (principal components) that capture the underlying structure in the data.

## Core Principle

### Dimensionality Reduction
- **Problem**: High-dimensional data (e.g., spectra with 635 wavelengths) is difficult to visualize and analyze
- **Solution**: Find new axes that capture maximum variance in fewer dimensions
- **Key insight**: Rotate coordinate system to align with data structure

### Mathematical Foundation
For a data matrix **D** with n samples and m variables:

```
[D]_{n×m} = [S]_{n×k} × [L]_{k×m}
```

Where:
- **S** = scores matrix (n samples × k components)
- **L** = loadings matrix (k components × m variables)
- k << m (dimensionality reduction)

## How PCA Works

### Step-by-Step Process
1. **Center and scale data**: Subtract mean, optionally scale to unit variance
2. **Find first principal component (PC1)**:
   - Axis that maximizes variance through data cloud
   - Analogous to regression line through scatter plot
3. **Find second principal component (PC2)**:
   - Orthogonal (perpendicular) to PC1
   - Maximizes remaining variance
4. **Repeat** for all components (or stop when variance is explained)

### Visualization
```
Original axes:          Rotated axes (PCs):
    y                       PC2
    ↑                       ↑
    │   ●                   │  ●
    │ ●   ●                 │●   ●
    │  ●                    │ ●
    │   ●                   │  ●
    └─────→ x       └─────→ PC1
    
Rotation aligns axes with data spread
```

## Scores and Loadings

### Scores (S)
- **Definition**: Coordinates of samples in new PC space
- **Interpretation**: Position of each sample along each principal component
- **Chemistry meaning**: Related to concentrations or properties of analytes

```
Score plot:              Interpretation:
    PC2                      PC2
      ↑                        ↑
   ●  │  ●                   ●  │  ●
 ●    │    ●  ← Sample       ●  │    ●
      │      positions         │
      └─────→ PC1              └─────→ PC1
```

### Loadings (L)
- **Definition**: Cosines of angles between PC axes and original axes
- **Interpretation**: Contribution of each original variable to each PC
- **Chemistry meaning**: Related to spectral signatures or property contributions

```
Loadings indicate:
- Which wavelengths correlate with which PCs
- Which variables group together
- Spectral features of components
```

## Variance Explained

### Variance Decomposition
Each principal component explains a portion of total variance:

| Component | Std Dev | Variance Explained | Cumulative |
|-----------|---------|-------------------|------------|
| PC1 | 3.3134 | 68.62% | 68.62% |
| PC2 | 2.1901 | 29.98% | 98.59% |
| PC3 | 0.4256 | 1.13% | 99.73% |
| PC4 | 0.1759 | 0.19% | 99.92% |
| ... | ... | ... | 100% |

### Scree Plot
```
Variance
  │*
  │**
  │***
  │****___
  │*******_______
  │******************____________
  └────────────────────────────→ PC
  1  2  3  4  5  6  7  8  9 10

"Elbow" indicates significant components
```

### Determining Number of Components
**Methods**:
1. **Cumulative variance**: Keep components until >95% variance explained
2. **Scree plot elbow**: Look for point where curve levels off
3. **Cross-validation**: Use predictive ability to select components
4. **Chemical reasoning**: Does number match expected analytes?

## Interpretation in Chemistry

### Beer's Law Analogy
For spectroscopic data:

```
PCA:            [A] = [S] × [L]

Beer's Law:     [A] = [C] × [εb]

Correspondence:
- Scores (S) ~ Concentrations (C)
- Loadings (L) ~ Molar absorptivities (εb)
```

### Sample Classification
**Pattern recognition**:
- Samples with similar scores are similar chemically
- Clusters in score plot indicate groups
- Outliers appear isolated

**Example: Ternary mixtures**
```
Score plot triangle:
    PC2
     ↑
  1  ●     ← Pure component 1
     │
  2  ●─────● 3  ← Pure components 2, 3
     │  ●       
     │ ● ●  ← Binary mixtures (on edges)
     │  ●     ← Ternary mixtures (interior)
     └─────→ PC1
```

### Biplot
Combines scores and loadings on one plot:

```
    PC2
     ↑
  ●  │  ●     Scores (samples) = dots
     │↗       Loadings = arrows
  ●  │  ●     Arrow direction = wavelength association
     │   ↘    
     └─────→ PC1

Arrows pointing toward sample = wavelength absorbed by that analyte
```

## R Implementation

### Basic PCA
```r
# Load data
spec_data <- read.csv("allSpec.csv", check.names = FALSE)

# Select subset
pca_data <- spec_data[sample_ids, wavelength_ids]

# Run PCA (center and scale)
pca_results <- prcomp(pca_data, center = TRUE, scale = TRUE)

# View summary
summary(pca_results)
```

### Exploring Results
```r
# Standard deviations and variance
plot(pca_results)  # Scree plot

# Score plots
plot(pca_results$x, pch = 19)  # PC1 vs PC2
plot(pca_results$x[,2], pca_results$x[,3], pch = 19,
     xlab = "PC2", ylab = "PC3")

# 3D visualization
library(plot3D)
scatter3D(x = pca_results$x[,1], y = pca_results$x[,2], 
          z = pca_results$x[,3], pch = 19)

# Biplot
biplot(pca_results, cex = c(2, 0.6), xlabs = rep("•", n))
```

### Color-Coding by Property
```r
# Create color palette for Cu concentration
cu_palette <- colorRampPalette(c("white", "blue"))
cu_color <- cu_palette(50)[as.numeric(cut(spec_data$concCu, breaks = 50))]

# Plot with colors
plot(pca_results$x, pch = 21, bg = cu_color, cex = 2)
```

## Applications in Chemistry

### 1. Spectroscopic Analysis
- **UV-Vis**: Identify components in mixtures
- **IR/NIR**: Functional group identification
- **Raman**: Molecular fingerprinting
- **Example**: Identify metal ions in solution from visible spectra

### 2. Quality Control
- **Process monitoring**: Detect deviations from normal
- **Batch classification**: Group similar products
- **Outlier detection**: Identify unusual samples

### 3. Environmental Analysis
- **Source apportionment**: Identify pollution sources
- **Time series**: Extract trends from noisy data
- **Multi-analyte screening**: Reduce complexity

### 4. Metabolomics and Proteomics
- **Biomarker discovery**: Find discriminating metabolites
- **Sample classification**: Disease vs control
- **Pattern recognition**: Biological state identification

## Assumptions and Limitations

### Assumptions
1. Linear relationships between variables
2. Large variance = important information
3. Orthogonal components (uncorrelated)

### Limitations
1. **May miss nonlinear structure**: Consider kernel PCA
2. **Variance ≠ importance**: Sometimes small variance is meaningful
3. **Interpretation required**: PCs don't directly identify chemicals
4. **Sensitive to scaling**: Choice of scaling affects results

### When to Use PCA
✅ **Good for**:
- High-dimensional data
- Exploratory analysis
- Reducing to 2-3 components for visualization
- Finding major patterns

❌ **Not ideal for**:
- Highly nonlinear relationships
- When all variables are uncorrelated
- When you need specific physical interpretation

## Comparison with Related Methods

| Method | Purpose | Key Feature |
|--------|---------|-------------|
| PCA | Dimensionality reduction | Maximum variance |
| ICA | Source separation | Statistical independence |
| MDS | Dimensionality reduction | Preserve distances |
| Factor Analysis | Latent variables | Model-based |
| PLS | Regression | Maximize covariance with Y |

## Decision Flow
1. Have multivariate data? → Consider PCA
2. How many dimensions? Check scree plot
3. Can you interpret scores? Look at sample patterns
4. Can you interpret loadings? Identify important variables
5. Validate with known samples

## Related Concepts
- [Cluster Analysis](./cluster_analysis.md) - Grouping similar samples
- [Multivariate Regression](./multivariate_regression.md) - Quantitative prediction
- [UV-Vis Spectroscopy](./uv_vis_spectroscopy.md) - Spectral applications

## L3 Tool Call Directives

**Source:** pca_analysis.py
PCA Analysis Tools - L3 Implementation

### Available functions:
- center_data(data, axis) →  — Mean-center the data matrix.
- standardize_data(data, axis) →  — Standardize data to zero mean and unit variance.
- pca_svd(data, n_components, standardize) →  — Perform PCA using singular value decomposition.
- scree_data(eigenvalues) →  — Generate data for scree plot.
- variance_table(eigenvalues, decimals) →  — Create variance explained table.
- n_components_for_variance(cumulative_variance, threshold) → int — Determine number of components needed for target variance.
- kaiser_criterion(eigenvalues) → int — Apply Kaiser criterion: retain components with eigenvalue > 1.
- reconstruct_data(scores, loadings, mean, std) →  — Reconstruct data from PCA components.
- project_new_samples(new_data, loadings, mean, std) →  — Project new samples onto existing PCA space.
- hotelling_t2(scores, eigenvalues) →  — Calculate Hotelling's T2 statistic for outlier detection.
- q_residuals(original_data, reconstructed_data) →  — Calculate Q residuals (SPE - Squared Prediction Error).

### Common errors:
- ❌ Passing wrong parameter types or missing required arguments
