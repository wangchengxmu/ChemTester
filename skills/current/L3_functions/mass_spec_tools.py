"""
L3 Tool: Mass Spectrometry Tools
Calculate molecular weights, exact masses, and fragmentation patterns.

Source: Organic Chemistry (OpenStax) Ch12
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter molecular weight calculation, exact mass, M+1/M+2 isotope peaks, fragmentation analysis, or nominal mass problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given molecular formula -> calculate MW, exact mass, or nominal mass?
- Given formula with C/H/N atoms -> calculate expected M+1 peak intensity?
- Given formula with Cl/Br/S -> calculate M+2 peak intensity?
- Given molecular ion and fragment m/z -> identify lost fragment?
- Given a lost mass -> identify what fragment was lost?

### Step 2: Choose the correct function
- **Molecular weight (average):** `molecular_weight(formula)` -> g/mol using average atomic masses. Formula: {'C': 6, 'H': 12, 'O': 6}
- **Exact mass:** `exact_mass(formula)` -> amu using most abundant isotope masses
- **Nominal mass:** `nominal_mass(formula)` -> integer mass of most abundant isotopes
- **M+1 intensity:** `m_plus_one_intensity(carbons, hydrogens, nitrogens)` -> %. 13C contributes 1.10% per carbon (dominant)
- **M+2 intensity:** `m_plus_two_intensity(carbons, oxygens, sulfurs, chlorines, bromines)` -> %. Cl: 24.23%/atom, Br: 49.31%/atom (characteristic doublet pattern)
- **Fragment mass:** `fragment_mass(molecular_ion, lost_mass)` -> m/z = M+ - lost
- **Identify fragment loss:** `identify_fragment_loss(molecular_ion, fragment_mz)` -> dict with lost mass and possible identity (e.g., 29->C2H5 or CHO, 18->H2O, 91->benzyl)

### Step 3: Handle special cases
- Cl and Br give CHARACTERISTIC M+2 patterns: Cl has 3:1 ratio, Br has 1:1 ratio
- M+1 intensity ~ 1.1 x number of carbons -> use to count carbons
- The molecular ion (M+) is always the highest m/z of significance (ignoring isotope peaks)
- Common losses: 15 (CH3), 17 (OH), 18 (H2O), 29 (C2H5), 43 (CH3CO), 91 (benzyl)

### Examples
```python
# Example 1: MW of glucose
molecular_weight({'C': 6, 'H': 12, 'O': 6})  -> 180.156 g/mol

# Example 2: M+1 intensity for benzene (C6H6)
m_plus_one_intensity(6, 6)  -> 6.69%

# Example 3: Identify fragment loss: M+ = 86, fragment at 57
identify_fragment_loss(86, 57)  -> {'lost_mass': 29, 'possible': 'C2H5 (ethyl) or CHO'}

# Example 4: M+2 intensity for chlorobenzene (1 Cl)
m_plus_two_intensity(chlorines=1)  -> 24.23%
```
"""

# Exact isotope masses (in amu)
EXACT_MASSES = {
    'C': 12.00000,      # 12C
    'H': 1.00783,       # 1H
    'O': 15.99491,      # 16O
    'N': 14.00307,      # 14N
    'S': 31.97207,      # 32S
    'Cl': 34.96885,     # 35Cl
    'Br': 78.91834,     # 79Br
    'F': 18.99840,      # 19F
    'P': 30.97376,      # 31P
    'I': 126.90447,     # 127I
}

# Average atomic masses
ATOMIC_MASSES = {
    'C': 12.011,
    'H': 1.008,
    'O': 15.999,
    'N': 14.007,
    'S': 32.065,
    'Cl': 35.453,
    'Br': 79.904,
    'F': 18.998,
    'P': 30.974,
    'I': 126.904,
}

# Natural abundances for isotope peaks
ISOTOPE_ABUNDANCES = {
    '13C': 1.10,    # %
    '2H': 0.015,    # %
    '15N': 0.366,   # %
    '17O': 0.038,   # %
    '18O': 0.205,   # %
    '37Cl': 24.23,  # %
    '81Br': 49.31,  # %
}


