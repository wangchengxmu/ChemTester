"""
Polymer Chemistry Calculation Tools.

Provides MCP-style tools for:
- Degree of polymerization
- Molecular weight from DP
- Number-average molecular weight
- Weight-average molecular weight
- Polydispersity index
- Copolymer composition (Mayo-Lewis)
- Glass transition temperature (Fox equation)

## Solver Instructions (for AI Agent)

When you encounter polymer chemistry problems (MW, PDI, Tg, copolymer), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given monomer and polymer MW -> calculate degree of polymerization?
- Given moles and MW fractions -> calculate Mn or Mw?
- Given Mw and Mn -> calculate PDI?
- Given feed composition and reactivity ratios -> calculate copolymer composition?
- Given homopolymer Tg values -> calculate copolymer Tg (Fox equation)?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Degree of polymerization | `degree_of_polymerization(monomer_mw, polymer_mw)` | DP = M_polymer/M_monomer |
| MW from DP | `molecular_weight_from_dp(dp, monomer_mw)` | M = DP x M_monomer |
| Number-average MW | `number_avg_mw(moles, molecular_weights)` | Mn = ΣnᵢMᵢ/Σnᵢ |
| Weight-average MW | `weight_avg_mw(moles, molecular_weights)` | Mw = ΣwᵢMᵢ |
| Polydispersity index | `polydispersity_index(Mw, Mn)` | PDI = Mw/Mn |
| Copolymer composition | `copolymer_composition(f1, r1, r2)` | Mayo-Lewis equation |
| Fox equation Tg | `fox_equation(w1, Tg1, w2, Tg2)` | 1/Tg = w1/Tg1 + w2/Tg2 |

### Step 3: Handle special cases
- PDI near 1: narrow distribution (living polymerization)
- PDI ~2: most probable distribution (step-growth)
- Mayo-Lewis: r1 x r2 ~ 1 for ideal copolymerization
- Fox equation: for random copolymers; block copolymers may show two Tg's

### Examples
```python
# Example 1: Degree of polymerization
degree_of_polymerization(28, 28000)  # PE: monomer=28, polymer=28000
# -> 1000

# Example 2: Number-average MW
number_avg_mw([1, 2, 1], [10000, 20000, 30000])
# -> 20000 g/mol

# Example 3: Copolymer composition
copolymer_composition(0.5, 0.5, 0.5)  # f1=0.5, r1=r2=0.5
# -> F1 ~ 0.5 (azeotropic)

# Example 4: Fox equation for Tg
fox_equation(0.5, 373, 0.5, 273)  # 50/50 blend of Tg=100degC and Tg=0degC
# -> Tg ~ 311 K (38degC)
```
"""

import math
from typing import Optional


