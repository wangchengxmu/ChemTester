"""
Solubility Tools - L3 Implementation
Chapter 11.03: Solubility and Henry's Law

## Solver Instructions (for AI Agent)

When you encounter solubility problems (Henry's Law, solubility product, common ion effect, precipitation prediction), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Henry's Law**: Given gas partial pressure and kH -> find dissolved concentration (or vice versa)
- **Solubility lookup**: Given gas and temperature -> get Henry's constant
- **Ksp calculation**: Given ion concentrations -> check if precipitate forms (Q vs Ksp)
- **Common ion effect**: Given Ksp and common ion concentration -> find solubility
- **Molar solubility**: Given Ksp -> find molar solubility (and vice versa)

### Step 2: Choose the correct function
- `henrys_law(kH, P)` -> C = kH x P (dissolved gas concentration in M)
- `henrys_law_pressure(kH, C)` -> P = C/kH
- `get_henry_constant(gas, temperature)` -> kH value in M/atm from HENRY_CONSTANTS
- `solubility_product(Q, Ksp)` -> precipitate forms if Q > Ksp
- `molar_solubility_from_Ksp(Ksp, formula)` -> molar solubility based on salt stoichiometry
- `Ksp_from_solubility(s, formula)` -> Ksp from molar solubility
- `common_ion_solubility(Ksp, common_ion_conc, stoichiometry)` -> reduced solubility

### Step 3: Handle special cases
- Henry's Law constants are temperature-dependent; database values at 25degC
- CO2 has much higher solubility (kH=0.034) than O2 (kH=0.0013) or N2 (kH=0.00061)
- For salts like CaF2, Ksp = 4s3; for AgCl, Ksp = s2 (check stoichiometry)
- Common ion effect always reduces solubility compared to pure water

### Examples
1. **Henry's Law**: O2 at 1 atm, kH = 1.3e-3 M/atm
   -> `henrys_law(1.3e-3, 1.0)` -> 0.0013 M dissolved O2
   -> At 0.21 atm (atmospheric): `henrys_law(1.3e-3, 0.21)` -> 2.73e-4 M

2. **Ksp check**: [Pb2+]=0.01 M, [Cl-]=0.1 M; Ksp(PbCl2)=1.7e-5
   -> Q = 0.01 x (0.1)2 = 1e-4 > 1.7e-5 -> precipitate forms

3. **CO2 solubility**: At 3 atm partial pressure
   -> `henrys_law(0.034, 3.0)` -> 0.102 M (carbonated drink under pressure)
"""

from typing import Optional, Dict

# Henry's Law constants (M/atm) at 25degC
HENRY_CONSTANTS = {
    'O2': 1.3e-3,
    'N2': 6.1e-4,
    'CO2': 3.4e-2,
    'He': 3.7e-4,
    'H2': 7.8e-4,
    'CO': 9.5e-4,
    'CH4': 1.4e-3,
}

# Solubility rules for ionic compounds
SOLUBILITY_RULES = {
    # Rule description: (condition, solubility)
    'group1': ('Compounds with Group 1 cations', 'soluble'),
    'ammonium': ('Compounds with NH4+', 'soluble'),
    'nitrate': ('Compounds with NO3-', 'soluble'),
    'acetate': ('Compounds with C2H3O2-', 'soluble'),
    'perchlorate': ('Compounds with ClO4-', 'soluble'),
    'chloride': ('Compounds with Cl-', 'mostly soluble (Ag+, Pb2+, Hg2 2+ exceptions)'),
    'bromide': ('Compounds with Br-', 'mostly soluble (Ag+, Pb2+, Hg2 2+ exceptions)'),
    'iodide': ('Compounds with I-', 'mostly soluble (Ag+, Pb2+, Hg2 2+ exceptions)'),
    'sulfate': ('Compounds with SO4 2-', 'mostly soluble (Ba2+, Pb2+, Ca2+ exceptions)'),
    'hydroxide': ('Compounds with OH-', 'mostly insoluble (Group 1, Ba2+, Ca2+, Sr2+ soluble)'),
    'carbonate': ('Compounds with CO3 2-', 'mostly insoluble (Group 1, NH4+ soluble)'),
    'phosphate': ('Compounds with PO4 3-', 'mostly insoluble (Group 1, NH4+ soluble)'),
    'sulfide': ('Compounds with S2-', 'mostly insoluble (Group 1, NH4+ soluble)'),
}


def henrys_law(kH: float, P: float) -> float:
    """
    Calculate gas solubility using Henry's Law.
    
    Args:
        kH: Henry's law constant (M/atm)
        P: Partial pressure of gas (atm)
    
    Returns:
        Concentration of dissolved gas (M)
    
    Examples:
        >>> henrys_law(1.3e-3, 1.0)  # O2 at 1 atm
        0.0013
    """
    return kH * P


def henrys_law_pressure(kH: float, C: float) -> float:
    """
    Calculate partial pressure from concentration using Henry's Law.
    
    Args:
        kH: Henry's law constant (M/atm)
        C: Concentration of dissolved gas (M)
    
    Returns:
        Partial pressure (atm)
    
    Examples:
        >>> henrys_law_pressure(1.3e-3, 0.0013)
        1.0
    """
    return C / kH


def henrys_law_gas_volume(moles_gas: float, T: float = 298.15, P: float = 1.0) -> float:
    """
    Calculate volume of gas released from solution using Henry's law context.
    Uses the ideal gas law V = nRT/P at the specified temperature.
    
    Args:
        moles_gas: Moles of gas
        T: Temperature in K (default 298.15, NOT 273K)
        P: Pressure in atm (default 1.0)
    
    Returns:
        Volume in liters
    
    Note:
        Do NOT use 273K (STP) when the problem specifies room temperature.
        Use the actual gas temperature given (typically 293K or 298K).
    """
    R = 0.08206  # L·atm/(mol·K)
    return moles_gas * R * T / P


