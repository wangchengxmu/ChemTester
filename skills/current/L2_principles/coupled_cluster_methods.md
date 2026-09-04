# Coupled Cluster Methods

## Concept Overview
Coupled cluster (CC) theory is a size-extensive, highly accurate ab initio electronic structure method. Considered the "gold standard" for single-reference molecular systems.

## Theoretical Framework

### Exponential Ansatz
|Ψ⟩ = e^T |Φ₀⟩

Where:
- |Φ₀⟩ = Hartree-Fock reference determinant
- T = T₁ + T₂ + T₃ + ... (cluster operator)
- Tₙ generates all n-tuple excitations

### Common Approximations
| Method | Excitations Included | Scaling | Accuracy |
|---|---|---|---|
| CCSD | T₁ + T₂ | N⁶ | Chemical accuracy for many systems |
| CCSD(T) | CCSD + perturbative T₃ | N⁷ | "Gold standard"; ~1 kcal/mol accuracy |
| CCSDT | T₁ + T₂ + T₃ | N⁸ | Very accurate, expensive |
| CCSDT(Q) | + perturbative T₄ | N⁹ | Benchmark quality |

### Energy Expression
E_CC = ⟨Φ₀|e^(-T) H e^T|Φ₀⟩ = ⟨Φ₀|H̄|Φ₀⟩

Where H̄ = e^(-T) H e^T is the similarity-transformed Hamiltonian.

### Amplitude Equations (Connected)
⟨Φᵢᵃ|H̄|Φ₀⟩ = 0 (singles)
⟨Φᵢⱼᵃᵇ|H̄|Φ₀⟩ = 0 (doubles)

Only connected diagrams contribute → size extensivity.

## Key Properties
- **Size extensive**: Energy scales correctly with system size (no unphysical delocalization error).
- **Size consistent**: Non-interacting fragments have additive energies.
- **Invariant to orbital rotations**: Unlike MP2, CC is insensitive to orbital choice.
- **Not variational**: CC energy can be below true energy (but usually very close).

## Scaling and Practical Considerations
- CCSD(T)/cc-pVTZ is standard for benchmark thermochemistry.
- **DLPNO-CCSD(T)**: Domain-based local pair natural orbital approximation, N⁴–N⁵ scaling, ~99.9% of canonical CCSD(T) correlation energy.
- **Explicitly correlated** (F12): Faster basis set convergence.

## Sources
[Source: Wikipedia, Coupled cluster]
[Source: Bartlett & Musiał, Rev. Mod. Phys. 2007]

## L3 Tools
-> `../L3_functions/quantum_tools.py` — `ccsd_energy()`, `ccsdt_correction()`
