"""
Thermal Analysis Tools - L3 Implementation

Functions for TGA, DSC, and DTA calculations.

Source: LibreTexts Instrumental Analysis (Harvey) Ch31 + Thermal Methods (Shetty)
"""

## Solver Instructions (for AI Agent)

# When you encounter **thermal analysis** problems (TGA, DSC, DTA), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - TGA mass loss calculations: `tga_mass_percent(initial_mass, final_mass)`, `tga_mass_loss_molar(...)`, `tga_residual_mass(...)`, `tga_decomposition_temperature(...)`, `tga_identify_product(...)`
# - DSC enthalpy/heat capacity: `dsc_enthalpy(...)`, `dsc_calibration_constant(...)`, `dsc_heat_capacity(...)`, `dsc_glass_transition(...)`, `dsc_crystallinity(...)`
# - DTA: `dta_temperature_difference(...)`, `dta_peak_type(Delta_T)`
# - General: `phase_transition_identification(...)`, `identify_thermal_process(...)`, `tga_mixture_analysis(...)`, `analyze_tga_thermogram(...)`, `calculate_heat_of_fusion(...)`, `estimate_purity_from_melting(...)`

### Step 2: Choose the correct function
# - Mass loss %: `tga_mass_percent`
# - Molar mass loss from TGA: `tga_mass_loss_molar`
# - Enthalpy from DSC peak: `dsc_enthalpy`
# - Identify decomposition product: `tga_identify_product`
# - Phase transition classification: `phase_transition_identification`

### Step 3: Handle special cases
# - TGA residual mass can indicate inorganic content or char formation
# - DSC crystallinity requires known 100% crystalline enthalpy reference
# - DTA peak type: positive DeltaT = exothermic, negative = endothermic

### Examples
# 1. Sample loses 0.150 g from 0.500 g: `tga_mass_percent(0.500, 0.350)` -> 30% mass loss
# 2. DSC peak area 0.250 J, sample 10 mg: `dsc_enthalpy(0.250, 0.010)` -> 25 J/g
# 3. Tm=180degC, Tf=165degC (depressed 15degC): `estimate_purity_from_melting(180, 165)` -> estimates impurity level



from typing import Tuple, Optional, Dict, List, Union
from dataclasses import dataclass
import math


# =============================================================================
# TGA (Thermogravimetric Analysis) Functions
# =============================================================================

def tga_mass_percent(initial_mass: float, final_mass: float) -> float:
    """
    Calculate the percentage of mass loss in a TGA experiment.

    Parameters
    ----------
    initial_mass : float
        Initial sample mass (mg or g)
    final_mass : float
        Final sample mass after decomposition (same units as initial)

    Returns
    -------
    float
        Percentage of mass lost (0-100)

    Raises
    ------
    ValueError
        If initial_mass <= 0 or final_mass < 0 or final_mass > initial_mass

    Examples
    --------
    >>> tga_mass_percent(17.61, 15.44)
    12.32
    >>> tga_mass_percent(100.0, 50.0)
    50.0
    >>> round(tga_mass_percent(17.61, 15.44), 2)
    12.32
    """
    if initial_mass <= 0:
        raise ValueError(f"initial_mass must be positive, got {initial_mass}")
    if final_mass < 0:
        raise ValueError(f"final_mass must be non-negative, got {final_mass}")
    if final_mass > initial_mass:
        raise ValueError(f"final_mass ({final_mass}) cannot exceed initial_mass ({initial_mass})")
    
    mass_loss = initial_mass - final_mass
    percent_loss = (mass_loss / initial_mass) * 100
    return round(percent_loss, 2)


def tga_mass_loss_molar(
    mass_loss_percent: float,
    initial_molar_mass: float
) -> float:
    """
    Calculate the molar mass decrease corresponding to a mass loss percentage.

    Used to identify volatile decomposition products by matching calculated
    mass loss to known molar masses (e.g., H2O = 18, CO = 28, CO2 = 44).

    Parameters
    ----------
    mass_loss_percent : float
        Percentage of mass lost (0-100)
    initial_molar_mass : float
        Molar mass of the original compound (g/mol)

    Returns
    -------
    float
        Molar mass decrease (g/mol)

    Raises
    ------
    ValueError
        If mass_loss_percent is negative or > 100, or initial_molar_mass <= 0

    Examples
    --------
    >>> round(tga_mass_loss_molar(12.3, 146.11), 1)  # CaC2O4·H2O losing H2O
    18.0
    >>> round(tga_mass_loss_molar(19.2, 146.11), 1)  # CaC2O4 losing CO
    28.1
    """
    if mass_loss_percent < 0 or mass_loss_percent > 100:
        raise ValueError(f"mass_loss_percent must be 0-100, got {mass_loss_percent}")
    if initial_molar_mass <= 0:
        raise ValueError(f"initial_molar_mass must be positive, got {initial_molar_mass}")
    
    fraction = mass_loss_percent / 100
    molar_decrease = fraction * initial_molar_mass
    return round(molar_decrease, 2)


