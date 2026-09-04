---
id: chem.molecular_dynamics
layer: 2
title: Molecular Dynamics Simulation
source: Physical Chemistry foundations; LibreTexts; ASE Documentation; Best Practices for Molecular Simulations
status: active
created: 2026-03-17
last_verified: 2026-03-17
---

# Molecular Dynamics Simulation

**L1 Parent:** statistical_mechanics.md

## Problem Types

1. **Equilibrium structure sampling** - Generate configurations from thermodynamic ensemble
2. **Dynamic property calculation** - Transport coefficients, diffusion, viscosity
3. **Free energy estimation** - PMF, binding free energies via enhanced sampling
4. **Protein folding/unfolding** - Long-timescale conformational changes
5. **Material properties** - Phase transitions, mechanical properties
6. **Reaction pathway exploration** - Metadynamics, string methods

## Decision Tree

### 1. What ensemble is appropriate?

```
System requirements → Ensemble choice

Equilibrium sampling at fixed E → NVE (microcanonical)
Equilibrium at fixed T → NVT (canonical)
Equilibrium at fixed T, P → NPT (isothermal-isobaric)
Grand canonical (μ, V, T) → μVT (particle exchange)
```

### 2. Which integrator to use?

```
Accuracy requirement → Integrator

Standard MD → Velocity Verlet (symplectic, time-reversible)
Enhanced sampling → Langevin dynamics
Large systems → RESPA (multiple time step)
Rigid bodies → SHAKE/RATTLE constraints
```

### 3. Which thermostat?

```
System type → Thermostat choice

General purpose → Nosé-Hoover chain
Fast equilibration → Berendsen (weak coupling)
Stochastic dynamics → Langevin
Protein simulations → Andersen or Langevin
```

### 4. Force field selection

```
System type → Force field

Biomolecules (proteins, DNA) → CHARMM, AMBER, OPLS
Lipids/membranes → CHARMM36, Slipids
Small molecules → GAFF, CGenFF
Materials/metals → EAM, MEAM
Generic organic → GROMOS
Coarse-grained → MARTINI
```

---

## Section 1: Equations of Motion Integration

### Newton's Equations

**Basic equations:**
```
F_i = m_i a_i = -∇_i U(r₁, r₂, ..., r_N)

dv_i/dt = F_i/m_i
dr_i/dt = v_i
```

**Hamiltonian form:**
```
H = Σᵢ p_i²/(2m_i) + U(r₁, ..., r_N)

dr_i/dt = ∂H/∂p_i = p_i/m_i
dp_i/dt = -∂H/∂r_i = -∇_i U
```

### Verlet Algorithm

**Original Verlet:**
```
r(t + Δt) = 2r(t) - r(t - Δt) + (F(t)/m)Δt²

Properties:
- Time-reversible
- Symplectic (preserves phase space volume)
- Energy conserving for long simulations
- Requires positions at two time steps
- Velocities not directly computed
```

**Velocity estimate:**
```
v(t) = [r(t + Δt) - r(t - Δt)]/(2Δt) + O(Δt²)
```

### Velocity Verlet Algorithm

**Algorithm:**
```
1. r(t + Δt) = r(t) + v(t)Δt + ½(F(t)/m)Δt²
2. Compute F(t + Δt) from new positions
3. v(t + Δt) = v(t) + ½[F(t) + F(t + Δt)]Δt/m
```

**Properties:**
- Most widely used integrator
- Only needs positions and velocities at single time step
- Time-reversible and symplectic
- Excellent energy conservation
- O(Δt⁴) error in positions

### Leapfrog Algorithm

**Algorithm:**
```
v(t + Δt/2) = v(t - Δt/2) + F(t)Δt/m
r(t + Δt) = r(t) + v(t + Δt/2)Δt
```

**Properties:**
- Equivalent to Velocity Verlet mathematically
- Velocities defined at half-steps
- Better numerical precision for some systems
- Used in GROMACS

### Time Step Selection

**Guidelines:**
```
Rule of thumb: Δt ≈ (1/10) × (period of fastest motion)

System                    Recommended Δt
─────────────────────────────────────────
Rigid water (SPC, TIP3P)      2 fs
Flexible water                1 fs
Hydrogen-containing           1-2 fs
All-heavy atoms (no H)        4-5 fs
Metals/crystals               5 fs
Coarse-grained                10-50 fs
```

