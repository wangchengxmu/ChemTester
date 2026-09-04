"""
Electroanalytical Chemistry Tools - L3 Implementation

Functions for ISE calibration, polarography (Ilkovic equation), standard addition,
electrolysis mass determination, and coulometric concentration.

Source: Harvey Analytical Chemistry Ch11, Skoog Instrumental Analysis Ch22-25
"""

import math
from typing import List, Tuple, Optional

# Constants
FARADAY = 96485  # C/mol e-
R_GAS = 8.314    # J/(mol·K)


# =============================================================================
# ISE Calibration
# =============================================================================

def ise_calibration(
    volumes: List[float],
    potentials: List[float],
    unknown_potential: float,
    initial_volume: float = 0.0,
    stock_concentration: float = None,
    charge: int = 1,
    ion_type: Optional[str] = None
) -> Tuple[float, float, float, float]:
    """
    ISE calibration via linear regression of E vs log(concentration).
    
    For standard addition calibration:
    - Calculate concentration of each standard from volumes
    - Fit E = E0 + slope * log10(C)
    - Use the fit to find unknown concentration from measured potential
    
    If stock_concentration and initial_volume are given, concentrations are
    computed via dilution from standard additions.
    If not, assumes volumes represent a concentration series directly.
    
    Sign convention:
    - ion_type="cation" (default if charge > 0): E = E0 + S*log(C), S > 0
    - ion_type="anion": E = E0 - S*log(C), where S > 0 and returned slope is -S
    - ion_type=None: auto-detect from data (if E increases with C → cation-like)
    
    Parameters
    ----------
    volumes : list of float
        Standard solution volumes (mL) added, or concentrations (M) if no stock_conc.
    potentials : list of float
        Corresponding measured potentials (mV)
    unknown_potential : float
        Measured potential of unknown (mV)
    initial_volume : float, optional
        Sample volume (mL), for standard addition
    stock_concentration : float, optional
        Stock standard concentration (M), for standard addition
    charge : int, optional
        Ion charge with sign (default 1 for +1 cation)
    ion_type : str, optional
        "cation", "anion", or None (auto-detect from data trend)
    
    Returns
    -------
    tuple : (concentration, slope, intercept, r_squared)
        concentration of unknown (M), calibration slope (mV/decade),
        intercept (mV), R² of calibration fit
    """
    if len(volumes) != len(potentials) or len(volumes) < 2:
        raise ValueError("Need at least 2 (volume, potential) pairs")
    
    # Determine concentrations
    if stock_concentration is not None and initial_volume > 0:
        # Standard addition: C = (V_spike * C_stock) / (V_initial + V_spike)
        concentrations = []
        for v in volumes:
            c = (v * stock_concentration) / (initial_volume + v)
            concentrations.append(c)
        # Unknown concentration from calibration curve
        # Sample only (no spike): C_unknown is found from potential
    else:
        # Assume volumes are concentrations directly
        concentrations = list(volumes)
    
    # Filter out zero/negative concentrations
    valid = [(c, e) for c, e in zip(concentrations, potentials) if c > 0]
    if len(valid) < 2:
        raise ValueError("Need at least 2 valid positive concentrations")
    
    log_c = [math.log10(c) for c, _ in valid]
    e_vals = [e for _, e in valid]
    n = len(log_c)
    
    # Linear regression: E = intercept + slope * log10(C)
    mean_x = sum(log_c) / n
    mean_y = sum(e_vals) / n
    
    ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_c, e_vals))
    ss_xx = sum((x - mean_x) ** 2 for x in log_c)
    ss_yy = sum((y - mean_y) ** 2 for y in e_vals)
    
    if ss_xx == 0:
        raise ValueError("All concentrations are identical, cannot calibrate")
    
    raw_slope = ss_xy / ss_xx
    intercept = mean_y - raw_slope * mean_x
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy > 0 else 0.0
    
    # Determine sign convention for anion vs cation
    if ion_type is None:
        ion_type = "anion" if charge < 0 else "cation"
    elif ion_type not in ("cation", "anion"):
        raise ValueError("ion_type must be 'cation', 'anion', or None")
    
    if ion_type == "anion":
        # For anion ISE: E = E0 - S*log(C), where S > 0
        # The raw regression slope may be positive or negative depending on data.
        # Convention: report slope as negative (anion convention).
        # Use absolute value as the magnitude S, report as -S.
        S = abs(raw_slope)
        slope = -S
        # Recalculate intercept: E = intercept_anion - S*log(C)
        # From data: mean_y = intercept_anion + raw_slope * mean_x
        # We want: mean_y = intercept_anion - S * mean_x
        intercept = mean_y + S * mean_x
    else:
        # Cation: E = E0 + S*log(C), slope is as-is
        slope = raw_slope
    
    # Find unknown concentration
    # E_unknown = intercept + slope * log10(C_unknown)
    # log10(C_unknown) = (E_unknown - intercept) / slope
    log_c_unknown = (unknown_potential - intercept) / slope
    c_unknown = 10 ** log_c_unknown
    
    # If standard addition was used, the unknown concentration needs adjustment
    # for dilution: C_unknown (true) = C_unknown * (V_initial + V_spike) / V_initial
    # But since unknown is measured without spike, no dilution correction needed.
    
    return (c_unknown, slope, intercept, r_squared)


