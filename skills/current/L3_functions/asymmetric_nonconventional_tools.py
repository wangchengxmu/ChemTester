"""
L3 Tools: Asymmetric Reactions in Nonconventional Conditions
============================================================
Green metrics calculator, ionic liquid recyclability, microwave vs thermal
rate comparison (Arrhenius-based).

Parent L2: asymmetric_nonconventional_conditions.md (Punniyamurthy Ch7)
L4 data: asymmetric_nonconventional_data.md
"""

## Solver Instructions (for AI Agent)

# When you encounter **non-conventional asymmetric synthesis** (green chemistry, ionic liquids, microwaves) problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Green chemistry metrics: `green_metrics(product_mass_g, solvent_mass_g, waste_mass_g, catalyst_mass_g, energy_kWh)`
# - Ionic liquid recyclability: `ionic_liquid_recyclability(num_cycles, ee_initial, ee_final)`
# - Microwave vs thermal comparison: `microwave_vs_thermal_rate(time_thermal, temp_thermal_C, time_microwave, temp_microwave_C, Ea)`

### Step 2: Choose the correct function
# - Process efficiency metrics: `green_metrics`
# - IL solvent evaluation: `ionic_liquid_recyclability`
# - Microwave enhancement: `microwave_vs_thermal_rate`

### Step 3: Handle special cases
# - Green metrics include E-factor, atom economy proxy, PMI
# - IL recyclability score accounts for ee loss per cycle and number of usable cycles
# - Microwave results include Arrhenius analysis and non-thermal effect assessment

### Examples
# 1. Product=10g, solvent=100g, waste=5g, catalyst=0.5g, energy=2 kWh: `green_metrics(10, 100, 5, 0.5, 2)`
# 2. IL: 10 cycles, ee drops from 99% to 95%: `ionic_liquid_recyclability(10, 99, 95)` -> recycling score
# 3. Thermal 120 min at 80degC vs MW 15 min at 150degC, Ea=50 kJ/mol: `microwave_vs_thermal_rate(120, 80, 15, 150, 50000)`



import math


def green_metrics(product_mass_g: float,
                  waste_mass_g: float = None,
                  reaction_mass_g: float = None,
                  atom_economy: float = None,
                  mw_product: float = None,
                  mw_all_reagents: float = None,
                  solvent_mass_g: float = None) -> dict:
    """Calculate green chemistry metrics for asymmetric reactions.
    
    Args:
        product_mass_g: mass of isolated product
        waste_mass_g: mass of all waste (byproducts + solvent + etc.)
        reaction_mass_g: total mass of everything that went in
        atom_economy: if known (0-100), skip calculation
        mw_product: molecular weight of product
        mw_all_reagents: sum of all reagent MWs
        solvent_mass_g: mass of solvent used
    
    Returns:
        dict with E_factor, atom_economy, RME, PMI, carbon_efficiency, rating
    """
    # E-factor = total waste / product
    if waste_mass_g is not None and product_mass_g > 0:
        e_factor = waste_mass_g / product_mass_g
    elif reaction_mass_g is not None and product_mass_g > 0:
        e_factor = (reaction_mass_g - product_mass_g) / product_mass_g
    else:
        e_factor = None
    
    # Atom economy
    if atom_economy is not None:
        ae = atom_economy
    elif mw_product and mw_all_reagents and mw_all_reagents > 0:
        ae = mw_product / mw_all_reagents * 100
    else:
        ae = None
    
    # Process Mass Intensity (PMI) = total mass in / product mass
    if reaction_mass_g and product_mass_g > 0:
        pmi = reaction_mass_g / product_mass_g
    elif e_factor is not None:
        pmi = 1 + e_factor  # PMI = 1 + E-factor (approx)
    else:
        pmi = None
    
    # Reaction Mass Efficiency (RME)
    if e_factor is not None and ae is not None:
        # RME = atom_economy * yield / 100, approximate from E-factor
        yield_frac = 1 / (1 + e_factor) if e_factor > 0 else 1
        rme = yield_frac * ae  # simplified
    elif pmi is not None:
        rme = 100 / pmi if pmi > 0 else 0
    else:
        rme = None
    
    # Carbon efficiency (approximate from atom economy)
    ce = ae * 0.9 if ae else None  # rough estimate
    
    # Rating
    if e_factor is not None:
        if e_factor < 5:
            rating = 'excellent'
        elif e_factor < 15:
            rating = 'good'
        elif e_factor < 30:
            rating = 'acceptable'
        elif e_factor < 50:
            rating = 'poor'
        else:
            rating = 'very poor (pharma typical: 25-100)'
    else:
        rating = 'insufficient data'
    
    # Solvent contribution
    solvent_note = ''
    if solvent_mass_g and reaction_mass_g:
        solvent_pct = solvent_mass_g / reaction_mass_g * 100
        solvent_note = f"Solvent is {solvent_pct:.1f}% of total mass - consider alternative solvent or solvent-free"
    
    return {
        'E_factor': round(e_factor, 1) if e_factor else 'N/A',
        'atom_economy_pct': round(ae, 1) if ae else 'N/A',
        'PMI': round(pmi, 1) if pmi else 'N/A',
        'RME_pct': round(rme, 1) if rme else 'N/A',
        'carbon_efficiency_pct': round(ce, 1) if ce else 'N/A',
        'rating': rating,
        'solvent_note': solvent_note if solvent_note else 'N/A',
        'benchmarks': {
            'ideal_E_factor': '<5 (bulk chem), <25 (fine chem), <100 (pharma)',
            'ideal_atom_economy': '>80%',
            'ideal_PMI': '<10 (excellent), <50 (acceptable)'
        }
    }


