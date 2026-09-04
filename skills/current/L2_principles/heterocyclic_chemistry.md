---
id: heterocyclic_chemistry
layer: 2
title: Heterocyclic Chemistry - Graduate Reference
stability: high
confidence: high
source: Graduate Organic Chemistry (Joule & Mills, Katritzky), Organic Synthesis
last_verified: 2026-03-31
---

# Heterocyclic Chemistry

## 1. Nomenclature and Classification

### 1.1 Hantzsch-Widman Nomenclature System

The IUPAC-approved system for naming heterocycles uses numerical prefixes for heteroatoms and suffixes for ring size and saturation.

**Heteroatom Prefixes (priority order):**
| Heteroatom | Prefix | Priority |
|------------|--------|----------|
| O | oxa- | 1 (highest) |
| S | thia- | 2 |
| Se | selena- | 3 |
| N | aza- | 4 |
| P | phospha- | 5 |
| Si | sila- | 6 |

**Ring Size Suffixes:**

| Ring Size | Unsaturated | Saturated |
|-----------|-------------|-----------|
| 3 | -irene | -irane |
| 4 | -ete | -etane |
| 5 | -ole | -olidine |
| 6 | -ine | -ane |
| 7 | -epine | -epane |
| 8 | -ocine | -ocane |

**Numbering Rules:**
1. Heteroatoms receive lowest numbers possible
2. Multiple heteroatoms numbered to minimize sum
3. Higher priority heteroatoms numbered first
4. H-atoms indicated by locants (e.g., 2H-pyran)

**Examples:**
- Aziridine: 3-membered saturated N-heterocycle
- Oxirane (epoxide): 3-membered saturated O-heterocycle  
- Thietane: 4-membered saturated S-heterocycle
- Tetrahydrofuran: 5-membered saturated O-heterocycle
- Piperidine: 6-membered saturated N-heterocycle

### 1.2 Classification by Aromaticity

#### 1.2.1 Aromatic Heterocycles (Hückel's Rule: 4n+2 π electrons)

**π-Electron Counting for Heterocycles:**

| Heterocycle | π-Electron Contribution | Total π e⁻ | Aromatic? |
|-------------|------------------------|------------|-----------|
| Pyrrole | N contributes 2 e⁻ (lone pair in ring) | 6 (4 C + 2 N) | Yes |
| Pyridine | N contributes 1 e⁻ (lone pair outside ring) | 6 (5 C + 1 N) | Yes |
| Furan | O contributes 2 e⁻ | 6 | Yes |
| Thiophene | S contributes 2 e⁻ | 6 | Yes |
| Oxazole | O and N contribute 2 e⁻ each | 6 | Yes |
| Imidazole | One N contributes 2 e⁻, one contributes 1 e⁻ | 6 | Yes |
| Pyrazine | Each N contributes 1 e⁻ | 6 | Yes |

**Hückel Molecular Orbital Energy Levels:**

For monocyclic systems, MO energies given by:
$$E_j = \alpha + 2\beta\cos\left(\frac{2j\pi}{n}\right)$$

Where:
- $n$ = number of atoms in ring
- $j$ = 0, ±1, ±2, ... up to n/2
- $\alpha$ = Coulomb integral
- $\beta$ = Resonance integral (negative)

**Frost Circle Method:** Inscribe polygon in circle; vertices at orbital energy levels.

### 1.3 Classification by Saturation

| Type | Examples | Characteristics |
|------|----------|-----------------|
| **Fully unsaturated** | Pyridine, pyrrole, thiophene | Planar, sp² hybridized, aromatic |
| **Partially saturated** | Dihydropyridine, tetrahydroquinoline | May have sp³ centers, reduced aromaticity |
| **Fully saturated** | Piperidine, morpholine, tetrahydrofuran | Non-aromatic, sp³ hybridized, 3D geometry |

### 1.4 Trivial Names (Common but Official)

| Trivial Name | Systematic Name | Structure |
|--------------|-----------------|-----------|
| Furan | Oxole | 5-membered O-heterocycle |
| Thiophene | Thiole | 5-membered S-heterocycle |
| Pyrrole | Azole | 5-membered NH-heterocycle |
| Pyridine | Azine | 6-membered N-heterocycle |
| Indole | 1H-Benzazole | Benzo[b]pyrrole |
| Quinoline | Benzo[b]azine | Benzo[b]pyridine |
| Isoquinoline | Benzo[c]azine | Benzo[c]pyridine |
| Purine | — | Imidazo[4,5-d]pyrimidine |

---

## 2. Five-Membered Aromatic Heterocycles

### 2.1 Pyrrole, Furan, Thiophene Series

#### 2.1.1 Electronic Structure and Aromaticity

**Molecular Orbital Picture:**

For C₄H₄X heterocycles, the heteroatom X contributes two electrons to the aromatic sextet through its lone pair in the p-orbital.

```
        Pyrrole resonance structures
        
    H       H       H       H
    |       |       |       |
    N       N⁺      N       N⁺
   / \     / \     / \     / \
  /   \   /   \   /   \   /   \
 ╱     ╲ ╱     ╲ ╱     ╲ ╱     ╲
●       ●       ●       ●
```

**Aromaticity Indices (NICS: Nucleus-Independent Chemical Shift):**

| Compound | NICS(0) [ppm] | NICS(1) [ppm] | Relative Aromaticity |
|----------|---------------|---------------|---------------------|
| Thiophene | −13.6 | −11.5 | Highest |
| Furan | −12.4 | −10.0 | Moderate |
| Pyrrole | −12.2 | −10.6 | Moderate |
| Benzene | −9.7 | −10.2 | Reference |

**HOMA (Harmonic Oscillator Model of Aromaticity):**
$$\text{HOMA} = 1 - \frac{\alpha}{n}\sum_{i=1}^{n}(R_i - R_{opt})^2$$

Where $\alpha$ = normalization constant, $R_i$ = bond length, $R_{opt}$ = optimal bond length.

| Compound | HOMA Value | Classification |
|----------|------------|----------------|
| Thiophene | 0.81 | Aromatic |
| Pyrrole | 0.79 | Aromatic |
| Furan | 0.56 | Moderately aromatic |

#### 2.1.2 Electrophilic Aromatic Substitution (EAS)

**Reactivity Order:** Pyrrole > Furan > Thiophene >> Benzene

**Reactivity Enhancement Factors:**
- Pyrrole: ~10¹³ times more reactive than benzene
- Furan: ~10¹¹ times more reactive than benzene
- Thiophene: ~10⁹ times more reactive than benzene

**Substitution Position Preference:**

For EAS on five-membered heterocycles:

**α-Position (C2, C5) preferred due to:**
1. More resonance structures in σ-complex
2. Lower activation energy
3. More delocalized positive charge

**Resonance Stabilization of σ-Complex (α-attack):**

```
Attack at α-position (C2):

Step 1: Electrophile E⁺ attacks C2
    H           H           H
    |           |           |
    N      →    N      →    N
   / \         /|\         / \
  /   \       / | \       /   \
 E    ●      E  ●  ●     E    ●

3 resonance structures possible
```

