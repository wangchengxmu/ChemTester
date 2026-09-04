"""
Thermodynamic Data Lookup Tools

Standard thermodynamic properties for ~100 common species,
plus Hess's law calculations for reactions.
"""

## Solver Instructions (for AI Agent)

# When you encounter **thermodynamic data lookup and Hess's law** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Need standard enthalpy/entropy/Gibbs/heat capacity of a species: `lookup_formation_enthalpy(species)`, `lookup_formation_gibbs(species)`, `lookup_standard_entropy(species)`, `lookup_heat_capacity(species)`
# - Need reaction thermodynamics from formation data: `calculate_hess_law(...)`, `calculate_reaction_entropy(...)`, `calculate_reaction_gibbs(...)`

### Step 2: Choose the correct function
# - Single species property: use the appropriate `lookup_*` function
# - Reaction property from formation data: use `calculate_hess_law`, `calculate_reaction_entropy`, or `calculate_reaction_gibbs`
# - All three functions accept reactants (list of tuples) and products (list of tuples)

### Step 3: Handle special cases
# - Species names must match the database (use standard chemical formulas)
# - `_lookup` is internal; use the public `lookup_*` functions
# - Stoichiometric coefficients are signed: negative for reactants in the internal calculation

### Examples
# 1. Enthalpy of formation of H2O(g): `lookup_formation_enthalpy("H2O(g)")` -> -241.8 kJ/mol
# 2. DeltaH for CH4 + 2O2 -> CO2 + 2H2O: `calculate_hess_law(reactants=[("CH4(g)",1),("O2(g)",2)], products=[("CO2(g)",1),("H2O(l)",2)])`
# 3. Standard entropy of CO2(g): `lookup_standard_entropy("CO2(g)")` -> 213.7 J/(mol·K)



from typing import Union


