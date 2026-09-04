"""
Quantum Mechanics Tools - L3 Implementation

Core functions for quantum mechanics calculations:
- Particle in a box (1D, 2D, 3D)
- Harmonic oscillator
- Rigid rotor
- Hydrogen atom
- Expectation values and uncertainties

Source: LibreTexts Physical Chemistry Ch03-06

## Solver Instructions (for AI Agent)

When you encounter quantum mechanics problems (particle in box, harmonic oscillator, rigid rotor, hydrogen atom, expectation values), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Particle in box**: Given quantum number, mass, box length -> find energy, wavelength, probability
- **Harmonic oscillator**: Given quantum number, frequency/mass/force constant -> find energy, turning points
- **Rigid rotor**: Given quantum number J, moment of inertia -> find energy, angular momentum
- **Hydrogen atom**: Given quantum numbers (n,l,m) or transition -> find energy, radius, wavelength
- **Expectation values**: Given quantum state and operator -> find <x>, <p>, Deltax, Deltap

### Step 2: Choose the correct function
- `particle_in_box_energy(n, mass, length)` -> E = n2h2/(8mL2) in Joules
- `particle_in_box_energy_ev(n, mass, length)` -> same but in eV
- `particle_in_box_wavelength(n, mass, length)` -> lambda = 2L/n
- `particle_in_box_probability(n, L, x1, x2)` -> probability of finding particle in [x1, x2]
- `harmonic_oscillator_energy(v, frequency)` -> E = (v+½)hν
- `harmonic_oscillator_energy_classical(freq, mass)` -> E = ½kA2 = ½mω2A2
- `rigid_rotor_energy(J, moment_of_inertia)` -> E = J(J+1)ℏ2/(2I)
- `hydrogen_energy(n)` -> E_n = -13.6 eV/n2
- `hydrogen_radius(n)` -> r = a0n2
- `hydrogen_transition_wavelength(n_initial, n_final)` -> lambda in nm

### Step 3: Handle special cases
- Quantum numbers start at 1 (particle in box, hydrogen n), 0 (oscillator v, rotor J)
- Mass must be in kg, length in meters - convert from amu/Å as needed
- Hydrogen energy: negative values (bound state); 0 eV at ionization
- For 2D/3D boxes, energy levels are degenerate; use the respective functions

### Examples
1. **Particle in box**: Electron (9.109e-31 kg) in 1 nm box, n=1
   -> `particle_in_box_energy(1, 9.109e-31, 1e-9)` -> 6.024e-20 J
   -> `particle_in_box_energy_ev(1, 9.109e-31, 1e-9)` -> 0.376 eV

2. **Hydrogen transition**: n=3 -> n=2 (Balmer Halpha)
   -> `hydrogen_transition_wavelength(3, 2)` -> 656.3 nm (red)

3. **Harmonic oscillator**: v=0 -> v=1 transition, ν=6.0e13 Hz (C=O stretch)
   -> `harmonic_oscillator_energy(1, 6.0e13)` - `harmonic_oscillator_energy(0, 6.0e13)` = hν = 3.976e-20 J = 0.248 eV
"""

import math
from typing import Tuple, List, Union, Optional
import numpy as np
from scipy import integrate
from scipy.special import hermite, factorial, genlaguerre
# sph_harm renamed in newer scipy versions
try:
    from scipy.special import sph_harm
except ImportError:
    from scipy.special import sph_harm_y as sph_harm

# Physical constants (SI units)
PLANCK_CONSTANT = 6.62607015e-34  # J·s
REDUCED_PLANCK = 1.05457182e-34   # J·s
ELECTRON_MASS = 9.1093837e-31     # kg
PROTON_MASS = 1.6726219e-27       # kg
ELEMENTARY_CHARGE = 1.60217663e-19  # C
BOHR_RADIUS = 5.2917721e-11       # m
RYDBERG_CONSTANT = 1.09737316e7   # m^-1
SPEED_OF_LIGHT = 2.99792458e8     # m/s
EV_TO_JOULE = 1.60217663e-19      # J/eV


# =============================================================================
# PARTICLE IN A BOX
# =============================================================================

def particle_in_box_energy(n: int, mass: float, length: float) -> float:
    """
    Calculate the energy of a particle in a 1D box.
    
    E_n = n2h2/(8mL2)
    
    Args:
        n: Quantum number (n = 1, 2, 3, ...)
        mass: Particle mass in kg
        length: Box length in meters
    
    Returns:
        Energy in Joules
    
    Raises:
        ValueError: If n < 1 or mass/length <= 0
    """
    if n < 1:
        raise ValueError(f"Quantum number n must be >= 1, got {n}")
    if mass <= 0:
        raise ValueError(f"Mass must be positive, got {mass}")
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")
    
    return (n**2 * PLANCK_CONSTANT**2) / (8 * mass * length**2)


def particle_in_box_energy_ev(n: int, mass: float, length: float) -> float:
    """
    Calculate particle in box energy in electron volts.
    
    Args:
        n: Quantum number
        mass: Particle mass in kg
        length: Box length in meters
    
    Returns:
        Energy in eV
    """
    return particle_in_box_energy(n, mass, length) / EV_TO_JOULE