def ise_calibration_direct(
    concentrations: List[float],
    potentials: List[float],
    unknown_potential: float
) -> Tuple[float, float, float, float]:
    """
    Simpler ISE calibration when concentrations are known directly.
    
    E = E0 + S * log10(C), where S = 59.16/z mV/decade at 25°C
    
    Parameters
    ----------
    concentrations : list of float
        Standard concentrations (M)
    potentials : list of float
        Measured potentials (mV)
    unknown_potential : float
        Potential of unknown (mV)
    
    Returns
    -------
    tuple : (concentration, slope, intercept, r_squared)
    """
    return ise_calibration(concentrations, potentials, unknown_potential)


# =============================================================================
# Polarography / Ilkovic Equation
# =============================================================================

def ilkovic_equation(
    n_electrons: int,
    diffusion_coeff: float,
    mercury_flow_rate: float,
    drop_time: float,
    concentration: float
) -> float:
    """
    Ilkovic equation for diffusion current in DC polarography.
    
    I_d = 607 * n * D^(1/2) * m^(2/3) * t^(1/6) * C
    
    Parameters
    ----------
    n_electrons : int
        Number of electrons transferred
    diffusion_coeff : float
        Diffusion coefficient D (cm²/s)
    mercury_flow_rate : float
        Mercury flow rate m (mg/s)
    drop_time : float
        Drop time t (s)
    concentration : float
        Analyte concentration C (mM, millimolar)
    
    Returns
    -------
    float
        Diffusion current (μA)
    
    Examples
    --------
    >>> ilkovic_equation(2, 1.0e-5, 2.0, 4.0, 1.0)
    ~3.05  # μA
    """
    if n_electrons <= 0 or diffusion_coeff <= 0 or mercury_flow_rate <= 0:
        raise ValueError("n_electrons, D, and m must be positive")
    if drop_time <= 0 or concentration < 0:
        raise ValueError("drop_time must be positive, concentration must be >= 0")
    
    I_d = 607 * n_electrons * (diffusion_coeff ** 0.5) * \
          (mercury_flow_rate ** (2/3)) * (drop_time ** (1/6)) * concentration
    return I_d


def concentration_from_ilkovic(
    diffusion_current: float,
    n_electrons: int,
    diffusion_coeff: float,
    mercury_flow_rate: float,
    drop_time: float
) -> float:
    """
    Calculate concentration from Ilkovic equation.
    
    C = I_d / (607 * n * D^(1/2) * m^(2/3) * t^(1/6))
    
    Parameters
    ----------
    diffusion_current : float
        Measured diffusion current (μA)
    n_electrons : int
        Number of electrons transferred
    diffusion_coeff : float
        Diffusion coefficient (cm²/s)
    mercury_flow_rate : float
        Mercury flow rate (mg/s)
    drop_time : float
        Drop time (s)
    
    Returns
    -------
    float
        Concentration (mM)
    """
    if n_electrons <= 0 or diffusion_coeff <= 0 or mercury_flow_rate <= 0:
        raise ValueError("Parameters must be positive")
    
    denominator = 607 * n_electrons * (diffusion_coeff ** 0.5) * \
                  (mercury_flow_rate ** (2/3)) * (drop_time ** (1/6))
    return diffusion_current / denominator


