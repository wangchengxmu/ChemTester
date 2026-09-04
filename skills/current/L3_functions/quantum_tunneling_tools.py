"""
Quantum Tunneling Tools (L3)
============================
Computational tools for quantum mechanical tunneling calculations.

Functions:
    - rectangular_barrier_T: Transmission coefficient for rectangular barrier
    - triangular_barrier_T: WKB transmission coefficient for triangular barrier
    - wkb_transmission: General WKB transmission coefficient
    - bell_tunneling_correction: Bell tunneling correction factor Q_tun
    - gamow_factor: Gamow factor for alpha decay

__all__ = [
    "rectangular_barrier_T",
    "triangular_barrier_T",
    "wkb_transmission",
    "bell_tunneling_correction",
    "gamow_factor",
]

## Solver Instructions (for AI Agent)

When you encounter quantum tunneling problems (transmission through barriers, alpha decay, tunneling correction to reaction rates), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Rectangular barrier**: Given particle energy, barrier height/width, mass -> find transmission coefficient T
- **Triangular barrier (WKB)**: Given energy, barrier height, barrier width at E, mass -> find T
- **General WKB**: Given barrier shape V(x), energy, mass -> find T via integral
- **Bell tunneling correction**: Given barrier height, frequency, mass, T -> find Q_tun to multiply rate constant
- **Alpha decay/Gamow factor**: Given alpha energy, nuclear charge, barrier height -> find decay rate/probability

### Step 2: Choose the correct function
- `rectangular_barrier_T(energy_eV, barrier_height_eV, width_angstrom, mass_amu)` -> T ~ (16E(V0-E)/V02)xexp(-2κa)
- `triangular_barrier_T(energy_eV, barrier_height_eV, width_at_energy_angstrom, mass_amu)` -> WKB approximation
- `wkb_transmission(energy_eV, barrier_func, x1, x2, mass_amu)` -> T = exp(-2∫κ(x)dx)
- `bell_tunneling_correction(barrier_height_eV, frequency_cm1, mass_amu, temperature_K)` -> Q_tun
- `gamow_factor(energy_eV, z1, z2, reduced_mass_amu)` -> G = 2piη/(exp(2piη)-1)

### Step 3: Handle special cases
- If energy ≥ barrier height: classical transmission (T~1 for rectangular)
- WKB valid when barrier is thick/low-transmission (κa >> 1)
- Bell correction: important for light atoms (H, D) at low temperatures; Q_tun = k_actual/k_classical
- Gamow factor: low G -> high tunneling probability -> faster decay

### Examples
1. **Rectangular barrier**: Electron (1 amu) with 1 eV energy, 2 eV barrier, 1 Å width
   -> `rectangular_barrier_T(1.0, 2.0, 1.0, 1.0)` -> T ~ very small (~10-2 range)
   -> Increasing width to 2 Å -> T drops exponentially

2. **Alpha decay 238U**: Ealpha = 4.27 MeV, Z_daughter=90, m_alpha=4 amu
   -> `gamow_factor(4.27e6, 2, 90, 4.0)` -> small Gamow factor -> very slow decay (t½ = 4.5 billion years)

3. **Bell tunneling**: H transfer, V_barrier=0.5 eV, ν=3000 cm-1, m=1 amu, T=300 K
   -> `bell_tunneling_correction(0.5, 3000, 1.0, 300)` -> Q_tun > 1 (rate enhanced by tunneling)
"""

import math
from typing import Callable, Optional

# Physical constants
HBAR = 1.054571817e-34  # J·s
HBAR_EV = 6.582119569e-16  # eV·s
E_CHARGE = 1.602176634e-19  # C
AMU = 1.66053906660e-27  # kg
K_B = 1.380649e-23  # J/K
K_B_EV = 8.617333262e-5  # eV/K


