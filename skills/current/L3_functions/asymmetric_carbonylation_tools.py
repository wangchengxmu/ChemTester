"""
L3 Tools: Asymmetric Carbonylation Reactions
=============================================
Enantioselectivity calculator, hydroformylation regioselectivity predictor,
CO insertion rate estimator for Rh/Co/Pd-catalyzed carbonylation.

Parent L2: asymmetric_carbonylation.md (Punniyamurthy Ch9)
L4 data: asymmetric_carbonylation_data.csv
"""

## Solver Instructions (for AI Agent)

# When you encounter **asymmetric carbonylation / hydroformylation** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Calculate ee from conversion and product ee: `calculate_ee_from_conversion(conversion, ee_product, ee_substrate=None)`
# - Hydroformylation regioselectivity: `predict_hydroformylation_regioselectivity(ligand_cone_angle, substrate_type, electronic_factor)`
# - CO insertion rate estimate: `estimate_co_insertion_rate(metal, ligand_donor_strength, temperature)`

### Step 2: Choose the correct function
# - ee analysis: `calculate_ee_from_conversion`
# - Regioselectivity (n:iso ratio): `predict_hydroformylation_regioselectivity`
# - Kinetic estimate: `estimate_co_insertion_rate`

### Step 3: Handle special cases
# - Large cone angle ligands favor branched (iso) products
# - Rh is default metal for hydroformylation
# - ee_substrate=0 assumed for resolution reactions if not provided

### Examples
# 1. Conversion=80%, ee_product=95%: `calculate_ee_from_conversion(80, 95)` -> ee_substrate computed
# 2. Bulky phosphite ligand (cone_angle=180deg), terminal alkene: `predict_hydroformylation_regioselectivity(180, "terminal", 1.0)` -> predicts high branched selectivity



import math


def calculate_ee_from_conversion(conversion: float, ee_product: float,
                                  ee_substrate: float = 0.0) -> dict:
    """Calculate enantiomeric excess considering conversion.
    
    For asymmetric reactions where ee depends on conversion (kinetic resolution).
    ee_observed = ee_product * conversion / (conversion + ee_substrate * (1 - conversion))
    Simplified: returns ee and er for the product mixture.
    
    Args:
        conversion: fractional conversion (0-1)
        ee_product: ee of product (0-100)
        ee_substrate: ee of remaining substrate (0-100), 0 for non-resolution
    
    Returns:
        dict with product_ee, product_er, substrate_ee, yield_enantiopure_max
    """
    c = max(0.0, min(1.0, conversion))
    ee_p = max(0.0, min(100.0, ee_product))
    ee_s = max(0.0, min(100.0, ee_substrate))
    
    er_p = (100 + ee_p) / (100 - ee_p) if ee_p < 100 else float('inf')
    er_s = (100 + ee_s) / (100 - ee_s) if ee_s < 100 else float('inf')
    
    # Maximum theoretical yield at given ee (kinetic resolution)
    # E = ln[(1-c)(1-ee_s)] / ln[(1-c)(1+ee_s)]
    if ee_s > 0 and c > 0 and c < 1:
        try:
            s_factor = math.log((1 - c) * (1 - ee_s / 100)) / math.log((1 - c) * (1 + ee_s / 100))
        except (ValueError, ZeroDivisionError):
            s_factor = float('inf')
    elif ee_p > 0 and c > 0:
        # For non-resolution asymmetric synthesis: s from ee and conversion
        s_factor = ee_p / 100 * c / ((1 - ee_p / 100) * c + 1 - c) if c > 0 else float('inf')
    else:
        s_factor = float('inf')
    
    return {
        'product_ee': round(ee_p, 1),
        'product_er': round(er_p, 2),
        'substrate_ee': round(ee_s, 1),
        'substrate_er': round(er_s, 2),
        'conversion': round(c, 4),
        'estimated_s_factor': round(s_factor, 1) if s_factor != float('inf') else '>1000'
    }


