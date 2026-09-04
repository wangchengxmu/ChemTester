"""
Nanomaterials Tools - L3 Implementation

Functions for calculating nanomaterial properties including quantum confinement,
surface effects, carbon nanotube electronic properties, and plasmon resonance.

Source: Wikibooks Nanotechnology Ch04 - Nanomaterials

Dependencies: numpy

## Solver Instructions (for AI Agent)

When you encounter nanomaterial problems (quantum dots, nanotubes, nanoparticles), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given quantum dot size -> calculate band gap (quantum confinement)?
- Given nanotube indices -> calculate diameter and electronic type?
- Given nanoparticle size -> calculate surface-to-volume ratio?
- Given metal nanoparticle -> calculate plasmon resonance wavelength?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Quantum confinement | `quantum_confinement_energy(radius, m_e_star, m_h_star, bulk_bandgap, dielectric)` | Returns bandgap, emission lambda |
| CNT diameter | `cnt_diameter(n, m)` | (n,m) chiral indices -> diameter in nm |
| CNT electronic type | `cnt_electronic_type(n, m)` | Returns 'metallic', 'semiconducting', or 'armchair' |
| Surface-to-volume ratio | `surface_to_volume_ratio(radius, shape)` | For spheres, cubes, etc. |
| Plasmon resonance | `plasmon_resonance_wavelength(particle_diameter, metal)` | Au, Ag nanoparticles |

### Step 3: Handle special cases
- Quantum confinement: Smaller QD -> larger band gap (blue shift)
- CNT: Armchair (n,n) always metallic; (n-m) divisible by 3 -> metallic
- Surface effects dominate below ~10 nm

### Examples
```python
# Example 1: CdSe quantum dot (r=2.5 nm)
quantum_confinement_energy(2.5, 0.13, 0.45, 1.74, 9.7)
# -> {'bandgap_eV': ~2.2, 'emission_wavelength_nm': ~560}

# Example 2: Carbon nanotube (10,0)
cnt_diameter(10, 0)
# -> ~0.78 nm

cnt_electronic_type(10, 0)  # 10-0=10, not divisible by 3
# -> 'semiconducting'

# Example 3: Surface-to-volume ratio (sphere, r=5 nm)
surface_to_volume_ratio(5, 'sphere')
# -> 3/r = 0.6 nm-1
```
"""

import numpy as np
from typing import Tuple, Dict, Optional, Union

# Physical constants
H_PLANCK = 6.62607015e-34  # J·s
H_BAR = H_PLANCK / (2 * np.pi)  # J·s
E_CHARGE = 1.602176634e-19  # C
M_ELECTRON = 9.10938370e-31  # kg
EPSILON_0 = 8.8541878128e-12  # F/m
C_LIGHT = 2.99792458e8  # m/s
EV_TO_J = 1.602176634e-19  # J/eV


def particle_in_a_box_energy(n: int, L: float, effective_mass_ratio: float = 1.0,
                              units: str = 'nm') -> float:
    """
    Calculate energy of a particle in a 1D box.
    
    E_n = n²h² / (8 * m * L²)
    
    Args:
        n: Quantum number (1, 2, 3, ...)
        L: Box length
        effective_mass_ratio: m*/m_e ratio (default 1.0 for free electron)
            E.g., GaAs quantum well: use 0.067
        units: 'nm' (default) or 'm'
    
    Returns:
        Energy in eV
    
    Note:
        For semiconductor quantum wells, use the effective mass ratio.
        GaAs electron: 0.067, GaAs hole: 0.45, CdSe electron: 0.13
        Using m_e directly (ratio=1.0) gives incorrect results for semiconductors.
    """
    if units == 'nm':
        L_m = L * 1e-9
    else:
        L_m = L
    
    m = effective_mass_ratio * M_ELECTRON
    E_J = (n ** 2 * H_PLANCK ** 2) / (8 * m * L_m ** 2)
    return E_J / EV_TO_J