def particle_in_box_wavefunction(n: int, x: Union[float, np.ndarray], 
                                  length: float, normalized: bool = True) -> Union[float, np.ndarray]:
    """
    Calculate the wavefunction for a particle in a 1D box.
    
    ψ_n(x) = √(2/L) sin(npix/L)
    
    Args:
        n: Quantum number (n = 1, 2, 3, ...)
        x: Position(s) in meters (0 ≤ x ≤ L)
        length: Box length in meters
        normalized: If True, return normalized wavefunction
    
    Returns:
        Wavefunction value(s)
    
    Raises:
        ValueError: If n < 1 or length <= 0
    """
    if n < 1:
        raise ValueError(f"Quantum number n must be >= 1, got {n}")
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")
    
    # Check if x is within bounds
    x_arr = np.atleast_1d(np.array(x))
    if np.any(x_arr < 0) or np.any(x_arr > length):
        # Return 0 for positions outside the box
        result = np.zeros_like(x_arr, dtype=float)
        inside = (x_arr >= 0) & (x_arr <= length)
        x_inside = x_arr[inside] if np.any(inside) else x_arr
        
        if normalized:
            norm_factor = np.sqrt(2 / length)
        else:
            norm_factor = 1.0
        
        result[inside] = norm_factor * np.sin(n * np.pi * x_inside / length)
        # Return scalar if input was scalar
        return float(result[0]) if np.isscalar(x) or result.size == 1 else result
    
    if normalized:
        norm_factor = np.sqrt(2 / length)
    else:
        norm_factor = 1.0
    
    return norm_factor * np.sin(n * np.pi * x / length)


def particle_in_box_probability(n: int, x: Union[float, np.ndarray], 
                                 length: float) -> Union[float, np.ndarray]:
    """
    Calculate probability density |ψ|2 for particle in a box.
    
    Args:
        n: Quantum number
        x: Position(s) in meters
        length: Box length in meters
    
    Returns:
        Probability density |ψ|2
    """
    psi = particle_in_box_wavefunction(n, x, length)
    return np.abs(psi)**2


def particle_in_box_3d_energy(n_x: int, n_y: int, n_z: int, 
                               mass: float, 
                               L_x: float, L_y: float, L_z: float) -> float:
    """
    Calculate energy for particle in a 3D box.
    
    E = (h2/8m)(n_x2/L_x2 + n_y2/L_y2 + n_z2/L_z2)
    
    Args:
        n_x, n_y, n_z: Quantum numbers (each >= 1)
        mass: Particle mass in kg
        L_x, L_y, L_z: Box dimensions in meters
    
    Returns:
        Energy in Joules
    """
    if any(n < 1 for n in [n_x, n_y, n_z]):
        raise ValueError("All quantum numbers must be >= 1")
    if any(L <= 0 for L in [L_x, L_y, L_z]) or mass <= 0:
        raise ValueError("All dimensions and mass must be positive")
    
    return (PLANCK_CONSTANT**2 / (8 * mass)) * \
           (n_x**2/L_x**2 + n_y**2/L_y**2 + n_z**2/L_z**2)


def particle_in_box_3d_wavefunction(n_x: int, n_y: int, n_z: int,
                                     x: float, y: float, z: float,
                                     L_x: float, L_y: float, L_z: float) -> float:
    """
    Calculate wavefunction for particle in a 3D box.
    
    ψ = √(8/L_xL_yL_z) sin(n_xpix/L_x) sin(n_ypiy/L_y) sin(n_zpiz/L_z)
    
    Args:
        n_x, n_y, n_z: Quantum numbers
        x, y, z: Position coordinates
        L_x, L_y, L_z: Box dimensions
    
    Returns:
        Wavefunction value
    """
    norm = np.sqrt(8 / (L_x * L_y * L_z))
    return norm * np.sin(n_x * np.pi * x / L_x) * \
                np.sin(n_y * np.pi * y / L_y) * \
                np.sin(n_z * np.pi * z / L_z)


def particle_in_box_degeneracy(n: int, cubic: bool = True) -> int:
    """
    Calculate degeneracy for particle in a cubic 3D box.
    
    For cubic box, count number of ways to write n as sum of three squares
    (for ground state approximation).
    
    Args:
        n: Principal quantum number level
        cubic: Whether box is cubic
    
    Returns:
        Degeneracy (1 for non-cubic)
    """
    if not cubic:
        return 1
    
    # For cubic box, count combinations (n_x, n_y, n_z) giving same E
    # This is approximate - exact counting requires checking E values
    count = 0
    limit = int(np.sqrt(3 * n**2)) + 1
    for nx in range(1, limit + 1):
        for ny in range(1, limit + 1):
            for nz in range(1, limit + 1):
                if nx**2 + ny**2 + nz**2 == n**2:
                    count += 1
    return max(1, count)


# =============================================================================
# HARMONIC OSCILLATOR
# =============================================================================

def harmonic_oscillator_frequency(force_constant: float, reduced_mass: float) -> float:
    """
    Calculate vibrational frequency from force constant and reduced mass.
    
    ν = (1/2pi)√(k/mu)
    
    Args:
        force_constant: Force constant k in N/m or J/m2
        reduced_mass: Reduced mass mu in kg
    
    Returns:
        Frequency in Hz
    """
    if force_constant <= 0:
        raise ValueError(f"Force constant must be positive, got {force_constant}")
    if reduced_mass <= 0:
        raise ValueError(f"Reduced mass must be positive, got {reduced_mass}")
    
    return (1 / (2 * np.pi)) * np.sqrt(force_constant / reduced_mass)


