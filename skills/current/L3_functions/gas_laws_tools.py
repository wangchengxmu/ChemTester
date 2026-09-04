"""
Gas Laws Tools - L3 Implementation
Chapter 8.02: The Gas Laws (Boyle, Charles, Gay-Lussac, Avogadro)

## Solver Instructions (for AI Agent)

When you encounter a gas law problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Initial and final conditions: Look for "initial", "final", "before", "after", "then", "compressed", "expanded", "heated", "cooled"
- Pressure (P): Units like "atm", "kPa", "mmHg", "torr"
- Volume (V): Units like "L", "mL", "m3"
- Temperature (T): MUST be in Kelvin - convert from degC (K = degC + 273.15)
- Moles (n): "mol", or mass/molar mass
- Identify which variables are held constant (this determines which law to use)

### Step 2: Choose the correct function
| Scenario (What's constant) | Function Call |
|---------------------------|---------------|
| T and n constant (P,V change) | `boyles_law(P1, V1, P2, V2)` - pass None for unknown |
| P and n constant (V,T change) | `charles_law(V1, T1, V2, T2)` |
| V and n constant (P,T change) | `gay_lussacs_law(P1, T1, P2, T2)` |
| P and T constant (V,n change) | `avogadros_law(V1, n1, V2, n2)` |
| Only n constant (P,V,T all change) | `combined_gas_law(P1, V1, T1, P2, V2, T2)` |
| Convert degC to K | `celsius_to_kelvin(celsius)` |
| Convert K to degC | `kelvin_to_celsius(kelvin)` |

### Step 3: Handle special cases
- **Temperature conversion**: ALWAYS convert temperature to Kelvin before using any gas law. K = degC + 273.15
- **Which law to use**: 
  - If only P and V change -> Boyle's Law
  - If only V and T change -> Charles's Law
  - If only P and T change -> Gay-Lussac's Law
  - If only V and n change -> Avogadro's Law
  - If P, V, and T all change -> Combined Gas Law
- **Pressure units**: Must be consistent within a problem (all in atm, or all in kPa, etc.)
- **Volume units**: Must be consistent within a problem (all in L, or all in mL, etc.)

### Examples

**Example 1: Boyle's Law**
Question: "A gas occupies 5.0 L at 1.5 atm. What volume will it occupy at 3.0 atm if temperature is constant?"
- Given: V1 = 5.0 L, P1 = 1.5 atm, P2 = 3.0 atm, T constant
- Solution: `boyles_law(P1=1.5, V1=5.0, P2=3.0, V2=None)` -> V2 = 2.5 L

**Example 2: Charles's Law**
Question: "A balloon has a volume of 2.0 L at 25degC. What volume at 50degC if pressure is constant?"
- Given: V1 = 2.0 L, T1 = 25degC = 298 K, T2 = 50degC = 323 K, P constant
- Solution: `charles_law(V1=2.0, T1=298, T2=323, V2=None)` -> V2 ~ 2.17 L

**Example 3: Combined Gas Law**
Question: "A gas at 1.0 atm and 27degC occupies 10.0 L. What is the pressure at 127degC and 5.0 L?"
- Given: P1 = 1.0 atm, V1 = 10.0 L, T1 = 27degC = 300 K, T2 = 127degC = 400 K, V2 = 5.0 L
- Solution: `combined_gas_law(P1=1.0, V1=10.0, T1=300, P2=None, V2=5.0, T2=400)` -> P2 ~ 2.67 atm

**Example 4: Avogadro's Law**
Question: "2.0 moles of gas occupy 50.0 L. What volume will 5.0 moles occupy at same T and P?"
- Given: n1 = 2.0 mol, V1 = 50.0 L, n2 = 5.0 mol
- Solution: `avogadros_law(V1=50.0, n1=2.0, n2=5.0, V2=None)` -> V2 = 125 L
"""

from typing import Optional
from math import isclose


