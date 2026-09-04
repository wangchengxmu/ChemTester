# -*- coding: utf-8 -*-
"""
Coordination Chemistry & Crystal Field Theory Tools
Self-contained Python (stdlib only).
"""

import math
import re

# ── Spectrochemical series (index = field strength rank) ──
_SPECTRO_SERIES = {
    'I⁻': 0, 'Br⁻': 1, 'S²⁻': 2, 'SCN⁻': 3, 'Cl⁻': 4, 'NO₃⁻': 5,
    'N₃⁻': 6, 'F⁻': 7, 'OH⁻': 8, 'C₂O₄²⁻': 9, 'H₂O': 10, 'NCS⁻': 11,
    'CH₃CN': 12, 'NH₃': 13, 'en': 14, 'bipy': 15, 'phen': 16,
    'NO₂⁻': 17, 'PPh₃': 18, 'CN⁻': 19, 'CO': 20,
}

_LIGAND_ALIASES = {
    'I-': 'I⁻', 'Br-': 'Br⁻', 'S2-': 'S²⁻', 'S^2-': 'S²⁻',
    'SCN-': 'SCN⁻', 'Cl-': 'Cl⁻', 'NO3-': 'NO₃⁻', 'N3-': 'N₃⁻',
    'F-': 'F⁻', 'OH-': 'OH⁻', 'C2O4 2-': 'C₂O₄²⁻', 'C2O4^2-': 'C₂O₄²⁻',
    'NH3': 'NH₃', 'H2O': 'H₂O', 'CH3CN': 'CH₃CN', 'NCS-': 'NCS⁻',
    'NO2-': 'NO₂⁻', 'CN-': 'CN⁻', 'PPh3': 'PPh₃', 'CN': 'CN⁻',
}


def _resolve_ligand(lig):
    return _LIGAND_ALIASES.get(lig, lig)


def _count_unpaired_high_spin(n_electrons, n_orbitals):
    """High-spin: fill one per orbital first, then pair."""
    if n_electrons <= n_orbitals:
        return n_electrons
    return 2 * n_orbitals - n_electrons


def _count_unpaired_low_spin(n_electrons, n_orbitals):
    """Low-spin: pair in each orbital before moving to next set."""
    if n_electrons <= n_orbitals:
        return n_electrons  # one per orbital, no pairing needed yet
    return n_electrons % 2  # all paired except maybe 1


def crystal_field_splitting(geometry, d_count, strong_field=False):
    """Crystal field splitting: CFSE, config, unpaired e⁻, spin state.
    
    Returns dict with: cfse (in Δo/Δt units), config, unpaired, spin_state, units
    """
    d_count = max(0, min(d_count, 10))

    if geometry == 'octahedral':
        t2g_cap, eg_cap = 3, 2
        if strong_field:
            # Fill t2g completely (pairing), then eg
            t2g = min(d_count, 6)
            eg = d_count - t2g
            unpaired = _count_unpaired_low_spin(d_count, 5)
            spin = 'low' if d_count in (4, 5, 6, 7) else 'high'
        else:
            # High-spin: fill each orbital once, then pair
            t2g = min(d_count, t2g_cap)
            eg = d_count - t2g
            unpaired = _count_unpaired_high_spin(d_count, 5)
            spin = 'high'
        cfse = -0.4 * t2g + 0.6 * eg
        return {'cfse': cfse, 'config': f"t2g^{t2g} eg^{eg}",
                'unpaired': unpaired, 'spin_state': spin, 'units': 'Δo'}

    elif geometry == 'tetrahedral':
        # Tetrahedral always high-spin (Δt = 4/9 Δo, too small for pairing)
        e_count = min(d_count, 2)
        t2_count = d_count - e_count
        unpaired = _count_unpaired_high_spin(d_count, 5)
        cfse = -0.6 * e_count + 0.4 * t2_count
        return {'cfse': cfse, 'config': f"e^{e_count} t2^{t2_count}",
                'unpaired': unpaired, 'spin_state': 'high', 'units': 'Δt'}

    elif geometry in ('square_planar', 'square planar'):
        # Splitting: (dxz,dyz) < dxy < dz² < dx²-y²
        # Occupancy order: dxz,dyz → dxy → dz² → dx²-y²
        orbital_order = [2, 1, 1, 1]  # degeneracy: (dxz,dyz)=2, dxy=1, dz²=1, dx²-y²=1
        cfse = 0.0
        remaining = d_count
        for i, deg in enumerate(orbital_order):
            filled = min(remaining, 2 * deg)
            remaining -= filled
            # Energy: level 0 = 0, level 1 = 0.2, level 2 = 1.2, level 3 = 2.0 (approx in Δo)
            level_energy = [0.0, -0.2, 0.0, 1.0][i]
            cfse += level_energy * filled

        if d_count == 8:
            config = "(dxz,dyz)^4 (dxy)^2 (dz2)^2 (dx2-y2)^0"
            unpaired = 0
            spin = 'low'
        else:
            config = f"d^{d_count} (sqp)"
            unpaired = _count_unpaired_high_spin(d_count, 4)
            spin = 'low' if strong_field else 'high'
        return {'cfse': round(cfse, 2), 'config': config,
                'unpaired': unpaired, 'spin_state': spin, 'units': 'Δo'}

    return {'cfse': 0, 'config': f"d^{d_count}", 'unpaired': d_count,
            'spin_state': 'unknown', 'units': 'Δ'}


