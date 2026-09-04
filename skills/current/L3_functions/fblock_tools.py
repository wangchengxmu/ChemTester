"""
L3 Implementation: f-Block Chemistry Tools
Source: L2_principles/fblock_lanthanides.md, fblock_actinides.md

This module provides functions for lanthanide and actinide chemistry calculations.
## Solver Instructions (for AI Agent)

When you encounter f-block (lanthanide/actinide) chemistry problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given lanthanide/actinide -> Find oxidation states? Use `oxidation_states(element)`
- Ionic radius needed? Use `ln3_ionic_radius(element, coordination_number)` or `ln3_ionic_radius_cn8(element)`
- f-electron count? Use `f_electron_count(element, oxidation_state)`
- Solution color? Use `ln3_solution_color(element)`
- Lanthanide contraction? Use `lanthanide_contraction_summary()`
- Separation factor? Use `separation_factor(Z1, Z2)`
- Magnetic moment? Use `effective_magnetic_moment(n_unpaired)`
- Actinide info? Use `actinide_info(element)`

### Step 2: Handle special cases
- **Lanthanide contraction**: Ln3+ radii decrease from La3+ (103 pm) to Lu3+ (86 pm) across the series
- **Oxidation states**: Most lanthanides are +3; Ce, Tb can be +4; Sm, Eu, Yb can be +2
- **Actinides**: Much wider range of oxidation states (e.g., U: +3 to +6)
- **Coordination number**: CN=6 and CN=8 radii available

### Examples
```python
# Example 1: Ionic radius
ln3_ionic_radius('Gd', 6)  # -> 93.8 pm

# Example 2: f-electron count
f_electron_count('Eu', 3)  # -> 6 (Eu3+ has 4f6)

# Example 3: Magnetic moment
effective_magnetic_moment(7)  # -> 7.94 muB (Gd3+)
```
"""

import math
from typing import Union, List, Tuple, Dict, Optional

# ============================================================================
# L4 Reference Data (embedded for efficiency)
# ============================================================================

# Shannon ionic radii for Ln3+ in pm (picometers)
# Source: Shannon, R.D. Acta Cryst. A32, 751-767 (1976)
LN3_RADII_CN6 = {
    'La': 103.2, 'Ce': 101.0, 'Pr': 99.0, 'Nd': 98.3,
    'Pm': 97.0, 'Sm': 95.8, 'Eu': 94.7, 'Gd': 93.8,
    'Tb': 92.3, 'Dy': 91.2, 'Ho': 90.1, 'Er': 89.0,
    'Tm': 88.0, 'Yb': 86.8, 'Lu': 86.1
}

LN3_RADII_CN8 = {
    'La': 116.0, 'Ce': 114.3, 'Pr': 112.6, 'Nd': 110.9,
    'Pm': 109.5, 'Sm': 107.9, 'Eu': 106.6, 'Gd': 105.3,
    'Tb': 104.0, 'Dy': 102.7, 'Ho': 101.5, 'Er': 100.4,
    'Tm': 99.4, 'Yb': 98.5, 'Lu': 97.7
}

# f-electron configurations for Ln3+
LN3_CONFIG = {
    'La': 0, 'Ce': 1, 'Pr': 2, 'Nd': 3, 'Pm': 4,
    'Sm': 5, 'Eu': 6, 'Gd': 7, 'Tb': 8, 'Dy': 9,
    'Ho': 10, 'Er': 11, 'Tm': 12, 'Yb': 13, 'Lu': 14
}

# Solution colors for Ln3+ ions
LN3_COLORS = {
    'La': 'colorless', 'Ce': 'colorless', 'Pr': 'green',
    'Nd': 'reddish', 'Pm': 'pink/yellow', 'Sm': 'yellow',
    'Eu': 'pale pink', 'Gd': 'colorless', 'Tb': 'pale pink',
    'Dy': 'yellow', 'Ho': 'pink/yellow', 'Er': 'reddish',
    'Tm': 'green', 'Yb': 'colorless', 'Lu': 'colorless'
}

