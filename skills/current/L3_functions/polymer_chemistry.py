"""
Polymer Chemistry - L3 Implementation

Polymerization kinetics and molecular weight calculations.
Source: Polymer Chemistry (Schaller), Ch3

## Solver Instructions (for AI Agent)

When you encounter polymer chemistry problems (degree of polymerization, molecular weight, kinetics), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given conversion -> calculate degree of polymerization (Carothers equation)?
- Given DP -> calculate required conversion?
- Given stoichiometric imbalance -> calculate DP?
- Given DP and monomer MW -> calculate Mn?
- Given Mw and Mn -> calculate PDI?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| DP from conversion | `carothers_dp(conversion)` | Xn = 1/(1-p) |
| Conversion from DP | `carothers_conversion(target_dp)` | p = 1 - 1/Xn |
| DP with imbalance | `stoichiometric_imbalance_dp(conversion, r_ratio)` | Xn = (1+r)/(1+r-2rp) |
| Number-average MW | `number_average_mw(dp, monomer_mw)` | Mn = Xn x M0 |
| Polydispersity index | `polydispersity_index(mw, mn)` | PDI = Mw/Mn |
| Flory weight fraction | `flory_weight_fraction(x, conversion)` | wx = x(1-p)2p^(x-1) |

### Step 3: Handle special cases
- Carothers equation: 99% conversion -> DP = 100
- Stoichiometric imbalance: r < 1 means one reagent in excess
- PDI: ideal step-growth = 2; chain-growth typically 1.1-2 for living polymerization
- Flory distribution: most probable for step-growth polymerization

### Examples
```python
# Example 1: DP from conversion
carothers_dp(0.99)  # 99% conversion
# -> 100

# Example 2: Required conversion for DP=200
carothers_conversion(200)
# -> 0.995 (99.5% conversion)

# Example 3: DP with stoichiometric imbalance
stoichiometric_imbalance_dp(0.99, 0.95)  # r=0.95 (5% imbalance)
# -> ~40 (limited by imbalance)

# Example 4: Polydispersity index
polydispersity_index(200000, 100000)
# -> 2.0
```
"""

from typing import Tuple
import math


def carothers_dp(conversion: float) -> float:
    """
    Calculate degree of polymerization from conversion (Carothers equation).
    
    Xn = 1 / (1 - p)
    
    Args:
        conversion: Fractional conversion (0 < p < 1)
    
    Returns:
        Number-average degree of polymerization
    """
    if conversion >= 1:
        return float('inf')
    return 1 / (1 - conversion)


def carothers_conversion(target_dp: float) -> float:
    """
    Calculate required conversion for target degree of polymerization.
    
    p = 1 - 1/Xn
    
    Args:
        target_dp: Target degree of polymerization
    
    Returns:
        Required fractional conversion
    """
    return 1 - 1 / target_dp


def stoichiometric_imbalance_dp(conversion: float, r_ratio: float) -> float:
    """
    Calculate DP with stoichiometric imbalance.
    
    Xn = (1 + r) / (1 + r - 2rp)
    
    Args:
        conversion: Fractional conversion
        r_ratio: Ratio of functional groups (r < 1)
    
    Returns:
        Degree of polymerization
    """
    return (1 + r_ratio) / (1 + r_ratio - 2 * r_ratio * conversion)


def number_average_mw(dp: float, monomer_mw: float) -> float:
    """
    Calculate number-average molecular weight.
    
    Mn = Xn * M0
    
    Args:
        dp: Degree of polymerization
        monomer_mw: Monomer molecular weight
    
    Returns:
        Number-average molecular weight
    """
    return dp * monomer_mw


def polydispersity_index(mw: float, mn: float) -> float:
    """
    Calculate polydispersity index.
    
    PDI = Mw / Mn
    
    Args:
        mw: Weight-average molecular weight
        mn: Number-average molecular weight
    
    Returns:
        Polydispersity index
    """
    return mw / mn


def flory_weight_fraction(x: int, conversion: float) -> float:
    """
    Calculate weight fraction for chains with x units (Flory distribution).
    
    wx = x * (1-p)2 * p^(x-1)
    
    Args:
        x: Number of monomer units
        conversion: Fractional conversion
    
    Returns:
        Weight fraction
    """
    return x * (1 - conversion)**2 * conversion**(x - 1)


def fox_equation_tg(w_a: float, tg_a: float, tg_b: float) -> float:
    """
    Calculate copolymer Tg using Fox equation.
    
    1/Tg = wA/TgA + wB/TgB
    
    Args:
        w_a: Weight fraction of monomer A
        tg_a: Tg of homopolymer A (Kelvin)
        tg_b: Tg of homopolymer B (Kelvin)
    
    Returns:
        Copolymer Tg in Kelvin
    """
    w_b = 1 - w_a
    inv_tg = w_a / tg_a + w_b / tg_b
    return 1 / inv_tg


def crystallinity_from_density(sample_density: float, 
                                amorphous_density: float,
                                crystalline_density: float) -> float:
    """
    Calculate percent crystallinity from density measurements.
    
    %Cryst = [(ρ - ρa) / (ρc - ρa)] x 100
    
    Args:
        sample_density: Measured sample density
        amorphous_density: Density of amorphous phase
        crystalline_density: Density of crystalline phase
    
    Returns:
        Percent crystallinity
    """
    return (sample_density - amorphous_density) / (crystalline_density - amorphous_density) * 100


def viscosity_mw_relation(molecular_weight: float, critical_mw: float, 
                          k_value: float = 1.0) -> float:
    """
    Calculate relative viscosity from molecular weight.
    
    η ∝ M^3.4 for M > Mc (entanglement regime)
    η ∝ M^1 for M < Mc
    
    Args:
        molecular_weight: Polymer molecular weight
        critical_mw: Critical MW for entanglement
        k_value: Proportionality constant
    
    Returns:
        Relative viscosity
    """
    if molecular_weight > critical_mw:
        return k_value * (molecular_weight / critical_mw)**3.4
    else:
        return k_value * (molecular_weight / critical_mw)


# TODO: Implement for Pass-3
# - chain_polymerization_kinetics() - Rate equations for chain polymerization
# - gpc_analysis() - Gel permeation chromatography data analysis
# - tg_from_structure() - Predict Tg from group contributions
