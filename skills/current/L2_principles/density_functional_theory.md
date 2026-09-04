---
id: chem.dft
layer: 2
title: Density Functional Theory (DFT)
source: Physical Chemistry foundations; LibreTexts; Academic sources
status: active
created: 2026-03-17
last_verified: 2026-03-17
---

# Density Functional Theory (DFT)

**L1 Parent:** computational_quantum_chemistry.md

## Problem Types

1. **Ground state energy calculation** - Find E? from electron density ¦Ñ(r)
2. **Geometry optimization** - Minimize energy with respect to nuclear coordinates
3. **Electronic structure analysis** - Orbital energies, densities, bonding
4. **Vibrational frequency calculation** - Second derivatives of energy
5. **Transition state search** - Saddle point on potential energy surface
6. **Property prediction** - Dipole moments, polarizabilities, NMR shifts

## Decision Tree

### 1. What DFT method is appropriate?

```
System requirements ¡ú Method choice

Quick screening ¡ú LDA (fast, qualitative)
General chemistry ¡ú GGA (BLYP, PBE)
Accurate thermochemistry ¡ú Hybrid (B3LYP, PBE0)
Transition metals ¡ú Meta-GGA (TPSS) or hybrid meta-GGA (M06)
Weak interactions ¡ú Dispersion-corrected (¦ØB97X-D, B3LYP-D3)
Band gaps/excitations ¡ú Range-separated hybrid (CAM-B3LYP, ¦ØB97X)
```

### 2. Basis set selection for DFT

```
Neutral molecules ¡ú 6-31G* (balanced)
Geometry optimization ¡ú def2-SVP (modern split-valence)
Accurate energies ¡ú def2-TZVP or 6-311G**
Weak interactions ¡ú aug-cc-pVTZ (diffuse functions)
Transition metals ¡ú def2-TZVP with ECP for heavy metals
Large systems ¡ú Minimal basis or plane-wave (periodic)
```

---

## Section 1: Hohenberg-Kohn Theorems

### First Hohenberg-Kohn Theorem

**Statement:** The ground state electron density ¦Ñ(r) uniquely determines the external potential V_ext(r) (up to an additive constant), and therefore all properties of the ground state.

```
¦Ñ(r) ¡ú V_ext(r) ¡ú ? ¡ú ¦·? ¡ú All ground state properties

Implication: ¦Ñ(r) is a fundamental variable, not just an observable
```

**Proof sketch:**
1. Assume two potentials V? and V? give same ¦Ñ(r)
2. Both give ground states ¦·? and ¦·?
3. By variational principle: E? < ?¦·?|??|¦·?? and E? < ?¦·?|??|¦·??
4. Adding inequalities leads to contradiction
5. Therefore V_ext is uniquely determined by ¦Ñ

### Second Hohenberg-Kohn Theorem

**Statement:** A universal functional F[¦Ñ] exists such that the energy functional:

```
E[¦Ñ] = F[¦Ñ] + ¡Ò V_ext(r) ¦Ñ(r) dr

is minimized by the true ground state density ¦Ñ?(r)
```

**Universal functional:**
```
F[¦Ñ] = T[¦Ñ] + V_ee[¦Ñ]

where:
T[¦Ñ] = kinetic energy of interacting electrons
V_ee[¦Ñ] = electron-electron repulsion energy
```

**Variational principle for DFT:**
```
E[¦Ñ] ¡Ý E?    for all N-electron densities ¦Ñ
E[¦Ñ?] = E?   (equality for ground state density)

¦ÄE[¦Ñ]/¦Ä¦Ñ = 0  at ground state
```

### Constrained Search Formulation (Levy)

**Extended functional:**
```
F[¦Ñ] = min_¦·¡ú¦Ñ ?¦·|T? + V?_ee|¦·?

Search over all ¦· giving density ¦Ñ
```

This formulation:
- Handles degenerate ground states
- Provides constructive definition
- Proves F[¦Ñ] exists without uniqueness proof

---

## Section 2: Kohn-Sham Equations

### Strategy

Replace interacting electrons with non-interacting reference system that has the same density.

**Key insight:** If we can find a potential V_KS(r) such that non-interacting electrons have density ¦Ñ(r), we can compute:

```
T_s[¦Ñ] = kinetic energy of non-interacting electrons (exactly)

But T[¦Ñ] ¡Ù T_s[¦Ñ]  (correlation difference must be in E_xc)
```

### Energy Decomposition

```
E[¦Ñ] = T_s[¦Ñ] + V_ne[¦Ñ] + J[¦Ñ] + E_xc[¦Ñ]

where:
T_s[¦Ñ]   = kinetic energy (non-interacting reference)
V_ne[¦Ñ]  = nuclear-electron attraction
J[¦Ñ]     = Coulomb repulsion (Hartree energy)
E_xc[¦Ñ]  = exchange-correlation (unknown, must approximate)
```

