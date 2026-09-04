"""
Organic Chemistry Tools - L3 Implementation
Chapter 20: Organic Chemistry

## Solver Instructions (for AI Agent)

When you encounter general organic chemistry problems - alkane naming, hydrocarbon formulas, functional group suffixes, alcohol classification, combustion balancing, or degree of unsaturation - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given carbon count -> need alkane name or molecular formula?
- Given hydrocarbon type and carbon count -> need formula?
- Given functional group name -> need IUPAC naming suffix?
- Given carbons attached to OH-bearing carbon -> classify alcohol?
- Given a hydrocarbon -> balance its combustion reaction?
- Given molecular formula -> calculate degree of unsaturation?
- Given carbon count -> estimate number of isomers?

### Step 2: Choose the correct function
- **Alkane name:** `alkane_name(carbons)` -> name for C1-C10, generic for higher
- **Hydrocarbon formula:** `hydrocarbon_formula(carbons, hydrocarbon_type)` -> 'CnHm'. Alkane: 2n+2, alkene: 2n, alkyne: 2n-2
- **Functional group suffix:** `functional_group_suffix(group)` -> 'ane', 'ene', 'yne', 'ol', 'al', 'one', 'oic acid', 'amine', 'oate'
- **Alcohol classification:** `classify_alcohol(carbons_alpha_to_OH)` -> 'primary' (1), 'secondary' (2), 'tertiary' (3)
- **Combustion balance:** `combustion_balance(carbons, hydrogens)` -> balanced coefficients for CxHy + O2 -> CO2 + H2O (GCD-simplified)
- **Degree of unsaturation:** `degree_of_unsaturation(carbons, hydrogens, halogens=0, nitrogens=0)` -> DU = (2C+2+N-H-X)/2
- **Isomer count:** `isomer_count_possible(carbons, hydrocarbon_type)` -> known counts for C1-C10 alkanes

### Step 3: Handle special cases
- Degree of unsaturation: halogens count as H (subtract), nitrogens add one H (add N)
- DU = 1 could be one double bond or one ring; DU = 4 could be benzene (3 double bonds + 1 ring)
- Combustion coefficients are automatically simplified by GCD
- Only C1-C10 alkane isomer counts are exact; beyond that, returns 'many'

### Examples
```python
# Example 1: Formula of C5 alkene
hydrocarbon_formula(5, 'alkene')  -> 'C5H10'

# Example 2: Classify alcohol with 3 carbons on alpha-carbon
classify_alcohol(3)  -> 'tertiary (3deg)'

# Example 3: Balance combustion of propane (C3H8)
combustion_balance(3, 8)  -> {'C3H8': 1, 'O2': 5, 'CO2': 3, 'H2O': 4}

# Example 4: Degree of unsaturation of benzene C6H6
degree_of_unsaturation(6, 6)  -> 4

# Example 5: How many hexane isomers?
isomer_count_possible(6, 'alkane')  -> 5
```
"""

from typing import Dict, Tuple, Optional, List


# Alkane names
ALKANE_NAMES = {
    1: 'methane', 2: 'ethane', 3: 'propane', 4: 'butane',
    5: 'pentane', 6: 'hexane', 7: 'heptane', 8: 'octane',
    9: 'nonane', 10: 'decane'
}

# Functional group suffixes
FUNCTIONAL_SUFFIXES = {
    'alkane': 'ane',
    'alkene': 'ene',
    'alkyne': 'yne',
    'alcohol': 'ol',
    'aldehyde': 'al',
    'ketone': 'one',
    'carboxylic_acid': 'oic acid',
    'amine': 'amine',
    'ester': 'oate'
}


def alkane_name(carbons: int) -> str:
    """
    Get alkane name from carbon count.
    
    Args:
        carbons: Number of carbon atoms
    
    Returns:
        Alkane name
    
    Examples:
        >>> alkane_name(4)
        'butane'
    """
    return ALKANE_NAMES.get(carbons, f'C{carbons}H{2*carbons+2}')


def hydrocarbon_formula(carbons: int, hydrocarbon_type: str = 'alkane') -> str:
    """
    Generate hydrocarbon formula.
    
    Args:
        carbons: Number of carbon atoms
        hydrocarbon_type: 'alkane', 'alkene', or 'alkyne'
    
    Returns:
        Molecular formula string
    
    Examples:
        >>> hydrocarbon_formula(4, 'alkane')
        'C4H10'
    """
    if hydrocarbon_type == 'alkane':
        hydrogens = 2 * carbons + 2
    elif hydrocarbon_type == 'alkene':
        hydrogens = 2 * carbons
    elif hydrocarbon_type == 'alkyne':
        hydrogens = 2 * carbons - 2
    else:
        return 'Unknown'
    
    return f'C{carbons}H{hydrogens}'


def functional_group_suffix(group: str) -> str:
    """
    Get suffix for functional group.
    
    Args:
        group: Functional group name
    
    Returns:
        Naming suffix
    """
    return FUNCTIONAL_SUFFIXES.get(group.lower(), '')


