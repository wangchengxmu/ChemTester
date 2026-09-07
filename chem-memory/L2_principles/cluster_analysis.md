---
id: chemometrics.cluster
layer: 2
title: Cluster Analysis
up_links:
  - ../L1_ontology/chemistry-core-map.md
down_links:
  - ../L3_functions/cluster_analysis.R
cross_links:
  - ./principal_component_analysis.md
  - ./multivariate_regression.md
source: Chemometrics Using R (Harvey), Ch11.2, Ch11.5
---

## Context
Cluster analysis is an unsupervised learning method that groups samples or variables based on similarity. It reveals structure in data by organizing objects into hierarchical trees (dendrograms) that show relationships and degrees of similarity.

## Core Principle

### Similarity-Based Grouping
- **Goal**: Group similar objects together
- **Method**: Calculate distances between all pairs
- **Output**: Dendrogram showing hierarchical relationships
- **Key insight**: No prior knowledge of groups needed (unsupervised)

### Distance Metrics

#### Euclidean Distance (most common)
For two samples with m variables:

```
d_ij = √[Σ(x_ik - x_jk)²]
       k=1 to m
```

**Example**: Two samples at 3 wavelengths
```
Sample i: [0.5, 0.8, 0.3]
Sample j: [0.4, 0.9, 0.2]

d_ij = √[(0.5-0.4)² + (0.8-0.9)² + (0.3-0.2)²]
     = √[0.01 + 0.01 + 0.01]
     = 0.173
```

#### Other Distance Measures
| Metric | Formula | Use When |
|--------|---------|----------|
| Euclidean | √Σ(x_i - y_i)² | Continuous variables, similar scales |
| Manhattan | Σ\|x_i - y_i\| | Robust to outliers |
| Cosine | 1 - (x·y)/(‖x‖‖y‖) | Text, high-dimensional |
| Correlation | 1 - r_xy | Pattern similarity |

### Clustering Algorithms

#### Hierarchical Agglomerative Clustering
**Process**:
1. Start with each sample as its own cluster
2. Find two closest samples/clusters
3. Merge them into new cluster
4. Recalculate distances between all clusters
5. Repeat until all merged into one

**Linkage Methods** (how to calculate cluster distances):

| Method | Distance Between Clusters | Properties |
|--------|--------------------------|------------|
| Ward.D | Minimize within-cluster variance | Compact clusters |
| Complete | Maximum distance between points | Tight, spherical clusters |
| Single | Minimum distance between points | Chain-like clusters |
| Average | Average distance between points | Balanced approach |

## Dendrogram Interpretation

### Structure
```
Height (distance)
  │
  │        ┌─── 1
  │    ┌───┤
  │    │   └─── 6
  │ ───┤
  │    │   ┌─── 2
  │    ├───┤
  │    │   └─── 3
  │    │
  │    │       ┌─── 4
  │    └───┬───┤
  │        │   └─── 5
  │
  └────────────────────────→ Samples
```

### Reading the Dendrogram
- **Height (y-axis)**: Distance at which clusters merge
- **Lower merge**: More similar samples
- **Higher merge**: Less similar samples
- **Horizontal lines**: Cluster boundaries

### Cutting the Tree
To get discrete clusters, draw horizontal line:

```
Height
  │
  │    Cluster A: {1, 6}
  │ ──┼────────────────  ← Cut here (k=3)
  │    Cluster B: {2, 3}
  │    Cluster C: {4, 5}
  │
  └────────────────────────
```

## Example: Spectral Data

### Problem Setup
24 samples measured at 16 wavelengths:
- Some contain Cu²⁺ only
- Some contain Cr³⁺ only  
- Some contain Co²⁺ only
- Some are binary mixtures
- Some are ternary mixtures

**Question**: Can we identify groupings without knowing compositions?

### Cluster Analysis Results
```
Dendrogram shows:
- Three main clusters emerge
- Within-cluster samples are more similar
- Between-cluster samples are less similar

Interpretation:
- Cluster 1: Cu²⁺-rich samples
- Cluster 2: Cr³⁺-rich samples  
- Cluster 3: Co²⁺-rich samples
```

### Spectral Interpretation
**Why it works**:
- Each metal ion has characteristic absorption spectrum
- Samples with same dominant ion have similar spectra
- Distance metric captures spectral similarity

## R Implementation

### Basic Clustering
```r
# Load data
spec_data <- read.csv("allSpec.csv", check.names = FALSE)

# Select subset
cluster_data <- spec_data[sample_ids, wavelength_ids]

# Calculate distances
cluster_dist <- dist(cluster_data, method = "euclidean")

# Perform hierarchical clustering
cluster_results <- hclust(cluster_dist, method = "ward.D")

# Plot dendrogram
plot(cluster_results, hang = -1, cex = 0.75)
```

