"""
Crystal Structures Tools - L3 Implementation
Source: Averill, Ch12

## Solver Instructions (for AI Agent)

When you encounter a crystal structure problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Lattice type: Simple cubic, body-centered cubic (bcc), face-centered cubic (fcc)
- Edge length: Unit cell dimension (often in pm or Å)
- Atomic radius: Often asked to calculate
- Density: Mass per volume
- Coordination number: Number of nearest neighbors
- Lattice parameters: a, b, c, alpha, beta, gamma

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate atomic radius from edge length | `cubic_lattice_radius(edge_length, cell_type)` - types: 'simple_cubic', 'bcc', 'fcc' |
| Calculate edge length from atomic radius | `edge_length_from_radius(radius, cell_type)` |
| Calculate unit cell volume | `unit_cell_volume_cubic(edge_length)` |
| Identify crystal system from parameters | `identify_crystal_system(a, b, c, alpha, beta, gamma)` |
| Predict coordination number from radius ratio | `ionic_radius_ratio_rule(cation_radius, anion_radius)` |
| Get Bravais lattice types | `bravais_lattice_types()` |
| Count atoms per unit area on face | `atoms_per_area_cubic(cell_type)` |

### Step 3: Handle special cases
- **Simple cubic**: 1 atom per unit cell, radius = edge/2
- **Body-centered cubic (bcc)**: 2 atoms per unit cell, radius = (edge x √3)/4
- **Face-centered cubic (fcc)**: 4 atoms per unit cell, radius = (edge x √2)/4
- **Radius ratio rule**: Predicts coordination geometry
  - < 0.155: CN=2 (linear)
  - 0.155-0.225: CN=3 (triangular)
  - 0.225-0.414: CN=4 (tetrahedral)
  - 0.414-0.732: CN=6 (octahedral)
  - 0.732-1.0: CN=8 (cubic)
  - ≥ 1.0: CN=12 (closest packing)

### Examples

**Example 1: Atomic radius from edge length**
Question: "Calculate the atomic radius for fcc aluminum with edge length 404 pm."
- Solution: `cubic_lattice_radius(edge_length=404, cell_type='fcc')` -> 143 pm

**Example 2: Edge length from radius**
Question: "What is the edge length of a bcc crystal with atomic radius 124 pm?"
- Solution: `edge_length_from_radius(radius=124, cell_type='bcc')` -> 286 pm

**Example 3: Radius ratio prediction**
Question: "Predict the coordination number for NaCl. Na+ radius = 102 pm, Cl- radius = 181 pm."
- Solution: `ionic_radius_ratio_rule(cation_radius=102, anion_radius=181)` -> 'CN=6 (octahedral)'

**Example 4: Identify crystal system**
Question: "What crystal system has a = b = c = 4.0 Å, alpha = beta = gamma = 90deg?"
- Solution: `identify_crystal_system(a=4.0, b=4.0, c=4.0, alpha=90, beta=90, gamma=90)` -> 'cubic'
"""

from typing import Dict, Tuple
import math


def cubic_lattice_radius(edge_length: float, cell_type: str) -> float:
    """
    Calculate atomic radius from cubic unit cell edge length.
    
    Args:
        edge_length: Unit cell edge in pm or Å
        cell_type: 'simple_cubic', 'bcc', or 'fcc'
    
    Returns:
        Atomic radius
    
    Examples:
        >>> cubic_lattice_radius(100, 'simple_cubic')
        50.0
        >>> round(cubic_lattice_radius(100, 'fcc'), 2)
        35.36
    """
    if cell_type == 'simple_cubic':
        # 2r = a
        return edge_length / 2
    elif cell_type == 'bcc':
        # 4r = a√3
        return edge_length * math.sqrt(3) / 4
    elif cell_type == 'fcc':
        # 4r = a√2
        return edge_length * math.sqrt(2) / 4
    else:
        return 0.0


