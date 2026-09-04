"""
pH Calculations Tools - L3 Implementation
Chapter 14.2: pH and pOH

## Solver Instructions (for AI Agent)

When you encounter a pH/pOH calculation problem, follow this decision tree:

### Step 1: Identify what is given and what is asked

Read the question carefully and extract:
- Concentration (M) of acid/base
- Whether the acid/base is STRONG (complete ionization) or WEAK (partial ionization, has Ka/Kb)
- Temperature (default 25degC if not specified)
- Whether the answer needs pH, pOH, [H3O+], or [OH-]

### Step 2: Choose the correct function

| Scenario | What to do | Function call |
|----------|-----------|---------------|
| Strong acid, find pH | [H3O+] = concentration, pH = -log[H3O+] | `pH_from_H3O(concentration)` |
| Strong base, find pOH | [OH-] = concentration, pOH = -log[OH-] | `pOH_from_OH(concentration)` then `pOH_to_pH(pOH)` for pH |
| Strong base, find pH | [OH-] = concentration x n(OH per formula) | `pOH_from_OH(conc)` -> `pOH_to_pH(pOH)` |
| Given pH, find [H3O+] | [H3O+] = 10^(-pH) | `H3O_from_pH(pH)` |
| Given pOH, find [OH-] | [OH-] = 10^(-pOH) | `OH_from_pOH(pOH)` |
| Given pH, find pOH | pOH = 14 - pH (at 25degC) | `pH_to_pOH(pH)` |
| Given pOH, find pH | pH = 14 - pOH (at 25degC) | `pOH_to_pH(pOH)` |
| Given Ka, find pKa | pKa = -log(Ka) | `pKa_from_Ka(Ka)` |
| Given pKa, find Ka | Ka = 10^(-pKa) | `Ka_from_pKa(pKa)` |

### Step 3: Handle special cases

- **Diprotic/triprotic acids** (e.g., H2SO4, H3PO4): Only the first dissociation of strong acids is complete.
  For H2SO4: [H3O+] = concentration (first H is strong), second H has Ka.
- **Strong base with multiple OH** (e.g., Ba(OH)2, Ca(OH)2): [OH-] = concentration x number of OH groups.
  For 0.000071 M Ba(OH)2: [OH-] = 2 x 0.000071 = 0.000142, then find pOH, then pH.
- **Temperature**: At non-25degC, pKw != 14. If Kw is given, use pH + pOH = -log(Kw).
- **Significant figures**: pH decimal places = significant figures in the concentration.

### Examples

**Q: Calculate pH and pOH of 0.000259 M HClO4 (strong acid) at 25degC**
-> pH = pH_from_H3O(0.000259) = 3.587
-> pOH = pH_to_pOH(3.587) = 10.413

**Q: Calculate pH and pOH of 0.21 M NaOH at 25degC**
-> pOH = pOH_from_OH(0.21) = 0.678
-> pH = pOH_to_pH(0.678) = 13.322

**Q: Calculate pH and pOH of 0.000071 M Ba(OH)2 at 25degC**
-> [OH-] = 2 x 0.000071 = 0.000142
-> pOH = pOH_from_OH(0.000142) = 3.848
-> pH = pOH_to_pH(3.848) = 10.152

**Q: Find [H3O+] and [OH-] in solution with pH 6.52 at 25degC**
-> [H3O+] = H3O_from_pH(6.52) = 3.02e-7
-> pOH = pH_to_pOH(6.52) = 7.48
-> [OH-] = OH_from_pOH(7.48) = 3.31e-8
"""

from typing import Optional
from math import log, log10


def pH_from_H3O(h3o_conc: float) -> float:
    """
    Calculate pH from hydronium ion concentration.
    
    Args:
        h3o_conc: [H3O+] in M
    
    Returns:
        pH value
    
    Examples:
        >>> pH_from_H3O(1e-7)
        7.0
        >>> pH_from_H3O(0.1)
        1.0
    """
    if h3o_conc <= 0:
        return None
    return -log10(h3o_conc)


def pOH_from_OH(oh_conc: float) -> float:
    """
    Calculate pOH from hydroxide ion concentration.
    
    Args:
        oh_conc: [OH-] in M
    
    Returns:
        pOH value
    
    Examples:
        >>> pOH_from_OH(1e-7)
        7.0
    """
    if oh_conc <= 0:
        return None
    return -log10(oh_conc)


