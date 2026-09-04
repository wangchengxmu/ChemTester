"""
Electrolyte Tools - L3 Implementation
Chapter 11.02: Electrolytes and Dissociation

## Solver Instructions (for AI Agent)

When you encounter electrolyte classification, dissociation, and solubility problems:

### Step 1: Identify what is given and what is asked
- Given: chemical formula
- Asked: strong/weak/nonelectrolyte, dissociation equation, ion count, solubility

### Step 2: Choose the correct function
- `classify_electrolyte(formula)`: Strong/weak/nonelectrolyte
- `dissociation_equation(formula)`: Dissociation equation string
- `ion_count(formula)`: Number of ions per formula unit (van't Hoff i)
- `parse_ionic_formula(formula)`: Split into (cation, anion)
- `get_ion_charges(cation, anion)`: Typical charges for ions
- `is_soluble(cation, anion)`: Solubility rules check
- `format_ion(ion, charge)`: Format with superscript (Na+, Ca2+)

### Step 3: Handle special cases
- Strong acids: HCl, HBr, HI, HNO3, HClO3, HClO4, H2SO4
- Strong bases: Group 1 hydroxides, Ba(OH)2, Ca(OH)2, Sr(OH)2
- All Na+, K+, NH4+, NO3- compounds are soluble

### Examples
```python
classify_electrolyte('NaCl')  # -> 'strong electrolyte'
dissociation_equation('CaCl2')  # -> 'CaCl2(s) -> Ca2+(aq) + 2Cl-(aq)'
ion_count('Al2(SO4)3')  # -> 5
is_soluble('Ag', 'Cl')  # -> False
```
"""

from typing import List, Tuple, Optional

# Strong acids (completely dissociate)
STRONG_ACIDS = ['HCl', 'HBr', 'HI', 'HNO3', 'H2SO4', 'HClO3', 'HClO4']

# Strong bases (completely dissociate)
STRONG_BASES = ['NaOH', 'KOH', 'LiOH', 'RbOH', 'CsOH', 'Ca(OH)2', 'Sr(OH)2', 'Ba(OH)2']

# Soluble ionic compounds (strong electrolytes)
SOLUBLE_RULES = {
    # Always soluble
    'always_soluble_cations': ['Na', 'K', 'Li', 'Rb', 'Cs', 'NH4'],
    'always_soluble_anions': ['NO3', 'C2H3O2', 'ClO3', 'ClO4'],
    # Mostly soluble with exceptions
    'Cl': {'exceptions': ['Ag', 'Pb', 'Hg2']},
    'Br': {'exceptions': ['Ag', 'Pb', 'Hg2']},
    'I': {'exceptions': ['Ag', 'Pb', 'Hg2']},
    'SO4': {'exceptions': ['Ba', 'Pb', 'Ca', 'Sr']},
    # Mostly insoluble with exceptions
    'OH': {'soluble': ['Na', 'K', 'Li', 'Rb', 'Cs', 'Ba', 'Ca', 'Sr']},
    'CO3': {'soluble': ['Na', 'K', 'Li', 'Rb', 'Cs', 'NH4']},
    'PO4': {'soluble': ['Na', 'K', 'Li', 'Rb', 'Cs', 'NH4']},
    'S': {'soluble': ['Na', 'K', 'Li', 'Rb', 'Cs', 'NH4', 'Ca', 'Ba', 'Sr']},
}


def classify_electrolyte(formula: str) -> str:
    """
    Classify substance as strong electrolyte, weak electrolyte, or nonelectrolyte.
    
    Args:
        formula: Chemical formula
    
    Returns:
        Classification string
    
    Examples:
        >>> classify_electrolyte('NaCl')
        'strong electrolyte'
        >>> classify_electrolyte('HC2H3O2')
        'weak electrolyte'
        >>> classify_electrolyte('C6H12O6')
        'nonelectrolyte'
    """
    formula = formula.strip()
    
    # Check strong acids
    if formula in STRONG_ACIDS:
        return 'strong electrolyte'
    
    # Check strong bases
    if formula in STRONG_BASES:
        return 'strong electrolyte'
    
    # Check for common weak acids
    weak_acids = ['HC2H3O2', 'H2CO3', 'H3PO4', 'HF', 'HCN', 'H2S', 'HNO2']
    if formula in weak_acids:
        return 'weak electrolyte'
    
    # Check for common weak bases
    weak_bases = ['NH3', 'C5H5N', 'CH3NH2']
    if formula in weak_bases:
        return 'weak electrolyte'
    
    # Check if ionic compound
    ions = parse_ionic_formula(formula)
    if ions:
        cation, anion = ions
        if is_soluble(cation, anion):
            return 'strong electrolyte'
        else:
            return 'weak electrolyte (insoluble)'
    
    # Default to nonelectrolyte for molecular compounds
    return 'nonelectrolyte'