def boyles_law(P1: Optional[float] = None, V1: Optional[float] = None,
               P2: Optional[float] = None, V2: Optional[float] = None) -> float:
    """
    Apply Boyle's Law: P1V1 = P2V2 (constant T, n).
    
    Args:
        P1, V1: Initial pressure and volume
        P2, V2: Final pressure and volume
        Exactly one argument should be None (the one to solve for)
    
    Returns:
        The missing value
    
    Examples:
        >>> boyles_law(P1=1, V1=2, P2=2)
        1.0
        >>> boyles_law(P1=1, V1=2, V2=4)
        0.5
    """
    args = [P1, V1, P2, V2]
    if sum(a is None for a in args) != 1:
        raise ValueError("Exactly one argument must be None")
    
    if P1 is None:
        return P2 * V2 / V1
    elif V1 is None:
        return P2 * V2 / P1
    elif P2 is None:
        return P1 * V1 / V2
    else:  # V2 is None
        return P1 * V1 / P2


def charles_law(V1: Optional[float] = None, T1: Optional[float] = None,
                V2: Optional[float] = None, T2: Optional[float] = None) -> float:
    """
    Apply Charles's Law: V1/T1 = V2/T2 (constant P, n).
    
    Args:
        V1, T1: Initial volume and temperature (K)
        V2, T2: Final volume and temperature (K)
        Exactly one argument should be None
    
    Returns:
        The missing value
    
    Examples:
        >>> charles_law(V1=1, T1=273, T2=546)
        2.0
        >>> charles_law(V1=1, T1=273, V2=0.5)
        136.5
    """
    args = [V1, T1, V2, T2]
    if sum(a is None for a in args) != 1:
        raise ValueError("Exactly one argument must be None")
    
    if V1 is None:
        return V2 * T1 / T2
    elif T1 is None:
        return T2 * V1 / V2
    elif V2 is None:
        return V1 * T2 / T1
    else:  # T2 is None
        return T1 * V2 / V1


def gay_lussacs_law(P1: Optional[float] = None, T1: Optional[float] = None,
                    P2: Optional[float] = None, T2: Optional[float] = None) -> float:
    """
    Apply Gay-Lussac's Law: P1/T1 = P2/T2 (constant V, n).
    
    Args:
        P1, T1: Initial pressure and temperature (K)
        P2, T2: Final pressure and temperature (K)
        Exactly one argument should be None
    
    Returns:
        The missing value
    
    Examples:
        >>> gay_lussacs_law(P1=1, T1=273, T2=546)
        2.0
        >>> gay_lussacs_law(P1=1, T1=273, P2=0.5)
        136.5
    """
    args = [P1, T1, P2, T2]
    if sum(a is None for a in args) != 1:
        raise ValueError("Exactly one argument must be None")
    
    if P1 is None:
        return P2 * T1 / T2
    elif T1 is None:
        return T2 * P1 / P2
    elif P2 is None:
        return P1 * T2 / T1
    else:  # T2 is None
        return T1 * P2 / P1


def avogadros_law(V1: Optional[float] = None, n1: Optional[float] = None,
                  V2: Optional[float] = None, n2: Optional[float] = None) -> float:
    """
    Apply Avogadro's Law: V1/n1 = V2/n2 (constant P, T).
    
    Args:
        V1, n1: Initial volume and moles
        V2, n2: Final volume and moles
        Exactly one argument should be None
    
    Returns:
        The missing value
    
    Examples:
        >>> avogadros_law(V1=1, n1=1, n2=2)
        2.0
        >>> avogadros_law(V1=1, n1=1, V2=0.5)
        0.5
    """
    args = [V1, n1, V2, n2]
    if sum(a is None for a in args) != 1:
        raise ValueError("Exactly one argument must be None")
    
    if V1 is None:
        return V2 * n1 / n2
    elif n1 is None:
        return n2 * V1 / V2
    elif V2 is None:
        return V1 * n2 / n1
    else:  # n2 is None
        return n1 * V2 / V1


