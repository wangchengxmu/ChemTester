---
id: industrial_catalysis
layer: 2
title: Industrial Catalysis (Haber, Fischer-Tropsch, Ziegler-Natta)
parent: ../L1_ontology/chemistry-core-map.md#entry-267
stability: high
confidence: high
last_verified: 2026-03-24
source: LibreTexts Inorganic Chemistry (Haas), LibreTexts Catalysis Module
---

# Industrial Catalysis

## Core Concept

Heterogeneous catalysts underpin the chemical industry, enabling large-scale production of fertilizers, fuels, and polymers under optimized conditions of temperature, pressure, and selectivity.

---

## Haber-Bosch Process (NH₃ Synthesis)

### Reaction
$$\text{N}_2(g) + 3\text{H}_2(g) \rightleftharpoons 2\text{NH}_3(g) \quad \Delta H^\circ = -92.4 \text{ kJ/mol}$$

### Conditions
- **Catalyst:** Fe with K₂O and Al₂O₃ promoters
- **Temperature:** 400–500°C (kinetics favor high T, equilibrium favors low T)
- **Pressure:** 150–300 atm (equilibrium favors high P)
- **Yield:** ~15–20% per pass (recycle unreacted gases)

### Mechanism (surface)
1. N₂(g) → N₂(adsorbed)
2. N₂(adsorbed) → 2N(adsorbed) — RDS
3. H₂(g) → 2H(adsorbed)
4. N(ads) + 3H(ads) → NH₃(ads)
5. NH₃(ads) → NH₃(g) — desorption

---

## Fischer-Tropsch Synthesis

### Reaction
$$n\text{CO} + (2n+1)\text{H}_2 \rightarrow \text{C}_n\text{H}_{2n+2} + n\text{H}_2\text{O}$$

### Conditions
- **Catalyst:** Fe or Co (Fe: high-T, gas-to-liquids; Co: low-T, wax)
- **Temperature:** 200–350°C
- **Pressure:** 10–40 atm
- **Product distribution:** follows Anderson-Schulz-Flory (ASF) distribution

### ASF Distribution
$$W_n = (1-\alpha)^2 \cdot \alpha^{n-1}$$

Where α = chain growth probability, W_n = mass fraction of Cₙ.

---

## Ziegler-Natta Polymerization

### Catalyst
- **TiCl₄/MgCl₂** (Ziegler component) + **AlR₃** (Natta co-catalyst)
- Heterogeneous (solid Ti on support)

### Reaction
$$n\text{CH}_2=\text{CH}_2 \xrightarrow{\text{Z-N}} -(\text{CH}_2-\text{CH}_2)_n-$$

### Key Features
- Stereoregular polymers (isotactic/ syndiotactic polypropylene)
- Cossee-Arlman mechanism at Ti active sites
- Living-like character in some systems

---

## Other Major Processes

| Process | Reaction | Catalyst | Product |
|---------|----------|----------|---------|
| Contact Process | 2SO₂ + O₂ → 2SO₃ | V₂O₅ | H₂SO₄ |
| Ostwald Process | 4NH₃ + 5O₂ → 4NO + 6H₂O | Pt/Rh | HNO₃ |
| Steam Reforming | CH₄ + H₂O → CO + 3H₂ | Ni | H₂ |
| Methanol Synthesis | CO + 2H₂ → CH₃OH | Cu/ZnO/Al₂O₃ | CH₃OH |
| Water-Gas Shift | CO + H₂O → CO₂ + H₂ | Fe/Cr₂O₃ or Cu | H₂ |
| Catalytic Reforming | C₆H₁₄ → C₆H₆ + 4H₂ | Pt/Al₂O₃ | Aromatics |

---

## Complete Extraction: Industrial Catalytic Processes (LibreTexts)

### Contact Process (H₂SO₄ Manufacture)
- **Catalyst:** V₂O₅ (replaced Pt due to As poisoning)
- **Overall:** 2SO₂(g) + O₂(g) ⇌ 2SO₃(g)
- **Mechanism (redox cycle of vanadium):**
  - 2V₂O₅(s) + 2SO₂(g) ⇌ 2SO₃(g) + 2V₂O₄(s)
  - 2V₂O₄(s) + O₂(g) ⇌ 2V₂O₅(s)
- **Product:** H₂SO₄ (via SO₃ hydration)

### Haber-Bosch Process (NH₃ Synthesis)
- **Catalyst:** Fe with K₂O and Al₂O₃ promoters (originally Os)
- **Overall:** N₂(g) + 3H₂(g) ⇌ 2NH₃(g)
- **Surface mechanism:**
  1. N₂(g) → N₂(adsorbed)
  2. N₂(adsorbed) → 2N(adsorbed)
  3. H₂(g) → H₂(adsorbed) → 2H(adsorbed)
  4. N(ads) + 3H(ads) → NH₃(adsorbed)
  5. NH₃(adsorbed) → NH₃(g)

### Ostwald Process (HNO₃ Manufacture)
- **Catalyst:** Pt and Rh gauze
- **Reaction:** 4NH₃ + 5O₂ → 4NO + 6H₂O
- **Product:** HNO₃ (via NO oxidation to NO₂ then hydration)

### Catalytic Converter (Automotive)
- **Composition:** 1-3 g Pt on Al₂O₃ honeycomb
- **Functions:** Oxidizes CO → CO₂, hydrocarbons → CO₂ + H₂O, reduces NOx → N₂
- **Poisoning:** Lead (from tetraethyllead) irreversibly deactivates catalyst

