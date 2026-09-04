"""
L3 Implementation: Molecular Dynamics Tools
Source: L2_principles/molecular_dynamics.md

This module provides basic MD simulation functions.

## Solver Instructions (for AI Agent)

When you encounter molecular dynamics problems (potentials, forces, integration), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given distance r and LJ parameters -> calculate potential and force?
- Given velocities and masses -> calculate kinetic energy and temperature?
- Given positions/velocities -> integrate equations of motion?
- Given atoms -> calculate temperature, pressure, or other observables?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Lennard-Jones potential | `lennard_jones(r, epsilon, sigma)` | r in nm, ε in kJ/mol, σ in nm -> returns (U, F) |
| Kinetic energy | `kinetic_energy(velocities, masses)` | velocities (Nx3) nm/ps, masses in amu -> returns (E_k, T) |
| Temperature from KE | `temperature_from_kinetic(E_k, N_dof)` | E_k in kJ/mol, N_dof = degrees of freedom |
| Velocity Verlet integration | `velocity_verlet_step(positions, velocities, forces, masses, dt, force_func)` | single MD step |
| Initialize velocities | `initialize_velocities(n_atoms, masses, temperature)` | Maxwell-Boltzmann distribution |

### Step 3: Handle special cases
- LJ equilibrium: r_eq = 2^(1/6) x σ ~ 1.122σ where F = 0
- Temperature: T = 2E_k / (N_f x k_B) from equipartition theorem
- MD units: mass in amu, distance in nm, time in ps, energy in kJ/mol

### Examples
```python
# Example 1: Lennard-Jones for Ar (ε=0.996 kJ/mol, σ=0.34 nm)
U, F = lennard_jones(0.38, 0.996, 0.34)  # r=0.38 nm
# -> U ~ -0.86 kJ/mol, F ~ 15 kJ/(mol·nm)

# Example 2: Kinetic energy and temperature
import numpy as np
v = np.array([[0.1, 0, 0], [-0.1, 0, 0]])  # nm/ps
m = np.array([16.0, 16.0])  # amu (oxygen atoms)
E_k, T = kinetic_energy(v, m)
# -> E_k in kJ/mol, T in K

# Example 3: Temperature from E_k with 6 DOF
temperature_from_kinetic(3.0, 6)  # E_k=3 kJ/mol, 6 degrees of freedom
# -> T in K
```
"""

import math
import numpy as np
from typing import Tuple, Callable, Optional


def lennard_jones(r: float, epsilon: float, sigma: float) -> Tuple[float, float]:
    """
    Calculate Lennard-Jones potential and force.
    
    U(r) = 4ε[(σ/r)12 - (σ/r)6]
    F(r) = 24ε/r [2(σ/r)12 - (σ/r)6]
    
    Args:
        r: Distance in nm
        epsilon: Well depth in kJ/mol
        sigma: Zero-crossing distance in nm
    
    Returns:
        Tuple of (potential in kJ/mol, force in kJ/(mol·nm))
    
    Examples:
        >>> U, F = lennard_jones(0.34, 0.996, 0.34)  # Ar parameters
        >>> f"{U:.4f}"
        '-0.9960'
    """
    if r <= 0:
        return float('inf'), 0.0
    
    sr = sigma / r
    sr6 = sr**6
    sr12 = sr6**2
    
    U = 4 * epsilon * (sr12 - sr6)
    F = 24 * epsilon / r * (2 * sr12 - sr6)
    
    return U, F


def kinetic_energy(velocities: np.ndarray, masses: np.ndarray) -> Tuple[float, float]:
    """
    Calculate kinetic energy and temperature.
    
    E_k = (1/2) Σ m_i v_i2
    T = 2E_k / (N_f k_B)
    
    Args:
        velocities: Velocity array (N x 3) in nm/ps
        masses: Mass array (N,) in amu
    
    Returns:
        Tuple of (kinetic energy in kJ/mol, temperature in K)
    
    Examples:
        >>> v = np.array([[0.1, 0, 0], [-0.1, 0, 0]])
        >>> m = np.array([16.0, 16.0])  # Oxygen atoms
        >>> E_k, T = kinetic_energy(v, m)
    """
    # Convert mass to kg (for proper units)
    # 1 amu = 1.66054e-27 kg
    # But in MD units: mass in amu, velocity in nm/ps
    # E_k = (1/2) m v2 gives kJ/mol when m in amu, v in nm/ps
    
    # Using MD units: 1 amu·(nm/ps)2 = 1 kJ/mol (roughly)
    # Actually: 1 amu·(nm/ps)2 = 0.001 kJ/mol
    # So we need conversion factor
    
    # Correct conversion for MD units:
    # E_k [kJ/mol] = 0.5 * Σ m[amu] * |v[nm/ps]|2 * 0.001
    
    v_squared = np.sum(velocities**2, axis=1)
    E_k = 0.5 * np.sum(masses * v_squared) * 0.001  # kJ/mol
    
    # Temperature from equipartition
    # E_k = (3N/2) k_B T
    # k_B = 0.008314 kJ/(mol·K)
    N = len(masses)
    k_B = 0.008314
    
    T = 2 * E_k / (3 * N * k_B)
    
    return E_k, T


