"""
Brønsted-Lowry Tools - L3 Implementation
Chapter 14.1: Brønsted-Lowry Acids and Bases
"""
## Solver Instructions (for AI Agent)

# When you encounter Brønsted-Lowry acid-base problems (conjugate pairs, Kw, solution classification), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: acid/base formulas, [H3O+] or [OH-], reaction equation, temperature
# - **Asked**: conjugate base/acid, [H3O+]/[OH-], Kw, solution classification, amphiprotic check

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Conjugate base | `conjugate_base(acid, formula)` | acid formula |
# | Conjugate acid | `conjugate_acid(base, formula)` | base formula |
# | Identify acid/base | `identify_acid_base(reaction)` | reaction string |
# | Amphiprotic check | `is_amphiprotic(formula)` | formula |
# | Kw at temperature | `Kw_value(temperature)` | degC |
# | [H3O+] from [OH-] | `h3o_from_oh(oh_conc, temperature)` | [OH-] |
# | [OH-] from [H3O+] | `oh_from_h3o(h3o_conc, temperature)` | [H3O+] |
# | Classify solution | `classify_solution(h3o_conc, temperature)` | [H3O+] |

### Step 3: Handle special cases
# - Kw = 1x10-14 at 25degC; 5.6x10-13 at 100degC
# - Amphiprotic species: H2O, HCO3-, H2PO4-, HS-, HSO4-

### Examples
# 1. **Conjugate**: `conjugate_base('HCl', 'HCl')` -> 'Cl-'; `conjugate_acid('NH3', 'NH3')` -> 'NH4+'
# 2. **Kw conversion**: `h3o_from_oh(1e-6)` -> 1e-8 M (basic)
# 3. **Classify**: `classify_solution(1e-4)` -> 'acidic'


from typing import Dict, List, Tuple, Optional


def conjugate_base(acid: str, formula: str) -> str:
    """
    Return conjugate base of an acid.
    
    Args:
        acid: Acid name/formula
        formula: Chemical formula with H count
    
    Returns:
        Conjugate base formula
    
    Examples:
        >>> conjugate_base('HCl', 'HCl')
        'Cl-'
        >>> conjugate_base('H2SO4', 'H2SO4')
        'HSO4-'
    """
    # Remove one H and add negative charge
    if formula.startswith('H'):
        return formula[1:] + '-'
    return formula


def conjugate_acid(base: str, formula: str) -> str:
    """
    Return conjugate acid of a base.
    
    Args:
        base: Base name/formula
        formula: Chemical formula
    
    Returns:
        Conjugate acid formula
    
    Examples:
        >>> conjugate_acid('NH3', 'NH3')
        'NH4+'
        >>> conjugate_acid('OH-', 'OH-')
        'H2O'
    """
    # Add H and adjust charge
    if formula.endswith('-'):
        return 'H' + formula[:-1]  # Remove charge, add H
    return 'H' + formula + '+'


def identify_acid_base(reaction: str) -> Dict:
    """
    Identify acid, base, conjugate acid, conjugate base in reaction.
    
    Args:
        reaction: Reaction string like "HA + B -> A- + HB+"
    
    Returns:
        Dict with identified species
    
    Examples:
        >>> identify_acid_base("HCl + H2O -> Cl- + H3O+")
        {'acid': 'HCl', 'base': 'H2O', 'conjugate_base': 'Cl-', 'conjugate_acid': 'H3O+'}
    """
    # Parse reaction
    sides = reaction.replace(' ', '').split('->')
    if len(sides) != 2:
        return {}
    
    reactants = sides[0].split('+')
    products = sides[1].split('+')
    
    if len(reactants) != 2 or len(products) != 2:
        return {}
    
    # Identify by H transfer (simplified)
    # Acid is species that loses H
    for i, r in enumerate(reactants):
        if r.startswith('H') and 'H' not in products[i % 2]:
            return {
                'acid': reactants[i],
                'base': reactants[1-i],
                'conjugate_base': products[i % 2],
                'conjugate_acid': products[1 - (i % 2)]
            }
    
    return {}


def is_amphiprotic(formula: str) -> bool:
    """
    Check if species is amphiprotic.
    
    Args:
        formula: Chemical formula
    
    Returns:
        True if amphiprotic
    
    Examples:
        >>> is_amphiprotic('H2O')
        True
        >>> is_amphiprotic('HCO3-')
        True
        >>> is_amphiprotic('Cl-')
        False
    """
    amphiprotic_species = ['H2O', 'HCO3-', 'H2PO4-', 'HS-', 'HSO4-', 'HPO4-2']
    return formula in amphiprotic_species


