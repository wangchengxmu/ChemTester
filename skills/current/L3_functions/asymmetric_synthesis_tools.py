"""
Asymmetric Synthesis Tools (L3)
================================
Functions for calculating stereoselectivity metrics and predicting
enantioselective reaction outcomes.

Functions:
    calculate_ee          - Enantiomeric excess from observed/total yield
    calculate_dr          - Diastereomeric ratio
    calculate_er          - Enantiomeric ratio
    calculate_de          - Diastereomeric excess
    sharpless_epoxidation_prediction - Predict absolute config via Sharpless rules
    proline_catalyzed_aldol_substrate_check - Check substrate suitability
    catalyst_loading_optimization - Suggest catalyst loading adjustment
    binap_substrate_compatibility - Check BINAP-Ru substrate compatibility
"""

## Solver Instructions (for AI Agent)

# When you encounter **asymmetric synthesis** (ee, dr, er, catalyst prediction) problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Calculate ee/dr/er/de: `calculate_ee(major, minor)`, `calculate_dr(major_diast, minor_diast)`, `calculate_er(major, minor)`, `calculate_de(major_diast, minor_diast)`
# - Sharpless epoxidation prediction: `sharpless_epoxidation_prediction(allylic_alcohol_smiles, tartrate)`
# - Proline aldol substrate check: `proline_catalyzed_aldol_substrate_check(aldehyde_smiles)`
# - Catalyst loading optimization: `catalyst_loading_optimization(loading_data, target_ee)`
# - BINAP compatibility: `binap_substrate_compatibility(substrate_class)`
# - Conversions: `ee_to_er(ee_percent)`, `er_to_ee(er)`, `dr_to_de(dr)`

### Step 2: Choose the correct function
# - From HPLC/GC data: `calculate_ee` (enantiomers) or `calculate_dr` (diastereomers)
# - Predict reaction outcome: `sharpless_epoxidation_prediction`, `proline_catalyzed_aldol_substrate_check`
# - Between representations: `ee_to_er`, `er_to_ee`, `dr_to_de`

### Step 3: Handle special cases
# - ee = |major - minor| / (major + minor) x 100
# - er = major/minor (always ≥ 1 in convention)
# - Sharpless: L-(+)-DET gives (2S) epoxy alcohol from E-allylic alcohols
# - `_classify_allylic_alcohol` is an internal helper

### Examples
# 1. HPLC: 90.5% and 9.5%: `calculate_ee(90.5, 9.5)` -> 81% ee; `calculate_er(90.5, 9.5)` -> 9.53:1
# 2. Sharpless: `sharpless_epoxidation_prediction("CC=CCO", "L-(+)-DET")` -> predicts product configuration
# 3. 99% ee to er: `ee_to_er(99)` -> er ~ 199:1



from __future__ import annotations
from typing import Optional, Tuple


# ---------------------------------------------------------------------------
# Core stereoselectivity calculations
# ---------------------------------------------------------------------------

def calculate_ee(major_enantiomer: float, minor_enantiomer: float) -> float:
    """Calculate enantiomeric excess (ee%).

    Parameters
    ----------
    major_enantiomer : float
        Yield or amount of the major enantiomer (any consistent unit).
    minor_enantiomer : float
        Yield or amount of the minor enantiomer.

    Returns
    -------
    float
        Enantiomeric excess as a percentage (0-100).

    Examples
    --------
    >>> calculate_ee(0.48, 0.02)
    92.0
    """
    total = major_enantiomer + minor_enantiomer
    if total == 0:
        return 0.0
    return abs(major_enantiomer - minor_enantiomer) / total * 100


def calculate_dr(major_diast: float, minor_diast: float) -> float:
    """Calculate diastereomeric ratio (dr).

    Parameters
    ----------
    major_diast : float
        Yield or amount of the major diastereomer.
    minor_diast : float
        Yield or amount of the minor diastereomer.

    Returns
    -------
    float
        Diastereomeric ratio (major:minor). Returns inf if minor is 0.

    Examples
    --------
    >>> calculate_dr(0.85, 0.15)
    5.67
    """
    if minor_diast == 0:
        return float('inf')
    return major_diast / minor_diast