def predict_hydroformylation_regioselectivity(ligand_cone_angle: float,
                                              substrate_type: str = 'styrene',
                                              temperature_C: float = 60,
                                              pressure_bar: float = 40) -> dict:
    """Predict branched/linear (b/l) ratio for asymmetric hydroformylation.
    
    Based on empirical correlations: larger cone angle favors branched selectivity
    for aryl alkenes. Rh systems with BINAPHOS-type ligands show strong steric control.
    
    Args:
        ligand_cone_angle: Tolman cone angle of ligand (degrees)
        substrate_type: 'styrene', 'vinyl_arene', 'aliphatic', 'internal'
        temperature_C: reaction temperature
        pressure_bar: syngas pressure
    
    Returns:
        dict with b_l_ratio, branched_fraction, recommended_conditions
    """
    # Substrate baseline b/l ratios (at cone_angle=140, 60C, 40 bar)
    substrate_params = {
        'styrene':      {'baseline_bl': 8.0, 'cone_sensitivity': 0.15, 'temp_penalty': 0.02},
        'vinyl_arene':  {'baseline_bl': 5.0, 'cone_sensitivity': 0.12, 'temp_penalty': 0.02},
        'aliphatic':    {'baseline_bl': 0.6, 'cone_sensitivity': 0.03, 'temp_penalty': 0.01},
        'internal':     {'baseline_bl': 0.3, 'cone_sensitivity': 0.02, 'temp_penalty': 0.01},
    }
    
    if substrate_type not in substrate_params:
        substrate_type = 'aliphatic'
    
    p = substrate_params[substrate_type]
    
    # Cone angle effect: larger angle = more branched (exponential)
    cone_factor = math.exp(p['cone_sensitivity'] * (ligand_cone_angle - 140))
    
    # Temperature effect: higher T favors linear (lower b/l)
    temp_factor = math.exp(-p['temp_penalty'] * (temperature_C - 60))
    
    # Pressure effect: higher CO pressure can slightly favor branched for Rh
    pressure_factor = 1.0 + 0.005 * (pressure_bar - 40)
    
    b_l_ratio = p['baseline_bl'] * cone_factor * temp_factor * pressure_factor
    b_l_ratio = max(0.1, b_l_ratio)
    
    branched_frac = b_l_ratio / (1 + b_l_ratio)
    
    # EE estimate based on substrate and b/l
    if substrate_type in ('styrene', 'vinyl_arene') and b_l_ratio > 5:
        ee_range = (85, 95)
    elif substrate_type in ('styrene', 'vinyl_arene'):
        ee_range = (70, 88)
    elif substrate_type == 'aliphatic' and b_l_ratio > 2:
        ee_range = (50, 75)
    else:
        ee_range = (20, 50)
    
    return {
        'b_l_ratio': round(b_l_ratio, 2),
        'branched_fraction': round(branched_frac, 3),
        'linear_fraction': round(1 - branched_frac, 3),
        'estimated_ee_range': ee_range,
        'substrate_type': substrate_type,
        'notes': f"Higher cone angle ({ligand_cone_angle} deg) promotes branched product. "
                 f"{'Excellent' if b_l_ratio > 10 else 'Good' if b_l_ratio > 3 else 'Moderate'} regioselectivity."
    }


