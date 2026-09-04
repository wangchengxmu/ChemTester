"""
Solubility Equilibria Tools - L3 Implementation
Chapter 15.1: Precipitation and Dissolution

## Solver Instructions (for AI Agent)

When you encounter a solubility equilibria problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Ksp value: Look for solubility product constant
- Molar solubility (s): mol/L of compound that dissolves
- Salt type: Determine stoichiometry (MX->1:1, MX2->1:2, M2X->2:1)
- Ion concentrations: For Q calculation or common ion effect
- Chemical formula: Extract to determine stoichiometry

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate molar solubility (1:1 salt) | `molar_solubility_11(Ksp)` |
| Calculate molar solubility (1:2 salt like MX2) | `molar_solubility_12(Ksp)` |
| Calculate molar solubility (2:1 salt like M2X) | `molar_solubility_21(Ksp)` |
| Calculate Ksp from solubility (1:1) | `Ksp_from_solubility_11(s)` |
| Calculate Ksp from solubility (1:2) | `Ksp_from_solubility_12(s)` |
| Calculate ion product Q | `ion_product(cation_conc, anion_conc, cation_coeff, anion_coeff)` |
| Predict precipitation | `predict_precipitation(Q, Ksp)` |
| Solubility with common ion | `solubility_common_ion(Ksp, common_ion_conc, salt_type)` |
| Calculate precipitate mass | `precipitate_amount(initial_conc, final_conc, volume, molar_mass)` |

### Step 3: Handle special cases
- **Salt stoichiometry**: Identify from formula (AgCl->1:1, PbCl2->1:2, Ag2CrO4->2:1)
- **Q vs Ksp**: Q < Ksp -> unsaturated; Q > Ksp -> precipitation; Q = Ksp -> saturated
- **Common ion effect**: Solubility decreases when common ion is present
- **Units**: Ksp is dimensionless; solubility in mol/L

### Examples

**Example 1: Molar solubility from Ksp**
Question: "Calculate the molar solubility of AgCl (Ksp = 1.8 x 10-10)."
- Given: Ksp = 1.8e-10, AgCl is 1:1 salt
- Solution: `molar_solubility_11(Ksp=1.8e-10)` -> 1.34 x 10-5 M

**Example 2: Ksp from solubility**
Question: "PbCl2 has solubility of 0.016 M. Calculate Ksp."
- Given: s = 0.016 M, PbCl2 is 1:2 salt
- Solution: `Ksp_from_solubility_12(s=0.016)` -> Ksp = 1.6 x 10-5

**Example 3: Predict precipitation**
Question: "Will precipitation occur if [Ag+] = 0.01 M and [Cl-] = 0.001 M? (Ksp = 1.8 x 10-10)"
- Given: [Ag+] = 0.01, [Cl-] = 0.001, Ksp = 1.8e-10
- Solution: 
  - `Q = ion_product(cation_conc=0.01, anion_conc=0.001)` -> Q = 1.0e-5
  - `predict_precipitation(Q=1e-5, Ksp=1.8e-10)` -> 'precipitation occurs'

**Example 4: Common ion effect**
Question: "What is the solubility of AgCl in 0.10 M NaCl?"
- Given: Ksp = 1.8e-10, [Cl-] = 0.10 M (common ion), salt_type = '11'
- Solution: `solubility_common_ion(Ksp=1.8e-10, common_ion_conc=0.10, salt_type='11')` -> 1.8 x 10-9 M
"""

from typing import Dict, Tuple, Optional
from math import sqrt


def Ksp_expression(cation: str, cation_coeff: int,
                   anion: str, anion_coeff: int) -> str:
    """
    Generate Ksp expression for a salt.
    
    Args:
        cation: Cation formula
        cation_coeff: Coefficient of cation
        anion: Anion formula
        anion_coeff: Coefficient of anion
    
    Returns:
        Ksp expression string
    
    Examples:
        >>> Ksp_expression('Ag+', 1, 'Cl-', 1)
        'Ksp = [Ag+][Cl-]'
        >>> Ksp_expression('Ca2+', 1, 'F-', 2)
        'Ksp = [Ca2+][F-]^2'
    """
    if cation_coeff == 1:
        cation_term = f'[{cation}]'
    else:
        cation_term = f'[{cation}]^{cation_coeff}'
    
    if anion_coeff == 1:
        anion_term = f'[{anion}]'
    else:
        anion_term = f'[{anion}]^{anion_coeff}'
    
    return f'Ksp = {cation_term}{anion_term}'


def molar_solubility_11(Ksp: float) -> float:
    """
    Calculate molar solubility for 1:1 salt (MX).
    
    s = √Ksp
    
    Args:
        Ksp: Solubility product
    
    Returns:
        Molar solubility (M)
    
    Examples:
        >>> molar_solubility_11(1.8e-10)
        1.34e-05
    """
    return sqrt(Ksp)


def molar_solubility_12(Ksp: float) -> float:
    """
    Calculate molar solubility for 1:2 salt (MX2).
    
    s = ∛(Ksp/4)
    
    Args:
        Ksp: Solubility product
    
    Returns:
        Molar solubility (M)
    
    Examples:
        >>> molar_solubility_12(3.9e-11)
        2.14e-04
    """
    return (Ksp / 4) ** (1/3)


def molar_solubility_21(Ksp: float) -> float:
    """
    Calculate molar solubility for 2:1 salt (M2X).
    
    s = ∛(Ksp/4)
    
    Args:
        Ksp: Solubility product
    
    Returns:
        Molar solubility (M)
    
    Examples:
        >>> molar_solubility_21(1.2e-5)
        0.014
    """
    return (Ksp / 4) ** (1/3)


