"""
L3 Tool: Heterogeneous Catalysis Tools
Langmuir isotherm, BET surface area, LH/ER rate laws, catalyst metrics.

Source: LibreTexts Inorganic Chemistry (Haas), LibreTexts Catalysis Module, Physical Chemistry Ch29.8
Created: 2026-03-24 (Phase 2)
## Solver Instructions (for AI Agent)

When you encounter surface chemistry, adsorption isotherms, or catalysis problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Langmuir isotherm (surface coverage)? Use `langmuir_coverage(pressure, k_ads)` -> θ = KP/(1+KP)
- Dissociative adsorption? Use `langmuir_dissociative_coverage(pressure, k_ads)` -> θ = √(KP)/(1+√(KP))
- Langmuir-Hinshelwood rate? Use `lh_rate(p_a, p_b, k_a, k_b, k_rate)` - both reactants adsorbed
- Eley-Rideal rate? Use `er_rate(p_a, p_b, k_a, k_rate)` - only one reactant adsorbed
- BET surface area? Use `bet_surface_area(v_m, c, cross_section=0.162)` - v_m in cm3(STP)/g
- Crystallite size from XRD? Use `scherrer_crystallite_size(wavelength, fwhm, theta, k=0.9)` - D = Klambda/(betacosθ)
- Catalyst dispersion? Use `catalyst_dispersion(particle_diameter_nm, density_g_cm3, molar_mass)`

### Step 2: Handle special cases
- **Langmuir vs BET**: Langmuir = monolayer; BET = multilayer (N2 cross-section 0.162 nm2)
- **LH vs ER**: LH = both adsorbed (denominator squared); ER = one gas-phase (denominator linear)
- **Scherrer equation**: All angles in radians; K ~ 0.9 (shape factor)
- **Dispersion**: Fraction of surface atoms; smaller particles = higher dispersion

### Examples
```python
# Example 1: Langmuir coverage
langmuir_coverage(2.0, 0.5)  # -> θ = 0.5 (half coverage)

# Example 2: BET surface area
bet_surface_area(150, 200)  # -> ~652 m2/g (high surface area catalyst)

# Example 3: Scherrer crystallite size
scherrer_crystallite_size(0.154, 0.005, 0.5)  # -> D ~ 27.7 nm
```
"""

import math


def langmuir_coverage(pressure: float, k_ads: float) -> dict:
    """Calculate fractional surface coverage using Langmuir isotherm.
    
    θ = KP / (1 + KP)
    """
    if k_ads < 0 or pressure < 0:
        return {'error': 'K and P must be non-negative'}
    theta = (k_ads * pressure) / (1 + k_ads * pressure)
    return {'theta': round(theta, 6), 'K': k_ads, 'P': pressure}


def langmuir_dissociative_coverage(pressure: float, k_ads: float) -> dict:
    """Langmuir isotherm for dissociative adsorption (e.g., H2 on metal).
    
    θ = √(KP) / (1 + √(KP))
    """
    if k_ads < 0 or pressure < 0:
        return {'error': 'K and P must be non-negative'}
    sqkp = math.sqrt(k_ads * pressure)
    theta = sqkp / (1 + sqkp)
    return {'theta': round(theta, 6), 'K': k_ads, 'P': pressure}


def lh_rate(p_a: float, p_b: float, k_a: float, k_b: float, k_rate: float) -> dict:
    """Langmuir-Hinshelwood rate law for bimolecular surface reaction.
    
    r = k * Ka * Pa * Kb * Pb / (1 + Ka*Pa + Kb*Pb)^2
    """
    denom = (1 + k_a * p_a + k_b * p_b) ** 2
    if denom == 0:
        return {'error': 'Denominator is zero'}
    rate = k_rate * k_a * p_a * k_b * p_b / denom
    return {'rate': rate, 'Pa': p_a, 'Pb': p_b}


def er_rate(p_a: float, p_b: float, k_a: float, k_rate: float) -> dict:
    """Eley-Rideal rate law.
    
    r = k * Ka * Pa * Pb / (1 + Ka * Pa)
    """
    denom = 1 + k_a * p_a
    if denom == 0:
        return {'error': 'Denominator is zero'}
    rate = k_rate * k_a * p_a * p_b / denom
    return {'rate': rate, 'Pa': p_a, 'Pb': p_b}


def bet_surface_area(v_m: float, c: float, cross_section: float = 0.162) -> dict:
    """Calculate BET surface area from monolayer volume.
    
    A = Vm * Na * σ / Vmolar (using N2 cross-section 0.162 nm2)
    V_m in cm3(STP)/g
    """
    na = 6.022e23
    v_molar = 22414.0  # cm3/mol at STP
    sigma = cross_section * 1e-18  # nm2 to cm2 (no, actually need m2)
    # σ in nm2, convert: 1 nm2 = 1e-18 m2
    # A = Vm * Na * σ / Vmolar  [m2/g]
    area = v_m * na * (cross_section * 1e-18) / v_molar
    return {
        'surface_area_m2_g': round(area, 4),
        'v_m': v_m,
        'C': c,
        'sigma_nm2': cross_section
    }


