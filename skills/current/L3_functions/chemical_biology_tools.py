"""
L3 Tool: Chemical Biology Tools
Bioorthogonal reactions, protein labeling calculations, proteomics metrics.

Source: LibreTexts Biological Chemistry, Bertozzi review (PMC2908729)
Created: 2026-03-24 (Phase 2)

## Solver Instructions (for AI Agent)

When you encounter chemical biology / bioorthogonal chemistry problems:

### Step 1: Identify what is given and what is asked
- Given: rate constants, concentrations, molecular weights, spectroscopic data
- Asked: half-life, labeling efficiency, MW change, IC50, fluorophore brightness

### Step 2: Choose the correct function
- `reaction_half_life(k_second_order, concentration)`: t1/2 = 1/(kx[C])
- `bioorthogonal_labeling_efficiency(k_rate, time_s, conc)`: % labeling at time t
- `mw_increase_labeling(mw_protein, mw_label, num_labels)`: DeltaMW from labeling
- `abpp_ic50(probe_signal_control, probe_signal_inhibitor, inhibitor_conc)`: IC50 from ABPP
- `fluorophore_brightness(extinction_coeff, quantum_yield)`: Brightness = ε x Φ
- `sortase_ligation_yield(conc_substrate, conc_probe, k_cat, Km)`: Enzymatic yield

### Step 3: Handle special cases
- CuAAC (k~102-103), SPAAC (k~10-3-1), IEDDA/TCO (k~103-106 M-1s-1)

### Examples
```python
reaction_half_life(0.5, 100e-6)  # SPAAC, 100muM -> 20000s
fluorophore_brightness(68000, 0.92)  # FITC -> 62,560
```
"""

import math


def reaction_half_life(k_second_order: float, concentration: float) -> dict:
    """Calculate half-life for a second-order bioorthogonal reaction.
    
    t1/2 = 1 / (k * [substrate])
    k in M-1s-1, concentration in M
    """
    if k_second_order <= 0 or concentration <= 0:
        return {'error': 'k and concentration must be positive'}
    t_half = 1.0 / (k_second_order * concentration)
    return {
        'half_life_s': t_half,
        'half_life_min': t_half / 60,
        'k': k_second_order,
        'concentration_M': concentration
    }


def bioorthogonal_labeling_efficiency(k_rate: float, time_s: float, conc: float) -> dict:
    """Estimate labeling efficiency (fraction labeled) for second-order reaction.
    
    Pseudo-first-order: k' = k * [probe]
    Fraction labeled = 1 - exp(-k' * t)
    """
    if k_rate <= 0 or time_s <= 0 or conc <= 0:
        return {'error': 'All parameters must be positive'}
    k_prime = k_rate * conc  # pseudo-first-order
    fraction = 1 - math.exp(-k_prime * time_s)
    return {
        'fraction_labeled': round(fraction, 6),
        'k_prime_s1': round(k_prime, 6),
        'k': k_rate,
        'time_s': time_s,
        'conc_M': conc
    }


def mw_increase_labeling(mw_protein: float, mw_label: float, num_labels: int = 1) -> dict:
    """Calculate MW shift from protein labeling.
    """
    mw_labeled = mw_protein + mw_label * num_labels
    shift_percent = (mw_labeled - mw_protein) / mw_protein * 100
    return {
        'mw_protein': mw_protein,
        'mw_label': mw_label,
        'mw_labeled': mw_labeled,
        'shift_Da': mw_label * num_labels,
        'shift_percent': round(shift_percent, 2),
        'num_labels': num_labels
    }


def abpp_ic50(probe_signal_control: float, probe_signal_inhibitor: float, inhibitor_conc: float) -> dict:
    """Calculate apparent IC50 from competitive ABPP data.
    
    Simple model: signal_inh = signal_control * (1 - conc / (conc + IC50))
    """
    if probe_signal_control <= 0 or inhibitor_conc < 0:
        return {'error': 'Invalid parameters'}
    fraction_remaining = probe_signal_inhibitor / probe_signal_control
    if fraction_remaining >= 1.0:
        return {'ic50': 'infinite or no inhibition', 'fraction_remaining': fraction_remaining}
    if fraction_remaining <= 0:
        return {'ic50': inhibitor_conc, 'fraction_remaining': 0}
    ic50 = inhibitor_conc * fraction_remaining / (1 - fraction_remaining)
    return {
        'ic50_M': round(ic50, 6),
        'fraction_remaining': round(fraction_remaining, 6),
        'inhibitor_conc_M': inhibitor_conc
    }


def fluorophore_brightness(extinction_coeff: float, quantum_yield: float) -> dict:
    """Calculate fluorophore brightness.
    
    Brightness = ε x Φ (M-1cm-1)
    """
    brightness = extinction_coeff * quantum_yield
    return {
        'brightness': brightness,
        'extinction_coeff': extinction_coeff,
        'quantum_yield': quantum_yield
    }


