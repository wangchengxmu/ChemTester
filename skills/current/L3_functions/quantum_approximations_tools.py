"""
Quantum Approximations Tools - L3 Implementation

Core functions for approximation methods and multielectron atoms:
- Variational method (trial energy, optimization)
- Perturbation theory (first and second order corrections)
- Term symbol construction
- Hund's rules (ground state prediction)
- Spin-orbit coupling

Source: LibreTexts Physical Chemistry Ch07-08

## Solver Instructions (for AI Agent)

When you encounter quantum approximation problems (variational method, perturbation theory, term symbols, Hund's rules), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Variational energy**: Given trial wavefunction and Hamiltonian -> find upper bound to ground state energy
- **Variational optimization**: Given trial wavefunction with parameter -> find optimal parameter and energy
- **Perturbation correction**: Given unperturbed energies/wavefunctions and perturbation -> find corrected energy
- **Term symbol**: Given electron configuration (e.g., 2p2) -> find all possible term symbols
- **Ground state term**: Given electron configuration -> predict ground state using Hund's rules
- **Spin-orbit coupling**: Given term symbol and ζ (spin-orbit constant) -> find energy levels

### Step 2: Choose the correct function
- `variational_energy(trial_function, hamiltonian_func, domain)` -> E_trial (upper bound)
- `variational_energy_with_param(param_func, hamiltonian_func, param, ...)` -> E(alpha), optimize over alpha
- `perturbation_first_order(psi_0, H_prime, domain)` -> E⁽1⁾ = ⟨ψ0|Ĥ'|ψ0⟩
- `perturbation_second_order(psi_0, H_prime, energies, psi_n, domain)` -> E⁽2⁾ correction
- `term_symbols(n, l, num_electrons)` -> list of valid term symbols (e.g., 1D, 3P, 1S for p2)
- `hunds_rules_ground_state(term_symbols)` -> ground state term (max S, then max L, then min J for <half, max J for >half)
- `spin_orbit_coupling(term_symbol, zeta)` -> energy splitting pattern

### Step 3: Handle special cases
- Variational energy is always ≥ true ground state (upper bound theorem)
- For perturbation: first-order correction to wavefunction is always zero if states are non-degenerate
- Term symbols: must respect Pauli exclusion; equivalent electrons have fewer terms than non-equivalent
- Hund's rules: (1) maximize total spin S, (2) maximize total orbital angular momentum L, (3) for <half-filled: minimize J; for >half-filled: maximize J
- Spin-orbit coupling: lambda = +ζ/(2S) for less than half-filled, -ζ/(2S) for more than half-filled

### Examples
1. **Term symbols for carbon (2p2)**:
   -> `term_symbols(2, 1, 2)` -> ['3P', '1D', '1S']
   -> `hunds_rules_ground_state(['3P', '1D', '1S'])` -> '3P' (max S=1)
   -> Ground state: 3P0 (less than half-filled p shell, so J=0 minimum)

2. **Variational method**: H atom trial function ψ=exp(-alphar), find optimal alpha
   -> Optimal alpha = Z/a0; E_trial ≥ -13.6 eV (exact ground state)
"""

import math
from typing import Tuple, List, Union, Optional, Dict, Callable
import numpy as np
from scipy import integrate
from scipy.special import factorial

# Physical constants (SI units)
PLANCK_CONSTANT = 6.62607015e-34  # J·s
REDUCED_PLANCK = 1.05457182e-34   # J·s
ELECTRON_MASS = 9.1093837e-31     # kg
BOHR_RADIUS = 5.2917721e-11       # m
HARTREE_ENERGY = 4.35974e-18      # J
EV_TO_JOULE = 1.60217663e-19      # J/eV


# =============================================================================
# VARIATIONAL METHOD
# =============================================================================