def dissociation_equation(formula: str) -> str:
    """
    Generate dissociation equation for an electrolyte.
    
    Args:
        formula: Chemical formula
    
    Returns:
        Dissociation equation as string
    
    Examples:
        >>> dissociation_equation('NaCl')
        'NaCl(s) -> Na+(aq) + Cl-(aq)'
        >>> dissociation_equation('CaCl2')
        'CaCl2(s) -> Ca2+(aq) + 2Cl-(aq)'
    """
    ions = parse_ionic_formula(formula)
    if not ions:
        # For acids or molecular compounds
        if formula in STRONG_ACIDS:
            return f"{formula}(aq) -> H+(aq) + {formula[1:]}-(aq)"
        return f"{formula} does not dissociate significantly"
    
    cation, anion = ions
    charges = get_ion_charges(cation, anion)
    
    if charges is None:
        return f"{formula} dissociation unknown"
    
    cat_charge, an_charge = charges
    cat_coeff, an_coeff = abs(an_charge), abs(cat_charge)
    
    # Simplify coefficients
    from math import gcd
    if cat_coeff > 1 or an_coeff > 1:
        g = gcd(cat_coeff, an_coeff)
        cat_coeff //= g
        an_coeff //= g
    
    # Build equation
    cat_str = f"{cat_coeff if cat_coeff > 1 else ''}{format_ion(cation, cat_charge)}"
    an_str = f"{an_coeff if an_coeff > 1 else ''}{format_ion(anion, an_charge)}"
    
    return f"{formula}(s) -> {cat_str}(aq) + {an_str}(aq)"


def ion_count(formula: str) -> int:
    """
    Count the number of ions produced per formula unit.
    
    Args:
        formula: Chemical formula
    
    Returns:
        Number of ions (van't Hoff factor ideal value)
    
    Examples:
        >>> ion_count('NaCl')
        2
        >>> ion_count('CaCl2')
        3
        >>> ion_count('Al2(SO4)3')
        5
    """
    ions = parse_ionic_formula(formula)
    if not ions:
        if formula in STRONG_ACIDS:
            return 2  # H+ + anion
        return 1  # Nonelectrolyte
    
    cation, anion = ions
    charges = get_ion_charges(cation, anion)
    
    if charges is None:
        return 2  # Default assumption
    
    cat_charge, an_charge = charges
    
    # Number of ions = |anion charge| + |cation charge| (balanced)
    from math import gcd
    return abs(an_charge) + abs(cat_charge)


def parse_ionic_formula(formula: str) -> Optional[Tuple[str, str]]:
    """
    Parse ionic formula into cation and anion.
    
    Args:
        formula: Chemical formula
    
    Returns:
        (cation, anion) tuple or None if not ionic
    """
    # Common ions mapping (simplified)
    common_ions = {
        'NaCl': ('Na', 'Cl'),
        'KCl': ('K', 'Cl'),
        'NaBr': ('Na', 'Br'),
        'KBr': ('K', 'Br'),
        'CaCl2': ('Ca', 'Cl'),
        'MgCl2': ('Mg', 'Cl'),
        'Na2SO4': ('Na', 'SO4'),
        'K2SO4': ('K', 'SO4'),
        'CaCO3': ('Ca', 'CO3'),
        'NaNO3': ('Na', 'NO3'),
        'KNO3': ('K', 'NO3'),
        'NaOH': ('Na', 'OH'),
        'KOH': ('K', 'OH'),
        'BaSO4': ('Ba', 'SO4'),
        'AgCl': ('Ag', 'Cl'),
        'PbCl2': ('Pb', 'Cl'),
    }
    
    return common_ions.get(formula)


def get_ion_charges(cation: str, anion: str) -> Optional[Tuple[int, int]]:
    """
    Get typical charges for ions.
    
    Args:
        cation: Cation symbol
        anion: Anion symbol
    
    Returns:
        (cation_charge, anion_charge) tuple
    """
    charges = {
        'Na': 1, 'K': 1, 'Li': 1, 'Rb': 1, 'Cs': 1,
        'Ca': 2, 'Mg': 2, 'Ba': 2, 'Sr': 2,
        'Al': 3, 'Fe': 2, 'Cu': 2, 'Zn': 2, 'Pb': 2, 'Ag': 1,
        'Cl': -1, 'Br': -1, 'I': -1, 'F': -1,
        'SO4': -2, 'CO3': -2, 'O': -2, 'S': -2,
        'NO3': -1, 'OH': -1, 'C2H3O2': -1, 'ClO3': -1, 'ClO4': -1,
        'PO4': -3,
    }
    
    if cation in charges and anion in charges:
        return (charges[cation], charges[anion])
    return None


