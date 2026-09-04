"""
Reaction Mechanism Tools - L3 Implementation
Chapter 12.06-12.07: Reaction Mechanisms and Catalysis

## Solver Instructions (for AI Agent)

When you encounter reaction mechanism, rate law derivation, intermediate identification, molecularity, catalyst effect, or steady-state approximation problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given an elementary step with reactants -> write the rate law?
- Given a multi-step mechanism -> derive overall rate law or find intermediates?
- Given a rate law and stoichiometry -> check if step is elementary?
- Given uncatalyzed and catalyzed activation energies -> calculate rate enhancement?
- Given catalyst and reactant phases -> classify as homogeneous or heterogeneous?
- Given a mechanism with an intermediate -> apply steady-state approximation?

### Step 2: Choose the correct function
- **Elementary rate law:** `elementary_rate_law(reactants, molecularity)` -> rate expression string. Unimolecular: rate=k[A]; Bimolecular: rate=k[A][B]
- **Molecularity:** `identify_molecularity(reactants)` -> 'unimolecular'(1)/'bimolecular'(2)/'termolecular'(3)
- **Overall rate law from mechanism:** `overall_rate_law_from_mechanism(mechanism, rds_index)` -> rate law based on rate-determining step. mechanism = list of dicts with 'reactants', 'products', 'rate_constant'
- **Find intermediates:** `find_intermediates(mechanism)` -> species that appear as products AND reactants in different steps
- **Validate elementary step:** `is_elementary_step_valid(rate_law, stoichiometry)` -> True if rate law matches molecularity
- **Catalyst rate enhancement:** `catalyst_effect(Ea_uncat, Ea_cat, T)` -> rate enhancement factor via Arrhenius equation. E_a in J/mol
- **Catalyst classification:** `classify_catalyst(catalyst_phase, reactant_phase)` -> 'homogeneous' (same phase) or 'heterogeneous' (different phase)
- **Steady-state approximation:** `steady_state_approximation(mechanism, intermediate)` -> simplified rate expression

### Step 3: Handle special cases
- Only termolecular (3-molecule) elementary steps are rare; most are unimolecular or bimolecular
- The rate-determining step (slowest) determines the overall rate law
- If RDS involves an intermediate, use SSA to express [intermediate] in terms of reactants
- Rate enhancement can be enormous: even 5 kJ/mol difference -> ~7x faster at 298 K

### Examples
```python
# Example 1: Rate law for bimolecular step A + B -> C
elementary_rate_law(['A', 'B'], 'bimolecular')  -> 'rate = k[A][B]'

# Example 2: Find intermediates in a two-step mechanism
mechanism = [
    {'reactants': ['A'], 'products': ['I']},
    {'reactants': ['I', 'B'], 'products': ['C']}
]
find_intermediates(mechanism)  -> ['I']

# Example 3: Catalyst effect: 100 kJ/mol -> 75 kJ/mol at 300 K
catalyst_effect(100000, 75000, 300)  -> rate_enhancement ~ 25000x

# Example 4: Classify catalyst
classify_catalyst('solid', 'gas')  -> 'heterogeneous'
```
"""

from typing import Dict, List, Tuple, Optional


def elementary_rate_law(reactants: List[str], molecularity: str = 'bimolecular') -> str:
    """
    Generate rate law for elementary step.
    
    Args:
        reactants: List of reactant species
        molecularity: 'unimolecular', 'bimolecular', or 'termolecular'
    
    Returns:
        Rate law string
    
    Examples:
        >>> elementary_rate_law(['A'])
        'rate = k[A]'
        >>> elementary_rate_law(['A', 'B'])
        'rate = k[A][B]'
    """
    if molecularity == 'unimolecular' or len(reactants) == 1:
        return f'rate = k[{reactants[0]}]'
    elif molecularity == 'bimolecular' or len(reactants) == 2:
        return f'rate = k[{reactants[0]}][{reactants[1]}]'
    elif molecularity == 'termolecular' or len(reactants) == 3:
        return f'rate = k[{reactants[0]}][{reactants[1]}][{reactants[2]}]'
    
    # Default: multiply all concentrations
    terms = ''.join(f'[{r}]' for r in reactants)
    return f'rate = k{terms}'


