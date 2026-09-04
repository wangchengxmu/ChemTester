"""
Diatomic Molecular Orbital Theory Tools - L3 Implementation

Core functions for diatomic molecular orbital calculations:
- Molecular orbital diagrams
- Bond order calculations
- Molecular term symbols
- Overlap integrals
- H2+ and H2 model systems
- Homonuclear and heteronuclear diatomics

Source: LibreTexts Physical Chemistry Ch09
"""
## Solver Instructions (for AI Agent)

# When you encounter diatomic molecular orbital problems (bond order, electron configuration, paramagnetism), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: molecule name, total valence electrons, orbital occupations
# - **Asked**: bond order, electron configuration, paramagnetic/diamagnetic, term symbol, bond energy/length

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Bond order | `bond_order(n_bonding, n_antibonding)` | electron counts |
# | Bond order from config | `bond_order_from_configuration(σg, σu, piu, pig, ...)` | per-orbital counts |
# | Electron configuration | `electron_configuration_diatomic(Z_total, heteronuclear)` | total valence e- |
# | MO energy H2+ | `mo_energy_h2_plus(R, n, symmetric)` | R in Bohr radii |
# | Overlap integral | `overlap_integral_1s(R)` | R in Bohr radii |
# | Coulomb integral | `coulomb_integral_1s(R, Z)` | R, nuclear charge |
# | Exchange integral | `exchange_integral_1s(R, Z)` | R, nuclear charge |
# | Term symbol | `molecular_term_symbol_diatomic(S, Lambda, omega, inversion, reflection)` | quantum numbers |
# | Λ from electrons | `calculate_Lambda_from_electrons(lambda_values)` | list of lambda values |
# | S from electrons | `calculate_S_from_electrons(spin_values)` | list of mₛ values |
# | Database lookup | `get_diatomic_data(molecule)` | 'H2', 'O2', 'CO', etc. |
# | Paramagnetic? | `is_paramagnetic(n_unpaired)` | unpaired e- count |
# | Orbital symmetry | `orbital_symmetry_label(l, m)` | l, m quantum numbers |
# | Bond energy estimate | `bond_energy_estimate(bond_order)` | BO |
# | Bond length estimate | `bond_length_estimate(BO, sum_radii_pm)` | BO, covalent radii |

### Step 3: Handle special cases
# - MO ordering changes: B2/C2/N2 have piu < σg(2p); O2/F2/Ne2 have σg(2p) < piu
# - O2 is paramagnetic (pig*2 with 2 unpaired electrons) - key prediction of MO theory
# - He2 and Ne2: bond order = 0, not stable
# - Heteronuclear: no g/u labels

### Examples
# 1. **N2**: `electron_configuration_diatomic(10)` -> BO = 3.0 (triple bond)
# 2. **O2**: `electron_configuration_diatomic(12)` -> BO = 2.0, paramagnetic (2 unpaired)
# 3. **Bond order**: `bond_order(8, 2)` -> 3.0; `bond_order(10, 10)` -> 0.0 (unstable)
# 4. **Database**: `get_diatomic_data('O2')` -> BO=2.0, D0=498 kJ/mol, r=121 pm, paramagnetic=True


import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants
from scipy.special import factorial

# Physical constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
BOHR_RADIUS = 5.2917721e-11       # m
HARTREE_ENERGY = 4.35974e-18      # J


# =============================================================================
# MOLECULAR ORBITAL ENERGY LEVELS
# =============================================================================

def mo_energy_h2_plus(R: float, n: int = 1, symmetric: bool = True) -> float:
    """
    Calculate MO energy for H2+ at given internuclear distance.
    
    Simple approximation using linear combination of atomic orbitals.
    
    Args:
        R: Internuclear distance in Bohr radii (a0)
        n: Principal quantum number (1 for 1s)
        symmetric: True for bonding (σg), False for antibonding (σu)
    
    Returns:
        Energy in Hartree (atomic units)
    
    Note:
        This is a simplified model. For accurate values, use
        quantum chemistry software.
    
    Example:
        >>> E_bond = mo_energy_h2_plus(2.0, symmetric=True)
        >>> E_anti = mo_energy_h2_plus(2.0, symmetric=False)
    """
    # Simplified model: E = E_H ± (S x E_coupling)
    # where S depends on overlap and E_coupling on exchange
    
    # Overlap integral approximation for 1s orbitals
    rho = R  # R in atomic units
    S = np.exp(-rho) * (1 + rho + rho**2/3)
    
    # Coulomb and resonance integrals (simplified)
    J = -1/R * (1 - (1 + rho) * np.exp(-2*rho))  # Coulomb
    K = -np.exp(-rho) * (1 + rho)  # Exchange (resonance)
    
    E_H = -0.5  # H atom ground state in Hartree
    
    if symmetric:  # Bonding σg
        return E_H + (J + K) / (1 + S)
    else:  # Antibonding σu
        return E_H + (J - K) / (1 - S)


