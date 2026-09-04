"""
Microscopy Tools - L3 Implementation

Functions for SEM, TEM, AFM, and STM calculations.

Source: LibreTexts Instrumental Analysis Ch21 + Surface Science (Nix) Ch7

## Solver Instructions (for AI Agent)

When you encounter microscopy problems (electron wavelength, resolution, AFM/STM), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given accelerating voltage -> calculate electron wavelength?
- Given wavelength -> calculate resolution limit?
- Given work function -> calculate STM tunneling current?
- Given cantilever properties -> calculate AFM spring constant?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Electron wavelength (non-relativistic) | `electron_wavelength_nonrelativistic(voltage_v)` | voltage in V -> returns pm (valid <100 kV) |
| Electron wavelength (relativistic) | `electron_wavelength_relativistic(voltage_v)` | voltage in V -> returns pm (all voltages) |
| TEM resolution limit | `tem_resolution_limit(wavelength_pm, alpha_rad)` | Abbe limit: d = 0.61lambda/sin(alpha) |
| AFM spring constant | `afm_cantilever_spring_constant(E, t, w, L)` | E=modulus, t=thickness, w=width, L=length |
| STM tunneling current | `stm_tunneling_current(I0, s, kappa)` | I = I0 x exp(-2κs), s=tip-sample distance |
| Aberration blur | `aberration_blur(Cs, alpha)` | Cs=spherical aberration coefficient |

### Step 3: Handle special cases
- Use relativistic formula for voltages >100 kV (TEM typically 200-300 kV)
- 100 kV -> lambda ~ 3.70 pm (relativistic), 3.88 pm (non-relativistic)
- STM: κ = √(2mφ/ℏ2) where φ is work function (~4-5 eV for metals)

### Examples
```python
# Example 1: Electron wavelength at 200 kV (TEM)
electron_wavelength_relativistic(200000)
# -> 2.51 pm

# Example 2: TEM resolution limit
tem_resolution_limit(2.51, 0.01)  # lambda=2.51 pm, alpha=0.01 rad
# -> ~153 pm

# Example 3: AFM cantilever spring constant
afm_cantilever_spring_constant(170e9, 1e-6, 30e-6, 100e-6)  # Si cantilever
# -> ~0.51 N/m
```
"""

from typing import Tuple, Optional, Dict, List, Union
from dataclasses import dataclass
import math


# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
REDUCED_PLANCK = 1.054571817e-34  # J·s
ELECTRON_MASS = 9.1093837015e-31  # kg
ELECTRON_CHARGE = 1.602176634e-19  # C
SPEED_OF_LIGHT = 2.99792458e8  # m/s
ELECTRON_REST_ENERGY_EV = 510.998950  # keV


# =============================================================================
# ELECTRON WAVELENGTH FUNCTIONS
# =============================================================================

def electron_wavelength_nonrelativistic(voltage_v: float) -> float:
    """
    Calculate electron wavelength using non-relativistic equation.
    
    lambda = h / √(2m_e x eV)
    
    Valid for voltages < 100 kV. For higher voltages, use relativistic version.
    
    Parameters
    ----------
    voltage_v : float
        Accelerating voltage in volts
    
    Returns
    -------
    float
        Wavelength in picometers
    
    Raises
    ------
    ValueError
        If voltage is not positive
    
    Examples
    --------
    >>> round(electron_wavelength_nonrelativistic(100000), 2)
    3.88
    >>> round(electron_wavelength_nonrelativistic(50000), 2)
    5.49
    >>> round(electron_wavelength_nonrelativistic(1000), 1)
    38.8
    """
    if voltage_v <= 0:
        raise ValueError(f"Voltage must be positive, got {voltage_v}")
    
    # lambda = h / √(2m x eV)
    momentum = math.sqrt(2 * ELECTRON_MASS * ELECTRON_CHARGE * voltage_v)
    wavelength_m = PLANCK_CONSTANT / momentum
    wavelength_pm = wavelength_m * 1e12  # Convert m to pm
    
    return round(wavelength_pm, 2)


