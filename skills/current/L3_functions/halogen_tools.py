"""
L3 Tool: Halogen and Noble Gas Tools
Predict oxidizing power, interhalogen compounds, and noble gas compound formation.

Source: Petrucci General Chemistry, Ch22.2-22.3
Created: 2026-03-13
## Solver Instructions (for AI Agent)

When you encounter halogen or noble gas chemistry problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Compare oxidizing power? Use `oxidizing_power(element, phase)` - 'gas' or 'aqueous' (different rankings!)
- Predict interhalogen formula? Use `interhalogen_formula(halogen1, halogen2)` - heavier halogen is central
- Noble gas compounds? Use `forms_noble_gas_compound(element)` - He/Ne/Ar: no; Kr: KrF2; Xe: many
- Metal oxidation by halogens? Use `max_halogen_oxidation(metal, halogen)` - F gives highest OS
- Disproportionation? Use `halogen_disproportionates(element)` - F2 does NOT disproportionate

### Step 2: Handle special cases
- **Gas vs aqueous oxidizing power**: Gas: F2>Cl2>Br2>I2; Aqueous: Cl2>F2>Br2>I2 (hydration effects)
- **F2 exceptions**: Does NOT disproportionate in water (too electronegative); no oxyacids
- **Noble gas compounds**: Xe is most reactive noble gas (IE = 1170 kJ/mol); forms XeF2, XeF4, XeF6, XeO3, XeO4
- **Interhalogen rules**: Heavier halogen = central atom; max terminal atoms depend on size ratio

### Examples
```python
# Example 1: Interhalogen formula
interhalogen_formula('I', 'F')  # -> IF7 (I is central, F is terminal)
interhalogen_formula('Br', 'F')  # -> BrF5

# Example 2: Oxidizing power comparison
oxidizing_power('F', 'gas')  # -> rank 1 (strongest)
oxidizing_power('Cl', 'aqueous')  # -> rank 1 (aqueous: Cl > F)

# Example 3: Disproportionation
halogen_disproportionates('F')  # -> False
halogen_disproportionates('Cl')  # -> True
```
"""

# Halogen data
HALOGENS = {
    'F': {'atomic_num': 9, 'electronegativity': 4.0, 'bond_energy': 159, 'state': 'gas', 'ea': -328},
    'Cl': {'atomic_num': 17, 'electronegativity': 3.2, 'bond_energy': 244, 'state': 'gas', 'ea': -349},
    'Br': {'atomic_num': 35, 'electronegativity': 3.0, 'bond_energy': 193, 'state': 'liquid', 'ea': -325},
    'I': {'atomic_num': 53, 'electronegativity': 2.7, 'bond_energy': 151, 'state': 'solid', 'ea': -295},
    'At': {'atomic_num': 85, 'electronegativity': 2.2, 'bond_energy': 80, 'state': 'solid', 'ea': -270},
}

NOBLE_GASES = {
    'He': {'atomic_num': 2, 'ie': 2372, 'compounds': []},
    'Ne': {'atomic_num': 10, 'ie': 2081, 'compounds': []},
    'Ar': {'atomic_num': 18, 'ie': 1521, 'compounds': []},
    'Kr': {'atomic_num': 36, 'ie': 1351, 'compounds': ['KrF2']},
    'Xe': {'atomic_num': 54, 'ie': 1170, 'compounds': ['XeF2', 'XeF4', 'XeF6', 'XeO3', 'XeO4']},
    'Rn': {'atomic_num': 86, 'ie': 1037, 'compounds': ['RnF2']},
}

GOOD_LEAVING_GROUPS = ['I-', 'Br-', 'Cl-', 'TsO-', 'MsO-', 'TfO-', 'H2O', 'NH3', 'RS-', 'CN-', 'N3-']


