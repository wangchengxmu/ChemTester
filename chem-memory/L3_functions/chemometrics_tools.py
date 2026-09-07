"""
Chemometrics Tools - L3 Implementation
======================================

Python functions for chemometric analysis including:
- Principal Component Analysis (PCA)
- Partial Least Squares (PLS)
- Multivariate Calibration (CLS, PCR)
- Data Preprocessing

Based on: Chemometrics Using R (Harvey)

Dependencies: numpy, scipy, scikit-learn

Author: Chem-Memory Pass-3 Builder
Date: 2026-03-18
"""
## Solver Instructions (for AI Agent)

# When you encounter chemometrics problems (PCA, PLS, calibration, preprocessing), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: spectral/data matrices (X, Y), preprocessing needs, model type
# - **Asked**: principal components, predictions, calibration model, variance explained, outliers

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Mean-centering | `mean_center(data, axis=0)` | data matrix |
# | Standardize | `standardize(data, axis=0)` | data matrix |
# | SNV transform | `snv(data)` | spectra matrix |
# | MSC correction | `msc(data, reference)` | spectra, optional ref |
# | PCA fit | `pca_fit(data, n_components, center, scale)` | data, n_comp |
# | PCA transform | `pca_transform(data, model)` | new data, fitted model |
# | Variance explained | `variance_explained(model, cumulative)` | PCA model |
# | PLS fit | `pls_fit(X, Y, n_components)` | predictor, response |
# | PLS predict | `pls_predict(X, model)` | new X, PLS model |
# | CLS calibration | `cls_calibration(A, C)` | absorbance, concentrations |
# | PCR fit | `pcr_fit(X, Y, n_components)` | predictor, response |
# | Cross-validation | `cross_validate(X, Y, method, max_components)` | data, method |
# | RMSEC/RMSEP | `rmsec_rmsep(Y_true, Y_pred, type)` | true vs predicted |
# | Descriptive stats | `descriptive_stats(data, axis)` | data matrix |
# | Hypothesis test | `hypothesis_test(sample1, sample2, test)` | samples, test type |
# | Outlier detection | `outlier_detection(model, residuals)` | model, residuals |

### Step 3: Handle special cases
# - For spectral data: use `center=True, scale=False` for PCA
# - For mixed-unit data: use `standardize` before PCA
# - Apply `snv` or `msc` before mean-centering for NIR spectra
# - Use `cross_validate` to choose optimal n_components for PLS/PCR

### Examples
# 1. **PCA**: `model = pca_fit(X, n_components=3); var = variance_explained(model, cumulative=True)` -> find 95% variance cutoff
# 2. **PLS**: `model = pls_fit(X_train, Y_train, n_components=5); Y_pred = pls_predict(X_test, model)`
# 3. **Cross-validation**: `cross_validate(X, Y, method='pls', max_components=10)` -> optimal_components


import numpy as np
from scipy import stats
from typing import Tuple, Dict, Optional, Union, List

# Try to import sklearn components
try:
    from sklearn.decomposition import PCA as sklearnPCA
    from sklearn.cross_decomposition import PLSRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score, KFold
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# =============================================================================
# PREPROCESSING FUNCTIONS
# =============================================================================