# Stable oxidation states
OXIDATION_STATES = {
    'La': [3], 'Ce': [3, 4], 'Pr': [3, 4], 'Nd': [3],
    'Pm': [3], 'Sm': [2, 3], 'Eu': [2, 3], 'Gd': [3],
    'Tb': [3, 4], 'Dy': [3], 'Ho': [3], 'Er': [3],
    'Tm': [2, 3], 'Yb': [2, 3], 'Lu': [3],
    # Actinides
    'Ac': [3], 'Th': [4], 'Pa': [4, 5], 'U': [3, 4, 5, 6],
    'Np': [3, 4, 5, 6, 7], 'Pu': [3, 4, 5, 6, 7], 'Am': [2, 3, 4, 5, 6],
    'Cm': [3, 4], 'Bk': [3, 4], 'Cf': [2, 3, 4], 'Es': [2, 3],
    'Fm': [2, 3], 'Md': [2, 3], 'No': [2, 3], 'Lr': [3]
}


def ionic_radius(element: str, oxidation_state: int = 3, 
                  coordination_number: int = 6) -> Optional[float]:
    """
    Return Shannon ionic radius for f-block elements.
    
    Args:
        element: Element symbol (e.g., 'La', 'Ce', 'U')
        oxidation_state: Oxidation state (default: 3)
        coordination_number: CN (6 or 8 for Ln3+, default: 6)
    
    Returns:
        Ionic radius in picometers (pm), or None if not available
    
    Examples:
        >>> ionic_radius('La', 3, 6)
        103.2
        >>> ionic_radius('Gd', 3, 8)
        105.3
        >>> ionic_radius('Ce', 4, 6)  # Ce4+
        87.0
    """
    element = element.capitalize()
    
    # Handle Ln3+ radii
    if oxidation_state == 3:
        if coordination_number == 6:
            return LN3_RADII_CN6.get(element)
        elif coordination_number == 8:
            return LN3_RADII_CN8.get(element)
    
    # Ce4+ special case
    if element == 'Ce' and oxidation_state == 4:
        return 87.0  # CN=6
    
    return None


def electron_config_fblock(element: str) -> Dict[str, int]:
    """
    Return f-electron configuration for lanthanide/actinide.
    
    Args:
        element: Element symbol
    
    Returns:
        Dictionary with 'f_electrons', 'd_electrons', 's_electrons'
    
    Examples:
        >>> electron_config_fblock('Gd')
        {'f_electrons': 7, 'd_electrons': 1, 's_electrons': 2}
        >>> electron_config_fblock('Lu')
        {'f_electrons': 14, 'd_electrons': 1, 's_electrons': 2}
    """
    element = element.capitalize()
    f_electrons = LN3_CONFIG.get(element, 0)
    
    # Most lanthanides: [Xe] 4f^n 6s2
    # Exceptions: Gd (4f75d16s2), Lu (4f145d16s2)
    exceptions = {'Gd': (7, 1), 'Lu': (14, 1)}
    
    if element in exceptions:
        f, d = exceptions[element]
        return {'f_electrons': f, 'd_electrons': d, 's_electrons': 2}
    
    # Standard configuration
    return {'f_electrons': f_electrons, 'd_electrons': 0, 's_electrons': 2}


def oxidation_states(element: str) -> List[int]:
    """
    Return stable oxidation states for f-block element.
    
    Args:
        element: Element symbol
    
    Returns:
        List of stable oxidation states
    
    Examples:
        >>> oxidation_states('Ce')
        [3, 4]
        >>> oxidation_states('Eu')
        [2, 3]
        >>> oxidation_states('Gd')
        [3]
    """
    return OXIDATION_STATES.get(element.capitalize(), [3])


def unpaired_electrons_f(element: str, oxidation_state: int = 3) -> int:
    """
    Count unpaired electrons in f-orbitals for f-block ion.
    
    Uses Hund's rule: electrons fill orbitals singly first.
    
    Args:
        element: Element symbol
        oxidation_state: Oxidation state (default: 3)
    
    Returns:
        Number of unpaired f-electrons
    
    Examples:
        >>> unpaired_electrons_f('Gd', 3)  # Gd3+ = 4f7
        7
        >>> unpaired_electrons_f('La', 3)  # La3+ = 4f0
        0
        >>> unpaired_electrons_f('Lu', 3)  # Lu3+ = 4f14
        0
    """
    element = element.capitalize()
    f_count = LN3_CONFIG.get(element, 0)
    
    # Hund's rule: maximum unpaired = min(f_count, 14 - f_count) for half-filling
    # But f-orbitals have 7 orbitals, max 14 electrons
    if f_count <= 7:
        return f_count  # All unpaired until half-filled
    else:
        return 14 - f_count  # Pairing after half-filled


