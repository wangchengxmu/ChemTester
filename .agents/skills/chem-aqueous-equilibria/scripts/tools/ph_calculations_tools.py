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

The concentration arguments to `pH_from_H3O` and `pOH_from_OH` are
equilibrium ion concentrations, not analytical concentrations of a dilute
weak acid or base.

| Scenario | What to do | Function call |
|----------|-----------|---------------|
| Strong acid, find pH | Determine equilibrium [H3O+] after stoichiometry, then pH = -log[H3O+] | `pH_from_H3O(equilibrium_h3o)` |
| Strong base, find pOH | Determine equilibrium [OH-] after stoichiometry, then pOH = -log[OH-] | `pOH_from_OH(equilibrium_oh)` then `pOH_to_pH(pOH)` for pH |
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
from math import isfinite, log10, sqrt
from numbers import Real


# These are approximate educational anchors, not a full IAPWS water-property
# model. They represent dilute water at standard pressure for the supported
# temperatures.
_KW_25C = 1e-14
_KW_100C = 5.6e-13
_NEUTRAL_PH_TOLERANCE = 0.001


def _finite_value(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number")
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be a finite real number")
    return value


def _positive_value(value: float, name: str) -> float:
    value = _finite_value(value, name)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _resolve_pKw(temperature: float = 25.0, Kw: Optional[float] = None) -> float:
    """Resolve pKw using approximate dilute-water standard-pressure anchors."""

    temperature = _finite_value(temperature, "temperature")
    if Kw is not None:
        return -log10(_positive_value(Kw, "Kw"))
    if temperature == 25.0:
        return -log10(_KW_25C)
    if temperature == 100.0:
        return -log10(_KW_100C)
    raise ValueError("Kw is required for temperatures other than 25 C or 100 C")


def _resolve_kw(Kw: Optional[float] = None) -> float:
    if Kw is None:
        return _KW_25C
    return _positive_value(Kw, "Kw")


def _solve_monoprotic_charge_balance(K: float, C: float, Kw: float) -> float:
    """Solve x = C*K/(K+x) + Kw/x on a deterministic physical bracket."""

    K = _positive_value(K, "dissociation constant")
    C = _finite_value(C, "C")
    if C < 0:
        raise ValueError("C must be nonnegative")
    Kw = _positive_value(Kw, "Kw")
    lower = sqrt(Kw)
    if C == 0:
        return lower
    upper = C + lower

    def residual(x: float) -> float:
        return x - C * (K / (K + x)) - Kw / x

    for _ in range(200):
        midpoint = (lower + upper) / 2.0
        if residual(midpoint) > 0:
            upper = midpoint
        else:
            lower = midpoint
    return (lower + upper) / 2.0


def pH_from_H3O(h3o_conc: float) -> float:
    """
    Calculate pH from hydronium ion concentration.

    This ideal concentration-based conversion assumes a unit activity
    coefficient (activity coefficient = 1).
    
    Args:
        h3o_conc: Equilibrium [H3O+] concentration in M, not an
            analytical acid concentration
    
    Returns:
        pH value
    
    Examples:
        >>> pH_from_H3O(1e-7)
        7.0
        >>> pH_from_H3O(0.1)
        1.0
    """
    h3o_conc = _positive_value(h3o_conc, "h3o_conc")
    return -log10(h3o_conc)


def pOH_from_OH(oh_conc: float) -> float:
    """
    Calculate pOH from hydroxide ion concentration.

    This ideal concentration-based conversion assumes a unit activity
    coefficient (activity coefficient = 1).
    
    Args:
        oh_conc: Equilibrium [OH-] concentration in M, not an
            analytical base concentration
    
    Returns:
        pOH value
    
    Examples:
        >>> pOH_from_OH(1e-7)
        7.0
    """
    oh_conc = _positive_value(oh_conc, "oh_conc")
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
    return 10 ** (-_finite_value(pH, "pH"))


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
    return 10 ** (-_finite_value(pOH, "pOH"))


def pH_to_pOH(
    pH: float, temperature: float = 25.0, Kw: Optional[float] = None
) -> float:
    """
    Convert pH to pOH.
    
    Args:
        pH: pH value
        temperature: Temperature in degC
        Kw: Optional water ion product override
    
    Returns:
        pOH value
    
    Examples:
        >>> pH_to_pOH(7.0)
        7.0
    """
    return _resolve_pKw(temperature, Kw) - _finite_value(pH, "pH")


def pOH_to_pH(
    pOH: float, temperature: float = 25.0, Kw: Optional[float] = None
) -> float:
    """
    Convert pOH to pH.
    
    Args:
        pOH: pOH value
        temperature: Temperature in degC
        Kw: Optional water ion product override
    
    Returns:
        pH value
    
    Examples:
        >>> pOH_to_pH(7.0)
        7.0
    """
    return _resolve_pKw(temperature, Kw) - _finite_value(pOH, "pOH")


def classify_by_pH(
    pH: float, temperature: float = 25.0, Kw: Optional[float] = None
) -> str:
    """
    Classify solution by pH value.
    
    Args:
        pH: pH value
        temperature: Temperature in degC
        Kw: Optional water ion product override
    
    Returns:
        Classification string

    Neutral is defined using an explicit +/- 0.001 pH-unit rounding
    tolerance around 0.5*pKw.
    
    Examples:
        >>> classify_by_pH(7.0)
        'neutral'
        >>> classify_by_pH(4.0)
        'acidic'
        >>> classify_by_pH(10.0)
        'basic'
    """
    neutral_pH = 0.5 * _resolve_pKw(temperature, Kw)
    pH = _finite_value(pH, "pH")
    
    if abs(pH - neutral_pH) <= _NEUTRAL_PH_TOLERANCE:
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
        conc: Equilibrium concentration
        sig_figs: Number of significant figures in concentration
    
    Returns:
        pH with correct decimal places
    
    Examples:
        >>> significant_figures_pH(0.10, 2)
        1.00
    """
    conc = _positive_value(conc, "conc")
    if sig_figs < 0:
        raise ValueError("sig_figs must be nonnegative")
    pH = -log10(conc)
    return round(pH, sig_figs)


def weak_acid_pH(
    Ka: float,
    C: float,
    use_quadratic: bool = False,
    Kw: Optional[float] = None,
) -> float:
    """
    Calculate pH of a weak acid solution.
    
    Uses the ideal monoprotic acid charge and mass balance, including water
    autoionization, with unit activity coefficients. ``use_quadratic`` is
    retained for API compatibility as a no-op and does not change the
    water-corrected solve.
    
    Args:
        Ka: Acid dissociation constant
        C: Initial acid concentration (M)
        use_quadratic: Retained for API compatibility; ignored by the
            water-corrected solver
        Kw: Optional water ion product override
    
    Returns:
        pH value
    
    Examples:
        >>> round(weak_acid_pH(1.8e-5, 0.1), 2)  # Acetic acid, dilute
        2.88
        >>> round(weak_acid_pH(0.1995, 0.286), 2)  # Benzenesulfonic acid
        0.8
    """
    del use_quadratic
    H = _solve_monoprotic_charge_balance(Ka, C, _resolve_kw(Kw))
    return -log10(H)


def weak_acid_Ka_from_pH(
    pH: float, C: float, Kw: Optional[float] = None
) -> float:
    """
    Calculate Ka from pH and concentration for a weak acid.
    
    Uses the water-corrected relationship from the monoprotic charge and mass
    balances with unit activity coefficients. The measured pH must be
    feasible for a finite positive Ka.
    
    Args:
        pH: Measured pH of the solution
        C: Initial acid concentration (M)
        Kw: Optional water ion product override
    
    Returns:
        Ka value
    
    Examples:
        >>> round(weak_acid_Ka_from_pH(2.40, 0.01574), 5)  # Salicylic acid
        0.00135
    """
    pH = _finite_value(pH, "pH")
    C = _positive_value(C, "C")
    Kw = _resolve_kw(Kw)
    H = 10**(-pH)
    acid_anion = H - Kw / H
    if acid_anion <= 0 or acid_anion >= C:
        raise ValueError("pH and C are infeasible for a finite positive Ka")
    return H * acid_anion / (C - acid_anion)


def weak_base_pH(
    Kb: float,
    C: float,
    use_quadratic: bool = False,
    Kw: Optional[float] = None,
) -> float:
    """
    Calculate pH of a weak base solution using unit activity coefficients.
    
    Args:
        Kb: Base dissociation constant
        C: Initial base concentration (M)
        use_quadratic: Retained for API compatibility; ignored by the
            water-corrected solver
        Kw: Optional water ion product override
    
    Returns:
        pH value
    
    Examples:
        >>> round(weak_base_pH(1.8e-5, 0.1), 2)  # Ammonia
        11.12
    """
    del use_quadratic
    Kw = _resolve_kw(Kw)
    OH = _solve_monoprotic_charge_balance(Kb, C, Kw)
    return -log10(Kw / OH)


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
