"""
L3 Tool: Lipid Chemistry Tools
Fatty acid analysis, saturation classification, melting point estimation.

Source: Human Biology (Wakim and Grewal), Ch3.6
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter lipid chemistry problems - fatty acid properties, saturation classification, melting point estimation, iodine value, or energy calculations - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a fatty acid notation (e.g., C18:1) -> name, properties, melting point?
- Given number of double bonds -> classify saturation level?
- Given chain length and unsaturation -> estimate melting point?
- Given iodine value -> interpret degree of unsaturation?
- Given fatty acid components -> calculate triglyceride energy?

### Step 2: Choose the correct function
- **Fatty acid info:** `fatty_acid_info(notation)` -> name, carbons, double_bonds, formula, mp, saturation_type. Accepts notation ('C18:1') or name ('Oleic')
- **Saturation classification:** `classify_saturation(n_double_bonds)` -> 0=saturated (solid RT), 1=monounsaturated (liquid RT), 2+=polyunsaturated (liquid cold)
- **Melting point estimate:** `melting_point_estimate(n_carbons, n_double_bonds)` -> estimated MP with state description. +4degC per carbon, -25degC per double bond
- **Iodine value interpretation:** `iodine_value_interpret(value)` -> <50 low unsaturation, 50-100 moderate, 100-150 high, >150 very high (drying oils)
- **Triglyceride energy:** `triglyceride_energy(fatty_acids)` -> energy density (~9 kcal/g), estimated MW. Pass list of fatty acid notations

### Step 3: Handle special cases
- Saturated fats (0 double bonds) are solid at room temp; more double bonds = lower MP
- Stearic acid (C18:0) MP=70degC; oleic acid (C18:1) MP=13degC - one double bond drops MP by 57degC!
- Iodine value measures grams of I2 absorbed per 100g fat - proxy for unsaturation
- All triglycerides have ~9 kcal/g regardless of saturation

### Examples
```python
# Example 1: What is C18:1?
fatty_acid_info('C18:1')  -> {'name': 'Oleic', 'carbons': 18, 'double_bonds': 1, 'mp': 13}

# Example 2: Classify fatty acid with 2 double bonds
classify_saturation(2)  -> 'polyunsaturated', 'Liquid at room temperature and when cold'

# Example 3: Estimate MP of C18:2
melting_point_estimate(18, 2)  -> {'estimated_mp': -5, 'state': 'liquid even when cold'}

# Example 4: Iodine value of 130
iodine_value_interpret(130)  -> 'high unsaturation' (e.g., soybean oil, sunflower oil)
```
"""

# Common fatty acids database
FATTY_ACIDS = {
    'C4:0': {'name': 'Butyric', 'carbons': 4, 'double_bonds': 0, 'formula': 'C4H8O2', 'mp': -8},
    'C6:0': {'name': 'Caproic', 'carbons': 6, 'double_bonds': 0, 'formula': 'C6H12O2', 'mp': -4},
    'C8:0': {'name': 'Caprylic', 'carbons': 8, 'double_bonds': 0, 'formula': 'C8H16O2', 'mp': 17},
    'C10:0': {'name': 'Capric', 'carbons': 10, 'double_bonds': 0, 'formula': 'C10H20O2', 'mp': 31},
    'C12:0': {'name': 'Lauric', 'carbons': 12, 'double_bonds': 0, 'formula': 'C12H24O2', 'mp': 44},
    'C14:0': {'name': 'Myristic', 'carbons': 14, 'double_bonds': 0, 'formula': 'C14H28O2', 'mp': 54},
    'C16:0': {'name': 'Palmitic', 'carbons': 16, 'double_bonds': 0, 'formula': 'C16H32O2', 'mp': 63},
    'C18:0': {'name': 'Stearic', 'carbons': 18, 'double_bonds': 0, 'formula': 'C18H36O2', 'mp': 70},
    'C20:0': {'name': 'Arachidic', 'carbons': 20, 'double_bonds': 0, 'formula': 'C20H40O2', 'mp': 76},
    'C18:1': {'name': 'Oleic', 'carbons': 18, 'double_bonds': 1, 'formula': 'C18H34O2', 'mp': 13},
    'C18:2': {'name': 'Linoleic', 'carbons': 18, 'double_bonds': 2, 'formula': 'C18H32O2', 'mp': -5},
    'C18:3': {'name': 'Linolenic', 'carbons': 18, 'double_bonds': 3, 'formula': 'C18H30O2', 'mp': -11},
    'C20:4': {'name': 'Arachidonic', 'carbons': 20, 'double_bonds': 4, 'formula': 'C20H32O2', 'mp': -50},
    'C22:1': {'name': 'Erucic', 'carbons': 22, 'double_bonds': 1, 'formula': 'C22H42O2', 'mp': 34},
}


