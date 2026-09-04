"""
Laser and Photochemistry Tools - L3 Implementation

Core functions for laser physics and photochemistry:
- Einstein coefficients
- Laser gain and threshold
- Beer-Lambert absorption
- Quantum yield
- Photochemical kinetics
- Excited state lifetimes

Source: LibreTexts Physical Chemistry Ch15
## Solver Instructions (for AI Agent)

When you encounter laser physics, photochemistry, Beer-Lambert, or quantum yield problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Einstein coefficients**: A↔B conversion? Use `einstein_A_from_B(B, freq)` or `einstein_B_from_A(A, freq)`; lifetime? `spontaneous_emission_lifetime(A)`; linewidth? `natural_linewidth(A)`
- **Doppler broadening**: `doppler_linewidth(freq, T, mass_amu)`
- **Beer-Lambert**: Absorbance? `beer_lambert_absorbance(c, l, ε)`; Concentration from A? `concentration_from_absorbance(A, l, ε)`; Transmittance? `beer_lambert_transmittance(c, l, ε)`; A↔T? `absorbance_from_transmittance(T)` / `transmittance_from_absorbance(A)`
- **Laser physics**: Gain? `laser_gain_coefficient(sigma, delta_N)`; Threshold? `laser_threshold_gain(gain, R1, R2, L)`; Mode spacing? `cavity_mode_spacing(L)`; Coherence? `coherence_length(lambda, Deltaν)`
- **Photochemistry**: Photon energy? `photon_energy(wavelength_nm)` or `photon_energy_eV(wavelength_nm)`; Quantum yield? `quantum_yield(reactant_consumed, photons_absorbed)`; Photon flux? `photon_flux_moles(power_W, wavelength_nm)`
- **Fluorescence**: Quenched lifetime? `fluorescence_lifetime(tau_0, quenching_rate)`; Stern-Volmer? `stern_volmer_quenching(tau_0, tau, [Q])`; Energy transfer? `energy_transfer_efficiency(k_ET, tau_0)`
- **Photolysis**: Rate constant? `photolysis_rate_constant(I_0, ε, l, Φ)`

### Step 2: Handle special cases
- **Units**: Einstein A in s-1, B depends on units; frequencies in Hz; wavelengths in m (laser) or nm (photochemistry)
- **Beer-Lambert**: A = εcl (ε in M-1cm-1, c in M, l in cm); valid for A < 2
- **Quantum yield**: Φ > 1 = chain reaction; Φ = 1 = one molecule per photon; Φ < 1 = competing processes
- **Stern-Volmer**: τ0/τ = 1 + k_q[Q]; k_q > 1010 M-1s-1 = diffusion-controlled

### Examples
```python
# Example 1: Beer-Lambert
beer_lambert_absorbance(0.001, 1, 1000)  # -> A = 1.0
concentration_from_absorbance(0.5, 1, 1000)  # -> 0.0005 M

# Example 2: Photon energy
photon_energy_eV(500)  # -> 2.48 eV

# Example 3: Stern-Volmer quenching
stern_volmer_quenching(1e-8, 5e-9, 0.01)  # -> k_q = 1e10 M-1s-1 (diffusion-controlled)
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
SPEED_OF_LIGHT = 2.99792458e8     # m/s
SPEED_OF_LIGHT_CM = SPEED_OF_LIGHT * 100  # cm/s
BOLTZMANN = 1.380649e-23          # J/K


# =============================================================================
# EINSTEIN COEFFICIENTS
# =============================================================================

def einstein_A_from_B(B_value: float, frequency_Hz: float) -> float:
    """
    Calculate Einstein A coefficient from B coefficient.
    
    A = (8pihν3/c3) B
    
    Args:
        B_value: Einstein B coefficient (m3/(J·s2) or appropriate units)
        frequency_Hz: Transition frequency in Hz
    
    Returns:
        Einstein A coefficient in s-1 (spontaneous emission rate)
    
    Example:
        >>> A = einstein_A_from_B(1e-20, 5e14)  # Visible light
    """
    return (8 * np.pi * PLANCK_CONSTANT * frequency_Hz**3 / 
            SPEED_OF_LIGHT**3) * B_value


def einstein_B_from_A(A_value: float, frequency_Hz: float) -> float:
    """
    Calculate Einstein B coefficient from A coefficient.
    
    B = (c3/8pihν3) A
    
    Args:
        A_value: Einstein A coefficient in s-1
        frequency_Hz: Transition frequency in Hz
    
    Returns:
        Einstein B coefficient
    """
    return (SPEED_OF_LIGHT**3 / 
            (8 * np.pi * PLANCK_CONSTANT * frequency_Hz**3)) * A_value


def einstein_B_absorption_from_B_emission(B_emission: float, 
                                          g_upper: int, g_lower: int) -> float:
    """
    Calculate Einstein B coefficient for absorption from emission coefficient.
    
    B_abs = (g_upper/g_lower) B_em
    
    where g are the degeneracies of the levels
    
    Args:
        B_emission: Einstein B coefficient for stimulated emission
        g_upper: Degeneracy of upper level
        g_lower: Degeneracy of lower level
    
    Returns:
        Einstein B coefficient for absorption
    """
    return (g_upper / g_lower) * B_emission


def spontaneous_emission_lifetime(A_value: float) -> float:
    """
    Calculate radiative lifetime from Einstein A coefficient.
    
    τ = 1/A
    
    Args:
        A_value: Einstein A coefficient in s-1
    
    Returns:
        Radiative lifetime in seconds
    
    Example:
        >>> spontaneous_emission_lifetime(1e8)  # Typical allowed transition
        1e-8  # 10 ns
    """
    if A_value <= 0:
        raise ValueError("A coefficient must be positive")
    return 1.0 / A_value


def natural_linewidth(A_value: float) -> float:
    """
    Calculate natural linewidth (FWHM) from Einstein A.
    
    Deltaν = A/(2pi)
    
    Args:
        A_value: Einstein A coefficient in s-1
    
    Returns:
        Natural linewidth in Hz
    
    Example:
        >>> natural_linewidth(1e8)
        1.59e7  # ~16 MHz
    """
    return A_value / (2 * np.pi)


def doppler_linewidth(frequency_Hz: float, temperature: float, 
                      mass_amu: float) -> float:
    """
    Calculate Doppler broadening linewidth (FWHM).
    
    Deltaν_D = (2ν/c) √(2kT ln 2 / m)
    
    Args:
        frequency_Hz: Transition frequency in Hz
        temperature: Temperature in K
        mass_amu: Atomic/molecular mass in amu
    
    Returns:
        Doppler linewidth (FWHM) in Hz
    
    Example:
        >>> doppler_linewidth(5e14, 300, 20)  # Visible, room T
        1e9  # ~1 GHz
    """
    mass_kg = mass_amu * 1.66053907e-27  # Convert amu to kg
    
    delta_nu = (2 * frequency_Hz / SPEED_OF_LIGHT) * \
               np.sqrt(2 * BOLTZMANN * temperature * np.log(2) / mass_kg)
    
    return delta_nu


# =============================================================================
# BEER-LAMBERT LAW
# =============================================================================

def beer_lambert_absorbance(concentration: float, path_length: float, 
                            epsilon: float) -> float:
    """
    Calculate absorbance using Beer-Lambert law.
    
    A = ε·c·l
    
    Args:
        concentration: Concentration in M (mol/L)
        path_length: Path length in cm
        epsilon: Molar absorptivity in M-1·cm-1
    
    Returns:
        Absorbance (dimensionless)
    
    Example:
        >>> beer_lambert_absorbance(0.01, 1, 1000)  # 10 mM, 1 cm path
        10  # Absorbance = 10 (very absorbing)
    """
    return epsilon * concentration * path_length


def beer_lambert_transmittance(concentration: float, path_length: float, 
                                epsilon: float) -> float:
    """
    Calculate transmittance using Beer-Lambert law.
    
    T = 10^(-εcl) = I/I0
    
    Args:
        concentration: Concentration in M
        path_length: Path length in cm
        epsilon: Molar absorptivity in M-1·cm-1
    
    Returns:
        Transmittance (0 to 1)
    
    Example:
        >>> beer_lambert_transmittance(0.001, 1, 1000)
        0.1  # 10% transmittance
    """
    A = beer_lambert_absorbance(concentration, path_length, epsilon)
    return 10**(-A)


def concentration_from_absorbance(absorbance: float, path_length: float, 
                                   epsilon: float) -> float:
    """
    Calculate concentration from absorbance.
    
    c = A/(ε·l)
    
    Args:
        absorbance: Measured absorbance
        path_length: Path length in cm
        epsilon: Molar absorptivity in M-1·cm-1
    
    Returns:
        Concentration in M
    
    Example:
        >>> concentration_from_absorbance(1.0, 1, 1000)
        0.001  # 1 mM
    """
    if epsilon * path_length == 0:
        raise ValueError("Epsilon and path length must be non-zero")
    return absorbance / (epsilon * path_length)


def epsilon_from_absorbance(absorbance: float, concentration: float, 
                             path_length: float) -> float:
    """
    Calculate molar absorptivity from absorbance.
    
    ε = A/(c·l)
    
    Args:
        absorbance: Measured absorbance
        concentration: Concentration in M
        path_length: Path length in cm
    
    Returns:
        Molar absorptivity in M-1·cm-1
    """
    if concentration * path_length == 0:
        raise ValueError("Concentration and path length must be non-zero")
    return absorbance / (concentration * path_length)


def absorbance_from_transmittance(transmittance: float) -> float:
    """
    Convert transmittance to absorbance.
    
    A = -log10(T)
    
    Args:
        transmittance: Transmittance (0 to 1)
    
    Returns:
        Absorbance
    """
    if transmittance <= 0:
        raise ValueError("Transmittance must be positive")
    return -np.log10(transmittance)


def transmittance_from_absorbance(absorbance: float) -> float:
    """
    Convert absorbance to transmittance.
    
    T = 10^(-A)
    
    Args:
        absorbance: Absorbance value
    
    Returns:
        Transmittance (0 to 1)
    """
    return 10**(-absorbance)


# =============================================================================
# LASER PHYSICS
# =============================================================================

def population_inversion_ratio(T: float, delta_E: float) -> float:
    """
    Calculate thermal population ratio between two levels.
    
    N_upper/N_lower = (g_u/g_l) exp(-DeltaE/kT)
    
    For laser operation, need N_upper > N_lower (population inversion).
    
    Args:
        T: Temperature in K
        delta_E: Energy difference in J
    
    Returns:
        Population ratio (Boltzmann factor)
    
    Note:
        At thermal equilibrium, ratio < 1 (no inversion possible)
    """
    return np.exp(-delta_E / (BOLTZMANN * T))


def small_signal_gain_cross_section(A_value: float, wavelength_m: float, 
                                     lineshape_width_Hz: float) -> float:
    """
    Calculate stimulated emission cross-section.
    
    σ = (lambda2·A)/(8pi·Deltaν)
    
    Args:
        A_value: Einstein A coefficient in s-1
        wavelength_m: Transition wavelength in m
        lineshape_width_Hz: Linewidth (FWHM) in Hz
    
    Returns:
        Stimulated emission cross-section in m2
    
    Example:
        >>> small_signal_gain_cross_section(1e8, 633e-9, 1e9)  # HeNe laser
        3e-17  # m2
    """
    return (wavelength_m**2 * A_value) / (8 * np.pi * lineshape_width_Hz)


def laser_gain_coefficient(sigma: float, delta_N: float) -> float:
    """
    Calculate laser gain coefficient.
    
    g = σ x (N_upper - N_lower)
    
    For gain > 0, need N_upper > N_lower (population inversion).
    
    Args:
        sigma: Stimulated emission cross-section in m2
        delta_N: Population inversion density (N_upper - N_lower) in m-3
    
    Returns:
        Gain coefficient in m-1
    
    Example:
        >>> laser_gain_coefficient(3e-17, 1e18)  # Typical HeNe
        0.03  # 3% gain per meter
    """
    return sigma * delta_N


def laser_threshold_gain(gain_coefficient: float, mirror_R1: float, 
                         mirror_R2: float, length: float, 
                         loss_per_pass: float = 0) -> float:
    """
    Check if gain exceeds threshold.
    
    Threshold condition: g·L > (1/2) ln(1/(R1·R2)) + loss
    
    Args:
        gain_coefficient: Small signal gain in m-1
        mirror_R1, mirror_R2: Mirror reflectivities (0 to 1)
        length: Cavity length in m
        loss_per_pass: Additional losses per pass
    
    Returns:
        Net gain (positive means above threshold)
    """
    threshold_gain = (0.5 / length) * np.log(1 / (mirror_R1 * mirror_R2)) + \
                     loss_per_pass / length
    return gain_coefficient - threshold_gain


def cavity_mode_spacing(cavity_length: float) -> float:
    """
    Calculate longitudinal mode spacing (free spectral range).
    
    Deltaν = c/(2L)
    
    Args:
        cavity_length: Cavity length in m
    
    Returns:
        Mode spacing in Hz
    
    Example:
        >>> cavity_mode_spacing(0.3)  # 30 cm cavity
        5e8  # 500 MHz
    """
    return SPEED_OF_LIGHT / (2 * cavity_length)


def cavity_finesse(R: float) -> float:
    """
    Calculate cavity finesse.
    
    F = pi√R / (1-R)
    
    Args:
        R: Mirror reflectivity (for symmetric cavity)
    
    Returns:
        Finesse (dimensionless)
    
    Example:
        >>> cavity_finesse(0.99)
        313  # High finesse
    """
    if R >= 1:
        raise ValueError("Reflectivity must be < 1")
    return np.pi * np.sqrt(R) / (1 - R)


def coherence_length(wavelength: float, linewidth: float) -> float:
    """
    Calculate coherence length.
    
    L_coh = c/Deltaν = lambda2/Deltalambda
    
    Args:
        wavelength: Wavelength in m
        linewidth: Linewidth in Hz
    
    Returns:
        Coherence length in m
    
    Example:
        >>> coherence_length(633e-9, 1e9)  # 1 GHz linewidth
        0.3  # 30 cm
    """
    return SPEED_OF_LIGHT / linewidth


# =============================================================================
# PHOTOCHEMISTRY
# =============================================================================

def photon_energy(wavelength_nm: float) -> float:
    """
    Calculate energy of a single photon.
    
    E = hc/lambda
    
    Args:
        wavelength_nm: Wavelength in nm
    
    Returns:
        Energy in J
    
    Example:
        >>> photon_energy(500)  # Green light
        3.97e-19  # J
    """
    wavelength_m = wavelength_nm * 1e-9
    return PLANCK_CONSTANT * SPEED_OF_LIGHT / wavelength_m


def photon_energy_eV(wavelength_nm: float) -> float:
    """
    Calculate photon energy in eV.
    
    Args:
        wavelength_nm: Wavelength in nm
    
    Returns:
        Energy in eV
    
    Example:
        >>> photon_energy_eV(500)
        2.48  # eV
    """
    return photon_energy(wavelength_nm) / 1.60217663e-19


def photon_flux_moles(power_W: float, wavelength_nm: float) -> float:
    """
    Calculate photon flux in moles per second (einstein).
    
    One einstein = 1 mole of photons
    
    Args:
        power_W: Light power in watts (J/s)
        wavelength_nm: Wavelength in nm
    
    Returns:
        Photon flux in einstein/s (mol photons/s)
    
    Example:
        >>> photon_flux_moles(1, 500)  # 1 W of green light
        4.2e-6  # 4.2 µeinstein/s
    """
    E_photon = photon_energy(wavelength_nm)
    photons_per_second = power_W / E_photon
    return photons_per_second / 6.02214076e23  # Convert to moles


def quantum_yield(reactant_consumed: float, photons_absorbed: float) -> float:
    """
    Calculate quantum yield.
    
    Φ = (moles reactant consumed) / (moles photons absorbed)
    
    Args:
        reactant_consumed: Moles of reactant consumed
        photons_absorbed: Moles (einstein) of photons absorbed
    
    Returns:
        Quantum yield (dimensionless)
    
    Note:
        - Φ = 1: One molecule per photon
        - Φ > 1: Chain reaction
        - Φ < 1: Competing processes
    
    Example:
        >>> quantum_yield(0.001, 0.002)
        0.5
    """
    if photons_absorbed <= 0:
        raise ValueError("Photons absorbed must be positive")
    return reactant_consumed / photons_absorbed


def photochemical_rate(k: float, I_absorbed: float, 
                        quantum_yield: float) -> float:
    """
    Calculate photochemical reaction rate.
    
    rate = k x I_absorbed x Φ
    
    For simple case: rate = Φ x I_absorbed
    
    Args:
        k: Rate constant (may absorb other factors)
        I_absorbed: Absorbed light intensity (einstein/s or photons/s)
        quantum_yield: Quantum yield Φ
    
    Returns:
        Reaction rate (same units as I_absorbed x concentration)
    """
    return k * I_absorbed * quantum_yield


def excited_state_concentration(I_absorbed: float, tau: float) -> float:
    """
    Calculate steady-state concentration of excited molecules.
    
    [M*] = I_absorbed x τ
    
    Args:
        I_absorbed: Rate of photon absorption (molecules/s)
        tau: Excited state lifetime in s
    
    Returns:
        Concentration of excited state (number or moles, same as I)
    """
    return I_absorbed * tau


def fluorescence_lifetime(natural_lifetime: float, 
                          quenching_rate: float) -> float:
    """
    Calculate observed fluorescence lifetime with quenching.
    
    1/τ_obs = 1/τ_0 + k_q[Q]
    
    Args:
        natural_lifetime: Natural radiative lifetime in s
        quenching_rate: k_q x [Q] (quenching rate constant x quencher concentration)
    
    Returns:
        Observed lifetime in s
    
    Example:
        >>> fluorescence_lifetime(1e-8, 1e8)
        5e-9  # Lifetime halved by quenching
    """
    return 1 / (1/natural_lifetime + quenching_rate)


def stern_volmer_quenching(tau_0: float, tau: float, 
                            quencher_concentration: float) -> float:
    """
    Calculate quenching rate constant from Stern-Volmer analysis.
    
    τ_0/τ = 1 + k_q[Q]
    
    Args:
        tau_0: Unquenched lifetime in s
        tau: Quenched lifetime in s
        quencher_concentration: Quencher concentration in M
    
    Returns:
        k_q (quenching rate constant) in M-1·s-1
    
    Example:
        >>> stern_volmer_quenching(1e-8, 5e-9, 0.01)
        1e10  # Diffusion-controlled quenching
    """
    return (tau_0 / tau - 1) / quencher_concentration


def energy_transfer_distance(k_ET: float, tau_0: float) -> float:
    """
    Calculate Förster distance for energy transfer.
    
    R_0 = (k_ET x τ_0)^(1/6) x R  (if k_ET in terms of R)
    
    Simplified: Given k_ET and τ_0, returns relative distance.
    
    Args:
        k_ET: Energy transfer rate in s-1
        tau_0: Donor lifetime in s
    
    Returns:
        Relative distance (normalized to Förster distance)
    """
    # At R_0, k_ET = 1/τ_0, so efficiency = 50%
    return (k_ET * tau_0)**(1/6)


def energy_transfer_efficiency(k_ET: float, tau_0: float) -> float:
    """
    Calculate energy transfer efficiency.
    
    E = k_ET / (k_ET + 1/τ_0)
    
    Args:
        k_ET: Energy transfer rate in s-1
        tau_0: Donor natural lifetime in s
    
    Returns:
        Transfer efficiency (0 to 1)
    
    Example:
        >>> energy_transfer_efficiency(1e8, 1e-8)
        0.5  # 50% efficiency
    """
    return k_ET / (k_ET + 1/tau_0)


# =============================================================================
# PHOTOLYSIS CALCULATIONS
# =============================================================================

def photolysis_rate_constant(I_0: float, epsilon: float, 
                              path_length: float, 
                              quantum_yield: float) -> float:
    """
    Calculate first-order photolysis rate constant.
    
    k = (I_0 x ε x l x Φ) / N_A
    
    For low absorbance (Beer-Lambert regime).
    
    Args:
        I_0: Incident light intensity (einstein/(L·s) or photons/(L·s))
        epsilon: Molar absorptivity in M-1·cm-1
        path_length: Path length in cm
        quantum_yield: Quantum yield for photolysis
    
    Returns:
        First-order rate constant in s-1
    
    Example:
        >>> photolysis_rate_constant(1e-6, 1000, 1, 0.1)
        1e-4  # Slow photolysis
    """
    # Convert to proper units
    # I_0 in einstein/(L·s) = mol photons/(L·s)
    # epsilon x l x c gives absorbance
    # Rate = Φ x I_absorbed = Φ x I_0 x (1 - 10^(-εlc))
    
    # For low absorbance: 1 - 10^(-εlc) ~ εlc x ln(10)/ln(10) ~ εlc x 2.303
    
    # Simplified: k ~ Φ x I_0 x ε x l x 2.303 (for dilute solutions)
    return 2.303 * quantum_yield * I_0 * epsilon * path_length


def half_life_from_rate_constant(k: float) -> float:
    """
    Calculate half-life from first-order rate constant.
    
    t_½ = ln(2)/k
    
    Args:
        k: First-order rate constant in s-1
    
    Returns:
        Half-life in s
    """
    if k <= 0:
        raise ValueError("Rate constant must be positive")
    return np.log(2) / k


# =============================================================================
# LASER TYPES DATABASE
# =============================================================================

LASER_DATABASE = {
    'HeNe': {
        'wavelength_nm': 632.8,
        'type': 'gas',
        'gain_medium': 'Helium-Neon mixture',
        'typical_power_mW': 0.5,
        'typical_power_W': 0.001,
        'linewidth_MHz': 1500,
        'A_coefficient': 6.56e6,  # s-1
    },
    'Nd:YAG': {
        'wavelength_nm': 1064,
        'type': 'solid-state',
        'gain_medium': 'Nd3+:YAG crystal',
        'typical_power_W': 10,
        'linewidth_MHz': 100,
        'A_coefficient': 6.7e3,
    },
    'CO2': {
        'wavelength_nm': 10600,  # 10.6 mum
        'type': 'gas',
        'gain_medium': 'CO2 gas',
        'typical_power_W': 100,
        'linewidth_MHz': 50,
    },
    'Ar+': {
        'wavelength_nm': [488, 514.5],  # Multiple lines
        'type': 'gas',
        'gain_medium': 'Argon ion plasma',
        'typical_power_W': 5,
        'linewidth_MHz': 5000,
    },
    'Ti:Sapphire': {
        'wavelength_nm': 800,  # Tunable 700-1000 nm
        'type': 'solid-state',
        'gain_medium': 'Ti3+:Al2O3',
        'typical_power_W': 2,
        'linewidth_MHz': 100000,  # Broad
        'tunable': True,
    },
    'Ruby': {
        'wavelength_nm': 694.3,
        'type': 'solid-state',
        'gain_medium': 'Cr3+:Al2O3',
        'typical_power_W': 0.1,  # Pulsed
        'linewidth_MHz': 330,
    },
    'Excimer': {
        'wavelength_nm': 193,  # ArF, also 248 KrF, 308 XeCl
        'type': 'gas',
        'gain_medium': 'ArF excimer',
        'typical_power_W': 10,  # Pulsed
        'linewidth_MHz': 10000,
    },
    'Diode': {
        'wavelength_nm': 780,  # Variable
        'type': 'semiconductor',
        'gain_medium': 'p-n junction',
        'typical_power_W': 0.005,
        'linewidth_MHz': 100,
        'tunable': True,
    }
}


def get_laser_info(laser_type: str) -> Dict:
    """
    Get information about a laser type.
    
    Args:
        laser_type: Laser name (e.g., 'HeNe', 'Nd:YAG', 'CO2')
    
    Returns:
        Dictionary with laser properties
    """
    laser_type = laser_type.replace(' ', '').replace('-', '')
    
    for key in LASER_DATABASE:
        if key.lower() == laser_type.lower():
            return LASER_DATABASE[key]
    
    raise ValueError(f"Unknown laser: {laser_type}. "
                    f"Available: {list(LASER_DATABASE.keys())}")


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Laser and Photochemistry Tools - Examples")
    print("=" * 60)
    
    # Einstein coefficients
    print("\n1. Einstein Coefficients:")
    A = 1e8  # Typical allowed transition
    B = einstein_B_from_A(A, 5e14)
    print(f"   A = {A:.1e} s-1 -> B = {B:.3e}")
    print(f"   Natural linewidth: {natural_linewidth(A)/1e6:.1f} MHz")
    print(f"   Radiative lifetime: {spontaneous_emission_lifetime(A)*1e9:.1f} ns")
    
    # Beer-Lambert
    print("\n2. Beer-Lambert Law:")
    A = beer_lambert_absorbance(0.001, 1, 1000)
    T = beer_lambert_transmittance(0.001, 1, 1000)
    print(f"   c = 1 mM, ε = 1000 M-1·cm-1, l = 1 cm")
    print(f"   Absorbance: {A:.2f}")
    print(f"   Transmittance: {T:.3f} ({T*100:.1f}%)")
    
    # Laser physics
    print("\n3. Laser Physics:")
    spacing = cavity_mode_spacing(0.3)
    print(f"   30 cm cavity mode spacing: {spacing/1e6:.0f} MHz")
    
    L_coh = coherence_length(633e-9, 1e9)
    print(f"   HeNe coherence length (1 GHz): {L_coh*100:.1f} cm")
    
    # Photochemistry
    print("\n4. Photochemistry:")
    E = photon_energy_eV(500)
    print(f"   500 nm photon energy: {E:.2f} eV")
    
    flux = photon_flux_moles(1, 500)
    print(f"   1 W of 500 nm: {flux*1e6:.2f} µeinstein/s")
    
    Phi = quantum_yield(0.001, 0.002)
    print(f"   Quantum yield (0.001 mol from 0.002 einstein): {Phi:.2f}")
    
    # Fluorescence
    print("\n5. Fluorescence Quenching:")
    tau = fluorescence_lifetime(1e-8, 1e8)
    print(f"   τ0 = 10 ns, k_q[Q] = 108 s-1 -> τ = {tau*1e9:.1f} ns")
    
    k_q = stern_volmer_quenching(1e-8, 5e-9, 0.01)
    print(f"   Stern-Volmer k_q: {k_q:.1e} M-1·s-1")
    
    # Laser database
    print("\n6. Laser Database:")
    hene = get_laser_info('HeNe')
    print(f"   HeNe wavelength: {hene['wavelength_nm']} nm")
    print(f"   HeNe power: {hene['typical_power_mW']} mW")
    
    print("\n" + "=" * 60)
    print("All examples completed!")

MCP_TOOLS = [
    {
        "name": "absorbance_from_transmittance",
        "description": "Convert transmittance to absorbance.",
        "parameters": [
            {
                "name": "transmittance",
                "type": "number"
            }
        ]
    },
    {
        "name": "beer_lambert_absorbance",
        "description": "Calculate absorbance using Beer-Lambert law.",
        "parameters": [
            {
                "name": "concentration",
                "type": "number"
            },
            {
                "name": "path_length",
                "type": "number"
            },
            {
                "name": "epsilon",
                "type": "number"
            }
        ]
    },
    {
        "name": "beer_lambert_transmittance",
        "description": "Calculate transmittance using Beer-Lambert law.",
        "parameters": [
            {
                "name": "concentration",
                "type": "number"
            },
            {
                "name": "path_length",
                "type": "number"
            },
            {
                "name": "epsilon",
                "type": "number"
            }
        ]
    },
    {
        "name": "cavity_finesse",
        "description": "Calculate cavity finesse.",
        "parameters": [
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "cavity_mode_spacing",
        "description": "Calculate longitudinal mode spacing (free spectral range).",
        "parameters": [
            {
                "name": "cavity_length",
                "type": "number"
            }
        ]
    },
    {
        "name": "coherence_length",
        "description": "Calculate coherence length.",
        "parameters": [
            {
                "name": "wavelength",
                "type": "number"
            },
            {
                "name": "linewidth",
                "type": "number"
            }
        ]
    },
    {
        "name": "concentration_from_absorbance",
        "description": "Calculate concentration from absorbance.",
        "parameters": [
            {
                "name": "absorbance",
                "type": "number"
            },
            {
                "name": "path_length",
                "type": "number"
            },
            {
                "name": "epsilon",
                "type": "number"
            }
        ]
    },
    {
        "name": "doppler_linewidth",
        "description": "Calculate Doppler broadening linewidth (FWHM).",
        "parameters": [
            {
                "name": "frequency_Hz",
                "type": "number"
            },
            {
                "name": "temperature",
                "type": "number"
            },
            {
                "name": "mass_amu",
                "type": "number"
            }
        ]
    },
    {
        "name": "einstein_A_from_B",
        "description": "Calculate Einstein A coefficient from B coefficient.",
        "parameters": [
            {
                "name": "B_value",
                "type": "number"
            },
            {
                "name": "frequency_Hz",
                "type": "number"
            }
        ]
    },
    {
        "name": "einstein_B_absorption_from_B_emission",
        "description": "Calculate Einstein B coefficient for absorption from emission coefficient.",
        "parameters": [
            {
                "name": "B_emission",
                "type": "number"
            },
            {
                "name": "g_upper",
                "type": "number"
            },
            {
                "name": "g_lower",
                "type": "number"
            }
        ]
    },
    {
        "name": "einstein_B_from_A",
        "description": "Calculate Einstein B coefficient from A coefficient.",
        "parameters": [
            {
                "name": "A_value",
                "type": "number"
            },
            {
                "name": "frequency_Hz",
                "type": "number"
            }
        ]
    },
    {
        "name": "energy_transfer_distance",
        "description": "Calculate Förster distance for energy transfer.",
        "parameters": [
            {
                "name": "k_ET",
                "type": "number"
            },
            {
                "name": "tau_0",
                "type": "number"
            }
        ]
    },
    {
        "name": "energy_transfer_efficiency",
        "description": "Calculate energy transfer efficiency.",
        "parameters": [
            {
                "name": "k_ET",
                "type": "number"
            },
            {
                "name": "tau_0",
                "type": "number"
            }
        ]
    },
    {
        "name": "epsilon_from_absorbance",
        "description": "Calculate molar absorptivity from absorbance.",
        "parameters": [
            {
                "name": "absorbance",
                "type": "number"
            },
            {
                "name": "concentration",
                "type": "number"
            },
            {
                "name": "path_length",
                "type": "number"
            }
        ]
    },
    {
        "name": "excited_state_concentration",
        "description": "Calculate steady-state concentration of excited molecules.",
        "parameters": [
            {
                "name": "I_absorbed",
                "type": "number"
            },
            {
                "name": "tau",
                "type": "number"
            }
        ]
    },
    {
        "name": "fluorescence_lifetime",
        "description": "Calculate observed fluorescence lifetime with quenching.",
        "parameters": [
            {
                "name": "natural_lifetime",
                "type": "number"
            },
            {
                "name": "quenching_rate",
                "type": "number"
            }
        ]
    },
    {
        "name": "get_laser_info",
        "description": "Get information about a laser type.",
        "parameters": [
            {
                "name": "laser_type",
                "type": "number"
            }
        ]
    },
    {
        "name": "half_life_from_rate_constant",
        "description": "Calculate half-life from first-order rate constant.",
        "parameters": [
            {
                "name": "k",
                "type": "number"
            }
        ]
    },
    {
        "name": "laser_gain_coefficient",
        "description": "Calculate laser gain coefficient.",
        "parameters": [
            {
                "name": "sigma",
                "type": "number"
            },
            {
                "name": "delta_N",
                "type": "number"
            }
        ]
    },
    {
        "name": "laser_threshold_gain",
        "description": "Check if gain exceeds threshold.",
        "parameters": [
            {
                "name": "gain_coefficient",
                "type": "number"
            },
            {
                "name": "mirror_R1",
                "type": "number"
            },
            {
                "name": "mirror_R2",
                "type": "number"
            },
            {
                "name": "length",
                "type": "number"
            },
            {
                "name": "loss_per_pass",
                "type": "number"
            }
        ]
    },
    {
        "name": "natural_linewidth",
        "description": "Calculate natural linewidth (FWHM) from Einstein A.",
        "parameters": [
            {
                "name": "A_value",
                "type": "number"
            }
        ]
    },
    {
        "name": "photochemical_rate",
        "description": "Calculate photochemical reaction rate.",
        "parameters": [
            {
                "name": "k",
                "type": "number"
            },
            {
                "name": "I_absorbed",
                "type": "number"
            },
            {
                "name": "quantum_yield",
                "type": "number"
            }
        ]
    },
    {
        "name": "photolysis_rate_constant",
        "description": "Calculate first-order photolysis rate constant.",
        "parameters": [
            {
                "name": "I_0",
                "type": "number"
            },
            {
                "name": "epsilon",
                "type": "number"
            },
            {
                "name": "path_length",
                "type": "number"
            },
            {
                "name": "quantum_yield",
                "type": "number"
            }
        ]
    },
    {
        "name": "photon_energy",
        "description": "Calculate energy of a single photon.",
        "parameters": [
            {
                "name": "wavelength_nm",
                "type": "number"
            }
        ]
    },
    {
        "name": "photon_energy_eV",
        "description": "Calculate photon energy in eV.",
        "parameters": [
            {
                "name": "wavelength_nm",
                "type": "number"
            }
        ]
    },
    {
        "name": "photon_flux_moles",
        "description": "Calculate photon flux in moles per second (einstein).",
        "parameters": [
            {
                "name": "power_W",
                "type": "number"
            },
            {
                "name": "wavelength_nm",
                "type": "number"
            }
        ]
    },
    {
        "name": "population_inversion_ratio",
        "description": "Calculate thermal population ratio between two levels.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "delta_E",
                "type": "number"
            }
        ]
    },
    {
        "name": "quantum_yield",
        "description": "Calculate quantum yield.",
        "parameters": [
            {
                "name": "reactant_consumed",
                "type": "number"
            },
            {
                "name": "photons_absorbed",
                "type": "number"
            }
        ]
    },
    {
        "name": "small_signal_gain_cross_section",
        "description": "Calculate stimulated emission cross-section.",
        "parameters": [
            {
                "name": "A_value",
                "type": "number"
            },
            {
                "name": "wavelength_m",
                "type": "number"
            },
            {
                "name": "lineshape_width_Hz",
                "type": "number"
            }
        ]
    },
    {
        "name": "spontaneous_emission_lifetime",
        "description": "Calculate radiative lifetime from Einstein A coefficient.",
        "parameters": [
            {
                "name": "A_value",
                "type": "number"
            }
        ]
    },
    {
        "name": "stern_volmer_quenching",
        "description": "Calculate quenching rate constant from Stern-Volmer analysis.",
        "parameters": [
            {
                "name": "tau_0",
                "type": "number"
            },
            {
                "name": "tau",
                "type": "number"
            },
            {
                "name": "quencher_concentration",
                "type": "number"
            }
        ]
    },
    {
        "name": "transmittance_from_absorbance",
        "description": "Convert absorbance to transmittance.",
        "parameters": [
            {
                "name": "absorbance",
                "type": "number"
            }
        ]
    }
]
