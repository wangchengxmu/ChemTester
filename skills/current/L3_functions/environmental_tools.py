"""
Environmental Chemistry Tools - L3 Implementation
Covers: atmospheric, aquatic, soil, fate & transport, green chemistry
## Solver Instructions (for AI Agent)

When you encounter atmospheric chemistry, aquatic chemistry, or Henry's law problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given Henry's constant and concentration -> Estimate volatilization? Use `henry_law_volatilization(kh_atm_l_mol, c_water, wind_speed, depth, temperature)`
- Given BOD/ultimate BOD -> Calculate BOD kinetics? Use `bod_calc(bod5=..., ultimate_bod=..., k_rate=..., temperature=..., time_days=...)`
- Need atmospheric lifetime estimation? Use `atmospheric_lifetime(k_oh=None, lifetime=None)` or `atmospheric_lifetime_from_rxn_rates(...)`
- pH of weak acid/base? Use `ph_weak_acid(pKa, concentration)` or `ph_weak_base(pKb, concentration)`

### Step 2: Handle special cases
- **BOD**: Temperature-corrected rate constant k_T = k_20 x 1.047^(T-20)
- **Henry's law**: Dimensionless H' = H / (RT); high H' = volatile
- **Atmospheric lifetimes**: Based on OH radical reaction rates (dominant removal mechanism)

### Examples
```python
# Example 1: BOD calculation
bod_calc(ultimate_bod=200, k_rate=0.23, time_days=5)  # -> BOD5 ~ 138 mg/L

# Example 2: Henry's law volatilization
henry_law_volatilization(0.001, 0.001, wind_speed=5, depth=1)  # Returns H', K_L, k_v, half-life
```
"""

from typing import Dict, Tuple, Optional
import math


def henry_law_volatilization(
    kh_atm_l_mol: float,
    c_water: float,
    wind_speed: float = 5.0,
    depth: float = 1.0,
    temperature: float = 25.0
) -> Dict:
    """
    Estimate volatilization flux using Henry's law and two-film model.
    
    Args:
        kh_atm_l_mol: Henry's law constant (atm·L/mol)
        c_water: Dissolved concentration in water (mol/L)
        wind_speed: Wind speed at 10m (m/s), default 5
        depth: Water body depth (m), default 1
        temperature: Temperature (degC), default 25
    
    Returns:
        Dict with dimensionless Henry constant (H'), overall mass transfer
        coefficient K_L (m/h), volatilization rate k_v (1/h), half-life (h)
    """
    R = 8.206e-5  # atm·L/(mol·K)
    T = temperature + 273.15
    H_prime = kh_atm_l_mol / (R * T)
    
    # Simplified mass transfer coefficients (Liss & Slattery model)
    k_L = 0.3 * (wind_speed ** 0.5)  # liquid film (m/h)
    k_G = 500.0 * wind_speed          # gas film (m/h)
    
    K_L = (1.0 / k_L + 1.0 / (k_G * H_prime)) ** -1
    
    k_v = K_L / depth  # first-order rate constant (1/h)
    t_half = math.log(2) / k_v if k_v > 0 else float('inf')
    
    return {
        'H_dimensionless': round(H_prime, 6),
        'K_L_m_per_h': round(K_L, 4),
        'k_v_per_h': round(k_v, 6),
        'half_life_h': round(t_half, 2),
        'notes': 'Simplified two-film model; use EPI Suite for regulatory work'
    }


def bod_calc(
    bod5: Optional[float] = None,
    ultimate_bod: Optional[float] = None,
    k_rate: float = 0.23,
    temperature: float = 20.0,
    time_days: float = 5.0
) -> Dict:
    """
    Calculate BOD values using first-order kinetics.
    
    BOD_t = L_0 * (1 - exp(-k * t))
    Temperature correction: k_T = k_20 * 1.047^(T-20)
    
    Args:
        bod5: BOD5 measurement (mg/L), optional
        ultimate_bod: L0 (mg/L), optional
        k_rate: Rate constant at 20degC (base e), default 0.23 /day
        temperature: Temperature (degC), default 20
        time_days: Time for BOD calculation (days), default 5
    
    Returns:
        Dict with calculated BOD, L0, k, and related values
    """
    k = k_rate * (1.047 ** (temperature - 20.0))
    
    result = {
        'k_T': round(k, 6),
        'temperature': temperature,
        'time_days': time_days
    }
    
    if ultimate_bod is not None:
        L0 = ultimate_bod
        result['L0_mg_L'] = L0
        result['BOD_t_mg_L'] = round(L0 * (1 - math.exp(-k * time_days)), 2)
        result['BOD5_mg_L'] = round(L0 * (1 - math.exp(-k * 5.0)), 2)
    elif bod5 is not None:
        # Solve for L0 from BOD5
        L0 = bod5 / (1 - math.exp(-k * 5.0))
        result['L0_mg_L'] = round(L0, 2)
        result['BOD_t_mg_L'] = round(L0 * (1 - math.exp(-k * time_days)), 2)
        result['BOD5_mg_L'] = round(bod5, 2)
    else:
        return {**result, 'error': 'Provide either bod5 or ultimate_bod'}
    
    return result


