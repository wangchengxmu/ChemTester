"""
Le Chatelier's Principle Tools - L3 Implementation
Chapter 13.3: Shifting Equilibria
## Solver Instructions (for AI Agent)

When you encounter Le Chatelier's principle problems (equilibrium shifts), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Concentration change? Use `predict_shift_concentration(stress_type, species, is_reactant)` - 'add' or 'remove'
- Pressure change? Use `predict_shift_pressure(delta_n, pressure_change)` - Deltan = gas products - gas reactants
- Temperature change? Use `predict_shift_temperature(delta_H, temp_change)` - DeltaH > 0 = endothermic
- Catalyst effect? Use `catalyst_effect()` - no shift, just faster equilibrium
- Volume change (gases)? Use `volume_change_moles(reactant_moles, product_moles, volume_change)`
- General stress? Use `apply_stress(K_initial, stress_dict)` or `summarize_le_chatelier()`

### Step 2: Handle special cases
- **Deltan = 0**: Pressure/volume changes have NO effect on equilibrium (e.g., H2 + Cl2 ⇌ 2HCl)
- **Temperature always changes K**: Concentration and pressure changes do NOT change K
- **Catalyst**: Does NOT shift equilibrium or change K - only speeds up attainment
- **Endothermic (DeltaH > 0)**: Heat acts as reactant; increasing T shifts right
- **Exothermic (DeltaH < 0)**: Heat acts as product; increasing T shifts left

### Examples
```python
# Example 1: Adding reactant
predict_shift_concentration('add', 'N2', True)  # -> 'right'
predict_shift_concentration('add', 'NH3', False)  # -> 'left'

# Example 2: Pressure increase with Deltan = -2
predict_shift_pressure(-2, 'increase')  # -> 'right' (toward fewer moles)

# Example 3: Temperature increase (exothermic)
predict_shift_temperature(-50000, 'increase')  # -> ('left', True) - K decreases
```
"""

from typing import Dict, List, Tuple, Optional


def predict_shift_concentration(stress_type: str, 
                                  species: str,
                                  is_reactant: bool) -> str:
    """
    Predict equilibrium shift from concentration change.
    
    Args:
        stress_type: 'add' or 'remove'
        species: Species being added/removed
        is_reactant: True if species is reactant
    
    Returns:
        Shift direction: 'right' or 'left'
    
    Examples:
        >>> predict_shift_concentration('add', 'N2', True)
        'right'
        >>> predict_shift_concentration('add', 'NH3', False)
        'left'
    """
    if stress_type == 'add':
        return 'right' if is_reactant else 'left'
    else:  # remove
        return 'left' if is_reactant else 'right'


def predict_shift_pressure(delta_n: int, pressure_change: str) -> str:
    """
    Predict equilibrium shift from pressure change.
    
    Args:
        delta_n: Moles gas products - moles gas reactants
        pressure_change: 'increase' or 'decrease'
    
    Returns:
        Shift direction or 'no change'
    
    Examples:
        >>> predict_shift_pressure(-2, 'increase')
        'right'
        >>> predict_shift_pressure(0, 'increase')
        'no change'
    """
    if delta_n == 0:
        return 'no change'
    
    if pressure_change == 'increase':
        # Shift toward fewer moles
        return 'right' if delta_n < 0 else 'left'
    else:  # decrease
        # Shift toward more moles
        return 'left' if delta_n < 0 else 'right'


def predict_shift_temperature(delta_H: float, 
                                temp_change: str) -> Tuple[str, bool]:
    """
    Predict equilibrium shift from temperature change.
    
    Args:
        delta_H: Enthalpy change (J/mol), positive = endothermic
        temp_change: 'increase' or 'decrease'
    
    Returns:
        (shift_direction, K_changes)
    
    Examples:
        >>> predict_shift_temperature(50000, 'increase')
        ('right', True)
        >>> predict_shift_temperature(-50000, 'increase')
        ('left', True)
    """
    is_endothermic = delta_H > 0
    K_changes = True  # Temperature always changes K
    
    if temp_change == 'increase':
        if is_endothermic:
            return ('right', K_changes)  # Heat is reactant, shifts right
        else:
            return ('left', K_changes)   # Heat is product, shifts left
    else:  # decrease
        if is_endothermic:
            return ('left', K_changes)   # Heat is reactant, removing shifts left
        else:
            return ('right', K_changes)  # Heat is product, removing shifts right


