# L3 Tool: Enzyme Kinetics Tools
# Michaelis-Menten kinetics, Lineweaver-Burk analysis, and inhibition studies.

"""
## Solver Instructions (for AI Agent)

When you encounter enzyme kinetics problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Given KM, Vmax, [S]** -> need velocity? Use `michaelis_menten_kinetics()`
- **Given multiple ([S], v) data points** -> need KM/Vmax? Use `lineweaver_burk_plot()`
- **Given control + inhibited data** -> need inhibition type? Use `inhibition_analysis()`
- **Given Vmax, [E]0** -> need turnover number? Use `turnover_number()`
- **Given target v, Vmax, KM** -> need [S]? Use `substrate_concentration_for_velocity()`
- **Given kcat/KM value** -> need classification? Use `classify_catalytic_efficiency()`
- **Want to compare methods** -> Use `compare_kinetic_methods()` or individual `eadie_hofstee_plot()` / `hanes_woolf_plot()`

### Step 2: Choose the correct function
| Problem type | Function |
|---|---|
| Calculate reaction velocity | `michaelis_menten_kinetics()` |
| Determine KM, Vmax from data | `lineweaver_burk_plot()` |
| Classify inhibition (competitive/noncompetitive/uncompetitive/mixed) | `inhibition_analysis()` |
| Calculate kcat from Vmax and [E]0 | `turnover_number()` |
| Find [S] for a target velocity | `substrate_concentration_for_velocity()` |
| Rank catalytic efficiency | `classify_catalytic_efficiency()` |
| Alternative linearization (less error at low [S]) | `eadie_hofstee_plot()` or `hanes_woolf_plot()` |

### Step 3: Handle special cases
- **[S] = KM** -> velocity is always exactly 0.5 x Vmax (no calculation needed)
- **target_velocity >= Vmax** -> `substrate_concentration_for_velocity()` returns an error; v can never reach Vmax
- **Ambiguous inhibition** -> if both KM and Vmax change but not clearly in one direction, the tool returns 'mixed' or 'unknown'
- **Edge cases for Lineweaver-Burk** -> this method amplifies errors at low [S]; use Eadie-Hofstee or Hanes-Woolf for noisy data
- **Catalytic efficiency >= 108 M-1s-1** -> enzyme is "diffusion-limited" (catalytically perfect)
- **enzyme_conc parameter** -> when provided to `michaelis_menten_kinetics()`, it additionally returns kcat and catalytic efficiency

### Examples

**Example 1: Calculate velocity and saturation**
An enzyme has KM = 5 uM, Vmax = 100 uM/s. What is v at [S] = 50 uM?
-> `michaelis_menten_kinetics(substrate_conc=50e-6, KM=5e-6, Vmax=100e-6)`
Result: v ~ 90.9 uM/s, 90.9% Vmax (near-maximal saturation)

**Example 2: Classify inhibition from data**
Control: [(1mM, 50uM/s), (2mM, 67uM/s), (5mM, 83uM/s)]
With 1 uM inhibitor: [(1mM, 25uM/s), (2mM, 40uM/s), (5mM, 67uM/s)]
-> `inhibition_analysis(control, inhibited, inhibitor_conc=1e-6)`
Result: competitive (KM increased, Vmax unchanged)

**Example 3: Turnover number**
Vmax = 200 uM/s, [E]0 = 5 nM.
-> `turnover_number(Vmax=200e-6, enzyme_conc=5e-9)`
Result: kcat = 40,000 s-1 (fast)

Source: LibreTexts Biochemistry (Jakubowski and Flatt), Ch6
Created: 2026-03-18
"""

import math
from typing import List, Dict, Tuple, Optional
import os

# Path to L4 data
L4_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'L4_reference', 'enzyme_kinetics_data.csv')


