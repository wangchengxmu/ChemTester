"""
Process Safety Analysis - L3 Implementation

Safety analysis calculations for chemical processes.
Source: Foundations of Chemical and Biological Engineering I (Verret), Ch8

## Solver Instructions (for AI Agent)

When you encounter process safety analysis problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Risk score**: Given event frequency and consequence severity -> calculate risk
- **Risk matrix**: Given frequency category and severity category -> classify risk level
- **HAZOP**: Given process parameter and guide word -> generate deviation
- **LOPA**: Given initiating event frequency, IPL probabilities -> find mitigated frequency
- **Inerting**: Given oxygen concentration -> check if below LOC (limiting oxygen concentration)
- **Flammability**: Given fuel properties -> determine flammability limits, NFPA classification

### Step 2: Choose the correct function
- `risk_score(frequency, consequence)` -> Risk = Frequency x Consequence
- `risk_matrix_category(frequency, severity)` -> 'very low' to 'extreme' category
- `hazop_deviation(parameter, guide_word)` -> deviation description string
- `lopa_frequency(initiating_freq, ipl_pfds)` -> mitigated event frequency
- `check_inerting(o2_concentration, loc)` -> bool: safe or not
- `flammability_range(lel, uel, given_concentration)` -> is concentration flammable?

### Step 3: Handle special cases
- Risk matrix uses specific string categories: 'frequent'/'occasional'/'rare'/'remote' x 'minor'/'moderate'/'major'/'severe'
- LOPA: multiply IPL PFDs (probability of failure on demand); typical IPL PFD ~ 0.01-0.001
- LOC depends on fuel type (e.g., hydrocarbons ~10-12% O2)
- HAZOP guide words: 'no', 'more', 'less', 'reverse', 'other than'

### Examples
1. **Risk score**: Event occurs 0.01/yr, consequence = 2 fatalities
   -> `risk_score(0.01, 2)` -> 0.02 (fatality-equivalents per year)

2. **Risk matrix**: Occasional frequency, major severity
   -> `risk_matrix_category('occasional', 'major')` -> 'high'

3. **HAZOP**: Flow parameter, 'no' guide word
   -> `hazop_deviation('flow', 'no')` -> 'No flow' (possible causes: pump failure, valve closed, blockage)
"""

from typing import List, Tuple, Dict


def risk_score(frequency: float, consequence: float) -> float:
    """
    Calculate risk score.
    
    Risk = Frequency x Consequence
    
    Args:
        frequency: Frequency of event (per year)
        consequence: Consequence severity (deaths, injuries, or cost)
    
    Returns:
        Risk score
    """
    return frequency * consequence


def risk_matrix_category(frequency: str, severity: str) -> str:
    """
    Determine risk category from risk matrix.
    
    Args:
        frequency: One of 'frequent', 'occasional', 'rare', 'remote'
        severity: One of 'minor', 'moderate', 'major', 'severe'
    
    Returns:
        Risk category: 'very low', 'low', 'medium', 'high', 'extreme'
    """
    matrix = {
        ('frequent', 'minor'): 'medium',
        ('frequent', 'moderate'): 'high',
        ('frequent', 'major'): 'extreme',
        ('frequent', 'severe'): 'extreme',
        ('occasional', 'minor'): 'low',
        ('occasional', 'moderate'): 'medium',
        ('occasional', 'major'): 'high',
        ('occasional', 'severe'): 'extreme',
        ('rare', 'minor'): 'low',
        ('rare', 'moderate'): 'low',
        ('rare', 'major'): 'medium',
        ('rare', 'severe'): 'high',
        ('remote', 'minor'): 'very low',
        ('remote', 'moderate'): 'low',
        ('remote', 'major'): 'low',
        ('remote', 'severe'): 'medium',
    }
    
    return matrix.get((frequency, severity), 'unknown')


def hazop_deviation(parameter: str, guide_word: str) -> str:
    """
    Generate HAZOP deviation description.
    
    Args:
        parameter: Process parameter (flow, temperature, pressure, etc.)
        guide_word: HAZOP guide word (no, more, less, reverse, other)
    
    Returns:
        Deviation description
    """
    deviations = {
        ('flow', 'no'): 'No flow',
        ('flow', 'more'): 'Higher flow rate',
        ('flow', 'less'): 'Lower flow rate',
        ('flow', 'reverse'): 'Reverse flow direction',
        ('temperature', 'no'): 'No heating/cooling',
        ('temperature', 'more'): 'Higher temperature',
        ('temperature', 'less'): 'Lower temperature',
        ('pressure', 'more'): 'Higher pressure',
        ('pressure', 'less'): 'Lower pressure',
        ('level', 'no'): 'Empty tank',
        ('level', 'more'): 'Overflow',
        ('level', 'less'): 'Low level',
    }
    
    return deviations.get((parameter, guide_word), f'{guide_word} {parameter}')


def fault_tree_probability(and_gate: bool, probabilities: List[float]) -> float:
    """
    Calculate fault tree probability.
    
    AND gate: P = P1 x P2 x ... x Pn
    OR gate: P = 1 - (1-P1) x (1-P2) x ... x (1-Pn)
    
    Args:
        and_gate: True for AND gate, False for OR gate
        probabilities: List of basic event probabilities
    
    Returns:
        Gate probability
    """
    if and_gate:
        result = 1.0
        for p in probabilities:
            result *= p
        return result
    else:
        result = 1.0
        for p in probabilities:
            result *= (1 - p)
        return 1 - result


def layers_of_protection_analysis(initiating_freq: float, 
                                   ipls: List[float]) -> float:
    """
    Calculate mitigated frequency after IPLs.
    
    f_mitigated = f_initiating x (1 - IPL1) x (1 - IPL2) x ...
    
    Args:
        initiating_freq: Initiating event frequency
        ipls: List of IPL probability of failure on demand (PFD)
    
    Returns:
        Mitigated frequency
    """
    result = initiating_freq
    for pfd in ipls:
        result *= pfd
    return result


def safety_integrity_level(pfd: float) -> str:
    """
    Determine SIL level from PFD.
    
    Args:
        pfd: Probability of failure on demand
    
    Returns:
        SIL level (SIL 1-4) or 'Not rated'
    """
    if pfd >= 0.1:
        return 'Not rated'
    elif pfd >= 0.01:
        return 'SIL 1'
    elif pfd >= 0.001:
        return 'SIL 2'
    elif pfd >= 0.0001:
        return 'SIL 3'
    else:
        return 'SIL 4'


# TODO: Implement for Pass-3
# - event_tree_analysis() - Full ETA calculation
# - hazop_worksheet() - Generate HAZOP worksheet
# - consequence_modeling() - Dispersion, fire, explosion