def partition_coefficient(
    log_kow: Optional[float] = None,
    foc: float = 0.02,
    mode: str = 'estimate'
) -> Dict:
    """
    Calculate partition coefficients for environmental fate assessment.
    
    Relationships:
        log Koc ~ 0.81 * log Kow + 0.10 (Karickhoff, 1981)
        log BCF ~ 0.85 * log Kow - 0.70 (Veith et al.)
        Kd = foc * Koc
    
    Args:
        log_kow: log10 octanol-water partition coefficient
        foc: Fraction of organic carbon in soil/sediment, default 0.02
        mode: 'estimate' (from log Kow) or 'classify' only
    
    Returns:
        Dict with Kow, Koc, Kd, BCF, and classification
    """
    result = {'foc': foc}
    
    if log_kow is None and mode != 'classify':
        return {**result, 'error': 'log_kow required'}
    
    if log_kow is not None:
        log_koc = 0.81 * log_kow + 0.10
        log_bcf = 0.85 * log_kow - 0.70
        Kd = foc * (10 ** log_koc)
        
        # Classification
        if log_kow < 0:
            hydrophobicity = 'Very hydrophilic'
        elif log_kow < 3:
            hydrophobicity = 'Moderate'
        elif log_kow < 5:
            hydrophobicity = 'Hydrophobic'
        else:
            hydrophobicity = 'Very hydrophobic'
        
        bcf_cat = 'Not B' if log_bcf < 3.3 else ('B' if log_bcf < 3.7 else 'vB')
        persist_note = 'High Kow may indicate potential persistence'
        
        result.update({
            'log_Kow': log_kow,
            'log_Koc': round(log_koc, 3),
            'Koc_L_kg': round(10 ** log_koc, 2),
            'log_BCF': round(log_bcf, 3),
            'BCF_L_kg': round(10 ** log_bcf, 2),
            'Kd_L_kg': round(Kd, 4),
            'Kd_mL_g': round(Kd * 1000, 2),
            'hydrophobicity': hydrophobicity,
            'bioaccumulation_category': bcf_cat,
            'notes': persist_note
        })
    
    return result


def greenhouse_forcing(
    co2_ppm: float = 421.0,
    ch4_ppb: float = 1866.0,
    n2o_ppb: float = 332.0,
    baseline_co2: float = 278.0,
    baseline_ch4: float = 722.0,
    baseline_n2o: float = 270.0
) -> Dict:
    """
    Calculate radiative forcing from greenhouse gases (IPCC simplified expressions).
    
    DeltaF_CO2 = 5.35 * ln(C/C0)
    DeltaF_CH4 = 0.036 * (√M - √M0) - f(M, N2O)  [simplified]
    DeltaF_N2O = 0.12 * (√N - √N0) [simplified]
    
    Climate sensitivity: DeltaT ~ 0.8 * DeltaF_total
    
    Args:
        co2_ppm: Current CO2 concentration (ppm)
        ch4_ppb: Current CH4 concentration (ppb)
        n2o_ppb: Current N2O concentration (ppb)
        baseline_co2: Pre-industrial CO2 (ppm)
        baseline_ch4: Pre-industrial CH4 (ppb)
        baseline_n2o: Pre-industrial N2O (ppb)
    
    Returns:
        Dict with individual and total radiative forcing, estimated temperature change
    """
    dF_co2 = 5.35 * math.log(co2_ppm / baseline_co2)
    
    # Simplified CH4 forcing (first-order)
    dF_ch4 = 0.036 * (math.sqrt(ch4_ppb) - math.sqrt(baseline_ch4))
    
    # Simplified N2O forcing
    dF_n2o = 0.12 * (math.sqrt(n2o_ppb) - math.sqrt(baseline_n2o))
    
    dF_total = dF_co2 + dF_ch4 + dF_n2o
    
    # Climate sensitivity estimate (lambda ~ 0.8 K/(W/m2))
    delta_T = 0.8 * dF_total
    
    return {
        'dF_CO2_Wm2': round(dF_co2, 3),
        'dF_CH4_Wm2': round(dF_ch4, 3),
        'dF_N2O_Wm2': round(dF_n2o, 3),
        'dF_total_Wm2': round(dF_total, 3),
        'delta_T_estimate_C': round(delta_T, 2),
        'notes': 'Simplified IPCC expressions; does not include aerosols, clouds, or feedbacks'
    }