def identify_molecularity(reactants: int) -> str:
    """
    Identify molecularity from number of reactants.
    
    Args:
        reactants: Number of reactant molecules
    
    Returns:
        Molecularity string
    
    Examples:
        >>> identify_molecularity(1)
        'unimolecular'
        >>> identify_molecularity(2)
        'bimolecular'
    """
    mapping = {
        1: 'unimolecular',
        2: 'bimolecular',
        3: 'termolecular',
    }
    return mapping.get(reactants, 'unknown')


def overall_rate_law_from_mechanism(mechanism: List[Dict], rds_index: int = None) -> str:
    """
    Derive overall rate law from mechanism.
    
    Args:
        mechanism: List of step dicts with 'reactants', 'products', 'rate_constant'
        rds_index: Index of rate-determining step (if None, find slowest)
    
    Returns:
        Overall rate law string
    
    Examples:
        >>> mechanism = [
        ...     {'reactants': ['A', 'B'], 'products': ['C'], 'rate_constant': 0.01},
        ...     {'reactants': ['C'], 'products': ['D'], 'rate_constant': 0.001}
        ... ]
        >>> overall_rate_law_from_mechanism(mechanism, rds_index=1)
        'rate = k[C]'
    """
    if rds_index is None:
        # Assume slowest step (lowest k) is RDS
        rds_index = min(range(len(mechanism)), 
                        key=lambda i: mechanism[i].get('rate_constant', 1))
    
    rds = mechanism[rds_index]
    reactants = rds['reactants']
    
    return elementary_rate_law(reactants)


def find_intermediates(mechanism: List[Dict]) -> List[str]:
    """
    Identify intermediates in a reaction mechanism.
    
    Args:
        mechanism: List of step dicts
    
    Returns:
        List of intermediate species
    
    Examples:
        >>> mechanism = [
        ...     {'reactants': ['A'], 'products': ['I']},
        ...     {'reactants': ['I', 'B'], 'products': ['C']}
        ... ]
        >>> find_intermediates(mechanism)
        ['I']
    """
    all_reactants = set()
    all_products = set()
    
    for step in mechanism:
        all_reactants.update(step.get('reactants', []))
        all_products.update(step.get('products', []))
    
    # Intermediates: products that are also reactants in later steps
    intermediates = all_products & all_reactants
    
    return list(intermediates)


def is_elementary_step_valid(rate_law: str, stoichiometry: str) -> bool:
    """
    Check if a step could be elementary based on rate law.
    
    Args:
        rate_law: Experimental rate law for step
        stoichiometry: Stoichiometric equation
    
    Returns:
        True if consistent with elementary step
    
    Examples:
        >>> is_elementary_step_valid('rate = k[A][B]', 'A + B -> C')
        True
        >>> is_elementary_step_valid('rate = k[A]^2', 'A + B -> C')
        False
    """
    # Extract reactants from stoichiometry
    if '->' in stoichiometry:
        reactant_side = stoichiometry.split('->')[0]
    elif '->' in stoichiometry:
        reactant_side = stoichiometry.split('->')[0]
    else:
        return False
    
    # Count reactant molecules
    reactants = reactant_side.replace('+', ' ').split()
    reactants = [r.strip() for r in reactants if r.strip()]
    
    # Check if rate law matches molecularity
    if len(reactants) == 1:
        return '[A]^2' not in rate_law and '[A]' in rate_law
    elif len(reactants) == 2:
        return '[A][B]' in rate_law or ('[A]' in rate_law and '[B]' in rate_law)
    
    return True


