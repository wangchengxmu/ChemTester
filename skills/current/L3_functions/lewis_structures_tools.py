"""
Lewis Structures Tools - L3 Implementation
Chapter 7.03: Lewis Symbols and Structures
## Solver Instructions (for AI Agent)

When you encounter Lewis structure problems (valence electrons, octet rule, bonding), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Count valence electrons? Use `count_valence_electrons(atoms, charge=0)`
- Typical bonds for element? Use `typical_bonds(element)` - C=4, N=3, O=2, H/F/Cl/Br/I=1
- Lewis structure summary? Use `lewis_structure_summary(formula)` - parses formula, counts valence e-, identifies central atom
- Check octet violations? Use `octet_rule_violation(atoms, bonds, lone_pairs)` - returns violations
- Is element an octet exception? Use `is_octet_exception(element)` - B/Be (deficient), P/S/Cl (hypervalent)
- Electrons needed for octet? Use `bonds_needed_for_octet(element)`
- Duet rule check? Use `duet_rule(atom, electrons)` - for hydrogen only

### Step 2: Handle special cases
- **Charge adjustment**: For ions, subtract charge from total valence electrons (anion adds, cation removes)
- **Central atom**: Least electronegative non-H atom; in `lewis_structure_summary`, uses electronegativity ordering
- **Octet exceptions**: B and Be are electron-deficient (stable with < 8); P, S, Cl, Br, I can be hypervalent (> 8)
- **Hydrogen**: Always follows duet rule (2 electrons), never central atom in typical structures

### Examples
```python
# Example 1: Count valence electrons
count_valence_electrons(['C', 'O', 'O'], charge=-2)  # -> 24 (CO32-)
count_valence_electrons(['N', 'H', 'H', 'H', 'H'], charge=1)  # -> 8 (NH4+)

# Example 2: Lewis structure summary
lewis_structure_summary('CO2')  # -> {'atoms': ['C','O','O'], 'valence_e': 16, 'central': 'C'}

# Example 3: Octet exception check
is_octet_exception('B')  # -> (True, 'electron-deficient')
is_octet_exception('P')  # -> (True, 'hypervalent')
```
"""

# Valence electrons by group
_VALENCE_ELECTRONS = {
    'H': 1, 'He': 2,
    'Li': 1, 'Be': 2, 'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Ne': 8,
    'Na': 1, 'Mg': 2, 'Al': 3, 'Si': 4, 'P': 5, 'S': 6, 'Cl': 7, 'Ar': 8,
    'K': 1, 'Ca': 2, 'Ga': 3, 'Ge': 4, 'As': 5, 'Se': 6, 'Br': 7, 'Kr': 8,
    'Rb': 1, 'Sr': 2, 'In': 3, 'Sn': 4, 'Sb': 5, 'Te': 6, 'I': 7, 'Xe': 8,
}

_TYPICAL_BONDS = {
    'H': 1,
    'C': 4,
    'N': 3,
    'O': 2,
    'F': 1, 'Cl': 1, 'Br': 1, 'I': 1,
    'P': 3,
    'S': 2,
}


def count_valence_electrons(atoms: list, charge: int = 0) -> int:
    """
    Count total valence electrons in a molecule or ion.
    
    Args:
        atoms: List of element symbols
        charge: Molecular charge (positive = cation, negative = anion)
    
    Returns:
        Total number of valence electrons
    
    Examples:
        >>> count_valence_electrons(['H', 'O', 'H'])  # H2O
        8
        >>> count_valence_electrons(['C', 'O', 'O'], charge=-2)  # CO3^2-
        24
        >>> count_valence_electrons(['N', 'H', 'H', 'H', 'H'], charge=1)  # NH4+
        8
    """
    total = 0
    for atom in atoms:
        if atom not in _VALENCE_ELECTRONS:
            raise ValueError(f"Unknown element: {atom}")
        total += _VALENCE_ELECTRONS[atom]
    
    # Adjust for charge
    total -= charge  # Cations lose electrons, anions gain
    
    return total


def typical_bonds(element: str) -> int:
    """
    Get typical number of bonds for an element.
    
    Args:
        element: Element symbol
    
    Returns:
        Typical number of bonds
    
    Examples:
        >>> typical_bonds('C')
        4
        >>> typical_bonds('O')
        2
    """
    if element not in _TYPICAL_BONDS:
        raise ValueError(f"Unknown typical bonding for {element}")
    return _TYPICAL_BONDS[element]


def octet_rule_violation(atoms: list, bonds: dict, lone_pairs: dict) -> list:
    """
    Identify atoms that violate the octet rule.
    
    Args:
        atoms: List of element symbols
        bonds: Dict mapping atom index to number of bonds
        lone_pairs: Dict mapping atom index to number of lone pairs
    
    Returns:
        List of (atom_index, element, electrons, violation_type)
    
    Examples:
        >>> octet_rule_violation(['B', 'F', 'F', 'F'], {0: 3, 1: 1, 2: 1, 3: 1}, {0: 0, 1: 3, 2: 3, 3: 3})
        [(0, 'B', 6, 'electron-deficient')]
    """
    violations = []
    
    for i, atom in enumerate(atoms):
        if atom == 'H':
            continue  # H follows duet rule
        
        bonds_count = bonds.get(i, 0)
        lone_count = lone_pairs.get(i, 0)
        electrons = 2 * bonds_count + 2 * lone_count
        
        if electrons < 8:
            if atom in ['Be', 'B']:
                violations.append((i, atom, electrons, 'electron-deficient'))
            elif electrons % 2 == 1:
                violations.append((i, atom, electrons, 'odd-electron'))
        elif electrons > 8:
            # Check if element can be hypervalent (n >= 3)
            period = {'Li': 2, 'Be': 2, 'B': 2, 'C': 2, 'N': 2, 'O': 2, 'F': 2, 'Ne': 2,
                      'Na': 3, 'Mg': 3, 'Al': 3, 'Si': 3, 'P': 3, 'S': 3, 'Cl': 3, 'Ar': 3}
            if period.get(atom, 3) < 3:
                violations.append((i, atom, electrons, 'hypervalent'))
    
    return violations


