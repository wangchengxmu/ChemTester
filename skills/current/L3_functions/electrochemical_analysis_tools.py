"""
Electrochemical Analysis Tools - L3 Implementation

Functions for potentiometry, voltammetry, coulometry, amperometry, and conductometry calculations.

Source: LibreTexts Analytical Chemistry 2.1 (Harvey) Ch11 + Instrumental Analysis Ch22/25
"""
## Solver Instructions (for AI Agent)

# When you encounter electrochemical analysis problems (potentiometry, voltammetry, coulometry, conductometry), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: concentrations, potentials, currents, electrode parameters, reference electrodes
# - **Asked**: electrode potential, peak current, moles from charge, conductivity, pH

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Nernst potential | `potentiometry_nernst(concentration, E0, n, temperature)` | [M], Edeg, n |
# | ISE potential | `ion_selective_electrode(activity, slope, intercept, charge)` | activity, slope |
# | pH from potential | `ph_from_potential(E, E0, slope)` | measured E |
# | Reference conversion | `reference_potential_convert(E, from_ref, to_ref)` | 'SHE'/'SCE'/'Ag/AgCl' |
# | ISE selectivity | `ise_selectivity_coefficient(a_A, a_I, z_A, z_I)` | activities, charges |
# | CV peak current | `cyclic_voltammetry_peak(conc, area, D, scan_rate, n)` | Randles-Sevcik |
# | Scan rate effect | `scan_rate_effect(peak_current, scan_rate, new_scan_rate)` | i_p ∝ √ν |
# | Half-wave potential | `voltammetry_half_wave_potential(E_anodic, E_cathodic)` | E_pa, E_pc |
# | Faraday's law (moles) | `coulometry_moles(charge, n_electrons)` | Q, n |
# | Charge needed | `coulometry_charge(moles, n_electrons)` | moles, n |
# | Constant current | `coulometry_constant_current(current, time, n_electrons)` | i, t, n |
# | Electrolysis time | `coulometry_electrolysis_time(moles, current, n_electrons)` | moles, i, n |
# | Coulometric purity | `coulometry_purity(mass, charge, n, M)` | mass, Q, n, M |
# | Amperometric current | `amperometry_current(conc, sensitivity)` | conc, sensitivity |
# | Conductivity from R | `conductivity_from_resistance(resistance, cell_constant)` | R, k |
# | Cell constant | `conductivity_cell_constant(resistance, conductivity)` | R, κ |
# | Molar conductivity | `molar_conductivity(conductivity, concentration)` | κ, c |
# | Kohlrausch's law | `kohlrausch_equation(conc, limiting_conductivity, K)` | c, Λdeg, K |

### Step 3: Handle special cases
# - Reference electrode conversion: SHE vs SCE = +0.244 V; SHE vs Ag/AgCl = +0.197 V
# - Randles-Sevcik requires concentration in mol/cm3 (not mol/L)
# - Scan rate effect: for reversible systems, i_p ∝ ν^(1/2)

### Examples
# 1. **Nernst**: `potentiometry_nernst(0.01, 0.7996, 1)` -> 0.7405 V (Ag+/Ag)
# 2. **CV peak**: `cyclic_voltammetry_peak(1e-6, 0.02, 1e-5, 0.1, 1)` -> ~1.7 muA
# 3. **Coulometry**: `coulometry_moles(96487, 1)` -> 1.0 mol (1 Faraday)
# 4. **Ref conversion**: `reference_potential_convert(0.750, 'SHE', 'SCE')` -> 0.506 V


from typing import Tuple, Optional, Dict, List, Union
from dataclasses import dataclass
import math


# =============================================================================
# POTENTIOMETRY Functions
# =============================================================================

def potentiometry_nernst(
    concentration: float,
    E0: float,
    n: int,
    temperature: float = 25.0
) -> float:
    """
    Calculate electrode potential using Nernst equation.
    
    E = Edeg - (RT/nF) ln(Q) = Edeg - (0.05916/n) log(Q) at 25degC
    
    For reduction: M^n+ + ne- -> M
    Q = 1/[M^n+]
    E = Edeg - (RT/nF) ln(1/[M^n+]) = Edeg + (RT/nF) ln([M^n+])
    
    Parameters
    ----------
    concentration : float
        Analyte concentration or activity (M)
    E0 : float
        Standard reduction potential (V)
    n : int
        Number of electrons transferred
    temperature : float, optional
        Temperature in degC (default 25.0)
    
    Returns
    -------
    float
        Electrode potential (V)
    
    Raises
    ------
    ValueError
        If concentration <= 0 or n <= 0
    
    Examples
    --------
    >>> round(potentiometry_nernst(0.1, 0.7996, 1), 4)  # Ag+/Ag
    0.7405
    >>> round(potentiometry_nernst(0.01, -0.7618, 2), 4)  # Zn2+/Zn
    -0.8209
    """
    if concentration <= 0:
        raise ValueError(f"concentration must be positive, got {concentration}")
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    
    # Calculate RT/F factor at given temperature
    R = 8.314  # J/(mol·K)
    F = 96487  # C/mol
    T = temperature + 273.15  # Convert to Kelvin
    
    # Nernst equation: E = Edeg + (RT/nF) ln([M^n+])
    factor = (R * T) / (n * F)
    E = E0 + factor * math.log(concentration)
    
    return round(E, 4)