def ionic_liquid_recyclability(num_cycles: int,
                                ee_initial: float,
                                ee_final: float,
                                yield_initial: float = None,
                                yield_final: float = None) -> dict:
    """Calculate ionic liquid recyclability metrics.
    
    ILs can be recycled multiple times with catalyst retention.
    This function assesses catalyst leaching and performance degradation.
    
    Args:
        num_cycles: number of reuse cycles completed
        ee_initial: initial enantiomeric excess (%)
        ee_final: ee after last cycle (%)
        yield_initial: initial yield (%) - optional
        yield_final: yield after last cycle (%) - optional
    
    Returns:
        dict with degradation rates, recyclability score, recommendations
    """
    if num_cycles <= 0:
        num_cycles = 1
    
    # EE degradation per cycle
    ee_loss_total = ee_initial - ee_final
    ee_loss_per_cycle = ee_loss_total / num_cycles
    
    # Projected cycles before ee drops below threshold
    thresholds = {}
    for thresh_ee in [90, 80, 70]:
        if ee_loss_per_cycle > 0:
            cycles_left = max(0, (ee_final - thresh_ee) / ee_loss_per_cycle)
        else:
            cycles_left = float('inf')
        thresholds[f'{thresh_ee}%_ee'] = {
            'cycles_remaining': round(cycles_left, 1),
            'total_cycles_at_threshold': round(num_cycles + cycles_left, 1)
        }
    
    # Yield degradation
    yield_info = {}
    if yield_initial and yield_final:
        yield_loss = yield_initial - yield_final
        yield_loss_per_cycle = yield_loss / num_cycles
        yield_info = {
            'yield_loss_per_cycle': round(yield_loss_per_cycle, 2),
            'yield_retention_pct': round(yield_final / yield_initial * 100, 1)
        }
    
    # Recyclability score (0-100)
    ee_retention = ee_final / ee_initial if ee_initial > 0 else 0
    score = min(100, ee_retention * 50 + min(num_cycles, 20) / 20 * 50)
    
    if score >= 80:
        grade = 'A - Excellent recyclability'
    elif score >= 60:
        grade = 'B - Good recyclability'
    elif score >= 40:
        grade = 'C - Moderate recyclability'
    else:
        grade = 'D - Poor recyclability'
    
    # Leaching assessment
    if ee_loss_per_cycle < 0.2:
        leaching = 'negligible'
    elif ee_loss_per_cycle < 0.5:
        leaching = 'low'
    elif ee_loss_per_cycle < 1.0:
        leaching = 'moderate - consider imidazolium-tagged ligand'
    else:
        leaching = 'significant - catalyst leaching likely; try IL anion modification'
    
    return {
        'num_cycles': num_cycles,
        'ee_initial': ee_initial,
        'ee_final': ee_final,
        'ee_loss_per_cycle': round(ee_loss_per_cycle, 3),
        'recyclability_score': round(score, 1),
        'grade': grade,
        'leaching_assessment': leaching,
        'thresholds': thresholds,
        'yield_info': yield_info,
        'recommendation': _il_recommendation(score, ee_loss_per_cycle, num_cycles)
    }


