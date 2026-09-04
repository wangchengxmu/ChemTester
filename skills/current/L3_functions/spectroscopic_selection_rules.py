"""
Spectroscopic Selection Rules - L3 Implementation

Transition dipole moment integrals and selection rule evaluation.
Source: Quantum States of Atoms and Molecules (Zielinksi et al.), Ch4.5-4.7

## Solver Instructions (for AI Agent)

When you encounter spectroscopic selection rule problems (transition dipole moments, allowed/forbidden transitions, IR/Raman activity), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **PIB transitions**: Given initial and final quantum numbers -> is transition allowed? What is the transition moment?
- **Harmonic oscillator**: Given initial/final vibrational quantum numbers -> selection rule check
- **Rigid rotor**: Given J quantum numbers -> check DeltaJ = ±1 selection rule
- **Hydrogen atom**: Given n,l,m quantum numbers -> check all selection rules (Deltal=±1, Deltam=0,±1)
- **IR/Raman activity**: Given molecular symmetry -> determine if mode is IR and/or Raman active

### Step 2: Choose the correct function
- `pib_wavefunction(n, L, x)` -> ψ_n(x) = √(2/L)sin(npix/L) value at position x
- `transition_dipole_integral(n_i, n_f, L, numerical=False)` -> mu_if for particle-in-a-box (C·m)
- `check_pib_selection_rule(n_i, n_f)` -> True if Deltan is odd (allowed)
- `check_ho_selection_rule(v_i, v_f)` -> True if Deltav = ±1 (harmonic oscillator)
- `check_rotor_selection_rule(J_i, J_f)` -> True if DeltaJ = ±1
- `check_atomic_selection_rule(n_i, l_i, m_i, n_f, l_f, m_f)` -> Deltal=±1, Deltam=0,±1
- `ir_raman_activity(symmetry_species, dipole_moment_change, polarizability_change)` -> (IR_active, Raman_active)

### Step 3: Handle special cases
- PIB: Deltan must be odd for non-zero transition dipole moment
- HO: only Deltav = ±1 allowed for harmonic oscillator; overtones (Deltav = 2,3,...) are weakly allowed for anharmonic
- Rotor: DeltaJ = +1 (absorption, R-branch), DeltaJ = -1 (emission, P-branch), DeltaJ = 0 (Q-branch, forbidden for diatomic)
- Hydrogen atom: Deltal = ±1 is the key rule; Deltan unrestricted
- Mutual exclusion: centrosymmetric molecules have modes that are either IR or Raman active, not both

### Examples
1. **PIB transition**: n=1 -> n=2 in box of length L=1 nm
   -> `check_pib_selection_rule(1, 2)` -> True (Deltan=1, odd)
   -> `transition_dipole_integral(1, 2, 1e-9)` -> non-zero value (allowed)

2. **PIB forbidden**: n=1 -> n=3
   -> `check_pib_selection_rule(1, 3)` -> True (Deltan=2, even) - wait, this is False/forbidden
   -> `transition_dipole_integral(1, 3, 1e-9)` -> 0.0 (forbidden)

3. **Hydrogen atom**: 2s (l=0) -> 2p (l=1)
   -> `check_atomic_selection_rule(2, 0, 0, 2, 1, 0)` -> True (Deltal=+1, Deltam=0, allowed)
   -> 2s -> 3s would be False (Deltal=0)
"""

import math
from typing import Callable, Tuple

# Physical constants
H = 6.62607015e-34  # Planck constant (J·s)
E_CHARGE = 1.602176634e-19  # Electron charge (C)


def pib_wavefunction(n: int, L: float, x: float) -> float:
    """
    Particle-in-a-box wavefunction.
    
    ψ_n(x) = √(2/L) sin(npix/L)
    
    Args:
        n: Quantum number
        L: Box length
        x: Position (0 ≤ x ≤ L)
    
    Returns:
        Wavefunction value
    """
    if x < 0 or x > L:
        return 0.0
    return math.sqrt(2/L) * math.sin(n * math.pi * x / L)