def is_soluble(cation: str, anion: str) -> bool:
    """
    Check if an ionic compound is soluble.
    
    Args:
        cation: Cation symbol
        anion: Anion symbol
    
    Returns:
        True if soluble
    
    Examples:
        >>> is_soluble('Na', 'Cl')
        True
        >>> is_soluble('Ag', 'Cl')
        False
    """
    # Check always soluble cations
    if cation in SOLUBLE_RULES['always_soluble_cations']:
        return True
    
    # Check always soluble anions
    if anion in SOLUBLE_RULES['always_soluble_anions']:
        return True
    
    # Check specific rules
    if anion in ['Cl', 'Br', 'I']:
        return cation not in SOLUBLE_RULES[anion]['exceptions']
    
    if anion == 'SO4':
        return cation not in SOLUBLE_RULES['SO4']['exceptions']
    
    if anion == 'OH':
        return cation in SOLUBLE_RULES['OH']['soluble']
    
    if anion in ['CO3', 'PO4', 'S']:
        return cation in SOLUBLE_RULES[anion]['soluble']
    
    return True  # Default to soluble


def format_ion(ion: str, charge: int) -> str:
    """Format ion with superscript charge."""
    superscripts = {1: '+', 2: '2+', 3: '3+', -1: '-', -2: '2-', -3: '3-'}
    return f"{ion}{superscripts.get(charge, str(charge))}"


def ion_pairing_tendency(cations: list, solvent: str = 'aqueous') -> list:
    """
    Rank ions by ion-pairing tendency with a given anion.
    
    Args:
        cations: List of cation symbols, e.g., ['Li', 'Na', 'K']
        solvent: 'aqueous' (default) or 'nonaqueous' (e.g., gas phase, organic solvent)
    
    Returns:
        List of cations ordered from strongest to weakest pairing tendency.
    
    AQUEOUS solution (default):
        Less hydrated ions pair more readily: K⁺ > Na⁺ > Li⁺
        (Smaller ions have larger hydration shells, reducing effective Coulomb attraction)
    
    NON-AQUEOUS / gas phase:
        Direct Coulomb attraction dominates: Li⁺ > Na⁺ > K⁺
        (Smaller ions = stronger Coulomb attraction = tighter pairs)
    
    Note:
        The incorrect ordering Li⁺>Na⁺>K⁺ for aqueous solutions ignores hydration effects.
        Always specify the solvent to get the correct ordering.
    """
    # Hydration radii (pm) - larger effective ionic radius in water
    hydration_radii = {
        'Li': 382, 'Na': 358, 'K': 331,
        'Rb': 329, 'Cs': 329,
        'Mg': 428, 'Ca': 412, 'Ba': 404,
        'H': 282,  # H3O+
    }
    
    if solvent == 'aqueous':
        # Aqueous: larger hydration radius = less tightly held by water = easier to pair
        # Sort by hydration radius descending (larger hydrated radius = weaker solvation = more pairing)
        # Actually: smaller hydration radius = less hydrated = easier to strip water = stronger pairing
        # K has smallest hydration radius (331) -> pairs most readily
        return sorted(cations, key=lambda c: hydration_radii.get(c, 400))
    elif solvent == 'nonaqueous':
        # Non-aqueous: bare ionic radius matters - smaller = stronger Coulomb
        bare_radii = {'Li': 76, 'Na': 102, 'K': 138, 'Rb': 152, 'Cs': 167,
                      'Mg': 72, 'Ca': 100, 'Ba': 135, 'H': 0}
        return sorted(cations, key=lambda c: bare_radii.get(c, 100))
    else:
        raise ValueError(f"Unknown solvent: {solvent}. Use 'aqueous' or 'nonaqueous'.")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "classify_electrolyte",
        "description": "Classify substance as strong electrolyte, weak electrolyte, or nonelectrolyte.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Formula"},
            },
            "required": ["formula"]
        }
    },
    {
        "name": "dissociation_equation",
        "description": "Generate dissociation equation for an electrolyte.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Formula"},
            },
            "required": ["formula"]
        }
    },
    {
        "name": "format_ion",
        "description": "Format ion with superscript charge.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ion": {"type": "number", "description": "Ion"},
                "charge": {"type": "number", "description": "Charge"},
            },
            "required": ["ion", "charge"]
        }
    },
    {
        "name": "get_ion_charges",
        "description": "Get typical charges for ions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cation": {"type": "number", "description": "Cation"},
                "anion": {"type": "number", "description": "Anion"},
            },
            "required": ["cation", "anion"]
        }
    },
    {
        "name": "ion_count",
        "description": "Count the number of ions produced per formula unit.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Formula"},
            },
            "required": ["formula"]
        }
    },
    {
        "name": "is_soluble",
        "description": "Check if an ionic compound is soluble.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cation": {"type": "number", "description": "Cation"},
                "anion": {"type": "number", "description": "Anion"},
            },
            "required": ["cation", "anion"]
        }
    },
    {
        "name": "parse_ionic_formula",
        "description": "Parse ionic formula into cation and anion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "Formula"},
            },
            "required": ["formula"]
        }
    }
]
