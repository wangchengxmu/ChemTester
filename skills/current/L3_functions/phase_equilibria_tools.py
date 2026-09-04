"""
Phase Equilibria Tools - L3 Implementation

Core functions for phase equilibria calculations:
- Clausius-Clapeyron equation
- Clapeyron equation
- Gibbs phase rule
- Phase boundary calculations
- Critical point properties
- Vapor pressure calculations

Source: LibreTexts Physical Chemistry Ch23, Averill Ch11

## Solver Instructions (for AI Agent)

When you encounter phase equilibria problems (vapor pressure, phase transitions, critical points), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given T1, P1, T2, DeltaHvap -> calculate P2 (Clausius-Clapeyron)?
- Given T1, P1, P2, DeltaHvap -> calculate T2?
- Given T1, P1, T2, P2 -> calculate DeltaHvap?
- Given DeltaH, DeltaV, T -> calculate dP/dT (Clapeyron equation)?
- Given components and phases -> calculate degrees of freedom (phase rule)?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Vapor pressure at T2 | `clausius_clapeyron_vapor_pressure(T1, P1, T2, delta_H_vap)` | Returns P2 |
| Temperature at P2 | `clausius_clapeyron_temperature(T1, P1, P2, delta_H_vap)` | Returns T2 |
| Calculate DeltaHvap | `clausius_clapeyron_enthalpy(T1, P1, T2, P2)` | Returns DeltaHvap in J/mol |
| Clapeyron dP/dT | `clapeyron_dp_dt(delta_H, delta_V, T)` | dP/dT = DeltaH/(T·DeltaV) |
| Gibbs phase rule | `gibbs_phase_rule(components, phases)` | F = C - P + 2 |
| Critical from VDW | `critical_point_from_vdw(a, b)` | Returns Tc, Pc, Vc |

### Step 3: Handle special cases
- Clausius-Clapeyron: assumes DeltaHvap constant and DeltaV ~ Vgas (valid for vaporization)
- Clapeyron: exact equation for any phase transition (solid-liquid, solid-solid)
- Critical point: above Tc, liquid and gas phases are indistinguishable

### Examples
```python
# Example 1: Vapor pressure at different temperature
clausius_clapeyron_vapor_pressure(373, 1, 298, 40700)  # Water: 100degC->25degC
# -> ~0.031 atm

# Example 2: Temperature for given vapor pressure
clausius_clapeyron_temperature(373, 1, 0.5, 40700)  # Water: P=0.5 atm
# -> ~354 K

# Example 3: Enthalpy of vaporization
clausius_clapeyron_enthalpy(373, 1, 353, 0.467)  # Water at 80degC
# -> ~41 kJ/mol

# Example 4: Gibbs phase rule
gibbs_phase_rule(1, 3)  # Water at triple point
# -> F = 0
```
"""

import math
from typing import Tuple, List, Union, Optional, Dict
import numpy as np
from scipy import constants
from scipy.optimize import brentq

# Physical constants
R = 8.314462618  # J/(mol·K)
R_kPa = 8.314462618e-3  # kPa·L/(mol·K)
ATM_TO_PA = 101325


# =============================================================================
# CLAUSIUS-CLAPEYRON EQUATION
# =============================================================================

def clausius_clapeyron_vapor_pressure(
    T1: float, P1: float,
    T2: float,
    delta_H_vap: float
) -> float:
    """
    Calculate vapor pressure at a different temperature using Clausius-Clapeyron.
    
    ln(P2/P1) = -DeltaH_vap/R x (1/T2 - 1/T1)
    
    Args:
        T1: Reference temperature in K
        P1: Vapor pressure at T1 (any units)
        T2: Target temperature in K
        delta_H_vap: Enthalpy of vaporization in J/mol
    
    Returns:
        P2: Vapor pressure at T2 (same units as P1)
    
    Example:
        >>> # Water at 373 K has P = 1 atm
        >>> # Find P at 298 K with DeltaH_vap = 40.7 kJ/mol
        >>> clausius_clapeyron_vapor_pressure(373, 1, 298, 40700)
        0.031...  # atm
    """
    ln_P2_P1 = -delta_H_vap / R * (1/T2 - 1/T1)
    return P1 * np.exp(ln_P2_P1)