def _il_recommendation(score, ee_loss, cycles):
    if score >= 80 and cycles >= 10:
        return "System is excellent - standard IL recycling protocol is sufficient"
    elif ee_loss > 0.5:
        return "Add imidazolium-tagged ligand to suppress metal leaching into organic phase"
    elif cycles < 5:
        return "Monitor for IL decomposition at elevated temperature; add IL replenishment"
    else:
        return "Continue monitoring; system performing adequately"


def microwave_vs_thermal_rate(time_thermal_min: float,
                               temp_thermal_C: float,
                               time_microwave_min: float = None,
                               temp_microwave_C: float = None,
                               activation_energy_kcal: float = 20.0) -> dict:
    """Compare microwave vs conventional thermal reaction rates using Arrhenius equation.
    
    Microwave heating can enhance rates through:
    1. Pure thermal effect (higher effective temperature)
    2. Non-thermal microwave effects (specific molecular heating, superheating)
    3. Hot-spot effects in heterogeneous systems
    
    Args:
        time_thermal_min: reaction time under conventional heating
        temp_thermal_C: conventional heating temperature (C)
        time_microwave_min: microwave reaction time (optional)
        temp_microwave_C: microwave temperature (optional)
        activation_energy_kcal: activation energy (kcal/mol)
    
    Returns:
        dict with rate_enhancement, effective_temp, time_savings
    """
    R = 0.001987  # kcal/(mol·K)
    T_thermal = temp_thermal_C + 273.15
    
    if time_microwave_min is not None and temp_microwave_C is not None:
        T_mw = temp_microwave_C + 273.15
        
        # Observed rate enhancement
        rate_enhancement = time_thermal_min / time_microwave_min
        
        # Expected thermal enhancement from Arrhenius (if both at same T, this = 1)
        arrhenius_factor = math.exp(-activation_energy_kcal / R * (1/T_mw - 1/T_thermal))
        
        # Non-thermal contribution
        non_thermal_factor = rate_enhancement / arrhenius_factor if arrhenius_factor > 0 else 0
        
        # Effective temperature equivalent (what T_thermal would need to be to match MW rate)
        # k_mw/k_th = exp(-Ea/R * (1/T_eff - 1/T_thermal))
        # ln(k_mw/k_th) = -Ea/R * (1/T_eff - 1/T_thermal)
        if rate_enhancement > 0 and rate_enhancement != 1:
            ln_ratio = math.log(rate_enhancement)
            T_effective = 1 / (1/T_thermal - R * ln_ratio / activation_energy_kcal)
            T_effective_C = T_effective - 273.15
        else:
            T_effective_C = temp_thermal_C
        
        time_savings_pct = (1 - time_microwave_min / time_thermal_min) * 100
        
        analysis = _analyze_microwave_results(rate_enhancement, arrhenius_factor, non_thermal_factor)
        
    elif time_microwave_min is not None:
        # Same temperature, different times
        rate_enhancement = time_thermal_min / time_microwave_min
        arrhenius_factor = 1.0  # same temp
        non_thermal_factor = rate_enhancement
        T_mw = T_thermal
        T_effective_C = temp_thermal_C
        time_savings_pct = (1 - time_microwave_min / time_thermal_min) * 100
        analysis = f"Rate enhancement purely from non-thermal/superheating effects. " \
                   f"Factor of {rate_enhancement:.1f}x is {'consistent with' if rate_enhancement < 10 else 'higher than expected for'} microwave effects."
    else:
        # Predict microwave time at elevated T
        return {
            'note': 'Provide time_microwave_min and/or temp_microwave_C for comparison',
            'thermal_time_min': time_thermal_min,
            'thermal_temp_C': temp_thermal_C,
            'prediction': _predict_microwave_time(time_thermal_min, temp_thermal_C, activation_energy_kcal)
        }
    
    return {
        'rate_enhancement': round(rate_enhancement, 2),
        'arrhenius_thermal_factor': round(arrhenius_factor, 2),
        'non_thermal_factor': round(non_thermal_factor, 2),
        'time_thermal_min': time_thermal_min,
        'time_microwave_min': time_microwave_min,
        'temp_thermal_C': temp_thermal_C,
        'temp_microwave_C': temp_microwave_C,
        'effective_thermal_temp_C': round(T_effective_C, 1),
        'time_savings_pct': round(time_savings_pct, 1),
        'analysis': analysis
    }