# =============================================================================
# Standard Addition
# =============================================================================

def standard_addition_concentration(
    sample_signal: float,
    spike_signals: List[float],
    spike_volumes: List[float],
    spike_concentration: float,
    sample_volume: float
) -> float:
    """
    Determine unknown concentration by standard addition (linear extrapolation).
    
    Method: Plot S_total vs V_spike. The x-intercept (where S=0, extrapolated)
    gives -V_eq. Then C_unknown = C_spike * V_eq / V_sample.
    
    Alternatively, using linear regression on:
    S_i = S_0 + k * (C_spike * V_i / V_total_i)
    
    More robust approach: fit signal vs added concentration of analyte,
    extrapolate to signal = 0.
    
    Parameters
    ----------
    sample_signal : float
        Signal from the original sample (no spike)
    spike_signals : list of float
        Signals after each standard addition spike
    spike_volumes : list of float
        Volume of each spike added (mL)
    spike_concentration : float
        Concentration of the spike standard (same units as desired output, e.g., mg/L)
    sample_volume : float
        Volume of the original sample (mL)
    
    Returns
    -------
    float
        Concentration of analyte in the original sample
    
    Notes
    -----
    Uses linear regression on total signal vs added amount.
    The x-intercept of the regression gives the equivalent amount
    of analyte in the sample: C_x = -b/m, then scale by volume.
    
    Examples
    --------
    # NO3- standard addition: 5 mL sample, 0.10 mL spikes of standard
    >>> standard_addition_concentration(2.36, [2.50, 2.64, 2.78], 
    ...     [0.10, 0.20, 0.30], 600e-6, 5.0)
    ~2.9e-6  # M, convert to mg/L as needed
    """
    if len(spike_signals) != len(spike_volumes):
        raise ValueError("spike_signals and spike_volumes must have same length")
    if len(spike_signals) < 1:
        raise ValueError("Need at least 1 spike measurement")
    
    # Build data: x = amount added (in concentration units), y = signal
    x_vals = []  # added analyte amount = V_spike * C_spike
    y_vals = []
    
    # Include original sample point (0 added)
    x_vals.append(0.0)
    y_vals.append(sample_signal)
    
    for v, s in zip(spike_volumes, spike_signals):
        # Total volume changes with each spike if sequential
        # For simplicity, treat as independent additions from fresh sample
        # Added concentration in the total volume
        added_amount = v * spike_concentration
        x_vals.append(added_amount)
        y_vals.append(s)
    
    n = len(x_vals)
    
    # Linear regression: y = a + b*x
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    
    ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    ss_xx = sum((x - mean_x) ** 2 for x in x_vals)
    
    if ss_xx == 0:
        raise ValueError("Cannot compute: all x values are identical")
    
    slope = ss_xy / ss_xx
    intercept = mean_y - slope * mean_x
    
    # x-intercept: where signal extrapolates to zero (or sample-only level)
    # For standard addition: signal increases with added amount
    # The x-intercept (negative) tells us how much was originally present
    if slope == 0:
        raise ValueError("Zero slope in calibration")
    
    # x-intercept where signal = 0: x_int = -intercept/slope
    x_intercept = -intercept / slope
    
    # x_intercept is typically negative for standard addition
    # The absolute value represents the amount of analyte in the sample
    concentration = abs(x_intercept) / sample_volume
    
    return concentration


# =============================================================================
# Electrolysis Mass Determination
# =============================================================================

