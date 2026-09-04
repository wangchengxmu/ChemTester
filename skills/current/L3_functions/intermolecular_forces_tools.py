"""
Intermolecular Forces Tools - L3 Implementation
Source: Averill, Ch11
## Solver Instructions (for AI Agent)

When you encounter intermolecular forces, boiling point trends, or H-bonding problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Classify dominant IMF? Use `classify_imf(molecule_type, has_h_bond_donor, has_h_bond_acceptor)`
- Compare IMF strength? Use `imf_strength_rank(force_type)` -> 1-5 (1=weakest)
- Predict boiling point order? Use `predict_boiling_point_order(substances_list)` -> sorted by IMF+mass
- Check H-bond capability? Use `h_bond_capable(elements)` -> (can_donate, can_accept)
- Estimate London dispersion strength? Use `estimate_london_strength(molecular_mass, surface_area_factor)`
- IMF energy range? Use `imf_energy_range(force_type)` -> (min, max) kJ/mol
- Polarizability trend? Use `polarizability_trend(elements)` -> qualitative description

### Step 2: Handle special cases
- **IMF hierarchy**: London dispersion < dipole-dipole < hydrogen bonding < ion-dipole < ion-ion
- **H-bonding**: Requires H bonded to N, O, or F AND lone pair on N, O, or F
- **Boiling point prediction**: Higher IMF rank -> higher bp; for same IMF, higher mass -> higher bp
- **Branching effect**: Branched isomers have lower bp than linear (less surface area -> weaker London)
- **Surface area factor**: >1 for linear/extended; <1 for branched/compact molecules

### Examples
```python
# Example 1: Classify IMF
classify_imf('polar', True, True)  # -> 'hydrogen_bonding' (e.g., ethanol)
classify_imf('nonpolar', False, False)  # -> 'london_dispersion' (e.g., CH4)

# Example 2: Boiling point order
predict_boiling_point_order([
    {'name': 'CH4', 'imf_type': 'london_dispersion', 'molecular_mass': 16},
    {'name': 'H2O', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 18},
    {'name': 'HCl', 'imf_type': 'dipole_dipole', 'molecular_mass': 36.5}
])  # -> ['CH4', 'HCl', 'H2O']
```
"""

from typing import Dict, List, Tuple, Optional


def _normalize_imf_name(force_type: str) -> str:
    """Normalize IMF type name: lowercase, replace spaces/hyphens with underscores."""
    if not isinstance(force_type, str):
        force_type = str(force_type)
    return force_type.lower().strip().replace(" ", "_").replace("-", "_")


def classify_imf(molecule_type: str, has_h_bond_donor: bool = False, 
                 has_h_bond_acceptor: bool = False) -> str:
    """
    Classify dominant intermolecular force for a molecule.
    
    Args:
        molecule_type: 'polar' or 'nonpolar'
        has_h_bond_donor: Has H bonded to N, O, or F
        has_h_bond_acceptor: Has lone pair on N, O, or F
    
    Returns:
        Dominant IMF type
    
    Examples:
        >>> classify_imf('polar', True, True)
        'hydrogen_bonding'
        >>> classify_imf('nonpolar', False, False)
        'london_dispersion'
    """
    if has_h_bond_donor and has_h_bond_acceptor:
        return 'hydrogen_bonding'
    elif molecule_type == 'polar':
        return 'dipole_dipole'
    else:
        return 'london_dispersion'


def imf_strength_rank(force_type: str) -> int:
    """
    Return relative strength ranking for IMF type.
    
    Higher number = stronger force.
    
    Args:
        force_type: Type of IMF
    
    Returns:
        Strength ranking (1-5)
    """
    rankings = {
        'london_dispersion': 1,
        'dipole_dipole': 2,
        'hydrogen_bonding': 3,
        'ion_dipole': 4,
        'ion_ion': 5
    }
    return rankings.get(_normalize_imf_name(force_type), 0)