def scherrer_crystallite_size(wavelength: float, fwhm: float, theta: float, k: float = 0.9) -> dict:
    """Crystallite size from XRD using Scherrer equation.
    
    D = Klambda / (beta cos θ)
    All angles in radians.
    """
    if fwhm <= 0 or math.cos(theta) <= 0:
        return {'error': 'Invalid parameters'}
    d = k * wavelength / (fwhm * math.cos(theta))
    return {'crystallite_size_nm': round(d, 4), 'lambda_nm': wavelength, 'FWHM_rad': fwhm, 'theta_rad': theta}


def catalyst_dispersion(particle_diameter_nm: float, density_g_cm3: float, molar_mass: float, atoms_per_area: float = 1.5e15) -> dict:
    """Calculate catalyst metal dispersion (fraction of surface atoms).
    
    D ~ 6*V_m / (d * N_s) where V_m = M/rho, d = particle diameter, N_s = surface atom density
    Simplified: D = 6*M / (d_cm * rho * Na * a_cross) where a_cross ~ 6.5e-20 m2
    For typical metals: D ~ 0.9 / d_nm (approximate for particles > 2 nm)
    """
    na = 6.022e23
    v_atom_cm3 = molar_mass / (density_g_cm3 * na)
    d_atom_nm = (v_atom_cm3 * 1e21) ** (1/3)
    dispersion = 6 * d_atom_nm / particle_diameter_nm
    dispersion = min(max(dispersion, 0.0), 1.0)
    return {'dispersion': round(dispersion, 4), 'd_nm': particle_diameter_nm}


TEXTBOOK_PROBLEMS = {
    "langmuir_basic": "Calculate θ when K=0.5 atm-1 and P=2 atm. θ = 0.5*2/(1+0.5*2) = 0.5",
    "lh_vs_er": "Compare LH and ER rates when both reactants have equal adsorption constants",
    "scherrer": "Calculate crystallite size: lambda=0.154 nm, FWHM=0.005 rad, θ=0.5 rad",
}

MCP_TOOLS = [
    {
        "name": "bet_surface_area",
        "description": "Calculate BET surface area from monolayer volume.",
        "parameters": [
            {
                "name": "v_m",
                "type": "number"
            },
            {
                "name": "c",
                "type": "number"
            },
            {
                "name": "cross_section",
                "type": "number"
            }
        ]
    },
    {
        "name": "catalyst_dispersion",
        "description": "Calculate catalyst metal dispersion (fraction of surface atoms).",
        "parameters": [
            {
                "name": "particle_diameter_nm",
                "type": "number"
            },
            {
                "name": "density_g_cm3",
                "type": "number"
            },
            {
                "name": "molar_mass",
                "type": "number"
            },
            {
                "name": "atoms_per_area",
                "type": "number"
            }
        ]
    },
    {
        "name": "er_rate",
        "description": "Eley-Rideal rate law.",
        "parameters": [
            {
                "name": "p_a",
                "type": "number"
            },
            {
                "name": "p_b",
                "type": "number"
            },
            {
                "name": "k_a",
                "type": "number"
            },
            {
                "name": "k_rate",
                "type": "number"
            }
        ]
    },
    {
        "name": "langmuir_coverage",
        "description": "Calculate fractional surface coverage using Langmuir isotherm.",
        "parameters": [
            {
                "name": "pressure",
                "type": "number"
            },
            {
                "name": "k_ads",
                "type": "number"
            }
        ]
    },
    {
        "name": "langmuir_dissociative_coverage",
        "description": "Langmuir isotherm for dissociative adsorption (e.g., H2 on metal).",
        "parameters": [
            {
                "name": "pressure",
                "type": "number"
            },
            {
                "name": "k_ads",
                "type": "number"
            }
        ]
    },
    {
        "name": "lh_rate",
        "description": "Langmuir-Hinshelwood rate law for bimolecular surface reaction.",
        "parameters": [
            {
                "name": "p_a",
                "type": "number"
            },
            {
                "name": "p_b",
                "type": "number"
            },
            {
                "name": "k_a",
                "type": "number"
            },
            {
                "name": "k_b",
                "type": "number"
            },
            {
                "name": "k_rate",
                "type": "number"
            }
        ]
    },
    {
        "name": "scherrer_crystallite_size",
        "description": "Crystallite size from XRD using Scherrer equation.",
        "parameters": [
            {
                "name": "wavelength",
                "type": "number"
            },
            {
                "name": "fwhm",
                "type": "number"
            },
            {
                "name": "theta",
                "type": "number"
            },
            {
                "name": "k",
                "type": "number"
            }
        ]
    }
]
