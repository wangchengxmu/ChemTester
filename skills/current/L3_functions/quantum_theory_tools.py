"""
Quantum Theory Tools (L3)
Source: LibreTexts Chemistry 2e Ch06.03

## Solver Instructions (for AI Agent)

When you encounter basic quantum theory problems (de Broglie wavelength, Heisenberg uncertainty, photoelectric effect, energy levels), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **de Broglie wavelength**: Given mass and velocity -> find lambda; or given lambda -> find velocity
- **Heisenberg uncertainty**: Given Deltax -> find minimum Deltap (or vice versa)
- **Photon energy**: Given frequency/wavelength -> find E
- **Photoelectric effect**: Given light frequency and work function -> find KE of ejected electron
- **Bohr model**: Given principal quantum number n -> find energy, radius, or transition wavelength

### Step 2: Choose the correct function
- `de_broglie_wavelength(mass, velocity)` -> lambda = h/(mv) in meters; mass in kg, velocity in m/s
- `de_broglie_wavelength_electron(velocity)` -> convenience wrapper for electrons
- `de_broglie_wavelength_accelerated(accelerating_voltage_volts)` -> for particles accelerated through voltage V (VOLTS, not eV); e.g. 100 V electron gives ~1.226 Å
- `de_broglie_wavelength_from_energy(kinetic_energy_J)` -> from kinetic energy in joules
- `uncertainty_position(uncertainty_momentum)` -> Deltax ≥ h/(4piDeltap)
- `uncertainty_momentum(uncertainty_position)` -> Deltap ≥ h/(4piDeltax)
- `photon_energy(frequency)` -> E = hν
- `photon_energy_wavelength(wavelength)` -> E = hc/lambda
- `photoelectron_ke(frequency, work_function)` -> KE = hν - φ
- `bohr_energy(n)` -> E_n = -2.18e-18/n2 J (or -13.6/n2 eV)
- `bohr_radius(n)` -> r_n = 5.29e-11 x n2 m

### Step 3: Handle special cases
- Velocity cannot be zero for de Broglie (raises ValueError)
- Photoelectric effect: if hν < φ, no electrons are ejected (KE would be negative)
- Heisenberg gives minimum uncertainty; actual uncertainty can be larger
- All results in SI units unless specifically noted

### Examples
1. **de Broglie from mass and velocity**: Electron moving at 2.0e6 m/s
   -> `de_broglie_wavelength(9.109e-31, 2.0e6)` -> 3.64e-10 m = 0.364 nm

2. **de Broglie from accelerating voltage**: Electron accelerated through 100 V
   -> `de_broglie_wavelength_accelerated(100)` -> 1.226e-10 m ≈ 1.226 Å
   NOTE: The argument is VOLTS (100), not eV!

2. **Photoelectric effect**: Light at ν=2.0e15 Hz hits metal with φ=4.5e-19 J
   -> `photoelectron_ke(2.0e15, 4.5e-19)` -> 6.626e-34x2.0e15 - 4.5e-19 = 8.75e-19 J

3. **Heisenberg**: Electron confined to Deltax = 1.0e-10 m
   -> `uncertainty_momentum(1.0e-10)` -> Deltap ≥ 6.626e-34/(4pix1.0e-10) = 5.27e-25 kg·m/s
"""

# === CONSTANTS ===

PLANCK_CONSTANT = 6.626e-34  # J·s
ELECTRON_MASS = 9.109e-31  # kg
PROTON_MASS = 1.673e-27  # kg
NEUTRON_MASS = 1.675e-27  # kg
ELECTRON_CHARGE = 1.602e-19  # C


# === DE BROGLIE WAVELENGTH ===

def de_broglie_wavelength(mass, velocity):
    """
    Calculate de Broglie wavelength of a particle.
    
    lambda = h / (m x v)
    
    Parameters:
        mass: mass in kg
        velocity: velocity in m/s
    
    Returns:
        wavelength in meters
    """
    if velocity == 0:
        raise ValueError("Velocity cannot be zero")
    return PLANCK_CONSTANT / (mass * velocity)


def de_broglie_wavelength_electron(velocity):
    """
    Calculate de Broglie wavelength of an electron.
    
    Parameters:
        velocity: velocity in m/s
    
    Returns:
        wavelength in meters
    """
    return de_broglie_wavelength(ELECTRON_MASS, velocity)


