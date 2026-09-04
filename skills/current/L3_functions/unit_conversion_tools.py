"""Chemistry unit conversion tools.

Provides conversion functions for temperature, pressure, energy, volume,
mass, concentration, and length, plus molar mass calculation and ideal gas law solver.

## Solver Instructions (for AI Agent)

When you encounter a unit conversion problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Value and current unit
- Target unit to convert to
- Type of quantity: temperature, pressure, energy, volume, mass, length, concentration
- Molar mass: Needed for concentration conversions involving g/L, ppm, etc.

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Convert temperature | `convert_temperature(value, from_unit, to_unit)` - units: C, K, F |
| Convert pressure | `convert_pressure(value, from_unit, to_unit)` - units: atm, Pa, kPa, bar, mmHg, torr |
| Convert energy | `convert_energy(value, from_unit, to_unit)` - units: J, kJ, cal, kcal, eV, L·atm |
| Convert volume | `convert_volume(value, from_unit, to_unit)` - units: L, mL, m3, cm3, gal, fl_oz |
| Convert mass | `convert_mass(value, from_unit, to_unit)` - units: g, kg, mg, lb, oz, amu |
| Convert length | `convert_length(value, from_unit, to_unit)` - units: m, cm, mm, nm, pm, Å, in |
| Convert concentration | `convert_concentration(value, from_unit, to_unit, molar_mass)` - units: M, mM, muM, g/L, %w/v, ppm, ppb |
| Calculate molar mass from formula | `calculate_molar_mass(formula)` |
| Convert moles to mass | `moles_to_mass(moles, molar_mass)` |
| Convert mass to moles | `mass_to_moles(mass, molar_mass)` |
| Solve ideal gas law | `ideal_gas_law(pressure, volume, moles, temperature, solve_for)` |

### Step 3: Handle special cases
- **Temperature**: K = degC + 273.15; degF = (degC x 9/5) + 32
- **Pressure**: 1 atm = 101.325 kPa = 760 mmHg = 760 torr = 1.01325 bar
- **Energy**: 1 cal = 4.184 J; 1 eV = 1.602 x 10-19 J
- **Volume**: 1 L = 1000 mL = 0.001 m3 = 1000 cm3
- **Concentration**: Need molar mass for M ↔ g/L, ppm, ppb conversions
- **Molar mass**: Parse formula like "H2O", "Ca(OH)2", "C6H12O6"

### Examples

**Example 1: Temperature conversion**
Question: "Convert 25degC to Kelvin."
- Solution: `convert_temperature(value=25, from_unit='C', to_unit='K')` -> 298.15 K

**Example 2: Pressure conversion**
Question: "Convert 1.5 atm to kPa."
- Solution: `convert_pressure(value=1.5, from_unit='atm', to_unit='kPa')` -> 151.99 kPa

**Example 3: Molar mass calculation**
Question: "Calculate the molar mass of H2SO4."
- Solution: `calculate_molar_mass(formula='H2SO4')` -> 98.08 g/mol

**Example 4: Mass to moles**
Question: "How many moles are in 58.44 g of NaCl (M = 58.44 g/mol)?"
- Solution: `mass_to_moles(mass=58.44, molar_mass=58.44)` -> 1.0 mol

**Example 5: Concentration conversion**
Question: "Convert 58.44 g/L NaCl to molarity (M = 58.44 g/mol)."
- Solution: `convert_concentration(value=58.44, from_unit='g/L', to_unit='M', molar_mass=58.44)` -> 1.0 M
"""

from __future__ import annotations

import re
from typing import Optional

# ── Periodic table (subset for molar mass) ──────────────────────────────────

ATOMIC_MASSES: dict[str, float] = {
    "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974,
    "S": 32.065, "Cl": 35.453, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.380,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Ru": 101.07, "Rh": 102.91, "Pd": 106.42,
    "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71, "Sb": 121.76,
    "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91, "Ba": 137.33,
    "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24, "Sm": 150.36,
    "Eu": 151.96, "Gd": 157.25, "Tb": 158.93, "Dy": 162.50, "Ho": 164.93,
    "Er": 167.26, "Tm": 168.93, "Yb": 173.05, "Lu": 174.97, "Hf": 178.49,
    "Ta": 180.95, "W": 183.84, "Re": 186.21, "Os": 190.23, "Ir": 192.22,
    "Pt": 195.08, "Au": 196.97, "Hg": 200.59, "Tl": 204.38, "Pb": 207.2,
    "Bi": 208.98, "Th": 232.04, "Pa": 231.04, "U": 238.03,
}

