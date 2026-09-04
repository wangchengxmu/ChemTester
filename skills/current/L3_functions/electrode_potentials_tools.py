"""
Electrode Potentials Tools - L3 Implementation
Chapter 17.3: Electrode and Cell Potentials

## Solver Instructions (for AI Agent)

When you encounter standard electrode and cell potential problems:

### Step 1: Identify what is given and what is asked
- Given: half-cell species, reduction potentials, or cell notation
- Asked: cell potential, spontaneity, relative oxidizing/reducing strength

### Step 2: Choose the correct function
- `standard_cell_potential(E_cathode, E_anode)`: Edeg = Edeg_cathode - Edeg_anode
- `lookup_potential(species)`: Look up Edeg from database (e.g., 'Cu2+/Cu' -> 0.337V)
- `will_reaction_occur(E_cathode, E_anode)`: E_cathode > E_anode -> spontaneous
- `compare_oxidizing_strength(E1, species1, E2, species2)`: Higher Edeg = stronger oxidizer
- `compare_reducing_strength(E1, species1, E2, species2)`: Lower Edeg = stronger reducer
- `calculate_cell_potential_from_notation(anode_species, cathode_species)`: Full cell from species names
- `list_species_by_oxidizing_strength(species_list)`: Sort strongest oxidizer first

### Step 3: Handle special cases
- Edeg_cell > 0 -> spontaneous (galvanic); Edeg_cell < 0 -> non-spontaneous (electrolytic)
- Standard conditions: 1 M, 1 atm, 25degC
- SHE (H+/H2) = 0.000 V by definition

### Examples
```python
lookup_potential('Cu2+/Cu')  # -> 0.337V
standard_cell_potential(0.337, -0.763)  # Cu-Zn -> 1.100V
will_reaction_occur(0.337, -0.763)  # -> True
list_species_by_oxidizing_strength(['Cu2+/Cu', 'Zn2+/Zn', 'Ag+/Ag'])
```
"""

from typing import Dict, Tuple, Optional, List
from math import log, exp


# Standard reduction potentials at 25degC (V)
STANDARD_POTENTIALS = {
    'F2/F-': 2.866,
    'Au3+/Au': 1.498,
    'Cl2/Cl-': 1.358,
    'O2/H2O': 1.229,
    'Br2/Br-': 1.087,
    'Ag+/Ag': 0.800,
    'Fe3+/Fe2+': 0.771,
    'I2/I-': 0.536,
    'Cu2+/Cu': 0.337,
    'H+/H2': 0.000,  # SHE
    'Pb2+/Pb': -0.126,
    'Sn2+/Sn': -0.138,
    'Ni2+/Ni': -0.257,
    'Co2+/Co': -0.280,
    'Cd2+/Cd': -0.403,
    'Fe2+/Fe': -0.447,
    'Cr3+/Cr': -0.744,
    'Zn2+/Zn': -0.762,
    'Al3+/Al': -1.662,
    'Mg2+/Mg': -2.372,
    'Na+/Na': -2.710,
    'Ca2+/Ca': -2.868,
    'K+/K': -2.931,
    'Li+/Li': -3.040
}


def standard_cell_potential(E_cathode: float, E_anode: float) -> float:
    """
    Calculate standard cell potential from standard reduction potentials.
    
    Edeg_cell = Edeg_cathode - Edeg_anode
    
    Args:
        E_cathode: Standard reduction potential of cathode (V)
        E_anode: Standard reduction potential of anode (V)
    
    Returns:
        Standard cell potential (V)
    """
    return E_cathode - E_anode


def lookup_potential(species: str) -> float:
    """
    Look up standard reduction potential for a species.
    
    Args:
        species: Species name (e.g., 'Cu2+/Cu')
    
    Returns:
        Standard reduction potential (V)
    """
    return STANDARD_POTENTIALS.get(species, 0.0)


def will_reaction_occur(E_cathode: float, E_anode: float) -> bool:
    """
    Determine if redox reaction will occur spontaneously.
    
    Args:
        E_cathode: Reduction potential of proposed oxidizing agent (V)
        E_anode: Reduction potential of proposed reducing agent (V)
    
    Returns:
        True if reaction is spontaneous
    """
    return E_cathode > E_anode


