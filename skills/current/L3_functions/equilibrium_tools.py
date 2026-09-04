"""
Equilibrium Tools - L3 Implementation
Chapter 13.1: Chemical Equilibrium

## Solver Instructions (for AI Agent)

When you encounter a chemical equilibrium problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Equilibrium constant K: May be Kc (concentrations) or Kp (pressures)
- Equilibrium concentrations: Values at equilibrium
- Initial concentrations: Starting values
- Reaction equation: Extract coefficients and species
- Direction prediction: Q vs K comparison

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Generate K expression | `equilibrium_expression(products, reactants)` |
| Calculate reaction quotient Q | `reaction_quotient(concentrations, products, reactants)` |
| Predict reaction direction | `predict_direction(Q, K)` |
| Calculate K from rate constants | `equilibrium_from_rates(kf, kr)` |
| Check if equilibrium | `rate_equality_condition(kf, kr, conc_A, conc_B)` |
| Check if homogeneous equilibrium | `is_homogeneous(phases)` |
| Determine if species omitted from Q | `omit_from_expression(species, phase, solvent)` |

### Step 3: Handle special cases
- **Solids and liquids**: Omitted from K expression (activity = 1)
- **Q vs K**: Q < K -> forward; Q > K -> reverse; Q = K -> equilibrium
- **Heterogeneous equilibria**: Include only gases and aqueous species in K
- **Phase notation**: 's' = solid, 'l' = liquid, 'g' = gas, 'aq' = aqueous

### Examples

**Example 1: Generate K expression**
Question: "Write the equilibrium expression for N2 + 3H2 ⇌ 2NH3."
- Given: reactants = {'N2': 1, 'H2': 3}, products = {'NH3': 2}
- Solution: `equilibrium_expression(products={'NH3': 2}, reactants={'N2': 1, 'H2': 3})` -> 'K = [NH3]^2 / ([N2][H2]^3)'

**Example 2: Predict direction**
Question: "If K = 50 and Q = 10, which direction will the reaction proceed?"
- Given: K = 50, Q = 10
- Solution: `predict_direction(Q=10, K=50)` -> 'forward'

**Example 3: Check if species omitted**
Question: "Should CaCO3(s) be included in the K expression for CaCO3(s) ⇌ CaO(s) + CO2(g)?"
- Given: species = 'CaCO3', phase = 's'
- Solution: `omit_from_expression(species='CaCO3', phase='s')` -> True (omit from expression)

**Example 4: Calculate K from rates**
Question: "If kf = 0.1 s-1 and kr = 0.001 s-1, what is K?"
- Solution: `equilibrium_from_rates(kf=0.1, kr=0.001)` -> K = 100
"""

from typing import Dict, List, Tuple, Optional


def equilibrium_expression(products: Dict[str, int], 
                           reactants: Dict[str, int]) -> str:
    """
    Generate equilibrium constant expression.
    
    Args:
        products: Dict of {product: coefficient}
        reactants: Dict of {reactant: coefficient}
    
    Returns:
        K expression string
    
    Examples:
        >>> equilibrium_expression({'NH3': 2}, {'N2': 1, 'H2': 3})
        'K = [NH3]^2 / ([N2][H2]^3)'
    """
    # Build numerator (products)
    num_terms = []
    for species, coeff in products.items():
        if coeff == 1:
            num_terms.append(f'[{species}]')
        else:
            num_terms.append(f'[{species}]^{coeff}')
    
    # Build denominator (reactants)
    den_terms = []
    for species, coeff in reactants.items():
        if coeff == 1:
            den_terms.append(f'[{species}]')
        else:
            den_terms.append(f'[{species}]^{coeff}')
    
    numerator = ''.join(num_terms) if num_terms else '1'
    denominator = ''.join(den_terms) if len(den_terms) == 1 else '(' + ''.join(den_terms) + ')'
    
    if not den_terms:
        return f'K = {numerator}'
    
    return f'K = {numerator} / {denominator}'


