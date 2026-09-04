"""
Liquid Properties Tools - L3 Implementation
Source: Averill, Ch11
## Solver Instructions (for AI Agent)

When you encounter liquid property problems (surface tension, viscosity, capillary action), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Capillary rise? Use `capillary_rise_height(surface_tension, contact_angle_deg, density, tube_radius, g=9.81)` - h = 2gammacosθ/(ρgr)
- Meniscus shape? Use `meniscus_shape(cohesive_strength, adhesive_strength)` - 'concave', 'convex', or 'flat'
- Order by viscosity? Use `viscosity_trend_comparison(substances_list)` - sorted lowest to highest
- Surface tension category? Use `surface_tension_prediction(imf_type, molecular_mass)`
- Viscosity at new temperature? Use `temperature_effect_on_viscosity(Ea, T1, T2, viscosity_T1)` - Arrhenius-type
- Work of adhesion? Use `work_of_adhesion(gamma_liquid, gamma_solid, gamma_interfacial)` - Dupre equation

### Step 2: Handle special cases
- **Capillary rise**: Positive = rise (wetting, θ < 90deg); Negative = depression (non-wetting, θ > 90deg)
- **Meniscus**: Adhesion > cohesion -> concave (water in glass); Cohesion > adhesion -> convex (Hg in glass)
- **Viscosity-temperature**: Viscosity decreases with temperature (Arrhenius: η = A·exp(Ea/RT))
- **Surface tension units**: N/m (SI) or mN/m; water at 20degC ~ 0.0728 N/m = 72.8 mN/m

### Examples
```python
# Example 1: Capillary rise for water in glass
capillary_rise_height(0.0728, 0, 1000, 0.001)  # -> ~0.0149 m (1.49 cm)

# Example 2: Viscosity change with temperature
temperature_effect_on_viscosity(20000, 293, 313, 1.0)  # -> ~0.603 (viscosity drops ~40%)

# Example 3: Meniscus prediction
meniscus_shape('weak', 'strong')  # -> 'concave' (water in glass)
meniscus_shape('strong', 'weak')  # -> 'convex' (mercury in glass)
```
"""

from typing import Dict, Tuple
import math


def capillary_rise_height(surface_tension: float, contact_angle_deg: float,
                          density: float, tube_radius: float,
                          g: float = 9.81) -> float:
    """
    Calculate capillary rise height.
    
    h = (2gamma cos θ) / (ρgr)
    
    Args:
        surface_tension: Surface tension in N/m
        contact_angle_deg: Contact angle in degrees
        density: Liquid density in kg/m3
        tube_radius: Tube radius in meters
        g: Gravitational acceleration (default 9.81 m/s2)
    
    Returns:
        Height in meters (positive = rise, negative = fall)
    
    Examples:
        >>> round(capillary_rise_height(0.0728, 0, 1000, 0.001), 4)
        0.0149
    """
    theta_rad = math.radians(contact_angle_deg)
    cos_theta = math.cos(theta_rad)
    
    # h = (2gamma cos θ) / (ρgr)
    h = (2 * surface_tension * cos_theta) / (density * g * tube_radius)
    return h


def meniscus_shape(cohesive_strength: str, adhesive_strength: str) -> str:
    """
    Predict meniscus shape based on cohesive vs adhesive forces.
    
    Args:
        cohesive_strength: 'weak', 'moderate', or 'strong'
        adhesive_strength: 'weak', 'moderate', or 'strong'
    
    Returns:
        'concave', 'convex', or 'flat'
    """
    strength_values = {'weak': 1, 'moderate': 2, 'strong': 3}
    coh = strength_values.get(cohesive_strength, 2)
    adh = strength_values.get(adhesive_strength, 2)
    
    if adh > coh:
        return 'concave'  # Liquid rises, curves up at edges
    elif coh > adh:
        return 'convex'   # Liquid falls, curves down at edges
    else:
        return 'flat'


def viscosity_trend_comparison(substances: list) -> list:
    """
    Order substances by viscosity (lowest to highest).
    
    Args:
        substances: List of dicts with:
            - name: substance name
            - imf_strength: 'weak', 'moderate', 'strong'
            - molecular_complexity: 1-5 scale
            - h_bond_sites: number of H-bond sites
    
    Returns:
        List of names in order of increasing viscosity
    """
    strength_values = {'weak': 1, 'moderate': 2, 'strong': 3}
    
    def viscosity_key(substance):
        imf = strength_values.get(substance.get('imf_strength', 'weak'), 1)
        complexity = substance.get('molecular_complexity', 1)
        h_bonds = substance.get('h_bond_sites', 0)
        return (imf, complexity, h_bonds)
    
    sorted_subs = sorted(substances, key=viscosity_key)
    return [s['name'] for s in sorted_subs]