def variational_energy(
    trial_function: Callable,
    hamiltonian_func: Callable,
    domain: Tuple[float, float] = (-np.inf, np.inf),
    normalize: bool = True
) -> float:
    """
    Calculate variational trial energy for a given trial wavefunction.
    
    E_trial = ⟨ψ|Ĥ|ψ⟩ / ⟨ψ|ψ⟩
    
    Args:
        trial_function: Trial wavefunction ψ(x)
        hamiltonian_func: Function that applies Hamiltonian to wavefunction
        domain: Integration domain (x_min, x_max)
        normalize: If True, normalize the trial function first
    
    Returns:
        Trial energy (upper bound to true ground state energy)
    
    Example:
        >>> # Particle in a box trial function
        >>> psi_trial = lambda x, alpha: x * (L - x) * np.exp(-alpha * x**2)
        >>> E = variational_energy(psi_trial, H_func, domain=(0, L))
    """
    def integrand_numerator(x):
        psi = trial_function(x)
        H_psi = hamiltonian_func(psi, x)
        return np.conj(psi) * H_psi
    
    def integrand_denominator(x):
        psi = trial_function(x)
        return np.conj(psi) * psi
    
    # Compute integrals
    numerator, _ = integrate.quad(integrand_numerator, domain[0], domain[1])
    denominator, _ = integrate.quad(integrand_denominator, domain[0], domain[1])
    
    if denominator == 0:
        raise ValueError("Trial function normalization integral is zero")
    
    return numerator / denominator


def variational_energy_with_param(
    param_func: Callable,
    hamiltonian_func: Callable,
    param: float,
    domain: Tuple[float, float] = (-np.inf, np.inf)
) -> float:
    """
    Calculate variational energy for a trial function with a single parameter.
    
    Args:
        param_func: Function f(x, param) returning trial wavefunction
        hamiltonian_func: Function that applies Hamiltonian
        param: Variational parameter value
        domain: Integration domain
    
    Returns:
        Trial energy for this parameter value
    """
    trial = lambda x: param_func(x, param)
    return variational_energy(trial, hamiltonian_func, domain)


# =============================================================================
# PERTURBATION THEORY
# =============================================================================

def perturbation_first_order_energy(
    psi0: np.ndarray,
    H_prime: np.ndarray
) -> float:
    """
    Calculate first-order energy correction in perturbation theory.
    
    E1 = ⟨ψ0|Ĥ'|ψ0⟩
    
    Args:
        psi0: Unperturbed wavefunction (normalized)
        H_prime: Perturbation Hamiltonian (matrix or operator)
    
    Returns:
        First-order energy correction
    
    Example:
        >>> psi0 = np.array([1, 0, 0])  # Ground state
        >>> H_prime = np.array([[0, V, 0], [V, 0, 0], [0, 0, 0]])
        >>> E1 = perturbation_first_order_energy(psi0, H_prime)
    """
    if isinstance(H_prime, np.ndarray):
        # Matrix representation
        return np.vdot(psi0, H_prime @ psi0).real
    else:
        raise TypeError("H_prime must be a numpy array for matrix operations")


def perturbation_first_order_wavefunction(
    psi0: np.ndarray,
    H_prime: np.ndarray,
    E0: float,
    unperturbed_energies: np.ndarray,
    unperturbed_states: np.ndarray
) -> np.ndarray:
    """
    Calculate first-order wavefunction correction.
    
    |ψ1⟩ = Σ_{m!=n} |m0⟩⟨m0|Ĥ'|n0⟩ / (Eₙ0 - Eₘ0)
    
    Args:
        psi0: Unperturbed state of interest
        H_prime: Perturbation Hamiltonian (matrix)
        E0: Energy of the unperturbed state
        unperturbed_energies: Array of all unperturbed energies
        unperturbed_states: Matrix where columns are unperturbed states
    
    Returns:
        First-order wavefunction correction
    """
    n_states = len(unperturbed_energies)
    psi1 = np.zeros_like(psi0, dtype=float)  # Ensure float dtype
    
    for m in range(n_states):
        if abs(unperturbed_energies[m] - E0) > 1e-15:  # m != n
            state_m = unperturbed_states[:, m]
            matrix_element = np.vdot(state_m, H_prime @ psi0)
            energy_diff = E0 - unperturbed_energies[m]
            psi1 += matrix_element * state_m / energy_diff
    
    return psi1


