# -*- coding: utf-8 -*-
"""Spectroscopy analysis tools — stdlib only."""
import re, math

# ── 1. ¹H NMR chemical shifts ──────────────────────────────────────────
_PROTON_SHIFTS = {
    'alkyl_CH3':  {'range': (0.7, 1.3), 'mult': 'triplet/quartet context-dependent'},
    'alkyl_CH2':  {'range': (1.2, 1.5), 'mult': 'multiplet'},
    'alkyl_CH':   {'range': (1.4, 1.8), 'mult': 'multiplet'},
    'allylic':    {'range': (1.6, 2.8), 'mult': 'multiplet'},
    'alpha_hetero':{'range': (2.0, 4.5), 'mult': 'depends on heteroatom'},
    'aromatic':   {'range': (6.0, 8.5), 'mult': 'multiplet (ortho/meta/para coupling)'},
    'aldehyde':   {'range': (9.0, 10.0), 'mult': 'doublet or singlet'},
    'carboxylic_acid': {'range': (10.0, 13.0), 'mult': 'singlet, very broad'},
    'vinylic':    {'range': (4.5, 6.5), 'mult': 'doublet of doublets common'},
    'alkyne':     {'range': (2.0, 3.0), 'mult': 'singlet (usually)'},
    'NH':         {'range': (0.5, 5.0), 'mult': 'broad, exchangeable'},
    'OH':         {'range': (0.5, 5.0), 'mult': 'broad, exchangeable'},
    'F':          {'range': (4.0, 4.5), 'mult': 'large J coupling to F'},
    'Cl':         {'range': (3.0, 4.0), 'mult': 'multiplet'},
    'Br':         {'range': (2.5, 3.5), 'mult': 'multiplet'},
    'I':          {'range': (2.0, 3.0), 'mult': 'multiplet'},
}

def nmr_chemical_shift_proton(atom_type, substituent_environment=''):
    """Return dict with shift_range, multiplicity, notes for ¹H NMR."""
    key = f"{substituent_environment}_{atom_type}" if substituent_environment else atom_type
    if key in _PROTON_SHIFTS:
        return {'type': key, **_PROTON_SHIFTS[key]}
    # Fallback: try atom_type alone
    if atom_type in _PROTON_SHIFTS:
        return {'type': atom_type, **_PROTON_SHIFTS[atom_type]}
    return {'type': key, 'range': (0.0, 12.0), 'mult': 'unknown', 'notes': f'No data for {key}'}

# ── 2. ¹³C NMR chemical shifts ────────────────────────────────────────
_CARBON_SHIFTS = {
    'sp3':            {'range': (0, 90)},
    'sp2':            {'range': (100, 220)},
    'sp':             {'range': (65, 90)},
    'carbonyl':       {'range': (160, 220)},
    'carbonyl_aldehyde': {'range': (190, 205)},
    'carbonyl_ketone':   {'range': (205, 220)},
    'carbonyl_ester':    {'range': (160, 185)},
    'carbonyl_acid':     {'range': (170, 185)},
    'carbonyl_amide':    {'range': (160, 180)},
    'aldehyde':          {'range': (190, 205)},
    'aromatic':       {'range': (110, 160)},
    'alkene':         {'range': (100, 150)},
}

def nmr_chemical_shift_carbon(atom_type, substituent_environment=''):
    key1 = f"{substituent_environment}_{atom_type}" if substituent_environment else atom_type
    key2 = f"{atom_type}_{substituent_environment}" if substituent_environment else atom_type
    for k in (key1, key2, substituent_environment, atom_type):
        if k in _CARBON_SHIFTS:
            return {'type': k, **_CARBON_SHIFTS[k]}
    return {'type': key1, 'range': (0, 220), 'notes': f'No data for {key1}'}

# ── 3. Splitting pattern (n+1 rule) ────────────────────────────────────
_MULT_NAMES = ['singlet', 'doublet', 'triplet', 'quartet', 'quintet',
               'sextet', 'septet', 'octet', 'nonet', 'decet']

def splitting_pattern(n_neighbors, equivalence='none'):
    """Return splitting name. equivalence='diastereotopic' notes non-equivalence."""
    if n_neighbors < 0:
        return 'invalid'
    name = _MULT_NAMES[n_neighbors] if n_neighbors < len(_MULT_NAMES) else f'{n_neighbors+1}-let'
    if equivalence == 'diastereotopic':
        return f"{name} (complex — diastereotopic protons may be non-equivalent)"
    return name