def quantum_confinement_energy(
    radius: float,
    m_e_star: float,
    m_h_star: float,
    bulk_bandgap: float,
    dielectric_constant: float,
    units: str = "nm"
) -> Dict[str, float]:
    """
    Calculate quantum confinement energy for semiconductor quantum dots.
    
    Uses the effective mass approximation with Coulomb correction:
    
    E_g(QD) = E_g(bulk) + (h2pi2)/(2R2) x (1/m_e* + 1/m_h*) - 1.8e2/(4piε0εR)
    
    Where:
    - R = nanocrystal radius
    - m_e*, m_h* = effective masses of electron and hole
    - ε = dielectric constant of material
    
    Args:
        radius: Quantum dot radius (default in nm)
        m_e_star: Effective electron mass (in units of m_e, e.g., 0.13 for CdSe)
        m_h_star: Effective hole mass (in units of m_e, e.g., 0.45 for CdSe)
        bulk_bandgap: Bulk material bandgap in eV
        dielectric_constant: Relative dielectric constant of material
        units: "nm" for nanometers, "m" for meters
    
    Returns:
        Dictionary containing:
        - 'bandgap_eV': Total quantum dot bandgap in eV
        - 'confinement_energy_eV': Quantum confinement contribution in eV
        - 'coulomb_correction_eV': Coulomb interaction correction in eV
        - 'emission_wavelength_nm': Predicted emission wavelength in nm
    
    Example:
        >>> result = quantum_confinement_energy(
        ...     radius=2.5, m_e_star=0.13, m_h_star=0.45,
        ...     bulk_bandgap=1.74, dielectric_constant=9.7
        ... )
        >>> print(f"CdSe QD bandgap: {result['bandgap_eV']:.2f} eV")
    """
    # Convert radius to meters if needed
    if units == "nm":
        R = radius * 1e-9
    else:
        R = radius
    
    # Convert effective masses to kg
    m_e_kg = m_e_star * M_ELECTRON
    m_h_kg = m_h_star * M_ELECTRON
    
    # Reduced mass for exciton
    mu = (m_e_kg * m_h_kg) / (m_e_kg + m_h_kg)
    
    # Quantum confinement term (particle in a sphere)
    # E_conf = ħ2pi2/(2R2) x (1/m_e* + 1/m_h*)  [using reduced Planck constant]
    confinement_energy_J = (H_BAR**2 * np.pi**2) / (2 * R**2) * \
                           (1/m_e_kg + 1/m_h_kg)
    confinement_energy_eV = confinement_energy_J / EV_TO_J
    
    # Coulomb interaction term (exciton binding)
    # E_coulomb = -1.8e2/(4piε0εR)
    coulomb_energy_J = -1.8 * E_CHARGE**2 / (4 * np.pi * EPSILON_0 * 
                                              dielectric_constant * R)
    coulomb_energy_eV = coulomb_energy_J / EV_TO_J
    
    # Total bandgap
    total_bandgap_eV = bulk_bandgap + confinement_energy_eV + coulomb_energy_eV
    
    # Emission wavelength
    emission_wavelength_nm = (H_PLANCK * C_LIGHT) / (total_bandgap_eV * EV_TO_J) * 1e9
    
    return {
        'bandgap_eV': total_bandgap_eV,
        'confinement_energy_eV': confinement_energy_eV,
        'coulomb_correction_eV': coulomb_energy_eV,
        'emission_wavelength_nm': emission_wavelength_nm
    }