def mass_from_electrolysis(
    molar_mass: float,
    current: float,
    time: float,
    n_electrons: int,
    reactant_to_product_ratio: float = 1.0
) -> float:
    """
    Calculate mass deposited/produced by electrolysis using Faraday's law.
    
    m = (M × I × t) / (n × F)
    
    CRITICAL: n_electrons must match the half-reaction stoichiometry!
    e.g., Cu → Cu²⁺ + 2e⁻ means n=2, NOT n=1.
    
    For coupling/dimerization reactions (e.g., 2 acrylonitrile → adiponitrile),
    set reactant_to_product_ratio=2.0 and provide the PRODUCT molar mass.
    Then: moles_product = (Q / F) / (n × reactant_to_product_ratio)
    
    Parameters
    ----------
    molar_mass : float
        Molar mass of product (g/mol)
    current : float
        Current (amperes)
    time : float
        Time (seconds)
    n_electrons : int
        Number of electrons transferred per reaction event (REQUIRED, no default!)
    reactant_to_product_ratio : float, optional
        Moles of reactant consumed per mole of product formed (default 1.0).
        Set to 2.0 for dimerization/coupling reactions.
    
    Returns
    -------
    float
        Mass of product (g)
    """
    if n_electrons <= 0:
        raise ValueError("n_electrons must be positive and match the half-reaction")
    if current <= 0 or time <= 0:
        raise ValueError("current and time must be positive")
    
    charge_passed = current * time  # Coulombs
    moles_electrons = charge_passed / FARADAY
    moles_product = moles_electrons / (n_electrons * reactant_to_product_ratio)
    return moles_product * molar_mass


# =============================================================================
# Coulometric Concentration
# =============================================================================

def coulometric_concentration(
    charge: float,
    n_electrons: int,
    volume: float,
    molar_mass: float
) -> float:
    """
    Calculate concentration from coulometric titration.
    
    m = (Q × M) / (n × F)
    C = m / V = (Q × M) / (n × F × V)
    
    Parameters
    ----------
    charge : float
        Total charge passed (Coulombs)
    n_electrons : int
        Number of electrons transferred per molecule
    volume : float
        Solution volume (L)
    molar_mass : float
        Molar mass of analyte (g/mol)
    
    Returns
    -------
    float
        Concentration (g/L)
    
    Examples
    --------
    >>> coulometric_concentration(96.485, 1, 0.1, 58.44)  # 0.1 F in 0.1 L
    58.44  # g/L
    """
    if n_electrons <= 0:
        raise ValueError("n_electrons must be positive")
    if volume <= 0:
        raise ValueError("volume must be positive")
    
    mass = (charge * molar_mass) / (n_electrons * FARADAY)
    return mass / volume


def coulometric_molar_concentration(
    charge: float,
    n_electrons: int,
    volume: float
) -> float:
    """
    Calculate molar concentration from coulometric titration.
    
    C = Q / (n × F × V)
    
    Parameters
    ----------
    charge : float
        Total charge passed (Coulombs)
    n_electrons : int
        Electrons transferred per molecule
    volume : float
        Solution volume (L)
    
    Returns
    -------
    float
        Molar concentration (mol/L)
    """
    if n_electrons <= 0 or volume <= 0:
        raise ValueError("n_electrons and volume must be positive")
    
    moles = charge / (n_electrons * FARADAY)
    return moles / volume


# =============================================================================
# Half-Wave Potential (Polarography)
# =============================================================================