def de_broglie_wavelength_accelerated(accelerating_voltage_volts, mass=ELECTRON_MASS):
    """
    Calculate de Broglie wavelength of a charged particle accelerated
    through an electric potential difference.

    Physics: A particle with charge q = e (electron charge) accelerated
    through potential V gains kinetic energy KE = eV. From KE = ½mv²,
    the velocity v = sqrt(2eV/m), giving:
        λ = h / (m·v) = h / sqrt(2·m·e·V)

    Parameters:
        accelerating_voltage_volts (float): Electric potential difference
            in VOLTS (not eV!). e.g. 100 means 100 V = 100 J/C.
            Common values: 50-300 V for electron diffraction tubes.
        mass (float): Particle mass in kg. Default is electron mass
            (9.109×10⁻³¹ kg). Use PROTON_MASS or NEUTRON_MASS for other particles.

    Returns:
        float: Wavelength in meters.

    Examples:
        >>> de_broglie_wavelength_accelerated(100)           # 100 V electron
        1.226e-10  # ≈ 1.226 Å
        >>> de_broglie_wavelength_accelerated(1000)          # 1 kV electron
        3.878e-11  # ≈ 0.039 nm
    """
    import math
    if accelerating_voltage_volts <= 0:
        raise ValueError("Accelerating voltage must be positive")
    return PLANCK_CONSTANT / math.sqrt(2 * mass * ELECTRON_CHARGE * accelerating_voltage_volts)


def de_broglie_wavelength_from_energy(energy_J, mass=ELECTRON_MASS):
    """
    Calculate de Broglie wavelength from kinetic energy.
    
    KE = 0.5 * m * v²
    v = sqrt(2*KE/m)
    lambda = h / (m * v) = h / sqrt(2 * m * KE)
    
    Parameters:
        energy_J: kinetic energy in joules
        mass: mass in kg (default: electron mass)
    
    Returns:
        wavelength in meters
    """
    import math
    if energy_J <= 0:
        raise ValueError("Energy must be positive")
    return PLANCK_CONSTANT / math.sqrt(2 * mass * energy_J)


def velocity_from_wavelength(mass, wavelength):
    """
    Calculate velocity from de Broglie wavelength.
    
    v = h / (m x lambda)
    
    Parameters:
        mass: mass in kg
        wavelength: wavelength in meters
    
    Returns:
        velocity in m/s
    """
    return PLANCK_CONSTANT / (mass * wavelength)


# === HEISENBERG UNCERTAINTY PRINCIPLE ===

def uncertainty_position(uncertainty_momentum):
    """
    Calculate minimum uncertainty in position.
    
    Deltax ≥ h / (4pi x Deltap)
    
    Parameters:
        uncertainty_momentum: uncertainty in momentum (kg·m/s)
    
    Returns:
        minimum uncertainty in position (m)
    """
    return PLANCK_CONSTANT / (4 * 3.14159 * uncertainty_momentum)


def uncertainty_momentum(uncertainty_position):
    """
    Calculate minimum uncertainty in momentum.
    
    Deltap ≥ h / (4pi x Deltax)
    
    Parameters:
        uncertainty_position: uncertainty in position (m)
    
    Returns:
        minimum uncertainty in momentum (kg·m/s)
    """
    return PLANCK_CONSTANT / (4 * 3.14159 * uncertainty_position)


def uncertainty_velocity(mass, uncertainty_position):
    """
    Calculate minimum uncertainty in velocity.
    
    Deltav ≥ h / (4pi x m x Deltax)
    
    Parameters:
        mass: mass in kg
        uncertainty_position: uncertainty in position (m)
    
    Returns:
        minimum uncertainty in velocity (m/s)
    """
    return PLANCK_CONSTANT / (4 * 3.14159 * mass * uncertainty_position)


# === QUANTUM NUMBERS ===