def electron_wavelength_relativistic(voltage_v: float) -> float:
    """
    Calculate electron wavelength with relativistic corrections.
    
    lambda = h / √[2m_e x eV x (1 + eV/(2m_e c2))]
    
    Parameters
    ----------
    voltage_v : float
        Accelerating voltage in volts
    
    Returns
    -------
    float
        Wavelength in picometers
    
    Raises
    ------
    ValueError
        If voltage is not positive
    
    Examples
    --------
    >>> round(electron_wavelength_relativistic(100000), 2)
    3.70
    >>> round(electron_wavelength_relativistic(200000), 2)
    2.51
    >>> round(electron_wavelength_relativistic(300000), 2)
    1.96
    """
    if voltage_v <= 0:
        raise ValueError(f"Voltage must be positive, got {voltage_v}")
    
    # Energy in eV
    energy_ev = voltage_v  # eV = V for electrons
    
    # Relativistic correction factor: (1 + eV/(2m_e c2))
    # m_e c2 = 511 keV
    relativistic_factor = 1 + energy_ev / (2 * ELECTRON_REST_ENERGY_EV * 1000)
    
    # Corrected momentum
    momentum = math.sqrt(2 * ELECTRON_MASS * ELECTRON_CHARGE * voltage_v * relativistic_factor)
    wavelength_m = PLANCK_CONSTANT / momentum
    wavelength_pm = wavelength_m * 1e12
    
    return round(wavelength_pm, 2)


# =============================================================================
# RESOLUTION FUNCTIONS
# =============================================================================

def abbe_resolution_limit(wavelength_nm: float, na: float) -> float:
    """
    Calculate the Abbe diffraction-limited resolution.
    
    d = lambda / (2 x NA)
    
    Parameters
    ----------
    wavelength_nm : float
        Wavelength in nanometers
    na : float
        Numerical aperture (n x sin θ)
    
    Returns
    -------
    float
        Resolution in nanometers
    
    Raises
    ------
    ValueError
        If wavelength or NA is not positive
    
    Examples
    --------
    >>> round(abbe_resolution_limit(550, 1.4), 0)
    196.0
    >>> round(abbe_resolution_limit(400, 1.0), 0)
    200.0
    >>> round(abbe_resolution_limit(550, 0.4), 0)
    688.0
    """
    if wavelength_nm <= 0:
        raise ValueError(f"Wavelength must be positive, got {wavelength_nm}")
    if na <= 0:
        raise ValueError(f"NA must be positive, got {na}")
    
    resolution = wavelength_nm / (2 * na)
    return round(resolution, 0)


def sem_resolution(working_distance_mm: float, beam_voltage_kv: float, 
                   aperture_angle_rad: float = 0.01) -> float:
    """
    Calculate theoretical SEM resolution.
    
    d = 0.753 / (alpha x √V)
    
    Parameters
    ----------
    working_distance_mm : float
        Working distance in mm (affects effective aperture)
    beam_voltage_kv : float
        Beam accelerating voltage in kV
    aperture_angle_rad : float
        Aperture half-angle in radians (default 0.01)
    
    Returns
    -------
    float
        Theoretical resolution in nanometers
    
    Raises
    ------
    ValueError
        If any parameter is not positive
    
    Examples
    --------
    >>> round(sem_resolution(10, 20), 1)
    16.8
    >>> round(sem_resolution(10, 30), 1)
    13.7
    >>> round(sem_resolution(10, 10), 1)
    23.8
    """
    if working_distance_mm <= 0:
        raise ValueError(f"Working distance must be positive, got {working_distance_mm}")
    if beam_voltage_kv <= 0:
        raise ValueError(f"Beam voltage must be positive, got {beam_voltage_kv}")
    if aperture_angle_rad <= 0:
        raise ValueError(f"Aperture angle must be positive, got {aperture_angle_rad}")
    
    # d = 0.753 / (alpha x √V) in nm
    resolution = 0.753 / (aperture_angle_rad * math.sqrt(beam_voltage_kv))
    return round(resolution, 1)


