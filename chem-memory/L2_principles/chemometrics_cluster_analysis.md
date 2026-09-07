---
id: chemometrics.cluster_analysis
layer: 2
title: Cluster Analysis in Chemistry
stability: high
confidence: high
last_verified: 2026-03-17
source: Chemometrics Using R (Harvey), Ch11.2
---

## Core Concepts

Cluster analysis groups samples based on similarity, revealing underlying structure in multivariate data without prior knowledge of group membership.

## How Cluster Analysis Works

### Hierarchical Clustering Algorithm

1. **Calculate distance matrix:**
   - Compute distances between all pairs of samples
   - Use distance metric (Euclidean, Manhattan, etc.)

2. **Find closest pair:**
   - Identify two samples with smallest distance

3. **Merge into cluster:**
   - Create new cluster from closest pair
   - Replace original points with cluster centroid

4. **Update distances:**
   - Recalculate distances to new cluster
   - Use linkage method (single, complete, average)

5. **Repeat:**
   - Continue until all samples in one cluster

## Distance Metrics

### Euclidean Distance

```
dij = √[Σ(xi,k - xj,k)²]
```

Most common for continuous variables.

### Manhattan Distance

```
dij = Σ|xi,k - xj,k|
```

More robust to outliers.

### Mahalanobis Distance

```
dij = √[(xi - xj)T S-1 (xi - xj)]
```

Accounts for covariance between variables.

**Formula:**
```
Mahalanobis distance = √[(xi - xj)T × S^(-1) × (xi - xj)]
```

Where S is the covariance matrix.

**Advantages:**
- Accounts for correlation between variables
- Scale-invariant
- Better for multivariate normal distributions

## Linkage Methods

### Single Linkage (Minimum Distance)

```
d(A,B) = min{d(a,b) : a ∈ A, b ∈ B}
```

- Tends to create long chains
- Sensitive to outliers

### Complete Linkage (Maximum Distance)

```
d(A,B) = max{d(a,b) : a ∈ A, b ∈ B}
```

- Creates compact, spherical clusters
- Less sensitive to outliers

### Average Linkage

```
d(A,B) = average{d(a,b) : a ∈ A, b ∈ B}
```

- Compromise between single and complete
- Often preferred

### Ward's Method

Minimizes within-cluster variance.

- Tends to create equal-sized clusters
- Good for quantitative data

## Dendrograms

### Interpretation

**Height (vertical axis):**
- Distance at which clusters merge
- Larger height = greater dissimilarity

**Branches:**
- Show cluster formation sequence
- Branch length indicates similarity

**Reading the dendrogram:**
- Samples that merge at low height are similar
- Large jumps in height suggest distinct clusters

### Determining Number of Clusters

1. **Visual inspection:**
   - Look for large gaps in height
   - Natural cluster breaks

2. **Cut dendrogram:**
   - Draw horizontal line
   - Number of intersections = number of clusters

3. **Elbow method:**
   - Plot within-cluster sum of squares vs. k
   - Find "elbow" point

## Data Preprocessing

### Standardization (Z-scores)

```
z = (x - x̄) / s
```

**When needed:**
- Variables on different scales
- Variables have different variances
- Essential for Euclidean distance

### Range Normalization

```
xnorm = (x - xmin) / (xmax - xmin)
```

Maps all values to [0, 1] range.

## K-Means Clustering

### Algorithm

1. Choose k (number of clusters)
2. Initialize k centroids randomly
3. Assign each point to nearest centroid
4. Recalculate centroids
5. Repeat steps 3-4 until convergence

### K-Means vs. Hierarchical

| Aspect | K-Means | Hierarchical |
|--------|---------|--------------|
| Speed | Faster | Slower |
| Clusters | Must specify k | Dendrogram shows structure |
| Shape | Spherical | Any shape |
| Outliers | Sensitive | Depends on linkage |

## Applications in Chemistry

### Spectral Classification
- Group similar spectra
- Identify sample types
- Detect outliers

### Pattern Recognition
- Identify compositional trends
- Classify samples by origin
- Detect adulteration

### Quality Control
- Identify batch similarities
- Detect process variations
- Cluster defective products

### Example: 24 Spectral Samples

**Data:** 24 samples measured at 635 wavelengths

**Analysis:**
1. Use 40 evenly-spaced wavelengths
2. Calculate Euclidean distance matrix
3. Apply hierarchical clustering (Ward's method)
4. Interpret dendrogram

**Result:** Three distinct clusters identified
- Suggests three analytes present
- Each cluster dominated by one analyte

## R Implementation

```r
# Hierarchical clustering
dist_matrix <- dist(data, method = "euclidean")
hc <- hclust(dist_matrix, method = "ward.D2")

# Plot dendrogram
plot(hc, main = "Cluster Dendrogram", xlab = "Sample", ylab = "Height")

# Cut dendrogram to get k clusters
clusters <- cutree(hc, k = 3)

# K-means clustering
km <- kmeans(data, centers = 3, nstart = 25)

# Add cluster assignments to data
data$cluster <- as.factor(km$cluster)

# Visualize clusters (for 2D data)
library(ggplot2)
ggplot(data, aes(x = var1, y = var2, color = cluster)) +
  geom_point()

# Determine optimal k (elbow method)
wss <- (nrow(data)-1) * sum(apply(data, 2, var))
for (i in 2:15) {
  wss[i] <- sum(kmeans(data, centers = i)$withinss)
}
plot(1:15, wss, type = "b")

# Standardize data first
data_scaled <- scale(data)

# Silhouette plot for cluster quality
library(cluster)
sil <- silhouette(clusters, dist_matrix)
plot(sil)
```

## Interpreting Cluster Results

### Questions to Ask

1. **How many clusters are appropriate?**
   - Examine dendrogram structure
   - Use silhouette analysis
   - Consider practical interpretation

2. **What do the clusters mean?**
   - Examine cluster centroids
   - Identify distinguishing features
   - Relate to chemical/physical properties

3. **Are there outliers?**
   - Single-point clusters
   - Late-joining points
   - Unusual spectral features

### Cluster Validation

**Internal validation:**
- Silhouette width
- Within-cluster sum of squares
- Between-cluster sum of squares

**External validation:**
- Compare to known groups
- Use for classification tasks

## Key Concepts Summary

| Concept | Description | Use Case |
|---------|-------------|----------|
| Distance metric | Measures sample similarity | Euclidean most common |
| Linkage method | Defines cluster distance | Ward's for quantitative |
| Dendrogram | Visualizes clustering hierarchy | Determine cluster count |
| K-means | Partitioning method | Large datasets, spherical clusters |
| Standardization | Scale variables to equal weight | Essential for different scales |

## Common Pitfalls

1. **Not standardizing data:** Variables with large values dominate
2. **Wrong distance metric:** Choose based on data type
3. **Ignoring preprocessing:** Outliers and missing data cause problems
4. **Over-interpreting clusters:** May not reflect true structure
5. **Choosing k arbitrarily:** Use validation methods

## Connection to Other Topics

- **PCA** (L2_principal_component_analysis.md): Reduce dimensions before clustering
- **Descriptive Statistics** (L2_descriptive_statistics.md): Calculate cluster centroids
- **Multivariate Regression** (L2_multivariate_regression.md): Use clusters as factors
- **Data Preprocessing** (L2_data_preprocessing.md): Standardization, outlier removal

## See Also

- Harvey, Chemometrics Using R, Chapter 11.2
- L3_code_examples/cluster_analysis_in_R.R
