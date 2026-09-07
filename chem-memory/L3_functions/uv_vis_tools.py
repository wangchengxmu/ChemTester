"""
UV-Visible Spectroscopy Tools

Implements tools for:
1. Beer-Lambert law calculations
2. Absorbance-transmittance conversions
3. Concentration determination
4. Dilution calculations

Source: Instrumental Analysis (LibreTexts)

## Solver Instructions (for AI Agent)

When you encounter UV-Vis spectroscopy problems - Beer-Lambert law, absorbance/transmittance conversions, concentration calculations, calibration curves, or multicomponent analysis - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given ε, path length, concentration -> calculate absorbance?
- Given absorbance, ε, path length -> calculate concentration?
- Given transmittance -> calculate absorbance or vice versa?
- Given calibration curve data -> determine concentration?
- Given absorbance of unknown -> check if in valid range?
- Given two components at two wavelengths -> calculate both concentrations?
- Given dilution information -> find original concentration?

### Step 2: Choose the correct function
- **Beer-Lambert absorbance:** `absorbance(epsilon, path_length, concentration)` -> A = εbc
- **Concentration from A:** `concentration_from_absorbance(A, epsilon, path_length=1.0)` -> c = A/(εb)
- **Molar absorptivity:** `molar_absorptivity(A, path_length, concentration)` -> ε = A/(bc)
- **Absorbance from T:** `absorbance_from_transmittance(T)` -> A = -log(T). T is 0-1 (not %)
- **Transmittance from A:** `transmittance_from_absorbance(A)` -> T = 10^(-A)
- **Percent transmittance:** `percent_transmittance_from_absorbance(A)` -> %T = 10^(-A) x 100
- **Calibration curve fit:** `calibration_curve_params(concentrations, absorbances)` -> (slope, intercept, R2)
- **Concentration from calibration:** `concentration_from_calibration(A, slope, intercept=0)` -> c = (A-intercept)/slope
- **Standard addition:** `standard_addition_concentration(sample_absorbance, spiked_absorbance, spike_concentration)` -> C_sample
- **Dilution factor:** `dilution_factor(final_volume, initial_volume)` -> Vf/Vi
- **Diluted concentration:** `diluted_concentration(initial_conc, dilution_factor)` -> Ci/DF
- **Original concentration:** `original_concentration(measured_conc, dilution_factor)` -> Cm x DF
- **Valid absorbance range:** `is_absorbance_valid(A, min_A=0.1, max_A=1.0)` -> bool
- **Recommended dilution:** `recommended_dilution(A_measured, target_A=0.5)` -> dilution factor
- **Two-component analysis:** `concentration_two_components(A1, A2, ε1_c1, ε1_c2, ε2_c1, ε2_c2, path_length=1.0)` -> (c1, c2) using Cramer's rule

### Step 3: Handle special cases
- A = 1.0 means only 10% light transmitted; A = 2.0 means 1% - very little light!
- Optimal absorbance range is 0.1–1.0 for best accuracy
- Transmittance T is a fraction (0-1), NOT a percentage - use percent_transmittance_from_absorbance for %
- For two-component analysis, choose wavelengths where ε ratios differ significantly

### Examples
```python
# Example 1: Calculate absorbance: ε=15000, b=1.0 cm, c=5x10-5 M
absorbance(15000, 1.0, 5e-5)  -> 0.75

# Example 2: 10% transmittance -> absorbance?
absorbance_from_transmittance(0.10)  -> 1.0

# Example 3: A=0.75, ε=15000, b=1.0 -> concentration?
concentration_from_absorbance(0.75, 15000, 1.0)  -> 5e-05 M

# Example 4: Sample diluted 10x, measured at 0.08 -> original concentration?
original_concentration(0.08, 10)  -> 0.8 (but may need further correction)
```
"""

from typing import Tuple, Optional
import math


# ============================================================================
# ABSORBANCE-TRANSMITTANCE CONVERSIONS
# ============================================================================

def absorbance_from_transmittance(T: float) -> float:
    """Calculate absorbance from transmittance.
    
    A = -log(T)
    
    Args:
        T: Transmittance (0-1, not percentage)
    
    Returns:
        Absorbance (dimensionless)
    
    Example:
        >>> absorbance_from_transmittance(0.10)
        1.0
    """
    if T <= 0 or T > 1:
        raise ValueError("Transmittance must be between 0 and 1")
    
    return round(-math.log10(T), 3)


