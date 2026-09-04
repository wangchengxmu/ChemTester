"""
Titration Tools - L3 Implementation
Chapter 14.7: Acid-Base Titrations

## Solver Instructions (for AI Agent)

When you encounter a titration problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Analyte: The substance being titrated (acid or base)
- Titrant: The solution of known concentration
- Volumes and concentrations: V_analyte, C_analyte, C_titrant
- Equivalence point: Where moles acid = moles base
- Acid/base type: Strong/strong, strong/weak, weak/strong
- Ka or Kb: For weak acid/base

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate equivalence volume | `equivalence_volume(analyte_mol, titrant_conc, stoichiometry)` |
| Calculate pH during strong-strong titration | `titration_pH_strong_strong(V_titrant, V_analyte, C_analyte, C_titrant, analyte_is_acid)` |
| Calculate pH at half-equivalence | `half_equivalence_pH(pKa)` |
| Calculate pH at equivalence (weak acid) | `equivalence_pH_weak_acid(V_analyte, C_analyte, Ka)` |
| Get indicator pH range | `indicator_range(indicator)` |
| Select appropriate indicator | `select_indicator(equivalence_pH)` |
| Generate titration curve points | `titration_curve_points(V_analyte, C_acid, C_base, Ka, is_weak_acid)` |

### Step 3: Handle special cases
- **Strong-strong titration**: pH = 7 at equivalence
- **Weak acid + strong base**: pH > 7 at equivalence (conjugate base hydrolysis)
- **Weak base + strong acid**: pH < 7 at equivalence (conjugate acid hydrolysis)
- **Half-equivalence**: pH = pKa for weak acid (or pOH = pKb for weak base)
- **Indicator selection**: Choose indicator whose range contains equivalence pH
- **Buffer region**: Before equivalence, use Henderson-Hasselbalch

### Examples

**Example 1: Strong-strong titration**
Question: "What is the pH when 25.0 mL of 0.10 M NaOH is added to 50.0 mL of 0.10 M HCl?"
- Given: V_titrant = 0.025 L, V_analyte = 0.050 L, C_acid = 0.10 M, C_base = 0.10 M
- Solution: `titration_pH_strong_strong(V_titrant=0.025, V_analyte=0.050, C_analyte=0.10, C_titrant=0.10, analyte_is_acid=True)` -> pH = 1.48 (before equivalence)

**Example 2: Equivalence volume**
Question: "What volume of 0.10 M NaOH is needed to titrate 25.0 mL of 0.15 M HCl?"
- Given: moles_HCl = 0.025 x 0.15 = 0.00375 mol, C_NaOH = 0.10 M
- Solution: `equivalence_volume(analyte_mol=0.00375, titrant_conc=0.10, stoichiometry=1)` -> 0.0375 L = 37.5 mL

**Example 3: Weak acid equivalence pH**
Question: "What is the pH at equivalence for titrating 25.0 mL of 0.10 M acetic acid (Ka = 1.8x10-5) with 0.10 M NaOH?"
- Given: V = 0.025 L, C = 0.10 M, Ka = 1.8e-5
- Solution: `equivalence_pH_weak_acid(V_analyte=0.025, C_analyte=0.10, Ka=1.8e-5)` -> pH ~ 8.72

**Example 4: Indicator selection**
Question: "Which indicator is best for a titration with equivalence pH = 8.7?"
- Solution: `select_indicator(equivalence_pH=8.7)` -> 'phenolphthalein'
"""

from typing import Dict, Tuple, Optional
from math import log10, sqrt


def equivalence_volume(analyte_mol: float, 
                       titrant_conc: float,
                       stoichiometry: int = 1) -> float:
    """
    Calculate volume of titrant at equivalence point.
    
    Args:
        analyte_mol: Moles of analyte
        titrant_conc: Concentration of titrant (M)
        stoichiometry: Molar ratio (titrant:analyte)
    
    Returns:
        Volume of titrant (L)
    
    Examples:
        >>> equivalence_volume(0.0025, 0.1, 1)
        0.025
    """
    return analyte_mol * stoichiometry / titrant_conc


def titration_pH_strong_strong(V_titrant: float,
                                V_analyte: float,
                                C_analyte: float,
                                C_titrant: float,
                                analyte_is_acid: bool = True) -> float:
    """
    Calculate pH during strong acid-strong base titration.
    
    Args:
        V_titrant: Volume of titrant added (L)
        V_analyte: Initial volume of analyte (L)
        C_analyte: Concentration of analyte (M)
        C_titrant: Concentration of titrant (M)
        analyte_is_acid: True if analyte is acid
    
    Returns:
        pH value
    
    Examples:
        >>> titration_pH_strong_strong(0, 0.025, 0.1, 0.1)
        1.0
    """
    mol_analyte = C_analyte * V_analyte
    mol_titrant = C_titrant * V_titrant
    V_total = V_analyte + V_titrant
    
    if analyte_is_acid:
        mol_H = mol_analyte - mol_titrant
        if mol_H > 0:
            return -log10(mol_H / V_total)
        elif mol_H < 0:
            pOH = -log10(-mol_H / V_total)
            return 14 - pOH
        else:
            return 7.0  # Equivalence point
    else:
        mol_OH = mol_analyte - mol_titrant
        if mol_OH > 0:
            pOH = -log10(mol_OH / V_total)
            return 14 - pOH
        elif mol_OH < 0:
            return -log10(-mol_OH / V_total)
        else:
            return 7.0


