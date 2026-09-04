"""
Supramolecular Chemistry Tools - L3 Implementation
Host-Guest Chemistry, Self-Assembly, MIMs, Catalysis, Crystal Engineering

## Solver Instructions (for AI Agent)

When you encounter supramolecular chemistry problems (host-guest binding, self-assembly, molecular recognition, binding thermodynamics), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Binding constant**: Given DeltaG -> find K; or given K -> find DeltaG; or given DeltaH, DeltaS -> find both
- **Host-guest binding**: Given concentrations and K -> find fraction bound, occupancy
- **Chelate effect**: Compare binding constants for mono- vs multidentate ligands
- **Self-assembly**: Given concentration and K -> predict aggregate formation
- **Cooperativity**: Given binding data -> determine if positive/negative cooperativity (Hill analysis)

### Step 2: Choose the correct function
- `binding_constant_calc(delta_G, delta_H, delta_S, temperature, K, mode)` -> convert between K, DeltaG, DeltaH, DeltaS
  - modes: "G_to_K", "K_to_G", "HS_to_K", "K_to_HS"
- `host_guest_stoichiometry(host_conc, guest_conc, K, stoichiometry, iterations)` -> fraction bound
- `chelate_effect(K_mono, K_bi, K_tri)` -> effective binding enhancement
- `hill_coefficient(binding_data)` -> n_H (cooperativity measure: n>1 positive, n<1 negative, n=1 non-cooperative)
- `binding_thermodynamics_window(delta_H, delta_S_range, T_range)` -> DeltaG(T) over temperature range

### Step 3: Handle special cases
- DeltaG = -RT ln K (at 298 K: DeltaG ~ -5.71 log K in kJ/mol)
- K > 103: strong binding (tight); K ~ 10-3: weak binding
- Entropy-driven binding: DeltaH ~ 0, DeltaS > 0 (hydrophobic effect)
- Enthalpy-driven binding: DeltaH < 0, DeltaS < 0 (hydrogen bonding, electrostatic)
- Stoichiometry: 1:1 most common, but 2:1 (sandwich), 1:2 (cryptands) also occur

### Examples
1. **K from DeltaG**: DeltaG = -34.2 kJ/mol at 298 K
   -> `binding_constant_calc(delta_G=-34.2, mode="G_to_K")` -> K ~ 1.0x106, log K ~ 6.0

2. **DeltaG from K**: K = 108 (very tight binding)
   -> `binding_constant_calc(K=1e8, mode="K_to_G")` -> DeltaG ~ -45.7 kJ/mol

3. **DeltaH and DeltaS from data**: DeltaH = -50 kJ/mol, DeltaS = -50 J/(mol·K)
   -> `binding_constant_calc(delta_H=-50, delta_S=-50, mode="HS_to_K")` -> DeltaG = -50 - 298x(-0.050) = -35.1 kJ/mol, K ~ 5.4x105
   -> Enthalpy-driven (DeltaH < 0, DeltaS < 0, but |DeltaH| > |TDeltaS| so still favorable)
"""

from typing import Dict, Tuple, Optional, List
from math import log10, log, exp


def binding_constant_calc(
    delta_G: float = None,
    delta_H: float = None,
    delta_S: float = None,
    temperature: float = 298.15,
    K: float = None,
    mode: str = "G_to_K"
) -> Dict:
    """
    Convert between thermodynamic parameters and binding constants.

    Args:
        delta_G: Gibbs free energy (kJ/mol)
        delta_H: Enthalpy (kJ/mol)
        delta_S: Entropy (J/(mol·K))
        temperature: Temperature in K
        K: Association constant
        mode: "G_to_K", "K_to_G", "HS_to_K", "K_to_HS"

    Returns:
        Dict with calculated thermodynamic parameters

    Examples:
        >>> binding_constant_calc(K=1e6, mode="K_to_G")
        {'delta_G': -34.22, 'K': 1e6}
        >>> binding_constant_calc(delta_H=-50, delta_S=-50, temperature=298.15, mode="HS_to_K")
    """
    R = 8.314e-3  # kJ/(mol·K)

    result = {}

    if mode == "G_to_K" and delta_G is not None:
        K = exp(-delta_G / (R * temperature))
        result = {"delta_G": delta_G, "K": K, "log_K": log10(K)}

    elif mode == "K_to_G" and K is not None:
        delta_G = -R * temperature * log(K)
        result = {"delta_G": round(delta_G, 2), "K": K, "log_K": log10(K)}

    elif mode == "HS_to_K" and delta_H is not None and delta_S is not None:
        delta_S_kJ = delta_S / 1000  # J to kJ
        delta_G = delta_H - temperature * delta_S_kJ
        K = exp(-delta_G / (R * temperature))
        result = {
            "delta_G": round(delta_G, 2),
            "delta_H": delta_H,
            "delta_S": delta_S,
            "K": K,
            "log_K": log10(K)
        }

    elif mode == "K_to_HS" and K is not None and delta_H is not None:
        delta_G = -R * temperature * log(K)
        delta_S = (delta_H - delta_G) / temperature * 1000  # kJ to J
        result = {
            "delta_G": round(delta_G, 2),
            "delta_H": delta_H,
            "delta_S": round(delta_S, 2),
            "K": K,
            "log_K": log10(K)
        }

    return result


