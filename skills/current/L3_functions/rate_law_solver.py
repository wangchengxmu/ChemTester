"""
Rate Law Solver - L3 Implementation
Kinetics: Advanced rate law solving and analysis

Extends basic rate law tools with:
- Integrated rate law solvers
- Half-life calculations
- Reaction progress prediction
- Rate constant determination from concentration-time data

## Solver Instructions (for AI Agent)

When you encounter chemical kinetics problems (integrated rate laws, half-lives, concentration-time prediction, rate constant determination), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Half-life**: Given rate constant k (and possibly [A]0) -> find t½
- **Concentration prediction**: Given [A]0, k, t, and reaction order -> find [A] at time t
- **Time to reach concentration**: Given [A]0, [A]target, k -> find time required
- **Rate constant from data**: Given concentration-time data pairs -> determine k and reaction order
- **Reaction order identification**: Given concentration vs time data -> determine if 0th, 1st, or 2nd order

### Step 2: Choose the correct function
- `half_life_first_order(k)` -> t½ = ln(2)/k
- `half_life_second_order(k, initial_conc)` -> t½ = 1/(k[A]0)
- `half_life_zero_order(k, initial_conc)` -> t½ = [A]0/(2k)
- `concentration_first_order(A0, k, t)` -> [A] = [A]0xexp(-kt)
- `concentration_second_order(A0, k, t)` -> 1/[A] = 1/[A]0 + kt
- `concentration_zero_order(A0, k, t)` -> [A] = [A]0 - kt
- `time_to_concentration(A0, A_target, k, order)` -> solve integrated rate law for t
- `determine_order_and_rate_constant(times, concentrations)` -> fit data to determine order and k
- `integrated_rate_law(A0, k, t, order)` -> general: returns [A] for any order (0, 1, 2)

### Step 3: Handle special cases
- First-order half-life is independent of concentration; second-order depends on [A]0
- For 1st order: plot ln[A] vs t -> straight line with slope = -k
- For 2nd order: plot 1/[A] vs t -> straight line with slope = k
- For 0th order: plot [A] vs t -> straight line with slope = -k
- k must be positive; raises ValueError if k ≤ 0

### Examples
1. **First-order half-life**: k = 0.0693 s-1
   -> `half_life_first_order(0.0693)` -> 10.0 s

2. **Concentration prediction**: [A]0=0.50 M, k=0.0231 s-1, t=100 s, first-order
   -> `concentration_first_order(0.50, 0.0231, 100)` -> 0.50xexp(-2.31) ~ 0.050 M

3. **Determine order**: Data: (0s, 1.0M), (50s, 0.61M), (100s, 0.37M), (200s, 0.14M)
   -> ln(0.61/1.0)/50 = -0.0100, ln(0.37/1.0)/100 = -0.0099 -> consistent slope -> first order with k~0.010 s-1
"""

from typing import Dict, List, Tuple, Optional, Callable
import numpy as np
from numpy.typing import NDArray
from math import log, log10, exp
from scipy.optimize import curve_fit


# ============================================================================
# Half-Life Calculations
# ============================================================================

def half_life_first_order(k: float) -> float:
    """
    Calculate half-life for a first-order reaction.
    
    t1/2 = ln(2) / k
    
    Args:
        k: Rate constant (time-1)
    
    Returns:
        Half-life (same units as 1/k)
    
    Examples:
        >>> half_life_first_order(0.0693)  # ~ln(2)/10
        10.0
    """
    if k <= 0:
        raise ValueError("Rate constant must be positive")
    return log(2) / k


def half_life_second_order(k: float, initial_conc: float) -> float:
    """
    Calculate half-life for a second-order reaction.
    
    t1/2 = 1 / (k x [A]0)
    
    Args:
        k: Rate constant (M-1·time-1)
        initial_conc: Initial concentration (M)
    
    Returns:
        Half-life (time units)
    
    Examples:
        >>> half_life_second_order(0.5, 0.1)
        20.0
    """
    if k <= 0 or initial_conc <= 0:
        raise ValueError("Rate constant and concentration must be positive")
    return 1 / (k * initial_conc)


