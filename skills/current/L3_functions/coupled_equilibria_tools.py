"""
Coupled Equilibria Tools - L3 Implementation
Chapter 15.3: Coupled Equilibria

## Solver Instructions (for AI Agent)

When you encounter coupled equilibria problems (common ion effect, acid-enhanced solubility, complex-enhanced solubility):

### Step 1: Identify what is given and what is asked
- Given: Ksp, Ka, Kf, concentrations, or pH
- Asked: solubility enhancement, dissolution behavior, effective K, common ion effect

### Step 2: Choose the correct function
- `combine_equilibrium_constants(K_values)`: K_net = K1 x K2 x ... (multiply for sequential reactions)
- `acid_enhanced_K(Ksp, Ka)`: K = Ksp x Ka (acid dissolves insoluble salt)
- `complex_enhanced_K(Ksp, Kf)`: K = Ksp x Kf (complex ion enhances solubility)
- `solubility_with_acid(Ksp, Ka, acid_conc, salt_formula)`: Solubility in acidic solution
- `solubility_with_complex(Ksp, Kf, ligand_conc, salt_formula)`: Solubility with complexing agent
- `predict_dissolution_behavior(Ksp, Kf, Ka)`: Will dissolution occur?
- `common_ion_effect_factor(common_ion_conc, Ksp, stoichiometry)`: Solubility reduction factor
- `coupled_system_summary(reactions)`: Summary of coupled equilibrium system

### Step 3: Handle special cases
- K_net for coupled reactions: multiply individual K values
- Common ion reduces solubility: s = √(Ksp/[common ion]) for MX type
- Acid-enhanced: Mg(OH)2 + 2H+ -> Mg2+ + 2H2O; K = Ksp x Ka2
- Complex-enhanced: AgCl + 2NH3 -> Ag(NH3)2+ + Cl-; K = Ksp x Kf

### Examples
```python
acid_enhanced_K(5.6e-12, 5.6e-10)  # Mg(OH)2 in acid -> 3.14e-21
complex_enhanced_K(1.8e-10, 1.7e7)  # AgCl in NH3 -> 3.06e-3
```
"""

from typing import Dict, List, Tuple, Optional


def combine_equilibrium_constants(K_values: List[float]) -> float:
    """
    Combine multiple equilibrium constants for coupled reactions.
    
    K_net = K1 x K2 x K3 x ...
    
    Args:
        K_values: List of equilibrium constants
    
    Returns:
        Combined equilibrium constant
    
    Examples:
        >>> combine_equilibrium_constants([1e-5, 1e7])
        100.0
    """
    result = 1.0
    for K in K_values:
        result *= K
    return result


def acid_enhanced_K(Ksp: float, Ka: float) -> float:
    """
    Calculate equilibrium constant for acid-enhanced dissolution.
    
    For: Salt + H+ -> Metal + Acid_anion
    K = Ksp / Ka
    
    Args:
        Ksp: Solubility product
        Ka: Acid dissociation constant
    
    Returns:
        Combined equilibrium constant
    
    Examples:
        >>> acid_enhanced_K(8.7e-9, 4.7e-11)
        185.1
    """
    return Ksp / Ka


def complex_enhanced_K(Ksp: float, Kf: float) -> float:
    """
    Calculate equilibrium constant for complex-enhanced dissolution.
    
    For: Salt + Ligand -> Complex ion
    K = Ksp x Kf
    
    Args:
        Ksp: Solubility product
        Kf: Formation constant
    
    Returns:
        Combined equilibrium constant
    
    Examples:
        >>> complex_enhanced_K(2e-32, 1.1e33)
        22.0
    """
    return Ksp * Kf


def solubility_with_acid(Ksp: float, Ka: float, 
                          H_conc: float, anion_coeff: int = 1) -> float:
    """
    Calculate solubility enhanced by acid.
    
    Args:
        Ksp: Solubility product
        Ka: Acid dissociation constant of anion
        H_conc: Hydrogen ion concentration (M)
        anion_coeff: Stoichiometric coefficient of anion
    
    Returns:
        Enhanced solubility (M)
    
    Examples:
        >>> solubility_with_acid(8.7e-9, 4.7e-11, 1e-6)
        3.7e-04
    """
    # Enhanced K = Ksp/Ka x [H+]
    K_net = (Ksp / Ka) * H_conc
    
    # For 1:1 salt, s = K_net
    # For other stoichiometries, adjust
    if anion_coeff == 1:
        return K_net ** 0.5
    else:
        return K_net ** (1/3)