# Standard thermodynamic data at 298.15 K, 1 bar
# Format: species -> (DeltaHdegf kJ/mol, DeltaGdegf kJ/mol, Sdeg J/(mol·K), Cp J/(mol·K))
# Elements in reference state: DeltaHdegf = DeltaGdegf = 0
_THERMO_DATA: dict[str, tuple[float, float, float, float]] = {
    # --- Elements (reference state) ---
    "H2(g)": (0.0, 0.0, 130.7, 28.8),
    "N2(g)": (0.0, 0.0, 191.6, 29.1),
    "O2(g)": (0.0, 0.0, 205.2, 29.4),
    "F2(g)": (0.0, 0.0, 202.8, 31.3),
    "Cl2(g)": (0.0, 0.0, 223.1, 33.9),
    "Br2(l)": (0.0, 0.0, 152.2, 75.7),
    "I2(s)": (0.0, 0.0, 116.1, 54.4),
    "C(s,graphite)": (0.0, 0.0, 5.7, 8.5),
    "S(s,rhombic)": (0.0, 0.0, 31.8, 22.6),
    "P4(s,white)": (0.0, 0.0, 164.4, 100.0),
    "Na(s)": (0.0, 0.0, 51.2, 28.2),
    "K(s)": (0.0, 0.0, 64.2, 29.6),
    "Mg(s)": (0.0, 0.0, 32.7, 24.9),
    "Ca(s)": (0.0, 0.0, 41.4, 25.3),
    "Al(s)": (0.0, 0.0, 28.3, 24.4),
    "Fe(s)": (0.0, 0.0, 27.3, 25.1),
    "Cu(s)": (0.0, 0.0, 33.2, 24.4),
    "Zn(s)": (0.0, 0.0, 41.6, 25.4),
    "Ag(s)": (0.0, 0.0, 42.6, 25.4),
    "Hg(l)": (0.0, 0.0, 76.0, 27.9),
    "Si(s)": (0.0, 0.0, 18.8, 20.0),
    # --- Diatomic ---
    "H(g)": (218.0, 203.3, 114.7, 20.8),
    "O(g)": (249.2, 231.7, 161.1, 21.9),
    "N(g)": (472.7, 455.5, 153.3, 20.8),
    "Cl(g)": (121.3, 105.3, 165.2, 21.8),
    "Br(g)": (111.9, 82.4, 175.0, 20.8),
    "F(g)": (79.0, 62.3, 158.8, 22.7),
    # --- Common inorganic compounds ---
    "H2O(l)": (-285.8, -237.1, 69.9, 75.3),
    "H2O(g)": (-241.8, -228.6, 188.8, 33.6),
    "H2O2(l)": (-187.8, -120.4, 109.6, 89.1),
    "CO(g)": (-110.5, -137.2, 197.7, 29.1),
    "CO2(g)": (-393.5, -394.4, 213.8, 37.1),
    "CH4(g)": (-74.8, -50.7, 186.3, 35.7),
    "C2H6(g)": (-84.7, -32.8, 229.6, 52.6),
    "C2H4(g)": (52.5, 68.4, 219.6, 43.6),
    "C2H2(g)": (227.4, 209.9, 200.9, 43.9),
    "C3H8(g)": (-104.7, -24.5, 270.3, 73.6),
    "C6H6(l)": (49.0, 124.5, 173.3, 136.0),
    "C6H6(g)": (82.9, 129.7, 269.2, 81.7),
    "CH3OH(l)": (-239.1, -166.6, 126.8, 81.6),
    "CH3OH(g)": (-201.0, -162.3, 239.9, 44.1),
    "C2H5OH(l)": (-277.7, -174.8, 160.7, 111.5),
    "C2H5OH(g)": (-235.1, -168.5, 282.7, 65.4),
    "NH3(g)": (-45.9, -16.4, 192.8, 35.1),
    "NO(g)": (90.3, 87.6, 210.8, 29.9),
    "NO2(g)": (33.1, 51.3, 240.1, 37.2),
    "N2O(g)": (82.1, 104.2, 219.9, 38.5),
    "N2O4(g)": (9.2, 97.9, 304.3, 77.3),
    "HNO3(l)": (-207.4, -80.7, 155.6, 109.9),
    "HNO3(aq)": (-207.4, -111.3, 146.4, 0.0),
    "HCl(g)": (-92.3, -95.3, 186.9, 29.1),
    "HCl(aq)": (-167.2, -131.2, 56.5, 0.0),
    "H2S(g)": (-20.6, -33.4, 205.8, 34.2),
    "SO2(g)": (-296.8, -300.1, 248.2, 39.9),
    "SO3(g)": (-395.7, -371.1, 256.8, 50.7),
    "H2SO4(l)": (-814.0, -690.0, 156.9, 138.9),
    "HF(g)": (-271.1, -273.2, 173.8, 29.1),
    "HBr(g)": (-36.3, -53.4, 198.7, 29.1),
    "HI(g)": (26.5, 1.7, 206.6, 29.2),
    "NaCl(s)": (-411.2, -384.1, 72.1, 50.5),
    "NaCl(aq)": (-407.3, -393.1, 115.5, 0.0),
    "NaOH(s)": (-425.6, -379.5, 64.5, 59.5),
    "NaOH(aq)": (-470.1, -419.2, 48.1, 0.0),
    "Na2CO3(s)": (-1130.7, -1044.4, 135.0, 112.3),
    "NaHCO3(s)": (-950.8, -851.0, 101.7, 91.0),
    "KCl(s)": (-436.5, -408.5, 82.6, 51.3),
    "KOH(s)": (-424.7, -379.1, 78.9, 64.9),
    "KOH(aq)": (-482.4, -440.5, 91.6, 0.0),
    "CaCO3(s)": (-1207.0, -1128.8, 91.7, 81.9),
    "CaO(s)": (-635.5, -603.6, 38.1, 42.0),
    "Ca(OH)2(s)": (-986.1, -898.5, 83.4, 87.5),
    "CaSO4(s)": (-1434.1, -1321.7, 106.7, 99.7),
    "MgO(s)": (-601.6, -569.0, 27.0, 37.2),
    "Mg(OH)2(s)": (-924.5, -833.5, 63.2, 77.0),
    "MgCO3(s)": (-1095.8, -1012.1, 65.7, 75.5),
    "Al2O3(s)": (-1675.7, -1582.3, 50.9, 79.0),
    "Fe2O3(s)": (-825.5, -742.2, 87.4, 103.8),
    "Fe3O4(s)": (-1118.4, -1015.4, 146.4, 150.5),
    "CuO(s)": (-157.3, -129.7, 42.6, 42.3),
    "Cu2O(s)": (-168.6, -146.0, 93.1, 63.6),
    "ZnO(s)": (-350.5, -320.5, 43.7, 40.3),
    "AgCl(s)": (-127.0, -109.8, 96.3, 50.8),
    "AgBr(s)": (-100.4, -96.9, 107.1, 52.4),
    "AgI(s)": (-61.8, -66.2, 115.5, 56.8),
    "SiO2(s,alpha-quartz)": (-910.7, -856.3, 41.5, 44.4),
    "NH4Cl(s)": (-314.4, -202.9, 94.6, 84.1),
    "NH4NO3(s)": (-365.6, -183.9, 151.1, 139.3),
    "(NH4)2SO4(s)": (-1180.9, -901.7, 220.1, 187.5),
    # --- Organic ---
    "HCHO(g)": (-108.6, -102.5, 218.8, 35.4),
    "CH3COOH(l)": (-484.5, -389.9, 159.8, 124.3),
    "CH3COOH(aq)": (-485.8, -396.5, 178.7, 0.0),
    "C6H12O6(s)": (-1273.3, -910.6, 212.1, 218.9),
    "C2H4O(g)": (-52.6, -13.0, 242.4, 47.9),   # ethylene oxide
    "CH3CHO(l)": (-192.3, -128.2, 160.2, 89.0),  # acetaldehyde
    # --- Gases ---
    "CCl4(g)": (-102.9, -60.6, 309.9, 83.4),
    "CCl4(l)": (-135.4, -65.2, 216.4, 131.8),
    "BF3(g)": (-1136.0, -1119.4, 254.4, 50.5),
    "SiCl4(g)": (-657.0, -617.0, 330.7, 90.3),
    "PCl3(g)": (-319.7, -272.3, 311.8, 71.8),
    "PCl5(g)": (-398.9, -324.6, 352.7, 112.3),
    # --- Ions (aq) ---
    "H+(aq)": (0.0, 0.0, 0.0, 0.0),
    "OH-(aq)": (-230.0, -157.2, -10.9, 0.0),
    "Na+(aq)": (-240.1, -261.9, 59.0, 46.4),
    "K+(aq)": (-252.4, -283.3, 102.5, 21.8),
    "Ca2+(aq)": (-542.8, -553.6, -53.1, 0.0),
    "Mg2+(aq)": (-466.9, -454.8, -138.1, 0.0),
    "Al3+(aq)": (-531.0, -485.0, -321.7, 0.0),
    "Fe2+(aq)": (-89.1, -78.9, -137.7, 0.0),
    "Fe3+(aq)": (-48.5, -4.7, -315.9, 0.0),
    "Zn2+(aq)": (-153.9, -147.1, -112.1, 0.0),
    "Cl-(aq)": (-167.2, -131.2, 56.5, 0.0),
    "Br-(aq)": (-121.6, -104.0, 82.4, 0.0),
    "I-(aq)": (-55.2, -51.6, 111.3, 0.0),
    "SO42-(aq)": (-909.3, -744.5, 20.1, 0.0),
    "CO32-(aq)": (-677.1, -527.8, -56.9, 0.0),
    "HCO3-(aq)": (-692.0, -586.8, 91.2, 0.0),
    "NO3-(aq)": (-207.4, -111.3, 146.4, 0.0),
    "NH4+(aq)": (-132.5, -79.3, 113.4, 79.9),
    "CH3COO-(aq)": (-486.0, -369.3, 86.6, 0.0),
    "CN-(aq)": (151.0, 172.4, 118.0, 0.0),
    "S2-(aq)": (41.8, 83.7, -22.0, 0.0),
}


