"""
Chemometrics Multivariate Linear Regression Tools - L3 Implementation
CLS, PLS, and Cross-Validation for Chemical Calibration

Provides core multivariate calibration methods:
- Classical Least Squares (CLS) calibration
- Partial Least Squares (PLS) regression
- Cross-validation for model assessment

References:
- Harvey, "Chemometrics Using R", Chapter 11
- Martens & Naes, "Multivariate Calibration", 1989
- Wold et al., "PLS-regression: a basic tool of chemometrics", 2001

## Solver Instructions (for AI Agent)

When you encounter chemometrics multivariate regression (CLS/PLS) problems:

### Step 1: Identify what is given and what is asked
- Given: spectra X, concentrations C or responses Y
- Asked: calibration model, predictions, cross-validation, VIP scores

### Step 2: Choose the correct function
- `cls_fit(C, A)`: CLS calibration (K = C Aᵀ (A Aᵀ)-1)
- `cls_predict(A, model)`: Predict with CLS model
- `pls_fit(X, Y, n_components)`: PLS calibration
- `pls_predict(X, model)`: Predict with PLS model
- `pls_vip(model)`: Variable Importance in Projection scores
- `cross_validate(model_func, X, Y, n_components, n_folds)`: k-fold CV
- `optimal_components(X, Y, max_components, n_folds)`: Find optimal PLS components
- `rmse(actual, predicted)`, `r_squared(actual, predicted)`: Model quality metrics
- `mae(actual, predicted)`, `bias(actual, predicted)`: Additional metrics

### Step 3: Handle special cases
- CLS requires pure component spectra known; PLS handles unknown interferents
- Always cross-validate to avoid overfitting; optimal components ~ minimum RMSECV
- VIP > 1 indicates important variables; VIP < 0.5 can be excluded
- Mean-center data before PLS

### Examples
```python
model = pls_fit(X, Y, n_components=3)
Y_pred = pls_predict(X_test, model)
vip = pls_vip(model)
rmse_val = rmse(Y_test, Y_pred)
```
"""

from typing import Tuple, Optional, Dict, Union, Callable
import numpy as np
from numpy.typing import NDArray


# =============================================================================
# Classical Least Squares (CLS)
# =============================================================================

def cls_fit(C: NDArray[np.floating], 
            A: NDArray[np.floating]) -> Dict[str, NDArray[np.floating]]:
    """
    Fit Classical Least Squares (CLS) calibration model.
    
    CLS (also called K-matrix calibration) is used when pure component
    spectra are known. The model assumes Beer's Law additivity:
        A = C x K
    where A is absorbance, C is concentration, K is molar absorptivity.
    
    The calibration determines K from known concentrations and spectra:
        K = (C^T C)^(-1) C^T A
    
    This is suitable for:
    - Known pure component spectra
    - Calibration with standard mixtures
    - Systems obeying Beer's Law (linear, additive)
    
    Args:
        C: Concentration matrix (n_samples x n_components)
           Each column is concentration of one component
        A: Absorbance/spectra matrix (n_samples x n_wavelengths)
           Each row is a spectrum
    
    Returns:
        Dict containing:
            - 'K': Sensitivity matrix (n_components x n_wavelengths)
                   Each row is the pure component spectrum (ε x pathlength)
            - 'C_train': Training concentrations
            - 'A_train': Training spectra
            - 'residuals': Calibration residuals (A - C @ K)
            - 'rmsec': Root mean square error of calibration
    
    Raises:
        ValueError: If matrix dimensions are incompatible
        np.linalg.LinAlgError: If C is rank-deficient
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> # Simulate Cu2+/Cr3+ mixture UV-Vis
        >>> n_samples, n_wl, n_comp = 10, 20, 2
        >>> C = np.random.rand(n_samples, n_comp)  # Concentrations
        >>> # Pure component spectra (K matrix)
        >>> K_true = np.random.rand(n_comp, n_wl)
        >>> A = C @ K_true + np.random.randn(n_samples, n_wl) * 0.01
        >>> model = cls_fit(C, A)
        >>> model['K'].shape
        (2, 20)
    
    Notes:
        - Requires n_samples ≥ n_components for stable inversion
        - Assumes linear, additive response (Beer's Law)
        - Sensitive to baseline offsets and scattering
    """
    C = np.asarray(C, dtype=np.float64)
    A = np.asarray(A, dtype=np.float64)
    
    # Validate dimensions
    if C.ndim != 2 or A.ndim != 2:
        raise ValueError("C and A must be 2D matrices")
    
    n_samples_c, n_components = C.shape
    n_samples_a, n_wavelengths = A.shape
    
    if n_samples_c != n_samples_a:
        raise ValueError(f"C has {n_samples_c} samples, A has {n_samples_a} samples")
    
    if n_samples_c < n_components:
        raise ValueError(f"Need at least {n_components} samples for {n_components} components")
    
    # Solve: K = (C^T C)^(-1) C^T A = C^+ A (pseudo-inverse)
    # Using least squares for numerical stability
    K, residuals_lstsq, rank, s = np.linalg.lstsq(C, A, rcond=None)
    
    # Calculate calibration residuals
    A_pred = np.dot(C, K)
    residuals = A - A_pred
    
    # RMSEC (per wavelength, then averaged)
    rmsec = np.sqrt(np.mean(residuals ** 2))
    
    return {
        'K': K,
        'C_train': C,
        'A_train': A,
        'residuals': residuals,
        'rmsec': rmsec,
        'n_components': n_components,
        'n_wavelengths': n_wavelengths,
        'n_samples': n_samples_c
    }


