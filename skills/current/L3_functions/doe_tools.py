"""
DOE Tools (G21) - Design of Experiments calculations

Provides functions for factorial designs, response surface methods,
Taguchi analysis, and simplex optimization.

## Solver Instructions (for AI Agent)

When you encounter Design of Experiments (DOE) problems:

### Step 1: Identify what is given and what is asked
- Given: number of factors (k), responses, experimental goal
- Asked: design matrix, effect estimates, ANOVA, optimal settings

### Step 2: Choose the correct function
- `full_factorial_design(k)`: 2^k design with coded levels (-1, +1)
- `interaction_columns(design)`: Add interaction columns
- `fractional_factorial(k, p, generators)`: 2^(k-p) fractional design
- `calculate_effects(design, responses)`: Main + interaction effects
- `coded_regression(design, responses)`: Regression coefficients (beta = effect/2)
- `uncoded_equation(coded_coefs, design, high_levels, low_levels)`: Convert to real units
- `anova_table(design, responses, alpha)`: ANOVA SS, MS, F, p
- `ccd_design(k, alpha, center_reps)`: Central Composite Design
- `box_behnken_design(k, center_reps)`: Box-Behnken Design
- `simplex_optimize(func, x0, step)`: Nelder-Mead optimization
- `taguchi_sn(ratios, goal)`: Signal-to-noise ratio
- `taguchi_orthogonal_array(array_type)`: L4, L8, L9, L12, L16 arrays

### Step 3: Handle special cases
- 2^k with k>4 requires many runs; use fractional factorial to reduce
- Resolution III: main effects confounded with 2-factor interactions
- CCD adds axial + center points to factorial for RSM

### Examples
```python
design = full_factorial_design(3)  # 2^3 = 8 runs
effects = calculate_effects(design, np.array([28,17,41,34,56,51,42,36]))
ccd, types = ccd_design(2)  # CCD for 2 factors
```
"""

import numpy as np
from itertools import product, combinations
from typing import List, Tuple, Dict, Optional, Callable


def full_factorial_design(k: int) -> np.ndarray:
    """Generate a 2^k full factorial design matrix with coded levels (-1, +1).
    
    Args:
        k: Number of factors
    
    Returns:
        Design matrix of shape (2^k, k) with columns for each factor
    """
    N = 2 ** k
    design = np.ones((N, k))
    for j in range(k):
        design[:, j] = [1 if (i >> j) & 1 else -1 for i in range(N)]
    return design


def interaction_columns(design: np.ndarray) -> np.ndarray:
    """Add all interaction columns to a design matrix.
    
    Args:
        design: Original design matrix (N x k) with -1/+1 coded levels
    
    Returns:
        Extended design matrix with interaction columns appended
    """
    k = design.shape[1]
    columns = [design]
    for order in range(2, k + 1):
        for combo in combinations(range(k), order):
            col = np.ones(design.shape[0])
            for idx in combo:
                col *= design[:, idx]
            columns.append(col.reshape(-1, 1))
    return np.hstack(columns)


def fractional_factorial(k: int, p: int, generators: Optional[List[int]] = None) -> Tuple[np.ndarray, List[str]]:
    """Generate a 2^(k-p) fractional factorial design.
    
    Args:
        k: Total number of factors
        p: Number of generators (fractionation level)
        generators: List of integers specifying which basic columns to use
                   for generating extra factors. Default uses standard generators.
    
    Returns:
        (design_matrix, alias_labels)
    """
    base_k = k - p
    base = full_factorial_design(base_k)
    
    if generators is None:
        # Default: use first p columns as generators for columns base_k to k-1
        generators = list(range(p))
    
    extra_cols = []
    for i in range(p):
        gen_col = generators[i]
        new_col = np.copy(base[:, gen_col])
        if i > 0:
            new_col *= base[:, generators[i - 1]]
        extra_cols.append(new_col)
    
    if extra_cols:
        extra = np.column_stack(extra_cols)
        design = np.hstack([base, extra])
    else:
        design = base
    
    labels = [f"F{i+1}" for i in range(k)]
    return design, labels