def estimate_co_insertion_rate(metal: str = 'Rh',
                               ligand_denticity: int = 2,
                               ligand_cone_angle: float = 140,
                               temperature_C: float = 60,
                               co_pressure_bar: float = 40) -> dict:
    """Estimate relative CO insertion rate based on metal/ligand parameters.
    
    CO insertion into M-alkyl bond is the key migratory insertion step.
    Rate depends on: metal electron density, steric crowding, CO concentration.
    
    Args:
        metal: 'Rh', 'Co', 'Pd'
        ligand_denticity: 1 (monodentate) or 2 (bidentate)
        ligand_cone_angle: Tolman cone angle (degrees)
        temperature_C: reaction temperature
        co_pressure_bar: CO partial pressure
    
    Returns:
        dict with relative_rate, co_coordination_strength, recommendations
    """
    # Metal intrinsic activity factors (relative to Rh=1.0)
    metal_factors = {
        'Rh': {'activity': 1.0, 'co_affinity': 1.0, 'typical_temp': (40, 100)},
        'Co': {'activity': 0.1, 'co_affinity': 1.5, 'typical_temp': (100, 180)},
        'Pd': {'activity': 0.5, 'co_affinity': 0.8, 'typical_temp': (60, 120)},
    }
    
    if metal not in metal_factors:
        metal = 'Rh'
    
    mf = metal_factors[metal]
    
    # Denticity effect: bidentate chelates reduce CO coordination sites
    denticity_factor = 1.2 if ligand_denticity == 1 else 0.8
    
    # Steric effect: larger cone angle slows CO coordination
    steric_factor = math.exp(-0.008 * (ligand_cone_angle - 130))
    
    # CO concentration effect (proportional to pressure via Henry's law approx)
    co_factor = (co_pressure_bar / 40) ** 0.5
    
    # Temperature effect (Arrhenius-like, relative to 60C)
    temp_K = temperature_C + 273.15
    ref_K = 333.15  # 60C
    # Typical Ea for CO insertion ~15-25 kcal/mol
    Ea = 20.0 if metal == 'Rh' else (25.0 if metal == 'Co' else 18.0)
    R = 0.001987  # kcal/(mol·K)
    temp_factor = math.exp(-Ea / R * (1/temp_K - 1/ref_K))
    
    relative_rate = mf['activity'] * denticity_factor * steric_factor * co_factor * temp_factor
    relative_rate = max(0.001, relative_rate)
    
    # CO coordination strength assessment
    if mf['co_affinity'] > 1.2 and co_pressure_bar < 10:
        co_note = "WARNING: Low CO pressure for high-affinity metal - may need higher pressure"
    elif co_pressure_bar > 100:
        co_note = "Very high CO pressure - ensure equipment safety"
    else:
        co_note = "CO pressure within normal operating range"
    
    return {
        'relative_rate': round(relative_rate, 3),
        'metal': metal,
        'co_affinity': round(mf['co_affinity'], 1),
        'steric_factor': round(steric_factor, 3),
        'co_factor': round(co_factor, 3),
        'temp_factor': round(temp_factor, 3),
        'co_pressure_note': co_note,
        'recommended_pressure': f"{mf['typical_temp'][0]}-{max(mf['typical_temp'][1], int(temperature_C))} C, "
                                f"{'20-80' if metal == 'Rh' else '50-200' if metal == 'Co' else '10-100'} bar"
    }


# ── Test Suite ────────────────────────────────────────────────────────

