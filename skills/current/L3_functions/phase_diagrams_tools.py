"""
Phase Diagrams Tools
[Source: Averill, Ch11]

Tools for analyzing phase diagrams, calculating phase boundaries,
and predicting phase stability under various conditions.
"""
## Solver Instructions (for AI Agent)

# When you encounter phase diagram problems (phase identification, vapor pressure, phase transitions), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: substance, temperature, pressure, enthalpies, van der Waals parameters
# - **Asked**: phase at conditions, vapor pressure, boiling point, critical properties, triple point

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Identify phase | `identify_phase(substance, T, P)` | T (K), P (atm) |
# | Vapor pressure | `calculate_vapor_pressure(T, T_ref, P_ref, deltaH_vap)` | Clausius-Clapeyron |
# | Boiling point at P | `calculate_boiling_point_at_pressure(P, Tb_normal, deltaH_vap)` | P, normal BP, DeltaHvap |
# | Triple point estimate | `calculate_triple_point(Tb, Tm, deltaH_vap, deltaH_fus)` | Tb, Tm, enthalpies |
# | Critical properties | `calculate_critical_properties(a, b)` | van der Waals a, b |
# | Supercritical check | `is_supercritical(substance, T, P)` | T, P |
# | Phase boundary crossing | `get_phase_boundary_crossing(T1, P1, T2, P2, substance)` | two states |
# | Sublimation pressure | `calculate_sublimation_pressure(T, T_triple, P_triple, deltaH_sub)` | sublimation data |
# | Full diagram analysis | `analyze_phase_diagram(substance)` | substance name |
# | Phase at STP | `predict_phase_at_stp(substance)` | 25degC, 1 atm |

### Step 3: Handle special cases
# - Water has anomalous solid-liquid boundary (negative slope)
# - CO2 sublimes at 1 atm (no liquid phase at standard pressure)
# - Database includes: water, CO2, N2, O2, benzene, ethane, propane

### Examples
# 1. **Vapor pressure**: `calculate_vapor_pressure(350, 373.15, 1.0, 40.7)` -> ~0.414 atm
# 2. **Phase**: `identify_phase('water', 300, 1)` -> 'liquid'
# 3. **Critical properties**: `calculate_critical_properties(5.46, 0.0305)` -> Tc, Pc, Vc


import math
from typing import Dict, List, Tuple, Optional


# Physical Constants
R = 8.314  # Gas constant J/(mol·K)


# Reference Data: Key Phase Diagram Points
TRIPLE_POINTS = {
    'water': {'T': 273.16, 'P': 0.00604},  # K, atm
    'CO2': {'T': 216.6, 'P': 5.11},
    'nitrogen': {'T': 63.15, 'P': 0.124},
    'oxygen': {'T': 54.36, 'P': 0.0015},
    'benzene': {'T': 278.7, 'P': 0.047},
}

CRITICAL_POINTS = {
    'water': {'Tc': 647.1, 'Pc': 217.7},  # K, atm
    'CO2': {'Tc': 304.2, 'Pc': 72.79},
    'nitrogen': {'Tc': 126.2, 'Pc': 33.5},
    'oxygen': {'Tc': 154.6, 'Pc': 49.8},
    'benzene': {'Tc': 562.2, 'Pc': 48.3},
    'ethane': {'Tc': 305.3, 'Pc': 48.2},
    'propane': {'Tc': 369.8, 'Pc': 41.9},
}

NORMAL_MELTING_POINTS = {
    'water': 273.15,  # K
    'CO2': None,  # Sublimes at 1 atm
    'nitrogen': 63.15,
    'oxygen': 54.36,
    'benzene': 278.7,
    'ethane': 89.9,
    'propane': 85.5,
}

NORMAL_BOILING_POINTS = {
    'water': 373.15,  # K
    'CO2': None,  # Sublimes
    'nitrogen': 77.36,
    'oxygen': 90.20,
    'benzene': 353.3,
    'ethane': 184.6,
    'propane': 231.1,
}

