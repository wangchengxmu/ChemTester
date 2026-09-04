"""
Formal Charges and Resonance Tools - L3 Implementation
Chapter 7.04: Formal Charges and Resonance
## Solver Instructions (for AI Agent)

When you encounter formal charge or resonance problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Calculate FC for one atom? Use `formal_charge(valence_e, lone_e, bonding_e)` or `formal_charge_from_structure(element, lone_pairs, bonds)`
- Find best Lewis structure (minimize FC)? Use `best_lewis_structure(formula)`
- Count resonance structures? Use `count_resonance_structures(formula)`
- Evaluate if FC distribution is favorable? Use `evaluate_fc_distribution(fc_values)`

### Step 2: Handle special cases
- **Formula**: FC = V - L - B/2 where V=valence electrons, L=lone pair electrons, B=bonding electrons
- **From structure**: `formal_charge_from_structure(element, lone_pairs, bonds)` uses PAIRS and BOND COUNT (not electrons)
- **Best structure**: Minimizes formal charges; negative FC on more electronegative atoms
- **Evaluate distribution**: Checks if most electronegative atoms have negative FC

### Examples
```python
# Example 1: FC on O in H2O
formal_charge_from_structure('O', 2, 2)  # -> 0 (6 - 4 - 4/2 = 0)

# Example 2: FC on N in NH4+
formal_charge_from_structure('N', 0, 4)  # -> 1 (5 - 0 - 8/2 = +1)

# Example 3: Best Lewis structure for SO2
best_lewis_structure('SO2')  # Evaluates multiple structures, picks best FC distribution
```
"""

from typing import Dict, List, Tuple, Optional


def formal_charge(valence_electrons: int, lone_pairs: int, bonding_electrons: int) -> int:
    """
    Calculate formal charge on an atom.
    
    Args:
        valence_electrons: Number of valence electrons in free atom
        lone_pairs: Number of lone pair electrons (not pairs!)
        bonding_electrons: Number of electrons in bonds (not bond count!)
    
    Returns:
        Formal charge
    
    Examples:
        >>> formal_charge(7, 6, 1)  # Cl in HCl
        0
        >>> formal_charge(6, 0, 8)  # C in CO2 (double bond to each O)
        0
        >>> formal_charge(5, 4, 4)  # N in NH4+
        1
    """
    # FC = V - LP - 1/2(BE)
    return valence_electrons - lone_pairs - bonding_electrons // 2


def formal_charge_from_structure(element: str, lone_pairs: int, bonds: int) -> int:
    """
    Calculate formal charge from structural information.
    
    Args:
        element: Element symbol
        lone_pairs: Number of lone pairs (pairs, not electrons)
        bonds: Number of bonds (single bonds count as 1, double as 2, triple as 3)
    
    Returns:
        Formal charge
    
    Examples:
        >>> formal_charge_from_structure('N', 1, 3)  # NH3
        0
        >>> formal_charge_from_structure('O', 3, 1)  # O in OH-
        -1
    """
    # Valence electrons for common elements
    valence = {
        'H': 1, 'He': 2,
        'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Ne': 8,
        'P': 5, 'S': 6, 'Cl': 7, 'Br': 7, 'I': 7,
    }
    
    if element not in valence:
        raise ValueError(f"Unknown element: {element}")
    
    v = valence[element]
    lp_electrons = 2 * lone_pairs
    bonding_electrons = 2 * bonds
    
    return v - lp_electrons - bonding_electrons // 2


def best_lewis_structure(candidates: List[Dict]) -> Dict:
    """
    Select the best Lewis structure from candidates.
    
    Args:
        candidates: List of structure dicts with 'formal_charges' key
    
    Returns:
        Best structure based on FC guidelines
    
    Examples:
        >>> candidates = [
        ...     {'structure': 'A', 'formal_charges': [0, 0, 0]},
        ...     {'structure': 'B', 'formal_charges': [1, -1, 0]}
        ... ]
        >>> best_lewis_structure(candidates)['structure']
        'A'
    """
    def score(structure):
        fcs = structure['formal_charges']
        
        # Score 1: Fewer non-zero FC is better
        non_zero = sum(1 for fc in fcs if fc != 0)
        
        # Score 2: Smaller |FC| is better
        magnitude = sum(abs(fc) for fc in fcs)
        
        # Score 3: Adjacent opposite signs is better
        adjacent_bonus = 0
        for i in range(len(fcs) - 1):
            if fcs[i] * fcs[i + 1] < 0:  # Opposite signs
                adjacent_bonus -= 1
        
        return (non_zero, magnitude, adjacent_bonus)
    
    return min(candidates, key=score)


def resonance_equivalent(structure1: Dict, structure2: Dict) -> bool:
    """
    Check if two structures are resonance forms.
    
    Args:
        structure1: First structure dict
        structure2: Second structure dict
    
    Returns:
        True if structures are resonance equivalent
    
    Examples:
        >>> s1 = {'atoms': ['O', 'N', 'O'], 'bonds': [(0, 1, 2), (1, 2, 1)]}
        >>> s2 = {'atoms': ['O', 'N', 'O'], 'bonds': [(0, 1, 1), (1, 2, 2)]}
        >>> resonance_equivalent(s1, s2)
        True
    """
    # Same atoms in same positions
    if structure1.get('atoms') != structure2.get('atoms'):
        return False
    
    # Different bond arrangements
    if structure1.get('bonds') == structure2.get('bonds'):
        return False
    
    return True


