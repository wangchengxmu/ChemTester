"""
Statistical Thermodynamics Tools - L3 Implementation

Extended statistical mechanics functions:
- Thermodynamic properties from partition functions
- Chemical equilibria from partition functions
- Heat capacities and their temperature dependence
- Free energy calculations
- Equilibrium constant from molecular properties

Source: LibreTexts Physical Chemistry Ch17-18

## Solver Instructions (for AI Agent)

When you encounter statistical thermodynamics problems (internal energy, entropy, heat capacity, equilibrium constants from molecular properties), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Internal energy**: Given T and molecular type -> find U contributions (trans, rot, vib)
- **Entropy**: Given T and molecular parameters -> find S
- **Heat capacity**: Given T and molecular parameters -> find Cv contributions
- **Free energy**: Given partition functions and T -> find A and G
- **Equilibrium constant**: Given partition functions of reactants and products -> find K
- **Temperature dependence**: Given Cv at multiple T -> find how Cv changes with T

### Step 2: Choose the correct function
- `internal_energy_translational(T, N_molecules, molar)` -> U_trans = (3/2)NkT or (3/2)RT
- `internal_energy_rotational(T, linear, molar)` -> U_rot = NkT (linear) or (3/2)NkT (nonlinear)
- `internal_energy_vibrational(T, frequencies, molar)` -> U_vib from each normal mode
- `entropy_translational(T, molar_mass, pressure, molar)` -> Sackur-Tetrode equation
- `entropy_rotational(T, B, sigma, linear, molar)` -> S_rot from rotational constant
- `entropy_vibrational(T, frequencies, molar)` -> S_vib from each normal mode
- `heat_capacity_translational(molar)` -> Cv_trans = (3/2)R (T-independent)
- `heat_capacity_rotational(linear, molar)` -> Cv_rot = R (linear) or (3/2)R (nonlinear)
- `heat_capacity_vibrational(T, frequencies, molar)` -> Cv_vib (T-dependent, Einstein model)
- `equilibrium_constant_from_partition_functions(q_reactants, q_products, T, stoich)` -> K(T)

### Step 3: Handle special cases
- Translational Cv = (3/2)R at all T (classical limit); rotational Cv = R (linear) above θ_rot
- Vibrational contribution: at low T (T << θ_vib), Cv_vib -> 0; at high T, Cv_vib -> R per mode
- Total Cv = Cv_trans + Cv_rot + Cv_vib + Cv_elec (usually Cv_elec ~ 0)
- Equipartition theorem: each DOF contributes (1/2)R to molar Cv (trans: 3, rot: 2 or 3, vib: ~2 per mode at high T)
- For equilibrium constant: K = (q_prod/q_react) x exp(-DeltaE0/kT), include stoichiometric coefficients

### Examples
1. **Total internal energy (molar)**: N2 at 298 K (linear, ν=2359 cm-1)
   -> `internal_energy_translational(298, molar=True)` -> 3718 J/mol
   -> `internal_energy_rotational(298, linear=True, molar=True)` -> 2479 J/mol
   -> `internal_energy_vibrational(298, [2359], molar=True)` -> ~0 J/mol (T << θ_vib)
   -> U_total ~ 6197 J/mol (mostly trans + rot)

2. **Heat capacity**: Compare Cv of Ar (monatomic) vs N2 (diatomic) vs CO2 (nonlinear) at 298 K
   -> Ar: Cv = (3/2)R = 12.5 J/(mol·K)
   -> N2: Cv ~ (3/2)R + R + 0 = (5/2)R = 20.8 J/(mol·K)
   -> CO2: Cv ~ (3/2)R + (3/2)R + ~0 = 3R = 24.9 J/(mol·K)
"""

import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants
from scipy.special import factorial

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
REDUCED_PLANCK = 1.05457182e-34   # J·s
SPEED_OF_LIGHT = 2.99792458e8     # m/s
SPEED_OF_LIGHT_CM = SPEED_OF_LIGHT * 100
BOLTZMANN = 1.380649e-23          # J/K
AVOGADRO = 6.02214076e23          # mol-1
R = 8.314462618                   # J/(mol·K)