def is_octet_exception(element: str) -> tuple:
    """
    Check if element commonly violates octet rule.
    
    Args:
        element: Element symbol
    
    Returns:
        (is_exception, exception_type)
    
    Examples:
        >>> is_octet_exception('B')
        (True, 'electron-deficient')
        >>> is_octet_exception('P')
        (True, 'hypervalent')
        >>> is_octet_exception('C')
        (False, None)
    """
    if element == 'H':
        return (True, 'duet')
    
    # Electron-deficient elements
    if element in ['Be', 'B', 'Al']:
        return (True, 'electron-deficient')
    
    # Can be hypervalent (n >= 3)
    hypervalent = ['P', 'S', 'Cl', 'Br', 'I', 'Xe', 'Kr']
    if element in hypervalent:
        return (True, 'hypervalent')
    
    return (False, None)


def lewis_structure_summary(formula: str) -> dict:
    """
    Generate a summary of Lewis structure properties.
    
    Args:
        formula: Chemical formula (e.g., 'H2O', 'CO2', 'CH4')
    
    Returns:
        Dictionary with valence electrons, typical bonds, etc.
    
    Examples:
        >>> lewis_structure_summary('H2O')
        {'formula': 'H2O', 'atoms': ['O', 'H', 'H'], 'valence_electrons': 8, 'central_atom': 'O'}
    """
    import re
    
    # Parse formula
    atoms = []
    matches = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    for element, count in matches:
        if element:
            count = int(count) if count else 1
            atoms.extend([element] * count)
    
    valence = count_valence_electrons(atoms)
    
    # Identify central atom (least electronegative, not H)
    en_order = ['Cs', 'Rb', 'K', 'Na', 'Li', 'Ba', 'Sr', 'Ca', 'Mg', 'Be',
                'Al', 'Mn', 'Zn', 'Cr', 'Fe', 'Cd', 'Co', 'Ni', 'Sn', 'Pb',
                'H', 'Ge', 'Cu', 'Si', 'B', 'Bi', 'Sb', 'As', 'P', 'Hg',
                'Te', 'Se', 'S', 'C', 'I', 'Br', 'Cl', 'N', 'O', 'F']
    
    non_h_atoms = [a for a in atoms if a != 'H']
    if non_h_atoms:
        central = min(non_h_atoms, key=lambda x: en_order.index(x) if x in en_order else 100)
    else:
        central = 'H'
    
    return {
        'formula': formula,
        'atoms': atoms,
        'valence_electrons': valence,
        'central_atom': central
    }


def bonds_needed_for_octet(element: str, current_electrons: int = 0) -> int:
    """
    Calculate number of electrons needed to complete octet.
    
    Args:
        element: Element symbol
        current_electrons: Current valence electrons
    
    Returns:
        Number of electrons needed
    
    Examples:
        >>> bonds_needed_for_octet('C')
        4
        >>> bonds_needed_for_octet('N')
        3
    """
    valence = _VALENCE_ELECTRONS.get(element, 0)
    
    if element == 'H':
        return 2 - valence
    
    return max(0, 8 - valence)


def duet_rule(atom: str, electrons: int) -> bool:
    """
    Check if atom satisfies duet rule (for H).
    
    Args:
        atom: Element symbol
        electrons: Number of electrons around atom
    
    Returns:
        True if duet satisfied
    
    Examples:
        >>> duet_rule('H', 2)
        True
        >>> duet_rule('H', 1)
        False
    """
    if atom != 'H':
        return True  # Not applicable
    
    return electrons == 2

MCP_TOOLS = [
    {
        "name": "bonds_needed_for_octet",
        "description": "Calculate number of electrons needed to complete octet.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            },
            {
                "name": "current_electrons",
                "type": "number"
            }
        ]
    },
    {
        "name": "count_valence_electrons",
        "description": "Count total valence electrons in a molecule or ion.",
        "parameters": [
            {
                "name": "atoms",
                "type": "number"
            },
            {
                "name": "charge",
                "type": "number"
            }
        ]
    },
    {
        "name": "duet_rule",
        "description": "Check if atom satisfies duet rule (for H).",
        "parameters": [
            {
                "name": "atom",
                "type": "number"
            },
            {
                "name": "electrons",
                "type": "number"
            }
        ]
    },
    {
        "name": "is_octet_exception",
        "description": "Check if element commonly violates octet rule.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            }
        ]
    },
    {
        "name": "lewis_structure_summary",
        "description": "Generate a summary of Lewis structure properties.",
        "parameters": [
            {
                "name": "formula",
                "type": "string"
            }
        ]
    },
    {
        "name": "octet_rule_violation",
        "description": "Identify atoms that violate the octet rule.",
        "parameters": [
            {
                "name": "atoms",
                "type": "number"
            },
            {
                "name": "bonds",
                "type": "number"
            },
            {
                "name": "lone_pairs",
                "type": "number"
            }
        ]
    },
    {
        "name": "typical_bonds",
        "description": "Get typical number of bonds for an element.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            }
        ]
    }
]