def edge_length_from_radius(radius: float, cell_type: str) -> float:
    """
    Calculate unit cell edge length from atomic radius.
    
    Args:
        radius: Atomic radius
        cell_type: Crystal structure type
    
    Returns:
        Edge length
    """
    if cell_type == 'simple_cubic':
        return 2 * radius
    elif cell_type == 'bcc':
        return 4 * radius / math.sqrt(3)
    elif cell_type == 'fcc':
        return 4 * radius / math.sqrt(2)
    else:
        return 0.0


def identify_crystal_system(a: float, b: float, c: float,
                            alpha: float = 90, beta: float = 90, 
                            gamma: float = 90) -> str:
    """
    Identify crystal system from lattice parameters.
    
    Args:
        a, b, c: Lattice constants
        alpha, beta, gamma: Angles in degrees
    
    Returns:
        Crystal system name
    """
    if a == b == c and alpha == beta == gamma == 90:
        return 'cubic'
    elif a == b != c and alpha == beta == gamma == 90:
        return 'tetragonal'
    elif a != b != c and alpha == beta == gamma == 90:
        return 'orthorhombic'
    elif a == b == c and alpha == beta == gamma != 90:
        return 'rhombohedral' if alpha != 90 else 'hexagonal'
    elif a == b and alpha == beta == 90 and gamma == 120:
        return 'hexagonal'
    elif alpha == gamma == 90 and beta != 90:
        return 'monoclinic'
    else:
        return 'triclinic'


def bravais_lattice_types() -> Dict:
    """
    Return all Bravais lattice types organized by crystal system.
    
    Returns:
        Dict mapping crystal system to Bravais lattices
    """
    return {
        'cubic': ['simple', 'body-centered', 'face-centered'],
        'tetragonal': ['simple', 'body-centered'],
        'orthorhombic': ['simple', 'body-centered', 'face-centered', 'base-centered'],
        'hexagonal': ['simple'],
        'rhombohedral': ['simple'],
        'monoclinic': ['simple', 'base-centered'],
        'triclinic': ['simple']
    }


def ionic_radius_ratio_rule(cation_radius: float, anion_radius: float) -> str:
    """
    Predict coordination number from radius ratio.
    
    Args:
        cation_radius: Radius of cation
        anion_radius: Radius of anion
    
    Returns:
        Predicted coordination number and geometry
    
    Examples:
        >>> ionic_radius_ratio_rule(60, 140)
        'CN=6 (octahedral)'
    """
    ratio = cation_radius / anion_radius
    
    if ratio < 0.155:
        return 'CN=2 (linear)'
    elif ratio < 0.225:
        return 'CN=3 (triangular)'
    elif ratio < 0.414:
        return 'CN=4 (tetrahedral)'
    elif ratio < 0.732:
        return 'CN=6 (octahedral)'
    elif ratio < 1.0:
        return 'CN=8 (cubic)'
    else:
        return 'CN=12 (closest packing)'


def unit_cell_volume_cubic(edge_length: float) -> float:
    """
    Calculate volume of cubic unit cell.
    
    Args:
        edge_length: Edge length in same units as desired volume
    
    Returns:
        Volume in units3
    """
    return edge_length ** 3


def atoms_per_area_cubic(cell_type: str) -> int:
    """
    Count atoms per unit area on crystal face.
    
    Args:
        cell_type: Crystal structure type
    
    Returns:
        Number of atoms per face
    """
    counts = {
        'simple_cubic': 1,
        'bcc': 1,  # (100) face
        'fcc': 2   # (100) face
    }
    return counts.get(cell_type, 0)