# Common compound properties for string-based lookups
_COMPOUND_DB = {
    'ch4': {'name': 'CH4', 'imf_type': 'london_dispersion', 'molecular_mass': 16.0, 'h_bond_count': 0},
    'methane': {'name': 'CH4', 'imf_type': 'london_dispersion', 'molecular_mass': 16.0, 'h_bond_count': 0},
    'c2h6': {'name': 'C2H6', 'imf_type': 'london_dispersion', 'molecular_mass': 30.1, 'h_bond_count': 0},
    'ethane': {'name': 'C2H6', 'imf_type': 'london_dispersion', 'molecular_mass': 30.1, 'h_bond_count': 0},
    'c3h8': {'name': 'C3H8', 'imf_type': 'london_dispersion', 'molecular_mass': 44.1, 'h_bond_count': 0},
    'propane': {'name': 'C3H8', 'imf_type': 'london_dispersion', 'molecular_mass': 44.1, 'h_bond_count': 0},
    'c4h10': {'name': 'C4H10', 'imf_type': 'london_dispersion', 'molecular_mass': 58.1, 'h_bond_count': 0},
    'butane': {'name': 'C4H10', 'imf_type': 'london_dispersion', 'molecular_mass': 58.1, 'h_bond_count': 0},
    'c5h12': {'name': 'C5H12', 'imf_type': 'london_dispersion', 'molecular_mass': 72.1, 'h_bond_count': 0},
    'pentane': {'name': 'C5H12', 'imf_type': 'london_dispersion', 'molecular_mass': 72.1, 'h_bond_count': 0},
    'c6h14': {'name': 'C6H14', 'imf_type': 'london_dispersion', 'molecular_mass': 86.2, 'h_bond_count': 0},
    'hexane': {'name': 'C6H14', 'imf_type': 'london_dispersion', 'molecular_mass': 86.2, 'h_bond_count': 0},
    'c2h4': {'name': 'C2H4', 'imf_type': 'london_dispersion', 'molecular_mass': 28.1, 'h_bond_count': 0},
    'ethylene': {'name': 'C2H4', 'imf_type': 'london_dispersion', 'molecular_mass': 28.1, 'h_bond_count': 0},
    'h2o': {'name': 'H2O', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 18.0, 'h_bond_count': 4},
    'water': {'name': 'H2O', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 18.0, 'h_bond_count': 4},
    'nh3': {'name': 'NH3', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 17.0, 'h_bond_count': 3},
    'ammonia': {'name': 'NH3', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 17.0, 'h_bond_count': 3},
    'hf': {'name': 'HF', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 20.0, 'h_bond_count': 2},
    'ch3oh': {'name': 'CH3OH', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 32.0, 'h_bond_count': 3},
    'methanol': {'name': 'CH3OH', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 32.0, 'h_bond_count': 3},
    'c2h5oh': {'name': 'C2H5OH', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 46.1, 'h_bond_count': 3},
    'ethanol': {'name': 'C2H5OH', 'imf_type': 'hydrogen_bonding', 'molecular_mass': 46.1, 'h_bond_count': 3},
    'hcl': {'name': 'HCl', 'imf_type': 'dipole_dipole', 'molecular_mass': 36.5, 'h_bond_count': 0},
    'hbr': {'name': 'HBr', 'imf_type': 'dipole_dipole', 'molecular_mass': 81.0, 'h_bond_count': 0},
    'hi': {'name': 'HI', 'imf_type': 'dipole_dipole', 'molecular_mass': 127.9, 'h_bond_count': 0},
    'so2': {'name': 'SO2', 'imf_type': 'dipole_dipole', 'molecular_mass': 64.1, 'h_bond_count': 0},
    'co2': {'name': 'CO2', 'imf_type': 'london_dispersion', 'molecular_mass': 44.0, 'h_bond_count': 0},
    'n2': {'name': 'N2', 'imf_type': 'london_dispersion', 'molecular_mass': 28.0, 'h_bond_count': 0},
    'o2': {'name': 'O2', 'imf_type': 'london_dispersion', 'molecular_mass': 32.0, 'h_bond_count': 0},
    'cl2': {'name': 'Cl2', 'imf_type': 'london_dispersion', 'molecular_mass': 71.0, 'h_bond_count': 0},
    'br2': {'name': 'Br2', 'imf_type': 'london_dispersion', 'molecular_mass': 159.8, 'h_bond_count': 0},
    'he': {'name': 'He', 'imf_type': 'london_dispersion', 'molecular_mass': 4.0, 'h_bond_count': 0},
    'ne': {'name': 'Ne', 'imf_type': 'london_dispersion', 'molecular_mass': 20.2, 'h_bond_count': 0},
    'ar': {'name': 'Ar', 'imf_type': 'london_dispersion', 'molecular_mass': 39.9, 'h_bond_count': 0},
    'ch3cl': {'name': 'CH3Cl', 'imf_type': 'dipole_dipole', 'molecular_mass': 50.5, 'h_bond_count': 0},
    'ch2cl2': {'name': 'CH2Cl2', 'imf_type': 'dipole_dipole', 'molecular_mass': 84.9, 'h_bond_count': 0},
    'ch3och3': {'name': 'CH3OCH3', 'imf_type': 'dipole_dipole', 'molecular_mass': 46.1, 'h_bond_count': 0},
    'acetone': {'name': 'CH3COCH3', 'imf_type': 'dipole_dipole', 'molecular_mass': 58.1, 'h_bond_count': 0},
    'ch3coch3': {'name': 'CH3COCH3', 'imf_type': 'dipole_dipole', 'molecular_mass': 58.1, 'h_bond_count': 0},
    'c6h6': {'name': 'C6H6', 'imf_type': 'london_dispersion', 'molecular_mass': 78.1, 'h_bond_count': 0},
    'benzene': {'name': 'C6H6', 'imf_type': 'london_dispersion', 'molecular_mass': 78.1, 'h_bond_count': 0},
    'ccl4': {'name': 'CCl4', 'imf_type': 'london_dispersion', 'molecular_mass': 153.8, 'h_bond_count': 0},
    'cf4': {'name': 'CF4', 'imf_type': 'london_dispersion', 'molecular_mass': 88.0, 'h_bond_count': 0},
}


