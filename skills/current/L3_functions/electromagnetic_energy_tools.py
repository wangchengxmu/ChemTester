"""
Electromagnetic Energy Tools (L3)
Source: LibreTexts Chemistry 2e Ch06.01

## Solver Instructions (for AI Agent)

When you encounter an electromagnetic energy problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Wavelength (lambda): Look for "nm", "Å", "m", wavelength values
- Frequency (ν): Look for "Hz", "s-1"
- Energy (E): Look for "J", "kJ/mol", "eV"
- Spectral region: UV, visible, IR, X-ray, etc.
- Photoelectric effect: Work function (φ), kinetic energy

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Convert wavelength -> frequency | `frequency_from_wavelength(wavelength)` |
| Convert frequency -> wavelength | `wavelength_from_frequency(frequency)` |
| Calculate photon energy from wavelength | `photon_energy_from_wavelength(wavelength)` |
| Calculate photon energy from frequency | `photon_energy_from_frequency(frequency)` |
| Calculate wavelength from energy | `wavelength_from_energy(energy)` |
| Identify spectral region | `identify_spectral_region(wavelength_nm)` |
| Photoelectric: KE of ejected electron | `kinetic_energy_ejected_electron(photon_energy, work_function)` |
| Photoelectric: Threshold frequency | `threshold_frequency(work_function)` |
| Photoelectric: Threshold wavelength | `threshold_wavelength(work_function)` |
| Convert J -> eV | `J_to_eV(J)` |
| Convert eV -> J | `eV_to_J(eV)` |
| Convert J -> kJ/mol | `J_to_kJ_per_mol(J)` |
| Convert nm -> m | `nm_to_m(nm)` |
| Convert m -> nm | `m_to_nm(m)` |

### Step 3: Handle special cases
- **Unit conversions**: nm -> m (x10-9), eV -> J (x1.602x10-19)
- **Wavelength for photoelectric**: Must be ≤ threshold wavelength for ejection
- **Spectral regions**: UV < 400 nm, Visible 400-700 nm, IR > 700 nm
- **Energy per mole**: Multiply single photon energy by Avogadro's number

### Examples

**Example 1: Wavelength to energy**
Question: "Calculate the energy of a photon with wavelength 500 nm."
- Given: lambda = 500 nm = 500 x 10-9 m
- Solution: `photon_energy_from_wavelength(wavelength=500e-9)` -> 3.97 x 10-19 J = 2.48 eV

**Example 2: Frequency to wavelength**
Question: "What is the wavelength of light with frequency 6.0 x 1014 Hz?"
- Solution: `wavelength_from_frequency(frequency=6e14)` -> 5.0 x 10-7 m = 500 nm

**Example 3: Photoelectric effect**
Question: "Can 400 nm light eject electrons from sodium (work function = 2.28 eV)?"
- Step 1: Convert work function to J: `eV_to_J(2.28)` -> 3.65 x 10-19 J
- Step 2: Calculate photon energy: `photon_energy_from_wavelength(400e-9)` -> 4.97 x 10-19 J
- Step 3: Compare: photon energy > work function -> Yes, electrons ejected
- KE: `kinetic_energy_ejected_electron(4.97e-19, 3.65e-19)` -> 1.32 x 10-19 J

**Example 4: Spectral region**
Question: "In what spectral region is 250 nm radiation?"
- Solution: `identify_spectral_region(wavelength_nm=250)` -> "ultraviolet"
"""

# === CONSTANTS ===

SPEED_OF_LIGHT = 2.998e8  # m/s
PLANCK_CONSTANT = 6.626e-34  # J·s
HC = PLANCK_CONSTANT * SPEED_OF_LIGHT  # J·m


# === WAVE EQUATION ===

def wavelength_from_frequency(frequency):
    if not frequency:
        raise ValueError("frequency must be non-zero")
    return SPEED_OF_LIGHT / frequency


def frequency_from_wavelength(wavelength):
    if not wavelength:
        raise ValueError("wavelength must be non-zero")
    return SPEED_OF_LIGHT / wavelength


# === PHOTON ENERGY ===

def photon_energy_from_frequency(frequency):
    """
    Calculate photon energy from frequency.
    
    E = h x ν
    
    Parameters:
        frequency: frequency in Hz
    
    Returns:
        energy in joules
    """
    return PLANCK_CONSTANT * frequency


def photon_energy_from_wavelength(wavelength, unit='m'):
    """
    Calculate photon energy from wavelength.
    
    E = h x c / lambda
    
    Parameters:
        wavelength: wavelength value
        unit: 'm' (meters, default), 'nm' (nanometers), 'um' (micrometers), 'pm' (picometers)
    
    Returns:
        energy in joules
    """
    conversions = {'m': 1, 'nm': 1e-9, 'um': 1e-6, 'pm': 1e-12}
    if unit not in conversions:
        raise ValueError(f"unit must be one of {list(conversions.keys())}, got '{unit}'")
    return HC / (wavelength * conversions[unit])


def wavelength_from_energy(energy):
    if not energy:
        raise ValueError("energy must be non-zero")
    return HC / energy


# === PHOTOELECTRIC EFFECT ===

def kinetic_energy_ejected_electron(photon_energy, work_function):
    """
    Calculate kinetic energy of ejected electron.
    
    E_k = hν - φ
    
    Parameters:
        photon_energy: photon energy in joules
        work_function: work function (threshold energy) in joules
    
    Returns:
        kinetic energy in joules (returns 0 if photon energy < work function)
    """
    if photon_energy < work_function:
        return 0  # No electron ejected
    return photon_energy - work_function