def transition_dipole_integral(n_i: int, n_f: int, L: float, 
                                numerical: bool = False) -> float:
    """
    Calculate transition dipole moment integral for particle-in-a-box.
    
    mu_if = -e ∫0ᴸ ψ_i*(x) x x x ψ_f(x) dx
    
    Args:
        n_i: Initial quantum number
        n_f: Final quantum number
        L: Box length
        numerical: If True, use numerical integration
    
    Returns:
        Transition dipole moment (C·m units without -e prefactor)
    """
    if n_i == n_f:
        return 0.0  # Orthogonality
    
    delta_n = n_f - n_i
    sum_n = n_f + n_i
    
    # Selection rule: integral is zero for even Deltan
    if delta_n % 2 == 0:
        return 0.0
    
    # Analytical result for Deltan = odd:
    term1 = (1 - (-1)**delta_n) / delta_n**2
    term2 = (1 - (-1)**sum_n) / sum_n**2
    
    if not numerical:
        return (2 * L / math.pi**2) * (term1 - term2)
    
    # Numerical integration (Simpson's rule)
    N_points = 1000
    dx = L / N_points
    
    integral = 0.0
    for i in range(N_points + 1):
        x = i * dx
        if i == 0 or i == N_points:
            weight = 1
        elif i % 2 == 0:
            weight = 2
        else:
            weight = 4
        
        integrand = pib_wavefunction(n_i, L, x) * x * pib_wavefunction(n_f, L, x)
        integral += weight * integrand
    
    integral *= dx / 3
    return integral


def selection_rule_pib(n_i: int, n_f: int) -> Tuple[bool, str]:
    """
    Apply particle-in-a-box selection rules.
    
    Rule: Deltan = ±1
    
    Args:
        n_i: Initial quantum number
        n_f: Final quantum number
    
    Returns:
        (is_allowed, reason)
    """
    delta_n = n_f - n_i
    
    if abs(delta_n) == 1:
        return True, f"Deltan = {delta_n} satisfies selection rule"
    else:
        return False, f"Deltan = {delta_n} violates Deltan = ±1 rule"


def selection_rule_harmonic_oscillator(v_i: int, v_f: int) -> Tuple[bool, str]:
    """
    Apply harmonic oscillator vibrational selection rules.
    
    Rule: Deltav = ±1
    
    Args:
        v_i: Initial vibrational quantum number
        v_f: Final vibrational quantum number
    
    Returns:
        (is_allowed, reason)
    """
    delta_v = v_f - v_i
    
    if abs(delta_v) == 1:
        return True, f"Deltav = {delta_v} satisfies selection rule"
    else:
        return False, f"Deltav = {delta_v} violates Deltav = ±1 rule"


def selection_rule_rotational(J_i: int, J_f: int) -> Tuple[bool, str]:
    """
    Apply rotational selection rules.
    
    Rule: DeltaJ = ±1
    
    Args:
        J_i: Initial rotational quantum number
        J_f: Final rotational quantum number
    
    Returns:
        (is_allowed, reason)
    """
    delta_J = J_f - J_i
    
    if abs(delta_J) == 1:
        return True, f"DeltaJ = {delta_J} satisfies selection rule"
    else:
        return False, f"DeltaJ = {delta_J} violates DeltaJ = ±1 rule"


def parity_check(parity_i: str, parity_f: str, operator_parity: str) -> bool:
    """
    Check if transition integral is non-zero using parity.
    
    Integral is non-zero if integrand has overall even parity.
    
    Args:
        parity_i: Parity of initial state ('even' or 'odd')
        parity_f: Parity of final state ('even' or 'odd')
        operator_parity: Parity of transition operator
    
    Returns:
        True if integral is non-zero (allowed)
    """
    # Convert to numeric: even = +1, odd = -1
    def to_num(p):
        return 1 if p == 'even' else -1
    
    product = to_num(parity_i) * to_num(operator_parity) * to_num(parity_f)
    
    # Integral is non-zero if overall parity is odd
    # (integral of odd function over symmetric limits is zero)
    return product == -1


def allowed_transitions_from_level(n: int, max_level: int, 
                                    system: str = 'pib') -> list:
    """
    Find all allowed transitions from a given level.
    
    Args:
        n: Initial quantum number
        max_level: Maximum level to consider
        system: 'pib', 'harmonic', or 'rotational'
    
    Returns:
        List of allowed final quantum numbers
    """
    allowed = []
    
    for n_f in range(1, max_level + 1):
        if n_f == n:
            continue
        
        if system == 'pib':
            is_allowed, _ = selection_rule_pib(n, n_f)
        elif system == 'harmonic':
            is_allowed, _ = selection_rule_harmonic_oscillator(n, n_f)
        elif system == 'rotational':
            is_allowed, _ = selection_rule_rotational(n, n_f)
        else:
            raise ValueError(f"Unknown system: {system}")
        
        if is_allowed:
            allowed.append(n_f)
    
    return allowed


# TODO: Implement for Pass-3
# - group_theory_selection_rule() - Apply group theory with character tables
# - spin_selection_rule() - DeltaS = 0 rule
# - laporte_selection_rule() - g↔u transitions only
# - calculate_intensity() - Relative intensity from |mu|2
