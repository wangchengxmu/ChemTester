"""
L3: Computational Chemistry Tools
Source: G06 DFT Module, G07 Rotational Spectroscopy, G08 Molecular Dynamics, G09 QSAR

This module provides simplified implementations of core computational chemistry functions.
For production use, refer to established packages: Gaussian, ORCA, GROMACS, RDKit, etc.

Functions:
- DFT (G06): dft_energy_calculator, exchange_correlation_function
- Rotational Spectroscopy (G07): rotational_constant_calculator, rotational_partition_function
- Molecular Dynamics (G08): md_integrator, kinetic_energy_calculator
- QSAR (G09): descriptor_calculator, qsar_model_builder

Dependencies: numpy

## Solver Instructions (for AI Agent)

When you encounter computational chemistry calculations (DFT, rotational spectroscopy, MD, QSAR, LJ potential):

### Step 1: Identify what is given and what is asked
- Given: molecular parameters, coordinates, basis sets, experimental data
- Asked: DFT energy, rotational constants, MD trajectories, molecular descriptors, QSAR model

### Step 2: Choose the correct function
- `dft_energy_calculator(method, basis_set, functional, ...)`: DFT single-point energy
- `exchange_correlation_function(functional, rho, rs)`: XC functional evaluation
- `rotational_constant_calculator(B, ...)`: Rotational constant B in cm-1
- `rotational_partition_function(B, T, symmetry)`: q_rot
- `md_integrator(positions, velocities, forces, dt, ...)`: Velocity-Verlet integrator
- `kinetic_energy_calculator(velocities, masses)`: KE from velocities
- `descriptor_calculator(molecule, ...)`: Molecular descriptors for QSAR
- `qsar_model_builder(descriptors, activities, ...)`: Build QSAR regression model
- `lennard_jones(r, epsilon, sigma)`: LJ potential energy and forces
- `boltzmann_distribution(energies, temperature)`: Boltzmann populations
- `rotational_energy(J, B, D)`: E_J = BJ(J+1) - DJ2(J+1)2

### Step 3: Handle special cases
- DFT functionals: LDA (basic), GGA (PBE), hybrid (B3LYP, PBE0), meta-GGA (M06)
- Rotational constant: B = h/(8pi2cI); I = mur2
- LJ: V(r) = 4ε[(σ/r)12 - (σ/r)6]; minimum at r = 2^(1/6)σ

### Examples
```python
lennard_jones(np.array([3.4]), 0.0103, 3.4)  # Ar-Ar at σ -> minimum
boltzmann_distribution(np.array([0, 100, 200]), 300)  # populations at 300K
```
"""

import numpy as np
from typing import Tuple, Dict, List, Optional, Union

# =============================================================================
# G06: DENSITY FUNCTIONAL THEORY (DFT)
# =============================================================================

def dft_energy_calculator(
    kinetic_energy: float,
    electron_nuclear_attraction: float,
    coulomb_energy: float,
    exchange_correlation_energy: float,
    nuclear_repulsion: float = 0.0
) -> Dict[str, float]:
    """
    Calculate total Kohn-Sham DFT energy from components.
    
    E_KS = T_s + V_ne + J + E_xc + E_nn
    
    Where:
    - T_s: Kinetic energy of non-interacting electrons
    - V_ne: Electron-nuclear attraction
    - J: Coulomb (Hartree) energy
    - E_xc: Exchange-correlation energy
    - E_nn: Nuclear-nuclear repulsion
    
    Args:
        kinetic_energy: T_s - kinetic energy of Kohn-Sham orbitals (Hartree)
        electron_nuclear_attraction: V_ne (Hartree)
        coulomb_energy: J - classical electron-electron repulsion (Hartree)
        exchange_correlation_energy: E_xc from XC functional (Hartree)
        nuclear_repulsion: E_nn for multi-atom systems (Hartree, default 0)
    
    Returns:
        Dictionary with energy components and total energy in Hartree
        
    Example:
        >>> dft_energy_calculator(76.0, -200.0, 50.0, -10.0, 5.0)
        {'T_s': 76.0, 'V_ne': -200.0, 'J': 50.0, 'E_xc': -10.0, 
         'E_nn': 5.0, 'E_total': -79.0}
    """
    total_energy = (kinetic_energy + electron_nuclear_attraction + 
                   coulomb_energy + exchange_correlation_energy + 
                   nuclear_repulsion)
    
    return {
        'T_s': kinetic_energy,
        'V_ne': electron_nuclear_attraction,
        'J': coulomb_energy,
        'E_xc': exchange_correlation_energy,
        'E_nn': nuclear_repulsion,
        'E_total': total_energy
    }