def cfse_energy(d_count, geometry, delta, pairing_energy, strong_field=False):
    """CFSE in kJ/mol with spin state determination.
    
    Args:
        delta: Δ in kJ/mol
        pairing_energy: P in kJ/mol
    """
    cfs = crystal_field_splitting(geometry, d_count, strong_field)
    cfse_kj = cfs['cfse'] * delta

    # Auto-determine spin if not forced
    actual_spin = cfs['spin_state']
    if geometry == 'octahedral' and d_count in (4, 5, 6, 7) and not strong_field:
        if delta > pairing_energy:
            actual_spin = 'low'
        elif delta < pairing_energy:
            actual_spin = 'high'
        else:
            actual_spin = 'borderline'
        # Recompute for auto-determined spin
        if actual_spin == 'low':
            cfs2 = crystal_field_splitting(geometry, d_count, strong_field=True)
            cfse_kj = cfs2['cfse'] * delta
            cfs = cfs2

    moment = spin_only_moment(cfs['unpaired'])
    return {
        'cfse_kj_mol': round(cfse_kj, 2),
        'cfse_delta_units': cfs['cfse'],
        'unpaired_electrons': cfs['unpaired'],
        'spin_state': actual_spin,
        'spin_only_moment': round(moment, 4),
        'config': cfs['config'],
    }


def spin_only_moment(unpaired_electrons):
    """μ = √(n(n+2)) Bohr magnetons."""
    return math.sqrt(unpaired_electrons * (unpaired_electrons + 2))


def spectrochemical_series(metal, oxidation, ligand_list):
    """Sort ligands by field strength (weak → strong)."""
    resolved = [_resolve_ligand(lig) for lig in ligand_list]
    resolved.sort(key=lambda name: _SPECTRO_SERIES.get(name, 99))
    return resolved