def reaction_quotient(concentrations: Dict[str, float], 
                       products: Dict[str, int],
                       reactants: Dict[str, int]) -> float:
    """
    Calculate reaction quotient Q from concentrations.
    
    Args:
        concentrations: Dict of {species: concentration}
        products: Dict of {product: coefficient}
        reactants: Dict of {reactant: coefficient}
    
    Returns:
        Q value
    
    Examples:
        >>> reaction_quotient({'NH3': 0.5, 'N2': 0.1, 'H2': 0.2}, 
        ...                   {'NH3': 2}, {'N2': 1, 'H2': 3})
        625.0
    
    Note: This function uses (products_dict, reactants_dict) API.
    For consistency with equilibrium_constant(stoichiometry_list), 
    consider using reaction_quotient_v2() instead.
    """
    # Numerator: products
    numerator = 1.0
    for species, coeff in products.items():
        conc = concentrations.get(species, 0)
        numerator *= conc ** coeff
    
    # Denominator: reactants
    denominator = 1.0
    for species, coeff in reactants.items():
        conc = concentrations.get(species, 0)
        if conc == 0:
            return float('inf')  # Q undefined (infinite)
        denominator *= conc ** coeff
    
    return numerator / denominator


def reaction_quotient_v2(concentrations_dict, reaction_stoichiometry):
    """
    Calculate reaction quotient Q using the same stoichiometry format as equilibrium_constant.
    
    This is the preferred function for Q calculations — consistent API with equilibrium_constant.
    
    Args:
        concentrations_dict: Dict of {species: concentration}
        reaction_stoichiometry: List of (coeff, formula, phase) tuples.
            Negative = reactant, positive = product.
            e.g., [(-1,'H2','g'), (-1,'I2','g'), (2,'HI','g')]
    
    Returns:
        Q value
    
    Examples:
        >>> reaction_quotient_v2({'SO2': 0.050, 'Cl2': 0.16, 'SO2Cl2': 0.12},
        ...                     [(-2,'SO2Cl2','g'), (2,'SO2','g'), (1,'Cl2','g')])
        0.0667
    """
    # Same logic as equilibrium_constant, just using current (non-equilibrium) concentrations
    return equilibrium_constant(concentrations_dict, reaction_stoichiometry)


def predict_direction(Q: float, K: float) -> str:
    """
    Predict reaction direction from Q and K comparison.
    
    Args:
        Q: Reaction quotient
        K: Equilibrium constant
    
    Returns:
        Direction string: 'forward', 'reverse', or 'at equilibrium'
    
    Examples:
        >>> predict_direction(0.1, 10.0)
        'forward'
        >>> predict_direction(100.0, 10.0)
        'reverse'
    """
    if Q < K:
        return 'forward'
    elif Q > K:
        return 'reverse'
    else:
        return 'at equilibrium'


def rate_equality_condition(kf: float, kr: float, 
                            conc_A: float, conc_B: float) -> bool:
    """
    Check if forward and reverse rates are equal.
    
    Args:
        kf: Forward rate constant
        kr: Reverse rate constant
        conc_A: Reactant concentration
        conc_B: Product concentration
    
    Returns:
        True if rates equal (at equilibrium)
    
    Examples:
        >>> rate_equality_condition(0.1, 0.01, 0.1, 1.0)
        True
    """
    forward_rate = kf * conc_A
    reverse_rate = kr * conc_B
    return abs(forward_rate - reverse_rate) < 1e-10


def equilibrium_from_rates(kf: float, kr: float) -> float:
    """
    Calculate equilibrium constant from rate constants.
    
    For elementary reaction A ⇌ B:
    K = kf/kr
    
    Args:
        kf: Forward rate constant
        kr: Reverse rate constant
    
    Returns:
        Equilibrium constant K
    
    Examples:
        >>> equilibrium_from_rates(0.1, 0.01)
        10.0
    """
    return kf / kr


def is_homogeneous(phases: Dict[str, str]) -> bool:
    """
    Check if equilibrium is homogeneous (same phase).
    
    Args:
        phases: Dict of {species: phase}
    
    Returns:
        True if all species in same phase
    
    Examples:
        >>> is_homogeneous({'H2': 'g', 'I2': 'g', 'HI': 'g'})
        True
        >>> is_homogeneous({'CaCO3': 's', 'CaO': 's', 'CO2': 'g'})
        False
    """
    unique_phases = set(phases.values())
    return len(unique_phases) == 1