MCP_TOOLS = [
    {
        "name": "degree_of_polymerization",
        "description": "Calculate degree of polymerization (DP) from monomer and polymer molecular weights: DP = M_polymer / M_monomer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "monomer_mw": {"type": "number", "description": "Molecular weight of monomer (g/mol)"},
                "polymer_mw": {"type": "number", "description": "Molecular weight of polymer (g/mol)"}
            },
            "required": ["monomer_mw", "polymer_mw"]
        },
        "returns": {"type": "number", "description": "Degree of polymerization DP"},
        "examples": [
            {"input": {"monomer_mw": 28, "polymer_mw": 28000}, "output": 1000, "note": "Polyethylene"}
        ]
    },
    {
        "name": "molecular_weight_from_dp",
        "description": "Calculate polymer molecular weight from degree of polymerization: M = DP x M_monomer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dp": {"type": "number", "description": "Degree of polymerization"},
                "monomer_mw": {"type": "number", "description": "Molecular weight of monomer (g/mol)"}
            },
            "required": ["dp", "monomer_mw"]
        },
        "returns": {"type": "number", "description": "Polymer molecular weight in g/mol"}
    },
    {
        "name": "number_avg_mw",
        "description": "Calculate number-average molecular weight: Mn = Σ(ni x Mi) / Σ(ni).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {"type": "array", "items": {"type": "number"}, "description": "List of mole amounts (ni)"},
                "molecular_weights": {"type": "array", "items": {"type": "number"}, "description": "List of molecular weights (Mi) for each fraction"}
            },
            "required": ["moles", "molecular_weights"]
        },
        "returns": {"type": "number", "description": "Number-average molecular weight Mn (g/mol)"}
    },
    {
        "name": "weight_avg_mw",
        "description": "Calculate weight-average molecular weight: Mw = Σ(wi x Mi) where wi = nixMi / Σ(nixMi).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "moles": {"type": "array", "items": {"type": "number"}, "description": "List of mole amounts (ni)"},
                "molecular_weights": {"type": "array", "items": {"type": "number"}, "description": "List of molecular weights (Mi) for each fraction"}
            },
            "required": ["moles", "molecular_weights"]
        },
        "returns": {"type": "number", "description": "Weight-average molecular weight Mw (g/mol)"}
    },
    {
        "name": "polydispersity_index",
        "description": "Calculate polydispersity index (PDI) = Mw / Mn. Values near 1 indicate narrow distribution; typical step-growth ~2, chain-growth ~5-20.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Mw": {"type": "number", "description": "Weight-average molecular weight (g/mol)"},
                "Mn": {"type": "number", "description": "Number-average molecular weight (g/mol)"}
            },
            "required": ["Mw", "Mn"]
        },
        "returns": {"type": "number", "description": "Polydispersity index (PDI)"},
        "examples": [
            {"input": {"Mw": 200000, "Mn": 100000}, "output": 2.0, "note": "Typical step-growth PDI"}
        ]
    },
    {
        "name": "copolymer_composition",
        "description": "Calculate instantaneous copolymer composition using the Mayo-Lewis equation: F1 = (r1xf12 + f1xf2) / (r1xf12 + 2xf1xf2 + r2xf22).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "f1": {"type": "number", "description": "Mole fraction of monomer 1 in feed"},
                "r1": {"type": "number", "description": "Reactivity ratio of monomer 1"},
                "r2": {"type": "number", "description": "Reactivity ratio of monomer 2"}
            },
            "required": ["f1", "r1", "r2"]
        },
        "returns": {"type": "object", "description": "{'F1': float, 'F2': float} copolymer mole fractions"}
    },
    {
        "name": "glass_transition_temperature",
        "description": "Estimate glass transition temperature of a polymer blend or copolymer using the Fox equation: 1/Tg = w1/Tg1 + w2/Tg2.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "Tg1": {"type": "number", "description": "Glass transition of component 1 in K"},
                "w1": {"type": "number", "description": "Weight fraction of component 1"},
                "Tg2": {"type": "number", "description": "Glass transition of component 2 in K"},
                "Tg_more": {"type": "array", "items": {"type": "number"}, "description": "Additional Tg values in K (optional)"},
                "w_more": {"type": "array", "items": {"type": "number"}, "description": "Additional weight fractions (optional)"}
            },
            "required": ["Tg1", "w1", "Tg2"]
        },
        "returns": {"type": "number", "description": "Glass transition temperature in K"}
    }
]


# =============================================================================
# IMPLEMENTATIONS
# =============================================================================


def degree_of_polymerization(monomer_mw: float, polymer_mw: float) -> dict:
    """
    Calculate degree of polymerization: DP = M_polymer / M_monomer.
    
    Args:
        monomer_mw: Molecular weight of monomer (g/mol)
        polymer_mw: Molecular weight of polymer (g/mol)
    
    Returns:
        {'dp': float, 'monomer_mw': float, 'polymer_mw': float}
    
    Raises:
        ValueError: If monomer_mw <= 0 or polymer_mw <= 0
    """
    if monomer_mw <= 0:
        raise ValueError("Monomer molecular weight must be positive")
    if polymer_mw <= 0:
        raise ValueError("Polymer molecular weight must be positive")
    
    dp = polymer_mw / monomer_mw
    return {
        'dp': round(dp),
        'monomer_mw': monomer_mw,
        'polymer_mw': polymer_mw
    }