def transmittance_from_absorbance(A: float) -> float:
    """Calculate transmittance from absorbance.
    
    T = 10^(-A)
    
    Args:
        A: Absorbance (dimensionless)
    
    Returns:
        Transmittance (0-1)
    
    Example:
        >>> transmittance_from_absorbance(1.0)
        0.1
    """
    if A < 0:
        raise ValueError("Absorbance cannot be negative")
    
    return round(10 ** (-A), 4)


def percent_transmittance_from_absorbance(A: float) -> float:
    """Calculate percent transmittance from absorbance.
    
    %T = 10^(-A) x 100
    
    Args:
        A: Absorbance
    
    Returns:
        Percent transmittance (0-100)
    """
    return round(transmittance_from_absorbance(A) * 100, 1)


# ============================================================================
# BEER-LAMBERT LAW
# ============================================================================

def absorbance(
    epsilon: float,
    path_length: float,
    concentration: float
) -> float:
    """Calculate absorbance from Beer-Lambert law.
    
    A = εbc
    
    Args:
        epsilon: Molar absorptivity (M-1cm-1)
        path_length: Path length (cm)
        concentration: Concentration (M)
    
    Returns:
        Absorbance (dimensionless)
    
    Example:
        >>> absorbance(15000, 1.0, 5e-5)
        0.75
    """
    return round(epsilon * path_length * concentration, 3)


def concentration_from_absorbance(
    A: float,
    epsilon: float,
    path_length: float = 1.0
) -> float:
    """Calculate concentration from absorbance.
    
    c = A / (εb)
    
    Args:
        A: Absorbance
        epsilon: Molar absorptivity (M-1cm-1)
        path_length: Path length (cm), default 1.0 cm
    
    Returns:
        Concentration (M)
    
    Example:
        >>> concentration_from_absorbance(0.75, 15000, 1.0)
        5e-05
    """
    if epsilon <= 0:
        raise ValueError("Molar absorptivity must be positive")
    
    return A / (epsilon * path_length)


def molar_absorptivity(
    A: float,
    path_length: float,
    concentration: float
) -> float:
    """Calculate molar absorptivity.
    
    ε = A / (bc)
    
    Args:
        A: Absorbance
        path_length: Path length (cm)
        concentration: Concentration (M)
    
    Returns:
        Molar absorptivity (M-1cm-1)
    """
    if concentration <= 0:
        raise ValueError("Concentration must be positive")
    
    return round(A / (path_length * concentration), 0)


# ============================================================================
# CALIBRATION CURVE
# ============================================================================

def concentration_from_calibration(
    A: float,
    slope: float,
    intercept: float = 0.0
) -> float:
    """Calculate concentration from calibration curve.
    
    c = (A - intercept) / slope
    
    Args:
        A: Absorbance
        slope: Slope of calibration curve (M-1)
        intercept: Y-intercept (default 0)
    
    Returns:
        Concentration (M)
    
    Example:
        >>> concentration_from_calibration(0.425, 12500, 0.02)
        3.24e-05
    """
    if slope <= 0:
        raise ValueError("Slope must be positive")
    
    return (A - intercept) / slope


def calibration_curve_params(
    concentrations: list,
    absorbances: list
) -> Tuple[float, float, float]:
    """Calculate calibration curve parameters by linear regression.
    
    Args:
        concentrations: List of concentrations
        absorbances: List of absorbances
    
    Returns:
        Tuple of (slope, intercept, R2)
    
    Example:
        >>> c = [1e-5, 2e-5, 3e-5, 4e-5]
        >>> A = [0.12, 0.24, 0.36, 0.48]
        >>> slope, intercept, r2 = calibration_curve_params(c, A)
    """
    if len(concentrations) != len(absorbances):
        raise ValueError("Lists must have same length")
    
    if len(concentrations) < 2:
        raise ValueError("Need at least 2 points for calibration")
    
    n = len(concentrations)
    
    # Calculate sums
    sum_x = sum(concentrations)
    sum_y = sum(absorbances)
    sum_xy = sum(c * a for c, a in zip(concentrations, absorbances))
    sum_x2 = sum(c ** 2 for c in concentrations)
    sum_y2 = sum(a ** 2 for a in absorbances)
    
    # Calculate slope and intercept
    denominator = n * sum_x2 - sum_x ** 2
    if denominator == 0:
        raise ValueError("Cannot calculate slope - concentration values may be identical")
    
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    
    # Calculate R2
    y_mean = sum_y / n
    ss_tot = sum((a - y_mean) ** 2 for a in absorbances)
    ss_res = sum((a - (slope * c + intercept)) ** 2 
                 for c, a in zip(concentrations, absorbances))
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
    
    return round(slope, 0), round(intercept, 4), round(r_squared, 4)