def combined_gas_law(P1: Optional[float] = None, V1: Optional[float] = None, 
                     T1: Optional[float] = None,
                     P2: Optional[float] = None, V2: Optional[float] = None,
                     T2: Optional[float] = None,
                     n: Optional[float] = None,
                     R: float = 0.08206) -> float:
    """
    Apply Combined Gas Law: P1V1/T1 = P2V2/T2 (constant n).
    
    If n (moles) is provided and P2, V2, T2 are the final conditions,
    uses ideal gas law: T = PV/(nR) for more accurate results when
    initial conditions may be inconsistent.
    
    Args:
        P1, V1, T1: Initial pressure, volume, and temperature (K)
        P2, V2, T2: Final pressure, volume, and temperature (K)
        n: Optional moles of gas (if provided, uses ideal gas law for final state)
        R: Gas constant (default 0.08206 L·atm/(mol·K))
        Exactly one of P1,V1,T1,P2,V2,T2 should be None
    
    Returns:
        The missing value
    
    Examples:
        >>> combined_gas_law(P1=1, V1=1, T1=273, P2=2, V2=1)
        546.0
        >>> combined_gas_law(P1=1, V1=1, T1=273, P2=1, T2=546)
        2.0
        >>> # With n provided, uses ideal gas law for final state
        >>> combined_gas_law(P2=3.3618, V2=1.255, n=1.0, T1=298.15, P1=1.0, V1=22.4)
        51.4...
    """
    args = [P1, V1, T1, P2, V2, T2]
    none_count = sum(a is None for a in args)
    
    if none_count != 1:
        raise ValueError("Exactly one argument must be None")
    
    # If n is provided and we're solving for T2, use ideal gas law
    # This handles cases where initial conditions may be inconsistent
    if n is not None and T2 is None and P2 is not None and V2 is not None:
        return P2 * V2 / (n * R)
    
    # If n is provided and we're solving for P2, use ideal gas law
    if n is not None and P2 is None and V2 is not None and T2 is not None:
        return n * R * T2 / V2
    
    # If n is provided and we're solving for V2, use ideal gas law
    if n is not None and V2 is None and P2 is not None and T2 is not None:
        return n * R * T2 / P2
    
    # Standard combined gas law calculations
    if P1 is None:
        return P2 * V2 * T1 / (V1 * T2)
    elif V1 is None:
        return P2 * V2 * T1 / (P1 * T2)
    elif T1 is None:
        return P1 * V1 * T2 / (P2 * V2)
    elif P2 is None:
        return P1 * V1 * T2 / (V2 * T1)
    elif V2 is None:
        return P1 * V1 * T2 / (P2 * T1)
    else:  # T2 is None
        return P2 * V2 * T1 / (P1 * V1)


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15


def partial_pressure_dalton(mole_fraction: float, total_pressure: float) -> float:
    """
    Calculate partial pressure from mole fraction and total pressure.
    
    P_i = X_i * P_total
    
    Args:
        mole_fraction: Mole fraction of the gas (n_i / n_total)
        total_pressure: Total pressure of the gas mixture
    
    Returns:
        Partial pressure of the gas (same units as total_pressure)
    
    Examples:
        >>> partial_pressure_dalton(0.5, 2.0)
        1.0
    """
    return mole_fraction * total_pressure


def mole_fraction(moles_component: float, total_moles: float) -> float:
    """
    Calculate mole fraction from component moles and total moles.
    
    X_i = n_i / n_total
    
    Args:
        moles_component: Moles of the component
        total_moles: Total moles in the mixture
    
    Returns:
        Mole fraction (dimensionless)
    
    Examples:
        >>> mole_fraction(0.5, 1.0)
        0.5
    """
    return moles_component / total_moles


