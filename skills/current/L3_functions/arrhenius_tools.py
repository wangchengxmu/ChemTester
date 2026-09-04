"""
Arrhenius Tools - L3 Implementation
Chapter 12.05: Collision Theory and Arrhenius Equation

## Solver Instructions (for AI Agent)

When you encounter an Arrhenius equation problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Rate constant k: At specific temperature
- Temperature T: In Kelvin (convert from degC if needed)
- Activation energy Ea: In J/mol or kJ/mol
- Frequency factor A: Pre-exponential factor
- Two temperatures with rate constants: For Ea calculation

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate k from A, Ea, T | `arrhenius_k(A, Ea, T)` |
| Calculate A from k, Ea, T | `frequency_factor(k, Ea, T)` |
| Calculate Ea from two k values | `activation_energy(k1, T1, k2, T2)` |
| Calculate Ea from Arrhenius plot slope | `activation_energy_from_slope(slope)` |
| Calculate k at different T | `rate_at_temperature(k1, T1, Ea, T2)` |
| Compare rates at two temperatures | `compare_rates(Ea, T1, T2)` |
| Calculate temperature for target k | `temperature_for_rate(k_target, A, Ea)` |
| Calculate fraction with energy ≥ Ea | `fraction_with_energy(Ea, T)` |
| Calculate catalyzed rate constant | `catalyzed_rate_constant(k_uncat, Ea_uncat, Ea_cat, T)` |

### Step 3: Handle special cases
- **Unit consistency**: Ea must be in J/mol for R = 8.314; convert kJ to J (×1000)
- **Temperature**: Always use Kelvin (K = °C + 273.15)
- **Arrhenius plot**: ln(k) vs 1/T gives straight line with slope = -Ea/R
- **Catalyst effect**: Lowers Ea, increases k exponentially
- **Temperature effect**: k increases exponentially with T

### Step 4: Parameter names — use EXACTLY these names
⚠️ The function parameters are named `Ea` (NOT `Ea_J`, `Ea_kJ`, or `activation_energy`). You MUST pass arguments using the exact parameter names shown in the function signature. Common mistake: passing `Ea_J=85000` instead of `Ea=85000` will silently fail or be ignored.

| Parameter | Name in code | Unit |
|-----------|-------------|------|
| Activation energy | `Ea` | J/mol (NOT kJ/mol!) |
| Temperatures | `T1`, `T2` | Kelvin |
| Rate constants | `k1`, `k2` | same as given |
| Frequency factor | `A` | same as k units |

### Examples

**Example 1: Calculate k**
Question: "Calculate k if A = 1.0 x 1010 s-1, Ea = 75 kJ/mol, T = 300 K."
- Given: A = 1e10, Ea = 75000 J/mol, T = 300 K
- Solution: `arrhenius_k(A=1e10, Ea=75000, T=300)` -> k ~ 0.025 s-1

**Example 2: Calculate Ea from two temperatures**
Question: "k = 0.001 at 300 K and k = 0.01 at 350 K. Calculate Ea."
- Solution: `activation_energy(k1=0.001, T1=300, k2=0.01, T2=350)` -> Ea ~ 53000 J/mol

**Example 3: Compare rates**
Question: "By what factor does rate increase when T goes from 300 K to 310 K (Ea = 75 kJ/mol)?"
- Solution: `compare_rates(Ea=75000, T1=300, T2=310)` -> rate increases by ~3x

**Example 4: Catalyst effect**
Question: "If Ea decreases from 100 kJ/mol to 75 kJ/mol, what is the new k (k_uncat = 1e-6, T = 300 K)?"
- Solution: `catalyzed_rate_constant(k_uncat=1e-6, Ea_uncat=100000, Ea_cat=75000, T=300)` -> k_cat ~ 1.9e-3
"""

from typing import Tuple, Optional
from math import log, exp

# Gas constant
R = 8.314  # J/(mol·K)