# ============================================================================
# STANDARD ADDITION
# ============================================================================

def standard_addition_concentration(
    sample_absorbance: float,
    spiked_absorbance: float,
    spike_concentration: float
) -> float:
    """Calculate sample concentration by standard addition.
    
    Csample = (Asample / Aspiked) x Cspike
    
    Args:
        sample_absorbance: Absorbance of original sample
        spiked_absorbance: Absorbance after adding standard
        spike_concentration: Concentration of added standard
    
    Returns:
        Original sample concentration
    
    Note: This is the simplified single-point addition
    """
    if spiked_absorbance <= sample_absorbance:
        raise ValueError("Spiked absorbance should be higher than sample")
    
    return round((sample_absorbance / spiked_absorbance) * spike_concentration, 6)


# ============================================================================
# DILUTION CALCULATIONS
# ============================================================================

def dilution_factor(
    final_volume: float,
    initial_volume: float
) -> float:
    """Calculate dilution factor.
    
    DF = Vf / Vi
    
    Args:
        final_volume: Volume after dilution
        initial_volume: Volume before dilution
    
    Returns:
        Dilution factor
    """
    return final_volume / initial_volume


def diluted_concentration(
    initial_conc: float,
    dilution_factor: float
) -> float:
    """Calculate concentration after dilution.
    
    Cf = Ci / DF
    
    Args:
        initial_conc: Initial concentration
        dilution_factor: Dilution factor
    
    Returns:
        Final concentration
    """
    return initial_conc / dilution_factor


def original_concentration(
    measured_conc: float,
    dilution_factor: float
) -> float:
    """Calculate original concentration from diluted measurement.
    
    Co = Cm x DF
    
    Args:
        measured_conc: Concentration measured
        dilution_factor: Dilution factor
    
    Returns:
        Original concentration
    """
    return measured_conc * dilution_factor


# ============================================================================
# ANALYSIS RANGE
# ============================================================================

def is_absorbance_valid(A: float, min_A: float = 0.1, max_A: float = 1.0) -> bool:
    """Check if absorbance is in optimal range.
    
    Args:
        A: Absorbance
        min_A: Minimum recommended absorbance
        max_A: Maximum recommended absorbance
    
    Returns:
        True if in optimal range
    
    Note: Absorbances outside 0.1-1.0 have higher relative error
    """
    return min_A <= A <= max_A


def recommended_dilution(
    A_measured: float,
    target_A: float = 0.5
) -> float:
    """Calculate recommended dilution factor to achieve target absorbance.
    
    Args:
        A_measured: Current absorbance
        target_A: Target absorbance (default 0.5, optimal range)
    
    Returns:
        Recommended dilution factor
    """
    if A_measured <= 0:
        raise ValueError("Absorbance must be positive")
    
    return round(A_measured / target_A, 1)


# ============================================================================
# MULTICOMPONENT ANALYSIS
# ============================================================================

