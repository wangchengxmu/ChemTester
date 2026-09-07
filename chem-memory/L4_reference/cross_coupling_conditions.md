# Cross-Coupling Reaction Conditions — Reference Tables

> Comprehensive lookup for palladium (and Ni) cross-coupling reactions.
> Last updated: 2026-03-31

---

## Table of Contents

1. [Halide Reactivity Comparison](#1-halide-reactivity-comparison)
2. [Ligand Selection Guide](#2-ligand-selection-guide)
3. [Base Compatibility Table](#3-base-compatibility-table)
4. [Solvent Polarity Comparison](#4-solvent-polarity-comparison)
5. [Suzuki-Miyaura](#5-suzuki-miyaura)
6. [Negishi](#6-negishi)
7. [Stille](#7-stille)
8. [Heck](#8-heck)
9. [Sonogashira](#9-sonogashira)
10. [Buchwald-Hartwig](#10-buchwald-hartwig-amination)
11. [Kumada](#11-kumada)
12. [Hiyama](#12-hiyama)
13. [Carbonylative Couplings](#13-carbonylative-couplings)
14. [Troubleshooting](#14-troubleshooting-table)

---

## 1. Halide Reactivity Comparison

| Halide / Pseudohalide | Relative Rate (Pd) | Relative Rate (Ni) | C–X Bond (kJ/mol) | Cost | Stability | Notes |
|---|---|---|---|---|---|---|
| I | ★★★★★ | ★★★★★ | 213 | $ | Sensitive to light | Most reactive; prone to side reactions (reduction, homocoupling) |
| OTf | ★★★★☆ | ★★☆☆☆ | — | $$$ | Sensitive to moisture | Pseudohalide; excellent in Ni catalysis with reductive coupling |
| Br | ★★★☆☆ | ★★★★☆ | 285 | $$ | Good | Workhorse; best cost/reactivity balance |
| Cl | ★☆☆☆☆ | ★★★☆☆ | 327 | $ | Excellent | Requires electron-rich bulky phosphine ligands or NHC |
| OTs | ★☆☆☆☆ | ★★☆☆☆ | — | $$ | Good | Poor leaving group for Pd; occasional use in Ni |

**Practical rule:** Br → default starting choice. Switch to Cl for cost at scale (with appropriate ligand). Use I/OTf only when Br fails or for electron-rich substrates.

---

## 2. Ligand Selection Guide

### Phosphine Ligands

| Ligand | Cone Angle (°) | Tolman Electronic (νCO, cm⁻¹) | Pd Complexes | Ni Complexes | Best For |
|---|---|---|---|---|---|
| PPh₃ | 145 | 2068.9 | Pd(PPh₃)₄ | — | Classic Suzuki, Stille; limited for Ar-Cl |
| P(o-tol)₃ | 194 | 2056.0 | Pd₂(dba)₃/P(o-tol)₃ | NiCl₂/P(o-tol)₃ | Ar-Cl amination, Suzuki; very bulky |
| SPhos | 168 | 2054 | Pd-G3 (SPhos) | Ni-cod/SPhos | Ar-Cl Suzuki, Buchwald-Hartwig |
| XPhos | 170 | 2051 | Pd-G3 (XPhos) | Ni-cod/XPhos | Ar-Cl amination, Suzuki; extremely versatile |
| BrettPhos | 197 | 2049 | Pd-G3 (BrettPhos) | — | Primary amines, anilines; steric bulk prevents β-hydride elimination |
| RuPhos | 157 | 2059 | Pd-G3 (RuPhos) | — | Secondary amines, indoles |
| JosiPhos | 178 | 2053 | Pd-JosiPhos G3 | NiCl₂/JosiPhos | Enantioselective couplings, industrial scale |
| BINAP | 170 | 2045 | Pd₂(dba)₃/BINAP | — | Chiral couplings; electron-rich; hindered rotation |
| DavePhos | 174 | 2052 | Pd-G2 (DavePhos) | — | Heteroaryl chlorides |
| XantPhos | 177 | 2052 (average) | — | Ni/XantPhos | Wide bite angle; promotes reductive elimination |
| P(t-Bu)₃ | 182 | 2056 | Pd-OAc₂/P(t-Bu)₃ | NiCl₂/P(t-Bu)₃ | Ar-Cl, Ar-OTf; very strong σ-donor |
| PCy₃ | 170 | 2056.3 | — | Ni/PCy₃ | Ni-catalyzed couplings |
| dppe | 85 | 2062 | — | Ni/dppe | Bidentate; small bite angle |
| dtbpf | 171 | — | — | Ni/dtbpf | Ni Suzuki, Negishi |

### N-Heterocyclic Carbenes (NHCs)

| Ligand | Pd Complex | Best For | Notes |
|---|---|---|---|
| IPr (SIPr) | Pd-IPr-Cl₂ | Ar-Cl Suzuki/Buchwald-Hartwig | Strong σ-donor; air-stable complexes |
| IMes | Pd-IMes-Cl₂ | General-purpose | Less bulky than IPr |
| Pd-PEPPSI-IPr | Pd-PEPPSI-IPr | Air-stable pre-catalyst | "Pyridine-enhanced precatalyst" — no ligand addition needed |
| Pd-PEPPSI-SIPr | Pd-PEPPSI-SIPr | Ar-Cl, Ar-OTs | Even more robust than IPr |

### Quick Ligand Picker

| Problem | Use |
|---|---|
| Aryl chloride → need high activity | XPhos, SPhos, P(t-Bu)₃, BrettPhos, NHC |
| Electron-rich aryl chloride | P(o-tol)₃, XPhos, NHC |
| Heteroaryl chloride | DavePhos, XPhos, SPhos |
| Sterically hindered coupling | BrettPhos, RuPhos, P(o-tol)₃ |
| Primary amine amination | BrettPhos, XPhos |
| Secondary amine amination | RuPhos, XPhos, DavePhos |
| Low temp (≤50°C) needed | XPhos G3, SPhos G3 |
| Cheap/ligandless | Pd/C (K₃PO₄, dioxane) |
| Enantioselective | BINAP, JosiPhos, TADDOL-derived phosphoramidites |

---

## 3. Base Compatibility Table

| Base | pKₐ (H₂O) | Solubility (Organic) | Typical Use | Coupling | Notes |
|---|---|---|---|---|---|
| K₂CO₃ | 10.3 | Low | Suzuki, Heck, Stille | S, H, St | Most common; inexpensive |
| Cs₂CO₃ | 10.3 | Moderate | Suzuki, Buchwald-Hartwig, amination | S, BH | Higher solubility; excellent for BH |
| K₃PO₄ | 12.3 | Low | Suzuki, Buchwald-Hartwig | S, BH | Stronger; use in dioxane/H₂O |
| Na₂CO₃ | 10.3 | Low | Suzuki | S | Cheap alternative to K₂CO₃ |
| NaOt-Bu | 17.2 | Good | Buchwald-Hartwig, Suzuki (Ar-Cl) | BH, S | Strong; deprotonates amines; incompatible with protic groups |
| KOt-Bu | 17.2 | Good | Buchwald-Hartwig, Kumada | BH, K | Very strong; can cause E2 elimination |
| NaOMe | 15.5 | Good | Stille (with CuI) | St | Methoxide source |
| LiOH | 11.9 | Good | Suzuki (aqueous) | S | Soluble in H₂O/THF |
| NaOH | 15.7 | Good | Suzuki (aqueous) | S | Cheap; requires aqueous cosolvent |
| KF | — | Moderate | Hiyama | Hi | Fluoride source for Si activation |
| TBAF | — | Excellent | Hiyama | Hi | Soluble fluoride; expensive |
| Et₃N | 10.8 | Excellent | Sonogashira | Son | Base + solvent for Pd/Cu system |
| DIPEA | 11.4 | Excellent | Sonogashira, Buchwald-Hartwig | Son, BH | Non-nucleophilic base |
| NaHCO₃ | 6.4 | Low | Mild Suzuki | S | Very mild; for base-sensitive substrates |

---

## 4. Solvent Polarity Comparison

| Solvent | ε (dielectric) | BP (°C) | Water Miscible | Typical Couplings | Notes |
|---|---|---|---|---|---|
| DMF | 36.7 | 153 | Yes | Suzuki, Stille, Sonogashira | High polarity; hard to remove; HCONMe₂ impurity |
| DMAc | 37.8 | 165 | Yes | Buchwald-Hartwig, Suzuki | Similar to DMF; higher BP |
| DMSO | 46.7 | 189 | Yes | Suzuki | Very polar; hard to remove |
| NMP | 32.0 | 202 | Yes | Suzuki, Buchwald-Hartwig | High BP for difficult substrates |
| dioxane | 2.2 | 101 | Partial | Suzuki, Buchwald-Hartwig | Standard BH solvent (with H₂O cosolvent) |
| THF | 7.6 | 66 | Partial | Negishi, Kumada, Suzuki | Low BP → use sealed tube for >66°C |
| toluene | 2.4 | 111 | No | Buchwald-Hartwig, Suzuki | Standard high-temp organic solvent |
| MeCN | 37.5 | 82 | Yes | Sonogashira, Suzuki | Good for Pd/Cu systems |
| EtOH | 24.6 | 78 | Yes | Suzuki | Cheap; green solvent option |
| iPrOH | 18.3 | 82 | Partial | Suzuki | Less protic than EtOH |
| H₂O | 80.1 | 100 | — | Suzuki (with cosolvent) | Ideal for boronic acid solubility |
| CPME | — | 106 | No | Industrial Suzuki | Green alternative to dioxane/THF |
| 2-MeTHF | 6.9 | 80 | Partial | Suzuki, industrial | Green; derived from renewable resources |
| MTBE | 4.5 | 55 | No | Suzuki | Low BP; phase separation useful |

---

## 5. Suzuki-Miyaura

**General:** Ar–X + R–B(OH)₂ → Ar–R. The most widely used cross-coupling due to boronic acid stability, low toxicity, and wide functional group tolerance.

**Halide reactivity:** ArI > ArOTf > ArBr > ArCl > ArF (ArF generally inert except with specialized Ni systems).

**Boronic acid partners:**

| Reagent | Reactivity | Stability | Notes |
|---|---|---|---|
| B(OH)₂ | Standard | Good | Can undergo protodeboronation of electron-rich substrates |
| Bpin | Moderate | Excellent | Stable; slower transmetalation (add base + heat) |
| Bneo | Moderate | Excellent | Neopentyl glycol ester; less prone to protodeboronation |
| B(OH)₃K (potassium trifluoroborate) | Moderate | Excellent | Crystalline, stable, easy to handle; slightly lower reactivity |
| BF₃K | Moderate | Excellent | Alternative to boronic acid for sensitive substrates |
| MIDA boronate | Low | Outstanding | Protected; slow-release; orthogonal coupling |
| NHC-borane | Low | Excellent | Non-basic; orthogonal to Suzuki conditions |

### Representative Conditions

#### Condition A: Classic Miyaura (1995)

| Parameter | Value |
|---|---|
| Catalyst | Pd(PPh₃)₄ (2 mol%) |
| Base | K₂CO₃ (2.0 equiv) |
| Solvent | DME/H₂O (3:1) or THF/H₂O (3:1) |
| Temp | 80 °C |
| Substrates | ArBr + ArB(OH)₂ |
| Yield | 70–95% |
| Scope | ArI, ArBr; limited for ArCl |

#### Condition B: Buchwald Aryl Chloride (2002)

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ (3 mol%) + SPhos (6 mol%) |
| Base | K₃PO₄ (3.0 equiv) |
| Solvent | Toluene or dioxane |
| Temp | 80–100 °C |
| Substrates | ArCl + ArB(OH)₂ |
| Yield | 70–95% |
| Scope | Electron-rich/poor ArCl; heteroaryl Cl |

#### Condition C: PEPPSI Air-Stable (2006)

| Parameter | Value |
|---|---|
| Catalyst | Pd-PEPPSI-IPr (1–2 mol%) |
| Base | K₂CO₃ or Cs₂CO₃ (2 equiv) |
| Solvent | iPrOH/H₂O or t-BuOH/H₂O |
| Temp | 80 °C |
| Substrates | ArBr, ArCl + ArB(OH)₂, ArBpin |
| Yield | 75–95% |
| Scope | Broad; no need for glovebox |

#### Condition D: Green Aqueous Suzuki

| Parameter | Value |
|---|---|
| Catalyst | Pd/C (10 wt%, 2 mol% Pd) |
| Base | K₂CO₃ (2.0 equiv) |
| Solvent | EtOH/H₂O (1:1) |
| Temp | reflux (~80 °C) |
| Substrates | ArBr + ArB(OH)₂ |
| Yield | 80–95% |
| Scope | Electron-neutral/deficient; easy Pd removal by filtration |

#### Condition E: MIDA Boronate Sequential Coupling

| Parameter | Value |
|---|---|
| Catalyst | PdCl₂(dppf) (3 mol%) |
| Base | NaOH (6 M aq, 3 equiv) |
| Solvent | THF |
| Temp | 65 °C |
| Substrates | ArBr + Ar-MIDA |
| Yield | 65–90% |
| Scope | Iterative cross-coupling; late-stage diversification |

### Quick Pick

| Substrate Pair | Recommended Condition |
|---|---|
| ArBr + ArB(OH)₂ (standard) | Pd(PPh₃)₄, K₂CO₃, DME/H₂O, 80 °C |
| ArCl + ArB(OH)₂ | Pd₂(dba)₃/SPhos, K₃PO₄, toluene, 100 °C |
| ArCl + ArBpin | Pd-PEPPSI-IPr, Cs₂CO₃, iPrOH/H₂O, 80 °C |
| Heteroaryl-Br + AlkylB(OH)₂ | Pd(dppf)Cl₂, Cs₂CO₃, dioxane/H₂O, 80 °C |
| Vinyl-Br + ArB(OH)₂ | Pd(PPh₃)₄, Na₂CO₃, DMF/H₂O, 80 °C |
| Scale-up (>100 mmol) | Pd/C, K₂CO₃, EtOH/H₂O, reflux |

### Common Side Reactions

| Problem | Cause | Fix |
|---|---|---|
| Protodeboronation | Electron-rich boronic acid; high temp | Use MIDA boronate, lower temp, or KF·Al₂O₃ |
| Homocoupling (biaryl) | Oxidative homocoupling of boronic acid | Degas solvent; use inert atmosphere |
| Aryl halide reduction | Pd-hydride pathway | Ensure sufficient boronic acid (1.2 equiv); fresh Pd source |
| Dehalogenation | Excess Pd(0) / insufficient boronic acid | Use correct stoichiometry; limit Pd loading |
| Boronic acid anhydride formation | Loss of water | Add molecular sieves or use Bpin instead |

---

## 6. Negishi

**General:** Ar–X + R–ZnX → Ar–R. Organozinc reagents offer excellent chemoselectivity and functional group tolerance. Mild basicity avoids protic incompatibilities.

### Representative Conditions

#### Condition A: Classic Negishi (1977)

| Parameter | Value |
|---|---|
| Catalyst | Pd(PPh₃)₄ (2–5 mol%) |
| Solvent | THF |
| Temp | 25–65 °C (often RT) |
| Substrates | ArI, ArBr + RZnCl |
| Yield | 60–90% |
| Notes | RZnCl prepared from R–X + Zn (activated) or R–MgX + ZnCl₂ |

#### Condition B: Modern Pd-PEPPSI (Ni Compatible)

| Parameter | Value |
|---|---|
| Catalyst | Pd-PEPPSI-IPr (2 mol%) |
| Solvent | THF or NMP |
| Temp | 50 °C |
| Substrates | ArBr, ArCl + RZnCl (alkyl, aryl, vinyl) |
| Yield | 70–95% |
| Notes | Tolerates esters, nitriles, ketones |

#### Condition C: Ni-Catalyzed (ArCl)

| Parameter | Value |
|---|---|
| Catalyst | NiCl₂(dppp) (5 mol%) |
| Solvent | THF |
| Temp | 60 °C |
| Substrates | ArCl + RZnCl |
| Yield | 60–85% |
| Notes | Cheaper than Pd; sensitive to β-hydride elimination in alkyl zinc |

### Chemoselectivity Notes

- Organozinc reagents tolerate: esters, nitriles, amides, aldehydes, ketones, halides
- **Incompatible with:** acidic protons (OH, NH, CO₂H), epoxides (ring opening)
- Transmetalation slower than Stille; competitive with Suzuki
- **Advantage over Grignard:** no uncontrolled nucleophilicity; can carry electrophilic functional groups

### Quick Pick

| Substrate Pair | Recommended |
|---|---|
| ArBr + ArZnCl | Pd(PPh₃)₄, THF, RT |
| ArBr + AlkylZnCl | Pd-PEPPSI-IPr, THF, 50 °C |
| ArCl + ArZnCl | NiCl₂(dppp), THF, 60 °C |
| Vinyl-Br + AlkylZnCl | Pd(PPh₃)₄, THF, 0 °C → RT |

---

## 7. Stille

**General:** Ar–X + R–SnBu₃ → Ar–R. Organostannanes are remarkably stable and tolerate diverse functional groups, but tin toxicity is a serious concern.

### Representative Conditions

#### Condition A: Classic Stille (Farina)

| Parameter | Value |
|---|---|
| Catalyst | Pd(PPh₃)₄ (2–5 mol%) |
| Solvent | DMF or toluene |
| Temp | 80–110 °C |
| Substrates | ArI, ArBr, Vinyl-X + RSnBu₃ |
| Yield | 70–95% |
| Notes | Add CuI (5 mol%) for vinyl stannanes |

#### Condition B: Fu's Low-Temp Stille

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ + AsPh₃ or P(t-Bu)₃ |
| Solvent | DMF |
| Temp | 0–25 °C |
| Substrates | ArBr + VinylSnBu₃ |
| Yield | 80–95% |
| Notes | Enables coupling of base-sensitive substrates |

#### Condition C: LiCl Accelerated

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ (2.5 mol%) + P(2-furyl)₃ (10 mol%) |
| Additive | LiCl (2–5 equiv) |
| Solvent | NMP or DMF |
| Temp | 60–80 °C |
| Substrates | ArBr, ArCl + RSnBu₃ |
| Yield | 75–95% |
| Notes | LiCl accelerates transmetalation by forming hypervalent tin ate complexes |

### Toxicity & Handling

| Hazard | Detail |
|---|---|
| Organotin toxicity | Highly toxic; accumulates in body; avoid skin contact |
| Stannane byproducts | Difficult to remove; use Florisil chromatography or KF wash |
| Disposal | Segregate tin-containing waste; do not pour down drain |
| Alternative | Replace with Suzuki where possible (much safer) |

### Quick Pick

| Substrate Pair | Recommended |
|---|---|
| ArBr + VinylSnBu₃ | Pd(PPh₃)₄, CuI, DMF, 80 °C |
| ArI + ArSnBu₃ | Pd(PPh₃)₄, toluene, 110 °C |
| ArCl + RSnBu₃ | Pd₂(dba)₃/P(t-Bu)₃, LiCl, NMP, 80 °C |
| Base-sensitive substrate | Fu's conditions (Pd₂(dba)₃/P(t-Bu)₃, DMF, 0 °C) |

---

## 8. Heck

**General:** Ar–X + CH₂=CH–R → Ar–CH=CH–R. Forms substituted alkenes via arylation. Regioselectivity governed by β-H elimination.

### Regioselectivity

| Product | Condition | Selectivity |
|---|---|---|
| **β-H elimination (branched)** | Electron-rich alkene, coordinating directing group | Typically minor |
| **β-H' elimination (linear)** | Standard conditions | Major (>95% for acrylates, styrenes) |
| **Internal alkenes** | More complex; mixture possible | Requires specific conditions |

### Representative Conditions

#### Condition A: Classic Heck (1972)

| Parameter | Value |
|---|---|
| Catalyst | Pd(OAc)₂ (1–5 mol%) + PPh₃ (4–10 mol%) |
| Base | Et₃N or K₂CO₃ (2 equiv) |
| Solvent | DMF or MeCN |
| Temp | 100 °C |
| Substrates | ArI, ArBr + CH₂=CH–R (styrenes, acrylates) |
| Yield | 60–90% |
| Notes | E-selectivity predominant |

#### Condition B: Herrmann's Palladacycle (1993)

| Parameter | Value |
|---|---|
| Catalyst | Herrmann's palladacycle (0.5–2 mol%) |
| Base | NaOAc (2 equiv) |
| Solvent | DMF or NMP |
| Temp | 120–140 °C |
| Substrates | ArBr, ArCl + alkenes |
| Yield | 70–95% |
| Notes | Air-stable precatalyst; works with ArCl |

#### Condition C: Ligandless / Pd(OAc)₂

| Parameter | Value |
|---|---|
| Catalyst | Pd(OAc)₂ (0.5–2 mol%) |
| Base | Et₃N (excess as solvent) or K₂CO₃ |
| Solvent | DMF |
| Temp | 100–120 °C |
| Substrates | ArI, ArBr + acrylates |
| Yield | 75–95% |
| Notes | Simplest conditions; Pd black formation risk |

#### Condition D: Tandem Heck–Hydrogenation

| Parameter | Value |
|---|---|
| Catalyst | Pd(OAc)₂ (5 mol%) |
| Additive | HCO₂H / Et₃N (5:2, azeotrope) |
| Solvent | DMF |
| Temp | 100 °C |
| Substrates | ArI + alkene |
| Yield | 70–85% (saturated) |
| Notes | Heck coupling followed by in situ reduction to alkyl product |

### Quick Pick

| Substrate Pair | Recommended |
|---|---|
| ArI + n-butyl acrylate | Pd(OAc)₂, Et₃N, DMF, 100 °C |
| ArBr + styrene | Pd(OAc)₂, PPh₃, K₂CO₃, DMF, 100 °C |
| ArCl + acrylate | Herrmann's palladacycle, NaOAc, DMF, 140 °C |
| Electron-rich ArBr + acrylate | Pd(OAc)₂, P(o-tol)₃, K₃PO₄, DMF, 100 °C |

---

## 9. Sonogashira

**General:** Ar–X + H–C≡C–R → Ar–C≡C–R. Terminal alkynes coupled to (pseudo)halides using Pd/Cu dual catalysis. Also applicable in Cu-free variants for base-sensitive substrates.

### Representative Conditions

#### Condition A: Classic Sonogashira (1975)

| Parameter | Value |
|---|---|
| Catalyst | Pd(PPh₃)₂Cl₂ (2–5 mol%) + CuI (5 mol%) |
| Base | Et₃N (excess, as solvent) or iPr₂NH |
| Solvent | Et₃N or THF/Et₃N |
| Temp | RT to 80 °C |
| Substrates | ArI, ArBr + terminal alkynes |
| Yield | 60–90% |
| Notes | CuI activates alkyne; Glaser homocoupling side reaction possible |

#### Condition B: Cu-Free Sonogashira

| Parameter | Value |
|---|---|
| Catalyst | Pd(PPh₃)₄ (5 mol%) |
| Base | Et₃N or DIPEA (2–3 equiv) |
| Solvent | THF or MeCN |
| Temp | 60–80 °C |
| Substrates | ArI, ArBr + terminal alkynes |
| Yield | 60–85% |
| Notes | Avoids Glaser homocoupling; slightly slower; use for Cu-sensitive substrates |

#### Condition C: Aryl Chloride (Modern)

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ (2 mol%) + XPhos (4 mol%) + CuI (4 mol%) |
| Base | Cs₂CO₃ (2 equiv) |
| Solvent | Dioxane |
| Temp | 100 °C |
| Substrates | ArCl + terminal alkynes |
| Yield | 65–90% |
| Notes | Bulky phosphine enables ArCl reactivity |

#### Condition D: Aqueous / Green

| Parameter | Value |
|---|---|
| Catalyst | PdCl₂(PPh₃)₂ (1 mol%) + CuI (2 mol%) |
| Base | K₂CO₃ (2 equiv) |
| Solvent | DMF/H₂O (4:1) |
| Temp | 80 °C |
| Substrates | ArBr + alkynes |
| Yield | 75–95% |
| Notes | Environmentally milder; water assists in alkyne deprotonation |

### Alkyne Protection/Deprotection

| Protecting Group | Conditions for Coupling | Deprotection |
|---|---|---|
| TMS (trimethylsilyl) | Requires TBAF or K₂CO₃/MeOH for in situ deprotection; or pre-deprotect | TBAF (THF) or K₂CO₃/MeOH |
| TIPS (triisopropylsilyl) | Often coupled directly (TIPS-acetylene + ArBr) | TBAF (longer time) |
| TES (triethylsilyl) | Direct coupling possible | TBAF |
| **Unprotected** | Standard conditions (Et₃N base) | N/A — preferred when possible |

### Quick Pick

| Substrate Pair | Recommended |
|---|---|
| ArI + TMS-acetylene | Pd(PPh₃)₂Cl₂, CuI, Et₃N, RT → then TBAF |
| ArBr + terminal alkyne | Pd(PPh₃)₂Cl₂, CuI, Et₃N, 60 °C |
| ArCl + terminal alkyne | Pd₂(dba)₃/XPhos, CuI, Cs₂CO₃, dioxane, 100 °C |
| Cu-sensitive alkyne | Cu-free: Pd(PPh₃)₄, DIPEA, THF, 60 °C |
| Heteroaryl-Br + alkyne | Pd(PPh₃)₂Cl₂, CuI, Et₃N, 50–80 °C |

---

## 10. Buchwald-Hartwig Amination

**General:** Ar–X + HNR₂ → Ar–NR₂. One of the most impactful modern cross-couplings. Enabling C–N bond formation for pharmaceuticals, materials, and natural products.

**Key variables:** substrate type (1° vs 2° amine vs aniline vs amide), halide (Br vs Cl), ligand choice (dominant variable).

### Representative Conditions

#### Condition A: Classic Buchwald-Hartwig (BINAP, 1995)

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ (2–3 mol%) + BINAP (4–6 mol%) |
| Base | NaOt-Bu (1.5 equiv) |
| Solvent | Toluene |
| Temp | 80–100 °C |
| Substrates | ArBr + 1°/2° amines, anilines |
| Yield | 60–85% |
| Notes | Foundational conditions; limited for ArCl |

#### Condition B: XPhos G3 (BrettPhos for 1° Amines)

| Parameter | Value |
|---|---|
| Catalyst | Pd-G3 XPhos (1–2 mol%) |
| Base | NaOt-Bu (1.5 equiv) |
| Solvent | t-BuOH or dioxane |
| Temp | 100 °C |
| Substrates | ArCl, ArBr + 2° amines |
| Yield | 80–98% |
| Notes | BrettPhos G3 for 1° amines (less β-H elimination) |

#### Condition C: RuPhos G3 (Secondary Amines)

| Parameter | Value |
|---|---|
| Catalyst | Pd-G3 RuPhos (1–2 mol%) |
| Base | NaOt-Bu (1.5 equiv) |
| Solvent | t-BuOH |
| Temp | 100 °C |
| Substrates | ArCl, ArBr + 2° cyclic amines (pyrrolidine, piperidine, morpholine) |
| Yield | 80–98% |
| Notes | Optimized for 2° amines |

#### Condition D: Aniline Coupling (DavePhos)

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ (2 mol%) + DavePhos (4 mol%) |
| Base | NaOt-Bu (1.2 equiv) |
| Solvent | Toluene |
| Temp | 100 °C |
| Substrates | ArBr, ArCl + anilines |
| Yield | 70–95% |
| Notes | Less nucleophilic NH₂ requires optimized conditions |

#### Condition E: Amide C–N Coupling (BrettPhos)

| Parameter | Value |
|---|---|
| Catalyst | Pd-G3 BrettPhos (1–3 mol%) |
| Base | Cs₂CO₃ (1.5 equiv) |
| Solvent | t-BuOH |
| Temp | 100 °C |
| Substrates | ArCl, ArBr + amides (primary) |
| Yield | 50–85% |
| Notes | Amide NH coupling; lower yields than amine coupling |

### Quick Pick

| Substrate Pair | Ligand / Conditions |
|---|---|
| ArBr + 1° alkyl amine | BrettPhos G3, NaOt-Bu, t-BuOH, 100 °C |
| ArBr + 2° amine (pyrrolidine) | RuPhos G3, NaOt-Bu, t-BuOH, 100 °C |
| ArCl + 1° amine | BrettPhos G3 or XPhos G3, NaOt-Bu, 100 °C |
| ArCl + 2° amine | XPhos G3, NaOt-Bu, t-BuOH, 100 °C |
| ArBr + aniline | DavePhos or XPhos, NaOt-Bu, toluene, 100 °C |
| ArCl + amide | BrettPhos G3, Cs₂CO₃, t-BuOH, 100 °C |
| Heteroaryl-Cl + 2° amine | XPhos or JosiPhos, NaOt-Bu, dioxane, 100 °C |

---

## 11. Kumada

**General:** Ar–X + R–MgX → Ar–R. The first cross-coupling (1972). Grignard reagents are cheap and reactive, but functional group tolerance is limited.

### Representative Conditions

#### Condition A: Classic Kumada (1972)

| Parameter | Value |
|---|---|
| Catalyst | NiCl₂(dppp) (1–3 mol%) or PdCl₂(dppf) |
| Solvent | THF |
| Temp | 0 °C → RT |
| Substrates | ArBr, ArI + RMgX |
| Yield | 60–90% |
| Notes | Ni preferred for cost and speed; Pd for selectivity |

#### Condition B: Kumada with Chemoselective Ligand

| Parameter | Value |
|---|---|
| Catalyst | NiCl₂(PPh₃)₂ (2 mol%) |
| Solvent | THF |
| Temp | 0 °C |
| Substrates | ArCl + RMgX (aryl, vinyl) |
| Yield | 50–85% |
| Notes | Limited functional group tolerance due to reactive Grignard |

### Chemoselectivity Challenges

| Functional Group | Tolerated? | Notes |
|---|---|---|
| Ester | ❌ (attacked by RMgX) | Transmetalation outcompetes ester addition only for hindered systems |
| Ketone | ❌ | Same as ester |
| Nitrile | ❌ | Nucleophilic addition |
| Aldehyde | ❌ | Nucleophilic addition |
| Ether | ✅ | Generally tolerated |
| Halide (Cl on ring, not coupling site) | ⚠️ | Competes; use lower temp |
| CF₃ | ✅ | Stable |
| Nitro | ⚠️ | May be reduced by Ni |

**Bottom line:** Use Kumada only when the Grignard is commercially available and the substrate has no electrophilic groups. Otherwise, use Negishi or Suzuki.

### Quick Pick

| Substrate Pair | Recommended |
|---|---|
| ArBr + PhMgBr | NiCl₂(dppp), THF, 0 °C → RT |
| Vinyl-Br + AlkylMgBr | NiCl₂(dppp), THF, 0 °C |
| ArCl + PhMgBr | NiCl₂(dppp) or Pd(PPh₃)₄, THF, RT |

---

## 12. Hiyama

**General:** Ar–X + R–Si(OR)₃ → Ar–R (with fluoride activation). Organosilicon reagents are non-toxic, air-stable, and inexpensive.

### Representative Conditions

#### Condition A: Classic Hiyama (Hatanaka–Hiyama, 1991)

| Parameter | Value |
|---|---|
| Catalyst | Pd(PPh₃)₄ (3–5 mol%) |
| Activator | TBAF (3 equiv) or KF (3 equiv) |
| Solvent | THF |
| Temp | 60–80 °C |
| Substrates | ArI, ArBr + R–Si(OMe)₃ (vinyl, aryl) |
| Yield | 50–80% |
| Notes | Fluoride activates silicon via pentacoordinate silicate |

#### Condition B: Denmark's Asymmetric Hiyama

| Parameter | Value |
|---|---|
| Catalyst | Pd₂(dba)₃ + chiral phosphoramidite ligand |
| Activator | TBAF (1.5 equiv) |
| Solvent | THF |
| Temp | -20 °C → RT |
| Substrates | ArBr + vinylsilane |
| Yield | 50–85%, up to 95% ee |
| Notes | Asymmetric variant |

#### Condition C: CuF-Mediated (Hiyama–Denmark)

| Parameter | Value |
|---|---|
| Catalyst | CuF·2MeOH (10 mol%) |
| Activator | (self-activating) |
| Solvent | DMF |
| Temp | 80 °C |
| Substrates | ArI + vinylsilane |
| Yield | 60–80% |
| Notes | Copper-mediated; no palladium needed |

### Silicon Reagent Types

| Reagent | Activation | Reactivity | Notes |
|---|---|---|---|
| R–Si(OMe)₃ (trimethoxysilane) | F⁻ (TBAF, KF) | Moderate | Classic Hiyama substrate |
| R–SiCl₃ | F⁻ | Moderate | More reactive, but moisture-sensitive |
| R–SiMe₃ | F⁻ + Cu or Pd | Low | Least reactive; requires harsher conditions |
| R–Si(OH)₃ | F⁻ | Moderate | Stable alternative to trialkoxysilanes |
| Aryl-H (direct C–H silylation then coupling) | Multistep | — | Sequential approach |

### Quick Pick

| Substrate Pair | Recommended |
|---|---|
| ArI + VinylSi(OMe)₃ | Pd(PPh₃)₄, TBAF, THF, 60 °C |
| ArBr + ArSi(OMe)₃ | Pd(dppf)Cl₂, KF, DMF, 80 °C |
| Vinyl-Br + ArSiMe₃ | Pd(PPh₃)₄, CuF, DMF, 80 °C |

---

## 13. Carbonylative Couplings

**General:** CO insertion into cross-coupling to form ketones, esters, or amides. Requires CO gas (or surrogate).

### CO Surrogates (when CO gas is unavailable)

| Surrogate | Conditions | Notes |
|---|---|---|
| Mo(CO)₆ | 150 °C, slow CO release | Thermal decomposition releases CO |
| 9-Methylfluorene-9-carbonyl chloride | Pd cat., 80 °C | Liquid surrogate; easy handling |
| Formic acid derivatives | HCO₂H/Et₃N | Also serves as hydrogen source |
| N-formylsaccharin | Pd cat., 80–100 °C | Solid; shelf-stable CO source |
| CO gas (balloon) | 1 atm | Standard; requires fume hood |

### Carbonylative Suzuki → Diaryl Ketones

| Parameter | Value |
|---|---|
| Catalyst | Pd(dppf)Cl₂ (3 mol%) |
| Base | K₂CO₃ (2 equiv) |
| CO source | CO (balloon, 1 atm) |
| Solvent | Toluene/H₂O (4:1) |
| Temp | 100 °C |
| Substrates | ArBr + ArB(OH)₂ |
| Yield | 50–85% |
| Notes | Competes with direct Suzuki; control CO pressure carefully |

### Carbonylative Sonogashira → Ynones

| Parameter | Value |
|---|---|
| Catalyst | PdCl₂(PPh₃)₂ (5 mol%) + CuI (5 mol%) |
| Base | Et₃N |
| CO source | CO (balloon) |
| Solvent | MeCN or THF |
| Temp | 60–80 °C |
| Substrates | ArI, ArBr + terminal alkyne |
| Yield | 50–80% |
| Notes | Useful ynones; Glaser homocoupling competes |

### Carbonylative Heck → α,β-Unsaturated Ketones

| Parameter | Value |
|---|---|
| Catalyst | Pd(OAc)₂ (5 mol%) + PPh₃ (10 mol%) |
| Base | Et₃N |
| CO source | CO (balloon) |
| Solvent | DMF |
| Temp | 100 °C |
| Substrates | ArI + alkene |
| Yield | 40–70% |
| Notes | Lower yields than standard Heck; CO coordination slows cycle |

### Carbonylative Aminocarbonylation → Amides

| Parameter | Value |
|---|---|
| Catalyst | Pd(OAc)₂ (2 mol%) + XantPhos (4 mol%) |
| Base | DIPEA (2 equiv) |
| CO source | CO (balloon) or Mo(CO)₆ |
| Solvent | Toluene |
| Temp | 100 °C |
| Substrates | ArI, ArBr + amine |
| Yield | 60–90% |
| Notes | Wide bite angle ligand (XantPhos) promotes CO insertion |

### Quick Pick

| Target | Conditions |
|---|---|
| Diaryl ketone | Pd(dppf)Cl₂, K₂CO₃, CO (1 atm), toluene/H₂O, 100 °C |
| Ynone | PdCl₂(PPh₃)₂, CuI, Et₃N, CO (1 atm), MeCN, 60 °C |
| α,β-Unsaturated ketone | Pd(OAc)₂, PPh₃, Et₃N, CO, DMF, 100 °C |
| Aryl amide | Pd(OAc)₂, XantPhos, DIPEA, CO, toluene, 100 °C |

---

## 14. Troubleshooting Table

| Symptom | Likely Cause | Solution |
|---|---|---|
| **No reaction** | Inert atmosphere compromised; Pd source inactive; wrong ligand | Degas solvents; use fresh Pd; verify ligand matches substrate |
| **Low conversion (<50%)** | Deactivated Pd; insufficient temp; wrong halide | Increase temp; use sealed tube; switch to more reactive halide (Br → I); increase Pd loading |
| **Homocoupling of nucleophile** | Oxidative conditions; Cu contamination | Degas rigorously; use inert atmosphere; add reductant (e.g., excess nucleophile); remove Cu |
| **Dehalogenated starting material** | Pd-hydride pathway; excess Pd(0); β-H elimination | Reduce Pd loading; ensure sufficient nucleophile (1.2–1.5 equiv); use bidentate ligand |
| **Protodeboronation (Suzuki)** | Electron-rich boronic acid; high temp; aqueous conditions | Lower temp; use Bpin or BF₃K; use MIDA boronate; reduce water |
| **β-Hydride elimination (Negishi, Kumada)** | Alkyl metal reagent with β-hydrogens | Use secondary/primary alkyl without β-H; use bulky ligand; switch to Suzuki |
| **Glaser homocoupling (Sonogashira)** | Cu(I) oxidation to Cu(II) | Degas; reduce Cu loading; try Cu-free conditions; add reductant |
| **E/Z mixture (Heck, Sonogashira)** | Non-selective β-elimination or cis-trans isomerization | Optimize ligand; lower temp; use coordinating directing group |
| **Ligand decomposition** | High temp; air exposure | Use air-stable precatalysts (Pd-G3, PEPPSI); lower temp; better degassing |
| **Palladium black (precipitation)** | Insufficient ligand; high temp; no stabilizer | Increase ligand:Pd ratio; use PPh₃ or stabilizing ligand; reduce temp |
| **Aryl chloride inactivity** | Insufficient ligand/electronic activation | Switch to XPhos/SPhos/P(t-Bu)₃/NHC; increase temp to 100–120 °C |
| **Heteroaryl substrate decomposition** | Coordination to Pd/Ni deactivates catalyst | Add catalytic CuI; use more electron-rich ligand; switch to Ni catalysis |
| **Amine oxidation (Buchwald-Hartwig)** | Excessive Pd, air | Use lower Pd loading; rigorously degas; use G3 precatalyst |
| **Tin residue (Stille)** | Incomplete removal | KF wash (aq); Florisil column; recrystallization |
| **CO insertion not occurring (carbonylative)** | Insufficient CO; wrong ligand | Verify CO delivery; use wide-bite-angle ligand (XantPhos); increase CO pressure |
| **Multiple products** | Competing pathways (e.g., direct coupling vs carbonylative) | Optimize CO pressure; change Pd:ligand ratio; use selective conditions |

---

## Quick Reference: Choosing a Coupling Reaction

| If you need to couple... | Use... | Because... |
|---|---|---|
| Ar–X + Ar–B(OH)₂ | **Suzuki** | Low toxicity; water-tolerant; broad scope |
| Ar–X + Ar–ZnX | **Negishi** | Chemoselective; tolerates esters, nitriles |
| Ar–X + Ar–SnBu₃ | **Stille** | Very stable stannanes; but toxic tin waste |
| Ar–X + alkene | **Heck** | Direct alkene arylation |
| Ar–X + alkyne | **Sonogashira** | Alkyne arylation; versatile alkyne handles |
| Ar–X + amine | **Buchwald-Hartwig** | C–N bond formation; pharmaceutical importance |
| Ar–X + Grignard | **Kumada** | Cheap; limited functional group tolerance |
| Ar–X + organosilicon | **Hiyama** | Non-toxic; fluoride activation required |
| Ar–X + nucleophile + CO | **Carbonylative** | Ketone/amide/ynone synthesis |

---

*This reference covers conditions current as of 2026. For latest developments, consult primary literature (ACS Catal., J. Am. Chem. Soc., Angew. Chem.) and protocol databases (Organic Syntheses, SciFinder).*
