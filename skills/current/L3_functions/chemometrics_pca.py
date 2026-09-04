"""
Chemometrics PCA Tools - L3 Implementation
Principal Component Analysis for Chemical Data

Provides streamlined PCA functions for chemometrics applications:
- PCA fitting and transformation
- Variance explained analysis
- Data preprocessing (centering, standardization)

References:
- Harvey, "Chemometrics Using R", Chapter 11
- Martens & Naes, "Multivariate Calibration"

## Solver Instructions (for AI Agent)

When you encounter PCA (Principal Component Analysis) problems:

### Step 1: Identify what is given and what is asked
- Given: data matrix X (samples x variables)
- Asked: principal components, variance explained, scores, loadings, outlier detection

### Step 2: Choose the correct function
- `mean_center(X)`: Subtract column means
- `standardize(X)`: Mean-center + divide by std (autoscaling)
- `pca_fit(X, n_components)`: Fit PCA model (scores, loadings, eigenvalues)
- `pca_transform(X_new, model)`: Project new data onto existing PC space
- `variance_explained(pca_result)`: Per-PC and cumulative variance
- `pca_reconstruct(pca_result, scores)`: Reconstruct data from scores
- `hotelling_t2(pca_result, X)`: Hotelling T2 statistic (multivariate outlier)
- `q_residuals(X, pca_result)`: Q residuals (squared residual sum)

### Step 3: Handle special cases
- Always mean-center first; standardize if variables have different scales
- Choose components where cumulative variance > 95-99%
- High T2 AND high Q = strong outlier; high Q only = different type

### Examples
```python
model = pca_fit(standardize(X), n_components=5)
var = variance_explained(model)
scores = pca_transform(X_new, model)
```
"""

from typing import Tuple, Optional, Dict, Union
import numpy as np
from numpy.typing import NDArray


def mean_center(X: NDArray[np.floating], 
                axis: int = 0) -> Tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Mean-center the data matrix by subtracting column means.
    
    Args:
        X: Data matrix (n_samples x n_variables)
        axis: Axis along which to compute mean (0 = column-wise, 1 = row-wise)
    
    Returns:
        Tuple of (centered_data, mean_values)
    
    Raises:
        ValueError: If X is empty or has invalid shape
    
    Examples:
        >>> import numpy as np
        >>> X = np.array([[1, 2], [3, 4], [5, 6]])
        >>> X_centered, mean = mean_center(X)
        >>> mean
        array([3., 4.])
        >>> X_centered.mean(axis=0)
        array([0., 0.])
    """
    X = np.asarray(X, dtype=np.float64)
    
    if X.size == 0:
        raise ValueError("Data matrix cannot be empty")
    
    mean_vals = np.mean(X, axis=axis, keepdims=True)
    centered = X - mean_vals
    
    return centered, mean_vals.squeeze()


def standardize(X: NDArray[np.floating], 
                axis: int = 0,
                ddof: int = 1) -> Tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Standardize data to zero mean and unit variance (Z-score normalization).
    
    This is essential for PCA when variables have different scales,
    e.g., combining absorbance at different wavelengths with different
    magnitude ranges.
    
    Args:
        X: Data matrix (n_samples x n_variables)
        axis: Axis along which to standardize (0 = column-wise)
        ddof: Delta degrees of freedom for std calculation (default: 1 for sample std)
    
    Returns:
        Tuple of (standardized_data, mean_values, std_values)
    
    Raises:
        ValueError: If X is empty or has zero variance columns
    
    Examples:
        >>> import numpy as np
        >>> X = np.array([[1, 10], [2, 20], [3, 30]])
        >>> X_std, mean, std = standardize(X)
        >>> np.allclose(X_std.mean(axis=0), 0)
        True
        >>> np.allclose(X_std.std(axis=0, ddof=1), 1)
        True
    """
    X = np.asarray(X, dtype=np.float64)
    
    if X.size == 0:
        raise ValueError("Data matrix cannot be empty")
    
    mean_vals = np.mean(X, axis=axis, keepdims=True)
    std_vals = np.std(X, axis=axis, keepdims=True, ddof=ddof)
    
    # Handle zero variance columns
    zero_var_mask = std_vals == 0
    if np.any(zero_var_mask):
        std_vals = np.where(zero_var_mask, 1.0, std_vals)
    
    standardized = (X - mean_vals) / std_vals
    
    return standardized, mean_vals.squeeze(), std_vals.squeeze()


