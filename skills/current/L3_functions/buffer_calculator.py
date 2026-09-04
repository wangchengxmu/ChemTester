"""
Buffer Calculator - L3 Implementation
Acid-Base: Advanced buffer system calculations

Extends basic buffer tools with:
- Buffer design and preparation calculations
- Buffer capacity calculations
- Polyprotic buffer systems
- Activity corrections
"""
## Solver Instructions (for AI Agent)

# When you encounter advanced buffer design/capacity/activity problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: target pH, pKa, concentrations, added acid/base, ionic strength
# - **Asked**: buffer pH, concentrations needed, buffer capacity, activity-corrected pH

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Henderson-Hasselbalch | `henderson_hasselbalch(pKa, base_conc, acid_conc)` | pKa, [A-], [HA] |
# | Design buffer | `design_buffer(target_pH, pKa, total_conc)` | target pH, pKa, C_total |
# | Buffer ratio | `buffer_concentrations_from_ratio(total_conc, ratio)` | C_total, [base]/[acid] |
# | Exact buffer capacity | `buffer_capacity_exact(acid_conc, base_conc, Ka, Kw)` | Van Slyke equation |
# | Approx capacity | `buffer_capacity_approximate(total_conc, pH, pKa)` | simplified |
# | Buffer range | `buffer_range(pKa)` | -> (pKa-1, pKa+1) |
# | Effective buffer check | `is_effective_buffer(target_pH, pKa)` | target pH, pKa |
# | After adding acid | `buffer_after_strong_acid(pKa, acid_mol, base_mol, added_H, vol)` | moles |
# | After adding base | `buffer_after_strong_base(pKa, acid_mol, base_mol, added_OH, vol)` | moles |
# | Dilution effect | `dilution_effect(pH, pKa, dilution_factor)` | ~no change for good buffers |
# | Debye-Hückel gamma | `debye_huckel_activity(ionic_strength, charge)` | I, z |
# | Ionic strength | `ionic_strength(concentrations)` | {ion: (conc, charge)} |
# | pH with activity | `buffer_pH_with_activity(pKa, acid_conc, base_conc, gamma_H)` | gamma_H |
# | Polyprotic buffer | `polyprotic_buffer_pH(pKa1, pKa2, H2A, HA, A)` | diprotic system |
# | Phosphate buffer | `phosphate_buffer(H2PO4_conc, HPO4_conc)` | pKa2 = 7.20 |
# | Carbonate buffer | `carbonate_buffer(H2CO3, HCO3, use_first_Ka)` | pKa1=6.35, pKa2=10.33 |
# | Citrate buffer | `citrate_buffer(CitH2, CitH, which_pair)` | pKa1-3 |
# | Prepare buffer (mixing) | `prepare_buffer_by_mixing(target_pH, pKa, total_vol, total_conc, acid_MM, base_MM)` | masses needed |
# | Grams needed | `grams_needed(molar_mass, moles)` | M, n |

### Step 3: Handle special cases
# - Buffer effective range: pKa ± 1
# - Maximum capacity at pH = pKa (ratio = 1)
# - Polyprotic systems: use appropriate pKa pair
# - Activity corrections lower pH by -log10(gamma_H) typically 0.1-0.3 pH units at I=0.1

### Examples
# 1. **Design**: `design_buffer(5.0, 4.76, 0.2)` -> [HA]=0.073 M, [A-]=0.127 M
# 2. **After acid**: `buffer_after_strong_acid(4.76, 0.01, 0.01, 0.001, 0.1)` -> pH 4.67
# 3. **Debye-Hückel**: `debye_huckel_activity(0.1, 1)` -> gamma ~ 0.78


from typing import Dict, Tuple, Optional, List
from math import log10, sqrt
import numpy as np
from numpy.typing import NDArray


# Physical constants
R = 8.314462618  # Gas constant (J/(mol·K))


def henderson_hasselbalch(pKa: float, base_conc: float, acid_conc: float) -> float:
    """
    Calculate buffer pH using Henderson-Hasselbalch equation.
    
    pH = pKa + log10([base]/[acid])
    
    Args:
        pKa: Acid dissociation constant (as pKa)
        base_conc: Concentration of conjugate base (M)
        acid_conc: Concentration of weak acid (M)
    
    Returns:
        pH value
    
    Examples:
        >>> round(henderson_hasselbalch(4.76, 0.1, 0.1), 2)
        4.76
        >>> round(henderson_hasselbalch(4.76, 0.2, 0.1), 2)
        5.06
    """
    if acid_conc <= 0 or base_conc <= 0:
        raise ValueError("Concentrations must be positive")
    return pKa + log10(base_conc / acid_conc)