def nanoparticle_surface_area(
    diameter: float,
    shape: str = "sphere",
    units: str = "nm"
) -> Dict[str, float]:
    """
    Calculate surface area and surface-to-volume ratio for nanoparticles.
    
    Surface/Volume ratio ∝ 1/r (for spheres)
    
    Args:
        diameter: Particle diameter (default in nm)
        shape: Particle shape - "sphere", "cube", "cylinder", or "rod"
        units: "nm" for nanometers, "m" for meters
    
    Returns:
        Dictionary containing:
        - 'surface_area_nm2': Surface area in nm2
        - 'volume_nm3': Volume in nm3
        - 'surface_volume_ratio': Surface-to-volume ratio in nm-1
        - 'surface_atoms_percent': Estimated percentage of surface atoms
    
    Example:
        >>> result = nanoparticle_surface_area(diameter=10, shape="sphere")
        >>> print(f"Surface area: {result['surface_area_nm2']:.1f} nm2")
        >>> print(f"Surface atoms: {result['surface_atoms_percent']:.1f}%")
    """
    # Work in nm
    d = diameter if units == "nm" else diameter * 1e9
    r = d / 2
    
    if shape == "sphere":
        # Sphere: A = 4pir2, V = (4/3)pir3
        surface_area = 4 * np.pi * r**2
        volume = (4/3) * np.pi * r**3
        
    elif shape == "cube":
        # Cube: A = 6a2, V = a3 where a = diameter
        surface_area = 6 * d**2
        volume = d**3
        
    elif shape == "cylinder":
        # Cylinder with height = 2xdiameter (aspect ratio 2)
        h = 2 * d
        surface_area = 2 * np.pi * r * (r + h)
        volume = np.pi * r**2 * h
        
    elif shape == "rod":
        # Rod with aspect ratio 5
        h = 5 * d
        surface_area = 2 * np.pi * r * (r + h)
        volume = np.pi * r**2 * h
        
    else:
        raise ValueError(f"Unknown shape: {shape}. Use 'sphere', 'cube', 'cylinder', or 'rod'")
    
    # Surface-to-volume ratio
    sv_ratio = surface_area / volume
    
    # Estimate surface atoms percentage (empirical relation for metals)
    # Assuming atomic radius ~0.15 nm and atoms at surface = ~surface_area / (atomic_area)
    # Simplified model: surface atoms % ~ 100 x (4/r) x 0.15 ~ 60/r
    # More accurate: scales with (surface atoms) / (total atoms) ~ 3x(atomic_diameter)/(particle_diameter)
    atomic_diameter = 0.3  # nm (typical metal atom)
    surface_atoms_percent = min(100, 300 * atomic_diameter / d)
    
    return {
        'surface_area_nm2': surface_area,
        'volume_nm3': volume,
        'surface_volume_ratio_nm_inv': sv_ratio,
        'surface_atoms_percent': surface_atoms_percent
    }


def cnt_electronic_properties(
    n: int,
    m: int,
    bond_length: float = 1.42
) -> Dict[str, Union[float, str, bool]]:
    """
    Determine electronic properties of a carbon nanotube from chiral indices (n,m).
    
    Classification rules:
    - Armchair (n = m): Always metallic
    - Zigzag (m = 0): Metallic if n divisible by 3
    - Chiral: Metallic if (n - m) = 3j (j = integer)
    
    Diameter formula:
    d = √3 x a_C-C x √(m2 + n2 + mn) / pi
    
    Bandgap for semiconducting tubes:
    E_g ~ 0.7-0.8 / d (eV·nm)
    
    Args:
        n: First chiral index
        m: Second chiral index
        bond_length: C-C bond length in Å (default 1.42 Å)
    
    Returns:
        Dictionary containing:
        - 'diameter_nm': Nanotube diameter in nm
        - 'chiral_angle_deg': Chiral angle in degrees
        - 'tube_type': "armchair", "zigzag", or "chiral"
        - 'electronic_type': "metallic" or "semiconducting"
        - 'bandgap_eV': Bandgap in eV (0 for metallic)
        - 'chiral_vector': Tuple (n, m)
    
    Example:
        >>> result = cnt_electronic_properties(10, 10)
        >>> print(f"(10,10) tube is {result['electronic_type']}")
        >>> print(f"Diameter: {result['diameter_nm']:.2f} nm")
    """
    # Calculate diameter
    # d = √3 x a x √(m2 + n2 + mn) / pi
    a_cc = bond_length  # Å
    diameter_A = np.sqrt(3) * a_cc * np.sqrt(n**2 + m**2 + n*m) / np.pi
    diameter_nm = diameter_A / 10
    
    # Calculate chiral angle
    # θ = tan-1(√3m / (2n + m))
    if n == 0 and m == 0:
        chiral_angle = 0
    else:
        chiral_angle = np.degrees(np.arctan(np.sqrt(3) * m / (2*n + m)))
    
    # Determine tube type
    if n == m:
        tube_type = "armchair"
    elif m == 0:
        tube_type = "zigzag"
    else:
        tube_type = "chiral"
    
    # Determine electronic type
    # Metallic if (n - m) is divisible by 3
    diff = n - m
    is_metallic = (diff % 3 == 0)
    
    electronic_type = "metallic" if is_metallic else "semiconducting"
    
    # Calculate bandgap
    if is_metallic:
        bandgap = 0.0
    else:
        # E_g ~ 0.7-0.8 / d (eV·nm)
        # Using k = 0.78 eV·nm (commonly used value)
        k = 0.78
        bandgap = k / diameter_nm
    
    return {
        'diameter_nm': diameter_nm,
        'chiral_angle_deg': chiral_angle,
        'tube_type': tube_type,
        'electronic_type': electronic_type,
        'bandgap_eV': bandgap,
        'chiral_vector': (n, m),
        'is_metallic': is_metallic
    }