ENTHALPIES_OF_VAPORIZATION = {
    'water': 40.7,  # kJ/mol at normal bp
    'CO2': 25.2,
    'nitrogen': 5.56,
    'oxygen': 6.82,
    'benzene': 30.8,
    'ethane': 14.7,
    'propane': 19.0,
}


def identify_phase(substance: str, T: float, P: float) -> str:
    """
    Identify the phase of a substance at given temperature and pressure.
    
    Args:
        substance: Substance name
        T: Temperature (K)
        P: Pressure (atm)
    
    Returns:
        Phase: 'solid', 'liquid', 'gas', or 'supercritical'
    """
    # Get reference data
    triple = TRIPLE_POINTS.get(substance.lower(), {})
    critical = CRITICAL_POINTS.get(substance.lower(), {})
    
    T_triple = triple.get('T', 0)
    P_triple = triple.get('P', 0)
    Tc = critical.get('Tc', float('inf'))
    Pc = critical.get('Pc', float('inf'))
    
    # Check supercritical
    if T > Tc and P > Pc:
        return 'supercritical'
    
    # Simplified phase identification
    # For water (anomalous solid-liquid line)
    if substance.lower() == 'water':
        if T < 273.15 and P < 1:
            # Could be solid or gas depending on P
            if P < 0.006:
                return 'gas'
            return 'solid'
        elif T < 273.15 and P > 1:
            return 'liquid'  # Pressure lowers mp
        elif T < 373.15:
            if P > 1:
                return 'liquid'
            return 'gas'
        else:
            return 'gas'
    
    # Normal phase diagram
    Tm = NORMAL_MELTING_POINTS.get(substance.lower())
    Tb = NORMAL_BOILING_POINTS.get(substance.lower())
    
    if Tm is not None and T < Tm:
        return 'solid'
    elif Tb is not None and T < Tb:
        return 'liquid' if P >= 1 else 'gas'
    else:
        return 'gas'


def calculate_vapor_pressure(T: float, T_ref: float, P_ref: float,
                               deltaH_vap: float) -> float:
    """
    Calculate vapor pressure using Clausius-Clapeyron equation.
    
    ln(P2/P1) = -DeltaH_vap/R × (1/T2 - 1/T1)
    
    Args:
        T: Temperature of interest (K)
        T_ref: Reference temperature (K)
        P_ref: Vapor pressure at reference temperature (atm)
        deltaH_vap: Enthalpy of vaporization (kJ/mol)
    
    Returns:
        Vapor pressure at T (atm)
    
    Examples:
        >>> calculate_vapor_pressure(350, 373.15, 1.0, 40.7)
        0.413...
    """
    # Convert kJ to J
    deltaH_J = deltaH_vap * 1000
    
    # Clausius-Clapeyron equation
    # ln(P2/P1) = -DeltaH/R × (1/T2 - 1/T1)
    ln_ratio = -deltaH_J / R * (1/T - 1/T_ref)
    P = P_ref * math.exp(ln_ratio)
    
    return P


def calculate_deltaH_vap_from_pressures(P1: float, T1: float, P2: float, T2: float) -> float:
    """
    Calculate enthalpy of vaporization from two vapor pressure points.
    
    Using Clausius-Clapeyron equation:
    ln(P2/P1) = -DeltaH_vap/R × (1/T2 - 1/T1)
    
    Args:
        P1: Vapor pressure at T1 (any unit)
        T1: Temperature 1 (K)
        P2: Vapor pressure at T2 (same unit as P1)
        T2: Temperature 2 (K)
    
    Returns:
        DeltaH_vap in kJ/mol
    
    Examples:
        >>> calculate_deltaH_vap_from_pressures(0.860, 336.85, 0.330, 308.25)
        7.81
    """
    # ln(P2/P1) = -DeltaH/R × (1/T2 - 1/T1)
    # DeltaH = -R × ln(P2/P1) / (1/T2 - 1/T1)
    ln_ratio = math.log(P2 / P1)
    deltaH_J = -R * ln_ratio / (1/T2 - 1/T1)
    return deltaH_J / 1000  # Convert to kJ/mol


