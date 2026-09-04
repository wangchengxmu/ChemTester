"""
Computational Organic Chemistry Workflow - L3 Implementation

Helper functions for computational chemistry calculations.
Source: Understanding Organic Chemistry Through Computation (Boaz and Pearce), Ch1-6

## Solver Instructions (for AI Agent)

When you encounter computational organic chemistry workflow problems (energy conversions, frequency analysis, HOMO-LUMO):

### Step 1: Identify what is given and what is asked
- Given: energies in Hartrees, vibrational frequencies (cm-1), HOMO/LUMO energies
- Asked: energy conversions, minimum/transition state check, HOMO-LUMO gap, ZPE, thermal corrections, reaction thermodynamics

### Step 2: Choose the correct function
- `hartree_to_ev(energy_hartree)`: 1 Ha = 27.211 eV
- `hartree_to_kcal(energy_hartree)`: 1 Ha = 627.509 kcal/mol
- `hartree_to_kjmol(energy_hartree)`: 1 Ha = 2625.5 kJ/mol
- `frequency_to_wavenumber(frequency_cm)`: Pass-through for cm-1
- `check_minimum(frequencies)`: True if all freqs > 0 (no imaginary)
- `homo_lumo_gap(homo_energy, lumo_energy)`: Gap in eV, plus chemical interpretation
- `zpe_correction(frequencies)`: Zero-point energy from vibrational frequencies
- `thermal_energy(frequencies, temperature)`: Thermal energy correction
- `is_reaction_exothermic(reactant_energy, product_energy)`: DeltaE < 0 check

### Step 3: Handle special cases
- 1 imaginary frequency = transition state; 0 = minimum; 2+ = higher order saddle
- ZPE = ½ Σ hνᵢ for all vibrations; always positive
- Typical HOMO-LUMO gap: ~5-9 eV for stable organics; <3 eV may indicate instability

### Examples
```python
check_minimum([100, 200, 300])  # -> True (minimum)
homo_lumo_gap(-0.25, -0.02)  # -> gap = 6.26 eV
hartree_to_kcal(-0.05)  # -> -31.38 kcal/mol
```
"""

import math
from typing import Tuple, Optional


def hartree_to_ev(energy_hartree: float) -> float:
    """Convert Hartree to eV."""
    return energy_hartree * 27.2114


def hartree_to_kcal(energy_hartree: float) -> float:
    """Convert Hartree to kcal/mol."""
    return energy_hartree * 627.509


def hartree_to_kjmol(energy_hartree: float) -> float:
    """Convert Hartree to kJ/mol."""
    return energy_hartree * 2625.5


def frequency_to_wavenumber(frequency_cm: float) -> float:
    """
    Check if frequency is valid (positive for real modes).
    
    Args:
        frequency_cm: Frequency in cm-1
    
    Returns:
        Same value if positive, None if negative (imaginary mode)
    """
    if frequency_cm < 0:
        return None  # Imaginary frequency - transition state
    return frequency_cm


def check_minimum(frequencies: list) -> Tuple[bool, int]:
    """
    Check if structure is a minimum (no imaginary frequencies).
    
    Args:
        frequencies: List of vibrational frequencies (cm-1)
    
    Returns:
        (is_minimum, num_imaginary)
    """
    imaginary = sum(1 for f in frequencies if f < 0)
    return (imaginary == 0, imaginary)


def homo_lumo_gap(homo_energy: float, lumo_energy: float) -> dict:
    """
    Calculate HOMO-LUMO gap properties.
    
    Args:
        homo_energy: HOMO energy (Hartree)
        lumo_energy: LUMO energy (Hartree)
    
    Returns:
        Dictionary with gap in various units
    """
    gap_hartree = lumo_energy - homo_energy
    
    return {
        "gap_hartree": gap_hartree,
        "gap_ev": hartree_to_ev(gap_hartree),
        "gap_kcal": hartree_to_kcal(gap_hartree),
        "gap_kjmol": hartree_to_kjmol(gap_hartree),
        "homo_ev": hartree_to_ev(homo_energy),
        "lumo_ev": hartree_to_ev(lumo_energy)
    }


def zpe_correction(frequencies: list) -> float:
    """
    Calculate Zero Point Energy correction.
    
    ZPE = Σ (1/2) hν for all vibrational modes
    
    Args:
        frequencies: List of vibrational frequencies (cm-1)
    
    Returns:
        ZPE in Hartree
    """
    # Constants
    h = 6.626e-34  # J·s
    c = 2.998e10   # cm/s
    NA = 6.022e23  # Avogadro
    hartree = 4.3597e-18  # J
    
    zpe_joules = 0.0
    for freq in frequencies:
        if freq > 0:  # Skip imaginary frequencies
            zpe_joules += 0.5 * h * c * freq
    
    # Convert to Hartree
    zpe_hartree = zpe_joules / hartree
    return zpe_hartree


def thermal_energy(frequencies: list, temperature: float = 298.15) -> float:
    """
    Calculate thermal energy contribution (without ZPE).
    
    E_thermal = Σ hν/(exp(hν/kT) - 1)
    
    Args:
        frequencies: List of vibrational frequencies (cm-1)
        temperature: Temperature in K
    
    Returns:
        Thermal energy in Hartree
    """
    h = 6.626e-34  # J·s
    c = 2.998e10   # cm/s
    k = 1.381e-23  # J/K
    hartree = 4.3597e-18  # J
    
    e_thermal = 0.0
    for freq in frequencies:
        if freq > 0:
            nu = freq * c  # Hz
            exponent = h * nu / (k * temperature)
            if exponent < 100:  # Avoid overflow
                e_thermal += h * nu / (math.exp(exponent) - 1)
    
    return e_thermal / hartree


def is_reaction_exothermic(reactant_energy: float, product_energy: float) -> bool:
    """
    Check if reaction is exothermic.
    
    Args:
        reactant_energy: Reactant total energy (Hartree)
        product_energy: Product total energy (Hartree)
    
    Returns:
        True if exothermic (product lower energy)
    """
    return product_energy < reactant_energy


# TODO: Implement for Pass-3
# - parse_orca_output() - Extract energies, frequencies from ORCA
# - generate_input_file() - Create ORCA input
# - solvation_model() - Implicit solvent calculations