**Resonance Stabilization of σ-Complex (β-attack):**

```
Attack at β-position (C3):

Only 2 resonance structures possible → less stable
```

**EAS Reactions and Conditions:**

| Reaction | Pyrrole | Furan | Thiophene |
|----------|---------|-------|-----------|
| Nitration | HNO₃/Ac₂O, −10°C (mild) | HNO₃/Ac₂O | HNO₃/Ac₂O |
| Sulfonation | Pyridine·SO₃ complex | — | H₂SO₄, room temp |
| Halogenation | X₂, no catalyst | X₂, CHCl₃, 0°C | X₂, AcOH |
| Acylation | (RCO)₂O, Lewis acid | (RCO)₂O, SnCl₄ | (RCO)₂O, SnCl₄ |
| Vilsmeier | POCI₃/DMF | POCI₃/DMF | POCI₃/DMF |

**Regioselectivity in Disubstituted Systems:**

For 2-substituted five-membered heterocycles:

| Substituent | Further Substitution Position |
|-------------|------------------------------|
| Electron-donating (EDG) | C5 (other α) |
| Electron-withdrawing (EWG) | C4 (β) |
| Large groups (steric) | C4 (β) |

### 2.2 Synthesis of Five-Membered Heterocycles

#### 2.2.1 Paal-Knorr Synthesis

**General Reaction:** 1,4-Dicarbonyl compounds + heteroatom source → heterocycle

**Pyrrole Synthesis:**
$$\text{R-CO-CH}_2\text{-CH}_2\text{-CO-R'} + \text{NH}_3 \xrightarrow{\Delta} \text{R} \xrightarrow{\text{N}} \text{R'} + 2\text{H}_2\text{O}$$

**Mechanism:**
1. Nucleophilic attack of NH₃ on carbonyl
2. Proton transfer and elimination of water
3. Cyclization via second carbonyl attack
4. Dehydration to aromatic system

**Furan Synthesis:**
$$\text{R-CO-CH}_2\text{-CH}_2\text{-CO-R'} \xrightarrow{\text{H}^+} \text{R} \xrightarrow{\text{O}} \text{R'} + \text{H}_2\text{O}$$

Acid-catalyzed cyclodehydration.

**Thiophene Synthesis:**
$$\text{R-CO-CH}_2\text{-CH}_2\text{-CO-R'} + \text{P}_2\text{S}_5 \text{ or H}_2\text{S} \xrightarrow{\Delta} \text{R} \xrightarrow{\text{S}} \text{R'}$$

**Limitations:**
- Requires 1,4-dicarbonyl precursors (often difficult to access)
- Symmetrical products from symmetric dicarbonyls
- Limited substitution pattern control

#### 2.2.2 Hantzsch Synthesis (Thiazoles)

**General Reaction:** α-Haloketone + thioamide → thiazole

$$\text{R-CO-CH}_2\text{-X} + \text{R'-CS-NH}_2 \rightarrow \text{R} \xrightarrow{\text{N}} \text{R'} + \text{HX}$$

**Mechanism:**
1. S-alkylation of thioamide by α-haloketone
2. Intramolecular nucleophilic attack by amine on carbonyl
3. Proton transfers and dehydration
4. Aromatization to thiazole

**Scope:**
- R and R' can be varied widely
- X = Cl, Br, I (Br preferred)
- Gives 2,4-disubstituted thiazoles
- Amino thiazoles from thioureas

**Example: 2-Amino-4-methylthiazole**
$$\text{CH}_3\text{-CO-CH}_2\text{-Br} + \text{H}_2\text{N-CS-NH}_2 \rightarrow \text{H}_2\text{N} \xrightarrow{\text{S}} \text{CH}_3$$

#### 2.2.3 Van Leusen Synthesis (Oxazoles)

**Tosylmethyl Isocyanide (TosMIC) Reaction:**

$$\text{R-CHO} + \text{TosMIC} \xrightarrow{\text{K}_2\text{CO}_3} \text{R} \xrightarrow{\text{N}} \text{H}$$

**Mechanism:**
1. Base deprotonates TosMIC (pKa ≈ 9)
2. Anion adds to aldehyde
3. Cyclization through isocyanide
4. Elimination of toluenesulfinate
5. Tautomerization to oxazole

**Variations:**
- Aldehyde + TosMIC → 5-substituted oxazole
- Ketone + TosMIC → 4,5-disubstituted oxazole
- Imines + TosMIC → imidazoles

#### 2.2.4 Oxazole and Imidazole Synthesis

**Robinson-Gabriel Synthesis (Oxazoles):**
$$\text{R-CO-CH}_2\text{-NH-CO-R'} \xrightarrow{\text{P}_2\text{O}_5, \Delta} \text{R} \xrightarrow{\text{N}} \text{R'} + \text{H}_2\text{O}$$

2-Acylaminoketone cyclodehydration.

**Debus-Radziszewski Synthesis (Imidazoles):**
$$\text{R-CO-CH}_2\text{-R'} + \text{R''-CHO} + \text{NH}_3 \rightarrow \text{R} \xrightarrow{\text{N}} \text{R'} + \text{H}_2\text{O}$$

1,2-Dicarbonyl + aldehyde + ammonia → imidazole.

**Mechanism:**
1. Condensation of ammonia with dicarbonyl
2. Aldehyde addition
3. Cyclization
4. Oxidation/dehydrogenation

#### 2.2.5 Pyrazole Synthesis

**From 1,3-Dicarbonyls and Hydrazines:**
$$\text{R-CO-CH}_2\text{-CO-R'} + \text{H}_2\text{N-NH}_2 \rightarrow \text{R} \xrightarrow{\text{N}} \text{R'} + 2\text{H}_2\text{O}$$

**Regiochemistry:**
- Unsymmetrical 1,3-diketones give mixture of regioisomers
- Can be controlled by:
  - Stoichiometry
  - Substituent effects
  - Use of substituted hydrazines

**Knorr Pyrazole Synthesis (from α,β-unsaturated ketones):**
$$\text{R-CH=CH-CO-R'} + \text{H}_2\text{N-NH}_2 \rightarrow \text{R} \xrightarrow{\text{N}} \text{R'}$$

### 2.3 Reactivity Patterns in Five-Membered Heterocycles

#### 2.3.1 Electrophilic Substitution Mechanism

**General Mechanism:**
```
Step 1: Electrophilic attack
    X-H                          X-H
     |                            |
    ●--●    + E⁺  →  ●--●⁺--E
   /    \                       /    \
  ●      ●                     ●      ●

Step 2: Deprotonation
    X-H
     |
    ●--●--E     Base  →   Aromatic heterocycle-E
   /    \      ↓
  ●      ●              + H-Base⁺
```

**Hammett σ Values for Heterocyclic Positions:**

| Position | Pyrrole | Furan | Thiophene |
|----------|---------|-------|-----------|
| C2 (α) | σ⁺ = −0.55 | σ⁺ = −0.50 | σ⁺ = −0.45 |
| C3 (β) | σ⁺ = −0.30 | σ⁺ = −0.25 | σ⁺ = −0.20 |

