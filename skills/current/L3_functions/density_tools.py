"""Density and specific gravity calculation tools."""

from __future__ import annotations

from typing import Optional


def calculate_density(mass: float, volume: float) -> float:
    """Calculate density (g/mL or g/cm3) from mass (g) and volume (mL).
## Solver Instructions (for AI Agent)

When you encounter density/specific gravity/buoyancy problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Given**: mass and volume, or density and one of mass/volume, or specific gravity
- **Asked**: density, mass, volume, specific gravity, buoyancy-corrected mass

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Calculate density | `calculate_density(mass, volume)` | mass (g), volume (mL) |
| Mass from density | `mass_from_density(density, volume)` | ρ, V |
| Volume from density | `volume_from_density(density, mass)` | ρ, m |
| Buoyancy correction | `buoyancy_correction(mass_air, density_sample, density_air, density_weights)` | measured mass, ρ_sample |
| Specific gravity | `calculate_specific_gravity(density, reference_density)` | ρ, ref ρ (default 1.0) |

### Step 3: Handle special cases
- SG is dimensionless; default reference = water at 4degC (1.0 g/mL)
- Buoyancy correction: true mass > mass measured in air
- All units: g and mL (or g/cm3)

### Examples
1. **Density**: `calculate_density(50.0, 25.0)` -> 2.0 g/mL
2. **SG of Hg**: `calculate_specific_gravity(13.6)` -> 13.6
3. **Buoyancy**: `buoyancy_correction(10.0, 1.0)` -> ~10.0015 g


    Args:
        mass: Mass in grams.
        volume: Volume in mL.

    Returns:
        Density in g/mL.

    Raises:
        ValueError: If volume is zero or negative.
    """
    if volume == 0:
        raise ValueError("Volume cannot be zero.")
    if volume < 0:
        raise ValueError("Volume cannot be negative.")
    return mass / volume


def mass_from_density(density: float, volume: float) -> float:
    """Calculate mass from density and volume.

    Args:
        density: Density in g/mL.
        volume: Volume in mL.

    Returns:
        Mass in grams.

    Raises:
        ValueError: If volume is negative.
    """
    if volume < 0:
        raise ValueError("Volume cannot be negative.")
    return density * volume


def volume_from_density(density: float, mass: float) -> float:
    """Calculate volume from density and mass.

    Args:
        density: Density in g/mL.
        mass: Mass in grams.

    Returns:
        Volume in mL.

    Raises:
        ValueError: If density is zero or negative.
    """
    if density == 0:
        raise ValueError("Density cannot be zero.")
    if density < 0:
        raise ValueError("Density cannot be negative.")
    return mass / density


def buoyancy_correction(mass_air: float, density_sample: float,
                        density_air: float = 0.0012,
                        density_weights: float = 8.0) -> float:
    """Apply air buoyancy correction to a mass measurement.

    Corrects for the buoyant force of air on both the sample and the weights.

    m_true = m_air * (1 - ρ_air/ρ_weights) / (1 - ρ_air/ρ_sample)

    Args:
        mass_air: Mass measured in air (g).
        density_sample: Density of the sample (g/mL).
        density_air: Density of air (g/mL), default 0.0012.
        density_weights: Density of calibration weights (g/mL), default 8.0.

    Returns:
        True (corrected) mass in grams.

    Raises:
        ValueError: If density_sample or density_weights is zero.
    """
    if density_sample == 0:
        raise ValueError("density_sample cannot be zero.")
    if density_weights == 0:
        raise ValueError("density_weights cannot be zero.")
    return mass_air * (1 - density_air / density_weights) / (1 - density_air / density_sample)


def calculate_specific_gravity(density: float, reference_density: float = 1.0) -> float:
    """Calculate specific gravity (dimensionless).

    Args:
        density: Density of substance (g/mL).
        reference_density: Reference density (default 1.0 g/mL for water at 4degC).

    Returns:
        Specific gravity (dimensionless ratio).

    Raises:
        ValueError: If reference_density is zero.
    """
    if reference_density == 0:
        raise ValueError("reference_density cannot be zero.")
    return density / reference_density


# ── Tests ───────────────────────────────────────────────────────────────────

def test_calculate_density():
    assert abs(calculate_density(10.0, 2.0) - 5.0) < 1e-10
    assert abs(calculate_density(0.0, 5.0) - 0.0) < 1e-10


def test_mass_from_density():
    assert abs(mass_from_density(5.0, 2.0) - 10.0) < 1e-10
    assert abs(mass_from_density(0.0, 10.0) - 0.0) < 1e-10


def test_volume_from_density():
    assert abs(volume_from_density(5.0, 10.0) - 2.0) < 1e-10


def test_buoyancy_correction():
    # With equal densities, correction is small but nonzero
    corrected = buoyancy_correction(10.0, 1.0)
    assert corrected > 10.0  # true mass > measured in air
    # Check round-trip sanity
    assert abs(corrected - 10.0015) < 0.01


