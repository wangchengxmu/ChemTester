"""
Non-Ideal Gas Behavior Tools - L3 Implementation
Chapter 8.07: Non-Ideal Gas Behavior and van der Waals Equation

## Solver Instructions (for AI Agent)

When you encounter non-ideal gas problems (van der Waals, compressibility, critical points), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given P, V, n, T -> calculate compressibility factor Z?
- Given gas and conditions -> calculate pressure or volume using van der Waals?
- Given van der Waals constants -> calculate critical properties?
- Given conditions -> predict if gas behaves ideally?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Compressibility factor | `compressibility_factor(P, V, n, T, R)` | Z = PV/(nRT), Z=1 for ideal |
| van der Waals pressure | `van_der_waals_pressure(n, V, T, a, b, R)` | P = nRT/(V-nb) - n2a/V2 |
| van der Waals volume | `van_der_waals_volume(n, P, T, a, b, R)` | Numerical solution |
| Critical properties | `critical_properties_from_vdw(a, b)` | Tc = 8a/(27Rb), Pc = a/(27b2) |
| Reduced properties | `reduced_properties(P, T, V, Pc, Tc, Vc)` | Pr = P/Pc, Tr = T/Tc |

### Step 3: Handle special cases
- VDW_CONSTANTS dict contains a (L2·atm/mol2) and b (L/mol) for common gases
- Z > 1: repulsive forces dominate; Z < 1: attractive forces dominate
- At critical point: (∂P/∂V)T = 0 and (∂2P/∂V2)T = 0

### Examples
```python
# Example 1: Compressibility factor
compressibility_factor(1, 22.4, 1, 273)  # 1 atm, 22.4 L, 1 mol, 273 K
# -> ~1.0 (ideal gas at STP)

# Example 2: van der Waals pressure for CO2
van_der_waals_pressure(1, 22.4, 273, 3.59, 0.0427)  # CO2 constants
# -> ~0.98 atm (slightly less than ideal)

# Example 3: Critical properties from VDW constants
critical_properties_from_vdw(3.59, 0.0427)  # CO2
# -> Tc ~ 304 K, Pc ~ 73 atm

# Example 4: Reduced properties
reduced_properties(50, 300, 0.1, 72.79, 304.2)  # CO2
# -> Pr ~ 0.69, Tr ~ 0.99
```
"""

from typing import Optional
from math import isclose

# Gas constants
R_atm = 0.08206  # L·atm/(mol·K)
R_kPa = 8.314    # kPa·L/(mol·K)

# van der Waals constants for common gases (a in L2·atm/mol2, b in L/mol)
VDW_CONSTANTS = {
    'H2': (0.244, 0.0266),
    'He': (0.0342, 0.0237),
    'N2': (1.39, 0.0391),
    'O2': (1.36, 0.0318),
    'CO2': (3.59, 0.0427),
    'H2O': (5.46, 0.0305),
    'NH3': (4.17, 0.0371),
    'CH4': (2.25, 0.0428),
    'Cl2': (6.49, 0.0562),
    'SO2': (6.71, 0.0564),
}


def compressibility_factor(P: float, V: float, n: float, T: float,
                           R: float = R_atm) -> float:
    """
    Calculate compressibility factor Z = PV/(nRT).
    
    Args:
        P: Pressure (unit must match R)
        V: Volume in liters
        n: Moles of gas
        T: Temperature in Kelvin
        R: Gas constant
    
    Returns:
        Compressibility factor Z
    
    Examples:
        >>> compressibility_factor(1, 22.4, 1, 273)  # Ideal gas
        1.0...
    """
    return P * V / (n * R * T)


def van_der_waals_pressure(n: float, V: float, T: float,
                           a: float, b: float, R: float = R_atm) -> float:
    """
    Calculate pressure using van der Waals equation.
    
    (P + n2a/V2)(V - nb) = nRT
    
    Args:
        n: Moles of gas
        V: Volume in liters
        T: Temperature in Kelvin
        a: van der Waals constant a (L2·atm/mol2)
        b: van der Waals constant b (L/mol)
        R: Gas constant (default for atm)
    
    Returns:
        Pressure in same units as R
    
    Examples:
        >>> van_der_waals_pressure(1, 22.4, 273, 1.39, 0.0391)  # N2
        1.0...
    """
    # P = nRT/(V-nb) - n2a/V2
    pressure_correction = (n ** 2 * a) / (V ** 2)
    volume_correction = V - n * b
    
    ideal_pressure = n * R * T / volume_correction
    return ideal_pressure - pressure_correction


