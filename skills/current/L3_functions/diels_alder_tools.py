"""
L3 Tool: Diels-Alder Reaction Tools
Predict Diels-Alder products and reactivity.

Source: Organic Chemistry (OpenStax) Ch14
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter Diels-Alder reaction problems - predicting product characteristics, dienophile reactivity, diene conformation, stereochemistry, or ranking dienophiles - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a diene + dienophile -> predict reaction product characteristics?
- Given a compound -> check if it's a good dienophile (has EWG)?
- Given a diene -> determine its conformation (s-cis vs flexible)?
- Given cis/trans dienophile -> predict product stereochemistry?
- Given multiple dienophiles -> rank by reactivity?

### Step 2: Choose the correct function
- **Product prediction:** `diels_alder_product(diene, dienophile)` -> dict with product_type ('cyclohexene derivative'), bonds_formed (2), diene_conformation, dienophile_reactivity, and reaction_occurs bool
- **Good dienophile check:** `is_good_dienophile(compound)` -> True if has electron-withdrawing group. maleic_anhydride=True, ethylene=False
- **Diene conformation:** `diene_conformation(diene)` -> 'locked_s-cis' (cyclic dienes), 'flexible' (acyclic). Cyclopentadiene=locked_s-cis, butadiene=flexible
- **Stereochemistry prediction:** `predict_stereochemistry(diene, dienophile)` -> cis/trans substituent preservation, endo/exo preference (endo is kinetically favored)
- **Reactivity ranking:** `diels_alder_reactivity_order(dienophiles)` -> sorted list by reactivity (very_high > high > low)

### Step 3: Handle special cases
- Cyclic dienes are locked in s-cis -> always reactive; acyclic need to rotate to s-cis
- Diels-Alder is CONCERTED and STEREOSPECIFIC - cis dienophile -> cis product
- Endo rule: electron-withdrawing groups on dienophile orient UNDER the diene (kinetic)
- Two EWGs on dienophile = very_high reactivity (maleic anhydride, benzoquinone)

### Examples
```python
# Example 1: Predict product of cyclopentadiene + maleic anhydride
diels_alder_product('cyclopentadiene', 'maleic_anhydride')  -> reaction_occurs=True, reactivity=very_high

# Example 2: Is ethylene a good dienophile?
is_good_dienophile('ethylene')  -> False (no EWG)

# Example 3: Diene conformation
diene_conformation('butadiene')  -> 'flexible'
diene_conformation('cyclopentadiene')  -> 'locked_s-cis'

# Example 4: Rank dienophiles
diels_alder_reactivity_order(['ethylene', 'acrolein', 'maleic_anhydride'])
# -> [('maleic_anhydride', 'very_high'), ('acrolein', 'high'), ('ethylene', 'low')]
```
"""

# Reactive dienophiles (electron-withdrawing groups increase reactivity)
REACTIVE_DIENOPHILES = {
    'maleic_anhydride': {'ewg_count': 2, 'reactivity': 'very_high'},
    'benzoquinone': {'ewg_count': 2, 'reactivity': 'very_high'},
    'acrolein': {'ewg_count': 1, 'reactivity': 'high'},
    'propenal': {'ewg_count': 1, 'reactivity': 'high'},  # Same as acrolein
    'methyl_acrylate': {'ewg_count': 1, 'reactivity': 'high'},
    'acrylonitrile': {'ewg_count': 1, 'reactivity': 'high'},
    'ethylene': {'ewg_count': 0, 'reactivity': 'low'},
    'ethene': {'ewg_count': 0, 'reactivity': 'low'},
}

# Common dienes and their conformations
DIENE_CONFORMATIONS = {
    'cyclopentadiene': 'locked_s-cis',
    '1,3-cyclopentadiene': 'locked_s-cis',
    'cyclohexadiene': 'locked_s-cis',
    '1,3-cyclohexadiene': 'locked_s-cis',
    'butadiene': 'flexible',
    '1,3-butadiene': 'flexible',
    'isoprene': 'flexible',
    '2,3-dimethylbutadiene': 'flexible',
}

# Electron-withdrawing groups
EW_GROUPS = ['CHO', 'COR', 'COOR', 'COOH', 'CN', 'NO2', 'CO', 'C(O)O']


def diels_alder_product(diene: str, dienophile: str) -> dict:
    """
    Predict Diels-Alder product characteristics.
    
    Args:
        diene: Diene name
        dienophile: Dienophile name
    
    Returns:
        Dictionary with product information
    
    Example:
        >>> diels_alder_product('butadiene', 'maleic_anhydride')
        {'product': 'cyclohexene derivative', 'bonds_formed': 2, ...}
    """
    # Normalize names (remove spaces, hyphens, underscores)
    diene_norm = diene.lower().replace('-', '').replace('_', '').replace(' ', '')
    dienophile_norm = dienophile.lower().replace('-', '').replace('_', '').replace(' ', '')
    
    # Check diene conformation
    diene_conf = diene_conformation(diene)
    
    # Check dienophile reactivity - use original name too
    dienophile_react = is_good_dienophile(dienophile)
    reactivity = 'high' if dienophile_react else 'low'
    
    # Check for very_high reactivity
    for name, data in REACTIVE_DIENOPHILES.items():
        name_norm = name.lower().replace('_', '')
        if name_norm in dienophile_norm or dienophile_norm in name_norm:
            reactivity = data['reactivity']
            break
    
    result = {
        'diene': diene,
        'dienophile': dienophile,
        'diene_conformation': diene_conf,
        'dienophile_reactivity': reactivity,
        'reaction_occurs': diene_conf in ['locked_s-cis', 'flexible'],
        'bonds_formed': 2,
        'product_type': 'cyclohexene derivative',
    }
    
    return result


