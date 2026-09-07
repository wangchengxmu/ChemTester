"""
Periodic Trends Tools - L3 Implementation
Chapter 18.1: Periodicity

The numeric tables in this bounded tool are approximate legacy teaching values,
not a complete or current authoritative data source. Missing values are refused.

## Solver Instructions (for AI Agent)

When you encounter periodic trends problems (atomic radius, ionization energy, electronegativity), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given two supported elements -> predict which has larger/smaller property?
- Given two supported elements -> compare their electronegativities or bond type?
- Given an element for oxide classification -> use the explicit conventional map only.

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Atomic radius trend | `predict_atomic_radius_trend(element1, element2)` | Returns comparison |
| Ionization energy trend | `predict_ionization_energy_trend(element1, element2)` | Returns comparison |
| Electronegativity compare | `compare_electronegativity(element1, element2)` | Returns values and difference |

### Step 3: Handle special cases
- Atomic radius: increases down group, decreases across period
- Ionization energy: decreases down group, increases across period (with exceptions)
- Electronegativity: decreases down group, increases across period
- Known first-ionization-energy exceptions in the supported table include Be > B and N > O.
- `oxide_type` uses only an explicit conventional highest-period-3 oxide map; it is not a generic periodic-classification rule.

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

```
"""

from typing import Dict, Tuple, Optional, List


# Approximate legacy teaching-table values, not a current authoritative data source.
# Atomic radii (pm) - selected elements
ATOMIC_RADII = {
    'H': 53, 'He': 31,
    'Li': 167, 'Be': 112, 'B': 87, 'C': 67, 'N': 56, 'O': 48, 'F': 42, 'Ne': 38,
    'Na': 190, 'Mg': 145, 'Al': 118, 'Si': 111, 'P': 98, 'S': 88, 'Cl': 79, 'Ar': 71,
    'K': 243, 'Ca': 194, 'Ga': 136, 'Ge': 125, 'As': 114, 'Se': 103, 'Br': 94, 'Kr': 88,
    'Rb': 265, 'Sr': 219, 'In': 156, 'Sn': 145, 'Sb': 133, 'Te': 123, 'I': 115, 'Xe': 108
}

# Approximate legacy teaching-table values, not a complete element table.
# Ionization energies (kJ/mol) - first IE
IONIZATION_ENERGIES = {
    'H': 1312, 'He': 2372,
    'Li': 520, 'Be': 899, 'B': 801, 'C': 1086, 'N': 1402, 'O': 1314, 'F': 1681, 'Ne': 2081,
    'Na': 496, 'Mg': 738, 'Al': 578, 'Si': 787, 'P': 1012, 'S': 1000, 'Cl': 1251, 'Ar': 1521,
    'K': 419, 'Ca': 590, 'Ga': 579, 'Ge': 762, 'As': 947, 'Se': 941, 'Br': 1140, 'Kr': 1351
}

# Approximate legacy Pauling-scale teaching-table values; absent values are missing,
# not zero. Noble-gas zeros are intentionally not used as data.
ELECTRONEGATIVITIES = {
    'H': 2.20,
    'Li': 0.98, 'Be': 1.57, 'B': 2.04, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'F': 3.98,
    'Na': 0.93, 'Mg': 1.31, 'Al': 1.61, 'Si': 1.90, 'P': 2.19, 'S': 2.58, 'Cl': 3.16,
    'K': 0.82, 'Ca': 1.00, 'Ga': 1.81, 'Ge': 2.01, 'As': 2.18, 'Se': 2.55, 'Br': 2.96, 'Kr': 3.00
}


def _required_table_value(table: Dict[str, float], element: str, property_name: str) -> float:
    if not isinstance(element, str) or element not in table:
        raise ValueError(f"Missing {property_name} data for element {element!r}")
    return table[element]


