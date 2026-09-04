# -*- coding: utf-8 -*-
"""
Alkyne Chemistry Tools - L3 Implementation

Functions for alkyne nomenclature, properties, reactivity predictions,
and synthesis route planning.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class AlkyneType(Enum):
    """Types of alkynes"""
    TERMINAL = "terminal"  # R-C(triple bond)C-H
    INTERNAL = "internal"  # R-C(triple bond)C-R'
    SYMMETRICAL = "symmetrical"  # R-C(triple bond)C-R


@dataclass
class AlkyneReaction:
    """Information about an alkyne reaction"""
    name: str
    reagents: List[str]
    product: str
    stereochemistry: str
    notes: str


# Common alkyne names
COMMON_ALKYNE_NAMES = {
    "ethyne": ("C2H2", "acetylene"),
    "propyne": ("C3H4", "methylacetylene"),
    "but-1-yne": ("C4H6", "ethylacetylene"),
    "but-2-yne": ("C4H6", "dimethylacetylene"),
}

# Alkyne reactions
ALKYNE_REACTIONS = {
    "complete_hydrogenation": AlkyneReaction(
        name="Complete Hydrogenation",
        reagents=["H2", "Pd/C or Pt"],
        product="Alkane",
        stereochemistry="syn addition",
        notes="2 equivalents of H2"
    ),
    "partial_hydrogenation_lindlar": AlkyneReaction(
        name="Partial Hydrogenation (Lindlar)",
        reagents=["H2", "Lindlar's Pd (Pd/CaCO3, quinoline)"],
        product="cis-Alkene",
        stereochemistry="syn addition",
        notes="Stops at alkene, gives cis product"
    ),
    "partial_hydrogenation_na": AlkyneReaction(
        name="Partial Hydrogenation (Na/NH3)",
        reagents=["Na", "NH3(l)"],
        product="trans-Alkene",
        stereochemistry="anti addition",
        notes="Dissolving metal reduction, gives trans product"
    ),
    "hydrohalogenation": AlkyneReaction(
        name="Hydrohalogenation",
        reagents=["HX (HCl, HBr, HI)"],
        product="Vinyl halide -> Geminal dihalide",
        stereochemistry="Markovnikov",
        notes="Can add 1 or 2 equivalents"
    ),
    "halogenation": AlkyneReaction(
        name="Halogenation",
        reagents=["X2 (Br2, Cl2)"],
        product="Tetrahalide",
        stereochemistry="anti addition",
        notes="Can add 1 or 2 equivalents"
    ),
    "hydration_hg": AlkyneReaction(
        name="Hydration (Hg2+-catalyzed)",
        reagents=["H2O", "HgSO4", "H2SO4"],
        product="Ketone",
        stereochemistry="Markovnikov",
        notes="Terminal alkynes -> methyl ketones"
    ),
    "hydroboration": AlkyneReaction(
        name="Hydroboration-Oxidation",
        reagents=["BH3", "H2O2", "OH-"],
        product="Aldehyde (terminal)",
        stereochemistry="Anti-Markovnikov",
        notes="Terminal alkynes -> aldehydes"
    ),
}

# Acidity of terminal alkynes
ACIDITY_DATA = {
    "terminal_alkyne": {"pKa": 25, "acidic_proton": True},
    "ammonia": {"pKa": 38, "acidic_proton": False},
    "alcohol": {"pKa": 16, "acidic_proton": True},
    "water": {"pKa": 15.7, "acidic_proton": True},
}


def classify_alkyne(structure: str) -> AlkyneType:
    """
    Classify an alkyne as terminal or internal.
    
    Args:
        structure: Alkyne structure description
    
    Returns:
        Alkyne type
    
    Examples:
        >>> classify_alkyne("HC(triple bond)C-CH3")
        AlkyneType.TERMINAL
        >>> classify_alkyne("CH3-C(triple bond)C-CH3")
        AlkyneType.INTERNAL
    """
    structure = structure.lower()
    
    if "hc" in structure and "c" in structure:
        return AlkyneType.TERMINAL
    elif "c" in structure:
        return AlkyneType.INTERNAL
    else:
        return AlkyneType.TERMINAL


def get_alkyne_formula(carbons: int) -> str:
    """
    Get the molecular formula for a straight-chain alkyne.
    
    Formula: CnH2n-2
    
    Args:
        carbons: Number of carbon atoms
    
    Returns:
        Molecular formula
    
    Examples:
        >>> get_alkyne_formula(4)
        'C4H6'
    """
    hydrogens = 2 * carbons - 2
    return f"C{carbons}H{hydrogens}"


def is_terminal_alkyne(structure: str) -> bool:
    """
    Check if an alkyne is terminal (has acidic proton).
    
    Args:
        structure: Alkyne structure
    
    Returns:
        True if terminal alkyne
    
    Examples:
        >>> is_terminal_alkyne("HC(triple bond)C-CH3")
        True
        >>> is_terminal_alkyne("CH3-C(triple bond)C-CH3")
        False
    """
    return classify_alkyne(structure) == AlkyneType.TERMINAL


def can_form_acetylide(structure: str) -> bool:
    """
    Check if an alkyne can form an acetylide anion.
    
    Terminal alkynes can be deprotonated by strong bases.
    
    Args:
        structure: Alkyne structure
    
    Returns:
        True if can form acetylide
    
    Examples:
        >>> can_form_acetylide("HC(triple bond)C-CH3")
        True
    """
    return is_terminal_alkyne(structure)


def suitable_base_for_deprotonation() -> Dict[str, str]:
    """
    Get bases suitable for deprotonating terminal alkynes.
    
    Returns:
        Dictionary of suitable bases and their properties
    """
    return {
        "NaNH2": "Sodium amide, very strong base, common choice",
        "NaH": "Sodium hydride, strong base, generates H2",
        "n-BuLi": "n-Butyllithium, very strong base",
        "LDA": "Lithium diisopropylamide, strong bulky base",
    }


def predict_partial_hydrogenation_product(catalyst: str) -> Tuple[str, str]:
    """
    Predict the product of partial hydrogenation.
    
    Args:
        catalyst: Catalyst system used
    
    Returns:
        Tuple of (alkene_type, stereochemistry)
    
    Examples:
        >>> predict_partial_hydrogenation_product("Lindlar")
        ('cis-alkene', 'syn addition')
        >>> predict_partial_hydrogenation_product("Na/NH3")
        ('trans-alkene', 'anti addition')
    """
    if catalyst.lower() == "lindlar" or "pd" in catalyst.lower():
        return ("cis-alkene", "syn addition")
    elif "na" in catalyst.lower() or "nh3" in catalyst.lower():
        return ("trans-alkene", "anti addition")
    else:
        return ("alkene", "variable")


def predict_hydration_product(alkyne_type: AlkyneType, method: str) -> str:
    """
    Predict the product of alkyne hydration.
    
    Args:
        alkyne_type: Type of alkyne
        method: "mercury" or "hydroboration"
    
    Returns:
        Product description
    
    Examples:
        >>> predict_hydration_product(AlkyneType.TERMINAL, "mercury")
        'methyl ketone'
        >>> predict_hydration_product(AlkyneType.TERMINAL, "hydroboration")
        'aldehyde'
    """
    if method.lower() == "mercury" or method.lower() == "hg":
        if alkyne_type == AlkyneType.TERMINAL:
            return "methyl ketone (Markovnikov addition)"
        else:
            return "ketone"
    elif method.lower() == "hydroboration" or "bh3" in method.lower():
        if alkyne_type == AlkyneType.TERMINAL:
            return "aldehyde (Anti-Markovnikov)"
        else:
            return "ketone"
    else:
        return "ketone or aldehyde"


def alkylation_with_acetylide(acetylide: str, alkyl_halide: str) -> str:
    """
    Predict the product of acetylide alkylation.
    
    R-C(triple bond)C:- + R'-X -> R-C(triple bond)C-R'
    
    Args:
        acetylide: Acetylide anion
        alkyl_halide: Alkyl halide
    
    Returns:
        Product description
    
    Examples:
        >>> alkylation_with_acetylide("HC(triple bond)C-Na+", "CH3I")
        'propyne (extended chain)'
    """
    return f"Extended alkyne (new C-C bond formed via SN2)"


def suitable_alkyl_halides_for_alkylation() -> List[str]:
    """
    Get alkyl halides suitable for acetylide alkylation.
    
    Only primary and methyl halides work well (SN2 mechanism).
    
    Returns:
        List of suitable alkyl halides
    """
    return [
        "Methyl halides (CH3I, CH3Br)",
        "Primary alkyl halides (RCH2X)",
        "NOT: Secondary alkyl halides (elimination competes)",
        "NOT: Tertiary alkyl halides (elimination dominates)",
    ]


def synthesis_from_vicinal_dihalide() -> List[str]:
    """
    Get steps for alkyne synthesis from vicinal dihalide.
    
    Returns:
        List of synthetic steps
    """
    return [
        "1. Start with alkene",
        "2. Add Br2 -> vicinal dibromide",
        "3. First elimination: vicinal dibromide + NaNH2 -> vinyl bromide",
        "4. Second elimination: vinyl bromide + NaNH2 -> alkyne",
        "Note: Excess NaNH2 required for terminal alkynes (deprotonation)",
    ]


def compare_triple_bond_properties() -> Dict[str, Tuple]:
    """
    Compare properties of single, double, and triple bonds.
    
    Returns:
        Dictionary of bond properties
    """
    return {
        "C-C": (154, 347, "tetrahedral", "sp3"),
        "C=C": (134, 611, "trigonal planar", "sp2"),
        "C(triple bond)C": (120, 839, "linear", "sp"),
    }


def alkyne_naming_rules() -> List[str]:
    """
    Get IUPAC naming rules for alkynes.
    
    Returns:
        List of naming rules
    """
    return [
        "1. Find longest chain containing the triple bond",
        "2. Number from end nearest the triple bond",
        "3. Use suffix '-yne'",
        "4. For multiple triple bonds: -diyne, -triyne",
        "5. For both double and triple bonds: -enyne",
        "6. Number to give lowest possible number to multiple bonds",
        "7. If tie, double bond gets lower number",
    ]


def alkyne_reaction_summary() -> Dict:
    """
    Get summary of major alkyne reactions.
    
    Returns:
        Dictionary of reaction summaries
    """
    return {name: {
        "reagents": rxn.reagents,
        "product": rxn.product,
        "stereochemistry": rxn.stereochemistry,
        "notes": rxn.notes
    } for name, rxn in ALKYNE_REACTIONS.items()}


# Test functions
def test_alkyne_classification():
    """Test alkyne classification"""
    assert classify_alkyne("HC(triple bond)C-CH3") == AlkyneType.TERMINAL
    assert classify_alkyne("CH3-C(triple bond)C-CH3") == AlkyneType.INTERNAL
    print("[OK] Alkyne classification tests passed")


def test_formulas():
    """Test formula generation"""
    assert get_alkyne_formula(4) == "C4H6"
    assert get_alkyne_formula(2) == "C2H2"
    print("[OK] Formula tests passed")


def test_partial_hydrogenation():
    """Test partial hydrogenation prediction"""
    product, stereo = predict_partial_hydrogenation_product("Lindlar")
    assert "cis" in product
    product, stereo = predict_partial_hydrogenation_product("Na/NH3")
    assert "trans" in product
    print("[OK] Partial hydrogenation tests passed")


def test_hydration():
    """Test hydration prediction"""
    product = predict_hydration_product(AlkyneType.TERMINAL, "mercury")
    assert "ketone" in product
    product = predict_hydration_product(AlkyneType.TERMINAL, "hydroboration")
    assert "aldehyde" in product
    print("[OK] Hydration prediction tests passed")


if __name__ == "__main__":
    test_alkyne_classification()
    test_formulas()
    test_partial_hydrogenation()
    test_hydration()
    print("\n[OK] All alkyne chemistry tools tests passed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "alkylation_with_acetylide",
        "description": "Predict the product of acetylide alkylation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "acetylide": {
                    "type": "string",
                    "description": "Acetylide"
                },
                "alkyl_halide": {
                    "type": "string",
                    "description": "Alkyl Halide"
                }
            },
            "required": [
                "acetylide",
                "alkyl_halide"
            ]
        }
    },
    {
        "name": "alkyne_naming_rules",
        "description": "Get IUPAC naming rules for alkynes.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "alkyne_reaction_summary",
        "description": "Get summary of major alkyne reactions.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "can_form_acetylide",
        "description": "Check if an alkyne can form an acetylide anion.",
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
        "name": "classify_alkyne",
        "description": "Classify an alkyne as terminal or internal.",
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
        "name": "compare_triple_bond_properties",
        "description": "Compare properties of single, double, and triple bonds.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_alkyne_formula",
        "description": "Get the molecular formula for a straight-chain alkyne.",
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
        "name": "is_terminal_alkyne",
        "description": "Check if an alkyne is terminal (has acidic proton).",
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
        "name": "predict_hydration_product",
        "description": "Predict the product of alkyne hydration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkyne_type": {
                    "type": "string",
                    "description": "Alkyne Type"
                },
                "method": {
                    "type": "string",
                    "description": "Method"
                }
            },
            "required": [
                "alkyne_type",
                "method"
            ]
        }
    },
    {
        "name": "predict_partial_hydrogenation_product",
        "description": "Predict the product of partial hydrogenation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "catalyst": {
                    "type": "string",
                    "description": "Catalyst"
                }
            },
            "required": [
                "catalyst"
            ]
        }
    },
    {
        "name": "suitable_alkyl_halides_for_alkylation",
        "description": "Get alkyl halides suitable for acetylide alkylation.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "suitable_base_for_deprotonation",
        "description": "Get bases suitable for deprotonating terminal alkynes.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "synthesis_from_vicinal_dihalide",
        "description": "Get steps for alkyne synthesis from vicinal dihalide.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_alkyne_classification",
        "description": "Test alkyne classification",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_formulas",
        "description": "Test formula generation",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_hydration",
        "description": "Test hydration prediction",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_partial_hydrogenation",
        "description": "Test partial hydrogenation prediction",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]
