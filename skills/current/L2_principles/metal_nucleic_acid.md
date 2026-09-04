# Metal-Nucleic Acid Chemistry

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 8
**Level**: Graduate
**Related L1 Entry**: 132 - Metal-Nucleic Acid Chemistry

---

## Core Concepts

### Metal-DNA Interactions
1. **Electrostatic binding**
   - Mg²⁺, Zn²⁺, Na⁺ with phosphate backbone
   - Stabilizes DNA structure

2. **Groove binding**
   - Minor groove preferred for small molecules
   - Major groove for proteins

3. **Intercalation**
   - Planar metal complexes insert between base pairs
   - Increases DNA length, decreases twist

4. **Covalent binding**
   - Cisplatin crosslinking
   - Bleomycin-mediated cleavage

### Zinc Finger Proteins
- Zn²⁺ stabilizes DNA-binding domain
- Classic Cys₂His₂ motif: Zn²⁺ coordinated by 2 Cys, 2 His
- Recognizes specific DNA sequences
- K_d for Zn²⁺: ~10¹² M⁻¹ (very tight)

### DNA Cleavage by Metal Complexes
1. **Redox cleavage**: Fe-bleomycin generates ROS
2. **Hydrolytic cleavage**: Metal-activated water
3. **Photoactivated cleavage**: Ru, Rh complexes

---

## Key Formulas

### DNA Binding Constant
```
K_b = [DNA-M] / ([DNA][M])
```

### Intercalation Binding
```
r / C_f = K(r_max - r)
```
where r = bound drug/nucleotide, C_f = free drug concentration

### DNA Melting Temperature
```
ΔT_m = T_m(complex) - T_m(DNA alone)
Positive ΔT_m indicates stabilization (intercalation)
```

### Zinc Finger Stability
```
Zn²⁺ + protein ⇌ Zn-protein
K = [Zn-protein] / ([protein][Zn²⁺])
```

---

## Rules

1. Mg²⁺ essential for DNA stability (charge screening)
2. Intercalation binding constants: 10⁵-10⁷ M⁻¹
3. Zinc fingers: Zn²⁺ affinity ~10¹² M⁻¹
4. Heavy metals (Hg, Pb) displace native metals → toxicity
5. Cisplatin preferentially binds at GG sites

---

## Constraints

- DNA persistence length: ~50 nm (stiff polymer)
- Mg²⁺-phosphate binding: K ≈ 10²-10³ M⁻¹
- Intercalation increases DNA length by ~3.4 Å per intercalator
- DNA phosphate spacing: 1.7 Å (along backbone)

---

## L3 Tool Targets

### `metal_nucleic_acid_tools.py`

1. `dna_binding_constant()` - Calculate K_b from titration data
2. `melting_temp_shift()` - Calculate ΔT_m from metal binding
3. `zinc_finger_affinity()` - Calculate Zn²⁺ binding affinity
4. `cisplatin_binding_sites()` - Predict cisplatin GG/AG/GA preferences
5. `intercalation_density()` - Calculate intercalator:base pair ratio

---

## L4 Reference Data

### DNA Properties
- Persistence length: ~50 nm
- Phosphate charge: -1 per phosphate
- Base pair spacing: 3.4 Å
- Helix diameter: 20 Å

### Metal Binding Data
- Mg²⁺-phosphate K: 10²-10³ M⁻¹
- Intercalation K: 10⁵-10⁷ M⁻¹
- Zn²⁺ in zinc finger: K ≈ 10¹² M⁻¹

### Zinc Finger Data
- Cys₂His₂ motif: Zn-S ~2.3 Å, Zn-N ~2.0 Å
- Finger length: ~30 amino acids
- Recognition helix contacts DNA major groove

### Bleomycin Data
- Fe(II)-bleomycin activated by O₂
- DNA cleavage at 5'-GC-3' and 5'-GT-3' sites
- Generates free radical intermediates

---

## L5 Worked Examples

### Example 1: DNA Binding Constant
Calculate K_b from fluorescence titration data.

### Example 2: Melting Temperature Shift
Determine ΔT_m for an intercalator with binding data.

### Example 3: Zinc Finger Stability
Calculate the fraction of folded zinc finger at various [Zn²⁺].

---

## Cross-References

- → `coordination_chemistry.md` (Metal-ligand bonding)
- → `zinc_chemistry.md` (Zn²⁺ biochemistry)
- → `dna_structure.md` (DNA structure)
- → `medicinal_inorganic.md` (Cisplatin mechanism)