def plasmon_resonance(
    material: str = "Au",
    diameter: float = 10,
    shape: str = "sphere",
    dielectric_medium: float = 1.0,
    units: str = "nm"
) -> Dict[str, float]:
    """
    Calculate surface plasmon resonance wavelength for metallic nanoparticles.
    
    For spherical particles, LSPR wavelength depends on:
    1. Material (electron density, effective mass)
    2. Particle size (smaller -> blue shift for Au)
    3. Shape (aspect ratio affects resonance)
    4. Dielectric environment (higher ε -> red shift)
    
    Simplified model for gold:
    lambda_LSPR ~ lambda_0 + size_correction + dielectric_shift
    
    Args:
        material: "Au" (gold), "Ag" (silver), or "Cu" (copper)
        diameter: Particle diameter (default in nm)
        shape: "sphere", "rod", or "ellipsoid"
        dielectric_medium: Dielectric constant of surrounding medium
        units: "nm" for nanometers
    
    Returns:
        Dictionary containing:
        - 'wavelength_nm': LSPR wavelength in nm
        - 'frequency_THz': LSPR frequency in THz
        - 'energy_eV': LSPR energy in eV
        - 'color': Predicted color of solution
    
    Example:
        >>> result = plasmon_resonance(material="Au", diameter=20)
        >>> print(f"Au 20nm LSPR: {result['wavelength_nm']:.1f} nm")
    """
    # Base LSPR wavelengths for spherical particles in water (nm)
    base_lspr = {
        "Au": 520,  # Gold
        "Ag": 400,  # Silver  
        "Cu": 570,  # Copper
        "Al": 360   # Aluminum
    }
    
    if material not in base_lspr:
        raise ValueError(f"Unknown material: {material}. Use Au, Ag, Cu, or Al")
    
    # Work in nm
    d = diameter if units == "nm" else diameter * 1e9
    
    lambda_0 = base_lspr[material]
    
    # Size correction (empirical - larger particles have red-shifted LSPR)
    # For Au: ~0.5 nm red shift per nm increase above 10 nm
    if material == "Au":
        size_shift = 0.5 * (d - 10) if d > 10 else 0
    elif material == "Ag":
        size_shift = 0.3 * (d - 10) if d > 10 else 0
    else:
        size_shift = 0.4 * (d - 10) if d > 10 else 0
    
    # Dielectric medium correction
    # Higher dielectric -> red shift
    # Approximate: Deltalambda ~ (ε - 1) x 40 nm for Au in typical media
    if material == "Au":
        dielectric_shift = (dielectric_medium - 1.33) * 40  # relative to water
    else:
        dielectric_shift = (dielectric_medium - 1.33) * 30
    
    # Shape correction
    if shape == "rod":
        # Nanorods have two LSPR peaks: transverse and longitudinal
        # This returns transverse; longitudinal would need aspect ratio
        shape_shift = 0
    elif shape == "ellipsoid":
        shape_shift = 20  # Red shift for elongated particles
    else:
        shape_shift = 0
    
    # Calculate final LSPR wavelength
    wavelength = lambda_0 + size_shift + dielectric_shift + shape_shift
    wavelength = max(300, wavelength)  # Physical lower limit
    
    # Calculate frequency and energy
    frequency = C_LIGHT / (wavelength * 1e-9) / 1e12  # THz
    energy = (H_PLANCK * C_LIGHT / (wavelength * 1e-9)) / EV_TO_J  # eV
    
    # Determine color
    def wavelength_to_color(wl):
        if wl < 380:
            return "UV"
        elif wl < 450:
            return "violet"
        elif wl < 495:
            return "blue"
        elif wl < 570:
            return "green"
        elif wl < 590:
            return "yellow"
        elif wl < 620:
            return "orange"
        elif wl < 750:
            return "red"
        else:
            return "IR"
    
    color = wavelength_to_color(wavelength)
    
    return {
        'wavelength_nm': wavelength,
        'frequency_THz': frequency,
        'energy_eV': energy,
        'color': color,
        'base_wavelength_nm': lambda_0,
        'size_shift_nm': size_shift,
        'dielectric_shift_nm': dielectric_shift
    }