**Stability criterion:**
- Too large: Energy drifts upward, system "blows up"
- Too small: Wasteful computation
- Optimal: Slight energy fluctuation, no systematic drift

---

## Section 2: Force Fields

### Classical Force Field Form

**Total potential energy:**
```
U = U_bond + U_angle + U_dihedral + U_improper + U_vdw + U_elec

U_bond     = Σᵢ k_b(r_i - r₀)²           (bond stretching)
U_angle    = Σᵢ k_θ(θ_i - θ₀)²           (angle bending)
U_dihedral = Σᵢ k_φ[1 + cos(nφ - δ)]     (torsion)
U_improper = Σᵢ k_ω(ω_i - ω₀)²           (improper torsion)
U_vdw      = Σᵢ<ⱼ 4εᵢⱼ[(σᵢⱼ/rᵢⱼ)¹² - (σᵢⱼ/rᵢⱼ)⁶]  (Lennard-Jones)
U_elec     = Σᵢ<ⱼ qᵢqⱼ/(4πε₀rᵢⱼ)         (Coulomb)
```

### CHARMM Force Field

**History:** Developed at Harvard (Karplus group)

**Features:**
- Extensive protein/nucleic acid parameters
- CMAP correction for protein backbone
- TIP3P water model standard
- Cross-terms for improved accuracy

**Parameter types:**
```
Bonded: k_b, r₀, k_θ, θ₀, k_φ, n, δ
Nonbonded: ε, σ, q (partial charges)
Cross-terms: Urey-Bradley, CMAP
```

**Versions:**
- CHARMM22: Standard for proteins
- CHARMM36: Improved lipids, proteins
- CHARMM36m: Better IDP/IDR modeling

### AMBER Force Field

**History:** Developed at UCSF (Kollman group)

**Features:**
- ff14SB: Current standard for proteins
- ff19SB: Improved with QM-derived charges
- GAFF: General AMBER force field for small molecules
- RESP charges from QM calculations

**Charging methods:**
```
RESP    - Restrained Electrostatic Potential
AM1-BCC - Semi-empirical with bond charge corrections
CM5    - Charge Model 5
```

### GROMOS Force Field

**History:** Developed at ETH Zurich (van Gunsteren group)

**Features:**
- United atom approach (aliphatic H not explicit)
- Faster simulation due to fewer atoms
- GROMOS 54A7, 54B7 variants
- Popular for lipids and membranes

### OPLS Force Field

**History:** Developed at Yale (Jorgensen group)

**Features:**
- OPLS-AA: All-atom version
- OPLS-UA: United atom version
- Optimized for liquid properties
- Good for organic molecules

### Specialized Force Fields

| Force Field | Application | Key Features |
|-------------|-------------|--------------|
| MARTINI | Coarse-grained | 4:1 mapping, fast dynamics |
| EAM/MEAM | Metals | Embedded atom, many-body |
| ReaxFF | Reactive | Bond breaking/forming |
| COMPASS | Materials | Condensed phase optimized |
| DREIDING | Generic | Minimal parameterization |
| UFF | Universal | All elements covered |

---

## Section 3: Statistical Ensembles

### NVE Ensemble (Microcanonical)

**Definition:**
- Constant Number of particles (N)
- Constant Volume (V)
- Constant Energy (E)

**Properties:**
- Natural ensemble from Newton's equations
- Energy should be conserved (up to numerical error)
- Temperature fluctuates
- Good for testing integrator stability

**Implementation:**
```
Use Velocity Verlet integrator directly
No thermostat or barostat needed
Monitor energy drift as quality check
```

### NVT Ensemble (Canonical)

**Definition:**
- Constant N
- Constant V
- Constant Temperature (T)

**Properties:**
- System coupled to heat bath
- Energy fluctuates
- Temperature is fixed (on average)
- Most common production ensemble

**Thermostat methods:**

