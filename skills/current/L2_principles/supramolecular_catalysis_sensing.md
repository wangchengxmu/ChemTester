# Supramolecular Catalysis & Sensing

## Concept Overview
Supramolecular catalysis uses non-covalent interactions to accelerate reactions, while supramolecular sensing exploits host-guest recognition for detection.

## Key Principles

### Supramolecular Enzyme Mimics
Artificial hosts that mimic enzymatic:
- **Substrate binding** (recognition)
- **Transition state stabilization**
- **Microenvironment effects** (hydrophobic, electrostatic)

### Catalysis Mechanisms
1. **Substrate preorganization**: Host brings reactants into proximity/orientation
2. **Transition state binding**: Host preferentially stabilizes the TS
3. **Microenvironment modulation**: Local polarity, pH, metal ion delivery
4. **Product release**: Weak binding ensures turnover

### Key Catalytic Systems
| Host | Reaction Type | Rate Enhancement |
|------|--------------|-----------------|
| Cyclodextrin | Hydrolysis of activated esters | 10-10â´Ã— |
| Crown ethers | Nucleophilic substitution (anion activation) | 10Â²-10Â³Ã— |
| Cucurbiturils | 1,3-dipolar cycloadditions | 10Â²Ã— |
| Metalloporphyrin cages | Oxidation, epoxidation | 10Â²-10Â³Ã— |
| Self-assembled capsules | Diels-Alder, photochemistry | 10Â²-10âµÃ— |

### Supramolecular Catalysis Kinetics
```
E + S â‡Œ ES â†’ E + P
Michaelis-Menten: v = V_max[S]/(K_M + [S])
Turnover frequency (TOF) = k_cat = V_max/[E]_total
```

### Anion Recognition
Anions are harder to bind than cations (larger, more solvated, diverse geometries):
| Anion geometry | Example binders |
|---------------|----------------|
| Spherical | Guanidinium, urea, pyrrole |
| Tetrahedral | Amide, sulfonamide |
| Octahedral | Metal complexes |
| Planar | Calixpyrroles, selenoureas |

### Cation Recognition
- Crown ethers and cryptands (alkali/alkaline earth)
- Calixarenes (alkali, transition metals)
- Siderophores (FeÂ³âº, high affinity Ka > 10Â³â°)

### Fluorescent Sensing
```
PET (Photoinduced Electron Transfer):
  Host bound â†’ PET blocked â†’ fluorescence ON
  Host unbound â†’ PET active â†’ fluorescence OFF

FRET (FÃ¶rster Resonance Energy Transfer):
  Proximity-dependent energy transfer between donor-acceptor pair

ICT (Intramolecular Charge Transfer):
  Guest binding shifts absorption/emission wavelength
```

### Molecular Switches
Reversible switching between two states via external stimulus:
- **FRET-based**: Distance change modulates energy transfer
- **Colorimetric**: Visual detection (e.g., calixarene + metal ion)
- **Chiroptical**: CD signal changes upon binding

## L3 Tools
-> `../L3_functions/supramolecular_tools.py` â€” `binding_constant_calc()`

## L4 Reference
-> `../L4_reference/supramolecular_data.csv`

## L5 Examples
-> `../L5_examples/supramolecular_examples.md` â€” Example 5

## L3 Tool Call Directives

**Source:** supramolecular_tools.py
Host-guest binding, self-assembly, template-directed synthesis, cage yields.

### Available functions:
- inding_constant_calc(delta_G=None, delta_H=None, delta_S=None, temperature=298.15, K=None, mode='G_to_K') ¡ú Dict ¡ª Convert K?¦¤G?¦¤H/¦¤S; modes: G_to_K, K_to_G, HS_to_K, K_to_HS
- host_guest_stoichiometry(host_conc, guest_conc, K, stoichiometry=1, iterations=1000) ¡ú Dict ¡ª Equilibrium concs, fraction bound
- self_assembly_cmc(tail_carbon, headgroup_area, temperature=298.15, units='M') ¡ú Dict ¡ª CMC, packing parameter, aggregate type
- otaxane_efficiency(with_template_yield, without_template_yield) ¡ú Dict ¡ª Template amplification factor
- cage_yield_calc(aldehyde_conc, amine_conc, stoich_aldehyde, stoich_amine, observed_yield, target_mass, mw_cage) ¡ú Dict ¡ª Limiting reagent, theoretical/actual yield

### Common errors:
- ? delta_S must be in J/(mol¡¤K), not kJ/(mol¡¤K) in binding_constant_calc
- ? host_guest_stoichiometry currently only supports 1:1 stoichiometry analytically