def tem_resolution(spherical_aberration_mm: float, voltage_kv: float,
                   coefficient: float = 0.43) -> float:
    """
    Calculate TEM resolution limited by spherical aberration.
    
    delta = A x Cs^(1/4) x lambda^(3/4)
    
    Parameters
    ----------
    spherical_aberration_mm : float
        Spherical aberration coefficient in mm
    voltage_kv : float
        Accelerating voltage in kV
    coefficient : float
        Resolution coefficient (default 0.43, Rayleigh-like criterion)
    
    Returns
    -------
    float
        Resolution in nanometers
    
    Raises
    ------
    ValueError
        If Cs or voltage is not positive
    
    Examples
    --------
    >>> round(tem_resolution(1.0, 200), 2)
    0.19
    >>> round(tem_resolution(2.0, 100), 2)
    0.32
    """
    if spherical_aberration_mm <= 0:
        raise ValueError(f"Cs must be positive, got {spherical_aberration_mm}")
    if voltage_kv <= 0:
        raise ValueError(f"Voltage must be positive, got {voltage_kv}")
    
    # Get relativistic wavelength in pm
    wavelength_pm = electron_wavelength_relativistic(voltage_kv * 1000)
    wavelength_nm = wavelength_pm / 1000  # Convert pm to nm
    
    # delta = A x Cs^(1/4) x lambda^(3/4)
    # Cs in mm, lambda in nm - result in nm
    cs_nm = spherical_aberration_mm * 1e6  # Convert mm to nm
    resolution = coefficient * (cs_nm ** 0.25) * (wavelength_nm ** 0.75)
    
    return round(resolution, 2)


# =============================================================================
# MAGNIFICATION FUNCTIONS
# =============================================================================

def sem_magnification(display_size_mm: float, sample_size_mm: float) -> float:
    """
    Calculate SEM magnification.
    
    M = L_display / L_sample
    
    Parameters
    ----------
    display_size_mm : float
        Display size in mm
    sample_size_mm : float
        Actual sample size scanned in mm
    
    Returns
    -------
    float
        Magnification factor
    
    Raises
    ------
    ValueError
        If either size is not positive
    
    Examples
    --------
    >>> sem_magnification(100, 0.001)
    100000.0
    >>> sem_magnification(100, 1)
    100.0
    >>> sem_magnification(200, 0.0001)
    2000000.0
    """
    if display_size_mm <= 0:
        raise ValueError(f"Display size must be positive, got {display_size_mm}")
    if sample_size_mm <= 0:
        raise ValueError(f"Sample size must be positive, got {sample_size_mm}")
    
    return display_size_mm / sample_size_mm


# =============================================================================
# AFM FUNCTIONS
# =============================================================================

def afm_force(spring_constant_n_m: float, deflection_nm: float) -> float:
    """
    Calculate AFM cantilever force using Hooke's law.
    
    F = k x x
    
    Parameters
    ----------
    spring_constant_n_m : float
        Cantilever spring constant in N/m
    deflection_nm : float
        Cantilever deflection in nanometers
    
    Returns
    -------
    float
        Force in nanonewtons
    
    Raises
    ------
    ValueError
        If spring constant or deflection is negative
    
    Examples
    --------
    >>> round(afm_force(0.5, 10), 1)
    5.0
    >>> round(afm_force(2.0, 5), 1)
    10.0
    >>> round(afm_force(0.1, 100), 1)
    10.0
    """
    if spring_constant_n_m < 0:
        raise ValueError(f"Spring constant cannot be negative, got {spring_constant_n_m}")
    if deflection_nm < 0:
        raise ValueError(f"Deflection cannot be negative, got {deflection_nm}")
    
    # Convert nm to m, calculate force, then convert N to nN
    deflection_m = deflection_nm * 1e-9
    force_n = spring_constant_n_m * deflection_m  # Force in N
    force_nn = force_n * 1e9  # Convert to nN
    
    return round(force_nn, 1)


def afm_resolution(tip_radius_nm: float, feature_depth_nm: float) -> float:
    """
    Estimate AFM lateral resolution limited by tip geometry.
    
    delta ~ √(R x D)
    
    Parameters
    ----------
    tip_radius_nm : float
        AFM tip radius in nanometers
    feature_depth_nm : float
        Feature depth/height in nanometers
    
    Returns
    -------
    float
        Estimated lateral resolution in nanometers
    
    Raises
    ------
    ValueError
        If tip radius or feature depth is not positive
    
    Examples
    --------
    >>> round(afm_resolution(10, 5), 1)
    7.1
    >>> round(afm_resolution(20, 2), 1)
    6.3
    >>> round(afm_resolution(5, 10), 1)
    7.1
    """
    if tip_radius_nm <= 0:
        raise ValueError(f"Tip radius must be positive, got {tip_radius_nm}")
    if feature_depth_nm <= 0:
        raise ValueError(f"Feature depth must be positive, got {feature_depth_nm}")
    
    resolution = math.sqrt(tip_radius_nm * feature_depth_nm)
    return round(resolution, 1)


