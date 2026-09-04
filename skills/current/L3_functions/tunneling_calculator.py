"""
tunneling_calculator.py - Quantum Mechanical Tunneling Calculations
L3 Implementation for chem.quantum_tunneling

Functions:
    transmission_rectangular()  - Exact rectangular barrier transmission
    decay_constant()            - κ inside a rectangular barrier
    transmission_wkb()          - WKB approximation for general barriers
    transmission_wkb_quad()     - WKB using scipy.integrate.quad
    transmission_eckart()       - Eckart barrier transmission
    wigner_tunneling_correction() - Wigner κ = 1 + (hν‡/24kT)2
    bell_tunneling_correction() - Bell tunneling correction to rate constants
    isotope_tunneling_ratio()   - H/D tunneling KIE prediction
    harmonic_oscillator_penetration() - Classically forbidden probability for QHO
"""

## Solver Instructions (for AI Agent)

# When you encounter **quantum tunneling** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Rectangular barrier transmission: `transmission_rectangular(mass_kg, barrier_height_J, energy_J, width_m)` (approximate) or `transmission_rectangular_exact(...)` (exact)
# - WKB transmission for arbitrary barrier: `transmission_wkb(mass_kg, energy_J, V_func, x1, x2)` or `transmission_wkb_quad(...)` (numerical quadrature)
# - Eckart barrier: `transmission_eckart(mass_kg, energy_J, barrier_height_J, width_m)`
# - Tunneling corrections for reaction rates: `wigner_tunneling_correction(imaginary_freq_cm_inv, temperature_K)`, `bell_tunneling_correction(...)`
# - Isotope effects: `isotope_tunneling_ratio(mass_light_amu, mass_heavy_amu, barrier_height_J)`
# - Decay constant: `decay_constant(mass_kg, barrier_height_J, energy_J)`
# - Unit conversions: `ev_to_J`, `J_to_ev`, `kjmol_to_J`, `amu_to_kg`, `cm_inv_to_J`

### Step 2: Choose the correct function
# - Simple rectangular barrier: `transmission_rectangular` or `transmission_rectangular_exact`
# - WKB for general barriers: `transmission_wkb` or `transmission_wkb_quad`
# - Chemical reaction tunneling: `wigner_tunneling_correction` or `bell_tunneling_correction`
# - Isotope effect comparison: `isotope_tunneling_ratio`

### Step 3: Handle special cases
# - Use conversion functions (`ev_to_J`, `amu_to_kg`, etc.) to get SI units before calling physics functions
# - `wkb_integral` is a helper; use `transmission_wkb` for the full calculation
# - Wigner correction uses imaginary frequency in cm-1 from frequency calculations
# - Gaussian barrier helper: `gaussian_barrier(x)` for testing WKB

### Examples
# 1. Electron (9.109e-31 kg) through 1 eV barrier, 1 Å wide, E=0.5 eV: `transmission_rectangular(9.109e-31, 1.602e-19, 0.801e-19, 1e-10)`
# 2. Wigner correction, ν*=1000i cm-1, T=298 K: `wigner_tunneling_correction(1000, 298)` -> κ > 1
# 3. H vs D tunneling ratio: `isotope_tunneling_ratio(1.008, 2.014, 5e-20)` -> ratio > 1 (H tunnels more)



import numpy as np
from scipy import integrate
from scipy.constants import hbar, eV, atomic_mass, m_e, physical_constants

# ---- Rectangular Barrier ----

def decay_constant(mass_kg, barrier_height_J, energy_J):
    """
    Decay constant κ for a particle inside a rectangular barrier.
    
    κ = sqrt(2m(V0 - E)) / ℏ
    
    Parameters
    ----------
    mass_kg : float - particle mass in kg
    barrier_height_J : float - V0 in Joules
    energy_J : float - E in Joules
    
    Returns
    -------
    float - κ in m-1
    """
    if energy_J >= barrier_height_J:
        return 0.0
    return np.sqrt(2.0 * mass_kg * (barrier_height_J - energy_J)) / hbar


