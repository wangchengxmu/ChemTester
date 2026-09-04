"""
Computational Quantum Chemistry Tools - L3 Implementation

Core functions for computational quantum chemistry:
- Hartree-Fock energy calculations
- Basis set properties and notation
- DFT functional classification
- Electron correlation methods

Source: LibreTexts Physical Chemistry Ch11

## Solver Instructions (for AI Agent)

When you encounter quantum chemistry calculations (Hartree-Fock, basis sets, DFT functionals, electron correlation):

### Step 1: Identify what is given and what is asked
- Given: method, basis set, molecule, or computational parameters
- Asked: HF energy, basis set info, functional type, electron correlation, basis recommendations

### Step 2: Choose the correct function
- `hartree_fock_energy(...)`: Hartree-Fock energy calculation
- `slater_determinant_normalization(n_electrons)`: Normalization factor
- `fock_matrix_element(...)`: Fock matrix element
- `koopmans_ionization_potential(orbital_energy)`: IP ~ -ε (Koopmans' theorem)
- `basis_set_info(basis_name)`: Information about STO-3G, 6-31G*, cc-pVDZ, etc.
- `sto_ng_exponent(n, zeta, element)`: STO-nG exponents
- `count_basis_functions(formula, basis_name)`: Total basis functions for a molecule
- `functional_type(functional_name)`: Classify DFT functional (LDA/GGA/hybrid/meta-GGA)
- `dft_functional_hierarchy()`: Full hierarchy of DFT functionals
- `electron_correlation_energy(...)`: Post-HF correlation energy
- `mp2_energy_contribution(...)`: MP2 correlation correction
- `parse_basis_notation(notation)`: Parse basis set notation
- `recommend_basis_set(element, property, accuracy)`: Basis set recommendation

### Step 3: Handle special cases
- Koopmans' theorem: IP ~ -ε_HOMO (HF only, no relaxation)
- MP2 = 2nd order Møller-Plesset; good for dispersion and weak interactions
- Basis set hierarchy: minimal (STO-3G) < split-valence (6-31G) < polarized (6-31G*) < diffuse (6-31+G*)

### Examples
```python
basis_set_info('6-31G*')  # -> split-valence + polarization
functional_type('B3LYP')  # -> 'hybrid GGA'
recommend_basis_set('C', 'geometry', 'medium')  # -> 6-31G*
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict, Callable
import numpy as np

# Physical constants (atomic units)
HARTREE_TO_EV = 27.2114  # eV
BOHR_TO_ANGSTROM = 0.529177  # Å


# =============================================================================
# BASIS SET DATABASE
# =============================================================================

# STO-nG minimal basis set exponents
# Format: {element: {n: [alpha values]}}
STO_NG_EXPONENTS = {
    'H': {
        3: [0.3425250914E+00, 0.6239137298E+00, 0.1688554040E+01],
        4: [0.1219492295E+00, 0.2841281879E+00, 0.6944915067E+00, 0.2591266824E+01],
        6: [0.5627147265E-01, 0.1274281247E+00, 0.2360287543E+00, 0.4331826074E+00,
            0.8382902973E+00, 0.2930260718E+01]
    },
    'C': {
        3: [0.1688554040E+00, 0.6239137298E+00, 0.3425250914E+01],  # 1s
    },
    'O': {
        3: [0.2416094253E+00, 0.8616815785E+00, 0.4440882594E+01],  # 1s
    }
}

# Basis set properties
BASIS_SET_INFO = {
    # Minimal basis sets
    'STO-3G': {
        'type': 'minimal',
        'n_primitives': 3,
        'split': False,
        'polarization': False,
        'diffuse': False,
        'functions_per_atom': {'H': 1, 'C': 5, 'N': 5, 'O': 5, 'F': 5},
        'description': 'Minimal basis, 3 Gaussians per STO'
    },
    'STO-4G': {
        'type': 'minimal',
        'n_primitives': 4,
        'split': False,
        'polarization': False,
        'diffuse': False,
        'description': 'Minimal basis, 4 Gaussians per STO'
    },
    'STO-6G': {
        'type': 'minimal',
        'n_primitives': 6,
        'split': False,
        'polarization': False,
        'diffuse': False,
        'description': 'Minimal basis, 6 Gaussians per STO'
    },
    
    # Split-valence basis sets
    '3-21G': {
        'type': 'split-valence',
        'core_primitives': 3,
        'valence_split': [2, 1],
        'polarization': False,
        'diffuse': False,
        'functions_per_atom': {'H': 2, 'C': 9, 'N': 9, 'O': 9},
        'description': 'Split-valence double-zeta'
    },
    '4-31G': {
        'type': 'split-valence',
        'core_primitives': 4,
        'valence_split': [3, 1],
        'polarization': False,
        'diffuse': False,
        'description': 'Split-valence double-zeta'
    },
    '6-31G': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1],
        'polarization': False,
        'diffuse': False,
        'functions_per_atom': {'H': 2, 'C': 9, 'N': 9, 'O': 9},
        'description': 'Split-valence double-zeta, standard'
    },
    '6-311G': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1, 1],
        'polarization': False,
        'diffuse': False,
        'functions_per_atom': {'H': 3, 'C': 13, 'N': 13, 'O': 13},
        'description': 'Split-valence triple-zeta'
    },
    
    # Polarized basis sets
    '6-31G*': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1],
        'polarization': True,
        'polarization_functions': {'heavy': 'd', 'H': None},
        'diffuse': False,
        'functions_per_atom': {'H': 2, 'C': 15, 'N': 15, 'O': 15},
        'description': '6-31G with d polarization on heavy atoms'
    },
    '6-31G**': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1],
        'polarization': True,
        'polarization_functions': {'heavy': 'd', 'H': 'p'},
        'diffuse': False,
        'functions_per_atom': {'H': 5, 'C': 15, 'N': 15, 'O': 15},
        'description': '6-31G with d polarization on heavy atoms, p on H'
    },
    '6-311G*': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1, 1],
        'polarization': True,
        'polarization_functions': {'heavy': 'd', 'H': None},
        'diffuse': False,
        'functions_per_atom': {'H': 3, 'C': 18, 'N': 18, 'O': 18},
        'description': 'Triple-zeta with d polarization'
    },
    
    # Diffuse basis sets
    '6-31+G*': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1],
        'polarization': True,
        'polarization_functions': {'heavy': 'd', 'H': None},
        'diffuse': True,
        'diffuse_functions': {'heavy': True, 'H': False},
        'functions_per_atom': {'H': 2, 'C': 19, 'N': 19, 'O': 19},
        'description': '6-31G* with diffuse functions on heavy atoms'
    },
    '6-31++G**': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1],
        'polarization': True,
        'polarization_functions': {'heavy': 'd', 'H': 'p'},
        'diffuse': True,
        'diffuse_functions': {'heavy': True, 'H': True},
        'description': '6-31G** with diffuse on all atoms'
    },
    '6-311+G**': {
        'type': 'split-valence',
        'core_primitives': 6,
        'valence_split': [3, 1, 1],
        'polarization': True,
        'polarization_functions': {'heavy': 'd', 'H': 'p'},
        'diffuse': True,
        'diffuse_functions': {'heavy': True, 'H': True},
        'description': 'Triple-zeta with polarization and diffuse'
    },
    
    # Correlation-consistent basis sets (Dunning)
    'cc-pVDZ': {
        'type': 'correlation-consistent',
        'zeta': 'double',
        'polarization': True,
        'diffuse': False,
        'description': 'Correlation-consistent polarized double-zeta'
    },
    'cc-pVTZ': {
        'type': 'correlation-consistent',
        'zeta': 'triple',
        'polarization': True,
        'diffuse': False,
        'description': 'Correlation-consistent polarized triple-zeta'
    },
    'aug-cc-pVDZ': {
        'type': 'correlation-consistent',
        'zeta': 'double',
        'polarization': True,
        'diffuse': True,
        'description': 'Augmented cc-pVDZ (with diffuse)'
    },
    'aug-cc-pVTZ': {
        'type': 'correlation-consistent',
        'zeta': 'triple',
        'polarization': True,
        'diffuse': True,
        'description': 'Augmented cc-pVTZ (with diffuse)'
    }
}

# DFT functional classification
DFT_FUNCTIONALS = {
    # LDA functionals
    'SVWN': {
        'type': 'LDA',
        'exchange': 'Slater (LDA)',
        'correlation': 'VWN',
        'hf_exchange': 0.0,
        'description': 'Local density approximation'
    },
    
    # GGA functionals
    'BLYP': {
        'type': 'GGA',
        'exchange': 'Becke88',
        'correlation': 'LYP',
        'hf_exchange': 0.0,
        'description': 'Generalized gradient approximation'
    },
    'PBE': {
        'type': 'GGA',
        'exchange': 'PBE',
        'correlation': 'PBE',
        'hf_exchange': 0.0,
        'description': 'Perdew-Burke-Ernzerhof GGA'
    },
    'PW91': {
        'type': 'GGA',
        'exchange': 'PW91',
        'correlation': 'PW91',
        'hf_exchange': 0.0,
        'description': 'Perdew-Wang 1991 GGA'
    },
    
    # Hybrid functionals
    'B3LYP': {
        'type': 'hybrid',
        'exchange': 'Becke88 + HF',
        'correlation': 'LYP',
        'hf_exchange': 0.20,
        'description': 'Becke 3-parameter hybrid, most popular'
    },
    'PBE0': {
        'type': 'hybrid',
        'exchange': 'PBE + HF',
        'correlation': 'PBE',
        'hf_exchange': 0.25,
        'description': 'PBE hybrid with 25% HF exchange'
    },
    'B3PW91': {
        'type': 'hybrid',
        'exchange': 'Becke88 + HF',
        'correlation': 'PW91',
        'hf_exchange': 0.20,
        'description': 'B3 hybrid with PW91 correlation'
    },
    
    # Meta-GGA functionals
    'TPSS': {
        'type': 'meta-GGA',
        'exchange': 'TPSS',
        'correlation': 'TPSS',
        'hf_exchange': 0.0,
        'description': 'Tao-Perdew-Staroverov-Scuseria meta-GGA'
    },
    'M06-2X': {
        'type': 'meta-GGA',
        'exchange': 'M06-2X',
        'correlation': 'M06-2X',
        'hf_exchange': 0.54,
        'description': 'Minnesota functional with 54% HF exchange'
    },
    
    # Range-separated hybrids
    'CAM-B3LYP': {
        'type': 'range-separated',
        'exchange': 'Coulomb-attenuated B3LYP',
        'correlation': 'LYP',
        'hf_exchange': 'range-dependent',
        'description': 'Long-range corrected B3LYP'
    },
    'ωB97X-D': {
        'type': 'range-separated',
        'exchange': 'ωB97X',
        'correlation': 'with dispersion',
        'hf_exchange': 'range-dependent',
        'description': 'Range-separated with dispersion correction'
    }
}


# =============================================================================
# HARTREE-FOCK FUNCTIONS
# =============================================================================

def hartree_fock_energy(
    n_electrons: int,
    orbital_energies: List[float],
    core_electrons: int = 0
) -> float:
    """
    Calculate Hartree-Fock electronic energy from orbital energies.
    
    E_HF = Σᵢ nᵢ εᵢ - ½ Σᵢⱼ (Jᵢⱼ - Kᵢⱼ)
    
    Simplified: E_HF ~ Σᵢ nᵢ εᵢ (without electron-electron correction)
    
    Args:
        n_electrons: Total number of electrons
        orbital_energies: List of orbital energies (εᵢ) in Hartree
        core_electrons: Number of frozen core electrons
    
    Returns:
        HF electronic energy in Hartree
    
    Example:
        >>> energies = [-11.0, -1.0, -0.5, 0.2, 0.5]
        >>> E = hartree_fock_energy(10, energies)
    """
    if len(orbital_energies) * 2 < n_electrons:
        raise ValueError("Not enough orbitals for electron count")
    
    # Sum occupied orbital energies (doubly occupied)
    # For restricted HF: 2 electrons per orbital
    n_occupied = n_electrons // 2
    total_energy = 2 * sum(orbital_energies[:n_occupied])
    
    # Handle odd electron (singly occupied HOMO)
    if n_electrons % 2 == 1:
        total_energy += orbital_energies[n_occupied]
    
    return total_energy


def slater_determinant_normalization(n_electrons: int) -> float:
    """
    Calculate normalization factor for N-electron Slater determinant.
    
    N = (N!)^{-1/2}
    
    Args:
        n_electrons: Number of electrons
    
    Returns:
        Normalization constant
    
    Example:
        >>> N = slater_determinant_normalization(2)
        >>> print(f"{N:.6f}")
        0.707107
    """
    return 1.0 / math.sqrt(math.factorial(n_electrons))


def fock_matrix_element(
    h_ij: float,
    density: np.ndarray,
    coulomb_integrals: np.ndarray,
    exchange_integrals: np.ndarray,
    i: int,
    j: int
) -> float:
    """
    Calculate element F_ij of Fock matrix.
    
    F_ij = h_ij + Σ_kl P_kl [(ij|kl) - 1/2 (ik|jl)]
    
    Args:
        h_ij: One-electron integral
        density: Density matrix P_kl
        coulomb_integrals: Two-electron Coulomb integrals (ij|kl)
        exchange_integrals: Two-electron exchange integrals (ik|jl)
        i, j: Orbital indices
    
    Returns:
        Fock matrix element F_ij
    
    Example:
        >>> F_ij = fock_matrix_element(h_11, P, J, K, 0, 0)
    """
    n_orbitals = density.shape[0]
    
    # Coulomb and exchange contributions
    J_ij = 0.0
    K_ij = 0.0
    
    for k in range(n_orbitals):
        for l in range(n_orbitals):
            J_ij += density[k, l] * coulomb_integrals[i, j, k, l]
            K_ij += density[k, l] * exchange_integrals[i, k, j, l]
    
    return h_ij + J_ij - 0.5 * K_ij


def koopmans_ionization_potential(orbital_energy: float) -> float:
    """
    Estimate ionization potential from HOMO energy (Koopmans' theorem).
    
    IP ~ -ε_HOMO
    
    Args:
        orbital_energy: HOMO orbital energy in Hartree
    
    Returns:
        Ionization potential in eV
    
    Example:
        >>> IP = koopmans_ionization_potential(-0.5)  # HOMO at -0.5 Hartree
        >>> print(f"IP = {IP:.2f} eV")
    """
    return -orbital_energy * HARTREE_TO_EV


# =============================================================================
# BASIS SET FUNCTIONS
# =============================================================================

def basis_set_info(basis_name: str) -> Dict:
    """
    Return comprehensive information about a basis set.
    
    Args:
        basis_name: Name of basis set (e.g., '6-31G*', 'cc-pVTZ')
    
    Returns:
        Dictionary with basis set properties
    
    Example:
        >>> info = basis_set_info('6-31G*')
        >>> print(info['type'])
        'split-valence'
        >>> print(info['polarization'])
        True
    """
    # Normalize name - handle both uppercase and mixed-case input
    basis_key = basis_name.upper().replace(' ', '')
    
    # Handle alternative notations
    if basis_key == '6-31G(D)':
        basis_key = '6-31G*'
    elif basis_key == '6-31G(D,P)':
        basis_key = '6-31G**'
    
    # Case-insensitive lookup
    for key in BASIS_SET_INFO:
        if key.upper() == basis_key:
            return BASIS_SET_INFO[key]
    
    raise ValueError(f"Unknown basis set: {basis_name}. "
                    f"Available: {list(BASIS_SET_INFO.keys())}")


def sto_ng_exponent(n: int, zeta: float, element: str = 'H') -> List[float]:
    """
    Return Gaussian exponents for STO-nG basis set.
    
    Args:
        n: Number of Gaussians (3, 4, or 6)
        zeta: Slater exponent (effective nuclear charge)
        element: Element symbol (for element-specific exponents)
    
    Returns:
        List of Gaussian exponents alpha
    
    Example:
        >>> alphas = sto_ng_exponent(3, 1.24, 'H')
    """
    # Use database if available
    if element in STO_NG_EXPONENTS and n in STO_NG_EXPONENTS[element]:
        return STO_NG_EXPONENTS[element][n]
    
    # Otherwise, return placeholder based on typical scaling
    # This is a simplified version; real implementations have optimized values
    base_exponents = {
        3: [0.1688, 0.6239, 3.425],
        4: [0.1219, 0.2841, 0.6945, 2.5913],
        6: [0.0563, 0.1274, 0.2360, 0.4332, 0.8383, 2.9303]
    }
    
    if n not in base_exponents:
        raise ValueError(f"STO-{n}G not supported. Use n=3, 4, or 6.")
    
    # Scale by zeta^2 for different elements
    return [alpha * (zeta ** 2) for alpha in base_exponents[n]]


def count_basis_functions(formula: str, basis_name: str) -> int:
    """
    Count total number of basis functions for a molecule.
    
    Args:
        formula: Molecular formula (e.g., 'H2O', 'C6H6')
        basis_name: Basis set name
    
    Returns:
        Total number of basis functions
    
    Example:
        >>> n = count_basis_functions('H2O', '6-31G*')
        >>> print(n)
        19
    """
    from collections import Counter
    
    info = basis_set_info(basis_name)
    
    # Parse molecular formula
    # Simple parser: element symbols followed by optional number
    import re
    elements = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    
    total_functions = 0
    for element, count_str in elements:
        count = int(count_str) if count_str else 1
        
        # Get functions per atom
        if 'functions_per_atom' in info:
            if element in info['functions_per_atom']:
                total_functions += count * info['functions_per_atom'][element]
            else:
                # Estimate based on valence
                total_functions += count * 9  # Default for first-row
        else:
            # Estimate
            total_functions += count * 9
    
    return total_functions


# =============================================================================
# DFT FUNCTIONS
# =============================================================================

def functional_type(functional_name: str) -> Dict:
    """
    Return classification and properties of DFT functional.
    
    Args:
        functional_name: Name of functional (e.g., 'B3LYP', 'PBE')
    
    Returns:
        Dictionary with functional properties
    
    Example:
        >>> info = functional_type('B3LYP')
        >>> print(info['type'])
        'hybrid'
        >>> print(info['hf_exchange'])
        0.2
    """
    # Normalize name
    func_key = functional_name.upper()
    
    if func_key not in DFT_FUNCTIONALS:
        raise ValueError(f"Unknown functional: {functional_name}. "
                        f"Available: {list(DFT_FUNCTIONALS.keys())}")
    
    return DFT_FUNCTIONALS[func_key]


def dft_functional_hierarchy() -> Dict[str, List[str]]:
    """
    Return DFT functionals organized by type.
    
    Returns:
        Dictionary mapping functional type to list of functionals
    
    Example:
        >>> hierarchy = dft_functional_hierarchy()
        >>> print(hierarchy['hybrid'])
        ['B3LYP', 'PBE0', 'B3PW91']
    """
    hierarchy = {}
    for name, props in DFT_FUNCTIONALS.items():
        func_type = props['type']
        if func_type not in hierarchy:
            hierarchy[func_type] = []
        hierarchy[func_type].append(name)
    
    return hierarchy


# =============================================================================
# ELECTRON CORRELATION
# =============================================================================

def electron_correlation_energy(
    method: str,
    hf_energy: float,
    exact_energy: Optional[float] = None,
    correlation_fraction: Optional[float] = None
) -> float:
    """
    Calculate or estimate electron correlation energy.
    
    E_corr = E_exact - E_HF
    
    For post-HF methods, provides typical recovery fractions:
    - MP2: ~80-90% of correlation energy
    - CCSD: ~95-98%
    - CCSD(T): ~99%
    
    Args:
        method: Correlation method ('MP2', 'CCSD', 'CCSD(T)', 'full_CI')
        hf_energy: Hartree-Fock energy in Hartree
        exact_energy: Known exact energy (if available)
        correlation_fraction: Fraction of correlation recovered (for estimates)
    
    Returns:
        Correlation energy in Hartree (negative value)
    
    Example:
        >>> E_corr = electron_correlation_energy('MP2', -76.0, exact_energy=-76.4)
        >>> print(f"Correlation energy: {E_corr:.4f} Hartree")
    """
    if exact_energy is not None:
        # Calculate exact correlation energy
        return exact_energy - hf_energy
    
    # Estimate based on typical recovery fractions
    recovery_fractions = {
        'MP2': 0.85,      # 80-90%
        'MP3': 0.90,
        'MP4': 0.93,
        'CCSD': 0.96,     # 95-98%
        'CCSD(T)': 0.99,  # ~99%
        'CCSDT': 0.995,
        'FULL_CI': 1.00   # Exact
    }
    
    if correlation_fraction is not None:
        frac = correlation_fraction
    elif method.upper() in recovery_fractions:
        frac = recovery_fractions[method.upper()]
    else:
        raise ValueError(f"Unknown method: {method}. "
                        f"Provide correlation_fraction or use: {list(recovery_fractions.keys())}")
    
    # Estimate: correlation energy is typically 1% of total energy
    # For Hartree-Fock, correlation is negative
    estimated_total_correlation = -0.01 * abs(hf_energy)
    
    return estimated_total_correlation * frac


def mp2_energy_contribution(
    occupied_energies: List[float],
    virtual_energies: List[float],
    two_electron_integrals: Optional[np.ndarray] = None
) -> float:
    """
    Calculate MP2 correlation energy correction.
    
    E_MP2 = Σ_{i<j,a<b} |⟨ij||ab⟩|2 / (ε_i + ε_j - ε_a - ε_b)
    
    Args:
        occupied_energies: Orbital energies for occupied orbitals (ε_i)
        virtual_energies: Orbital energies for virtual orbitals (ε_a)
        two_electron_integrals: Two-electron integrals ⟨ij||ab⟩ (optional)
    
    Returns:
        MP2 correlation energy (negative) in Hartree
    
    Note:
        If integrals not provided, returns formula explanation
    
    Example:
        >>> E_MP2 = mp2_energy_contribution([-0.5, -0.3], [0.1, 0.2])
    """
    if two_electron_integrals is None:
        # Return formula description
        return -999.999  # Placeholder indicating need for integrals
    
    E_MP2 = 0.0
    n_occ = len(occupied_energies)
    n_virt = len(virtual_energies)
    
    for i in range(n_occ):
        for j in range(i+1, n_occ):
            for a in range(n_virt):
                for b in range(a+1, n_virt):
                    denominator = (occupied_energies[i] + occupied_energies[j] -
                                 virtual_energies[a] - virtual_energies[b])
                    
                    # Antisymmetrized integral
                    integral = two_electron_integrals[i, j, a, b]
                    
                    E_MP2 += (integral ** 2) / denominator
    
    return E_MP2


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def parse_basis_notation(notation: str) -> Dict:
    """
    Parse Pople-style basis set notation.
    
    Args:
        notation: Basis set name like '6-311+G**'
    
    Returns:
        Dictionary with parsed components
    
    Example:
        >>> parsed = parse_basis_notation('6-311+G**')
        >>> print(parsed)
        {
            'core_primitives': 6,
            'valence_split': [3, 1, 1],
            'polarization': True,
            'polarization_on_H': True,
            'diffuse': True,
            'diffuse_on_H': True
        }
    """
    import re
    
    # Try minimal basis pattern first
    minimal_pattern = r'^STO-(\d+)G$'
    minimal_match = re.match(minimal_pattern, notation.upper())
    if minimal_match:
        return {
            'type': 'minimal',
            'n_primitives': int(minimal_match.group(1)),
            'polarization': False,
            'diffuse': False
        }
    
    # Pattern for split-valence: N-MPG or N-MMPG (triple-zeta)
    # Examples: 6-31G, 6-311G, 6-31G*, 6-311+G**
    pattern = r'^(\d+)-(\d)(\d*)([+]*)G([*]*)$'
    match = re.match(pattern, notation.upper())
    
    if not match:
        raise ValueError(f"Cannot parse basis notation: {notation}")
    
    core = int(match.group(1))
    val1 = int(match.group(2))
    val2 = match.group(3)  # May be empty or '1', '11', etc.
    diffuse = match.group(4)
    polarization = match.group(5)
    
    # Build valence split
    # For 6-31G: val1=3, val2='1' -> [3, 1]
    # For 6-311G: val1=3, val2='11' -> [3, 1, 1] (two additional '1's)
    # For 6-3111G: val1=3, val2='111' -> [3, 1, 1, 1] (three additional '1's)
    valence_split = [val1]
    for char in val2:
        if char == '1':
            valence_split.append(1)
    
    return {
        'core_primitives': core,
        'valence_split': valence_split,
        'polarization': len(polarization) > 0,
        'polarization_on_H': len(polarization) > 1,
        'diffuse': len(diffuse) > 0,
        'diffuse_on_H': len(diffuse) > 1
    }


def recommend_basis_set(
    system_type: str,
    property_of_interest: str,
    accuracy: str = 'medium'
) -> List[str]:
    """
    Recommend appropriate basis sets for a calculation.
    
    Args:
        system_type: 'neutral', 'anion', 'cation', 'transition_metal', 'large'
        property_of_interest: 'energy', 'geometry', 'frequency', 'dipole', 'bond_energy'
        accuracy: 'low', 'medium', 'high'
    
    Returns:
        List of recommended basis sets (ordered by cost)
    
    Example:
        >>> bases = recommend_basis_set('neutral', 'geometry', 'medium')
        >>> print(bases)
        ['6-31G*', '6-311G**', 'aug-cc-pVTZ']
    """
    recommendations = {
        ('neutral', 'energy', 'low'): ['STO-3G', '3-21G'],
        ('neutral', 'energy', 'medium'): ['6-31G', '6-31G*'],
        ('neutral', 'energy', 'high'): ['6-311G**', 'cc-pVTZ'],
        ('neutral', 'geometry', 'medium'): ['6-31G*', '6-311G**'],
        ('neutral', 'geometry', 'high'): ['aug-cc-pVTZ'],
        ('anion', 'energy', 'medium'): ['6-31+G*', '6-31++G**'],
        ('anion', 'energy', 'high'): ['aug-cc-pVTZ'],
        ('cation', 'energy', 'medium'): ['6-31G*', '6-311G*'],
        ('transition_metal', 'energy', 'medium'): ['6-31G*', 'LANL2DZ'],
        ('large', 'energy', 'low'): ['STO-3G', '3-21G'],
        ('large', 'geometry', 'medium'): ['6-31G'],
    }
    
    key = (system_type, property_of_interest, accuracy)
    
    if key in recommendations:
        return recommendations[key]
    else:
        # Default recommendations
        return ['6-31G*', '6-311G**', 'aug-cc-pVTZ']


# =============================================================================
# TEST FUNCTIONS (for validation)
# =============================================================================

def test_hartree_fock_energy():
    """Test Hartree-Fock energy calculation."""
    # He atom: 2 electrons, one orbital
    energies = [-0.918]  # 1s orbital energy in Hartree
    E_HF = hartree_fock_energy(2, energies)
    assert abs(E_HF - 2 * (-0.918)) < 0.001
    print("✓ test_hartree_fock_energy passed")


def test_slater_normalization():
    """Test Slater determinant normalization."""
    N2 = slater_determinant_normalization(2)
    assert abs(N2 - 1/math.sqrt(2)) < 0.001
    
    N10 = slater_determinant_normalization(10)
    assert abs(N10 - 1/math.sqrt(math.factorial(10))) < 1e-10
    print("✓ test_slater_normalization passed")


def test_basis_set_info():
    """Test basis set info retrieval."""
    info = basis_set_info('6-31G*')
    assert info['type'] == 'split-valence'
    assert info['polarization'] == True
    assert info['diffuse'] == False
    print("✓ test_basis_set_info passed")


def test_functional_type():
    """Test DFT functional classification."""
    info = functional_type('B3LYP')
    assert info['type'] == 'hybrid'
    assert info['hf_exchange'] == 0.20
    
    info2 = functional_type('PBE')
    assert info2['type'] == 'GGA'
    assert info2['hf_exchange'] == 0.0
    print("✓ test_functional_type passed")


def test_parse_basis_notation():
    """Test basis set notation parsing."""
    parsed = parse_basis_notation('6-31G**')
    assert parsed['core_primitives'] == 6
    assert parsed['valence_split'] == [3, 1]
    assert parsed['polarization'] == True
    assert parsed['polarization_on_H'] == True
    
    parsed2 = parse_basis_notation('STO-3G')
    assert parsed2['type'] == 'minimal'
    assert parsed2['n_primitives'] == 3
    print("✓ test_parse_basis_notation passed")


if __name__ == '__main__':
    print("Running computational QC tools tests...\n")
    test_hartree_fock_energy()
    test_slater_normalization()
    test_basis_set_info()
    test_functional_type()
    test_parse_basis_notation()
    print("\nAll tests passed! ✓")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'basis_set_info', 'description': "Return comprehensive information about a basis set.\n\nArgs:\n    basis_name: Name of basis set (e.g., '6-31G*', 'cc-pVTZ')\n\nReturns:\n    Dictionary with basis set properties\n\nExample:\n    >>> info = basis_set_info('6-31G*')\n    >>> print(info['type'])\n    'split-valence'\n    >>> print(info['polarization'])\n    true", 'inputSchema': {'type': 'object', 'properties': {'basis_name': {'type': 'string', 'description': 'Basis Name'}}, 'required': ['basis_name']}},
    {'name': 'count_basis_functions', 'description': "Count total number of basis functions for a molecule.\n\nArgs:\n    formula: Molecular formula (e.g., 'H2O', 'C6H6')\n    basis_name: Basis set name\n\nReturns:\n    Total number of basis functions\n\nExample:\n    >>> n = count_basis_functions('H2O', '6-31G*')\n    >>> print(n)\n    19", 'inputSchema': {'type': 'object', 'properties': {'formula': {'type': 'string', 'description': 'Formula'}, 'basis_name': {'type': 'string', 'description': 'Basis Name'}}, 'required': ['formula', 'basis_name']}},
    {'name': 'dft_functional_hierarchy', 'description': "Return DFT functionals organized by type.\n\nReturns:\n    Dictionary mapping functional type to list of functionals\n\nExample:\n    >>> hierarchy = dft_functional_hierarchy()\n    >>> print(hierarchy['hybrid'])\n    ['B3LYP', 'PBE0', 'B3PW91']", 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'electron_correlation_energy', 'description': 'Calculate or estimate electron correlation energy.\n\nE_corr = E_exact - E_HF\n\nFor post-HF methods, provides typical recovery fractions:\n- MP2: ~80-90% of correlation energy\n- CCSD: ~95-98%\n- CCSD(T): ~99%\n\nArgs:\n    method: Correlation method (\'MP2\', \'CCSD\', \'CCSD(T)\', \'full_CI\')\n    hf_energy: Hartree-Fock energy in Hartree\n    exact_energy: Known exact energy (if available)\n    correlation_fraction: Fraction of correlation recovered (for estimates)\n\nReturns:\n    Correlation energy in Hartree (negative value)\n\nExample:\n    >>> E_corr = electron_correlation_energy(\'MP2\', -76.0, exact_energy=-76.4)\n    >>> print(f"Correlation energy: {E_corr:.4f} Hartree")', 'inputSchema': {'type': 'object', 'properties': {'method': {'type': 'string', 'description': 'Method'}, 'hf_energy': {'type': 'number', 'description': 'Hf Energy'}, 'exact_energy': {'type': 'number', 'description': 'Exact Energy', 'default': None}, 'correlation_fraction': {'type': 'string', 'description': 'Correlation Fraction', 'default': None}}, 'required': ['method', 'hf_energy']}},
    {'name': 'fock_matrix_element', 'description': 'Calculate element F_ij of Fock matrix.\n\nF_ij = h_ij + Σ_kl P_kl [(ij|kl) - 1/2 (ik|jl)]\n\nArgs:\n    h_ij: One-electron integral\n    density: Density matrix P_kl\n    coulomb_integrals: Two-electron Coulomb integrals (ij|kl)\n    exchange_integrals: Two-electron exchange integrals (ik|jl)\n    i, j: Orbital indices\n\nReturns:\n    Fock matrix element F_ij\n\nExample:\n    >>> F_ij = fock_matrix_element(h_11, P, J, K, 0, 0)', 'inputSchema': {'type': 'object', 'properties': {'h_ij': {'type': 'number', 'description': 'H Ij'}, 'density': {'type': 'number', 'description': 'Density'}, 'coulomb_integrals': {'type': 'number', 'description': 'Coulomb Integrals'}, 'exchange_integrals': {'type': 'string', 'description': 'Exchange Integrals'}, 'i': {'type': 'number', 'description': 'I'}, 'j': {'type': 'number', 'description': 'J'}}, 'required': ['h_ij', 'density', 'coulomb_integrals', 'exchange_integrals', 'i', 'j']}},
    {'name': 'functional_type', 'description': "Return classification and properties of DFT functional.\n\nArgs:\n    functional_name: Name of functional (e.g., 'B3LYP', 'PBE')\n\nReturns:\n    Dictionary with functional properties\n\nExample:\n    >>> info = functional_type('B3LYP')\n    >>> print(info['type'])\n    'hybrid'\n    >>> print(info['hf_exchange'])\n    0.2", 'inputSchema': {'type': 'object', 'properties': {'functional_name': {'type': 'string', 'description': 'Functional Name'}}, 'required': ['functional_name']}},
    {'name': 'hartree_fock_energy', 'description': 'Calculate Hartree-Fock electronic energy from orbital energies.\n\nE_HF = Σᵢ nᵢ εᵢ - ½ Σᵢⱼ (Jᵢⱼ - Kᵢⱼ)\n\nSimplified: E_HF ~ Σᵢ nᵢ εᵢ (without electron-electron correction)\n\nArgs:\n    n_electrons: Total number of electrons\n    orbital_energies: List of orbital energies (εᵢ) in Hartree\n    core_electrons: Number of frozen core electrons\n\nReturns:\n    HF electronic energy in Hartree\n\nExample:\n    >>> energies = [-11.0, -1.0, -0.5, 0.2, 0.5]\n    >>> E = hartree_fock_energy(10, energies)', 'inputSchema': {'type': 'object', 'properties': {'n_electrons': {'type': 'number', 'description': 'N Electrons'}, 'orbital_energies': {'type': 'string', 'description': 'Orbital Energies'}, 'core_electrons': {'type': 'number', 'description': 'Core Electrons', 'default': 0}}, 'required': ['n_electrons', 'orbital_energies']}},
    {'name': 'koopmans_ionization_potential', 'description': 'Estimate ionization potential from HOMO energy (Koopmans\' theorem).\n\nIP ~ -ε_HOMO\n\nArgs:\n    orbital_energy: HOMO orbital energy in Hartree\n\nReturns:\n    Ionization potential in eV\n\nExample:\n    >>> IP = koopmans_ionization_potential(-0.5)  # HOMO at -0.5 Hartree\n    >>> print(f"IP = {IP:.2f} eV")', 'inputSchema': {'type': 'object', 'properties': {'orbital_energy': {'type': 'string', 'description': 'Orbital Energy'}}, 'required': ['orbital_energy']}},
    {'name': 'mp2_energy_contribution', 'description': 'Calculate MP2 correlation energy correction.\n\nE_MP2 = Σ_{i<j,a<b} |⟨ij||ab⟩|2 / (ε_i + ε_j - ε_a - ε_b)\n\nArgs:\n    occupied_energies: Orbital energies for occupied orbitals (ε_i)\n    virtual_energies: Orbital energies for virtual orbitals (ε_a)\n    two_electron_integrals: Two-electron integrals ⟨ij||ab⟩ (optional)\n\nReturns:\n    MP2 correlation energy (negative) in Hartree\n\nNote:\n    If integrals not provided, returns formula explanation\n\nExample:\n    >>> E_MP2 = mp2_energy_contribution([-0.5, -0.3], [0.1, 0.2])', 'inputSchema': {'type': 'object', 'properties': {'occupied_energies': {'type': 'number', 'description': 'Occupied Energies'}, 'virtual_energies': {'type': 'number', 'description': 'Virtual Energies'}, 'two_electron_integrals': {'type': 'number', 'description': 'Two Electron Integrals', 'default': None}}, 'required': ['occupied_energies', 'virtual_energies']}},
    {'name': 'parse_basis_notation', 'description': "Parse Pople-style basis set notation.\n\nArgs:\n    notation: Basis set name like '6-311+G**'\n\nReturns:\n    Dictionary with parsed components\n\nExample:\n    >>> parsed = parse_basis_notation('6-311+G**')\n    >>> print(parsed)\n    {\n        'core_primitives': 6,\n        'valence_split': [3, 1, 1],\n        'polarization': True,\n        'polarization_on_H': True,\n        'diffuse': True,\n        'diffuse_on_H': True\n    }", 'inputSchema': {'type': 'object', 'properties': {'notation': {'type': 'string', 'description': 'Notation'}}, 'required': ['notation']}},
    {'name': 'recommend_basis_set', 'description': "Recommend appropriate basis sets for a calculation.\n\nArgs:\n    system_type: 'neutral', 'anion', 'cation', 'transition_metal', 'large'\n    property_of_interest: 'energy', 'geometry', 'frequency', 'dipole', 'bond_energy'\n    accuracy: 'low', 'medium', 'high'\n\nReturns:\n    List of recommended basis sets (ordered by cost)\n\nExample:\n    >>> bases = recommend_basis_set('neutral', 'geometry', 'medium')\n    >>> print(bases)\n    ['6-31G*', '6-311G**', 'aug-cc-pVTZ']", 'inputSchema': {'type': 'object', 'properties': {'system_type': {'type': 'string', 'description': 'System Type'}, 'property_of_interest': {'type': 'number', 'description': 'Property Of Interest'}, 'accuracy': {'type': 'number', 'description': 'Accuracy', 'default': 'medium'}}, 'required': ['system_type', 'property_of_interest']}},
    {'name': 'slater_determinant_normalization', 'description': 'Calculate normalization factor for N-electron Slater determinant.\n\nN = (N!)^{-1/2}\n\nArgs:\n    n_electrons: Number of electrons\n\nReturns:\n    Normalization constant\n\nExample:\n    >>> N = slater_determinant_normalization(2)\n    >>> print(f"{N:.6f}")\n    0.707107', 'inputSchema': {'type': 'object', 'properties': {'n_electrons': {'type': 'number', 'description': 'N Electrons'}}, 'required': ['n_electrons']}},
    {'name': 'sto_ng_exponent', 'description': "Return Gaussian exponents for STO-nG basis set.\n\nArgs:\n    n: Number of Gaussians (3, 4, or 6)\n    zeta: Slater exponent (effective nuclear charge)\n    element: Element symbol (for element-specific exponents)\n\nReturns:\n    List of Gaussian exponents alpha\n\nExample:\n    >>> alphas = sto_ng_exponent(3, 1.24, 'H')", 'inputSchema': {'type': 'object', 'properties': {'n': {'type': 'number', 'description': 'N'}, 'zeta': {'type': 'number', 'description': 'Zeta'}, 'element': {'type': 'string', 'description': 'Element', 'default': 'H'}}, 'required': ['n', 'zeta']}},
    {'name': 'test_basis_set_info', 'description': 'Test basis set info retrieval.', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_functional_type', 'description': 'Test DFT functional classification.', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_hartree_fock_energy', 'description': 'Test Hartree-Fock energy calculation.', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_parse_basis_notation', 'description': 'Test basis set notation parsing.', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_slater_normalization', 'description': 'Test Slater determinant normalization.', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}}
]