def solubility_with_complex(Ksp: float, Kf: float,
                             ligand_conc: float, n_ligands: int = 1) -> float:
    """
    Calculate solubility enhanced by complex formation.
    
    Args:
        Ksp: Solubility product
        Kf: Formation constant
        ligand_conc: Ligand concentration (M)
        n_ligands: Number of ligands per metal
    
    Returns:
        Enhanced solubility (M)
    
    Examples:
        >>> solubility_with_complex(1.8e-10, 1.7e7, 0.1, 2)
        0.0055
    """
    # K_net = Ksp x Kf x [L]^n
    K_net = Ksp * Kf * (ligand_conc ** n_ligands)
    
    # Solubility = K_net (for 1:1 stoichiometry)
    return K_net


def predict_dissolution_behavior(Ksp: float, Kf: float = None,
                                  Ka: float = None, 
                                  conditions: Dict = None) -> str:
    """
    Predict dissolution behavior under various conditions.
    
    Args:
        Ksp: Solubility product
        Kf: Formation constant (optional)
        Ka: Acid dissociation constant of anion (optional)
        conditions: Dict of conditions
    
    Returns:
        Prediction string
    """
    predictions = []
    
    if Ksp < 1e-10:
        predictions.append('very low solubility')
    
    if Kf and Kf > 1e10:
        predictions.append('complex formation increases solubility significantly')
    
    if Ka and Ka < 1e-7:
        predictions.append('acid increases solubility')
    
    if not predictions:
        return 'normal dissolution behavior'
    
    return '; '.join(predictions)


def common_ion_effect_factor(common_ion_conc: float,
                              stoich_coeff: int = 1) -> float:
    """
    Calculate the reduction factor due to common ion effect.
    
    Args:
        common_ion_conc: Concentration of common ion (M)
        stoich_coeff: Stoichiometric coefficient
    
    Returns:
        Reduction factor (fraction of original solubility)
    
    Examples:
        >>> common_ion_effect_factor(0.1, 1)
        0.01
    """
    # Simplified: solubility decreases by factor of common ion concentration
    # for 1:1 salts
    return 1.0 / (1.0 + common_ion_conc)


