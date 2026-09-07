"""
Gibbs Free Energy Tools - L3 Implementation
Chapter 16.4: Free Energy

## Solver Instructions (for AI Agent)

When you encounter a Gibbs free energy problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- DeltaH (enthalpy change): Look for "kJ/mol", often from formation data or reaction
- DeltaS (entropy change): Look for "J/mol·K" - NOTE units are typically J, not kJ!
- T (temperature): Look for "K", "degC" -> convert to Kelvin (K = degC + 273.15)
- DeltaG: What you're often solving for
- Equilibrium constant K: May be given or asked for

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate DeltaG from DeltaH, DeltaS, T | `gibbs_free_energy(delta_H, delta_S, T)` |
| Determine spontaneity from DeltaG | `spontaneity_from_G(delta_G)` |
| Calculate DeltaGdeg from formation data | `gibbs_from_formation(products_list, reactants_list, delta_G_f_data)` |
| Find temperature at equilibrium | `equilibrium_temperature(delta_H, delta_S)` |
| Relate DeltaGdeg to equilibrium constant K | `gibbs_from_K(K, T)` or `K_from_gibbs(delta_G, T)` |
| Predict spontaneity from DeltaH, DeltaS signs | `predict_spontaneity(delta_H, delta_S)` |

### Step 3: Handle special cases
- **Unit conversion**: DeltaH is typically kJ/mol, but DeltaS is typically J/mol·K. Convert DeltaS to kJ before using: DeltaS(kJ) = DeltaS(J)/1000
- **Temperature dependence**: DeltaG = DeltaH - TDeltaS, so DeltaG changes with T
- **Equilibrium condition**: At equilibrium, DeltaG = 0, so T_eq = DeltaH/DeltaS (when both in same units)
- **K relationship**: DeltaGdeg = -RT ln K, or K = exp(-DeltaGdeg/RT)
- **Spontaneity rules**: DeltaG < 0 -> spontaneous; DeltaG > 0 -> non-spontaneous; DeltaG = 0 -> equilibrium

### Examples

**Example 1: Calculate DeltaG**
Question: "Calculate DeltaG for a reaction with DeltaH = 44.0 kJ/mol and DeltaS = 118.8 J/mol·K at 298 K."
- Given: DeltaH = 44.0 kJ/mol, DeltaS = 118.8 J/mol·K = 0.1188 kJ/mol·K, T = 298 K
- Solution: `gibbs_free_energy(delta_H=44.0, delta_S=118.8, T=298)` -> 8.6 kJ/mol (non-spontaneous)

**Example 2: Find equilibrium temperature**
Question: "At what temperature is a reaction with DeltaH = 50 kJ/mol and DeltaS = 100 J/mol·K at equilibrium?"
- Given: DeltaH = 50 kJ/mol, DeltaS = 100 J/mol·K
- Solution: T = DeltaH/DeltaS = 50000 J/mol / 100 J/mol·K = 500 K

**Example 3: DeltaGdeg from K**
Question: "Calculate DeltaGdeg for a reaction with K = 1.0 x 106 at 298 K."
- Given: K = 1.0e6, T = 298 K
- Solution: `gibbs_from_K(K=1e6, T=298)` -> ~ -34.2 kJ/mol
"""

from typing import Dict, Tuple, Optional
from math import exp, log


# Gas constant (J/mol·K)
R = 8.314

# Standard Gibbs free energies of formation (kJ/mol) at 298 K
# Keys: (formula, phase) where phase is 'g', 'l', 's', or 'aq'
# IMPORTANT: Phase matters! E.g., CH3OH(l) = -166.3 vs CH3OH(g) = -162.0
STANDARD_GF_DATA = {
    # Common species - gas phase
    ('CO2', 'g'): -394.4,
    ('H2O', 'g'): -228.6,
    ('H2O', 'l'): -237.1,
    ('O2', 'g'): 0.0,
    ('H2', 'g'): 0.0,
    ('N2', 'g'): 0.0,
    ('Cl2', 'g'): 0.0,
    ('CO', 'g'): -137.2,
    ('NH3', 'g'): -16.4,
    ('NO', 'g'): 87.6,
    ('NO2', 'g'): 51.3,
    ('SO2', 'g'): -300.1,
    ('SO3', 'g'): -371.1,
    ('CH4', 'g'): -50.5,
    ('C2H6', 'g'): -32.0,
    ('C2H4', 'g'): 68.4,
    ('C2H2', 'g'): 209.2,
    # Methanol - phase matters!
    ('CH3OH', 'g'): -162.0,
    ('CH3OH', 'l'): -166.3,
    ('CH3OH', 'aq'): -175.2,
    # Dimethyl ether
    ('(CH3)2O', 'g'): -156.5,
    # Ethanol
    ('C2H5OH', 'g'): -168.5,
    ('C2H5OH', 'l'): -174.8,
    # Solid species
    ('C', 's'): 0.0,  # graphite
    ('Fe', 's'): 0.0,
    ('NaCl', 's'): -384.1,
    ('CaCO3', 's'): -735.6,
    ('CaO', 's'): -603.3,
    # Aqueous ions
    ('H+', 'aq'): 0.0,
    ('OH-', 'aq'): -157.2,
    ('Na+', 'aq'): -261.9,
    ('Cl-', 'aq'): -131.2,
}


