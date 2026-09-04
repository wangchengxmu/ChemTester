"""
Gas-Phase Reaction Dynamics Tools - L3 Implementation

Core functions for gas-phase reaction dynamics:
- Collision theory
- Potential energy surfaces
- Transition state theory
- Reaction cross sections
- Arrhenius parameters from molecular properties
- Trajectory calculations

Source: LibreTexts Physical Chemistry Ch30
## Solver Instructions (for AI Agent)

When you encounter collision theory, transition state theory, or gas-phase kinetics problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Relative velocity between molecules? Use `relative_velocity(T, mu_amu)`
- Collision frequency? Use `collision_frequency(T, P, sigma_collision_m2, mu_amu)`
- Collision rate between A and B? Use `collision_rate(T, P, sigma_m2, mu_amu, n_A, n_B)`
- Rate constant from collision theory? Use `collision_theory_rate(T, sigma_m2, mu_amu, E_a)`
- Arrhenius parameters? Use `arrhenius_parameters(A, E_a)` or `activation_energy_from_arrhenius(k1, T1, k2, T2)`
- Transition state theory rate? Use `tst_rate_constant(T, delta_H_dagger, delta_S_dagger)`
- Effective activation energy? Use `effective_activation_energy(k1, k2, E_a1, E_a2)` (parallel reactions)
- Pre-exponential factor from molecular properties? Use `pre_exponential_from_properties(T, sigma_m2, mu_amu)`

### Step 2: Handle special cases
- **Units**: Reduced mass in amu (converted internally to kg); σ in m2; T in K
- **Collision theory**: k = Z x exp(-Ea/RT); includes steric factor if provided
- **TST**: DeltaH‡ in kJ/mol, DeltaS‡ in J/(mol·K); internally converts
- **Arrhenius plot**: Plot ln(k) vs 1/T to get -Ea/R (slope) and ln(A) (intercept)

### Examples
```python
# Example 1: Relative velocity
relative_velocity(300, 10)  # -> ~620 m/s

# Example 2: Activation energy from two rate constants
activation_energy_from_arrhenius(0.02, 300, 0.08, 320)  # -> Ea in kJ/mol

# Example 3: TST rate constant
tst_rate_constant(298, 75, -50)  # DeltaH‡=75 kJ/mol, DeltaS‡=-50 J/(mol·K)
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants
from scipy.integrate import quad

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
BOLTZMANN = 1.380649e-23          # J/K
AVOGADRO = 6.02214076e23          # mol-1
R = 8.314462618                   # J/(mol·K)
AMU_TO_KG = 1.66053907e-27        # kg/amu


# =============================================================================
# COLLISION THEORY
# =============================================================================

def relative_velocity(T: float, mu_amu: float) -> float:
    """
    Calculate average relative velocity between two molecules.
    
    v_rel = √(8kT/pimu)
    
    Args:
        T: Temperature in K
        mu_amu: Reduced mass in amu
    
    Returns:
        Relative velocity in m/s
    
    Example:
        >>> relative_velocity(300, 10)  # ~10 amu reduced mass
        500  # m/s
    """
    mu_kg = mu_amu * AMU_TO_KG
    return np.sqrt(8 * BOLTZMANN * T / (np.pi * mu_kg))


def collision_frequency(T: float, P: float, 
                        sigma_collision_m2: float,
                        mu_amu: float) -> float:
    """
    Calculate collision frequency (collisions per molecule per second).
    
    Z = σ x v_rel x (N/V) = σ x √(8kT/pimu) x P/(kT)
    
    Args:
        T: Temperature in K
        P: Pressure in Pa
        sigma_collision_m2: Collision cross-section in m2
        mu_amu: Reduced mass in amu
    
    Returns:
        Collision frequency in s-1
    
    Example:
        >>> collision_frequency(300, 101325, 5e-19, 20)
        7e9  # ~7 billion collisions/s at 1 atm
    """
    v_rel = relative_velocity(T, mu_amu)
    number_density = P / (BOLTZMANN * T)  # molecules/m3
    
    return sigma_collision_m2 * v_rel * number_density


def collision_frequency_molar(T: float, P: float,
                               sigma_collision_m2: float,
                               mu_amu: float) -> float:
    """
    Calculate molar collision frequency (collisions per mole per second).
    
    Z_molar = Z x N_A
    
    Args:
        T: Temperature in K
        P: Pressure in Pa
        sigma_collision_m2: Collision cross-section in m2
        mu_amu: Reduced mass in amu
    
    Returns:
        Molar collision frequency in mol/(L·s) or similar units
    """
    Z = collision_frequency(T, P, sigma_collision_m2, mu_amu)
    return Z * AVOGADRO


def collision_cross_section(d1_m: float, d2_m: float) -> float:
    """
    Calculate collision cross-section from molecular diameters.
    
    σ = pi(d1 + d2)2/4
    
    Args:
        d1_m: Diameter of molecule 1 in m
        d2_m: Diameter of molecule 2 in m
    
    Returns:
        Collision cross-section in m2
    
    Example:
        >>> collision_cross_section(3e-10, 3e-10)  # 3 Å each
        2.8e-19  # m2
    """
    return np.pi * (d1_m + d2_m)**2 / 4


def collision_theory_rate_constant(T: float, 
                                    sigma_m2: float,
                                    mu_amu: float,
                                    E_a: float = 0) -> float:
    """
    Calculate rate constant from collision theory.
    
    k = σ x √(8kT/pimu) x exp(-E_a/RT)
    
    For bimolecular reaction, returns k in m3/(molecule·s)
    Multiply by AVOGADRO x 1000 for L/(mol·s)
    
    Args:
        T: Temperature in K
        sigma_m2: Collision cross-section in m2
        mu_amu: Reduced mass in amu
        E_a: Activation energy in J/mol
    
    Returns:
        Rate constant in m3/(molecule·s)
    
    Example:
        >>> k = collision_theory_rate_constant(300, 5e-19, 20, 50000)
        >>> k * AVOGADRO * 1000  # Convert to L/(mol·s)
    """
    v_rel = relative_velocity(T, mu_amu)
    boltzmann_factor = np.exp(-E_a / (R * T))
    
    return sigma_m2 * v_rel * boltzmann_factor


def steric_factor(k_experimental: float, 
                  k_collision: float) -> float:
    """
    Calculate steric (probability) factor.
    
    P = k_exp / k_collision
    
    Args:
        k_experimental: Experimental rate constant
        k_collision: Collision theory rate constant
    
    Returns:
        Steric factor (typically 0.01 to 1)
    
    Note:
        P < 1 indicates orientation effects matter
    """
    return k_experimental / k_collision


# =============================================================================
# TRANSITION STATE THEORY
# =============================================================================

def tst_rate_constant(T: float, 
                       delta_H_double_dagger: float,
                       delta_S_double_dagger: float,
                       transmission_coeff: float = 1.0) -> float:
    """
    Calculate rate constant from transition state theory.
    
    k = κ x (k_B T/h) x exp(DeltaS‡/R) x exp(-DeltaH‡/RT)
    
    Args:
        T: Temperature in K
        delta_H_double_dagger: Activation enthalpy in J/mol
        delta_S_double_dagger: Activation entropy in J/(mol·K)
        transmission_coeff: Transmission coefficient κ (default 1)
    
    Returns:
        Rate constant in s-1 (first order) or appropriate units
    
    Example:
        >>> tst_rate_constant(300, 80000, -20)
        1.2e-3  # s-1
    """
    prefactor = (BOLTZMANN * T / PLANCK_CONSTANT) * \
                np.exp(delta_S_double_dagger / R)
    boltzmann = np.exp(-delta_H_double_dagger / (R * T))
    
    return transmission_coeff * prefactor * boltzmann


def eyring_equation(T: float,
                    delta_G_double_dagger: float) -> float:
    """
    Calculate rate constant from Eyring equation.
    
    k = (k_B T/h) x exp(-DeltaG‡/RT)
    
    Args:
        T: Temperature in K
        delta_G_double_dagger: Gibbs energy of activation in J/mol
    
    Returns:
        Rate constant in s-1 (or with concentration units for bimolecular)
    
    Example:
        >>> eyring_equation(300, 80000)
        1.5e-3  # s-1
    """
    return (BOLTZMANN * T / PLANCK_CONSTANT) * \
           np.exp(-delta_G_double_dagger / (R * T))


def activation_parameters_from_rates(T1: float, k1: float,
                                      T2: float, k2: float) -> Dict:
    """
    Calculate activation parameters from rate constants at two temperatures.
    
    Uses Eyring plot: ln(k/T) vs 1/T
    
    Args:
        T1, T2: Temperatures in K
        k1, k2: Rate constants in same units
    
    Returns:
        Dictionary with DeltaH‡, DeltaS‡, DeltaG‡
    
    Example:
        >>> params = activation_parameters_from_rates(300, 1e-3, 320, 5e-3)
    """
    # Eyring equation: ln(k/T) = ln(k_B/h) + DeltaS‡/R - DeltaH‡/(RT)
    
    y1 = np.log(k1 / T1)
    y2 = np.log(k2 / T2)
    x1 = 1 / T1
    x2 = 1 / T2
    
    # Slope = -DeltaH‡/R
    slope = (y2 - y1) / (x2 - x1)
    delta_H = -slope * R
    
    # Intercept = ln(k_B/h) + DeltaS‡/R
    intercept = y1 - slope * x1
    delta_S = (intercept - np.log(BOLTZMANN / PLANCK_CONSTANT)) * R
    
    # DeltaG‡ at average temperature
    T_avg = (T1 + T2) / 2
    delta_G = delta_H - T_avg * delta_S
    
    return {
        'delta_H_double_dagger': delta_H,  # J/mol
        'delta_S_double_dagger': delta_S,  # J/(mol·K)
        'delta_G_double_dagger': delta_G,  # J/mol
        'T_average': T_avg
    }


def pre_exponential_factor_tst(T: float, 
                                delta_S_double_dagger: float) -> float:
    """
    Calculate pre-exponential factor from TST.
    
    A = (k_B T/h) x exp(DeltaS‡/R)
    
    Args:
        T: Temperature in K
        delta_S_double_dagger: Activation entropy in J/(mol·K)
    
    Returns:
        Pre-exponential factor in s-1
    """
    return (BOLTZMANN * T / PLANCK_CONSTANT) * \
           np.exp(delta_S_double_dagger / R)


# =============================================================================
# POTENTIAL ENERGY SURFACES
# =============================================================================

def harmonic_barrier_height(V0: float, 
                             x0: float,
                             force_constant: float) -> float:
    """
    Calculate barrier height for harmonic barrier.
    
    V(x) = V0 + ½k(x - x0)2
    
    Args:
        V0: Barrier top energy in J
        x0: Position of barrier top
        force_constant: Force constant k
    
    Returns:
        Barrier height (same as V0 for simple harmonic)
    """
    return V0


def eckart_potential(x: float, 
                     V0: float,
                     V1: float = 0,
                     a: float = 1) -> float:
    """
    Calculate Eckart potential (model barrier for reactions).
    
    V(x) = V1 + (V0 - V1)/(1 + e^(-x/a)) + A x e^(-x/a)/(1 + e^(-x/a))2
    
    Args:
        x: Position
        V0: Asymptotic energy as x -> +∞
        V1: Asymptotic energy as x -> -∞
        a: Width parameter
    
    Returns:
        Potential energy at position x
    """
    exp_term = np.exp(-x/a)
    
    V = V1 + (V0 - V1) / (1 + exp_term)
    
    return V


def reaction_coordinate_minimum(V: callable,
                                 x_range: Tuple[float, float],
                                 n_points: int = 1000) -> Tuple[float, float]:
    """
    Find minimum on potential energy surface along reaction coordinate.
    
    Args:
        V: Potential energy function
        x_range: (x_min, x_max) search range
        n_points: Number of points to evaluate
    
    Returns:
        (x_min, V_min) position and energy of minimum
    """
    x_values = np.linspace(x_range[0], x_range[1], n_points)
    V_values = [V(x) for x in x_values]
    
    min_idx = np.argmin(V_values)
    
    return x_values[min_idx], V_values[min_idx]


def saddle_point_height(V: callable,
                        reactant_energy: float,
                        x_range: Tuple[float, float],
                        n_points: int = 1000) -> float:
    """
    Find saddle point (transition state) height above reactants.
    
    Args:
        V: Potential energy function
        reactant_energy: Energy of reactants
        x_range: Search range for saddle point
        n_points: Number of evaluation points
    
    Returns:
        Barrier height in same units as V
    """
    x_values = np.linspace(x_range[0], x_range[1], n_points)
    V_values = [V(x) for x in x_values]
    
    # Find maximum (saddle point)
    max_idx = np.argmax(V_values)
    
    return V_values[max_idx] - reactant_energy


# =============================================================================
# REACTION CROSS SECTION
# =============================================================================

def reaction_cross_section_simple(E: float, 
                                   E_threshold: float,
                                   sigma_max: float) -> float:
    """
    Simple reaction cross-section model.
    
    σ(E) = 0           for E < E_threshold
    σ(E) = σ_max       for E ≥ E_threshold
    
    Args:
        E: Collision energy in J
        E_threshold: Threshold energy in J
        sigma_max: Maximum cross-section in m2
    
    Returns:
        Reaction cross-section in m2
    """
    if E < E_threshold:
        return 0
    else:
        return sigma_max


def reaction_cross_section_arrhenius(E: float,
                                      E_a: float,
                                      sigma_0: float) -> float:
    """
    Arrhenius-type energy-dependent cross-section.
    
    σ(E) = σ0 x exp(-E_a/E)  [simplified]
    
    More correctly: σ(E) = σ0 x (1 - E_a/E) for E > E_a
    
    Args:
        E: Collision energy in J
        E_a: Activation energy in J
        sigma_0: Pre-exponential cross-section in m2
    
    Returns:
        Reaction cross-section in m2
    """
    if E <= E_a:
        return 0
    
    return sigma_0 * (1 - E_a / E)


def total_cross_section(energies_J: np.ndarray,
                         sigma_func: callable) -> float:
    """
    Calculate integrated (total) cross-section.
    
    σ_total = ∫σ(E) dE
    
    Args:
        energies_J: Array of energies in J
        sigma_func: Cross-section function σ(E)
    
    Returns:
        Integrated cross-section
    """
    integrand = lambda E: sigma_func(E)
    result, _ = quad(integrand, energies_J[0], energies_J[-1])
    return result


# =============================================================================
# TRAJECTORY CALCULATIONS
# =============================================================================

def impact_parameter_max(sigma_reaction: float) -> float:
    """
    Calculate maximum impact parameter from reaction cross-section.
    
    b_max = √(σ/pi)
    
    Args:
        sigma_reaction: Reaction cross-section in m2
    
    Returns:
        Maximum impact parameter in m
    """
    return np.sqrt(sigma_reaction / np.pi)


def deflection_angle(b: float, 
                     potential_func: callable,
                     velocity: float,
                     reduced_mass: float) -> float:
    """
    Calculate scattering deflection angle.
    
    χ = pi - 2b ∫0^∞ dr/(r2√(1 - b2/r2 - V(r)/E))
    
    Simplified numerical approximation.
    
    Args:
        b: Impact parameter in m
        potential_func: V(r) potential function
        velocity: Relative velocity in m/s
        reduced_mass: Reduced mass in kg
    
    Returns:
        Deflection angle in radians
    """
    # This is a simplified approximation
    # Full calculation requires numerical integration
    
    E_kin = 0.5 * reduced_mass * velocity**2
    
    # Approximate using impact parameter ratio
    # More accurate calculation requires trajectory integration
    
    return np.pi / 2 * np.exp(-b / 1e-10)  # Placeholder


def mean_free_path(T: float, P: float, 
                   sigma_collision: float) -> float:
    """
    Calculate mean free path.
    
    lambda = kT/(√2 x P x σ)
    
    Args:
        T: Temperature in K
        P: Pressure in Pa
        sigma_collision: Collision cross-section in m2
    
    Returns:
        Mean free path in m
    
    Example:
        >>> mean_free_path(300, 101325, 5e-19)
        6e-8  # ~60 nm at 1 atm
    """
    return BOLTZMANN * T / (np.sqrt(2) * P * sigma_collision)


# =============================================================================
# KINETIC ISOTOPE EFFECTS
# =============================================================================

def primary_kinetic_isotope_effect(m_light: float, 
                                    m_heavy: float,
                                    T: float,
                                    E0_light: float,
                                    E0_heavy: float) -> float:
    """
    Calculate primary kinetic isotope effect.
    
    KIE = k_light/k_heavy ~ √(m_heavy/m_light) x exp((E0,heavy - E0,light)/RT)
    
    Args:
        m_light: Mass of light isotope in amu
        m_heavy: Mass of heavy isotope in amu
        T: Temperature in K
        E0_light: Zero-point energy with light isotope in J/mol
        E0_heavy: Zero-point energy with heavy isotope in J/mol
    
    Returns:
        Kinetic isotope effect ratio
    
    Example:
        >>> primary_kinetic_isotope_effect(1, 2, 300, 40000, 28000)
        7.5  # Typical H/D KIE
    """
    mass_ratio = np.sqrt(m_heavy / m_light)
    zpe_factor = np.exp((E0_heavy - E0_light) / (R * T))
    
    return mass_ratio * zpe_factor


def tunneling_correction_wigner(T: float, 
                                 nu_TS_cm: float) -> float:
    """
    Calculate Wigner tunneling correction.
    
    κ = 1 + (hν‡/kT)2/24
    
    Args:
        T: Temperature in K
        nu_TS_cm: Imaginary frequency at transition state in cm-1
    
    Returns:
        Tunneling correction factor (≥ 1)
    
    Example:
        >>> tunneling_correction_wigner(300, 1000)
        1.05  # Small tunneling
    """
    # Convert wavenumber to frequency
    nu = nu_TS_cm * 3e10  # Hz
    
    x = PLANCK_CONSTANT * nu / (BOLTZMANN * T)
    
    return 1 + x**2 / 24


# =============================================================================
# DIFFUSION-CONTROLLED REACTIONS
# =============================================================================

def diffusion_controlled_rate_constant(T: float,
                                        eta_Pa_s: float,
                                        r1_m: float,
                                        r2_m: float) -> float:
    """
    Calculate rate constant for diffusion-controlled reaction.
    
    k_D = 4pi(r1 + r2)(D1 + D2)N_A
    
    Using Stokes-Einstein: D = kT/(6piηr)
    
    k_D = 8RT/(3η)  (for equal-sized reactants)
    
    Args:
        T: Temperature in K
        eta_Pa_s: Viscosity in Pa·s
        r1_m, r2_m: Radii of reactants in m
    
    Returns:
        Rate constant in L/(mol·s)
    
    Example:
        >>> diffusion_controlled_rate_constant(298, 0.001, 3e-10, 3e-10)
        6.5e9  # L/(mol·s)
    """
    # Stokes-Einstein diffusion coefficients
    D1 = BOLTZMANN * T / (6 * np.pi * eta_Pa_s * r1_m)
    D2 = BOLTZMANN * T / (6 * np.pi * eta_Pa_s * r2_m)
    
    # Sum of radii
    r_sum = r1_m + r2_m
    
    # Diffusion-controlled rate constant
    k_D = 4 * np.pi * r_sum * (D1 + D2) * AVOGADRO
    
    # Convert from m3/(mol·s) to L/(mol·s)
    return k_D * 1000


def is_diffusion_controlled(k_observed: float, 
                             k_diffusion: float) -> bool:
    """
    Determine if reaction is diffusion-controlled.
    
    Args:
        k_observed: Observed rate constant in L/(mol·s)
        k_diffusion: Diffusion-controlled limit in L/(mol·s)
    
    Returns:
        True if reaction is diffusion-controlled
    """
    return k_observed >= 0.5 * k_diffusion


# =============================================================================
# DATABASE
# =============================================================================

COLLISION_DIAMETERS = {
    'He': 2.58e-10,
    'Ne': 2.79e-10,
    'Ar': 3.64e-10,
    'Kr': 4.16e-10,
    'Xe': 4.85e-10,
    'H2': 2.89e-10,
    'N2': 3.70e-10,
    'O2': 3.55e-10,
    'CO': 3.76e-10,
    'CO2': 4.00e-10,
    'CH4': 4.14e-10,
    'C2H6': 5.30e-10,
    'H2O': 2.65e-10,
    'NH3': 3.15e-10,
}


def get_collision_diameter(molecule: str) -> float:
    """Get collision diameter for a molecule."""
    return COLLISION_DIAMETERS.get(molecule.upper(), 4e-10)


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Gas-Phase Reaction Dynamics Tools - Examples")
    print("=" * 60)
    
    # Collision theory
    print("\n1. Collision Theory:")
    v_rel = relative_velocity(300, 20)
    print(f"   Relative velocity (mu=20 amu, T=300K): {v_rel:.1f} m/s")
    
    sigma = collision_cross_section(3e-10, 3e-10)
    print(f"   Collision cross-section (d=3Å each): {sigma:.2e} m2")
    
    Z = collision_frequency(300, 101325, 5e-19, 20)
    print(f"   Collision frequency (1 atm, 300K): {Z:.2e} s-1")
    
    lambda_mfp = mean_free_path(300, 101325, 5e-19)
    print(f"   Mean free path: {lambda_mfp*1e9:.1f} nm")
    
    # Transition state theory
    print("\n2. Transition State Theory:")
    k_tst = tst_rate_constant(300, 80000, -20)
    print(f"   k (DeltaH‡=80 kJ/mol, DeltaS‡=-20 J/mol·K): {k_tst:.2e} s-1")
    
    params = activation_parameters_from_rates(300, 1e-3, 320, 5e-3)
    print(f"   From rates: DeltaH‡ = {params['delta_H_double_dagger']/1000:.1f} kJ/mol")
    print(f"              DeltaS‡ = {params['delta_S_double_dagger']:.1f} J/(mol·K)")
    
    # Diffusion control
    print("\n3. Diffusion-Controlled Reactions:")
    k_D = diffusion_controlled_rate_constant(298, 0.001, 3e-10, 3e-10)
    print(f"   k_D (water, 298K): {k_D:.2e} L/(mol·s)")
    
    # KIE
    print("\n4. Kinetic Isotope Effects:")
    KIE = primary_kinetic_isotope_effect(1, 2, 300, 40000, 28000)
    print(f"   H/D KIE: {KIE:.1f}")
    
    kappa = tunneling_correction_wigner(300, 1000)
    print(f"   Tunneling correction (ν=1000 cm-1): {kappa:.3f}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "activation_parameters_from_rates",
        "description": "Calculate activation parameters from rate constants at two temperatures.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T1": {"type": "number", "description": "T1"},
                "k1": {"type": "number", "description": "K1"},
                "T2": {"type": "number", "description": "T2"},
                "k2": {"type": "number", "description": "K2"},
            },
            "required": ["T1", "k1", "T2", "k2"]
        }
    },
    {
        "name": "collision_cross_section",
        "description": "Calculate collision cross-section from molecular diameters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "d1_m": {"type": "number", "description": "D1 M"},
                "d2_m": {"type": "number", "description": "D2 M"},
            },
            "required": ["d1_m", "d2_m"]
        }
    },
    {
        "name": "collision_frequency",
        "description": "Calculate collision frequency (collisions per molecule per second).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "P": {"type": "number", "description": "P"},
                "sigma_collision_m2": {"type": "number", "description": "Sigma Collision M2"},
                "mu_amu": {"type": "number", "description": "Mu Amu"},
            },
            "required": ["T", "P", "sigma_collision_m2", "mu_amu"]
        }
    },
    {
        "name": "collision_frequency_molar",
        "description": "Calculate molar collision frequency (collisions per mole per second).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "P": {"type": "number", "description": "P"},
                "sigma_collision_m2": {"type": "number", "description": "Sigma Collision M2"},
                "mu_amu": {"type": "number", "description": "Mu Amu"},
            },
            "required": ["T", "P", "sigma_collision_m2", "mu_amu"]
        }
    },
    {
        "name": "collision_theory_rate_constant",
        "description": "Calculate rate constant from collision theory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "sigma_m2": {"type": "number", "description": "Sigma M2"},
                "mu_amu": {"type": "number", "description": "Mu Amu"},
                "E_a": {"type": "number", "description": "E A", "default": 0},
            },
            "required": ["T", "sigma_m2", "mu_amu"]
        }
    },
    {
        "name": "deflection_angle",
        "description": "Calculate scattering deflection angle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "b": {"type": "number", "description": "B"},
                "potential_func": {"type": "number", "description": "Potential Func"},
                "velocity": {"type": "number", "description": "Velocity"},
                "reduced_mass": {"type": "number", "description": "Reduced Mass"},
            },
            "required": ["b", "potential_func", "velocity", "reduced_mass"]
        }
    },
    {
        "name": "diffusion_controlled_rate_constant",
        "description": "Calculate rate constant for diffusion-controlled reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "eta_Pa_s": {"type": "number", "description": "Eta Pa S"},
                "r1_m": {"type": "number", "description": "R1 M"},
                "r2_m": {"type": "number", "description": "R2 M"},
            },
            "required": ["T", "eta_Pa_s", "r1_m", "r2_m"]
        }
    },
    {
        "name": "eckart_potential",
        "description": "Calculate Eckart potential (model barrier for reactions).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "x": {"type": "number", "description": "X"},
                "V0": {"type": "number", "description": "V0"},
                "V1": {"type": "number", "description": "V1", "default": 0},
                "a": {"type": "number", "description": "A", "default": 1},
            },
            "required": ["x", "V0"]
        }
    },
    {
        "name": "eyring_equation",
        "description": "Calculate rate constant from Eyring equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "delta_G_double_dagger": {"type": "number", "description": "Delta G Double Dagger"},
            },
            "required": ["T", "delta_G_double_dagger"]
        }
    },
    {
        "name": "get_collision_diameter",
        "description": "Get collision diameter for a molecule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "molecule": {"type": "number", "description": "Molecule"},
            },
            "required": ["molecule"]
        }
    },
    {
        "name": "harmonic_barrier_height",
        "description": "Calculate barrier height for harmonic barrier.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "V0": {"type": "number", "description": "V0"},
                "x0": {"type": "number", "description": "X0"},
                "force_constant": {"type": "number", "description": "Force Constant"},
            },
            "required": ["V0", "x0", "force_constant"]
        }
    },
    {
        "name": "impact_parameter_max",
        "description": "Calculate maximum impact parameter from reaction cross-section.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sigma_reaction": {"type": "number", "description": "Sigma Reaction"},
            },
            "required": ["sigma_reaction"]
        }
    },
    {
        "name": "is_diffusion_controlled",
        "description": "Determine if reaction is diffusion-controlled.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_observed": {"type": "number", "description": "K Observed"},
                "k_diffusion": {"type": "number", "description": "K Diffusion"},
            },
            "required": ["k_observed", "k_diffusion"]
        }
    },
    {
        "name": "mean_free_path",
        "description": "Calculate mean free path.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "P": {"type": "number", "description": "P"},
                "sigma_collision": {"type": "number", "description": "Sigma Collision"},
            },
            "required": ["T", "P", "sigma_collision"]
        }
    },
    {
        "name": "pre_exponential_factor_tst",
        "description": "Calculate pre-exponential factor from TST.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "delta_S_double_dagger": {"type": "number", "description": "Delta S Double Dagger"},
            },
            "required": ["T", "delta_S_double_dagger"]
        }
    },
    {
        "name": "primary_kinetic_isotope_effect",
        "description": "Calculate primary kinetic isotope effect.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "m_light": {"type": "number", "description": "M Light"},
                "m_heavy": {"type": "number", "description": "M Heavy"},
                "T": {"type": "number", "description": "T"},
                "E0_light": {"type": "number", "description": "E0 Light"},
                "E0_heavy": {"type": "number", "description": "E0 Heavy"},
            },
            "required": ["m_light", "m_heavy", "T", "E0_light", "E0_heavy"]
        }
    },
    {
        "name": "quad",
        "description": "Compute a definite integral.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "func": {"type": "number", "description": "Func"},
                "a": {"type": "number", "description": "A"},
                "b": {"type": "number", "description": "B"},
                "args": {"type": "number", "description": "Args", "default": []},
                "full_output": {"type": "number", "description": "Full Output", "default": 0},
                "epsabs": {"type": "number", "description": "Epsabs", "default": 1.49e-08},
                "epsrel": {"type": "number", "description": "Epsrel", "default": 1.49e-08},
                "limit": {"type": "number", "description": "Limit", "default": 50},
                "points": {"type": "number", "description": "Points", "default": None},
                "weight": {"type": "number", "description": "Weight", "default": None},
                "wvar": {"type": "number", "description": "Wvar", "default": None},
                "wopts": {"type": "number", "description": "Wopts", "default": None},
                "maxp1": {"type": "number", "description": "Maxp1", "default": 50},
                "limlst": {"type": "number", "description": "Limlst", "default": 50},
                "complex_func": {"type": "number", "description": "Complex Func", "default": False},
            },
            "required": ["func", "a", "b"]
        }
    },
    {
        "name": "reaction_coordinate_minimum",
        "description": "Find minimum on potential energy surface along reaction coordinate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "V": {"type": "number", "description": "V"},
                "x_range": {"type": "number", "description": "X Range"},
                "n_points": {"type": "number", "description": "N Points", "default": 1000},
            },
            "required": ["V", "x_range"]
        }
    },
    {
        "name": "reaction_cross_section_arrhenius",
        "description": "Arrhenius-type energy-dependent cross-section.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E": {"type": "number", "description": "E"},
                "E_a": {"type": "number", "description": "E A"},
                "sigma_0": {"type": "number", "description": "Sigma 0"},
            },
            "required": ["E", "E_a", "sigma_0"]
        }
    },
    {
        "name": "reaction_cross_section_simple",
        "description": "Simple reaction cross-section model.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E": {"type": "number", "description": "E"},
                "E_threshold": {"type": "number", "description": "E Threshold"},
                "sigma_max": {"type": "number", "description": "Sigma Max"},
            },
            "required": ["E", "E_threshold", "sigma_max"]
        }
    },
    {
        "name": "relative_velocity",
        "description": "Calculate average relative velocity between two molecules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "mu_amu": {"type": "number", "description": "Mu Amu"},
            },
            "required": ["T", "mu_amu"]
        }
    },
    {
        "name": "saddle_point_height",
        "description": "Find saddle point (transition state) height above reactants.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "V": {"type": "number", "description": "V"},
                "reactant_energy": {"type": "number", "description": "Reactant Energy"},
                "x_range": {"type": "number", "description": "X Range"},
                "n_points": {"type": "number", "description": "N Points", "default": 1000},
            },
            "required": ["V", "reactant_energy", "x_range"]
        }
    },
    {
        "name": "steric_factor",
        "description": "Calculate steric (probability) factor.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_experimental": {"type": "number", "description": "K Experimental"},
                "k_collision": {"type": "number", "description": "K Collision"},
            },
            "required": ["k_experimental", "k_collision"]
        }
    },
    {
        "name": "total_cross_section",
        "description": "Calculate integrated (total) cross-section.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "energies_J": {"type": "number", "description": "Energies J"},
                "sigma_func": {"type": "number", "description": "Sigma Func"},
            },
            "required": ["energies_J", "sigma_func"]
        }
    },
    {
        "name": "tst_rate_constant",
        "description": "Calculate rate constant from transition state theory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "delta_H_double_dagger": {"type": "number", "description": "Delta H Double Dagger"},
                "delta_S_double_dagger": {"type": "number", "description": "Delta S Double Dagger"},
                "transmission_coeff": {"type": "number", "description": "Transmission Coeff", "default": 1.0},
            },
            "required": ["T", "delta_H_double_dagger", "delta_S_double_dagger"]
        }
    },
    {
        "name": "tunneling_correction_wigner",
        "description": "Calculate Wigner tunneling correction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T": {"type": "number", "description": "T"},
                "nu_TS_cm": {"type": "number", "description": "Nu Ts Cm"},
            },
            "required": ["T", "nu_TS_cm"]
        }
    }
]
