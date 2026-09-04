"""
Molecular Spectroscopy Tools - L3 Implementation

Core functions for molecular spectroscopy calculations:
- Rotational spectroscopy (microwave)
- Vibrational-rotational spectroscopy (IR)
- Raman spectroscopy
- Selection rules and intensities
- Spectral line positions and spacings

Source: LibreTexts Physical Chemistry Ch13-15

## Solver Instructions (for AI Agent)

When you encounter molecular spectroscopy problems (rotational, vibrational, Raman), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given rotational constant B -> calculate energy levels or line positions?
- Given bond length -> calculate rotational constant?
- Given vibrational frequency -> calculate force constant?
- Given temperatures -> calculate Boltzmann populations?
- Given Raman shift -> interpret spectrum?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Rotational energy | `rotational_energy_J(J, B_cm)` | E(J) = B·J(J+1) in cm-1 |
| Rotational line position | `rotational_line_position(J_lower, B_cm)` | ν̃ = 2B(J+1) in cm-1 |
| Rotational line frequency | `rotational_line_frequency_GHz(J_lower, B_cm)` | in GHz |
| Rotational constant | `rotational_constant_B(r_angstrom, mu_amu)` | B = h/(8pi2Ic) in cm-1 |
| Vibrational energy | `vibrational_energy_nu(nu, omega_cm, x_e)` | G(ν) = ωₑ(ν+½) - ωₑxₑ(ν+½)2 |
| Force constant | `force_constant_from_frequency(omega_cm, mu_amu)` | k = (2picω)2mu in N/m |
| Boltzmann population | `boltzmann_population_J(J, B_cm, T)` | rotational state population |

### Step 3: Handle special cases
- Rotational transitions: DeltaJ = +1 (microwave), DeltaJ = 0, ±1 (Raman)
- Vibrational transitions: Deltaν = +1 (fundamental), Deltaν = +2 (first overtone)
- Intensity follows Boltzmann distribution with degeneracy factor (2J+1)

### Examples
```python
# Example 1: HCl rotational line (B = 10.44 cm-1)
rotational_line_position(0, 10.44)  # J=0->1
# -> 20.88 cm-1

rotational_line_frequency_GHz(0, 10.44)
# -> 626.4 GHz

# Example 2: Rotational constant from bond length
rotational_constant_B(1.27, 0.98)  # r=1.27 Å, mu=0.98 amu (HCl)
# -> ~10.6 cm-1

# Example 3: Force constant from vibrational frequency
force_constant_from_frequency(2886, 0.98)  # ω=2886 cm-1 (HCl)
# -> ~481 N/m
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
REDUCED_PLANCK = 1.05457182e-34   # J·s
SPEED_OF_LIGHT = 2.99792458e8     # m/s
SPEED_OF_LIGHT_CM = SPEED_OF_LIGHT * 100  # cm/s
BOLTZMANN = 1.380649e-23          # J/K
AMU_TO_KG = 1.66053907e-27        # kg/amu


# =============================================================================
# ROTATIONAL SPECTROSCOPY
# =============================================================================

def rotational_energy_J(J: int, B_cm: float) -> float:
    """
    Calculate rotational energy level in wavenumbers.
    
    E(J) = B·J(J+1)  [in cm-1]
    
    Args:
        J: Rotational quantum number (0, 1, 2, ...)
        B_cm: Rotational constant in cm-1
    
    Returns:
        Energy in cm-1
    
    Example:
        >>> rotational_energy_J(1, 10.44)  # HCl J=1
        20.88
    """
    if J < 0:
        raise ValueError(f"J must be >= 0, got {J}")
    return B_cm * J * (J + 1)


def rotational_energy_joules(J: int, B_cm: float) -> float:
    """
    Calculate rotational energy in Joules.
    
    E(J) = hc·B·J(J+1)
    
    Args:
        J: Rotational quantum number
        B_cm: Rotational constant in cm-1
    
    Returns:
        Energy in Joules
    """
    return PLANCK_CONSTANT * SPEED_OF_LIGHT_CM * rotational_energy_J(J, B_cm)


def rotational_line_position(J_lower: int, B_cm: float) -> float:
    """
    Calculate position of rotational transition J -> J+1.
    
    ν̃ = 2B(J + 1)  [in cm-1]
    
    For microwave spectroscopy, transitions follow DeltaJ = +1.
    
    Args:
        J_lower: Lower rotational quantum number
        B_cm: Rotational constant in cm-1
    
    Returns:
        Line position in cm-1
    
    Example:
        >>> rotational_line_position(0, 10.44)  # HCl J=0->1
        20.88
        >>> rotational_line_position(1, 10.44)  # HCl J=1->2
        41.76
    """
    return 2 * B_cm * (J_lower + 1)


def rotational_line_frequency_GHz(J_lower: int, B_cm: float) -> float:
    """
    Calculate rotational transition frequency in GHz.
    
    ν = 2Bc(J + 1)  [in Hz]
    
    Args:
        J_lower: Lower rotational quantum number
        B_cm: Rotational constant in cm-1
    
    Returns:
        Frequency in GHz
    
    Example:
        >>> rotational_line_frequency_GHz(0, 10.44)  # HCl J=0->1
        626.4...
    """
    freq_Hz = rotational_line_position(J_lower, B_cm) * SPEED_OF_LIGHT_CM
    return freq_Hz / 1e9


def rotational_line_spacing(B_cm: float) -> float:
    """
    Calculate spacing between adjacent rotational lines.
    
    For rigid rotor: Lines are equally spaced by 2B.
    
    Args:
        B_cm: Rotational constant in cm-1
    
    Returns:
        Line spacing in cm-1
    """
    return 2 * B_cm


def rotational_degeneracy(J: int) -> int:
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


def rotational_population(J: int, B_cm: float, temperature: float) -> float:
    """
    Calculate Boltzmann population of rotational level J.
    
    N_J/N_total ∝ (2J+1) exp(-E_J/kT)
    
    Args:
        J: Rotational quantum number
        B_cm: Rotational constant in cm-1
        temperature: Temperature in Kelvin
    
    Returns:
        Relative population (not normalized)
    
    Example:
        >>> rotational_population(0, 10.44, 300)  # HCl J=0 at 300K
    """
    E_J = rotational_energy_joules(J, B_cm)
    g_J = rotational_degeneracy(J)
    return g_J * np.exp(-E_J / (BOLTZMANN * temperature))


def rotational_partition_function_diatomic(B_cm: float, temperature: float) -> float:
    """
    Calculate rotational partition function for diatomic molecule.
    
    q_rot = kT/(Bhc) = T/(Θ_rot)  [high temperature limit]
    
    Args:
        B_cm: Rotational constant in cm-1
        temperature: Temperature in Kelvin
    
    Returns:
        Rotational partition function
    """
    # Convert B from cm-1 to energy
    B_energy = PLANCK_CONSTANT * SPEED_OF_LIGHT_CM * B_cm
    return BOLTZMANN * temperature / B_energy


def most_populated_rotational_level(B_cm: float, temperature: float) -> int:
    """
    Find the most populated rotational level at given temperature.
    
    J_max ~ √(kT/2Bhc) - 1/2 ~ √(T/2Θ_rot) - 1/2
    
    Args:
        B_cm: Rotational constant in cm-1
        temperature: Temperature in Kelvin
    
    Returns:
        Most populated J value (integer)
    
    Example:
        >>> most_populated_rotational_level(10.44, 300)  # HCl at 300K
        3
    """
    # Exact: d/dJ[(2J+1)exp(-BJ(J+1)/kT)] = 0
    # Gives: J_max = -1/2 + √(kT/2Bhc) = -1/2 + √(T/2Θ_rot)
    B_energy = PLANCK_CONSTANT * SPEED_OF_LIGHT_CM * B_cm
    J_max = -0.5 + np.sqrt(BOLTZMANN * temperature / (2 * B_energy))
    return max(0, round(J_max))


def rotational_constant_from_line_spacing(spacing_cm: float) -> float:
    """
    Calculate rotational constant from line spacing.
    
    B = spacing/2
    
    Args:
        spacing_cm: Spacing between adjacent lines in cm-1
    
    Returns:
        Rotational constant B in cm-1
    """
    return spacing_cm / 2


def bond_length_from_B(B_cm: float, reduced_mass_amu: float) -> float:
    """
    Calculate bond length from rotational constant.
    
    B = h/(8pi2cI) = h/(8pi2cmur2)
    r = √(h/(8pi2cmuB))
    
    Args:
        B_cm: Rotational constant in cm-1
        reduced_mass_amu: Reduced mass in amu
    
    Returns:
        Bond length in meters
    
    Example:
        >>> bond_length_from_B(10.44, 0.9796)  # HCl
        1.27e-10  # ~ 127 pm
    """
    mu_kg = reduced_mass_amu * AMU_TO_KG
    B_SI = B_cm * SPEED_OF_LIGHT_CM  # Convert to Hz
    
    # B = h/(8pi2I) -> I = h/(8pi2B)
    # I = mur2 -> r = √(I/mu) = √(h/(8pi2Bmu))
    
    r = np.sqrt(PLANCK_CONSTANT / (8 * np.pi**2 * B_SI * mu_kg))
    return r


def rotational_constant_from_geometry(m1_amu: float, m2_amu: float, 
                                      bond_length_m: float) -> float:
    """
    Calculate rotational constant from atomic masses and bond length.
    
    Args:
        m1_amu, m2_amu: Atomic masses in amu
        bond_length_m: Bond length in meters
    
    Returns:
        Rotational constant B in cm-1
    """
    # Reduced mass
    mu_amu = m1_amu * m2_amu / (m1_amu + m2_amu)
    mu_kg = mu_amu * AMU_TO_KG
    
    # Moment of inertia
    I = mu_kg * bond_length_m**2
    
    # B = h/(8pi2cI) in cm-1
    B = PLANCK_CONSTANT / (8 * np.pi**2 * SPEED_OF_LIGHT_CM * I)
    
    return B


# =============================================================================
# CENTRIFUGAL DISTORTION
# =============================================================================

def rotational_energy_with_distortion(J: int, B_cm: float, D_cm: float) -> float:
    """
    Calculate rotational energy with centrifugal distortion.
    
    E(J) = BJ(J+1) - DJ2(J+1)2
    
    Args:
        J: Rotational quantum number
        B_cm: Rotational constant in cm-1
        D_cm: Centrifugal distortion constant in cm-1
    
    Returns:
        Energy in cm-1
    
    Example:
        >>> rotational_energy_with_distortion(5, 10.44, 5.28e-4)  # HCl J=5
    """
    return B_cm * J * (J + 1) - D_cm * J**2 * (J + 1)**2


def distorted_rotational_line(J_lower: int, B_cm: float, D_cm: float) -> float:
    """
    Calculate rotational line position with distortion correction.
    
    ν̃ = 2B(J+1) - 4D(J+1)3
    
    Args:
        J_lower: Lower rotational quantum number
        B_cm: Rotational constant in cm-1
        D_cm: Centrifugal distortion constant in cm-1
    
    Returns:
        Line position in cm-1
    """
    J = J_lower + 1
    return 2 * B_cm * J - 4 * D_cm * J**3


def centrifugal_distortion_constant(B_cm: float, wavenumber_cm: float) -> float:
    """
    Estimate centrifugal distortion constant from vibrational frequency.
    
    D ~ 4B3/ω2
    
    Args:
        B_cm: Rotational constant in cm-1
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Centrifugal distortion constant D in cm-1
    """
    return 4 * B_cm**3 / wavenumber_cm**2


# =============================================================================
# VIBRATIONAL-ROTATIONAL SPECTROSCOPY
# =============================================================================

def vibrational_energy_v(v: int, wavenumber_cm: float) -> float:
    """
    Calculate harmonic oscillator vibrational energy.
    
    G(v) = ω(v + 1/2)  [in cm-1]
    
    Args:
        v: Vibrational quantum number (0, 1, 2, ...)
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Energy in cm-1
    """
    if v < 0:
        raise ValueError(f"v must be >= 0, got {v}")
    return wavenumber_cm * (v + 0.5)


def vibrational_transition_fundamental(wavenumber_cm: float) -> float:
    """
    Calculate fundamental vibrational transition (v=0->1).
    
    For harmonic oscillator: ν̃ = ω
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Transition wavenumber in cm-1
    """
    return wavenumber_cm


def vibrational_first_overtone(wavenumber_cm: float) -> float:
    """
    Calculate first overtone (v=0->2).
    
    For harmonic oscillator: ν̃ = 2ω
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Overtone wavenumber in cm-1
    """
    return 2 * wavenumber_cm


def anharmonic_vibrational_energy(v: int, omega_e: float, 
                                   omega_e_x_e: float) -> float:
    """
    Calculate anharmonic vibrational energy.
    
    G(v) = ωₑ(v + 1/2) - ωₑxₑ(v + 1/2)2
    
    Args:
        v: Vibrational quantum number
        omega_e: Harmonic frequency in cm-1
        omega_e_x_e: Anharmonicity constant in cm-1
    
    Returns:
        Energy in cm-1
    """
    term = v + 0.5
    return omega_e * term - omega_e_x_e * term**2


def anharmonic_fundamental(omega_e: float, omega_e_x_e: float) -> float:
    """
    Calculate anharmonic fundamental transition.
    
    ν̃01 = ωₑ - 2ωₑxₑ
    
    Args:
        omega_e: Harmonic frequency in cm-1
        omega_e_x_e: Anharmonicity constant in cm-1
    
    Returns:
        Fundamental wavenumber in cm-1
    """
    return omega_e - 2 * omega_e_x_e


def dissociation_energy_vibrational(omega_e: float, omega_e_x_e: float) -> float:
    """
    Calculate dissociation energy from vibrational constants.
    
    D0 = ωₑ2/(4ωₑxₑ) - ωₑ/2
    
    Args:
        omega_e: Harmonic frequency in cm-1
        omega_e_x_e: Anharmonicity constant in cm-1
    
    Returns:
        Dissociation energy D0 in cm-1
    """
    return omega_e**2 / (4 * omega_e_x_e) - omega_e / 2


def rotation_vibration_branch_position(J: int, B_cm: float, 
                                        wavenumber_cm: float,
                                        branch: str = 'R') -> float:
    """
    Calculate line position in vibrational-rotational band.
    
    P-branch (DeltaJ = -1): ν̃_P(J) = ω - 2BJ
    R-branch (DeltaJ = +1): ν̃_R(J) = ω + 2B(J+1)
    
    Args:
        J: Lower rotational quantum number
        B_cm: Rotational constant in cm-1
        wavenumber_cm: Vibrational wavenumber in cm-1
        branch: 'P' or 'R'
    
    Returns:
        Line position in cm-1
    
    Example:
        >>> rotation_vibration_branch_position(0, 10.44, 2886, 'R')  # HCl R(0)
    """
    if branch.upper() == 'P':
        return wavenumber_cm - 2 * B_cm * J
    elif branch.upper() == 'R':
        return wavenumber_cm + 2 * B_cm * (J + 1)
    else:
        raise ValueError(f"Branch must be 'P' or 'R', got {branch}")


def vibration_rotation_band_gap(B_cm: float, wavenumber_cm: float) -> Dict:
    """
    Calculate band origin and spacing in vibration-rotation spectrum.
    
    Returns positions of first few P and R lines.
    
    Args:
        B_cm: Rotational constant in cm-1
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Dictionary with band origin and line positions
    """
    return {
        'origin': wavenumber_cm,
        'P_branch': {
            'P(1)': wavenumber_cm - 2 * B_cm,
            'P(2)': wavenumber_cm - 4 * B_cm,
            'P(3)': wavenumber_cm - 6 * B_cm,
        },
        'R_branch': {
            'R(0)': wavenumber_cm + 2 * B_cm,
            'R(1)': wavenumber_cm + 4 * B_cm,
            'R(2)': wavenumber_cm + 6 * B_cm,
        }
    }


# =============================================================================
# RAMAN SPECTROSCOPY
# =============================================================================

def raman_stokes_shift(wavenumber_cm: float) -> float:
    """
    Calculate Stokes Raman shift.
    
    Stokes lines appear at lower energy (longer wavelength) than incident.
    Shift equals vibrational frequency.
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Stokes shift in cm-1
    """
    return wavenumber_cm


def raman_antistokes_shift(wavenumber_cm: float) -> float:
    """
    Calculate anti-Stokes Raman shift.
    
    Anti-Stokes lines appear at higher energy than incident.
    Same magnitude shift, opposite direction.
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Anti-Stokes shift in cm-1
    """
    return wavenumber_cm


def raman_line_positions(excitation_nm: float, 
                         wavenumber_cm: float) -> Dict[str, float]:
    """
    Calculate Raman line positions for given excitation wavelength.
    
    Args:
        excitation_nm: Excitation laser wavelength in nm
        wavenumber_cm: Vibrational wavenumber in cm-1
    
    Returns:
        Dictionary with Rayleigh, Stokes, and anti-Stokes positions in nm
    
    Example:
        >>> raman_line_positions(532, 1000)  # 532nm laser, 1000 cm-1 mode
    """
    # Convert excitation to cm-1
    excitation_cm = 1e7 / excitation_nm
    
    # Stokes: lower energy, longer wavelength
    stokes_cm = excitation_cm - wavenumber_cm
    stokes_nm = 1e7 / stokes_cm
    
    # Anti-Stokes: higher energy, shorter wavelength
    antistokes_cm = excitation_cm + wavenumber_cm
    antistokes_nm = 1e7 / antistokes_cm
    
    return {
        'excitation_nm': excitation_nm,
        'stokes_nm': stokes_nm,
        'antistokes_nm': antistokes_nm,
        'rayleigh_nm': excitation_nm
    }


def stokes_antistokes_intensity_ratio(wavenumber_cm: float, 
                                        temperature: float) -> float:
    """
    Calculate intensity ratio of Stokes to anti-Stokes Raman lines.
    
    I_Stokes/I_AntiStokes = exp(hcω̃/kT)
    
    Args:
        wavenumber_cm: Vibrational wavenumber in cm-1
        temperature: Temperature in Kelvin
    
    Returns:
        Intensity ratio (Stokes always more intense)
    
    Example:
        >>> stokes_antistokes_intensity_ratio(1000, 300)
        100+  # Stokes much more intense at room temperature
    """
    E_vib = wavenumber_cm * PLANCK_CONSTANT * SPEED_OF_LIGHT_CM
    return np.exp(E_vib / (BOLTZMANN * temperature))


def rotational_raman_selection_rules(J_initial: int) -> List[int]:
    """
    Calculate allowed DeltaJ values for rotational Raman transitions.
    
    For linear molecules: DeltaJ = 0, ±2
    - S-branch: DeltaJ = +2
    - O-branch: DeltaJ = -2
    
    Args:
        J_initial: Initial rotational quantum number
    
    Returns:
        List of allowed DeltaJ values
    """
    return [2, -2] if J_initial >= 2 else [2]


def rotational_raman_line_position(J: int, B_cm: float, branch: str) -> float:
    """
    Calculate rotational Raman line position.
    
    S-branch (DeltaJ = +2): Deltaν̃ = B(4J + 6)
    O-branch (DeltaJ = -2): Deltaν̃ = B(4J - 6)
    
    Args:
        J: Initial rotational quantum number
        B_cm: Rotational constant in cm-1
        branch: 'S' or 'O'
    
    Returns:
        Raman shift in cm-1
    """
    if branch.upper() == 'S':
        return B_cm * (4 * J + 6)
    elif branch.upper() == 'O':
        if J < 2:
            raise ValueError("O-branch requires J ≥ 2")
        return B_cm * (4 * J - 6)
    else:
        raise ValueError(f"Branch must be 'S' or 'O', got {branch}")


# =============================================================================
# SELECTION RULES
# =============================================================================

def rotational_selection_rule_microwave(J_initial: int) -> List[int]:
    """
    Allowed rotational transitions for microwave spectroscopy.
    
    For molecules with permanent dipole moment: DeltaJ = ±1
    
    Args:
        J_initial: Initial rotational quantum number
    
    Returns:
        List of allowed final J values
    """
    return [J_initial - 1, J_initial + 1]


def vibrational_selection_rule_ir(v_initial: int) -> List[int]:
    """
    Allowed vibrational transitions for IR spectroscopy.
    
    For harmonic oscillator: Deltav = ±1
    For anharmonic: Deltav = ±1, ±2, ±3, ... (decreasing intensity)
    
    Args:
        v_initial: Initial vibrational quantum number
    
    Returns:
        List of allowed final v values
    """
    # For harmonic oscillator
    return [v_initial - 1, v_initial + 1]


def is_ir_active(dipole_moment_change: bool) -> bool:
    """
    Determine if vibrational mode is IR active.
    
    IR active if dipole moment changes during vibration.
    
    Args:
        dipole_moment_change: True if dipole moment changes
    
    Returns:
        True if IR active
    """
    return dipole_moment_change


def is_raman_active(polarizability_change: bool) -> bool:
    """
    Determine if vibrational mode is Raman active.
    
    Raman active if polarizability changes during vibration.
    
    Args:
        polarizability_change: True if polarizability changes
    
    Returns:
        True if Raman active
    """
    return polarizability_change


def mutual_exclusion_rule(point_group: str) -> Dict[str, str]:
    """
    Apply mutual exclusion rule for centrosymmetric molecules.
    
    For molecules with center of inversion:
    - IR active modes are Raman inactive
    - Raman active modes are IR inactive
    
    Args:
        point_group: Molecular point group
    
    Returns:
        Dictionary explaining the rule
    """
    centrosymmetric = ['Ci', 'C2h', 'D2h', 'D4h', 'D6h', 'D∞h', 
                       'D3h', 'D5h', 'Oh', 'Td']  # Td is exception
    
    if point_group in centrosymmetric:
        return {
            'centrosymmetric': True,
            'rule': 'Mutual exclusion applies',
            'IR_active': 'ungerade (u) modes',
            'Raman_active': 'gerade (g) modes',
            'mutual_exclusion': 'No mode is both IR and Raman active'
        }
    else:
        return {
            'centrosymmetric': False,
            'rule': 'Mutual exclusion does not apply',
            'note': 'Modes can be both IR and Raman active'
        }


# =============================================================================
# SPECTRAL ANALYSIS UTILITIES
# =============================================================================

def wavelength_to_wavenumber(wavelength_nm: float) -> float:
    """
    Convert wavelength to wavenumber.
    
    ν̃ = 107/lambda  [cm-1]
    
    Args:
        wavelength_nm: Wavelength in nm
    
    Returns:
        Wavenumber in cm-1
    """
    return 1e7 / wavelength_nm


def wavenumber_to_wavelength(wavenumber_cm: float) -> float:
    """
    Convert wavenumber to wavelength.
    
    lambda = 107/ν̃  [nm]
    
    Args:
        wavenumber_cm: Wavenumber in cm-1
    
    Returns:
        Wavelength in nm
    """
    return 1e7 / wavenumber_cm


def frequency_to_wavenumber(frequency_GHz: float) -> float:
    """
    Convert frequency to wavenumber.
    
    ν̃ = ν/c
    
    Args:
        frequency_GHz: Frequency in GHz
    
    Returns:
        Wavenumber in cm-1
    """
    freq_Hz = frequency_GHz * 1e9
    return freq_Hz / SPEED_OF_LIGHT_CM


def wavenumber_to_frequency(wavenumber_cm: float) -> float:
    """
    Convert wavenumber to frequency.
    
    ν = c·ν̃
    
    Args:
        wavenumber_cm: Wavenumber in cm-1
    
    Returns:
        Frequency in GHz
    """
    freq_Hz = wavenumber_cm * SPEED_OF_LIGHT_CM
    return freq_Hz / 1e9


def spectral_resolution_required(delta_nu_cm: float) -> float:
    """
    Calculate required spectral resolution to resolve lines.
    
    Args:
        delta_nu_cm: Line spacing in cm-1
    
    Returns:
        Required resolution in cm-1 (should be < delta_nu)
    """
    return delta_nu_cm / 10  # Typically need 10x finer resolution


def doppler_broadening(wavenumber_cm: float, temperature: float, 
                       mass_amu: float) -> float:
    """
    Calculate Doppler broadening width.
    
    Deltaν̃_D = ν̃·√(2kT ln 2 / mc2)
    
    Args:
        wavenumber_cm: Line position in cm-1
        temperature: Temperature in Kelvin
        mass_amu: Molecular mass in amu
    
    Returns:
        FWHM in cm-1
    """
    mass_kg = mass_amu * AMU_TO_KG
    
    # Doppler width formula
    delta_nu = wavenumber_cm * np.sqrt(
        2 * BOLTZMANN * temperature * np.log(2) / (mass_kg * SPEED_OF_LIGHT**2)
    )
    
    return delta_nu


# =============================================================================
# DIATOMIC MOLECULE DATABASE
# =============================================================================

DIATOMIC_SPECTROSCOPIC_DATA = {
    'H2': {
        'B_cm': 60.864,
        'D_cm': 0.0471,
        'omega_e': 4401.21,
        'omega_e_x_e': 121.34,
        're_pm': 74.14,
        'mu_amu': 0.5039
    },
    'N2': {
        'B_cm': 1.998,
        'D_cm': 5.76e-6,
        'omega_e': 2358.57,
        'omega_e_x_e': 14.32,
        're_pm': 109.77,
        'mu_amu': 7.0015
    },
    'O2': {
        'B_cm': 1.4456,
        'D_cm': 4.84e-6,
        'omega_e': 1580.19,
        'omega_e_x_e': 11.98,
        're_pm': 120.75,
        'mu_amu': 8.0000
    },
    'CO': {
        'B_cm': 1.9313,
        'D_cm': 6.12e-6,
        'omega_e': 2169.81,
        'omega_e_x_e': 13.29,
        're_pm': 112.83,
        'mu_amu': 6.856
    },
    'HCl': {
        'B_cm': 10.593,
        'D_cm': 5.28e-4,
        'omega_e': 2990.95,
        'omega_e_x_e': 52.82,
        're_pm': 127.46,
        'mu_amu': 0.9796
    },
    'HBr': {
        'B_cm': 8.473,
        'D_cm': 3.45e-4,
        'omega_e': 2649.67,
        'omega_e_x_e': 45.21,
        're_pm': 141.44,
        'mu_amu': 0.9956
    },
    'HI': {
        'B_cm': 6.551,
        'D_cm': 1.97e-4,
        'omega_e': 2309.01,
        'omega_e_x_e': 39.64,
        're_pm': 160.92,
        'mu_amu': 1.000
    },
    'NO': {
        'B_cm': 1.7046,
        'D_cm': 5.4e-6,
        'omega_e': 1904.03,
        'omega_e_x_e': 14.06,
        're_pm': 115.08,
        'mu_amu': 7.466
    }
}


def get_spectroscopic_constants(molecule: str) -> Dict:
    """
    Get spectroscopic constants for a diatomic molecule.
    
    Args:
        molecule: Molecule formula (e.g., 'HCl', 'CO', 'N2')
    
    Returns:
        Dictionary of spectroscopic constants
    
    Example:
        >>> get_spectroscopic_constants('HCl')
        {'B_cm': 10.593, 'D_cm': 5.28e-4, ...}
    """
    if molecule in DIATOMIC_SPECTROSCOPIC_DATA:
        return DIATOMIC_SPECTROSCOPIC_DATA[molecule]
    else:
        raise ValueError(f"Molecule {molecule} not in database. "
                        f"Available: {list(DIATOMIC_SPECTROSCOPIC_DATA.keys())}")


def predict_rotational_spectrum(molecule: str, J_max: int = 10) -> List[Dict]:
    """
    Predict rotational spectrum for a diatomic molecule.
    
    Args:
        molecule: Molecule formula
        J_max: Maximum J value to calculate
    
    Returns:
        List of transitions with positions and intensities
    """
    data = get_spectroscopic_constants(molecule)
    B = data['B_cm']
    D = data.get('D_cm', 0)
    
    spectrum = []
    for J in range(J_max):
        # Position with distortion
        position = distorted_rotational_line(J, B, D)
        frequency_GHz = wavenumber_to_frequency(position)
        
        spectrum.append({
            'transition': f'{J}->{J+1}',
            'J_lower': J,
            'position_cm': position,
            'frequency_GHz': frequency_GHz,
            'wavelength_mm': 1e7 / position if position > 0 else None
        })
    
    return spectrum


def predict_vibrational_rotational_band(molecule: str, 
                                         J_max: int = 5) -> Dict:
    """
    Predict vibrational-rotational band structure.
    
    Args:
        molecule: Molecule formula
        J_max: Maximum J value
    
    Returns:
        Dictionary with P and R branch lines
    """
    data = get_spectroscopic_constants(molecule)
    B = data['B_cm']
    omega = data['omega_e']
    omega_x = data.get('omega_e_x_e', 0)
    
    # Fundamental transition
    fundamental = anharmonic_fundamental(omega, omega_x)
    
    P_branch = {}
    R_branch = {}
    
    for J in range(J_max + 1):
        # P-branch (J upper -> J lower)
        if J >= 1:
            P_branch[f'P({J})'] = rotation_vibration_branch_position(
                J, B, fundamental, 'P'
            )
        
        # R-branch (J lower -> J upper)
        R_branch[f'R({J})'] = rotation_vibration_branch_position(
            J, B, fundamental, 'R'
        )
    
    return {
        'molecule': molecule,
        'fundamental_cm': fundamental,
        'band_origin_cm': fundamental,
        'P_branch': P_branch,
        'R_branch': R_branch,
        'band_gap': 4 * B  # Gap between P(1) and R(0)
    }


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Molecular Spectroscopy Tools - Examples")
    print("=" * 60)
    
    # Rotational spectroscopy
    print("\n1. Rotational Spectroscopy (HCl):")
    B = 10.44  # cm-1
    print(f"   J=0->1 transition: {rotational_line_position(0, B):.2f} cm-1")
    print(f"   J=0->1 frequency: {rotational_line_frequency_GHz(0, B):.1f} GHz")
    print(f"   Line spacing: {rotational_line_spacing(B):.2f} cm-1")
    print(f"   Most populated J at 300K: {most_populated_rotational_level(B, 300)}")
    
    # Bond length calculation
    print("\n2. Bond Length from Rotational Constant:")
    r = bond_length_from_B(10.44, 0.9796)  # HCl
    print(f"   HCl bond length: {r*1e12:.1f} pm")
    
    # Vibrational-rotational
    print("\n3. Vibrational-Rotational Spectrum:")
    band = predict_vibrational_rotational_band('HCl', J_max=3)
    print(f"   Band origin: {band['fundamental_cm']:.1f} cm-1")
    print(f"   R(0): {band['R_branch']['R(0)']:.1f} cm-1")
    print(f"   P(1): {band['P_branch']['P(1)']:.1f} cm-1")
    
    # Raman spectroscopy
    print("\n4. Raman Spectroscopy:")
    positions = raman_line_positions(532, 1000)
    print(f"   Excitation: {positions['excitation_nm']} nm")
    print(f"   Stokes: {positions['stokes_nm']:.2f} nm")
    print(f"   Anti-Stokes: {positions['antistokes_nm']:.2f} nm")
    
    ratio = stokes_antistokes_intensity_ratio(1000, 300)
    print(f"   Stokes/Anti-Stokes ratio: {ratio:.1f}")
    
    # Anharmonicity
    print("\n5. Anharmonicity:")
    omega_e = 2990.95
    omega_e_x_e = 52.82
    fundamental = anharmonic_fundamental(omega_e, omega_e_x_e)
    D0 = dissociation_energy_vibrational(omega_e, omega_e_x_e)
    print(f"   ωₑ: {omega_e:.1f} cm-1")
    print(f"   ωₑxₑ: {omega_e_x_e:.1f} cm-1")
    print(f"   Fundamental (0->1): {fundamental:.1f} cm-1")
    print(f"   Dissociation energy: {D0:.1f} cm-1")
    
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
            name="anharmonic_fundamental",
            description="Calculate anharmonic fundamental transition.",
            input_schema=[
            InputSchemaField(name="omega_e", type="number", required=True),
            InputSchemaField(name="omega_e_x_e", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="anharmonic_vibrational_energy",
            description="Calculate anharmonic vibrational energy.",
            input_schema=[
            InputSchemaField(name="v", type="number", required=True),
            InputSchemaField(name="omega_e", type="number", required=True),
            InputSchemaField(name="omega_e_x_e", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="bond_length_from_B",
            description="Calculate bond length from rotational constant.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="reduced_mass_amu", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="centrifugal_distortion_constant",
            description="Estimate centrifugal distortion constant from vibrational frequency.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dissociation_energy_vibrational",
            description="Calculate dissociation energy from vibrational constants.",
            input_schema=[
            InputSchemaField(name="omega_e", type="number", required=True),
            InputSchemaField(name="omega_e_x_e", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="distorted_rotational_line",
            description="Calculate rotational line position with distortion correction.",
            input_schema=[
            InputSchemaField(name="J_lower", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="D_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="doppler_broadening",
            description="Calculate Doppler broadening width.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="mass_amu", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="frequency_to_wavenumber",
            description="Convert frequency to wavenumber.",
            input_schema=[
            InputSchemaField(name="frequency_GHz", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="get_spectroscopic_constants",
            description="Get spectroscopic constants for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="molecule", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_ir_active",
            description="Determine if vibrational mode is IR active.",
            input_schema=[
            InputSchemaField(name="dipole_moment_change", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_raman_active",
            description="Determine if vibrational mode is Raman active.",
            input_schema=[
            InputSchemaField(name="polarizability_change", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="most_populated_rotational_level",
            description="Find the most populated rotational level at given temperature.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mutual_exclusion_rule",
            description="Apply mutual exclusion rule for centrosymmetric molecules.",
            input_schema=[
            InputSchemaField(name="point_group", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_rotational_spectrum",
            description="Predict rotational spectrum for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="molecule", type="string", required=True),
            InputSchemaField(name="J_max", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_vibrational_rotational_band",
            description="Predict vibrational-rotational band structure.",
            input_schema=[
            InputSchemaField(name="molecule", type="string", required=True),
            InputSchemaField(name="J_max", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="raman_antistokes_shift",
            description="Calculate anti-Stokes Raman shift.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="raman_line_positions",
            description="Calculate Raman line positions for given excitation wavelength.",
            input_schema=[
            InputSchemaField(name="excitation_nm", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="raman_stokes_shift",
            description="Calculate Stokes Raman shift.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotation_vibration_branch_position",
            description="Calculate line position in vibrational-rotational band.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="branch", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_constant_from_geometry",
            description="Calculate rotational constant from atomic masses and bond length.",
            input_schema=[
            InputSchemaField(name="m1_amu", type="number", required=True),
            InputSchemaField(name="m2_amu", type="number", required=True),
            InputSchemaField(name="bond_length_m", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_constant_from_line_spacing",
            description="Calculate rotational constant from line spacing.",
            input_schema=[
            InputSchemaField(name="spacing_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_degeneracy",
            description="Calculate degeneracy of rotational level J.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_energy_J",
            description="Calculate rotational energy level in wavenumbers.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_energy_joules",
            description="Calculate rotational energy in Joules.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_energy_with_distortion",
            description="Calculate rotational energy with centrifugal distortion.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="D_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_line_frequency_GHz",
            description="Calculate rotational transition frequency in GHz.",
            input_schema=[
            InputSchemaField(name="J_lower", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_line_position",
            description="Calculate position of rotational transition J -> J+1.",
            input_schema=[
            InputSchemaField(name="J_lower", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_line_spacing",
            description="Calculate spacing between adjacent rotational lines.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_partition_function_diatomic",
            description="Calculate rotational partition function for diatomic molecule.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_population",
            description="Calculate Boltzmann population of rotational level J.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_raman_line_position",
            description="Calculate rotational Raman line position.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="branch", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_raman_selection_rules",
            description="Calculate allowed DeltaJ values for rotational Raman transitions.",
            input_schema=[
            InputSchemaField(name="J_initial", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_selection_rule_microwave",
            description="Allowed rotational transitions for microwave spectroscopy.",
            input_schema=[
            InputSchemaField(name="J_initial", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spectral_resolution_required",
            description="Calculate required spectral resolution to resolve lines.",
            input_schema=[
            InputSchemaField(name="delta_nu_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="stokes_antistokes_intensity_ratio",
            description="Calculate intensity ratio of Stokes to anti-Stokes Raman lines.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibration_rotation_band_gap",
            description="Calculate band origin and spacing in vibration-rotation spectrum.",
            input_schema=[
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_energy_v",
            description="Calculate harmonic oscillator vibrational energy.",
            input_schema=[
            InputSchemaField(name="v", type="number", required=True),
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_first_overtone",
            description="Calculate first overtone (v=0->2).",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_selection_rule_ir",
            description="Allowed vibrational transitions for IR spectroscopy.",
            input_schema=[
            InputSchemaField(name="v_initial", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vibrational_transition_fundamental",
            description="Calculate fundamental vibrational transition (v=0->1).",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavelength_to_wavenumber",
            description="Convert wavelength to wavenumber.",
            input_schema=[
            InputSchemaField(name="wavelength_nm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavenumber_to_frequency",
            description="Convert wavenumber to frequency.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavenumber_to_wavelength",
            description="Convert wavenumber to wavelength.",
            input_schema=[
            InputSchemaField(name="wavenumber_cm", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
