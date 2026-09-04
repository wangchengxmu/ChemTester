# Photochemical Reactions

## Concept Overview

Photochemical reactions proceed via pathways unavailable thermally, accessing excited-state surfaces with distinct selectivity.

## Key Principles

### Norrish Type I (α-Cleavage)
- Ketone undergoes homolytic C–C cleavage at the α-position from carbonyl
- Produces acyl + alkyl radicals
- Common for aliphatic ketones

### Norrish Type II (Intramolecular H-Abstraction)
- γ-hydrogen abstraction by excited carbonyl oxygen (1,5-H shift)
- Forms 1,4-biradical → cleavage to enol + alkene, or cyclization to cyclobutanol

### [2+2] Photocycloaddition
- Two π-bonds form a cyclobutane ring
- Suprafacial on both reactants (allowed via excited state)
- Key step in vitamin D synthesis, Paternò-Büchi reaction

### E-Z Photoisomerization
- Rotation around C=C occurs in excited state (S₁ or T₁)
- Efficient for stilbenes, azobenzenes, retinal (vision)
- Often reversible with different λ

### Photochemical Halogenation
- Radical chain initiation by homolytic X–X bond cleavage
- Cl₂ → 2Cl· (hv)
- Differs from thermal halogenation in selectivity

### Photoreduction
- Electron transfer from donor to excited acceptor
- E.g., benzophenone + alcohol → benzpinacol via ketyl radical

## Problem-Solving Routes

1. **Identify reaction type**: From substrate and conditions, classify (Norrish, cycloaddition, isomerization)
2. **Predict regiochemistry**: Norrish II requires γ-H; Type I depends on bond dissociation energies
3. **Stereochemical outcome**: [2+2] gives suprafacial addition; E-Z depends on substitution pattern

## Links

- **L3 Tools**: `../L3_functions/photochemistry_tools.py`
- **L4 Data**: `../L4_reference/photochemistry_data.csv`
- **L5 Examples**: `../L5_examples/photochemistry_examples.md`

---

## Source Attribution: Roberts & Caserio, Ch28 (LibreTexts)
[Source: Roberts & Caserio, Basic Principles of Organic Chemistry, 2nd ed., Ch28](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Basic_Principles_of_Organic_Chemistry_(Roberts_and_Caserio)/28%3A_Photochemistry)

- Modern organic photochemistry correlates the nature of excited electronic states of molecules with the reactions they undergo.
- Spectroscopy enabled detection of transient intermediates critical to understanding photochemical mechanisms.
- Historical context: organic photochemistry was slow to develop until spectroscopic techniques matured.

## Source Attribution: Chang Ch15.2 �� Photosynthesis as Photochemistry
[Source: Physical Chemistry for the Biosciences, 15.2: Photosynthesis](https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_for_the_Biosciences_(LibreTexts)/15%3A_Photochemistry_and_Photobiology/15.02%3A_Photosynthesis)

### Key Photochemical Reactions in Photosynthesis
- **Overall reaction**: 6CO? + 12H?O �� C?H??O? + 6O? + 6H?O (light + chlorophyll)
- **Light-dependent reactions** (thylakoids):
  - Photosystem II (P680): Splits H?O �� ?O? + 2H? + 2e?; generates proton gradient �� ATP via chemiosmosis
  - Photosystem I (P700): Further excites electrons �� reduces NADP? to NADPH
  - Noncyclic photophosphorylation involves both PS I and PS II, produces ATP + NADPH
  - Cyclic photophosphorylation uses only PS I, produces only ATP
- **Light-independent reactions** (Calvin cycle, stroma):
  - CO? fixation by RuBisCO �� G3P �� glucose + regeneration of RuBP
- **Antenna complexes**: Arrays of chlorophyll and accessory pigments (carotenoids, phycocyanins) that funnel energy to reaction centers.
- **Chlorophyll a**: Primary pigment; **Chlorophyll b**: Accessory pigment absorbing different wavelengths.
- **Electromagnetic spectrum**: Visible light 380�C760 nm; shorter �� = higher energy per photon (E = hc/��).

### Key Quantitative Details
- Photosystem II: Antenna complex, P680 reaction center, O? evolution complex
- Photosystem I: P700 reaction center, ferredoxin, NADP? reductase
- Proton gradient drives ATP synthase (chemiosmotic coupling)

---

## [Source: Wikipedia, Photoredox Catalysis]
### Modern Applications of Photoredox Catalysis
- **C-H functionalization**: Direct activation of unreactive C-H bonds.
- **Cross-coupling**: Nickel/photoredox dual catalysis (Molander, MacMillan).
- **Decarboxylative couplings**: Reductive cleavage of carboxylic acids to generate radicals.
- **Atom transfer radical polymerization (ATRP)**: Photocontrolled polymer growth.
- **Trifluoromethylation**: Introduction of CF鈧?groups via photoredox.

### Mechanism Outline (Ru(bpy)鈧兟测伜):
1. Photoexcitation: Ru(bpy)鈧兟测伜 + h谓 鈫?Ru(bpy)鈧兟测伜* (MLCT state, 蟿 鈮?1 渭s)
2. Single Electron Transfer (SET) to/from substrate
3. Ground-state Ru regenerated
4. Substrate radical undergoes desired transformation