def transmission_rectangular(mass_kg, barrier_height_J, energy_J, width_m):
    """
    Transmission coefficient for a rectangular barrier (E < V0 approximation).
    
    T ~ 16E(V0-E)/V02 x exp(-2κa)
    
    Parameters
    ----------
    mass_kg : float - particle mass in kg
    barrier_height_J : float - V0 in Joules
    energy_J : float - E in Joules
    width_m : float - barrier width in meters
    
    Returns
    -------
    float - transmission coefficient T (0 ≤ T ≤ 1)
    """
    if energy_J >= barrier_height_J:
        return 1.0
    if barrier_height_J == 0:
        return 1.0
    
    kappa = decay_constant(mass_kg, barrier_height_J, energy_J)
    prefactor = 16.0 * energy_J * (barrier_height_J - energy_J) / barrier_height_J**2
    T = prefactor * np.exp(-2.0 * kappa * width_m)
    return min(T, 1.0)


def transmission_rectangular_exact(mass_kg, barrier_height_J, energy_J, width_m):
    """
    Exact transmission coefficient for a rectangular barrier.
    
    T = 1 / [1 + V02sinh2(κa) / (4E(V0-E))]
    """
    if energy_J >= barrier_height_J:
        k2 = np.sqrt(2.0 * mass_kg * (energy_J - barrier_height_J)) / hbar
        sin_k2a = np.sin(k2 * width_m)
        denom = 1.0 + barrier_height_J**2 * sin_k2a**2 / (4.0 * energy_J * (energy_J - barrier_height_J))
        return 1.0 / denom
    
    if barrier_height_J == 0 or width_m == 0:
        return 1.0
    
    kappa = decay_constant(mass_kg, barrier_height_J, energy_J)
    sinh_ka = np.sinh(kappa * width_m)
    denom = 1.0 + barrier_height_J**2 * sinh_ka**2 / (4.0 * energy_J * (barrier_height_J - energy_J))
    return 1.0 / denom


# ---- WKB Approximation ----

def wkb_integral(mass_kg, energy_J, V_func, x1, x2, n_points=1000):
    """
    Numerical WKB integral: ∫√(2m[V(x)-E]) dx from x1 to x2
    """
    x = np.linspace(x1, x2, n_points)
    integrand = np.sqrt(np.maximum(2.0 * mass_kg * (V_func(x) - energy_J), 0.0))
    return integrate.trapezoid(integrand, x)


def transmission_wkb(mass_kg, energy_J, V_func, x1, x2, n_points=1000):
    """
    WKB transmission coefficient: T ~ exp(-2I/ℏ)
    """
    I = wkb_integral(mass_kg, energy_J, V_func, x1, x2, n_points)
    return np.exp(-2.0 * I / hbar)


def transmission_wkb_quad(mass_kg, energy_J, V_func, x1, x2):
    """
    WKB transmission using scipy.integrate.quad (higher accuracy).
    
    T ~ exp(-2∫_{x1}^{x2} √(2m[V(x)-E])/ℏ dx)
    """
    def integrand(x):
        dv = V_func(x) - energy_J
        if dv <= 0:
            return 0.0
        return np.sqrt(2.0 * mass_kg * dv)
    
    I, _ = integrate.quad(integrand, x1, x2, limit=200)
    return np.exp(-2.0 * I / hbar)


def transmission_wkb_rectangular(mass_kg, barrier_height_J, energy_J, width_m):
    """
    WKB for a rectangular barrier (analytical): T ~ exp(-2κa)
    """
    kappa = decay_constant(mass_kg, barrier_height_J, energy_J)
    return np.exp(-2.0 * kappa * width_m)


# ---- Eckart Barrier ----

def transmission_eckart(mass_kg, energy_J, barrier_height_J, width_m, E_react_J=0.0):
    """
    Eckart barrier transmission coefficient (simplified symmetric form).
    """
    if energy_J >= barrier_height_J:
        return 1.0
    if energy_J <= 0:
        return 0.0
    
    k = np.sqrt(2.0 * mass_kg * energy_J) / hbar
    arg = np.pi * k * width_m / 2.0
    T = 1.0 / (1.0 + np.cosh(2.0 * np.pi * width_m * np.sqrt(2.0 * mass_kg * barrier_height_J) / hbar)
               / (4.0 * np.sinh(arg)**2 + 1e-30))
    return min(T, 1.0)


# ---- Tunneling Corrections for Kinetics ----

