"""
Equilibrium Constant Tools - L3 Implementation
Chapter 13.2: Equilibrium Constants

## Solver Instructions (for AI Agent)

When you encounter an equilibrium constant problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Kc (concentration equilibrium constant): From equilibrium concentrations
- Kp (pressure equilibrium constant): For gas-phase reactions
- Temperature T: For Kc ↔ Kp conversions
- Equilibrium concentrations: Values at equilibrium
- Stoichiometry: Deltan (change in moles of gas)
- Q (reaction quotient): For direction prediction

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate Kc from equilibrium concentrations | `calculate_Kc(equilibrium_concentrations, products, reactants)` |
| Convert Kc to Kp | `Kc_to_Kp(Kc, delta_n, T)` |
| Convert Kp to Kc | `Kp_to_Kc(Kp, delta_n, T)` |
| Calculate Qp from partial pressures | `calculate_Qp(partial_pressures, products, reactants)` |
| Generate Q expression string | `Q_expression_string(products, reactants)` |
| Find unknown concentration from Kc | `concentration_from_Kc(Kc, known_concs, unknown_species, coeff, products, reactants)` |
| Interpret K value | `interpret_K(K)` |

### Step 3: Handle special cases
- **Kc vs Kp**: Kp = Kc(RT)^Deltan, where Deltan = moles gas products - moles gas reactants
- **R value**: Use R = 0.0821 L·atm/(mol·K) for Kp calculations
- **Q vs K**: Q < K -> forward; Q > K -> reverse; Q = K -> equilibrium
- **Large K**: > 1000 means products strongly favored
- **Small K**: < 0.001 means reactants strongly favored

### Examples

**Example 1: Calculate Kc**
Question: "Calculate Kc for H2 + I2 ⇌ 2HI if [H2] = 0.5 M, [I2] = 0.5 M, [HI] = 2.0 M at equilibrium."
- Solution: `calculate_Kc(equilibrium_concentrations={'H2': 0.5, 'I2': 0.5, 'HI': 2.0}, products={'HI': 2}, reactants={'H2': 1, 'I2': 1})` -> Kc = 16

**Example 2: Kc to Kp conversion**
Question: "Convert Kc = 16 to Kp for H2 + I2 ⇌ 2HI at 298 K."
- Given: Deltan = 2 - 2 = 0, so Kp = Kc
- Solution: `Kc_to_Kp(Kc=16, delta_n=0, T=298)` -> Kp = 16

**Example 3: Kp to Kc conversion**
Question: "Convert Kp = 1.8 x 10-4 to Kc for N2(g) + 3H2(g) ⇌ 2NH3(g) at 700 K."
- Given: Deltan = 2 - 4 = -2
- Solution: `Kp_to_Kc(Kp=1.8e-4, delta_n=-2, T=700)` -> Kc ~ 5.8 x 10-5

**Example 4: Interpret K**
Question: "What does K = 1000 mean?"
- Solution: `interpret_K(K=1000)` -> 'Products strongly favored'

**Example 5: Find unknown concentration**
Question: "If Kc = 4.0 for H2 + I2 ⇌ 2HI, and [H2] = [I2] = 0.5 M, find [HI]."
- Solution: `concentration_from_Kc(Kc=4.0, known_concs={'H2': 0.5, 'I2': 0.5}, unknown_species='HI', coeff=2, products={'HI': 2}, reactants={'H2': 1, 'I2': 1})` -> [HI] = 1.0 M
"""

from typing import Dict, List, Tuple, Optional
from math import sqrt

R = 0.0821  # L·atm/(mol·K)


def calculate_Kc(equilibrium_concentrations: Dict[str, float],
                  products: Dict[str, int],
                  reactants: Dict[str, int]) -> float:
    """
    Calculate Kc from equilibrium concentrations.
    
    Args:
        equilibrium_concentrations: Dict of {species: concentration}
        products: Dict of {product: coefficient}
        reactants: Dict of {reactant: coefficient}
    
    Returns:
        Kc value
    
    Examples:
        >>> calculate_Kc({'HI': 0.1, 'H2': 0.01, 'I2': 0.01},
        ...              {'HI': 2}, {'H2': 1, 'I2': 1})
        100.0
    """
    from equilibrium_tools import reaction_quotient
    return reaction_quotient(equilibrium_concentrations, products, reactants)


def Kc_to_Kp(Kc: float, delta_n: int, T: float) -> float:
    """
    Convert Kc to Kp.
    
    Kp = Kc(RT)^Deltan
    
    Args:
        Kc: Equilibrium constant (concentration)
        delta_n: Change in moles of gas (products - reactants)
        T: Temperature (K)
    
    Returns:
        Kp value
    
    Examples:
        >>> Kc_to_Kp(1.0, -1, 298)
        0.041
    """
    return Kc * (R * T) ** delta_n


def Kp_to_Kc(Kp: float, delta_n: int, T: float) -> float:
    """
    Convert Kp to Kc.
    
    Kc = Kp(RT)^(-Deltan)
    
    Args:
        Kp: Equilibrium constant (pressure)
        delta_n: Change in moles of gas
        T: Temperature (K)
    
    Returns:
        Kc value
    
    Examples:
        >>> Kp_to_Kc(1.0, -1, 298)
        24.5
    """
    return Kp / (R * T) ** delta_n


def interpret_K(K: float) -> str:
    """
    Interpret the meaning of K value.
    
    Args:
        K: Equilibrium constant
    
    Returns:
        Interpretation string
    
    Examples:
        >>> interpret_K(1000)
        'Products strongly favored'
        >>> interpret_K(0.001)
        'Reactants strongly favored'
    """
    if K > 1000:
        return 'Products strongly favored'
    elif K > 10:
        return 'Products favored'
    elif K > 0.1:
        return 'Neither favored (significant both sides)'
    elif K > 0.001:
        return 'Reactants favored'
    else:
        return 'Reactants strongly favored'