def magnetic_moment_f(element: str, oxidation_state: int = 3) -> float:
    """
    Calculate spin-only magnetic moment for f-block ion.
    
    mu_eff = g√(J(J+1)) BM
    
    For f-block, spin-orbit coupling is significant.
    This uses simplified spin-only formula for quick estimation.
    
    Args:
        element: Element symbol
        oxidation_state: Oxidation state (default: 3)
    
    Returns:
        Magnetic moment in Bohr magnetons (BM)
    
    Examples:
        >>> magnetic_moment_f('Gd', 3)  # Gd3+ = 4f7, S=7/2
        7.94
        >>> magnetic_moment_f('La', 3)  # La3+ = 4f0
        0.0
    """
    n = unpaired_electrons_f(element, oxidation_state)
    
    if n == 0:
        return 0.0
    
    # Spin-only formula: mu = √(n(n+2)) BM
    return round(math.sqrt(n * (n + 2)), 2)


def lanthanide_color(element: str, oxidation_state: int = 3) -> str:
    """
    Return expected solution color for lanthanide ion.
    
    Args:
        element: Element symbol
        oxidation_state: Oxidation state (default: 3)
    
    Returns:
        Color description
    
    Examples:
        >>> lanthanide_color('Pr')
        'green'
        >>> lanthanide_color('Gd')
        'colorless'
    """
    element = element.capitalize()
    
    if oxidation_state == 3:
        return LN3_COLORS.get(element, 'unknown')
    
    # Ce4+ is yellow/orange
    if element == 'Ce' and oxidation_state == 4:
        return 'yellow/orange'
    
    return 'unknown'


def lanthanide_contraction(start: str = 'La', end: str = 'Lu',
                          coordination_number: int = 6) -> float:
    """
    Calculate lanthanide contraction (radius decrease).
    
    Args:
        start: Starting element (default: La)
        end: Ending element (default: Lu)
        coordination_number: CN for radii (default: 6)
    
    Returns:
        Decrease in ionic radius in pm
    
    Examples:
        >>> lanthanide_contraction()
        17.1
    """
    r_start = ionic_radius(start, 3, coordination_number)
    r_end = ionic_radius(end, 3, coordination_number)
    
    if r_start and r_end:
        return round(r_start - r_end, 1)
    return 0.0


def coordination_number_predict(element: str, oxidation_state: int = 3) -> List[int]:
    """
    Predict typical coordination numbers for f-block ion.
    
    Based on ionic radius and charge.
    
    Args:
        element: Element symbol
        oxidation_state: Oxidation state (default: 3)
    
    Returns:
        List of likely coordination numbers
    
    Examples:
        >>> coordination_number_predict('La', 3)
        [8, 9, 10, 12]
        >>> coordination_number_predict('Lu', 3)
        [6, 7, 8]
    """
    radius = ionic_radius(element, oxidation_state, 6)
    
    if radius is None:
        return [8]  # Default
    
    # Larger ions can accommodate higher CN
    if radius > 100:  # Light lanthanides
        return [8, 9, 10, 12]
    elif radius > 95:  # Middle lanthanides
        return [8, 9, 10]
    else:  # Heavy lanthanides
        return [6, 7, 8]


# ============================================================================
# G10: Lanthanide J-Dependent Magnetic Moment Functions
# ============================================================================