def calculate_er(major_enantiomer: float, minor_enantiomer: float) -> float:
    """Calculate enantiomeric ratio (er).

    Parameters
    ----------
    major_enantiomer : float
        Yield or amount of the major enantiomer.
    minor_enantiomer : float
        Yield or amount of the minor enantiomer.

    Returns
    -------
    float
        Enantiomeric ratio (major:minor). Returns inf if minor is 0.

    Examples
    --------
    >>> calculate_er(0.48, 0.02)
    24.0
    """
    if minor_enantiomer == 0:
        return float('inf')
    return major_enantiomer / minor_enantiomer


def calculate_de(major_diast: float, minor_diast: float) -> float:
    """Calculate diastereomeric excess (de%).

    Parameters
    ----------
    major_diast, minor_diast : float
        Yields of each diastereomer.

    Returns
    -------
    float
        Diastereomeric excess as a percentage (0-100).
    """
    total = major_diast + minor_diast
    if total == 0:
        return 0.0
    return abs(major_diast - minor_diast) / total * 100


# ---------------------------------------------------------------------------
# Sharpless Epoxidation Prediction
# ---------------------------------------------------------------------------

# Simplified SMILES-based detection of allylic alcohol geometry
def _classify_allylic_alcohol(smiles: str) -> Optional[dict]:
    """Parse SMILES to classify allylic alcohol for Sharpless rules.

    Returns dict with keys: 'has_allylic_alcohol', 'geometry' (E/Z/unknown),
    'substitution' (1,2,3), or None if not an allylic alcohol.
    """
    smiles_upper = smiles.upper()
    has_oh = 'O' in smiles_upper and not 'O=' in smiles_upper  # rough check

    # Check for C=C pattern (simplified)
    has_double_bond = False
    for i in range(len(smiles) - 1):
        if smiles[i] == '=' or (smiles[i] == '/' or smiles[i] == '\\'):
            has_double_bond = True
            break

    if not (has_oh and has_double_bond):
        return None

    # Determine geometry from SMILES notation
    geometry = 'unknown'
    if '/' in smiles and '\\' in smiles:
        geometry = 'E'  # trans
    elif '/' in smiles or '\\' in smiles:
        geometry = 'E'  # simplified
    elif 'C=C' in smiles_upper:
        geometry = 'E'  # default assumption

    # Determine substitution
    substitution = 1
    # Count groups around double bond (very simplified heuristic)
    if 'C(' in smiles or 'C)' in smiles:
        substitution = 3
    elif any(smiles[i] == '(' for i in range(min(10, len(smiles)))):
        substitution = 2

    return {
        'has_allylic_alcohol': True,
        'geometry': geometry,
        'substitution': substitution,
    }