def apply_stress(K_initial: float, stress: Dict) -> Dict:
    """
    Apply stress and predict new equilibrium state.
    
    Args:
        K_initial: Initial equilibrium constant
        stress: Dict with 'type', 'change', and relevant parameters
    
    Returns:
        Dict with predicted shift and K change
    
    Examples:
        >>> apply_stress(10.0, {'type': 'concentration', 'change': 'add reactant'})
        {'shift': 'right', 'K_changes': False}
    """
    result = {'shift': None, 'K_changes': False}
    
    if stress['type'] == 'concentration':
        result['shift'] = 'right' if 'add reactant' in stress['change'] or 'remove product' in stress['change'] else 'left'
    
    elif stress['type'] == 'pressure':
        result['shift'] = 'toward fewer moles' if stress['change'] == 'increase' else 'toward more moles'
    
    elif stress['type'] == 'temperature':
        result['shift'] = 'depends on DeltaH'
        result['K_changes'] = True
    
    elif stress['type'] == 'catalyst':
        result['shift'] = 'no change'
        result['note'] = 'Catalyst only speeds equilibrium attainment'
    
    return result


def catalyst_effect() -> Dict:
    """
    Explain catalyst effect on equilibrium.
    
    Returns:
        Dict explaining catalyst behavior
    
    Examples:
        >>> catalyst_effect()['shifts_equilibrium']
        False
    """
    return {
        'shifts_equilibrium': False,
        'effect': 'Increases both forward and reverse rates equally',
        'result': 'Faster attainment of equilibrium',
        'K_unchanged': True,
        'composition_unchanged': True
    }


def volume_change_moles(reactant_moles: int, product_moles: int,
                        volume_change: str) -> str:
    """
    Predict shift from volume change for gas-phase equilibrium.
    
    Args:
        reactant_moles: Total moles of gaseous reactants
        product_moles: Total moles of gaseous products
        volume_change: 'increase' or 'decrease'
    
    Returns:
        Shift direction
    
    Examples:
        >>> volume_change_moles(2, 3, 'decrease')
        'left'
    """
    delta_n = product_moles - reactant_moles
    pressure_change = 'increase' if volume_change == 'decrease' else 'decrease'
    return predict_shift_pressure(delta_n, pressure_change)


def summarize_le_chatelier() -> Dict:
    """
    Return summary table of Le Chatelier's Principle.
    
    Returns:
        Dict with stress-response mapping
    """
    return {
        'concentration': {
            'Add reactant': 'Shifts right (-> products)',
            'Remove reactant': 'Shifts left (<- reactants)',
            'Add product': 'Shifts left (<- reactants)',
            'Remove product': 'Shifts right (-> products)'
        },
        'pressure': {
            'Increase (Deltan < 0)': 'Shifts right',
            'Increase (Deltan > 0)': 'Shifts left',
            'Increase (Deltan = 0)': 'No change',
            'Decrease': 'Opposite of increase'
        },
        'temperature': {
            'Increase (endothermic)': 'Shifts right, K increases',
            'Increase (exothermic)': 'Shifts left, K decreases',
            'Decrease': 'Opposite of increase'
        },
        'catalyst': {
            'Added': 'No shift, faster equilibrium'
        }
    }

MCP_TOOLS = [
    {
        "name": "apply_stress",
        "description": "Apply stress and predict new equilibrium state.",
        "parameters": [
            {
                "name": "K_initial",
                "type": "number"
            },
            {
                "name": "stress",
                "type": "number"
            }
        ]
    },
    {
        "name": "catalyst_effect",
        "description": "Explain catalyst effect on equilibrium.",
        "parameters": []
    },
    {
        "name": "predict_shift_concentration",
        "description": "Predict equilibrium shift from concentration change.",
        "parameters": [
            {
                "name": "stress_type",
                "type": "number"
            },
            {
                "name": "species",
                "type": "number"
            },
            {
                "name": "is_reactant",
                "type": "boolean"
            }
        ]
    },
    {
        "name": "predict_shift_pressure",
        "description": "Predict equilibrium shift from pressure change.",
        "parameters": [
            {
                "name": "delta_n",
                "type": "number"
            },
            {
                "name": "pressure_change",
                "type": "number"
            }
        ]
    },
    {
        "name": "predict_shift_temperature",
        "description": "Predict equilibrium shift from temperature change.",
        "parameters": [
            {
                "name": "delta_H",
                "type": "number"
            },
            {
                "name": "temp_change",
                "type": "number"
            }
        ]
    },
    {
        "name": "summarize_le_chatelier",
        "description": "Return summary table of Le Chatelier's Principle.",
        "parameters": []
    },
    {
        "name": "volume_change_moles",
        "description": "Predict shift from volume change for gas-phase equilibrium.",
        "parameters": [
            {
                "name": "reactant_moles",
                "type": "number"
            },
            {
                "name": "product_moles",
                "type": "number"
            },
            {
                "name": "volume_change",
                "type": "number"
            }
        ]
    }
]