# ── Conversion tables (all in terms of SI base) ────────────────────────────

PRESSURE_SI: dict[str, float] = {
    "Pa": 1.0, "kPa": 1e3, "atm": 101325.0,
    "bar": 1e5, "mmHg": 133.322, "torr": 133.322,
}

ENERGY_SI: dict[str, float] = {
    "J": 1.0, "kJ": 1e3, "cal": 4.184, "kcal": 4184.0,
    "eV": 1.602176634e-19, "L·atm": 101.325,
}

VOLUME_L: dict[str, float] = {
    "L": 1.0, "mL": 1e-3, "m3": 1e3, "cm3": 1e-3,
    "gal": 3.78541, "fl_oz": 0.0295735,
}

MASS_G: dict[str, float] = {
    "g": 1.0, "kg": 1e3, "mg": 1e-3, "lb": 453.592,
    "oz": 28.3495, "amu": 1.66053906660e-24,
}

LENGTH_M: dict[str, float] = {
    "m": 1.0, "cm": 0.01, "mm": 0.001, "nm": 1e-9,
    "pm": 1e-12, "Å": 1e-10, "in": 0.0254, "ft": 0.3048,
}

# Concentration: M as base. For g/L and %w/v/ppm/ppb we need molar mass -> None here handled specially.
CONC_M: dict[str, float] = {
    "M": 1.0, "mM": 1e-3, "muM": 1e-6,
}


# ── Temperature ─────────────────────────────────────────────────────────────

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between C, K, F."""
    fu, tu = from_unit.strip(), to_unit.strip()
    if fu == tu:
        return value
    # to Kelvin first
    if fu == "C":
        k = value + 273.15
    elif fu == "F":
        k = (value - 32) * 5 / 9 + 273.15
    elif fu == "K":
        k = value
    else:
        raise ValueError(f"Invalid temperature unit: {fu}. Use C, K, or F.")
    if tu == "K":
        return k
    elif tu == "C":
        return k - 273.15
    elif tu == "F":
        return (k - 273.15) * 9 / 5 + 32
    else:
        raise ValueError(f"Invalid temperature unit: {tu}. Use C, K, or F.")


# ── Generic linear conversion helper ────────────────────────────────────────

def _linear_convert(value: float, from_unit: str, to_unit: str, table: dict[str, float], name: str) -> float:
    fu, tu = from_unit.strip(), to_unit.strip()
    if fu == tu:
        return value
    if fu not in table:
        raise ValueError(f"Invalid {name} unit: {fu}. Use {', '.join(table)}")
    if tu not in table:
        raise ValueError(f"Invalid {name} unit: {tu}. Use {', '.join(table)}")
    return value * table[fu] / table[tu]


def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
    """Convert pressure between atm, Pa, kPa, bar, mmHg, torr."""
    return _linear_convert(value, from_unit, to_unit, PRESSURE_SI, "pressure")


def convert_energy(value: float, from_unit: str, to_unit: str) -> float:
    """Convert energy between J, kJ, cal, kcal, eV, L·atm."""
    return _linear_convert(value, from_unit, to_unit, ENERGY_SI, "energy")


def convert_volume(value: float, from_unit: str, to_unit: str) -> float:
    """Convert volume between L, mL, m3, cm3, gal, fl_oz."""
    return _linear_convert(value, from_unit, to_unit, VOLUME_L, "volume")


def convert_mass(value: float, from_unit: str, to_unit: str) -> float:
    """Convert mass between g, kg, mg, lb, oz, amu."""
    return _linear_convert(value, from_unit, to_unit, MASS_G, "mass")


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert length between m, cm, mm, nm, pm, Å, in."""
    return _linear_convert(value, from_unit, to_unit, LENGTH_M, "length")


# ── Concentration (needs molar mass for g/L ↔ M) ───────────────────────────

