"""
L3 Tool: Surface Chemistry Tools
Langmuir isotherm calculations.

Source: Surface Science (Nix), Ch3
Created: 2026-03-13
"""

## Solver Instructions (for AI Agent)

# When you encounter **Langmuir isotherm / surface chemistry** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Given pressure P and Langmuir constant b, want coverage -> `langmuir_coverage(P, b)`
# - Given coverage θ and constant b, want pressure -> `langmuir_pressure(theta, b)`
# - Given coverage θ and pressure P, want constant -> `langmuir_constant(theta, P)`
# - Given b at T1, want b at T2 (with DeltaH_ads) -> `langmuir_temperature_effect(b1, T1, T2, delta_H_ads)`
# - Given P vs V adsorption data, want V_monolayer and b -> `langmuir_linear_analysis(P_data, V_data)`
# - Want linearized form value -> `langmuir_linear_form(P, V, V_mono, b)`

### Step 2: Choose the correct function
# - Direct calculation: use `langmuir_coverage`, `langmuir_pressure`, or `langmuir_constant`
# - Temperature dependence: use `langmuir_temperature_effect`
# - Experimental data fitting: use `langmuir_linear_analysis`

### Step 3: Handle special cases
# - θ must be in (0, 1); `langmuir_pressure` returns error otherwise
# - Linear analysis expects matching-length P_data and V_data lists
# - Low-pressure (θ < 0.1) -> linear regime; high-pressure (θ > 0.9) -> saturation

### Examples
# 1. Gas at P=2.0 atm, b=0.5 atm-1: `langmuir_coverage(2.0, 0.5)` -> θ=0.5, moderate regime
# 2. Need P for θ=0.8, b=0.5: `langmuir_pressure(0.8, 0.5)` -> P=8.0 atm
# 3. b increases from 0.1 to ? when T drops from 500K to 400K, DeltaH_ads=-50 kJ/mol: `langmuir_temperature_effect(0.1, 500, 400, -50000)`



import math

# Universal gas constant
R = 8.314  # J/(mol·K)


def langmuir_coverage(P: float, b: float) -> dict:
    """
    Calculate surface coverage using Langmuir isotherm.
    
    θ = bP / (1 + bP)
    
    Args:
        P: Gas pressure (atm or consistent units)
        b: Langmuir equilibrium constant (atm-1)
    
    Returns:
        Dictionary with surface coverage
    
    Example:
        >>> langmuir_coverage(2.0, 0.5)
        {'theta': 0.5, 'regime': 'moderate'}
    """
    theta = b * P / (1 + b * P)
    
    # Determine regime
    if theta < 0.1:
        regime = 'linear'
    elif theta > 0.9:
        regime = 'saturation'
    else:
        regime = 'moderate'
    
    return {
        'theta': theta,
        'P': P,
        'b': b,
        'regime': regime,
        'formula': 'θ = bP/(1+bP)'
    }


def langmuir_pressure(theta: float, b: float) -> dict:
    """
    Calculate pressure needed for given surface coverage.
    
    Rearranging: P = θ / (b(1-θ))
    
    Args:
        theta: Surface coverage (0 < θ < 1)
        b: Langmuir equilibrium constant (atm-1)
    
    Returns:
        Dictionary with pressure
    
    Example:
        >>> langmuir_pressure(0.5, 0.5)
        {'pressure': 2.0}
    """
    if theta <= 0 or theta >= 1:
        return {'error': 'θ must be between 0 and 1'}
    
    P = theta / (b * (1 - theta))
    
    return {
        'pressure': P,
        'theta': theta,
        'b': b,
        'formula': 'P = θ/(b(1-θ))'
    }


def langmuir_constant(theta: float, P: float) -> dict:
    """
    Calculate Langmuir constant from coverage data.
    
    Rearranging: b = θ / (P(1-θ))
    
    Args:
        theta: Surface coverage
        P: Gas pressure
    
    Returns:
        Dictionary with equilibrium constant
    
    Example:
        >>> langmuir_constant(0.67, 1.0)
        {'b': 2.03}
    """
    if theta <= 0 or theta >= 1:
        return {'error': 'θ must be between 0 and 1'}
    
    b = theta / (P * (1 - theta))
    
    return {
        'b': round(b, 4),
        'theta': theta,
        'P': P,
        'formula': 'b = θ/(P(1-θ))'
    }


def langmuir_temperature_effect(b1: float, T1: float, T2: float, 
                                 delta_H: float) -> dict:
    """
    Calculate how Langmuir constant changes with temperature.
    
    b2/b1 = exp(DeltaH/R x (1/T1 - 1/T2))
    
    Args:
        b1: Langmuir constant at T1
        T1: Initial temperature (K)
        T2: Final temperature (K)
        delta_H: Enthalpy of adsorption (J/mol, negative for exothermic)
    
    Returns:
        Dictionary with new Langmuir constant
    
    Example:
        >>> langmuir_temperature_effect(1.0, 300, 400, -50000)
        {'b2': 0.007, 'ratio': 0.007}
    """
    exponent = delta_H / R * (1/T1 - 1/T2)
    ratio = math.exp(exponent)
    b2 = b1 * ratio
    
    return {
        'b2': round(b2, 6),
        'b1': b1,
        'ratio': round(ratio, 6),
        'T1': T1,
        'T2': T2,
        'delta_H': delta_H,
        'formula': 'b2/b1 = exp(DeltaH/R x (1/T1 - 1/T2))'
    }