| Method | Description | Use Case |
|--------|-------------|----------|
| Berendsen | Weak coupling, exponential relaxation | Equilibration |
| Nosé-Hoover | Deterministic, proper sampling | Production |
| Nosé-Hoover chain | Multiple coupled baths | Robust sampling |
| Langevin | Stochastic friction + noise | Biomolecules |
| Andersen | Random velocity reassignment | Simple, robust |

### NPT Ensemble (Isothermal-Isobaric)

**Definition:**
- Constant N
- Constant Pressure (P)
- Constant T

**Properties:**
- Most relevant to experiments
- Volume and shape can change
- Density equilibrates naturally
- Required for phase transitions

**Barostat methods:**

| Method | Description | Properties |
|--------|-------------|------------|
| Berendsen | Weak coupling | Fast but not correct ensemble |
| Parrinello-Rahman | Proper NPT | Correct fluctuations |
| Martyna-Tuckerman-Klein (MTK) | Hamiltonian formulation | Symplectic, correct ensemble |
| Langevin piston | Stochastic | Robust for membranes |

### μVT Ensemble (Grand Canonical)

**Definition:**
- Constant Chemical Potential (μ)
- Constant V
- Constant T

**Properties:**
- Particle number fluctuates
- Used for adsorption, surface phenomena
- More common in Monte Carlo than MD

---

## Section 4: Thermostats and Barostats

### Berendsen Thermostat

**Algorithm:**
```
dT/dt = (T₀ - T)/τ_T

Velocity scaling: λ = √[1 + (Δt/τ_T)(T₀/T - 1)]

Parameters:
T₀ = target temperature
τ_T = coupling time constant
```

**Properties:**
- First-order relaxation to T₀
- Fast equilibration
- Does NOT produce correct canonical ensemble
- Use for equilibration only, not production

### Nosé-Hoover Thermostat

**Extended Lagrangian:**
```
L = Σᵢ ½m_i v_i² - U(r) + ½Q ṡ² - gkT ln(s)

where:
s = thermostat coordinate
Q = thermostat "mass"
g = degrees of freedom
```

**Equations of motion:**
```
dr_i/dt = p_i/m_i
dp_i/dt = -∇_i U - (ṡ/s)p_i
ds/dt = s·p_s/Q
dp_s/dt = Σᵢ p_i²/m_i - gkT
```

**Properties:**
- Deterministic, time-reversible
- Produces correct canonical ensemble
- May have non-ergodic behavior
- Nosé-Hoover chain solves this

### Langevin Thermostat

**Equation:**
```
m_i dv_i/dt = F_i - γm_i v_i + √(2γm_i k_B T) R(t)

where:
γ = friction coefficient
R(t) = random force (Gaussian, mean=0)
```

**Properties:**
- Stochastic dynamics
- Correct canonical sampling
- Models implicit solvent
- Good for biomolecules

**Friction coefficient selection:**
```
γ small (0.1-1 ps⁻¹): Weak coupling, natural dynamics
γ medium (5-10 ps⁻¹): Moderate damping
γ large (50+ ps⁻¹): Strong damping, overdamped
```

### Berendsen Barostat

**Algorithm:**
```
dP/dt = (P₀ - P)/τ_P

Volume scaling: μ = 1 - (βΔt/τ_P)(P - P₀)

where:
β = isothermal compressibility
τ_P = pressure coupling constant
```

### Parrinello-Rahman Barostat

**Properties:**
- Proper NPT ensemble
- Box vectors can change independently
- Anisotropic cell fluctuations
- Correct pressure fluctuations

---

## Section 5: Periodic Boundary Conditions

### Basic Concept

**Purpose:**
- Simulate bulk properties with finite system
- Eliminate surface effects
- Maintain constant density

**Implementation:**
```
For each atom i:
  r_i = r_i - L × floor(r_i/L)

where L = box length
```

### Minimum Image Convention

**Distance calculation:**
```
r_ij = r_j - r_i
r_ij = r_ij - L × round(r_ij/L)

This ensures |r_ij| ≤ L/2
```

### Cutoff Schemes

**Truncation methods:**

| Method | Description | Cutoff radius |
|--------|-------------|---------------|
| Hard cutoff | Zero after r_c | Energy discontinuity |
| Shifted potential | Smooth to zero | No force discontinuity |
| Switching function | Gradual transition | Smooth force |
| Force switching | Direct force modification | Common in CHARMM |

