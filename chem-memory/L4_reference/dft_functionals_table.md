# DFT Functionals Reference Table - L4 Database

**Source:** LibreTexts Physical Chemistry Ch11 + Computational Chemistry Standards
**Last Updated:** 2026-03-14

---

## 1. Functional Classification

### Jacob's Ladder of DFT Functionals

```
                     Chemical Accuracy
                           ↑
                     ┌─────┴─────┐
     Level 5:       │  Double   │  B2PLYP, DSD-PBEP86
                     │  Hybrid   │
                     └─────┬─────┘
                     ┌─────┴─────┐
     Level 4:       │ Meta-GGA  │  TPSS, M06, SCAN
                     │  Hybrid   │
                     └─────┬─────┘
                     ┌─────┴─────┐
     Level 3:       │   Hybrid  │  B3LYP, PBE0, M06-2X
                     │  GGA      │
                     └─────┬─────┘
                     ┌─────┴─────┐
     Level 2:       │    GGA    │  BLYP, PBE, BP86
                     │           │
                     └─────┬─────┘
                     ┌─────┴─────┐
     Level 1:       │    LDA    │  SVWN, SPW92
                     │           │
                     └─────┬─────┘
                           ↓
                    Hartree-Fock
```

---

## 2. LDA Functionals (Local Density Approximation)

### LDA Exchange

| Functional | Formula | Notes |
|------------|---------|-------|
| Slater (S) | E_x = -C_x ∫ρ^(4/3) dr | Dirac exchange |
| C_x = (3/4)(3/π)^(1/3) | | |

### LDA Correlation

| Functional | Description | Notes |
|------------|-------------|-------|
| VWN | Vosko-Wilk-Nusair | Parametrizes uniform electron gas |
| VWN5 | VWN variant 5 | Most common |
| PW92 | Perdew-Wang 1992 | Smooth parametrization |

### Complete LDA Functionals

| Name | Exchange | Correlation | Use |
|------|----------|-------------|-----|
| SVWN | Slater | VWN | Basic LDA |
| SPW92 | Slater | PW92 | Modern LDA |
| SPL | Slater | Perdew-Lee-Zhang | Solid state |

**LDA Performance:**
- ✅ Overbinds molecules (bond lengths too short)
- ✅ Good for solids, metals
- ❌ Poor for molecules (errors ~10-20 kcal/mol)
- ❌ Underestimates reaction barriers

---

## 3. GGA Functionals (Generalized Gradient Approximation)

### GGA Exchange

| Functional | Dependencies | Notes |
|------------|--------------|-------|
| B88 (Becke88) | ρ, ∇ρ | Gradient correction to Slater |
| PBE | ρ, ∇ρ | Non-empirical, satisfies constraints |
| PW91 | ρ, ∇ρ | Perdew-Wang 1991 |
| mPW | ρ, ∇ρ | Modified PW91 |

### GGA Correlation

| Functional | Description | Notes |
|------------|-------------|-------|
| LYP | Lee-Yang-Parr | 4 parameters, from He atom |
| PBE | Non-empirical | Satisfies exact conditions |
| PW91 | Perdew-Wang | Smooth form |
| P86 | Perdew 1986 | Older functional |

### Popular GGA Combinations

| Name | Exchange | Correlation | HF % | MAE (kcal/mol) | Use |
|------|----------|-------------|------|----------------|-----|
| BLYP | B88 | LYP | 0% | ~3-5 | General purpose |
| BP86 | B88 | P86 | 0% | ~5-7 | Quick calculations |
| PBE | PBE | PBE | 0% | ~4-6 | Non-empirical |
| PW91 | PW91 | PW91 | 0% | ~4-6 | Solid state |
| mPWPW | mPW | PW91 | 0% | ~3-5 | Improved over PW91 |

**GGA Performance:**
- ✅ Much better than LDA for molecules
- ✅ Good geometries, frequencies
- ✅ Reasonable energetics
- ❌ Still misses exact exchange
- ❌ Self-interaction error

---

## 4. Meta-GGA Functionals

### Meta-GGA Features

Include kinetic energy density τ = ½Σ|∇φᵢ|²

| Functional | Dependencies | Parameters | Notes |
|------------|--------------|------------|-------|
| TPSS | ρ, ∇ρ, τ | 0 | Non-empirical meta-GGA |
| revTPSS | ρ, ∇ρ, τ | 0 | Revised TPSS |
| M06-L | ρ, ∇ρ, τ | 44 | Minnesota local functional |
| SCAN | ρ, ∇ρ, τ | 0 | Strongly constrained, appropriately normed |

### Meta-GGA Performance

| Functional | MAE (kcal/mol) | Pros | Cons |
|------------|----------------|------|------|
| TPSS | ~2-3 | Non-empirical | Harder to converge |
| M06-L | ~2-3 | Good for transition metals | Many parameters |
| SCAN | ~2 | Satisfies 17 constraints | Numerical issues |

---