def omit_from_expression(species: str, phase: str, 
                         solvent: str = None) -> bool:
    """
    Determine if species should be omitted from Q expression.
    
    Pure solids, pure liquids, and solvents are omitted.
    
    Args:
        species: Species name
        phase: Phase ('s', 'l', 'g', 'aq')
        solvent: Name of solvent (if applicable)
    
    Returns:
        True if species should be omitted
    
    Examples:
        >>> omit_from_expression('CaCO3', 's')
        True
        >>> omit_from_expression('H2O', 'l', solvent='H2O')
        True
    """
    # Pure solids always omitted
    if phase == 's':
        return True
    
    # Pure liquids and solvents omitted
    if phase == 'l' and (solvent is None or species == solvent):
        return True
    
    return False


def equilibrium_concentrations(initial_concentrations, reaction_stoichiometry, K,
                               mode='auto', tol=1e-10):
    """
    Solve ICE table to find equilibrium concentrations given K and initial conditions.
    
    Supports the common patterns:
    - aA + bB ⇌ cC + dD with all species having initial concentrations
    - Symmetric initial concentrations (e.g., [A]₀=[B]₀) -> simplifies to linear
    - Large K -> assume 100% forward, then small reverse
    - Small K -> assume x ≈ 0 change from initial
    
    Args:
        initial_concentrations: Dict of {species: initial concentration} in M
            Species not listed default to 0.
        reaction_stoichiometry: List of (coeff, formula, phase) tuples.
            Negative = reactant, positive = product.
            e.g., H2 + I2 ⇌ 2HI: [(-1,'H2','g'), (-1,'I2','g'), (2,'HI','g')]
        K: Equilibrium constant Kc (must be > 0)
        mode: 'auto', 'quadratic', 'large_K', 'small_K'
            'auto' chooses based on K magnitude.
        tol: Convergence tolerance for iterative methods.
    
    Returns:
        Dict of {species: equilibrium concentration}
    
    Examples:
        >>> # H2 + I2 <=> 2HI, K=54, [H2]=[I2]=0.172
        >>> eq = equilibrium_concentrations(
        ...     {'H2': 0.172, 'I2': 0.172},
        ...     [(-1,'H2','g'), (-1,'I2','g'), (2,'HI','g')],
        ...     K=54)
        >>> round(eq['HI'], 2)
        0.27
        >>> round(eq['H2'], 3)
        0.037
        
        >>> # H2 + C2H4 <=> C2H6, K=9.6e18, [H2]=0.200, [C2H4]=0.155
        >>> eq = equilibrium_concentrations(
        ...     {'H2': 0.200, 'C2H4': 0.155},
        ...     [(-1,'H2','g'), (-1,'C2H4','g'), (1,'C2H6','g')],
        ...     K=9.6e18)
        >>> round(eq['C2H6'], 3)
        0.155
    """
    import math
    
    if K <= 0:
        raise ValueError("K must be positive")
    
    # Parse stoichiometry: reactants and products
    reactants = []  # [(formula, |coeff|), ...]
    products = []   # [(formula, coeff), ...]
    gas_species = []
    
    for coeff, formula, phase in reaction_stoichiometry:
        if phase in ('s', 'l'):
            continue  # Pure solids/liquids don't participate
        gas_species.append((formula, abs(coeff), coeff))
        if coeff < 0:
            reactants.append((formula, abs(coeff)))
        else:
            products.append((formula, abs(coeff)))
    
    initial = {}
    for formula, _, _ in gas_species:
        initial[formula] = initial_concentrations.get(formula, 0.0)
    
    # Choose mode
    if mode == 'auto':
        if K > 1e6:
            mode = 'large_K'
        elif K < 1e-6:
            mode = 'small_K'
        else:
            mode = 'quadratic'
    
    if mode == 'large_K':
        return _ice_large_K(initial, reactants, products, gas_species, K)
    elif mode == 'small_K':
        return _ice_small_K(initial, reactants, products, gas_species, K)
    else:
        return _ice_quadratic(initial, reactants, products, gas_species, K)


def _ice_quadratic(initial, reactants, products, gas_species, K):
    """Solve ICE table using quadratic formula. Works for K ~ 0.01 to ~1e6."""
    import math
    
    # Check if all reactants have same initial concentration (symmetric case)
    # and stoichiometric coefficients are 1:1 (or symmetric)
    # e.g., H2 + I2 <=> 2HI with [H2]=[I2]
    
    # Try symmetric simplification first:
    # If 1 reactant + 1 product (1 reactant species, 1 product species),
    # or if equal initial concs with same reactant coeffs
    sym_result = _try_symmetric(initial, reactants, products, gas_species, K)
    if sym_result is not None:
        return sym_result
    
    # General case: solve numerically
    return _ice_numerical(initial, reactants, products, gas_species, K)


