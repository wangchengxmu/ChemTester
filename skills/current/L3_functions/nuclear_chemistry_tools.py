"""
Nuclear Chemistry Tools - L3 Implementation
Chapter 21: Nuclear Chemistry

## Solver Instructions (for AI Agent)

When you encounter nuclear chemistry problems (half-life, decay, binding energy), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given half-life -> calculate decay constant or remaining amount?
- Given initial and final amounts -> calculate time elapsed?
- Given isotopes and masses -> calculate binding energy or mass defect?
- Given decay chain -> calculate activity?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Half-life to lambda | `half_life_to_decay_constant(half_life)` | lambda = ln(2) / t½ |
| Decay constant to t½ | `decay_constant_to_half_life(decay_constant)` | t½ = ln(2) / lambda |
| Remaining amount | `remaining_amount(initial, time, half_life)` | N = N0 x (½)^(t/t½) |
| Remaining fraction | `remaining_fraction(time, half_life)` | f = (½)^(t/t½) |
| Time to decay | `time_to_decay(initial, final, half_life)` | t = t½ x log2(N0/N) |
| Binding energy | `binding_energy(A, Z, mass_defect)` | E = Deltam x c2 (in MeV) |
| Mass defect | `mass_defect(A, Z, actual_mass)` | Deltam = Zxmₚ + (A-Z)xmₙ - M_actual |

### Step 3: Handle special cases
- Use consistent units (half-life in seconds, time in seconds)
- Masses in amu; binding energy converted to MeV (1 amu = 931.5 MeV)
- Activity: A = lambdaN (Bq = decays per second)

### Examples
```python
# Example 1: Half-life to decay constant
half_life_to_decay_constant(5730 * 365.25 * 24 * 3600)  # C-14
# -> lambda ~ 3.83e-12 s-1

# Example 2: Remaining amount after 2 half-lives
remaining_amount(100, 2, 1)  # N0=100, t=2, t½=1
# -> 25

# Example 3: Binding energy for He-4
binding_energy(4, 2, 0.0304)  # mass defect = 0.0304 amu
# -> ~28.3 MeV

# Example 4: Time for 75% decay
time_to_decay(100, 25, 5730)  # C-14 half-life in years
# -> ~11460 years (2 half-lives)
```
"""

from typing import Dict, Tuple, Optional
import math

# Physical constants
C = 2.998e8  # Speed of light (m/s)
AMU_TO_KG = 1.66054e-27  # kg per amu
AMU_TO_MEV = 931.5  # MeV per amu
E_CHARGE = 1.602e-19  # Coulomb

# Particle masses in amu
PARTICLE_MASSES = {
    'proton': 1.00728,
    'neutron': 1.00867,
    'electron': 0.00055
}


def half_life_to_decay_constant(half_life: float) -> float:
    """
    Convert half-life to decay constant.
    
    lambda = ln(2) / t1/2
    
    Args:
        half_life: Half-life in seconds
    
    Returns:
        Decay constant (s-1)
    
    Examples:
        >>> round(half_life_to_decay_constant(100), 6)
        0.006931
    """
    return math.log(2) / half_life


def decay_constant_to_half_life(decay_constant: float) -> float:
    """
    Convert decay constant to half-life.
    
    t1/2 = ln(2) / lambda
    
    Args:
        decay_constant: Decay constant (s-1)
    
    Returns:
        Half-life in seconds
    """
    return math.log(2) / decay_constant


def remaining_amount(initial_amount: float, time: float, half_life: float) -> float:
    """
    Calculate remaining amount after decay.
    
    N = N0 x (1/2)^(t/t1/2)
    
    Args:
        initial_amount: Initial amount N0
        time: Time elapsed
        half_life: Half-life
    
    Returns:
        Remaining amount
    """
    return initial_amount * (0.5 ** (time / half_life))


def remaining_fraction(time: float, half_life: float) -> float:
    """
    Calculate fraction remaining after decay.
    
    Args:
        time: Time elapsed
        half_life: Half-life
    
    Returns:
        Fraction remaining (0 to 1)
    """
    return 0.5 ** (time / half_life)


