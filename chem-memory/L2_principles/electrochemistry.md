---
id: electrochemistry.core
layer: 2
title: Electrochemistry
parent: ../L1_ontology/chemistry-core-map.md#entry-67
stability: high
confidence: very_high
last_verified: 2026-03-16
source: Brown et al., Chemistry: The Central Science, Ch20
---

# Electrochemistry

## Core Concept

Electrochemistry studies the relationship between chemical reactions and electricity, including redox reactions, galvanic cells, and electrolysis.

---

## Redox Reactions

### Oxidation States

**Rules for Assigning Oxidation States:**
1. Free element = 0
2. Monatomic ion = ion charge
3. H in compounds = +1 (except hydrides, -1)
4. O in compounds = -2 (except peroxides, -1; superoxides, -0.5)
5. Sum of oxidation states = overall charge

### Half-Reaction Method

**Balancing in Acidic Solution:**
1. Write skeletal equation
2. Balance atoms other than H and O
3. Balance O by adding H₂O
4. Balance H by adding H⁺
5. Balance charge by adding e⁻

**Balancing in Basic Solution:**
1. Balance as if acidic
2. Add OH⁻ to neutralize H⁺
3. Cancel water on both sides

---

## Galvanic (Voltaic) Cells

### Cell Components

| Component | Function |
|-----------|----------|
| Anode | Oxidation occurs, electrons leave |
| Cathode | Reduction occurs, electrons enter |
| Salt bridge | Maintains charge neutrality |
| External circuit | Electron flow path |

### Cell Notation

```
Anode | Anode solution || Cathode solution | Cathode

Example: Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s)
```

### Standard Cell Potential

$$E°_{cell} = E°_{cathode} - E°_{anode}$$

**Sign Convention:**
- Positive E°cell = spontaneous reaction
- All reduction potentials measured relative to SHE (E° = 0.00 V)

---

## Thermodynamics and Cell Potential

### Relationship to Gibbs Free Energy

$$\Delta G° = -nFE°_{cell}$$

where:
- n = moles of electrons transferred
- F = Faraday constant = 96,485 C/mol e⁻
- E°cell = standard cell potential (V)

### Relationship to Equilibrium Constant

$$E°_{cell} = \frac{RT}{nF} \ln K = \frac{0.0592}{n} \log K \quad (at \, 25°C)$$

---

## Nernst Equation

### Nonstandard Conditions

$$E = E° - \frac{RT}{nF} \ln Q = E° - \frac{0.0592}{n} \log Q \quad (at \, 25°C)$$

where Q = reaction quotient

### Applications
1. Calculate cell potential at nonstandard concentrations
2. Determine ion concentrations from measured potentials
3. pH measurement (glass electrode)

---

## Concentration Cells

**Same half-reactions, different concentrations:**

$$E = \frac{0.0592}{n} \log \frac{[ion]_{cathode}}{[ion]_{anode}}$$

At equilibrium: E = 0, concentrations equal

---

## Batteries and Fuel Cells

### Primary (Non-rechargeable) Batteries

| Battery | Anode | Cathode | Cell Voltage |
|---------|-------|---------|--------------|
| Dry cell (Leclanché) | Zn | MnO₂ | ~1.5 V |
| Alkaline | Zn | MnO₂ | ~1.5 V |
| Mercury | Zn | HgO | ~1.3 V |

### Secondary (Rechargeable) Batteries

| Battery | Anode | Cathode | Cell Voltage |
|---------|-------|---------|--------------|
| Lead-acid | Pb | PbO₂ | ~2.0 V |
| Ni-Cd | Cd | NiO(OH) | ~1.2 V |
| Li-ion | C (graphite) | LiCoO₂ | ~3.7 V |

### Fuel Cells

- H₂-O₂ fuel cell: 2H₂ + O₂ → 2H₂O
- Continuous fuel supply
- High efficiency (~50-70%)

---

## Corrosion

### Electrochemical Nature

```
Anode (Fe oxidation): Fe → Fe²⁺ + 2e⁻
Cathode (O₂ reduction): O₂ + 2H₂O + 4e⁻ → 4OH⁻

Overall: 2Fe + O₂ + 2H₂O → 2Fe(OH)₂
```

### Protection Methods

| Method | Mechanism |
|--------|-----------|
| Coating | Barrier to O₂ and H₂O |
| Galvanization | Zn sacrificial anode |
| Cathodic protection | External sacrificial anode |
| Passivation | Protective oxide layer |

---

## Electrolysis

### Quantitative Aspects

**Faraday's Laws:**
1. Mass produced ∝ charge passed
2. 1 mol e⁻ = 96,485 C (1 Faraday)

$$m = \frac{I \times t \times M}{n \times F}$$

where:
- m = mass (g)
- I = current (A)
- t = time (s)
- M = molar mass (g/mol)
- n = electrons per ion

### Common Applications

| Process | Reaction |
|---------|----------|
| Water electrolysis | 2H₂O → 2H₂ + O₂ |
| Aluminum production | Al³⁺ + 3e⁻ → Al |
| Chlor-alkali | 2Cl⁻ → Cl₂ + 2e⁻ |
| Electroplating | Metal deposition |

---

## Key Equations Summary

| Equation | Use |
|----------|-----|
| E°cell = E°cathode - E°anode | Standard cell potential |
| ΔG° = -nFE° | Free energy from potential |
| E = E° - (0.0592/n)log Q | Nernst equation |
| E° = (0.0592/n)log K | Equilibrium from potential |
| m = ItM/nF | Electrolysis mass |

---

## Related Topics

- `gibbs_free_energy.md` - Thermodynamic basis
- `redox_reactions.md` - Electron transfer
- `corrosion_science.md` - Degradation processes
- `batteries_and_fuel_cells.md` - Energy storage

---

## L3 Tool Call Directives

When solving electrochemistry problems, ALWAYS use these tools. Do NOT calculate manually.

### Electrolysis calculations:
- `mass_from_electrolysis(current, time, molar_mass, n_electrons)` → mass (g)
- `moles_from_electrolysis(current, time, n_electrons)` → moles
- `time_for_mass(mass, current, molar_mass, n_electrons)` → time (s)
- `current_for_mass(mass, time, molar_mass, n_electrons)` → current (A)

**How to determine n_electrons:** Write the half-reaction first. n = electrons transferred per formula unit.
- Cu²⁺ + 2e⁻ → Cu: n=2
- Al³⁺ + 3e⁻ → Al: n=3
- Ag⁺ + e⁻ → Ag: n=1
- 2H₂O → O₂ + 4H⁺ + 4e⁻: n=2 (per H₂O molecule, 4 total for O₂)

### Cell potential calculations:
- `cell_potential()` — Calculate E°cell from half-reactions
- `nernst_equation()` — Nonstandard potential: E = E° - (0.0592/n)log Q
- `equilibrium_from_potential()` — K from E°cell

### Key constants:
- F = 96,485 C/mol e⁻
- R = 8.314 J/(mol·K)
- At 25°C: RT/F·ln(10) = 0.0592 V

## L4 Data

- Standard reduction potentials table
- Battery specifications
- Corrosion rates by environment

---

## L5 Examples

- Cell potential calculation
- Nernst equation application
- Electrolysis mass calculation

## Data Reference
- L4 Data: L4_reference/electrode_potentials.csv — Standard reduction potentials E° for 28 half-reactions
- L4 Reference: L4_reference/THERMODYNAMIC_DATABASES.md — Links to NIST, CRC Handbook