def particle_size_distribution(
    sizes: np.ndarray,
    weights: Optional[np.ndarray] = None
) -> Dict[str, float]:
    """
    Calculate statistical parameters for nanoparticle size distribution.
    
    Parameters:
    - Number-average diameter: D_n = ΣnᵢDᵢ / Σnᵢ
    - Weight-average diameter: D_w = ΣnᵢDᵢ2 / ΣnᵢDᵢ
    - Polydispersity index: PDI = D_w / D_n
    - Standard deviation: σ = √(Σnᵢ(Dᵢ - D̄)2 / N)
    
    Args:
        sizes: Array of particle diameters (nm)
        weights: Optional weights for each measurement
    
    Returns:
        Dictionary containing:
        - 'mean_nm': Arithmetic mean diameter in nm
        - 'std_nm': Standard deviation in nm
        - 'median_nm': Median diameter in nm
        - 'min_nm': Minimum diameter
        - 'max_nm': Maximum diameter
        - 'pdi': Polydispersity index (D_w/D_n)
        - 'span': Span = (D90 - D10) / D50
        - 'd10_nm': 10th percentile diameter
        - 'd50_nm': 50th percentile diameter (median)
        - 'd90_nm': 90th percentile diameter
        - 'count': Number of particles
    
    Example:
        >>> sizes = np.array([8, 9, 10, 10, 11, 12, 10, 9, 11, 10])
        >>> result = particle_size_distribution(sizes)
        >>> print(f"Mean: {result['mean_nm']:.1f} nm, PDI: {result['pdi']:.3f}")
    """
    sizes = np.asarray(sizes)
    
    if len(sizes) == 0:
        raise ValueError("Size array cannot be empty")
    
    # Basic statistics
    mean_val = np.mean(sizes)
    std_val = np.std(sizes, ddof=1)  # Sample standard deviation
    median_val = np.median(sizes)
    min_val = np.min(sizes)
    max_val = np.max(sizes)
    count = len(sizes)
    
    # Percentiles
    d10 = np.percentile(sizes, 10)
    d50 = np.percentile(sizes, 50)
    d90 = np.percentile(sizes, 90)
    
    # Span (measure of distribution width)
    span = (d90 - d10) / d50 if d50 > 0 else 0
    
    # Number-average and weight-average diameters
    # D_n = ΣnᵢDᵢ / Σnᵢ = mean
    d_n = mean_val
    
    # D_w = ΣnᵢDᵢ2 / ΣnᵢDᵢ
    d_w = np.sum(sizes**2) / np.sum(sizes)
    
    # Polydispersity index
    pdi = d_w / d_n if d_n > 0 else 0
    
    # Coefficient of variation
    cv = (std_val / mean_val) * 100 if mean_val > 0 else 0
    
    return {
        'mean_nm': float(mean_val),
        'std_nm': float(std_val),
        'median_nm': float(median_val),
        'min_nm': float(min_val),
        'max_nm': float(max_val),
        'pdi': float(pdi),
        'span': float(span),
        'd10_nm': float(d10),
        'd50_nm': float(d50),
        'd90_nm': float(d90),
        'count': int(count),
        'cv_percent': float(cv),
        'number_avg_nm': float(d_n),
        'weight_avg_nm': float(d_w)
    }