### Enhanced Visualization
```r
# Add custom labels (e.g., Cu concentration)
cluster_copper <- spec_data$concCu / spec_data$concCu[1]
plot(cluster_results, hang = -1, 
     labels = cluster_copper[sample_ids],
     main = "Cluster Analysis",
     xlab = "Fraction of Cu stock",
     sub = "", cex = 0.75)

# Highlight clusters
rect.hclust(cluster_results, k = 3, 
            which = c(1,2,3), border = "blue")
```

### Clustering Variables (vs. Samples)
```r
# Transpose data to cluster wavelengths instead of samples
wavelength_dist <- dist(t(cluster_data))
wavelength_clust <- hclust(wavelength_dist, method = "ward.D")

plot(wavelength_clust, hang = -1,
     main = "Wavelength Clustering")

# Highlight wavelength groups
rect.hclust(wavelength_clust, k = 2, which = 2, border = "blue")
```

## Choosing Number of Clusters

### Methods
1. **Dendrogram inspection**: Look for large jumps in height
2. **Elbow method**: Plot within-cluster sum of squares vs. k
3. **Silhouette analysis**: Measure of cluster cohesion
4. **Domain knowledge**: How many groups expected?

### Visual Guide
```
Within-cluster SS
  │
  │*
  │ *
  │  *
  │   *
  │    *────  ← Elbow here
  │     *
  │      *
  └────────────→ k (number of clusters)
  1  2  3  4  5  6
```

## Applications in Chemistry

### 1. Sample Classification
**Environmental analysis**:
- Group water samples by contamination source
- Identify similar pollution patterns
- Track temporal changes

**Example**: NOx measurements
- Variables: temperature, day of week, wind, location
- Clusters reveal underlying factors
- Weekday vs. weekend patterns

### 2. Analyte Identification
**Spectroscopy**:
- Cluster samples by spectral similarity
- Identify pure component spectra
- Detect mixture compositions

### 3. Quality Control
**Manufacturing**:
- Group similar product batches
- Identify outliers
- Process monitoring

### 4. Metabolomics
**Biomarker discovery**:
- Cluster samples by metabolite profiles
- Identify disease subtypes
- Treatment response groups

## Comparison with PCA

| Aspect | Cluster Analysis | PCA |
|--------|-----------------|-----|
| Purpose | Grouping | Dimensionality reduction |
| Output | Dendrogram, clusters | Scores, loadings |
| Supervision | Unsupervised | Unsupervised |
| Visualization | Tree structure | Scatter plots |
| Interpretation | Similarity groups | Major variance sources |
| Complementary | Use together | Use together |

**Best practice**: Use both!
1. PCA for visualization and understanding major patterns
2. Cluster analysis for formal grouping
3. Compare results for validation

## Distance Matrix Analysis

### Viewing Distances
```r
# Print distance matrix (partial)
cluster_dist

# Heat map of distances
library(pheatmap)
pheatmap(as.matrix(cluster_dist))
```

### Interpreting Distance Matrix
- Small values = similar samples
- Large values = different samples
- Block structure = natural clustering

## Advanced Techniques

### K-Means Clustering
Alternative to hierarchical:
```r
kmeans_result <- kmeans(cluster_data, centers = 3)
```

**Pros**: Fast, works well with spherical clusters
**Cons**: Need to specify k, sensitive to initialization

### Density-Based Clustering (DBSCAN)
```r
library(dbscan)
dbscan_result <- dbscan(cluster_data, eps = 0.5, minPts = 5)
```

**Pros**: Finds arbitrary shapes, identifies outliers
**Cons**: Need to set parameters, may not work with varying densities

## Limitations and Considerations

### Challenges
1. **Choice of distance metric**: Different metrics give different results
2. **Choice of linkage**: Affects cluster shape and interpretation
3. **Number of clusters**: Often subjective
4. **Sensitivity to scaling**: Variables on different scales can dominate
5. **Noise and outliers**: Can distort clustering

### Best Practices
1. **Scale data appropriately**: Use scaling when variables have different units
2. **Try multiple methods**: Compare different distance/linkage combinations
3. **Validate clusters**: Use domain knowledge or external validation
4. **Visualize**: Always plot dendrogram and examine structure
5. **Consider PCA first**: Reduce dimensionality before clustering

## Decision Flow
1. Multivariate data with unknown structure? → Cluster analysis
2. Calculate distances (choose appropriate metric)
3. Perform hierarchical clustering (try Ward.D)
4. Visualize dendrogram
5. Identify natural number of clusters
6. Interpret in chemical context
7. Validate with known samples if available
8. Consider complementary PCA analysis

## Related Concepts
- [Principal Component Analysis](./principal_component_analysis.md) - Pattern recognition
- [Multivariate Regression](./multivariate_regression.md) - Quantitative prediction
- [Calibration Curves](./calibration_curves.md) - Univariate calibration
