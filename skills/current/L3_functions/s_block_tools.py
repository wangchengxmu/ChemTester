"""
L3 Tool: s-Block Elements Tools (Groups 1-2)
Predict oxide products, reactivity patterns, and compound properties.

Source: Petrucci General Chemistry, Ch21.1-21.3
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter s-block element problems (oxide products, nitride formation, compound properties, diagonal relationships), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Oxide product**: Given s-block element -> predict what oxide forms when burned in air
- **Nitride formation**: Given element -> predict if it reacts with N2
- **Compound solubility**: Given compound -> predict solubility
- **Amphoteric behavior**: Given element -> is the oxide/hydroxide amphoteric?
- **Diagonal relationship**: Given Li or Be -> what Group 2 element behaves similarly?

### Step 2: Choose the correct function
- `oxide_product(element)` -> dict with product formula and type (oxide/peroxide/superoxide)
- `reacts_with_nitrogen(element)` -> dict with boolean and product formula
- `compound_solubility(element, compound_type)` -> solubility prediction
- `is_amphoteric(element)` -> bool
- `diagonal_relationship(element)` -> related element across periods

### Step 3: Handle special cases
- **Group 1 oxides**: Li->Li2O (oxide), Na->Na2O2 (peroxide), K/Rb/Cs->MO2 (superoxide)
- **Group 2 oxides**: Be-Mg-Ca-Sr->MO, Ba->BaO2 (peroxide)
- **Nitrides**: Only Li in Group 1; all except Be in Group 2
- **Amphoteric**: BeO and Be(OH)2 are amphoteric (react with both acids and bases)
- Diagonal: Li↔Mg (both form nitrides, carbonates decompose on heating), Be↔Al (amphoteric)

### Examples
1. **Oxide product**: Potassium burned in air
   -> `oxide_product('K')` -> {'product': 'KO2', 'type': 'superoxide'}

2. **Nitride formation**: Does Ca react with N2?
   -> `reacts_with_nitrogen('Ca')` -> {'reacts': True, 'product': 'Ca3N2'}

3. **Amphoteric check**: Is BeO amphoteric?
   -> `is_amphoteric('Be')` -> True (BeO + 2HCl -> BeCl2 + H2O; BeO + 2NaOH -> Na2BeO2 + H2O)
"""

# Group 1 data
GROUP_1 = {
    'Li': {'oxide': 'Li2O', 'oxide_type': 'oxide', 'nitride': 'Li3N', 'reacts_n2': True},
    'Na': {'oxide': 'Na2O2', 'oxide_type': 'peroxide', 'nitride': None, 'reacts_n2': False},
    'K': {'oxide': 'KO2', 'oxide_type': 'superoxide', 'nitride': None, 'reacts_n2': False},
    'Rb': {'oxide': 'RbO2', 'oxide_type': 'superoxide', 'nitride': None, 'reacts_n2': False},
    'Cs': {'oxide': 'CsO2', 'oxide_type': 'superoxide', 'nitride': None, 'reacts_n2': False},
    'Fr': {'oxide': 'FrO2', 'oxide_type': 'superoxide', 'nitride': None, 'reacts_n2': False},
}

GROUP_2 = {
    'Be': {'oxide': 'BeO', 'oxide_type': 'oxide', 'nitride': None, 'reacts_n2': False, 'amphoteric': True},
    'Mg': {'oxide': 'MgO', 'oxide_type': 'oxide', 'nitride': 'Mg3N2', 'reacts_n2': True, 'amphoteric': False},
    'Ca': {'oxide': 'CaO', 'oxide_type': 'oxide', 'nitride': 'Ca3N2', 'reacts_n2': True, 'amphoteric': False},
    'Sr': {'oxide': 'SrO', 'oxide_type': 'oxide', 'nitride': 'Sr3N2', 'reacts_n2': True, 'amphoteric': False},
    'Ba': {'oxide': 'BaO2', 'oxide_type': 'peroxide', 'nitride': 'Ba3N2', 'reacts_n2': True, 'amphoteric': False},
    'Ra': {'oxide': 'RaO2', 'oxide_type': 'peroxide', 'nitride': 'Ra3N2', 'reacts_n2': True, 'amphoteric': False},
}

