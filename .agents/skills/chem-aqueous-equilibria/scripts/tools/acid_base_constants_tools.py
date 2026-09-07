"""
Acid-Base Constants Tools - L3 Implementation
Chapter 14.3: Relative Strengths of Acids and Bases

## Solver Instructions (for AI Agent)

When you encounter acid-base strength/pKa/Ka/Kb problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given: compound name, Kₐ value, pKₐ value, conjugate pair, or pH
- Asked: relative strength, pKₐ from Kₐ, Kₐ from pKₐ, conjugate identification

### Step 2: Choose the correct function
- `pKa_from_Ka(Ka)`: Convert Ka to pKa (pKa = -log10 Ka)
- `Ka_from_pKa(pKa)`: Convert pKa to Ka (Ka = 10^(-pKa))
- `conjugate_base_Ka(Ka_acid)`: Get Ka of conjugate base (Ka_base = Kw/Ka_acid)
- `conjugate_acid_Kb(Kb_base)`: Get Kb of conjugate acid (Kb_acid = Kw/Kb_base)
- `relative_strength(Ka1, Ka2)`: Compare two acids by Ka values
- `ph_from_weak_acid(Ka, concentration)`: Calculate pH of weak acid solution
- `ph_from_weak_base(Kb, concentration)`: Calculate pH of weak base solution
- `percent_ionization(Ka, concentration)`: Calculate % ionization
- `polyprotic_distribution(pKa_values, pH)`: Species distribution for polyprotic acids

### Step 3: Handle special cases
- For polyprotic acids (H2SO4, H3PO4, H2CO3), use polyprotic functions
- Remember: stronger acid -> weaker conjugate base (Ka x Kb = Kw = 1.0x10-14 at 25degC)
- At 25degC: pKa + pKb = 14 for conjugate pairs

### Examples
```python
pKa = pKa_from_Ka(1.8e-5)        # acetic acid -> 4.74
Kb = conjugate_base_Ka(1.8e-5)     # acetate -> 5.56e-10
ph = ph_from_weak_acid(1.8e-5, 0.1)  # 0.1 M HOAc -> ~2.87
result = relative_strength(6.2e-10, 6.8e-4)  # HF stronger than HCN
```
"""

from typing import Dict, Tuple, Optional
from math import log10, sqrt


def Ka_Kb_relationship(Ka: float = None, Kb: float = None, 
                        temperature: float = 25.0) -> float:
    """
    Calculate Ka from Kb or vice versa.
    
    Ka x Kb = Kw
    
    Args:
        Ka: Acid ionization constant
        Kb: Base ionization constant
        temperature: Temperature in degC
    
    Returns:
        The other constant
    
    Examples:
        >>> Ka_Kb_relationship(Kb=1.8e-5)
        5.6e-10
    """
    Kw = 1.0e-14 if temperature == 25.0 else 1.0e-14
    
    if Ka is not None and Kb is None:
        return Kw / Ka
    elif Kb is not None and Ka is None:
        return Kw / Kb
    return None


def percent_ionization(h3o_conc: float, initial_conc: float) -> float:
    """
    Calculate percent ionization of a weak acid.
    
    Args:
        h3o_conc: Equilibrium [H3O+]
        initial_conc: Initial acid concentration
    
    Returns:
        Percent ionization
    
    Examples:
        >>> percent_ionization(0.001, 0.1)
        1.0
    """
    return (h3o_conc / initial_conc) * 100


def weak_acid_pH(Ka: float, initial_conc: float) -> float:
    """
    Calculate pH of weak acid solution.
    
    Uses quadratic formula when Ka/C > 0.01 (5% ionization threshold),
    otherwise uses the sqrt approximation.
    
    Args:
        Ka: Acid ionization constant
        initial_conc: Initial concentration (M)
    
    Returns:
        pH value
    
    Examples:
        >>> round(weak_acid_pH(1.8e-5, 0.1), 2)
        2.87
        >>> round(weak_acid_pH(1.8e-4, 0.1), 2)
        2.38
    """
    C = initial_conc
    # Check if approximation is valid (ionization < 5%)
    if Ka * C < 1e-12:
        h3o = sqrt(Ka * C)
    else:
        # Quadratic: [H+]^2 + Ka[H+] - Ka*C = 0
        # h = (-Ka + sqrt(Ka^2 + 4*Ka*C)) / 2
        h3o = (-Ka + sqrt(Ka * Ka + 4 * Ka * C)) / 2.0
    return -log10(h3o)


def weak_base_pH(Kb: float, initial_conc: float) -> float:
    """
    Calculate pH of weak base solution.
    
    Uses quadratic formula when Kb/C > 0.01 (5% ionization threshold),
    otherwise uses the sqrt approximation.
    
    Args:
        Kb: Base ionization constant
        initial_conc: Initial concentration (M)
    
    Returns:
        pH value
    
    Examples:
        >>> round(weak_base_pH(1.8e-5, 0.1), 2)
        11.13
    """
    C = initial_conc
    if Kb * C < 1e-12:
        oh = sqrt(Kb * C)
    else:
        # Quadratic: [OH-]^2 + Kb[OH-] - Kb*C = 0
        oh = (-Kb + sqrt(Kb * Kb + 4 * Kb * C)) / 2.0
    pOH = -log10(oh)
    return 14.0 - pOH


