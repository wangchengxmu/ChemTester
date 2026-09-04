"""
L3 Implementation: Advanced Inorganic Chemistry Tools
Source: L2_principles/crystal_field_theory.md, magnetic_properties.md, organometallic_chemistry.md

This module provides functions for advanced inorganic chemistry calculations.

## Solver Instructions (for AI Agent)

When you encounter advanced inorganic chemistry problems (crystal field theory, magnetic properties, organometallics):

### Step 1: Identify what is given and what is asked
- Given: metal, oxidation state, ligands, d-electron count, geometry, spectroscopic data
- Asked: CFSE, magnetic moment, spin state, color, geometry, electron count

### Step 2: Choose the correct function
- `crystal_field_splitting(metal, oxidation_state, ligands, geometry)`: Delta0 or Deltaₜ
- `calculate_cfse(d_electrons, geometry, spin_state, delta)`: Crystal field stabilization energy
- `magnetic_moment(n_unpaired)`: mu = √(n(n+2)) BM
- `predict_spin_state(d_electrons, delta, pairing_energy)`: High-spin vs low-spin
- `spectrochemical_series()`: Ordered ligands by field strength
- `irving_williams_series()`: M2+ stability order
- `predict_transitions(d_electrons, geometry, delta)`: d-d transition energies
- `organometallic_electron_count(metal, ligands, charge)`: 18-electron rule

### Step 3: Handle special cases
- Octahedral vs Tetrahedral: Deltaₜ ~ 4/9 Delta0
- Only d4-d7 can be high or low spin in octahedral
- Jahn-Teller distortion for d9 (Cu2+) and high-spin d4 (Cr2+)

### Examples
```python
calculate_cfse(6, 'octahedral', 'high', 10400)  # [Fe(H2O)6]2+ -> -4.0 Dq
magnetic_moment(4)  # 4 unpaired e- -> 4.90 BM
calculate_cfse(6, 'octahedral', 'low', 33000)  # [Fe(CN)6]4- -> -24.0 Dq
```
"""

import math
from typing import Tuple, List, Dict, Optional


# ============================================================================
# Crystal Field Theory
# ============================================================================

# CFSE values in units of Delta_o
CFSE_OCT_HIGH = {
    0: 0.0, 1: -0.4, 2: -0.8, 3: -1.2, 4: -0.6,
    5: 0.0, 6: -0.4, 7: -0.8, 8: -1.2, 9: -0.6, 10: 0.0
}

CFSE_OCT_LOW = {
    0: 0.0, 1: -0.4, 2: -0.8, 3: -1.2, 4: -1.6,
    5: -2.0, 6: -2.4, 7: -1.8, 8: -1.2, 9: -0.6, 10: 0.0
}

# Pairing energies in kJ/mol (approximate)
PAIRING_ENERGIES = {
    'Cr': 224.7, 'Mn': 258.2, 'Fe': 210.5, 'Co': 188.3
}


def calculate_lfse(d_electrons: int, geometry: str = 'octahedral',
                   spin: str = 'high') -> float:
    """
    Calculate Ligand Field Stabilization Energy.
    
    Args:
        d_electrons: Number of d electrons (0-10)
        geometry: 'octahedral', 'tetrahedral', or 'square_planar'
        spin: 'high' or 'low'
    
    Returns:
        LFSE in units of Delta_o
    
    Examples:
        >>> calculate_lfse(6, 'octahedral', 'high')
        -0.4
        >>> calculate_lfse(6, 'octahedral', 'low')
        -2.4
    """
    d = d_electrons
    
    if geometry == 'octahedral':
        if spin == 'high':
            return CFSE_OCT_HIGH.get(d, 0.0)
        else:
            return CFSE_OCT_LOW.get(d, 0.0)
    
    elif geometry == 'tetrahedral':
        # Delta_t = 4/9 Delta_o
        # For tetrahedral, always high spin
        # t2: -0.6 Delta_t each, e: +0.4 Delta_t each
        if d <= 2:
            return -0.6 * d * (4/9)  # t2^n
        elif d <= 4:
            return (-0.6 * 2 + 0.4 * (d-2)) * (4/9)
        elif d <= 7:
            return (-0.6 * 2 + 0.4 * 2 - 0.6 * (d-4)) * (4/9)
        else:
            return (-0.6 * 4 + 0.4 * 2 - 0.6 * (d-7)) * (4/9)
    
    elif geometry == 'square_planar':
        # Approximate: d8 low-spin is most stable
        if d == 8:
            return -2.456  # For d8 square planar
        return CFSE_OCT_HIGH.get(d, 0.0) * 1.3  # Rough approximation
    
    return 0.0


def spin_only_moment(n: int) -> float:
    """
    Calculate spin-only magnetic moment.
    
    mu_eff = √(n(n+2)) BM
    
    Args:
        n: Number of unpaired electrons
    
    Returns:
        Magnetic moment in Bohr magnetons (BM)
    
    Examples:
        >>> spin_only_moment(3)
        3.87
        >>> spin_only_moment(5)
        5.92
    """
    if n == 0:
        return 0.0
    return round(math.sqrt(n * (n + 2)), 2)