def harmonic_oscillator_energy(v: int, frequency: float, in_ev: bool = False) -> float:
    """
    Calculate harmonic oscillator energy.
    
    E_v = (v + ½)hν
    
    Args:
        v: Vibrational quantum number (v = 0, 1, 2, ...)
        frequency: Vibrational frequency in Hz
        in_ev: If True, return energy in eV instead of Joules
    
    Returns:
        Energy in Joules (or eV if in_ev=True)
    
    Raises:
        ValueError: If v < 0 or frequency <= 0
    """
    if v < 0:
        raise ValueError(f"Quantum number v must be >= 0, got {v}")
    if frequency <= 0:
        raise ValueError(f"Frequency must be positive, got {frequency}")
    
    energy = (v + 0.5) * PLANCK_CONSTANT * frequency
    return energy / EV_TO_JOULE if in_ev else energy


def harmonic_oscillator_zero_point_energy(frequency: float, in_ev: bool = False) -> float:
    """
    Calculate zero-point energy of harmonic oscillator.
    
    E_0 = ½hν
    
    Args:
        frequency: Vibrational frequency in Hz
        in_ev: If True, return energy in eV
    
    Returns:
        Zero-point energy
    """
    return harmonic_oscillator_energy(0, frequency, in_ev)


def harmonic_oscillator_energy_spacing(frequency: float, in_ev: bool = False) -> float:
    """
    Calculate energy spacing between adjacent levels.
    
    DeltaE = hν
    
    Args:
        frequency: Vibrational frequency in Hz
        in_ev: If True, return energy in eV
    
    Returns:
        Energy spacing
    """
    energy = PLANCK_CONSTANT * frequency
    return energy / EV_TO_JOULE if in_ev else energy


def harmonic_oscillator_wavefunction(v: int, x: Union[float, np.ndarray], 
                                      mass: float, frequency: float,
                                      normalized: bool = True) -> Union[float, np.ndarray]:
    """
    Calculate harmonic oscillator wavefunction.
    
    ψ_v(x) = N_v · H_v(alpha^½ x) · e^(-alphax2/2)
    
    where alpha = mω/ℏ
    
    Args:
        v: Vibrational quantum number
        x: Position(s) in meters
        mass: Particle mass in kg
        frequency: Frequency in Hz
        normalized: If True, return normalized wavefunction
    
    Returns:
        Wavefunction value(s)
    """
    if v < 0:
        raise ValueError(f"Quantum number v must be >= 0, got {v}")
    
    omega = 2 * np.pi * frequency
    alpha = mass * omega / REDUCED_PLANCK
    sqrt_alpha = np.sqrt(alpha)
    
    # Hermite polynomial
    H_v = hermite(v)
    
    # Normalization constant
    if normalized:
        N_v = (alpha / np.pi)**0.25 / np.sqrt(2**v * math.factorial(v))
    else:
        N_v = 1.0
    
    return N_v * H_v(sqrt_alpha * x) * np.exp(-alpha * x**2 / 2)


def reduced_mass(m1: float, m2: float) -> float:
    """
    Calculate reduced mass for a two-body system.
    
    mu = m1m2/(m1 + m2)
    
    Args:
        m1: Mass of first particle in kg
        m2: Mass of second particle in kg
    
    Returns:
        Reduced mass in kg
    """
    if m1 <= 0 or m2 <= 0:
        raise ValueError("Both masses must be positive")
    return (m1 * m2) / (m1 + m2)


def reduced_mass_amu(m1_amu: float, m2_amu: float) -> float:
    """
    Calculate reduced mass given atomic mass units.
    
    Args:
        m1_amu: Mass of first atom in amu
        m2_amu: Mass of second atom in amu
    
    Returns:
        Reduced mass in kg
    """
    AMU_TO_KG = 1.66053907e-27  # kg/amu
    m1 = m1_amu * AMU_TO_KG
    m2 = m2_amu * AMU_TO_KG
    return reduced_mass(m1, m2)


# =============================================================================
# RIGID ROTOR
# =============================================================================

def moment_of_inertia(reduced_mass: float, bond_length: float) -> float:
    """
    Calculate moment of inertia for a diatomic molecule.
    
    I = mur2
    
    Args:
        reduced_mass: Reduced mass in kg
        bond_length: Bond length in meters
    
    Returns:
        Moment of inertia in kg·m2
    """
    if reduced_mass <= 0:
        raise ValueError("Reduced mass must be positive")
    if bond_length <= 0:
        raise ValueError("Bond length must be positive")
    return reduced_mass * bond_length**2


def rotational_constant(reduced_mass: float, bond_length: float, 
                        in_cm: bool = True) -> float:
    """
    Calculate rotational constant B.
    
    B = h/(8pi2I) = h/(8pi2mur2)
    
    Args:
        reduced_mass: Reduced mass in kg
        bond_length: Bond length in meters
        in_cm: If True, return B in cm-1; if False, return in Hz
    
    Returns:
        Rotational constant
    """
    I = moment_of_inertia(reduced_mass, bond_length)
    
    if in_cm:
        # B = h/(8pi2cI) gives result in m-1, divide by 100 for cm-1
        return PLANCK_CONSTANT / (8 * np.pi**2 * SPEED_OF_LIGHT * I * 100)
    else:
        return PLANCK_CONSTANT / (8 * np.pi**2 * I)


def rigid_rotor_energy(J: int, B: float, in_cm: bool = True) -> float:
    """
    Calculate rigid rotor energy.
    
    E_J = J(J+1)B
    
    Args:
        J: Rotational quantum number (J = 0, 1, 2, ...)
        B: Rotational constant (in cm-1 or same units as desired output)
        in_cm: If True, B is in cm-1; affects interpretation
    
    Returns:
        Energy in same units as B
    """
    if J < 0:
        raise ValueError(f"Quantum number J must be >= 0, got {J}")
    return J * (J + 1) * B


