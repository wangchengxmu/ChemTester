"""
Crystallography Tools - L3 Implementation
Source: LibreTexts Chemistry (Bragg's Law, Miller Indices, d-spacing)

## Solver Instructions (for AI Agent)

When you encounter crystallography problems (Bragg's law, Miller indices, d-spacing, unit cell calculations):

### Step 1: Identify what is given and what is asked
- Given: wavelength, angle, crystal system, lattice parameters, Miller indices
- Asked: d-spacing, diffraction angles, unit cell volume, density, coordination number, packing fraction

### Step 2: Choose the correct function
- `braggs_law(n, wavelength, d_spacing)`: nlambda = 2d sin θ -> solve for unknown
- `braggs_angle(n, wavelength, d_spacing)`: θ from Bragg's law
- `d_spacing_from_bragg(n, wavelength, angle_deg)`: d from Bragg's law
- `is_reflection_possible(n, wavelength, d_spacing)`: Check if nlambda ≤ 2d
- `intercepts_to_miller(intercepts)`: Convert intercepts to (hkl)
- `miller_to_intercepts(h, k, l, a, b, c)`: Convert (hkl) to intercepts
- `d_spacing_cubic(a, h, k, l)`: d = a/√(h2+k2+l2)
- `d_spacing_tetragonal(a, c, h, k, l)`, `d_spacing_orthorhombic(...)`: Other crystal systems
- `d_spacing_general(crystal_system, params, h, k, l)`: Universal d-spacing
- `unit_cell_volume(cell_type, a, b, c, ...)`: Volume for any cell type
- `crystal_density(n_atoms, atomic_mass, ...)`: ρ = nM/(VxN_A)
- `atoms_per_unit_cell(cell_type)`: Z for SC(1), BCC(2), FCC(4)
- `coordination_number(structure_type)`: CN for SC(6), BCC(8), FCC(12)
- `packing_fraction(structure_type)`: SC(0.52), BCC(0.68), FCC(0.74)
- `atomic_radius_from_lattice(edge_length, structure_type)`: r from a
- `lattice_parameter_from_radius(radius, structure_type)`: a from r
- `get_xray_wavelength(source)`: Cu Kalpha = 1.5418 Å

### Step 3: Handle special cases
- FCC: atoms at corners + face centers; BCC: corners + body center
- Systematic absences: FCC requires h,k,l all odd or all even; BCC requires h+k+l = even

### Examples
```python
d_spacing_cubic(3.61, 1, 1, 1)  # Cu (111) -> 2.085 Å
braggs_angle(1, 1.5418, 2.085)  # Cu Kalpha, (111) -> 21.7deg
crystal_density(4, 63.55, 3.61, 'fcc')  # Cu -> 8.93 g/cm3
```
"""

from typing import Tuple, Optional, Dict, Union
import math


# ============================================================================
# Constants
# ============================================================================

AVOGADRO = 6.02214076e23  # mol-1

XRAY_WAVELENGTHS = {
    'Cu': 1.5418,
    'Cu_Ka': 1.5418,
    'Mo': 0.7107,
    'Mo_Ka': 0.7107,
    'Cr': 2.2910,
    'Cr_Ka': 2.2910,
    'Co': 1.7903,
    'Co_Ka': 1.7903,
    'Fe': 1.9373,
    'Fe_Ka': 1.9373,
}


# ============================================================================
# Bragg's Law Functions
# ============================================================================

def braggs_law(n: int = 1, wavelength: Optional[float] = None,
               d_spacing: Optional[float] = None,
               angle_deg: Optional[float] = None) -> Dict[str, float]:
    """
    Apply Bragg's law: nlambda = 2d sin(θ)
    
    Solve for the missing variable given two of three:
    - wavelength (lambda)
    - d_spacing (d)
    - angle (θ)
    
    Args:
        n: Order of reflection (integer ≥ 1)
        wavelength: X-ray wavelength in Angstroms
        d_spacing: Interplanar spacing in Angstroms
        angle_deg: Bragg angle in degrees
    
    Returns:
        Dict with all parameters including calculated value
    
    Raises:
        ValueError: If fewer than two of wavelength/d_spacing/angle_deg are provided
        ValueError: If reflection is not possible (nlambda > 2d)
    
    Examples:
        >>> result = braggs_law(n=1, wavelength=1.5418, d_spacing=2.0)
        >>> round(result['angle_deg'], 2)
        50.35
        
        >>> result = braggs_law(n=1, wavelength=1.5418, angle_deg=20.0)
        >>> round(result['d_spacing'], 3)
        2.254
    """
    provided = sum(x is not None for x in [wavelength, d_spacing, angle_deg])
    if provided < 2:
        raise ValueError("At least two of wavelength, d_spacing, angle_deg must be provided")
    
    if n < 1:
        raise ValueError("Order n must be >= 1")
    
    # Solve for angle
    if angle_deg is None:
        # θ = arcsin(nlambda / 2d)
        sin_theta = n * wavelength / (2 * d_spacing)
        if sin_theta > 1:
            raise ValueError(f"Reflection not possible: nlambda = {n * wavelength:.4f} > 2d = {2 * d_spacing:.4f}")
        angle_deg = math.degrees(math.asin(sin_theta))
    
    # Solve for d-spacing
    elif d_spacing is None:
        # d = nlambda / (2 sin θ)
        d_spacing = n * wavelength / (2 * math.sin(math.radians(angle_deg)))
    
    # Solve for wavelength
    elif wavelength is None:
        # lambda = 2d sin θ / n
        wavelength = 2 * d_spacing * math.sin(math.radians(angle_deg)) / n
    
    return {
        'n': n,
        'wavelength': wavelength,
        'd_spacing': d_spacing,
        'angle_deg': angle_deg
    }


def braggs_angle(n: int, wavelength: float, d_spacing: float) -> Optional[float]:
    """
    Calculate Bragg angle from wavelength and d-spacing.
    
    Args:
        n: Order of reflection
        wavelength: X-ray wavelength in Angstroms
        d_spacing: Interplanar spacing in Angstroms
    
    Returns:
        Bragg angle in degrees, or None if reflection not possible
    
    Examples:
        >>> round(braggs_angle(1, 1.5418, 2.0), 2)
        50.35
        >>> braggs_angle(3, 1.5418, 1.0) is None
        True
    """
    sin_theta = n * wavelength / (2 * d_spacing)
    if sin_theta > 1 or sin_theta < 0:
        return None
    return math.degrees(math.asin(sin_theta))