def van_der_waals_volume(n: float, P: float, T: float,
                         a: float, b: float, R: float = R_atm,
                         tolerance: float = 0.001) -> float:
    """
    Calculate volume using van der Waals equation (numerical solution).
    
    Args:
        n: Moles of gas
        P: Pressure
        T: Temperature in Kelvin
        a: van der Waals constant a
        b: van der Waals constant b
        R: Gas constant
        tolerance: Convergence tolerance
    
    Returns:
        Volume in liters
    
    Examples:
        >>> van_der_waals_volume(1, 1, 273, 1.39, 0.0391)  # N2
        22.4...
    """
    # Start with ideal gas estimate
    V = n * R * T / P
    
    # Iterative solution (Newton's method simplified)
    for _ in range(100):
        # Calculate pressure with current V
        P_calc = van_der_waals_pressure(n, V, T, a, b, R)
        
        # Check convergence
        if abs(P_calc - P) / P < tolerance:
            return V
        
        # Adjust V based on pressure difference
        # If P_calc > P, increase V; if P_calc < P, decrease V
        dP_dV = -n * R * T / (V - n * b) ** 2 + 2 * n ** 2 * a / V ** 3
        V = V - (P_calc - P) / dP_dV
        
        # Ensure V > nb
        if V <= n * b:
            V = n * b * 1.01
    
    return V


def ideal_vs_real(n: float, V: float, T: float,
                  a: float, b: float, R: float = R_atm) -> dict:
    """
    Compare ideal gas pressure to real gas (van der Waals) pressure.
    
    Args:
        n: Moles of gas
        V: Volume in liters
        T: Temperature in Kelvin
        a: van der Waals constant a
        b: van der Waals constant b
        R: Gas constant
    
    Returns:
        Dictionary with ideal, real pressures and Z factor
    
    Examples:
        >>> ideal_vs_real(1, 22.4, 273, 1.39, 0.0391)
        {'ideal_pressure': 1.0..., 'real_pressure': 1.0..., 'Z': 1.0...}
    """
    P_ideal = n * R * T / V
    P_real = van_der_waals_pressure(n, V, T, a, b, R)
    Z = compressibility_factor(P_real, V, n, T, R)
    
    return {
        'ideal_pressure': P_ideal,
        'real_pressure': P_real,
        'difference': P_real - P_ideal,
        'Z': Z,
        'deviation_percent': (Z - 1) * 100
    }


def get_vdw_constants(gas: str) -> tuple:
    """
    Get van der Waals constants for a gas.
    
    Args:
        gas: Gas formula (e.g., 'N2', 'CO2', 'H2O')
    
    Returns:
        Tuple of (a, b) constants
    
    Raises:
        ValueError: If gas not in database
    
    Examples:
        >>> get_vdw_constants('N2')
        (1.39, 0.0391)
        >>> get_vdw_constants('CO2')
        (3.59, 0.0427)
    """
    if gas not in VDW_CONSTANTS:
        raise ValueError(f"van der Waals constants not available for {gas}")
    return VDW_CONSTANTS[gas]


def deviation_from_ideal(P: float, V: float, n: float, T: float,
                         R: float = R_atm) -> dict:
    """
    Analyze deviation from ideal behavior.
    
    Args:
        P, V, n, T: Gas properties
        R: Gas constant
    
    Returns:
        Dictionary with Z and interpretation
    
    Examples:
        >>> deviation_from_ideal(1, 22.4, 1, 273)
        {'Z': 1.0..., 'behavior': 'ideal', 'dominant_factor': 'none'}
    """
    Z = compressibility_factor(P, V, n, T, R)
    
    if abs(Z - 1) < 0.05:
        behavior = 'ideal'
        factor = 'none'
    elif Z < 1:
        behavior = 'more compressible'
        factor = 'attractive forces dominate'
    else:
        behavior = 'less compressible'
        factor = 'molecular volume dominates'
    
    return {
        'Z': Z,
        'behavior': behavior,
        'dominant_factor': factor,
        'percent_deviation': (Z - 1) * 100
    }


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="compressibility_factor",
            description="Calculate compressibility factor Z = PV/(nRT).",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="deviation_from_ideal",
            description="Analyze deviation from ideal behavior.",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="get_vdw_constants",
            description="Get van der Waals constants for a gas.",
            input_schema=[
            InputSchemaField(name="gas", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ideal_vs_real",
            description="Compare ideal gas pressure to real gas (van der Waals) pressure.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="a", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="van_der_waals_pressure",
            description="Calculate pressure using van der Waals equation.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="a", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="van_der_waals_volume",
            description="Calculate volume using van der Waals equation (numerical solution).",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="a", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False),
            InputSchemaField(name="tolerance", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
