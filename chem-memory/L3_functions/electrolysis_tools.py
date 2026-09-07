"""
Electrolysis Tools - L3 Implementation
Chapter 17.7: Electrolysis

## Solver Instructions (for AI Agent)

When you encounter an electrolysis problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Current (I): In amperes (A)
- Time (t): In seconds, minutes, or hours
- Mass of product: In grams
- Moles of electrons: From Faraday's law
- Molar mass: From chemical formula
- Number of electrons transferred: From half-reaction

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate moles from electrolysis | `moles_from_electrolysis(current, time, n_electrons)` |
| Calculate mass from electrolysis | `mass_from_electrolysis(current, time, molar_mass, n_electrons)` |
| Calculate time needed for mass | `time_for_mass(mass, current, molar_mass, n_electrons)` |
| Calculate current needed for mass | `current_for_mass(mass, time, molar_mass, n_electrons)` |
| Calculate charge from current and time | `charge_from_current_time(current, time)` |
| Calculate moles of electrons from charge | `electrons_transferred(charge)` |
| Calculate gas volume at STP | `gas_volume_at_stp(moles)` |
| Minimum voltage for electrolysis | `minimum_voltage_for_electrolysis(E_cell)` |
| Compare galvanic vs electrolytic | `compare_galvanic_vs_electrolytic(E_cell)` |

### Step 3: Handle special cases
- **Faraday's law**: moles = (I x t) / (n x F), where F = 96485 C/mol e-
- **Time units**: Convert to seconds (1 min = 60 s, 1 hr = 3600 s)
- **Electrons from half-reaction**: Extract n from balanced half-reaction (e.g., Cu2+ + 2e- -> Cu, n = 2)
- **Gas at STP**: 1 mol gas = 22.4 L at STP
- **Electrolytic cells**: E_cell < 0, requires external voltage

### Examples

**Example 1: Calculate mass from electrolysis**
Question: "What mass of Cu is deposited when 2.0 A flows for 1.0 hour? (Cu2+ + 2e- -> Cu)"
- Given: I = 2.0 A, t = 3600 s, M(Cu) = 63.5 g/mol, n = 2
- Solution: `mass_from_electrolysis(current=2.0, time=3600, molar_mass=63.5, n_electrons=2)` -> 2.37 g

**Example 2: Calculate time needed**
Question: "How long to deposit 10.0 g Ag from Ag+ using 5.0 A? (Ag+ + e- -> Ag)"
- Given: mass = 10.0 g, I = 5.0 A, M(Ag) = 107.9 g/mol, n = 1
- Solution: `time_for_mass(mass=10.0, current=5.0, molar_mass=107.9, n_electrons=1)` -> 1788 s ~ 30 min

**Example 3: Gas volume from electrolysis**
Question: "What volume of H2 at STP is produced by passing 1.0 A for 30 min? (2H2O + 2e- -> H2 + 2OH-)"
- Given: I = 1.0 A, t = 1800 s, n = 2
- Solution:
  - `moles_H2 = moles_from_electrolysis(current=1.0, time=1800, n_electrons=2)` -> 0.00934 mol
  - `gas_volume_at_stp(moles=0.00934)` -> 0.209 L

**Example 4: Calculate current needed**
Question: "What current is needed to produce 5.0 g Al in 2.0 hours? (Al3+ + 3e- -> Al)"
- Given: mass = 5.0 g, t = 7200 s, M(Al) = 27.0 g/mol, n = 3
- Solution: `current_for_mass(mass=5.0, time=7200, molar_mass=27.0, n_electrons=3)` -> 7.45 A
"""

from typing import Dict, Tuple, Optional


# Constants
FARADAY = 96485  # C/mol e-


def mass_from_electrolysis(current: float, time: float, 
                           molar_mass: float, n_electrons: int) -> float:
    """
    Calculate mass of product from electrolysis using Faraday's law.
    
    m = (M x I x t) / (n x F)
    
    Args:
        current: Current (amperes)
        time: Time (seconds)
        molar_mass: Molar mass of product (g/mol)
        n_electrons: Electrons per ion transferred
    
    Returns:
        Mass of product (g)
    
    Examples:
        >>> mass_from_electrolysis(2.0, 3600, 63.55, 2)
        2.37
    """
    charge = current * time  # Coulombs
    moles_electrons = charge / FARADAY
    moles_product = moles_electrons / n_electrons
    return moles_product * molar_mass


def moles_from_electrolysis(current: float, time: float, 
                            n_electrons: int) -> float:
    """
    Calculate moles of product from electrolysis.
    
    Args:
        current: Current (amperes)
        time: Time (seconds)
        n_electrons: Electrons per ion transferred
    
    Returns:
        Moles of product
    """
    charge = current * time
    moles_electrons = charge / FARADAY
    return moles_electrons / n_electrons


def time_for_mass(mass: float, current: float, molar_mass: float,
                  n_electrons: int) -> float:
    """
    Calculate time needed to produce given mass by electrolysis.
    
    t = (m x n x F) / (M x I)
    
    Args:
        mass: Desired mass (g)
        current: Current (amperes)
        molar_mass: Molar mass (g/mol)
        n_electrons: Electrons per ion transferred
    
    Returns:
        Time (seconds)
    """
    moles_needed = mass / molar_mass
    moles_electrons = moles_needed * n_electrons
    charge_needed = moles_electrons * FARADAY
    return charge_needed / current


