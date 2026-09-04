"""
Periodic Trends Tools - L3 Implementation
Chapter 18.1: Periodicity

## Solver Instructions (for AI Agent)

When you encounter periodic trends problems (atomic radius, ionization energy, electronegativity), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given two elements -> predict which has larger/smaller property?
- Given element -> get atomic radius, ionization energy, or electronegativity?
- Given position in periodic table -> predict trends?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Atomic radius trend | `predict_atomic_radius_trend(element1, element2)` | Returns comparison |
| Ionization energy trend | `predict_ionization_energy_trend(element1, element2)` | Returns comparison |
| Electronegativity compare | `compare_electronegativity(element1, element2)` | Returns values and difference |
| Atomic radius value | `get_atomic_radius(element)` | Returns radius in pm |
| Ionization energy value | `get_ionization_energy(element)` | Returns IE in kJ/mol |
| Electronegativity value | `get_electronegativity(element)` | Returns Pauling EN |

### Step 3: Handle special cases
- Atomic radius: increases down group, decreases across period
- Ionization energy: decreases down group, increases across period (with exceptions)
- Electronegativity: decreases down group, increases across period
- Exceptions: Be > B (IE), N > O (IE), Ga < Al (radius due to d-block)

### Examples
```python
# Example 1: Atomic radius comparison
predict_atomic_radius_trend('Na', 'K')
# -> 'K has larger radius'

# Example 2: Ionization energy comparison
predict_ionization_energy_trend('Li', 'F')
# -> 'F has higher ionization energy'

# Example 3: Electronegativity difference
compare_electronegativity('Na', 'Cl')
# -> {'EN1': 0.93, 'EN2': 3.16, 'difference': 2.23}

# Example 4: Get specific values
get_ionization_energy('He')  # Highest IE
# -> 2372 kJ/mol
```
"""

from typing import Dict, Tuple, Optional, List


# Approximate atomic radii (pm) - selected elements
ATOMIC_RADII = {
    'H': 53, 'He': 31,
    'Li': 167, 'Be': 112, 'B': 87, 'C': 67, 'N': 56, 'O': 48, 'F': 42, 'Ne': 38,
    'Na': 190, 'Mg': 145, 'Al': 118, 'Si': 111, 'P': 98, 'S': 88, 'Cl': 79, 'Ar': 71,
    'K': 243, 'Ca': 194, 'Ga': 136, 'Ge': 125, 'As': 114, 'Se': 103, 'Br': 94, 'Kr': 88,
    'Rb': 265, 'Sr': 219, 'In': 156, 'Sn': 145, 'Sb': 133, 'Te': 123, 'I': 115, 'Xe': 108
}

# Ionization energies (kJ/mol) - first IE
IONIZATION_ENERGIES = {
    'H': 1312, 'He': 2372,
    'Li': 520, 'Be': 899, 'B': 801, 'C': 1086, 'N': 1402, 'O': 1314, 'F': 1681, 'Ne': 2081,
    'Na': 496, 'Mg': 738, 'Al': 578, 'Si': 787, 'P': 1012, 'S': 1000, 'Cl': 1251, 'Ar': 1521,
    'K': 419, 'Ca': 590, 'Ga': 579, 'Ge': 762, 'As': 947, 'Se': 941, 'Br': 1140, 'Kr': 1351
}

# Electronegativity (Pauling scale)
ELECTRONEGATIVITIES = {
    'H': 2.20, 'He': 0,
    'Li': 0.98, 'Be': 1.57, 'B': 2.04, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'F': 3.98, 'Ne': 0,
    'Na': 0.93, 'Mg': 1.31, 'Al': 1.61, 'Si': 1.90, 'P': 2.19, 'S': 2.58, 'Cl': 3.16, 'Ar': 0,
    'K': 0.82, 'Ca': 1.00, 'Ga': 1.81, 'Ge': 2.01, 'As': 2.18, 'Se': 2.55, 'Br': 2.96, 'Kr': 3.00
}


def predict_atomic_radius_trend(element1: str, element2: str) -> str:
    """
    Predict which element has larger atomic radius.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Comparison result
    
    Examples:
        >>> predict_atomic_radius_trend('Na', 'K')
        'K has larger radius'
    """
    r1 = ATOMIC_RADII.get(element1, 0)
    r2 = ATOMIC_RADII.get(element2, 0)
    
    if r1 > r2:
        return f'{element1} has larger radius'
    elif r2 > r1:
        return f'{element2} has larger radius'
    else:
        return 'Radii are similar or unknown'


