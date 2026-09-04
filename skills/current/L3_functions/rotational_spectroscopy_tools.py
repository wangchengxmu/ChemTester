"""
L3 Implementation: Rotational Spectroscopy Tools
Source: L2_principles/rotational_spectroscopy.md

This module provides functions for microwave/rotational spectroscopy calculations.

## Solver Instructions (for AI Agent)

When you encounter rotational spectroscopy problems (microwave spectra, bond lengths, moments of inertia, rotational constants), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Moment of inertia**: Given two atomic masses and bond length -> find I
- **Rotational constant**: Given I -> find B (or vice versa)
- **Energy levels**: Given J and B -> find rotational energy
- **Transition frequencies**: Given B -> find J->J+1 transition frequencies
- **Bond length from spectrum**: Given transition frequency and masses -> find bond length r
- **Selection rules**: Check if transition J->J' is allowed (DeltaJ = ±1)

### Step 2: Choose the correct function
- `moment_of_inertia_diatomic(m1, m2, r)` -> I = mur2 (m1, m2 in amu, r in meters)
- `rotational_constant(I)` -> B = h/(8pi2cI) in cm-1
- `rotational_energy(J, B, D=0)` -> E_J = BJ(J+1) - DJ2(J+1)2 in cm-1
- `transition_frequency(J, B)` -> ν = 2B(J+1) in cm-1 for J->J+1
- `bond_length_from_spectrum(freq_cm, m1, m2)` -> solve for r from observed transition
- `centrifugal_distortion(D, B)` -> correction to rigid rotor model
- `population_at_J(J, B, T)` -> Boltzmann population of rotational level

### Step 3: Handle special cases
- Masses in amu (not kg); bond length in meters (not Å - convert by x1e-10)
- Diatomic only: linear molecules have one I; symmetric tops and asymmetric tops need I_A, I_B, I_C
- Selection rule: DeltaJ = ±1 (absorption) -> transitions are evenly spaced by 2B
- Centrifugal distortion D is small; only matters for high J or high precision
- Homonuclear diatomics (N2, O2) have no microwave spectrum (zero dipole moment)

### Examples
1. **Moment of inertia - HCl**: m1=1.008 amu, m2=35.45 amu, r=1.27e-10 m
   -> `moment_of_inertia_diatomic(1.008, 35.45, 1.27e-10)` -> 2.64e-47 kg·m2
   -> `rotational_constant(2.64e-47)` -> B ~ 10.6 cm-1

2. **Transition frequencies - CO**: B = 1.9227 cm-1
   -> J=0->1: `transition_frequency(0, 1.9227)` -> 3.85 cm-1
   -> J=1->2: `transition_frequency(1, 1.9227)` -> 7.69 cm-1 (spacing = 2B)

3. **Bond length from spectrum**: 12C16O, J=0->1 at 3.842 cm-1
   -> `bond_length_from_spectrum(3.842, 12.0, 15.995)` -> r ~ 1.13 Å
"""

import math
from typing import Union, Tuple

# Physical constants
H_PLANCK = 6.62607015e-34  # J·s
C_SPEED = 2.99792458e10    # cm/s (in cm-1 units)
AMU = 1.66053906660e-27    # kg


def moment_of_inertia_diatomic(m1: float, m2: float, r: float) -> float:
    """
    Calculate moment of inertia for a diatomic molecule.
    
    I = mur2 where mu = m1m2/(m1+m2)
    
    Args:
        m1: Mass of atom 1 in amu
        m2: Mass of atom 2 in amu
        r: Bond length in meters
    
    Returns:
        Moment of inertia in kg·m2
    
    Examples:
        >>> # HCl: H=1.008 amu, Cl=35.45 amu, r=1.27 Å
        >>> I = moment_of_inertia_diatomic(1.008, 35.45, 1.27e-10)
        >>> f"{I:.4e}"
        '2.6424e-47'
    """
    # Convert amu to kg
    m1_kg = m1 * AMU
    m2_kg = m2 * AMU
    
    # Reduced mass
    mu = (m1_kg * m2_kg) / (m1_kg + m2_kg)
    
    return mu * r**2