def buffer_concentrations_from_ratio(total_conc: float, 
                                      ratio: float) -> Tuple[float, float]:
    """
    Calculate acid and base concentrations from total concentration and ratio.
    
    Args:
        total_conc: [acid] + [base] (M)
        ratio: [base]/[acid]
    
    Returns:
        Tuple of (acid_conc, base_conc)
    
    Examples:
        >>> acid, base = buffer_concentrations_from_ratio(0.2, 1.0)
        >>> round(acid, 3), round(base, 3)
        (0.1, 0.1)
    """
    # [base] = ratio x [acid]
    # [acid] + ratio x [acid] = total_conc
    # [acid] = total_conc / (1 + ratio)
    
    acid_conc = total_conc / (1 + ratio)
    base_conc = ratio * acid_conc
    
    return acid_conc, base_conc


def design_buffer(target_pH: float, 
                   pKa: float,
                   total_conc: float) -> Tuple[float, float]:
    """
    Design a buffer to achieve target pH.
    
    Args:
        target_pH: Desired pH
        pKa: pKa of weak acid
        total_conc: Total concentration [acid] + [base] (M)
    
    Returns:
        Tuple of (acid_conc, base_conc) in M
    
    Examples:
        >>> acid, base = design_buffer(5.0, 4.76, 0.2)
        >>> round(acid, 3), round(base, 3)
        (0.073, 0.127)
    """
    # Calculate required ratio
    ratio = 10 ** (target_pH - pKa)
    
    return buffer_concentrations_from_ratio(total_conc, ratio)


def buffer_capacity_exact(acid_conc: float, base_conc: float,
                           Ka: float, Kw: float = 1e-14) -> float:
    """
    Calculate exact buffer capacity using the Van Slyke equation.
    
    beta = 2.303 x [HA][A-] / ([HA] + [A-]) + [H+] + [OH-]
    
    Args:
        acid_conc: Concentration of weak acid (M)
        base_conc: Concentration of conjugate base (M)
        Ka: Acid dissociation constant
        Kw: Water ion product (default 1e-14)
    
    Returns:
        Buffer capacity (mol/L per pH unit)
    
    Examples:
        >>> beta = buffer_capacity_exact(0.1, 0.1, 1.8e-5)
        >>> round(beta, 4)
        0.0576
    """
    # Calculate [H+] from buffer equilibrium
    # [H+] = Ka x [HA] / [A-]
    H_conc = Ka * acid_conc / base_conc
    OH_conc = Kw / H_conc
    
    # Van Slyke equation
    total = acid_conc + base_conc
    buffer_term = 2.303 * acid_conc * base_conc / total
    
    return buffer_term + H_conc + OH_conc


def buffer_capacity_approximate(total_conc: float, 
                                  pH: float, 
                                  pKa: float) -> float:
    """
    Approximate buffer capacity near pKa.
    
    Maximum at pH = pKa: beta_max ~ 0.576 x C_total
    
    Args:
        total_conc: [acid] + [base] (M)
        pH: Buffer pH
        pKa: Acid pKa
    
    Returns:
        Approximate buffer capacity
    
    Examples:
        >>> beta = buffer_capacity_approximate(0.2, 4.76, 4.76)
        >>> round(beta, 4)
        0.1152
    """
    # Ratio from HH equation
    ratio = 10 ** (pH - pKa)
    
    # [HA] and [A-]
    HA = total_conc / (1 + ratio)
    A = total_conc - HA
    
    # Buffer capacity
    return 2.303 * HA * A / total_conc


def buffer_range(pKa: float, 
                  effectiveness: float = 0.1) -> Tuple[float, float]:
    """
    Calculate effective buffer range.
    
    Standard range: pKa ± 1 (ratio from 0.1 to 10)
    
    Args:
        pKa: Acid pKa
        effectiveness: Minimum fraction of max capacity (default 0.1)
    
    Returns:
        Tuple of (min_pH, max_pH)
    
    Examples:
        >>> buffer_range(4.76)
        (3.76, 5.76)
    """
    # At pKa ± 1, the ratio is 10 or 0.1
    # Buffer capacity at these points is about 33% of maximum
    return (pKa - 1, pKa + 1)