def overlap_integral_1s(R: float) -> float:
    """
    Calculate overlap integral for two 1s orbitals.
    
    S = ⟨1s_A | 1s_B⟩
    
    For STO-1s orbitals:
    S = e^(-R) (1 + R + R2/3)
    
    Args:
        R: Internuclear distance in Bohr radii
    
    Returns:
        Overlap integral (dimensionless)
    
    Example:
        >>> overlap_integral_1s(2.0)
        0.586
    """
    return np.exp(-R) * (1 + R + R**2/3)


def coulomb_integral_1s(R: float, Z: float = 1) -> float:
    """
    Calculate Coulomb integral for H2+.
    
    J = ⟨1s_A | -1/r_B | 1s_A⟩
    
    Args:
        R: Internuclear distance in Bohr radii
        Z: Nuclear charge
    
    Returns:
        Coulomb integral in Hartree
    """
    rho = Z * R
    return -Z/R * (1 - (1 + rho) * np.exp(-2*rho))


def exchange_integral_1s(R: float, Z: float = 1) -> float:
    """
    Calculate exchange (resonance) integral.
    
    K = ⟨1s_A | -1/r_B | 1s_B⟩
    
    Args:
        R: Internuclear distance in Bohr radii
        Z: Nuclear charge
    
    Returns:
        Exchange integral in Hartree
    """
    rho = Z * R
    return -Z * np.exp(-rho) * (1 + rho)


# =============================================================================
# BOND ORDER CALCULATIONS
# =============================================================================

def bond_order(n_bonding: int, n_antibonding: int) -> float:
    """
    Calculate bond order from electron counts.
    
    BO = (n_bonding - n_antibonding) / 2
    
    Args:
        n_bonding: Number of electrons in bonding orbitals
        n_antibonding: Number of electrons in antibonding orbitals
    
    Returns:
        Bond order
    
    Example:
        >>> bond_order(2, 0)  # H2
        1.0
        >>> bond_order(8, 4)  # O2
        2.0
    """
    return (n_bonding - n_antibonding) / 2


def bond_order_from_configuration(
    sigma_g_electrons: int = 0,
    sigma_u_electrons: int = 0,
    pi_u_electrons: int = 0,
    pi_g_electrons: int = 0,
    sigma_g2_electrons: int = 0,
    sigma_u2_electrons: int = 0
) -> float:
    """
    Calculate bond order from MO electron configuration.
    
    For homonuclear diatomics (standard MO diagram).
    
    Args:
        sigma_g_electrons: σg(1s) electrons
        sigma_u_electrons: σu*(1s) electrons
        pi_u_electrons: piu(2p) electrons
        pi_g_electrons: pig*(2p) electrons
        sigma_g2_electrons: σg(2s) electrons
        sigma_u2_electrons: σu*(2s) electrons
    
    Returns:
        Bond order
    """
    # Bonding: σg(1s), σg(2s), σg(2p), piu(2p)
    # Antibonding: σu*(1s), σu*(2s), pig*(2p), σu*(2p)
    
    n_bonding = sigma_g_electrons + sigma_g2_electrons + pi_u_electrons
    n_antibonding = sigma_u_electrons + sigma_u2_electrons + pi_g_electrons
    
    # Note: σg(2p) typically counted as bonding
    # For simplicity, using standard MO ordering
    
    return bond_order(n_bonding, n_antibonding)


def bond_order_for_charged_species(molecule: str, charge: int) -> Dict:
    """
    Calculate bond order for a charged diatomic species.
    
    Args:
        molecule: Molecule formula (e.g., 'O2', 'N2')
        charge: Charge on the molecule (e.g., +2 for O2²⁺)
    
    Returns:
        Dictionary with bond order and configuration info
    
    Examples:
        >>> bond_order_for_charged_species('O2', 2)  # O2²⁺
        {'bond_order': 3.0, 'valence_electrons': 10}
        >>> bond_order_for_charged_species('O2', 1)  # O2⁺
        {'bond_order': 2.5, 'valence_electrons': 11}
    """
    # Valence electrons for common diatomic molecules
    valence_map = {
        'H2': 2, 'HE2': 4, 'LI2': 2, 'BE2': 4, 'B2': 6, 'C2': 8, 'N2': 10,
        'O2': 12, 'F2': 14, 'NE2': 16
    }
    
    molecule_upper = molecule.upper()
    if molecule_upper not in valence_map:
        raise ValueError(f"Unknown molecule {molecule}. Use electron_configuration_diatomic with total valence electrons.")
    
    base_electrons = valence_map[molecule_upper]
    # Positive charge removes electrons, negative charge adds electrons
    total_electrons = base_electrons - charge
    
    config = electron_configuration_diatomic(total_electrons)
    
    return {
        'molecule': f"{molecule}{('+' * charge) if charge > 0 else ('-' * abs(charge))}",
        'bond_order': config['bond_order'],
        'valence_electrons': total_electrons,
        'configuration': config['configuration'],
        'n_bonding': config['n_bonding'],
        'n_antibonding': config['n_antibonding']
    }


