"""
Chromatography Tools

Implements tools for:
1. Resolution calculation
2. Number of theoretical plates
3. Van Deemter equation
4. Retention factor
5. Selectivity factor
6. Internal standard quantitation

## Solver Instructions (for AI Agent)

When you encounter a chromatography problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Retention times: tR1, tR2 (minutes)
- Peak widths: w1, w2 (minutes) or width at half-height
- Dead time (tM): Time for unretained peak
- Column length: L (mm or cm)
- Linear velocity: u (cm/s)
- Peak areas: For quantitation
- Internal standard: Concentration and peak area

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate resolution from times | `resolution_from_times(tR1, tR2, w1, w2)` |
| Calculate resolution from parameters | `resolution_from_parameters(N, alpha, k)` |
| Calculate theoretical plates | `theoretical_plates(retention_time, width, use_half_height)` |
| Calculate plate height | `plate_height(L, N)` |
| Calculate retention factor | `retention_factor(tR, tM)` |
| Calculate selectivity factor | `selectivity_factor(k1, k2)` |
| Calculate linear velocity | `linear_velocity(column_length, dead_time)` |
| Van Deemter plate height | `van_deemter_height(A, B, C, u)` |
| Optimal velocity | `optimal_velocity(B, C)` |
| Minimum plate height | `minimum_plate_height(A, B, C)` |
| Check baseline separation | `baseline_separation_achieved(Rs)` |
| Internal standard concentration | `internal_standard_concentration(analyte_area, internal_std_area, internal_std_conc, response_factor)` |
| Response factor calculation | `response_factor(analyte_area, analyte_conc, internal_std_area, internal_std_conc)` |
| External standard concentration | `external_standard_concentration(analyte_area, slope, intercept)` |
| Peak asymmetry | `peak_asymmetry(leading_width, trailing_width)` |

### Step 3: Handle special cases
- **Baseline separation**: Rs >= 1.5
- **Theoretical plates formulas**: N = 16(tR/w)2 or N = 5.54(tR/w1/2)2
- **Retention factor**: k = (tR - tM)/tM
- **Selectivity**: alpha = k2/k1 (always > 1)
- **Van Deemter**: H = A + B/u + Cu

### Examples

**Example 1: Resolution**
Question: "Calculate resolution between two peaks with tR1 = 5.2 min, tR2 = 6.1 min, w1 = 0.3 min, w2 = 0.35 min."
- Solution: `resolution_from_times(tR1=5.2, tR2=6.1, w1=0.3, w2=0.35)` -> Rs = 2.77

**Example 2: Theoretical plates**
Question: "Calculate N for a peak with tR = 12.5 min and w = 0.4 min."
- Solution: `theoretical_plates(retention_time=12.5, width=0.4)` -> N = 15625

**Example 3: Retention factor**
Question: "What is the retention factor if tR = 10.0 min and tM = 1.0 min?"
- Solution: `retention_factor(tR=10.0, tM=1.0)` -> k = 9.0

**Example 4: Internal standard**
Question: "Calculate analyte concentration: analyte area = 50000, IS area = 40000, [IS] = 10.0 M, RF = 0.95."
- Solution: `internal_standard_concentration(analyte_area=50000, internal_std_area=40000, internal_std_conc=10.0, response_factor=0.95)` -> 11.88 M
"""

# Source: Instrumental Analysis (LibreTexts)

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import math


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ChromatographicPeak:
    """Represents a chromatographic peak."""
    retention_time: float  # minutes
    width: float  # minutes (baseline width)
    width_half_height: Optional[float] = None  # minutes
    height: Optional[float] = None  # arbitrary units
    area: Optional[float] = None  # arbitrary units
    name: Optional[str] = None


# ============================================================================
# RESOLUTION CALCULATIONS
# ============================================================================