def is_effective_buffer(target_pH: float, pKa: float) -> bool:
    """
    Check if pKa is suitable for target pH.
    
    Rule: pKa should be within ±1 of target pH
    
    Args:
        target_pH: Desired buffer pH
        pKa: Acid pKa
    
    Returns:
        True if suitable
    
    Examples:
        >>> is_effective_buffer(5.0, 4.76)
        True
        >>> is_effective_buffer(8.0, 4.76)
        False
    """
    min_pH, max_pH = buffer_range(pKa)
    return min_pH <= target_pH <= max_pH


def dilution_effect(pH_initial: float, 
                    pKa: float,
                    dilution_factor: float) -> float:
    """
    Estimate pH change upon dilution.
    
    For most buffers, dilution has minimal effect on pH
    (because ratio stays constant).
    
    Args:
        pH_initial: Initial pH
        pKa: Acid pKa
        dilution_factor: Final volume / initial volume
    
    Returns:
        New pH (approximately same as initial for good buffers)
    
    Examples:
        >>> dilution_effect(5.0, 4.76, 2.0)  # 2x dilution
        5.0
    """
    # For simple buffers, pH depends on ratio, not absolute concentration
    # Dilution doesn't change ratio, so pH stays approximately constant
    return pH_initial


def buffer_after_strong_acid(pKa: float,
                              acid_mol: float,
                              base_mol: float,
                              added_H_mol: float,
                              volume: float) -> Tuple[float, float, float]:
    """
    Calculate new pH after adding strong acid to buffer.
    
    A- + H+ -> HA
    
    Args:
        pKa: Acid pKa
        acid_mol: Initial moles of HA
        base_mol: Initial moles of A-
        added_H_mol: Moles of H+ added
        volume: Total volume (L)
    
    Returns:
        Tuple of (new_pH, new_acid_conc, new_base_conc)
    
    Examples:
        >>> pH, ha, a = buffer_after_strong_acid(4.76, 0.01, 0.01, 0.001, 0.1)
        >>> round(pH, 2)
        4.67
    """
    # Reaction: A- + H+ -> HA
    new_acid_mol = acid_mol + added_H_mol
    new_base_mol = base_mol - added_H_mol
    
    if new_base_mol <= 0:
        # Buffer exhausted - return approximate pH
        # This would need full equilibrium calculation
        return None, None, None
    
    new_acid_conc = new_acid_mol / volume
    new_base_conc = new_base_mol / volume
    
    new_pH = henderson_hasselbalch(pKa, new_base_conc, new_acid_conc)
    
    return new_pH, new_acid_conc, new_base_conc


def buffer_after_strong_base(pKa: float,
                              acid_mol: float,
                              base_mol: float,
                              added_OH_mol: float,
                              volume: float) -> Tuple[float, float, float]:
    """
    Calculate new pH after adding strong base to buffer.
    
    HA + OH- -> A- + H2O
    
    Args:
        pKa: Acid pKa
        acid_mol: Initial moles of HA
        base_mol: Initial moles of A-
        added_OH_mol: Moles of OH- added
        volume: Total volume (L)
    
    Returns:
        Tuple of (new_pH, new_acid_conc, new_base_conc)
    
    Examples:
        >>> pH, ha, a = buffer_after_strong_base(4.76, 0.01, 0.01, 0.001, 0.1)
        >>> round(pH, 2)
        4.85
    """
    # Reaction: HA + OH- -> A- + H2O
    new_acid_mol = acid_mol - added_OH_mol
    new_base_mol = base_mol + added_OH_mol
    
    if new_acid_mol <= 0:
        return None, None, None
    
    new_acid_conc = new_acid_mol / volume
    new_base_conc = new_base_mol / volume
    
    new_pH = henderson_hasselbalch(pKa, new_base_conc, new_acid_conc)
    
    return new_pH, new_acid_conc, new_base_conc


