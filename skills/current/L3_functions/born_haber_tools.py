"""
Born-Haber Cycle Calculation Tools

Calculates thermodynamic cycles for ionic compound formation,
including lattice energy and formation enthalpy.

## Solver Instructions (for AI Agent)

When you encounter Born-Haber cycle problems for ionic compound formation:

### Step 1: Identify what is given and what is asked
- Given: some of DeltaH_f, IE, EA, sublimation energy, dissociation energy, lattice energy
- Asked: the missing thermodynamic value

### Step 2: Choose the correct function
- `calculate_born_haber_cycle(data)`: Full cycle with all values
- `calculate_lattice_energy(data)`: Find U from other components
- `calculate_formation_enthalpy(data)`: Find DeltaH_f from U and other components

### Step 3: Handle special cases
- Cycle: DeltaH_f = DeltaH_sub + IE + ½DeltaH_diss + EA + U
- Rearrange: U = DeltaH_f - DeltaH_sub - IE - ½DeltaH_diss - EA
- For multivalent metals: sum all ionization energies
- bond_dissociation_energy is the FULL X₂ BDE; functions automatically use BDE/2

### Examples
```python
calculate_lattice_energy({
    'delta_H_f': -411, 'delta_H_sub_Na': 108, 'IE_Na': 496,
    'bond_diss_Cl2': 242, 'EA_Cl': -349
})  # -> U ~ -787 kJ/mol
```
"""

from typing import Optional


# Common thermodynamic data for Born-Haber cycles (kJ/mol, 298 K)
BORN_HABER_DATA = {
    "NaCl": {
        "sublimation_energy": 107.0,       # Na(s) -> Na(g)
        "ionization_energies": [496.0],     # Na(g) -> Na+(g) + e-
        "bond_dissociation_energy": 242.0,  # Cl2(g) -> 2Cl(g) full BDE
        "electron_affinities": [-349.0],    # Cl(g) + e- -> Cl-(g)
        "lattice_energy": -788.0,           # Na+(g) + Cl-(g) -> NaCl(s)
        "formation_enthalpy": -411.0,       # Na(s) + ½Cl2(g) -> NaCl(s)
    },
    "MgO": {
        "sublimation_energy": 147.1,        # Mg(s) -> Mg(g)
        "ionization_energies": [738.0, 1451.0],  # Mg(g) -> Mg2+(g) + 2e-
        "bond_dissociation_energy": 498.0,   # O2(g) -> 2O(g) full BDE
        "electron_affinities": [-141.0, 744.0],  # O(g) + 2e- -> O2-(g) (EA + 2nd EA)
        "lattice_energy": -3791.0,
        "formation_enthalpy": -601.6,
    },
    "CaO": {
        "sublimation_energy": 178.2,
        "ionization_energies": [590.0, 1145.0],
        "bond_dissociation_energy": 498.0,
        "electron_affinities": [-141.0, 744.0],
        "lattice_energy": -3414.0,
        "formation_enthalpy": -635.5,
    },
    "Al2O3": {
        "sublimation_energy": 330.0,
        "ionization_energies": [578.0, 1817.0, 2745.0],
        "bond_dissociation_energy": 498.0,
        "electron_affinities": [-141.0, 744.0],
        "lattice_energy": -15916.0,
        "formation_enthalpy": -1675.7,
    },
    "KCl": {
        "sublimation_energy": 89.0,
        "ionization_energies": [419.0],
        "bond_dissociation_energy": 242.0,
        "electron_affinities": [-349.0],
        "lattice_energy": -715.0,
        "formation_enthalpy": -436.5,
    },
    "NaF": {
        "sublimation_energy": 107.0,
        "ionization_energies": [496.0],
        "bond_dissociation_energy": 158.0,  # F2(g) -> 2F(g) full BDE
        "electron_affinities": [-328.0],
        "lattice_energy": -910.0,
        "formation_enthalpy": -573.6,
    },
    "MgCl2": {
        "sublimation_energy": 147.1,
        "ionization_energies": [738.0, 1451.0],
        "bond_dissociation_energy": 242.0,
        "electron_affinities": [-349.0],
        "lattice_energy": -2526.0,
        "formation_enthalpy": -641.3,
    },
    "CaF2": {
        "sublimation_energy": 178.2,
        "ionization_energies": [590.0, 1145.0],
        "bond_dissociation_energy": 158.0,
        "electron_affinities": [-328.0],
        "lattice_energy": -2630.0,
        "formation_enthalpy": -1219.6,
    },
    "LiF": {
        "sublimation_energy": 159.3,
        "ionization_energies": [520.0],
        "bond_dissociation_energy": 158.0,
        "electron_affinities": [-328.0],
        "lattice_energy": -1036.0,
        "formation_enthalpy": -617.0,
    },
    "KF": {
        "sublimation_energy": 89.0,
        "ionization_energies": [419.0],
        "bond_dissociation_energy": 158.0,
        "electron_affinities": [-328.0],
        "lattice_energy": -808.0,
        "formation_enthalpy": -568.0,
    },
}


