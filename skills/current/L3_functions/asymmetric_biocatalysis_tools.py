"""
L3 Tools: Enzyme-Catalyzed Asymmetric Reactions (Biocatalysis)
==============================================================
Dynamic kinetic resolution calculator, cofactor regeneration efficiency,
enantioselectivity predictor from E-value.

Parent L2: asymmetric_biocatalysis.md (Punniyamurthy Ch11)
L4 data: asymmetric_biocatalysis_data.md
"""

## Solver Instructions (for AI Agent)

# When you encounter **asymmetric biocatalysis / DKR** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - DKR enantiomeric excess and conversion: `dkr_calculator(conversion, ee_product)`
# - Enantioselectivity from E-value: `enantioselectivity_from_E(E_value, conversion)`
# - Cofactor regeneration efficiency: `cofactor_regeneration_efficiency(nadh_initial, nadh_final, product_mmol, substrate_mmol)`

### Step 2: Choose the correct function
# - DKR analysis: `dkr_calculator` - returns ee_substrate, ee_product, C, and diagnostic info
# - E-value analysis: `enantioselectivity_from_E` - determines if E-value is sufficient for target ee
# - Cofactor efficiency: `cofactor_regeneration_efficiency`

### Step 3: Handle special cases
# - DKR requires both high conversion AND high ee_product
# - E-value > 200 for ee > 99% at >50% conversion
# - `_solve_max_conversion` and `_dkr_diagnosis` are internal helpers

### Examples
# 1. Conversion=95%, ee_product=99%: `dkr_calculator(95, 99)` -> high ee_substrate, successful DKR
# 2. E=50, target ee=99%: `enantioselectivity_from_E(50)` -> may need higher E-value
# 3. NADH: 1.0 -> 0.2 mmol, product=0.8 mmol: `cofactor_regeneration_efficiency(1.0, 0.2, 0.8, 1.0)` -> 80% TTN



import math


def dkr_calculator(conversion: float, ee_product: float) -> dict:
    """Dynamic Kinetic Resolution calculator.
    
    In DKR: resolution + in situ racemization of unwanted enantiomer.
    Unlike simple kinetic resolution, DKR can theoretically give 100% yield
    at 100% ee. This function calculates key DKR metrics.
    
    Args:
        conversion: fractional conversion (0-1)
        ee_product: enantiomeric excess of product (0-100)
    
    Returns:
        dict with yield, ee, er, selectivity_factor_s, theoretical_max_yield,
              efficiency_score
    """
    c = max(0.0, min(1.0, conversion))
    ee = max(0.0, min(100.0, ee_product))
    
    er = (100 + ee) / (100 - ee) if ee < 100 else float('inf')
    yield_pct = c * 100
    
    # E-value (selectivity factor) from ee and conversion (Chen et al. equation)
    # E = ln[(1-c)(1-ee)] / ln[(1-c)(1+ee)]
    # where ee and c are fractional
    ee_frac = ee / 100
    if c > 0 and c < 1 and ee_frac > 0 and ee_frac < 1:
        try:
            num = math.log((1 - c) * (1 - ee_frac))
            den = math.log((1 - c) * (1 + ee_frac))
            E = num / den if abs(den) > 1e-10 else float('inf')
        except (ValueError, ZeroDivisionError):
            E = float('inf')
    else:
        E = float('inf') if ee >= 99 else 0
    
    # Theoretical max yield at 99% ee for given E
    if E > 1 and E != float('inf'):
        # c_max at ee=99%: solve E = ln[(1-c)(0.01)] / ln[(1-c)(1.99)]
        # Iterative solution
        c_max = _solve_max_conversion(E, 0.99)
    elif E == float('inf'):
        c_max = 1.0
    else:
        c_max = 0.5  # No DKR benefit if E < 1
    
    # DKR efficiency: actual yield at given ee vs theoretical simple KR max (50%)
    kr_max = 0.5
    dkr_improvement = (yield_pct / 100) / kr_max if kr_max > 0 else 0
    
    # Check if results consistent with DKR vs simple KR
    is_dkr = yield_pct > 50  # If yield > 50%, it must be DKR
    
    return {
        'conversion': round(c, 4),
        'yield_pct': round(yield_pct, 1),
        'product_ee': round(ee, 1),
        'product_er': round(er, 2),
        'E_value': round(E, 1) if E != float('inf') else '>1000',
        'theoretical_max_yield_at_99ee': round(c_max * 100, 1),
        'dkr_vs_kr_improvement': round(dkr_improvement, 2),
        'is_consistent_with_dkr': is_dkr,
        'diagnosis': _dkr_diagnosis(c, ee, E, is_dkr)
    }