**Exchange-correlation contains:**
```
E_xc[¦Ñ] = (T[¦Ñ] - T_s[¦Ñ]) + (V_ee[¦Ñ] - J[¦Ñ])
        = T_corr + E_exchange + E_correlation
```

### Kohn-Sham Equations

**One-electron equations:**
```
[-??2 + V_eff(r)] ¦Õ?(r) = ¦Å? ¦Õ?(r)

V_eff(r) = V_ne(r) + V_H(r) + V_xc(r)

where:
V_H(r) = ¡Ò ¦Ñ(r')/|r-r'| dr'           (Hartree potential)
V_xc(r) = ¦ÄE_xc[¦Ñ]/¦Ä¦Ñ(r)              (XC potential)
```

**Density from orbitals:**
```
¦Ñ(r) = ¦²?? |¦Õ?(r)|2    (occupied orbitals only)

For spin-polarized:
¦Ñ(r) = ¦Ñ¡ü(r) + ¦Ñ¡ý(r) = ¦²?¡ü |¦Õ?¡ü(r)|2 + ¦²?¡ý |¦Õ?¡ý(r)|2
```

### Self-Consistent Field Procedure

```
1. Guess initial density ¦Ñ???(r)

2. Construct V_eff[¦Ñ]:
   - V_ne: nuclear attraction (fixed)
   - V_H: Coulomb from density
   - V_xc: from XC functional

3. Solve KS equations for orbitals ¦Õ?

4. Compute new density: ¦Ñ?1?(r) = ¦²|¦Õ?|2

5. Check convergence: |¦Ñ?1? - ¦Ñ???| < threshold

6. If not converged, mix densities and iterate (steps 2-5)
```

---

## Section 3: Exchange-Correlation Functionals

### Jacob's Ladder of DFT

```
                     Chemical Accuracy
                           ¡ü
    ©°©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©´
    ©¦ 5. Double Hybrid (B2PLYP)               ©¦ ¡û ~1 kcal/mol
    ©¦    E_xc = E_x[DFA] + E_c[DFA] + E_c[MP2]©¦
    ©À©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©È
    ©¦ 4. Meta-GGA (TPSS, M06)                 ©¦ ¡û Better kinetics
    ©¦    E_xc[¦Ñ, ?¦Ñ, ?2¦Ñ, ¦Ó]                  ©¦
    ©À©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©È
    ©¦ 3. Hybrid (B3LYP, PBE0)                 ©¦ ¡û Most common
    ©¦    E_xc = ¦Á¡¤E_x[HF] + (1-¦Á)¡¤E_x[GGA]    ©¦
    ©À©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©È
    ©¦ 2. GGA (BLYP, PBE)                      ©¦ ¡û Good balance
    ©¦    E_xc[¦Ñ, ?¦Ñ]                          ©¦
    ©À©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©È
    ©¦ 1. LDA (SVWN)                           ©¦ ¡û Foundation
    ©¦    E_xc[¦Ñ]                              ©¦
    ©¸©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¤©¼
```

### LDA (Local Density Approximation)

**Form:**
```
E_xc^LDA[¦Ñ] = ¡Ò ¦Ñ(r) ¦Å_xc(¦Ñ(r)) dr

¦Å_xc(¦Ñ) = XC energy per electron of uniform electron gas
```

**Exchange (Dirac):**
```
¦Å_x(¦Ñ) = -C_x ¦Ñ^(1/3)

C_x = -(3/4)(3/¦Ð)^(1/3) ¡Ö -0.7386

E_x^LDA = -C_x ¡Ò ¦Ñ^(4/3) dr
```

**Properties:**
- Exact for uniform electron gas
- Overbinds molecules (10-20% error in atomization energies)
- Too delocalized densities
- Good for metals and solid state

### GGA (Generalized Gradient Approximation)

**Form:**
```
E_xc^GGA[¦Ñ] = ¡Ò f(¦Ñ(r), ?¦Ñ(r)) dr

Adds dependence on density gradient
```

**Common GGAs:**

| Functional | Exchange | Correlation | Notes |
|------------|----------|-------------|-------|
| BLYP | Becke88 | LYP | Popular for molecules |
| PBE | PBE | PBE | Good for solids |
| BP86 | Becke88 | Perdew86 | Thermochemistry |

**Becke88 exchange:**
```
E_x^B88 = E_x^LDA - ¦Â ¡Ò ¦Ñ^(4/3) x2/(1 + 6¦Âx sinh?1x) dr

x = |?¦Ñ|/¦Ñ^(4/3)  (reduced gradient)
¦Â = 0.0042 (empirical parameter)
```