def compare_oxidizing_strength(E1: float, species1: str, 
                                E2: float, species2: str) -> str:
    """
    Compare oxidizing strengths of two species.
    
    Args:
        E1, E2: Reduction potentials (V)
        species1, species2: Species names
    
    Returns:
        Comparison string
    """
    if E1 > E2:
        return f"{species1} is stronger oxidizing agent"
    elif E2 > E1:
        return f"{species2} is stronger oxidizing agent"
    else:
        return "Equal oxidizing strength"


def compare_reducing_strength(E1: float, species1: str,
                               E2: float, species2: str) -> str:
    """
    Compare reducing strengths of two species.
    
    Lower Edeg = stronger reducing agent
    
    Args:
        E1, E2: Reduction potentials (V)
        species1, species2: Species names
    
    Returns:
        Comparison string
    """
    if E1 < E2:
        return f"{species1} is stronger reducing agent"
    elif E2 < E1:
        return f"{species2} is stronger reducing agent"
    else:
        return "Equal reducing strength"


def calculate_cell_potential_from_notation(anode_species: str, 
                                            cathode_species: str) -> float:
    """
    Calculate cell potential from half-cell species.
    
    Args:
        anode_species: Anode half-cell (e.g., 'Zn2+/Zn')
        cathode_species: Cathode half-cell (e.g., 'Cu2+/Cu')
    
    Returns:
        Standard cell potential (V)
    """
    E_cathode = lookup_potential(cathode_species)
    E_anode = lookup_potential(anode_species)
    return standard_cell_potential(E_cathode, E_anode)


def list_species_by_oxidizing_strength(species_list: List[str]) -> List[str]:
    """
    Sort species by oxidizing strength (highest Edeg first).
    
    Args:
        species_list: List of species names
    
    Returns:
        Sorted list (strongest oxidizer first)
    """
    return sorted(species_list, key=lambda s: STANDARD_POTENTIALS.get(s, 0), reverse=True)


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calculate_cell_potential_from_notation",
        "description": "Calculate cell potential from half-cell species.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "anode_species": {"type": "number", "description": "Anode Species"},
                "cathode_species": {"type": "number", "description": "Cathode Species"},
            },
            "required": ["anode_species", "cathode_species"]
        }
    },
    {
        "name": "compare_oxidizing_strength",
        "description": "Compare oxidizing strengths of two species.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E1": {"type": "number", "description": "E1"},
                "species1": {"type": "number", "description": "Species1"},
                "E2": {"type": "number", "description": "E2"},
                "species2": {"type": "number", "description": "Species2"},
            },
            "required": ["E1", "species1", "E2", "species2"]
        }
    },
    {
        "name": "compare_reducing_strength",
        "description": "Compare reducing strengths of two species.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E1": {"type": "number", "description": "E1"},
                "species1": {"type": "number", "description": "Species1"},
                "E2": {"type": "number", "description": "E2"},
                "species2": {"type": "number", "description": "Species2"},
            },
            "required": ["E1", "species1", "E2", "species2"]
        }
    },
    {
        "name": "list_species_by_oxidizing_strength",
        "description": "Sort species by oxidizing strength (highest E\u00b0 first).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "species_list": {"type": "number", "description": "Species List"},
            },
            "required": ["species_list"]
        }
    },
    {
        "name": "lookup_potential",
        "description": "Look up standard reduction potential for a species.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "species": {"type": "number", "description": "Species"},
            },
            "required": ["species"]
        }
    },
    {
        "name": "standard_cell_potential",
        "description": "Calculate standard cell potential from standard reduction potentials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_cathode": {"type": "number", "description": "E Cathode"},
                "E_anode": {"type": "number", "description": "E Anode"},
            },
            "required": ["E_cathode", "E_anode"]
        }
    },
    {
        "name": "will_reaction_occur",
        "description": "Determine if redox reaction will occur spontaneously.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_cathode": {"type": "number", "description": "E Cathode"},
                "E_anode": {"type": "number", "description": "E Anode"},
            },
            "required": ["E_cathode", "E_anode"]
        }
    }
]