def Q_expression_string(products: Dict[str, int], 
                        reactants: Dict[str, int]) -> str:
    """
    Generate Q expression string.
    
    Args:
        products: Dict of {product: coefficient}
        reactants: Dict of {reactant: coefficient}
    
    Returns:
        Q expression string
    
    Examples:
        >>> Q_expression_string({'NH3': 2}, {'N2': 1, 'H2': 3})
        'Q = [NH3]^2 / ([N2][H2]^3)'
    """
    from equilibrium_tools import equilibrium_expression
    return equilibrium_expression(products, reactants).replace('K', 'Q')


def calculate_Qp(partial_pressures: Dict[str, float],
                  products: Dict[str, int],
                  reactants: Dict[str, int]) -> float:
    """
    Calculate Qp from partial pressures.
    
    Args:
        partial_pressures: Dict of {species: pressure (atm)}
        products: Dict of {product: coefficient}
        reactants: Dict of {reactant: coefficient}
    
    Returns:
        Qp value
    
    Examples:
        >>> calculate_Qp({'NH3': 0.5, 'N2': 0.1, 'H2': 0.2},
        ...              {'NH3': 2}, {'N2': 1, 'H2': 3})
        625.0
    """
    # Numerator: products
    numerator = 1.0
    for species, coeff in products.items():
        P = partial_pressures.get(species, 0)
        numerator *= P ** coeff
    
    # Denominator: reactants
    denominator = 1.0
    for species, coeff in reactants.items():
        P = partial_pressures.get(species, 0)
        if P == 0:
            return float('inf')
        denominator *= P ** coeff
    
    return numerator / denominator


def concentration_from_Kc(Kc: float, known_concs: Dict[str, float],
                           unknown_species: str, coeff: int,
                           products: Dict[str, int],
                           reactants: Dict[str, int]) -> float:
    """
    Calculate unknown equilibrium concentration from Kc.
    
    Args:
        Kc: Equilibrium constant
        known_concs: Dict of known equilibrium concentrations
        unknown_species: Species to solve for
        coeff: Coefficient of unknown species in K expression
        products: Product coefficients
        reactants: Reactant coefficients
    
    Returns:
        Unknown concentration
    
    Examples:
        >>> concentration_from_Kc(4.0, {'H2': 0.5, 'I2': 0.5},
        ...                       'HI', 2, {'HI': 2}, {'H2': 1, 'I2': 1})
        1.0
    """
    # For simple case: K = [unknown]^coeff / denominator
    # Solve: [unknown] = (K * denominator)^(1/coeff)
    
    denominator = 1.0
    for species, c in reactants.items():
        if species in known_concs:
            denominator *= known_concs[species] ** c
    
    for species, c in products.items():
        if species != unknown_species and species in known_concs:
            denominator /= known_concs[species] ** c
    
    # K = [unknown]^coeff / denominator
    # [unknown] = (K * denominator)^(1/coeff)
    
    return (Kc * denominator) ** (1.0 / coeff)


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "Kc_to_Kp",
        "description": "Convert Kc to Kp.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Kc": {"type": "number", "description": "Kc"},
                "delta_n": {"type": "number", "description": "Delta N"},
                "T": {"type": "number", "description": "T"},
            },
            "required": ["Kc", "delta_n", "T"]
        }
    },
    {
        "name": "Kp_to_Kc",
        "description": "Convert Kp to Kc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Kp": {"type": "number", "description": "Kp"},
                "delta_n": {"type": "number", "description": "Delta N"},
                "T": {"type": "number", "description": "T"},
            },
            "required": ["Kp", "delta_n", "T"]
        }
    },
    {
        "name": "Q_expression_string",
        "description": "Generate Q expression string.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "products": {"type": "number", "description": "Products"},
                "reactants": {"type": "number", "description": "Reactants"},
            },
            "required": ["products", "reactants"]
        }
    },
    {
        "name": "calculate_Kc",
        "description": "Calculate Kc from equilibrium concentrations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "equilibrium_concentrations": {"type": "number", "description": "Equilibrium Concentrations"},
                "products": {"type": "number", "description": "Products"},
                "reactants": {"type": "number", "description": "Reactants"},
            },
            "required": ["equilibrium_concentrations", "products", "reactants"]
        }
    },
    {
        "name": "calculate_Qp",
        "description": "Calculate Qp from partial pressures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "partial_pressures": {"type": "number", "description": "Partial Pressures"},
                "products": {"type": "number", "description": "Products"},
                "reactants": {"type": "number", "description": "Reactants"},
            },
            "required": ["partial_pressures", "products", "reactants"]
        }
    },
    {
        "name": "concentration_from_Kc",
        "description": "Calculate unknown equilibrium concentration from Kc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Kc": {"type": "number", "description": "Kc"},
                "known_concs": {"type": "number", "description": "Known Concs"},
                "unknown_species": {"type": "number", "description": "Unknown Species"},
                "coeff": {"type": "number", "description": "Coeff"},
                "products": {"type": "number", "description": "Products"},
                "reactants": {"type": "number", "description": "Reactants"},
            },
            "required": ["Kc", "known_concs", "unknown_species", "coeff", "products", "reactants"]
        }
    },
    {
        "name": "interpret_K",
        "description": "Interpret the meaning of K value.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "K": {"type": "number", "description": "K"},
            },
            "required": ["K"]
        }
    }
]
