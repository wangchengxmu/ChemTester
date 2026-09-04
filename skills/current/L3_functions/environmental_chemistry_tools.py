"""
Environmental chemistry tools: half-life, bioconcentration, hazard quotient,
risk characterization, LC50/LD50 conversion, decay kinetics, COD/BOD, dilution.
## Solver Instructions (for AI Agent)

When you encounter environmental fate/transport, risk, or pollution chemistry problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given k or half-life -> Find the other? Use `half_life(k=..., half_life=...)` (first-order default)
- Given BCF or log_BCF -> Convert? Use `bioconcentration_factor(BCF=...)` or `bioconcentration_factor(log_BCF=...)`
- Given BAF or log_BAF -> Convert? Use `bioaccumulation_factor(BAF=...)` or `bioaccumulation_factor(log_BAF=...)`
- Given exposure, RfD -> Calculate hazard quotient? Use `hazard_quotient(exposure_conc, reference_dose)`
- Given HQ -> Classify risk? Use `risk_characterization(hazard_quotient)`
- Given LC50, body weight -> Approximate LD50? Use `lc50_to_ld50(lc50, body_weight_kg)`
- Given C0, k, t -> Find remaining concentration? Use `decay_concentration(C0, k, t)`
- Given COD, BOD -> Assess biodegradability? Use `cod_bod_ratio(COD, BOD)`
- Given source/receiving water -> Mixing zone concentration? Use `dilution_factor(C_source, Q_source, C_ambient, Q_ambient)`
- Henry's law volatilization? Use `henry_law_volatilization(kh_atm_l_mol, c_water, wind_speed, depth, temperature)`
- BOD kinetics? Use `bod_calc(bod5=..., ultimate_bod=..., k_rate=..., temperature=..., time_days=...)`

### Step 2: Handle special cases
- **HQ interpretation**: < 1 acceptable, 1-10 moderate concern, ≥ 10 high risk
- **COD/BOD ratio**: < 2 highly biodegradable, 2-4 moderate, ≥ 4 low (refractory organics)
- **BCF vs BAF**: BCF = laboratory bioconcentration; BAF = field bioaccumulation (includes dietary uptake)
- **Decay**: First-order; half-life = ln(2)/k
- **Dilution factor**: DF = Q_total/Q_source; higher DF = more dilution

### Examples
```python
# Example 1: Hazard quotient
hazard_quotient(0.005, 0.01)  # HQ = 0.5 -> acceptable

# Example 2: Decay after 30 days (k=0.1/day)
decay_concentration(100, 0.1, 30)  # -> C = 4.98, fraction remaining = 0.050

# Example 3: Dilution
dilution_factor(50, 1, 0, 99)  # C_mix=0.50, DF=100, 1% from source
```
"""

import math
from typing import Optional, Dict


def half_life(k: float = None, half_life: float = None, order: int = 1):
    """Interconvert half-life and rate constant.

    For first-order (default): t½ = ln(2)/k.
    For second-order (order=2): t½ = 1/(k·[A]0) - needs initial concentration, so returns formula note.

    Provide exactly one of k or half_life.
    Returns the other value.
    """
    if k is not None and half_life is None:
        if order == 1:
            return {'half_life': math.log(2) / k, 'k': k, 'order': order}
        else:
            return {'error': f'For order={order}, half-life depends on initial concentration; use the formula directly.'}
    elif half_life is not None and k is None:
        if order == 1:
            return {'k': math.log(2) / half_life, 'half_life': half_life, 'order': order}
        else:
            return {'error': f'For order={order}, k depends on initial concentration; use the formula directly.'}
    elif k is not None and half_life is not None:
        if order == 1:
            expected = math.log(2) / k
            if abs(expected - half_life) < 1e-6:
                return {'k': k, 'half_life': half_life, 'order': order, 'verified': True}
            return {'error': f'Inconsistent: k={k} gives t½={expected:.4g}, not {half_life}'}
        return {'error': 'Provide only one of k or half_life (or both for verification with order=1).'}
    return {'error': 'Provide at least one of k or half_life.'}


def bioconcentration_factor(BCF: float = None, log_BCF: float = None):
    """Interconvert BCF and log10(BCF).

    Provide exactly one of BCF or log_BCF; returns the other.
    """
    if BCF is not None and log_BCF is None:
        if BCF <= 0:
            return {'error': 'BCF must be positive.'}
        return {'BCF': BCF, 'log_BCF': math.log10(BCF)}
    elif log_BCF is not None and BCF is None:
        return {'BCF': 10 ** log_BCF, 'log_BCF': log_BCF}
    elif BCF is not None and log_BCF is not None:
        expected = math.log10(BCF) if BCF > 0 else None
        if expected is not None and abs(expected - log_BCF) < 1e-6:
            return {'BCF': BCF, 'log_BCF': log_BCF, 'verified': True}
        return {'error': f'Inconsistent values.'}
    return {'error': 'Provide BCF or log_BCF.'}