## 5. Hybrid GGA Functionals

### B3LYP (Most Popular)

**Formula:**
```
E_xc^B3LYP = (1-a)E_x^Slater + aE_x^HF + bΔE_x^B88 + cE_c^LYP + (1-c)E_c^VWN

Parameters: a = 0.20, b = 0.72, c = 0.81
```

**Performance:**
- MAE: ~1-2 kcal/mol for thermochemistry
- Good for: Organic molecules, geometries, frequencies
- Limitations: Long-range, dispersion, transition metals

### Common Hybrid Functionals

| Functional | Exchange | Correlation | HF % | MAE | Use |
|------------|----------|-------------|------|-----|-----|
| B3LYP | B88 + HF | LYP | 20% | ~2 | General organic |
| PBE0 | PBE + HF | PBE | 25% | ~2 | Thermochemistry |
| B3PW91 | B88 + HF | PW91 | 20% | ~2 | Similar to B3LYP |
| B97-D | B97 | D | 21% | ~2 | With dispersion |
| APFD | APF | D | 22% | ~1.5 | Thermochemistry |

### Hybrid Meta-GGA

| Functional | Type | HF % | MAE | Notes |
|------------|------|------|-----|-------|
| M06-2X | Meta-GGA | 54% | ~1 | High HF for main group |
| M06 | Meta-GGA | 27% | ~2 | Transition metals |
| TPSSh | Meta-GGA | 10% | ~2 | Low HF, good for TM |
| wB97X-D | Range-separated | Var. | ~1 | Long-range corrected |

---

## 6. Range-Separated Hybrids

### Concept

Split Coulomb operator:
```
1/r = [α + β·erf(μr)]/r + [1 - α - β·erf(μr)]/r
      └─────────────────┘   └─────────────────────┘
         short-range             long-range
```

### Range-Separated Functionals

| Functional | SR HF | LR HF | μ (bohr⁻¹) | Use |
|------------|-------|-------|------------|-----|
| CAM-B3LYP | 19% | 65% | 0.33 | Charge transfer |
| ωB97X-D | 15.8% | 100% | 0.20 | Dispersion, excited states |
| LC-ωPBE | 0% | 100% | 0.40 | Long-range only |
| HSE06 | 25% | 0% | 0.11 | Solid state |

**When to use:**
- Charge transfer excitations
- Long-range interactions
- Polarizabilities
- Extended systems

---

## 7. Double Hybrid Functionals

### Concept

Add MP2-like correlation:
```
E_xc = (1-a_x)E_x^DFT + a_x E_x^HF + (1-a_c)E_c^DFT + a_c E_c^MP2
```

### Double Hybrid Functionals

| Functional | HF % | MP2 % | MAE | Cost | Notes |
|------------|------|-------|-----|------|-------|
| B2PLYP | 53% | 27% | ~1 | O(N⁵) | First double hybrid |
| DSD-PBEP86 | 71% | 54% | ~0.5 | O(N⁵) | Spin-component scaled |
| DSD-PBEB95 | 75% | 54% | ~0.5 | O(N⁵) | Best accuracy |
| PBE0-DH | 50% | 27% | ~0.7 | O(N⁵) | Non-empirical |

**Performance:**
- Near CCSD(T) accuracy for thermochemistry
- 10-50x more expensive than hybrid DFT
- Best for: High-accuracy thermochemistry

---

## 8. Dispersion-Corrected Functionals

### DFT-D Methods

Add empirical dispersion:
```
E_disp = -s₆ Σ_{i<j} C₆^{ij}/R_{ij}⁶ · f_damp(R_{ij})
```

| Method | Parameters | Notes |
|--------|------------|-------|
| DFT-D2 | C₆, R₀ | Grimme's D2 |
| DFT-D3 | C₆, C₈, C₁₀ | Grimme's D3, more accurate |
| DFT-D3(BJ) | + Becke-Johnson damping | Most common |
| DFT-D4 | Charge-dependent C₆ | Latest Grimme |

### Dispersion-Corrected Functionals

| Functional | Dispersion | MAE (non-covalent) |
|------------|------------|-------------------|
| B3LYP-D3(BJ) | D3(BJ) | ~0.3 kcal/mol |
| B97-D3 | D3 | ~0.3 kcal/mol |
| ωB97X-D | Built-in + D2 | ~0.2 kcal/mol |
| PBE0-D3 | D3 | ~0.3 kcal/mol |

### Non-local vdW Functionals

| Functional | Approach | Notes |
|------------|----------|-------|
| vdW-DF | Non-local correlation | Dion et al. |
| vdW-DF2 | Revised vdW-DF | Better parameters |
| rVV10 | Revised VV10 | Efficient implementation |
| DFT-TS | Tkatchenko-Scheffler | Atom-in-molecule C₆ |

---

## 9. Minnesota Functionals

### Mxx Family