def host_guest_stoichiometry(
    host_conc: float,
    guest_conc: float,
    K: float,
    stoichiometry: int = 1,
    iterations: int = 1000
) -> Dict:
    """
    Calculate equilibrium concentrations for host-guest binding.

    Args:
        host_conc: Total host concentration (M)
        guest_conc: Total guest concentration (M)
        K: Association constant (M^(-n))
        stoichiometry: Guests per host (1:1 = 1, 1:2 = 2, etc.)
        iterations: Number of iterative refinement steps

    Returns:
        Dict with free host, free guest, complex concentration, fraction bound

    Examples:
        >>> host_guest_stoichiometry(1e-3, 1e-3, 1e4)
    """
    H_t = host_conc
    G_t = guest_conc
    H_free = H_t
    G_free = G_t

    for _ in range(iterations):
        # Forward: form complex
        H_bound = min(H_free, G_free / stoichiometry) if stoichiometry > 0 else 0
        reaction = K * (H_free ** stoichiometry) if stoichiometry == 1 else K * H_free * G_free

        # Simple iterative approach for 1:1
        if stoichiometry == 1:
            # [HG] = K * [H][G], [H_t] = [H] + [HG], [G_t] = [G] + [HG]
            # Solve quadratic: K*x2 - (K*(H_t+G_t)+1)*x + K*H_t*G_t = 0
            a = K
            b = -(K * (H_t + G_t) + 1)
            c = K * H_t * G_t
            disc = b**2 - 4*a*c
            if disc >= 0:
                x = (-b - (disc)**0.5) / (2*a)
                x = max(0, min(x, min(H_t, G_t)))
            else:
                x = 0
            H_free = H_t - x
            G_free = G_t - x
            break
        else:
            break

    complex_conc = H_t - H_free
    frac_bound = complex_conc / H_t if H_t > 0 else 0

    return {
        "H_free": H_free,
        "G_free": G_free,
        "HG_complex": complex_conc,
        "fraction_bound": round(frac_bound, 4)
    }


def self_assembly_cmc(
    tail_carbon: int,
    headgroup_area: float,
    temperature: float = 298.15,
    units: str = "M"
) -> Dict:
    """
    Estimate critical micelle concentration using empirical correlations.

    Args:
        tail_carbon: Number of carbon atoms in alkyl chain
        headgroup_area: Headgroup area (Å2)
        temperature: Temperature in K
        units: "M" or "mM"

    Returns:
        Dict with CMC estimate and derived parameters

    Examples:
        >>> self_assembly_cmc(12, 60)
    """
    R = 8.314  # J/(mol·K)
    T = temperature

    # Tail length (Å): ~1.27 Å per CH2
    l_c = 1.27 * (tail_carbon + 1)  # +1 for terminal CH3
    # Tail volume (Å3): ~27 Å3 per CH2 + 54 for CH3
    v_tail = 27 * tail_carbon + 27

    # Packing parameter
    g = v_tail / (headgroup_area * l_c)

    # Aggregate type prediction
    if g < 1/3:
        agg_type = "spherical micelle"
    elif g < 1/2:
        agg_type = "cylindrical micelle"
    elif g < 1:
        agg_type = "vesicle/bilayer"
    else:
        agg_type = "inverted structure"

    # Empirical CMC: log10(CMC/M) ~ a - b*n_c
    # For ionic: a ~ 1.5, b ~ 0.30; for nonionic: a ~ 2.5, b ~ 0.50
    # Use intermediate values for estimation
    log_cmc = 1.8 - 0.35 * tail_carbon  # rough average
    cmc_M = 10**log_cmc

    # Free energy of micellization per chain (approximate)
    delta_G_mic = R * T * log_cmc * 0.001  # convert log10 to ln: multiply by ln(10)

    return {
        "tail_carbons": tail_carbon,
        "tail_length_A": round(l_c, 2),
        "tail_volume_A3": round(v_tail, 1),
        "headgroup_area_A2": headgroup_area,
        "packing_parameter": round(g, 3),
        "aggregate_type": agg_type,
        "CMC_M": cmc_M,
        "CMC_mM": cmc_M * 1000,
        "log_CMC": round(log_cmc, 2),
        "delta_G_micellization_kJ_mol": round(delta_G_mic, 2)
    }