def michaelis_menten_kinetics(
    substrate_conc: float,
    KM: float,
    Vmax: float,
    enzyme_conc: Optional[float] = None
) -> Dict:
    """
    Calculate reaction velocity using Michaelis-Menten equation.
    
    v = Vmax * [S] / (KM + [S])
    
    The Michaelis-Menten model describes enzyme kinetics when:
    - Enzyme concentration is much less than substrate
    - Reaction is at steady state
    - Single substrate reaction
    
    Args:
        substrate_conc: Substrate concentration [S] (M)
        KM: Michaelis constant (M) - substrate conc at half Vmax
        Vmax: Maximum velocity (M/s or consistent units)
        enzyme_conc: Total enzyme concentration [E]0 (M), optional
    
    Returns:
        Dictionary with:
        - velocity: Reaction velocity v
        - fraction_Vmax: v/Vmax as decimal
        - saturation: Substrate saturation level
        - kcat: Turnover number (if enzyme_conc provided)
        - catalytic_efficiency: kcat/KM (if enzyme_conc provided)
    
    Example:
        >>> result = michaelis_menten_kinetics(10e-6, 5e-6, 100e-6)
        >>> print(f"v = {result['velocity']:.2e} M/s")
    """
    # Calculate velocity
    velocity = Vmax * substrate_conc / (KM + substrate_conc)
    fraction_Vmax = velocity / Vmax
    
    result = {
        'velocity': velocity,
        'fraction_Vmax': fraction_Vmax,
        'saturation': f"{fraction_Vmax*100:.1f}% of Vmax",
        'KM': KM,
        'Vmax': Vmax,
        'substrate_conc': substrate_conc
    }
    
    # Calculate kcat if enzyme concentration provided
    if enzyme_conc is not None and enzyme_conc > 0:
        kcat = Vmax / enzyme_conc  # Turnover number (s^-1)
        catalytic_efficiency = kcat / KM
        result['kcat'] = kcat
        result['catalytic_efficiency'] = catalytic_efficiency
        result['efficiency_classification'] = classify_catalytic_efficiency(catalytic_efficiency)
    
    return result


def lineweaver_burk_plot(substrate_concs: List[float], velocities: List[float]) -> Dict:
    """
    Determine KM and Vmax from Lineweaver-Burk (double reciprocal) plot.
    
    1/v = (KM/Vmax)(1/[S]) + 1/Vmax
    
    This is the classical method but has issues with error at low [S].
    For better alternatives, use Eadie-Hofstee or Hanes-Woolf.
    
    Args:
        substrate_concs: List of substrate concentrations [S] (M)
        velocities: List of corresponding velocities v (M/s)
    
    Returns:
        Dictionary with:
        - KM: Michaelis constant (M)
        - Vmax: Maximum velocity (M/s)
        - slope: Slope of Lineweaver-Burk line
        - intercept: Y-intercept (1/Vmax)
        - x_intercept: X-intercept (-1/KM)
        - R_squared: Correlation coefficient
    """
    import numpy as np
    
    # Convert to reciprocal
    inv_S = [1/s for s in substrate_concs if s > 0]
    inv_v = [1/v for v in velocities[:len(inv_S)] if v > 0]
    
    if len(inv_S) < 2:
        return {'error': 'Need at least 2 valid data points'}
    
    # Linear regression
    n = len(inv_S)
    sum_x = sum(inv_S)
    sum_y = sum(inv_v)
    sum_xy = sum(x*y for x, y in zip(inv_S, inv_v))
    sum_x2 = sum(x*x for x in inv_S)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    Vmax = 1 / intercept
    KM = slope / intercept
    
    # R-squared
    y_mean = sum_y / n
    ss_tot = sum((y - y_mean)**2 for y in inv_v)
    ss_res = sum((y - (slope*x + intercept))**2 for x, y in zip(inv_S, inv_v))
    R_squared = 1 - ss_res/ss_tot if ss_tot > 0 else 0
    
    return {
        'KM': KM,
        'Vmax': Vmax,
        'slope': slope,
        'intercept': intercept,
        'x_intercept': -1/KM,
        'R_squared': R_squared
    }


def eadie_hofstee_plot(substrate_concs: List[float], velocities: List[float]) -> Dict:
    """
    Determine KM and Vmax from Eadie-Hofstee plot.
    
    v = -KM(v/[S]) + Vmax
    
    Less error-prone than Lineweaver-Burk for low [S].
    
    Args:
        substrate_concs: List of substrate concentrations [S] (M)
        velocities: List of corresponding velocities v (M/s)
    
    Returns:
        Dictionary with KM, Vmax, slope, intercept, R_squared
    """
    import numpy as np
    
    # v vs v/[S]
    v_over_S = [v/s for v, s in zip(velocities, substrate_concs) if s > 0 and v > 0]
    v_vals = velocities[:len(v_over_S)]
    
    if len(v_over_S) < 2:
        return {'error': 'Need at least 2 valid data points'}
    
    # Linear regression: v = -KM * (v/[S]) + Vmax
    n = len(v_over_S)
    sum_x = sum(v_over_S)
    sum_y = sum(v_vals)
    sum_xy = sum(x*y for x, y in zip(v_over_S, v_vals))
    sum_x2 = sum(x*x for x in v_over_S)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    KM = -slope
    Vmax = intercept
    
    return {
        'KM': KM,
        'Vmax': Vmax,
        'slope': slope,
        'intercept': intercept
    }