def _analyze_microwave_results(re, arrh, nontherm):
    if nontherm > 5:
        return f"Significant non-thermal effect detected (factor {nontherm:.1f}x). " \
               "May include specific microwave absorption, hot-spots, or superheating."
    elif nontherm > 2:
        return f"Moderate non-thermal contribution ({nontherm:.1f}x). Partial superheating likely."
    elif arrh > 1.5:
        return f"Enhancement primarily thermal (Arrhenius factor {arrh:.1f}x). " \
               "Microwave advantage is faster heating, not fundamentally different chemistry."
    else:
        return f"Minimal enhancement. Microwave benefit is rapid heating/reproducibility, not rate."


def _predict_microwave_time(t_thermal, temp_thermal_C, Ea, temp_targets=None):
    """Predict microwave reaction times at various temperatures."""
    if temp_targets is None:
        temp_targets = [temp_thermal_C + 20, temp_thermal_C + 40, temp_thermal_C + 60]
    
    R = 0.001987
    T_ref = temp_thermal_C + 273.15
    predictions = []
    for T_C in temp_targets:
        T = T_C + 273.15
        factor = math.exp(-Ea / R * (1/T - 1/T_ref))
        t_mw = t_thermal / factor
        predictions.append({
            'temp_C': T_C,
            'predicted_time_min': round(t_mw, 1),
            'speedup': round(factor, 1)
        })
    return predictions


# ── Test Suite ────────────────────────────────────────────────────────

def _run_tests():
    tests_passed = 0
    tests_total = 0
    
    print("=" * 60)
    print("Nonconventional Conditions Tools - Test Suite")
    print("=" * 60)
    
    # Test 1: E-factor calculation
    tests_total += 1
    r = green_metrics(product_mass_g=1.0, waste_mass_g=25.0)
    assert r['E_factor'] == 25.0
    assert r['PMI'] == 26.0
    tests_passed += 1
    print(f"[PASS] Test 1: E-factor={r['E_factor']}, PMI={r['PMI']}")
    
    # Test 2: Atom economy
    tests_total += 1
    r = green_metrics(product_mass_g=1.0, reaction_mass_g=5.0,
                      mw_product=100, mw_all_reagents=150)
    assert r['atom_economy_pct'] == 66.7
    tests_passed += 1
    print(f"[PASS] Test 2: Atom economy={r['atom_economy_pct']}%")
    
    # Test 3: Green metrics rating
    tests_total += 1
    r = green_metrics(product_mass_g=1.0, waste_mass_g=12.0)
    assert r['rating'] == 'good'
    tests_passed += 1
    print(f"[PASS] Test 3: Rating={r['rating']}")
    
    # Test 4: IL recyclability - excellent
    tests_total += 1
    r = ionic_liquid_recyclability(10, 95, 93)
    assert r['ee_loss_per_cycle'] == 0.2
    assert r['recyclability_score'] > 70
    tests_passed += 1
    print(f"[PASS] Test 4: IL recycled 10x, ee loss/cycle={r['ee_loss_per_cycle']}, score={r['recyclability_score']}")
    
    # Test 5: IL recyclability - poor
    tests_total += 1
    r = ionic_liquid_recyclability(3, 90, 60)
    assert r['ee_loss_per_cycle'] > 5
    assert r['grade'].startswith('C') or r['grade'].startswith('D')
    tests_passed += 1
    print(f"[PASS] Test 5: IL poor recycling, ee loss/cycle={r['ee_loss_per_cycle']}, grade={r['grade']}")
    
    # Test 6: Microwave vs thermal - same temp, faster
    tests_total += 1
    r = microwave_vs_thermal_rate(60, 80, time_microwave_min=5)
    assert r['rate_enhancement'] == 12.0
    assert r['time_savings_pct'] == 91.7
    tests_passed += 1
    print(f"[PASS] Test 6: 12x rate enhancement, 91.7% time savings")
    
    # Test 7: Microwave at higher temperature
    tests_total += 1
    r = microwave_vs_thermal_rate(60, 60, time_microwave_min=10, temp_microwave_C=100,
                                   activation_energy_kcal=20.0)
    assert r['rate_enhancement'] == 6.0
    assert r['arrhenius_thermal_factor'] > 1.0
    tests_passed += 1
    print(f"[PASS] Test 7: Thermal factor={r['arrhenius_thermal_factor']}, non-thermal={r['non_thermal_factor']}")
    
    # Test 8: Microwave prediction
    tests_total += 1
    r = microwave_vs_thermal_rate(120, 25, activation_energy_kcal=20.0)
    assert 'prediction' in r
    assert len(r['prediction']) == 3
    tests_passed += 1
    print(f"[PASS] Test 8: Predictions: {[(p['temp_C'], p['predicted_time_min']) for p in r['prediction']]}")
    
    # Test 9: Solvent contribution note
    tests_total += 1
    r = green_metrics(product_mass_g=1.0, reaction_mass_g=100.0, solvent_mass_g=80.0)
    assert 'Solvent' in r['solvent_note']
    tests_passed += 1
    print(f"[PASS] Test 9: {r['solvent_note'][:50]}...")
    
    print(f"\n{'=' * 60}")
    print(f"Results: {tests_passed}/{tests_total} tests passed")
    if tests_passed == tests_total:
        print("All tests passed!")
    print(f"{'=' * 60}")
    return tests_passed == tests_total