def convert_concentration(value: float, from_unit: str, to_unit: str,
                          molar_mass: Optional[float] = None) -> float:
    """Convert concentration between M, mM, muM, g/L, %w/v, ppm, ppb.

    Conversions involving g/L, %w/v, ppm, or ppb require *molar_mass* (g/mol).
    """
    fu, tu = from_unit.strip(), to_unit.strip()
    if fu == tu:
        return value

    mass_units = {"g/L", "%w/v", "ppm", "ppb"}
    needs_mm = (fu in mass_units) != (tu in mass_units)

    if needs_mm:
        if molar_mass is None:
            raise ValueError(
                f"Converting {fu} ↔ {tu} requires molar_mass (g/mol)."
            )
        if molar_mass <= 0:
            raise ValueError("molar_mass must be positive.")

    # Normalize to M (mol/L)
    if fu in CONC_M:
        molar = value * CONC_M[fu]
    elif fu == "g/L":
        molar = value / molar_mass  # type: ignore[arg-type]
    elif fu == "%w/v":
        molar = (value / 100 * 1000) / molar_mass  # type: ignore[arg-type]
    elif fu == "ppm":
        molar = (value / 1e6 * 1000) / molar_mass  # type: ignore[arg-type]
    elif fu == "ppb":
        molar = (value / 1e9 * 1000) / molar_mass  # type: ignore[arg-type]
    else:
        raise ValueError(f"Invalid concentration unit: {fu}")

    # Convert from M to target
    if tu in CONC_M:
        return molar / CONC_M[tu]
    elif tu == "g/L":
        return molar * molar_mass  # type: ignore[operator]
    elif tu == "%w/v":
        return molar * molar_mass / 10  # type: ignore[operator]
    elif tu == "ppm":
        return molar * molar_mass / 1e3  # type: ignore[operator]
    elif tu == "ppb":
        return molar * molar_mass / 1e6  # type: ignore[operator]
    else:
        raise ValueError(f"Invalid concentration unit: {tu}")


# ── Molar mass ──────────────────────────────────────────────────────────────

def calculate_molar_mass(formula: str) -> float:
    """Calculate molar mass (g/mol) from a chemical formula (e.g. 'H2O', 'C6H12O6', 'Ca(OH)2')."""
    pattern = r"([A-Z][a-z]?)(\d*)|\(([^)]+)\)(\d*)"
    tokens: list[tuple[str, int]] = []
    i = 0
    while i < len(formula):
        m = re.match(r"([A-Z][a-z]?)(\d*)", formula[i:])
        if m:
            elem, num = m.group(1), m.group(2)
            tokens.append((elem, int(num) if num else 1))
            i += m.end()
        elif formula[i] == "(":
            # find matching )
            depth = 1
            j = i + 1
            while j < len(formula) and depth > 0:
                if formula[j] == "(":
                    depth += 1
                elif formula[j] == ")":
                    depth -= 1
                j += 1
            sub = formula[i + 1 : j - 1]
            # read multiplier
            km = re.match(r"(\d*)", formula[j:])
            mult = int(km.group(1)) if km.group(1) else 1
            sub_tokens = _parse_tokens(sub)
            for elem, cnt in sub_tokens:
                tokens.append((elem, cnt * mult))
            i = j + (len(km.group(1)) if km.group(1) else 0)
        else:
            raise ValueError(f"Cannot parse formula at position {i}: {formula}")
    total = 0.0
    for elem, cnt in tokens:
        if elem not in ATOMIC_MASSES:
            raise ValueError(f"Unknown element: {elem}")
        total += ATOMIC_MASSES[elem] * cnt
    return total


def _parse_tokens(formula: str) -> list[tuple[str, int]]:
    """Helper to parse formula into (element, count) tokens (no parentheses)."""
    tokens: list[tuple[str, int]] = []
    i = 0
    while i < len(formula):
        m = re.match(r"([A-Z][a-z]?)(\d*)", formula[i:])
        if m:
            elem, num = m.group(1), m.group(2)
            tokens.append((elem, int(num) if num else 1))
            i += m.end()
        else:
            raise ValueError(f"Cannot parse: {formula}")
    return tokens


# ── Mass ↔ moles ────────────────────────────────────────────────────────────

def moles_to_mass(moles: float, molar_mass: float) -> float:
    """Convert moles to mass (g)."""
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive.")
    return moles * molar_mass


def mass_to_moles(mass: float, molar_mass: float) -> float:
    """Convert mass (g) to moles."""
    if molar_mass <= 0:
        raise ValueError("molar_mass must be positive.")
    return mass / molar_mass


# ── Ideal gas law ───────────────────────────────────────────────────────────

R = 0.082057  # L·atm/(mol·K)