More negative σ⁺ = more reactive to electrophiles.

#### 2.3.2 Nucleophilic Substitution (Rare)

Five-membered heterocycles are electron-rich; nucleophilic substitution requires:
- Strong electron-withdrawing groups
- Leaving groups at activated positions
- S_NAr mechanism via Meisenheimer complexes

**Example:** 2-Chloro-5-nitrothiophene with NaOMe → 2-methoxy-5-nitrothiophene

#### 2.3.3 Metalation and Functionalization

**Directed Ortho-Metalation (DoM):**

Five-membered heterocycles can be lithiated at α-positions:

$$\text{Pyrrole} + \text{n-BuLi} \xrightarrow{\text{THF}, -78°C} \text{2-Lithiopyrrole} \xrightarrow{\text{E}^+} \text{2-substituted pyrrole}$$

**N-Protection Required:** N-blocked pyrroles (N-Boc, N-TIPS) for clean lithiation.

**Common Metalation Conditions:**

| Substrate | Base | Position | Temperature |
|-----------|------|----------|-------------|
| N-Boc-pyrrole | n-BuLi | C2 | −78°C |
| Thiophene | n-BuLi | C2 | −78°C |
| Furan | n-BuLi | C2 | −78°C |
| N-Methylpyrrole | t-BuLi | C2 | −78°C |

**Transmetalation for Cross-Coupling:**
$$\text{2-Lithiothiophene} + \text{ZnCl}_2 \rightarrow \text{2-zinciothiophene} \xrightarrow{\text{Pd(0)}} \text{cross-coupled product}$$

#### 2.3.4 Cycloaddition Reactions

**Diels-Alder Reactions:**

Furan acts as diene:
$$\text{Furan} + \text{Maleic anhydride} \rightarrow \text{endo-adduct}$$

**Reversibility:** Aromatic furan adducts can retro-Diels-Alder at elevated temperatures.

**Pyrrole and Thiophene:** Poor dienes due to higher aromaticity (less reactive).

---

## 3. Six-Membered Aromatic Heterocycles

### 3.1 Pyridine and Diazines

#### 3.1.1 Electronic Structure

**Pyridine:**
- N contributes 1 electron to π-system
- Lone pair in sp² orbital perpendicular to π-system
- N is electron-withdrawing (−I, −M effects)
- π-electron deficient (unlike five-membered heterocycles)

**Molecular Orbital Energies (Pyridine):**

| Orbital | Energy | Character |
|---------|--------|-----------|
| LUMO | −0.5 β | π* (b₁) |
| HOMO | 0.5 β | π (a₂) |
| n(N) | 0.0 | Non-bonding (lone pair) |

**Basicity:**
$$\text{pK}_a(\text{pyridinium}) = 5.25$$

Lone pair availability makes pyridine basic and nucleophilic.

#### 3.1.2 Diazines (Six-Membered Rings with Two N Atoms)

| Compound | N Positions | pKₐ | Characteristics |
|----------|-------------|-----|-----------------|
| Pyridazine | 1,2 | 2.3 | Most basic diazine |
| Pyrimidine | 1,3 | 1.3 | Uracil, cytosine base |
| Pyrazine | 1,4 | 0.6 | Least basic diazine |

**Reactivity Pattern:**
- More N atoms = more electron-deficient
- Increased susceptibility to nucleophilic attack
- Decreased basicity (except pyridazine)

### 3.2 Synthesis of Six-Membered Heterocycles

#### 3.2.1 Hantzsch Dihydropyridine Synthesis

