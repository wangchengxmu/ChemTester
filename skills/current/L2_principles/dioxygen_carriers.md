# Dioxygen Carriers

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 4
**Level**: Graduate
**Related L1 Entry**: 128 - Dioxygen Carriers

---

## Core Concepts

### Hemoglobin Structure
- α₂β₂ tetramer (4 subunits, 4 hemes)
- Each heme contains Fe(II) in a porphyrin ring
- Fe(II) is 5-coordinate in deoxy state (His F8 as proximal ligand)
- Fe(II) becomes 6-coordinate upon O₂ binding

### O₂ Binding Cooperativity
- Positive cooperativity: binding of one O₂ facilitates subsequent binding
- T (tense) state: low affinity, deoxy form
- R (relaxed) state: high affinity, oxy form
- Allosteric transition: T ↔ R

### Key Parameters
- **P₅₀**: pO₂ at 50% saturation
- **Hill coefficient (n)**: measure of cooperativity
- **Bohr effect**: pH dependence of O₂ affinity

---

## Key Formulas

### Hill Equation (O₂ Saturation)
```
Y = pO₂ⁿ / (P₅₀ⁿ + pO₂ⁿ)
```
where:
- Y = fractional saturation
- n = Hill coefficient
- P₅₀ = pO₂ at half-saturation

### Bohr Effect
```
d(log P₅₀)/dpH ≈ -0.5 (for hemoglobin)
```
Lower pH → higher P₅₀ → lower affinity

### Adair Equation (4-site binding)
```
Y = (K₁p + 2K₁K₂p² + 3K₁K₂K₃p³ + 4K₁K₂K₃K₄p⁴) / (4(1 + K₁p + K₁K₂p² + K₁K₂K₃p³ + K₁K₂K₃K₄p⁴))
```

### O₂ Binding Equilibrium
```
Hb + nO₂ ⇌ Hb(O₂)ₙ
```

---

## Rules

1. Fe(II) in heme binds O₂ reversibly; Fe(III) (met) does not
2. CO binds with 200-250× affinity of O₂ (competitive inhibitor)
3. Hill coefficient: n = 1 (no cooperativity) to n ≈ 2.8 (strong cooperativity)
4. Myoglobin (monomer): no cooperativity (n = 1)
5. Fetal hemoglobin: lower P₅₀ than adult (higher O₂ affinity)

---

## Constraints

- Normal arterial pO₂: ~100 torr (13.3 kPa)
- Normal venous pO₂: ~40 torr (5.3 kPa)
- Hemoglobin P₅₀: ~26 torr (normal blood)
- Myoglobin P₅₀: ~2-3 torr
- CO-Hb saturation > 50% is life-threatening

---

## L3 Tool Targets

### `dioxygen_carrier_tools.py`

1. `oxygen_saturation_hill()` - Calculate Y from pO₂, P₅₀, and n
2. `p50_from_hill_plot()` - Determine P₅₀ from saturation data
3. `bohr_effect_shift()` - Calculate P₅₀ change with pH
4. `co_poisoning_effect()` - Predict O₂ saturation reduction from CO-Hb level
5. `hemoglobin_oxygen_delivery()` - Calculate O₂ delivery (arterial - venous saturation)

---

## L4 Reference Data

### Hemoglobin Properties
- Molecular weight: ~64.5 kDa
- 4 subunits (α₂β₂)
- 4 heme groups
- P₅₀: ~26 torr
- Hill coefficient: 2.8-3.0

### Myoglobin Properties
- Molecular weight: ~17 kDa
- Single polypeptide
- 1 heme
- P₅₀: 2-3 torr
- Hill coefficient: 1.0

### Heme Iron Properties
- Fe-O₂ bond length: ~1.8 Å
- O-O bond length: 1.21 Å (free), 1.30 Å (bound)
- Fe-O-O angle: ~120° (end-on binding)

### CO Binding
- CO affinity: 200-250× O₂ affinity
- CO-Hb half-life: 4-6 hours (room air)
- Treatment: 100% O₂ or hyperbaric O₂

---

## L5 Worked Examples

### Example 1: O₂ Saturation from Hill Equation
Calculate Y for hemoglobin at pO₂ = 40 torr, P₅₀ = 26 torr, n = 2.8.

### Example 2: Bohr Effect
Calculate the change in P₅₀ when pH drops from 7.4 to 7.2.

### Example 3: CO Poisoning
Predict the reduction in O₂-carrying capacity with 20% CO-Hb.

---

## Cross-References

- → `heme_chemistry.md` (Porphyrin and heme structure)
- → `cooperative_binding.md` (Allostery and cooperativity)
- → `iron_metabolism.md` (Fe transport and storage)
- → `respiratory_physiology.md` (Gas exchange)