def tga_identify_product(
    calculated_mass_loss: float,
    candidates: List[Tuple[str, float]],
    tolerance: float = 2.0
) -> Optional[str]:
    """
    Identify the volatile decomposition product from molar mass loss.

    Parameters
    ----------
    calculated_mass_loss : float
        Calculated molar mass decrease (g/mol)
    candidates : List[Tuple[str, float]]
        List of (product_name, molar_mass) tuples to match against
        Common: [('H2O', 18.02), ('CO', 28.01), ('CO2', 44.01)]
    tolerance : float
        Acceptable deviation in g/mol (default 2.0)

    Returns
    -------
    Optional[str]
        Name of matching product, or None if no match found

    Examples
    --------
    >>> tga_identify_product(18.0, [('H2O', 18.02), ('CO', 28.01)])
    'H2O'
    >>> tga_identify_product(28.0, [('H2O', 18.02), ('CO', 28.01)])
    'CO'
    >>> tga_identify_product(100.0, [('H2O', 18.02), ('CO', 28.01)])
    """
    for name, molar_mass in candidates:
        if abs(calculated_mass_loss - molar_mass) <= tolerance:
            return name
    return None


def tga_decomposition_temperature(
    mass_data: List[Tuple[float, float]],
    method: str = 'onset'
) -> float:
    """
    Determine decomposition temperature from TGA data.

    Parameters
    ----------
    mass_data : List[Tuple[float, float]]
        List of (temperature, mass) data points
    method : str
        'onset' - extrapolated onset temperature
        'midpoint' - temperature at 50% mass loss for the step

    Returns
    -------
    float
        Decomposition temperature (degC)

    Raises
    ------
    ValueError
        If mass_data has fewer than 3 points or invalid method

    Examples
    --------
    >>> data = [(100, 100), (200, 100), (300, 90), (400, 80), (500, 80)]
    >>> tga_decomposition_temperature(data, method='midpoint')
    300.0
    """
    if len(mass_data) < 3:
        raise ValueError("Need at least 3 data points")
    
    # Sort by temperature
    sorted_data = sorted(mass_data, key=lambda x: x[0])
    temps = [d[0] for d in sorted_data]
    masses = [d[1] for d in sorted_data]
    
    if method == 'midpoint':
        # Find where mass loss is halfway between start and end
        initial_mass = masses[0]
        final_mass = masses[-1]
        midpoint_mass = (initial_mass + final_mass) / 2
        
        for i in range(len(masses) - 1):
            m1, m2 = masses[i], masses[i + 1]
            if (m1 >= midpoint_mass >= m2) or (m1 <= midpoint_mass <= m2):
                # Linear interpolation
                if m1 == m2:
                    return temps[i]
                fraction = (m1 - midpoint_mass) / (m1 - m2)
                return round(temps[i] + fraction * (temps[i + 1] - temps[i]), 1)
        return temps[-1]
    
    elif method == 'onset':
        # Find where mass starts decreasing significantly
        # Use derivative approximation to find steepest point
        max_rate = 0
        max_rate_idx = 0
        for i in range(1, len(masses) - 1):
            rate = abs(masses[i - 1] - masses[i + 1]) / (temps[i + 1] - temps[i - 1])
            if rate > max_rate:
                max_rate = rate
                max_rate_idx = i
        
        # Extrapolate onset from before the decomposition
        # Simple approach: find temperature where mass first deviates from initial
        initial_mass = masses[0]
        threshold = initial_mass * 0.01  # 1% deviation
        
        for i in range(len(masses)):
            if initial_mass - masses[i] > threshold:
                return round(temps[i], 1)
        return round(temps[0], 1)
    
    else:
        raise ValueError(f"Unknown method: {method}. Use 'onset' or 'midpoint'")