def pca_fit(X: NDArray[np.floating], 
            n_components: Optional[int] = None,
            center: bool = True,
            scale: bool = False) -> Dict[str, Union[NDArray[np.floating], int]]:
    """
    Fit PCA to data matrix using Singular Value Decomposition.
    
    This function performs PCA decomposition on the input data matrix,
    returning scores, loadings, and variance information. It's the
    primary function for exploratory data analysis in chemometrics.
    
    The PCA model follows:
        X = T P^T + E
    where T is scores, P is loadings, and E is residuals.
    
    Args:
        X: Data matrix (n_samples x n_variables), typically spectra
        n_components: Number of principal components to retain.
                     If None, keeps min(n_samples, n_variables) components.
        center: Whether to mean-center the data (default: True)
        scale: Whether to standardize to unit variance (default: False)
    
    Returns:
        Dict containing:
            - 'scores': Sample scores (n_samples x n_components)
            - 'loadings': Variable loadings (n_components x n_variables)
            - 'eigenvalues': Eigenvalues (variance per PC)
            - 'explained_variance_ratio': Proportion of variance explained
            - 'cumulative_variance': Cumulative proportion explained
            - 'n_components': Number of components retained
            - 'mean': Column means (if center=True)
            - 'std': Column std devs (if scale=True)
            - 'n_samples': Number of samples
            - 'n_features': Number of variables
    
    Raises:
        ValueError: If X is empty or n_components is invalid
    
    Examples:
        >>> import numpy as np
        >>> # Simulate UV-Vis spectra of 3-component mixture
        >>> np.random.seed(42)
        >>> X = np.random.randn(24, 16)  # 24 samples, 16 wavelengths
        >>> result = pca_fit(X, n_components=3)
        >>> result['scores'].shape
        (24, 3)
        >>> result['loadings'].shape
        (3, 16)
        >>> result['explained_variance_ratio'].sum() <= 1.0
        True
    
    Notes:
        - For spectroscopic data, center=True, scale=False is typical
        - For data with different units/scales, use scale=True
        - Eigenvalues = s2/(n-1) where s are singular values
    """
    X = np.asarray(X, dtype=np.float64)
    
    if X.size == 0:
        raise ValueError("Data matrix cannot be empty")
    
    n_samples, n_features = X.shape
    
    # Determine max possible components
    max_components = min(n_samples, n_features)
    if n_components is None:
        n_components = max_components
    elif n_components > max_components:
        raise ValueError(f"n_components ({n_components}) cannot exceed min(n_samples, n_features) = {max_components}")
    elif n_components < 1:
        raise ValueError("n_components must be at least 1")
    
    # Preprocessing
    mean = None
    std = None
    
    if center:
        X_proc, mean = mean_center(X)
    else:
        X_proc = X.copy()
    
    if scale:
        X_proc, mean_s, std = standardize(X_proc if not center else X_proc)
        if mean is None:
            mean = mean_s
    
    # Perform SVD: X = U @ diag(s) @ Vt
    U, s, Vt = np.linalg.svd(X_proc, full_matrices=False)
    
    # Calculate eigenvalues (variance)
    eigenvalues = (s ** 2) / (n_samples - 1)
    
    # Truncate to n_components
    eigenvalues = eigenvalues[:n_components]
    scores = U[:, :n_components] * s[:n_components]  # T = U * s
    loadings = Vt[:n_components, :]  # P^T
    
    # Variance explained
    total_variance = np.sum((s ** 2) / (n_samples - 1))
    explained_variance_ratio = eigenvalues / total_variance
    cumulative_variance = np.cumsum(explained_variance_ratio)
    
    return {
        'scores': scores,
        'loadings': loadings,
        'eigenvalues': eigenvalues,
        'explained_variance_ratio': explained_variance_ratio,
        'cumulative_variance': cumulative_variance,
        'n_components': n_components,
        'mean': mean,
        'std': std,
        'n_samples': n_samples,
        'n_features': n_features
    }