def exciton_bohr_radius(
    dielectric_constant: float,
    m_e_star: float,
    m_h_star: float
) -> float:
    """
    Calculate the exciton Bohr radius for a semiconductor.
    
    Formula:
    a_B = ε x ħ2 / (mu x e2)
    
    Where mu = reduced mass = (m_e* x m_h*) / (m_e* + m_h*)
    
    This determines the size threshold for strong quantum confinement:
    - Strong confinement: particle size < a_B
    - Weak confinement: particle size > a_B
    
    Args:
        dielectric_constant: Relative dielectric constant
        m_e_star: Effective electron mass (in units of m_e)
        m_h_star: Effective hole mass (in units of m_e)
    
    Returns:
        Exciton Bohr radius in nm
    
    Example:
        >>> a_B = exciton_bohr_radius(9.7, 0.13, 0.45)
        >>> print(f"CdSe exciton Bohr radius: {a_B:.2f} nm")
    """
    # Reduced mass in kg
    m_e_kg = m_e_star * M_ELECTRON
    m_h_kg = m_h_star * M_ELECTRON
    mu = (m_e_kg * m_h_kg) / (m_e_kg + m_h_kg)
    
    # Bohr radius calculation
    # a_B = ε x 4piε0 x ħ2 / (mu x e2)
    a_B_m = dielectric_constant * 4 * np.pi * EPSILON_0 * H_BAR**2 / (mu * E_CHARGE**2)
    a_B_nm = a_B_m * 1e9
    
    return a_B_nm


# Convenience function for common quantum dots
def quantum_dot_emission_wavelength(
    material: str,
    diameter: float
) -> Dict[str, float]:
    """
    Quick calculation of emission wavelength for common quantum dot materials.
    
    Uses pre-calculated effective masses and dielectric constants.
    
    Args:
        material: "CdSe", "CdTe", "PbS", "PbSe", "InP", or "Si"
        diameter: Quantum dot diameter in nm
    
    Returns:
        Dictionary with bandgap and emission wavelength
    
    Example:
        >>> result = quantum_dot_emission_wavelength("CdSe", 5.0)
        >>> print(f"CdSe 5nm QD emits at {result['emission_nm']:.0f} nm")
    """
    # Material properties: (bulk_bandgap_eV, m_e*, m_h*, dielectric)
    materials = {
        "CdSe": (1.74, 0.13, 0.45, 9.7),
        "CdTe": (1.44, 0.11, 0.35, 10.2),
        "PbS":  (0.41, 0.09, 0.07, 17.0),
        "PbSe": (0.27, 0.07, 0.05, 23.0),
        "InP":  (1.35, 0.08, 0.60, 12.5),
        "Si":   (1.11, 0.19, 0.16, 11.7)
    }
    
    if material not in materials:
        raise ValueError(f"Unknown material: {material}. Available: {list(materials.keys())}")
    
    bulk_gap, m_e, m_h, eps = materials[material]
    
    result = quantum_confinement_energy(
        radius=diameter/2,
        m_e_star=m_e,
        m_h_star=m_h,
        bulk_bandgap=bulk_gap,
        dielectric_constant=eps
    )
    
    return {
        'material': material,
        'diameter_nm': diameter,
        'bandgap_eV': result['bandgap_eV'],
        'emission_nm': result['emission_wavelength_nm'],
        'bulk_bandgap_eV': bulk_gap
    }