# Ground state term symbols for Ln3+ ions (Russell-Saunders coupling)
# Format: {'Element': (S, L, J, term_symbol)}
LN3_GROUND_TERMS = {
    'La': (0, 0, 0, '1S0'),       # 4f0
    'Ce': (1/2, 3, 5/2, '2F5/2'), # 4f1
    'Pr': (1, 5, 4, '3H4'),       # 4f2
    'Nd': (3/2, 6, 9/2, '4I9/2'), # 4f3
    'Pm': (2, 6, 4, '5I4'),       # 4f4
    'Sm': (5/2, 5, 5/2, '6H5/2'), # 4f5
    'Eu': (3, 3, 0, '7F0'),       # 4f6
    'Gd': (7/2, 0, 7/2, '8S7/2'), # 4f7
    'Tb': (3, 3, 6, '7F6'),       # 4f8
    'Dy': (5/2, 5, 15/2, '6H15/2'), # 4f9
    'Ho': (2, 6, 8, '5I8'),       # 4f10
    'Er': (3/2, 6, 6, '4I15/2'),  # 4f11 (note: J = 6, but term symbol shows 15/2 for free ion)
    'Tm': (1, 5, 6, '3H6'),       # 4f12
    'Yb': (1/2, 3, 7/2, '2F7/2'), # 4f13
    'Lu': (0, 0, 0, '1S0')        # 4f14
}

# Corrected ground state J values for Ln3+ (from Hund's rules)
LN3_J_VALUES = {
    'La': 0, 'Ce': 5/2, 'Pr': 4, 'Nd': 9/2, 'Pm': 4,
    'Sm': 5/2, 'Eu': 0, 'Gd': 7/2, 'Tb': 6, 'Dy': 15/2,
    'Ho': 8, 'Er': 6, 'Tm': 6, 'Yb': 7/2, 'Lu': 0
}

# Ground state L values for Ln3+
LN3_L_VALUES = {
    'La': 0, 'Ce': 3, 'Pr': 5, 'Nd': 6, 'Pm': 6,
    'Sm': 5, 'Eu': 3, 'Gd': 0, 'Tb': 3, 'Dy': 5,
    'Ho': 6, 'Er': 6, 'Tm': 5, 'Yb': 3, 'Lu': 0
}

# Ground state S values for Ln3+
LN3_S_VALUES = {
    'La': 0, 'Ce': 1/2, 'Pr': 1, 'Nd': 3/2, 'Pm': 2,
    'Sm': 5/2, 'Eu': 3, 'Gd': 7/2, 'Tb': 3, 'Dy': 5/2,
    'Ho': 2, 'Er': 3/2, 'Tm': 1, 'Yb': 1/2, 'Lu': 0
}


def lande_g_factor(J: Union[int, float], L: Union[int, float], 
                   S: Union[int, float]) -> float:
    """
    Calculate the Landé g-factor for an ion.
    
    The Landé g-factor accounts for both spin and orbital contributions
    to the magnetic moment. This is essential for accurate magnetic moment
    predictions in lanthanides and actinides where spin-orbit coupling is strong.
    
    Formula:
        g_J = 1 + [J(J+1) + S(S+1) - L(L+1)] / [2J(J+1)]
    
    For J = 0, g_J is undefined (returns 0 as ion is diamagnetic).
    
    Args:
        J: Total angular momentum quantum number
        L: Orbital angular momentum quantum number
        S: Spin angular momentum quantum number
    
    Returns:
        Landé g-factor (dimensionless)
    
    Examples:
        >>> lande_g_factor(7/2, 0, 7/2)  # Gd3+ (S-state, L=0)
        2.0
        >>> lande_g_factor(6, 3, 3)  # Tb3+
        1.5
        >>> lande_g_factor(0, 0, 0)  # La3+ (J=0, diamagnetic)
        0.0
    
    Note:
        For pure spin (L=0), g_J = 2.0 (spin-only value)
        For pure orbital (S=0), g_J = 1.0
    """
    if J == 0:
        return 0.0  # Diamagnetic, J=0 state
    
    numerator = J * (J + 1) + S * (S + 1) - L * (L + 1)
    denominator = 2 * J * (J + 1)
    
    g_J = 1 + numerator / denominator
    return round(g_J, 4)