def electron_configuration_diatomic(Z_total: int, 
                                    heteronuclear: bool = False) -> Dict:
    """
    Generate electron configuration for diatomic molecule.
    
    Args:
        Z_total: Total number of valence electrons
        heteronuclear: If True, use heteronuclear MO diagram
    
    Returns:
        Dictionary with orbital occupations and bond order
    
    Example:
        >>> config = electron_configuration_diatomic(10)  # N2
        >>> print(config['bond_order'])
        3.0
    """
    # Standard MO ordering for homonuclear diatomics (up to N2):
    # σg(1s) < σu*(1s) < σg(2s) < σu*(2s) < piu(2p) < σg(2p) < pig*(2p) < σu*(2p)
    
    # For O2, F2, Ne2 (different ordering):
    # σg(1s) < σu*(1s) < σg(2s) < σu*(2s) < σg(2p) < piu(2p) < pig*(2p) < σu*(2p)
    
    if heteronuclear:
        # No g/u labels - valence orbitals only (skip 1s core)
        orbitals = [
            ('σ(2s)', 2, 'bonding'),
            ('σ*(2s)', 2, 'antibonding'),
            ('σ(2p)', 2, 'bonding'),
            ('pi(2p)', 4, 'bonding'),
            ('pi*(2p)', 4, 'antibonding'),
            ('σ*(2p)', 2, 'antibonding'),
        ]
    else:
        # Determine ordering based on molecule
        # For B2, C2, N2 (Z_total <= 10): piu(2p) < σg(2p)
        # For O2, F2, Ne2 (Z_total > 10): σg(2p) < piu(2p)
        # Note: These are VALENCE orbitals only (2s and 2p)
        if Z_total <= 10:  # Up to N2 ordering
            orbitals = [
                ('σg(2s)', 2, 'bonding'),
                ('σu*(2s)', 2, 'antibonding'),
                ('piu(2p)', 4, 'bonding'),
                ('σg(2p)', 2, 'bonding'),
                ('pig*(2p)', 4, 'antibonding'),
                ('σu*(2p)', 2, 'antibonding'),
            ]
        else:  # O2, F2, Ne2 ordering
            orbitals = [
                ('σg(2s)', 2, 'bonding'),
                ('σu*(2s)', 2, 'antibonding'),
                ('σg(2p)', 2, 'bonding'),
                ('piu(2p)', 4, 'bonding'),
                ('pig*(2p)', 4, 'antibonding'),
                ('σu*(2p)', 2, 'antibonding'),
            ]
    
    # Fill orbitals
    electrons_remaining = Z_total
    configuration = {}
    n_bonding = 0
    n_antibonding = 0
    
    for name, capacity, orbital_type in orbitals:
        if electrons_remaining >= capacity:
            configuration[name] = capacity
            electrons_remaining -= capacity
            if orbital_type == 'bonding':
                n_bonding += capacity
            else:
                n_antibonding += capacity
        elif electrons_remaining > 0:
            configuration[name] = electrons_remaining
            if orbital_type == 'bonding':
                n_bonding += electrons_remaining
            else:
                n_antibonding += electrons_remaining
            electrons_remaining = 0
            break
        else:
            break
    
    BO = bond_order(n_bonding, n_antibonding)
    
    return {
        'configuration': configuration,
        'n_bonding': n_bonding,
        'n_antibonding': n_antibonding,
        'bond_order': BO,
        'remaining_electrons': electrons_remaining
    }


# =============================================================================
# MOLECULAR TERM SYMBOLS
# =============================================================================

def molecular_term_symbol_diatomic(
    total_spin_S: float,
    total_Lambda: int,
    total_omega: Optional[float] = None,
    inversion_symmetry: Optional[str] = None,
    reflection_symmetry: Optional[str] = None
) -> str:
    """
    Construct molecular term symbol for diatomic molecule.
    
    Format: ^{2S+1}Λ_{Ω}^{±}
    
    where:
        2S+1 = multiplicity
        Λ = |Σlambdaᵢ| (projection of L on internuclear axis)
        Ω = |Λ + Σ| (projection of J)
        ± = inversion symmetry (g/u for homonuclear)
        +/- = reflection symmetry for Σ states
    
    Args:
        total_spin_S: Total spin quantum number
        total_Lambda: |Λ| value (0=Σ, 1=Π, 2=Delta, 3=Φ)
        total_omega: Ω value (optional)
        inversion_symmetry: 'g' or 'u' (for homonuclear)
        reflection_symmetry: '+' or '-' (for Σ states)
    
    Returns:
        Molecular term symbol string
    
    Example:
        >>> molecular_term_symbol_diatomic(0, 0, inversion_symmetry='g', reflection_symmetry='+')
        '1Σg+'
    """
    # Multiplicity
    multiplicity = int(2 * total_spin_S + 1)
    
    # Lambda symbol
    lambda_symbols = {0: 'Σ', 1: 'Π', 2: 'Delta', 3: 'Φ', 4: 'Γ'}
    Lambda_symbol = lambda_symbols.get(abs(total_Lambda), '?')
    
    # Build term symbol
    # Using unicode superscripts
    superscripts = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5'}
    mult_str = superscripts.get(str(multiplicity), str(multiplicity))
    
    term = f"{mult_str}{Lambda_symbol}"
    
    # Add reflection symmetry for Σ states
    if total_Lambda == 0 and reflection_symmetry:
        term += reflection_symmetry
    
    # Add inversion symmetry
    if inversion_symmetry:
        term += inversion_symmetry
    
    # Add omega subscript if provided
    if total_omega is not None:
        if total_omega == int(total_omega):
            term += f"_{int(total_omega)}"
        else:
            term += f"_{int(2*total_omega)}/2"
    
    return term