def rotational_constant(I: float) -> float:
    """
    Calculate rotational constant B from moment of inertia.
    
    B = h/(8pi2cI) in cm-1
    
    Args:
        I: Moment of inertia in kg·m2
    
    Returns:
        Rotational constant B in cm-1
    
    Examples:
        >>> # CO: I = 1.46e-46 kg·m2
        >>> B = rotational_constant(1.46e-46)
        >>> f"{B:.4f}"
        '1.9227'
    """
    return H_PLANCK / (8 * math.pi**2 * C_SPEED * I)


def rotational_energy(J: int, B: float, D: float = 0) -> float:
    """
    Calculate rotational energy level.
    
    E_J = BJ(J+1) - DJ2(J+1)2 (in cm-1)
    
    Args:
        J: Rotational quantum number
        B: Rotational constant in cm-1
        D: Centrifugal distortion constant in cm-1 (default: 0)
    
    Returns:
        Energy in cm-1
    
    Examples:
        >>> rotational_energy(2, 1.93, 0)
        11.58
        >>> rotational_energy(2, 1.93, 6e-6)
        11.57985416
    """
    E = B * J * (J + 1)
    if D != 0:
        E -= D * J**2 * (J + 1)**2
    return E


def transition_frequency(J_lower: int, B: float, D: float = 0) -> float:
    """
    Calculate transition frequency for DeltaJ = +1 (R-branch).
    
    ν = 2B(J+1) - 4D(J+1)3
    
    Args:
        J_lower: Lower J value (J'')
        B: Rotational constant in cm-1
        D: Centrifugal distortion constant in cm-1 (default: 0)
    
    Returns:
        Transition frequency in cm-1
    
    Examples:
        >>> transition_frequency(0, 1.93)  # J=0->1
        3.86
        >>> transition_frequency(1, 1.93)  # J=1->2
        5.79
    """
    J = J_lower
    nu = 2 * B * (J + 1)
    if D != 0:
        nu -= 4 * D * (J + 1)**3
    return nu


def wavenumber_from_wavelength(wavelength_nm: float) -> float:
    """
    Convert wavelength to wavenumber.
    
    ṽ = 107/lambda (nm to cm-1)
    
    Args:
        wavelength_nm: Wavelength in nanometers
    
    Returns:
        Wavenumber in cm-1
    
    Examples:
        >>> wavenumber_from_wavelength(500)
        20000.0
        >>> wavenumber_from_wavelength(1000)
        10000.0
    """
    return 1e7 / wavelength_nm


def wavelength_from_wavenumber(wavenumber: float) -> float:
    """
    Convert wavenumber to wavelength.
    
    Args:
        wavenumber: Wavenumber in cm-1
    
    Returns:
        Wavelength in nm
    
    Examples:
        >>> wavelength_from_wavenumber(20000)
        500.0
    """
    return 1e7 / wavenumber


def boltzmann_population(J: int, B: float, T: float) -> float:
    """
    Calculate Boltzmann population of rotational level.
    
    n_J/n0 = (2J+1)exp(-E_J/kT)
    
    Args:
        J: Rotational quantum number
        B: Rotational constant in cm-1
        T: Temperature in Kelvin
    
    Returns:
        Relative population n_J/n0
    
    Examples:
        >>> boltzmann_population(0, 1.93, 300)
        1.0
        >>> boltzmann_population(1, 1.93, 300)
        5.7049
    """
    # k in cm-1/K
    k_B_cm = 0.695  # cm-1/K
    
    E_J = rotational_energy(J, B)
    degeneracy = 2 * J + 1
    
    return degeneracy * math.exp(-E_J / (k_B_cm * T))