def bioaccumulation_factor(BAF: float = None, log_BAF: float = None):
    """Interconvert BAF and log10(BAF).

    Provide exactly one of BAF or log_BAF; returns the other.
    """
    if BAF is not None and log_BAF is None:
        if BAF <= 0:
            return {'error': 'BAF must be positive.'}
        return {'BAF': BAF, 'log_BAF': math.log10(BAF)}
    elif log_BAF is not None and BAF is None:
        return {'BAF': 10 ** log_BAF, 'log_BAF': log_BAF}
    elif BAF is not None and log_BAF is not None:
        expected = math.log10(BAF) if BAF > 0 else None
        if expected is not None and abs(expected - log_BAF) < 1e-6:
            return {'BAF': BAF, 'log_BAF': log_BAF, 'verified': True}
        return {'error': 'Inconsistent values.'}
    return {'error': 'Provide BAF or log_BAF.'}


def hazard_quotient(exposure_conc: float, reference_dose: float):
    """Calculate Hazard Quotient: HQ = E / RfD.

    HQ < 1: unlikely adverse effect; HQ ≥ 1: potential concern.
    """
    if reference_dose <= 0:
        return {'error': 'Reference dose must be positive.'}
    hq = exposure_conc / reference_dose
    return {
        'hazard_quotient': round(hq, 4),
        'exposure_conc': exposure_conc,
        'reference_dose': reference_dose
    }


def risk_characterization(hazard_quotient: float):
    """Classify risk level from Hazard Quotient.

    HQ < 1: Low risk (acceptable)
    1 ≤ HQ < 10: Moderate risk
    HQ ≥ 10: High risk
    """
    if hazard_quotient < 1:
        level = 'Low risk (acceptable)'
    elif hazard_quotient < 10:
        level = 'Moderate risk (potential concern)'
    else:
        level = 'High risk (unacceptable)'
    return {
        'hazard_quotient': hazard_quotient,
        'risk_level': level
    }


def lc50_to_ld50(lc50: float, body_weight_kg: float, water_consumption_L_day: float = 2.0):
    """Approximate conversion from LC50 (mg/L) to LD50 (mg/kg).

    LD50 ~ LC50 x (water consumption L/day) / body weight (kg)
    Assumes 24-hour exposure for aquatic LC50.
    """
    if body_weight_kg <= 0:
        return {'error': 'Body weight must be positive.'}
    ld50 = lc50 * water_consumption_L_day / body_weight_kg
    return {
        'lc50_mg_L': lc50,
        'ld50_mg_kg': round(ld50, 4),
        'body_weight_kg': body_weight_kg,
        'water_consumption_L_day': water_consumption_L_day,
        'note': 'Rough approximation; actual LD50 depends on absorption, metabolism, and exposure duration.'
    }


def decay_concentration(C0: float, k: float, t: float):
    """First-order decay: C = C0 x e^(-kt).

    Args:
        C0: Initial concentration (any units)
        k: First-order rate constant (1/time)
        t: Time (same units as 1/k)
    """
    if C0 < 0 or k < 0 or t < 0:
        return {'error': 'C0, k, and t must be non-negative.'}
    C = C0 * math.exp(-k * t)
    return {
        'initial_concentration': C0,
        'rate_constant': k,
        'time': t,
        'concentration': round(C, 6),
        'fraction_remaining': round(C / C0, 6) if C0 > 0 else 0.0
    }


def cod_bod_ratio(COD: float, BOD: float):
    """Calculate COD/BOD ratio indicating biodegradability.

    COD/BOD < 2: Highly biodegradable
    2 ≤ COD/BOD < 4: Moderately biodegradable
    COD/BOD ≥ 4: Low biodegradability (contains refractory organics)
    """
    if BOD <= 0:
        return {'error': 'BOD must be positive.'}
    if COD < 0:
        return {'error': 'COD cannot be negative.'}
    ratio = COD / BOD
    if ratio < 2:
        category = 'Highly biodegradable'
    elif ratio < 4:
        category = 'Moderately biodegradable'
    else:
        category = 'Low biodegradability (refractory organics)'
    return {
        'COD': COD,
        'BOD': BOD,
        'ratio': round(ratio, 2),
        'biodegradability': category
    }