NOBLE_GASES = {
    'He': {'atomic_num': 2, 'ie': 2372},
    'Ne': {'atomic_num': 10, 'ie': 2081},
    'Ar': {'atomic_num': 18, 'ie': 1521},
    'Kr': {'atomic_num': 36, 'ie': 1351},
    'Xe': {'atomic_num': 54, 'ie': 1170},
    'Rn': {'atomic_num': 86, 'ie': 1037},
}

ION_CHARGES = {
    'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Fr': 1,
    'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Ra': 2,
    'Al': 3, 'Ga': 3, 'In': 3,
    'Zn': 2, 'Cd': 2, 'Hg': 2,
    'Ag': 1, 'Cu': 2,
    'Fe': 2, 'Co': 2, 'Ni': 2, 'Cr': 3, 'Mn': 2,
}


def oxide_product(element: str) -> dict:
    """
    Predict the oxide product when an s-block element burns in air.
    
    Group 1:
    - Li -> Li2O (oxide)
    - Na -> Na2O2 (peroxide)
    - K, Rb, Cs -> MO2 (superoxide)
    
    Group 2:
    - Be, Mg, Ca, Sr -> MO (oxide)
    - Ba -> BaO2 (peroxide)
    
    Args:
        element: Element symbol
    
    Returns:
        Dictionary with oxide product
    
    Example:
        >>> oxide_product('K')
        {'product': 'KO2', 'type': 'superoxide'}
    """
    element = element.capitalize()
    
    if element in GROUP_1:
        data = GROUP_1[element]
        return {
            'element': element,
            'group': 1,
            'product': data['oxide'],
            'type': data['oxide_type']
        }
    elif element in GROUP_2:
        data = GROUP_2[element]
        return {
            'element': element,
            'group': 2,
            'product': data['oxide'],
            'type': data['oxide_type']
        }
    else:
        return {'error': f'{element} not in s-block'}


def reacts_with_nitrogen(element: str) -> dict:
    """
    Predict if element reacts with N2.
    
    Group 1: Only Li reacts (Li3N)
    Group 2: All except Be react (M3N2)
    
    Args:
        element: Element symbol
    
    Returns:
        Dictionary with reaction prediction
    
    Example:
        >>> reacts_with_nitrogen('Li')
        {'reacts': True, 'product': 'Li3N'}
    """
    element = element.capitalize()
    
    if element in GROUP_1:
        data = GROUP_1[element]
        return {
            'element': element,
            'group': 1,
            'reacts': data['reacts_n2'],
            'product': data['nitride']
        }
    elif element in GROUP_2:
        data = GROUP_2[element]
        return {
            'element': element,
            'group': 2,
            'reacts': data['reacts_n2'],
            'product': data['nitride']
        }
    else:
        return {'error': f'{element} not in s-block'}


def hydration_energy_ranking(group: int) -> dict:
    """
    Return hydration energy ranking for s-block cations.
    
    Group 1: Li+ > Na+ > K+ > Rb+ > Cs+
    Group 2: Be2+ > Mg2+ > Ca2+ > Sr2+ > Ba2+
    
    Args:
        group: Group number (1 or 2)
    
    Returns:
        Dictionary with ranking
    
    Example:
        >>> hydration_energy_ranking(1)
        {'ranking': ['Li', 'Na', 'K', 'Rb', 'Cs'], 'trend': 'decreasing'}
    """
    if group == 1:
        return {
            'group': 1,
            'ranking': ['Li', 'Na', 'K', 'Rb', 'Cs'],
            'trend': 'decreasing (Li highest hydration energy)',
            'reason': 'Smaller ions have higher charge density'
        }
    elif group == 2:
        return {
            'group': 2,
            'ranking': ['Be', 'Mg', 'Ca', 'Sr', 'Ba'],
            'trend': 'decreasing (Be highest hydration energy)',
            'reason': 'Smaller ions with +2 charge have very high charge density'
        }
    else:
        return {'error': 'Group must be 1 or 2'}