**PBE (non-empirical):**
- Satisfies known exact conditions
- No fitted parameters
- Good across chemistry and physics

### Hybrid Functionals

**Strategy:** Mix exact (HF) exchange with DFT exchange

```
E_xc^hybrid = ¦Á E_x^HF + (1-¦Á) E_x^DFT + E_c^DFT

¦Á = fraction of exact exchange
```

**B3LYP (most popular):**
```
E_xc^B3LYP = 0.20 E_x^HF + 0.80 E_x^B88 + 0.19 E_c^VWN + 0.81 E_c^LYP

Three-parameter hybrid (empirical coefficients)
```

**PBE0 (PBE hybrid):**
```
E_xc^PBE0 = 0.25 E_x^HF + 0.75 E_x^PBE + E_c^PBE

25% exact exchange from perturbation theory argument
```

**Why hybrids work:**
- Exact exchange cancels self-interaction error
- Better description of charge transfer
- Improved band gaps
- Standard for organic molecules

### Meta-GGA Functionals

**Form:**
```
E_xc^meta-GGA[¦Ñ] = ¡Ò f(¦Ñ, ?¦Ñ, ?2¦Ñ, ¦Ó) dr

¦Ó(r) = (1/2) ¦² |?¦Õ?(r)|2  (kinetic energy density)
```

**TPSS (Tao-Perdew-Staroverov-Scuseria):**
- Non-empirical meta-GGA
- Better for transition metals
- Improved thermochemistry

**M06 family:**
- Highly parameterized
- M06-2X: 54% exact exchange (good for kinetics)
- M06-L: 0% exact exchange (good for transition metals)
- Good for non-covalent interactions

### Range-Separated Hybrids

**Strategy:** Exchange fraction varies with interelectronic distance

```
1/r = [¦Á + ¦Â¡¤erf(¦Ìr)]/r + [1-¦Á - ¦Â¡¤erf(¦Ìr)]/r
      ©¸©¤©¤©¤©¤©¤©¤©¤ short-range ©¤©¤©¤©¤©¤©¤©¤©¼   ©¸©¤©¤©¤ long-range ©¤©¤©¤©¤©¼

Short-range: DFT exchange
Long-range: HF exchange (better for charge transfer)
```

**CAM-B3LYP:**
```
E_xc = ¦Á E_x^HF(SR) + (1-¦Á) E_x^DFT(SR) + ¦Â E_x^HF(LR) + E_c^DFT

¦Á = 0.19, ¦Â = 0.46, ¦Ì = 0.33
```

**¦ØB97X-D:**
- Range-separated + dispersion
- Excellent for excited states
- Good for non-covalent interactions

### Dispersion Corrections

**Problem:** Standard DFT misses van der Waals (dispersion) interactions

**DFT-D3 (Grimme):**
```
E_disp = -s? ¦²?<? C?^ij/(R_ij? + f(R_ij)?)

C?^ij = dispersion coefficient (element pair dependent)
s? = scaling factor (functional-dependent)
```

**Common dispersion-corrected functionals:**
- B3LYP-D3
- ¦ØB97X-D
- PBE0-D3
- B97-D3

---

## Section 4: Basis Sets for DFT

### Gaussian Basis Sets

**Standard molecular calculations use Gaussian-type orbitals (GTOs):**

| Basis | Description | Use Case |
|-------|-------------|----------|
| 6-31G* | Split-valence + polarization | General purpose |
| 6-311G** | Triple-zeta + polarization | Accurate energies |
| def2-SVP | Def2 split-valence polarization | Modern standard |
| def2-TZVP | Def2 triple-zeta | Production level |
| cc-pVDZ | Correlation-consistent double | Systematic improvement |
| cc-pVTZ | Correlation-consistent triple | High accuracy |
| aug-cc-pVTZ | + diffuse functions | Anions, Rydberg states |

### Plane Wave Basis (Periodic Systems)

**Used for:**
- Crystals and solids
- Surfaces and interfaces
- Large periodic systems

**Form:**
```
¦Õ_k(r) = exp(ik¡¤r)  (plane wave)

Expand KS orbitals:
¦×?(r) = ¦²_G c_{i,G} exp[i(k+G)¡¤r]

G = reciprocal lattice vectors
```

**Pseudopotentials/PAW:**
- Replace core electrons with effective potential
- Reduce plane wave cutoff
- VASP, Quantum ESPRESSO use PAW method

---

## Section 5: Common DFT Software

### Gaussian

**Strengths:**
- Industry standard
- Wide range of functionals
- Good documentation

**Example:**
```
# B3LYP/6-31G* Opt Freq
```

### VASP (Vienna Ab initio Simulation Package)

**Strengths:**
- Plane-wave DFT
- Periodic systems
- Materials science standard
- PAW pseudopotentials