def ideal_gas_law(pressure: Optional[float] = None, volume: Optional[float] = None,
                  moles: Optional[float] = None, temperature: Optional[float] = None,
                  solve_for: str = "unknown") -> float:
    """Solve PV = nRT for the unknown variable.

    Pass None for the variable to solve for, or set solve_for to 'P', 'V', 'n', or 'T'.
    Units: P in atm, V in L, n in mol, T in K.
    """
    solve_for = solve_for.strip().lower()
    knowns = sum(1 for x in (pressure, volume, moles, temperature) if x is not None)
    if knowns != 3:
        raise ValueError("Exactly 3 of pressure, volume, moles, temperature must be provided.")

    # Determine which is None
    if solve_for in ("p", "pressure"):
        if volume is None or moles is None or temperature is None:
            raise ValueError("volume, moles, and temperature must be provided to solve for P.")
        if temperature == 0:
            raise ValueError("Temperature cannot be zero.")
        return moles * R * temperature / volume
    elif solve_for in ("v", "volume"):
        if pressure is None or moles is None or temperature is None:
            raise ValueError("pressure, moles, and temperature must be provided to solve for V.")
        if pressure == 0:
            raise ValueError("Pressure cannot be zero.")
        return moles * R * temperature / pressure
    elif solve_for in ("n", "moles"):
        if pressure is None or volume is None or temperature is None:
            raise ValueError("pressure, volume, and temperature must be provided to solve for n.")
        if temperature == 0:
            raise ValueError("Temperature cannot be zero.")
        return pressure * volume / (R * temperature)
    elif solve_for in ("t", "temperature"):
        if pressure is None or volume is None or moles is None:
            raise ValueError("pressure, volume, and moles must be provided to solve for T.")
        if moles == 0:
            raise ValueError("Moles cannot be zero.")
        return pressure * volume / (R * moles)
    else:
        raise ValueError(f"solve_for must be P, V, n, or T; got '{solve_for}'")


# ── Tests ───────────────────────────────────────────────────────────────────

def test_convert_temperature():
    assert abs(convert_temperature(0, "C", "K") - 273.15) < 1e-10
    assert abs(convert_temperature(100, "C", "F") - 212.0) < 1e-10
    assert abs(convert_temperature(32, "F", "C") - 0.0) < 1e-10
    assert abs(convert_temperature(0, "K", "C") + 273.15) < 1e-10


def test_convert_pressure():
    assert abs(convert_pressure(1, "atm", "Pa") - 101325.0) < 1e-2
    assert abs(convert_pressure(760, "torr", "atm") - 1.0) < 1e-3
    assert abs(convert_pressure(1, "bar", "kPa") - 100.0) < 1e-6


def test_convert_energy():
    assert abs(convert_energy(1, "cal", "J") - 4.184) < 1e-6
    assert abs(convert_energy(1, "kJ", "J") - 1000.0) < 1e-6
    assert abs(convert_energy(1, "L·atm", "J") - 101.325) < 1e-3


def test_convert_volume():
    assert abs(convert_volume(1, "L", "mL") - 1000.0) < 1e-6
    assert abs(convert_volume(1, "m3", "L") - 1000.0) < 1e-6


def test_convert_mass():
    assert abs(convert_mass(1, "kg", "g") - 1000.0) < 1e-6
    assert abs(convert_mass(1, "lb", "g") - 453.592) < 1e-3


def test_convert_length():
    assert abs(convert_length(1, "nm", "m") - 1e-9) < 1e-15
    assert abs(convert_length(1, "Å", "pm") - 100.0) < 1e-6
    assert abs(convert_length(1, "in", "cm") - 2.54) < 1e-6


def test_convert_concentration():
    assert abs(convert_concentration(1, "M", "mM") - 1000.0) < 1e-6
    assert abs(convert_concentration(58.44, "g/L", "M", molar_mass=58.44) - 1.0) < 1e-6
    assert abs(convert_concentration(1, "M", "g/L", molar_mass=58.44) - 58.44) < 1e-3


def test_calculate_molar_mass():
    assert abs(calculate_molar_mass("H2O") - 18.015) < 0.01
    assert abs(calculate_molar_mass("C6H12O6") - 180.156) < 0.01
    assert abs(calculate_molar_mass("NaCl") - 58.44) < 0.01
    assert abs(calculate_molar_mass("Ca(OH)2") - 74.09) < 0.01


def test_moles_mass():
    assert abs(moles_to_mass(1.0, 18.015) - 18.015) < 1e-6
    assert abs(mass_to_moles(18.015, 18.015) - 1.0) < 1e-6