def _try_symmetric(initial, reactants, products, gas_species, K):
    """Try symmetric simplification for simple reactions.
    
    Handles patterns like:
    - A + B <=> C + D with [A]₀=[B]₀ -> K = x²/(C₀-x)² -> x = C₀√K/(1+√K)
    - A + B <=> 2C with [A]₀=[B]₀ -> K = 4x²/(C₀-x)² -> x = C₀√(K/4)/(1+√(K/4))
    """
    import math
    
    if len(reactants) != 2 or len(products) != 2:
        return None
    
    r1_form, r1_coeff = reactants[0]
    r2_form, r2_coeff = reactants[1]
    p1_form, p1_coeff = products[0]
    p2_form, p2_coeff = products[1]
    
    # Check: all stoichiometric coefficients = 1 and equal initial concs
    if r1_coeff != 1 or r2_coeff != 1 or p1_coeff != 1 or p2_coeff != 1:
        # Check H2+I2<=>2HI pattern: r1=r2=1, p1=2 (only 1 product with coeff 2)
        if len(products) == 1 and products[0][1] == 2:
            # Single product with coeff 2, e.g., H2+I2<=>2HI
            return _symmetric_double_product(initial, reactants, products, K)
        if len(reactants) == 1 and reactants[0][1] == 2:
            # Single reactant with coeff 2, e.g., 2A<=>B+C
            return _symmetric_double_reactant(initial, reactants, products, K)
        return None
    
    if abs(initial[r1_form] - initial[r2_form]) > 1e-10:
        return None
    
    # A + B <=> C + D, [A]₀=[B]₀=C₀
    C0 = initial[r1_form]
    # K = x²/(C0-x)² -> sqrt(K) = x/(C0-x) -> x = C0*sqrt(K)/(1+sqrt(K))
    sqrtK = math.sqrt(K)
    x = C0 * sqrtK / (1 + sqrtK)
    
    result = {
        r1_form: C0 - x,
        r2_form: C0 - x,
        p1_form: x,
        p2_form: x,
    }
    # Restore original species names from gas_species
    return result


def _symmetric_double_product(initial, reactants, products, K):
    """A + B <=> 2C, [A]₀=[B]₀=C₀.
    K = (2x)²/(C0-x)² -> 2x/(C0-x) = √K -> x = C0√K/(2+√K)
    """
    import math
    
    r1_form, _ = reactants[0]
    r2_form, _ = reactants[1]
    p_form, p_coeff = products[0]  # Should have coeff=2
    
    C0 = initial[r1_form]
    sqrtK = math.sqrt(K)
    x = C0 * sqrtK / (p_coeff + sqrtK)
    
    return {
        r1_form: C0 - x,
        r2_form: C0 - x,
        p_form: p_coeff * x,
    }


def _symmetric_double_reactant(initial, reactants, products, K):
    """2A <=> B + C, [B]₀=[C]₀=0.
    K = x²/(C0-2x)² -> x/(C0-2x) = √K -> x = C0√K/(2+2√K)
    Actually: K = [B][C]/[A]² = x*x/(C0-2x)²
    x/(C0-2x) = √K -> x = √K*(C0-2x) -> x(1+2√K) = C0√K -> x = C0√K/(1+2√K)
    """
    import math
    
    r_form, r_coeff = reactants[0]  # coeff=2
    C0 = initial[r_form]
    sqrtK = math.sqrt(K)
    x = C0 * sqrtK / (1 + r_coeff * sqrtK)
    
    result = {r_form: C0 - r_coeff * x}
    for p_form, p_coeff in products:
        result[p_form] = p_coeff * x
    return result