def drude_resistivity(lattice_constant_A: float, valence_electrons: int,
                      scattering_time_fs: float, atoms_per_cell: int = 4,
                      structure: str = 'fcc') -> Dict:
    """
    Calculate electrical resistivity using the Drude model.
    
    The Drude model treats electrons as a classical gas. The resistivity is:
        ρ = m_e / (n × e² × τ)
    
    where n is the electron density (in electrons/m³, NOT cm³).
    
    Args:
        lattice_constant_A: Lattice constant in Angstroms (Å)
        valence_electrons: Number of conduction electrons per atom
        scattering_time_fs: Mean scattering time in femtoseconds (fs)
        atoms_per_cell: Number of atoms per unit cell (default: 4 for fcc)
        structure: Crystal structure ('fcc', 'bcc', 'sc')
    
    Returns:
        Dictionary with resistivity in various units
    
    Examples:
        >>> drude_resistivity(4.046, 3, 11.8)  # Aluminum
        {'resistivity_ohm_m': 2.65e-08, 'resistivity_uOhm_cm': 2.65}
    
    Note:
        CRITICAL: The electron density n must be in SI units (electrons/m³).
        Using electrons/cm³ causes a 10⁶ error in resistivity.
        
        Unit conversion:
        - Lattice constant: Å → m: multiply by 1e-10
        - Scattering time: fs → s: multiply by 1e-15
        - Electron density: electrons/Å³ → electrons/m³: multiply by 1e30
    """
    import math
    
    # Physical constants (SI units)
    m_e = 9.10938e-31  # electron mass in kg
    e = 1.602176634e-19  # electron charge in C
    
    # Convert inputs to SI units
    a_m = lattice_constant_A * 1e-10  # Å to m
    tau_s = scattering_time_fs * 1e-15  # fs to s
    
    # Calculate electron density in electrons/m³ (CRITICAL: use SI units!)
    # Volume in m³
    cell_volume_m3 = a_m ** 3
    # Total electrons per unit cell
    total_electrons = atoms_per_cell * valence_electrons
    # Electron density in electrons/m³
    n_m3 = total_electrons / cell_volume_m3  # electrons/m³
    
    # Drude resistivity formula (all SI units)
    # ρ = m_e / (n × e² × τ)
    rho_ohm_m = m_e / (n_m3 * e**2 * tau_s)
    
    # Convert to convenient units
    rho_ohm_cm = rho_ohm_m * 100  # Ω·m to Ω·cm
    rho_uOhm_cm = rho_ohm_cm * 1e6  # Ω·cm to μΩ·cm
    
    return {
        'resistivity_ohm_m': rho_ohm_m,
        'resistivity_ohm_cm': rho_ohm_cm,
        'resistivity_uOhm_cm': round(rho_uOhm_cm, 2),
        'electron_density_m3': n_m3,
        'scattering_time_s': tau_s,
        'lattice_constant_m': a_m
    }


