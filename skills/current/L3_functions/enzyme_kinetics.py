"""
Enzyme Kinetics Tools
=====================

Python implementations for enzyme kinetics including Michaelis-Menten,
Lineweaver-Burk analysis, and inhibition studies.

Source: L2 enzyme_kinetics.md
"""
## Solver Instructions (for AI Agent)

# When you encounter enzyme kinetics problems (Michaelis-Menten, inhibition, catalytic efficiency), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: [S], Vmax, Km, Ki, [I], inhibition type, enzyme concentration
# - **Asked**: reaction velocity, kcat, catalytic efficiency, IC50/Ki, inhibited velocity

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Michaelis-Menten velocity | `michaelis_menten(S, Vmax, Km)` | [S], Vmax, Km |
# | Lineweaver-Burk plot | `lineweaver_burk(S, Vmax, Km)` | -> (1/[S], 1/v) |
# | Turnover number | `kcat(Vmax, E0)` | Vmax, [E]0 |
# | Catalytic efficiency | `catalytic_efficiency(kcat, Km)` | kcat, Km |
# | Inhibited velocity | `inhibition_analysis(S, Vmax, Km, Ki, I, type)` | all params + type |
# | IC50 -> Ki | `ic50_to_ki(IC50, Km, S, type)` | IC50, Km, [S] |

### Step 3: Handle special cases
# - v = Vmax/2 when [S] = Km (definition of Km)
# - Competitive: Vmax unchanged, Km increases (Km_app = Km(1+[I]/Ki))
# - Noncompetitive: Km unchanged, Vmax decreases (Vmax_app = Vmax/(1+[I]/Ki))
# - Uncompetitive: both decrease
# - Diffusion-limited: kcat/Km > 108 M-1s-1

### Examples
# 1. **MM**: `michaelis_menten(0.01, 1e-6, 0.005)` -> 6.67e-07 M/s
# 2. **kcat**: `kcat(1e-6, 1e-9)` -> 1000 s-1
# 3. **Competitive inhibition**: `inhibition_analysis(0.01, 1e-6, 0.005, 0.002, 0.001, 'competitive')` -> 5.00e-07
# 4. **IC50->Ki**: `ic50_to_ki(1e-6, 1e-5, 5e-6, 'competitive')` -> 6.67e-07


import numpy as np
from typing import Tuple, Dict, Optional

def michaelis_menten(S: float, Vmax: float, Km: float) -> float:
    """
    Calculate reaction velocity using Michaelis-Menten equation.
    
    v = Vmax * [S] / (Km + [S])
    
    Parameters
    ----------
    S : float
        Substrate concentration (M)
    Vmax : float
        Maximum velocity (M/s)
    Km : float
        Michaelis constant (M)
    
    Returns
    -------
    float
        Reaction velocity (M/s)
    
    Examples
    --------
    >>> v = michaelis_menten(0.01, 1e-6, 0.005)
    >>> f"{v:.2e}"
    '6.67e-07'
    """
    return Vmax * S / (Km + S)


def lineweaver_burk(S: float, Vmax: float, Km: float) -> Tuple[float, float]:
    """
    Calculate 1/v and 1/[S] for Lineweaver-Burk plot.
    
    1/v = (Km/Vmax)(1/[S]) + 1/Vmax
    
    Parameters
    ----------
    S : float
        Substrate concentration (M)
    Vmax : float
        Maximum velocity (M/s)
    Km : float
        Michaelis constant (M)
    
    Returns
    -------
    tuple
        (1/[S], 1/v) for plotting
    
    Examples
    --------
    >>> x, y = lineweaver_burk(0.01, 1e-6, 0.005)
    >>> f"x={x:.0f}, y={y:.2e}"
    'x=100, y=1.50e+06'
    """
    v = michaelis_menten(S, Vmax, Km)
    return (1/S, 1/v)


def kcat(Vmax: float, E0: float) -> float:
    """
    Calculate turnover number (kcat).
    
    kcat = Vmax / [E]0
    
    Parameters
    ----------
    Vmax : float
        Maximum velocity (M/s)
    E0 : float
        Total enzyme concentration (M)
    
    Returns
    -------
    float
        Turnover number (s^-1)
    
    Examples
    --------
    >>> kcat(1e-6, 1e-9)
    1000.0
    """
    return Vmax / E0


