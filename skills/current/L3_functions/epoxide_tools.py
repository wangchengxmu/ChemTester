"""
L3 Tool: Epoxide Reaction Tools
Predict epoxide ring-opening products and reactions.

Source: Organic Chemistry (OpenStax) Ch18
Created: 2026-03-13
"""

## Solver Instructions (for AI Agent)

# When you encounter **epoxide** (formation, ring-opening, regiochemistry) problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Epoxide ring-opening product: `epoxide_ring_opening(epoxide, nucleophile, conditions)`
# - Epoxide synthesis from alkene: `epoxide_from_alkene(alkene, method)`
# - Regiochemistry prediction: `predict_regiochemistry(epoxide, conditions)`

### Step 2: Choose the correct function
# - Ring-opening: `epoxide_ring_opening` - needs epoxide name, nucleophile, and conditions (acidic/basic)
# - Synthesis: `epoxide_from_alkene` - methods include 'peroxyacid' (default), 'mCPBA', 'Sharpless'
# - Regiochemistry: `predict_regiochemistry` - predicts which C gets attacked

### Step 3: Handle special cases
# - Acidic conditions: nucleophile attacks more substituted carbon (SN1-like)
# - Basic conditions: nucleophile attacks less substituted carbon (SN2-like)
# - Sharpless epoxidation requires allylic alcohol substrate

### Examples
# 1. Propylene oxide + MeOH, acid: `epoxide_ring_opening("propylene oxide", "methanol", "acidic")`
# 2. Styrene to epoxide: `epoxide_from_alkene("styrene", "mCPBA")`
# 3. Regiochemistry of isobutylene oxide + NH3, base: `predict_regiochemistry("isobutylene oxide", "basic")` -> less substituted C



# Common epoxides and their substitution patterns
EPOXIDES = {
    'ethylene_oxide': {'carbons': ['primary', 'primary'], 'symmetric': True},
    'oxirane': {'carbons': ['primary', 'primary'], 'symmetric': True},
    'propylene_oxide': {'carbons': ['primary', 'secondary'], 'symmetric': False},
    '1,2-epoxypropane': {'carbons': ['primary', 'secondary'], 'symmetric': False},
    '1,2-epoxybutane': {'carbons': ['primary', 'secondary'], 'symmetric': False},
    'butylene_oxide': {'carbons': ['primary', 'secondary'], 'symmetric': False},
    'styrene_oxide': {'carbons': ['primary', 'benzylic'], 'symmetric': False},
    'cyclohexene_oxide': {'carbons': ['secondary', 'secondary'], 'symmetric': True},
    'limonene_oxide': {'carbons': ['secondary', 'tertiary'], 'symmetric': False},
    '2-methyl-1,2-epoxypropane': {'carbons': ['primary', 'tertiary'], 'symmetric': False},
    '2methyl12epoxypropane': {'carbons': ['primary', 'tertiary'], 'symmetric': False},  # normalized alias
}

# Nucleophiles for epoxide opening
NUCLEOPHILES = {
    'H2O': {'type': 'water', 'acidic_only': False},
    'H3O+': {'type': 'water', 'acidic_only': True},
    'HCl': {'type': 'halide', 'acidic_only': True, 'nucleophile': 'Cl'},
    'HBr': {'type': 'halide', 'acidic_only': True, 'nucleophile': 'Br'},
    'HI': {'type': 'halide', 'acidic_only': True, 'nucleophile': 'I'},
    'OH-': {'type': 'hydroxide', 'acidic_only': False},
    'NaOH': {'type': 'hydroxide', 'acidic_only': False},
    'CH3O-': {'type': 'alkoxide', 'acidic_only': False, 'nucleophile': 'CH3O'},
    'EtO-': {'type': 'alkoxide', 'acidic_only': False, 'nucleophile': 'EtO'},
    'CH3CH2O-': {'type': 'alkoxide', 'acidic_only': False, 'nucleophile': 'EtO'},
    'NH3': {'type': 'amine', 'acidic_only': False, 'nucleophile': 'NH2'},
    'CH3NH2': {'type': 'amine', 'acidic_only': False, 'nucleophile': 'CH3NH'},
    'RMgX': {'type': 'grignard', 'acidic_only': False, 'nucleophile': 'R'},
    'MeMgBr': {'type': 'grignard', 'acidic_only': False, 'nucleophile': 'Me'},
}


