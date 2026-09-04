# Crystal Field Theory (CFT) and Ligand Field Theory (LFT)

## Overview

Two complementary models for understanding transition metal complexes:

| Theory | Basis | Advantages | Disadvantages |
|--------|-------|------------|---------------|
| **Crystal Field Theory (CFT)** | Pure electrostatics | Simple, uses symmetry effectively | Does not describe bonding, based on naive assumptions |
| **Ligand Field Theory (LFT)** | Molecular orbital theory | More accurate, describes bonding | More complex |

**Source:** CHM 320 Chapter 7 (LibreTexts)

---

## Crystal Field Theory (CFT)

### Core Assumptions
- Metal-ligand interactions are purely electrostatic
- Electrons in metal d-orbitals are repelled by ligands' electrons
- Ligands treated as point charges

### d-Orbital Splitting in Octahedral Complexes

In an octahedral field, the five degenerate d-orbitals split into two sets:

| Set | Orbitals | Symmetry | Energy Change | Electrons |
|-----|----------|----------|---------------|-----------|
| **e_g** | d_x2-y2, d_z2 | Point directly at ligands | +0.6¦¤_o | 2 orbitals |
| **t_2g** | d_xy, d_xz, d_yz | Point between ligands | -0.4¦¤_o | 3 orbitals |

**Key insight:** The total energy is conserved:
- 2 orbitals ¡Á (+0.6¦¤_o) = +1.2¦¤_o
- 3 orbitals ¡Á (-0.4¦¤_o) = -1.2¦¤_o
- **Total change = 0**

### Crystal Field Splitting Energy (¦¤_o)

The energy difference between e_g and t_2g sets:

```
        ¡ü e_g (2 orbitals)
        |
   ¦¤_o  |
        |
        ¡ý t_2g (3 orbitals)
```

#### Factors Affecting ¦¤_o

1. **Charge on Metal Ion**
   - Higher charge ¡ú larger ¦¤_o
   - Example: [V(H_2O)_6]^2+ ¦¤_o = 11,800 cm^-1; [V(H_2O)_6]^3+ ¦¤_o = 17,850 cm^-1
   - Rule: +3 ions have ~50% larger ¦¤_o than +2 ions of same metal

2. **Principal Quantum Number (Period)**
   - ¦¤_o(3d) < ¦¤_o(4d) < ¦¤_o(5d)
   - Example hexaammine complexes:
     - [Co(NH_3)_6]^3+: ¦¤_o = 22,900 cm^-1
     - [Rh(NH_3)_6]^3+: ¦¤_o = 34,100 cm^-1
     - [Ir(NH_3)_6]^3+: ¦¤_o = 40,000 cm^-1
   - **Rule:** 2nd and 3rd row transition metals are almost always low-spin

3. **Nature of Ligands (Spectrochemical Series)**
   - Weak field ¡ú Strong field:
   ```
   I^- < Br^- < S^2- < SCN^- < Cl^- < NO_3^- < N_3^- < F^- < OH^- < C_2O_4^2- < H_2O < NCS^- < CH_3CN < py < NH_3 < en < bipy < phen < NO_2^- < PPh_3 < CN^- ¡Ö CO
   ```

---

## High-Spin vs Low-Spin Complexes

### When Does This Matter?
Only for d^4, d^5, d^6, d^7 configurations in octahedral complexes.

### The Trade-off
- **Pairing Energy (P):** Energy cost to pair electrons in same orbital
- **¦¤_o:** Energy cost to promote electron to e_g orbital

| Condition | Configuration | Example |
|-----------|---------------|---------|
| ¦¤_o < P | **High-spin** (max unpaired e^-) | [Fe(H_2O)_6]^2+ |
| ¦¤_o > P | **Low-spin** (min unpaired e^-) | [Fe(CN)_6]^4- |

### Electron Configurations

