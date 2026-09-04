"""VLE Tools - Vapor-Liquid Equilibrium, bubble/dew point, azeotrope detection."""

## Solver Instructions (for AI Agent)

# When you encounter **vapor-liquid equilibrium (VLE)** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Bubble point pressure from liquid compositions: `bubble_pressure(xs, Psat_func, T)`
# - Dew point pressure from vapor compositions: `dew_pressure(ys, Psat_func, T)`
# - Relative volatility: `relative_volatility(Psat1, Psat2)`

### Step 2: Choose the correct function
# - Bubble point (first bubble of vapor): `bubble_pressure`
# - Dew point (first drop of liquid): `dew_pressure`
# - Separation feasibility: `relative_volatility` - alpha > 1 indicates the first component is more volatile

### Step 3: Handle special cases
# - `Psat_func` should be a callable (function) that returns P_sat for a given component at T
# - `xs` and `ys` are lists of liquid/vapor mole fractions that must sum to 1
# - Relative volatility near 1 -> difficult separation

### Examples
# 1. Benzene-toluene at 373 K: `bubble_pressure([0.5, 0.5], lambda comp, T: Antoine(comp, T), 373)`
# 2. Relative volatility: `relative_volatility(101.3, 40.0)` -> alpha~2.53 (benzene more volatile)


import math

def bubble_pressure(xs, Psat_func, T):
    """Calculate bubble pressure given liquid mole fractions and T."""
    return sum(x * Psat_func(i, T) for i, x in enumerate(xs))

def dew_pressure(ys, Psat_func, T):
    """Calculate dew pressure given vapor mole fractions and T."""
    denom = sum(y / Psat_func(i, T) for i, y in enumerate(ys))
    return 1.0 / denom

def relative_volatility(Psat1: float, Psat2: float) -> float:
    """Relative volatility alpha = Psat1 / Psat2."""
    if Psat2 == 0:
        raise ValueError("Psat2 cannot be zero")
    return Psat1 / Psat2


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="bubble_pressure",
            description="Calculate bubble pressure given liquid mole fractions and T.",
            input_schema=[
            InputSchemaField(name="xs", type="number", required=True),
            InputSchemaField(name="Psat_func", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dew_pressure",
            description="Calculate dew pressure given vapor mole fractions and T.",
            input_schema=[
            InputSchemaField(name="ys", type="number", required=True),
            InputSchemaField(name="Psat_func", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="relative_volatility",
            description="Relative volatility alpha = Psat1 / Psat2.",
            input_schema=[
            InputSchemaField(name="Psat1", type="number", required=True),
            InputSchemaField(name="Psat2", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