def calculate_boiling_point_at_pressure(P_target: float, T_ref: float, P_ref: float,
                                          deltaH_vap: float) -> float:
    """
    Calculate boiling point at a target pressure.
    
    Uses Clausius-Clapeyron equation:
    ln(P_target/P_ref) = -DeltaH/R × (1/T_target - 1/T_ref)
    
    Args:
        P_target: Target pressure (atm)
        T_ref: Reference temperature (K) at P_ref
        P_ref: Reference pressure (atm) at T_ref
        deltaH_vap: Enthalpy of vaporization (kJ/mol)
    
    Returns:
        Boiling point at P_target (K)
    
    Examples:
        >>> # CCl4: P=54.0 kPa at 57.8°C, find Tb at 1 atm
        >>> calculate_boiling_point_at_pressure(1.0, 330.95, 54.0/101.325, 33.05)
        349.5...
    """
    deltaH_J = deltaH_vap * 1000
    
    # Rearranged Clausius-Clapeyron
    # ln(P_target/P_ref) = -DeltaH/R × (1/T_target - 1/T_ref)
    # 1/T_target = 1/T_ref - (R/DeltaH) × ln(P_target/P_ref)
    inv_T = 1/T_ref - R/deltaH_J * math.log(P_target / P_ref)
    
    return 1/inv_T


def antoine_equation(T: float, A: float, B: float, C: float,
                      T_min=None, T_max=None) -> float:
    """
    Calculate vapor pressure using Antoine equation.
    
    log10(P) = A - B/(T + C)
    
    Args:
        T: Temperature (K)
        A, B, C: Antoine coefficients (C is typically negative for many substances)
        T_min: Minimum valid temperature (K) for Antoine range
        T_max: Maximum valid temperature (K) for Antoine range
    
    Returns:
        Vapor pressure in bar
    
    Warning:
        The Antoine equation is only valid within its parameter range.
        Extrapolation outside the range gives wildly incorrect results.
        E.g., water at 200°C: Antoine gives ~123 bar, but actual is ~15.5 bar.
    
    Examples:
        >>> # Water: A=5.20389, B=1733.926, C=-39.485 (valid 1-100°C approx)
        >>> antoine_equation(373, 5.20389, 1733.926, -39.485)
        1.01...
    """
    import warnings
    if T_min is not None and T < T_min:
        warnings.warn(f"Temperature {T}K is below Antoine valid range ({T_min}K). "
                       f"Result may be inaccurate.", UserWarning)
    if T_max is not None and T > T_max:
        warnings.warn(f"Temperature {T}K exceeds Antoine valid range ({T_max}K). "
                       f"Result may be inaccurate. Use steam tables or "
                       f"Wagner equation for high temperatures.", UserWarning)
    
    log_P = A - B / (T + C)
    P_bar = 10 ** log_P
    
    # Safety clamp: cap at 1000 bar to prevent absurd extrapolations
    if P_bar > 1000:
        warnings.warn(f"Antoine gives P={P_bar:.1f} bar at {T}K — likely "
                       f"extrapolation error. Use steam tables.", UserWarning)
    return min(P_bar, 1000.0)


def antoine_equation_from_coefficients(T: float, coefficients: tuple) -> float:
    """
    Calculate vapor pressure using Antoine equation from coefficient tuple.
    
    Args:
        T: Temperature (K)
        coefficients: (A, B, C) Antoine coefficients
    
    Returns:
        Vapor pressure in bar
    """
    A, B, C = coefficients
    return antoine_equation(T, A, B, C)