# =============================================================================
# INTERNAL ENERGY FROM PARTITION FUNCTIONS
# =============================================================================

def internal_energy_translational(temperature: float, 
                                   N_molecules: int = 1,
                                   molar: bool = False) -> float:
    """
    Calculate translational contribution to internal energy.
    
    U_trans = (3/2)NkT  (per N molecules)
    U_trans = (3/2)RT   (per mole)
    
    Args:
        temperature: Temperature in K
        N_molecules: Number of molecules (default 1)
        molar: If True, return molar quantity
    
    Returns:
        Translational internal energy in J (or J/mol if molar)
    
    Example:
        >>> internal_energy_translational(300, molar=True)
        3740.6  # J/mol
    """
    if molar:
        return 1.5 * R * temperature
    else:
        return 1.5 * N_molecules * BOLTZMANN * temperature


def internal_energy_rotational(temperature: float, 
                                linear: bool = True,
                                molar: bool = False) -> float:
    """
    Calculate rotational contribution to internal energy.
    
    Linear molecules: U_rot = kT (2 rotational DOF)
    Nonlinear molecules: U_rot = 3kT/2 (3 rotational DOF)
    
    Args:
        temperature: Temperature in K
        linear: True for linear molecule, False for nonlinear
        molar: If True, return molar quantity
    
    Returns:
        Rotational internal energy
    
    Example:
        >>> internal_energy_rotational(300, linear=True, molar=True)
        2493.8  # J/mol
    """
    if linear:
        energy = BOLTZMANN * temperature  # kT
    else:
        energy = 1.5 * BOLTZMANN * temperature  # 3kT/2
    
    if molar:
        energy *= AVOGADRO
    
    return energy


