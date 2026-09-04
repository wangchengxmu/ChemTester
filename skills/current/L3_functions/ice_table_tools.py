"""
ICE Table Tools - L3 Implementation
Chapter 13.4: Equilibrium Calculations

## Solver Instructions (for AI Agent)

When you encounter an ICE table problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Initial concentrations: Starting values for all species
- Equilibrium constant K: Given value
- Balanced equation: Extract coefficients
- Change variable x: What changes occur
- Equilibrium concentrations: What to find

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Build ICE table structure | `build_ice_table(species, coefficients, initial, is_reactant)` |
| Solve simple ICE (A ⇌ nB) | `ice_table_simple(K, initial_reactant, coeff_reactant, coeff_product)` |
| Solve quadratic equation | `solve_quadratic(a, b, c)` |
| Use small K approximation | `small_k_approximation(K, initial)` |
| Check if approximation valid | `check_approximation_valid(K, initial, x, threshold)` |
| Calculate stoichiometric changes | `stoichiometric_changes(x, coefficients, is_reactant)` |
| Find equilibrium from initial and changes | `equilibrium_from_initial(initial, changes)` |
| Verify equilibrium satisfies K | `verify_equilibrium(equilibrium, K, products, reactants)` |

### Step 3: Handle special cases
- **Small K approximation**: Valid when K x initial << 1, simplifies math
- **Quadratic solutions**: May need to reject negative or physically impossible roots
- **Change direction**: Reactants decrease (-), products increase (+)
- **5% rule**: Approximation valid if x/initial < 0.05 (5%)

### Examples

**Example 1: Simple ICE table**
Question: "For A ⇌ B with K = 0.02 and initial [A] = 1.0 M, find equilibrium concentrations."
- Given: K = 0.02, initial_reactant = 1.0, coeff_reactant = 1, coeff_product = 1
- Solution: `ice_table_simple(K=0.02, initial_reactant=1.0, coeff_reactant=1, coeff_product=1)` -> {'reactant': 0.85, 'product': 0.15}

**Example 2: Quadratic solution**
Question: "Solve x2/(1-x) = 0.5 where initial = 1.0 M."
- This gives: x2 = 0.5(1-x) -> x2 + 0.5x - 0.5 = 0
- Solution: `solve_quadratic(a=1, b=0.5, c=-0.5)` -> x = 0.5 (positive root)

**Example 3: Check approximation**
Question: "Is the small K approximation valid if x = 0.032 and initial = 1.0?"
- Solution: `check_approximation_valid(K=0.001, initial=1.0, x=0.032)` -> True (3.2% < 5%)

**Example 4: Verify equilibrium**
Question: "Verify [HI] = 0.78, [H2] = 0.11, [I2] = 0.11 satisfies K = 50."
- Solution: `verify_equilibrium({'HI': 0.78, 'H2': 0.11, 'I2': 0.11}, K=50, products={'HI': 2}, reactants={'H2': 1, 'I2': 1})` -> True
"""

from typing import Dict, List, Tuple, Optional
from math import sqrt


def build_ice_table(species: List[str], 
                    coefficients: Dict[str, int],
                    initial: Dict[str, float],
                    is_reactant: Dict[str, bool]) -> Dict:
    """
    Build ICE table structure.
    
    Args:
        species: List of species names
        coefficients: Dict of {species: coefficient}
        initial: Dict of {species: initial concentration}
        is_reactant: Dict of {species: is_reactant}
    
    Returns:
        Dict with ICE table data
    
    Examples:
        >>> build_ice_table(['N2', 'H2', 'NH3'], {'N2': 1, 'H2': 3, 'NH3': 2},
        ...                 {'N2': 1.0, 'H2': 3.0, 'NH3': 0},
        ...                 {'N2': True, 'H2': True, 'NH3': False})
        {'species': ['N2', 'H2', 'NH3'], 'initial': {...}, ...}
    """
    table = {
        'species': species,
        'initial': {s: initial.get(s, 0) for s in species},
        'change': {},
        'equilibrium': {}
    }
    
    # Set up change expressions
    reference = None
    for s in species:
        if is_reactant[s]:
            table['change'][s] = f"-{coefficients[s]}x"
        else:
            table['change'][s] = f"+{coefficients[s]}x"
    
    return table