def calculate_born_haber_cycle(
    compound: str,
    ionization_energies: list[float],
    electron_affinities: list[float],
    sublimation_energy: Optional[float] = None,
    bond_dissociation_energy: Optional[float] = None,
    atomization_energy: Optional[float] = None,
    lattice_energy: Optional[float] = None,
    formation_enthalpy: Optional[float] = None,
) -> dict:
    """Calculate a full Born-Haber cycle for an ionic compound.

    Args:
        compound: Chemical formula (e.g., "NaCl")
        ionization_energies: List of IE values (kJ/mol) for the metal
        electron_affinities: List of EA values (kJ/mol); typically negative
        sublimation_energy: Metal sublimation DeltaH (kJ/mol)
        bond_dissociation_energy: Full X₂ bond dissociation energy (kJ/mol), e.g., Cl₂→2Cl = 242. Function uses BDE/2.
        atomization_energy: Alternative to sublimation+BDE (kJ/mol)
        lattice_energy: Lattice energy (kJ/mol), negative by convention
        formation_enthalpy: Standard formation enthalpy (kJ/mol)

    Returns:
        dict with all cycle steps and the computed missing value.
    """
    # Try to fill missing values from built-in data
    data = BORN_HABER_DATA.get(compound, {})
    if sublimation_energy is None:
        sublimation_energy = data.get("sublimation_energy")
    if bond_dissociation_energy is None:
        bond_dissociation_energy = data.get("bond_dissociation_energy")
    if lattice_energy is None:
        lattice_energy = data.get("lattice_energy")
    if formation_enthalpy is None:
        formation_enthalpy = data.get("formation_enthalpy")

    total_ie = sum(ionization_energies)
    total_ea = sum(electron_affinities)

    # atomization = sublimation + BDE/2 (per formula unit: X₂ → 2X, one atom per formula unit)
    if atomization_energy is None:
        bde_per_atom = (bond_dissociation_energy or 0) / 2
        atomization_energy = (sublimation_energy or 0) + bde_per_atom

    result = {
        "compound": compound,
        "sublimation_energy": sublimation_energy,
        "bond_dissociation_energy": bond_dissociation_energy,
        "atomization_energy": atomization_energy,
        "total_ionization_energy": total_ie,
        "ionization_energies": ionization_energies,
        "total_electron_affinity": total_ea,
        "electron_affinities": electron_affinities,
        "lattice_energy": lattice_energy,
        "formation_enthalpy": formation_enthalpy,
    }

    # Born-Haber cycle: DeltaHf = DeltaHsub + IE + BDE + EA + DeltaHlatt
    # (all signs follow thermochemical convention)
    known_sum = atomization_energy + total_ie + total_ea
    if lattice_energy is not None and formation_enthalpy is None:
        formation_enthalpy = known_sum + lattice_energy
        result["formation_enthalpy"] = formation_enthalpy
        result["computed"] = "formation_enthalpy"
    elif formation_enthalpy is not None and lattice_energy is None:
        lattice_energy = formation_enthalpy - known_sum
        result["lattice_energy"] = lattice_energy
        result["computed"] = "lattice_energy"
    else:
        result["computed"] = "none"

    return result