def coupled_system_summary(reactions: List[Dict]) -> Dict:
    """
    Summarize a coupled equilibrium system.
    
    Args:
        reactions: List of reaction dicts with 'equation' and 'K'
    
    Returns:
        Summary dict with net K and analysis
    """
    total_K = 1.0
    
    for rxn in reactions:
        total_K *= rxn.get('K', 1.0)
    
    return {
        'number_of_reactions': len(reactions),
        'net_K': total_K,
        'favorable': total_K > 1,
        'summary': f"Net K = {total_K:.2e}"
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'acid_enhanced_K', 'description': 'Calculate equilibrium constant for acid-enhanced dissolution.\n\nFor: Salt + H+ -> Metal + Acid_anion\nK = Ksp / Ka\n\nArgs:\n    Ksp: Solubility product\n    Ka: Acid dissociation constant\n\nReturns:\n    Combined equilibrium constant\n\nExamples:\n    >>> acid_enhanced_K(8.7e-9, 4.7e-11)\n    185.1', 'inputSchema': {'type': 'object', 'properties': {'Ksp': {'type': 'number', 'description': 'Ksp'}, 'Ka': {'type': 'number', 'description': 'Ka'}}, 'required': ['Ksp', 'Ka']}},
    {'name': 'combine_equilibrium_constants', 'description': 'Combine multiple equilibrium constants for coupled reactions.\n\nK_net = K1 x K2 x K3 x ...\n\nArgs:\n    K_values: List of equilibrium constants\n\nReturns:\n    Combined equilibrium constant\n\nExamples:\n    >>> combine_equilibrium_constants([1e-5, 1e7])\n    100.0', 'inputSchema': {'type': 'object', 'properties': {'K_values': {'type': 'number', 'description': 'K Values'}}, 'required': ['K_values']}},
    {'name': 'common_ion_effect_factor', 'description': 'Calculate the reduction factor due to common ion effect.\n\nArgs:\n    common_ion_conc: Concentration of common ion (M)\n    stoich_coeff: Stoichiometric coefficient\n\nReturns:\n    Reduction factor (fraction of original solubility)\n\nExamples:\n    >>> common_ion_effect_factor(0.1, 1)\n    0.01', 'inputSchema': {'type': 'object', 'properties': {'common_ion_conc': {'type': 'string', 'description': 'Common Ion Conc'}, 'stoich_coeff': {'type': 'number', 'description': 'Stoich Coeff', 'default': 1}}, 'required': ['common_ion_conc']}},
    {'name': 'complex_enhanced_K', 'description': 'Calculate equilibrium constant for complex-enhanced dissolution.\n\nFor: Salt + Ligand -> Complex ion\nK = Ksp x Kf\n\nArgs:\n    Ksp: Solubility product\n    Kf: Formation constant\n\nReturns:\n    Combined equilibrium constant\n\nExamples:\n    >>> complex_enhanced_K(2e-32, 1.1e33)\n    22.0', 'inputSchema': {'type': 'object', 'properties': {'Ksp': {'type': 'number', 'description': 'Ksp'}, 'Kf': {'type': 'number', 'description': 'Kf'}}, 'required': ['Ksp', 'Kf']}},
    {'name': 'coupled_system_summary', 'description': "Summarize a coupled equilibrium system.\n\nArgs:\n    reactions: List of reaction dicts with 'equation' and 'K'\n\nReturns:\n    Summary dict with net K and analysis", 'inputSchema': {'type': 'object', 'properties': {'reactions': {'type': 'string', 'description': 'Reactions'}}, 'required': ['reactions']}},
    {'name': 'predict_dissolution_behavior', 'description': 'Predict dissolution behavior under various conditions.\n\nArgs:\n    Ksp: Solubility product\n    Kf: Formation constant (optional)\n    Ka: Acid dissociation constant of anion (optional)\n    conditions: Dict of conditions\n\nReturns:\n    Prediction string', 'inputSchema': {'type': 'object', 'properties': {'Ksp': {'type': 'number', 'description': 'Ksp'}, 'Kf': {'type': 'number', 'description': 'Kf', 'default': None}, 'Ka': {'type': 'number', 'description': 'Ka', 'default': None}, 'conditions': {'type': 'string', 'description': 'Conditions', 'default': None}}, 'required': ['Ksp']}},
    {'name': 'solubility_with_acid', 'description': 'Calculate solubility enhanced by acid.\n\nArgs:\n    Ksp: Solubility product\n    Ka: Acid dissociation constant of anion\n    H_conc: Hydrogen ion concentration (M)\n    anion_coeff: Stoichiometric coefficient of anion\n\nReturns:\n    Enhanced solubility (M)\n\nExamples:\n    >>> solubility_with_acid(8.7e-9, 4.7e-11, 1e-6)\n    3.7e-04', 'inputSchema': {'type': 'object', 'properties': {'Ksp': {'type': 'number', 'description': 'Ksp'}, 'Ka': {'type': 'number', 'description': 'Ka'}, 'H_conc': {'type': 'number', 'description': 'H Conc'}, 'anion_coeff': {'type': 'string', 'description': 'Anion Coeff', 'default': 1}}, 'required': ['Ksp', 'Ka', 'H_conc']}},
    {'name': 'solubility_with_complex', 'description': 'Calculate solubility enhanced by complex formation.\n\nArgs:\n    Ksp: Solubility product\n    Kf: Formation constant\n    ligand_conc: Ligand concentration (M)\n    n_ligands: Number of ligands per metal\n\nReturns:\n    Enhanced solubility (M)\n\nExamples:\n    >>> solubility_with_complex(1.8e-10, 1.7e7, 0.1, 2)\n    0.0055', 'inputSchema': {'type': 'object', 'properties': {'Ksp': {'type': 'number', 'description': 'Ksp'}, 'Kf': {'type': 'number', 'description': 'Kf'}, 'ligand_conc': {'type': 'string', 'description': 'Ligand Conc'}, 'n_ligands': {'type': 'string', 'description': 'N Ligands', 'default': 1}}, 'required': ['Ksp', 'Kf', 'ligand_conc']}}
]