def afm_spring_constant(
    youngs_modulus_pa: float,
    width_um: float,
    thickness_um: float,
    length_um: float
) -> float:
    """
    Calculate cantilever spring constant from geometry.
    
    k = E x w x t3 / (4 x L3)
    
    For a rectangular cantilever beam.
    
    Parameters
    ----------
    youngs_modulus_pa : float
        Young's modulus in Pa
    width_um : float
        Cantilever width in micrometers
    thickness_um : float
        Cantilever thickness in micrometers
    length_um : float
        Cantilever length in micrometers
    
    Returns
    -------
    float
        Spring constant in N/m
    
    Raises
    ------
    ValueError
        If any dimension is not positive
    
    Examples
    --------
    >>> # Silicon cantilever: E = 170 GPa, w=30um, t=1um, L=200um
    >>> round(afm_spring_constant(170e9, 30, 1, 200), 2)
    0.04
    >>> # Stiffer cantilever: thicker
    >>> round(afm_spring_constant(170e9, 30, 2, 200), 2)
    0.29
    """
    if youngs_modulus_pa <= 0:
        raise ValueError(f"Young's modulus must be positive, got {youngs_modulus_pa}")
    if width_um <= 0:
        raise ValueError(f"Width must be positive, got {width_um}")
    if thickness_um <= 0:
        raise ValueError(f"Thickness must be positive, got {thickness_um}")
    if length_um <= 0:
        raise ValueError(f"Length must be positive, got {length_um}")
    
    # Convert to meters
    w = width_um * 1e-6
    t = thickness_um * 1e-6
    L = length_um * 1e-6
    
    # k = E x w x t3 / (4 x L3)
    k = youngs_modulus_pa * w * (t ** 3) / (4 * (L ** 3))
    
    return round(k, 2)


# =============================================================================
# STM FUNCTIONS
# =============================================================================

def stm_tunneling_current(
    bias_voltage_v: float,
    distance_nm: float,
    constant_c: float = 10.0
) -> float:
    """
    Calculate STM tunneling current.
    
    I_t = V x e^(-C x d)
    
    Returns relative current (arbitrary units).
    
    Parameters
    ----------
    bias_voltage_v : float
        Bias voltage in volts
    distance_nm : float
        Tip-sample distance in nanometers
    constant_c : float
        Decay constant in nm-1 (default 10 for metals)
    
    Returns
    -------
    float
        Relative tunneling current (arbitrary units)
    
    Raises
    ------
    ValueError
        If bias voltage or distance is negative, or C not positive
    
    Examples
    --------
    >>> round(stm_tunneling_current(1.0, 0.5), 2)
    0.01
    >>> round(stm_tunneling_current(1.0, 0.3), 3)
    0.050
    >>> round(stm_tunneling_current(0.5, 0.5), 2)
    0.00
    """
    if bias_voltage_v < 0:
        raise ValueError(f"Bias voltage cannot be negative, got {bias_voltage_v}")
    if distance_nm < 0:
        raise ValueError(f"Distance cannot be negative, got {distance_nm}")
    if constant_c <= 0:
        raise ValueError(f"Constant C must be positive, got {constant_c}")
    
    current = bias_voltage_v * math.exp(-constant_c * distance_nm)
    return round(current, 3)


