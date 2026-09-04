"""
Thermodynamic potentials tools - Legendre transforms, Maxwell relations, spontaneity checks.
L3 function for chem-memory knowledge base.
Source: DeVoe Ch5
"""

## Solver Instructions (for AI Agent)

# When you encounter **advanced thermodynamic potentials and relationships** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Legendre transform between potentials: `legendre_transform(U, S, T, V, p)`
# - Maxwell relations with numerical partials: `maxwell_relations(T, V, p, ...)`
# - Gibbs-Helmholtz equation: `gibbs_helmholtz(T, G, H)`
# - Spontaneity from multiple criteria: `spontaneity_criteria(T, p, dU, dH, dA, dG)`
# - Cp - Cv relation: `Cp_minus_Cv(T, V, alpha, kappa_T)`
# - Gibbs-Duhem consistency: `gibbs_duhem_check(x, dmu)`

### Step 2: Choose the correct function
# - Converting between thermodynamic potentials: `legendre_transform`
# - Verifying Maxwell relations numerically: `maxwell_relations`
# - Gibbs-Helmholtz (G/T vs 1/T): `gibbs_helmholtz`
# - Comprehensive spontaneity check: `spontaneity_criteria`

### Step 3: Handle special cases
# - `maxwell_relations` can accept partial derivatives or compute from equations of state
# - `spontaneity_criteria` checks all applicable criteria for given T, p conditions

### Examples
# 1. Legendre: U=100, S=0.3, T=300, V=0.01, p=1e5: `legendre_transform(100, 0.3, 300, 0.01, 1e5)`
# 2. Cp-Cv for ideal gas (alpha=1/T, κT=1/p): `Cp_minus_Cv(300, 0.0245, 1/300, 1/101325)` -> ~8.314 J/(mol·K)
# 3. Gibbs-Helmholtz: `gibbs_helmholtz(298, -237.13e3, -285.83e3)`



import numpy as np
from typing import Dict, Optional, Tuple

R = 8.3145  # J/(mol·K)

def legendre_transform(U, S, T, V, p):
    """Compute all four thermodynamic potentials."""
    H = U + p * V
    A = U - T * S
    G = H - T * S
    return {'U': U, 'H': H, 'A': A, 'G': G}

def maxwell_relations(T, V, p, dT_dV=None, dp_dS=None, dS_dV=None, dp_dT=None):
    """Check Maxwell relations. Returns dict of left vs right sides for verification."""
    relations = {}
    if dT_dV is not None and dp_dS is not None:
        relations['dU'] = {'left': dT_dV, 'right': -dp_dS}
    if dS_dV is not None and dp_dT is not None:
        relations['dA'] = {'left': dS_dV, 'right': dp_dT}
    return relations

def gibbs_helmholtz(T, G, H=None):
    """Gibbs-Helmholtz equation: d(G/T)/dT = -H/T^2"""
    return -H / T**2 if H is not None else None

def spontaneity_criteria(T, p, dU=None, dH=None, dA=None, dG=None):
    """Check spontaneity based on available potential changes."""
    results = {}
    if dG is not None:
        results['const_T_p'] = 'spontaneous' if dG < 0 else ('equilibrium' if dG == 0 else 'nonspontaneous')
    if dA is not None:
        results['const_T_V'] = 'spontaneous' if dA < 0 else ('equilibrium' if dA == 0 else 'nonspontaneous')
    if dH is not None:
        results['const_S_p'] = 'spontaneous' if dH < 0 else ('equilibrium' if dH == 0 else 'nonspontaneous')
    if dU is not None:
        results['const_S_V'] = 'spontaneous' if dU < 0 else ('equilibrium' if dU == 0 else 'nonspontaneous')
    return results

def Cp_minus_Cv(T, V, alpha, kappa_T):
    """C_p - C_V = TV*alpha^2 / kappa_T"""
    return T * V * alpha**2 / kappa_T

def gibbs_duhem_check(x, dmu, tol=1e-10):
    """Check Gibbs-Duhem: sum(x_i * dmu_i) = 0 at const T, p."""
    total = sum(xi * dmi for xi, dmi in zip(x, dmu))
    return abs(total) < tol

if __name__ == '__main__':
    # Quick test
    U, S, T, V, p = 1000, 50, 300, 0.01, 101325
    pots = legendre_transform(U, S, T, V, p)
    print(f"U={U}, H={pots['H']:.1f}, A={pots['A']:.1f}, G={pots['G']:.1f}")
    print(f"Cp-Cv: {Cp_minus_Cv(300, 0.01, 2.1e-4, 4.5e-10):.2f} J/(mol·K)")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="Cp_minus_Cv",
            description="C_p - C_V = TV*alpha^2 / kappa_T",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="alpha", type="number", required=True),
            InputSchemaField(name="kappa_T", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_duhem_check",
            description="Check Gibbs-Duhem: sum(x_i * dmu_i) = 0 at const T, p.",
            input_schema=[
            InputSchemaField(name="x", type="number", required=True),
            InputSchemaField(name="dmu", type="number", required=True),
            InputSchemaField(name="tol", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gibbs_helmholtz",
            description="Gibbs-Helmholtz equation: d(G/T)/dT = -H/T^2",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="G", type="number", required=True),
            InputSchemaField(name="H", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="legendre_transform",
            description="Compute all four thermodynamic potentials.",
            input_schema=[
            InputSchemaField(name="U", type="number", required=True),
            InputSchemaField(name="S", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="p", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="maxwell_relations",
            description="Check Maxwell relations. Returns dict of left vs right sides for verification.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="p", type="number", required=True),
            InputSchemaField(name="dT_dV", type="number", required=False),
            InputSchemaField(name="dp_dS", type="number", required=False),
            InputSchemaField(name="dS_dV", type="number", required=False),
            InputSchemaField(name="dp_dT", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spontaneity_criteria",
            description="Check spontaneity based on available potential changes.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="p", type="number", required=True),
            InputSchemaField(name="dU", type="number", required=False),
            InputSchemaField(name="dH", type="number", required=False),
            InputSchemaField(name="dA", type="number", required=False),
            InputSchemaField(name="dG", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
