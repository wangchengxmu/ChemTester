"""
Nonideal Mixture Tools - Activity coefficients, Raoult's/Henry's law, azeotropes.

## Solver Instructions (for AI Agent)

When you encounter nonideal mixture problems (activity coefficients, VLE, azeotropes), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given mole fraction and pure vapor pressure -> calculate partial pressure (Raoult's law)?
- Given concentration -> calculate partial pressure (Henry's law)?
- Given mole fraction and Margules parameter -> calculate activity coefficient?
- Given mixture composition -> calculate bubble point temperature?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Raoult's law | `raoult_pv(x, pvap_pure)` | Pᵢ = xᵢ x Pᵢ* |
| Henry's law | `henry_law(c, kh)` | P = kH x c |
| Margules activity coeff | `margules_one_suffix(x1, A12)` | gamma1 = exp(A12 x x22) |
| Bubble point | `bubble_point_temperature(xs, Psat_func, P_total)` | Iterative solution |

### Step 3: Handle special cases
- Raoult's law: valid for solvent in dilute solutions or ideal mixtures
- Henry's law: valid for solute in dilute solutions
- Margules: A12 > 0 indicates positive deviation (repulsion); A12 < 0 negative deviation
- Azeotrope: occurs when xᵢ = yᵢ (cannot be separated by simple distillation)

### Examples
```python
# Example 1: Raoult's law
raoult_pv(0.5, 0.1)  # x=0.5, P*vap = 0.1 atm
# -> 0.05 atm

# Example 2: Henry's law
henry_law(0.01, 100)  # c = 0.01 M, kH = 100 atm/M
# -> 1.0 atm

# Example 3: Margules activity coefficient
margules_one_suffix(0.3, 1.0)  # x1=0.3, A12=1.0
# -> gamma1 ~ 1.60

# Example 4: Bubble point (simplified)
# bubble_point_temperature([0.5, 0.5], antoine_func, 101325)
# -> temperature where sum(xᵢ x Pᵢ*(T)) = P_total
```
"""
import math

def raoult_pv(x: float, pvap_pure: float) -> float:
    """Raoult's law: P_i = x_i · P_i*."""
    return x * pvap_pure

def henry_law(c: float, kh: float) -> float:
    """Henry's law: P = k_H · c."""
    return kh * c

def margules_one_suffix(x1: float, A12: float) -> float:
    """One-suffix Margules activity coefficient for component 1."""
    if x1 <= 0 or x1 >= 1:
        raise ValueError("Mole fraction must be between 0 and 1")
    x2 = 1.0 - x1
    return math.exp(A12 * x2**2)

def bubble_point_temperature(xs, Psat_func, P_total=101325, tol=0.01):
    """Simple bubble point calculation via iterative search."""
    T_low, T_high = 200.0, 600.0
    for _ in range(100):
        T_mid = (T_low + T_high) / 2
        Ps = [Psat_func(x, T_mid) for x in xs]
        p_sum = sum(x * p for x, p in zip(xs, Ps))
        if abs(p_sum - P_total) < tol:
            return T_mid
        if p_sum < P_total:
            T_low = T_mid
        else:
            T_high = T_mid
    return T_mid


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="bubble_point_temperature",
            description="Simple bubble point calculation via iterative search.",
            input_schema=[
            InputSchemaField(name="xs", type="number", required=True),
            InputSchemaField(name="Psat_func", type="number", required=True),
            InputSchemaField(name="P_total", type="number", required=False),
            InputSchemaField(name="tol", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="henry_law",
            description="Henry's law: P = k_H · c.",
            input_schema=[
            InputSchemaField(name="c", type="number", required=True),
            InputSchemaField(name="kh", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="margules_one_suffix",
            description="One-suffix Margules activity coefficient for component 1.",
            input_schema=[
            InputSchemaField(name="x1", type="number", required=True),
            InputSchemaField(name="A12", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="raoult_pv",
            description="Raoult's law: P_i = x_i · P_i*.",
            input_schema=[
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="pvap_pure", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