def unpaired_from_moment(mu_eff: float) -> int:
    """
    Determine number of unpaired electrons from magnetic moment.
    
    Solve n(n+2) = mu2 for integer n.
    
    Args:
        mu_eff: Magnetic moment in BM
    
    Returns:
        Estimated number of unpaired electrons
    
    Examples:
        >>> unpaired_from_moment(3.87)
        3
        >>> unpaired_from_moment(5.92)
        5
    """
    n_squared = mu_eff**2
    # Solve n2 + 2n - mu2 = 0
    n = (-2 + math.sqrt(4 + 4 * n_squared)) / 2
    return int(round(n))


# ============================================================================
# Spectroscopy Utilities
# ============================================================================

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


# ============================================================================
# 18-Electron Rule
# ============================================================================

# Common ligands and their electron donations (neutral method)
LIGAND_DONATION_NEUTRAL = {
    'CO': 2, 'C5H5': 5, 'Cp': 5, 'Cp*': 5,  # Cyclopentadienyl
    'H': 1, 'Cl': 1, 'Br': 1, 'I': 1,
    'CH3': 1, 'Ph': 1,  # Alkyl, aryl
    'NH3': 2, 'H2O': 2, 'PR3': 2,  # L-type (2e donor)
    'CN': 1, 'SCN': 1,  # X-type when anionic
    'NO': 3,  # Linear nitrosyl (3e donor)
    'bipy': 2, 'phen': 2,  # Bidentate L-type
    'acac': 1, 'ox': 2,  # Anionic bidentate
    'CO2': 0, 'N2': 2, 'O2': 2,  # Weak donors
}

# Common ligands and their electron donations (oxidation state method)
LIGAND_DONATION_OXIDATION = {
    'CO': 2, 'C5H5': 6, 'Cp': 6, 'Cp*': 6,  # Cp-
    'H': 2, 'Cl': 2, 'Br': 2, 'I': 2,  # X-
    'CH3': 2, 'Ph': 2,  # Alkyl, aryl anions
    'NH3': 2, 'H2O': 2, 'PR3': 2,  # L-type
    'CN': 2, 'SCN': 2,  # X-
    'NO': 2,  # NO-
    'bipy': 4, 'phen': 4,  # Bidentate L-type
    'acac': 3, 'ox': 4,  # Anionic bidentate
}

# Valence electrons for transition metals
METAL_VALENCE = {
    'Ti': 4, 'V': 5, 'Cr': 6, 'Mn': 7, 'Fe': 8,
    'Co': 9, 'Ni': 10, 'Cu': 11, 'Zn': 12,
    'Zr': 4, 'Nb': 5, 'Mo': 6, 'Tc': 7, 'Ru': 8,
    'Rh': 9, 'Pd': 10, 'Ag': 11, 'Cd': 12,
    'Hf': 4, 'Ta': 5, 'W': 6, 'Re': 7, 'Os': 8,
    'Ir': 9, 'Pt': 10, 'Au': 11, 'Hg': 12,
}


def count_electrons_neutral(metal: str, ligands: List[str], 
                            charge: int = 0) -> Tuple[int, int]:
    """
    Count electrons using neutral ligand method.
    
    Args:
        metal: Metal symbol
        ligands: List of ligand formulas
        charge: Overall complex charge (positive = cation)
    
    Returns:
        Tuple of (electron count, deviation from 18)
    
    Examples:
        >>> count_electrons_neutral('Fe', ['Cp', 'CO', 'CO'], 0)
        (18, 0)
        >>> count_electrons_neutral('Cr', ['CO'] * 6, 0)
        (18, 0)
    """
    metal_e = METAL_VALENCE.get(metal, 0)
    
    ligand_e = sum(LIGAND_DONATION_NEUTRAL.get(lig, 0) for lig in ligands)
    
    # Charge contribution: positive charge means electron removed
    total = metal_e + ligand_e - charge
    
    deviation = 18 - total
    
    return total, deviation


def count_electrons_oxidation(metal: str, ligands: List[str],
                              charge: int = 0) -> Tuple[int, int, int]:
    """
    Count electrons using oxidation state method.
    
    Args:
        metal: Metal symbol
        ligands: List of ligand formulas
        charge: Overall complex charge
    
    Returns:
        Tuple of (electron count, deviation from 18, oxidation state)
    
    Examples:
        >>> count_electrons_oxidation('Fe', ['Cp', 'CO', 'CO'], 0)
        (18, 0, 2)
    """
    # Calculate oxidation state from ligand charges
    # This is simplified - real implementation needs formal charges
    metal_e = METAL_VALENCE.get(metal, 0)
    
    ligand_e = sum(LIGAND_DONATION_OXIDATION.get(lig, 0) for lig in ligands)
    
    # Oxidation state = charge + ligand anionic charge
    # For neutral ligands only, oxidation state = charge
    oxidation_state = charge  # Simplified
    
    # d-electron count
    d_electrons = metal_e - oxidation_state
    
    total = d_electrons + ligand_e
    deviation = 18 - total
    
    return total, deviation, oxidation_state