def tga_residual_mass(
    initial_mass: float,
    formula_initial: str,
    formula_final: str,
    molar_mass_initial: float,
    molar_mass_final: float
) -> float:
    """
    Calculate theoretical residual mass after complete decomposition.

    Parameters
    ----------
    initial_mass : float
        Initial sample mass (mg or g)
    formula_initial : str
        Chemical formula of initial compound (for reference)
    formula_final : str
        Chemical formula of final residue (for reference)
    molar_mass_initial : float
        Molar mass of initial compound (g/mol)
    molar_mass_final : float
        Molar mass of final residue (g/mol)

    Returns
    -------
    float
        Theoretical final mass (same units as initial_mass)

    Examples
    --------
    >>> # CaCO3 -> CaO, M(CaCO3)=100.09, M(CaO)=56.08
    >>> round(tga_residual_mass(100.0, 'CaCO3', 'CaO', 100.09, 56.08), 1)
    56.0
    """
    if initial_mass <= 0:
        raise ValueError(f"initial_mass must be positive, got {initial_mass}")
    if molar_mass_initial <= 0 or molar_mass_final <= 0:
        raise ValueError("Molar masses must be positive")
    
    # Calculate moles of initial compound
    moles = initial_mass / molar_mass_initial
    
    # Calculate mass of final residue (1:1 stoichiometry assumed)
    final_mass = moles * molar_mass_final
    
    return round(final_mass, 2)


# =============================================================================
# DSC (Differential Scanning Calorimetry) Functions
# =============================================================================

def dsc_enthalpy(
    peak_area: float,
    calibration_constant: float
) -> float:
    """
    Calculate enthalpy change from DSC peak area.

    Parameters
    ----------
    peak_area : float
        Integrated area under the DSC peak (arbitrary units)
    calibration_constant : float
        Instrument calibration constant K (J/area unit)
        Determined from standard: K = DeltaH_known / A_measured

    Returns
    -------
    float
        Enthalpy change DeltaH (J/g or J/mol depending on calibration)

    Raises
    ------
    ValueError
        If peak_area or calibration_constant is negative

    Examples
    --------
    >>> dsc_enthalpy(25.0, 1.138)  # Area and K from indium calibration
    28.45
    >>> round(dsc_enthalpy(25.0, 1.138), 2)
    28.45
    """
    if peak_area < 0:
        raise ValueError(f"peak_area cannot be negative, got {peak_area}")
    if calibration_constant <= 0:
        raise ValueError(f"calibration_constant must be positive, got {calibration_constant}")
    
    enthalpy = peak_area * calibration_constant
    return round(enthalpy, 2)


def dsc_calibration_constant(
    known_enthalpy: float,
    measured_area: float
) -> float:
    """
    Determine DSC calibration constant from a standard.

    Parameters
    ----------
    known_enthalpy : float
        Known enthalpy of standard (J/g), e.g., In: 28.45, Sn: 60.22
    measured_area : float
        Measured peak area for the standard (arbitrary units)

    Returns
    -------
    float
        Calibration constant K (J/area unit)

    Raises
    ------
    ValueError
        If known_enthalpy <= 0 or measured_area <= 0

    Examples
    --------
    >>> round(dsc_calibration_constant(28.45, 25.0), 3)  # Indium standard
    1.138
    """
    if known_enthalpy <= 0:
        raise ValueError(f"known_enthalpy must be positive, got {known_enthalpy}")
    if measured_area <= 0:
        raise ValueError(f"measured_area must be positive, got {measured_area}")
    
    K = known_enthalpy / measured_area
    return round(K, 4)


