"""
s-Block Elements Tools - L3 Implementation
Source: Averill, Ch20

## Solver Instructions (for AI Agent)

When you encounter s-block element problems (Group 1 and 2 properties, reactions, trends), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Element property lookup**: Given element symbol and property name -> find value (IE, radius, mp, density)
- **Reaction prediction**: Given element and reactant (water, oxygen, halogen, nitrogen) -> describe reaction
- **Periodic trends**: Compare properties across Group 1 or Group 2
- **Flame test colors**: Given element -> predict flame color
- **Anomalous behavior**: Li vs other Group 1, Be vs other Group 2

### Step 2: Choose the correct function
- `alkali_metal_property(element, property_name)` -> lookup from ALKALI_METALS dict (Li, Na, K, Rb, Cs)
- `alkaline_earth_property(element, property_name)` -> lookup from ALKALINE_EARTH dict (Be, Mg, Ca, Sr, Ba)
- `group_1_reaction(element, reactant)` -> reaction description for 'water', 'oxygen', 'halogen', 'nitrogen'
- `group_2_reaction(element, reactant)` -> same for Group 2
- `flame_test_color(element)` -> characteristic flame color
- `compare_reactivity(element1, element2)` -> which is more reactive

### Step 3: Handle special cases
- Only Li reacts with N2 (forms Li3N); Mg and heavier Group 2 also form nitrides
- Li and Be show diagonal relationships (Li↔Mg, Be↔Al)
- Ionization energy decreases down group; reactivity increases down group
- Group 2 oxides: BeO and BaO2 are exceptions (peroxide for Ba)
- Flame tests: Li=crimson, Na=yellow, K=lilac, Ca=orange-red, Sr=red, Ba=green

### Examples
1. **Property lookup**: First ionization energy of Na
   -> `alkali_metal_property('Na', 'IE')` -> 496 kJ/mol

2. **Reaction with water**: K + H2O
   -> `group_1_reaction('K', 'water')` -> 'K + H2O -> KOH + H2 (vigorous)'

3. **Trend**: Compare IE of Li vs Cs
   -> Li: `alkali_metal_property('Li', 'IE')` -> 520 kJ/mol
   -> Cs: `alkali_metal_property('Cs', 'IE')` -> 376 kJ/mol (much lower, easier to remove electron)
"""

from typing import Dict, List, Tuple


# Alkali metal properties
ALKALI_METALS = {
    'Li': {'group': 1, 'period': 2, 'IE': 520, 'radius': 152, 'mp': 181, 'density': 0.53},
    'Na': {'group': 1, 'period': 3, 'IE': 496, 'radius': 186, 'mp': 98, 'density': 0.97},
    'K': {'group': 1, 'period': 4, 'IE': 419, 'radius': 227, 'mp': 63, 'density': 0.86},
    'Rb': {'group': 1, 'period': 5, 'IE': 403, 'radius': 248, 'mp': 39, 'density': 1.53},
    'Cs': {'group': 1, 'period': 6, 'IE': 376, 'radius': 265, 'mp': 28, 'density': 1.88}
}

# Alkaline earth properties
ALKALINE_EARTH = {
    'Be': {'group': 2, 'period': 2, 'IE': 899, 'radius': 112, 'mp': 1287, 'density': 1.85},
    'Mg': {'group': 2, 'period': 3, 'IE': 738, 'radius': 160, 'mp': 650, 'density': 1.74},
    'Ca': {'group': 2, 'period': 4, 'IE': 590, 'radius': 197, 'mp': 842, 'density': 1.55},
    'Sr': {'group': 2, 'period': 5, 'IE': 549, 'radius': 215, 'mp': 777, 'density': 2.63},
    'Ba': {'group': 2, 'period': 6, 'IE': 503, 'radius': 217, 'mp': 727, 'density': 3.62}
}


def alkali_metal_property(element: str, property_name: str) -> float:
    """
    Get property of alkali metal.
    
    Args:
        element: Element symbol (Li, Na, K, Rb, Cs)
        property_name: 'IE', 'radius', 'mp', 'density'
    
    Returns:
        Property value
    
    Examples:
        >>> alkali_metal_property('Na', 'IE')
        496
    """
    if element in ALKALI_METALS:
        return ALKALI_METALS[element].get(property_name, 0)
    return 0


def alkaline_earth_property(element: str, property_name: str) -> float:
    """
    Get property of alkaline earth metal.
    
    Args:
        element: Element symbol (Be, Mg, Ca, Sr, Ba)
        property_name: 'IE', 'radius', 'mp', 'density'
    
    Returns:
        Property value
    """
    if element in ALKALINE_EARTH:
        return ALKALINE_EARTH[element].get(property_name, 0)
    return 0


