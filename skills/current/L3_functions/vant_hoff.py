"""
Van't Hoff Analysis Tools - L3 Implementation
Source: DeVoe Thermodynamics and Chemistry, Ch11.8-11.9
TRUE source extraction - equations from actual source text

Equations from source:
- Eq 11.8.10: Delta_rGdeg = -RT ln K
- Eq 11.8.11: K = exp(-Delta_rGdeg/RT)
- Eq 11.8.20: Delta_rG = Delta_rH - TDelta_rS
"""

## Solver Instructions (for AI Agent)

# When you encounter **van't Hoff / equilibrium thermodynamics** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - DeltaG from K: `delta_G_from_equilibrium_constant(K, T)`
# - K from DeltaG: `equilibrium_constant_from_delta_G(delta_G, T)`
# - DeltaG from DeltaH, DeltaS: `delta_G_from_H_S(delta_H, delta_S, T)`
# - K from DeltaH, DeltaS: `equilibrium_constant_from_H_S(delta_H, delta_S, T)`
# - van't Hoff equation (K at T2 from K at T1): `vant_hoff_equation(K1, T1, T2, delta_H)`
# - van't Hoff slope/intercept: `vant_hoff_slope(...)`, `enthalpy_from_vant_hoff_slope(...)`
# - Reaction quotient Q: `reaction_quotient(pressures)` or `(concentrations)`
# - Equilibrium position: `equilibrium_position(Q, K)`
# - Temperature effect: `temperature_effect_on_equilibrium(delta_H, T)`

### Step 2: Choose the correct function
# - Converting between K and DeltaG: `delta_G_from_equilibrium_constant` / `equilibrium_constant_from_delta_G`
# - Predicting K at new temperature: `vant_hoff_equation`
# - Determining spontaneity from Q vs K: `reaction_quotient` -> `equilibrium_position`

### Step 3: Handle special cases
# - Units: T in Kelvin, DeltaH/DeltaG in J/mol, DeltaS in J/(mol·K)
# - Q and K use same conventions (partial pressures for gases, concentrations for solutions)
# - Endothermic (DeltaH>0): K increases with T; Exothermic (DeltaH<0): K decreases with T

### Examples
# 1. K=50 at 298 K, find DeltaG: `delta_G_from_equilibrium_constant(50, 298)` -> ~-9.89 kJ/mol
# 2. K=10 at 300 K, DeltaH=-40 kJ/mol, K at 400 K: `vant_hoff_equation(10, 300, 400, -40000)` -> K decreases
# 3. Q=0.01, K=100: `equilibrium_position(0.01, 100)` -> "Forward reaction favored"



import math
from typing import Dict, Tuple, Optional, List

# Physical constants
R = 8.314462618  # Gas constant (J/(mol·K))