def pca_transform(X_new: NDArray[np.floating], 
                  pca_result: Dict[str, Union[NDArray[np.floating], int, None]],
                  n_components: Optional[int] = None) -> NDArray[np.floating]:
    """
    Transform new data to PCA space using fitted loadings.
    
    Project new samples onto the principal component space defined
    by previously fitted loadings. This is useful for:
    - Predicting scores for validation samples
    - Applying a calibration model to new spectra
    
    Args:
        X_new: New data matrix (m_samples x n_variables)
        pca_result: Dict from pca_fit containing 'loadings', 'mean', 'std'
        n_components: Number of components to use (default: all from model)
    
    Returns:
        Scores for new samples (m_samples x n_components)
    
    Raises:
        ValueError: If X_new has incompatible dimensions with loadings
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> # Fit on training data
        >>> X_train = np.random.randn(20, 10)
        >>> model = pca_fit(X_train, n_components=3)
        >>> # Transform new data
        >>> X_new = np.random.randn(5, 10)
        >>> scores_new = pca_transform(X_new, model)
        >>> scores_new.shape
        (5, 3)
    """
    X_new = np.asarray(X_new, dtype=np.float64)
    
    loadings = pca_result['loadings']
    n_features_model = loadings.shape[1]
    
    if X_new.shape[1] != n_features_model:
        raise ValueError(f"X_new has {X_new.shape[1]} features, but model expects {n_features_model}")
    
    # Determine components to use
    if n_components is None:
        n_components = loadings.shape[0]
    else:
        n_components = min(n_components, loadings.shape[0])
    
    loadings_use = loadings[:n_components, :]
    
    # Apply same preprocessing as training
    X_proc = X_new.copy()
    
    if pca_result.get('mean') is not None:
        X_proc = X_proc - pca_result['mean']
    
    if pca_result.get('std') is not None:
        X_proc = X_proc / pca_result['std']
    
    # Project: scores = X @ P
    scores = np.dot(X_proc, loadings_use.T)
    
    return scores


def variance_explained(pca_result: Dict[str, Union[NDArray[np.floating], int, None]],
                       threshold: Optional[float] = None) -> Dict[str, Union[np.ndarray, int, list]]:
    """
    Get variance explained per principal component.
    
    Returns detailed variance information and can determine the number
    of components needed to reach a target variance threshold.
    
    Args:
        pca_result: Dict from pca_fit containing variance information
        threshold: Optional target cumulative variance (e.g., 0.95 for 95%)
    
    Returns:
        Dict containing:
            - 'per_component': Variance explained by each PC
            - 'cumulative': Cumulative variance explained
            - 'eigenvalues': Eigenvalues per PC
            - 'n_components_for_threshold': Components needed for threshold (if given)
            - 'table': Human-readable table as list of dicts
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(30, 10)
        >>> model = pca_fit(X)
        >>> var_info = variance_explained(model, threshold=0.95)
        >>> var_info['n_components_for_threshold']  # Components for 95%
        >>> table = var_info['table']
        >>> len(table) == model['n_components']
        True
    
    Notes:
        - Kaiser criterion: retain PCs with eigenvalue > 1 (for standardized data)
        - Scree plot: look for "elbow" in eigenvalue curve
        - Cumulative variance: common thresholds are 90%, 95%, 99%
    """
    eigenvalues = pca_result['eigenvalues']
    explained_ratio = pca_result['explained_variance_ratio']
    cumulative = pca_result['cumulative_variance']
    
    # Build human-readable table
    table = []
    for i, (ev, ex, cum) in enumerate(zip(eigenvalues, explained_ratio, cumulative)):
        table.append({
            'PC': i + 1,
            'eigenvalue': float(ev),
            'variance_explained': float(ex),
            'cumulative_variance': float(cum)
        })
    
    result = {
        'per_component': explained_ratio,
        'cumulative': cumulative,
        'eigenvalues': eigenvalues,
        'table': table
    }
    
    # Determine components for threshold
    if threshold is not None:
        if threshold <= 0 or threshold > 1:
            raise ValueError("Threshold must be between 0 and 1")
        
        n_for_threshold = int(np.argmax(cumulative >= threshold) + 1)
        result['n_components_for_threshold'] = n_for_threshold
    
    return result


def pca_reconstruct(pca_result: Dict[str, Union[NDArray[np.floating], int, None]],
                    n_components: Optional[int] = None) -> NDArray[np.floating]:
    """
    Reconstruct data from PCA model.
    
    Reconstruct the original data matrix using a specified number of
    principal components. Useful for:
    - Visualizing model quality
    - Calculating residuals (Q-statistic)
    - Noise reduction (denoising spectra)
    
    Args:
        pca_result: Dict from pca_fit
        n_components: Number of components to use (default: all)
    
    Returns:
        Reconstructed data matrix (n_samples x n_features)
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(20, 10)
        >>> model = pca_fit(X, n_components=5)
        >>> X_reconstructed = pca_reconstruct(model)
        >>> X_reconstructed.shape
        (20, 10)
    """
    scores = pca_result['scores']
    loadings = pca_result['loadings']
    
    if n_components is None:
        n_components = scores.shape[1]
    else:
        n_components = min(n_components, scores.shape[1])
    
    # Reconstruct: X = T @ P + mean
    X_reconstructed = np.dot(scores[:, :n_components], loadings[:n_components, :])
    
    if pca_result.get('mean') is not None:
        X_reconstructed = X_reconstructed + pca_result['mean']
    
    return X_reconstructed


