"""
Covalent Bonding Tools - L3 Implementation
Chapter 7.02: Covalent Bonding and Electronegativity

## Solver Instructions (for AI Agent)

When you encounter covalent bonding, electronegativity, bond polarity, and bond energy problems:

### Step 1: Identify what is given and what is asked
- Given: two elements, their positions on periodic table, bond type
- Asked: electronegativity values, bond classification, polarity, bond energy, % ionic character

### Step 2: Choose the correct function
- `get_electronegativity(element)`: Pauling electronegativity
- `classify_bond_type(element1, element2)`: Nonpolar covalent / polar covalent / ionic
- `bond_polarity(element1, element2)`: Partial charges (delta+ on less EN, delta- on more EN)
- `get_bond_energy(element1, element2, bond_order)`: Average bond energy (kJ/mol)
- `compare_bond_polarity(bonds)`: Rank bonds by polarity
- `percent_ionic_character(element1, element2)`: % ionic character from EN difference

### Step 3: Handle special cases
- DeltaEN < 0.5: nonpolar covalent; 0.5-1.7: polar covalent; >1.7: ionic
- % ionic character ~ 1 - exp(-0.25(DeltaEN)2)
- F is most electronegative (3.98); Fr least (0.7)

### Examples
```python
classify_bond_type('H', 'Cl')  # -> polar covalent (DeltaEN=0.96)
bond_polarity('H', 'Cl')  # -> ('H', 'delta+', 'Cl', 'delta-')
percent_ionic_character('H', 'F')  # -> ~59% (DeltaEN=1.78)
```
"""

# Pauling electronegativity values (selected elements)
ELECTRONEGATIVITY = {
    'H': 2.1, 'He': 0,
    'Li': 1.0, 'Be': 1.5, 'B': 2.0, 'C': 2.5, 'N': 3.0, 'O': 3.5, 'F': 4.0, 'Ne': 0,
    'Na': 0.9, 'Mg': 1.2, 'Al': 1.5, 'Si': 1.8, 'P': 2.1, 'S': 2.5, 'Cl': 3.0, 'Ar': 0,
    'K': 0.8, 'Ca': 1.0, 'Ga': 1.6, 'Ge': 1.8, 'As': 2.0, 'Se': 2.4, 'Br': 2.8, 'Kr': 0,
    'Rb': 0.8, 'Sr': 1.0, 'In': 1.7, 'Sn': 1.8, 'Sb': 1.9, 'Te': 2.1, 'I': 2.5, 'Xe': 0,
    'Cs': 0.7, 'Ba': 0.9, 'Tl': 1.8, 'Pb': 1.9, 'Bi': 1.9, 'Po': 2.0, 'At': 2.2, 'Rn': 0,
}

# Average bond energies (kJ/mol)
BOND_ENERGIES = {
    ('H', 'H'): 436, ('C', 'C'): 345, ('N', 'N'): 160, ('O', 'O'): 140,
    ('C', 'H'): 415, ('C', 'N'): 290, ('C', 'O'): 350, ('C', 'F'): 439,
    ('C', 'Cl'): 330, ('C', 'Br'): 275, ('C', 'I'): 240,
    ('N', 'H'): 390, ('O', 'H'): 464, ('F', 'H'): 569, ('Cl', 'H'): 432,
    ('Br', 'H'): 370, ('I', 'H'): 295,
    ('C', 'C', 2): 611, ('C', 'C', 3): 837,  # double, triple
    ('C', 'O', 2): 741, ('C', 'O', 3): 1080,  # double, triple
    ('N', 'N', 2): 418, ('N', 'N', 3): 946,  # double, triple
    ('O', 'O', 2): 498,  # O=O
    ('C', 'N', 2): 615, ('C', 'N', 3): 891,  # double, triple
}


def get_electronegativity(element: str) -> float:
    """Get electronegativity value for an element."""
    if element not in ELECTRONEGATIVITY:
        raise ValueError(f"Electronegativity not available for {element}")
    return ELECTRONEGATIVITY[element]


