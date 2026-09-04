"""
Ionic Bonding Tools - L3 Implementation
Chapter 7.01: Ionic Bonding and Ion Formation
## Solver Instructions (for AI Agent)

When you encounter ionic bonding, ion formation, or lattice energy problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Predict ion charge? Use `predict_ion_charge(element, group)` - returns int or list of common charges
- Write ionic formula? Use `ionic_formula(cation, cation_charge, anion, anion_charge)`
- Ion electron configuration? Use `ion_electron_config(element, charge)`
- Compare lattice energies? Use `compare_lattice_energy(compound1, compound2)` - tuples of (cat_charge, an_charge, distance)
- Is compound ionic? Use `is_ionic_compound(element1, element2)` - True if metal + nonmetal

### Step 2: Handle special cases
- **Transition metals**: Often have multiple charges (e.g., Fe: +2 or +3; Cu: +1 or +2)
- **Ionic formula**: Polyatomic ions in parentheses when multiplied: Ca(NO3)2 not CaNO32
- **Lattice energy trends**: U ∝ (Z+xZ-)/r - higher charges and smaller distances = higher U
- **ION_CHARGES dict**: Pre-loaded for Groups 1-2, 13-17, and common transition metals

### Examples
```python
# Example 1: Ionic formula
ionic_formula('Al', 3, 'O', -2)  # -> 'Al2O3'
ionic_formula('Ca', 2, 'NO3', -1)  # -> 'Ca(NO3)2'

# Example 2: Compare lattice energy
compare_lattice_energy((2, 2, 200), (1, 1, 200))
# -> 'Compound 1 has higher lattice energy (4x vs 1x charge product)' (MgO vs NaCl)

# Example 3: Ion charge prediction
predict_ion_charge('Fe')  # -> [2, 3]
predict_ion_charge('Na')  # -> 1
```
"""

# Ion charge predictions based on group
ION_CHARGES = {
    # Group 1 (alkali metals)
    'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1, 'Fr': 1,
    # Group 2 (alkaline earth)
    'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2, 'Ra': 2,
    # Group 13
    'B': 3, 'Al': 3, 'Ga': 3, 'In': 3, 'Tl': [1, 3],
    # Group 14
    'C': [4, -4], 'Si': 4, 'Ge': 4, 'Sn': [2, 4], 'Pb': [2, 4],
    # Group 15
    'N': -3, 'P': -3, 'As': -3, 'Sb': -3, 'Bi': [3, 5],
    # Group 16
    'O': -2, 'S': -2, 'Se': -2, 'Te': -2, 'Po': -2,
    # Group 17 (halogens)
    'F': -1, 'Cl': -1, 'Br': -1, 'I': -1, 'At': -1,
    # Transition metals (common charges)
    'Fe': [2, 3], 'Cu': [1, 2], 'Zn': 2, 'Ag': 1, 'Au': [1, 3],
    'Cr': [2, 3, 6], 'Mn': [2, 3, 4, 7], 'Co': [2, 3], 'Ni': 2,
}

# Noble gas electron configurations for ion shorthand
NOBLE_GAS_CONFIGS = {
    'He': '1s2',
    'Ne': '1s2 2s2 2p6',
    'Ar': '1s2 2s2 2p6 3s2 3p6',
    'Kr': '1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6',
    'Xe': '1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6',
}


def predict_ion_charge(element: str, group: int = None) -> int | list:
    """
    Predict ion charge for an element.
    
    Args:
        element: Element symbol
        group: Periodic table group (optional, used for validation)
    
    Returns:
        Predicted ion charge (int) or list of common charges
    
    Examples:
        >>> predict_ion_charge('Na')
        1
        >>> predict_ion_charge('Fe')
        [2, 3]
        >>> predict_ion_charge('O')
        -2
    """
    if element in ION_CHARGES:
        return ION_CHARGES[element]
    
    # Predict from group if not in table
    if group is not None:
        if group in [1]:
            return 1
        elif group == 2:
            return 2
        elif group in [13]:
            return 3
        elif group in [14]:
            return [4, -4]
        elif group in [15]:
            return -3
        elif group in [16]:
            return -2
        elif group in [17]:
            return -1
    
    raise ValueError(f"Cannot predict charge for {element}")


def ionic_formula(cation: str, cation_charge: int, 
                   anion: str, anion_charge: int) -> str:
    """
    Generate ionic compound formula from ions.
    
    Args:
        cation: Cation symbol
        cation_charge: Cation charge (positive)
        anion: Anion symbol
        anion_charge: Anion charge (negative)
    
    Returns:
        Empirical formula string
    
    Examples:
        >>> ionic_formula('Na', 1, 'Cl', -1)
        'NaCl'
        >>> ionic_formula('Al', 3, 'O', -2)
        'Al2O3'
        >>> ionic_formula('Ca', 2, 'NO3', -1)
        'Ca(NO3)2'
    """
    import re
    
    # Make charges positive for calculation
    cat_charge = abs(cation_charge)
    an_charge = abs(anion_charge)
    
    # Find LCM for charge balance
    from math import gcd
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    total = lcm(cat_charge, an_charge)
    cat_count = total // cat_charge
    an_count = total // an_charge
    
    # Build formula
    cat_part = cation if cat_count == 1 else f"{cation}{cat_count}"
    
    # Check if anion is polyatomic (has more than one element)
    # Count element symbols (uppercase letter followed by optional lowercase)
    element_pattern = r'[A-Z][a-z]?'
    elements = re.findall(element_pattern, anion)
    is_polyatomic = len(elements) > 1 or '(' in anion
    
    if an_count == 1:
        an_part = anion
    else:
        if is_polyatomic:
            an_part = f"({anion}){an_count}"
        else:
            an_part = f"{anion}{an_count}"
    
    return cat_part + an_part