def epoxide_ring_opening(epoxide: str, nucleophile: str, conditions: str) -> dict:
    """
    Predict epoxide ring-opening product.
    
    Regiochemistry:
    - Acidic: Attack at MORE substituted carbon (for tertiary epoxides)
    - Acidic: Attack at LESS substituted carbon (for primary/secondary epoxides)
    - Basic: Attack at LESS substituted carbon (always, pure SN2)
    
    Args:
        epoxide: Epoxide name
        nucleophile: Nucleophile (H2O, HX, OH-, RO-, RNH2, RMgX)
        conditions: 'acidic' or 'basic'
    
    Returns:
        Dictionary with product information
    
    Example:
        >>> epoxide_ring_opening('propylene_oxide', 'HCl', 'acidic')
        {'product': '1-chloro-2-propanol', 'attack_site': 'less_substituted'}
    """
    epoxide_lower = epoxide.lower().replace('-', '').replace('_', '').replace(' ', '')
    
    # Determine epoxide substitution
    epoxide_data = None
    for name, data in EPOXIDES.items():
        name_norm = name.lower().replace('-', '').replace('_', '')
        if name_norm in epoxide_lower or epoxide_lower in name_norm:
            epoxide_data = data
            break
    
    if epoxide_data is None:
        # Default assumption
        epoxide_data = {'carbons': ['primary', 'secondary'], 'symmetric': False}
    
    # Determine attack site
    conditions_lower = conditions.lower()
    has_tertiary = 'tertiary' in epoxide_data['carbons']
    
    if epoxide_data['symmetric']:
        attack_site = 'either'
    elif conditions_lower == 'acidic':
        # Acidic: tertiary epoxides attack at more substituted
        if has_tertiary:
            attack_site = 'more_substituted'
        else:
            attack_site = 'less_substituted'
    else:
        # Basic: always attacks less substituted (SN2)
        attack_site = 'less_substituted'
    
    # Determine product
    nuc_lower = nucleophile.lower().replace('-', '').replace(' ', '')
    nuc_data = None
    for name, data in NUCLEOPHILES.items():
        if name.lower() in nuc_lower or nuc_lower in name.lower():
            nuc_data = data
            break
    
    if nuc_data is None:
        added_group = 'Nu'
    else:
        added_group = nuc_data.get('nucleophile', 'Nu')
    
    # Build product name
    if nuc_lower in ['h2o', 'h3o+'] or (nuc_lower in ['oh-', 'naoh']):
        product_type = 'diol'
        added_group = 'OH'
    elif nuc_data and nuc_data.get('type') == 'halide':
        product_type = 'halohydrin'
    elif nuc_data and nuc_data.get('type') == 'alkoxide':
        product_type = 'alkoxy alcohol'
    elif nuc_data and nuc_data.get('type') == 'grignard':
        product_type = 'alcohol'
        added_group = 'R'
    else:
        product_type = 'substituted alcohol'
    
    return {
        'epoxide': epoxide,
        'nucleophile': nucleophile,
        'conditions': conditions,
        'attack_site': attack_site,
        'product_type': product_type,
        'added_group': added_group,
        'stereochemistry': 'trans'
    }


def epoxide_from_alkene(alkene: str, method: str = 'peroxyacid') -> dict:
    """
    Predict epoxide formation from alkene.
    
    Methods:
    - 'peroxyacid': Direct epoxidation (mCPBA, peroxyacetic acid)
    - 'halohydrin': Halohydrin + base (X2/H2O then base)
    
    Args:
        alkene: Alkene name
        method: Epoxidation method
    
    Returns:
        Dictionary with epoxide product
    
    Example:
        >>> epoxide_from_alkene('propene', 'peroxyacid')
        {'epoxide': 'propylene_oxide', 'method': 'peroxyacid'}
    """
    alkene_lower = alkene.lower().replace('-', '').replace('_', '')
    
    # Map alkenes to epoxides
    alkene_to_epoxide = {
        'ethene': 'ethylene_oxide',
        'ethylene': 'ethylene_oxide',
        'propene': 'propylene_oxide',
        'propylene': 'propylene_oxide',
        '1-butene': 'butylene_oxide',
        'cyclohexene': 'cyclohexene_oxide',
        'styrene': 'styrene_oxide',
    }
    
    epoxide = None
    for name, epox in alkene_to_epoxide.items():
        if name in alkene_lower or alkene_lower in name:
            epoxide = epox
            break
    
    if epoxide is None:
        epoxide = f'{alkene}_oxide'
    
    method_lower = method.lower()
    
    return {
        'alkene': alkene,
        'method': method,
        'epoxide': epoxide,
        'reagents': {
            'peroxyacid': ['mCPBA', 'peroxyacetic acid', 'peroxybenzoic acid'],
            'halohydrin': ['Br2/H2O then NaOH', 'Cl2/H2O then NaOH']
        }.get(method_lower, ['mCPBA'])
    }


