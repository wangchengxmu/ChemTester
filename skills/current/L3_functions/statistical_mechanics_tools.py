"""
Statistical Mechanics Tools - L3 Implementation

Provides functions for calculating partition functions and thermodynamic
properties from molecular parameters.

Physical Constants:
    k_B = 1.380649e-23 J/K (Boltzmann constant)
    h = 6.62607e-34 J·s (Planck constant)
    hbar = 1.05457e-34 J·s (reduced Planck)
    c = 2.998e10 cm/s (speed of light)
    N_A = 6.022e23 mol-1 (Avogadro's number)

Dependencies:
    - numpy (for array operations)
    - scipy.constants (for physical constants)

Related L2: ../L2_principles/statistical_mechanics.md
Related L4: ../L4_reference/statistical_mechanics_data.md

## Solver Instructions (for AI Agent)

When you encounter statistical mechanics problems (partition functions, Boltzmann distributions, thermodynamic properties from molecular data), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Boltzmann factor**: Given energy level and temperature -> find relative population
- **Partition function**: Given energy levels and T -> calculate Z (canonical ensemble)
- **Thermodynamic properties from Z**: Given Z and T -> find U, A, S, G, Cv
- **Molecular partition functions**: Given spectroscopic constants -> find q_trans, q_rot, q_vib, q_elec
- **Heat capacity**: Given temperature and molecular parameters -> find Cv contributions

### Step 2: Choose the correct function
- `boltzmann_factor(energy, temperature)` -> exp(-E/kT)
- `partition_function_canonical(energies, temperature)` -> Z = Σ exp(-Ei/kT)
- `internal_energy(energies, temperature)` -> U from partition function
- `entropy(energies, temperature)` -> S from partition function
- `heat_capacity(energies, temperature)` -> Cv = dU/dT
- `q_translational(T, mass, volume)` -> q_trans = V/lambda3 (thermal de Broglie)
- `q_rotational(T, B, sigma)` -> q_rot = T/(σθ_rot) for linear molecules
- `q_vibrational(T, nu)` -> q_vib = exp(-θ_vib/2T)/(1-exp(-θ_vib/T))
- `q_electronic(g0, E1, T)` -> q_elec = g0 + g1·exp(-E1/kT) + ...

### Step 3: Handle special cases
- Energy must be in Joules; temperature in Kelvin
- σ (symmetry number): 1 for heteronuclear diatomic (HCl), 2 for homonuclear (N2)
- At high T: q_rot ~ T/(σθ_rot); at low T: must sum explicitly
- q_vib for high frequency (θ_vib >> T) -> q_vib ~ 1 (ground state only)
- Total q = q_trans x q_rot x q_vib x q_elec (product approximation)

### Examples
1. **Boltzmann factor**: Energy level 4.0e-21 J at 300 K
   -> `boltzmann_factor(4.0e-21, 300)` -> exp(-4e-21/(1.38e-23x300)) = exp(-0.966) ~ 0.381

2. **Rotational partition function**: N2 at 300 K, B=2.0 cm-1, σ=2
   -> `q_rotational(300, 2.0, 2)` -> T/(σθ_rot) = 300/(2x2.88) ~ 52.1

3. **Total partition function**: N2 at 300 K
   -> q_trans ~ 1030, q_rot ~ 52, q_vib ~ 1.00003 (ν=2359 cm-1), q_elec ~ 1
   -> q_total ~ 5.2x1030 (dominated by translation)
"""

import numpy as np
from scipy import constants

# Physical constants
k_B = constants.Boltzmann  # J/K
h = constants.Planck  # J·s
hbar = constants.hbar  # J·s
c = constants.c * 100  # cm/s (convert from m/s)
N_A = constants.Avogadro  # mol-1
R = constants.R  # J/(mol·K)


# =============================================================================
# Core Functions
# =============================================================================