def rotaxane_efficiency(
    with_template_yield: float,
    without_template_yield: float
) -> Dict:
    """
    Calculate template-directed synthesis efficiency for rotaxanes/catenanes.

    Args:
        with_template_yield: Yield (%) with template
        without_template_yield: Yield (%) without template (statistical)

    Returns:
        Dict with template efficiency, amplification factor

    Examples:
        >>> rotaxane_efficiency(72, 22)
    """
    if with_template_yield <= 0:
        return {"error": "Template yield must be positive"}

    amplification = with_template_yield / without_template_yield if without_template_yield > 0 else float('inf')

    return {
        "with_template_yield_pct": with_template_yield,
        "without_template_yield_pct": without_template_yield,
        "template_efficiency_ratio": round(amplification, 2),
        "yield_improvement_pct": round(with_template_yield - without_template_yield, 1),
        "amplification_factor": round(amplification, 2)
    }


def cage_yield_calc(
    aldehyde_conc: float,
    amine_conc: float,
    stoich_aldehyde: int,
    stoich_amine: int,
    observed_yield: float,
    target_mass: float,
    mw_cage: float
) -> Dict:
    """
    Calculate porous organic cage synthesis parameters.

    Args:
        aldehyde_conc: Aldehyde concentration (mM)
        amine_conc: Amine concentration (mM)
        stoich_aldehyde: Aldehyde units per cage
        stoich_amine: Amine units per cage
        observed_yield: Isolated yield (%)
        target_mass: Target cage mass (mg)
        mw_cage: Molecular weight of cage (g/mol)

    Returns:
        Dict with theoretical yield, amount needed, etc.

    Examples:
        >>> cage_yield_calc(10, 15, 4, 6, 65, 100, 2500)
    """
    # Limiting reagent check
    ratio_aldehyde = aldehyde_conc / stoich_aldehyde
    ratio_amine = amine_conc / stoich_amine

    if ratio_aldehyde < ratio_amine:
        limiting = "aldehyde"
        theoretical_mmol = aldehyde_conc * 0.001 / stoich_aldehyde
    else:
        limiting = "amine"
        theoretical_mmol = amine_conc * 0.001 / stoich_amine

    theoretical_mg = theoretical_mmol * mw_cage * 1000
    actual_mg = theoretical_mg * observed_yield / 100
    actual_mmol = actual_mg / (mw_cage * 1000)

    # How much starting material needed for target mass
    mmol_target = target_mass / (mw_cage * 1000) / (observed_yield / 100)

    if limiting == "aldehyde":
        aldehyde_needed = mmol_target * stoich_aldehyde * 1000  # mM equivalent
        amine_needed = mmol_target * stoich_amine * 1000
    else:
        amine_needed = mmol_target * stoich_amine * 1000
        aldehyde_needed = mmol_target * stoich_aldehyde * 1000

    return {
        "limiting_reagent": limiting,
        "theoretical_yield_mg": round(theoretical_mg, 2),
        "actual_yield_mg": round(actual_mg, 2),
        "actual_yield_mmol": round(actual_mmol, 4),
        "observed_yield_pct": observed_yield,
        "for_target_mass_mg": {
            "target": target_mass,
            "aldehyde_needed_mM": round(aldehyde_needed, 2),
            "amine_needed_mM": round(amine_needed, 2)
        }
    }


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="binding_constant_calc",
            description="Convert between thermodynamic parameters and binding constants.",
            input_schema=[
            InputSchemaField(name="delta_G", type="number", required=False),
            InputSchemaField(name="delta_H", type="number", required=False),
            InputSchemaField(name="delta_S", type="number", required=False),
            InputSchemaField(name="temperature", type="number", required=False),
            InputSchemaField(name="K", type="number", required=False),
            InputSchemaField(name="mode", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="cage_yield_calc",
            description="Calculate porous organic cage synthesis parameters.",
            input_schema=[
            InputSchemaField(name="aldehyde_conc", type="number", required=True),
            InputSchemaField(name="amine_conc", type="number", required=True),
            InputSchemaField(name="stoich_aldehyde", type="number", required=True),
            InputSchemaField(name="stoich_amine", type="number", required=True),
            InputSchemaField(name="observed_yield", type="number", required=True),
            InputSchemaField(name="target_mass", type="number", required=True),
            InputSchemaField(name="mw_cage", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="host_guest_stoichiometry",
            description="Calculate equilibrium concentrations for host-guest binding.",
            input_schema=[
            InputSchemaField(name="host_conc", type="number", required=True),
            InputSchemaField(name="guest_conc", type="number", required=True),
            InputSchemaField(name="K", type="number", required=True),
            InputSchemaField(name="stoichiometry", type="number", required=False),
            InputSchemaField(name="iterations", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="rotaxane_efficiency",
            description="Calculate template-directed synthesis efficiency for rotaxanes/catenanes.",
            input_schema=[
            InputSchemaField(name="with_template_yield", type="number", required=True),
            InputSchemaField(name="without_template_yield", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="self_assembly_cmc",
            description="Estimate critical micelle concentration using empirical correlations.",
            input_schema=[
            InputSchemaField(name="tail_carbon", type="number", required=True),
            InputSchemaField(name="headgroup_area", type="number", required=True),
            InputSchemaField(name="temperature", type="number", required=False),
            InputSchemaField(name="units", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
