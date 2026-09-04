"""
p-Block Elements Tools - L3 Implementation
Source: Averill, Ch21

## Solver Instructions (for AI Agent)

When you encounter p-block element problems (Groups 13-18), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given group number -> list common oxidation states?
- Given halogen -> compare properties or predict displacement reactions?
- Given noble gas -> get physical properties?
- Given element position -> describe inert-pair effect?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Group oxidation states | `group_oxidation_states(group)` | Groups 13-18 |
| Halogen property | `halogen_property(element, property_name)` | 'electronegativity', 'bp', 'radius' |
| Noble gas properties | `noble_gas_property(element)` | Returns bp, density, uses |
| Inert pair effect | `inert_pair_effect(group, period)` | Groups 13-15, periods 4-6 |
| Halogen displacement | `halogen_displacement(halogen1, halogen2)` | Predicts if displacement occurs |

### Step 3: Handle special cases
- Oxidation states: Group 14 has +2 and +4; Group 15 has +3 and +5
- Inert pair effect: Strong in period 5-6 (Tl, Pb, Bi prefer lower oxidation states)
- Halogen displacement: More electronegative halogen displaces less electronegative
- F > Cl > Br > I in electronegativity and oxidizing power

### Examples
```python
# Example 1: Group oxidation states
group_oxidation_states(17)  # Halogens
# -> [-1, 1, 3, 5, 7]

# Example 2: Halogen electronegativity
halogen_property('F', 'electronegativity')
# -> 3.98

# Example 3: Inert pair effect
inert_pair_effect(14, 6)  # Group 14, Period 6 (Pb)
# -> "Strong inert pair effect: lower oxidation state (4) more stable"

# Example 4: Halogen displacement
halogen_displacement('Cl', 'Br')  # Can Cl displace Br?
# -> "Cl can displace Br from its compounds"
```
"""

from typing import Dict, List, Tuple


# Group oxidation states
GROUP_OXIDATION_STATES = {
    13: [3],           # Boron family
    14: [-4, 2, 4],    # Carbon family
    15: [-3, 3, 5],    # Nitrogen family
    16: [-2, 2, 4, 6], # Oxygen family
    17: [-1, 1, 3, 5, 7], # Halogens
    18: [0]            # Noble gases
}


def group_oxidation_states(group: int) -> List[int]:
    """
    Return common oxidation states for p-block group.
    
    Args:
        group: Group number (13-18)
    
    Returns:
        List of oxidation states
    
    Examples:
        >>> group_oxidation_states(17)
        [-1, 1, 3, 5, 7]
    """
    return GROUP_OXIDATION_STATES.get(group, [])


def halogen_property(element: str, property_name: str) -> float:
    """
    Get property of halogen.
    
    Args:
        element: Halogen symbol (F, Cl, Br, I)
        property_name: 'electronegativity', 'bp', 'radius'
    
    Returns:
        Property value
    """
    halogens = {
        'F': {'electronegativity': 3.98, 'bp': 85, 'radius': 71},
        'Cl': {'electronegativity': 3.16, 'bp': 239, 'radius': 99},
        'Br': {'electronegativity': 2.96, 'bp': 332, 'radius': 114},
        'I': {'electronegativity': 2.66, 'bp': 457, 'radius': 133}
    }
    if element in halogens:
        return halogens[element].get(property_name, 0)
    return 0


def noble_gas_property(element: str) -> Dict:
    """
    Get properties of noble gas.
    
    Args:
        element: Noble gas symbol
    
    Returns:
        Dict with properties
    """
    noble_gases = {
        'He': {'bp': 4, 'density': 0.00017, 'uses': 'balloons, cryogenics'},
        'Ne': {'bp': 27, 'density': 0.0009, 'uses': 'neon signs'},
        'Ar': {'bp': 87, 'density': 0.00178, 'uses': 'welding, lighting'},
        'Kr': {'bp': 121, 'density': 0.0037, 'uses': 'lighting'},
        'Xe': {'bp': 165, 'density': 0.0058, 'uses': 'anesthesia, lighting'}
    }
    return noble_gases.get(element, {})