def ion_selective_electrode(
    activity: float,
    slope: float = 0.05916,
    intercept: float = 0.0,
    charge: int = 1
) -> float:
    """
    Calculate potential for ion-selective electrode.
    
    E = K + (slope/z) x log(activity)
    
    Parameters
    ----------
    activity : float
        Ion activity (dimensionless, must be positive)
    slope : float, optional
        Nernstian slope (default 0.05916 V at 25degC)
    intercept : float, optional
        Cell constant K (V)
    charge : int, optional
        Ion charge with sign (default +1)
    
    Returns
    -------
    float
        Cell potential (V)
    
    Raises
    ------
    ValueError
        If activity <= 0 or slope <= 0 or charge == 0
    
    Examples
    --------
    >>> round(ion_selective_electrode(0.01, 0.05916, 0.0, 1), 4)
    -0.1183
    >>> round(ion_selective_electrode(1e-7, 0.05916, 0.0, 1), 4)  # pH 7
    -0.4141
    """
    if activity <= 0:
        raise ValueError(f"activity must be positive, got {activity}")
    if slope <= 0:
        raise ValueError(f"slope must be positive, got {slope}")
    if charge == 0:
        raise ValueError(f"charge cannot be zero")
    
    # E = K + (slope/z) x log(activity)
    E = intercept + (slope / abs(charge)) * math.log10(activity)
    
    return round(E, 4)


def ph_from_potential(
    E: float,
    E0: float = 0.0,
    slope: float = 0.05916
) -> float:
    """
    Calculate pH from electrode potential.
    
    pH = (E0 - E) / slope
    
    The Nernst equation for pH electrode is:
    E = E0 - slope x pH
    Therefore: pH = (E0 - E) / slope
    
    Parameters
    ----------
    E : float
        Measured potential (V)
    E0 : float, optional
        Reference potential (V)
    slope : float, optional
        Electrode slope (V/pH unit, default 0.05916)
    
    Returns
    -------
    float
        pH value
    
    Raises
    ------
    ValueError
        If slope <= 0
    
    Examples
    --------
    >>> ph_from_potential(0.0, 0.0)
    0.0
    >>> round(ph_from_potential(-0.414, 0.0), 1)  # pH 7
    7.0
    """
    if slope <= 0:
        raise ValueError(f"slope must be positive, got {slope}")
    
    # E = E0 - slope x pH, so pH = (E0 - E) / slope
    pH = (E0 - E) / slope
    
    return round(pH, 2)


def reference_potential_convert(
    E_measured: float,
    from_reference: str,
    to_reference: str,
    temperature: float = 25.0
) -> float:
    """
    Convert potential between different reference electrodes.
    
    E_relative to electrode B = E_relative to A - E_A + E_B
    
    Parameters
    ----------
    E_measured : float
        Measured potential (V)
    from_reference : str
        Original reference electrode ('SHE', 'SCE', 'Ag/AgCl')
    to_reference : str
        Target reference electrode ('SHE', 'SCE', 'Ag/AgCl')
    temperature : float, optional
        Temperature in degC (default 25.0)
    
    Returns
    -------
    float
        Converted potential (V)
    
    Raises
    ------
    ValueError
        If invalid reference electrode name provided
    
    Examples
    --------
    >>> round(reference_potential_convert(0.750, 'SHE', 'SCE'), 3)
    0.506
    >>> round(reference_potential_convert(0.750, 'SHE', 'Ag/AgCl'), 3)
    0.553
    """
    # Reference potentials vs SHE at 25degC
    ref_potentials = {
        'SHE': 0.000,
        'SCE': 0.2444,
        'Ag/AgCl': 0.197
    }
    
    from_reference = from_reference.upper()
    to_reference = to_reference.upper()
    
    if from_reference not in ref_potentials:
        raise ValueError(f"Invalid from_reference: {from_reference}. Must be one of {list(ref_potentials.keys())}")
    if to_reference not in ref_potentials:
        raise ValueError(f"Invalid to_reference: {to_reference}. Must be one of {list(ref_potentials.keys())}")
    
    # E_relative to B = E_relative to A - E_A + E_B
    E_vs_SHE = E_measured + ref_potentials[from_reference]
    E_vs_new = E_vs_SHE - ref_potentials[to_reference]
    
    return round(E_vs_new, 3)


def ise_selectivity_coefficient(
    activity_analyte: float,
    activity_interferent: float,
    charge_analyte: int,
    charge_interferent: int
) -> float:
    """
    Calculate ISE selectivity coefficient K_A,I.
    
    K_A,I = (a_A)_e / (a_I)_e^(z_A/z_I)
    
    Parameters
    ----------
    activity_analyte : float
        Analyte activity giving same response
    activity_interferent : float
        Interferent activity
    charge_analyte : int
        Analyte charge
    charge_interferent : int
        Interferent charge
    
    Returns
    -------
    float
        Selectivity coefficient
    
    Raises
    ------
    ValueError
        If any activity is non-positive or charge is zero
    
    Examples
    --------
    >>> round(ise_selectivity_coefficient(4.1e-12, 0.01025, 2, 2), 11)
    4.0e-10
    """
    if activity_analyte <= 0:
        raise ValueError(f"activity_analyte must be positive, got {activity_analyte}")
    if activity_interferent <= 0:
        raise ValueError(f"activity_interferent must be positive, got {activity_interferent}")
    if charge_analyte == 0:
        raise ValueError(f"charge_analyte cannot be zero")
    if charge_interferent == 0:
        raise ValueError(f"charge_interferent cannot be zero")
    
    # K_A,I = (a_A)_e / (a_I)_e^(z_A/z_I)
    exponent = abs(charge_analyte) / abs(charge_interferent)
    K = activity_analyte / (activity_interferent ** exponent)
    
    return K


# =============================================================================
# VOLTAMMETRY Functions
# =============================================================================

