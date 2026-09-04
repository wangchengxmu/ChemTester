"""
Mixture and partial molar quantities tools.
L3 function for chem-memory knowledge base.
Source: DeVoe Ch9-10

## Solver Instructions (for AI Agent)

When you encounter mixture, partial molar, or solution thermodynamics problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given molar property vs composition -> calculate partial molar quantities?
- Given mole fractions -> calculate mixing properties (DeltaG, DeltaH, DeltaS)?
- Given ionic strength -> calculate activity coefficient (Debye-Hückel)?
- Given concentration -> calculate osmotic pressure?
- Given vapor pressures -> apply Clausius-Clapeyron or Raoult's law?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Partial molar (binary) | `partial_molar_binary(X_molar, x_B)` | Intercept method for V_A, V_B |
| Mixing properties | `mixing_properties(n_total, x, dH_mix, dS_mix)` | Ideal: dS_mix = -nRΣxᵢln(xᵢ) |
| Fugacity coefficient | `fugacity_coefficient_virial(B_prime, p, T)` | ln(φ) = B'P/(RT) |
| Activity (Raoult) | `activity_raoult(x_i, gamma_i)` | aᵢ = gammaᵢ x xᵢ |
| Clausius-Clapeyron | `clausius_clapeyron(T1, T2, dH_vap, p1, p2)` | Solve for unknown P or T |
| Debye-Hückel | `debye_huckel_limiting(I, z_plus, z_minus, A)` | Mean ionic activity coefficient |
| Osmotic pressure | `osmotic_pressure(c, T)` | Π = cRT (van't Hoff) |

### Step 3: Handle special cases
- Debye-Hückel limiting law valid for I < 0.01 M
- A ~ 1.171 (kg/mol)^0.5 at 298 K for water
- Osmotic pressure: c in mol/m3, T in K, R = 8.314 J/(mol·K)

### Examples
```python
# Example 1: Partial molar volumes
import numpy as np
xB = np.array([0.0, 0.5, 1.0])
Vm = np.array([18e-6, 25e-6, 40e-6])  # m3/mol
partial_molar_binary(Vm, xB)
# -> (V_A, V_B) at last composition point

# Example 2: Ideal mixing entropy
mixing_properties(1.0, np.array([0.5, 0.5]))
# -> {'dG_mix': ..., 'dH_mix': 0, 'dS_mix': ...}

# Example 3: Osmotic pressure
osmotic_pressure(100, 298)  # c=100 mol/m3, T=298K
# -> Π ~ 248,000 Pa
```
"""

import numpy as np
from typing import List, Optional, Dict, Tuple

R = 8.3145  # J/(mol·K)

def partial_molar_binary(X_molar, x_B):
    """Intercept method: compute partial molar quantities X_A and X_B
    from molar property X as function of x_B.
    X_molar: array of molar property values at different x_B
    x_B: array of mole fractions of B (same length as X_molar)
    Returns (X_A, X_B) at the last composition point.
    """
    dx = np.gradient(x_B)
    dX_dx = np.gradient(X_molar, x_B)
    xB = x_B[-1]
    XB = X_molar[-1] - (1 - xB) * dX_dx[-1]
    XA = X_molar[-1] + xB * dX_dx[-1]
    return XA, XB

def mixing_properties(n_total, x, dH_mix=0, dS_mix=None):
    """Compute ideal mixing properties.
    n_total: total moles
    x: array of mole fractions
    dH_mix: enthalpy of mixing (0 for ideal)
    """
    if dS_mix is None:
        dS_mix = -n_total * R * np.sum(x * np.log(x + 1e-30))
    dG_mix = dH_mix - 298.15 * dS_mix  # default T=298.15K
    return {'dG_mix': dG_mix, 'dH_mix': dH_mix, 'dS_mix': dS_mix}

def fugacity_coefficient_virial(B_prime, p, T):
    """Fugacity coefficient from virial EOS: ln(phi) = B'*p/(RT)"""
    return np.exp(B_prime * p / (R * T))

def activity_raoult(x_i, gamma_i):
    """Activity using Raoult's law convention."""
    return gamma_i * x_i

def clausius_clapeyron(T1, T2, dH_vap, p1=None, p2=None):
    """Clausius-Clapeyron equation."""
    if p1 is not None and p2 is None:
        p2 = p1 * np.exp(-dH_vap / R * (1/T2 - 1/T1))
        return p2
    elif p2 is not None and p1 is None:
        p1 = p2 / np.exp(-dH_vap / R * (1/T2 - 1/T1))
        return p1
    elif p1 is not None and p2 is not None:
        dH_vap = -R * np.log(p2/p1) / (1/T2 - 1/T1)
        return dH_vap

def debye_huckel_limiting(I, z_plus, z_minus, A=1.171):
    """Mean ionic activity coefficient (limiting law)."""
    return np.exp(-A * abs(z_plus * z_minus) * np.sqrt(I))

def osmotic_pressure(c, T):
    """van't Hoff equation: Pi = cRT"""
    return c * R * T

if __name__ == '__main__':
    # Test binary partial molar volumes
    xB = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    Vm = np.array([18.07, 19.8, 21.5, 23.0, 24.3, 25.4, 26.3, 27.1, 27.8, 28.5, 40.75]) * 1e-6  # m3/mol
    XA, XB_val = partial_molar_binary(Vm, xB)
    print(f"Partial molar V_A = {XA*1e6:.2f} cm3/mol, V_B = {XB_val*1e6:.2f} cm3/mol")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="activity_raoult",
            description="Activity using Raoult's law convention.",
            input_schema=[
            InputSchemaField(name="x_i", type="number", required=True),
            InputSchemaField(name="gamma_i", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="clausius_clapeyron",
            description="Clausius-Clapeyron equation.",
            input_schema=[
            InputSchemaField(name="T1", type="number", required=True),
            InputSchemaField(name="T2", type="number", required=True),
            InputSchemaField(name="dH_vap", type="number", required=True),
            InputSchemaField(name="p1", type="number", required=False),
            InputSchemaField(name="p2", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="debye_huckel_limiting",
            description="Mean ionic activity coefficient (limiting law).",
            input_schema=[
            InputSchemaField(name="I", type="number", required=True),
            InputSchemaField(name="z_plus", type="number", required=True),
            InputSchemaField(name="z_minus", type="number", required=True),
            InputSchemaField(name="A", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fugacity_coefficient_virial",
            description="Fugacity coefficient from virial EOS: ln(phi) = B'*p/(RT)",
            input_schema=[
            InputSchemaField(name="B_prime", type="number", required=True),
            InputSchemaField(name="p", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mixing_properties",
            description="Compute ideal mixing properties.",
            input_schema=[
            InputSchemaField(name="n_total", type="number", required=True),
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="dH_mix", type="number", required=False),
            InputSchemaField(name="dS_mix", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="osmotic_pressure",
            description="van't Hoff equation: Pi = cRT",
            input_schema=[
            InputSchemaField(name="c", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="partial_molar_binary",
            description="Intercept method: compute partial molar quantities X_A and X_B",
            input_schema=[
            InputSchemaField(name="X_molar", type="number", required=True),
            InputSchemaField(name="x_B", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