def ion_electron_config(element: str, charge: int) -> str:
    """
    Predict electron configuration of an ion.
    
    Args:
        element: Neutral element symbol
        charge: Ion charge (positive = cation, negative = anion)
    
    Returns:
        Electron configuration string
    
    Examples:
        >>> ion_electron_config('Na', 1)
        '[Ne]'
        >>> ion_electron_config('O', -2)
        '[Ne]'
        >>> ion_electron_config('Fe', 2)
        '[Ar] 3d6'
        >>> ion_electron_config('Fe', 3)
        '[Ar] 3d5'
    """
    from .electron_configuration_tools import get_ground_state_config, noble_gas_core
    
    # Get neutral atom configuration
    neutral_config = get_ground_state_config(element)
    
    # Adjust for ion charge
    if charge > 0:
        # Cation - remove electrons (from highest n first)
        total_electrons = sum(neutral_config.values()) - charge
    elif charge < 0:
        # Anion - add electrons
        total_electrons = sum(neutral_config.values()) + abs(charge)
    else:
        total_electrons = sum(neutral_config.values())
    
    # Find noble gas core
    return noble_gas_core(total_electrons)


def compare_lattice_energy(compound1: tuple, compound2: tuple) -> str:
    """
    Compare lattice energies of two ionic compounds.
    
    Args:
        compound1: (cation_charge, anion_charge, ion_distance)
        compound2: (cation_charge, anion_charge, ion_distance)
    
    Returns:
        Comparison result string
    
    Examples:
        >>> compare_lattice_energy((1, 1, 200), (2, 2, 200))
        'Compound 2 has higher lattice energy (4x vs 1x charge product)'
        >>> compare_lattice_energy((1, 1, 200), (1, 1, 300))
        'Compound 1 has higher lattice energy (smaller ion distance)'
    """
    z1_cat, z1_an, r1 = compound1
    z2_cat, z2_an, r2 = compound2
    
    # Lattice energy ∝ Z+ * Z- / R
    ratio1 = (z1_cat * z1_an) / r1
    ratio2 = (z2_cat * z2_an) / r2
    
    if ratio1 > ratio2:
        return f"Compound 1 has higher lattice energy ({ratio1/ratio2:.1f}x)"
    elif ratio2 > ratio1:
        return f"Compound 2 has higher lattice energy ({ratio2/ratio1:.1f}x)"
    else:
        return "Compounds have similar lattice energies"


def is_ionic_compound(element1: str, element2: str) -> bool:
    """
    Predict if compound between two elements is ionic.
    
    Args:
        element1: First element symbol
        element2: Second element symbol
    
    Returns:
        True if likely ionic, False otherwise
    
    Examples:
        >>> is_ionic_compound('Na', 'Cl')
        True
        >>> is_ionic_compound('C', 'H')
        False
    """
    # Simplified metal/nonmetal classification
    metals = {'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr',
              'Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra',
              'Al', 'Ga', 'In', 'Tl', 'Sn', 'Pb', 'Bi',
              'Fe', 'Cu', 'Zn', 'Ag', 'Au', 'Cr', 'Mn', 'Co', 'Ni'}
    
    nonmetals = {'H', 'C', 'N', 'O', 'P', 'S', 'Se',
                 'F', 'Cl', 'Br', 'I', 'At'}
    
    # Ionic if metal + nonmetal
    e1_metal = element1 in metals
    e2_metal = element2 in metals
    e1_nonmetal = element1 in nonmetals
    e2_nonmetal = element2 in nonmetals
    
    return (e1_metal and e2_nonmetal) or (e2_metal and e1_nonmetal)

MCP_TOOLS = [
    {
        "name": "compare_lattice_energy",
        "description": "Compare lattice energies of two ionic compounds.",
        "parameters": [
            {
                "name": "compound1",
                "type": "number"
            },
            {
                "name": "compound2",
                "type": "number"
            }
        ]
    },
    {
        "name": "ion_electron_config",
        "description": "Predict electron configuration of an ion.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            },
            {
                "name": "charge",
                "type": "number"
            }
        ]
    },
    {
        "name": "ionic_formula",
        "description": "Generate ionic compound formula from ions.",
        "parameters": [
            {
                "name": "cation",
                "type": "number"
            },
            {
                "name": "cation_charge",
                "type": "number"
            },
            {
                "name": "anion",
                "type": "number"
            },
            {
                "name": "anion_charge",
                "type": "number"
            }
        ]
    },
    {
        "name": "is_ionic_compound",
        "description": "Predict if compound between two elements is ionic.",
        "parameters": [
            {
                "name": "element1",
                "type": "string"
            },
            {
                "name": "element2",
                "type": "string"
            }
        ]
    },
    {
        "name": "predict_ion_charge",
        "description": "Predict ion charge for an element.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            },
            {
                "name": "group",
                "type": "number"
            }
        ]
    }
]
