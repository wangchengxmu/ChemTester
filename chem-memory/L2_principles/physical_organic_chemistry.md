---
id: physical_organic_chemistry
layer: 2
title: Physical Organic Chemistry
scope: Graduate-level reference on structure-reactivity relationships, LFER, mechanisms, KIEs, and computational methods
stability: high
confidence: high
last_verified: 2026-03-31
cross_refs:
  - pericyclic_reactions.md
  - reaction_mechanisms.md
  - density_functional_theory.md
  - stereochemistry_chirality.md
---

# Physical Organic Chemistry

## 1. Structure-Reactivity Relationships

### 1.1 Hammett Equation

The Hammett equation establishes a linear free-energy relationship (LFER) for para- and meta-substituted benzene derivatives:

$$\log \frac{k}{k_0} = \rho \sigma$$

or equivalently:

$$\log \frac{K}{K_0} = \rho \sigma$$

**Key Parameters:**

| Parameter | Definition | Physical Meaning |
|-----------|------------|------------------|
| σ | Substituent constant | Electronic effect of substituent (intrinsic property) |
| ρ | Reaction constant | Sensitivity of reaction to electronic effects |
| k₀ | Rate constant for unsubstituted | Reference (H substituent) |
| k | Rate constant for substituted | Measured rate |

**Hammett σ Constants (Selected Values):**

| Substituent | σₘ | σₚ | Classification |
|-------------|------|------|----------------|
| NMe₂ | −0.10 | −0.83 | Strong EDG (+R > −I) |
| NH₂ | −0.16 | −0.66 | Strong EDG |
| OH | +0.12 | −0.37 | EDG (+R > −I) |
| OMe | +0.12 | −0.27 | EDG (+R > −I) |
| Me | −0.07 | −0.17 | Weak EDG (+I, +H) |
| H | 0.00 | 0.00 | Reference |
| F | +0.34 | +0.06 | EWG (−I > +R) |
| Cl | +0.37 | +0.23 | EWG (−I > +R) |
| CF₃ | +0.43 | +0.54 | Strong EWG (−I only) |
| CN | +0.56 | +0.66 | Strong EWG |
| NO₂ | +0.71 | +0.78 | Very strong EWG (+R, −I) |
| NMe₃⁺ | +0.88 | +0.82 | Strongest EWG |

**Interpretation of ρ:**

- **ρ > 0**: Reaction favored by EWGs; positive charge develops at reaction center (nucleophilic attack, deprotonation)
- **ρ < 0**: Reaction favored by EDGs; negative charge develops at reaction center (electrophilic attack, protonation)
- **ρ ≈ 0**: Little charge development; reaction insensitive to electronic effects (radical reactions, steric control)
- **\|ρ\| magnitude**: Larger values indicate greater charge development at the transition state

**Typical ρ Values:**

| Reaction | ρ | Interpretation |
|----------|---|----------------|
| Phenol ionization | +2.23 | Large positive charge on O |
| Benzoic acid ionization | +1.00 | Definition (reference) |
| Saponification of ethyl benzoates | +2.23 | Anionic TS with negative charge |
| Ester hydrolysis (basic) | +2.0 to +2.5 | Anionic tetrahedral intermediate |
| Electrophilic aromatic substitution | −0.5 to −1.5 | Positive charge in TS |
| SN1 solvolysis of ArCH₂Cl | −4.5 to −2.0 | Full carbocation in TS |

### 1.2 Taft Equation

For aliphatic systems and ortho-substituted aromatics, the Taft equation separates inductive and steric effects:

$$\log \frac{k}{k_0} = \rho^* \sigma^* + \delta E_s$$

**Taft Parameters:**

| Parameter | Definition |
|-----------|------------|
| σ* | Polar (inductive) substituent constant |
| Eₛ | Steric substituent constant |
| ρ* | Polar sensitivity |
| δ | Steric sensitivity |

**Taft σ* Constants (Selected):**

| Substituent | σ* | Eₛ |
|-------------|------|------|
| H | 0.00 | 0.00 |
| Me | 0.00 | −0.07 |
| Et | −0.10 | −0.36 |
| i-Pr | −0.19 | −0.93 |
| t-Bu | −0.30 | −1.54 |
| CH₂Ph | +0.215 | −0.69 |
| CH₂Cl | +0.17 | −0.24 |
| CHCl₂ | +1.92 | −1.54 |
| CCl₃ | +2.65 | −2.06 |

**Derivation:** σ* from acid hydrolysis rates (insensitive to steric effects in tetrahedral intermediate):
$$\sigma^* = \frac{1}{2.48}\left[\log\left(\frac{k}{k_0}\right)_{\text{base}} - \log\left(\frac{k}{k_0}\right)_{\text{acid}}\right]$$

### 1.3 Swain-Lupton Parameters

Swain and Lupton proposed that all substituent effects can be described by two orthogonal components: field (F) and resonance (R):

$$\sigma = fF + rR$$

**Swain-Lupton Constants (Selected):**

| Substituent | F | R |
|-------------|------|------|
| NMe₂ | 0.06 | −0.52 |
| OMe | 0.26 | −0.42 |
| OH | 0.29 | −0.43 |
| Me | −0.04 | −0.08 |
| H | 0.00 | 0.00 |
| F | 0.43 | −0.35 |
| Cl | 0.41 | −0.17 |
| CF₃ | 0.38 | 0.19 |
| CN | 0.51 | 0.14 |
| NO₂ | 0.65 | 0.11 |

**Dual-Parameter Hammett:**
$$\log \frac{k}{k_0} = \rho_F F + \rho_R R$$

### 1.4 Yukawa-Tsuno Equation

For reactions with enhanced resonance demands (e.g., carbocation formation):

$$\log \frac{k}{k_0} = \rho \left[\sigma + r(\sigma^+ - \sigma)\right]$$

**Where:**
- r = resonance demand parameter (0 ≤ r ≤ 1)
- σ⁺ = special substituent constant for reactions with direct resonance with developing positive charge
- When r = 0: reverts to Hammett equation
- When r = 1: full resonance enhancement (σ⁺ applies)

**σ⁺ Values (Selected):**

| Substituent | σₚ⁺ |
|-------------|-------|
| NMe₂ | −1.7 |
| NH₂ | −1.3 |
| OMe | −0.78 |
| OH | −0.92 |
| Me | −0.31 |
| H | 0.00 |
| Cl | +0.11 |
| CF₃ | +0.61 |
| CN | +0.66 |
| NO₂ | +0.79 |

**Typical r Values:**

| Reaction | r | Interpretation |
|----------|---|----------------|
| SN1 solvolysis of cumyl chlorides | 1.00 | Full carbocation |
| Solvolysis of benzyl tosylates | 0.74 | Significant cation character |
| Electrophilic aromatic substitution | 0.4–0.6 | Partial positive charge |
| Phenol ionization | 0.0 | No enhanced resonance |

---

## 2. Linear Free Energy Relationships (LFER)

### 2.1 General Principles

LFERs express the linear relationship between changes in free energy (logarithms of equilibrium or rate constants) and structural changes:

$$\Delta \Delta G^\ddagger = \Delta G^\ddagger - \Delta G_0^\ddagger = -RT \ln \frac{k}{k_0}$$

**Marcus Theory Foundation:**
$$\Delta G^\ddagger = \frac{\lambda}{4}\left(1 + \frac{\Delta G^\circ}{\lambda}\right)^2$$

where λ is the reorganization energy.

### 2.2 Brønsted Catalysis Law

Relates the catalytic activity of acids/bases to their strength:

**For general acid catalysis:**
$$\log k_{HA} = \alpha \log K_a + C = -\alpha pK_a + C$$

**For general base catalysis:**
$$\log k_B = \beta \log K_b + C = \beta pK_a + C$$

**Brønsted α and β Values:**

| Parameter | Range | Interpretation |
|-----------|-------|----------------|
| α ≈ 0 | 0–0.2 | Little proton transfer in TS |
| α ≈ 0.5 | 0.3–0.7 | Late/early TS, significant proton transfer |
| α ≈ 1 | 0.8–1.0 | Nearly complete proton transfer |

**Hammond Postulate Implication:**
- α, β close to 0: TS resembles reactants (early TS)
- α, β close to 1: TS resembles products (late TS)
- α, β close to 0.5: TS midway along reaction coordinate

**Marcus Theory Interpretation:**
$$\alpha = \frac{1}{2}\left(1 + \frac{\Delta G^\circ}{\lambda}\right)$$

### 2.3 Bell-Evans-Polanyi Principle

For series of similar reactions, activation energy correlates with reaction enthalpy:

$$E_a = E_0 + \alpha \Delta H$$