def half_life_zero_order(k: float, initial_conc: float) -> float:
    """
    Calculate half-life for a zero-order reaction.
    
    t1/2 = [A]0 / (2k)
    
    Args:
        k: Rate constant (M·time-1)
        initial_conc: Initial concentration (M)
    
    Returns:
        Half-life (time units)
    
    Examples:
        >>> half_life_zero_order(0.1, 1.0)
        5.0
    """
    if k <= 0 or initial_conc <= 0:
        raise ValueError("Rate constant and concentration must be positive")
    return initial_conc / (2 * k)


# ============================================================================
# Integrated Rate Laws
# ============================================================================

def integrated_zero_order(k: float, A0: float, t: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Calculate concentration vs time for zero-order reaction.
    
    [A] = [A]0 - kt
    
    Args:
        k: Rate constant (M·time-1)
        A0: Initial concentration (M)
        t: Time array
    
    Returns:
        Concentration array
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2, 3])
        >>> A = integrated_zero_order(0.1, 1.0, t)
        >>> A[0]
        1.0
    """
    A = A0 - k * t
    return np.maximum(A, 0)  # Concentration can't be negative


def integrated_first_order(k: float, A0: float, t: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Calculate concentration vs time for first-order reaction.
    
    ln([A]) = ln([A]0) - kt
    [A] = [A]0 x e^(-kt)
    
    Args:
        k: Rate constant (time-1)
        A0: Initial concentration (M)
        t: Time array
    
    Returns:
        Concentration array
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2])
        >>> A = integrated_first_order(0.693, 1.0, t)  # ln(2)
        >>> round(A[1], 3)  # After one half-life
        0.5
    """
    return A0 * np.exp(-k * t)


def integrated_second_order_one_reactant(k: float, A0: float, 
                                          t: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Calculate concentration vs time for second-order reaction (A -> products).
    
    1/[A] = 1/[A]0 + kt
    
    Args:
        k: Rate constant (M-1·time-1)
        A0: Initial concentration (M)
        t: Time array
    
    Returns:
        Concentration array
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 10])
        >>> A = integrated_second_order_one_reactant(0.1, 0.1, t)
        >>> round(A[0], 3)
        0.1
    """
    inv_A = 1/A0 + k * t
    return 1 / inv_A


def integrated_second_order_equal(k: float, A0: float, B0: float,
                                   t: NDArray[np.floating]) -> NDArray[np.floating]:
    """
    Calculate concentration for second-order A + B -> products with [A]0 = [B]0.
    
    Uses same formula as single reactant case.
    
    Args:
        k: Rate constant (M-1·time-1)
        A0: Initial concentration of A (M)
        B0: Initial concentration of B (M) - must equal A0
        t: Time array
    
    Returns:
        Concentration of A (same as B)
    
    Raises:
        ValueError: If A0 != B0
    """
    if not np.isclose(A0, B0):
        raise ValueError("This function requires [A]0 = [B]0. Use integrated_second_order_unequal for different concentrations.")
    return integrated_second_order_one_reactant(k, A0, t)


def integrated_second_order_unequal(k: float, A0: float, B0: float,
                                     t: NDArray[np.floating]) -> Tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Calculate concentrations for second-order A + B -> products with [A]0 != [B]0.
    
    ln([A]/[B]) = ln([A]0/[B]0) + ([A]0 - [B]0)kt
    
    Args:
        k: Rate constant (M-1·time-1)
        A0: Initial concentration of A (M)
        B0: Initial concentration of B (M)
        t: Time array
    
    Returns:
        Tuple of (A_concentrations, B_concentrations)
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2])
        >>> A, B = integrated_second_order_unequal(0.1, 0.2, 0.1, t)
        >>> A[0], B[0]
        (0.2, 0.1)
    """
    delta = A0 - B0
    ratio0 = A0 / B0
    
    # ln(A/B) = ln(A0/B0) + delta * k * t
    ln_ratio = log(ratio0) + delta * k * t
    
    # A/B = exp(ln_ratio)
    ratio = np.exp(ln_ratio)
    
    # A - B = delta (conserved)
    # A = ratio * B
    # A - A/ratio = delta
    # A(1 - 1/ratio) = delta
    # A = delta / (1 - 1/ratio) = delta * ratio / (ratio - 1)
    
    A = delta * ratio / (ratio - 1)
    B = A - delta
    
    return A, B


# ============================================================================
# Rate Constant Determination from Data
# ============================================================================

