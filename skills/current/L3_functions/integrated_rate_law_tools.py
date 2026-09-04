"""
Integrated Rate Law Tools - L3 Implementation
Chapter 12.04: Integrated Rate Laws and Half-Life

## Solver Instructions (for AI Agent)

When you encounter an integrated rate law problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Reaction order: Look for "first order", "second order", "zero order"
- Rate constant k: With appropriate units (s-1, M-1·s-1, M·s-1)
- Initial concentration C0: Starting concentration
- Time t: Elapsed time
- Concentration at time t: [A]t
- Half-life: t1/2
- Data points: Time-concentration data for order determination

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| First order: Find [A]t | `first_order_concentration(C0, k, t)` |
| First order: Find time to reach [A]t | `first_order_time(C0, Ct, k)` |
| First order: Find half-life | `first_order_half_life(k)` |
| Second order: Find [A]t | `second_order_concentration(C0, k, t)` |
| Second order: Find time | `second_order_time(C0, Ct, k)` |
| Second order: Find half-life | `second_order_half_life(C0, k)` |
| Zero order: Find [A]t | `zero_order_concentration(C0, k, t)` |
| Zero order: Find time | `zero_order_time(C0, Ct, k)` |
| Zero order: Find half-life | `zero_order_half_life(C0, k)` |
| General half-life | `half_life(order, k, C0)` |
| Identify order from data | `identify_order_from_data(times, concentrations)` |

### Step 3: Handle special cases
- **Order identification**: Plot ln[A] vs t (1st order linear), 1/[A] vs t (2nd order linear), [A] vs t (0th order linear)
- **Half-life dependencies**: 1st order: t1/2 independent of C0; 2nd order: t1/2 ∝ 1/C0; 0th order: t1/2 ∝ C0
- **Units of k**: 1st order: time-1; 2nd order: M-1·time-1; 0th order: M·time-1
- **Concentration limit**: Zero order: can't go below zero

### Examples

**Example 1: First order decay**
Question: "A first-order reaction has k = 0.1 s-1. Find [A] after 10 s if C0 = 1.0 M."
- Solution: `first_order_concentration(C0=1.0, k=0.1, t=10)` -> 0.37 M

**Example 2: First order half-life**
Question: "Calculate the half-life of a first-order reaction with k = 0.05 s-1."
- Solution: `first_order_half_life(k=0.05)` -> 13.9 s

**Example 3: Second order**
Question: "For a second-order reaction (k = 0.1 M-1·s-1), find [A] at t = 50 s if C0 = 0.2 M."
- Solution: `second_order_concentration(C0=0.2, k=0.1, t=50)` -> 0.10 M

**Example 4: Identify order from data**
Question: "Determine the reaction order from data: t=[0,6,12,18] min, [A]=[1.0,0.5,0.25,0.125] M"
- Solution: `identify_order_from_data(times=[0,6,12,18], concentrations=[1.0,0.5,0.25,0.125])` -> (1, ~0.116) first order
"""

from typing import Tuple, Optional
from math import log, exp


def first_order_concentration(C0: float, k: float, t: float) -> float:
    """
    Calculate concentration for first-order reaction.
    
    Args:
        C0: Initial concentration (M)
        k: Rate constant (time-1)
        t: Time
    
    Returns:
        Concentration at time t
    
    Examples:
        >>> first_order_concentration(1.0, 0.1, 6.93)
        0.5
    """
    return C0 * exp(-k * t)


def first_order_time(C0: float, Ct: float, k: float) -> float:
    """
    Calculate time to reach concentration for first-order reaction.
    
    Args:
        C0: Initial concentration (M)
        Ct: Target concentration (M)
        k: Rate constant (time-1)
    
    Returns:
        Time to reach Ct
    
    Examples:
        >>> first_order_time(1.0, 0.5, 0.1)
        6.93
    """
    return log(C0 / Ct) / k


def first_order_half_life(k: float) -> float:
    """
    Calculate half-life for first-order reaction.
    
    Args:
        k: Rate constant (time-1)
    
    Returns:
        Half-life
    
    Examples:
        >>> first_order_half_life(0.1)
        6.93
    """
    return 0.693 / k