def boltzmann_factor(energy: float, temperature: float) -> float:
    """
    Calculate the Boltzmann factor exp(-E/kT).

    Parameters
    ----------
    energy : float
        Energy in Joules
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Boltzmann factor exp(-E/(k_B * T))

    Examples
    --------
    >>> boltzmann_factor(1e-20, 300)  # Energy level at 300 K
    0.0889...
    >>> boltzmann_factor(0, 300)  # Ground state
    1.0
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    beta = 1 / (k_B * temperature)
    return np.exp(-beta * energy)


def partition_function_canonical(energies: np.ndarray, temperature: float) -> float:
    """
    Calculate the canonical partition function Z = Σ exp(-E_i/kT).

    Parameters
    ----------
    energies : array-like
        Array of energy levels in Joules
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Partition function Z

    Examples
    --------
    >>> partition_function_canonical([0, 1e-20, 2e-20], 300)
    1.097...
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    energies = np.asarray(energies)
    beta = 1 / (k_B * temperature)
    return np.sum(np.exp(-beta * energies))


def boltzmann_probability(energy: float, partition_function: float,
                          temperature: float) -> float:
    """
    Calculate the probability of occupying a state with given energy.

    P_i = exp(-E_i/kT) / Z

    Parameters
    ----------
    energy : float
        Energy of the state in Joules
    partition_function : float
        Partition function Z
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Occupation probability (0 to 1)

    Examples
    --------
    >>> Z = partition_function_canonical([0, 1e-20], 300)
    >>> boltzmann_probability(0, Z, 300)
    0.917...
    """
    if partition_function <= 0:
        raise ValueError("Partition function must be positive")
    return boltzmann_factor(energy, temperature) / partition_function


# =============================================================================
# Translational Partition Function
# =============================================================================

def de_broglie_wavelength(mass: float, temperature: float) -> float:
    """
    Calculate the thermal de Broglie wavelength.

    Λ = h / √(2pimkT)

    Parameters
    ----------
    mass : float
        Molecular mass in kg
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        de Broglie wavelength in meters

    Examples
    --------
    >>> de_broglie_wavelength(3.35e-26, 300)  # O2 at 300 K
    2.0e-11...
    """
    if mass <= 0 or temperature <= 0:
        raise ValueError("Mass and temperature must be positive")
    return h / np.sqrt(2 * np.pi * mass * k_B * temperature)


def translational_partition_function(mass: float, volume: float,
                                     temperature: float) -> float:
    """
    Calculate the translational partition function.

    q_trans = V / Λ3 = (2pimkT/h2)^(3/2) x V

    Parameters
    ----------
    mass : float
        Molecular mass in kg
    volume : float
        Volume in m3
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Translational partition function (dimensionless)

    Examples
    --------
    >>> translational_partition_function(3.35e-26, 1e-3, 300)  # O2, 1L, 300K
    1.2e+30...
    """
    if mass <= 0 or volume <= 0 or temperature <= 0:
        raise ValueError("Mass, volume, and temperature must be positive")

    Lambda = de_broglie_wavelength(mass, temperature)
    return volume / Lambda**3


# =============================================================================
# Rotational Partition Function
# =============================================================================

def rotational_temperature(moment_of_inertia: float) -> float:
    """
    Calculate the rotational temperature Θ_rot.

    Θ_rot = ℏ2 / (2Ik)

    Parameters
    ----------
    moment_of_inertia : float
        Moment of inertia in kg·m2

    Returns
    -------
    float
        Rotational temperature in Kelvin

    Examples
    --------
    >>> rotational_temperature(1.94e-46)  # N2
    2.88...
    """
    if moment_of_inertia <= 0:
        raise ValueError("Moment of inertia must be positive")
    return hbar**2 / (2 * moment_of_inertia * k_B)


def rotational_partition_function(moment_of_inertia: float, temperature: float,
                                  sigma: int = 1) -> float:
    """
    Calculate the rotational partition function for a diatomic molecule.

    q_rot = T / (Θ_rot x σ)

    Parameters
    ----------
    moment_of_inertia : float
        Moment of inertia in kg·m2
    temperature : float
        Temperature in Kelvin
    sigma : int, optional
        Symmetry number (1 for heteronuclear, 2 for homonuclear), default 1

    Returns
    -------
    float
        Rotational partition function (dimensionless)

    Examples
    --------
    >>> rotational_partition_function(1.94e-46, 300, sigma=2)  # N2 at 300K
    52.0...
    """
    if moment_of_inertia <= 0 or temperature <= 0:
        raise ValueError("Moment of inertia and temperature must be positive")
    if sigma < 1:
        raise ValueError("Symmetry number must be >= 1")

    theta_rot = rotational_temperature(moment_of_inertia)
    return temperature / (theta_rot * sigma)