def _solve_max_conversion(E: float, target_ee: float, tol: float = 1e-6) -> float:
    """Numerically solve for max conversion at target ee given E-value."""
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        try:
            num = math.log((1 - mid) * (1 - target_ee))
            den = math.log((1 - mid) * (1 + target_ee))
            E_calc = num / den
        except (ValueError, ZeroDivisionError):
            lo = mid
            continue
        if E_calc > E:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


def _dkr_diagnosis(c, ee, E, is_dkr):
    """Generate diagnostic message for DKR results."""
    if c > 0.9 and ee > 95:
        return "Excellent DKR: High conversion and ee indicate effective racemization"
    elif c > 0.7 and ee > 90:
        return "Good DKR: Both racemization and resolution working well"
    elif c > 0.5 and ee > 80:
        return "Moderate DKR: Racemization may be rate-limiting"
    elif is_dkr and ee < 70:
        return "DKR active but selectivity needs improvement - consider different enzyme or ligand"
    elif not is_dkr and c < 0.5:
        return "Simple kinetic resolution (no DKR): Max yield limited to 50%"
    else:
        return "Intermediate results - optimize racemization catalyst or enzyme loading"


def cofactor_regeneration_efficiency(nadh_initial_umol: float,
                                      nadh_consumed_umol: float,
                                      cosubstrate_mmol: float = None,
                                      ttn_target: int = 1000) -> dict:
    """Calculate cofactor regeneration efficiency.
    
    Common systems: GDH/glucose, FDH/formate, ADH/2-propanol.
    Total Turnover Number (TTN) = product formed / cofactor used.
    
    Args:
        nadh_initial_umol: initial NAD(P)H (umol)
        nadh_consumed_umol: NAD(P)H consumed (umol, equals cofactor turnover)
        cosubstrate_mmol: cosubstrate used for regeneration (mmol), optional
        ttn_target: target TTN for industrial viability
    
    Returns:
        dict with ttn, efficiency, regeneration_cost, viability
    """
    ttn = nadh_consumed_umol / nadh_initial_umol if nadh_initial_umol > 0 else 0
    
    # Theoretical max TTN from cosubstrate stoichiometry (1:1 for most systems)
    if cosubstrate_mmol is not None:
        cosubstrate_umol = cosubstrate_mmol * 1000
        theoretical_max_ttn = cosubstrate_umol / nadh_initial_umol
        cosubstrate_utilization = (nadh_consumed_umol / cosubstrate_umol * 100) if cosubstrate_umol > 0 else 0
    else:
        theoretical_max_ttn = None
        cosubstrate_utilization = None
    
    # Cofactor cost assessment (NADH ~$500/g, ~$5/umol at prep scale)
    cofactor_cost_per_mmol_product = (nadh_initial_umol / nadh_consumed_umol) if nadh_consumed_umol > 0 else float('inf')
    
    # Viability thresholds
    if ttn >= ttn_target:
        viability = 'excellent'
    elif ttn >= 500:
        viability = 'good'
    elif ttn >= 100:
        viability = 'acceptable'
    elif ttn >= 20:
        viability = 'marginal'
    else:
        viability = 'poor'
    
    # Regeneration method recommendation
    if ttn < 100:
        recommendation = "Switch to whole-cell system or improve regeneration enzyme"
    elif ttn < 500:
        recommendation = "Consider GDH/glucose (irreversible) or increase cosubstrate"
    else:
        recommendation = "Current system viable; optimize for higher substrate loading"
    
    return {
        'TTN': round(ttn, 1),
        'cofactor_initial_umol': nadh_initial_umol,
        'cofactor_turnovers': round(nadh_consumed_umol, 1),
        'theoretical_max_ttn': round(theoretical_max_ttn, 1) if theoretical_max_ttn else 'N/A',
        'cosubstrate_utilization_pct': round(cosubstrate_utilization, 1) if cosubstrate_utilization else 'N/A',
        'cofactor_relative_cost': round(cofactor_cost_per_mmol_product, 4),
        'viability': viability,
        'meets_target': ttn >= ttn_target,
        'recommendation': recommendation
    }