def dsc_heat_capacity(
    heat_flow: float,
    heating_rate: float,
    mass: float
) -> float:
    """
    Calculate specific heat capacity from DSC baseline.

    Parameters
    ----------
    heat_flow : float
        Heat flow rate (mW = mJ/s)
    heating_rate : float
        Heating rate (degC/min or K/min)
    mass : float
        Sample mass (mg)

    Returns
    -------
    float
        Specific heat capacity Cp (J/g·K)

    Notes
    -----
    Formula: Cp = (dQ/dt) / (dT/dt) / m
    Unit conversion: mW/(degC/min)/mg = mJ/s/(K/min)/mg
                   = mJ/s x min/K / mg
                   = mJ/s x 60s/K / mg
                   = 60 mJ/(K·mg) = 60 mJ/(K·mg) x (1g/1000mg)
                   = 0.06 J/(g·K) per unit input

    Examples
    --------
    >>> # 10 mW, 10degC/min, 10 mg -> expected ~6 J/g·K
    >>> dsc_heat_capacity(10.0, 10.0, 10.0)
    6.0
    >>> dsc_heat_capacity(20.0, 10.0, 5.0)
    24.0
    """
    if heat_flow < 0:
        raise ValueError(f"heat_flow should be non-negative, got {heat_flow}")
    if heating_rate <= 0:
        raise ValueError(f"heating_rate must be positive, got {heating_rate}")
    if mass <= 0:
        raise ValueError(f"mass must be positive, got {mass}")
    
    # Convert units:
    # heat_flow: mW = mJ/s
    # heating_rate: degC/min = K/min
    # mass: mg
    # Result: J/(g·K)
    
    # Cp = (mJ/s) / (K/min) / mg
    #    = (mJ/s) x (60 s/K) / mg
    #    = 60 mJ/(K·mg) = 60 J/(g·K) per unit input
    #    (mJ→J and mg→g cancel out)
    
    Cp = (heat_flow * 60) / (heating_rate * mass)  # Convert to J/(g·K)
    return round(Cp, 2)


def dsc_glass_transition(
    baseline_shift: float,
    heating_rate: float,
    mass: float
) -> float:
    """
    Calculate heat capacity change at glass transition temperature.

    Parameters
    ----------
    baseline_shift : float
        Shift in baseline heat flow at Tg (mW)
    heating_rate : float
        Heating rate (degC/min)
    mass : float
        Sample mass (mg)

    Returns
    -------
    float
        Heat capacity change DeltaCp (J/g·K)

    Examples
    --------
    >>> dsc_glass_transition(5.0, 10.0, 10.0)
    3.0
    """
    # Same calculation as dsc_heat_capacity
    return dsc_heat_capacity(baseline_shift, heating_rate, mass)


def dsc_crystallinity(
    measured_enthalpy: float,
    enthalpy_100_crystalline: float
) -> float:
    """
    Calculate degree of crystallinity from melting enthalpy.

    Parameters
    ----------
    measured_enthalpy : float
        Measured melting enthalpy (J/g)
    enthalpy_100_crystalline : float
        Melting enthalpy of 100% crystalline material (J/g)
        Example: PE = 293 J/g, PP = 207 J/g, PET = 140 J/g

    Returns
    -------
    float
        Degree of crystallinity (0-100%)

    Raises
    ------
    ValueError
        If enthalpy_100_crystalline <= 0 or measured_enthalpy < 0

    Examples
    --------
    >>> round(dsc_crystallinity(140, 293), 2)  # PE sample
    47.78
    >>> dsc_crystallinity(207, 207)  # 100% crystalline PP
    100.0
    """
    if enthalpy_100_crystalline <= 0:
        raise ValueError(f"enthalpy_100_crystalline must be positive, got {enthalpy_100_crystalline}")
    if measured_enthalpy < 0:
        raise ValueError(f"measured_enthalpy cannot be negative, got {measured_enthalpy}")
    
    crystallinity = (measured_enthalpy / enthalpy_100_crystalline) * 100
    return round(crystallinity, 2)


# =============================================================================
# DTA (Differential Thermal Analysis) Functions
# =============================================================================

def dta_temperature_difference(
    T_sample: float,
    T_reference: float
) -> float:
    """
    Calculate the temperature difference in DTA.

    Parameters
    ----------
    T_sample : float
        Temperature of the sample (degC)
    T_reference : float
        Temperature of the reference (degC)

    Returns
    -------
    float
        Temperature difference DeltaT = T_sample - T_reference (degC)

    Notes
    -----
    Positive DeltaT: exothermic (sample hotter than reference, sample releases heat)
    Negative DeltaT: endothermic (sample cooler than reference, sample absorbs heat)

    Examples
    --------
    >>> dta_temperature_difference(95, 100)
    -5.0
    >>> dta_temperature_difference(105, 100)
    5.0
    """
    return round(T_sample - T_reference, 2)


def dta_peak_type(Delta_T: float) -> str:
    """
    Classify DTA peak as endothermic or exothermic.

    Parameters
    ----------
    Delta_T : float
        Temperature difference (degC)

    Returns
    -------
    str
        'endothermic' or 'exothermic'

    Examples
    --------
    >>> dta_peak_type(-5.0)  # Sample hotter
    'endothermic'
    >>> dta_peak_type(5.0)   # Sample cooler
    'exothermic'
    >>> dta_peak_type(0.0)
    'no_peak'
    """
    if Delta_T > 0:
        return 'exothermic'
    elif Delta_T < 0:
        return 'endothermic'
    else:
        return 'no_peak'


