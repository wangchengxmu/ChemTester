"""
Conformational Analysis Tools - L3 Implementation
[Source: Organic Chemistry OpenStax, Ch03-04]

Functions for analyzing molecular conformations and strain energies.

## Solver Instructions (for AI Agent)

When you encounter conformational analysis, ring strain, cyclohexane chair/boat, A-values, or equilibrium distribution problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a molecule -> need rotational barrier or energy profile?
- Given substituents on cyclohexane -> need preferred conformation?
- Given ring size -> need strain energy or explanation?
- Given dihedral angle -> need butane conformation energy?
- Given two conformers with energy difference -> need equilibrium distribution?

### Step 2: Choose the correct function
- **Ethane barrier:** `calculate_ethane_barrier()` -> 12.0 kJ/mol (3 H-H eclipsing interactions)
- **Butane energy at angle:** `calculate_butane_energy(dihedral_angle)` -> relative energy in kJ/mol. Key values: 0deg=19.0, 60deg=3.8, 180deg=0.0, 300deg=3.8
- **A-value lookup:** `get_a_value(substituent)` -> kJ/mol. Key: CH3=7.3, C(CH3)3=23.0, OH=4.0, tBu=23.0
- **Monosubstituted cyclohexane:** `predict_cyclohexane_conformation(substituent)` -> preference level (equatorial preferred for A-value > 1)
- **Disubstituted cyclohexane energy:** `calculate_disubstituted_cyclohexane_energy(positions, stereochemistry, substituents)` -> total strain kJ/mol. Pass (1,2)/(1,3)/(1,4) and 'cis'/'trans'
- **Ring strain:** `get_ring_strain(ring_size)` -> kJ/mol by default; pass unit="kcal/mol" for kcal/mol (3->27.5, 4->26.3, 5->6.2, 6->0, 7->6.2, 8->9.6)
- **Ring strain explanation:** `explain_ring_strain(ring_size)` -> text explanation
- **1,3-Diaxial interactions:** `calculate_1_3_diaxial_interactions(substituent)` -> total strain (2x per-interaction value)
- **Energy profile:** `conformation_energy_profile(molecule)` -> dict of all conformation energies for 'ethane' or 'butane'
- **Ring flip:** `ring_flip_positions()` -> description of axial↔equatorial conversion
- **Equilibrium distribution:** `calculate_equilibrium_distribution(energy_difference, temperature)` -> Boltzmann distribution fractions

### Step 3: Handle special cases
- A-value = 1,3-diaxial strain x 2 (two gauche interactions)
- trans-1,2 and trans-1,4 can place both substituents equatorial -> 0 strain
- cis-1,3 can place both equatorial -> 0 strain
- For cis-1,2: one must be axial -> use min(A1, A2) as strain

### Examples
```python
# Example 1: Preferred position of tert-butyl on cyclohexane
predict_cyclohexane_conformation('C(CH3)3')  -> 'equatorial (very strongly preferred)' (A=23.0)

# Example 2: Butane energy at gauche (60deg)
calculate_butane_energy(60)  -> 3.8 kJ/mol

# Example 3: Ring strain of cyclopropane
get_ring_strain(3)  -> 115.0 kJ/mol (60deg vs 109.5deg ideal)

# Example 4: Equilibrium distribution for CH3 (A=7.3 kJ/mol at 298K)
calculate_equilibrium_distribution(7.3)  -> (0.947, 0.053) -> ~95% equatorial
```
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math


class ConformationType(Enum):
    """Types of molecular conformations"""
    STAGGERED = "staggered"
    ECLIPSED = "eclipsed"
    GAUCHE = "gauche"
    ANTI = "anti"
    CHAIR = "chair"
    BOAT = "boat"
    TWIST_BOAT = "twist_boat"


@dataclass
class ConformationEnergy:
    """Energy information for a conformation"""
    name: str
    energy_kj_mol: float
    stability: str


# Torsional strain (eclipsing interactions) in kJ/mol
TORSIONAL_STRAINS = {
    "H-H": 4.0,
    "H-CH3": 6.0,
    "CH3-CH3": 11.0,
    "H-CH2CH3": 7.0,
    "CH3-CH2CH3": 13.0,
}

# Butane conformation energies (relative to anti)
BUTANE_CONFORMATIONS = {
    "anti": ConformationEnergy("anti", 0.0, "most stable"),
    "gauche_plus": ConformationEnergy("gauche (+60deg)", 3.8, "stable"),
    "gauche_minus": ConformationEnergy("gauche (-60deg)", 3.8, "stable"),
    "eclipsed_CH3_H": ConformationEnergy("eclipsed (CH3-H)", 14.0, "unstable"),
    "eclipsed_CH3_CH3": ConformationEnergy("eclipsed (CH3-CH3)", 19.0, "most unstable"),
}

# A-values for cyclohexane substituents (kJ/mol)
A_VALUES = {
    "H": 0.0,
    "CH3": 7.3,
    "CH2CH3": 7.5,
    "C2H5": 7.5,
    "CH(CH3)2": 9.0,
    "i-Pr": 9.0,
    "C(CH3)3": 23.0,
    "t-Bu": 23.0,
    "tBu": 23.0,
    "OH": 4.0,
    "OCH3": 2.1,
    "F": 0.5,
    "Cl": 2.0,
    "Br": 2.4,
    "I": 2.6,
    "CN": 0.7,
    "COOH": 3.5,
    "CH2OH": 4.0,
    "CH2CN": 3.0,
    "NH2": 5.0,
    "NHCHO": 7.0,
    "NO2": 4.5,
    "Ph": 11.5,
    "C≡CH": 1.7,
    "C=C": 8.0,
    "CHO": 2.1,
    "COCH3": 3.0,
    "SH": 3.7,
    "SCH3": 4.0,
    "SiH3": 5.7,
    "GeH3": 6.5,
    "SnH3": 7.0,
    "alkyne": 1.7,
    "alkene": 8.0,
    "vinyl": 8.0,
    "phenyl": 11.5,
    "tert-butyl": 23.0,
    "isopropyl": 9.0,
    "ethyl": 7.5,
    "methyl": 7.3,
    "amino": 5.0,
    "hydroxyl": 4.0,
    "formyl": 2.1,
    "acetyl": 3.0,
    "carboxyl": 3.5,
    "nitro": 4.5,
    "cyano": 0.7,
    "fluoro": 0.5,
    "chloro": 2.0,
    "bromo": 2.4,
    "iodo": 2.6,
    "methoxy": 2.1,
    "methylamino": 7.0,
}

# Ring strain energies (kJ/mol)
RING_STRAINS = {
    3: 115.0,   # cyclopropane
    4: 110.0,   # cyclobutane
    5: 26.0,    # cyclopentane
    6: 0.0,     # cyclohexane
    7: 26.0,    # cycloheptane
    8: 40.0,    # cyclooctane
}

# 1,3-diaxial interactions (kJ/mol per interaction)
DIAAXIAL_STRAINS = {
    "H": 0.0,
    "CH3": 3.65,
    "CH2CH3": 3.75,
    "OH": 2.0,
    "Cl": 1.0,
    "Br": 1.2,
    "C(CH3)3": 11.5,
    "t-Bu": 11.5,
    "Ph": 5.75,
}


def calculate_ethane_barrier() -> float:
    """
    Calculate the rotational barrier for ethane.
    
    Ethane: 3 eclipsing H-H interactions
    
    Returns:
        Barrier height in kJ/mol
    
    Examples:
        >>> calculate_ethane_barrier()
        12.0
    """
    return 3 * TORSIONAL_STRAINS["H-H"]


def calculate_butane_energy(dihedral_angle: float) -> float:
    """
    Calculate the energy of a butane conformation.
    
    Args:
        dihedral_angle: Dihedral angle in degrees (0-360)
    
    Returns:
        Relative energy in kJ/mol
    
    Examples:
        >>> calculate_butane_energy(180)  # anti
        0.0
        >>> calculate_butane_energy(60)  # gauche
        3.8
    """
    # Simplified cosine model
    angle = dihedral_angle % 360
    
    if angle < 30 or angle > 330:
        return 19.0  # eclipsed CH3-CH3
    elif 30 <= angle < 90:
        return 3.8 + 10.2 * math.cos(math.radians(2 * (angle - 60)))
    elif 90 <= angle < 150:
        return 14.0 - 10.2 * math.cos(math.radians(2 * (angle - 120)))
    elif 150 <= angle < 210:
        return 3.8 - 3.8 * math.cos(math.radians(2 * (angle - 180)))
    elif 210 <= angle < 270:
        return 14.0 - 10.2 * math.cos(math.radians(2 * (angle - 240)))
    else:  # 270-330
        return 3.8 + 10.2 * math.cos(math.radians(2 * (angle - 300)))


def get_a_value(substituent: str) -> float:
    """
    Get the A-value for a cyclohexane substituent.
    
    A-value = Energy difference between axial and equatorial positions.
    
    Args:
        substituent: Name of substituent
    
    Returns:
        A-value in kJ/mol
    
    Examples:
        >>> get_a_value("CH3")
        7.3
        >>> get_a_value("C(CH3)3")
        23.0
    """
    return A_VALUES.get(substituent, 0.0)


def predict_cyclohexane_conformation(substituent: str) -> str:
    """
    Predict the preferred conformation of monosubstituted cyclohexane.
    
    Args:
        substituent: Name of substituent
    
    Returns:
        Preferred position
    
    Examples:
        >>> predict_cyclohexane_conformation("CH3")
        'equatorial (strongly preferred)'
    """
    a_value = get_a_value(substituent)
    
    if a_value >= 15:
        return "equatorial (very strongly preferred)"
    elif a_value >= 7:
        return "equatorial (strongly preferred)"
    elif a_value >= 3:
        return "equatorial (moderately preferred)"
    elif a_value >= 1:
        return "equatorial (slightly preferred)"
    else:
        return "no significant preference"


def calculate_disubstituted_cyclohexane_energy(
    positions: Tuple[int, int],
    stereochemistry: str,
    substituents: Tuple[str, str]
) -> float:
    """
    Calculate the energy of a disubstituted cyclohexane.
    
    Args:
        positions: Tuple of positions (e.g., (1, 2) for 1,2-disubstituted)
        stereochemistry: "cis" or "trans"
        substituents: Tuple of substituent names
    
    Returns:
        Total strain energy in kJ/mol
    
    Examples:
        >>> calculate_disubstituted_cyclohexane_energy((1, 2), "trans", ("CH3", "CH3"))
        14.6  # Both equatorial
    """
    sub1, sub2 = substituents
    a1 = get_a_value(sub1)
    a2 = get_a_value(sub2)
    
    # Simplified model
    if stereochemistry == "trans":
        # Can have both equatorial (most stable)
        if positions == (1, 2) or positions == (1, 4):
            return 0  # Both can be equatorial
        elif positions == (1, 3):
            return min(a1, a2)  # One must be axial
    else:  # cis
        if positions == (1, 3):
            return 0  # Both can be equatorial
        else:
            return min(a1, a2)  # One must be axial
    
    return 0


def get_ring_strain(ring_size: int, unit: str = "kJ/mol") -> float:
    """
    Get the ring strain energy for a cycloalkane.
    
    Args:
        ring_size: Number of carbons in ring
        unit: "kJ/mol" (default) or "kcal/mol"
    
    Returns:
        Ring strain in the requested unit
    
    Examples:
        >>> get_ring_strain(3)
        115.0
        >>> get_ring_strain(3, "kcal/mol")
        27.5
        >>> get_ring_strain(6)
        0.0
    """
    ring_size = int(ring_size)
    strain_kj = RING_STRAINS.get(ring_size, 0.0)
    if unit == "kcal/mol":
        return round(strain_kj / 4.184, 1)
    return strain_kj


def explain_ring_strain(ring_size: int) -> str:
    """
    Explain the source of ring strain for a cycloalkane.
    
    Args:
        ring_size: Number of carbons in ring
    
    Returns:
        Explanation of strain sources
    """
    if ring_size == 3:
        return "Severe angle strain (60deg vs ideal 109.5deg) + torsional strain"
    elif ring_size == 4:
        return "Angle strain (90deg) + torsional strain (puckered)"
    elif ring_size == 5:
        return "Minimal angle strain, mainly torsional (envelope/twist)"
    elif ring_size == 6:
        return "No strain (chair conformation, ideal angles, staggered)"
    elif ring_size == 7:
        return "Slight torsional strain + transannular strain"
    elif ring_size == 8:
        return "Torsional strain + transannular strain"
    else:
        return "Variable strain depending on conformation"


def calculate_1_3_diaxial_interactions(substituent: str) -> float:
    """
    Calculate the 1,3-diaxial strain for a substituent in axial position.
    
    Each axial substituent has two 1,3-diaxial interactions.
    
    Args:
        substituent: Name of substituent
    
    Returns:
        Total 1,3-diaxial strain in kJ/mol
    
    Examples:
        >>> calculate_1_3_diaxial_interactions("CH3")
        7.6  # 2 x 3.8
    """
    strain_per_interaction = DIAAXIAL_STRAINS.get(substituent, 0.0)
    return 2 * strain_per_interaction


def conformation_energy_profile(molecule: str) -> Dict[str, float]:
    """
    Get energy profile for conformations of a simple molecule.
    
    Args:
        molecule: "ethane" or "butane"
    
    Returns:
        Dictionary of conformation energies
    """
    profiles = {
        "ethane": {
            "staggered": 0.0,
            "eclipsed": 12.0,
        },
        "butane": {
            "anti": 0.0,
            "gauche": 3.8,
            "eclipsed_CH3_H": 14.0,
            "eclipsed_CH3_CH3": 19.0,
        },
    }
    
    return profiles.get(molecule.lower(), {})


def ring_flip_positions() -> Dict[str, str]:
    """
    Describe the ring flip process in cyclohexane.
    
    Returns:
        Dictionary describing the ring flip
    """
    return {
        "before": "Axial positions point up/down",
        "after": "All axial become equatorial, all equatorial become axial",
        "energy_barrier": "45 kJ/mol",
        "rate": "~105 flips/second at room temperature",
        "consequence": "Rapid interconversion of conformers",
    }


def calculate_equilibrium_distribution(energy_difference: float, 
                                       temperature: float = 298.0) -> Tuple[float, float]:
    """
    Calculate the equilibrium distribution between two conformers.
    
    Uses Boltzmann distribution.
    
    Args:
        energy_difference: Energy difference in kJ/mol (E2 - E1)
        temperature: Temperature in Kelvin
    
    Returns:
        Tuple of (fraction_conformer1, fraction_conformer2)
    
    Examples:
        >>> calculate_equilibrium_distribution(7.3)  # CH3 A-value
        (0.947, 0.053)  # ~95% equatorial
    """
    R = 8.314e-3  # Gas constant in kJ/(mol·K)
    delta_G = energy_difference
    
    # K = exp(-DeltaG/RT)
    K = math.exp(-delta_G / (R * temperature))
    
    # Fraction of conformer 2 (higher energy)
    frac2 = 1 / (1 + K)
    frac1 = K / (1 + K)
    
    return (frac1, frac2)


# Test functions
def test_ethane_barrier():
    """Test ethane rotational barrier calculation"""
    barrier = calculate_ethane_barrier()
    assert barrier == 12.0
    print("✓ Ethane barrier tests passed")


def test_a_values():
    """Test A-value lookup"""
    assert get_a_value("CH3") == 7.3
    assert get_a_value("C(CH3)3") == 23.0
    assert get_a_value("OH") == 4.0
    print("✓ A-value tests passed")


def test_ring_strain():
    """Test ring strain calculation"""
    assert get_ring_strain(3) == 115.0
    assert get_ring_strain(6) == 0.0
    print("✓ Ring strain tests passed")


def test_conformation_prediction():
    """Test conformation prediction"""
    assert "equatorial" in predict_cyclohexane_conformation("CH3")
    print("✓ Conformation prediction tests passed")


def test_equilibrium():
    """Test equilibrium distribution calculation"""
    f1, f2 = calculate_equilibrium_distribution(7.3)
    assert f1 > f2  # Lower energy conformer favored
    print("✓ Equilibrium distribution tests passed")


if __name__ == "__main__":
    test_ethane_barrier()
    test_a_values()
    test_ring_strain()
    test_conformation_prediction()
    test_equilibrium()
    print("\n✓ All conformational analysis tools tests passed!")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'calculate_1_3_diaxial_interactions', 'description': 'Calculate the 1,3-diaxial strain for a substituent in axial position.\n\nEach axial substituent has two 1,3-diaxial interactions.\n\nArgs:\n    substituent: Name of substituent\n\nReturns:\n    Total 1,3-diaxial strain in kJ/mol\n\nExamples:\n    >>> calculate_1_3_diaxial_interactions("CH3")\n    7.6  # 2 x 3.8', 'inputSchema': {'type': 'object', 'properties': {'substituent': {'type': 'number', 'description': 'Substituent'}}, 'required': ['substituent']}},
    {'name': 'calculate_butane_energy', 'description': 'Calculate the energy of a butane conformation.\n\nArgs:\n    dihedral_angle: Dihedral angle in degrees (0-360)\n\nReturns:\n    Relative energy in kJ/mol\n\nExamples:\n    >>> calculate_butane_energy(180)  # anti\n    0.0\n    >>> calculate_butane_energy(60)  # gauche\n    3.8', 'inputSchema': {'type': 'object', 'properties': {'dihedral_angle': {'type': 'number', 'description': 'Dihedral Angle'}}, 'required': ['dihedral_angle']}},
    {'name': 'calculate_disubstituted_cyclohexane_energy', 'description': 'Calculate the energy of a disubstituted cyclohexane.\n\nArgs:\n    positions: Tuple of positions (e.g., (1, 2) for 1,2-disubstituted)\n    stereochemistry: "cis" or "trans"\n    substituents: Tuple of substituent names\n\nReturns:\n    Total strain energy in kJ/mol\n\nExamples:\n    >>> calculate_disubstituted_cyclohexane_energy((1, 2), "trans", ("CH3", "CH3"))\n    14.6  # Both equatorial', 'inputSchema': {'type': 'object', 'properties': {'positions': {'type': 'string', 'description': 'Positions'}, 'stereochemistry': {'type': 'string', 'description': 'Stereochemistry'}, 'substituents': {'type': 'number', 'description': 'Substituents'}}, 'required': ['positions', 'stereochemistry', 'substituents']}},
    {'name': 'calculate_equilibrium_distribution', 'description': 'Calculate the equilibrium distribution between two conformers.\n\nUses Boltzmann distribution.\n\nArgs:\n    energy_difference: Energy difference in kJ/mol (E2 - E1)\n    temperature: Temperature in Kelvin\n\nReturns:\n    Tuple of (fraction_conformer1, fraction_conformer2)\n\nExamples:\n    >>> calculate_equilibrium_distribution(7.3)  # CH3 A-value\n    (0.947, 0.053)  # ~95% equatorial', 'inputSchema': {'type': 'object', 'properties': {'energy_difference': {'type': 'number', 'description': 'Energy Difference'}, 'temperature': {'type': 'number', 'description': 'Temperature', 'default': 298.0}}, 'required': ['energy_difference']}},
    {'name': 'calculate_ethane_barrier', 'description': 'Calculate the rotational barrier for ethane.\n\nEthane: 3 eclipsing H-H interactions\n\nReturns:\n    Barrier height in kJ/mol\n\nExamples:\n    >>> calculate_ethane_barrier()\n    12.0', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'conformation_energy_profile', 'description': 'Get energy profile for conformations of a simple molecule.\n\nArgs:\n    molecule: "ethane" or "butane"\n\nReturns:\n    Dictionary of conformation energies', 'inputSchema': {'type': 'object', 'properties': {'molecule': {'type': 'string', 'description': 'Molecule'}}, 'required': ['molecule']}},
    {'name': 'explain_ring_strain', 'description': 'Explain the source of ring strain for a cycloalkane.\n\nArgs:\n    ring_size: Number of carbons in ring\n\nReturns:\n    Explanation of strain sources', 'inputSchema': {'type': 'object', 'properties': {'ring_size': {'type': 'string', 'description': 'Ring Size'}}, 'required': ['ring_size']}},
    {'name': 'get_a_value', 'description': 'Get the A-value for a cyclohexane substituent.\n\nA-value = Energy difference between axial and equatorial positions.\n\nArgs:\n    substituent: Name of substituent\n\nReturns:\n    A-value in kJ/mol\n\nExamples:\n    >>> get_a_value("CH3")\n    7.3\n    >>> get_a_value("C(CH3)3")\n    23.0', 'inputSchema': {'type': 'object', 'properties': {'substituent': {'type': 'number', 'description': 'Substituent'}}, 'required': ['substituent']}},
    {'name': 'get_ring_strain', 'description': 'Get the ring strain energy for a cycloalkane.\n\nArgs:\n    ring_size: Number of carbons in ring\n\nReturns:\n    Ring strain in kJ/mol\n\nExamples:\n    >>> get_ring_strain(3)\n    115.0\n    >>> get_ring_strain(6)\n    0.0', 'inputSchema': {'type': 'object', 'properties': {'ring_size': {'type': 'string', 'description': 'Ring Size'}}, 'required': ['ring_size']}},
    {'name': 'predict_cyclohexane_conformation', 'description': 'Predict the preferred conformation of monosubstituted cyclohexane.\n\nArgs:\n    substituent: Name of substituent\n\nReturns:\n    Preferred position\n\nExamples:\n    >>> predict_cyclohexane_conformation("CH3")\n    \'equatorial (strongly preferred)\'', 'inputSchema': {'type': 'object', 'properties': {'substituent': {'type': 'number', 'description': 'Substituent'}}, 'required': ['substituent']}},
    {'name': 'ring_flip_positions', 'description': 'Describe the ring flip process in cyclohexane.\n\nReturns:\n    Dictionary describing the ring flip', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_a_values', 'description': 'Test A-value lookup', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_conformation_prediction', 'description': 'Test conformation prediction', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_equilibrium', 'description': 'Test equilibrium distribution calculation', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_ethane_barrier', 'description': 'Test ethane rotational barrier calculation', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_ring_strain', 'description': 'Test ring strain calculation', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}}
]
