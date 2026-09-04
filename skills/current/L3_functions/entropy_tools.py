"""
Entropy Tools - L3 Implementation
Chapter 16.2: Entropy

## Solver Instructions (for AI Agent)

When you encounter an entropy problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Microstates (W): Number of possible arrangements
- Entropy change sign prediction: Look for phase changes, temperature changes, dissolution
- Standard entropies (Sdeg): Look for tables with J/mol·K values
- Reversible heat transfer: Look for q_rev and T
- Reaction entropy: Look for products and reactants with entropy values

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate entropy from microstates | `entropy_from_microstates(W)` |
| Calculate entropy change from microstates | `entropy_change_microstates(W_initial, W_final)` |
| Calculate entropy change from heat | `entropy_change_heat(q_rev, T)` |
| Predict entropy sign for phase change | `predict_entropy_sign_phase_change(initial_phase, final_phase)` |
| Calculate DeltaSdeg for reaction | `standard_entropy_change(S_products, S_reactants, coeffs_products, coeffs_reactants)` |
| Compare entropies of phases | `compare_entropies(['solid', 'liquid', 'gas'])` |

### Step 3: Handle special cases
- **Phase changes**: Melting, vaporization -> entropy increases; freezing, condensation -> entropy decreases
- **Standard entropy trends**: S(solid) < S(liquid) < S(gas); higher T -> higher S
- **Reaction entropy**: DeltaSdeg = ΣSdeg(products) - ΣSdeg(reactants) (multiply by coefficients)
- **Units**: Entropy is in J/mol·K (not kJ like enthalpy)
- **Reversible process**: DeltaS = q_rev/T for reversible heat transfer

### Examples

**Example 1: Entropy from microstates**
Question: "Calculate entropy when W = 100."
- Solution: `entropy_from_microstates(W=100)` -> 6.35 x 10-22 J/K

**Example 2: Predict entropy sign**
Question: "Predict the entropy change when ice melts."
- Given: solid -> liquid
- Solution: `predict_entropy_sign_phase_change('solid', 'liquid')` -> 'positive (entropy increases)'

**Example 3: Standard entropy change**
Question: "Calculate DeltaSdeg for H2(g) + ½O2(g) -> H2O(l) given Sdeg(H2)=130.7, Sdeg(O2)=205.2, Sdeg(H2O)=69.9 J/mol·K"
- Solution: `standard_entropy_change(S_products=[69.9], S_reactants=[130.7, 102.6], coeffs_products=[1], coeffs_reactants=[1, 1])` -> -163.4 J/K

**Example 4: Entropy change from heat**
Question: "Calculate DeltaS when 1000 J of heat is transferred reversibly at 298 K."
- Solution: `entropy_change_heat(q_rev=1000, T=298)` -> 3.36 J/K
"""

from typing import Dict, Tuple, Optional
from math import log


# Boltzmann constant (J/K)
K_BOLTZMANN = 1.38e-23


def entropy_from_microstates(W: float) -> float:
    """
    Calculate entropy from number of microstates using Boltzmann equation.
    
    S = k ln W
    
    Args:
        W: Number of microstates
    
    Returns:
        Entropy (J/K)
    
    Examples:
        >>> entropy_from_microstates(1)
        0.0
        >>> entropy_from_microstates(10)
        3.17e-23
    """
    if W <= 0:
        return 0.0
    return K_BOLTZMANN * log(W)


def entropy_change_microstates(W_initial: float, W_final: float) -> float:
    """
    Calculate entropy change from initial and final microstates.
    
    DeltaS = k ln(W_final/W_initial)
    
    Args:
        W_initial: Initial number of microstates
        W_final: Final number of microstates
    
    Returns:
        Entropy change (J/K)
    
    Examples:
        >>> entropy_change_microstates(1, 6)
        2.47e-23
    """
    if W_initial <= 0 or W_final <= 0:
        return 0.0
    return K_BOLTZMANN * log(W_final / W_initial)


def entropy_change_heat(q_rev: float, T: float) -> float:
    """
    Calculate entropy change from reversible heat transfer.
    
    DeltaS = q_rev / T
    
    Args:
        q_rev: Reversible heat transfer (J)
        T: Absolute temperature (K)
    
    Returns:
        Entropy change (J/K)
    
    Examples:
        >>> entropy_change_heat(1000, 298)
        3.36
    """
    if T <= 0:
        raise ValueError("Temperature must be positive")
    return q_rev / T


