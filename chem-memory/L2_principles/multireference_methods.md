# Multireference Methods

## Concept Overview
Multireference methods treat systems where a single Slater determinant (Hartree-Fock) is inadequate. Essential for bond breaking, transition metals, excited states, and diradicals.

## When Multireference Methods Are Needed
- Near-degenerate frontier orbitals (e.g., bond dissociation, O₂, NO).
- Strongly correlated systems (transition metal complexes, actinides).
- Excited states with double-excitation character.
- **T₁ diagnostic**: T₁ > 0.02 (CCSD) suggests multireference character.

## CASSCF (Complete Active Space SCF)

### Theory
Wavefunction is full CI within an active space of selected orbitals:
|Ψ_CASSCF⟩ = Σ c_I |I⟩ (over all configurations in active space)

Active space notation: CAS(n,m) = n electrons in m orbitals.

### Common Active Spaces
| System | Active Space | Description |
|---|---|---|
| Ozone (O₃) | CAS(6,6) | π system + lone pairs |
| Cr₂ | CAS(12,12) | d-electrons + bonding |
| Fe(II) porphyrin | CAS(14,14) | d-orbitals + π system |
| Butadiene | CAS(4,4) | π-valence electrons |
| Transition states | CAS(x,y) | Bond breaking orbitals |

### Steps in CASSCF Calculation
1. Choose active space (critical step!).
2. State-averaged CASSCF (SA-CASSCF): optimize orbitals for multiple states simultaneously.
3. Dynamic correlation: Add on top of CASSCF wavefunction.

### Dynamic Correlation on Top of CASSCF
| Method | Description | Scaling |
|---|---|---|
| CASPT2 | Second-order perturbation | N⁶ |
| NEVPT2 | N-electron valence PT2 (no intruder states) | N⁶ |
| MRCI | Multireference CI | N⁷ |
| MR-AQCC | Averaged quadratic CC | N⁷ |

### Limitations
- **Active space explosion**: CAS(n,m) scales as C(2m,n) configurations.
- **Intruder states**: CASPT2 can diverge; level shift or IPEA shift used.
- **Orbital choice**: Results can depend heavily on initial orbital guess.

## Sources
[Source: Wikipedia, CASSCF]
[Source: Roos et al., Multiconfigurational quantum chemistry, 2004]

## L3 Tools
-> `../L3_functions/quantum_tools.py` — `casscf_energy()`, `caspt2_correction()`