def oxidation_state_complex(complex_formula, charge):
    """Determine metal oxidation state from complex formula and overall charge.
    
    Examples: "[Co(NH3)6]" charge=3, "K3[Fe(CN)6]" charge=0
    """
    match = re.match(r'^(.*?)\[([^\]]+)\](.*?)$', complex_formula)
    if not match:
        return {'metal': None, 'oxidation_state': None, 'error': 'Invalid format'}

    prefix, inner, _ = match.groups()

    # Outer counter-ion charges
    outer_charge = 0
    ion_charges = {'K': 1, 'Na': 1, 'Li': 1, 'Rb': 1, 'Cs': 1,
                   'Ca': 2, 'Ba': 2, 'Mg': 2, 'Sr': 2, 'Zn': 2}
    for m in re.finditer(r'([A-Z][a-z]?)(\d*)', prefix):
        elem, count_str = m.groups()
        count = int(count_str) if count_str else 1
        outer_charge += ion_charges.get(elem, 0) * count

    complex_charge = charge - outer_charge

    # Extract metal
    metal_match = re.match(r'([A-Z][a-z]?)', inner)
    if not metal_match:
        return {'metal': None, 'oxidation_state': None, 'error': 'No metal found'}
    metal = metal_match.group(1)

    # Sum ligand charges
    ligand_charges = {
        'NH3': 0, 'H2O': 0, 'CO': 0, 'en': 0, 'bipy': 0, 'phen': 0, 'PPh3': 0,
        'NO2-': -1, 'NO2⁻': -1, 'CN-': -1, 'CN⁻': -1,
        'Cl-': -1, 'Cl⁻': -1, 'Br-': -1, 'Br⁻': -1, 'I-': -1, 'I⁻': -1,
        'F-': -1, 'F⁻': -1, 'OH-': -1, 'OH⁻': -1, 'SCN-': -1, 'SCN⁻': -1,
        'NCS-': -1, 'NCS⁻': -1, 'NO3-': -1, 'NO₃⁻': -1, 'N3-': -1, 'N₃⁻': -1,
        'C2O4 2-': -2, 'C2O4²⁻': -2, 'C2O4^2-': -2, 'S2-': -2, 'S²⁻': -2,
    }

    ligand_charge_sum = 0
    for m in re.finditer(r'\(([^\)]+)\)(\d*)', inner[metal_match.end():]):
        lig_name, count_str = m.groups()
        count = int(count_str) if count_str else 1
        charge_val = ligand_charges.get(lig_name, ligand_charges.get(_resolve_ligand(lig_name), 0))
        ligand_charge_sum += charge_val * count

    oxidation = complex_charge - ligand_charge_sum
    return {'metal': metal, 'oxidation_state': oxidation,
            'ligand_charge_sum': ligand_charge_sum, 'complex_charge': complex_charge}


def coordination_number(geometry):
    """Return coordination number from geometry name."""
    return {'octahedral': 6, 'tetrahedral': 4, 'square planar': 4,
            'linear': 2, 'trigonal bipyramidal': 5, 'trigonal planar': 3,
            'trigonal prismatic': 6}.get(geometry, 0)


def geometry_from_coordination(cn, metal, ligands=None):
    """Predict geometry from coordination number."""
    mapping = {2: 'linear', 3: 'trigonal planar', 4: 'tetrahedral',
               5: 'trigonal bipyramidal', 6: 'octahedral',
               7: 'pentagonal bipyramidal', 8: 'square antiprismatic'}
    geom = mapping.get(cn, 'unknown')
    # d8 CN=4 → square planar with strong-field ligands
    if cn == 4 and ligands:
        if any(_resolve_ligand(l) in ('CN⁻', 'CO', 'NO₂⁻', 'PPh₃', 'en', 'phen') for l in ligands):
            geom = 'square planar'
    return geom


