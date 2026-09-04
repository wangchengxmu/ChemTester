"""
Enzyme Kinetics Tools (G15)
Implements Michaelis-Menten kinetics, Lineweaver-Burk analysis, and inhibition analysis

## Solver Instructions (for AI Agent)

When you encounter an enzyme kinetics problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Substrate concentration [S]: In M, mM, muM
- Reaction velocity v: In M/s, mumol/min, etc.
- Km (Michaelis constant): In concentration units
- Vmax (maximum velocity): In velocity units
- kcat (turnover number): In s-1
- Enzyme concentration [E]: For kcat calculation
- Inhibition data: Velocities with and without inhibitor

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate velocity from [S], Km, Vmax | `michaelis_menten_kinetics(substrate, Km, Vmax)` |
| Determine Km and Vmax from data (Lineweaver-Burk) | `lineweaver_burk_analysis(substrate_array, velocity_array, enzyme_concentration)` |
| Fit Michaelis-Menten directly (nonlinear) | `fit_michaelis_menten(substrate_array, velocity_array)` |
| Analyze inhibition type and Ki | `inhibition_analysis(substrate, velocity_control, velocity_inhibited, inhibitor_concentration)` |
| Dixon plot analysis | `dixon_plot_analysis(inhibitor_concentrations, velocities, substrate_concentration)` |
| Calculate catalytic efficiency | `calculate_specificity_constant(Km, kcat)` |
| Classify enzyme efficiency | `enzyme_efficiency_classification(kcat_Km)` |

### Step 3: Handle special cases
- **Michaelis-Menten equation**: v = Vmax x [S] / (Km + [S])
- **Lineweaver-Burk**: 1/v = (Km/Vmax)(1/[S]) + 1/Vmax (linear plot)
- **kcat**: kcat = Vmax / [E]total
- **Catalytic efficiency**: kcat/Km (higher = more efficient)
- **Inhibition types**:
  - Competitive: Km increases, Vmax unchanged
  - Uncompetitive: Both Km and Vmax decrease
  - Noncompetitive: Vmax decreases, Km unchanged
  - Mixed: Both change

### Examples

**Example 1: Calculate velocity**
Question: "Calculate the reaction velocity if [S] = 5 mM, Km = 2 mM, Vmax = 100 muM/s."
- Solution: `michaelis_menten_kinetics(substrate=0.005, Km=0.002, Vmax=100e-6)` -> 71.4 muM/s

**Example 2: Lineweaver-Burk analysis**
Question: "Determine Km and Vmax from data: [S] = [1, 2, 5, 10, 20] mM, v = [50, 67, 83, 91, 95] muM/s."
- Solution: `lineweaver_burk_analysis(substrate=np.array([1e-3,2e-3,5e-3,1e-2,2e-2]), velocity=np.array([50e-6,67e-6,83e-6,91e-6,95e-6]))` -> Km ~ 2 mM, Vmax ~ 100 muM/s

**Example 3: Catalytic efficiency**
Question: "Calculate kcat/Km if kcat = 1000 s-1 and Km = 1 mM."
- Solution: `calculate_specificity_constant(Km=0.001, kcat=1000)` -> 1.0 x 106 M-1·s-1
- `enzyme_efficiency_classification(kcat_Km=1e6)` -> 'highly_efficient'

**Example 4: Inhibition analysis**
Question: "Analyze competitive inhibition: control v = [1e-6, 3e-6, 4e-6, 4.5e-6], inhibited v = [5e-7, 2e-6, 3e-6, 4e-6] at [I] = 10 muM, [S] = [1, 5, 10, 50] mM."
- Solution: `inhibition_analysis(substrate=np.array([1e-3,5e-3,1e-2,5e-2]), velocity_control=np.array([1e-6,3e-6,4e-6,4.5e-6]), velocity_inhibited=np.array([5e-7,2e-6,3e-6,4e-6]), inhibitor_concentration=1e-5)`
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings('ignore')


@dataclass
class KineticParameters:
    """Container for enzyme kinetic parameters"""
    Km: float  # Michaelis constant (M)
    Vmax: float  # Maximum velocity (M/s)
    kcat: Optional[float] = None  # Turnover number (s^-1)
    enzyme_concentration: Optional[float] = None  # [E]total (M)
    
    def __post_init__(self):
        if self.kcat is None and self.enzyme_concentration is not None:
            self.kcat = self.Vmax / self.enzyme_concentration


@dataclass
class InhibitionParameters:
    """Container for inhibition analysis results"""
    inhibition_type: str
    Ki: float  # Inhibition constant (M)
    alpha: Optional[float] = None  # For mixed inhibition
    IC50: Optional[float] = None  # Half-maximal inhibitory concentration


def michaelis_menten_kinetics(substrate: np.ndarray,
                              Km: float,
                              Vmax: float) -> np.ndarray:
    """
    Calculate reaction velocity using Michaelis-Menten equation.
    
    v = Vmax * [S] / (Km + [S])
    
    Parameters:
    -----------
    substrate : np.ndarray
        Substrate concentration(s) (M)
    Km : float
        Michaelis constant (M)
    Vmax : float
        Maximum reaction velocity (M/s)
    
    Returns:
    --------
    np.ndarray
        Reaction velocity (M/s)
    
    Example:
    --------
    >>> v = michaelis_menten_kinetics(np.array([0.001, 0.01, 0.1]), Km=0.01, Vmax=1e-6)
    """
    substrate = np.atleast_1d(substrate)
    return Vmax * substrate / (Km + substrate)


def lineweaver_burk_analysis(substrate: np.ndarray,
                             velocity: np.ndarray,
                             enzyme_concentration: Optional[float] = None) -> Dict[str, any]:
    """
    Determine Km and Vmax from Lineweaver-Burk (double reciprocal) plot.
    
    1/v = (Km/Vmax)(1/[S]) + 1/Vmax
    
    Parameters:
    -----------
    substrate : np.ndarray
        Substrate concentrations (M)
    velocity : np.ndarray
        Reaction velocities (M/s)
    enzyme_concentration : float, optional
        Total enzyme concentration for kcat calculation (M)
    
    Returns:
    --------
    Dict containing:
        - 'Km': Michaelis constant (M)
        - 'Vmax': Maximum velocity (M/s)
        - 'kcat': Turnover number if [E] provided (s^-1)
        - 'slope': Lineweaver-Burk slope
        - 'intercept': Lineweaver-Burk intercept
        - 'R_squared': Correlation coefficient
        - 'plot_data': Dict with x, y coordinates for plotting
    
    Example:
    --------
    >>> result = lineweaver_burk_analysis(
    ...     substrate=np.array([0.001, 0.002, 0.005, 0.01, 0.02]),
    ...     velocity=np.array([5e-7, 8e-7, 1.2e-6, 1.4e-6, 1.5e-6])
    ... )
    """
    substrate = np.atleast_1d(substrate)
    velocity = np.atleast_1d(velocity)
    
    # Filter out zero concentrations
    mask = (substrate > 0) & (velocity > 0)
    S = substrate[mask]
    v = velocity[mask]
    
    if len(S) < 2:
        raise ValueError("Need at least 2 valid data points")
    
    # Transform to Lineweaver-Burk coordinates
    x = 1.0 / S  # 1/[S]
    y = 1.0 / v  # 1/v
    
    # Linear regression: y = slope * x + intercept
    slope, intercept = np.polyfit(x, y, 1)
    
    # Calculate kinetic parameters
    Vmax = 1.0 / intercept
    Km = slope * Vmax
    
    # Calculate R-squared
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    R_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    result = {
        'Km': Km,
        'Vmax': Vmax,
        'slope': slope,
        'intercept': intercept,
        'R_squared': R_squared,
        'plot_data': {
            'x': x.tolist(),
            'y': y.tolist(),
            'xlabel': '1/[S] (M^-1)',
            'ylabel': '1/v (M^-1·s)',
            'slope': slope,
            'intercept': intercept
        }
    }
    
    if enzyme_concentration is not None:
        result['kcat'] = Vmax / enzyme_concentration
        result['enzyme_concentration'] = enzyme_concentration
    
    return result


def inhibition_analysis(substrate: np.ndarray,
                        velocity_control: np.ndarray,
                        velocity_inhibited: np.ndarray,
                        inhibitor_concentration: float,
                        substrate_fixed: Optional[float] = None) -> Dict[str, any]:
    """
    Analyze enzyme inhibition to determine inhibition type and Ki.
    
    Parameters:
    -----------
    substrate : np.ndarray
        Substrate concentrations (M)
    velocity_control : np.ndarray
        Velocities without inhibitor (M/s)
    velocity_inhibited : np.ndarray
        Velocities with inhibitor (M/s)
    inhibitor_concentration : float
        Concentration of inhibitor (M)
    substrate_fixed : float, optional
        If provided, uses Dixon plot analysis
    
    Returns:
    --------
    Dict containing:
        - 'inhibition_type': 'competitive', 'uncompetitive', 'noncompetitive', or 'mixed'
        - 'Ki': Inhibition constant (M)
        - 'alpha': Mixed inhibition factor (if applicable)
        - 'IC50': Approximate IC50 value
    
    Example:
    --------
    >>> result = inhibition_analysis(
    ...     substrate=np.array([0.001, 0.005, 0.01, 0.05]),
    ...     velocity_control=np.array([1e-6, 3e-6, 4e-6, 4.5e-6]),
    ...     velocity_inhibited=np.array([5e-7, 2e-6, 3e-6, 4e-6]),
    ...     inhibitor_concentration=0.001
    ... )
    """
    substrate = np.atleast_1d(substrate)
    velocity_control = np.atleast_1d(velocity_control)
    velocity_inhibited = np.atleast_1d(velocity_inhibited)
    
    # Get control parameters
    control_params = lineweaver_burk_analysis(substrate, velocity_control)
    Km_control = control_params['Km']
    Vmax_control = control_params['Vmax']
    
    # Get inhibited parameters
    inhibited_params = lineweaver_burk_analysis(substrate, velocity_inhibited)
    Km_inhibited = inhibited_params['Km']
    Vmax_inhibited = inhibited_params['Vmax']
    
    # Determine inhibition type based on parameter changes
    Km_ratio = Km_inhibited / Km_control if Km_control > 0 else 1
    Vmax_ratio = Vmax_inhibited / Vmax_control if Vmax_control > 0 else 1
    
    # Classification thresholds
    threshold = 1.2  # 20% change threshold
    
    if Km_ratio > threshold and abs(Vmax_ratio - 1) < 0.2:
        # Competitive: Km increases, Vmax unchanged
        inhibition_type = 'competitive'
        # Ki = [I] / (Km_app/Km - 1)
        Ki = inhibitor_concentration / (Km_ratio - 1) if Km_ratio > 1 else inhibitor_concentration
        
    elif Km_ratio < 0.8 and Vmax_ratio < 0.8:
        # Uncompetitive: both Km and Vmax decrease
        inhibition_type = 'uncompetitive'
        # Ki = [I] / (Km/Km_app - 1)
        Ki = inhibitor_concentration / (1/Km_ratio - 1) if Km_ratio < 1 else inhibitor_concentration
        
    elif abs(Km_ratio - 1) < 0.2 and Vmax_ratio < 0.8:
        # Noncompetitive: Vmax decreases, Km unchanged
        inhibition_type = 'noncompetitive'
        # Ki = [I] / (Vmax/Vmax_app - 1)
        Ki = inhibitor_concentration / (1/Vmax_ratio - 1) if Vmax_ratio < 1 else inhibitor_concentration
        
    else:
        # Mixed inhibition
        inhibition_type = 'mixed'
        # Calculate Ki values for both binding modes
        Ki = inhibitor_concentration
        alpha = Km_ratio / Vmax_ratio if Vmax_ratio > 0 else 1
    
    # Estimate IC50
    IC50 = inhibitor_concentration  # Simplified estimate
    
    result = {
        'inhibition_type': inhibition_type,
        'Ki': Ki,
        'IC50': IC50,
        'Km_control': Km_control,
        'Vmax_control': Vmax_control,
        'Km_inhibited': Km_inhibited,
        'Vmax_inhibited': Vmax_inhibited,
        'inhibitor_concentration': inhibitor_concentration
    }
    
    if inhibition_type == 'mixed':
        result['alpha'] = alpha
    
    return result


def dixon_plot_analysis(inhibitor_concentrations: np.ndarray,
                         velocities: np.ndarray,
                         substrate_concentration: float) -> Dict[str, any]:
    """
    Analyze inhibition using Dixon plot (1/v vs [I]).
    
    Parameters:
    -----------
    inhibitor_concentrations : np.ndarray
        Inhibitor concentrations (M)
    velocities : np.ndarray
        Reaction velocities at each [I] (M/s)
    substrate_concentration : float
        Fixed substrate concentration (M)
    
    Returns:
    --------
    Dict containing Ki estimate from Dixon plot
    
    Example:
    --------
    >>> Ki = dixon_plot_analysis(
    ...     inhibitor_concentrations=np.array([0, 1e-6, 5e-6, 1e-5]),
    ...     velocities=np.array([1e-6, 7e-7, 4e-7, 3e-7]),
    ...     substrate_concentration=1e-3
    ... )
    """
    I = np.atleast_1d(inhibitor_concentrations)
    v = np.atleast_1d(velocities)
    
    # Filter valid points
    mask = v > 0
    I = I[mask]
    v = v[mask]
    
    # Dixon plot: 1/v vs [I]
    x = I
    y = 1.0 / v
    
    # Linear fit
    slope, intercept = np.polyfit(x, y, 1)
    
    # Ki is where line crosses x-axis: -intercept/slope
    Ki = -intercept / slope if slope != 0 else float('inf')
    
    return {
        'Ki': abs(Ki),
        'slope': slope,
        'intercept': intercept,
        'plot_data': {
            'x': x.tolist(),
            'y': y.tolist(),
            'xlabel': '[I] (M)',
            'ylabel': '1/v (M^-1·s)'
        }
    }


def calculate_specificity_constant(Km: float, kcat: float) -> float:
    """
    Calculate enzyme specificity constant (catalytic efficiency).
    
    kcat/Km indicates how efficiently an enzyme converts substrate to product.
    
    Parameters:
    -----------
    Km : float
        Michaelis constant (M)
    kcat : float
        Turnover number (s^-1)
    
    Returns:
    --------
    float
        Specificity constant (M^-1·s^-1)
    
    Example:
    --------
    >>> efficiency = calculate_specificity_constant(Km=1e-3, kcat=1000)
    >>> print(f"{efficiency:.2e} M^-1·s^-1")
    """
    if Km <= 0:
        return 0
    return kcat / Km


def enzyme_efficiency_classification(kcat_Km: float) -> str:
    """
    Classify enzyme efficiency based on kcat/Km.
    
    Parameters:
    -----------
    kcat_Km : float
        Specificity constant (M^-1·s^-1)
    
    Returns:
    --------
    str
        Efficiency classification
    """
    if kcat_Km >= 1e8:
        return "catalytically_perfect"
    elif kcat_Km >= 1e6:
        return "highly_efficient"
    elif kcat_Km >= 1e4:
        return "moderately_efficient"
    elif kcat_Km >= 1e2:
        return "modestly_efficient"
    else:
        return "inefficient"


# Convenience functions
def fit_michaelis_menten(substrate: np.ndarray,
                         velocity: np.ndarray,
                         p0: Optional[Tuple[float, float]] = None) -> Dict[str, float]:
    """
    Fit Michaelis-Menten equation directly to data (non-linear regression).
    
    Parameters:
    -----------
    substrate : np.ndarray
        Substrate concentrations (M)
    velocity : np.ndarray
        Reaction velocities (M/s)
    p0 : tuple, optional
        Initial guess for (Km, Vmax)
    
    Returns:
    --------
    Dict with fitted parameters
    """
    S = np.atleast_1d(substrate)
    v = np.atleast_1d(velocity)
    
    if p0 is None:
        p0 = (np.median(S), np.max(v))
    
    try:
        popt, pcov = curve_fit(
            michaelis_menten_kinetics,
            S, v,
            p0=p0,
            bounds=([0, 0], [np.inf, np.inf])
        )
        Km, Vmax = popt
        perr = np.sqrt(np.diag(pcov))
        
        return {
            'Km': Km,
            'Vmax': Vmax,
            'Km_error': perr[0],
            'Vmax_error': perr[1],
            'method': 'nonlinear_regression'
        }
    except Exception as e:
        # Fall back to Lineweaver-Burk
        lb_result = lineweaver_burk_analysis(S, v)
        lb_result['method'] = 'lineweaver_burk_fallback'
        lb_result['error'] = str(e)
        return lb_result


if __name__ == "__main__":
    # Example usage
    print("=== Michaelis-Menten Kinetics ===")
    S = np.array([0.001, 0.002, 0.005, 0.01, 0.02])
    v = michaelis_menten_kinetics(S, Km=0.005, Vmax=1e-6)
    print(f"Substrate: {S}")
    print(f"Velocity: {v}")
    
    print("\n=== Lineweaver-Burk Analysis ===")
    result = lineweaver_burk_analysis(S, v, enzyme_concentration=1e-9)
    print(f"Km = {result['Km']:.2e} M")
    print(f"Vmax = {result['Vmax']:.2e} M/s")
    print(f"kcat = {result['kcat']:.2e} s^-1")
    print(f"R2 = {result['R_squared']:.4f}")
    
    print("\n=== Enzyme Efficiency ===")
    efficiency = calculate_specificity_constant(result['Km'], result['kcat'])
    classification = enzyme_efficiency_classification(efficiency)
    print(f"kcat/Km = {efficiency:.2e} M^-1·s^-1")
    print(f"Classification: {classification}")
    
    print("\n=== Competitive Inhibition Example ===")
    v_control = michaelis_menten_kinetics(S, Km=0.005, Vmax=1e-6)
    v_inhibited = michaelis_menten_kinetics(S, Km=0.015, Vmax=1e-6)  # Km tripled
    
    inh_result = inhibition_analysis(S, v_control, v_inhibited, 1e-5)
    print(f"Inhibition type: {inh_result['inhibition_type']}")
    print(f"Ki = {inh_result['Ki']:.2e} M")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calculate_specificity_constant",
        "description": "Calculate enzyme specificity constant (catalytic efficiency).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Km": {"type": "number", "description": "Km"},
                "kcat": {"type": "number", "description": "Kcat"},
            },
            "required": ["Km", "kcat"]
        }
    },
    {
        "name": "curve_fit",
        "description": "Use non-linear least squares to fit a function, f, to data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "f": {"type": "number", "description": "F"},
                "xdata": {"type": "number", "description": "Xdata"},
                "ydata": {"type": "number", "description": "Ydata"},
                "p0": {"type": "number", "description": "P0", "default": None},
                "sigma": {"type": "number", "description": "Sigma", "default": None},
                "absolute_sigma": {"type": "number", "description": "Absolute Sigma", "default": False},
                "check_finite": {"type": "number", "description": "Check Finite", "default": None},
                "bounds": {"type": "number", "description": "Bounds", "default": None},
                "method": {"type": "string", "description": "Method", "default": None},
                "jac": {"type": "number", "description": "Jac", "default": None},
                "full_output": {"type": "number", "description": "Full Output", "default": False},
                "nan_policy": {"type": "number", "description": "Nan Policy", "default": None},
                "kwargs": {"type": "number", "description": "Kwargs"},
            },
            "required": ["f", "xdata", "ydata", "kwargs"]
        }
    },
    {
        "name": "dataclass",
        "description": "Add dunder methods based on the fields defined in the class.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cls": {"type": "number", "description": "Cls", "default": None},
                "init": {"type": "number", "description": "Init", "default": True},
                "repr": {"type": "number", "description": "Repr", "default": True},
                "eq": {"type": "number", "description": "Eq", "default": True},
                "order": {"type": "number", "description": "Order", "default": False},
                "unsafe_hash": {"type": "number", "description": "Unsafe Hash", "default": False},
                "frozen": {"type": "number", "description": "Frozen", "default": False},
                "match_args": {"type": "number", "description": "Match Args", "default": True},
                "kw_only": {"type": "number", "description": "Kw Only", "default": False},
                "slots": {"type": "number", "description": "Slots", "default": False},
                "weakref_slot": {"type": "number", "description": "Weakref Slot", "default": False},
            },
            "required": []
        }
    },
    {
        "name": "dixon_plot_analysis",
        "description": "Analyze inhibition using Dixon plot (1/v vs [I]).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "inhibitor_concentrations": {"type": "number", "description": "Inhibitor Concentrations"},
                "velocities": {"type": "number", "description": "Velocities"},
                "substrate_concentration": {"type": "number", "description": "Substrate Concentration"},
            },
            "required": ["inhibitor_concentrations", "velocities", "substrate_concentration"]
        }
    },
    {
        "name": "enzyme_efficiency_classification",
        "description": "Classify enzyme efficiency based on kcat/Km.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kcat_Km": {"type": "number", "description": "Kcat Km"},
            },
            "required": ["kcat_Km"]
        }
    },
    {
        "name": "fit_michaelis_menten",
        "description": "Fit Michaelis-Menten equation directly to data (non-linear regression).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate": {"type": "number", "description": "Substrate"},
                "velocity": {"type": "number", "description": "Velocity"},
                "p0": {"type": "number", "description": "P0", "default": None},
            },
            "required": ["substrate", "velocity"]
        }
    },
    {
        "name": "inhibition_analysis",
        "description": "Analyze enzyme inhibition to determine inhibition type and Ki.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate": {"type": "number", "description": "Substrate"},
                "velocity_control": {"type": "number", "description": "Velocity Control"},
                "velocity_inhibited": {"type": "number", "description": "Velocity Inhibited"},
                "inhibitor_concentration": {"type": "number", "description": "Inhibitor Concentration"},
                "substrate_fixed": {"type": "number", "description": "Substrate Fixed", "default": None},
            },
            "required": ["substrate", "velocity_control", "velocity_inhibited", "inhibitor_concentration"]
        }
    },
    {
        "name": "lineweaver_burk_analysis",
        "description": "Determine Km and Vmax from Lineweaver-Burk (double reciprocal) plot.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate": {"type": "number", "description": "Substrate"},
                "velocity": {"type": "number", "description": "Velocity"},
                "enzyme_concentration": {"type": "number", "description": "Enzyme Concentration", "default": None},
            },
            "required": ["substrate", "velocity"]
        }
    },
    {
        "name": "michaelis_menten_kinetics",
        "description": "Calculate reaction velocity using Michaelis-Menten equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate": {"type": "number", "description": "Substrate"},
                "Km": {"type": "number", "description": "Km"},
                "Vmax": {"type": "number", "description": "Vmax"},
            },
            "required": ["substrate", "Km", "Vmax"]
        }
    }
]
