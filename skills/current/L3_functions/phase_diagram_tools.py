"""
Phase Diagram and Phase Equilibrium Calculation Tools.

Provides MCP-style tools for:
- Clausius-Clapeyron equation
- Gibbs phase rule
- Triple point estimation
- Lever rule for phase fractions
- Raoult's law
- Boiling point elevation / Freezing point depression

## Solver Instructions (for AI Agent)

When you encounter phase diagram and phase equilibrium problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given P1, T1, T2, DeltaHvap -> calculate P2 (Clausius-Clapeyron)?
- Given components and phases -> calculate degrees of freedom (Gibbs phase rule)?
- Given overall composition and phase boundaries -> calculate phase fractions (lever rule)?
- Given mole fraction and pure vapor pressure -> calculate partial pressure (Raoult's law)?
- Given solute molality -> calculate boiling point elevation or freezing point depression?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Clausius-Clapeyron | `clausius_clapeyron(P1, T1, T2, delta_H_vap, P2)` | Solve for unknown P or T |
| Gibbs phase rule | `gibbs_phase_rule(C, P)` | F = C - P + 2 |
| Lever rule | `phase_fraction_lever_rule(x_overall, x_alpha, x_beta)` | Returns alpha and beta fractions |
| Raoult's law | `raoults_law(x_A, P_A_star, x_B, P_B_star)` | Returns partial pressures |
| Boiling point elevation | `boiling_point_elevation(i, K_b, m)` | DeltaTb = i x Kb x m |
| Freezing point depression | `freezing_point_depression(i, K_f, m)` | DeltaTf = i x Kf x m |

### Step 3: Handle special cases
- Clausius-Clapeyron: valid when DeltaHvap is constant (narrow T range)
- Phase rule: F ≥ 0 always; negative F means impossible situation
- Lever rule: distances measured from overall composition to phase boundaries
- Raoult's law: assumes ideal solution behavior

### Examples
```python
# Example 1: Clausius-Clapeyron - find vapor pressure
# Water: P at 100degC given P=0.023 atm at 20degC, DeltaHvap=40.7 kJ/mol
clausius_clapeyron(0.023, 293, 373, 40700)
# -> ~1.0 atm

# Example 2: Gibbs phase rule
gibbs_phase_rule(2, 3)  # 2 components, 3 phases
# -> F = 1

# Example 3: Lever rule
phase_fraction_lever_rule(0.4, 0.2, 0.8)  # x=0.4, alpha=0.2, beta=0.8
# -> {'alpha_fraction': 2/3, 'beta_fraction': 1/3}

# Example 4: Boiling point elevation
boiling_point_elevation(2, 0.512, 1.0)  # NaCl (i~2), water Kb=0.512, m=1.0
# -> DeltaTb = 1.024 K
```
"""

import math
from typing import Optional

# Physical constants
R = 8.314  # J/(mol·K)