def oxidizing_power(element: str, phase: str = 'gas') -> dict:
    """
    Compare oxidizing power of halogens.
    
    Gas phase: F2 > Cl2 > Br2 > I2
    Aqueous: Cl2 > F2 > Br2 > I2 (hydration effects)
    
    Args:
        element: Halogen symbol (F, Cl, Br, I)
        phase: 'gas' or 'aqueous'
    
    Returns:
        Dictionary with ranking
    
    Example:
        >>> oxidizing_power('F', 'gas')
        {'element': 'F', 'ranking': 1, 'phase': 'gas'}
    """
    element = element.capitalize()
    if element not in HALOGENS:
        return {'error': f'{element} not a halogen'}
    
    phase = phase.lower()
    if phase == 'gas':
        ranking = {'F': 1, 'Cl': 2, 'Br': 3, 'I': 4, 'At': 5}
        explanation = 'Gas phase: F2 > Cl2 > Br2 > I2 (oxidizing power)'
    else:  # aqueous
        ranking = {'Cl': 1, 'F': 2, 'Br': 3, 'I': 4, 'At': 5}
        explanation = 'Aqueous: Cl2 > F2 > Br2 > I2 (hydration energy effect)'
    
    return {
        'element': element,
        'ranking': ranking.get(element, 'unknown'),
        'phase': phase,
        'explanation': explanation
    }


def interhalogen_formula(halogen1: str, halogen2: str) -> dict:
    """
    Predict interhalogen compound formula.
    
    Rules:
    - Heavier halogen is central atom
    - Formula depends on size ratio
    - Examples: IF7, BrF5, ICl3
    
    Args:
        halogen1, halogen2: Halogen symbols
    
    Returns:
        Dictionary with predicted formula
    
    Example:
        >>> interhalogen_formula('I', 'F')
        {'formula': 'IF7', 'central': 'I'}
    """
    h1 = halogen1.capitalize()
    h2 = halogen2.capitalize()
    
    if h1 not in HALOGENS or h2 not in HALOGENS:
        return {'error': 'Both elements must be halogens'}
    
    # Determine central atom (heavier halogen)
    data1 = HALOGENS[h1]
    data2 = HALOGENS[h2]
    
    if data1['atomic_num'] > data2['atomic_num']:
        central = h1
        terminal = h2
    else:
        central = h2
        terminal = h1
    
    # Known interhalogen formulas
    # Maximum number of terminal atoms depends on central atom
    max_terminal = {
        'I': {'F': 7, 'Cl': 3, 'Br': 1},  # IF7, ICl3, IBr
        'Br': {'F': 5, 'Cl': 1},  # BrF5, BrCl
        'Cl': {'F': 3},  # ClF3
    }
    
    if central in max_terminal and terminal in max_terminal[central]:
        n_terminal = max_terminal[central][terminal]
        formula = f"{central}{terminal}{n_terminal}" if n_terminal > 1 else f"{central}{terminal}"
    else:
        # Simple 1:1 compound
        formula = f"{central}{terminal}"
    
    return {
        'formula': formula,
        'central': central,
        'terminal': terminal,
        'note': 'Heavier halogen is central atom'
    }


def forms_noble_gas_compound(element: str) -> dict:
    """
    Predict if noble gas forms stable compounds.
    
    He, Ne, Ar: No compounds (IE too high)
    Kr: KrF2 only
    Xe: XeF2, XeF4, XeF6, XeO3, XeO4
    Rn: RnF2 (predicted)
    
    Args:
        element: Noble gas symbol
    
    Returns:
        Dictionary with compound information
    
    Example:
        >>> forms_noble_gas_compound('Xe')
        {'forms_compounds': True, 'examples': ['XeF2', 'XeF4', 'XeF6']}
    """
    element = element.capitalize()
    if element not in NOBLE_GASES:
        return {'error': f'{element} not a noble gas'}
    
    data = NOBLE_GASES[element]
    compounds = data['compounds']
    
    return {
        'element': element,
        'forms_compounds': len(compounds) > 0,
        'ionization_energy': data['ie'],
        'examples': compounds if compounds else 'No stable compounds known',
        'reason': 'IE too high' if not compounds else 'IE low enough to form compounds'
    }