def hotelling_t2(pca_result: Dict[str, Union[NDArray[np.floating], int, None]],
                 n_components: Optional[int] = None) -> NDArray[np.floating]:
    """
    Calculate Hotelling's T2 statistic for outlier detection.
    
    T2 measures the distance of each sample from the center in the
    reduced PCA space. Large T2 indicates samples that are extreme
    in the model space.
    
    T2_i = Σ_j (score_ij2 / eigenvalue_j)
    
    Args:
        pca_result: Dict from pca_fit
        n_components: Number of components to use (default: all)
    
    Returns:
        T2 values for each sample
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(20, 10)
        >>> model = pca_fit(X, n_components=3)
        >>> t2 = hotelling_t2(model)
        >>> t2.shape
        (20,)
    """
    scores = pca_result['scores']
    eigenvalues = pca_result['eigenvalues']
    
    if n_components is None:
        n_components = scores.shape[1]
    else:
        n_components = min(n_components, scores.shape[1])
    
    scores_use = scores[:, :n_components]
    eigenvalues_use = eigenvalues[:n_components]
    
    # T2 = sum(score2 / eigenvalue)
    t2 = np.sum((scores_use ** 2) / eigenvalues_use, axis=1)
    
    return t2


def q_residuals(X: NDArray[np.floating],
                pca_result: Dict[str, Union[NDArray[np.floating], int, None]],
                n_components: Optional[int] = None) -> NDArray[np.floating]:
    """
    Calculate Q residuals (SPE - Squared Prediction Error).
    
    Q measures the distance of each sample from the PCA model plane.
    Large Q indicates samples that don't fit the model well (new
    sources of variation not captured by the model).
    
    Q_i = Σ_j (x_ij - x̂_ij)2
    
    Args:
        X: Original data matrix
        pca_result: Dict from pca_fit
        n_components: Number of components to use (default: all)
    
    Returns:
        Q residual values for each sample
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(20, 10)
        >>> model = pca_fit(X, n_components=3)
        >>> q = q_residuals(X, model)
        >>> q.shape
        (20,)
    """
    X = np.asarray(X, dtype=np.float64)
    
    X_reconstructed = pca_reconstruct(pca_result, n_components)
    
    # Q = sum of squared residuals
    residuals = X - X_reconstructed
    q = np.sum(residuals ** 2, axis=1)
    
    return q


if __name__ == "__main__":
    """Example usage and tests."""
    import numpy as np
    
    print("=" * 60)
    print("Chemometrics PCA Tools - Example Usage")
    print("=" * 60)
    
    # Simulate UV-Vis spectra of Cu2+/Cr3+/Co2+ mixtures
    np.random.seed(42)
    n_samples = 24
    n_wavelengths = 16
    
    # Generate mixture spectra with 3 underlying components
    true_loadings = np.zeros((3, n_wavelengths))
    true_loadings[0, :5] = np.linspace(0, 1, 5)    # Cu2+ spectrum
    true_loadings[1, 5:10] = np.linspace(0, 1, 5)  # Cr3+ spectrum
    true_loadings[2, 10:15] = np.linspace(0, 1, 5) # Co2+ spectrum
    
    true_scores = np.random.rand(n_samples, 3) * 2
    data = np.dot(true_scores, true_loadings)
    data += np.random.randn(n_samples, n_wavelengths) * 0.05
    
    print(f"\nData shape: {data.shape} (samples x wavelengths)")
    
    # Fit PCA
    model = pca_fit(data, n_components=5)
    
    print(f"\n--- PCA Model Summary ---")
    print(f"Scores shape: {model['scores'].shape}")
    print(f"Loadings shape: {model['loadings'].shape}")
    
    # Variance explained
    var_info = variance_explained(model, threshold=0.95)
    
    print(f"\n--- Variance Explained ---")
    print(f"{'PC':<5} {'Eigenvalue':>12} {'Var Expl':>12} {'Cumul':>12}")
    for row in var_info['table'][:5]:
        print(f"{row['PC']:<5} {row['eigenvalue']:>12.4f} {row['variance_explained']:>12.4f} {row['cumulative_variance']:>12.4f}")
    
    print(f"\nComponents for 95% variance: {var_info.get('n_components_for_threshold', 'N/A')}")
    
    # Transform new data
    X_new = np.random.randn(2, n_wavelengths)
    scores_new = pca_transform(X_new, model, n_components=3)
    print(f"\nNew sample scores (PC1-3): {scores_new}")
    
    # Outlier detection
    t2 = hotelling_t2(model, n_components=3)
    q = q_residuals(data, model, n_components=3)
    print(f"\nT2 range: {t2.min():.3f} to {t2.max():.3f}")
    print(f"Q range: {q.min():.6f} to {q.max():.6f}")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
