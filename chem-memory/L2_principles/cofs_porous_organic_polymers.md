# L2 Topic: COFs & Porous Organic Polymers

**Source**: Expert knowledge; Côté et al., Science 2005; Jiang & Yaghi, Chem. Rev. 2015
**Created**: 2026-03-24
**Status**: Pass-1

---

## Covalent Organic Frameworks (COFs)

COFs are crystalline porous polymers linked by strong covalent bonds. Unlike MOFs, they contain only light elements (C, H, O, N, B).

### Linkage Types

| Linkage | Reaction | Reversibility | Stability |
|---------|----------|--------------|-----------|
| **Boronic ester** | Boronic acid + diol | Reversible | Moderate (hydrolytic sensitivity) |
| **Boroxine** | Boronic acid self-condensation | Reversible | Low |
| **Imine (β-ketoenamine)** | Aldehyde + amine → then tautomerize | Reversible | High (COF-300, COF-1) |
| **Hydrazone** | Aldehyde + hydrazide | Reversible | Moderate-High |
| **Imide** | Anhydride + amine | Irreversible (kinetic) | Very High |
| **Triazine** | Trimerization of nitrile | Irreversible | Very High (CTFs) |

### Notable COFs

| COF | Linkage | BET (m²/g) | Feature |
|-----|---------|-----------|---------|
| COF-1 | Boroxine | 711 | First COF (2005) |
| COF-5 | Boronic ester | 1590 | 2D hexagonal |
| COF-300 | Imine | 416 | 3D diamondoid |
| TpPa-1 | β-Ketoenamine | 588 | Chemical stability |
| Porphyrin COFs | Imine/boronic ester | 500-1400 | Photocatalysis, CO₂ reduction |

---

## Other Porous Organic Polymers (POPs)

| Class | Synthesis | Porosity | Applications |
|-------|-----------|----------|-------------|
| **PAFs** (Porous Aromatic Frameworks) | Yamamoto coupling | 1000-5600 m²/g | Gas storage, adsorption |
| **Hypercrosslinked Polymers (HCPs)** | Friedel-Crafts post-crosslinking | 500-2000 m²/g | Gas capture, water treatment |
| **CMPs** (Conjugated Microporous Polymers) | Sonogashira, Suzuki coupling | 500-2000 m²/g | Light harvesting, conductivity |
| **CTFs** (Covalent Triazine Frameworks) | Trimerization of nitriles (ZnCl₂, 400°C) | 500-2500 m²/g | Catalysis, CO₂ capture |
| **PIMs** (Polymers of Intrinsic Microporosity) | Step-growth with contorted monomers | 300-1000 m²/g | Gas separation membranes |

### MOFs vs. COFs vs. POPs

| Property | MOFs | COFs | POPs |
|----------|------|------|------|
| Crystallinity | Yes | Yes | Amorphous (usually) |
| Metal content | Yes | No | No |
| Stability | Varies (water-sensitive MOFs exist) | Good (β-ketoenamine) | Excellent |
| Surface area | 100-10000 m²/g | 500-4000 m²/g | 500-5600 m²/g |
| Designability | High (reticular) | High (reticular) | Moderate |

---

## L3 Tools
- `../L3_functions/mof_tools.py` → `surface_area_bet()`, `pore_volume_calc()`
