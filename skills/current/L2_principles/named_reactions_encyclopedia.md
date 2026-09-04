---
id: organic.named_reactions
layer: 2
title: Named Reactions Encyclopedia
up_links:
  - ../L1_ontology/organic_chemistry.md
down_links:
  - - `../L3_functions/reaction_sequence_tracker.py` — predict_product(), identify_reaction_type()
  - - `../L3_functions/retrosynthesis_tools.py` — forward_reaction_predict()
  - - `../L3_functions/rdkit_structure_tools.py` — aromatic_substitution_planner()
  - ../L3_functions/organic_chemistry_tools.py
---

# Named Reactions Encyclopedia

> Practical decision-support reference for predicting products, selectivity, and avoiding common errors. PhD-level coverage of 52 named reactions.

---

## 1. Diels-Alder Reaction

**One-line:** [4+2] cycloaddition forming a six-membered ring from a conjugated diene and a dienophile.

**General equation:** Diene + Dienophile → Cyclohexene derivative

**Mechanism summary:**
- Concerted pericyclic reaction (no intermediates)
- Suprafacial on both components; symmetry-allowed thermally
- Endo rule: TS favors approach where dienophile EWGs overlap with diene π system
- One-step, stereospecific — all stereochemistry of dienophile preserved

**Regioselectivity:** EWG on dienophile orients para to EDG on diene. Both unsymmetrically substituted → follow maximum secondary orbital overlap.

**Stereoselectivity:** Endo (kinetic) preferred over exo (thermodynamic). Cis-dienophile → cis-substituents; trans → trans. Stereospecific.

**Common variations:** Hetero-Diels-Alder (O/N in components); inverse electron-demand DA; intramolecular DA.

**Typical exam traps:** Assuming only one product (endo+exo); wrong stereochemistry assignment; forgetting furan as diene gives reversible adducts.

---

## 2. Aldol Reaction

**One-line:** Enolate of one carbonyl attacks another carbonyl, forming a β-hydroxy carbonyl (may dehydrate to enone).

**General equation:** RCHO + R'CHO —(base/acid)→ RCH(OH)CH(R')CHO →(−H₂O)→ RCH=CR'CHO

**Mechanism summary:**
- Base: enolate formation → nucleophilic addition → protonation → optional E1cb dehydration
- Acid: enol formation → protonated carbonyl attack → deprotonation → E1 dehydration

**Regioselectivity:** Kinetic (LDA, −78°C) → less substituted enolate. Thermodynamic (stronger base, higher T) → more substituted. Crossed aldol: one partner must lack α-H or use pre-formed enolate.

**Stereoselectivity:** Zimmerman-Traxler chair TS: Z-enolates → anti product; E-enolates → syn product. Chelation vs non-chelation reverses facial selectivity.

**Common variations:** Evans aldol (oxazolidinone auxiliary); Mukaiyama aldol (silyl enol ether + Lewis acid); directed aldol (boron enolates).

**Typical exam traps:** Self-aldol in crossed reactions; confusing anti/syn with enolate geometry; assuming esters/ketones/amides have same kinetic/thermodynamic preferences.

---

## 3. Claisen Condensation

**One-line:** Two esters under base give a β-keto ester (ester analog of aldol).

**General equation:** 2 RCH₂COOR' + base → RCH₂COCH(R)COOR' + R'OH

**Mechanism summary:** Deprotonation → enolate → attack on second ester carbonyl → eliminate alkoxide → β-keto ester. Product pKa ~11 drives completion.

**Regioselectivity:** Crossed Claisen requires one ester with no α-H. Otherwise pre-form enolate with LDA.

**Stereoselectivity:** Not stereoselective without chiral auxiliaries.

**Common variations:** Dieckmann condensation (intramolecular → cyclic β-keto ester); Stork enamine acylation; Claisen-Schmidt (aromatic aldehyde + aliphatic ketone).

**Typical exam traps:** Forgetting product is more acidic than starting material (driving force); crossed Claisen with two α-H esters gives polymers; confusing with Claisen rearrangement.

---

## 4. Michael Addition

**One-line:** 1,4-addition of a nucleophile to an α,β-unsaturated carbonyl, forming a new C–C bond at the β-position.

**General equation:** NuH + CH₂=CHC(O)R → NuCH₂CH₂C(O)R

**Mechanism summary:** Nucleophile attacks β-carbon → enolate intermediate → protonation.

**Regioselectivity:** Soft nucleophiles (enolates, cuprates) → 1,4. Hard nucleophiles (RMgX, RLi) → 1,2. Aldehydes favor 1,2; esters/amides favor 1,4.

**Stereoselectivity:** Enolate geometry controls new stereocenter. Organocatalytic proline derivatives give high ee.

**Common variations:** Robinson annulation (Michael + aldol); cuprate conjugate addition; Stork enamine Michael.

**Typical exam traps:** Assuming Grignards give 1,4 (they give 1,2!); not recognizing nitroalkenes/enones as Michael acceptors.

---

## 5. Grignard Reaction

**One-line:** Organomagnesium halide (RMgX) adds to carbonyls as a carbon nucleophile.

**General equation:** RMgX + R'R''C=O → RR'R''COH (after H₃O⁺)

**Mechanism summary:** Mg coordinates to carbonyl O → C–C bond formation → acidic workup releases alcohol.

**Regioselectivity:** Reacts with aldehydes, ketones, esters (×2), acid chlorides (×2), epoxides (less sub C), CO₂ → carboxylic acid. Does NOT react with isolated alkenes/arenes.

**Stereoselectivity:** Felkin-Anh model: nucleophile approaches from less hindered side. Chelation control reverses.

**Common variations:** Organolithium (more reactive); CeCl₃+RLi (milder); Grignard+CO₂ (carboxylic acid).

**Typical exam traps:** Esters react TWICE → tertiary alcohol; no protic solvents tolerated; acid chlorides react twice.

---

## 6. Wittig Reaction

**One-line:** Phosphonium ylide + carbonyl → alkene + triphenylphosphine oxide.