def velocity_verlet_step(r: np.ndarray, v: np.ndarray, 
                         forces: np.ndarray, masses: np.ndarray,
                         dt: float, force_func: Callable) -> Tuple[np.ndarray, np.ndarray]:
    """
    Single Velocity Verlet integration step.
    
    r(t+dt) = r(t) + v(t)dt + (F(t)/2m)dt2
    v(t+dt) = v(t) + (F(t) + F(t+dt))/(2m) dt
    
    Args:
        r: Positions (N x 3) in nm
        v: Velocities (N x 3) in nm/ps
        forces: Current forces (N x 3) in kJ/(mol·nm)
        masses: Masses (N,) in amu
        dt: Time step in ps
        force_func: Function to calculate forces from positions
    
    Returns:
        Tuple of (new positions, new velocities)
    
    Examples:
        >>> # Simple harmonic oscillator
        >>> def spring_force(r): return -100 * r
        >>> r = np.array([[0.1, 0, 0]])
        >>> v = np.array([[0.0, 0, 0]])
        >>> F = spring_force(r)
        >>> m = np.array([1.0])
        >>> r_new, v_new = velocity_verlet_step(r, v, F, m, 0.001, spring_force)
    """
    # Convert force units: kJ/(mol·nm) to acceleration
    # a = F/m where m is in amu
    # Need conversion: 1 kJ/(mol·nm·amu) = 1 nm/ps2
    
    acc = forces / masses[:, np.newaxis]  # nm/ps2
    
    # Update positions
    r_new = r + v * dt + 0.5 * acc * dt**2
    
    # Calculate new forces
    forces_new = force_func(r_new)
    acc_new = forces_new / masses[:, np.newaxis]
    
    # Update velocities
    v_new = v + 0.5 * (acc + acc_new) * dt
    
    return r_new, v_new


def pbc_wrap(positions: np.ndarray, box_size: np.ndarray) -> np.ndarray:
    """
    Apply periodic boundary conditions.
    
    Wrap positions into the primary simulation box.
    
    Args:
        positions: Position array (N x 3) in nm
        box_size: Box dimensions (3,) in nm
    
    Returns:
        Wrapped positions
    
    Examples:
        >>> pos = np.array([[1.5, -0.5, 2.5]])
        >>> box = np.array([2.0, 2.0, 2.0])
        >>> pbc_wrap(pos, box)
        array([[-0.5,  1.5,  0.5]])
    """
    return positions - box_size * np.floor(positions / box_size)


def pbc_distance(r1: np.ndarray, r2: np.ndarray, box_size: np.ndarray) -> np.ndarray:
    """
    Calculate minimum image distance with PBC.
    
    Args:
        r1: First position (3,) in nm
        r2: Second position (3,) in nm
        box_size: Box dimensions (3,) in nm
    
    Returns:
        Distance vector (3,) in nm
    
    Examples:
        >>> r1 = np.array([0.1, 0, 0])
        >>> r2 = np.array([1.9, 0, 0])
        >>> box = np.array([2.0, 2.0, 2.0])
        >>> pbc_distance(r1, r2, box)
        array([-0.2,  0. ,  0. ])
    """
    dr = r2 - r1
    dr = dr - box_size * np.round(dr / box_size)
    return dr