def rotational_partition_function_from_B(B_cm: float, temperature: float,
                                         sigma: int = 1) -> float:
    """
    Calculate rotational partition function from rotational constant B.

    q_rot = kT / (B̃ x σ)

    Parameters
    ----------
    B_cm : float
        Rotational constant in cm-1
    temperature : float
        Temperature in Kelvin
    sigma : int, optional
        Symmetry number, default 1

    Returns
    -------
    float
        Rotational partition function

    Examples
    --------
    >>> rotational_partition_function_from_B(2.0, 300, sigma=2)  # N2
    52.4...
    """
    if B_cm <= 0 or temperature <= 0:
        raise ValueError("Rotational constant and temperature must be positive")

    # Convert B from cm-1 to energy: E = hc x B_cm
    B_energy = h * c * B_cm  # J
    return k_B * temperature / (B_energy * sigma)


# =============================================================================
# Vibrational Partition Function
# =============================================================================

def vibrational_temperature(frequency_Hz: float) -> float:
    """
    Calculate the vibrational temperature Θ_vib.

    Θ_vib = hν / k

    Parameters
    ----------
    frequency_Hz : float
        Vibrational frequency in Hz

    Returns
    -------
    float
        Vibrational temperature in Kelvin

    Examples
    --------
    >>> vibrational_temperature(7.07e13)  # N2 (2358 cm-1)
    3393...
    """
    if frequency_Hz <= 0:
        raise ValueError("Frequency must be positive")
    return h * frequency_Hz / k_B


def vibrational_temperature_from_wavenumber(wavenumber_cm: float) -> float:
    """
    Calculate vibrational temperature from wavenumber.

    Θ_vib = hcν̃ / k

    Parameters
    ----------
    wavenumber_cm : float
        Wavenumber in cm-1

    Returns
    -------
    float
        Vibrational temperature in Kelvin

    Examples
    --------
    >>> vibrational_temperature_from_wavenumber(2358)  # N2
    3393...
    """
    if wavenumber_cm <= 0:
        raise ValueError("Wavenumber must be positive")
    frequency = wavenumber_cm * c  # Hz
    return vibrational_temperature(frequency)


def vibrational_partition_function(frequency_Hz: float, temperature: float,
                                   include_zpe: bool = False) -> float:
    """
    Calculate the vibrational partition function.

    q_vib = 1 / (1 - exp(-hν/kT))  [ground state as zero]
    q_vib = exp(-hν/2kT) / (1 - exp(-hν/kT))  [including ZPE]

    Parameters
    ----------
    frequency_Hz : float
        Vibrational frequency in Hz
    temperature : float
        Temperature in Kelvin
    include_zpe : bool, optional
        Include zero-point energy contribution, default False

    Returns
    -------
    float
        Vibrational partition function (dimensionless)

    Examples
    --------
    >>> vibrational_partition_function(7.07e13, 300)  # N2 at 300K
    1.00...
    >>> vibrational_partition_function(6.42e12, 300)  # I2 at 300K
    1.56...
    """
    if frequency_Hz <= 0 or temperature <= 0:
        raise ValueError("Frequency and temperature must be positive")

    theta_vib = vibrational_temperature(frequency_Hz)
    x = theta_vib / temperature

    if include_zpe:
        return np.exp(-x/2) / (1 - np.exp(-x))
    else:
        return 1 / (1 - np.exp(-x))


def vibrational_partition_function_from_wavenumber(
    wavenumber_cm: float, temperature: float, include_zpe: bool = False
) -> float:
    """
    Calculate vibrational partition function from wavenumber.

    Parameters
    ----------
    wavenumber_cm : float
        Wavenumber in cm-1
    temperature : float
        Temperature in Kelvin
    include_zpe : bool, optional
        Include zero-point energy, default False

    Returns
    -------
    float
        Vibrational partition function
    """
    if wavenumber_cm <= 0 or temperature <= 0:
        raise ValueError("Wavenumber and temperature must be positive")

    frequency = wavenumber_cm * c  # Hz
    return vibrational_partition_function(frequency, temperature, include_zpe)