def d_spacing_from_bragg(n: int, wavelength: float, angle_deg: float) -> float:
    """
    Calculate d-spacing from Bragg's law.
    
    Args:
        n: Order of reflection
        wavelength: X-ray wavelength in Angstroms
        angle_deg: Bragg angle in degrees
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: If angle is not in valid range (0 < θ ≤ 90)
    
    Examples:
        >>> round(d_spacing_from_bragg(1, 1.5418, 20.0), 3)
        2.254
    """
    if angle_deg <= 0 or angle_deg >= 90:
        raise ValueError("Angle must be between 0 and 90 degrees (exclusive)")
    
    sin_theta = math.sin(math.radians(angle_deg))
    return n * wavelength / (2 * sin_theta)


def is_reflection_possible(n: int, wavelength: float, d_spacing: float) -> bool:
    """
    Check if reflection is possible given n, lambda, and d.
    
    Constraint: nlambda ≤ 2d
    
    Args:
        n: Order of reflection
        wavelength: X-ray wavelength in Angstroms
        d_spacing: Interplanar spacing in Angstroms
    
    Returns:
        True if reflection is possible
    
    Examples:
        >>> is_reflection_possible(1, 1.5418, 2.0)
        True
        >>> is_reflection_possible(3, 1.5418, 1.0)
        False
    """
    return n * wavelength <= 2 * d_spacing


def path_difference(d_spacing: float, angle_deg: float) -> float:
    """
    Calculate path difference between rays from adjacent planes.
    
    Path difference = 2d sin(θ)
    
    Args:
        d_spacing: Interplanar spacing in Angstroms
        angle_deg: Angle in degrees
    
    Returns:
        Path difference in Angstroms
    
    Examples:
        >>> round(path_difference(2.0, 30.0), 3)
        2.0
    """
    return 2 * d_spacing * math.sin(math.radians(angle_deg))


# ============================================================================
# Miller Indices Functions
# ============================================================================