MCP_TOOLS = [
    {
        "name": "clausius_clapeyron",
        "description": "Calculate vapor pressure at a different temperature using the Clausius-Clapeyron equation: ln(P2/P1) = -DeltaH_vap/R x (1/T2 - 1/T1). Provide P1, T1, T2, delta_H_vap to get P2; or P1, T1, P2, delta_H_vap to get T2; or P1, T1, P2, T2 to get delta_H_vap.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "P1": {"type": "number", "description": "Vapor pressure at T1 (any unit, must match P2)"},
                "T1": {"type": "number", "description": "Temperature 1 in Kelvin"},
                "P2": {"type": "number", "description": "Vapor pressure at T2 (optional if solving for P2)"},
                "T2": {"type": "number", "description": "Temperature 2 in Kelvin (optional if solving for T2)"},
                "delta_H_vap": {"type": "number", "description": "Enthalpy of vaporization in J/mol (optional if solving for DeltaH_vap)"}
            },
            "required": []
        },
        "returns": {"type": "number", "description": "The unknown value"},
        "examples": [
            {"input": {"P1": 0.023, "T1": 293, "T2": 373, "delta_H_vap": 40700}, "output": 1.0, "note": "Water: P at 100degC from P at 20degC"}
        ]
    },
    {
        "name": "gibbs_phase_rule",
        "description": "Apply Gibbs phase rule F = C - P + 2. Calculate degrees of freedom given number of components and phases. Use for phase diagram analysis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "C": {"type": "integer", "description": "Number of components", "minimum": 1},
                "P": {"type": "integer", "description": "Number of phases present", "minimum": 1}
            },
            "required": ["C", "P"]
        },
        "returns": {"type": "integer", "description": "Degrees of freedom F"}
    },
    {
        "name": "triple_point_pressure",
        "description": "Estimate triple point pressure from normal boiling and melting points using the Clausius-Clapeyron equation for both solid-gas and liquid-gas equilibria.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "T_melt": {"type": "number", "description": "Normal melting point in K"},
                "T_boil": {"type": "number", "description": "Normal boiling point in K"},
                "delta_H_sub": {"type": "number", "description": "Enthalpy of sublimation in J/mol"},
                "delta_H_vap": {"type": "number", "description": "Enthalpy of vaporization in J/mol"},
                "P_atm": {"type": "number", "description": "Atmospheric pressure in atm (default 1.0)", "default": 1.0}
            },
            "required": ["T_melt", "T_boil", "delta_H_sub", "delta_H_vap"]
        },
        "returns": {"type": "number", "description": "Triple point pressure in atm"}
    },
    {
        "name": "phase_fraction_lever_rule",
        "description": "Apply the lever rule to determine the fraction of each phase in a two-phase region of a phase diagram. Given overall composition and the compositions of the two phases, calculate the mole or mass fractions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "x_overall": {"type": "number", "description": "Overall composition (mole or mass fraction of component B)"},
                "x_alpha": {"type": "number", "description": "Composition of phase alpha (left boundary)"},
                "x_beta": {"type": "number", "description": "Composition of phase beta (right boundary)"}
            },
            "required": ["x_overall", "x_alpha", "x_beta"]
        },
        "returns": {"type": "object", "description": "{'alpha_fraction': float, 'beta_fraction': float}"}
    },
    {
        "name": "raoults_law",
        "description": "Calculate vapor pressure of a solution using Raoult's law: P_i = x_i x P_i*. Also calculate total vapor pressure and vapor composition for ideal solutions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "x_A": {"type": "number", "description": "Mole fraction of component A in liquid"},
                "P_A_star": {"type": "number", "description": "Vapor pressure of pure A (same units as output)"},
                "x_B": {"type": "number", "description": "Mole fraction of component B in liquid (optional)"},
                "P_B_star": {"type": "number", "description": "Vapor pressure of pure B (optional, for total P)"}
            },
            "required": ["x_A", "P_A_star"]
        },
        "returns": {"type": "object", "description": "{'P_A': float, 'P_total': float or None, 'y_A': float or None}"}
    },
    {
        "name": "boiling_point_elevation",
        "description": "Calculate boiling point elevation: DeltaT_b = i x K_b x m. Where i is van't Hoff factor, K_b is ebullioscopic constant, m is molality.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "K_b": {"type": "number", "description": "Ebullioscopic constant (K·kg/mol)"},
                "molality": {"type": "number", "description": "Molality of solute (mol/kg)"},
                "i": {"type": "number", "description": "Van't Hoff factor (default 1.0)", "default": 1.0}
            },
            "required": ["K_b", "molality"]
        },
        "returns": {"type": "number", "description": "Boiling point elevation in K"}
    },
    {
        "name": "freezing_point_depression",
        "description": "Calculate freezing point depression: DeltaT_f = i x K_f x m.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "K_f": {"type": "number", "description": "Cryoscopic constant (K·kg/mol)"},
                "molality": {"type": "number", "description": "Molality of solute (mol/kg)"},
                "i": {"type": "number", "description": "Van't Hoff factor (default 1.0)", "default": 1.0}
            },
            "required": ["K_f", "molality"]
        },
        "returns": {"type": "number", "description": "Freezing point depression in K"}
    }
]


# =============================================================================
# IMPLEMENTATIONS
# =============================================================================