def isomer_count(metal, ligands, geometry):
    """Count geometric and optical isomers.
    
    ligands: list of (name, count) tuples
    """
    counts = [c for _, c in ligands]
    n_types = len(ligands)

    if geometry == 'octahedral':
        if counts == [2, 2]:
            return {'geometric': 2, 'optical': 0, 'total': 2, 'types': ['cis', 'trans']}
        if counts == [3, 3]:
            return {'geometric': 2, 'optical': 0, 'total': 2, 'types': ['facial', 'meridional']}
        if n_types == 6 and all(c == 1 for c in counts):
            return {'geometric': 30, 'optical': 15, 'total': 30, 'types': ['30 total (15 enantiomer pairs)']}
        if n_types == 3 and sorted(counts) == [2, 2, 2]:
            return {'geometric': 5, 'optical': 1, 'total': 6, 'types': ['5 geometric + 1 optical pair']}
        if sorted(counts) == [1, 1, 4]:
            return {'geometric': 2, 'optical': 0, 'total': 2, 'types': ['cis', 'trans']}
        if sorted(counts) == [1, 5]:
            return {'geometric': 1, 'optical': 0, 'total': 1, 'types': ['single isomer']}
        return {'geometric': 'multiple', 'optical': 'unknown', 'total': 'multiple', 'types': []}

    elif geometry == 'tetrahedral':
        if n_types == 2 and sorted(counts) == [2, 2]:
            return {'geometric': 1, 'optical': 1, 'total': 2, 'types': ['1 pair enantiomers']}
        if n_types == 4 and all(c == 1 for c in counts):
            return {'geometric': 1, 'optical': 1, 'total': 2, 'types': ['1 pair enantiomers']}
        return {'geometric': 1, 'optical': 0, 'total': 1, 'types': ['single isomer']}

    elif geometry == 'square planar':
        if n_types == 2 and sorted(counts) == [2, 2]:
            return {'geometric': 2, 'optical': 0, 'total': 2, 'types': ['cis', 'trans']}
        if n_types == 4 and all(c == 1 for c in counts):
            return {'geometric': 3, 'optical': 0, 'total': 3, 'types': ['3 positional isomers']}
        return {'geometric': 'multiple', 'optical': 0, 'total': 'multiple', 'types': []}

    return {'geometric': 'unknown', 'optical': 'unknown', 'total': 'unknown', 'types': []}


def color_from_absorption(wavelength_nm):
    """Determine complementary color from absorbed wavelength (nm).
    
    Uses wavelength-to-color lookup for both the absorbed color and its
    approximate complementary color. The complement is estimated from a
    lookup table based on the visible spectrum.
    """
    # Absorbed color
    if wavelength_nm < 380:
        region = 'UV'
    elif wavelength_nm < 450:
        region = 'violet'
    elif wavelength_nm < 495:
        region = 'blue'
    elif wavelength_nm < 570:
        region = 'green'
    elif wavelength_nm < 590:
        region = 'yellow'
    elif wavelength_nm < 620:
        region = 'orange'
    elif wavelength_nm < 750:
        region = 'red'
    else:
        region = 'IR'

    # Complementary color lookup (absorbed → observed complementary)
    # Based on color-wheel complements of the visible spectrum
    complement_map = [
        (380, 'yellow'),       # violet absorbed → yellow observed
        (440, 'yellow-orange'), # violet-blue → yellow-orange
        (450, 'orange'),        # blue → orange
        (495, 'red-magenta'),   # cyan-blue → red-magenta
        (530, 'magenta'),       # green → magenta/purple
        (570, 'purple'),        # green → purple (boundary)
        (595, 'blue'),          # yellow → blue
        (625, 'blue-cyan'),     # orange → blue-cyan
        (680, 'cyan-green'),    # red → cyan-green
        (750, 'green'),         # deep red → green
        (900, 'blue-green'),    # near-IR → blue-green
    ]
    observed = next(c for cutoff, c in complement_map if wavelength_nm < cutoff)

    return {'absorbed_nm': wavelength_nm, 'absorbed_color': region,
            'observed_color': observed, 'complement': observed}