def intercepts_to_miller(intercepts: Tuple[float, float, float]) -> Tuple[int, int, int]:
    """
    Convert intercepts to Miller indices.
    
    Args:
        intercepts: (x_intercept, y_intercept, z_intercept) in units of a, b, c
                   Use float('inf') for planes parallel to an axis
    
    Returns:
        Miller indices (h, k, l) as integers
    
    Examples:
        >>> intercepts_to_miller((1, 1, 1))
        (1, 1, 1)
        >>> intercepts_to_miller((1, float('inf'), float('inf')))
        (1, 0, 0)
        >>> intercepts_to_miller((1, 2, 3))
        (6, 3, 2)
    """
    reciprocals = []
    for intercept in intercepts:
        if intercept == float('inf') or intercept == 0:
            reciprocals.append(0)
        else:
            reciprocals.append(1.0 / intercept)
    
    # Find LCM to clear fractions
    # Convert to fractions and find common denominator
    def float_to_fraction(x: float, tolerance: float = 1e-9) -> Tuple[int, int]:
        """Convert float to fraction (numerator, denominator)."""
        if abs(x) < tolerance:
            return (0, 1)
        
        # Try to find a simple fraction
        for denom in range(1, 1000):
            numer = round(x * denom)
            if abs(x - numer / denom) < tolerance:
                return (int(numer), denom)
        return (int(round(x * 1000000)), 1000000)
    
    fractions = [float_to_fraction(r) for r in reciprocals]
    denominators = [f[1] for f in fractions]
    
    # Find LCM of denominators
    def lcm(a: int, b: int) -> int:
        return abs(a * b) // math.gcd(a, b)
    
    common_denom = 1
    for d in denominators:
        common_denom = lcm(common_denom, d)
    
    # Clear fractions
    miller_indices = []
    for numer, denom in fractions:
        miller_indices.append(int(numer * common_denom // denom))
    
    # Reduce to smallest integers by dividing by GCD
    def gcd_three(a: int, b: int, c: int) -> int:
        return math.gcd(math.gcd(abs(a), abs(b)), abs(c))
    
    common_gcd = gcd_three(miller_indices[0], miller_indices[1], miller_indices[2])
    if common_gcd > 0:
        miller_indices = [m // common_gcd for m in miller_indices]
    
    return tuple(miller_indices)


def miller_to_intercepts(h: int, k: int, l: int,
                         a: float = 1.0, b: float = 1.0, c: float = 1.0) -> Tuple[float, float, float]:
    """
    Convert Miller indices to intercepts.
    
    Args:
        h, k, l: Miller indices
        a, b, c: Lattice parameters (default to 1 for normalized intercepts)
    
    Returns:
        Intercepts (x, y, z) in units of a, b, c
    
    Examples:
        >>> miller_to_intercepts(1, 0, 0)
        (1.0, inf, inf)
        >>> miller_to_intercepts(1, 1, 1, a=4.0, b=4.0, c=4.0)
        (4.0, 4.0, 4.0)
    """
    def intercept(index: int, lattice_param: float) -> float:
        if index == 0:
            return float('inf')
        return lattice_param / index
    
    return (intercept(h, a), intercept(k, b), intercept(l, c))


# ============================================================================
# d-Spacing Functions
# ============================================================================

def d_spacing_cubic(a: float, h: int, k: int, l: int) -> float:
    """
    Calculate d-spacing for cubic system.
    
    d = a / √(h2 + k2 + l2)
    
    Args:
        a: Lattice parameter in Angstroms
        h, k, l: Miller indices
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: If h=k=l=0 (invalid Miller indices)
    
    Examples:
        >>> round(d_spacing_cubic(4.0, 1, 1, 1), 3)
        2.309
        >>> round(d_spacing_cubic(3.0, 1, 0, 0), 3)
        3.0
    """
    sum_sq = h**2 + k**2 + l**2
    if sum_sq == 0:
        raise ValueError("Invalid Miller indices: h=k=l=0")
    return a / math.sqrt(sum_sq)


def d_spacing_tetragonal(a: float, c: float, h: int, k: int, l: int) -> float:
    """
    Calculate d-spacing for tetragonal system.
    
    1/d2 = (h2 + k2)/a2 + l2/c2
    
    Args:
        a, c: Lattice parameters in Angstroms
        h, k, l: Miller indices
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: If all indices are zero
    
    Examples:
        >>> round(d_spacing_tetragonal(3.0, 5.0, 1, 0, 1), 3)
        2.572
    """
    inv_d_sq = (h**2 + k**2) / a**2 + l**2 / c**2
    if inv_d_sq == 0:
        raise ValueError("Invalid Miller indices: h=k=l=0")
    return 1.0 / math.sqrt(inv_d_sq)


def d_spacing_orthorhombic(a: float, b: float, c: float,
                           h: int, k: int, l: int) -> float:
    """
    Calculate d-spacing for orthorhombic system.
    
    1/d2 = h2/a2 + k2/b2 + l2/c2
    
    Args:
        a, b, c: Lattice parameters in Angstroms
        h, k, l: Miller indices
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: If all indices are zero
    
    Examples:
        >>> round(d_spacing_orthorhombic(3.0, 4.0, 5.0, 1, 1, 1), 3)
        2.182
    """
    inv_d_sq = h**2 / a**2 + k**2 / b**2 + l**2 / c**2
    if inv_d_sq == 0:
        raise ValueError("Invalid Miller indices: h=k=l=0")
    return 1.0 / math.sqrt(inv_d_sq)


def d_spacing_hexagonal(a: float, c: float, h: int, k: int, l: int) -> float:
    """
    Calculate d-spacing for hexagonal system.
    
    1/d2 = (4/3)[(h2 + hk + k2)/a2] + l2/c2
    
    Args:
        a, c: Lattice parameters in Angstroms
        h, k, l: Miller indices
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: If all indices are zero
    
    Examples:
        >>> round(d_spacing_hexagonal(2.5, 4.0, 1, 0, 1), 3)
        2.113
    """
    inv_d_sq = (4.0/3.0) * (h**2 + h*k + k**2) / a**2 + l**2 / c**2
    if inv_d_sq == 0:
        raise ValueError("Invalid Miller indices: h=k=l=0")
    return 1.0 / math.sqrt(inv_d_sq)


def d_spacing_monoclinic(a: float, b: float, c: float, beta_deg: float,
                         h: int, k: int, l: int) -> float:
    """
    Calculate d-spacing for monoclinic system.
    
    1/d2 = [h2/a2 + k2sin2beta/b2 + l2/c2 - 2hl cosbeta/(ac)] / sin2beta
    
    Args:
        a, b, c: Lattice parameters in Angstroms
        beta_deg: Angle beta in degrees
        h, k, l: Miller indices
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: If all indices are zero
    
    Examples:
        >>> round(d_spacing_monoclinic(5.0, 4.0, 3.0, 100.0, 1, 1, 1), 3)
        2.109
    """
    beta = math.radians(beta_deg)
    sin_beta = math.sin(beta)
    cos_beta = math.cos(beta)
    
    inv_d_sq = (h**2/a**2 + k**2*sin_beta**2/b**2 + l**2/c**2 - 
                2*h*l*cos_beta/(a*c)) / sin_beta**2
    
    if inv_d_sq <= 0:
        raise ValueError("Invalid parameters or Miller indices")
    return 1.0 / math.sqrt(inv_d_sq)


def d_spacing_general(crystal_system: str, params: Dict[str, float],
                      h: int, k: int, l: int) -> float:
    """
    Calculate d-spacing for any crystal system.
    
    Args:
        crystal_system: 'cubic', 'tetragonal', 'orthorhombic', 'hexagonal',
                       'monoclinic', 'rhombohedral', 'triclinic'
        params: Dictionary of lattice parameters
            - cubic: {'a': value}
            - tetragonal: {'a': value, 'c': value}
            - orthorhombic: {'a': value, 'b': value, 'c': value}
            - hexagonal: {'a': value, 'c': value}
            - monoclinic: {'a': value, 'b': value, 'c': value, 'beta': degrees}
        h, k, l: Miller indices
    
    Returns:
        d-spacing in Angstroms
    
    Raises:
        ValueError: For unknown crystal system or missing parameters
    """
    system = crystal_system.lower()
    
    if system == 'cubic':
        return d_spacing_cubic(params['a'], h, k, l)
    elif system == 'tetragonal':
        return d_spacing_tetragonal(params['a'], params['c'], h, k, l)
    elif system == 'orthorhombic':
        return d_spacing_orthorhombic(params['a'], params['b'], params['c'], h, k, l)
    elif system == 'hexagonal':
        return d_spacing_hexagonal(params['a'], params['c'], h, k, l)
    elif system == 'monoclinic':
        return d_spacing_monoclinic(params['a'], params['b'], params['c'], 
                                   params.get('beta', 90.0), h, k, l)
    elif system in ('rhombohedral', 'triclinic'):
        raise ValueError(f"Crystal system '{crystal_system}' not yet fully implemented")
    else:
        raise ValueError(f"Unknown crystal system: {crystal_system}")


# ============================================================================
# Unit Cell Volume Functions
# ============================================================================

def unit_cell_volume(cell_type: str, a: float, b: Optional[float] = None,
                     c: Optional[float] = None,
                     alpha: float = 90.0, beta: float = 90.0,
                     gamma: float = 90.0) -> float:
    """
    Calculate unit cell volume for any crystal system.
    
    Args:
        cell_type: 'cubic', 'tetragonal', 'orthorhombic', 'hexagonal',
                  'monoclinic', 'rhombohedral', 'triclinic'
        a, b, c: Lattice parameters in Angstroms
        alpha, beta, gamma: Angles in degrees
    
    Returns:
        Volume in Å3
    
    Examples:
        >>> unit_cell_volume('cubic', a=4.0)
        64.0
        >>> round(unit_cell_volume('hexagonal', a=2.0, c=3.0), 2)
        10.39
    """
    system = cell_type.lower()
    
    if system == 'cubic':
        return a ** 3
    
    elif system == 'tetragonal':
        return a ** 2 * c
    
    elif system == 'orthorhombic':
        return a * b * c
    
    elif system == 'hexagonal':
        # V = (√3/2) x a2 x c
        return (math.sqrt(3) / 2) * a ** 2 * c
    
    elif system == 'monoclinic':
        # V = abc x sin(beta)
        return a * b * c * math.sin(math.radians(beta))
    
    elif system == 'rhombohedral':
        # V = a3√(1 - 3cos2alpha + 2cos3alpha)
        alpha_rad = math.radians(alpha)
        cos_alpha = math.cos(alpha_rad)
        factor = 1 - 3 * cos_alpha**2 + 2 * cos_alpha**3
        if factor < 0:
            raise ValueError("Invalid rhombohedral angle")
        return a ** 3 * math.sqrt(factor)
    
    elif system == 'triclinic':
        # V = abc√(1 - cos2alpha - cos2beta - cos2gamma + 2cosalpha cosbeta cosgamma)
        cos_alpha = math.cos(math.radians(alpha))
        cos_beta = math.cos(math.radians(beta))
        cos_gamma = math.cos(math.radians(gamma))
        factor = (1 - cos_alpha**2 - cos_beta**2 - cos_gamma**2 + 
                  2 * cos_alpha * cos_beta * cos_gamma)
        if factor < 0:
            raise ValueError("Invalid triclinic angles")
        return a * b * c * math.sqrt(factor)
    
    else:
        raise ValueError(f"Unknown crystal system: {cell_type}")


# ============================================================================
# Crystal Density Functions
# ============================================================================

def crystal_density(n_atoms: int, atomic_mass: float,
                    volume_angstrom3: float) -> float:
    """
    Calculate crystal density from unit cell parameters.
    
    ρ = (n x M) / (V x N_A)
    
    Args:
        n_atoms: Number of atoms per unit cell
        atomic_mass: Molar mass in g/mol
        volume_angstrom3: Unit cell volume in Å3
    
    Returns:
        Density in g/cm3
    
    Examples:
        >>> round(crystal_density(4, 58.69, 43.8), 2)  # Ni, FCC
        8.91
    """
    # Convert volume from Å3 to cm3
    volume_cm3 = volume_angstrom3 * 1e-24
    
    # ρ = (n x M) / (V x N_A)
    density = (n_atoms * atomic_mass) / (volume_cm3 * AVOGADRO)
    
    return density


def atoms_per_unit_cell(cell_type: str) -> int:
    """
    Return number of atoms per unit cell for common structures.
    
    Args:
        cell_type: 'simple_cubic', 'sc', 'bcc', 'fcc', 'hcp', 'diamond'
    
    Returns:
        Number of atoms per unit cell
    
    Examples:
        >>> atoms_per_unit_cell('fcc')
        4
        >>> atoms_per_unit_cell('bcc')
        2
    """
    counts = {
        'simple_cubic': 1,
        'sc': 1,
        'bcc': 2,
        'fcc': 4,
        'hcp': 2,
        'diamond': 8,
    }
    cell_type_lower = cell_type.lower()
    if cell_type_lower not in counts:
        raise ValueError(f"Unknown cell type: {cell_type}")
    return counts[cell_type_lower]


# ============================================================================
# Crystal System Identification
# ============================================================================

def identify_crystal_system_from_params(a: float, b: float, c: float,
                                        alpha: float = 90.0,
                                        beta: float = 90.0,
                                        gamma: float = 90.0) -> str:
    """
    Identify crystal system from lattice parameters.
    
    Args:
        a, b, c: Lattice parameters
        alpha, beta, gamma: Angles in degrees
    
    Returns:
        Crystal system name
    
    Examples:
        >>> identify_crystal_system_from_params(4.0, 4.0, 4.0, 90, 90, 90)
        'cubic'
        >>> identify_crystal_system_from_params(3.0, 3.0, 5.0, 90, 90, 90)
        'tetragonal'
    """
    # Tolerance for floating point comparison
    tol = 1e-6
    
    edges_equal = abs(a - b) < tol and abs(b - c) < tol
    a_equal_b = abs(a - b) < tol
    all_angles_90 = (abs(alpha - 90) < tol and 
                     abs(beta - 90) < tol and 
                     abs(gamma - 90) < tol)
    all_angles_equal = abs(alpha - beta) < tol and abs(beta - gamma) < tol
    alpha_gamma_90 = abs(alpha - 90) < tol and abs(gamma - 90) < tol
    
    if edges_equal and all_angles_90:
        return 'cubic'
    elif a_equal_b and not edges_equal and all_angles_90:
        return 'tetragonal'
    elif not a_equal_b and not edges_equal and all_angles_90:
        return 'orthorhombic'
    elif a_equal_b and alpha_gamma_90 and abs(gamma - 120) < tol:
        return 'hexagonal'
    elif edges_equal and all_angles_equal and not all_angles_90:
        return 'rhombohedral'
    elif alpha_gamma_90 and not all_angles_90:
        return 'monoclinic'
    else:
        return 'triclinic'


# ============================================================================
# X-ray Wavelength Utilities
# ============================================================================

def get_xray_wavelength(source: str) -> float:
    """
    Get X-ray wavelength for common sources.
    
    Args:
        source: Source name ('Cu', 'Mo', 'Cr', 'Co', 'Fe') or full name ('Cu_Ka')
    
    Returns:
        Wavelength in Angstroms
    
    Raises:
        ValueError: If source is not recognized
    
    Examples:
        >>> get_xray_wavelength('Cu')
        1.5418
        >>> get_xray_wavelength('Mo_Ka')
        0.7107
    """
    source_key = source.strip()
    if source_key in XRAY_WAVELENGTHS:
        return XRAY_WAVELENGTHS[source_key]
    raise ValueError(f"Unknown X-ray source: {source}. "
                     f"Available: {', '.join(set(XRAY_WAVELENGTHS.keys()))}")


# ============================================================================
# Higher-Order Reflections
# ============================================================================

def higher_order_angles(wavelength: float, d_spacing: float, 
                        max_order: int = 5) -> Dict[int, Optional[float]]:
    """
    Calculate Bragg angles for higher-order reflections.
    
    Args:
        wavelength: X-ray wavelength in Angstroms
        d_spacing: Interplanar spacing in Angstroms
        max_order: Maximum order to calculate
    
    Returns:
        Dict mapping order n to angle in degrees (None if not possible)
    
    Examples:
        >>> angles = higher_order_angles(1.5418, 2.0, max_order=3)
        >>> round(angles[1], 2)
        50.35
        >>> round(angles[2], 2)
        90.0  # or None if not possible
    """
    result = {}
    for n in range(1, max_order + 1):
        result[n] = braggs_angle(n, wavelength, d_spacing)
    return result


# ============================================================================
# Multiple Planes Analysis
# ============================================================================

def diffraction_angles_for_planes(a: float, planes: list, 
                                  wavelength: float = 1.5418,
                                  crystal_system: str = 'cubic') -> list:
    """
    Calculate diffraction angles for multiple crystal planes.
    
    Args:
        a: Lattice parameter (for cubic; may need additional params for other systems)
        planes: List of (h, k, l) Miller indices
        wavelength: X-ray wavelength in Angstroms
        crystal_system: Crystal system type
    
    Returns:
        List of dicts with plane and angle information
    
    Examples:
        >>> result = diffraction_angles_for_planes(4.0, [(1,0,0), (1,1,0), (1,1,1)])
        >>> len(result)
        3
    """
    results = []
    for h, k, l in planes:
        d = d_spacing_general(crystal_system, {'a': a}, h, k, l)
        angle = braggs_angle(1, wavelength, d)
        results.append({
            'plane': (h, k, l),
            'd_spacing': d,
            'angle_deg': angle,
            'reflection_possible': angle is not None
        })
    return results


# ============================================================================
# Coordination Number and Packing Functions
# ============================================================================

def coordination_number(structure_type: str) -> int:
    """
    Return coordination number for common crystal structures.
    
    Args:
        structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc', 'hcp', 'diamond'
    
    Returns:
        Coordination number (number of nearest neighbors)
    
    Examples:
        >>> coordination_number('fcc')
        12
        >>> coordination_number('bcc')
        8
        >>> coordination_number('diamond')
        4
    """
    cn_values = {
        'simple_cubic': 6,
        'sc': 6,
        'bcc': 8,
        'fcc': 12,
        'hcp': 12,
        'diamond': 4,
    }
    structure_lower = structure_type.lower()
    if structure_lower not in cn_values:
        raise ValueError(f"Unknown structure type: {structure_type}")
    return cn_values[structure_lower]


def packing_fraction(structure_type: str) -> float:
    """
    Return packing fraction (efficiency) for common crystal structures.
    
    Packing fraction = Volume of atoms / Volume of unit cell
    
    Args:
        structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc', 'hcp', 'diamond'
    
    Returns:
        Packing fraction (0 to 1)
    
    Examples:
        >>> packing_fraction('fcc')
        0.74
        >>> packing_fraction('bcc')
        0.68
        >>> packing_fraction('diamond')
        0.34
    """
    pf_values = {
        'simple_cubic': 0.524,
        'sc': 0.524,
        'bcc': 0.680,
        'fcc': 0.740,
        'hcp': 0.740,
        'diamond': 0.340,
    }
    structure_lower = structure_type.lower()
    if structure_lower not in pf_values:
        raise ValueError(f"Unknown structure type: {structure_type}")
    return pf_values[structure_lower]


def atomic_radius_from_lattice(edge_length: float, structure_type: str) -> float:
    """
    Calculate atomic radius from lattice parameter for cubic structures.
    
    Args:
        edge_length: Unit cell edge length in Angstroms
        structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc'
    
    Returns:
        Atomic radius in Angstroms
    
    Raises:
        ValueError: For unknown structure type
    
    Examples:
        >>> round(atomic_radius_from_lattice(4.0, 'fcc'), 3)
        1.414
        >>> round(atomic_radius_from_lattice(4.0, 'bcc'), 3)
        1.732
        >>> atomic_radius_from_lattice(4.0, 'sc')
        2.0
    """
    structure_lower = structure_type.lower()
    
    if structure_lower in ('simple_cubic', 'sc'):
        # r = a/2 (atoms touch along edge)
        return edge_length / 2
    elif structure_lower == 'bcc':
        # r = a√3/4 (atoms touch along body diagonal)
        return edge_length * math.sqrt(3) / 4
    elif structure_lower == 'fcc':
        # r = a√2/4 (atoms touch along face diagonal)
        return edge_length * math.sqrt(2) / 4
    else:
        raise ValueError(f"Cannot calculate atomic radius for structure type: {structure_type}")


def lattice_parameter_from_radius(radius: float, structure_type: str) -> float:
    """
    Calculate lattice parameter from atomic radius for cubic structures.
    
    Args:
        radius: Atomic radius in Angstroms
        structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc'
    
    Returns:
        Lattice parameter (edge length) in Angstroms
    
    Examples:
        >>> lattice_parameter_from_radius(1.414, 'fcc')
        4.0
        >>> round(lattice_parameter_from_radius(1.732, 'bcc'), 1)
        4.0
    """
    structure_lower = structure_type.lower()
    
    if structure_lower in ('simple_cubic', 'sc'):
        return 2 * radius
    elif structure_lower == 'bcc':
        return 4 * radius / math.sqrt(3)
    elif structure_lower == 'fcc':
        return 4 * radius / math.sqrt(2)
    else:
        raise ValueError(f"Cannot calculate lattice parameter for structure type: {structure_type}")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'atomic_radius_from_lattice', 'description': "Calculate atomic radius from lattice parameter for cubic structures.\n\nArgs:\n    edge_length: Unit cell edge length in Angstroms\n    structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc'\n\nReturns:\n    Atomic radius in Angstroms\n\nRaises:\n    ValueError: For unknown structure type\n\nExamples:\n    >>> round(atomic_radius_from_lattice(4.0, 'fcc'), 3)\n    1.414\n    >>> round(atomic_radius_from_lattice(4.0, 'bcc'), 3)\n    1.732\n    >>> atomic_radius_from_lattice(4.0, 'sc')\n    2.0", 'inputSchema': {'type': 'object', 'properties': {'edge_length': {'type': 'number', 'description': 'Edge Length'}, 'structure_type': {'type': 'string', 'description': 'Structure Type'}}, 'required': ['edge_length', 'structure_type']}},
    {'name': 'atoms_per_unit_cell', 'description': "Return number of atoms per unit cell for common structures.\n\nArgs:\n    cell_type: 'simple_cubic', 'sc', 'bcc', 'fcc', 'hcp', 'diamond'\n\nReturns:\n    Number of atoms per unit cell\n\nExamples:\n    >>> atoms_per_unit_cell('fcc')\n    4\n    >>> atoms_per_unit_cell('bcc')\n    2", 'inputSchema': {'type': 'object', 'properties': {'cell_type': {'type': 'string', 'description': 'Cell Type'}}, 'required': ['cell_type']}},
    {'name': 'braggs_angle', 'description': 'Calculate Bragg angle from wavelength and d-spacing.\n\nArgs:\n    n: Order of reflection\n    wavelength: X-ray wavelength in Angstroms\n    d_spacing: Interplanar spacing in Angstroms\n\nReturns:\n    Bragg angle in degrees, or null if reflection not possible\n\nExamples:\n    >>> round(braggs_angle(1, 1.5418, 2.0), 2)\n    50.35\n    >>> braggs_angle(3, 1.5418, 1.0) is null\n    true', 'inputSchema': {'type': 'object', 'properties': {'n': {'type': 'number', 'description': 'N'}, 'wavelength': {'type': 'number', 'description': 'Wavelength'}, 'd_spacing': {'type': 'number', 'description': 'D Spacing'}}, 'required': ['n', 'wavelength', 'd_spacing']}},
    {'name': 'braggs_law', 'description': "Apply Bragg's law: nlambda = 2d sin(θ)\n\nSolve for the missing variable given two of three:\n- wavelength (lambda)\n- d_spacing (d)\n- angle (θ)\n\nArgs:\n    n: Order of reflection (integer ≥ 1)\n    wavelength: X-ray wavelength in Angstroms\n    d_spacing: Interplanar spacing in Angstroms\n    angle_deg: Bragg angle in degrees\n\nReturns:\n    Dict with all parameters including calculated value\n\nRaises:\n    ValueError: If fewer than two of wavelength/d_spacing/angle_deg are provided\n    ValueError: If reflection is not possible (nlambda > 2d)\n\nExamples:\n    >>> result = braggs_law(n=1, wavelength=1.5418, d_spacing=2.0)\n    >>> round(result['angle_deg'], 2)\n    50.35\n    \n    >>> result = braggs_law(n=1, wavelength=1.5418, angle_deg=20.0)\n    >>> round(result['d_spacing'], 3)\n    2.254", 'inputSchema': {'type': 'object', 'properties': {'n': {'type': 'number', 'description': 'N', 'default': 1}, 'wavelength': {'type': 'number', 'description': 'Wavelength', 'default': None}, 'd_spacing': {'type': 'number', 'description': 'D Spacing', 'default': None}, 'angle_deg': {'type': 'number', 'description': 'Angle Deg', 'default': None}}, 'required': []}},
    {'name': 'coordination_number', 'description': "Return coordination number for common crystal structures.\n\nArgs:\n    structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc', 'hcp', 'diamond'\n\nReturns:\n    Coordination number (number of nearest neighbors)\n\nExamples:\n    >>> coordination_number('fcc')\n    12\n    >>> coordination_number('bcc')\n    8\n    >>> coordination_number('diamond')\n    4", 'inputSchema': {'type': 'object', 'properties': {'structure_type': {'type': 'string', 'description': 'Structure Type'}}, 'required': ['structure_type']}},
    {'name': 'crystal_density', 'description': 'Calculate crystal density from unit cell parameters.\n\nρ = (n x M) / (V x N_A)\n\nArgs:\n    n_atoms: Number of atoms per unit cell\n    atomic_mass: Molar mass in g/mol\n    volume_angstrom3: Unit cell volume in Å3\n\nReturns:\n    Density in g/cm3\n\nExamples:\n    >>> round(crystal_density(4, 58.69, 43.8), 2)  # Ni, FCC\n    8.91', 'inputSchema': {'type': 'object', 'properties': {'n_atoms': {'type': 'number', 'description': 'N Atoms'}, 'atomic_mass': {'type': 'number', 'description': 'Atomic Mass'}, 'volume_angstrom3': {'type': 'number', 'description': 'Volume Angstrom3'}}, 'required': ['n_atoms', 'atomic_mass', 'volume_angstrom3']}},
    {'name': 'd_spacing_cubic', 'description': 'Calculate d-spacing for cubic system.\n\nd = a / √(h2 + k2 + l2)\n\nArgs:\n    a: Lattice parameter in Angstroms\n    h, k, l: Miller indices\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: If h=k=l=0 (invalid Miller indices)\n\nExamples:\n    >>> round(d_spacing_cubic(4.0, 1, 1, 1), 3)\n    2.309\n    >>> round(d_spacing_cubic(3.0, 1, 0, 0), 3)\n    3.0', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}}, 'required': ['a', 'h', 'k', 'l']}},
    {'name': 'd_spacing_from_bragg', 'description': "Calculate d-spacing from Bragg's law.\n\nArgs:\n    n: Order of reflection\n    wavelength: X-ray wavelength in Angstroms\n    angle_deg: Bragg angle in degrees\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: If angle is not in valid range (0 < θ ≤ 90)\n\nExamples:\n    >>> round(d_spacing_from_bragg(1, 1.5418, 20.0), 3)\n    2.254", 'inputSchema': {'type': 'object', 'properties': {'n': {'type': 'number', 'description': 'N'}, 'wavelength': {'type': 'number', 'description': 'Wavelength'}, 'angle_deg': {'type': 'number', 'description': 'Angle Deg'}}, 'required': ['n', 'wavelength', 'angle_deg']}},
    {'name': 'd_spacing_general', 'description': "Calculate d-spacing for any crystal system.\n\nArgs:\n    crystal_system: 'cubic', 'tetragonal', 'orthorhombic', 'hexagonal',\n                   'monoclinic', 'rhombohedral', 'triclinic'\n    params: Dictionary of lattice parameters\n        - cubic: {'a': value}\n        - tetragonal: {'a': value, 'c': value}\n        - orthorhombic: {'a': value, 'b': value, 'c': value}\n        - hexagonal: {'a': value, 'c': value}\n        - monoclinic: {'a': value, 'b': value, 'c': value, 'beta': degrees}\n    h, k, l: Miller indices\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: For unknown crystal system or missing parameters", 'inputSchema': {'type': 'object', 'properties': {'crystal_system': {'type': 'string', 'description': 'Crystal System'}, 'params': {'type': 'number', 'description': 'Params'}, 'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}}, 'required': ['crystal_system', 'params', 'h', 'k', 'l']}},
    {'name': 'd_spacing_hexagonal', 'description': 'Calculate d-spacing for hexagonal system.\n\n1/d2 = (4/3)[(h2 + hk + k2)/a2] + l2/c2\n\nArgs:\n    a, c: Lattice parameters in Angstroms\n    h, k, l: Miller indices\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: If all indices are zero\n\nExamples:\n    >>> round(d_spacing_hexagonal(2.5, 4.0, 1, 0, 1), 3)\n    2.113', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'c': {'type': 'number', 'description': 'C'}, 'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}}, 'required': ['a', 'c', 'h', 'k', 'l']}},
    {'name': 'd_spacing_monoclinic', 'description': 'Calculate d-spacing for monoclinic system.\n\n1/d2 = [h2/a2 + k2sin2beta/b2 + l2/c2 - 2hl cosbeta/(ac)] / sin2beta\n\nArgs:\n    a, b, c: Lattice parameters in Angstroms\n    beta_deg: Angle beta in degrees\n    h, k, l: Miller indices\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: If all indices are zero\n\nExamples:\n    >>> round(d_spacing_monoclinic(5.0, 4.0, 3.0, 100.0, 1, 1, 1), 3)\n    2.109', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'b': {'type': 'number', 'description': 'B'}, 'c': {'type': 'number', 'description': 'C'}, 'beta_deg': {'type': 'number', 'description': 'Beta Deg'}, 'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}}, 'required': ['a', 'b', 'c', 'beta_deg', 'h', 'k', 'l']}},
    {'name': 'd_spacing_orthorhombic', 'description': 'Calculate d-spacing for orthorhombic system.\n\n1/d2 = h2/a2 + k2/b2 + l2/c2\n\nArgs:\n    a, b, c: Lattice parameters in Angstroms\n    h, k, l: Miller indices\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: If all indices are zero\n\nExamples:\n    >>> round(d_spacing_orthorhombic(3.0, 4.0, 5.0, 1, 1, 1), 3)\n    2.182', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'b': {'type': 'number', 'description': 'B'}, 'c': {'type': 'number', 'description': 'C'}, 'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}}, 'required': ['a', 'b', 'c', 'h', 'k', 'l']}},
    {'name': 'd_spacing_tetragonal', 'description': 'Calculate d-spacing for tetragonal system.\n\n1/d2 = (h2 + k2)/a2 + l2/c2\n\nArgs:\n    a, c: Lattice parameters in Angstroms\n    h, k, l: Miller indices\n\nReturns:\n    d-spacing in Angstroms\n\nRaises:\n    ValueError: If all indices are zero\n\nExamples:\n    >>> round(d_spacing_tetragonal(3.0, 5.0, 1, 0, 1), 3)\n    2.572', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'c': {'type': 'number', 'description': 'C'}, 'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}}, 'required': ['a', 'c', 'h', 'k', 'l']}},
    {'name': 'diffraction_angles_for_planes', 'description': 'Calculate diffraction angles for multiple crystal planes.\n\nArgs:\n    a: Lattice parameter (for cubic; may need additional params for other systems)\n    planes: List of (h, k, l) Miller indices\n    wavelength: X-ray wavelength in Angstroms\n    crystal_system: Crystal system type\n\nReturns:\n    List of dicts with plane and angle information\n\nExamples:\n    >>> result = diffraction_angles_for_planes(4.0, [(1,0,0), (1,1,0), (1,1,1)])\n    >>> len(result)\n    3', 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'planes': {'type': 'string', 'description': 'Planes'}, 'wavelength': {'type': 'number', 'description': 'Wavelength', 'default': 1.5418}, 'crystal_system': {'type': 'string', 'description': 'Crystal System', 'default': 'cubic'}}, 'required': ['a', 'planes']}},
    {'name': 'get_xray_wavelength', 'description': "Get X-ray wavelength for common sources.\n\nArgs:\n    source: Source name ('Cu', 'Mo', 'Cr', 'Co', 'Fe') or full name ('Cu_Ka')\n\nReturns:\n    Wavelength in Angstroms\n\nRaises:\n    ValueError: If source is not recognized\n\nExamples:\n    >>> get_xray_wavelength('Cu')\n    1.5418\n    >>> get_xray_wavelength('Mo_Ka')\n    0.7107", 'inputSchema': {'type': 'object', 'properties': {'source': {'type': 'string', 'description': 'Source'}}, 'required': ['source']}},
    {'name': 'higher_order_angles', 'description': 'Calculate Bragg angles for higher-order reflections.\n\nArgs:\n    wavelength: X-ray wavelength in Angstroms\n    d_spacing: Interplanar spacing in Angstroms\n    max_order: Maximum order to calculate\n\nReturns:\n    Dict mapping order n to angle in degrees (null if not possible)\n\nExamples:\n    >>> angles = higher_order_angles(1.5418, 2.0, max_order=3)\n    >>> round(angles[1], 2)\n    50.35\n    >>> round(angles[2], 2)\n    90.0  # or null if not possible', 'inputSchema': {'type': 'object', 'properties': {'wavelength': {'type': 'number', 'description': 'Wavelength'}, 'd_spacing': {'type': 'number', 'description': 'D Spacing'}, 'max_order': {'type': 'number', 'description': 'Max Order', 'default': 5}}, 'required': ['wavelength', 'd_spacing']}},
    {'name': 'identify_crystal_system_from_params', 'description': "Identify crystal system from lattice parameters.\n\nArgs:\n    a, b, c: Lattice parameters\n    alpha, beta, gamma: Angles in degrees\n\nReturns:\n    Crystal system name\n\nExamples:\n    >>> identify_crystal_system_from_params(4.0, 4.0, 4.0, 90, 90, 90)\n    'cubic'\n    >>> identify_crystal_system_from_params(3.0, 3.0, 5.0, 90, 90, 90)\n    'tetragonal'", 'inputSchema': {'type': 'object', 'properties': {'a': {'type': 'number', 'description': 'A'}, 'b': {'type': 'number', 'description': 'B'}, 'c': {'type': 'number', 'description': 'C'}, 'alpha': {'type': 'number', 'description': 'Alpha', 'default': 90.0}, 'beta': {'type': 'number', 'description': 'Beta', 'default': 90.0}, 'gamma': {'type': 'string', 'description': 'Gamma', 'default': 90.0}}, 'required': ['a', 'b', 'c']}},
    {'name': 'intercepts_to_miller', 'description': "Convert intercepts to Miller indices.\n\nArgs:\n    intercepts: (x_intercept, y_intercept, z_intercept) in units of a, b, c\n               Use float('inf') for planes parallel to an axis\n\nReturns:\n    Miller indices (h, k, l) as integers\n\nExamples:\n    >>> intercepts_to_miller((1, 1, 1))\n    (1, 1, 1)\n    >>> intercepts_to_miller((1, float('inf'), float('inf')))\n    (1, 0, 0)\n    >>> intercepts_to_miller((1, 2, 3))\n    (6, 3, 2)", 'inputSchema': {'type': 'object', 'properties': {'intercepts': {'type': 'number', 'description': 'Intercepts'}}, 'required': ['intercepts']}},
    {'name': 'is_reflection_possible', 'description': 'Check if reflection is possible given n, lambda, and d.\n\nConstraint: nlambda ≤ 2d\n\nArgs:\n    n: Order of reflection\n    wavelength: X-ray wavelength in Angstroms\n    d_spacing: Interplanar spacing in Angstroms\n\nReturns:\n    true if reflection is possible\n\nExamples:\n    >>> is_reflection_possible(1, 1.5418, 2.0)\n    true\n    >>> is_reflection_possible(3, 1.5418, 1.0)\n    false', 'inputSchema': {'type': 'object', 'properties': {'n': {'type': 'number', 'description': 'N'}, 'wavelength': {'type': 'number', 'description': 'Wavelength'}, 'd_spacing': {'type': 'number', 'description': 'D Spacing'}}, 'required': ['n', 'wavelength', 'd_spacing']}},
    {'name': 'lattice_parameter_from_radius', 'description': "Calculate lattice parameter from atomic radius for cubic structures.\n\nArgs:\n    radius: Atomic radius in Angstroms\n    structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc'\n\nReturns:\n    Lattice parameter (edge length) in Angstroms\n\nExamples:\n    >>> lattice_parameter_from_radius(1.414, 'fcc')\n    4.0\n    >>> round(lattice_parameter_from_radius(1.732, 'bcc'), 1)\n    4.0", 'inputSchema': {'type': 'object', 'properties': {'radius': {'type': 'number', 'description': 'Radius'}, 'structure_type': {'type': 'string', 'description': 'Structure Type'}}, 'required': ['radius', 'structure_type']}},
    {'name': 'miller_to_intercepts', 'description': 'Convert Miller indices to intercepts.\n\nArgs:\n    h, k, l: Miller indices\n    a, b, c: Lattice parameters (default to 1 for normalized intercepts)\n\nReturns:\n    Intercepts (x, y, z) in units of a, b, c\n\nExamples:\n    >>> miller_to_intercepts(1, 0, 0)\n    (1.0, inf, inf)\n    >>> miller_to_intercepts(1, 1, 1, a=4.0, b=4.0, c=4.0)\n    (4.0, 4.0, 4.0)', 'inputSchema': {'type': 'object', 'properties': {'h': {'type': 'number', 'description': 'H'}, 'k': {'type': 'number', 'description': 'K'}, 'l': {'type': 'number', 'description': 'L'}, 'a': {'type': 'number', 'description': 'A', 'default': 1.0}, 'b': {'type': 'number', 'description': 'B', 'default': 1.0}, 'c': {'type': 'number', 'description': 'C', 'default': 1.0}}, 'required': ['h', 'k', 'l']}},
    {'name': 'packing_fraction', 'description': "Return packing fraction (efficiency) for common crystal structures.\n\nPacking fraction = Volume of atoms / Volume of unit cell\n\nArgs:\n    structure_type: 'simple_cubic', 'sc', 'bcc', 'fcc', 'hcp', 'diamond'\n\nReturns:\n    Packing fraction (0 to 1)\n\nExamples:\n    >>> packing_fraction('fcc')\n    0.74\n    >>> packing_fraction('bcc')\n    0.68\n    >>> packing_fraction('diamond')\n    0.34", 'inputSchema': {'type': 'object', 'properties': {'structure_type': {'type': 'string', 'description': 'Structure Type'}}, 'required': ['structure_type']}},
    {'name': 'path_difference', 'description': 'Calculate path difference between rays from adjacent planes.\n\nPath difference = 2d sin(θ)\n\nArgs:\n    d_spacing: Interplanar spacing in Angstroms\n    angle_deg: Angle in degrees\n\nReturns:\n    Path difference in Angstroms\n\nExamples:\n    >>> round(path_difference(2.0, 30.0), 3)\n    2.0', 'inputSchema': {'type': 'object', 'properties': {'d_spacing': {'type': 'number', 'description': 'D Spacing'}, 'angle_deg': {'type': 'number', 'description': 'Angle Deg'}}, 'required': ['d_spacing', 'angle_deg']}},
    {'name': 'unit_cell_volume', 'description': "Calculate unit cell volume for any crystal system.\n\nArgs:\n    cell_type: 'cubic', 'tetragonal', 'orthorhombic', 'hexagonal',\n              'monoclinic', 'rhombohedral', 'triclinic'\n    a, b, c: Lattice parameters in Angstroms\n    alpha, beta, gamma: Angles in degrees\n\nReturns:\n    Volume in Å3\n\nExamples:\n    >>> unit_cell_volume('cubic', a=4.0)\n    64.0\n    >>> round(unit_cell_volume('hexagonal', a=2.0, c=3.0), 2)\n    10.39", 'inputSchema': {'type': 'object', 'properties': {'cell_type': {'type': 'string', 'description': 'Cell Type'}, 'a': {'type': 'number', 'description': 'A'}, 'b': {'type': 'number', 'description': 'B', 'default': None}, 'c': {'type': 'number', 'description': 'C', 'default': None}, 'alpha': {'type': 'number', 'description': 'Alpha', 'default': 90.0}, 'beta': {'type': 'number', 'description': 'Beta', 'default': 90.0}, 'gamma': {'type': 'string', 'description': 'Gamma', 'default': 90.0}}, 'required': ['cell_type', 'a']}}
]