def packing_fraction(cell_type: str) -> float:
    """
    Calculate packing fraction for different crystal structures.
    
    Packing fraction = volume of atoms / volume of unit cell
    
    Args:
        cell_type: 'sc', 'bcc', 'fcc', 'hcp'
    
    Returns:
        Packing fraction as decimal (e.g., 0.74 for fcc)
    
    Examples:
        >>> packing_fraction('fcc')
        0.7405
        >>> packing_fraction('bcc')
        0.6802
        >>> packing_fraction('sc')
        0.5236
    """
    import math
    
    fractions = {
        'sc': math.pi / 6,           # 0.5236
        'bcc': math.sqrt(3) * math.pi / 8,  # 0.6802
        'fcc': math.sqrt(2) * math.pi / 6,  # 0.7405
        'hcp': math.sqrt(2) * math.pi / 6,  # 0.7405 (same as fcc)
        'simple_cubic': math.pi / 6,
        'body_centered_cubic': math.sqrt(3) * math.pi / 8,
        'face_centered_cubic': math.sqrt(2) * math.pi / 6,
    }
    return fractions.get(cell_type.lower(), 0.0)


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'atoms_per_area_cubic', 'description': 'Count atoms per unit area on crystal face.\n\nArgs:\n    cell_type: Crystal structure type\n\nReturns:\n    Number of atoms per face', 'inputSchema': {'type': 'object', 'properties': {'cell_type': {'type': 'string', 'description': 'Cell Type'}}, 'required': ['cell_type']}},
    {'name': 'bravais_lattice_types', 'description': 'Return all Bravais lattice types organized by crystal system.\n\nReturns:\n    Dict mapping crystal system to Bravais lattices', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'cubic_lattice_radius', 'description': "Calculate atomic radius from cubic unit cell edge length.\n\nArgs:\n    edge_length: Unit cell edge in pm or Å\n    cell_type: 'simple_cubic', 'bcc', or 'fcc'\n\nReturns:\n    Atomic radius\n\nExamples:\n    >>> cubic_lattice_radius(100, 'simple_cubic')\n    50.0\n    >>> round(cubic_lattice_radius(100, 'fcc'), 2)\n    35.36", 'inputSchema': {'type': 'object', 'properties': {'edge_length': {'type': 'number', 'description': 'Edge Length'}, 'cell_type': {'type': 'string', 'description': 'Cell Type'}}, 'required': ['edge_length', 'cell_type']}},
    {'name': 'edge_length_from_radius', 'description': 'Calculate unit cell edge length from atomic radius.\n\nArgs:\n    radius: Atomic radius\n    cell_type: Crystal structure type\n\nReturns:\n    Edge length', 'inputSchema': {'type': 'object', 'properties': {'radius': {'type': 'number', 'description': 'Radius'}, 'cell_type': {'type': 'string', 'description': 'Cell Type'}}, 'required': ['radius', 'cell_type']}},
    {'name': 'identify_crystal_system', 'description': 'Identify crystal system from lattice parameters.\n\nArgs:\n    a, b, c: Lattice constants\n    alpha, beta, gamma: Angles in degrees\n\nReturns:\n    Crystal system name', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'b': {'type': 'number', 'description': 'B'}, 'c': {'type': 'number', 'description': 'C'}, 'alpha': {'type': 'number', 'description': 'Alpha', 'default': 90}, 'beta': {'type': 'number', 'description': 'Beta', 'default': 90}, 'gamma': {'type': 'string', 'description': 'Gamma', 'default': 90}}, 'required': ['a', 'b', 'c']}},
    {'name': 'ionic_radius_ratio_rule', 'description': "Predict coordination number from radius ratio.\n\nArgs:\n    cation_radius: Radius of cation\n    anion_radius: Radius of anion\n\nReturns:\n    Predicted coordination number and geometry\n\nExamples:\n    >>> ionic_radius_ratio_rule(60, 140)\n    'CN=6 (octahedral)'", 'inputSchema': {'type': 'object', 'properties': {'cation_radius': {'type': 'string', 'description': 'Cation Radius'}, 'anion_radius': {'type': 'string', 'description': 'Anion Radius'}}, 'required': ['cation_radius', 'anion_radius']}},
    {'name': 'unit_cell_volume_cubic', 'description': 'Calculate volume of cubic unit cell.\n\nArgs:\n    edge_length: Edge length in same units as desired volume\n\nReturns:\n    Volume in units3', 'inputSchema': {'type': 'object', 'properties': {'edge_length': {'type': 'number', 'description': 'Edge Length'}}, 'required': ['edge_length']}},
    {'name': 'drude_resistivity', 'description': 'Calculate electrical resistivity using the Drude model. CRITICAL: Uses SI units internally. Returns resistivity in μΩ·cm.', 'inputSchema': {'type': 'object', 'properties': {'lattice_constant_A': {'type': 'number', 'description': 'Lattice constant in Angstroms'}, 'valence_electrons': {'type': 'number', 'description': 'Conduction electrons per atom'}, 'scattering_time_fs': {'type': 'number', 'description': 'Mean scattering time in femtoseconds'}, 'atoms_per_cell': {'type': 'number', 'description': 'Atoms per unit cell (default 4 for fcc)', 'default': 4}, 'structure': {'type': 'string', 'description': 'Crystal structure', 'default': 'fcc'}}, 'required': ['lattice_constant_A', 'valence_electrons', 'scattering_time_fs']}},
    {'name': 'packing_fraction', 'description': 'Calculate packing fraction for crystal structures. Returns decimal (e.g., 0.74 for fcc).', 'inputSchema': {'type': 'object', 'properties': {'cell_type': {'type': 'string', 'description': 'Crystal structure type (sc, bcc, fcc, hcp)'}}, 'required': ['cell_type']}}
]