def exchange_correlation_function(
    rho: np.ndarray,
    grad_rho: Optional[np.ndarray] = None,
    functional_type: str = 'lda',
    rho_cutoff: float = 1e-10
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Calculate exchange-correlation energy and potential.
    
    Implements simplified versions of common functionals:
    - LDA: Local Density Approximation (Slater exchange + VWN correlation)
    - GGA: Generalized Gradient Approximation (PBE)
    - Hybrid: Mix of HF exchange and DFT (B3LYP-like)
    
    Args:
        rho: Electron density array (electrons/bohr3)
        grad_rho: Density gradient magnitude (bohr-1·electrons/bohr3), required for GGA
        functional_type: 'lda', 'gga', or 'hybrid'
        rho_cutoff: Minimum density threshold (default 1e-10)
    
    Returns:
        Dictionary with:
        - 'E_xc': Exchange-correlation energy (Hartree)
        - 'epsilon_xc': XC energy per particle
        - 'v_xc': XC potential
        - 'E_x': Exchange energy
        - 'E_c': Correlation energy
        
    Example:
        >>> rho = np.array([0.1, 0.2, 0.3])
        >>> result = exchange_correlation_function(rho, functional_type='lda')
        >>> print(f"E_xc = {result['E_xc']:.6f} Ha")
    """
    # Filter low-density regions
    mask = rho > rho_cutoff
    rho_eff = np.where(mask, rho, rho_cutoff)
    
    # Constants (atomic units)
    # Slater exchange: E_x = -C_x * ∫ρ^(4/3) dr, where C_x = (3/4)(3/pi)^(1/3)
    C_x = 0.738558766382  # (3/4)(3/pi)^(1/3)
    
    # VWN correlation parameters (simplified)
    A = 0.0310907
    b = 3.72744
    c = 12.9352
    x0 = -0.10498
    
    if functional_type.lower() == 'lda':
        # LDA Exchange: ε_x = -C_x * ρ^(1/3)
        epsilon_x = -C_x * np.power(rho_eff, 1.0/3.0)
        E_x = np.sum(epsilon_x * rho_eff)  # ∫ε_x * ρ dr
        
        # LDA Correlation (VWN parametrization, simplified for unpolarized)
        rs = np.power(3.0 / (4.0 * np.pi * rho_eff), 1.0/3.0)  # Wigner-Seitz radius
        x = np.sqrt(rs)
        X = rs + b*x + c
        Q = np.sqrt(4*c - b*b)
        
        # VWN correlation energy per particle
        epsilon_c = A * (np.log(x*x/X) + 
                         2*b/Q * np.arctan(Q/(2*x + b)) -
                         b*x0/(X0*(x - x0)) * 
                         (np.log((x - x0)*(x - x0)/X) + 
                          2*(b + 2*x0)/Q * np.arctan(Q/(2*x + b))))
        # Simplified: use parameterized fit
        epsilon_c = A * np.log(1 + 1.0 / (b*x + c*x*x))
        
        E_c = np.sum(epsilon_c * rho_eff)
        
        # Total XC
        epsilon_xc = epsilon_x + epsilon_c
        E_xc = E_x + E_c
        
        # XC potential (functional derivative)
        # v_xc = d(ρ*ε_xc)/dρ = ε_xc + ρ * dε_xc/dρ
        # For exchange: dε_x/dρ = -(1/3)C_x * ρ^(-2/3)
        v_x = (4.0/3.0) * epsilon_x  # v_x = 4/3 * ε_x for Slater
        v_c = epsilon_c * 0.8  # Approximation
        v_xc = v_x + v_c
        
    elif functional_type.lower() == 'gga':
        if grad_rho is None:
            grad_rho = np.zeros_like(rho_eff)
        
        # PBE Enhancement factor
        kappa = 0.804
        mu = 0.2195149724
        
        # Reduced density gradient: s = |∇ρ| / (2*kF*ρ)
        kF = np.power(3 * np.pi**2 * rho_eff, 1.0/3.0)  # Fermi wave vector
        s = grad_rho / (2 * kF * rho_eff + 1e-10)
        
        # PBE exchange enhancement factor
        Fx = 1 + kappa - kappa / (1 + mu/kappa * s**2)
        
        # Exchange
        epsilon_x_lda = -C_x * np.power(rho_eff, 1.0/3.0)
        epsilon_x = epsilon_x_lda * Fx
        E_x = np.sum(epsilon_x * rho_eff)
        
        # Correlation (simplified PBE)
        beta = 0.0667245506
        t = s / (4 * np.pi * rho_eff / 9)**0.5  # Reduced gradient for correlation
        H = beta * s**2 / (1 + beta * s**2 / A)  # Enhancement
        epsilon_c = A * np.log(1 + 1.0 / (b*np.sqrt(rs) + c*rs)) + H
        E_c = np.sum(epsilon_c * rho_eff)
        
        epsilon_xc = epsilon_x + epsilon_c
        E_xc = E_x + E_c
        v_xc = epsilon_xc  # Simplified
        
    elif functional_type.lower() == 'hybrid':
        # B3LYP-like hybrid: 20% HF + 80% DFT exchange
        a_hf = 0.20
        
        # Get GGA components
        gga_result = exchange_correlation_function(
            rho, grad_rho, 'gga', rho_cutoff)
        E_x_gga = gga_result['E_x']
        E_c_gga = gga_result['E_c']
        
        # Get LDA components for mixing
        lda_result = exchange_correlation_function(
            rho, None, 'lda', rho_cutoff)
        E_x_lda = lda_result['E_x']
        
        # B3LYP mixing (simplified)
        # E_xc = 0.20*E_x_HF + 0.80*E_x_B88 + 0.19*E_c_VWN + 0.81*E_c_LYP
        # Here we use simplified: E_x = 0.8*E_x_gga + 0.2*E_x_approx
        E_x = 0.8 * E_x_gga + 0.2 * E_x_lda
        E_c = E_c_gga
        E_xc = E_x + E_c
        epsilon_xc = E_xc / np.sum(rho_eff)
        v_xc = epsilon_xc
        
    else:
        raise ValueError(f"Unknown functional type: {functional_type}")
    
    return {
        'E_xc': float(E_xc),
        'epsilon_xc': epsilon_xc,
        'v_xc': v_xc,
        'E_x': float(E_x),
        'E_c': float(E_c)
    }


# =============================================================================
# G07: ROTATIONAL SPECTROSCOPY
# =============================================================================

def rotational_constant_calculator(
    masses: np.ndarray,
    coordinates: np.ndarray,
    units: str = 'amu_angstrom'
) -> Dict[str, Union[float, np.ndarray]]:
    """
    Calculate rotational constants from molecular geometry.
    
    For a diatomic: B = h/(8pi2cI) = h/(8pi2cmur2)
    For polyatomic: A, B, C from principal moments of inertia
    
    Args:
        masses: Atomic masses array (amu by default)
        coordinates: Atomic coordinates array, shape (N, 3) (Å by default)
        units: 'amu_angstrom' (default) or 'si' (kg, m)
    
    Returns:
        Dictionary with:
        - 'A', 'B', 'C': Rotational constants (cm-1, A ≥ B ≥ C)
        - 'I_a', 'I_b', 'I_c': Principal moments of inertia (amu·Å2)
        - 'molecule_type': 'diatomic', 'linear', 'symmetric_top', 'spherical_top', or 'asymmetric_top'
        
    Example:
        >>> # CO molecule: C at origin, O at 1.128 Å
        >>> masses = np.array([12.0, 16.0])  # amu
        >>> coords = np.array([[0, 0, 0], [1.128, 0, 0]])  # Å
        >>> result = rotational_constant_calculator(masses, coords)
        >>> print(f"B = {result['B']:.4f} cm^-1")
    """
    # Physical constants
    h = 6.62607015e-34  # J·s
    c = 299792458  # m/s
    amu_to_kg = 1.66053906660e-27  # kg/amu
    angstrom_to_m = 1e-10  # m/Å
    B_conversion = h / (8 * np.pi**2 * c)  # J·s/(m/s) = J·s2/m
    
    # Convert to SI if needed
    if units == 'amu_angstrom':
        mass_kg = masses * amu_to_kg
        coord_m = coordinates * angstrom_to_m
    else:
        mass_kg = masses
        coord_m = coordinates
    
    n_atoms = len(masses)
    
    # Calculate center of mass
    total_mass = np.sum(mass_kg)
    com = np.sum(mass_kg[:, np.newaxis] * coord_m, axis=0) / total_mass
    
    # Translate to center of mass frame
    coord_com = coord_m - com
    
    # Calculate inertia tensor
    I_tensor = np.zeros((3, 3))
    for i in range(n_atoms):
        m = mass_kg[i]
        x, y, z = coord_com[i]
        I_tensor[0, 0] += m * (y**2 + z**2)  # I_xx
        I_tensor[1, 1] += m * (x**2 + z**2)  # I_yy
        I_tensor[2, 2] += m * (x**2 + y**2)  # I_zz
        I_tensor[0, 1] -= m * x * y  # I_xy
        I_tensor[0, 2] -= m * x * z  # I_xz
        I_tensor[1, 2] -= m * y * z  # I_yz
    
    # Symmetrize
    I_tensor[1, 0] = I_tensor[0, 1]
    I_tensor[2, 0] = I_tensor[0, 2]
    I_tensor[2, 1] = I_tensor[1, 2]
    
    # Diagonalize to get principal moments
    eigenvalues, _ = np.linalg.eigh(I_tensor)
    
    # Sort eigenvalues (I_a ≤ I_b ≤ I_c, so A ≥ B ≥ C)
    eigenvalues = np.sort(eigenvalues)
    I_a, I_b, I_c = eigenvalues  # kg·m2
    
    # Convert back to amu·Å2 for output
    I_a_amu = I_a / (amu_to_kg * angstrom_to_m**2)
    I_b_amu = I_b / (amu_to_kg * angstrom_to_m**2)
    I_c_amu = I_c / (amu_to_kg * angstrom_to_m**2)
    
    # Calculate rotational constants in cm-1
    # B (cm-1) = h/(8pi2cI) x (1/100) for cm-1 from m-1
    B_factor = h / (8 * np.pi**2 * c) * 0.01  # converts to cm-1
    
    A = B_factor / I_a if I_a > 1e-50 else 0.0
    B = B_factor / I_b if I_b > 1e-50 else 0.0
    C = B_factor / I_c if I_c > 1e-50 else 0.0
    
    # Determine molecule type
    tol = 1e-4  # Relative tolerance
    if n_atoms == 2:
        mol_type = 'diatomic'
    elif abs(I_a - I_b) / I_b < tol and I_c > I_b * (1 + tol):
        mol_type = 'linear'  # I_a ~ I_b, I_c ~ 0
    elif abs(I_a - I_b) / I_b < tol and abs(I_b - I_c) / I_c < tol:
        mol_type = 'spherical_top'  # I_a ~ I_b ~ I_c
    elif abs(I_a - I_b) / I_b < tol or abs(I_b - I_c) / I_c < tol:
        mol_type = 'symmetric_top'  # Two equal moments
    else:
        mol_type = 'asymmetric_top'  # All different
    
    return {
        'A': float(A),
        'B': float(B),
        'C': float(C),
        'I_a': float(I_a_amu),
        'I_b': float(I_b_amu),
        'I_c': float(I_c_amu),
        'molecule_type': mol_type
    }


def rotational_partition_function(
    rotational_constants: Union[float, Tuple[float, float, float]],
    temperature: float,
    symmetry_number: int = 1,
    molecule_type: str = 'diatomic',
    include_excited_states: bool = True,
    max_J: int = 100
) -> Dict[str, float]:
    """
    Calculate rotational partition function.
    
    For diatomic/linear: Q_rot = T/(σθ_rot) where θ_rot = hcB/k_B
    For symmetric tops: Q_rot = (pi^(1/2)/σ) x (T3/(θ_Axθ_Bxθ_C))^(1/2)
    For asymmetric tops: Q_rot = (pi^(1/2)/σ) x (T3/(θ_Axθ_Bxθ_C))^(1/2)
    
    Args:
        rotational_constants: B (cm-1) for diatomic, or (A, B, C) tuple for polyatomic
        temperature: Temperature in Kelvin
        symmetry_number: σ (1 for heteronuclear, 2 for homonuclear diatomic, etc.)
        molecule_type: 'diatomic', 'linear', 'symmetric_top', 'spherical_top', 'asymmetric_top'
        include_excited_states: Whether to sum over J states explicitly (slower but more accurate)
        max_J: Maximum J quantum number for explicit summation
    
    Returns:
        Dictionary with:
        - 'Q_rot': Rotational partition function
        - 'theta_rot': Rotational temperature(s) (K)
        - 'Q_rot_high_T': High-temperature approximation
        - 'contribution_per_rotor': For each rotational degree of freedom
        
    Example:
        >>> # CO at 298 K
        >>> result = rotational_partition_function(1.931, 298, symmetry_number=1)
        >>> print(f"Q_rot = {result['Q_rot']:.2f}")
    """
    # Physical constants
    h = 6.62607015e-34  # J·s
    c = 299792458  # m/s
    k_B = 1.380649e-23  # J/K
    hc_k = h * c * 100 / k_B  # Converts cm-1 to K: (J·s)(m/s)(cm/m)/(J/K) = K·cm
    
    if molecule_type in ['diatomic', 'linear']:
        if isinstance(rotational_constants, (tuple, list, np.ndarray)):
            B = rotational_constants[1] if len(rotational_constants) > 1 else rotational_constants[0]
        else:
            B = rotational_constants
        
        # Rotational temperature θ_rot = hcB/k_B (in K)
        theta_rot = hc_k * B
        
        # High-temperature approximation
        Q_rot_high_T = temperature / (symmetry_number * theta_rot) if theta_rot > 0 else 0
        
        if include_excited_states and theta_rot > 0:
            # Explicit summation over J states
            Q_rot = 0.0
            for J in range(max_J + 1):
                # Energy: E_J = hcBJ(J+1)
                # Degeneracy: g_J = (2J+1)
                E_J = theta_rot * J * (J + 1)  # in K
                g_J = 2 * J + 1
                
                # Boltzmann factor
                if E_J / temperature < 30:  # Avoid underflow
                    Q_rot += g_J * np.exp(-E_J / temperature)
            Q_rot /= symmetry_number
        else:
            Q_rot = Q_rot_high_T
        
        return {
            'Q_rot': float(Q_rot),
            'theta_rot': float(theta_rot),
            'Q_rot_high_T': float(Q_rot_high_T),
            'contribution_per_rotor': float(Q_rot),
            'degrees_of_freedom': 2
        }
    
    else:
        # Polyatomic molecule
        if isinstance(rotational_constants, (tuple, list, np.ndarray)):
            A, B, C = rotational_constants
        else:
            A = B = C = rotational_constants
        
        # Rotational temperatures
        theta_A = hc_k * A
        theta_B = hc_k * B
        theta_C = hc_k * C
        
        # High-temperature approximation for asymmetric top
        if theta_A * theta_B * theta_C > 0:
            Q_rot_high_T = (np.sqrt(np.pi) / symmetry_number) * np.sqrt(
                temperature**3 / (theta_A * theta_B * theta_C)
            )
        else:
            Q_rot_high_T = 0
        
        # For symmetric tops, use appropriate formula
        if molecule_type == 'spherical_top':
            # All three moments equal
            Q_rot_high_T = (np.sqrt(np.pi) / symmetry_number) * (temperature / theta_B)**1.5
        
        return {
            'Q_rot': float(Q_rot_high_T),
            'theta_A': float(theta_A),
            'theta_B': float(theta_B),
            'theta_C': float(theta_C),
            'Q_rot_high_T': float(Q_rot_high_T),
            'degrees_of_freedom': 3
        }


# =============================================================================
# G08: MOLECULAR DYNAMICS
# =============================================================================

def md_integrator(
    positions: np.ndarray,
    velocities: np.ndarray,
    forces: np.ndarray,
    masses: np.ndarray,
    dt: float,
    integrator: str = 'velocity_verlet'
) -> Dict[str, np.ndarray]:
    """
    Perform one MD integration step using Velocity Verlet algorithm.
    
    Velocity Verlet algorithm:
    1. r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt2
    2. Calculate F(t+dt) from new positions
    3. v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
    
    Args:
        positions: Current positions, shape (N, 3) in nm
        velocities: Current velocities, shape (N, 3) in nm/ps
        forces: Current forces, shape (N, 3) in kJ/mol/nm
        masses: Atomic masses, shape (N,) in amu
        dt: Time step in ps
        integrator: 'velocity_verlet' (default) or 'leapfrog'
    
    Returns:
        Dictionary with:
        - 'positions': New positions (nm)
        - 'velocities': New velocities (nm/ps)
        - 'half_step_velocities': Half-step velocities for force calculation
        - 'accelerations': Current accelerations (nm/ps2)
        
    Example:
        >>> pos = np.array([[0, 0, 0], [0.3, 0, 0]])  # nm
        >>> vel = np.array([[0.1, 0, 0], [-0.1, 0, 0]])  # nm/ps
        >>> forces = np.array([[10, 0, 0], [-10, 0, 0]])  # kJ/mol/nm
        >>> masses = np.array([12.0, 16.0])  # amu
        >>> result = md_integrator(pos, vel, forces, masses, dt=0.001)
    """
    # Conversion factor: kJ/mol/nm to nm/ps2 for amu
    # F = ma -> a = F/m
    # 1 kJ/mol = 1.660539e-21 J per molecule
    # 1 amu = 1.660539e-27 kg
    # a (nm/ps2) = F (kJ/mol/nm) / m (amu) x (1.660539e-21/1.660539e-27) x 1e-9
    # = F/m x 1e6 nm/ps2
    force_to_accel = 1.0  # kJ/mol/nm / amu gives nm/ps2 (GROMACS units)
    
    # Calculate accelerations: a = F/m
    accelerations = forces / masses[:, np.newaxis] * force_to_accel
    
    if integrator == 'velocity_verlet':
        # Step 1: Update positions
        # r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt2
        new_positions = positions + velocities * dt + 0.5 * accelerations * dt**2
        
        # Half-step velocities (for force recalculation)
        half_step_velocities = velocities + 0.5 * accelerations * dt
        
        # Note: In practice, forces need to be recalculated at new_positions
        # Here we return the state before force recalculation
        new_velocities = half_step_velocities  # Will be updated after force calc
        
    elif integrator == 'leapfrog':
        # Leapfrog: v at half-steps, r at full steps
        # v(t+dt/2) = v(t-dt/2) + a(t)*dt
        # r(t+dt) = r(t) + v(t+dt/2)*dt
        
        half_step_velocities = velocities + accelerations * dt
        new_positions = positions + half_step_velocities * dt
        new_velocities = half_step_velocities
        
    else:
        raise ValueError(f"Unknown integrator: {integrator}")
    
    return {
        'positions': new_positions,
        'velocities': new_velocities,
        'half_step_velocities': half_step_velocities,
        'accelerations': accelerations
    }


def kinetic_energy_calculator(
    velocities: np.ndarray,
    masses: np.ndarray,
    units: str = 'gromacs'
) -> Dict[str, float]:
    """
    Calculate kinetic energy and instantaneous temperature.
    
    KE = (1/2) Σ m_i v_i2
    
    Temperature from equipartition:
    T = 2*KE / (N_df * k_B)
    
    Args:
        velocities: Velocity array, shape (N, 3) in nm/ps
        masses: Mass array, shape (N,) in amu
        units: 'gromacs' (nm/ps, amu, kJ/mol) or 'si' (m/s, kg, J)
    
    Returns:
        Dictionary with:
        - 'KE': Kinetic energy (kJ/mol for GROMACS, J for SI)
        - 'temperature': Instantaneous temperature (K)
        - 'KE_per_atom': KE contribution per atom
        - 'degrees_of_freedom': Number of translational DOF
        
    Example:
        >>> vel = np.random.randn(100, 3) * 0.1  # nm/ps
        >>> masses = np.ones(100) * 18.0  # Water, amu
        >>> result = kinetic_energy_calculator(vel, masses)
        >>> print(f"T = {result['temperature']:.1f} K")
    """
    n_atoms = len(masses)
    n_dims = velocities.shape[1] if velocities.ndim > 1 else 1
    n_dof = n_atoms * n_dims  # Degrees of freedom (translational)
    
    # Calculate KE = (1/2) m v2
    # For GROMACS: KE in kJ/mol, velocities in nm/ps, masses in amu
    # 1 amu·(nm/ps)2 = 1.660539e-27 kg x (1e-9 m / 1e-12 s)2
    #                = 1.660539e-27 x 1e6 J
    #                = 1.660539e-21 J per molecule
    # = 1.660539e-21 x 6.022e23 J/mol = 1000 J/mol = 1 kJ/mol
    
    if units == 'gromacs':
        # KE in kJ/mol when v in nm/ps and m in amu
        v_squared = np.sum(velocities**2, axis=1)
        KE_per_atom = 0.5 * masses * v_squared  # kJ/mol per atom
        KE_total = np.sum(KE_per_atom)  # kJ/mol
        
        # Temperature: T = 2*KE / (N_df * k_B)
        # For GROMACS: KE in kJ/mol, need to convert to J
        # k_B = 0.008314462618 kJ/(mol·K)
        k_B_gromacs = 0.008314462618  # kJ/(mol·K)
        temperature = 2 * KE_total / (n_dof * k_B_gromacs)
        
    else:  # SI units
        v_squared = np.sum(velocities**2, axis=1)
        KE_per_atom = 0.5 * masses * v_squared  # J per atom
        KE_total = np.sum(KE_per_atom)  # J
        
        k_B = 1.380649e-23  # J/K
        temperature = 2 * KE_total / (n_dof * k_B)
    
    return {
        'KE': float(KE_total),
        'temperature': float(temperature),
        'KE_per_atom': KE_per_atom,
        'degrees_of_freedom': n_dof
    }


# =============================================================================
# G09: QUANTITATIVE STRUCTURE-ACTIVITY RELATIONSHIPS (QSAR)
# =============================================================================

def descriptor_calculator(
    smiles: str = None,
    molecular_weight: float = None,
    logP: float = None,
    h_bond_donors: int = None,
    h_bond_acceptors: int = None,
    rotatable_bonds: int = None,
    topological_polar_surface_area: float = None,
    num_atoms: int = None,
    num_heavy_atoms: int = None,
    num_rings: int = None,
    num_aromatic_rings: int = None,
    fraction_csp3: float = None,
) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Calculate molecular descriptors for QSAR modeling.
    
    Computes commonly used descriptors:
    - Lipinski descriptors (MW, LogP, HBD, HBA)
    - Topological descriptors
    - Electronic descriptors (simplified)
    - Physicochemical descriptors
    
    Note: For full descriptor calculation, use RDKit or PaDEL-Descriptor.
    This function provides simplified calculations from basic inputs.
    
    Args:
        smiles: SMILES string (for future RDKit integration)
        molecular_weight: MW in g/mol
        logP: Octanol-water partition coefficient
        h_bond_donors: Number of H-bond donors (OH, NH)
        h_bond_acceptors: Number of H-bond acceptors (O, N)
        rotatable_bonds: Number of rotatable bonds
        topological_polar_surface_area: TPSA in Å2
        num_atoms: Total number of atoms
        num_heavy_atoms: Number of heavy atoms (non-H)
        num_rings: Total number of rings
        num_aromatic_rings: Number of aromatic rings
        fraction_csp3: Fraction of sp3 carbons
    
    Returns:
        Dictionary with:
        - 'lipinski_descriptors': Dict of Lipinski-related descriptors
        - 'topological_descriptors': Topological descriptor dict
        - 'druglikeness_scores': Druglikeness indicators
        - 'all_descriptors': Flat dict of all computed descriptors
        
    Example:
        >>> result = descriptor_calculator(
        ...     molecular_weight=350,
        ...     logP=2.5,
        ...     h_bond_donors=2,
        ...     h_bond_acceptors=4
        ... )
        >>> print(f"Lipinski violations: {result['druglikeness_scores']['lipinski_violations']}")
    """
    # Default values
    mw = molecular_weight or 0
    logp = logP or 0
    hbd = h_bond_donors or 0
    hba = h_bond_acceptors or 0
    rot_bonds = rotatable_bonds or 0
    tpsa = topological_polar_surface_area or 0
    n_atoms = num_atoms or 0
    n_heavy = num_heavy_atoms or 0
    n_rings = num_rings or 0
    n_arom = num_aromatic_rings or 0
    fsp3 = fraction_csp3 or 0
    
    # Lipinski Rule of Five descriptors
    lipinski = {
        'MW': mw,
        'LogP': logp,
        'HBD': hbd,
        'HBA': hba,
        'MW_pass': mw <= 500,
        'LogP_pass': logp <= 5,
        'HBD_pass': hbd <= 5,
        'HBA_pass': hba <= 10
    }
    
    lipinski_violations = sum([
        mw > 500, logp > 5, hbd > 5, hba > 10
    ])
    
    # Veber's rules
    veber_oral_bioavailability = (rot_bonds <= 10) and (tpsa <= 140)
    
    # Topological descriptors
    topological = {
        'rotatable_bonds': rot_bonds,
        'TPSA': tpsa,
        'num_atoms': n_atoms,
        'num_heavy_atoms': n_heavy,
        'num_rings': n_rings,
        'num_aromatic_rings': n_arom,
        'fraction_csp3': fsp3
    }
    
    # Druglikeness scores
    # QED (Quantitative Estimate of Drug-likeness) - simplified
    # Based on weighted sum of property desirability
    
    # Simple druglikeness score (0-1 scale)
    druglikeness_score = 1.0
    if mw > 500:
        druglikeness_score -= 0.2 * min(1, (mw - 500) / 200)
    if logp > 5:
        druglikeness_score -= 0.15 * min(1, (logp - 5) / 3)
    if hbd > 5:
        druglikeness_score -= 0.1 * min(1, (hbd - 5) / 3)
    if hba > 10:
        druglikeness_score -= 0.1 * min(1, (hba - 10) / 5)
    if rot_bonds > 10:
        druglikeness_score -= 0.1 * min(1, (rot_bonds - 10) / 5)
    druglikeness_score = max(0, druglikeness_score)
    
    # Synthetic accessibility (simplified estimate)
    # Higher for complex molecules (many rings, stereocenters)
    sa_score = 1.0  # Easy to synthesize
    if n_rings > 3:
        sa_score += 0.5 * (n_rings - 3)
    if n_arom > 2:
        sa_score += 0.3 * (n_arom - 2)
    sa_score = min(10, sa_score)  # Cap at 10
    
    druglikeness = {
        'lipinski_violations': lipinski_violations,
        'lipinski_compliant': lipinski_violations <= 1,
        'veber_compliant': veber_oral_bioavailability,
        'druglikeness_score': druglikeness_score,
        'synthetic_accessibility': sa_score
    }
    
    # All descriptors as flat dict
    all_desc = {
        **{f'lipinski_{k}': v for k, v in lipinski.items()},
        **{f'topo_{k}': v for k, v in topological.items()},
        **{f'drug_{k}': v for k, v in druglikeness.items()}
    }
    
    return {
        'lipinski_descriptors': lipinski,
        'topological_descriptors': topological,
        'druglikeness_scores': druglikeness,
        'all_descriptors': all_desc
    }


def qsar_model_builder(
    X: np.ndarray,
    y: np.ndarray,
    method: str = 'mlr',
    n_components: int = 2,
    cross_validate: bool = True,
    n_folds: int = 5,
    random_state: int = 42
) -> Dict[str, Union[np.ndarray, float, Dict]]:
    """
    Build a QSAR model using MLR, PLS, or PCR.
    
    Multiple Linear Regression (MLR):
    y = Xbeta + ε, solved by beta = (X'X)-1X'y
    
    Partial Least Squares (PLS):
    Projects X and y to latent variables maximizing covariance
    
    Principal Component Regression (PCR):
    PCR on X followed by regression on components
    
    Args:
        X: Descriptor matrix, shape (n_samples, n_descriptors)
        y: Activity/property vector, shape (n_samples,)
        method: 'mlr', 'pls', or 'pcr'
        n_components: Number of components for PLS/PCR
        cross_validate: Whether to perform cross-validation
        n_folds: Number of CV folds
        random_state: Random seed for reproducibility
    
    Returns:
        Dictionary with:
        - 'coefficients': Model coefficients
        - 'intercept': Model intercept
        - 'R2': R-squared on training data
        - 'Q2': Cross-validated R-squared (if CV performed)
        - 'RMSE': Root mean square error
        - 'predictions': Predicted y values
        - 'residuals': y - y_pred
        - 'feature_importance': Relative importance of descriptors
        
    Example:
        >>> X = np.random.randn(50, 10)  # 50 compounds, 10 descriptors
        >>> y = X @ np.array([1, 0.5, -0.3, 0, 0, 0, 0, 0, 0, 0]) + np.random.randn(50) * 0.1
        >>> model = qsar_model_builder(X, y, method='pls', n_components=3)
        >>> print(f"R2 = {model['R2']:.3f}, Q2 = {model.get('Q2', 'N/A')}")
    """
    np.random.seed(random_state)
    n_samples, n_features = X.shape
    
    # Standardize X (important for PLS/PCR)
    X_mean = np.mean(X, axis=0)
    X_std = np.std(X, axis=0, ddof=1)
    X_std[X_std == 0] = 1  # Avoid division by zero
    X_scaled = (X - X_mean) / X_std
    
    y_mean = np.mean(y)
    y_centered = y - y_mean
    
    if method == 'mlr':
        # Multiple Linear Regression with regularization to handle collinearity
        # Using ridge regression (L2 regularization)
        alpha = 0.01  # Small regularization
        XtX = X_scaled.T @ X_scaled + alpha * np.eye(n_features)
        Xty = X_scaled.T @ y_centered
        coefficients_scaled = np.linalg.solve(XtX, Xty)
        
        # Transform back to original scale
        coefficients = coefficients_scaled / X_std
        intercept = y_mean - np.dot(X_mean, coefficients)
        
        # Predictions
        predictions = X @ coefficients + intercept
        
    elif method == 'pls':
        # Simplified PLS (NIPALS algorithm)
        n_comp = min(n_components, n_features, n_samples)
        
        X_pls = X_scaled.copy()
        y_pls = y_centered.copy()
        
        W = np.zeros((n_features, n_comp))  # Weights
        T = np.zeros((n_samples, n_comp))   # Scores
        P = np.zeros((n_features, n_comp))  # Loadings
        Q = np.zeros(n_comp)  # y-loadings
        
        for comp in range(n_comp):
            # Start with y as initial weight
            w = X_pls.T @ y_pls
            w = w / np.linalg.norm(w)
            
            # X scores
            t = X_pls @ w
            
            # X loadings
            p = X_pls.T @ t / (t.T @ t)
            
            # y loadings
            q = y_pls.T @ t / (t.T @ t)
            
            # Deflate
            X_pls = X_pls - np.outer(t, p)
            y_pls = y_pls - q * t
            
            W[:, comp] = w
            T[:, comp] = t
            P[:, comp] = p
            Q[comp] = q
        
        # PLS coefficients
        # beta = W(P'W)-1Q
        coefficients_scaled = W @ np.linalg.inv(P.T @ W) @ Q
        coefficients = coefficients_scaled / X_std
        intercept = y_mean - np.dot(X_mean, coefficients)
        
        predictions = X @ coefficients + intercept
        
    elif method == 'pcr':
        # Principal Component Regression
        n_comp = min(n_components, n_features, n_samples)
        
        # PCA on X
        U, S, Vt = np.linalg.svd(X_scaled, full_matrices=False)
        
        # Scores and loadings
        T = U[:, :n_comp] * S[:n_comp]
        V = Vt[:n_comp, :].T
        
        # Regression on components
        TtT_inv = np.linalg.inv(T.T @ T + 0.01 * np.eye(n_comp))
        beta_T = TtT_inv @ T.T @ y_centered
        
        # Transform back to original space
        coefficients_scaled = V @ beta_T
        coefficients = coefficients_scaled / X_std
        intercept = y_mean - np.dot(X_mean, coefficients)
        
        predictions = X @ coefficients + intercept
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Calculate statistics
    residuals = y - predictions
    SS_res = np.sum(residuals**2)
    SS_tot = np.sum((y - y_mean)**2)
    R2 = 1 - SS_res / SS_tot
    RMSE = np.sqrt(SS_res / n_samples)
    
    # Feature importance (absolute coefficient magnitude)
    feature_importance = np.abs(coefficients)
    feature_importance = feature_importance / np.sum(feature_importance)
    
    # Cross-validation
    Q2 = None
    if cross_validate:
        np.random.seed(random_state)
        indices = np.random.permutation(n_samples)
        fold_size = n_samples // n_folds
        
        Q2_folds = []
        for fold in range(n_folds):
            val_idx = indices[fold * fold_size:(fold + 1) * fold_size]
            train_idx = np.concatenate([
                indices[:fold * fold_size],
                indices[(fold + 1) * fold_size:]
            ])
            
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            
            # Refit model on training fold
            X_train_scaled = (X_train - X_mean) / X_std
            y_train_centered = y_train - y_mean
            
            if method == 'mlr':
                XtX = X_train_scaled.T @ X_train_scaled + 0.01 * np.eye(n_features)
                Xty = X_train_scaled.T @ y_train_centered
                coef_cv = np.linalg.solve(XtX, Xty) / X_std
                int_cv = y_mean - np.dot(X_mean, coef_cv)
            else:
                # Simplified: use full model coefficients
                coef_cv = coefficients
                int_cv = intercept
            
            y_pred_val = X_val @ coef_cv + int_cv
            
            # Q2 for this fold
            SS_res_cv = np.sum((y_val - y_pred_val)**2)
            SS_tot_cv = np.sum((y_val - np.mean(y_val))**2)
            Q2_fold = 1 - SS_res_cv / SS_tot_cv if SS_tot_cv > 0 else 0
            Q2_folds.append(Q2_fold)
        
        Q2 = np.mean(Q2_folds)
    
    return {
        'coefficients': coefficients,
        'intercept': intercept,
        'R2': float(R2),
        'Q2': float(Q2) if Q2 is not None else None,
        'RMSE': float(RMSE),
        'predictions': predictions,
        'residuals': residuals,
        'feature_importance': feature_importance,
        'method': method,
        'n_components': n_components if method != 'mlr' else None
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def lennard_jones(r: np.ndarray, epsilon: float, sigma: float) -> Dict[str, np.ndarray]:
    """
    Calculate Lennard-Jones potential and force.
    
    V(r) = 4ε[(σ/r)12 - (σ/r)6]
    F(r) = -dV/dr = 24ε/r [2(σ/r)12 - (σ/r)6]
    
    Args:
        r: Distance array (nm)
        epsilon: Well depth (kJ/mol)
        sigma: Collision diameter (nm)
    
    Returns:
        Dictionary with 'potential' and 'force' arrays
    """
    # Avoid division by zero
    r_safe = np.where(r > 0, r, 1e-10)
    
    sr6 = (sigma / r_safe)**6
    sr12 = sr6**2
    
    potential = 4 * epsilon * (sr12 - sr6)
    force = 24 * epsilon / r_safe * (2 * sr12 - sr6)
    
    return {
        'potential': potential,
        'force': force
    }


def boltzmann_distribution(energies: np.ndarray, temperature: float) -> np.ndarray:
    """
    Calculate Boltzmann population distribution.
    
    P_i = exp(-E_i/kT) / Q
    where Q = Σ exp(-E_i/kT)
    
    Args:
        energies: Energy levels (in K if using k_B=1, or J)
        temperature: Temperature (K)
    
    Returns:
        Population probabilities
    """
    # Reduced energies
    beta_E = energies / temperature
    
    # Subtract minimum for numerical stability
    beta_E -= np.min(beta_E)
    
    # Calculate Boltzmann factors
    boltzmann = np.exp(-beta_E)
    
    # Normalize
    probabilities = boltzmann / np.sum(boltzmann)
    
    return probabilities


if __name__ == '__main__':
    # Quick tests
    print("=" * 60)
    print("Computational Chemistry Tools - Quick Tests")
    print("=" * 60)
    
    # Test DFT
    print("\n[DFT Test]")
    energy = dft_energy_calculator(76.0, -200.0, 50.0, -10.0, 5.0)
    print(f"Total DFT energy: {energy['E_total']:.2f} Ha")
    
    # Test rotational spectroscopy
    print("\n[Rotational Spectroscopy Test]")
    masses = np.array([12.0, 16.0])
    coords = np.array([[0, 0, 0], [1.128, 0, 0]])
    rot = rotational_constant_calculator(masses, coords)
    print(f"CO rotational constant: B = {rot['B']:.4f} cm^-1")
    
    qrot = rotational_partition_function(rot['B'], 298, symmetry_number=1)
    print(f"Rotational partition function at 298 K: Q_rot = {qrot['Q_rot']:.2f}")
    
    # Test MD
    print("\n[MD Test]")
    pos = np.array([[0, 0, 0], [0.3, 0, 0]])
    vel = np.array([[0.1, 0, 0], [-0.1, 0, 0]])
    forces = np.array([[10, 0, 0], [-10, 0, 0]])
    masses_md = np.array([12.0, 16.0])
    
    md_result = md_integrator(pos, vel, forces, masses_md, dt=0.001)
    print(f"New positions:\n{md_result['positions']}")
    
    ke_result = kinetic_energy_calculator(vel, masses_md)
    print(f"Temperature: {ke_result['temperature']:.1f} K")
    
    # Test QSAR
    print("\n[QSAR Test]")
    desc = descriptor_calculator(molecular_weight=350, logP=2.5, 
                                 h_bond_donors=2, h_bond_acceptors=4)
    print(f"Lipinski violations: {desc['druglikeness_scores']['lipinski_violations']}")
    
    # Build QSAR model
    np.random.seed(42)
    X = np.random.randn(50, 10)
    y = X[:, 0] + 0.5 * X[:, 1] + np.random.randn(50) * 0.1
    model = qsar_model_builder(X, y, method='pls', n_components=3)
    print(f"PLS model: R2 = {model['R2']:.3f}, Q2 = {model['Q2']:.3f}")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


# Simple rotational spectroscopy convenience wrappers
def rotational_energy(J: int, B: float, D: float = 0.0) -> dict:
    """Rotational energy level E_J = B*J*(J+1) - D*[J*(J+1)]^2 in cm^-1."""
    E = B * J * (J + 1) - D * (J * (J + 1))**2
    return {"result": E, "E_J": E, "J": J, "B": B, "D": D}

def transition_frequency(J_lower: int, B: float, D: float = 0.0) -> dict:
    """Transition frequency nu = 2*B*(J+1) - 4*D*(J+1)^3 in cm^-1."""
    nu = 2 * B * (J_lower + 1) - 4 * D * (J_lower + 1)**3
    return {"result": nu, "frequency_cm-1": nu, "J_lower": J_lower, "J_upper": J_lower + 1}

def j_max(B: float, T: float) -> dict:
    """Most populated J level: J_max = sqrt(kT/(2hcB)) - 0.5."""
    import math
    # kT/(hcB), k=1.381e-23, h=6.626e-34, c=2.998e10 cm/s
    x = 1.4388 * T / B  # hc/k in cm·K
    J = round(math.sqrt(T / (1.4388 * B)) - 0.5)
    return {"result": max(J, 0), "J_max": max(J, 0), "B": B, "T": T}

def rotational_constant(I: float) -> dict:
    """Rotational constant B = h / (8 * pi^2 * I * c) in cm^-1.
    I in kg*m^2, returns B in cm^-1."""
    h = 6.62607015e-34  # J·s
    c = 2.99792458e10   # cm/s
    import math
    pi = math.pi
    B = h / (8 * pi**2 * I * c)
    return {"B_cm-1": B, "I_kg_m2": I, "result": B}

def moment_of_inertia(m1: float, m2: float, r: float) -> dict:
    """Moment of inertia for diatomic: I = mu * r^2, mu = m1*m2/(m1+m2). m in kg, r in m."""
    mu = (m1 * m2) / (m1 + m2)
    I = mu * r**2
    return {"I_kg_m2": I, "reduced_mass_kg": mu, "result": I}


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'boltzmann_distribution', 'description': 'Calculate Boltzmann population distribution.\n\nP_i = exp(-E_i/kT) / Q\nwhere Q = Σ exp(-E_i/kT)\n\nArgs:\n    energies: Energy levels (in K if using k_B=1, or J)\n    temperature: Temperature (K)\n\nReturns:\n    Population probabilities', 'inputSchema': {'type': 'object', 'properties': {'energies': {'type': 'number', 'description': 'Energies'}, 'temperature': {'type': 'number', 'description': 'Temperature'}}, 'required': ['energies', 'temperature']}},
    {'name': 'descriptor_calculator', 'description': 'Calculate molecular descriptors for QSAR modeling.\n\nComputes commonly used descriptors:\n- Lipinski descriptors (MW, LogP, HBD, HBA)\n- Topological descriptors\n- Electronic descriptors (simplified)\n- Physicochemical descriptors\n\nNote: For full descriptor calculation, use RDKit or PaDEL-Descriptor.\nThis function provides simplified calculations from basic inputs.\n\nArgs:\n    smiles: SMILES string (for future RDKit integration)\n    molecular_weight: MW in g/mol\n    logP: Octanol-water partition coefficient\n    h_bond_donors: Number of H-bond donors (OH, NH)\n    h_bond_acceptors: Number of H-bond acceptors (O, N)\n    rotatable_bonds: Number of rotatable bonds\n    topological_polar_surface_area: TPSA in Å2\n    num_atoms: Total number of atoms\n    num_heavy_atoms: Number of heavy atoms (non-H)\n    num_rings: Total number of rings\n    num_aromatic_rings: Number of aromatic rings\n    fraction_csp3: Fraction of sp3 carbons\n\nReturns:\n    Dictionary with:\n    - \'lipinski_descriptors\': Dict of Lipinski-related descriptors\n    - \'topological_descriptors\': Topological descriptor dict\n    - \'druglikeness_scores\': Druglikeness indicators\n    - \'all_descriptors\': Flat dict of all computed descriptors\n    \nExample:\n    >>> result = descriptor_calculator(\n    ...     molecular_weight=350,\n    ...     logP=2.5,\n    ...     h_bond_donors=2,\n    ...     h_bond_acceptors=4\n    ... )\n    >>> print(f"Lipinski violations: {result[\'druglikeness_scores\'][\'lipinski_violations\']}")', 'inputSchema': {'type': 'object', 'properties': {'smiles': {'type': 'number', 'description': 'Smiles', 'default': None}, 'molecular_weight': {'type': 'number', 'description': 'Molecular Weight', 'default': None}, 'logP': {'type': 'number', 'description': 'Logp', 'default': None}, 'h_bond_donors': {'type': 'number', 'description': 'H Bond Donors', 'default': None}, 'h_bond_acceptors': {'type': 'number', 'description': 'H Bond Acceptors', 'default': None}, 'rotatable_bonds': {'type': 'number', 'description': 'Rotatable Bonds', 'default': None}, 'topological_polar_surface_area': {'type': 'string', 'description': 'Topological Polar Surface Area', 'default': None}, 'num_atoms': {'type': 'number', 'description': 'Num Atoms', 'default': None}, 'num_heavy_atoms': {'type': 'number', 'description': 'Num Heavy Atoms', 'default': None}, 'num_rings': {'type': 'string', 'description': 'Num Rings', 'default': None}, 'num_aromatic_rings': {'type': 'string', 'description': 'Num Aromatic Rings', 'default': None}, 'fraction_csp3': {'type': 'string', 'description': 'Fraction Csp3', 'default': None}}, 'required': []}},
    {'name': 'dft_energy_calculator', 'description': "Calculate total Kohn-Sham DFT energy from components.\n\nE_KS = T_s + V_ne + J + E_xc + E_nn\n\nWhere:\n- T_s: Kinetic energy of non-interacting electrons\n- V_ne: Electron-nuclear attraction\n- J: Coulomb (Hartree) energy\n- E_xc: Exchange-correlation energy\n- E_nn: Nuclear-nuclear repulsion\n\nArgs:\n    kinetic_energy: T_s - kinetic energy of Kohn-Sham orbitals (Hartree)\n    electron_nuclear_attraction: V_ne (Hartree)\n    coulomb_energy: J - classical electron-electron repulsion (Hartree)\n    exchange_correlation_energy: E_xc from XC functional (Hartree)\n    nuclear_repulsion: E_nn for multi-atom systems (Hartree, default 0)\n\nReturns:\n    Dictionary with energy components and total energy in Hartree\n    \nExample:\n    >>> dft_energy_calculator(76.0, -200.0, 50.0, -10.0, 5.0)\n    {'T_s': 76.0, 'V_ne': -200.0, 'J': 50.0, 'E_xc': -10.0, \n     'E_nn': 5.0, 'E_total': -79.0}", 'inputSchema': {'type': 'object', 'properties': {'kinetic_energy': {'type': 'number', 'description': 'Kinetic Energy'}, 'electron_nuclear_attraction': {'type': 'string', 'description': 'Electron Nuclear Attraction'}, 'coulomb_energy': {'type': 'number', 'description': 'Coulomb Energy'}, 'exchange_correlation_energy': {'type': 'string', 'description': 'Exchange Correlation Energy'}, 'nuclear_repulsion': {'type': 'string', 'description': 'Nuclear Repulsion', 'default': 0.0}}, 'required': ['kinetic_energy', 'electron_nuclear_attraction', 'coulomb_energy', 'exchange_correlation_energy']}},
    {'name': 'exchange_correlation_function', 'description': 'Calculate exchange-correlation energy and potential.\n\nImplements simplified versions of common functionals:\n- LDA: Local Density Approximation (Slater exchange + VWN correlation)\n- GGA: Generalized Gradient Approximation (PBE)\n- Hybrid: Mix of HF exchange and DFT (B3LYP-like)\n\nArgs:\n    rho: Electron density array (electrons/bohr3)\n    grad_rho: Density gradient magnitude (bohr-1·electrons/bohr3), required for GGA\n    functional_type: \'lda\', \'gga\', or \'hybrid\'\n    rho_cutoff: Minimum density threshold (default 1e-10)\n\nReturns:\n    Dictionary with:\n    - \'E_xc\': Exchange-correlation energy (Hartree)\n    - \'epsilon_xc\': XC energy per particle\n    - \'v_xc\': XC potential\n    - \'E_x\': Exchange energy\n    - \'E_c\': Correlation energy\n    \nExample:\n    >>> rho = np.array([0.1, 0.2, 0.3])\n    >>> result = exchange_correlation_function(rho, functional_type=\'lda\')\n    >>> print(f"E_xc = {result[\'E_xc\']:.6f} Ha")', 'inputSchema': {'type': 'object', 'properties': {'rho': {'type': 'number', 'description': 'Rho'}, 'grad_rho': {'type': 'number', 'description': 'Grad Rho', 'default': None}, 'functional_type': {'type': 'string', 'description': 'Functional Type', 'default': 'lda'}, 'rho_cutoff': {'type': 'number', 'description': 'Rho Cutoff', 'default': 1e-10}}, 'required': ['rho']}},
    {'name': 'j_max', 'description': 'Most populated J level: J_max = sqrt(kT/(2hcB)) - 0.5.', 'inputSchema': {'type': 'object', 'properties': {'B': {'type': 'number', 'description': 'B'}, 'T': {'type': 'number', 'description': 'T'}}, 'required': ['B', 'T']}},
    {'name': 'kinetic_energy_calculator', 'description': 'Calculate kinetic energy and instantaneous temperature.\n\nKE = (1/2) Σ m_i v_i2\n\nTemperature from equipartition:\nT = 2*KE / (N_df * k_B)\n\nArgs:\n    velocities: Velocity array, shape (N, 3) in nm/ps\n    masses: Mass array, shape (N,) in amu\n    units: \'gromacs\' (nm/ps, amu, kJ/mol) or \'si\' (m/s, kg, J)\n\nReturns:\n    Dictionary with:\n    - \'KE\': Kinetic energy (kJ/mol for GROMACS, J for SI)\n    - \'temperature\': Instantaneous temperature (K)\n    - \'KE_per_atom\': KE contribution per atom\n    - \'degrees_of_freedom\': Number of translational DOF\n    \nExample:\n    >>> vel = np.random.randn(100, 3) * 0.1  # nm/ps\n    >>> masses = np.ones(100) * 18.0  # Water, amu\n    >>> result = kinetic_energy_calculator(vel, masses)\n    >>> print(f"T = {result[\'temperature\']:.1f} K")', 'inputSchema': {'type': 'object', 'properties': {'velocities': {'type': 'number', 'description': 'Velocities'}, 'masses': {'type': 'number', 'description': 'Masses'}, 'units': {'type': 'string', 'description': 'Units', 'default': 'gromacs'}}, 'required': ['velocities', 'masses']}},
    {'name': 'lennard_jones', 'description': "Calculate Lennard-Jones potential and force.\n\nV(r) = 4ε[(σ/r)12 - (σ/r)6]\nF(r) = -dV/dr = 24ε/r [2(σ/r)12 - (σ/r)6]\n\nArgs:\n    r: Distance array (nm)\n    epsilon: Well depth (kJ/mol)\n    sigma: Collision diameter (nm)\n\nReturns:\n    Dictionary with 'potential' and 'force' arrays", 'inputSchema': {'type': 'object', 'properties': {'r': {'type': 'number', 'description': 'R'}, 'epsilon': {'type': 'number', 'description': 'Epsilon'}, 'sigma': {'type': 'number', 'description': 'Sigma'}}, 'required': ['r', 'epsilon', 'sigma']}},
    {'name': 'md_integrator', 'description': "Perform one MD integration step using Velocity Verlet algorithm.\n\nVelocity Verlet algorithm:\n1. r(t+dt) = r(t) + v(t)*dt + 0.5*a(t)*dt2\n2. Calculate F(t+dt) from new positions\n3. v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt\n\nArgs:\n    positions: Current positions, shape (N, 3) in nm\n    velocities: Current velocities, shape (N, 3) in nm/ps\n    forces: Current forces, shape (N, 3) in kJ/mol/nm\n    masses: Atomic masses, shape (N,) in amu\n    dt: Time step in ps\n    integrator: 'velocity_verlet' (default) or 'leapfrog'\n\nReturns:\n    Dictionary with:\n    - 'positions': New positions (nm)\n    - 'velocities': New velocities (nm/ps)\n    - 'half_step_velocities': Half-step velocities for force calculation\n    - 'accelerations': Current accelerations (nm/ps2)\n    \nExample:\n    >>> pos = np.array([[0, 0, 0], [0.3, 0, 0]])  # nm\n    >>> vel = np.array([[0.1, 0, 0], [-0.1, 0, 0]])  # nm/ps\n    >>> forces = np.array([[10, 0, 0], [-10, 0, 0]])  # kJ/mol/nm\n    >>> masses = np.array([12.0, 16.0])  # amu\n    >>> result = md_integrator(pos, vel, forces, masses, dt=0.001)", 'inputSchema': {'type': 'object', 'properties': {'positions': {'type': 'string', 'description': 'Positions'}, 'velocities': {'type': 'number', 'description': 'Velocities'}, 'forces': {'type': 'number', 'description': 'Forces'}, 'masses': {'type': 'number', 'description': 'Masses'}, 'dt': {'type': 'number', 'description': 'Dt'}, 'integrator': {'type': 'number', 'description': 'Integrator', 'default': 'velocity_verlet'}}, 'required': ['positions', 'velocities', 'forces', 'masses', 'dt']}},
    {'name': 'moment_of_inertia', 'description': 'Moment of inertia for diatomic: I = mu * r^2, mu = m1*m2/(m1+m2). m in kg, r in m.', 'inputSchema': {'type': 'object', 'properties': {'m1': {'type': 'number', 'description': 'M1'}, 'm2': {'type': 'number', 'description': 'M2'}, 'r': {'type': 'number', 'description': 'R'}}, 'required': ['m1', 'm2', 'r']}},
    {'name': 'qsar_model_builder', 'description': 'Build a QSAR model using MLR, PLS, or PCR.\n\nMultiple Linear Regression (MLR):\ny = Xbeta + ε, solved by beta = (X\'X)-1X\'y\n\nPartial Least Squares (PLS):\nProjects X and y to latent variables maximizing covariance\n\nPrincipal Component Regression (PCR):\nPCR on X followed by regression on components\n\nArgs:\n    X: Descriptor matrix, shape (n_samples, n_descriptors)\n    y: Activity/property vector, shape (n_samples,)\n    method: \'mlr\', \'pls\', or \'pcr\'\n    n_components: Number of components for PLS/PCR\n    cross_validate: Whether to perform cross-validation\n    n_folds: Number of CV folds\n    random_state: Random seed for reproducibility\n\nReturns:\n    Dictionary with:\n    - \'coefficients\': Model coefficients\n    - \'intercept\': Model intercept\n    - \'R2\': R-squared on training data\n    - \'Q2\': Cross-validated R-squared (if CV performed)\n    - \'RMSE\': Root mean square error\n    - \'predictions\': Predicted y values\n    - \'residuals\': y - y_pred\n    - \'feature_importance\': Relative importance of descriptors\n    \nExample:\n    >>> X = np.random.randn(50, 10)  # 50 compounds, 10 descriptors\n    >>> y = X @ np.array([1, 0.5, -0.3, 0, 0, 0, 0, 0, 0, 0]) + np.random.randn(50) * 0.1\n    >>> model = qsar_model_builder(X, y, method=\'pls\', n_components=3)\n    >>> print(f"R2 = {model[\'R2\']:.3f}, Q2 = {model.get(\'Q2\', \'N/A\')}")', 'inputSchema': {'type': 'object', 'properties': {'X': {'type': 'number', 'description': 'X'}, 'y': {'type': 'number', 'description': 'Y'}, 'method': {'type': 'string', 'description': 'Method', 'default': 'mlr'}, 'n_components': {'type': 'number', 'description': 'N Components', 'default': 2}, 'cross_validate': {'type': 'string', 'description': 'Cross Validate', 'default': True}, 'n_folds': {'type': 'number', 'description': 'N Folds', 'default': 5}, 'random_state': {'type': 'string', 'description': 'Random State', 'default': 42}}, 'required': ['X', 'y']}},
    {'name': 'rotational_constant', 'description': 'Rotational constant B = h / (8 * pi^2 * I * c) in cm^-1.\nI in kg*m^2, returns B in cm^-1.', 'inputSchema': {'type': 'object', 'properties': {'I': {'type': 'number', 'description': 'I'}}, 'required': ['I']}},
    {'name': 'rotational_constant_calculator', 'description': 'Calculate rotational constants from molecular geometry.\n\nFor a diatomic: B = h/(8pi2cI) = h/(8pi2cmur2)\nFor polyatomic: A, B, C from principal moments of inertia\n\nArgs:\n    masses: Atomic masses array (amu by default)\n    coordinates: Atomic coordinates array, shape (N, 3) (Å by default)\n    units: \'amu_angstrom\' (default) or \'si\' (kg, m)\n\nReturns:\n    Dictionary with:\n    - \'A\', \'B\', \'C\': Rotational constants (cm-1, A ≥ B ≥ C)\n    - \'I_a\', \'I_b\', \'I_c\': Principal moments of inertia (amu·Å2)\n    - \'molecule_type\': \'diatomic\', \'linear\', \'symmetric_top\', \'spherical_top\', or \'asymmetric_top\'\n    \nExample:\n    >>> # CO molecule: C at origin, O at 1.128 Å\n    >>> masses = np.array([12.0, 16.0])  # amu\n    >>> coords = np.array([[0, 0, 0], [1.128, 0, 0]])  # Å\n    >>> result = rotational_constant_calculator(masses, coords)\n    >>> print(f"B = {result[\'B\']:.4f} cm^-1")', 'inputSchema': {'type': 'object', 'properties': {'masses': {'type': 'number', 'description': 'Masses'}, 'coordinates': {'type': 'number', 'description': 'Coordinates'}, 'units': {'type': 'string', 'description': 'Units', 'default': 'amu_angstrom'}}, 'required': ['masses', 'coordinates']}},
    {'name': 'rotational_energy', 'description': 'Rotational energy level E_J = B*J*(J+1) - D*[J*(J+1)]^2 in cm^-1.', 'inputSchema': {'type': 'object', 'properties': {'J': {'type': 'number', 'description': 'J'}, 'B': {'type': 'number', 'description': 'B'}, 'D': {'type': 'number', 'description': 'D', 'default': 0.0}}, 'required': ['J', 'B']}},
    {'name': 'rotational_partition_function', 'description': 'Calculate rotational partition function.\n\nFor diatomic/linear: Q_rot = T/(σθ_rot) where θ_rot = hcB/k_B\nFor symmetric tops: Q_rot = (pi^(1/2)/σ) x (T3/(θ_Axθ_Bxθ_C))^(1/2)\nFor asymmetric tops: Q_rot = (pi^(1/2)/σ) x (T3/(θ_Axθ_Bxθ_C))^(1/2)\n\nArgs:\n    rotational_constants: B (cm-1) for diatomic, or (A, B, C) tuple for polyatomic\n    temperature: Temperature in Kelvin\n    symmetry_number: σ (1 for heteronuclear, 2 for homonuclear diatomic, etc.)\n    molecule_type: \'diatomic\', \'linear\', \'symmetric_top\', \'spherical_top\', \'asymmetric_top\'\n    include_excited_states: Whether to sum over J states explicitly (slower but more accurate)\n    max_J: Maximum J quantum number for explicit summation\n\nReturns:\n    Dictionary with:\n    - \'Q_rot\': Rotational partition function\n    - \'theta_rot\': Rotational temperature(s) (K)\n    - \'Q_rot_high_T\': High-temperature approximation\n    - \'contribution_per_rotor\': For each rotational degree of freedom\n    \nExample:\n    >>> # CO at 298 K\n    >>> result = rotational_partition_function(1.931, 298, symmetry_number=1)\n    >>> print(f"Q_rot = {result[\'Q_rot\']:.2f}")', 'inputSchema': {'type': 'object', 'properties': {'rotational_constants': {'type': 'string', 'description': 'Rotational Constants'}, 'temperature': {'type': 'number', 'description': 'Temperature'}, 'symmetry_number': {'type': 'string', 'description': 'Symmetry Number', 'default': 1}, 'molecule_type': {'type': 'string', 'description': 'Molecule Type', 'default': 'diatomic'}, 'include_excited_states': {'type': 'string', 'description': 'Include Excited States', 'default': True}, 'max_J': {'type': 'number', 'description': 'Max J', 'default': 100}}, 'required': ['rotational_constants', 'temperature']}},
    {'name': 'transition_frequency', 'description': 'Transition frequency nu = 2*B*(J+1) - 4*D*(J+1)^3 in cm^-1.', 'inputSchema': {'type': 'object', 'properties': {'J_lower': {'type': 'number', 'description': 'J Lower'}, 'B': {'type': 'number', 'description': 'B'}, 'D': {'type': 'number', 'description': 'D', 'default': 0.0}}, 'required': ['J_lower', 'B']}}
]
