"""
Quantitative Analysis Tools (L3)
Source: LibreTexts Chemistry 2e Ch04.05
"""
## Solver Instructions (for AI Agent)

# When you encounter analytical chemistry quantitative problems (calibration, titration, gravimetry), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: concentration data, signals, masses, volumes, titration curves
# - **Asked**: unknown concentration, sample purity, detection limits, recovery

### Step 2: Choose the correct function
# Read the file to identify available functions and their parameters.

### Step 3: Handle special cases
# - Always check units consistency (M, mg/L, ppm, ppb)
# - For dilution series, use M1V1 = M2V2
# - Report with appropriate significant figures

### Examples
# 1. Calibration curve: fit concentrations vs signals, predict unknown concentration
# 2. Gravimetric analysis: calculate purity from precipitate mass
# 3. Titration: determine concentration from equivalence point volume


# === TITRATION ===

def titration_molarity(M_titrant, V_titrant_mL, V_analyte_mL, coeff_ratio):
    """
    Calculate analyte molarity from titration data.
    
    M_analyte = (M_titrant x V_titrant x coeff_ratio) / V_analyte
    
    Parameters:
        M_titrant: molarity of titrant (mol/L)
        V_titrant_mL: volume of titrant (mL)
        V_analyte_mL: volume of analyte (mL)
        coeff_ratio: (coeff_analyte / coeff_titrant) from balanced equation
    
    Returns:
        M_analyte: molarity of analyte (mol/L)
    
    Raises:
        ValueError: if volume is zero or negative
    """
    if V_analyte_mL <= 0:
        raise ValueError("Analyte volume must be positive")
    if V_titrant_mL < 0:
        raise ValueError("Titrant volume cannot be negative")
    
    # mmol = M (mol/L) x V (mL) / 1000
    # But using the shortcut: M = mmol / mL
    mmol_titrant = M_titrant * V_titrant_mL
    mmol_analyte = mmol_titrant * coeff_ratio
    M_analyte = mmol_analyte / V_analyte_mL
    
    return M_analyte


def titration_moles(M_titrant, V_titrant_L):
    """
    Calculate moles of titrant.
    
    mol = M x V
    
    Parameters:
        M_titrant: molarity in mol/L
        V_titrant_L: volume in liters
    
    Returns:
        moles (float)
    """
    return M_titrant * V_titrant_L


# === GRAVIMETRIC ===

def gravimetric_mass_analyte(mass_precipitate, molar_mass_precipitate, 
                              molar_mass_analyte, mol_ratio):
    """
    Calculate mass of analyte from precipitate mass.
    
    mass_analyte = mass_precip x (1/M_precip) x mol_ratio x M_analyte
    
    Parameters:
        mass_precipitate: mass of precipitate (g)
        molar_mass_precipitate: molar mass of precipitate (g/mol)
        molar_mass_analyte: molar mass of analyte (g/mol)
        mol_ratio: (mol analyte / mol precipitate) from stoichiometry
    
    Returns:
        mass of analyte in grams
    """
    if molar_mass_precipitate <= 0:
        raise ValueError("Molar mass of precipitate must be positive")
    
    mol_precip = mass_precipitate / molar_mass_precipitate
    mol_analyte = mol_precip * mol_ratio
    mass_analyte = mol_analyte * molar_mass_analyte
    
    return mass_analyte


def gravimetric_mass_percent(mass_precipitate, molar_mass_precipitate, 
                              molar_mass_analyte, mol_ratio, mass_sample):
    """
    Calculate mass percent of analyte from gravimetric data.
    
    mass_percent = (mass_analyte / mass_sample) x 100%
    
    Parameters:
        mass_precipitate: mass of precipitate (g)
        molar_mass_precipitate: molar mass of precipitate (g/mol)
        molar_mass_analyte: molar mass of analyte (g/mol)
        mol_ratio: (mol analyte / mol precipitate) from stoichiometry
        mass_sample: mass of original sample (g)
    
    Returns:
        mass percent (float, 0-100)
    """
    if mass_sample <= 0:
        raise ValueError("Sample mass must be positive")
    
    mass_analyte = gravimetric_mass_analyte(
        mass_precipitate, molar_mass_precipitate, molar_mass_analyte, mol_ratio
    )
    return (mass_analyte / mass_sample) * 100.0


# === COMBUSTION ANALYSIS ===

def combustion_moles_from_CO2(mass_CO2):
    """
    Calculate moles of carbon from CO2 mass.
    
    mol_C = mass_CO2 / 44.01
    
    Parameters:
        mass_CO2: mass of CO2 in grams
    
    Returns:
        moles of carbon
    """
    M_CO2 = 44.01  # g/mol
    return mass_CO2 / M_CO2


def combustion_moles_from_H2O(mass_H2O):
    """
    Calculate moles of hydrogen from H2O mass.
    
    mol_H = (mass_H2O / 18.02) x 2
    
    Parameters:
        mass_H2O: mass of H2O in grams
    
    Returns:
        moles of hydrogen
    """
    M_H2O = 18.02  # g/mol
    mol_H2O = mass_H2O / M_H2O
    return mol_H2O * 2


