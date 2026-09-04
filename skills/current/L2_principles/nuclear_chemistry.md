---
id: nuclear_chemistry.expanded
layer: 2
title: Nuclear Chemistry
parent: ../L1_ontology/chemistry-core-map.md#entry-68
stability: high
confidence: high
last_verified: 2026-03-16
source: Brown et al., Chemistry: The Central Science, Ch21
---

# Nuclear Chemistry

## Core Concept

Nuclear chemistry studies changes in atomic nuclei, including radioactive decay, nuclear reactions, and the energy associated with nuclear processes.

---

## Nuclear Structure

### Nuclide Notation

$$^A_Z X$$

where:
- A = mass number (protons + neutrons)
- Z = atomic number (protons)
- X = element symbol

### Binding Energy

**Mass Defect:**
$$\Delta m = Z(m_p) + N(m_n) - m_{nucleus}$$

**Binding Energy:**
$$BE = \Delta m \times c^2$$

**Binding Energy per Nucleon:**
- Peaks around Fe-56 (~8.8 MeV/nucleon)
- Lower for light and heavy nuclei
- Explains why fusion of light elements and fission of heavy elements release energy

---

## Radioactive Decay

### Decay Modes

| Mode | Symbol | Change | Example |
|------|--------|--------|---------|
| Alpha decay | Î± | A-4, Z-2 | Â²Â³â¸U â?Â²Â³â´Th + â´He |
| Beta decay | Î²â?| Z+1 | Â¹â´C â?Â¹â´N + eâ?|
| Positron emission | Î²â?| Z-1 | Â¹Â¹C â?Â¹Â¹B + eâ?|
| Electron capture | EC | Z-1 | â´â°K + eâ?â?â´â°Ar |
| Gamma emission | Î³ | No change | Excited â?ground state |

### Decay Kinetics

**First-Order Decay:**
$$N = N_0 e^{-\lambda t}$$

**Half-Life:**
$$t_{1/2} = \frac{\ln 2}{\lambda} = \frac{0.693}{\lambda}$$

**Activity:**
$$A = \lambda N = A_0 e^{-\lambda t}$$

### Decay Series

**Uranium-238 Series:**
```
Â²Â³â¸U â?Â²Â³â´Th â?Â²Â³â´Pa â?Â²Â³â´U â?Â²Â³â°Th â?Â²Â²â¶Ra â?Â²Â²Â²Rn â?Â²Â¹â¸Po â?Â²Â¹â´Pb â?Â²Â¹â´Bi â?Â²Â¹â´Po â?Â²Â¹â°Pb â?Â²Â¹â°Bi â?Â²Â¹â°Po â?Â²â°â¶Pb (stable)
```

---

## Nuclear Stability

### Factors Affecting Stability

1. **N/Z Ratio:**
   - Light nuclei: N â?Z
   - Heavy nuclei: N > Z (up to N/Z â?1.5)

2. **Even vs Odd:**
   - Even-even nuclei most stable
   - Odd-odd nuclei least stable

3. **Magic Numbers:**
   - 2, 8, 20, 28, 50, 82, 126
   - Closed shells = extra stability

### Valley of Stability

Nuclei with optimal N/Z ratio are stable; others decay toward the valley.

---

## Nuclear Reactions

### Transmutation

**Alpha bombardment:**
$$^A_Z X + ^4_2 He \rightarrow ^{A+4}_{Z+2} Y + ^1_0 n$$

**Neutron capture:**
$$^A_Z X + ^1_0 n \rightarrow ^{A+1}_Z X$$

### Q-Value (Energy Release)

$$Q = (m_{reactants} - m_{products}) \times c^2$$

- Q > 0: Exothermic (energy released)
- Q < 0: Endothermic (energy required)

---

## Nuclear Fission

### Process

Heavy nucleus splits into lighter fragments:

$$^{235}U + ^1_0 n \rightarrow ^{141}Ba + ^{92}Kr + 3^1_0 n + energy$$

### Chain Reaction

- Neutrons released can trigger more fissions
- Critical mass required for sustained reaction
- Controlled in reactors, uncontrolled in weapons

### Energy Release

- ~200 MeV per fission of U-235
- Compare: ~3 eV per chemical bond

---

## Nuclear Fusion

### Process

Light nuclei combine to form heavier nucleus:

$$^2H + ^3H \rightarrow ^4He + ^1_0 n + 17.6 MeV$$

### Conditions Required

- High temperature (10â?K)
- High pressure
- Plasma confinement

### Stellar Fusion

**Proton-proton chain (Sun):**
$$4^1H \rightarrow ^4He + 2e^+ + 2\nu_e + 26.7 MeV$$

---

## Biological Effects

### Radiation Units

| Unit | Measures | Conversion |
|------|----------|------------|
| Gray (Gy) | Absorbed dose | 1 Gy = 1 J/kg |
| Sievert (Sv) | Equivalent dose | Sv = Gy Ã QF |
| Becquerel (Bq) | Activity | 1 Bq = 1 decay/s |
| Curie (Ci) | Activity | 1 Ci = 3.7 Ã 10Â¹â?Bq |

### Quality Factors

| Radiation | QF |
|-----------|-----|
| X-rays, Î³-rays | 1 |
| Î² particles | 1 |
| Î± particles | 20 |
| Neutrons | 5-20 |

