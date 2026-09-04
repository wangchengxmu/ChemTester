"""
Thermodynamic Potentials - L3 Implementation
Source: DeVoe Thermodynamics and Chemistry, Ch5.3
TRUE source extraction - equations from actual source text

Equations from source:
- Eq 5.3.1: H ≡ U + pV
- Eq 5.3.2: A ≡ U - TS
- Eq 5.3.3: G ≡ U - TS + pV = H - TS
- Eq 5.3.7: dH = đq (constant p, dw' = 0)
- Eq 5.3.9: dU = đq (constant V, dw' = 0)
"""

## Solver Instructions (for AI Agent)

# When you encounter **thermodynamic potentials** (U, H, A, G) and their relationships, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Calculate H from U, p, V: `calculate_enthalpy(U, p, V)`
# - Calculate Helmholtz A from U, T, S: `calculate_helmholtz(U, T, S)`
# - Calculate Gibbs G from H, T, S: `calculate_gibbs(H, T, S)` or from U directly: `calculate_gibbs_from_U(U, T, S, p, V)`
# - Total differentials: `total_differential_H(...)`, `total_differential_A(...)`, `total_differential_G(...)`
# - Spontaneity: `spontaneity_criterion_G(dG)`, `spontaneity_criterion_A(dA)`
# - Heat at constant p/V: `heat_at_constant_p(dH)`, `heat_at_constant_V(dU)`
# - Maxwell relations: `maxwell_relations()`

### Step 2: Choose the correct function
# - Direct potential calculation: use `calculate_enthalpy`, `calculate_helmholtz`, `calculate_gibbs`
# - Differential forms: use `total_differential_*` functions
# - Spontaneity check: use `spontaneity_criterion_G` or `spontaneity_criterion_A`

### Step 3: Handle special cases
# - G = H - TS is the most commonly used; use `calculate_gibbs`
# - Maxwell relations returns a dictionary of all four relations
# - Spontaneity: dG < 0 -> spontaneous at constant T, p; dA < 0 -> spontaneous at constant T, V

### Examples
# 1. U=100 J, p=1 atm, V=1 L: `calculate_enthalpy(100, 101325, 0.001)` -> H~201.13 J
# 2. G = H - TS where H=-100 kJ, T=298 K, S=200 J/K: `calculate_gibbs(-100000, 298, 200)` -> -159.6 kJ
# 3. dG < 0: `spontaneity_criterion_G(-5000)` -> "Spontaneous"



import math
from typing import Tuple, Dict, Optional

# Gas constant
R = 8.314462618  # J/(mol·K)


def calculate_enthalpy(U: float, p: float, V: float) -> float:
    """
    Calculate enthalpy from internal energy, pressure, volume.
    
    Source: DeVoe Eq 5.3.1: H ≡ U + pV
    
    Args:
        U: Internal energy (J)
        p: Pressure (Pa)
        V: Volume (m3)
    
    Returns:
        Enthalpy H (J)
    """
    return U + p * V


def calculate_helmholtz(U: float, T: float, S: float) -> float:
    """
    Calculate Helmholtz energy from internal energy, temperature, entropy.
    
    Source: DeVoe Eq 5.3.2: A ≡ U - TS
    
    Args:
        U: Internal energy (J)
        T: Temperature (K)
        S: Entropy (J/K)
    
    Returns:
        Helmholtz energy A (J)
    """
    return U - T * S


def calculate_gibbs(H: float, T: float, S: float) -> float:
    """
    Calculate Gibbs energy from enthalpy, temperature, entropy.
    
    Source: DeVoe Eq 5.3.3: G ≡ H - TS
    
    Args:
        H: Enthalpy (J)
        T: Temperature (K)
        S: Entropy (J/K)
    
    Returns:
        Gibbs energy G (J)
    """
    return H - T * S


def calculate_gibbs_from_U(U: float, T: float, S: float, p: float, V: float) -> float:
    """
    Calculate Gibbs energy from U, T, S, p, V.
    
    Source: DeVoe Eq 5.3.3: G = U - TS + pV
    
    Args:
        U: Internal energy (J)
        T: Temperature (K)
        S: Entropy (J/K)
        p: Pressure (Pa)
        V: Volume (m3)
    
    Returns:
        Gibbs energy G (J)
    """
    return U - T * S + p * V


def total_differential_H(dU: float, p: float, dV: float, V: float, dp: float) -> float:
    """
    Calculate total differential of enthalpy.
    
    Source: DeVoe Eq 5.3.4: dH = dU + pdV + Vdp
    
    Args:
        dU: Change in internal energy (J)
        p: Pressure (Pa)
        dV: Change in volume (m3)
        V: Volume (m3)
        dp: Change in pressure (Pa)
    
    Returns:
        Change in enthalpy dH (J)
    """
    return dU + p * dV + V * dp