def _lookup(species: str) -> tuple[float, float, float, float]:
    """Case-insensitive lookup. Returns (DeltaHdegf, DeltaGdegf, Sdeg, Cp)."""
    key = species.strip()
    if key in _THERMO_DATA:
        return _THERMO_DATA[key]
    lowered = {k.lower(): v for k, v in _THERMO_DATA.items()}
    if key.lower() in lowered:
        return lowered[key.lower()]
    raise KeyError(f"Species '{species}' not found in thermodynamic database.")


def lookup_formation_enthalpy(species: str) -> float:
    """DeltaHdegf in kJ/mol for the given species."""
    return _lookup(species)[0]


def lookup_formation_gibbs(species: str) -> float:
    """DeltaGdegf in kJ/mol for the given species."""
    return _lookup(species)[1]


def lookup_standard_entropy(species: str) -> float:
    """Sdeg in J/(mol·K) for the given species."""
    return _lookup(species)[2]


def lookup_heat_capacity(species: str) -> float:
    """Cp in J/(mol·K) for the given species."""
    return _lookup(species)[3]


def calculate_hess_law(
    products: dict[str, float],
    reactants: dict[str, float],
) -> float:
    """Calculate reaction enthalpy via Hess's law: Σ nDeltaHdegf(products) - Σ nDeltaHdegf(reactants).

    Args:
        products: dict of species -> stoichiometric coefficient
        reactants: dict of species -> stoichiometric coefficient

    Returns:
        DeltaHdegrxn in kJ/mol.
    """
    return _reaction_property(products, reactants, 0)


