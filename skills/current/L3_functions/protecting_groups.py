"""
Protecting Groups Tools
=======================

Python implementations for protecting group selection and
orthogonal protection planning.

Source: L2 protecting_groups.md

## Solver Instructions (for AI Agent)

When you encounter organic synthesis problems involving protecting groups, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Select protecting group**: Given functional group (alcohol, amine, carbonyl, carboxylic acid) and conditions -> choose appropriate PG
- **Orthogonal strategy**: Given multiple functional groups -> plan orthogonal deprotection sequence
- **Check stability**: Given protecting group and reaction conditions -> will it survive?
- **Install/remove conditions**: Given protecting group name -> find reagents for installation/removal

### Step 2: Choose the correct function
- `select_protecting_group(functional_group, conditions)` -> best PG for the situation
- `find_orthogonal_set(groups_to_protect)` -> set of PGs that can be removed independently
- `deprotection_sequence(protected_groups, target_group)` -> ordered removal steps
- `check_stability(pg_name, reaction_conditions)` -> whether PG survives given conditions
- Look up `PROTECTING_GROUPS` dict for full details on any PG (install/remove conditions, stability)

### Step 3: Handle special cases
- Orthogonality means each PG can be removed without affecting others
- Acid-labile PGs (TMS, THP, Boc) cannot be used with acid-catalyzed reactions
- Bn is stable to acid/base but requires hydrogenolysis (Pd/C, H2)
- TBDPS > TBDMS in stability (use TBDPS when TBDMS might fail)
- For amines: Boc (acid-labile), Fmoc (base-labile), Cbz (hydrogenolysis)

### Examples
1. **Select alcohol PG for Grignard reaction**: Need base-stable, acid-labile removal
   -> `select_protecting_group('alcohol', {'base': True, 'organometallics': True})` -> TBDMS

2. **Orthogonal set for diol + amine**: Primary OH, secondary OH, NH2
   -> TBDMS on primary OH, TBDPS on secondary OH (both acid-labile but different bulk), Boc on amine
   -> Remove Boc first (TFA), then TBDMS (mild acid), then TBDPS (TBAF)

3. **Check stability**: Will TMS survive NaH (strong base)?
   -> `check_stability('TMS', 'strong_base')` -> True (TMS is stable to base)
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ProtectingGroup:
    name: str
    abbreviation: str
    functional_group: str
    install_conditions: str
    remove_conditions: str
    stable_to: List[str]
    unstable_to: List[str]


# Common protecting groups database
PROTECTING_GROUPS = {
    # Alcohol protecting groups
    'TMS': ProtectingGroup(
        name='Trimethylsilyl',
        abbreviation='TMS',
        functional_group='alcohol',
        install_conditions='TMSCl, imidazole, DMF',
        remove_conditions='TBAF or acid',
        stable_to=['base', 'hydrogenation'],
        unstable_to=['acid', 'fluoride']
    ),
    'TBDMS': ProtectingGroup(
        name='tert-Butyldimethylsilyl',
        abbreviation='TBDMS',
        functional_group='alcohol',
        install_conditions='TBDMSCl, imidazole, DMF',
        remove_conditions='TBAF or acid',
        stable_to=['base', 'hydrogenation', 'Grignard'],
        unstable_to=['fluoride', 'strong acid']
    ),
    'THP': ProtectingGroup(
        name='Tetrahydropyranyl',
        abbreviation='THP',
        functional_group='alcohol',
        install_conditions='DHP, cat. TsOH',
        remove_conditions='dilute acid',
        stable_to=['base', 'organometallics'],
        unstable_to=['acid']
    ),
    'Bn': ProtectingGroup(
        name='Benzyl',
        abbreviation='Bn',
        functional_group='alcohol',
        install_conditions='BnBr, NaH, DMF',
        remove_conditions='H2, Pd/C',
        stable_to=['base', 'acid'],
        unstable_to=['hydrogenolysis']
    ),
    'TBDPS': ProtectingGroup(
        name='tert-Butyldiphenylsilyl',
        abbreviation='TBDPS',
        functional_group='alcohol',
        install_conditions='TBDPSCl, imidazole, DMF',
        remove_conditions='TBAF or HF',
        stable_to=['base', 'acid', 'hydrogenation', 'Grignard', 'reduction'],
        unstable_to=['fluoride', 'strong acid']
    ),
    
    # Amine protecting groups
    'Boc': ProtectingGroup(
        name='tert-Butoxycarbonyl',
        abbreviation='Boc',
        functional_group='amine',
        install_conditions='Boc2O, base',
        remove_conditions='TFA or HCl',
        stable_to=['base', 'hydrogenation'],
        unstable_to=['strong acid']
    ),
    'Fmoc': ProtectingGroup(
        name='9-Fluorenylmethoxycarbonyl',
        abbreviation='Fmoc',
        functional_group='amine',
        install_conditions='Fmoc-Cl, base',
        remove_conditions='Piperidine, base',
        stable_to=['acid'],
        unstable_to=['base']
    ),
    'Cbz': ProtectingGroup(
        name='Carbobenzyloxy',
        abbreviation='Cbz',
        functional_group='amine',
        install_conditions='Cbz-Cl, base',
        remove_conditions='H2, Pd/C',
        stable_to=['acid', 'base'],
        unstable_to=['hydrogenolysis']
    ),
    'Ac': ProtectingGroup(
        name='Acetyl',
        abbreviation='Ac',
        functional_group='alcohol',
        install_conditions='Ac2O, pyridine',
        remove_conditions='base (NaOH, K2CO3)',
        stable_to=['acid', 'reduction'],
        unstable_to=['base']
    ),
    'Bz': ProtectingGroup(
        name='Benzoyl',
        abbreviation='Bz',
        functional_group='alcohol',
        install_conditions='BzCl, pyridine',
        remove_conditions='base (NaOH, K2CO3)',
        stable_to=['acid', 'reduction'],
        unstable_to=['base']
    ),
    
    # Carbonyl protecting groups
    'Acetal': ProtectingGroup(
        name='Acetal',
        abbreviation='Acetal',
        functional_group='aldehyde/ketone',
        install_conditions='ROH, TsOH, remove water',
        remove_conditions='aqueous acid',
        stable_to=['base', 'organometallics'],
        unstable_to=['acid']
    ),
    'Dithiane': ProtectingGroup(
        name='1,3-Dithiane',
        abbreviation='Dithiane',
        functional_group='aldehyde/ketone',
        install_conditions='1,3-propanedithiol, Lewis acid',
        remove_conditions='Hg(II) or NBS',
        stable_to=['base'],
        unstable_to=['electrophiles', 'Hg(II)']
    ),
    
    # Carboxylic acid protecting groups
    'Me ester': ProtectingGroup(
        name='Methyl ester',
        abbreviation='Me ester',
        functional_group='carboxylic acid',
        install_conditions='MeOH, H+ or CH2N2',
        remove_conditions='NaOH, then H+',
        stable_to=['base (mild)', 'organometallics'],
        unstable_to=['strong base']
    ),
    't-Bu ester': ProtectingGroup(
        name='tert-Butyl ester',
        abbreviation='t-Bu ester',
        functional_group='carboxylic acid',
        install_conditions='isobutylene, H+ or Boc2O',
        remove_conditions='TFA or HCl',
        stable_to=['base', 'hydrogenation'],
        unstable_to=['strong acid']
    ),
}


def get_protecting_group(abbreviation: str) -> ProtectingGroup:
    """
    Get protecting group information by abbreviation.
    
    Parameters
    ----------
    abbreviation : str
        PG abbreviation (e.g., 'TBDMS', 'Boc', 'Fmoc')
    
    Returns
    -------
    ProtectingGroup
        Protecting group data
    
    Examples
    --------
    >>> pg = get_protecting_group('Boc')
    >>> pg.name
    'tert-Butoxycarbonyl'
    """
    # Try exact match first, then case-insensitive
    if abbreviation in PROTECTING_GROUPS:
        return PROTECTING_GROUPS[abbreviation]
    return PROTECTING_GROUPS.get(abbreviation.upper())


def list_protecting_groups(functional_group: str = None) -> List[str]:
    """
    List available protecting groups.
    
    Parameters
    ----------
    functional_group : str, optional
        Filter by functional group ('alcohol', 'amine', 'aldehyde', etc.)
    
    Returns
    -------
    list
        List of protecting group abbreviations
    
    Examples
    --------
    >>> list_protecting_groups('amine')
    ['Boc', 'Fmoc', 'Cbz']
    """
    if functional_group is None:
        return list(PROTECTING_GROUPS.keys())
    
    return [
        abbr for abbr, pg in PROTECTING_GROUPS.items()
        if functional_group.lower() in pg.functional_group.lower()
    ]


def check_compatibility(pg1: str, pg2: str) -> Dict:
    """
    Check if two protecting groups are compatible (orthogonal).
    
    Parameters
    ----------
    pg1 : str
        First protecting group abbreviation
    pg2 : str
        Second protecting group abbreviation
    
    Returns
    -------
    dict
        Compatibility information
    
    Examples
    --------
    >>> check_compatibility('Boc', 'Fmoc')['orthogonal']
    True
    """
    p1 = get_protecting_group(pg1)
    p2 = get_protecting_group(pg2)
    
    if not p1 or not p2:
        return {'error': 'Unknown protecting group'}
    
    # Check if removal conditions of one affect the other
    p1_stable_to_p2_removal = p2.remove_conditions.split()[0] in ' '.join(p1.stable_to).lower()
    p2_stable_to_p1_removal = p1.remove_conditions.split()[0] in ' '.join(p2.stable_to).lower()
    
    orthogonal = p1_stable_to_p2_removal or p2_stable_to_p1_removal
    
    return {
        'pg1': pg1,
        'pg2': pg2,
        'orthogonal': orthogonal,
        'p1_stable_to_p2_removal': p1_stable_to_p2_removal,
        'p2_stable_to_p1_removal': p2_stable_to_p1_removal,
        'recommended_order': f"Remove {pg1} first" if p1_stable_to_p2_removal else f"Remove {pg2} first" if p2_stable_to_p1_removal else "Neither is ideal"
    }


def deprotection_sequence(protecting_groups: List[str]) -> List[str]:
    """
    Determine optimal deprotection sequence.
    
    Parameters
    ----------
    protecting_groups : list
        List of protecting group abbreviations
    
    Returns
    -------
    list
        Ordered deprotection sequence
    
    Examples
    --------
    >>> deprotection_sequence(['Boc', 'Fmoc', 'Bn'])
    ['Fmoc', 'Boc', 'Bn']
    """
    # Priority order based on removal conditions
    priority = {
        'Fmoc': 1,  # Base labile - remove first
        'Boc': 2,   # Acid labile
        'Cbz': 3,   # Hydrogenolysis
        'Bn': 3,    # Hydrogenolysis
        'THP': 4,   # Mild acid
        'TMS': 5,   # Very labile
        'TBDMS': 6, # Fluoride
    }
    
    return sorted(protecting_groups, key=lambda x: priority.get(x.upper(), 99))


def pg_selection(functional_group: str, conditions: list, priority: str = 'stability') -> dict:
    """Select best protecting group for a functional group under given conditions."""
    candidates = list_protecting_groups(functional_group)
    if not candidates:
        return {'recommended': None, 'error': f'No PGs found for {functional_group}'}
    
    condition_synonyms = {
        'reduction': ['hydrogenation', 'reduction', 'hydrogenolysis'],
        'acid': ['acid', 'strong acid'],
        'base': ['base', 'basic'],
        'oxidation': ['oxidation', 'oxidizing'],
    }
    
    def cond_match(a, b):
        """Check if condition a relates to condition b. Exact match required for modifiers."""
        a_l, b_l = a.lower().strip(), b.lower().strip()
        if a_l == b_l: return True
        # Don't let 'acid' match 'strong acid' or 'dilute acid'
        if a_l == 'acid' and ('strong' in b_l or 'dilute' in b_l): return False
        if b_l == 'acid' and ('strong' in a_l or 'dilute' in a_l): return False
        if a_l in b_l or b_l in a_l: return True
        for syns in condition_synonyms.values():
            sa, sb = [s.lower() for s in syns], [s.lower() for s in syns]
            if a_l in sa and b_l in sb: return True
        return False
    
    scored = []
    for name in candidates:
        pg = get_protecting_group(name)
        if not pg: continue
        unstable = [s.lower() for s in pg.unstable_to]
        stable_list = [s.lower() for s in pg.stable_to]
        
        is_stable = True
        for cond in conditions:
            if any(cond_match(cond.lower(), u) for u in unstable):
                is_stable = False; break
        if not is_stable: continue
        
        stable_count = sum(1 for c in conditions if any(cond_match(c.lower(), s) for s in stable_list))
        # Prefer groups with more stable conditions AND more stable entries (more robust)
        robustness = len(pg.stable_to)
        scored.append((name, stable_count, robustness, len(pg.unstable_to)))
    
    if not scored:
        for name in candidates:
            pg = get_protecting_group(name)
            if pg: scored.append((name, 0, 0, len(pg.unstable_to)))
    
    if priority == 'yield':
        scored.sort(key=lambda x: (x[3], -x[1]))
    else:
        # stability: prefer more stable conditions matched, then more robust, then fewer unstable
        scored.sort(key=lambda x: (-x[1], -x[2], x[3]))
    
    return {'recommended': scored[0][0] if scored else None}


def orthogonality_check(pg_list: list) -> dict:
    """Check if a set of protecting groups are orthogonal (independently removable)."""
    if not pg_list:
        return {'is_orthogonal': True, 'conflicts': []}
    
    removal_conds = {}
    for name in pg_list:
        pg = get_protecting_group(name)
        if pg:
            removal_conds[name] = pg.remove_conditions.lower()
        else:
            removal_conds[name] = ''
    
    conflicts = []
    names = list(pg_list)
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            ri, rj = removal_conds[names[i]], removal_conds[names[j]]
            # Check if primary removal conditions overlap significantly
            if ri == rj and ri:
                conflicts.append((names[i], names[j], ri))
            elif ri and rj:
                # Check if one removal condition would affect the other
                ri_words = set(ri.replace(',', ' ').replace('or', ' ').split())
                rj_words = set(rj.replace(',', ' ').replace('or', ' ').split())
                shared = ri_words & rj_words
                # Shared keywords like "acid", "base", "TBAF" mean not orthogonal
                trigger_words = {'acid', 'base', 'tbaf', 'fluoride', 'h2', 'hydrogen', 'piperidine'}
                if shared & trigger_words:
                    conflicts.append((names[i], names[j], str(shared & trigger_words)))
    
    return {'is_orthogonal': len(conflicts) == 0, 'conflicts': conflicts}


# Self-test
if __name__ == '__main__':
    print("Protecting Groups Tools Test")
    print("=" * 40)
    
    # Test lookup
    print("\nProtecting group lookup:")
    pg = get_protecting_group('Boc')
    if pg:
        print(f"  Boc: {pg.name}")
        print(f"  Install: {pg.install_conditions}")
        print(f"  Remove: {pg.remove_conditions}")
    else:
        print("  Boc: Not found")
    
    # Test listing
    print("\nAmine protecting groups:")
    amine_pgs = list_protecting_groups('amine')
    print(f"  {amine_pgs}")
    
    # Test compatibility
    print("\nCompatibility check:")
    comp = check_compatibility('Boc', 'Fmoc')
    print(f"  Boc + Fmoc: orthogonal = {comp['orthogonal']}")
    print(f"  Recommended: {comp['recommended_order']}")
    
    # Test sequence
    print("\nDeprotection sequence for ['Boc', 'Fmoc', 'Bn']:")
    seq = deprotection_sequence(['Boc', 'Fmoc', 'Bn'])
    print(f"  {seq}")
    
    print("\nAll tests passed")