def rigid_rotor_energy_joules(J: int, reduced_mass: float, bond_length: float) -> float:
    """
    Calculate rigid rotor energy in Joules.
    
    E_J = J(J+1)ℏ2/(2I)
    
    Args:
        J: Rotational quantum number
        reduced_mass: Reduced mass in kg
        bond_length: Bond length in meters
    
    Returns:
        Energy in Joules
    """
    I = moment_of_inertia(reduced_mass, bond_length)
    return J * (J + 1) * REDUCED_PLANCK**2 / (2 * I)


def rigid_rotor_degeneracy(J: int) -> int:
    """
    Calculate degeneracy of rotational level J.
    
    g_J = 2J + 1
    
    Args:
        J: Rotational quantum number
    
    Returns:
        Degeneracy
    """
    if J < 0:
        raise ValueError(f"J must be >= 0, got {J}")
    return 2 * J + 1


def rotational_transition_energy(J_initial: int, B: float) -> float:
    """
    Calculate energy of rotational transition J -> J+1.
    
    DeltaE = 2B(J+1)
    
    Args:
        J_initial: Initial rotational quantum number
        B: Rotational constant (same units as desired output)
    
    Returns:
        Transition energy in same units as B
    """
    if J_initial < 0:
        raise ValueError(f"J must be >= 0, got {J_initial}")
    return 2 * B * (J_initial + 1)


def rotational_transition_frequency(J_initial: int, reduced_mass: float, 
                                     bond_length: float) -> float:
    """
    Calculate frequency of rotational transition J -> J+1.
    
    Args:
        J_initial: Initial rotational quantum number
        reduced_mass: Reduced mass in kg
        bond_length: Bond length in meters
    
    Returns:
        Transition frequency in Hz
    """
    B_hz = rotational_constant(reduced_mass, bond_length, in_cm=False)
    return 2 * B_hz * (J_initial + 1)


# =============================================================================
# HYDROGEN ATOM
# =============================================================================

def hydrogen_energy(n: int, Z: int = 1, in_ev: bool = True) -> float:
    """
    Calculate hydrogen-like atom energy.
    
    E_n = -Z2 x 13.6 eV / n2
    
    Args:
        n: Principal quantum number (n = 1, 2, 3, ...)
        Z: Atomic number (default 1 for hydrogen)
        in_ev: If True, return energy in eV; if False, return in Joules
    
    Returns:
        Energy (negative for bound states)
    
    Raises:
        ValueError: If n < 1 or Z < 1
    """
    if n < 1:
        raise ValueError(f"Principal quantum number n must be >= 1, got {n}")
    if Z < 1:
        raise ValueError(f"Atomic number Z must be >= 1, got {Z}")
    
    # Ground state energy constant
    E_1 = -13.6 * Z**2  # eV
    
    energy_eV = E_1 / n**2
    
    if in_ev:
        return energy_eV
    else:
        return energy_eV * EV_TO_JOULE


def hydrogen_ionization_energy(Z: int = 1, in_ev: bool = True) -> float:
    """
    Calculate ionization energy of hydrogen-like atom.
    
    IE = |E_1| = Z2 x 13.6 eV
    
    Args:
        Z: Atomic number
        in_ev: If True, return in eV
    
    Returns:
        Ionization energy
    """
    return abs(hydrogen_energy(1, Z, in_ev))


def validate_quantum_numbers(n: int, l: int, m_l: int) -> bool:
    """
    Check if a set of quantum numbers is valid for hydrogen atom.
    
    Rules:
    - n >= 1 (positive integer)
    - 0 <= l <= n-1
    - -l <= m_l <= +l
    
    Args:
        n: Principal quantum number
        l: Angular momentum quantum number
        m_l: Magnetic quantum number
    
    Returns:
        True if valid, False otherwise
    """
    if n < 1:
        return False
    if l < 0 or l >= n:
        return False
    if abs(m_l) > l:
        return False
    return True


def angular_momentum_magnitude(l: int) -> float:
    """
    Calculate angular momentum magnitude.
    
    |L| = √(l(l+1)) ℏ
    
    Args:
        l: Angular momentum quantum number
    
    Returns:
        Angular momentum in J·s
    """
    if l < 0:
        raise ValueError(f"l must be >= 0, got {l}")
    return np.sqrt(l * (l + 1)) * REDUCED_PLANCK


def angular_momentum_z_component(m_l: int) -> float:
    """
    Calculate z-component of angular momentum.
    
    L_z = m_l ℏ
    
    Args:
        m_l: Magnetic quantum number
    
    Returns:
        L_z in J·s
    """
    return m_l * REDUCED_PLANCK


def orbital_count(n: int) -> int:
    """
    Calculate total number of orbitals for principal quantum number n.
    
    Total = n2
    
    Args:
        n: Principal quantum number
    
    Returns:
        Number of orbitals
    """
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    return n**2


def electron_capacity(n: int) -> int:
    """
    Calculate maximum electrons in shell n.
    
    Max electrons = 2n2 (2 electrons per orbital)
    
    Args:
        n: Principal quantum number
    
    Returns:
        Maximum number of electrons
    """
    return 2 * orbital_count(n)