def sharpless_epoxidation_prediction(
    allylic_alcohol_smiles: str,
    tartrate: str = "L-(+)-DET",
) -> dict:
    """Predict absolute configuration of epoxy alcohol via Sharpless rules.

    Applies the empirical Sharpless epoxidation model:
    - L-(+)-DET or L-(+)-DIPT -> oxygen delivered from bottom face
    - D-(−)-DET or D-(−)-DIPT -> oxygen delivered from top face

    Parameters
    ----------
    allylic_alcohol_smiles : str
        SMILES of the allylic alcohol substrate.
    tartrate : str
        Tartrate ester used. Options: 'L-(+)-DET', 'D-(-)-DET',
        'L-(+)-DIPT', 'D-(-)-DIPT'.

    Returns
    -------
    dict
        Keys: 'predicted_config' (e.g. '2S,3S'), 'tartrate',
        'oxygen_face', 'substrate_info', 'note'.

    Examples
    --------
    >>> result = sharpless_epoxidation_prediction("C/C=C\\CO", "L-(+)-DET")
    >>> result['oxygen_face']
    'bottom'
    """
    substrate_info = _classify_allylic_alcohol(allylic_alcohol_smiles)

    tartrate_upper = tartrate.upper().replace(' ', '')

    is_L = 'L' in tartrate_upper and '+' in tartrate
    is_D = 'D' in tartrate_upper and '-' in tartrate

    if not (is_L or is_D):
        return {
            'predicted_config': 'unknown',
            'tartrate': tartrate,
            'oxygen_face': 'unknown',
            'substrate_info': substrate_info,
            'note': f'Unrecognized tartrate: {tartrate}. Use L-(+)-DET, D-(-)-DET, L-(+)-DIPT, or D-(-)-DIPT.',
        }

    if substrate_info is None:
        return {
            'predicted_config': 'unknown',
            'tartrate': tartrate,
            'oxygen_face': 'bottom' if is_L else 'top',
            'substrate_info': None,
            'note': 'SMILES may not represent an allylic alcohol. Prediction assumes E-geometry.',
        }

    # Sharpless rules
    if is_L:
        # L-(+)-DET/DIPT: oxygen from bottom face -> (2S,3S) for E-allylic alcohols
        oxygen_face = 'bottom'
        if substrate_info['geometry'] == 'E':
            predicted_config = '2S,3S'
        else:
            predicted_config = '2S,3S (assuming E-geometry)'
    else:
        # D-(−)-DET/DIPT: oxygen from top face -> (2R,3R)
        oxygen_face = 'top'
        if substrate_info['geometry'] == 'E':
            predicted_config = '2R,3R'
        else:
            predicted_config = '2R,3R (assuming E-geometry)'

    return {
        'predicted_config': predicted_config,
        'tartrate': tartrate,
        'oxygen_face': oxygen_face,
        'substrate_info': substrate_info,
        'note': 'Prediction for E-allylic alcohols. Z-substrates may give different results.',
    }


# ---------------------------------------------------------------------------
# Proline-Catalyzed Aldol Substrate Check
# ---------------------------------------------------------------------------

def proline_catalyzed_aldol_substrate_check(aldehyde_smiles: str) -> dict:
    """Check if an aldehyde is suitable for L-proline-catalyzed aldol reaction.

    Proline catalysis works best with:
    - Aromatic aldehydes (benzaldehydes, cinnamaldehydes)
    - Aliphatic aldehydes (propionaldehyde, butyraldehyde)
    - alpha,beta-unsaturated aldehydes (enals)

    Poor substrates:
    - Sterically hindered aldehydes (ortho-substituted aromatics)
    - alpha-branched aldehydes
    - Strongly electron-withdrawing aldehydes

    Parameters
    ----------
    aldehyde_smiles : str
        SMILES of the aldehyde substrate.

    Returns
    -------
    dict
        Keys: 'suitable' (bool), 'category', 'expected_ee_range',
        'recommendations', 'warnings'.
    """
    smiles_upper = aldehyde_smiles.upper()
    result = {
        'suitable': True,
        'category': 'unknown',
        'expected_ee_range': '70-95%',
        'recommendations': [],
        'warnings': [],
    }

    # Check for aldehyde group
    has_aldehyde = False
    for i in range(len(aldehyde_smiles)):
        if aldehyde_smiles[i] == '=' and i + 1 < len(aldehyde_smiles) and aldehyde_smiles[i + 1].upper() == 'O':
            has_aldehyde = True
            break
    if not has_aldehyde:
        result['suitable'] = False
        result['warnings'].append('No aldehyde (C=O) group detected in SMILES.')
        return result

    # Classify substrate
    if 'C1=CC' in aldehyde_smiles or 'c1cc' in aldehyde_smiles.lower() or 'C1=CC=C' in aldehyde_smiles:
        result['category'] = 'aromatic'
        result['expected_ee_range'] = '80-99%'
        # Check for ortho substitution
        if 'C(C)' in aldehyde_smiles[:15]:
            result['expected_ee_range'] = '50-80%'
            result['warnings'].append('Possible ortho-substitution may reduce ee.')
    elif 'C=CC=O' in aldehyde_smiles or 'C/C=C' in aldehyde_smiles:
        result['category'] = 'enals (alpha,beta-unsaturated)'
        result['expected_ee_range'] = '85-99%'
        result['recommendations'].append('Consider iminium activation pathway.')
    else:
        result['category'] = 'aliphatic'
        result['expected_ee_range'] = '70-90%'
        result['recommendations'].append('Use 20-30 mol% L-proline in DMSO or DMF.')
        result['recommendations'].append('Additives like 4-nitrobenzoic acid may improve yield.')

    # Check for steric hindrance
    if aldehyde_smiles.count('(') >= 3:
        result['warnings'].append('Highly branched substrate may have steric issues.')
        result['expected_ee_range'] = '40-70%'

    return result