def perturbation_second_order_energy(
    psi0: np.ndarray,
    H_prime: np.ndarray,
    E0: float,
    unperturbed_energies: np.ndarray,
    unperturbed_states: np.ndarray
) -> float:
    """
    Calculate second-order energy correction.
    
    E2 = Σ_{m!=n} |⟨m0|Ĥ'|n0⟩|2 / (Eₙ0 - Eₘ0)
    
    Args:
        psi0: Unperturbed state of interest
        H_prime: Perturbation Hamiltonian (matrix)
        E0: Energy of the unperturbed state
        unperturbed_energies: Array of all unperturbed energies
        unperturbed_states: Matrix where columns are unperturbed states
    
    Returns:
        Second-order energy correction (negative for ground state)
    """
    n_states = len(unperturbed_energies)
    E2 = 0.0
    
    for m in range(n_states):
        if abs(unperturbed_energies[m] - E0) > 1e-15:  # m != n
            state_m = unperturbed_states[:, m]
            matrix_element = np.vdot(state_m, H_prime @ psi0)
            energy_diff = E0 - unperturbed_energies[m]
            E2 += abs(matrix_element)**2 / energy_diff
    
    return E2.real


# =============================================================================
# ANGULAR MOMENTUM COUPLING
# =============================================================================

def possible_L_values(l1: int, l2: int) -> List[int]:
    """
    Calculate possible total orbital angular momentum L values.
    
    L = |l1 + l2|, |l1 + l2| - 1, ..., |l1 - l2|
    
    Args:
        l1: Orbital quantum number of electron 1
        l2: Orbital quantum number of electron 2
    
    Returns:
        List of possible L values
    
    Example:
        >>> possible_L_values(1, 1)  # Two p electrons
        [2, 1, 0]
    """
    l_max = l1 + l2
    l_min = abs(l1 - l2)
    return list(range(l_max, l_min - 1, -1))


def possible_S_values(n_electrons: int) -> List[float]:
    """
    Calculate possible total spin S values for n electrons.
    
    For n electrons: S = n/2, n/2 - 1, ..., 0 or ½
    
    Args:
        n_electrons: Number of electrons
    
    Returns:
        List of possible S values
    
    Example:
        >>> possible_S_values(2)  # Two electrons
        [1.0, 0.0]
        >>> possible_S_values(3)  # Three electrons
        [1.5, 0.5]
    """
    s_max = n_electrons / 2
    s_min = 0 if n_electrons % 2 == 0 else 0.5
    
    values = []
    s = s_max
    while s >= s_min - 1e-10:
        values.append(s)
        s -= 1
    
    return values


def possible_J_values(L: int, S: float) -> List[float]:
    """
    Calculate possible total angular momentum J values.
    
    J = |L + S|, |L + S| - 1, ..., |L - S|
    
    Args:
        L: Total orbital angular momentum quantum number
        S: Total spin quantum number
    
    Returns:
        List of possible J values (may be half-integer)
    
    Example:
        >>> possible_J_values(1, 1)  # P term, S=1
        [2.0, 1.0, 0.0]
    """
    j_max = L + S
    j_min = abs(L - S)
    
    values = []
    j = j_max
    while j >= j_min - 1e-10:
        values.append(j)
        j -= 1
    
    return values


