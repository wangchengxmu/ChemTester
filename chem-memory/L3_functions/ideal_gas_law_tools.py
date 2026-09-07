"""
Ideal Gas Law Tools - L3 Implementation
Chapter 8.03-8.04: The Ideal Gas Law and Applications

## Solver Instructions (for AI Agent)

When you encounter an ideal gas law problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Pressure (P): look for "atm", "kPa", "mmHg", "torr", "bar" -> convert to atm if needed (1 atm = 101.325 kPa = 760 mmHg = 760 torr)
- Volume (V): look for "L", "mL", "m3" -> convert to L (1 L = 1000 mL, 1 m3 = 1000 L)
- Moles (n): look for "mol", or mass + molar mass, or particles/Avogadro's number
- Temperature (T): look for "degC", "K", "degF" -> MUST convert to Kelvin (K = degC + 273.15)
- Molar mass (M): look for g/mol, or calculate from chemical formula
- Density (d): look for "g/L"

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Find P, V, n, or T given the other three | `ideal_gas_law(P, V, n, T)` - pass None for unknown |
| Calculate molar volume at given T, P | `molar_volume(T, P)` |
| Calculate gas density from P, M, T | `gas_density(P, M, T)` |
| Find molar mass from density, P, T | `molar_mass_from_gas(d, P, T)` |
| Convert volume to moles at STP | `moles_at_stp(V)` |
| Convert moles to volume at STP | `volume_at_stp(n)` |
| Gas stoichiometry from volume | `gas_stoichiometry(gas_volume, gas_coeff, product_coeff, molar_mass)` |

### Step 3: Handle special cases
- **Unit conversions**: Always convert temperature to Kelvin first. Match R constant to pressure units:
  - R = 0.08206 L·atm/(mol·K) for pressure in atm
  - R = 8.314 kPa·L/(mol·K) for pressure in kPa
  - R = 62.36 L·torr/(mol·K) for pressure in torr/mmHg
- **STP vs SATP**: STP = 0degC (273.15 K), 1 atm -> molar volume = 22.4 L/mol; SATP = 25degC (298.15 K), 1 atm -> 24.8 L/mol
- **Molar mass from formula**: Extract chemical formula from question (e.g., "CO2", "NH3") and calculate M
- **Gas stoichiometry**: First convert gas volume to moles, then use mole ratio from balanced equation

### Examples

**Example 1: Find pressure**
Question: "What is the pressure of 2.5 moles of gas in a 10.0 L container at 25degC?"
- Given: n = 2.5 mol, V = 10.0 L, T = 25degC = 298.15 K
- Solution: `ideal_gas_law(P=None, V=10.0, n=2.5, T=298.15)` -> P ~ 6.1 atm

**Example 2: Calculate density**
Question: "Calculate the density of CO2 (M = 44.0 g/mol) at 1.5 atm and 100degC."
- Given: P = 1.5 atm, M = 44.0 g/mol, T = 100degC = 373.15 K
- Solution: `gas_density(P=1.5, M=44.0, T=373.15)` -> d ~ 2.17 g/L

**Example 3: Find molar mass from density**
Question: "A gas has a density of 2.86 g/L at 1.00 atm and 273 K. What is its molar mass?"
- Given: d = 2.86 g/L, P = 1.00 atm, T = 273 K
- Solution: `molar_mass_from_gas(d=2.86, P=1.00, T=273)` -> M ~ 64.1 g/mol

**Example 4: Gas stoichiometry**
Question: "How many grams of water are produced when 5.0 L of H2 reacts with excess O2 at STP? (2H2 + O2 -> 2H2O)"
- Given: V(H2) = 5.0 L at STP, molar mass H2O = 18.0 g/mol, mole ratio 2:2
- Solution: `gas_stoichiometry(gas_volume=5.0, gas_moles_coeff=2, product_moles_coeff=2, molar_mass=18.0)` -> 4.0 g H2O
"""

from typing import Optional
from math import isclose

# Gas constant values
R_atm = 0.08206  # L·atm/(mol·K)
R_kPa = 8.314    # kPa·L/(mol·K)
R_J = 8.314      # J/(mol·K)
R_torr = 62.36   # L·torr/(mol·K)


def ideal_gas_law(P: Optional[float] = None, V: Optional[float] = None,
                  n: Optional[float] = None, T: Optional[float] = None,
                  R: float = R_atm) -> float:
    """
    Apply the ideal gas law: PV = nRT.
    
    Args:
        P: Pressure (unit must match R)
        V: Volume in liters
        n: Moles of gas
        T: Temperature in Kelvin
        R: Gas constant (default 0.08206 L·atm/(mol·K))
        Exactly one argument should be None
    
    Returns:
        The missing value
    
    Examples:
        >>> ideal_gas_law(P=1, V=22.4, n=1, T=273)
        1.0
        >>> ideal_gas_law(P=1, n=1, T=273)
        22.414...
    """
    args = [P, V, n, T]
    if sum(a is None for a in args) != 1:
        raise ValueError("Exactly one of P, V, n, T must be None")
    
    if P is None:
        return n * R * T / V
    elif V is None:
        return n * R * T / P
    elif n is None:
        return P * V / (R * T)
    else:  # T is None
        return P * V / (n * R)