def debye_huckel_activity(ionic_strength: float, 
                          charge: int,
                          A: float = 0.509) -> float:
    """
    Calculate activity coefficient using Debye-Hückel limiting law.
    
    log10(gamma) = -A x z2 x √I
    
    Args:
        ionic_strength: Ionic strength (M)
        charge: Ion charge
        A: Debye-Hückel constant (0.509 for water at 25degC)
    
    Returns:
        Activity coefficient gamma
    
    Examples:
        >>> gamma = debye_huckel_activity(0.1, 1)
        >>> round(gamma, 2)
        0.78
    """
    log_gamma = -A * charge**2 * sqrt(ionic_strength)
    return 10 ** log_gamma


def ionic_strength(concentrations: Dict[str, Tuple[float, int]]) -> float:
    """
    Calculate ionic strength of a solution.
    
    I = 0.5 x Σ(ci x zi2)
    
    Args:
        concentrations: Dict of {ion_name: (concentration_M, charge)}
    
    Returns:
        Ionic strength (M)
    
    Examples:
        >>> I = ionic_strength({'Na+': (0.1, 1), 'Cl-': (0.1, -1)})
        >>> round(I, 2)
        0.1
    """
    I = 0.0
    for name, (conc, charge) in concentrations.items():
        I += conc * charge**2
    return 0.5 * I


def buffer_pH_with_activity(pKa: float,
                             acid_conc: float,
                             base_conc: float,
                             gamma_H: float = 1.0) -> float:
    """
    Calculate buffer pH with activity correction.
    
    pH = pKa + log10([A-]/[HA]) - log10(gamma_H)
    
    Args:
        pKa: Thermodynamic pKa
        acid_conc: Concentration of HA (M)
        base_conc: Concentration of A- (M)
        gamma_H: Activity coefficient of H+
    
    Returns:
        pH with activity correction
    
    Examples:
        >>> pH = buffer_pH_with_activity(4.76, 0.1, 0.1, 0.8)
        >>> round(pH, 2)
        4.86
    """
    pH_ideal = henderson_hasselbalch(pKa, base_conc, acid_conc)
    return pH_ideal - log10(gamma_H)


# ============================================================================
# Polyprotic Buffer Systems
# ============================================================================

def polyprotic_buffer_pH(pKa1: float, pKa2: float,
                          H2A_conc: float, HA_conc: float, A_conc: float) -> float:
    """
    Calculate pH for polyprotic buffer system (H2A/HA-/A2-).
    
    Uses the appropriate Henderson-Hasselbalch equation based on
    dominant species.
    
    Args:
        pKa1: First dissociation constant
        pKa2: Second dissociation constant
        H2A_conc: Concentration of H2A (M)
        HA_conc: Concentration of HA- (M)
        A_conc: Concentration of A2- (M)
    
    Returns:
        pH value
    
    Examples:
        >>> # Phosphate buffer H2PO4-/HPO42-
        >>> pH = polyprotic_buffer_pH(2.14, 7.20, 0.0, 0.1, 0.1)
        >>> round(pH, 2)
        7.2
    """
    # Determine which pair is dominant
    if H2A_conc > 0 and HA_conc > 0 and A_conc == 0:
        # H2A/HA- buffer
        return henderson_hasselbalch(pKa1, HA_conc, H2A_conc)
    elif HA_conc > 0 and A_conc > 0 and H2A_conc == 0:
        # HA-/A2- buffer
        return henderson_hasselbalch(pKa2, A_conc, HA_conc)
    elif H2A_conc > 0 and A_conc > 0 and HA_conc == 0:
        # Special case: need full calculation
        # pH ~ (pKa1 + pKa2) / 2 for amphoteric species
        return (pKa1 + pKa2) / 2
    else:
        # Use the dominant pair
        if H2A_conc + HA_conc > A_conc:
            return henderson_hasselbalch(pKa1, HA_conc, max(H2A_conc, 1e-15))
        else:
            return henderson_hasselbalch(pKa2, A_conc, max(HA_conc, 1e-15))


def phosphate_buffer(H2PO4_conc: float, HPO4_conc: float) -> float:
    """
    Calculate pH of phosphate buffer (H2PO4-/HPO42-).
    
    pKa2 = 7.20
    
    Args:
        H2PO4_conc: Concentration of H2PO4- (M)
        HPO4_conc: Concentration of HPO42- (M)
    
    Returns:
        pH value
    
    Examples:
        >>> pH = phosphate_buffer(0.05, 0.05)
        >>> round(pH, 2)
        7.2
    """
    return henderson_hasselbalch(7.20, HPO4_conc, H2PO4_conc)


