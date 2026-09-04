"""
CHM 320 Advanced Inorganic Chemistry - Computational Tools
==========================================================

This module provides functions for:
- Ligand Field Stabilization Energy (LFSE) calculations
- Tanabe-Sugano diagram predictions
- Magnetic moment calculations
- Crystal field splitting calculations

Author: Chemistry Memory System
Course: CHM 320 - Advanced Inorganic Chemistry

## Solver Instructions (for AI Agent)

When you encounter crystal field theory, LFSE, spin state, magnetic moment, and d-d transition problems:

### Step 1: Identify what is given and what is asked
- Given: metal, oxidation state, ligands, geometry, spectroscopic transitions or magnetic data
- Asked: Delta0, LFSE, spin state, mu_eff, transition wavelengths, spectrochemical series

### Step 2: Choose the correct function
- `calculate_cf_splitting(metal, oxidation_state, ligands, geometry)`: Delta0 or Deltaₜ
- `calculate_lfse(d_electrons, geometry, spin_state, delta_o)`: LFSE in kJ/mol and cm-1
- `predict_transitions(d_electrons, geometry, delta_o)`: Predict d-d transition wavelengths
- `find_delta_from_transitions(d_n, transitions)`: Back-calculate Delta from observed transitions
- `calculate_magnetic_moment(unpaired_electrons)`: mu_eff = √(n(n+2))
- `determine_spin_state_from_moment(moment, d_electrons)`: Deduce spin state from mu
- `predict_spin_state(d_electrons, delta_o, pairing_energy)`: High-spin vs low-spin
- `get_spectrochemical_series()`: Ligands ordered by field strength
- `get_irving_williams_series()`: M2+ complex stability order

### Step 3: Handle special cases
- Deltaₜ ~ 4/9 Delta0 for same metal/ligands
- Only d4-d7 in octahedral have high/low spin choice
- Spin-only formula: mu = √(n(n+2)); orbital contribution adds for >3d metals
- Jahn-Teller: d9 (Cu2+) octahedral -> elongated

### Examples
```python
calculate_lfse(6, 'octahedral', 'low', 22000)  # [Fe(CN)6]4- -> LFSE = -528 kJ/mol
calculate_magnetic_moment(4)  # -> mu = 4.90 BM
predict_spin_state(6, 22000, 25000)  # Delta > P -> low spin
```
"""

from typing import Literal, Tuple, Dict, Optional
import math

# =============================================================================
# CRYSTAL FIELD SPLITTING CALCULATIONS
# =============================================================================

def calculate_cf_splitting(
    metal: str,
    oxidation: int,
    geometry: Literal["octahedral", "tetrahedral", "square_planar"],
    ligand_strength: str = "intermediate"
) -> Dict[str, float]:
    """
    Calculate crystal field splitting parameters for a metal complex.
    
    Parameters
    ----------
    metal : str
        Metal symbol (e.g., "Fe", "Co", "Ni")
    oxidation : int
        Oxidation state of the metal (e.g., 2, 3)
    geometry : str
        Geometry of the complex: "octahedral", "tetrahedral", or "square_planar"
    ligand_strength : str
        Ligand field strength: "weak", "intermediate", or "strong"
    
    Returns
    -------
    dict
        Dictionary containing:
        - delta_oct: Octahedral splitting (cm-1)
        - delta_actual: Actual splitting for given geometry (cm-1)
        - delta_ratio: Ratio of actual to octahedral splitting
    
    Notes
    -----
    For tetrahedral: Delta_tet ~ 4/9 x Delta_oct
    For square planar: Complex splitting pattern, approximated here
    
    Example
    -------
    >>> result = calculate_cf_splitting("Fe", 3, "octahedral", "intermediate")
    >>> print(f"Delta_oct = {result['delta_oct']:.0f} cm-1")
    """
    # Approximate Delta_oct values (cm-1) for common metals
    # These are typical ranges; actual values depend on specific ligands
    delta_oct_base = {
        "Ti": {2: 12500, 3: 17000, 4: 22000},
        "V": {2: 14000, 3: 18000, 4: 20000},
        "Cr": {2: 14000, 3: 17500, 4: 22000},
        "Mn": {2: 8000, 3: 16000, 4: 21000},
        "Fe": {2: 10000, 3: 17000, 4: 20000},
        "Co": {2: 9000, 3: 18000, 4: 21000},
        "Ni": {2: 8500, 3: 14000, 4: 17000},
        "Cu": {2: 12500, 3: 16000},
    }
    
    # Ligand strength multipliers
    ligand_multipliers = {
        "weak": 0.7,       # e.g., F-, H2O
        "intermediate": 1.0,  # e.g., NH3, pyridine
        "strong": 1.5      # e.g., CN-, CO
    }
    
    # Get base Delta_oct value
    metal = metal.capitalize()
    if metal not in delta_oct_base:
        raise ValueError(f"Metal '{metal}' not in database")
    if oxidation not in delta_oct_base[metal]:
        raise ValueError(f"Oxidation state {oxidation} not available for {metal}")
    
    delta_oct = delta_oct_base[metal][oxidation] * ligand_multipliers.get(ligand_strength, 1.0)
    
    # Calculate geometry-specific splitting
    geometry_ratios = {
        "octahedral": 1.0,
        "tetrahedral": 4/9,
        "square_planar": 1.3  # Approximate; actual pattern is complex
    }
    
    if geometry not in geometry_ratios:
        raise ValueError(f"Unknown geometry: {geometry}")
    
    delta_actual = delta_oct * geometry_ratios[geometry]
    
    return {
        "delta_oct": delta_oct,
        "delta_actual": delta_actual,
        "delta_ratio": geometry_ratios[geometry]
    }