def calculate_effects(design: np.ndarray, responses: np.ndarray,
                      factor_names: Optional[List[str]] = None) -> Dict[str, float]:
    """Calculate main effects and interaction effects for a 2^k design.
    
    Args:
        design: Design matrix (N x k) with -1/+1 coded levels
        responses: Response vector (N,)
        factor_names: Optional list of factor names (e.g., ["X","Y","Z"]).
            If None, defaults to ["A","B","C",...]. Column 0 maps to
            factor_names[0], column 1 to factor_names[1], etc.
    
    Returns:
        Dictionary mapping effect names to values
    """
    N = len(responses)
    k = design.shape[1]
    
    if factor_names is None:
        factor_names = [chr(65 + i) for i in range(k)]  # A, B, C, ...
    elif len(factor_names) != k:
        raise ValueError(f"factor_names has {len(factor_names)} entries but design has {k} columns")
    
    # Build contrast matrix
    contrasts = [design[:, i] for i in range(k)]
    names = [f"E_{factor_names[i]}" for i in range(k)]
    
    for order in range(2, k + 1):
        for combo in combinations(range(k), order):
            col = np.ones(N)
            name = ""
            for idx in combo:
                col *= design[:, idx]
                name += factor_names[idx]
            contrasts.append(col)
            names.append(f"E_{name}")
    
    effects = {}
    for name, contrast in zip(names, contrasts):
        # Effect = (2/N) * sum(contrast * response)
        effects[name] = float(np.sum(contrast * responses) * 2.0 / N)
    
    # Intercept
    effects["beta_0"] = float(np.mean(responses))
    
    return effects


def coded_regression(design: np.ndarray, responses: np.ndarray,
                     factor_names: Optional[List[str]] = None) -> Dict[str, float]:
    """Fit a coded linear regression model for a factorial design.
    
    Args:
        design: Design matrix (N x k)
        responses: Response vector (N,)
        factor_names: Optional list of factor names (passed to calculate_effects)
    
    Returns:
        Dictionary of regression coefficients (half the effect values)
    """
    effects = calculate_effects(design, responses, factor_names=factor_names)
    coefs = {}
    coefs["beta_0"] = effects["beta_0"]
    for key in effects:
        if key != "beta_0":
            coefs[key.replace("E_", "beta_")] = effects[key] / 2.0
    return coefs


def uncoded_equation(coded_coefs: Dict[str, float], 
                     design: np.ndarray,
                     high_levels: np.ndarray,
                     low_levels: np.ndarray,
                     response_name: str = "R") -> str:
    """Convert coded regression coefficients to uncoded equation string.
    
    Args:
        coded_coefs: Dictionary of coded beta coefficients
        design: Design matrix used
        high_levels: Array of high-level values for each factor
        low_levels: Array of low-level values for each factor
        response_name: Name of the response variable
    
    Returns:
        String representation of the uncoded equation
    """
    mid = (high_levels + low_levels) / 2.0
    step = (high_levels - low_levels) / 2.0
    k = len(high_levels)
    terms = []
    
    # For simplicity, only handle main effects
    beta_0 = coded_coefs.get("beta_0", 0)
    for i in range(k):
        key = f"beta_{chr(65+i)}"
        beta_i = coded_coefs.get(key, 0)
        if abs(beta_i) > 1e-10:
            uncoded_coef = beta_i / step[i]
            terms.append(f"{uncoded_coef:+.4f}*F{i+1}")
    
    intercept = beta_0 - sum(coded_coefs.get(f"beta_{chr(65+i)}", 0) * mid[i] / step[i] 
                              for i in range(k) 
                              if abs(coded_coefs.get(f"beta_{chr(65+i)}", 0)) > 1e-10)
    
    eq = f"{response_name} = {intercept:.4f}"
    for t in terms:
        eq += f" {t}"
    return eq