def hanes_woolf_plot(substrate_concs: List[float], velocities: List[float]) -> Dict:
    """
    Determine KM and Vmax from Hanes-Woolf plot.
    
    [S]/v = (1/Vmax)[S] + KM/Vmax
    
    Often the most reliable linearization method.
    
    Args:
        substrate_concs: List of substrate concentrations [S] (M)
        velocities: List of corresponding velocities v (M/s)
    
    Returns:
        Dictionary with KM, Vmax, slope, intercept
    """
    # [S]/v vs [S]
    S_over_v = [s/v for v, s in zip(velocities, substrate_concs) if v > 0]
    S_vals = substrate_concs[:len(S_over_v)]
    
    if len(S_over_v) < 2:
        return {'error': 'Need at least 2 valid data points'}
    
    # Linear regression
    n = len(S_over_v)
    sum_x = sum(S_vals)
    sum_y = sum(S_over_v)
    sum_xy = sum(x*y for x, y in zip(S_vals, S_over_v))
    sum_x2 = sum(x*x for x in S_vals)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    Vmax = 1 / slope
    KM = intercept * Vmax
    
    return {
        'KM': KM,
        'Vmax': Vmax,
        'slope': slope,
        'intercept': intercept
    }


def inhibition_analysis(
    control_data: List[Tuple[float, float]],
    inhibited_data: List[Tuple[float, float]],
    inhibitor_conc: float = None
) -> Dict:
    """
    Analyze enzyme inhibition from control and inhibited kinetics.
    
    Args:
        control_data: List of ([S], v) tuples for uninhibited enzyme
        inhibited_data: List of ([S], v) tuples with inhibitor present
        inhibitor_conc: Concentration of inhibitor (M), optional
    
    Returns:
        Dictionary with:
        - inhibition_type: 'competitive', 'noncompetitive', 'uncompetitive', or 'mixed'
        - control_KM: KM without inhibitor
        - control_Vmax: Vmax without inhibitor
        - inhibited_KM: KM with inhibitor
        - inhibited_Vmax: Vmax with inhibitor
        - Ki: Inhibition constant (if inhibitor_conc provided)
    """
    # Extract data
    control_S = [d[0] for d in control_data]
    control_v = [d[1] for d in control_data]
    inhib_S = [d[0] for d in inhibited_data]
    inhib_v = [d[1] for d in inhibited_data]
    
    # Determine KM and Vmax for each
    control_result = lineweaver_burk_plot(control_S, control_v)
    inhib_result = lineweaver_burk_plot(inhib_S, inhib_v)
    
    if 'error' in control_result or 'error' in inhib_result:
        return {'error': 'Could not determine kinetics from data'}
    
    control_KM = control_result['KM']
    control_Vmax = control_result['Vmax']
    inhib_KM = inhib_result['KM']
    inhib_Vmax = inhib_result['Vmax']
    
    # Classify inhibition type
    KM_ratio = inhib_KM / control_KM if control_KM > 0 else 1
    Vmax_ratio = inhib_Vmax / control_Vmax if control_Vmax > 0 else 1
    
    # Tolerance for "unchanged"
    tol = 0.15  # 15% tolerance
    
    KM_changed = abs(KM_ratio - 1) > tol
    Vmax_changed = abs(Vmax_ratio - 1) > tol
    
    if KM_changed and not Vmax_changed:
        inhibition_type = 'competitive'
    elif Vmax_changed and not KM_changed:
        inhibition_type = 'noncompetitive'
    elif KM_ratio < 1 and Vmax_ratio < 1:
        inhibition_type = 'uncompetitive'
    else:
        inhibition_type = 'mixed'
    
    result = {
        'inhibition_type': inhibition_type,
        'control_KM': control_KM,
        'control_Vmax': control_Vmax,
        'inhibited_KM': inhib_KM,
        'inhibited_Vmax': inhib_Vmax,
        'KM_ratio': KM_ratio,
        'Vmax_ratio': Vmax_ratio
    }
    
    # Calculate Ki if inhibitor concentration provided
    if inhibitor_conc is not None:
        if inhibition_type == 'competitive':
            Ki = inhibitor_conc / (KM_ratio - 1) if KM_ratio > 1 else None
        elif inhibition_type == 'noncompetitive':
            Ki = inhibitor_conc / (1/Vmax_ratio - 1) if Vmax_ratio < 1 else None
        else:
            Ki = None
        
        if Ki:
            result['Ki'] = Ki
    
    return result


def turnover_number(Vmax: float, enzyme_conc: float) -> Dict:
    """
    Calculate turnover number (kcat) from Vmax and enzyme concentration.
    
    kcat = Vmax / [E]0
    
    Represents the number of substrate molecules converted per enzyme per second.
    
    Args:
        Vmax: Maximum velocity (M/s)
        enzyme_conc: Total enzyme concentration [E]0 (M)
    
    Returns:
        Dictionary with kcat and classification
    """
    kcat = Vmax / enzyme_conc
    
    # Classify turnover rate
    if kcat > 1000:
        classification = 'very fast'
    elif kcat > 100:
        classification = 'fast'
    elif kcat > 10:
        classification = 'moderate'
    else:
        classification = 'slow'
    
    return {
        'kcat': kcat,
        'classification': classification
    }