# =============================================================================
# LIGAND FIELD STABILIZATION ENERGY (LFSE)
# =============================================================================

def calculate_lfse(
    d_electrons: int,
    geometry: Literal["octahedral", "tetrahedral", "square_planar"],
    spin: Literal["high", "low"] = "high",
    pairing_energy: float = None
) -> Dict[str, float]:
    """
    Calculate Ligand Field Stabilization Energy for a transition metal complex.
    
    Parameters
    ----------
    d_electrons : int
        Number of d electrons (1-10)
    geometry : str
        "octahedral", "tetrahedral", or "square_planar"
    spin : str
        "high" or "low" spin (only relevant for octahedral d4-d7)
    pairing_energy : float, optional
        Pairing energy in Delta units (default: 0.5 Delta_oct)
    
    Returns
    -------
    dict
        - lfse_dq: LFSE in units of Dq
        - lfse_actual: LFSE in cm-1 (if geometry parameters available)
        - electron_config: Electron configuration string
        - unpaired_electrons: Number of unpaired electrons
        - spin_only_moment: Spin-only magnetic moment (mu_eff)
    
    Notes
    -----
    Octahedral splitting: t2g (lower) and eg (higher)
    - Each t2g electron: -4 Dq (stabilization)
    - Each eg electron: +6 Dq (destabilization)
    
    Tetrahedral splitting: e (lower) and t2 (higher)
    - Each e electron: -6 Dq
    - Each t2 electron: +4 Dq
    
    Example
    -------
    >>> result = calculate_lfse(6, "octahedral", "low")
    >>> print(f"LFSE = {result['lfse_dq']:.1f} Dq")
    >>> print(f"Electron config: {result['electron_config']}")
    """
    if d_electrons < 0 or d_electrons > 10:
        raise ValueError("d_electrons must be between 0 and 10")
    
    # Octahedral configurations
    # t2g can hold 6 electrons, eg can hold 4
    oct_configs = {
        # d^n: (high_spin_t2g, high_spin_eg, low_spin_t2g, low_spin_eg)
        0: (0, 0, 0, 0),
        1: (1, 0, 1, 0),
        2: (2, 0, 2, 0),
        3: (3, 0, 3, 0),
        4: (3, 1, 4, 0),  # d4: high=t2g3eg1, low=t2g4
        5: (3, 2, 5, 0),  # d5: high=t2g3eg2, low=t2g5
        6: (4, 2, 6, 0),  # d6: high=t2g4eg2, low=t2g6
        7: (5, 2, 6, 1),  # d7: high=t2g5eg2, low=t2g6eg1
        8: (6, 2, 6, 2),
        9: (6, 3, 6, 3),
        10: (6, 4, 6, 4),
    }
    
    # Tetrahedral configurations (always high spin due to small Delta)
    # e can hold 4 electrons, t2 can hold 6
    tet_configs = {
        # d^n: (e, t2)
        0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (2, 1), 4: (2, 2),
        5: (2, 3), 6: (3, 3), 7: (4, 3), 8: (4, 4), 9: (4, 5), 10: (4, 6)
    }
    
    if geometry == "octahedral":
        t2g_h, eg_h, t2g_l, eg_l = oct_configs[d_electrons]
        
        # Determine which configuration to use
        t2g, eg = t2g_h, eg_h  # default to high spin
        if d_electrons in [4, 5, 6, 7]:
            if spin == "low":
                t2g, eg = t2g_l, eg_l
        
        # LFSE = -4 * n(t2g) + 6 * n(eg) in Dq
        lfse_dq = -4 * t2g + 6 * eg
        electron_config = f"t2g^{t2g}e_g^{eg}"
        unpaired = _count_unpaired_oct(d_electrons, spin)
        
    elif geometry == "tetrahedral":
        e, t2 = tet_configs[d_electrons]
        # LFSE = -6 * n(e) + 4 * n(t2) in Dq (using octahedral Dq)
        lfse_dq = -6 * e + 4 * t2
        # Convert to tetrahedral Dq (Delta_tet = 4/9 Delta_oct)
        lfse_dq_tet = lfse_dq * (4/9)
        electron_config = f"e^{e}t2^{t2}"
        unpaired = _count_unpaired_tet(d_electrons)
        
    elif geometry == "square_planar":
        # Square planar: derived from octahedral
        # Approximate using d-orbital ordering: dxy < dz2 < dxz, dyz < dx2-y2
        # Simplified LFSE calculation
        lfse_sq = _calculate_sq_planar_lfse(d_electrons)
        lfse_dq = lfse_sq
        electron_config = f"SP-d^{d_electrons}"
        unpaired = 0 if d_electrons == 8 else _count_unpaired_oct(d_electrons, "low")
    
    else:
        raise ValueError(f"Unknown geometry: {geometry}")
    
    # Calculate spin-only magnetic moment
    spin_only = _spin_only_moment(unpaired)
    
    return {
        "lfse_dq": lfse_dq,
        "electron_config": electron_config,
        "unpaired_electrons": unpaired,
        "spin_only_moment": spin_only,
        "geometry": geometry,
        "spin_state": spin if geometry == "octahedral" else "high"
    }


