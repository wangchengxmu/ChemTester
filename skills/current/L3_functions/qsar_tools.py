"""
L3 Implementation: QSAR Tools
Source: L2_principles/qsar.md

This module provides functions for Quantitative Structure-Activity Relationships.

## Solver Instructions (for AI Agent)

When you encounter QSAR (Quantitative Structure-Activity Relationship) problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Drug-likeness check**: Given molecular properties (MW, logP, HBD, HBA) -> check Lipinski's Rule of Five
- **Similarity**: Given two molecular fingerprints -> calculate Tanimoto similarity
- **Applicability domain**: Given training and test set descriptors -> determine if predictions are reliable
- **Hansch analysis**: Given substituent constants (σ, pi, Es) and biological activity -> build QSAR equation
- **Topological descriptors**: Given molecular structure -> calculate Wiener index, Balaban index

### Step 2: Choose the correct function
- `lipinski_rule_of_five(properties)` -> (num_violations, [list of violations])
  - properties dict needs keys: 'mw', 'logp', 'hbd', 'hba'
- `tanimoto_similarity(fp1, fp2)` -> coefficient 0-1 (sets of fingerprint bits)
- `applicability_domain(X_train, X_test, ...)` -> leverage values, AD assessment
- `hansch_equation(coeffs, descriptors)` -> predicted log(1/C) = ρσ + pi(logP) + deltaEs + const
- `wiener_index(adj_matrix)` -> sum of shortest path distances
- `balaban_index(adj_matrix)` -> distance-connectivity index

### Step 3: Handle special cases
- Lipinski: ≤1 violation is generally acceptable for drug candidates
- Tanimoto: >0.7 indicates similar molecules; empty sets return 1.0
- Applicability domain: leverage > 3p/n means prediction is unreliable
- Hansch: different σ for meta vs para substituents (σ_m vs σ_p)

### Examples
1. **Lipinski check**: MW=350, logP=3.2, HBD=1, HBA=4
   -> `lipinski_rule_of_five({'mw': 350, 'logp': 3.2, 'hbd': 1, 'hba': 4})` -> (0, []) - drug-like

2. **Tanimoto similarity**: fp1={1,2,3,4,5}, fp2={3,4,5,6,7}
   -> `tanimoto_similarity({1,2,3,4,5}, {3,4,5,6,7})` -> |{3,4,5}|/|{1,2,3,4,5,6,7}| = 3/7 ~ 0.4286

3. **Lipinski violation**: MW=600, logP=6, HBD=3, HBA=12
   -> `lipinski_rule_of_five({'mw': 600, 'logp': 6, 'hbd': 3, 'hba': 12})` -> (3, ['MW > 500 Da', 'logP > 5', 'HBA > 10'])
"""

import math
from typing import Dict, List, Tuple, Optional, Set
import numpy as np


def lipinski_rule_of_five(properties: Dict[str, float]) -> Tuple[int, List[str]]:
    """
    Check Lipinski's Rule of Five for drug-likeness.
    
    Rules:
    - MW ≤ 500 Da
    - logP ≤ 5
    - HBD (H-bond donors) ≤ 5
    - HBA (H-bond acceptors) ≤ 10
    
    Args:
        properties: Dictionary with keys 'mw', 'logp', 'hbd', 'hba'
    
    Returns:
        Tuple of (number of violations, list of violations)
    
    Examples:
        >>> lipinski_rule_of_five({'mw': 300, 'logp': 2.5, 'hbd': 2, 'hba': 5})
        (0, [])
        >>> lipinski_rule_of_five({'mw': 600, 'logp': 2, 'hbd': 2, 'hba': 5})
        (1, ['MW > 500 Da'])
    """
    violations = []
    
    if properties.get('mw', 0) > 500:
        violations.append('MW > 500 Da')
    if properties.get('logp', 0) > 5:
        violations.append('logP > 5')
    if properties.get('hbd', 0) > 5:
        violations.append('HBD > 5')
    if properties.get('hba', 0) > 10:
        violations.append('HBA > 10')
    
    return len(violations), violations


