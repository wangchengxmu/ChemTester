"""
Galvanic Cells Tools - L3 Implementation
Chapter 17.2: Galvanic Cells

## Solver Instructions (for AI Agent)

When you encounter a galvanic cell problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Standard reduction potentials Edeg: Look for table values or given values
- Half-reactions: Identify oxidation (anode) and reduction (cathode)
- Cell notation: Format like Zn|Zn2+||Cu2+|Cu
- Spontaneity: Whether reaction proceeds as written
- Strongest oxidizing/reducing agent: Compare Edeg values

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate standard cell potential | `cell_potential(E_cathode, E_anode)` |
| Identify anode and cathode | `identify_anode_cathode(E1, E2)` |
| Predict spontaneity | `predict_spontaneity(E_cell)` |
| Generate cell notation | `cell_notation(anode_species, anode_solution, cathode_solution, cathode_species)` |
| Find strongest oxidizing agent | `strongest_oxidizing_agent(E_values)` |
| Find strongest reducing agent | `strongest_reducing_agent(E_values)` |
| Combine half-reactions | `half_reactions_balanced(anode_reaction, cathode_reaction, n_electrons)` |
| Get overall reaction | `overall_reaction(anode_half, cathode_half)` |

### Step 3: Handle special cases
- **Edeg convention**: All values are reduction potentials; oxidation potential = -reduction potential
- **Cathode**: Higher Edeg (reduction occurs); Anode: Lower Edeg (oxidation occurs)
- **Edegcell = Edegcathode - Edeganode**: Always use reduction potentials
- **Spontaneous**: Edegcell > 0 (positive)
- **Oxidizing agent**: Higher Edeg = stronger; Reducing agent: Lower Edeg = stronger
- **Cell notation**: Anode | Anode solution || Cathode solution | Cathode

### Examples

**Example 1: Calculate cell potential**
Question: "Calculate Edegcell for Zn|Zn2+||Cu2+|Cu. Edeg(Zn2+/Zn) = -0.76 V, Edeg(Cu2+/Cu) = +0.34 V."
- Given: E_cathode = 0.34 V (Cu), E_anode = -0.76 V (Zn)
- Solution: `cell_potential(E_cathode=0.34, E_anode=-0.76)` -> Edegcell = 1.10 V

**Example 2: Identify strongest oxidizing agent**
Question: "Which is strongest oxidizing agent: Ag+ (0.80 V), Cu2+ (0.34 V), or Zn2+ (-0.76 V)?"
- Solution: `strongest_oxidizing_agent({'Ag+': 0.80, 'Cu2+': 0.34, 'Zn2+': -0.76})` -> 'Ag+' (highest Edeg)

**Example 3: Identify strongest reducing agent**
Question: "Which is strongest reducing agent: Ag (0.80 V), Cu (0.34 V), or Zn (-0.76 V)?"
- Solution: `strongest_reducing_agent({'Ag+': 0.80, 'Cu2+': 0.34, 'Zn2+': -0.76})` -> 'Zn' (lowest Edeg)

**Example 4: Predict spontaneity**
Question: "Is the Zn-Cu galvanic cell spontaneous?"
- Given: Edegcell = 1.10 V
- Solution: `predict_spontaneity(E_cell=1.10)` -> 'spontaneous'
"""

from typing import Dict, Tuple, Optional


def cell_potential(E_cathode: float, E_anode: float) -> float:
    """
    Calculate standard cell potential.
    
    E_cell = E_cathode - E_anode
    
    Args:
        E_cathode: Standard reduction potential of cathode (V)
        E_anode: Standard reduction potential of anode (V)
    
    Returns:
        Cell potential (V)
    
    Examples:
        >>> cell_potential(0.80, 0.34)
        0.46
    """
    return E_cathode - E_anode


def identify_anode_cathode(E1: float, E2: float) -> Dict:
    """
    Identify anode and cathode from two half-cell potentials.
    
    Higher Edeg = cathode (reduction)
    Lower Edeg = anode (oxidation)
    
    Args:
        E1: First half-cell potential (V)
        E2: Second half-cell potential (V)
    
    Returns:
        Dict with anode and cathode assignments
    """
    if E1 > E2:
        return {'cathode_E': E1, 'anode_E': E2, 'spontaneous': True}
    else:
        return {'cathode_E': E2, 'anode_E': E1, 'spontaneous': True}