def inert_pair_effect(group: int, period: int) -> str:
    """
    Describe inert pair effect for element.
    
    Args:
        group: Group number (13-15)
        period: Period number (4-6)
    
    Returns:
        Effect description
    """
    if group in [13, 14, 15] and period >= 5:
        return f"Strong inert pair effect: lower oxidation state ({group}-10) more stable"
    elif group in [13, 14, 15] and period == 4:
        return "Moderate inert pair effect"
    else:
        return "Minimal or no inert pair effect"


def halogen_displacement(halogen1: str, halogen2: str) -> str:
    """
    Predict if halogen can displace another from compound.
    
    More reactive (higher up group) displaces less reactive.
    
    Args:
        halogen1: Displacing halogen
        halogen2: Halogen in compound
    
    Returns:
        Displacement prediction
    """
    reactivity_order = ['F', 'Cl', 'Br', 'I']
    
    if halogen1 not in reactivity_order or halogen2 not in reactivity_order:
        return "Unknown halogen"
    
    if reactivity_order.index(halogen1) < reactivity_order.index(halogen2):
        return f"{halogen1} will displace {halogen2}"
    else:
        return f"{halogen1} will NOT displace {halogen2}"


def allotrope_exists(element: str) -> List[str]:
    """
    List allotropes of p-block element.
    
    Args:
        element: Element symbol
    
    Returns:
        List of allotrope names
    """
    allotropes = {
        'C': ['diamond', 'graphite', 'fullerene', 'graphene'],
        'P': ['white phosphorus', 'red phosphorus', 'black phosphorus'],
        'S': ['rhombic sulfur', 'monoclinic sulfur', 'plastic sulfur'],
        'O': ['O2 (dioxygen)', 'O3 (ozone)'],
        'Se': ['gray selenium', 'red selenium'],
        'B': ['amorphous boron', 'crystalline boron']
    }
    return allotropes.get(element, ['No common allotropes'])


def p_block_oxide_type(element: str) -> str:
    """
    Classify oxide of p-block element.
    
    Args:
        element: Element symbol
    
    Returns:
        Oxide type (acidic, basic, amphoteric)
    """
    acidic_oxides = {'C', 'N', 'P', 'S', 'Cl', 'Br', 'I'}
    basic_oxides = {}
    amphoteric_oxides = {'Al', 'Sn', 'Pb', 'Zn'}
    
    if element in acidic_oxides:
        return 'acidic'
    elif element in basic_oxides:
        return 'basic'
    elif element in amphoteric_oxides:
        return 'amphoteric'
    else:
        return 'varies with oxidation state'


def group_14_element(element: str) -> Dict:
    """
    Get properties of Group 14 element.
    
    Args:
        element: Element symbol (C, Si, Ge, Sn, Pb)
    
    Returns:
        Dict with properties
    """
    elements = {
        'C': {'type': 'nonmetal', 'mp': 3550, 'bp': 4827, 'allotropes': 4},
        'Si': {'type': 'metalloid', 'mp': 1414, 'bp': 3265, 'allotropes': 1},
        'Ge': {'type': 'metalloid', 'mp': 938, 'bp': 2833, 'allotropes': 1},
        'Sn': {'type': 'metal', 'mp': 232, 'bp': 2602, 'allotropes': 2},
        'Pb': {'type': 'metal', 'mp': 327, 'bp': 1749, 'allotropes': 1}
    }
    return elements.get(element, {})


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="allotrope_exists",
            description="List allotropes of p-block element.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="group_14_element",
            description="Get properties of Group 14 element.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="group_oxidation_states",
            description="Return common oxidation states for p-block group.",
            input_schema=[
            InputSchemaField(name="group", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="halogen_displacement",
            description="Predict if halogen can displace another from compound.",
            input_schema=[
            InputSchemaField(name="halogen1", type="number", required=True),
            InputSchemaField(name="halogen2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="halogen_property",
            description="Get property of halogen.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="property_name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="inert_pair_effect",
            description="Describe inert pair effect for element.",
            input_schema=[
            InputSchemaField(name="group", type="number", required=True),
            InputSchemaField(name="period", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="noble_gas_property",
            description="Get properties of noble gas.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="p_block_oxide_type",
            description="Classify oxide of p-block element.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        )
    ]