def lookup_Gf(species: str, phase: str = 'g') -> float:
    """
    Look up standard Gibbs free energy of formation.
    
    Args:
        species: Chemical formula
        phase: Phase state ('g', 'l', 's', 'aq'), default 'g'
    
    Returns:
        DeltaG_f° in kJ/mol
    
    Raises:
        ValueError if species not found
    
    Note:
        Always specify the correct phase! Using wrong phase gives wrong results.
        E.g., CH3OH(l) has Gf = -166.3, not -162.0 (gas).
    """
    key = (species, phase)
    if key in STANDARD_GF_DATA:
        return STANDARD_GF_DATA[key]
    raise ValueError(f"No Gf data for {species} ({phase}). Available: {list(STANDARD_GF_DATA.keys())}")


def gibbs_free_energy(delta_H: float, delta_S: float, T: float) -> float:
    """
    Calculate Gibbs free energy change.
    
    DeltaG = DeltaH - TDeltaS
    
    Args:
        delta_H: Enthalpy change (kJ/mol)
        delta_S: Entropy change (J/mol·K)
        T: Temperature (K)
    
    Returns:
        Gibbs free energy change (kJ/mol)
    
    Examples:
        >>> gibbs_free_energy(44.0, 118.8, 298)
        8.6
    """
    # Convert delta_S from J/mol·K to kJ/mol·K
    delta_S_kJ = delta_S / 1000.0
    return delta_H - T * delta_S_kJ


def spontaneity_from_G(delta_G: float) -> str:
    """
    Determine spontaneity from DeltaG.
    
    Args:
        delta_G: Gibbs free energy change (kJ/mol)
    
    Returns:
        Spontaneity prediction
    
    Examples:
        >>> spontaneity_from_G(-10.0)
        'spontaneous (forward)'
        >>> spontaneity_from_G(10.0)
        'nonspontaneous (reverse spontaneous)'
    """
    if delta_G < 0:
        return 'spontaneous (forward)'
    elif delta_G > 0:
        return 'nonspontaneous (reverse spontaneous)'
    else:
        return 'at equilibrium'


def standard_G_from_formation(Gf_products: list, Gf_reactants: list,
                               coeffs_products: list = None,
                               coeffs_reactants: list = None) -> float:
    """
    Calculate standard free energy change from formation values.
    
    DeltaGdeg = ΣνDeltaG_fdeg(products) - ΣνDeltaG_fdeg(reactants)
    
    Args:
        Gf_products: List of DeltaG_fdeg for products (kJ/mol)
        Gf_reactants: List of DeltaG_fdeg for reactants (kJ/mol)
        coeffs_products: Stoichiometric coefficients for products
        coeffs_reactants: Stoichiometric coefficients for reactants
    
    Returns:
        Standard free energy change (kJ/mol)
    
    Examples:
        >>> standard_G_from_formation([0, 0], [-58.43], [1, 0.5], [1])
        58.43
    """
    if coeffs_products is None:
        coeffs_products = [1] * len(Gf_products)
    if coeffs_reactants is None:
        coeffs_reactants = [1] * len(Gf_reactants)
    
    sum_products = sum(c * g for c, g in zip(coeffs_products, Gf_products))
    sum_reactants = sum(c * g for c, g in zip(coeffs_reactants, Gf_reactants))
    
    return sum_products - sum_reactants


def equilibrium_constant_from_G(delta_G: float, T: float = 298.15) -> float:
    """
    Calculate equilibrium constant from standard free energy change.
    
    DeltaGdeg = -RT ln K
    K = e^(-DeltaGdeg/RT)
    
    Args:
        delta_G: Standard free energy change (kJ/mol)
        T: Temperature (K)
    
    Returns:
        Equilibrium constant K
    
    Examples:
        >>> equilibrium_constant_from_G(-5.7, 298)
        10.0
    """
    # Convert delta_G from kJ/mol to J/mol
    delta_G_J = delta_G * 1000.0
    return exp(-delta_G_J / (R * T))