def max_halogen_oxidation(metal: str, halogen: str) -> dict:
    """
    Predict relative oxidation state of metal with halogen.
    
    Fluorine produces highest oxidation state.
    Iodine produces lowest oxidation state.
    
    Example: V + F2 -> VF5; V + I2 -> VI3
    
    Args:
        metal: Metal symbol
        halogen: Halogen symbol
    
    Returns:
        Dictionary with predicted oxidation tendency
    """
    halogen = halogen.capitalize()
    if halogen not in HALOGENS:
        return {'error': f'{halogen} not a halogen'}
    
    # Oxidizing power ranking (gas phase)
    oxidation_power = {'F': 'highest', 'Cl': 'high', 'Br': 'moderate', 'I': 'lowest'}
    
    # Relative oxidation state produced
    rel_ox = {'F': 'highest', 'Cl': 'high', 'Br': 'moderate', 'I': 'lowest'}
    
    return {
        'metal': metal,
        'halogen': halogen,
        'oxidizing_power': oxidation_power.get(halogen, 'unknown'),
        'metal_oxidation': rel_ox.get(halogen, 'unknown'),
        'note': 'F produces highest OS, I produces lowest'
    }


def halogen_disproportionates(element: str) -> dict:
    """
    Check if halogen disproportionates in water.
    
    F2 does NOT disproportionate (too electronegative).
    Cl2, Br2, I2 do: X2 + H2O -> HX + HOX
    
    Args:
        element: Halogen symbol
    
    Returns:
        Dictionary with disproportionation info
    """
    element = element.capitalize()
    if element not in HALOGENS:
        return {'error': f'{element} not a halogen'}
    
    if element == 'F':
        return {
            'element': element,
            'disproportionates': False,
            'reason': 'F2 too electronegative; does not form oxyacids'
        }
    else:
        return {
            'element': element,
            'disproportionates': True,
            'products': ['HX', 'HOX'],
            'equation': f'{element}2 + H2O -> H{element} + HO{element}'
        }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "22-01",
        "question": "Interhalogen formula for I and F",
        "halogen1": "I",
        "halogen2": "F",
        "expected_central": "I"
    },
    {
        "id": "22-02",
        "question": "Does Ar form compounds?",
        "element": "Ar",
        "expected": False
    },
    {
        "id": "22-03",
        "question": "Xe compounds",
        "element": "Xe",
        "expected": True
    },
    {
        "id": "22-04",
        "question": "F disproportionation",
        "element": "F",
        "expected_disproportionates": False
    },
    {
        "id": "22-05",
        "question": "Cl disproportionation",
        "element": "Cl",
        "expected_disproportionates": True
    },
]


if __name__ == "__main__":
    print("Halogen and Noble Gas Tools")
    print("=" * 40)
    
    # Test oxidizing power
    print("\nOxidizing Power:")
    for el in ['F', 'Cl', 'Br', 'I']:
        result = oxidizing_power(el, 'gas')
        print(f"  {el}: rank {result['ranking']} (gas)")
    
    # Test noble gas compounds
    print("\nNoble Gas Compounds:")
    for el in ['He', 'Ar', 'Kr', 'Xe']:
        result = forms_noble_gas_compound(el)
        print(f"  {el}: {result['examples']}")
    
    # Test interhalogens
    print("\nInterhalogens:")
    for pair in [('I', 'F'), ('Br', 'F'), ('I', 'Cl')]:
        result = interhalogen_formula(pair[0], pair[1])
        print(f"  {pair[0]}+{pair[1]}: {result['formula']} (central: {result['central']})")

MCP_TOOLS = [
    {
        "name": "forms_noble_gas_compound",
        "description": "Predict if noble gas forms stable compounds.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            }
        ]
    },
    {
        "name": "halogen_disproportionates",
        "description": "Check if halogen disproportionates in water.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            }
        ]
    },
    {
        "name": "interhalogen_formula",
        "description": "Predict interhalogen compound formula.",
        "parameters": [
            {
                "name": "halogen1",
                "type": "number"
            },
            {
                "name": "halogen2",
                "type": "number"
            }
        ]
    },
    {
        "name": "max_halogen_oxidation",
        "description": "Predict relative oxidation state of metal with halogen.",
        "parameters": [
            {
                "name": "metal",
                "type": "number"
            },
            {
                "name": "halogen",
                "type": "number"
            }
        ]
    },
    {
        "name": "oxidizing_power",
        "description": "Compare oxidizing power of halogens.",
        "parameters": [
            {
                "name": "element",
                "type": "string"
            },
            {
                "name": "phase",
                "type": "number"
            }
        ]
    }
]
