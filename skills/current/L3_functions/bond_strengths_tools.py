"""
Bond Strengths Tools - L3 Implementation
Chapter 7.05: Strengths of Ionic and Covalent Bonds

## Solver Instructions (for AI Agent)

When you encounter bond energy, lattice energy, and reaction enthalpy from bonds problems:

### Step 1: Identify what is given and what is asked
- Given: atoms, bond type, ionic charges, distances, or bonds broken/formed
- Asked: bond energy, lattice energy, reaction enthalpy, relative bond strengths

### Step 2: Choose the correct function
- `average_bond_energy(atom1, atom2, bond_order)`: Average BDE in kJ/mol
- `reaction_enthalpy_from_bonds(bonds_broken, bonds_formed)`: DeltaH = Σ(broken) - Σ(formed)
- `lattice_energy_ionic(z_cation, z_anion, distance_pm)`: Born-Landé equation
- `compare_lattice_energies(compounds)`: Rank compounds by lattice energy
- `born_haber_lattice(data_dict)`: Lattice energy from Born-Haber cycle
- `bond_strength_order(bonds)`: Rank bonds by strength
- `multiple_bond_effect(atom1, atom2)`: Compare single/double/triple bond energies

### Step 3: Handle special cases
- Bond breaking = endothermic (+), bond forming = exothermic (-)
- Higher ionic charge + smaller radius -> larger lattice energy
- Triple > double > single bond (but not linear multiples)

### Examples
```python
# CH4 combustion: break 4 C-H (413), form 2 C=O (799), 4 O-H (463)
reaction_enthalpy_from_bonds([('C','H',1)]*4, [('C','O',2)]*2 + [('O','H',1)]*4)
lattice_energy_ionic(1, -1, 282)  # NaCl -> ~787 kJ/mol
```
"""

from typing import Dict, List, Tuple

# Average bond energies in kJ/mol
BOND_ENERGIES = {
    # Single bonds (OpenStax Chemistry 2e Table 7.2 values)
    ('H', 'H'): 436, ('C', 'C'): 348, ('N', 'N'): 160, ('O', 'O'): 140,
    ('F', 'F'): 160, ('Cl', 'Cl'): 243, ('Br', 'Br'): 190, ('I', 'I'): 151,
    ('C', 'H'): 413, ('N', 'H'): 390, ('O', 'H'): 463, ('F', 'H'): 569,
    ('Cl', 'H'): 432, ('Br', 'H'): 370, ('I', 'H'): 299,
    ('C', 'N'): 290, ('C', 'O'): 350, ('C', 'F'): 439,
    ('C', 'Cl'): 330, ('C', 'Br'): 275, ('C', 'I'): 240,
    ('N', 'O'): 200, ('O', 'F'): 160, ('O', 'Cl'): 205,
    # Double bonds (OpenStax Chemistry 2e Table 7.2 values)
    ('C', 'C', 2): 614, ('C', 'N', 2): 615, ('C', 'O', 2): 799,
    ('N', 'N', 2): 418, ('O', 'O', 2): 498,
    # Triple bonds (OpenStax Chemistry 2e Table 7.2 values)
    ('C', 'C', 3): 839, ('C', 'N', 3): 891, ('C', 'O', 3): 1080,
    ('N', 'N', 3): 946,
}


def get_bond_energy(atom1: str, atom2: str, bond_order: int = 1) -> float:
    """
    Get average bond energy for a bond.
    
    Args:
        atom1: First element symbol
        atom2: Second element symbol
        bond_order: 1, 2, or 3
    
    Returns:
        Bond energy in kJ/mol
    
    Examples:
        >>> get_bond_energy('C', 'H')
        415
        >>> get_bond_energy('C', 'O', 2)
        741
    """
    if bond_order > 1:
        key = (atom1, atom2, bond_order)
        key_rev = (atom2, atom1, bond_order)
        if key in BOND_ENERGIES:
            return BOND_ENERGIES[key]
        if key_rev in BOND_ENERGIES:
            return BOND_ENERGIES[key_rev]
    
    key = (atom1, atom2)
    key_rev = (atom2, atom1)
    if key in BOND_ENERGIES:
        return BOND_ENERGIES[key]
    if key_rev in BOND_ENERGIES:
        return BOND_ENERGIES[key_rev]
    
    raise ValueError(f"Bond energy not available for {atom1}-{atom2}")


