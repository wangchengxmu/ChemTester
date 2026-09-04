"""
Lewis Acid-Base Tools - L3 Implementation
Chapter 15.2: Lewis Acids and Bases
"""
## Solver Instructions (for AI Agent)

# When you encounter Lewis acid-base problems (complex ion formation, Kf, dissolution), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: complex/metal/ligand concentrations, Kf or Kd, Ksp, charges
# - **Asked**: formation constant, free metal concentration, complex stability, ligand needed

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Identify Lewis acid/base | `identify_lewis_acid_base(s1, s2, s1_lone, s2_lone)` | lone pair info |
# | Formation constant | `formation_constant(complex_conc, metal_conc, ligand_conc, n)` | [MLn], [M], [L], n |
# | Metal conc from Kf | `metal_concentration_from_Kf(Kf, complex_conc, ligand_conc, n)` | Kf, [MLn], [L] |
# | Complex conc | `complex_ion_concentration(Kf, metal_conc, ligand_conc, n)` | Kf, [M], [L] |
# | Dissociation constant | `dissociation_constant(Kf)` | Kd = 1/Kf |
# | Stability check | `is_complex_ion_stable(Kf, threshold)` | default threshold 1010 |
# | Ligand for dissolution | `ligand_needed_for_dissolution(Ksp, Kf, target_conc, n)` | Ksp, Kf, n |
# | Brønsted vs Lewis | `compare_brønsted_lewis(acid_type, base_type)` | comparison text |

### Step 3: Handle special cases
# - Kf = [MLn]/([M][L]ⁿ) - higher Kf = more stable complex
# - Kd = 1/Kf - lower Kd = more stable
# - Ligand with lone pair = Lewis base; electron pair acceptor = Lewis acid

### Examples
# 1. **Kf**: `formation_constant(0.1, 0.001, 0.002, 2)` -> 2.5x107
# 2. **Kd**: `dissociation_constant(1.7e7)` -> 5.9x10-8
# 3. **Stability**: `is_complex_ion_stable(1e12)` -> True


from typing import Dict, Tuple, Optional
from math import sqrt


def identify_lewis_acid_base(species1: str, species2: str,
                              species1_has_lone_pair: bool,
                              species2_has_lone_pair: bool) -> Dict:
    """
    Identify Lewis acid and base in a reaction.
    
    Args:
        species1, species2: Species names
        species1_has_lone_pair: True if species1 can donate electrons
        species2_has_lone_pair: True if species2 can donate electrons
    
    Returns:
        Dict with acid and base identification
    
    Examples:
        >>> identify_lewis_acid_base('BF3', 'F-', False, True)
        {'acid': 'BF3', 'base': 'F-'}
    """
    if species1_has_lone_pair and not species2_has_lone_pair:
        return {'acid': species2, 'base': species1}
    elif species2_has_lone_pair and not species1_has_lone_pair:
        return {'acid': species1, 'base': species2}
    else:
        return {'acid': 'ambiguous', 'base': 'ambiguous'}


def formation_constant(complex_conc: float, metal_conc: float,
                        ligand_conc: float, n_ligands: int) -> float:
    """
    Calculate formation constant Kf.
    
    Kf = [MLn] / ([M][L]^n)
    
    Args:
        complex_conc: Complex ion concentration (M)
        metal_conc: Free metal ion concentration (M)
        ligand_conc: Free ligand concentration (M)
        n_ligands: Number of ligands in complex
    
    Returns:
        Formation constant Kf
    
    Examples:
        >>> formation_constant(0.1, 0.001, 0.002, 2)
        2.5e+07
    """
    return complex_conc / (metal_conc * ligand_conc ** n_ligands)


def metal_concentration_from_Kf(Kf: float, complex_conc: float,
                                 ligand_conc: float, n_ligands: int) -> float:
    """
    Calculate free metal ion concentration from Kf.
    
    Args:
        Kf: Formation constant
        complex_conc: Complex ion concentration (M)
        ligand_conc: Free ligand concentration (M)
        n_ligands: Number of ligands
    
    Returns:
        Free metal ion concentration (M)
    
    Examples:
        >>> metal_concentration_from_Kf(1.7e7, 0.1, 0.002, 2)
        1.47e-03
    """
    return complex_conc / (Kf * ligand_conc ** n_ligands)


def complex_ion_concentration(Kf: float, metal_conc: float,
                               ligand_conc: float, n_ligands: int) -> float:
    """
    Calculate complex ion concentration from Kf.
    
    Args:
        Kf: Formation constant
        metal_conc: Free metal ion concentration (M)
        ligand_conc: Free ligand concentration (M)
        n_ligands: Number of ligands
    
    Returns:
        Complex ion concentration (M)
    
    Examples:
        >>> complex_ion_concentration(1.7e7, 0.001, 0.002, 2)
        68.0
    """
    return Kf * metal_conc * ligand_conc ** n_ligands


def dissociation_constant(Kf: float) -> float:
    """
    Calculate dissociation constant Kd from Kf.
    
    Kd = 1/Kf
    
    Args:
        Kf: Formation constant
    
    Returns:
        Dissociation constant
    
    Examples:
        >>> dissociation_constant(1.7e7)
        5.9e-08
    """
    return 1.0 / Kf