def tanimoto_similarity(fp1: Set, fp2: Set) -> float:
    """
    Calculate Tanimoto similarity between two fingerprints.
    
    T = |A ∩ B| / |A ∪ B|
    
    Args:
        fp1: First fingerprint as set of bits
        fp2: Second fingerprint as set of bits
    
    Returns:
        Tanimoto coefficient (0-1)
    
    Examples:
        >>> tanimoto_similarity({1,2,3,4}, {3,4,5,6})
        0.3333
        >>> tanimoto_similarity({1,2,3}, {1,2,3})
        1.0
    """
    if not fp1 and not fp2:
        return 1.0
    
    intersection = len(fp1 & fp2)
    union = len(fp1 | fp2)
    
    if union == 0:
        return 1.0
    
    return round(intersection / union, 4)


def applicability_domain(X_train: np.ndarray, X_test: np.ndarray,
                         threshold: float = 3.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate leverage-based applicability domain.
    
    h_i = x_i(X'X)-1x_i'
    h* = 3(p+1)/n
    
    Args:
        X_train: Training set descriptors (n x p)
        X_test: Test set descriptors (m x p)
        threshold: Multiplier for h* (default: 3.0)
    
    Returns:
        Tuple of (leverage values, AD status: True if inside AD)
    
    Examples:
        >>> import numpy as np
        >>> X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        >>> X_test = np.array([[2, 3], [10, 20]])
        >>> h, ad = applicability_domain(X_train, X_test)
    """
    n, p = X_train.shape
    
    # Calculate (X'X)-1
    XtX = X_train.T @ X_train
    
    try:
        XtX_inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        # Use pseudo-inverse for singular matrix
        XtX_inv = np.linalg.pinv(XtX)
    
    # Calculate leverage for test samples
    h_values = np.array([x @ XtX_inv @ x.T for x in X_test])
    
    # Warning leverage
    h_star = threshold * (p + 1) / n
    
    # AD status
    inside_AD = h_values <= h_star
    
    return h_values, inside_AD


def vif(X: np.ndarray, feature_names: List[str] = None) -> Dict[str, float]:
    """
    Calculate Variance Inflation Factor for multicollinearity.
    
    VIF = 1 / (1 - R2)
    
    VIF > 5 indicates problematic multicollinearity.
    VIF > 10 indicates severe multicollinearity.
    
    Args:
        X: Feature matrix (n x p)
        feature_names: Optional list of feature names
    
    Returns:
        Dictionary mapping feature name to VIF
    
    Examples:
        >>> import numpy as np
        >>> X = np.array([[1, 2, 4], [2, 4, 8], [3, 6, 12]])  # Collinear
        >>> vifs = vif(X, ['a', 'b', 'c'])
    """
    if feature_names is None:
        feature_names = [f'X{i}' for i in range(X.shape[1])]
    
    vif_values = {}
    
    for i, name in enumerate(feature_names):
        # Regress feature i on all others
        y = X[:, i]
        X_others = np.delete(X, i, axis=1)
        
        # Add intercept
        X_with_intercept = np.column_stack([np.ones(len(y)), X_others])
        
        try:
            # OLS solution
            beta = np.linalg.lstsq(X_with_intercept, y, rcond=None)[0]
            y_pred = X_with_intercept @ beta
            
            # R2
            ss_res = np.sum((y - y_pred)**2)
            ss_tot = np.sum((y - np.mean(y))**2)
            
            if ss_tot == 0:
                r2 = 1.0
            else:
                r2 = 1 - ss_res / ss_tot
            
            # VIF
            if r2 >= 1:
                vif_val = float('inf')
            else:
                vif_val = 1 / (1 - r2)
        except:
            vif_val = float('inf')
        
        vif_values[name] = round(vif_val, 2)
    
    return vif_values


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Root Mean Square Error."""
    return np.sqrt(np.mean((y_true - y_pred)**2))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Mean Absolute Error."""
    return np.mean(np.abs(y_true - y_pred))


def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Coefficient of Determination R2."""
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    return 1 - ss_res / ss_tot


def q2_loo(y_true: np.ndarray, y_pred_loo: np.ndarray) -> float:
    """
    Calculate Q2 for leave-one-out cross-validation.
    
    Q2 = 1 - Σ(y_i - ŷ_i)2 / Σ(y_i - ȳ)2
    
    Args:
        y_true: Actual values
        y_pred_loo: Predicted values from LOO-CV
    
    Returns:
        Q2 value
    """
    return r_squared(y_true, y_pred_loo)


# ============================================================================
# Self-test
# ============================================================================

if __name__ == '__main__':
    print("QSAR Tools Test")
    print("=" * 40)
    
    # Test Lipinski
    print("\nLipinski Rule of Five:")
    aspirin = {'mw': 180.16, 'logp': 1.19, 'hbd': 1, 'hba': 4}
    violations, details = lipinski_rule_of_five(aspirin)
    print(f"  Aspirin: {violations} violations")
    
    large_molecule = {'mw': 600, 'logp': 6, 'hbd': 3, 'hba': 8}
    violations, details = lipinski_rule_of_five(large_molecule)
    print(f"  Large molecule: {violations} violations - {details}")
    
    # Test Tanimoto
    print("\nTanimoto Similarity:")
    print(f"  {{1,2,3}} vs {{1,2,3}}: {tanimoto_similarity({1,2,3}, {1,2,3})}")
    print(f"  {{1,2,3}} vs {{4,5,6}}: {tanimoto_similarity({1,2,3}, {4,5,6})}")
    
    # Test AD
    print("\nApplicability Domain:")
    X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    X_test = np.array([[2, 3], [10, 20]])
    h, ad = applicability_domain(X_train, X_test)
    print(f"  Test sample 1: h={h[0]:.3f}, in AD: {ad[0]}")
    print(f"  Test sample 2: h={h[1]:.3f}, in AD: {ad[1]}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="applicability_domain",
            description="Calculate leverage-based applicability domain.",
            input_schema=[
            InputSchemaField(name="X_train", type="number", required=True),
            InputSchemaField(name="X_test", type="number", required=True),
            InputSchemaField(name="threshold", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lipinski_rule_of_five",
            description="Check Lipinski's Rule of Five for drug-likeness.",
            input_schema=[
            InputSchemaField(name="properties", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mae",
            description="Calculate Mean Absolute Error.",
            input_schema=[
            InputSchemaField(name="y_true", type="number", required=True),
            InputSchemaField(name="y_pred", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="q2_loo",
            description="Calculate Q2 for leave-one-out cross-validation.",
            input_schema=[
            InputSchemaField(name="y_true", type="number", required=True),
            InputSchemaField(name="y_pred_loo", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="r_squared",
            description="Calculate Coefficient of Determination R2.",
            input_schema=[
            InputSchemaField(name="y_true", type="number", required=True),
            InputSchemaField(name="y_pred", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rmse",
            description="Calculate Root Mean Square Error.",
            input_schema=[
            InputSchemaField(name="y_true", type="number", required=True),
            InputSchemaField(name="y_pred", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tanimoto_similarity",
            description="Calculate Tanimoto similarity between two fingerprints.",
            input_schema=[
            InputSchemaField(name="fp1", type="number", required=True),
            InputSchemaField(name="fp2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vif",
            description="Calculate Variance Inflation Factor for multicollinearity.",
            input_schema=[
            InputSchemaField(name="X", type="number", required=True),
            InputSchemaField(name="feature_names", type="string", required=False)
            ],
            handler="{name}",
        )
    ]
