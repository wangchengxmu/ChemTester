"""
Bohr Model Tools (L3)
Source: LibreTexts Chemistry 2e Ch06.02

## Solver Instructions (for AI Agent)

When you encounter a Bohr model problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Principal quantum number n: Energy level (n = 1, 2, 3, ...)
- Transition: n_initial -> n_final (emission or absorption)
- Wavelength, frequency, or energy of spectral line
- Ionization energy: Energy to remove electron
- Spectral series: Lyman (UV), Balmer (visible), Paschen (IR)
- Hydrogen-like ion: Nuclear charge Z

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate energy of level n | `energy_level(n)` |
| Calculate energy for transition | `energy_transition(n_initial, n_final)` |
| Calculate wavelength for transition | `wavelength_transition(n_initial, n_final)` |
| Calculate frequency for transition | `frequency_transition(n_initial, n_final)` |
| Identify spectral series | `identify_spectral_series(n_final)` |
| Calculate ionization energy from level n | `ionization_energy_from_level(n)` |
| Get ground state ionization energy | `ground_state_ionization_energy()` |
| Calculate energy for hydrogen-like ion | `energy_level_hydrogen_like(Z, n)` |
| Calculate wavelength for hydrogen-like ion | `wavelength_hydrogen_like(Z, n_initial, n_final)` |
| Convert J to kJ/mol | `J_to_kJ_per_mol(J)` |
| Convert m to nm | `m_to_nm(m)` |

### Step 3: Handle special cases
- **Energy levels**: E_n = -2.18 x 10-18 J / n2 = -13.6 eV / n2 for hydrogen
- **Emission**: n_initial > n_final, energy released (positive DeltaE)
- **Absorption**: n_initial < n_final, energy absorbed (positive DeltaE for electron)
- **Ionization**: Transition to n = ∞
- **Spectral series**: Lyman (n_f=1, UV), Balmer (n_f=2, visible), Paschen (n_f=3, IR)
- **Hydrogen-like ions**: Energy scales with Z2

### Examples

**Example 1: Energy transition**
Question: "Calculate the energy and wavelength for the n=4 -> n=2 transition in hydrogen."
- Solution:
  - `energy_transition(n_initial=4, n_final=2)` -> 4.09 x 10-19 J
  - `wavelength_transition(n_initial=4, n_final=2)` -> 4.86 x 10-7 m = 486 nm (Balmer series, visible)

**Example 2: Ionization energy**
Question: "What is the ionization energy from n=1 for hydrogen?"
- Solution: `ground_state_ionization_energy()` -> 2.18 x 10-18 J = 13.6 eV = 1312 kJ/mol

**Example 3: Spectral series**
Question: "Which spectral series does the n=5 -> n=1 transition belong to?"
- Solution: `identify_spectral_series(n_final=1)` -> ("Lyman", "ultraviolet")

**Example 4: Hydrogen-like ion**
Question: "Calculate the n=2 -> n=1 transition energy for He+ (Z=2)."
- Solution: `energy_level_hydrogen_like(Z=2, n=1)` = -4 x 2.18e-18 = -8.72e-18 J
- `wavelength_hydrogen_like(Z=2, n_initial=2, n_final=1)` -> ~30.4 nm (X-ray region)
"""

# === CONSTANTS ===

RYDBERG_ENERGY = 2.18e-18  # J (for hydrogen)
RYDBERG_CONSTANT = 1.097e7  # m-1 (for wavelength calculations)
PLANCK_CONSTANT = 6.626e-34  # J·s
SPEED_OF_LIGHT = 2.998e8  # m/s
HC = PLANCK_CONSTANT * SPEED_OF_LIGHT  # J·m


# === ENERGY LEVELS ===

def energy_level(n):
    """
    Calculate energy of electron in Bohr orbit n.
    
    E_n = -R_H / n2
    
    Parameters:
        n: principal quantum number (1, 2, 3, ...)
    
    Returns:
        energy in joules (negative, relative to ionized state)
    """
    if n < 1:
        raise ValueError("n must be positive integer")
    return -RYDBERG_ENERGY / (n ** 2)


def energy_transition(n_initial, n_final):
    """
    Calculate energy of photon from electron transition.
    
    DeltaE = E_final - E_initial = R_H x (1/n_f2 - 1/n_i2)
    
    Parameters:
        n_initial: initial principal quantum number
        n_final: final principal quantum number
    
    Returns:
        energy in joules (positive for absorption, negative for emission)
    """
    E_i = energy_level(n_initial)
    E_f = energy_level(n_final)
    return E_f - E_i


def wavelength_transition(n_initial, n_final):
    """
    Calculate wavelength of photon from electron transition.
    
    lambda = h x c / |DeltaE|
    
    Parameters:
        n_initial: initial principal quantum number
        n_final: final principal quantum number
    
    Returns:
        wavelength in meters
    """
    delta_E = abs(energy_transition(n_initial, n_final))
    return HC / delta_E


def frequency_transition(n_initial, n_final):
    """
    Calculate frequency of photon from electron transition.
    
    ν = c / lambda = |DeltaE| / h
    
    Parameters:
        n_initial: initial principal quantum number
        n_final: final principal quantum number
    
    Returns:
        frequency in Hz
    """
    delta_E = abs(energy_transition(n_initial, n_final))
    return delta_E / PLANCK_CONSTANT


# === SPECTRAL SERIES ===