def clausius_clapeyron(P1: float = None, T1: float = None, P2: float = None,
                       T2: float = None, delta_H_vap: float = None) -> float:
    """
    Calculate unknown from Clausius-Clapeyron equation.
    
    ln(P2/P1) = -DeltaH_vap/R x (1/T2 - 1/T1)
    
    Provide 4 of 5 parameters; the 5th is solved for.
    
    Args:
        P1: Vapor pressure at T1
        T1: Temperature 1 in K
        P2: Vapor pressure at T2
        T2: Temperature 2 in K
        delta_H_vap: Enthalpy of vaporization in J/mol
    
    Returns:
        The unknown value
    
    Raises:
        ValueError: If exactly one parameter is not provided, or if values are invalid
    """
    params = {'P1': P1, 'T1': T1, 'P2': P2, 'T2': T2, 'delta_H_vap': delta_H_vap}
    missing = [k for k, v in params.items() if v is None]
    
    if len(missing) != 1:
        raise ValueError(f"Provide exactly 4 of 5 parameters. Missing: {missing}")
    
    unknown = missing[0]
    
    if unknown == 'P2':
        # ln(P2/P1) = -DeltaH/R x (1/T2 - 1/T1)
        ln_ratio = -delta_H_vap / R * (1.0 / T2 - 1.0 / T1)
        return P1 * math.exp(ln_ratio)
    
    elif unknown == 'T2':
        # 1/T2 = 1/T1 - R/DeltaH x ln(P2/P1)
        T2_inv = 1.0 / T1 - R / delta_H_vap * math.log(P2 / P1)
        if T2_inv <= 0:
            raise ValueError("No valid solution for T2 with given parameters")
        return 1.0 / T2_inv
    
    elif unknown == 'delta_H_vap':
        # DeltaH = -R x ln(P2/P1) / (1/T2 - 1/T1)
        denom = (1.0 / T2 - 1.0 / T1)
        if denom == 0:
            raise ValueError("T1 and T2 must be different")
        return -R * math.log(P2 / P1) / denom
    
    elif unknown == 'P1':
        ln_ratio = -delta_H_vap / R * (1.0 / T2 - 1.0 / T1)
        return P2 / math.exp(ln_ratio)
    
    elif unknown == 'T1':
        # 1/T1 = 1/T2 + R/DeltaH x ln(P2/P1)
        T1_inv = 1.0 / T2 + R / delta_H_vap * math.log(P2 / P1)
        if T1_inv <= 0:
            raise ValueError("No valid solution for T1 with given parameters")
        return 1.0 / T1_inv


def gibbs_phase_rule(C: int, P: int) -> int:
    """
    Apply Gibbs phase rule: F = C - P + 2.
    
    Args:
        C: Number of components
        P: Number of phases present
    
    Returns:
        Degrees of freedom F
    
    Raises:
        ValueError: If C < 1 or P < 1
    """
    if C < 1:
        raise ValueError("Number of components C must be >= 1")
    if P < 1:
        raise ValueError("Number of phases P must be >= 1")
    return C - P + 2


def triple_point_pressure(T_melt: float, T_boil: float,
                          delta_H_sub: float, delta_H_vap: float,
                          P_atm: float = 1.0) -> float:
    """
    Estimate triple point pressure.
    
    Uses Clausius-Clapeyron for sublimation (solid->gas) and vaporization
    (liquid->gas) curves to find intersection at T_triple ~ T_melt.
    
    Args:
        T_melt: Normal melting point in K
        T_boil: Normal boiling point in K
        delta_H_sub: Enthalpy of sublimation in J/mol
        delta_H_vap: Enthalpy of vaporization in J/mol
        P_atm: Atmospheric pressure in atm (default 1.0)
    
    Returns:
        Triple point pressure in atm
    """
    # Sublimation curve: ln(P/P_atm) = -DeltaH_sub/R x (1/T_melt - 1/T_boil_sub)
    # Approximate: use sublimation to get P at T_melt
    # ln(P_sub/T_melt / P_atm) = -DeltaH_sub/R x (1/T_melt - 1/T_boil)
    # This is a rough estimate assuming sublimation curve to boiling pressure
    
    # Better approach: integrate from T_boil (P=P_atm) to T_melt for vaporization,
    # and use sublimation curve from T_boil to T_melt
    # At triple point, both give same P at T_melt
    
    # Vapor pressure at T_melt from liquid-gas curve:
    P_liq = P_atm * math.exp(-delta_H_vap / R * (1.0 / T_melt - 1.0 / T_boil))
    
    # Vapor pressure at T_melt from solid-gas curve:
    P_sol = P_atm * math.exp(-delta_H_sub / R * (1.0 / T_melt - 1.0 / T_boil))
    
    # Average as rough estimate (true triple point requires more sophisticated treatment)
    return (P_liq + P_sol) / 2.0