def jahn_teller_analysis(d_count, geometry='octahedral', spin_state='high'):
    """Predict Jahn-Teller distortion for d-electron configurations.
    
    In octahedral complexes, Jahn-Teller is significant when the 
    eg orbitals are unevenly occupied:
    - Strong JT: d⁴ (high-spin), d⁹
    - Weak JT: d⁷ (low-spin)
    - Tetrahedral: d², d⁴, d⁵, d⁷ can show JT (opposite orbital pattern)
    - No JT: all other configurations (fully filled, half-filled, symmetric)
    
    Returns: dict with prediction, strength, and explanation
    """
    d_count = max(0, min(d_count, 10))

    if geometry == 'octahedral':
        if spin_state == 'high':
            # High-spin: t2g filled first (1 per orbital), then eg
            t2g = min(d_count, 3)
            eg = d_count - t2g
            if eg > 2:
                eg = 2
                t2g = d_count - 2
        else:
            # Low-spin: t2g pairs first (up to 6), then eg
            t2g = min(d_count, 6)
            eg = d_count - t2g
            if eg > 2:
                eg = 2
                t2g = d_count - 2

        if d_count == 10:
            return {
                'prediction': 'No Jahn-Teller distortion',
                'strength': 'none',
                'config': f't2g^{t2g} eg^{eg}',
                'explanation': 'All d orbitals fully filled (eg⁴), no degeneracy to lift.',
            }
        if d_count in (4, 9):
            strength = 'strong'
            if d_count == 4:
                detail = 'eg² (one electron per eg orbital) → elongation lowers degeneracy'
            else:
                detail = 'eg³ (hole in eg) → elongation stabilizes the filled orbital'
            return {
                'prediction': 'Strong Jahn-Teller distortion',
                'strength': strength,
                'config': f't2g^{t2g} eg^{eg}',
                'explanation': detail,
            }
        if d_count == 7 and spin_state == 'low':
            return {
                'prediction': 'Weak Jahn-Teller distortion',
                'strength': 'weak',
                'config': f't2g^{t2g} eg^{eg}',
                'explanation': 'Low-spin d⁷ has eg¹ — single electron in degenerate eg orbitals causes weak distortion.',
            }
        if d_count == 7 and spin_state == 'high':
            return {
                'prediction': 'No Jahn-Teller distortion',
                'strength': 'none',
                'config': f't2g^{t2g} eg^{eg}',
                'explanation': 'High-spin d⁷ has t2g⁵ eg² — both eg orbitals singly occupied (symmetric).',
            }
        # All other octahedral cases
        return {
            'prediction': 'No Jahn-Teller distortion',
            'strength': 'none',
            'config': f't2g^{t2g} eg^{eg}',
            'explanation': f'{"t2g" if t2g > 0 else "t2g"}^{t2g} eg^{eg} — no uneven occupation in degenerate orbitals.',
        }

    elif geometry == 'tetrahedral':
        # In tetrahedral, the e set (upper) has JT analogs to t2g in octahedral
        # e orbitals (doubly degenerate) filled first in tetrahedral
        if spin_state == 'high':
            e_occ = min(d_count, 2)
            t2_occ = d_count - e_occ
        else:
            e_occ = min(d_count, 2)
            t2_occ = d_count - e_occ

        if d_count in (2, 4, 5, 7):
            strength = 'weak' if d_count in (4, 5, 7) else 'weak'
            return {
                'prediction': 'Weak Jahn-Teller distortion (tetrahedral)',
                'strength': strength,
                'config': f'e^{e_occ} t2^{t2_occ}',
                'explanation': f'Tetrahedral d{d_count}: e orbitals unevenly occupied. '
                               'Tetrahedral JT distortions are generally weaker than octahedral.',
            }
        if d_count == 10:
            return {
                'prediction': 'No Jahn-Teller distortion',
                'strength': 'none',
                'config': f'e^{e_occ} t2^{t2_occ}',
                'explanation': 'All orbitals fully filled.',
            }
        return {
            'prediction': 'No Jahn-Teller distortion',
            'strength': 'none',
            'config': f'e^{e_occ} t2^{t2_occ}',
            'explanation': 'No uneven occupation in degenerate orbitals.',
        }

    return {
        'prediction': 'Jahn-Teller analysis not standard for this geometry',
        'strength': 'unknown',
        'config': f'd^{d_count}',
        'explanation': f'Geometry "{geometry}" not in standard JT analysis.',
    }


def tanabe_sugano_diagram(d_count, transition_type='spin_allowed'):
    """Describe expected transitions for a d^n configuration."""
    info = {
        1: '²D → ²T₂: one spin-allowed transition. Single absorption band.',
        2: '³F → ³T₁, ³T₂: two spin-allowed transitions.',
        3: '⁴F → ⁴T₁, ⁴T₂: two spin-allowed transitions.',
        4: 'High-spin: ⁵D → ⁵E, ⁵T₂. Low-spin: multiple bands.',
        5: 'High-spin (e.g. [Fe(H₂O)₆]³⁺): ALL transitions spin-forbidden — very pale/colorless. Low-spin: similar to d⁶.',
        6: 'Low-spin (e.g. [Co(NH₃)₆]³⁺): ¹I → ¹T₁, ¹T₂ spin-allowed — colored. High-spin: spin-forbidden, pale.',
        7: 'High-spin: ⁴F → ⁴T₁, ⁴T₂. Multiple bands.',
        8: '³F → ³T₁(P), ³T₂: two to three spin-allowed transitions.',
        9: '²D → ²E, ²T₂: broad absorption, typically intense color.',
    }
    desc = info.get(d_count, f'No standard description for d{d_count}.')
    if transition_type == 'spin_forbidden':
        desc += ' Spin-forbidden transitions are weak (ε ≪ 1 M⁻¹cm⁻¹).'
    return desc


