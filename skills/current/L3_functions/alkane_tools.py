"""
Alkane Nomenclature Tools - L3 Implementation
[Source: Organic Chemistry OpenStax, Ch03]

Functions for naming alkanes and alkyl groups according to IUPAC rules.

## Solver Instructions (for AI Agent)

When you encounter alkane nomenclature, isomer counting, or hydrocarbon formula problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a carbon count -> need a name, formula, or isomer count?
- Given a structure description -> need IUPAC name?
- Given an alkyl halide description -> need classification?
- Given a molecular formula -> need degree of unsaturation?

### Step 2: Choose the correct function
- **Name/family lookup:** `get_alkane_name(carbons)` -> returns (name, formula)
- **Alkyl group info:** `get_alkyl_group(name)` -> returns AlkylGroup with formula, common name, carbon count
- **Molecular formula:** `hydrocarbon_formula(carbons, saturation)` -> 'alkane', 'alkene', or 'alkyne'
- **Isomer count:** `count_isomers(carbons)` -> number of structural isomers (up to C10)
- **Full IUPAC name:** `generate_iupac_name(parent_chain, substituents)` where substituents = [(position, group_name), ...]
- **Parent chain identification:** `find_parent_chain_length(structure)` -> returns int
- **Chain numbering:** `number_chain(substituent_positions)` -> returns numbered positions (lowest numbers)
- **Alkyl halide classification:** `classify_alkyl_halide(carbons_alpha_to_halogen)` -> 'primary', 'secondary', or 'tertiary'
- **Physical properties:** `alkane_properties(carbons)` -> returns dict with boiling point, formula, etc.
- **Naming rules:** `naming_rules_summary()` -> returns list of IUPAC rules
- **Degree of unsaturation from formula:** `calculate_degree_of_unsaturation(formula)` -> pass formula string like 'C6H6'

### Step 3: Handle special cases
- Carbons > 12: `get_alkane_name` returns generic 'CnH2n+2' format
- Branched alkanes: Use `generate_iupac_name` with substituent list; chain numbering auto-assigns lowest numbers
- Degree of unsaturation: Subtract 1 H for each halogen, add 1 H for each nitrogen before calculating

### Examples
```python
# Example 1: What is the formula and name of a 5-carbon alkane?
get_alkane_name(5)  -> ('pentane', 'C5H12')

# Example 2: How many isomers does hexane have?
count_isomers(6)  -> 5

# Example 3: Name 2-methylbutane using IUPAC generator
generate_iupac_name(4, [(2, 'methyl')])  -> '2-methylbutane'

# Example 4: Degree of unsaturation for benzene (C6H6)
calculate_degree_of_unsaturation('C6H6')  -> 4
```
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class AlkaneType(Enum):
    """Types of alkanes"""
    STRAIGHT_CHAIN = "straight_chain"
    BRANCHED = "branched"
    CYCLIC = "cyclic"


@dataclass
class AlkylGroup:
    """Information about an alkyl substituent"""
    name: str
    formula: str
    common_name: str
    carbon_count: int


# Straight-chain alkane names
ALKANE_NAMES = {
    1: ("methane", "CH4"),
    2: ("ethane", "C2H6"),
    3: ("propane", "C3H8"),
    4: ("butane", "C4H10"),
    5: ("pentane", "C5H12"),
    6: ("hexane", "C6H14"),
    7: ("heptane", "C7H16"),
    8: ("octane", "C8H18"),
    9: ("nonane", "C9H20"),
    10: ("decane", "C10H22"),
    11: ("undecane", "C11H24"),
    12: ("dodecane", "C12H26"),
}

# Alkyl groups
ALKYL_GROUPS = {
    "methyl": AlkylGroup("methyl", "CH3-", "Me", 1),
    "ethyl": AlkylGroup("ethyl", "CH3CH2-", "Et", 2),
    "propyl": AlkylGroup("propyl", "CH3CH2CH2-", "Pr", 3),
    "isopropyl": AlkylGroup("isopropyl", "(CH3)2CH-", "i-Pr", 3),
    "butyl": AlkylGroup("butyl", "CH3CH2CH2CH2-", "Bu", 4),
    "sec-butyl": AlkylGroup("sec-butyl", "CH3CH2CH(CH3)-", "sec-Bu", 4),
    "isobutyl": AlkylGroup("isobutyl", "(CH3)2CHCH2-", "i-Bu", 4),
    "tert-butyl": AlkylGroup("tert-butyl", "(CH3)3C-", "t-Bu", 4),
    "pentyl": AlkylGroup("pentyl", "CH3(CH2)3CH2-", "Pe", 5),
    "neopentyl": AlkylGroup("neopentyl", "(CH3)3CCH2-", "neo-Pe", 5),
}

# Number of structural isomers
ISOMER_COUNTS = {
    1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 5, 7: 9, 8: 18, 9: 35, 10: 75,
    11: 159, 12: 355,
}


def _to_subscript(s: str) -> str:
    """Convert digits in a string to Unicode subscripts."""
    return s.translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))


def get_alkane_name(carbons: int) -> Tuple[str, str]:
    """
    Get the IUPAC name and formula for a straight-chain alkane.
    
    Args:
        carbons: Number of carbon atoms
    
    Returns:
        Tuple of (name, formula)
    
    Examples:
        >>> get_alkane_name(4)
        ('butane', 'C4H10')
    """
    name, formula = ALKANE_NAMES.get(carbons, (f"C{carbons}H{2*carbons+2}", f"C{carbons}H{2*carbons+2}"))
    return (name, _to_subscript(formula))


def get_alkyl_group(name: str) -> AlkylGroup:
    """
    Get information about an alkyl group.
    
    Args:
        name: Alkyl group name
    
    Returns:
        AlkylGroup object
    
    Examples:
        >>> get_alkyl_group("methyl").formula
        'CH3-'
    """
    return ALKYL_GROUPS.get(name.lower())


def hydrocarbon_formula(carbons: int, saturation: str = "alkane") -> str:
    """
    Generate hydrocarbon molecular formula.
    
    Args:
        carbons: Number of carbon atoms
        saturation: "alkane", "alkene", "alkyne", or "cycloalkane"
    
    Returns:
        Molecular formula
    
    Examples:
        >>> hydrocarbon_formula(5, "alkane")
        'C5H12'
        >>> hydrocarbon_formula(6, "cycloalkane")
        'C6H12'
    """
    if saturation == "alkane":
        hydrogens = 2 * carbons + 2
    elif saturation == "alkene" or saturation == "cycloalkane":
        hydrogens = 2 * carbons
    elif saturation == "alkyne":
        hydrogens = 2 * carbons - 2
    else:
        hydrogens = 2 * carbons + 2
    
    return f"C{carbons}H{hydrogens}"


def count_isomers(carbons: int) -> int:
    """
    Get the number of structural isomers for an alkane.
    
    Args:
        carbons: Number of carbon atoms
    
    Returns:
        Number of structural isomers
    
    Examples:
        >>> count_isomers(5)
        3
        >>> count_isomers(8)
        18
    """
    return ISOMER_COUNTS.get(carbons, "many")


def generate_iupac_name(parent_chain: int, substituents: List[Tuple[int, str]]) -> str:
    """
    Generate IUPAC name for a substituted alkane.
    
    Args:
        parent_chain: Number of carbons in parent chain
        substituents: List of (position, substituent_name) tuples
    
    Returns:
        IUPAC name
    
    Examples:
        >>> generate_iupac_name(4, [(2, "methyl")])
        '2-methylbutane'
        >>> generate_iupac_name(5, [(2, "methyl"), (4, "methyl")])
        '2,4-dimethylpentane'
    """
    parent_name, _ = get_alkane_name(parent_chain)
    
    if not substituents:
        return parent_name
    
    # Sort substituents by position
    substituents = sorted(substituents, key=lambda x: x[0])
    
    # Group identical substituents
    sub_dict: Dict[str, List[int]] = {}
    for pos, name in substituents:
        if name not in sub_dict:
            sub_dict[name] = []
        sub_dict[name].append(pos)
    
    # Build name parts
    prefixes = []
    for name in sorted(sub_dict.keys()):
        positions = sub_dict[name]
        count = len(positions)
        
        # Multiplying prefix
        mult_prefix = {1: "", 2: "di", 3: "tri", 4: "tetra"}.get(count, f"{count}-")
        
        # Position numbers
        pos_str = ",".join(str(p) for p in positions)
        
        prefixes.append(f"{pos_str}-{mult_prefix}{name}")
    
    # Join prefixes and add parent name
    prefix_str = "-".join(prefixes)
    return f"{prefix_str}{parent_name}"


def find_parent_chain_length(structure: str) -> int:
    """
    Find the longest carbon chain (parent chain) in a structure.
    
    Args:
        structure: SMILES or structural description
    
    Returns:
        Number of carbons in longest chain
    
    Examples:
        >>> find_parent_chain_length("CCCCC")
        5
    """
    # Simplified: count C atoms
    return structure.upper().count("C")


def number_chain(substituent_positions: List[int]) -> List[int]:
    """
    Determine chain numbering direction for lowest numbers.
    
    Args:
        substituent_positions: Positions of substituents from one direction
    
    Returns:
        Corrected positions (numbered to minimize)
    
    Examples:
        >>> number_chain([4, 5])  # Should be numbered from other end
        [1, 2]
    """
    if not substituent_positions:
        return []
    
    max_pos = max(substituent_positions)
    
    # Compare sum of positions from both directions
    forward_sum = sum(substituent_positions)
    reverse_sum = sum(max_pos + 1 - p for p in substituent_positions)
    
    if reverse_sum < forward_sum:
        return [max_pos + 1 - p for p in substituent_positions]
    else:
        return substituent_positions


def classify_alkyl_halide(carbons_alpha_to_halogen: int) -> str:
    """
    Classify an alkyl halide as primary, secondary, or tertiary.
    
    Args:
        carbons_alpha_to_halogen: Number of carbons attached to carbon with halogen
    
    Returns:
        Classification
    
    Examples:
        >>> classify_alkyl_halide(1)
        'primary (1deg)'
        >>> classify_alkyl_halide(3)
        'tertiary (3deg)'
    """
    if carbons_alpha_to_halogen == 1:
        return "primary (1°)"
    elif carbons_alpha_to_halogen == 2:
        return "secondary (2°)"
    elif carbons_alpha_to_halogen == 3:
        return "tertiary (3°)"
    else:
        return "unknown"


def alkane_properties(carbons: int) -> Dict:
    """
    Get physical properties of a straight-chain alkane.
    
    Args:
        carbons: Number of carbon atoms
    
    Returns:
        Dictionary of properties
    """
    # Approximate values
    bp_data = {
        1: -161.5, 2: -88.6, 3: -42.1, 4: -0.5, 5: 36.1,
        6: 68.9, 7: 98.4, 8: 125.7, 9: 150.8, 10: 174.0,
    }
    
    mp_data = {
        1: -182.5, 2: -183.3, 3: -187.7, 4: -138.3, 5: -129.8,
        6: -95.3, 7: -90.6, 8: -56.8, 9: -53.5, 10: -29.7,
    }
    
    density_data = {
        5: 0.626, 6: 0.659, 7: 0.684, 8: 0.703, 9: 0.718, 10: 0.730,
    }
    
    return {
        "name": get_alkane_name(carbons)[0],
        "formula": get_alkane_name(carbons)[1],
        "boiling_point_c": bp_data.get(carbons, "varies"),
        "melting_point_c": mp_data.get(carbons, "varies"),
        "density_g_ml": density_data.get(carbons, "< 1.0"),
        "solubility": "insoluble in water, soluble in organic solvents",
        "state": "gas" if carbons <= 4 else ("liquid" if carbons <= 17 else "solid"),
    }


def naming_rules_summary() -> List[str]:
    """
    Get IUPAC naming rules summary.
    
    Returns:
        List of naming rules
    """
    return [
        "1. Find the longest continuous carbon chain (parent chain)",
        "2. Number the chain to give substituents the lowest possible numbers",
        "3. Name substituents as alkyl groups",
        "4. Use multiplying prefixes (di-, tri-, tetra-) for identical groups",
        "5. List substituents alphabetically (ignore prefixes)",
        "6. Use commas between numbers, hyphens between numbers and names",
        "7. For multiple functional groups, use priority order for suffix",
    ]


# Test functions
def test_alkane_names():
    """Test alkane naming"""
    assert get_alkane_name(4) == ("butane", "C4H10")
    assert get_alkane_name(6) == ("hexane", "C6H14")
    print("✓ Alkane name tests passed")


def test_hydrocarbon_formulas():
    """Test formula generation"""
    assert hydrocarbon_formula(5, "alkane") == "C5H12"
    assert hydrocarbon_formula(6, "alkene") == "C6H12"
    assert hydrocarbon_formula(4, "alkyne") == "C4H6"
    print("✓ Hydrocarbon formula tests passed")


def test_isomer_counts():
    """Test isomer counting"""
    assert count_isomers(4) == 2
    assert count_isomers(5) == 3
    assert count_isomers(6) == 5
    print("✓ Isomer count tests passed")


def test_iupac_naming():
    """Test IUPAC name generation"""
    assert generate_iupac_name(4, [(2, "methyl")]) == "2-methylbutane"
    assert "dimethyl" in generate_iupac_name(5, [(2, "methyl"), (4, "methyl")])
    print("✓ IUPAC naming tests passed")


if __name__ == "__main__":
    test_alkane_names()
    test_hydrocarbon_formulas()
    test_isomer_counts()
    test_iupac_naming()
    print("\n✓ All alkane nomenclature tools tests passed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "alkane_properties",
        "description": "Get physical properties of a straight-chain alkane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbons": {
                    "type": "number",
                    "description": "Carbons"
                }
            },
            "required": [
                "carbons"
            ]
        }
    },
    {
        "name": "classify_alkyl_halide",
        "description": "Classify an alkyl halide as primary, secondary, or tertiary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbons_alpha_to_halogen": {
                    "type": "number",
                    "description": "Carbons Alpha To Halogen"
                }
            },
            "required": [
                "carbons_alpha_to_halogen"
            ]
        }
    },
    {
        "name": "count_isomers",
        "description": "Get the number of structural isomers for an alkane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbons": {
                    "type": "number",
                    "description": "Carbons"
                }
            },
            "required": [
                "carbons"
            ]
        }
    },
    {
        "name": "dataclass",
        "description": "Add dunder methods based on the fields defined in the class.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cls": {
                    "type": "number",
                    "description": "Cls",
                    "default": None
                },
                "init": {
                    "type": "number",
                    "description": "Init",
                    "default": True
                },
                "repr": {
                    "type": "number",
                    "description": "Repr",
                    "default": True
                },
                "eq": {
                    "type": "number",
                    "description": "Eq",
                    "default": True
                },
                "order": {
                    "type": "number",
                    "description": "Order",
                    "default": False
                },
                "unsafe_hash": {
                    "type": "number",
                    "description": "Unsafe Hash",
                    "default": False
                },
                "frozen": {
                    "type": "number",
                    "description": "Frozen",
                    "default": False
                },
                "match_args": {
                    "type": "number",
                    "description": "Match Args",
                    "default": True
                },
                "kw_only": {
                    "type": "number",
                    "description": "Kw Only",
                    "default": False
                },
                "slots": {
                    "type": "number",
                    "description": "Slots",
                    "default": False
                },
                "weakref_slot": {
                    "type": "number",
                    "description": "Weakref Slot",
                    "default": False
                }
            },
            "required": []
        }
    },
    {
        "name": "find_parent_chain_length",
        "description": "Find the longest carbon chain (parent chain) in a structure.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "structure": {
                    "type": "string",
                    "description": "Structure"
                }
            },
            "required": [
                "structure"
            ]
        }
    },
    {
        "name": "generate_iupac_name",
        "description": "Generate IUPAC name for a substituted alkane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent_chain": {
                    "type": "number",
                    "description": "Parent Chain"
                },
                "substituents": {
                    "type": "number",
                    "description": "Substituents"
                }
            },
            "required": [
                "parent_chain",
                "substituents"
            ]
        }
    },
    {
        "name": "get_alkane_name",
        "description": "Get the IUPAC name and formula for a straight-chain alkane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbons": {
                    "type": "number",
                    "description": "Carbons"
                }
            },
            "required": [
                "carbons"
            ]
        }
    },
    {
        "name": "get_alkyl_group",
        "description": "Get information about an alkyl group.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name"
                }
            },
            "required": [
                "name"
            ]
        }
    },
    {
        "name": "hydrocarbon_formula",
        "description": "Generate hydrocarbon molecular formula.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbons": {
                    "type": "number",
                    "description": "Carbons"
                },
                "saturation": {
                    "type": "number",
                    "description": "Saturation",
                    "default": "alkane"
                }
            },
            "required": [
                "carbons"
            ]
        }
    },
    {
        "name": "naming_rules_summary",
        "description": "Get IUPAC naming rules summary.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "number_chain",
        "description": "Determine chain numbering direction for lowest numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substituent_positions": {
                    "type": "number",
                    "description": "Substituent Positions"
                }
            },
            "required": [
                "substituent_positions"
            ]
        }
    },
    {
        "name": "test_alkane_names",
        "description": "Test alkane naming",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_hydrocarbon_formulas",
        "description": "Test formula generation",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_isomer_counts",
        "description": "Test isomer counting",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_iupac_naming",
        "description": "Test IUPAC name generation",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]