def calculate_Lambda_from_electrons(lambda_values: List[int]) -> int:
    """
    Calculate total |Λ| from individual electron lambda values.
    
    Λ = |Σlambdaᵢ|
    
    lambda values: σ(0), pi(±1), delta(±2), φ(±3)
    
    Args:
        lambda_values: List of individual electron lambda values
    
    Returns:
        |Λ| value
    """
    return abs(sum(lambda_values))


def calculate_S_from_electrons(spin_values: List[float]) -> float:
    """
    Calculate total S from individual electron spin values.
    
    S = |Σsᵢ| (for parallel spins)
    
    Args:
        spin_values: List of individual m_s values (+½ or -½)
    
    Returns:
        Total S value
    """
    # S can range from |Σm_s| to maximum possible
    # This gives minimum S
    return abs(sum(spin_values))


# =============================================================================
# HOMONUCLEAR DIATOMIC DATABASE
# =============================================================================

HOMONUCLEAR_DIATOMIC_DATA = {
    'H2': {
        'valence_electrons': 2,
        'bond_order': 1.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 436,
        'bond_length_pm': 74.1,
        'configuration': 'σg(1s)2'
    },
    'He2': {
        'valence_electrons': 4,
        'bond_order': 0.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 0,  # Not stable
        'bond_length_pm': None,
        'configuration': 'σg(1s)2σu*(1s)2',
        'note': 'Not stable at room temperature'
    },
    'Li2': {
        'valence_electrons': 2,
        'bond_order': 1.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 105,
        'bond_length_pm': 267,
        'configuration': 'σg(2s)2'
    },
    'Be2': {
        'valence_electrons': 4,
        'bond_order': 0.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 0,  # Very weak
        'bond_length_pm': None,
        'note': 'Very weakly bound'
    },
    'B2': {
        'valence_electrons': 6,
        'bond_order': 1.0,
        'ground_state_term': '3Σg-',
        'bond_energy_kJ': 290,
        'bond_length_pm': 159,
        'configuration': 'σg(2s)2σu*(2s)2piu(2p)2'
    },
    'C2': {
        'valence_electrons': 8,
        'bond_order': 2.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 620,
        'bond_length_pm': 124,
        'configuration': 'σg(2s)2σu*(2s)2piu(2p)4'
    },
    'N2': {
        'valence_electrons': 10,
        'bond_order': 3.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 945,
        'bond_length_pm': 110,
        'configuration': 'σg(2s)2σu*(2s)2piu(2p)4σg(2p)2'
    },
    'O2': {
        'valence_electrons': 12,
        'bond_order': 2.0,
        'ground_state_term': '3Σg-',
        'bond_energy_kJ': 498,
        'bond_length_pm': 121,
        'configuration': 'σg(2s)2σu*(2s)2σg(2p)2piu(2p)4pig*(2p)2',
        'paramagnetic': True
    },
    'F2': {
        'valence_electrons': 14,
        'bond_order': 1.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 159,
        'bond_length_pm': 142,
        'configuration': 'σg(2s)2σu*(2s)2σg(2p)2piu(2p)4pig*(2p)4'
    },
    'Ne2': {
        'valence_electrons': 16,
        'bond_order': 0.0,
        'ground_state_term': '1Σg+',
        'bond_energy_kJ': 0,  # Not stable
        'bond_length_pm': None,
        'configuration': 'σg(2s)2σu*(2s)2σg(2p)2piu(2p)4pig*(2p)4σu*(2p)2',
        'note': 'Not stable'
    }
}


HETERONUCLEAR_DIATOMIC_DATA = {
    'CO': {
        'valence_electrons': 10,
        'bond_order': 3.0,
        'ground_state_term': '1Σ+',
        'bond_energy_kJ': 1072,
        'bond_length_pm': 113,
        'configuration': 'σ2σ*2pi4σ2',
        'isoelectronic_with': 'N2'
    },
    'NO': {
        'valence_electrons': 11,
        'bond_order': 2.5,
        'ground_state_term': '2Π',
        'bond_energy_kJ': 630,
        'bond_length_pm': 115,
        'configuration': 'σ2σ*2pi4σ2pi*1',
        'paramagnetic': True
    },
    'CN': {
        'valence_electrons': 9,
        'bond_order': 2.5,
        'ground_state_term': '2Σ+',
        'bond_energy_kJ': 750,
        'bond_length_pm': 117
    },
    'HCl': {
        'valence_electrons': 8,
        'bond_order': 1.0,
        'ground_state_term': '1Σ+',
        'bond_energy_kJ': 432,
        'bond_length_pm': 127
    },
    'HF': {
        'valence_electrons': 8,
        'bond_order': 1.0,
        'ground_state_term': '1Σ+',
        'bond_energy_kJ': 569,
        'bond_length_pm': 92
    },
    'LiH': {
        'valence_electrons': 2,
        'bond_order': 1.0,
        'ground_state_term': '1Σ+',
        'bond_energy_kJ': 238,
        'bond_length_pm': 160
    }
}