def calculate_triple_point(Tb: float, Tm: float, deltaH_vap: float,
                             deltaH_fus: float) -> Dict:
    """
    Estimate triple point from melting and boiling data.
    
    Args:
        Tb: Normal boiling point (K)
        Tm: Normal melting point (K)
        deltaH_vap: Enthalpy of vaporization (kJ/mol)
        deltaH_fus: Enthalpy of fusion (kJ/mol)
    
    Returns:
        Dict with estimated triple point T and P
    """
    # Triple point temperature is approximately melting point at low P
    T_triple = Tm
    
    # Triple point pressure from Clausius-Clapeyron extrapolation
    # From solid-gas equilibrium
    deltaH_sub = deltaH_vap + deltaH_fus
    
    # Estimate P at triple point
    # P_triple ~ exp(-DeltaH_sub/R x (1/T_triple - 1/Tb))
    deltaH_sub_J = deltaH_sub * 1000
    ln_P_ratio = -deltaH_sub_J / R * (1/T_triple - 1/Tb)
    P_triple = math.exp(ln_P_ratio)
    
    return {'T': T_triple, 'P': P_triple}


def calculate_critical_properties(a: float, b: float) -> Dict:
    """
    Calculate critical properties from van der Waals parameters.
    
    Tc = 8a/(27Rb)
    Pc = a/(27b2)
    Vc = 3b
    
    Args:
        a: van der Waals 'a' parameter (L2·atm/mol2)
        b: van der Waals 'b' parameter (L/mol)
    
    Returns:
        Dict with Tc (K), Pc (atm), Vc (L/mol)
    """
    # Convert a to proper units (L2·atm/mol2 to J·m3/mol2)
    # For simplicity, use R = 0.0821 L·atm/(mol·K)
    R_L = 0.0821
    
    Tc = 8 * a / (27 * R_L * b)
    Pc = a / (27 * b**2)
    Vc = 3 * b
    
    return {'Tc': Tc, 'Pc': Pc, 'Vc': Vc}


def is_supercritical(substance: str, T: float, P: float) -> bool:
    """
    Check if substance is in supercritical state.
    
    Args:
        substance: Substance name
        T: Temperature (K)
        P: Pressure (atm)
    
    Returns:
        True if supercritical, False otherwise
    """
    critical = CRITICAL_POINTS.get(substance.lower(), {})
    Tc = critical.get('Tc', float('inf'))
    Pc = critical.get('Pc', float('inf'))
    
    return T > Tc and P > Pc


def get_phase_boundary_crossing(T1: float, P1: float, T2: float, P2: float,
                                  substance: str) -> List[Dict]:
    """
    Determine phase changes when moving from state 1 to state 2.
    
    Args:
        T1, P1: Initial temperature (K) and pressure (atm)
        T2, P2: Final temperature (K) and pressure (atm)
        substance: Substance name
    
    Returns:
        List of phase changes encountered
    """
    phase1 = identify_phase(substance, T1, P1)
    phase2 = identify_phase(substance, T2, P2)
    
    changes = []
    
    if phase1 != phase2:
        changes.append({
            'initial_phase': phase1,
            'final_phase': phase2,
            'process': f'{phase1}_to_{phase2}'
        })
    
    return changes


def calculate_sublimation_pressure(T: float, T_triple: float, P_triple: float,
                                     deltaH_sub: float) -> float:
    """
    Calculate sublimation pressure at temperature T.
    
    Args:
        T: Temperature (K)
        T_triple: Triple point temperature (K)
        P_triple: Triple point pressure (atm)
        deltaH_sub: Enthalpy of sublimation (kJ/mol)
    
    Returns:
        Sublimation pressure (atm)
    """
    deltaH_J = deltaH_sub * 1000
    
    ln_ratio = -deltaH_J / R * (1/T - 1/T_triple)
    P = P_triple * math.exp(ln_ratio)
    
    return P