def enantioselectivity_from_E(E_value: float, conversion: float = None) -> dict:
    """Predict ee from E-value (and optionally conversion).
    
    E-value: enantioselectivity = (k_fast / k_slow) for enzyme kinetic resolution.
    High E (>200) = excellent, E~20 = moderate, E<5 = poor.
    
    At given conversion c (fractional):
      ee = (E-1) / (E+1) * (1 + c*E) / (1 + c)  ... but simplified:
      ee(c) ~ [c(E-1)] / [c(E+1) - 2c^2*E/(c+1)] ... use Chen equation inverse
    
    Args:
        E_value: selectivity factor (1 to infinity)
        conversion: optional fractional conversion for ee prediction
    
    Returns:
        dict with E classification, ee predictions, recommendations
    """
    E = max(1.0, E_value)
    
    # Classification
    if E >= 200:
        category = 'excellent'
        color = 'green'
    elif E >= 50:
        category = 'good'
        color = 'green'
    elif E >= 20:
        category = 'moderate'
        color = 'yellow'
    elif E >= 5:
        category = 'low'
        color = 'orange'
    else:
        category = 'poor'
        color = 'red'
    
    # Max ee at 50% conversion (standard KR)
    ee_max_50 = (E - 1) / (E + 1) * 100
    
    # ee at various conversions
    conversions = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
    ee_at_c = {}
    for c in conversions:
        ee_frac = (E - 1) * c / (E + 1 - 2 * c) if (E + 1 - 2 * c) > 0 else 100
        ee_frac = min(100, max(0, ee_frac * 100))
        ee_at_c[f'{int(c*100)}%'] = round(ee_frac, 1)
    
    # If specific conversion given
    if conversion is not None and 0 < conversion < 1:
        c = conversion
        ee_at_c_val = (E - 1) * c / (E + 1 - 2 * c) if (E + 1 - 2 * c) > 0 else 100
        ee_at_c_val = min(100, max(0, ee_at_c_val * 100))
    else:
        ee_at_c_val = None
        conversion = 0.5  # default
    
    # Recommended conversion for >95% ee
    if E > 1:
        c_95 = (E + 1) * 0.95 / ((E - 1) + 2 * 0.95) if E > 1 else 0.5
        c_95 = min(c_95, 0.99)
    else:
        c_95 = None
    
    return {
        'E_value': E if E < 10000 else '>10000',
        'category': category,
        'max_ee_at_50pct_conversion': round(ee_max_50, 1),
        'ee_at_conversion': round(ee_at_c_val, 1) if ee_at_c_val else 'N/A',
        'ee_table': ee_at_c,
        'conversion_for_95pct_ee': round(c_95 * 100, 1) if c_95 else 'unachievable',
        'recommendation': f"{'Use for resolution' if E >= 20 else 'DKR needed' if E >= 5 else 'Not viable for resolution - use DKR or different enzyme'}"
    }


# ── Test Suite ────────────────────────────────────────────────────────