if __name__ == '__main__':
    _run_tests()


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "green_metrics",
        "description": "Calculate green chemistry metrics for asymmetric reactions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_mass_g": {
                    "type": "number",
                    "description": "Product Mass G"
                },
                "waste_mass_g": {
                    "type": "number",
                    "description": "Waste Mass G",
                    "default": None
                },
                "reaction_mass_g": {
                    "type": "number",
                    "description": "Reaction Mass G",
                    "default": None
                },
                "atom_economy": {
                    "type": "number",
                    "description": "Atom Economy",
                    "default": None
                },
                "mw_product": {
                    "type": "number",
                    "description": "Mw Product",
                    "default": None
                },
                "mw_all_reagents": {
                    "type": "number",
                    "description": "Mw All Reagents",
                    "default": None
                },
                "solvent_mass_g": {
                    "type": "number",
                    "description": "Solvent Mass G",
                    "default": None
                }
            },
            "required": [
                "product_mass_g"
            ]
        }
    },
    {
        "name": "ionic_liquid_recyclability",
        "description": "Calculate ionic liquid recyclability metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "num_cycles": {
                    "type": "number",
                    "description": "Num Cycles"
                },
                "ee_initial": {
                    "type": "number",
                    "description": "Ee Initial"
                },
                "ee_final": {
                    "type": "number",
                    "description": "Ee Final"
                },
                "yield_initial": {
                    "type": "number",
                    "description": "Yield Initial",
                    "default": None
                },
                "yield_final": {
                    "type": "number",
                    "description": "Yield Final",
                    "default": None
                }
            },
            "required": [
                "num_cycles",
                "ee_initial",
                "ee_final"
            ]
        }
    },
    {
        "name": "microwave_vs_thermal_rate",
        "description": "Compare microwave vs conventional thermal reaction rates using Arrhenius equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "time_thermal_min": {
                    "type": "number",
                    "description": "Time Thermal Min"
                },
                "temp_thermal_C": {
                    "type": "number",
                    "description": "Temp Thermal C"
                },
                "time_microwave_min": {
                    "type": "number",
                    "description": "Time Microwave Min",
                    "default": None
                },
                "temp_microwave_C": {
                    "type": "number",
                    "description": "Temp Microwave C",
                    "default": None
                },
                "activation_energy_kcal": {
                    "type": "number",
                    "description": "Activation Energy Kcal",
                    "default": 20.0
                }
            },
            "required": [
                "time_thermal_min",
                "temp_thermal_C"
            ]
        }
    }
]