def _count_unpaired_oct(d_electrons: int, spin: str) -> int:
    """Count unpaired electrons for octahedral geometry."""
    # High spin configurations
    high_spin_unpaired = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1, 10: 0
    }
    # Low spin configurations
    low_spin_unpaired = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 1, 6: 0, 7: 1, 8: 2, 9: 1, 10: 0
    }
    
    if spin == "low" and d_electrons in [4, 5, 6, 7]:
        return low_spin_unpaired[d_electrons]
    return high_spin_unpaired[d_electrons]


def _count_unpaired_tet(d_electrons: int) -> int:
    """Count unpaired electrons for tetrahedral geometry (always high spin)."""
    unpaired = {
        0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1, 10: 0
    }
    return unpaired[d_electrons]


def _calculate_sq_planar_lfse(d_electrons: int) -> float:
    """
    Calculate LFSE for square planar geometry.
    Using approximate orbital energies relative to barycenter:
    dxy: -4.28 Dq, dz2: -0.86 Dq, dxz/dyz: -2.28 Dq each, dx2-y2: +12.28 Dq
    """
    # Orbital energies in Dq
    dxy_e = -4.28
    dz2_e = -0.86
    dxz_dyz_e = -2.28
    dx2y2_e = 12.28
    
    # Fill orbitals in order (simplified)
    configs = {
        0: (0, 0, 0, 0),
        1: (1, 0, 0, 0),
        2: (1, 1, 0, 0),
        3: (1, 2, 0, 0),
        4: (1, 2, 1, 0),
        5: (1, 2, 2, 0),
        6: (2, 2, 2, 0),
        7: (2, 2, 2, 0),  # Unpaired
        8: (2, 2, 2, 0),  # d8 square planar is very stable
        9: (2, 2, 2, 1),
        10: (2, 2, 2, 2),
    }
    
    n_dxy, n_dz2, n_dxzdyz, n_dx2y2 = configs.get(d_electrons, (0, 0, 0, 0))
    
    lfse = (n_dxy * dxy_e + n_dz2 * dz2_e + 
            n_dxzdyz * dxz_dyz_e + n_dx2y2 * dx2y2_e)
    
    return lfse


def _spin_only_moment(n_unpaired: int) -> float:
    """Calculate spin-only magnetic moment: mu = √(n(n+2)) BM."""
    if n_unpaired == 0:
        return 0.0
    return math.sqrt(n_unpaired * (n_unpaired + 2))


# =============================================================================
# TANABE-SUGANO DIAGRAM PREDICTIONS
# =============================================================================

def predict_transitions(
    d_n: int,
    delta_B_ratio: float,
    B: float = None
) -> Dict[str, any]:
    """
    Predict electronic transitions from Tanabe-Sugano diagram parameters.
    
    Parameters
    ----------
    d_n : int
        d electron count (2-8)
    delta_B_ratio : float
        Ratio of Delta_oct/B (field strength parameter)
    B : float, optional
        Racah parameter in cm-1 (uses typical value if not provided)
    
    Returns
    -------
    dict
        - ground_state: Ground state term symbol
        - transitions: List of predicted transitions with energies
        - spin_allowed: Spin-allowed transitions
        - spin_forbidden: Spin-forbidden transitions
    
    Notes
    -----
    Tanabe-Sugano diagrams plot E/B vs Delta/B for each d^n configuration.
    This function provides approximate transition energies.
    
    Example
    -------
    >>> result = predict_transitions(2, 25.0)
    >>> for t in result['transitions']:
    ...     print(f"{t['state']}: {t['energy_cm']:.0f} cm-1")
    """
    # Typical B values (cm-1) for free ions
    B_values = {
        2: 1030,  # d2: V3+
        3: 860,   # d3: Cr3+
        4: 1030,  # d4: Mn3+
        5: 860,   # d5: Fe3+
        6: 1030,  # d6: Co3+
        7: 970,   # d7: Co2+
        8: 1030,  # d8: Ni2+
    }
    
    if d_n < 2 or d_n > 8:
        raise ValueError("d_n must be between 2 and 8 for Tanabe-Sugano analysis")
    
    if B is None:
        B = B_values.get(d_n, 1000)
    
    # Ground states for each d^n
    ground_states = {
        2: "3T1g(F)",  # d2
        3: "4A2g",     # d3
        4: "5Eg",      # d4 (high spin)
        5: "6A1g",     # d5 (high spin)
        6: "5T2g",     # d6 (high spin)
        7: "4T1g(F)",  # d7 (high spin)
        8: "3A2g",     # d8
    }
    
    # Transition data for each d^n (simplified)
    # Format: {d_n: [(state, energy_B_formula, spin_allowed), ...]}
    transitions_data = _get_ts_transitions(d_n, delta_B_ratio)
    
    transitions = []
    spin_allowed = []
    spin_forbidden = []
    
    for state, energy_B, is_allowed in transitions_data:
        energy_cm = energy_B * B
        
        trans = {
            "state": state,
            "energy_B": energy_B,
            "energy_cm": energy_cm,
            "spin_allowed": is_allowed
        }
        transitions.append(trans)
        
        if is_allowed:
            spin_allowed.append(trans)
        else:
            spin_forbidden.append(trans)
    
    return {
        "d_electrons": d_n,
        "ground_state": ground_states[d_n],
        "delta_B_ratio": delta_B_ratio,
        "B_parameter": B,
        "delta_oct_cm": delta_B_ratio * B,
        "transitions": transitions,
        "spin_allowed": spin_allowed,
        "spin_forbidden": spin_forbidden
    }