def solubility_trend(compound_type: str) -> dict:
    """
    Return solubility trend for alkaline earth compounds.
    
    Hydroxides: solubility increases down group
    Carbonates: solubility decreases down group
    Sulfates: solubility decreases down group
    
    Args:
        compound_type: 'hydroxide', 'carbonate', or 'sulfate'
    
    Returns:
        Dictionary with solubility trend
    
    Example:
        >>> solubility_trend('sulfate')
        {'trend': 'decreasing', 'most_soluble': 'Be', 'least_soluble': 'Ba'}
    """
    compound_type = compound_type.lower()
    
    if compound_type == 'hydroxide':
        return {
            'compound': 'M(OH)2',
            'trend': 'increasing',
            'most_soluble': 'Ba',
            'least_soluble': 'Be',
            'reason': 'Lattice energy decreases faster than hydration energy'
        }
    elif compound_type == 'carbonate' or compound_type == 'sulfate':
        return {
            'compound': f'M{compound_type[:4]}',
            'trend': 'decreasing',
            'most_soluble': 'Be',
            'least_soluble': 'Ba',
            'reason': 'Hydration energy decreases faster than lattice energy'
        }
    else:
        return {'error': 'compound_type must be hydroxide, carbonate, or sulfate'}


def is_amphoteric(element: str) -> dict:
    """
    Check if s-block element forms amphoteric oxide.
    
    Only BeO is amphoteric among s-block oxides.
    
    Args:
        element: Element symbol
    
    Returns:
        Dictionary with amphotericity status
    
    Example:
        >>> is_amphoteric('Be')
        {'amphoteric': True, 'oxide': 'BeO'}
    """
    element = element.capitalize()
    
    if element in GROUP_2:
        data = GROUP_2[element]
        return {
            'element': element,
            'amphoteric': data.get('amphoteric', False),
            'oxide': data['oxide']
        }
    elif element in GROUP_1:
        return {
            'element': element,
            'amphoteric': False,
            'note': 'Group 1 oxides are all basic'
        }
    else:
        return {'error': f'{element} not in s-block'}


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "21-01",
        "question": "Oxide product for K",
        "element": "K",
        "expected_type": "superoxide"
    },
    {
        "id": "21-02",
        "question": "Oxide product for Na",
        "element": "Na",
        "expected_type": "peroxide"
    },
    {
        "id": "21-03",
        "question": "Nitrogen reaction for Mg",
        "element": "Mg",
        "expected_reacts": True
    },
    {
        "id": "21-04",
        "question": "Nitrogen reaction for Be",
        "element": "Be",
        "expected_reacts": False
    },
    {
        "id": "21-05",
        "question": "Nitrogen reaction for Na",
        "element": "Na",
        "expected_reacts": False
    },
]


if __name__ == "__main__":
    print("s-Block Elements Tools")
    print("=" * 40)
    
    # Test oxide products
    print("\nOxide Products:")
    for el in ['Li', 'Na', 'K', 'Be', 'Mg', 'Ba']:
        result = oxide_product(el)
        print(f"  {el}: {result['product']} ({result['type']})")
    
    # Test nitrogen reactions
    print("\nReacts with N2:")
    for el in ['Li', 'Na', 'K', 'Be', 'Mg', 'Ca']:
        result = reacts_with_nitrogen(el)
        status = 'Yes' if result['reacts'] else 'No'
        print(f"  {el}: {status} -> {result['product']}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="hydration_energy_ranking",
            description="Return hydration energy ranking for s-block cations.",
            input_schema=[
            InputSchemaField(name="group", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_amphoteric",
            description="Check if s-block element forms amphoteric oxide.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="oxide_product",
            description="Predict the oxide product when an s-block element burns in air.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reacts_with_nitrogen",
            description="Predict if element reacts with N2.",
            input_schema=[
            InputSchemaField(name="element", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="solubility_trend",
            description="Return solubility trend for alkaline earth compounds.",
            input_schema=[
            InputSchemaField(name="compound_type", type="string", required=True)
            ],
            handler="{name}",
        )
    ]
