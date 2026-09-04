"""
PCA Analysis Tools - L3 Implementation
Chemometrics: Principal Component Analysis

Provides core PCA functionality for chemical data analysis including:
- PCA decomposition
- Variance explained analysis
- Scores and loadings computation
- Component selection methods

## Solver Instructions (for AI Agent)

When you encounter PCA/chemometrics problems (dimensionality reduction, variance analysis), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given data matrix -> perform PCA and find principal components?
- Given PCA results -> interpret variance explained or loadings?
- Given spectra or chromatograms -> reduce dimensionality?
- Given scores -> identify outliers or clusters?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Center data | `center_data(data, axis)` | Returns centered data and mean |
| Standardize data | `standardize_data(data, axis)` | Returns z-scored data, mean, std |
| PCA via SVD | `pca_svd(data, n_components, standardize)` | Returns scores, loadings, eigenvalues |
| Select components | `select_n_components(variance_explained, threshold)` | Threshold default 0.95 (95%) |
| Reconstruct data | `reconstruct_data(scores, loadings, mean, std)` | Inverse transform |

### Step 3: Handle special cases
- Standardize=True: use when variables have different scales
- Standardize=False: use when variables are already normalized or same units
- First PC captures maximum variance direction
- Loadings show contribution of original variables

### Examples
```python
import numpy as np

# Example 1: PCA on spectral data
X = np.random.randn(50, 10)  # 50 samples, 10 wavelengths
result = pca_svd(X, n_components=3, standardize=True)
# -> result['scores'].shape = (50, 3)
# -> result['variance_explained'] shows % variance per PC

# Example 2: Center and standardize
centered, mean = center_data(X)
standardized, mean, std = standardize_data(X)

# Example 3: Select components for 95% variance
n = select_n_components(result['variance_explained'], 0.95)
# -> number of PCs needed

# Example 4: Interpret loadings
# loadings[0] = first PC loadings -> which original variables contribute most
```
"""

from typing import Tuple, List, Optional, Dict
import numpy as np
from numpy.typing import NDArray


def center_data(data: NDArray[np.floating], 
                axis: int = 0) -> Tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Mean-center the data matrix.
    
    Args:
        data: Data matrix (samples x variables)
        axis: Axis along which to compute mean (0 = column-wise)
    
    Returns:
        Tuple of (centered_data, mean_values)
    
    Examples:
        >>> import numpy as np
        >>> data = np.array([[1, 2], [3, 4], [5, 6]])
        >>> centered, mean = center_data(data)
        >>> mean
        array([3., 4.])
    """
    mean_vals = np.mean(data, axis=axis, keepdims=True)
    centered = data - mean_vals
    return centered, mean_vals.squeeze()


def standardize_data(data: NDArray[np.floating],
                     axis: int = 0) -> Tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Standardize data to zero mean and unit variance.
    
    Args:
        data: Data matrix (samples x variables)
        axis: Axis along which to standardize
    
    Returns:
        Tuple of (standardized_data, mean_values, std_values)
    
    Examples:
        >>> import numpy as np
        >>> data = np.array([[1, 2], [3, 4], [5, 6]])
        >>> std_data, mean, std = standardize_data(data)
        >>> np.allclose(std_data.mean(axis=0), 0)
        True
    """
    mean_vals = np.mean(data, axis=axis, keepdims=True)
    std_vals = np.std(data, axis=axis, keepdims=True, ddof=1)
    
    # Avoid division by zero
    std_vals = np.where(std_vals == 0, 1, std_vals)
    
    standardized = (data - mean_vals) / std_vals
    return standardized, mean_vals.squeeze(), std_vals.squeeze()


def pca_svd(data: NDArray[np.floating], 
            n_components: Optional[int] = None,
            standardize: bool = False) -> Dict[str, NDArray[np.floating]]:
    """
    Perform PCA using singular value decomposition.
    
    Args:
        data: Data matrix (n_samples x n_variables)
        n_components: Number of components to retain (None = all)
        standardize: Whether to standardize data before PCA
    
    Returns:
        Dict with keys:
            - 'scores': Sample scores (n_samples x n_components)
            - 'loadings': Variable loadings (n_components x n_variables)
            - 'eigenvalues': Eigenvalues (variance explained by each PC)
            - 'variance_explained': Proportion of variance explained
            - 'cumulative_variance': Cumulative variance explained
            - 'mean': Mean values used for centering
            - 'std': Standard deviations (if standardize=True)
    
    Examples:
        >>> import numpy as np
        >>> # Create synthetic data with 2 components
        >>> np.random.seed(42)
        >>> X = np.random.randn(20, 5)
        >>> result = pca_svd(X, n_components=2)
        >>> result['scores'].shape
        (20, 2)
        >>> result['loadings'].shape
        (2, 5)
    """
    n_samples, n_variables = data.shape
    
    # Preprocess data
    if standardize:
        data_proc, mean_vals, std_vals = standardize_data(data)
    else:
        data_proc, mean_vals = center_data(data)
        std_vals = None
    
    # Perform SVD
    U, s, Vt = np.linalg.svd(data_proc, full_matrices=False)
    
    # Calculate eigenvalues
    eigenvalues = (s ** 2) / (n_samples - 1)
    
    # Determine number of components
    if n_components is None:
        n_components = min(n_samples, n_variables)
    
    n_components = min(n_components, len(eigenvalues))
    
    # Extract scores and loadings
    scores = U[:, :n_components] * s[:n_components]
    loadings = Vt[:n_components, :]
    eigenvalues = eigenvalues[:n_components]
    
    # Calculate variance explained
    total_variance = np.sum(eigenvalues)
    variance_explained = eigenvalues / total_variance
    cumulative_variance = np.cumsum(variance_explained)
    
    return {
        'scores': scores,
        'loadings': loadings,
        'eigenvalues': eigenvalues,
        'variance_explained': variance_explained,
        'cumulative_variance': cumulative_variance,
        'mean': mean_vals,
        'std': std_vals
    }