def group_1_reaction(element: str, reactant: str) -> str:
    """
    Describe reaction of Group 1 metal.
    
    Args:
        element: Alkali metal symbol
        reactant: 'water', 'oxygen', 'halogen'
    
    Returns:
        Reaction description
    """
    if reactant == 'water':
        return f'{element} + H2O -> {element}OH + H2 (vigorous)'
    elif reactant == 'oxygen':
        return f'{element} + O2 -> {element}2O or {element}2O2 (varies)'
    elif reactant == 'halogen':
        return f'{element} + X2 -> {element}X (ionic halide)'
    else:
        return 'Unknown reaction'


def group_2_reaction(element: str, reactant: str) -> str:
    """
    Describe reaction of Group 2 metal.
    
    Args:
        element: Alkaline earth symbol
        reactant: 'water', 'oxygen', 'halogen'
    
    Returns:
        Reaction description
    """
    if reactant == 'water':
        if element == 'Be':
            return 'Be does not react with water'
        elif element == 'Mg':
            return 'Mg + H2O (steam) -> MgO + H2'
        else:
            return f'{element} + H2O -> {element}(OH)2 + H2'
    elif reactant == 'oxygen':
        return f'{element} + O2 -> {element}O (oxide)'
    elif reactant == 'halogen':
        return f'{element} + X2 -> {element}X2 (ionic halide)'
    else:
        return 'Unknown reaction'


def diagonal_relationship(element1: str, element2: str) -> bool:
    """
    Check for diagonal relationship in periodic table.
    
    Args:
        element1: First element
        element2: Second element
    
    Returns:
        True if diagonal relationship exists
    
    Examples:
        >>> diagonal_relationship('Li', 'Mg')
        True
        >>> diagonal_relationship('Be', 'Al')
        True
    """
    diagonal_pairs = [
        ('Li', 'Mg'), ('Mg', 'Li'),
        ('Be', 'Al'), ('Al', 'Be'),
        ('B', 'Si'), ('Si', 'B')
    ]
    return (element1, element2) in diagonal_pairs


def flame_test_color(element: str) -> str:
    """
    Return flame test color for s-block element.
    
    Args:
        element: Element symbol
    
    Returns:
        Flame color
    """
    colors = {
        'Li': 'crimson red',
        'Na': 'yellow',
        'K': 'lilac/violet',
        'Rb': 'red',
        'Cs': 'blue',
        'Ca': 'brick red',
        'Sr': 'crimson red',
        'Ba': 'apple green'
    }
    return colors.get(element, 'no characteristic color')


def s_block_trend(property_type: str) -> str:
    """
    Describe trend in s-block properties.
    
    Args:
        property_type: 'reactivity', 'ionization_energy', 'radius'
    
    Returns:
        Trend description
    """
    trends = {
        'reactivity': 'Increases down group (lower IE, easier electron loss)',
        'ionization_energy': 'Decreases down group (valence electron farther from nucleus)',
        'radius': 'Increases down group (more electron shells)',
        'melting_point': 'Generally decreases down group (weaker metallic bonding)'
    }
    return trends.get(property_type, 'Unknown property')


def compare_alkali_alkaline_earth() -> Dict:
    """
    Compare Group 1 vs Group 2 properties.
    
    Returns:
        Dict with comparisons
    """
    return {
        'reactivity': 'Group 1 > Group 2',
        'ionization_energy': 'Group 1 < Group 2',
        'melting_point': 'Group 1 < Group 2',
        'oxide_type': 'Group 1: M2O (basic), Group 2: MO (basic)',
        'hydroxide': 'Group 1: MOH, Group 2: M(OH)2'
    }


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="alkali_metal_property",
            description="Get property of alkali metal.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="property_name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="alkaline_earth_property",
            description="Get property of alkaline earth metal.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="property_name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="compare_alkali_alkaline_earth",
            description="Compare Group 1 vs Group 2 properties.",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="diagonal_relationship",
            description="Check for diagonal relationship in periodic table.",
            input_schema=[
            InputSchemaField(name="element1", type="string", required=True),
            InputSchemaField(name="element2", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="flame_test_color",
            description="Return flame test color for s-block element.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="group_1_reaction",
            description="Describe reaction of Group 1 metal.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="reactant", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="group_2_reaction",
            description="Describe reaction of Group 2 metal.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True),
            InputSchemaField(name="reactant", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="s_block_trend",
            description="Describe trend in s-block properties.",
            input_schema=[
            InputSchemaField(name="property_type", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