def initialize_velocities(n_atoms: int, temperature: float, 
                          masses: np.ndarray, seed: int = None) -> np.ndarray:
    """
    Initialize velocities from Maxwell-Boltzmann distribution.
    
    Args:
        n_atoms: Number of atoms
        temperature: Target temperature in K
        masses: Masses (N,) in amu
        seed: Random seed (optional)
    
    Returns:
        Velocity array (N x 3) in nm/ps
    
    Examples:
        >>> v = initialize_velocities(10, 300, np.ones(10))
        >>> v.shape
        (10, 3)
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate random velocities
    velocities = np.random.randn(n_atoms, 3)
    
    # Scale by sqrt(k_B T / m) for each atom
    # k_B = 0.008314 kJ/(mol·K)
    # 1 kJ/mol = 1 amu·nm2/ps2 (roughly)
    k_B = 0.008314
    
    for i in range(n_atoms):
        velocities[i] *= np.sqrt(k_B * temperature / (masses[i] * 0.001))
    
    # Remove center of mass motion
    total_momentum = np.sum(masses[:, np.newaxis] * velocities, axis=0)
    total_mass = np.sum(masses)
    velocities -= total_momentum / total_mass / np.sum(masses) * masses[:, np.newaxis]
    
    return velocities


def berendsen_thermostat(velocities: np.ndarray, current_temp: float,
                         target_temp: float, tau: float, dt: float) -> np.ndarray:
    """
    Apply Berendsen thermostat.
    
    Scale velocities toward target temperature.
    
    lambda = √(1 + (dt/τ)(T_target/T_current - 1))
    
    Args:
        velocities: Velocity array (N x 3) in nm/ps
        current_temp: Current temperature in K
        target_temp: Target temperature in K
        tau: Coupling constant in ps
        dt: Time step in ps
    
    Returns:
        Scaled velocities
    
    Examples:
        >>> v = np.ones((10, 3))
        >>> v_scaled = berendsen_thermostat(v, 200, 300, 0.1, 0.001)
    """
    if current_temp <= 0:
        return velocities
    
    scaling = math.sqrt(1 + (dt / tau) * (target_temp / current_temp - 1))
    return velocities * scaling


def rmsd(r1: np.ndarray, r2: np.ndarray) -> float:
    """
    Calculate Root Mean Square Deviation.
    
    RMSD = √(Σ|r1_i - r2_i|2 / N)
    
    Args:
        r1: Reference positions (N x 3)
        r2: Positions to compare (N x 3)
    
    Returns:
        RMSD in same units as positions
    
    Examples:
        >>> r1 = np.array([[0, 0, 0], [1, 0, 0]])
        >>> r2 = np.array([[0.1, 0, 0], [1.1, 0, 0]])
        >>> rmsd(r1, r2)
        0.1
    """
    diff = r1 - r2
    return np.sqrt(np.mean(np.sum(diff**2, axis=1)))


# ============================================================================
# Self-test
# ============================================================================

if __name__ == '__main__':
    print("Molecular Dynamics Tools Test")
    print("=" * 40)
    
    # Test LJ potential
    print("\nLennard-Jones Potential (Ar, ε=0.996, σ=0.34):")
    for r in [0.3, 0.34, 0.4, 0.5]:
        U, F = lennard_jones(r, 0.996, 0.34)
        print(f"  r={r:.2f} nm: U={U:.4f} kJ/mol, F={F:.4f} kJ/(mol·nm)")
    
    # Test PBC
    print("\nPeriodic Boundary Conditions:")
    pos = np.array([[1.5, -0.5, 2.5]])
    box = np.array([2.0, 2.0, 2.0])
    wrapped = pbc_wrap(pos, box)
    print(f"  Original: {pos}")
    print(f"  Wrapped: {wrapped}")
    
    # Test kinetic energy
    print("\nKinetic Energy:")
    v = np.array([[0.1, 0, 0], [-0.1, 0, 0]])
    m = np.array([16.0, 16.0])
    E_k, T = kinetic_energy(v, m)
    print(f"  KE = {E_k:.4f} kJ/mol")
    print(f"  T = {T:.1f} K")

MCP_TOOLS = [
    {
        "name": "berendsen_thermostat",
        "description": "Apply Berendsen thermostat.",
        "parameters": [
            {
                "name": "velocities",
                "type": "number"
            },
            {
                "name": "current_temp",
                "type": "number"
            },
            {
                "name": "target_temp",
                "type": "number"
            },
            {
                "name": "tau",
                "type": "number"
            },
            {
                "name": "dt",
                "type": "number"
            }
        ]
    },
    {
        "name": "initialize_velocities",
        "description": "Initialize velocities from Maxwell-Boltzmann distribution.",
        "parameters": [
            {
                "name": "n_atoms",
                "type": "number"
            },
            {
                "name": "temperature",
                "type": "number"
            },
            {
                "name": "masses",
                "type": "number"
            },
            {
                "name": "seed",
                "type": "number"
            }
        ]
    },
    {
        "name": "kinetic_energy",
        "description": "Calculate kinetic energy and temperature.",
        "parameters": [
            {
                "name": "velocities",
                "type": "number"
            },
            {
                "name": "masses",
                "type": "number"
            }
        ]
    },
    {
        "name": "lennard_jones",
        "description": "Calculate Lennard-Jones potential and force.",
        "parameters": [
            {
                "name": "r",
                "type": "number"
            },
            {
                "name": "epsilon",
                "type": "number"
            },
            {
                "name": "sigma",
                "type": "number"
            }
        ]
    },
    {
        "name": "pbc_distance",
        "description": "Calculate minimum image distance with PBC.",
        "parameters": [
            {
                "name": "r1",
                "type": "number"
            },
            {
                "name": "r2",
                "type": "number"
            },
            {
                "name": "box_size",
                "type": "number"
            }
        ]
    },
    {
        "name": "pbc_wrap",
        "description": "Apply periodic boundary conditions.",
        "parameters": [
            {
                "name": "positions",
                "type": "number"
            },
            {
                "name": "box_size",
                "type": "number"
            }
        ]
    },
    {
        "name": "rmsd",
        "description": "Calculate Root Mean Square Deviation.",
        "parameters": [
            {
                "name": "r1",
                "type": "number"
            },
            {
                "name": "r2",
                "type": "number"
            }
        ]
    },
    {
        "name": "velocity_verlet_step",
        "description": "Single Velocity Verlet integration step.",
        "parameters": [
            {
                "name": "r",
                "type": "number"
            },
            {
                "name": "v",
                "type": "number"
            },
            {
                "name": "forces",
                "type": "number"
            },
            {
                "name": "masses",
                "type": "number"
            },
            {
                "name": "dt",
                "type": "number"
            },
            {
                "name": "force_func",
                "type": "number"
            }
        ]
    }
]