| d^n | High-Spin | Low-Spin | Unpaired (HS) | Unpaired (LS) |
|-----|-----------|----------|---------------|---------------|
| d^4 | t_2g^3 e_g^1 | t_2g^4 | 4 | 2 |
| d^5 | t_2g^3 e_g^2 | t_2g^5 | 5 | 1 |
| d^6 | t_2g^4 e_g^2 | t_2g^6 | 4 | 0 |
| d^7 | t_2g^5 e_g^2 | t_2g^6 e_g^1 | 3 | 1 |

---

## Ligand Field Stabilization Energy (LFSE)

### Formula
```
LFSE = [(0.6 ¡Á #e_g electrons) - (0.4 ¡Á #t_2g electrons)] ¡Á ¦¤_o
```

Or more simply:
```
LFSE = [(0.6 ¡Á upper e^-) - (0.4 ¡Á lower e^-)] ¡Á ¦¤_o
```

### Pairing Energy Correction
```
SE = LFSE + PE
```
Where PE = (number of electron pairs) ¡Á P

### Example: d^4 Complex

**High-spin:**
```
LFSE = [(0.6 ¡Á 1) - (0.4 ¡Á 3)] ¡Á ¦¤_o
     = [0.6 - 1.2] ¡Á ¦¤_o
     = -0.6 ¦¤_o
SE = -0.6 ¦¤_o + 0P = -0.6 ¦¤_o
```

**Low-spin:**
```
LFSE = [(0.6 ¡Á 0) - (0.4 ¡Á 4)] ¡Á ¦¤_o
     = -1.6 ¦¤_o
SE = -1.6 ¦¤_o + 2P
```

The low-spin case is favored when -1.6¦¤_o + 2P < -0.6¦¤_o, i.e., when ¦¤_o > P.

---

## Ligand Field Theory (LFT)

### Concept
LFT applies MO theory to coordination complexes:
- Metal d-orbitals interact with ligand SALCs (Symmetry Adapted Linear Combinations)
- Results in bonding, antibonding, and non-bonding molecular orbitals

### Octahedral Case with s-donor Ligands

| Metal Orbital | Ligand SALC | Result |
|---------------|-------------|--------|
| d_x2-y2, d_z2 | e_g SALCs | Bonding (e_g) + Antibonding (e_g^*) |
| d_xy, d_xz, d_yz | No interaction | Non-bonding (t_2g) |

### Key Difference from CFT
In LFT, the "d-orbitals" are actually antibonding molecular orbitals:
- The e_g^* orbitals are antibonding combinations
- The t_2g orbitals are essentially non-bonding (with s-donor ligands)

### ¦Ð-Effects

#### ¦Ð-Donor Ligands
- Ligands with additional lone pairs (e.g., O^2-, F^-, Cl^-)
- Donate electron density to metal t_2g orbitals
- **Raises t_2g energy** ¡ú **Smaller ¦¤_o**
- Examples: Oxide, fluoride, chloride

#### ¦Ð-Acceptor Ligands
- Ligands with empty ¦Ð* orbitals (e.g., CO, CN^-)
- Accept electron density from metal t_2g orbitals
- **Lowers t_2g energy** ¡ú **Larger ¦¤_o**
- Examples: Carbonyl (CO), cyanide (CN^-), NO_2^-

```
¦Ð-donor:     t_2g raised ¡ú smaller ¦¤_o ¡ú high-spin favored
¦Ð-acceptor:  t_2g lowered ¡ú larger ¦¤_o ¡ú low-spin favored
```

---

## Tetrahedral Complexes

### d-Orbital Splitting
- Opposite splitting pattern to octahedral
- ¦¤_t ¡Ö (4/9) ¦¤_o (much smaller)

| Set | Orbitals | Energy |
|-----|----------|--------|
| **t_2** | d_xy, d_xz, d_yz | Higher |
| **e** | d_x2-y2, d_z2 | Lower |

### Why Smaller Splitting?
- Ligands don't point directly at d-orbitals
- Weaker orbital overlap
- **Result:** Almost always high-spin

---

## Predicting Spin State