def j_max(B: float, T: float) -> int:
    """
    Calculate most populated J level.
    
    J_max = √(kT/2hcB) - 1/2
    
    Args:
        B: Rotational constant in cm-1
        T: Temperature in Kelvin
    
    Returns:
        Most populated J quantum number
    
    Examples:
        >>> j_max(1.93, 300)
        6
    """
    # k in cm-1/K
    k_B_cm = 0.695
    
    J_max = math.sqrt(k_B_cm * T / (2 * B)) - 0.5
    return int(round(J_max))


def bond_length_from_B(B: float, m1: float, m2: float) -> float:
    """
    Calculate bond length from rotational constant.
    
    Args:
        B: Rotational constant in cm-1
        m1: Mass of atom 1 in amu
        m2: Mass of atom 2 in amu
    
    Returns:
        Bond length in meters
    
    Examples:
        >>> # From B = 1.93 cm-1 for CO
        >>> r = bond_length_from_B(1.93, 12.0, 16.0)
        >>> f"{r*1e10:.3f}"  # in Angstroms
        '1.131'
    """
    # Calculate I from B
    I = H_PLANCK / (8 * math.pi**2 * C_SPEED * B)
    
    # Convert masses to kg
    m1_kg = m1 * AMU
    m2_kg = m2 * AMU
    
    # Reduced mass
    mu = (m1_kg * m2_kg) / (m1_kg + m2_kg)
    
    # r = √(I/mu)
    return math.sqrt(I / mu)


# ============================================================================
# Self-test
# ============================================================================

if __name__ == '__main__':
    print("Rotational Spectroscopy Tools Test")
    print("=" * 40)
    
    # Test diatomic calculations
    print("\nHCl Rotational Analysis:")
    I = moment_of_inertia_diatomic(1.008, 35.45, 1.27e-10)
    B = rotational_constant(I)
    print(f"  I = {I:.4e} kg·m2")
    print(f"  B = {B:.4f} cm-1")
    
    # Test transitions
    print("\nTransition frequencies (B = 1.93 cm-1):")
    for J in range(4):
        print(f"  J={J}->{J+1}: {transition_frequency(J, 1.93):.2f} cm-1")
    
    # Test population
    print("\nJ_max at 300 K for B = 1.93 cm-1:")
    print(f"  J_max = {j_max(1.93, 300)}")
    
    # Test conversions
    print("\nWavelength ↔ Wavenumber:")
    print(f"  500 nm = {wavenumber_from_wavelength(500)} cm-1")
    print(f"  20000 cm-1 = {wavelength_from_wavenumber(20000)} nm")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="boltzmann_population",
            description="Calculate Boltzmann population of rotational level.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="bond_length_from_B",
            description="Calculate bond length from rotational constant.",
            input_schema=[
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="m1", type="number", required=True),
            InputSchemaField(name="m2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="j_max",
            description="Calculate most populated J level.",
            input_schema=[
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="moment_of_inertia_diatomic",
            description="Calculate moment of inertia for a diatomic molecule.",
            input_schema=[
            InputSchemaField(name="m1", type="number", required=True),
            InputSchemaField(name="m2", type="number", required=True),
            InputSchemaField(name="r", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_constant",
            description="Calculate rotational constant B from moment of inertia.",
            input_schema=[
            InputSchemaField(name="I", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotational_energy",
            description="Calculate rotational energy level.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="D", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="transition_frequency",
            description="Calculate transition frequency for DeltaJ = +1 (R-branch).",
            input_schema=[
            InputSchemaField(name="J_lower", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="D", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavelength_from_wavenumber",
            description="Convert wavenumber to wavelength.",
            input_schema=[
            InputSchemaField(name="wavenumber", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavenumber_from_wavelength",
            description="Convert wavelength to wavenumber.",
            input_schema=[
            InputSchemaField(name="wavelength_nm", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