def radial_nodes(n: int, l: int) -> int:
    """
    Calculate number of radial nodes in hydrogen orbital.
    
    Radial nodes = n - l - 1
    
    Args:
        n: Principal quantum number
        l: Angular momentum quantum number
    
    Returns:
        Number of radial nodes
    """
    if n < 1:
        raise ValueError(f"n must be >= 1")
    if l < 0 or l >= n:
        raise ValueError(f"l must be in range [0, {n-1}]")
    return n - l - 1


def angular_nodes(l: int) -> int:
    """
    Calculate number of angular nodes in hydrogen orbital.
    
    Angular nodes = l
    
    Args:
        l: Angular momentum quantum number
    
    Returns:
        Number of angular nodes
    """
    if l < 0:
        raise ValueError(f"l must be >= 0")
    return l


def total_nodes(n: int) -> int:
    """
    Calculate total number of nodes in hydrogen orbital.
    
    Total nodes = n - 1
    
    Args:
        n: Principal quantum number
    
    Returns:
        Total number of nodes
    """
    if n < 1:
        raise ValueError(f"n must be >= 1")
    return n - 1


def hydrogen_radial_wavefunction(n: int, l: int, r: Union[float, np.ndarray],
                                  Z: int = 1) -> Union[float, np.ndarray]:
    """
    Calculate radial wavefunction R_{n,l}(r) for hydrogen-like atom.
    
    Uses associated Laguerre polynomials.
    
    Args:
        n: Principal quantum number
        l: Angular momentum quantum number
        r: Radial distance in meters (or Bohr radii)
        Z: Atomic number
    
    Returns:
        Radial wavefunction value
    """
    if not validate_quantum_numbers(n, l, 0):
        raise ValueError(f"Invalid quantum numbers: n={n}, l={l}")
    
    # Convert to dimensionless variable ρ = Zr/a0
    rho = Z * r / BOHR_RADIUS
    
    # Normalization constant
    norm = np.sqrt((2*Z/n/BOHR_RADIUS)**3 * math.factorial(n-l-1) / 
                   (2*n * math.factorial(n+l)))
    
    # Associated Laguerre polynomial
    L = genlaguerre(n-l-1, 2*l+1)(2*rho/n)
    
    return norm * np.exp(-rho/n) * (2*rho/n)**l * L


def radial_distribution_function(n: int, l: int, 
                                  r: Union[float, np.ndarray],
                                  Z: int = 1) -> Union[float, np.ndarray]:
    """
    Calculate radial distribution function.
    
    P(r) = r2 |R_{n,l}(r)|2
    
    Args:
        n: Principal quantum number
        l: Angular momentum quantum number
        r: Radial distance
        Z: Atomic number
    
    Returns:
        Radial distribution function value
    """
    R = hydrogen_radial_wavefunction(n, l, r, Z)
    return r**2 * np.abs(R)**2


def most_probable_radius(n: int, l: int = 0, Z: int = 1) -> float:
    """
    Calculate most probable radius for hydrogen orbital.
    
    For 1s: r_mp = a0/Z
    For 2s: r_mp ~ 5.24 a0/Z (outer maximum)
    For 2p: r_mp = 4a0/Z
    
    Args:
        n: Principal quantum number
        l: Angular momentum quantum number
        Z: Atomic number
    
    Returns:
        Most probable radius in meters
    """
    # Analytical formulas for specific orbitals
    if n == 1 and l == 0:  # 1s
        return BOHR_RADIUS / Z
    elif n == 2 and l == 0:  # 2s (outer maximum)
        return 5.24 * BOHR_RADIUS / Z
    elif n == 2 and l == 1:  # 2p
        return 4 * BOHR_RADIUS / Z
    elif n == 3 and l == 0:  # 3s
        return 13.1 * BOHR_RADIUS / Z
    elif n == 3 and l == 1:  # 3p
        return 12 * BOHR_RADIUS / Z
    elif n == 3 and l == 2:  # 3d
        return 9 * BOHR_RADIUS / Z
    else:
        # General approximation for maximum l
        return n**2 * BOHR_RADIUS / Z


# =============================================================================
# EXPECTATION VALUES AND UNCERTAINTIES
# =============================================================================

def expectation_value(psi_func, operator_func, 
                       x_min: float = -np.inf, x_max: float = np.inf) -> float:
    """
    Calculate expectation value ⟨A⟩ = ∫ψ*Âψ dx.
    
    Args:
        psi_func: Wavefunction (callable)
        operator_func: Operator (callable)
        x_min, x_max: Integration limits
    
    Returns:
        Expectation value
    """
    def integrand(x):
        psi = psi_func(x)
        A_psi = operator_func(psi, x)
        return np.conj(psi) * A_psi
    
    result, _ = integrate.quad(integrand, x_min, x_max)
    return result.real


def expectation_position_box(n: int, L: float) -> float:
    """
    Calculate ⟨x⟩ for particle in a box.
    
    ⟨x⟩ = L/2
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Expectation value of position
    """
    return L / 2


def expectation_x_squared_box(n: int, L: float) -> float:
    """
    Calculate ⟨x2⟩ for particle in a box.
    
    ⟨x2⟩ = L2(1/3 - 1/(2n2pi2))
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Expectation value of x2
    """
    return L**2 * (1/3 - 1/(2 * n**2 * np.pi**2))


def expectation_momentum_box(n: int, L: float) -> float:
    """
    Calculate ⟨p⟩ for particle in a box.
    
    ⟨p⟩ = 0
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Expectation value of momentum (always 0)
    """
    return 0.0