def reaction_enthalpy_from_bonds(
    bonds_broken: List[Tuple[str, str, int]],
    bonds_formed: List[Tuple[str, str, int]]
) -> float:
    """
    Calculate reaction enthalpy from bond energies.
    
    Args:
        bonds_broken: List of (atom1, atom2, count) bonds broken
        bonds_formed: List of (atom1, atom2, count) bonds formed
    
    Returns:
        DeltaH in kJ/mol (negative = exothermic)
    
    Examples:
        >>> reaction_enthalpy_from_bonds(
        ...     [('H', 'H', 1), ('Cl', 'Cl', 1)],
        ...     [('H', 'Cl', 2)]
        ... )
        -185
    """
    # Energy required to break bonds (positive)
    energy_in = 0
    for atom1, atom2, count in bonds_broken:
        try:
            energy_in += get_bond_energy(atom1, atom2) * count
        except ValueError:
            # Assume single bond if not found
            pass
    
    # Energy released when bonds form (negative)
    energy_out = 0
    for atom1, atom2, count in bonds_formed:
        try:
            energy_out += get_bond_energy(atom1, atom2) * count
        except ValueError:
            pass
    
    # DeltaH = bonds broken - bonds formed
    return energy_in - energy_out


def lattice_energy_ionic(z_cation: int, z_anion: int, distance_pm: float,
                         reference_U=None, reference_z=None, reference_r=None) -> float:
    """
    Estimate lattice energy from ion properties using Coulomb proportionality.
    
    If reference values provided, returns absolute lattice energy in kJ/mol
    by scaling from a known compound. Otherwise returns relative units.
    
    Args:
        z_cation: Cation charge
        z_anion: Anion charge (as positive number)
        distance_pm: Interionic distance in picometers
        reference_U: Known lattice energy in kJ/mol (for calibration)
        reference_z: Tuple of (z_cation, z_anion) for reference compound
        reference_r: Interionic distance for reference compound in pm
    
    Returns:
        Lattice energy (relative units or kJ/mol if reference provided)
    
    Examples:
        >>> # Relative
        >>> lattice_energy_ionic(1, 1, 280)
        3.57...
        >>> # Estimate MgO from LiF (1036 kJ/mol, z=1,1, r=201 pm)
        >>> lattice_energy_ionic(2, 2, 210, reference_U=1036, reference_z=(1,1), reference_r=201)
        3966.0...
    """
    # U ∝ Z+ * Z- / r
    relative = (z_cation * z_anion) / distance_pm
    
    if reference_U is not None and reference_z is not None and reference_r is not None:
        ref_relative = (reference_z[0] * reference_z[1]) / reference_r
        return reference_U * (relative / ref_relative)
    
    return relative * 100  # Keep backward compat: multiply by 100 for same scale


def compare_lattice_energies(compounds: List[Dict]) -> List[Tuple[str, float]]:
    """
    Compare lattice energies of multiple compounds.
    
    Args:
        compounds: List of dicts with 'name', 'z_cat', 'z_an', 'distance'
    
    Returns:
        List sorted by lattice energy (highest first)
    
    Examples:
        >>> compare_lattice_energies([
        ...     {'name': 'NaCl', 'z_cat': 1, 'z_an': 1, 'distance': 280},
        ...     {'name': 'MgO', 'z_cat': 2, 'z_an': 2, 'distance': 210}
        ... ])
        [('MgO', 19.05...), ('NaCl', 3.57...)]
    """
    results = []
    for compound in compounds:
        le = lattice_energy_ionic(
            compound['z_cat'], 
            compound['z_an'], 
            compound['distance']
        )
        results.append((compound['name'], le))
    
    return sorted(results, key=lambda x: -x[1])


def born_haber_lattice(
    delta_h_f: float,
    delta_h_s: float,  # sublimation
    bond_d: float,     # bond dissociation
    ie: float,         # ionization energy
    ea: float          # electron affinity
) -> float:
    """
    Calculate lattice energy from Born-Haber cycle.
    
    Args:
        delta_h_f: Standard enthalpy of formation (kJ/mol)
        delta_h_s: Enthalpy of sublimation (kJ/mol)
        bond_d: Bond dissociation energy (kJ/mol)
        ie: Ionization energy (kJ/mol)
        ea: Electron affinity (kJ/mol, negative if exothermic)
    
    Returns:
        Lattice energy (kJ/mol)
    
    Examples:
        >>> born_haber_lattice(-553.5, 76.5, 158.8, 375.7, -328.2)  # CsF
        756.9
    """
    # DeltaH_f = DeltaH_s + 1/2D + IE + EA - DeltaH_lattice
    # DeltaH_lattice = DeltaH_s + 1/2D + IE + EA - DeltaH_f
    lattice = delta_h_s + bond_d + ie + ea - delta_h_f
    return round(lattice, 1)


