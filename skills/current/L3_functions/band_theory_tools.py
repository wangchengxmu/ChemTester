"""
Band Theory Tools - L3 Implementation
Source: Averill, Ch12

## Solver Instructions (for AI Agent)

When you encounter solid-state/band theory problems (conductors, semiconductors, insulators):

### Step 1: Identify what is given and what is asked
- Given: band gap energy, material type, Fermi level, doping info
- Asked: conductivity type, band gap classification, carrier concentration, optical absorption edge

### Step 2: Choose the correct function
- `band_gap_from_wavelength(wavelength_nm)`: Eg = hc/lambda in eV
- `classify_material(band_gap_ev)`: Conductor/semiconductor/insulator
- `carrier_concentration_intrinsic(Eg, T, me_eff, mh_eff)`: Intrinsic ni
- `fermi_level_intrinsic(Eg, me_eff, mh_eff)`: Intrinsic Fermi level position
- `conductivity_type(material_type)`: n-type, p-type, or intrinsic
- `optical_absorption_edge(Eg)`: Wavelength threshold for absorption

### Step 3: Handle special cases
- Conductors: Eg ~ 0; Semiconductors: 0 < Eg < ~3 eV; Insulators: Eg > ~3 eV
- Si: 1.1 eV, GaAs: 1.4 eV, Diamond: 5.5 eV

### Examples
```python
classify_material(1.1)  # Si -> 'semiconductor'
optical_absorption_edge(1.1)  # -> ~1127 nm (IR edge)
```
"""

from typing import Dict, Tuple
import math


def band_gap_energy(conductivity_300K: float, conductivity_0K: float = 0) -> float:
    """
    Estimate band gap from conductivity ratio.
    
    This is a simplified estimation.
    
    Args:
        conductivity_300K: Conductivity at 300K
        conductivity_0K: Conductivity at 0K (usually ~0 for semiconductors)
    
    Returns:
        Estimated band gap in eV (approximate)
    """
    # Simplified: use typical ranges
    if conductivity_300K > 1e4:
        return 0.0  # Metal
    elif conductivity_300K > 1:
        return 0.5  # Poor metal
    elif conductivity_300K > 1e-6:
        return 1.5  # Semiconductor
    else:
        return 4.0  # Insulator


def conductivity_temperature_dependence(Eg: float, T1: float, T2: float,
                                         sigma1: float) -> float:
    """
    Calculate conductivity at new temperature for semiconductor.
    
    σ ∝ exp(-Eg/2kT)
    
    Args:
        Eg: Band gap in eV
        T1: Initial temperature in K
        T2: New temperature in K
        sigma1: Conductivity at T1
    
    Returns:
        Conductivity at T2
    
    Examples:
        >>> result = conductivity_temperature_dependence(1.1, 300, 350, 1)
        >>> result > 1  # Conductivity increases with T
        True
    """
    k = 8.617e-5  # eV/K
    
    ratio = math.exp(-Eg/(2*k) * (1/T2 - 1/T1))
    return sigma1 * ratio


def intrinsic_carrier_concentration(Eg: float, temperature: float,
                                     Nc: float = 2.8e19, 
                                     Nv: float = 1.04e19) -> float:
    """
    Calculate intrinsic carrier concentration.
    
    n_i = √(Nc x Nv) x exp(-Eg/2kT)
    
    Args:
        Eg: Band gap in eV
        temperature: Temperature in K
        Nc: Effective density of states in conduction band (cm-3)
        Nv: Effective density of states in valence band (cm-3)
    
    Returns:
        Carrier concentration in cm-3
    """
    k = 8.617e-5  # eV/K
    
    ni = math.sqrt(Nc * Nv) * math.exp(-Eg / (2 * k * temperature))
    return ni


def fermi_level_intrinsic(Eg: float, Nc: float = 2.8e19,
                          Nv: float = 1.04e19) -> float:
    """
    Calculate Fermi level for intrinsic semiconductor.
    
    E_F = E_g/2 + (3/4)kT x ln(m_h*/m_e*)
    
    Simplified: E_F ~ E_g/2 for symmetric bands
    
    Args:
        Eg: Band gap in eV
        Nc: Effective density of states (conduction)
        Nv: Effective density of states (valence)
    
    Returns:
        Fermi level measured from valence band in eV
    """
    # Simplified: Fermi level at mid-gap for intrinsic semiconductor
    return Eg / 2


