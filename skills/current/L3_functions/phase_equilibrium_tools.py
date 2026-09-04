"""
Phase Equilibrium Tools - Clapeyron, Clausius-Clapeyron, phase rule.

## Solver Instructions (for AI Agent)

When you encounter phase equilibrium problems (Clapeyron, Clausius-Clapeyron, phase rule), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given DeltaH, DeltaV, T -> calculate dP/dT (Clapeyron)?
- Given T1, P1, T2, DeltaHvap -> calculate P2 (Clausius-Clapeyron)?
- Given components and phases -> calculate degrees of freedom (Gibbs phase rule)?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Clapeyron equation | `clapeyron_dp_dt(dh, dv, T)` | dP/dT = DeltaH/(T·DeltaV) |
| Clausius-Clapeyron | `clausius_clapeyron(T1, P1, T2, dh_vap)` | Returns P2 |
| Gibbs phase rule | `gibbs_phase_rule(components, phases)` | F = C - P + 2 |

### Step 3: Handle special cases
- Clapeyron: exact equation for any phase transition
- Clausius-Clapeyron: approximates DeltaV ~ Vgas, assumes ideal gas
- Phase rule: F ≥ 0 for valid systems

### Examples
```python
# Example 1: Clapeyron for ice-water transition
clapeyron_dp_dt(6008, -1.63e-6, 273)  # DeltaH=6008 J/mol, DeltaV=-1.63e-6 m3/mol
# -> -13.5 MPa/K (negative slope for water!)

# Example 2: Clausius-Clapeyron
clausius_clapeyron(373, 1, 298, 40700)  # Water
# -> ~0.031 atm

# Example 3: Gibbs phase rule
gibbs_phase_rule(2, 2)  # Binary mixture, 2 phases
# -> F = 2
```
"""
import math

def clapeyron_dp_dt(dh: float, dv: float, T: float) -> float:
    """Clapeyron equation: dP/dT = DeltaH / (T·DeltaV)."""
    if dv == 0:
        raise ValueError("DeltaV cannot be zero")
    return dh / (T * dv)

def clausius_clapeyron(T1: float, P1: float, T2: float, dh_vap: float) -> float:
    """Clausius-Clapeyron: ln(P2/P1) = -DeltaH_vap/R · (1/T2 - 1/T1). Returns P2."""
    R = 8.314
    ln_ratio = -dh_vap / R * (1.0/T2 - 1.0/T1)
    return P1 * math.exp(ln_ratio)

def gibbs_phase_rule(components: int, phases: int) -> int:
    """Gibbs phase rule: F = C - P + 2."""
    return components - phases + 2


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="clapeyron_dp_dt",
            description="Clapeyron equation: dP/dT = DeltaH / (T·DeltaV).",
            input_schema=[
            InputSchemaField(name="dh", type="number", required=True),
            InputSchemaField(name="dv", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="clausius_clapeyron",
            description="Clausius-Clapeyron: ln(P2/P1) = -DeltaH_vap/R · (1/T2 - 1/T1). Returns P2.",
            input_schema=[
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="P1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True),
            InputSchemaField(name="dh_vap", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_phase_rule",
            description="Gibbs phase rule: F = C - P + 2.",
            input_schema=[
            InputSchemaField(name="components", type="number", required=True),
            InputSchemaField(name="phases", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
