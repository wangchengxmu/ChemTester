---
id: organic.spectroscopy_rules
layer: 2
title: Spectroscopy Interpretation Rules
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - ../L4_reference/spectroscopy_tables.md
---

# Spectroscopy Interpretation Rules

> How to interpret NMR, IR, MS, UV-Vis spectra.
> Raw shift/frequency tables are in `L4_reference/spectroscopy_tables.md`.

---

## 1H NMR — Core Principles

### Reading a Spectrum
1. **Count signals** → number of chemically distinct proton environments
2. **Integration** → relative proton count per signal
3. **Chemical shift** → what's near the proton (electron-withdrawing groups deshield, shift downfield)
4. **Splitting (multiplicity)** → number of neighboring protons (n+1 rule)
5. **Coupling constants (J)** → bond types, stereochemistry, conformation

### Key Shift Trends
- **Electron-withdrawing groups** (C=O, NO2, CN, halogens) deshield → higher δ
- **Electron-donating groups** (alkyl, O-alkyl, NR2) shield → lower δ
- **Conjugation** with C=O shifts vinyl protons downfield (5→6 ppm)
- **Anisotropy** of aromatic rings and C=O causes specific shielding/deshielding zones

### Coupling Interpretation
- **Large J (15-18 Hz)** → trans alkene, or anti dihedral in rigid systems
- **Medium J (6-12 Hz)** → cis alkene, ortho aromatic, free-rotation vicinal
- **Small J (0-3 Hz)** → vinylic geminal, allylic, W-coupling, meta aromatic
- **Aliphatic sp3 geminal 2J_HH** → commonly about 10-18 Hz in magnitude and often negative by sign convention; do not identify coupling topology from magnitude alone
- **No coupling**: rapid exchange (OH, NH, COOH), equivalent protons, long distance

### When n+1 Fails
- **Diastereotopic CH2**: apply the replacement test. If replacing H_a versus H_b gives diastereomers, the hydrogens are diastereotopic and chemically non-equivalent.
- A CH2 next to an existing stereogenic center is a common case, but confirm the complete molecular symmetry and exchange behavior rather than using proximity alone.
- Treat H_a and H_b as separate spins. Each may show a geminal coupling to the other and different vicinal couplings; one resolved geminal plus one resolved vicinal coupling gives a doublet of doublets for that proton.
- Use AB or ABX analysis when chemical shifts are close. Diastereotopicity does not guarantee two visibly resolved signals or a simple first-order pattern.
- **AA'BB' systems**: para-disubstituted benzene with different substituents → 2 apparent doublets
- **Second-order effects**: when δ/J < ~10, patterns distort from first-order

### D2O Exchange
Add D2O: OH, NH, COOH, SH signals disappear or shift. Use to identify exchangeable protons.

### Common Exam Patterns
| Pattern | Interpretation |
|---|---|
| Singlet 9-10 ppm (1H) | Aldehyde |
| Broad 10-13 ppm (1H) | Carboxylic acid |
| Two doublets ~7 ppm (each 2H) | Para-disubstituted benzene |
| 5H multiplet ~7.2 ppm | Monosubstituted benzene |
| Two doublets J≈16 Hz (1H each) | trans alkene |
| Two doublets J≈10 Hz (1H each) | cis alkene |
| Singlet 2H at ~4.8-5.2 ppm | Terminal vinyl =CH2 |
| 6H singlet ~0.9 ppm | Two equivalent CH3 |
| 4H quartet + 6H triplet | Ethyl group |
| 9H singlet ~1.0-1.5 ppm | tert-butyl |

---

## 13C NMR — Core Principles

- **Number of signals** = number of unique carbon environments (symmetry reduces this)
- **DEPT-135**: CH3/CH positive, CH2 negative, Cq invisible
- **Quaternary carbons** only visible in broadband-decoupled (normal) spectrum, not DEPT
- **Symmetry check**: if formula says 8 carbons but only 4 signals → molecule has a symmetry plane/axis
- **Carbonyl region** (160-220 ppm) is diagnostic for functional group type

---

## IR — Core Principles

### Diagnostic Strategy
1. **Check 3700-2700 cm⁻¹** → OH, NH, CH stretches
2. **Check 2250-2100 cm⁻¹** → triple bonds (C≡C, C≡N)
3. **Check 1850-1650 cm⁻¹** → carbonyl (if present, note exact position)
4. **Check 1650-1600 cm⁻¹** → C=C stretch (weak unless conjugated)
5. **Check 1600, 1500 cm⁻¹** → aromatic ring modes
6. **Check 1300-1000 cm⁻¹** → C-O stretches
7. **Check below 1000 cm⁻¹** → fingerprint, aromatic substitution pattern

### Key Rules
- **Conjugation** lowers C=O frequency by ~20-30 cm⁻¹
- **Ring strain** increases C=O frequency: 4-ring > 5-ring > 6-ring
- **H-bonding** broadens and lowers OH/NH stretch
- **Two C=O bands** → anhydride or possibly two different carbonyl groups

---

## MS — Core Principles

### Nitrogen Rule
- Odd molecular weight → odd number of N atoms
- Even molecular weight → zero or even number of N atoms

### Degree of Unsaturation (DBE)
```
DBE = C - H/2 + N/2 + 1
(Halogens count as H; O and S ignored)
```
- DBE ≥ 4 with aromatic signals → likely contains benzene ring

### Key Fragmentation Patterns
- **Alpha cleavage**: break next to heteroatom (O, N, S)
- **McLafferty rearrangement**: requires γ-H relative to carbonyl → characteristic for aldehydes, ketones, esters
- **Benzyl cleavage**: strong m/z 91 tropylium ion from benzyl compounds
- **Allylic cleavage**: favored at allylic positions
- **Retro-Diels-Alder**: cyclohexenes fragment back to diene + dienophile

### Isotope Patterns
- **M and M+2 roughly equal** → one Br atom
- **M+2 ≈ 1/3 of M** → one Cl atom
- Use to count halogen atoms

---

## Structure Elucidation Workflow

1. **Molecular formula** → calculate DBE
2. **IR** → identify functional groups (C=O, OH, NH, C≡C, C≡N, aromatic)
3. **MS** → confirm MW, isotope pattern, key fragments
4. **¹H NMR integration** → total H distribution
5. **¹H NMR shifts** → assign proton environments
6. **¹H NMR splitting + J values** → establish connectivity
7. **¹³C NMR** → carbon skeleton, symmetry, quaternary vs CH
8. **DEPT** → distinguish CH3/CH/CH2/Cq
9. **Assemble** → combine all info, verify DBE

### Common Pitfalls
- Forgetting that D2O exchangeable protons exist (may not integrate correctly)
- Assuming para-disubstituted benzene with identical groups gives 2 signals (it gives 1)
- Misassigning geminal vs vicinal coupling in alkenes (check J value)
- Overlooking symmetry in ¹³C (fewer signals ≠ fewer carbons)
- Confusing alpha cleavage (next to heteroatom) with McLafferty (γ-H transfer)