# ---------------------------------------------------------------------------
# Catalyst Loading Optimization
# ---------------------------------------------------------------------------

def catalyst_loading_optimization(
    current_yield: float,
    current_ee: float,
    target_ee: float,
    current_loading: float = 20.0,
    min_loading: float = 1.0,
    max_loading: float = 50.0,
) -> dict:
    """Suggest catalyst loading adjustment based on current vs target ee.

    Heuristic model: ee generally increases with catalyst loading up to
    a plateau. This function suggests a new loading to reach target ee.

    Parameters
    ----------
    current_yield : float
        Current isolated yield (%).
    current_ee : float
        Current enantiomeric excess (%).
    target_ee : float
        Target enantiomeric excess (%).
    current_loading : float
        Current catalyst loading (mol%).
    min_loading, max_loading : float
        Allowed loading range (mol%).

    Returns
    -------
    dict
        Keys: 'suggested_loading', 'action', 'confidence', 'note'.
    """
    if current_ee >= target_ee:
        return {
            'suggested_loading': current_loading,
            'action': 'no_change',
            'confidence': 'high',
            'note': f'Current ee ({current_ee}%) already meets target ({target_ee}%). Consider reducing loading to optimize cost.',
        }

    # Calculate gap and estimate loading change
    # Heuristic: ~2-5 mol% increase per ~5% ee improvement near plateau
    ee_gap = target_ee - current_ee
    estimated_increase = min(ee_gap * 0.6, max_loading - current_loading)
    suggested = min(current_loading + estimated_increase, max_loading)

    if suggested > max_loading:
        action = 'change_method'
        note = (f'Cannot reach {target_ee}% ee by loading alone. '
                f'Consider: different catalyst, lower temperature, or substrate modification.')
    elif ee_gap > 20:
        action = 'significant_increase'
        note = (f'Large ee gap ({ee_gap}%). Consider alternative catalyst system '
                f'rather than just increasing loading.')
    else:
        action = 'moderate_increase'
        note = (f'Suggest increasing loading from {current_loading} to ~{suggested:.1f} mol%. '
                f'Try at lower temperature first (-20degC to -40degC).')

    return {
        'suggested_loading': round(suggested, 1),
        'action': action,
        'confidence': 'medium',
        'note': note,
    }


# ---------------------------------------------------------------------------
# BINAP-Ru Substrate Compatibility
# ---------------------------------------------------------------------------

