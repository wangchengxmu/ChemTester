"""
L3 Tool: Main Group Chemistry Tools (Groups 13-16)
Predict oxidation states, bonding patterns, and compound properties.

Source: Petrucci General Chemistry, Ch21-22
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter main group element problems (Groups 13-16), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given element symbol -> predict oxidation states, oxide type, or inert-pair effect?
- Given group number -> predict trends (catenation, bonding)?
- Comparing elements -> predict relative properties?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Predict oxidation state | `predict_oxidation_state(element, group=None)` | element symbol (e.g., 'Tl', 'Pb', 'Bi') |
| Predict oxide type | `predict_oxide_type(element)` | Returns: acidic/basic/amphoteric |
| Check inert-pair effect | `inert_pair_effect(element)` | Tl, Pb, Bi, Po affected |
| Catenation trend | `catenation_trend(group)` | group=14 or 16 |

### Step 3: Handle special cases
- **Inert-pair effect**: Heavy p-block elements (Tl, Pb, Bi, Po) prefer lower oxidation states
- **Oxide trends**: Nonmetal oxides = acidic, metal oxides = basic, diagonal = amphoteric
- **Catenation**: C > Si > Ge > Sn > Pb (decreases down group)

### Examples
```python
# Example 1: Tl oxidation state (inert-pair effect)
predict_oxidation_state('Tl')
# -> {'preferred': 1, 'possible': [1, 3], 'reason': 'inert-pair effect'}

# Example 2: Al2O3 oxide type
predict_oxide_type('Al')
# -> {'type': 'amphoteric', 'formula': 'Al2O3'}

# Example 3: Catenation in Group 14
catenation_trend(14)
# -> {'elements': ['C', 'Si', 'Ge', 'Sn', 'Pb'], 'trend': 'decreasing', 'best_catenator': 'C'}
```
"""

# Group data
GROUP_13 = {
    'B': {'oxidations': [3], 'preferred': 3, 'type': 'nonmetal', 'ie1': 801, 'chi': 2.0},
    'Al': {'oxidations': [3], 'preferred': 3, 'type': 'metal', 'ie1': 578, 'chi': 1.6},
    'Ga': {'oxidations': [3], 'preferred': 3, 'type': 'metal', 'ie1': 579, 'chi': 1.8},
    'In': {'oxidations': [3], 'preferred': 3, 'type': 'metal', 'ie1': 558, 'chi': 1.8},
    'Tl': {'oxidations': [1, 3], 'preferred': 1, 'type': 'metal', 'ie1': 589, 'chi': 1.8, 'inert_pair': True},
}

GROUP_14 = {
    'C': {'oxidations': [-4, 2, 4], 'preferred': 4, 'type': 'nonmetal', 'ie1': 1087, 'chi': 2.6},
    'Si': {'oxidations': [4], 'preferred': 4, 'type': 'metalloid', 'ie1': 787, 'chi': 1.9},
    'Ge': {'oxidations': [4], 'preferred': 4, 'type': 'metalloid', 'ie1': 762, 'chi': 2.0},
    'Sn': {'oxidations': [2, 4], 'preferred': 4, 'type': 'metal', 'ie1': 709, 'chi': 2.0},
    'Pb': {'oxidations': [2, 4], 'preferred': 2, 'type': 'metal', 'ie1': 716, 'chi': 1.8, 'inert_pair': True},
}

GROUP_15 = {
    'N': {'oxidations': [-3, 1, 2, 3, 4, 5], 'preferred': None, 'type': 'nonmetal', 'ie1': 1402, 'chi': 3.0},
    'P': {'oxidations': [-3, 3, 5], 'preferred': 5, 'type': 'nonmetal', 'ie1': 1012, 'chi': 2.1},
    'As': {'oxidations': [-3, 3, 5], 'preferred': 5, 'type': 'metalloid', 'ie1': 947, 'chi': 2.0},
    'Sb': {'oxidations': [3, 5], 'preferred': 5, 'type': 'metalloid', 'ie1': 834, 'chi': 1.9},
    'Bi': {'oxidations': [3, 5], 'preferred': 3, 'type': 'metal', 'ie1': 703, 'chi': 1.9, 'inert_pair': True},
}