def calculate_reaction_entropy(
    products: dict[str, float],
    reactants: dict[str, float],
) -> float:
    """DeltaSdegrxn = Σ nSdeg(products) - Σ nSdeg(reactants). Returns J/(mol·K)."""
    return _reaction_property(products, reactants, 2)


def calculate_reaction_gibbs(
    products: dict[str, float],
    reactants: dict[str, float],
) -> float:
    """DeltaGdegrxn = Σ nDeltaGdegf(products) - Σ nDeltaGdegf(reactants). Returns kJ/mol."""
    return _reaction_property(products, reactants, 1)


def _reaction_property(
    products: dict[str, float],
    reactants: dict[str, float],
    idx: int,
) -> float:
    total = 0.0
    for species, coeff in products.items():
        total += coeff * _lookup(species)[idx]
    for species, coeff in reactants.items():
        total -= coeff * _lookup(species)[idx]
    return total


# --- pytest-compatible tests ---

def test_lookup_enthalpy():
    assert lookup_formation_enthalpy("H2O(l)") == -285.8
    assert lookup_formation_enthalpy("co2(g)") == -393.5  # case-insensitive


def test_lookup_gibbs():
    assert abs(lookup_formation_gibbs("NH3(g)") - (-16.4)) < 0.1


def test_lookup_entropy():
    assert abs(lookup_standard_entropy("N2(g)") - 191.6) < 0.1


def test_lookup_case_insensitive():
    assert lookup_formation_enthalpy("nacl(s)") == -411.2
    assert lookup_formation_enthalpy("NACL(S)") == -411.2


def test_hess_combustion_methane():
    # CH4 + 2O2 -> CO2 + 2H2O(l)
    drx = calculate_hess_law(
        {"CO2(g)": 1, "H2O(l)": 2},
        {"CH4(g)": 1, "O2(g)": 2},
    )
    assert abs(drx - (-890.3)) < 1.0


def test_hess_water_formation():
    # H2 + 1/2 O2 -> H2O(l)
    drx = calculate_hess_law({"H2O(l)": 1}, {"H2(g)": 1, "O2(g)": 0.5})
    assert abs(drx - (-285.8)) < 0.1


def test_reaction_entropy():
    # 2H2 + O2 -> 2H2O(g)
    ds = calculate_reaction_entropy(
        {"H2O(g)": 2}, {"H2(g)": 2, "O2(g)": 1},
    )
    expected = 2 * 188.8 - 2 * 130.7 - 205.2
    assert abs(ds - expected) < 0.1


def test_reaction_gibbs():
    # H2 + 1/2 O2 -> H2O(l)
    dg = calculate_reaction_gibbs({"H2O(l)": 1}, {"H2(g)": 1, "O2(g)": 0.5})
    assert abs(dg - (-237.1)) < 0.1


def test_missing_species_raises():
    try:
        lookup_formation_enthalpy("Nonexistent(g)")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_database_size():
    assert len(_THERMO_DATA) >= 80  # well above 100 entries target


