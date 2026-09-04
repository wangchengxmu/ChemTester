"""
L3 Tool: IR Spectroscopy Tools
Identify functional groups from IR absorption frequencies.

Source: Organic Chemistry (OpenStax) Ch12
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter IR spectroscopy problems - identifying functional groups from wavenumbers, analyzing spectra, distinguishing compounds by IR, or converting units - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a wavenumber (cm-1) -> identify possible functional groups?
- Given a carbonyl wavenumber -> distinguish aldehyde/ketone/ester/acid/amide?
- Given a list of absorptions -> comprehensive spectrum analysis?
- Given two compounds -> how to distinguish by IR?
- Given wavenumber -> what IR region does it fall in?
- Need to convert between wavenumber and wavelength?

### Step 2: Choose the correct function
- **Identify functional group:** `identify_functional_group(wavenumber, tolerance=10)` -> list of matching groups with intensities
- **IR region:** `ir_region(wavenumber)` -> 'X-H stretch' (≥2500), 'triple bond' (2000-2500), 'double bond' (1500-2000), 'fingerprint' (<1500)
- **Carbonyl type:** `carbonyl_type(wavenumber)` -> 'ester'(1730-1750), 'aldehyde'(1720-1730), 'ketone'(1705-1720), 'carboxylic acid'(1700-1705), 'amide'(1680-1700)
- **Convert units:** `wavenumber_to_wavelength(wavenumber)` -> mum (formula: 10000/wn); `wavelength_to_wavenumber(wavelength)` -> cm-1
- **Check for O-H:** `has_oh(absorptions)` -> {'present': True, 'type': 'alcohol O-H'(3400-3650) or 'carboxylic acid O-H'(2500-3100)}
- **Check for C=O:** `has_carbonyl(absorptions)` -> presence, type, and wavenumber
- **Full spectrum analysis:** `analyze_ir_spectrum(absorptions)` -> comprehensive dict with all identified groups, O-H, C=O status
- **Distinguish compounds:** `distinguish_compounds(compound1, compound2)` -> explanation of key IR differences

### Step 3: Handle special cases
- Broad absorption 2500-3100 cm-1 = carboxylic acid O-H (very distinctive)
- Aldehydes show characteristic C-H stretch at 2720-2820 cm-1 (two weak peaks) in addition to C=O
- Fingerprint region (400-1500 cm-1) is complex and rarely diagnostic alone
- Aromatic C=C shows multiple peaks at 1450-1600 cm-1 (not just one)

### Examples
```python
# Example 1: What functional group absorbs at 1715 cm-1?
identify_functional_group(1715)  -> ['C=O ketone - strong', 'C=O carboxylic acid - strong']
carbonyl_type(1715)  -> 'ketone'

# Example 2: Analyze spectrum with absorptions at 3400 and 1710
analyze_ir_spectrum([3400, 1710])  -> has_OH=True(alcohol), has_carbonyl=True(ketone)

# Example 3: Convert 1000 cm-1 to wavelength
wavenumber_to_wavelength(1000)  -> 10.0 mum

# Example 4: Distinguish ethanol from dimethyl ether
distinguish_compounds('ethanol', 'dimethyl ether')  -> 'Ethanol has O-H (3400-3650); ether does not'
```
"""