def molecular_weight_from_dp(dp: float, monomer_mw: float) -> float:
    """
    Calculate polymer molecular weight: M = DP x M_monomer.
    
    Args:
        dp: Degree of polymerization
        monomer_mw: Molecular weight of monomer (g/mol)
    
    Returns:
        Polymer molecular weight in g/mol
    
    Raises:
        ValueError: If dp <= 0 or monomer_mw <= 0
    """
    if dp <= 0:
        raise ValueError("Degree of polymerization must be positive")
    if monomer_mw <= 0:
        raise ValueError("Monomer molecular weight must be positive")
    
    return dp * monomer_mw


def number_avg_mw(moles: list, molecular_weights: list) -> float:
    """
    Calculate number-average molecular weight: Mn = Σ(ni x Mi) / Σ(ni).
    
    Args:
        moles: List of mole amounts
        molecular_weights: List of molecular weights for each fraction
    
    Returns:
        Mn in g/mol
    
    Raises:
        ValueError: If lists are empty, mismatched, or all moles are zero
    """
    if len(moles) != len(molecular_weights):
        raise ValueError("moles and molecular_weights must have same length")
    if len(moles) == 0:
        raise ValueError("Lists must not be empty")
    
    total_mass = sum(n * m for n, m in zip(moles, molecular_weights))
    total_moles = sum(moles)
    
    if total_moles == 0:
        raise ValueError("Total moles cannot be zero")
    
    return total_mass / total_moles


def weight_avg_mw(moles: list, molecular_weights: list) -> float:
    """
    Calculate weight-average molecular weight: Mw = Σ(wi x Mi).
    
    Where wi = ni x Mi / Σ(ni x Mi)
    
    Args:
        moles: List of mole amounts
        molecular_weights: List of molecular weights for each fraction
    
    Returns:
        Mw in g/mol
    
    Raises:
        ValueError: If lists are empty, mismatched, or all masses are zero
    """
    if len(moles) != len(molecular_weights):
        raise ValueError("moles and molecular_weights must have same length")
    if len(moles) == 0:
        raise ValueError("Lists must not be empty")
    
    total_mass = sum(n * m for n, m in zip(moles, molecular_weights))
    
    if total_mass == 0:
        raise ValueError("Total mass cannot be zero")
    
    return sum(n * m * m for n, m in zip(moles, molecular_weights)) / total_mass


def polydispersity_index(Mw: float, Mn: float) -> float:
    """
    Calculate polydispersity index: PDI = Mw / Mn.
    
    Args:
        Mw: Weight-average molecular weight (g/mol)
        Mn: Number-average molecular weight (g/mol)
    
    Returns:
        PDI (dimensionless)
    
    Raises:
        ValueError: If Mn <= 0 or Mw < 0
    """
    if Mn <= 0:
        raise ValueError("Mn must be positive")
    if Mw < 0:
        raise ValueError("Mw must be non-negative")
    
    return Mw / Mn


def copolymer_composition(f1: float, r1: float, r2: float) -> dict:
    """
    Calculate instantaneous copolymer composition using Mayo-Lewis equation.
    
    F1 = (r1xf12 + f1xf2) / (r1xf12 + 2xf1xf2 + r2xf22)
    
    Args:
        f1: Mole fraction of monomer 1 in feed (0-1)
        r1: Reactivity ratio of monomer 1
        r2: Reactivity ratio of monomer 2
    
    Returns:
        {'F1': float, 'F2': float} copolymer mole fractions
    
    Raises:
        ValueError: If f1 is outside [0, 1]
    """
    if not 0 <= f1 <= 1:
        raise ValueError("f1 must be between 0 and 1")
    
    f2 = 1.0 - f1
    
    numerator = r1 * f1**2 + f1 * f2
    denominator = r1 * f1**2 + 2 * f1 * f2 + r2 * f2**2
    
    if denominator == 0:
        return {'F1': 0.0, 'F2': 1.0}
    
    F1 = numerator / denominator
    F2 = 1.0 - F1
    
    return {'F1': round(F1, 6), 'F2': round(F2, 6)}


