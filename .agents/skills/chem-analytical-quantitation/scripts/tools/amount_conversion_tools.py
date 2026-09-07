from __future__ import annotations

import math

AVOGADRO = 6.02214076e23


def mass_to_moles(mass_g: float, molar_mass_g_per_mol: float) -> float:
    if molar_mass_g_per_mol <= 0:
        raise ValueError("molar_mass_g_per_mol must be > 0")
    return mass_g / molar_mass_g_per_mol


def moles_to_mass(moles: float, molar_mass_g_per_mol: float) -> float:
    if molar_mass_g_per_mol <= 0:
        raise ValueError("molar_mass_g_per_mol must be > 0")
    return moles * molar_mass_g_per_mol


def moles_to_particles(moles: float) -> float:
    return moles * AVOGADRO


def particles_to_moles(particles: float) -> float:
    if particles < 0:
        raise ValueError("particles must be >= 0")
    return particles / AVOGADRO


def convert_amount(
    value: float,
    from_type: str,
    to_type: str,
    molar_mass_g_per_mol: float | None = None,
) -> float:
    """
    Generic converter among: mass_g, moles, particles.
    Uses moles as bridge.

    Solver Instructions (for AI Agent):

    When you encounter amount/mass/mole/particle conversion or dilution problems, follow this decision tree:

    Step 1: Identify what is given and what is asked
    Step 2: Choose the correct function
    Step 3: Handle special cases

    Examples:
        mass_to_moles(18.0, 18.015) -> 0.999 mol H2O
        dilution_volume(6.0, 0.5, 1.0) -> 0.0833 L
    """
    from_type = from_type.lower()
    to_type = to_type.lower()

    valid = {"mass_g", "moles", "particles"}
    if from_type not in valid or to_type not in valid:
        raise ValueError(f"from_type/to_type must be one of {valid}")

    if from_type == to_type:
        return value

    # Convert source to moles first
    if from_type == "moles":
        moles = value
    elif from_type == "mass_g":
        if molar_mass_g_per_mol is None:
            raise ValueError("molar_mass_g_per_mol required for mass conversions")
        moles = mass_to_moles(value, molar_mass_g_per_mol)
    else:  # particles
        moles = particles_to_moles(value)

    # Convert moles to target
    if to_type == "moles":
        return moles
    if to_type == "mass_g":
        if molar_mass_g_per_mol is None:
            raise ValueError("molar_mass_g_per_mol required for mass conversions")
        return moles_to_mass(moles, molar_mass_g_per_mol)
    return moles_to_particles(moles)


def dilution_volume(M1: float, M2: float, V2: float) -> float:
    """Calculate V1 needed for dilution: M1*V1 = M2*V2.
    
    Args:
        M1: initial concentration (stock)
        M2: desired final concentration
        V2: desired final volume
    
    Returns:
        V1: volume of stock solution needed
    """
    if M1 <= 0 or M2 <= 0 or V2 <= 0:
        raise ValueError("M1, M2, V2 must all be > 0")
    return (M2 * V2) / M1


def dilution_final_conc(M1: float, V1: float, V2: float) -> float:
    """Calculate final concentration after dilution: M2 = M1*V1/V2."""
    if V2 <= 0:
        raise ValueError("V2 must be > 0")
    return (M1 * V1) / V2


def sigfig_round(value: float, sigfigs: int) -> float:
    if sigfigs <= 0:
        raise ValueError("sigfigs must be >= 1")
    if value == 0:
        return 0.0
    return round(value, sigfigs - int(math.floor(math.log10(abs(value)))) - 1)


if __name__ == "__main__":
    n = mass_to_moles(18.0, 18.015)
    print("moles from 18.0 g H2O:", n)
    print("particles:", moles_to_particles(n))
    print("mass from 3.011e23 molecules H2O:", convert_amount(3.011e23, "particles", "mass_g", 18.015))


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "convert_amount",
        "description": "Generic converter among: mass_g, moles, particles.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "Value"
                },
                "from_type": {
                    "type": "number",
                    "description": "From Type"
                },
                "to_type": {
                    "type": "number",
                    "description": "To Type"
                },
                "molar_mass_g_per_mol": {
                    "type": "number",
                    "description": "Molar Mass G Per Mol",
                    "default": None
                }
            },
            "required": [
                "value",
                "from_type",
                "to_type"
            ]
        }
    },
    {
        "name": "dilution_final_conc",
        "description": "Calculate final concentration after dilution: M2 = M1*V1/V2.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "M1": {
                    "type": "number",
                    "description": "M1"
                },
                "V1": {
                    "type": "number",
                    "description": "V1"
                },
                "V2": {
                    "type": "number",
                    "description": "V2"
                }
            },
            "required": [
                "M1",
                "V1",
                "V2"
            ]
        }
    },
    {
        "name": "dilution_volume",
        "description": "Calculate V1 needed for dilution: M1*V1 = M2*V2.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "M1": {
                    "type": "number",
                    "description": "M1"
                },
                "M2": {
                    "type": "number",
                    "description": "M2"
                },
                "V2": {
                    "type": "number",
                    "description": "V2"
                }
            },
            "required": [
                "M1",
                "M2",
                "V2"
            ]
        }
    },
    {
        "name": "mass_to_moles",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_g": {
                    "type": "number",
                    "description": "Mass G"
                },
                "molar_mass_g_per_mol": {
                    "type": "number",
                    "description": "Molar Mass G Per Mol"
                }
            },
            "required": [
                "mass_g",
                "molar_mass_g_per_mol"
            ]
        }
    },
    {
        "name": "moles_to_mass",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {
                    "type": "number",
                    "description": "Moles"
                },
                "molar_mass_g_per_mol": {
                    "type": "number",
                    "description": "Molar Mass G Per Mol"
                }
            },
            "required": [
                "moles",
                "molar_mass_g_per_mol"
            ]
        }
    },
    {
        "name": "moles_to_particles",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {
                    "type": "number",
                    "description": "Moles"
                }
            },
            "required": [
                "moles"
            ]
        }
    },
    {
        "name": "particles_to_moles",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "particles": {
                    "type": "number",
                    "description": "Particles"
                }
            },
            "required": [
                "particles"
            ]
        }
    },
    {
        "name": "sigfig_round",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "Value"
                },
                "sigfigs": {
                    "type": "number",
                    "description": "Sigfigs"
                }
            },
            "required": [
                "value",
                "sigfigs"
            ]
        }
    }
]