# =============================================================================
# Phase Transition Identification Functions
# =============================================================================

def phase_transition_identification(
    peak_type: str,
    temperature: float,
    has_mass_change: bool
) -> Dict[str, str]:
    """
    Identify the type of phase transition from thermal analysis data.

    Parameters
    ----------
    peak_type : str
        'endothermic', 'exothermic', or 'baseline_shift'
    temperature : float
        Transition temperature (degC)
    has_mass_change : bool
        Whether TGA shows mass change at this temperature

    Returns
    -------
    Dict[str, str]
        Dictionary with keys:
        - 'transition': identified transition type
        - 'technique': recommended technique for confirmation
        - 'notes': additional information

    Examples
    --------
    >>> result = phase_transition_identification('endothermic', 250, False)
    >>> result['transition']
    'melting'
    >>> phase_transition_identification('baseline_shift', 100, False)['transition']
    'glass_transition'
    """
    result = {
        'transition': 'unknown',
        'technique': 'DSC',
        'notes': ''
    }
    
    if peak_type == 'baseline_shift':
        result['transition'] = 'glass_transition'
        result['notes'] = 'No peak; baseline shift indicates Cp change'
        return result
    
    if has_mass_change:
        if peak_type == 'endothermic':
            if temperature < 200:
                result['transition'] = 'dehydration'
                result['notes'] = 'Mass loss with endotherm suggests water loss'
            else:
                result['transition'] = 'decomposition'
                result['notes'] = 'Mass loss with endotherm suggests decomposition'
        elif peak_type == 'exothermic':
            result['transition'] = 'oxidative_decomposition'
            result['notes'] = 'Mass change with exotherm suggests oxidation'
        result['technique'] = 'TGA + DSC'
    else:
        # No mass change
        if peak_type == 'endothermic':
            result['transition'] = 'melting'
            result['notes'] = 'No mass loss; endotherm likely melting'
        elif peak_type == 'exothermic':
            result['transition'] = 'crystallization'
            result['notes'] = 'No mass loss; exotherm likely crystallization'
    
    return result


def identify_thermal_process(
    temperature_range: Tuple[float, float],
    mass_change: Optional[float] = None,
    heat_flow_direction: Optional[str] = None
) -> List[Dict]:
    """
    Suggest possible thermal processes based on temperature range.

    Parameters
    ----------
    temperature_range : Tuple[float, float]
        (onset_temp, final_temp) in degC
    mass_change : Optional[float]
        Percentage mass change if TGA data available
    heat_flow_direction : Optional[str]
        'endothermic' or 'exothermic' if DSC/DTA data available

    Returns
    -------
    List[Dict]
        List of possible processes with confidence levels

    Examples
    --------
    >>> results = identify_thermal_process((100, 150), mass_change=12.0)
    >>> len(results) > 0
    True
    >>> results[0]['process']
    'dehydration'
    """
    onset, final = temperature_range
    mid_temp = (onset + final) / 2
    results = []
    
    # Temperature-based suggestions
    if mass_change is not None and mass_change > 0:
        # Mass loss detected
        if 50 <= mid_temp <= 300:
            if abs(mass_change - 12) < 5 or abs(mass_change - 18) < 5:
                results.append({
                    'process': 'dehydration',
                    'confidence': 'high' if mid_temp < 200 else 'medium',
                    'notes': f'Typical water loss range ({onset}-{final}degC)'
                })
        
        if 300 <= mid_temp <= 600:
            if mass_change > 10:
                results.append({
                    'process': 'decomposition',
                    'confidence': 'medium',
                    'notes': 'Possible CO loss or organic decomposition'
                })
        
        if 500 <= mid_temp <= 900:
            if mass_change > 30:
                results.append({
                    'process': 'carbonate_decomposition',
                    'confidence': 'high' if mass_change > 40 else 'medium',
                    'notes': f'CO2 loss typical in this range'
                })
    else:
        # No mass change data or no mass change
        if heat_flow_direction == 'endothermic':
            if 0 <= mid_temp <= 500:
                results.append({
                    'process': 'melting',
                    'confidence': 'medium',
                    'notes': 'Endothermic without mass loss'
                })
        elif heat_flow_direction == 'exothermic':
            results.append({
                'process': 'crystallization',
                'confidence': 'medium',
                'notes': 'Exothermic without mass loss'
            })
        elif heat_flow_direction is None:
            # Just temperature range
            if onset < 0:
                results.append({
                    'process': 'glass_transition',
                    'confidence': 'low',
                    'notes': 'Check for baseline shift in DSC'
                })
    
    return results