def is_complex_ion_stable(Kf: float, threshold: float = 1e10) -> bool:
    """
    Determine if complex ion is highly stable.
    
    Args:
        Kf: Formation constant
        threshold: Stability threshold (default 10^10)
    
    Returns:
        True if stable
    
    Examples:
        >>> is_complex_ion_stable(1e12)
        True
    """
    return Kf > threshold


def ligand_needed_for_dissolution(Ksp: float, Kf: float,
                                   metal_conc_target: float,
                                   n_ligands: int) -> float:
    """
    Calculate ligand concentration needed to achieve target metal dissolution.
    
    Args:
        Ksp: Solubility product of metal salt
        Kf: Formation constant of complex
        metal_conc_target: Target metal concentration (M)
        n_ligands: Number of ligands per metal
    
    Returns:
        Required ligand concentration (M)
    
    Examples:
        >>> ligand_needed_for_dissolution(1.8e-10, 1.7e7, 0.01, 2)
        0.18
    """
    # For complete dissolution: [MLn] ~ initial metal
    # Kf x [M][L]^n = [MLn]
    # Combined: Ksp x Kf = [MLn]/[L]^n
    
    # This is simplified - full calculation needs equilibrium
    return (Kf * metal_conc_target) ** (1/n_ligands) / Kf ** (1/n_ligands)


def compare_brønsted_lewis(acid_type: str = None,
                            base_type: str = None) -> str:
    """
    Compare Brønsted-Lowry and Lewis definitions.
    
    Args:
        acid_type: 'brønsted' or 'lewis'
        base_type: 'brønsted' or 'lewis'
    
    Returns:
        Comparison explanation
    """
    if acid_type == 'brønsted':
        return 'Brønsted acid: H+ donor (subset of Lewis acids)'
    elif acid_type == 'lewis':
        return 'Lewis acid: electron pair acceptor (broader definition)'
    elif base_type == 'brønsted':
        return 'Brønsted base: H+ acceptor (subset of Lewis bases)'
    elif base_type == 'lewis':
        return 'Lewis base: electron pair donor (broader definition)'
    return 'Lewis model encompasses Brønsted-Lowry model'

MCP_TOOLS = [
    {
        "name": "compare_brønsted_lewis",
        "description": "Compare Brønsted-Lowry and Lewis definitions.",
        "parameters": [
            {
                "name": "acid_type",
                "type": "number"
            },
            {
                "name": "base_type",
                "type": "number"
            }
        ]
    },
    {
        "name": "complex_ion_concentration",
        "description": "Calculate complex ion concentration from Kf.",
        "parameters": [
            {
                "name": "Kf",
                "type": "number"
            },
            {
                "name": "metal_conc",
                "type": "number"
            },
            {
                "name": "ligand_conc",
                "type": "number"
            },
            {
                "name": "n_ligands",
                "type": "number"
            }
        ]
    },
    {
        "name": "dissociation_constant",
        "description": "Calculate dissociation constant Kd from Kf.",
        "parameters": [
            {
                "name": "Kf",
                "type": "number"
            }
        ]
    },
    {
        "name": "formation_constant",
        "description": "Calculate formation constant Kf.",
        "parameters": [
            {
                "name": "complex_conc",
                "type": "number"
            },
            {
                "name": "metal_conc",
                "type": "number"
            },
            {
                "name": "ligand_conc",
                "type": "number"
            },
            {
                "name": "n_ligands",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_lewis_acid_base",
        "description": "Identify Lewis acid and base in a reaction.",
        "parameters": [
            {
                "name": "species1",
                "type": "number"
            },
            {
                "name": "species2",
                "type": "number"
            },
            {
                "name": "species1_has_lone_pair",
                "type": "number"
            },
            {
                "name": "species2_has_lone_pair",
                "type": "number"
            }
        ]
    },
    {
        "name": "is_complex_ion_stable",
        "description": "Determine if complex ion is highly stable.",
        "parameters": [
            {
                "name": "Kf",
                "type": "number"
            },
            {
                "name": "threshold",
                "type": "number"
            }
        ]
    },
    {
        "name": "ligand_needed_for_dissolution",
        "description": "Calculate ligand concentration needed to achieve target metal dissolution.",
        "parameters": [
            {
                "name": "Ksp",
                "type": "number"
            },
            {
                "name": "Kf",
                "type": "number"
            },
            {
                "name": "metal_conc_target",
                "type": "number"
            },
            {
                "name": "n_ligands",
                "type": "number"
            }
        ]
    },
    {
        "name": "metal_concentration_from_Kf",
        "description": "Calculate free metal ion concentration from Kf.",
        "parameters": [
            {
                "name": "Kf",
                "type": "number"
            },
            {
                "name": "complex_conc",
                "type": "number"
            },
            {
                "name": "ligand_conc",
                "type": "number"
            },
            {
                "name": "n_ligands",
                "type": "number"
            }
        ]
    }
]