def jj_magnetic_moment(J: Union[int, float], g_J: float, 
                        n: Optional[int] = None) -> float:
    """
    Calculate the J-dependent magnetic moment using the Landé formula.
    
    This gives the correct magnetic moment for lanthanides and actinides
    where spin-orbit coupling is significant. The spin-only formula
    is INACCURATE for heavy lanthanides (Tb, Dy, Ho, Er, Tm).
    
    Formula:
        mu_eff = g_J x √(J(J+1)) BM
    
    Args:
        J: Total angular momentum quantum number
        g_J: Landé g-factor (use lande_g_factor() to calculate)
        n: Number of unpaired electrons (optional, for spin-only comparison)
    
    Returns:
        Effective magnetic moment in Bohr magnetons (BM)
    
    Examples:
        >>> g_gd = lande_g_factor(7/2, 0, 7/2)
        >>> jj_magnetic_moment(7/2, g_gd)  # Gd3+
        7.94
        >>> g_tb = lande_g_factor(6, 3, 3)
        >>> jj_magnetic_moment(6, g_tb)  # Tb3+ (J=6)
        9.72
        >>> g_dy = lande_g_factor(15/2, 5, 5/2)
        >>> jj_magnetic_moment(15/2, g_dy)  # Dy3+
        10.65
    
    Note:
        Comparison with spin-only (mu_so = √(n(n+2))):
        - Gd3+: J-dependent = 7.94, spin-only = 7.94 ✓ (L=0)
        - Tb3+: J-dependent = 9.72, spin-only = 7.94 (large difference!)
        - Dy3+: J-dependent = 10.65, spin-only = 5.92 (huge difference!)
    """
    if J == 0 or g_J == 0:
        return 0.0  # Diamagnetic
    
    mu_eff = g_J * math.sqrt(J * (J + 1))
    return round(mu_eff, 2)


def magnetic_moment_jj(element: str, oxidation_state: int = 3) -> Dict[str, float]:
    """
    Calculate J-dependent magnetic moment for lanthanide ion.
    
    Returns both the J-dependent moment (correct) and spin-only moment
    (approximation) for comparison.
    
    Args:
        element: Element symbol
        oxidation_state: Oxidation state (default: 3)
    
    Returns:
        Dictionary with 'jj_moment', 'spin_only', 'g_factor', 'J', 'L', 'S'
    
    Examples:
        >>> magnetic_moment_jj('Tb')  # Tb3+
        {'jj_moment': 9.72, 'spin_only': 7.94, 'g_factor': 1.5, 'J': 6, 'L': 3, 'S': 3}
        >>> magnetic_moment_jj('Gd')  # Gd3+
        {'jj_moment': 7.94, 'spin_only': 7.94, 'g_factor': 2.0, 'J': 3.5, 'L': 0, 'S': 3.5}
    """
    element = element.capitalize()
    
    J = LN3_J_VALUES.get(element, 0)
    L = LN3_L_VALUES.get(element, 0)
    S = LN3_S_VALUES.get(element, 0)
    
    g_J = lande_g_factor(J, L, S)
    mu_jj = jj_magnetic_moment(J, g_J)
    
    # Spin-only for comparison
    n = unpaired_electrons_f(element, oxidation_state)
    mu_so = magnetic_moment_f(element, oxidation_state)
    
    return {
        'jj_moment': mu_jj,
        'spin_only': mu_so,
        'g_factor': g_J,
        'J': J,
        'L': L,
        'S': S,
        'n_unpaired': n
    }


# ============================================================================
# G11: Actinide Chemistry Functions
# ============================================================================

# Standard redox potentials for actinides (vs SHE, in V)
# Source: Various literature compilations
ACTINIDE_REDOX_POTENTIALS = {
    # Uranium redox couples
    'U': {
        'U3+/U': -1.80,
        'U4+/U3+': -0.61,
        'UO2+/U4+': 0.33,
        'UO22+/UO2+': 0.06,
    },
    # Neptunium redox couples
    'Np': {
        'Np3+/Np': -1.79,
        'Np4+/Np3+': 0.15,
        'NpO2+/Np4+': 0.74,
        'NpO22+/NpO2+': 1.24,
        'NpO23+/NpO22+': '~1.5',  # Np(VII)
    },
    # Plutonium redox couples
    'Pu': {
        'Pu3+/Pu': -2.03,
        'Pu4+/Pu3+': 0.97,
        'PuO2+/Pu4+': 1.04,
        'PuO22+/PuO2+': 0.94,
        'PuO23+/PuO22+': '~1.4',  # Pu(VII)
    },
    # Americium redox couples
    'Am': {
        'Am3+/Am': -2.07,
        'Am4+/Am3+': 2.62,
        'AmO2+/Am3+': 1.74,
        'AmO22+/AmO2+': 1.59,
    },
    # Curium redox couples
    'Cm': {
        'Cm3+/Cm': -2.02,
        'Cm4+/Cm3+': 3.2,
    },
    # Berkelium redox couples
    'Bk': {
        'Bk3+/Bk': -1.96,
        'Bk4+/Bk3+': 1.67,
    },
    # Californium redox couples
    'Cf': {
        'Cf3+/Cf': -1.93,
        'Cf4+/Cf3+': 3.2,
    },
}