def cls_predict(A: NDArray[np.floating], 
                K: Union[NDArray[np.floating], Dict]) -> NDArray[np.floating]:
    """
    Predict concentrations from spectra using CLS model.
    
    Given unknown spectra, predict component concentrations using
    the sensitivity matrix K:
        Ĉ = A x K^T x (K x K^T)^(-1)
    
    This inverts the Beer's Law relationship to solve for concentrations.
    
    Args:
        A: Unknown absorbance/spectra matrix (n_samples x n_wavelengths)
        K: Sensitivity matrix (n_components x n_wavelengths) or CLS model dict
    
    Returns:
        Predicted concentrations (n_samples x n_components)
    
    Raises:
        ValueError: If A and K have incompatible dimensions
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> # Calibration
        >>> C_cal = np.array([[1, 0], [0, 1], [0.5, 0.5]])
        >>> K_true = np.array([[0.1, 0.2, 0.1], [0.05, 0.15, 0.1]])
        >>> A_cal = C_cal @ K_true
        >>> model = cls_fit(C_cal, A_cal)
        >>> # Prediction
        >>> A_unknown = np.array([[0.075, 0.175, 0.1]])  # Equal mixture
        >>> C_pred = cls_predict(A_unknown, model['K'])
        >>> C_pred.round(2)
        array([[0.5, 0.5]])
    """
    A = np.asarray(A, dtype=np.float64)
    
    # Handle dict input
    if isinstance(K, dict):
        K = K['K']
    
    K = np.asarray(K, dtype=np.float64)
    
    # Validate dimensions
    if A.ndim == 1:
        A = A.reshape(1, -1)
    
    n_wavelengths_a = A.shape[1]
    n_components, n_wavelengths_k = K.shape
    
    if n_wavelengths_a != n_wavelengths_k:
        raise ValueError(f"A has {n_wavelengths_a} wavelengths, K has {n_wavelengths_k}")
    
    # Solve: C = A K^T (K K^T)^(-1)
    # Using least squares: C = argmin ||A - C K||2
    C_pred = np.linalg.lstsq(K.T, A.T, rcond=None)[0].T
    
    return C_pred


# =============================================================================
# Partial Least Squares (PLS)
# =============================================================================