### Decision Tree
```
1. Is the metal 4d or 5d? ¡ú Low-spin (almost always)
2. Is the metal 3d?
   a. What is the oxidation state?
      - +3 or higher ¡ú Often low-spin
      - +2 or lower ¡ú Often high-spin
   b. What are the ligands?
      - Strong field (CN^-, CO, NO_2^-) ¡ú Low-spin
      - Weak field (F^-, Cl^-, Br^-, I^-) ¡ú High-spin
      - Intermediate ¡ú Check ¦¤_o vs P values
```

### Quick Rules
- **4d, 5d metals:** Always low-spin
- **3d, +3 or higher charge:** Often low-spin
- **3d, +2 charge:** Depends on ligands
- **Tetrahedral:** Always high-spin

---

## Applications

### Colors of Transition Metal Complexes
- d-d transitions absorb visible light
- Energy of transition ¡Ö ¦¤_o
- E = h¦Í = hc/¦Ë
- Wavenumber: ¦Í? = 1/¦Ë (in cm^-1) ¡Ö ¦¤_o

### Magnetic Properties
- **Paramagnetic:** Unpaired electrons ¡ú attracted to magnetic field
- **Diamagnetic:** All paired ¡ú repelled by magnetic field
- Magnetic moment related to number of unpaired electrons

### Structure Prediction
- d^8 with strong field ligands ¡ú Square planar
- d^8 with weak field ligands ¡ú Tetrahedral
- d^10 ¡ú Always tetrahedral (no LFSE)

---

## Related Topics
- [[coordination_chemistry]] - Isomers and nomenclature
- [[symmetry_group_theory]] - Character tables and SALCs
- [[molecular_orbital_theory]] - MO diagrams for complexes
- [[transition_metals]] - Electronic configurations

## References
- CHM 320: Advanced Inorganic Chemistry (LibreTexts)
- Miessler, Tarr - Inorganic Chemistry
- Shriver, Atkins, Langford - Inorganic Chemistry

## L3 Implementation
¡ú `../L3_functions/crystal_field_calculator.py`

## L4 Reference Data
¡ú `../L4_reference/spectrochemical_series.md`
¡ú `../L4_reference/lfse_values.md`

## L5 Examples
¡ú `../L5_examples/lfse_calculation_examples.md


## Implementations

- Implementation: `../L3_functions/crystal_field_theory_tools.py`

## L3 Tool Call Directives

**Source:** `crystal_field_calculator.py`

Crystal Field Theory Calculator

### Available functions:
- `calculate_lfse(d_electrons: int, geometry: str, spin_state: str, delta_o: float)` → dict — Calculate Ligand Field Stabilization Energy.
- `calculate_magnetic_moment(unpaired_electrons: int, spin_only: bool)` → dict — Calculate the magnetic moment.
- `predict_spin_state(metal: str, oxidation_state: int, ligand: str, d_electrons: int)` → dict — Predict high-spin vs low-spin based on metal and ligand.
- `wavelength_to_delta_o(wavelength_nm: float)` → float — Convert absorption wavelength to Delta_o.
- `delta_o_to_wavelength(delta_o_cm: float)` → float — Convert Delta_o to absorption wavelength.
- `d_electron_count()` → int — Calculate the number of d-electrons.

### Common errors:
- ❌ Passing wrong units (check function docstring for expected units)
- ❌ Omitting required parameters

---

**Source:** crystal_field_calculator.py
LFSE, spin state prediction, magnetic moments, wavelength conversions.

### Available functions:
- calculate_lfse(d_electrons: int, geometry='octahedral', spin_state='high', delta_o=None) �� dict �� LFSE coefficient and numerical values
- calculate_magnetic_moment(unpaired_electrons: int, spin_only=True) �� dict �� ��_eff = ��(n(n+2)) ��B, observed ranges
- predict_spin_state(metal, oxidation_state, ligand, d_electrons=None) �� dict �� high/low/N/A with reason
- wavelength_to_delta_o(wavelength_nm: float) �� float �� ��? in cm?1
- delta_o_to_wavelength(delta_o_cm: float) �� float �� �� in nm

### Common errors:
- ? predict_spin_state requires metal symbol and oxidation state, not just d-electron count
- ? Only octahedral and tetrahedral geometries supported; square_planar raises ValueError
