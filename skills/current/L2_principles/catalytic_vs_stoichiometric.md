---
id: catalytic_vs_stoichiometric
layer: 2
title: Catalytic vs Stoichiometric Reagents (Biocatalysis, Organocatalysis, Flow)
parent: ../L1_ontology/chemistry-core-map.md#entry-282
stability: high
confidence: high
last_verified: 2026-03-24
source: Manahan (LibreTexts), Anastas & Warner
---

# Catalytic vs Stoichiometric Approaches

## Core Concept

Green chemistry principle #9: "Catalytic reagents (as selective as possible) are superior to stoichiometric reagents." Modern catalysis strategies minimize waste while enabling selective transformations.

---

## Comparison

| Aspect | Stoichiometric | Catalytic |
|--------|---------------|-----------|
| Reagent consumption | >1 equiv (waste generated) | <1 equiv (regenerated) |
| Atom economy | Often poor | Often high |
| Selectivity | Variable | Can be excellent |
| Energy | May need harsh conditions | Often mild |
| Cost | Reagent consumed each cycle | Amortized over many cycles |

---

## Biocatalysis

### Enzymes as Green Catalysts
- **Advantages:** high selectivity (enantio-, regio-, chemoselectivity), mild conditions, biodegradable
- **Limitations:** substrate scope, stability, scale

### Major Enzyme Classes in Synthesis
| Class | Reaction | Example |
|-------|----------|---------|
| Ketoreductases (KRED) | Asymmetric reduction | Statin side chains |
| Transaminases (ATA) | Asymmetric amination | Sitagliptin (Merck) |
| Lipases | Hydrolysis, esterification | Resolution |
| Cytochrome P450 | C-H oxidation | Drug metabolism |
| Aldolases | C-C bond formation | Imine reduction |

### Directed Evolution
- Iterative mutagenesis + screening (Frances Arnold, Nobel 2018)
- Dramatically expands enzyme substrate scope and stability

---

## Organocatalysis

### Small organic molecules as catalysts
- No metals → no heavy metal contamination
- Often chiral → asymmetric induction

### Major Organocatalyst Classes
1. **Proline derivatives** — enamine catalysis (aldol, Mannich)
2. **Imidazolidinones** — MacMillan catalyst (Diels-Alder)
3. **Thioureas** — H-bond donor catalysis
4. **Phase-transfer catalysts** — cinchona alkaloids

---

## Flow Chemistry

### Advantages for Green Chemistry
- Improved heat/mass transfer → smaller reactors
- Continuous processing → consistent quality
- Reduced solvent volumes
- Safer handling of hazardous reagents (small inventory)
- Easy scale-out (numbering up vs scaling up)

### Applications
- APIs (pharmaceutical manufacturing)
- Photochemistry (efficient light penetration)
- Ozonolysis, nitration (hazardous chemistry)

---

## Links

- L3: `../L3_functions/green_chemistry_tools.py`
- L4: `../L4_reference/green_chemistry_reference.csv`