def equilibrium_constant_from_delta_G(
    delta_G: float,
    temperature: float
) -> float:
    """
    Calculate equilibrium constant from standard Gibbs energy.
    
    Source: DeVoe Eq 11.8.11: K = exp(-Delta_rGdeg/RT)
    
    Note from source: "K is less than 1 if Delta_rGdeg is positive 
    and greater than 1 if Delta_rGdeg is negative."
    
    Args:
        delta_G: Standard Gibbs energy change Delta_rGdeg (J/mol)
        temperature: Temperature (K)
    
    Returns:
        Equilibrium constant K (dimensionless)
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    
    K = math.exp(-delta_G / (R * temperature))
    return K


def delta_G_from_equilibrium_constant(
    K: float,
    temperature: float
) -> float:
    """
    Calculate standard Gibbs energy from equilibrium constant.
    
    Source: DeVoe Eq 11.8.10: Delta_rGdeg = -RT ln K
    
    Args:
        K: Equilibrium constant (dimensionless)
        temperature: Temperature (K)
    
    Returns:
        Standard Gibbs energy change Delta_rGdeg (J/mol)
    """
    if K <= 0:
        raise ValueError("Equilibrium constant must be positive")
    if temperature <= 0:
        raise ValueError("Temperature must be positive")
    
    delta_G = -R * temperature * math.log(K)
    return delta_G


def delta_G_from_H_S(
    delta_H: float,
    delta_S: float,
    temperature: float
) -> float:
    """
    Calculate Gibbs energy from enthalpy and entropy.
    
    Source: DeVoe Eq 11.8.20: Delta_rG = Delta_rH - TDelta_rS
    
    This is the Gibbs-Helmholtz relation.
    
    Args:
        delta_H: Enthalpy change Delta_rH (J/mol)
        delta_S: Entropy change Delta_rS (J/(mol·K))
        temperature: Temperature (K)
    
    Returns:
        Gibbs energy change Delta_rG (J/mol)
    """
    return delta_H - temperature * delta_S


def equilibrium_constant_from_H_S(
    delta_H: float,
    delta_S: float,
    temperature: float
) -> float:
    """
    Calculate equilibrium constant from enthalpy and entropy.
    
    Combines Eq 11.8.11 and 11.8.20:
    K = exp(-(Delta_rH - TDelta_rS) / RT) = exp(-Delta_rH/RT + Delta_rS/R)
    
    Args:
        delta_H: Standard enthalpy change Delta_rHdeg (J/mol)
        delta_S: Standard entropy change Delta_rSdeg (J/(mol·K))
        temperature: Temperature (K)
    
    Returns:
        Equilibrium constant K (dimensionless)
    """
    delta_G = delta_G_from_H_S(delta_H, delta_S, temperature)
    return equilibrium_constant_from_delta_G(delta_G, temperature)


def vant_hoff_equation(
    K1: float,
    T1: float,
    T2: float,
    delta_H: float
) -> float:
    """
    Calculate equilibrium constant at new temperature using van't Hoff equation.
    
    The van't Hoff equation (integrated form assuming constant DeltaH):
    ln(K2/K1) = -DeltaH/R x (1/T2 - 1/T1)
    
    Args:
        K1: Equilibrium constant at T1
        T1: Initial temperature (K)
        T2: Final temperature (K)
        delta_H: Enthalpy change Delta_rHdeg (J/mol), assumed constant
    
    Returns:
        Equilibrium constant K2 at T2
    """
    if K1 <= 0:
        raise ValueError("K1 must be positive")
    if T1 <= 0 or T2 <= 0:
        raise ValueError("Temperatures must be positive")
    
    ln_K2_K1 = -delta_H / R * (1/T2 - 1/T1)
    K2 = K1 * math.exp(ln_K2_K1)
    return K2


def vant_hoff_temperature_transfer(
    K1: float,
    T1: float,
    T2: float,
    delta_H: float
) -> dict:
    """
    Calculate the integrated van't Hoff temperature transfer and related
    thermodynamic outputs.

    Args:
        K1: Equilibrium constant at T1
        T1: Initial temperature (K)
        T2: Final temperature (K)
        delta_H: Enthalpy change Delta_rHdeg (J/mol), assumed constant

    Returns:
        Dict with K2, ln(K2/K1), and DeltaG at T2 in kJ/mol.
    """
    if K1 <= 0:
        raise ValueError("K1 must be positive")
    if T1 <= 0 or T2 <= 0:
        raise ValueError("Temperatures must be positive")

    ln_K2_K1 = -delta_H / R * (1 / T2 - 1 / T1)
    K2 = K1 * math.exp(ln_K2_K1)
    delta_G_t2_kj_mol = -R * T2 * math.log(K2) / 1000.0
    answer = (
        f"K2 = {K2:.6g}; ln(K2/K1) = {ln_K2_K1:.6g}; "
        f"Delta G at T2 = {delta_G_t2_kj_mol:.6g} kJ/mol"
    )
    return {
        "answer": answer,
        "answer_values": [K2, ln_K2_K1, delta_G_t2_kj_mol],
        "K2": K2,
        "ln_K2_over_K1": ln_K2_K1,
        "delta_G_T2_kJ_mol": delta_G_t2_kj_mol,
        "units": ["dimensionless", "dimensionless", "kJ/mol"],
        "assumptions": "Constant DeltaH over the stated temperature interval; natural logarithm.",
    }


def vant_hoff_slope(
    delta_H: float
) -> float:
    """
    Calculate van't Hoff plot slope.
    
    From d(ln K)/d(1/T) = -DeltaH/R
    
    Args:
        delta_H: Enthalpy change Delta_rHdeg (J/mol)
    
    Returns:
        Slope of ln K vs 1/T plot (K)
    """
    return -delta_H / R


def enthalpy_from_vant_hoff_slope(
    slope: float
) -> float:
    """
    Calculate enthalpy change from van't Hoff plot slope.
    
    DeltaH = -slope x R
    
    Args:
        slope: Slope of ln K vs 1/T plot (K)
    
    Returns:
        Enthalpy change Delta_rHdeg (J/mol)
    """
    return -slope * R


def reaction_quotient(
    activities: Dict[str, float],
    stoichiometry: Dict[str, int]
) -> float:
    """
    Calculate reaction quotient Q from activities.
    
    Source: DeVoe Eq 11.8.6: Q_rxn = ∏ a_i^ν_i
    
    Note from source: "At a fixed temperature, reaction equilibrium is 
    attained only if and only if the value of Q_rxn becomes equal to 
    the value of K at that temperature."
    
    Args:
        activities: Dict of species activities {species: a_i}
        stoichiometry: Dict of stoichiometric coefficients {species: ν_i}
                      (positive for products, negative for reactants)
    
    Returns:
        Reaction quotient Q
    """
    Q = 1.0
    for species, nu in stoichiometry.items():
        if species in activities:
            a = activities[species]
            if a > 0:
                Q *= a ** nu
    return Q


def equilibrium_position(
    Q: float,
    K: float
) -> str:
    """
    Determine equilibrium position from Q vs K comparison.
    
    From source: "At a fixed temperature, reaction equilibrium is 
    attained only if and only if the value of Q_rxn becomes equal 
    to the value of K at that temperature."
    
    Args:
        Q: Reaction quotient
        K: Equilibrium constant
    
    Returns:
        String indicating equilibrium position
    """
    if abs(Q - K) / K < 0.001:  # Within 0.1% of equilibrium
        return "at equilibrium"
    elif Q < K:
        return "proceeds forward (Q < K)"
    else:
        return "proceeds reverse (Q > K)"


def temperature_effect_on_equilibrium(
    delta_H: float,
    T1: float,
    T2: float,
    K1: float
) -> Dict:
    """
    Analyze temperature effect on equilibrium position.
    
    Source: DeVoe Eq 11.9.8 shows that (∂ξ_eq/∂T)_p and Delta_rH 
    have the same sign.
    
    From source: "Because the partial second derivative (∂2G/∂ξ2)_T,p 
    is positive, Eqs. 11.9.8 and 11.9.9 show that (∂ξ_eq/∂T)_p and 
    Delta_rH have the same sign."
    
    For endothermic reactions (DeltaH > 0): increasing T favors products
    For exothermic reactions (DeltaH < 0): increasing T favors reactants
    
    Args:
        delta_H: Enthalpy change Delta_rHdeg (J/mol)
        T1: Initial temperature (K)
        T2: Final temperature (K)
        K1: Equilibrium constant at T1
    
    Returns:
        Dict with K2 and qualitative analysis
    """
    K2 = vant_hoff_equation(K1, T1, T2, delta_H)
    
    # Le Chatelier analysis from source
    if delta_H > 0:
        reaction_type = "endothermic"
        if T2 > T1:
            shift = "increasing temperature favors products (equilibrium shifts right)"
        else:
            shift = "decreasing temperature favors reactants (equilibrium shifts left)"
    else:
        reaction_type = "exothermic"
        if T2 > T1:
            shift = "increasing temperature favors reactants (equilibrium shifts left)"
        else:
            shift = "decreasing temperature favors products (equilibrium shifts right)"
    
    return {
        "K1": K1,
        "K2": K2,
        "K_ratio": K2 / K1,
        "reaction_type": reaction_type,
        "shift": shift,
        "delta_H_kJ": delta_H / 1000
    }


def get_module_status() -> Dict:
    """Return status of this module."""
    functions = [
        "equilibrium_constant_from_delta_G",
        "delta_G_from_equilibrium_constant",
        "delta_G_from_H_S",
        "equilibrium_constant_from_H_S",
        "vant_hoff_equation",
        "vant_hoff_slope",
        "enthalpy_from_vant_hoff_slope",
        "reaction_quotient",
        "equilibrium_position",
        "temperature_effect_on_equilibrium"
    ]
    return {
        "module": "vant_hoff",
        "total_functions": len(functions),
        "functions": functions,
        "status": "complete",
        "source": "DeVoe Ch11.8-11.9"
    }