def second_order_concentration(C0: float, k: float, t: float) -> float:
    """
    Calculate concentration for second-order reaction.
    
    Args:
        C0: Initial concentration (M)
        k: Rate constant (M-1·time-1)
        t: Time
    
    Returns:
        Concentration at time t
    
    Examples:
        >>> round(second_order_concentration(0.2, 0.1, 10), 3)
        0.167
    """
    return 1.0 / (k * t + 1.0 / C0)


def second_order_time(C0: float, Ct: float, k: float) -> float:
    """
    Calculate time to reach concentration for second-order reaction.
    
    Args:
        C0: Initial concentration (M)
        Ct: Target concentration (M)
        k: Rate constant (M-1·time-1)
    
    Returns:
        Time to reach Ct
    
    Examples:
        >>> round(second_order_time(0.2, 0.15, 0.1), 1)
        16.7
    """
    return (1.0 / Ct - 1.0 / C0) / k


def second_order_half_life(C0: float, k: float) -> float:
    """
    Calculate half-life for second-order reaction.
    
    Args:
        C0: Initial concentration (M)
        k: Rate constant (M-1·time-1)
    
    Returns:
        Half-life
    
    Examples:
        >>> second_order_half_life(0.2, 0.1)
        50.0
    """
    return 1.0 / (k * C0)


def zero_order_concentration(C0: float, k: float, t: float) -> float:
    """
    Calculate concentration for zero-order reaction.
    
    Args:
        C0: Initial concentration (M)
        k: Rate constant (M·time-1)
        t: Time
    
    Returns:
        Concentration at time t
    
    Examples:
        >>> zero_order_concentration(1.0, 0.1, 5)
        0.5
    """
    return max(0, C0 - k * t)


def zero_order_time(C0: float, Ct: float, k: float) -> float:
    """
    Calculate time to reach concentration for zero-order reaction.
    
    Args:
        C0: Initial concentration (M)
        Ct: Target concentration (M)
        k: Rate constant (M·time-1)
    
    Returns:
        Time to reach Ct
    
    Examples:
        >>> zero_order_time(1.0, 0.5, 0.1)
        5.0
    """
    return (C0 - Ct) / k


def zero_order_half_life(C0: float, k: float) -> float:
    """
    Calculate half-life for zero-order reaction.
    
    Args:
        C0: Initial concentration (M)
        k: Rate constant (M·time-1)
    
    Returns:
        Half-life
    
    Examples:
        >>> zero_order_half_life(1.0, 0.1)
        5.0
    """
    return C0 / (2 * k)


def identify_order_from_data(times: list, concentrations: list) -> Tuple[int, float]:
    """
    Identify reaction order from concentration vs time data.
    
    Args:
        times: List of time values
        concentrations: List of concentration values
    
    Returns:
        (order, rate_constant)
    
    Examples:
        >>> identify_order_from_data([0, 6, 12, 18], [1.0, 0.5, 0.25, 0.125])
        (1, 0.116)
    """
    # Test first-order: ln[C] vs t should be linear
    ln_conc = [log(c) for c in concentrations if c > 0]
    
    if len(ln_conc) == len(times):
        # Simple linear regression for slope
        n = len(times)
        sum_x = sum(times)
        sum_y = sum(ln_conc)
        sum_xy = sum(t * lc for t, lc in zip(times, ln_conc))
        sum_x2 = sum(t**2 for t in times)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        r_squared = calculate_r_squared(times, ln_conc, slope)
        
        if r_squared > 0.99:
            return (1, -slope)
    
    # Test second-order: 1/[C] vs t should be linear
    inv_conc = [1.0/c for c in concentrations if c > 0]
    times_trimmed = times[:len(inv_conc)]
    
    if len(inv_conc) > 1:
        n = len(times_trimmed)
        sum_x = sum(times_trimmed)
        sum_y = sum(inv_conc)
        sum_xy = sum(t * ic for t, ic in zip(times_trimmed, inv_conc))
        sum_x2 = sum(t**2 for t in times_trimmed)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        r_squared = calculate_r_squared(times_trimmed, inv_conc, slope)
        
        if r_squared > 0.99:
            return (2, slope)
    
    # Test zero-order: [C] vs t should be linear
    n = len(times)
    sum_x = sum(times)
    sum_y = sum(concentrations)
    sum_xy = sum(t * c for t, c in zip(times, concentrations))
    sum_x2 = sum(t**2 for t in times)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    
    if slope < 0:  # Concentration decreasing
        return (0, -slope)
    
    return (1, 0.1)  # Default