def dilution_factor(C_source: float, Q_source: float, C_ambient: float, Q_ambient: float):
    """Calculate mixing zone concentration after dilution.

    C_mix = (C_source x Q_source + C_ambient x Q_ambient) / (Q_source + Q_ambient)

    Args:
        C_source: Concentration in source stream (any units)
        Q_source: Flow rate of source stream (any units)
        C_ambient: Ambient concentration in receiving water
        Q_ambient: Flow rate of receiving water
    """
    if Q_source < 0 or Q_ambient < 0:
        return {'error': 'Flow rates must be non-negative.'}
    Q_total = Q_source + Q_ambient
    if Q_total <= 0:
        return {'error': 'Total flow rate must be positive.'}
    C_mix = (C_source * Q_source + C_ambient * Q_ambient) / Q_total
    df = Q_total / Q_source if Q_source > 0 else float('inf')
    return {
        'C_mix': round(C_mix, 6),
        'dilution_factor': round(df, 4),
        'Q_total': Q_total,
        'percent_from_source': round(Q_source / Q_total * 100, 2) if Q_total > 0 else 0
    }


MCP_TOOLS = [
    {
        "name": "half_life",
        "description": "Calculate half-life from rate constant, or rate constant from half-life. For first-order: t½ = ln(2)/k.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "k": {"type": "number", "description": "Rate constant (provide if calculating half-life)"},
                "half_life": {"type": "number", "description": "Half-life in consistent time units (provide if calculating k)"},
                "order": {"type": "integer", "description": "Reaction order (default 1 for first-order)", "default": 1}
            },
            "required": []
        },
        "returns": {"type": "object", "description": "Dict with the computed value"}
    },
    {
        "name": "bioconcentration_factor",
        "description": "Interconvert BCF (bioconcentration factor) and log10(BCF).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "BCF": {"type": "number", "description": "BCF value (provide if calculating log BCF)"},
                "log_BCF": {"type": "number", "description": "log10(BCF) (provide if calculating BCF)"}
            },
            "required": []
        },
        "returns": {"type": "object", "description": "Dict with BCF and log_BCF"}
    },
    {
        "name": "bioaccumulation_factor",
        "description": "Interconvert BAF (bioaccumulation factor) and log10(BAF).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "BAF": {"type": "number", "description": "BAF value (provide if calculating log BAF)"},
                "log_BAF": {"type": "number", "description": "log10(BAF) (provide if calculating BAF)"}
            },
            "required": []
        },
        "returns": {"type": "object", "description": "Dict with BAF and log_BAF"}
    },
    {
        "name": "hazard_quotient",
        "description": "Calculate Hazard Quotient: HQ = exposure concentration / reference dose (RfD).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "exposure_conc": {"type": "number", "description": "Exposure concentration"},
                "reference_dose": {"type": "number", "description": "Reference dose (RfD)"}
            },
            "required": ["exposure_conc", "reference_dose"]
        },
        "returns": {"type": "object", "description": "Dict with hazard quotient value"}
    },
    {
        "name": "risk_characterization",
        "description": "Classify risk level from Hazard Quotient. HQ<1: Low, 1-10: Moderate, ≥10: High.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hazard_quotient": {"type": "number", "description": "Hazard quotient value"}
            },
            "required": ["hazard_quotient"]
        },
        "returns": {"type": "object", "description": "Dict with risk level classification"}
    },
    {
        "name": "lc50_to_ld50",
        "description": "Approximate conversion from LC50 (mg/L) to LD50 (mg/kg).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lc50": {"type": "number", "description": "LC50 value in mg/L"},
                "body_weight_kg": {"type": "number", "description": "Body weight in kg"},
                "water_consumption_L_day": {"type": "number", "description": "Daily water consumption in L", "default": 2.0}
            },
            "required": ["lc50", "body_weight_kg"]
        },
        "returns": {"type": "object", "description": "Dict with estimated LD50"}
    },
    {
        "name": "decay_concentration",
        "description": "First-order decay: C = C0 x e^(-kt).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "C0": {"type": "number", "description": "Initial concentration"},
                "k": {"type": "number", "description": "First-order rate constant (1/time)"},
                "t": {"type": "number", "description": "Time"}
            },
            "required": ["C0", "k", "t"]
        },
        "returns": {"type": "object", "description": "Dict with concentration at time t"}
    },
    {
        "name": "cod_bod_ratio",
        "description": "Calculate COD/BOD ratio indicating biodegradability of wastewater.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "COD": {"type": "number", "description": "Chemical oxygen demand"},
                "BOD": {"type": "number", "description": "Biochemical oxygen demand"}
            },
            "required": ["COD", "BOD"]
        },
        "returns": {"type": "object", "description": "Dict with ratio and biodegradability classification"}
    },
    {
        "name": "dilution_factor",
        "description": "Calculate mixing zone concentration after dilution of a source into receiving water.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "C_source": {"type": "number", "description": "Source concentration"},
                "Q_source": {"type": "number", "description": "Source flow rate"},
                "C_ambient": {"type": "number", "description": "Ambient concentration"},
                "Q_ambient": {"type": "number", "description": "Receiving water flow rate"}
            },
            "required": ["C_source", "Q_source", "C_ambient", "Q_ambient"]
        },
        "returns": {"type": "object", "description": "Dict with mixed concentration and dilution factor"}
    },
]