def resolution_from_times(
    tR1: float,
    tR2: float,
    w1: float,
    w2: float
) -> float:
    """Calculate resolution between two peaks.
    
    Rs = (tR2 - tR1) / (0.5 x (w1 + w2))
    
    Args:
        tR1: Retention time of peak 1 (minutes)
        tR2: Retention time of peak 2 (minutes)
        w1: Baseline width of peak 1 (minutes)
        w2: Baseline width of peak 2 (minutes)
    
    Returns:
        Resolution (Rs)
    
    Example:
        >>> resolution_from_times(5.2, 6.1, 0.3, 0.35)
        2.77
    """
    if tR1 >= tR2:
        raise ValueError("tR2 must be greater than tR1")
    
    delta_t = tR2 - tR1
    avg_width = 0.5 * (w1 + w2)
    
    return round(delta_t / avg_width, 2)


def resolution_from_parameters(
    N: float,
    alpha: float,
    k: float
) -> float:
    """Calculate resolution from plate count, selectivity, and retention factor.
    
    Rs = (sqrt(N) / 4) * (alpha - 1)/alpha * k/(1 + k)
    
    Args:
        N: Number of theoretical plates
        alpha: Selectivity factor (k2/k1)
        k: Average retention factor
    
    Returns:
        Resolution (Rs)
    """
    if alpha <= 1:
        raise ValueError("Selectivity factor must be > 1 for separation")
    
    term1 = math.sqrt(N) / 4
    term2 = (alpha - 1) / alpha
    term3 = k / (1 + k)
    
    return round(term1 * term2 * term3, 2)


def baseline_separation_achieved(Rs: float) -> bool:
    """Check if baseline separation is achieved.
    
    Args:
        Rs: Resolution value
    
    Returns:
        True if Rs >= 1.5 (baseline separation)
    """
    return Rs >= 1.5


# ============================================================================
# THEORETICAL PLATES
# ============================================================================

def theoretical_plates(
    retention_time: float,
    width: float,
    use_half_height: bool = False,
    convention: str = "16"
) -> float:
    """Calculate number of theoretical plates.
    
    Using baseline width: N = C x (tR/w)2
    Using half-height width: N = 5.54 x (tR/w1/2)2
    
    Args:
        retention_time: Retention time (minutes)
        width: Peak width (minutes)
        use_half_height: If True, use formula for width at half height
        convention: Constant factor when using baseline width.
            "16" (default): N = 16(tR/w)^2 (w = baseline width, most common)
            "4": N = 4(tR/w)^2 (some textbooks, w = full baseline width measured differently)
    
    Returns:
        Number of theoretical plates (N)
    
    Example:
        >>> theoretical_plates(12.5, 0.4)
        15625.0
        >>> theoretical_plates(8.04, 0.15, convention="4")
        11492.0
    """
    if use_half_height:
        N = 5.54 * (retention_time / width) ** 2
    else:
        if convention == "4":
            C = 4
        else:
            C = 16
        N = C * (retention_time / width) ** 2
    
    return round(N, 0)


def plate_height(L: float, N: float) -> float:
    """Calculate plate height (height equivalent to theoretical plate).
    
    H = L / N
    
    Args:
        L: Column length (m)
        N: Number of theoretical plates
    
    Returns:
        Plate height (m)
    
    Example:
        >>> plate_height(0.25, 5000)
        5e-05
    """
    return L / N


# ============================================================================
# VAN DEEMTER EQUATION
# ============================================================================

def van_deemter_height(
    A: float,
    B: float,
    C: float,
    u: float
) -> float:
    """Calculate plate height from Van Deemter equation.
    
    H = A + B/u + Cu
    
    Args:
        A: Eddy diffusion term (cm)
        B: Longitudinal diffusion term (cm2/s)
        C: Mass transfer term (s)
        u: Linear velocity (cm/s)
    
    Returns:
        Plate height (cm)
    """
    return A + B / u + C * u


def optimal_velocity(B: float, C: float) -> float:
    """Calculate optimal linear velocity from Van Deemter parameters.
    
    u_opt = sqrt(B/C)
    
    Args:
        B: Longitudinal diffusion term (cm2/s)
        C: Mass transfer term (s)
    
    Returns:
        Optimal linear velocity (cm/s)
    
    Example:
        >>> optimal_velocity(0.5, 0.03)
        4.08
    """
    return round(math.sqrt(B / C), 2)


