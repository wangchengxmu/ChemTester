"""
Medicinal Chemistry Tools - L3 Implementation
Functions for drug discovery, pharmacokinetics, pharmacodynamics, and drug-likeness analysis.

## Solver Instructions (for AI Agent)

When you encounter medicinal chemistry problems (drug-likeness, PK/PD, enzyme inhibition), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given molecular properties (MW, logP, HBD, HBA) -> check Lipinski's Rule of Five?
- Given absorption and metabolism fractions -> calculate bioavailability?
- Given clearance and volume of distribution -> calculate half-life?
- Given IC50 and substrate concentration -> convert to Kᵢ?
- Given dose and volume -> calculate concentration?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Lipinski Rule of Five | `lipinski_check(mw, logp, hbd, hba)` | MW≤500, logP≤5, HBD≤5, HBA≤10 |
| Bioavailability | `bioavailability_calc(f_abs, f_gut, f_hepatic)` | F = f_abs x f_gut x f_hepatic |
| Half-life | `half_life_from_clearance(cl, vd)` | t½ = 0.693 x Vd / CL |
| IC50 to Kᵢ | `ic50_to_ki(ic50, substrate_conc, km)` | Cheng-Prusoff: Kᵢ = IC50/(1+[S]/Km) |
| Concentration | `dose_to_concentration(dose_mg, vd_L, mw)` | C = dose / (Vd x MW) |
| vd_from_halflife | `vd_from_halflife(t_half, cl)` | Vd = t½ x CL / 0.693 |

### Step 3: Handle special cases
- Lipinski: Passes if ≤1 violation (not zero)
- Half-life: CL must be positive (raises ValueError otherwise)
- IC50 to Kᵢ: Valid only for competitive inhibition

### Examples
```python
# Example 1: Lipinski check for aspirin-like compound
lipinski_check(180, 1.2, 1, 3)
# -> {'passes': True, 'violations': 0, 'details': [...]}

# Example 2: Oral bioavailability
bioavailability_calc(0.8, 1.0, 0.7)
# -> 0.56 (56% bioavailable)

# Example 3: Elimination half-life
half_life_from_clearance(10, 50)  # CL=10 L/h, Vd=50 L
# -> 3.465 hours

# Example 4: IC50 to Kᵢ (competitive inhibitor)
ic50_to_ki(50, 10, 5)  # IC50=50 nM, [S]=10 nM, Km=5 nM
# -> Kᵢ = 16.67 nM
```
"""

from typing import Dict, List, Tuple, Optional
from math import log10, log


def lipinski_check(mw: float, logp: float, hbd: int, hba: int) -> Dict[str, object]:
    """
    Evaluate Lipinski's Rule of Five for drug-likeness.

    Args:
        mw: Molecular weight (Da)
        logp: Octanol-water partition coefficient
        hbd: Number of hydrogen bond donors (OH + NH)
        hba: Number of hydrogen bond acceptors (N + O)

    Returns:
        Dict with pass/fail status and details.

    Examples:
        >>> lipinski_check(300, 2.5, 2, 5)
        {'passes': True, 'violations': 0, 'details': [...]}
    """
    checks = [
        ("MW ≤ 500", mw <= 500),
        ("logP ≤ 5", logp <= 5),
        ("HBD ≤ 5", hbd <= 5),
        ("HBA ≤ 10", hba <= 10),
    ]
    details = [(name, ok, val) for (name, ok), val in zip(checks, [mw, logp, hbd, hba])]
    violations = sum(1 for _, ok, _ in details if not ok)
    return {
        "passes": violations <= 1,
        "violations": violations,
        "details": [(name, ok, val) for name, ok, val in details],
    }


def bioavailability_calc(f_abs: float, f_gut: float = 1.0, f_hepatic: float = 1.0) -> float:
    """
    Calculate overall oral bioavailability.

    F = f_absorption x f_gut_wall x f_hepatic

    Args:
        f_abs: Fraction absorbed from GI tract (0-1)
        f_gut: Fraction escaping gut wall metabolism (default 1)
        f_hepatic: Fraction escaping hepatic first-pass (default 1)

    Returns:
        Overall bioavailability fraction (0-1).

    Examples:
        >>> bioavailability_calc(0.8, 1.0, 0.7)
        0.56
    """
    return f_abs * f_gut * f_hepatic


def half_life_from_clearance(cl: float, vd: float) -> float:
    """
    Calculate elimination half-life from clearance and volume of distribution.

    t½ = 0.693 x Vd / CL

    Args:
        cl: Clearance (L/h)
        vd: Volume of distribution (L)

    Returns:
        Half-life in hours.

    Examples:
        >>> half_life_from_clearance(10, 50)
        3.465
    """
    if cl <= 0:
        raise ValueError("Clearance must be positive")
    return 0.693 * vd / cl