def stm_current_ratio(
    distance_change_nm: float,
    constant_c: float = 10.0
) -> float:
    """
    Calculate ratio of tunneling currents for a distance change.
    
    I2/I1 = e^(C x Deltad)
    
    Positive Deltad means moving away (current decreases).
    
    Parameters
    ----------
    distance_change_nm : float
        Change in tip-sample distance in nm (positive = moving away)
    constant_c : float
        Decay constant in nm-1 (default 10 for metals)
    
    Returns
    -------
    float
        Current ratio (factor by which current changes)
    
    Raises
    ------
    ValueError
        If C is not positive
    
    Examples
    --------
    >>> round(stm_current_ratio(0.1), 1)
    2.7
    >>> round(stm_current_ratio(-0.1), 1)
    0.4
    >>> round(stm_current_ratio(0.2), 1)
    7.4
    """
    if constant_c <= 0:
        raise ValueError(f"Constant C must be positive, got {constant_c}")
    
    ratio = math.exp(constant_c * distance_change_nm)
    return round(ratio, 1)


# =============================================================================
# DEPTH OF FIELD FUNCTIONS
# =============================================================================

def depth_of_field(wavelength_nm: float, na: float) -> float:
    """
    Calculate depth of field for optical microscopy.
    
    DOF = lambda / (2 x NA2)
    
    Parameters
    ----------
    wavelength_nm : float
        Wavelength in nanometers
    na : float
        Numerical aperture
    
    Returns
    -------
    float
        Depth of field in nanometers
    
    Raises
    ------
    ValueError
        If wavelength or NA is not positive
    
    Examples
    --------
    >>> round(depth_of_field(550, 1.4), 0)
    140.0
    >>> round(depth_of_field(550, 0.4), 0)
    1719.0
    >>> round(depth_of_field(400, 1.0), 0)
    200.0
    """
    if wavelength_nm <= 0:
        raise ValueError(f"Wavelength must be positive, got {wavelength_nm}")
    if na <= 0:
        raise ValueError(f"NA must be positive, got {na}")
    
    dof = wavelength_nm / (2 * na ** 2)
    return round(dof, 0)


def numerical_aperture(refractive_index: float, half_angle_deg: float) -> float:
    """
    Calculate numerical aperture.
    
    NA = n x sin(θ)
    
    Parameters
    ----------
    refractive_index : float
        Refractive index of medium
    half_angle_deg : float
        Half-angle of light cone in degrees
    
    Returns
    -------
    float
        Numerical aperture
    
    Raises
    ------
    ValueError
        If refractive index not positive or angle out of range
    
    Examples
    --------
    >>> round(numerical_aperture(1.0, 60), 2)
    0.87
    >>> round(numerical_aperture(1.5, 72), 2)
    1.43
    >>> round(numerical_aperture(1.0, 90), 2)
    1.0
    """
    if refractive_index <= 0:
        raise ValueError(f"Refractive index must be positive, got {refractive_index}")
    if half_angle_deg < 0 or half_angle_deg > 90:
        raise ValueError(f"Half-angle must be 0-90deg, got {half_angle_deg}")
    
    half_angle_rad = math.radians(half_angle_deg)
    na = refractive_index * math.sin(half_angle_rad)
    return round(na, 2)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def wavelength_from_voltage_simplified(voltage_kv: float) -> float:
    """
    Simplified electron wavelength calculation returning nm.
    
    lambda (nm) = 1.23 / √V
    
    Use for quick estimates; use relativistic version for accuracy.
    
    Parameters
    ----------
    voltage_kv : float
        Accelerating voltage in kV
    
    Returns
    -------
    float
        Wavelength in nanometers
    
    Raises
    ------
    ValueError
        If voltage is not positive
    
    Examples
    --------
    >>> round(wavelength_from_voltage_simplified(100), 3)
    0.123
    >>> round(wavelength_from_voltage_simplified(200), 3)
    0.087
    """
    if voltage_kv <= 0:
        raise ValueError(f"Voltage must be positive, got {voltage_kv}")
    
    wavelength_nm = 1.23 / math.sqrt(voltage_kv)
    return round(wavelength_nm, 3)