def test_ideal_gas_law():
    # STP: 1 atm, 22.414 L, 1 mol, 273.15 K
    v = ideal_gas_law(pressure=1.0, moles=1.0, temperature=273.15, solve_for="V")
    assert abs(v - 22.414) < 0.01
    t = ideal_gas_law(pressure=1.0, volume=22.414, moles=1.0, solve_for="T")
    assert abs(t - 273.15) < 0.1


def test_invalid_units():
    import pytest
    with pytest.raises(ValueError):
        convert_temperature(0, "X", "C")
    with pytest.raises(ValueError):
        convert_pressure(1, "psi", "atm")


def test_zero_division():
    import pytest
    with pytest.raises(ValueError):
        mass_to_moles(1.0, 0.0)
    with pytest.raises(ValueError):
        ideal_gas_law(pressure=1, volume=1, moles=1, temperature=0, solve_for="V")


# ── Main demo ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Unit Conversion Tools Demo ===")
    print(f"0degC -> {convert_temperature(0, 'C', 'F')}degF")
    print(f"1 atm -> {convert_pressure(1, 'atm', 'kPa'):.1f} kPa")
    print(f"1 kcal -> {convert_energy(1, 'kcal', 'kJ'):.3f} kJ")
    print(f"1 gal -> {convert_volume(1, 'gal', 'mL'):.1f} mL")
    print(f"1 lb -> {convert_mass(1, 'lb', 'g'):.2f} g")
    print(f"1 nm -> {convert_length(1, 'nm', 'Å'):.2f} Å")
    print(f"Molar mass H2SO4: {calculate_molar_mass('H2SO4'):.3f} g/mol")
    print(f"Molar mass Ca(OH)2: {calculate_molar_mass('Ca(OH)2'):.3f} g/mol")
    print(f"2 mol NaCl -> {moles_to_mass(2, 58.44):.2f} g")
    print(f"58.44 g NaCl -> {mass_to_moles(58.44, 58.44):.4f} mol")
    print(f"Ideal gas V at STP: {ideal_gas_law(1, None, 1, 273.15, 'V'):.3f} L")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="calculate_molar_mass",
            description="Calculate molar mass (g/mol) from a chemical formula (e.g. 'H2O', 'C6H12O6', 'Ca(OH)2').",
            input_schema=[
            InputSchemaField(name="formula", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_concentration",
            description="Convert concentration between M, mM, muM, g/L, %w/v, ppm, ppb.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_energy",
            description="Convert energy between J, kJ, cal, kcal, eV, L·atm.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_length",
            description="Convert length between m, cm, mm, nm, pm, Å, in.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_mass",
            description="Convert mass between g, kg, mg, lb, oz, amu.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_pressure",
            description="Convert pressure between atm, Pa, kPa, bar, mmHg, torr.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_temperature",
            description="Convert temperature between C, K, F.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="convert_volume",
            description="Convert volume between L, mL, m3, cm3, gal, fl_oz.",
            input_schema=[
            InputSchemaField(name="value", type="number", required=True),
            InputSchemaField(name="from_unit", type="number", required=True),
            InputSchemaField(name="to_unit", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ideal_gas_law",
            description="Solve PV = nRT for the unknown variable.",
            input_schema=[
            InputSchemaField(name="pressure", type="number", required=False),
            InputSchemaField(name="volume", type="number", required=False),
            InputSchemaField(name="moles", type="number", required=False),
            InputSchemaField(name="temperature", type="number", required=False),
            InputSchemaField(name="solve_for", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mass_to_moles",
            description="Convert mass (g) to moles.",
            input_schema=[
            InputSchemaField(name="mass", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="moles_to_mass",
            description="Convert moles to mass (g).",
            input_schema=[
            InputSchemaField(name="moles", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_calculate_molar_mass",
            description="Compute test_calculate_molar_mass",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_concentration",
            description="Compute test_convert_concentration",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_energy",
            description="Compute test_convert_energy",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_length",
            description="Compute test_convert_length",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_mass",
            description="Compute test_convert_mass",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_pressure",
            description="Compute test_convert_pressure",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_temperature",
            description="Compute test_convert_temperature",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_convert_volume",
            description="Compute test_convert_volume",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_ideal_gas_law",
            description="Compute test_ideal_gas_law",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_invalid_units",
            description="Compute test_invalid_units",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_moles_mass",
            description="Compute test_moles_mass",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_zero_division",
            description="Compute test_zero_division",
            input_schema=[

            ],
            handler="{name}",
        )
    ]