def clausius_clapeyron_temperature(
    T1: float, P1: float,
    P2: float,
    delta_H_vap: float
) -> float:
    """
    Calculate temperature at a different vapor pressure.
    
    Args:
        T1: Reference temperature in K
        P1: Vapor pressure at T1
        P2: Target vapor pressure
        delta_H_vap: Enthalpy of vaporization in J/mol
    
    Returns:
        T2: Temperature in K
    
    Example:
        >>> # At what T does water have P = 0.5 atm?
        >>> clausius_clapeyron_temperature(373, 1, 0.5, 40700)
        354...  # K
    """
    # 1/T2 = 1/T1 - R/DeltaH_vap x ln(P2/P1)
    inv_T2 = 1/T1 - R/delta_H_vap * np.log(P2/P1)
    return 1 / inv_T2


def clausius_clapeyron_enthalpy(
    T1: float, P1: float,
    T2: float, P2: float
) -> float:
    """
    Calculate enthalpy of vaporization from two vapor pressure points.
    
    DeltaH_vap = -R x ln(P2/P1) / (1/T2 - 1/T1)
    
    Args:
        T1, T2: Temperatures in K
        P1, P2: Vapor pressures (same units)
    
    Returns:
        DeltaH_vap in J/mol
    
    Example:
        >>> # Water: P = 1 atm at 373 K, P = 0.031 atm at 298 K
        >>> clausius_clapeyron_enthalpy(373, 1, 298, 0.031)
        40700...  # J/mol
    """
    delta_H = -R * np.log(P2/P1) / (1/T2 - 1/T1)
    return delta_H


def normal_boiling_point(
    delta_H_vap: float,
    vapor_pressure_at_T: Tuple[float, float]
) -> float:
    """
    Calculate normal boiling point from vapor pressure data.
    
    Args:
        delta_H_vap: Enthalpy of vaporization in J/mol
        vapor_pressure_at_T: (T, P) at a known point
    
    Returns:
        Normal boiling point in K (where P = 1 atm = 101325 Pa)
    
    Example:
        >>> normal_boiling_point(40700, (298, 3170))  # Water data
        373...
    """
    T1, P1 = vapor_pressure_at_T
    P_normal = ATM_TO_PA  # 1 atm in Pa
    
    return clausius_clapeyron_temperature(T1, P1, P_normal, delta_H_vap)


def vapor_pressure_antione(A: float, B: float, C: float, T: float) -> float:
    """
    Calculate vapor pressure using Antoine equation.
    
    log10(P) = A - B/(T + C)
    
    Args:
        A, B, C: Antoine coefficients
        T: Temperature (typically degC, check coefficient units)
    
    Returns:
        Vapor pressure (typically mmHg or kPa, check coefficient units)
    
    Note:
        Antoine coefficients are tabulated with specific units.
        Common conventions:
        - T in degC, P in mmHg
        - T in degC, P in kPa
        Always check the source of coefficients!
    
    Example:
        >>> # Water: A=8.07131, B=1730.63, C=233.426 (T in degC, P in mmHg)
        >>> vapor_pressure_antione(8.07131, 1730.63, 233.426, 100)
        760...  # mmHg at 100degC
    """
    log_P = A - B / (T + C)
    return 10**log_P


def temperature_from_antione(A: float, B: float, C: float, P: float) -> float:
    """
    Calculate temperature from vapor pressure using Antoine equation.
    
    T = B/(A - log10(P)) - C
    
    Args:
        A, B, C: Antoine coefficients
        P: Vapor pressure (check coefficient units)
    
    Returns:
        Temperature (typically degC)
    """
    return B / (A - np.log10(P)) - C


# =============================================================================
# CLAPEYRON EQUATION (General Phase Boundaries)
# =============================================================================

def clapeyron_slope(
    delta_H: float,
    delta_V: float,
    T: float
) -> float:
    """
    Calculate slope of phase boundary using Clapeyron equation.
    
    dP/dT = DeltaH/(T·DeltaV)
    
    Args:
        delta_H: Enthalpy of transition in J/mol
        delta_V: Volume change of transition in m3/mol
        T: Transition temperature in K
    
    Returns:
        dP/dT in Pa/K
    
    Example:
        >>> # Water ice I -> liquid at 273 K
        >>> # DeltaH = 6008 J/mol, DeltaV = -1.63e-6 m3/mol
        >>> clapeyron_slope(6008, -1.63e-6, 273)
        -1.35e7  # Pa/K (negative slope!)
    """
    return delta_H / (T * delta_V)