# =============================================================================
# Thermodynamic Properties from Partition Function
# =============================================================================

def internal_energy_from_Z(partition_function: float,
                           dlnZ_dT: float, temperature: float) -> float:
    """
    Calculate internal energy from partition function.

    U = kT2 (∂ln Z/∂T)_V

    Parameters
    ----------
    partition_function : float
        Partition function Z
    dlnZ_dT : float
        Derivative of ln(Z) with respect to T
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Internal energy in Joules

    Notes
    -----
    This requires knowing d(ln Z)/dT, which depends on the specific system.
    """
    if partition_function <= 0 or temperature <= 0:
        raise ValueError("Partition function and temperature must be positive")
    return k_B * temperature**2 * dlnZ_dT


def internal_energy_translational(temperature: float) -> float:
    """
    Calculate translational contribution to internal energy.

    U_trans = 3/2 x kT (per molecule)

    Parameters
    ----------
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Translational internal energy in Joules (per molecule)

    Examples
    --------
    >>> internal_energy_translational(300)
    6.21e-21...
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    return 1.5 * k_B * temperature


def internal_energy_rotational(temperature: float, linear: bool = True) -> float:
    """
    Calculate rotational contribution to internal energy.

    U_rot = kT (linear, 2 DOF)
    U_rot = 3/2 x kT (nonlinear, 3 DOF)

    Parameters
    ----------
    temperature : float
        Temperature in Kelvin
    linear : bool, optional
        True for linear molecule, False for nonlinear, default True

    Returns
    -------
    float
        Rotational internal energy in Joules (per molecule)

    Examples
    --------
    >>> internal_energy_rotational(300)  # linear
    4.14e-21...
    >>> internal_energy_rotational(300, linear=False)  # nonlinear
    6.21e-21...
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    if linear:
        return k_B * temperature  # 2 rotational DOF
    else:
        return 1.5 * k_B * temperature  # 3 rotational DOF


def internal_energy_vibrational(frequency_Hz: float,
                                temperature: float) -> float:
    """
    Calculate vibrational contribution to internal energy.

    U_vib = hν / (exp(hν/kT) - 1)  [per mode, ground state as zero]

    Parameters
    ----------
    frequency_Hz : float
        Vibrational frequency in Hz
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Vibrational internal energy in Joules (per molecule, per mode)

    Examples
    --------
    >>> internal_energy_vibrational(7.07e13, 300)  # N2 at 300K
    1.2e-21...  # very small, mostly frozen out
    """
    if frequency_Hz <= 0 or temperature <= 0:
        raise ValueError("Frequency and temperature must be positive")

    x = h * frequency_Hz / (k_B * temperature)
    return h * frequency_Hz / (np.exp(x) - 1)


def entropy_from_partition_function(partition_function: float,
                                    internal_energy: float,
                                    temperature: float,
                                    N: int = 1) -> float:
    """
    Calculate entropy from partition function.

    S = k ln(Z) + U/T  [for distinguishable]
    S = k ln(Z/N!) + U/T  [for indistinguishable]

    For indistinguishable particles, use Sackur-Tetrode.

    Parameters
    ----------
    partition_function : float
        Partition function Z
    internal_energy : float
        Internal energy U in Joules
    temperature : float
        Temperature in Kelvin
    N : int, optional
        Number of particles (for indistinguishable correction), default 1

    Returns
    -------
    float
        Entropy in J/K

    Examples
    --------
    >>> # Approximate for ideal gas (use Sackur-Tetrode for accurate values)
    """
    if partition_function <= 0 or temperature <= 0:
        raise ValueError("Partition function and temperature must be positive")

    # For distinguishable particles (or single molecule)
    return k_B * np.log(partition_function) + internal_energy / temperature