def compare_optical_electron_resolution(
    optical_wavelength_nm: float,
    optical_na: float,
    electron_voltage_kv: float,
    electron_aperture: float = 0.01
) -> Dict[str, float]:
    """
    Compare resolution between optical and electron microscopy.
    
    Parameters
    ----------
    optical_wavelength_nm : float
        Optical wavelength in nm
    optical_na : float
        Optical numerical aperture
    electron_voltage_kv : float
        Electron accelerating voltage in kV
    electron_aperture : float
        Electron beam aperture angle in radians (default 0.01)
    
    Returns
    -------
    Dict[str, float]
        Dictionary with optical and electron resolutions in nm
    
    Raises
    ------
    ValueError
        If any parameter is not positive
    
    Examples
    --------
    >>> result = compare_optical_electron_resolution(550, 1.4, 200, 0.01)
    >>> round(result['optical_resolution_nm'], 0)
    196.0
    >>> round(result['electron_resolution_nm'], 1)
    5.3
    """
    if optical_wavelength_nm <= 0:
        raise ValueError(f"Optical wavelength must be positive, got {optical_wavelength_nm}")
    if optical_na <= 0:
        raise ValueError(f"Optical NA must be positive, got {optical_na}")
    if electron_voltage_kv <= 0:
        raise ValueError(f"Electron voltage must be positive, got {electron_voltage_kv}")
    if electron_aperture <= 0:
        raise ValueError(f"Electron aperture must be positive, got {electron_aperture}")
    
    optical_res = abbe_resolution_limit(optical_wavelength_nm, optical_na)
    electron_res = sem_resolution(10, electron_voltage_kv, electron_aperture)  # Use default working distance
    
    improvement_factor = optical_res / electron_res
    
    return {
        'optical_resolution_nm': optical_res,
        'electron_resolution_nm': electron_res,
        'improvement_factor': round(improvement_factor, 1)
    }


def optimal_tem_aperture(voltage_kv: float, spherical_aberration_mm: float) -> float:
    """
    Calculate optimal aperture angle for TEM.
    
    beta_optimal = (lambda/Cs)^(1/4)
    
    Parameters
    ----------
    voltage_kv : float
        Accelerating voltage in kV
    spherical_aberration_mm : float
        Spherical aberration coefficient in mm
    
    Returns
    -------
    float
        Optimal semi-angle in milliradians
    
    Raises
    ------
    ValueError
        If voltage or Cs is not positive
    
    Examples
    --------
    >>> round(optimal_tem_aperture(200, 1.0), 1)
    7.5
    """
    if voltage_kv <= 0:
        raise ValueError(f"Voltage must be positive, got {voltage_kv}")
    if spherical_aberration_mm <= 0:
        raise ValueError(f"Cs must be positive, got {spherical_aberration_mm}")
    
    # Get wavelength in nm
    wavelength_pm = electron_wavelength_relativistic(voltage_kv * 1000)
    wavelength_nm = wavelength_pm / 1000
    
    # Cs in nm
    cs_nm = spherical_aberration_mm * 1e6
    
    # beta = (lambda/Cs)^(1/4) in radians
    beta_rad = (wavelength_nm / cs_nm) ** 0.25
    
    # Convert to milliradians
    beta_mrad = beta_rad * 1000
    
    return round(beta_mrad, 1)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class MicroscopeSpecs:
    """Microscope specifications container."""
    name: str
    type: str  # 'optical', 'SEM', 'TEM', 'AFM', 'STM'
    resolution_nm: float
    magnification_range: Tuple[float, float]
    notes: str = ""