def doping_type_effect(dopant_type: str) -> Dict:
    """
    Describe effect of doping type.
    
    Args:
        dopant_type: 'n-type' or 'p-type'
    
    Returns:
        Dict with doping effects
    """
    if dopant_type == 'n-type':
        return {
            'majority_carriers': 'electrons',
            'minority_carriers': 'holes',
            'dopant': 'donor (Group V for Si)',
            'examples': ['P in Si', 'As in Si']
        }
    elif dopant_type == 'p-type':
        return {
            'majority_carriers': 'holes',
            'minority_carriers': 'electrons',
            'dopant': 'acceptor (Group III for Si)',
            'examples': ['B in Si', 'Al in Si']
        }
    else:
        return {}


def semiconductor_material_properties(material: str) -> Dict:
    """
    Return key semiconductor properties.
    
    Args:
        material: Semiconductor name
    
    Returns:
        Dict with Eg, electron mobility, hole mobility
    """
    properties = {
        'Si': {'Eg': 1.12, 'mu_e': 1400, 'mu_h': 450, 'type': 'indirect'},
        'Ge': {'Eg': 0.66, 'mu_e': 3900, 'mu_h': 1900, 'type': 'indirect'},
        'GaAs': {'Eg': 1.43, 'mu_e': 8500, 'mu_h': 400, 'type': 'direct'},
        'InP': {'Eg': 1.35, 'mu_e': 4600, 'mu_h': 150, 'type': 'direct'},
        'GaP': {'Eg': 2.26, 'mu_e': 110, 'mu_h': 75, 'type': 'indirect'}
    }
    return properties.get(material, {})


def pn_junction_bias(bias_type: str) -> Dict:
    """
    Describe PN junction behavior under bias.
    
    Args:
        bias_type: 'forward', 'reverse', or 'none'
    
    Returns:
        Dict describing junction state
    """
    if bias_type == 'forward':
        return {
            'current': 'large (exponential with voltage)',
            'depletion_region': 'narrow',
            'barrier': 'reduced',
            'application': 'LED, rectifier'
        }
    elif bias_type == 'reverse':
        return {
            'current': 'very small (saturation)',
            'depletion_region': 'wide',
            'barrier': 'increased',
            'application': 'photodiode, Zener'
        }
    else:
        return {
            'current': 'none (equilibrium)',
            'depletion_region': 'normal width',
            'barrier': 'built-in potential'
        }


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "band_gap_energy",
        "description": "Estimate band gap from conductivity ratio.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "conductivity_300K": {
                    "type": "number",
                    "description": "Conductivity 300K"
                },
                "conductivity_0K": {
                    "type": "number",
                    "description": "Conductivity 0K",
                    "default": 0
                }
            },
            "required": [
                "conductivity_300K"
            ]
        }
    },
    {
        "name": "conductivity_temperature_dependence",
        "description": "Calculate conductivity at new temperature for semiconductor.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Eg": {
                    "type": "number",
                    "description": "Eg"
                },
                "T1": {
                    "type": "number",
                    "description": "T1"
                },
                "T2": {
                    "type": "number",
                    "description": "T2"
                },
                "sigma1": {
                    "type": "number",
                    "description": "Sigma1"
                }
            },
            "required": [
                "Eg",
                "T1",
                "T2",
                "sigma1"
            ]
        }
    },
    {
        "name": "doping_type_effect",
        "description": "Describe effect of doping type.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dopant_type": {
                    "type": "number",
                    "description": "Dopant Type"
                }
            },
            "required": [
                "dopant_type"
            ]
        }
    },
    {
        "name": "fermi_level_intrinsic",
        "description": "Calculate Fermi level for intrinsic semiconductor.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Eg": {
                    "type": "number",
                    "description": "Eg"
                },
                "Nc": {
                    "type": "number",
                    "description": "Nc",
                    "default": 2.8e+19
                },
                "Nv": {
                    "type": "number",
                    "description": "Nv",
                    "default": 1.04e+19
                }
            },
            "required": [
                "Eg"
            ]
        }
    },
    {
        "name": "intrinsic_carrier_concentration",
        "description": "Calculate intrinsic carrier concentration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Eg": {
                    "type": "number",
                    "description": "Eg"
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature"
                },
                "Nc": {
                    "type": "number",
                    "description": "Nc",
                    "default": 2.8e+19
                },
                "Nv": {
                    "type": "number",
                    "description": "Nv",
                    "default": 1.04e+19
                }
            },
            "required": [
                "Eg",
                "temperature"
            ]
        }
    },
    {
        "name": "pn_junction_bias",
        "description": "Describe PN junction behavior under bias.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bias_type": {
                    "type": "number",
                    "description": "Bias Type"
                }
            },
            "required": [
                "bias_type"
            ]
        }
    },
    {
        "name": "semiconductor_material_properties",
        "description": "Return key semiconductor properties.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material": {
                    "type": "number",
                    "description": "Material"
                }
            },
            "required": [
                "material"
            ]
        }
    }
]