def molecular_weight(formula: dict) -> float:
    """
    Calculate molecular weight from formula.
    
    Args:
        formula: Dictionary like {'C': 6, 'H': 12, 'O': 6}
    
    Returns:
        Molecular weight in g/mol
    
    Example:
        >>> molecular_weight({'C': 6, 'H': 12, 'O': 6})
        180.156
    """
    total = 0.0
    for element, count in formula.items():
        if element in ATOMIC_MASSES:
            total += count * ATOMIC_MASSES[element]
        else:
            raise ValueError(f"Unknown element: {element}")
    return round(total, 3)


def exact_mass(formula: dict) -> float:
    """
    Calculate exact mass using isotope masses.
    
    Args:
        formula: Dictionary like {'C': 5, 'H': 12}
    
    Returns:
        Exact mass in amu
    
    Example:
        >>> exact_mass({'C': 5, 'H': 12})
        72.09396
    """
    total = 0.0
    for element, count in formula.items():
        if element in EXACT_MASSES:
            total += count * EXACT_MASSES[element]
        else:
            raise ValueError(f"Unknown element: {element}")
    return round(total, 5)


def m_plus_one_intensity(carbons: int, hydrogens: int = 0, 
                         nitrogens: int = 0) -> float:
    """
    Calculate expected M+1 peak intensity.
    
    Based on natural abundance of heavier isotopes:
    - 13C: 1.10% per carbon
    - 2H: 0.015% per hydrogen
    - 15N: 0.366% per nitrogen
    
    Args:
        carbons: Number of carbon atoms
        hydrogens: Number of hydrogen atoms
        nitrogens: Number of nitrogen atoms
    
    Returns:
        Expected M+1 intensity as percentage
    
    Example:
        >>> m_plus_one_intensity(6, 6)  # benzene
        6.69
    """
    intensity = (
        carbons * ISOTOPE_ABUNDANCES['13C'] +
        hydrogens * ISOTOPE_ABUNDANCES['2H'] +
        nitrogens * ISOTOPE_ABUNDANCES['15N']
    )
    return round(intensity, 2)


def m_plus_two_intensity(carbons: int, oxygens: int = 0,
                         sulfurs: int = 0, chlorines: int = 0,
                         bromines: int = 0) -> float:
    """
    Calculate expected M+2 peak intensity.
    
    Args:
        carbons: Number of carbon atoms (13C2 contribution)
        oxygens: Number of oxygen atoms
        sulfurs: Number of sulfur atoms
        chlorines: Number of chlorine atoms
        bromines: Number of bromine atoms
    
    Returns:
        Expected M+2 intensity as percentage
    """
    # 18O contribution
    o_contrib = oxygens * ISOTOPE_ABUNDANCES['18O']
    
    # 34S contribution  
    s_contrib = sulfurs * 4.21  # 34S abundance
    
    # 37Cl contribution
    cl_contrib = chlorines * ISOTOPE_ABUNDANCES['37Cl']
    
    # 81Br contribution
    br_contrib = bromines * ISOTOPE_ABUNDANCES['81Br']
    
    # 13C2 contribution (small)
    c_contrib = carbons * (ISOTOPE_ABUNDANCES['13C'] ** 2) / 100
    
    total = o_contrib + s_contrib + cl_contrib + br_contrib + c_contrib
    return round(total, 2)


def fragment_mass(molecular_ion: int, lost_mass: int) -> int:
    """
    Calculate fragment mass from loss.
    
    Args:
        molecular_ion: M+ value
        lost_mass: Mass of lost fragment
    
    Returns:
        Fragment m/z value
    
    Example:
        >>> fragment_mass(86, 29)  # hexane losing C2H5
        57
    """
    return molecular_ion - lost_mass


def identify_fragment_loss(molecular_ion: int, fragment_mz: int) -> dict:
    """
    Identify the fragment lost from molecular ion.
    
    Args:
        molecular_ion: M+ value
        fragment_mz: Observed fragment m/z
    
    Returns:
        Dictionary with lost mass and possible identity
    
    Example:
        >>> identify_fragment_loss(86, 57)
        {'lost_mass': 29, 'possible': 'C2H5 (ethyl)'}
    """
    lost_mass = molecular_ion - fragment_mz
    
    # Common losses
    common_losses = {
        1: 'H',
        15: 'CH3 (methyl)',
        17: 'OH',
        18: 'H2O',
        29: 'C2H5 (ethyl) or CHO',
        31: 'CH3O',
        35: 'Cl (35Cl)',
        43: 'C3H7 (propyl) or CH3CO',
        44: 'CO2',
        45: 'C2H5O or COOH',
        57: 'C4H9 (butyl)',
        79: 'Br (79Br)',
        91: 'C7H7 (benzyl)',
        127: 'I',
    }
    
    possible = common_losses.get(lost_mass, 'Unknown fragment')
    
    return {
        'lost_mass': lost_mass,
        'possible': possible
    }