def predict_ionization_energy_trend(element1: str, element2: str) -> str:
    """
    Predict which element has higher ionization energy.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Comparison result
    """
    ie1 = IONIZATION_ENERGIES.get(element1, 0)
    ie2 = IONIZATION_ENERGIES.get(element2, 0)
    
    if ie1 > ie2:
        return f'{element1} has higher ionization energy'
    elif ie2 > ie1:
        return f'{element2} has higher ionization energy'
    else:
        return 'Ionization energies are similar or unknown'


def compare_electronegativity(element1: str, element2: str) -> Dict:
    """
    Compare electronegativities of two elements.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Dict with EN values and comparison
    """
    en1 = ELECTRONEGATIVITIES.get(element1, 0)
    en2 = ELECTRONEGATIVITIES.get(element2, 0)
    
    return {
        'element1': element1,
        'EN1': en1,
        'element2': element2,
        'EN2': en2,
        'difference': abs(en1 - en2),
        'more_electronegative': element1 if en1 > en2 else element2 if en2 > en1 else 'equal'
    }


def classify_element(element: str) -> str:
    """
    Classify element as metal, nonmetal, or metalloid.
    
    Args:
        element: Element symbol
    
    Returns:
        Classification string
    """
    metals = {'Li', 'Na', 'K', 'Rb', 'Be', 'Mg', 'Ca', 'Sr', 'Al', 'Ga', 'In', 'Sn', 'Pb'}
    metalloids = {'B', 'Si', 'Ge', 'As', 'Sb', 'Te'}
    nonmetals = {'H', 'C', 'N', 'P', 'O', 'S', 'Se', 'F', 'Cl', 'Br', 'I', 'He', 'Ne', 'Ar', 'Kr', 'Xe'}
    
    if element in metals:
        return 'metal'
    elif element in metalloids:
        return 'metalloid'
    elif element in nonmetals:
        return 'nonmetal'
    else:
        return 'unknown'


def oxide_type(element: str) -> str:
    """
    Predict if element oxide is acidic, basic, or amphoteric.
    
    Args:
        element: Element symbol
    
    Returns:
        Oxide type
    """
    classification = classify_element(element)
    
    if classification == 'metal':
        return 'basic oxide'
    elif classification == 'nonmetal':
        return 'acidic oxide'
    elif classification == 'metalloid':
        return 'amphoteric oxide'
    else:
        return 'unknown'


def bond_type_prediction(element1: str, element2: str) -> str:
    """
    Predict bond type between two elements based on electronegativity.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Predicted bond type
    """
    en1 = ELECTRONEGATIVITIES.get(element1, 0)
    en2 = ELECTRONEGATIVITIES.get(element2, 0)
    
    if en1 == 0 or en2 == 0:
        return 'unknown'
    
    diff = abs(en1 - en2)
    
    if diff < 0.4:
        return 'nonpolar covalent'
    elif diff < 1.7:
        return 'polar covalent'
    else:
        return 'ionic'


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="bond_type_prediction",
            description="Predict bond type between two elements based on electronegativity.",
            input_schema=[
            InputSchemaField(name="element1", type="string", required=True),
            InputSchemaField(name="element2", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="classify_element",
            description="Classify element as metal, nonmetal, or metalloid.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="compare_electronegativity",
            description="Compare electronegativities of two elements.",
            input_schema=[
            InputSchemaField(name="element1", type="string", required=True),
            InputSchemaField(name="element2", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="oxide_type",
            description="Predict if element oxide is acidic, basic, or amphoteric.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_atomic_radius_trend",
            description="Predict which element has larger atomic radius.",
            input_schema=[
            InputSchemaField(name="element1", type="string", required=True),
            InputSchemaField(name="element2", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_ionization_energy_trend",
            description="Predict which element has higher ionization energy.",
            input_schema=[
            InputSchemaField(name="element1", type="string", required=True),
            InputSchemaField(name="element2", type="string", required=True)
            ],
            handler="{name}",
        )
    ]
