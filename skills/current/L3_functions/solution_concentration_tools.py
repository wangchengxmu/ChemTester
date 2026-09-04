"""
Solution Concentration Tools - L3 Implementation
Chapter 11: Solutions - Concentration units and conversions

## Solver Instructions (for AI Agent)

When you encounter a solution concentration problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Moles of solute: Look for "mol", or calculate from mass/molar mass
- Mass of solute: Look for "g", "kg"
- Volume of solution: Look for "L", "mL" -> convert to L
- Mass of solvent: Look for "kg solvent" for molality
- Concentration units: Look for "M" (molarity), "m" (molality), "ppm", "ppb", "%"
- Density: Given for some conversions, often in g/mL

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate molarity | `molarity(moles_solute, L_solution)` |
| Calculate molality | `molality(moles_solute, kg_solvent)` |
| Calculate mole fraction | `mole_fraction({'A': mol_A, 'B': mol_B})` |
| Calculate mass percent | `mass_percent(mass_solute, mass_solution)` |
| Convert ppm/ppb | `ppm_ppb(concentration, unit)` |
| Dilution calculation (M1V1=M2V2) | `dilution(M1, V1, M2, V2)` - pass None for unknown |
| Convert ppm to molarity | `parts_per_to_molarity(ppm, molar_mass)` |
| Convert molality to molarity | `molality_to_molarity(m, density, M_solute)` |
| Convert molarity to molality | `molarity_to_molality(M, density, M_solute)` |
| Calculate moles from molarity | `molarity_from_moles(moles, volume, unit)` |

### Step 3: Handle special cases
- **Unit conversions**: mL -> L (/1000), g -> kg (/1000)
- **Molarity vs Molality**: Molarity uses solution volume; molality uses solvent mass
- **Molar mass needed**: For ppm->M conversions, extract formula from question
- **Dilution**: M1V1 = M2V2; one of M2 or V2 must be None
- **Density usage**: Needed for M↔m conversions

### Examples

**Example 1: Calculate molarity**
Question: "What is the molarity of a solution with 0.50 mol NaCl in 250 mL?"
- Given: moles = 0.50 mol, V = 250 mL = 0.250 L
- Solution: `molarity(moles_solute=0.50, L_solution=0.250)` -> 2.0 M

**Example 2: Mole fraction**
Question: "Calculate mole fraction of each component if 2 mol ethanol mixed with 8 mol water."
- Given: {'ethanol': 2, 'water': 8}
- Solution: `mole_fraction({'ethanol': 2, 'water': 8})` -> {'ethanol': 0.20, 'water': 0.80}

**Example 3: Dilution**
Question: "What volume of 6.0 M HCl is needed to prepare 500 mL of 0.10 M HCl?"
- Given: M1=6.0, M2=0.10, V2=0.500 L
- Solution: `dilution(M1=6.0, V1=None, M2=0.10, V2=0.500)` -> V1 = 0.0083 L = 8.3 mL

**Example 4: Mass percent**
Question: "What is the mass percent of NaCl if 5.0 g NaCl dissolved in 95 g water?"
- Given: mass_solute = 5.0 g, mass_solution = 100 g
- Solution: `mass_percent(mass_solute=5.0, mass_solution=100)` -> 5.0%
"""

from typing import Dict, List, Tuple, Optional


