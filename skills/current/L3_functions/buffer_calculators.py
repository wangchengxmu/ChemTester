"""
Buffer calculators (L3 implementation)

Scope: textbook-level design/calculation helpers.
Assumptions: ideal concentration-based behavior unless noted.

## Solver Instructions (for AI Agent)

When you encounter buffer solution design and calculation problems:

### Step 1: Identify what is given and what is asked
- Given: target pH, pKa, concentrations, or amount of strong acid/base added
- Asked: buffer pH, required concentrations/ratio, buffer capacity, pH after perturbation

### Step 2: Choose the correct function
- `hh_pH(pKa, base_conc, acid_conc)`: Henderson-Hasselbalch: pH = pKa + log([A-]/[HA])
- `required_ratio_for_target_pH(pKa, target_pH)`: [base]/[acid] ratio needed
- `pair_match_score(pKa, target_pH)`: How well a pair matches target pH
- `perturbation_estimate(pKa, acid_mol, base_mol, added_mol, is_acid)`: pH after adding strong acid/base

### Step 3: Handle special cases
- Effective buffer range: pKa ± 1
- Best buffer at [base]=[acid]: pH = pKa
- Higher total concentration -> greater buffer capacity

### Examples
```python
hh_pH(4.74, 0.2, 0.1)  # acetate -> 5.04
required_ratio_for_target_pH(4.74, 5.0)  # -> ~1.82
```
"""

from __future__ import annotations
import math


def hh_pH(pKa: float, base_conc: float, acid_conc: float) -> float:
    """Henderson-Hasselbalch pH estimate."""
    if base_conc <= 0 or acid_conc <= 0:
        raise ValueError("base_conc and acid_conc must be > 0")
    return pKa + math.log10(base_conc / acid_conc)


def required_ratio_for_target_pH(pKa: float, target_pH: float) -> float:
    """Return required [base]/[acid] ratio."""
    return 10 ** (target_pH - pKa)


def pair_match_score(pKa: float, target_pH: float) -> dict:
    """Simple suitability score by distance to pKa."""
    delta = abs(target_pH - pKa)
    if delta <= 0.5:
        label = "excellent"
    elif delta <= 1.0:
        label = "good"
    elif delta <= 1.5:
        label = "marginal"
    else:
        label = "poor"
    return {"delta_pH": delta, "rating": label}


def perturbation_estimate(
    pKa: float,
    acid_moles: float,
    base_moles: float,
    added_strong_acid_moles: float = 0.0,
    added_strong_base_moles: float = 0.0,
) -> float:
    """
    Estimate new pH after small strong acid/base addition.
    Stoichiometric pre-adjustment then HH estimate.
    """
    a = acid_moles + added_strong_acid_moles - added_strong_base_moles
    b = base_moles + added_strong_base_moles - added_strong_acid_moles
    if a <= 0 or b <= 0:
        raise ValueError("Perturbation too large for HH regime.")
    return hh_pH(pKa, b, a)


if __name__ == "__main__":
    # quick smoke demo
    print("ratio@pH7.4,pKa7.2=", required_ratio_for_target_pH(7.2, 7.4))
    print("pH=", hh_pH(7.2, 0.03, 0.02))
    print("match=", pair_match_score(7.2, 7.4))