def entropy_sackur_tetrode(mass: float, volume: float,
                           temperature: float, N: int = 1) -> float:
    """
    Calculate entropy of monatomic ideal gas using Sackur-Tetrode equation.

    S/Nk = ln(V/N x (2pimkT/h2)^(3/2)) + 5/2

    Parameters
    ----------
    mass : float
        Atomic mass in kg
    volume : float
        Volume in m3
    temperature : float
        Temperature in Kelvin
    N : int, optional
        Number of atoms, default 1

    Returns
    -------
    float
        Entropy in J/K

    Examples
    --------
    >>> entropy_sackur_tetrode(6.64e-26, 1e-3, 300, N=1)  # Ar, 1L, 300K
    1.5e-22...
    """
    if mass <= 0 or volume <= 0 or temperature <= 0 or N <= 0:
        raise ValueError("All parameters must be positive")

    q = translational_partition_function(mass, volume, temperature)
    # S = k ln(q/N) + 5/2 k for indistinguishable particles
    return k_B * (np.log(q / N) + 2.5)


def helmholtz_free_energy(partition_function: float,
                          temperature: float) -> float:
    """
    Calculate Helmholtz free energy from partition function.

    A = -kT ln(Z)

    Parameters
    ----------
    partition_function : float
        Partition function Z
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Helmholtz free energy in Joules

    Examples
    --------
    >>> helmholtz_free_energy(1e30, 300)
    -1.38e-20...
    """
    if partition_function <= 0 or temperature <= 0:
        raise ValueError("Partition function and temperature must be positive")
    return -k_B * temperature * np.log(partition_function)


def gibbs_free_energy(partition_function: float, temperature: float,
                      pressure: float = 101325) -> float:
    """
    Calculate Gibbs free energy for ideal gas.

    G = A + PV = -kT ln(Z) + kT ln(q_trans)
    For ideal gas: G = -kT ln(Z/N) for N molecules

    Parameters
    ----------
    partition_function : float
        Partition function Z
    temperature : float
        Temperature in Kelvin
    pressure : float, optional
        Pressure in Pa, default 1 atm (101325 Pa)

    Returns
    -------
    float
        Gibbs free energy in Joules (per molecule)
    """
    if partition_function <= 0 or temperature <= 0 or pressure <= 0:
        raise ValueError("All parameters must be positive")

    A = helmholtz_free_energy(partition_function, temperature)
    # PV = kT for single molecule in ideal gas
    return A + k_B * temperature


# =============================================================================
# Heat Capacity Calculations
# =============================================================================

def heat_capacity_translational(molar: bool = False) -> float:
    """
    Translational contribution to heat capacity.

    C_V = 3/2 x k (per molecule)
    C_V = 3/2 x R (per mole)

    Parameters
    ----------
    molar : bool, optional
        Return molar heat capacity if True, default False

    Returns
    -------
    float
        Heat capacity in J/K (per molecule) or J/(mol·K) (per mole)

    Examples
    --------
    >>> heat_capacity_translational()
    2.07e-23...
    >>> heat_capacity_translational(molar=True)
    12.47...
    """
    if molar:
        return 1.5 * R
    else:
        return 1.5 * k_B


def heat_capacity_rotational(linear: bool = True, molar: bool = False) -> float:
    """
    Rotational contribution to heat capacity.

    C_V = k (linear, 2 DOF)
    C_V = 3/2 x k (nonlinear, 3 DOF)

    Parameters
    ----------
    linear : bool, optional
        True for linear molecule, default True
    molar : bool, optional
        Return molar heat capacity if True, default False

    Returns
    -------
    float
        Heat capacity

    Examples
    --------
    >>> heat_capacity_rotational(molar=True)  # linear
    8.314...
    """
    if molar:
        factor = R
    else:
        factor = k_B

    if linear:
        return factor  # 2 DOF x 1/2 k each
    else:
        return 1.5 * factor  # 3 DOF x 1/2 k each