def is_good_dienophile(compound: str) -> bool:
    """
    Check if compound is a good dienophile.
    
    Good dienophiles have electron-withdrawing groups that make
    them more reactive in Diels-Alder reactions.
    
    Args:
        compound: Compound name or SMILES
    
    Returns:
        True if compound has electron-withdrawing groups
    
    Example:
        >>> is_good_dienophile('maleic_anhydride')
        True
        >>> is_good_dienophile('ethylene')
        False
    """
    compound_lower = compound.lower().replace('-', '').replace('_', '')
    
    # Check known dienophiles
    if compound_lower in REACTIVE_DIENOPHILES:
        return REACTIVE_DIENOPHILES[compound_lower]['reactivity'] in ['high', 'very_high']
    
    # Check for EWG in name
    for ewg in EW_GROUPS:
        if ewg.lower() in compound_lower:
            return True
    
    # Check for common EWG keywords
    ewg_keywords = ['aldehyde', 'ketone', 'ester', 'nitrile', 'anhydride', 
                    'quinone', 'acryl', 'acrolein', 'maleic']
    for keyword in ewg_keywords:
        if keyword in compound_lower:
            return True
    
    return False


def diene_conformation(diene: str) -> str:
    """
    Determine diene conformation (s-cis or s-trans).
    
    Cyclic dienes are locked in s-cis conformation.
    Acyclic dienes can rotate between s-cis and s-trans.
    
    Args:
        diene: Diene name
    
    Returns:
        'locked_s-cis', 'flexible', or 's-trans'
    
    Example:
        >>> diene_conformation('cyclopentadiene')
        'locked_s-cis'
        >>> diene_conformation('butadiene')
        'flexible'
    """
    diene_lower = diene.lower().replace('-', '').replace('_', '')
    
    # Check known dienes
    if diene_lower in DIENE_CONFORMATIONS:
        return DIENE_CONFORMATIONS[diene_lower]
    
    # Check for cyclic diene keywords
    cyclic_keywords = ['cyclo', 'cyclic']
    for keyword in cyclic_keywords:
        if keyword in diene_lower:
            return 'locked_s-cis'
    
    return 'flexible'


def predict_stereochemistry(diene: str, dienophile: str) -> dict:
    """
    Predict stereochemistry of Diels-Alder product.
    
    Diels-Alder is stereospecific:
    - cis-dienophile gives cis-substituents in product
    - trans-dienophile gives trans-substituents in product
    - Endo product is kinetically favored
    
    Args:
        diene: Diene name
        dienophile: Dienophile name
    
    Returns:
        Dictionary with stereochemistry prediction
    
    Example:
        >>> predict_stereochemistry('butadiene', 'cis-dichloroethene')
        {'substituents': 'cis', 'endo_exo': 'endo preferred'}
    """
    dienophile_lower = dienophile.lower()
    
    # Determine substituent stereochemistry
    if 'cis' in dienophile_lower:
        substituent_config = 'cis'
    elif 'trans' in dienophile_lower:
        substituent_config = 'trans'
    else:
        substituent_config = 'preserved from dienophile'
    
    # Endo is typically preferred
    endo_exo = 'endo preferred (kinetic product)'
    
    return {
        'substituents': substituent_config,
        'endo_exo': endo_exo,
        'stereospecific': True,
        'concerted': True
    }