**General equation:** Ph₃P=CR'R'' + R'''CHO → R'''CH=CR'R'' + Ph₃PO

**Mechanism summary:** Ylide formation → [2+2] cycloaddition → oxaphosphetane → collapse to alkene + Ph₃PO.

**Regioselectivity:** Works with aldehydes and ketones. Ketones are slower.

**Stereoselectivity:** Non-stabilized ylides (alkyl) → Z-alkene (kinetic). Stabilized ylides (EWG) → E-alkene (thermodynamic). Semi-stabilized (aryl/vinyl) → E-favored. Schlosser modification → E from non-stabilized.

**Common variations:** Horner-Wadsworth-Emmons (phosphonate → E-alkene); Julia-Kocienski (sulfone → E); Peterson olefination.

**Typical exam traps:** Stabilized ylides give E, not Z; retro-synthesis: alkene ↔ carbonyl + phosphonium.

---

## 7. Friedel-Crafts Alkylation

**One-line:** Lewis acid-catalyzed EAS installing an alkyl group on an aromatic ring.

**General equation:** ArH + RX + AlCl₃ → ArR + HX

**Mechanism summary:** AlCl₃ + RX → carbocation (or ion pair) → aromatic attack → Wheland intermediate → deprotonation.

**Regioselectivity:** Ortho/para directing. **Carbocation rearrangements are common** (hydride/alkyl shifts). Polyalkylation is a problem.

**Stereoselectivity:** Carbocation → racemic at new stereocenter.

**Common variations:** FC acylation (no rearrangement); Gattermann-Koch (CO+HCl+AlCl₃ → CHO); FC on heterocycles (indole C3).

**Typical exam traps:** n-PrCl gives isopropylbenzene (rearrangement!); polyalkylation; deactivating groups shut it down.

---

## 8. Friedel-Crafts Acylation

**One-line:** Lewis acid-catalyzed EAS installing an acyl group (aryl ketone).

**General equation:** ArH + RCOCl + AlCl₃ → ArCOR + HCl

**Mechanism summary:** AlCl₃ + RCOCl → acylium ion R–C≡O⁺ (resonance-stabilized, linear, NO rearrangement) → aromatic attack → deprotonation.

**Regioselectivity:** Ortho/para directing. Mono-substitution only (product is deactivated). No carbocation rearrangement.

**Stereoselectivity:** N/A (trigonal acyl carbon).

**Common variations:** Houben-Hoesch (nitrile → aryl ketone); Vilsmeier-Haack (DMF+POCl₃); Fries rearrangement (phenolic ester → hydroxyaryl ketone).

**Typical exam traps:** AlCl₃ is stoichiometric (binds ketone O); acyl group is meta-director for FUTURE EAS but ortho/para-directing in the FC acylation itself.

---

## 9. Pinacol-Pinacolone Rearrangement

**One-line:** Acid-catalyzed 1,2-diol → ketone via 1,2-migration.

**General equation:** R₂C(OH)C(OH)R₂ + H⁺ → R₂C=O + R₂CH (ketone)

**Mechanism summary:** Protonate OH → H₂O leaves → carbocation → 1,2-migration → deprotonation → ketone.

**Regioselectivity:** Migratory aptitude: aryl > H > alkyl. More substituted C tends to lose water. The carbon that loses OH becomes C=O.

**Stereoselectivity:** Anti migration (anti to leaving group). Retention at migrating carbon.

**Common variations:** Semipinacol (other leaving groups); Tiffeneau-Demjanov (ring expansion).

**Typical exam traps:** Carbonyl forms at the OH-loss carbon, NOT the migrating carbon; aryl > alkyl > H (students invert alkyl vs H).

---

## 10. Beckmann Rearrangement

**One-line:** Ketoxime → amide via acid-catalyzed anti-migration to nitrogen.

**General equation:** RC(=NOH)R' + acid → RC(O)NHR'

**Mechanism summary:** Protonate OH → anti-migration of R to N as H₂O leaves → nitrilium ion → water capture → tautomerization → amide.

**Regioselectivity:** The group ANTI to OH migrates. E vs Z oximes of unsymmetrical ketones give different products.

**Stereoselectivity:** Strictly anti-periplanar. Config of oxime determines product.

**Common variations:** Beckmann fragmentation (unstable migrating group → nitrile + alkene); photochemical Beckmann.

**Typical exam traps:** Which group migrates = anti to OH; product is amide, not nitrile; symmetric ketoximes give same amide regardless.

---

## 11. Hofmann Rearrangement (Degradation)

**One-line:** Primary amide → primary amine with one fewer carbon (via isocyanate).

**General equation:** RCONH₂ + Br₂ + NaOH → RNH₂ + CO₂ + NaBr

**Mechanism summary:** Deprotonation → N-bromination → second deprotonation → R migration to N (Br⁻ leaves) → isocyanate → hydrolysis → amine + CO₂.

**Regioselectivity:** Primary amides only. Product loses one carbon (carbonyl C becomes CO₂).

**Stereoselectivity:** Retention at migrating carbon.

**Common variations:** Lossen (hydroxamate → isocyanate); Curtius (acyl azide → isocyanate); Schmidt (acid + HN₃ → amine).

**Typical exam traps:** Confusing with Hofmann elimination (quaternary ammonium → alkene); product has ONE fewer carbon.

---

## 12. Baeyer-Villiger Oxidation

**One-line:** Ketone + peracid → ester (or lactone) via oxygen insertion.

**General equation:** RCOR' + R''CO₃H → R(O)COR' + R''CO₂H

**Mechanism summary:** Peroxyacid adds to carbonyl → Criegee intermediate → migration of R/R' to O as carboxylate leaves → ester.

**Regioselectivity:** Migratory aptitude: 3° alkyl > 2° > 1° > methyl; aryl migrates over alkyl. Migrating group becomes R–O– (alkoxy part of ester).

**Stereoselectivity:** Retention at migrating carbon.

**Common variations:** mCPBA (common peracid); MMPP (water-soluble); chiral BV catalysis.

**Typical exam traps:** Migrating group → alkoxy oxygen (NOT acyl side); aldehydes → carboxylic acids; migratory aptitude order wrong.

---

## 13. Cope Rearrangement

**One-line:** [3,3]-sigmatropic rearrangement of 1,5-dienes.

**General equation:** RCH=CH–CH₂–CH=CHR' → R'CH=CH–CH₂–CH=CHR

**Mechanism summary:** Concerted [3,3]-shift via chair TS (preferred over boat). No intermediates.

**Regioselectivity:** Equilibrium; product distribution follows thermodynamic stability.

**Stereoselectivity:** Chair TS → substituents equatorial; predictable stereochemistry.

**Common variations:** Oxy-Cope (3-hydroxy-1,5-diene → enone; accelerated ~10¹⁰ fold); anionic oxy-Cope; aza-Cope.

**Typical exam traps:** Drawing wrong atom connectivity; confusing [3,3] with [2,3]; not recognizing oxy-Cope acceleration.

---

## 14. Claisen Rearrangement

**One-line:** [3,3]-sigmatropic rearrangement of allyl vinyl ether → γ,δ-unsaturated carbonyl.

**General equation:** CH₂=CH–CH₂–O–CH=CH₂ → CH₃CH=CH–CH₂–CHO

**Mechanism summary:** Concerted [3,3]-shift → chair TS → ketene → tautomerization → aldehyde/ketone.

**Regioselectivity:** Allyl migrates to β-carbon of vinyl ether. Product: γ,δ-unsaturated carbonyl.

**Stereoselectivity:** Chair TS → E-alkene preferred. Chirality transfer from allylic center.

**Common variations:** Ireland-Claisen (silyl ketene acetal from ester → γ,δ-unsaturated acid); Johnson-Claisen (allyl alcohol + orthoester → ester); Eschenmoser-Claisen (→ amide).

**Typical exam traps:** Confusing with Claisen condensation; requires heat (150-200°C for simple); double bond is γ,δ, not α,β.

---

## 15. Birch Reduction

**One-line:** Na/NH₃(l)/ROH reduces arenes to 1,4-cyclohexadienes.

**General equation:** Aromatic + 2e⁻ + 2H⁺ → 1,4-cyclohexadiene

**Mechanism summary:** Solvated electron → radical anion → protonation → second electron → anion → protonation → 1,4-diene.

**Regioselectivity:** EDG (OR, NR₂) → double bonds AWAY from substituent. EWG (COOR, COOH) → double bonds TOWARD substituent.

**Stereoselectivity:** Protons from less hindered side.

**Common variations:** Benkeser reduction (Li → more complete); reductive alkylation.

**Typical exam traps:** Wrong double bond positions (EDG=away, EWG=toward); drawing 1,3- instead of 1,4-diene; confusing with catalytic hydrogenation.

---

## 16. Ozonolysis

**One-line:** O₃ cleaves alkenes to carbonyl fragments.

**General equation:** RCH=CHR' + O₃ → RCHO + R'CHO (reductive workup: Me₂S or Zn)

**Mechanism summary:** 1,3-dipolar cycloaddition of O₃ → molozonide → fragmentation → carbonyl oxide + carbonyl → recombination → ozonide → workup.

**Regioselectivity:** Terminal alkenes → formaldehyde + aldehyde (reductive) or carboxylic acid (oxidative). Internal → two carbonyls.

**Stereoselectivity:** N/A (cleavage destroys alkene stereochemistry).

**Common variations:** Reductive workup (Me₂S, Zn, PPh₃ → aldehydes); oxidative workup (H₂O₂ → carboxylic acids); OsO₄ alternative for diol.

**Typical exam traps:** Oxidative vs reductive workup determines aldehyde vs acid from terminal alkenes; cyclic alkenes give dicarbonyls; styrenes give benzaldehyde.

---

## 17. Robinson Annulation

**One-line:** Michael addition of an enolate to an enone, followed by intramolecular aldol → 2-cyclohexenone.

**General equation:** Ketone + CH₂=CHC(O)CH₃ → 2-cyclohexenone fused ring

**Mechanism summary:**
1. Enolate formation from ketone (Michael donor)
2. 1,4-addition to methyl vinyl ketone (Michael acceptor) → 1,5-diketone
3. Intramolecular aldol condensation → cyclohexenone

**Regioselectivity:** Forms 6-membered rings preferentially. The enolate attacks the β-carbon of the enone.

**Stereoselectivity:** Trans ring junction preferred for bicyclic systems.

**Common variations:** Robinson annulation with pre-formed enones; Wieland-Miescher ketone synthesis (proline-catalyzed asymmetric).

**Typical exam traps:** Drawing Michael addition without subsequent aldol (incomplete); wrong ring size; not recognizing that the product has an α,β-unsaturated ketone.

---

## 18. Mannich Reaction

**One-line:** Three-component condensation of an amine, aldehyde, and enolizable carbonyl → β-amino carbonyl.

**General equation:** R₂NH + R'CHO + R''CH₂C(O)R''' → R''CH(C(O)R''')CH₂NR₂ + H₂O

**Mechanism summary:**
- Amine + aldehyde → iminium ion
- Enol/enolate attacks iminium → Mannich base

**Regioselectivity:** The enolizable component must have an α-H. Most common: ketones. Aldehydes and activated methylene compounds also work.

**Stereoselectivity:** Not inherently stereoselective. Catalytic asymmetric versions exist (e.g., proline-catalyzed).

**Common variations:** Mannich with pre-formed iminium salts; Betti reaction (naphthol variant); Eschweiler-Clarke (N-methylation via formaldehyde + formic acid, related).

**Typical exam traps:** Confusing the amine component (secondary amines most common, not primary); not recognizing that the β-amino carbonyl is formed, not α-amino.

---

## 19. Knoevenagel Condensation

**One-line:** Active methylene compound + aldehyde/ketone → α,β-unsaturated product, base-catalyzed.

**General equation:** CH₂(Z)₂ + RCHO —base→ RCH=C(Z)₂ + H₂O (Z = EWG like COOR, CN, CHO)

**Mechanism summary:** Enolate of active methylene → aldol addition to carbonyl → dehydration → conjugated product.

**Regioselectivity:** Requires activated methylene (pKa < ~13). Common: malonic ester, acetoacetic ester, cyanoacetate.

**Stereoselectivity:** Generally E-isomer favored (thermodynamic).

**Common variations:** Doebner modification (malonic acid + aldehyde → α,β-unsaturated acid with CO₂ loss); Stork-Danheiser (see below).

**Typical exam traps:** Forgetting that the active methylene must be activated by two EWGs; non-activated ketones/aldehydes don't work well.

---

## 20. Suzuki-Miyaura Coupling

**One-line:** Palladium-catalyzed cross-coupling of organoboronic acids with organic halides.

**General equation:** R–B(OH)₂ + R'–X —Pd(0), base→ R–R' + B(OH)₃X

**Mechanism summary:** Oxidative addition (R'–X to Pd(0)) → transmetalation (R–B transfers to Pd) → reductive elimination (R–R').

**Regioselectivity:** Aryl–aryl, aryl–vinyl, vinyl–vinyl. Works with sp² halides. Sp³ requires special conditions (alkyl Suzuki).

**Stereoselectivity:** Stereochemistry of vinyl boronic acids and vinyl halides is RETAINED in product.

**Common variations:** Stille (organotin), Heck (alkene + halide), Sonogashira (alkyne + halide), Negishi (organozinc), Buchwald-Hartwig (C–N).

**Typical exam traps:** Base is essential (not a catalyst detail); stereochemistry of vinyl/vinyl is retained; sp³ couplings are much harder; boronic acids can undergo protodeboronation.

---

## 21. Heck Reaction

**One-line:** Pd-catalyzed coupling of an alkene with an organic halide → substituted alkene.

**General equation:** R–CH=CH₂ + R'–X —Pd(0), base→ R–CH=CH–R'

**Mechanism summary:** Oxidative addition (R'X to Pd(0)) → alkene coordination/insertion → β-hydride elimination → alkene product + HPdX → base regenerates Pd(0).

**Regioselectivity:** Aryl/vinyl halides + terminal alkenes → internal alkene. The aryl group attaches to the LESS substituted end of the alkene.

**Stereoselectivity:** Generally E-alkene (from syn insertion + anti β-H elimination).

**Common variations:** Intramolecular Heck (cyclization); asymmetric Heck; Heck with directing groups.

**Typical exam traps:** Aryl attaches to LESS substituted alkene carbon; E-selectivity; need a β-hydrogen for elimination (no β-H = no reaction or other pathway).

---

## 22. Sonogashira Coupling

**One-line:** Pd/Cu co-catalyzed coupling of terminal alkynes with aryl/vinyl halides.

**General equation:** R–C≡CH + R'–X —Pd(0), CuI, base→ R–C≡C–R'

**Mechanism summary:** Cu deprotonates alkyne → copper acetylide → transmetalation to Pd → reductive elimination with aryl/vinyl from oxidative addition.

**Regioselectivity:** Terminal alkynes + aryl/vinyl halides. Halide order: I > OTf > Br >> Cl (but Cl possible with modern ligands).

**Stereoselectivity:** Retains stereochemistry of vinyl halides.

**Common variations:** Sonogashira with amine base (triethylamine); copper-free Sonogashira; Cadiot-Chodkiewicz (diacetylene formation).

**Typical exam traps:** Cu is essential as co-catalyst (not just Pd); terminal alkyne needed; Glaser coupling (alkyne homocoupling) is a side reaction.

---

## 23. Stille Coupling

**One-line:** Pd-catalyzed coupling of organostannanes with organic halides.

**General equation:** R–SnR₃' + R''–X —Pd(0)→ R–R''

**Mechanism summary:** Oxidative addition → transmetalation from Sn to Pd → reductive elimination.

**Regioselectivity:** Broad scope: aryl–aryl, aryl–vinyl, vinyl–vinyl, acyl. Tolerates many functional groups.

**Stereoselectivity:** Retains stereochemistry of vinyl stannanes and vinyl halides.

**Common variations:** Stille-Kelly (bis-stannane + dihalide → macrocycle); carbostannylation of alkynes.

**Typical exam traps:** Organotin compounds are TOXIC; removal of tin byproducts is problematic; transmetalation is often rate-limiting.

---

## 24. Sharpless Asymmetric Epoxidation (AE)

**One-line:** Ti(OiPr)₄/tartrate ester/TBHP epoxidizes allylic alcohols with high enantioselectivity.

**General equation:** Allylic alcohol + TBHP + Ti(OiPr)₄ + (R or S)-DET → chiral epoxy alcohol

**Regioselectivity:** Only works with **allylic alcohols** (the OH coordinates to Ti). The epoxide forms on the double bond face opposite the directing OH.

**Stereoselectivity:** Predicted by mnemonic: **L-DET = epoxide approaches from bottom left; D-DET = from bottom right** (standard mnemonic diagram). Typically 90-99% ee.

**Common variations:** Katsuki-Sharpless (Jacobsen-Katsuki Mn-salen epoxidation for unfunctionalized alkenes); Shi epoxidation (fructose-derived dioxirane).

**Typical exam traps:** Must have allylic alcohol (won't work on simple alkenes); D vs L tartrate assignment; students draw wrong face approach.

---

## 25. Sharpless Asymmetric Dihydroxylation (AD)

**One-line:** OsO₄ + chiral ligand (DHQ or DHQD derivatives) gives cis-diols with high ee.

**General equation:** Alkene + OsO₄ + chiral ligand + oxidant → chiral vicinal diol

**Regioselectivity:** Mono-substituted alkenes → diol on the less hindered face typically. Ligand choice (DHQD vs DHQ) determines face selection.

**Stereoselectivity:** AD-Mix-α (DHQD-PHAL) and AD-Mix-β (DHQ-PHAL) give predictable enantiomers. Rule of thumb: the more electron-rich alkene face is attacked.

**Common variations:** Upjohn dihydroxylation (OsO₄, NMO, catalytic Os); Lemieux-Johnson (OsO₄, NaIO₄ → cleavage).

**Typical exam traps:** DHQD vs DHQ ligand assignment; OsO₄ is toxic and expensive; cis-diols only (trans alkenes give meso or racemic).

---

## 26. Simmons-Smith Cyclopropanation

**One-line:** Zn/Cu couple with CH₂I₂ converts alkenes to cyclopropanes.

**General equation:** RCH=CHR' + CH₂I₂ + Zn(Cu) → cyclopropane derivative

**Mechanism summary:** IZnCH₂I (iodozinc carbenoid) delivers CH₂ to alkene in a concerted syn addition.

**Regioselectivity:** Works on alkenes with coordinating groups (allylic alcohols, ethers) which direct the carbenoid.

**Stereoselectivity:** **Syn addition** — both new C–C bonds form on same face. Retains alkene stereochemistry in cyclopropane.

**Common variations:** Furukawa modification (ZnEt₂ + CH₂I₂); Charette cyclopropanation (chiral dioxaborolane ligand → enantioselective).

**Typical exam traps:** Syn addition only (cis-alkene → cis-cyclopropane substituents); directing groups enhance selectivity but aren't required; only adds CH₂ (methylene).

---

## 27. Swern Oxidation

**One-line:** Mild oxidation of alcohols to aldehydes/ketones using (COCl)₂, DMSO, Et₃N at low temperature.

**General equation:** RCH₂OH + (COCl)₂ + DMSO + Et₃N → RCHO + DMS + CO₂ + Et₃NHCl

**Mechanism summary:** (COCl)₂ + DMSO → chlorodimethylsulfonium ion → alcohol attacks S → deprotonation → sulfur ylide → intramolecular SN2 → aldehyde/ketone + DMS.

**Regioselectivity:** Primary → aldehyde (no overoxidation). Secondary → ketone.

**Stereoselectivity:** Retention of stereochemistry at alcohol carbon (no enolization under these conditions).

**Common variations:** Parikh-Doering (SO₃·Py, DMSO, Et₃N); Dess-Martin periodinane (milder, room temp); Swern at −60°C to avoid side products.

**Typical exam traps:** Must keep cold to avoid side reactions (Pummerer-like); dimethyl sulfide byproduct smells terrible; overoxidation not an issue (unlike PCC for some substrates).

---

## 28. Jones Oxidation

**One-line:** CrO₃/H₂SO₄/acetone oxidizes primary alcohols to carboxylic acids, secondary to ketones.

**General equation:** RCH₂OH + CrO₃/H₂SO₄ → RCOOH (primary); R₂CHOH → R₂C=O (secondary)

**Mechanism summary:** Chromate ester formation → elimination of Cr(IV) → carbonyl.

**Regioselectivity:** Primary → carboxylic acid (NO stopping at aldehyde). Secondary → ketone.

**Stereoselectivity:** No stereochemical issues (sp² product).

**Common variations:** PCC (stops at aldehyde for primary); PDC; Collins oxidation (CrO₃·pyridine).

**Typical exam traps:** Primary alcohols give carboxylic acids, NOT aldehydes; acetone can be oxidized; Cr(VI) is toxic/carcinogenic.

---

## 29. PCC Oxidation

**One-line:** Pyridinium chlorochromate (PCC) in CH₂Cl₂ oxidizes alcohols; primary → aldehyde, secondary → ketone.

**General equation:** RCH₂OH + PCC/CH₂Cl₂ → RCHO (primary); R₂CHOH → R₂C=O (secondary)

**Mechanism summary:** Chromate ester → elimination → carbonyl. Anhydrous conditions prevent overoxidation.

**Regioselectivity:** Primary → aldehyde (no overoxidation in anhydrous CH₂Cl₂). Secondary → ketone. Allylic alcohols can give α,β-unsaturated carbonyls.

**Stereoselectivity:** Generally not stereoselective.

**Common variations:** PDC (pyridinium dichromate); Dess-Martin periodinane (milder); IBX.

**Typical exam traps:** PCC CAN overoxidize some primary alcohols (especially in protic solvents); acid-sensitive groups may not survive; Cr(VI) toxicity.

---

## 30. LiAlH₄ Reduction

**One-line:** Strong hydride reducing agent: reduces aldehydes, ketones, esters, acids, amides, epoxides, nitriles.

**General equation:** RCOOR' + LiAlH₄ → RCH₂OH + R'OH (esters); RCOOH → RCH₂OH (acids); RCONH₂ → RCH₂NH₂ (amides)

**Mechanism summary:** Hydride delivery to carbonyl → alkoxide. Stoichiometry matters: esters need 1 equiv (2H⁻), acids/amides need 2 equiv.

**Regioselectivity:** Reduces: aldehydes, ketones, esters (→ 1° alcohol), acids (→ 1° alcohol), acid chlorides, epoxides, amides (→ amines), nitriles (→ 1° amines), azides. Does NOT reduce isolated alkenes/alkynes.

**Stereoselectivity:** Cis for epoxide opening (hydride attacks less substituted carbon). Felkin-Anh for ketones.

**Common variations:** NaBH₄ (milder, selective); DIBAL-H (partial reduction of esters to aldehydes); Super Hydride (LiEt₃BH).

**Typical exam traps:** Esters → primary alcohols (NOT secondary!); amides → amines (need excess LiAlH₄); carboxylic acids need 2 equiv; DOES reduce epoxides; anhydrous conditions required.

---

## 31. NaBH₄ Reduction

**One-line:** Mild hydride reducing agent: reduces aldehydes and ketones to alcohols; generally doesn't touch esters/amides.

**General equation:** RCHO/RCOR' + NaBH₄ → RCH₂OH/R'CHOH (ketone → secondary alcohol; aldehyde → primary alcohol)

**Mechanism summary:** Hydride delivery to carbonyl carbon → alkoxide → protonation (aqueous workup).

**Regioselectivity:** Reduces aldehydes and ketones. Does NOT reduce esters, amides, or carboxylic acids under normal conditions. DOES reduce acid chlorides and acyl imidazoles. CeCl₃ (Luche conditions) enhances selectivity for conjugate reduction of α,β-unsaturated carbonyls.

**Stereoselectivity:** Felkin-Anh for ketones. Luche reduction (NaBH₄/CeCl₃) gives 1,2-reduction of enones with high 1,2-selectivity.

**Common variations:** Luche reduction (CeCl₃ + NaBH₄ → 1,2-selective); NaBH₃CN (reductive amination, acid-stable); NaBH(OAc)₃ (chemoselective).

**Typical exam traps:** NaBH₄ does NOT reduce esters/amides (unlike LiAlH₄); NaBH₃CN is used in reductive amination because it works at pH 7; MeOH or EtOH as solvent.

---

## 32. Fischer Indole Synthesis

**One-line:** Arylhydrazone of a ketone/aldehyde cyclizes under acid to give an indole.

**General equation:** ArNHNH₂ + RCOR' —acid, Δ→ indole derivative

**Mechanism summary:** Hydrazone formation → [3,3]-sigmatropic rearrangement → ring closure → loss of NH₃ → indole.

**Regioselectivity:** The more substituted carbon of the original carbonyl becomes C3 of the indole. Asymmetric ketones can give two regioisomeric indoles.

**Stereoselectivity:** N/A (aromatization destroys stereochemistry).

**Common variations:** Bartoli indole synthesis (o-substituted nitroarenes + vinyl Grignard); Larock indole synthesis (Pd-catalyzed, o-iodoaniline + alkyne).

**Typical exam traps:** Regiochemistry — which carbon becomes C3 (the more substituted one); works only with arylhydrazines (not alkyl hydrazines); strong acid + heat required.

---

## 33. Vilsmeier-Haack Formylation

**One-line:** DMF + POCl₃ generates an iminium electrophile that formylates electron-rich arenes.

**General equation:** ArH + DMF + POCl₃ → ArCHO

**Mechanism summary:** POCl₃ activates DMF → chloroiminium ion (Vilsmeier reagent, [Cl–CH=NMe₂]⁺) → electrophilic aromatic substitution → hydrolysis → aryl aldehyde.

**Regioselectivity:** Electron-rich arenes only (phenols, anilines, pyrroles, furans). Para-directing on phenols/anilines. Does NOT work on deactivated rings.

**Stereoselectivity:** N/A.

**Common variations:** Vilsmeier-Haack acylation (using N-methylformanilide instead of DMF → aryl ketone); on heterocycles (pyrroles → 2-formylpyrroles).

**Typical exam traps:** Only works on electron-rich rings; product is an aldehyde, not a ketone; overreaction is possible with very activated systems.

---

## 34. Clemmensen Reduction

**One-line:** Zinc amalgam/HCl reduces aryl ketones (and other carbonyls) to methylene.

**General equation:** ArCOR + Zn(Hg), HCl → ArCH₂R

**Mechanism summary:** Surface reaction on zinc; carbonyl is reduced directly to CH₂. Exact mechanism debated (carbenoid vs stepwise).

**Regioselectivity:** Works on aryl ketones, diaryl ketones, some aliphatic ketones. Acid-sensitive functional groups won't survive.

**Stereoselectivity:** N/A (product is sp³ CH₂).

**Common variations:** Wolff-Kishner (basic alternative — avoids acid-sensitive groups); Mozingo reduction (thioacetal + Raney Ni).

**Typical exam traps:** Acidic conditions destroy acid-sensitive groups (use Wolff-Kishner instead); not as general as often assumed — some substrates fail.

---

## 35. Wolff-Kishner Reduction

**One-line:** Hydrazine + strong base at high temperature reduces carbonyl to methylene.

**General equation:** RCOR' + N₂H₄ + KOH/EtOH, Δ → RCH₂R' + N₂

**Mechanism summary:** Hydrazone formation → deprotonation → loss of N₂ → carbanion → protonation → methylene.

**Regioselectivity:** Aldehydes and ketones. Acid-sensitive groups tolerated (unlike Clemmensen).

**Stereoselectivity:** N/A.

**Common variations:** Huang-Minlon modification (sealed tube, KOH, diethylene glycol, high T); Caglioti reaction (tosylhydrazone + organolithium).

**Typical exam traps:** Requires high temperature (200°C+ in original); Huang-Minlon is the practical version; Clemmensen is the acidic alternative — know when to use which.

---

## 36. McMurry Coupling

**One-line:** Low-valent titanium (TiCl₃/LiAlH₄ or TiCl₄/Zn) couples carbonyls to alkenes.

**General equation:** 2 RCOR' + Ti(0) → RCH=CHR' + TiO₂

**Mechanism summary:** Pinacol coupling on Ti surface → Ti-mediated deoxygenation → alkene. Radical mechanism debated.

**Regioselectivity:** Symmetrical or intramolecular coupling preferred. Intermolecular unsymmetrical gives mixtures.

**Stereoselectivity:** Favors E-alkene for intermolecular. Intramolecular gives defined stereochemistry based on ring constraints.

**Common variations:** McMurry olefination (TiCl₃/Zn-Cu couple); intramolecular McMurry (macrocycle synthesis); pinacol coupling (stops at diol with milder reductant).

**Typical exam traps:** Unsymmetrical ketones give mixtures (use intramolecular for clean results); overreduction to alkane is a side reaction; low-valent Ti is pyrophoric.

---

## 37. Shapiro Reaction

**One-line:** Base-induced elimination of p-toluenesulfonylhydrazones to give alkenes (typically terminal).

**General equation:** RCH₂CH=N–NHTs + 2 RLi → RCH=CH₂ + Li₂SO₂Tos + N₂

**Mechanism summary:** Tosylhydrazone formation → deprotonation (2 equiv strong base) → elimination of TsLi + N₂ → vinyllithium intermediate.

**Regioselectivity:** The less substituted carbon of the hydrazone becomes the alkene carbon bonded to lithium (→ gives less substituted vinyl lithium → after protonation, terminal alkene).

**Stereoselectivity:** Vinyllithium is formed with defined geometry; protonation gives E or Z depending on conditions.

**Common variations:** Bamford-Stevens (see below — thermal variant); Shapiro vinyllithium can be trapped with electrophiles (not just protonated).

**Typical exam traps:** Requires 2 equiv of strong base (RLi or LDA); gives terminal alkene preferentially (NOT Zaitsev!); Bamford-Stevens is the thermal analog.

---

## 38. Bamford-Stevens Reaction

**One-line:** Thermal or base-induced decomposition of tosylhydrazones to give alkenes (or carbenes).

**General equation:** RCH₂CH=N–NHTs + base, heat → alkene

**Mechanism summary:** Tosylhydrazone + base → diazo compound → loss of N₂ → carbene (or carbene rearranges to alkene).

**Regioselectivity:** Under protic conditions (e.g., glycol, heat) → more substituted alkene (Zaitsev). Under aprotic conditions (e.g., DMSO, heat) → less substituted alkene (anti-Zaitsev, similar to Shapiro).

**Stereoselectivity:** Depends on conditions; generally mixture.

**Common variations:** Shapiro (organolithium base, low temp → vinyllithium); Bamford-Stevens in aprotic solvent → carbene → rearrangement.

**Typical exam traps:** Aprotic vs protic gives OPPOSITE regioselectivity (this is the key exam point); don't confuse with Shapiro.

---

## 39. Stork Enamine Reaction

**One-line:** Enamine (from secondary amine + ketone) acts as a nucleophilic enolate equivalent in alkylation and acylation.

**General equation:** R₂C=O + R'₂NH —Δ, -H₂O→ enamine + RX → hydrolysis → α-substituted ketone

**Mechanism summary:** Enamine formation (secondary amine + ketone, acid cat., remove water) → enamine attacks electrophile (alkyl halide or acyl halide) → iminium → hydrolysis → α-substituted ketone.

**Regioselectivity:** Monosubstitution (enamine is a mild nucleophile → doesn't polyalkylate like hard enolates). Works with alkyl halides and acid chlorides.

**Stereoselectivity:** Enamine attacks from less hindered face; not highly stereoselective without chiral auxiliaries.

**Common variations:** Stork enamine alkylation (alkyl halide); Stork enamine acylation (acid chloride → 1,3-diketone); proline-catalyzed enamine reactions (organocatalysis).

**Typical exam traps:** Only secondary amines work (pyrrolidine, morpholine — primary amines give imines, not enamines); hydrolysis step is essential to recover the ketone; acylation gives 1,3-dicarbonyls (not aldol products).

---

## 40. Danheiser Annulation

**One-line:** Allenylsilane + activated alkene (enone) under Lewis acid → cyclopentene annulation.

**General equation:** Allenylsilane + CH₂=CHC(O)R —Lewis acid→ cyclopentene derivative

**Mechanism summary:** Lewis acid activates enone → [3+2] cycloaddition with allenylsilane → cyclopentyl cation → desilylation.

**Regioselectivity:** Forms 5-membered rings. The allenylsilane provides 3 carbons; the enone provides 2.

**Stereoselectivity:** Depends on substitution of allene and enone.

**Common variations:** Stork-Danheiser (see below); Danheiser with silyl-substituted alkynes.

**Typical exam traps:** It's a [3+2], NOT a [4+2] like Diels-Alder; allenylsilane is the specific dienophile component; gives cyclopentenes, not cyclohexenes.

---

## 41. Stork-Danheiser Transposition

**One-line:** Three-step sequence converting an α,β-unsaturated ketone to its constitutional isomer (double bond migration).

**General equation:** Enone → 1,2-addition of organocuprate → silylation → Brook rearrangement/elimination → isomeric enone

**Mechanism summary:** 1,2-addition of R₂CuLi to enone → silyl enol ether formation → Lewis acid-promoted rearrangement → new enone with migrated double bond.

**Regioselectivity:** The double bond shifts to the adjacent position with respect to the carbonyl.

**Stereoselectivity:** Depends on enolate geometry and trapping conditions.

**Typical exam traps:** This is a multi-step transformation, not a single reaction; easily confused with the Danheiser annulation.

---

## 42. Sakurai Reaction (Hosomi-Sakurai)

**One-line:** Allylsilane + carbonyl (or related electrophile) under Lewis acid → homoallylic alcohol.

**General equation:** CH₂=CH–CH₂–SiR₃ + R'R''C=O —Lewis acid→ CH₂=CH–CH₂–C(OH)R'R''

**Mechanism summary:** Lewis acid coordinates to carbonyl → allylsilane attacks via SE' mechanism (β-silicon effect stabilizes cationic intermediate) → homoallylic alcohol after workup.

**Regioselectivity:** γ-attack (homoallylic product). Works with aldehydes, ketones, acetals. Allylsilanes are stable, non-basic nucleophiles.

**Stereoselectivity:** Chelation control with appropriate Lewis acids. Crotylsilanes give anti or syn depending on geometry.

**Common variations:** Hosomi-Sakurai with acetals (→ ethers); Sakurai with iminium ions (Mannich-type); intramolecular Sakurai (cyclizations).

**Typical exam traps:** Attack is at the γ-position of the allylsilane (homoallylic product), not the α-position; allylsilanes are stable unlike allyl Grignards.

---

## 43. Ferrier Rearrangement

**One-line:** Lewis acid-promoted rearrangement of glycals to 2,3-unsaturated glycosides.

**General equation:** Glycal + ROH —Lewis acid→ 2,3-unsaturated glycoside

**Mechanism summary:** Lewis acid coordinates to glycal OAc → allylic rearrangement → oxocarbenium → nucleophile (ROH) capture → 2,3-unsaturated glycopyranoside.

**Regioselectivity:** The double bond migrates from C1-C2 to C2-C3. Gives α-glycoside with many promoters.

**Stereoselectivity:** Generally α-selective for D-glycals. Reversal possible with chiral catalysts.

**Typical exam traps:** This is a rearrangement (double bond moves), not a simple substitution; different from Ferrier carbocyclization.

---

## 44. Ferrier Carbocyclization

**One-line:** Pd(II)-catalyzed conversion of glycals to cyclohexenones (carbocycle from sugar).

**General equation:** Glycal —Pd(II)→ cyclohexenone derivative

**Mechanism summary:** Pd coordinates to alkene → forms π-allyl-Pd intermediate → enolization → reductive elimination → cyclohexenone.

**Regioselectivity:** Forms 6-membered carbocycles. Only works with certain glycol configurations.

**Stereoselectivity:** Depends on substrate geometry.

**Typical exam traps:** Completely different from Ferrier rearrangement (which gives 2,3-unsaturated glycosides); this gives a CARBOCYCLE, not a carbohydrate.

---

## 45. Rubottom Oxidation

**One-line:** Oxidation of silyl enol ethers with mCPBA to give α-hydroxy carbonyl compounds.

**General equation:** Silyl enol ether + mCPBA → α-hydroxy carbonyl after workup

**Mechanism summary:** Epoxidation of enol ether double bond → silyl migration (Brook rearrangement) → α-siloxy carbonyl → desilylation → α-hydroxy carbonyl.

**Regioselectivity:** Oxygen adds to the face of the enol ether, giving the α-hydroxy carbonyl with stereochemistry determined by enol ether geometry.

**Stereoselectivity:** High facial selectivity based on enol ether geometry (E or Z silyl enol ether → predictable stereochemistry at the α-carbon).

**Common variations:** Davis oxaziridine oxidation (alternative to Rubottom); Vedejs oxaziridine.

**Typical exam traps:** The stereochemistry is controlled by the silyl enol ether geometry (not the carbonyl); silyl migration is a key step (Brook-type); don't confuse with simple epoxidation of the parent alkene.

---

## 46. Evans Aldol

**One-line:** Chiral oxazolidinone auxiliary-mediated aldol reaction for high enantioselectivity.

**General equation:** N-acyloxazolidinone + aldehyde + Lewis acid (Sn(OTf)₂, Bu₂BOTf) → syn or anti β-hydroxy carbonyl

**Mechanism summary:** Metal enolate formed from N-acyloxazolidinone → Zimmerman-Traxler chair TS → aldehyde approach from less hindered face → aldolate.

**Regioselectivity:** The enolate geometry (Z or E) is controlled by the Lewis acid and base. Z-enolates → anti aldol product; E-enolates → syn.

**Stereoselectivity:** Typically >95% ee and >20:1 dr. Syn or anti controlled by choice of base and metal.

**Common variations:** Evans syn aldol (Bu₂BOTf, Et₃N → Z-enolate → anti product); anti-selective conditions (different Lewis acid/base); auxiliary removal (LiOH, LiOOH, LiBH₄).

**Typical exam traps:** The nomenclature is confusing: Z-enolate gives ANTI aldol product, E-enolate gives SYN (because of the Zimmerman-Traxler model); auxiliary must be removed after reaction.

---

## 47. Mukaiyama Aldol

**One-line:** Lewis acid-mediated addition of silyl enol ethers to aldehydes/ketones (Lewis acid aldol).

**General equation:** Silyl enol ether + RCHO —Lewis acid→ β-hydroxy carbonyl (after workup)

**Mechanism summary:** Lewis acid activates aldehyde → silyl enol ether attacks → β-siloxy carbonyl → aqueous workup → β-hydroxy carbonyl.

**Regioselectivity:** Works with aldehydes and ketones. Enol ether geometry determines syn/anti selectivity.

**Stereoselectivity:** Z-silyl enol ether → syn; E-silyl enol ether → anti (opposite of Evans due to open vs chair TS, depends on Lewis acid). With chiral Lewis acids → high ee.

**Common variations:** Mukaiyama-Michael (silyl enol ether + enone); vinylogous Mukaiyama aldol (diene equivalent → δ-hydroxy carbonyl); Mukaiyama with TiCl₄ (classic conditions).

**Typical exam traps:** Silyl enol ether geometry controls diastereoselectivity — know which geometry gives which; this is a LEWIS ACID reaction, not base-promoted; different Lewis acids can reverse selectivity.

---

## 48. Chan-Lam Coupling

**One-line:** Cu(II)-mediated coupling of boronic acids with N/O/S nucleophiles.

**General equation:** ArB(OH)₂ + R–NH₂ —Cu(OAc)₂, base, air→ Ar–NHR

**Mechanism summary:** Transmetalation of aryl from B to Cu → oxidation → reductive elimination → C–N (or C–O, C–S) bond.

**Regioselectivity:** Works with boronic acids + amines, phenols, alcohols, thiols. Aryl and vinyl boronic acids.

**Stereoselectivity:** Retains stereochemistry of vinyl boronic acids.

**Common variations:** Chan-Lam amination; Chan-Lam O-arylation; Chan-Lam S-arylation; Chan-Evans-Lam.

**Typical exam traps:** Requires base AND air (oxidant); mild conditions (room temp); competitive protodeboronation; not as general as Buchwald-Hartwig for C–N coupling.

---

## 49. Buchwald-Hartwig Amination

**One-line:** Pd-catalyzed coupling of aryl halides with amines → aryl amines.

**General equation:** Ar–X + R₂NH —Pd(0), ligand, base→ Ar–NR₂

**Mechanism summary:** Oxidative addition (Ar–X to Pd(0)) → amine deprotonation/coordination → reductive elimination → C–N bond.

**Regioselectivity:** Aryl bromides and chlorides (with modern ligands). Primary and secondary amines. Electron-rich and -poor aryl halides.

**Stereoselectivity:** N/A for C(sp²)–N.

**Common variations:** Buchwald-Hartwig with biarylphosphine ligands (XPhos, SPhos, BrettPhos); C–O coupling; C–C coupling (α-arylation of carbonyls).

**Typical exam traps:** Ligand choice is crucial (different ligands for different substrate combinations); requires strong base; competitive β-hydride elimination with certain ligands.

---

## 50. Mitsunobu Reaction

**One-line:** Inversion of alcohol configuration via SN2 displacement with carboxylic acid/nucleophile using DEAD and PPh₃.

**General equation:** RCH(OH)R' + R''COOH + PPh₃ + DEAD → RCH(R')OCOR'' + Ph₃PO + byproduct

**Mechanism summary:** PPh₃ + DEAD → betaine → alcohol attacks P → alkoxyphosphonium ion → nucleophile (carboxylate) does SN2 → inverted product.

**Regioselectivity:** Primary and secondary alcohols. The nucleophile must be acidic enough to be deprotonated (pKa < ~11). Tertiary alcohols don't work (SN2).

**Stereoselectivity:** Complete INVERSION of configuration at the alcohol carbon (SN2 mechanism).

**Common variations:** Mitsunobu esterification (R''COOH); Mitsunobu etherification (phenols); Mitsunobu with azodicarboxylates (DIAD, DEAD).

**Typical exam traps:** Net INVERSION (not retention!); the nucleophile must be acidic; Ph₃PO byproduct is hard to remove; DEAD/DIAD are explosive; the alcohol carbon must be SN2-accessible.

---

## 51. Julia-Kocienski Olefination

**One-line:** Sulfone-mediated conversion of carbonyls to alkenes, generally E-selective.

**General equation:** RSO₂CH₂R' + R''CHO —base→ RCH=CHR''

**Mechanism summary:** Deprotonation of sulfone → addition to aldehyde → β-hydroxysulfone → SmI₂ or other reductant → alkene + sulfinate.

**Regioselectivity:** E-selective for most 1-aryl-2-alkyl combinations.

**Stereoselectivity:** High E-selectivity (opposite of non-stabilized Wittig which gives Z). Kocienski modification uses 1-phenyl-1H-tetrazol-5-yl sulfones (PT-sulfones) for cleaner reactions.

**Common variations:** Julia olefination (original, Na/Hg reductant); Julia-Kocienski (SmI₂, PT-sulfones); one-pot Julia-Kocienski.

**Typical exam traps:** E-selectivity (compare with Wittig Z for non-stabilized); the original Julia uses Na/Hg (unpleasant); Kocienski modification is the modern version.

---

## 52. Overman Rearrangement

**One-line:** [3,3]-sigmatropic rearrangement converting allylic alcohols to allylic amines with chirality transfer.

**General equation:** Allylic alcohol → trichloroacetimidate —heat→ allylic trichloroacetamide

**Mechanism summary:** Allylic alcohol + Cl₃CCN, base → trichloroacetimidate → thermal [3,3]-sigmatropic rearrangement → allylic amide.

**Regioselectivity:** The nitrogen ends up at the allylic position with the double bond shifted. Regioselective for the more substituted position.

**Stereoselectivity:** High chirality transfer: stereochemistry at the allylic carbon is transferred to the new C–N bond center with inversion.

**Common variations:** Eschenmoser-Claisen (related but O→C migration); Overman with chiral catalysts.

**Typical exam traps:** This is a [3,3]-rearrangement (like Cope/Claisen), not an SN2; the alcohol must first be converted to trichloroacetimidate; chirality TRANSFER is the key feature.

---

## Quick Reference: Reaction Classification

| Category | Reactions |
|----------|-----------|
| **Pericyclic** | Diels-Alder, Cope, Claisen rearrangement |
| **Carbonyl C–C formation** | Aldol, Claisen cond., Michael, Mannich, Knoevenagel, Robinson annulation |
| **Organometallic addition** | Grignard, Sakurai, Mukaiyama aldol |
| **Olefin formation** | Wittig, HWE, Julia-Kocienski, McMurry, Shapiro, Bamford-Stevens |
| **Cross-coupling (Pd)** | Suzuki, Heck, Sonogashira, Stille, Buchwald-Hartwig |
| **Cross-coupling (other)** | Chan-Lam |
| **Oxidation** | Swern, Jones, PCC, Baeyer-Villiger, Sharpless AE/AD, Ozonolysis |
| **Reduction** | LiAlH₄, NaBH₄, Birch, Clemmensen, Wolff-Kishner |
| **Rearrangement** | Beckmann, Hofmann, Pinacol-pinacolone, Overman, Ferrier, Claisen, Cope |
| **EAS** | Friedel-Crafts alkyl/acyl, Vilsmeier-Haack |
| **Heterocycle formation** | Fischer indole |
| **Enamine chemistry** | Stork enamine, Danheiser |
| **Stereocontrolled** | Evans aldol, Mukaiyama aldol, Sharpless AE/AD, Simmons-Smith, Rubottom |
