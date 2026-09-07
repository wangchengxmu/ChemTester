# L4: Asymmetric Biocatalysis Reference Data

## Common Enzyme Types and Performance

| Enzyme Class | Source | Transformation | Typical Substrate | Typical ee | Cofactor | Regeneration |
|---|---|---|---|---|---|---|
| Lipase (CAL-B) | *Candida antarctica* | Resolution (acylation) | Secondary alcohols, amines | 95-99% | None | N/A |
| Lipase (PCL) | *Pseudomonas cepacia* | Resolution | Primary alcohols | 90-98% | None | N/A |
| ADH | *Leifsonia* sp. | Ketone reduction | Substituted acetophenones | 95-99% | NADPH | 2-propanol |
| ADH (LB-ADH) | *Lactobacillus brevis* | Ketone reduction | 2,5-Diketo esters | >99% | NADH | GDH/glucose |
| ADH (ADH-A) | *Rhodococcus ruber* | Ketone reduction | Broad scope | 95-99% | NADH | 2-propanol |
| FDH | *Candida boidinii* | Cofactor regeneration | Formate → CO₂ | N/A | NADH | Formate |
| GDH | *Bacillus megaterium* | Cofactor regeneration | Glucose → gluconolactone | N/A | NADPH | D-glucose |
| Oxynitrilase | *Hevea brasiliensis* | Hydrocyanation | Aldehydes → cyanohydrins | 95-99% | None | N/A |
| BAL | *Pseudomonas fluorescens* | Benzoin condensation | Benzaldehydes | 95-99% | ThDP | None |
| Threonine aldolase | *E. coli* | Aldol | Glycine + benzaldehyde | >99% | PLP | N/A |
| BVMO | *Acinetobacter* sp. | Baeyer-Villiger | Cyclohexanones | 90-99% | NADPH | NADPH in situ |
| Epoxide hydrolase | *Methylobacterium* sp. | Epoxide hydrolysis | Styrene oxides | 90-99% | None | N/A |
| Transaminase | *E. coli* | Transamination | Ketones → amines | 95-99% | PLP | Alanine/L-alanine dehydrogenase |
| Enoate reductase | *Candida macedoniensis* | C=C reduction | α,β-Unsaturated ketones | 90-99% | NADPH | GDH |
| Nitrilase | *Alcaligenes faecalis* | Nitrile hydrolysis | α-Hydroxynitriles | 95-99% | None | N/A |
| Amino acid DH | *Bacillus sphaericus* | Reductive amination | α-Keto acids → amino acids | >99% | NADH | FDH/formate |

## Cofactor Regeneration Systems

| System | Reaction | Cost | Irreversible | TTN Typical |
|---|---|---|---|---|
| 2-propanol/ADH | i-PrOH → acetone | Low | No (equilibrium) | 100-500 |
| Formate/FDH | HCOO⁻ → CO₂ | Medium | Yes | 500-2000 |
| Glucose/GDH | Glucose → gluconate | Low | Yes | 1000-5000 |
| Glucose-6-P/G6PDH | G6P → 6-phosphogluconate | Higher | Yes | 1000+ |
| PNT | NADH + NADP⁺ ↔ NAD⁺ + NADPH | Medium | No | 1000+ |

## DKR Systems (Lipase + Metal Racemization)

| Racemization Agent | Enzyme | Substrate Class | Yield | ee | Reference |
|---|---|---|---|---|---|
| Ru complex (Shvo's) | CAL-B | Secondary alcohols | 78-92% | 99% | Kim et al. |
| AlMe₃/BINOL | CAL-B | Benzylic alcohols | 99% | 98% | Pàmies/Bäckvall |
| Pd nanoparticle | CAL-B | Allylic alcohols | 85-95% | >99% | Modrak et al. |
| Ni(acac)₂ | PLE | Esters | 90-95% | 97% | Typical DKR |

## E-value Scale

| E range | Selectivity | Description |
|---|---|---|
| >200 | Excellent | Commercial resolution viable |
| 50-200 | Very good | Good resolution with moderate conversion |
| 20-50 | Good | Acceptable with optimization |
| 5-20 | Moderate | DKR recommended |
| 1-5 | Poor | Not viable for simple resolution |