def threshold_frequency(work_function):
    """
    Calculate minimum frequency needed for photoelectric effect.
    
    ν_0 = φ / h
    
    Parameters:
        work_function: work function in joules
    
    Returns:
        threshold frequency in Hz
    """
    return work_function / PLANCK_CONSTANT


def threshold_wavelength(work_function):
    """
    Calculate maximum wavelength that can cause photoelectric effect.
    
    lambda_0 = h x c / φ
    
    Parameters:
        work_function: work function in joules
    
    Returns:
        threshold wavelength in meters
    """
    return HC / work_function


# === UNIT CONVERSIONS ===

def nm_to_m(nm):
    """Convert nanometers to meters."""
    return nm * 1e-9


def m_to_nm(m):
    """Convert meters to nanometers."""
    return m * 1e9


def J_to_eV(J):
    """Convert joules to electron volts."""
    return J / 1.602e-19


def eV_to_J(eV):
    """Convert electron volts to joules."""
    return eV * 1.602e-19


def J_to_kJ_per_mol(J):
    """Convert joules per photon to kJ per mole."""
    AVOGADRO = 6.022e23
    return J * AVOGADRO / 1000


# === SPECTRAL REGION ===

def identify_spectral_region(wavelength_nm):
    """
    Identify the spectral region from wavelength.
    
    Parameters:
        wavelength_nm: wavelength in nanometers
    
    Returns:
        string describing spectral region
    """
    if wavelength_nm < 0.01:
        return "gamma ray"
    elif wavelength_nm < 10:
        return "X-ray"
    elif wavelength_nm < 400:
        return "ultraviolet"
    elif wavelength_nm <= 700:
        return "visible"
    elif wavelength_nm < 1e6:
        return "infrared"
    elif wavelength_nm < 1e9:
        return "microwave"
    else:
        return "radio"


if __name__ == "__main__":
    print("Electromagnetic energy tools - implemented")
    
    # Test wavelength/frequency
    nu = frequency_from_wavelength(500e-9)  # 500 nm
    print(f"Frequency of 500 nm light: {nu:.2e} Hz")
    
    # Test photon energy
    E = photon_energy_from_wavelength(500e-9)
    print(f"Energy of 500 nm photon: {E:.2e} J = {J_to_eV(E):.2f} eV")
    
    # Test photoelectric effect
    E_k = kinetic_energy_ejected_electron(1e-18, 5e-19)
    print(f"Kinetic energy (hν=1e-18 J, φ=5e-19 J): {E_k:.2e} J")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "J_to_eV",
        "description": "Convert joules to electron volts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "J": {"type": "number", "description": "J"},
            },
            "required": ["J"]
        }
    },
    {
        "name": "J_to_kJ_per_mol",
        "description": "Convert joules per photon to kJ per mole.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "J": {"type": "number", "description": "J"},
            },
            "required": ["J"]
        }
    },
    {
        "name": "eV_to_J",
        "description": "Convert electron volts to joules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "eV": {"type": "number", "description": "Ev"},
            },
            "required": ["eV"]
        }
    },
    {
        "name": "frequency_from_wavelength",
        "description": "Calculate frequency from wavelength.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavelength": {"type": "number", "description": "Wavelength"},
            },
            "required": ["wavelength"]
        }
    },
    {
        "name": "identify_spectral_region",
        "description": "Identify the spectral region from wavelength.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavelength_nm": {"type": "number", "description": "Wavelength Nm"},
            },
            "required": ["wavelength_nm"]
        }
    },
    {
        "name": "kinetic_energy_ejected_electron",
        "description": "Calculate kinetic energy of ejected electron.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "photon_energy": {"type": "number", "description": "Photon Energy"},
                "work_function": {"type": "number", "description": "Work Function"},
            },
            "required": ["photon_energy", "work_function"]
        }
    },
    {
        "name": "m_to_nm",
        "description": "Convert meters to nanometers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "m": {"type": "number", "description": "M"},
            },
            "required": ["m"]
        }
    },
    {
        "name": "nm_to_m",
        "description": "Convert nanometers to meters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nm": {"type": "number", "description": "Nm"},
            },
            "required": ["nm"]
        }
    },
    {
        "name": "photon_energy_from_frequency",
        "description": "Calculate photon energy from frequency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "frequency": {"type": "number", "description": "Frequency"},
            },
            "required": ["frequency"]
        }
    },
    {
        "name": "photon_energy_from_wavelength",
        "description": "Calculate photon energy from wavelength. Supports nm, um, pm units.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "wavelength": {"type": "number", "description": "Wavelength value"},
                "unit": {"type": "string", "enum": ["m", "nm", "um", "pm"], "description": "Unit of wavelength (default: 'm')"},
            },
            "required": ["wavelength"]
        }
    },
    {
        "name": "threshold_frequency",
        "description": "Calculate minimum frequency needed for photoelectric effect.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "work_function": {"type": "number", "description": "Work Function"},
            },
            "required": ["work_function"]
        }
    },
    {
        "name": "threshold_wavelength",
        "description": "Calculate maximum wavelength that can cause photoelectric effect.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "work_function": {"type": "number", "description": "Work Function"},
            },
            "required": ["work_function"]
        }
    },
    {
        "name": "wavelength_from_energy",
        "description": "Calculate wavelength from photon energy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "energy": {"type": "number", "description": "Energy"},
            },
            "required": ["energy"]
        }
    },
    {
        "name": "wavelength_from_frequency",
        "description": "Calculate wavelength from frequency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "frequency": {"type": "number", "description": "Frequency"},
            },
            "required": ["frequency"]
        }
    }
]