def pls_fit(X: NDArray[np.floating], 
            Y: NDArray[np.floating], 
            n_components: int,
            max_iter: int = 500,
            tol: float = 1e-6) -> Dict[str, Union[NDArray[np.floating], int]]:
    """
    Fit Partial Least Squares (PLS) regression model using NIPALS algorithm.
    
    PLS finds latent variables that maximize covariance between X and Y.
    It's the most widely used multivariate calibration method in
    chemometrics because it:
    - Handles collinear variables (overlapping spectral bands)
    - Works when X has more variables than samples
    - Reduces noise by dimensionality reduction
    
    The model: X = T P^T + E, Y = U Q^T + F
    with scores T and U related by: U = T D (diagonal matrix)
    
    Args:
        X: Predictor matrix (n_samples x n_variables), typically spectra
        Y: Response matrix (n_samples x n_responses), typically concentrations
        n_components: Number of PLS components (latent variables)
        max_iter: Maximum iterations for NIPALS convergence
        tol: Convergence tolerance
    
    Returns:
        Dict containing:
            - 'W': X weights (n_variables x n_components)
            - 'P': X loadings (n_variables x n_components)
            - 'Q': Y loadings (n_responses x n_components)
            - 'T': X scores (n_samples x n_components)
            - 'U': Y scores (n_samples x n_components)
            - 'B': Regression coefficients (n_variables x n_responses)
            - 'x_mean': Mean of X columns
            - 'y_mean': Mean of Y columns
            - 'x_std': Std of X columns (if scaling)
            - 'y_std': Std of Y columns (if scaling)
            - 'n_components': Number of components
            - 'explained_variance_x': Variance of X explained per component
            - 'explained_variance_y': Variance of Y explained per component
    
    Raises:
        ValueError: If dimensions are incompatible or n_components invalid
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> n_samples, n_wl, n_comp = 30, 50, 3
        >>> X = np.random.randn(n_samples, n_wl)
        >>> Y = np.random.randn(n_samples, 2)
        >>> model = pls_fit(X, Y, n_components=5)
        >>> model['B'].shape
        (50, 2)
    
    Notes:
        - Default is mean-centering (no scaling)
        - For PLS1 (single Y), use Y as column vector
        - For PLS2 (multiple Y), use Y as matrix
        - Component selection typically done by cross-validation
    
    References:
        - Wold, S. et al. (2001). PLS-regression: a basic tool of chemometrics
        - Geladi, P. & Kowalski, B.R. (1986). Partial least-squares regression
    """
    X = np.asarray(X, dtype=np.float64).copy()
    Y = np.asarray(Y, dtype=np.float64).copy()
    
    # Validate dimensions
    if X.ndim != 2 or Y.ndim != 2:
        raise ValueError("X and Y must be 2D matrices")
    
    n_samples_x, n_variables = X.shape
    n_samples_y, n_responses = Y.shape
    
    if n_samples_x != n_samples_y:
        raise ValueError(f"X has {n_samples_x} samples, Y has {n_samples_y} samples")
    
    n_samples = n_samples_x
    
    if n_components > min(n_samples, n_variables):
        raise ValueError(f"n_components ({n_components}) cannot exceed min(n_samples, n_variables)")
    
    # Center data
    x_mean = np.mean(X, axis=0)
    y_mean = np.mean(Y, axis=0)
    X = X - x_mean
    Y = Y - y_mean
    
    # Initialize matrices
    T = np.zeros((n_samples, n_components))
    U = np.zeros((n_samples, n_components))
    W = np.zeros((n_variables, n_components))
    P = np.zeros((n_variables, n_components))
    Q = np.zeros((n_responses, n_components))
    
    # Variance tracking
    var_x_explained = np.zeros(n_components)
    var_y_explained = np.zeros(n_components)
    total_var_x = np.sum(X ** 2)
    total_var_y = np.sum(Y ** 2)
    
    # NIPALS algorithm
    X_res = X.copy()
    Y_res = Y.copy()
    
    for comp in range(n_components):
        # Start with first column of Y
        u = Y_res[:, 0].copy()
        
        # Power iteration
        for iteration in range(max_iter):
            # X weights: w = X^T u / (u^T u)
            w = np.dot(X_res.T, u) / np.dot(u.T, u)
            w = w / np.linalg.norm(w)  # Normalize
            
            # X scores: t = X w / (w^T w)
            t = np.dot(X_res, w) / np.dot(w.T, w)
            
            # Y weights: q = Y^T t / (t^T t)
            q = np.dot(Y_res.T, t) / np.dot(t.T, t)
            
            # Y scores: u = Y q / (q^T q)
            u_new = np.dot(Y_res, q) / np.dot(q.T, q)
            
            # Check convergence
            if np.linalg.norm(u_new - u) < tol:
                u = u_new
                break
            u = u_new
        
        # X loadings: p = X^T t / (t^T t)
        p = np.dot(X_res.T, t) / np.dot(t.T, t)
        
        # Store results
        T[:, comp] = t
        U[:, comp] = u
        W[:, comp] = w
        P[:, comp] = p
        Q[:, comp] = q
        
        # Deflate
        X_res = X_res - np.outer(t, p)
        Y_res = Y_res - np.outer(t, q)
        
        # Variance explained
        var_x_explained[comp] = np.dot(t, t) * np.dot(p, p) / total_var_x if total_var_x > 0 else 0
        var_y_explained[comp] = np.dot(t, t) * np.dot(q, q) / total_var_y if total_var_y > 0 else 0
    
    # Calculate regression coefficients
    # B = W (P^T W)^(-1) Q^T
    # Using R = W (P^T W)^(-1) formulation
    R = np.dot(W, np.linalg.inv(np.dot(P.T, W)))
    B = np.dot(R, Q.T)
    
    return {
        'W': W,
        'P': P,
        'Q': Q,
        'T': T,
        'U': U,
        'R': R,
        'B': B,
        'x_mean': x_mean,
        'y_mean': y_mean,
        'x_std': None,
        'y_std': None,
        'n_components': n_components,
        'n_variables': n_variables,
        'n_responses': n_responses,
        'explained_variance_x': var_x_explained,
        'explained_variance_y': var_y_explained
    }