**Classic Reaction:**
$$2\text{R-CO-CH}_2\text{-COOR'} + \text{R''-CHO} + \text{NH}_3 \rightarrow \text{1,4-DHP} \xrightarrow{[\text{O}]} \text{Pyridine}$$

**Mechanism:**
1. Knoevenagel condensation of aldehyde with β-ketoester
2. Michael addition of second β-ketoester
3. Condensation with ammonia
4. Cyclization → 1,4-dihydropyridine (1,4-DHP)
5. Oxidation → pyridine

**Oxidants for DHP → Pyridine:**
- HNO₃
- KMnO₄
- DDQ
- Air/O₂ with catalyst

**Pharmacological Importance:**
1,4-DHPs are calcium channel blockers (nifedipine, amlodipine).

#### 3.2.2 Bohlmann-Rahtz Pyridine Synthesis

**Reaction:**
$$\text{Enamine} + \text{Ynone} \rightarrow \text{Dihydropyridine} \xrightarrow{\Delta} \text{Pyridine}$$

**Detailed Mechanism:**
1. Michael addition of enamine to ynone
2. Intramolecular aldol-type cyclization
3. Elimination of amine
4. Dehydration to pyridine

**Advantages:**
- Mild conditions
- Good functional group tolerance
- Access to highly substituted pyridines

**Typical Conditions:**
- Enamine: from ketone + secondary amine
- Ynone: from acyl chloride + terminal alkyne
- Heat (150-180°C) or acid catalyst for aromatization

#### 3.2.3 Chichibabin Pyridine Synthesis

**Classic Method:**
$$\text{Aldehyde} + \text{Ketone} + \text{NH}_3 \xrightarrow{\Delta} \text{Pyridine}$$

**Mechanism (Self-Condensation of Aldehydes):**
1. Aldol condensation between aldehydes
2. Michael addition
3. Ammonia incorporation
4. Cyclization and dehydration

**Scope:**
- Best for symmetric pyridines from single aldehyde
- Mixed aldehydes give mixtures
- Limited regiocontrol

**Modern Variations:**
- Transition metal catalyzed (Co, Rh, Ru)
- Solvent-free microwave conditions
- Flow chemistry approaches

#### 3.2.4 Kröhnke Pyridine Synthesis

**Pyridinium Salts to Pyridines:**
$$\text{Pyridinium salt} + \alpha,\beta\text{-unsaturated ketone} \xrightarrow{\text{base}} \text{substituted pyridine}$$

**Mechanism:**
1. Formation of Zincke salt (pyridinium)
2. Ring opening
3. Condensation with enone
4. Recyclization to new pyridine

#### 3.2.5 Diazine Synthesis

**Pyrimidine Synthesis (Pinner Method):**
$$\text{1,3-Dicarbonyl} + \text{Amidine} \rightarrow \text{Pyrimidine}$$

**Example: Uracil Synthesis**
$$\text{Malic acid} + \text{Urea} \xrightarrow{\text{H}_2\text{SO}_4} \text{Uracil}$$

**Pyrazine Synthesis:**
$$2\text{α-Aminoketone} \xrightarrow{\text{oxidation}} \text{Pyrazine}$$

Self-condensation with oxidation.

**Pyridazine Synthesis:**
$$\text{1,4-Diketone} + \text{Hydrazine} \rightarrow \text{Dihydropyridazine} \xrightarrow{[\text{O}]} \text{Pyridazine}$$

### 3.3 Reactivity of Six-Membered Heterocycles

#### 3.3.1 Nucleophilic Aromatic Substitution (S_NAr)

Pyridines and diazines are electron-deficient and undergo nucleophilic substitution readily.

**Chichibabin Reaction (Amination):**
$$\text{Pyridine} + \text{NaNH}_2 \xrightarrow{\text{liq NH}_3} \text{2-Aminopyridine}$$

**Mechanism:**
1. Nucleophilic attack at C2 (adjacent to N)
2. Formation of σ-complex (Meisenheimer complex)
3. Hydride elimination (H⁻)
4. Aromatization

**Why C2 (not C3)?**
- σ-Complex at C2 stabilized by adjacent N
- Negative charge on electronegative N

**General S_NAr with Leaving Groups:**
$$\text{2-Halopyridine} + \text{Nu}^- \rightarrow \text{2-Substituted pyridine} + \text{Hal}^-$$

**Reactivity Order for Halides:** F >> Cl > Br > I (contrary to aliphatic S_N2)

**Reason:** Rate-determining step is addition, not elimination; F⁻ best leaving group in Meisenheimer complex.

#### 3.3.2 N-Oxidation

**Formation of Pyridine N-Oxides:**
$$\text{Pyridine} + \text{H}_2\text{O}_2 \text{ or m-CPBA} \rightarrow \text{Pyridine N-oxide}$$

**Properties of N-Oxides:**
1. **Activation:** N-O activates ring for substitution at C2, C4
2. **Deactivation:** For electrophilic substitution
3. **Versatility:** Can be reduced back to pyridine

**Reactions of Pyridine N-Oxides:**

| Reaction | Conditions | Product |
|----------|------------|---------|
| Nitration | HNO₃/H₂SO₄ | 4-Nitropyridine N-oxide |
| Cyanation | Me₃SiCN, Ac₂O | 2-Cyanopyridine |
| Deoxygenation | PCl₃, Zn, or H₂/Pd | Pyridine |

**Boekelheide Reaction:**
$$\text{Pyridine N-oxide} \xrightarrow{\text{Ac}_2\text{O}} \text{2-Acetoxypyridine}$$

Rearrangement via [1,2]-shift of acetyl group.

#### 3.3.3 Electrophilic Aromatic Substitution (EAS)

Pyridines are deactivated toward EAS due to electron-withdrawing N.

**Typical Conditions:**
- Require harsh conditions
- Low yields
- Often give N-oxidation instead

**Examples:**

| Reaction | Conditions | Position | Yield |
|----------|------------|----------|-------|
| Sulfonation | H₂SO₄, 300°C | C3 | Low |
| Nitration | KNO₃/H₂SO₄, 300°C | C3 | ~5% |
| Bromination | Br₂, 300°C | C3 | Low |

**Strategy:** Use N-oxide or pyridinium salts to activate.

#### 3.3.4 Metalation and Cross-Coupling

**Directed Metalation:**

Substituents can direct lithiation:

| Substituent | Metalation Position |
|-------------|---------------------|
| OMe (C2) | C3 |
| OMe (C3) | C2, C4, C6 |
| CONR₂ | Ortho to substituent |
| OCONMe₂ | C3 (DOGS: Directed Ortho Metalation Group) |

**Ir-Catalyzed C-H Borylation:**
$$\text{Pyridine} + \text{B}_2\text{pin}_2 \xrightarrow{[\text{Ir}], \text{dtbpy}} \text{3-Borylpyridine}$$

**Palladium Cross-Coupling:**
- Suzuki: Pyridyl boronic acids + aryl halides
- Stille: Pyridyl stannanes + halides
- Negishi: Pyridyl zinc reagents + halides

**Buchwald-Hartwig Amination:**
$$\text{Halopyridine} + \text{R-NH}_2 \xrightarrow{\text{Pd, ligand}} \text{Aminopyridine}$$

---

## 4. Fused Heterocycles

### 4.1 Indole

#### 4.1.1 Structure and Properties

**Electronic Structure:**
- Benzene fused to pyrrole at [b] face
- 10 π-electrons (aromatic)
- Electron-rich (similar to pyrrole)
- C3 most reactive toward electrophiles

**NICS Values:**
- 5-membered ring: −10.3 ppm
- 6-membered ring: −9.8 ppm

#### 4.1.2 Fischer Indole Synthesis

**General Reaction:**
$$\text{Phenylhydrazine} + \text{Ketone/Aldehyde} \xrightarrow{\text{acid}} \text{Indole}$$

**Mechanism:**
1. Condensation: Phenylhydrazone formation
2. Protonation and [3,3]-sigmatropic rearrangement
3. Cyclization
4. Aromatization via NH₃ elimination

**Acid Catalysts:**
- ZnCl₂ (classic)
- Polyphosphoric acid (PPA)
- TsOH
- H₂SO₄
- BF₃·OEt₂

**Regiochemistry (Unsymmetrical Ketones):**

For R-CO-CH₂-R':

| R vs R' | Product |
|---------|---------|
| R = H (aldehyde) | No regiochemistry issue |
| R > R' (steric) | R ends up at C3 |
| R can enolize | More substituted product |

**Modified Fischer Indole Conditions:**

| Substrate | Conditions | Notes |
|-----------|------------|-------|
| Unsubstituted phenylhydrazine | HCl, EtOH, Δ | Simple indoles |
| Substituted phenylhydrazine | Same | 5-, 6-, 7-substituted indoles |
| Ketones with α-protons | Stronger acid (PPA) | Avoids enamine side products |

**Bischler Indole Synthesis:**
$$\text{α-Bromoacetophenone} + \text{Aniline} \xrightarrow{\text{acid}} \text{2-Arylindole}$$

Alternative for 2-substituted indoles.

#### 4.1.3 Electrophilic Substitution on Indole

**Position Preference:** C3 >> C2 > C5 > C6 > C7

**Resonance Structures (C3 Attack):**
```
C3 attack gives 4 resonance structures:

    H                       H
    N      E⁺              N
     \\     ↓               \\--E
      ●       →     ●--●⁺--●--●
     / \                 / \
    ●   ●               ●   ●
```

**Common Reactions:**

| Reaction | Conditions | Product |
|----------|------------|---------|
| Vilsmeier-Haack | POCI₃/DMF | 3-Formylindole |
| Mannich | R₂NH, HCHO | 3-Aminomethylindole |
| Friedel-Crafts | RCOCl, AlCl₃ | 3-Acylindole |
| Nitration | HNO₃/Ac₂O | 3-Nitroindole |

### 4.2 Quinoline and Isoquinoline

#### 4.2.1 Structure

**Quinoline:** Benzene fused to pyridine at [b] face
**Isoquinoline:** Benzene fused to pyridine at [c] face

**Electron Distribution:**
- Pyridine ring: electron-deficient
- Benzene ring: relatively electron-rich
- Different reactivity in each ring

#### 4.2.2 Quinoline Synthesis

**Skraup Synthesis:**
$$\text{Aniline} + \text{Glycerol} + \text{H}_2\text{SO}_4 \xrightarrow{\text{oxidant}} \text{Quinoline}$$

**Mechanism:**
1. Glycerol → acrolein (dehydration)
2. Michael addition of aniline to acrolein
3. Electrophilic cyclization
4. Oxidation to quinoline

**Oxidants:** Nitrobenzene, Fe₂O₃, As₂O₅, iodine

**Doebner-von Miller Synthesis:**
$$\text{Aniline} + \text{α,β-Unsaturated aldehyde} \rightarrow \text{Quinoline}$$

**Mechanism:**
1. Michael addition
2. Aldol condensation
3. Cyclization
4. Oxidation

**Conrad-Limpach Synthesis:**
$$\text{Aniline} + \text{β-Ketoester} \xrightarrow{\Delta} \text{4-Hydroxyquinoline}$$

Via anilide formation and cyclization.

**Friedländer Synthesis:**
$$\text{2-Aminobenzaldehyde} + \text{Ketone} \xrightarrow{\text{base}} \text{Quinoline}$$

**Scope:** Excellent for 2,3-disubstituted quinolines.

#### 4.2.3 Isoquinoline Synthesis

**Bischler-Napieralski Synthesis:**
$$\text{Phenethylamide} \xrightarrow{\text{P}_2\text{O}_5 \text{ or POCI}_3} \text{3,4-Dihydroisoquinoline} \xrightarrow{[\text{O}]} \text{Isoquinoline}$$

**Mechanism:**
1. Activation of amide by POCI₃
2. Electrophilic cyclization (Friedel-Crafts type)
3. Dehydration

**Dehydrogenation:** Pd/C, Δ; or S, Δ

**Pictet-Spengler Synthesis:**
$$\text{β-Phenethylamine} + \text{Aldehyde} \xrightarrow{\text{acid}} \text{Tetrahydroisoquinoline}$$

**Mechanism:**
1. Imine formation
2. Electrophilic cyclization
3. Proton loss

**Conditions:**
- Mild: pH 4-6, room temp
- Harsh: concentrated acid, Δ

**Biological Relevance:** Key step in alkaloid biosynthesis.

**Pomeranz-Fritsch Synthesis:**
$$\text{Benzaldehyde} + \text{Aminoacetal} \rightarrow \text{Isoquinoline}$$

### 4.3 Benzimidazole, Purine, and Others

#### 4.3.1 Benzimidazole

**Synthesis:**
$$\text{o-Phenylenediamine} + \text{Carboxylic acid derivative} \rightarrow \text{Benzimidazole}$$

**Conditions:**
- Carboxylic acid: HCl, Δ
- Orthoester: mild acid
- Aldehyde: oxidative conditions

**Example: Omeprazole core**
$$\text{4-Methoxy-o-phenylenediamine} + \text{2-Methoxyacetic acid} \xrightarrow{\text{HCl}} \text{Benzimidazole intermediate}$$

#### 4.3.2 Purine

**Structure:** Imidazole fused to pyrimidine

**Synthesis (Traube Synthesis):**
$$\text{4,5-Diaminopyrimidine} + \text{Formic acid} \rightarrow \text{Purine}$$

**Biological Purines:**
- Adenine: 6-aminopurine
- Guanine: 2-amino-6-oxopurine
- Xanthine: 2,6-dioxopurine
- Caffeine: 1,3,7-trimethylxanthine

#### 4.3.3 Benzofuran and Benzothiophene

**Benzofuran Synthesis:**
$$\text{o-Hydroxybenzaldehyde} + \text{α-Haloketone} \xrightarrow{\text{base}} \text{Benzofuran}$$

Via Perkin-type condensation.

**Benzothiophene Synthesis:**
$$\text{Thiophenol} + \text{α,β-Unsaturated carbonyl} \xrightarrow{\text{acid}} \text{Benzothiophene}$$

---

## 5. Saturated Heterocycles

### 5.1 Three-Membered Rings

#### 5.1.1 Aziridines

**Structure:** Strained, ~27 kcal/mol ring strain

**Synthesis:**
1. **From Alkenes:**
   $$\text{Alkene} + \text{PhI=NTs} \xrightarrow{\text{Cu or Rh}} \text{Aziridine}$$
   (Catalytic nitrene transfer)

2. **From Amino Alcohols:**
   $$\text{β-Aminoalcohol} \xrightarrow{\text{Mitsunobu or MsCl/base}} \text{Aziridine}$$

**Ring-Opening Reactions:**

| Nucleophile | Regiochemistry | Product |
|-------------|---------------|---------|
| N₃⁻ | Attack at less substituted C | 2-Azidoamine |
| Halide | Attack at less substituted C | 2-Haloamine |
| H₂O (acid) | Protonated aziridine opens at more substituted C | Amino alcohol |
| Amines | Attack at less substituted C | Diamine |

**Stereoelectronics:** Inversion at attacked carbon (S_N2-like).

**Applications:**
- Building blocks for amino sugars
- Anticancer agents (mitomycin)
- Chiral auxiliaries

#### 5.1.2 Oxiranes (Epoxides)

**Ring Strain:** ~28 kcal/mol

**Synthesis:**
1. **Epoxidation of Alkenes:**
   - m-CPBA (peracid)
   - H₂O₂/VO(acac)₂ (Sharpless)
   - NaOCl/Mn-salen (Jacobsen)

2. **Darzens Reaction:**
   $$\text{Aldehyde} + \text{α-Haloester} \xrightarrow{\text{base}} \text{Epoxide}$$

**Ring-Opening:**

| Conditions | Regiochemistry | Stereochemistry |
|------------|---------------|-----------------|
| Acidic | More substituted C attacked | Inversion |
| Basic | Less substituted C attacked | Inversion |
| Nucleophile (strong) | Less substituted C | Inversion |
| Reductive (LiAlH₄) | Less substituted C | Inversion with retention overall |

**Payne Rearrangement:**
$$\text{2,3-Epoxyalcohol} \xrightarrow{\text{base}} \text{1,2-Epoxyalcohol}$$

Epoxide migration under basic conditions.

### 5.2 Four-Membered Rings

#### 5.2.1 Azetidines

**Ring Strain:** ~26 kcal/mol

**Synthesis:**
1. **Cyclization:**
   $$\text{γ-Haloamine} \xrightarrow{\text{base}} \text{Azetidine}$$

2. **[2+2] Cycloaddition:**
   $$\text{Imine} + \text{Ketene} \rightarrow \text{β-Lactam (azetidin-2-one)}$$

**β-Lactam Antibiotics:**
- Penicillins
- Cephalosporins
- Carbapenems
- Monobactams

**Ring-Opening:**
- Less common than aziridines due to lower strain
- Nucleophilic attack at carbonyl (for β-lactams)
- Strain-driven reactivity

### 5.3 Five- and Six-Membered Saturated Heterocycles

#### 5.3.1 Tetrahydrofuran (THF)

**Synthesis:**
1. Hydrogenation of furan
2. Cyclization of 1,4-diols

**Ring-Opening:**
- Under strongly acidic conditions
- Via oxonium ion intermediate

$$\text{THF} \xrightarrow{\text{H}^+} \text{Oxonium ion} \xrightarrow{\text{Nu}^-} \text{4-Halo-1-butanol derivative}$$

#### 5.3.2 Piperidine

**Synthesis:**
1. Hydrogenation of pyridine
2. Intramolecular cyclization of δ-amino compounds

**Reactivity:**
- Secondary amine chemistry
- N-Alkylation, N-acylation
- Enamine formation (from N-alkylpiperidines via α-deprotonation)

**Important Natural Products:**
- Alkaloids: morphine, nicotine, cocaine, strychnine
- All contain piperidine or reduced piperidine ring

#### 5.3.3 Morpholine

**Structure:** 1,4-Oxazine (O and N)

**Synthesis:**
$$\text{Diethanolamine} \xrightarrow{\text{H}_2\text{SO}_4, \Delta} \text{Morpholine}$$

**Uses:**
- Solvent
- Building block for pharmaceuticals
- Corrosion inhibitor

---

## 6. Medicinal Chemistry Relevance

### 6.1 Common Heterocyclic Pharmacophores

#### 6.1.1 Five-Membered Rings

| Heterocycle | Drug Examples | Role |
|-------------|---------------|------|
| Pyrrole | Atorvastatin (Lipitor) | Lipid-lowering |
| Furan | Nitrofurantoin | Antibacterial |
| Thiophene | Clopidogrel (Plavix) | Antithrombotic |
| Imidazole | Ketoconazole | Antifungal |
| Pyrazole | Celecoxib | Anti-inflammatory |
| Oxazole | Oxacillin | Antibiotic |
| Thiazole | Sulfathiazole | Antibacterial |

#### 6.1.2 Six-Membered Rings

| Heterocycle | Drug Examples | Role |
|-------------|---------------|------|
| Pyridine | Isoniazid, Nicotine | Antitubercular, CNS |
| Pyrimidine | Fluorouracil, Barbiturates | Anticancer, sedative |
| Piperidine | Morphine, Risperidone | Analgesic, antipsychotic |
| Morpholine | Linezolid | Antibiotic |

#### 6.1.3 Fused Systems

| Heterocycle | Drug Examples | Role |
|-------------|---------------|------|
| Indole | Sumatriptan, Indomethacin | Migraine, anti-inflammatory |
| Quinoline | Chloroquine, Quinine | Antimalarial |
| Isoquinoline | Papaverine | Vasodilator |
| Benzimidazole | Omeprazole, Albendazole | Proton pump inhibitor, antihelminthic |
| Purine | Acyclovir, Mercaptopurine | Antiviral, anticancer |
| Benzodiazepine | Diazepam, Alprazolam | Anxiolytic |

### 6.2 Structure-Activity Relationship (SAR) Considerations

#### 6.2.1 Physicochemical Properties

**Lipophilicity (Log P):**

| Heterocycle | π-Value (Hansch) | Effect on Log P |
|-------------|------------------|-----------------|
| Pyrrole | 0.95 | Increases |
| Furan | 1.02 | Increases |
| Thiophene | 1.61 | Increases more |
| Pyridine | 0.48 | Increases slightly |
| Pyrimidine | −0.10 | Decreases slightly |
| Piperidine | 0.73 | Increases |

**pKₐ and Ionization:**

| Heterocycle | pKₐ (conjugate acid) | State at pH 7.4 |
|-------------|---------------------|-----------------|
| Pyridine | 5.25 | Mostly neutral |
| Imidazole | 7.05 | ~50% protonated |
| Piperidine | 11.22 | Mostly protonated |
| Morpholine | 8.33 | Mostly protonated |

**Implications:**
- Ionized species have different distribution
- Blood-brain barrier penetration requires neutral form
- pKₐ affects oral absorption

#### 6.2.2 Hydrogen Bonding

**H-Bond Donors (HBD) and Acceptors (HBA):**

| Heterocycle | HBD | HBA | Notes |
|-------------|-----|-----|-------|
| Pyrrole | 1 (N-H) | 0 (π-system only) | Can donate |
| Pyridine | 0 | 1 (N lone pair) | Good acceptor |
| Imidazole | 1 | 2 | Both donor and acceptor |
| Piperidine | 1 (N-H) | 1 | Both |
| Morpholine | 0 | 2 (O and N) | Strong acceptor |

**Lipinski's Rule of Five:**
- HBD ≤ 5
- HBA ≤ 10
- MW < 500
- Log P < 5

Heterocycles help fine-tune these parameters.

#### 6.2.3 Metabolic Considerations

**Metabolic Soft Spots:**

| Heterocycle | Metabolic Site | Transformation |
|-------------|----------------|----------------|
| Pyridine | N-oxidation | Pyridine N-oxide |
| Thiophene | S-oxidation | Thiophene S-oxide |
| Furan | Ring opening | Dicarboxylic acid |
| Imidazole | C-H oxidation | Hydroxylimidazole |
| Piperidine | N-dealkylation | Amine + aldehyde |

**Design Strategies:**
- Fluorination to block oxidation
- Methyl to tert-butyl substitution
- Replace labile heterocycles with stable isosteres

#### 6.2.4 Bioisosterism

**Common Heterocyclic Replacements:**

| Original | Bioisostere | Reason |
|----------|-------------|--------|
| Benzene | Thiophene | Similar size, different electronics |
| Phenyl | Pyridine | N provides H-bond acceptance |
| Carboxylic acid | Tetrazole | Similar pKₐ, more lipophilic |
| Amide | Oxazole | H-bond mimic, metabolic stability |
| Ester | Oxadiazole | Stability, reduced hydrolysis |

---

## 7. Worked Examples

### Example 1: Paal-Knorr Pyrrole Synthesis

**Problem:** Synthesize 2,5-dimethylpyrrole from accessible starting materials.

**Solution:**

**Step 1: Prepare 2,5-hexanedione**
$$\text{CH}_3\text{-CO-CH}_3 \xrightarrow{\text{I}_2, \text{KOH}} \text{CH}_3\text{-CO-CH}_2\text{-CH}_2\text{-CO-CH}_3$$

Mechanism: Iodoform reaction on acetone followed by coupling.

**Step 2: Paal-Knorr cyclization**
$$\text{CH}_3\text{-CO-CH}_2\text{-CH}_2\text{-CO-CH}_3 + \text{NH}_3 \xrightarrow{\Delta} \text{2,5-Dimethylpyrrole} + 2\text{H}_2\text{O}$$

**Mechanism Detail:**
1. NH₃ attacks carbonyl → hemiaminal
2. Proton transfer, elimination of H₂O
3. Second carbonyl attack, cyclization
4. Dehydration, aromatization

**Yield:** 70-85%

---

### Example 2: Fischer Indole Synthesis

**Problem:** Synthesize indole-3-carboxaldehyde.

**Solution:**

**Step 1: Fischer indole synthesis**
$$\text{Phenylhydrazine} + \text{Glyoxal} \rightarrow \text{Indole}$$

Glyoxal provides no substituents → unsubstituted indole.

**Better route: Vilsmeier-Haack**

**Step 1:** Fischer synthesis of indole from phenylhydrazine + acetaldehyde
**Step 2:** Vilsmeier-Haack formylation

$$\text{Indole} + \text{DMF/POCI}_3 \rightarrow \text{Indole-3-carboxaldehyde}$$

**Mechanism:**
1. POCI₃ activates DMF → iminium electrophile
2. Electrophilic attack at C3 of indole
3. Hydrolysis of iminium

**Yield:** 60-75% for Vilsmeier step

---

### Example 3: Chichibabin Amination

**Problem:** Convert pyridine to 2-aminopyridine.

**Solution:**

$$\text{Pyridine} + \text{NaNH}_2 \xrightarrow{\text{liq NH}_3, 100°C} \text{2-Aminopyridine} + \text{H}_2$$

**Mechanism:**
1. Nucleophilic attack of NH₂⁻ at C2
2. Formation of σ-complex (anionic)
3. Elimination of H⁻
4. H⁻ + NH₃ → H₂ + NH₂⁻ (chain propagation)

**Key Points:**
- C2 attack preferred over C4 (better charge delocalization in intermediate)
- Liquid ammonia as solvent (low temperature for control)
- No oxidant needed; H⁻ eliminated directly

**Yield:** 70-80%

---

### Example 4: Bischler-Napieralski Isoquinoline Synthesis

**Problem:** Synthesize 6,7-dimethoxyisoquinoline.

**Solution:**

**Step 1: Prepare starting material**
$$\text{3,4-Dimethoxyphenethylamine} + \text{Acetyl chloride} \rightarrow \text{N-Acetyl derivative}$$

**Step 2: Cyclization**
$$\text{N-Acetyl-3,4-dimethoxyphenethylamine} \xrightarrow{\text{POCI}_3, \Delta} \text{6,7-Dimethoxy-3,4-dihydroisoquinoline}$$

**Step 3: Dehydrogenation**
$$\text{Dihydroisoquinoline} \xrightarrow{\text{Pd/C, Δ or S, Δ}} \text{6,7-Dimethoxyisoquinoline}$$

**Mechanism:**
1. POCI₃ activates amide (forms imidoyl chloride)
2. Electrophilic aromatic substitution (Friedel-Crafts type)
3. Cyclization at activated position (para to OMe)
4. Elimination of HCl

**Yield:** 60-70% overall

---

### Example 5: Hantzsch Dihydropyridine Synthesis

**Problem:** Synthesize nifedipine (calcium channel blocker).

**Solution:**

**Structure:** 1,4-DHP with:
- 2,6-Dimethyl-3,5-dicarboxylate groups
- 4-(2-Nitrophenyl) substituent

**Synthesis:**
$$2\text{Methyl acetoacetate} + \text{2-Nitrobenzaldehyde} + \text{NH}_3 \rightarrow \text{Nifedipine precursor}$$

**Conditions:**
- Ethanol/ammonia solution
- Room temperature or mild heating
- Followed by oxidation (HNO₃) for pyridine analog, or use as-is for DHP drug

**Key Features:**
- Symmetrical from 2 equivalents β-ketoester
- Aldehyde determines C4 substituent
- NH₃ provides N1

**Yield:** 50-65%

---

### Example 6: Van Leusen Oxazole Synthesis

**Problem:** Synthesize 5-phenyloxazole.

**Solution:**

$$\text{Benzaldehyde} + \text{TosMIC} \xrightarrow{\text{K}_2\text{CO}_3, \text{MeOH}} \text{5-Phenyloxazole}$$

**Mechanism:**
1. Base deprotonates TosMIC α-carbon
2. Anion adds to aldehyde carbonyl
3. Intramolecular addition to isocyanide
4. Ring closure
5. Elimination of Ts⁻ (excellent leaving group)

**Advantages:**
- Mild conditions
- No transition metals
- Good functional group tolerance
- TosMIC readily available

**Yield:** 60-80%

---

### Example 7: Pyridine N-Oxide Activation

**Problem:** Synthesize 2-cyanopyridine from pyridine.

**Solution:**

**Step 1: N-Oxidation**
$$\text{Pyridine} + \text{m-CPBA} \rightarrow \text{Pyridine N-oxide}$$

**Step 2: Cyanation (Reissert-Henze reaction)**
$$\text{Pyridine N-oxide} + \text{Me}_3\text{SiCN} + \text{Ac}_2\text{O} \rightarrow \text{2-Cyanopyridine}$$

**Mechanism:**
1. Acetylation of N-oxide
2. Nucleophilic attack by CN⁻ at C2
3. Elimination of acetate
4. Deoxygenation

**Alternative:** Direct Chichibabin with KCN (harsher)

**Yield:** 50-70%

---

### Example 8: Thiophene Synthesis and Functionalization

**Problem:** Synthesize 2-acetylthiophene.

**Solution:**

**Route A: Paal-Knorr from 1,4-dicarbonyl**
$$\text{CH}_3\text{-CO-CH}_2\text{-CH}_2\text{-CO-CH}_3 + \text{P}_2\text{S}_5 \rightarrow \text{2,5-Dimethylthiophene}$$

Not suitable for 2-acetyl product.

**Route B: Vilsmeier-Haack on thiophene**
$$\text{Thiophene} + \text{DMF/POCI}_3 \rightarrow \text{2-Formylthiophene} \xrightarrow{\text{MeMgBr, then oxidation}} \text{2-Acetylthiophene}$$

**Route C: Friedel-Crafts (modified)**
$$\text{Thiophene} + \text{Ac}_2\text{O} \xrightarrow{\text{SnCl}_4} \text{2-Acetylthiophene}$$

**Yield:** Route C: 65-75%

---

### Example 9: Imidazole Synthesis

**Problem:** Synthesize 4,5-diphenylimidazole.

**Solution:**

**Debus-Radziszewski Synthesis:**
$$\text{Benzil (Ph-CO-CO-Ph)} + \text{Benzaldehyde} + \text{NH}_3 \rightarrow \text{2,4,5-Triphenylimidazole}$$

This gives wrong product (3 phenyls).

**Correct route: From 1,2-diketone**
$$\text{Benzil} + \text{HCHO} + \text{NH}_3 \xrightarrow{\text{NH}_4\text{OAc}} \text{4,5-Diphenylimidazole}$$

**Mechanism:**
1. Condensation of ammonia with benzil → diimine intermediate
2. Formaldehyde addition
3. Cyclization
4. Aromatization

**Yield:** 60-75%

---

### Example 10: Pictet-Spengler Reaction

**Problem:** Synthesize tetrahydropapaverine.

**Solution:**

**Starting materials:**
- 3,4-Dimethoxyphenethylamine
- 3,4-Dimethoxybenzaldehyde (veratraldehyde)

**Reaction:**
$$\text{Dopamine derivative} + \text{Veratraldehyde} \xrightarrow{\text{HCl, 0°C}} \text{Tetrahydropapaverine}$$

**Mechanism:**
1. Imine formation
2. Electrophilic cyclization (Friedel-Crafts type)
3. Aromatic proton loss

**Conditions:**
- Mild acid (pH 4-6)
- Can use Lewis acids (BF₃·OEt₂)

**Yield:** 70-85%

---

### Example 11: Aziridine Synthesis and Ring-Opening

**Problem:** Synthesize trans-2-aminocyclohexanol from cyclohexene.

**Solution:**

**Step 1: Epoxidation**
$$\text{Cyclohexene} + \text{m-CPBA} \rightarrow \text{Cyclohexene oxide}$$

**Step 2: Ring-opening with azide**
$$\text{Epoxide} + \text{NaN}_3 \xrightarrow{\text{NH}_4\text{Cl}} \text{trans-2-Azidocyclohexanol}$$

**Step 3: Reduction**
$$\text{Azide} \xrightarrow{\text{LiAlH}_4 \text{ or H}_2/\text{Pd}} \text{trans-2-Aminocyclohexanol}$$

**Stereochemistry:**
- Epoxidation: syn addition
- Ring-opening: S_N2 at less substituted C, inversion
- Overall: trans product

**Yield:** 60-75% overall

---

### Example 12: Pyrimidine Synthesis

**Problem:** Synthesize 2-amino-4,6-dihydroxypyrimidine (isocytosine).

**Solution:**

$$\text{Malonic acid} + \text{Guanidine} \xrightarrow{\text{NaOEt}} \text{Isocytosine}$$

**Mechanism:**
1. Condensation of guanidine with both carbonyls
2. Cyclization
3. Aromatization with loss of water

**Alternative from urea:**
$$\text{Malonic acid} + \text{Urea} \rightarrow \text{Barbituric acid}$$

**Yield:** 70-85%

---

### Example 13: Benzimidazole Drug Synthesis (Omeprazole Core)

**Problem:** Synthesize 5-methoxy-2-[(4-methoxy-3,5-dimethyl-2-pyridinyl)methylsulfinyl]-1H-benzimidazole (omeprazole).

**Solution:**

**Step 1: Benzimidazole formation**
$$\text{4-Methoxy-o-phenylenediamine} + \text{2-Methoxyacetic acid} \xrightarrow{\text{HCl}} \text{2-Methoxymethyl-5-methoxybenzimidazole}$$

**Step 2: Sulfide formation**
$$\text{Benzimidazole} + \text{2-Chloromethyl-3,5-dimethyl-4-methoxypyridine} \xrightarrow{\text{base}} \text{Sulfide intermediate}$$

**Step 3: Oxidation**
$$\text{Sulfide} \xrightarrow{\text{m-CPBA}} \text{Sulfoxide (omeprazole)}$$

**Yield:** 40-55% overall

---

### Example 14: Quinoline Synthesis (Skraup)

**Problem:** Synthesize 6-methoxyquinoline.

**Solution:**

**Starting materials:**
- 3-Methoxyaniline
- Glycerol
- Sulfuric acid
- Nitrobenzene (oxidant)

**Reaction:**
$$\text{3-Methoxyaniline} + \text{Glycerol} \xrightarrow{\text{H}_2\text{SO}_4, \text{PhNO}_2} \text{6-Methoxyquinoline}$$

**Mechanism:**
1. Glycerol → acrolein (dehydration)
2. Michael addition
3. Electrophilic cyclization
4. Oxidation by nitrobenzene

**Yield:** 45-60%

---

### Example 15: Purine Nucleoside Synthesis

**Problem:** Outline the synthesis of acyclovir (antiviral).

**Solution:**

**Strategy:** Vorbrüggen glycosylation

**Step 1: Prepare silylated base**
$$\text{Guanine} + \text{HMDS} \xrightarrow{(\text{NH}_4)_2\text{SO}_4} \text{Silylated guanine}$$

**Step 2: Glycosylation**
$$\text{Silylated guanine} + \text{Acyclovir sugar precursor} \xrightarrow{\text{TMSOTf, MeCN}} \text{Acyclovir}$$

**Sugar precursor:** 2-[(2-acetoxyethoxy)methyl]-1,3-diacetoxypropane derivative

**Mechanism:**
1. Activation of anomeric position by TMSOTf
2. N9 attack of guanine
3. Deprotection

**Yield:** 35-50% (final step)

---

## Summary Tables

### Key Heterocycle Properties

| Heterocycle | pKₐ (BH⁺) | Aromaticity (NICS) | Dominant Reactivity |
|-------------|-----------|-------------------|---------------------|
| Pyrrole | −0.3 (N-H) | −12.2 | EAS (α) |
| Furan | — | −12.4 | EAS (α), D-A |
| Thiophene | — | −13.6 | EAS (α) |
| Imidazole | 7.05 | −11.8 | EAS (C4, C5) |
| Pyridine | 5.25 | −9.7 | S_NAr, N-alkylation |
| Pyrimidine | 1.3 | — | S_NAr |
| Indole | −2.4 (N-H) | −10.3 | EAS (C3) |
| Quinoline | 4.85 | — | S_NAr (pyridine ring) |

### Named Reaction Summary

| Reaction | Substrate | Product | Key Feature |
|----------|-----------|---------|-------------|
| Paal-Knorr | 1,4-Dicarbonyl + NH₃ | Pyrrole | General for 5-membered |
| Hantzsch (thiazole) | α-Haloketone + thioamide | Thiazole | 2,4-Disubstituted |
| Van Leusen | Aldehyde + TosMIC | Oxazole | Mild conditions |
| Fischer | Phenylhydrazone | Indole | Most versatile |
| Skraup | Aniline + glycerol | Quinoline | Classical |
| Bischler-Napieralski | Phenethylamide | Isoquinoline | Via dihydroisoquinoline |
| Pictet-Spengler | Phenethylamine + aldehyde | Tetrahydroisoquinoline | Alkaloid synthesis |
| Hantzsch (DHP) | 2 β-Ketoester + aldehyde + NH₃ | 1,4-DHP | Ca²⁺ channel blockers |
| Chichibabin | Pyridine + NaNH₂ | 2-Aminopyridine | S_NAr |
| Bohlmann-Rahtz | Enamine + ynone | Pyridine | Highly substituted |

---

## References

1. Joule, J. A.; Mills, K. *Heterocyclic Chemistry*, 5th ed.; Wiley-Blackwell: Chichester, 2010.
2. Katritzky, A. R.; Ramsden, C. A.; Scriven, E. F. V.; Taylor, R. J. K. *Comprehensive Heterocyclic Chemistry III*; Elsevier: Oxford, 2008.
3. Carey, J. S.; Laffan, D.; Thomson, C.; Williams, M. T. Analysis of the reactions used for the preparation of drug candidate molecules. *Org. Biomol. Chem.* **2006**, *4*, 2337–2347.
4. Vitaku, E.; Smith, D. T.; Njardarson, J. T. Analysis of the structural diversity, substitution patterns, and frequency of nitrogen heterocycles among U.S. FDA approved pharmaceuticals. *J. Med. Chem.* **2014**, *57*, 10257–10274.
5. Taylor, R. D.; MacCoss, M.; Lawson, A. D. Rings in drugs. *J. Med. Chem.* **2014**, *57*, 5845–5859.
