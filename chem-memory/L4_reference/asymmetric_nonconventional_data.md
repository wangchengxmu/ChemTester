# L4: Asymmetric Nonconventional Conditions Reference Data

## Ionic Liquid Properties

| Ionic Liquid | Cation | Anion | Tm (°C) | Viscosity (cP, 25°C) | Density (g/mL) | Key Feature |
|---|---|---|---|---|---|---|
| [bmim][PF₆] | 1-Butyl-3-methylimidazolium | PF₆⁻ | 10 | 312 | 1.37 | Most widely used, hydrophobic |
| [bmim][BF₄] | [bmim]⁺ | BF₄⁻ | -81 | 219 | 1.20 | Hydrophilic, lower viscosity |
| [bmim][NTf₂] | [bmim]⁺ | NTf₂⁻ | -87 | 52 | 1.44 | Low viscosity, high stability |
| [bmim][OTf] | [bmim]⁺ | OTf⁻ | 15 | 90 | 1.30 | Moderate viscosity |
| [bmim][Cl] | [bmim]⁺ | Cl⁻ | 65 | >10000 | 1.10 | High viscosity, hydrophilic |
| [C₄C₁im][NTf₂] | 1-Butyl-2,3-dimethylimidazolium | NTf₂⁻ | ~-20 | 70 | 1.40 | Better oxidative stability |
| [C₄C₂im][PF₆] | 1-Butyl-3-ethylimidazolium | PF₆⁻ | 15 | 400 | 1.38 | Modified hydrophobicity |
| [C₄C₁im][OTf] | [C₄C₁im]⁺ | OTf⁻ | ~5 | 120 | 1.30 | Epoxide opening reactions |
| [C₄mpy][NTf₂] | N-Butyl-4-methylpyridinium | NTf₂⁻ | ~-10 | 80 | 1.35 | Pyridinium-based |
| [P₆₆₆₁₄][NTf₂] | Trihexyltetradecylphosphonium | NTf₂⁻ | <-20 | 350 | 1.05 | Very hydrophobic, phase separation |

## IL-Catalyst Recycling Performance

| Reaction | Catalyst | IL | Cycles | ee Retention | Notes |
|---|---|---|---|---|---|
| Hydrogenation (alkenes) | Rh-L-1 | [C₄C₂im][PF₆] | 5+ | Full | High ee retained |
| Diels-Alder | Cu(II)-bisox-imid | [C₄C₁im][NTf₂] | 10 | Full | No loss |
| Epoxidation | Mn(III)-salen | [C₄C₁im][PF₆] | 5 | Slight drop (~2%/cycle) | CH₂Cl₂ cosolvent |
| Epoxide opening | Cr(III)-salen | [C₄C₁im][OTf] | 5 | Good | Rate decrease |
| Hydrolytic resolution | Co(II)-salen | [C₄C₁im][PF₆] | 10 | Full | Excellent |
| Dihydroxylation | OsO₄ + ligand | [C₄C₁im][PF₆] | 3 | Full | Minimal Os leaching |
| Fluorination | Pd-BINAP | [C₄C₁im][BF₄] | 10 | Full | Scaled |

## Supercritical CO₂ (scCO₂) Conditions

| Parameter | Value | Notes |
|---|---|---|
| Critical temperature (Tc) | 31.1°C | Mild conditions |
| Critical pressure (Pc) | 73.8 bar | ~74 atm |
| Density (at 100 bar, 40°C) | ~0.6 g/mL | Tunable with P/T |
| Typical operating range | 40-80°C, 80-200 bar | Above Tc and Pc |
| Solvent power | Similar to hexane | Poor for polar substrates |
| Dielectric constant | ~1.1-1.5 | Gas-like |
| Key advantage | Solvent removal by depressurization | No solvent residue |
| Catalyst recovery | Immobilized catalyst remains after depressurization | Continuous flow possible |

## scCO₂ Applications in Asymmetric Catalysis

| Reaction | Catalyst | Product ee | Notes |
|---|---|---|---|
| Hydrogenation | Rh-BINAP | >95% | Homogeneous during reaction |
| Cyclopropanation | Chiral Ru complex | High | 7.7x more efficient than CH₂Cl₂ |

## Microwave Parameters for Common Asymmetric Reactions

| Reaction | Conventional (T, time) | Microwave (T, time) | Speedup | ee (conv vs MW) |
|---|---|---|---|---|
| Allylic alkylation (Mo) | 60°C, 2h | 120°C, 10min | 12x | Similar |
| Arylation of aldehydes | 25°C, 1h | 80°C, 15min | 4x | 98% (both) |
| Aldol (proline) | RT, 24h | 60°C, 30min | 48x | Slight drop possible |

## Green Chemistry Benchmarks

| Metric | Excellent | Good | Acceptable | Pharma Typical |
|---|---|---|---|---|
| E-factor | <5 | 5-25 | 25-50 | 25-100 |
| Atom economy | >80% | 60-80% | 40-60% | Varies widely |
| PMI | <10 | 10-50 | 50-100 | 50-500 |
| Solvent recovery | >95% | 80-95% | 50-80% | Often not recovered |