if __name__ == "__main__":
    # Test 1: Combustion of methane
    print("=== Combustion of CH4 ===")
    drx = calculate_hess_law(
        {"CO2(g)": 1, "H2O(l)": 2}, {"CH4(g)": 1, "O2(g)": 2},
    )
    print(f"  DeltaHdegrxn = {drx:.1f} kJ/mol")

    # Test 2: Combustion of ethane
    print("\n=== Combustion of C2H6 ===")
    drx = calculate_hess_law(
        {"CO2(g)": 2, "H2O(l)": 3}, {"C2H6(g)": 1, "O2(g)": 3.5},
    )
    print(f"  DeltaHdegrxn = {drx:.1f} kJ/mol")

    # Test 3: Formation of ammonia (Haber process)
    print("\n=== Haber Process ===")
    dg = calculate_reaction_gibbs(
        {"NH3(g)": 2}, {"N2(g)": 1, "H2(g)": 3},
    )
    print(f"  DeltaGdegrxn = {dg:.1f} kJ/mol")

    # Test 4: Dissolution of NaCl
    print("\n=== Dissolution of NaCl ===")
    drx = calculate_hess_law(
        {"Na+(aq)": 1, "Cl-(aq)": 1}, {"NaCl(s)": 1},
    )
    print(f"  DeltaHdegrxn = {drx:.1f} kJ/mol")

    # Test 5: Thermal decomposition of CaCO3
    print("\n=== Decomposition of CaCO3 ===")
    drx = calculate_hess_law(
        {"CaO(s)": 1, "CO2(g)": 1}, {"CaCO3(s)": 1},
    )
    dg = calculate_reaction_gibbs(
        {"CaO(s)": 1, "CO2(g)": 1}, {"CaCO3(s)": 1},
    )
    print(f"  DeltaHdegrxn = {drx:.1f} kJ/mol")
    print(f"  DeltaGdegrxn = {dg:.1f} kJ/mol")

    # Test 6: Rust formation
    print("\n=== Rust Formation (Fe2O3) ===")
    drx = calculate_hess_law(
        {"Fe2O3(s)": 1}, {"Fe(s)": 2, "O2(g)": 1.5},
    )
    print(f"  DeltaHdegrxn = {drx:.1f} kJ/mol")

    # Test 7: Neutralization
    print("\n=== Neutralization HCl + NaOH ===")
    drx = calculate_hess_law(
        {"NaCl(aq)": 1, "H2O(l)": 1},
        {"HCl(aq)": 1, "NaOH(aq)": 1},
    )
    print(f"  DeltaHdegrxn = {drx:.1f} kJ/mol")

    # Test 8: Database size
    print(f"\n=== Database: {len(_THERMO_DATA)} species ===")
    print("Done!")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="calculate_hess_law",
            description="Calculate reaction enthalpy via Hess's law: Σ nDeltaHdegf(products) - Σ nDeltaHdegf(reactants).",
            input_schema=[
            InputSchemaField(name="products", type="number", required=True),
            InputSchemaField(name="reactants", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_reaction_entropy",
            description="DeltaSdegrxn = Σ nSdeg(products) - Σ nSdeg(reactants). Returns J/(mol·K).",
            input_schema=[
            InputSchemaField(name="products", type="number", required=True),
            InputSchemaField(name="reactants", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="calculate_reaction_gibbs",
            description="DeltaGdegrxn = Σ nDeltaGdegf(products) - Σ nDeltaGdegf(reactants). Returns kJ/mol.",
            input_schema=[
            InputSchemaField(name="products", type="number", required=True),
            InputSchemaField(name="reactants", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lookup_formation_enthalpy",
            description="DeltaHdegf in kJ/mol for the given species.",
            input_schema=[
            InputSchemaField(name="species", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lookup_formation_gibbs",
            description="DeltaGdegf in kJ/mol for the given species.",
            input_schema=[
            InputSchemaField(name="species", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lookup_heat_capacity",
            description="Cp in J/(mol·K) for the given species.",
            input_schema=[
            InputSchemaField(name="species", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lookup_standard_entropy",
            description="Sdeg in J/(mol·K) for the given species.",
            input_schema=[
            InputSchemaField(name="species", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_database_size",
            description="Compute test_database_size",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_hess_combustion_methane",
            description="Compute test_hess_combustion_methane",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_hess_water_formation",
            description="Compute test_hess_water_formation",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_lookup_case_insensitive",
            description="Compute test_lookup_case_insensitive",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_lookup_enthalpy",
            description="Compute test_lookup_enthalpy",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_lookup_entropy",
            description="Compute test_lookup_entropy",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_lookup_gibbs",
            description="Compute test_lookup_gibbs",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_missing_species_raises",
            description="Compute test_missing_species_raises",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_reaction_entropy",
            description="Compute test_reaction_entropy",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_reaction_gibbs",
            description="Compute test_reaction_gibbs",
            input_schema=[

            ],
            handler="{name}",
        )
    ]
