# Energy Transfer & Electron Transfer

## Concept Overview

Excited-state energy and electron transfer are the primary pathways by which photoexcitation drives chemical change.

## Key Principles

### Förster Resonance Energy Transfer (FRET)
- Dipole-dipole mechanism, long-range (1–10 nm)
- Efficiency depends on spectral overlap and distance:
```
E_FRET = 1 / (1 + (r/R₀)⁶)
```
- R₀ = Förster radius (distance at 50% efficiency, typically 2–8 nm)
- Requires donor emission spectrum overlaps acceptor absorption

### Dexter Energy Transfer
- Exchange mechanism, short-range (<1 nm)
- Requires orbital overlap (wavefunction contact)
- Can transfer triplet energy (unlike FRET)

### Marcus Theory for Photoinduced Electron Transfer (PET)
```
k_ET = (2π/ℏ) |V|² (1/√(4πλk_BT)) exp(-(ΔG + λ)²/(4λk_BT))
```
- V = electronic coupling matrix element
- λ = reorganization energy (inner + outer sphere)
- ΔG = Gibbs free energy change
- **Inverted region**: rate decreases when |ΔG| >> λ

### Quenching Mechanisms
| Type | Mechanism | Stern-Volmer |
|------|-----------|-------------|
| Dynamic (collisional) | Diffusion-controlled | Linear at low [Q] |
| Static (complex formation) | Ground-state complex | Deviation at high [Q] |

### Stern-Volmer Equation
```
I₀/I = τ₀/τ = 1 + K_SV[Q] = 1 + k_q τ₀[Q]
```
- K_SV = Stern-Volmer constant
- k_q = bimolecular quenching constant (diffusion limit ~10¹⁰ M⁻¹s⁻¹)
- [Q] = quencher concentration

## Problem-Solving Routes

1. **Calculate FRET efficiency**: Use E = 1/(1 + (r/R₀)⁶)
2. **Analyze quenching data**: Plot I₀/I vs [Q]; slope = K_SV
3. **Distinguish static vs dynamic quenching**: Check lifetime quenching (τ₀/τ) vs intensity quenching

## Links

- **L3 Tools**: `../L3_functions/photochemistry_tools.py`
- **L4 Data**: `../L4_reference/photochemistry_data.csv`
- **L5 Examples**: `../L5_examples/photochemistry_examples.md`

---

## Source Attribution: Chang, Physical Chemistry for the Biosciences, Ch15 (LibreTexts)
[Source: Ch15: Photochemistry and Photobiology](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_for_the_Biosciences_(LibreTexts)/15%3A_Photochemistry_and_Photobiology)

### 15.1: Electronic Excitation and Energy Transfer
- **Photon absorption rule**: Photon energy must match an energy difference within the absorbing compound.
  - UV/vis light �� electronic transitions
  - IR light �� vibrational transitions
  - Microwave �� rotational transitions
- **Franck-Condon Principle**: Electronic transitions are vertical; nuclei don't move. Result: excited vibrational + electronic state.
- **Laporte Selection Rule (Orbital Symmetry)**: Allowed transitions require donor and acceptor orbitals of different symmetry (e.g., centrosymmetric g �� antisymmetric u).
- **Spin state conservation**: Number of unpaired electrons preserved during transitions.
  - 0 unpaired �� singlet; 1 �� doublet; 2 �� triplet; 3 �� quartet
- **Extinction coefficient ranges** indicate transition probability:
  | Transition | �� (M?1 cm?1) |
  |---|---|
  | �С���* | 3,000�C25,000 |
  | p����* | 20�C150 |
  | p����* | 100�C7,000 |
  | d��d | 5�C400 |

### 15.2: Energy Transfer in Photosynthesis
- **Antenna complexes** funnel absorbed photon energy to reaction centers via resonance energy transfer.
- **Photosystem II (P680)**: Primary electron donor at 680 nm; water oxidation; proton gradient formation.
- **Photosystem I (P700)**: 700 nm; drives NADP? reduction.
- **Chemiosmotic coupling**: Proton gradient across thylakoid membrane drives ATP synthesis.
- **Noncyclic photophosphorylation**: H?O �� NADP? (linear electron flow, produces ATP + NADPH + O?).
- **Cyclic photophosphorylation**: Only PS I involved; electrons cycle back; produces ATP only.

### 15.4: Ionizing Radiation and Biological Damage
- **Ionizing radiation** (��, ��, ��, X-ray, high-energy UV): Breaks bonds, ionizes molecules, causes DNA damage.
- **Indirect damage pathway**: H?O + radiation �� H?O? + e? �� H?O? + ?OH (hydroxyl radical damages biomolecules).
- **Radiation penetration order**: �� < �� < neutron < �� (paper stops ��; metal stops ��; lead/concrete for ��).
- **Alpha particles**: ~20�� ionizing power of �� rays but least penetrating.
- **Radon-222**: Major natural radiation hazard; ��-emitter (t? = 3.82 d); from U-238 decay series; causes ~20,000 US deaths/year.

---

## [Source: Wikipedia, Marcus Theory]
### Marcus Theory of Electron Transfer
Developed by Rudolph A. Marcus (Nobel Prize 1992). Describes rates of outer-sphere electron transfer.

**Marcus equation (normal region):**
k_ET = (2蟺/鈩?|V|虏 脳 (1/鈭?4蟺位k_BT)) 脳 exp[-(螖G掳+位)虏/(4位k_BT)]

Where:
- V = electronic coupling matrix element (donor-acceptor overlap)
- 位 = reorganization energy (sum of inner-sphere + outer-sphere)
- 螖G掳 = standard free energy change of the reaction
- k_B = Boltzmann constant, T = temperature

**Marcus regions:**
1. **Normal region** (螖G掳 < -位): Rate increases as 螖G掳 becomes more negative.
2. **Activationless** (螖G掳 = -位): Maximum rate.
3. **Inverted region** (螖G掳 < -位, highly exergonic): Rate decreases! Counterintuitive but experimentally confirmed.

**Reorganization energy components:**
- Inner-sphere (位_i): Bond length changes in reactant/product.
- Outer-sphere (位_o): Solvent reorganization around the redox centers.

### [Source: Wikipedia, Photoredox Catalysis]
### Key Photoredox Catalysts

| Catalyst | Excited State E掳(Ru鲁鈦?Ru虏鈦?) | E掳(Ru虏鈦?/Ru鈦? | 位_max (nm) |
|---|---|---|---|
| Ru(bpy)鈧僀l鈧?| +0.77 V vs SCE | -0.81 V | 452 |
| Ir(ppy)鈧?| +0.31 V | -1.73 V | 375 |
| Eosin Y (organic) | +0.83 V | -1.11 V | 517 |
| 4CzIPN (organophotocatalyst) | +1.35 V | -1.21 V | ~420 |

- Ru(bpy)鈧兟测伜: Most widely used; can both oxidize and reduce substrates via SET.
- Ir(ppy)鈧? Stronger reducing power in excited state.
- Eosin Y: Cheap, visible-light organic dye alternative.