def ic50_to_ki(ic50: float, substrate_conc: float, km: float) -> float:
    """
    Convert IC50 to Ki using the Cheng-Prusoff equation.

    Ki = IC50 / (1 + [S]/Km)

    Valid for competitive inhibition.

    Args:
        ic50: IC50 value (same units as Ki)
        substrate_conc: [S] substrate concentration
        km: Michaelis constant Km

    Returns:
        Ki value (same units as IC50).

    Examples:
        >>> ic50_to_ki(100, 50, 25)  # nM
        33.333
    """
    return ic50 / (1 + substrate_conc / km)


def pk_parameters(dose: float, auc: float, f: float = 1.0,
                  c0: float = None, tau: float = None) -> Dict[str, float]:
    """
    Calculate core PK parameters.

    CL = F x Dose / AUC
    Vd = CL / k_elim  (if C0 given)
    t½ = 0.693 x Vd / CL  (if C0 given)
    Css_avg = F x Dose / (τ x CL)  (if τ given)

    Args:
        dose: Administered dose (mg)
        auc: Area under curve (mg·h/L)
        f: Bioavailability fraction (default 1.0)
        c0: Initial plasma concentration (mg/L), optional
        tau: Dosing interval (h), optional

    Returns:
        Dict of calculated PK parameters.

    Examples:
        >>> pk_parameters(500, 50)
        {'CL': 10.0}
    """
    if auc <= 0:
        raise ValueError("AUC must be positive")
    cl = f * dose / auc
    result = {"CL": cl}
    if c0 is not None and c0 > 0:
        k_elim = cl / (dose / c0)  # k = CL / Vd, Vd = Dose/C0
        vd = dose / c0
        t_half = 0.693 / k_elim
        result.update({"Vd": vd, "k_elim": k_elim, "t_half": t_half})
    if tau is not None and tau > 0:
        css_avg = f * dose / (tau * cl)
        result["Css_avg"] = css_avg
    return result


def hill_response(conc: float, ec50: float, emax: float = 100,
                  emin: float = 0, hill_slope: float = 1.0) -> float:
    """
    Calculate response using the Hill equation.

    E = E_bottom + (E_top - E_bottom) / (1 + (EC50/[A])^nH)

    Args:
        conc: Ligand/drug concentration
        ec50: EC50 concentration
        emax: Maximum response (default 100)
        emin: Minimum response (default 0)
        hill_slope: Hill coefficient (default 1.0)

    Returns:
        Calculated response.
    """
    return emin + (emax - emin) / (1 + (ec50 / conc) ** hill_slope)


def therapeutic_index(td50: float, ed50: float) -> float:
    """Calculate therapeutic index: TD50/ED50."""
    return td50 / ed50


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="bioavailability_calc",
            description="Calculate overall oral bioavailability.",
            input_schema=[
            InputSchemaField(name="f_abs", type="number", required=True),
            InputSchemaField(name="f_gut", type="number", required=False),
            InputSchemaField(name="f_hepatic", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="half_life_from_clearance",
            description="Calculate elimination half-life from clearance and volume of distribution.",
            input_schema=[
            InputSchemaField(name="cl", type="number", required=True),
            InputSchemaField(name="vd", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="hill_response",
            description="Calculate response using the Hill equation.",
            input_schema=[
            InputSchemaField(name="conc", type="number", required=True),
            InputSchemaField(name="ec50", type="number", required=True),
            InputSchemaField(name="emax", type="number", required=False),
            InputSchemaField(name="emin", type="number", required=False),
            InputSchemaField(name="hill_slope", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ic50_to_ki",
            description="Convert IC50 to Ki using the Cheng-Prusoff equation.",
            input_schema=[
            InputSchemaField(name="ic50", type="number", required=True),
            InputSchemaField(name="substrate_conc", type="number", required=True),
            InputSchemaField(name="km", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="lipinski_check",
            description="Evaluate Lipinski's Rule of Five for drug-likeness.",
            input_schema=[
            InputSchemaField(name="mw", type="number", required=True),
            InputSchemaField(name="logp", type="number", required=True),
            InputSchemaField(name="hbd", type="number", required=True),
            InputSchemaField(name="hba", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pk_parameters",
            description="Calculate core PK parameters.",
            input_schema=[
            InputSchemaField(name="dose", type="number", required=True),
            InputSchemaField(name="auc", type="number", required=True),
            InputSchemaField(name="f", type="number", required=False),
            InputSchemaField(name="c0", type="number", required=False),
            InputSchemaField(name="tau", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="therapeutic_index",
            description="Calculate therapeutic index: TD50/ED50.",
            input_schema=[
            InputSchemaField(name="td50", type="number", required=True),
            InputSchemaField(name="ed50", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