def heat_capacity_vibrational(frequency_Hz: float,
                              temperature: float,
                              molar: bool = False) -> float:
    """
    Vibrational contribution to heat capacity.

    C_V = k x (Θ_vib/T)2 x exp(-Θ_vib/T) / (1 - exp(-Θ_vib/T))2

    Parameters
    ----------
    frequency_Hz : float
        Vibrational frequency in Hz
    temperature : float
        Temperature in Kelvin
    molar : bool, optional
        Return molar heat capacity if True, default False

    Returns
    -------
    float
        Heat capacity

    Examples
    --------
    >>> heat_capacity_vibrational(7.07e13, 300)  # N2 at 300K
    6.9e-25...  # nearly frozen out
    """
    if frequency_Hz <= 0 or temperature <= 0:
        raise ValueError("Frequency and temperature must be positive")

    theta_vib = vibrational_temperature(frequency_Hz)
    x = theta_vib / temperature

    # C_V = k x x2 x e^x / (e^x - 1)2
    # More numerically stable form:
    exp_x = np.exp(x)
    C_v = k_B * x**2 * exp_x / (exp_x - 1)**2

    if molar:
        return C_v * N_A
    return C_v


# =============================================================================
# Utility Functions
# =============================================================================

def reduced_mass(m1: float, m2: float) -> float:
    """
    Calculate reduced mass mu = m1 x m2 / (m1 + m2).

    Parameters
    ----------
    m1, m2 : float
        Masses in kg

    Returns
    -------
    float
        Reduced mass in kg

    Examples
    --------
    >>> reduced_mass(1.67e-27, 1.67e-27)  # H2
    8.35e-28...
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Masses must be positive")
    return m1 * m2 / (m1 + m2)


def moment_of_inertia_diatomic(m1: float, m2: float,
                               bond_length: float) -> float:
    """
    Calculate moment of inertia for a diatomic molecule.

    I = mu x r2

    Parameters
    ----------
    m1, m2 : float
        Atomic masses in kg
    bond_length : float
        Bond length in meters

    Returns
    -------
    float
        Moment of inertia in kg·m2

    Examples
    --------
    >>> moment_of_inertia_diatomic(14 * 1.66e-27, 14 * 1.66e-27, 1.097e-10)  # N2
    1.4e-46...
    """
    if bond_length <= 0:
        raise ValueError("Bond length must be positive")
    mu = reduced_mass(m1, m2)
    return mu * bond_length**2


def population_ratio(energy1: float, energy2: float,
                     temperature: float) -> float:
    """
    Calculate population ratio N2/N1 between two energy levels.

    N2/N1 = exp(-(E2 - E1)/kT)

    Parameters
    ----------
    energy1, energy2 : float
        Energies of levels 1 and 2 in Joules
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Population ratio N2/N1

    Examples
    --------
    >>> population_ratio(0, 1e-20, 300)  # ground vs excited state
    0.0889...
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    delta_E = energy2 - energy1
    return np.exp(-delta_E / (k_B * temperature))


def fraction_in_vibrational_state(v: int, theta_vib: float,
                                  temperature: float) -> float:
    """
    Calculate fraction of molecules in vibrational state v.

    f_v = (1 - exp(-Θ_vib/T)) x exp(-v x Θ_vib/T)

    Parameters
    ----------
    v : int
        Vibrational quantum number (0, 1, 2, ...)
    theta_vib : float
        Vibrational temperature in Kelvin
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Fraction in state v

    Examples
    --------
    >>> fraction_in_vibrational_state(0, 3393, 300)  # N2 v=0
    0.999...
    >>> fraction_in_vibrational_state(1, 3393, 300)  # N2 v=1
    0.001...
    """
    if v < 0 or theta_vib <= 0 or temperature <= 0:
        raise ValueError("Invalid parameters")

    x = theta_vib / temperature
    return (1 - np.exp(-x)) * np.exp(-v * x)


# =============================================================================
# Conversion Utilities
# =============================================================================

def wavenumber_to_frequency(wavenumber_cm: float) -> float:
    """Convert wavenumber (cm-1) to frequency (Hz)."""
    return wavenumber_cm * c


def frequency_to_wavenumber(frequency_Hz: float) -> float:
    """Convert frequency (Hz) to wavenumber (cm-1)."""
    return frequency_Hz / c


def energy_to_wavenumber(energy_J: float) -> float:
    """Convert energy (J) to wavenumber (cm-1)."""
    return energy_J / (h * c)


def wavenumber_to_energy(wavenumber_cm: float) -> float:
    """Convert wavenumber (cm-1) to energy (J)."""
    return wavenumber_cm * h * c


