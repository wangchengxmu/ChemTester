# L2 Topic: NMR Spectroscopy (¹H and ¹³C)

**Source**: Organic Chemistry (OpenStax) Ch13
**Created**: 2026-03-13
**Status**: Scaffold (Pass-2)

---

## Concept Overview

Nuclear Magnetic Resonance (NMR) spectroscopy is the most powerful technique for determining molecular structure. ¹H NMR reveals the environment of hydrogen atoms; ¹³C NMR reveals the carbon framework.

### Key Features of ¹H NMR

1. **Chemical shift (δ)**: Position reveals electronic environment
2. **Integration**: Peak area reveals number of protons
3. **Spin-spin splitting**: Peak multiplicity reveals neighboring protons

---

## Core Principles

### 13.3-13.4: Chemical Shifts

**Factors affecting chemical shift**:
- **Electronegativity**: Deshielding by electronegative atoms
- **Hybridization**: sp² > sp³ (more deshielding)
- **Hydrogen bonding**: O-H, N-H are broad and variable

**Characteristic ranges**:
| Proton | δ (ppm) |
|--------|---------|
| Alkyl (R-CH₃) | 0.7-1.3 |
| Allylic/benzylic | 1.6-2.5 |
| α to O/N | 3.2-4.5 |
| Aromatic | 6.5-8.0 |
| Aldehyde | 9.5-10.5 |
| Carboxylic acid | 10-13 |

### 13.5: Integration

- Peak area ∝ number of protons
- Integration ratios give relative proton counts
- Convert to smallest whole numbers

### 13.6: Spin-Spin Splitting

**n + 1 Rule**: Proton with n equivalent neighbors → n + 1 peaks

| n | Multiplet | Intensities |
|---|-----------|-------------|
| 0 | Singlet | 1 |
| 1 | Doublet | 1:1 |
| 2 | Triplet | 1:2:1 |
| 3 | Quartet | 1:3:3:1 |

**Coupling constant (J)**:
- Distance between split peaks (Hz)
- Same J for coupled protons
- Independent of spectrometer field

### Diastereotopic Methylene Protons

- The preferred term is **diastereotopic protons** or **diastereotopic methylene hydrogens**.
- Use the substitution test: replace H_a and H_b separately by the same test group. If the two products are diastereomers, H_a and H_b are diastereotopic.
- A pre-existing stereogenic center commonly makes the two hydrogens of a nearby CH2 diastereotopic, subject to the molecule's actual symmetry and exchange on the NMR timescale.
- Analyze H_a and H_b separately. Each can couple geminally to the other (2J_HH) and vicinally to a neighboring proton (3J_HH); if those two couplings are resolved and first-order, each signal can be a doublet of doublets.
- If the chemical-shift separation is not large relative to J, describe the spin system as AB or ABX and expect second-order distortion rather than forcing an n+1 label.
- Diastereotopicity is a stereochemical relationship. Accidental overlap, conformational averaging, or insufficient resolution can still hide the chemical-shift difference.

### 13.10-13.11: ¹³C NMR

- Range: 0-220 ppm
- No splitting (usually decoupled)
- DEPT distinguishes CH, CH₂, CH₃

---

## Decision Trees

### Interpreting ¹H NMR

```
1. Count signals → Number of proton environments
2. Integration → Relative number of protons each
3. Chemical shift → Type of proton (alkyl, allylic, etc.)
4. Splitting pattern → Neighboring protons
5. J value → Identify coupled pairs
```

### Structure from NMR

```
1. Calculate degrees of unsaturation
2. Identify characteristic signals (O-H, CHO, Ar-H)
3. Identify spin systems (coupled multiplets)
4. Build molecular fragments
5. Assemble fragments consistent with formula
```

---

## Two-Dimensional (2D) NMR Techniques

2D NMR correlates two NMR parameters (usually two chemical shifts) to reveal connectivity through bonds or through space. Essential for complex molecule structure elucidation.

### COSY (Correlation Spectroscopy)
- **What it shows**: ¹H-¹H correlations via scalar (J) coupling, typically 2-3 bond (H-C-C-H)
- **Axes**: Both axes are ¹H chemical shift
- **Diagonal**: Normal 1D spectrum; **cross-peaks**: coupled protons
- **Interpretation**: Cross-peak at (δ_A, δ_B) means H_A and H_B are J-coupled (typically geminal or vicinal)
- **Use**: Identify spin systems — groups of coupled protons in a molecule

### HSQC (Heteronuclear Single Quantum Coherence)
- **What it shows**: Direct ¹H-¹³C one-bond correlations (H-C)
- **Axes**: ¹H (F2) vs ¹³C (F1)
- **Cross-peaks**: Each cross-peak = one proton bonded to one carbon
- **Does NOT show**: Quaternary carbons (no attached H) or long-range C-H
- **Use**: Assign each proton to its directly bonded carbon; map CH, CH₂, CH₃ groups

### HMBC (Heteronuclear Multiple Bond Correlation)
- **What it shows**: ¹H-¹³C long-range correlations (2-3 bonds, sometimes 4)
- **Axes**: ¹H (F2) vs ¹³C (F1)
- **Cross-peaks**: Proton correlated to carbon 2-3 bonds away
- **Key advantage**: Reveals quaternary carbons, carbonyls, connectivity between fragments
- **Use**: Connect spin systems identified by COSY; locate carbonyls and substituted positions
- **Note**: HMBC complements HSQC — HSQC = 1-bond, HMBC = 2,3-bond

