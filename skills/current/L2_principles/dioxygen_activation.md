# Dioxygen Activation Enzymes

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 5
**Level**: Graduate
**Related L1 Entry**: 129 - Dioxygen Activation

---

## Core Concepts

### O₂ Reduction Pathways
1. **4-electron reduction**: O₂ + 4H⁺ + 4e⁻ → 2H₂O (E° = +0.815 V)
2. **Superoxide formation**: O₂ + e⁻ → O₂•⁻ (E° = -0.33 V)
3. **Hydrogen peroxide**: O₂•⁻ + 2H⁺ + e⁻ → H₂O₂ (E° = +0.94 V)

### Enzyme Classes
1. **Monooxygenases**
   - Incorporate 1 O atom from O₂ into substrate
   - Other O atom → H₂O
   - Example: Cytochrome P450

2. **Dioxygenases**
   - Incorporate both O atoms from O₂
   - Example: Lipoxygenase, tryptophan dioxygenase

3. **Superoxide Dismutase (SOD)**
   - 2O₂•⁻ + 2H⁺ → O₂ + H₂O₂
   - Diffusion-limited rate (~2×10⁹ M⁻¹s⁻¹)

### Cytochrome P450 Mechanism
- **Oxygen rebound mechanism**
- Fe(III) → Fe(II) → Fe(III)-O₂⁻ → Fe(III)-OOH → Fe(IV)=O (Compound I)
- Catalytic cycle involves O₂ activation and O-O bond cleavage

---

## Key Formulas

### O₂ Reduction Potentials
```
O₂ + e⁻ → O₂•⁻          E° = -0.33 V
O₂•⁻ + 2H⁺ + e⁻ → H₂O₂  E° = +0.94 V
H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O E° = +1.78 V
O₂ + 4H⁺ + 4e⁻ → 2H₂O   E° = +0.815 V
```

### SOD Reaction
```
M⁽ⁿ⁺¹⁾ + O₂•⁻ → Mⁿ⁺ + O₂
Mⁿ⁺ + O₂•⁻ + 2H⁺ → M⁽ⁿ⁺¹⁾ + H₂O₂
Net: 2O₂•⁻ + 2H⁺ → O₂ + H₂O₂
```

### Rate Constant from Diffusion Limit
```
k = 8RT/3η (Smoluchowski equation)
For SOD: k ≈ 2×10⁹ M⁻¹s⁻¹
```

### Fenton Reaction
```
Fe²⁺ + H₂O₂ → Fe³⁺ + •OH + OH⁻
```

---

## Rules

1. Monooxygenases: 1 O from O₂ → substrate, 1 O → H₂O
2. Dioxygenases: both O from O₂ → substrate
3. SOD is diffusion-limited: rate ~2×10⁹ M⁻¹s⁻¹
4. ROS (O₂•⁻, H₂O₂, •OH) damage biomolecules
5. Singlet oxygen (¹O₂) is highly reactive

---

## Constraints

- O₂ is kinetically stable (triplet ground state)
- Activation requires metal centers or radical pathways
- ROS must be controlled to prevent oxidative damage
- Antioxidant systems (SOD, catalase, peroxidases) essential

---

## L3 Tool Targets

### `dioxygen_activation_tools.py`

1. `oxygen_reduction_potential()` - Calculate E for each reduction step
2. `sod_activity_rate()` - Calculate SOD rate from concentration
3. `fenton_reaction_rate()` - Calculate •OH production rate
4. `monooxygenase_stoichiometry()` - Balance monooxygenase reactions
5. `ros_half_life()` - Calculate ROS half-lives in biological systems

---

## L4 Reference Data

### O₂ Bond Properties
- O-O bond dissociation energy: 498 kJ/mol
- O-O bond length: 1.21 Å (O₂), 1.33 Å (O₂•⁻), 1.49 Å (H₂O₂)

### SOD Data
- Cu,Zn-SOD: k ≈ 2×10⁹ M⁻¹s⁻¹
- Mn-SOD: k ≈ 1.6×10⁹ M⁻¹s⁻¹
- Fe-SOD: k ≈ 1.2×10⁹ M⁻¹s⁻¹

### Cytochrome P450 Data
- Fe(III)-O₂ reduction potential: ~0 V
- Turnover: 1-100 s⁻¹ (substrate dependent)
- Resting state: Fe(III) low-spin

### ROS Lifetimes
- •OH: < 1 μs
- O₂•⁻: ~1 μs
- H₂O₂: milliseconds to minutes
- ¹O₂: ~1-10 μs

---

## L5 Worked Examples

### Example 1: SOD Activity
Calculate the rate of O₂•⁻ dismutation with 1 μM Cu,Zn-SOD.

### Example 2: Fenton Reaction
Calculate •OH production rate from 10 μM Fe²⁺ and 100 μM H₂O₂.

### Example 3: Redox Potential Calculation
Calculate the overall potential for O₂ + 4H⁺ + 4e⁻ → 2H₂O.

---

## Cross-References

- → `redox_reactions.md` (Electron transfer fundamentals)
- → `heme_chemistry.md` (Cytochrome P450)
- → `copper_proteins.md` (Cu,Zn-SOD)
- → `oxidative_stress.md` (ROS biology)