# =============================================================================
# Summary Statistics for Common Molecules
# =============================================================================

MOLECULAR_DATA = {
    'H2': {
        'mass_kg': 2 * 1.00794 * 1.66054e-27,
        'bond_length_m': 74.14e-12,
        'wavenumber_cm': 4400,
        'B_cm': 60.864,
        'sigma': 2
    },
    'N2': {
        'mass_kg': 2 * 14.0067 * 1.66054e-27,
        'bond_length_m': 109.7e-12,
        'wavenumber_cm': 2358,
        'B_cm': 2.001,
        'sigma': 2
    },
    'O2': {
        'mass_kg': 2 * 15.9994 * 1.66054e-27,
        'bond_length_m': 120.7e-12,
        'wavenumber_cm': 1580,
        'B_cm': 1.446,
        'sigma': 2
    },
    'CO': {
        'mass_kg': (12.0107 + 15.9994) * 1.66054e-27,
        'bond_length_m': 112.8e-12,
        'wavenumber_cm': 2170,
        'B_cm': 1.931,
        'sigma': 1
    },
    'HCl': {
        'mass_kg': (1.00794 + 35.453) * 1.66054e-27,
        'bond_length_m': 127.5e-12,
        'wavenumber_cm': 2938,
        'B_cm': 10.44,
        'sigma': 1
    },
    'I2': {
        'mass_kg': 2 * 126.9045 * 1.66054e-27,
        'bond_length_m': 266.6e-12,
        'wavenumber_cm': 214.57,
        'B_cm': 0.037,
        'sigma': 2
    }
}


def get_partition_functions(molecule: str, temperature: float,
                            volume: float = 1e-3) -> dict:
    """
    Calculate all partition functions for a known molecule.

    Parameters
    ----------
    molecule : str
        Molecule name ('H2', 'N2', 'O2', 'CO', 'HCl', 'I2')
    temperature : float
        Temperature in Kelvin
    volume : float, optional
        Volume in m3, default 1 liter

    Returns
    -------
    dict
        Dictionary with q_trans, q_rot, q_vib, q_total

    Examples
    --------
    >>> get_partition_functions('N2', 300)
    {'q_trans': ..., 'q_rot': ..., 'q_vib': ..., 'q_total': ...}
    """
    if molecule not in MOLECULAR_DATA:
        raise ValueError(f"Unknown molecule: {molecule}")

    data = MOLECULAR_DATA[molecule]

    q_trans = translational_partition_function(
        data['mass_kg'], volume, temperature
    )
    q_rot = rotational_partition_function_from_B(
        data['B_cm'], temperature, data['sigma']
    )
    q_vib = vibrational_partition_function_from_wavenumber(
        data['wavenumber_cm'], temperature
    )

    return {
        'q_trans': q_trans,
        'q_rot': q_rot,
        'q_vib': q_vib,
        'q_total': q_trans * q_rot * q_vib,
        'theta_vib': vibrational_temperature_from_wavenumber(data['wavenumber_cm']),
        'theta_rot': temperature / q_rot  # from q_rot = T/(theta_rot * sigma)
    }