def mean_center(data: np.ndarray, axis: int = 0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Mean-center data by subtracting column (or row) means.
    
    Parameters
    ----------
    data : np.ndarray
        Input data matrix (samples x variables)
    axis : int
        Axis along which to center (0=columns, 1=rows)
    
    Returns
    -------
    centered : np.ndarray
        Mean-centered data
    means : np.ndarray
        Mean values subtracted
    
    Examples
    --------
    >>> X = np.array([[1, 2], [3, 4], [5, 6]])
    >>> Xc, means = mean_center(X)
    >>> means
    array([3., 4.])
    
    Notes
    -----
    Mean centering is essential for PCA as it ensures the first principal
    component passes through the centroid of the data.
    """
    means = np.mean(data, axis=axis, keepdims=True)
    centered = data - means
    return centered, means.flatten()


def standardize(data: np.ndarray, axis: int = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Z-score standardization: center and scale to unit variance.
    
    Parameters
    ----------
    data : np.ndarray
        Input data matrix
    axis : int
        Axis along which to standardize
    
    Returns
    -------
    standardized : np.ndarray
        Standardized data (mean=0, std=1)
    means : np.ndarray
        Column/row means
    stds : np.ndarray
        Column/row standard deviations
    
    Examples
    --------
    >>> X = np.array([[1, 2], [3, 4], [5, 6]])
    >>> Xs, means, stds = standardize(X)
    
    Notes
    -----
    Use standardization when variables have different units or scales.
    For spectroscopic data, mean-centering alone is often sufficient.
    """
    means = np.mean(data, axis=axis, keepdims=True)
    stds = np.std(data, axis=axis, keepdims=True, ddof=1)
    
    # Avoid division by zero
    stds = np.where(stds == 0, 1, stds)
    
    standardized = (data - means) / stds
    return standardized, means.flatten(), stds.flatten()


def snv(data: np.ndarray) -> np.ndarray:
    """
    Standard Normal Variate (SNV) transformation.
    
    Each spectrum is standardized independently (row-wise).
    Common preprocessing for NIR spectroscopy.
    
    Parameters
    ----------
    data : np.ndarray
        Spectral data (samples x wavelengths)
    
    Returns
    -------
    snv_data : np.ndarray
        SNV-transformed spectra
    
    Notes
    -----
    SNV removes scatter effects and baseline variations.
    Apply before mean-centering for PCA of spectral data.
    """
    means = np.mean(data, axis=1, keepdims=True)
    stds = np.std(data, axis=1, keepdims=True, ddof=1)
    stds = np.where(stds == 0, 1, stds)
    return (data - means) / stds


def msc(data: np.ndarray, reference: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Multiplicative Scatter Correction (MSC).
    
    Corrects for scatter effects in spectroscopic data.
    
    Parameters
    ----------
    data : np.ndarray
        Spectral data (samples x wavelengths)
    reference : np.ndarray, optional
        Reference spectrum (default: mean spectrum)
    
    Returns
    -------
    corrected : np.ndarray
        MSC-corrected spectra
    reference : np.ndarray
        Reference spectrum used
    
    Notes
    -----
    MSC fits each spectrum to the reference using linear regression,
    then corrects for additive and multiplicative effects.
    """
    if reference is None:
        reference = np.mean(data, axis=0)
    
    corrected = np.zeros_like(data)
    
    for i in range(data.shape[0]):
        # Linear fit: spectrum = a + b * reference
        coeffs = np.polyfit(reference, data[i, :], 1)
        corrected[i, :] = (data[i, :] - coeffs[1]) / coeffs[0]
    
    return corrected, reference


# =============================================================================
# PRINCIPAL COMPONENT ANALYSIS (PCA)
# =============================================================================

def pca_fit(data: np.ndarray, 
            n_components: Optional[int] = None,
            center: bool = True,
            scale: bool = False) -> Dict:
    """
    Fit a PCA model to data.
    
    Parameters
    ----------
    data : np.ndarray
        Input data matrix (samples x variables)
    n_components : int, optional
        Number of components to retain (default: all)
    center : bool
        Whether to mean-center the data
    scale : bool
        Whether to standardize variables
    
    Returns
    -------
    model : dict
        PCA model containing:
        - scores : np.ndarray (samples x n_components)
        - loadings : np.ndarray (variables x n_components)
        - explained_variance : np.ndarray
        - explained_variance_ratio : np.ndarray
        - singular_values : np.ndarray
        - mean : np.ndarray
        - scale : np.ndarray (if scale=True)
    
    Examples
    --------
    >>> X = np.random.randn(50, 10)
    >>> model = pca_fit(X, n_components=3)
    >>> model['explained_variance_ratio']
    array([...])
    
    Notes
    -----
    PCA finds orthogonal directions of maximum variance.
    For spectral data, use center=True, scale=False.
    """
    n_samples, n_vars = data.shape
    
    # Preprocessing
    if center:
        data_centered, mean = mean_center(data, axis=0)
    else:
        data_centered = data.copy()
        mean = np.zeros(n_vars)
    
    if scale:
        data_processed, _, scale_vals = standardize(data_centered, axis=0)
    else:
        data_processed = data_centered
        scale_vals = np.ones(n_vars)
    
    # Set default number of components
    if n_components is None:
        n_components = min(n_samples, n_vars)
    
    # SVD decomposition
    U, S, Vt = np.linalg.svd(data_processed, full_matrices=False)
    
    # Limit to n_components
    U = U[:, :n_components]
    S = S[:n_components]
    Vt = Vt[:n_components, :]
    
    # Calculate scores and loadings
    scores = U * S  # T = U * S
    loadings = Vt.T  # P = V^T
    
    # Explained variance
    total_var = np.sum(S ** 2)
    explained_variance = (S ** 2) / (n_samples - 1)
    explained_variance_ratio = explained_variance / np.sum(explained_variance)
    
    return {
        'scores': scores,
        'loadings': loadings,
        'explained_variance': explained_variance,
        'explained_variance_ratio': explained_variance_ratio,
        'singular_values': S,
        'mean': mean,
        'scale': scale_vals,
        'n_components': n_components,
        'n_samples': n_samples,
        'n_variables': n_vars
    }


def pca_transform(data: np.ndarray, model: Dict) -> np.ndarray:
    """
    Transform new data using fitted PCA model.
    
    Parameters
    ----------
    data : np.ndarray
        New data to transform (samples x variables)
    model : dict
        Fitted PCA model from pca_fit()
    
    Returns
    -------
    scores : np.ndarray
        Scores for new samples
    
    Examples
    --------
    >>> model = pca_fit(X_train, n_components=3)
    >>> X_test_scores = pca_transform(X_test, model)
    """
    # Center and scale using model parameters
    data_centered = data - model['mean']
    
    if not np.allclose(model['scale'], 1.0):
        data_centered = data_centered / model['scale']
    
    # Project onto loadings
    scores = data_centered @ model['loadings']
    
    return scores


def variance_explained(model: Dict, 
                       cumulative: bool = False) -> np.ndarray:
    """
    Get variance explained by each principal component.
    
    Parameters
    ----------
    model : dict
        Fitted PCA model
    cumulative : bool
        Return cumulative variance
    
    Returns
    -------
    variance : np.ndarray
        Variance explained (individual or cumulative)
    
    Examples
    --------
    >>> model = pca_fit(X)
    >>> cum_var = variance_explained(model, cumulative=True)
    >>> # Find components for 95% variance
    >>> n_comp = np.argmax(cum_var >= 0.95) + 1
    """
    if cumulative:
        return np.cumsum(model['explained_variance_ratio'])
    return model['explained_variance_ratio']


def scree_plot_data(model: Dict) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate data for scree plot.
    
    Parameters
    ----------
    model : dict
        Fitted PCA model
    
    Returns
    -------
    components : np.ndarray
        Component numbers (1, 2, 3, ...)
    variance : np.ndarray
        Variance explained by each component
    
    Examples
    --------
    >>> model = pca_fit(X)
    >>> comp_nums, var = scree_plot_data(model)
    >>> # Plot: plt.plot(comp_nums, var, 'o-')
    """
    components = np.arange(1, model['n_components'] + 1)
    variance = model['explained_variance_ratio'] * 100  # As percentage
    return components, variance


def scores_loadings(model: Dict) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract scores and loadings from PCA model.
    
    Parameters
    ----------
    model : dict
        Fitted PCA model
    
    Returns
    -------
    scores : np.ndarray
        Sample scores
    loadings : np.ndarray
        Variable loadings
    
    Notes
    -----
    Scores show sample positions in PC space.
    Loadings show variable contributions to each PC.
    """
    return model['scores'], model['loadings']


def biplot_data(model: Dict, 
                pc_x: int = 1, 
                pc_y: int = 2,
                loading_scale: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prepare coordinates for a biplot.
    
    Parameters
    ----------
    model : dict
        Fitted PCA model
    pc_x : int
        Principal component for x-axis (1-indexed)
    pc_y : int
        Principal component for y-axis (1-indexed)
    loading_scale : float
        Scale factor for loading vectors
    
    Returns
    -------
    scores_xy : np.ndarray
        Score coordinates (n_samples, 2)
    loadings_xy : np.ndarray
        Loading vectors (n_variables, 2)
    
    Examples
    --------
    >>> model = pca_fit(X)
    >>> scores_xy, loadings_xy = biplot_data(model, pc_x=1, pc_y=2)
    >>> # Plot scores as points, loadings as arrows
    """
    i_x = pc_x - 1  # Convert to 0-indexed
    i_y = pc_y - 1
    
    scores_xy = model['scores'][:, [i_x, i_y]]
    loadings_xy = model['loadings'][:, [i_x, i_y]] * loading_scale
    
    return scores_xy, loadings_xy


# =============================================================================
# PARTIAL LEAST SQUARES (PLS)
# =============================================================================

def pls_fit(X: np.ndarray, 
            Y: np.ndarray,
            n_components: int = 2,
            center: bool = True,
            scale: bool = False) -> Dict:
    """
    Fit a PLS regression model.
    
    Parameters
    ----------
    X : np.ndarray
        Predictor matrix (samples x variables)
    Y : np.ndarray
        Response matrix (samples x responses)
    n_components : int
        Number of latent variables
    center : bool
        Mean-center X and Y
    scale : bool
        Standardize X and Y
    
    Returns
    -------
    model : dict
        PLS model containing:
        - X_scores : np.ndarray (T)
        - X_loadings : np.ndarray (P)
        - Y_scores : np.ndarray (U)
        - Y_loadings : np.ndarray (Q)
        - weights : np.ndarray (W)
        - coefficients : np.ndarray (B)
        - X_mean, Y_mean : np.ndarray
        - X_scale, Y_scale : np.ndarray
    
    Examples
    --------
    >>> X = np.random.randn(50, 10)
    >>> Y = np.random.randn(50, 1)
    >>> model = pls_fit(X, Y, n_components=3)
    
    Notes
    -----
    PLS finds latent variables that maximize covariance with Y.
    Use cross-validation to select optimal n_components.
    """
    n_samples, n_vars = X.shape
    n_responses = Y.shape[1] if Y.ndim > 1 else 1
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    
    # Preprocessing
    if center:
        Xc, X_mean = mean_center(X, axis=0)
        Yc, Y_mean = mean_center(Y, axis=0)
    else:
        Xc = X.copy()
        Yc = Y.copy()
        X_mean = np.zeros(n_vars)
        Y_mean = np.zeros(n_responses)
    
    if scale:
        Xc, _, X_scale = standardize(Xc, axis=0)
        Yc, _, Y_scale = standardize(Yc, axis=0)
    else:
        X_scale = np.ones(n_vars)
        Y_scale = np.ones(n_responses)
    
    # Use sklearn if available
    if SKLEARN_AVAILABLE:
        pls = PLSRegression(n_components=n_components, scale=False)
        pls.fit(Xc, Yc)
        
        return {
            'X_scores': pls.x_scores_,
            'X_loadings': pls.x_loadings_,
            'Y_scores': pls.y_scores_,
            'Y_loadings': pls.y_loadings_,
            'weights': pls.x_weights_,
            'coefficients': pls.coef_,
            'X_mean': X_mean,
            'Y_mean': Y_mean,
            'X_scale': X_scale,
            'Y_scale': Y_scale,
            'n_components': n_components,
            '_sklearn_model': pls
        }
    
    # Manual NIPALS implementation for PLS
    T = np.zeros((n_samples, n_components))
    P = np.zeros((n_vars, n_components))
    U = np.zeros((n_samples, n_components))
    Q = np.zeros((n_responses, n_components))
    W = np.zeros((n_vars, n_components))
    
    X_work = Xc.copy()
    Y_work = Yc.copy()
    
    for a in range(n_components):
        # Start with Y column with max variance
        y_var = np.var(Y_work, axis=0)
        u = Y_work[:, np.argmax(y_var)]
        
        for _ in range(100):  # Max iterations
            # X weights
            w = X_work.T @ u
            w = w / np.linalg.norm(w)
            
            # X scores
            t = X_work @ w
            
            # Y weights
            q = Y_work.T @ t
            q = q / (np.linalg.norm(q) + 1e-10)
            
            # Y scores
            u_new = Y_work @ q
            
            # Check convergence
            if np.linalg.norm(u_new - u) < 1e-10:
                break
            u = u_new
        
        # X loadings
        p = X_work.T @ t / (t.T @ t)
        
        # Deflation
        X_work = X_work - t.reshape(-1, 1) @ p.reshape(1, -1)
        Y_work = Y_work - t.reshape(-1, 1) @ q.reshape(1, -1)
        
        # Store
        T[:, a] = t
        P[:, a] = p
        U[:, a] = u
        Q[:, a] = q
        W[:, a] = w
    
    # Calculate regression coefficients
    R = W @ np.linalg.inv(P.T @ W)
    B = R @ Q.T
    
    return {
        'X_scores': T,
        'X_loadings': P,
        'Y_scores': U,
        'Y_loadings': Q,
        'weights': W,
        'coefficients': B,
        'X_mean': X_mean,
        'Y_mean': Y_mean,
        'X_scale': X_scale,
        'Y_scale': Y_scale,
        'n_components': n_components
    }


def pls_predict(X: np.ndarray, model: Dict) -> np.ndarray:
    """
    Predict Y values from X using fitted PLS model.
    
    Parameters
    ----------
    X : np.ndarray
        Predictor data (samples x variables)
    model : dict
        Fitted PLS model from pls_fit()
    
    Returns
    -------
    Y_pred : np.ndarray
        Predicted Y values
    
    Examples
    --------
    >>> model = pls_fit(X_train, Y_train, n_components=3)
    >>> Y_pred = pls_predict(X_test, model)
    """
    # Center and scale
    Xc = X - model['X_mean']
    if not np.allclose(model['X_scale'], 1.0):
        Xc = Xc / model['X_scale']
    
    # Predict
    Y_pred = Xc @ model['coefficients']
    
    # Add back Y mean
    Y_pred = Y_pred + model['Y_mean']
    
    # Rescale if needed
    if not np.allclose(model['Y_scale'], 1.0):
        Y_pred = Y_pred * model['Y_scale']
    
    return Y_pred


# =============================================================================
# CLASSICAL LEAST SQUARES (CLS) CALIBRATION
# =============================================================================

def cls_calibration(A: np.ndarray, C: np.ndarray) -> np.ndarray:
    """
    Classical Least Squares calibration (Beer's law approach).
    
    Determines molar absorptivities from known concentrations.
    
    Parameters
    ----------
    A : np.ndarray
        Absorbance matrix (samples x wavelengths)
    C : np.ndarray
        Concentration matrix (samples x analytes)
    
    Returns
    -------
    K : np.ndarray
        Molar absorptivity matrix (analytes x wavelengths)
    
    Examples
    --------
    >>> # 3 analytes, 10 wavelengths, 5 calibration samples
    >>> A = np.random.rand(5, 10)  # Absorbance
    >>> C = np.random.rand(5, 3)   # Concentrations
    >>> K = cls_calibration(A, C)  # Shape: (3, 10)
    
    Notes
    -----
    CLS assumes: A = C @ K
    Requires all analytes in mixture to be known.
    Solves: K = (C^T C)^{-1} C^T A
    """
    # Least squares solution: K = (C^T C)^{-1} C^T A
    K = np.linalg.lstsq(C, A, rcond=None)[0]
    return K


def cls_predict(A: np.ndarray, K: np.ndarray) -> np.ndarray:
    """
    Predict concentrations from absorbance using CLS.
    
    Parameters
    ----------
    A : np.ndarray
        Absorbance matrix (samples x wavelengths)
    K : np.ndarray
        Molar absorptivity matrix (analytes x wavelengths)
    
    Returns
    -------
    C : np.ndarray
        Predicted concentrations (samples x analytes)
    
    Notes
    -----
    Solves: C = A @ K^T @ (K @ K^T)^{-1}
    """
    C = np.linalg.lstsq(K.T, A.T, rcond=None)[0].T
    return C


# =============================================================================
# PRINCIPAL COMPONENT REGRESSION (PCR)
# =============================================================================

def pcr_fit(X: np.ndarray, 
            Y: np.ndarray,
            n_components: int = 2) -> Dict:
    """
    Principal Component Regression.
    
    Combines PCA dimensionality reduction with linear regression.
    
    Parameters
    ----------
    X : np.ndarray
        Predictor matrix (samples x variables)
    Y : np.ndarray
        Response matrix (samples x responses)
    n_components : int
        Number of principal components to use
    
    Returns
    -------
    model : dict
        PCR model containing PCA model and regression coefficients
    
    Notes
    -----
    PCR is simpler than PLS but may require more components
    to achieve the same predictive power.
    """
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    
    # PCA on X
    pca_model = pca_fit(X, n_components=n_components, center=True, scale=False)
    
    # Regress Y on scores
    scores = pca_model['scores']
    Y_centered = Y - np.mean(Y, axis=0)
    
    # Regression coefficients for scores
    B_scores = np.linalg.lstsq(scores, Y_centered, rcond=None)[0]
    
    # Convert to original variable coefficients
    B = pca_model['loadings'] @ B_scores
    
    return {
        'pca_model': pca_model,
        'B_scores': B_scores,
        'coefficients': B,
        'X_mean': pca_model['mean'],
        'Y_mean': np.mean(Y, axis=0),
        'n_components': n_components
    }


def pcr_predict(X: np.ndarray, model: Dict) -> np.ndarray:
    """
    Predict using PCR model.
    
    Parameters
    ----------
    X : np.ndarray
        Predictor data
    model : dict
        Fitted PCR model
    
    Returns
    -------
    Y_pred : np.ndarray
        Predictions
    """
    Xc = X - model['X_mean']
    Y_pred = Xc @ model['coefficients'] + model['Y_mean']
    return Y_pred


# =============================================================================
# CROSS-VALIDATION AND MODEL EVALUATION
# =============================================================================

def cross_validate(X: np.ndarray, 
                   Y: np.ndarray,
                   method: str = 'pls',
                   max_components: int = 10,
                   cv_folds: int = 5) -> Dict:
    """
    Cross-validation for component selection.
    
    Parameters
    ----------
    X : np.ndarray
        Predictor matrix
    Y : np.ndarray
        Response matrix
    method : str
        'pls' or 'pcr'
    max_components : int
        Maximum number of components to test
    cv_folds : int
        Number of cross-validation folds
    
    Returns
    -------
    results : dict
        - rmsecv : np.ndarray (RMSECV for each n_components)
        - optimal_components : int
        - optimal_rmsecv : float
    
    Examples
    --------
    >>> cv_result = cross_validate(X, Y, method='pls', max_components=10)
    >>> print(f"Optimal components: {cv_result['optimal_components']}")
    """
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    
    n_samples = X.shape[0]
    max_components = min(max_components, n_samples - 1, X.shape[1])
    
    rmsecv = np.zeros(max_components)
    kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42) if SKLEARN_AVAILABLE else None
    
    for n_comp in range(1, max_components + 1):
        fold_errors = []
        
        if kf is not None:
            for train_idx, test_idx in kf.split(X):
                X_train, X_test = X[train_idx], X[test_idx]
                Y_train, Y_test = Y[train_idx], Y[test_idx]
                
                if method == 'pls':
                    model = pls_fit(X_train, Y_train, n_components=n_comp)
                else:
                    model = pcr_fit(X_train, Y_train, n_components=n_comp)
                    model['coefficients'] = model['coefficients']
                
                if method == 'pls':
                    Y_pred = pls_predict(X_test, model)
                else:
                    Y_pred = pcr_predict(X_test, model)
                
                error = np.mean((Y_test - Y_pred) ** 2)
                fold_errors.append(error)
        else:
            # Simple LOO if sklearn not available
            for i in range(n_samples):
                mask = np.ones(n_samples, dtype=bool)
                mask[i] = False
                X_train, X_test = X[mask], X[~mask]
                Y_train, Y_test = Y[mask], Y[~mask]
                
                if method == 'pls':
                    model = pls_fit(X_train, Y_train, n_components=n_comp)
                    Y_pred = pls_predict(X_test, model)
                else:
                    model = pcr_fit(X_train, Y_train, n_components=n_comp)
                    Y_pred = pcr_predict(X_test, model)
                
                fold_errors.append(np.mean((Y_test - Y_pred) ** 2))
        
        rmsecv[n_comp - 1] = np.sqrt(np.mean(fold_errors))
    
    optimal_idx = np.argmin(rmsecv)
    
    return {
        'rmsecv': rmsecv,
        'n_components_tested': np.arange(1, max_components + 1),
        'optimal_components': optimal_idx + 1,
        'optimal_rmsecv': rmsecv[optimal_idx]
    }


def rmsec_rmsep(Y_true: np.ndarray, 
                Y_pred: np.ndarray,
                type: str = 'RMSEC') -> Dict:
    """
    Calculate calibration/prediction error metrics.
    
    Parameters
    ----------
    Y_true : np.ndarray
        True values
    Y_pred : np.ndarray
        Predicted values
    type : str
        'RMSEC' (calibration) or 'RMSEP' (prediction)
    
    Returns
    -------
    metrics : dict
        - rmse : Root mean squared error
        - r2 : R-squared
        - bias : Mean prediction error
        - sep : Standard error of prediction
    
    Examples
    --------
    >>> metrics = rmsec_rmsep(Y_test, Y_pred, type='RMSEP')
    >>> print(f"R2 = {metrics['r2']:.4f}")
    """
    residuals = Y_true - Y_pred
    
    # RMSE
    rmse = np.sqrt(np.mean(residuals ** 2))
    
    # R-squared
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((Y_true - np.mean(Y_true)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    
    # Bias
    bias = np.mean(residuals)
    
    # SEP (Standard Error of Prediction)
    sep = np.sqrt(np.mean((residuals - bias) ** 2))
    
    return {
        'type': type,
        'rmse': rmse,
        'r2': r2,
        'bias': bias,
        'sep': sep,
        'n_samples': len(Y_true)
    }


# =============================================================================
# DESCRIPTIVE STATISTICS
# =============================================================================

def descriptive_stats(data: np.ndarray, axis: int = 0) -> Dict:
    """
    Calculate comprehensive descriptive statistics.
    
    Parameters
    ----------
    data : np.ndarray
        Input data
    axis : int
        Axis for calculations
    
    Returns
    -------
    stats_dict : dict
        - mean, median, std, var
        - skewness, kurtosis
        - min, max, range
        - q1, q3, iqr
    
    Examples
    --------
    >>> stats = descriptive_stats(X, axis=0)
    >>> print(f"Mean: {stats['mean']}")
    >>> print(f"Skewness: {stats['skewness']}")
    """
    return {
        'mean': np.mean(data, axis=axis),
        'median': np.median(data, axis=axis),
        'std': np.std(data, axis=axis, ddof=1),
        'var': np.var(data, axis=axis, ddof=1),
        'skewness': stats.skew(data, axis=axis),
        'kurtosis': stats.kurtosis(data, axis=axis),
        'min': np.min(data, axis=axis),
        'max': np.max(data, axis=axis),
        'range': np.ptp(data, axis=axis),
        'q1': np.percentile(data, 25, axis=axis),
        'q3': np.percentile(data, 75, axis=axis),
        'iqr': np.percentile(data, 75, axis=axis) - np.percentile(data, 25, axis=axis),
        'n': data.shape[axis]
    }


def hypothesis_test(sample1: np.ndarray, 
                    sample2: Optional[np.ndarray] = None,
                    test: str = 't-test',
                    alpha: float = 0.05) -> Dict:
    """
    Perform common hypothesis tests.
    
    Parameters
    ----------
    sample1 : np.ndarray
        First sample
    sample2 : np.ndarray, optional
        Second sample (for two-sample tests)
    test : str
        't-test', 'paired-t', 'f-test', 'chi2'
    alpha : float
        Significance level
    
    Returns
    -------
    result : dict
        - statistic : test statistic
        - p_value : p-value
        - reject_H0 : bool (whether to reject null hypothesis)
        - confidence_level : 1 - alpha
    
    Examples
    --------
    >>> result = hypothesis_test(method_A, method_B, test='t-test')
    >>> if result['reject_H0']:
    >>>     print("Significant difference found!")
    """
    if test == 't-test' and sample2 is not None:
        stat, pval = stats.ttest_ind(sample1, sample2)
        test_name = "Independent samples t-test"
    elif test == 'paired-t' and sample2 is not None:
        stat, pval = stats.ttest_rel(sample1, sample2)
        test_name = "Paired t-test"
    elif test == 'f-test' and sample2 is not None:
        # F-test for variance comparison
        var1 = np.var(sample1, ddof=1)
        var2 = np.var(sample2, ddof=1)
        stat = var1 / var2 if var1 > var2 else var2 / var1
        df1 = len(sample1) - 1
        df2 = len(sample2) - 1
        pval = 2 * min(stats.f.cdf(stat, df1, df2), 1 - stats.f.cdf(stat, df1, df2))
        test_name = "F-test for equal variances"
    elif test == 'chi2':
        stat, pval = stats.chisquare(sample1)
        test_name = "Chi-square goodness of fit"
    else:
        # One-sample t-test
        stat, pval = stats.ttest_1samp(sample1, 0)
        test_name = "One-sample t-test"
    
    return {
        'test': test_name,
        'statistic': stat,
        'p_value': pval,
        'alpha': alpha,
        'reject_H0': pval < alpha,
        'confidence_level': 1 - alpha
    }


def confidence_interval(data: np.ndarray, 
                        confidence: float = 0.95,
                        axis: int = 0):
    """
    Calculate confidence interval for the mean.
    
    Parameters
    ----------
    data : np.ndarray or list
        Sample data
    confidence : float
        Confidence level (default 0.95)
    axis : int
        Axis for calculation (for arrays)
    
    Returns
    -------
    lower : float or np.ndarray
        Lower bound
    upper : float or np.ndarray
        Upper bound
    
    Examples
    --------
    >>> lower, upper = confidence_interval(measurements, confidence=0.99)
    >>> print(f"99% CI: [{lower:.3f}, {upper:.3f}]")
    """
    data = np.asarray(data, dtype=float)
    n = data.shape[axis]
    mean = np.mean(data, axis=axis)
    se = stats.sem(data, axis=axis)
    
    # t-critical value
    t_crit = stats.t.ppf((1 + confidence) / 2, n - 1)
    
    margin = t_crit * se
    lower = mean - margin
    upper = mean + margin
    # Return scalar if input was 1-D
    if data.ndim == 1:
        return float(lower), float(upper)
    return lower, upper


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def leverage(n_samples: int, n_components: int) -> np.ndarray:
    """
    Calculate leverage for samples in PCA/PLS model.
    
    Parameters
    ----------
    n_samples : int
        Number of samples
    n_components : int
        Number of components
    
    Returns
    -------
    h : np.ndarray
        Leverage values (diagonal of hat matrix)
    
    Notes
    -----
    High leverage samples have strong influence on the model.
    Leverage > 2 * (n_components + 1) / n_samples is considered high.
    """
    # For orthogonal scores, leverage = scores @ (T'T)^{-1} @ scores'
    # Simplified: each sample contributes 1/n to total variance
    h = np.ones(n_samples) * (n_components / n_samples)
    return h


def outlier_detection(model: Dict, 
                      residuals: np.ndarray,
                      threshold_leverage: float = 2.0,
                      threshold_residual: float = 3.0) -> Dict:
    """
    Detect outliers in PCA/PLS model.
    
    Parameters
    ----------
    model : dict
        Fitted model
    residuals : np.ndarray
        Model residuals (X - X_reconstructed) or Y - Y_pred
    threshold_leverage : float
        Leverage threshold multiplier
    threshold_residual : float
        Residual threshold (standard deviations)
    
    Returns
    -------
    outliers : dict
        - leverage_outliers : indices of high leverage samples
        - residual_outliers : indices of high residual samples
        - total_outliers : combined outlier indices
    """
    n = model['n_samples']
    n_comp = model['n_components']
    
    # Calculate leverage threshold
    h = leverage(n, n_comp)
    h_limit = threshold_leverage * (n_comp + 1) / n
    
    # Leverage outliers
    leverage_outliers = np.where(h > h_limit)[0]
    
    # Residual outliers (standardized residuals)
    residual_std = np.std(residuals, axis=0)
    residual_std = np.where(residual_std == 0, 1, residual_std)
    standardized_residuals = residuals / residual_std
    
    # For multivariate residuals, use total residual
    total_residual = np.sqrt(np.sum(residuals ** 2, axis=1))
    r_limit = threshold_residual * np.std(total_residual)
    residual_outliers = np.where(total_residual > r_limit)[0]
    
    return {
        'leverage_outliers': leverage_outliers,
        'leverage_values': h,
        'leverage_threshold': h_limit,
        'residual_outliers': residual_outliers,
        'total_residuals': total_residual,
        'residual_threshold': r_limit,
        'total_outliers': np.union1d(leverage_outliers, residual_outliers)
    }


# =============================================================================
# MODULE INFO
# =============================================================================

__all__ = [
    # Preprocessing
    'mean_center', 'standardize', 'snv', 'msc',
    # PCA
    'pca_fit', 'pca_transform', 'variance_explained', 'scree_plot_data',
    'scores_loadings', 'biplot_data',
    # PLS
    'pls_fit', 'pls_predict',
    # CLS
    'cls_calibration', 'cls_predict',
    # PCR
    'pcr_fit', 'pcr_predict',
    # Validation
    'cross_validate', 'rmsec_rmsep',
    # Statistics
    'descriptive_stats', 'hypothesis_test', 'confidence_interval',
    # Utilities
    'leverage', 'outlier_detection',
    # Additional
    't_test', 'one_way_anova', 'linear_regression', 'standard_addition',
    'internal_standard', 'propagation_uncertainty_expression', 'chromatography_resolution', 'plate_count',
    'plate_height', 'van_deemter', 'rsd', 'propagation_uncertainty'
]

__version__ = '1.0.0'


# =============================================================================
# ADDITIONAL STATISTICAL FUNCTIONS
# =============================================================================

def t_test(data, true_value=None, alpha=0.05):
    """One-sample t-test comparing data mean to true_value.
    
    Returns dict with t_calc, df, t_critical, p_value, significant.
    """
    data = np.asarray(data, dtype=float)
    n = len(data)
    df = n - 1
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    se = std / np.sqrt(n)
    
    if true_value is None:
        true_value = 0.0
    
    t_calc = (mean - true_value) / se
    p_value = 2 * stats.t.sf(np.abs(t_calc), df)
    t_critical = stats.t.ppf(1 - alpha/2, df)
    significant = p_value < alpha
    
    return {
        'mean': mean, 'std': std, 'n': n, 'df': df,
        't_calc': float(t_calc), 't_critical': float(t_critical),
        'p_value': float(p_value), 'significant': significant,
        'alpha': alpha
    }


def one_way_anova(*groups):
    """One-way ANOVA.
    
    groups: variable number of arrays/lists.
    Returns dict with SS_between, SS_within, MS_between, MS_within,
    F, F_critical, p_value, df_between, df_within.
    """
    groups = [np.asarray(g, dtype=float) for g in groups]
    k = len(groups)
    all_data = np.concatenate(groups)
    grand_mean = np.mean(all_data)
    n_total = len(all_data)
    
    SS_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
    SS_within = sum(np.sum((g - np.mean(g))**2) for g in groups)
    
    df_between = k - 1
    df_within = n_total - k
    
    MS_between = SS_between / df_between if df_between > 0 else 0
    MS_within = SS_within / df_within if df_within > 0 else 0
    
    F = MS_between / MS_within if MS_within > 0 else float('inf')
    p_value = 1 - stats.f.cdf(F, df_between, df_within)
    F_critical = stats.f.ppf(1 - 0.05, df_between, df_within)
    
    return {
        'SS_between': float(SS_between), 'SS_within': float(SS_within),
        'MS_between': float(MS_between), 'MS_within': float(MS_within),
        'F': float(F), 'F_critical': float(F_critical),
        'p_value': float(p_value),
        'df_between': df_between, 'df_within': df_within
    }


def linear_regression(x, y):
    """Simple linear regression y = mx + b.
    
    Returns slope, intercept, r_squared, std_err (of slope).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    
    sx = np.sum(x)
    sy = np.sum(y)
    sxx = np.sum(x**2)
    sxy = np.sum(x*y)
    syy = np.sum(y**2)
    
    denom = n*sxx - sx**2
    slope = (n*sxy - sx*sy) / denom
    intercept = (sy - slope*sx) / n
    
    ss_res = np.sum((y - (slope*x + intercept))**2)
    ss_tot = syy - sy**2/n
    r_squared = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
    
    se_y = np.sqrt(ss_res / (n - 2)) if n > 2 else 0
    std_err = se_y / np.sqrt(denom / n)
    
    return {
        'slope': float(slope), 'intercept': float(intercept),
        'r_squared': float(r_squared), 'std_err': float(std_err)
    }


def standard_addition(sample_signal, spike_data, c_spike=None, v_sample=None, method='simple'):
    """Standard addition method to determine concentration.
    
    Two methods available for handling dilution effects:
    
    **Method 1 - 'simple' (default)**: Plot S vs V_spike
    - Used when spike volume is negligible compared to sample volume (V_spike << V_sample)
    - Simpler calculation, but may underestimate concentration if dilution is significant
    - x-intercept = -C_sample × V_sample / C_spike
    
    **Method 2 - 'dilution_corrected'**: Plot S × (V_sample + V_spike) vs V_spike
    - Corrects for dilution of the original analyte when spike volumes are significant
    - Recommended when spike volume > 1% of sample volume
    - x-intercept = -C_sample × V_sample / C_spike
    - The transformation S×(V_sample+V_spike) accounts for dilution effect
    
    Harvey textbook (Analytical Chemistry 2.1) recommends:
    - Use 'simple' when V_spike < 1% of V_sample
    - Use 'dilution_corrected' for larger spike volumes
    
    Parameters
    ----------
    sample_signal : float
        Signal for unspiked sample
    spike_data : list
        List of (spike_volume, signal) tuples (excluding the 0-spike point)
        Spike volumes should be in same units as v_sample
    c_spike : float, optional
        Concentration of standard spike solution (same units as desired result)
    v_sample : float, optional
        Volume of original sample (required for 'dilution_corrected' method)
    method : str, optional
        'simple' (default) or 'dilution_corrected'
    
    Returns
    -------
    dict with:
        - concentration: calculated sample concentration (if c_spike and v_sample provided)
        - slope: regression slope
        - intercept: regression intercept
        - x_intercept: absolute value of x-intercept (volume of spike at S=0)
        - method: which method was used
    
    Examples
    --------
    >>> # Simple method (default)
    >>> result = standard_addition(15.0, [(0.10, 45.0), (0.20, 75.0)], 
    ...                            c_spike=600, v_sample=5.0)
    >>> result['concentration']
    6.0
    
    >>> # Dilution-corrected method
    >>> result = standard_addition(15.0, [(0.10, 45.0), (0.20, 75.0)], 
    ...                            c_spike=600, v_sample=5.0, method='dilution_corrected')
    """
    spike_data = list(spike_data)
    if len(spike_data) == 0 or spike_data[0][0] != 0:
        spike_data.insert(0, (0, sample_signal))
    
    x = np.array([d[0] for d in spike_data], dtype=float)  # spike volumes
    y = np.array([d[1] for d in spike_data], dtype=float)  # signals
    
    if method == 'dilution_corrected':
        if v_sample is None:
            raise ValueError("v_sample is required for 'dilution_corrected' method")
        # Transform: y = S × (V_sample + V_spike) to correct for dilution
        y = y * (v_sample + x)
    
    n = len(x)
    sx = np.sum(x)
    sy = np.sum(y)
    sxx = np.sum(x**2)
    sxy = np.sum(x*y)
    denom = n*sxx - sx**2
    
    if abs(denom) < 1e-15:
        raise ValueError("Cannot compute regression: x values are constant")
    
    slope = (n*sxy - sx*sy) / denom
    intercept = (sy - slope*sx) / n
    
    # x-intercept where signal = 0: x = -intercept/slope
    x_intercept = -intercept / slope if slope != 0 else 0
    
    if c_spike is not None and v_sample is not None:
        # C_sample = |x_intercept| * c_spike / v_sample
        concentration = abs(float(x_intercept)) * c_spike / v_sample
    else:
        concentration = abs(float(x_intercept))
    
    return {
        'concentration': float(concentration),
        'slope': float(slope),
        'intercept': float(intercept),
        'x_intercept': abs(float(x_intercept)),
        'method': method
    }


def internal_standard(sample_signals, standard_signals, is_concentration=None):
    """Internal standard method.
    
    sample_signals: analyte signals for samples
    standard_signals: internal standard signals for same samples  
    is_concentration: known IS concentration (if needed)
    
    Returns dict with response_ratios, mean_ratio.
    """
    sample_signals = np.asarray(sample_signals, dtype=float)
    standard_signals = np.asarray(standard_signals, dtype=float)
    ratios = sample_signals / standard_signals
    
    return {
        'response_ratios': ratios.tolist(),
        'mean_ratio': float(np.mean(ratios))
    }


def single_point_standard_addition(S_unspiked, S_spiked, C_std, V_std, 
                                     V_aliquot=None, V_flask_final=None, 
                                     V_stock_flask=None, mass_sample_g=None):
    """Single-point standard addition with multi-step dilution support.

    For problems where a sample undergoes dilution steps before standard addition:
    
    Step 1: Compute concentration of analyte in the MEASUREMENT flask (unspiked):
        C_analyte_flask = C_sample * V_aliquot / V_flask_final
        (where C_sample is concentration in the stock flask)
    
    Step 2: Compute concentration of standard added to the MEASUREMENT flask:
        C_std_flask = C_std * V_std / V_flask_final
    
    Step 3: From signal ratio:
        C_analyte_flask = C_std_flask * S_unspiked / (S_spiked - S_unspiked)
    
    Step 4: Back-calculate to original:
        C_stock = C_analyte_flask * V_flask_final / V_aliquot
        mass_analyte = C_stock * V_stock_flask (if in ppm = mg/L, multiply by L to get mg)
        weight_percent = mass_analyte / mass_sample_g * 100 (if mass_sample_g provided)

    Parameters
    ----------
    S_unspiked : float - signal for unspiked measurement flask
    S_spiked : float - signal for spiked measurement flask  
    C_std : float - concentration of standard solution (ppm or same units as desired result)
    V_std : float - volume of standard added (mL)
    V_aliquot : float - volume of aliquot taken from stock flask (mL)
    V_flask_final : float - final volume of measurement flask (mL)
    V_stock_flask : float - volume of original stock flask (mL)
    mass_sample_g : float - original sample mass in grams (for weight_percent)

    Returns dict with concentration_ppm, weight_percent (if mass_sample_g given),
    and intermediate values for verification.
    """
    if V_aliquot is None or V_flask_final is None:
        raise ValueError("V_aliquot and V_flask_final are required for multi-step dilution problems")
    
    # Concentration of standard in the measurement flask
    C_std_in_flask = C_std * V_std / V_flask_final
    
    # Concentration of analyte in the measurement flask (unspiked)
    dS = S_spiked - S_unspiked
    if abs(dS) < 1e-15:
        raise ValueError("S_spiked must differ from S_unspiked")
    C_analyte_flask = C_std_in_flask * S_unspiked / dS
    
    # Back-calculate to stock flask concentration (ppm = mg/L)
    C_stock = C_analyte_flask * V_flask_final / V_aliquot
    
    result = {
        'C_analyte_flask_ppm': float(C_analyte_flask),
        'C_stock_ppm': float(C_stock),
        'C_std_in_flask_ppm': float(C_std_in_flask)
    }
    
    if V_stock_flask is not None:
        mass_mg = C_stock * V_stock_flask / 1000.0  # ppm * L = mg
        result['mass_analyte_mg'] = float(mass_mg)
    
    if mass_sample_g is not None:
        V_stock = V_stock_flask if V_stock_flask is not None else V_flask_final
        mass_mg = C_stock * V_stock / 1000.0
        # Convert mg to g for weight percent
        mass_g = mass_mg / 1000.0
        wt_pct = mass_g / mass_sample_g * 100.0
        result['weight_percent'] = float(wt_pct)
    
    return result


def chromatography_resolution(tR1, tR2, w1, w2):
    """Calculate chromatographic resolution Rs = 2(tR2-tR1)/(w1+w2)."""
    return abs(tR2 - tR1) / ((w1 + w2) / 2)


def plate_count(tR, w):
    """Calculate number of theoretical plates N = 16*(tR/w)^2."""
    return 16 * (tR / w)**2


def plate_height(L, N):
    """Calculate plate height H = L/N."""
    return L / N


def van_deemter(u, A, B, C):
    """Van Deemter equation: H = A + B/u + C*u."""
    return A + B/u + C*u


def rsd(data):
    """Relative standard deviation (RSD) = std/mean * 100 (%)."""
    data = np.asarray(data, dtype=float)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    return (std / mean * 100) if mean != 0 else 0


def propagation_uncertainty(values, uncertainties, operation='multiply'):
    """Error propagation.
    
    For multiplication/division: relative uncertainties add.
    For addition/subtraction: absolute uncertainties add.
    
    values: list of measured values
    uncertainties: list of uncertainties (same length)
    operation: 'multiply', 'divide', 'add', 'subtract', or formula string
    
    Returns propagated uncertainty.
    """
    values = np.asarray(values, dtype=float)
    uncertainties = np.asarray(uncertainties, dtype=float)
    
    if operation in ('multiply', 'divide'):
        # Relative (fractional) uncertainties add in quadrature
        rel_unc = uncertainties / np.abs(values)
        total_rel = np.sqrt(np.sum(rel_unc**2))
        result = np.prod(values)
        return abs(result) * total_rel
    elif operation in ('add', 'subtract'):
        # Absolute uncertainties add in quadrature
        return np.sqrt(np.sum(uncertainties**2))
    elif operation == 'power':
        # Special: result = value^n, uncertainty = n * (u/value) * result
        # values[0] = base value, values[1] = exponent n
        base = values[0]
        n_exp = values[1]
        u_base = uncertainties[0]
        result = base ** n_exp
        return abs(n_exp * u_base / base) * abs(result)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def propagation_uncertainty_expression(result_value, partial_derivatives, uncertainties):
    """Error propagation via partial derivatives.
    
    Given f(x1, x2, ...) = result_value, and a list of partial derivatives
    evaluated at the measurement points, computes:
    δf = sqrt( Σ (∂f/∂xi)² × δxi² )
    
    Parameters
    ----------
    result_value : float
        The computed result (f)
    partial_derivatives : list of float
        ∂f/∂x1, ∂f/∂x2, ... evaluated at the measurement points
    uncertainties : list of float
        Uncertainties δx1, δx2, ... for each variable
    
    Returns
    -------
    dict with result, uncertainty, relative_uncertainty
    
    Examples
    --------
    >>> # FW = gRT/(PV), ∂FW/∂g = RT/(PV), etc.
    >>> propagation_uncertainty_expression(16.04, [135.9, 0.0003, 0.0538, -22.15], 
    ...                                   [0.002, 0.000001, 0.1, 0.003])
    """
    partial_derivatives = np.asarray(partial_derivatives, dtype=float)
    uncertainties = np.asarray(uncertainties, dtype=float)
    
    variance = np.sum((partial_derivatives * uncertainties)**2)
    abs_uncertainty = np.sqrt(variance)
    rel_uncertainty = abs_uncertainty / abs(result_value) if result_value != 0 else float('inf')
    
    return {
        'result': float(result_value),
        'uncertainty': float(abs_uncertainty),
        'relative_uncertainty': float(rel_uncertainty)
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'biplot_data', 'description': 'Prepare coordinates for a biplot.\n\nParameters\n----------\nmodel : dict\n    Fitted PCA model\npc_x : int\n    Principal component for x-axis (1-indexed)\npc_y : int\n    Principal component for y-axis (1-indexed)\nloading_scale : float\n    Scale factor for loading vectors\n\nReturns\n-------\nscores_xy : np.ndarray\n    Score coordinates (n_samples, 2)\nloadings_xy : np.ndarray\n    Loading vectors (n_variables, 2)\n\nExamples\n--------\n>>> model = pca_fit(X)\n>>> scores_xy, loadings_xy = biplot_data(model, pc_x=1, pc_y=2)\n>>> # Plot scores as points, loadings as arrows', 'inputSchema': {'type': 'object', 'properties': {'model': {'type': 'string', 'description': 'Model'}, 'pc_x': {'type': 'number', 'description': 'Pc X', 'default': 1}, 'pc_y': {'type': 'number', 'description': 'Pc Y', 'default': 2}, 'loading_scale': {'type': 'number', 'description': 'Loading Scale', 'default': 1.0}}, 'required': ['model']}},
    {'name': 'cls_calibration', 'description': "Classical Least Squares calibration (Beer's law approach).\n\nDetermines molar absorptivities from known concentrations.\n\nParameters\n----------\nA : np.ndarray\n    Absorbance matrix (samples x wavelengths)\nC : np.ndarray\n    Concentration matrix (samples x analytes)\n\nReturns\n-------\nK : np.ndarray\n    Molar absorptivity matrix (analytes x wavelengths)\n\nExamples\n--------\n>>> # 3 analytes, 10 wavelengths, 5 calibration samples\n>>> A = np.random.rand(5, 10)  # Absorbance\n>>> C = np.random.rand(5, 3)   # Concentrations\n>>> K = cls_calibration(A, C)  # Shape: (3, 10)\n\nNotes\n-----\nCLS assumes: A = C @ K\nRequires all analytes in mixture to be known.\nSolves: K = (C^T C)^{-1} C^T A", 'inputSchema': {'type': 'object', 'properties': {'A': {'type': 'number', 'description': 'A'}, 'C': {'type': 'number', 'description': 'C'}}, 'required': ['A', 'C']}},
    {'name': 'cls_predict', 'description': 'Predict concentrations from absorbance using CLS.\n\nParameters\n----------\nA : np.ndarray\n    Absorbance matrix (samples x wavelengths)\nK : np.ndarray\n    Molar absorptivity matrix (analytes x wavelengths)\n\nReturns\n-------\nC : np.ndarray\n    Predicted concentrations (samples x analytes)\n\nNotes\n-----\nSolves: C = A @ K^T @ (K @ K^T)^{-1}', 'inputSchema': {'type': 'object', 'properties': {'A': {'type': 'number', 'description': 'A'}, 'K': {'type': 'number', 'description': 'K'}}, 'required': ['A', 'K']}},
    {'name': 'confidence_interval', 'description': 'Calculate confidence interval for the mean.\n\nParameters\n----------\ndata : np.ndarray\n    Sample data\nconfidence : float\n    Confidence level (default 0.95)\naxis : int\n    Axis for calculation\n\nReturns\n-------\nlower : np.ndarray\n    Lower bound\nupper : np.ndarray\n    Upper bound\n\nExamples\n--------\n>>> lower, upper = confidence_interval(measurements, confidence=0.99)\n>>> print(f"99% CI: [{lower:.3f}, {upper:.3f}]")', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'confidence': {'type': 'string', 'description': 'Confidence', 'default': 0.95}, 'axis': {'type': 'number', 'description': 'Axis', 'default': 0}}, 'required': ['data']}},
    {'name': 'cross_validate', 'description': 'Cross-validation for component selection.\n\nParameters\n----------\nX : np.ndarray\n    Predictor matrix\nY : np.ndarray\n    Response matrix\nmethod : str\n    \'pls\' or \'pcr\'\nmax_components : int\n    Maximum number of components to test\ncv_folds : int\n    Number of cross-validation folds\n\nReturns\n-------\nresults : dict\n    - rmsecv : np.ndarray (RMSECV for each n_components)\n    - optimal_components : int\n    - optimal_rmsecv : float\n\nExamples\n--------\n>>> cv_result = cross_validate(X, Y, method=\'pls\', max_components=10)\n>>> print(f"Optimal components: {cv_result[\'optimal_components\']}")', 'inputSchema': {'type': 'object', 'properties': {'X': {'type': 'number', 'description': 'X'}, 'Y': {'type': 'number', 'description': 'Y'}, 'method': {'type': 'string', 'description': 'Method', 'default': 'pls'}, 'max_components': {'type': 'number', 'description': 'Max Components', 'default': 10}, 'cv_folds': {'type': 'number', 'description': 'Cv Folds', 'default': 5}}, 'required': ['X', 'Y']}},
    {'name': 'descriptive_stats', 'description': 'Calculate comprehensive descriptive statistics.\n\nParameters\n----------\ndata : np.ndarray\n    Input data\naxis : int\n    Axis for calculations\n\nReturns\n-------\nstats_dict : dict\n    - mean, median, std, var\n    - skewness, kurtosis\n    - min, max, range\n    - q1, q3, iqr\n\nExamples\n--------\n>>> stats = descriptive_stats(X, axis=0)\n>>> print(f"Mean: {stats[\'mean\']}")\n>>> print(f"Skewness: {stats[\'skewness\']}")', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'axis': {'type': 'number', 'description': 'Axis', 'default': 0}}, 'required': ['data']}},
    {'name': 'hypothesis_test', 'description': 'Perform common hypothesis tests.\n\nParameters\n----------\nsample1 : np.ndarray\n    First sample\nsample2 : np.ndarray, optional\n    Second sample (for two-sample tests)\ntest : str\n    \'t-test\', \'paired-t\', \'f-test\', \'chi2\'\nalpha : float\n    Significance level\n\nReturns\n-------\nresult : dict\n    - statistic : test statistic\n    - p_value : p-value\n    - reject_H0 : bool (whether to reject null hypothesis)\n    - confidence_level : 1 - alpha\n\nExamples\n--------\n>>> result = hypothesis_test(method_A, method_B, test=\'t-test\')\n>>> if result[\'reject_H0\']:\n>>>     print("Significant difference found!")', 'inputSchema': {'type': 'object', 'properties': {'sample1': {'type': 'string', 'description': 'Sample1'}, 'sample2': {'type': 'string', 'description': 'Sample2', 'default': None}, 'test': {'type': 'number', 'description': 'Test', 'default': 't-test'}, 'alpha': {'type': 'number', 'description': 'Alpha', 'default': 0.05}}, 'required': ['sample1']}},
    {'name': 'leverage', 'description': 'Calculate leverage for samples in PCA/PLS model.\n\nParameters\n----------\nn_samples : int\n    Number of samples\nn_components : int\n    Number of components\n\nReturns\n-------\nh : np.ndarray\n    Leverage values (diagonal of hat matrix)\n\nNotes\n-----\nHigh leverage samples have strong influence on the model.\nLeverage > 2 * (n_components + 1) / n_samples is considered high.', 'inputSchema': {'type': 'object', 'properties': {'n_samples': {'type': 'string', 'description': 'N Samples'}, 'n_components': {'type': 'number', 'description': 'N Components'}}, 'required': ['n_samples', 'n_components']}},
    {'name': 'mean_center', 'description': 'Mean-center data by subtracting column (or row) means.\n\nParameters\n----------\ndata : np.ndarray\n    Input data matrix (samples x variables)\naxis : int\n    Axis along which to center (0=columns, 1=rows)\n\nReturns\n-------\ncentered : np.ndarray\n    Mean-centered data\nmeans : np.ndarray\n    Mean values subtracted\n\nExamples\n--------\n>>> X = np.array([[1, 2], [3, 4], [5, 6]])\n>>> Xc, means = mean_center(X)\n>>> means\narray([3., 4.])\n\nNotes\n-----\nMean centering is essential for PCA as it ensures the first principal\ncomponent passes through the centroid of the data.', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'axis': {'type': 'number', 'description': 'Axis', 'default': 0}}, 'required': ['data']}},
    {'name': 'msc', 'description': 'Multiplicative Scatter Correction (MSC).\n\nCorrects for scatter effects in spectroscopic data.\n\nParameters\n----------\ndata : np.ndarray\n    Spectral data (samples x wavelengths)\nreference : np.ndarray, optional\n    Reference spectrum (default: mean spectrum)\n\nReturns\n-------\ncorrected : np.ndarray\n    MSC-corrected spectra\nreference : np.ndarray\n    Reference spectrum used\n\nNotes\n-----\nMSC fits each spectrum to the reference using linear regression,\nthen corrects for additive and multiplicative effects.', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'reference': {'type': 'string', 'description': 'Reference', 'default': None}}, 'required': ['data']}},
    {'name': 'outlier_detection', 'description': 'Detect outliers in PCA/PLS model.\n\nParameters\n----------\nmodel : dict\n    Fitted model\nresiduals : np.ndarray\n    Model residuals (X - X_reconstructed) or Y - Y_pred\nthreshold_leverage : float\n    Leverage threshold multiplier\nthreshold_residual : float\n    Residual threshold (standard deviations)\n\nReturns\n-------\noutliers : dict\n    - leverage_outliers : indices of high leverage samples\n    - residual_outliers : indices of high residual samples\n    - total_outliers : combined outlier indices', 'inputSchema': {'type': 'object', 'properties': {'model': {'type': 'string', 'description': 'Model'}, 'residuals': {'type': 'string', 'description': 'Residuals'}, 'threshold_leverage': {'type': 'number', 'description': 'Threshold Leverage', 'default': 2.0}, 'threshold_residual': {'type': 'string', 'description': 'Threshold Residual', 'default': 3.0}}, 'required': ['model', 'residuals']}},
    {'name': 'pca_fit', 'description': "Fit a PCA model to data.\n\nParameters\n----------\ndata : np.ndarray\n    Input data matrix (samples x variables)\nn_components : int, optional\n    Number of components to retain (default: all)\ncenter : bool\n    Whether to mean-center the data\nscale : bool\n    Whether to standardize variables\n\nReturns\n-------\nmodel : dict\n    PCA model containing:\n    - scores : np.ndarray (samples x n_components)\n    - loadings : np.ndarray (variables x n_components)\n    - explained_variance : np.ndarray\n    - explained_variance_ratio : np.ndarray\n    - singular_values : np.ndarray\n    - mean : np.ndarray\n    - scale : np.ndarray (if scale=true)\n\nExamples\n--------\n>>> X = np.random.randn(50, 10)\n>>> model = pca_fit(X, n_components=3)\n>>> model['explained_variance_ratio']\narray([...])\n\nNotes\n-----\nPCA finds orthogonal directions of maximum variance.\nFor spectral data, use center=true, scale=false.", 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'n_components': {'type': 'number', 'description': 'N Components', 'default': None}, 'center': {'type': 'boolean', 'description': 'Center', 'default': True}, 'scale': {'type': 'boolean', 'description': 'Scale', 'default': False}}, 'required': ['data']}},
    {'name': 'pca_transform', 'description': 'Transform new data using fitted PCA model.\n\nParameters\n----------\ndata : np.ndarray\n    New data to transform (samples x variables)\nmodel : dict\n    Fitted PCA model from pca_fit()\n\nReturns\n-------\nscores : np.ndarray\n    Scores for new samples\n\nExamples\n--------\n>>> model = pca_fit(X_train, n_components=3)\n>>> X_test_scores = pca_transform(X_test, model)', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'model': {'type': 'string', 'description': 'Model'}}, 'required': ['data', 'model']}},
    {'name': 'pcr_fit', 'description': 'Principal Component Regression.\n\nCombines PCA dimensionality reduction with linear regression.\n\nParameters\n----------\nX : np.ndarray\n    Predictor matrix (samples x variables)\nY : np.ndarray\n    Response matrix (samples x responses)\nn_components : int\n    Number of principal components to use\n\nReturns\n-------\nmodel : dict\n    PCR model containing PCA model and regression coefficients\n\nNotes\n-----\nPCR is simpler than PLS but may require more components\nto achieve the same predictive power.', 'inputSchema': {'type': 'object', 'properties': {'X': {'type': 'number', 'description': 'X'}, 'Y': {'type': 'number', 'description': 'Y'}, 'n_components': {'type': 'number', 'description': 'N Components', 'default': 2}}, 'required': ['X', 'Y']}},
    {'name': 'pcr_predict', 'description': 'Predict using PCR model.\n\nParameters\n----------\nX : np.ndarray\n    Predictor data\nmodel : dict\n    Fitted PCR model\n\nReturns\n-------\nY_pred : np.ndarray\n    Predictions', 'inputSchema': {'type': 'object', 'properties': {'X': {'type': 'number', 'description': 'X'}, 'model': {'type': 'string', 'description': 'Model'}}, 'required': ['X', 'model']}},
    {'name': 'pls_fit', 'description': 'Fit a PLS regression model.\n\nParameters\n----------\nX : np.ndarray\n    Predictor matrix (samples x variables)\nY : np.ndarray\n    Response matrix (samples x responses)\nn_components : int\n    Number of latent variables\ncenter : bool\n    Mean-center X and Y\nscale : bool\n    Standardize X and Y\n\nReturns\n-------\nmodel : dict\n    PLS model containing:\n    - X_scores : np.ndarray (T)\n    - X_loadings : np.ndarray (P)\n    - Y_scores : np.ndarray (U)\n    - Y_loadings : np.ndarray (Q)\n    - weights : np.ndarray (W)\n    - coefficients : np.ndarray (B)\n    - X_mean, Y_mean : np.ndarray\n    - X_scale, Y_scale : np.ndarray\n\nExamples\n--------\n>>> X = np.random.randn(50, 10)\n>>> Y = np.random.randn(50, 1)\n>>> model = pls_fit(X, Y, n_components=3)\n\nNotes\n-----\nPLS finds latent variables that maximize covariance with Y.\nUse cross-validation to select optimal n_components.', 'inputSchema': {'type': 'object', 'properties': {'X': {'type': 'number', 'description': 'X'}, 'Y': {'type': 'number', 'description': 'Y'}, 'n_components': {'type': 'number', 'description': 'N Components', 'default': 2}, 'center': {'type': 'boolean', 'description': 'Center', 'default': True}, 'scale': {'type': 'boolean', 'description': 'Scale', 'default': False}}, 'required': ['X', 'Y']}},
    {'name': 'pls_predict', 'description': 'Predict Y values from X using fitted PLS model.\n\nParameters\n----------\nX : np.ndarray\n    Predictor data (samples x variables)\nmodel : dict\n    Fitted PLS model from pls_fit()\n\nReturns\n-------\nY_pred : np.ndarray\n    Predicted Y values\n\nExamples\n--------\n>>> model = pls_fit(X_train, Y_train, n_components=3)\n>>> Y_pred = pls_predict(X_test, model)', 'inputSchema': {'type': 'object', 'properties': {'X': {'type': 'number', 'description': 'X'}, 'model': {'type': 'string', 'description': 'Model'}}, 'required': ['X', 'model']}},
    {'name': 'rmsec_rmsep', 'description': 'Calculate calibration/prediction error metrics.\n\nParameters\n----------\nY_true : np.ndarray\n    true values\nY_pred : np.ndarray\n    Predicted values\ntype : str\n    \'RMSEC\' (calibration) or \'RMSEP\' (prediction)\n\nReturns\n-------\nmetrics : dict\n    - rmse : Root mean squared error\n    - r2 : R-squared\n    - bias : Mean prediction error\n    - sep : Standard error of prediction\n\nExamples\n--------\n>>> metrics = rmsec_rmsep(Y_test, Y_pred, type=\'RMSEP\')\n>>> print(f"R2 = {metrics[\'r2\']:.4f}")', 'inputSchema': {'type': 'object', 'properties': {'Y_true': {'type': 'number', 'description': 'Y true'}, 'Y_pred': {'type': 'number', 'description': 'Y Pred'}, 'type': {'type': 'string', 'description': 'Type', 'default': 'RMSEC'}}, 'required': ['Y_true', 'Y_pred']}},
    {'name': 'scores_loadings', 'description': 'Extract scores and loadings from PCA model.\n\nParameters\n----------\nmodel : dict\n    Fitted PCA model\n\nReturns\n-------\nscores : np.ndarray\n    Sample scores\nloadings : np.ndarray\n    Variable loadings\n\nNotes\n-----\nScores show sample positions in PC space.\nLoadings show variable contributions to each PC.', 'inputSchema': {'type': 'object', 'properties': {'model': {'type': 'string', 'description': 'Model'}}, 'required': ['model']}},
    {'name': 'scree_plot_data', 'description': "Generate data for scree plot.\n\nParameters\n----------\nmodel : dict\n    Fitted PCA model\n\nReturns\n-------\ncomponents : np.ndarray\n    Component numbers (1, 2, 3, ...)\nvariance : np.ndarray\n    Variance explained by each component\n\nExamples\n--------\n>>> model = pca_fit(X)\n>>> comp_nums, var = scree_plot_data(model)\n>>> # Plot: plt.plot(comp_nums, var, 'o-')", 'inputSchema': {'type': 'object', 'properties': {'model': {'type': 'string', 'description': 'Model'}}, 'required': ['model']}},
    {'name': 'snv', 'description': 'Standard Normal Variate (SNV) transformation.\n\nEach spectrum is standardized independently (row-wise).\nCommon preprocessing for NIR spectroscopy.\n\nParameters\n----------\ndata : np.ndarray\n    Spectral data (samples x wavelengths)\n\nReturns\n-------\nsnv_data : np.ndarray\n    SNV-transformed spectra\n\nNotes\n-----\nSNV removes scatter effects and baseline variations.\nApply before mean-centering for PCA of spectral data.', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}}, 'required': ['data']}},
    {'name': 'standardize', 'description': 'Z-score standardization: center and scale to unit variance.\n\nParameters\n----------\ndata : np.ndarray\n    Input data matrix\naxis : int\n    Axis along which to standardize\n\nReturns\n-------\nstandardized : np.ndarray\n    Standardized data (mean=0, std=1)\nmeans : np.ndarray\n    Column/row means\nstds : np.ndarray\n    Column/row standard deviations\n\nExamples\n--------\n>>> X = np.array([[1, 2], [3, 4], [5, 6]])\n>>> Xs, means, stds = standardize(X)\n\nNotes\n-----\nUse standardization when variables have different units or scales.\nFor spectroscopic data, mean-centering alone is often sufficient.', 'inputSchema': {'type': 'object', 'properties': {'data': {'type': 'number', 'description': 'Data'}, 'axis': {'type': 'number', 'description': 'Axis', 'default': 0}}, 'required': ['data']}},
    {'name': 'variance_explained', 'description': 'Get variance explained by each principal component.\n\nParameters\n----------\nmodel : dict\n    Fitted PCA model\ncumulative : bool\n    Return cumulative variance\n\nReturns\n-------\nvariance : np.ndarray\n    Variance explained (individual or cumulative)\n\nExamples\n--------\n>>> model = pca_fit(X)\n>>> cum_var = variance_explained(model, cumulative=true)\n>>> # Find components for 95% variance\n>>> n_comp = np.argmax(cum_var >= 0.95) + 1', 'inputSchema': {'type': 'object', 'properties': {'model': {'type': 'string', 'description': 'Model'}, 'cumulative': {'type': 'number', 'description': 'Cumulative', 'default': False}}, 'required': ['model']}}
]
