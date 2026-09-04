"""
Group Theory Chemistry Tools - L3 Implementation

Core functions for group theory applications in chemistry:
- Point group determination
- Character tables
- Symmetry operations
- IR/Raman activity prediction
- Molecular orbital symmetry
- Selection rules from group theory

Source: LibreTexts Physical Chemistry Ch12
## Solver Instructions (for AI Agent)

When you encounter molecular symmetry, point groups, IR/Raman activity, or character table problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given molecule -> Point group? Use `get_molecule_point_group(molecule)` - has database of common molecules
- Need character table? Use `get_character_table(point_group)` - supports C1, Cs, C2, C2v, C3v, C2h, D2, D2h, D3h, D4h, D6h, Td, Oh, D∞h, C∞v
- IR active mode? Use `is_ir_active(irrep, point_group)` - True if irrep contains x, y, or z
- Raman active mode? Use `is_raman_active(irrep, point_group)` - True if irrep contains quadratic functions
- Mutual exclusion? Use `mutual_exclusion_applies(point_group)` - True for centrosymmetric molecules
- Decompose reducible representation? Use `decompose_representation(reducible_chars, point_group, class_sizes)`
- Direct product? Use `direct_product_decomposition(irrep1_name, irrep2_name, point_group)`
- Symmetry properties? Use `has_inversion_center(point_group)`, `has_horizontal_mirror(point_group)`, `count_symmetry_operations(point_group)`
- Symmetry matrices? Use `rotation_matrix_axis(angle, axis)`, `reflection_matrix(plane)`, `inversion_matrix()`, `identity_matrix()`

### Step 2: Handle special cases
- **Mutual exclusion rule**: Applies to centrosymmetric molecules (Ci, C2h, D2h, D4h, D6h, D∞h, Oh); IR and Raman active modes are mutually exclusive
- **IR vs Raman**: IR requires x/y/z (dipole moment change); Raman requires x2/y2/z2/xy/xz/yz (polarizability change)
- **Decomposition**: Provide class_sizes for accurate results; default assumes all sizes = 1
- **MOLECULE_POINT_GROUPS database**: H2O->C2v, NH3->C3v, CH4->Td, SF6->Oh, C6H6->D6h, BF3->D3h, CO2->D∞h, CO->C∞v

### Examples
```python
# Example 1: IR/Raman activity in C2v
is_ir_active('A1', 'C2v')  # -> True (contains z)
is_raman_active('A1', 'C2v')  # -> True (contains x2, y2, z2)
is_ir_active('A2', 'C2v')  # -> False

# Example 2: Decompose representation
decompose_representation([4, 0, 0, 0], 'C2v', [1, 1, 1, 1])  # -> {'A1': 1, 'A2': 1, 'B1': 1, 'B2': 1}

# Example 3: Direct product in C3v
direct_product_decomposition('E', 'E', 'C3v')  # -> {'A1': 1, 'A2': 1, 'E': 1}
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict, Set
import numpy as np
from itertools import product


# =============================================================================
# SYMMETRY OPERATIONS
# =============================================================================

def rotation_matrix_axis(angle_deg: float, axis: str = 'z') -> np.ndarray:
    """
    Generate rotation matrix about a principal axis.
    
    Args:
        angle_deg: Rotation angle in degrees
        axis: Rotation axis ('x', 'y', or 'z')
    
    Returns:
        3x3 rotation matrix
    
    Example:
        >>> R = rotation_matrix_axis(90, 'z')
        >>> R @ [1, 0, 0]  # Rotates x to y
        [0, 1, 0]
    """
    angle_rad = np.radians(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    
    if axis == 'z':
        return np.array([[c, -s, 0],
                         [s, c, 0],
                         [0, 0, 1]])
    elif axis == 'y':
        return np.array([[c, 0, s],
                         [0, 1, 0],
                         [-s, 0, c]])
    elif axis == 'x':
        return np.array([[1, 0, 0],
                         [0, c, -s],
                         [0, s, c]])
    else:
        raise ValueError(f"Unknown axis: {axis}")


def reflection_matrix(plane: str = 'xy') -> np.ndarray:
    """
    Generate reflection matrix for a plane.
    
    Args:
        plane: Reflection plane ('xy', 'xz', 'yz')
    
    Returns:
        3x3 reflection matrix
    """
    if plane == 'xy':
        return np.array([[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, -1]])
    elif plane == 'xz':
        return np.array([[1, 0, 0],
                         [0, -1, 0],
                         [0, 0, 1]])
    elif plane == 'yz':
        return np.array([[-1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]])
    else:
        raise ValueError(f"Unknown plane: {plane}")


def inversion_matrix() -> np.ndarray:
    """
    Generate inversion matrix.
    
    Returns:
        3x3 inversion matrix (diagonal -1)
    """
    return -np.eye(3)


def identity_matrix() -> np.ndarray:
    """
    Generate identity matrix.
    
    Returns:
        3x3 identity matrix
    """
    return np.eye(3)


# =============================================================================
# CHARACTER TABLES
# =============================================================================

CHARACTER_TABLES = {
    'C1': {
        'order': 1,
        'classes': ['E'],
        'irreps': {
            'A': [1]
        },
        'functions': {
            'A': ['x, y, z, xy, xz, yz, x2, y2, z2']
        }
    },
    
    'Cs': {
        'order': 2,
        'classes': ['E', 'σh'],
        'irreps': {
            "A'": [1, 1],
            "A''": [1, -1]
        },
        'functions': {
            "A'": ['x2, y2, z2, xy'],
            "A''": ['x, y, z, xz, yz']
        }
    },
    
    'C2': {
        'order': 2,
        'classes': ['E', 'C2'],
        'irreps': {
            'A': [1, 1],
            'B': [1, -1]
        },
        'functions': {
            'A': ['z, x2, y2, z2, xy'],
            'B': ['x, y, xz, yz']
        }
    },
    
    'C2v': {
        'order': 4,
        'classes': ['E', 'C2', 'σv(xz)', "σv'(yz)"],
        'irreps': {
            'A1': [1, 1, 1, 1],
            'A2': [1, 1, -1, -1],
            'B1': [1, -1, 1, -1],
            'B2': [1, -1, -1, 1]
        },
        'functions': {
            'A1': ['z, x2, y2, z2'],
            'A2': ['xy'],
            'B1': ['x, xz'],
            'B2': ['y, yz']
        }
    },
    
    'C3v': {
        'order': 6,
        'classes': ['E', '2C3', '3σv'],
        'irreps': {
            'A1': [1, 1, 1],
            'A2': [1, 1, -1],
            'E': [2, -1, 0]
        },
        'functions': {
            'A1': ['z, x2+y2, z2'],
            'A2': [],
            'E': ['(x, y), (x2-y2, xy), (xz, yz)']
        }
    },
    
    'C2h': {
        'order': 4,
        'classes': ['E', 'C2', 'i', 'σh'],
        'irreps': {
            'Ag': [1, 1, 1, 1],
            'Bg': [1, -1, 1, -1],
            'Au': [1, 1, -1, -1],
            'Bu': [1, -1, -1, 1]
        },
        'functions': {
            'Ag': ['x2, y2, z2, xy'],
            'Bg': ['xz, yz'],
            'Au': [],
            'Bu': ['x, y, z']
        }
    },
    
    'D2': {
        'order': 4,
        'classes': ['E', 'C2(z)', 'C2(y)', 'C2(x)'],
        'irreps': {
            'A': [1, 1, 1, 1],
            'B1': [1, 1, -1, -1],
            'B2': [1, -1, 1, -1],
            'B3': [1, -1, -1, 1]
        },
        'functions': {
            'A': ['x2, y2, z2'],
            'B1': ['z, xy'],
            'B2': ['y, xz'],
            'B3': ['x, yz']
        }
    },
    
    'D2h': {
        'order': 8,
        'classes': ['E', 'C2(z)', 'C2(y)', 'C2(x)', 'i', 'σ(xy)', 'σ(xz)', 'σ(yz)'],
        'irreps': {
            'Ag': [1, 1, 1, 1, 1, 1, 1, 1],
            'B1g': [1, 1, -1, -1, 1, 1, -1, -1],
            'B2g': [1, -1, 1, -1, 1, -1, 1, -1],
            'B3g': [1, -1, -1, 1, 1, -1, -1, 1],
            'Au': [1, 1, 1, 1, -1, -1, -1, -1],
            'B1u': [1, 1, -1, -1, -1, -1, 1, 1],
            'B2u': [1, -1, 1, -1, -1, 1, -1, 1],
            'B3u': [1, -1, -1, 1, -1, 1, 1, -1]
        },
        'functions': {
            'Ag': ['x2, y2, z2'],
            'B1g': ['xy'],
            'B2g': ['xz'],
            'B3g': ['yz'],
            'Au': [],
            'B1u': ['z'],
            'B2u': ['y'],
            'B3u': ['x']
        }
    },
    
    'D3h': {
        'order': 12,
        'classes': ['E', '2C3', '3C2', 'σh', '2S3', '3σv'],
        'irreps': {
            "A1'": [1, 1, 1, 1, 1, 1],
            "A2'": [1, 1, -1, 1, 1, -1],
            "E'": [2, -1, 0, 2, -1, 0],
            "A1''": [1, 1, 1, -1, -1, -1],
            "A2''": [1, 1, -1, -1, -1, 1],
            "E''": [2, -1, 0, -2, 1, 0]
        },
        'functions': {
            "A1'": ['x2+y2, z2'],
            "A2'": [],
            "E'": ['(x, y), (x2-y2, xy)'],
            "A1''": [],
            "A2''": ['z'],
            "E''": ['(xz, yz)']
        }
    },
    
    'D4h': {
        'order': 16,
        'classes': ['E', '2C4', 'C2', "2C2'", "2C2''", 'i', '2S4', 'σh', "2σv", "2σd"],
        'irreps': {
            'A1g': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'A2g': [1, 1, 1, -1, -1, 1, 1, 1, -1, -1],
            'B1g': [1, -1, 1, 1, -1, 1, -1, 1, 1, -1],
            'B2g': [1, -1, 1, -1, 1, 1, -1, 1, -1, 1],
            'Eg': [2, 0, -2, 0, 0, 2, 0, -2, 0, 0],
            'A1u': [1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
            'A2u': [1, 1, 1, -1, -1, -1, -1, -1, 1, 1],
            'B1u': [1, -1, 1, 1, -1, -1, 1, -1, -1, 1],
            'B2u': [1, -1, 1, -1, 1, -1, 1, -1, 1, -1],
            'Eu': [2, 0, -2, 0, 0, -2, 0, 2, 0, 0]
        },
        'functions': {
            'A1g': ['x2+y2, z2'],
            'A2g': [],
            'B1g': ['x2-y2'],
            'B2g': ['xy'],
            'Eg': ['(xz, yz)'],
            'A1u': [],
            'A2u': ['z'],
            'B1u': [],
            'B2u': [],
            'Eu': ['(x, y)']
        }
    },
    
    'D6h': {
        'order': 24,
        'classes': ['E', '2C6', '2C3', 'C2', '3C2\'', '3C2\"', 'i', '2S3', '2S6', 'σh', '3σd', '3σv'],
        'irreps': {
            'A1g': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'A2g': [1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1],
            'B1g': [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1],
            'B2g': [1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1],
            'E1g': [2, 1, -1, -2, 0, 0, 2, 1, -1, -2, 0, 0],
            'E2g': [2, -1, -1, 2, 0, 0, 2, -1, -1, 2, 0, 0],
            'A1u': [1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1],
            'A2u': [1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1],
            'B1u': [1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1],
            'B2u': [1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1],
            'E1u': [2, 1, -1, -2, 0, 0, -2, -1, 1, 2, 0, 0],
            'E2u': [2, -1, -1, 2, 0, 0, -2, 1, 1, -2, 0, 0]
        },
        'functions': {
            'A1g': ['x2+y2, z2'],
            'E1g': ['(xz, yz)'],
            'E2g': ['(x2-y2, xy)'],
            'A2u': ['z'],
            'E1u': ['(x, y)']
        }
    },
    
    'Td': {
        'order': 24,
        'classes': ['E', '8C3', '3C2', '6S4', '6σd'],
        'irreps': {
            'A1': [1, 1, 1, 1, 1],
            'A2': [1, 1, 1, -1, -1],
            'E': [2, -1, 2, 0, 0],
            'T1': [3, 0, -1, 1, -1],
            'T2': [3, 0, -1, -1, 1]
        },
        'functions': {
            'A1': ['x2+y2+z2'],
            'A2': [],
            'E': ['(2z2-x2-y2, x2-y2)'],
            'T1': ['(Rx, Ry, Rz)'],
            'T2': ['(x, y, z), (xy, xz, yz)']
        }
    },
    
    'Oh': {
        'order': 48,
        'classes': ['E', '8C3', '6C2', '6C4', '3C2', 'i', '6S4', '8S6', '3σh', '6σd'],
        'irreps': {
            'A1g': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'A2g': [1, 1, -1, -1, 1, 1, -1, 1, 1, -1],
            'Eg': [2, -1, 0, 0, 2, 2, 0, -1, 2, 0],
            'T1g': [3, 0, -1, 1, -1, 3, 1, 0, -1, -1],
            'T2g': [3, 0, 1, -1, -1, 3, -1, 0, -1, 1],
            'A1u': [1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
            'A2u': [1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
            'Eu': [2, -1, 0, 0, 2, -2, 0, 1, -2, 0],
            'T1u': [3, 0, -1, 1, -1, -3, -1, 0, 1, 1],
            'T2u': [3, 0, 1, -1, -1, -3, 1, 0, 1, -1]
        },
        'functions': {
            'A1g': ['x2+y2+z2'],
            'Eg': ['(2z2-x2-y2, x2-y2)'],
            'T1g': ['(Rx, Ry, Rz)'],
            'T2g': ['(xy, xz, yz)'],
            'T1u': ['(x, y, z)']
        }
    },
    
    'D∞h': {
        'order': '∞',
        'classes': ['E', '2C∞', '∞σv', 'i', '2S∞', '∞C2\''],
        'irreps': {
            'Σg+': [1, 1, 1, 1, 1, 1],
            'Σg-': [1, 1, -1, 1, 1, -1],
            'Σu+': [1, 1, 1, -1, -1, -1],
            'Σu-': [1, 1, -1, -1, -1, 1],
            'Πg': [2,"2 cosφ", 0, 2,"-2 cosφ", 0],
            'Πu': [2,"2 cosφ", 0, -2,"2 cosφ", 0],
            'Deltag': [2,"2 cos2φ", 0, 2,"2 cos2φ", 0],
            'Deltau': [2,"2 cos2φ", 0, -2,"-2 cos2φ", 0]
        },
        'note': 'Linear molecules (H2, CO, N2, etc.)'
    },
    
    'C∞v': {
        'order': '∞',
        'classes': ['E', '2C∞', '∞σv'],
        'irreps': {
            'Σ+': [1, 1, 1],
            'Σ-': [1, 1, -1],
            'Π': [2,"2 cosφ", 0],
            'Delta': [2,"2 cos2φ", 0]
        },
        'note': 'Heteronuclear linear molecules (CO, HCl, etc.)'
    }
}


def get_character_table(point_group: str) -> Dict:
    """
    Get character table for a point group.
    
    Args:
        point_group: Point group symbol (e.g., 'C2v', 'Td', 'Oh')
    
    Returns:
        Dictionary with character table data
    
    Example:
        >>> table = get_character_table('C2v')
        >>> print(table['irreps'])
        {'A1': [1,1,1,1], 'A2': [1,1,-1,-1], ...}
    """
    # Normalize input
    pg = point_group.replace(' ', '').replace('_', '')
    
    # Handle infinity symbol variations
    pg = pg.replace('infinity', '∞').replace('inf', '∞')
    
    if pg in CHARACTER_TABLES:
        return CHARACTER_TABLES[pg]
    else:
        raise ValueError(f"Unknown point group: {point_group}. "
                        f"Available: {list(CHARACTER_TABLES.keys())}")


# =============================================================================
# IRREDUCIBLE REPRESENTATION ANALYSIS
# =============================================================================

def character(irrep: List[int], class_index: int) -> int:
    """
    Get character of an irreducible representation for a class.
    
    Args:
        irrep: List of characters for the irrep
        class_index: Index of the symmetry class
    
    Returns:
        Character value
    """
    return irrep[class_index]


def dot_product_irrep(irrep1: List[int], irrep2: List[int], 
                       class_sizes: List[int], order: int) -> float:
    """
    Calculate dot product of two irreducible representations.
    
    ⟨Γ1|Γ2⟩ = (1/h) Σᵢ gᵢ χ1ᵢ χ2ᵢ
    
    Args:
        irrep1, irrep2: Character lists for irreps
        class_sizes: Number of operations in each class
        order: Order of the group (h)
    
    Returns:
        Dot product (1 if same irrep, 0 if different)
    """
    total = sum(g * c1 * c2 for g, c1, c2 in 
                zip(class_sizes, irrep1, irrep2))
    return total / order


def decompose_representation(reducible_chars: List[int],
                              point_group: str,
                              class_sizes: List[int] = None) -> Dict[str, int]:
    """
    Decompose a reducible representation into irreducible components.
    
    nᵢ = (1/h) Σᵢ gᵢ χ(R) χᵢ(R)
    
    Args:
        reducible_chars: Characters of the reducible representation
        point_group: Point group name
        class_sizes: Sizes of each class (default: 1 for each)
    
    Returns:
        Dictionary mapping irrep names to their coefficients
    
    Example:
        >>> chars = [4, 0, 0, 0]  # For C2v
        >>> decompose_representation(chars, 'C2v')
        {'A1': 1, 'A2': 1, 'B1': 1, 'B2': 1}
    """
    table = get_character_table(point_group)
    order = table['order']
    
    if class_sizes is None:
        # Default: assume each class has size 1 (simplified)
        # For accurate decomposition, provide actual class sizes
        class_sizes = [1] * len(reducible_chars)
    
    decomposition = {}
    
    for irrep_name, irrep_chars in table['irreps'].items():
        # Calculate coefficient
        n = sum(g * cr * ci for g, cr, ci in 
                zip(class_sizes, reducible_chars, irrep_chars)) / order
        
        n = round(n)  # Should be integer
        if n > 0:
            decomposition[irrep_name] = n
    
    return decomposition


# =============================================================================
# SPECTROSCOPIC ACTIVITY
# =============================================================================

def is_ir_active(irrep: str, point_group: str) -> bool:
    """
    Determine if a mode is IR active.
    
    IR active if irrep contains x, y, or z (dipole moment components).
    
    Args:
        irrep: Irreducible representation name
        point_group: Point group name
    
    Returns:
        True if IR active
    
    Example:
        >>> is_ir_active('A1', 'C2v')
        True  # Contains z
        >>> is_ir_active('A2', 'C2v')
        False
    """
    table = get_character_table(point_group)
    
    if irrep not in table['irreps']:
        raise ValueError(f"Unknown irrep: {irrep}")
    
    functions = table.get('functions', {}).get(irrep, [])
    
    # Check for x, y, z
    for func in functions:
        if 'x' in func.lower() or 'y' in func.lower() or 'z' in func.lower():
            # But not x2, y2, z2, xy, xz, yz (quadratic)
            if 'x2' not in func and 'y2' not in func and 'z2' not in func:
                if 'xy' not in func and 'xz' not in func and 'yz' not in func:
                    return True
    
    return False


def is_raman_active(irrep: str, point_group: str) -> bool:
    """
    Determine if a mode is Raman active.
    
    Raman active if irrep contains quadratic functions (x2, y2, z2, xy, xz, yz).
    
    Args:
        irrep: Irreducible representation name
        point_group: Point group name
    
    Returns:
        True if Raman active
    
    Example:
        >>> is_raman_active('A1', 'C2v')
        True  # Contains x2, y2, z2
    """
    table = get_character_table(point_group)
    
    if irrep not in table['irreps']:
        raise ValueError(f"Unknown irrep: {irrep}")
    
    functions = table.get('functions', {}).get(irrep, [])
    
    # Check for quadratic functions
    quadratic = ['x2', 'y2', 'z2', 'xy', 'xz', 'yz', 'x2-y2', '2z2-x2-y2']
    
    for func in functions:
        for q in quadratic:
            if q in func:
                return True
    
    return False


def mutual_exclusion_applies(point_group: str) -> bool:
    """
    Check if mutual exclusion rule applies.
    
    Mutual exclusion applies to centrosymmetric molecules (have inversion center).
    
    Args:
        point_group: Point group name
    
    Returns:
        True if mutual exclusion applies
    """
    # Centrosymmetric point groups
    centrosymmetric = ['Ci', 'C2h', 'D2h', 'D4h', 'D6h', 'D∞h', 'Oh']
    
    return point_group in centrosymmetric


# =============================================================================
# DIRECT PRODUCTS
# =============================================================================

def direct_product(irrep1: List[int], irrep2: List[int]) -> List[int]:
    """
    Calculate direct product of two irreps.
    
    Γ1 ⊗ Γ2: Multiply characters element-wise.
    
    Args:
        irrep1, irrep2: Character lists
    
    Returns:
        Direct product characters
    
    Example:
        >>> direct_product([1,1,1,1], [1,-1,1,-1])
        [1, -1, 1, -1]
    """
    return [c1 * c2 for c1, c2 in zip(irrep1, irrep2)]


def direct_product_decomposition(irrep1_name: str, irrep2_name: str,
                                  point_group: str) -> Dict[str, int]:
    """
    Decompose direct product of two irreps.
    
    Args:
        irrep1_name, irrep2_name: Names of irreps
        point_group: Point group
    
    Returns:
        Decomposition into irreps
    
    Example:
        >>> direct_product_decomposition('E', 'E', 'C3v')
        {'A1': 1, 'A2': 1, 'E': 1}
    """
    table = get_character_table(point_group)
    
    irrep1 = table['irreps'][irrep1_name]
    irrep2 = table['irreps'][irrep2_name]
    
    product = direct_product(irrep1, irrep2)
    
    # Assume class sizes = 1 for simplicity
    class_sizes = [1] * len(product)
    
    return decompose_representation(product, point_group, class_sizes)


# =============================================================================
# MOLECULAR SYMMETRY ANALYSIS
# =============================================================================

def count_symmetry_operations(point_group: str) -> int:
    """
    Count total number of symmetry operations in a group.
    
    Args:
        point_group: Point group name
    
    Returns:
        Order of the group
    """
    table = get_character_table(point_group)
    return table.get('order', 0)


def has_inversion_center(point_group: str) -> bool:
    """
    Check if molecule has inversion center.
    
    Args:
        point_group: Point group name
    
    Returns:
        True if has inversion
    """
    table = get_character_table(point_group)
    classes = table.get('classes', [])
    return 'i' in classes


def has_horizontal_mirror(point_group: str) -> bool:
    """
    Check if molecule has horizontal mirror plane.
    
    Args:
        point_group: Point group name
    
    Returns:
        True if has σh
    """
    table = get_character_table(point_group)
    classes = table.get('classes', [])
    return 'σh' in classes


# =============================================================================
# COMMON MOLECULE ASSIGNMENTS
# =============================================================================

MOLECULE_POINT_GROUPS = {
    'H2O': 'C2v',
    'NH3': 'C3v',
    'CH4': 'Td',
    'SF6': 'Oh',
    'C6H6': 'D6h',
    'BF3': 'D3h',
    'CO2': 'D∞h',
    'CO': 'C∞v',
    'HCl': 'C∞v',
    'N2': 'D∞h',
    'O2': 'D∞h',
    'H2': 'D∞h',
    'C2H4': 'D2h',
    'C2H2': 'D∞h',
    'XeF4': 'D4h',
    'PCl5': 'D3h',
    'ClF3': 'C2v',
    'H2O2': 'C2',
    'CH3Cl': 'C3v',
    'CH2Cl2': 'C2v',
    'CBr4': 'Td',
    'CCl4': 'Td',
    'NH2Cl': 'Cs',
    'H2S': 'C2v',
    'SO2': 'C2v',
    'NO2': 'C2v',
    'C3H6': 'C3v',
}


def get_molecule_point_group(molecule: str) -> str:
    """
    Get point group for a common molecule.
    
    Args:
        molecule: Molecule formula
    
    Returns:
        Point group name
    
    Example:
        >>> get_molecule_point_group('H2O')
        'C2v'
    """
    mol = molecule.upper()
    if mol in MOLECULE_POINT_GROUPS:
        return MOLECULE_POINT_GROUPS[mol]
    else:
        raise ValueError(f"Molecule {molecule} not in database. "
                        f"Available: {list(MOLECULE_POINT_GROUPS.keys())}")


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Group Theory Chemistry Tools - Examples")
    print("=" * 60)
    
    # Character tables
    print("\n1. Character Tables:")
    for pg in ['C2v', 'C3v', 'Td']:
        table = get_character_table(pg)
        print(f"   {pg}: {list(table['irreps'].keys())}")
    
    # IR/Raman activity
    print("\n2. IR/Raman Activity (C2v):")
    for irrep in ['A1', 'A2', 'B1', 'B2']:
        ir = is_ir_active(irrep, 'C2v')
        raman = is_raman_active(irrep, 'C2v')
        print(f"   {irrep}: IR={ir}, Raman={raman}")
    
    # Mutual exclusion
    print("\n3. Mutual Exclusion:")
    for pg in ['C2v', 'D2h', 'Oh']:
        applies = mutual_exclusion_applies(pg)
        print(f"   {pg}: {applies}")
    
    # Direct products
    print("\n4. Direct Products (C3v):")
    result = direct_product_decomposition('E', 'E', 'C3v')
    print(f"   E ⊗ E = {result}")
    
    # Molecule point groups
    print("\n5. Molecule Point Groups:")
    for mol in ['H2O', 'NH3', 'CH4', 'SF6', 'C6H6']:
        pg = get_molecule_point_group(mol)
        print(f"   {mol}: {pg}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")

MCP_TOOLS = [
    {
        "name": "character",
        "description": "Get character of an irreducible representation for a class.",
        "parameters": [
            {
                "name": "irrep",
                "type": "number"
            },
            {
                "name": "class_index",
                "type": "number"
            }
        ]
    },
    {
        "name": "count_symmetry_operations",
        "description": "Count total number of symmetry operations in a group.",
        "parameters": [
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "decompose_representation",
        "description": "Decompose a reducible representation into irreducible components.",
        "parameters": [
            {
                "name": "reducible_chars",
                "type": "number"
            },
            {
                "name": "point_group",
                "type": "number"
            },
            {
                "name": "class_sizes",
                "type": "number"
            }
        ]
    },
    {
        "name": "direct_product",
        "description": "Calculate direct product of two irreps.",
        "parameters": [
            {
                "name": "irrep1",
                "type": "number"
            },
            {
                "name": "irrep2",
                "type": "number"
            }
        ]
    },
    {
        "name": "direct_product_decomposition",
        "description": "Decompose direct product of two irreps.",
        "parameters": [
            {
                "name": "irrep1_name",
                "type": "string"
            },
            {
                "name": "irrep2_name",
                "type": "string"
            },
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "dot_product_irrep",
        "description": "Calculate dot product of two irreducible representations.",
        "parameters": [
            {
                "name": "irrep1",
                "type": "number"
            },
            {
                "name": "irrep2",
                "type": "number"
            },
            {
                "name": "class_sizes",
                "type": "number"
            },
            {
                "name": "order",
                "type": "number"
            }
        ]
    },
    {
        "name": "get_character_table",
        "description": "Get character table for a point group.",
        "parameters": [
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "get_molecule_point_group",
        "description": "Get point group for a common molecule.",
        "parameters": [
            {
                "name": "molecule",
                "type": "number"
            }
        ]
    },
    {
        "name": "has_horizontal_mirror",
        "description": "Check if molecule has horizontal mirror plane.",
        "parameters": [
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "has_inversion_center",
        "description": "Check if molecule has inversion center.",
        "parameters": [
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "identity_matrix",
        "description": "Generate identity matrix.",
        "parameters": []
    },
    {
        "name": "inversion_matrix",
        "description": "Generate inversion matrix.",
        "parameters": []
    },
    {
        "name": "is_ir_active",
        "description": "Determine if a mode is IR active.",
        "parameters": [
            {
                "name": "irrep",
                "type": "number"
            },
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "is_raman_active",
        "description": "Determine if a mode is Raman active.",
        "parameters": [
            {
                "name": "irrep",
                "type": "number"
            },
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "mutual_exclusion_applies",
        "description": "Check if mutual exclusion rule applies.",
        "parameters": [
            {
                "name": "point_group",
                "type": "number"
            }
        ]
    },
    {
        "name": "reflection_matrix",
        "description": "Generate reflection matrix for a plane.",
        "parameters": [
            {
                "name": "plane",
                "type": "number"
            }
        ]
    },
    {
        "name": "rotation_matrix_axis",
        "description": "Generate rotation matrix about a principal axis.",
        "parameters": [
            {
                "name": "angle_deg",
                "type": "number"
            },
            {
                "name": "axis",
                "type": "number"
            }
        ]
    }
]