def glass_transition_temperature(Tg1: float, w1: float, Tg2: float,
                                 Tg_more: list = None, w_more: list = None) -> float:
    """
    Estimate Tg of blend/copolymer using Fox equation.
    
    1/Tg = Σ(wi/Tgi)
    
    Args:
        Tg1: Glass transition of component 1 in K
        w1: Weight fraction of component 1
        Tg2: Glass transition of component 2 in K
        Tg_more: Additional Tg values in K (optional)
        w_more: Additional weight fractions (optional)
    
    Returns:
        Tg in K
    
    Raises:
        ValueError: If weight fractions don't sum to ~1, or Tg <= 0
    """
    if Tg1 <= 0 or Tg2 <= 0:
        raise ValueError("Tg values must be positive")
    
    tgs = [Tg1, Tg2]
    weights = [w1, 1.0 - w1]
    
    if Tg_more is not None and w_more is not None:
        if len(Tg_more) != len(w_more):
            raise ValueError("Tg_more and w_more must have same length")
        # Recalculate w2 from constraint that all weights sum to 1
        w2 = 1.0 - w1 - sum(w_more)
        weights = [w1, w2] + list(w_more)
        tgs = [Tg1, Tg2] + list(Tg_more)
        for tg in Tg_more:
            if tg <= 0:
                raise ValueError("Tg values must be positive")
    elif Tg_more is not None or w_more is not None:
        raise ValueError("Provide both Tg_more and w_more, or neither")
    
    # Validate weight sum
    total_w = sum(weights)
    if abs(total_w - 1.0) > 1e-6:
        raise ValueError(f"Weight fractions must sum to 1.0, got {total_w}")
    
    inv_Tg = sum(w / tg for w, tg in zip(weights, tgs))
    
    if inv_Tg <= 0:
        raise ValueError("Invalid parameters: resulting Tg is non-physical")
    
    return 1.0 / inv_Tg


