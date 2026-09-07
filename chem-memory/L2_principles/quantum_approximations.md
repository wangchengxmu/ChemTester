---
id: chem.quantum_approximations
layer: 2
title: Quantum Approximation Methods and Multielectron Atoms
source: LibreTexts Physical Chemistry Ch07-08
status: active
created: 2026-03-14
last_verified: 2026-03-28
down_links:
  - ../L3_functions/quantum_approximations_tools.py
---

# Quantum Approximation Methods and Multielectron Atoms

**L1 Parent:** quantum_mechanics.md

## Problem Types

1. **Variational Method** - Estimate ground state energy with trial wavefunctions
2. **Perturbation Theory** - Correct energies and wavefunctions for small perturbations
3. **Term Symbols** - Determine atomic state notation from electron configuration
4. **Hund's Rules** - Find ground state term symbol
5. **Angular Momentum Coupling** - Combine L, S, J for multielectron atoms
6. **Spin-Orbit Coupling** - Calculate fine structure splitting

## Decision Tree

### 1. What type of approximation is needed?

- **Ground state energy estimate** → Use variational method
- **Small perturbation to known system** → Use perturbation theory
- **Atomic state identification** → Construct term symbol
- **Ground state prediction** → Apply Hund's rules

### 2. Variational Method

- **Trial function with parameter α** → Calculate E(α), minimize ∂E/∂α = 0
- **Linear combination ψ = Σcᵢφᵢ** → Solve secular determinant
- **Key constraint:** E_trial ≥ E_true always!

### 3. Perturbation Theory

- **First-order energy:** E₁ = ⟨ψ⁰|Ĥ'|ψ⁰⟩
- **First-order wavefunction:** |ψ¹⟩ = Σ_{m≠n} |m⁰⟩⟨m⁰|Ĥ'|n⁰⟩/(Eₙ⁰ - Eₘ⁰)
- **Second-order energy:** E₂ = Σ_{m≠n} |⟨m⁰|Ĥ'|n⁰⟩|²/(Eₙ⁰ - Eₘ⁰)

### 4. Term Symbol Construction

- **Count open-shell electrons** → Closed shells contribute L=0, S=0
- **Calculate L** → L = |l₁+l₂|, |l₁+l₂|-1, ..., |l₁-l₂|
- **Calculate S** → S = maximum spin from unpaired electrons
- **Calculate J** → J = |L+S|, |L+S|-1, ..., |L-S|
- **Format:** ^{2S+1}L_J

### 5. Hund's Rules Application

1. Maximize S (highest multiplicity = lowest energy)
2. For same S, maximize L
3. If subshell < half-filled: minimize J
3. If subshell > half-filled: maximize J

### 6. Check Constraints

- Pauli exclusion: No two electrons with same (n, l, mₗ, mₛ)
- Closed shells: L=0, S=0, J=0 → ^1S₀
- Complement rule: pⁿ and p^{6-n} have same terms

---

## Section 1: Variational Method

### The Variational Principle

```
E_trial ≥ E_true

Any trial wavefunction gives energy ≥ true ground state energy.
```

### Trial Energy Formula

```
E_trial = ⟨ψ_trial|Ĥ|ψ_trial⟩ / ⟨ψ_trial|ψ_trial⟩

       = ∫ψ*Ĥψ dτ / ∫ψ*ψ dτ
```

### Optimization Procedure

1. Choose trial function ψ(α) with variational parameter(s)
2. Evaluate E_trial(α) = expectation value
3. Solve ∂E/∂α = 0 for optimal parameter
4. Result: E_opt ≥ E_true (upper bound)

### Example: Helium Atom

```
Trial function: ψ(ζ) = φ₁ₛ(ζ)φ₁ₛ(ζ)
Parameter: ζ = effective nuclear charge

E(ζ) = -R_H(ζ² - 27ζ/8)
∂E/∂ζ = 0 → ζ_opt = 27/16 = 1.6875
E_opt = -77.483 eV (cf. experimental -79.0 eV)
```

### Linear Variational Method

```
ψ_trial = Σᵢ cᵢφᵢ

Secular equations: Σⱼ(Hᵢⱼ - ESᵢⱼ)cⱼ = 0
Secular determinant: |H - ES| = 0

Solve for energies E, then coefficients cᵢ
```

---

## Section 2: Perturbation Theory

### Problem Setup

```
Ĥ = Ĥ⁰ + Ĥ' (or Ĥ¹)

Ĥ⁰|n⁰⟩ = Eₙ⁰|n⁰⟩  (unperturbed, known)

Goal: Find Eₙ ≈ Eₙ⁰ + Eₙ¹ + Eₙ² + ...
```