def current_for_mass(mass: float, time: float, molar_mass: float,
                     n_electrons: int) -> float:
    """
    Calculate current needed to produce given mass in given time.
    
    I = (m x n x F) / (M x t)
    
    Args:
        mass: Desired mass (g)
        time: Time (seconds)
        molar_mass: Molar mass (g/mol)
        n_electrons: Electrons per ion transferred
    
    Returns:
        Current (amperes)
    """
    moles_needed = mass / molar_mass
    moles_electrons = moles_needed * n_electrons
    charge_needed = moles_electrons * FARADAY
    return charge_needed / time


def charge_from_current_time(current: float, time: float) -> float:
    """
    Calculate total charge passed.
    
    Q = I x t
    
    Args:
        current: Current (amperes)
        time: Time (seconds)
    
    Returns:
        Charge (coulombs)
    """
    return current * time


def electrons_transferred(charge: float) -> float:
    """
    Calculate moles of electrons from charge.
    
    n(e-) = Q / F
    
    Args:
        charge: Charge (coulombs)
    
    Returns:
        Moles of electrons
    """
    return charge / FARADAY


def gas_volume_at_stp(moles: float) -> float:
    """
    Calculate gas volume at STP (22.4 L/mol).
    
    Args:
        moles: Moles of gas
    
    Returns:
        Volume at STP (L)
    """
    return moles * 22.4


def minimum_voltage_for_electrolysis(E_cell: float) -> float:
    """
    Calculate minimum voltage needed for electrolysis.
    
    For nonspontaneous cell (E_cell < 0), minimum voltage = |E_cell|
    
    Args:
        E_cell: Cell potential (V) - will be negative for electrolysis
    
    Returns:
        Minimum voltage (positive value)
    """
    return abs(E_cell) if E_cell < 0 else 0.0


def compare_galvanic_vs_electrolytic(E_cell: float) -> str:
    """
    Determine if cell is galvanic or electrolytic.
    
    Args:
        E_cell: Cell potential (V)
    
    Returns:
        Cell type description
    """
    if E_cell > 0:
        return 'galvanic (spontaneous, produces electricity)'
    elif E_cell < 0:
        return 'electrolytic (nonspontaneous, requires external power)'
    else:
        return 'at equilibrium'


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "charge_from_current_time",
        "description": "Calculate total charge passed.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current": {"type": "number", "description": "Current"},
                "time": {"type": "number", "description": "Time"},
            },
            "required": ["current", "time"]
        }
    },
    {
        "name": "compare_galvanic_vs_electrolytic",
        "description": "Determine if cell is galvanic or electrolytic.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_cell": {"type": "number", "description": "E Cell"},
            },
            "required": ["E_cell"]
        }
    },
    {
        "name": "current_for_mass",
        "description": "Calculate current needed to produce given mass in given time.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass": {"type": "number", "description": "Mass"},
                "time": {"type": "number", "description": "Time"},
                "molar_mass": {"type": "number", "description": "Molar Mass"},
                "n_electrons": {"type": "number", "description": "N Electrons"},
            },
            "required": ["mass", "time", "molar_mass", "n_electrons"]
        }
    },
    {
        "name": "electrons_transferred",
        "description": "Calculate moles of electrons from charge.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "charge": {"type": "number", "description": "Charge"},
            },
            "required": ["charge"]
        }
    },
    {
        "name": "gas_volume_at_stp",
        "description": "Calculate gas volume at STP (22.4 L/mol).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {"type": "number", "description": "Moles"},
            },
            "required": ["moles"]
        }
    },
    {
        "name": "mass_from_electrolysis",
        "description": "Calculate mass of product from electrolysis using Faraday's law.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current": {"type": "number", "description": "Current"},
                "time": {"type": "number", "description": "Time"},
                "molar_mass": {"type": "number", "description": "Molar Mass"},
                "n_electrons": {"type": "number", "description": "N Electrons"},
            },
            "required": ["current", "time", "molar_mass", "n_electrons"]
        }
    },
    {
        "name": "minimum_voltage_for_electrolysis",
        "description": "Calculate minimum voltage needed for electrolysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_cell": {"type": "number", "description": "E Cell"},
            },
            "required": ["E_cell"]
        }
    },
    {
        "name": "moles_from_electrolysis",
        "description": "Calculate moles of product from electrolysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current": {"type": "number", "description": "Current"},
                "time": {"type": "number", "description": "Time"},
                "n_electrons": {"type": "number", "description": "N Electrons"},
            },
            "required": ["current", "time", "n_electrons"]
        }
    },
    {
        "name": "time_for_mass",
        "description": "Calculate time needed to produce given mass by electrolysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass": {"type": "number", "description": "Mass"},
                "current": {"type": "number", "description": "Current"},
                "molar_mass": {"type": "number", "description": "Molar Mass"},
                "n_electrons": {"type": "number", "description": "N Electrons"},
            },
            "required": ["mass", "current", "molar_mass", "n_electrons"]
        }
    }
]
