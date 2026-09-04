"""
Potential, Free Energy, and Equilibrium Tools - L3 Implementation
Chapter 17.4: Potential, Free Energy, and Equilibrium

## Solver Instructions (for AI Agent)

When you encounter electrochemistry problems linking cell potential, free energy, and equilibrium constants, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **DeltaG from Edeg**: Given cell potential and electrons transferred -> find DeltaGdeg
- **Edeg from DeltaG**: Given DeltaGdeg and n -> find cell potential
- **K from Edeg**: Given cell potential and n -> find equilibrium constant
- **Edeg from K**: Given K and n -> find cell potential
- **Nernst equation**: Given Edeg, concentrations, n, T -> find non-standard cell potential
- **Concentration from E**: Given cell potential and known conditions -> find unknown concentration

### Step 2: Choose the correct function
- `free_energy_from_potential(E_cell, n)` -> DeltaGdeg = -nFEdeg (returns kJ/mol)
- `potential_from_free_energy(delta_G, n)` -> Edeg = -DeltaGdeg/(nF)
- `equilibrium_constant_from_potential(E_cell, n, T)` -> K = 10^(nEdeg/0.0592) at 25degC
- `potential_from_equilibrium_constant(K, n, T)` -> Edeg = (0.0592/n)log K
- `nernst_equation(E_cell, n, Q, T)` -> E = Edeg - (RT/nF)ln Q
- `concentration_from_potential(E, E_cell, n, Q_known, T)` -> solve for unknown concentration

### Step 3: Handle special cases
- n must be moles of electrons (from balancing half-reactions)
- Default T=298.15 K; the simplified 0.0592 factor only works at 25degC
- DeltaGdeg from potential returns kJ/mol (not J/mol)
- K from potential can be astronomically large - use scientific notation

### Examples
1. **DeltaG from Edeg**: Daniell cell Edeg=1.10 V, n=2
   -> `free_energy_from_potential(1.10, 2)` -> -212.3 kJ/mol

2. **K from Edeg**: Edeg=1.24 V (fluorine cell), n=2
   -> `equilibrium_constant_from_potential(1.24, 2)` -> ~1.3x1042 (extremely product-favored)

3. **Nernst equation**: Edeg=0.34 V, n=1, [Cu2+]=0.01 M, T=298.15 K, other terms cancel Q=0.01
   -> `nernst_equation(0.34, 1, 0.01)` -> E = 0.34 - 0.0592xlog(0.01) = 0.34 + 0.118 = 0.458 V
"""

from typing import Dict, Tuple, Optional
from math import log, exp


# Constants
FARADAY = 96485  # C/mol e-
R = 8.314  # J/(mol·K)


def free_energy_from_potential(E_cell: float, n: int) -> float:
    """
    Calculate standard free energy change from cell potential.
    
    DeltaGdeg = -nFEdeg_cell
    
    Args:
        E_cell: Standard cell potential (V)
        n: Number of electrons transferred
    
    Returns:
        DeltaGdeg in kJ/mol
    
    Examples:
        >>> free_energy_from_potential(1.24, 2)
        -239.6
    """
    return -n * FARADAY * E_cell / 1000  # Convert J to kJ


def potential_from_free_energy(delta_G: float, n: int) -> float:
    """
    Calculate cell potential from free energy change.
    
    Edeg = -DeltaGdeg/(nF)
    
    Args:
        delta_G: Free energy change (kJ/mol)
        n: Number of electrons transferred
    
    Returns:
        Cell potential (V)
    """
    return -delta_G * 1000 / (n * FARADAY)


def equilibrium_constant_from_potential(E_cell: float, n: int, 
                                         T: float = 298.15) -> float:
    """
    Calculate equilibrium constant from standard cell potential.
    
    K = 10^(nEdeg/0.0592) at 25degC
    
    Args:
        E_cell: Standard cell potential (V)
        n: Number of electrons transferred
        T: Temperature (K)
    
    Returns:
        Equilibrium constant K
    
    Examples:
        >>> equilibrium_constant_from_potential(1.24, 2)
        1.3e+42
    """
    # At 25degC: Edeg = (0.0592/n) log K
    # log K = nEdeg/0.0592
    log_K = n * E_cell / 0.0592
    return 10 ** log_K