def total_differential_A(dU: float, T: float, dS: float, S: float, dT: float) -> float:
    """
    Calculate total differential of Helmholtz energy.
    
    Source: DeVoe Eq 5.3.5: dA = dU - TdS - SdT
    
    Args:
        dU: Change in internal energy (J)
        T: Temperature (K)
        dS: Change in entropy (J/K)
        S: Entropy (J/K)
        dT: Change in temperature (K)
    
    Returns:
        Change in Helmholtz energy dA (J)
    """
    return dU - T * dS - S * dT


def total_differential_G(dU: float, T: float, dS: float, S: float, dT: float,
                         p: float, dV: float, V: float, dp: float) -> float:
    """
    Calculate total differential of Gibbs energy.
    
    Source: DeVoe Eq 5.3.6: dG = dU - TdS - SdT + pdV + Vdp
    
    Args:
        dU: Change in internal energy (J)
        T, dT: Temperature and its change (K)
        S, dS: Entropy and its change (J/K)
        p, dp: Pressure and its change (Pa)
        V, dV: Volume and its change (m3)
    
    Returns:
        Change in Gibbs energy dG (J)
    """
    return dU - T * dS - S * dT + p * dV + V * dp


def spontaneity_criterion_G(dG: float) -> str:
    """
    Determine spontaneity from Gibbs energy change.
    
    Source: DeVoe Ch5.8 - at constant T, p, with expansion work only:
    - dG < 0: spontaneous
    - dG = 0: equilibrium
    - dG > 0: non-spontaneous
    
    Args:
        dG: Change in Gibbs energy (J)
    
    Returns:
        String indicating spontaneity
    """
    if dG < 0:
        return "spontaneous"
    elif dG == 0:
        return "equilibrium"
    else:
        return "non-spontaneous"


def spontaneity_criterion_A(dA: float) -> str:
    """
    Determine spontaneity from Helmholtz energy change.
    
    Source: DeVoe Ch5.8 - at constant T, V, with expansion work only:
    - dA < 0: spontaneous
    - dA = 0: equilibrium
    - dA > 0: non-spontaneous
    
    Args:
        dA: Change in Helmholtz energy (J)
    
    Returns:
        String indicating spontaneity
    """
    if dA < 0:
        return "spontaneous"
    elif dA == 0:
        return "equilibrium"
    else:
        return "non-spontaneous"


def heat_at_constant_p(dH: float) -> float:
    """
    Calculate heat at constant pressure.
    
    Source: DeVoe Eq 5.3.7-5.3.8: dH = đq at constant p, dw' = 0
    
    Args:
        dH: Change in enthalpy (J)
    
    Returns:
        Heat q (J)
    """
    return dH


def heat_at_constant_V(dU: float) -> float:
    """
    Calculate heat at constant volume.
    
    Source: DeVoe Eq 5.3.9: dU = đq at constant V, dw' = 0
    
    Args:
        dU: Change in internal energy (J)
    
    Returns:
        Heat q (J)
    """
    return dU


def maxwell_relations() -> Dict[str, str]:
    """
    Return Maxwell relations from thermodynamic potentials.
    
    Source: DeVoe Ch5.3 - derived from exact differentials
    
    Returns:
        Dictionary of Maxwell relations
    """
    return {
        "from dU": "(∂T/∂V)_S = -(∂p/∂S)_V",
        "from dH": "(∂T/∂p)_S = (∂V/∂S)_p",
        "from dA": "(∂S/∂V)_T = (∂p/∂T)_V",
        "from dG": "(∂S/∂p)_T = -(∂V/∂T)_p"
    }


# ============ Unit Tests ============

if __name__ == "__main__":
    print("Testing thermodynamic_potentials.py...")
    
    # Test 1: Enthalpy
    H = calculate_enthalpy(1000, 101325, 0.001)
    expected_H = 1000 + 101.325
    assert abs(H - expected_H) < 0.1, f"H calculation failed: {H} vs {expected_H}"
    print(f"✓ H = U + pV: {H:.2f} J")
    
    # Test 2: Helmholtz
    A = calculate_helmholtz(1000, 298, 50)
    expected_A = 1000 - 14900
    assert abs(A - expected_A) < 1, f"A calculation failed: {A} vs {expected_A}"
    print(f"✓ A = U - TS: {A:.0f} J")
    
    # Test 3: Gibbs
    G = calculate_gibbs(1101.325, 298, 50)
    expected_G = 1101.325 - 14900
    assert abs(G - expected_G) < 1, f"G calculation failed: {G} vs {expected_G}"
    print(f"✓ G = H - TS: {G:.0f} J")
    
    # Test 4: Spontaneity
    assert spontaneity_criterion_G(-100) == "spontaneous"
    assert spontaneity_criterion_G(0) == "equilibrium"
    assert spontaneity_criterion_G(100) == "non-spontaneous"
    print("✓ Spontaneity criteria correct")
    
    # Test 5: Maxwell relations
    maxwell = maxwell_relations()
    assert len(maxwell) == 4
    print(f"✓ Maxwell relations: {len(maxwell)} relations")
    
    print("\nAll thermodynamic potential tests passed!")