def calculate_lattice_energy(
    compound: str,
    ionization_energies: list[float],
    electron_affinities: list[float],
    sublimation_energy: Optional[float] = None,
    bond_dissociation_energy: Optional[float] = None,
    formation_enthalpy: Optional[float] = None,
) -> float:
    """Derive lattice energy from the Born-Haber cycle.

    Returns:
        Lattice energy in kJ/mol.
    """
    data = BORN_HABER_DATA.get(compound, {})
    if sublimation_energy is None:
        sublimation_energy = data.get("sublimation_energy", 0)
    if bond_dissociation_energy is None:
        bond_dissociation_energy = data.get("bond_dissociation_energy", 0)
    if formation_enthalpy is None:
        formation_enthalpy = data.get("formation_enthalpy")

    atomization = sublimation_energy + bond_dissociation_energy / 2
    known_sum = atomization + sum(ionization_energies) + sum(electron_affinities)
    return formation_enthalpy - known_sum


def calculate_formation_enthalpy(
    compound: str,
    ionization_energies: list[float],
    electron_affinities: list[float],
    lattice_energy: float,
    sublimation_energy: Optional[float] = None,
    bond_dissociation_energy: Optional[float] = None,
) -> float:
    """Derive formation enthalpy from the Born-Haber cycle.

    Returns:
        Formation enthalpy in kJ/mol.
    """
    data = BORN_HABER_DATA.get(compound, {})
    if sublimation_energy is None:
        sublimation_energy = data.get("sublimation_energy", 0)
    if bond_dissociation_energy is None:
        bond_dissociation_energy = data.get("bond_dissociation_energy", 0)

    atomization = sublimation_energy + bond_dissociation_energy / 2
    return atomization + sum(ionization_energies) + sum(electron_affinities) + lattice_energy


# --- pytest-compatible tests ---

def test_nacl_lattice_energy():
    data = BORN_HABER_DATA["NaCl"]
    result = calculate_born_haber_cycle(
        "NaCl", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        formation_enthalpy=data["formation_enthalpy"],
    )
    assert abs(result["lattice_energy"] - (-788.0)) < 1.0


def test_mgo_formation_enthalpy():
    data = BORN_HABER_DATA["MgO"]
    result = calculate_born_haber_cycle(
        "MgO", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        lattice_energy=data["lattice_energy"],
    )
    assert abs(result["formation_enthalpy"] - (-601.6)) < 2.0


def test_known_compound_data():
    for compound in ["NaCl", "KCl", "MgO", "CaO", "LiF"]:
        data = BORN_HABER_DATA[compound]
        result = calculate_born_haber_cycle(
            compound,
            ionization_energies=data["ionization_energies"],
            electron_affinities=data["electron_affinities"],
        )
        assert result["compound"] == compound
        assert result["computed"] == "none"  # all values provided from data


def test_calculate_lattice_energy():
    data = BORN_HABER_DATA["NaCl"]
    le = calculate_lattice_energy(
        "NaCl", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        formation_enthalpy=data["formation_enthalpy"],
    )
    assert abs(le - (-788.0)) < 1.0


def test_calculate_formation_enthalpy():
    data = BORN_HABER_DATA["NaCl"]
    fh = calculate_formation_enthalpy(
        "NaCl", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        lattice_energy=data["lattice_energy"],
    )
    assert abs(fh - (-411.0)) < 1.0