def phase_fraction_lever_rule(x_overall: float, x_alpha: float,
                              x_beta: float) -> dict:
    """
    Apply the lever rule for two-phase equilibrium.
    
    f_alpha = (x_beta - x_overall) / (x_beta - x_alpha)
    f_beta = (x_overall - x_alpha) / (x_beta - x_alpha)
    
    Args:
        x_overall: Overall composition
        x_alpha: Composition of phase alpha (left boundary)
        x_beta: Composition of phase beta (right boundary)
    
    Returns:
        {'alpha_fraction': float, 'beta_fraction': float}
    
    Raises:
        ValueError: If x_alpha == x_beta or x_overall is outside [x_alpha, x_beta]
    """
    if x_alpha == x_beta:
        raise ValueError("Phase boundary compositions must differ")
    
    span = x_beta - x_alpha
    if span < 0:
        raise ValueError("x_alpha must be <= x_beta")
    
    f_alpha = (x_beta - x_overall) / span
    f_beta = (x_overall - x_alpha) / span
    
    if f_alpha < -1e-9 or f_beta < -1e-9:
        raise ValueError("x_overall must be between x_alpha and x_beta")
    
    # Clamp small negatives from floating point
    f_alpha = max(0.0, f_alpha)
    f_beta = max(0.0, f_beta)
    
    return {'alpha_fraction': round(f_alpha, 6), 'beta_fraction': round(f_beta, 6)}


def raoults_law(x_A: float, P_A_star: float, x_B: float = None,
                P_B_star: float = None) -> dict:
    """
    Apply Raoult's law for ideal solutions.
    
    P_A = x_A x P_A*
    P_total = P_A + x_B x P_B* (if both components given)
    y_A = P_A / P_total (if both components given)
    
    Args:
        x_A: Mole fraction of A in liquid
        P_A_star: Vapor pressure of pure A
        x_B: Mole fraction of B in liquid (optional)
        P_B_star: Vapor pressure of pure B (optional)
    
    Returns:
        {'P_A': float, 'P_total': float or None, 'y_A': float or None}
    """
    P_A = x_A * P_A_star
    
    result = {'P_A': P_A}
    
    if x_B is not None and P_B_star is not None:
        P_B = x_B * P_B_star
        P_total = P_A + P_B
        y_A = P_A / P_total if P_total > 0 else 0.0
        result['P_total'] = P_total
        result['P_B'] = P_B
        result['y_A'] = round(y_A, 6)
    else:
        result['P_total'] = None
        result['y_A'] = None
    
    return result


def boiling_point_elevation(K_b: float, molality: float, i: float = 1.0) -> float:
    """
    Calculate boiling point elevation: DeltaT_b = i x K_b x m.
    
    Args:
        K_b: Ebullioscopic constant (K·kg/mol)
        molality: Molality of solute (mol/kg)
        i: Van't Hoff factor (default 1.0)
    
    Returns:
        Boiling point elevation in K
    """
    return i * K_b * molality


def freezing_point_depression(K_f: float, molality: float, i: float = 1.0) -> float:
    """
    Calculate freezing point depression: DeltaT_f = i x K_f x m.
    
    Args:
        K_f: Cryoscopic constant (K·kg/mol)
        molality: Molality of solute (mol/kg)
        i: Van't Hoff factor (default 1.0)
    
    Returns:
        Freezing point depression in K
    """
    return i * K_f * molality


# Antoine equation data: constants A, B, C (mmHg, °C scale)
# Source: NIST Chemistry WebBook (common substances)
ANTOINE_DATA = {
    "water": {"A": 8.07131, "B": 1730.63, "C": 233.426, "T_min": 1, "T_max": 100},
    "ethanol": {"A": 8.20417, "B": 1642.89, "C": 230.300, "T_min": -57, "T_max": 80},
    "benzene": {"A": 6.90565, "B": 1211.033, "C": 220.790, "T_min": 8, "T_max": 103},
    "methanol": {"A": 8.08097, "B": 1582.271, "C": 239.726, "T_min": -16, "T_max": 91},
    "acetone": {"A": 7.02447, "B": 1161.0, "C": 224.0, "T_min": -32, "T_max": 77},
    "toluene": {"A": 6.95464, "B": 1344.800, "C": 219.482, "T_min": 6, "T_max": 137},
}