def substrate_concentration_for_velocity(
    target_velocity: float,
    KM: float,
    Vmax: float
) -> Dict:
    """
    Calculate substrate concentration needed to achieve target velocity.
    
    Rearranged Michaelis-Menten:
    [S] = KM * v / (Vmax - v)
    
    Args:
        target_velocity: Desired velocity v (M/s)
        KM: Michaelis constant (M)
        Vmax: Maximum velocity (M/s)
    
    Returns:
        Dictionary with required [S] and validation
    """
    if target_velocity >= Vmax:
        return {
            'error': 'Target velocity cannot reach or exceed Vmax',
            'max_possible': Vmax
        }
    
    substrate_conc = KM * target_velocity / (Vmax - target_velocity)
    fraction_Vmax = target_velocity / Vmax
    
    return {
        'substrate_conc': substrate_conc,
        'target_velocity': target_velocity,
        'fraction_Vmax': fraction_Vmax
    }


def classify_catalytic_efficiency(catalytic_efficiency: float) -> str:
    """
    Classify catalytic efficiency (kcat/KM).
    
    Args:
        catalytic_efficiency: kcat/KM in M^-1 s^-1
    
    Returns:
        Classification string
    """
    if catalytic_efficiency >= 1e8:
        return 'diffusion-limited (catalytically perfect)'
    elif catalytic_efficiency >= 1e6:
        return 'very efficient'
    elif catalytic_efficiency >= 1e4:
        return 'moderately efficient'
    else:
        return 'low efficiency'


def compare_kinetic_methods(substrate_concs: List[float], velocities: List[float]) -> Dict:
    """
    Compare KM and Vmax from different linearization methods.
    
    Args:
        substrate_concs: List of substrate concentrations [S] (M)
        velocities: List of corresponding velocities v (M/s)
    
    Returns:
        Dictionary comparing Lineweaver-Burk, Eadie-Hofstee, and Hanes-Woolf results
    """
    lb = lineweaver_burk_plot(substrate_concs, velocities)
    eh = eadie_hofstee_plot(substrate_concs, velocities)
    hw = hanes_woolf_plot(substrate_concs, velocities)
    
    return {
        'lineweaver_burk': {'KM': lb.get('KM'), 'Vmax': lb.get('Vmax')},
        'eadie_hofstee': {'KM': eh.get('KM'), 'Vmax': eh.get('Vmax')},
        'hanes_woolf': {'KM': hw.get('KM'), 'Vmax': hw.get('Vmax')}
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "michaelis_menten_kinetics",
        "description": "Calculate reaction velocity using Michaelis-Menten equation: v = Vmax * [S] / (KM + [S])",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate_conc": {"type": "number", "description": "Substrate concentration [S] (M)"},
                "KM": {"type": "number", "description": "Michaelis constant (M)"},
                "Vmax": {"type": "number", "description": "Maximum velocity (M/s)"},
                "enzyme_conc": {"type": "number", "description": "Total enzyme concentration [E]0 (M), optional"}
            },
            "required": ["substrate_conc", "KM", "Vmax"]
        }
    },
    {
        "name": "lineweaver_burk_plot",
        "description": "Determine KM and Vmax from Lineweaver-Burk (double reciprocal) plot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate_concs": {"type": "array", "items": {"type": "number"}, "description": "List of substrate concentrations [S] (M)"},
                "velocities": {"type": "array", "items": {"type": "number"}, "description": "List of corresponding velocities v (M/s)"}
            },
            "required": ["substrate_concs", "velocities"]
        }
    },
    {
        "name": "inhibition_analysis",
        "description": "Analyze enzyme inhibition from control and inhibited kinetics data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "control_data": {"type": "array", "description": "List of ([S], v) tuples for uninhibited enzyme"},
                "inhibited_data": {"type": "array", "description": "List of ([S], v) tuples with inhibitor present"},
                "inhibitor_conc": {"type": "number", "description": "Concentration of inhibitor (M), optional"}
            },
            "required": ["control_data", "inhibited_data"]
        }
    },
    {
        "name": "turnover_number",
        "description": "Calculate turnover number (kcat) from Vmax and enzyme concentration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Vmax": {"type": "number", "description": "Maximum velocity (M/s)"},
                "enzyme_conc": {"type": "number", "description": "Total enzyme concentration [E]0 (M)"}
            },
            "required": ["Vmax", "enzyme_conc"]
        }
    }
]