def dalton_law_partial_pressures(moles_dict: dict, total_pressure: float) -> dict:
    """
    Calculate all partial pressures from mole amounts and total pressure.
    
    Args:
        moles_dict: Dictionary of {'species': moles}
        total_pressure: Total pressure
    
    Returns:
        Dictionary of {'species': partial_pressure}
    
    Examples:
        >>> dalton_law_partial_pressures({'CH4': 0.75, 'C2H6': 0.30, 'C3H8': 0.05}, 306)
        {'P_CH4': 208.6, 'P_C2H6': 83.5, 'P_C3H8': 13.9}
    """
    total_moles = sum(moles_dict.values())
    partial_pressures = {}
    for species, moles in moles_dict.items():
        X_i = moles / total_moles
        partial_pressures[f'P_{species}'] = X_i * total_pressure
    return partial_pressures


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "avogadros_law",
        "description": "Apply Avogadro's Law: V\u2081/n\u2081 = V\u2082/n\u2082 (constant P, T).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "V1": {"type": "number", "description": "V1", "default": None},
                "n1": {"type": "number", "description": "N1", "default": None},
                "V2": {"type": "number", "description": "V2", "default": None},
                "n2": {"type": "number", "description": "N2", "default": None},
            },
            "required": []
        }
    },
    {
        "name": "boyles_law",
        "description": "Apply Boyle's Law: P\u2081V\u2081 = P\u2082V\u2082 (constant T, n).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "P1": {"type": "number", "description": "P1", "default": None},
                "V1": {"type": "number", "description": "V1", "default": None},
                "P2": {"type": "number", "description": "P2", "default": None},
                "V2": {"type": "number", "description": "V2", "default": None},
            },
            "required": []
        }
    },
    {
        "name": "celsius_to_kelvin",
        "description": "Convert Celsius to Kelvin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "celsius": {"type": "number", "description": "Celsius"},
            },
            "required": ["celsius"]
        }
    },
    {
        "name": "charles_law",
        "description": "Apply Charles's Law: V\u2081/T\u2081 = V\u2082/T\u2082 (constant P, n).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "V1": {"type": "number", "description": "V1", "default": None},
                "T1": {"type": "number", "description": "T1", "default": None},
                "V2": {"type": "number", "description": "V2", "default": None},
                "T2": {"type": "number", "description": "T2", "default": None},
            },
            "required": []
        }
    },
    {
        "name": "combined_gas_law",
        "description": "Apply Combined Gas Law: P₁V₁/T₁ = P₂V₂/T₂ (constant n). If n (moles) is provided, uses ideal gas law for final state calculations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "P1": {"type": "number", "description": "P1", "default": None},
                "V1": {"type": "number", "description": "V1", "default": None},
                "T1": {"type": "number", "description": "T1", "default": None},
                "P2": {"type": "number", "description": "P2", "default": None},
                "V2": {"type": "number", "description": "V2", "default": None},
                "T2": {"type": "number", "description": "T2", "default": None},
                "n": {"type": "number", "description": "Moles of gas (optional, enables ideal gas law)", "default": None},
                "R": {"type": "number", "description": "Gas constant", "default": 0.08206}
            },
            "required": []
        }
    },
    {
        "name": "gay_lussacs_law",
        "description": "Apply Gay-Lussac's Law: P\u2081/T\u2081 = P\u2082/T\u2082 (constant V, n).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "P1": {"type": "number", "description": "P1", "default": None},
                "T1": {"type": "number", "description": "T1", "default": None},
                "P2": {"type": "number", "description": "P2", "default": None},
                "T2": {"type": "number", "description": "T2", "default": None},
            },
            "required": []
        }
    },
    {
        "name": "kelvin_to_celsius",
        "description": "Convert Kelvin to Celsius.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kelvin": {"type": "number", "description": "Kelvin"},
            },
            "required": ["kelvin"]
        }
    },
    {
        "name": "partial_pressure_dalton",
        "description": "Calculate partial pressure from mole fraction and total pressure using Dalton's Law.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mole_fraction": {"type": "number", "description": "Mole fraction of the gas"},
                "total_pressure": {"type": "number", "description": "Total pressure of the mixture"},
            },
            "required": ["mole_fraction", "total_pressure"]
        }
    },
    {
        "name": "mole_fraction",
        "description": "Calculate mole fraction from component moles and total moles.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles_component": {"type": "number", "description": "Moles of the component"},
                "total_moles": {"type": "number", "description": "Total moles in mixture"},
            },
            "required": ["moles_component", "total_moles"]
        }
    },
    {
        "name": "dalton_law_partial_pressures",
        "description": "Calculate all partial pressures from mole amounts and total pressure.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles_dict": {"type": "object", "description": "Dictionary of species:moles pairs"},
                "total_pressure": {"type": "number", "description": "Total pressure"},
            },
            "required": ["moles_dict", "total_pressure"]
        }
    }
]