### Effects by Dose

| Dose (Sv) | Effect |
|-----------|--------|
| 0-0.25 | No immediate effect |
| 0.25-1 | Blood changes |
| 1-3 | Radiation sickness |
| 3-5 | 50% lethal in 30 days |
| >5 | Usually fatal |

---

## Applications

### Dating Methods

**Carbon-14 Dating:**
$$t = \frac{1}{\lambda} \ln \frac{A_0}{A}$$

- Half-life: 5730 years
- Useful for 100-50,000 years

**Uranium-Lead Dating:**
- Half-life: 4.5 Ã 10â?years
- Useful for geological timescales

### Medical Applications

| Application | Isotope | Use |
|-------------|---------|-----|
| Imaging | Tc-99m | Bone scans |
| Therapy | I-131 | Thyroid treatment |
| PET | F-18 | Glucose metabolism |

---

## Key Equations Summary

| Equation | Use |
|----------|-----|
| N = Nâe^(-Î»t) | Decay law |
| tâ?â?= 0.693/Î» | Half-life |
| BE = Îm Ã 931.5 MeV/amu | Binding energy |
| E = mcÂ² | Mass-energy equivalence |
| Q = (m_react - m_prod)cÂ² | Reaction energy |

---

## Related Topics

- `electrochemistry.md` - Energy storage
- `thermodynamics.md` - Energy in reactions
- `atomic_structure.md` - Nuclear models

---

## L3 Tools

- `decay_activity()` - Calculate activity
- `half_life_remaining()` - Fraction remaining
- `binding_energy()` - BE calculation
- `q_value()` - Reaction energy

---

## L4 Data

- Nuclide table
- Half-life values
- Decay series data

---

## L5 Examples

- Carbon dating calculation
- Binding energy per nucleon
- Reactor fuel consumption


## Implementations

## L3 Tool Call Directive

When solving nuclear chemistry problems (half-life, decay, binding energy), call the appropriate L3 function:

**remaining_amount** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Calculate amount remaining after radioactive decay over time.
- Parameters: `initial_amount`, `time`, `half_life`

**remaining_fraction** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Calculate fraction remaining (or percentage decayed) after a given time.
- Parameters: `time`, `half_life`

**time_to_decay** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Calculate time needed for a sample to decay to a given amount.
- Parameters: `initial_amount`, `final_amount`, `half_life`

**half_life_to_decay_constant** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Convert half-life to decay constant λ (λ = ln2 / t½).
- Parameters: `half_life`

**binding_energy** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Calculate nuclear binding energy from mass defect.
- Parameters: `protons`, `neutrons`, `actual_mass` (atomic mass in amu)
- Note: Uses mass of proton (1.007276 amu), neutron (1.008665 amu), and electron (0.000549 amu).

**binding_energy_per_nucleon** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Calculate binding energy per nucleon for stability comparison.
- Parameters: `protons`, `neutrons`, `actual_mass`

**balance_nuclear_equation** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Fill in missing particle in a nuclear equation.
- Parameters: `reactant_a`, `reactant_z`, `product_a`, `product_z`, `emitted_a`, `emitted_z` (set one pair to None)

**predict_decay_mode** (`L3_functions/nuclear_chemistry_tools.py`):
- Use when: Predict likely decay mode based on N/Z ratio.
- Parameters: `protons`, `neutrons`

**Critical notes:**
- For carbon dating: use `remaining_amount` with half_life = 5730 years.
- Ensure consistent time units throughout calculations.
- `actual_mass` should be the measured atomic mass of the nuclide in amu.


- Implementation: `../L3_functions/nuclear_chemistry_tools.py`

## L3 Tool Call Directives

**Source:** `nuclear_chemistry_tools.py`
Half-life, decay calculations, binding energy, nuclear equations, decay mode prediction.

### Available functions:
- `half_life_to_decay_constant(half_life)` → float — λ = ln(2)/t½ (s⁻¹)
- `decay_constant_to_half_life(decay_constant)` → float — t½ = ln(2)/λ (s)
- `remaining_amount(initial_amount, time, half_life)` → float — N = N0 × (½)^(t/t½)
- `remaining_fraction(time, half_life)` → float — Fraction 0–1 remaining
- `time_to_decay(initial_amount, final_amount, half_life)` → float — t = t½ × log₂(N0/N)
- `activity(nuclei_count, decay_constant)` → float — A = λN (Bq)
- `binding_energy(protons, neutrons, actual_mass)` → float — BE in MeV (uses 1 amu = 931.5 MeV)
- `binding_energy_per_nucleon(protons, neutrons, actual_mass)` → float — BE/A in MeV
- `balance_nuclear_equation(reactant_a, reactant_z, product_a, product_z)` → tuple — (A, Z) of missing particle
- `predict_decay_mode(protons, neutrons)` → str — alpha/beta_minus/positron/stable based on n:p ratio
- `daughter_nuclide(parent_a, parent_z, decay_type)` → tuple — (A, Z) after decay
- `decay_chain_steps(initial_a, initial_z, decay_types)` → list — Chain of (A, Z) tuples

### Common errors:
- ❌ Inconsistent time units — convert all to same unit (seconds or years)
- ❌ Forgetting binding_energy uses atomic mass (includes electrons), not nuclear mass
- ❌ Confusing mass number A with atomic number Z in decay calculations