def minimum_plate_height(A: float, B: float, C: float) -> float:
    """Calculate minimum plate height at optimal velocity.
    
    H_min = A + 2sqrt(BC)
    
    Args:
        A: Eddy diffusion term (cm)
        B: Longitudinal diffusion term (cm2/s)
        C: Mass transfer term (s)
    
    Returns:
        Minimum plate height (cm)
    """
    return round(A + 2 * math.sqrt(B * C), 4)


# ============================================================================
# RETENTION AND SELECTIVITY
# ============================================================================

def retention_factor(tR: float, tM: float) -> float:
    """Calculate retention factor (capacity factor).
    
    k = (tR - tM) / tM
    
    Args:
        tR: Retention time (minutes)
        tM: Dead time (minutes)
    
    Returns:
        Retention factor (k)
    
    Example:
        >>> retention_factor(10.0, 1.0)
        9.0
    """
    if tR < tM:
        raise ValueError("Retention time must be >= dead time")
    
    return round((tR - tM) / tM, 2)


def selectivity_factor(k1: float, k2: float) -> float:
    """Calculate selectivity factor (separation factor).
    
    alpha = k2 / k1
    
    Args:
        k1: Retention factor for peak 1
        k2: Retention factor for peak 2
    
    Returns:
        Selectivity factor (alpha)
    
    Note: alpha > 1 indicates separation possible
    """
    if k2 < k1:
        raise ValueError("k2 should be greater than k1 for peak 2")
    
    return round(k2 / k1, 3)


def retention_time_from_k(k: float, tM: float) -> float:
    """Calculate retention time from retention factor.
    
    tR = tM x (1 + k)
    
    Args:
        k: Retention factor
        tM: Dead time (minutes)
    
    Returns:
        Retention time (minutes)
    """
    return round(tM * (1 + k), 2)


# ============================================================================
# QUANTITATIVE ANALYSIS
# ============================================================================

def internal_standard_concentration(
    analyte_area: float,
    internal_std_area: float,
    internal_std_conc: float,
    response_factor: float
) -> float:
    """Calculate analyte concentration using internal standard method.
    
    Cx = (Ax / Ais) x Cis x RF
    
    Args:
        analyte_area: Peak area of analyte
        internal_std_area: Peak area of internal standard
        internal_std_conc: Concentration of internal standard (M or other units)
        response_factor: Response factor (RF)
    
    Returns:
        Analyte concentration (same units as internal_std_conc)
    
    Example:
        >>> internal_standard_concentration(50000, 40000, 10.0, 0.95)
        11.88
    """
    area_ratio = analyte_area / internal_std_area
    return round(area_ratio * internal_std_conc * response_factor, 2)


def response_factor(
    analyte_area: float,
    analyte_conc: float,
    internal_std_area: float,
    internal_std_conc: float
) -> float:
    """Calculate response factor for internal standard method.
    
    RF = (Cx / Ax) x (Ais / Cis)
    
    Args:
        analyte_area: Peak area of analyte
        analyte_conc: Known concentration of analyte (calibration standard)
        internal_std_area: Peak area of internal standard
        internal_std_conc: Concentration of internal standard
    
    Returns:
        Response factor (RF)
    """
    return round((analyte_conc / analyte_area) * 
                 (internal_std_area / internal_std_conc), 4)


def external_standard_concentration(
    analyte_area: float,
    slope: float,
    intercept: float = 0
) -> float:
    """Calculate concentration from external standard calibration.
    
    C = (Area - intercept) / slope
    
    Args:
        analyte_area: Peak area of analyte
        slope: Slope of calibration curve
        intercept: Y-intercept of calibration curve (default 0)
    
    Returns:
        Concentration
    """
    return round((analyte_area - intercept) / slope, 4)


# ============================================================================
# PEAK ANALYSIS
# ============================================================================

