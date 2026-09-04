"""
Buffer Tools - L3 Implementation
Chapter 14.6: Buffers
"""
## Solver Instructions (for AI Agent)

from typing import Dict, Tuple, Optional
from math import log10

# When you encounter basic buffer problems (pH calculation, buffer selection, addition effects), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: pKa or Ka, acid/base concentrations, target pH, added acid/base moles
# - **Asked**: buffer pH, acid/base ratio, best acid selection, pH after addition

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Buffer pH (H-H) | `henderson_hasselbalch(pKa, base_conc, acid_conc)` | pKa, [base], [acid] |
# | pH from Ka | `buffer_pH_from_Ka(Ka, base_conc, acid_conc)` | Ka instead of pKa |
# | Buffer ratio | `buffer_ratio(pH, pKa)` | -> [base]/[acid] |
# | pH after addition | `buffer_after_addition(pKa, acid_mol, base_mol, added_acid, added_base, volume)` | moles |
# | Buffer capacity | `buffer_capacity(total_conc, ratio)` | C_total, ratio |
# | Optimal pH range | `optimal_buffer_pH(pKa)` | -> (pKa-1, pKa+1) |
# | Select best acid | `design_buffer(target_pH, Ka_values)` | {name: Ka} dict |

### Step 3: Handle special cases
# - pH = pKa when [acid] = [base]
# - Buffer exhausted -> function returns None when acid or base ≤ 0
# - `buffer_capacity` max at ratio=1, decreases symmetrically

### Examples
# 1. **Buffer pH**: `henderson_hasselbalch(4.74, 0.1, 0.1)` -> 4.74
# 2. **Ratio**: `buffer_ratio(5.74, 4.74)` -> 10.0
# 3. **After base**: `buffer_after_addition(4.74, 0.01, 0.01, added_base=0.001)` -> 4.79


from typing import Dict, Tuple, Optional
from math import log10


def henderson_hasselbalch(pKa: float, 
                          base_conc: float, 
                          acid_conc: float) -> Optional[float]:
    """
    Calculate buffer pH using Henderson-Hasselbalch equation.
    
    pH = pKa + log([base]/[acid])
    
    Handles edge cases:
    - If acid_conc is 0 or negative, returns None (buffer exhausted, strong base case)
    - If base_conc is 0 or negative, returns None (buffer exhausted, strong acid case)
    
    Args:
        pKa: Acid dissociation constant (as pKa)
        base_conc: Concentration of conjugate base (M)
        acid_conc: Concentration of weak acid (M)
    
    Returns:
        pH value, or None if buffer is exhausted
    
    Examples:
        >>> henderson_hasselbalch(4.74, 0.1, 0.1)
        4.74
        >>> henderson_hasselbalch(4.74, 0.2, 0.1)
        5.04
        >>> henderson_hasselbalch(4.74, 0, 0.1)  # Buffer exhausted
        None
    """
    if acid_conc <= 0:
        return None
    if base_conc <= 0:
        return None
    return pKa + log10(base_conc / acid_conc)


def buffer_after_addition(pKa: float, acid_mol: float, base_mol: float,
                           added_acid: float = 0, added_base: float = 0,
                           volume: float = 1.0,
                           strong_acid_pKa: Optional[float] = None) -> Optional[float]:
    """
    Calculate buffer pH after adding acid or base.
    
    Handles edge cases where buffer is exhausted:
    - If strong acid consumes all base, calculates pH from excess strong acid
    - If strong base consumes all acid, calculates pH from excess strong base
    
    Args:
        pKa: Acid pKa
        acid_mol: Initial moles of weak acid
        base_mol: Initial moles of conjugate base
        added_acid: Moles of strong acid added (e.g., HCl)
        added_base: Moles of strong base added (e.g., NaOH)
        volume: Total volume (L)
        strong_acid_pKa: pKa of strong acid (for edge case handling, optional)
    
    Returns:
        New pH, or None if calculation not possible
    
    Examples:
        >>> buffer_after_addition(4.74, 0.01, 0.01, added_base=0.001)
        4.79
        >>> # HCl consumes all acetate, leaves excess HCl
        >>> buffer_after_addition(4.74, 0.0, 0.001, added_acid=0.002, volume=0.2)
        2.30...
    """
    # Adding strong base: base increases, acid decreases
    # Adding strong acid: acid increases, base decreases
    
    new_acid = acid_mol + added_acid - added_base
    new_base = base_mol + added_base - added_acid
    
    # Case 1: Buffer still intact
    if new_acid > 0 and new_base > 0:
        new_acid_conc = new_acid / volume
        new_base_conc = new_base / volume
        return henderson_hasselbalch(pKa, new_base_conc, new_acid_conc)
    
    # Case 2: Strong acid added in excess - all base consumed
    if new_base <= 0 < new_acid:
        # Excess strong acid
        excess_H = abs(new_base) + new_acid  # Total H+ from strong acid
        H_conc = excess_H / volume
        if H_conc > 0:
            return -log10(H_conc)
    
    # Case 3: Strong base added in excess - all acid consumed
    if new_acid <= 0 < new_base:
        # Excess strong base
        excess_OH = abs(new_acid) + new_base  # Total OH- from strong base
        OH_conc = excess_OH / volume
        if OH_conc > 0:
            pOH = -log10(OH_conc)
            return 14.0 - pOH
    
    # Case 4: Both consumed (shouldn't happen normally)
    return None