def fatty_acid_info(notation: str) -> dict:
    """
    Get fatty acid properties by notation.
    
    Args:
        notation: Fatty acid notation (e.g., 'C18:1', 'oleic')
    
    Returns:
        Dictionary with fatty acid properties
    
    Example:
        >>> fatty_acid_info('C18:1')
        {'name': 'Oleic', 'carbons': 18, 'double_bonds': 1, ...}
    """
    notation = notation.upper()
    
    # Check if notation is in database
    if notation in FATTY_ACIDS:
        data = FATTY_ACIDS[notation].copy()
        data['notation'] = notation
        data['saturation_type'] = classify_saturation(data['double_bonds'])
        return data
    
    # Check by name
    for key, data in FATTY_ACIDS.items():
        if data['name'].upper() == notation:
            result = data.copy()
            result['notation'] = key
            result['saturation_type'] = classify_saturation(data['double_bonds'])
            return result
    
    return {'error': f'Unknown fatty acid: {notation}'}


def classify_saturation(n_double_bonds: int) -> dict:
    """
    Classify fatty acid by saturation level.
    
    Args:
        n_double_bonds: Number of double bonds
    
    Returns:
        Dictionary with classification
    
    Example:
        >>> classify_saturation(2)
        {'type': 'polyunsaturated', 'description': 'Liquid at room temp and when cold'}
    """
    if n_double_bonds == 0:
        sat_type = 'saturated'
        state = 'Solid at room temperature'
        mp_note = 'High melting point due to straight chains'
    elif n_double_bonds == 1:
        sat_type = 'monounsaturated'
        state = 'Liquid at room temperature'
        mp_note = 'Moderate melting point, solidifies when cold'
    else:
        sat_type = 'polyunsaturated'
        state = 'Liquid at room temperature and when cold'
        mp_note = 'Low melting point due to bent chains'
    
    return {
        'type': sat_type,
        'n_double_bonds': n_double_bonds,
        'state_at_room_temp': state,
        'melting_point_note': mp_note
    }


def melting_point_estimate(n_carbons: int, n_double_bonds: int) -> dict:
    """
    Estimate melting point based on chain length and unsaturation.
    
    Rules:
    - More carbons -> Higher MP
    - More double bonds -> Lower MP
    
    Args:
        n_carbons: Number of carbon atoms
        n_double_bonds: Number of double bonds
    
    Returns:
        Dictionary with estimated melting point
    
    Example:
        >>> melting_point_estimate(18, 0)
        {'estimated_mp': 70, 'range': '60-75degC'}
    """
    # Base MP for C18:0 (stearic acid) = 70degC
    # Each double bond reduces MP by ~20-25degC
    # Each carbon adds ~3-5degC
    
    base_mp = 70  # Stearic acid
    carbon_diff = n_carbons - 18
    mp = base_mp + carbon_diff * 4 - n_double_bonds * 25
    
    # Clamp to reasonable range
    mp = max(-60, min(90, mp))
    
    if mp > 40:
        state = 'solid at room temperature'
    elif mp > 0:
        state = 'liquid at room temperature, may solidify when cold'
    else:
        state = 'liquid even when cold'
    
    return {
        'estimated_mp': round(mp, 1),
        'state': state,
        'n_carbons': n_carbons,
        'n_double_bonds': n_double_bonds,
        'method': 'Approximate based on chain length and unsaturation'
    }


def iodine_value_interpret(value: float) -> dict:
    """
    Interpret iodine value for unsaturation.
    
    Iodine value = grams of I2 absorbed per 100g fat
    
    Args:
        value: Iodine value
    
    Returns:
        Dictionary with interpretation
    
    Example:
        >>> iodine_value_interpret(85)
        {'classification': 'monounsaturated', 'description': 'Moderate unsaturation'}
    """
    if value < 50:
        classification = 'low unsaturation'
        description = 'Predominantly saturated fats'
        examples = 'Butter, lard, coconut oil'
    elif value < 100:
        classification = 'moderate unsaturation'
        description = 'Mixture of mono- and polyunsaturated'
        examples = 'Olive oil, peanut oil'
    elif value < 150:
        classification = 'high unsaturation'
        description = 'Predominantly polyunsaturated'
        examples = 'Soybean oil, sunflower oil'
    else:
        classification = 'very high unsaturation'
        description = 'Highly polyunsaturated drying oils'
        examples = 'Linseed oil, tung oil'
    
    return {
        'iodine_value': value,
        'classification': classification,
        'description': description,
        'examples': examples
    }