def nominal_mass(formula: dict) -> int:
    """
    Calculate nominal mass (integer mass of most abundant isotopes).
    
    Args:
        formula: Dictionary like {'C': 6, 'H': 12, 'O': 6}
    
    Returns:
        Nominal mass as integer
    """
    nominal_masses = {
        'C': 12, 'H': 1, 'O': 16, 'N': 14, 'S': 32,
        'Cl': 35, 'Br': 79, 'F': 19, 'P': 31, 'I': 127
    }
    
    total = 0
    for element, count in formula.items():
        if element in nominal_masses:
            total += count * nominal_masses[element]
    return total


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "12-01",
        "question": "Calculate MW of C6H12O6",
        "formula": {'C': 6, 'H': 12, 'O': 6},
        "expected_mw": 180.156
    },
    {
        "id": "12-02",
        "question": "Calculate exact mass of C5H12",
        "formula": {'C': 5, 'H': 12},
        "expected_exact": 72.09396
    },
    {
        "id": "12-03",
        "question": "M+1 intensity for C6H6",
        "carbons": 6,
        "hydrogens": 6,
        "expected": 6.69
    },
    {
        "id": "12-04",
        "question": "Fragment mass from hexane M+ losing C2H5",
        "molecular_ion": 86,
        "lost_mass": 29,
        "expected": 57
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Mass Spectrometry Tools")
    print("=" * 40)
    
    # Test molecular weight
    mw = molecular_weight({'C': 6, 'H': 12, 'O': 6})
    print(f"C6H12O6 MW = {mw} g/mol")
    
    # Test exact mass
    em = exact_mass({'C': 5, 'H': 12})
    print(f"C5H12 exact mass = {em} amu")
    
    # Test M+1 intensity
    m1 = m_plus_one_intensity(6, 6)
    print(f"C6H6 M+1 intensity = {m1}%")

MCP_TOOLS = [
    {
        "name": "exact_mass",
        "description": "Calculate exact mass using isotope masses.",
        "parameters": [
            {
                "name": "formula",
                "type": "string"
            }
        ]
    },
    {
        "name": "fragment_mass",
        "description": "Calculate fragment mass from loss.",
        "parameters": [
            {
                "name": "molecular_ion",
                "type": "number"
            },
            {
                "name": "lost_mass",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_fragment_loss",
        "description": "Identify the fragment lost from molecular ion.",
        "parameters": [
            {
                "name": "molecular_ion",
                "type": "number"
            },
            {
                "name": "fragment_mz",
                "type": "number"
            }
        ]
    },
    {
        "name": "m_plus_one_intensity",
        "description": "Calculate expected M+1 peak intensity.",
        "parameters": [
            {
                "name": "carbons",
                "type": "number"
            },
            {
                "name": "hydrogens",
                "type": "number"
            },
            {
                "name": "nitrogens",
                "type": "number"
            }
        ]
    },
    {
        "name": "m_plus_two_intensity",
        "description": "Calculate expected M+2 peak intensity.",
        "parameters": [
            {
                "name": "carbons",
                "type": "number"
            },
            {
                "name": "oxygens",
                "type": "number"
            },
            {
                "name": "sulfurs",
                "type": "number"
            },
            {
                "name": "chlorines",
                "type": "number"
            },
            {
                "name": "bromines",
                "type": "number"
            }
        ]
    },
    {
        "name": "molecular_weight",
        "description": "Calculate molecular weight from formula.",
        "parameters": [
            {
                "name": "formula",
                "type": "string"
            }
        ]
    },
    {
        "name": "nominal_mass",
        "description": "Calculate nominal mass (integer mass of most abundant isotopes).",
        "parameters": [
            {
                "name": "formula",
                "type": "string"
            }
        ]
    }
]