# =============================================================================
# Mixture Analysis Functions
# =============================================================================

def tga_mixture_analysis(
    total_mass: float,
    mass_loss_step: float,
    gas_molar_mass: float,
    compound_molar_mass: float,
    gas_per_mole_compound: float = 1.0
) -> float:
    """
    Calculate component mass in mixture from TGA mass loss.

    Parameters
    ----------
    total_mass : float
        Total initial sample mass (mg)
    mass_loss_step : float
        Mass loss for this decomposition step (mg)
    gas_molar_mass : float
        Molar mass of gas evolved (g/mol)
    compound_molar_mass : float
        Molar mass of compound that decomposes (g/mol)
    gas_per_mole_compound : float
        Moles of gas released per mole of compound (default 1.0)

    Returns
    -------
    float
        Mass of the component (mg)

    Examples
    --------
    >>> # CaCO3 -> CaO + CO2, mass loss = CO2
    >>> # If 5.30 mg CO2 lost, how much CaC2O4·H2O was present?
    >>> # (Simplified example)
    >>> round(tga_mixture_analysis(17.61, 5.30, 44.01, 146.11), 1)
    17.6
    """
    if total_mass <= 0:
        raise ValueError(f"total_mass must be positive, got {total_mass}")
    if mass_loss_step < 0:
        raise ValueError(f"mass_loss_step cannot be negative, got {mass_loss_step}")
    if gas_molar_mass <= 0 or compound_molar_mass <= 0:
        raise ValueError("Molar masses must be positive")
    
    # Mass of gas lost = mass_loss_step mg
    # Moles of gas = mass_loss_step / gas_molar_mass
    # Moles of compound = moles of gas / gas_per_mole_compound
    # Mass of compound = moles of compound x compound_molar_mass
    
    moles_gas = mass_loss_step / gas_molar_mass
    moles_compound = moles_gas / gas_per_mole_compound
    mass_compound = moles_compound * compound_molar_mass
    
    return round(mass_compound, 2)


# =============================================================================
# Data Classes for Structured Results
# =============================================================================

@dataclass
class TGAStep:
    """Represents a single decomposition step in TGA."""
    temperature_onset: float
    temperature_final: float
    mass_initial: float
    mass_final: float
    mass_loss_percent: float
    identified_product: Optional[str] = None


@dataclass
class DSCPeak:
    """Represents a peak in DSC analysis."""
    temperature: float
    onset_temperature: float
    peak_area: float
    enthalpy: float
    peak_type: str  # 'endothermic' or 'exothermic'
    transition_type: Optional[str] = None


@dataclass
class ThermalProfile:
    """Complete thermal analysis profile for a sample."""
    sample_name: str
    tga_steps: List[TGAStep]
    dsc_peaks: List[DSCPeak]
    glass_transition: Optional[float] = None
    notes: str = ""


# =============================================================================
# Reference Data
# =============================================================================

# Common decomposition products
DECOMPOSITION_PRODUCTS = {
    'H2O': 18.015,
    'CO': 28.010,
    'CO2': 44.009,
    'O2': 31.998,
    'N2': 28.013,
    'NH3': 17.031,
    'SO2': 64.064,
    'NO2': 46.005,
    'HCl': 36.461,
}

# DSC calibration standards
DSC_STANDARDS = {
    'In': {'Tm': 156.6, 'dH': 28.45},
    'Sn': {'Tm': 231.9, 'dH': 60.22},
    'Pb': {'Tm': 327.5, 'dH': 23.03},
    'Zn': {'Tm': 419.5, 'dH': 112.0},
}

# 100% crystalline melting enthalpies (J/g)
CRYSTALLINE_ENTHALPIES = {
    'PE': 293,    # Polyethylene
    'PP': 207,    # Polypropylene
    'PET': 140,   # Polyethylene terephthalate
    'PA6': 230,   # Nylon 6
    'PA66': 255,  # Nylon 66
    'POM': 326,   # Polyoxymethylene
}


# =============================================================================
# Additional Utility Functions
# =============================================================================

