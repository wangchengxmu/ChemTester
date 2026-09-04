"""
Photochemistry Tools - L3 Implementation
Chapters: Photochemistry (L1 entries 241-245)

## Solver Instructions (for AI Agent)

When you encounter photochemistry problems (quantum yield, excited states, quenching), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given rate constants -> calculate quantum yield or excited state lifetime?
- Given intensity with/without quencher -> calculate Stern-Volmer ratio?
- Given quencher concentrations and intensities -> fit Stern-Volmer constant?
- Given excitation and emission -> calculate Stokes shift or energy?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Quantum yield | `quantum_yield_calc(k_radiative, k_nonradiative, k_other)` | Φ = kᵣ/(kᵣ+kₙᵣ+k_other) |
| Excited state lifetime | `excited_state_lifetime(k_radiative, k_nonradiative, k_other)` | τ = 1/Σk |
| Stern-Volmer ratio | `stern_volmer_quenching(I0, I)` | I0/I = 1 + K_SV[Q] |
| Stern-Volmer fit | `stern_volmer_fit(quencher_concs, intensity_ratios)` | Returns K_SV |
| Energy from wavelength | `energy_from_wavelength(wavelength_nm)` | E = hc/lambda in eV |
| Stokes shift | `stokes_shift(excitation_nm, emission_nm)` | Returns shift in cm-1 |

### Step 3: Handle special cases
- Quantum yield: 0 ≤ Φ ≤ 1; Φ = 1 means all photons produce product
- Lifetime: typically ns (fluorescence) to mus (phosphorescence)
- Stern-Volmer: linear for dynamic quenching; curvature suggests static quenching
- Stokes shift: positive (emission always lower energy than excitation)

### Examples
```python
# Example 1: Quantum yield
quantum_yield_calc(1e8, 1e8)  # kᵣ = kₙᵣ
# -> 0.5 (50% quantum yield)

# Example 2: Excited state lifetime
excited_state_lifetime(1e8, 1e8)  # 1/(1e8+1e8) s
# -> 5e-9 s (5 ns)

# Example 3: Stern-Volmer ratio
stern_volmer_quenching(100, 50)  # I0=100, I=50
# -> 2.0 (I0/I ratio)

# Example 4: Energy from wavelength
energy_from_wavelength(400)  # 400 nm violet light
# -> 3.10 eV
```
"""

from typing import Tuple, Optional
from math import exp, sqrt, pi, log


def quantum_yield_calc(k_radiative: float, k_nonradiative: float = 0,
                       k_other: float = 0) -> float:
    """
    Calculate quantum yield from rate constants.
    
    Φ = k_r / (k_r + k_nr + k_other)
    
    Args:
        k_radiative: Radiative rate constant (s-1)
        k_nonradiative: Non-radiative rate constant (s-1)
        k_other: Additional decay rate constant (s-1)
    
    Returns:
        Quantum yield (0 to 1)
    
    Examples:
        >>> round(quantum_yield_calc(1e8, 1e8), 2)
        0.5
        >>> round(quantum_yield_calc(5e8, 1e7), 2)
        0.98
    """
    total = k_radiative + k_nonradiative + k_other
    if total == 0:
        return 0.0
    return k_radiative / total


def excited_state_lifetime(k_radiative: float, k_nonradiative: float = 0,
                           k_other: float = 0) -> float:
    """
    Calculate excited state lifetime from rate constants.
    
    τ = 1 / (k_r + k_nr + k_other)
    
    Args:
        k_radiative: Radiative rate constant (s-1)
        k_nonradiative: Non-radiative rate constant (s-1)
        k_other: Additional decay rate constant (s-1)
    
    Returns:
        Lifetime in seconds
    
    Examples:
        >>> excited_state_lifetime(1e8, 1e8)
        5e-09
    """
    total = k_radiative + k_nonradiative + k_other
    if total == 0:
        return float('inf')
    return 1.0 / total


def stern_volmer_quenching(I0: float, I: float) -> float:
    """
    Calculate Stern-Volmer ratio from intensity data.
    
    I0/I = 1 + K_SV[Q]
    
    For two points at different [Q], returns K_SV:
        K_SV = ((I0/I1) - (I0/I2)) / ([Q1] - [Q2])
    
    Simple form: returns I0/I ratio.
    
    Args:
        I0: Emission intensity without quencher
        I: Emission intensity with quencher at concentration [Q]
    
    Returns:
        I0/I ratio
    
    Examples:
        >>> stern_volmer_quenching(100, 50)
        2.0
    """
    if I == 0:
        return float('inf')
    return I0 / I


def stern_volmer_fit(quencher_concs: list, intensity_ratios: list) -> dict:
    """
    Fit Stern-Volmer data to get K_SV.
    
    I0/I = 1 + K_SV * [Q]
    
    Args:
        quencher_concs: List of quencher concentrations [Q] (M)
        intensity_ratios: List of I0/I values
    
    Returns:
        dict with 'K_SV' (Stern-Volmer constant) and 'k_q' if tau0 given
    
    Examples:
        >>> stern_volmer_fit([0.01, 0.02, 0.03], [1.5, 2.0, 2.5])
        {'K_SV': 50.0}
    """
    n = len(quencher_concs)
    if n < 2:
        return {}
    
    # Linear regression: y = 1 + K_SV * x
    sum_x = sum(quencher_concs)
    sum_y = sum(intensity_ratios)
    sum_xy = sum(x * y for x, y in zip(quencher_concs, intensity_ratios))
    sum_x2 = sum(x ** 2 for x in quencher_concs)
    
    denom = n * sum_x2 - sum_x ** 2
    if denom == 0:
        return {'K_SV': 0}
    
    slope = (n * sum_xy - sum_x * sum_y) / denom
    return {'K_SV': slope}


