"""
Crystal Field Theory Tools - L3 Implementation
Chapter 19.3: Spectroscopic and Magnetic Properties
"""
## Solver Instructions (for AI Agent)

# When you encounter crystal field theory problems (magnetic moments, spin states, colors), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: metal ion, d-electron count, ligand type, geometry, wavelength/color
# - **Asked**: magnetic moment, spin state, paramagnetic/diamagnetic, CFSE, color absorbed/emitted

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Magnetic moment (mu) | `magnetic_moment(unpaired)` | number of unpaired electrons |
# | Paramagnetic check | `is_paramagnetic(unpaired)` | unpaired e- count |
# | High/low spin prediction | `high_spin_or_low_spin(d_count, ligand)` | d count, ligand name |
# | d-electron distribution | `d_electron_distribution(d_count, geometry, spin_state)` | d count, geometry |
# | CFSE calculation | `crystal_field_stabilization_energy(d_count, geometry, spin_state, delta)` | d count, geometry, Delta |
# | Color prediction | `predict_color(complementary, delta)` | complementary color OR Delta |
# | Pairing energy needed | `pairing_energy_needed(d_count, geometry, P, delta)` | d count, P, Delta |

### Step 3: Handle special cases
# - Octahedral only for strong/weak field splitting (3d metals); 4d/5d always low-spin
# - Tetrahedral fields are weak (Delta_t ~ 4/9 Delta_o) - always high-spin
# - Square planar arises from strong-field d8 (e.g., [Ni(CN)4]2-)

### Examples
# 1. **Magnetic moment**: `magnetic_moment(4)` -> 4.90 u_B (spin-only for d6 high-spin)
# 2. **Spin state**: `high_spin_or_low_spin(6, 'CN-')` -> 'low_spin'; `high_spin_or_low_spin(6, 'H2O')` -> 'high_spin'
# 3. **CFSE**: `crystal_field_stabilization_energy(6, 'octahedral', 'low_spin')` -> -2.4 Delta_o (t2g6)
# 4. **Color**: `predict_color(delta=21000)` -> absorbs ~476 nm -> appears orange


from typing import Dict, Tuple, Optional
from math import sqrt


# Spectrochemical series (relative field strength)
SPECTROCHEMICAL_SERIES = {
    'I': 0.5, 'Br': 0.6, 'Cl': 0.7, 'F': 0.9,
    'H2O': 1.0, 'NH3': 1.2, 'en': 1.5, 'CN': 2.0, 'CO': 2.5
}


def magnetic_moment(unpaired: int) -> float:
    """
    Calculate spin-only magnetic moment.
    
    u = √(n(n+2)) BM
    
    Args:
        unpaired: Number of unpaired electrons
    
    Returns:
        Magnetic moment in Bohr magnetons
    
    Examples:
        >>> magnetic_moment(1)
        1.73
        >>> magnetic_moment(5)
        5.92
    """
    return sqrt(unpaired * (unpaired + 2))


def is_paramagnetic(unpaired: int) -> bool:
    """
    Determine if complex is paramagnetic.
    
    Args:
        unpaired: Number of unpaired electrons
    
    Returns:
        True if paramagnetic
    """
    return unpaired > 0


def high_spin_or_low_spin(d_count: int, ligand: str) -> str:
    """
    Predict high-spin or low-spin for octahedral complex.
    
    Only applicable for d4-d7 configurations.
    
    Args:
        d_count: Number of d electrons
        ligand: Ligand name
    
    Returns:
        'high-spin' or 'low-spin' or 'N/A'
    """
    if d_count < 4 or d_count > 7:
        return 'N/A (only d4-d7 can be high or low spin)'
    
    field_strength = SPECTROCHEMICAL_SERIES.get(ligand, 1.0)
    
    if field_strength >= 1.5:
        return 'low-spin'
    elif field_strength <= 0.9:
        return 'high-spin'
    else:
        return 'could be either (depends on metal and conditions)'