def get_henry_constant(gas: str, temperature: float = 25) -> float:
    """
    Get Henry's Law constant for a gas.
    
    Args:
        gas: Gas formula (e.g., 'O2', 'CO2')
        temperature: Temperature in degC (default 25)
    
    Returns:
        Henry's law constant (M/atm)
    
    Examples:
        >>> get_henry_constant('O2')
        0.0013
    """
    return HENRY_CONSTANTS.get(gas, 0.001)


def predict_ionic_solubility(cation: str, anion: str) -> dict:
    """
    Predict solubility of an ionic compound.
    
    Args:
        cation: Cation symbol
        anion: Anion symbol
    
    Returns:
        Dictionary with solubility prediction and reasoning
    
    Examples:
        >>> predict_ionic_solubility('Na', 'Cl')
        {'soluble': True, 'rule': 'Compounds with Group 1 cations'}
    """
    # Group 1 cations
    group1 = ['Na', 'K', 'Li', 'Rb', 'Cs']
    if cation in group1:
        return {'soluble': True, 'rule': 'Compounds with Group 1 cations'}
    
    # Ammonium
    if cation == 'NH4':
        return {'soluble': True, 'rule': 'Compounds with NH4+'}
    
    # Always soluble anions
    always_soluble = ['NO3', 'C2H3O2', 'ClO3', 'ClO4']
    if anion in always_soluble:
        return {'soluble': True, 'rule': f'Compounds with {anion}-'}
    
    # Halides with exceptions
    halide_exceptions = ['Ag', 'Pb', 'Hg2']
    if anion in ['Cl', 'Br', 'I']:
        if cation in halide_exceptions:
            return {'soluble': False, 'rule': f'{anion}- compounds with {cation}+ are exceptions'}
        return {'soluble': True, 'rule': f'Most {anion}- compounds are soluble'}
    
    # Sulfate with exceptions
    sulfate_exceptions = ['Ba', 'Pb', 'Ca', 'Sr']
    if anion == 'SO4':
        if cation in sulfate_exceptions:
            return {'soluble': False, 'rule': f'SO4 2- compounds with {cation}2+ are exceptions'}
        return {'soluble': True, 'rule': 'Most sulfate compounds are soluble'}
    
    # Hydroxides
    if anion == 'OH':
        oh_soluble = group1 + ['Ba', 'Ca', 'Sr']
        if cation in oh_soluble:
            return {'soluble': True, 'rule': 'OH- compounds with alkali/alkaline earth metals'}
        return {'soluble': False, 'rule': 'Most hydroxides are insoluble'}
    
    # Carbonates, phosphates, sulfides
    if anion in ['CO3', 'PO4', 'S']:
        if cation in group1 or cation == 'NH4':
            return {'soluble': True, 'rule': f'{anion}- compounds with Group 1 or NH4+'}
        return {'soluble': False, 'rule': f'Most {anion}- compounds are insoluble'}
    
    return {'soluble': True, 'rule': 'Default: assumed soluble'}


def saturation_status(mass_solute: float, volume_L: float, 
                      solubility_g_per_100mL: float) -> str:
    """
    Determine if solution is unsaturated, saturated, or supersaturated.
    
    Args:
        mass_solute: Mass of solute in grams
        volume_L: Volume of solution in liters
        solubility_g_per_100mL: Solubility in g/100mL
    
    Returns:
        Saturation status string
    
    Examples:
        >>> saturation_status(10, 0.1, 20)
        'unsaturated'
        >>> saturation_status(30, 0.1, 20)
        'supersaturated'
    """
    # Convert solubility to g/L
    solubility_g_per_L = solubility_g_per_100mL * 10
    
    # Calculate actual concentration
    actual_conc = mass_solute / volume_L
    
    if actual_conc < solubility_g_per_L * 0.99:
        return 'unsaturated'
    elif actual_conc <= solubility_g_per_L * 1.01:
        return 'saturated'
    else:
        return 'supersaturated'


def temperature_effect_on_solubility(substance_type: str) -> str:
    """
    Describe how temperature affects solubility.
    
    Args:
        substance_type: 'solid' or 'gas'
    
    Returns:
        Description of temperature effect
    """
    if substance_type == 'solid':
        return 'Solubility usually increases with temperature for solids'
    elif substance_type == 'gas':
        return 'Solubility decreases with temperature for gases'
    else:
        return 'Unknown substance type'


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="get_henry_constant",
            description="Get Henry's Law constant for a gas.",
            input_schema=[
            InputSchemaField(name="gas", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="henrys_law",
            description="Calculate gas solubility using Henry's Law.",
            input_schema=[
            InputSchemaField(name="kH", type="number", required=True),
            InputSchemaField(name="P", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="henrys_law_pressure",
            description="Calculate partial pressure from concentration using Henry's Law.",
            input_schema=[
            InputSchemaField(name="kH", type="number", required=True),
            InputSchemaField(name="C", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_ionic_solubility",
            description="Predict solubility of an ionic compound.",
            input_schema=[
            InputSchemaField(name="cation", type="number", required=True),
            InputSchemaField(name="anion", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="saturation_status",
            description="Determine if solution is unsaturated, saturated, or supersaturated.",
            input_schema=[
            InputSchemaField(name="mass_solute", type="number", required=True),
            InputSchemaField(name="volume_L", type="number", required=True),
            InputSchemaField(name="solubility_g_per_100mL", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="temperature_effect_on_solubility",
            description="Describe how temperature affects solubility.",
            input_schema=[
            InputSchemaField(name="substance_type", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