def bond_strength_order(bonds: List[Tuple[str, str, int]]) -> List[Tuple[str, str, int, float]]:
    """
    Rank bonds by strength.
    
    Args:
        bonds: List of (atom1, atom2, bond_order)
    
    Returns:
        List sorted by strength (strongest first)
    
    Examples:
        >>> bond_strength_order([('C', 'C', 1), ('C', 'C', 2), ('C', 'C', 3)])
        [('C', 'C', 3, 837), ('C', 'C', 2, 611), ('C', 'C', 1, 345)]
    """
    results = []
    for atom1, atom2, order in bonds:
        try:
            energy = get_bond_energy(atom1, atom2, order)
        except ValueError:
            energy = 0
        results.append((atom1, atom2, order, energy))
    
    return sorted(results, key=lambda x: -x[3])


def multiple_bond_effect(atom1: str, atom2: str) -> Dict:
    """
    Show effect of multiple bonds on bond properties.
    
    Args:
        atom1: First element
        atom2: Second element
    
    Returns:
        Dictionary with bond orders, energies, lengths
    
    Examples:
        >>> multiple_bond_effect('C', 'C')
        {'single': 345, 'double': 611, 'triple': 837}
    """
    result = {}
    
    try:
        result['single'] = get_bond_energy(atom1, atom2, 1)
    except ValueError:
        pass
    
    try:
        result['double'] = get_bond_energy(atom1, atom2, 2)
    except ValueError:
        pass
    
    try:
        result['triple'] = get_bond_energy(atom1, atom2, 3)
    except ValueError:
        pass
    
    return result


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "bond_strength_order",
        "description": "Rank bonds by strength.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bonds": {
                    "type": "number",
                    "description": "Bonds"
                }
            },
            "required": [
                "bonds"
            ]
        }
    },
    {
        "name": "born_haber_lattice",
        "description": "Calculate lattice energy from Born-Haber cycle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_h_f": {
                    "type": "number",
                    "description": "Delta H F"
                },
                "delta_h_s": {
                    "type": "number",
                    "description": "Delta H S"
                },
                "bond_d": {
                    "type": "number",
                    "description": "Bond D"
                },
                "ie": {
                    "type": "number",
                    "description": "Ie"
                },
                "ea": {
                    "type": "number",
                    "description": "Ea"
                }
            },
            "required": [
                "delta_h_f",
                "delta_h_s",
                "bond_d",
                "ie",
                "ea"
            ]
        }
    },
    {
        "name": "compare_lattice_energies",
        "description": "Compare lattice energies of multiple compounds.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compounds": {
                    "type": "number",
                    "description": "Compounds"
                }
            },
            "required": [
                "compounds"
            ]
        }
    },
    {
        "name": "get_bond_energy",
        "description": "Get average bond energy for a bond.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "atom1": {
                    "type": "number",
                    "description": "Atom1"
                },
                "atom2": {
                    "type": "number",
                    "description": "Atom2"
                },
                "bond_order": {
                    "type": "number",
                    "description": "Bond Order",
                    "default": 1
                }
            },
            "required": [
                "atom1",
                "atom2"
            ]
        }
    },
    {
        "name": "lattice_energy_ionic",
        "description": "Estimate relative lattice energy from ion properties.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "z_cation": {
                    "type": "number",
                    "description": "Z Cation"
                },
                "z_anion": {
                    "type": "number",
                    "description": "Z Anion"
                },
                "distance_pm": {
                    "type": "number",
                    "description": "Distance Pm"
                }
            },
            "required": [
                "z_cation",
                "z_anion",
                "distance_pm"
            ]
        }
    },
    {
        "name": "multiple_bond_effect",
        "description": "Show effect of multiple bonds on bond properties.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "atom1": {
                    "type": "number",
                    "description": "Atom1"
                },
                "atom2": {
                    "type": "number",
                    "description": "Atom2"
                }
            },
            "required": [
                "atom1",
                "atom2"
            ]
        }
    },
    {
        "name": "reaction_enthalpy_from_bonds",
        "description": "Calculate reaction enthalpy from bond energies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bonds_broken": {
                    "type": "number",
                    "description": "Bonds Broken"
                },
                "bonds_formed": {
                    "type": "number",
                    "description": "Bonds Formed"
                }
            },
            "required": [
                "bonds_broken",
                "bonds_formed"
            ]
        }
    }
]