def potential_from_equilibrium_constant(K: float, n: int, 
                                         T: float = 298.15) -> float:
    """
    Calculate standard cell potential from equilibrium constant.
    
    Edeg = (0.0592/n) log K at 25degC
    
    Args:
        K: Equilibrium constant
        n: Number of electrons transferred
        T: Temperature (K)
    
    Returns:
        Standard cell potential (V)
    """
    from math import log10
    return (0.0592 / n) * log10(K)


def nernst_equation(E_standard: float, n: int, Q: float, 
                    T: float = 298.15) -> float:
    """
    Calculate cell potential under nonstandard conditions using Nernst equation.
    
    E = Edeg - (0.0592/n) log Q at 25degC
    
    Args:
        E_standard: Standard cell potential (V)
        n: Number of electrons transferred
        Q: Reaction quotient
        T: Temperature (K)
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> nernst_equation(0.46, 2, 0.1)
        0.49
    """
    from math import log10
    return E_standard - (0.0592 / n) * log10(Q)


def concentration_cell_potential(c_anode: float, c_cathode: float, 
                                  n: int, T: float = 298.15) -> float:
    """
    Calculate potential of a concentration cell.
    
    E = (0.0592/n) log(c_cathode/c_anode)
    
    Args:
        c_anode: Concentration at anode (M)
        c_cathode: Concentration at cathode (M)
        n: Number of electrons transferred
        T: Temperature (K)
    
    Returns:
        Concentration cell potential (V)
    """
    from math import log10
    return (0.0592 / n) * log10(c_cathode / c_anode)


def spontaneity_summary(E_cell: float) -> Dict:
    """
    Summarize spontaneity from cell potential.
    
    Args:
        E_cell: Cell potential (V)
    
    Returns:
        Dict with spontaneity info
    """
    if E_cell > 0:
        return {
            'spontaneous': True,
            'direction': 'forward',
            'delta_G_sign': 'negative',
            'K': 'greater than 1'
        }
    elif E_cell < 0:
        return {
            'spontaneous': False,
            'direction': 'reverse',
            'delta_G_sign': 'positive',
            'K': 'less than 1'
        }
    else:
        return {
            'spontaneous': False,
            'direction': 'equilibrium',
            'delta_G_sign': 'zero',
            'K': 'equals 1'
        }


def reaction_quotient_from_potential(E_cell: float, E_standard: float,
                                      n: int) -> float:
    """
    Calculate reaction quotient from measured cell potential.
    
    Q = 10^(n(Edeg-E)/0.0592)
    
    Args:
        E_cell: Measured cell potential (V)
        E_standard: Standard cell potential (V)
        n: Number of electrons transferred
    
    Returns:
        Reaction quotient Q
    """
    from math import log10
    return 10 ** (n * (E_standard - E_cell) / 0.0592)


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="concentration_cell_potential",
            description="Calculate potential of a concentration cell.",
            input_schema=[
            InputSchemaField(name="c_anode", type="number", required=True),
            InputSchemaField(name="c_cathode", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="T", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="equilibrium_constant_from_potential",
            description="Calculate equilibrium constant from standard cell potential.",
            input_schema=[
            InputSchemaField(name="E_cell", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="T", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="free_energy_from_potential",
            description="Calculate standard free energy change from cell potential.",
            input_schema=[
            InputSchemaField(name="E_cell", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="nernst_equation",
            description="Calculate cell potential under nonstandard conditions using Nernst equation.",
            input_schema=[
            InputSchemaField(name="E_standard", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="Q", type="number", required=True),
            InputSchemaField(name="T", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="potential_from_equilibrium_constant",
            description="Calculate standard cell potential from equilibrium constant.",
            input_schema=[
            InputSchemaField(name="K", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="T", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="potential_from_free_energy",
            description="Calculate cell potential from free energy change.",
            input_schema=[
            InputSchemaField(name="delta_G", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reaction_quotient_from_potential",
            description="Calculate reaction quotient from measured cell potential.",
            input_schema=[
            InputSchemaField(name="E_cell", type="number", required=True),
            InputSchemaField(name="E_standard", type="number", required=True),
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spontaneity_summary",
            description="Summarize spontaneity from cell potential.",
            input_schema=[
            InputSchemaField(name="E_cell", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