def determine_rate_constant_zero_order(t: NDArray[np.floating], 
                                        A: NDArray[np.floating]) -> Tuple[float, float]:
    """
    Determine k from concentration-time data for zero-order reaction.
    
    Linear fit: [A] = [A]0 - kt
    Slope = -k
    
    Args:
        t: Time array
        A: Concentration array
    
    Returns:
        Tuple of (k, R2)
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2, 3, 4])
        >>> A = 1.0 - 0.1 * t  # k = 0.1
        >>> k, r2 = determine_rate_constant_zero_order(t, A)
        >>> round(k, 3)
        0.1
    """
    # Linear regression
    coeffs = np.polyfit(t, A, 1)
    k = -coeffs[0]  # Slope is negative of k
    A0 = coeffs[1]
    
    # Calculate R2
    A_pred = A0 - k * t
    ss_res = np.sum((A - A_pred) ** 2)
    ss_tot = np.sum((A - np.mean(A)) ** 2)
    r2 = 1 - ss_res / ss_tot
    
    return k, r2


def determine_rate_constant_first_order(t: NDArray[np.floating], 
                                         A: NDArray[np.floating]) -> Tuple[float, float]:
    """
    Determine k from concentration-time data for first-order reaction.
    
    Linear fit: ln([A]) = ln([A]0) - kt
    Slope = -k
    
    Args:
        t: Time array
        A: Concentration array
    
    Returns:
        Tuple of (k, R2)
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2, 3])
        >>> A = 1.0 * np.exp(-0.5 * t)
        >>> k, r2 = determine_rate_constant_first_order(t, A)
        >>> round(k, 3)
        0.5
    """
    ln_A = np.log(A)
    
    coeffs = np.polyfit(t, ln_A, 1)
    k = -coeffs[0]
    
    # Calculate R2
    ln_A_pred = coeffs[1] - k * t
    ss_res = np.sum((ln_A - ln_A_pred) ** 2)
    ss_tot = np.sum((ln_A - np.mean(ln_A)) ** 2)
    r2 = 1 - ss_res / ss_tot
    
    return k, r2


def determine_rate_constant_second_order(t: NDArray[np.floating], 
                                          A: NDArray[np.floating]) -> Tuple[float, float]:
    """
    Determine k from concentration-time data for second-order reaction.
    
    Linear fit: 1/[A] = 1/[A]0 + kt
    Slope = k
    
    Args:
        t: Time array
        A: Concentration array
    
    Returns:
        Tuple of (k, R2)
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 5, 10, 15])
        >>> A = 1.0 / (1.0/0.1 + 0.5 * t)
        >>> k, r2 = determine_rate_constant_second_order(t, A)
        >>> round(k, 2)
        0.5
    """
    inv_A = 1 / A
    
    coeffs = np.polyfit(t, inv_A, 1)
    k = coeffs[0]
    
    # Calculate R2
    inv_A_pred = coeffs[1] + k * t
    ss_res = np.sum((inv_A - inv_A_pred) ** 2)
    ss_tot = np.sum((inv_A - np.mean(inv_A)) ** 2)
    r2 = 1 - ss_res / ss_tot
    
    return k, r2


def determine_order_and_constant(t: NDArray[np.floating], 
                                  A: NDArray[np.floating]) -> Dict:
    """
    Automatically determine reaction order and rate constant from data.
    
    Tests 0th, 1st, and 2nd order fits and returns best fit.
    
    Args:
        t: Time array
        A: Concentration array
    
    Returns:
        Dict with order, k, R2, and all fit results
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2, 3, 4])
        >>> A = 1.0 * np.exp(-0.5 * t)
        >>> result = determine_order_and_constant(t, A)
        >>> result['order']
        1
    """
    results = {}
    
    # Test zero order
    try:
        k0, r2_0 = determine_rate_constant_zero_order(t, A)
        results['zero_order'] = {'k': k0, 'r2': r2_0, 'order': 0}
    except:
        results['zero_order'] = {'k': None, 'r2': -1, 'order': 0}
    
    # Test first order
    try:
        k1, r2_1 = determine_rate_constant_first_order(t, A)
        results['first_order'] = {'k': k1, 'r2': r2_1, 'order': 1}
    except:
        results['first_order'] = {'k': None, 'r2': -1, 'order': 1}
    
    # Test second order
    try:
        k2, r2_2 = determine_rate_constant_second_order(t, A)
        results['second_order'] = {'k': k2, 'r2': r2_2, 'order': 2}
    except:
        results['second_order'] = {'k': None, 'r2': -1, 'order': 2}
    
    # Find best fit
    best = max(results.values(), key=lambda x: x['r2'])
    
    return {
        'best_order': best['order'],
        'k': best['k'],
        'r2': best['r2'],
        'all_results': results
    }