# Compatibility database
_BINAP_COMPATIBILITY = {
    'unsaturated_carboxylic_acid': {
        'compatible': True,
        'metal': 'Ru(II)',
        'typical_ee': '95-99%',
        'conditions': 'H2 (50-100 atm), MeOH',
        'note': 'Excellent substrate class. Example: (S)-Naproxen synthesis.',
    },
    'unsaturated_ester': {
        'compatible': True,
        'metal': 'Ru(II)',
        'typical_ee': '90-98%',
        'conditions': 'H2 (50-100 atm)',
        'note': 'Good compatibility. beta,beta-disubstituted may give lower ee.',
    },
    'allylic_alcohol': {
        'compatible': True,
        'metal': 'Ru(II) / Ir',
        'typical_ee': '94-99%',
        'conditions': 'H2 (50-100 atm)',
        'note': 'Geraniol -> (S)-citronellol (94% ee). Ir-phosphanodihydrooxazole alternative.',
    },
    'allylic_amine': {
        'compatible': True,
        'metal': 'Rh(I)-BINAP',
        'typical_ee': '96-99%',
        'conditions': 'Isomerization-hydrogenation',
        'note': 'Works via isomerization mechanism. Example: citronellal synthesis.',
    },
    'enamide': {
        'compatible': True,
        'metal': 'Rh(I)-BINAP/DIPAMP/DuPHOS',
        'typical_ee': '95-99%',
        'conditions': 'H2 (1-4 atm), MeOH',
        'note': 'Best substrate class for Rh catalysts. DIPAMP > BINAP for amino acids.',
    },
    'ketone': {
        'compatible': True,
        'metal': 'Ru(II)-BINAP/diamine (Noyori)',
        'typical_ee': '95-99%',
        'conditions': 'H2 (1-10 atm) or transfer H2',
        'note': 'Requires bifunctional Ru-BINAP/diamine system. Noyori transfer hydrogenation.',
    },
    'imine': {
        'compatible': True,
        'metal': 'Rh(I) or Ir',
        'typical_ee': '80-95%',
        'conditions': 'H2 (1-10 atm)',
        'note': 'Less developed. Chiral phosphine-oxazoline ligands may be better.',
    },
    'simple_alkene': {
        'compatible': False,
        'metal': 'N/A',
        'typical_ee': 'N/A',
        'conditions': 'N/A',
        'note': 'BINAP-Ru requires coordinating group (COOH, OH, NR2, CONH2). Use asymmetric epoxidation or dihydroxylation instead.',
    },
}


def binap_substrate_compatibility(substrate_class: str) -> dict:
    """Check BINAP-Ru substrate compatibility.

    Parameters
    ----------
    substrate_class : str
        Substrate class identifier. Recognized values:
        'unsaturated_carboxylic_acid', 'unsaturated_ester', 'allylic_alcohol',
        'allylic_amine', 'enamide', 'ketone', 'imine', 'simple_alkene'.
        Partial matching is supported (e.g., 'acid', 'ketone').

    Returns
    -------
    dict
        Compatibility info with keys: 'compatible', 'metal', 'typical_ee',
        'conditions', 'note', 'matched_class'.
    """
    substrate_lower = substrate_class.lower().strip()

    # Try exact match first
    if substrate_lower in _BINAP_COMPATIBILITY:
        info = _BINAP_COMPATIBILITY[substrate_lower].copy()
        info['matched_class'] = substrate_lower
        return info

    # Fuzzy match
    for key, info in _BINAP_COMPATIBILITY.items():
        if substrate_lower in key or key in substrate_lower:
            result = info.copy()
            result['matched_class'] = key
            return result

    # Keyword matching
    keyword_map = {
        'acid': 'unsaturated_carboxylic_acid',
        'ester': 'unsaturated_ester',
        'alcohol': 'allylic_alcohol',
        'amine': 'allylic_amine',
        'enamide': 'enamide',
        'ketone': 'ketone',
        'imine': 'imine',
        'alkene': 'simple_alkene',
        'olefin': 'simple_alkene',
    }

    for kw, mapped in keyword_map.items():
        if kw in substrate_lower:
            info = _BINAP_COMPATIBILITY[mapped].copy()
            info['matched_class'] = mapped
            return info

    return {
        'compatible': None,
        'metal': 'unknown',
        'typical_ee': 'unknown',
        'conditions': 'unknown',
        'note': f'Unrecognized substrate class: "{substrate_class}". '
                f'Known classes: {", ".join(_BINAP_COMPATIBILITY.keys())}',
        'matched_class': None,
    }


# ---------------------------------------------------------------------------
# Convenience conversions
# ---------------------------------------------------------------------------

def ee_to_er(ee_percent: float) -> float:
    """Convert ee (%) to enantiomeric ratio.

    >>> ee_to_er(90.0)
    19.0
    """
    minor = (100 - ee_percent) / 2
    if minor == 0:
        return float('inf')
    return (ee_percent + 100) / 2 / minor