def buffer_pH_from_Ka(Ka: float, base_conc: float, 
                       acid_conc: float) -> float:
    """
    Calculate buffer pH from Ka instead of pKa.
    
    Args:
        Ka: Acid dissociation constant
        base_conc: Concentration of conjugate base (M)
        acid_conc: Concentration of weak acid (M)
    
    Returns:
        pH value
    
    Examples:
        >>> buffer_pH_from_Ka(1.8e-5, 0.1, 0.1)
        4.74
    """
    pKa = -log10(Ka)
    return henderson_hasselbalch(pKa, base_conc, acid_conc)


def buffer_ratio(pH: float, pKa: float) -> float:
    """
    Calculate [base]/[acid] ratio from pH and pKa.
    
    Args:
        pH: Buffer pH
        pKa: Acid pKa
    
    Returns:
        Base/acid ratio
    
    Examples:
        >>> buffer_ratio(4.74, 4.74)
        1.0
        >>> buffer_ratio(5.74, 4.74)
        10.0
    """
    return 10 ** (pH - pKa)


def buffer_capacity(total_conc: float, ratio: float = 1.0) -> float:
    """
    Estimate buffer capacity.
    
    Maximum capacity when ratio = 1 (equal acid and base).
    
    Args:
        total_conc: [acid] + [base]
        ratio: [base]/[acid] ratio
    
    Returns:
        Relative buffer capacity
    
    Examples:
        >>> buffer_capacity(0.2, 1.0)
        0.05
    """
    # Capacity proportional to total concentration
    # And maximum when ratio = 1
    efficiency = 4 * ratio / (1 + ratio) ** 2  # Max = 1 at ratio = 1
    return total_conc * efficiency / 4


def optimal_buffer_pH(pKa: float) -> Tuple[float, float]:
    """
    Return optimal buffer range.
    
    Effective range is pKa ± 1
    
    Args:
        pKa: Acid pKa
    
    Returns:
        (min_pH, max_pH) tuple
    
    Examples:
        >>> optimal_buffer_pH(4.74)
        (3.74, 5.74)
    """
    return (pKa - 1, pKa + 1)