def peak_asymmetry(
    leading_width: float,
    trailing_width: float
) -> float:
    """Calculate peak asymmetry factor (tailing factor).
    
    As = b / a
    
    Args:
        leading_width: Width from peak front to peak maximum
        trailing_width: Width from peak maximum to peak end
    
    Returns:
        Asymmetry factor (1.0 = symmetric)
    
    Interpretation:
        - As < 1: Fronting
        - As = 1: Symmetric
        - As > 1: Tailing
    """
    return round(trailing_width / leading_width, 2)


def is_peak_acceptable(
    asymmetry: float,
    min_asym: float = 0.9,
    max_asym: float = 1.5
) -> bool:
    """Check if peak shape is acceptable.
    
    Args:
        asymmetry: Peak asymmetry factor
        min_asym: Minimum acceptable asymmetry
        max_asym: Maximum acceptable asymmetry
    
    Returns:
        True if peak shape is acceptable
    """
    return min_asym <= asymmetry <= max_asym


# ============================================================================
# COLUMN PARAMETERS
# ============================================================================

def linear_velocity(
    column_length: float,
    dead_time: float
) -> float:
    """Calculate linear velocity.
    
    u = L / tM
    
    Args:
        column_length: Column length (cm)
        dead_time: Dead time (seconds)
    
    Returns:
        Linear velocity (cm/s)
    """
    return round(column_length / dead_time, 2)


def phase_ratio(
    V_m: float,
    V_s: float
) -> float:
    """Calculate phase ratio for chromatography.
    
    beta = V_m / V_s
    
    Args:
        V_m: Mobile phase volume (mL or L, same units as V_s)
        V_s: Stationary phase volume (mL or L, same units as V_m)
    
    Returns:
        Phase ratio (dimensionless)
    
    Example:
        >>> phase_ratio(2.0, 0.5)
        4.0
    """
    return V_m / V_s


# ============================================================================
# COMPREHENSIVE ANALYSIS
# ============================================================================