def atom_economy(
    product_mw: float,
    reactant_mws: list,
    product_formula: str = '',
    reactant_formulas: Optional[list] = None
) -> Dict:
    """
    Calculate atom economy of a chemical reaction.
    
    Atom Economy (%) = (MW of desired product / Sum of MW of all reactants) x 100
    
    Args:
        product_mw: Molecular weight of desired product (g/mol)
        reactant_mws: List of molecular weights of all reactants (g/mol)
        product_formula: Optional formula string for display
        reactant_formulas: Optional list of formula strings
    
    Returns:
        Dict with atom economy percentage and related metrics
    """
    total_reactant_mw = sum(reactant_mws)
    ae = (product_mw / total_reactant_mw) * 100 if total_reactant_mw > 0 else 0
    waste_mw = total_reactant_mw - product_mw
    
    # E-factor and PMI (assuming 100% yield for atom economy context)
    e_factor = waste_mw / product_mw if product_mw > 0 else float('inf')
    pmi = e_factor + 1
    
    return {
        'atom_economy_pct': round(ae, 2),
        'product_mw': product_mw,
        'total_reactant_mw': round(total_reactant_mw, 2),
        'waste_mw': round(waste_mw, 2),
        'E_factor_atm_econ': round(e_factor, 4),
        'PMI_atm_econ': round(pmi, 4),
        'product_formula': product_formula,
        'reactant_formulas': reactant_formulas,
        'rating': 'Excellent' if ae > 80 else ('Good' if ae > 60 else ('Moderate' if ae > 40 else 'Poor'))
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "atom_economy",
        "description": "Calculate atom economy of a chemical reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_mw": {"type": "number", "description": "Product Mw"},
                "reactant_mws": {"type": "number", "description": "Reactant Mws"},
                "product_formula": {"type": "string", "description": "Product Formula", "default": ""},
                "reactant_formulas": {"type": "string", "description": "Reactant Formulas", "default": None},
            },
            "required": ["product_mw", "reactant_mws"]
        }
    },
    {
        "name": "bod_calc",
        "description": "Calculate BOD values using first-order kinetics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "bod5": {"type": "number", "description": "Bod5", "default": None},
                "ultimate_bod": {"type": "number", "description": "Ultimate Bod", "default": None},
                "k_rate": {"type": "number", "description": "K Rate", "default": 0.23},
                "temperature": {"type": "number", "description": "Temperature", "default": 20.0},
                "time_days": {"type": "number", "description": "Time Days", "default": 5.0},
            },
            "required": []
        }
    },
    {
        "name": "greenhouse_forcing",
        "description": "Calculate radiative forcing from greenhouse gases (IPCC simplified expressions).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "co2_ppm": {"type": "number", "description": "Co2 Ppm", "default": 421.0},
                "ch4_ppb": {"type": "number", "description": "Ch4 Ppb", "default": 1866.0},
                "n2o_ppb": {"type": "number", "description": "N2O Ppb", "default": 332.0},
                "baseline_co2": {"type": "number", "description": "Baseline Co2", "default": 278.0},
                "baseline_ch4": {"type": "number", "description": "Baseline Ch4", "default": 722.0},
                "baseline_n2o": {"type": "number", "description": "Baseline N2O", "default": 270.0},
            },
            "required": []
        }
    },
    {
        "name": "henry_law_volatilization",
        "description": "Estimate volatilization flux using Henry's law and two-film model.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kh_atm_l_mol": {"type": "number", "description": "Kh Atm L Mol"},
                "c_water": {"type": "number", "description": "C Water"},
                "wind_speed": {"type": "number", "description": "Wind Speed", "default": 5.0},
                "depth": {"type": "number", "description": "Depth", "default": 1.0},
                "temperature": {"type": "number", "description": "Temperature", "default": 25.0},
            },
            "required": ["kh_atm_l_mol", "c_water"]
        }
    },
    {
        "name": "partition_coefficient",
        "description": "Calculate partition coefficients for environmental fate assessment.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "log_kow": {"type": "number", "description": "Log Kow", "default": None},
                "foc": {"type": "number", "description": "Foc", "default": 0.02},
                "mode": {"type": "string", "description": "Mode", "default": "estimate"},
            },
            "required": []
        }
    }
]