def clapeyron_pressure_change(
    delta_H: float,
    delta_V: float,
    T: float,
    delta_T: float
) -> float:
    """
    Calculate pressure change for a temperature change along phase boundary.
    
    DeltaP ~ DeltaH/(T·DeltaV) x DeltaT
    
    Args:
        delta_H: Enthalpy of transition in J/mol
        delta_V: Volume change in m3/mol
        T: Transition temperature in K
        delta_T: Temperature change in K
    
    Returns:
        Pressure change in Pa
    
    Example:
        >>> # Ice melting point change per degree
        >>> clapeyron_pressure_change(6008, -1.63e-6, 273, 1)
        -1.35e7  # Pa/K
    """
    return clapeyron_slope(delta_H, delta_V, T) * delta_T


def melting_point_pressure_dependence(
    T_melt: float,
    delta_H_fus: float,
    rho_solid: float,
    rho_liquid: float,
    M: float
) -> float:
    """
    Calculate how melting point changes with pressure.
    
    dT/dP = T·DeltaV/DeltaH
    
    Args:
        T_melt: Normal melting point in K
        delta_H_fus: Enthalpy of fusion in J/mol
        rho_solid: Solid density in kg/m3
        rho_liquid: Liquid density in kg/m3
        M: Molar mass in kg/mol
    
    Returns:
        dT/dP in K/Pa (how much melting point shifts per unit pressure)
    
    Example:
        >>> # Water: Tm = 273 K, DeltaH = 6008 J/mol
        >>> # ρ_solid = 917 kg/m3, ρ_liquid = 1000 kg/m3, M = 0.018 kg/mol
        >>> melting_point_pressure_dependence(273, 6008, 917, 1000, 0.018)
        -7.4e-8  # K/Pa (melting point decreases with pressure!)
    """
    # Volume per mole: V = M/ρ
    V_solid = M / rho_solid
    V_liquid = M / rho_liquid
    delta_V = V_liquid - V_solid
    
    # dT/dP = T·DeltaV/DeltaH
    return T_melt * delta_V / delta_H_fus


# =============================================================================
# TRIPLE POINT CALCULATIONS
# =============================================================================

def triple_point_from_phase_boundaries(
    solid_liquid_params: Tuple[float, float, float],  # (T_ref, P_ref, dP_dT)
    liquid_gas_params: Tuple[float, float, float]
) -> Tuple[float, float]:
    """
    Estimate triple point from two phase boundary lines.
    
    Assumes linear phase boundaries near intersection.
    
    Args:
        solid_liquid_params: (T_ref, P_ref, dP/dT) for s-l line
        liquid_gas_params: (T_ref, P_ref, dP/dT) for l-g line
    
    Returns:
        (T_triple, P_triple) in (K, Pa)
    
    Note:
        This is an approximation assuming linear boundaries.
        More accurate methods use integrated Clausius-Clapeyron.
    """
    T_sl, P_sl, slope_sl = solid_liquid_params
    T_lg, P_lg, slope_lg = liquid_gas_params
    
    # Linear lines: P = P_ref + slope x (T - T_ref)
    # Intersection: P_sl + slope_sl x (T - T_sl) = P_lg + slope_lg x (T - T_lg)
    # T x (slope_sl - slope_lg) = P_lg - P_sl + slope_slxT_sl - slope_lgxT_lg
    
    T_triple = (P_lg - P_sl + slope_sl*T_sl - slope_lg*T_lg) / (slope_sl - slope_lg)
    P_triple = P_sl + slope_sl * (T_triple - T_sl)
    
    return T_triple, P_triple


# =============================================================================
# GIBBS PHASE RULE
# =============================================================================

