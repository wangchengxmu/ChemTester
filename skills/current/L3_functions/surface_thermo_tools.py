"""Surface Thermodynamics Tools - Young-Laplace, Kelvin equation, adsorption isotherms."""

## Solver Instructions (for AI Agent)

# When you encounter **surface thermodynamics** problems (Young-Laplace, Kelvin equation, adsorption), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Surface tension + curvature radii -> pressure difference: `young_laplace(gamma, r1, r2)`
# - Vapor pressure ratio -> pore radius: `kelvin_radius(T, gamma, vm, p_ratio)`
# - Pressure + Langmuir constant -> adsorbed amount: `langmuir_adsorption(P, KL, qmax)`
# - BET monolayer amount + molecular area -> surface area: `bet_surface_area(n_monolayer, area_molecule, na)`

### Step 2: Choose the correct function
# - Capillary pressure / bubble pressure: `young_laplace`
# - Kelvin effect (small pores, nucleation): `kelvin_radius`
# - Monolayer adsorption: `langmuir_adsorption`
# - BET surface area from experiment: `bet_surface_area`

### Step 3: Handle special cases
# - For a sphere: r1 = r2 = r
# - For a cylinder: r1 = r, r2 = ∞
# - `kelvin_radius` uses p/p_sat ratio (p_ratio < 1 for concave meniscus)

### Examples
# 1. Water droplet (gamma=0.0728 N/m, r=1mum): `young_laplace(0.0728, 1e-6, 1e-6)` -> 1.456x105 Pa
# 2. Pore at T=298K, gamma=0.0728, Vm=18e-6 m3/mol, p/p0=0.9: `kelvin_radius(298, 0.0728, 18e-6, 0.9)` -> r~10.4 nm
# 3. BET: n_mono=2.5 mmol/g, area=0.162 nm2/molecule: `bet_surface_area(2.5e-3, 0.162e-18)` -> ~243 m2/g


import math

def young_laplace(gamma: float, r1: float, r2: float) -> float:
    """Young-Laplace equation: DeltaP = gamma(1/r1 + 1/r2)."""
    return gamma * (1.0/r1 + 1.0/r2)

def kelvin_radius(T: float, gamma: float, vm: float, p_ratio: float) -> float:
    """Kelvin equation: r = 2gammaV_m / (RT·ln(P/P0)). Returns pore radius."""
    R = 8.314
    ln_ratio = math.log(p_ratio)
    if ln_ratio == 0:
        return float('inf')
    return 2 * gamma * vm / (R * T * ln_ratio)

def langmuir_adsorption(P: float, KL: float, qmax: float) -> float:
    """Langmuir isotherm: q = qmax·KL·P / (1 + KL·P)."""
    return qmax * KL * P / (1.0 + KL * P)

def bet_surface_area(n_monolayer: float, area_molecule: float, na: float = 6.022e23) -> float:
    """BET surface area from monolayer capacity."""
    return n_monolayer * area_molecule * na


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="bet_surface_area",
            description="BET surface area from monolayer capacity.",
            input_schema=[
            InputSchemaField(name="n_monolayer", type="number", required=True),
            InputSchemaField(name="area_molecule", type="string", required=True),
            InputSchemaField(name="na", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="kelvin_radius",
            description="Kelvin equation: r = 2gammaV_m / (RT·ln(P/P0)). Returns pore radius.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="gamma", type="number", required=True),
            InputSchemaField(name="vm", type="number", required=True),
            InputSchemaField(name="p_ratio", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="langmuir_adsorption",
            description="Langmuir isotherm: q = qmax·KL·P / (1 + KL·P).",
            input_schema=[
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="KL", type="number", required=True),
            InputSchemaField(name="qmax", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="young_laplace",
            description="Young-Laplace equation: DeltaP = gamma(1/r1 + 1/r2).",
            input_schema=[
            InputSchemaField(name="gamma", type="number", required=True),
            InputSchemaField(name="r1", type="number", required=True),
            InputSchemaField(name="r2", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