def rectangular_barrier_T(
    energy_eV: float,
    barrier_height_eV: float,
    width_angstrom: float,
    mass_amu: float = 1.0,
) -> float:
    """
    Transmission coefficient for a rectangular potential barrier.

    Uses the approximation T ~ (16E(V0-E)/V02) x exp(-2κa),
    valid when κa >> 1 (thick barrier / low transmission limit).

    Parameters
    ----------
    energy_eV : float
        Particle kinetic energy in eV.
    barrier_height_eV : float
        Barrier height V0 in eV (must be > energy_eV).
    width_angstrom : float
        Barrier width in Angstroms.
    mass_amu : float
        Particle mass in atomic mass units.

    Returns
    -------
    float
        Transmission coefficient (0 < T < 1).

    Raises
    ------
    ValueError
        If energy >= barrier height or negative inputs.
    """
    if energy_eV <= 0 or barrier_height_eV <= 0 or width_angstrom <= 0 or mass_amu <= 0:
        raise ValueError("All inputs must be positive.")
    if energy_eV >= barrier_height_eV:
        return 1.0  # classically allowed; exact treatment needed for E ~ V0

    dV = barrier_height_eV - energy_eV  # eV
    m = mass_amu * AMU  # kg
    kappa = math.sqrt(2.0 * m * dV * E_CHARGE) / HBAR  # m-1
    a = width_angstrom * 1e-10  # m

    prefactor = 16.0 * energy_eV * dV / (barrier_height_eV ** 2)
    T = prefactor * math.exp(-2.0 * kappa * a)
    return min(T, 1.0)


def triangular_barrier_T(
    energy_eV: float,
    barrier_height_eV: float,
    width_angstrom: float,
    mass_amu: float = 1.0,
) -> float:
    """
    WKB transmission coefficient for a triangular (linearly sloped) barrier.

    For a linear barrier V(x) = V0(1 - x/a), the WKB integral gives:
    T ~ exp(-4√(2m) a √(V0-E) / (3ℏ))

    Parameters
    ----------
    energy_eV : float
        Particle kinetic energy in eV.
    barrier_height_eV : float
        Peak barrier height in eV.
    width_angstrom : float
        Barrier width in Angstroms.
    mass_amu : float
        Particle mass in amu.

    Returns
    -------
    float
        Transmission coefficient.
    """
    if energy_eV <= 0 or barrier_height_eV <= 0 or width_angstrom <= 0:
        raise ValueError("All inputs must be positive.")
    if energy_eV >= barrier_height_eV:
        return 1.0

    dV = barrier_height_eV - energy_eV  # eV
    m = mass_amu * AMU
    a = width_angstrom * 1e-10
    exponent = (4.0 * a * math.sqrt(2.0 * m * dV * E_CHARGE)) / (3.0 * HBAR)
    return math.exp(-exponent)


def wkb_transmission(
    energy_eV: float,
    V_func: Callable[[float], float],
    x1: float,
    x2: float,
    mass_amu: float,
    n_points: int = 1000,
) -> float:
    """
    General WKB transmission coefficient via numerical integration.

    T ~ exp(-2/ℏ ∫_{x1}^{x2} √(2m[V(x)-E]) dx)

    Uses the trapezoidal rule for the integral.

    Parameters
    ----------
    energy_eV : float
        Particle energy in eV.
    V_func : callable
        Potential function V(x) returning eV, where x is in Angstroms.
    x1, x2 : float
        Classical turning points in Angstroms (x1 < x2).
    mass_amu : float
        Particle mass in amu.
    n_points : int
        Number of integration points.

    Returns
    -------
    float
        Transmission coefficient.
    """
    m = mass_amu * AMU
    dx = (x2 - x1) / n_points
    integral = 0.0
    for i in range(n_points + 1):
        x_A = x1 + i * dx  # Angstroms
        x_m = x_A * 1e-10   # meters
        V_eV = V_func(x_A)
        dV = V_eV - energy_eV
        if dV > 0:
            integrand = math.sqrt(2.0 * m * dV * E_CHARGE) * dx * 1e-10
            if i == 0 or i == n_points:
                integrand *= 0.5
            integral += integrand
    return math.exp(-2.0 * integral / HBAR)