def _run_tests():
    """Run all tests for asymmetric carbonylation tools."""
    tests_passed = 0
    tests_total = 0
    
    print("=" * 60)
    print("Asymmetric Carbonylation Tools - Test Suite")
    print("=" * 60)
    
    # Test 1: EE from conversion
    tests_total += 1
    result = calculate_ee_from_conversion(0.8, 90.0, 10.0)
    assert result['product_ee'] == 90.0, f"Expected 90.0, got {result['product_ee']}"
    assert result['product_er'] == 19.0, f"Expected 19.0, got {result['product_er']}"
    tests_passed += 1
    print(f"[PASS] Test 1: EE from conversion")
    
    # Test 2: ER for 99% ee
    tests_total += 1
    result = calculate_ee_from_conversion(0.95, 99.0, 0.0)
    assert result['product_er'] == 199.0, f"Expected 199.0, got {result['product_er']}"
    tests_passed += 1
    print(f"[PASS] Test 2: ER for 99% ee = 199:1")
    
    # Test 3: Hydroformylation regioselectivity - styrene with large ligand
    tests_total += 1
    result = predict_hydroformylation_regioselectivity(170, 'styrene', 60, 40)
    assert result['b_l_ratio'] > 10.0, f"Expected b/l > 10, got {result['b_l_ratio']}"
    assert result['branched_fraction'] > 0.9, f"Expected branched > 0.9, got {result['branched_fraction']}"
    tests_passed += 1
    print(f"[PASS] Test 3: Styrene hydroformylation b/l = {result['b_l_ratio']}")
    
    # Test 4: Aliphatic alkene gives lower regioselectivity
    tests_total += 1
    result = predict_hydroformylation_regioselectivity(140, 'aliphatic', 80, 40)
    assert result['b_l_ratio'] < 2.0, f"Expected b/l < 2 for aliphatic, got {result['b_l_ratio']}"
    tests_passed += 1
    print(f"[PASS] Test 4: Aliphatic b/l = {result['b_l_ratio']} (low as expected)")
    
    # Test 5: Temperature effect on regioselectivity
    tests_total += 1
    r_low = predict_hydroformylation_regioselectivity(150, 'styrene', 25, 40)
    r_high = predict_hydroformylation_regioselectivity(150, 'styrene', 100, 40)
    assert r_low['b_l_ratio'] > r_high['b_l_ratio'], "Lower T should give higher b/l"
    tests_passed += 1
    print(f"[PASS] Test 5: Temp effect - 25C b/l={r_low['b_l_ratio']:.1f} > 100C b/l={r_high['b_l_ratio']:.1f}")
    
    # Test 6: CO insertion rate - Rh vs Co
    tests_total += 1
    r_rh = estimate_co_insertion_rate('Rh', 2, 140, 60, 40)
    r_co = estimate_co_insertion_rate('Co', 2, 140, 60, 40)
    assert r_rh['relative_rate'] > r_co['relative_rate'], "Rh should be faster than Co"
    tests_passed += 1
    print(f"[PASS] Test 6: Rh rate={r_rh['relative_rate']:.3f} > Co rate={r_co['relative_rate']:.3f}")
    
    # Test 7: Steric effect on CO insertion
    tests_total += 1
    r_small = estimate_co_insertion_rate('Rh', 1, 120, 60, 40)
    r_big = estimate_co_insertion_rate('Rh', 1, 180, 60, 40)
    assert r_small['relative_rate'] > r_big['relative_rate'], "Smaller ligand should be faster"
    tests_passed += 1
    print(f"[PASS] Test 7: Steric effect - 120deg={r_small['relative_rate']:.3f} > 180deg={r_big['relative_rate']:.3f}")
    
    # Test 8: CO pressure effect
    tests_total += 1
    r_low_p = estimate_co_insertion_rate('Rh', 2, 140, 60, 10)
    r_high_p = estimate_co_insertion_rate('Rh', 2, 140, 60, 100)
    assert r_high_p['relative_rate'] > r_low_p['relative_rate'], "Higher CO pressure should be faster"
    tests_passed += 1
    print(f"[PASS] Test 8: Pressure effect - 100bar={r_high_p['relative_rate']:.3f} > 10bar={r_low_p['relative_rate']:.3f}")
    
    # Test 9: Pd hydroesterification rate
    tests_total += 1
    r_pd = estimate_co_insertion_rate('Pd', 2, 145, 80, 30)
    assert 0.1 < r_pd['relative_rate'] < 2.0, f"Unexpected Pd rate: {r_pd['relative_rate']}"
    tests_passed += 1
    print(f"[PASS] Test 9: Pd rate={r_pd['relative_rate']:.3f} (reasonable)")
    
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
        "name": "calculate_ee_from_conversion",
        "description": "Calculate enantiomeric excess considering conversion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "conversion": {
                    "type": "number",
                    "description": "Conversion"
                },
                "ee_product": {
                    "type": "number",
                    "description": "Ee Product"
                },
                "ee_substrate": {
                    "type": "number",
                    "description": "Ee Substrate",
                    "default": 0.0
                }
            },
            "required": [
                "conversion",
                "ee_product"
            ]
        }
    },
    {
        "name": "estimate_co_insertion_rate",
        "description": "Estimate relative CO insertion rate based on metal/ligand parameters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "metal": {
                    "type": "number",
                    "description": "Metal",
                    "default": "Rh"
                },
                "ligand_denticity": {
                    "type": "number",
                    "description": "Ligand Denticity",
                    "default": 2
                },
                "ligand_cone_angle": {
                    "type": "number",
                    "description": "Ligand Cone Angle",
                    "default": 140
                },
                "temperature_C": {
                    "type": "number",
                    "description": "Temperature C",
                    "default": 60
                },
                "co_pressure_bar": {
                    "type": "number",
                    "description": "Co Pressure Bar",
                    "default": 40
                }
            },
            "required": []
        }
    },
    {
        "name": "predict_hydroformylation_regioselectivity",
        "description": "Predict branched/linear (b/l) ratio for asymmetric hydroformylation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ligand_cone_angle": {
                    "type": "number",
                    "description": "Ligand Cone Angle"
                },
                "substrate_type": {
                    "type": "number",
                    "description": "Substrate Type",
                    "default": "styrene"
                },
                "temperature_C": {
                    "type": "number",
                    "description": "Temperature C",
                    "default": 60
                },
                "pressure_bar": {
                    "type": "number",
                    "description": "Pressure Bar",
                    "default": 40
                }
            },
            "required": [
                "ligand_cone_angle"
            ]
        }
    }
]