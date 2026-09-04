# Stagewise organic structure tracking to product or proton multiplicity

**Retrieve with:** multistep organic product tracking, carbocation ring expansion alkyl shift, ozonolysis carbonyl mapping, intramolecular aldol ring size, alpha site enumeration

**Use when:** A multistep organic product or spectroscopy problem combines carbocation rearrangement, elimination or alkene cleavage, and carbonyl cyclization, making the result depend on propagated connectivity and competing ring closures.

## Procedure

1. Label the starting carbon skeleton and maintain an atom-and-connectivity ledger after every reagent, recording each broken bond, formed bond, charge, and migrated substituent.
2. At each carbocation, iteratively enumerate feasible 1,2-hydride, alkyl, and ring-bond shifts before capture; retain shifts that improve cation stability or relieve meaningful ring strain and redraw the full skeleton.
3. For elimination and alkene cleavage, identify the actual beta hydrogen and leaving group, then convert each alkene carbon separately to an aldehyde or ketone according to its retained substituents.
4. For a dicarbonyl, list every alpha carbon that bears hydrogen and pair it with each electrophilic carbonyl; count the prospective ring as the atoms on the existing path between those two carbons, endpoints included.
5. Compare feasible closures, normally favoring five- or six-membered rings under reversible conditions; draw the beta-hydroxy carbonyl, reverse-cleave its new bond, and verify carbon and functional-group conservation.

## Preferred Support

- chem-memory/L2_principles/chemtester_gap_skills/stagewise_organic_structure_to_proton_multiplicity.md
- chem-memory/L2_principles/openstax_organic_ch08_alkene_reactions.md
- chem-memory/L2_principles/organic_reaction_mechanisms.md
- chem-memory/L2_principles/carbonyl_chemistry.md

## Guards

- Do not trap the first carbocation before checking whether sequential rearrangements remain favorable.
- Do not infer a new ring size from dicarbonyl locants; count the atoms on the closing path.
- Do not assume the least hindered alpha site wins when reversible enolization and ring topology favor another closure.
- Reject a proposed product unless retro-aldol cleavage and atom balance recover the mapped precursor.