def bell_tunneling_correction(
    barrier_height_eV: float = None,
    temperature_K: float = None,
    reduced_mass_amu: float = None,
    imaginary_frequency_cm1: Optional[float] = None,
    barrier_width_angstrom: Optional[float] = None,
    # Aliases for backward compatibility with different callers
    barrier_height_J: float = None,
    mass_kg: float = None,
    width_m: float = None,
    imaginary_freq_cm_inv: float = None,
) -> float:
    """
    Bell tunneling correction factor Q_tun for TST reaction rates.

    k_tunneling = k_TST x Q_tun

    If imaginary frequency is given, uses the Wigner correction:
        Q_Wigner = 1 + (ℏω‡ / k_B T)2 / 24

    If barrier width is given, uses the Bell (parabolic) correction:
        Q_Bell = (betaℏω‡/2) / sin(betaℏω‡/2)
    where beta = 1/(k_B T) and ω‡ is estimated from the parabolic barrier fit.

    Parameters
    ----------
    barrier_height_eV : float, optional
        Classical barrier height in eV.
    temperature_K : float
        Temperature in Kelvin.
    reduced_mass_amu : float, optional
        Reduced mass of tunneling particle in amu.
    imaginary_frequency_cm1 : float, optional
        Imaginary frequency at the barrier top in cm-1.
    barrier_width_angstrom : float, optional
        Barrier width in Angstroms (for parabolic fit).
    barrier_height_J : float, optional
        Barrier height in Joules (alternative to eV).
    mass_kg : float, optional
        Mass in kg (alternative to amu).
    width_m : float, optional
        Width in meters (alternative to angstrom).
    imaginary_freq_cm_inv : float, optional
        Alias for imaginary_frequency_cm1.

    Returns
    -------
    float
        Tunneling correction factor Q_tun (≥ 1).
    """
    # Handle parameter aliases
    if imaginary_frequency_cm1 is None and imaginary_freq_cm_inv is not None:
        imaginary_frequency_cm1 = imaginary_freq_cm_inv
    
    if barrier_height_eV is None and barrier_height_J is not None:
        barrier_height_eV = barrier_height_J / E_CHARGE
    
    if reduced_mass_amu is None and mass_kg is not None:
        reduced_mass_amu = mass_kg / AMU
    
    if barrier_width_angstrom is None and width_m is not None:
        barrier_width_angstrom = width_m * 1e10
    
    if temperature_K is None:
        return {"error": "temperature_K is required"}
    
    beta = 1.0 / (K_B * temperature_K)  # J-1

    if imaginary_frequency_cm1 is not None:
        # Wigner correction
        omega = 2.0 * math.pi * 3e10 * imaginary_frequency_cm1  # s-1 (rad/s)
        hw_beta = HBAR * omega * beta
        Q = 1.0 + hw_beta ** 2 / 24.0
        return Q

    if barrier_width_angstrom is not None and reduced_mass_amu is not None:
        # Parabolic barrier: ω‡ ~ pi√(2V0/m) / a
        if barrier_height_eV is None:
            raise ValueError("barrier_height_eV (or barrier_height_J) required when using width")
        V0_J = barrier_height_eV * E_CHARGE
        m = reduced_mass_amu * AMU
        a = barrier_width_angstrom * 1e-10
        omega = math.pi * math.sqrt(2.0 * V0_J / m) / a
        hw_beta = HBAR * omega * beta
        if hw_beta >= math.pi:
            return float("inf")  # complete tunneling regime
        Q = (hw_beta / 2.0) / math.sin(hw_beta / 2.0)
        return Q

    raise ValueError("Provide either imaginary_frequency_cm1 or (barrier_width_angstrom + reduced_mass_amu + barrier_height_eV).")