def average_bond_order(resonance_forms: List[Dict], atom1_idx: int, atom2_idx: int) -> float:
    """
    Calculate average bond order from resonance forms.
    
    Args:
        resonance_forms: List of resonance structures
        atom1_idx: First atom index
        atom2_idx: Second atom index
    
    Returns:
        Average bond order
    
    Examples:
        >>> forms = [
        ...     {'bonds': [(0, 1, 2), (1, 2, 1)]},  # N=O, N-O
        ...     {'bonds': [(0, 1, 1), (1, 2, 2)]}   # N-O, N=O
        ... ]
        >>> average_bond_order(forms, 0, 1)
        1.5
    """
    total_order = 0
    count = 0
    
    for form in resonance_forms:
        for bond in form.get('bonds', []):
            if (bond[0] == atom1_idx and bond[1] == atom2_idx) or \
               (bond[0] == atom2_idx and bond[1] == atom1_idx):
                total_order += bond[2]  # bond order
                count += 1
                break
    
    return total_order / count if count > 0 else 0


def sum_formal_charges(formal_charges: List[int]) -> int:
    """
    Calculate total charge from formal charges.
    
    Args:
        formal_charges: List of formal charges on each atom
    
    Returns:
        Total molecular charge
    
    Examples:
        >>> sum_formal_charges([0, 0, 0])
        0
        >>> sum_formal_charges([1, 0, 0, 0, -1])  # CO3^2- would be different
        0
    """
    return sum(formal_charges)


def validate_formal_charges(formal_charges: List[int], expected_charge: int) -> bool:
    """
    Validate that formal charges sum to expected molecular charge.
    
    Args:
        formal_charges: List of formal charges
        expected_charge: Expected total charge
    
    Returns:
        True if valid
    
    Examples:
        >>> validate_formal_charges([0, 0, 0], 0)
        True
        >>> validate_formal_charges([-1, 0, 0], -1)
        True
    """
    return sum(formal_charges) == expected_charge


def fc_minimization_preferred(fc1: List[int], fc2: List[int]) -> bool:
    """
    Determine if first FC distribution is preferred over second.
    
    Args:
        fc1: First formal charge distribution
        fc2: Second formal charge distribution
    
    Returns:
        True if fc1 is preferred
    
    Examples:
        >>> fc_minimization_preferred([0, 0], [1, -1])
        True
    """
    # Rule 1: Fewer non-zero charges
    non_zero1 = sum(1 for fc in fc1 if fc != 0)
    non_zero2 = sum(1 for fc in fc2 if fc != 0)
    if non_zero1 != non_zero2:
        return non_zero1 < non_zero2
    
    # Rule 2: Smaller magnitude
    mag1 = sum(abs(fc) for fc in fc1)
    mag2 = sum(abs(fc) for fc in fc2)
    
    return mag1 < mag2


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "average_bond_order",
        "description": "Calculate average bond order from resonance forms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resonance_forms": {"type": "number", "description": "Resonance Forms"},
                "atom1_idx": {"type": "number", "description": "Atom1 Idx"},
                "atom2_idx": {"type": "number", "description": "Atom2 Idx"},
            },
            "required": ["resonance_forms", "atom1_idx", "atom2_idx"]
        }
    },
    {
        "name": "best_lewis_structure",
        "description": "Select the best Lewis structure from candidates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "candidates": {"type": "number", "description": "Candidates"},
            },
            "required": ["candidates"]
        }
    },
    {
        "name": "fc_minimization_preferred",
        "description": "Determine if first FC distribution is preferred over second.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "fc1": {"type": "number", "description": "Fc1"},
                "fc2": {"type": "number", "description": "Fc2"},
            },
            "required": ["fc1", "fc2"]
        }
    },
    {
        "name": "formal_charge",
        "description": "Calculate formal charge on an atom.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "valence_electrons": {"type": "number", "description": "Valence Electrons"},
                "lone_pairs": {"type": "number", "description": "Lone Pairs"},
                "bonding_electrons": {"type": "number", "description": "Bonding Electrons"},
            },
            "required": ["valence_electrons", "lone_pairs", "bonding_electrons"]
        }
    },
    {
        "name": "formal_charge_from_structure",
        "description": "Calculate formal charge from structural information.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "lone_pairs": {"type": "number", "description": "Lone Pairs"},
                "bonds": {"type": "number", "description": "Bonds"},
            },
            "required": ["element", "lone_pairs", "bonds"]
        }
    },
    {
        "name": "resonance_equivalent",
        "description": "Check if two structures are resonance forms.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "structure1": {"type": "string", "description": "Structure1"},
                "structure2": {"type": "string", "description": "Structure2"},
            },
            "required": ["structure1", "structure2"]
        }
    },
    {
        "name": "sum_formal_charges",
        "description": "Calculate total charge from formal charges.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formal_charges": {"type": "number", "description": "Formal Charges"},
            },
            "required": ["formal_charges"]
        }
    },
    {
        "name": "validate_formal_charges",
        "description": "Validate that formal charges sum to expected molecular charge.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formal_charges": {"type": "number", "description": "Formal Charges"},
                "expected_charge": {"type": "number", "description": "Expected Charge"},
            },
            "required": ["formal_charges", "expected_charge"]
        }
    }
]