GROUP_16 = {
    'O': {'oxidations': [-2, -1], 'preferred': -2, 'type': 'nonmetal', 'ie1': 1314, 'chi': 3.5},
    'S': {'oxidations': [-2, 2, 4, 6], 'preferred': 6, 'type': 'nonmetal', 'ie1': 1000, 'chi': 2.5},
    'Se': {'oxidations': [-2, 2, 4, 6], 'preferred': 6, 'type': 'metalloid', 'ie1': 941, 'chi': 2.4},
    'Te': {'oxidations': [2, 4, 6], 'preferred': 6, 'type': 'metalloid', 'ie1': 869, 'chi': 2.1},
    'Po': {'oxidations': [2, 4], 'preferred': 4, 'type': 'metal', 'ie1': 812, 'chi': 2.0, 'inert_pair': True},
}

ALL_ELEMENTS = {}
ALL_ELEMENTS.update(GROUP_13)
ALL_ELEMENTS.update(GROUP_14)
ALL_ELEMENTS.update(GROUP_15)
ALL_ELEMENTS.update(GROUP_16)

OXIDE_TYPES = {
    'B': 'acidic',
    'Al': 'amphoteric',
    'Ga': 'amphoteric',
    'In': 'amphoteric',
    'Tl': 'basic',
    'C': 'acidic',
    'Si': 'amphoteric',
    'Ge': 'amphoteric',
    'Sn': 'amphoteric',
    'Pb': 'basic',
    'N': 'acidic',
    'P': 'acidic',
    'As': 'amphoteric',
    'Sb': 'amphoteric',
    'Bi': 'basic',
    'O': 'none',
    'S': 'acidic',
    'Se': 'acidic',
    'Te': 'amphoteric',
    'Po': 'basic',
}


def predict_oxidation_state(element: str, group: int = None) -> dict:
    """
    Predict preferred oxidation state for main-group elements.
    
    Group 13: +3 (Tl prefers +1 due to inert-pair effect)
    Group 14: +4 (Pb prefers +2)
    Group 15: +5, +3 (Bi prefers +3)
    Group 16: +6, +4, -2 (heavier prefer +4)
    
    Args:
        element: Element symbol or name
        group: Group number (13-16), optional
    
    Returns:
        Dictionary with oxidation states
    
    Example:
        >>> predict_oxidation_state('Tl')
        {'preferred': 1, 'possible': [1, 3], 'reason': 'inert-pair effect'}
    """
    element = element.capitalize()
    if element not in ALL_ELEMENTS:
        return {'error': f'Element {element} not in Groups 13-16'}
    
    data = ALL_ELEMENTS[element]
    result = {
        'element': element,
        'possible': data['oxidations'],
        'preferred': data.get('preferred'),
    }
    
    if data.get('inert_pair'):
        result['reason'] = 'inert-pair effect'
    else:
        result['reason'] = 'standard group behavior'
    
    return result


def predict_oxide_type(element: str) -> dict:
    """
    Predict whether element oxide is acidic, basic, or amphoteric.
    
    Rules:
    - Nonmetal oxides: Acidic
    - Metal oxides: Basic
    - Near diagonal: Amphoteric
    
    Args:
        element: Element symbol
    
    Returns:
        Dictionary with oxide classification
    
    Example:
        >>> predict_oxide_type('Al')
        {'type': 'amphoteric', 'examples': ['Al2O3']}
    """
    element = element.capitalize()
    if element not in OXIDE_TYPES:
        return {'error': f'Element {element} not in Groups 13-16'}
    
    oxide_type = OXIDE_TYPES[element]
    element_data = ALL_ELEMENTS.get(element, {})
    
    # Generate common oxide formula
    if element == 'B':
        formula = 'B2O3'
    elif element == 'Al':
        formula = 'Al2O3'
    elif element == 'C':
        formula = 'CO2'
    elif element == 'Si':
        formula = 'SiO2'
    elif element == 'N':
        formula = 'N2O5'
    elif element == 'P':
        formula = 'P4O10'
    elif element == 'S':
        formula = 'SO3'
    elif element in ['O', 'Po']:
        formula = 'N/A'
    else:
        formula = f'{element}O2'
    
    return {
        'element': element,
        'type': oxide_type,
        'formula': formula,
        'element_type': element_data.get('type', 'unknown')
    }