def _get_ts_transitions(d_n: int, delta_B: float) -> list:
    """
    Get approximate transition energies from Tanabe-Sugano diagram.
    Returns list of (state, E/B, spin_allowed) tuples.
    """
    # Simplified transition data
    # These are approximations based on Tanabe-Sugano diagrams
    
    if d_n == 2:
        # d2: V3+ - Transitions from 3T1g(F)
        return [
            ("3T2g", delta_B, True),
            ("3T1g(P)", 1.5 * delta_B + 15, True),
            ("3A2g", 2 * delta_B, True),
            ("1D", delta_B + 10, False),
            ("1G", 2 * delta_B + 5, False),
        ]
    
    elif d_n == 3:
        # d3: Cr3+ - Transitions from 4A2g
        return [
            ("4T2g", delta_B, True),
            ("4T1g(F)", 1.5 * delta_B, True),
            ("4T1g(P)", 2.5 * delta_B + 10, True),
            ("2Eg", delta_B + 5, False),
            ("2T1g", delta_B + 7, False),
        ]
    
    elif d_n == 8:
        # d8: Ni2+ - Transitions from 3A2g
        return [
            ("3T2g", delta_B, True),
            ("3T1g(F)", 1.5 * delta_B, True),
            ("3T1g(P)", 2.5 * delta_B + 10, True),
            ("1Eg", delta_B + 2, False),
            ("1A1g", 2 * delta_B, False),
        ]
    
    elif d_n == 6:
        # d6: Co3+ - High spin from 5T2g
        if delta_B < 20:  # High spin region
            return [
                ("5Eg", delta_B, True),
                ("3T1g", delta_B + 10, False),
            ]
        else:  # Low spin region
            return [
                ("1A1g", delta_B - 5, True),
                ("1T1g", delta_B + 10, True),
                ("1T2g", 1.5 * delta_B, True),
            ]
    
    elif d_n == 4:
        # d4: Mn3+ - High spin from 5Eg
        return [
            ("5T2g", delta_B, True),
            ("3T1g", delta_B + 15, False),
        ]
    
    elif d_n == 5:
        # d5: Fe3+ - High spin from 6A1g
        return [
            ("4T1g", delta_B, False),
            ("4T2g", 1.5 * delta_B, False),
            ("4A1g", 2 * delta_B + 10, False),
        ]
    
    elif d_n == 7:
        # d7: Co2+ - High spin from 4T1g(F)
        return [
            ("4T2g", delta_B, True),
            ("4A2g", 2 * delta_B, True),
            ("4T1g(P)", 1.5 * delta_B + 15, True),
        ]
    
    return []


def find_delta_from_transitions(
    d_n: int,
    observed_transitions_cm: Dict[str, float]
) -> Dict[str, float]:
    """
    Extract Delta_oct and B parameters from observed transition energies.
    
    Parameters
    ----------
    d_n : int
        d electron count
    observed_transitions_cm : dict
        Dictionary mapping transition labels to observed energies (cm-1)
    
    Returns
    -------
    dict
        - delta_oct: Crystal field splitting (cm-1)
        - B: Racah parameter (cm-1)
        - delta_B_ratio: Delta_oct/B ratio
    
    Example
    -------
    >>> transitions = {"v1": 17400, "v2": 24600, "v3": 38000}
    >>> result = find_delta_from_transitions(3, transitions)
    >>> print(f"Delta_oct = {result['delta_oct']:.0f} cm-1")
    """
    # For d3 and d8 (most common), v1 = Delta_oct
    if d_n == 3 or d_n == 8:
        if "v1" in observed_transitions_cm:
            delta_oct = observed_transitions_cm["v1"]
            
            # B can be estimated from v2 and v3
            # v2 = Delta_oct + x, where x relates to B
            # For d3: v3 = (1/2)(15 + 3Delta_oct - √(225 - 18Delta_oct + 9Delta_oct2))
            
            if "v3" in observed_transitions_cm:
                v3 = observed_transitions_cm["v3"]
                # Approximate B calculation for d3/d8
                B = (v3 - 1.5 * delta_oct) / 10  # Rough approximation
            else:
                B = 900  # Default approximate value
            
            return {
                "delta_oct": delta_oct,
                "B": B,
                "delta_B_ratio": delta_oct / B if B > 0 else 0
            }
    
    # For d2 and d7
    elif d_n == 2 or d_n == 7:
        if "v1" in observed_transitions_cm:
            # v1 ~ Delta_oct for these systems
            delta_oct = observed_transitions_cm["v1"]
            B = observed_transitions_cm.get("v2", delta_oct) / 15
            
            return {
                "delta_oct": delta_oct,
                "B": B,
                "delta_B_ratio": delta_oct / B if B > 0 else 0
            }
    
    return {
        "delta_oct": 0,
        "B": 0,
        "delta_B_ratio": 0,
        "note": "Insufficient data or unsupported d^n configuration"
    }