def valid_quantum_numbers(n, l, m_l, m_s):
    """
    Check if a set of quantum numbers is valid.
    
    Rules:
    - n: positive integer (1, 2, 3, ...)
    - l: integer from 0 to n-1
    - m_l: integer from -l to +l
    - m_s: +1/2 or -1/2
    
    Parameters:
        n: principal quantum number
        l: angular momentum quantum number
        m_l: magnetic quantum number
        m_s: spin quantum number
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Check n
    if not isinstance(n, int) or n < 1:
        return False
    
    # Check l
    if not isinstance(l, int) or l < 0 or l >= n:
        return False
    
    # Check m_l
    if not isinstance(m_l, int) or m_l < -l or m_l > l:
        return False
    
    # Check m_s
    if m_s not in (0.5, -0.5, 1/2, -1/2):
        return False
    
    return True


def orbital_count(n):
    """
    Calculate number of orbitals in shell n.
    
    Number of orbitals = n2
    
    Parameters:
        n: principal quantum number
    
    Returns:
        number of orbitals
    """
    return n ** 2


def electron_capacity(n):
    """
    Calculate maximum electrons in shell n.
    
    Max electrons = 2n2
    
    Parameters:
        n: principal quantum number
    
    Returns:
        maximum electrons
    """
    return 2 * n ** 2


def orbitals_in_subshell(l):
    """
    Calculate number of orbitals in subshell.
    
    Parameters:
        l: angular momentum quantum number
    
    Returns:
        number of orbitals (2l + 1)
    """
    return 2 * l + 1


def electrons_in_subshell(l):
    """
    Calculate maximum electrons in subshell.
    
    Parameters:
        l: angular momentum quantum number
    
    Returns:
        maximum electrons (2(2l + 1) = 4l + 2)
    """
    return 2 * (2 * l + 1)


def subshell_name(l):
    """
    Get subshell name from l value.
    
    Parameters:
        l: angular momentum quantum number
    
    Returns:
        subshell name (s, p, d, f)
    """
    names = {0: 's', 1: 'p', 2: 'd', 3: 'f'}
    if l in names:
        return names[l]
    # For higher l values, use letter sequence
    if l > 3:
        return chr(ord('g') + l - 4)
    return '?'


def l_from_subshell(name):
    """
    Get l value from subshell name.
    
    Parameters:
        name: subshell name (s, p, d, f)
    
    Returns:
        l value
    """
    names = {'s': 0, 'p': 1, 'd': 2, 'f': 3}
    return names.get(name.lower())


# === UNIT CONVERSIONS ===

def m_to_pm(m):
    """Convert meters to picometers."""
    return m * 1e12


def m_to_nm(m):
    """Convert meters to nanometers."""
    return m * 1e9


if __name__ == "__main__":
    print("Quantum theory tools - implemented")
    
    # Test de Broglie wavelength
    v = 1e6  # m/s (typical electron velocity)
    lambda_e = de_broglie_wavelength_electron(v)
    print(f"Electron velocity {v:.0e} m/s: lambda = {m_to_pm(lambda_e):.1f} pm")
    
    # Test uncertainty
    delta_x = 1e-10  # 100 pm
    delta_v = uncertainty_velocity(ELECTRON_MASS, delta_x)
    print(f"Deltax = {m_to_pm(delta_x):.0f} pm: Deltav ≥ {delta_v:.2e} m/s")
    
    # Test quantum numbers
    print(f"(3, 2, 1, +1/2) valid: {valid_quantum_numbers(3, 2, 1, 0.5)}")
    print(f"(3, 3, 0, +1/2) valid: {valid_quantum_numbers(3, 3, 0, 0.5)}")  # Invalid: l >= n
    
    # Test orbital counts
    print(f"n=3: {orbital_count(3)} orbitals, {electron_capacity(3)} electrons max")
    print(f"l=2 (d): {orbitals_in_subshell(2)} orbitals, {electrons_in_subshell(2)} electrons max")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="de_broglie_wavelength",
            description="Calculate de Broglie wavelength of a particle.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="velocity", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="de_broglie_wavelength_electron",
            description="Calculate de Broglie wavelength of an electron.",
            input_schema=[
            InputSchemaField(name="velocity", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="electron_capacity",
            description="Calculate maximum electrons in shell n.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="electrons_in_subshell",
            description="Calculate maximum electrons in subshell.",
            input_schema=[
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="l_from_subshell",
            description="Get l value from subshell name.",
            input_schema=[
            InputSchemaField(name="name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="m_to_nm",
            description="Convert meters to nanometers.",
            input_schema=[
            InputSchemaField(name="m", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="m_to_pm",
            description="Convert meters to picometers.",
            input_schema=[
            InputSchemaField(name="m", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="orbital_count",
            description="Calculate number of orbitals in shell n.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="orbitals_in_subshell",
            description="Calculate number of orbitals in subshell.",
            input_schema=[
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="subshell_name",
            description="Get subshell name from l value.",
            input_schema=[
            InputSchemaField(name="l", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="uncertainty_momentum",
            description="Calculate minimum uncertainty in momentum.",
            input_schema=[
            InputSchemaField(name="uncertainty_position", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="uncertainty_position",
            description="Calculate minimum uncertainty in position.",
            input_schema=[
            InputSchemaField(name="uncertainty_momentum", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="uncertainty_velocity",
            description="Calculate minimum uncertainty in velocity.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="uncertainty_position", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="valid_quantum_numbers",
            description="Check if a set of quantum numbers is valid.",
            input_schema=[
            InputSchemaField(name="n", type="number", required=True),
            InputSchemaField(name="l", type="number", required=True),
            InputSchemaField(name="m_l", type="number", required=True),
            InputSchemaField(name="m_s", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="velocity_from_wavelength",
            description="Calculate velocity from de Broglie wavelength.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="wavelength", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
