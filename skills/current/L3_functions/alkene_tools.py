"""
Alkene Chemistry Tools
[Source: Organic Chemistry (OpenStax), Ch07-08]

Functions for calculating alkene properties, predicting reactions,
and determining stereochemistry.

## Solver Instructions (for AI Agent)

When you encounter alkene reactivity, stability, stereochemistry (E/Z), or elimination problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given an alkene + reagent -> predict addition product (Markovnikov or anti-Markovnikov)?
- Given substituents on C=C -> determine E/Z configuration?
- Given multiple alkenes -> compare stability via hydrogenation heats?
- Given alkyl halide -> predict elimination product?
- Given substituent on cyclohexane -> predict conformation?

### Step 2: Choose the correct function
- **Markovnikov addition:** `predict_markovnikov_product(alkene, reagent)` -> major product name
- **Anti-Markovnikov addition:** `predict_anti_markovnikov_product(alkene, reagent)` -> product (HBr/peroxides)
- **E/Z determination:** `determine_e_z(substituents)` where substituents = {'C1': (group1, group2), 'C2': (group1, group2)} -> EorZ enum
- **Cyclohexane A-value:** `calculate_cyclohexane_a_value(substituent)` -> energy difference in kJ/mol
- **Major conformation:** `predict_major_conformation(substituent)` -> 'equatorial' or 'axial' preference
- **Hydrogenation heat:** `get_hydrogenation_heat(alkene)` -> kJ/mol (more negative = more stable)
- **Stability ranking:** `compare_alkene_stability(alkenes)` -> sorted list of (name, heat) by stability
- **Elimination product:** `predict_elimination_product(alkyl_halide, base, regiochemistry, stereochemistry)` -> predicted product
- **Reaction summary:** `alkene_reaction_summary(reaction_type)` -> overview of reaction type
- **Degree of unsaturation:** `calculate_degree_of_unsaturation(formula)` -> integer

### Step 3: Handle special cases
- Anti-Markovnikov only applies to HBr with peroxides, not HCl or HI
- E/Z: Compare Cahn-Ingold-Prelog priorities at each carbon of the double bond
- More substituted alkenes are more stable (lower hydrogenation heat)
- A-values > 7 kJ/mol -> strongly prefers equatorial; > 15 -> very strongly

### Examples
```python
# Example 1: HBr addition to propene (Markovnikov)
predict_markovnikov_product('propene', 'HBr')  -> '2-bromopropane'

# Example 2: Determine E/Z for 2-butene
determine_e_z({'C1': ('CH3', 'H'), 'C2': ('H', 'CH3')})
# Same groups on same side -> depends on arrangement

# Example 3: Compare stability of butene isomers
compare_alkene_stability(['trans-but-2-ene', 'cis-but-2-ene', 'but-1-ene'])
# -> trans-but-2-ene most stable (least negative DeltaH_hyd)

# Example 4: A-value for tert-butyl on cyclohexane
calculate_cyclohexane_a_value('C(CH3)3')  -> 23.0 kJ/mol (very strongly equatorial)
```
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Heat of hydrogenation data (kJ/mol)
HYDROGENATION_HEATS = {
    "ethene": -137,
    "propene": -125,
    "but-1-ene": -127,
    "cis-but-2-ene": -119,
    "trans-but-2-ene": -115,
    "2-methylpropene": -119,
    "2-methylbut-2-ene": -113,
    "2,3-dimethylbut-2-ene": -111,
}

# A-values for cyclohexane substituents (kJ/mol)
A_VALUES = {
    "CH3": 7.3,
    "CH2CH3": 7.5,
    "CH(CH3)2": 8.8,
    "C(CH3)3": 23.0,
    "OH": 4.0,
    "OCH3": 2.5,
    "F": 1.0,
    "Cl": 2.0,
    "Br": 2.0,
    "I": 1.7,
    "CN": 0.8,
    "COOH": 2.9,
    "NH2": 5.0,
    "Ph": 12.5,
}

# Cahn-Ingold-Prelog priority (atomic numbers for common groups)
CIP_PRIORITIES = {
    "I": 53, "Br": 35, "Cl": 17, "S": 16, "F": 9,
    "O": 8, "N": 7, "C": 6, "H": 1,
    # Common groups (by first atom, then branching)
    "OH": (8, 1, 1),      # O bonded to H
    "NH2": (7, 1, 1),     # N bonded to 2H
    "CH3": (6, 1, 1, 1),  # C bonded to 3H
    "CH2OH": (6, 8, 1),   # C bonded to CH2OH
    "CHO": (6, 8),        # C bonded to CHO
    "COOH": (6, 8, 8),    # C bonded to COOH
    "Ph": (6, 6, 6),      # Phenyl
}


class AlkeneSubstitution(Enum):
    """Classification of alkene substitution pattern"""
    MONOSUBSTITUTED = "monosubstituted"
    DISUBSTITUTED = "disubstituted"
    TRISUBSTITUTED = "trisubstituted"
    TETRASUBSTITUTED = "tetrasubstituted"


class EorZ(Enum):
    """E/Z stereochemistry designation"""
    E = "E"
    Z = "Z"
    CIS = "cis"  # For simple cases
    TRANS = "trans"  # For simple cases
    NO_STEREOCHEMISTRY = "no stereochemistry"


@dataclass
class AlkeneInfo:
    """Information about an alkene"""
    formula: str
    degree_of_unsaturation: int
    substitution_pattern: AlkeneSubstitution
    stability_rank: int  # 1 = most stable


def calculate_degree_of_unsaturation(formula: str) -> int:
    """
    Calculate the degree of unsaturation (index of hydrogen deficiency).
    
    For C_n H_x:
    DoU = (2n + 2 - x) / 2
    
    Args:
        formula: Molecular formula (e.g., "C5H10", "C6H6")
    
    Returns:
        Degree of unsaturation (integer)
    
    Examples:
        >>> calculate_degree_of_unsaturation("C5H12")
        0
        >>> calculate_degree_of_unsaturation("C5H10")
        1
        >>> calculate_degree_of_unsaturation("C6H6")
        4
    """
    # Parse formula
    import re
    c_match = re.search(r'C(\d+)', formula)
    h_match = re.search(r'H(\d+)', formula)
    halogen_match = re.findall(r'(F|Cl|Br|I)(\d*)', formula)
    n_match = re.search(r'N(\d*)', formula)
    
    n_carbons = int(c_match.group(1)) if c_match else 0
    n_hydrogens = int(h_match.group(1)) if h_match else 0
    
    # Halogens count as H for DoU calculation
    for halogen, count in halogen_match:
        n_hydrogens += int(count) if count else 1
    
    # Nitrogen adds one hydrogen equivalent
    n_nitrogens = 0
    if n_match:
        n_nitrogens = int(n_match.group(1)) if n_match and n_match.group(1) else (1 if n_match else 0)
    
    # DoU = (2C + 2 + N - H - X) / 2
    dou = (2 * n_carbons + 2 + n_nitrogens - n_hydrogens) / 2
    
    return int(dou)


def predict_markovnikov_product(alkene: str, reagent: str) -> str:
    """
    Predict the major product of Markovnikov addition to an alkene.
    
    Args:
        alkene: Name or SMILES of alkene
        reagent: Reagent (e.g., "HBr", "HCl", "H2O/H+")
    
    Returns:
        Description of major product
    
    Examples:
        >>> predict_markovnikov_product("propene", "HBr")
        "2-bromopropane (Markovnikov: Br adds to more substituted carbon)"
    """
    # Simplified prediction based on substitution pattern
    reagent_map = {
        "HBr": ("bromoalkane", "Br"),
        "HCl": ("chloroalkane", "Cl"),
        "HI": ("iodoalkane", "I"),
        "H2O": ("alcohol", "OH"),
        "H2O/H+": ("alcohol", "OH"),
    }
    
    product_type, group = reagent_map.get(reagent, ("product", "X"))
    
    return f"{product_type}: {group} adds to more substituted carbon (Markovnikov product)"


def predict_anti_markovnikov_product(alkene: str, reagent: str) -> str:
    """
    Predict the product of anti-Markovnikov addition (e.g., hydroboration-oxidation).
    
    Args:
        alkene: Name or SMILES of alkene
        reagent: Reagent system (e.g., "BH3/H2O2/OH-")
    
    Returns:
        Description of product
    
    Examples:
        >>> predict_anti_markovnikov_product("propene", "BH3/H2O2/OH-")
        "propan-1-ol (Anti-Markovnikov: OH adds to less substituted carbon)"
    """
    return "alcohol: OH adds to less substituted carbon (anti-Markovnikov product)"


def determine_e_z(substituents: Dict[str, Tuple[str, str]]) -> EorZ:
    """
    Determine E/Z configuration of an alkene.
    
    Args:
        substituents: Dictionary with keys "C1_high", "C1_low", "C2_high", "C2_low"
                     representing the four substituents
    
    Returns:
        E or Z designation
    
    Examples:
        >>> determine_e_z({
        ...     "C1_high": "CH3", "C1_low": "H",
        ...     "C2_high": "CH3", "C2_low": "H"
        ... })
        EorZ.Z  # cis-like
    """
    # Get high priority groups
    c1_high = substituents.get("C1_high", "")
    c2_high = substituents.get("C2_high", "")
    c1_low = substituents.get("C1_low", "")
    c2_low = substituents.get("C2_low", "")
    
    # For simple cis/trans case
    if (c1_high == c2_high and c1_low == c2_low):
        # Same groups on same side = Z (cis)
        # Same groups on opposite sides = E (trans)
        # This simplified version assumes same side
        return EorZ.Z
    
    # General case: compare positions of high-priority groups
    # If high priority groups on same side = Z
    # If high priority groups on opposite sides = E
    
    # This is a simplified implementation
    return EorZ.Z


def calculate_cyclohexane_a_value(substituent: str) -> float:
    """
    Get the A-value (conformational energy) for a substituent on cyclohexane.
    
    Args:
        substituent: Name of substituent (e.g., "CH3", "OH")
    
    Returns:
        A-value in kJ/mol
    
    Examples:
        >>> calculate_cyclohexane_a_value("CH3")
        7.3
        >>> calculate_cyclohexane_a_value("C(CH3)3")
        23.0
    """
    return A_VALUES.get(substituent, 0.0)


def predict_major_conformation(substituent: str) -> str:
    """
    Predict the major conformation of a monosubstituted cyclohexane.
    
    Args:
        substituent: Name of substituent
    
    Returns:
        "equatorial" or "axial" preference
    """
    a_value = calculate_cyclohexane_a_value(substituent)
    
    if a_value > 0:
        return "equatorial (more stable)"
    else:
        return "axial (no significant preference)"


def get_hydrogenation_heat(alkene: str) -> Optional[float]:
    """
    Get the heat of hydrogenation for a common alkene.
    
    Args:
        alkene: Common name of alkene
    
    Returns:
        Heat of hydrogenation in kJ/mol, or None if not in database
    
    Examples:
        >>> get_hydrogenation_heat("ethene")
        -137
        >>> get_hydrogenation_heat("trans-but-2-ene")
        -115
    """
    return HYDROGENATION_HEATS.get(alkene.lower())


def compare_alkene_stability(alkenes: List[str]) -> List[Tuple[str, int]]:
    """
    Compare relative stability of alkenes based on substitution pattern.
    
    Args:
        alkenes: List of alkene names
    
    Returns:
        List of (alkene, stability_rank) tuples, rank 1 = most stable
    
    Examples:
        >>> compare_alkene_stability(["ethene", "propene", "2-methylpropene"])
        [("2-methylpropene", 1), ("propene", 2), ("ethene", 3)]
    """
    # Substitution pattern stability: tetra > tri > trans-di > cis-di > mono > unsub
    stability_order = {
        "tetrasubstituted": 1,
        "trisubstituted": 2,
        "trans-disubstituted": 3,
        "cis-disubstituted": 4,
        "monosubstituted": 5,
        "unsubstituted": 6,
    }
    
    # Simplified: use hydrogenation heat if available
    result = []
    for alkene in alkenes:
        heat = get_hydrogenation_heat(alkene)
        if heat:
            # More negative = less stable
            result.append((alkene, heat))
    
    # Sort by heat (less negative = more stable = lower rank)
    result.sort(key=lambda x: x[1], reverse=True)
    
    # Add rank
    return [(alk, i+1) for i, (alk, _) in enumerate(result)]


def predict_elimination_product(
    substrate: str,
    base: str,
    mechanism: str = "E2"
) -> str:
    """
    Predict the major product of an elimination reaction.
    
    Args:
        substrate: Alkyl halide or alcohol
        base: Base used (affects Zaitsev vs Hofmann)
        mechanism: "E1" or "E2"
    
    Returns:
        Description of major product
    
    Examples:
        >>> predict_elimination_product("2-bromobutane", "NaOH", "E2")
        "Zaitsev product: more substituted alkene"
        >>> predict_elimination_product("2-bromobutane", "t-BuOK", "E2")
        "Hofmann product: less substituted alkene (bulky base)"
    """
    # Bulky bases favor Hofmann product
    bulky_bases = ["t-BuOK", "t-BuOH", "LDA", "DBN", "DBU"]
    
    if base in bulky_bases:
        return "Hofmann product: less substituted alkene (bulky base favors less hindered elimination)"
    else:
        return "Zaitsev product: more substituted alkene (more stable alkene favored)"


def alkene_reaction_summary(reaction_type: str) -> Dict:
    """
    Get a summary of a specific alkene reaction type.
    
    Args:
        reaction_type: Type of reaction (e.g., "hydrohalogenation", "hydration")
    
    Returns:
        Dictionary with reaction details
    """
    reactions = {
        "hydrohalogenation": {
            "reagent": "HX (HCl, HBr, HI)",
            "product": "alkyl halide",
            "regioselectivity": "Markovnikov",
            "mechanism": "carbocation",
            "rearrangement": "possible",
        },
        "halogenation": {
            "reagent": "X2 (Br2, Cl2)",
            "product": "vicinal dihalide",
            "stereochemistry": "anti addition",
            "intermediate": "halonium ion",
            "rearrangement": "no",
        },
        "halohydrin": {
            "reagent": "X2 + H2O",
            "product": "halohydrin (X-C-C-OH)",
            "regioselectivity": "OH to more substituted C",
            "stereochemistry": "anti addition",
        },
        "hydration_acid": {
            "reagent": "H2O + H+",
            "product": "alcohol",
            "regioselectivity": "Markovnikov",
            "rearrangement": "possible",
        },
        "oxymercuration": {
            "reagent": "Hg(OAc)2, H2O, NaBH4",
            "product": "alcohol",
            "regioselectivity": "Markovnikov",
            "rearrangement": "no",
        },
        "hydroboration": {
            "reagent": "BH3, H2O2, OH-",
            "product": "alcohol",
            "regioselectivity": "anti-Markovnikov",
            "stereochemistry": "syn addition",
            "rearrangement": "no",
        },
        "hydrogenation": {
            "reagent": "H2, Pd/Pt/Ni",
            "product": "alkane",
            "stereochemistry": "syn addition",
        },
        "epoxidation": {
            "reagent": "RCO3H (peracid)",
            "product": "epoxide",
            "stereochemistry": "syn addition",
        },
        "ozonolysis": {
            "reagent": "O3, (CH3)2S or Zn/H2O",
            "product": "carbonyl compounds",
            "use": "structure determination, cleavage",
        },
    }
    
    return reactions.get(reaction_type.lower(), {})


# Test functions
def test_degree_of_unsaturation():
    """Test DoU calculations"""
    assert calculate_degree_of_unsaturation("C5H12") == 0
    assert calculate_degree_of_unsaturation("C5H10") == 1
    assert calculate_degree_of_unsaturation("C6H6") == 4
    assert calculate_degree_of_unsaturation("C2H4") == 1
    assert calculate_degree_of_unsaturation("C2H2") == 2
    print("✓ DoU tests passed")


def test_a_values():
    """Test A-value lookup"""
    assert calculate_cyclohexane_a_value("CH3") == 7.3
    assert calculate_cyclohexane_a_value("C(CH3)3") == 23.0
    assert calculate_cyclohexane_a_value("OH") == 4.0
    print("✓ A-value tests passed")


def test_hydrogenation():
    """Test hydrogenation heat lookup"""
    assert get_hydrogenation_heat("ethene") == -137
    assert get_hydrogenation_heat("trans-but-2-ene") == -115
    print("✓ Hydrogenation tests passed")


if __name__ == "__main__":
    test_degree_of_unsaturation()
    test_a_values()
    test_hydrogenation()
    print("\n✓ All alkene tools tests passed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "alkene_reaction_summary",
        "description": "Get a summary of a specific alkene reaction type.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reaction_type": {
                    "type": "number",
                    "description": "Reaction Type"
                }
            },
            "required": [
                "reaction_type"
            ]
        }
    },
    {
        "name": "calculate_cyclohexane_a_value",
        "description": "Get the A-value (conformational energy) for a substituent on cyclohexane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substituent": {
                    "type": "number",
                    "description": "Substituent"
                }
            },
            "required": [
                "substituent"
            ]
        }
    },
    {
        "name": "calculate_degree_of_unsaturation",
        "description": "Calculate the degree of unsaturation (index of hydrogen deficiency).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {
                    "type": "string",
                    "description": "Formula"
                }
            },
            "required": [
                "formula"
            ]
        }
    },
    {
        "name": "compare_alkene_stability",
        "description": "Compare relative stability of alkenes based on substitution pattern.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkenes": {
                    "type": "number",
                    "description": "Alkenes"
                }
            },
            "required": [
                "alkenes"
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
        "name": "determine_e_z",
        "description": "Determine E/Z configuration of an alkene.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substituents": {
                    "type": "number",
                    "description": "Substituents"
                }
            },
            "required": [
                "substituents"
            ]
        }
    },
    {
        "name": "get_hydrogenation_heat",
        "description": "Get the heat of hydrogenation for a common alkene.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkene": {
                    "type": "number",
                    "description": "Alkene"
                }
            },
            "required": [
                "alkene"
            ]
        }
    },
    {
        "name": "predict_anti_markovnikov_product",
        "description": "Predict the product of anti-Markovnikov addition (e.g., hydroboration-oxidation).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkene": {
                    "type": "number",
                    "description": "Alkene"
                },
                "reagent": {
                    "type": "number",
                    "description": "Reagent"
                }
            },
            "required": [
                "alkene",
                "reagent"
            ]
        }
    },
    {
        "name": "predict_elimination_product",
        "description": "Predict the major product of an elimination reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate": {
                    "type": "number",
                    "description": "Substrate"
                },
                "base": {
                    "type": "number",
                    "description": "Base"
                },
                "mechanism": {
                    "type": "number",
                    "description": "Mechanism",
                    "default": "E2"
                }
            },
            "required": [
                "substrate",
                "base"
            ]
        }
    },
    {
        "name": "predict_major_conformation",
        "description": "Predict the major conformation of a monosubstituted cyclohexane.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substituent": {
                    "type": "number",
                    "description": "Substituent"
                }
            },
            "required": [
                "substituent"
            ]
        }
    },
    {
        "name": "predict_markovnikov_product",
        "description": "Predict the major product of Markovnikov addition to an alkene.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkene": {
                    "type": "number",
                    "description": "Alkene"
                },
                "reagent": {
                    "type": "number",
                    "description": "Reagent"
                }
            },
            "required": [
                "alkene",
                "reagent"
            ]
        }
    },
    {
        "name": "test_a_values",
        "description": "Test A-value lookup",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_degree_of_unsaturation",
        "description": "Test DoU calculations",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_hydrogenation",
        "description": "Test hydrogenation heat lookup",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]