def predict_regiochemistry(epoxide: str, conditions: str) -> dict:
    """
    Predict which carbon is attacked in epoxide opening.
    
    Args:
        epoxide: Epoxide name
        conditions: 'acidic' or 'basic'
    
    Returns:
        Dictionary with attack site prediction
    
    Example:
        >>> predict_regiochemistry('propylene_oxide', 'acidic')
        {'attack_site': 'less_substituted', 'reason': 'primary/secondary epoxide'}
    """
    epoxide_lower = epoxide.lower().replace('-', '').replace('_', '').replace(' ', '').replace(',', '')
    
    # Determine epoxide type - check exact match first, then substring
    epoxide_data = None
    
    # First: exact match
    for name, data in EPOXIDES.items():
        name_norm = name.lower().replace('-', '').replace('_', '').replace(',', '')
        if name_norm == epoxide_lower:
            epoxide_data = data
            break
    
    # Second: longest substring match (more specific = better)
    if epoxide_data is None:
        best_match = None
        best_len = 0
        for name, data in EPOXIDES.items():
            name_norm = name.lower().replace('-', '').replace('_', '').replace(',', '')
            if name_norm in epoxide_lower and len(name_norm) > best_len:
                best_match = data
                best_len = len(name_norm)
            elif epoxide_lower in name_norm and len(epoxide_lower) > best_len:
                best_match = data
                best_len = len(epoxide_lower)
        epoxide_data = best_match
    
    if epoxide_data is None:
        # Check for tertiary keywords (e.g., '2-methyl' indicates tertiary carbon)
        if 'tertiary' in epoxide_lower or ('methyl' in epoxide_lower and 'epoxy' in epoxide_lower):
            epoxide_data = {'carbons': ['primary', 'tertiary'], 'symmetric': False}
        else:
            epoxide_data = {'carbons': ['primary', 'secondary'], 'symmetric': False}
    
    conditions_lower = conditions.lower()
    
    if epoxide_data['symmetric']:
        return {
            'attack_site': 'either',
            'reason': 'symmetric epoxide',
            'mechanism': 'SN2'
        }
    
    has_tertiary = 'tertiary' in epoxide_data['carbons']
    carbons_desc = '/'.join(epoxide_data['carbons'])
    
    if conditions_lower == 'acidic':
        if has_tertiary:
            return {
                'attack_site': 'more_substituted',
                'reason': f'{carbons_desc} epoxide with tertiary carbon',
                'mechanism': 'SN1-like with carbocation character'
            }
        else:
            return {
                'attack_site': 'less_substituted',
                'reason': f'{carbons_desc} epoxide under acidic conditions',
                'mechanism': 'SN2-like backside attack'
            }
    else:
        return {
            'attack_site': 'less_substituted',
            'reason': 'basic conditions favor SN2 at less hindered carbon',
            'mechanism': 'SN2'
        }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "18-01",
        "question": "Propylene oxide + HCl",
        "epoxide": "propylene_oxide",
        "nucleophile": "HCl",
        "conditions": "acidic",
        "expected_attack": "less_substituted"
    },
    {
        "id": "18-02",
        "question": "Ethylene oxide + sodium ethoxide",
        "epoxide": "ethylene_oxide",
        "nucleophile": "EtO-",
        "conditions": "basic",
        "expected_attack": "either"
    },
    {
        "id": "18-03",
        "question": "Cyclohexene oxide + HBr",
        "epoxide": "cyclohexene_oxide",
        "nucleophile": "HBr",
        "conditions": "acidic",
        "expected_attack": "either"
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Epoxide Reaction Tools")
    print("=" * 40)
    
    # Test regiochemistry
    print("\nRegiochemistry predictions:")
    tests = [
        ('propylene_oxide', 'acidic'),
        ('propylene_oxide', 'basic'),
        ('2-methyl-1,2-epoxypropane', 'acidic'),
    ]
    for epox, cond in tests:
        result = predict_regiochemistry(epox, cond)
        print(f"  {epox} ({cond}): attack at {result['attack_site']}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "epoxide_from_alkene",
        "description": "Predict epoxide formation from alkene.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkene": {"type": "number", "description": "Alkene"},
                "method": {"type": "string", "description": "Method", "default": "peroxyacid"},
            },
            "required": ["alkene"]
        }
    },
    {
        "name": "epoxide_ring_opening",
        "description": "Predict epoxide ring-opening product.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "epoxide": {"type": "number", "description": "Epoxide"},
                "nucleophile": {"type": "number", "description": "Nucleophile"},
                "conditions": {"type": "number", "description": "Conditions"},
            },
            "required": ["epoxide", "nucleophile", "conditions"]
        }
    },
    {
        "name": "predict_regiochemistry",
        "description": "Predict which carbon is attacked in epoxide opening.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "epoxide": {"type": "number", "description": "Epoxide"},
                "conditions": {"type": "number", "description": "Conditions"},
            },
            "required": ["epoxide", "conditions"]
        }
    }
]