def cyclic_voltammetry_peak(
    concentration: float,
    area: float,
    diffusion_coeff: float,
    scan_rate: float,
    n: int,
    temperature: float = 25.0
) -> float:
    """
    Calculate peak current in cyclic voltammetry (Randles-Sevcik equation).
    
    i_p = (2.69 x 10^5) x n^(3/2) x A x D^(1/2) x ν^(1/2) x C
    
    At 25degC, for concentration in mol/cm3, area in cm2, D in cm2/s, ν in V/s.
    
    Parameters
    ----------
    concentration : float
        Analyte concentration (mol/cm3)
    area : float
        Electrode area (cm2)
    diffusion_coeff : float
        Diffusion coefficient (cm2/s)
    scan_rate : float
        Scan rate (V/s)
    n : int
        Number of electrons
    temperature : float, optional
        Temperature in degC (default 25.0, currently unused)
    
    Returns
    -------
    float
        Peak current (A)
    
    Raises
    ------
    ValueError
        If any parameter is non-positive
    
    Examples
    --------
    >>> round(cyclic_voltammetry_peak(1e-6, 0.02, 1e-5, 0.1, 1), 2)
    1.7e-06
    """
    if concentration <= 0:
        raise ValueError(f"concentration must be positive, got {concentration}")
    if area <= 0:
        raise ValueError(f"area must be positive, got {area}")
    if diffusion_coeff <= 0:
        raise ValueError(f"diffusion_coeff must be positive, got {diffusion_coeff}")
    if scan_rate <= 0:
        raise ValueError(f"scan_rate must be positive, got {scan_rate}")
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    
    # Randles-Sevcik equation at 25degC
    # i_p = (2.69 x 10^5) x n^(3/2) x A x D^(1/2) x ν^(1/2) x C
    factor = 2.69e5  # C/mol x cm2/s^(1/2)
    
    ip = factor * (n ** 1.5) * area * math.sqrt(diffusion_coeff) * math.sqrt(scan_rate) * concentration
    
    return ip


def scan_rate_effect(
    peak_current: float,
    scan_rate: float,
    new_scan_rate: float
) -> float:
    """
    Calculate peak current at different scan rate for reversible system.
    
    For reversible systems, peak current is proportional to ν^(1/2):
    i_p ∝ ν^(1/2)
    
    i_p2 = i_p1 x √(ν2/ν1)
    
    Parameters
    ----------
    peak_current : float
        Original peak current (A)
    scan_rate : float
        Original scan rate (V/s)
    new_scan_rate : float
        New scan rate (V/s)
    
    Returns
    -------
    float
        New peak current (A)
    
    Raises
    ------
    ValueError
        If any parameter is non-positive
    
    Examples
    --------
    >>> round(scan_rate_effect(1e-6, 0.1, 0.4), 7)  # Double scan rate
    2e-06
    """
    if peak_current <= 0:
        raise ValueError(f"peak_current must be positive, got {peak_current}")
    if scan_rate <= 0:
        raise ValueError(f"scan_rate must be positive, got {scan_rate}")
    if new_scan_rate <= 0:
        raise ValueError(f"new_scan_rate must be positive, got {new_scan_rate}")
    
    # i_p2 = i_p1 x √(ν2/ν1)
    ratio = math.sqrt(new_scan_rate / scan_rate)
    new_peak_current = peak_current * ratio
    
    return new_peak_current


def voltammetry_half_wave_potential(
    E_anodic: float,
    E_cathodic: float
) -> float:
    """
    Calculate half-wave potential from cyclic voltammetry peak potentials.
    
    E_1/2 = (E_p,a + E_p,c) / 2
    
    Parameters
    ----------
    E_anodic : float
        Anodic peak potential (V)
    E_cathodic : float
        Cathodic peak potential (V)
    
    Returns
    -------
    float
        Half-wave potential (V)
    
    Examples
    --------
    >>> voltammetry_half_wave_potential(0.45, 0.35)
    0.40
    """
    # TODO: Implement
    pass


def limiting_current_concentration(
    limiting_current: float,
    K_constant: float
) -> float:
    """
    Calculate concentration from limiting current.
    
    [A] = i_l / K
    
    Parameters
    ----------
    limiting_current : float
        Measured limiting current (A)
    K_constant : float
        Calibration constant (A/M or A·L/mol)
    
    Returns
    -------
    float
        Analyte concentration (M)
    
    Examples
    --------
    >>> limiting_current_concentration(1e-6, 1e4)
    1e-10
    """
    # TODO: Implement
    pass


# =============================================================================
# COULOMETRY Functions
# =============================================================================

def coulometry_moles(
    charge: float,
    n_electrons: int
) -> float:
    """
    Calculate moles of analyte from total charge (Faraday's law).
    
    N_A = Q / (n x F)
    
    Parameters
    ----------
    charge : float
        Total charge passed (C)
    n_electrons : int
        Number of electrons per molecule
    
    Returns
    -------
    float
        Moles of analyte
    
    Raises
    ------
    ValueError
        If charge < 0 or n_electrons <= 0
    
    Examples
    --------
    >>> round(coulometry_moles(96487, 1), 2)  # 1 Faraday
    1.0
    >>> round(coulometry_moles(16.11, 2), 5)  # Cu2+ reduction
    8.35e-05
    """
    if charge < 0:
        raise ValueError(f"charge must be non-negative, got {charge}")
    if n_electrons <= 0:
        raise ValueError(f"n_electrons must be positive, got {n_electrons}")
    
    F = 96487  # C/mol e-
    moles = charge / (n_electrons * F)
    
    return moles


def coulometry_charge(
    moles: float,
    n_electrons: int
) -> float:
    """
    Calculate charge needed for complete electrolysis.
    
    Q = n x F x N_A
    
    Parameters
    ----------
    moles : float
        Moles of analyte
    n_electrons : int
        Number of electrons per molecule
    
    Returns
    -------
    float
        Total charge (C)
    
    Examples
    --------
    >>> coulometry_charge(1.0, 1)
    96487.0
    >>> coulometry_charge(1e-3, 2)
    192.97
    """
    # TODO: Implement
    pass