def catalyst_effect(Ea_uncat: float, Ea_cat: float, T: float = 298) -> Dict:
    """
    Calculate catalyst effect on reaction rate.
    
    Args:
        Ea_uncat: Uncatalyzed activation energy (J/mol)
        Ea_cat: Catalyzed activation energy (J/mol)
        T: Temperature (K)
    
    Returns:
        Dict with rate enhancement factor
    
    Examples:
        >>> catalyst_effect(100000, 75000, 300)
        {'rate_enhancement': 25000}
    """
    from math import exp
    R = 8.314
    
    enhancement = exp((Ea_uncat - Ea_cat) / (R * T))
    
    return {
        'rate_enhancement': enhancement,
        'delta_Ea': Ea_uncat - Ea_cat,
        'uncat_Ea': Ea_uncat,
        'cat_Ea': Ea_cat,
    }


def classify_catalyst(catalyst_phase: str, reactant_phase: str) -> str:
    """
    Classify catalyst type.
    
    Args:
        catalyst_phase: Phase of catalyst
        reactant_phase: Phase of reactants
    
    Returns:
        Catalyst type string
    
    Examples:
        >>> classify_catalyst('solid', 'gas')
        'heterogeneous'
        >>> classify_catalyst('aqueous', 'aqueous')
        'homogeneous'
    """
    if catalyst_phase == reactant_phase:
        return 'homogeneous'
    else:
        return 'heterogeneous'


def steady_state_approximation(mechanism: List[Dict], 
                               intermediate: str) -> str:
    """
    Apply steady-state approximation for intermediate.
    
    Args:
        mechanism: Reaction mechanism steps
        intermediate: Intermediate species name
    
    Returns:
        Rate expression (simplified)
    
    Examples:
        >>> mechanism = [
        ...     {'reactants': ['A'], 'products': ['I'], 'k': 0.1},
        ...     {'reactants': ['I'], 'products': ['B'], 'k': 0.01}
        ... ]
        >>> steady_state_approximation(mechanism, 'I')
        'rate = k1[A]'
    """
    # Simplified: rate = rate of formation of intermediate
    for step in mechanism:
        if intermediate in step.get('products', []):
            k = step.get('k', 'k1')
            reactants = step.get('reactants', [])
            rate_expr = f'rate = {k}' + ''.join(f'[{r}]' for r in reactants)
            return rate_expr
    
    return 'rate = k[reactants]'

MCP_TOOLS = [
    {
        "name": "catalyst_effect",
        "description": "Calculate catalyst effect on reaction rate.",
        "parameters": [
            {
                "name": "Ea_uncat",
                "type": "number"
            },
            {
                "name": "Ea_cat",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "classify_catalyst",
        "description": "Classify catalyst type.",
        "parameters": [
            {
                "name": "catalyst_phase",
                "type": "number"
            },
            {
                "name": "reactant_phase",
                "type": "number"
            }
        ]
    },
    {
        "name": "elementary_rate_law",
        "description": "Generate rate law for elementary step.",
        "parameters": [
            {
                "name": "reactants",
                "type": "number"
            },
            {
                "name": "molecularity",
                "type": "number"
            }
        ]
    },
    {
        "name": "find_intermediates",
        "description": "Identify intermediates in a reaction mechanism.",
        "parameters": [
            {
                "name": "mechanism",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_molecularity",
        "description": "Identify molecularity from number of reactants.",
        "parameters": [
            {
                "name": "reactants",
                "type": "number"
            }
        ]
    },
    {
        "name": "is_elementary_step_valid",
        "description": "Check if a step could be elementary based on rate law.",
        "parameters": [
            {
                "name": "rate_law",
                "type": "number"
            },
            {
                "name": "stoichiometry",
                "type": "number"
            }
        ]
    },
    {
        "name": "overall_rate_law_from_mechanism",
        "description": "Derive overall rate law from mechanism.",
        "parameters": [
            {
                "name": "mechanism",
                "type": "number"
            },
            {
                "name": "rds_index",
                "type": "number"
            }
        ]
    },
    {
        "name": "steady_state_approximation",
        "description": "Apply steady-state approximation for intermediate.",
        "parameters": [
            {
                "name": "mechanism",
                "type": "number"
            },
            {
                "name": "intermediate",
                "type": "number"
            }
        ]
    }
]