def molar_volume(T: float = 273.15, P: float = 1.0, 
                 R: float = R_atm) -> float:
    """
    Calculate molar volume of ideal gas at given conditions.
    
    Args:
        T: Temperature in Kelvin
        P: Pressure (unit must match R)
        R: Gas constant
    
    Returns:
        Molar volume in L/mol
    
    Examples:
        >>> molar_volume(273.15, 1.0)  # STP
        22.414...
        >>> molar_volume(298.15, 1.0)  # SATP
        24.46...
    """
    return ideal_gas_law(P=P, n=1, T=T, R=R)


def gas_density(P: float, M: float, T: float, R: float = R_atm) -> float:
    """
    Calculate density of a gas.
    
    Args:
        P: Pressure (unit must match R)
        M: Molar mass in g/mol
        T: Temperature in Kelvin
        R: Gas constant
    
    Returns:
        Density in g/L
    
    Examples:
        >>> gas_density(1, 28.0, 273)  # N2 at STP
        1.25...
    """
    # d = PM/RT
    return P * M / (R * T)


def molar_mass_from_gas(d: float, P: float, T: float, 
                         R: float = R_atm) -> float:
    """
    Calculate molar mass from gas density.
    
    Args:
        d: Density in g/L
        P: Pressure (unit must match R)
        T: Temperature in Kelvin
        R: Gas constant
    
    Returns:
        Molar mass in g/mol
    
    Examples:
        >>> molar_mass_from_gas(1.25, 1, 273)
        28.0...
    """
    # M = dRT/P
    return d * R * T / P


def moles_at_stp(V: float) -> float:
    """
    Calculate moles of gas at STP (22.4 L/mol).
    
    Args:
        V: Volume in liters
    
    Returns:
        Moles of gas
    
    Examples:
        >>> moles_at_stp(22.4)
        1.0
        >>> moles_at_stp(44.8)
        2.0
    """
    return V / 22.4


def volume_at_stp(n: float = None, mass: float = None, M: float = None) -> float:
    """
    Calculate volume of gas at STP (22.4 L/mol).
    
    Args:
        n: Moles of gas
        mass: Mass in grams (requires M)
        M: Molar mass in g/mol (used with mass)
    
    Returns:
        Volume in liters
    
    Examples:
        >>> volume_at_stp(n=1)
        22.4
        >>> volume_at_stp(n=2)
        44.8
        >>> volume_at_stp(mass=1.68, M=83.8)  # Kr
        0.449
    """
    if n is not None:
        return n * 22.4
    elif mass is not None and M is not None:
        return (mass / M) * 22.4
    else:
        raise ValueError("Provide either n or (mass and M)")


def mass_at_stp(V: float, M: float) -> float:
    """
    Calculate mass of gas at STP from volume.
    
    Args:
        V: Volume in liters
        M: Molar mass in g/mol
    
    Returns:
        Mass in grams
    
    Examples:
        >>> mass_at_stp(22.4, 2.016)  # H2
        2.016
    """
    return (V / 22.4) * M


def gas_stoichiometry(gas_volume: float, gas_moles_coeff: int,
                      product_moles_coeff: int, molar_mass: float = None,
                      conditions: str = 'STP') -> dict:
    """
    Calculate product amounts from gas volume stoichiometry.
    
    Args:
        gas_volume: Volume of gas in liters
        gas_moles_coeff: Stoichiometric coefficient of gas
        product_moles_coeff: Stoichiometric coefficient of product
        molar_mass: Molar mass of product (optional, for mass)
        conditions: 'STP' or 'SATP'
    
    Returns:
        Dictionary with moles and optionally mass of product
    
    Examples:
        >>> gas_stoichiometry(22.4, 1, 1)  # 1 mol gas -> 1 mol product
        {'product_moles': 1.0}
    """
    # Calculate moles of gas
    Vm = 22.4 if conditions == 'STP' else 24.8
    gas_moles = gas_volume / Vm
    
    # Stoichiometric ratio
    product_moles = gas_moles * product_moles_coeff / gas_moles_coeff
    
    result = {'product_moles': product_moles}
    
    if molar_mass:
        result['product_mass'] = product_moles * molar_mass
    
    return result

MCP_TOOLS = [
    {
        "name": "gas_density",
        "description": "Calculate density of a gas.",
        "parameters": [
            {
                "name": "P",
                "type": "number"
            },
            {
                "name": "M",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "gas_stoichiometry",
        "description": "Calculate product amounts from gas volume stoichiometry.",
        "parameters": [
            {
                "name": "gas_volume",
                "type": "number"
            },
            {
                "name": "gas_moles_coeff",
                "type": "number"
            },
            {
                "name": "product_moles_coeff",
                "type": "number"
            },
            {
                "name": "molar_mass",
                "type": "number"
            },
            {
                "name": "conditions",
                "type": "number"
            }
        ]
    },
    {
        "name": "ideal_gas_law",
        "description": "Apply the ideal gas law: PV = nRT.",
        "parameters": [
            {
                "name": "P",
                "type": "number"
            },
            {
                "name": "V",
                "type": "number"
            },
            {
                "name": "n",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "molar_mass_from_gas",
        "description": "Calculate molar mass from gas density.",
        "parameters": [
            {
                "name": "d",
                "type": "number"
            },
            {
                "name": "P",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "molar_volume",
        "description": "Calculate molar volume of ideal gas at given conditions.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "P",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "moles_at_stp",
        "description": "Calculate moles of gas at STP (22.4 L/mol).",
        "parameters": [
            {
                "name": "V",
                "type": "number"
            }
        ]
    },
    {
        "name": "volume_at_stp",
        "description": "Calculate volume of gas at STP (22.4 L/mol).",
        "parameters": [
            {
                "name": "n",
                "type": "number"
            }
        ]
    }
]
