# Basis Sets Reference Table - L4 Database

**Source:** LibreTexts Physical Chemistry Ch11
**Last Updated:** 2026-03-14

---

## 1. Minimal Basis Sets

### STO-nG Series

| Basis Set | Gaussians/STO | Description | Typical Use |
|-----------|---------------|-------------|-------------|
| STO-3G | 3 | Smallest, fastest | Initial geometry guess |
| STO-4G | 4 | Slightly better | Quick estimates |
| STO-6G | 6 | Best minimal | When speed critical |

**STO-3G Exponents (1s orbital):**

| Element | α₁ | α₂ | α₃ |
|---------|-----|-----|-----|
| H | 0.1689 | 0.6239 | 3.425 |
| He | 0.297 | 1.079 | 5.757 |
| Li | 0.0336 | 0.1179 | 0.534 |
| C | 0.1689 | 0.6239 | 3.425 |
| N | 0.202 | 0.732 | 3.985 |
| O | 0.242 | 0.862 | 4.441 |
| F | 0.283 | 0.999 | 5.097 |

**Functions per atom (first row):**
- H, He: 1 (1s)
- Li-Ne: 5 (2 s-type + 3 p-type)

---

## 2. Split-Valence Basis Sets

### Double-Zeta Basis Sets

| Basis | Core | Valence | Functions (H) | Functions (C,N,O) | Notes |
|-------|------|---------|---------------|-------------------|-------|
| 3-21G | 3 | 2+1 | 2 | 9 | Basic split-valence |
| 4-31G | 4 | 3+1 | 2 | 9 | Better core |
| 6-31G | 6 | 3+1 | 2 | 9 | Standard double-zeta |

**Valence orbital composition (6-31G):**

For carbon 2s:
```
φ₂s = 0.17·GTO(α=0.169) + 0.91·GTO(α=0.558) + ... [inner]
    + GTO(α=0.187) [outer]
```

### Triple-Zeta Basis Sets

| Basis | Core | Valence | Functions (H) | Functions (C,N,O) |
|-------|------|---------|---------------|-------------------|
| 6-311G | 6 | 3+1+1 | 3 | 13 |
| cc-pVTZ | - | TZ + 2d1f | 5 | 30+ |

### Quadruple-Zeta and Higher

| Basis | Valence | Functions (C,N,O) | Notes |
|-------|---------|-------------------|-------|
| 6-3111G | 3+1+1+1 | 17 | QZ valence |
| cc-pVQZ | QZ + 3d2f1g | 55+ | High accuracy |
| cc-pV5Z | 5Z + 4d3f2g1h | 100+ | Benchmark quality |

---

## 3. Polarization Functions

### Polarized Basis Sets

| Basis | Heavy Atoms | H/He | Functions (C) | Functions (H) |
|-------|-------------|------|---------------|---------------|
| 6-31G* | +d | - | 15 (9+6d) | 2 |
| 6-31G** | +d | +p | 15 | 5 (2+3p) |
| 6-311G* | +d | - | 18 (13+5d) | 3 |
| 6-311G** | +d | +p | 18 | 6 (3+3p) |
| 6-31G(2df) | +2d1f | - | 25 | 2 |

### Polarization Function Types

| Type | l-value | Orbitals Added | Purpose |
|------|---------|----------------|---------|
| p | l=1 | pₓ, pᵧ, p₂ | Polarize s orbitals |
| d | l=2 | dₓ²-ᵧ², d₂², dₓᵧ, dₓ₂, dᵧ₂ | Polarize p orbitals |
| f | l=3 | 7 f orbitals | Polarize d orbitals |
| g | l=4 | 9 g orbitals | High accuracy |

**Standard notation:**
- * = add d functions to heavy atoms
- ** = add d to heavy atoms AND p to H/He
- (d,p) = same as **
- (2df,2pd) = two d and one f on heavy, two p and one d on H

---

## 4. Diffuse Functions

### Diffuse Basis Sets