def classify_bond_type(element1: str, element2: str) -> dict:
    """
    Classify bond type based on electronegativity difference.
    
    Args:
        element1: First element symbol
        element2: Second element symbol
    
    Returns:
        Dictionary with bond classification details
    
    Examples:
        >>> classify_bond_type('H', 'H')
        {'delta_EN': 0.0, 'bond_type': 'pure covalent', 'polar': False}
        >>> classify_bond_type('H', 'Cl')
        {'delta_EN': 0.9, 'bond_type': 'polar covalent', 'polar': True, 'delta_plus': 'H', 'delta_minus': 'Cl'}
    """
    en1 = get_electronegativity(element1)
    en2 = get_electronegativity(element2)
    delta_en = abs(en1 - en2)
    
    # Classify bond type
    if delta_en == 0:
        bond_type = 'pure covalent'
        polar = False
    elif delta_en < 0.5:
        bond_type = 'mostly covalent'
        polar = False
    elif delta_en < 2.0:
        bond_type = 'polar covalent'
        polar = True
    else:
        bond_type = 'ionic'
        polar = True
    
    result = {
        'delta_EN': round(delta_en, 1),
        'bond_type': bond_type,
        'polar': polar
    }
    
    if polar and delta_en > 0:
        # Identify delta+ and delta- atoms
        if en1 < en2:
            result['delta_plus'] = element1
            result['delta_minus'] = element2
        else:
            result['delta_plus'] = element2
            result['delta_minus'] = element1
    
    return result


def bond_polarity(element1: str, element2: str) -> tuple:
    """
    Get bond polarity information.
    
    Args:
        element1: First element symbol
        element2: Second element symbol
    
    Returns:
        (delta_EN, delta_plus_atom, delta_minus_atom)
    
    Examples:
        >>> bond_polarity('H', 'O')
        (1.4, 'H', 'O')
    """
    en1 = get_electronegativity(element1)
    en2 = get_electronegativity(element2)
    delta_en = abs(en1 - en2)
    
    if en1 < en2:
        return (round(delta_en, 1), element1, element2)
    else:
        return (round(delta_en, 1), element2, element1)


def get_bond_energy(element1: str, element2: str, bond_order: int = 1) -> float:
    """
    Get average bond energy for a bond.
    
    Args:
        element1: First element symbol
        element2: Second element symbol
        bond_order: 1 for single, 2 for double, 3 for triple
    
    Returns:
        Bond energy in kJ/mol
    
    Examples:
        >>> get_bond_energy('C', 'H')
        415
        >>> get_bond_energy('C', 'O', 2)
        741
    """
    # Check for bond order-specific energy
    if bond_order > 1:
        key = (element1, element2, bond_order)
        key_rev = (element2, element1, bond_order)
        if key in BOND_ENERGIES:
            return BOND_ENERGIES[key]
        if key_rev in BOND_ENERGIES:
            return BOND_ENERGIES[key_rev]
    
    # Check for single bond
    key = (element1, element2)
    key_rev = (element2, element1)
    if key in BOND_ENERGIES:
        return BOND_ENERGIES[key]
    if key_rev in BOND_ENERGIES:
        return BOND_ENERGIES[key_rev]
    
    raise ValueError(f"Bond energy not available for {element1}-{element2}")


def compare_bond_polarity(bonds: list) -> list:
    """
    Rank bonds by polarity.
    
    Args:
        bonds: List of (element1, element2) tuples
    
    Returns:
        List of bonds sorted by polarity (increasing)
    
    Examples:
        >>> compare_bond_polarity([('C', 'H'), ('O', 'H'), ('N', 'H')])
        [('C', 'H', 0.4), ('N', 'H', 0.9), ('O', 'H', 1.4)]
    """
    results = []
    for e1, e2 in bonds:
        en1 = get_electronegativity(e1)
        en2 = get_electronegativity(e2)
        delta_en = abs(en1 - en2)
        results.append((e1, e2, round(delta_en, 1)))
    
    return sorted(results, key=lambda x: x[2])


