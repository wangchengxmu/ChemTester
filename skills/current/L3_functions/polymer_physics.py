"""
Polymer Physics - L3 Implementation

Chain models and viscoelasticity calculations.
Source: Polymer Physics (Steimel), Ch3, Ch13

## Solver Instructions (for AI Agent)

When you encounter polymer physics problems (chain dimensions, viscoelasticity, polymer solution properties), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Chain dimensions**: Given N (segments), l (segment length), or bond geometry -> find <R2>, Rg, C∞, persistence length
- **End-to-end distribution**: Given R (distance) and <R2> -> find P(R)
- **Solution properties**: Given Mw, Rg, solvent conditions -> find [η], intrinsic viscosity
- **Viscoelasticity**: Given moduli or relaxation times -> find creep compliance, stress relaxation

### Step 2: Choose the correct function
- `freely_jointed_chain_R2(N, l)` -> Mean squared end-to-end distance <R2> = Nl2
- `radius_of_gyration(R2)` -> Rg = √(<R2>/6)
- `characteristic_ratio(R2, N, l)` -> C∞ = <R2>/(Nl2)
- `persistence_length(bond_length, bond_angle)` -> Lp = l/(1-cos(θ))
- `gaussian_distribution(R, R2)` -> P(R) for end-to-end distance
- `entanglement_molecular_weight(N_e, M_0)` -> Me = N_e x M_0

### Step 3: Handle special cases
- Bond angle must be in radians (convert from degrees if needed)
- For real chains vs ideal chains: C∞ > 1 indicates chain stiffness
- Gaussian distribution only valid when R << contour length (Nl)

### Examples
1. **Freely jointed chain**: N=1000 segments, l=2.5 Å
   -> `freely_jointed_chain_R2(1000, 2.5e-10)` -> <R2> = 6.25e-14 m2
   -> `radius_of_gyration(6.25e-14)` -> Rg ~ 3.23e-7 m = 32.3 nm

2. **Persistence length**: C-C bond length 1.54 Å, tetrahedral angle θ=109.5deg=1.911 rad
   -> `persistence_length(1.54e-10, 1.911)` -> Lp ~ 1.54e-10/(1-cos(1.911)) ~ 1.54e-10/1.334 ~ 1.15 Å

3. **Characteristic ratio**: PE chain with <R2>=4.5e-17 m2, N=5000, l=1.54e-10 m
   -> `characteristic_ratio(4.5e-17, 5000, 1.54e-10)` -> C∞ = 4.5e-17/5000/(1.54e-10)2 ~ 3.79
"""

import math
from typing import Tuple


def freely_jointed_chain_R2(N: int, l: float) -> float:
    """
    Calculate mean squared end-to-end distance for freely jointed chain.
    
    <R2> = Nl2
    
    Args:
        N: Number of segments
        l: Segment length
    
    Returns:
        Mean squared end-to-end distance
    """
    return N * l**2


def radius_of_gyration(R2: float) -> float:
    """
    Calculate radius of gyration from mean squared end-to-end distance.
    
    Rg = √(<R2>/6)
    
    Args:
        R2: Mean squared end-to-end distance
    
    Returns:
        Radius of gyration
    """
    return math.sqrt(R2 / 6)


def characteristic_ratio(R2: float, N: int, l: float) -> float:
    """
    Calculate characteristic ratio.
    
    C∞ = <R2>/(Nl2)
    
    Args:
        R2: Mean squared end-to-end distance
        N: Number of segments
        l: Segment length
    
    Returns:
        Characteristic ratio
    """
    return R2 / (N * l**2)


def persistence_length(bond_length: float, bond_angle: float) -> float:
    """
    Calculate persistence length from bond geometry.
    
    Lp = l/(1-cos(θ))
    
    Args:
        bond_length: Bond length
        bond_angle: Bond angle in radians
    
    Returns:
        Persistence length
    """
    return bond_length / (1 - math.cos(bond_angle))


def gaussian_distribution(R: float, R2: float) -> float:
    """
    Gaussian probability distribution for end-to-end distance.
    
    P(R) = (3/(2pi<R2>))^(3/2) * exp(-3R2/(2<R2>))
    
    Args:
        R: End-to-end distance
        R2: Mean squared end-to-end distance
    
    Returns:
        Probability density
    """
    prefactor = (3 / (2 * math.pi * R2))**1.5
    exponent = -3 * R**2 / (2 * R2)
    return prefactor * math.exp(exponent)


def maxwell_relaxation(G0: float, t: float, tau: float) -> float:
    """
    Maxwell model stress relaxation modulus.
    
    G(t) = G0 * exp(-t/τ)
    
    Args:
        G0: Initial modulus
        t: Time
        tau: Relaxation time
    
    Returns:
        Relaxation modulus
    """
    return G0 * math.exp(-t / tau)


def complex_modulus(G_prime: float, G_double_prime: float) -> Tuple[float, float]:
    """
    Calculate magnitude and phase of complex modulus.
    
    |G*| = √(G'2 + G''2)
    tan(delta) = G''/G'
    
    Args:
        G_prime: Storage modulus
        G_double_prime: Loss modulus
    
    Returns:
        (magnitude, tan_delta)
    """
    magnitude = math.sqrt(G_prime**2 + G_double_prime**2)
    tan_delta = G_double_prime / G_prime if G_prime > 0 else float('inf')
    return magnitude, tan_delta


def complex_viscosity(G_prime: float, G_double_prime: float, omega: float) -> float:
    """
    Calculate complex viscosity.
    
    η* = √(G'2 + G''2)/ω
    
    Args:
        G_prime: Storage modulus
        G_double_prime: Loss modulus
        omega: Angular frequency
    
    Returns:
        Complex viscosity magnitude
    """
    return math.sqrt(G_prime**2 + G_double_prime**2) / omega


def wlf_shift(T: float, T_ref: float, C1: float = 17.44, C2: float = 51.6) -> float:
    """
    Calculate WLF shift factor.
    
    log(aT) = -C1(T - Tref)/(C2 + T - Tref)
    
    Args:
        T: Temperature
        T_ref: Reference temperature
        C1: WLF constant (default 17.44)
        C2: WLF constant (default 51.6 K)
    
    Returns:
        Shift factor (log scale)
    """
    return -C1 * (T - T_ref) / (C2 + (T - T_ref))


def arrhenius_shift(T: float, T_ref: float, Ea: float, R: float = 8.314) -> float:
    """
    Calculate Arrhenius shift factor.
    
    aT = exp[(Ea/R)(1/T - 1/Tref)]
    
    Args:
        T: Temperature (K)
        T_ref: Reference temperature (K)
        Ea: Activation energy (J/mol)
        R: Gas constant (J/mol·K)
    
    Returns:
        Shift factor
    """
    return math.exp((Ea / R) * (1/T - 1/T_ref))


# TODO: Implement for Pass-3
# - flory_huggins_chi() - Chi parameter from solubility parameters
# - sec_molecular_weight() - MW from SEC retention time
# - reptation_time() - Terminal relaxation from reptation model