def fret_efficiency(r: float, R0: float) -> float:
    """
    Calculate FRET efficiency.
    
    E = 1 / (1 + (r/R0)6)
    
    Args:
        r: Donor-acceptor distance (nm)
        R0: Förster radius at 50% efficiency (nm)
    
    Returns:
        FRET efficiency (0 to 1)
    
    Examples:
        >>> round(fret_efficiency(5.0, 5.0), 2)
        0.5
        >>> round(fret_efficiency(3.5, 5.0), 2)
        0.88
    """
    if R0 == 0:
        return 0.0
    return 1.0 / (1.0 + (r / R0) ** 6)


def fret_distance(efficiency: float, R0: float) -> float:
    """
    Calculate donor-acceptor distance from FRET efficiency.
    
    r = R0 * (1/E - 1)^(1/6)
    
    Args:
        efficiency: FRET efficiency (0 to 1)
        R0: Förster radius (nm)
    
    Returns:
        Distance r (nm)
    
    Examples:
        >>> round(fret_distance(0.5, 5.0), 2)
        5.0
    """
    if efficiency <= 0 or efficiency >= 1:
        return float('inf') if efficiency <= 0 else 0.0
    return R0 * ((1.0 / efficiency) - 1.0) ** (1.0 / 6.0)


def marcus_rate(dG: float, lambda_reorg: float, V: float,
                T: float = 298.15, in_eV: bool = True) -> float:
    """
    Calculate electron transfer rate using Marcus theory.
    
    k_ET = (2pi/ℏ)|V|2 x (1/√(4pilambdak_BT)) x exp(-(DeltaG+lambda)2/(4lambdak_BT))
    
    Args:
        dG: Gibbs free energy change (eV or J)
        lambda_reorg: Reorganization energy (eV or J)
        V: Electronic coupling (eV or J)
        T: Temperature (K)
        in_eV: If True, inputs are in eV (default); if False, in J
    
    Returns:
        Rate constant k_ET (s-1)
    
    Examples:
        >>> k = marcus_rate(-0.5, 1.0, 0.01)
        >>> k > 0
        True
    """
    kB = 1.380649e-23  # J/K
    hbar = 1.054571817e-34  # J·s
    
    if in_eV:
        eV_to_J = 1.602176634e-19
        dG *= eV_to_J
        lambda_reorg *= eV_to_J
        V *= eV_to_J
    
    kBT = kB * T
    
    prefactor = (2 * pi / hbar) * V ** 2
    boltz = (1.0 / sqrt(4 * pi * lambda_reorg * kBT))
    activation = exp(-((dG + lambda_reorg) ** 2) / (4 * lambda_reorg * kBT))
    
    return prefactor * boltz * activation


def stokes_shift(wavelength_abs: float, wavelength_em: float) -> dict:
    """
    Calculate Stokes shift in nm and cm-1.
    
    Args:
        wavelength_abs: Absorption maximum (nm)
        wavelength_em: Emission maximum (nm)
    
    Returns:
        dict with 'shift_nm', 'shift_cm_inv'
    
    Examples:
        >>> stokes_shift(350, 450)
        {'shift_nm': 100, 'shift_cm_inv': 6349}
    """
    shift_nm = wavelength_em - wavelength_abs
    if wavelength_abs == 0 or wavelength_em == 0:
        return {'shift_nm': shift_nm, 'shift_cm_inv': 0}
    nu_abs = 1e7 / wavelength_abs
    nu_em = 1e7 / wavelength_em
    return {'shift_nm': shift_nm, 'shift_cm_inv': round(nu_abs - nu_em)}


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="excited_state_lifetime",
            description="Calculate excited state lifetime from rate constants.",
            input_schema=[
            InputSchemaField(name="k_radiative", type="number", required=True),
            InputSchemaField(name="k_nonradiative", type="number", required=False),
            InputSchemaField(name="k_other", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fret_distance",
            description="Calculate donor-acceptor distance from FRET efficiency.",
            input_schema=[
            InputSchemaField(name="efficiency", type="number", required=True),
            InputSchemaField(name="R0", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fret_efficiency",
            description="Calculate FRET efficiency.",
            input_schema=[
            InputSchemaField(name="r", type="number", required=True),
            InputSchemaField(name="R0", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="marcus_rate",
            description="Calculate electron transfer rate using Marcus theory.",
            input_schema=[
            InputSchemaField(name="dG", type="number", required=True),
            InputSchemaField(name="lambda_reorg", type="number", required=True),
            InputSchemaField(name="V", type="number", required=True),
            InputSchemaField(name="T", type="number", required=False),
            InputSchemaField(name="in_eV", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="quantum_yield_calc",
            description="Calculate quantum yield from rate constants.",
            input_schema=[
            InputSchemaField(name="k_radiative", type="number", required=True),
            InputSchemaField(name="k_nonradiative", type="number", required=False),
            InputSchemaField(name="k_other", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="stern_volmer_fit",
            description="Fit Stern-Volmer data to get K_SV.",
            input_schema=[
            InputSchemaField(name="quencher_concs", type="number", required=True),
            InputSchemaField(name="intensity_ratios", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="stern_volmer_quenching",
            description="Calculate Stern-Volmer ratio from intensity data.",
            input_schema=[
            InputSchemaField(name="I0", type="number", required=True),
            InputSchemaField(name="I", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="stokes_shift",
            description="Calculate Stokes shift in nm and cm-1.",
            input_schema=[
            InputSchemaField(name="wavelength_abs", type="number", required=True),
            InputSchemaField(name="wavelength_em", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