def concentration_two_components(
    A1: float,
    A2: float,
    epsilon1_comp1: float,
    epsilon1_comp2: float,
    epsilon2_comp1: float,
    epsilon2_comp2: float,
    path_length: float = 1.0
) -> Tuple[float, float]:
    """Calculate concentrations of two components from absorbances at two wavelengths.
    
    Uses simultaneous equations:
    A1 = (ε1,1 x c1 + ε1,2 x c2) x b
    A2 = (ε2,1 x c1 + ε2,2 x c2) x b
    
    Args:
        A1: Absorbance at wavelength 1
        A2: Absorbance at wavelength 2
        epsilon1_comp1: Molar absorptivity of component 1 at lambda1
        epsilon1_comp2: Molar absorptivity of component 2 at lambda1
        epsilon2_comp1: Molar absorptivity of component 1 at lambda2
        epsilon2_comp2: Molar absorptivity of component 2 at lambda2
        path_length: Path length (cm)
    
    Returns:
        Tuple of (c1, c2) concentrations
    """
    # Divide out path length
    A1 = A1 / path_length
    A2 = A2 / path_length
    
    # Solve simultaneous equations using Cramer's rule
    det = epsilon1_comp1 * epsilon2_comp2 - epsilon2_comp1 * epsilon1_comp2
    
    if abs(det) < 1e-10:
        raise ValueError("Cannot solve - wavelengths may not be independent")
    
    c1 = (A1 * epsilon2_comp2 - A2 * epsilon1_comp2) / det
    c2 = (epsilon1_comp1 * A2 - epsilon2_comp1 * A1) / det
    
    return round(c1, 6), round(c2, 6)


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="absorbance",
            description="Calculate absorbance from Beer-Lambert law.",
            input_schema=[
            InputSchemaField(name="epsilon", type="number", required=True),
            InputSchemaField(name="path_length", type="number", required=True),
            InputSchemaField(name="concentration", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="absorbance_from_transmittance",
            description="Calculate absorbance from transmittance.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calibration_curve_params",
            description="Calculate calibration curve parameters by linear regression.",
            input_schema=[
            InputSchemaField(name="concentrations", type="number", required=True),
            InputSchemaField(name="absorbances", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="concentration_from_absorbance",
            description="Calculate concentration from absorbance.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True),
            InputSchemaField(name="epsilon", type="number", required=True),
            InputSchemaField(name="path_length", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="concentration_from_calibration",
            description="Calculate concentration from calibration curve.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True),
            InputSchemaField(name="slope", type="number", required=True),
            InputSchemaField(name="intercept", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="concentration_two_components",
            description="Calculate concentrations of two components from absorbances at two wavelengths.",
            input_schema=[
            InputSchemaField(name="A1", type="number", required=True),
            InputSchemaField(name="A2", type="number", required=True),
            InputSchemaField(name="epsilon1_comp1", type="number", required=True),
            InputSchemaField(name="epsilon1_comp2", type="number", required=True),
            InputSchemaField(name="epsilon2_comp1", type="number", required=True),
            InputSchemaField(name="epsilon2_comp2", type="number", required=True),
            InputSchemaField(name="path_length", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="diluted_concentration",
            description="Calculate concentration after dilution.",
            input_schema=[
            InputSchemaField(name="initial_conc", type="number", required=True),
            InputSchemaField(name="dilution_factor", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dilution_factor",
            description="Calculate dilution factor.",
            input_schema=[
            InputSchemaField(name="final_volume", type="number", required=True),
            InputSchemaField(name="initial_volume", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_absorbance_valid",
            description="Check if absorbance is in optimal range.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True),
            InputSchemaField(name="min_A", type="number", required=False),
            InputSchemaField(name="max_A", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molar_absorptivity",
            description="Calculate molar absorptivity.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True),
            InputSchemaField(name="path_length", type="number", required=True),
            InputSchemaField(name="concentration", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="original_concentration",
            description="Calculate original concentration from diluted measurement.",
            input_schema=[
            InputSchemaField(name="measured_conc", type="number", required=True),
            InputSchemaField(name="dilution_factor", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="percent_transmittance_from_absorbance",
            description="Calculate percent transmittance from absorbance.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="recommended_dilution",
            description="Calculate recommended dilution factor to achieve target absorbance.",
            input_schema=[
            InputSchemaField(name="A_measured", type="number", required=True),
            InputSchemaField(name="target_A", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="standard_addition_concentration",
            description="Calculate sample concentration by standard addition.",
            input_schema=[
            InputSchemaField(name="sample_absorbance", type="number", required=True),
            InputSchemaField(name="spiked_absorbance", type="number", required=True),
            InputSchemaField(name="spike_concentration", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="transmittance_from_absorbance",
            description="Calculate transmittance from absorbance.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