**Marcus Theory Extension:**
For electron transfer and proton transfer:
$$\Delta G^\ddagger = w^r + \frac{\lambda}{4}\left(1 + \frac{\Delta G^\circ + w^p - w^r}{\lambda}\right)^2$$

where w^r and w^p are work terms for reactant approach and product separation.

### 2.4 Exner's Rules for LFER Validation

1. **Linearity**: Plot must be linear (no curvature)
2. **Same mechanism**: All points must represent same mechanism
3. **Isokinetic relationship**: ΔH‡ vs ΔS‡ should be linear if LFER valid
4. **Range**: Must span sufficient range of substituents

**Isokinetic Temperature:**
$$\beta = \frac{\Delta H^\ddagger}{\Delta S^\ddagger}$$

If β falls within experimental temperature range, the LFER may be spurious.

---

## 3. Reaction Mechanisms

### 3.1 Nucleophilic Substitution: SN2

**Bimolecular Nucleophilic Substitution**

$$\text{Nu}^- + \text{R-LG} \xrightarrow{k_2} \text{R-Nu} + \text{LG}^-$$

**Kinetics:** Rate = k₂[Nu⁻][R-LG] (second-order)

**Stereochemistry:** Inversion (Walden inversion) at chiral center

**TS Geometry:** Pentacoordinate, approximately trigonal bipyramidal

**Key Features:**

| Factor | Effect | Trend |
|--------|--------|-------|
| Nucleophilicity | Stronger Nu → faster | HSAB: softer Nu for C |
| Leaving group | Better LG → faster | I⁻ > Br⁻ > Cl⁻ >> F⁻ |
| Substrate | Less hindered → faster | Me > 1° > 2° >> 3° |
| Solvent | Polar aprotic faster | DMSO > DMF > acetone > MeOH |
| Sterics | Dominant factor | 3° effectively no SN2 |

**Nucleophilicity Trends:**
- In polar aprotic solvents: F⁻ > Cl⁻ > Br⁻ > I⁻ (basicity order)
- In protic solvents: I⁻ > Br⁻ > Cl⁻ > F⁻ (solvation effect)
- Soft nucleophiles: RS⁻ > I⁻ > CN⁻ > SCN⁻ > Br⁻
- Hard nucleophiles: F⁻ > OH⁻ > H₂O > NH₃

### 3.2 SN2' Reaction

**Allylic substitution with rearrangement:**

$$\text{Nu}^- + \text{CH}_2=\text{CH-CH}_2\text{-LG} \rightarrow \text{CH}_2(\text{Nu})-\text{CH}=\text{CH}_2$$

**Two modes:**
- **Syn addition**: Nucleophile attacks same face as leaving group
- **Anti addition**: Nucleophile attacks opposite face (generally preferred)

**Regiochemistry:**
- γ-Attack gives SN2' product
- α-Attack gives normal SN2 product

**Selectivity governed by:**
1. Steric effects at α vs γ positions
2. Electronic effects (conjugation)
3. Leaving group ability
4. Nucleophile hardness

### 3.3 SN1 Reaction

**Unimolecular Nucleophilic Substitution**

$$\text{R-LG} \xrightarrow{k_1} \text{R}^+ + \text{LG}^- \xrightarrow{\text{Nu}^-} \text{R-Nu}$$

**Kinetics:** Rate = k₁[R-LG] (first-order in substrate, zero-order in nucleophile)

**Stereochemistry:** Racemization (with possible inversion excess due to ion pair effects)

**Rate-determining step:** Ionization to carbocation

**Carbocation Stability:**

| Carbocation | Relative Stability |
|-------------|-------------------|
| CH₃⁺ | Least stable |
| 1° (primary) | Very unstable |
| 2° (secondary) | Moderately stable |
| 3° (tertiary) | Stable |
| Allyl | ~3° stability |
| Benzyl | ~3° stability |
| t-Bu⁺ | Standard tertiary |
| (Ph)₂CH⁺ | Very stable |
| (Ph)₃C⁺ | Extremely stable |

**Hammond Postulate Application:** The more stable the carbocation, the earlier the TS along the ionization coordinate.

**Ion Pair Effects:**
1. **Intimate ion pair**: LG still associated; nucleophile attacks from backside → inversion
2. **Solvent-separated ion pair**: LG solvated; partial stereochemical loss
3. **Free ions**: Complete racemization

**Winstein-Grunwald Equation:**
$$\log \frac{k}{k_0} = mY$$

where Y measures solvent ionizing power and m measures substrate sensitivity.

### 3.4 E2 Elimination

**Bimolecular Elimination**

$$\text{Base} + \text{H-C-C-LG} \rightarrow \text{Base-H} + \text{C=C} + \text{LG}^-$$

**Kinetics:** Rate = k₂[Base][Substrate] (second-order)

**Stereoelectronic Requirements:**
- Anti-periplanar arrangement of H-C-C-LG (E2 anti)
- Syn-periplanar (E2 syn) possible but less favorable

**Regioselectivity (Zaitsev vs Hoffmann):**
- **Zaitsev product**: More substituted alkene (thermodynamic control)
- **Hoffmann product**: Less substituted alkene (kinetic control with bulky base)

**Factors affecting regioselectivity:**

| Factor | Favors Zaitsev | Favors Hoffmann |
|--------|----------------|-----------------|
| Base size | Small (OH⁻) | Large (t-BuO⁻) |
| Leaving group | Good (I⁻, Br⁻) | Poor (F⁻, NR₃⁺) |
| Substrate | Unhindered | Hindered |
| Temperature | Lower | Higher |