def is_strong_acid(Ka: float) -> bool:
    """
    Determine if acid is strong based on Ka.
    
    Args:
        Ka: Acid ionization constant
    
    Returns:
        True if strong acid
    
    Examples:
        >>> is_strong_acid(1e6)
        True
        >>> is_strong_acid(1.8e-5)
        False
    """
    return Ka > 1.0


def is_strong_base(Kb: float) -> bool:
    """
    Determine if base is strong based on Kb.
    
    Args:
        Kb: Base ionization constant
    
    Returns:
        True if strong base
    
    Examples:
        >>> is_strong_base(1e6)
        True
    """
    return Kb > 1.0


def compare_acid_strengths(Ka1: float, Ka2: float) -> str:
    """
    Compare relative acid strengths.
    
    Args:
        Ka1: First acid's Ka
        Ka2: Second acid's Ka
    
    Returns:
        Comparison result
    
    Examples:
        >>> compare_acid_strengths(1.8e-5, 4.6e-4)
        'Acid 2 is stronger'
    """
    if Ka1 > Ka2:
        return 'Acid 1 is stronger'
    elif Ka2 > Ka1:
        return 'Acid 2 is stronger'
    else:
        return 'Acids have equal strength'


def conjugate_base_strength(Ka: float, temperature: float = 25.0) -> float:
    """
    Calculate Kb of conjugate base.
    
    Args:
        Ka: Acid ionization constant
        temperature: Temperature in degC
    
    Returns:
        Kb of conjugate base
    
    Examples:
        >>> conjugate_base_strength(1.8e-5)
        5.6e-10
    """
    return Ka_Kb_relationship(Ka=Ka, temperature=temperature)


def validate_approximation(Ka: float, C0: float, 
                           threshold: float = 0.05) -> bool:
    """
    Check if small x approximation is valid.
    
    Valid when x/C0 < 5%, i.e., when Ka << C0
    
    Args:
        Ka: Acid ionization constant
        C0: Initial concentration
        threshold: Maximum acceptable ratio
    
    Returns:
        True if approximation valid
    
    Examples:
        >>> validate_approximation(1.8e-5, 0.1)
        True
        >>> validate_approximation(0.1, 0.01)
        False
    """
    # Approximation valid when Ka x C0 is small
    # Check if ionization < 5%
    ionization_ratio = sqrt(Ka / C0)
    return ionization_ratio < threshold


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "Ka_Kb_relationship",
        "description": "Calculate Ka from Kb or vice versa.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ka": {
                    "type": "number",
                    "description": "Ka",
                    "default": None
                },
                "Kb": {
                    "type": "number",
                    "description": "Kb",
                    "default": None
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 25.0
                }
            },
            "required": []
        }
    },
    {
        "name": "compare_acid_strengths",
        "description": "Compare relative acid strengths.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ka1": {
                    "type": "number",
                    "description": "Ka1"
                },
                "Ka2": {
                    "type": "number",
                    "description": "Ka2"
                }
            },
            "required": [
                "Ka1",
                "Ka2"
            ]
        }
    },
    {
        "name": "conjugate_base_strength",
        "description": "Calculate Kb of conjugate base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ka": {
                    "type": "number",
                    "description": "Ka"
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 25.0
                }
            },
            "required": [
                "Ka"
            ]
        }
    },
    {
        "name": "is_strong_acid",
        "description": "Determine if acid is strong based on Ka.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ka": {
                    "type": "number",
                    "description": "Ka"
                }
            },
            "required": [
                "Ka"
            ]
        }
    },
    {
        "name": "is_strong_base",
        "description": "Determine if base is strong based on Kb.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Kb": {
                    "type": "number",
                    "description": "Kb"
                }
            },
            "required": [
                "Kb"
            ]
        }
    },
    {
        "name": "percent_ionization",
        "description": "Calculate percent ionization of a weak acid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "h3o_conc": {
                    "type": "number",
                    "description": "H3O Conc"
                },
                "initial_conc": {
                    "type": "number",
                    "description": "Initial Conc"
                }
            },
            "required": [
                "h3o_conc",
                "initial_conc"
            ]
        }
    },
    {
        "name": "validate_approximation",
        "description": "Check if small x approximation is valid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ka": {
                    "type": "number",
                    "description": "Ka"
                },
                "C0": {
                    "type": "number",
                    "description": "C0"
                },
                "threshold": {
                    "type": "number",
                    "description": "Threshold",
                    "default": 0.05
                }
            },
            "required": [
                "Ka",
                "C0"
            ]
        }
    },
    {
        "name": "weak_acid_pH",
        "description": "Calculate pH of weak acid solution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Ka": {
                    "type": "number",
                    "description": "Ka"
                },
                "initial_conc": {
                    "type": "number",
                    "description": "Initial Conc"
                }
            },
            "required": [
                "Ka",
                "initial_conc"
            ]
        }
    },
    {
        "name": "weak_base_pH",
        "description": "Calculate pH of weak base solution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Kb": {
                    "type": "number",
                    "description": "Kb"
                },
                "initial_conc": {
                    "type": "number",
                    "description": "Initial Conc"
                }
            },
            "required": [
                "Kb",
                "initial_conc"
            ]
        }
    }
]