### NOESY (Nuclear Overhauser Effect Spectroscopy)
- **What it shows**: Through-space ¹H-¹H correlations (≤ 5 Å distance)
- **Mechanism**: Dipole-dipole cross-relaxation (not J-coupling)
- **Axes**: Both axes are ¹H chemical shift
- **Cross-peaks**: Protons spatially close (< 5 Å), regardless of bonding
- **Use**: Stereochemistry (cis/trans, relative configuration), conformation, protein structure
- **Important**: NOE depends on r⁻⁶ — very distance-sensitive; zero for distant protons

### Comparison Table

| Technique | Correlation | Bonds | Information |
|-----------|------------|-------|-------------|
| COSY | ¹H-¹H | J-coupling (2-3 bond) | Spin systems, connectivity through bonds |
| HSQC | ¹H-¹³C | 1-bond | Direct C-H assignment |
| HMBC | ¹H-¹³C | 2-3 bond | Quaternary C, fragment connections |
| NOESY | ¹H-¹H | Through space (≤5Å) | Stereochemistry, conformation |

### Structure Elucidation Workflow with 2D NMR
1. **¹H NMR**: Identify proton environments, integration, multiplicity
2. **¹³C NMR**: Count carbons, identify carbonyls, quaternary carbons
3. **HSQC**: Assign each proton to its bonded carbon
4. **COSY**: Identify coupled proton spin systems
5. **HMBC**: Connect spin systems via quaternary carbons; locate carbonyl connections
6. **NOESY**: Determine stereochemistry and conformation

---

## Solid-State NMR (Advanced)

Solid-state NMR probes structure and dynamics of non-crystalline or rigid solids (membrane proteins, polymers, MOFs, battery materials).

### Key Difference from Solution NMR
In solids, anisotropic interactions (chemical shift anisotropy, dipolar couplings) are NOT averaged by molecular tumbling → broad powder patterns.

### Magic-Angle Spinning (MAS)
- Sample spun at 54.7° (the "magic angle") relative to B₀
- Averages second-rank tensor interactions to zero → high-resolution spectra
- MAS rates: 5–100 kHz; rotor diameters: 7 mm → 0.7 mm
- Faster MAS averages stronger interactions but requires smaller samples

### Key Solid-State NMR Parameters
- **Chemical Shift Anisotropy (CSA)**: Reflects electronic environment geometry (not just isotropic shift)
- **Dipolar couplings**: Depend on internuclear distance (r⁻³); used for distance measurements
- **Quadrupolar couplings**: For I > ½ nuclei; range 100 kHz to tens of MHz

### Important Nuclei in Solids (at 18.8 T)

| Nucleus | Spin | Abundance (%) | Freq (MHz) | Applications |
|---------|------|--------------|------------|--------------|
| ¹H | ½ | 99.98 | 800 | Organic materials, proteins |
| ¹³C | ½ | 1.1 | 200 | Organic compounds, MOFs |
| ¹⁹F | ½ | 100 | 753 | Pharmaceuticals, minerals |
| ³¹P | ½ | 100 | 324 | Phospholipids, nucleic acids |
| ²⁹Si | ½ | 4.7 | 159 | Zeolites, silica catalysts |
| ²⁷Al | 5/2 | 100 | 208 | Zeolites, minerals |
| ⁷Li | 3/2 | 92.6 | 311 | Li-ion batteries |
| ¹⁵N | ½ | 0.37 | 80 | Proteins, nucleic acids |

### Sensitivity Enhancement Methods
- **Dynamic Nuclear Polarization (DNP)**: Transfers electron spin polarization to nuclei → 10-100× sensitivity boost
- **¹H-detected fast MAS**: Detect on ¹H at >60 kHz MAS for biomolecular solids
- **Ultrahigh magnetic fields**: Up to 28 T (1200 MHz ¹H) for improved resolution and sensitivity

**Source enhancement**: Nat Rev Methods Primers (2021), PMC8341432; LibreTexts Organic Spectroscopy Ch7

---

## Connected Topics

- **Upstream**: [spectroscopy.md](spectroscopy.md) (MS and IR)
- **Downstream**: [structure_elucidation_np.md](structure_elucidation_np.md), [advanced_nmr_techniques.md](advanced_nmr_techniques.md)
- **Related**: [organic_functional_groups.md](organic_functional_groups.md)

---

## Textbook Problems

### Problem 1: COSY Spin System Identification
A compound C₈H₁₀ dissolved in CDCl₃ shows: ¹H triplet at 1.2 ppm (3H), quartet at 2.67 ppm (2H), multiplet at 7.2 ppm (5H). COSY shows cross-peaks at (1.2, 2.67) and (2.67, 1.2). ¹³C shows 6 signals (C₈H₁₀ → symmetry). HSQC: (1.2, 15), (2.67, 29), (7.2, 125-128). No HSQC cross-peak for 144 ppm carbon. HMBC: (1.2, 144), (2.67, 144). Identify the compound.
**Answer**: Ethylbenzene (para-substitution gives symmetry: 5 aromatic C signals not 8)

### Problem 2: 2D NMR Structure Verification
Menthyl anthranilate in DMSO-d₆: HMBC shows aromatic proton correlations to carbonyl at 167 ppm, and correlation between O-CH (4.8 ppm) and carbonyl. Confirm this establishes the ester linkage (O-CH → O-C=O connectivity).

---

## L3 Tools

- `../L3_functions/nmr_splitting_tools.py` - Splitting patterns, multiplet analysis
- `../L3_functions/nmr_tools.py` - Chemical shift prediction, spectrum analysis

---

## L4 References (TODO)

- [ ] Complete chemical shift tables
- [ ] Coupling constant reference values
- [ ] DEPT signal patterns

---

## L5 Worked Examples (TODO)

- [ ] Structure determination from ¹H NMR
- [ ] Predicting NMR spectra from structure
- [ ] Combined MS/IR/NMR structure problems