def _ice_numerical(initial, reactants, products, gas_species, K, max_iter=200):
    """Solve ICE table numerically using bisection on extent of reaction x.
    
    For a reaction with extent x:
    - Each species concentration = initial + signed_coeff * x
    - Q(x) = products expression / reactants expression
    - Find x where Q(x) = K
    """
    import math
    
    # Signed coefficients for each species
    signed_coeffs = {formula: coeff for formula, _, coeff in gas_species}
    
    def Q_of_x(x):
        """Calculate Q at extent x."""
        numerator = 1.0
        denominator = 1.0
        for formula, abs_coeff, signed_coeff in gas_species:
            conc = initial[formula] + signed_coeff * x
            if conc < 0:
                return -1  # Invalid x
            if signed_coeff > 0:
                numerator *= conc ** abs_coeff
            else:
                if conc < 1e-30:
                    return float('inf')
                denominator *= conc ** abs_coeff
        return numerator / denominator
    
    # Find valid range for x: [0, x_max] where x_max is limited by smallest reactant
    x_max = float('inf')
    for formula, _, signed_coeff in gas_species:
        if signed_coeff < 0 and initial[formula] > 0:
            x_limit = initial[formula] / abs(signed_coeff)
            x_max = min(x_max, x_limit)
    
    if x_max == float('inf'):
        x_max = 1.0
    
    # Check bounds
    q_min = Q_of_x(0)  # Q at initial conditions
    q_max = Q_of_x(x_max * 0.9999)  # Q near x_max (avoid exact edge)
    
    # Determine direction: Q should go from Q(0) to K
    # If Q(0) < K, forward reaction (x increases)
    # If Q(0) > K, reverse reaction... but we assumed products start at 0
    # Handle both cases
    
    if Q_of_x(0) <= K <= q_max or q_max <= K <= Q_of_x(0):
        pass  # Solution exists in [0, x_max]
    else:
        # K might be outside range — expand or use different approach
        pass
    
    # Bisection
    lo, hi = 0.0, x_max
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        q_mid = Q_of_x(mid)
        
        if q_mid < 0 or q_mid == float('inf'):
            # x too large, back off
            hi = mid
            continue
        
        if abs(q_mid - K) / max(K, 1e-30) < 1e-10:
            break
        
        if q_mid < K:
            lo = mid
        else:
            hi = mid
    
    x = (lo + hi) / 2
    result = {}
    for formula, _, signed_coeff in gas_species:
        conc = initial[formula] + signed_coeff * x
        result[formula] = max(0.0, conc)
    
    return result


def _ice_large_K(initial, reactants, products, gas_species, K):
    """Solve ICE table for K >> 1 (assume reaction goes essentially to completion).
    
    Find limiting reactant, assume it's consumed, then solve small reverse reaction.
    """
    import math
    
    signed_coeffs = {formula: coeff for formula, _, coeff in gas_species}
    
    # Find limiting reactant: smallest initial/coeff ratio
    limiting = None
    min_ratio = float('inf')
    for formula, _, signed_coeff in gas_species:
        if signed_coeff < 0 and initial[formula] > 0:
            ratio = initial[formula] / abs(signed_coeff)
            if ratio < min_ratio:
                min_ratio = ratio
                limiting = formula
    
    if limiting is None:
        return dict(initial)  # No reactants — nothing happens
    
    # Forward extent ≈ min_ratio
    x_forward = min_ratio
    
    # Now find small reverse extent y
    # After forward: concentrations
    after_forward = {}
    for formula, _, signed_coeff in gas_species:
        after_forward[formula] = max(0, initial[formula] + signed_coeff * x_forward)
    
    # Now solve for small y (reverse reaction extent)
    # K = Q(after_forward adjusted by y in reverse direction)
    # For small y: approximate using dominant terms
    
    # Use numerical bisection on small y
    # Q after forward should be >> K, then as y increases Q decreases
    # But actually after 100% forward, Q is very large (products/remaining_reactants)
    # We need to find y where Q = K
    
    def Q_of_y(y):
        num = 1.0
        den = 1.0
        for formula, _, signed_coeff in gas_species:
            # Reverse direction: subtract signed_coeff * y
            conc = after_forward[formula] - signed_coeff * y
            if conc < 0:
                return -1
            if signed_coeff > 0:
                num *= conc ** abs(signed_coeff)
            elif signed_coeff < 0:
                if conc < 1e-30:
                    return float('inf')
                den *= conc ** abs(signed_coeff)
        return num / den
    
    # y_max limited by product concentrations
    y_max = float('inf')
    for formula, _, signed_coeff in gas_species:
        if signed_coeff > 0 and after_forward[formula] > 0:
            y_max = min(y_max, after_forward[formula] / signed_coeff)
    
    if y_max == float('inf') or y_max <= 0:
        result = dict(after_forward)
        return result
    
    # Bisection
    lo, hi = 0.0, y_max
    for _ in range(200):
        mid = (lo + hi) / 2
        q_mid = Q_of_y(mid)
        if q_mid < 0 or q_mid == float('inf'):
            hi = mid
            continue
        if abs(q_mid - K) / max(K, 1e-30) < 1e-12:
            break
        if q_mid > K:
            lo = mid
        else:
            hi = mid
    
    y = (lo + hi) / 2
    result = {}
    for formula, _, signed_coeff in gas_species:
        conc = after_forward[formula] - signed_coeff * y
        result[formula] = max(0.0, conc)
    
    return result