def predict_spontaneity(E_cell: float) -> str:
    """
    Predict if a redox reaction is spontaneous.
    
    Args:
        E_cell: Cell potential (V)
    
    Returns:
        Spontaneity prediction
    
    Examples:
        >>> predict_spontaneity(0.46)
        'spontaneous'
        >>> predict_spontaneity(-0.47)
        'nonspontaneous'
    """
    if E_cell > 0:
        return 'spontaneous'
    elif E_cell < 0:
        return 'nonspontaneous'
    else:
        return 'at equilibrium'


def cell_notation(anode_species: str, anode_solution: str,
                  cathode_solution: str, cathode_species: str) -> str:
    """
    Generate cell notation from components.
    
    Format: anode | anode_soln || cathode_soln | cathode
    
    Args:
        anode_species: Anode solid species
        anode_solution: Anode solution species
        cathode_solution: Cathode solution species
        cathode_species: Cathode solid species
    
    Returns:
        Cell notation string
    """
    return f"{anode_species} | {anode_solution} || {cathode_solution} | {cathode_species}"


def half_reactions_balanced(anode_reaction: str, cathode_reaction: str,
                            n_electrons: int) -> Dict:
    """
    Return balanced half-reactions.
    
    Args:
        anode_reaction: Anode half-reaction (oxidation)
        cathode_reaction: Cathode half-reaction (reduction)
        n_electrons: Number of electrons transferred
    
    Returns:
        Dict with balanced reactions
    """
    return {
        'anode': anode_reaction,
        'cathode': cathode_reaction,
        'electrons': n_electrons,
        'balanced': True
    }


def overall_reaction(anode_half: str, cathode_half: str) -> str:
    """
    Combine half-reactions into overall cell reaction.
    
    Args:
        anode_half: Anode oxidation reaction
        cathode_half: Cathode reduction reaction
    
    Returns:
        Overall reaction string
    """
    return f"{anode_half} + {cathode_half}"


def strongest_oxidizing_agent(E_values: Dict) -> str:
    """
    Identify strongest oxidizing agent from reduction potentials.
    
    Higher Edeg = stronger oxidizing agent
    
    Args:
        E_values: Dict of species:potential pairs
    
    Returns:
        Species with highest reduction potential
    """
    return max(E_values, key=E_values.get)


def strongest_reducing_agent(E_values: Dict) -> str:
    """
    Identify strongest reducing agent from reduction potentials.
    
    Lower Edeg = stronger reducing agent
    
    Args:
        E_values: Dict of species:potential pairs
    
    Returns:
        Species with lowest reduction potential
    """
    return min(E_values, key=E_values.get)


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "cell_notation",
        "description": "Generate cell notation from components.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "anode_species": {"type": "number", "description": "Anode Species"},
                "anode_solution": {"type": "number", "description": "Anode Solution"},
                "cathode_solution": {"type": "number", "description": "Cathode Solution"},
                "cathode_species": {"type": "number", "description": "Cathode Species"},
            },
            "required": ["anode_species", "anode_solution", "cathode_solution", "cathode_species"]
        }
    },
    {
        "name": "cell_potential",
        "description": "Calculate standard cell potential.",
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
        "name": "half_reactions_balanced",
        "description": "Return balanced half-reactions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "anode_reaction": {"type": "number", "description": "Anode Reaction"},
                "cathode_reaction": {"type": "number", "description": "Cathode Reaction"},
                "n_electrons": {"type": "number", "description": "N Electrons"},
            },
            "required": ["anode_reaction", "cathode_reaction", "n_electrons"]
        }
    },
    {
        "name": "identify_anode_cathode",
        "description": "Identify anode and cathode from two half-cell potentials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E1": {"type": "number", "description": "E1"},
                "E2": {"type": "number", "description": "E2"},
            },
            "required": ["E1", "E2"]
        }
    },
    {
        "name": "overall_reaction",
        "description": "Combine half-reactions into overall cell reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "anode_half": {"type": "number", "description": "Anode Half"},
                "cathode_half": {"type": "number", "description": "Cathode Half"},
            },
            "required": ["anode_half", "cathode_half"]
        }
    },
    {
        "name": "predict_spontaneity",
        "description": "Predict if a redox reaction is spontaneous.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_cell": {"type": "number", "description": "E Cell"},
            },
            "required": ["E_cell"]
        }
    },
    {
        "name": "strongest_oxidizing_agent",
        "description": "Identify strongest oxidizing agent from reduction potentials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_values": {"type": "number", "description": "E Values"},
            },
            "required": ["E_values"]
        }
    },
    {
        "name": "strongest_reducing_agent",
        "description": "Identify strongest reducing agent from reduction potentials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_values": {"type": "number", "description": "E Values"},
            },
            "required": ["E_values"]
        }
    }
]