def inert_pair_effect(element: str) -> dict:
    """
    Determine if element shows inert-pair effect.
    
    Elements affected: Tl, Pb, Bi, Po
    Heavy p-block elements where s2 electrons don't participate.
    
    Args:
        element: Element symbol
    
    Returns:
        Dictionary with inert-pair analysis
    
    Example:
        >>> inert_pair_effect('Tl')
        {'affected': True, 'lower_oxidation': 1, 'higher_oxidation': 3}
    """
    element = element.capitalize()
    if element not in ALL_ELEMENTS:
        return {'error': f'Element {element} not in Groups 13-16'}
    
    data = ALL_ELEMENTS[element]
    affected = data.get('inert_pair', False)
    
    if affected:
        # Determine lower and higher oxidation states
        ox_states = sorted(data['oxidations'])
        return {
            'element': element,
            'affected': True,
            'lower_oxidation': ox_states[0],
            'higher_oxidation': ox_states[-1],
            'reason': '6s2 electrons are inert due to relativistic effects'
        }
    else:
        return {
            'element': element,
            'affected': False,
            'note': 'No inert-pair effect for this element'
        }


def catenation_trend(group: int) -> dict:
    """
    Predict catenation ability down a group.
    
    Catenation decreases down group due to weaker E-E bonds.
    Carbon is best (356 kJ/mol C-C).
    
    Args:
        group: Group number (14 or 16)
    
    Returns:
        Dictionary with catenation trend
    
    Example:
        >>> catenation_trend(14)
        {'elements': ['C', 'Si', 'Ge', 'Sn', 'Pb'], 'trend': 'decreasing'}
    """
    if group == 14:
        elements = ['C', 'Si', 'Ge', 'Sn', 'Pb']
        bond_energies = {'C-C': 356, 'Si-Si': 222, 'Ge-Ge': 188, 'Sn-Sn': 146}
    elif group == 16:
        elements = ['O', 'S', 'Se', 'Te', 'Po']
        bond_energies = {'O-O': 142, 'S-S': 226, 'Se-Se': 172}
    else:
        return {'error': 'Catenation trend only for Groups 14 and 16'}
    
    return {
        'group': group,
        'elements': elements,
        'trend': 'decreasing',
        'bond_energies': bond_energies,
        'best_catenator': elements[0]
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "21-01",
        "question": "Oxidation state of Tl",
        "element": "Tl",
        "expected_preferred": 1
    },
    {
        "id": "21-02",
        "question": "Oxidation state of Pb",
        "element": "Pb",
        "expected_preferred": 2
    },
    {
        "id": "21-03",
        "question": "Oxidation state of Bi",
        "element": "Bi",
        "expected_preferred": 3
    },
    {
        "id": "22-01",
        "question": "Oxide type for Al2O3",
        "element": "Al",
        "expected_type": "amphoteric"
    },
    {
        "id": "22-02",
        "question": "Oxide type for PbO",
        "element": "Pb",
        "expected_type": "basic"
    },
]


if __name__ == "__main__":
    print("Main Group Chemistry Tools")
    print("=" * 40)
    
    # Test oxidation states
    print("\nOxidation State Predictions:")
    for el in ['B', 'Al', 'Tl', 'C', 'Pb', 'N', 'Bi', 'S']:
        result = predict_oxidation_state(el)
        print(f"  {el}: {result['possible']}, preferred: {result['preferred']}")
    
    # Test inert-pair
    print("\nInert-Pair Effect:")
    for el in ['Tl', 'Pb', 'Bi', 'Po', 'Al', 'C']:
        result = inert_pair_effect(el)
        print(f"  {el}: {result}")

MCP_TOOLS = [
    {
        "name": "catenation_trend",
        "description": "Predict catenation ability down a group.",
        "parameters": [
            {
                "name": "group",
                "type": "number"
            }
        ]
    },
    {
        "name": "inert_pair_effect",
        "description": "Determine if element shows inert-pair effect.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            }
        ]
    },
    {
        "name": "predict_oxidation_state",
        "description": "Predict preferred oxidation state for main-group elements.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            },
            {
                "name": "group",
                "type": "number"
            }
        ]
    },
    {
        "name": "predict_oxide_type",
        "description": "Predict whether element oxide is acidic, basic, or amphoteric.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            }
        ]
    }
]
