"""
Non-ideal Gases Tools - Compressibility, fugacity, virial equation.

## Solver Instructions (for AI Agent)

When you encounter non-ideal gas problems (compressibility, fugacity, virial equation), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given P, V, T -> calculate compressibility factor Z?
- Given second virial coefficient -> calculate Z from virial equation?
- Given Z -> calculate fugacity coefficient?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Compressibility factor | `compressibility_factor(p, v_mol, R, T)` | Z = PV/(nRT), p in Pa, v_mol in m3/mol |
| Virial equation (2nd order) | `virial_z_b(T, B, P, R)` | Z = 1 + BP/(RT), B is 2nd virial coeff |
| Fugacity coefficient | `fugacity_coefficient_z(Z)` | φ ~ exp(Z - 1 - ln Z) |

### Step 3: Handle special cases
- Z = 1: ideal gas behavior
- Z < 1: attractive forces dominate (typical at moderate T, high P)
- Z > 1: repulsive forces dominate (high T, very high P)
- B < 0: attractive interactions; B > 0: repulsive interactions

### Examples
```python
# Example 1: Compressibility factor
compressibility_factor(1e6, 0.024, 8.314, 298)  # 1 MPa, 0.024 m3/mol
# -> Z ~ 0.97

# Example 2: Virial equation
virial_z_b(298, -0.0001, 1e6)  # B = -100 cm3/mol, P = 1 MPa
# -> Z ~ 0.96

# Example 3: Fugacity coefficient
fugacity_coefficient_z(0.97)
# -> φ ~ 0.976
```
"""
import math

def compressibility_factor(p: float, v_mol: float, R: float = 8.314, T: float = 298.15) -> float:
    """Compressibility factor: Z = PV/(nRT)."""
    return p * v_mol / (R * T)

def virial_z_b(T: float, B: float, P: float, R: float = 8.314) -> float:
    """Virial equation (2nd order): Z = 1 + B·P/(RT)."""
    return 1.0 + B * P / (R * T)

def fugacity_coefficient_z(Z: float) -> float:
    """Approximate fugacity coefficient from compressibility factor."""
    if Z <= 0:
        raise ValueError("Z must be positive")
    return math.exp(Z - 1 - math.log(Z))


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="compressibility_factor",
            description="Compressibility factor: Z = PV/(nRT).",
            input_schema=[
            InputSchemaField(name="p", type="number", required=True),
            InputSchemaField(name="v_mol", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False),
            InputSchemaField(name="T", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fugacity_coefficient_z",
            description="Approximate fugacity coefficient from compressibility factor.",
            input_schema=[
            InputSchemaField(name="Z", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="virial_z_b",
            description="Virial equation (2nd order): Z = 1 + B·P/(RT).",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="B", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True),
            InputSchemaField(name="R", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