# Shannon ionic radii for actinides (pm)
# Source: Shannon, R.D. Acta Cryst. A32, 751-767 (1976)
ACTINIDE_RADII_CN6 = {
    # An3+ radii
    'Ac': 112.0, 'Th': None, 'Pa': 104.0, 'U': 102.5, 'Np': 101.0,
    'Pu': 100.0, 'Am': 97.5, 'Cm': 96.0, 'Bk': 94.0, 'Cf': 92.0,
    'Es': 90.0, 'Fm': 88.0, 'Md': 86.0, 'No': 84.0, 'Lr': 82.0,
}

ACTINIDE_RADII_CN8 = {
    # An3+ radii (CN=8)
    'Ac': 126.0, 'Th': None, 'Pa': 118.0, 'U': 116.0, 'Np': 114.0,
    'Pu': 112.0, 'Am': 110.0, 'Cm': 109.0, 'Bk': 107.0, 'Cf': 105.0,
}

# An4+ radii (CN=6)
ACTINIDE_4_RADII_CN6 = {
    'Th': 94.0, 'Pa': 90.0, 'U': 89.0, 'Np': 87.0,
    'Pu': 85.0, 'Am': 85.0, 'Cm': 85.0, 'Bk': 83.0, 'Cf': 82.0,
}

# f-electron configurations for An3+
AN3_CONFIG = {
    'Ac': 0, 'Th': None, 'Pa': 2, 'U': 3, 'Np': 4,
    'Pu': 5, 'Am': 6, 'Cm': 7, 'Bk': 8, 'Cf': 9,
    'Es': 10, 'Fm': 11, 'Md': 12, 'No': 13, 'Lr': 14
}


def actinide_redox_potential(element: str, couple: str) -> Optional[float]:
    """
    Return standard redox potential for actinide couple.
    
    Args:
        element: Element symbol (e.g., 'U', 'Pu', 'Am')
        couple: Redox couple string (e.g., 'U4+/U3+', 'PuO22+/PuO2+')
    
    Returns:
        Standard redox potential in volts vs SHE, or None if not available
    
    Examples:
        >>> actinide_redox_potential('U', 'U4+/U3+')
        -0.61
        >>> actinide_redox_potential('Pu', 'Pu4+/Pu3+')
        0.97
        >>> actinide_redox_potential('U', 'UO22+/UO2+')
        0.06
    
    Note:
        Common couples:
        - U: U3+/U, U4+/U3+, UO2+/U4+, UO22+/UO2+
        - Np: Np3+/Np, Np4+/Np3+, NpO2+/Np4+, NpO22+/NpO2+
        - Pu: Pu3+/Pu, Pu4+/Pu3+, PuO2+/Pu4+, PuO22+/PuO2+
        - Am: Am3+/Am, AmO2+/Am3+, AmO22+/AmO2+
    """
    element = element.capitalize()
    
    if element in ACTINIDE_REDOX_POTENTIALS:
        potentials = ACTINIDE_REDOX_POTENTIALS[element]
        # Try exact match first
        if couple in potentials:
            val = potentials[couple]
            if isinstance(val, str) and '~' in val:
                return float(val.replace('~', ''))
            return val
        # Try reverse match (e.g., 'U3+/U4+' -> 'U4+/U3+')
        parts = couple.split('/')
        if len(parts) == 2:
            reverse = f"{parts[1]}/{parts[0]}"
            if reverse in potentials:
                val = potentials[reverse]
                if isinstance(val, str) and '~' in val:
                    return -float(val.replace('~', ''))
                return -val
    
    return None


