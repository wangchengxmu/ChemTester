"""
Functional Group Tools - L3 Implementation
[Source: Organic Chemistry OpenStax, Ch03]

Functions for identifying, classifying, and analyzing organic functional groups.

## Solver Instructions (for AI Agent)

When you encounter functional group identification, naming priority, boiling point prediction, solubility, or electron effect questions, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a molecule (SMILES/formula) -> identify all functional groups?
- Given multiple functional groups -> determine naming priority (suffix vs prefix)?
- Given functional groups -> predict boiling point trend or solubility?
- Given a group name -> get IUPAC suffix, prefix, or electron effect?

### Step 2: Choose the correct function
- **Identify functional groups:** `identify_functional_groups(smiles_or_formula)` -> list of group names from SMILES or formula string
- **Naming priority:** `get_naming_priority(group_name)` -> integer (higher = gets suffix). In this bounded implementation, the IUPAC P-41 seniority order for ordinary acyclic characteristic groups is carboxylic_acid > anhydride > ester > acyl_halide > amide > nitrile > aldehyde > ketone > alcohol (hydroxy) > amine. This is not a full cyclic-parent nomenclature engine.
- **Principal group:** `determine_principal_group(groups)` -> highest priority group (gets the suffix)
- **IUPAC suffix:** `get_suffix(group_name)` -> 'ane', 'ene', 'ol', 'al', 'one', 'oic acid', 'oate', 'amide', etc.
- **IUPAC prefix:** `get_prefix(group_name)` -> 'hydroxy', 'oxo', 'formyl', 'amino', 'nitro', 'cyano', 'alkoxy', etc.
- **Electron effect:** `classify_electron_effect(group_name)` -> 'withdrawing'/'donating'/'neutral'. EWG: nitro, nitrile, COOH, aldehyde, ketone, ester, amide. EDG: alcohol, ether, amine, thiol, sulfide
- **Boiling point trend:** `predict_boiling_point_trend(groups)` -> text description based on H-bonding and dipole-dipole
- **Solubility prediction:** `predict_solubility(groups, carbons)` -> water solubility description. More carbons -> less soluble
- **Full summary table:** `functional_group_summary()` -> dict of all groups with structure, suffix, prefix, priority, electron effect

### Step 3: Handle special cases
- P-41 characteristic-group seniority is represented locally as 10 through 1 in the order documented above; unsupported group names raise `ValueError`.
- Reference: IUPAC Blue Book P-41, https://iupac.qmul.ac.uk/BlueBook/P4.html
- Carboxylic acids form dimers -> highest boiling point
- Molecules with ≤4 carbons and H-bonding groups are typically water-soluble
- Alkane is the default if no other groups are identified

### Examples
```python
# Example 1: Identify groups in ethanol
identify_functional_groups('CH3CH2OH')  -> ['alkane', 'alcohol']

# Example 2: Principal group in a molecule with alcohol and alkene
determine_principal_group(['alcohol', 'alkene'])  -> 'alcohol' (priority 10 > 2)

# Example 3: Electron effect of nitro group
classify_electron_effect('nitro')  -> 'withdrawing'

# Example 4: Will a 6-carbon carboxylic acid be water soluble?
predict_solubility(['carboxylic_acid'], 6)  -> 'Moderately water soluble'
```
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class FunctionalGroupType(Enum):
    """Classification of functional group types"""
    HYDROCARBON = "hydrocarbon"
    OXYGEN_CONTAINING = "oxygen_containing"
    NITROGEN_CONTAINING = "nitrogen_containing"
    HALOGEN_CONTAINING = "halogen_containing"
    SULFUR_CONTAINING = "sulfur_containing"


@dataclass
class FunctionalGroup:
    """Information about a functional group"""
    name: str
    structure: str
    suffix: str
    prefix: Optional[str]
    group_type: FunctionalGroupType
    priority: int  # Local P-41 ordinal; 0 means outside this characteristic-group scope
    electron_effect: str  # "withdrawing", "donating", or "neutral"


# Functional group database. P-41 characteristic-group seniority is intentionally
# limited to ordinary acyclic groups; this is not a complete parent-selection engine.
FUNCTIONAL_GROUPS = {
    # Hydrocarbons
    "alkane": FunctionalGroup(
        name="alkane", structure="C-C", suffix="ane", prefix=None,
        group_type=FunctionalGroupType.HYDROCARBON, priority=0, electron_effect="neutral"
    ),
    "alkene": FunctionalGroup(
        name="alkene", structure="C=C", suffix="ene", prefix=None,
        group_type=FunctionalGroupType.HYDROCARBON, priority=0, electron_effect="neutral"
    ),
    "alkyne": FunctionalGroup(
        name="alkyne", structure="C≡C", suffix="yne", prefix=None,
        group_type=FunctionalGroupType.HYDROCARBON, priority=0, electron_effect="neutral"
    ),
    "aromatic": FunctionalGroup(
        name="aromatic", structure="benzene ring", suffix="benzene", prefix="phenyl",
        group_type=FunctionalGroupType.HYDROCARBON, priority=0, electron_effect="neutral"
    ),
    
    # Oxygen-containing
    "alcohol": FunctionalGroup(
        name="alcohol", structure="R-OH", suffix="ol", prefix="hydroxy",
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=2, electron_effect="donating"
    ),
    "ether": FunctionalGroup(
        name="ether", structure="R-O-R'", suffix="ether", prefix="alkoxy",
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=0, electron_effect="donating"
    ),
    "aldehyde": FunctionalGroup(
        name="aldehyde", structure="R-CHO", suffix="al", prefix="formyl",
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=4, electron_effect="withdrawing"
    ),
    "ketone": FunctionalGroup(
        name="ketone", structure="R-CO-R'", suffix="one", prefix="oxo",
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=3, electron_effect="withdrawing"
    ),
    "carboxylic_acid": FunctionalGroup(
        name="carboxylic acid", structure="R-COOH", suffix="oic acid", prefix=None,
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=10, electron_effect="withdrawing"
    ),
    "ester": FunctionalGroup(
        name="ester", structure="R-COO-R'", suffix="oate", prefix="alkoxycarbonyl",
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=8, electron_effect="withdrawing"
    ),
    "anhydride": FunctionalGroup(
        name="anhydride", structure="R-CO-O-CO-R'", suffix="anhydride", prefix=None,
        group_type=FunctionalGroupType.OXYGEN_CONTAINING, priority=9, electron_effect="withdrawing"
    ),
    
    # Nitrogen-containing
    "amine": FunctionalGroup(
        name="amine", structure="R-NH2/R2NH/R3N", suffix="amine", prefix="amino",
        group_type=FunctionalGroupType.NITROGEN_CONTAINING, priority=1, electron_effect="donating"
    ),
    "amide": FunctionalGroup(
        name="amide", structure="R-CONH2", suffix="amide", prefix="carbamoyl",
        group_type=FunctionalGroupType.NITROGEN_CONTAINING, priority=6, electron_effect="withdrawing"
    ),
    "nitrile": FunctionalGroup(
        name="nitrile", structure="R-C≡N", suffix="nitrile", prefix="cyano",
        group_type=FunctionalGroupType.NITROGEN_CONTAINING, priority=5, electron_effect="withdrawing"
    ),
    "nitro": FunctionalGroup(
        name="nitro", structure="R-NO2", suffix=None, prefix="nitro",
        group_type=FunctionalGroupType.NITROGEN_CONTAINING, priority=0, electron_effect="withdrawing"
    ),
    
    # Halogen-containing
    "alkyl_halide": FunctionalGroup(
        name="alkyl halide", structure="R-X", suffix="halide", prefix="halo",
        group_type=FunctionalGroupType.HALOGEN_CONTAINING, priority=0, electron_effect="withdrawing"
    ),
    "acyl_halide": FunctionalGroup(
        name="acyl halide", structure="R-COX", suffix="oyl halide", prefix=None,
        group_type=FunctionalGroupType.HALOGEN_CONTAINING, priority=7, electron_effect="withdrawing"
    ),
    
    # Sulfur-containing
    "thiol": FunctionalGroup(
        name="thiol", structure="R-SH", suffix="thiol", prefix="mercapto",
        group_type=FunctionalGroupType.SULFUR_CONTAINING, priority=0, electron_effect="donating"
    ),
    "sulfide": FunctionalGroup(
        name="sulfide", structure="R-S-R'", suffix="sulfide", prefix="alkylthio",
        group_type=FunctionalGroupType.SULFUR_CONTAINING, priority=0, electron_effect="donating"
    ),
}

# Electron-withdrawing groups (EWG)
EWG_GROUPS = ["nitro", "nitrile", "carboxylic_acid", "aldehyde", "ketone", "ester", "amide", "acyl_halide"]

# Electron-donating groups (EDG)
EDG_GROUPS = ["alcohol", "ether", "amine", "thiol", "sulfide"]


def identify_functional_groups(smiles_or_formula: str) -> List[str]:
    """
    Identify functional groups present in a molecule.
    
    Args:
        smiles_or_formula: SMILES string or molecular formula
    
    Returns:
        List of identified functional group names
    
    Examples:
        >>> identify_functional_groups("CH3CH2OH")
        ['alcohol']
        >>> identify_functional_groups("CH3COOH")
        ['carboxylic_acid']
    """
    groups = []
    s = smiles_or_formula.lower()
    
    # Check for functional groups (order matters for priority)
    if "cooh" in s or "c(=o)o" in s:
        groups.append("carboxylic_acid")
    elif "coo" in s or "c(=o)oc" in s:
        groups.append("ester")
    elif "conh" in s or "c(=o)n" in s:
        groups.append("amide")
    elif "cho" in s or "c=O" in s.lower():
        groups.append("aldehyde")
    elif "c=O".lower() in s or "co" in s:
        if "carboxylic" not in groups and "ester" not in groups:
            groups.append("ketone")
    
    if "oh" in s or "-o" in s:
        if "carboxylic_acid" not in groups:
            groups.append("alcohol")
    
    if "nh2" in s or "n" in s:
        if "amide" not in groups and "nitrile" not in groups:
            groups.append("amine")
    
    if "cn" in s or "c#n" in s:
        groups.append("nitrile")
    
    if "no2" in s or "n(=o)=o" in s:
        groups.append("nitro")
    
    if "sh" in s:
        groups.append("thiol")
    
    # Check for hydrocarbons
    if "=" in s and "c=c" in s:
        groups.append("alkene")
    if "#" in s and "c#c" in s:
        groups.append("alkyne")
    
    # Default to alkane if carbon present
    if "c" in s and not groups:
        groups.append("alkane")
    
    return list(set(groups))


def _get_functional_group(group_name: str) -> FunctionalGroup:
    if not isinstance(group_name, str):
        raise ValueError(f"Unknown functional group: {group_name!r}")
    key = group_name.lower().replace(" ", "_")
    try:
        return FUNCTIONAL_GROUPS[key]
    except KeyError as exc:
        raise ValueError(f"Unknown functional group: {group_name!r}") from exc


def get_naming_priority(group_name: str) -> int:
    """
    Get the naming priority of a functional group.
    
    Higher priority = principal group (suffix).
    
    Args:
        group_name: Name of functional group
    
    Returns:
        Priority number (higher = higher priority)

    Raises:
        ValueError: If the group is unknown or outside the supported ordinary
            acyclic characteristic-group nomenclature scope. Recognized
            priority-0 groups remain available to the other property getters,
            but do not have a usable principal-group priority here.
    
    Examples:
        >>> get_naming_priority("carboxylic_acid")
        10
        >>> get_naming_priority("alcohol")
        2
    """
    fg = _get_functional_group(group_name)
    if fg.priority == 0:
        raise ValueError(
            "Unsupported nomenclature scope (unsupported-nomenclature-scope): "
            f"{group_name!r} has no supported characteristic-group priority"
        )
    return fg.priority


def determine_principal_group(groups: List[str]) -> str:
    """
    Determine the principal functional group for naming.
    
    The principal group gets the suffix; others become prefixes.
    
    Args:
        groups: List of functional group names
    
    Returns:
        Name of principal group

    Notes:
        An empty list retains the legacy ``"alkane"`` default. For non-empty
        input, recognized hydrocarbon and prefix-only groups are ignored when
        a supported characteristic group is present. Thiol is deliberately
        refused in every mixture until its nomenclature scope is sourced.
        Inputs with no supported characteristic group raise ``ValueError``;
        this function is not a full IUPAC parent-selection engine.
    
    Examples:
        >>> determine_principal_group(["alcohol", "alkene"])
        'alcohol'
    """
    if not groups:
        return "alkane"

    resolved = [(group_name, _get_functional_group(group_name)) for group_name in groups]
    if any(fg.name == "thiol" for _, fg in resolved):
        raise ValueError(
            "Unsupported nomenclature scope (unsupported-nomenclature-scope): "
            "thiol principal-group selection is not sourced"
        )

    characteristic_groups = [
        (group_name, fg) for group_name, fg in resolved if fg.priority > 0
    ]
    if not characteristic_groups:
        raise ValueError(
            "Unsupported nomenclature scope (unsupported-nomenclature-scope): "
            "no supported characteristic principal group was supplied"
        )
    return max(characteristic_groups, key=lambda item: item[1].priority)[0]


def get_suffix(group_name: str) -> str:
    """
    Get the IUPAC suffix for a functional group.
    
    Args:
        group_name: Name of functional group
    
    Returns:
        Suffix for naming
    
    Examples:
        >>> get_suffix("alcohol")
        'ol'
        >>> get_suffix("carboxylic_acid")
        'oic acid'
    """
    fg = _get_functional_group(group_name)
    return fg.suffix or ""


def get_prefix(group_name: str) -> str:
    """
    Get the IUPAC prefix for a functional group.
    
    Args:
        group_name: Name of functional group
    
    Returns:
        Prefix for naming
    
    Examples:
        >>> get_prefix("alcohol")
        'hydroxy'
        >>> get_prefix("nitro")
        'nitro'
    """
    fg = _get_functional_group(group_name)
    return fg.prefix or ""


def classify_electron_effect(group_name: str) -> str:
    """
    Classify whether a group is electron-withdrawing or donating.
    
    Args:
        group_name: Name of functional group
    
    Returns:
        "withdrawing", "donating", or "neutral"
    
    Examples:
        >>> classify_electron_effect("nitro")
        'withdrawing'
        >>> classify_electron_effect("amine")
        'donating'
    """
    return _get_functional_group(group_name).electron_effect


def predict_boiling_point_trend(groups: List[str]) -> str:
    """
    Predict boiling point trend based on functional groups.
    
    Args:
        groups: List of functional groups
    
    Returns:
        Description of boiling point trend
    
    Examples:
        >>> predict_boiling_point_trend(["alcohol"])
        'Higher bp due to hydrogen bonding'
    """
    if any(g in groups for g in ["carboxylic_acid"]):
        return "Highest bp among organics (strong H-bonding, forms dimers)"
    elif any(g in groups for g in ["alcohol", "amine"]) and "thiol" not in groups:
        return "Higher bp due to hydrogen bonding"
    elif any(g in groups for g in ["aldehyde", "ketone", "ester"]):
        return "Moderate bp due to dipole-dipole interactions"
    elif "alkane" in groups and len(groups) == 1:
        return "Low bp, only London dispersion forces"
    else:
        return "Variable bp depending on molecular weight and functional groups"


def predict_solubility(groups: List[str], carbons: int = 4) -> str:
    """
    Predict water solubility based on functional groups.
    
    Args:
        groups: List of functional groups
        carbons: Approximate number of carbons
    
    Returns:
        Solubility description
    
    Examples:
        >>> predict_solubility(["alcohol"], 2)
        'Highly water soluble (small polar molecule with H-bonding)'
    """
    polar_groups = ["alcohol", "carboxylic_acid", "amine", "aldehyde", "ketone"]
    h_bonding_groups = ["alcohol", "carboxylic_acid", "amine"]
    
    has_polar = any(g in groups for g in polar_groups)
    has_h_bonding = any(g in groups for g in h_bonding_groups)
    
    if has_h_bonding and carbons <= 4:
        return "Highly water soluble (small polar molecule with H-bonding)"
    elif has_h_bonding and carbons <= 8:
        return "Moderately water soluble (larger but still H-bonding)"
    elif has_polar and carbons <= 4:
        return "Slightly water soluble (polar but limited H-bonding)"
    else:
        return "Water insoluble (hydrophobic)"


def functional_group_summary() -> Dict:
    """
    Get a summary table of all functional groups.
    
    Returns:
        Dictionary with functional group information
    """
    summary = {}
    for name, fg in FUNCTIONAL_GROUPS.items():
        summary[name] = {
            "structure": fg.structure,
            "suffix": fg.suffix,
            "prefix": fg.prefix,
            "type": fg.group_type.value,
            "priority": fg.priority,
            "electron_effect": fg.electron_effect,
        }
    return summary


# Test functions
def test_identify_groups():
    """Test functional group identification"""
    assert "alcohol" in identify_functional_groups("CH3CH2OH")
    assert "carboxylic_acid" in identify_functional_groups("CH3COOH")
    print("✓ Group identification tests passed")


def test_priorities():
    """Test priority ordering"""
    assert get_naming_priority("carboxylic_acid") > get_naming_priority("alcohol")
    try:
        get_naming_priority("alkene")
    except ValueError:
        pass
    else:
        raise AssertionError("alkene must remain outside naming-priority scope")
    print("✓ Priority tests passed")


def test_principal():
    """Test principal group determination"""
    assert determine_principal_group(["alcohol", "alkene"]) == "alcohol"
    assert determine_principal_group(["carboxylic_acid", "alcohol"]) == "carboxylic_acid"
    print("✓ Principal group tests passed")


if __name__ == "__main__":
    test_identify_groups()
    test_priorities()
    test_principal()
    print("\n✓ All functional group tools tests passed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "classify_electron_effect",
        "description": "Classify whether a group is electron-withdrawing or donating.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group Name"},
            },
            "required": ["group_name"]
        }
    },
    {
        "name": "dataclass",
        "description": "Add dunder methods based on the fields defined in the class.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cls": {"type": "number", "description": "Cls", "default": None},
                "init": {"type": "number", "description": "Init", "default": True},
                "repr": {"type": "number", "description": "Repr", "default": True},
                "eq": {"type": "number", "description": "Eq", "default": True},
                "order": {"type": "number", "description": "Order", "default": False},
                "unsafe_hash": {"type": "number", "description": "Unsafe Hash", "default": False},
                "frozen": {"type": "number", "description": "Frozen", "default": False},
                "match_args": {"type": "number", "description": "Match Args", "default": True},
                "kw_only": {"type": "number", "description": "Kw Only", "default": False},
                "slots": {"type": "number", "description": "Slots", "default": False},
                "weakref_slot": {"type": "number", "description": "Weakref Slot", "default": False},
            },
            "required": []
        }
    },
    {
        "name": "determine_principal_group",
        "description": "Determine the principal functional group for naming.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "groups": {"type": "number", "description": "Groups"},
            },
            "required": ["groups"]
        }
    },
    {
        "name": "functional_group_summary",
        "description": "Get a summary table of all functional groups.",
        "inputSchema": {
            "type": "object",
            "properties": {
            },
            "required": []
        }
    },
    {
        "name": "get_naming_priority",
        "description": "Get the naming priority of a functional group.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group Name"},
            },
            "required": ["group_name"]
        }
    },
    {
        "name": "get_prefix",
        "description": "Get the IUPAC prefix for a functional group.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group Name"},
            },
            "required": ["group_name"]
        }
    },
    {
        "name": "get_suffix",
        "description": "Get the IUPAC suffix for a functional group.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group_name": {"type": "string", "description": "Group Name"},
            },
            "required": ["group_name"]
        }
    },
    {
        "name": "identify_functional_groups",
        "description": "Identify functional groups present in a molecule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "smiles_or_formula": {"type": "string", "description": "Smiles Or Formula"},
            },
            "required": ["smiles_or_formula"]
        }
    },
    {
        "name": "predict_boiling_point_trend",
        "description": "Predict boiling point trend based on functional groups.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "groups": {"type": "number", "description": "Groups"},
            },
            "required": ["groups"]
        }
    },
    {
        "name": "predict_solubility",
        "description": "Predict water solubility based on functional groups.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "groups": {"type": "number", "description": "Groups"},
                "carbons": {"type": "number", "description": "Carbons", "default": 4},
            },
            "required": ["groups"]
        }
    },
    {
        "name": "test_identify_groups",
        "description": "Test functional group identification",
        "inputSchema": {
            "type": "object",
            "properties": {
            },
            "required": []
        }
    },
    {
        "name": "test_principal",
        "description": "Test principal group determination",
        "inputSchema": {
            "type": "object",
            "properties": {
            },
            "required": []
        }
    },
    {
        "name": "test_priorities",
        "description": "Test priority ordering",
        "inputSchema": {
            "type": "object",
            "properties": {
            },
            "required": []
        }
    }
]