def analyze_peak_pair(
    peak1: ChromatographicPeak,
    peak2: ChromatographicPeak,
    tM: float,
    column_length: float
) -> Dict[str, float]:
    """Comprehensive analysis of a peak pair.
    
    Args:
        peak1: First peak
        peak2: Second peak
        tM: Dead time
        column_length: Column length (mm)
    
    Returns:
        Dictionary with all calculated parameters
    """
    k1 = retention_factor(peak1.retention_time, tM)
    k2 = retention_factor(peak2.retention_time, tM)
    
    N1 = theoretical_plates(peak1.retention_time, peak1.width)
    N2 = theoretical_plates(peak2.retention_time, peak2.width)
    
    alpha = selectivity_factor(k1, k2)
    avg_k = (k1 + k2) / 2
    
    Rs = resolution_from_times(
        peak1.retention_time,
        peak2.retention_time,
        peak1.width,
        peak2.width
    )
    
    return {
        'k1': k1,
        'k2': k2,
        'alpha': alpha,
        'N1': N1,
        'N2': N2,
        'H1_mm': plate_height(column_length, N1),
        'H2_mm': plate_height(column_length, N2),
        'Rs': Rs,
        'baseline_separation': baseline_separation_achieved(Rs),
        'avg_k': round(avg_k, 2)
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'analyze_peak_pair', 'description': 'Comprehensive analysis of a peak pair.\n\nArgs:\n    peak1: First peak\n    peak2: Second peak\n    tM: Dead time\n    column_length: Column length (mm)\n\nReturns:\n    Dictionary with all calculated parameters', 'inputSchema': {'type': 'object', 'properties': {'peak1': {'type': 'number', 'description': 'Peak1'}, 'peak2': {'type': 'number', 'description': 'Peak2'}, 'tM': {'type': 'number', 'description': 'Tm'}, 'column_length': {'type': 'string', 'description': 'Column Length'}}, 'required': ['peak1', 'peak2', 'tM', 'column_length']}},
    {'name': 'baseline_separation_achieved', 'description': 'Check if baseline separation is achieved.\n\nArgs:\n    Rs: Resolution value\n\nReturns:\n    true if Rs >= 1.5 (baseline separation)', 'inputSchema': {'type': 'object', 'properties': {'Rs': {'type': 'number', 'description': 'Rs'}}, 'required': ['Rs']}},
    {'name': 'external_standard_concentration', 'description': 'Calculate concentration from external standard calibration.\n\nC = (Area - intercept) / slope\n\nArgs:\n    analyte_area: Peak area of analyte\n    slope: Slope of calibration curve\n    intercept: Y-intercept of calibration curve (default 0)\n\nReturns:\n    Concentration', 'inputSchema': {'type': 'object', 'properties': {'analyte_area': {'type': 'string', 'description': 'Analyte Area'}, 'slope': {'type': 'number', 'description': 'Slope'}, 'intercept': {'type': 'number', 'description': 'Intercept', 'default': 0}}, 'required': ['analyte_area', 'slope']}},
    {'name': 'internal_standard_concentration', 'description': 'Calculate analyte concentration using internal standard method.\n\nCx = (Ax / Ais) x Cis x RF\n\nArgs:\n    analyte_area: Peak area of analyte\n    internal_std_area: Peak area of internal standard\n    internal_std_conc: Concentration of internal standard (M or other units)\n    response_factor: Response factor (RF)\n\nReturns:\n    Analyte concentration (same units as internal_std_conc)\n\nExample:\n    >>> internal_standard_concentration(50000, 40000, 10.0, 0.95)\n    11.88', 'inputSchema': {'type': 'object', 'properties': {'analyte_area': {'type': 'string', 'description': 'Analyte Area'}, 'internal_std_area': {'type': 'number', 'description': 'Internal Std Area'}, 'internal_std_conc': {'type': 'number', 'description': 'Internal Std Conc'}, 'response_factor': {'type': 'string', 'description': 'Response Factor'}}, 'required': ['analyte_area', 'internal_std_area', 'internal_std_conc', 'response_factor']}},
    {'name': 'is_peak_acceptable', 'description': 'Check if peak shape is acceptable.\n\nArgs:\n    asymmetry: Peak asymmetry factor\n    min_asym: Minimum acceptable asymmetry\n    max_asym: Maximum acceptable asymmetry\n\nReturns:\n    true if peak shape is acceptable', 'inputSchema': {'type': 'object', 'properties': {'asymmetry': {'type': 'string', 'description': 'Asymmetry'}, 'min_asym': {'type': 'number', 'description': 'Min Asym', 'default': 0.9}, 'max_asym': {'type': 'number', 'description': 'Max Asym', 'default': 1.5}}, 'required': ['asymmetry']}},
    {'name': 'linear_velocity', 'description': 'Calculate linear velocity.\n\nu = L / tM\n\nArgs:\n    column_length: Column length (cm)\n    dead_time: Dead time (seconds)\n\nReturns:\n    Linear velocity (cm/s)', 'inputSchema': {'type': 'object', 'properties': {'column_length': {'type': 'string', 'description': 'Column Length'}, 'dead_time': {'type': 'string', 'description': 'Dead Time'}}, 'required': ['column_length', 'dead_time']}},
    {'name': 'minimum_plate_height', 'description': 'Calculate minimum plate height at optimal velocity.\n\nH_min = A + 2sqrt(BC)\n\nArgs:\n    A: Eddy diffusion term (cm)\n    B: Longitudinal diffusion term (cm2/s)\n    C: Mass transfer term (s)\n\nReturns:\n    Minimum plate height (cm)', 'inputSchema': {'type': 'object', 'properties': {'A': {'type': 'number', 'description': 'A'}, 'B': {'type': 'number', 'description': 'B'}, 'C': {'type': 'number', 'description': 'C'}}, 'required': ['A', 'B', 'C']}},
    {'name': 'optimal_velocity', 'description': 'Calculate optimal linear velocity from Van Deemter parameters.\n\nu_opt = sqrt(B/C)\n\nArgs:\n    B: Longitudinal diffusion term (cm2/s)\n    C: Mass transfer term (s)\n\nReturns:\n    Optimal linear velocity (cm/s)\n\nExample:\n    >>> optimal_velocity(0.5, 0.03)\n    4.08', 'inputSchema': {'type': 'object', 'properties': {'B': {'type': 'number', 'description': 'B'}, 'C': {'type': 'number', 'description': 'C'}}, 'required': ['B', 'C']}},
    {'name': 'peak_asymmetry', 'description': 'Calculate peak asymmetry factor (tailing factor).\n\nAs = b / a\n\nArgs:\n    leading_width: Width from peak front to peak maximum\n    trailing_width: Width from peak maximum to peak end\n\nReturns:\n    Asymmetry factor (1.0 = symmetric)\n\nInterpretation:\n    - As < 1: Fronting\n    - As = 1: Symmetric\n    - As > 1: Tailing', 'inputSchema': {'type': 'object', 'properties': {'leading_width': {'type': 'string', 'description': 'Leading Width'}, 'trailing_width': {'type': 'string', 'description': 'Trailing Width'}}, 'required': ['leading_width', 'trailing_width']}},
    {'name': 'phase_ratio', 'description': 'Calculate phase ratio for capillary columns.\n\nbeta = r / (2 x df) = d / (4 x df)\n\nArgs:\n    column_diameter: Internal diameter (mm)\n    film_thickness: Film thickness (mum)\n\nReturns:\n    Phase ratio (dimensionless)', 'inputSchema': {'type': 'object', 'properties': {'column_diameter': {'type': 'string', 'description': 'Column Diameter'}, 'film_thickness': {'type': 'number', 'description': 'Film Thickness'}}, 'required': ['column_diameter', 'film_thickness']}},
    {'name': 'plate_height', 'description': 'Calculate plate height (height equivalent to theoretical plate).\n\nH = L / N\n\nArgs:\n    L: Column length (mm)\n    N: Number of theoretical plates\n\nReturns:\n    Plate height (mm)\n\nExample:\n    >>> plate_height(30000, 15625)\n    1.92', 'inputSchema': {'type': 'object', 'properties': {'L': {'type': 'number', 'description': 'L'}, 'N': {'type': 'number', 'description': 'N'}}, 'required': ['L', 'N']}},
    {'name': 'resolution_from_parameters', 'description': 'Calculate resolution from plate count, selectivity, and retention factor.\n\nRs = (sqrtN / 4) x (alpha - 1)/alpha x k/(1 + k)\n\nArgs:\n    N: Number of theoretical plates\n    alpha: Selectivity factor (k2/k1)\n    k: Average retention factor\n\nReturns:\n    Resolution (Rs)', 'inputSchema': {'type': 'object', 'properties': {'N': {'type': 'number', 'description': 'N'}, 'alpha': {'type': 'number', 'description': 'Alpha'}, 'k': {'type': 'number', 'description': 'K'}}, 'required': ['N', 'alpha', 'k']}},
    {'name': 'resolution_from_times', 'description': 'Calculate resolution between two peaks.\n\nRs = (tR2 - tR1) / (0.5 x (w1 + w2))\n\nArgs:\n    tR1: Retention time of peak 1 (minutes)\n    tR2: Retention time of peak 2 (minutes)\n    w1: Baseline width of peak 1 (minutes)\n    w2: Baseline width of peak 2 (minutes)\n\nReturns:\n    Resolution (Rs)\n\nExample:\n    >>> resolution_from_times(5.2, 6.1, 0.3, 0.35)\n    2.77', 'inputSchema': {'type': 'object', 'properties': {'tR1': {'type': 'number', 'description': 'Tr1'}, 'tR2': {'type': 'number', 'description': 'Tr2'}, 'w1': {'type': 'number', 'description': 'W1'}, 'w2': {'type': 'number', 'description': 'W2'}}, 'required': ['tR1', 'tR2', 'w1', 'w2']}},
    {'name': 'response_factor', 'description': 'Calculate response factor for internal standard method.\n\nRF = (Cx / Ax) x (Ais / Cis)\n\nArgs:\n    analyte_area: Peak area of analyte\n    analyte_conc: Known concentration of analyte (calibration standard)\n    internal_std_area: Peak area of internal standard\n    internal_std_conc: Concentration of internal standard\n\nReturns:\n    Response factor (RF)', 'inputSchema': {'type': 'object', 'properties': {'analyte_area': {'type': 'string', 'description': 'Analyte Area'}, 'analyte_conc': {'type': 'string', 'description': 'Analyte Conc'}, 'internal_std_area': {'type': 'number', 'description': 'Internal Std Area'}, 'internal_std_conc': {'type': 'number', 'description': 'Internal Std Conc'}}, 'required': ['analyte_area', 'analyte_conc', 'internal_std_area', 'internal_std_conc']}},
    {'name': 'retention_factor', 'description': 'Calculate retention factor (capacity factor).\n\nk = (tR - tM) / tM\n\nArgs:\n    tR: Retention time (minutes)\n    tM: Dead time (minutes)\n\nReturns:\n    Retention factor (k)\n\nExample:\n    >>> retention_factor(10.0, 1.0)\n    9.0', 'inputSchema': {'type': 'object', 'properties': {'tR': {'type': 'number', 'description': 'Tr'}, 'tM': {'type': 'number', 'description': 'Tm'}}, 'required': ['tR', 'tM']}},
    {'name': 'retention_time_from_k', 'description': 'Calculate retention time from retention factor.\n\ntR = tM x (1 + k)\n\nArgs:\n    k: Retention factor\n    tM: Dead time (minutes)\n\nReturns:\n    Retention time (minutes)', 'inputSchema': {'type': 'object', 'properties': {'k': {'type': 'number', 'description': 'K'}, 'tM': {'type': 'number', 'description': 'Tm'}}, 'required': ['k', 'tM']}},
    {'name': 'selectivity_factor', 'description': 'Calculate selectivity factor (separation factor).\n\nalpha = k2 / k1\n\nArgs:\n    k1: Retention factor for peak 1\n    k2: Retention factor for peak 2\n\nReturns:\n    Selectivity factor (alpha)\n\nNote: alpha > 1 indicates separation possible', 'inputSchema': {'type': 'object', 'properties': {'k1': {'type': 'number', 'description': 'K1'}, 'k2': {'type': 'number', 'description': 'K2'}}, 'required': ['k1', 'k2']}},
    {'name': 'theoretical_plates', 'description': 'Calculate number of theoretical plates.\n\nUsing baseline width: N = 16 x (tR/w)2\nUsing half-height width: N = 5.54 x (tR/w1/2)2\n\nArgs:\n    retention_time: Retention time (minutes)\n    width: Peak width (minutes)\n    use_half_height: If true, use formula for width at half height\n\nReturns:\n    Number of theoretical plates (N)\n\nExample:\n    >>> theoretical_plates(12.5, 0.4)\n    15625.0', 'inputSchema': {'type': 'object', 'properties': {'retention_time': {'type': 'string', 'description': 'Retention Time'}, 'width': {'type': 'string', 'description': 'Width'}, 'use_half_height': {'type': 'boolean', 'description': 'Use Half Height', 'default': False}}, 'required': ['retention_time', 'width']}},
    {'name': 'van_deemter_height', 'description': 'Calculate plate height from Van Deemter equation.\n\nH = A + B/u + Cu\n\nArgs:\n    A: Eddy diffusion term (cm)\n    B: Longitudinal diffusion term (cm2/s)\n    C: Mass transfer term (s)\n    u: Linear velocity (cm/s)\n\nReturns:\n    Plate height (cm)', 'inputSchema': {'type': 'object', 'properties': {'A': {'type': 'number', 'description': 'A'}, 'B': {'type': 'number', 'description': 'B'}, 'C': {'type': 'number', 'description': 'C'}, 'u': {'type': 'number', 'description': 'U'}}, 'required': ['A', 'B', 'C', 'u']}}
]