def gibbs_phase_rule(C: int, P: int, num_reactions: int = 0) -> int:
    """
    Calculate degrees of freedom using Gibbs phase rule.
    
    F = C - P + 2 (for non-reacting systems)
    F = C - P + 2 - R (for reacting systems)
    
    where:
        C = number of components
        P = number of phases
        R = number of independent reactions
    
    Args:
        C: Number of components
        P: Number of phases in equilibrium
        num_reactions: Number of independent chemical reactions (default 0)
    
    Returns:
        F: Degrees of freedom (number of intensive variables that can be varied)
    
    Example:
        >>> gibbs_phase_rule(1, 3)  # Water at triple point
        0  # No degrees of freedom - invariant point
        >>> gibbs_phase_rule(1, 2)  # Water at melting point
        1  # Can vary T or P (but not both independently)
    """
    F = C - P + 2 - num_reactions
    return max(0, F)  # F cannot be negative


def phase_rule_interpretation(F: int) -> str:
    """
    Interpret Gibbs phase rule result.
    
    Args:
        F: Degrees of freedom
    
    Returns:
        Description of the system behavior
    """
    if F == 0:
        return "Invariant point: All variables fixed (e.g., triple point)"
    elif F == 1:
        return "Univariant: Can vary one variable (e.g., melting curve)"
    elif F == 2:
        return "Bivariant: Can vary two variables (e.g., single phase region)"
    elif F > 2:
        return f"Multivariant: Can vary {F} variables independently"
    else:
        return "Invalid (negative degrees of freedom)"


def max_phases_at_equilibrium(C: int) -> int:
    """
    Maximum number of phases that can coexist at equilibrium.
    
    Occurs when F = 0 (invariant point).
    P_max = C + 2
    
    Args:
        C: Number of components
    
    Returns:
        Maximum number of phases
    
    Example:
        >>> max_phases_at_equilibrium(1)  # Single component
        3  # Triple point (solid, liquid, gas)
        >>> max_phases_at_equilibrium(2)  # Two components
        4  # Could have 4 phases coexist
    """
    return C + 2


# =============================================================================
# CRITICAL POINT PROPERTIES
# =============================================================================

def critical_compression_factor(Z_c: float = 0.27) -> float:
    """
    Return typical critical compression factor.
    
    Z_c = P_c V_c / (R T_c)
    
    For most substances: Z_c ~ 0.27
    
    Args:
        Z_c: Critical compression factor (default 0.27)
    
    Returns:
        Z_c (just returns the value for reference)
    """
    return Z_c


def estimate_critical_properties(
    T_b: float,
    method: str = 'lydersen'
) -> Dict[str, float]:
    """
    Estimate critical properties from normal boiling point.
    
    Simple estimation methods for order-of-magnitude values.
    
    Args:
        T_b: Normal boiling point in K
        method: Estimation method ('lydersen', 'simple')
    
    Returns:
        Dictionary with estimated T_c, P_c, V_c
    
    Note:
        These are rough estimates. Use experimental data when available.
    """
    if method == 'simple':
        # Very simple estimation
        T_c = 1.5 * T_b  # Critical temperature ~ 1.5 x T_b
        P_c = 1e7  # Rough estimate: 100 bar
        return {
            'T_c': T_c,
            'P_c': P_c,
            'V_c': None,  # Cannot estimate simply
            'note': 'Very rough estimates'
        }
    else:
        return {
            'note': 'Use detailed group contribution methods for accurate estimates',
            'reference': 'Lydersen (1955), Joback (1984)'
        }


def reduced_temperature(T: float, T_c: float) -> float:
    """
    Calculate reduced temperature.
    
    T_r = T/T_c
    
    Args:
        T: Temperature in K
        T_c: Critical temperature in K
    
    Returns:
        Reduced temperature (dimensionless)
    """
    return T / T_c


def reduced_pressure(P: float, P_c: float) -> float:
    """
    Calculate reduced pressure.
    
    P_r = P/P_c
    
    Args:
        P: Pressure (any units)
        P_c: Critical pressure (same units)
    
    Returns:
        Reduced pressure (dimensionless)
    """
    return P / P_c


def reduced_volume(V: float, V_c: float) -> float:
    """
    Calculate reduced volume.
    
    V_r = V/V_c
    
    Args:
        V: Molar volume (any units)
        V_c: Critical molar volume (same units)
    
    Returns:
        Reduced volume (dimensionless)
    """
    return V / V_c