# ============================================================================
# Time Calculations
# ============================================================================

def time_to_fraction_zero_order(k: float, A0: float, fraction: float) -> float:
    """
    Calculate time to reach a certain fraction of initial concentration.
    
    For zero-order: t = [A]0(1 - f) / k
    
    Args:
        k: Rate constant
        A0: Initial concentration
        fraction: Target fraction (0 to 1)
    
    Returns:
        Time
    
    Examples:
        >>> time_to_fraction_zero_order(0.1, 1.0, 0.5)  # Half-life
        5.0
    """
    if not 0 <= fraction <= 1:
        raise ValueError("Fraction must be between 0 and 1")
    return A0 * (1 - fraction) / k


def time_to_fraction_first_order(k: float, fraction: float) -> float:
    """
    Calculate time to reach a certain fraction of initial concentration.
    
    For first-order: t = -ln(f) / k
    
    Args:
        k: Rate constant
        fraction: Target fraction (0 to 1)
    
    Returns:
        Time
    
    Examples:
        >>> time_to_fraction_first_order(0.693, 0.5)  # Half-life
        1.0
    """
    if not 0 < fraction <= 1:
        raise ValueError("Fraction must be between 0 and 1")
    return -log(fraction) / k


def time_to_fraction_second_order(k: float, A0: float, fraction: float) -> float:
    """
    Calculate time to reach a certain fraction of initial concentration.
    
    For second-order: t = (1/f - 1) / (k x [A]0)
    
    Args:
        k: Rate constant
        A0: Initial concentration
        fraction: Target fraction (0 to 1)
    
    Returns:
        Time
    
    Examples:
        >>> time_to_fraction_second_order(0.1, 0.1, 0.5)
        100.0
    """
    if not 0 < fraction <= 1:
        raise ValueError("Fraction must be between 0 and 1")
    return (1/fraction - 1) / (k * A0)


# ============================================================================
# Complex Rate Laws
# ============================================================================

def consecutive_first_order(k1: float, k2: float, A0: float,
                             t: NDArray[np.floating]) -> Tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Calculate concentrations for consecutive first-order reactions.
    
    A -> B -> C
    
    [A] = [A]0 e^(-k1t)
    [B] = [A]0 k1(e^(-k1t) - e^(-k2t)) / (k2 - k1)  (for k1 != k2)
    [C] = [A]0 - [A] - [B]
    
    Args:
        k1: Rate constant for A -> B
        k2: Rate constant for B -> C
        A0: Initial concentration of A
        t: Time array
    
    Returns:
        Tuple of ([A], [B], [C]) concentration arrays
    
    Examples:
        >>> import numpy as np
        >>> t = np.array([0, 1, 2])
        >>> A, B, C = consecutive_first_order(0.5, 0.3, 1.0, t)
        >>> round(A[0], 3)
        1.0
    """
    A = A0 * np.exp(-k1 * t)
    
    if np.isclose(k1, k2):
        # Special case: k1 = k2
        B = A0 * k1 * t * np.exp(-k1 * t)
    else:
        B = A0 * k1 * (np.exp(-k1 * t) - np.exp(-k2 * t)) / (k2 - k1)
    
    C = A0 - A - B
    
    return A, B, C


def parallel_first_order(k1: float, k2: float, A0: float,
                          t: NDArray[np.floating]) -> Tuple[NDArray[np.floating], NDArray[np.floating], NDArray[np.floating]]:
    """
    Calculate concentrations for parallel first-order reactions.
    
    A -> B (k1)
    A -> C (k2)
    
    [A] = [A]0 e^(-(k1+k2)t)
    [B] = [A]0 k1(1 - e^(-(k1+k2)t)) / (k1 + k2)
    [C] = [A]0 k2(1 - e^(-(k1+k2)t)) / (k1 + k2)
    
    Args:
        k1: Rate constant for A -> B
        k2: Rate constant for A -> C
        A0: Initial concentration of A
        t: Time array
    
    Returns:
        Tuple of ([A], [B], [C]) concentration arrays
    """
    k_total = k1 + k2
    A = A0 * np.exp(-k_total * t)
    B = A0 * k1 * (1 - np.exp(-k_total * t)) / k_total
    C = A0 * k2 * (1 - np.exp(-k_total * t)) / k_total
    
    return A, B, C


def reversible_first_order(kf: float, kr: float, A0: float, B0: float,
                            t: NDArray[np.floating]) -> Tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Calculate concentrations for reversible first-order reaction.
    
    A ⇌ B
    
    Args:
        kf: Forward rate constant
        kr: Reverse rate constant
        A0: Initial concentration of A
        B0: Initial concentration of B
        t: Time array
    
    Returns:
        Tuple of ([A], [B]) concentration arrays
    """
    K = kf / kr  # Equilibrium constant
    k_total = kf + kr
    
    # Equilibrium concentrations
    A_eq = (A0 + B0) / (1 + K)
    B_eq = K * A_eq
    
    # Approach to equilibrium
    A = A_eq + (A0 - A_eq) * np.exp(-k_total * t)
    B = B_eq + (B0 - B_eq) * np.exp(-k_total * t)
    
    return A, B


