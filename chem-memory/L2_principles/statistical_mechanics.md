# Statistical Mechanics - L2 Principle

**Topic:** Statistical Mechanics (Boltzmann Factor & Partition Functions)
**Source:** LibreTexts Physical Chemistry Ch17-18
**L1 Parent:** thermodynamics.md, quantum_mechanics.md
**L3 Implementation:** ../L3_functions/statistical_mechanics_tools.py

---

## Core Concept

Statistical mechanics bridges microscopic quantum states and macroscopic thermodynamic properties. It provides the foundation for calculating thermodynamic quantities from molecular properties.

### The Central Object: Partition Function

The **partition function** Z (or Q) encodes all thermodynamic information:

```
Z = ¦²? exp(-E?/kT)
```

Everything follows from Z through derivatives.

---

## Key Formulas

### 1. Boltzmann Factor

**Purpose:** Weight for state with energy E at temperature T

```
exp(-E/kT) = exp(-¦ÂE)
```

where:
- k = 1.380649 ¡Á 10?23 J/K (Boltzmann constant)
- ¦Â = 1/kT
- Higher energy states are exponentially suppressed

### 2. Boltzmann Distribution

**Purpose:** Probability of finding system in state i

```
P? = exp(-E?/kT) / Z
```

where Z = ¦²? exp(-E?/kT) is the partition function.

**Constraints:**
- ¦²? P? = 1 (normalization)
- Lower energy states more probable at low T
- All states have non-zero probability (except T=0)

### 3. Partition Function Hierarchy

**Molecular (single molecule):**
```
q = ¦²? exp(-¦Å?/kT)
```

**Ensemble (N molecules):**
```
Z = q^N          (distinguishable)
Z = q^N / N!     (indistinguishable)
```

### 4. Decomposition by Degree of Freedom

```
q_total = q_trans ¡Á q_rot ¡Á q_vib ¡Á q_elec
```

**Why separable:** Energy is additive when degrees of freedom are independent.

---

## Translational Partition Function

**Applies to:** All gases

```
q_trans = V / ¦«3
```

where ¦« = h / ¡Ì(2¦ÐmkT) is the thermal de Broglie wavelength.

**Properties:**
- Very large (¡Ö102? for 1 cm3)
- Many states accessible
- Always use integral approximation

**Temperature dependence:** q_trans ¡Ø T^(3/2)

---

## Rotational Partition Function

**Applies to:** Diatomic and polyatomic molecules

### Diatomic Molecules

```
q_rot = T / (¦¨_rot ¡Á ¦Ò)
```

where:
- ¦¨_rot = ?2 / (2Ik) = rotational temperature
- ¦Ò = symmetry number
- I = ¦Ìr2 = moment of inertia

**Symmetry Numbers:**
| Type | ¦Ò | Examples |
|------|---|----------|
| Heteronuclear | 1 | HCl, CO, NO |
| Homonuclear | 2 | H?, N?, O? |

**Approximation valid when:** T >> ¦¨_rot

### Polyatomic Molecules

**Linear:** Same as diatomic

**Nonlinear:**
```
q_rot = ¡Ì(¦Ð/¦Ò) ¡Á (T3/(¦¨_A ¡Á ¦¨_B ¡Á ¦¨_C))^(1/2)
```

---

## Vibrational Partition Function

**Applies to:** Molecules with internal vibrations

### Single Mode

```
q_vib = 1 / (1 - exp(-¦¨_vib/T))
```

where ¦¨_vib = h¦Í/k = vibrational temperature

### Multiple Modes

```
q_vib = ¦°? 1/(1 - exp(-¦¨_vib,i/T))
```

**Number of modes:**
- Linear polyatomic: 3N - 5
- Nonlinear polyatomic: 3N - 6

**Key insight:** Most molecules in ground vibrational state at room T

---

## Electronic Partition Function

```
q_elec = ¦²? g? exp(-E?/kT)
```

At typical temperatures: q_elec ¡Ö g? (ground state degeneracy only)

---

## Thermodynamic Properties from Z

### Internal Energy

```
U = kT2 (?ln Z/?T)_V
```

### Entropy

```
S = k ln Z + U/T
```

**Sackur-Tetrode (monatomic ideal gas):**
```
S/Nk = ln(V/N ¡Á (2¦ÐmkT/h2)^(3/2)) + 5/2
```

### Helmholtz Free Energy

```
A = -kT ln Z
```

### Gibbs Free Energy

```
G = A + PV
```

### Pressure

```
P = kT (?ln Z/?V)_T
```

### Heat Capacity

```
C_V = (?U/?T)_V
```

---

## Equipartition Principle

**Classical limit:** Each quadratic degree of freedom contributes ?kT to average energy.

| DOF Type | Energy (per molecule) | Heat Capacity |
|----------|----------------------|---------------|
| Translation (3D) | 3/2 kT | 3/2 k |
| Rotation (linear) | kT | k |
| Rotation (nonlinear) | 3/2 kT | 3/2 k |
| Vibration (high T) | kT | k |

**Note:** Equipartition fails when kT << energy level spacing

---

## Common Pitfalls

1. **Forgetting N!** for indistinguishable particles
2. **Using integral approximation** when T ¡Ö ¦¨_rot (light gases)
3. **Including zero-point energy** inconsistently
4. **Wrong symmetry number** for homonuclear molecules
5. **Applying equipartition** to frozen-out modes