def identify_spectral_series(n_final):
    """
    Identify spectral series from final energy level.
    
    Parameters:
        n_final: final principal quantum number
    
    Returns:
        tuple: (series_name, spectral_region)
    """
    series = {
        1: ("Lyman", "ultraviolet"),
        2: ("Balmer", "visible"),
        3: ("Paschen", "infrared"),
        4: ("Brackett", "infrared"),
        5: ("Pfund", "infrared"),
    }
    return series.get(n_final, (f"n={n_final}", "unknown"))


# === IONIZATION ENERGY ===

def ionization_energy_from_level(n):
    """
    Calculate energy needed to ionize from level n.
    
    Ionization: transition from n to n=∞
    E_ion = -E_n = R_H / n2
    
    Parameters:
        n: initial principal quantum number
    
    Returns:
        ionization energy in joules
    """
    return -energy_level(n)


def ground_state_ionization_energy():
    """
    Return ionization energy from ground state (n=1).
    
    Returns:
        ionization energy in joules (2.18 x 10-18 J)
    """
    return RYDBERG_ENERGY


# === HYDROGEN-LIKE IONS ===

def energy_level_hydrogen_like(Z, n):
    """
    Calculate energy for hydrogen-like ion with nuclear charge Z.
    
    E_n = -Z2 x R_H / n2
    
    Parameters:
        Z: atomic number (nuclear charge)
        n: principal quantum number
    
    Returns:
        energy in joules
    """
    return -Z**2 * RYDBERG_ENERGY / (n ** 2)


def wavelength_hydrogen_like(Z, n_initial, n_final):
    """
    Calculate wavelength for hydrogen-like ion transition.
    
    Parameters:
        Z: atomic number
        n_initial: initial energy level
        n_final: final energy level
    
    Returns:
        wavelength in meters
    """
    delta_E = Z**2 * RYDBERG_ENERGY * abs(1/n_final**2 - 1/n_initial**2)
    return HC / delta_E


# === UNIT CONVERSIONS ===

def J_to_kJ_per_mol(J):
    """Convert joules to kJ/mol."""
    AVOGADRO = 6.022e23
    return J * AVOGADRO / 1000


def m_to_nm(m):
    """Convert meters to nanometers."""
    return m * 1e9


if __name__ == "__main__":
    print("Bohr model tools - implemented")
    
    # Test energy levels
    E1 = energy_level(1)
    E2 = energy_level(2)
    print(f"E_1 = {E1:.2e} J, E_2 = {E2:.2e} J")
    
    # Test transition
    delta_E = energy_transition(2, 1)
    wavelength = wavelength_transition(2, 1)
    print(f"2->1 transition: DeltaE = {delta_E:.2e} J, lambda = {m_to_nm(wavelength):.1f} nm")
    
    # Test spectral series
    series, region = identify_spectral_series(2)
    print(f"n_f=2: {series} series ({region})")
    
    # Test ionization energy
    E_ion = ground_state_ionization_energy()
    print(f"Ionization energy (n=1): {E_ion:.2e} J = {J_to_kJ_per_mol(E_ion):.0f} kJ/mol")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "J_to_kJ_per_mol",
        "description": "Convert joules to kJ/mol.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "J": {
                    "type": "number",
                    "description": "J"
                }
            },
            "required": [
                "J"
            ]
        }
    },
    {
        "name": "energy_level",
        "description": "Calculate energy of electron in Bohr orbit n.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "n"
            ]
        }
    },
    {
        "name": "energy_level_hydrogen_like",
        "description": "Calculate energy for hydrogen-like ion with nuclear charge Z.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Z": {
                    "type": "number",
                    "description": "Z"
                },
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "Z",
                "n"
            ]
        }
    },
    {
        "name": "energy_transition",
        "description": "Calculate energy of photon from electron transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n_initial": {
                    "type": "number",
                    "description": "N Initial"
                },
                "n_final": {
                    "type": "number",
                    "description": "N Final"
                }
            },
            "required": [
                "n_initial",
                "n_final"
            ]
        }
    },
    {
        "name": "frequency_transition",
        "description": "Calculate frequency of photon from electron transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n_initial": {
                    "type": "number",
                    "description": "N Initial"
                },
                "n_final": {
                    "type": "number",
                    "description": "N Final"
                }
            },
            "required": [
                "n_initial",
                "n_final"
            ]
        }
    },
    {
        "name": "ground_state_ionization_energy",
        "description": "Return ionization energy from ground state (n=1).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "identify_spectral_series",
        "description": "Identify spectral series from final energy level.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n_final": {
                    "type": "number",
                    "description": "N Final"
                }
            },
            "required": [
                "n_final"
            ]
        }
    },
    {
        "name": "ionization_energy_from_level",
        "description": "Calculate energy needed to ionize from level n.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "number",
                    "description": "N"
                }
            },
            "required": [
                "n"
            ]
        }
    },
    {
        "name": "m_to_nm",
        "description": "Convert meters to nanometers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "m": {
                    "type": "number",
                    "description": "M"
                }
            },
            "required": [
                "m"
            ]
        }
    },
    {
        "name": "wavelength_hydrogen_like",
        "description": "Calculate wavelength for hydrogen-like ion transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Z": {
                    "type": "number",
                    "description": "Z"
                },
                "n_initial": {
                    "type": "number",
                    "description": "N Initial"
                },
                "n_final": {
                    "type": "number",
                    "description": "N Final"
                }
            },
            "required": [
                "Z",
                "n_initial",
                "n_final"
            ]
        }
    },
    {
        "name": "wavelength_transition",
        "description": "Calculate wavelength of photon from electron transition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n_initial": {
                    "type": "number",
                    "description": "N Initial"
                },
                "n_final": {
                    "type": "number",
                    "description": "N Final"
                }
            },
            "required": [
                "n_initial",
                "n_final"
            ]
        }
    }
]