def sortase_ligation_yield(conc_substrate: float, conc_probe: float, k_cat: float,
                           k_m: float, time_s: float, enzyme_conc: float = 1e-6) -> dict:
    """Estimate sortase-mediated ligation yield using Michaelis-Menten kinetics.
    
    v = Vmax * [S] / (Km + [S]), where Vmax = kcat * [E]
    """
    if enzyme_conc <= 0 or time_s <= 0:
        return {'error': 'Invalid parameters'}
    v_max = k_cat * enzyme_conc
    v = v_max * conc_substrate / (k_m + conc_substrate)
    product = v * time_s
    yield_frac = min(product / conc_substrate, 1.0)
    return {
        'yield_fraction': round(yield_frac, 6),
        'product_uM': round(product * 1e6, 2),
        'v_uM_s': round(v * 1e6, 4),
        'kcat': k_cat,
        'Km': k_m
    }


TEXTBOOK_PROBLEMS = {
    "bioorthogonal_half_life": "Calculate t½ for SPAAC (k=1 M-1s-1) at [probe]=100 muM",
    "mw_shift": "Calculate MW shift: 50 kDa protein + 543 Da fluorophore",
}


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'abpp_ic50', 'description': 'Calculate apparent IC50 from competitive ABPP data.\n\nSimple model: signal_inh = signal_control * (1 - conc / (conc + IC50))', 'inputSchema': {'type': 'object', 'properties': {'probe_signal_control': {'type': 'number', 'description': 'Probe Signal Control'}, 'probe_signal_inhibitor': {'type': 'number', 'description': 'Probe Signal Inhibitor'}, 'inhibitor_conc': {'type': 'number', 'description': 'Inhibitor Conc'}}, 'required': ['probe_signal_control', 'probe_signal_inhibitor', 'inhibitor_conc']}},
    {'name': 'bioorthogonal_labeling_efficiency', 'description': "Estimate labeling efficiency (fraction labeled) for second-order reaction.\n\nPseudo-first-order: k' = k * [probe]\nFraction labeled = 1 - exp(-k' * t)", 'inputSchema': {'type': 'object', 'properties': {'k_rate': {'type': 'number', 'description': 'K Rate'}, 'time_s': {'type': 'string', 'description': 'Time S'}, 'conc': {'type': 'number', 'description': 'Conc'}}, 'required': ['k_rate', 'time_s', 'conc']}},
    {'name': 'fluorophore_brightness', 'description': 'Calculate fluorophore brightness.\n\nBrightness = ε x Φ (M-1cm-1)', 'inputSchema': {'type': 'object', 'properties': {'extinction_coeff': {'type': 'string', 'description': 'Extinction Coeff'}, 'quantum_yield': {'type': 'number', 'description': 'Quantum Yield'}}, 'required': ['extinction_coeff', 'quantum_yield']}},
    {'name': 'mw_increase_labeling', 'description': 'Calculate MW shift from protein labeling.', 'inputSchema': {'type': 'object', 'properties': {'mw_protein': {'type': 'string', 'description': 'Mw Protein'}, 'mw_label': {'type': 'string', 'description': 'Mw Label'}, 'num_labels': {'type': 'string', 'description': 'Num Labels', 'default': 1}}, 'required': ['mw_protein', 'mw_label']}},
    {'name': 'reaction_half_life', 'description': 'Calculate half-life for a second-order bioorthogonal reaction.\n\nt1/2 = 1 / (k * [substrate])\nk in M-1s-1, concentration in M', 'inputSchema': {'type': 'object', 'properties': {'k_second_order': {'type': 'number', 'description': 'K Second Order'}, 'concentration': {'type': 'string', 'description': 'Concentration'}}, 'required': ['k_second_order', 'concentration']}},
    {'name': 'sortase_ligation_yield', 'description': 'Estimate sortase-mediated ligation yield using Michaelis-Menten kinetics.\n\nv = Vmax * [S] / (Km + [S]), where Vmax = kcat * [E]', 'inputSchema': {'type': 'object', 'properties': {'conc_substrate': {'type': 'number', 'description': 'Conc Substrate'}, 'conc_probe': {'type': 'number', 'description': 'Conc Probe'}, 'k_cat': {'type': 'number', 'description': 'K Cat'}, 'k_m': {'type': 'number', 'description': 'K M'}, 'time_s': {'type': 'string', 'description': 'Time S'}, 'enzyme_conc': {'type': 'number', 'description': 'Enzyme Conc', 'default': 1e-06}}, 'required': ['conc_substrate', 'conc_probe', 'k_cat', 'k_m', 'time_s']}}
]