def arrhenius_k(A: float, Ea: float, T: float) -> float:
    """
    Calculate rate constant using Arrhenius equation.
    
    Args:
        A: Frequency factor (same units as k)
        Ea: Activation energy (J/mol)
        T: Temperature (K)
    
    Returns:
        Rate constant k
    
    Examples:
        >>> arrhenius_k(1e10, 75000, 300)
        2.5e-3
    """
    return A * exp(-Ea / (R * T))


def activation_energy(k1: float, T1: float, k2: float, T2: float) -> float:
    """
    Calculate activation energy from rate constants at two temperatures.
    
    Args:
        k1: Rate constant at T1
        T1: Temperature 1 (K)
        k2: Rate constant at T2
        T2: Temperature 2 (K)
    
    Returns:
        Activation energy (J/mol)
    
    Examples:
        >>> activation_energy(1e-3, 300, 1e-2, 320)
        52000
    """
    return -R * log(k2 / k1) / (1/T2 - 1/T1)


def frequency_factor(k: float, Ea: float, T: float) -> float:
    """
    Calculate frequency factor from rate constant.
    
    Args:
        k: Rate constant
        Ea: Activation energy (J/mol)
        T: Temperature (K)
    
    Returns:
        Frequency factor A
    
    Examples:
        >>> frequency_factor(1e-3, 75000, 300)
        4.1e10
    """
    return k / exp(-Ea / (R * T))


def rate_at_temperature(k1: float, T1: float, Ea: float, T2: float) -> float:
    """
    Calculate rate constant at a different temperature.
    
    Args:
        k1: Rate constant at T1
        T1: Known temperature (K)
        Ea: Activation energy (J/mol)
        T2: Target temperature (K)
    
    Returns:
        Rate constant at T2
    
    Examples:
        >>> rate_at_temperature(1e-3, 300, 75000, 320)
        0.025
    """
    return k1 * exp(Ea / R * (1/T1 - 1/T2))


def temperature_for_rate(k_target: float, A: float, Ea: float) -> float:
    """
    Calculate temperature needed for a specific rate constant.
    
    Args:
        k_target: Target rate constant
        A: Frequency factor
        Ea: Activation energy (J/mol)
    
    Returns:
        Temperature (K)
    
    Examples:
        >>> temperature_for_rate(1e-3, 1e10, 75000)
        300
    """
    return -Ea / (R * log(k_target / A))


def compare_rates(Ea: float, T1: float, T2: float) -> float:
    """
    Compare rates at two temperatures.
    
    Args:
        Ea: Activation energy (J/mol)
        T1: Lower temperature (K)
        T2: Higher temperature (K)
    
    Returns:
        Ratio k2/k1
    
    Examples:
        >>> compare_rates(75000, 300, 310)
        3.0
    """
    return exp(Ea / R * (1/T1 - 1/T2))


def arrhenius_plot_slope(Ea: float) -> float:
    """
    Get slope for Arrhenius plot (ln k vs 1/T).
    
    Args:
        Ea: Activation energy (J/mol)
    
    Returns:
        Slope (equals -Ea/R)
    
    Examples:
        >>> arrhenius_plot_slope(75000)
        -9022
    """
    return -Ea / R


def activation_energy_from_slope(slope: float) -> float:
    """
    Calculate activation energy from Arrhenius plot slope.
    
    Args:
        slope: Slope from ln k vs 1/T plot
    
    Returns:
        Activation energy (J/mol)
    
    Examples:
        >>> activation_energy_from_slope(-9022)
        75000
    """
    return -slope * R


def fraction_with_energy(Ea: float, T: float) -> float:
    """
    Calculate fraction of molecules with energy >= Ea.
    
    Args:
        Ea: Activation energy (J/mol)
        T: Temperature (K)
    
    Returns:
        Fraction of molecules
    
    Examples:
        >>> fraction_with_energy(75000, 300)
        7.2e-14
    """
    return exp(-Ea / (R * T))