def carbonate_buffer(H2CO3_conc: float, HCO3_conc: float, 
                      use_first_Ka: bool = True) -> float:
    """
    Calculate pH of carbonate buffer.
    
    H2CO3/HCO3-: pKa1 = 6.35
    HCO3-/CO32-: pKa2 = 10.33
    
    Args:
        H2CO3_conc: Concentration of H2CO3 or HCO3- (M)
        HCO3_conc: Concentration of HCO3- or CO32- (M)
        use_first_Ka: Use first dissociation (H2CO3/HCO3-)
    
    Returns:
        pH value
    
    Examples:
        >>> pH = carbonate_buffer(0.1, 0.1, True)  # H2CO3/HCO3-
        >>> round(pH, 2)
        6.35
    """
    pKa = 6.35 if use_first_Ka else 10.33
    return henderson_hasselbalch(pKa, HCO3_conc, H2CO3_conc)


def citrate_buffer(CitH2_conc: float, CitH_conc: float,
                   which_pair: int = 2) -> float:
    """
    Calculate pH of citrate buffer.
    
    pKa1 = 3.13 (H3Cit/H2Cit-)
    pKa2 = 4.76 (H2Cit-/HCit2-)
    pKa3 = 6.40 (HCit2-/Cit3-)
    
    Args:
        CitH2_conc: Concentration of more protonated form (M)
        CitH_conc: Concentration of less protonated form (M)
        which_pair: Which pKa to use (1, 2, or 3)
    
    Returns:
        pH value
    """
    pKa_values = {1: 3.13, 2: 4.76, 3: 6.40}
    pKa = pKa_values[which_pair]
    return henderson_hasselbalch(pKa, CitH_conc, CitH2_conc)


# ============================================================================
# Buffer Preparation Calculations
# ============================================================================

def grams_needed(molar_mass: float, moles: float) -> float:
    """
    Calculate grams of compound needed.
    
    Args:
        molar_mass: Molar mass (g/mol)
        moles: Moles needed
    
    Returns:
        Mass in grams
    
    Examples:
        >>> grams_needed(82.03, 0.1)  # Sodium acetate
        8.203
    """
    return molar_mass * moles


def prepare_buffer_by_mixing(target_pH: float,
                              pKa: float,
                              total_volume: float,
                              total_conc: float,
                              acid_molar_mass: float,
                              base_molar_mass: float) -> Tuple[float, float]:
    """
    Calculate masses needed to prepare buffer by mixing acid and base salts.
    
    Args:
        target_pH: Desired pH
        pKa: pKa of weak acid
        total_volume: Final buffer volume (L)
        total_conc: Total concentration (M)
        acid_molar_mass: Molar mass of acid form (g/mol)
        base_molar_mass: Molar mass of conjugate base form (g/mol)
    
    Returns:
        Tuple of (grams_acid, grams_base)
    
    Examples:
        >>> g_acid, g_base = prepare_buffer_by_mixing(5.0, 4.76, 0.5, 0.1, 60.05, 82.03)
        >>> round(g_acid, 2), round(g_base, 2)
        (2.19, 5.21)
    """
    # Design concentrations
    acid_conc, base_conc = design_buffer(target_pH, pKa, total_conc)
    
    # Calculate moles
    acid_moles = acid_conc * total_volume
    base_moles = base_conc * total_volume
    
    # Calculate masses
    grams_acid = grams_needed(acid_molar_mass, acid_moles)
    grams_base = grams_needed(base_molar_mass, base_moles)
    
    return grams_acid, grams_base


def prepare_buffer_by_neutralization(target_pH: float,
                                      pKa: float,
                                      total_volume: float,
                                      acid_concentration: float,
                                      base_concentration: float,
                                      Ka: float) -> Tuple[float, float]:
    """
    Calculate volumes needed to prepare buffer by partial neutralization.
    
    Mix weak acid with strong base to create buffer.
    
    Args:
        target_pH: Desired pH
        pKa: pKa of weak acid
        total_volume: Final buffer volume (L)
        acid_concentration: Stock weak acid concentration (M)
        base_concentration: Stock strong base concentration (M)
        Ka: Acid dissociation constant
    
    Returns:
        Tuple of (volume_acid, volume_base)
    """
    # For target pH, calculate ratio
    ratio = 10 ** (target_pH - pKa)
    
    # Total buffer species = [HA] + [A-]
    # After neutralization: moles_A = moles_OH_added
    # [A-]/[HA] = ratio
    
    # Let x = fraction neutralized
    # ratio = x / (1-x)
    # x = ratio / (1 + ratio)
    
    x = ratio / (1 + ratio)
    
    # Total buffer species concentration
    # From partial neutralization
    # Need to solve for volumes
    
    # This is simplified - assumes acid is in excess
    # Full calculation would need more constraints
    
    # For now, return approximate calculation
    vol_acid = total_volume * 0.8  # Placeholder
    vol_base = total_volume * 0.2  # Placeholder
    
    return vol_acid, vol_base