def predict_boiling_point_order(substances) -> List[str]:
    """
    Predict boiling point order from lowest to highest.
    
    Args:
        substances: List of dicts with keys:
            - name: substance name
            - imf_type: dominant IMF
            - molecular_mass: mass in g/mol
            - h_bond_count: number of H-bond sites (optional)
            OR list of compound name strings (looked up from built-in database)
    
    Returns:
        List of substance names in order of increasing bp
    """
    normalized = []
    for s in substances:
        if isinstance(s, str):
            entry = _COMPOUND_DB.get(s.lower().strip())
            if entry is None:
                raise ValueError(f"Unknown compound '{s}'. Available: {sorted(_COMPOUND_DB.keys())}")
            normalized.append(entry.copy())
        elif isinstance(s, dict):
            normalized.append(s)
        else:
            raise TypeError(f"Expected str or dict, got {type(s)}")
    
    def bp_key(substance):
        imf_type = substance.get('imf_type', 'london_dispersion')
        if not isinstance(imf_type, str):
            imf_type = str(imf_type)
        imf_rank = imf_strength_rank(imf_type)
        mass = substance.get('molecular_mass', 0)
        h_bonds = substance.get('h_bond_count', 0)
        return (imf_rank, mass, h_bonds)
    
    sorted_subs = sorted(normalized, key=bp_key)
    return [s['name'] for s in sorted_subs]


def h_bond_capable(elements: List[str]) -> Tuple[bool, bool]:
    """
    Check if molecule can donate and/or accept H-bonds.
    
    Args:
        elements: List of element symbols in molecule
    
    Returns:
        (can_donate, can_accept) tuple
    
    Examples:
        >>> h_bond_capable(['H', 'O'])
        (True, True)
        >>> h_bond_capable(['C', 'H'])
        (False, False)
    """
    h_bond_elements = {'N', 'O', 'F'}
    has_h = 'H' in elements
    has_nof = any(e in h_bond_elements for e in elements)
    
    can_donate = has_h and has_nof
    can_accept = has_nof
    
    return (can_donate, can_accept)