**Applications:**
- Crystal structures
- Surfaces and interfaces
- Molecular dynamics

### ORCA

**Strengths:**
- Free for academics
- Excellent for spectroscopy
- Good for transition metals
- Supports DLPNO for large systems

**Example:**
```
! B3LYP def2-TZVP TightSCF Grid5

*xyz 0 1
C 0.0 0.0 0.0
...
*
```

### Quantum ESPRESSO

**Strengths:**
- Plane-wave DFT
- Open source
- Materials simulations

---

## Section 6: DFT Accuracy and Limitations

### Typical Accuracy

| Property | Typical Error |
|----------|---------------|
| Bond lengths | 0.01-0.02 ? |
| Bond angles | 1-2¡ã |
| Vibrational frequencies | 1-5% |
| Atomization energies | 5-10 kcal/mol |
| Reaction barriers | 5-10 kcal/mol |
| Ionization potentials | 0.2-0.3 eV |

### Known Problems

**1. Self-Interaction Error (SIE)**
```
Hartree energy includes self-repulsion:
E_H = (1/2) ¡Ò¡Ò ¦Ñ(r)¦Ñ(r')/|r-r'| dr dr'

But electron doesn't repel itself!
XC must cancel this ¡ª LDA/GGA don't fully

Consequences:
- Delocalization error
- Underestimated band gaps
- Wrong dissociation limits
```

**2. Static Correlation**
```
DFT (single-reference) fails for:
- Bond breaking
- Transition metal complexes with multi-reference character
- Diradicals

Solution: Use multi-reference methods (CASSCF)
```

**3. Charge Transfer Excitations**
```
Standard functionals underestimate CT excitation energies

Solution: Range-separated hybrids (CAM-B3LYP, ¦ØB97X)
```

**4. Dispersion**
```
Standard DFT misses van der Waals

Solution: DFT-D3, vdW-DF, or range-separated with dispersion
```

### Functional Selection Guide

| Application | Recommended Functional |
|-------------|----------------------|
| Organic molecules | B3LYP-D3/6-31G* |
| Thermochemistry | PBE0/def2-TZVP |
| Transition metals | TPSSh or M06-L |
| Kinetics (barriers) | M06-2X |
| Non-covalent interactions | ¦ØB97X-D |
| Excited states | CAM-B3LYP or ¦ØB97X-D |
| Solids/metals | PBE (plane-wave) |
| Large systems | B3LYP-D3/def2-SVP |

---

## Key Formulas Summary

| Concept | Formula |
|---------|---------|
| Hohenberg-Kohn I | ¦Ñ? ¡ú V_ext ¡ú ? ¡ú ¦·? (unique) |
| Hohenberg-Kohn II | E[¦Ñ] ¡Ý E?, minimized by ¦Ñ? |
| KS energy | E = T_s + V_ne + J + E_xc |
| KS equation | [-??2 + V_eff]¦Õ = ¦Å¦Õ |
| Effective potential | V_eff = V_ne + V_H + V_xc |
| Hartree potential | V_H(r) = ¡Ò¦Ñ(r')/|r-r'| dr' |
| XC potential | V_xc = ¦ÄE_xc/¦Ä¦Ñ |
| Density | ¦Ñ(r) = ¦²?|¦Õ?|2 |
| LDA exchange | E_x ¡Ø ¡Ò¦Ñ^(4/3) dr |
| Hybrid | E_xc = ¦ÁE_x^HF + (1-¦Á)E_x^DFT + E_c^DFT |

---

## Related L2 Nodes

- `computational_quantum_chemistry.md` - Hartree-Fock, post-HF methods
- `quantum_mechanics_core.md` - Schr?dinger equation foundation
- `molecular_orbital_theory.md` - MO theory for bonding
- `quantum_approximations.md` - Variational and perturbation methods

---

## L3 Tool Implementations

See: `L3_functions/dft_tools.py`

**Functions:**
- `functional_type()` - Classify XC functional (LDA/GGA/hybrid/etc.)
- `basis_set_recommendation()` - Suggest basis for system type
- `scf_convergence_check()` - Diagnose SCF failures

---

## L4 Reference Tables

See: `../L4_reference/dft_functionals_table.md`

**Contents:**
- Complete functional listing with parameters
- Performance benchmarks by property type
- Basis set recommendations

---

## L5 Worked Examples

See: `L5_worked_examples/dft_examples.md`

**Examples:**
- H?O geometry optimization with B3LYP
- CO orbital analysis
- Transition metal complex
- Non-covalent interaction energy

---

*Source: Physical Chemistry foundations, LibreTexts, Academic sources*
*Created: 2026-03-17*


## Implementations

- Implementation: `../L3_functions/computational_chemistry_tools.py`