def wigner_tunneling_correction(imaginary_freq_cm_inv, temperature_K=298.15):
    """
    Wigner tunneling correction (parabolic barrier approximation).
    
    κ_Wigner = 1 + (1/24)(ℏω‡/k_BT)2
    
    Valid for ℏω‡ ≪ k_BT (weak tunneling regime). Always ≥ 1.
    
    Parameters
    ----------
    imaginary_freq_cm_inv : float - |ν‡| in cm-1 (magnitude of imaginary TS frequency)
    temperature_K : float - temperature in K (default 298.15)
    
    Returns
    -------
    float - Wigner correction factor κ (≥ 1)
    """
    kB = physical_constants['Boltzmann constant'][0]
    c = physical_constants['speed of light in vacuum'][0]
    # ω‡ = 2pic·ν̃  where ν̃ is in cm-1
    omega_barrier = 2.0 * np.pi * c * 100.0 * imaginary_freq_cm_inv  # rad/s
    u = hbar * omega_barrier / (kB * temperature_K)
    return 1.0 + u**2 / 24.0


def bell_tunneling_correction(mass_kg, barrier_height_J, temperature_K, width_m=1e-10):
    """
    Bell tunneling correction factor (Eckart barrier approximation).
    
    κ_Bell = u / (2·tanh(u/2))
    
    where u = ℏω‡/(k_BT), ω‡ = √(2V0/m)/a
    
    Reduces to Wigner form for small u: κ ~ 1 + u2/24.
    Always ≥ 1.
    
    Parameters
    ----------
    mass_kg : float - tunneling particle mass in kg
    barrier_height_J : float - barrier height in J
    temperature_K : float - temperature in K
    width_m : float - barrier width in m (default 1 Å)
    
    Returns
    -------
    float - Bell correction factor (κ ≥ 1)
    """
    kB = physical_constants['Boltzmann constant'][0]
    if width_m <= 0 or barrier_height_J <= 0:
        return 1.0
    omega_barrier = np.sqrt(2.0 * barrier_height_J / mass_kg) / width_m
    u = hbar * omega_barrier / (kB * temperature_K)
    if u > 100:
        return 1e6
    if u < 0.01:
        return 1.0 + u**2 / 24.0  # Wigner limit
    kappa = u / (2.0 * np.tanh(u / 2.0))
    return min(kappa, 1e6)


def isotope_tunneling_ratio(mass_light_amu, mass_heavy_amu, barrier_height_J, width_m=1e-10):
    """
    Predicted kinetic isotope effect from tunneling alone.
    
    KIE ~ exp(2a√(2V0)(√m_heavy - √m_light)/ℏ)
    
    Parameters
    ----------
    mass_light_amu : float - light isotope mass (e.g., 1.0078 for H)
    mass_heavy_amu : float - heavy isotope mass (e.g., 2.0141 for D)
    barrier_height_J : float - barrier height in J
    width_m : float - barrier width in m
    
    Returns
    -------
    float - predicted H/D KIE from tunneling (k_H/k_D)
    """
    m_light = mass_light_amu * atomic_mass
    m_heavy = mass_heavy_amu * atomic_mass
    
    # Low-energy limit (E ~ 0)
    exponent = 2.0 * width_m * np.sqrt(2.0 * barrier_height_J) * (np.sqrt(m_heavy) - np.sqrt(m_light)) / hbar
    return np.exp(exponent)


# ---- Harmonic Oscillator Penetration ----