# =============================================================================
# PHASE STABILITY
# =============================================================================

def gibbs_energy_phase(
    H: float,
    S: float,
    T: float
) -> float:
    """
    Calculate Gibbs free energy for a phase.
    
    G = H - TS
    
    Args:
        H: Enthalpy in J/mol
        S: Entropy in J/(mol·K)
        T: Temperature in K
    
    Returns:
        Gibbs free energy in J/mol
    """
    return H - T * S


def entropy_of_vaporization(T_b: float, delta_H_vap: float) -> float:
    """
    Calculate entropy of vaporization at boiling point.
    
    DeltaS_vap = DeltaH_vap/T_b
    
    Trouton's rule: DeltaS_vap ~ 88 J/(mol·K) for many liquids
    
    Args:
        T_b: Boiling point in K
        delta_H_vap: Enthalpy of vaporization in J/mol
    
    Returns:
        Entropy of vaporization in J/(mol·K)
    
    Example:
        >>> entropy_of_vaporization(373, 40700)  # Water
        109  # Higher than Trouton's rule due to H-bonding
    """
    return delta_H_vap / T_b


def trouton_rule_check(T_b: float, delta_H_vap: float) -> Dict:
    """
    Check if substance follows Trouton's rule.
    
    Args:
        T_b: Boiling point in K
        delta_H_vap: Enthalpy of vaporization in J/mol
    
    Returns:
        Dictionary with Trouton's rule analysis
    """
    delta_S = entropy_of_vaporization(T_b, delta_H_vap)
    
    deviation = delta_S - 88  # Compare to Trouton's rule
    
    if abs(deviation) < 10:
        classification = "Follows Trouton's rule"
    elif deviation > 10:
        classification = "Higher than Trouton's rule (likely H-bonding)"
    else:
        classification = "Lower than Trouton's rule (likely weak interactions)"
    
    return {
        'delta_S_vap': delta_S,
        'trouton_value': 88,
        'deviation': deviation,
        'classification': classification
    }


# =============================================================================
# SUBSTANCE DATABASE
# =============================================================================

PHASE_DATA = {
    'water': {
        'T_melt': 273.15,  # K
        'T_b': 373.15,  # K
        'T_c': 647.096,  # K
        'P_c': 22.064e6,  # Pa
        'V_c': 55.95e-6,  # m3/mol
        'delta_H_fus': 6008,  # J/mol
        'delta_H_vap': 40650,  # J/mol
        'rho_solid': 917,  # kg/m3
        'rho_liquid': 997,  # kg/m3
        'M': 0.018015,  # kg/mol
        'triple_point': (273.16, 611.73),  # (K, Pa)
    },
    'CO2': {
        'T_melt': None,  # Sublimes at 1 atm
        'T_b': None,  # No liquid at 1 atm
        'T_c': 304.128,  # K
        'P_c': 7.377e6,  # Pa
        'V_c': 94e-6,  # m3/mol
        'delta_H_sub': 25200,  # J/mol (sublimation)
        'delta_H_vap': None,  # Not applicable at 1 atm
        'triple_point': (216.55, 5.185e5),  # (K, Pa) - above 1 atm!
        'M': 0.04401,  # kg/mol
    },
    'nitrogen': {
        'T_melt': 63.15,  # K
        'T_b': 77.36,  # K
        'T_c': 126.192,  # K
        'P_c': 3.3958e6,  # Pa
        'V_c': 89.5e-6,  # m3/mol
        'delta_H_fus': 720,  # J/mol
        'delta_H_vap': 5560,  # J/mol
        'M': 0.028014,  # kg/mol
        'triple_point': (63.151, 12.53e3),  # (K, Pa)
    },
    'oxygen': {
        'T_melt': 54.36,  # K
        'T_b': 90.188,  # K
        'T_c': 154.581,  # K
        'P_c': 5.043e6,  # Pa
        'V_c': 73.4e-6,  # m3/mol
        'delta_H_fus': 444,  # J/mol
        'delta_H_vap': 6820,  # J/mol
        'M': 0.031998,  # kg/mol
        'triple_point': (54.3584, 146.33),  # (K, Pa)
    },
    'benzene': {
        'T_melt': 278.68,  # K
        'T_b': 353.25,  # K
        'T_c': 562.02,  # K
        'P_c': 4.895e6,  # Pa
        'V_c': 256e-6,  # m3/mol
        'delta_H_fus': 9900,  # J/mol
        'delta_H_vap': 30700,  # J/mol
        'M': 0.07811,  # kg/mol
        'triple_point': (278.68, 47.9),  # (K, Pa)
    }
}


