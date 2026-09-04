"""
MOF/COF computational tools for surface area, porosity, gas uptake, and topology analysis.

## Solver Instructions (for AI Agent)

When you encounter MOF (metal-organic framework) or COF (covalent organic framework) problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given adsorption isotherm data -> calculate BET surface area?
- Given adsorbed amount at saturation -> calculate pore volume?
- Given surface area and conditions -> predict gas uptake?
- Given coordination and linker -> classify topology?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| BET surface area | `surface_area_bet(n_adsorbed, p_relative, cross_section)` | n in mmol/g, P/P0 in 0.05-0.30 range |
| Pore volume | `pore_volume_calc(n_adsorbed_sat, molar_volume)` | at P/P0 ~ 0.99 |
| Gas uptake prediction | `gas_uptake_prediction(surface_area, pressure, temperature, gas)` | Langmuir model |
| Topology classification | `topology_classify(coordination, linker)` | e.g., 'tetrahedral', 'octahedral' |
| Langmuir fit | `langmuir_fit(pressures, uptakes)` | Returns q_max and K_L |

### Step 3: Handle special cases
- BET: Use P/P0 range 0.05-0.30 for valid linear fit
- N2 cross-section = 0.162 nm2 (standard)
- Gas uptake: Uses empirical SA/mmol relationships and default Qst values

### Examples
```python
# Example 1: BET surface area
n_ads = [2.5, 3.8, 4.9, 5.8, 6.5]  # mmol/g
p_rel = [0.05, 0.10, 0.15, 0.20, 0.25]
surface_area_bet(n_ads, p_rel)
# -> {'bet_surface_area': ~500, 'c_constant': ..., 'monolayer_capacity': ...}

# Example 2: Pore volume
pore_volume_calc(15.0)  # 15 mmol/g at P/P0 ~ 0.99
# -> ~0.336 cm3/g

# Example 3: H2 uptake prediction
gas_uptake_prediction(2000, 50, 77, gas='H2')
# -> uptake at 77K, 50 bar
```
"""

from typing import Optional
import math


def surface_area_bet(n_adsorbed: list, p_relative: list, cross_section: float = 0.162) -> dict:
    """
    Calculate BET surface area from adsorption isotherm data.
    
    Parameters:
        n_adsorbed: Amount adsorbed (mmol/g) at each P/P0
        p_relative: Relative pressures (P/P0), typically 0.05-0.30
        cross_section: N2 cross-sectional area (nm^2), default 0.162
    
    Returns:
        dict with bet_surface_area (m^2/g), c_constant, monolayer_capacity
    """
    # BET equation: P/(n(P0-P)) = 1/(n_m * C) + (C-1)/(n_m * C) * P/P0
    # Linear fit: y = m*x + b where y = P/(n(P0-P)), x = P/P0
    
    x_data, y_data = [], []
    for n, p in zip(n_adsorbed, p_relative):
        if 0.05 <= p <= 0.30 and n > 0:
            y = p / (n * (1 - p))
            x = p
            x_data.append(x)
            y_data.append(y)
    
    if len(x_data) < 3:
        return {"error": "Insufficient data points in BET range (0.05-0.30 P/P0)", "bet_surface_area": 0, "c_constant": 0, "monolayer_capacity": 0}
    
    n = len(x_data)
    sum_x = sum(x_data)
    sum_y = sum(y_data)
    sum_xy = sum(x * y for x, y in zip(x_data, y_data))
    sum_x2 = sum(x * x for x in x_data)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    if slope <= 0 or intercept < 0:
        return {"error": "Invalid BET parameters (negative intercept or slope)", "bet_surface_area": 0, "c_constant": 0, "monolayer_capacity": 0}
    
    n_m = 1.0 / (slope + intercept)  # monolayer capacity in mmol/g
    c = slope / intercept + 1 if intercept > 0 else 0
    
    # SA = n_m * N_A * sigma * 1e-18  (mmol -> mol, nm^2 -> m^2)
    N_A = 6.022e23
    sa = n_m * 1e-3 * N_A * cross_section * 1e-18  # m^2/g
    
    return {
        "bet_surface_area": round(sa, 1),
        "c_constant": round(c, 2),
        "monolayer_capacity": round(n_m, 4),
        "data_points_used": len(x_data)
    }


def pore_volume_calc(n_adsorbed_sat: float, molar_volume: float = 22.414) -> float:
    """
    Calculate total pore volume from adsorption at saturation (P/P0 ~ 0.99).
    
    Parameters:
        n_adsorbed_sat: Amount adsorbed at P/P0 ~ 0.99 (mmol/g)
        molar_volume: Molar volume of adsorbate (cm^3/mol) at STP, default N2
    
    Returns:
        Pore volume in cm^3/g
    """
    v_pore = n_adsorbed_sat * 1e-3 * molar_volume
    return round(v_pore, 4)