def predict_entropy_sign_phase_change(initial_phase: str, final_phase: str) -> str:
    """
    Predict sign of entropy change for phase transition.
    
    Args:
        initial_phase: 'solid', 'liquid', or 'gas'
        final_phase: 'solid', 'liquid', or 'gas'
    
    Returns:
        Sign prediction
    
    Examples:
        >>> predict_entropy_sign_phase_change('solid', 'liquid')
        'positive (entropy increases)'
    """
    entropy_order = {'solid': 1, 'liquid': 2, 'gas': 3}
    
    if initial_phase not in entropy_order or final_phase not in entropy_order:
        return 'unknown phases'
    
    initial_order = entropy_order[initial_phase]
    final_order = entropy_order[final_phase]
    
    if final_order > initial_order:
        return 'positive (entropy increases)'
    elif final_order < initial_order:
        return 'negative (entropy decreases)'
    else:
        return 'zero (no phase change)'


def standard_entropy_change(S_products: list, S_reactants: list,
                            coeffs_products: list = None,
                            coeffs_reactants: list = None) -> float:
    """
    Calculate standard entropy change for a reaction.
    
    DeltaSdeg = ΣνSdeg(products) - ΣνSdeg(reactants)
    
    Args:
        S_products: List of standard entropies for products (J/mol·K)
        S_reactants: List of standard entropies for reactants (J/mol·K)
        coeffs_products: Stoichiometric coefficients for products
        coeffs_reactants: Stoichiometric coefficients for reactants
    
    Returns:
        Standard entropy change (J/K)
    
    Examples:
        >>> standard_entropy_change([188.7], [69.9])
        118.8
    """
    if coeffs_products is None:
        coeffs_products = [1] * len(S_products)
    if coeffs_reactants is None:
        coeffs_reactants = [1] * len(S_reactants)
    
    sum_products = sum(c * s for c, s in zip(coeffs_products, S_products))
    sum_reactants = sum(c * s for c, s in zip(coeffs_reactants, S_reactants))
    
    return sum_products - sum_reactants


def compare_entropies(phases: list) -> str:
    """
    Compare relative entropies of different phases.
    
    Args:
        phases: List of phase names
    
    Returns:
        Comparison string
    
    Examples:
        >>> compare_entropies(['solid', 'liquid', 'gas'])
        'S(solid) < S(liquid) < S(gas)'
    """
    entropy_order = {'solid': 1, 'liquid': 2, 'gas': 3}
    sorted_phases = sorted(phases, key=lambda p: entropy_order.get(p, 0))
    return ' < '.join(f'S({p})' for p in sorted_phases)


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "compare_entropies",
        "description": "Compare relative entropies of different phases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phases": {"type": "number", "description": "Phases"},
            },
            "required": ["phases"]
        }
    },
    {
        "name": "entropy_change_heat",
        "description": "Calculate entropy change from reversible heat transfer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "q_rev": {"type": "number", "description": "Q Rev"},
                "T": {"type": "number", "description": "T"},
            },
            "required": ["q_rev", "T"]
        }
    },
    {
        "name": "entropy_change_microstates",
        "description": "Calculate entropy change from initial and final microstates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "W_initial": {"type": "number", "description": "W Initial"},
                "W_final": {"type": "number", "description": "W Final"},
            },
            "required": ["W_initial", "W_final"]
        }
    },
    {
        "name": "entropy_from_microstates",
        "description": "Calculate entropy from number of microstates using Boltzmann equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "W": {"type": "number", "description": "W"},
            },
            "required": ["W"]
        }
    },
    {
        "name": "predict_entropy_sign_phase_change",
        "description": "Predict sign of entropy change for phase transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "initial_phase": {"type": "number", "description": "Initial Phase"},
                "final_phase": {"type": "number", "description": "Final Phase"},
            },
            "required": ["initial_phase", "final_phase"]
        }
    },
    {
        "name": "standard_entropy_change",
        "description": "Calculate standard entropy change for a reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "S_products": {"type": "number", "description": "S Products"},
                "S_reactants": {"type": "number", "description": "S Reactants"},
                "coeffs_products": {"type": "number", "description": "Coeffs Products", "default": None},
                "coeffs_reactants": {"type": "number", "description": "Coeffs Reactants", "default": None},
            },
            "required": ["S_products", "S_reactants"]
        }
    }
]