def half_equivalence_pH(pKa: float) -> float:
    """
    pH at half-equivalence point equals pKa.
    
    Args:
        pKa: Acid pKa
    
    Returns:
        pH at half-equivalence
    
    Examples:
        >>> half_equivalence_pH(4.74)
        4.74
    """
    return pKa


def equivalence_pH_weak_acid(V_analyte: float,
                              C_analyte: float,
                              Ka: float) -> float:
    """
    Calculate pH at equivalence point of weak acid + strong base.
    
    At equivalence, solution contains conjugate base.
    
    Args:
        V_analyte: Volume of analyte (L)
        C_analyte: Initial concentration of weak acid (M)
        Ka: Acid dissociation constant
    
    Returns:
        pH at equivalence
    
    Examples:
        >>> equivalence_pH_weak_acid(0.025, 0.1, 1.8e-5)
        8.72
    """
    # [A-] at equivalence = original acid concentration (diluted)
    Kb = 1.0e-14 / Ka
    
    # For weak base: [OH-] = sqrt(Kb x [A-])
    oh_conc = sqrt(Kb * C_analyte)
    pOH = -log10(oh_conc)
    
    return 14.0 - pOH


def indicator_range(indicator: str) -> Tuple[float, float]:
    """
    Return pH range for common indicators.
    
    Args:
        indicator: Indicator name
    
    Returns:
        (min_pH, max_pH) tuple
    
    Examples:
        >>> indicator_range('phenolphthalein')
        (8.2, 10.0)
    """
    indicators = {
        'methyl_orange': (3.1, 4.4),
        'bromocresol_green': (3.8, 5.4),
        'litmus': (4.5, 8.3),
        'phenol_red': (6.4, 8.0),
        'phenolphthalein': (8.2, 10.0),
        'thymolphthalein': (9.3, 10.5),
    }
    return indicators.get(indicator.lower().replace(' ', '_'), (None, None))


def select_indicator(equivalence_pH: float) -> str:
    """
    Select appropriate indicator for titration.
    
    Args:
        equivalence_pH: pH at equivalence point
    
    Returns:
        Best indicator name
    
    Examples:
        >>> select_indicator(8.7)
        'phenolphthalein'
    """
    if equivalence_pH < 5:
        return 'methyl_orange'
    elif equivalence_pH < 7:
        return 'bromocresol_green'
    elif equivalence_pH < 8:
        return 'phenol_red'
    elif equivalence_pH < 10:
        return 'phenolphthalein'
    else:
        return 'thymolphthalein'


def titration_curve_points(V_analyte: float, C_acid: float,
                            C_base: float, Ka: float = None,
                            is_weak_acid: bool = False) -> Dict:
    """
    Generate key points for titration curve.
    
    Args:
        V_analyte: Volume of acid (L)
        C_acid: Acid concentration (M)
        C_base: Base concentration (M)
        Ka: Acid dissociation constant (for weak acid)
        is_weak_acid: True if acid is weak
    
    Returns:
        Dict with key volumes and pH values
    """
    mol_acid = C_acid * V_analyte
    V_eq = mol_acid / C_base
    
    points = {
        'initial_V': 0,
        'half_eq_V': V_eq / 2,
        'equivalence_V': V_eq,
        'double_eq_V': V_eq * 2,
    }
    
    if is_weak_acid and Ka:
        pKa = -log10(Ka)
        points['initial_pH'] = -log10(sqrt(Ka * C_acid))
        points['half_eq_pH'] = pKa
        points['equivalence_pH'] = equivalence_pH_weak_acid(V_analyte, C_acid, Ka)
    else:
        points['initial_pH'] = -log10(C_acid)
        points['half_eq_pH'] = None  # No special meaning for strong
        points['equivalence_pH'] = 7.0
    
    return points


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="equivalence_pH_weak_acid",
            description="Calculate pH at equivalence point of weak acid + strong base.",
            input_schema=[
            InputSchemaField(name="V_analyte", type="number", required=True),
            InputSchemaField(name="C_analyte", type="number", required=True),
            InputSchemaField(name="Ka", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="equivalence_volume",
            description="Calculate volume of titrant at equivalence point.",
            input_schema=[
            InputSchemaField(name="analyte_mol", type="number", required=True),
            InputSchemaField(name="titrant_conc", type="number", required=True),
            InputSchemaField(name="stoichiometry", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="half_equivalence_pH",
            description="pH at half-equivalence point equals pKa.",
            input_schema=[
            InputSchemaField(name="pKa", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="indicator_range",
            description="Return pH range for common indicators.",
            input_schema=[
            InputSchemaField(name="indicator", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="select_indicator",
            description="Select appropriate indicator for titration.",
            input_schema=[
            InputSchemaField(name="equivalence_pH", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="titration_curve_points",
            description="Generate key points for titration curve.",
            input_schema=[
            InputSchemaField(name="V_analyte", type="number", required=True),
            InputSchemaField(name="C_acid", type="string", required=True),
            InputSchemaField(name="C_base", type="string", required=True),
            InputSchemaField(name="Ka", type="number", required=False),
            InputSchemaField(name="is_weak_acid", type="boolean", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="titration_pH_strong_strong",
            description="Calculate pH during strong acid-strong base titration.",
            input_schema=[
            InputSchemaField(name="V_titrant", type="number", required=True),
            InputSchemaField(name="V_analyte", type="number", required=True),
            InputSchemaField(name="C_analyte", type="number", required=True),
            InputSchemaField(name="C_titrant", type="number", required=True),
            InputSchemaField(name="analyte_is_acid", type="string", required=False)
            ],
            handler="{name}",
        )
    ]