### First-Order Corrections

```
Energy:    Eₙ¹ = ⟨n⁰|Ĥ'|n⁰⟩  (expectation value of perturbation)

Wavefunction: |n¹⟩ = Σ_{m≠n} cₘₙ|m⁰⟩

where cₘₙ = ⟨m⁰|Ĥ'|n⁰⟩ / (Eₙ⁰ - Eₘ⁰)
```

### Second-Order Energy

```
Eₙ² = Σ_{m≠n} |⟨m⁰|Ĥ'|n⁰⟩|² / (Eₙ⁰ - Eₘ⁰)

Always negative for ground state (stabilizing)
```

### Application Conditions

- Perturbation must be "small": |⟨m⁰|Ĥ'|n⁰⟩| << |Eₙ⁰ - Eₘ⁰|
- Series converges if perturbation is weak

---

## Section 3: Angular Momentum Coupling

### L-S (Russell-Saunders) Coupling

For light atoms (Z < 40):

```
Total orbital:    L = Σᵢ lᵢ
Total spin:       S = Σᵢ sᵢ
Total angular:    J = L + S
```

### Calculating L

```
L = |l₁ + l₂|, |l₁ + l₂| - 1, ..., |l₁ - l₂|

Notation:
  L = 0 → S
  L = 1 → P
  L = 2 → D
  L = 3 → F
  L = 4 → G
```

### Calculating S

```
S = |s₁ + s₂|, |s₁ + s₂| - 1, ..., |s₁ - s₂|

Multiplicity: 2S + 1 (singlet, doublet, triplet, ...)
```

### Calculating J

```
J = |L + S|, |L + S| - 1, ..., |L - S|

Number of J values = 2·min(L,S) + 1
```

### Magnitudes

```
|L| = √(L(L+1)) ℏ
|S| = √(S(S+1)) ℏ
|J| = √(J(J+1)) ℏ
```

---

## Section 4: Term Symbols

### Format

```
^{2S+1}L_J

where:
  2S+1 = multiplicity (superscript)
  L    = total orbital (letter S, P, D, F, ...)
  J    = total angular momentum (subscript)
```

### Construction Procedure

1. Identify open-shell electrons (ignore closed shells)
2. Determine possible L values from individual l values
3. Determine possible S values from electron spins
4. Combine L and S to get possible J values
5. Write term symbol for each combination

### Examples

**Hydrogen (1s¹):**
```
L = 0 → S
S = ½ → multiplicity = 2
J = ½
Term: ²S_{1/2}
```

**Carbon (2p²):**
```
l₁ = l₂ = 1
L = 2, 1, 0 → D, P, S terms
S = 1, 0 → triplets and singlets

Terms: ¹S, ³P, ¹D
```

**Nitrogen (2p³):**
```
Three unpaired electrons
M_L = 1 + 0 + (-1) = 0 → L = 0 → S
M_S = ½ + ½ + ½ = 3/2 → S = 3/2 → multiplicity = 4
J = 3/2
Term: ⁴S_{3/2}
```

---

## Section 5: Hund's Rules

### The Three Rules

**Rule 1:** Maximum S (maximum multiplicity)
- State with highest total spin is most stable
- Electrons with parallel spin avoid each other

**Rule 2:** Maximum L (for same S)
- State with highest orbital angular momentum is most stable
- Electrons orbit in same direction, minimizing repulsion

**Rule 3:** J depends on filling
- Subshell < half-filled: minimum J is most stable
- Subshell > half-filled: maximum J is most stable
- Half-filled: J = L (only one value)

### Application Workflow

```
1. Determine electron configuration
2. List all possible terms
3. Apply Rule 1: Find term(s) with highest S
4. Apply Rule 2: Among those, find highest L
5. Apply Rule 3: Determine optimal J
6. Result: Ground state term symbol
```

### Examples

| Configuration | Filling | Ground State |
|--------------|---------|--------------|
| p¹ | 1/6 (< half) | ²P_{1/2} |
| p² | 2/6 (< half) | ³P₀ |
| p³ | 3/6 (half) | ⁴S_{3/2} |
| p⁴ | 4/6 (> half) | ³P₂ |
| p⁵ | 5/6 (> half) | ²P_{3/2} |
| d¹ | 1/10 (< half) | ²D_{3/2} |
| d⁵ | 5/10 (half) | ⁶S_{5/2} |
| d⁹ | 9/10 (> half) | ²D_{5/2} |

---

## Section 6: Spin-Orbit Coupling

### Interaction Energy

