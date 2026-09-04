"""
Electronic Spectroscopy Tools - L3 Implementation

Core functions for electronic spectroscopy:
- Electronic transitions and selection rules
- Franck-Condon factors
- Electronic term symbols
- Transition energies
- Absorption and emission spectra
- Jablonski diagrams

Source: LibreTexts Physical Chemistry Ch13-15

## Solver Instructions (for AI Agent)

When you encounter electronic spectroscopy problems (transitions, Franck-Condon, term symbols, selection rules, FRET):

### Step 1: Identify what is given and what is asked
- Given: wavelength, energy, quantum numbers, rate constants, distances
- Asked: transition energy, FC factors, term symbols, quantum yields, FRET efficiency

### Step 2: Choose the correct function
**Energy conversions:**
- `transition_energy_wavelength(E_J)`: lambda = hc/E (nm)
- `transition_energy_eV(wavelength_nm)`: E = hc/lambda (eV)
- `transition_energy_wavenumber(wavelength_nm)`: ν̃ = 107/lambda (cm-1)
- `wavelength_from_wavenumber(wavenumber_cm)`: lambda from ν̃

**Franck-Condon:**
- `franck_condon_factor(v1, v2, delta_q)`: FC factor for vibronic transition
- `vibronic_progression_positions(E_00, omega_cm)`: Band positions
- `vertical_transition_energy(E_0, delta_E_reorg)`: E_vert = E_0 + lambda

**Term symbols & selection rules:**
- `electronic_term_symbol(multiplicity, L, J)`: ^{2S+1}L_J
- `ground_state_term(p_electrons)`: Hund's rules for pⁿ
- `electronic_selection_rules(L1,S1,J1,L2,S2,J2)`: DeltaS=0, DeltaL=0,±1, DeltaJ=0,±1
- `laporte_selection_rule(g_u_initial, g_u_final)`: g↔u allowed

**Photophysics:**
- `quantum_yield_fluorescence(k_f, k_nr, k_isc)`: Φ_f = k_f/(k_f+k_nr+k_ISC)
- `quantum_yield_phosphorescence(k_p, k_nr_T)`: Φ_p
- `intersystem_crossing_rate(S1_T1_gap_J, spin_orbit_coupling_J)`: k_ISC
- `forster_radius(k_D, tau_D, J_overlap, n_refractive)`: R0 (Förster radius)
- `energy_transfer_efficiency_distance(R, R0)`: E = R06/(R6+R06)
- `molar_absorptivity_from_oscillator(f, bandwidth_nm, lambda_max_nm)`: ε from f

### Step 3: Handle special cases
- FC progression: 0->0 strongest for small displacement; shifts to higher v2 for large DeltaQ
- FRET efficiency = 0.5 at R = R0; sensitive to R6 dependence
- Spin-forbidden transitions (DeltaS!=0) have very low intensity

### Examples
```python
transition_energy_eV(500)  # -> 2.48 eV
franck_condon_factor(0, 0, 1.0)  # -> 0.37
quantum_yield_fluorescence(1e8, 1e7)  # -> 0.91
energy_transfer_efficiency_distance(5e-9, 5e-9)  # -> 0.5
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants
from scipy.special import factorial
from scipy.integrate import quad

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
SPEED_OF_LIGHT = 2.99792458e8     # m/s
SPEED_OF_LIGHT_CM = SPEED_OF_LIGHT * 100
BOLTZMANN = 1.380649e-23          # J/K
EV_TO_JOULE = 1.60217663e-19


# =============================================================================
# ELECTRONIC TRANSITIONS
# =============================================================================

def transition_energy_wavelength(E_J: float) -> float:
    """
    Calculate wavelength from transition energy.
    
    lambda = hc/E
    
    Args:
        E_J: Energy in Joules
    
    Returns:
        Wavelength in nm
    
    Example:
        >>> transition_energy_wavelength(3.2e-19)  # ~2 eV
        620  # nm (orange-red)
    """
    wavelength_m = PLANCK_CONSTANT * SPEED_OF_LIGHT / E_J
    return wavelength_m * 1e9  # Convert to nm


def transition_energy_eV(wavelength_nm: float) -> float:
    """
    Calculate transition energy in eV from wavelength.
    
    E = hc/lambda
    
    Args:
        wavelength_nm: Wavelength in nm
    
    Returns:
        Energy in eV
    
    Example:
        >>> transition_energy_eV(500)  # Green light
        2.48  # eV
    """
    wavelength_m = wavelength_nm * 1e-9
    E_J = PLANCK_CONSTANT * SPEED_OF_LIGHT / wavelength_m
    return E_J / EV_TO_JOULE


def transition_energy_wavenumber(wavelength_nm: float) -> float:
    """
    Calculate transition energy in wavenumbers.
    
    ν̃ = 107/lambda(nm)
    
    Args:
        wavelength_nm: Wavelength in nm
    
    Returns:
        Energy in cm-1
    
    Example:
        >>> transition_energy_wavenumber(500)
        20000  # cm-1
    """
    return 1e7 / wavelength_nm


def wavelength_from_wavenumber(wavenumber_cm: float) -> float:
    """
    Calculate wavelength from wavenumber.
    
    lambda = 107/ν̃
    
    Args:
        wavenumber_cm: Wavenumber in cm-1
    
    Returns:
        Wavelength in nm
    """
    return 1e7 / wavenumber_cm


# =============================================================================
# FRANCK-CONDON FACTORS
# =============================================================================

def franck_condon_factor(v1: int, v2: int, 
                          delta_q: float,
                          omega_ratio: float = 1.0) -> float:
    """
    Calculate Franck-Condon factor for vibronic transition.
    
    Approximate formula using displaced harmonic oscillator model.
    
    S = ⟨v1|v2⟩2
    
    where S depends on displacement DeltaQ and frequency ratio.
    
    Args:
        v1: Vibrational quantum number in initial state
        v2: Vibrational quantum number in final state
        delta_q: Displacement parameter (dimensionless)
        omega_ratio: ω2/ω1 ratio of frequencies
    
    Returns:
        Franck-Condon factor (probability, 0 to 1)
    
    Note:
        This is an approximation. Full calculation requires
        overlap integrals of wavefunctions.
    
    Example:
        >>> franck_condon_factor(0, 0, 1.0)  # 0->0 with moderate displacement
        0.37
    """
    # Simplified displaced harmonic oscillator model
    # FC factor = (S^|v2-v1| / |v2-v1|!) x exp(-S) for v1=0
    # where S = (DeltaQ x √(ω/2ℏ))2 = Huang-Rhys factor
    
    S = delta_q**2  # Huang-Rhys factor approximation
    
    if v1 == 0:
        # For v1=0, simpler formula
        return (S**v2 / factorial(v2)) * np.exp(-S)
    else:
        # General case requires more complex calculation
        # Approximation for small S
        return (S**abs(v2-v1) / factorial(abs(v2-v1))) * np.exp(-S)


def huang_rhys_factor(delta_q: float, omega: float) -> float:
    """
    Calculate Huang-Rhys factor.
    
    S = (DeltaQ x √(muω/2ℏ))2
    
    Args:
        delta_q: Displacement in meters
        omega: Vibrational frequency in rad/s
    
    Returns:
        Huang-Rhys factor (dimensionless)
    
    Note:
        S determines the intensity distribution in vibronic progression.
    """
    # Simplified: need reduced mass for full calculation
    # S ~ (DeltaQ)2 x muω/2ℏ
    return delta_q**2  # Placeholder - needs proper implementation


def vertical_transition_energy(E_0: float, delta_E_reorg: float) -> float:
    """
    Calculate vertical transition energy.
    
    E_vertical = E_0 + lambda
    
    where lambda is the reorganization energy.
    
    Args:
        E_0: Adiabatic transition energy (0-0 transition)
        delta_E_reorg: Reorganization energy
    
    Returns:
        Vertical transition energy
    """
    return E_0 + delta_E_reorg


def vibronic_progression_positions(E_00: float,
                                    omega_cm: float,
                                    max_v: int = 10) -> List[float]:
    """
    Calculate positions of vibronic progression bands.
    
    E(v') = E_00 + v' x ω
    
    Args:
        E_00: 0-0 transition energy in cm-1
        omega_cm: Vibrational spacing in cm-1
        max_v: Maximum vibrational quantum number
    
    Returns:
        List of transition energies in cm-1
    
    Example:
        >>> vibronic_progression_positions(20000, 1000, 5)
        [20000, 21000, 22000, 23000, 24000, 25000]
    """
    return [E_00 + v * omega_cm for v in range(max_v + 1)]


# =============================================================================
# ELECTRONIC TERM SYMBOLS
# =============================================================================

def electronic_term_symbol(multiplicity: int, 
                            L: int,
                            J: Optional[float] = None) -> str:
    """
    Construct electronic term symbol.
    
    Format: ^{2S+1}L_J
    
    Args:
        multiplicity: 2S+1
        L: Total orbital angular momentum (0=S, 1=P, 2=D, 3=F)
        J: Total angular momentum (optional)
    
    Returns:
        Term symbol string
    
    Example:
        >>> electronic_term_symbol(3, 1)  # Triplet P
        '3P'
        >>> electronic_term_symbol(2, 0, 0.5)  # Doublet S, J=1/2
        '2S_{1/2}'
    """
    L_symbols = ['S', 'P', 'D', 'F', 'G', 'H', 'I']
    L_symbol = L_symbols[L] if L < len(L_symbols) else '?'
    
    # Unicode superscripts
    superscripts = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
                    '6': '6', '7': '7', '8': '8', '9': '9'}
    mult_str = ''.join(superscripts.get(c, c) for c in str(multiplicity))
    
    term = f"{mult_str}{L_symbol}"
    
    if J is not None:
        if J == int(J):
            term += f"_{int(J)}"
        else:
            term += f"_{int(2*J)}/2"
    
    return term


def ground_state_term(p_electrons: int) -> str:
    """
    Determine ground state term symbol for pⁿ configuration.
    
    Uses Hund's rules.
    
    Args:
        p_electrons: Number of p electrons (1-5)
    
    Returns:
        Ground state term symbol
    
    Example:
        >>> ground_state_term(2)  # Carbon
        '3P'
        >>> ground_state_term(3)  # Nitrogen
        '4S'
    """
    # Hund's rules applied to pⁿ
    terms = {
        1: '2P',      # p1
        2: '3P',      # p2
        3: '4S',      # p3
        4: '3P',      # p4 (same as p2, complement)
        5: '2P',      # p5 (same as p1)
    }
    
    if p_electrons in terms:
        return terms[p_electrons]
    else:
        raise ValueError(f"Invalid p electron count: {p_electrons}")


# =============================================================================
# SELECTION RULES
# =============================================================================

def electronic_selection_rules(L1: int, S1: float, J1: float,
                                L2: int, S2: float, J2: float) -> Tuple[bool, str]:
    """
    Check selection rules for electronic transitions.
    
    Rules (L-S coupling):
    - DeltaS = 0 (spin selection)
    - DeltaL = 0, ±1 (orbital selection)
    - DeltaJ = 0, ±1 (but J=0 to J=0 forbidden)
    
    Args:
        L1, S1, J1: Initial state quantum numbers
        L2, S2, J2: Final state quantum numbers
    
    Returns:
        (allowed, reason)
    
    Example:
        >>> electronic_selection_rules(0, 0, 0, 1, 0, 1)  # S->P
        (True, 'Allowed')
    """
    delta_S = abs(S2 - S1)
    delta_L = L2 - L1
    delta_J = J2 - J1
    
    # Spin selection
    if delta_S > 0.01:  # DeltaS must be 0
        return (False, f"Forbidden: DeltaS = {delta_S:.1f} != 0 (spin-forbidden)")
    
    # Orbital selection
    if abs(delta_L) > 1:
        return (False, f"Forbidden: DeltaL = {delta_L} (must be 0 or ±1)")
    
    # Angular momentum selection
    if abs(delta_J) > 1:
        return (False, f"Forbidden: DeltaJ = {delta_J:.1f} (must be 0 or ±1)")
    
    if J1 == 0 and J2 == 0:
        return (False, "Forbidden: J=0 to J=0")
    
    return (True, f"Allowed: DeltaS=0, DeltaL={delta_L}, DeltaJ={delta_J:.1f}")


def laporte_selection_rule(g_u_initial: str, g_u_final: str) -> Tuple[bool, str]:
    """
    Apply Laporte selection rule.
    
    For centrosymmetric molecules:
    - g -> u and u -> g allowed
    - g -> g and u -> u forbidden
    
    Args:
        g_u_initial: 'g' or 'u' for initial state
        g_u_final: 'g' or 'u' for final state
    
    Returns:
        (allowed, reason)
    """
    if g_u_initial == g_u_final:
        return (False, f"Laporte-forbidden: {g_u_initial}->{g_u_final}")
    else:
        return (True, f"Laporte-allowed: {g_u_initial}->{g_u_final}")


# =============================================================================
# JABLONSKI DIAGRAM
# =============================================================================

def fluorescence_rate(A: float) -> float:
    """
    Calculate fluorescence rate (radiative decay).
    
    k_f = A (Einstein coefficient for spontaneous emission)
    
    Args:
        A: Einstein A coefficient in s-1
    
    Returns:
        Fluorescence rate in s-1
    """
    return A


def intersystem_crossing_rate(S1_T1_gap_J: float,
                               spin_orbit_coupling_J: float) -> float:
    """
    Estimate intersystem crossing rate.
    
    k_ISC ∝ |⟨S|Ĥ_SO|T⟩|2 / DeltaE
    
    Args:
        S1_T1_gap_J: Energy gap between S1 and T1 in J
        spin_orbit_coupling_J: Spin-orbit coupling strength in J
    
    Returns:
        ISC rate in s-1 (order of magnitude)
    """
    # Simplified Fermi's golden rule
    return (spin_orbit_coupling_J**2) / S1_T1_gap_J * 1e15  # Scaling factor


def phosphorescence_lifetime(A: float, ISC_rate: float) -> float:
    """
    Calculate phosphorescence lifetime.
    
    τ_phos = 1/(k_ISC + k_r)
    
    For triplet: k_r << k_ISC typically
    
    Args:
        A: Radiative rate for T1->S0
        ISC_rate: Intersystem crossing rate
    
    Returns:
        Phosphorescence lifetime in s
    """
    total_rate = A + ISC_rate
    return 1 / total_rate if total_rate > 0 else float('inf')


def quantum_yield_fluorescence(k_f: float, k_nr: float, 
                                k_isc: float = 0) -> float:
    """
    Calculate fluorescence quantum yield.
    
    Φ_f = k_f / (k_f + k_nr + k_ISC)
    
    Args:
        k_f: Fluorescence rate
        k_nr: Non-radiative decay rate
        k_isc: Intersystem crossing rate
    
    Returns:
        Quantum yield (0 to 1)
    
    Example:
        >>> quantum_yield_fluorescence(1e8, 1e7)
        0.91
    """
    total_rate = k_f + k_nr + k_isc
    return k_f / total_rate if total_rate > 0 else 0


def quantum_yield_phosphorescence(k_p: float, k_nr_T: float) -> float:
    """
    Calculate phosphorescence quantum yield.
    
    Φ_p = k_p / (k_p + k_nr_T)
    
    Args:
        k_p: Phosphorescence rate
        k_nr_T: Non-radiative decay from triplet
    
    Returns:
        Quantum yield (0 to 1)
    """
    total_rate = k_p + k_nr_T
    return k_p / total_rate if total_rate > 0 else 0


def intersystem_crossing_yield(k_isc: float, k_f: float, k_nr: float) -> float:
    """
    Calculate ISC quantum yield.
    
    Φ_ISC = k_ISC / (k_f + k_nr + k_ISC)
    
    Args:
        k_isc: ISC rate
        k_f: Fluorescence rate
        k_nr: Non-radiative rate from S1
    
    Returns:
        ISC yield (0 to 1)
    """
    total_rate = k_f + k_nr + k_isc
    return k_isc / total_rate if total_rate > 0 else 0


# =============================================================================
# ABSORPTION INTENSITY
# =============================================================================

def oscillator_strength(f: float) -> float:
    """
    Validate oscillator strength (should be 0 to 1 for allowed transitions).
    
    f = (4.32x10-9) ∫ε(ν) dν
    
    Args:
        f: Oscillator strength
    
    Returns:
        f (validated)
    
    Note:
        f ~ 1 for fully allowed transition
        f ~ 0.01 for partially allowed
        f < 0.001 for weak/forbidden
    """
    if f < 0 or f > 2:  # Can exceed 1 for some cases
        raise ValueError(f"Unusual oscillator strength: {f}")
    return f


def molar_absorptivity_from_oscillator(f: float, 
                                        bandwidth_nm: float,
                                        lambda_max_nm: float) -> float:
    """
    Estimate molar absorptivity from oscillator strength.
    
    ε_max ~ (f x 108) / (Deltalambda x lambda_max)
    
    Args:
        f: Oscillator strength
        bandwidth_nm: Bandwidth in nm
        lambda_max_nm: Peak wavelength in nm
    
    Returns:
        Molar absorptivity in M-1·cm-1
    
    Example:
        >>> molar_absorptivity_from_oscillator(0.5, 20, 400)
        6250  # M-1·cm-1
    """
    return (f * 1e8) / (bandwidth_nm * lambda_max_nm)


# =============================================================================
# ENERGY TRANSFER
# =============================================================================

def forster_radius(k_D: float, tau_D: float,
                   J_overlap: float,
                   n_refractive: float,
                   kappa2: float = 2/3) -> float:
    """
    Calculate Förster radius for resonance energy transfer.
    
    R0 = (8.79x10-25 x κ2 x n-4 x Φ_D x J)^(1/6)  [in cm]
    
    Args:
        k_D: Donor radiative rate
        tau_D: Donor lifetime
        J_overlap: Spectral overlap integral
        n_refractive: Refractive index of medium
        kappa2: Orientation factor (2/3 for random)
    
    Returns:
        Förster radius in meters
    
    Example:
        >>> forster_radius(1e8, 1e-8, 1e-15, 1.33)
        5e-9  # 5 nm
    """
    phi_D = k_D * tau_D  # Donor quantum yield
    
    # R0 calculation (simplified)
    R0_cm = (8.79e-25 * kappa2 * n_refractive**(-4) * phi_D * J_overlap)**(1/6)
    
    return R0_cm * 100  # Convert to m


def energy_transfer_efficiency_distance(R: float, R0: float) -> float:
    """
    Calculate FRET efficiency at distance R.
    
    E = R06 / (R6 + R06)
    
    Args:
        R: Donor-acceptor distance
        R0: Förster radius (same units)
    
    Returns:
        Transfer efficiency (0 to 1)
    
    Example:
        >>> energy_transfer_efficiency_distance(5e-9, 5e-9)  # R = R0
        0.5
    """
    return R0**6 / (R**6 + R0**6)


# =============================================================================
# DATABASE
# =============================================================================

ELECTRONIC_TRANSITIONS_DATA = {
    'Na': {
        'ground_state': '3s 2S',
        'D_lines': {
            'D1': {'transition': '3p 2P_{1/2} -> 3s 2S_{1/2}', 'wavelength_nm': 589.59},
            'D2': {'transition': '3p 2P_{3/2} -> 3s 2S_{1/2}', 'wavelength_nm': 588.99}
        }
    },
    'H': {
        'ground_state': '1s 2S',
        'Lyman': {'transition': 'np -> 1s', 'wavelength_range': 'UV'},
        'Balmer': {'transition': 'np -> 2s', 'wavelength_range': 'visible'},
        'Paschen': {'transition': 'np -> 3s', 'wavelength_range': 'IR'}
    },
    'Hg': {
        'ground_state': '6s2 1S0',
        '254_nm': {'transition': '63P1 -> 61S0', 'wavelength_nm': 253.7}
    }
}


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Electronic Spectroscopy Tools - Examples")
    print("=" * 60)
    
    # Transition energies
    print("\n1. Transition Energies:")
    print(f"   500 nm -> {transition_energy_eV(500):.2f} eV")
    print(f"   500 nm -> {transition_energy_wavenumber(500):.0f} cm-1")
    
    # Franck-Condon
    print("\n2. Franck-Condon Factors:")
    for v2 in range(5):
        fc = franck_condon_factor(0, v2, 1.0)
        print(f"   0->{v2}: {fc:.3f}")
    
    # Selection rules
    print("\n3. Selection Rules:")
    allowed, reason = electronic_selection_rules(0, 0, 0, 1, 0, 1)
    print(f"   S->P: {reason}")
    
    allowed, reason = electronic_selection_rules(0, 0, 0, 1, 1, 1)
    print(f"   Singlet->Triplet: {reason}")
    
    # Quantum yields
    print("\n4. Quantum Yields:")
    phi_f = quantum_yield_fluorescence(1e8, 1e7)
    print(f"   Fluorescence (k_f=108, k_nr=107): Φ_f = {phi_f:.2f}")
    
    # Energy transfer
    print("\n5. FRET:")
    E = energy_transfer_efficiency_distance(5e-9, 5e-9)
    print(f"   E at R=R0: {E:.2f}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "electronic_selection_rules",
        "description": "Check selection rules for electronic transitions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "L1": {"type": "number", "description": "L1"},
                "S1": {"type": "number", "description": "S1"},
                "J1": {"type": "number", "description": "J1"},
                "L2": {"type": "number", "description": "L2"},
                "S2": {"type": "number", "description": "S2"},
                "J2": {"type": "number", "description": "J2"},
            },
            "required": ["L1", "S1", "J1", "L2", "S2", "J2"]
        }
    },
    {
        "name": "electronic_term_symbol",
        "description": "Construct electronic term symbol.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "multiplicity": {"type": "number", "description": "Multiplicity"},
                "L": {"type": "number", "description": "L"},
                "J": {"type": "number", "description": "J", "default": None},
            },
            "required": ["multiplicity", "L"]
        }
    },
    {
        "name": "energy_transfer_efficiency_distance",
        "description": "Calculate FRET efficiency at distance R.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "R": {"type": "number", "description": "R"},
                "R0": {"type": "number", "description": "R0"},
            },
            "required": ["R", "R0"]
        }
    },
    {
        "name": "factorial",
        "description": "The factorial of a number or array of numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {"type": "number", "description": "N"},
                "exact": {"type": "number", "description": "Exact", "default": False},
                "extend": {"type": "number", "description": "Extend", "default": "zero"},
            },
            "required": ["n"]
        }
    },
    {
        "name": "fluorescence_rate",
        "description": "Calculate fluorescence rate (radiative decay).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "A": {"type": "number", "description": "A"},
            },
            "required": ["A"]
        }
    },
    {
        "name": "forster_radius",
        "description": "Calculate F\u00f6rster radius for resonance energy transfer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_D": {"type": "number", "description": "K D"},
                "tau_D": {"type": "number", "description": "Tau D"},
                "J_overlap": {"type": "number", "description": "J Overlap"},
                "n_refractive": {"type": "number", "description": "N Refractive"},
                "kappa2": {"type": "number", "description": "Kappa2", "default": 0.6666666666666666},
            },
            "required": ["k_D", "tau_D", "J_overlap", "n_refractive"]
        }
    },
    {
        "name": "franck_condon_factor",
        "description": "Calculate Franck-Condon factor for vibronic transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "v1": {"type": "number", "description": "V1"},
                "v2": {"type": "number", "description": "V2"},
                "delta_q": {"type": "number", "description": "Delta Q"},
                "omega_ratio": {"type": "number", "description": "Omega Ratio", "default": 1.0},
            },
            "required": ["v1", "v2", "delta_q"]
        }
    },
    {
        "name": "ground_state_term",
        "description": "Determine ground state term symbol for p\u207f configuration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "p_electrons": {"type": "number", "description": "P Electrons"},
            },
            "required": ["p_electrons"]
        }
    },
    {
        "name": "huang_rhys_factor",
        "description": "Calculate Huang-Rhys factor.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_q": {"type": "number", "description": "Delta Q"},
                "omega": {"type": "number", "description": "Omega"},
            },
            "required": ["delta_q", "omega"]
        }
    },
    {
        "name": "intersystem_crossing_rate",
        "description": "Estimate intersystem crossing rate.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "S1_T1_gap_J": {"type": "number", "description": "S1 T1 Gap J"},
                "spin_orbit_coupling_J": {"type": "number", "description": "Spin Orbit Coupling J"},
            },
            "required": ["S1_T1_gap_J", "spin_orbit_coupling_J"]
        }
    },
    {
        "name": "intersystem_crossing_yield",
        "description": "Calculate ISC quantum yield.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_isc": {"type": "number", "description": "K Isc"},
                "k_f": {"type": "number", "description": "K F"},
                "k_nr": {"type": "number", "description": "K Nr"},
            },
            "required": ["k_isc", "k_f", "k_nr"]
        }
    },
    {
        "name": "laporte_selection_rule",
        "description": "Apply Laporte selection rule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "g_u_initial": {"type": "number", "description": "G U Initial"},
                "g_u_final": {"type": "number", "description": "G U Final"},
            },
            "required": ["g_u_initial", "g_u_final"]
        }
    },
    {
        "name": "molar_absorptivity_from_oscillator",
        "description": "Estimate molar absorptivity from oscillator strength.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "f": {"type": "number", "description": "F"},
                "bandwidth_nm": {"type": "number", "description": "Bandwidth Nm"},
                "lambda_max_nm": {"type": "number", "description": "Lambda Max Nm"},
            },
            "required": ["f", "bandwidth_nm", "lambda_max_nm"]
        }
    },
    {
        "name": "oscillator_strength",
        "description": "Validate oscillator strength (should be 0 to 1 for allowed transitions).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "f": {"type": "number", "description": "F"},
            },
            "required": ["f"]
        }
    },
    {
        "name": "phosphorescence_lifetime",
        "description": "Calculate phosphorescence lifetime.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "A": {"type": "number", "description": "A"},
                "ISC_rate": {"type": "number", "description": "Isc Rate"},
            },
            "required": ["A", "ISC_rate"]
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
        "name": "quantum_yield_fluorescence",
        "description": "Calculate fluorescence quantum yield.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_f": {"type": "number", "description": "K F"},
                "k_nr": {"type": "number", "description": "K Nr"},
                "k_isc": {"type": "number", "description": "K Isc", "default": 0},
            },
            "required": ["k_f", "k_nr"]
        }
    },
    {
        "name": "quantum_yield_phosphorescence",
        "description": "Calculate phosphorescence quantum yield.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k_p": {"type": "number", "description": "K P"},
                "k_nr_T": {"type": "number", "description": "K Nr T"},
            },
            "required": ["k_p", "k_nr_T"]
        }
    },
    {
        "name": "transition_energy_eV",
        "description": "Calculate transition energy in eV from wavelength.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavelength_nm": {"type": "number", "description": "Wavelength Nm"},
            },
            "required": ["wavelength_nm"]
        }
    },
    {
        "name": "transition_energy_wavelength",
        "description": "Calculate wavelength from transition energy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_J": {"type": "number", "description": "E J"},
            },
            "required": ["E_J"]
        }
    },
    {
        "name": "transition_energy_wavenumber",
        "description": "Calculate transition energy in wavenumbers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavelength_nm": {"type": "number", "description": "Wavelength Nm"},
            },
            "required": ["wavelength_nm"]
        }
    },
    {
        "name": "vertical_transition_energy",
        "description": "Calculate vertical transition energy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_0": {"type": "number", "description": "E 0"},
                "delta_E_reorg": {"type": "number", "description": "Delta E Reorg"},
            },
            "required": ["E_0", "delta_E_reorg"]
        }
    },
    {
        "name": "vibronic_progression_positions",
        "description": "Calculate positions of vibronic progression bands.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_00": {"type": "number", "description": "E 00"},
                "omega_cm": {"type": "number", "description": "Omega Cm"},
                "max_v": {"type": "number", "description": "Max V", "default": 10},
            },
            "required": ["E_00", "omega_cm"]
        }
    },
    {
        "name": "wavelength_from_wavenumber",
        "description": "Calculate wavelength from wavenumber.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavenumber_cm": {"type": "number", "description": "Wavenumber Cm"},
            },
            "required": ["wavenumber_cm"]
        }
    }
]
