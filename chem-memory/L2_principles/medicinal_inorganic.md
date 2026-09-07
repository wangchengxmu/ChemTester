# Medicinal Inorganic Chemistry

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 9
**Level**: Graduate
**Related L1 Entry**: 133 - Medicinal Inorganic Chemistry

---

## Core Concepts

### Platinum Anticancer Drugs
1. **Cisplatin**: cis-PtCl₂(NH₃)₂
   - Activated by aquation in cells
   - Forms DNA crosslinks (GG > AG > GA)
   - Triggers apoptosis

2. **Carboplatin**: Pt(CBDCA)(NH₃)₂
   - Less toxic than cisplatin
   - Same mechanism (DNA crosslinking)

3. **Oxaliplatin**: Different leaving groups
   - Used for colorectal cancer

### Cisplatin Mechanism
1. Cellular uptake (passive diffusion, CTR1 transporter)
2. Aquation: Pt-Cl + H₂O → Pt-OH₂⁺ + Cl⁻
3. DNA binding: intrastrand crosslinks (65%), interstrand crosslinks (5%)
4. DNA damage response → apoptosis

### Gold Drugs
- **Auranofin**: Au(I) for rheumatoid arthritis
- Mechanism: inhibits thioredoxin reductase
- Au(I) binds to cysteine residues

### Radiopharmaceuticals
1. **Diagnostic**: ⁹⁹ᵐTc (γ emitter, t₁/₂ = 6 h)
2. **Therapeutic**: ⁹⁰Y, ¹⁷⁷Lu (β emitters)

### Chelation Therapy
- Remove toxic metals using selective chelators
- Deferoxamine (Fe), DMSA (Pb), DMPS (Hg)

---

## Key Formulas

### Cisplatin Aquation
```
PtCl₂(NH₃)₂ + H₂O → [PtCl(H₂O)(NH₃)₂]⁺ + Cl⁻
```

### DNA Crosslink Formation
```
Pt-X + DNA-N7(G) → Pt-DNA + X⁻
```

### Radioactive Decay
```
A = A₀ × e^(-λt)
λ = ln(2)/t₁/₂
```

### Chelation Equilibrium
```
Mⁿ⁺ + L ⇌ ML⁽ⁿ⁻ˣ⁾⁺
K_f = [ML⁽ⁿ⁻ˣ⁾⁺] / ([Mⁿ⁺][L]ˣ)
```

---

## Rules

1. Cisplatin: Pt(II) geometry is square planar
2. Transplatin is inactive (wrong geometry for DNA crosslinking)
3. Cisplatin preference: GG (65%) > AG (25%) > other
4. Au(I)-S bond: ~40 kcal/mol (strong, used in therapy)
5. ⁹⁹ᵐTc most widely used diagnostic isotope

---

## Constraints

- Cisplatin nephrotoxicity: dose-limiting
- Resistance mechanisms: increased DNA repair, glutathione conjugation
- Radiopharmaceuticals limited by half-life
- Chelators must be selective to avoid removing essential metals

---

## L3 Tool Targets

### `medicinal_inorganic_tools.py`

1. `cisplatin_aquation_rate()` - Calculate rate of cisplatin activation
2. `dna_crosslink_sites()` - Predict preferred binding sites from sequence
3. `chelator_affinity()` - Calculate K_f for metal-chelator complexes
4. `radioactivity_decay()` - Calculate activity after time t
5. `chelation_selectivity()` - Compare chelator affinity for different metals

---

## L4 Reference Data

### Cisplatin Data
- Molecular weight: 300 g/mol
- Solubility: 1 mg/mL in water
- Typical dose: 50-100 mg/m²
- Half-life: 30 min (free), days (protein-bound)

### Au-S Bond Properties
- Bond energy: ~40 kcal/mol
- Bond length: ~2.3 Å
- Au(I) coordination: typically linear 2-coordinate

### Radiopharmaceutical Data
- ⁹⁹ᵐTc: t₁/₂ = 6.0 h, E_γ = 140 keV
- ²⁰¹Tl: t₁/₂ = 73 h (cardiac imaging)
- ⁹⁰Y: t₁/₂ = 64 h (therapy)

### Chelator Affinities
- Deferoxamine for Fe(III): K ≈ 10³¹ M⁻¹
- DMSA for Pb²⁺: K ≈ 10²² M⁻¹
- EDTA for Ca²⁺: K ≈ 10¹⁰ M⁻¹

---

## L5 Worked Examples

### Example 1: Cisplatin Dose Calculation
Calculate the mg dose for a 70 kg patient at 100 mg/m².

### Example 2: Radioactive Decay
Calculate the remaining activity of ⁹⁹ᵐTc after 6 hours.

### Example 3: Chelation Equilibrium
Calculate free [Fe³⁺] when 1 μM Fe³⁺ is treated with deferoxamine (K = 10³¹ M⁻¹).

---

## Cross-References

- → `metal_nucleic_acid.md` (DNA binding)
- → `coordination_chemistry.md` (Platinum chemistry)
- → `radioactivity.md` (Nuclear decay)
- → `toxic_metals.md` (Heavy metal poisoning)