### Sohio Process (Acrylonitrile)
- **Catalyst:** Bismuth phosphomolybdate
- **Reaction:** CH₂=CHCH₃ + NH₃ + 3/2 O₂ → CH₂=CHCN + 3H₂O
- **Product:** Acrylonitrile (for acrylic fibers, ABS plastic)

### Hydrogenation (Food Industry)
- **Catalysts:** Ni, Pd, Pt
- **Example:** RCH=CHR′ + H₂ → RCH₂—CH₂R′
- **Application:** Converting polyunsaturated vegetable oils to margarine
- **Key point:** H₂ dissociation energy (432 kJ/mol) is overcome by metal surface adsorption (exothermic, ΔH° ≥ −160 kJ/mol for Pt)

### Petroleum Industry Applications
- **Cracking:** SiO₂/Al₂O₃ catalyst breaks long-chain hydrocarbons into gasoline-range molecules
- **Reforming:** Pt catalyst converts hydrocarbon chains to aromatic rings (improves octane rating)

### Source Cross-References
- LibreTexts Inorganic Chemistry (Haas) 14.4
- LibreTexts Catalysis Module (Heterogeneous catalysis)
- ChemPRIME (Moore et al.) 18.12
- Physical Chemistry (LibreTexts) 29.8

---

## Textbook Problems

```json
{
  "id": "P2_industrial_catalysis_001",
  "topic": "Heterogeneous Catalysis",
  "difficulty": "medium",
  "question": "In the contact process, why was vanadium(V) oxide preferred over platinum as the catalyst?",
  "answer": "Platinum is susceptible to poisoning by arsenic impurities in the sulfur feedstock. V₂O₅ is more robust and less expensive.",
  "source": "LibreTexts Catalysis Module"
}
```

```json
{
  "id": "P2_industrial_catalysis_002",
  "topic": "Heterogeneous Catalysis",
  "difficulty": "medium",
  "question": "Write the six-step surface mechanism for the Haber-Bosch process on an iron catalyst.",
  "answer": "N₂(g)→N₂(ads)→2N(ads); H₂(g)→H₂(ads)→2H(ads); N(ads)+3H(ads)→NH₃(ads)→NH₃(g)",
  "source": "LibreTexts Catalysis Module"
}
```

```json
{
  "id": "P2_industrial_catalysis_003",
  "topic": "Catalyst Poisoning",
  "difficulty": "easy",
  "question": "Why was leaded gasoline prohibited for cars with catalytic converters?",
  "answer": "Lead atoms react irreversibly with the Pt surface, preventing CO and hydrocarbons from adsorbing and being oxidized.",
  "source": "ChemPRIME 18.12"
}
```

---

## Links

- L3: `../L3_functions/heterogeneous_catalysis_tools.py`
- L4: `../L4_reference/heterogeneous_catalysis_reference.csv`
- L5: `../L5_examples/heterogeneous_catalysis_examples.md`

---

## [Source: Wikipedia, Haber Process]
### Haber-Bosch Process (N₂ + 3H₂ → 2NH₃)
- **Conditions**: 150–300 atm, 400–500°C, Fe-based catalyst (Fe₃O₄ promoted with K₂O, Al₂O₃, CaO).
- **Thermodynamics**: ΔH° = −92 kJ/mol (exothermic), ΔS° = −199 J/(mol·K).
- **Le Chatelier**: Higher pressure favors product; lower temperature favors product but slows kinetics.
- **Single-pass conversion**: ~15–20%; unreacted gases recycled.
- **Global production**: ~150 million tonnes/year; feeds ~50% of world's nitrogen fertilizer.

## [Source: Wikipedia, Fischer–Tropsch Process]
### Fischer–Tropsch: CO + 2H₂ → (−CH₂−)ₙ + H₂O
- **Catalysts**: Fe or Co (Fe for coal-derived syngas, Co for natural gas-derived).
- **Conditions**: 1–30 atm, 200–350°C.
- **Product distribution** (Anderson-Schulz-Flory): Chain growth probability α determines product mix.
  - Linear alkanes (C₁–C₁₀₀+), α-olefins, alcohols.
  - W_n = (1−α)²·α^(n−1) where W_n = weight fraction of carbon number n.
- **Modern plants**: Sasol (South Africa), Shell Pearl GTL (Qatar).
- **Sasol Advanced Synthol**: High-temperature Fe catalyst, circulating fluidized bed.

## [Source: Wikipedia, Ziegler-Natta Catalyst]
### Ziegler-Natta Catalysis (Polymerization)
- **Discovery**: Karl Ziegler (1953) — TiCl₄/Al(C₂H₅)₃ for ethylene polymerization; Nobel Prize 1963.
- **Components**: Transition metal halide (TiCl₄, TiCl₃, VCl₃) + organoaluminum cocatalyst (AlR₃).
- **Stereospecificity**: Produces isotactic or syndiotactic polypropylene.
- **Modern versions**: Supported (MgCl₂/TiCl₄) for higher activity (>10⁶ g PP/g catalyst).
- **Metallocene catalysts**: ansa-metallocenes (e.g., rac-Et(Ind)₂ZrCl₂/MAO) — single-site, better control.

## [Source: Wikipedia, Catalytic Converter]
### Three-Way Catalytic Converter (TWC)
- Converts: CO → CO₂, NOₓ → N₂ + O₂, HC → CO₂ + H₂O simultaneously.
- **Components**: Pt, Pd, Rh on ceramic honeycomb (cordierite) or metallic substrate.
- Pt: Oxidation (CO, HC). Pd: Oxidation (CO, HC). Rh: NOₓ reduction.
- **Optimal operation**: Stoichiometric air-fuel ratio (λ = 1), monitored by O₂ sensor.
- **Poisoning**: Lead (historical), sulfur, phosphorus.