def time_to_decay(initial_amount: float, final_amount: float, half_life: float) -> float:
    """
    Calculate time required to decay from initial to final amount.
    
    t = t1/2 x log2(N0/N)
    
    Args:
        initial_amount: Initial amount N0
        final_amount: Final amount N
        half_life: Half-life
    
    Returns:
        Time required
    """
    return half_life * math.log2(initial_amount / final_amount)


def activity(nuclei_count: int, decay_constant: float) -> float:
    """
    Calculate activity (decays per second).
    
    A = lambdaN
    
    Args:
        nuclei_count: Number of radioactive nuclei
        decay_constant: Decay constant (s-1)
    
    Returns:
        Activity in Bq (decays/s)
    """
    return decay_constant * nuclei_count


def binding_energy(protons: int, neutrons: int, actual_mass: float) -> float:
    """
    Calculate nuclear binding energy in MeV.
    
    BE = Deltam x c2
    
    Args:
        protons: Number of protons (Z)
        neutrons: Number of neutrons (N)
        actual_mass: Measured atomic mass in amu
    
    Returns:
        Binding energy in MeV
    
    Examples:
        >>> round(binding_energy(2, 2, 4.0026), 1)
        28.3
    """
    # Calculate mass of constituent particles
    calculated_mass = (protons * PARTICLE_MASSES['proton'] +
                       neutrons * PARTICLE_MASSES['neutron'] +
                       protons * PARTICLE_MASSES['electron'])
    
    # Mass defect
    mass_defect = calculated_mass - actual_mass
    
    # Convert to energy (MeV)
    return mass_defect * AMU_TO_MEV


def binding_energy_per_nucleon(protons: int, neutrons: int, actual_mass: float) -> float:
    """
    Calculate binding energy per nucleon in MeV.
    
    Args:
        protons: Number of protons
        neutrons: Number of neutrons
        actual_mass: Measured atomic mass in amu
    
    Returns:
        Binding energy per nucleon in MeV
    """
    total_be = binding_energy(protons, neutrons, actual_mass)
    return total_be / (protons + neutrons)


def balance_nuclear_equation(reactant_a: int, reactant_z: int,
                             product_a: int, product_z: int) -> Tuple[int, int]:
    """
    Find missing particle in nuclear equation.
    
    Given: R1 + R2 -> P1 + P2
    Find P2 given R2 is unknown
    
    Args:
        reactant_a: Sum of mass numbers on reactant side
        reactant_z: Sum of atomic numbers on reactant side
        product_a: Known product mass number
        product_z: Known product atomic number
    
    Returns:
        (mass_number, atomic_number) of missing particle
    
    Examples:
        >>> balance_nuclear_equation(25, 12, 1, 1)  # Mg-25 + He-4 -> H-1 + ?
        (28, 13)
    """
    missing_a = reactant_a - product_a
    missing_z = reactant_z - product_z
    return (missing_a, missing_z)


def predict_decay_mode(protons: int, neutrons: int) -> str:
    """
    Predict decay mode based on n:p ratio vs band of stability.
    
    Args:
        protons: Number of protons
        neutrons: Number of neutrons
    
    Returns:
        Predicted decay mode
    
    Examples:
        >>> predict_decay_mode(6, 8)  # C-14, high n:p
        'beta_minus'
        >>> predict_decay_mode(8, 7)  # O-15, low n:p
        'positron'
    """
    np_ratio = neutrons / protons if protons > 0 else 0
    
    # Band of stability approximation
    # Light nuclei: n:p ~ 1
    # Heavy nuclei: n:p ~ 1.5
    
    if protons > 83:
        return 'alpha'  # Heavy nuclei
    elif np_ratio > 1.5:
        return 'beta_minus'  # Neutron rich
    elif np_ratio < 1.0:
        return 'positron'  # Proton rich
    elif np_ratio > 1.2 and protons < 20:
        return 'beta_minus'
    else:
        return 'stable'


