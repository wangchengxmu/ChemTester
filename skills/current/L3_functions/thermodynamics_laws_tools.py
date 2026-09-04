"""
Thermodynamics Laws Tools - L3 Implementation
Chapter 16.3: Second and Third Laws of Thermodynamics
"""

## Solver Instructions (for AI Agent)

# When you encounter **thermodynamic laws** (entropy, spontaneity, third law) problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Entropy of surroundings from DeltaH: `entropy_surroundings(delta_H, T)`
# - Total entropy of universe: `entropy_universe(delta_S_sys, delta_S_surr)`
# - Spontaneity from S_univ: `spontaneity_from_Suniv(delta_S_univ)`
# - Combined: `calculate_Suniv_from_process(delta_S_sys, delta_H_sys, T)`
# - Third law (W=1 for perfect crystal): `third_law_entropy(W)`
# - Standard reaction entropy: `standard_entropy_reaction(S_values)`

### Step 2: Choose the correct function
# - Quick spontaneity check: `calculate_Suniv_from_process` (combines DeltaS_sys, DeltaH_sys, T)
# - Step-by-step: `entropy_surroundings` -> `entropy_universe` -> `spontaneity_from_Suniv`
# - Reaction entropy from tabulated values: `standard_entropy_reaction`

### Step 3: Handle special cases
# - `entropy_surroundings` uses DeltaS_surr = -DeltaH_sys/T (at constant pressure)
# - `standard_entropy_reaction` accepts a dict of species->entropy values with stoichiometry
# - Third law: S -> 0 as T -> 0 for a perfect crystal (W=1)

### Examples
# 1. DeltaH_sys=-100 kJ, T=298 K: `entropy_surroundings(-100000, 298)` -> 335.6 J/(mol·K)
# 2. DeltaS_sys=150 J/K, DeltaS_surr=335.6 J/K: `entropy_universe(150, 335.6)` -> 485.6 J/K > 0, spontaneous
# 3. Shortcut: `calculate_Suniv_from_process(150, -100000, 298)` -> same result with spontaneity determination



from typing import Dict, Tuple, Optional
from math import log


def entropy_universe(delta_S_sys: float, delta_S_surr: float) -> float:
    """
    Calculate entropy change of the universe.
    
    DeltaS_univ = DeltaS_sys + DeltaS_surr
    
    Args:
        delta_S_sys: Entropy change of system (J/K)
        delta_S_surr: Entropy change of surroundings (J/K)
    
    Returns:
        Entropy change of universe (J/K)
    
    Examples:
        >>> entropy_universe(22.1, -22.0)
        0.1
    """
    return delta_S_sys + delta_S_surr


def entropy_surroundings(delta_H: float, T: float) -> float:
    """
    Calculate entropy change of surroundings.
    
    DeltaS_surr = -DeltaH_sys / T
    
    Args:
        delta_H: Enthalpy change of system (J)
        T: Temperature (K)
    
    Returns:
        Entropy change of surroundings (J/K)
    
    Examples:
        >>> entropy_surroundings(-6000, 263.15)
        22.8
    """
    if T <= 0:
        raise ValueError("Temperature must be positive")
    return -delta_H / T


def spontaneity_from_Suniv(delta_S_univ: float) -> str:
    """
    Determine spontaneity from DeltaS_universe.
    
    Args:
        delta_S_univ: Entropy change of universe (J/K)
    
    Returns:
        Spontaneity prediction
    
    Examples:
        >>> spontaneity_from_Suniv(0.9)
        'spontaneous'
        >>> spontaneity_from_Suniv(-0.7)
        'nonspontaneous'
    """
    if delta_S_univ > 0:
        return 'spontaneous'
    elif delta_S_univ < 0:
        return 'nonspontaneous'
    else:
        return 'at equilibrium'


def calculate_Suniv_from_process(delta_S_sys: float, delta_H_sys: float,
                                  T: float) -> Dict:
    """
    Calculate DeltaS_universe from process data.
    
    Args:
        delta_S_sys: Entropy change of system (J/K)
        delta_H_sys: Enthalpy change of system (J)
        T: Temperature (K)
    
    Returns:
        Dict with all calculated values
    
    Examples:
        >>> calculate_Suniv_from_process(22.1, -6000, 283.15)
        {'delta_S_sys': 22.1, 'delta_S_surr': 21.2, 'delta_S_univ': 43.3, 'spontaneity': 'spontaneous'}
    """
    delta_S_surr = entropy_surroundings(delta_H_sys, T)
    delta_S_univ = delta_S_sys + delta_S_surr
    
    return {
        'delta_S_sys': delta_S_sys,
        'delta_S_surr': round(delta_S_surr, 2),
        'delta_S_univ': round(delta_S_univ, 2),
        'spontaneity': spontaneity_from_Suniv(delta_S_univ)
    }


def third_law_entropy(W: float = 1) -> float:
    """
    Calculate entropy using Third Law (perfect crystal at 0 K).
    
    At 0 K, W = 1 for perfect crystal, so S = k ln(1) = 0
    
    Args:
        W: Number of microstates (default 1 for perfect crystal)
    
    Returns:
        Entropy (J/K) - should be 0 for perfect crystal at 0 K
    
    Examples:
        >>> third_law_entropy()
        0.0
    """
    if W == 1:
        return 0.0
    # For non-perfect crystals
    K_BOLTZMANN = 1.38e-23
    return K_BOLTZMANN * log(W) if W > 0 else 0.0


def standard_entropy_reaction(S_values: Dict, 
                               reactants: list, 
                               products: list,
                               coeffs: Dict = None) -> float:
    """
    Calculate standard entropy change for a reaction.
    
    Args:
        S_values: Dict of standard entropies {substance: Sdeg}
        reactants: List of reactant substances
        products: List of product substances
        coeffs: Dict of stoichiometric coefficients
    
    Returns:
        Standard entropy change (J/K)
    
    Examples:
        >>> standard_entropy_reaction({'H2O(l)': 69.9, 'H2O(g)': 188.7},
        ...                           ['H2O(l)'], ['H2O(g)'])
        118.8
    """
    if coeffs is None:
        coeffs = {}
    
    sum_products = sum(coeffs.get(p, 1) * S_values.get(p, 0) for p in products)
    sum_reactants = sum(coeffs.get(r, 1) * S_values.get(r, 0) for r in reactants)
    
    return sum_products - sum_reactants


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="calculate_Suniv_from_process",
            description="Calculate DeltaS_universe from process data.",
            input_schema=[
            InputSchemaField(name="delta_S_sys", type="number", required=True),
            InputSchemaField(name="delta_H_sys", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_surroundings",
            description="Calculate entropy change of surroundings.",
            input_schema=[
            InputSchemaField(name="delta_H", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_universe",
            description="Calculate entropy change of the universe.",
            input_schema=[
            InputSchemaField(name="delta_S_sys", type="number", required=True),
            InputSchemaField(name="delta_S_surr", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spontaneity_from_Suniv",
            description="Determine spontaneity from DeltaS_universe.",
            input_schema=[
            InputSchemaField(name="delta_S_univ", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="standard_entropy_reaction",
            description="Calculate standard entropy change for a reaction.",
            input_schema=[
            InputSchemaField(name="S_values", type="number", required=True),
            InputSchemaField(name="reactants", type="number", required=True),
            InputSchemaField(name="products", type="number", required=True),
            InputSchemaField(name="coeffs", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="third_law_entropy",
            description="Calculate entropy using Third Law (perfect crystal at 0 K).",
            input_schema=[
            InputSchemaField(name="W", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