**Standard cutoffs:**
```
Lennard-Jones: 10-12 Å
Electrostatics: Use Ewald/PME (no cutoff)
Combined (reaction field): 12-15 Å
```

### Ewald Summation and PME

**Problem:** Long-range electrostatics in periodic systems

**Ewald decomposition:**
```
1/r = 1/r·erfc(κr) + 1/r·erf(κr)
      └─ short-range ──┘  └─ long-range ──┘
```

**Particle Mesh Ewald (PME):**
- FFT-accelerated long-range calculation
- O(N log N) scaling
- Standard in most MD packages

**Parameters:**
```
κ (kappa) = Ewald parameter (determines real/reciprocal balance)
Typical: κ = 0.34-0.36 Å⁻¹
Grid spacing: 1.0-1.2 Å
Interpolation: 4th-6th order B-spline
```

---

## Section 6: Common MD Software

### GROMACS

**Strengths:**
- Free, open source
- Excellent GPU acceleration
- Very fast on modern hardware
- Comprehensive documentation
- Large user community

**Typical workflow:**
```
gmx pdb2gmx    # Generate topology
gmx editconf   # Define box
gmx solvate    # Add solvent
gmx grompp     # Preprocess
gmx mdrun      # Run simulation
gmx energy     # Analyze energies
gmx rms        # RMSD analysis
```

### LAMMPS

**Strengths:**
- Highly flexible
- Many force fields and potentials
- Excellent for materials
- Active development
- Supports many accelerators

**Key features:**
- Pair styles for many potentials
- Fix commands for thermostats/barostats
- Compute for analysis
- Variable for custom calculations

### NAMD

**Strengths:**
- Designed for biomolecules
- Excellent scalability
- VMD integration
- GPU acceleration
- User-friendly

**Configuration style:**
```
# NAMD config file
structure      system.psf
coordinates    system.pdb
temperature    300
timestep       2.0
run            1000000
```

### AMBER

**Strengths:**
- Integrated with AMBER force field
- PMEMD for MD
- Comprehensive analysis tools
- Free energy methods
- Explicit QM/MM

**Programs:**
- `tleap`: System setup
- `sander`: General MD engine
- `pmemd`: Optimized MD (GPU support)
- `cpptraj`: Trajectory analysis

### OpenMM

**Strengths:**
- Python API
- GPU acceleration (CUDA, OpenCL)
- Easy to customize
- Jupyter-friendly
- Good for method development

**Example:**
```python
from openmm.app import *
from openmm import *
from simtk.openmm import app

# Create system
pdb = PDBFile('system.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
system = forcefield.createSystem(pdb.topology)

# Setup integrator
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 2*femtoseconds)

# Run simulation
simulation = Simulation(pdb.topology, system, integrator)
simulation.step(10000)
```

---

## Section 7: Enhanced Sampling Methods

### Replica Exchange (REMD)

**Concept:**
- Multiple replicas at different temperatures
- Exchange attempts between neighboring temperatures
- Overcome energy barriers

**Acceptance criterion:**
```
P_accept = min(1, exp[(β_i - β_j)(E_j - E_i)])

where β = 1/kT
```

### Metadynamics

**Concept:**
- Add history-dependent bias potential
- Fill free energy minima
- Explore reaction coordinates

**Bias potential:**
```
V(s, t) = Σ_{t' < t} w exp(-|s - s(t')|²/2σ²)

where:
s = collective variable
w = Gaussian height
σ = Gaussian width
```

### Umbrella Sampling

**Concept:**
- Restrain system along reaction coordinate
- Sample windows along coordinate
- Combine with WHAM

**Restraint:**
```
U_restraint = ½k(ξ - ξ₀)²

where ξ = reaction coordinate
```

### Accelerated MD (aMD)

**Concept:**
- Modify potential energy surface
- Lower barriers, faster transitions
- Boost potential: ΔV = (E - V)²/(α + E - V)

---

## Section 8: Analysis Methods

### Structural Analysis

| Property | Method | Software |
|----------|--------|----------|
| RMSD | Align to reference | gmx rms |
| RMSF | Per-atom fluctuation | gmx rmsf |
| Radius of gyration | R_g = √(Σm_i r_i²/Σm_i) | gmx gyrate |
| Hydrogen bonds | Distance/angle criteria | gmx hbond |
| Secondary structure | DSSP algorithm | do_dssp |