def surface_tension_prediction(imf_type: str, molecular_mass: float) -> str:
    """
    Predict surface tension category.
    
    Args:
        imf_type: Dominant IMF type
        molecular_mass: Molecular mass in g/mol
    
    Returns:
        Surface tension category
    """
    imf_rank = {
        'london_dispersion': 1,
        'dipole_dipole': 2,
        'hydrogen_bonding': 3
    }
    
    rank = imf_rank.get(imf_type.lower(), 1)
    
    if rank >= 3 and molecular_mass < 50:
        return "Very high (like water)"
    elif rank >= 3:
        return "High"
    elif rank >= 2:
        return "Moderate"
    elif molecular_mass > 100:
        return "Moderate (large molecule)"
    else:
        return "Low"


def temperature_effect_on_viscosity(activation_energy: float, 
                                     T1: float, T2: float,
                                     viscosity_T1: float) -> float:
    """
    Calculate viscosity at new temperature using Arrhenius-type equation.
    
    η = A x exp(Ea/RT)
    
    Args:
        activation_energy: Activation energy for flow in J/mol
        T1: Initial temperature in K
        T2: New temperature in K
        viscosity_T1: Viscosity at T1 in mPa·s
    
    Returns:
        Viscosity at T2 in mPa·s
    
    Examples:
        >>> round(temperature_effect_on_viscosity(20000, 293, 313, 1.0), 3)
        0.603
    """
    R = 8.314  # J/(mol·K)
    
    # η2/η1 = exp(Ea/R x (1/T2 - 1/T1))
    ratio = math.exp(activation_energy / R * (1/T2 - 1/T1))
    return viscosity_T1 * ratio


def work_of_adhesion(surface_tension_liquid: float, 
                     surface_tension_solid: float,
                     interfacial_tension: float) -> float:
    """
    Calculate work of adhesion (Dupre equation).
    
    W_ad = gamma_L + gamma_S - gamma_LS
    
    Args:
        surface_tension_liquid: Liquid surface tension in mJ/m2
        surface_tension_solid: Solid surface tension in mJ/m2
        interfacial_tension: Liquid-solid interfacial tension in mJ/m2
    
    Returns:
        Work of adhesion in mJ/m2
    """
    return surface_tension_liquid + surface_tension_solid - interfacial_tension

MCP_TOOLS = [
    {
        "name": "capillary_rise_height",
        "description": "Calculate capillary rise height.",
        "parameters": [
            {
                "name": "surface_tension",
                "type": "number"
            },
            {
                "name": "contact_angle_deg",
                "type": "number"
            },
            {
                "name": "density",
                "type": "number"
            },
            {
                "name": "tube_radius",
                "type": "number"
            },
            {
                "name": "g",
                "type": "number"
            }
        ]
    },
    {
        "name": "meniscus_shape",
        "description": "Predict meniscus shape based on cohesive vs adhesive forces.",
        "parameters": [
            {
                "name": "cohesive_strength",
                "type": "number"
            },
            {
                "name": "adhesive_strength",
                "type": "number"
            }
        ]
    },
    {
        "name": "surface_tension_prediction",
        "description": "Predict surface tension category.",
        "parameters": [
            {
                "name": "imf_type",
                "type": "number"
            },
            {
                "name": "molecular_mass",
                "type": "number"
            }
        ]
    },
    {
        "name": "temperature_effect_on_viscosity",
        "description": "Calculate viscosity at new temperature using Arrhenius-type equation.",
        "parameters": [
            {
                "name": "activation_energy",
                "type": "number"
            },
            {
                "name": "T1",
                "type": "number"
            },
            {
                "name": "T2",
                "type": "number"
            },
            {
                "name": "viscosity_T1",
                "type": "number"
            }
        ]
    },
    {
        "name": "viscosity_trend_comparison",
        "description": "Order substances by viscosity (lowest to highest).",
        "parameters": [
            {
                "name": "substances",
                "type": "number"
            }
        ]
    },
    {
        "name": "work_of_adhesion",
        "description": "Calculate work of adhesion (Dupre equation).",
        "parameters": [
            {
                "name": "surface_tension_liquid",
                "type": "number"
            },
            {
                "name": "surface_tension_solid",
                "type": "number"
            },
            {
                "name": "interfacial_tension",
                "type": "number"
            }
        ]
    }
]
