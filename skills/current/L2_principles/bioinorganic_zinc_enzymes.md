# Bioinorganic Zinc Enzymes

**Source**: Bioinorganic Chemistry (Bertini et al.), Chapter 2
**Level**: Graduate
**Related L1 Entry**: 126 - Bioinorganic Zinc Enzymes

---

## Core Concepts

### Zinc as a Lewis Acid Catalyst
- ZnÂ²â?is a dÂ¹â?ion with filled d orbitals, no redox activity
- Acts purely as a Lewis acid (electron pair acceptor)
- Polarizes substrates for nucleophilic attack
- Tetrahedral or trigonal bipyramidal coordination geometry

### Key Zinc Enzymes
1. **Carbonic Anhydrase (CA)**
   - COâ?+ HâO â?HCOââ» + Hâ?   - One of the fastest enzymes known (k_cat ~ 10â?sâ»Â?
   - ZnÂ²â?bound to 3 His residues + HâO/OHâ?
2. **Carboxypeptidase A**
   - Peptide hydrolysis at C-terminus
   - ZnÂ²â?activates water for nucleophilic attack
   - ZnÂ²â?coordinates His69, Glu72, His196

### Zn-HâO pKa Depression
- Free water: pKa = 14.7
- Zn-bound water in CA: pKa = 6.9-7.1
- ~8 unit depression enables catalysis at physiological pH

---

## Key Formulas

### Carbonic Anhydrase Mechanism
```
Zn-OHâ?+ COâ?â?Zn-HCOââ»
Zn-HCOââ» + HâO â?Zn-HâO + HCOââ»
Zn-HâO â?Zn-OHâ?+ Hâ?(rate-limiting)
```

### Rate Enhancement
```
k_cat / k_uncat = up to 10Â¹â?```

### Zinc Coordination
```
[ZnLâ?HâO)]â¿âº â?[ZnLâ?OH)]â½â¿â»Â¹â¾â?+ Hâ?```

---

## Rules

1. ZnÂ²â?concentration in cells: 10â»â¹ to 10â»Â¹Â?M free ion (tightly regulated)
2. Zinc coordination number: typically 4 (tetrahedral) or 5 (trigonal bipyramidal)
3. Metal substitution studies: CoÂ²â?best mimic (spectroscopic probe)
4. Inhibition by chelators: EDTA, 1,10-phenanthroline (competitive)

---

## Constraints

- pH optimum: typically 6.5-8.0 for Zn-HâO deprotonation
- Metal-free apoenzyme can be reconstituted with ZnÂ²â?- Heavy metals (HgÂ²â? PbÂ²â? displace ZnÂ²â?and inactivate enzyme
- Coordination geometry affects catalytic efficiency

---

## L3 Tool Targets

### `bioinorganic_zinc_enzyme_tools.py`

1. `carbonic_anhydrase_turnover()` - Calculate CA activity from COâ?hydration rates
2. `zinc_water_pka()` - Calculate pKa of Zn-bound water from ligand field
3. `zinc_binding_constant()` - Calculate ZnÂ²â?affinity from inhibition data
4. `enzyme_rate_enhancement()` - Calculate k_cat/k_uncat ratio
5. `metal_substitution_effect()` - Predict activity change with metal substitution

---

## L4 Reference Data

### Zinc Ionic Properties
- Ionic radius: 0.74 Ã
- Preferred coordination: 4 (tetrahedral)
- Electronegativity: 1.65 (Pauling)
- No redox activity (dÂ¹â?configuration)

### Carbonic Anhydrase Data
- Turnover number: ~10â?sâ»Â?- Zn-HâO pKa: 6.9-7.1
- Molecular weight: ~30 kDa (CA II)
- K_m for COâ? ~10 mM

### Carboxypeptidase A Data
- Turnover number: ~100 sâ»Â?- Zn-OHâ?pKa: ~9.0
- Molecular weight: ~35 kDa

---

## L5 Worked Examples

### Example 1: Carbonic Anhydrase Turnover
Calculate the time to hydrate 1 mmol COâ?with 1 Î¼M CA at pH 7.4.

### Example 2: pKa Depression
Calculate the pKa of Zn-bound water given a ligand field of 3 His residues.

### Example 3: Inhibition Analysis
Determine K_i for acetazolamide inhibition from activity data.

---

## Cross-References

- â?`enzymes_general.md` (Enzyme kinetics fundamentals)
- â?`lewis_acid_base.md` (Lewis acid theory)
- â?`coordination_chemistry.md` (Metal coordination principles)
- â?`protein_structure.md` (Metalloprotein structure)


## Implementations

- Implementation: `../L3_functions/bioinorganic_chemistry_tools.py`