# IR absorption data by functional group
IR_ABSORPTIONS = {
    'O-H_alcohol': {'min': 3400, 'max': 3650, 'intensity': 'strong, broad'},
    'O-H_carboxylic_acid': {'min': 2500, 'max': 3100, 'intensity': 'strong, broad'},
    'N-H': {'min': 3300, 'max': 3500, 'intensity': 'medium'},
    'C-H_alkane': {'min': 2850, 'max': 2960, 'intensity': 'medium'},
    'C-H_alkene': {'min': 3020, 'max': 3100, 'intensity': 'medium'},
    'C-H_alkyne': {'min': 3300, 'max': 3300, 'intensity': 'strong'},
    'C-H_arene': {'min': 3030, 'max': 3100, 'intensity': 'weak'},
    'C-H_aldehyde': {'min': 2720, 'max': 2820, 'intensity': 'medium'},  # Characteristic
    'C≡N': {'min': 2210, 'max': 2260, 'intensity': 'medium'},
    'C≡C': {'min': 2100, 'max': 2260, 'intensity': 'medium'},
    'C=O_aldehyde': {'min': 1720, 'max': 1740, 'intensity': 'strong'},
    'C=O_ketone': {'min': 1705, 'max': 1725, 'intensity': 'strong'},
    'C=O_ester': {'min': 1730, 'max': 1750, 'intensity': 'strong'},
    'C=O_carboxylic_acid': {'min': 1700, 'max': 1725, 'intensity': 'strong'},
    'C=O_amide': {'min': 1680, 'max': 1700, 'intensity': 'strong'},
    'C=C': {'min': 1640, 'max': 1680, 'intensity': 'medium'},
    'C=C_aromatic': {'min': 1450, 'max': 1600, 'intensity': 'medium'},
    'NO2': {'min': 1510, 'max': 1570, 'intensity': 'strong'},
    'C-O_alcohol': {'min': 1050, 'max': 1150, 'intensity': 'strong'},
    'C-O_ether': {'min': 1070, 'max': 1150, 'intensity': 'strong'},
    'C-O_ester': {'min': 1200, 'max': 1300, 'intensity': 'strong'},
    'C-N': {'min': 1030, 'max': 1230, 'intensity': 'medium'},
    'C-Cl': {'min': 600, 'max': 800, 'intensity': 'strong'},
    'C-Br': {'min': 500, 'max': 600, 'intensity': 'strong'},
}


def identify_functional_group(wavenumber: float, tolerance: float = 10) -> list:
    """
    Identify possible functional groups from IR absorption.
    
    Args:
        wavenumber: Absorption wavenumber in cm-1
        tolerance: Range tolerance in cm-1
    
    Returns:
        List of possible functional groups with their intensities
    
    Example:
        >>> identify_functional_group(1715)
        ['C=O (ketone) - strong']
    """
    matches = []
    
    for group, data in IR_ABSORPTIONS.items():
        if data['min'] - tolerance <= wavenumber <= data['max'] + tolerance:
            # Format the group name
            group_name = group.replace('_', ' ').replace('C H', 'C-H')
            matches.append(f"{group_name} - {data['intensity']}")
    
    return matches if matches else ['Unknown']


def ir_region(wavenumber: float) -> str:
    """
    Identify which IR region a wavenumber falls in.
    
    Args:
        wavenumber: Absorption wavenumber in cm-1
    
    Returns:
        Region name: 'X-H stretch', 'triple bond', 'double bond', or 'fingerprint'
    
    Example:
        >>> ir_region(1715)
        'double bond'
    """
    if wavenumber >= 2500:
        if wavenumber >= 4000:
            return 'X-H stretch (high)'
        return 'X-H stretch'
    elif wavenumber >= 2000:
        return 'triple bond'
    elif wavenumber >= 1500:
        return 'double bond'
    else:
        return 'fingerprint'


def carbonyl_type(wavenumber: float) -> str:
    """
    Identify type of carbonyl from C=O absorption.
    
    Args:
        wavenumber: C=O absorption wavenumber
    
    Returns:
        Type: 'aldehyde', 'ketone', 'ester', 'carboxylic acid', 'amide', or 'unknown'
    
    Example:
        >>> carbonyl_type(1715)
        'ketone'
    """
    # Check in order of most specific ranges
    if 1730 <= wavenumber <= 1750:
        return 'ester'
    elif 1720 <= wavenumber < 1730:
        return 'aldehyde'
    elif 1705 <= wavenumber < 1720:
        return 'ketone'
    elif 1700 <= wavenumber < 1705:
        return 'carboxylic acid'
    elif 1680 <= wavenumber < 1700:
        return 'amide'
    else:
        return 'unknown carbonyl'