def gas_uptake_prediction(surface_area: float, pressure: float, temperature: float,
                          gas: str = "N2", isosteric_heat: Optional[float] = None) -> dict:
    """
    Estimate gas uptake using simplified Langmuir model.
    
    Parameters:
        surface_area: BET surface area (m^2/g)
        pressure: Pressure (bar)
        temperature: Temperature (K)
        gas: Gas type ('H2', 'CH4', 'CO2', 'N2')
        isosteric_heat: Isosteric heat of adsorption Qst (kJ/mol), default by gas
    
    Returns:
        dict with uptake_mmol_g, uptake_wt_pct, uptake_g_cm3
    """
    # Approximate saturation capacities based on surface area
    # n_max ~ SA / (SA_per_mmol) - empirical relationship
    sa_per_mmol = {
        "H2": 200,    # ~200 m^2/g per mmol H2/g at 77K
        "CH4": 350,   # ~350 m^2/g per mmol CH4/g at 298K
        "CO2": 150,   # ~150 m^2/g per mmol CO2/g at 298K
        "N2": 200,    # ~200 m^2/g per mmol N2/g at 77K
    }
    default_qst = {"H2": 5.0, "CH4": 15.0, "CO2": 25.0, "N2": 8.0}
    
    if gas not in sa_per_mmol:
        return {"error": f"Unsupported gas: {gas}"}
    
    n_max = surface_area / sa_per_mmol[gas]
    Qst = (isosteric_heat or default_qst[gas]) * 1000  # J/mol
    R = 8.314
    
    b = math.exp(Qst / (R * temperature)) / 1.01325e5  # bar^-1
    uptake = n_max * b * pressure / (1 + b * pressure)
    
    mol_weight = {"H2": 2.016, "CH4": 16.04, "CO2": 44.01, "N2": 28.01}
    molar_vol_gas = {"H2": 22.414, "CH4": 22.414, "CO2": 22.414, "N2": 22.414}
    mw = mol_weight[gas]
    
    return {
        "uptake_mmol_g": round(uptake, 3),
        "uptake_wt_pct": round(uptake * mw / (1 + uptake * mw) * 100, 2),
        "gas": gas,
        "pressure_bar": pressure,
        "temperature_K": temperature
    }


def topology_analysis(connectivity_node: int, connectivity_linker: int) -> dict:
    """
    Predict net topology from node and linker connectivity.
    
    Parameters:
        connectivity_node: Number of connecting points on the node/SBU
        connectivity_linker: Number of connecting points on the linker
    
    Returns:
        dict with topology info
    """
    topology_db = {
        (6, 2): {"net": "pcu", "name": "Primitive Cubic", "example": "MOF-5 (IRMOF-1)"},
        (4, 2): {"net": "nbo", "name": "Niobium Oxide / Sodalite", "example": "ZIF-8"},
        (12, 2): {"net": "fcu", "name": "Face-Centered Cubic", "example": "UiO-66"},
        (4, 3): {"net": "spn", "name": "SrSi2 Net", "example": "HKUST-1"},
        (6, 3): {"net": "acs", "name": "Acetate", "example": "MIL-88"},
        (8, 2): {"net": "bcu", "name": "Body-Centered Cubic", "example": "MIL-100/MIL-101"},
        (6, 4): {"net": "soc", "name": "Squashed Octahedron", "example": "MOF-74 (CPO-27)"},
        (3, 2): {"net": "hcb", "name": "Honeycomb", "example": "2D COFs (COF-1)"},
        (4, 4): {"net": "pts", "name": "Platinum Sulfide", "example": "COF-300 (3D)"},
    }
    
    key = (connectivity_node, connectivity_linker)
    if key in topology_db:
        result = topology_db[key]
    else:
        # Check swapped (some MOFs have linker as the higher-connectivity component)
        key2 = (connectivity_linker, connectivity_node)
        if key2 in topology_db:
            result = topology_db[key2]
            result["note"] = f"Node/linker assignments may be swapped"
        else:
            result = {"net": "unknown", "name": "Unknown topology", "example": "Check RCSR database"}
    
    result["connectivity_node"] = connectivity_node
    result["connectivity_linker"] = connectivity_linker
    return result


def framework_density_calc(molar_mass: float, unit_cell_volume: float, z: int = 1) -> dict:
    """
    Calculate crystal framework density.
    
    Parameters:
        molar_mass: Molar mass of formula unit (g/mol)
        unit_cell_volume: Unit cell volume (Å^3)
        z: Number of formula units per unit cell
    
    Returns:
        dict with density (g/cm^3), packing coefficient info
    """
    N_A = 6.022e23
    mass = molar_mass * z  # g/mol per cell
    vol_cm3 = unit_cell_volume * 1e-24  # Å^3 to cm^3
    density = mass / (N_A * vol_cm3)
    
    return {
        "density_g_cm3": round(density, 4),
        "molar_mass_g_mol": molar_mass,
        "cell_volume_A3": unit_cell_volume,
        "z": z
    }


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="framework_density_calc",
            description="Calculate crystal framework density.",
            input_schema=[
            InputSchemaField(name="molar_mass", type="number", required=True),
            InputSchemaField(name="unit_cell_volume", type="number", required=True),
            InputSchemaField(name="z", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gas_uptake_prediction",
            description="Estimate gas uptake using simplified Langmuir model.",
            input_schema=[
            InputSchemaField(name="surface_area", type="number", required=True),
            InputSchemaField(name="pressure", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=True),
            InputSchemaField(name="gas", type="number", required=False),
            InputSchemaField(name="isosteric_heat", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pore_volume_calc",
            description="Calculate total pore volume from adsorption at saturation (P/P0 ~ 0.99).",
            input_schema=[
            InputSchemaField(name="n_adsorbed_sat", type="number", required=True),
            InputSchemaField(name="molar_volume", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="surface_area_bet",
            description="Calculate BET surface area from adsorption isotherm data.",
            input_schema=[
            InputSchemaField(name="n_adsorbed", type="number", required=True),
            InputSchemaField(name="p_relative", type="number", required=True),
            InputSchemaField(name="cross_section", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="topology_analysis",
            description="Predict net topology from node and linker connectivity.",
            input_schema=[
            InputSchemaField(name="connectivity_node", type="number", required=True),
            InputSchemaField(name="connectivity_linker", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