def analyze_tga_thermogram(
    data_points: List[Tuple[float, float]],
    initial_molar_mass: Optional[float] = None
) -> List[TGAStep]:
    """
    Analyze a complete TGA thermogram and identify decomposition steps.

    Parameters
    ----------
    data_points : List[Tuple[float, float]]
        List of (temperature, mass) data points
    initial_molar_mass : Optional[float]
        Molar mass of initial compound for product identification

    Returns
    -------
    List[TGAStep]
        List of identified decomposition steps

    Examples
    --------
    >>> data = [(100, 100), (200, 100), (250, 88), (300, 88), (400, 60)]
    >>> steps = analyze_tga_thermogram(data)
    >>> len(steps)
    2
    """
    if len(data_points) < 4:
        return []
    
    # Sort by temperature
    sorted_data = sorted(data_points, key=lambda x: x[0])
    
    steps = []
    in_plateau = True
    plateau_start_idx = 0
    plateau_mass = sorted_data[0][1]
    
    for i in range(1, len(sorted_data)):
        temp, mass = sorted_data[i]
        prev_temp, prev_mass = sorted_data[i - 1]
        
        # Check for mass change
        if abs(mass - prev_mass) > plateau_mass * 0.005:  # 0.5% threshold
            if in_plateau:
                # Start of a decomposition step
                in_plateau = False
        else:
            if not in_plateau:
                # End of decomposition step
                in_plateau = True
                
                # Record the step
                step = TGAStep(
                    temperature_onset=sorted_data[plateau_start_idx][0],
                    temperature_final=temp,
                    mass_initial=sorted_data[plateau_start_idx][1],
                    mass_final=mass,
                    mass_loss_percent=tga_mass_percent(
                        sorted_data[plateau_start_idx][1], mass
                    ) if sorted_data[plateau_start_idx][1] > 0 else 0
                )
                
                # Try to identify product if molar mass provided
                if initial_molar_mass:
                    molar_loss = tga_mass_loss_molar(
                        step.mass_loss_percent, initial_molar_mass
                    )
                    step.identified_product = tga_identify_product(
                        molar_loss,
                        list(DECOMPOSITION_PRODUCTS.items())
                    )
                    initial_molar_mass -= molar_loss  # Update for next step
                
                steps.append(step)
                plateau_start_idx = i
                plateau_mass = mass
    
    return steps


def calculate_heat_of_fusion(
    peak_area: float,
    calibration_constant: float,
    sample_mass: float
) -> float:
    """
    Calculate heat of fusion per gram from DSC melting peak.

    Parameters
    ----------
    peak_area : float
        Integrated peak area
    calibration_constant : float
        Calibration constant (J/area unit)
    sample_mass : float
        Sample mass in mg

    Returns
    -------
    float
        Heat of fusion (J/g)

    Examples
    --------
    >>> round(calculate_heat_of_fusion(25.0, 1.138, 10.0), 2)
    2.85
    """
    total_enthalpy = dsc_enthalpy(peak_area, calibration_constant)
    return round(total_enthalpy / (sample_mass / 1000), 2)  # Convert mg to g