def coulometry_constant_current(
    current: float,
    time: float,
    n_electrons: int
) -> float:
    """
    Calculate moles from constant current electrolysis.
    
    N_A = (i x t_e) / (n x F)
    
    Parameters
    ----------
    current : float
        Constant current (A)
    time : float
        Electrolysis time (s)
    n_electrons : int
        Number of electrons per molecule
    
    Returns
    -------
    float
        Moles of analyte
    
    Examples
    --------
    >>> coulometry_constant_current(0.03645, 221.8, 1)
    8.38e-5
    """
    # TODO: Implement
    pass


def coulometry_electrolysis_time(
    moles: float,
    current: float,
    n_electrons: int
) -> float:
    """
    Calculate time needed for complete electrolysis.
    
    t_e = (n x F x N_A) / i
    
    Parameters
    ----------
    moles : float
        Moles of analyte
    current : float
        Applied current (A)
    n_electrons : int
        Number of electrons per molecule
    
    Returns
    -------
    float
        Electrolysis time (s)
    
    Examples
    --------
    >>> coulometry_electrolysis_time(1e-3, 0.1, 1)
    964.87
    """
    # TODO: Implement
    pass


def coulometry_purity(
    mass_sample: float,
    charge: float,
    n_electrons: int,
    molar_mass: float
) -> float:
    """
    Calculate sample purity from coulometric analysis.
    
    % purity = (calculated_mass / sample_mass) x 100
    
    Parameters
    ----------
    mass_sample : float
        Sample mass (g)
    charge : float
        Total charge (C)
    n_electrons : int
        Number of electrons per molecule
    molar_mass : float
        Molar mass of pure analyte (g/mol)
    
    Returns
    -------
    float
        Purity percentage (0-100)
    
    Examples
    --------
    >>> coulometry_purity(0.1342, 7.86, 1, 158.11)  # Na2S2O3
    98.73
    """
    # TODO: Implement
    pass


# =============================================================================
# AMPEROMETRY Functions
# =============================================================================

def amperometry_current(
    concentration: float,
    sensitivity: float
) -> float:
    """
    Calculate current for amperometric sensor.
    
    i = sensitivity x concentration
    
    Parameters
    ----------
    concentration : float
        Analyte concentration (M or other units)
    sensitivity : float
        Sensor sensitivity (A/M or A/unit)
    
    Returns
    -------
    float
        Measured current (A)
    
    Raises
    ------
    ValueError
        If concentration < 0 or sensitivity <= 0
    
    Examples
    --------
    >>> amperometry_current(1e-6, 1e4)
    0.01
    """
    if concentration < 0:
        raise ValueError(f"concentration must be non-negative, got {concentration}")
    if sensitivity <= 0:
        raise ValueError(f"sensitivity must be positive, got {sensitivity}")
    
    # i = sensitivity x concentration
    current = sensitivity * concentration
    
    return current


def amperometry_concentration(
    current: float,
    sensitivity: float
) -> float:
    """
    Calculate concentration from amperometric measurement.
    
    [A] = i / sensitivity
    
    Parameters
    ----------
    current : float
        Measured current (A)
    sensitivity : float
        Sensor sensitivity (A/M or A/unit)
    
    Returns
    -------
    float
        Analyte concentration (M or other units)
    
    Examples
    --------
    >>> amperometry_concentration(0.01, 1e4)
    1e-6
    """
    # TODO: Implement
    pass


# =============================================================================
# CONDUCTOMETRY Functions
# =============================================================================

def conductivity_from_resistance(
    resistance: float,
    cell_constant: float
) -> float:
    """
    Calculate conductivity from measured resistance.
    
    κ = k / R  (where k = l/A = cell constant)
    
    Parameters
    ----------
    resistance : float
        Measured resistance (Ω)
    cell_constant : float
        Cell constant k (cm-1)
    
    Returns
    -------
    float
        Conductivity (S/cm)
    
    Examples
    --------
    >>> conductivity_from_resistance(1000, 1.0)
    0.001
    """
    # TODO: Implement
    pass


def conductivity_cell_constant(
    resistance: float,
    conductivity: float
) -> float:
    """
    Determine cell constant from standard solution.
    
    k = R x κ
    
    Parameters
    ----------
    resistance : float
        Measured resistance of standard (Ω)
    conductivity : float
        Known conductivity of standard (S/cm)
    
    Returns
    -------
    float
        Cell constant (cm-1)
    
    Raises
    ------
    ValueError
        If resistance <= 0 or conductivity <= 0
    
    Examples
    --------
    >>> round(conductivity_cell_constant(500, 0.001413), 4)  # 0.01 M KCl at 25degC
    0.7065
    """
    if resistance <= 0:
        raise ValueError(f"resistance must be positive, got {resistance}")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive, got {conductivity}")
    
    # k = R x κ
    cell_constant = resistance * conductivity
    
    return cell_constant


def molar_conductivity(
    conductivity: float,
    concentration: float
) -> float:
    """
    Calculate molar conductivity.
    
    Λ_m = κ / c
    
    Parameters
    ----------
    conductivity : float
        Conductivity (S/cm)
    concentration : float
        Concentration (mol/cm3)
    
    Returns
    -------
    float
        Molar conductivity (S·cm2/mol)
    
    Examples
    --------
    >>> molar_conductivity(0.001413, 1e-5)  # 0.01 M KCl
    141.3
    """
    # TODO: Implement
    pass