def actinide_ionic_radius(element: str, oxidation_state: int = 3,
                          coordination_number: int = 6) -> Optional[float]:
    """
    Return Shannon ionic radius for actinide ions.
    
    Args:
        element: Element symbol
        oxidation_state: Oxidation state (3 or 4)
        coordination_number: CN (6 or 8)
    
    Returns:
        Ionic radius in picometers (pm), or None if not available
    
    Examples:
        >>> actinide_ionic_radius('U', 3, 6)
        102.5
        >>> actinide_ionic_radius('Pu', 4, 6)
        85.0
        >>> actinide_ionic_radius('Am', 3, 8)
        110.0
    """
    element = element.capitalize()
    
    if oxidation_state == 3:
        if coordination_number == 6:
            return ACTINIDE_RADII_CN6.get(element)
        elif coordination_number == 8:
            return ACTINIDE_RADII_CN8.get(element)
    elif oxidation_state == 4:
        if coordination_number == 6:
            return ACTINIDE_4_RADII_CN6.get(element)
    
    return None


def uranyl_bond_length(charge: int = 2) -> Dict[str, float]:
    """
    Return typical uranyl ion bond lengths.
    
    The uranyl ion (UO2^n+) is a linear oxycation with short, strong U=O bonds.
    
    Args:
        charge: Charge on uranyl ion (2+ or 1+)
    
    Returns:
        Dictionary with 'U-O bond length' in pm
    
    Examples:
        >>> uranyl_bond_length(2)  # UO22+
        {'U-O_bond_length_pm': 180.0, 'description': 'UO2^2+ (uranyl)'}
        >>> uranyl_bond_length(1)  # UO2+
        {'U-O_bond_length_pm': 185.0, 'description': 'UO2^+ (uranyl(V))'}
    """
    if charge == 2:
        return {
            'U-O_bond_length_pm': 180.0,
            'description': 'UO2^2+ (uranyl)',
            'typical_range_pm': '177-185'
        }
    elif charge == 1:
        return {
            'U-O_bond_length_pm': 185.0,
            'description': 'UO2^+ (uranyl(V))',
            'typical_range_pm': '182-190'
        }
    return {'U-O_bond_length_pm': None, 'description': 'Unknown'}


def list_actinide_oxidation_states(element: str) -> List[int]:
    """
    List known oxidation states for actinide element.
    
    Args:
        element: Element symbol
    
    Returns:
        List of known oxidation states
    
    Examples:
        >>> list_actinide_oxidation_states('U')
        [3, 4, 5, 6]
        >>> list_actinide_oxidation_states('Pu')
        [3, 4, 5, 6, 7]
        >>> list_actinide_oxidation_states('Am')
        [2, 3, 4, 5, 6]
    """
    element = element.capitalize()
    return OXIDATION_STATES.get(element, [3])


# ============================================================================
# Self-test
# ============================================================================