# =============================================================================
# MAGNETIC MOMENT CALCULATIONS
# =============================================================================

def calculate_magnetic_moment(
    n_unpaired: int,
    include_orbital: bool = False,
    orbital_contribution: float = 0.0
) -> Dict[str, float]:
    """
    Calculate effective magnetic moment for a transition metal complex.
    
    Parameters
    ----------
    n_unpaired : int
        Number of unpaired electrons
    include_orbital : bool
        Whether to include orbital contribution
    orbital_contribution : float
        Orbital contribution in Bohr magnetons (typical: 0-1 BM)
    
    Returns
    -------
    dict
        - mu_spin_only: Spin-only magnetic moment
        - mu_eff: Effective magnetic moment (with orbital if included)
        - spin_contribution: S value
        - formula_used: Formula description
    
    Notes
    -----
    Spin-only formula: mu_so = √(n(n+2)) BM
    With orbital: mu_eff ~ √(4S(S+1) + L(L+1)) for free ions
    
    Example
    -------
    >>> result = calculate_magnetic_moment(3)
    >>> print(f"mu_eff = {result['mu_spin_only']:.2f} BM")
    """
    # Spin-only calculation
    mu_spin_only = _spin_only_moment(n_unpaired)
    
    # Spin quantum number
    S = n_unpaired / 2
    
    # Effective moment with orbital contribution
    if include_orbital and orbital_contribution > 0:
        mu_eff = math.sqrt(mu_spin_only**2 + orbital_contribution**2)
        formula = "mu_eff = √(mu_so2 + mu_orb2)"
    else:
        mu_eff = mu_spin_only
        formula = "mu_so = √(n(n+2)) BM"
    
    return {
        "unpaired_electrons": n_unpaired,
        "spin_S": S,
        "mu_spin_only": round(mu_spin_only, 2),
        "mu_eff": round(mu_eff, 2),
        "orbital_contribution": orbital_contribution if include_orbital else 0,
        "formula_used": formula
    }


def determine_spin_state_from_moment(
    d_electrons: int,
    mu_observed: float,
    geometry: str = "octahedral"
) -> Dict[str, any]:
    """
    Determine spin state from observed magnetic moment.
    
    Parameters
    ----------
    d_electrons : int
        Number of d electrons
    mu_observed : float
        Observed magnetic moment in Bohr magnetons
    geometry : str
        Complex geometry (default: octahedral)
    
    Returns
    -------
    dict
        - predicted_spin_state: "high" or "low"
        - predicted_unpaired: Predicted number of unpaired electrons
        - high_spin_moment: Expected moment for high spin
        - low_spin_moment: Expected moment for low spin
        - confidence: "high", "medium", or "low"
    
    Example
    -------
    >>> result = determine_spin_state_from_moment(6, 5.2)
    >>> print(f"Predicted: {result['predicted_spin_state']} spin")
    """
    # Expected moments for high and low spin
    if geometry == "octahedral":
        spin_data = {
            # d_n: (high_spin_unpaired, low_spin_unpaired)
            0: (0, 0), 1: (1, 1), 2: (2, 2), 3: (3, 3),
            4: (4, 2),   # d4: high=4 unpaired, low=2
            5: (5, 1),   # d5: high=5 unpaired, low=1
            6: (4, 0),   # d6: high=4 unpaired, low=0
            7: (3, 1),   # d7: high=3 unpaired, low=1
            8: (2, 2), 9: (1, 1), 10: (0, 0)
        }
    else:
        # Tetrahedral always high spin
        spin_data = {i: (_count_unpaired_tet(i), _count_unpaired_tet(i)) 
                     for i in range(11)}
    
    if d_electrons not in spin_data:
        raise ValueError(f"Invalid d_electron count: {d_electrons}")
    
    high_unpaired, low_unpaired = spin_data[d_electrons]
    high_moment = _spin_only_moment(high_unpaired)
    low_moment = _spin_only_moment(low_unpaired)
    
    # Determine which is closer
    high_diff = abs(mu_observed - high_moment)
    low_diff = abs(mu_observed - low_moment)
    
    # Consider orbital contributions (±0.5 BM is typical)
    tolerance = 0.5
    
    if d_electrons in [0, 1, 2, 3, 8, 9, 10]:
        # Only one spin state possible
        predicted = "high" if high_unpaired > 0 else "diamagnetic"
        confidence = "high"
        predicted_unpaired = high_unpaired
    elif high_diff < low_diff - tolerance:
        predicted = "high"
        predicted_unpaired = high_unpaired
        confidence = "high" if high_diff < tolerance else "medium"
    elif low_diff < high_diff - tolerance:
        predicted = "low"
        predicted_unpaired = low_unpaired
        confidence = "high" if low_diff < tolerance else "medium"
    else:
        predicted = "intermediate/spin_crossover"
        predicted_unpaired = (high_unpaired + low_unpaired) // 2
        confidence = "low"
    
    return {
        "d_electrons": d_electrons,
        "geometry": geometry,
        "mu_observed": mu_observed,
        "predicted_spin_state": predicted,
        "predicted_unpaired": predicted_unpaired,
        "high_spin_moment": round(high_moment, 2),
        "low_spin_moment": round(low_moment, 2),
        "confidence": confidence
    }