def Ksp_from_solubility_11(s: float) -> float:
    """
    Calculate Ksp from molar solubility for 1:1 salt.
    
    Ksp = s2
    
    Args:
        s: Molar solubility (M)
    
    Returns:
        Ksp value
    
    Examples:
        >>> Ksp_from_solubility_11(1.34e-5)
        1.8e-10
    """
    return s ** 2


def Ksp_from_solubility_12(s: float) -> float:
    """
    Calculate Ksp from molar solubility for 1:2 salt.
    
    Ksp = 4s3
    
    Args:
        s: Molar solubility (M)
    
    Returns:
        Ksp value
    
    Examples:
        >>> Ksp_from_solubility_12(2.14e-4)
        3.9e-11
    """
    return 4 * s ** 3


def ion_product(cation_conc: float, anion_conc: float,
                cation_coeff: int = 1, anion_coeff: int = 1) -> float:
    """
    Calculate ion product Q for a salt.
    
    Q = [cation]^a[anion]^b
    
    Args:
        cation_conc: Cation concentration (M)
        anion_conc: Anion concentration (M)
        cation_coeff: Cation coefficient
        anion_coeff: Anion coefficient
    
    Returns:
        Ion product Q
    
    Examples:
        >>> ion_product(0.01, 0.01, 1, 1)
        0.0001
    """
    return (cation_conc ** cation_coeff) * (anion_conc ** anion_coeff)


def predict_precipitation(Q: float, Ksp: float) -> str:
    """
    Predict if precipitation will occur.
    
    Args:
        Q: Ion product
        Ksp: Solubility product
    
    Returns:
        Prediction string
    
    Examples:
        >>> predict_precipitation(1e-8, 1e-10)
        'precipitation occurs'
        >>> predict_precipitation(1e-12, 1e-10)
        'unsaturated'
    """
    if Q < Ksp:
        return 'unsaturated'
    elif Q > Ksp:
        return 'precipitation occurs'
    else:
        return 'saturated (equilibrium)'


def solubility_common_ion(Ksp: float, common_ion_conc: float,
                           salt_type: str = '11') -> float:
    """
    Calculate solubility in presence of common ion.
    
    Args:
        Ksp: Solubility product
        common_ion_conc: Concentration of common ion (M)
        salt_type: '11', '12', or '21'
    
    Returns:
        Molar solubility
    
    Examples:
        >>> solubility_common_ion(1.8e-10, 0.1, '11')
        1.8e-09
    """
    if salt_type == '11':
        # Ksp = s x (common_ion_conc + s) ~ s x common_ion_conc
        return Ksp / common_ion_conc
    elif salt_type == '12':
        # For MX2 with common M2+: Ksp = [M][X]2
        return sqrt(Ksp / common_ion_conc) / 2
    else:
        return Ksp / common_ion_conc


def precipitate_amount(initial_conc: float, final_conc: float,
                       volume: float, molar_mass: float) -> float:
    """
    Calculate mass of precipitate formed.
    
    Args:
        initial_conc: Initial concentration (M)
        final_conc: Final equilibrium concentration (M)
        volume: Solution volume (L)
        molar_mass: Molar mass (g/mol)
    
    Returns:
        Mass of precipitate (g)
    
    Examples:
        >>> precipitate_amount(0.1, 0.01, 1.0, 143.3)
        12.9
    """
    moles_precipitated = (initial_conc - final_conc) * volume
    return moles_precipitated * molar_mass


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="Ksp_expression",
            description="Generate Ksp expression for a salt.",
            input_schema=[
            InputSchemaField(name="cation", type="number", required=True),
            InputSchemaField(name="cation_coeff", type="number", required=True),
            InputSchemaField(name="anion", type="number", required=True),
            InputSchemaField(name="anion_coeff", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="Ksp_from_solubility_11",
            description="Calculate Ksp from molar solubility for 1:1 salt.",
            input_schema=[
            InputSchemaField(name="s", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="Ksp_from_solubility_12",
            description="Calculate Ksp from molar solubility for 1:2 salt.",
            input_schema=[
            InputSchemaField(name="s", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ion_product",
            description="Calculate ion product Q for a salt.",
            input_schema=[
            InputSchemaField(name="cation_conc", type="number", required=True),
            InputSchemaField(name="anion_conc", type="number", required=True),
            InputSchemaField(name="cation_coeff", type="number", required=False),
            InputSchemaField(name="anion_coeff", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molar_solubility_11",
            description="Calculate molar solubility for 1:1 salt (MX).",
            input_schema=[
            InputSchemaField(name="Ksp", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molar_solubility_12",
            description="Calculate molar solubility for 1:2 salt (MX2).",
            input_schema=[
            InputSchemaField(name="Ksp", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="molar_solubility_21",
            description="Calculate molar solubility for 2:1 salt (M2X).",
            input_schema=[
            InputSchemaField(name="Ksp", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="precipitate_amount",
            description="Calculate mass of precipitate formed.",
            input_schema=[
            InputSchemaField(name="initial_conc", type="number", required=True),
            InputSchemaField(name="final_conc", type="number", required=True),
            InputSchemaField(name="volume", type="number", required=True),
            InputSchemaField(name="molar_mass", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_precipitation",
            description="Predict if precipitation will occur.",
            input_schema=[
            InputSchemaField(name="Q", type="number", required=True),
            InputSchemaField(name="Ksp", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="solubility_common_ion",
            description="Calculate solubility in presence of common ion.",
            input_schema=[
            InputSchemaField(name="Ksp", type="number", required=True),
            InputSchemaField(name="common_ion_conc", type="number", required=True),
            InputSchemaField(name="salt_type", type="string", required=False)
            ],
            handler="{name}",
        )
    ]