def internal_energy_vibrational(wavenumber_cm: float, 
                                 temperature: float,
                                 molar: bool = False) -> float:
    """
    Calculate vibrational contribution to internal energy.
    
    U_vib = hcν̃ / (exp(hcν̃/kT) - 1)  [per molecule, per mode]
    
    This is the contribution above zero-point energy.
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
        temperature: Temperature in K
        molar: If True, return molar quantity
    
    Returns:
        Vibrational internal energy (above ZPE)
    
    Example:
        >>> internal_energy_vibrational(1000, 300, molar=True)
        37.7  # J/mol (mostly frozen out)
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    
    # Convert wavenumber to energy
    nu_tilde = wavenumber_cm * 100  # m-1
    E_vib = PLANCK_CONSTANT * SPEED_OF_LIGHT * nu_tilde
    
    # U = E / (exp(E/kT) - 1)
    x = E_vib / (BOLTZMANN * temperature)
    
    if x > 100:  # Prevent overflow, return ~0
        U = 0
    else:
        U = E_vib / (np.exp(x) - 1)
    
    if molar:
        U *= AVOGADRO
    
    return U


def internal_energy_vibrational_high_T(wavenumber_cm: float, 
                                        temperature: float,
                                        molar: bool = False) -> float:
    """
    High-temperature limit of vibrational internal energy.
    
    U_vib ~ kT  (equipartition)
    
    Valid when T >> Θ_vib = hcν̃/k
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
        temperature: Temperature in K
        molar: If True, return molar quantity
    
    Returns:
        High-T limit vibrational energy
    """
    U = BOLTZMANN * temperature
    if molar:
        U *= AVOGADRO
    return U


def internal_energy_electronic(energy_levels_cm: List[float], 
                                degeneracies: List[int],
                                temperature: float,
                                molar: bool = False) -> float:
    """
    Calculate electronic contribution to internal energy.
    
    U_elec = Σ Eᵢgᵢexp(-Eᵢ/kT) / Σ gⱼexp(-Eⱼ/kT)
    
    Args:
        energy_levels_cm: Electronic energy levels in cm-1 (relative to ground)
        degeneracies: Degeneracy of each level
        temperature: Temperature in K
        molar: If True, return molar quantity
    
    Returns:
        Electronic internal energy
    
    Example:
        >>> # Two-level system: ground (g=2) at 0, excited (g=4) at 10000 cm-1
        >>> internal_energy_electronic([0, 10000], [2, 4], 300)
    """
    # Convert to energies
    energies_J = [E * PLANCK_CONSTANT * SPEED_OF_LIGHT_CM for E in energy_levels_cm]
    
    # Calculate partition function
    Z = 0
    for i, (E, g) in enumerate(zip(energies_J, degeneracies)):
        Z += g * np.exp(-E / (BOLTZMANN * temperature))
    
    # Calculate average energy
    numerator = 0
    for E, g in zip(energies_J, degeneracies):
        numerator += E * g * np.exp(-E / (BOLTZMANN * temperature))
    
    U = numerator / Z
    
    if molar:
        U *= AVOGADRO
    
    return U


# =============================================================================
# ENTROPY FROM PARTITION FUNCTIONS
# =============================================================================

def entropy_translational(mass_kg: float, 
                          volume_m3: float,
                          temperature: float,
                          N_molecules: int = 1) -> float:
    """
    Calculate translational contribution to entropy.
    
    S_trans = Nk[ln(V/N x (2pimkT/h2)^(3/2)) + 5/2]
    
    This is the Sackur-Tetrode equation.
    
    Args:
        mass_kg: Molecular mass in kg
        volume_m3: Volume in m3
        temperature: Temperature in K
        N_molecules: Number of molecules
    
    Returns:
        Translational entropy in J/K
    
    Example:
        >>> # Argon at 300 K, 1 L
        >>> entropy_translational(6.63e-26, 1e-3, 300, AVOGADRO)
        154.8  # J/(mol·K)
    """
    # Thermal de Broglie wavelength
    Lambda = PLANCK_CONSTANT / np.sqrt(2 * np.pi * mass_kg * BOLTZMANN * temperature)
    
    # Translational partition function
    q = volume_m3 / Lambda**3
    
    # Entropy (Sackur-Tetrode)
    S = N_molecules * BOLTZMANN * (np.log(q / N_molecules) + 2.5)
    
    return S


def entropy_sackur_tetrode_molar(mass_amu: float,
                                  pressure_Pa: float,
                                  temperature: float) -> float:
    """
    Molar entropy of ideal gas at given P and T.
    
    S_m = R[ln((2pim)^(3/2)(kT)^(5/2)/(h3P)) + 5/2]
    
    Args:
        mass_amu: Molecular mass in amu
        pressure_Pa: Pressure in Pa
        temperature: Temperature in K
    
    Returns:
        Molar entropy in J/(mol·K)
    
    Example:
        >>> entropy_sackur_tetrode_molar(40, 101325, 298)
        154.8  # J/(mol·K) for Ar at STP
    """
    # Convert mass
    mass_kg = mass_amu * 1.66053907e-27
    
    # Standard formula
    term1 = 1.5 * np.log(2 * np.pi * mass_kg)
    term2 = 2.5 * np.log(BOLTZMANN * temperature)
    term3 = -3 * np.log(PLANCK_CONSTANT)
    term4 = -np.log(pressure_Pa)
    
    S = R * (term1 + term2 + term3 + term4 + 2.5)
    
    return S


def entropy_rotational(theta_rot: float, 
                        temperature: float,
                        sigma: int = 1,
                        linear: bool = True,
                        molar: bool = True) -> float:
    """
    Calculate rotational contribution to entropy.
    
    Linear: S_rot = R[ln(T/(σΘ_rot)) + 1]
    Nonlinear: S_rot = R[ln(√(piT3/(σΘ_AΘ_BΘ_C))) + 3/2]
    
    Args:
        theta_rot: Rotational temperature in K (or Θ_A for nonlinear)
        temperature: Temperature in K
        sigma: Symmetry number
        linear: True for linear molecule
        molar: If True, return molar entropy
    
    Returns:
        Rotational entropy
    
    Example:
        >>> entropy_rotational(2.88, 300, sigma=2)  # N2
        41.5  # J/(mol·K)
    """
    if linear:
        S = R * (np.log(temperature / (sigma * theta_rot)) + 1)
    else:
        # For nonlinear, need all three rotational temps
        # Simplified version assumes theta_rot is product
        S = R * (0.5 * np.log(np.pi * temperature**3 / sigma) - 
                 1.5 * np.log(theta_rot) + 1.5)
    
    if not molar:
        S /= AVOGADRO
    
    return S


def entropy_vibrational(wavenumber_cm: float, 
                         temperature: float,
                         molar: bool = True) -> float:
    """
    Calculate vibrational contribution to entropy.
    
    S_vib = R[(x/(e^x - 1)) - ln(1 - e^(-x))]
    where x = Θ_vib/T = hcν̃/kT
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
        temperature: Temperature in K
        molar: If True, return molar entropy
    
    Returns:
        Vibrational entropy (per mode)
    
    Example:
        >>> entropy_vibrational(2358, 300)  # N2 at 300K
        0.0017  # J/(mol·K) (nearly frozen out)
    """
    # Calculate Θ_vib/T
    theta_vib = wavenumber_cm * PLANCK_CONSTANT * SPEED_OF_LIGHT_CM / BOLTZMANN
    x = theta_vib / temperature
    
    if x > 50:  # High x, contribution is negligible
        S = 0
    else:
        exp_x = np.exp(x)
        S = R * (x / (exp_x - 1) - np.log(1 - 1/exp_x))
    
    if not molar:
        S /= AVOGADRO
    
    return S


def entropy_vibrational_total(wavenumbers_cm: List[float], 
                               temperature: float,
                               molar: bool = True) -> float:
    """
    Calculate total vibrational entropy for multiple modes.
    
    S_total = Σ S_mode
    
    Args:
        wavenumbers_cm: List of vibrational wavenumbers in cm-1
        temperature: Temperature in K
        molar: If True, return molar entropy
    
    Returns:
        Total vibrational entropy
    """
    S_total = sum(entropy_vibrational(wn, temperature, molar=False) 
                  for wn in wavenumbers_cm)
    
    if molar:
        S_total *= AVOGADRO
    
    return S_total


# =============================================================================
# HEAT CAPACITY FROM PARTITION FUNCTIONS
# =============================================================================

def heat_capacity_translational(molar: bool = True) -> float:
    """
    Translational contribution to C_V.
    
    C_V,trans = 3/2 x R  (per mole)
    C_V,trans = 3/2 x k  (per molecule)
    
    Args:
        molar: If True, return molar heat capacity
    
    Returns:
        Heat capacity
    
    Example:
        >>> heat_capacity_translational()
        12.47  # J/(mol·K)
    """
    if molar:
        return 1.5 * R
    else:
        return 1.5 * BOLTZMANN


def heat_capacity_rotational(linear: bool = True, 
                              molar: bool = True) -> float:
    """
    Rotational contribution to C_V.
    
    Linear: C_V,rot = R  (2 DOF)
    Nonlinear: C_V,rot = 3R/2  (3 DOF)
    
    Valid at T >> Θ_rot
    
    Args:
        linear: True for linear molecule
        molar: If True, return molar heat capacity
    
    Returns:
        Heat capacity
    
    Example:
        >>> heat_capacity_rotational(linear=True)
        8.314  # J/(mol·K)
    """
    if molar:
        factor = R
    else:
        factor = BOLTZMANN
    
    if linear:
        return factor  # 2 DOF x 1/2 R each
    else:
        return 1.5 * factor  # 3 DOF


def heat_capacity_vibrational(wavenumber_cm: float, 
                               temperature: float,
                               molar: bool = True) -> float:
    """
    Vibrational contribution to C_V.
    
    C_V,vib = R x x2 x e^x / (e^x - 1)2
    where x = Θ_vib/T
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
        temperature: Temperature in K
        molar: If True, return molar heat capacity
    
    Returns:
        Heat capacity (per mode)
    
    Example:
        >>> heat_capacity_vibrational(2358, 300)  # N2 at 300K
        0.001  # J/(mol·K) (nearly frozen out)
    """
    theta_vib = wavenumber_cm * PLANCK_CONSTANT * SPEED_OF_LIGHT_CM / BOLTZMANN
    x = theta_vib / temperature
    
    if x > 50:
        C_V = 0  # Mode frozen out
    else:
        exp_x = np.exp(x)
        C_V = R * x**2 * exp_x / (exp_x - 1)**2
    
    if not molar:
        C_V /= AVOGADRO
    
    return C_V


def heat_capacity_vibrational_total(wavenumbers_cm: List[float], 
                                     temperature: float,
                                     molar: bool = True) -> float:
    """
    Calculate total vibrational heat capacity.
    
    Args:
        wavenumbers_cm: List of vibrational wavenumbers
        temperature: Temperature in K
        molar: If True, return molar heat capacity
    
    Returns:
        Total vibrational C_V
    """
    C_total = sum(heat_capacity_vibrational(wn, temperature, molar=False) 
                   for wn in wavenumbers_cm)
    
    if molar:
        C_total *= AVOGADRO
    
    return C_total


# =============================================================================
# FREE ENERGY FROM PARTITION FUNCTIONS
# =============================================================================

def helmholtz_free_energy_translational(mass_kg: float,
                                         volume_m3: float,
                                         temperature: float,
                                         N_molecules: int = 1) -> float:
    """
    Calculate translational Helmholtz free energy.
    
    A = -kT ln(Q) = -NkT ln(q/N) - NkT
    
    Args:
        mass_kg: Molecular mass in kg
        volume_m3: Volume in m3
        temperature: Temperature in K
        N_molecules: Number of molecules
    
    Returns:
        Helmholtz free energy in J
    
    Example:
        >>> # Ar atom at 300 K in 1 L
        >>> A = helmholtz_free_energy_translational(6.63e-26, 1e-3, 300, 1)
    """
    # Thermal de Broglie wavelength
    Lambda = PLANCK_CONSTANT / np.sqrt(2 * np.pi * mass_kg * BOLTZMANN * temperature)
    
    # Partition function
    q = volume_m3 / Lambda**3
    
    # Helmholtz free energy
    A = -N_molecules * BOLTZMANN * temperature * (np.log(q / N_molecules) + 1)
    
    return A


def gibbs_free_energy_ideal_gas(mass_amu: float,
                                 pressure_Pa: float,
                                 temperature: float) -> float:
    """
    Calculate molar Gibbs free energy of ideal gas.
    
    G = -RT ln[(2pim)^(3/2)(kT)^(5/2)/(h3P)]
    
    Args:
        mass_amu: Molecular mass in amu
        pressure_Pa: Pressure in Pa
        temperature: Temperature in K
    
    Returns:
        Molar Gibbs free energy in J/mol
    
    Example:
        >>> gibbs_free_energy_ideal_gas(40, 101325, 298)
        -40000  # J/mol (approximately)
    """
    mass_kg = mass_amu * 1.66053907e-27
    
    # Argument of log
    arg = ((2 * np.pi * mass_kg)**1.5 * 
           (BOLTZMANN * temperature)**2.5 / 
           (PLANCK_CONSTANT**3 * pressure_Pa))
    
    G = -R * temperature * np.log(arg)
    
    return G


# =============================================================================
# EQUILIBRIUM CONSTANTS FROM PARTITION FUNCTIONS
# =============================================================================

def equilibrium_constant_from_partition_functions(
    q_A: float,
    q_B: float,
    q_C: float,
    q_D: float,
    delta_E0: float,
    temperature: float,
    stoichiometry: Tuple[int, int, int, int] = (1, 1, 1, 1)
) -> float:
    """
    Calculate equilibrium constant from partition functions.
    
    For reaction: aA + bB ⇌ cC + dD
    
    K = (q_C^c x q_D^d / (q_A^a x q_B^b)) x exp(-DeltaE0/RT)
    
    Args:
        q_A, q_B, q_C, q_D: Molecular partition functions
        delta_E0: Zero-point energy difference (products - reactants) in J/mol
        temperature: Temperature in K
        stoichiometry: (a, b, c, d) coefficients
    
    Returns:
        Equilibrium constant K (dimensionless)
    
    Note:
        Partition functions must be on same scale (same volume reference).
        Use q/N for proper units.
    """
    a, b, c, d = stoichiometry
    
    # Product of partition functions
    numerator = q_C**c * q_D**d
    denominator = q_A**a * q_B**b
    
    # Boltzmann factor
    boltzmann = np.exp(-delta_E0 / (R * temperature))
    
    K = (numerator / denominator) * boltzmann
    
    return K


def equilibrium_constant_translational_contribution(
    stoichiometry_coeff: int,
    mass_products_kg: List[float],
    mass_reactants_kg: List[float],
    temperature: float
) -> float:
    """
    Calculate translational contribution to equilibrium constant.
    
    Deltan = (c + d) - (a + b)
    K_trans = (kT/Pdeg)^Deltan x (mu_products/mu_reactants)^(3/2) x ...
    
    Simplified: returns the mass ratio contribution.
    
    Args:
        stoichiometry_coeff: Deltan = moles products - moles reactants
        mass_products_kg: Masses of product molecules in kg
        mass_reactants_kg: Masses of reactant molecules in kg
        temperature: Temperature in K
    
    Returns:
        Translational contribution to K
    """
    # Mass ratio contribution
    mass_product = np.prod(mass_products_kg)
    mass_reactant = np.prod(mass_reactants_kg)
    
    K_trans = (mass_product / mass_reactant)**1.5
    
    return K_trans


# =============================================================================
# COMBINED MOLECULAR PROPERTIES
# =============================================================================

def total_partition_function_diatomic(
    mass_amu: float,
    volume_m3: float,
    temperature: float,
    bond_length_m: float,
    wavenumber_cm: float,
    sigma: int = 1,
    electronic_degeneracy: int = 1
) -> Dict[str, float]:
    """
    Calculate all partition functions for a diatomic molecule.
    
    Returns:
        Dictionary with q_trans, q_rot, q_vib, q_elec, q_total
    """
    mass_kg = mass_amu * 1.66053907e-27
    
    # Translational
    Lambda = PLANCK_CONSTANT / np.sqrt(2 * np.pi * mass_kg * BOLTZMANN * temperature)
    q_trans = volume_m3 / Lambda**3
    
    # Rotational
    theta_rot = REDUCED_PLANCK**2 / (2 * mass_kg * bond_length_m**2 * BOLTZMANN)
    q_rot = temperature / (sigma * theta_rot)
    
    # Vibrational
    theta_vib = wavenumber_cm * PLANCK_CONSTANT * SPEED_OF_LIGHT_CM / BOLTZMANN
    q_vib = 1 / (1 - np.exp(-theta_vib / temperature))
    
    # Electronic
    q_elec = electronic_degeneracy
    
    return {
        'q_trans': q_trans,
        'q_rot': q_rot,
        'q_vib': q_vib,
        'q_elec': q_elec,
        'q_total': q_trans * q_rot * q_vib * q_elec,
        'theta_rot': theta_rot,
        'theta_vib': theta_vib
    }


def thermodynamic_properties_diatomic(
    mass_amu: float,
    volume_m3: float,
    temperature: float,
    bond_length_m: float,
    wavenumber_cm: float,
    sigma: int = 1
) -> Dict[str, float]:
    """
    Calculate all thermodynamic properties for a diatomic molecule.
    
    Returns:
        Dictionary with U, S, A, G, C_V contributions and totals
    """
    mass_kg = mass_amu * 1.66053907e-27
    
    # Internal energy contributions
    U_trans = internal_energy_translational(temperature, AVOGADRO, molar=True)
    U_rot = internal_energy_rotational(temperature, linear=True, molar=True)
    U_vib = internal_energy_vibrational(wavenumber_cm, temperature, molar=True)
    U_total = U_trans + U_rot + U_vib
    
    # Entropy contributions
    S_trans = entropy_translational(mass_kg, volume_m3, temperature, AVOGADRO)
    S_rot = entropy_rotational(
        REDUCED_PLANCK**2 / (2 * mass_kg * bond_length_m**2 * BOLTZMANN),
        temperature, sigma, linear=True, molar=True
    )
    S_vib = entropy_vibrational(wavenumber_cm, temperature, molar=True)
    S_total = S_trans + S_rot + S_vib
    
    # Heat capacities
    C_V_trans = heat_capacity_translational(molar=True)
    C_V_rot = heat_capacity_rotational(linear=True, molar=True)
    C_V_vib = heat_capacity_vibrational(wavenumber_cm, temperature, molar=True)
    C_V_total = C_V_trans + C_V_rot + C_V_vib
    
    # Free energies
    A_total = U_total - temperature * S_total
    G_total = A_total  # For ideal gas at standard pressure
    
    return {
        'U_trans': U_trans,
        'U_rot': U_rot,
        'U_vib': U_vib,
        'U_total': U_total,
        'S_trans': S_trans,
        'S_rot': S_rot,
        'S_vib': S_vib,
        'S_total': S_total,
        'C_V_trans': C_V_trans,
        'C_V_rot': C_V_rot,
        'C_V_vib': C_V_vib,
        'C_V_total': C_V_total,
        'A': A_total,
        'G': G_total
    }


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Statistical Thermodynamics Tools - Examples")
    print("=" * 60)
    
    # Internal energy
    print("\n1. Internal Energy Contributions (N2 at 300 K):")
    U_trans = internal_energy_translational(300, molar=True)
    U_rot = internal_energy_rotational(300, linear=True, molar=True)
    U_vib = internal_energy_vibrational(2358, 300, molar=True)
    print(f"   U_trans: {U_trans:.1f} J/mol")
    print(f"   U_rot: {U_rot:.1f} J/mol")
    print(f"   U_vib: {U_vib:.3f} J/mol (nearly frozen)")
    print(f"   Total: {U_trans + U_rot + U_vib:.1f} J/mol")
    
    # Entropy
    print("\n2. Entropy Contributions (N2 at 300 K, 1 atm):")
    S_trans = entropy_sackur_tetrode_molar(28, 101325, 300)
    S_rot = entropy_rotational(2.88, 300, sigma=2, linear=True)
    S_vib = entropy_vibrational(2358, 300)
    print(f"   S_trans: {S_trans:.1f} J/(mol·K)")
    print(f"   S_rot: {S_rot:.1f} J/(mol·K)")
    print(f"   S_vib: {S_vib:.4f} J/(mol·K)")
    
    # Heat capacity
    print("\n3. Heat Capacity Contributions:")
    C_V_trans = heat_capacity_translational()
    C_V_rot = heat_capacity_rotational()
    C_V_vib = heat_capacity_vibrational(2358, 300)
    print(f"   C_V,trans: {C_V_trans:.2f} J/(mol·K)")
    print(f"   C_V,rot: {C_V_rot:.2f} J/(mol·K)")
    print(f"   C_V,vib: {C_V_vib:.4f} J/(mol·K)")
    print(f"   Total: {C_V_trans + C_V_rot + C_V_vib:.2f} J/(mol·K)")
    
    # Complete calculation
    print("\n4. Complete Thermodynamic Properties (N2 at 300 K):")
    props = thermodynamic_properties_diatomic(
        mass_amu=28,
        volume_m3=24.8e-3,  # ~24.8 L at STP
        temperature=300,
        bond_length_m=110e-12,
        wavenumber_cm=2358,
        sigma=2
    )
    print(f"   U_total: {props['U_total']:.1f} J/mol")
    print(f"   S_total: {props['S_total']:.1f} J/(mol·K)")
    print(f"   C_V,total: {props['C_V_total']:.2f} J/(mol·K)")
    print(f"   G: {props['G']:.1f} J/mol")
    
    print("\n" + "=" * 60)
    print("All examples completed!")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="entropy_rotational",
            description="Calculate rotational contribution to entropy.",
            input_schema=[
            InputSchemaField(name="theta_rot", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="sigma", type="number", required=False),
            InputSchemaField(name="linear", type="number", required=False),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_sackur_tetrode_molar",
            description="Molar entropy of ideal gas at given P and T.",
            input_schema=[
            InputSchemaField(name="mass_amu", type="number", required=True),
            InputSchemaField(name="pressure_Pa", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_translational",
            description="Calculate translational contribution to entropy.",
            input_schema=[
            InputSchemaField(name="mass_kg", type="number", required=True),
            InputSchemaField(name="volume_m3", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="N_molecules", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_vibrational",
            description="Calculate vibrational contribution to entropy.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_vibrational_total",
            description="Calculate total vibrational entropy for multiple modes.",
            input_schema=[
            InputSchemaField(name="wavenumbers_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="equilibrium_constant_from_partition_functions",
            description="Calculate equilibrium constant from partition functions.",
            input_schema=[
            InputSchemaField(name="q_A", type="number", required=True),
            InputSchemaField(name="q_B", type="number", required=True),
            InputSchemaField(name="q_C", type="number", required=True),
            InputSchemaField(name="q_D", type="number", required=True),
            InputSchemaField(name="delta_E0", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="stoichiometry", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="equilibrium_constant_translational_contribution",
            description="Calculate translational contribution to equilibrium constant.",
            input_schema=[
            InputSchemaField(name="stoichiometry_coeff", type="number", required=True),
            InputSchemaField(name="mass_products_kg", type="number", required=True),
            InputSchemaField(name="mass_reactants_kg", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_free_energy_ideal_gas",
            description="Calculate molar Gibbs free energy of ideal gas.",
            input_schema=[
            InputSchemaField(name="mass_amu", type="number", required=True),
            InputSchemaField(name="pressure_Pa", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_rotational",
            description="Rotational contribution to C_V.",
            input_schema=[
            InputSchemaField(name="linear", type="number", required=False),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_translational",
            description="Translational contribution to C_V.",
            input_schema=[
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_vibrational",
            description="Vibrational contribution to C_V.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heat_capacity_vibrational_total",
            description="Calculate total vibrational heat capacity.",
            input_schema=[
            InputSchemaField(name="wavenumbers_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="helmholtz_free_energy_translational",
            description="Calculate translational Helmholtz free energy.",
            input_schema=[
            InputSchemaField(name="mass_kg", type="number", required=True),
            InputSchemaField(name="volume_m3", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="N_molecules", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_electronic",
            description="Calculate electronic contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="energy_levels_cm", type="number", required=True),
            InputSchemaField(name="degeneracies", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_rotational",
            description="Calculate rotational contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="linear", type="number", required=False),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_translational",
            description="Calculate translational contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="N_molecules", type="string", required=False),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_vibrational",
            description="Calculate vibrational contribution to internal energy.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="internal_energy_vibrational_high_T",
            description="High-temperature limit of vibrational internal energy.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="molar", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="thermodynamic_properties_diatomic",
            description="Calculate all thermodynamic properties for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="mass_amu", type="number", required=True),
            InputSchemaField(name="volume_m3", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="bond_length_m", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="sigma", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="total_partition_function_diatomic",
            description="Calculate all partition functions for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="mass_amu", type="number", required=True),
            InputSchemaField(name="volume_m3", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="bond_length_m", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="sigma", type="number", required=False),
            InputSchemaField(name="electronic_degeneracy", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