def design_buffer(target_pH: float, Ka_values: Dict[str, float]) -> str:
    """
    Select best acid for buffer at target pH.
    
    Args:
        target_pH: Desired buffer pH
        Ka_values: Dict of {acid_name: Ka}
    
    Returns:
        Best acid name
    
    Examples:
        >>> design_buffer(4.7, {'acetic': 1.8e-5, 'formic': 1.8e-4})
        'acetic'
    """
    best_acid = None
    min_diff = float('inf')
    
    for name, Ka in Ka_values.items():
        pKa = -log10(Ka)
        diff = abs(pKa - target_pH)
        if diff < min_diff:
            min_diff = diff
            best_acid = name
    
    return best_acid


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'buffer_after_addition', 'description': 'Calculate buffer pH after adding acid or base.\n\nArgs:\n    pKa: Acid pKa\n    acid_mol: Initial moles of weak acid\n    base_mol: Initial moles of conjugate base\n    added_acid: Moles of strong acid added\n    added_base: Moles of strong base added\n    volume: Total volume (L)\n\nReturns:\n    New pH\n\nExamples:\n    >>> buffer_after_addition(4.74, 0.01, 0.01, added_base=0.001)\n    4.79', 'inputSchema': {'type': 'object', 'properties': {'pKa': {'type': 'number', 'description': 'Pka'}, 'acid_mol': {'type': 'string', 'description': 'Acid Mol'}, 'base_mol': {'type': 'number', 'description': 'Base Mol'}, 'added_acid': {'type': 'string', 'description': 'Added Acid', 'default': 0}, 'added_base': {'type': 'number', 'description': 'Added Base', 'default': 0}, 'volume': {'type': 'number', 'description': 'Volume', 'default': 1.0}}, 'required': ['pKa', 'acid_mol', 'base_mol']}},
    {'name': 'buffer_capacity', 'description': 'Estimate buffer capacity.\n\nMaximum capacity when ratio = 1 (equal acid and base).\n\nArgs:\n    total_conc: [acid] + [base]\n    ratio: [base]/[acid] ratio\n\nReturns:\n    Relative buffer capacity\n\nExamples:\n    >>> buffer_capacity(0.2, 1.0)\n    0.05', 'inputSchema': {'type': 'object', 'properties': {'total_conc': {'type': 'number', 'description': 'Total Conc'}, 'ratio': {'type': 'number', 'description': 'Ratio', 'default': 1.0}}, 'required': ['total_conc']}},
    {'name': 'buffer_pH_from_Ka', 'description': 'Calculate buffer pH from Ka instead of pKa.\n\nArgs:\n    Ka: Acid dissociation constant\n    base_conc: Concentration of conjugate base (M)\n    acid_conc: Concentration of weak acid (M)\n\nReturns:\n    pH value\n\nExamples:\n    >>> buffer_pH_from_Ka(1.8e-5, 0.1, 0.1)\n    4.74', 'inputSchema': {'type': 'object', 'properties': {'Ka': {'type': 'number', 'description': 'Ka'}, 'base_conc': {'type': 'number', 'description': 'Base Conc'}, 'acid_conc': {'type': 'string', 'description': 'Acid Conc'}}, 'required': ['Ka', 'base_conc', 'acid_conc']}},
    {'name': 'buffer_ratio', 'description': 'Calculate [base]/[acid] ratio from pH and pKa.\n\nArgs:\n    pH: Buffer pH\n    pKa: Acid pKa\n\nReturns:\n    Base/acid ratio\n\nExamples:\n    >>> buffer_ratio(4.74, 4.74)\n    1.0\n    >>> buffer_ratio(5.74, 4.74)\n    10.0', 'inputSchema': {'type': 'object', 'properties': {'pH': {'type': 'number', 'description': 'Ph'}, 'pKa': {'type': 'number', 'description': 'Pka'}}, 'required': ['pH', 'pKa']}},
    {'name': 'design_buffer', 'description': "Select best acid for buffer at target pH.\n\nArgs:\n    target_pH: Desired buffer pH\n    Ka_values: Dict of {acid_name: Ka}\n\nReturns:\n    Best acid name\n\nExamples:\n    >>> design_buffer(4.7, {'acetic': 1.8e-5, 'formic': 1.8e-4})\n    'acetic'", 'inputSchema': {'type': 'object', 'properties': {'target_pH': {'type': 'string', 'description': 'Target Ph'}, 'Ka_values': {'type': 'number', 'description': 'Ka Values'}}, 'required': ['target_pH', 'Ka_values']}},
    {'name': 'henderson_hasselbalch', 'description': 'Calculate buffer pH using Henderson-Hasselbalch equation.\n\npH = pKa + log([base]/[acid])\n\nArgs:\n    pKa: Acid dissociation constant (as pKa)\n    base_conc: Concentration of conjugate base (M)\n    acid_conc: Concentration of weak acid (M)\n\nReturns:\n    pH value\n\nExamples:\n    >>> henderson_hasselbalch(4.74, 0.1, 0.1)\n    4.74\n    >>> henderson_hasselbalch(4.74, 0.2, 0.1)\n    5.04', 'inputSchema': {'type': 'object', 'properties': {'pKa': {'type': 'number', 'description': 'Pka'}, 'base_conc': {'type': 'number', 'description': 'Base Conc'}, 'acid_conc': {'type': 'string', 'description': 'Acid Conc'}}, 'required': ['pKa', 'base_conc', 'acid_conc']}},
    {'name': 'optimal_buffer_pH', 'description': 'Return optimal buffer range.\n\nEffective range is pKa ± 1\n\nArgs:\n    pKa: Acid pKa\n\nReturns:\n    (min_pH, max_pH) tuple\n\nExamples:\n    >>> optimal_buffer_pH(4.74)\n    (3.74, 5.74)', 'inputSchema': {'type': 'object', 'properties': {'pKa': {'type': 'number', 'description': 'Pka'}}, 'required': ['pKa']}}
]