def H3O_from_pH(pH: float) -> float:
    """
    Calculate [H3O+] from pH.
    
    Args:
        pH: pH value
    
    Returns:
        [H3O+] in M
    
    Examples:
        >>> H3O_from_pH(7.0)
        1e-07
    """
    return 10 ** (-pH)


def OH_from_pOH(pOH: float) -> float:
    """
    Calculate [OH-] from pOH.
    
    Args:
        pOH: pOH value
    
    Returns:
        [OH-] in M
    
    Examples:
        >>> OH_from_pOH(7.0)
        1e-07
    """
    return 10 ** (-pOH)


def pH_to_pOH(pH: float, temperature: float = 25.0) -> float:
    """
    Convert pH to pOH.
    
    Args:
        pH: pH value
        temperature: Temperature in degC
    
    Returns:
        pOH value
    
    Examples:
        >>> pH_to_pOH(7.0)
        7.0
    """
    pKw = 14.0 if temperature == 25.0 else -log10(5.6e-13) if temperature == 100.0 else 14.0
    return pKw - pH


def pOH_to_pH(pOH: float, temperature: float = 25.0) -> float:
    """
    Convert pOH to pH.
    
    Args:
        pOH: pOH value
        temperature: Temperature in degC
    
    Returns:
        pH value
    
    Examples:
        >>> pOH_to_pH(7.0)
        7.0
    """
    pKw = 14.0 if temperature == 25.0 else 14.0
    return pKw - pOH


def classify_by_pH(pH: float, temperature: float = 25.0) -> str:
    """
    Classify solution by pH value.
    
    Args:
        pH: pH value
        temperature: Temperature in degC
    
    Returns:
        Classification string
    
    Examples:
        >>> classify_by_pH(7.0)
        'neutral'
        >>> classify_by_pH(4.0)
        'acidic'
        >>> classify_by_pH(10.0)
        'basic'
    """
    neutral_pH = 7.0 if temperature == 25.0 else 6.31 if temperature == 80.0 else 7.0
    
    if abs(pH - neutral_pH) < 0.1:
        return 'neutral'
    elif pH < neutral_pH:
        return 'acidic'
    else:
        return 'basic'


def pKa_from_Ka(Ka: float) -> float:
    """
    Calculate pKa from Ka.
    
    Args:
        Ka: Acid dissociation constant
    
    Returns:
        pKa value
    
    Examples:
        >>> pKa_from_Ka(1.8e-5)
        4.74
    """
    return -log10(Ka)


def Ka_from_pKa(pKa: float) -> float:
    """
    Calculate Ka from pKa.
    
    Args:
        pKa: pKa value
    
    Returns:
        Ka value
    
    Examples:
        >>> Ka_from_pKa(4.74)
        1.8e-05
    """
    return 10 ** (-pKa)


def pKb_from_Kb(Kb: float) -> float:
    """
    Calculate pKb from Kb.
    
    Args:
        Kb: Base dissociation constant
    
    Returns:
        pKb value
    
    Examples:
        >>> pKb_from_Kb(1.8e-5)
        4.74
    """
    return -log10(Kb)


def Kb_from_pKb(pKb: float) -> float:
    """
    Calculate Kb from pKb.
    
    Args:
        pKb: pKb value
    
    Returns:
        Kb value
    
    Examples:
        >>> Kb_from_pKb(4.74)
        1.8e-05
    """
    return 10 ** (-pKb)


def significant_figures_pH(conc: float, sig_figs: int = 2) -> float:
    """
    Report pH with appropriate significant figures.
    
    Args:
        conc: Concentration
        sig_figs: Number of significant figures in concentration
    
    Returns:
        pH with correct decimal places
    
    Examples:
        >>> significant_figures_pH(0.10, 2)
        1.00
    """
    pH = -log10(conc)
    return round(pH, sig_figs)