**E2 Transition State Spectrum (Bunnett's):**

| TS Type | C-H Bond | C-LG Bond | Description |
|---------|----------|-----------|-------------|
| E1cB-like | Nearly broken | Intact | Carbanion character |
| Central | Both partially broken | Both partially broken | Symmetric TS |
| E1-like | Intact | Nearly broken | Carbocation character |

### 3.5 E1 Elimination

**Unimolecular Elimination**

$$\text{R-LG} \xrightarrow{k_1} \text{R}^+ + \text{LG}^- \xrightarrow{-\text{H}^+} \text{alkene}$$

**Kinetics:** Rate = k₁[R-LG] (first-order)

**Requirements:**
- Good leaving group
- Stable carbocation
- Often: no strong base (weak base or heat)

**Regioselectivity:** Zaitsev product strongly favored (thermodynamic control)

**Competition with SN1:**
- Higher temperature favors E1
- Better nucleophiles favor SN1
- More substituted cations favor E1
- Polar protic solvents favor both

### 3.6 E1cB Elimination

**Elimination Unimolecular conjugate Base**

$$\text{H-C-C-LG} \xrightarrow{-\text{H}^+} \text{ }^-\text{C-C-LG} \xrightarrow{k_1} \text{C=C} + \text{LG}^-$$

**Requirements:**
- Acidic β-hydrogen (stabilized carbanion)
- Poor leaving group
- Strong base

**Kinetics:** Rate = k₁[base][substrate] if proton transfer is fast and irreversible
Or: Rate = k₂[carbanion] if proton transfer is at equilibrium

**E1cB Spectrum:**

| Type | Proton Transfer | LG Departure | Rate Law |
|------|-----------------|--------------|----------|
| (E1cB)ᵢ | Fast, irreversible | Rate-limiting | First-order in base |
| (E1cB)ᵣ | Reversible | Rate-limiting | Complex |
| E1cB | Irreversible | Following | [Base][Substrate] |

**Examples:**
- Strongly acidic β-H: Carbonyl compounds, nitro compounds
- Poor leaving groups: NR₃⁺, SR₂⁺, OH₂⁺
- Quaternary ammonium hydroxides (Hoffmann elimination under E1cB conditions)

### 3.7 Addition-Elimination Mechanism

**Nucleophilic Acyl Substitution:**

$$\text{Nu}^- + \text{RC(O)X} \rightleftharpoons \text{RC(O)Nu} + \text{X}^-$$

**General mechanism:**
$$\text{Nu}^- + \text{RC(O)X} \rightleftharpoons [\text{Nu-C(O)R-X}]^- \rightarrow \text{RC(O)Nu} + \text{X}^-$$

**Rate depends on:**

| Factor | Effect on Addition | Effect on Elimination |
|--------|-------------------|----------------------|
| Electrophilicity of C | EWGs accelerate | EWGs decelerate |
| Leaving group ability | — | Better LG faster |
| Steric hindrance | hinders | may hinder |
| Nucleophilicity | Strong Nu faster | — |

**Tetrahedral Intermediate:**
- Stability determines rate-limiting step
- Stable intermediate → addition rate-limiting
- Unstable intermediate → elimination rate-limiting

### 3.8 Single Electron Transfer (SET) Mechanisms

**General Features:**

$$\text{D} + \text{A} \rightleftharpoons \text{D}^+ + \text{A}^-$$

**Key Characteristics:**

| Feature | Description |
|---------|-------------|
| Spin | Radical intermediate (unpaired electron) |
| Kinetics | Often radical chain mechanisms |
| Solvent | Polar aprotic often beneficial |
| Inhibition | Radical inhibitors slow reaction |
| Detection | EPR, radical traps |

**Marcus Theory for SET:**

$$k_{ET} = Z \exp\left[-\frac{(\lambda + \Delta G^\circ)^2}{4\lambda RT}\right]$$

**Rehm-Weller Equation:**
$$\Delta G_{ET} = E_{ox} - E_{red} - \frac{e^2}{\epsilon r} + C$$

**SET in Organic Reactions:**
1. **SRN1 (Substitution Radical Nucleophilic Unimolecular)**
2. **Radical nucleophilic aromatic substitution**
3. **Kolbe electrolysis**
4. **McMurray coupling**
5. **Pinacol coupling**

### 3.9 Nucleophilic Aromatic Substitution (S_NAr)

#### 3.9.1 Addition-Elimination (S_NAr)

**Mechanism:**
$$\text{Ar-X} \xrightarrow{\text{Nu}^-} [\text{Ar(Nu)X}]^- \xrightarrow{-\text{X}^-} \text{Ar-Nu}$$

**Requirements:**
- EWGs ortho or para to leaving group (stabilize Meisenheimer complex)
- Good leaving group (F⁻ > Cl⁻ > Br⁻ > I⁻, opposite to aliphatic)
- Strong nucleophile

**Rate Law:** Rate = k₂[Ar-X][Nu⁻]

**Hammett ρ:** Very large positive values (+4 to +5) indicating substantial negative charge in TS

#### 3.9.2 Benzyne Mechanism

**Elimination-Addition:**

$$\text{Ar-X} \xrightarrow{\text{strong base}} \text{benzyne} \xrightarrow{\text{Nu}^-} \text{Ar-Nu}$$

**Key Features:**
- Strong base required (NaNH₂, LDA)
- No EWG requirement
- Regiochemistry: Nucleophile can add to either position (often mixture)
- Benzyne is extremely reactive intermediate

**Benzyne Structure:**
- Strained alkyne (bond angle ~120° instead of 180°)
- Triple bond character in HOMO
- singlet ground state

#### 3.9.3 S_N1Ar (Unimolecular Aromatic Substitution)

**Mechanism:**
$$\text{Ar-N₂}^+ \rightarrow \text{Ar}^+ + \text{N}_2 \xrightarrow{\text{Nu}^-} \text{Ar-Nu}$$

**Requirements:**
- Very good leaving group (N₂ from diazonium salts)
- Occurs under mild conditions
- Often radical pathway (homolytic cleavage)

**Sandmeyer-type reactions:**

$$\text{Ar-N₂}^+ + \text{CuX} \rightarrow \text{Ar-X} + \text{N}_2 + \text{Cu}^{n+}$$

---

## 4. Kinetic Isotope Effects (KIE)

### 4.1 Primary Kinetic Isotope Effect

**Definition:** KIE arising from breaking a bond to the isotopically labeled atom in the rate-determining step.

**Theoretical Basis:**

Zero-point energy difference:
$$\text{ZPE} = \frac{1}{2}h\nu = \frac{h}{2\pi}\sqrt{\frac{k}{\mu}}$$

where μ is reduced mass: $\mu = \frac{m_1 m_2}{m_1 + m_2}$

**Maximum Primary KIEs (at 25°C):**

| Isotope Pair | Maximum k_H/k_X |
|--------------|-----------------|
| H/D | ~6-8 (theoretical: 7-10) |
| H/T | ~10-15 |
| ¹²C/¹³C | ~1.05 |
| ¹⁴N/¹⁵N | ~1.04 |
| ¹⁶O/¹⁸O | ~1.03 |

**Factors Modulating Primary KIE:**

| Factor | Effect on k_H/k_D |
|--------|-------------------|
| Symmetric TS | Maximum KIE |
| Early TS | Smaller KIE |
| Late TS | Smaller KIE |
| Tunneling | Larger KIE (>7) |
| Mixed mechanism | Intermediate values |

**Swain-Schaad Relationship:**
$$\frac{k_H}{k_T} = \left(\frac{k_H}{k_D}\right)^{1.44}$$

Used to diagnose primary vs secondary KIEs.

### 4.2 Secondary Kinetic Isotope Effect

**Definition:** KIE when the bond to the isotopically labeled atom is not broken in the TS.

**α-Secondary KIE:** Isotope at carbon bearing the reaction center

| Hybridization Change | k_H/k_D Range | Mechanism |
|---------------------|---------------|-----------|
| sp³ → sp² (more s in product) | 1.10-1.35 | SN1, E1 (carbocation) |
| sp³ → sp³ (no change) | 0.95-1.05 | SN2 with retention |
| sp² → sp³ (less s in product) | 0.80-0.95 | Nucleophilic addition |

**β-Secondary KIE:** Isotope at β-carbon

- Hyperconjugation effects: k_H/k_D = 1.05-1.20 for SN1 (positive β-KIE)
- Loss of hyperconjugative stabilization in TS

**Origin:** Change in vibrational frequencies (C-H/D bending modes) upon hybridization change.

### 4.3 Solvent Kinetic Isotope Effect

**Definition:** Rate change when solvent is changed from H₂O to D₂O (or ROH to ROD).

**Types:**

| Type | k_H/k_D | Mechanism |
|------|---------|-----------|
| Primary SKIE | 2-3 | Proton transfer in RDS |
| Secondary SKIE | 1.0-1.5 | Solvent reorganization |
| Equilibrium SKIE | Variable | Acid/base equilibria |

**Interpretation:**
- SKIE > 1.5 suggests proton transfer in RDS
- SKIE ~ 1 suggests no proton transfer in RDS
- SKIE < 1 (inverse) can occur with specific H-bonding effects

### 4.4 Heavy Atom Kinetic Isotope Effects

**Definition:** KIE for isotopes other than H/D

**Typical Values:**

| Isotope Pair | Typical KIE | Information |
|--------------|-------------|-------------|
| ¹²C/¹³C | 1.00-1.05 | C bond breaking in RDS |
| ¹⁴N/¹⁵N | 1.00-1.04 | N bond involvement |
| ¹⁶O/¹⁸O | 1.00-1.03 | O bond involvement |
| ³²S/³⁴S | 1.00-1.02 | S bond involvement |
| ³⁵Cl/³⁷Cl | 1.00-1.01 | Cl bond involvement |

**Measurement:** Requires precise isotope ratio mass spectrometry or NMR methods.

**Applications:**
- Mechanism elucidation
- Identifying rate-limiting steps
- Transition state structure determination

---

## 5. Acid-Base Chemistry

### 5.1 pKa Prediction Methods

#### 5.1.1 Taft Approach

For aliphatic acids:
$$pK_a = pK_{a,0} + \rho^* \sigma^*$$

**Example values:**
- Acetic acid series: pKₐ = 4.76 + 1.72σ*
- Propanoic acids: pKₐ = 4.87 + 1.55σ*

#### 5.1.2 Fragment Methods

**Hine's Method:**
$$pK_a = A + \sum n_i \Delta pK_{a,i}$$

where ΔpKₐ,ᵢ are fragment contributions.

**Fragment Contributions (for aliphatic acids):**

| Fragment | ΔpKₐ |
|----------|-------|
| H | 0.00 |
| CH₃ | −0.07 |
| CH₂ | 0.00 |
| OH | +0.25 |
| NH₂ | −0.15 |
| Cl | +0.90 |
| Br | +0.85 |
| CN | +1.30 |
| COOH | +0.25 |

#### 5.1.3 Hammett-Based Prediction

For substituted benzoic acids:
$$pK_a = 4.20 - \rho\sigma$$

For phenols:
$$pK_a = 9.92 - \rho\sigma$$

With enhanced resonance for para substituents affecting conjugation.

### 5.2 Solvent Effects on pKa

**Solvent Scales and pKₐ Shifts:**

The pKₐ of an acid depends on solvent:

$$pK_a(\text{solvent}) = pK_a(\text{water}) + \Delta pK_a(\text{solvent})$$

**Key Factors:**
1. Dielectric constant (ε)
2. Hydrogen bonding ability
3. Ion solvation energy
4. Specific acid-solvent interactions

**Typical pKₐ Shifts (H₂O → DMSO):**

| Acid Type | ΔpKₐ (DMSO-H₂O) |
|-----------|------------------|
| Carboxylic acids | +5 to +7 |
| Phenols | +3 to +4 |
| Alcohols | +8 to +10 |
| Amines | −1 to −3 |
| Amides | +12 to +15 |

**Bordwell pKₐ Table (DMSO):**

| Compound | pKₐ (DMSO) | pKₐ (H₂O) |
|----------|------------|-----------|
| H₂O | 31.4 | 15.7 |
| MeOH | 29.0 | 15.5 |
| t-BuOH | 32.2 | 19.0 |
| PhOH | 18.0 | 10.0 |
| CH₃COOH | 12.6 | 4.76 |
| CH₃NO₂ | 17.2 | 10.2 |
| CH₂(CN)₂ | 11.0 | 11.0 |
| NH₃ | 41.0 | 38.0 |
| PhNH₂ | 30.6 | 27.0 |

### 5.3 Ion Pairs

**Types of Ion Pairs:**

| Type | Description | Properties |
|------|-------------|------------|
| Contact ion pair | Anion-cation in direct contact | Tight, specific stereochemistry |
| Solvent-separated ion pair | One solvent molecule between | Less stereochemical control |
| Loose ion pair | Multiple solvent layers | Near-free ion behavior |
| Free ions | Fully solvated, independent | Complete stereochemical scrambling |

**Ion Pair Formation Constant:**
$$K_{ip} = \frac{[\text{ion pair}]}{[\text{free ions}]}$$

**Fuoss Equation (for spherical ions):**
$$K_{ip} = \frac{4\pi N_A a^3}{3000} \exp\left(\frac{e^2}{a\varepsilon k_B T}\right)$$

where a = contact distance, ε = dielectric constant.

**Effects on Reactivity:**

| Property | Contact Ion Pair | Free Ions |
|----------|-----------------|-----------|
| Reactivity with Nu⁻ | Higher | Lower |
| Stereochemistry | Partial control | Racemic |
| Return to starting material | Possible | Negligible |
| Rearrangement | Possible | Complete |

---

## 6. Solvent Effects

### 6.1 Polarity Scales

#### 6.1.1 Dimroth-Reichardt Eₜ(30) Scale

Based on the charge-transfer absorption of betaine dye:

$$E_T(30) = \frac{hc\tilde{\nu}_{max}}{N_A} = \frac{28591}{\lambda_{max}(\text{nm})} \text{ kcal/mol}$$

**Eₜ(30) Values (Selected Solvents):**

| Solvent | Eₜ(30) (kcal/mol) | Polarity |
|---------|-------------------|----------|
| Water | 63.1 | Highest |
| Methanol | 55.5 | Very high |
| Ethanol | 51.9 | High |
| Acetonitrile | 46.0 | Medium-high |
| DMF | 43.8 | Medium |
| Acetone | 42.2 | Medium |
| DCM | 41.1 | Medium-low |
| THF | 37.4 | Low |
| Benzene | 34.5 | Low |
| Hexane | 30.9 | Lowest |

**Normalized Scale:**
$$E_T^N = \frac{E_T(\text{solvent}) - E_T(\text{SiMe}_4)}{E_T(\text{water}) - E_T(\text{SiMe}_4)} = \frac{E_T - 30.7}{32.4}$$

#### 6.1.2 Kosower Z Scale

Based on charge-transfer absorption of 1-ethyl-4-methoxycarbonylpyridinium iodide:

$$Z = \frac{hc\tilde{\nu}_{max}}{N_A} \text{ kcal/mol}$$

**Z Values:**
- Water: 94.6 kcal/mol
- MeOH: 83.6 kcal/mol
- EtOH: 79.6 kcal/mol
- Acetone: 65.7 kcal/mol

#### 6.1.3 Grunwald-Winstein Y Scale

Measures solvent ionizing power for SN1 reactions:

$$Y = \log \frac{k_{t-BuCl}}{k_{t-BuCl}^0}$$

**Y Values:**

| Solvent | Y |
|---------|------|
| 100% EtOH | −2.03 |
| 80% EtOH/20% H₂O | 0.00 |
| 50% EtOH/50% H₂O | 1.65 |
| Water | 3.49 |
| 97% HFIP | 4.57 |

### 6.2 Hydrogen Bonding Scales

#### 6.2.1 Kamlet-Taft Parameters

**α (hydrogen bond donor acidity):**
Measures ability to donate H-bonds

| Solvent | α |
|---------|------|
| Water | 1.17 |
| MeOH | 0.98 |
| EtOH | 0.86 |
| CHCl₃ | 0.44 |
| DCM | 0.13 |
| Acetonitrile | 0.19 |

**β (hydrogen bond acceptor basicity):**
Measures ability to accept H-bonds

| Solvent | β |
|---------|------|
| HMPA | 1.00 |
| DMSO | 0.76 |
| DMF | 0.69 |
| Pyridine | 0.64 |
| THF | 0.55 |
| Acetone | 0.48 |
| Acetonitrile | 0.31 |
| DCM | 0.00 |

#### 6.2.2 Abraham's H-bond Parameters

**H-bond acidity (A):**
$$\log K_A = aA + b$$

**H-bond basicity (B):**
$$\log K_B = aB + b$$

### 6.3 π* Scale (Polarizability)

Measures solvent polarizability and dipolarity:

**π* Values (Selected):**

| Solvent | π* |
|---------|------|
| DMSO | 1.00 |
| DMF | 0.88 |
| Acetonitrile | 0.75 |
| Acetone | 0.71 |
| THF | 0.58 |
| CHCl₃ | 0.58 |
| DCM | 0.82 |
| Benzene | 0.59 |
| Hexane | −0.08 |

**LSER (Linear Solvation Energy Relationship):**
$$XYZ = XYZ_0 + s\pi^* + a\alpha + b\beta$$

### 6.4 Solvent Cages

**Definition:** Enclosed region where reactants are trapped by solvent molecules.

**Characteristics:**
- High local concentration of radicals/intermediates
- Enhanced recombination rates
- Reduced diffusion to bulk solution

**Cage Effect Quantification:**

$$\text{Cage Efficiency} = \frac{\text{products from cage}}{\text{total products}}$$

**Noyes Model:**
$$F_c = \frac{k_{diff} + k_{recomb}}{k_{diff} + k_{recomb} + k_{escape}}$$

**Examples:**

| Reaction | Cage Effect |
|----------|-------------|
| Azocompound decomposition | Significant geminate recombination |
| Peroxide decomposition | Radical recombination in cage |
| Photolysis of RI | R• + I• recombination |
| Fenton chemistry | •OH recombination |

**Factors Affecting Cage Effects:**

| Factor | Effect |
|--------|--------|
| Solvent viscosity | Higher → more cage effect |
| Temperature | Lower → more cage effect |
| Radical reactivity | Higher → more escape |
| Solvent structure | Organized solvents enhance cages |

---

## 7. Stereochemistry

### 7.1 Conformational Analysis

#### 7.1.1 Molecular Mechanics (MM)

**Force Field Energy:**
$$E_{total} = E_{bond} + E_{angle} + E_{torsion} + E_{VDW} + E_{electrostatic} + E_{special}$$

**Common Force Fields:**

| Force Field | Application | Key Features |
|-------------|-------------|--------------|
| MM2/MM3/MM4 | Small molecules | Accurate hydrocarbons |
| MMFF94 | Drug-like molecules | Balanced parameters |
| AMBER | Biomolecules | Proteins, nucleic acids |
| CHARMM | Biomolecules | Extensive testing |
| OPLS-AA | Liquids, biomolecules | Liquid-state properties |
| UFF | General | All elements |

**Torsional Energy:**
$$E_{torsion} = \sum_n \frac{V_n}{2}[1 + \cos(n\phi - \gamma)]$$

**Example: Ethane**
- Three-fold barrier
- V₃ ≈ 2.9 kcal/mol
- Staggered preferred over eclipsed by ~0.9 kcal/mol

#### 7.1.2 DFT for Conformational Analysis

**Recommended Methods:**

| Method | Basis Set | Application |
|--------|-----------|-------------|
| B3LYP | 6-31G(d) | General organic molecules |
| M06-2X | 6-311+G(d,p) | Noncovalent interactions |
| ωB97X-D | def2-TZVP | Dispersion-important systems |
| B97-D3 | def2-SVP | Large systems, dispersion |

**Dispersion Correction:** Essential for accurate conformer energies
- DFT-D3 (Grimme)
- DFT-D4
- Nonlocal functionals (VV10, rVV10)

### 7.2 Cyclohexane Chair Conformations

**A Values (Conformational Free Energy):**

| Substituent | A (kcal/mol) | Preference |
|-------------|--------------|------------|
| H | 0.00 | — |
| F | 0.15-0.25 | Equatorial |
| Cl | 0.43-0.53 | Equatorial |
| Br | 0.48-0.63 | Equatorial |
| I | 0.43-0.57 | Equatorial |
| OH | 0.60-0.87 | Equatorial |
| OMe | 0.60-0.70 | Equatorial |
| NH₂ | 1.20-1.70 | Equatorial |
| CH₃ | 1.70-1.80 | Equatorial |
| CH₂CH₃ | 1.75-1.80 | Equatorial |
| CH(CH₃)₂ | 2.10-2.20 | Equatorial |
| C(CH₃)₃ | >4.0 | Strongly equatorial |
| Ph | 3.0 | Equatorial |

**Ring Flip Energy Barrier:**
- Cyclohexane: ~10.8 kcal/mol (chair → twist-boat → chair)
- Substituted: Modified by A-values

**1,3-Diaxial Interactions:**

| Interaction | Energy (kcal/mol) |
|-------------|-------------------|
| H-H | 0.5 |
| H-Me | 0.9 |
| Me-Me | 1.8 |
| H-t-Bu | 2.2 |
| t-Bu-t-Bu | >5 |

**Bürgi-Dunitz Angle:**
- Nucleophilic attack on C=O: ~107° from C=O axis
- Similar angles for other trigonal centers

### 7.3 Atropisomerism

**Definition:** Stereoisomers arising from hindered rotation about a single bond.

**Requirements:**
1. Restricted rotation (high barrier)
2. Asymmetric substitution on both sides of bond
3. Barrier high enough to prevent interconversion

**Barrier Classification:**

| Barrier (kcal/mol) | t₁/₂ at 25°C | Classification |
|-------------------|--------------|----------------|
| < 15 | < 1 second | Freely rotating |
| 15-20 | seconds-days | Slow rotation |
| 20-25 | months-years | Atropisomeric |
| > 25 | > years | Configurationally stable |

**Common Atropisomeric Systems:**

| System | Barrier (kcal/mol) | Example |
|--------|-------------------|---------|
| Biaryls (2,2'-disubstituted) | 15-40+ | BINAP, BINOL |
| Anilides | 15-25 | Drugs with atropisomerism |
| Aryl-amides | 15-20 | Conformationally restricted |
| Bridged biaryls | > 40 | Caged structures |

**Factors Affecting Barrier:**

| Factor | Effect on Barrier |
|--------|-------------------|
| Ortho substituent size | Larger → higher barrier |
| Number of ortho substituents | More → higher barrier |
| Bond order (partial) | Higher → higher barrier |
| Intramolecular H-bonding | Can increase or decrease |
| Ring size (fused systems) | Smaller → higher barrier |

### 7.4 Axial Chirality

**Descriptor Systems:**

**Rₐ/Sₐ (Axial):**
1. View along chiral axis
2. Assign priorities to front pair (Cahn-Ingold-Prelog)
3. View from rear; determine rotation of rear priorities
4. Rₐ = clockwise when viewed from front

**M/P (Helical):**
- M (minus): Left-handed helix
- P (plus): Right-handed helix

**Examples:**

| Molecule | Chirality Type | Descriptor |
|----------|----------------|------------|
| BINOL | Axial | Rₐ/Sₐ |
| Allenes | Axial | Rₐ/Sₐ |
| Spiranes | Central + axial | Combined |
| Helicenes | Helical | M/P |
| Twisted amides | Axial | Rₐ/Sₐ |

---

## 8. Reactive Intermediates

### 8.1 Carbocations

**Structure and Stability:**

| Carbocation | Geometry | Stability Trend |
|-------------|----------|-----------------|
| Methyl | Planar | Least stable |
| Primary | Planar | Very unstable |
| Secondary | Planar | Moderately stable |
| Tertiary | Planar | Stable |
| Allyl | Planar delocalized | ~Tertiary |
| Benzyl | Planar delocalized | ~Tertiary |
| Vinyl | Linear | Unstable (sp) |
| Acyl | Linear | Unstable |

**Stabilization Mechanisms:**

| Mechanism | Example | Stabilization (kcal/mol) |
|-----------|---------|-------------------------|
| Hyperconjugation | t-Bu⁺ | ~10-15 |
| Resonance | PhCH₂⁺ | ~15-20 |
| π-Donation | CH₂=CH-CH₂⁺ | ~15 |
| σ-Donation | (CH₃)₃C⁺ | ~10 |
| Aromaticity | Cyclopropenium | Very stable |

**NMR Chemical Shifts:**

| Carbocation | ¹³C δ (ppm) | ¹H δ (ppm) |
|-------------|-------------|------------|
| CH₃⁺ (calculated) | ~400 | — |
| (CH₃)₃C⁺ | 330 | 4.0 |
| Ph₂CH⁺ | 210 | 9.0 |
| Ph₃C⁺ | 180 | — |
| Tropylium | 155 | 9.3 |

**Trapping Reactions:**

| Trap | Product |
|------|---------|
| Nucleophile (Nu⁻) | R-Nu |
| Water/alcohol | R-OH/OR |
| Alkene | Addition products |
| Aromatic ring | Friedel-Crafts |
| Hydride donor | R-H |
| Azide | R-N₃ |

### 8.2 Carbanions

**Structure and Stability:**

| Carbanion | Geometry | Stability Trend |
|-----------|----------|-----------------|
| Methyl | Pyramidal (sp³) | Most reactive |
| Primary | Pyramidal | Reactive |
| Secondary | Pyramidal | Less reactive |
| Tertiary | Pyramidal | Least reactive |
| Allyl | Planar delocalized | Stable |
| Benzyl | Planar delocalized | Stable |
| α to carbonyl | Planar | Stable |
| α to nitro | Planar | Very stable |

**Stabilization Mechanisms:**

| Mechanism | Example | Effect |
|-----------|---------|--------|
| Resonance | PhCH₂⁻ | Strong stabilization |
| Inductive (EWG) | F₃C⁻ | Moderate stabilization |
| Aromaticity | Cyclopentadienyl | Very stable (aromatic) |
| α to heteroatom | CH₃CH₂OCH₂⁻ | Moderate |
| d-Orbital participation | SiR₃⁻ | Moderate |

**pKₐ Values of Precursors (DMSO):**

| Compound | pKₐ (DMSO) | Anion Type |
|----------|------------|------------|
| CH₄ | ~48 | Methyl |
| PhH | 43 | Phenyl |
| CH₃CH₃ | ~50 | Primary |
| (CH₃)₃CH | ~51 | Tertiary |
| CH₃CH₂Ph | 40.5 | Benzyl |
| CH₂=CHCH₃ | 43 | Allylic |
| CH₃COPh | 24.0 | α to carbonyl |
| CH₂(COPh)₂ | 13.5 | α to two carbonyls |
| CH₃NO₂ | 17.2 | α to nitro |
| CH₂(NO₂)₂ | 3.6 | α to two nitros |

**NMR of Carbanions:**

| Carbanion | ¹³C δ (ppm) | Characteristics |
|-----------|-------------|-----------------|
| CH₃⁻ | ~−10 | Shielded |
| PhCH₂⁻ | ~35 | Less shielded |
| (Ph)₂CH⁻ | ~60 | Even less |
| (Ph)₃C⁻ | ~90 | Least shielded |

### 8.3 Radicals

**Structure and Stability:**

| Radical | Geometry | Stability Trend |
|---------|----------|-----------------|
| Methyl | Planar (sp²) | Reactive |
| Primary alkyl | Planar | Reactive |
| Secondary alkyl | Planar | Less reactive |
| Tertiary alkyl | Planar | Moderately stable |
| Allyl | Planar delocalized | Stable |
| Benzyl | Planar delocalized | Stable |
| Phenyl | Planar | Reactive |
| Peroxyl | Bent | Moderately stable |
| Nitroxyl (TEMPO) | Bent | Very stable |

**Bond Dissociation Energies (BDE):**

| Bond | BDE (kcal/mol) | Radical Stability |
|------|----------------|-------------------|
| H-CH₃ | 105 | Methyl radical |
| H-CH₂CH₃ | 101 | Primary radical |
| H-CH(CH₃)₂ | 98.5 | Secondary radical |
| H-C(CH₃)₃ | 96.5 | Tertiary radical |
| H-CH₂Ph | 90 | Benzyl radical |
| H-CH₂CH=CH₂ | 88 | Allyl radical |

**EPR Parameters:**

| Radical | g-value | a_H (G) | Characteristics |
|---------|---------|---------|-----------------|
| CH₃• | 2.0026 | 23 | Three equivalent H |
| CH₃CH₂• | 2.0025 | 22 (α), 27 (β) | α and β H |
| (CH₃)₂CH• | 2.0026 | 22 (α) | One α H |
| (CH₃)₃C• | 2.0026 | — | No α H |
| CH₂=CH-CH₂• | 2.0025 | 4.9, 14.8 | Delocalized |

**Stabilization (kcal/mol):**

| Substituent | Stabilization of R• |
|-------------|---------------------|
| Ph | 12-15 |
| CH=CH₂ | 13 |
| OR | 5-10 |
| NR₂ | 8-12 |
| F | 3 |
| Cl | 4 |
| CN | 6 |

### 8.4 Carbenes

**Electronic Structure:**

| Type | Configuration | Geometry | Reactivity |
|------|---------------|----------|------------|
| Singlet | sp² + p (empty) | Bent (~100-110°) | Electrophilic |
| Triplet | sp + 2p (2 electrons) | Linear/bent | Diradical-like |

**Singlet-Triplet Gap:**

| Carbene | ΔE_ST (kcal/mol) | Ground State |
|---------|------------------|--------------|
| CH₂ | 9 | Triplet |
| CHF | −15 | Singlet |
| CF₂ | −56 | Singlet |
| CCl₂ | −20 | Singlet |
| CHPh | −4 | Singlet |
| C(Ph)₂ | −5 | Singlet |
| CH(COOR) | −20 | Singlet |
| CH(NR₂) | −30 | Singlet |

**Carbene Generation Methods:**

| Method | Precursor | Conditions |
|--------|-----------|------------|
| α-Elimination | CHX₃, base | Strong base |
| Diazocompound decomposition | R₂C=N₂ | Heat, light, or catalyst |
| Simmons-Smith | CH₂I₂, Zn-Cu | Zn-Cu couple |
| Photolysis of ketene | R₂C=C=O | hν |
| Nucleophilic attack | Dihalocarbene from CHX₃ | Base |

**Reactivity Patterns:**

| Reaction | Singlet | Triplet |
|----------|---------|---------|
| Cyclopropanation | Concerted | Stepwise |
| C-H insertion | Concerted | Radical abstraction |
| Addition to alkene | Stereospecific | Non-stereospecific |

### 8.5 Nitrenes

**Electronic Structure:**

| Type | Configuration | Geometry | Reactivity |
|------|---------------|----------|------------|
| Singlet | sp² + p (empty) | Bent | Electrophilic |
| Triplet | sp + 2p (2 electrons) | Linear/bent | Diradical |

**Singlet-Triplet Gap:**

| Nitrene | ΔE_ST (kcal/mol) | Ground State |
|---------|------------------|--------------|
| NH | 36 | Triplet |
| NPh | −18 | Singlet |
| NAcyl | ~−40 | Singlet |
| NSO₂R | — | Singlet |

**Generation Methods:**

| Method | Precursor |
|--------|-----------|
| Azide thermolysis | RN₃ → RN + N₂ |
| Azide photolysis | RN₃ → RN + N₂ |
| α-Elimination | R-NHX, base |
| Oxidation of amines | RNH₂ + oxidant |

**Reactions:**

| Reaction | Product |
|----------|---------|
| C-H insertion | R-NH-R' |
| H abstraction | R-NH• |
| Addition to alkene | Aziridine |
| Rearrangement (Curtius) | Isocyanate |
| Ring expansion | Lactam |

### 8.6 Arynes

**Structure:**
- Formal triple bond in aromatic ring
- Bond angle strain (~120° instead of 180°)
- Bent triple bond

**Generation Methods:**

| Method | Precursor | Conditions |
|--------|-----------|------------|
| Base elimination | Ar-X (ortho dihalide) | Strong base |
| Diazonium decomposition | Ar-N₂⁺ | Heat |
| Oxidation | Aryl silane/ester | Fluoride/oxidant |
| Benzothiadiazoles | 1,2-Benzothiadiazoles | Heat |

**Reactivity:**

| Reaction | Regiochemistry | Notes |
|----------|----------------|-------|
| Nucleophilic addition | Unsymmetrical, depends on substituents | Mixtures common |
| Cycloaddition | [2+2], [4+2] | Strain release |
| Diels-Alder | 4+2 | Common |
| With nucleophiles | Can be guided by EWGs/EDGs | LUMO control |

**Aryne LUMO:**

The LUMO of benzyne determines regiochemistry:
- Electron-withdrawing substituents stabilize LUMO
- Direct nucleophile addition to less hindered position with electronic guidance

**Spectroscopic Detection:**
- Transient absorption (UV-Vis)
- Matrix isolation IR
- Trapping with dienes (Diels-Alder adducts)

---

## 9. Pericyclic Theory

**Brief overview; detailed treatment in** `pericyclic_reactions.md` **and** `pericyclic_advanced.md`.

### 9.1 Orbital Symmetry Conservation

**Woodward-Hoffmann Rules:**

For pericyclic reactions, orbital symmetry is conserved:
- Ground state reactions: thermally allowed if (4n+2) suprafacial or 4n antarafacial
- Excited state reactions: photochemically allowed when thermal is forbidden

### 9.2 Frontier Molecular Orbital (FMO) Theory

**HOMO-LUMO Interactions:**

| Reaction | Key Interaction |
|----------|-----------------|
| Cycloaddition | HOMO(diene)-LUMO(dienophile) |
| Electrocyclic | HOMO of polyene |
| Sigmatropic | HOMO of component |

**FMO Analysis for [4+2] Diels-Alder:**
- Diene HOMO: ψ₂ (2 nodes, symmetric)
- Dienophile LUMO: π* (1 node, antisymmetric)
- Symmetry-allowed: suprafacial-suprafacial

### 9.3 Correlation Diagrams

**Principle:** Correlate orbitals of reactants and products by symmetry.

**Correlation Diagram Components:**
1. Identify symmetry elements preserved
2. List reactant and product orbitals
3. Assign symmetry labels
4. Connect orbitals of same symmetry
5. Check for symmetry-imposed barriers

**Example: Electrocyclic Ring Closure of Butadiene**
- Disrotatory: C₂ symmetry preserved → thermally allowed
- Conrotatory: σᵥ symmetry preserved → thermally forbidden

---

## 10. Computational Chemistry for Organic Mechanisms

### 10.1 DFT Functionals

**Recommended Functionals by Application:**

| Application | Recommended Functional | Basis Set |
|-------------|----------------------|-----------|
| General thermochemistry | B3LYP | 6-31G(d) |
| Noncovalent interactions | M06-2X, ωB97X-D | 6-311+G(d,p) |
| Transition metals | B3LYP, M06, TPSSh | def2-TZVP |
| Barrier heights | M06-2X, ωB97X-D | 6-311+G(d,p) |
| Radicals | M06-2X, ωB97X-D | 6-311+G(d,p) |
| Charge transfer | CAM-B3LYP, ωB97X-D | 6-311+G(d,p) |
| Large systems | B97-D3, GFN2-xTB | minimal |

**Dispersion Correction:**

| Method | Description | When to Use |
|--------|-------------|-------------|
| DFT-D3 | Grimme's empirical dispersion | Always for noncovalent |
| DFT-D4 | Atom-in-molecule dependent | Improved accuracy |
| DFT-NL | Nonlocal correlation | ωB97M-V, B97M-V |

**Functional Accuracy (Barriers):**

| Functional | MAE (kcal/mol) | Notes |
|------------|----------------|-------|
| B3LYP | 3-4 | May underestimate barriers |
| M06-2X | 1-2 | Good for kinetics |
| ωB97X-D | 1-2 | Good all-around |
| B2PLYP-D3 | 0.5-1 | Double hybrid, accurate |
| DLPNO-CCSD(T) | < 0.5 | Near benchmark |

### 10.2 Solvent Models

#### 10.2.1 Implicit Solvent Models

**Polarizable Continuum Model (PCM):**

$$\Delta G_{solv} = G_{solvated} - G_{gas}$$

**PCM Variants:**

| Model | Description | Use Case |
|-------|-------------|----------|
| IEF-PCM | Integral equation formalism | General |
| CPCM | Conductor-like | Fast, general |
| SMD | Solvation model based on density | Accurate ΔG_solv |

**SMD Solvation Free Energies (Selected Solvents):**

| Solvent | ε | Typical ΔG_solv (kcal/mol) |
|---------|---|---------------------------|
| Water | 78.4 | Strong stabilization of ions |
| DMSO | 46.7 | Moderate |
| Acetonitrile | 36.6 | Moderate |
| Methanol | 32.7 | Moderate |
| THF | 7.43 | Weak |
| DCM | 8.93 | Weak |
| Benzene | 2.27 | Very weak |

#### 10.2.2 Explicit-Implicit Hybrid Models

**Cluster-Continuum:**
- Include key explicit solvent molecules (first solvation shell)
- Embed in implicit solvent

**Thermodynamic Cycle:**
$$\Delta G_{soln} = \Delta G_{gas} + \Delta G_{solv}(products) - \Delta G_{solv}(reactants)$$

### 10.3 Activation Barriers

**Eyring Equation:**

$$k = \frac{k_B T}{h} \exp\left(-\frac{\Delta G^\ddagger}{RT}\right)$$

**Computational Protocol:**

1. **Geometry Optimization:**
   - Optimize reactants and products (DFT, moderate basis)
   - Confirm minima (frequency calculation: all positive)

2. **Transition State Search:**
   - QST2, QST3, or TS optimization
   - Confirm TS (one imaginary frequency)

3. **Frequency Calculation:**
   - Obtain thermal corrections
   - Verify TS (negative frequency corresponds to reaction coordinate)

4. **Single-Point Energy:**
   - Higher-level calculation on optimized geometries
   - Larger basis set, better functional

5. **Solvent Correction:**
   - Apply implicit solvent model

6. **Free Energy:**
   $$G = E_{electronic} + G_{thermal} + G_{solvation}$$

**Activation Barrier:**
$$\Delta G^\ddagger = G_{TS} - G_{reactants}$$

**Kinetic Isotope Effect from Calculation:**

$$\text{KIE} = \frac{k_H}{k_D} = \exp\left[\frac{\Delta \Delta G^\ddagger}{RT}\right]$$

where ΔΔG‡ = ΔG‡(D) − ΔG‡(H)

### 10.4 Common Computational Pitfalls

| Issue | Consequence | Solution |
|-------|-------------|----------|
| Insufficient basis set | Inaccurate barriers | At least 6-31G(d), preferably 6-311+G(d,p) |
| No dispersion correction | Wrong conformer energies | Use D3 or D4 correction |
| Gas phase only | Wrong mechanism in solution | Include solvent model |
| Single conformer | Missing lowest-energy conformer | Conformer search |
| No zero-point correction | Wrong relative energies | Always include ZPE |
| Incomplete TS verification | Not a TS | Check frequency, IRC |

---

## 11. Worked Examples

### Example 1: Hammett Analysis of Ester Hydrolysis

**Problem:** The rates of base-catalyzed hydrolysis of substituted methyl benzoates give the following data:

| Substituent | k/k₀ |
|-------------|------|
| p-OMe | 0.26 |
| p-Me | 0.62 |
| H | 1.00 |
| p-Cl | 3.10 |
| p-CN | 15.5 |
| p-NO₂ | 48.0 |

**Solution:**

1. Calculate log(k/k₀):
   - p-OMe: log(0.26) = −0.585
   - p-Me: log(0.62) = −0.208
   - H: log(1.00) = 0.000
   - p-Cl: log(3.10) = +0.491
   - p-CN: log(15.5) = +1.190
   - p-NO₂: log(48.0) = +1.681

2. Plot log(k/k₀) vs σₚ

3. From linear regression: ρ = +2.23

**Interpretation:**
- Positive ρ indicates reaction is favored by EWGs
- Large magnitude indicates substantial negative charge development in TS
- Consistent with anionic tetrahedral intermediate mechanism

### Example 2: Brønsted Analysis

**Problem:** The rate constants for general base-catalyzed hydrolysis of ethyl acetate with various bases:

| Base | pKₐ (conjugate acid) | k (M⁻¹s⁻¹) |
|------|---------------------|------------|
| Acetate | 4.76 | 0.11 |
| Formate | 3.75 | 0.041 |
| Chloroacetate | 2.86 | 0.012 |
| Fluoroacetate | 2.59 | 0.0098 |

**Solution:**

1. Calculate log k:
   - Acetate: log(0.11) = −0.959
   - Formate: log(0.041) = −1.387
   - Chloroacetate: log(0.012) = −1.921
   - Fluoroacetate: log(0.0098) = −2.009

2. Plot log k vs pKₐ

3. From linear regression: β = 0.47

**Interpretation:**
- β ≈ 0.5 indicates partial proton transfer in TS
- TS is approximately midway between reactants and products
- Hammond Postulate: TS is "central" in character

### Example 3: KIE Mechanism Determination

**Problem:** A nucleophilic substitution reaction shows k_H/k_D = 6.5 when the α-hydrogen is replaced with deuterium. What does this indicate?

**Solution:**

1. k_H/k_D = 6.5 is a large primary KIE (maximum ~7 for H/D)

2. Primary KIE indicates C-H(D) bond is being broken in the rate-determining step

3. This is inconsistent with classical SN2 (no C-H bond breaking) or SN1 (no C-H bond breaking in RDS)

4. **Mechanism:** This suggests an E2 elimination or hydride transfer mechanism

**Further Investigation:**
- Check for β-secondary KIE (would support E2)
- Look for alkene products
- Test effect of base concentration on rate

### Example 4: Solvent Effect Analysis

**Problem:** The rate of SN1 solvolysis of t-butyl chloride increases by a factor of ~10⁵ when changing from 80% ethanol/20% water (Y = 0) to water (Y = 3.49). Calculate the reaction sensitivity.

**Solution:**

Using Winstein-Grunwald equation:
$$\log \frac{k}{k_0} = mY$$

$$\log(10^5) = 5 = m \times 3.49$$

$$m = \frac{5}{3.49} = 1.43$$

**Interpretation:**
- m > 1 indicates high sensitivity to solvent ionizing power
- t-Butyl chloride is highly dependent on solvent polarity for ionization
- Consistent with SN1 mechanism with extensive charge separation in TS

### Example 5: Conformational Analysis

**Problem:** Calculate the equilibrium ratio of axial:equatorial conformers for trans-1,4-dimethylcyclohexane.

**Solution:**

1. Both conformations have one axial and one equatorial methyl group

2. For each conformer, one methyl is axial (A = 1.7 kcal/mol penalty)

3. Both conformers are equivalent in energy

4. **Ratio:** 50:50 at equilibrium

**Contrast with cis-1,4-dimethylcyclohexane:**
- One conformer: both methyls axial (2 × 1.7 = 3.4 kcal/mol)
- Other conformer: both methyls equatorial (0 kcal/mol)
- ΔG = 3.4 kcal/mol

$$K = e^{-\Delta G/RT} = e^{-3.4/(0.592)} = e^{-5.74} \approx 0.003$$

- Ratio: ~99.7% diequatorial at 25°C

### Example 6: Carbocation Stability Prediction

**Problem:** Rank the following carbocations by stability: CH₃⁺, CH₃CH₂⁺, (CH₃)₂CH⁺, (CH₃)₃C⁺, CH₂=CH-CH₂⁺, PhCH₂⁺

**Solution:**

1. **Methyl cation (CH₃⁺):** Least stable, no hyperconjugation
2. **Primary (CH₃CH₂⁺):** Unstable, 3 hyperconjugative interactions
3. **Secondary ((CH₃)₂CH⁺):** Moderately stable, 6 hyperconjugative interactions
4. **Tertiary ((CH₃)₃C⁺):** Stable, 9 hyperconjugative interactions
5. **Allyl (CH₂=CH-CH₂⁺):** Very stable, resonance delocalization
6. **Benzyl (PhCH₂⁺):** Most stable, extended resonance delocalization

**Order:** CH₃⁺ < CH₃CH₂⁺ < (CH₃)₂CH⁺ < (CH₃)₃C⁺ ≈ CH₂=CH-CH₂⁺ < PhCH₂⁺

### Example 7: Radical Stability from BDE

**Problem:** Calculate the stabilization energy of the benzyl radical relative to methyl radical using BDE data.

**Solution:**

BDE(H-CH₃) = 105 kcal/mol
BDE(H-CH₂Ph) = 90 kcal/mol

**Stabilization Energy:**
$$\Delta E = \text{BDE}(H-CH_3) - \text{BDE}(H-CH_2Ph) = 105 - 90 = 15 \text{ kcal/mol}$$

**Interpretation:**
- Benzyl radical is stabilized by 15 kcal/mol relative to methyl radical
- This stabilization comes from resonance delocalization of the unpaired electron into the phenyl ring

### Example 8: Taft Equation Application

**Problem:** The rate constants for hydrolysis of substituted acetates XC₂H₄OCOCH₃ are:

| X | k/k₀ | σ* |
|---|------|------|
| H | 1.00 | 0.00 |
| Me | 0.75 | −0.10 |
| Et | 0.60 | −0.10 |
| Cl | 3.2 | +0.17 |
| CN | 12.5 | +0.60 |

Determine if polar or steric effects dominate.

**Solution:**

1. Plot log(k/k₀) vs σ*

2. If polar effects dominate: linear correlation with σ*
3. If steric effects dominate: poor correlation with σ*

**Data Analysis:**
- H and Et have same σ* but different rates → steric effects present
- Me and Et have same σ* but Et is slower → steric effect

**Taft Analysis:**
$$\log \frac{k}{k_0} = \rho^* \sigma^* + \delta E_s$$

Using Cl and H (similar Eₛ):
$$\log 3.2 = \rho^* \times 0.17$$
$$\rho^* = \frac{0.505}{0.17} = 2.97$$

**Conclusion:** Both polar (ρ* = ~3) and steric effects are significant.

### Example 9: Yukawa-Tsuno Analysis

**Problem:** The solvolysis of cumyl chlorides gives a Hammett ρ = −4.54 and r = 1.00. Interpret.

**Solution:**

1. **ρ = −4.54:** Large negative value indicates reaction strongly favored by EDGs

2. **r = 1.00:** Maximum resonance enhancement; full carbocation character in TS

3. **Mechanism:** SN1 with complete carbocation formation in RDS

4. **Implication:** Reaction involves σ⁺ rather than σ for para substituents

**Using Yukawa-Tsuno equation:**
$$\log \frac{k}{k_0} = -4.54[\sigma + 1.00(\sigma^+ - \sigma)] = -4.54\sigma^+$$

For p-OMe (σ⁺ = −0.78):
$$\log \frac{k}{k_0} = -4.54 \times (-0.78) = +3.54$$
$$k/k_0 = 10^{3.54} \approx 3467$$

Huge rate acceleration from electron donation!

### Example 10: DFT Barrier Calculation

**Problem:** Calculate the rate constant at 298 K for a reaction with computed ΔG‡ = 18.5 kcal/mol.

**Solution:**

Using Eyring equation:
$$k = \frac{k_B T}{h} \exp\left(-\frac{\Delta G^\ddagger}{RT}\right)$$

Where:
- k_B = 1.381 × 10⁻²³ J/K
- h = 6.626 × 10⁻³⁴ J·s
- T = 298 K
- R = 1.987 cal/(mol·K) = 8.314 J/(mol·K)
- ΔG‡ = 18.5 kcal/mol = 18,500 cal/mol

$$\frac{k_B T}{h} = \frac{(1.381 \times 10^{-23})(298)}{6.626 \times 10^{-34}} = 6.21 \times 10^{12} \text{ s}^{-1}$$

$$\exp\left(-\frac{18500}{1.987 \times 298}\right) = \exp(-31.2) = 2.4 \times 10^{-14}$$

$$k = (6.21 \times 10^{12})(2.4 \times 10^{-14}) = 1.5 \times 10^{-1} \text{ s}^{-1}$$

**Half-life:**
$$t_{1/2} = \frac{\ln 2}{k} = \frac{0.693}{0.15} = 4.6 \text{ s}$$

### Example 11: Solvent KIE

**Problem:** A reaction shows k_H₂O/k_D₂O = 2.5. Interpret.

**Solution:**

1. SKIE = 2.5 indicates proton transfer is involved in RDS

2. This is a primary solvent kinetic isotope effect

3. Mechanism involves proton (or H₃O⁺) transfer in rate-determining step

**Further Tests:**
- If SKIE varies with substrate structure: specific acid catalysis
- If SKIE is constant: general acid catalysis
- Check pH (pD) dependence for mechanistic details

### Example 12: Benzyne Regioselectivity

**Problem:** Predict the major product when benzyne reacts with ammonia.

**Solution:**

1. Benzyne is symmetric, so nucleophile can add to either position

2. No electronic bias in unsubstituted benzyne

3. Ammonia adds to give equal mixture of ortho- and meta-substituted aniline

**With 3-methoxybenzyne:**
- Methoxy is an EDG
- LUMO coefficient is larger at C-2 (less substituted position)
- Nucleophile adds preferentially to C-2
- Major product: 2-methoxyaniline

### Example 13: Secondary KIE and Mechanism

**Problem:** The solvolysis of a series of deuterated tosylates shows:

| Substrate | k_H/k_D |
|-----------|---------|
| C₆H₅CH₂CH₂OTs | — |
| C₆H₅CD₂CH₂OTs | 1.17 |
| C₆H₅CH₂CD₂OTs | 1.22 |

Identify the mechanism.

**Solution:**

1. **α-deuterium KIE (k_H/k_D = 1.22):** Secondary α-KIE
   - Value > 1 indicates hybridization change sp³ → sp²
   - Consistent with carbocation formation

2. **β-deuterium KIE (k_H/k_D = 1.17):** Secondary β-KIE
   - Value > 1 indicates hyperconjugation loss
   - Carbocation adjacent to labeled position

3. **Conclusion:** SN1 mechanism with carbocation intermediate

**Contrast with SN2:**
- SN2 would show inverse α-KIE (< 1)
- No significant β-KIE for SN2

### Example 14: Atropisomerism Barrier

**Problem:** 2,2'-Dibromobiphenyl has a rotational barrier of 15.5 kcal/mol. Is it atropisomeric at room temperature?

**Solution:**

Using Eyring equation for rate:
$$k = \frac{k_B T}{h} \exp\left(-\frac{\Delta G^\ddagger}{RT}\right)$$

$$k = (6.21 \times 10^{12}) \exp\left(-\frac{15500}{1.987 \times 298}\right)$$
$$k = (6.21 \times 10^{12}) \exp(-26.2)$$
$$k = (6.21 \times 10^{12})(4.0 \times 10^{-12}) = 2.5 \text{ s}^{-1}$$

**Half-life:**
$$t_{1/2} = \frac{0.693}{2.5} = 0.28 \text{ s}$$

**Conclusion:** Too fast for atropisomerism (need t₁/₂ > 1000 s typically)
- Borderline case
- At low temperature (−78°C): k ≈ 5 × 10⁻⁴ s⁻¹, t₁/₂ ≈ 23 min
- Could be resolved at low temperature

### Example 15: Computational Study of Reaction Mechanism

**Problem:** DFT calculations for an SN2 reaction show:
- Reactants: −234.567890 Hartree
- TS: −234.551234 Hartree
- Products: −234.589012 Hartree

Calculate ΔG‡, ΔG_rxn, and predict if reaction is exergonic.

**Solution:**

1. **Electronic Energy Difference:**
   $$\Delta E^\ddagger = E_{TS} - E_{react} = −234.551234 - (−234.567890) = 0.016656 \text{ Hartree}$$
   
   $$\Delta E^\ddagger = 0.016656 \times 627.5 = 10.5 \text{ kcal/mol}$$

   $$\Delta E_{rxn} = E_{prod} - E_{react} = −234.589012 - (−234.567890) = −0.021122 \text{ Hartree}$$
   
   $$\Delta E_{rxn} = −0.021122 \times 627.5 = −13.3 \text{ kcal/mol}$$

2. **Note:** These are electronic energies. For accurate free energies, need:
   - Zero-point energy correction
   - Thermal correction (H - E)
   - Entropy contribution (TS)
   - Solvation free energy

3. **Expected corrections:**
   - ZPE typically reduces barrier by 0.5-1 kcal/mol
   - Entropy penalty for TS (~2-5 kcal/mol)
   - Total ΔG‡ ≈ 12-15 kcal/mol

4. **Prediction:**
   - Reaction is exergonic (ΔG_rxn < 0)
   - Moderate activation barrier
   - Should proceed at room temperature

---

## References and Further Reading

1. **Hammett Equation:** Hammett, L. P. *Chem. Rev.* **1935**, *17*, 125.
2. **Taft Equation:** Taft, R. W. *J. Am. Chem. Soc.* **1952**, *74*, 3120.
3. **Yukawa-Tsuno:** Yukawa, Y.; Tsuno, Y. *Bull. Chem. Soc. Jpn.* **1959**, *32*, 965.
4. **Brønsted Catalysis Law:** Brønsted, J. N. *Chem. Rev.* **1928**, *5*, 322.
5. **KIE Theory:** Bigeleisen, J.; Wolfsberg, M. *Adv. Chem. Phys.* **1958**, *1*, 15.
6. **Marcus Theory:** Marcus, R. A. *Annu. Rev. Phys. Chem.* **1964**, *15*, 155.
7. **Woodward-Hoffmann:** Woodward, R. B.; Hoffmann, R. *The Conservation of Orbital Symmetry*; 1970.
8. **Computational Methods:** Cramer, C. J. *Essentials of Computational Chemistry*, 2nd ed.; 2004.
9. **Carbocations:** Olah, G. A. *J. Org. Chem.* **2001**, *66*, 5943.
10. **Solvent Effects:** Reichardt, C.; Welton, T. *Solvents and Solvent Effects in Organic Chemistry*, 4th ed.; 2011.

---

## Cross-References

- **Pericyclic Reactions:** `pericyclic_reactions.md` (detailed FMO, correlation diagrams)
- **Advanced Pericyclic Theory:** `pericyclic_advanced.md` (correlation diagrams, group theory)
- **Reaction Mechanisms:** `reaction_mechanisms.md` (kinetics, rate laws)
- **Computational Quantum Chemistry:** `computational_quantum_chemistry.md`
- **Density Functional Theory:** `density_functional_theory.md`
- **Stereochemistry and Chirality:** `stereochemistry_chirality.md`
- **Conformational Analysis:** `conformational_analysis.md`
