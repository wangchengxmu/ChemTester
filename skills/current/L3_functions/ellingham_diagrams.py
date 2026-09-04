"""
Ellingham Diagrams - L3 Implementation

Thermodynamic calculations for oxide reduction and metallurgical extraction.
Source: TLP Library I (DoITPoMS), Ch25
## Solver Instructions (for AI Agent)

When you encounter Ellingham diagram or oxide reduction problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given DeltaHdeg, DeltaSdeg, T -> Calculate DeltaGdeg? Use `gibbs_energy_formation(dH, dS, T)`
- Given DeltaGdeg and T -> Find equilibrium pO2? Use `equilibrium_po2(dG, T)`
- Compare two oxides -> Can one reduce the other? Use `reduction_feasibility(dG_oxide1, dG_oxide2)`
- Need CO/CO2 or H2/H2O ratio for reduction? Use `co_co2_ratio(dG, T)` or `h2_h2o_ratio(dG, T)`
- Find T at specific pO2? Use `temperature_for_po2(dH, dS, pO2_target)`
- Generate Ellingham diagram data? Use `ellingham_line(dH, dS, T_range)`
- Get standard oxide data? Use `get_oxide_data(oxide_name)` - returns dH, dS for common oxides

### Step 2: Choose the correct function
| Scenario | Function | Key Notes |
|----------|----------|-----------|
| DeltaGdeg at given T | `gibbs_energy_formation(dH, dS, T)` | dH/dS in J/mol |
| Equilibrium pO2 | `equilibrium_po2(dG, T)` | Returns atm |
| Reduction feasibility | `reduction_feasibility(dG_oxide1, dG_oxide2)` | True if oxide1 line is below oxide2 |
| CO/CO2 ratio needed | `co_co2_ratio(dG, T)` | For carbon reduction |
| H2/H2O ratio needed | `h2_h2o_ratio(dG, T)` | For hydrogen reduction |
| T for target pO2 | `temperature_for_po2(dH, dS, pO2_target)` | Solves T = DeltaH/(DeltaS + R·ln(pO2)) |
| Rank oxide stability | `compare_oxide_stability(dG_values)` | Most negative DeltaG = most stable |

### Step 3: Handle special cases
- **Units**: All dH, dS, dG values are in J/mol (not kJ/mol!)
- **Ellingham diagrams**: Lower line on diagram = more stable oxide. A lower oxide can reduce oxides above it.
- **CO exception**: The C -> CO line has positive DeltaS (slope goes upward), making carbon a better reductant at high T
- **OXIDE_DATA dict**: Contains pre-loaded dH, dS for Al2O3, FeO, Fe2O3, ZnO, MgO, CaO, SiO2, CO, CO2

### Examples
```python
# Example 1: Can Al reduce FeO at 1000degC?
dG_Al = gibbs_energy_formation(-1675700, -313, 1273)
dG_Fe = gibbs_energy_formation(-272000, -66.7, 1273)
reduction_feasibility(dG_Al, dG_Fe)  # True (Al2O3 more stable than FeO)

# Example 2: Equilibrium pO2 for ZnO at 800degC
dG = gibbs_energy_formation(-350000, -100, 1073)
equilibrium_po2(dG, 1073)  # Very small number (ZnO very stable)

# Example 3: CO/CO2 ratio to reduce FeO at 1000degC
co_co2_ratio(-272000 - (-393500), 1273)  # DeltaG for FeO + CO -> Fe + CO2
```
"""

import math
from typing import Tuple, Optional


def gibbs_energy_formation(dH: float, dS: float, T: float) -> float:
    """
    Calculate standard Gibbs free energy for oxide formation.
    
    DeltaGdeg = DeltaHdeg - T·DeltaSdeg
    
    Args:
        dH: Standard enthalpy change (J/mol)
        dS: Standard entropy change (J/mol·K)
        T: Temperature (K)
    
    Returns:
        Standard Gibbs free energy change (J/mol)
    """
    return dH - T * dS


def equilibrium_po2(dG: float, T: float, R: float = 8.314) -> float:
    """
    Calculate equilibrium oxygen partial pressure.
    
    DeltaGdeg = RT ln(pO2)
    pO2 = exp(DeltaGdeg / RT)
    
    Args:
        dG: Gibbs free energy change (J/mol)
        T: Temperature (K)
        R: Gas constant (J/mol·K)
    
    Returns:
        Equilibrium pO2 (atm)
    """
    return math.exp(dG / (R * T))


def po2_from_gibbs(dG: float, T: float, R: float = 8.314) -> float:
    """
    Calculate pO2 from Gibbs free energy (alias for equilibrium_po2).
    
    Args:
        dG: Gibbs free energy (J/mol)
        T: Temperature (K)
        R: Gas constant
    
    Returns:
        Equilibrium pO2 (atm)
    """
    return equilibrium_po2(dG, T, R)