def classify_alcohol(carbons_alpha_to_OH: int) -> str:
    """
    Classify alcohol as primary, secondary, or tertiary.
    
    Args:
        carbons_alpha_to_OH: Number of carbons attached to carbon with OH
    
    Returns:
        Classification string
    
    Examples:
        >>> classify_alcohol(1)
        'primary'
        >>> classify_alcohol(3)
        'tertiary'
    """
    if carbons_alpha_to_OH == 1:
        return 'primary (1deg)'
    elif carbons_alpha_to_OH == 2:
        return 'secondary (2deg)'
    elif carbons_alpha_to_OH == 3:
        return 'tertiary (3deg)'
    else:
        return 'unknown'


def combustion_balance(carbons: int, hydrogens: int) -> Dict:
    """
    Balance combustion reaction for hydrocarbon.
    
    CₓHᵧ + O2 -> CO2 + H2O
    
    Balanced: CₓHᵧ + (x + y/4)O2 -> xCO2 + (y/2)H2O
    
    Multiply by 4 to avoid fractions:
    4CₓHᵧ + (4x + y)O2 -> 4xCO2 + 2yH2O
    
    Args:
        carbons: Number of C atoms
        hydrogens: Number of H atoms
    
    Returns:
        Dict with balanced coefficients
    
    Examples:
        >>> combustion_balance(1, 4)  # methane
        {'C1H4': 1, 'O2': 2, 'CO2': 1, 'H2O': 2}
    """
    # 4CₓHᵧ + (4x + y)O2 -> 4xCO2 + 2yH2O
    fuel_coef = 4
    o2_coef = 4 * carbons + hydrogens
    co2_coef = 4 * carbons
    h2o_coef = 2 * hydrogens
    
    # Simplify by GCD
    from math import gcd
    from functools import reduce
    
    coeffs = [fuel_coef, o2_coef, co2_coef, h2o_coef]
    divisor = reduce(gcd, coeffs)
    
    fuel_coef //= divisor
    o2_coef //= divisor
    co2_coef //= divisor
    h2o_coef //= divisor
    
    return {
        f'C{carbons}H{hydrogens}': fuel_coef,
        'O2': o2_coef,
        'CO2': co2_coef,
        'H2O': h2o_coef
    }


def degree_of_unsaturation(carbons: int, hydrogens: int, 
                           halogens: int = 0, nitrogens: int = 0) -> int:
    """
    Calculate degree of unsaturation (double bond equivalents).
    
    DU = (2C + 2 + N - H - X) / 2
    
    Args:
        carbons: Number of C atoms
        hydrogens: Number of H atoms
        halogens: Number of halogen atoms
        nitrogens: Number of N atoms
    
    Returns:
        Degree of unsaturation
    
    Examples:
        >>> degree_of_unsaturation(6, 6)  # benzene
        4
    """
    return (2 * carbons + 2 + nitrogens - hydrogens - halogens) // 2


def isomer_count_possible(carbons: int, hydrocarbon_type: str = 'alkane') -> int:
    """
    Return approximate number of structural isomers.
    
    Args:
        carbons: Number of carbon atoms
        hydrocarbon_type: Type of hydrocarbon
    
    Returns:
        Approximate isomer count
    """
    # Known alkane isomer counts
    alkane_isomers = {
        1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 5, 7: 9, 8: 18, 9: 35, 10: 75
    }
    
    if hydrocarbon_type == 'alkane':
        return alkane_isomers.get(carbons, 'many')
    else:
        return 'varies (many possible)'


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="alkane_name",
            description="Get alkane name from carbon count.",
            input_schema=[
            InputSchemaField(name="carbons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="classify_alcohol",
            description="Classify alcohol as primary, secondary, or tertiary.",
            input_schema=[
            InputSchemaField(name="carbons_alpha_to_OH", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="combustion_balance",
            description="Balance combustion reaction for hydrocarbon.",
            input_schema=[
            InputSchemaField(name="carbons", type="number", required=True),
            InputSchemaField(name="hydrogens", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="degree_of_unsaturation",
            description="Calculate degree of unsaturation (double bond equivalents).",
            input_schema=[
            InputSchemaField(name="carbons", type="number", required=True),
            InputSchemaField(name="hydrogens", type="number", required=True),
            InputSchemaField(name="halogens", type="number", required=False),
            InputSchemaField(name="nitrogens", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="functional_group_suffix",
            description="Get suffix for functional group.",
            input_schema=[
            InputSchemaField(name="group", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="hydrocarbon_formula",
            description="Generate hydrocarbon formula.",
            input_schema=[
            InputSchemaField(name="carbons", type="number", required=True),
            InputSchemaField(name="hydrocarbon_type", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="isomer_count_possible",
            description="Return approximate number of structural isomers.",
            input_schema=[
            InputSchemaField(name="carbons", type="number", required=True),
            InputSchemaField(name="hydrocarbon_type", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