def ceiling_temperature(dH_polymerization: float, dS_polymerization: float, 
                        monomer_concentration: float = None, 
                        units: str = 'kJ') -> dict:
    """
    Calculate ceiling temperature (Tc) for chain-growth polymerization.
    
    At equilibrium (Tc): DeltaG = DeltaH - Tc*DeltaS + RTc*ln[M] = 0
    
    So: Tc = DeltaH / (DeltaS - R*ln[M])
    
    For DeltaH < 0 and DeltaS < 0 (typical polymerization):
    - Without [M]: Tc = DeltaH / DeltaS (standard ceiling temperature)
    - With [M]: Tc = DeltaH / (DeltaS + R*ln[M]) - the monomer concentration affects Tc
    
    Above Tc, depolymerization is favored over polymerization.
    
    Args:
        dH_polymerization: Enthalpy change of polymerization
            - If units='kJ': value in kJ/mol (typical)
            - If units='cal': value in cal/mol
        dS_polymerization: Entropy change of polymerization
            - If units='kJ': value in J/(mol*K) (will convert to kJ)
            - If units='cal': value in cal/(mol*K)
        monomer_concentration: Monomer concentration [M] in mol/L (optional)
            - If provided, includes the RTc*ln[M] term
        units: 'kJ' for kJ/mol and J/(mol*K), or 'cal' for cal/mol and cal/(mol*K)
    
    Returns:
        Dictionary with Tc in K and degC
    
    Examples:
        >>> ceiling_temperature(-56, -110)  # kJ/mol and J/(mol*K)
        {'Tc_K': 509.1, 'Tc_C': 235.9, 'dH_kJ': -56, 'dS_J_per_K': -110}
        
        >>> ceiling_temperature(-7000, -8.6, monomer_concentration=8.7, units='cal')
        # dH=-7000 cal/mol, dS=-8.6 cal/(mol*K), [M]=8.7 M, R=1.987 cal/(mol*K)
        # Tc = -7000 / (-8.6 + 1.987*ln(8.7))
        {'Tc_K': ..., 'Tc_C': ...}
    """
    import math
    
    R_kJ = 0.008314  # kJ/(mol*K)
    R_cal = 1.987    # cal/(mol*K)
    
    if units == 'cal':
        # dH in cal/mol, dS in cal/(mol*K)
        dH = dH_polymerization
        dS = dS_polymerization
        R = R_cal
        dH_kJ = dH / 1000.0 * 4.184  # Convert to kJ for output
        dS_J = dS * 4.184  # Convert to J/(mol*K) for output
    else:
        # dH in kJ/mol, dS in J/(mol*K) - convert dS to kJ
        dH = dH_polymerization
        dS = dS_polymerization / 1000.0  # kJ/(mol*K)
        R = R_kJ
        dH_kJ = dH
        dS_J = dS_polymerization
    
    if dS == 0:
        return {'error': 'DeltaS cannot be zero', 'Tc_K': None}
    if dS > 0:
        return {'error': 'DeltaS should be negative for polymerization', 'Tc_K': None}
    
    # Calculate effective entropy term including monomer concentration
    if monomer_concentration is not None and monomer_concentration > 0:
        # Tc = DeltaH / (DeltaS + R*ln[M])
        dS_effective = dS + R * math.log(monomer_concentration)
        if dS_effective == 0:
            return {'error': 'Effective DeltaS is zero (check concentration)', 'Tc_K': None}
        Tc = dH / dS_effective
    else:
        # Simple case: Tc = DeltaH / DeltaS
        Tc = dH / dS
    
    # Both dH and dS_effective should be negative, so Tc is positive
    if Tc < 0:
        return {'error': 'Calculated Tc is negative - check input values', 'Tc_K': None}
    
    Tc_C = Tc - 273.15
    
    result = {
        'Tc_K': round(Tc, 1),
        'Tc_C': round(Tc_C, 1),
        'dH_kJ': round(dH_kJ, 2),
        'dS_J_per_K': round(dS_J, 2),
    }
    
    if monomer_concentration is not None:
        result['monomer_concentration_M'] = monomer_concentration
        result['note'] = 'Tc calculated with monomer concentration term'
    
    return result


def kinetic_chain_length(rp: float, rt: float) -> dict:
    """
    Calculate kinetic chain length (v) = Rp / Rt = rate of propagation / rate of termination.
    
    For steady-state free radical polymerization:
    v = kp[M] / (2 kt [M*]) = Rp / Rt
    
    Args:
        rp: Rate of propagation (mol/(L·s))
        rt: Rate of termination (mol/(L·s))
    
    Returns:
        Dictionary with kinetic chain length
    
    Examples:
        >>> kinetic_chain_length(0.00125, 3.68e-8)
        {'v': 33967, 'Rp': 0.00125, 'Rt': 3.68e-08}
    """
    if rt == 0:
        return {'error': 'Rt cannot be zero', 'v': None}
    
    v = rp / rt
    return {
        'v': round(v),
        'Rp': rp,
        'Rt': rt,
    }


def kinetic_chain_length_from_k(kp: float, kt: float, M_conc: float, M_dot_conc: float) -> dict:
    """
    Calculate kinetic chain length from rate constants and concentrations.
    
    v = kp[M] / (2·kt·[M*]) = Rp / Rt
    
    Args:
        kp: Propagation rate constant (L/(mol·s))
        kt: Termination rate constant (L/(mol·s))
        M_conc: Monomer concentration [M] (mol/L)
        M_dot_conc: Radical concentration [M*] (mol/L)
    
    Returns:
        Dictionary with kinetic chain length
    """
    rp = kp * M_conc * M_dot_conc
    rt = 2 * kt * M_dot_conc ** 2
    
    if rt == 0:
        return {'error': 'Rt is zero', 'v': None}
    
    v = rp / rt
    return {
        'v': round(v),
        'Rp': rp,
        'Rt': rt,
        'formula': 'v = kp[M][M*] / (2·kt·[M*]2) = kp[M] / (2·kt·[M*])'
    }