def estimate_london_strength(molecular_mass: float, surface_area_factor: float = 1.0) -> float:
    """
    Estimate relative London dispersion force strength.
    
    Args:
        molecular_mass: Molecular mass in g/mol
        surface_area_factor: 1.0 for normal, >1 for linear/extended, <1 for branched
    
    Returns:
        Relative strength estimate
    """
    return molecular_mass * surface_area_factor


def imf_energy_range(force_type: str) -> Tuple[float, float]:
    """
    Return typical energy range for IMF type in kJ/mol.
    
    Args:
        force_type: Type of IMF
    
    Returns:
        (min_energy, max_energy) in kJ/mol
    """
    ranges = {
        'london_dispersion': (0.1, 40),
        'dipole_dipole': (5, 20),
        'hydrogen_bonding': (15, 25),
        'ion_dipole': (40, 600),
        'ion_ion': (400, 4000)
    }
    return ranges.get(_normalize_imf_name(force_type), (0, 0))


def polarizability_trend(elements: List[str]) -> str:
    """
    Determine polarizability trend for given elements.
    
    Larger atoms with more electrons are more polarizable.
    
    Args:
        elements: List of element symbols
    
    Returns:
        Description of polarizability trend
    """
    # Period trend: increases down group
    # Group trend: increases with size
    atomic_sizes = {
        'H': 1, 'He': 1,
        'Li': 2, 'Be': 2, 'B': 2, 'C': 2, 'N': 2, 'O': 2, 'F': 2, 'Ne': 2,
        'Na': 3, 'Mg': 3, 'Al': 3, 'Si': 3, 'P': 3, 'S': 3, 'Cl': 3, 'Ar': 3,
        'K': 4, 'Ca': 4, 'Br': 4, 'Kr': 4,
        'I': 5, 'Xe': 5
    }
    
    if not elements:
        return "No elements provided"
    
    sizes = [atomic_sizes.get(e, 0) for e in elements]
    avg_size = sum(sizes) / len(sizes)
    
    if avg_size < 2:
        return "Low polarizability (small atoms)"
    elif avg_size < 3:
        return "Moderate polarizability"
    elif avg_size < 4:
        return "High polarizability (large atoms)"
    else:
        return "Very high polarizability (very large atoms)"

MCP_TOOLS = [
    {
        "name": "classify_imf",
        "description": "Classify dominant intermolecular force for a molecule.",
        "parameters": [
            {
                "name": "molecule_type",
                "type": "number"
            },
            {
                "name": "has_h_bond_donor",
                "type": "boolean"
            },
            {
                "name": "has_h_bond_acceptor",
                "type": "boolean"
            }
        ]
    },
    {
        "name": "estimate_london_strength",
        "description": "Estimate relative London dispersion force strength.",
        "parameters": [
            {
                "name": "molecular_mass",
                "type": "number"
            },
            {
                "name": "surface_area_factor",
                "type": "number"
            }
        ]
    },
    {
        "name": "h_bond_capable",
        "description": "Check if molecule can donate and/or accept H-bonds.",
        "parameters": [
            {
                "name": "elements",
                "type": "string"
            }
        ]
    },
    {
        "name": "imf_energy_range",
        "description": "Return typical energy range for IMF type in kJ/mol.",
        "parameters": [
            {
                "name": "force_type",
                "type": "number"
            }
        ]
    },
    {
        "name": "imf_strength_rank",
        "description": "Return relative strength ranking for IMF type.",
        "parameters": [
            {
                "name": "force_type",
                "type": "number"
            }
        ]
    },
    {
        "name": "polarizability_trend",
        "description": "Determine polarizability trend for given elements.",
        "parameters": [
            {
                "name": "elements",
                "type": "string"
            }
        ]
    },
    {
        "name": "predict_boiling_point_order",
        "description": "Predict boiling point order from lowest to highest.",
        "parameters": [
            {
                "name": "substances",
                "type": "number"
            }
        ]
    }
]