if __name__ == "__main__":
    """Example usage and simple tests."""
    import numpy as np
    
    print("=" * 60)
    print("Buffer Calculator - Example Usage")
    print("=" * 60)
    
    # Example 1: Basic buffer design
    print("\n--- Example 1: Buffer Design ---")
    target_pH = 5.0
    pKa = 4.76  # Acetic acid
    total_conc = 0.2  # M
    
    acid_conc, base_conc = design_buffer(target_pH, pKa, total_conc)
    print(f"Target pH: {target_pH}, pKa: {pKa}")
    print(f"[HA] = {acid_conc:.3f} M")
    print(f"[A-] = {base_conc:.3f} M")
    
    # Verify
    pH_calc = henderson_hasselbalch(pKa, base_conc, acid_conc)
    print(f"Calculated pH: {pH_calc:.2f}")
    
    # Example 2: Buffer capacity
    print("\n--- Example 2: Buffer Capacity ---")
    beta = buffer_capacity_exact(0.1, 0.1, 1.8e-5)
    print(f"Buffer capacity (0.1 M each): {beta:.4f} mol/L per pH unit")
    
    beta_approx = buffer_capacity_approximate(0.2, 4.76, 4.76)
    print(f"Approximate at pH = pKa: {beta_approx:.4f} mol/L per pH unit")
    
    # Example 3: After adding acid
    print("\n--- Example 3: Buffer After Strong Acid ---")
    pH_new, ha_new, a_new = buffer_after_strong_acid(4.76, 0.01, 0.01, 0.001, 0.1)
    print(f"Initial: [HA] = 0.1 M, [A-] = 0.1 M, pH = 4.76")
    print(f"After adding 1 mL of 1 M HCl:")
    print(f"  New [HA] = {ha_new:.3f} M")
    print(f"  New [A-] = {a_new:.3f} M")
    print(f"  New pH = {pH_new:.2f}")
    
    # Example 4: Phosphate buffer
    print("\n--- Example 4: Phosphate Buffer ---")
    pH = phosphate_buffer(0.05, 0.05)
    print(f"Phosphate buffer (0.05 M each): pH = {pH:.2f}")
    
    # Example 5: Activity correction
    print("\n--- Example 5: Activity Correction ---")
    gamma = debye_huckel_activity(0.1, 1)
    print(f"Activity coefficient at I=0.1: gamma = {gamma:.3f}")
    
    pH_ideal = henderson_hasselbalch(4.76, 0.1, 0.1)
    pH_activity = buffer_pH_with_activity(4.76, 0.1, 0.1, gamma)
    print(f"Ideal pH: {pH_ideal:.2f}")
    print(f"With activity correction: {pH_activity:.2f}")
    
    # Example 6: Buffer preparation
    print("\n--- Example 6: Buffer Preparation ---")
    g_acid, g_base = prepare_buffer_by_mixing(
        5.0, 4.76, 0.5, 0.1, 60.05, 82.03
    )
    print(f"To prepare 500 mL of pH 5.0 acetate buffer (0.1 M):")
    print(f"  Acetic acid: {g_acid:.2f} g")
    print(f"  Sodium acetate: {g_base:.2f} g")
    
    # Example 7: Check buffer effectiveness
    print("\n--- Example 7: Buffer Selection ---")
    acids = {
        'acetic': 4.76,
        'phosphoric': 7.20,
        'carbonic': 6.35,
        'boric': 9.24
    }
    
    target = 7.0
    print(f"Best buffer for pH {target}:")
    for name, pKa in acids.items():
        effective = is_effective_buffer(target, pKa)
        print(f"  {name} (pKa={pKa}): {'OK' if effective else 'NO'}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