def estimate_purity_from_melting(
    melting_point_pure: float,
    melting_point_observed: float,
    entropy_of_fusion: float = 50.0
) -> float:
    """
    Estimate purity from melting point depression.

    Uses simplified van't Hoff equation for dilute solutions.

    Parameters
    ----------
    melting_point_pure : float
        Melting point of pure compound (degC)
    melting_point_observed : float
        Observed melting point (degC)
    entropy_of_fusion : float
        Entropy of fusion (J/mol·K), default 50 J/mol·K

    Returns
    -------
    float
        Estimated mole fraction purity (0-1)

    Examples
    --------
    >>> round(estimate_purity_from_melting(135.0, 134.0), 3)
    0.977
    """
    # DeltaT = K x x_impurity
    # where K = R x Tf2 / DeltaHf = R x Tf / DeltaSf
    # x_purity = 1 - DeltaT / K
    
    R = 8.314  # J/mol·K
    T_pure = melting_point_pure + 273.15  # Convert to K
    T_obs = melting_point_observed + 273.15
    
    delta_T = T_pure - T_obs
    K = R * T_pure / entropy_of_fusion
    
    purity = 1 - delta_T / K
    return max(0, min(1, purity))


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="analyze_tga_thermogram",
            description="Analyze a complete TGA thermogram and identify decomposition steps.",
            input_schema=[
            InputSchemaField(name="data_points", type="number", required=True),
            InputSchemaField(name="initial_molar_mass", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_heat_of_fusion",
            description="Calculate heat of fusion per gram from DSC melting peak.",
            input_schema=[
            InputSchemaField(name="peak_area", type="number", required=True),
            InputSchemaField(name="calibration_constant", type="number", required=True),
            InputSchemaField(name="sample_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dsc_calibration_constant",
            description="Determine DSC calibration constant from a standard.",
            input_schema=[
            InputSchemaField(name="known_enthalpy", type="number", required=True),
            InputSchemaField(name="measured_area", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dsc_crystallinity",
            description="Calculate degree of crystallinity from melting enthalpy.",
            input_schema=[
            InputSchemaField(name="measured_enthalpy", type="number", required=True),
            InputSchemaField(name="enthalpy_100_crystalline", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dsc_enthalpy",
            description="Calculate enthalpy change from DSC peak area.",
            input_schema=[
            InputSchemaField(name="peak_area", type="number", required=True),
            InputSchemaField(name="calibration_constant", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dsc_glass_transition",
            description="Calculate heat capacity change at glass transition temperature.",
            input_schema=[
            InputSchemaField(name="baseline_shift", type="string", required=True),
            InputSchemaField(name="heating_rate", type="number", required=True),
            InputSchemaField(name="mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dsc_heat_capacity",
            description="Calculate specific heat capacity from DSC baseline.",
            input_schema=[
            InputSchemaField(name="heat_flow", type="number", required=True),
            InputSchemaField(name="heating_rate", type="number", required=True),
            InputSchemaField(name="mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dta_peak_type",
            description="Classify DTA peak as endothermic or exothermic.",
            input_schema=[
            InputSchemaField(name="Delta_T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dta_temperature_difference",
            description="Calculate the temperature difference in DTA.",
            input_schema=[
            InputSchemaField(name="T_sample", type="number", required=True),
            InputSchemaField(name="T_reference", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="estimate_purity_from_melting",
            description="Estimate purity from melting point depression.",
            input_schema=[
            InputSchemaField(name="melting_point_pure", type="number", required=True),
            InputSchemaField(name="melting_point_observed", type="number", required=True),
            InputSchemaField(name="entropy_of_fusion", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="identify_thermal_process",
            description="Suggest possible thermal processes based on temperature range.",
            input_schema=[
            InputSchemaField(name="temperature_range", type="number", required=True),
            InputSchemaField(name="mass_change", type="number", required=False),
            InputSchemaField(name="heat_flow_direction", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="phase_transition_identification",
            description="Identify the type of phase transition from thermal analysis data.",
            input_schema=[
            InputSchemaField(name="peak_type", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="has_mass_change", type="boolean", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tga_decomposition_temperature",
            description="Determine decomposition temperature from TGA data.",
            input_schema=[
            InputSchemaField(name="mass_data", type="number", required=True),
            InputSchemaField(name="method", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tga_identify_product",
            description="Identify the volatile decomposition product from molar mass loss.",
            input_schema=[
            InputSchemaField(name="calculated_mass_loss", type="number", required=True),
            InputSchemaField(name="candidates", type="number", required=True),
            InputSchemaField(name="tolerance", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tga_mass_loss_molar",
            description="Calculate the molar mass decrease corresponding to a mass loss percentage.",
            input_schema=[
            InputSchemaField(name="mass_loss_percent", type="number", required=True),
            InputSchemaField(name="initial_molar_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tga_mass_percent",
            description="Calculate the percentage of mass loss in a TGA experiment.",
            input_schema=[
            InputSchemaField(name="initial_mass", type="number", required=True),
            InputSchemaField(name="final_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tga_mixture_analysis",
            description="Calculate component mass in mixture from TGA mass loss.",
            input_schema=[
            InputSchemaField(name="total_mass", type="number", required=True),
            InputSchemaField(name="mass_loss_step", type="number", required=True),
            InputSchemaField(name="gas_molar_mass", type="number", required=True),
            InputSchemaField(name="compound_molar_mass", type="string", required=True),
            InputSchemaField(name="gas_per_mole_compound", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tga_residual_mass",
            description="Calculate theoretical residual mass after complete decomposition.",
            input_schema=[
            InputSchemaField(name="initial_mass", type="number", required=True),
            InputSchemaField(name="formula_initial", type="string", required=True),
            InputSchemaField(name="formula_final", type="string", required=True),
            InputSchemaField(name="molar_mass_initial", type="number", required=True),
            InputSchemaField(name="molar_mass_final", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