def mole_fraction(components: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate mole fractions for all components.
    
    Args:
        components: Dictionary of {substance: moles}
    
    Returns:
        Dictionary of {substance: mole_fraction}
    
    Examples:
        >>> mole_fraction({'A': 1, 'B': 3})
        {'A': 0.25, 'B': 0.75}
    """
    total_moles = sum(components.values())
    return {name: moles / total_moles for name, moles in components.items()}


def molality(moles_solute: float, kg_solvent: float) -> float:
    """
    Calculate molality of a solution.
    
    Args:
        moles_solute: Moles of solute
        kg_solvent: Mass of solvent in kilograms
    
    Returns:
        Molality (mol/kg)
    
    Examples:
        >>> molality(2, 0.5)
        4.0
    """
    return moles_solute / kg_solvent


def molarity(moles_solute: float, L_solution: float) -> float:
    """
    Calculate molarity of a solution.
    
    Args:
        moles_solute: Moles of solute
        L_solution: Volume of solution in liters
    
    Returns:
        Molarity (mol/L)
    
    Examples:
        >>> molarity(0.5, 2)
        0.25
    """
    return moles_solute / L_solution


def molarity_from_moles(moles: float, volume: float, unit: str = "L") -> float:
    """
    Calculate molarity from moles and volume.
    
    Args:
        moles: Moles of solute
        volume: Volume value
        unit: Volume unit ('L', 'mL')
    
    Returns:
        Molarity (mol/L)
    
    Examples:
        >>> molarity_from_moles(0.5, 250, "mL")
        2.0
    """
    if unit == "mL":
        volume = volume / 1000
    return moles / volume


def molality_to_molarity(m: float, density: float, 
                         molar_mass_solute: float, 
                         molar_mass_solvent: float = 18.015) -> float:
    """
    Convert molality to molarity.
    
    Args:
        m: Molality (mol/kg)
        density: Solution density (g/mL)
        molar_mass_solute: Molar mass of solute (g/mol)
        molar_mass_solvent: Molar mass of solvent (g/mol, default water)
    
    Returns:
        Molarity (mol/L)
    
    Examples:
        >>> molality_to_molarity(1, 1.05, 58.44)  # 1m NaCl
        1.02...
    """
    # For 1 kg solvent with m mol solute
    mass_solvent = 1000  # g
    mass_solute = m * molar_mass_solute  # g
    mass_solution = mass_solvent + mass_solute  # g
    
    volume_solution = mass_solution / density / 1000  # L
    
    return m / volume_solution


def molarity_to_molality(M: float, density: float,
                         molar_mass_solute: float) -> float:
    """
    Convert molarity to molality.
    
    Args:
        M: Molarity (mol/L)
        density: Solution density (g/mL)
        molar_mass_solute: Molar mass of solute (g/mol)
    
    Returns:
        Molality (mol/kg)
    
    Examples:
        >>> molarity_to_molality(1, 1.05, 58.44)  # 1M NaCl
        1.04...
    """
    # For 1 L solution
    mass_solution = density * 1000  # g
    mass_solute = M * molar_mass_solute  # g
    mass_solvent = mass_solution - mass_solute  # g
    
    return M * 1000 / mass_solvent


def mass_percent(mass_solute: float, mass_solution: float) -> float:
    """
    Calculate mass percentage.
    
    Args:
        mass_solute: Mass of solute
        mass_solution: Total mass of solution
    
    Returns:
        Mass percentage
    
    Examples:
        >>> mass_percent(10, 100)
        10.0
    """
    return 100 * mass_solute / mass_solution


def ppm_ppb(concentration: float, unit: str = 'ppm') -> float:
    """
    Convert between ppm and ppb.
    
    Args:
        concentration: Concentration value
        unit: 'ppm' or 'ppb'
    
    Returns:
        Concentration in the other unit
    
    Examples:
        >>> ppm_ppb(1, 'ppm')
        1000
    """
    if unit == 'ppm':
        return concentration * 1000  # ppb
    else:
        return concentration / 1000  # ppm


def dilution(M1: float, V1: float, M2: float = None, V2: float = None) -> float:
    """
    Calculate dilution using M1V1 = M2V2.
    
    Args:
        M1, V1: Initial concentration and volume
        M2, V2: Final concentration and volume (one must be None)
    
    Returns:
        The missing value
    
    Examples:
        >>> dilution(M1=1, V1=100, M2=0.5)
        200.0
    """
    if M2 is None:
        return M1 * V1 / V2
    elif V2 is None:
        return M1 * V1 / M2
    else:
        raise ValueError("One of M2 or V2 must be None")


def parts_per_to_molarity(ppm: float, molar_mass: float, 
                          density: float = 1.0) -> float:
    """
    Convert ppm to molarity for aqueous solutions.
    
    Args:
        ppm: Concentration in ppm (mg/L for dilute aqueous)
        molar_mass: Molar mass in g/mol
        density: Solution density (default 1.0 g/mL)
    
    Returns:
        Molarity (mol/L)
    
    Examples:
        >>> parts_per_to_molarity(100, 58.44)  # 100 ppm NaCl
        0.00171...
    """
    mg_per_L = ppm
    g_per_L = mg_per_L / 1000
    return g_per_L / molar_mass


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="dilution",
            description="Calculate dilution using M1V1 = M2V2.",
            input_schema=[
            InputSchemaField(name="M1", type="number", required=True),
            InputSchemaField(name="V1", type="number", required=True),
            InputSchemaField(name="M2", type="number", required=False),
            InputSchemaField(name="V2", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mass_percent",
            description="Calculate mass percentage.",
            input_schema=[
            InputSchemaField(name="mass_solute", type="number", required=True),
            InputSchemaField(name="mass_solution", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molality",
            description="Calculate molality of a solution.",
            input_schema=[
            InputSchemaField(name="moles_solute", type="number", required=True),
            InputSchemaField(name="kg_solvent", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molality_to_molarity",
            description="Convert molality to molarity.",
            input_schema=[
            InputSchemaField(name="m", type="number", required=True),
            InputSchemaField(name="density", type="number", required=True),
            InputSchemaField(name="molar_mass_solute", type="number", required=True),
            InputSchemaField(name="molar_mass_solvent", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molarity",
            description="Calculate molarity of a solution.",
            input_schema=[
            InputSchemaField(name="moles_solute", type="number", required=True),
            InputSchemaField(name="L_solution", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molarity_from_moles",
            description="Calculate molarity from moles and volume.",
            input_schema=[
            InputSchemaField(name="moles", type="number", required=True),
            InputSchemaField(name="volume", type="number", required=True),
            InputSchemaField(name="unit", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molarity_to_molality",
            description="Convert molarity to molality.",
            input_schema=[
            InputSchemaField(name="M", type="number", required=True),
            InputSchemaField(name="density", type="number", required=True),
            InputSchemaField(name="molar_mass_solute", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mole_fraction",
            description="Calculate mole fractions for all components.",
            input_schema=[
            InputSchemaField(name="components", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="parts_per_to_molarity",
            description="Convert ppm to molarity for aqueous solutions.",
            input_schema=[
            InputSchemaField(name="ppm", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=True),
            InputSchemaField(name="density", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ppm_ppb",
            description="Convert between ppm and ppb.",
            input_schema=[
            InputSchemaField(name="concentration", type="number", required=True),
            InputSchemaField(name="unit", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