def calculate_r_squared(x: list, y: list, slope: float) -> float:
    """Calculate R-squared for linear fit."""
    n = len(x)
    if n == 0:
        return 0.0
    
    mean_y = sum(y) / n
    intercept = (sum(y) - slope * sum(x)) / n
    
    ss_tot = sum((yi - mean_y)**2 for yi in y)
    ss_res = sum((yi - (slope * xi + intercept))**2 for xi, yi in zip(x, y))
    
    if ss_tot == 0:
        return 1.0
    
    return 1 - ss_res / ss_tot


def half_life(order: int, k: float, C0: float = None) -> float:
    """
    Calculate half-life for any order.
    
    Args:
        order: Reaction order (0, 1, or 2)
        k: Rate constant
        C0: Initial concentration (required for order 0 and 2)
    
    Returns:
        Half-life
    
    Examples:
        >>> half_life(1, 0.1)
        6.93
        >>> half_life(2, 0.1, 0.2)
        50.0
        >>> half_life(0, 0.1, 1.0)
        5.0
    """
    if order == 0:
        if C0 is None:
            raise ValueError("C0 required for zero-order half-life")
        return zero_order_half_life(C0, k)
    elif order == 1:
        return first_order_half_life(k)
    elif order == 2:
        if C0 is None:
            raise ValueError("C0 required for second-order half-life")
        return second_order_half_life(C0, k)
    else:
        raise ValueError(f"Order {order} not supported")

MCP_TOOLS = [
    {
        "name": "calculate_r_squared",
        "description": "Calculate R-squared for linear fit.",
        "parameters": [
            {
                "name": "x",
                "type": "number"
            },
            {
                "name": "y",
                "type": "number"
            },
            {
                "name": "slope",
                "type": "number"
            }
        ]
    },
    {
        "name": "first_order_concentration",
        "description": "Calculate concentration for first-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            },
            {
                "name": "t",
                "type": "number"
            }
        ]
    },
    {
        "name": "first_order_half_life",
        "description": "Calculate half-life for first-order reaction.",
        "parameters": [
            {
                "name": "k",
                "type": "number"
            }
        ]
    },
    {
        "name": "first_order_time",
        "description": "Calculate time to reach concentration for first-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "Ct",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            }
        ]
    },
    {
        "name": "half_life",
        "description": "Calculate half-life for any order.",
        "parameters": [
            {
                "name": "order",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            },
            {
                "name": "C0",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_order_from_data",
        "description": "Identify reaction order from concentration vs time data.",
        "parameters": [
            {
                "name": "times",
                "type": "number"
            },
            {
                "name": "concentrations",
                "type": "number"
            }
        ]
    },
    {
        "name": "second_order_concentration",
        "description": "Calculate concentration for second-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            },
            {
                "name": "t",
                "type": "number"
            }
        ]
    },
    {
        "name": "second_order_half_life",
        "description": "Calculate half-life for second-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            }
        ]
    },
    {
        "name": "second_order_time",
        "description": "Calculate time to reach concentration for second-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "Ct",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            }
        ]
    },
    {
        "name": "zero_order_concentration",
        "description": "Calculate concentration for zero-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            },
            {
                "name": "t",
                "type": "number"
            }
        ]
    },
    {
        "name": "zero_order_half_life",
        "description": "Calculate half-life for zero-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            }
        ]
    },
    {
        "name": "zero_order_time",
        "description": "Calculate time to reach concentration for zero-order reaction.",
        "parameters": [
            {
                "name": "C0",
                "type": "number"
            },
            {
                "name": "Ct",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            }
        ]
    }
]