def wavenumber_to_wavelength(wavenumber: float) -> float:
    """
    Convert wavenumber (cm-1) to wavelength (mum).
    
    Args:
        wavenumber: Wavenumber in cm-1
    
    Returns:
        Wavelength in micrometers
    
    Example:
        >>> wavenumber_to_wavelength(1000)
        10.0
    """
    if wavenumber <= 0:
        raise ValueError("Wavenumber must be positive")
    return 10000 / wavenumber


def wavelength_to_wavenumber(wavelength: float) -> float:
    """
    Convert wavelength (mum) to wavenumber (cm-1).
    
    Args:
        wavelength: Wavelength in micrometers
    
    Returns:
        Wavenumber in cm-1
    """
    if wavelength <= 0:
        raise ValueError("Wavelength must be positive")
    return 10000 / wavelength


def has_oh(absorptions: list) -> dict:
    """
    Check if IR spectrum indicates O-H group.
    
    Args:
        absorptions: List of wavenumber values
    
    Returns:
        Dictionary with O-H presence and type
    """
    for wn in absorptions:
        if 3400 <= wn <= 3650:
            return {'present': True, 'type': 'alcohol O-H'}
        if 2500 <= wn <= 3100:
            return {'present': True, 'type': 'carboxylic acid O-H'}
    return {'present': False, 'type': None}


def has_carbonyl(absorptions: list) -> dict:
    """
    Check if IR spectrum indicates carbonyl group.
    
    Args:
        absorptions: List of wavenumber values
    
    Returns:
        Dictionary with carbonyl presence and type
    """
    for wn in absorptions:
        if 1670 <= wn <= 1780:
            return {
                'present': True, 
                'type': carbonyl_type(wn),
                'wavenumber': wn
            }
    return {'present': False, 'type': None}


def analyze_ir_spectrum(absorptions: list) -> dict:
    """
    Comprehensive IR spectrum analysis.
    
    Args:
        absorptions: List of (wavenumber, intensity) tuples or just wavenumbers
    
    Returns:
        Dictionary with identified functional groups
    """
    if not absorptions:
        return {'error': 'No absorptions provided'}
    
    # Handle both formats
    if isinstance(absorptions[0], tuple):
        wn_list = [wn for wn, _ in absorptions]
    else:
        wn_list = absorptions
    
    results = {
        'functional_groups': [],
        'has_OH': has_oh(wn_list),
        'has_carbonyl': has_carbonyl(wn_list),
    }
    
    for wn in wn_list:
        groups = identify_functional_group(wn)
        for g in groups:
            if g != 'Unknown' and g not in results['functional_groups']:
                results['functional_groups'].append(g)
    
    return results