def expectation_p_squared_box(n: int, L: float) -> float:
    """
    Calculate ⟨p2⟩ for particle in a box.
    
    ⟨p2⟩ = n2h2/(4L2) = 2mEₙ
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Expectation value of p2 in (kg·m/s)2
    """
    return n**2 * PLANCK_CONSTANT**2 / (4 * L**2)


def position_uncertainty_box(n: int, L: float) -> float:
    """
    Calculate position uncertainty Deltax for particle in a box.
    
    Deltax = √(⟨x2⟩ - ⟨x⟩2)
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Position uncertainty in meters
    """
    x_avg = expectation_position_box(n, L)
    x2_avg = expectation_x_squared_box(n, L)
    return np.sqrt(x2_avg - x_avg**2)


def momentum_uncertainty_box(n: int, L: float) -> float:
    """
    Calculate momentum uncertainty Deltap for particle in a box.
    
    Deltap = √(⟨p2⟩ - ⟨p⟩2) = √⟨p2⟩ (since ⟨p⟩ = 0)
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Momentum uncertainty in kg·m/s
    """
    p2_avg = expectation_p_squared_box(n, L)
    return np.sqrt(p2_avg)


def uncertainty_product_box(n: int, L: float) -> float:
    """
    Calculate Deltax·Deltap for particle in a box.
    
    Should satisfy: Deltax·Deltap ≥ ℏ/2
    
    Args:
        n: Quantum number
        L: Box length
    
    Returns:
        Uncertainty product in J·s
    """
    dx = position_uncertainty_box(n, L)
    dp = momentum_uncertainty_box(n, L)
    return dx * dp


def heisenberg_limit() -> float:
    """
    Return the Heisenberg uncertainty limit ℏ/2.
    
    Returns:
        ℏ/2 in J·s
    """
    return REDUCED_PLANCK / 2


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def normalize_wavefunction(psi_values: np.ndarray, x_values: np.ndarray) -> np.ndarray:
    """
    Normalize a wavefunction numerically.
    
    Args:
        psi_values: Wavefunction values at x_values
        x_values: Position values
    
    Returns:
        Normalized wavefunction values
    """
    # Integrate |ψ|2 - use trapezoid for numpy 2.0+ compatibility
    try:
        norm_squared = np.trapezoid(np.abs(psi_values)**2, x_values)
    except AttributeError:
        norm_squared = np.trapz(np.abs(psi_values)**2, x_values)
    
    if norm_squared == 0:
        raise ValueError("Wavefunction integrates to zero")
    
    return psi_values / np.sqrt(norm_squared)


def check_normalization(psi_values: np.ndarray, x_values: np.ndarray, 
                         tolerance: float = 1e-6) -> bool:
    """
    Check if a wavefunction is normalized.
    
    Args:
        psi_values: Wavefunction values
        x_values: Position values
        tolerance: Tolerance for |∫|ψ|2 - 1|
    
    Returns:
        True if normalized within tolerance
    """
    norm = np.trapezoid(np.abs(psi_values)**2, x_values) if hasattr(np, 'trapezoid') else np.trapz(np.abs(psi_values)**2, x_values)
    return abs(norm - 1) < tolerance


def wavelength_to_energy(wavelength: float, in_ev: bool = True) -> float:
    """
    Convert wavelength to photon energy.
    
    E = hc/lambda
    
    Args:
        wavelength: Wavelength in meters
        in_ev: If True, return in eV
    
    Returns:
        Photon energy
    """
    energy_J = PLANCK_CONSTANT * SPEED_OF_LIGHT / wavelength
    return energy_J / EV_TO_JOULE if in_ev else energy_J


def energy_to_wavelength(energy: float, in_ev: bool = True) -> float:
    """
    Convert energy to photon wavelength.
    
    lambda = hc/E
    
    Args:
        energy: Energy in eV (or Joules if in_ev=False)
        in_ev: If True, energy is in eV
    
    Returns:
        Wavelength in meters
    """
    energy_J = energy * EV_TO_JOULE if in_ev else energy
    return PLANCK_CONSTANT * SPEED_OF_LIGHT / energy_J


def wavenumber_to_energy(wavenumber: float) -> float:
    """
    Convert wavenumber (cm-1) to energy.
    
    Args:
        wavenumber: Wavenumber in cm-1
    
    Returns:
        Energy in Joules
    """
    return wavenumber * 100 * PLANCK_CONSTANT * SPEED_OF_LIGHT


def energy_to_wavenumber(energy: float, in_joules: bool = True) -> float:
    """
    Convert energy to wavenumber.
    
    Args:
        energy: Energy in Joules (or eV if in_joules=False)
        in_joules: If True, energy is in Joules
    
    Returns:
        Wavenumber in cm-1
    """
    if not in_joules:
        energy = energy * EV_TO_JOULE
    return energy / (100 * PLANCK_CONSTANT * SPEED_OF_LIGHT)


# =============================================================================
# ORBITAL DESIGNATION
# =============================================================================

def l_to_orbital(l: int) -> str:
    """
    Convert angular momentum quantum number to orbital designation.
    
    Args:
        l: Angular momentum quantum number
    
    Returns:
        Orbital letter (s, p, d, f, ...)
    """
    orbitals = ['s', 'p', 'd', 'f', 'g', 'h', 'i', 'k', 'l', 'm']
    if l < 0:
        raise ValueError(f"l must be >= 0")
    if l < len(orbitals):
        return orbitals[l]
    return chr(ord('n') + l - len(orbitals))