def catalyzed_rate_constant(k_uncat: float, Ea_uncat: float, 
                             Ea_cat: float, T: float) -> float:
    """
    Calculate catalyzed rate constant.
    
    Args:
        k_uncat: Uncatalyzed rate constant
        Ea_uncat: Uncatalyzed activation energy (J/mol)
        Ea_cat: Catalyzed activation energy (J/mol)
        T: Temperature (K)
    
    Returns:
        Catalyzed rate constant
    
    Examples:
        >>> catalyzed_rate_constant(1e-6, 100000, 75000, 300)
        1.9e-3
    """
    ratio = exp((Ea_uncat - Ea_cat) / (R * T))
    return k_uncat * ratio


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "activation_energy",
        "description": "Calculate activation energy from rate constants at two temperatures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k1": {
                    "type": "number",
                    "description": "K1"
                },
                "T1": {
                    "type": "number",
                    "description": "T1"
                },
                "k2": {
                    "type": "number",
                    "description": "K2"
                },
                "T2": {
                    "type": "number",
                    "description": "T2"
                }
            },
            "required": [
                "k1",
                "T1",
                "k2",
                "T2"
            ]
        }
    },
    {
        "name": "activation_energy_from_slope",
        "description": "Calculate activation energy from Arrhenius plot slope.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "slope": {
                    "type": "number",
                    "description": "Slope"
                }
            },
            "required": [
                "slope"
            ]
        }
    },
    {
        "name": "arrhenius_k",
        "description": "Calculate rate constant using Arrhenius equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "A": {
                    "type": "number",
                    "description": "A"
                },
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                },
                "T": {
                    "type": "number",
                    "description": "T"
                }
            },
            "required": [
                "A",
                "Ea",
                "T"
            ]
        }
    },
    {
        "name": "arrhenius_plot_slope",
        "description": "Get slope for Arrhenius plot (ln k vs 1/T).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                }
            },
            "required": [
                "Ea"
            ]
        }
    },
    {
        "name": "catalyzed_rate_constant",
        "description": "Calculate catalyzed rate constant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_uncat": {
                    "type": "number",
                    "description": "K Uncat"
                },
                "Ea_uncat": {
                    "type": "number",
                    "description": "Ea Uncat"
                },
                "Ea_cat": {
                    "type": "number",
                    "description": "Ea Cat"
                },
                "T": {
                    "type": "number",
                    "description": "T"
                }
            },
            "required": [
                "k_uncat",
                "Ea_uncat",
                "Ea_cat",
                "T"
            ]
        }
    },
    {
        "name": "compare_rates",
        "description": "Compare rates at two temperatures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                },
                "T1": {
                    "type": "number",
                    "description": "T1"
                },
                "T2": {
                    "type": "number",
                    "description": "T2"
                }
            },
            "required": [
                "Ea",
                "T1",
                "T2"
            ]
        }
    },
    {
        "name": "fraction_with_energy",
        "description": "Calculate fraction of molecules with energy >= Ea.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                },
                "T": {
                    "type": "number",
                    "description": "T"
                }
            },
            "required": [
                "Ea",
                "T"
            ]
        }
    },
    {
        "name": "frequency_factor",
        "description": "Calculate frequency factor from rate constant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k": {
                    "type": "number",
                    "description": "K"
                },
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                },
                "T": {
                    "type": "number",
                    "description": "T"
                }
            },
            "required": [
                "k",
                "Ea",
                "T"
            ]
        }
    },
    {
        "name": "rate_at_temperature",
        "description": "Calculate rate constant at a different temperature.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k1": {
                    "type": "number",
                    "description": "K1"
                },
                "T1": {
                    "type": "number",
                    "description": "T1"
                },
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                },
                "T2": {
                    "type": "number",
                    "description": "T2"
                }
            },
            "required": [
                "k1",
                "T1",
                "Ea",
                "T2"
            ]
        }
    },
    {
        "name": "temperature_for_rate",
        "description": "Calculate temperature needed for a specific rate constant.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_target": {
                    "type": "number",
                    "description": "K Target"
                },
                "A": {
                    "type": "number",
                    "description": "A"
                },
                "Ea": {
                    "type": "number",
                    "description": "Ea"
                }
            },
            "required": [
                "k_target",
                "A",
                "Ea"
            ]
        }
    }
]