if __name__ == '__main__':
    print("f-Block Tools Test")
    print("=" * 40)
    
    # Test ionic radii
    print("\nIonic Radii (CN=6):")
    for elem in ['La', 'Gd', 'Lu']:
        print(f"  {elem}3+: {ionic_radius(elem, 3, 6)} pm")
    
    # Test magnetic moments
    print("\nMagnetic Moments (mu_eff):")
    for elem in ['Ce', 'Gd', 'Dy', 'Yb']:
        print(f"  {elem}3+: {magnetic_moment_f(elem)} BM")
    
    # Test colors
    print("\nSolution Colors:")
    for elem in ['Pr', 'Nd', 'Eu', 'Er']:
        print(f"  {elem}3+: {lanthanide_color(elem)}")
    
    # Lanthanide contraction
    print(f"\nLanthanide Contraction (La3+ to Lu3+): {lanthanide_contraction()} pm")
    
    # G10: Test J-dependent magnetic moments
    print("\n" + "=" * 40)
    print("J-Dependent Magnetic Moments (G10):")
    print("=" * 40)
    for elem in ['Tb', 'Dy', 'Ho', 'Er']:
        result = magnetic_moment_jj(elem)
        print(f"  {elem}3+: mu_JJ = {result['jj_moment']:.2f} BM, "
              f"mu_so = {result['spin_only']:.2f} BM, "
              f"g_J = {result['g_factor']:.3f}")
    
    # G11: Test actinide functions
    print("\n" + "=" * 40)
    print("Actinide Redox Potentials (G11):")
    print("=" * 40)
    for elem in ['U', 'Np', 'Pu', 'Am']:
        pot = actinide_redox_potential(elem, f'{elem}4+/{elem}3+')
        if pot:
            print(f"  {elem}4+/{elem}3+: Edeg = {pot:.2f} V")
    
    print("\nActinide Ionic Radii (CN=6, +3):")
    for elem in ['U', 'Np', 'Pu', 'Am', 'Cm']:
        r = actinide_ionic_radius(elem, 3, 6)
        print(f"  {elem}3+: {r} pm")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "actinide_ionic_radius",
        "description": "Return Shannon ionic radius for actinide ions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
                "coordination_number": {"type": "number", "description": "Coordination Number", "default": 6},
            },
            "required": ["element"]
        }
    },
    {
        "name": "actinide_redox_potential",
        "description": "Return standard redox potential for actinide couple.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "couple": {"type": "number", "description": "Couple"},
            },
            "required": ["element", "couple"]
        }
    },
    {
        "name": "coordination_number_predict",
        "description": "Predict typical coordination numbers for f-block ion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
            },
            "required": ["element"]
        }
    },
    {
        "name": "electron_config_fblock",
        "description": "Return f-electron configuration for lanthanide/actinide.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
            },
            "required": ["element"]
        }
    },
    {
        "name": "ionic_radius",
        "description": "Return Shannon ionic radius for f-block elements.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
                "coordination_number": {"type": "number", "description": "Coordination Number", "default": 6},
            },
            "required": ["element"]
        }
    },
    {
        "name": "jj_magnetic_moment",
        "description": "Calculate the J-dependent magnetic moment using the Land\u00e9 formula.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "J": {"type": "number", "description": "J"},
                "g_J": {"type": "number", "description": "G J"},
                "n": {"type": "number", "description": "N", "default": None},
            },
            "required": ["J", "g_J"]
        }
    },
    {
        "name": "lande_g_factor",
        "description": "Calculate the Land\u00e9 g-factor for an ion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "J": {"type": "number", "description": "J"},
                "L": {"type": "number", "description": "L"},
                "S": {"type": "number", "description": "S"},
            },
            "required": ["J", "L", "S"]
        }
    },
    {
        "name": "lanthanide_color",
        "description": "Return expected solution color for lanthanide ion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
            },
            "required": ["element"]
        }
    },
    {
        "name": "lanthanide_contraction",
        "description": "Calculate lanthanide contraction (radius decrease).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "start": {"type": "number", "description": "Start", "default": "La"},
                "end": {"type": "number", "description": "End", "default": "Lu"},
                "coordination_number": {"type": "number", "description": "Coordination Number", "default": 6},
            },
            "required": []
        }
    },
    {
        "name": "list_actinide_oxidation_states",
        "description": "List known oxidation states for actinide element.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
            },
            "required": ["element"]
        }
    },
    {
        "name": "magnetic_moment_f",
        "description": "Calculate spin-only magnetic moment for f-block ion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
            },
            "required": ["element"]
        }
    },
    {
        "name": "magnetic_moment_jj",
        "description": "Calculate J-dependent magnetic moment for lanthanide ion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
            },
            "required": ["element"]
        }
    },
    {
        "name": "oxidation_states",
        "description": "Return stable oxidation states for f-block element.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
            },
            "required": ["element"]
        }
    },
    {
        "name": "unpaired_electrons_f",
        "description": "Count unpaired electrons in f-orbitals for f-block ion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element": {"type": "string", "description": "Element"},
                "oxidation_state": {"type": "number", "description": "Oxidation State", "default": 3},
            },
            "required": ["element"]
        }
    },
    {
        "name": "uranyl_bond_length",
        "description": "Return typical uranyl ion bond lengths.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "charge": {"type": "number", "description": "Charge", "default": 2},
            },
            "required": []
        }
    }
]
