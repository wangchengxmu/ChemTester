# Calcium Signaling Biology

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 3
**Level**: Graduate
**Related L1 Entry**: 127 - Calcium Signaling Biology

---

## Core Concepts

### Calcium Homeostasis
- Resting cytosolic [Ca²⁺]: 100-200 nM
- Extracellular [Ca²⁺]: 1-2 mM
- 10⁴-fold gradient across plasma membrane
- Rapid signaling via transient Ca²⁺ spikes

### EF-Hand Motif
- Helix-loop-helix structural motif
- Loop provides 6-7 oxygen ligands for Ca²⁺
- Canonical sequence: 12-residue loop with specific positions
- Undergoes conformational change upon Ca²⁺ binding

### Key Ca²⁺-Binding Proteins
1. **Calmodulin (CaM)**
   - 4 EF-hand domains (2 per lobe)
   - Undergoes large conformational change
   - Regulates >100 target enzymes

2. **Troponin C**
   - 4 Ca²⁺ sites (2 high affinity, 2 regulatory)
   - Muscle contraction regulation

3. **Ca²⁺-ATPase (SERCA)**
   - Active transport: Ca²⁺_in + ATP → Ca²⁺_out + ADP + Pi
   - Maintains low cytosolic Ca²⁺

---

## Key Formulas

### Ca²⁺ Equilibrium Potential (Nernst)
```
E_Ca = (RT/2F) × ln([Ca²⁺]_out/[Ca²⁺]_in)
     = (0.059/2) × log([Ca²⁺]_out/[Ca²⁺]_in) at 25°C
```

### Ca²⁺ Binding (Michaelis-Menten type)
```
θ = [Ca²⁺]/(K_d + [Ca²⁺])
```

### Cooperative Binding (Hill Equation)
```
θ = [Ca²ⁿ]/(K_dⁿ + [Ca²⁺]ⁿ)
```

### Ca²⁺-ATPase Kinetics
```
V = V_max × [Ca²⁺]/(K_m + [Ca²⁺])
```

---

## Rules

1. Ca²⁺ binding constant for EF-hand: K_a ≈ 10⁵-10⁷ M⁻¹
2. Mg²⁺ competes with Ca²⁺ but lower affinity (K_a ≈ 10³ M⁻¹)
3. Cooperative binding: Hill coefficient n > 1 for calmodulin
4. Ca²⁺ binding induces α-helix formation in EF-hand loop

---

## Constraints

- Free Ca²⁺ in cytosol: 10⁻⁷ to 10⁻⁹ M
- Total Ca²⁺ in cells: ~1-2 mM (mostly buffered)
- Ca²⁺ spike duration: milliseconds to seconds
- Spatial gradients: microdomains near channels

---

## L3 Tool Targets

### `calcium_signaling_tools.py`

1. `calcium_equilibrium_potential()` - Calculate E_Ca from concentration gradient
2. `calcium_binding_saturation()` - Calculate θ from free [Ca²⁺] and K_d
3. `calmodulin_saturation()` - Calculate fractional saturation of CaM with Hill equation
4. `ca_atpase_rate()` - Calculate Ca²⁺-ATPase activity
5. `calcium_buffer_capacity()` - Calculate buffering capacity from free/total Ca²⁺

---

## L4 Reference Data

### Ca²⁺ Ionic Properties
- Ionic radius: 1.00 Å
- Preferred coordination: 6-8
- Electronegativity: 1.00 (Pauling)
- Binding preferences: oxygen donors (carboxylates, carbonyls)

### Calmodulin Data
- Molecular weight: ~17 kDa
- 4 Ca²⁺ binding sites
- K_d ≈ 10⁻⁶ M (average)
- Hill coefficient: 1.5-2.0

### Troponin C Data
- Molecular weight: ~18 kDa
- 4 Ca²⁺ sites
- K_d: 10⁻⁸ M (high affinity), 10⁻⁶ M (low affinity)

### Ca²⁺-ATPase Data
- K_m for Ca²⁺: 0.1-1 μM
- V_max: varies by isoform
- Stoichiometry: 2 Ca²⁺ per ATP

---

## L5 Worked Examples

### Example 1: Ca²⁺ Equilibrium Potential
Calculate E_Ca for [Ca²⁺]_out = 2 mM, [Ca²⁺]_in = 100 nM.

### Example 2: Calmodulin Saturation
Calculate fractional saturation of CaM at 1 μM free Ca²⁺ with K_d = 1 μM and n = 2.

### Example 3: Ca²⁺ Buffer Capacity
Calculate the buffer capacity given free Ca²⁺ = 100 nM and total Ca²⁺ = 1 mM.

---

## Cross-References

- → `enzyme_kinetics.md` (Michaelis-Menten kinetics)
- → `electrochemistry_cells.md` (Nernst equation)
- → `cooperative_binding.md` (Hill equation)
- → `protein_structure.md` (EF-hand structure)