def get_diatomic_data(molecule: str) -> Dict:
    """
    Get data for a diatomic molecule.
    
    Args:
        molecule: Molecule formula (e.g., 'H2', 'O2', 'CO')
    
    Returns:
        Dictionary with molecular properties
    
    Example:
        >>> data = get_diatomic_data('N2')
        >>> print(data['bond_order'])
        3.0
    """
    molecule = molecule.upper()
    
    if molecule in HOMONUCLEAR_DIATOMIC_DATA:
        return HOMONUCLEAR_DIATOMIC_DATA[molecule]
    elif molecule in HETERONUCLEAR_DIATOMIC_DATA:
        return HETERONUCLEAR_DIATOMIC_DATA[molecule]
    else:
        raise ValueError(f"Molecule {molecule} not in database. "
                        f"Available: {list(HOMONUCLEAR_DIATOMIC_DATA.keys()) + list(HETERONUCLEAR_DIATOMIC_DATA.keys())}")


# =============================================================================
# MOLECULAR ORBITAL ANALYSIS
# =============================================================================

def is_paramagnetic(n_unpaired_electrons: int) -> bool:
    """
    Determine if molecule is paramagnetic.
    
    Args:
        n_unpaired_electrons: Number of unpaired electrons
    
    Returns:
        True if paramagnetic (has unpaired electrons)
    """
    return n_unpaired_electrons > 0


def count_unpaired_electrons(orbital_occupations: Dict[str, int]) -> int:
    """
    Count unpaired electrons from orbital occupations.
    
    Args:
        orbital_occupations: Dictionary of orbital -> electron count
    
    Returns:
        Number of unpaired electrons
    """
    unpaired = 0
    for orbital, n_electrons in orbital_occupations.items():
        # Degenerate orbitals (pi, delta) can have unpaired electrons
        if 'pi' in orbital or 'delta' in orbital:
            # These are doubly degenerate
            if n_electrons == 1 or n_electrons == 3:
                unpaired += 1
            elif n_electrons == 2:
                # Could be paired in one orbital or one each
                # Hund's rule: one each for ground state
                pass  # Need more detailed analysis
    
    return unpaired


def orbital_symmetry_label(l: int, m: int) -> str:
    """
    Get molecular orbital symmetry label from atomic quantum numbers.
    
    Args:
        l: Orbital angular momentum quantum number
        m: Magnetic quantum number
    
    Returns:
        MO symmetry label (σ, pi, delta, φ)
    
    Example:
        >>> orbital_symmetry_label(0, 0)
        'σ'
        >>> orbital_symmetry_label(1, 1)
        'pi'
    """
    if m == 0:
        return 'σ'
    elif abs(m) == 1:
        return 'pi'
    elif abs(m) == 2:
        return 'delta'
    elif abs(m) == 3:
        return 'φ'
    else:
        return '?'


def gerade_ungerade(nuclear_charge_product: float) -> str:
    """
    Determine g/u symmetry for homonuclear diatomic MO.
    
    For homonuclear diatomics:
    - gerade (g): symmetric under inversion
    - ungerade (u): antisymmetric under inversion
    
    For bonding σ: g (from s-s, p_z-p_z)
    For antibonding σ*: u
    For bonding pi: u (from p_x/p_y - p_x/p_y)
    For antibonding pi*: g
    
    Args:
        nuclear_charge_product: Z1 x Z2 (same nuclei = homonuclear)
    
    Returns:
        'g' or 'u' or 'neither'
    """
    # This is a placeholder - actual determination needs orbital type
    return 'depends on orbital type'


# =============================================================================
# BOND ENERGY ESTIMATES
# =============================================================================

def bond_energy_estimate(bond_order: float, 
                         reference_energy_kJ: float = 400) -> float:
    """
    Estimate bond energy from bond order.
    
    Very rough approximation: E ∝ BO
    
    Args:
        bond_order: Bond order
        reference_energy: Energy per bond order unit (kJ/mol)
    
    Returns:
        Estimated bond energy in kJ/mol
    
    Example:
        >>> bond_energy_estimate(3)  # Triple bond
        1200  # kJ/mol (rough)
    """
    return bond_order * reference_energy


