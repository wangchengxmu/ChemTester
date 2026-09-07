# Nitrogenase and Hydrogenases

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 7
**Level**: Graduate
**Related L1 Entry**: 131 - Nitrogenase and Hydrogenases

---

## Core Concepts

### Nitrogenase
- Catalyzes N₂ → 2NH₃ (nitrogen fixation)
- Requires 16-18 ATP per N₂ fixed
- Extremely O₂-sensitive
- Two-component system: Fe protein + MoFe protein

### Nitrogenase Cofactors
1. **FeMo-cofactor (FeMoco)**
   - Composition: Fe₇MoS₉C-homocitrate
   - Located in MoFe protein
   - N₂ binding site

2. **P-cluster**
   - [Fe₈S₇] cluster
   - Mediates ET between Fe protein and FeMoco

### Hydrogenases
- Catalyze: H₂ ⇌ 2H⁺ + 2e⁻
- Two major classes:
  1. **[Fe-Fe] hydrogenase**: H₂ evolution (high activity)
  2. **[Ni-Fe] hydrogenase**: H₂ oxidation (more O₂ tolerant)

### Fe-S Clusters
- Electron carriers in both nitrogenase and hydrogenases
- [Fe₂S₂], [Fe₃S₄], [Fe₄S₄] types
- Delocalized electrons

---

## Key Formulas

### Nitrogenase Reaction
```
N₂ + 8H⁺ + 8e⁻ + 16ATP → 2NH₃ + H₂ + 16ADP + 16Pi
```

### Hydrogenase Reaction
```
H₂ ⇌ 2H⁺ + 2e⁻    E°' = -0.42 V
```

### Fe-S Cluster Redox
```
[Fe₄S₄]²⁺ + e⁻ ⇌ [Fe₄S₄]⁺
```

### ATP Requirement
```
ATP/N₂ = 16-18 (in vivo)
```

---

## Rules

1. Nitrogenase is extremely O₂-sensitive (inactivated by O₂)
2. H₂ is always produced as a byproduct of N₂ fixation
3. [Fe-Fe] hydrogenases are more active but more O₂-sensitive
4. [Ni-Fe] hydrogenases can tolerate some O₂
5. Alternative substrates: C₂H₂ → C₂H₄, N₂O → N₂ + H₂O

---

## Constraints

- Nitrogenase rate: 1-3 N₂ per second per enzyme
- Fe protein requires Mg-ATP for electron transfer
- N₂ binding competes with H₂ evolution
- CO, NO inhibit hydrogenases (competitive)
- Fe-S clusters degrade under oxidative stress

---

## L3 Tool Targets

### `nitrogenase_hydrogenase_tools.py`

1. `nitrogenase_atp_cost()` - Calculate ATP required for N₂ fixation
2. `hydrogen_evolution_rate()` - Calculate H₂ production from hydrogenase
3. `fe_s_redox_potential()` - Calculate cluster potential from composition
4. `nitrogenase_inhibition()` - Predict inhibition by alternative substrates
5. `h2_production_yield()` - Calculate H₂ yield relative to N₂ fixed

---

## L4 Reference Data

### Nitrogenase Data
- Fe protein MW: ~60 kDa (dimer of identical subunits)
- MoFe protein MW: ~230 kDa (α₂β₂)
- FeMoco: Fe₇MoS₉C-homocitrate
- P-cluster: [Fe₈S₇]
- Turnover: 1-3 N₂/s

### Hydrogenase Data
- [Fe-Fe] hydrogenase: ~50 kDa, ~1000 s⁻¹
- [Ni-Fe] hydrogenase: ~60-90 kDa, ~100 s⁻¹
- H-cluster (Fe-Fe): [Fe₄S₄]-[2Fe] subcluster

### Fe-S Cluster Potentials
- [Fe₂S₂] (ferredoxin): -400 to -200 mV
- [Fe₄S₄] (ferredoxin): -700 to -100 mV
- [Fe₄S₄] (HiPIP): +100 to +400 mV

### Redox Potentials
- H₂/2H⁺: -0.42 V
- N₂/NH₃: -0.28 V
- FeMoco: ~-0.4 V

---

## L5 Worked Examples

### Example 1: ATP Cost
Calculate the total ATP needed to fix 1 mol N₂.

### Example 2: H₂ Production
Calculate the expected H₂ production when fixing 10 mmol N₂.

### Example 3: Fe-S Redox
Determine the potential for [Fe₄S₄]²⁺/⁺ couple given structural parameters.

---

## Cross-References

- → `iron_sulfur_proteins.md` (Fe-S cluster chemistry)
- → `redox_reactions.md` (Electron transfer)
- → `enzyme_kinetics.md` (Enzyme mechanisms)
- → `metal_clusters.md` (Polymetallic clusters)