if __name__ == "__main__":
    # Quick test examples
    print("=== Nanomaterials Tools Test ===\n")
    
    # Test quantum confinement
    print("1. CdSe Quantum Dot (5 nm diameter):")
    result = quantum_confinement_energy(2.5, 0.13, 0.45, 1.74, 9.7)
    print(f"   Bandgap: {result['bandgap_eV']:.2f} eV")
    print(f"   Emission: {result['emission_wavelength_nm']:.0f} nm\n")
    
    # Test surface area
    print("2. Au Nanoparticle (10 nm diameter):")
    result = nanoparticle_surface_area(10)
    print(f"   Surface area: {result['surface_area_nm2']:.1f} nm2")
    print(f"   S/V ratio: {result['surface_volume_ratio_nm_inv']:.3f} nm-1")
    print(f"   Surface atoms: {result['surface_atoms_percent']:.0f}%\n")
    
    # Test CNT properties
    print("3. CNT (10,10) Armchair:")
    result = cnt_electronic_properties(10, 10)
    print(f"   Type: {result['electronic_type']}")
    print(f"   Diameter: {result['diameter_nm']:.2f} nm")
    print(f"   Chiral angle: {result['chiral_angle_deg']:.1f}deg\n")
    
    # Test plasmon resonance
    print("4. Au Nanoparticle (20 nm):")
    result = plasmon_resonance("Au", 20)
    print(f"   LSPR: {result['wavelength_nm']:.0f} nm")
    print(f"   Color: {result['color']}\n")
    
    # Test size distribution
    print("5. Size Distribution:")
    sizes = np.array([8, 9, 10, 10, 11, 12, 10, 9, 11, 10])
    result = particle_size_distribution(sizes)
    print(f"   Mean: {result['mean_nm']:.1f} nm")
    print(f"   Std: {result['std_nm']:.2f} nm")
    print(f"   PDI: {result['pdi']:.3f}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="cnt_electronic_properties",
            description="Determine electronic properties of a carbon nanotube from chiral indices (n,m).",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="m", type="number", required=True),
            InputSchemaField(name="bond_length", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="exciton_bohr_radius",
            description="Calculate the exciton Bohr radius for a semiconductor.",
            input_schema=[
            InputSchemaField(name="dielectric_constant", type="number", required=True),
            InputSchemaField(name="m_e_star", type="number", required=True),
            InputSchemaField(name="m_h_star", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="nanoparticle_surface_area",
            description="Calculate surface area and surface-to-volume ratio for nanoparticles.",
            input_schema=[
            InputSchemaField(name="diameter", type="number", required=True),
            InputSchemaField(name="shape", type="number", required=False),
            InputSchemaField(name="units", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="particle_size_distribution",
            description="Calculate statistical parameters for nanoparticle size distribution.",
            input_schema=[
            InputSchemaField(name="sizes", type="number", required=True),
            InputSchemaField(name="weights", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="plasmon_resonance",
            description="Calculate surface plasmon resonance wavelength for metallic nanoparticles.",
            input_schema=[
            InputSchemaField(name="material", type="number", required=False),
            InputSchemaField(name="diameter", type="number", required=False),
            InputSchemaField(name="shape", type="number", required=False),
            InputSchemaField(name="dielectric_medium", type="number", required=False),
            InputSchemaField(name="units", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="quantum_confinement_energy",
            description="Calculate quantum confinement energy for semiconductor quantum dots.",
            input_schema=[
            InputSchemaField(name="radius", type="number", required=True),
            InputSchemaField(name="m_e_star", type="number", required=True),
            InputSchemaField(name="m_h_star", type="number", required=True),
            InputSchemaField(name="bulk_bandgap", type="number", required=True),
            InputSchemaField(name="dielectric_constant", type="number", required=True),
            InputSchemaField(name="units", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="quantum_dot_emission_wavelength",
            description="Quick calculation of emission wavelength for common quantum dot materials.",
            input_schema=[
            InputSchemaField(name="material", type="number", required=True),
            InputSchemaField(name="diameter", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