def analyze_phase_diagram(substance: str) -> Dict:
    """
    Provide comprehensive analysis of a substance's phase diagram.
    
    Args:
        substance: Substance name
    
    Returns:
        Dict with all key phase diagram parameters
    """
    substance = substance.lower()
    
    result = {
        'substance': substance,
        'triple_point': TRIPLE_POINTS.get(substance, {}),
        'critical_point': CRITICAL_POINTS.get(substance, {}),
        'normal_melting_point': NORMAL_MELTING_POINTS.get(substance),
        'normal_boiling_point': NORMAL_BOILING_POINTS.get(substance),
        'deltaH_vap': ENTHALPIES_OF_VAPORIZATION.get(substance),
    }
    
    # Add analysis
    critical = result['critical_point']
    triple = result['triple_point']
    
    if critical and triple:
        result['temperature_range_liquid'] = {
            'min': triple.get('T', 0),
            'max': critical.get('Tc', float('inf'))
        }
        
        # Can liquid exist at 1 atm?
        Tm = result['normal_melting_point']
        Tb = result['normal_boiling_point']
        result['liquid_at_1atm'] = Tm is not None and Tb is not None
    
    return result


def predict_phase_at_stp(substance: str) -> str:
    """
    Predict phase at standard temperature and pressure (25degC, 1 atm).
    
    Args:
        substance: Substance name
    
    Returns:
        Phase at STP
    """
    return identify_phase(substance, 298.15, 1.0)


if __name__ == "__main__":
    # Example calculations
    print("Phase Analysis for Water:")
    water_analysis = analyze_phase_diagram('water')
    for key, value in water_analysis.items():
        print(f"  {key}: {value}")
    
    print("\nVapor Pressure Calculation:")
    P_vap = calculate_vapor_pressure(350, 373.15, 1.0, 40.7)
    print(f"  Water vapor pressure at 350 K: {P_vap:.3f} atm")
    
    print("\nPhase Identification:")
    print(f"  Water at 300 K, 1 atm: {identify_phase('water', 300, 1)}")
    print(f"  CO2 at 200 K, 1 atm: {identify_phase('CO2', 200, 1)}")
    print(f"  CO2 at 300 K, 100 atm: {identify_phase('CO2', 300, 100)}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="analyze_phase_diagram",
            description="Provide comprehensive analysis of a substance's phase diagram.",
            input_schema=[
            InputSchemaField(name="substance", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_boiling_point_at_pressure",
            description="Calculate boiling point at non-standard pressure.",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="Tb_normal", type="number", required=True),
            InputSchemaField(name="deltaH_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_critical_properties",
            description="Calculate critical properties from van der Waals parameters.",
            input_schema=[
            InputSchemaField(name="a", type="number", required=True),
            InputSchemaField(name="b", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_sublimation_pressure",
            description="Calculate sublimation pressure at temperature T.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="T_triple", type="number", required=True),
            InputSchemaField(name="P_triple", type="number", required=True),
            InputSchemaField(name="deltaH_sub", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_triple_point",
            description="Estimate triple point from melting and boiling data.",
            input_schema=[
            InputSchemaField(name="Tb", type="number", required=True),
            InputSchemaField(name="Tm", type="number", required=True),
            InputSchemaField(name="deltaH_vap", type="number", required=True),
            InputSchemaField(name="deltaH_fus", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_vapor_pressure",
            description="Calculate vapor pressure using Clausius-Clapeyron equation.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="T_ref", type="number", required=True),
            InputSchemaField(name="P_ref", type="number", required=True),
            InputSchemaField(name="deltaH_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="get_phase_boundary_crossing",
            description="Determine phase changes when moving from state 1 to state 2.",
            input_schema=[
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="P1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True),
            InputSchemaField(name="P2", type="number", required=True),
            InputSchemaField(name="substance", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="identify_phase",
            description="Identify the phase of a substance at given temperature and pressure.",
            input_schema=[
            InputSchemaField(name="substance", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="is_supercritical",
            description="Check if substance is in supercritical state.",
            input_schema=[
            InputSchemaField(name="substance", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_phase_at_stp",
            description="Predict phase at standard temperature and pressure (25degC, 1 atm).",
            input_schema=[
            InputSchemaField(name="substance", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
