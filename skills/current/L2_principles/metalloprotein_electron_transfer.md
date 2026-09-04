# Metalloprotein Electron Transfer

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 6
**Level**: Graduate
**Related L1 Entry**: 130 - Metalloprotein Electron Transfer

---

## Core Concepts

### Marcus Theory
Electron transfer rate depends on:
- Driving force (ΔG°)
- Reorganization energy (λ)
- Distance between redox centers (r)

### Inner-Sphere vs Outer-Sphere ET
1. **Inner-Sphere ET**
   - Bridging ligand connects metal centers
   - Requires direct bond formation
   - Example: Cr²⁺ + Co(NH₃)₅Cl²⁺

2. **Outer-Sphere ET**
   - No direct bond between centers
   - Electron tunnels through space/protein
   - Example: Cytochrome c oxidation

### Key Metalloproteins
1. **Cytochromes**
   - Heme proteins with Fe(III)/Fe(II) redox couple
   - E°' ≈ +0.25 V (cytochrome c)

2. **Blue Copper Proteins**
   - Cu(II)/Cu(I) redox couple
   - Type I copper sites
   - E°' ≈ +0.3 to +0.8 V

3. **Iron-Sulfur Proteins**
   - [Fe₂S₂], [Fe₃S₄], [Fe₄S₄] clusters
   - E°' ≈ -0.7 to +0.1 V

---

## Key Formulas

### Marcus Equation
```
k_ET = k_0 × exp[-β(r - r₀)] × exp[-(ΔG° + λ)²/4λRT]
```

where:
- k_0 = pre-exponential factor
- β = decay constant (~1.0 Å⁻¹ for proteins)
- r = distance between centers
- λ = reorganization energy
- ΔG° = driving force

### Simplified Distance Dependence
```
k_ET ∝ exp(-βr)
```

### Driving Force
```
ΔG° = -nFΔE°
```

### Reorganization Energy
```
λ = λ_in + λ_out
```
- λ_in = inner-sphere (bond length changes)
- λ_out = outer-sphere (solvent reorganization)

---

## Rules

1. ET rate decreases exponentially with distance (β ≈ 1.0-1.4 Å⁻¹)
2. Electron tunneling distance limit: ~14 Å in proteins
3. Optimal rate when -ΔG° = λ (activationless)
4. Marcus inverted region: rate decreases for highly exergonic reactions
5. Edge-to-edge distance matters (not center-to-center)

---

## Constraints

- Typical β values: 1.0-1.4 Å⁻¹ for proteins
- Maximum tunneling distance: ~14 Å
- Reorganization energy: 0.5-1.0 eV for metalloproteins
- Protein medium affects electron tunneling

---

## L3 Tool Targets

### `metalloprotein_et_tools.py`

1. `marcus_et_rate()` - Calculate k_ET from Marcus equation
2. `et_distance_decay()` - Calculate rate from distance and β
3. `reorganization_energy()` - Calculate λ from activation energy
4. `driving_force_from_potential()` - Calculate ΔG° from redox potentials
5. `optimal_driving_force()` - Find ΔG° for maximum rate

---

## L4 Reference Data

### Cytochrome c Data
- E°' ≈ +0.25 V
- Molecular weight: ~12 kDa
- Fe-S(Met80) bond: 2.3 Å
- Edge exposure for ET

### Blue Copper Proteins
- E°' range: +0.3 to +0.8 V
- Cu coordination: 2 His, 1 Cys, 1 Met
- Typical MW: 10-20 kDa

### Fe-S Cluster Data
- [Fe₂S₂] E°': -400 to +200 mV
- [Fe₄S₄] E°': -700 to -100 mV
- Cluster-core distances: ~2.7 Å (Fe-Fe), ~2.3 Å (Fe-S)

### β Values
- Water: ~1.7 Å⁻¹
- Proteins: ~1.0-1.4 Å⁻¹
- Saturated hydrocarbons: ~0.8 Å⁻¹

---

## L5 Worked Examples

### Example 1: Distance Dependence
Calculate the rate ratio for ET at 10 Å vs 14 Å (β = 1.0 Å⁻¹).

### Example 2: Marcus Theory
Calculate k_ET for ΔG° = -0.5 eV, λ = 0.8 eV, β = 1.0 Å⁻¹, r = 12 Å.

### Example 3: Driving Force
Calculate ΔG° for electron transfer from cytochrome c (+0.25 V) to cytochrome c oxidase (+0.35 V).

---

## Cross-References

- → `redox_reactions.md` (Electrochemistry fundamentals)
- → `quantum_tunneling.md` (Tunneling theory)
- → `heme_chemistry.md` (Cytochromes)
- → `iron_sulfur_proteins.md` (Fe-S clusters)