def reduction_feasibility(dG_oxide1: float, dG_oxide2: float) -> bool:
    """
    Determine if oxide2 can be reduced by element forming oxide1.
    
    Reduction feasible if DeltaG(oxide2) > DeltaG(oxide1)
    
    Args:
        dG_oxide1: DeltaGdeg for reductant oxide (J/mol)
        dG_oxide2: DeltaGdeg for target oxide (J/mol)
    
    Returns:
        True if reduction is thermodynamically feasible
    """
    return dG_oxide2 > dG_oxide1


def temperature_for_po2(dH: float, dS: float, pO2_target: float, 
                         R: float = 8.314) -> float:
    """
    Calculate temperature at which equilibrium pO2 equals target.
    
    DeltaGdeg = DeltaHdeg - TDeltaSdeg = RT ln(pO2)
    T = DeltaHdeg / (DeltaSdeg + R ln(pO2))
    
    Args:
        dH: Standard enthalpy change (J/mol)
        dS: Standard entropy change (J/mol·K)
        pO2_target: Target oxygen partial pressure (atm)
        R: Gas constant (J/mol·K)
    
    Returns:
        Temperature (K)
    """
    return dH / (dS + R * math.log(pO2_target))


def co_co2_ratio(dG: float, T: float, R: float = 8.314) -> float:
    """
    Calculate required CO/CO2 ratio for reduction at given T.
    
    For: MO + CO -> M + CO2
    K = pCO2/pCO
    
    Args:
        dG: Gibbs free energy for reduction (J/mol)
        T: Temperature (K)
        R: Gas constant
    
    Returns:
        CO/CO2 ratio required
    """
    K = math.exp(-dG / (R * T))
    return 1 / K if K > 0 else float('inf')


def h2_h2o_ratio(dG: float, T: float, R: float = 8.314) -> float:
    """
    Calculate required H2/H2O ratio for reduction at given T.
    
    For: MO + H2 -> M + H2O
    K = pH2O/pH2
    
    Args:
        dG: Gibbs free energy for reduction (J/mol)
        T: Temperature (K)
        R: Gas constant
    
    Returns:
        H2/H2O ratio required
    """
    K = math.exp(-dG / (R * T))
    return 1 / K if K > 0 else float('inf')


def ellingham_line(dH: float, dS: float, T_range: Tuple[float, float], 
                   n_points: int = 100) -> list:
    """
    Generate points for Ellingham diagram line.
    
    Args:
        dH: Standard enthalpy (J/mol)
        dS: Standard entropy (J/mol·K)
        T_range: (T_min, T_max) in Kelvin
        n_points: Number of points
    
    Returns:
        List of (T, DeltaGdeg) tuples
    """
    T_min, T_max = T_range
    step = (T_max - T_min) / (n_points - 1)
    points = []
    for i in range(n_points):
        T = T_min + i * step
        dG = gibbs_energy_formation(dH, dS, T)
        points.append((T, dG))
    return points


def compare_oxide_stability(dG_values: dict) -> list:
    """
    Rank oxides by stability (most stable first).
    
    Args:
        dG_values: Dict of {oxide_name: DeltaGdeg value}
    
    Returns:
        List of (oxide_name, DeltaGdeg) sorted by stability
    """
    return sorted(dG_values.items(), key=lambda x: x[1])


# Standard thermodynamic data for common oxides (J/mol)
OXIDE_DATA = {
    'Al2O3': {'dH': -1675700, 'dS': -313},   # 2Al + 1.5O2 -> Al2O3
    'FeO': {'dH': -272000, 'dS': -66.7},     # Fe + 0.5O2 -> FeO
    'Fe2O3': {'dH': -822000, 'dS': -87},     # 2Fe + 1.5O2 -> Fe2O3
    'ZnO': {'dH': -350000, 'dS': -100},      # Zn + 0.5O2 -> ZnO
    'MgO': {'dH': -601500, 'dS': -107},      # Mg + 0.5O2 -> MgO
    'CaO': {'dH': -635000, 'dS': -98},       # Ca + 0.5O2 -> CaO
    'SiO2': {'dH': -910000, 'dS': -182},     # Si + O2 -> SiO2
    'CO': {'dH': -110500, 'dS': 89.5},       # C + 0.5O2 -> CO (per mole O2)
    'CO2': {'dH': -393500, 'dS': 3},         # C + O2 -> CO2
}


def get_oxide_data(oxide_name: str) -> Optional[dict]:
    """
    Get thermodynamic data for common oxide.
    
    Args:
        oxide_name: Name of oxide (e.g., 'Al2O3', 'FeO')
    
    Returns:
        Dict with 'dH' and 'dS' or None if not found
    """
    return OXIDE_DATA.get(oxide_name)


if __name__ == "__main__":
    # Example: Calculate pO2 for Al2O3 at 1000degC
    T = 1273  # K
    data = OXIDE_DATA['Al2O3']
    dG = gibbs_energy_formation(data['dH'], data['dS'], T)
    pO2 = equilibrium_po2(dG, T)
    print(f"Al2O3 at {T}K: DeltaGdeg = {dG/1000:.1f} kJ/mol, pO2 = {pO2:.2e} atm")