def kohlrausch_equation(
    concentration: float,
    limiting_conductivity: float,
    kohlrausch_coefficient: float
) -> float:
    """
    Calculate molar conductivity for strong electrolyte (Kohlrausch's law).
    
    Λ_m = Λ_mdeg - K x √c
    
    Parameters
    ----------
    concentration : float
        Concentration (M)
    limiting_conductivity : float
        Limiting molar conductivity at infinite dilution (S·cm2/mol)
    kohlrausch_coefficient : float
        Kohlrausch coefficient
    
    Returns
    -------
    float
        Molar conductivity (S·cm2/mol)
    
    Examples
    --------
    >>> kohlrausch_equation(0.01, 149.9, 100)
    139.9
    """
    # TODO: Implement
    pass


# =============================================================================
# Additional Utility Functions
# =============================================================================

def faraday_constant() -> float:
    """Return Faraday's constant (96487 C/mol e-)."""
    return 96487.0


def nernst_slope(temperature: float = 25.0) -> float:
    """
    Calculate Nernst equation slope RT/F x ln(10).
    
    Parameters
    ----------
    temperature : float, optional
        Temperature in degC (default 25.0)
    
    Returns
    -------
    float
        Nernst slope (V/decade)
    
    Examples
    --------
    >>> nernst_slope(25.0)
    0.05916
    """
    # TODO: Implement
    pass


# =============================================================================
# Data Classes for Electrochemical Systems
# =============================================================================

@dataclass
class ElectrodeSystem:
    """Container for electrochemical cell parameters."""
    reference_potential: float  # V
    reference_type: str  # 'SHE', 'SCE', 'Ag/AgCl'
    temperature: float = 25.0  # degC


@dataclass
class VoltammogramPeaks:
    """Container for cyclic voltammetry peak data."""
    E_anodic: float  # V
    E_cathodic: float  # V
    i_anodic: float  # A
    i_cathodic: float  # A
    
    @property
    def half_wave_potential(self) -> float:
        """Calculate E_1/2 from peak potentials."""
        return (self.E_anodic + self.E_cathodic) / 2
    
    @property
    def peak_separation(self) -> float:
        """Calculate DeltaE_p."""
        return abs(self.E_anodic - self.E_cathodic)
    
    @property
    def is_reversible(self, n: int = 1) -> bool:
        """Check if system shows reversible behavior."""
        expected_separation = 0.059 / n  # V at 25degC
        return abs(self.peak_separation - expected_separation) < 0.01