def anova_table(design: np.ndarray, responses: np.ndarray, alpha: float = 0.05) -> Dict:
    """One-way ANOVA for factorial design.
    
    Args:
        design: Design matrix
        responses: Response vector
        alpha: Significance level
    
    Returns:
        Dictionary with SS, MS, F, and p-values
    """
    N = len(responses)
    effects = calculate_effects(design, responses)
    k = design.shape[1]
    
    SS_total = float(np.sum((responses - np.mean(responses))**2))
    SS_model = 0.0
    
    factor_results = {}
    for key, val in effects.items():
        if key == "beta_0":
            continue
        ss = (val**2 * N) / 4.0  # SS for each effect
        factor_results[key] = {"effect": val, "SS": ss}
        SS_model += ss
    
    SS_error = SS_total - SS_model
    df_model = 2**k - 1
    df_error = N - 2**k
    df_total = N - 1
    
    MS_model = SS_model / df_model if df_model > 0 else 0
    MS_error = SS_error / df_error if df_error > 0 else 1e-10
    F_value = MS_model / MS_error
    
    from scipy import stats
    p_value = 1.0 - stats.f.cdf(F_value, df_model, df_error) if df_error > 0 else 1.0
    
    return {
        "SS_model": SS_model, "SS_error": SS_error, "SS_total": SS_total,
        "df_model": df_model, "df_error": df_error, "df_total": df_total,
        "MS_model": MS_model, "MS_error": MS_error,
        "F": F_value, "p_value": p_value,
        "significant": p_value < alpha,
        "factor_results": factor_results
    }