def _ice_small_K(initial, reactants, products, gas_species, K):
    """Solve ICE table for K << 1 (assume x is very small compared to initial concs).
    
    Initial approximation: x ≈ K * reactant_product / product_coeff (first-order approx)
    Then refine with numerical method if needed.
    """
    import math
    
    signed_coeffs = {formula: coeff for formula, _, coeff in gas_species}
    
    # First approximation: assume reactant concs unchanged
    # Q ≈ (product_conc_product) / (reactant_conc_product)
    # For K << 1, x is small, so [reactants] ≈ initial
    
    # Simple case: single reactant A -> products
    if len(reactants) == 1 and len(products) >= 1:
        r_form, r_coeff = reactants[0]
        # K = prod(product_concs^coeff) / [A]^r_coeff
        # Approximate: numerator ≈ x^sum_p_coeff (if all products start at 0)
        # x^(sum p coeff) = K * [A]^r_coeff
        num_power = sum(c for _, c in products)
        if all(initial[f] < 1e-15 for f, _ in products):
            x_approx = (K * initial[r_form] ** r_coeff) ** (1.0 / num_power)
        else:
            # Some products already present — use numerical
            return _ice_numerical(initial, reactants, products, gas_species, K)
        
        # Check if x << initial (5% rule)
        if x_approx < 0.05 * initial[r_form]:
            result = dict(initial)
            for f, c in products:
                result[f] = initial[f] + c * x_approx
            result[r_form] = initial[r_form] - r_coeff * x_approx
            return result
    
    # Fall back to numerical
    return _ice_numerical(initial, reactants, products, gas_species, K)


def equilibrium_constant(concentrations_dict, reaction_stoichiometry):
    """
    Calculate Kc from equilibrium concentrations using signed stoichiometry.
    
    Args:
        concentrations_dict: Dict of {species: equilibrium concentration}
        reaction_stoichiometry: List of (coeff, formula, phase) tuples.
            Negative coeff = reactant, positive = product.
            e.g., 2NOBr(g) ⇌ 2NO(g) + Br2(g): [(-2,'NOBr','g'), (2,'NO','g'), (1,'Br2','g')]
    
    Returns:
        Kc value
    
    Examples:
        >>> equilibrium_constant({'NOBr': 0.423, 'NO': 1.29, 'Br2': 10.52},
        ...                     [(-2,'NOBr','g'), (2,'NO','g'), (1,'Br2','g')])
        97.8...
    """
    numerator = 1.0
    denominator = 1.0
    for coeff, formula, phase in reaction_stoichiometry:
        if phase in ('s', 'l'):
            continue  # Pure solids/liquids omitted
        conc = concentrations_dict[formula]
        if coeff > 0:
            numerator *= conc ** coeff
        else:
            denominator *= conc ** abs(coeff)
    return numerator / denominator


def kp_from_kc(Kc, delta_n, temperature_K):
    """
    Convert Kc to Kp: Kp = Kc * (RT)^delta_n
    
    Args:
        Kc: Equilibrium constant in concentration units
        delta_n: Change in moles of gas (moles gas products - moles gas reactants)
        temperature_K: Temperature in Kelvin
    
    Returns:
        Kp value
    
    Examples:
        >>> kp_from_kc(97.8, 1, 1000.15)
        8026.4...
    """
    R = 0.08206  # L·atm/(mol·K)
    return Kc * (R * temperature_K) ** delta_n


def kc_from_kp(Kp, delta_n, temperature_K):
    """
    Convert Kp to Kc: Kc = Kp / (RT)^delta_n
    
    Args:
        Kp: Equilibrium constant in pressure units
        delta_n: Change in moles of gas (moles gas products - moles gas reactants)
        temperature_K: Temperature in Kelvin
    
    Returns:
        Kc value
    """
    R = 0.08206  # L·atm/(mol·K)
    return Kp / (R * temperature_K) ** delta_n