def er_to_ee(er: float) -> float:
    """Convert enantiomeric ratio to ee (%).

    >>> er_to_ee(19.0)
    90.0
    """
    if er == float('inf'):
        return 100.0
    return (er - 1) / (er + 1) * 100


def dr_to_de(dr: float) -> float:
    """Convert diastereomeric ratio to diastereomeric excess (%).

    >>> dr_to_de(9.0)
    80.0
    """
    if dr == float('inf'):
        return 100.0
    return (dr - 1) / (dr + 1) * 100


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Asymmetric Synthesis Tools - Test Suite")
    print("=" * 60)

    # Test calculate_ee
    assert abs(calculate_ee(0.48, 0.02) - 92.0) < 0.01
    assert calculate_ee(0.5, 0.5) == 0.0
    assert calculate_ee(1.0, 0.0) == 100.0
    print("[PASS] calculate_ee")

    # Test calculate_dr
    assert abs(calculate_dr(0.85, 0.15) - 5.6667) < 0.01
    assert calculate_dr(1.0, 0.0) == float('inf')
    print("[PASS] calculate_dr")

    # Test calculate_er
    assert calculate_er(0.48, 0.02) == 24.0
    assert calculate_er(1.0, 0.0) == float('inf')
    print("[PASS] calculate_er")

    # Test calculate_de
    assert abs(calculate_de(0.9, 0.1) - 80.0) < 0.01
    print("[PASS] calculate_de")

    # Test conversions
    assert abs(ee_to_er(90.0) - 19.0) < 0.01
    assert abs(er_to_ee(19.0) - 90.0) < 0.01
    assert abs(dr_to_de(9.0) - 80.0) < 0.01
    print("[PASS] ee_to_er, er_to_ee, dr_to_de")

    # Test Sharpless prediction
    r1 = sharpless_epoxidation_prediction("C/C=C\\CO", "L-(+)-DET")
    assert r1['oxygen_face'] == 'bottom'
    assert '2S,3S' in r1['predicted_config']
    print(f"[PASS] Sharpless L-(+)-DET -> {r1['predicted_config']}")

    r2 = sharpless_epoxidation_prediction("C/C=C\\CO", "D-(-)-DET")
    assert r2['oxygen_face'] == 'top'
    assert '2R,3R' in r2['predicted_config']
    print(f"[PASS] Sharpless D-(-)-DET -> {r2['predicted_config']}")

    # Test proline substrate check
    p1 = proline_catalyzed_aldol_substrate_check("c1ccccc1C=O")  # benzaldehyde
    assert p1['suitable'] is True
    assert 'aromatic' in p1['category']
    print(f"[PASS] Proline check benzaldehyde -> {p1['category']}, ee {p1['expected_ee_range']}")

    # Test catalyst loading
    c1 = catalyst_loading_optimization(85, 80, 95, 20)
    assert c1['suggested_loading'] > 20
    print(f"[PASS] Catalyst loading -> {c1['suggested_loading']} mol%, {c1['action']}")

    c2 = catalyst_loading_optimization(90, 98, 95, 20)
    assert c2['action'] == 'no_change'
    print(f"[PASS] Catalyst loading no change -> {c2['action']}")

    # Test BINAP compatibility
    b1 = binap_substrate_compatibility('unsaturated_carboxylic_acid')
    assert b1['compatible'] is True
    print(f"[PASS] BINAP acid -> compatible, ee {b1['typical_ee']}")

    b2 = binap_substrate_compatibility('simple_alkene')
    assert b2['compatible'] is False
    print(f"[PASS] BINAP alkene -> not compatible")

    b3 = binap_substrate_compatibility('ketone')
    assert b3['compatible'] is True
    print(f"[PASS] BINAP ketone -> compatible (Noyori)")

    print("\nAll tests passed! [PASS]")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "binap_substrate_compatibility",
        "description": "Check BINAP-Ru substrate compatibility.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "substrate_class": {
                    "type": "number",
                    "description": "Substrate Class"
                }
            },
            "required": [
                "substrate_class"
            ]
        }
    },
    {
        "name": "calculate_de",
        "description": "Calculate diastereomeric excess (de%).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "major_diast": {
                    "type": "number",
                    "description": "Major Diast"
                },
                "minor_diast": {
                    "type": "number",
                    "description": "Minor Diast"
                }
            },
            "required": [
                "major_diast",
                "minor_diast"
            ]
        }
    },
    {
        "name": "calculate_dr",
        "description": "Calculate diastereomeric ratio (dr).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "major_diast": {
                    "type": "number",
                    "description": "Major Diast"
                },
                "minor_diast": {
                    "type": "number",
                    "description": "Minor Diast"
                }
            },
            "required": [
                "major_diast",
                "minor_diast"
            ]
        }
    },
    {
        "name": "calculate_ee",
        "description": "Calculate enantiomeric excess (ee%).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "major_enantiomer": {
                    "type": "number",
                    "description": "Major Enantiomer"
                },
                "minor_enantiomer": {
                    "type": "number",
                    "description": "Minor Enantiomer"
                }
            },
            "required": [
                "major_enantiomer",
                "minor_enantiomer"
            ]
        }
    },
    {
        "name": "calculate_er",
        "description": "Calculate enantiomeric ratio (er).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "major_enantiomer": {
                    "type": "number",
                    "description": "Major Enantiomer"
                },
                "minor_enantiomer": {
                    "type": "number",
                    "description": "Minor Enantiomer"
                }
            },
            "required": [
                "major_enantiomer",
                "minor_enantiomer"
            ]
        }
    },
    {
        "name": "catalyst_loading_optimization",
        "description": "Suggest catalyst loading adjustment based on current vs target ee.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_yield": {
                    "type": "number",
                    "description": "Current Yield"
                },
                "current_ee": {
                    "type": "number",
                    "description": "Current Ee"
                },
                "target_ee": {
                    "type": "number",
                    "description": "Target Ee"
                },
                "current_loading": {
                    "type": "number",
                    "description": "Current Loading",
                    "default": 20.0
                },
                "min_loading": {
                    "type": "number",
                    "description": "Min Loading",
                    "default": 1.0
                },
                "max_loading": {
                    "type": "number",
                    "description": "Max Loading",
                    "default": 50.0
                }
            },
            "required": [
                "current_yield",
                "current_ee",
                "target_ee"
            ]
        }
    },
    {
        "name": "dr_to_de",
        "description": "Convert diastereomeric ratio to diastereomeric excess (%).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dr": {
                    "type": "number",
                    "description": "Dr"
                }
            },
            "required": [
                "dr"
            ]
        }
    },
    {
        "name": "ee_to_er",
        "description": "Convert ee (%) to enantiomeric ratio.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ee_percent": {
                    "type": "number",
                    "description": "Ee Percent"
                }
            },
            "required": [
                "ee_percent"
            ]
        }
    },
    {
        "name": "er_to_ee",
        "description": "Convert enantiomeric ratio to ee (%).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "er": {
                    "type": "number",
                    "description": "Er"
                }
            },
            "required": [
                "er"
            ]
        }
    },
    {
        "name": "proline_catalyzed_aldol_substrate_check",
        "description": "Check if an aldehyde is suitable for L-proline-catalyzed aldol reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "aldehyde_smiles": {
                    "type": "number",
                    "description": "Aldehyde Smiles"
                }
            },
            "required": [
                "aldehyde_smiles"
            ]
        }
    },
    {
        "name": "sharpless_epoxidation_prediction",
        "description": "Predict absolute configuration of epoxy alcohol via Sharpless rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "allylic_alcohol_smiles": {
                    "type": "number",
                    "description": "Allylic Alcohol Smiles"
                },
                "tartrate": {
                    "type": "number",
                    "description": "Tartrate",
                    "default": "L-(+)-DET"
                }
            },
            "required": [
                "allylic_alcohol_smiles"
            ]
        }
    }
]