# Common microscope specifications
COMMON_MICROSCOPES = {
    'optical_100x': MicroscopeSpecs(
        name='Optical Microscope 100x Oil',
        type='optical',
        resolution_nm=200,
        magnification_range=(100, 1000),
        notes='NA=1.4, green light'
    ),
    'sem_standard': MicroscopeSpecs(
        name='Standard SEM',
        type='SEM',
        resolution_nm=3,
        magnification_range=(10, 300000),
        notes='20-30 kV, tungsten filament'
    ),
    'sem_fe': MicroscopeSpecs(
        name='Field Emission SEM',
        type='SEM',
        resolution_nm=1,
        magnification_range=(10, 1000000),
        notes='1-30 kV, field emission source'
    ),
    'tem_standard': MicroscopeSpecs(
        name='Standard TEM',
        type='TEM',
        resolution_nm=0.2,
        magnification_range=(1000, 1000000),
        notes='200 kV, LaB6 source'
    ),
    'tem_hr': MicroscopeSpecs(
        name='High Resolution TEM',
        type='TEM',
        resolution_nm=0.08,
        magnification_range=(1000, 2000000),
        notes='300 kV, Cs-corrected'
    ),
    'afm_standard': MicroscopeSpecs(
        name='AFM',
        type='AFM',
        resolution_nm=0.5,
        magnification_range=(1, 100000),  # Equivalent lateral magnification
        notes='Tapping mode, Si tip'
    ),
    'stm_standard': MicroscopeSpecs(
        name='STM',
        type='STM',
        resolution_nm=0.01,
        magnification_range=(1, 1000000),
        notes='UHV, atomic resolution'
    ),
}


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="abbe_resolution_limit",
            description="Calculate the Abbe diffraction-limited resolution.",
            input_schema=[
            InputSchemaField(name="wavelength_nm", type="number", required=True),
            InputSchemaField(name="na", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="afm_force",
            description="Calculate AFM cantilever force using Hooke's law.",
            input_schema=[
            InputSchemaField(name="spring_constant_n_m", type="number", required=True),
            InputSchemaField(name="deflection_nm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="afm_resolution",
            description="Estimate AFM lateral resolution limited by tip geometry.",
            input_schema=[
            InputSchemaField(name="tip_radius_nm", type="number", required=True),
            InputSchemaField(name="feature_depth_nm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="afm_spring_constant",
            description="Calculate cantilever spring constant from geometry.",
            input_schema=[
            InputSchemaField(name="youngs_modulus_pa", type="number", required=True),
            InputSchemaField(name="width_um", type="number", required=True),
            InputSchemaField(name="thickness_um", type="number", required=True),
            InputSchemaField(name="length_um", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="compare_optical_electron_resolution",
            description="Compare resolution between optical and electron microscopy.",
            input_schema=[
            InputSchemaField(name="optical_wavelength_nm", type="number", required=True),
            InputSchemaField(name="optical_na", type="number", required=True),
            InputSchemaField(name="electron_voltage_kv", type="number", required=True),
            InputSchemaField(name="electron_aperture", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="depth_of_field",
            description="Calculate depth of field for optical microscopy.",
            input_schema=[
            InputSchemaField(name="wavelength_nm", type="number", required=True),
            InputSchemaField(name="na", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="electron_wavelength_nonrelativistic",
            description="Calculate electron wavelength using non-relativistic equation.",
            input_schema=[
            InputSchemaField(name="voltage_v", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="electron_wavelength_relativistic",
            description="Calculate electron wavelength with relativistic corrections.",
            input_schema=[
            InputSchemaField(name="voltage_v", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="numerical_aperture",
            description="Calculate numerical aperture.",
            input_schema=[
            InputSchemaField(name="refractive_index", type="number", required=True),
            InputSchemaField(name="half_angle_deg", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="optimal_tem_aperture",
            description="Calculate optimal aperture angle for TEM.",
            input_schema=[
            InputSchemaField(name="voltage_kv", type="number", required=True),
            InputSchemaField(name="spherical_aberration_mm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="sem_magnification",
            description="Calculate SEM magnification.",
            input_schema=[
            InputSchemaField(name="display_size_mm", type="number", required=True),
            InputSchemaField(name="sample_size_mm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="sem_resolution",
            description="Calculate theoretical SEM resolution.",
            input_schema=[
            InputSchemaField(name="working_distance_mm", type="number", required=True),
            InputSchemaField(name="beam_voltage_kv", type="number", required=True),
            InputSchemaField(name="aperture_angle_rad", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="stm_current_ratio",
            description="Calculate ratio of tunneling currents for a distance change.",
            input_schema=[
            InputSchemaField(name="distance_change_nm", type="number", required=True),
            InputSchemaField(name="constant_c", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="stm_tunneling_current",
            description="Calculate STM tunneling current.",
            input_schema=[
            InputSchemaField(name="bias_voltage_v", type="number", required=True),
            InputSchemaField(name="distance_nm", type="number", required=True),
            InputSchemaField(name="constant_c", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tem_resolution",
            description="Calculate TEM resolution limited by spherical aberration.",
            input_schema=[
            InputSchemaField(name="spherical_aberration_mm", type="number", required=True),
            InputSchemaField(name="voltage_kv", type="number", required=True),
            InputSchemaField(name="coefficient", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavelength_from_voltage_simplified",
            description="Simplified electron wavelength calculation returning nm.",
            input_schema=[
            InputSchemaField(name="voltage_kv", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