def ccd_design(k: int, alpha: float = None, center_reps: int = 6) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a Central Composite Design.
    
    Args:
        k: Number of factors
        alpha: Axial distance (default: 2^(k/4) for rotatability)
        center_reps: Number of center point replicates
    
    Returns:
        (design_matrix, point_types) where point_types: 0=factorial, 1=axial, 2=center
    """
    if alpha is None:
        alpha = 2 ** (k / 4.0)
    
    # Factorial points
    factorial = full_factorial_design(k)
    n_fact = len(factorial)
    
    # Axial points
    axial = np.zeros((2 * k, k))
    for i in range(k):
        axial[2*i, i] = alpha
        axial[2*i+1, i] = -alpha
    
    # Center points
    center = np.zeros((center_reps, k))
    
    design = np.vstack([factorial, axial, center])
    types = np.array([0]*n_fact + [1]*(2*k) + [2]*center_reps)
    
    return design, types


def box_behnken_design(k: int, center_reps: int = 3) -> np.ndarray:
    """Generate a Box-Behnken Design for k factors (3 ≤ k ≤ 7).
    
    Args:
        k: Number of factors (must be ≥ 3)
        center_reps: Number of center point replicates
    
    Returns:
        Design matrix
    """
    if k < 3:
        raise ValueError("Box-Behnken requires at least 3 factors")
    
    runs = []
    # For each pair of factors, create runs at their edge midpoints
    for i in range(k):
        for j in range(i + 1, k):
            for level_i in [-1, 1]:
                for level_j in [-1, 1]:
                    row = np.zeros(k)
                    row[i] = level_i
                    row[j] = level_j
                    runs.append(row)
    
    # Center points
    for _ in range(center_reps):
        runs.append(np.zeros(k))
    
    return np.array(runs)


def simplex_optimize(func: Callable, x0: np.ndarray, step: float = 1.0,
                     max_iter: int = 200, tol: float = 1e-8) -> Dict:
    """Fixed-size simplex optimization (Nelder-Mead variant).
    
    Args:
        func: Objective function (to maximize)
        x0: Starting point
        step: Initial step size
        max_iter: Maximum iterations
        tol: Convergence tolerance
    
    Returns:
        Dictionary with optimum point, value, and trajectory
    """
    k = len(x0)
    
    # Initialize simplex
    simplex = np.zeros((k + 1, k))
    simplex[0] = np.array(x0, dtype=float)
    for i in range(k):
        simplex[i + 1] = np.array(x0, dtype=float)
        simplex[i + 1, i] += step
    
    values = np.array([func(simplex[i]) for i in range(k + 1)])
    trajectory = [simplex[0].copy()]
    
    for iteration in range(max_iter):
        # Sort vertices by value (worst first for maximization)
        order = np.argsort(values)  # ascending
        # We want to MAXIMIZE, so best is last
        worst_idx = order[0]
        best_idx = order[-1]
        
        # Check convergence
        if np.std(values) < tol:
            break
        
        # Centroid of all vertices except worst
        centroid = np.mean(np.delete(simplex, worst_idx, axis=0), axis=0)
        
        # Reflection
        reflected = centroid + (centroid - simplex[worst_idx])
        reflected_val = func(reflected)
        
        if reflected_val > values[best_idx]:
            # Expansion
            expanded = centroid + 2.0 * (reflected - centroid)
            expanded_val = func(expanded)
            if expanded_val > reflected_val:
                simplex[worst_idx] = expanded
                values[worst_idx] = expanded_val
            else:
                simplex[worst_idx] = reflected
                values[worst_idx] = reflected_val
        elif reflected_val > values[np.argsort(values)[1]]:
            # Better than second worst
            simplex[worst_idx] = reflected
            values[worst_idx] = reflected_val
        else:
            # Contraction
            contracted = centroid + 0.5 * (simplex[worst_idx] - centroid)
            contracted_val = func(contracted)
            if contracted_val > values[worst_idx]:
                simplex[worst_idx] = contracted
                values[worst_idx] = contracted_val
            else:
                # Shrink
                for i in range(k + 1):
                    if i != best_idx:
                        simplex[i] = simplex[best_idx] + 0.5 * (simplex[i] - simplex[best_idx])
                        values[i] = func(simplex[i])
        
        best_idx = np.argmax(values)
        trajectory.append(simplex[best_idx].copy())
    
    best_idx = np.argmax(values)
    return {
        "optimum": simplex[best_idx],
        "optimum_value": float(values[best_idx]),
        "iterations": iteration + 1,
        "trajectory": np.array(trajectory)
    }


def taguchi_sn(ratios: np.ndarray, goal: str = "larger_the_better") -> float:
    """Calculate Taguchi signal-to-noise ratio.
    
    Args:
        ratios: Array of response values (multiple measurements per condition)
        goal: 'larger_the_better', 'smaller_the_better', or 'nominal_the_best'
    
    Returns:
        S/N ratio in dB
    """
    n = len(ratios)
    
    if goal == "larger_the_better":
        msd = np.mean(1.0 / ratios**2)  # mean squared deviation
    elif goal == "smaller_the_better":
        msd = np.mean(ratios**2)
    elif goal == "nominal_the_better":
        mean = np.mean(ratios)
        var = np.var(ratios, ddof=1)
        return 10.0 * np.log10(mean**2 / var)
    else:
        raise ValueError(f"Unknown goal: {goal}")
    
    return -10.0 * np.log10(msd)


def taguchi_orthogonal_array(array_type: str) -> np.ndarray:
    """Return standard Taguchi orthogonal array.
    
    Args:
        array_type: 'L4', 'L8', 'L9', 'L12', 'L16', 'L18', 'L27'
    
    Returns:
        Design matrix with coded levels
    """
    arrays = {
        'L4': np.array([[-1,-1,-1], [1,-1,-1], [-1,1,-1], [1,1,1]]),
        'L8': np.array([
            [-1,-1,-1,-1,-1,-1,-1],
            [1,-1,-1,1,-1,1,1],
            [-1,1,-1,1,1,-1,1],
            [1,1,-1,-1,1,1,-1],
            [-1,-1,1,1,1,1,-1],
            [1,-1,1,-1,1,-1,1],
            [-1,1,1,-1,-1,1,1],
            [1,1,1,1,-1,-1,-1]
        ]),
        'L9': np.array([
            [-1,-1,-1,-1],
            [-1,0,0,0],
            [-1,1,1,1],
            [0,-1,0,1],
            [0,0,1,-1],
            [0,1,-1,0],
            [1,-1,1,0],
            [1,0,-1,1],
            [1,1,0,-1]
        ]),
    }
    
    if array_type not in arrays:
        raise ValueError(f"Array type '{array_type}' not available. Use one of: {list(arrays.keys())}")
    
    return arrays[array_type]


# Quick test
if __name__ == "__main__":
    # Test 2^3 factorial
    d = full_factorial_design(3)
    print("2^3 design:")
    print(d)
    
    # Test effects
    r = np.array([28, 17, 41, 34, 56, 51, 42, 36])
    eff = calculate_effects(d, r)
    print("\nEffects:")
    for k, v in eff.items():
        print(f"  {k}: {v:.2f}")
    
    # Test simplex
    def f(x):
        return -(x[0]-3.9)**2 - (x[1]-6.2)**2 + 10  # Parabola
    
    result = simplex_optimize(f, np.array([0.0, 0.0]), step=1.0)
    print(f"\nSimplex optimum: {result['optimum']}, value: {result['optimum_value']:.4f}")
    
    # Test CCD
    ccd, types = ccd_design(2, center_reps=3)
    print(f"\nCCD (k=2): {len(ccd)} runs")
    
    # Test Taguchi S/N
    sn = taguchi_sn(np.array([10.5, 11.2, 10.8]), "nominal_the_better")
    print(f"\nS/N ratio: {sn:.2f} dB")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'anova_table', 'description': 'One-way ANOVA for factorial design.\n\nArgs:\n    design: Design matrix\n    responses: Response vector\n    alpha: Significance level\n\nReturns:\n    Dictionary with SS, MS, F, and p-values', 'inputSchema': {'type': 'object', 'properties': {'design': {'type': 'string', 'description': 'Design'}, 'responses': {'type': 'string', 'description': 'Responses'}, 'alpha': {'type': 'number', 'description': 'Alpha', 'default': 0.05}}, 'required': ['design', 'responses']}},
    {'name': 'box_behnken_design', 'description': 'Generate a Box-Behnken Design for k factors (3 ≤ k ≤ 7).\n\nArgs:\n    k: Number of factors (must be ≥ 3)\n    center_reps: Number of center point replicates\n\nReturns:\n    Design matrix', 'inputSchema': {'type': 'object', 'properties': {'k': {'type': 'number', 'description': 'K'}, 'center_reps': {'type': 'number', 'description': 'Center Reps', 'default': 3}}, 'required': ['k']}},
    {'name': 'calculate_effects', 'description': 'Calculate main effects and interaction effects for a 2^k design.\n\nArgs:\n    design: Design matrix (N x k) with -1/+1 coded levels\n    responses: Response vector (N,)\n\nReturns:\n    Dictionary mapping effect names to values', 'inputSchema': {'type': 'object', 'properties': {'design': {'type': 'string', 'description': 'Design'}, 'responses': {'type': 'string', 'description': 'Responses'}}, 'required': ['design', 'responses']}},
    {'name': 'ccd_design', 'description': 'Generate a Central Composite Design.\n\nArgs:\n    k: Number of factors\n    alpha: Axial distance (default: 2^(k/4) for rotatability)\n    center_reps: Number of center point replicates\n\nReturns:\n    (design_matrix, point_types) where point_types: 0=factorial, 1=axial, 2=center', 'inputSchema': {'type': 'object', 'properties': {'k': {'type': 'number', 'description': 'K'}, 'alpha': {'type': 'number', 'description': 'Alpha', 'default': None}, 'center_reps': {'type': 'number', 'description': 'Center Reps', 'default': 6}}, 'required': ['k']}},
    {'name': 'coded_regression', 'description': 'Fit a coded linear regression model for a factorial design.\n\nArgs:\n    design: Design matrix (N x k)\n    responses: Response vector (N,)\n\nReturns:\n    Dictionary of regression coefficients (half the effect values)', 'inputSchema': {'type': 'object', 'properties': {'design': {'type': 'string', 'description': 'Design'}, 'responses': {'type': 'string', 'description': 'Responses'}}, 'required': ['design', 'responses']}},
    {'name': 'fractional_factorial', 'description': 'Generate a 2^(k-p) fractional factorial design.\n\nArgs:\n    k: Total number of factors\n    p: Number of generators (fractionation level)\n    generators: List of integers specifying which basic columns to use\n               for generating extra factors. Default uses standard generators.\n\nReturns:\n    (design_matrix, alias_labels)', 'inputSchema': {'type': 'object', 'properties': {'k': {'type': 'number', 'description': 'K'}, 'p': {'type': 'number', 'description': 'P'}, 'generators': {'type': 'string', 'description': 'Generators', 'default': None}}, 'required': ['k', 'p']}},
    {'name': 'full_factorial_design', 'description': 'Generate a 2^k full factorial design matrix with coded levels (-1, +1).\n\nArgs:\n    k: Number of factors\n\nReturns:\n    Design matrix of shape (2^k, k) with columns for each factor', 'inputSchema': {'type': 'object', 'properties': {'k': {'type': 'number', 'description': 'K'}}, 'required': ['k']}},
    {'name': 'interaction_columns', 'description': 'Add all interaction columns to a design matrix.\n\nArgs:\n    design: Original design matrix (N x k) with -1/+1 coded levels\n\nReturns:\n    Extended design matrix with interaction columns appended', 'inputSchema': {'type': 'object', 'properties': {'design': {'type': 'string', 'description': 'Design'}}, 'required': ['design']}},
    {'name': 'simplex_optimize', 'description': 'Fixed-size simplex optimization (Nelder-Mead variant).\n\nArgs:\n    func: Objective function (to maximize)\n    x0: Starting point\n    step: Initial step size\n    max_iter: Maximum iterations\n    tol: Convergence tolerance\n\nReturns:\n    Dictionary with optimum point, value, and trajectory', 'inputSchema': {'type': 'object', 'properties': {'func': {'type': 'number', 'description': 'Func'}, 'x0': {'type': 'number', 'description': 'X0'}, 'step': {'type': 'number', 'description': 'Step', 'default': 1.0}, 'max_iter': {'type': 'number', 'description': 'Max Iter', 'default': 200}, 'tol': {'type': 'number', 'description': 'Tol', 'default': 1e-08}}, 'required': ['func', 'x0']}},
    {'name': 'taguchi_orthogonal_array', 'description': "Return standard Taguchi orthogonal array.\n\nArgs:\n    array_type: 'L4', 'L8', 'L9', 'L12', 'L16', 'L18', 'L27'\n\nReturns:\n    Design matrix with coded levels", 'inputSchema': {'type': 'object', 'properties': {'array_type': {'type': 'string', 'description': 'Array Type'}}, 'required': ['array_type']}},
    {'name': 'taguchi_sn', 'description': "Calculate Taguchi signal-to-noise ratio.\n\nArgs:\n    ratios: Array of response values (multiple measurements per condition)\n    goal: 'larger_the_better', 'smaller_the_better', or 'nominal_the_best'\n\nReturns:\n    S/N ratio in dB", 'inputSchema': {'type': 'object', 'properties': {'ratios': {'type': 'number', 'description': 'Ratios'}, 'goal': {'type': 'number', 'description': 'Goal', 'default': 'larger_the_better'}}, 'required': ['ratios']}},
    {'name': 'uncoded_equation', 'description': 'Convert coded regression coefficients to uncoded equation string.\n\nArgs:\n    coded_coefs: Dictionary of coded beta coefficients\n    design: Design matrix used\n    high_levels: Array of high-level values for each factor\n    low_levels: Array of low-level values for each factor\n    response_name: Name of the response variable\n\nReturns:\n    String representation of the uncoded equation', 'inputSchema': {'type': 'object', 'properties': {'coded_coefs': {'type': 'string', 'description': 'Coded Coefs'}, 'design': {'type': 'string', 'description': 'Design'}, 'high_levels': {'type': 'string', 'description': 'High Levels'}, 'low_levels': {'type': 'string', 'description': 'Low Levels'}, 'response_name': {'type': 'string', 'description': 'Response Name', 'default': 'R'}}, 'required': ['coded_coefs', 'design', 'high_levels', 'low_levels']}}
]