if __name__ == "__main__":
    """Example usage and simple tests."""
    import numpy as np
    
    print("=" * 60)
    print("Rate Law Solver - Example Usage")
    print("=" * 60)
    
    # Example 1: Half-lives
    print("\n--- Example 1: Half-Life Calculations ---")
    k = 0.0693  # ~ln(2)/10
    print(f"First-order half-life (k={k}): {half_life_first_order(k):.1f} time units")
    
    k = 0.1
    A0 = 0.5
    print(f"Second-order half-life (k={k}, [A]0={A0}): {half_life_second_order(k, A0):.1f} time units")
    
    k = 0.2
    A0 = 1.0
    print(f"Zero-order half-life (k={k}, [A]0={A0}): {half_life_zero_order(k, A0):.1f} time units")
    
    # Example 2: First-order kinetics
    print("\n--- Example 2: First-Order Kinetics ---")
    k = 0.5
    A0 = 1.0
    t = np.array([0, 1, 2, 3, 4, 5])
    A = integrated_first_order(k, A0, t)
    print(f"k = {k}, [A]0 = {A0}")
    print(f"Time: {t}")
    print(f"[A]: {np.round(A, 3)}")
    
    # Determine k from data
    k_calc, r2 = determine_rate_constant_first_order(t, A)
    print(f"Determined k: {k_calc:.3f}, R2: {r2:.4f}")
    
    # Example 3: Auto-determine order
    print("\n--- Example 3: Auto-Determine Order ---")
    # Generate second-order data
    k_true = 0.5
    A0 = 0.1
    t = np.linspace(0, 20, 10)
    A = integrated_second_order_one_reactant(k_true, A0, t)
    
    result = determine_order_and_constant(t, A)
    print(f"True order: 2, k = {k_true}")
    print(f"Determined order: {result['best_order']}, k = {result['k']:.3f}, R2 = {result['r2']:.4f}")
    
    # Example 4: Consecutive reactions
    print("\n--- Example 4: Consecutive Reactions A -> B -> C ---")
    k1, k2 = 0.3, 0.1
    t = np.linspace(0, 20, 5)
    A, B, C = consecutive_first_order(k1, k2, 1.0, t)
    print(f"k1 = {k1}, k2 = {k2}")
    print(f"t = {t}")
    print(f"[A] = {np.round(A, 3)}")
    print(f"[B] = {np.round(B, 3)}")
    print(f"[C] = {np.round(C, 3)}")
    
    # Example 5: Time to fraction
    print("\n--- Example 5: Time to Reach 10% Remaining ---")
    fraction = 0.1
    print(f"First-order (k=0.5): {time_to_fraction_first_order(0.5, fraction):.2f} time units")
    print(f"Second-order (k=0.1, [A]0=0.1): {time_to_fraction_second_order(0.1, 0.1, fraction):.2f} time units")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