def triglyceride_energy(fatty_acids: list) -> dict:
    """
    Calculate approximate energy content of a triglyceride.
    
    Triglycerides provide ~9 kcal/g
    
    Args:
        fatty_acids: List of fatty acid notations (e.g., ['C16:0', 'C18:1', 'C18:0'])
    
    Returns:
        Dictionary with energy calculation
    """
    total_carbons = 0
    total_hydrogens = 0
    
    for fa in fatty_acids:
        info = fatty_acid_info(fa)
        if 'error' not in info:
            total_carbons += info['carbons']
            total_hydrogens += info['carbons'] * 2 - info['double_bonds'] * 2
    
    # Approximate molecular weight
    glycerol_mw = 92  # C3H8O3
    fa_mw = total_carbons * 12 + total_hydrogens * 1 + (len(fatty_acids) * 2) * 16
    total_mw = glycerol_mw + fa_mw - 3 * 18  # Subtract 3 H2O
    
    # Energy calculation
    energy_per_mol = total_mw * 9  # kcal per gram
    energy_per_gram = 9  # kcal/g for triglycerides
    
    return {
        'fatty_acids': fatty_acids,
        'total_carbons': total_carbons,
        'estimated_mw': round(total_mw, 1),
        'energy_density': energy_per_gram,
        'unit': 'kcal/g',
        'note': 'Triglycerides contain >2x energy of carbohydrates (4 kcal/g)'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "LC-01",
        "question": "Double bond count",
        "notation": "C20:4",
        "expected_double_bonds": 4
    },
    {
        "id": "LC-02",
        "question": "Saturation classification",
        "n_double_bonds": 1,
        "expected_type": "monounsaturated"
    },
    {
        "id": "LC-03",
        "question": "Melting point comparison",
        "fa1": "C18:0",
        "fa2": "C18:1",
        "expected_higher": "C18:0"
    },
    {
        "id": "LC-04",
        "question": "Iodine value interpretation",
        "value": 130,
        "expected_class": "high unsaturation"
    },
    {
        "id": "LC-05",
        "question": "Energy density",
        "expected_energy": 9
    },
]


if __name__ == "__main__":
    print("Lipid Chemistry Tools")
    print("=" * 40)
    
    # Test fatty acid info
    print("\nFatty Acid Info:")
    for notation in ['C18:0', 'C18:1', 'C18:2', 'C20:4']:
        info = fatty_acid_info(notation)
        print(f"  {notation}: {info['name']}, MP={info['mp']}degC, {info['saturation_type']['type']}")
    
    # Test iodine value
    print("\nIodine Value Interpretation:")
    for value in [30, 80, 130, 180]:
        result = iodine_value_interpret(value)
        print(f"  IV={value}: {result['classification']}")

MCP_TOOLS = [
    {
        "name": "classify_saturation",
        "description": "Classify fatty acid by saturation level.",
        "parameters": [
            {
                "name": "n_double_bonds",
                "type": "number"
            }
        ]
    },
    {
        "name": "fatty_acid_info",
        "description": "Get fatty acid properties by notation.",
        "parameters": [
            {
                "name": "notation",
                "type": "number"
            }
        ]
    },
    {
        "name": "iodine_value_interpret",
        "description": "Interpret iodine value for unsaturation.",
        "parameters": [
            {
                "name": "value",
                "type": "number"
            }
        ]
    },
    {
        "name": "melting_point_estimate",
        "description": "Estimate melting point based on chain length and unsaturation.",
        "parameters": [
            {
                "name": "n_carbons",
                "type": "number"
            },
            {
                "name": "n_double_bonds",
                "type": "number"
            }
        ]
    },
    {
        "name": "triglyceride_energy",
        "description": "Calculate approximate energy content of a triglyceride.",
        "parameters": [
            {
                "name": "fatty_acids",
                "type": "number"
            }
        ]
    }
]
