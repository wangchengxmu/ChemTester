"""
Quantum Tools - General quantum chemistry helpers.

## Solver Instructions (for AI Agent)

When you encounter basic quantum chemistry calculations, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **de Broglie wavelength**: Given mass and velocity -> find lambda
- **Photon energy**: Given frequency -> find energy (E = hν)
- **Heisenberg uncertainty**: Given position uncertainty -> find minimum momentum uncertainty
- **Wavelength-frequency conversion**: Given λ -> ν or ν -> λ (c = λν)

### Step 2: Choose the correct function
- `de_broglie_wavelength(mass_kg, velocity)` -> lambda = h/(mv) in meters
- `energy_from_frequency(freq)` -> E = hν in Joules
- `heisenberg_uncertainty(dx)` -> dp ≥ ℏ/(2·dx) in kg·m/s
- `wavelength_to_frequency(wavelength_m)` -> ν = c/λ in Hz
- `frequency_to_wavelength(freq)` -> λ = c/ν in meters

### Step 3: Handle special cases
- Mass must be in kg (convert amu to kg: multiply by 1.66054e-27)
- velocity must be non-zero
- These are simplified versions; for more complex quantum problems use quantum_mechanics_tools.py or quantum_theory_tools.py

### Examples
1. **de Broglie**: Proton (1.673e-27 kg) at 1.0e6 m/s
   -> `de_broglie_wavelength(1.673e-27, 1.0e6)` -> 3.96e-13 m = 0.396 pm

2. **Photon energy**: ν=5.0e14 Hz
   -> `energy_from_frequency(5.0e14)` -> 3.31e-19 J = 2.07 eV

3. **Heisenberg**: Deltax = 1.0e-15 m (nuclear scale)
   -> `heisenberg_uncertainty(1.0e-15)` -> 1.055e-34/(2x1.0e-15) = 5.28e-20 kg·m/s
"""
import math

def de_broglie_wavelength(mass_kg: float, velocity: float) -> float:
    """de Broglie wavelength: lambda = h/(mv)."""
    h = 6.626e-34
    return h / (mass_kg * velocity)

def energy_from_frequency(freq: float) -> float:
    """E = hν."""
    h = 6.626e-34
    return h * freq

def heisenberg_uncertainty(dx: float) -> float:
    """Minimum momentum uncertainty: dp ≥ ℏ/(2·dx)."""
    hbar = 1.055e-34
    return hbar / (2.0 * dx)


C = 2.998e8  # Speed of light in m/s


def wavelength_to_frequency(wavelength_m: float) -> float:
    """Convert wavelength to frequency: ν = c/λ.
    
    Args:
        wavelength_m: wavelength in meters
    
    Returns:
        frequency in Hz
    """
    return C / wavelength_m


def frequency_to_wavelength(freq: float) -> float:
    """Convert frequency to wavelength: λ = c/ν.
    
    Args:
        freq: frequency in Hz
    
    Returns:
        wavelength in meters
    """
    return C / freq


def energy_from_wavelength(wavelength_m: float) -> float:
    """Photon energy from wavelength: E = hc/λ.
    
    Args:
        wavelength_m: wavelength in meters
    
    Returns:
        energy in joules
    """
    h = 6.626e-34
    return h * C / wavelength_m


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="de_broglie_wavelength",
            description="de Broglie wavelength: lambda = h/(mv).",
            input_schema=[
            InputSchemaField(name="mass_kg", type="number", required=True),
            InputSchemaField(name="velocity", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="energy_from_frequency",
            description="E = hν.",
            input_schema=[
            InputSchemaField(name="freq", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="heisenberg_uncertainty",
            description="Minimum momentum uncertainty: dp ≥ ℏ/(2·dx).",
            input_schema=[
            InputSchemaField(name="dx", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="wavelength_to_frequency",
            description="ν = c/λ. Speed of light / wavelength.",
            input_schema=[
            InputSchemaField(name="wavelength_m", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="frequency_to_wavelength",
            description="λ = c/ν. Speed of light / frequency.",
            input_schema=[
            InputSchemaField(name="freq", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