def distinguish_compounds(compound1: str, compound2: str, 
                         key_difference: str = None) -> str:
    """
    Explain how to distinguish two compounds by IR.
    
    Args:
        compound1: First compound name
        compound2: Second compound name
        key_difference: Optional hint about the key difference
    
    Returns:
        Explanation of how to distinguish
    """
    # Common distinguishing features
    distinguishing = {
        ('ethanol', 'dimethyl ether'): 'Ethanol has O-H absorption (3400-3650 cm-1); dimethyl ether does not',
        ('ethanol', 'dimethylether'): 'Ethanol has O-H absorption (3400-3650 cm-1); dimethyl ether does not',
        ('hexane', '1-hexene'): '1-Hexene has C=C absorption (1640-1680 cm-1) and =C-H (3020-3100 cm-1); hexane does not',
        ('cyclohexane', '1-hexene'): '1-Hexene has C=C absorption (1640-1680 cm-1); cyclohexane does not',
        ('acetone', 'ethanol'): 'Acetone has C=O (1715 cm-1); ethanol has O-H (3400-3650 cm-1)',
        ('aldehyde', 'ketone'): 'Aldehydes show characteristic C-H stretch at 2720-2820 cm-1 in addition to C=O',
    }
    
    key = (compound1.lower(), compound2.lower())
    reverse_key = (compound2.lower(), compound1.lower())
    
    if key in distinguishing:
        return distinguishing[key]
    elif reverse_key in distinguishing:
        return distinguishing[reverse_key]
    else:
        return f"Compare functional group absorptions for {compound1} and {compound2}"


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "12-05",
        "question": "Identify functional group with strong absorption at 1715 cm-1",
        "wavenumber": 1715,
        "expected": "ketone"
    },
    {
        "id": "12-06",
        "question": "IR shows broad 3400 and strong 1050. What functional group?",
        "wavenumbers": [3400, 1050],
        "expected": "alcohol"
    },
    {
        "id": "12-07",
        "question": "Which IR region is 1715 cm-1 in?",
        "wavenumber": 1715,
        "expected": "double bond"
    },
    {
        "id": "12-08",
        "question": "Convert 1000 cm-1 to wavelength",
        "wavenumber": 1000,
        "expected_wavelength": 10.0
    },
]


if __name__ == "__main__":
    # Quick tests
    print("IR Spectroscopy Tools")
    print("=" * 40)
    
    # Test functional group identification
    groups = identify_functional_group(1715)
    print(f"1715 cm-1: {groups}")
    
    # Test region identification
    region = ir_region(1715)
    print(f"1715 cm-1 region: {region}")
    
    # Test carbonyl type
    ctype = carbonyl_type(1715)
    print(f"Carbonyl at 1715 cm-1: {ctype}")
    
    # Test wavelength conversion
    wl = wavenumber_to_wavelength(1000)
    print(f"1000 cm-1 = {wl} mum")

MCP_TOOLS = [
    {
        "name": "analyze_ir_spectrum",
        "description": "Comprehensive IR spectrum analysis.",
        "parameters": [
            {
                "name": "absorptions",
                "type": "number"
            }
        ]
    },
    {
        "name": "carbonyl_type",
        "description": "Identify type of carbonyl from C=O absorption.",
        "parameters": [
            {
                "name": "wavenumber",
                "type": "number"
            }
        ]
    },
    {
        "name": "distinguish_compounds",
        "description": "Explain how to distinguish two compounds by IR.",
        "parameters": [
            {
                "name": "compound1",
                "type": "number"
            },
            {
                "name": "compound2",
                "type": "number"
            },
            {
                "name": "key_difference",
                "type": "number"
            }
        ]
    },
    {
        "name": "has_carbonyl",
        "description": "Check if IR spectrum indicates carbonyl group.",
        "parameters": [
            {
                "name": "absorptions",
                "type": "number"
            }
        ]
    },
    {
        "name": "has_oh",
        "description": "Check if IR spectrum indicates O-H group.",
        "parameters": [
            {
                "name": "absorptions",
                "type": "number"
            }
        ]
    },
    {
        "name": "identify_functional_group",
        "description": "Identify possible functional groups from IR absorption.",
        "parameters": [
            {
                "name": "wavenumber",
                "type": "number"
            },
            {
                "name": "tolerance",
                "type": "number"
            }
        ]
    },
    {
        "name": "ir_region",
        "description": "Identify which IR region a wavenumber falls in.",
        "parameters": [
            {
                "name": "wavenumber",
                "type": "number"
            }
        ]
    },
    {
        "name": "wavelength_to_wavenumber",
        "description": "Convert wavelength (mum) to wavenumber (cm-1).",
        "parameters": [
            {
                "name": "wavelength",
                "type": "number"
            }
        ]
    },
    {
        "name": "wavenumber_to_wavelength",
        "description": "Convert wavenumber (cm-1) to wavelength (mum).",
        "parameters": [
            {
                "name": "wavenumber",
                "type": "number"
            }
        ]
    }
]