# =============================================================================
# PREDICT SPIN STATE
# =============================================================================

def predict_spin_state(
    metal: str,
    oxidation: int,
    ligand_strength: str = "intermediate"
) -> Dict[str, any]:
    """
    Predict high-spin vs low-spin state for a metal complex.
    
    Parameters
    ----------
    metal : str
        Metal symbol
    oxidation : int
        Oxidation state
    ligand_strength : str
        "weak", "intermediate", or "strong"
    
    Returns
    -------
    dict
        - predicted_spin: "high" or "low"
        - d_electrons: Number of d electrons
        - notes: Additional information
    
    Example
    -------
    >>> result = predict_spin_state("Fe", 3, "strong")
    >>> print(f"Predicted: {result['predicted_spin']} spin")
    """
    # d electron configurations
    d_electron_config = {
        ("Ti", 2): 2, ("Ti", 3): 1, ("Ti", 4): 0,
        ("V", 2): 3, ("V", 3): 2, ("V", 4): 1,
        ("Cr", 2): 4, ("Cr", 3): 3,
        ("Mn", 2): 5, ("Mn", 3): 4, ("Mn", 4): 3,
        ("Fe", 2): 6, ("Fe", 3): 5,
        ("Co", 2): 7, ("Co", 3): 6,
        ("Ni", 2): 8, ("Ni", 3): 7,
        ("Cu", 2): 9, ("Cu", 1): 10,
        ("Zn", 2): 10,
    }
    
    metal = metal.capitalize()
    key = (metal, oxidation)
    
    if key not in d_electron_config:
        return {
            "predicted_spin": "unknown",
            "d_electrons": None,
            "notes": f"Unknown configuration for {metal}({oxidation})"
        }
    
    d_electrons = d_electron_config[key]
    
    # Only d4-d7 can be high or low spin
    if d_electrons not in [4, 5, 6, 7]:
        spin = "high" if d_electrons > 0 else "N/A"
        return {
            "predicted_spin": spin,
            "d_electrons": d_electrons,
            "notes": f"d{d_electrons} has only one spin state possible"
        }
    
    # Predict based on ligand strength
    # Strong field -> low spin, weak field -> high spin
    if ligand_strength == "strong":
        predicted = "low"
        notes = "Strong field ligands favor low spin (large Delta > P)"
    elif ligand_strength == "weak":
        predicted = "high"
        notes = "Weak field ligands favor high spin (small Delta < P)"
    else:
        # Intermediate - depends on specific metal
        # Higher oxidation -> larger Delta -> more likely low spin
        if oxidation >= 3:
            predicted = "low"
            notes = "Higher oxidation state increases Delta, favoring low spin"
        else:
            predicted = "high"
            notes = "Lower oxidation state, intermediate field likely high spin"
    
    return {
        "predicted_spin": predicted,
        "d_electrons": d_electrons,
        "ligand_strength": ligand_strength,
        "notes": notes
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_spectrochemical_series() -> Dict[str, float]:
    """
    Return the spectrochemical series ranking.
    
    Returns
    -------
    dict
        Ligand names mapped to relative field strength values
    """
    return {
        "I-": 0.5,
        "Br-": 0.6,
        "S2-": 0.7,
        "SCN-": 0.8,
        "Cl-": 0.8,
        "N3-": 0.9,
        "F-": 0.9,
        "OH-": 0.95,
        "oxalate": 1.0,
        "H2O": 1.0,
        "NCS-": 1.02,
        "pyridine": 1.15,
        "NH3": 1.25,
        "en": 1.28,
        "bipy": 1.33,
        "phen": 1.34,
        "NO2-": 1.4,
        "PPh3": 1.45,
        "CN-": 1.7,
        "CO": 2.0,
    }


def get_irving_williams_series() -> list:
    """
    Return the Irving-Williams series for complex stability.
    
    Returns
    -------
    list
        Metals in order of increasing complex stability
    """
    return ["Mn2+", "Fe2+", "Co2+", "Ni2+", "Cu2+", "Zn2+"]


if __name__ == "__main__":
    # Quick test
    print("=== LFSE Test ===")
    result = calculate_lfse(6, "octahedral", "low")
    print(f"d6 low spin: LFSE = {result['lfse_dq']:.1f} Dq")
    print(f"Config: {result['electron_config']}")
    print(f"Unpaired: {result['unpaired_electrons']}")
    
    print("\n=== Magnetic Moment Test ===")
    mu = calculate_magnetic_moment(4)
    print(f"4 unpaired electrons: mu = {mu['mu_spin_only']:.2f} BM")
    
    print("\n=== Tanabe-Sugano Test ===")
    ts = predict_transitions(3, 25.0)
    print(f"Ground state: {ts['ground_state']}")
    for t in ts['spin_allowed'][:3]:
        print(f"  {t['state']}: {t['energy_cm']:.0f} cm-1")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'calculate_cf_splitting', 'description': 'Calculate crystal field splitting parameters for a metal complex.\n\nParameters\n----------\nmetal : str\n    Metal symbol (e.g., "Fe", "Co", "Ni")\noxidation : int\n    Oxidation state of the metal (e.g., 2, 3)\ngeometry : str\n    Geometry of the complex: "octahedral", "tetrahedral", or "square_planar"\nligand_strength : str\n    Ligand field strength: "weak", "intermediate", or "strong"\n\nReturns\n-------\ndict\n    Dictionary containing:\n    - delta_oct: Octahedral splitting (cm-1)\n    - delta_actual: Actual splitting for given geometry (cm-1)\n    - delta_ratio: Ratio of actual to octahedral splitting\n\nNotes\n-----\nFor tetrahedral: Delta_tet ~ 4/9 x Delta_oct\nFor square planar: Complex splitting pattern, approximated here\n\nExample\n-------\n>>> result = calculate_cf_splitting("Fe", 3, "octahedral", "intermediate")\n>>> print(f"Delta_oct = {result[\'delta_oct\']:.0f} cm-1")', 'inputSchema': {'type': 'object', 'properties': {'metal': {'type': 'string', 'description': 'Metal'}, 'oxidation': {'type': 'string', 'description': 'Oxidation'}, 'geometry': {'type': 'string', 'description': 'Geometry'}, 'ligand_strength': {'type': 'string', 'description': 'Ligand Strength', 'default': 'intermediate'}}, 'required': ['metal', 'oxidation', 'geometry']}},
    {'name': 'calculate_lfse', 'description': 'Calculate Ligand Field Stabilization Energy for a transition metal complex.\n\nParameters\n----------\nd_electrons : int\n    Number of d electrons (1-10)\ngeometry : str\n    "octahedral", "tetrahedral", or "square_planar"\nspin : str\n    "high" or "low" spin (only relevant for octahedral d4-d7)\npairing_energy : float, optional\n    Pairing energy in Delta units (default: 0.5 Delta_oct)\n\nReturns\n-------\ndict\n    - lfse_dq: LFSE in units of Dq\n    - lfse_actual: LFSE in cm-1 (if geometry parameters available)\n    - electron_config: Electron configuration string\n    - unpaired_electrons: Number of unpaired electrons\n    - spin_only_moment: Spin-only magnetic moment (mu_eff)\n\nNotes\n-----\nOctahedral splitting: t2g (lower) and eg (higher)\n- Each t2g electron: -4 Dq (stabilization)\n- Each eg electron: +6 Dq (destabilization)\n\nTetrahedral splitting: e (lower) and t2 (higher)\n- Each e electron: -6 Dq\n- Each t2 electron: +4 Dq\n\nExample\n-------\n>>> result = calculate_lfse(6, "octahedral", "low")\n>>> print(f"LFSE = {result[\'lfse_dq\']:.1f} Dq")\n>>> print(f"Electron config: {result[\'electron_config\']}")', 'inputSchema': {'type': 'object', 'properties': {'d_electrons': {'type': 'number', 'description': 'D Electrons'}, 'geometry': {'type': 'string', 'description': 'Geometry'}, 'spin': {'type': 'string', 'description': 'Spin', 'default': 'high'}, 'pairing_energy': {'type': 'string', 'description': 'Pairing Energy', 'default': None}}, 'required': ['d_electrons', 'geometry']}},
    {'name': 'calculate_magnetic_moment', 'description': 'Calculate effective magnetic moment for a transition metal complex.\n\nParameters\n----------\nn_unpaired : int\n    Number of unpaired electrons\ninclude_orbital : bool\n    Whether to include orbital contribution\norbital_contribution : float\n    Orbital contribution in Bohr magnetons (typical: 0-1 BM)\n\nReturns\n-------\ndict\n    - mu_spin_only: Spin-only magnetic moment\n    - mu_eff: Effective magnetic moment (with orbital if included)\n    - spin_contribution: S value\n    - formula_used: Formula description\n\nNotes\n-----\nSpin-only formula: mu_so = √(n(n+2)) BM\nWith orbital: mu_eff ~ √(4S(S+1) + L(L+1)) for free ions\n\nExample\n-------\n>>> result = calculate_magnetic_moment(3)\n>>> print(f"mu_eff = {result[\'mu_spin_only\']:.2f} BM")', 'inputSchema': {'type': 'object', 'properties': {'n_unpaired': {'type': 'number', 'description': 'N Unpaired'}, 'include_orbital': {'type': 'string', 'description': 'Include Orbital', 'default': False}, 'orbital_contribution': {'type': 'string', 'description': 'Orbital Contribution', 'default': 0.0}}, 'required': ['n_unpaired']}},
    {'name': 'determine_spin_state_from_moment', 'description': 'Determine spin state from observed magnetic moment.\n\nParameters\n----------\nd_electrons : int\n    Number of d electrons\nmu_observed : float\n    Observed magnetic moment in Bohr magnetons\ngeometry : str\n    Complex geometry (default: octahedral)\n\nReturns\n-------\ndict\n    - predicted_spin_state: "high" or "low"\n    - predicted_unpaired: Predicted number of unpaired electrons\n    - high_spin_moment: Expected moment for high spin\n    - low_spin_moment: Expected moment for low spin\n    - confidence: "high", "medium", or "low"\n\nExample\n-------\n>>> result = determine_spin_state_from_moment(6, 5.2)\n>>> print(f"Predicted: {result[\'predicted_spin_state\']} spin")', 'inputSchema': {'type': 'object', 'properties': {'d_electrons': {'type': 'number', 'description': 'D Electrons'}, 'mu_observed': {'type': 'number', 'description': 'Mu Observed'}, 'geometry': {'type': 'string', 'description': 'Geometry', 'default': 'octahedral'}}, 'required': ['d_electrons', 'mu_observed']}},
    {'name': 'find_delta_from_transitions', 'description': 'Extract Delta_oct and B parameters from observed transition energies.\n\nParameters\n----------\nd_n : int\n    d electron count\nobserved_transitions_cm : dict\n    Dictionary mapping transition labels to observed energies (cm-1)\n\nReturns\n-------\ndict\n    - delta_oct: Crystal field splitting (cm-1)\n    - B: Racah parameter (cm-1)\n    - delta_B_ratio: Delta_oct/B ratio\n\nExample\n-------\n>>> transitions = {"v1": 17400, "v2": 24600, "v3": 38000}\n>>> result = find_delta_from_transitions(3, transitions)\n>>> print(f"Delta_oct = {result[\'delta_oct\']:.0f} cm-1")', 'inputSchema': {'type': 'object', 'properties': {'d_n': {'type': 'number', 'description': 'D N'}, 'observed_transitions_cm': {'type': 'string', 'description': 'Observed Transitions Cm'}}, 'required': ['d_n', 'observed_transitions_cm']}},
    {'name': 'get_irving_williams_series', 'description': 'Return the Irving-Williams series for complex stability.\n\nReturns\n-------\nlist\n    Metals in order of increasing complex stability', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'get_spectrochemical_series', 'description': 'Return the spectrochemical series ranking.\n\nReturns\n-------\ndict\n    Ligand names mapped to relative field strength values', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'predict_spin_state', 'description': 'Predict high-spin vs low-spin state for a metal complex.\n\nParameters\n----------\nmetal : str\n    Metal symbol\noxidation : int\n    Oxidation state\nligand_strength : str\n    "weak", "intermediate", or "strong"\n\nReturns\n-------\ndict\n    - predicted_spin: "high" or "low"\n    - d_electrons: Number of d electrons\n    - notes: Additional information\n\nExample\n-------\n>>> result = predict_spin_state("Fe", 3, "strong")\n>>> print(f"Predicted: {result[\'predicted_spin\']} spin")', 'inputSchema': {'type': 'object', 'properties': {'metal': {'type': 'string', 'description': 'Metal'}, 'oxidation': {'type': 'string', 'description': 'Oxidation'}, 'ligand_strength': {'type': 'string', 'description': 'Ligand Strength', 'default': 'intermediate'}}, 'required': ['metal', 'oxidation']}},
    {'name': 'predict_transitions', 'description': 'Predict electronic transitions from Tanabe-Sugano diagram parameters.\n\nParameters\n----------\nd_n : int\n    d electron count (2-8)\ndelta_B_ratio : float\n    Ratio of Delta_oct/B (field strength parameter)\nB : float, optional\n    Racah parameter in cm-1 (uses typical value if not provided)\n\nReturns\n-------\ndict\n    - ground_state: Ground state term symbol\n    - transitions: List of predicted transitions with energies\n    - spin_allowed: Spin-allowed transitions\n    - spin_forbidden: Spin-forbidden transitions\n\nNotes\n-----\nTanabe-Sugano diagrams plot E/B vs Delta/B for each d^n configuration.\nThis function provides approximate transition energies.\n\nExample\n-------\n>>> result = predict_transitions(2, 25.0)\n>>> for t in result[\'transitions\']:\n...     print(f"{t[\'state\']}: {t[\'energy_cm\']:.0f} cm-1")', 'inputSchema': {'type': 'object', 'properties': {'d_n': {'type': 'number', 'description': 'D N'}, 'delta_B_ratio': {'type': 'number', 'description': 'Delta B Ratio'}, 'B': {'type': 'number', 'description': 'B', 'default': None}}, 'required': ['d_n', 'delta_B_ratio']}}
]