def get_phase_data(substance: str) -> Dict:
    """
    Get phase equilibrium data for a substance.
    
    Args:
        substance: Substance name (e.g., 'water', 'CO2', 'nitrogen')
    
    Returns:
        Dictionary of phase properties
    
    Example:
        >>> data = get_phase_data('water')
        >>> print(data['T_c'])
        647.096
    """
    # Case-insensitive lookup
    key_map = {k.lower(): k for k in PHASE_DATA}
    if substance.lower() in key_map:
        return PHASE_DATA[key_map[substance.lower()]]
    else:
        raise ValueError(f"Substance '{substance}' not in database. "
                        f"Available: {list(PHASE_DATA.keys())}")


def phase_at_conditions(substance: str, T: float, P: float) -> str:
    """
    Predict phase of substance at given conditions.
    
    Simple prediction based on critical point and triple point.
    For accurate predictions, use equation of state.
    
    Args:
        substance: Substance name
        T: Temperature in K
        P: Pressure in Pa
    
    Returns:
        Phase description
    """
    data = get_phase_data(substance)
    T_c = data['T_c']
    P_c = data['P_c']
    
    if T > T_c and P > P_c:
        return "supercritical fluid"
    elif T > T_c:
        return "gas (above T_c)"
    elif P > P_c:
        return "dense fluid (above P_c)"
    else:
        # Simple check - would need actual phase diagram for accuracy
        T_b = data.get('T_b')
        if T_b is None:
            return "Requires detailed phase diagram"
        
        # Approximate: if T < T_b and P > 1 atm -> liquid
        if T < T_b and P > ATM_TO_PA:
            return "likely liquid"
        elif T < T_b:
            return "likely gas"
        else:
            return "likely gas (above boiling point)"


# =============================================================================
# BINARY PHASE DIAGRAMS
# =============================================================================

def lever_rule_fraction(
    overall_comp: float,
    phase1_comp: float,
    phase2_comp: float
) -> Tuple[float, float]:
    """
    Calculate phase fractions using lever rule.
    
    fraction_phase1 = (x_2 - x)/(x_2 - x_1)
    fraction_phase2 = (x - x_1)/(x_2 - x_1)
    
    Args:
        overall_comp: Overall composition x
        phase1_comp: Composition of phase 1 (x_1)
        phase2_comp: Composition of phase 2 (x_2)
    
    Returns:
        (fraction_phase1, fraction_phase2)
    
    Example:
        >>> # Overall composition x = 0.4
        >>> # Phase 1 has x_1 = 0.2, Phase 2 has x_2 = 0.8
        >>> lever_rule_fraction(0.4, 0.2, 0.8)
        (0.667, 0.333)
    """
    if phase1_comp == phase2_comp:
        raise ValueError("Phase compositions cannot be equal")
    
    f1 = (phase2_comp - overall_comp) / (phase2_comp - phase1_comp)
    f2 = (overall_comp - phase1_comp) / (phase2_comp - phase1_comp)
    
    return f1, f2


