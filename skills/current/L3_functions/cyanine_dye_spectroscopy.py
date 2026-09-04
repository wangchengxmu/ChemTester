"""
Cyanine Dye Spectroscopy - L3 Implementation

Particle-in-a-box model applied to cyanine dye electronic spectra.
Source: Quantum States of Atoms and Molecules (Zielinksi et al.), Ch4

## Solver Instructions (for AI Agent)

When you encounter cyanine dye spectroscopy and particle-in-a-box problems:

### Step 1: Identify what is given and what is asked
- Given: chain length (p carbons or box length L), quantum numbers
- Asked: absorption wavelength, energy levels, transition dipole, oscillator strength

### Step 2: Choose the correct function
- `energy_level(n, L, m)`: E_n = n2h2/(8mL2)
- `absorption_wavelength(L, n_initial, n_final)`: lambda from PIB transition
- `cyanine_wavelength_from_chain(p, N)`: lambda for cyanine dye with p C=C units
- `box_length_from_wavelength(wavelength_nm, N)`: L from observed lambda
- `transition_dipole_moment(L, n_i, n_f)`: Transition dipole integral
- `is_transition_allowed(n_i, n_f)`: Selection rule Deltan = odd
- `oscillator_strength(L, n_i, n_f, wavelength_nm)`: Oscillator strength f

### Step 3: Handle special cases
- For cyanine dyes: L = (p+1) x 1.40 Å (C=C bond length) + 2 x bond extensions
- HOMO = n = (N+1)/2; transition is HOMO -> LUMO: Deltan = 1 (always allowed)
- lambda increases with chain length (red shift with longer chain)

### Examples
```python
cyanine_wavelength_from_chain(9)  # 9 C=C units -> ~500-600 nm
box_length_from_wavelength(500, 10)  # -> L in Å
```
"""

import math
from typing import Tuple

# Physical constants
H = 6.62607015e-34  # Planck constant (J·s)
C = 2.99792458e8    # Speed of light (m/s)
M_E = 9.10938370e-31  # Electron mass (kg)
E_CHARGE = 1.602176634e-19  # Electron charge (C)


def energy_level(n: int, L: float, m: float = M_E) -> float:
    """
    Calculate particle-in-a-box energy level.
    
    E_n = n2h2 / (8mL2)
    
    Args:
        n: Quantum number (positive integer)
        L: Box length (m)
        m: Particle mass (kg), default is electron mass
    
    Returns:
        Energy in Joules
    """
    if n < 1:
        raise ValueError("Quantum number n must be positive integer")
    return (n**2 * H**2) / (8 * m * L**2)


def absorption_wavelength(L: float, n_initial: int, n_final: int) -> float:
    """
    Calculate absorption wavelength for a transition.
    
    lambda = hc / DeltaE = 8mcL2 / [h(n_f2 - n_i2)]
    
    Args:
        L: Box length (m)
        n_initial: Initial quantum number
        n_final: Final quantum number
    
    Returns:
        Wavelength in meters
    """
    if n_final <= n_initial:
        raise ValueError("n_final must be greater than n_initial for absorption")
    
    delta_E = energy_level(n_final, L) - energy_level(n_initial, L)
    return (H * C) / delta_E


def cyanine_wavelength_from_chain(p: int, N: int = None) -> float:
    """
    Calculate absorption wavelength for cyanine dye.
    
    For HOMO->LUMO: lambda = 8mcL2 / [h(2N + 1)]
    Box length L ~ (p + 3) x 139 pm
    
    Args:
        p: Number of carbon atoms in polymethine chain
        N: Number of pi electrons (default: 2p + 3 for simple cyanines)
    
    Returns:
        Wavelength in nanometers
    """
    L = (p + 3) * 139e-12  # Convert pm to m
    if N is None:
        N = 2 * p + 3  # Simple cyanine dyes
    
    # HOMO -> LUMO transition
    n_homo = N // 2
    n_lumo = n_homo + 1
    
    wavelength_m = absorption_wavelength(L, n_homo, n_lumo)
    return wavelength_m * 1e9  # Convert to nm


def box_length_from_wavelength(wavelength_nm: float, N: int) -> float:
    """
    Estimate box length from experimental absorption wavelength.
    
    From lambda = 8mcL2 / [h(2N + 1)] for HOMO->LUMO:
    L = √[lambdah(2N+1) / (8mc)]
    
    Args:
        wavelength_nm: Experimental absorption wavelength (nm)
        N: Number of pi electrons
    
    Returns:
        Box length in picometers
    """
    wavelength_m = wavelength_nm * 1e-9
    L_squared = (wavelength_m * H * (2*N + 1)) / (8 * M_E * C)
    L = math.sqrt(L_squared)
    return L * 1e12  # Convert to pm


def transition_dipole_moment(L: float, n_i: int, n_f: int) -> float:
    """
    Calculate transition dipole moment for particle-in-a-box.
    
    mu_if = (eL/pi2) x 4n_i n_f / (n_f2 - n_i2)2  for Deltan = ±1
    
    Args:
        L: Box length (m)
        n_i: Initial quantum number
        n_f: Final quantum number
    
    Returns:
        Transition dipole moment in Coulomb-meters
    """
    if abs(n_f - n_i) != 1:
        return 0.0  # Forbidden transition
    
    # For allowed transitions (Deltan = ±1)
    numerator = 4 * n_i * n_f
    denominator = (n_f**2 - n_i**2)**2
    
    return (E_CHARGE * L / math.pi**2) * (numerator / denominator)


def is_transition_allowed(n_i: int, n_f: int) -> bool:
    """
    Check if a transition satisfies particle-in-a-box selection rules.
    
    Selection rule: Deltan = ±1
    
    Args:
        n_i: Initial quantum number
        n_f: Final quantum number
    
    Returns:
        True if transition is allowed
    """
    return abs(n_f - n_i) == 1


def oscillator_strength(L: float, n_i: int, n_f: int, wavelength_nm: float) -> float:
    """
    Calculate oscillator strength for a transition.
    
    f = (8pi2m/3h2e2) x E x |mu|2
    
    Args:
        L: Box length (m)
        n_i: Initial quantum number
        n_f: Final quantum number
        wavelength_nm: Transition wavelength (nm)
    
    Returns:
        Oscillator strength (dimensionless)
    """
    mu = transition_dipole_moment(L, n_i, n_f)
    if mu == 0:
        return 0.0
    
    E = (H * C) / (wavelength_nm * 1e-9)  # Energy in Joules
    
    f = (8 * math.pi**2 * M_E / (3 * H**2)) * E * (mu / E_CHARGE)**2
    return f


# TODO: Implement for Pass-3
# - pi_electron_count() - Count pi electrons from molecular structure
# - chain_length_from_structure() - Estimate L from molecular geometry
# - multiple_transitions() - Find all allowed transitions