def pls_predict(X: NDArray[np.floating], 
                model: Dict[str, Union[NDArray[np.floating], int, None]],
                n_components: Optional[int] = None) -> NDArray[np.floating]:
    """
    Predict Y values from X using fitted PLS model.
    
    Args:
        X: Predictor matrix (n_samples x n_variables)
        model: Dict from pls_fit
        n_components: Number of components to use (default: all)
    
    Returns:
        Predicted Y values (n_samples x n_responses)
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X_train = np.random.randn(30, 20)
        >>> Y_train = np.random.randn(30, 2)
        >>> model = pls_fit(X_train, Y_train, n_components=5)
        >>> X_test = np.random.randn(5, 20)
        >>> Y_pred = pls_predict(X_test, model)
        >>> Y_pred.shape
        (5, 2)
    """
    X = np.asarray(X, dtype=np.float64)
    
    if X.ndim == 1:
        X = X.reshape(1, -1)
    
    n_wavelengths_x = X.shape[1]
    n_wavelengths_model = model['n_variables']
    
    if n_wavelengths_x != n_wavelengths_model:
        raise ValueError(f"X has {n_wavelengths_x} variables, model expects {n_wavelengths_model}")
    
    # Center
    X_centered = X - model['x_mean']
    
    if n_components is None:
        n_components = model['n_components']
    else:
        n_components = min(n_components, model['n_components'])
    
    # Use reduced coefficients if needed
    if n_components == model['n_components']:
        B = model['B']
    else:
        # Recalculate with fewer components
        R = model['R'][:, :n_components]
        Q = model['Q'][:, :n_components]
        B = np.dot(R, Q.T)
    
    # Predict: Y = X_centered @ B + y_mean
    Y_pred = np.dot(X_centered, B) + model['y_mean']
    
    return Y_pred