def G_from_equilibrium_constant(K: float, T: float = 298.15) -> float:
    """
    Calculate standard free energy change from equilibrium constant.
    
    DeltaGdeg = -RT ln K
    
    Args:
        K: Equilibrium constant
        T: Temperature (K)
    
    Returns:
        Standard free energy change (kJ/mol)
    
    Examples:
        >>> G_from_equilibrium_constant(1000, 298)
        -17.1
    """
    if K <= 0:
        raise ValueError("K must be positive")
    delta_G_J = -R * T * log(K)
    return delta_G_J / 1000.0  # Convert to kJ/mol


def temperature_spontaneity_range(delta_H: float, delta_S: float) -> Dict:
    """
    Determine temperature range for spontaneity.
    
    Args:
        delta_H: Enthalpy change (kJ/mol)
        delta_S: Entropy change (J/mol·K)
    
    Returns:
        Dict with temperature range info
    
    Examples:
        >>> temperature_spontaneity_range(-90.0, -200.0)
        {'low_T': 'spontaneous', 'high_T': 'nonspontaneous', 'crossover_T': 450.0}
    """
    # Convert delta_S from J/mol·K to kJ/mol·K
    delta_S_kJ = delta_S / 1000.0
    
    # Crossover temperature where DeltaG = 0
    # DeltaG = 0 = DeltaH - TDeltaS -> T = DeltaH/DeltaS
    crossover_T = None
    
    if delta_S != 0:
        crossover_T = abs(delta_H / delta_S_kJ)
    
    # Determine behavior
    if delta_H < 0 and delta_S > 0:
        return {'low_T': 'spontaneous', 'high_T': 'spontaneous', 'crossover_T': None, 'always': 'spontaneous'}
    elif delta_H < 0 and delta_S < 0:
        return {'low_T': 'spontaneous', 'high_T': 'nonspontaneous', 'crossover_T': crossover_T}
    elif delta_H > 0 and delta_S > 0:
        return {'low_T': 'nonspontaneous', 'high_T': 'spontaneous', 'crossover_T': crossover_T}
    else:  # delta_H > 0 and delta_S < 0
        return {'low_T': 'nonspontaneous', 'high_T': 'nonspontaneous', 'crossover_T': None, 'always': 'nonspontaneous'}


def maximum_work(delta_G: float) -> float:
    """
    Calculate maximum useful work from a spontaneous process.
    
    w_max = DeltaG (for spontaneous process)
    
    Args:
        delta_G: Gibbs free energy change (kJ/mol)
    
    Returns:
        Maximum useful work (kJ/mol)
    
    Examples:
        >>> maximum_work(-100.0)
        -100.0
    """
    return delta_G

MCP_TOOLS = [
    {
        "name": "G_from_equilibrium_constant",
        "description": "Calculate standard free energy change from equilibrium constant.",
        "parameters": [
            {
                "name": "K",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "equilibrium_constant_from_G",
        "description": "Calculate equilibrium constant from standard free energy change.",
        "parameters": [
            {
                "name": "delta_G",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "gibbs_free_energy",
        "description": "Calculate Gibbs free energy change.",
        "parameters": [
            {
                "name": "delta_H",
                "type": "number"
            },
            {
                "name": "delta_S",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "maximum_work",
        "description": "Calculate maximum useful work from a spontaneous process.",
        "parameters": [
            {
                "name": "delta_G",
                "type": "number"
            }
        ]
    },
    {
        "name": "spontaneity_from_G",
        "description": "Determine spontaneity from DeltaG.",
        "parameters": [
            {
                "name": "delta_G",
                "type": "number"
            }
        ]
    },
    {
        "name": "standard_G_from_formation",
        "description": "Calculate standard free energy change from formation values.",
        "parameters": [
            {
                "name": "Gf_products",
                "type": "number"
            },
            {
                "name": "Gf_reactants",
                "type": "number"
            },
            {
                "name": "coeffs_products",
                "type": "number"
            },
            {
                "name": "coeffs_reactants",
                "type": "number"
            }
        ]
    },
    {
        "name": "temperature_spontaneity_range",
        "description": "Determine temperature range for spontaneity.",
        "parameters": [
            {
                "name": "delta_H",
                "type": "number"
            },
            {
                "name": "delta_S",
                "type": "number"
            }
        ]
    }
]