def eutectic_composition(T_A: float, T_B: float, 
                         delta_H_A: float, delta_H_B: float,
                         x_eutectic_guess: float = 0.5) -> float:
    """
    Estimate eutectic composition for ideal eutectic system.
    
    Uses simplified thermodynamic model.
    
    Args:
        T_A, T_B: Melting points of pure components A and B in K
        delta_H_A, delta_H_B: Enthalpies of fusion in J/mol
        x_eutectic_guess: Initial guess for eutectic composition
    
    Returns:
        Estimated eutectic composition (mole fraction of B)
    
    Note:
        This is a simplified estimate. Real eutectic systems
        require detailed thermodynamic modeling.
    """
    # For ideal eutectic: ln(x_A) = -DeltaH_A/R x (1/T - 1/T_A)
    # At eutectic: x_A + x_B = 1
    # Solve iteratively
    
    R_local = 8.314
    
    def equations(T_e):
        if T_e >= min(T_A, T_B):
            return float('inf')
        x_A = np.exp(-delta_H_A / R_local * (1/T_e - 1/T_A))
        x_B = np.exp(-delta_H_B / R_local * (1/T_e - 1/T_B))
        return x_A + x_B - 1
    
    # Find eutectic temperature
    T_min = 0.5 * min(T_A, T_B)
    try:
        T_e = brentq(equations, T_min, min(T_A, T_B) - 1)
        x_B = np.exp(-delta_H_B / R_local * (1/T_e - 1/T_B))
        return x_B
    except:
        return x_eutectic_guess  # Return guess if solution fails


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    print("Phase Equilibria Tools - Examples")
    print("=" * 60)
    
    # Clausius-Clapeyron
    print("\n1. Clausius-Clapeyron Equation:")
    P2 = clausius_clapeyron_vapor_pressure(373, 1, 298, 40700)
    print(f"   Water vapor pressure at 298 K: {P2:.3f} atm")
    
    T2 = clausius_clapeyron_temperature(373, 1, 0.5, 40700)
    print(f"   Temperature where P = 0.5 atm: {T2:.1f} K")
    
    # Phase rule
    print("\n2. Gibbs Phase Rule:")
    F = gibbs_phase_rule(1, 3)
    print(f"   Water at triple point (C=1, P=3): F = {F}")
    print(f"   {phase_rule_interpretation(F)}")
    
    F = gibbs_phase_rule(1, 2)
    print(f"   Water on melting curve (C=1, P=2): F = {F}")
    print(f"   {phase_rule_interpretation(F)}")
    
    # Clapeyron equation (water anomaly)
    print("\n3. Clapeyron Equation (Water Anomaly):")
    dP_dT = clapeyron_slope(6008, -1.63e-6, 273)
    print(f"   Ice-water boundary slope: {dP_dT:.2e} Pa/K")
    print(f"   Negative slope: melting point decreases with pressure!")
    
    # Trouton's rule
    print("\n4. Trouton's Rule:")
    analysis = trouton_rule_check(373, 40700)
    print(f"   DeltaS_vap for water: {analysis['delta_S_vap']:.1f} J/(mol·K)")
    print(f"   Classification: {analysis['classification']}")
    
    # Lever rule
    print("\n5. Lever Rule:")
    f1, f2 = lever_rule_fraction(0.4, 0.2, 0.8)
    print(f"   Overall x = 0.4, phases at x1 = 0.2, x2 = 0.8")
    print(f"   Fraction phase 1: {f1:.3f}")
    print(f"   Fraction phase 2: {f2:.3f}")
    
    # Substance data
    print("\n6. Phase Data:")
    water = get_phase_data('water')
    print(f"   Water T_c: {water['T_c']:.1f} K")
    print(f"   Water P_c: {water['P_c']/1e6:.2f} MPa")
    print(f"   Water triple point: {water['triple_point']}")
    
    # Reduced properties
    print("\n7. Reduced Properties (water at 500 K, 10 MPa):")
    T_r = reduced_temperature(500, water['T_c'])
    P_r = reduced_pressure(10e6, water['P_c'])
    print(f"   T_r = {T_r:.3f}")
    print(f"   P_r = {P_r:.3f}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="clapeyron_pressure_change",
            description="Calculate pressure change for a temperature change along phase boundary.",
            input_schema=[
            InputSchemaField(name="delta_H", type="number", required=True),
            InputSchemaField(name="delta_V", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="delta_T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="clapeyron_slope",
            description="Calculate slope of phase boundary using Clapeyron equation.",
            input_schema=[
            InputSchemaField(name="delta_H", type="number", required=True),
            InputSchemaField(name="delta_V", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="clausius_clapeyron_enthalpy",
            description="Calculate enthalpy of vaporization from two vapor pressure points.",
            input_schema=[
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="P1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True),
            InputSchemaField(name="P2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="clausius_clapeyron_temperature",
            description="Calculate temperature at a different vapor pressure.",
            input_schema=[
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="P1", type="number", required=True),
            InputSchemaField(name="P2", type="number", required=True),
            InputSchemaField(name="delta_H_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="clausius_clapeyron_vapor_pressure",
            description="Calculate vapor pressure at a different temperature using Clausius-Clapeyron.",
            input_schema=[
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="P1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True),
            InputSchemaField(name="delta_H_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="critical_compression_factor",
            description="Return typical critical compression factor.",
            input_schema=[
            InputSchemaField(name="Z_c", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="entropy_of_vaporization",
            description="Calculate entropy of vaporization at boiling point.",
            input_schema=[
            InputSchemaField(name="T_b", type="number", required=True),
            InputSchemaField(name="delta_H_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="estimate_critical_properties",
            description="Estimate critical properties from normal boiling point.",
            input_schema=[
            InputSchemaField(name="T_b", type="number", required=True),
            InputSchemaField(name="method", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="eutectic_composition",
            description="Estimate eutectic composition for ideal eutectic system.",
            input_schema=[
            InputSchemaField(name="T_A", type="number", required=True),
            InputSchemaField(name="T_B", type="number", required=True),
            InputSchemaField(name="delta_H_A", type="number", required=True),
            InputSchemaField(name="delta_H_B", type="number", required=True),
            InputSchemaField(name="x_eutectic_guess", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="get_phase_data",
            description="Get phase equilibrium data for a substance.",
            input_schema=[
            InputSchemaField(name="substance", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_energy_phase",
            description="Calculate Gibbs free energy for a phase.",
            input_schema=[
            InputSchemaField(name="H", type="number", required=True),
            InputSchemaField(name="S", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_phase_rule",
            description="Calculate degrees of freedom using Gibbs phase rule.",
            input_schema=[
            InputSchemaField(name="C", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="num_reactions", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lever_rule_fraction",
            description="Calculate phase fractions using lever rule.",
            input_schema=[
            InputSchemaField(name="overall_comp", type="number", required=True),
            InputSchemaField(name="phase1_comp", type="number", required=True),
            InputSchemaField(name="phase2_comp", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="max_phases_at_equilibrium",
            description="Maximum number of phases that can coexist at equilibrium.",
            input_schema=[
            InputSchemaField(name="C", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="melting_point_pressure_dependence",
            description="Calculate how melting point changes with pressure.",
            input_schema=[
            InputSchemaField(name="T_melt", type="number", required=True),
            InputSchemaField(name="delta_H_fus", type="number", required=True),
            InputSchemaField(name="rho_solid", type="number", required=True),
            InputSchemaField(name="rho_liquid", type="number", required=True),
            InputSchemaField(name="M", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="normal_boiling_point",
            description="Calculate normal boiling point from vapor pressure data.",
            input_schema=[
            InputSchemaField(name="delta_H_vap", type="number", required=True),
            InputSchemaField(name="vapor_pressure_at_T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="phase_at_conditions",
            description="Predict phase of substance at given conditions.",
            input_schema=[
            InputSchemaField(name="substance", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="phase_rule_interpretation",
            description="Interpret Gibbs phase rule result.",
            input_schema=[
            InputSchemaField(name="F", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reduced_pressure",
            description="Calculate reduced pressure.",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="P_c", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reduced_temperature",
            description="Calculate reduced temperature.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="T_c", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="reduced_volume",
            description="Calculate reduced volume.",
            input_schema=[
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="V_c", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="temperature_from_antione",
            description="Calculate temperature from vapor pressure using Antoine equation.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="C", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="triple_point_from_phase_boundaries",
            description="Estimate triple point from two phase boundary lines.",
            input_schema=[
            InputSchemaField(name="solid_liquid_params", type="number", required=True),
            InputSchemaField(name="liquid_gas_params", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="trouton_rule_check",
            description="Check if substance follows Trouton's rule.",
            input_schema=[
            InputSchemaField(name="T_b", type="number", required=True),
            InputSchemaField(name="delta_H_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="vapor_pressure_antione",
            description="Calculate vapor pressure using Antoine equation.",
            input_schema=[
            InputSchemaField(name="A", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="C", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