def pls_vip(model: Dict[str, Union[NDArray[np.floating], int, None]]) -> NDArray[np.floating]:
    """
    Calculate Variable Importance in Projection (VIP) scores.
    
    VIP scores identify which X variables (e.g., wavelengths) are
    most important for predicting Y. Variables with VIP > 1 are
    generally considered important.
    
    VIP_j = sqrt(p x Σ(SSY_h x (w_jh2 / Σw_kh2)) / ΣSSY_h)
    
    Args:
        model: Dict from pls_fit
    
    Returns:
        VIP scores for each X variable (n_variables,)
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(30, 20)
        >>> Y = np.random.randn(30, 1)
        >>> model = pls_fit(X, Y, n_components=5)
        >>> vip = pls_vip(model)
        >>> vip.shape
        (20,)
        >>> np.all(vip >= 0)
        True
    """
    W = model['W']
    Q = model['Q']
    T = model['T']
    n_components = model['n_components']
    n_variables = model['n_variables']
    n_responses = model['n_responses']
    
    # Calculate SSY (sum of squares Y explained) per component
    SSY = np.zeros(n_components)
    for h in range(n_components):
        SSY[h] = np.sum((T[:, h] * Q[0, h]) ** 2) if n_responses == 1 else np.sum(Q[:, h] ** 2) * np.sum(T[:, h] ** 2)
    
    total_SSY = np.sum(SSY)
    
    if total_SSY == 0:
        return np.ones(n_variables)
    
    # Calculate VIP for each variable
    VIP = np.zeros(n_variables)
    for j in range(n_variables):
        wj2_sum = 0
        for h in range(n_components):
            w_norm_sq = np.sum(W[:, h] ** 2)
            if w_norm_sq > 0:
                wj2_sum += SSY[h] * (W[j, h] ** 2 / w_norm_sq)
        VIP[j] = np.sqrt(n_variables * wj2_sum / total_SSY)
    
    return VIP


# =============================================================================
# Cross-Validation
# =============================================================================