def _run_tests():
    tests_passed = 0
    tests_total = 0
    
    print("=" * 60)
    print("Biocatalysis Tools - Test Suite")
    print("=" * 60)
    
    # Test 1: DKR basic
    tests_total += 1
    r = dkr_calculator(0.92, 99.0)
    assert r['product_ee'] == 99.0
    assert r['yield_pct'] == 92.0
    assert r['is_consistent_with_dkr'] == True
    tests_passed += 1
    print(f"[PASS] Test 1: DKR basic - yield={r['yield_pct']}%, ee={r['product_ee']}%")
    
    # Test 2: DKR E-value calculation
    tests_total += 1
    r = dkr_calculator(0.50, 90.0)
    assert isinstance(r['E_value'], (int, float)), f"E should be numeric: {r['E_value']}"
    assert r['E_value'] > 10, f"E should be >10 for 90% ee at 50% conversion"
    tests_passed += 1
    print(f"[PASS] Test 2: E-value from 90% ee/50% conversion = {r['E_value']}")
    
    # Test 3: Simple KR detection (yield < 50%)
    tests_total += 1
    r = dkr_calculator(0.40, 80.0)
    assert r['is_consistent_with_dkr'] == False
    tests_passed += 1
    print(f"[PASS] Test 3: Simple KR detected (40% conv < 50%)")
    
    # Test 4: Cofactor regeneration TTN
    tests_total += 1
    r = cofactor_regeneration_efficiency(0.01, 10.0, cosubstrate_mmol=20.0)
    assert r['TTN'] == 1000.0
    assert r['viability'] == 'excellent'
    tests_passed += 1
    print(f"[PASS] Test 4: TTN=1000, viability={r['viability']}")
    
    # Test 5: Poor cofactor regeneration
    tests_total += 1
    r = cofactor_regeneration_efficiency(1.0, 5.0)
    assert r['TTN'] == 5.0
    assert r['viability'] == 'poor'
    tests_passed += 1
    print(f"[PASS] Test 5: TTN=5, viability={r['viability']}")
    
    # Test 6: E-value classification
    tests_total += 1
    r = enantioselectivity_from_E(200)
    assert r['category'] == 'excellent'
    assert r['max_ee_at_50pct_conversion'] >= 99.0
    tests_passed += 1
    print(f"[PASS] Test 6: E=200, category={r['category']}, max ee={r['max_ee_at_50pct_conversion']}")
    
    # Test 7: E-value table
    tests_total += 1
    r = enantioselectivity_from_E(20)
    table = r['ee_table']
    assert table['50%'] > table['25%'], "ee should increase with conversion for E>1"
    assert table['90%'] > table['50%']
    tests_passed += 1
    print(f"[PASS] Test 7: E=20 ee table: 25%={table['25%']}%, 50%={table['50%']}%, 90%={table['90%']}%")
    
    # Test 8: Low E-value
    tests_total += 1
    r = enantioselectivity_from_E(3)
    assert r['category'] == 'poor'
    tests_passed += 1
    print(f"[PASS] Test 8: E=3, category={r['category']}")
    
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
        "name": "cofactor_regeneration_efficiency",
        "description": "Calculate cofactor regeneration efficiency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nadh_initial_umol": {
                    "type": "number",
                    "description": "Nadh Initial Umol"
                },
                "nadh_consumed_umol": {
                    "type": "number",
                    "description": "Nadh Consumed Umol"
                },
                "cosubstrate_mmol": {
                    "type": "number",
                    "description": "Cosubstrate Mmol",
                    "default": None
                },
                "ttn_target": {
                    "type": "number",
                    "description": "Ttn Target",
                    "default": 1000
                }
            },
            "required": [
                "nadh_initial_umol",
                "nadh_consumed_umol"
            ]
        }
    },
    {
        "name": "dkr_calculator",
        "description": "Dynamic Kinetic Resolution calculator.",
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
                }
            },
            "required": [
                "conversion",
                "ee_product"
            ]
        }
    },
    {
        "name": "enantioselectivity_from_E",
        "description": "Predict ee from E-value (and optionally conversion).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "E_value": {
                    "type": "number",
                    "description": "E Value"
                },
                "conversion": {
                    "type": "number",
                    "description": "Conversion",
                    "default": None
                }
            },
            "required": [
                "E_value"
            ]
        }
    }
]