| Functional | Type | HF % | Parameters | Use |
|------------|------|------|------------|-----|
| M06-L | Meta-GGA | 0% | 44 | Transition metals |
| M06 | Meta-GGA hybrid | 27% | 36 | General purpose |
| M06-2X | Meta-GGA hybrid | 54% | 29 | Main group thermochemistry |
| M11 | Range-separated | 42.8% | 40 | Excited states |
| MN15 | Meta-GGA hybrid | 44% | 58 | Broad accuracy |
| MN15-L | Meta-GGA | 0% | 57 | Local functional |

**Performance:**
- Good for diverse chemistry
- Many parameters (concern about overfitting)
- M06-2X: Good for main group thermochemistry
- M06: Good for transition metals

---

## 10. Functional Selection Guide

### By Application

| Application | Recommended | Alternative |
|-------------|-------------|-------------|
| **General organic** | B3LYP/6-31G* | PBE0/def2-SVP |
| **Thermochemistry** | M06-2X/aug-cc-pVTZ | CCSD(T) |
| **Geometries** | B3LYP/6-31G* | PBE0/def2-TZVP |
| **Frequencies** | B3LYP/6-31G* | ωB97X-D/def2-TZVP |
| **Transition metals** | TPSSh/def2-TZVP | M06/def2-TZVP |
| **Non-covalent** | ωB97X-D/aug-cc-pVTZ | B3LYP-D3(BJ) |
| **Excited states** | CAM-B3LYP/aug-cc-pVTZ | ωB97X-D |
| **Charge transfer** | CAM-B3LYP | ωB97X-D |
| **Solids/metals** | PBE | PBE0 |
| **High accuracy** | DSD-PBEP86 | CCSD(T) |

### By System Size

| System Size | Functional | Basis | Time Factor |
|-------------|------------|-------|-------------|
| Small (<10 atoms) | DSD-PBEP86 | aug-cc-pVTZ | 100× |
| Medium (10-30) | M06-2X | def2-TZVP | 10× |
| Large (30-100) | B3LYP | 6-31G* | 1× |
| Very large (>100) | BLYP | 6-31G | 0.3× |
| Huge (>500) | PBE | minimal | 0.1× |

### By Property

| Property | Best Functional | Why |
|----------|-----------------|-----|
| Bond energies | M06-2X, DSD-PBEP86 | Correlation accuracy |
| Reaction barriers | M06-2X, MPWB1K | Barrier heights |
| Dipole moments | PBE0 | Balanced |
| Polarizabilities | CAM-B3LYP | Long-range |
| Ionization potentials | M06-2X | IP correct |
| Electron affinities | ωB97X-D | Diffuse needed |
| NMR shifts | PBE0 | Magnetic properties |
| UV-Vis spectra | CAM-B3LYP | Excited states |
| Spin states | TPSSh | Transition metals |

---

## 11. Known Issues and Limitations

### B3LYP Issues

1. **Self-interaction error:** Underestimates reaction barriers
2. **Long-range:** Poor for charge transfer
3. **Dispersion:** Missing without D3 correction
4. **Transition metals:** Can be unreliable

### Common Problems

| Problem | Solution |
|---------|----------|
| Delocalization error | Use higher HF % (M06-2X) |
| Missing dispersion | Add D3(BJ) correction |
| Spin contamination | Use restricted methods |
| Long-range failure | Use range-separated |
| Transition metals | Use TPSSh or M06 |

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│     DFT FUNCTIONAL QUICK REFERENCE      │
├─────────────────────────────────────────┤
│ LDA:        SVWN (solids, metals)       │
│ GGA:        BLYP, PBE (fast, decent)    │
│ Meta-GGA:   TPSS (improved accuracy)    │
│ Hybrid:     B3LYP (standard organic)    │
│ Meta-Hybrid: M06-2X (thermochemistry)   │
│ Range-sep:  ωB97X-D (excited, CT)       │
│ Double:     B2PLYP (high accuracy)      │
├─────────────────────────────────────────┤
│ Add -D3(BJ) for dispersion              │
│ Use aug- basis for excited states       │
│ Use 6-31G* minimum for geometry         │
│ Transition metals: TPSSh or M06         │
└─────────────────────────────────────────┘
```

---

## 12. Computational Cost Comparison

### Relative Timings (normalized to HF)

| Method | Small System | Large System | Scaling |
|--------|--------------|--------------|---------|
| HF | 1 | 1 | O(N⁴) |
| LDA | 1.1 | 1.1 | O(N³) |
| GGA | 1.5 | 1.5 | O(N³) |
| Hybrid GGA | 2-5 | 5-10 | O(N⁴) |
| Meta-GGA | 2 | 2 | O(N³) |
| Hybrid Meta-GGA | 3-6 | 6-12 | O(N⁴) |
| MP2 | 5-10 | 20-50 | O(N⁵) |
| Double Hybrid | 10-20 | 50-100 | O(N⁵) |

---

*Last updated: 2026-03-14*
*Source: Computational Chemistry Standards + LibreTexts*