if __name__ == "__main__":
    # Example 1: NaCl full cycle
    data = BORN_HABER_DATA["NaCl"]
    result = calculate_born_haber_cycle(
        "NaCl", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
    )
    print(f"\n=== {result['compound']} Born-Haber Cycle ===")
    for k, v in result.items():
        if k not in ("ionization_energies", "electron_affinities", "compound"):
            print(f"  {k}: {v}")
    print()

    # Example 2: MgO - derive lattice energy
    data = BORN_HABER_DATA["MgO"]
    le = calculate_lattice_energy(
        "MgO", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        formation_enthalpy=data["formation_enthalpy"],
    )
    print(f"MgO lattice energy: {le:.1f} kJ/mol (expected {data['lattice_energy']})")

    # Example 3: CaO - derive formation enthalpy
    data = BORN_HABER_DATA["CaO"]
    fh = calculate_formation_enthalpy(
        "CaO", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        lattice_energy=data["lattice_energy"],
    )
    print(f"CaO formation enthalpy: {fh:.1f} kJ/mol (expected {data['formation_enthalpy']})")

    # Example 4: Al2O3 full cycle
    data = BORN_HABER_DATA["Al2O3"]
    result = calculate_born_haber_cycle(
        "Al2O3", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
    )
    print(f"\n=== {result['compound']} Born-Haber Cycle ===")
    for k, v in result.items():
        if k not in ("ionization_energies", "electron_affinities", "compound"):
            print(f"  {k}: {v}")

    # Example 5: KCl - derive formation enthalpy
    data = BORN_HABER_DATA["KCl"]
    fh = calculate_formation_enthalpy(
        "KCl", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
        lattice_energy=data["lattice_energy"],
    )
    print(f"\nKCl formation enthalpy: {fh:.1f} kJ/mol (expected {data['formation_enthalpy']})")

    # Example 6: NaF
    data = BORN_HABER_DATA["NaF"]
    result = calculate_born_haber_cycle(
        "NaF", ionization_energies=data["ionization_energies"],
        electron_affinities=data["electron_affinities"],
    )
    print(f"\n=== {result['compound']} Born-Haber Cycle ===")
    print(f"  Formation enthalpy: {result['formation_enthalpy']} kJ/mol")
    print(f"  Lattice energy: {result['lattice_energy']} kJ/mol")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calculate_born_haber_cycle",
        "description": "Calculate a full Born-Haber cycle for an ionic compound.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compound": {
                    "type": "number",
                    "description": "Compound"
                },
                "ionization_energies": {
                    "type": "number",
                    "description": "Ionization Energies"
                },
                "electron_affinities": {
                    "type": "number",
                    "description": "Electron Affinities"
                },
                "sublimation_energy": {
                    "type": "number",
                    "description": "Sublimation Energy",
                    "default": None
                },
                "bond_dissociation_energy": {
                    "type": "number",
                    "description": "Bond Dissociation Energy",
                    "default": None
                },
                "atomization_energy": {
                    "type": "number",
                    "description": "Atomization Energy",
                    "default": None
                },
                "lattice_energy": {
                    "type": "number",
                    "description": "Lattice Energy",
                    "default": None
                },
                "formation_enthalpy": {
                    "type": "number",
                    "description": "Formation Enthalpy",
                    "default": None
                }
            },
            "required": [
                "compound",
                "ionization_energies",
                "electron_affinities"
            ]
        }
    },
    {
        "name": "calculate_formation_enthalpy",
        "description": "Derive formation enthalpy from the Born-Haber cycle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compound": {
                    "type": "number",
                    "description": "Compound"
                },
                "ionization_energies": {
                    "type": "number",
                    "description": "Ionization Energies"
                },
                "electron_affinities": {
                    "type": "number",
                    "description": "Electron Affinities"
                },
                "lattice_energy": {
                    "type": "number",
                    "description": "Lattice Energy"
                },
                "sublimation_energy": {
                    "type": "number",
                    "description": "Sublimation Energy",
                    "default": None
                },
                "bond_dissociation_energy": {
                    "type": "number",
                    "description": "Bond Dissociation Energy",
                    "default": None
                }
            },
            "required": [
                "compound",
                "ionization_energies",
                "electron_affinities",
                "lattice_energy"
            ]
        }
    },
    {
        "name": "calculate_lattice_energy",
        "description": "Derive lattice energy from the Born-Haber cycle.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compound": {
                    "type": "number",
                    "description": "Compound"
                },
                "ionization_energies": {
                    "type": "number",
                    "description": "Ionization Energies"
                },
                "electron_affinities": {
                    "type": "number",
                    "description": "Electron Affinities"
                },
                "sublimation_energy": {
                    "type": "number",
                    "description": "Sublimation Energy",
                    "default": None
                },
                "bond_dissociation_energy": {
                    "type": "number",
                    "description": "Bond Dissociation Energy",
                    "default": None
                },
                "formation_enthalpy": {
                    "type": "number",
                    "description": "Formation Enthalpy",
                    "default": None
                }
            },
            "required": [
                "compound",
                "ionization_energies",
                "electron_affinities"
            ]
        }
    },
    {
        "name": "test_calculate_formation_enthalpy",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_calculate_lattice_energy",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_known_compound_data",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_mgo_formation_enthalpy",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "test_nacl_lattice_energy",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]