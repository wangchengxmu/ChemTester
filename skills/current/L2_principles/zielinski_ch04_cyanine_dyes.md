# Electronic Spectroscopy of Cyanine Dyes — Zielinski Ch4

**Source:** Quantum States of Atoms and Molecules, Ch4

## Key Concepts

- **Particle-in-a-box (PIB)** model applied to cyanine dyes
- Cyanine dyes: conjugated polymethine chain between two nitrogen atoms
- Free electrons in π-system modeled as particles in 1D box
- **Box length L** = polyene chain length + one bond length on each end

### Key Formulas

| Formula | Description |
|---------|-------------|
| E_n = n²h²/(8mL²) | PIB energy levels |
| ΔE = E_{n+1} − E_n = (2n+1)h²/(8mL²) | Transition energy |
| λ = hc/ΔE | Absorption wavelength |
| ψ_n = √(2/L) sin(nπx/L) | PIB wavefunctions |

### Selection Rules (PIB)
- **Δn = ±1** for electric dipole transitions
- Derived from transition moment integral: M = ∫ψ*_{n'} μ̂ ψ_n dx
- Even↔odd parity selection rule: only transitions changing parity are allowed

### Application to Cyanine Dyes
- Number of π-electrons = p+3 (p = number of CH=CH groups)
- HOMO→LUMO transition: n → n+1 where n = (p+3)/2
- Predicted λ compared with experimental absorption maxima
- Good agreement validates PIB model for conjugated systems

## Cross-References
- **L2:** cyanine_dye_spectroscopy.md, quantum_mechanics.md, spectroscopic_selection_rules.md
- **Related:** `physchem_LT_ch3_particleinbox.json`
- **Problems:** `test_problems/textbook/zielinski_ch04_cyanine_dyes.json`