def gamow_factor(
    energy_MeV: float,
    Z_daughter: int,
    Z_alpha: int = 2,
) -> float:
    """
    Gamow factor for alpha decay through the Coulomb barrier.

    G = 2η [arccos(√(R/B)) - √(R/B · (1 - R/B))]

    where η = Z_d Z_alpha e2/(4piε0 ℏv) is the Sommerfeld parameter,
    B = Z_d Z_alpha e2/(4piε0 R) is the Coulomb barrier height,
    and R ~ 1.2 (A_d^(1/3) + 4^(1/3)) fm.

    Transmission T ~ exp(-2G), and half-life ∝ exp(2G).

    Parameters
    ----------
    energy_MeV : float
        Alpha particle kinetic energy in MeV.
    Z_daughter : int
        Atomic number of daughter nucleus.
    Z_alpha : int
        Charge of alpha particle (default 2).

    Returns
    -------
    float
        Gamow factor G (dimensionless).
    """
    KE_J = energy_MeV * 1e6 * E_CHARGE
    # Alpha velocity (non-relativistic)
    m_alpha = 4.0 * AMU
    v = math.sqrt(2.0 * KE_J / m_alpha)

    # Sommerfeld parameter: η = Z_d Z_alpha e2 / (4piε0 ℏ v)
    k_e = 8.987551787e9  # Coulomb constant
    eta = Z_daughter * Z_alpha * E_CHARGE ** 2 * k_e / (HBAR * v)

    # Nuclear radius ~ 1.2 x A^(1/3) fm; approximate A_d ~ 4xZ_d (rough)
    A_daughter = 4 * Z_daughter  # rough estimate
    R = 1.2e-15 * (A_daughter ** (1.0 / 3.0) + 4.0 ** (1.0 / 3.0))  # m

    # Classical distance of closest approach: b = Z1 Z2 e2 / (4piε0 E)
    b = Z_daughter * Z_alpha * k_e * E_CHARGE ** 2 / KE_J  # m
    R_over_b = R / b

    if R_over_b >= 1.0:
        return 0.0  # energy exceeds barrier

    sqrt_term = math.sqrt(R_over_b * (1.0 - R_over_b))
    G = 2.0 * eta * (math.acos(math.sqrt(R_over_b)) - sqrt_term)
    return G


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="bell_tunneling_correction",
            description="Bell tunneling correction factor Q_tun for TST reaction rates.",
            input_schema=[
            InputSchemaField(name="barrier_height_eV", type="number", required=False),
            InputSchemaField(name="temperature_K", type="number", required=False),
            InputSchemaField(name="reduced_mass_amu", type="number", required=False),
            InputSchemaField(name="imaginary_frequency_cm1", type="number", required=False),
            InputSchemaField(name="barrier_width_angstrom", type="number", required=False),
            InputSchemaField(name="barrier_height_J", type="number", required=False),
            InputSchemaField(name="mass_kg", type="number", required=False),
            InputSchemaField(name="width_m", type="number", required=False),
            InputSchemaField(name="imaginary_freq_cm_inv", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gamow_factor",
            description="Gamow factor for alpha decay through the Coulomb barrier.",
            input_schema=[
            InputSchemaField(name="energy_MeV", type="number", required=True),
            InputSchemaField(name="Z_daughter", type="number", required=True),
            InputSchemaField(name="Z_alpha", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rectangular_barrier_T",
            description="Transmission coefficient for a rectangular potential barrier.",
            input_schema=[
            InputSchemaField(name="energy_eV", type="number", required=True),
            InputSchemaField(name="barrier_height_eV", type="number", required=True),
            InputSchemaField(name="width_angstrom", type="number", required=True),
            InputSchemaField(name="mass_amu", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="triangular_barrier_T",
            description="WKB transmission coefficient for a triangular (linearly sloped) barrier.",
            input_schema=[
            InputSchemaField(name="energy_eV", type="number", required=True),
            InputSchemaField(name="barrier_height_eV", type="number", required=True),
            InputSchemaField(name="width_angstrom", type="number", required=True),
            InputSchemaField(name="mass_amu", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wkb_transmission",
            description="General WKB transmission coefficient via numerical integration.",
            input_schema=[
            InputSchemaField(name="energy_eV", type="number", required=True),
            InputSchemaField(name="V_func", type="number", required=True),
            InputSchemaField(name="x1", type="number", required=True),
            InputSchemaField(name="x2", type="number", required=True),
            InputSchemaField(name="mass_amu", type="number", required=True),
            InputSchemaField(name="n_points", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