```
E_{s-o} ∝ L·S = L·S·cos(θ)

Ĥ_{s-o} = ξ(r) L·S
```

### L·S from Quantum Numbers

```
L·S = ½[J(J+1) - L(L+1) - S(S+1)] ℏ²
```

### Energy Splitting

```
ΔE_{s-o} = ζ × [J(J+1) - L(L+1) - S(S+1)]

where ζ = spin-orbit coupling constant
```

### Fine Structure

Different J values → different energies
One term splits into multiple fine structure levels

**Example: Sodium D-line**
```
Ground: 3s¹ → ²S_{1/2}
Excited: 3p¹ → ²P

²P splits into:
  ²P_{1/2} (J = 1/2)
  ²P_{3/2} (J = 3/2)

D₁: ²P_{1/2} → ²S_{1/2} at 589.59 nm
D₂: ²P_{3/2} → ²S_{1/2} at 589.00 nm
```

---

## Selection Rules

### Single Electron

```
Δl = ±1
Δmₗ = 0, ±1
```

### L-S Coupling

```
ΔS = 0        (spin cannot change)
ΔL = 0, ±1    (orbital can stay same or change by 1)
ΔJ = 0, ±1    (J can stay same or change by 1)

Forbidden: J = 0 → J = 0
```

---

## Tool Functions

See: `../L3_functions/quantum_approximations_tools.py`

- `variational_energy(trial_function, H)` - Calculate trial energy
- `perturbation_first_order(psi0, H_prime, E0)` - First-order correction
- `perturbation_second_order(psi0, H_prime, basis)` - Second-order correction
- `term_symbol(L, S, J)` - Construct term symbol
- `hund_ground_state(electrons, orbital)` - Apply Hund's rules
- `spin_orbit_energy(L, S, J, zeta)` - Calculate spin-orbit splitting

---

## Cross-References

**L1:** `../L1_ontology/chemistry-core-map.md` (entries 122-123)

**L3:** `../L3_functions/quantum_approximations_tools.py`

**L4:** `../L4_reference/quantum_approximations_reference.md`

**L5:** `../L5_examples/quantum-mechanics/

**Source:** `../sources/ingestion/source-quantum_approximations-stepwise.md`

## L3 Tool Call Directives

**Source:** `quantum_approximations_tools.py`
Quantum mechanics approximations: variational method, perturbation theory, term symbols, angular momentum.

### Available functions:
- `variational_energy(trial_params, Hamiltonian_func)` → dict — Calculate variational energy and compare to exact
- `variational_energy_with_param(alpha, exact_energy, domain)` → dict — Hydrogen-like variational calculation with parameter α
- `perturbation_first_order_energy(H0_func, H1_func, psi0_func)` → float — First-order energy correction E⁽¹⁾ = ⟨ψ₀|Ĥ₁|ψ₀⟩
- `perturbation_first_order_wavefunction(H0_func, H1_func, psi0_func)` → dict — First-order wavefunction correction
- `perturbation_second_order_energy(H0_func, H1_func, psi0_func)` → float — Second-order energy correction
- `possible_L_values(l1, l2)` → List[int] — Possible L values for two electrons (|l1-l2| to l1+l2)
- `possible_S_values(n_electrons)` → List[float] — Possible S values for n electrons
- `possible_J_values(L, S)` → List[float] — Possible J values from |L-S| to L+S
- `L_to_term_letter(L)` → str — Convert L quantum number to spectroscopic letter (S,P,D,F...)
- `term_symbol(L, S, J)` → str — Construct full term symbol e.g., ³P₂
- `multiplicity(S)` → int — Calculate multiplicity 2S+1
- `degeneracy(J)` → int — Calculate degeneracy 2J+1
- `hund_ground_state(orbital_type, n_electrons)` → dict — Predict ground state term using Hund's rules
- `spin_orbit_coupling_energy(zeta, L, S, J)` → float — Spin-orbit coupling energy E_SO = ζ·[J(J+1)-L(L+1)-S(S+1)]/2
- `fine_structure_splitting(zeta, L, S)` → dict — Calculate fine structure level splitting
- `transition_allowed(L1, S1, J1, L2, S2, J2)` → bool — Check electric dipole selection rules
- `angular_momentum_magnitude(j)` → float — |J| = ℏ√(j(j+1))
- `z_component(j, m)` → float — J_z = ℏm
- `count_microstates(orbital_type, n_electrons)` → int — Count possible microstates

### Common errors:
- ❌ Applying first-order perturbation without checking if ⟨ψ₀|Ĥ₁|ψ₀⟩ is zero (need second-order)
- ❌ Confusing Hund's first rule (max S) with second rule (max L for given S)