def langmuir_linear_analysis(P_data: list, V_data: list) -> dict:
    """
    Linear regression analysis of Langmuir isotherm data.
    
    Linear form: P/V = 1/(V_mono x b) + P/V_mono
    
    Slope = 1/V_mono
    Intercept = 1/(V_mono x b)
    
    Args:
        P_data: List of pressure values
        V_data: List of adsorbed volumes
    
    Returns:
        Dictionary with V_mono and b
    
    Example:
        >>> langmuir_linear_analysis([1, 2, 3], [5, 7, 8])
        {'V_mono': 10.0, 'b': 0.5, 'R2': 0.99}
    """
    if len(P_data) != len(V_data):
        return {'error': 'P_data and V_data must have same length'}
    
    n = len(P_data)
    if n < 2:
        return {'error': 'Need at least 2 data points'}
    
    # Calculate P/V values
    PV = [P / V for P, V in zip(P_data, V_data)]
    
    # Linear regression: y = a + bx where y = P/V, x = P
    sum_x = sum(P_data)
    sum_y = sum(PV)
    sum_xy = sum(p * pv for p, pv in zip(P_data, PV))
    sum_x2 = sum(p**2 for p in P_data)
    
    # Slope (b) and intercept (a)
    denom = n * sum_x2 - sum_x**2
    if denom == 0:
        return {'error': 'Cannot perform regression'}
    
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    
    # Calculate V_mono and b
    # slope = 1/V_mono, intercept = 1/(V_mono x b)
    V_mono = 1 / slope
    b = 1 / (V_mono * intercept)
    
    # Calculate R2
    y_mean = sum_y / n
    ss_tot = sum((pv - y_mean)**2 for pv in PV)
    y_pred = [intercept + slope * p for p in P_data]
    ss_res = sum((pv - yp)**2 for pv, yp in zip(PV, y_pred))
    R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    
    return {
        'V_mono': round(V_mono, 4),
        'b': round(b, 6),
        'slope': round(slope, 6),
        'intercept': round(intercept, 6),
        'R2': round(R2, 4),
        'n_points': n
    }


def langmuir_linear_form(P: float, V: float, V_mono: float, b: float) -> dict:
    """
    Verify Langmuir linear form.
    
    Args:
        P: Pressure
        V: Volume adsorbed
        V_mono: Monolayer volume
        b: Langmuir constant
    
    Returns:
        Dictionary with linear form verification
    """
    P_over_V = P / V
    expected_P_over_V = 1/(V_mono * b) + P/V_mono
    
    return {
        'P_over_V': round(P_over_V, 4),
        'expected': round(expected_P_over_V, 4),
        'difference': round(abs(P_over_V - expected_P_over_V), 4)
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "SC-01",
        "question": "Coverage calculation",
        "P": 2.0,
        "b": 0.5,
        "expected_theta": 0.5
    },
    {
        "id": "SC-02",
        "question": "Pressure for half coverage",
        "theta": 0.5,
        "b": 0.5,
        "expected_P": 2.0
    },
    {
        "id": "SC-03",
        "question": "Equilibrium constant from data",
        "theta": 0.67,
        "P": 1.0,
        "expected_b": 2.03
    },
    {
        "id": "SC-04",
        "question": "Linear analysis",
        "P_data": [1, 2, 3, 4],
        "V_data": [5, 7, 8, 8.5],
        "check": "R2"
    },
    {
        "id": "SC-05",
        "question": "Temperature effect",
        "b1": 1.0,
        "T1": 300,
        "T2": 400,
        "delta_H": -50000,
        "check": "ratio_decreases"
    },
]


if __name__ == "__main__":
    print("Surface Chemistry Tools")
    print("=" * 40)
    
    # Test coverage
    print("\nLangmuir Coverage:")
    for P in [0.5, 1.0, 2.0, 5.0]:
        result = langmuir_coverage(P, 0.5)
        print(f"  P={P}: θ={result['theta']:.2f} ({result['regime']})")
    
    # Test pressure
    print("\nPressure for coverage:")
    for theta in [0.25, 0.5, 0.75]:
        result = langmuir_pressure(theta, 0.5)
        print(f"  θ={theta}: P={result['pressure']:.2f} atm")
    
    # Test temperature effect
    print("\nTemperature effect (DeltaH=-50 kJ/mol):")
    result = langmuir_temperature_effect(1.0, 300, 400, -50000)
    print(f"  b at 400K = {result['b2']:.4f} (ratio = {result['ratio']:.4f})")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="langmuir_constant",
            description="Calculate Langmuir constant from coverage data.",
            input_schema=[
            InputSchemaField(name="theta", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="langmuir_coverage",
            description="Calculate surface coverage using Langmuir isotherm.",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="langmuir_linear_analysis",
            description="Linear regression analysis of Langmuir isotherm data.",
            input_schema=[
            InputSchemaField(name="P_data", type="number", required=True),
            InputSchemaField(name="V_data", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="langmuir_linear_form",
            description="Verify Langmuir linear form.",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="V_mono", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="langmuir_pressure",
            description="Calculate pressure needed for given surface coverage.",
            input_schema=[
            InputSchemaField(name="theta", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="langmuir_temperature_effect",
            description="Calculate how Langmuir constant changes with temperature.",
            input_schema=[
            InputSchemaField(name="b1", type="number", required=True),
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True),
            InputSchemaField(name="delta_H", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
