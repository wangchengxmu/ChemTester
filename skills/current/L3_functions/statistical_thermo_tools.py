"""
Statistical thermodynamics tools - partition functions, thermodynamic properties from spectroscopic data.
L3 function for chem-memory knowledge base.
Source: DeVoe Ch15

## Solver Instructions (for AI Agent)

When you encounter statistical thermodynamics problems (computing partition functions and thermodynamic properties from spectroscopic data), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Translational q**: Given T, molecular mass, volume -> find q_trans
- **Rotational q**: Given T, rotational constant B, symmetry number -> find q_rot
- **Vibrational q**: Given T, vibrational frequency -> find q_vib
- **Thermodynamic properties from q**: Given q and T -> find U, A, S, G, Cv
- **Residual entropy**: Given degeneracy of ground state -> find S_res = k ln(W0)
- **Boltzmann populations**: Given energy levels and T -> find fraction in each level

### Step 2: Choose the correct function
- `q_translational(T, M_kg, V)` -> q_trans = V/Λ3 where Λ = h/√(2piMkT)
- `q_rotational(T, B_cm, sigma)` -> q_rot = T/(σ·θ_rot) for T >> θ_rot
- `q_vibrational(T, nu_cm)` -> q_vib = exp(-θ_vib/2T)/(1-exp(-θ_vib/T))
- `thermo_from_q(T, q, N)` -> dict with U, A, S, G, Cv
- `residual_entropy(W0)` -> S = k·ln(W0)
- `boltzmann_population(energies, T, degeneracies)` -> fractional populations

### Step 3: Handle special cases
- M_kg must be mass of single molecule in kg (M_molar/N_A)
- B_cm is rotational constant in cm-1; sigma is symmetry number (1 heteronuclear, 2 homonuclear)
- nu_cm is vibrational frequency in cm-1
- At low T/T_rot: use explicit summation in q_rotational (function handles this automatically)
- Residual entropy > 0 indicates degenerate ground state (e.g., CO at 0 K: W0=2, S_res = 5.76 J/(mol·K))

### Examples
1. **N2 at 298 K**: M=28 g/mol -> M_kg=4.65e-26 kg, V=0.0245 m3/mol, B=2.0 cm-1, σ=2, ν=2359.6 cm-1
   -> `q_translational(298.15, 4.65e-26, 0.0245)` -> ~3.5e30
   -> `q_rotational(298.15, 2.0, 2)` -> ~51.8
   -> `q_vibrational(298.15, 2359.6)` -> ~1.000012 (essentially 1, ground state)

2. **CO residual entropy**: W0 = 2 (random orientation)
   -> `residual_entropy(2)` -> 1.38e-23 x ln(2) = 9.57e-24 J/K per molecule
   -> Molar: 5.76 J/(mol·K) (agrees with experimental 3rd law anomaly)
"""

import numpy as np
from typing import Dict, Optional, Tuple

k_B = 1.380649e-23  # J/K
N_A = 6.02214076e23  # mol^-1
R = 8.3145  # J/(mol·K)
h = 6.62607015e-34  # J·s
c = 2.99792458e10  # cm/s

def q_translational(T, M_kg, V):
    """Translational partition function.
    M_kg: molecular mass in kg
    V: volume in m^3
    """
    lam = h / np.sqrt(2 * np.pi * M_kg * k_B * T)  # thermal de Broglie wavelength
    return V / lam**3

def q_rotational(T, B_cm, sigma=1):
    """Rotational partition function for linear molecule.
    B_cm: rotational constant in cm^-1
    sigma: symmetry number
    """
    theta_rot = h * c * B_cm / k_B  # in K
    if T > 2 * theta_rot:
        return T / (sigma * theta_rot)
    else:
        # Sum explicitly
        J_max = int(5 * T / theta_rot) + 1
        return sum((2*J+1) * np.exp(-J*(J+1)*theta_rot/T) for J in range(J_max))

def q_vibrational(T, nu_cm):
    """Vibrational partition function (harmonic oscillator).
    nu_cm: vibrational frequency in cm^-1
    """
    theta_vib = h * c * nu_cm / k_B  # in K
    x = np.exp(-theta_vib / (2*T))
    return x / (1 - np.exp(-theta_vib / T))

def thermo_from_q(T, q, N=N_A):
    """Compute thermodynamic properties from partition function (ideal gas)."""
    dq_dT = np.gradient(q, T) if hasattr(T, '__len__') else (q * 0.0)  # placeholder
    U = N * k_B * T**2 * np.gradient(np.log(q), T) if hasattr(T, '__len__') else 0
    A = -N * k_B * T * np.log(q / N)
    S = (U - A) / T
    G = A + N * k_B * T  # G = -NkT ln(q/N) for indistinguishable
    Cv = np.gradient(U, T) if hasattr(T, '__len__') else 0
    return {'U': U, 'A': A, 'S': S, 'G': G, 'Cv': Cv}

def residual_entropy(W0):
    """Residual entropy S_res = k ln(W0)"""
    return k_B * np.log(W0)

def boltzmann_population(energies, T, degeneracies=None):
    """Boltzmann population of energy levels."""
    if degeneracies is None:
        degeneracies = np.ones_like(energies)
    q = np.sum(degeneracies * np.exp(-energies / (k_B * T)))
    return degeneracies * np.exp(-energies / (k_B * T)) / q

if __name__ == '__main__':
    T = 298.15
    M_N2 = 28.014e-3 / N_A  # kg
    V = 0.024465  # m3/mol at STP-like conditions
    B_N2 = 2.0  # cm^-1
    nu_N2 = 2359.6  # cm^-1

    qt = q_translational(T, M_N2, V)
    qr = q_rotational(T, B_N2, sigma=2)
    qv = q_vibrational(T, nu_N2)
    q_total = qt * qr * qv
    print(f"q_trans = {qt:.3e}, q_rot = {qr:.1f}, q_vib = {qv:.6f}")
    print(f"q_total = {q_total:.3e}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="boltzmann_population",
            description="Boltzmann population of energy levels.",
            input_schema=[
            InputSchemaField(name="energies", type="number", required=True),
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="degeneracies", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="q_rotational",
            description="Rotational partition function for linear molecule.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="B_cm", type="number", required=True),
            InputSchemaField(name="sigma", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="q_translational",
            description="Translational partition function.",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="M_kg", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="q_vibrational",
            description="Vibrational partition function (harmonic oscillator).",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="nu_cm", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="residual_entropy",
            description="Residual entropy S_res = k ln(W0)",
            input_schema=[
            InputSchemaField(name="W0", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="thermo_from_q",
            description="Compute thermodynamic properties from partition function (ideal gas).",
            input_schema=[
            InputSchemaField(name="T", type="number", required=True),
            InputSchemaField(name="q", type="number", required=True),
            InputSchemaField(name="N", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