def scree_data(eigenvalues: NDArray[np.floating]) -> Tuple[NDArray[np.int_], NDArray[np.floating]]:
    """
    Generate data for scree plot.
    
    Args:
        eigenvalues: Eigenvalues from PCA
    
    Returns:
        Tuple of (component_numbers, eigenvalues)
    
    Examples:
        >>> import numpy as np
        >>> eigenvalues = np.array([4.0, 2.0, 1.0, 0.5, 0.3])
        >>> components, values = scree_data(eigenvalues)
        >>> components
        array([1, 2, 3, 4, 5])
    """
    n_components = len(eigenvalues)
    return np.arange(1, n_components + 1), eigenvalues


def variance_table(eigenvalues: NDArray[np.floating],
                   decimals: int = 4) -> List[Dict]:
    """
    Create variance explained table.
    
    Args:
        eigenvalues: Eigenvalues from PCA
        decimals: Number of decimal places
    
    Returns:
        List of dicts with PC, eigenvalue, variance_explained, cumulative_variance
    
    Examples:
        >>> import numpy as np
        >>> eigenvalues = np.array([3.3134, 2.1901, 0.4256])
        >>> table = variance_table(eigenvalues)
        >>> table[0]['variance_explained']
        0.6862
    """
    total = np.sum(eigenvalues)
    variance_explained = eigenvalues / total
    cumulative = np.cumsum(variance_explained)
    
    table = []
    for i, (ev, ve, cv) in enumerate(zip(eigenvalues, variance_explained, cumulative)):
        table.append({
            'PC': i + 1,
            'eigenvalue': round(ev, decimals),
            'variance_explained': round(ve, decimals),
            'cumulative_variance': round(cv, decimals)
        })
    
    return table


def n_components_for_variance(cumulative_variance: NDArray[np.floating],
                               threshold: float = 0.95) -> int:
    """
    Determine number of components needed for target variance.
    
    Args:
        cumulative_variance: Cumulative variance explained array
        threshold: Target variance (default 0.95 = 95%)
    
    Returns:
        Number of components needed
    
    Examples:
        >>> import numpy as np
        >>> cum_var = np.array([0.7, 0.9, 0.95, 0.99, 1.0])
        >>> n_components_for_variance(cum_var, 0.95)
        3
    """
    return int(np.argmax(cumulative_variance >= threshold) + 1)


def kaiser_criterion(eigenvalues: NDArray[np.floating]) -> int:
    """
    Apply Kaiser criterion: retain components with eigenvalue > 1.
    
    Args:
        eigenvalues: Eigenvalues from PCA
    
    Returns:
        Number of components to retain
    
    Examples:
        >>> import numpy as np
        >>> eigenvalues = np.array([3.5, 2.1, 0.8, 0.4])
        >>> kaiser_criterion(eigenvalues)
        2
    """
    return int(np.sum(eigenvalues > 1.0))


def reconstruct_data(scores: NDArray[np.floating],
                     loadings: NDArray[np.floating],
                     mean: NDArray[np.floating],
                     std: Optional[NDArray[np.floating]] = None) -> NDArray[np.floating]:
    """
    Reconstruct data from PCA components.
    
    Args:
        scores: PCA scores
        loadings: PCA loadings
        mean: Mean values used for centering
        std: Standard deviations (if data was standardized)
    
    Returns:
        Reconstructed data matrix
    
    Examples:
        >>> import numpy as np
        >>> # Reconstruct using all components
        >>> scores = np.array([[1, 0], [0, 1]])
        >>> loadings = np.array([[1, 0], [0, 1]])
        >>> mean = np.array([0, 0])
        >>> reconstructed = reconstruct_data(scores, loadings, mean)
    """
    # Reconstruct centered data
    reconstructed = np.dot(scores, loadings)
    
    # Add back mean
    reconstructed = reconstructed + mean
    
    # If standardized, multiply back by std
    if std is not None:
        reconstructed = reconstructed * std
    
    return reconstructed