---

## Decision Tree: Which Partition Function?

```
Is it a gas?
©À©¤©¤ Yes ¡ú Include q_trans
©¦   ©¸©¤©¤ Monatomic?
©¦       ©À©¤©¤ Yes ¡ú q_total = q_trans ¡Á q_elec
©¦       ©¸©¤©¤ No ¡ú Diatomic?
©¦           ©À©¤©¤ Yes ¡ú q_total = q_trans ¡Á q_rot ¡Á q_vib ¡Á q_elec
©¦           ©¸©¤©¤ No ¡ú Polyatomic
©¦               ©¸©¤©¤ q_total = q_trans ¡Á q_rot ¡Á q_vib ¡Á q_elec
©¸©¤©¤ No ¡ú Different treatment (not covered here)
```

---

## Connections to Other Topics

- **Thermodynamics:** Z ¡ú all thermodynamic properties
- **Quantum Mechanics:** Energy levels from Schr?dinger equation
- **Kinetics:** Transition state theory uses partition functions
- **Spectroscopy:** Rotational/vibrational spectra give ¦¨_rot, ¦¨_vib

---

## L3 Tools Required

1. `boltzmann_factor(energy, temperature)` ¡ú exp(-E/kT)
2. `partition_function_canonical(energies, temperature)` ¡ú Z
3. `boltzmann_probability(energy, partition_function, temperature)` ¡ú P?
4. `translational_partition_function(mass, volume, temperature)` ¡ú q_trans
5. `rotational_partition_function(I, temperature, sigma)` ¡ú q_rot
6. `vibrational_partition_function(frequency, temperature)` ¡ú q_vib
7. `internal_energy_from_Z(Z, temperature)` ¡ú U
8. `entropy_from_Z(Z, temperature)` ¡ú S
9. `helmholtz_from_Z(Z, temperature)` ¡ú A

---

## Quick Reference

| Quantity | Formula | Units |
|----------|---------|-------|
| ¦Â | 1/kT | J?1 |
| ¦« | h/¡Ì(2¦ÐmkT) | m |
| ¦¨_rot | ?2/(2Ik) | K |
| ¦¨_vib | h¦Í/k | K |
| q_trans | V/¦«3 | dimensionless |
| q_rot | T/(¦¨_rot ¡Á ¦Ò) | dimensionless |
| q_vib | 1/(1-exp(-¦¨_vib/T)) | dimensionless |

---

*L2 Principle Document*
*Generated: 2026-03-14*


## Implementations

- Implementation: `../L3_functions/statistical_thermodynamics_tools.py`

## L3 Tool Call Directives

**Source:** `statistical_mechanics_tools.py`

Partition functions (translational, rotational, vibrational), Boltzmann distributions, thermodynamic properties from Z, heat capacities. Requires numpy/scipy.

### Available functions:
- `boltzmann_factor(energy, temperature)` → float — exp(-E/kT)
- `partition_function_canonical(energies, temperature)` → float — Z = Σ exp(-Eᵢ/kT)
- `boltzmann_probability(energy, partition_function, temperature)` → float — Pᵢ = exp(-Eᵢ/kT)/Z
- `translational_partition_function(mass, volume, temperature)` → float — q_trans = V/Λ³
- `rotational_partition_function(moment_of_inertia, temperature, sigma=1)` → float — q_rot = T/(Θ_rot×σ)
- `rotational_partition_function_from_B(B_cm, temperature, sigma=1)` → float — From rotational constant
- `vibrational_partition_function(frequency_Hz, temperature, include_zpe=False)` → float — q_vib
- `vibrational_partition_function_from_wavenumber(wavenumber_cm, temperature, include_zpe=False)` → float — From cm⁻¹
- `internal_energy_translational(temperature)` → float — U_trans = 3/2 kT
- `internal_energy_rotational(temperature, linear=True)` → float — kT (linear) or 3/2 kT (nonlinear)
- `internal_energy_vibrational(frequency_Hz, temperature)` → float — U_vib per mode
- `heat_capacity_translational(molar=False)` → float — C_V = 3/2 k (or R)
- `heat_capacity_rotational(linear=True, molar=False)` → float — C_V rotational contribution
- `heat_capacity_vibrational(frequency_Hz, temperature, molar=False)` → float — C_V vibrational
- `helmholtz_free_energy(partition_function, temperature)` → float — A = -kT ln Z
- `gibbs_free_energy(partition_function, temperature, pressure=101325)` → float — G = A + kT
- `entropy_sackur_tetrode(mass, volume, temperature, N=1)` → float — Monatomic ideal gas entropy
- `get_partition_functions(molecule, temperature, volume=1e-3)` → Dict — All q for H₂/N₂/O₂/CO/HCl/I₂
- `fraction_in_vibrational_state(v, theta_vib, temperature)` → float — Population in state v
- `population_ratio(energy1, energy2, temperature)` → float — N₂/N₁ between levels

### Common errors:
- ❌ Using amu for mass instead of kg (multiply by 1.66054e-27)
- ❌ Wrong symmetry number σ: 1 for heteronuclear (HCl), 2 for homonuclear (N₂)
- ❌ Using cm⁻¹ for frequency_Hz parameter — convert via wavenumber_to_frequency first
