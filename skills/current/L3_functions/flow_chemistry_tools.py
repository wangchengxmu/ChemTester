"""Flow Chemistry Tools - Reactor and flow system calculations.
## Solver Instructions (for AI Agent)

When you encounter flow chemistry or continuous reactor problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given reactor volume and flow rate -> Residence time? Use `residence_time(volume_ml, flow_rate_ml_min)`
- Given product, volume, time -> Space-time yield? Use `space_time_yield(product_g, volume_ml, time_h)`
- Given D, v, ρ, mu -> Reynolds number? Use `reynolds_number(D, v, rho, mu)`

### Step 2: Handle special cases
- **Residence time**: τ = V/F; longer τ = more reaction time
- **Reynolds number**: Re < 2100 laminar, 2100-4000 transitional, > 4000 turbulent
- **Space-time yield**: Productivity metric in g/(mL·h)

### Examples
```python
# Example 1: Residence time
residence_time(10, 0.5)  # -> 20 min

# Example 2: Reynolds number (check flow regime)
reynolds_number(0.001, 0.01, 1000, 0.001)  # -> 10 (laminar)

# Example 3: Space-time yield
space_time_yield(50, 10, 24)  # -> 0.208 g/(mL·h)
```
"""
import math

def residence_time(volume_ml: float, flow_rate_ml_min: float) -> float:
    """Residence time in minutes: τ = V / F."""
    if flow_rate_ml_min == 0:
        raise ValueError("Flow rate cannot be zero")
    return volume_ml / flow_rate_ml_min

def space_time_yield(product_g: float, volume_ml: float, time_h: float) -> float:
    """Space-time yield: g/(mL·h)."""
    if time_h == 0 or volume_ml == 0:
        raise ValueError("Volume and time must be non-zero")
    return product_g / (volume_ml * time_h)

def reynolds_number(D: float, v: float, rho: float, mu: float) -> float:
    """Reynolds number: Re = ρvD/mu."""
    return rho * v * D / mu


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "residence_time",
        "description": "Residence time in minutes: \u03c4 = V / F.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "volume_ml": {"type": "number", "description": "Volume Ml"},
                "flow_rate_ml_min": {"type": "number", "description": "Flow Rate Ml Min"},
            },
            "required": ["volume_ml", "flow_rate_ml_min"]
        }
    },
    {
        "name": "reynolds_number",
        "description": "Reynolds number: Re = \u03c1vD/\u03bc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "D": {"type": "number", "description": "D"},
                "v": {"type": "number", "description": "V"},
                "rho": {"type": "number", "description": "Rho"},
                "mu": {"type": "number", "description": "Mu"},
            },
            "required": ["D", "v", "rho", "mu"]
        }
    },
    {
        "name": "space_time_yield",
        "description": "Space-time yield: g/(mL\u00b7h).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_g": {"type": "number", "description": "Product G"},
                "volume_ml": {"type": "number", "description": "Volume Ml"},
                "time_h": {"type": "number", "description": "Time H"},
            },
            "required": ["product_g", "volume_ml", "time_h"]
        }
    }
]