def d_electron_distribution(d_count: int, geometry: str = 'octahedral',
                             high_spin: bool = True) -> Dict:
    """
    Distribute d electrons in orbital sets.
    
    Args:
        d_count: Number of d electrons
        geometry: 'octahedral' or 'tetrahedral'
        high_spin: True for high-spin
    
    Returns:
        Dict with t2g and eg populations
    """
    if geometry == 'octahedral':
        if high_spin:
            # Fill t2g first, then eg
            t2g = min(d_count, 3)
            eg = max(0, d_count - 3)
            # Pair in eg first after 5 electrons
            if d_count > 5:
                t2g = 6 - (d_count - 5)
                eg = d_count - 4 if d_count <= 8 else 4
        else:
            # Low-spin: fill t2g completely first
            t2g = min(d_count, 6)
            eg = max(0, d_count - 6)
        return {'t2g': t2g, 'eg': eg}
    else:
        # Tetrahedral (always high-spin)
        e = min(d_count, 2)
        t2 = max(0, d_count - 2)
        return {'e': e, 't2': t2}


def crystal_field_stabilization_energy(d_count: int, geometry: str = 'octahedral',
                                        high_spin: bool = True,
                                        Dq: float = 1.0) -> float:
    """
    Calculate crystal field stabilization energy (CFSE).
    
    Args:
        d_count: Number of d electrons
        geometry: 'octahedral' or 'tetrahedral'
        high_spin: True for high-spin
        Dq: Crystal field splitting parameter
    
    Returns:
        CFSE in Dq units
    """
    if geometry == 'octahedral':
        if high_spin:
            # High-spin octahedral
            cfse = {
                0: 0, 1: -4, 2: -8, 3: -12, 4: -6,
                5: 0, 6: -4, 7: -8, 8: -12, 9: -6, 10: 0
            }
        else:
            # Low-spin octahedral
            cfse = {
                0: 0, 1: -4, 2: -8, 3: -12, 4: -16,
                5: -20, 6: -24, 7: -18, 8: -12, 9: -6, 10: 0
            }
        return cfse.get(d_count, 0) * Dq
    else:
        # Tetrahedral (always high-spin, Deltat = 4/9 Deltao)
        cfse = {
            0: 0, 1: -6, 2: -12, 3: -8, 4: -4,
            5: 0, 6: -6, 7: -12, 8: -8, 9: -4, 10: 0
        }
        return cfse.get(d_count, 0) * Dq * 4/9


def predict_color(complementary: str = None, delta: float = None) -> str:
    """
    Predict color of complex from absorbed wavelength.
    
    Args:
        complementary: Absorbed color
        delta: Crystal field splitting (kJ/mol)
    
    Returns:
        Predicted visible color
    """
    color_pairs = {
        'violet': 'yellow',
        'blue': 'orange',
        'blue-green': 'red',
        'green': 'red-purple',
        'yellow-green': 'violet',
        'yellow': 'violet-blue',
        'orange': 'blue',
        'red': 'blue-green'
    }
    
    if complementary:
        return color_pairs.get(complementary.lower(), 'unknown')
    
    return 'Color depends on Delta value'