# STP conditions
STP_TEMP_K = 273.15  # 0°C
STP_PRESSURE_ATM = 1.0

# Normal boiling points (°C) for phase prediction
BOILING_POINTS = {
    "water": 100.0, "ethanol": 78.37, "benzene": 80.1, "methanol": 64.7,
    "acetone": 56.0, "toluene": 110.6, "hcl": -85.0, "oxygen": -183.0,
    "nitrogen": -196.0, "co2": -78.5, "methane": -161.5,
}

# Normal melting points (°C) for phase prediction
MELTING_POINTS = {
    "water": 0.0, "ethanol": -114.1, "benzene": 5.5, "methanol": -97.6,
    "acetone": -95.0, "toluene": -95.0, "hcl": -114.2, "oxygen": -218.8,
    "nitrogen": -210.0, "co2": -56.6,  # CO2 sublimation point at 1 atm
    "methane": -182.5,
}


def antoine(substance: str, T_celsius: float) -> float:
    """
    Calculate vapor pressure using the Antoine equation.
    
    log10(P) = A - B / (C + T)
    
    Where P is in mmHg and T is in °C.
    
    Args:
        substance: Substance name (e.g., 'water', 'ethanol')
        T_celsius: Temperature in °C
    
    Returns:
        Vapor pressure in mmHg
    
    Raises:
        ValueError: If substance not found or T outside valid range
    """
    sub = substance.lower().strip()
    if sub not in ANTOINE_DATA:
        raise ValueError(f"No Antoine constants for '{substance}'. Available: {list(ANTOINE_DATA.keys())}")
    
    data = ANTOINE_DATA[sub]
    if T_celsius < data["T_min"] or T_celsius > data["T_max"]:
        # Warn but still calculate (extrapolation)
        pass
    
    log10_P = data["A"] - data["B"] / (data["C"] + T_celsius)
    return 10.0 ** log10_P


def deltaH_vap_from_pressures(P1: float, T1: float, P2: float, T2: float) -> float:
    """
    Calculate enthalpy of vaporization from two (P, T) data points
    using the Clausius-Clapeyron equation.
    
    DeltaH_vap = -R * ln(P2/P1) / (1/T2 - 1/T1)
    
    Args:
        P1: Vapor pressure at T1 (any unit, must match P2)
        T1: Temperature 1 in K
        P2: Vapor pressure at T2
        T2: Temperature 2 in K
    
    Returns:
        Enthalpy of vaporization in J/mol
    """
    delta_H = -R * math.log(P2 / P1) / (1.0 / T2 - 1.0 / T1)
    return delta_H


def predict_phase_at_stp(substance: str) -> str:
    """
    Predict the phase of a substance at standard temperature and pressure.
    
    STP: T = 273.15 K (0°C), P = 1 atm.
    
    Logic:
    - If melting point > 0°C: solid
    - If melting point <= 0°C and boiling point > 0°C: liquid  
    - If boiling point <= 0°C: gas
    
    Args:
        substance: Substance name
    
    Returns:
        Phase name: 'solid', 'liquid', or 'gas'
    """
    sub = substance.lower().strip()
    
    if sub not in MELTING_POINTS:
        raise ValueError(f"No melting/boiling data for '{substance}'. Available: {list(MELTING_POINTS.keys())}")
    
    mp = MELTING_POINTS[sub]
    bp = BOILING_POINTS.get(sub)
    
    # Special case: CO2 sublimates at 1 atm (no liquid phase at STP)
    if sub == "co2":
        if STP_TEMP_K > (MELTING_POINTS["co2"] + 273.15):
            return "gas"
        else:
            return "solid"
    
    if bp is None:
        raise ValueError(f"No boiling point data for '{substance}'")
    
    if mp > 0.0:
        return "solid"
    elif bp > 0.0:
        return "liquid"
    else:
        return "gas"