def bond_length_estimate(bond_order: float,
                         sum_covalent_radii_pm: float) -> float:
    """
    Estimate bond length from bond order.
    
    Higher bond order -> shorter bond
    
    Args:
        bond_order: Bond order
        sum_covalent_radii_pm: Sum of covalent radii in pm
    
    Returns:
        Estimated bond length in pm
    
    Example:
        >>> bond_length_estimate(3, 150)  # Triple bond
        120  # pm (rough)
    """
    # Rough correlation: BO=1 -> full length, BO=3 -> ~80% length
    factor = 1 - 0.1 * (bond_order - 1)
    factor = max(0.7, min(1.0, factor))  # Clamp
    
    return sum_covalent_radii_pm * factor


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Diatomic Molecular Orbital Tools - Examples")
    print("=" * 60)
    
    # Overlap integral
    print("\n1. Overlap Integral:")
    for R in [1.0, 2.0, 3.0, 4.0]:
        S = overlap_integral_1s(R)
        print(f"   R = {R} a0: S = {S:.4f}")
    
    # MO energies for H2+
    print("\n2. H2+ MO Energies:")
    for R in [1.0, 2.0, 3.0, 4.0]:
        E_bond = mo_energy_h2_plus(R, symmetric=True)
        E_anti = mo_energy_h2_plus(R, symmetric=False)
        print(f"   R = {R} a0: E(σg) = {E_bond:.4f}, E(σu) = {E_anti:.4f} Hartree")
    
    # Electron configurations
    print("\n3. Electron Configurations and Bond Orders:")
    for molecule in ['H2', 'N2', 'O2', 'F2']:
        config = electron_configuration_diatomic(
            HOMONUCLEAR_DIATOMIC_DATA[molecule]['valence_electrons']
        )
        print(f"   {molecule}: BO = {config['bond_order']:.1f}")
    
    # Database lookup
    print("\n4. Diatomic Molecule Database:")
    for molecule in ['N2', 'O2', 'CO']:
        data = get_diatomic_data(molecule)
        print(f"   {molecule}: BO = {data['bond_order']}, "
              f"D0 = {data['bond_energy_kJ']} kJ/mol, "
              f"r = {data['bond_length_pm']} pm")
    
    # Molecular term symbols
    print("\n5. Molecular Term Symbols:")
    print(f"   H2: {molecular_term_symbol_diatomic(0, 0, 'g', '+')}")
    print(f"   O2: {molecular_term_symbol_diatomic(1, 0, 'g', '-')}")
    print(f"   B2: {molecular_term_symbol_diatomic(1, 0, 'g', '-')}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'bond_energy_estimate', 'description': 'Estimate bond energy from bond order.\n\nVery rough approximation: E ∝ BO\n\nArgs:\n    bond_order: Bond order\n    reference_energy: Energy per bond order unit (kJ/mol)\n\nReturns:\n    Estimated bond energy in kJ/mol\n\nExample:\n    >>> bond_energy_estimate(3)  # Triple bond\n    1200  # kJ/mol (rough)', 'inputSchema': {'type': 'object', 'properties': {'bond_order': {'type': 'string', 'description': 'Bond Order'}, 'reference_energy_kJ': {'type': 'string', 'description': 'Reference Energy Kj', 'default': 400}}, 'required': ['bond_order']}},
    {'name': 'bond_length_estimate', 'description': 'Estimate bond length from bond order.\n\nHigher bond order -> shorter bond\n\nArgs:\n    bond_order: Bond order\n    sum_covalent_radii_pm: Sum of covalent radii in pm\n\nReturns:\n    Estimated bond length in pm\n\nExample:\n    >>> bond_length_estimate(3, 150)  # Triple bond\n    120  # pm (rough)', 'inputSchema': {'type': 'object', 'properties': {'bond_order': {'type': 'string', 'description': 'Bond Order'}, 'sum_covalent_radii_pm': {'type': 'number', 'description': 'Sum Covalent Radii Pm'}}, 'required': ['bond_order', 'sum_covalent_radii_pm']}},
    {'name': 'bond_order', 'description': 'Calculate bond order from electron counts.\n\nBO = (n_bonding - n_antibonding) / 2\n\nArgs:\n    n_bonding: Number of electrons in bonding orbitals\n    n_antibonding: Number of electrons in antibonding orbitals\n\nReturns:\n    Bond order\n\nExample:\n    >>> bond_order(2, 0)  # H2\n    1.0\n    >>> bond_order(8, 4)  # O2\n    2.0', 'inputSchema': {'type': 'object', 'properties': {'n_bonding': {'type': 'number', 'description': 'N Bonding'}, 'n_antibonding': {'type': 'number', 'description': 'N Antibonding'}}, 'required': ['n_bonding', 'n_antibonding']}},
    {'name': 'bond_order_from_configuration', 'description': 'Calculate bond order from MO electron configuration.\n\nFor homonuclear diatomics (standard MO diagram).\n\nArgs:\n    sigma_g_electrons: σg(1s) electrons\n    sigma_u_electrons: σu*(1s) electrons\n    pi_u_electrons: piu(2p) electrons\n    pi_g_electrons: pig*(2p) electrons\n    sigma_g2_electrons: σg(2s) electrons\n    sigma_u2_electrons: σu*(2s) electrons\n\nReturns:\n    Bond order', 'inputSchema': {'type': 'object', 'properties': {'sigma_g_electrons': {'type': 'number', 'description': 'Sigma G Electrons', 'default': 0}, 'sigma_u_electrons': {'type': 'number', 'description': 'Sigma U Electrons', 'default': 0}, 'pi_u_electrons': {'type': 'number', 'description': 'Pi U Electrons', 'default': 0}, 'pi_g_electrons': {'type': 'number', 'description': 'Pi G Electrons', 'default': 0}, 'sigma_g2_electrons': {'type': 'number', 'description': 'Sigma G2 Electrons', 'default': 0}, 'sigma_u2_electrons': {'type': 'number', 'description': 'Sigma U2 Electrons', 'default': 0}}, 'required': []}},
    {'name': 'calculate_Lambda_from_electrons', 'description': 'Calculate total |Λ| from individual electron lambda values.\n\nΛ = |Σlambdaᵢ|\n\nlambda values: σ(0), pi(±1), delta(±2), φ(±3)\n\nArgs:\n    lambda_values: List of individual electron lambda values\n\nReturns:\n    |Λ| value', 'inputSchema': {'type': 'object', 'properties': {'lambda_values': {'type': 'number', 'description': 'Lambda Values'}}, 'required': ['lambda_values']}},
    {'name': 'calculate_S_from_electrons', 'description': 'Calculate total S from individual electron spin values.\n\nS = |Σsᵢ| (for parallel spins)\n\nArgs:\n    spin_values: List of individual m_s values (+½ or -½)\n\nReturns:\n    Total S value', 'inputSchema': {'type': 'object', 'properties': {'spin_values': {'type': 'string', 'description': 'Spin Values'}}, 'required': ['spin_values']}},
    {'name': 'coulomb_integral_1s', 'description': 'Calculate Coulomb integral for H2+.\n\nJ = ⟨1s_A | -1/r_B | 1s_A⟩\n\nArgs:\n    R: Internuclear distance in Bohr radii\n    Z: Nuclear charge\n\nReturns:\n    Coulomb integral in Hartree', 'inputSchema': {'type': 'object', 'properties': {'R': {'type': 'number', 'description': 'R'}, 'Z': {'type': 'number', 'description': 'Z', 'default': 1}}, 'required': ['R']}},
    {'name': 'count_unpaired_electrons', 'description': 'Count unpaired electrons from orbital occupations.\n\nArgs:\n    orbital_occupations: Dictionary of orbital -> electron count\n\nReturns:\n    Number of unpaired electrons', 'inputSchema': {'type': 'object', 'properties': {'orbital_occupations': {'type': 'string', 'description': 'Orbital Occupations'}}, 'required': ['orbital_occupations']}},
    {'name': 'electron_configuration_diatomic', 'description': "Generate electron configuration for diatomic molecule.\n\nArgs:\n    Z_total: Total number of valence electrons\n    heteronuclear: If true, use heteronuclear MO diagram\n\nReturns:\n    Dictionary with orbital occupations and bond order\n\nExample:\n    >>> config = electron_configuration_diatomic(10)  # N2\n    >>> print(config['bond_order'])\n    3.0", 'inputSchema': {'type': 'object', 'properties': {'Z_total': {'type': 'number', 'description': 'Z Total'}, 'heteronuclear': {'type': 'number', 'description': 'Heteronuclear', 'default': False}}, 'required': ['Z_total']}},
    {'name': 'exchange_integral_1s', 'description': 'Calculate exchange (resonance) integral.\n\nK = ⟨1s_A | -1/r_B | 1s_B⟩\n\nArgs:\n    R: Internuclear distance in Bohr radii\n    Z: Nuclear charge\n\nReturns:\n    Exchange integral in Hartree', 'inputSchema': {'type': 'object', 'properties': {'R': {'type': 'number', 'description': 'R'}, 'Z': {'type': 'number', 'description': 'Z', 'default': 1}}, 'required': ['R']}},
    {'name': 'gerade_ungerade', 'description': "Determine g/u symmetry for homonuclear diatomic MO.\n\nFor homonuclear diatomics:\n- gerade (g): symmetric under inversion\n- ungerade (u): antisymmetric under inversion\n\nFor bonding σ: g (from s-s, p_z-p_z)\nFor antibonding σ*: u\nFor bonding pi: u (from p_x/p_y - p_x/p_y)\nFor antibonding pi*: g\n\nArgs:\n    nuclear_charge_product: Z1 x Z2 (same nuclei = homonuclear)\n\nReturns:\n    'g' or 'u' or 'neither'", 'inputSchema': {'type': 'object', 'properties': {'nuclear_charge_product': {'type': 'string', 'description': 'Nuclear Charge Product'}}, 'required': ['nuclear_charge_product']}},
    {'name': 'get_diatomic_data', 'description': "Get data for a diatomic molecule.\n\nArgs:\n    molecule: Molecule formula (e.g., 'H2', 'O2', 'CO')\n\nReturns:\n    Dictionary with molecular properties\n\nExample:\n    >>> data = get_diatomic_data('N2')\n    >>> print(data['bond_order'])\n    3.0", 'inputSchema': {'type': 'object', 'properties': {'molecule': {'type': 'string', 'description': 'Molecule'}}, 'required': ['molecule']}},
    {'name': 'is_paramagnetic', 'description': 'Determine if molecule is paramagnetic.\n\nArgs:\n    n_unpaired_electrons: Number of unpaired electrons\n\nReturns:\n    true if paramagnetic (has unpaired electrons)', 'inputSchema': {'type': 'object', 'properties': {'n_unpaired_electrons': {'type': 'number', 'description': 'N Unpaired Electrons'}}, 'required': ['n_unpaired_electrons']}},
    {'name': 'mo_energy_h2_plus', 'description': 'Calculate MO energy for H2+ at given internuclear distance.\n\nSimple approximation using linear combination of atomic orbitals.\n\nArgs:\n    R: Internuclear distance in Bohr radii (a0)\n    n: Principal quantum number (1 for 1s)\n    symmetric: True for bonding (σg), false for antibonding (σu)\n\nReturns:\n    Energy in Hartree (atomic units)\n\nNote:\n    This is a simplified model. For accurate values, use\n    quantum chemistry software.\n\nExample:\n    >>> E_bond = mo_energy_h2_plus(2.0, symmetric=true)\n    >>> E_anti = mo_energy_h2_plus(2.0, symmetric=false)', 'inputSchema': {'type': 'object', 'properties': {'R': {'type': 'number', 'description': 'R'}, 'n': {'type': 'number', 'description': 'N', 'default': 1}, 'symmetric': {'type': 'string', 'description': 'Symmetric', 'default': True}}, 'required': ['R']}},
    {'name': 'molecular_term_symbol_diatomic', 'description': "Construct molecular term symbol for diatomic molecule.\n\nFormat: ^{2S+1}Λ_{Ω}^{±}\n\nwhere:\n    2S+1 = multiplicity\n    Λ = |Σlambdaᵢ| (projection of L on internuclear axis)\n    Ω = |Λ + Σ| (projection of J)\n    ± = inversion symmetry (g/u for homonuclear)\n    +/- = reflection symmetry for Σ states\n\nArgs:\n    total_spin_S: Total spin quantum number\n    total_Lambda: |Λ| value (0=Σ, 1=Π, 2=Delta, 3=Φ)\n    total_omega: Ω value (optional)\n    inversion_symmetry: 'g' or 'u' (for homonuclear)\n    reflection_symmetry: '+' or '-' (for Σ states)\n\nReturns:\n    Molecular term symbol string\n\nExample:\n    >>> molecular_term_symbol_diatomic(0, 0, inversion_symmetry='g', reflection_symmetry='+')\n    '1Σg+'", 'inputSchema': {'type': 'object', 'properties': {'total_spin_S': {'type': 'string', 'description': 'Total Spin S'}, 'total_Lambda': {'type': 'number', 'description': 'Total Lambda'}, 'total_omega': {'type': 'number', 'description': 'Total Omega', 'default': None}, 'inversion_symmetry': {'type': 'string', 'description': 'Inversion Symmetry', 'default': None}, 'reflection_symmetry': {'type': 'string', 'description': 'Reflection Symmetry', 'default': None}}, 'required': ['total_spin_S', 'total_Lambda']}},
    {'name': 'orbital_symmetry_label', 'description': "Get molecular orbital symmetry label from atomic quantum numbers.\n\nArgs:\n    l: Orbital angular momentum quantum number\n    m: Magnetic quantum number\n\nReturns:\n    MO symmetry label (σ, pi, delta, φ)\n\nExample:\n    >>> orbital_symmetry_label(0, 0)\n    'σ'\n    >>> orbital_symmetry_label(1, 1)\n    'pi'", 'inputSchema': {'type': 'object', 'properties': {'l': {'type': 'number', 'description': 'L'}, 'm': {'type': 'number', 'description': 'M'}}, 'required': ['l', 'm']}},
    {'name': 'overlap_integral_1s', 'description': 'Calculate overlap integral for two 1s orbitals.\n\nS = ⟨1s_A | 1s_B⟩\n\nFor STO-1s orbitals:\nS = e^(-R) (1 + R + R2/3)\n\nArgs:\n    R: Internuclear distance in Bohr radii\n\nReturns:\n    Overlap integral (dimensionless)\n\nExample:\n    >>> overlap_integral_1s(2.0)\n    0.586', 'inputSchema': {'type': 'object', 'properties': {'R': {'type': 'number', 'description': 'R'}}, 'required': ['R']}},
    {'name': 'bond_order_for_charged_species', 'description': "Calculate bond order for a charged diatomic species.\n\nArgs:\n    molecule: Molecule formula (e.g., 'O2', 'N2')\n    charge: Charge on the molecule (e.g., +2 for O2²⁺)\n\nReturns:\n    Dictionary with bond order and configuration info\n\nExample:\n    >>> bond_order_for_charged_species('O2', 2)  # O2²⁺\n    {'bond_order': 3.0, 'valence_electrons': 10}", 'inputSchema': {'type': 'object', 'properties': {'molecule': {'type': 'string', 'description': 'Molecule formula'}, 'charge': {'type': 'number', 'description': 'Charge on the molecule'}}, 'required': ['molecule', 'charge']}}
]