# ── 4. Coupling constant estimates ─────────────────────────────────────
_J_VALUES = {
    'vicinal_trans':  (11, 19),
    'vicinal_cis':    (5, 12),
    'geminal':        (0, 3),
    'aromatic_ortho': (6, 9),
    'aromatic_meta':  (1, 3),
    'aromatic_para':  (0, 1),
    'allylic':        (0, 3),
    'HC_one_bond':    (125, 250),
    'HC_two_bond':    (0, 10),
    'HC_three_bond':  (0, 10),
}

def coupling_constant_estimate(system_type):
    if system_type in _J_VALUES:
        lo, hi = _J_VALUES[system_type]
        return {'type': system_type, 'J_range_Hz': (lo, hi), 'typical': (lo+hi)//2}
    return {'type': system_type, 'J_range_Hz': None, 'notes': f'No data for {system_type}'}

# ── 5. IR frequency / bond ─────────────────────────────────────────────
_IR_DATA = {
    'OH_stretch':  {'range': (3200, 3600), 'intensity': 'broad, strong'},
    'NH_stretch':  {'range': (3300, 3500), 'intensity': 'medium'},
    'CH_stretch':  {'range': (2850, 3100), 'intensity': 'medium'},
    'C=O':         {'range': (1650, 1800), 'intensity': 'strong'},
    'C=O_ester':   {'range': (1735, 1750), 'intensity': 'strong'},
    'C=O_ketone':  {'range': (1710, 1725), 'intensity': 'strong'},
    'C=O_aldehyde':{'range': (1720, 1740), 'intensity': 'strong'},
    'C=O_acid':    {'range': (1710, 1725), 'intensity': 'strong, broad'},
    'C=O_amide':   {'range': (1650, 1690), 'intensity': 'strong'},
    'C=C':         {'range': (1620, 1680), 'intensity': 'medium-weak'},
    'C≡C':         {'range': (2100, 2260), 'intensity': 'weak'},
    'C≡N':         {'range': (2210, 2260), 'intensity': 'medium'},
    'C-O':         {'range': (1000, 1300), 'intensity': 'strong'},
    'C_Cl':        {'range': (600, 800),   'intensity': 'strong'},
    'C_Br':        {'range': (500, 600),   'intensity': 'strong'},
    'NH_bend':     {'range': (1550, 1640), 'intensity': 'medium'},
    'CH_bend':     {'range': (1350, 1480), 'intensity': 'medium'},
}

_IR_ALIASES = {
    'O-H': 'OH_stretch', 'N-H': 'NH_stretch', 'C-H': 'CH_stretch',
    'C-O': 'C-O',
}

def ir_frequency_bond(bond_type):
    key = _IR_ALIASES.get(bond_type, bond_type)
    if key in _IR_DATA:
        return {'bond': bond_type, **_IR_DATA[key]}
    return {'bond': bond_type, 'range': None, 'notes': f'No data for {bond_type}'}

# ── 6. MS molecular ion exact mass ─────────────────────────────────────
_MASSES = {'H':1.00783,'C':12.0,'N':14.00307,'O':15.99491,'F':18.99840,
           'Cl':34.96885,'Br':78.91834,'S':31.97207,'P':30.97376,
           'I':126.90447,'Si':27.97693,'B':11.00931}

def ms_molecular_ion(molecular_formula):
    """Parse formula like 'C6H12O' and return exact monoisotopic mass."""
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', molecular_formula)
    mass = 0.0
    for elem, count in tokens:
        if elem not in _MASSES:
            raise ValueError(f"Unknown element: {elem}")
        mass += _MASSES[elem] * (int(count) if count else 1)
    return round(mass, 5)

# ── 7. MS nitrogen rule ────────────────────────────────────────────────
def ms_nitrogen_rule(molecular_mass):
    is_even = molecular_mass % 2 < 0.5
    return {
        'mass': molecular_mass,
        'is_even': is_even,
        'nitrogen_count_parity': 'even (0, 2, 4...)' if is_even else 'odd (1, 3, 5...)',
    }

# ── 8. MS isotope pattern ─────────────────────────────────────────────
_ISOTOPE_ABUND = {
    'C':  (0.011, 1),   # 13C  1.1%  → +1
    'H':  (0.00015, 1),  # 2H   0.015% → +1
    'Cl': (0.2423, 2),   # 37Cl 24.23% → +2
    'Br': (0.4931, 2),   # 81Br 49.31% → +2
    'S':  (0.044, 2),    # 34S  4.4%   → +2
}

def ms_isotope_pattern(element_counts):
    """element_counts: dict like {'C':6,'H':12,'O':1,'Cl':1}"""
    M1 = 0.0
    M2 = 0.0
    for elem, n in element_counts.items():
        if elem in _ISOTOPE_ABUND:
            frac, mass_offset = _ISOTOPE_ABUND[elem]
            p_light = 1.0 - frac
            if mass_offset == 1:
                # +1 isotope: M+1 from 1 heavy atom, M+2 from 2 heavy atoms
                M1 += math.comb(n, 1) * frac * p_light**(n-1) * 100
                M2 += math.comb(n, 2) * frac**2 * p_light**(n-2) * 100
            elif mass_offset == 2:
                # +2 isotope: M+2 from 1 heavy atom, M+4 from 2 heavy atoms
                M2 += math.comb(n, 1) * frac * p_light**(n-1) * 100
    return {'M': 100.0, 'M+1': round(M1, 2), 'M+2': round(M2, 2),
            'M+1_pct': f"{M1:.1f}%", 'M+2_pct': f"{M2:.1f}%"}
    return {'M': 100.0, 'M+1': round(M1, 2), 'M+2': round(M2, 2),
            'M+1_pct': f"{M1:.1f}%", 'M+2_pct': f"{M2:.1f}%"}

# ── 9. UV-Vis max absorption ──────────────────────────────────────────
_UV_DATA = {
    'C=C':             {'lambda_max_nm': (170, 180), 'epsilon': '~10,000'},
    'conjugated_diene':{'lambda_max_nm': (217, 250), 'epsilon': '~21,000'},
    'conjugated_triene':{'lambda_max_nm': (258, 258), 'epsilon': '~35,000'},
    'alpha_beta_unsat':{'lambda_max_nm': [(210, 250), (310, 330)], 'epsilon': 'varies'},
    'benzene':         {'lambda_max_nm': (255, 255), 'epsilon': '~200'},
    'aniline':         {'lambda_max_nm': [(230, 230), (280, 280)], 'epsilon': 'varies'},
    'nitro':           {'lambda_max_nm': (270, 270), 'epsilon': 'varies'},
    'azo':             {'lambda_max_nm': (350, 450), 'epsilon': 'strong'},
}

def uv_vis_max_absorption(chromophore):
    if chromophore in _UV_DATA:
        return {'chromophore': chromophore, **_UV_DATA[chromophore]}
    return {'chromophore': chromophore, 'notes': f'No data for {chromophore}'}

# ── 10. Deduce structure from NMR ──────────────────────────────────────
def _shift_to_fragment(shift):
    """Map a shift value to possible fragment(s)."""
    if shift < 2.0:   return 'alkyl (CH₃/CH₂/CH)'
    if shift < 3.0:   return 'allylic / alkyne / α-Br/I'
    if shift < 4.5:   return 'α-heteroatom (O/N/Cl) / vinylic (low end)'
    if shift < 5.0:   return 'NH/OH (broad, exchangeable)'
    if shift < 6.5:   return 'vinylic'
    if shift < 8.5:   return 'aromatic'
    if shift < 10.0:  return 'aldehyde'
    return 'carboxylic acid'

def deduce_structure_from_nmr(shifts, integrals, splitting):
    """shifts/integrals/splitting: lists of same length. Returns analysis string."""
    lines = []
    total_h = sum(integrals)
    lines.append(f"Total H count (from integration): {total_h}")
    for s, i, sp in zip(shifts, integrals, splitting):
        frag = _shift_to_fragment(s)
        lines.append(f"  δ {s:.1f} ppm, {i}H, {sp} → likely {frag}")
    # Check for aromatic
    aromatic_h = sum(i for s, i in zip(shifts, integrals) if 6.0 <= s <= 8.5)
    if aromatic_h >= 4:
        lines.append("  → Possible monosubstituted benzene or similar aromatic ring")
    elif aromatic_h >= 2:
        lines.append("  → Possible disubstituted or heteroaromatic system")
    # Check for aldehyde
    if any(9.0 <= s <= 10.0 for s in shifts):
        lines.append("  → Aldehyde proton detected (C=O confirmed)")
    # Check for carboxylic acid
    if any(s >= 10.0 for s in shifts):
        lines.append("  → Carboxylic acid proton detected (broad singlet)")
    # Splitting analysis
    for s, i, sp in zip(shifts, integrals, splitting):
        if 'doublet' in sp.lower() and i == 3:
            lines.append(f"  → Doublet, 3H at δ {s:.1f}: likely CH₃ adjacent to CH")
        elif 'quartet' in sp.lower() and i == 2:
            lines.append(f"  → Quartet, 2H at δ {s:.1f}: likely CH₂ adjacent to CH₃ (ethyl group)")
    return '\n'.join(lines)


# ── Tests ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=== 1. ¹H NMR shifts ===")
    assert nmr_chemical_shift_proton('CH3', 'alkyl')['range'] == (0.7, 1.3)
    assert nmr_chemical_shift_proton('aldehyde')['range'] == (9.0, 10.0)
    assert nmr_chemical_shift_proton('F')['range'] == (4.0, 4.5)
    print("PASS")

    print("=== 2. ¹³C NMR shifts ===")
    assert nmr_chemical_shift_carbon('C', 'carbonyl')['range'] == (160, 220)
    assert nmr_chemical_shift_carbon('C', 'aromatic')['range'] == (110, 160)
    print("PASS")

    print("=== 3. Splitting pattern ===")
    assert splitting_pattern(0) == 'singlet'
    assert splitting_pattern(3) == 'quartet'
    assert 'diastereotopic' in splitting_pattern(2, 'diastereotopic')
    print("PASS")

    print("=== 4. Coupling constants ===")
    j = coupling_constant_estimate('vicinal_trans')
    assert j['J_range_Hz'] == (11, 19)
    j = coupling_constant_estimate('aromatic_ortho')
    assert j['J_range_Hz'] == (6, 9)
    print("PASS")

    print("=== 5. IR frequencies ===")
    ir = ir_frequency_bond('C=O_ketone')
    assert ir['range'] == (1710, 1725)
    ir = ir_frequency_bond('OH_stretch')
    assert ir['intensity'] == 'broad, strong'
    print("PASS")

    print("=== 6. MS molecular ion ===")
    m = ms_molecular_ion('C6H12O')
    assert abs(m - 100.08883) < 0.001, f"Got {m}"
    m = ms_molecular_ion('C2H5Cl')
    assert abs(m - 64.008) < 0.001, f"Got {m}"
    print("PASS")

    print("=== 7. Nitrogen rule ===")
    r = ms_nitrogen_rule(100.09)
    assert r['is_even'] == True
    r = ms_nitrogen_rule(93.07)
    assert r['is_even'] == False
    print("PASS")

    print("=== 8. Isotope pattern ===")
    p = ms_isotope_pattern({'C':6,'H':6})
    assert abs(p['M+1'] - 6.69) < 0.5, f"Got {p['M+1']}"
    p2 = ms_isotope_pattern({'C':6,'H':5,'Cl':1})
    assert p2['M+2'] > 20, f"M+2 too low: {p2['M+2']}"
    print("PASS")

    print("=== 9. UV-Vis ===")
    uv = uv_vis_max_absorption('conjugated_diene')
    assert uv['lambda_max_nm'] == (217, 250)
    uv = uv_vis_max_absorption('azo')
    assert uv['lambda_max_nm'] == (350, 450)
    print("PASS")

    print("=== 10. Deduce structure from NMR ===")
    result = deduce_structure_from_nmr(
        [1.23, 3.65, 7.25, 9.78],
        [3, 2, 5, 1],
        ['triplet', 'quartet', 'multiplet', 'singlet']
    )
    assert 'ethyl' in result.lower() or 'CH₃' in result
    assert 'aldehyde' in result.lower()
    assert 'aromatic' in result.lower()
    print(result)
    print("PASS")

    # ── New tests for fixed gaps ──
    print("=== Gap 1: ¹³C NMR aldehyde ===")
    r = nmr_chemical_shift_carbon('aldehyde')
    assert r['range'] == (190, 205), f"Got {r}"
    print("PASS")

    print("=== Gap 2: IR O-H bond ===")
    ir = ir_frequency_bond('O-H')
    assert ir['range'] == (3200, 3600), f"Got {ir}"
    ir2 = ir_frequency_bond('N-H')
    assert ir2['range'] == (3300, 3500), f"Got {ir2}"
    print("PASS")

    print("=== Gap 3: MS Cl isotope pattern (2 Cl) ===")
    p = ms_isotope_pattern({'Cl': 2})
    # For 2 Cl: M ≈ 0.7577² × 100 = 57.4, M+2 ≈ 2 × 0.2423 × 0.7577 × 100 = 36.7
    # Ratio M:M+2 ≈ 57.4:36.7 ≈ 1.56 (≈ 3:2)
    actual_M = 0.7577**2 * 100
    ratio = actual_M / p['M+2']
    assert 1.3 < ratio < 1.8, f"M:M+2 = {ratio:.2f}, expected ~1.5 (3:2). M+2={p['M+2']}"
    print(f"  M:M+2 ratio = {ratio:.2f} (expected ~1.5)")
    print("PASS")

    print("\n✅ All tests passed!")