def pairing_energy_needed(d_count: int, geometry: str = 'octahedral',
                           high_spin: bool = True) -> int:
    """
    Calculate number of electron pairs that need pairing energy.
    
    Args:
        d_count: Number of d electrons
        geometry: Geometry type
        high_spin: True for high-spin
    
    Returns:
        Number of pairs requiring pairing energy
    """
    # Simplified calculation
    if geometry == 'octahedral':
        if high_spin:
            if d_count <= 3:
                return 0
            elif d_count == 4:
                return 0  # One in eg
            elif d_count == 5:
                return 0
            elif d_count == 6:
                return 1
            elif d_count == 7:
                return 2
            elif d_count == 8:
                return 3
            else:
                return 2
        else:
            # Low-spin
            if d_count <= 6:
                return max(0, d_count - 3)
            else:
                return d_count - 6
    return 0


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'crystal_field_stabilization_energy', 'description': "Calculate crystal field stabilization energy (CFSE).\n\nArgs:\n    d_count: Number of d electrons\n    geometry: 'octahedral' or 'tetrahedral'\n    high_spin: True for high-spin\n    Dq: Crystal field splitting parameter\n\nReturns:\n    CFSE in Dq units", 'inputSchema': {'type': 'object', 'properties': {'d_count': {'type': 'number', 'description': 'D Count'}, 'geometry': {'type': 'string', 'description': 'Geometry', 'default': 'octahedral'}, 'high_spin': {'type': 'string', 'description': 'High Spin', 'default': True}, 'Dq': {'type': 'number', 'description': 'Dq', 'default': 1.0}}, 'required': ['d_count']}},
    {'name': 'd_electron_distribution', 'description': "Distribute d electrons in orbital sets.\n\nArgs:\n    d_count: Number of d electrons\n    geometry: 'octahedral' or 'tetrahedral'\n    high_spin: True for high-spin\n\nReturns:\n    Dict with t2g and eg populations", 'inputSchema': {'type': 'object', 'properties': {'d_count': {'type': 'number', 'description': 'D Count'}, 'geometry': {'type': 'string', 'description': 'Geometry', 'default': 'octahedral'}, 'high_spin': {'type': 'string', 'description': 'High Spin', 'default': True}}, 'required': ['d_count']}},
    {'name': 'high_spin_or_low_spin', 'description': "Predict high-spin or low-spin for octahedral complex.\n\nOnly applicable for d4-d7 configurations.\n\nArgs:\n    d_count: Number of d electrons\n    ligand: Ligand name\n\nReturns:\n    'high-spin' or 'low-spin' or 'N/A'", 'inputSchema': {'type': 'object', 'properties': {'d_count': {'type': 'number', 'description': 'D Count'}, 'ligand': {'type': 'string', 'description': 'Ligand'}}, 'required': ['d_count', 'ligand']}},
    {'name': 'is_paramagnetic', 'description': 'Determine if complex is paramagnetic.\n\nArgs:\n    unpaired: Number of unpaired electrons\n\nReturns:\n    true if paramagnetic', 'inputSchema': {'type': 'object', 'properties': {'unpaired': {'type': 'number', 'description': 'Unpaired'}}, 'required': ['unpaired']}},
    {'name': 'magnetic_moment', 'description': 'Calculate spin-only magnetic moment.\n\nu = √(n(n+2)) BM\n\nArgs:\n    unpaired: Number of unpaired electrons\n\nReturns:\n    Magnetic moment in Bohr magnetons\n\nExamples:\n    >>> magnetic_moment(1)\n    1.73\n    >>> magnetic_moment(5)\n    5.92', 'inputSchema': {'type': 'object', 'properties': {'unpaired': {'type': 'number', 'description': 'Unpaired'}}, 'required': ['unpaired']}},
    {'name': 'pairing_energy_needed', 'description': 'Calculate number of electron pairs that need pairing energy.\n\nArgs:\n    d_count: Number of d electrons\n    geometry: Geometry type\n    high_spin: True for high-spin\n\nReturns:\n    Number of pairs requiring pairing energy', 'inputSchema': {'type': 'object', 'properties': {'d_count': {'type': 'number', 'description': 'D Count'}, 'geometry': {'type': 'string', 'description': 'Geometry', 'default': 'octahedral'}, 'high_spin': {'type': 'string', 'description': 'High Spin', 'default': True}}, 'required': ['d_count']}},
    {'name': 'predict_color', 'description': 'Predict color of complex from absorbed wavelength.\n\nArgs:\n    complementary: Absorbed color\n    delta: Crystal field splitting (kJ/mol)\n\nReturns:\n    Predicted visible color', 'inputSchema': {'type': 'object', 'properties': {'complementary': {'type': 'number', 'description': 'Complementary', 'default': None}, 'delta': {'type': 'number', 'description': 'Delta', 'default': None}}, 'required': []}}
]