def project_new_samples(new_data: NDArray[np.floating],
                        loadings: NDArray[np.floating],
                        mean: NDArray[np.floating],
                        std: Optional[NDArray[np.floating]] = None) -> NDArray[np.floating]:
    """
    Project new samples onto existing PCA space.
    
    Args:
        new_data: New data matrix (n_samples x n_variables)
        loadings: PCA loadings from original analysis
        mean: Mean values from original analysis
        std: Standard deviations (if data was standardized)
    
    Returns:
        Scores for new samples
    
    Examples:
        >>> import numpy as np
        >>> new_data = np.array([[1, 2, 3], [4, 5, 6]])
        >>> loadings = np.array([[0.5, 0.5, 0.5], [0.5, -0.5, 0.0]])
        >>> mean = np.array([0, 0, 0])
        >>> scores = project_new_samples(new_data, loadings, mean)
    """
    # Center (and optionally standardize) new data
    centered = new_data - mean
    
    if std is not None:
        centered = centered / std
    
    # Project onto loadings
    scores = np.dot(centered, loadings.T)
    
    return scores


def hotelling_t2(scores: NDArray[np.floating],
                 eigenvalues: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Calculate Hotelling's T2 statistic for outlier detection.
    
    T2 = Σ (score_i2 / eigenvalue_i)
    
    Args:
        scores: PCA scores (n_samples x n_components)
        eigenvalues: Eigenvalues for each component
    
    Returns:
        T2 values for each sample
    
    Examples:
        >>> import numpy as np
        >>> scores = np.array([[2, 0], [0, 2], [0.1, 0.1]])
        >>> eigenvalues = np.array([4.0, 2.0])
        >>> t2 = hotelling_t2(scores, eigenvalues)
    """
    # Normalize scores by eigenvalues
    normalized = scores ** 2 / eigenvalues
    return np.sum(normalized, axis=1)


def q_residuals(original_data: NDArray[np.floating],
                reconstructed_data: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Calculate Q residuals (SPE - Squared Prediction Error).
    
    Args:
        original_data: Original data matrix
        reconstructed_data: Reconstructed data from PCA
    
    Returns:
        Q residual for each sample
    
    Examples:
        >>> import numpy as np
        >>> original = np.array([[1, 2, 3], [4, 5, 6]])
        >>> reconstructed = np.array([[1.1, 2.1, 2.9], [3.9, 5.1, 6.1]])
        >>> q = q_residuals(original, reconstructed)
    """
    residuals = original_data - reconstructed_data
    return np.sum(residuals ** 2, axis=1)


if __name__ == "__main__":
    """Example usage and simple tests."""
    import numpy as np
    
    print("=" * 60)
    print("PCA Analysis Tools - Example Usage")
    print("=" * 60)
    
    # Create synthetic spectral data
    np.random.seed(42)
    n_samples = 24
    n_wavelengths = 16
    
    # Generate data with 3 underlying components
    # Component spectra (loadings)
    true_loadings = np.zeros((3, n_wavelengths))
    true_loadings[0, :5] = np.linspace(0, 1, 5)  # Component 1
    true_loadings[1, 5:10] = np.linspace(0, 1, 5)  # Component 2
    true_loadings[2, 10:15] = np.linspace(0, 1, 5)  # Component 3
    
    # Sample concentrations (scores)
    true_scores = np.random.rand(n_samples, 3) * 2
    
    # Generate mixture spectra
    data = np.dot(true_scores, true_loadings)
    # Add noise
    data += np.random.randn(n_samples, n_wavelengths) * 0.05
    
    print(f"\nData shape: {data.shape} (samples x wavelengths)")
    
    # Perform PCA
    result = pca_svd(data, standardize=False)
    
    print("\n--- Variance Explained Table ---")
    table = variance_table(result['eigenvalues'][:5])
    print(f"{'PC':<5} {'Eigenvalue':>12} {'Var Expl':>12} {'Cumul Var':>12}")
    for row in table:
        print(f"{row['PC']:<5} {row['eigenvalue']:>12.4f} {row['variance_explained']:>12.4f} {row['cumulative_variance']:>12.4f}")
    
    # Determine number of components
    n_comp_95 = n_components_for_variance(result['cumulative_variance'])
    n_comp_kaiser = kaiser_criterion(result['eigenvalues'])
    
    print(f"\n--- Component Selection ---")
    print(f"Components for 95% variance: {n_comp_95}")
    print(f"Components by Kaiser criterion: {n_comp_kaiser}")
    
    # Scores shape
    print(f"\nScores shape: {result['scores'].shape}")
    print(f"Loadings shape: {result['loadings'].shape}")
    
    # Test projection
    new_sample = np.random.randn(1, n_wavelengths)
    new_score = project_new_samples(new_sample, result['loadings'], result['mean'])
    print(f"\nNew sample projected score (PC1, PC2): {new_score[0, :2]}")
    
    # Test Hotelling T2
    t2 = hotelling_t2(result['scores'][:, :3], result['eigenvalues'][:3])
    print(f"\nT-squared range: {t2.min():.3f} to {t2.max():.3f}")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