def predict_atomic_radius_trend(element1: str, element2: str) -> str:
    """
    Predict which element has larger atomic radius.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Comparison result. The comparison uses approximate legacy values in
        ``ATOMIC_RADII`` with units of pm; the radius definition and provenance
        are not specified or independently verified, so this is not an
        authoritative exact-radius claim. Equal values are ties at stored
        table precision. Missing values raise ``ValueError``.
    
    Examples:
        >>> predict_atomic_radius_trend('Na', 'K')
        'K has larger radius'
    """
    r1 = _required_table_value(ATOMIC_RADII, element1, "atomic-radius")
    r2 = _required_table_value(ATOMIC_RADII, element2, "atomic-radius")
    
    if r1 > r2:
        return f'{element1} has larger radius'
    elif r2 > r1:
        return f'{element2} has larger radius'
    else:
        return 'Radii are equal'


def predict_ionization_energy_trend(element1: str, element2: str) -> str:
    """
    Predict which element has higher ionization energy.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Comparison result using approximate legacy first-ionization-energy
        values in kJ/mol. The table provenance is unverified; equal values are
        ties at stored table precision, and missing values raise ``ValueError``.
    """
    ie1 = _required_table_value(IONIZATION_ENERGIES, element1, "first-ionization-energy")
    ie2 = _required_table_value(IONIZATION_ENERGIES, element2, "first-ionization-energy")
    
    if ie1 > ie2:
        return f'{element1} has higher ionization energy'
    elif ie2 > ie1:
        return f'{element2} has higher ionization energy'
    else:
        return 'Ionization energies are equal'


def compare_electronegativity(element1: str, element2: str) -> Dict:
    """
    Compare electronegativities of two elements.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Dict with approximate legacy Pauling-scale EN values and comparison.
        The table provenance is unverified; ``difference`` is computed from
        stored precision, equal values are ties at stored table precision, and
        missing values raise ``ValueError``.
    """
    en1 = _required_table_value(ELECTRONEGATIVITIES, element1, "electronegativity")
    en2 = _required_table_value(ELECTRONEGATIVITIES, element2, "electronegativity")
    
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


OXIDE_TYPE_MAP = {
    'Na': {'formula': 'Na2O', 'type': 'basic oxide'},
    'Mg': {'formula': 'MgO', 'type': 'basic oxide'},
    'Al': {'formula': 'Al2O3', 'type': 'amphoteric oxide'},
    'Si': {'formula': 'SiO2', 'type': 'acidic oxide'},
    'P': {'formula': 'P4O10', 'type': 'acidic oxide'},
    'S': {'formula': 'SO3', 'type': 'acidic oxide'},
    'Cl': {'formula': 'Cl2O7', 'type': 'acidic oxide'},
}


def oxide_type(element: str) -> str:
    """
    Predict if element oxide is acidic, basic, or amphoteric.
    
    Args:
        element: Element symbol
    
    Returns:
        Oxide type for the exact conventional highest-period-3 oxide in
        ``OXIDE_TYPE_MAP``: Na2O, MgO, Al2O3, SiO2, P4O10, SO3, or Cl2O7.
        Elements outside that limited map raise ``ValueError``.
    """
    if not isinstance(element, str) or element not in OXIDE_TYPE_MAP:
        raise ValueError(
            f"No supported conventional highest-period-3 oxide mapping for {element!r}"
        )
    return OXIDE_TYPE_MAP[element]['type']


def bond_type_prediction(element1: str, element2: str) -> str:
    """
    Predict bond type between two elements based on electronegativity.
    
    Args:
        element1, element2: Element symbols
    
    Returns:
        Predicted bond type from approximate legacy Pauling-scale
        electronegativities. The table provenance is unverified and missing
        values raise ``ValueError`` rather than being treated as zero.
    """
    en1 = _required_table_value(ELECTRONEGATIVITIES, element1, "electronegativity")
    en2 = _required_table_value(ELECTRONEGATIVITIES, element2, "electronegativity")
    
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
            description="Classify an element's exact conventional highest-period-3 oxide using the limited supported map.",
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