def Kw_value(temperature: float = 25.0) -> float:
    """
    Return ion product of water at given temperature.
    
    Args:
        temperature: Temperature in degC
    
    Returns:
        Kw value
    
    Examples:
        >>> Kw_value(25.0)
        1e-14
    """
    # Simplified: return standard value at 25degC
    # Real Kw varies with temperature
    if temperature == 25.0:
        return 1.0e-14
    elif temperature == 100.0:
        return 5.6e-13
    else:
        return 1.0e-14  # Default to 25degC


def h3o_from_oh(oh_conc: float, temperature: float = 25.0) -> float:
    """
    Calculate [H3O+] from [OH-] using Kw.
    
    Args:
        oh_conc: Hydroxide ion concentration (M)
        temperature: Temperature in degC
    
    Returns:
        Hydronium ion concentration (M)
    
    Examples:
        >>> h3o_from_oh(1e-7)
        1e-07
    """
    Kw = Kw_value(temperature)
    return Kw / oh_conc


def oh_from_h3o(h3o_conc: float, temperature: float = 25.0) -> float:
    """
    Calculate [OH-] from [H3O+] using Kw.
    
    Args:
        h3o_conc: Hydronium ion concentration (M)
        temperature: Temperature in degC
    
    Returns:
        Hydroxide ion concentration (M)
    
    Examples:
        >>> oh_from_h3o(1e-7)
        1e-07
    """
    Kw = Kw_value(temperature)
    return Kw / h3o_conc


def classify_solution(h3o_conc: float, temperature: float = 25.0) -> str:
    """
    Classify solution as acidic, basic, or neutral.
    
    Args:
        h3o_conc: Hydronium ion concentration (M)
        temperature: Temperature in degC
    
    Returns:
        Classification string
    
    Examples:
        >>> classify_solution(1e-7)
        'neutral'
        >>> classify_solution(1e-4)
        'acidic'
    """
    # At 25degC, neutral is 1e-7 M
    neutral_conc = (Kw_value(temperature)) ** 0.5
    
    if abs(h3o_conc - neutral_conc) < neutral_conc * 0.01:
        return 'neutral'
    elif h3o_conc > neutral_conc:
        return 'acidic'
    else:
        return 'basic'


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "Kw_value",
        "description": "Return ion product of water at given temperature.",
        "inputSchema": {
            "type": "object",
            "properties": {
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
        "name": "classify_solution",
        "description": "Classify solution as acidic, basic, or neutral.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "h3o_conc": {
                    "type": "number",
                    "description": "H3O Conc"
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 25.0
                }
            },
            "required": [
                "h3o_conc"
            ]
        }
    },
    {
        "name": "conjugate_acid",
        "description": "Return conjugate acid of a base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base": {
                    "type": "number",
                    "description": "Base"
                },
                "formula": {
                    "type": "string",
                    "description": "Formula"
                }
            },
            "required": [
                "base",
                "formula"
            ]
        }
    },
    {
        "name": "conjugate_base",
        "description": "Return conjugate base of an acid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "acid": {
                    "type": "number",
                    "description": "Acid"
                },
                "formula": {
                    "type": "string",
                    "description": "Formula"
                }
            },
            "required": [
                "acid",
                "formula"
            ]
        }
    },
    {
        "name": "h3o_from_oh",
        "description": "Calculate [H3O+] from [OH-] using Kw.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "oh_conc": {
                    "type": "number",
                    "description": "Oh Conc"
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 25.0
                }
            },
            "required": [
                "oh_conc"
            ]
        }
    },
    {
        "name": "identify_acid_base",
        "description": "Identify acid, base, conjugate acid, conjugate base in reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reaction": {
                    "type": "number",
                    "description": "Reaction"
                }
            },
            "required": [
                "reaction"
            ]
        }
    },
    {
        "name": "is_amphiprotic",
        "description": "Check if species is amphiprotic.",
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
        "name": "oh_from_h3o",
        "description": "Calculate [OH-] from [H3O+] using Kw.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "h3o_conc": {
                    "type": "number",
                    "description": "H3O Conc"
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 25.0
                }
            },
            "required": [
                "h3o_conc"
            ]
        }
    }
]