def solve_quadratic(a: float, b: float, c: float) -> Tuple[float, float]:
    """
    Solve quadratic equation ax2 + bx + c = 0.
    
    Args:
        a, b, c: Coefficients
    
    Returns:
        (root1, root2) - only positive root is physically meaningful
    
    Examples:
        >>> solve_quadratic(1, -3, 2)
        (2.0, 1.0)
    """
    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return (None, None)
    
    sqrt_disc = sqrt(discriminant)
    root1 = (-b + sqrt_disc) / (2 * a)
    root2 = (-b - sqrt_disc) / (2 * a)
    
    return (root1, root2)


def ice_table_simple(K: float, initial_reactant: float,
                      coeff_reactant: int, coeff_product: int) -> Dict:
    """
    Solve simple ICE table for A ⇌ nB (one reactant, one product).
    
    Args:
        K: Equilibrium constant
        initial_reactant: Initial concentration of reactant
        coeff_reactant: Coefficient of reactant
        coeff_product: Coefficient of product
    
    Returns:
        Dict with equilibrium concentrations
    
    Examples:
        >>> ice_table_simple(0.02, 1.0, 1, 2)
        {'reactant': 0.85, 'product': 0.30}
    """
    # A ⇌ nB
    # K = [B]^n / [A]
    # ICE: A = C0 - x, B = nx
    
    # For K = (nx)^n / (C0 - x)
    # Simple case n=1: K = x / (C0 - x)
    # x = K*C0 / (1 + K)
    
    if coeff_product == 1:
        x = K * initial_reactant / (1 + K)
        return {
            'reactant': initial_reactant - x,
            'product': x,
            'x': x
        }
    
    # For n=2: K = (2x)^2 / (C0 - x) = 4x2 / (C0 - x)
    # 4x2 + Kx - K*C0 = 0
    if coeff_product == 2:
        a = 4
        b = K
        c = -K * initial_reactant
        
        root1, root2 = solve_quadratic(a, b, c)
        x = root1 if root1 and root1 > 0 and initial_reactant - root1 > 0 else root2
        
        return {
            'reactant': initial_reactant - x,
            'product': 2 * x,
            'x': x
        }
    
    return {'error': 'Complex case - use general solver'}


def small_k_approximation(K: float, initial: float) -> float:
    """
    Use small K approximation to find x.
    
    Valid when K x initial << 1.
    
    Args:
        K: Equilibrium constant
        initial: Initial concentration
    
    Returns:
        Approximate x value
    
    Examples:
        >>> small_k_approximation(0.001, 1.0)
        0.032
    """
    return sqrt(K * initial)


def check_approximation_valid(K: float, initial: float, 
                               x: float, threshold: float = 0.05) -> bool:
    """
    Check if small K approximation is valid.
    
    Args:
        K: Equilibrium constant
        initial: Initial concentration
        x: Calculated x value
        threshold: Maximum acceptable error (default 5%)
    
    Returns:
        True if approximation valid
    
    Examples:
        >>> check_approximation_valid(0.001, 1.0, 0.032)
        True
    """
    return x / initial < threshold


def stoichiometric_changes(x: float, 
                            coefficients: Dict[str, int],
                            is_reactant: Dict[str, bool]) -> Dict[str, float]:
    """
    Calculate concentration changes from x.
    
    Args:
        x: Change variable
        coefficients: Species coefficients
        is_reactant: Whether each species is reactant
    
    Returns:
        Dict of concentration changes
    
    Examples:
        >>> stoichiometric_changes(0.1, {'N2': 1, 'H2': 3, 'NH3': 2},
        ...                        {'N2': True, 'H2': True, 'NH3': False})
        {'N2': -0.1, 'H2': -0.3, 'NH3': 0.2}
    """
    changes = {}
    for species, coeff in coefficients.items():
        if is_reactant[species]:
            changes[species] = -coeff * x
        else:
            changes[species] = coeff * x
    return changes