### Dynamic Analysis

| Property | Method | Formula |
|----------|--------|---------|
| Diffusion coefficient | MSD slope | D = lim_t MS(t)/(6t) |
| Viscosity | Green-Kubo | η = V/(k_B T) ∫⟨P_αβ(0)P_αβ(t)⟩dt |
| Correlation time | Autocorrelation decay | C(t) = ⟨A(0)A(t)⟩ |

### Free Energy

| Method | Description | Accuracy |
|--------|-------------|----------|
| MM/PBSA | End-point method | Moderate |
| TI | Thermodynamic integration | High |
| FEP | Free energy perturbation | High |
| WHAM | Histogram analysis | High |

---

## Key Formulas Summary

| Concept | Formula | Notes |
|---------|---------|-------|
| Verlet | r(t+Δt) = 2r(t) - r(t-Δt) + FΔt²/m | Time-reversible |
| Velocity Verlet | r(t+Δt) = r(t) + v(t)Δt + ½a(t)Δt² | Most common |
| LJ potential | U = 4ε[(σ/r)¹² - (σ/r)⁶] | Van der Waals |
| Coulomb | U = q₁q₂/(4πε₀r) | Electrostatic |
| Nosé-Hoover | ξ̇ = (T - T₀)/Q | Thermostat |
| Kinetic energy | E_k = ½Σm_i v_i² = (3N/2)k_B T | Temperature |
| Pressure | P = (2E_k + Σr·F)/(3V) | Virial theorem |

---

## Related L2 Nodes

- `statistical_mechanics.md` - Ensemble theory foundation
- `computational_quantum_chemistry.md` - QM/MM methods
- `density_functional_theory.md` - Ab initio MD
- `thermodynamics_laws.md` - Thermodynamic background
- `entropy.md` - Entropy and free energy

---

## L3 Tool Implementations

See: `L3_functions/md_tools.py`

**Functions:**
- `velocity_verlet_step()` - Single integration step
- `apply_thermostat()` - Temperature coupling
- `apply_barostat()` - Pressure coupling
- `calculate_msd()` - Mean square displacement
- `pbc_wrap()` - Periodic boundary conditions

---

## L4 Reference Tables


**Contents:**
- Force field parameters comparison
- Recommended time steps by system type
- Cutoff values and Ewald parameters
- Thermostat/barostat parameters

---

## L5 Worked Examples

See: `L5_worked_examples/md_examples.md`

**Examples:**
- Simple Lennard-Jones MD simulation
- Protein equilibration protocol
- Free energy calculation setup
- Enhanced sampling configuration

---

*Source: Physical Chemistry foundations, LibreTexts, ASE Documentation, Best Practices for Molecular Simulations*
*Created: 2026-03-17*

## L3 Tool Call Directives

**Source:** `md_tools.py`
Molecular dynamics: LJ potential, Verlet integration, PBC, thermostat, observables.

### Available functions:
- `lennard_jones(r, epsilon, sigma)` → Tuple[float, float] — LJ potential U and force F (r in nm, ε in kJ/mol)
- `kinetic_energy(velocities, masses)` → Tuple[float, float] — Kinetic energy (kJ/mol) and temperature (K)
- `velocity_verlet_step(r, v, forces, masses, dt, force_func)` → Tuple[ndarray, ndarray] — Single Verlet integration step
- `pbc_wrap(positions, box_size)` → ndarray — Apply periodic boundary conditions
- `pbc_distance(r1, r2, box_size)` → ndarray — Minimum image convention distance
- `initialize_velocities(n_atoms, temperature, masses, seed)` → ndarray — Maxwell-Boltzmann velocity initialization
- `berendsen_thermostat(velocities, current_temp, target_temp, tau, dt)` → ndarray — Scale velocities toward target T
- `rmsd(r1, r2)` → float — Root mean square deviation between two structures

### Common errors:
- ❌ Forgetting to remove center-of-mass motion after velocity initialization
- ❌ Using non-relativistic electron wavelength for TEM voltages >100 kV