def L_to_term_letter(L: int) -> str:
    """
    Convert orbital angular momentum L to term symbol letter.
    
    Args:
        L: Orbital angular momentum quantum number
    
    Returns:
        Term symbol letter (S, P, D, F, G, H, ...)
    
    Example:
        >>> L_to_term_letter(0)
        'S'
        >>> L_to_term_letter(2)
        'D'
    """
    letters = ['S', 'P', 'D', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O']
    if L < 0:
        raise ValueError(f"L must be non-negative, got {L}")
    if L >= len(letters):
        return chr(ord('P') + L - 1)  # Continue alphabetically
    return letters[L]


# =============================================================================
# TERM SYMBOLS
# =============================================================================

def term_symbol(L: int, S: float, J: float) -> str:
    """
    Construct atomic term symbol from quantum numbers.
    
    Format: ^{2S+1}L_J
    
    Args:
        L: Total orbital angular momentum quantum number
        S: Total spin quantum number
        J: Total angular momentum quantum number
    
    Returns:
        Term symbol string
    
    Example:
        >>> term_symbol(0, 0.5, 0.5)
        '2S_{1/2}'
        >>> term_symbol(1, 1, 2)
        '3P2'
    """
    multiplicity = int(2 * S + 1)
    letter = L_to_term_letter(L)
    
    # Format J subscript
    if J == int(J):
        j_str = str(int(J))
    else:
        j_str = f"{int(2*J)}/2"
    
    # Format multiplicity superscript
    # Using unicode superscripts for common cases
    superscripts = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
    mult_str = str(multiplicity)
    mult_sup = ''.join(superscripts.get(c, c) for c in mult_str)
    
    return f"{mult_sup}{letter}_{j_str}"


def multiplicity(S: float) -> int:
    """
    Calculate multiplicity from total spin S.
    
    Multiplicity = 2S + 1
    
    Args:
        S: Total spin quantum number
    
    Returns:
        Multiplicity (1=singlet, 2=doublet, 3=triplet, etc.)
    """
    return int(2 * S + 1)


def degeneracy(J: float) -> int:
    """
    Calculate degeneracy of a term from J quantum number.
    
    g = 2J + 1
    
    Args:
        J: Total angular momentum quantum number
    
    Returns:
        Number of M_J states
    """
    return int(2 * J + 1)


# =============================================================================
# HUND'S RULES
# =============================================================================

def hund_ground_state(
    n_electrons: int,
    orbital_type: str,
    fill_fraction: Optional[float] = None
) -> Dict[str, Union[str, int, float]]:
    """
    Apply Hund's rules to determine ground state term symbol.
    
    Rules:
    1. Maximize S (highest multiplicity)
    2. For same S, maximize L
    3. J: minimize if < half-filled, maximize if > half-filled
    
    Args:
        n_electrons: Number of electrons in the open subshell
        orbital_type: Type of orbital ('s', 'p', 'd', 'f')
        fill_fraction: Optional manual fill fraction (overrides calculation)
    
    Returns:
        Dictionary with L, S, J, term symbol, and multiplicity
    
    Example:
        >>> hund_ground_state(2, 'p')  # Carbon
        {'L': 1, 'S': 1.0, 'J': 0.0, 'term': '3P_0', 'multiplicity': 3}
        >>> hund_ground_state(3, 'p')  # Nitrogen
        {'L': 0, 'S': 1.5, 'J': 1.5, 'term': '4S_3/2', 'multiplicity': 4}
    """
    # Maximum electrons in subshell
    max_electrons = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
    orbital_l = {'s': 0, 'p': 1, 'd': 2, 'f': 3}
    
    orbital_type = orbital_type.lower()
    if orbital_type not in max_electrons:
        raise ValueError(f"Unknown orbital type: {orbital_type}")
    
    max_e = max_electrons[orbital_type]
    l = orbital_l[orbital_type]
    
    if n_electrons > max_e:
        raise ValueError(f"Too many electrons ({n_electrons}) for {orbital_type} orbital (max {max_e})")
    
    # Store original n_electrons for J rule
    original_n_electrons = n_electrons
    is_more_than_half = original_n_electrons > max_e / 2
    is_half_filled = original_n_electrons == max_e / 2
    
    # Complement rule: use equivalent hole representation for L calculation
    # but keep track of original filling for J rule
    if is_more_than_half:
        n_electrons = max_e - original_n_electrons  # Use holes
    
    # Rule 1: Maximize S
    # S = n_electrons/2 for maximum spin (all electrons unpaired)
    S_max = n_electrons / 2
    
    # Rule 2: Maximize L for maximum S
    # For maximum parallel spin, electrons occupy different m_l values
    # L_max = sum of largest m_l values
    m_l_values = list(range(l, -l - 1, -1))  # l, l-1, ..., -l
    
    if is_half_filled:
        # Half-filled: all m_l values occupied, sum = 0
        L_max = 0
    elif n_electrons <= len(m_l_values):
        L_max = sum(m_l_values[:n_electrons])
    else:
        # Should not happen after complement conversion
        L_max = sum(m_l_values[:len(m_l_values)])
    
    # Rule 3: Determine J based on ORIGINAL filling
    J_values = possible_J_values(L_max, S_max)
    
    if is_half_filled:
        # Half-filled: only one J value
        J = J_values[0]
    elif is_more_than_half:
        # More than half-filled: maximize J
        J = max(J_values)
    else:
        # Less than half-filled: minimize J
        J = min(J_values)
    
    # Construct term symbol
    term = term_symbol(L_max, S_max, J)
    
    return {
        'L': L_max,
        'S': S_max,
        'J': J,
        'term': term,
        'multiplicity': multiplicity(S_max),
        'degeneracy': degeneracy(J)
    }


# =============================================================================
# SPIN-ORBIT COUPLING
# =============================================================================

def spin_orbit_coupling_energy(
    L: int,
    S: float,
    J: float,
    zeta: float
) -> float:
    """
    Calculate spin-orbit coupling energy contribution.
    
    E_{s-o} = (ζ/2)[J(J+1) - L(L+1) - S(S+1)]
    
    Args:
        L: Total orbital angular momentum quantum number
        S: Total spin quantum number
        J: Total angular momentum quantum number
        zeta: Spin-orbit coupling constant (in same units as desired energy)
    
    Returns:
        Spin-orbit energy contribution
    
    Example:
        >>> spin_orbit_coupling_energy(1, 0.5, 1.5, 1.0)
        0.5
        >>> spin_orbit_coupling_energy(1, 0.5, 0.5, 1.0)
        -1.0
    """
    factor = J * (J + 1) - L * (L + 1) - S * (S + 1)
    return (zeta / 2) * factor


def fine_structure_splitting(
    L: int,
    S: float,
    zeta: float
) -> Dict[float, float]:
    """
    Calculate fine structure splitting for a term.
    
    Args:
        L: Total orbital angular momentum quantum number
        S: Total spin quantum number
        zeta: Spin-orbit coupling constant
    
    Returns:
        Dictionary mapping J values to energy shifts
    
    Example:
        >>> fine_structure_splitting(1, 1, 1.0)  # 3P term
        {2.0: 1.0, 1.0: -1.0, 0.0: -2.0}
    """
    J_values = possible_J_values(L, S)
    splitting = {}
    
    for J in J_values:
        splitting[J] = spin_orbit_coupling_energy(L, S, J, zeta)
    
    return splitting


# =============================================================================
# SELECTION RULES
# =============================================================================

def transition_allowed(
    term1: Tuple[int, float, float],
    term2: Tuple[int, float, float],
    strict: bool = True
) -> Tuple[bool, str]:
    """
    Check if a transition between two atomic terms is allowed.
    
    Selection rules (L-S coupling):
    - DeltaS = 0
    - DeltaL = 0, ±1 (but L=0 to L=0 forbidden if strict)
    - DeltaJ = 0, ±1 (but J=0 to J=0 forbidden)
    
    Args:
        term1: (L1, S1, J1) for initial state
        term2: (L2, S2, J2) for final state
        strict: If True, enforce J=0 to J=0 forbidden rule
    
    Returns:
        Tuple of (is_allowed, reason)
    
    Example:
        >>> transition_allowed((1, 0.5, 1.5), (0, 0.5, 0.5))  # 2P_{3/2} to 2S_{1/2}
        (True, 'Allowed: DeltaS=0, DeltaL=-1, DeltaJ=-1')
    """
    L1, S1, J1 = term1
    L2, S2, J2 = term2
    
    delta_S = abs(S2 - S1)
    delta_L = L2 - L1
    delta_J = J2 - J1
    
    reasons = []
    
    # Check DeltaS = 0
    if delta_S > 1e-10:
        return (False, f"Forbidden: ΔS = {delta_S:.1f} != 0")
    
    reasons.append(f"DeltaS=0")
    
    # Check DeltaL = 0, ±1
    if abs(delta_L) > 1:
        return (False, f"Forbidden: ΔL = {delta_L} (must be 0, ±1)")
    reasons.append(f"DeltaL={delta_L:+d}" if delta_L != 0 else "DeltaL=0")
    
    # Check DeltaJ = 0, ±1
    if abs(delta_J) > 1 + 1e-10:
        return (False, f"Forbidden: DeltaJ = {delta_J:.1f} (must be 0, ±1)")
    
    # Check J=0 to J=0 forbidden
    if strict and J1 == 0 and J2 == 0:
        return (False, "Forbidden: J=0 to J=0 transition")
    
    reasons.append(f"DeltaJ={delta_J:+.1f}" if delta_J != 0 else "DeltaJ=0")
    
    return (True, f"Allowed: " + ", ".join(reasons))


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def angular_momentum_magnitude(j: float) -> float:
    """
    Calculate magnitude of angular momentum vector.
    
    |J| = √(j(j+1)) ℏ
    
    Args:
        j: Angular momentum quantum number
    
    Returns:
        Magnitude in units of ℏ
    """
    return math.sqrt(j * (j + 1))


def z_component(j: float, m: float) -> float:
    """
    Calculate z-component of angular momentum.
    
    J_z = m·ℏ
    
    Args:
        j: Angular momentum quantum number
        m: Magnetic quantum number (-j ≤ m ≤ j)
    
    Returns:
        Z-component in units of ℏ
    """
    if abs(m) > j + 1e-10:
        raise ValueError(f"m = {m} is outside valid range [-{j}, {j}]")
    return m


def count_microstates(orbital_type: str, n_electrons: int) -> int:
    """
    Count the number of possible microstates for an electron configuration.
    
    For n electrons in an orbital with capacity m:
    Number of microstates = C(m, n) where m is orbital capacity
    
    Args:
        orbital_type: Type of orbital ('s', 'p', 'd', 'f')
        n_electrons: Number of electrons
    
    Returns:
        Number of possible microstates
    """
    max_electrons = {'s': 2, 'p': 6, 'd': 10, 'f': 14}
    orbital_type = orbital_type.lower()
    
    if orbital_type not in max_electrons:
        raise ValueError(f"Unknown orbital type: {orbital_type}")
    
    m = max_electrons[orbital_type]
    
    if n_electrons > m:
        raise ValueError(f"Too many electrons for {orbital_type} orbital")
    
    # Binomial coefficient C(m, n) = m! / (n! * (m-n)!)
    from math import comb
    return comb(m, n_electrons)


# =============================================================================
# EXAMPLES AND TESTS
# =============================================================================

if __name__ == "__main__":
    print("Quantum Approximations Tools - Examples")
    print("=" * 50)
    
    # Angular momentum coupling
    print("\n1. Angular Momentum Coupling:")
    print(f"   Possible L values for two p electrons: {possible_L_values(1, 1)}")
    print(f"   Possible S values for 2 electrons: {possible_S_values(2)}")
    print(f"   Possible J values for L=1, S=1: {possible_J_values(1, 1)}")
    
    # Term symbols
    print("\n2. Term Symbols:")
    print(f"   Hydrogen ground state (L=0, S=½, J=½): {term_symbol(0, 0.5, 0.5)}")
    print(f"   Boron excited state (L=1, S=1, J=2): {term_symbol(1, 1, 2)}")
    print(f"   Carbon (L=1, S=1, J=0): {term_symbol(1, 1, 0)}")
    
    # Hund's rules
    print("\n3. Hund's Rules - Ground States:")
    for config in [('p', 1), ('p', 2), ('p', 3), ('p', 4), ('p', 5)]:
        result = hund_ground_state(config[1], config[0])
        print(f"   {config[0]}^{config[1]}: {result['term']}")
    
    # Spin-orbit coupling
    print("\n4. Spin-Orbit Coupling:")
    print(f"   2P term (L=1, S=½) splitting with ζ=1:")
    splitting = fine_structure_splitting(1, 0.5, 1.0)
    for J, E in splitting.items():
        print(f"     J={J}: E={E:.2f}")
    
    # Selection rules
    print("\n5. Selection Rules:")
    # 2P_{3/2} -> 2S_{1/2}
    allowed, reason = transition_allowed((1, 0.5, 1.5), (0, 0.5, 0.5))
    print(f"   2P_{{3/2}} -> 2S_{{1/2}}: {reason}")
    
    # Forbidden: singlet to triplet
    allowed, reason = transition_allowed((0, 0, 0), (1, 1, 1))
    print(f"   1S0 -> 3P1: {reason}")
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="L_to_term_letter",
            description="Convert orbital angular momentum L to term symbol letter.",
            input_schema=[
            InputSchemaField(name="L", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="angular_momentum_magnitude",
            description="Calculate magnitude of angular momentum vector.",
            input_schema=[
            InputSchemaField(name="j", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="count_microstates",
            description="Count the number of possible microstates for an electron configuration.",
            input_schema=[
            InputSchemaField(name="orbital_type", type="number", required=True),
            InputSchemaField(name="n_electrons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="degeneracy",
            description="Calculate degeneracy of a term from J quantum number.",
            input_schema=[
            InputSchemaField(name="J", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fine_structure_splitting",
            description="Calculate fine structure splitting for a term.",
            input_schema=[
            InputSchemaField(name="L", type="number", required=True),
            InputSchemaField(name="S", type="number", required=True),
            InputSchemaField(name="zeta", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="hund_ground_state",
            description="Apply Hund's rules to determine ground state term symbol.",
            input_schema=[
            InputSchemaField(name="n_electrons", type="number", required=True),
            InputSchemaField(name="orbital_type", type="number", required=True),
            InputSchemaField(name="fill_fraction", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="multiplicity",
            description="Calculate multiplicity from total spin S.",
            input_schema=[
            InputSchemaField(name="S", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="perturbation_first_order_energy",
            description="Calculate first-order energy correction in perturbation theory.",
            input_schema=[
            InputSchemaField(name="psi0", type="number", required=True),
            InputSchemaField(name="H_prime", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="perturbation_first_order_wavefunction",
            description="Calculate first-order wavefunction correction.",
            input_schema=[
            InputSchemaField(name="psi0", type="number", required=True),
            InputSchemaField(name="H_prime", type="number", required=True),
            InputSchemaField(name="E0", type="number", required=True),
            InputSchemaField(name="unperturbed_energies", type="number", required=True),
            InputSchemaField(name="unperturbed_states", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="perturbation_second_order_energy",
            description="Calculate second-order energy correction.",
            input_schema=[
            InputSchemaField(name="psi0", type="number", required=True),
            InputSchemaField(name="H_prime", type="number", required=True),
            InputSchemaField(name="E0", type="number", required=True),
            InputSchemaField(name="unperturbed_energies", type="number", required=True),
            InputSchemaField(name="unperturbed_states", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="possible_J_values",
            description="Calculate possible total angular momentum J values.",
            input_schema=[
            InputSchemaField(name="L", type="number", required=True),
            InputSchemaField(name="S", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="possible_L_values",
            description="Calculate possible total orbital angular momentum L values.",
            input_schema=[
            InputSchemaField(name="l1", type="number", required=True),
            InputSchemaField(name="l2", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="possible_S_values",
            description="Calculate possible total spin S values for n electrons.",
            input_schema=[
            InputSchemaField(name="n_electrons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spin_orbit_coupling_energy",
            description="Calculate spin-orbit coupling energy contribution.",
            input_schema=[
            InputSchemaField(name="L", type="number", required=True),
            InputSchemaField(name="S", type="number", required=True),
            InputSchemaField(name="J", type="number", required=True),
            InputSchemaField(name="zeta", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="term_symbol",
            description="Construct atomic term symbol from quantum numbers.",
            input_schema=[
            InputSchemaField(name="L", type="number", required=True),
            InputSchemaField(name="S", type="number", required=True),
            InputSchemaField(name="J", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="transition_allowed",
            description="Check if a transition between two atomic terms is allowed.",
            input_schema=[
            InputSchemaField(name="term1", type="number", required=True),
            InputSchemaField(name="term2", type="number", required=True),
            InputSchemaField(name="strict", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="variational_energy",
            description="Calculate variational trial energy for a given trial wavefunction.",
            input_schema=[
            InputSchemaField(name="trial_function", type="number", required=True),
            InputSchemaField(name="hamiltonian_func", type="number", required=True),
            InputSchemaField(name="domain", type="number", required=False),
            InputSchemaField(name="normalize", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="variational_energy_with_param",
            description="Calculate variational energy for a trial function with a single parameter.",
            input_schema=[
            InputSchemaField(name="param_func", type="number", required=True),
            InputSchemaField(name="hamiltonian_func", type="number", required=True),
            InputSchemaField(name="param", type="number", required=True),
            InputSchemaField(name="domain", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="z_component",
            description="Calculate z-component of angular momentum.",
            input_schema=[
            InputSchemaField(name="j", type="number", required=True),
            InputSchemaField(name="m", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