def percent_ionic_character(element1: str, element2: str) -> float:
    """
    Calculate approximate percent ionic character.
    
    Args:
        element1: First element symbol
        element2: Second element symbol
    
    Returns:
        Percent ionic character (0-100)
    
    Examples:
        >>> percent_ionic_character('H', 'Cl')
        20.0
        >>> percent_ionic_character('Na', 'Cl')
        70.0
    """
    delta_en = abs(get_electronegativity(element1) - get_electronegativity(element2))
    
    # Empirical formula: % ionic ~ 16|DeltaEN| + 3.5(DeltaEN)2
    percent = 16 * delta_en + 3.5 * delta_en ** 2
    
    return min(100, round(percent, 1))


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'bond_polarity', 'description': "Get bond polarity information.\n\nArgs:\n    element1: First element symbol\n    element2: Second element symbol\n\nReturns:\n    (delta_EN, delta_plus_atom, delta_minus_atom)\n\nExamples:\n    >>> bond_polarity('H', 'O')\n    (1.4, 'H', 'O')", 'inputSchema': {'type': 'object', 'properties': {'element1': {'type': 'string', 'description': 'Element1'}, 'element2': {'type': 'string', 'description': 'Element2'}}, 'required': ['element1', 'element2']}},
    {'name': 'classify_bond_type', 'description': "Classify bond type based on electronegativity difference.\n\nArgs:\n    element1: First element symbol\n    element2: Second element symbol\n\nReturns:\n    Dictionary with bond classification details\n\nExamples:\n    >>> classify_bond_type('H', 'H')\n    {'delta_EN': 0.0, 'bond_type': 'pure covalent', 'polar': False}\n    >>> classify_bond_type('H', 'Cl')\n    {'delta_EN': 0.9, 'bond_type': 'polar covalent', 'polar': True, 'delta_plus': 'H', 'delta_minus': 'Cl'}", 'inputSchema': {'type': 'object', 'properties': {'element1': {'type': 'string', 'description': 'Element1'}, 'element2': {'type': 'string', 'description': 'Element2'}}, 'required': ['element1', 'element2']}},
    {'name': 'compare_bond_polarity', 'description': "Rank bonds by polarity.\n\nArgs:\n    bonds: List of (element1, element2) tuples\n\nReturns:\n    List of bonds sorted by polarity (increasing)\n\nExamples:\n    >>> compare_bond_polarity([('C', 'H'), ('O', 'H'), ('N', 'H')])\n    [('C', 'H', 0.4), ('N', 'H', 0.9), ('O', 'H', 1.4)]", 'inputSchema': {'type': 'object', 'properties': {'bonds': {'type': 'number', 'description': 'Bonds'}}, 'required': ['bonds']}},
    {'name': 'get_bond_energy', 'description': "Get average bond energy for a bond.\n\nArgs:\n    element1: First element symbol\n    element2: Second element symbol\n    bond_order: 1 for single, 2 for double, 3 for triple\n\nReturns:\n    Bond energy in kJ/mol\n\nExamples:\n    >>> get_bond_energy('C', 'H')\n    415\n    >>> get_bond_energy('C', 'O', 2)\n    741", 'inputSchema': {'type': 'object', 'properties': {'element1': {'type': 'string', 'description': 'Element1'}, 'element2': {'type': 'string', 'description': 'Element2'}, 'bond_order': {'type': 'string', 'description': 'Bond Order', 'default': 1}}, 'required': ['element1', 'element2']}},
    {'name': 'get_electronegativity', 'description': 'Get electronegativity value for an element.', 'inputSchema': {'type': 'object', 'properties': {'element': {'type': 'string', 'description': 'Element'}}, 'required': ['element']}},
    {'name': 'percent_ionic_character', 'description': "Calculate approximate percent ionic character.\n\nArgs:\n    element1: First element symbol\n    element2: Second element symbol\n\nReturns:\n    Percent ionic character (0-100)\n\nExamples:\n    >>> percent_ionic_character('H', 'Cl')\n    20.0\n    >>> percent_ionic_character('Na', 'Cl')\n    70.0", 'inputSchema': {'type': 'object', 'properties': {'element1': {'type': 'string', 'description': 'Element1'}, 'element2': {'type': 'string', 'description': 'Element2'}}, 'required': ['element1', 'element2']}}
]