def test_specific_gravity():
    assert abs(calculate_specific_gravity(13.6, 1.0) - 13.6) < 1e-10
    assert abs(calculate_specific_gravity(1.0, 1.0) - 1.0) < 1e-10
    assert abs(calculate_specific_gravity(0.8) - 0.8) < 1e-10


def test_zero_division_errors():
    import pytest
    with pytest.raises(ValueError):
        calculate_density(1.0, 0.0)
    with pytest.raises(ValueError):
        volume_from_density(0.0, 1.0)
    with pytest.raises(ValueError):
        buoyancy_correction(1.0, 0.0)
    with pytest.raises(ValueError):
        calculate_specific_gravity(1.0, 0.0)


# ── Main demo ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Density Tools Demo ===")
    print(f"Density of 50g in 25mL: {calculate_density(50.0, 25.0)} g/mL")
    print(f"Mass of ρ=1.2 g/mL, V=100mL: {mass_from_density(1.2, 100.0)} g")
    print(f"Volume of ρ=2.0 g/mL, m=20g: {volume_from_density(2.0, 20.0)} mL")
    print(f"SG of mercury (ρ=13.6): {calculate_specific_gravity(13.6)}")
    print(f"Buoyancy-corrected mass (10g, ρ=1.0): {buoyancy_correction(10.0, 1.0):.6f} g")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'buoyancy_correction', 'description': 'Apply air buoyancy correction to a mass measurement.\n\nCorrects for the buoyant force of air on both the sample and the weights.\n\nm_true = m_air * (1 - ρ_air/ρ_weights) / (1 - ρ_air/ρ_sample)\n\nArgs:\n    mass_air: Mass measured in air (g).\n    density_sample: Density of the sample (g/mL).\n    density_air: Density of air (g/mL), default 0.0012.\n    density_weights: Density of calibration weights (g/mL), default 8.0.\n\nReturns:\n    true (corrected) mass in grams.\n\nRaises:\n    ValueError: If density_sample or density_weights is zero.', 'inputSchema': {'type': 'object', 'properties': {'mass_air': {'type': 'number', 'description': 'Mass Air'}, 'density_sample': {'type': 'string', 'description': 'Density Sample'}, 'density_air': {'type': 'number', 'description': 'Density Air', 'default': 0.0012}, 'density_weights': {'type': 'number', 'description': 'Density Weights', 'default': 8.0}}, 'required': ['mass_air', 'density_sample']}},
    {'name': 'calculate_density', 'description': 'Calculate density (g/mL or g/cm3) from mass (g) and volume (mL).\n\nArgs:\n    mass: Mass in grams.\n    volume: Volume in mL.\n\nReturns:\n    Density in g/mL.\n\nRaises:\n    ValueError: If volume is zero or negative.', 'inputSchema': {'type': 'object', 'properties': {'mass': {'type': 'number', 'description': 'Mass'}, 'volume': {'type': 'number', 'description': 'Volume'}}, 'required': ['mass', 'volume']}},
    {'name': 'calculate_specific_gravity', 'description': 'Calculate specific gravity (dimensionless).\n\nArgs:\n    density: Density of substance (g/mL).\n    reference_density: Reference density (default 1.0 g/mL for water at 4degC).\n\nReturns:\n    Specific gravity (dimensionless ratio).\n\nRaises:\n    ValueError: If reference_density is zero.', 'inputSchema': {'type': 'object', 'properties': {'density': {'type': 'number', 'description': 'Density'}, 'reference_density': {'type': 'string', 'description': 'Reference Density', 'default': 1.0}}, 'required': ['density']}},
    {'name': 'mass_from_density', 'description': 'Calculate mass from density and volume.\n\nArgs:\n    density: Density in g/mL.\n    volume: Volume in mL.\n\nReturns:\n    Mass in grams.\n\nRaises:\n    ValueError: If volume is negative.', 'inputSchema': {'type': 'object', 'properties': {'density': {'type': 'number', 'description': 'Density'}, 'volume': {'type': 'number', 'description': 'Volume'}}, 'required': ['density', 'volume']}},
    {'name': 'test_buoyancy_correction', 'description': 'test_buoyancy_correction', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_calculate_density', 'description': 'test_calculate_density', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_mass_from_density', 'description': 'test_mass_from_density', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_specific_gravity', 'description': 'test_specific_gravity', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_volume_from_density', 'description': 'test_volume_from_density', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'test_zero_division_errors', 'description': 'test_zero_division_errors', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'volume_from_density', 'description': 'Calculate volume from density and mass.\n\nArgs:\n    density: Density in g/mL.\n    mass: Mass in grams.\n\nReturns:\n    Volume in mL.\n\nRaises:\n    ValueError: If density is zero or negative.', 'inputSchema': {'type': 'object', 'properties': {'density': {'type': 'number', 'description': 'Density'}, 'mass': {'type': 'number', 'description': 'Mass'}}, 'required': ['density', 'mass']}}
]