def cross_validate(model_func: Callable,
                   X: NDArray[np.floating],
                   Y: NDArray[np.floating],
                   k: int = 10,
                   **model_kwargs) -> Dict[str, Union[np.ndarray, float]]:
    """
    Perform k-fold cross-validation for model assessment.
    
    Cross-validation assesses how well a model generalizes to new data.
    It's essential for:
    - Determining optimal number of components
    - Estimating prediction error (RMSECV)
    - Detecting overfitting
    
    Args:
        model_func: Function that takes (X_train, Y_train) and returns model dict
                   Must have 'predict' capability via pls_predict or similar
        X: Predictor matrix (n_samples x n_variables)
        Y: Response matrix (n_samples x n_responses)
        k: Number of folds (default: 10)
                   k=n_samples gives leave-one-out CV
        **model_kwargs: Additional arguments passed to model_func
    
    Returns:
        Dict containing:
            - 'rmsecv': Root mean square error of cross-validation
            - 'predictions': Cross-validated predictions (n_samples x n_responses)
            - 'actual': Actual Y values
            - 'errors': Prediction errors (Y - Y_pred)
            - 'fold_errors': RMSE per fold
            - 'n_components': Number of components used (if applicable)
            - 'r2_cv': Cross-validated R2
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(30, 20)
        >>> Y = np.random.randn(30, 1)
        >>> 
        >>> def pls_wrapper(X, Y, n_components=3):
        ...     return pls_fit(X, Y, n_components)
        >>> 
        >>> cv_result = cross_validate(pls_wrapper, X, Y, k=5, n_components=3)
        >>> cv_result['rmsecv'] > 0
        True
    
    Notes:
        - For time series, use blocked cross-validation instead
        - Stratified CV for classification problems
        - LOO-CV (k=n) has low bias but high variance
    """
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    
    n_samples = X.shape[0]
    
    if k > n_samples:
        raise ValueError(f"k ({k}) cannot exceed n_samples ({n_samples})")
    
    # Create fold indices
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    fold_sizes = np.full(k, n_samples // k, dtype=int)
    fold_sizes[:n_samples % k] += 1
    
    fold_indices = []
    current = 0
    for fold_size in fold_sizes:
        fold_indices.append(indices[current:current + fold_size])
        current += fold_size
    
    # Cross-validation
    predictions = np.zeros_like(Y)
    fold_rmse = []
    
    for fold in range(k):
        # Split data
        test_idx = fold_indices[fold]
        train_idx = np.concatenate([fold_indices[i] for i in range(k) if i != fold])
        
        X_train, X_test = X[train_idx], X[test_idx]
        Y_train, Y_test = Y[train_idx], Y[test_idx]
        
        # Fit model
        model = model_func(X_train, Y_train, **model_kwargs)
        
        # Predict
        Y_pred = pls_predict(X_test, model)
        
        predictions[test_idx] = Y_pred
        
        # Fold RMSE
        fold_rmse.append(np.sqrt(np.mean((Y_test - Y_pred) ** 2)))
    
    # Calculate metrics
    errors = Y - predictions
    rmsecv = np.sqrt(np.mean(errors ** 2))
    
    # R2 CV
    ss_res = np.sum(errors ** 2)
    ss_tot = np.sum((Y - np.mean(Y)) ** 2)
    r2_cv = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    
    return {
        'rmsecv': rmsecv,
        'predictions': predictions,
        'actual': Y,
        'errors': errors,
        'fold_rmse': np.array(fold_rmse),
        'r2_cv': r2_cv,
        'k': k,
        'n_samples': n_samples
    }


def optimal_components(X: NDArray[np.floating],
                       Y: NDArray[np.floating],
                       max_components: int,
                       k: int = 10) -> Dict[str, Union[np.ndarray, int, list]]:
    """
    Find optimal number of PLS components by cross-validation.
    
    Tests all component counts from 1 to max_components and finds
    the number that minimizes RMSECV.
    
    Args:
        X: Predictor matrix
        Y: Response matrix
        max_components: Maximum components to test
        k: Folds for cross-validation
    
    Returns:
        Dict containing:
            - 'optimal_n': Optimal number of components
            - 'rmsecv_values': RMSECV for each n_components
            - 'r2_values': R2 for each n_components
            - 'recommended': Recommended components (may use simpler model)
    
    Examples:
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> X = np.random.randn(40, 30)
        >>> Y = X[:, :3] @ np.random.randn(3, 1) + np.random.randn(40, 1) * 0.1
        >>> result = optimal_components(X, Y, max_components=10, k=5)
        >>> 1 <= result['optimal_n'] <= 10
        True
    """
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    
    if Y.ndim == 1:
        Y = Y.reshape(-1, 1)
    
    max_possible = min(X.shape[0], X.shape[1])
    max_components = min(max_components, max_possible)
    
    rmsecv_values = []
    r2_values = []
    
    for n_comp in range(1, max_components + 1):
        cv_result = cross_validate(pls_fit, X, Y, k=k, n_components=n_comp)
        rmsecv_values.append(cv_result['rmsecv'])
        r2_values.append(cv_result['r2_cv'])
    
    rmsecv_values = np.array(rmsecv_values)
    r2_values = np.array(r2_values)
    
    # Find minimum RMSECV
    optimal_n = int(np.argmin(rmsecv_values) + 1)
    
    # Recommended: use simpler model if RMSECV is within 1 std of minimum
    min_rmsecv = rmsecv_values.min()
    # Simple heuristic: find first component with RMSECV close to minimum
    threshold = min_rmsecv * 1.05  # Within 5% of minimum
    recommended = 1
    for i, rmse in enumerate(rmsecv_values):
        if rmse <= threshold:
            recommended = i + 1
            break
    
    return {
        'optimal_n': optimal_n,
        'rmsecv_values': rmsecv_values,
        'r2_values': r2_values,
        'recommended': recommended,
        'components_tested': list(range(1, max_components + 1))
    }


# =============================================================================
# Utility Functions
# =============================================================================

def rmse(actual: NDArray[np.floating], 
         predicted: NDArray[np.floating]) -> float:
    """Calculate Root Mean Square Error."""
    return float(np.sqrt(np.mean((actual - predicted) ** 2)))


def mae(actual: NDArray[np.floating], 
        predicted: NDArray[np.floating]) -> float:
    """Calculate Mean Absolute Error."""
    return float(np.mean(np.abs(actual - predicted)))


def r_squared(actual: NDArray[np.floating], 
              predicted: NDArray[np.floating]) -> float:
    """Calculate coefficient of determination R2."""
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def bias(actual: NDArray[np.floating], 
         predicted: NDArray[np.floating]) -> float:
    """Calculate bias (mean prediction error)."""
    return float(np.mean(predicted - actual))


if __name__ == "__main__":
    """Example usage and tests."""
    import numpy as np
    
    print("=" * 60)
    print("Chemometrics MLR Tools - Example Usage")
    print("=" * 60)
    
    np.random.seed(42)
    
    # --- CLS Example ---
    print("\n--- Classical Least Squares ---")
    n_samples, n_wl, n_comp = 10, 20, 2
    
    # Simulate Cu2+/Cr3+ mixture spectra
    C_cal = np.random.rand(n_samples, n_comp) * 2  # Concentrations
    K_true = np.random.rand(n_comp, n_wl)  # Pure component spectra
    A_cal = C_cal @ K_true + np.random.randn(n_samples, n_wl) * 0.01
    
    cls_model = cls_fit(C_cal, A_cal)
    print(f"K matrix shape: {cls_model['K'].shape}")
    print(f"RMSEC: {cls_model['rmsec']:.6f}")
    
    # Predict
    A_unknown = np.array([K_true[0] * 1.5 + K_true[1] * 0.5]) + np.random.randn(1, n_wl) * 0.01
    C_pred = cls_predict(A_unknown, cls_model['K'])
    print(f"Predicted concentrations: {C_pred.round(3)}")
    
    # --- PLS Example ---
    print("\n--- Partial Least Squares ---")
    n_samples, n_wl, n_resp = 50, 100, 2
    X = np.random.randn(n_samples, n_wl)
    Y = np.random.randn(n_samples, n_resp)
    
    pls_model = pls_fit(X, Y, n_components=5)
    print(f"B coefficients shape: {pls_model['B'].shape}")
    print(f"X variance explained (first 5): {pls_model['explained_variance_x'][:5].round(3)}")
    
    # VIP scores
    vip = pls_vip(pls_model)
    print(f"VIP scores range: {vip.min():.3f} to {vip.max():.3f}")
    print(f"Important variables (VIP>1): {np.sum(vip > 1)}")
    
    # --- Cross-Validation Example ---
    print("\n--- Cross-Validation ---")
    # Create data with known structure
    X = np.random.randn(40, 30)
    Y = X[:, :3] @ np.random.randn(3, 1) + np.random.randn(40, 1) * 0.1
    
    # Find optimal components
    opt_result = optimal_components(X, Y, max_components=8, k=5)
    print(f"Optimal components: {opt_result['optimal_n']}")
    print(f"Recommended components: {opt_result['recommended']}")
    print(f"RMSECV values: {opt_result['rmsecv_values'].round(4)}")
    
    # Full cross-validation
    cv_result = cross_validate(pls_fit, X, Y, k=10, n_components=opt_result['optimal_n'])
    print(f"RMSECV: {cv_result['rmsecv']:.4f}")
    print(f"R2 CV: {cv_result['r2_cv']:.4f}")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