| Basis | Heavy Atoms | H/He | Functions (C) | Functions (H) |
|-------|-------------|------|---------------|---------------|
| 6-31+G | +diffuse s,p | - | 14 (9+1s+3p) | 2 |
| 6-31++G | +diffuse s,p | +diffuse s | 14 | 3 |
| 6-31+G* | +diffuse + d | - | 19 | 2 |
| 6-31++G** | +diffuse + d | +diffuse s + p | 19 | 6 |
| aug-cc-pVDZ | DZ + diffuse | + diffuse | 22 | 9 |

### When to Use Diffuse Functions

| System Type | Recommended | Reason |
|-------------|-------------|--------|
| Anions | aug- or ++ | Electron density tail |
| Rydberg states | aug- | Extended orbitals |
| Hydrogen bonds | ++ | H bonding tail |
| Electron affinities | aug- | LUMO description |
| Polarizabilities | aug- | Response to field |
| Neutral molecules | Optional | Not usually needed |

---

## 5. Correlation-Consistent Basis Sets (Dunning)

### cc-pVnZ Series

| Basis | Valence | Polarization | Diffuse | Functions (C) |
|-------|---------|--------------|---------|---------------|
| cc-pVDZ | DZ | 1d (heavy), 1p (H) | No | 14 |
| cc-pVTZ | TZ | 2d1f (heavy), 2p1d (H) | No | 30 |
| cc-pVQZ | QZ | 3d2f1g (heavy), 3p2d1f (H) | No | 55 |
| cc-pV5Z | 5Z | 4d3f2g1h (heavy), 4p3d2f1g (H) | No | 91 |

### Augmented cc-pVnZ Series

| Basis | Augmented | Functions (C) | Use |
|-------|-----------|---------------|-----|
| aug-cc-pVDZ | + diffuse s,p,d on all | 22 | Anions, EA |
| aug-cc-pVTZ | + diffuse on all | 43 | High accuracy |
| aug-cc-pVQZ | + diffuse on all | 73 | Benchmark |

### CBS (Complete Basis Set) Extrapolation

Two-point extrapolation formula:
```
E(n) = E_CBS + A/n³

E_CBS = (n³·E(n) - (n-1)³·E(n-1)) / (n³ - (n-1)³)

Use cc-pVTZ and cc-pVQZ for extrapolation
```

---

## 6. Pseudopotential Basis Sets

### Effective Core Potentials (ECPs)

| Basis | Element Range | Core Electrons | Valence | Use |
|-------|---------------|----------------|---------|-----|
| LANL2DZ | Na-Bi | Varies | DZ | Transition metals |
| SDD | All | Varies | DZ | Heavy elements |
| Stuttgart | All | Varies | Various | Relativistic |
| Def2-SVP | All | Varies | Split-valence | General |

**When to use ECPs:**
- Transition metals (many core electrons)
- Heavy elements (>Kr, relativistic effects)
- Computational efficiency
- Relativistic corrections needed

---

## 7. Special Purpose Basis Sets

### For Specific Properties

| Property | Recommended Basis | Notes |
|----------|-------------------|-------|
| Geometry optimization | 6-31G* | Standard choice |
| Frequencies | 6-31G* | Same as geometry |
| Dipole moments | aug-cc-pVTZ | Diffuse important |
| Polarizabilities | aug-cc-pVTZ | Diffuse critical |
| NMR shifts | 6-311+G** | Magnetic properties |
| Electron affinities | aug-cc-pVTZ | Diffuse essential |
| Bond dissociation | cc-pVTZ or better | Correlation important |

### For Specific Systems

| System | Recommended Basis | Reason |
|--------|-------------------|--------|
| Water clusters | aug-cc-pVTZ | H-bonding |
| Anions | aug-cc-pVDZ or better | Electron tail |
| Transition metals | Def2-TZVP or LANL2DZ | d-electrons |
| Aromatic systems | 6-311G** | π-systems |
| Van der Waals | aug-cc-pVTZ | Long-range |

---

## 8. Basis Set Selection Guide