def harmonic_oscillator_penetration(quantum_number_v, frequency_Hz, mass_kg):
    """
    Classically forbidden probability for a quantum harmonic oscillator.
    
    P_v = |ψ(x)|2 integrated beyond classical turning points.
    
    Uses exact Hermite function integration with careful numerical handling.
    
    Parameters
    ----------
    quantum_number_v : int - vibrational quantum number (0, 1, 2, ...)
    frequency_Hz : float - oscillator frequency in Hz
    mass_kg : float - reduced mass in kg
    
    Returns
    -------
    float - probability of finding particle in classically forbidden region
    """
    import math
    from scipy.special import eval_hermite
    from scipy.integrate import quad
    
    omega = 2.0 * np.pi * frequency_Hz
    # Characteristic length scale
    sigma = np.sqrt(hbar / (mass_kg * omega))
    alpha = 1.0 / sigma**2
    
    # Classical turning point: x_t = σ * sqrt(2v+1)
    x_t = sigma * np.sqrt(2.0 * quantum_number_v + 1.0)
    
    # Normalization constant: N = (alpha/pi)^0.25 / sqrt(2^v * v!)
    norm = (alpha / np.pi)**0.25 / np.sqrt(2**quantum_number_v * float(math.factorial(quantum_number_v)))
    
    def psi_squared(x):
        # Use dimensionless coordinate ξ = x/σ
        xi = x / sigma
        # Evaluate Hermite polynomial H_v(ξ) using scipy's stable implementation
        H_v_xi = eval_hermite(quantum_number_v, xi)
        # Wave function: ψ = N * H_v(ξ) * exp(-ξ2/2)
        psi = norm * H_v_xi * np.exp(-xi**2 / 2.0)
        return psi**2
    
    # Integrate from turning point to a practical upper limit (20σ beyond turning point)
    # Using np.inf fails because quad can't detect contributions in the tail
    upper_limit = x_t + 20 * sigma
    integral, _ = quad(psi_squared, x_t, upper_limit, limit=200)
    total_prob = 2.0 * integral  # both sides
    
    return min(total_prob, 1.0)


# ---- Utility: Unit Conversions ----

def ev_to_J(eV_val):
    """Convert eV to Joules."""
    return eV_val * eV

def J_to_ev(J_val):
    """Convert Joules to eV."""
    return J_val / eV

def kjmol_to_J(kjmol_val):
    """Convert kJ/mol to J per molecule."""
    NA = physical_constants['Avogadro constant'][0]
    return kjmol_val * 1000.0 / NA

def amu_to_kg(amu_val):
    """Convert atomic mass units to kg."""
    return amu_val * atomic_mass

def cm_inv_to_J(cm_inv_val):
    """Convert wavenumber (cm-1) to Joules."""
    h = physical_constants['Planck constant'][0]
    c = physical_constants['speed of light in vacuum'][0]
    return h * c * 100.0 * cm_inv_val


# ---- Demo / Quick Test ----

if __name__ == "__main__":
    print("=== Quantum Tunneling Calculator ===\n")
    
    # Example 1: Rectangular barrier - electron tunneling
    V0 = ev_to_J(2.0)
    E = ev_to_J(1.0)
    a = 5e-10
    
    T_approx = transmission_rectangular(m_e, V0, E, a)
    T_exact = transmission_rectangular_exact(m_e, V0, E, a)
    print(f"Electron, V0=2 eV, E=1 eV, a=5 A")
    print(f"  T (approx):  {T_approx:.6e}")
    print(f"  T (exact):   {T_exact:.6e}")
    
    # Example 2: Proton vs Deuteron tunneling
    m_H = amu_to_kg(1.0078)
    V0_kJ = kjmol_to_J(40.0)  # 40 kJ/mol barrier
    a_proton = 0.5e-10
    
    T_H = transmission_rectangular(m_H, V0_kJ, 0.0, a_proton)
    print(f"\nProton tunneling, V0=40 kJ/mol, a=0.5 A: T = {T_H:.6e}")
    
    # Example 3: WKB for Gaussian barrier (proton)
    def gaussian_barrier(x, V0=V0_kJ, sigma=0.5e-10):
        return V0 * np.exp(-0.5 * (x / sigma)**2)
    
    T_wkb = transmission_wkb_quad(m_H, 0.0, gaussian_barrier, -2e-10, 2e-10)
    print(f"WKB Gaussian barrier T: {T_wkb:.6e}")
    
    # Example 4: Wigner tunneling correction
    for nu in [500, 1000, 1500, 2000]:
        kappa = wigner_tunneling_correction(nu, 298.15)
        print(f"  Wigner kappa(nu*={nu} cm-1): {kappa:.4f}")
    
    # Example 5: Harmonic oscillator penetration
    nu_CO = 6.5e13  # CO stretch ~2170 cm-1
    m_CO = amu_to_kg(6.85)
    for v in range(3):
        p = harmonic_oscillator_penetration(v, nu_CO, m_CO)
        print(f"  QHO v={v}: P(forbidden) = {p:.6f}")