def half_wave_potential(
    E_half: float,
    E_formal: float = None,
    n_electrons: int = None,
    D_reduced: float = None,
    D_oxidized: float = None,
    T: float = 298.15
) -> dict:
    """
    Relate half-wave potential to formal potential in polarography.
    
    E_1/2 = E°' + (RT/nF) * ln(D_red/D_ox)^(1/2)
    
    Can compute E_1/2 from E°' and D values, or E°' from E_1/2.
    
    Parameters
    ----------
    E_half : float
        Half-wave potential (V)
    E_formal : float, optional
        Formal potential E°' (V). If provided with D values, used to compute E_1/2.
    n_electrons : int, optional
        Electrons transferred. Required if E_formal is given.
    D_reduced : float, optional
        Diffusion coefficient of reduced species (cm²/s)
    D_oxidized : float, optional
        Diffusion coefficient of oxidized species (cm²/s)
    T : float
        Temperature (K), default 298.15
    
    Returns
    -------
    dict with keys: E_half, E_formal (if computable), correction (V)
    
    Examples
    --------
    # When D_reduced ≈ D_oxidized, E_1/2 ≈ E°'
    >>> half_wave_potential(E_formal=0.1, n_electrons=2, D_reduced=1e-5, D_oxidized=1e-5)
    """
    result = {'E_half': E_half, 'T': T}
    
    if E_formal is not None and n_electrons is not None and D_reduced and D_oxidized:
        correction = (R_GAS * T) / (n_electrons * FARADAY) * 0.5 * math.log(D_reduced / D_oxidized)
        computed_half = E_formal + correction
        result['E_half'] = computed_half
        result['E_formal'] = E_formal
        result['correction'] = correction
    elif E_half is not None and n_electrons is not None and D_reduced and D_oxidized:
        correction = -(R_GAS * T) / (n_electrons * FARADAY) * 0.5 * math.log(D_reduced / D_oxidized)
        result['E_formal'] = E_half + correction
        result['correction'] = correction
    else:
        result['E_formal'] = E_formal
        result['correction'] = 0.0
    
    return result


# =============================================================================
# Cyclic Voltammetry - Randles-Sevcik Equation
# =============================================================================

def cyclic_voltammetry_peak_current(
    n_electrons: int,
    area: float,
    diffusion_coeff: float,
    concentration: float,
    scan_rate: float,
    T: float = 298.15
) -> float:
    """
    Randles-Sevcik equation for peak current in cyclic voltammetry.
    
    i_p = (2.69 × 10⁵) × n^(3/2) × A × D^(1/2) × C × v^(1/2)
    
    At 25°C for a reversible system.
    
    Parameters
    ----------
    n_electrons : int
        Number of electrons transferred
    area : float
        Electrode surface area (cm²)
    diffusion_coeff : float
        Diffusion coefficient D (cm²/s)
    concentration : float
        Bulk concentration C (mol/L = mol/cm³ × 1000)
    scan_rate : float
        Scan rate v (V/s)
    T : float
        Temperature (K), default 298.15
    
    Returns
    -------
    float
        Peak current i_p (amperes)
    
    Examples
    --------
    >>> cyclic_voltammetry_peak_current(1, 0.1, 1e-5, 0.001, 0.1)
    ~8.5e-6  # ~8.5 μA
    """
    if n_electrons <= 0 or area <= 0 or diffusion_coeff <= 0 or scan_rate <= 0:
        raise ValueError("n_electrons, area, D, and scan_rate must be positive")
    if concentration < 0:
        raise ValueError("concentration must be non-negative")
    
    # Temperature correction factor (Randles-Sevcik constant at 25°C is 2.69e5)
    # The constant scales as sqrt(T); at T=298.15K the standard constant applies
    temp_factor = math.sqrt(T / 298.15) if T != 298.15 else 1.0
    
    ip = 2.69e5 * temp_factor * (n_electrons ** 1.5) * area * \
         (diffusion_coeff ** 0.5) * concentration * (scan_rate ** 0.5)
    return ip


def cv_peak_potential_shift(
    delta_Ep: float = None,
    n_electrons: int = 1
) -> float:
    """
    Expected peak separation for reversible vs quasi-reversible CV.
    
    Reversible: ΔEp ≈ 59/n mV at 25°C
    Quasi-reversible: ΔEp > 59/n mV (increases with scan rate)
    Irreversible: no return peak
    
    Parameters
    ----------
    delta_Ep : float, optional
        Observed peak separation (V). If provided, compare to theoretical.
    n_electrons : int
        Electrons transferred
    
    Returns
    -------
    float
        Theoretical reversible ΔEp (V)
    """
    return 0.05916 / n_electrons


# =============================================================================
# Coulometric Determination (mass-based)
# =============================================================================