# ── Tests ──
if __name__ == "__main__":
    print("=" * 60)
    print("Coordination Chemistry Tools — Test Suite")
    print("=" * 60)

    # 1. [Co(NH₃)₆]³⁺ d⁶ low-spin
    print("\n--- [Co(NH₃)₆]³⁺ (d⁶, low spin, orange) ---")
    r = crystal_field_splitting('octahedral', 6, strong_field=True)
    assert r['config'] == 't2g^6 eg^0' and r['unpaired'] == 0 and abs(r['cfse'] - (-2.4)) < 1e-9
    print(f"  ✓ CFSE={r['cfse']}Δo, {r['config']}, μ={spin_only_moment(r['unpaired']):.2f} BM")
    r = cfse_energy(6, 'octahedral', delta=230, pairing_energy=210, strong_field=True)
    assert r['cfse_kj_mol'] == -552.0
    print(f"  ✓ CFSE={r['cfse_kj_mol']} kJ/mol, spin={r['spin_state']}")

    # 2. [Fe(H₂O)₆]³⁺ d⁵ high-spin
    print("\n--- [Fe(H₂O)₆]³⁺ (d⁵, high spin, pale) ---")
    r = crystal_field_splitting('octahedral', 5, strong_field=False)
    assert r['config'] == 't2g^3 eg^2' and r['unpaired'] == 5 and abs(r['cfse']) < 1e-9
    print(f"  ✓ CFSE={r['cfse']}Δo, {r['config']}, μ={spin_only_moment(r['unpaired']):.2f} BM")
    r = cfse_energy(5, 'octahedral', delta=164, pairing_energy=300)
    assert r['spin_state'] == 'high'
    print(f"  ✓ Δ={164} < P={300} → high spin, μ={r['spin_only_moment']} BM")

    # 3. [Ni(CN)₄]²⁻ d⁸ square planar
    print("\n--- [Ni(CN)₄]²⁻ (d⁸, square planar, diamagnetic) ---")
    r = crystal_field_splitting('square planar', 8)
    assert r['unpaired'] == 0
    print(f"  ✓ {r['config']}, unpaired={r['unpaired']}, μ={spin_only_moment(r['unpaired']):.2f} BM")

    # 4. Spin-only moments
    print("\n--- Spin-only moments ---")
    for n in range(6):
        print(f"  {n}e⁻: μ = {spin_only_moment(n):.4f} BM")

    # 5. Spectrochemical series
    print("\n--- Spectrochemical series ---")
    sorted_ligs = spectrochemical_series('Fe', 3, ['NH3', 'Cl-', 'CN-', 'H2O', 'en', 'I-'])
    expected_order = ['I⁻', 'Cl⁻', 'H₂O', 'NH₃', 'en', 'CN⁻']
    assert sorted_ligs == expected_order
    print(f"  ✓ {' < '.join(sorted_ligs)}")

    # 6. Oxidation states
    print("\n--- Oxidation states ---")
    r = oxidation_state_complex("[Co(NH3)6]", 3)
    assert r['oxidation_state'] == 3
    print(f"  ✓ [Co(NH₃)₆]³⁺ → Co{r['oxidation_state']:+d}")
    r = oxidation_state_complex("[Fe(CN)6]", -4)
    assert r['oxidation_state'] == 2
    print(f"  ✓ [Fe(CN)₆]⁴⁻ → Fe{r['oxidation_state']:+d}")
    r = oxidation_state_complex("K3[Fe(CN)6]", 0)
    assert r['oxidation_state'] == 3
    print(f"  ✓ K₃[Fe(CN)₆] → Fe{r['oxidation_state']:+d}")

    # 7. Geometry
    print("\n--- Geometry ---")
    assert coordination_number('octahedral') == 6
    assert coordination_number('tetrahedral') == 4
    assert geometry_from_coordination(6, 'Co') == 'octahedral'
    print(f"  ✓ CN=6 → {geometry_from_coordination(6, 'Co')}")

    # 8. Isomer counting
    print("\n--- Isomer counting ---")
    r = isomer_count('M', [('a',2),('b',2)], 'octahedral')
    assert r['total'] == 2
    print(f"  ✓ [Ma₂b₂] oct: {r['types']}")
    r = isomer_count('M', [('a',3),('b',3)], 'octahedral')
    assert r['total'] == 2
    print(f"  ✓ [Ma₃b₃] oct: {r['types']}")
    r = isomer_count('M', [('a',2),('b',2)], 'tetrahedral')
    print(f"  ✓ [Ma₂b₂] tet: {r['types']}")
    r = isomer_count('M', [('a',1),('b',1),('c',1),('d',1),('e',1),('f',1)], 'octahedral')
    assert r['total'] == 30
    print(f"  ✓ [Mabcdef] oct: {r['total']} total")

    # 9. Color
    print("\n--- Color from absorption ---")
    c = color_from_absorption(530)
    assert c['absorbed_color'] == 'green'
    assert c['observed_color'] in ('magenta', 'purple'), f"Expected magenta/purple, got {c['observed_color']}"
    print(f"  ✓ Absorb 530nm (green) → {c['observed_color']}")
    # Additional color checks
    c = color_from_absorption(460)
    assert c['absorbed_color'] == 'blue'
    print(f"  ✓ Absorb 460nm (blue) → {c['observed_color']}")
    c = color_from_absorption(580)
    assert c['absorbed_color'] == 'yellow'
    assert 'blue' in c['observed_color']
    print(f"  ✓ Absorb 580nm (yellow) → {c['observed_color']}")

    # 10. Tanabe-Sugano
    print("\n--- Tanabe-Sugano ---")
    for d in [1, 5, 6]:
        print(f"  d{d}: {tanabe_sugano_diagram(d)}")

    # 11. Edge cases
    print("\n--- Edge cases ---")
    r = crystal_field_splitting('tetrahedral', 5)
    print(f"  ✓ d⁵ tetrahedral (always high-spin): {r['config']}, unpaired={r['unpaired']}")
    assert r['spin_state'] == 'high'

    # 12. Jahn-Teller analysis
    print("\n--- Jahn-Teller analysis ---")
    jt = jahn_teller_analysis(4, 'octahedral', 'high')
    assert jt['strength'] == 'strong'
    print(f"  ✓ d⁴ high-spin oct: {jt['strength']} — {jt['prediction']}")

    jt = jahn_teller_analysis(9, 'octahedral', 'high')
    assert jt['strength'] == 'strong'
    print(f"  ✓ d⁹ oct: {jt['strength']} — {jt['prediction']}")

    jt = jahn_teller_analysis(7, 'octahedral', 'low')
    assert jt['strength'] == 'weak'
    print(f"  ✓ d⁷ low-spin oct: {jt['strength']} — {jt['prediction']}")

    jt = jahn_teller_analysis(10, 'octahedral')
    assert jt['strength'] == 'none'
    print(f"  ✓ d¹⁰ oct: {jt['strength']} — {jt['prediction']}")

    jt = jahn_teller_analysis(5, 'octahedral', 'high')
    assert jt['strength'] == 'none'
    print(f"  ✓ d⁵ high-spin oct: {jt['strength']} — {jt['prediction']}")

    jt = jahn_teller_analysis(2, 'tetrahedral')
    assert jt['strength'] == 'weak'
    print(f"  ✓ d² tetrahedral: {jt['strength']} — {jt['prediction']}")

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