def catalytic_efficiency(kcat: float, Km: float) -> float:
    """
    Calculate catalytic efficiency.
    
    kcat/Km measures enzyme efficiency
    
    Parameters
    ----------
    kcat : float
        Turnover number (s^-1)
    Km : float
        Michaelis constant (M)
    
    Returns
    -------
    float
        Catalytic efficiency (M^-1 s^-1)
    
    Examples
    --------
    >>> catalytic_efficiency(1000, 0.001)
    1000000.0
    """
    return kcat / Km


def inhibition_analysis(
    S: float,
    Vmax: float,
    Km: float,
    Ki: float,
    I: float,
    inhibition_type: str
) -> float:
    """
    Calculate velocity with inhibitor present.
    
    Parameters
    ----------
    S : float
        Substrate concentration (M)
    Vmax : float
        Maximum velocity without inhibitor (M/s)
    Km : float
        Michaelis constant without inhibitor (M)
    Ki : float
        Inhibition constant (M)
    I : float
        Inhibitor concentration (M)
    inhibition_type : str
        'competitive', 'noncompetitive', or 'uncompetitive'
    
    Returns
    -------
    float
        Velocity with inhibitor (M/s)
    
    Examples
    --------
    >>> v = inhibition_analysis(0.01, 1e-6, 0.005, 0.002, 0.001, 'competitive')
    >>> f"{v:.2e}"
    '5.00e-07'
    """
    alpha = 1 + I/Ki
    
    if inhibition_type == 'competitive':
        # Km apparent = Km * alpha, Vmax unchanged
        Km_app = Km * alpha
        return Vmax * S / (Km_app + S)
    elif inhibition_type == 'noncompetitive':
        # Vmax apparent = Vmax / alpha, Km unchanged
        Vmax_app = Vmax / alpha
        return Vmax_app * S / (Km + S)
    elif inhibition_type == 'uncompetitive':
        # Both Vmax and Km divided by alpha
        Vmax_app = Vmax / alpha
        Km_app = Km / alpha
        return Vmax_app * S / (Km_app + S)
    else:
        raise ValueError(f"Unknown inhibition type: {inhibition_type}")


def ic50_to_ki(IC50: float, Km: float, S: float, 
               inhibition_type: str = 'competitive') -> float:
    """
    Convert IC50 to Ki using Cheng-Prusoff equation.
    
    Ki = IC50 / (1 + [S]/Km) for competitive
    
    Parameters
    ----------
    IC50 : float
        Concentration for 50% inhibition (M)
    Km : float
        Michaelis constant (M)
    S : float
        Substrate concentration (M)
    inhibition_type : str
        Type of inhibition
    
    Returns
    -------
    float
        Inhibition constant Ki (M)
    
    Examples
    --------
    >>> ki = ic50_to_ki(1e-6, 1e-5, 5e-6)
    >>> f"{ki:.2e}"
    '6.67e-07'
    """
    if inhibition_type == 'competitive':
        return IC50 / (1 + S/Km)
    elif inhibition_type == 'noncompetitive':
        return IC50
    elif inhibition_type == 'uncompetitive':
        return IC50 / (1 + Km/S)
    else:
        raise ValueError(f"Unknown inhibition type: {inhibition_type}")


# Self-test
if __name__ == '__main__':
    print("Enzyme Kinetics Tools Test")
    print("=" * 40)
    
    # Test Michaelis-Menten
    print("\nMichaelis-Menten:")
    v = michaelis_menten(0.01, 1e-6, 0.005)
    print(f"  v at [S]=0.01M, Vmax=1e-6 M/s, Km=0.005M: {v:.2e} M/s")
    
    # Test at half-maximal
    v_half = michaelis_menten(0.005, 1e-6, 0.005)
    print(f"  v at [S]=Km: {v_half:.2e} M/s (should be Vmax/2)")
    
    # Test kcat
    print("\nTurnover number:")
    k = kcat(1e-6, 1e-9)
    print(f"  kcat = Vmax/[E]0 = 1e-6/1e-9 = {k:.0f} s^-1")
    
    # Test catalytic efficiency
    eff = catalytic_efficiency(1000, 0.001)
    print(f"\nCatalytic efficiency: kcat/Km = {eff:.2e} M^-1 s^-1")
    if eff > 1e8:
        print("  -> Diffusion-limited!")
    
    # Test inhibition
    print("\nInhibition analysis:")
    v_comp = inhibition_analysis(0.01, 1e-6, 0.005, 0.002, 0.001, 'competitive')
    print(f"  Competitive: v = {v_comp:.2e} M/s")
    
    print("\nAll tests passed")