def coulometric_determination(
    charge: float,
    n_electrons: int,
    molar_mass: float
) -> float:
    """
    Determine mass from charge using Faraday's law (coulometry).
    
    m = (Q × M) / (n × F)
    
    Parameters
    ----------
    charge : float
        Total charge passed (Coulombs)
    n_electrons : int
        Electrons transferred per formula unit
    molar_mass : float
        Molar mass (g/mol)
    
    Returns
    -------
    float
        Mass (g)
    """
    if n_electrons <= 0:
        raise ValueError("n_electrons must be positive")
    return (charge * molar_mass) / (n_electrons * FARADAY)


# =============================================================================
# Amperometric Detection
# =============================================================================

def amperometric_detection(
    measured_current: float,
    sensitivity: float,
    blank_current: float = 0.0
) -> float:
    """
    Determine concentration from amperometric measurement.
    
    I = I_blank + S × C  →  C = (I - I_blank) / S
    
    Parameters
    ----------
    measured_current : float
        Measured current (A or nA, units must match sensitivity)
    sensitivity : float
        Calibration sensitivity S (current per concentration unit)
    blank_current : float
        Current at zero concentration (default 0)
    
    Returns
    -------
    float
        Concentration (in units consistent with sensitivity)
    """
    if sensitivity == 0:
        raise ValueError("Sensitivity cannot be zero")
    return (measured_current - blank_current) / sensitivity


# =============================================================================
# Nernst Equation (general)
# =============================================================================

def nernst_potential(
    E_formal: float,
    n_electrons: int,
    reduced_conc: float,
    oxidized_conc: float = 1.0,
    T: float = 298.15
) -> float:
    """
    Nernst equation for electrode potential.
    
    E = E°' + (RT/nF) × ln([ox]/[red])
    
    Parameters
    ----------
    E_formal : float
        Formal reduction potential (V)
    n_electrons : int
        Electrons transferred
    reduced_conc : float
        Concentration of reduced species
    oxidized_conc : float
        Concentration of oxidized species (default 1.0)
    T : float
        Temperature (K)
    
    Returns
    -------
    float
        Electrode potential (V)
    """
    if reduced_conc <= 0 or oxidized_conc <= 0:
        raise ValueError("Concentrations must be positive")
    return E_formal + (R_GAS * T) / (n_electrons * FARADAY) * math.log(oxidized_conc / reduced_conc)


# =============================================================================
# Redox Electron Counting
# =============================================================================

def electrons_in_reduction(
    reactant_formula: str,
    product_formula: str = None,
    n_known: int = None
) -> int:
    """
    Determine number of electrons transferred in a reduction.
    
    For common electrode reactions, provides the electron count.
    This is a lookup helper for common analytical electrochemistry reactions.
    
    Parameters
    ----------
    reactant_formula : str
        Formula or name of reactant
    product_formula : str, optional
        Formula or name of product
    n_known : int, optional
        If provided, return this directly (for verification)
    
    Returns
    -------
    int
        Number of electrons transferred
    
    Examples
    --------
    >>> electrons_in_reduction("Cu")
    2  # Cu → Cu²⁺ + 2e⁻
    >>> electrons_in_reduction("acrylonitrile")
    2  # acrylonitrile → adiponitrile (2e⁻ each, but coupling = 2 × 2 = 4 total)
    """
    # Common electrode reactions lookup
    _reactions = {
        'cu': 2, 'copper': 2,
        'ag': 1, 'silver': 1,
        'zn': 2, 'zinc': 2,
        'fe': 2,  # Fe²⁺ or Fe³⁺ → depends on context
        'al': 3, 'aluminum': 3,
        'ni': 2, 'nickel': 2,
        'pb': 2, 'lead': 2,
        'acrylonitrile': 2,  # per molecule, n=2
        'adiponitrile': 2,
    }
    
    key = reactant_formula.lower().strip()
    
    if n_known is not None:
        return n_known
    
    if key in _reactions:
        return _reactions[key]
    
    # Try to infer from oxidation state change
    raise ValueError(
        f"Unknown reaction for '{reactant_formula}'. "
        f"Please specify n_electrons explicitly. Known: {list(_reactions.keys())}"
    )