def daughter_nuclide(parent_a: int, parent_z: int, decay_type: str) -> Tuple[int, int]:
    """
    Calculate daughter nuclide after decay.
    
    Args:
        parent_a: Parent mass number
        parent_z: Parent atomic number
        decay_type: 'alpha', 'beta_minus', 'beta_plus', 'electron_capture'
    
    Returns:
        (mass_number, atomic_number) of daughter
    
    Examples:
        >>> daughter_nuclide(238, 92, 'alpha')
        (234, 90)
        >>> daughter_nuclide(14, 6, 'beta_minus')
        (14, 7)
    """
    if decay_type == 'alpha':
        return (parent_a - 4, parent_z - 2)
    elif decay_type == 'beta_minus':
        return (parent_a, parent_z + 1)
    elif decay_type == 'beta_plus':
        return (parent_a, parent_z - 1)
    elif decay_type == 'electron_capture':
        return (parent_a, parent_z - 1)
    else:
        return (parent_a, parent_z)


def decay_chain_steps(initial_a: int, initial_z: int, 
                      decay_types: list) -> list:
    """
    Calculate decay chain through multiple steps.
    
    Args:
        initial_a: Initial mass number
        initial_z: Initial atomic number
        decay_types: List of decay types
    
    Returns:
        List of (A, Z) tuples including initial nuclide
    """
    chain = [(initial_a, initial_z)]
    a, z = initial_a, initial_z
    
    for decay in decay_types:
        a, z = daughter_nuclide(a, z, decay)
        chain.append((a, z))
    
    return chain


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="activity",
            description="Calculate activity (decays per second).",
            input_schema=[
            InputSchemaField(name="nuclei_count", type="number", required=True),
            InputSchemaField(name="decay_constant", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="balance_nuclear_equation",
            description="Find missing particle in nuclear equation.",
            input_schema=[
            InputSchemaField(name="reactant_a", type="number", required=True),
            InputSchemaField(name="reactant_z", type="number", required=True),
            InputSchemaField(name="product_a", type="number", required=True),
            InputSchemaField(name="product_z", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="binding_energy",
            description="Calculate nuclear binding energy in MeV.",
            input_schema=[
            InputSchemaField(name="protons", type="number", required=True),
            InputSchemaField(name="neutrons", type="number", required=True),
            InputSchemaField(name="actual_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="binding_energy_per_nucleon",
            description="Calculate binding energy per nucleon in MeV.",
            input_schema=[
            InputSchemaField(name="protons", type="number", required=True),
            InputSchemaField(name="neutrons", type="number", required=True),
            InputSchemaField(name="actual_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="daughter_nuclide",
            description="Calculate daughter nuclide after decay.",
            input_schema=[
            InputSchemaField(name="parent_a", type="number", required=True),
            InputSchemaField(name="parent_z", type="number", required=True),
            InputSchemaField(name="decay_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="decay_chain_steps",
            description="Calculate decay chain through multiple steps.",
            input_schema=[
            InputSchemaField(name="initial_a", type="number", required=True),
            InputSchemaField(name="initial_z", type="number", required=True),
            InputSchemaField(name="decay_types", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="decay_constant_to_half_life",
            description="Convert decay constant to half-life.",
            input_schema=[
            InputSchemaField(name="decay_constant", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="half_life_to_decay_constant",
            description="Convert half-life to decay constant.",
            input_schema=[
            InputSchemaField(name="half_life", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_decay_mode",
            description="Predict decay mode based on n:p ratio vs band of stability.",
            input_schema=[
            InputSchemaField(name="protons", type="number", required=True),
            InputSchemaField(name="neutrons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="remaining_amount",
            description="Calculate remaining amount after decay.",
            input_schema=[
            InputSchemaField(name="initial_amount", type="number", required=True),
            InputSchemaField(name="time", type="number", required=True),
            InputSchemaField(name="half_life", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="remaining_fraction",
            description="Calculate fraction remaining after decay.",
            input_schema=[
            InputSchemaField(name="time", type="number", required=True),
            InputSchemaField(name="half_life", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="time_to_decay",
            description="Calculate time required to decay from initial to final amount.",
            input_schema=[
            InputSchemaField(name="initial_amount", type="number", required=True),
            InputSchemaField(name="final_amount", type="number", required=True),
            InputSchemaField(name="half_life", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