def weak_acid_pH(Ka: float, C: float, use_quadratic: bool = False) -> float:
    """
    Calculate pH of a weak acid solution.
    
    Uses the appropriate method based on the C/Ka ratio:
    - If C/Ka > 400 and not use_quadratic: uses approximation [H+] = sqrt(Ka * C)
    - Otherwise: uses exact quadratic solution
    
    Args:
        Ka: Acid dissociation constant
        C: Initial acid concentration (M)
        use_quadratic: Force use of quadratic solution
    
    Returns:
        pH value
    
    Examples:
        >>> weak_acid_pH(1.8e-5, 0.1)  # Acetic acid, dilute
        2.87
        >>> weak_acid_pH(0.1995, 0.286)  # Benzenesulfonic acid, concentrated
        0.80
    """
    from math import sqrt
    
    Kw = 1e-14  # at 25°C
    
    # Check if approximation is valid
    # Approximation is valid when C/Ka > 400 (dissociation < 5%)
    ratio = C / Ka
    
    if ratio > 400 and not use_quadratic:
        # Use approximation: [H+] = sqrt(Ka * C)
        H = sqrt(Ka * C)
        # For very dilute acids, account for water autoionization
        if H < 1e-6:
            H = sqrt(Ka * C + Kw)
    else:
        # Use exact quadratic solution
        # Ka = [H+]^2 / (C - [H+])
        # [H+]^2 + Ka*[H+] - Ka*C = 0
        # Using quadratic formula: [H+] = (-Ka + sqrt(Ka^2 + 4*Ka*C)) / 2
        discriminant = Ka**2 + 4 * Ka * C
        H = (-Ka + sqrt(discriminant)) / 2
    
    return -log10(H)


def weak_acid_Ka_from_pH(pH: float, C: float) -> float:
    """
    Calculate Ka from pH and concentration for a weak acid.
    
    Uses the relationship: Ka = [H+]^2 / (C - [H+])
    
    Args:
        pH: Measured pH of the solution
        C: Initial acid concentration (M)
    
    Returns:
        Ka value
    
    Examples:
        >>> weak_acid_Ka_from_pH(2.40, 0.01574)  # Salicylic acid
        1.01e-3
    """
    H = 10**(-pH)
    Ka = H**2 / (C - H)
    return Ka


def weak_base_pH(Kb: float, C: float, use_quadratic: bool = False) -> float:
    """
    Calculate pH of a weak base solution.
    
    Args:
        Kb: Base dissociation constant
        C: Initial base concentration (M)
        use_quadratic: Force use of quadratic solution
    
    Returns:
        pH value
    
    Examples:
        >>> weak_base_pH(1.8e-5, 0.1)  # Ammonia
        11.13
    """
    from math import sqrt
    
    ratio = C / Kb
    
    if ratio > 400 and not use_quadratic:
        OH = sqrt(Kb * C)
    else:
        discriminant = Kb**2 + 4 * Kb * C
        OH = (-Kb + sqrt(discriminant)) / 2
    
    pOH = -log10(OH)
    return 14.0 - pOH


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="H3O_from_pH",
            description="Calculate [H3O+] from pH.",
            input_schema=[
            InputSchemaField(name="pH", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="Ka_from_pKa",
            description="Calculate Ka from pKa.",
            input_schema=[
            InputSchemaField(name="pKa", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="Kb_from_pKb",
            description="Calculate Kb from pKb.",
            input_schema=[
            InputSchemaField(name="pKb", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="OH_from_pOH",
            description="Calculate [OH-] from pOH.",
            input_schema=[
            InputSchemaField(name="pOH", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="classify_by_pH",
            description="Classify solution by pH value.",
            input_schema=[
            InputSchemaField(name="pH", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pH_from_H3O",
            description="Calculate pH from hydronium ion concentration.",
            input_schema=[
            InputSchemaField(name="h3o_conc", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pH_to_pOH",
            description="Convert pH to pOH.",
            input_schema=[
            InputSchemaField(name="pH", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pKa_from_Ka",
            description="Calculate pKa from Ka.",
            input_schema=[
            InputSchemaField(name="Ka", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pKb_from_Kb",
            description="Calculate pKb from Kb.",
            input_schema=[
            InputSchemaField(name="Kb", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pOH_from_OH",
            description="Calculate pOH from hydroxide ion concentration.",
            input_schema=[
            InputSchemaField(name="oh_conc", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pOH_to_pH",
            description="Convert pOH to pH.",
            input_schema=[
            InputSchemaField(name="pOH", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="significant_figures_pH",
            description="Report pH with appropriate significant figures.",
            input_schema=[
            InputSchemaField(name="conc", type="number", required=True),
            InputSchemaField(name="sig_figs", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
