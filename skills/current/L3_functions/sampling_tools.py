"""
Sampling Tools - Enhanced sampling helpers.

## Solver Instructions (for AI Agent)

When you encounter enhanced sampling / molecular dynamics problems (replica exchange, umbrella sampling, WHAM), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Replica exchange**: Given energy difference and two temperatures -> acceptance probability
- **Umbrella sampling**: Given reaction coordinate position, target position, force constant -> bias potential
- **WHAM**: Given trajectories from multiple windows -> combine into free energy profile

### Step 2: Choose the correct function
- `replica_exchange_prob(dE, T1, T2)` -> min(1, exp(-beta1DeltaE + beta2DeltaE)) acceptance probability
- `umbrella_bias(xi, xi0, k)` -> V = 0.5·k·(xi - xi0)2
- `wham_weights(trajs, kBT)` -> placeholder returning uniform weights

### Step 3: Handle special cases
- If dE ≤ 0, replica exchange always accepted (probability = 1.0)
- T1 and T2 are in Kelvin; R = 8.314 J/(mol·K)
- Umbrella bias is always non-negative (minimum of 0 at xi=xi0)
- Typical k values: 100-2000 kJ/(mol·nm2) for umbrella sampling

### Examples
1. **Replica exchange**: dE = 5.0 kJ/mol, T1=300 K, T2=350 K
   -> `replica_exchange_prob(5000, 300, 350)` -> ~0.38 (moderate acceptance)

2. **Umbrella bias**: xi=0.5 nm, target xi0=0.3 nm, k=1000 kJ/(mol·nm2)
   -> `umbrella_bias(0.5, 0.3, 1000)` -> 0.5x1000x(0.2)2 = 20.0 kJ/mol
"""
import math, random

def replica_exchange_prob(dE: float, T1: float, T2: float) -> float:
    """Replica exchange acceptance probability."""
    R = 8.314
    if dE <= 0:
        return 1.0
    beta_diff = 1.0/(R*T1) - 1.0/(R*T2)
    return min(1.0, math.exp(-beta_diff * dE))

def umbrella_bias(xi: float, xi0: float, k: float) -> float:
    """Umbrella sampling bias potential: V = 0.5·k·(xi - xi0)^2."""
    return 0.5 * k * (xi - xi0)**2

def wham_weights(trajs, kBT: float) -> list:
    """Placeholder for WHAM weight computation. Returns uniform weights."""
    return [1.0 / len(trajs)] * len(trajs)


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="replica_exchange_prob",
            description="Replica exchange acceptance probability.",
            input_schema=[
            InputSchemaField(name="dE", type="number", required=True),
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="umbrella_bias",
            description="Umbrella sampling bias potential: V = 0.5·k·(xi - xi0)^2.",
            input_schema=[
            InputSchemaField(name="xi", type="number", required=True),
            InputSchemaField(name="xi0", type="number", required=True),
            InputSchemaField(name="k", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wham_weights",
            description="Placeholder for WHAM weight computation. Returns uniform weights.",
            input_schema=[
            InputSchemaField(name="trajs", type="number", required=True),
            InputSchemaField(name="kBT", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