### By Accuracy Level

| Level | Basis Set | Cost | Use Case |
|-------|-----------|------|----------|
| Minimal | STO-3G | Very low | Initial guess, large systems |
| Basic | 3-21G | Low | Quick survey |
| Standard | 6-31G* | Medium | Routine calculations |
| Good | 6-311G** | Medium-high | Accurate geometries |
| High | cc-pVTZ | High | Accurate energies |
| Benchmark | aug-cc-pVQZ | Very high | Reference calculations |

### By System Size

| Atoms | Recommended Basis | Reason |
|-------|-------------------|--------|
| 1-5 | cc-pVTZ or better | Small systems, high accuracy possible |
| 5-20 | 6-311G** | Balanced accuracy/cost |
| 20-50 | 6-31G* | Moderate systems |
| 50-100 | 6-31G | Large systems |
| >100 | STO-3G or semi-empirical | Very large systems |

### By Property

| Property | Minimal Acceptable | Recommended |
|----------|-------------------|-------------|
| Energy (relative) | 6-31G | 6-311G** |
| Geometry | 6-31G | 6-31G* |
| Frequencies | 6-31G | 6-31G* |
| Dipole moment | 6-31+G* | aug-cc-pVTZ |
| Ionization potential | 6-31+G* | aug-cc-pVTZ |
| Electron affinity | 6-31++G* | aug-cc-pVTZ |
| Bond energy | cc-pVDZ | cc-pVTZ |
| Reaction barrier | 6-31G* | cc-pVTZ |

---

## 9. Basis Set Superposition Error (BSSE)

### Counterpoise Correction

For dimer AB:
```
E_AB^CP = E_AB(AB) - E_A(AB) - E_B(AB)

where:
E_AB(AB) = energy of AB with AB basis
E_A(AB) = energy of A with AB basis (ghost B)
E_B(AB) = energy of B with AB basis (ghost A)
```

**BSSE magnitude:**
- Small basis (STO-3G): ~10 kcal/mol
- Medium basis (6-31G*): ~2-5 kcal/mol
- Large basis (cc-pVTZ): ~0.5 kcal/mol
- Very large (cc-pVQZ): <0.1 kcal/mol

---

## 10. Practical Guidelines

### Basis Set Convergence

Monitor convergence of property of interest:
```
6-31G → 6-31G* → 6-311G** → cc-pVTZ → aug-cc-pVTZ

Stop when: |Property(n) - Property(n-1)| < threshold
```

### Common Mistakes to Avoid

1. **Using minimal basis for energetics**
   - Use at least double-zeta (6-31G) for relative energies

2. **Forgetting polarization for geometry**
   - Polarization (*) needed for accurate bond lengths/angles

3. **Missing diffuse functions for anions**
   - Use aug- or ++ basis sets

4. **Using too small basis for correlation methods**
   - MP2, CCSD need at least 6-31G*, preferably cc-pVTZ

5. **Ignoring BSSE for weak interactions**
   - Use counterpoise correction or large basis

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│     BASIS SET QUICK REFERENCE           │
├─────────────────────────────────────────┤
│ Minimal:     STO-3G (fast, crude)       │
│ Basic:       3-21G (quick survey)       │
│ Standard:    6-31G* (routine)           │
│ Good:        6-311G** (accurate)        │
│ High:        cc-pVTZ (research)         │
│ Benchmark:   aug-cc-pVQZ (best)         │
├─────────────────────────────────────────┤
│ + = diffuse on heavy atoms              │
│ ++ = diffuse on all atoms               │
│ * = d polarization on heavy atoms       │
│ ** = d on heavy, p on H                 │
├─────────────────────────────────────────┤
│ Anions: need diffuse (aug or ++)        │
│ Geometries: need polarization (*)       │
│ Energies: need larger basis             │
│ Transition metals: use ECP (LANL2DZ)    │
└─────────────────────────────────────────┘
```

---

*Last updated: 2026-03-14*
*Source: LibreTexts Physical Chemistry, Chapter 11*