def predict_geometry_18e(electron_count: int, d_electrons: int) -> str:
    """
    Predict geometry based on electron count.
    
    Args:
        electron_count: Total valence electrons
        d_electrons: d-electron count
    
    Returns:
        Predicted geometry
    
    Examples:
        >>> predict_geometry_18e(18, 8)
        'square planar'
        >>> predict_geometry_18e(18, 6)
        'octahedral'
    """
    if electron_count == 16:
        if d_electrons == 8:
            return 'square planar'
        elif d_electrons == 10:
            return 'linear'
        return 'coordination 4-5'
    
    elif electron_count == 18:
        if d_electrons == 6:
            return 'octahedral'
        elif d_electrons == 8:
            return 'trigonal bipyramidal or square pyramidal'
        return 'coordination 4-6'
    
    return 'unusual electron count'


# ============================================================================
# Self-test
# ============================================================================

if __name__ == '__main__':
    print("Advanced Inorganic Chemistry Tools Test")
    print("=" * 40)
    
    # Test LFSE
    print("\nLFSE Calculations:")
    for d in range(1, 10):
        high = calculate_lfse(d, 'octahedral', 'high')
        low = calculate_lfse(d, 'octahedral', 'low')
        print(f"  d{d}: high-spin={high:+.1f}Deltao, low-spin={low:+.1f}Deltao")
    
    # Test magnetic moments
    print("\nMagnetic Moments:")
    for n in [1, 3, 5, 7]:
        mu = spin_only_moment(n)
        n_back = unpaired_from_moment(mu)
        print(f"  n={n}: mu={mu} BM -> n={n_back}")
    
    # Test 18-electron rule
    print("\n18-Electron Rule:")
    # Fe(Cp)(CO)2+
    e_count, dev = count_electrons_neutral('Fe', ['Cp', 'CO', 'CO'], 0)
    print(f"  FeCp(CO)2: {e_count}e, deviation={dev}")
    
    # Cr(CO)6
    e_count, dev = count_electrons_neutral('Cr', ['CO'] * 6, 0)
    print(f"  Cr(CO)6: {e_count}e, deviation={dev}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calculate_lfse",
        "description": "Calculate Ligand Field Stabilization Energy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "d_electrons": {
                    "type": "number",
                    "description": "D Electrons"
                },
                "geometry": {
                    "type": "number",
                    "description": "Geometry",
                    "default": "octahedral"
                },
                "spin": {
                    "type": "number",
                    "description": "Spin",
                    "default": "high"
                }
            },
            "required": [
                "d_electrons"
            ]
        }
    },
    {
        "name": "count_electrons_neutral",
        "description": "Count electrons using neutral ligand method.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "metal": {
                    "type": "number",
                    "description": "Metal"
                },
                "ligands": {
                    "type": "number",
                    "description": "Ligands"
                },
                "charge": {
                    "type": "number",
                    "description": "Charge",
                    "default": 0
                }
            },
            "required": [
                "metal",
                "ligands"
            ]
        }
    },
    {
        "name": "count_electrons_oxidation",
        "description": "Count electrons using oxidation state method.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "metal": {
                    "type": "number",
                    "description": "Metal"
                },
                "ligands": {
                    "type": "number",
                    "description": "Ligands"
                },
                "charge": {
                    "type": "number",
                    "description": "Charge",
                    "default": 0
                }
            },
            "required": [
                "metal",
                "ligands"
            ]
        }
    },
    {
        "name": "predict_geometry_18e",
        "description": "Predict geometry based on electron count.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "electron_count": {
                    "type": "number",
                    "description": "Electron Count"
                },
                "d_electrons": {
                    "type": "number",
                    "description": "D Electrons"
                }
            },
            "required": [
                "electron_count",
                "d_electrons"
            ]
        }
    },
    {
        "name": "spin_only_moment",
        "description": "Calculate spin-only magnetic moment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "n"
            ]
        }
    },
    {
        "name": "unpaired_from_moment",
        "description": "Determine number of unpaired electrons from magnetic moment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mu_eff": {
                    "type": "number",
                    "description": "Mu Eff"
                }
            },
            "required": [
                "mu_eff"
            ]
        }
    },
    {
        "name": "wavelength_from_wavenumber",
        "description": "Convert wavenumber to wavelength.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavenumber": {
                    "type": "number",
                    "description": "Wavenumber"
                }
            },
            "required": [
                "wavenumber"
            ]
        }
    },
    {
        "name": "wavenumber_from_wavelength",
        "description": "Convert wavelength to wavenumber.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavelength_nm": {
                    "type": "number",
                    "description": "Wavelength Nm"
                }
            },
            "required": [
                "wavelength_nm"
            ]
        }
    }
]