def equilibrium_from_composition(initial_concentrations, reaction_stoichiometry, extent):
    """
    Calculate K and equilibrium concentrations from initial conditions and extent of reaction.
    
    Args:
        initial_concentrations: Dict of {species: initial concentration}
        reaction_stoichiometry: List of (coeff, formula, phase) tuples (negative=reactant)
        extent: Extent of reaction (xi)
    
    Returns:
        (K, equilibrium_concentrations_dict)
    
    Examples:
        >>> K, eq = equilibrium_from_composition(
        ...     {'NOBr': 2.0, 'NO': 0.0, 'Br2': 0.0},
        ...     [(-2,'NOBr','g'), (2,'NO','g'), (1,'Br2','g')],
        ...     0.789
        ... )
    """
    eq_concs = {}
    for coeff, formula, phase in reaction_stoichiometry:
        init = initial_concentrations.get(formula, 0.0)
        eq_concs[formula] = init + coeff * extent
    K = equilibrium_constant(eq_concs, reaction_stoichiometry)
    return K, eq_concs


def ice_table(initial, change, equilibrium):
    """
    Calculate Kc from ICE table data.
    
    Args:
        initial: Dict of {species: initial concentration}
        change: Dict of {species: change in concentration}
        equilibrium: Dict of {species: equilibrium concentration}
    
    Returns:
        Kc value calculated from equilibrium concentrations.
        Note: stoichiometry is inferred from change values (sign and magnitude).
    
    Examples:
        >>> ice_table({'A': 1.0, 'B': 1.0, 'C': 0.0},
        ...           {'A': -0.5, 'B': -0.5, 'C': 1.0},
        ...           {'A': 0.5, 'B': 0.5, 'C': 1.0})
        4.0
    """
    # Determine products (positive change) and reactants (negative change)
    products = {sp: abs(ch) for sp, ch in change.items() if ch > 0}
    reactants = {sp: abs(ch) for sp, ch in change.items() if ch < 0}
    
    numerator = 1.0
    for sp, coeff in products.items():
        numerator *= equilibrium[sp] ** coeff
    
    denominator = 1.0
    for sp, coeff in reactants.items():
        denominator *= equilibrium[sp] ** coeff
    
    return numerator / denominator


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "equilibrium_expression",
        "description": "Generate equilibrium constant expression.",
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
        "name": "equilibrium_from_rates",
        "description": "Calculate equilibrium constant from rate constants.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kf": {"type": "number", "description": "Kf"},
                "kr": {"type": "number", "description": "Kr"},
            },
            "required": ["kf", "kr"]
        }
    },
    {
        "name": "is_homogeneous",
        "description": "Check if equilibrium is homogeneous (same phase).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phases": {"type": "number", "description": "Phases"},
            },
            "required": ["phases"]
        }
    },
    {
        "name": "omit_from_expression",
        "description": "Determine if species should be omitted from Q expression.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "species": {"type": "number", "description": "Species"},
                "phase": {"type": "number", "description": "Phase"},
                "solvent": {"type": "number", "description": "Solvent", "default": None},
            },
            "required": ["species", "phase"]
        }
    },
    {
        "name": "predict_direction",
        "description": "Predict reaction direction from Q and K comparison.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Q": {"type": "number", "description": "Q"},
                "K": {"type": "number", "description": "K"},
            },
            "required": ["Q", "K"]
        }
    },
    {
        "name": "rate_equality_condition",
        "description": "Check if forward and reverse rates are equal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kf": {"type": "number", "description": "Kf"},
                "kr": {"type": "number", "description": "Kr"},
                "conc_A": {"type": "number", "description": "Conc A"},
                "conc_B": {"type": "number", "description": "Conc B"},
            },
            "required": ["kf", "kr", "conc_A", "conc_B"]
        }
    },
    {
        "name": "reaction_quotient",
        "description": "Calculate reaction quotient Q from concentrations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "concentrations": {"type": "number", "description": "Concentrations"},
                "products": {"type": "number", "description": "Products"},
                "reactants": {"type": "number", "description": "Reactants"},
            },
            "required": ["concentrations", "products", "reactants"]
        }
    }
]