def orbital_to_l(orbital: str) -> int:
    """
    Convert orbital designation to angular momentum quantum number.
    
    Args:
        orbital: Orbital letter (s, p, d, f, ...)
    
    Returns:
        Angular momentum quantum number
    """
    orbital_map = {'s': 0, 'p': 1, 'd': 2, 'f': 3, 'g': 4, 'h': 5, 'i': 6}
    orbital = orbital.lower()
    if orbital not in orbital_map:
        raise ValueError(f"Unknown orbital: {orbital}")
    return orbital_map[orbital]


def orbital_name(n: int, l: int) -> str:
    """
    Get orbital name from quantum numbers.
    
    Args:
        n: Principal quantum number
        l: Angular momentum quantum number
    
    Returns:
        Orbital name (e.g., "1s", "2p", "3d")
    """
    return f"{n}{l_to_orbital(l)}"


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == "__main__":
    # Quick test
    print("=== Particle in a Box ===")
    print(f"E1 for electron in 1 nm box: {particle_in_box_energy_ev(1, ELECTRON_MASS, 1e-9):.3f} eV")
    print(f"E2 for electron in 1 nm box: {particle_in_box_energy_ev(2, ELECTRON_MASS, 1e-9):.3f} eV")
    
    print("\n=== Harmonic Oscillator ===")
    k = 500  # N/m typical bond
    mu = reduced_mass_amu(1, 35)  # HCl
    nu = harmonic_oscillator_frequency(k, mu)
    print(f"HCl vibrational frequency: {nu:.2e} Hz")
    print(f"Zero-point energy: {harmonic_oscillator_zero_point_energy(nu, in_ev=True):.4f} eV")
    
    print("\n=== Rigid Rotor ===")
    r = 127e-12  # HCl bond length ~127 pm
    B = rotational_constant(mu, r, in_cm=True)
    print(f"HCl rotational constant: {B:.2f} cm-1")
    print(f"E(J=1) = {rigid_rotor_energy(1, B):.2f} cm-1")
    
    print("\n=== Hydrogen Atom ===")
    print(f"H ground state energy: {hydrogen_energy(1):.2f} eV")
    print(f"H ionization energy: {hydrogen_ionization_energy():.2f} eV")
    print(f"1s most probable radius: {most_probable_radius(1, 0)*1e12:.1f} pm")
    
    print("\n=== Uncertainty ===")
    L = 1e-9  # 1 nm box
    dx = position_uncertainty_box(1, L)
    dp = momentum_uncertainty_box(1, L)
    print(f"Deltax·Deltap for n=1: {uncertainty_product_box(1, L):.3e} J·s")
    print(f"Heisenberg limit ℏ/2: {heisenberg_limit():.3e} J·s")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="angular_momentum_magnitude",
            description="Calculate angular momentum magnitude.",
            input_schema=[
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="angular_momentum_z_component",
            description="Calculate z-component of angular momentum.",
            input_schema=[
            InputSchemaField(name="m_l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="angular_nodes",
            description="Calculate number of angular nodes in hydrogen orbital.",
            input_schema=[
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="check_normalization",
            description="Check if a wavefunction is normalized.",
            input_schema=[
            InputSchemaField(name="psi_values", type="number", required=True),
            InputSchemaField(name="x_values", type="number", required=True),
            InputSchemaField(name="tolerance", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="electron_capacity",
            description="Calculate maximum electrons in shell n.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="energy_to_wavelength",
            description="Convert energy to photon wavelength.",
            input_schema=[
            InputSchemaField(name="energy", type="number", required=True),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="energy_to_wavenumber",
            description="Convert energy to wavenumber.",
            input_schema=[
            InputSchemaField(name="energy", type="number", required=True),
            InputSchemaField(name="in_joules", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="expectation_momentum_box",
            description="Calculate ⟨p⟩ for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="expectation_p_squared_box",
            description="Calculate ⟨p2⟩ for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="expectation_position_box",
            description="Calculate ⟨x⟩ for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="expectation_value",
            description="Calculate expectation value ⟨A⟩ = ∫ψ*Âψ dx.",
            input_schema=[
            InputSchemaField(name="psi_func", type="number", required=True),
            InputSchemaField(name="operator_func", type="number", required=True),
            InputSchemaField(name="x_min", type="number", required=False),
            InputSchemaField(name="x_max", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="expectation_x_squared_box",
            description="Calculate ⟨x2⟩ for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="harmonic_oscillator_energy",
            description="Calculate harmonic oscillator energy.",
            input_schema=[
            InputSchemaField(name="v", type="number", required=True),
            InputSchemaField(name="frequency", type="number", required=True),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="harmonic_oscillator_energy_spacing",
            description="Calculate energy spacing between adjacent levels.",
            input_schema=[
            InputSchemaField(name="frequency", type="number", required=True),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="harmonic_oscillator_frequency",
            description="Calculate vibrational frequency from force constant and reduced mass.",
            input_schema=[
            InputSchemaField(name="force_constant", type="number", required=True),
            InputSchemaField(name="reduced_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="harmonic_oscillator_wavefunction",
            description="Calculate harmonic oscillator wavefunction.",
            input_schema=[
            InputSchemaField(name="v", type="number", required=True),
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="frequency", type="number", required=True),
            InputSchemaField(name="normalized", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="harmonic_oscillator_zero_point_energy",
            description="Calculate zero-point energy of harmonic oscillator.",
            input_schema=[
            InputSchemaField(name="frequency", type="number", required=True),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heisenberg_limit",
            description="Return the Heisenberg uncertainty limit ℏ/2.",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="hydrogen_energy",
            description="Calculate hydrogen-like atom energy.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="Z", type="number", required=False),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="hydrogen_ionization_energy",
            description="Calculate ionization energy of hydrogen-like atom.",
            input_schema=[
            InputSchemaField(name="Z", type="number", required=False),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="hydrogen_radial_wavefunction",
            description="Calculate radial wavefunction R_{n,l}(r) for hydrogen-like atom.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=True),
            InputSchemaField(name="r", type="number", required=True),
            InputSchemaField(name="Z", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="l_to_orbital",
            description="Convert angular momentum quantum number to orbital designation.",
            input_schema=[
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="moment_of_inertia",
            description="Calculate moment of inertia for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="reduced_mass", type="number", required=True),
            InputSchemaField(name="bond_length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="momentum_uncertainty_box",
            description="Calculate momentum uncertainty Deltap for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="most_probable_radius",
            description="Calculate most probable radius for hydrogen orbital.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=False),
            InputSchemaField(name="Z", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="normalize_wavefunction",
            description="Normalize a wavefunction numerically.",
            input_schema=[
            InputSchemaField(name="psi_values", type="number", required=True),
            InputSchemaField(name="x_values", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="orbital_count",
            description="Calculate total number of orbitals for principal quantum number n.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="orbital_name",
            description="Get orbital name from quantum numbers.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="orbital_to_l",
            description="Convert orbital designation to angular momentum quantum number.",
            input_schema=[
            InputSchemaField(name="orbital", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_3d_energy",
            description="Calculate energy for particle in a 3D box.",
            input_schema=[
            InputSchemaField(name="n_x", type="number", required=True),
            InputSchemaField(name="n_y", type="number", required=True),
            InputSchemaField(name="n_z", type="number", required=True),
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="L_x", type="number", required=True),
            InputSchemaField(name="L_y", type="number", required=True),
            InputSchemaField(name="L_z", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_3d_wavefunction",
            description="Calculate wavefunction for particle in a 3D box.",
            input_schema=[
            InputSchemaField(name="n_x", type="number", required=True),
            InputSchemaField(name="n_y", type="number", required=True),
            InputSchemaField(name="n_z", type="number", required=True),
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="y", type="number", required=True),
            InputSchemaField(name="z", type="number", required=True),
            InputSchemaField(name="L_x", type="number", required=True),
            InputSchemaField(name="L_y", type="number", required=True),
            InputSchemaField(name="L_z", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_degeneracy",
            description="Calculate degeneracy for particle in a cubic 3D box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="cubic", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_energy",
            description="Calculate the energy of a particle in a 1D box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_energy_ev",
            description="Calculate particle in box energy in electron volts.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_probability",
            description="Calculate probability density |ψ|2 for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_in_box_wavefunction",
            description="Calculate the wavefunction for a particle in a 1D box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="length", type="number", required=True),
            InputSchemaField(name="normalized", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="position_uncertainty_box",
            description="Calculate position uncertainty Deltax for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="radial_distribution_function",
            description="Calculate radial distribution function.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=True),
            InputSchemaField(name="r", type="number", required=True),
            InputSchemaField(name="Z", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="radial_nodes",
            description="Calculate number of radial nodes in hydrogen orbital.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reduced_mass",
            description="Calculate reduced mass for a two-body system.",
            input_schema=[
            InputSchemaField(name="m1", type="number", required=True),
            InputSchemaField(name="m2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reduced_mass_amu",
            description="Calculate reduced mass given atomic mass units.",
            input_schema=[
            InputSchemaField(name="m1_amu", type="number", required=True),
            InputSchemaField(name="m2_amu", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rigid_rotor_degeneracy",
            description="Calculate degeneracy of rotational level J.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rigid_rotor_energy",
            description="Calculate rigid rotor energy.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="in_cm", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rigid_rotor_energy_joules",
            description="Calculate rigid rotor energy in Joules.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="reduced_mass", type="number", required=True),
            InputSchemaField(name="bond_length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_constant",
            description="Calculate rotational constant B.",
            input_schema=[
            InputSchemaField(name="reduced_mass", type="number", required=True),
            InputSchemaField(name="bond_length", type="number", required=True),
            InputSchemaField(name="in_cm", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_transition_energy",
            description="Calculate energy of rotational transition J -> J+1.",
            input_schema=[
            InputSchemaField(name="J_initial", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_transition_frequency",
            description="Calculate frequency of rotational transition J -> J+1.",
            input_schema=[
            InputSchemaField(name="J_initial", type="number", required=True),
            InputSchemaField(name="reduced_mass", type="number", required=True),
            InputSchemaField(name="bond_length", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="total_nodes",
            description="Calculate total number of nodes in hydrogen orbital.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="uncertainty_product_box",
            description="Calculate Deltax·Deltap for particle in a box.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="validate_quantum_numbers",
            description="Check if a set of quantum numbers is valid for hydrogen atom.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=True),
            InputSchemaField(name="m_l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavelength_to_energy",
            description="Convert wavelength to photon energy.",
            input_schema=[
            InputSchemaField(name="wavelength", type="number", required=True),
            InputSchemaField(name="in_ev", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavenumber_to_energy",
            description="Convert wavenumber (cm-1) to energy.",
            input_schema=[
            InputSchemaField(name="wavenumber", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