def equilibrium_from_initial(initial: Dict[str, float],
                              changes: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate equilibrium concentrations from initial and changes.
    
    Args:
        initial: Initial concentrations
        changes: Concentration changes
    
    Returns:
        Equilibrium concentrations
    
    Examples:
        >>> equilibrium_from_initial({'A': 1.0, 'B': 0}, {'A': -0.2, 'B': 0.2})
        {'A': 0.8, 'B': 0.2}
    """
    equilibrium = {}
    for species in initial:
        equilibrium[species] = initial[species] + changes.get(species, 0)
    return equilibrium


def verify_equilibrium(equilibrium: Dict[str, float],
                        K: float,
                        products: Dict[str, int],
                        reactants: Dict[str, int]) -> bool:
    """
    Verify equilibrium concentrations satisfy K.
    
    Args:
        equilibrium: Equilibrium concentrations
        K: Equilibrium constant
        products: Product coefficients
        reactants: Reactant coefficients
    
    Returns:
        True if Q ~ K
    
    Examples:
        >>> verify_equilibrium({'HI': 0.78, 'H2': 0.11, 'I2': 0.11}, 50.0,
        ...                    {'HI': 2}, {'H2': 1, 'I2': 1})
        True
    """
    from equilibrium_constant_tools import calculate_Kc
    
    Q = calculate_Kc(equilibrium, products, reactants)
    
    # Allow 1% tolerance
    return abs(Q - K) / K < 0.01

MCP_TOOLS = [
    {
        "name": "build_ice_table",
        "description": "Build ICE table structure.",
        "parameters": [
            {
                "name": "species",
                "type": "number"
            },
            {
                "name": "coefficients",
                "type": "number"
            },
            {
                "name": "initial",
                "type": "number"
            },
            {
                "name": "is_reactant",
                "type": "boolean"
            }
        ]
    },
    {
        "name": "check_approximation_valid",
        "description": "Check if small K approximation is valid.",
        "parameters": [
            {
                "name": "K",
                "type": "number"
            },
            {
                "name": "initial",
                "type": "number"
            },
            {
                "name": "x",
                "type": "number"
            },
            {
                "name": "threshold",
                "type": "number"
            }
        ]
    },
    {
        "name": "equilibrium_from_initial",
        "description": "Calculate equilibrium concentrations from initial and changes.",
        "parameters": [
            {
                "name": "initial",
                "type": "number"
            },
            {
                "name": "changes",
                "type": "number"
            }
        ]
    },
    {
        "name": "ice_table_simple",
        "description": "Solve simple ICE table for A ⇌ nB (one reactant, one product).",
        "parameters": [
            {
                "name": "K",
                "type": "number"
            },
            {
                "name": "initial_reactant",
                "type": "number"
            },
            {
                "name": "coeff_reactant",
                "type": "number"
            },
            {
                "name": "coeff_product",
                "type": "number"
            }
        ]
    },
    {
        "name": "small_k_approximation",
        "description": "Use small K approximation to find x.",
        "parameters": [
            {
                "name": "K",
                "type": "number"
            },
            {
                "name": "initial",
                "type": "number"
            }
        ]
    },
    {
        "name": "solve_quadratic",
        "description": "Solve quadratic equation ax2 + bx + c = 0.",
        "parameters": [
            {
                "name": "a",
                "type": "number"
            },
            {
                "name": "b",
                "type": "number"
            },
            {
                "name": "c",
                "type": "number"
            }
        ]
    },
    {
        "name": "stoichiometric_changes",
        "description": "Calculate concentration changes from x.",
        "parameters": [
            {
                "name": "x",
                "type": "number"
            },
            {
                "name": "coefficients",
                "type": "number"
            },
            {
                "name": "is_reactant",
                "type": "boolean"
            }
        ]
    },
    {
        "name": "verify_equilibrium",
        "description": "Verify equilibrium concentrations satisfy K.",
        "parameters": [
            {
                "name": "equilibrium",
                "type": "number"
            },
            {
                "name": "K",
                "type": "number"
            },
            {
                "name": "products",
                "type": "number"
            },
            {
                "name": "reactants",
                "type": "number"
            }
        ]
    }
]