def combustion_empirical_formula(mass_CO2, mass_H2O, mass_sample=None, 
                                  other_elements=None):
    """
    Determine empirical formula from combustion analysis.
    
    mol_C = mass_CO2 / 44.01
    mol_H = (mass_H2O / 18.02) x 2
    
    Parameters:
        mass_CO2: mass of CO2 produced (g)
        mass_H2O: mass of H2O produced (g)
        mass_sample: optional, for checking mass balance
        other_elements: optional dict {element: moles} for compounds with O, N, etc.
    
    Returns:
        empirical formula as string (e.g., "CH2")
    """
    mol_C = combustion_moles_from_CO2(mass_CO2)
    mol_H = combustion_moles_from_H2O(mass_H2O)
    
    # Collect all elements
    elements = {'C': mol_C, 'H': mol_H}
    if other_elements:
        elements.update(other_elements)
    
    # Find smallest mole value
    min_mol = min(v for v in elements.values() if v > 0)
    
    # Calculate ratios
    ratios = {elem: mol / min_mol for elem, mol in elements.items()}
    
    # Convert to near-integer values
    def near_integer(x, tolerance=0.1):
        rounded = round(x)
        if abs(x - rounded) < tolerance:
            return int(rounded)
        return x  # Keep as float if not close to integer
    
    int_ratios = {elem: near_integer(r) for elem, r in ratios.items()}
    
    # Build formula string
    formula = ""
    # Standard order: C, H, then alphabetical
    order = ['C', 'H'] + sorted(set(elements.keys()) - {'C', 'H'})
    for elem in order:
        if elem in int_ratios:
            count = int_ratios[elem]
            if count == 1:
                formula += elem
            else:
                formula += f"{elem}{int(count) if isinstance(count, float) else count}"
    
    return formula


if __name__ == "__main__":
    print("Quantitative analysis tools - implemented")
    
    # Test titration: 50.00 mL HCl titrated with 35.23 mL of 0.250 M NaOH
    # HCl + NaOH -> NaCl + H2O (1:1 ratio)
    M_HCl = titration_molarity(0.250, 35.23, 50.00, coeff_ratio=1)
    print(f"Test 1: M_HCl = {M_HCl:.4f} M (expected: 0.176 M)")
    
    # Test gravimetric: 0.4550 g sample with MgSO4, yields 0.6168 g BaSO4
    # MgSO4 + Ba(NO3)2 -> BaSO4 + Mg(NO3)2
    # M(BaSO4) = 233.43, M(MgSO4) = 120.37
    mass_percent = gravimetric_mass_percent(
        0.6168, 233.43, 120.37, mol_ratio=1, mass_sample=0.4550
    )
    print(f"Test 2: MgSO4 mass percent = {mass_percent:.1f}%")
    
    # Test combustion: 0.00394 g CO2, 0.00161 g H2O
    formula = combustion_empirical_formula(0.00394, 0.00161)
    print(f"Test 3: Empirical formula = {formula} (expected: CH2)")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="combustion_empirical_formula",
            description="Determine empirical formula from combustion analysis.",
            input_schema=[
            InputSchemaField(name="mass_CO2", type="number", required=True),
            InputSchemaField(name="mass_H2O", type="number", required=True),
            InputSchemaField(name="mass_sample", type="number", required=False),
            InputSchemaField(name="other_elements", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="combustion_moles_from_CO2",
            description="Calculate moles of carbon from CO2 mass.",
            input_schema=[
            InputSchemaField(name="mass_CO2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="combustion_moles_from_H2O",
            description="Calculate moles of hydrogen from H2O mass.",
            input_schema=[
            InputSchemaField(name="mass_H2O", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gravimetric_mass_analyte",
            description="Calculate mass of analyte from precipitate mass.",
            input_schema=[
            InputSchemaField(name="mass_precipitate", type="number", required=True),
            InputSchemaField(name="molar_mass_precipitate", type="number", required=True),
            InputSchemaField(name="molar_mass_analyte", type="number", required=True),
            InputSchemaField(name="mol_ratio", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gravimetric_mass_percent",
            description="Calculate mass percent of analyte from gravimetric data.",
            input_schema=[
            InputSchemaField(name="mass_precipitate", type="number", required=True),
            InputSchemaField(name="molar_mass_precipitate", type="number", required=True),
            InputSchemaField(name="molar_mass_analyte", type="number", required=True),
            InputSchemaField(name="mol_ratio", type="number", required=True),
            InputSchemaField(name="mass_sample", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="titration_molarity",
            description="Calculate analyte molarity from titration data.",
            input_schema=[
            InputSchemaField(name="M_titrant", type="number", required=True),
            InputSchemaField(name="V_titrant_mL", type="number", required=True),
            InputSchemaField(name="V_analyte_mL", type="number", required=True),
            InputSchemaField(name="coeff_ratio", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="titration_moles",
            description="Calculate moles of titrant.",
            input_schema=[
            InputSchemaField(name="M_titrant", type="number", required=True),
            InputSchemaField(name="V_titrant_L", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