if __name__ == '__main__':
    # Placeholder for testing
    print("Electrochemical Analysis Tools - L3 Implementation")
    print("Module loaded successfully")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'amperometry_concentration', 'description': 'Calculate concentration from amperometric measurement.\n\n[A] = i / sensitivity\n\nParameters\n----------\ncurrent : float\n    Measured current (A)\nsensitivity : float\n    Sensor sensitivity (A/M or A/unit)\n\nReturns\n-------\nfloat\n    Analyte concentration (M or other units)\n\nExamples\n--------\n>>> amperometry_concentration(0.01, 1e4)\n1e-6', 'inputSchema': {'type': 'object', 'properties': {'current': {'type': 'number', 'description': 'Current'}, 'sensitivity': {'type': 'number', 'description': 'Sensitivity'}}, 'required': ['current', 'sensitivity']}},
    {'name': 'amperometry_current', 'description': 'Calculate current for amperometric sensor.\n\ni = sensitivity x concentration\n\nParameters\n----------\nconcentration : float\n    Analyte concentration (M or other units)\nsensitivity : float\n    Sensor sensitivity (A/M or A/unit)\n\nReturns\n-------\nfloat\n    Measured current (A)\n\nRaises\n------\nValueError\n    If concentration < 0 or sensitivity <= 0\n\nExamples\n--------\n>>> amperometry_current(1e-6, 1e4)\n0.01', 'inputSchema': {'type': 'object', 'properties': {'concentration': {'type': 'string', 'description': 'Concentration'}, 'sensitivity': {'type': 'number', 'description': 'Sensitivity'}}, 'required': ['concentration', 'sensitivity']}},
    {'name': 'conductivity_cell_constant', 'description': 'Determine cell constant from standard solution.\n\nk = R x κ\n\nParameters\n----------\nresistance : float\n    Measured resistance of standard (Ω)\nconductivity : float\n    Known conductivity of standard (S/cm)\n\nReturns\n-------\nfloat\n    Cell constant (cm-1)\n\nRaises\n------\nValueError\n    If resistance <= 0 or conductivity <= 0\n\nExamples\n--------\n>>> round(conductivity_cell_constant(500, 0.001413), 4)  # 0.01 M KCl at 25degC\n0.7065', 'inputSchema': {'type': 'object', 'properties': {'resistance': {'type': 'number', 'description': 'Resistance'}, 'conductivity': {'type': 'number', 'description': 'Conductivity'}}, 'required': ['resistance', 'conductivity']}},
    {'name': 'conductivity_from_resistance', 'description': 'Calculate conductivity from measured resistance.\n\nκ = k / R  (where k = l/A = cell constant)\n\nParameters\n----------\nresistance : float\n    Measured resistance (Ω)\ncell_constant : float\n    Cell constant k (cm-1)\n\nReturns\n-------\nfloat\n    Conductivity (S/cm)\n\nExamples\n--------\n>>> conductivity_from_resistance(1000, 1.0)\n0.001', 'inputSchema': {'type': 'object', 'properties': {'resistance': {'type': 'number', 'description': 'Resistance'}, 'cell_constant': {'type': 'number', 'description': 'Cell Constant'}}, 'required': ['resistance', 'cell_constant']}},
    {'name': 'coulometry_charge', 'description': 'Calculate charge needed for complete electrolysis.\n\nQ = n x F x N_A\n\nParameters\n----------\nmoles : float\n    Moles of analyte\nn_electrons : int\n    Number of electrons per molecule\n\nReturns\n-------\nfloat\n    Total charge (C)\n\nExamples\n--------\n>>> coulometry_charge(1.0, 1)\n96487.0\n>>> coulometry_charge(1e-3, 2)\n192.97', 'inputSchema': {'type': 'object', 'properties': {'moles': {'type': 'number', 'description': 'Moles'}, 'n_electrons': {'type': 'number', 'description': 'N Electrons'}}, 'required': ['moles', 'n_electrons']}},
    {'name': 'coulometry_constant_current', 'description': 'Calculate moles from constant current electrolysis.\n\nN_A = (i x t_e) / (n x F)\n\nParameters\n----------\ncurrent : float\n    Constant current (A)\ntime : float\n    Electrolysis time (s)\nn_electrons : int\n    Number of electrons per molecule\n\nReturns\n-------\nfloat\n    Moles of analyte\n\nExamples\n--------\n>>> coulometry_constant_current(0.03645, 221.8, 1)\n8.38e-5', 'inputSchema': {'type': 'object', 'properties': {'current': {'type': 'number', 'description': 'Current'}, 'time': {'type': 'string', 'description': 'Time'}, 'n_electrons': {'type': 'number', 'description': 'N Electrons'}}, 'required': ['current', 'time', 'n_electrons']}},
    {'name': 'coulometry_electrolysis_time', 'description': 'Calculate time needed for complete electrolysis.\n\nt_e = (n x F x N_A) / i\n\nParameters\n----------\nmoles : float\n    Moles of analyte\ncurrent : float\n    Applied current (A)\nn_electrons : int\n    Number of electrons per molecule\n\nReturns\n-------\nfloat\n    Electrolysis time (s)\n\nExamples\n--------\n>>> coulometry_electrolysis_time(1e-3, 0.1, 1)\n964.87', 'inputSchema': {'type': 'object', 'properties': {'moles': {'type': 'number', 'description': 'Moles'}, 'current': {'type': 'number', 'description': 'Current'}, 'n_electrons': {'type': 'number', 'description': 'N Electrons'}}, 'required': ['moles', 'current', 'n_electrons']}},
    {'name': 'coulometry_moles', 'description': "Calculate moles of analyte from total charge (Faraday's law).\n\nN_A = Q / (n x F)\n\nParameters\n----------\ncharge : float\n    Total charge passed (C)\nn_electrons : int\n    Number of electrons per molecule\n\nReturns\n-------\nfloat\n    Moles of analyte\n\nRaises\n------\nValueError\n    If charge < 0 or n_electrons <= 0\n\nExamples\n--------\n>>> round(coulometry_moles(96487, 1), 2)  # 1 Faraday\n1.0\n>>> round(coulometry_moles(16.11, 2), 5)  # Cu2+ reduction\n8.35e-05", 'inputSchema': {'type': 'object', 'properties': {'charge': {'type': 'number', 'description': 'Charge'}, 'n_electrons': {'type': 'number', 'description': 'N Electrons'}}, 'required': ['charge', 'n_electrons']}},
    {'name': 'coulometry_purity', 'description': 'Calculate sample purity from coulometric analysis.\n\n% purity = (calculated_mass / sample_mass) x 100\n\nParameters\n----------\nmass_sample : float\n    Sample mass (g)\ncharge : float\n    Total charge (C)\nn_electrons : int\n    Number of electrons per molecule\nmolar_mass : float\n    Molar mass of pure analyte (g/mol)\n\nReturns\n-------\nfloat\n    Purity percentage (0-100)\n\nExamples\n--------\n>>> coulometry_purity(0.1342, 7.86, 1, 158.11)  # Na2S2O3\n98.73', 'inputSchema': {'type': 'object', 'properties': {'mass_sample': {'type': 'string', 'description': 'Mass Sample'}, 'charge': {'type': 'number', 'description': 'Charge'}, 'n_electrons': {'type': 'number', 'description': 'N Electrons'}, 'molar_mass': {'type': 'number', 'description': 'Molar Mass'}}, 'required': ['mass_sample', 'charge', 'n_electrons', 'molar_mass']}},
    {'name': 'cyclic_voltammetry_peak', 'description': 'Calculate peak current in cyclic voltammetry (Randles-Sevcik equation).\n\ni_p = (2.69 x 10^5) x n^(3/2) x A x D^(1/2) x ν^(1/2) x C\n\nAt 25degC, for concentration in mol/cm3, area in cm2, D in cm2/s, ν in V/s.\n\nParameters\n----------\nconcentration : float\n    Analyte concentration (mol/cm3)\narea : float\n    Electrode area (cm2)\ndiffusion_coeff : float\n    Diffusion coefficient (cm2/s)\nscan_rate : float\n    Scan rate (V/s)\nn : int\n    Number of electrons\ntemperature : float, optional\n    Temperature in degC (default 25.0, currently unused)\n\nReturns\n-------\nfloat\n    Peak current (A)\n\nRaises\n------\nValueError\n    If any parameter is non-positive\n\nExamples\n--------\n>>> round(cyclic_voltammetry_peak(1e-6, 0.02, 1e-5, 0.1, 1), 2)\n1.7e-06', 'inputSchema': {'type': 'object', 'properties': {'concentration': {'type': 'string', 'description': 'Concentration'}, 'area': {'type': 'number', 'description': 'Area'}, 'diffusion_coeff': {'type': 'string', 'description': 'Diffusion Coeff'}, 'scan_rate': {'type': 'number', 'description': 'Scan Rate'}, 'n': {'type': 'number', 'description': 'N'}, 'temperature': {'type': 'number', 'description': 'Temperature', 'default': 25.0}}, 'required': ['concentration', 'area', 'diffusion_coeff', 'scan_rate', 'n']}},
    {'name': 'faraday_constant', 'description': "Return Faraday's constant (96487 C/mol e-).", 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'ion_selective_electrode', 'description': 'Calculate potential for ion-selective electrode.\n\nE = K + (slope/z) x log(activity)\n\nParameters\n----------\nactivity : float\n    Ion activity (dimensionless, must be positive)\nslope : float, optional\n    Nernstian slope (default 0.05916 V at 25degC)\nintercept : float, optional\n    Cell constant K (V)\ncharge : int, optional\n    Ion charge with sign (default +1)\n\nReturns\n-------\nfloat\n    Cell potential (V)\n\nRaises\n------\nValueError\n    If activity <= 0 or slope <= 0 or charge == 0\n\nExamples\n--------\n>>> round(ion_selective_electrode(0.01, 0.05916, 0.0, 1), 4)\n-0.1183\n>>> round(ion_selective_electrode(1e-7, 0.05916, 0.0, 1), 4)  # pH 7\n-0.4141', 'inputSchema': {'type': 'object', 'properties': {'activity': {'type': 'number', 'description': 'Activity'}, 'slope': {'type': 'number', 'description': 'Slope', 'default': 0.05916}, 'intercept': {'type': 'number', 'description': 'Intercept', 'default': 0.0}, 'charge': {'type': 'number', 'description': 'Charge', 'default': 1}}, 'required': ['activity']}},
    {'name': 'ise_selectivity_coefficient', 'description': 'Calculate ISE selectivity coefficient K_A,I.\n\nK_A,I = (a_A)_e / (a_I)_e^(z_A/z_I)\n\nParameters\n----------\nactivity_analyte : float\n    Analyte activity giving same response\nactivity_interferent : float\n    Interferent activity\ncharge_analyte : int\n    Analyte charge\ncharge_interferent : int\n    Interferent charge\n\nReturns\n-------\nfloat\n    Selectivity coefficient\n\nRaises\n------\nValueError\n    If any activity is non-positive or charge is zero\n\nExamples\n--------\n>>> round(ise_selectivity_coefficient(4.1e-12, 0.01025, 2, 2), 11)\n4.0e-10', 'inputSchema': {'type': 'object', 'properties': {'activity_analyte': {'type': 'string', 'description': 'Activity Analyte'}, 'activity_interferent': {'type': 'number', 'description': 'Activity Interferent'}, 'charge_analyte': {'type': 'string', 'description': 'Charge Analyte'}, 'charge_interferent': {'type': 'number', 'description': 'Charge Interferent'}}, 'required': ['activity_analyte', 'activity_interferent', 'charge_analyte', 'charge_interferent']}},
    {'name': 'kohlrausch_equation', 'description': "Calculate molar conductivity for strong electrolyte (Kohlrausch's law).\n\nΛ_m = Λ_mdeg - K x √c\n\nParameters\n----------\nconcentration : float\n    Concentration (M)\nlimiting_conductivity : float\n    Limiting molar conductivity at infinite dilution (S·cm2/mol)\nkohlrausch_coefficient : float\n    Kohlrausch coefficient\n\nReturns\n-------\nfloat\n    Molar conductivity (S·cm2/mol)\n\nExamples\n--------\n>>> kohlrausch_equation(0.01, 149.9, 100)\n139.9", 'inputSchema': {'type': 'object', 'properties': {'concentration': {'type': 'string', 'description': 'Concentration'}, 'limiting_conductivity': {'type': 'number', 'description': 'Limiting Conductivity'}, 'kohlrausch_coefficient': {'type': 'number', 'description': 'Kohlrausch Coefficient'}}, 'required': ['concentration', 'limiting_conductivity', 'kohlrausch_coefficient']}},
    {'name': 'limiting_current_concentration', 'description': 'Calculate concentration from limiting current.\n\n[A] = i_l / K\n\nParameters\n----------\nlimiting_current : float\n    Measured limiting current (A)\nK_constant : float\n    Calibration constant (A/M or A·L/mol)\n\nReturns\n-------\nfloat\n    Analyte concentration (M)\n\nExamples\n--------\n>>> limiting_current_concentration(1e-6, 1e4)\n1e-10', 'inputSchema': {'type': 'object', 'properties': {'limiting_current': {'type': 'number', 'description': 'Limiting Current'}, 'K_constant': {'type': 'number', 'description': 'K Constant'}}, 'required': ['limiting_current', 'K_constant']}},
    {'name': 'molar_conductivity', 'description': 'Calculate molar conductivity.\n\nΛ_m = κ / c\n\nParameters\n----------\nconductivity : float\n    Conductivity (S/cm)\nconcentration : float\n    Concentration (mol/cm3)\n\nReturns\n-------\nfloat\n    Molar conductivity (S·cm2/mol)\n\nExamples\n--------\n>>> molar_conductivity(0.001413, 1e-5)  # 0.01 M KCl\n141.3', 'inputSchema': {'type': 'object', 'properties': {'conductivity': {'type': 'number', 'description': 'Conductivity'}, 'concentration': {'type': 'string', 'description': 'Concentration'}}, 'required': ['conductivity', 'concentration']}},
    {'name': 'nernst_slope', 'description': 'Calculate Nernst equation slope RT/F x ln(10).\n\nParameters\n----------\ntemperature : float, optional\n    Temperature in degC (default 25.0)\n\nReturns\n-------\nfloat\n    Nernst slope (V/decade)\n\nExamples\n--------\n>>> nernst_slope(25.0)\n0.05916', 'inputSchema': {'type': 'object', 'properties': {'temperature': {'type': 'number', 'description': 'Temperature', 'default': 25.0}}, 'required': []}},
    {'name': 'ph_from_potential', 'description': 'Calculate pH from electrode potential.\n\npH = (E0 - E) / slope\n\nThe Nernst equation for pH electrode is:\nE = E0 - slope x pH\nTherefore: pH = (E0 - E) / slope\n\nParameters\n----------\nE : float\n    Measured potential (V)\nE0 : float, optional\n    Reference potential (V)\nslope : float, optional\n    Electrode slope (V/pH unit, default 0.05916)\n\nReturns\n-------\nfloat\n    pH value\n\nRaises\n------\nValueError\n    If slope <= 0\n\nExamples\n--------\n>>> ph_from_potential(0.0, 0.0)\n0.0\n>>> round(ph_from_potential(-0.414, 0.0), 1)  # pH 7\n7.0', 'inputSchema': {'type': 'object', 'properties': {'E': {'type': 'number', 'description': 'E'}, 'E0': {'type': 'number', 'description': 'E0', 'default': 0.0}, 'slope': {'type': 'number', 'description': 'Slope', 'default': 0.05916}}, 'required': ['E']}},
    {'name': 'potentiometry_nernst', 'description': 'Calculate electrode potential using Nernst equation.\n\nE = Edeg - (RT/nF) ln(Q) = Edeg - (0.05916/n) log(Q) at 25degC\n\nFor reduction: M^n+ + ne- -> M\nQ = 1/[M^n+]\nE = Edeg - (RT/nF) ln(1/[M^n+]) = Edeg + (RT/nF) ln([M^n+])\n\nParameters\n----------\nconcentration : float\n    Analyte concentration or activity (M)\nE0 : float\n    Standard reduction potential (V)\nn : int\n    Number of electrons transferred\ntemperature : float, optional\n    Temperature in degC (default 25.0)\n\nReturns\n-------\nfloat\n    Electrode potential (V)\n\nRaises\n------\nValueError\n    If concentration <= 0 or n <= 0\n\nExamples\n--------\n>>> round(potentiometry_nernst(0.1, 0.7996, 1), 4)  # Ag+/Ag\n0.7405\n>>> round(potentiometry_nernst(0.01, -0.7618, 2), 4)  # Zn2+/Zn\n-0.8209', 'inputSchema': {'type': 'object', 'properties': {'concentration': {'type': 'string', 'description': 'Concentration'}, 'E0': {'type': 'number', 'description': 'E0'}, 'n': {'type': 'number', 'description': 'N'}, 'temperature': {'type': 'number', 'description': 'Temperature', 'default': 25.0}}, 'required': ['concentration', 'E0', 'n']}},
    {'name': 'reference_potential_convert', 'description': "Convert potential between different reference electrodes.\n\nE_relative to electrode B = E_relative to A - E_A + E_B\n\nParameters\n----------\nE_measured : float\n    Measured potential (V)\nfrom_reference : str\n    Original reference electrode ('SHE', 'SCE', 'Ag/AgCl')\nto_reference : str\n    Target reference electrode ('SHE', 'SCE', 'Ag/AgCl')\ntemperature : float, optional\n    Temperature in degC (default 25.0)\n\nReturns\n-------\nfloat\n    Converted potential (V)\n\nRaises\n------\nValueError\n    If invalid reference electrode name provided\n\nExamples\n--------\n>>> round(reference_potential_convert(0.750, 'SHE', 'SCE'), 3)\n0.506\n>>> round(reference_potential_convert(0.750, 'SHE', 'Ag/AgCl'), 3)\n0.553", 'inputSchema': {'type': 'object', 'properties': {'E_measured': {'type': 'number', 'description': 'E Measured'}, 'from_reference': {'type': 'string', 'description': 'From Reference'}, 'to_reference': {'type': 'string', 'description': 'To Reference'}, 'temperature': {'type': 'number', 'description': 'Temperature', 'default': 25.0}}, 'required': ['E_measured', 'from_reference', 'to_reference']}},
    {'name': 'scan_rate_effect', 'description': 'Calculate peak current at different scan rate for reversible system.\n\nFor reversible systems, peak current is proportional to ν^(1/2):\ni_p ∝ ν^(1/2)\n\ni_p2 = i_p1 x √(ν2/ν1)\n\nParameters\n----------\npeak_current : float\n    Original peak current (A)\nscan_rate : float\n    Original scan rate (V/s)\nnew_scan_rate : float\n    New scan rate (V/s)\n\nReturns\n-------\nfloat\n    New peak current (A)\n\nRaises\n------\nValueError\n    If any parameter is non-positive\n\nExamples\n--------\n>>> round(scan_rate_effect(1e-6, 0.1, 0.4), 7)  # Double scan rate\n2e-06', 'inputSchema': {'type': 'object', 'properties': {'peak_current': {'type': 'number', 'description': 'Peak Current'}, 'scan_rate': {'type': 'number', 'description': 'Scan Rate'}, 'new_scan_rate': {'type': 'number', 'description': 'New Scan Rate'}}, 'required': ['peak_current', 'scan_rate', 'new_scan_rate']}},
    {'name': 'voltammetry_half_wave_potential', 'description': 'Calculate half-wave potential from cyclic voltammetry peak potentials.\n\nE_1/2 = (E_p,a + E_p,c) / 2\n\nParameters\n----------\nE_anodic : float\n    Anodic peak potential (V)\nE_cathodic : float\n    Cathodic peak potential (V)\n\nReturns\n-------\nfloat\n    Half-wave potential (V)\n\nExamples\n--------\n>>> voltammetry_half_wave_potential(0.45, 0.35)\n0.40', 'inputSchema': {'type': 'object', 'properties': {'E_anodic': {'type': 'number', 'description': 'E Anodic'}, 'E_cathodic': {'type': 'number', 'description': 'E Cathodic'}}, 'required': ['E_anodic', 'E_cathodic']}}
]