if __name__ == '__main__':
    # Quick test
    print("Statistical Mechanics Tools - Quick Test")
    print("=" * 50)

    # Test N2 at 300 K
    T = 300
    V = 1e-3  # 1 liter

    print(f"\nN2 at {T} K, {V*1000:.1f} L:")
    result = get_partition_functions('N2', T, V)
    for key, value in result.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3e}")

    print(f"\nTranslational energy: {internal_energy_translational(T):.3e} J")
    print(f"Rotational energy: {internal_energy_rotational(T):.3e} J")
    print(f"Vibrational energy: {internal_energy_vibrational(7.07e13, T):.3e} J")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="boltzmann_factor",
            description="Calculate the Boltzmann factor exp(-E/kT).",
            input_schema=[
            InputSchemaField(name="energy", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="boltzmann_probability",
            description="Calculate the probability of occupying a state with given energy.",
            input_schema=[
            InputSchemaField(name="energy", type="number", required=True),
            InputSchemaField(name="partition_function", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="de_broglie_wavelength",
            description="Calculate the thermal de Broglie wavelength.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="energy_to_wavenumber",
            description="Convert energy (J) to wavenumber (cm-1).",
            input_schema=[
            InputSchemaField(name="energy_J", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_from_partition_function",
            description="Calculate entropy from partition function.",
            input_schema=[
            InputSchemaField(name="partition_function", type="number", required=True),
            InputSchemaField(name="internal_energy", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="N", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_sackur_tetrode",
            description="Calculate entropy of monatomic ideal gas using Sackur-Tetrode equation.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="volume", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="N", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fraction_in_vibrational_state",
            description="Calculate fraction of molecules in vibrational state v.",
            input_schema=[
            InputSchemaField(name="v", type="number", required=True),
            InputSchemaField(name="theta_vib", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="frequency_to_wavenumber",
            description="Convert frequency (Hz) to wavenumber (cm-1).",
            input_schema=[
            InputSchemaField(name="frequency_Hz", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="get_partition_functions",
            description="Calculate all partition functions for a known molecule.",
            input_schema=[
            InputSchemaField(name="molecule", type="string", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="volume", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_free_energy",
            description="Calculate Gibbs free energy for ideal gas.",
            input_schema=[
            InputSchemaField(name="partition_function", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="pressure", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_rotational",
            description="Rotational contribution to heat capacity.",
            input_schema=[
            InputSchemaField(name="linear", type="number", required=False),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_translational",
            description="Translational contribution to heat capacity.",
            input_schema=[
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_vibrational",
            description="Vibrational contribution to heat capacity.",
            input_schema=[
            InputSchemaField(name="frequency_Hz", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="helmholtz_free_energy",
            description="Calculate Helmholtz free energy from partition function.",
            input_schema=[
            InputSchemaField(name="partition_function", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_from_Z",
            description="Calculate internal energy from partition function.",
            input_schema=[
            InputSchemaField(name="partition_function", type="number", required=True),
            InputSchemaField(name="dlnZ_dT", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_rotational",
            description="Calculate rotational contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="linear", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_translational",
            description="Calculate translational contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_vibrational",
            description="Calculate vibrational contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="frequency_Hz", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="moment_of_inertia_diatomic",
            description="Calculate moment of inertia for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="m1", type="number", required=True),
            InputSchemaField(name="m2", type="number", required=True),
            InputSchemaField(name="bond_length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="partition_function_canonical",
            description="Calculate the canonical partition function Z = Σ exp(-E_i/kT).",
            input_schema=[
            InputSchemaField(name="energies", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="population_ratio",
            description="Calculate population ratio N2/N1 between two energy levels.",
            input_schema=[
            InputSchemaField(name="energy1", type="number", required=True),
            InputSchemaField(name="energy2", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reduced_mass",
            description="Calculate reduced mass mu = m1 x m2 / (m1 + m2).",
            input_schema=[
            InputSchemaField(name="m1", type="number", required=True),
            InputSchemaField(name="m2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_partition_function",
            description="Calculate the rotational partition function for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="moment_of_inertia", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="sigma", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_partition_function_from_B",
            description="Calculate rotational partition function from rotational constant B.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="sigma", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_temperature",
            description="Calculate the rotational temperature Θ_rot.",
            input_schema=[
            InputSchemaField(name="moment_of_inertia", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="translational_partition_function",
            description="Calculate the translational partition function.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="volume", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_partition_function",
            description="Calculate the vibrational partition function.",
            input_schema=[
            InputSchemaField(name="frequency_Hz", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="include_zpe", type="boolean", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_partition_function_from_wavenumber",
            description="Calculate vibrational partition function from wavenumber.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="include_zpe", type="boolean", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_temperature",
            description="Calculate the vibrational temperature Θ_vib.",
            input_schema=[
            InputSchemaField(name="frequency_Hz", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_temperature_from_wavenumber",
            description="Calculate vibrational temperature from wavenumber.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavenumber_to_energy",
            description="Convert wavenumber (cm-1) to energy (J).",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavenumber_to_frequency",
            description="Convert wavenumber (cm-1) to frequency (Hz).",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