def diels_alder_reactivity_order(dienophiles: list) -> list:
    """
    Rank dienophiles by reactivity in Diels-Alder.
    
    Args:
        dienophiles: List of dienophile names
    
    Returns:
        List of (dienophile, reactivity) tuples sorted by reactivity
    
    Example:
        >>> diels_alder_reactivity_order(['ethylene', 'acrolein', 'maleic_anhydride'])
        [('maleic_anhydride', 'very_high'), ('acrolein', 'high'), ('ethylene', 'low')]
    """
    ranked = []
    for d in dienophiles:
        d_lower = d.lower().replace('-', '').replace('_', '').replace(' ', '')
        
        # Check known dienophiles
        found = False
        for name, data in REACTIVE_DIENOPHILES.items():
            name_norm = name.lower().replace('_', '')
            if name_norm in d_lower or d_lower in name_norm:
                ranked.append((d, data['reactivity']))
                found = True
                break
        
        if not found:
            if is_good_dienophile(d):
                ranked.append((d, 'high'))
            else:
                ranked.append((d, 'low'))
    
    # Sort by reactivity
    reactivity_order = {'very_high': 3, 'high': 2, 'low': 1}
    ranked.sort(key=lambda x: reactivity_order.get(x[1], 0), reverse=True)
    
    return ranked


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "14-01",
        "question": "Diels-Alder product of cyclopentadiene + maleic anhydride",
        "diene": "cyclopentadiene",
        "dienophile": "maleic_anhydride",
        "expected_conformation": "locked_s-cis",
        "expected_reactivity": "very_high"
    },
    {
        "id": "14-02",
        "question": "Rank dienophiles by reactivity",
        "dienophiles": ["ethylene", "acrolein", "maleic_anhydride"],
        "expected_order": ["maleic_anhydride", "acrolein", "ethylene"]
    },
    {
        "id": "14-03",
        "question": "Diene conformation of 1,3-cyclohexadiene",
        "diene": "1,3-cyclohexadiene",
        "expected": "locked_s-cis"
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Diels-Alder Reaction Tools")
    print("=" * 40)
    
    # Test dienophile reactivity
    print("\nDienophile reactivity:")
    for d in ['ethylene', 'acrolein', 'maleic_anhydride']:
        print(f"  {d}: {is_good_dienophile(d)}")
    
    # Test diene conformation
    print("\nDiene conformations:")
    for d in ['butadiene', 'cyclopentadiene']:
        print(f"  {d}: {diene_conformation(d)}")
    
    # Test stereochemistry
    print("\nStereochemistry prediction:")
    result = predict_stereochemistry('butadiene', 'cis-dichloroethene')
    print(f"  cis-dienophile: {result}")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'diels_alder_product', 'description': "Predict Diels-Alder product characteristics.\n\nArgs:\n    diene: Diene name\n    dienophile: Dienophile name\n\nReturns:\n    Dictionary with product information\n\nExample:\n    >>> diels_alder_product('butadiene', 'maleic_anhydride')\n    {'product': 'cyclohexene derivative', 'bonds_formed': 2, ...}", 'inputSchema': {'type': 'object', 'properties': {'diene': {'type': 'number', 'description': 'Diene'}, 'dienophile': {'type': 'number', 'description': 'Dienophile'}}, 'required': ['diene', 'dienophile']}},
    {'name': 'diels_alder_reactivity_order', 'description': "Rank dienophiles by reactivity in Diels-Alder.\n\nArgs:\n    dienophiles: List of dienophile names\n\nReturns:\n    List of (dienophile, reactivity) tuples sorted by reactivity\n\nExample:\n    >>> diels_alder_reactivity_order(['ethylene', 'acrolein', 'maleic_anhydride'])\n    [('maleic_anhydride', 'very_high'), ('acrolein', 'high'), ('ethylene', 'low')]", 'inputSchema': {'type': 'object', 'properties': {'dienophiles': {'type': 'number', 'description': 'Dienophiles'}}, 'required': ['dienophiles']}},
    {'name': 'diene_conformation', 'description': "Determine diene conformation (s-cis or s-trans).\n\nCyclic dienes are locked in s-cis conformation.\nAcyclic dienes can rotate between s-cis and s-trans.\n\nArgs:\n    diene: Diene name\n\nReturns:\n    'locked_s-cis', 'flexible', or 's-trans'\n\nExample:\n    >>> diene_conformation('cyclopentadiene')\n    'locked_s-cis'\n    >>> diene_conformation('butadiene')\n    'flexible'", 'inputSchema': {'type': 'object', 'properties': {'diene': {'type': 'number', 'description': 'Diene'}}, 'required': ['diene']}},
    {'name': 'is_good_dienophile', 'description': "Check if compound is a good dienophile.\n\nGood dienophiles have electron-withdrawing groups that make\nthem more reactive in Diels-Alder reactions.\n\nArgs:\n    compound: Compound name or SMILES\n\nReturns:\n    true if compound has electron-withdrawing groups\n\nExample:\n    >>> is_good_dienophile('maleic_anhydride')\n    true\n    >>> is_good_dienophile('ethylene')\n    false", 'inputSchema': {'type': 'object', 'properties': {'compound': {'type': 'string', 'description': 'Compound'}}, 'required': ['compound']}},
    {'name': 'predict_stereochemistry', 'description': "Predict stereochemistry of Diels-Alder product.\n\nDiels-Alder is stereospecific:\n- cis-dienophile gives cis-substituents in product\n- trans-dienophile gives trans-substituents in product\n- Endo product is kinetically favored\n\nArgs:\n    diene: Diene name\n    dienophile: Dienophile name\n\nReturns:\n    Dictionary with stereochemistry prediction\n\nExample:\n    >>> predict_stereochemistry('butadiene', 'cis-dichloroethene')\n    {'substituents': 'cis', 'endo_exo': 'endo preferred'}", 'inputSchema': {'type': 'object', 'properties': {'diene': {'type': 'number', 'description': 'Diene'}, 'dienophile': {'type': 'number', 'description': 'Dienophile'}}, 'required': ['diene', 'dienophile']}}
]
