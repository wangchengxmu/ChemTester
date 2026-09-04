"""
heterocyclic_tools.py — Heterocyclic Chemistry Analysis Toolkit

Functions:
  heterocycle_info(name) — properties of 50+ heterocycles
  aromaticity_check(smiles_or_formula) — Hückel rule analysis
  synthesis_recommend(name, preferred_method) — synthesis routes
  electrophilic_substitution_positions(name) — EAS prediction
  bioisostere_suggest(name) — bioisosteric replacements
  snar_predictor(name, leaving_group, nucleophile) — SnAr feasibility

Uses only stdlib (+ RDKit if available for SMILES parsing).
"""

from __future__ import annotations
import re
from typing import Optional

try:
    from rdkit import Chem; _RDKIT = True
except ImportError:
    _RDKIT = False

# ═══════════════════════════════════════════════════════════════════════════
# DATABASE — 50+ heterocycles
# Keys: lowercase common name.
# ═══════════════════════════════════════════════════════════════════════════
_DB: dict[str, dict] = {}

def _a(fmt, smi, rs, het, aro, pka_a, pka_b, nics, dip, snar, synth, esub):
    return dict(formula=fmt, smiles=smi, ring_size=rs, heteroatoms=het,
                aromatic=aro, pKa_acid=pka_a, pKa_base=pka_b, nics1=nics,
                dipole=dip, snar=snar, synthesis=synth, e_sub=esub)

# ── Five-membered ──────────────────────────────────────────────────
_DB["pyrrole"] = _a("C4H5N","C1=CNC=C1",5,["N"],True,23.0,-3.8,-11.5,1.80,"poor",
    ["Paal-Knorr synthesis","Knorr pyrrole synthesis","Hantzsch pyrrole synthesis","Barton-Zard synthesis"],
    [(2,"alpha, electron-rich via resonance"),(3,"beta, less activated"),(1,"N-H substitution (rare)")])
_DB["furan"] = _a("C4H4O","C1=COC=C1",5,["O"],True,None,-2.0,-9.7,0.66,"poor",
    ["Paal-Knorr synthesis","Feist-Benary synthesis","Ag-catalyzed cyclization"],
    [(2,"alpha, most electron-rich"),(3,"beta, less activated")])
_DB["thiophene"] = _a("C4H4S","C1=CSC=C1",5,["S"],True,None,-2.5,-13.0,0.52,"poor",
    ["Paal-Knorr synthesis","Hinsberg synthesis","Gewald reaction"],
    [(2,"alpha, most reactive"),(3,"beta, less reactive")])
_DB["pyrazole"] = _a("C3H4N2","C1=CC=NN1",5,["N","N"],True,14.2,2.5,-12.0,2.20,"moderate",
    ["1,3-Dipolar cycloaddition of diazo compounds","Condensation of hydrazine with 1,3-diketones"],
    [(4,"para to pyridine N")])
_DB["imidazole"] = _a("C3H4N2","C1=NC=CN1",5,["N","N"],True,14.5,7.0,-12.5,3.70,"poor",
    ["Debus-Radziszewski imidazole synthesis"],
    [(4,"between two N, most electron-rich"),(2,"pyrrole-type N side"),(5,"symmetric to C-4")])
_DB["oxazole"] = _a("C3H3NO","C1=COC=N1",5,["N","O"],True,None,0.5,-10.5,1.40,"moderate",
    ["Robinson-Gabriel synthesis","Van Leusen oxazole synthesis"],
    [(5,"C-5 most electron-rich"),(4,"less reactive")])
_DB["thiazole"] = _a("C3H3NS","C1=NC=CS1",5,["N","S"],True,None,2.5,-11.2,1.60,"good",
    ["Hantzsch thiazole synthesis","Cook-Heilbron synthesis"],
    [(5,"C-5 most electron-rich"),(4,"less reactive")])
_DB["isoxazole"] = _a("C3H3NO","C1=CON=C1",5,["N","O"],True,None,-1.0,-9.3,2.60,"moderate",
    ["1,3-Dipolar cycloaddition (nitrile oxide + alkyne)"],
    [(4,"only practical EAS site")])
_DB["1,2,3-triazole"] = _a("C2H3N3","C1=NNN=N1",5,["N","N","N"],True,9.3,1.2,-13.8,4.80,"good",
    ["Click chemistry: CuAAC azide-alkyne cycloaddition"],[])
_DB["1,2,4-triazole"] = _a("C2H3N3","C1=NN=CN1",5,["N","N","N"],True,10.3,2.2,-13.2,4.20,"good",
    ["Einhorn-Brunner triazole synthesis","Pellizzari reaction"],[])
_DB["tetrazole"] = _a("CH2N4","C1=NNN=N1",5,["N","N","N","N"],True,4.9,None,-14.0,5.10,"excellent",
    ["[2+3] cycloaddition of azide with nitrile"],[])
_DB["1,3,4-thiadiazole"] = _a("C2H2N2S","C1=NN=CS1",5,["N","N","S"],True,None,None,-10.8,3.50,"good",
    ["From thiosemicarbazide + POCl3"],[])
_DB["1,3,4-oxadiazole"] = _a("C2H2N2O","C1=NN=CO1",5,["N","N","O"],True,None,None,-10.2,2.90,"moderate",
    ["From acylhydrazides + POCl3"],[])
_DB["1,2,5-oxadiazole"] = _a("C2H2N2O","C1=NO=CC=N1",5,["N","N","O"],True,None,None,-9.5,3.10,"good",
    ["From vicinal dioximes (furazan synthesis)"],[])
_DB["selenophene"] = _a("C4H4Se","C1=C[Se]C=C1",5,["Se"],True,None,-2.5,-12.0,0.55,"poor",
    ["From 1,4-diketones + Se source"],[(2,"alpha, most reactive"),(3,"beta")])

# ── Six-membered ───────────────────────────────────────────────────
_DB["pyridine"] = _a("C5H5N","C1=CC=NC=C1",6,["N"],True,None,5.25,-10.0,2.19,"good",
    ["Hantzsch dihydropyridine synthesis + oxidation","Krohnke pyridine synthesis","Boennemann cyclization"],
    [(3,"meta to N, least deactivated"),(4,"para to N"),(2,"ortho to N, most deactivated")])
_DB["pyridazine"] = _a("C4H4N2","C1=CC=NN=C1",6,["N","N"],True,None,2.3,-8.5,4.10,"excellent",
    ["Condensation of 1,4-diketones with hydrazine"],[(4,"between two N")])
_DB["pyrimidine"] = _a("C4H4N2","C1=NC=CC=N1",6,["N","N"],True,None,1.3,-7.5,2.10,"good",
    ["Pinner pyrimidine synthesis","Biginelli reaction"],
    [(5,"least deactivated"),(4,"C-4"),(2,"most deactivated")])
_DB["pyrazine"] = _a("C4H4N2","C1=NC=CN=C1",6,["N","N"],True,None,0.6,-7.0,0.0,"good",
    ["Condensation of alpha-diketones with ethylenediamine"],
    [(2,"all positions equivalent, deactivated")])
_DB["pyridone"] = _a("C5H5NO","O=C1C=CC=CN1",6,["N","O"],False,11.6,None,-3.5,4.10,"moderate",
    ["Hydrolysis of 2-pyridyl halides"],[(3,"moderate activation"),(5,"similar to C-3")])
_DB["pyran"] = _a("C5H6O","C1=CC=CC=C1O",6,["O"],False,None,None,0.5,1.50,"poor",
    ["From dihydropyran oxidation"],[])
_DB["pyrylium"] = _a("C5H5O+","C1=CC=[O+]=CC=C1",6,["O"],True,None,None,-12.0,5.80,"excellent",
    ["From 1,5-diketones under acid","Krohnke pyrylium synthesis"],
    [(2,"very electrophilic, alpha substitution")])
_DB["pyridine n-oxide"] = _a("C5H5NO","O=[N+]1=CC=CC=C1",6,["N","O"],True,None,0.8,-9.5,4.30,"good",
    ["Oxidation of pyridine with mCPBA"],
    [(2,"activated by N-oxide, ortho"),(4,"para to N-oxide, strongly activated")])
_DB["piperidine"] = _a("C5H11N","N1CCCCC1",6,["N"],False,11.2,None,0.0,1.10,"poor",
    ["Catalytic hydrogenation of pyridine"],[])
_DB["morpholine"] = _a("C4H9NO","C1COCCN1",6,["N","O"],False,8.36,None,0.0,1.50,"poor",
    ["Bis(2-chloroethyl)ether + ammonia"],[])
_DB["piperazine"] = _a("C4H10N2","N1CCNCC1",6,["N","N"],False,9.8,None,0.0,1.30,"poor",
    ["Ethylene dichloride + ammonia"],[])
_DB["1,3,5-triazine"] = _a("C3H3N3","C1=NC=NC=N1",6,["N","N","N"],True,None,-1.0,-8.0,0.0,"excellent",
    ["Trimerization of nitriles"],[])
_DB["1,2,4-triazine"] = _a("C3H3N3","C1=NC=NN=C1",6,["N","N","N"],True,None,-1.5,-7.2,3.50,"excellent",
    ["From alpha-dicarbonyls + amidrazones"],[(5,"least deactivated")])
_DB["1,2,4,5-tetrazine"] = _a("C2H2N4","C1=NN=NN=N1",6,["N","N","N","N"],True,None,-3.0,-7.8,0.0,"excellent",
    ["From amidrazone + nitrous acid"],[])
_DB["pyrimidinone"] = _a("C4H4N2O","O=C1NC=CC=N1",6,["N","N","O"],False,9.7,None,-2.8,3.80,"moderate",
    ["Condensation of urea with 1,3-dicarbonyls"],[(5,"least deactivated")])
_DB["dioxane"] = _a("C4H8O2","C1COCOCO1",6,["O","O"],False,None,None,0.0,0.45,"poor",
    ["Acid-catalyzed dimerization of ethylene oxide"],[])
_DB["pyranone"] = _a("C5H4O2","O=C1C=CC=CO1",6,["O","O"],False,None,None,-2.0,3.20,"poor",
    ["Pyrylium hydrolysis"],[])

# ── Fused bicyclic 5+6 ────────────────────────────────────────────
_DB["indole"] = _a("C8H7N","C1=CC=C2C(=C1)C=CN2","5+6",["N"],True,21.0,-3.5,-10.5,2.10,"poor",
    ["Fischer indole synthesis","Bischler indole synthesis","Leimgruber-Batcho synthesis","Larock indole synthesis"],
    [(3,"pyrrole C-3, most electron-rich"),(2,"pyrrole C-2"),(5,"benzene ring, ortho to N")])
_DB["isoindole"] = _a("C8H7N","C1=CC=C2C=CC=C2N1","5+6",["N"],True,20.5,-2.5,-9.8,1.90,"poor",
    ["From phthalimide reduction"],[(1,"N-adjacent"),(3,"peri position")])
_DB["benzofuran"] = _a("C8H6O","C1=CC=C2C=CC=CO2","5+6",["O"],True,None,-1.0,-9.5,0.75,"poor",
    ["Perkin rearrangement","Pechmann condensation","Au-catalyzed cyclization"],
    [(2,"furan alpha"),(3,"furan beta")])
_DB["benzothiophene"] = _a("C8H6S","C1=CC=C2C=CC=CS2","5+6",["S"],True,None,-1.5,-11.0,0.60,"poor",
    ["From o-haloaryl ketones + Na2S"],[(2,"thiophene alpha"),(3,"thiophene beta")])
_DB["indazole"] = _a("C7H6N2","C1=CC=C2C=NN=C2C1","5+6",["N","N"],True,14.0,1.2,-10.2,2.80,"moderate",
    ["Bartoli indazole synthesis"],[(3,"N-adjacent"),(5,"benzene ring")])
_DB["benzimidazole"] = _a("C7H6N2","C1=CC=C2C(=C1)NC=N2","5+6",["N","N"],True,12.8,5.5,-11.5,3.90,"moderate",
    ["Phillips synthesis (o-phenylenediamine + acid)"],[(5,"benzene ring, para to imidazole")])
_DB["benzoxazole"] = _a("C7H5NO","C1=CC=C2C=NO=C2C1","5+6",["N","O"],True,None,0.5,-9.8,2.10,"moderate",
    ["From o-aminophenol + carboxylic acid + POCl3"],[(5,"benzene ring")])
_DB["benzothiazole"] = _a("C7H5NS","C1=CC=C2C=NC=S2C1","5+6",["N","S"],True,None,1.2,-10.5,2.30,"good",
    ["From o-aminothiophenol + carboxylic acid"],[(5,"benzene ring")])
_DB["purine"] = _a("C5H4N4","C1=NC2=C(N1)N=CN=C2N","5+6",["N","N","N","N"],True,8.9,2.5,-9.0,3.50,"good",
    ["Traube purine synthesis"],[])

# ── Fused bicyclic 6+6 ────────────────────────────────────────────
_DB["quinoline"] = _a("C9H7N","C1=NC2=CC=CC=C2=C1","6+6",["N"],True,None,4.85,-9.5,2.20,"good",
    ["Skraup synthesis","Doebner-Miller synthesis","Friedlander synthesis","Combes synthesis","Pfitzinger reaction"],
    [(5,"fused ring, meta to N"),(8,"fused ring, ortho to N"),(3,"pyridine C-3")])
_DB["isoquinoline"] = _a("C9H7N","C1=CC=C2C=NC=CC2=C1","6+6",["N"],True,None,5.40,-9.8,2.60,"good",
    ["Bischler-Napieralski reaction","Pictet-Spengler reaction","Pomeranz-Fritsch synthesis"],
    [(5,"benzene ring"),(8,"furthest from N"),(1,"pyridine C-1")])
_DB["acridine"] = _a("C13H9N","C1=CC=C2C(=C1)C3=CC=CC=C3N2","6+6+6",["N"],True,None,5.60,-8.5,2.50,"good",
    ["Bernthsen acridine synthesis"],[(2,"peri position"),(4,"para to N")])
_DB["phenanthridine"] = _a("C13H9N","C1=CC=C2C=CC3=CC=CC=C3N2C1","6+6+6",["N"],True,None,4.60,-8.2,2.30,"good",
    ["Bischler-Napieralski on biphenyl-2-carboxamide"],[(3,"benzene ring")])
_DB["pteridine"] = _a("C6H4N4","C1=NC2=NC=NC=C2N1","6+6",["N","N","N","N"],True,None,0.0,-8.0,3.00,"excellent",
    ["From 4,5-diaminopyrimidine + glyoxal"],[])
_DB["quinazoline"] = _a("C8H6N2","C1=NC2=CC=CC=C2=N1","6+6",["N","N"],True,None,3.5,-8.0,2.50,"good",
    ["From anthranilic acid + formamide (Niementowski)"],
    [(5,"benzene ring, meta to N"),(7,"benzene ring")])
_DB["quinoxaline"] = _a("C8H6N2","C1=CC=NC2=CC=CC=N12","6+6",["N","N"],True,None,0.6,-7.5,0.50,"good",
    ["From o-phenylenediamine + alpha-diketone"],[(5,"benzene ring, meta to N")])
_DB["cinnoline"] = _a("C8H6N2","C1=CC=CC2=NN=CC=C12","6+6",["N","N"],True,None,2.3,-7.8,3.80,"excellent",
    ["From o-aminoaryl diazonium + beta-ketoester (von Richter)"],
    [(4,"between two N, least deactivated")])
_DB["phthalazine"] = _a("C8H6N2","C1=CC=C2C=NN=CC2=C1","6+6",["N","N"],True,None,3.5,-8.3,2.40,"good",
    ["From phthalaldehyde + hydrazine"],[(5,"benzene ring, meta to N")])

# ── Seven-membered ─────────────────────────────────────────────────
_DB["azepine"] = _a("C6H7N","C1=CCCC=N1",7,["N"],False,None,None,1.0,1.50,"poor",
    ["Schmidt reaction on cyclohexanone"],[])
_DB["oxepine"] = _a("C6H6O","C1=CCCC=CO1",7,["O"],False,None,None,0.5,1.30,"poor",
    ["From epsilon-caprolactone reduction"],[])
_DB["diazepine"] = _a("C5H6N2","C1=CC=CN=N1",7,["N","N"],False,None,None,1.5,2.00,"moderate",
    ["From o-phenylenediamine derivatives + beta-diketones"],[])

# ── Aliases ────────────────────────────────────────────────────────
_ALIASES = {
    "azaindole": "indole", "indolizine": "indole",
    "carbazole": "indole", "pyrrolopyridine": "indole",
    "2-pyridone": "pyridone", "4-pyridone": "pyridone",
    "uracil": "pyrimidinone", "cytosine": "pyrimidinone",
    "thymine": "pyrimidinone",
    "quinazolinone": "quinazoline",
}

# ═══════════════════════════════════════════════════════════════════════════
# 1. heterocycle_info
# ═══════════════════════════════════════════════════════════════════════════
def heterocycle_info(name: str) -> dict:
    """Return properties of a named heterocycle.

    Parameters
    ----------
    name : str
        Common name, e.g. 'pyrrole', 'pyridine', 'indole'. Case-insensitive.
        Aliases like 'uracil' -> 'pyrimidinone' are resolved.

    Returns
    -------
    dict with keys: formula, smiles, ring_size, heteroatoms, aromatic,
        pKa_acid, pKa_base, nics1, dipole, snar, synthesis, e_sub.
        Raises KeyError if not found (with list of available names).
    """
    key = name.strip().lower()
    key = _ALIASES.get(key, key)
    if key not in _DB:
        available = sorted(_DB.keys())
        raise KeyError(
            f"Heterocycle '{name}' not found. Available: {available}")
    entry = _DB[key].copy()
    entry["name"] = key
    return entry

def list_heterocycles() -> list[str]:
    """Return sorted list of all known heterocycle names."""
    return sorted(_DB.keys())

# ═══════════════════════════════════════════════════════════════════════════
# 2. aromaticity_check
# ═══════════════════════════════════════════════════════════════════════════
def aromaticity_check(smiles_or_formula: str) -> dict:
    """Check aromaticity of a heterocycle using Hückel's rule.

    Parameters
    ----------
    smiles_or_formula : str
        SMILES string or molecular formula.

    Returns
    -------
    dict with keys: input, pi_electrons, huckel_4n2 (bool), aromatic (bool),
        method ('huckel' or 'rdkit' or 'database'), explanation.
    """
    s = smiles_or_formula.strip()

    # Try RDKit if available and input looks like SMILES
    if _RDKIT and not re.match(r'^[A-Z][a-z]?\d*(\([A-Za-z]\))?\d*$', s):
        mol = Chem.MolFromSmiles(s)
        if mol is not None:
            pi_count = 0
            for atom in mol.GetAtoms():
                # Count sp2 heteroatoms contributing lone pair (pyrrole-type)
                # and pi electrons from double bonds
                hybrid = atom.GetHybridization()
                if hybrid == Chem.HybridizationType.SP2:
                    if atom.GetAtomicNum() in (7, 15):  # N, P
                        # Check if pyrrole-type (3 bonds, lone pair in ring)
                        degree = atom.GetDegree()
                        if degree == 3 and atom.IsInRing():
                            pi_count += 2  # lone pair + 1 from bond
                        else:
                            pi_count += 1  # pyridine-type (no lone pair)
                    elif atom.GetAtomicNum() in (8, 16, 34):  # O, S, Se
                        degree = atom.GetDegree()
                        if degree == 2 and atom.IsInRing():
                            pi_count += 2  # furan/thiophene-type
                    else:
                        pi_count += 1  # C in double bond
            # Also count non-sp2 ring atoms for pi electrons from conjugation
            # RDKit aromaticity flag
            rdkit_arom = Chem.Descriptors.NumAromaticRings(mol) > 0

            huckel = (pi_count >= 2) and ((pi_count - 2) % 4 == 0)
            return dict(
                input=s, pi_electrons=pi_count, huckel_4n2=huckel,
                aromatic=rdkit_arom, method="rdkit+huckel",
                explanation=f"RDKit aromatic rings={Chem.Descriptors.NumAromaticRings(mol)}, "
                            f"estimated pi={pi_count}, Hückel (4n+2): {huckel}"
            )

    # Formula parsing — count pi electrons from formula + heuristics
    # Try to match against database first
    for key, entry in _DB.items():
        if entry["formula"] == s or entry["smiles"] == s:
            pi_est = _estimate_pi_electrons(entry)
            huckel = (pi_est >= 2) and ((pi_est - 2) % 4 == 0)
            return dict(
                input=s, pi_electrons=pi_est, huckel_4n2=huckel,
                aromatic=entry["aromatic"], method="database",
                explanation=f"Matched '{key}' in database. "
                            f"pi≈{pi_est}, Hückel (4n+2): {huckel}"
            )

    # Simple formula heuristic
    pi_est = _pi_from_formula(s)
    huckel = (pi_est >= 2) and ((pi_est - 2) % 4 == 0)
    return dict(
        input=s, pi_electrons=pi_est, huckel_4n2=huckel,
        aromatic=huckel, method="formula_heuristic",
        explanation=f"Estimated pi={pi_est} from formula '{s}'. "
                    f"Hückel prediction: {'aromatic' if huckel else 'non-aromatic'}. "
                    f"Low confidence — use SMILES for better results."
    )

def _estimate_pi_electrons(entry: dict) -> int:
    """Rough pi electron count from database entry."""
    het = entry["heteroatoms"]
    rs = entry["ring_size"]
    # 5-membered: 6 pi (4n+2, n=1) if aromatic
    if isinstance(rs, int) and rs == 5 and entry["aromatic"]:
        return 6
    # 6-membered: 6 pi if aromatic
    if isinstance(rs, int) and rs == 6 and entry["aromatic"]:
        return 6
    # 7-membered: 6 pi if aromatic (azepine)
    if isinstance(rs, int) and rs == 7 and entry["aromatic"]:
        return 6
    # Fused: use 10 or 14 depending on rings
    if isinstance(rs, str):
        n_rings = len(rs.split("+"))
        return 4 * n_rings + 2  # 10 for 2 fused, 14 for 3 fused
    return 0

def _pi_from_formula(formula: str) -> int:
    """Very rough pi electron estimate from molecular formula."""
    # Count atoms
    elements = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    counts = {}
    for el, num in elements:
        counts[el] = int(num) if num else 1
    c = counts.get("C", 0)
    n = counts.get("N", 0)
    o = counts.get("O", 0)
    s = counts.get("S", 0)
    h = counts.get("H", 0)
    # Degree of unsaturation
    dou = (2*c + 2 + n - h) // 2 - o // 2  # simplified
    # Each double bond/ring contributes 2 pi electrons, heteroatoms may add lone pairs
    pi = dou * 2
    # Subtract sigma bonds to O, S that don't contribute pi
    pi -= (o + s)
    return max(pi, 0)

# ═══════════════════════════════════════════════════════════════════════════
# 3. synthesis_recommend
# ═══════════════════════════════════════════════════════════════════════════
_SYNTHESIS_DETAILS: dict[str, list[dict]] = {
    "Paal-Knorr synthesis": dict(
        category="condensation",
        reagents="1,4-diketone + primary amine (pyrrole) or acid catalyst (furan/thiophene)",
        conditions="Reflux in AcOH or TsOH, 80-120 C",
        yield_range="50-90%"),
    "Knorr pyrrole synthesis": dict(
        category="condensation",
        reagents="alpha-amino ketone + beta-keto ester",
        conditions="Acid catalysis, reflux",
        yield_range="40-70%"),
    "Hantzsch pyrrole synthesis": dict(
        category="condensation",
        reagents="beta-keto ester + alpha-halo ketone + ammonia/amine",
        conditions="Ethanol, reflux",
        yield_range="50-80%"),
    "Barton-Zard synthesis": dict(
        category="condensation",
        reagents="Nitroalkene + isocyanoacetate",
        conditions="DBU, THF, rt to 60 C",
        yield_range="30-70%"),
    "Fischer indole synthesis": dict(
        category="named_reaction",
        reagents="Aryl hydrazine + ketone/aldehyde",
        conditions="ZnCl2 or polyphosphoric acid, 80-200 C",
        yield_range="40-90%"),
    "Bischler indole synthesis": dict(
        category="named_reaction",
        reagents="alpha-halo ketone + excess aniline",
        conditions="Reflux in EtOH or AcOH, 100-150 C",
        yield_range="20-60%"),
    "Leimgruber-Batcho indole synthesis": dict(
        category="named_reaction",
        reagents="o-Nitrotoluene + DMF-DMA, then reduction",
        conditions="DMF-DMA 150 C; then SnCl2/HCl or catalytic hydrogenation",
        yield_range="55-80%"),
    "Larock indole synthesis": dict(
        category="named_reaction",
        reagents="o-Iodoaniline + alkyne",
        conditions="Pd catalyst, base, DMF, 100 C",
        yield_range="60-95%"),
    "Hantzsch thiazole synthesis": dict(
        category="named_reaction",
        reagents="alpha-halo ketone + thioamide",
        conditions="Ethanol, reflux, 2-6 h",
        yield_range="50-90%"),
    "Debus-Radziszewski imidazole synthesis": dict(
        category="named_reaction",
        reagents="1,2-Dicarbonyl + aldehyde + ammonia",
        conditions="AcOH or NH4OAc, reflux",
        yield_range="50-85%"),
    "Skraup synthesis": dict(
        category="named_reaction",
        reagents="Aniline + glycerol + sulfuric acid + oxidant (nitrobenzene)",
        conditions="Conc. H2SO4, 100-120 C, exothermic",
        yield_range="30-60%"),
    "Doebner-Miller synthesis": dict(
        category="named_reaction",
        reagents="Aniline + alpha,beta-unsaturated aldehyde (acrolein)",
        conditions="HCl, reflux",
        yield_range="30-70%"),
    "Friedlander synthesis": dict(
        category="named_reaction",
        reagents="o-Aminoaryl ketone + ketone with alpha-methylene",
        conditions="NaOH or KOH, EtOH, reflux",
        yield_range="50-90%"),
    "Bischler-Napieralski reaction": dict(
        category="named_reaction",
        reagents="beta-Phenylethylamide + POCl3 or P2O5",
        conditions="Toluene, reflux, then reduction",
        yield_range="40-75%"),
    "Pictet-Spengler reaction": dict(
        category="named_reaction",
        reagents="beta-Phenylethylamine + aldehyde",
        conditions="Acid, rt or reflux",
        yield_range="50-95%"),
    "Pomeranz-Fritsch synthesis": dict(
        category="named_reaction",
        reagents="Benzaldehyde + aminoacetaldehyde diethyl acetal",
        conditions="Strong acid (HCl, H2SO4), 150-200 C",
        yield_range="20-40%"),
    "Phillips synthesis": dict(
        category="condensation",
        reagents="o-Phenylenediamine + carboxylic acid",
        conditions="HCl, 180-250 C (or H3PO4)",
        yield_range="40-80%"),
    "Hantzsch dihydropyridine synthesis + oxidation": dict(
        category="named_reaction",
        reagents="Aldehyde + 2 eq beta-keto ester + NH3",
        conditions="EtOH, reflux, then oxidation (HNO3 or MnO2)",
        yield_range="40-80%"),
    "Gewald reaction": dict(
        category="named_reaction",
        reagents="Ketone + sulfur + cyanoacetate",
        conditions="Morpholine or Et3N, EtOH, rt",
        yield_range="40-75%"),
    "1,3-Dipolar cycloaddition of diazo compounds": dict(
        category="cycloaddition",
        reagents="Diazo compound + alkyne or alkene",
        conditions="Cu or Rh catalysis, rt-80 C",
        yield_range="50-90%"),
    "Click chemistry: CuAAC azide-alkyne cycloaddition": dict(
        category="cycloaddition",
        reagents="Azide + terminal alkyne",
        conditions="CuSO4 + sodium ascorbate, t-BuOH/H2O, rt",
        yield_range="80-99%"),
    "Feist-Benary synthesis": dict(
        category="condensation",
        reagents="alpha-Halo ketone + beta-keto ester",
        conditions="Pyridine, reflux",
        yield_range="30-60%"),
    "Robinson-Gabriel synthesis": dict(
        category="condensation",
        reagents="2-Acylamino ketone + dehydrating agent",
        conditions="H2SO4 or P2O5, heat",
        yield_range="40-70%"),
    "Van Leusen oxazole synthesis": dict(
        category="named_reaction",
        reagents="Tosylmethyl isocyanide (TosMIC) + aldehyde",
        conditions="K2CO3, MeOH, rt-60 C",
        yield_range="50-85%"),
    "Biginelli reaction": dict(
        category="condensation",
        reagents="Aldehyde + beta-keto ester + urea",
        conditions="HCl, EtOH, reflux",
        yield_range="40-80%"),
    "Traube purine synthesis": dict(
        category="named_reaction",
        reagents="4,5-Diaminopyrimidine + formic acid (or triethyl orthoformate)",
        conditions="Heat, 100-180 C",
        yield_range="50-75%"),
    "Bernthsen acridine synthesis": dict(
        category="named_reaction",
        reagents="Diphenylamine + carboxylic acid + ZnCl2",
        conditions="ZnCl2, 200-250 C",
        yield_range="30-60%"),
    "Combes synthesis": dict(
        category="condensation",
        reagents="o-Aminoaryl ketone + beta-diketone",
        conditions="Acid, reflux",
        yield_range="50-80%"),
    "Pfitzinger reaction": dict(
        category="condensation",
        reagents="Isatin + carbonyl compound + base",
        conditions="KOH, EtOH, reflux",
        yield_range="40-75%"),
    "Niementowski quinazoline synthesis": dict(
        category="named_reaction",
        reagents="Anthranilic acid + amide (or formamide)",
        conditions="Heat 180-220 C",
        yield_range="50-80%"),
    "Krohnke pyridine synthesis": dict(
        category="named_reaction",
        reagents="alpha-Pyridinium methyl ketone salt + alpha,beta-unsaturated ketone + NH3",
        conditions="NH4OAc, AcOH, reflux",
        yield_range="50-80%"),
    "Krohnke pyrylium synthesis": dict(
        category="named_reaction",
        reagents="2,4,6-Trimethylpyrylium route",
        conditions="Ac2O, 100-150 C",
        yield_range="40-70%"),
    "From 1,5-diketones under acid": dict(
        category="condensation",
        reagents="1,5-Diketone + H2SO4 or HClO4",
        conditions="Strong acid, 0-50 C",
        yield_range="50-80%"),
    "Trimerization of nitriles": dict(
        category="cycloaddition",
        reagents="Nitrile (3 eq) + acid catalyst",
        conditions="ZnCl2 or HCl, high temperature",
        yield_range="20-60%"),
    "From amidrazone + nitrous acid": dict(
        category="condensation",
        reagents="Amidrazone + NaNO2/AcOH",
        conditions="AcOH, 0-25 C",
        yield_range="40-70%"),
    "From vicinal dioximes (furazan synthesis)": dict(
        category="condensation",
        reagents="Vicinal dioxime + dehydrating agent",
        conditions="SOCl2 or P2O5, reflux",
        yield_range="30-65%"),
    "From thiosemicarbazide + POCl3": dict(
        category="condensation",
        reagents="Thiosemicarbazide + carboxylic acid + POCl3",
        conditions="POCl3, reflux",
        yield_range="40-70%"),
    "From acylhydrazides + POCl3": dict(
        category="condensation",
        reagents="Acylhydrazide + POCl3",
        conditions="Reflux, 80-120 C",
        yield_range="40-75%"),
    "Einhorn-Brunner triazole synthesis": dict(
        category="condensation",
        reagents="Hydrazine + imidate ester",
        conditions="Reflux in ethanol",
        yield_range="40-70%"),
    "Pellizzari reaction": dict(
        category="condensation",
        reagents="Acylhydrazide + amide + heat",
        conditions="Heat 200-300 C",
        yield_range="20-40%"),
    "Bartoli indazole synthesis": dict(
        category="named_reaction",
        reagents="o-Substituted nitrobenzene + vinyl Grignard",
        conditions="Vinylmagnesium bromide, THF, -40 to 0 C",
        yield_range="40-70%"),
    "Condensation of hydrazine with 1,3-diketones": dict(
        category="condensation",
        reagents="Hydrazine + 1,3-diketone",
        conditions="EtOH, reflux",
        yield_range="60-90%"),
    "Condensation of urea with 1,3-dicarbonyls": dict(
        category="condensation",
        reagents="Urea + 1,3-dicarbonyl compound",
        conditions="Acid or base, reflux",
        yield_range="50-85%"),
    "From phthalimide reduction": dict(
        category="condensation",
        reagents="Phthalimide + reducing agent (LiAlH4)",
        conditions="LiAlH4, THF, reflux",
        yield_range="30-60%"),
    "Condensation of alpha-diketones with ethylenediamine": dict(
        category="condensation",
        reagents="alpha-Diketone + ethylenediamine",
        conditions="EtOH, reflux",
        yield_range="50-85%"),
    "Condensation of 1,4-diketones with hydrazine": dict(
        category="condensation",
        reagents="1,4-Diketone + hydrazine",
        conditions="AcOH, reflux",
        yield_range="40-75%"),
    "Oxidation of pyridine with mCPBA": dict(
        category="named_reaction",
        reagents="Pyridine + mCPBA or H2O2/AcOH",
        conditions="DCM, rt (mCPBA) or AcOH, 80 C (H2O2)",
        yield_range="70-95%"),
    "Catalytic hydrogenation of pyridine": dict(
        category="named_reaction",
        reagents="Pyridine + H2 + catalyst (PtO2, Rh/C)",
        conditions="High pressure H2, acidic conditions",
        yield_range="60-90%"),
    "Ag-catalyzed cyclization": dict(
        category="named_reaction",
        reagents="Alkyne + phenol/alcohol + Ag catalyst",
        conditions="AgOTf or Ag2O, DCM, rt",
        yield_range="40-75%"),
    "Cook-Heilbron synthesis": dict(
        category="condensation",
        reagents="alpha-Aminonitrile + CS2 or COS",
        conditions="Base, then acid workup",
        yield_range="40-70%"),
    "Schmidt reaction on cyclohexanone": dict(
        category="named_reaction",
        reagents="Cyclohexanone + HN3 + acid",
        conditions="H2SO4, 0-50 C (DANGEROUS)",
        yield_range="30-60%"),
    "From o-aminothiophenol + carboxylic acid": dict(
        category="condensation",
        reagents="o-Aminothiophenol + carboxylic acid",
        conditions="Polyphosphoric acid, heat",
        yield_range="50-80%"),
    "From o-aminophenol + carboxylic acid + POCl3": dict(
        category="condensation",
        reagents="o-Aminophenol + carboxylic acid + POCl3",
        conditions="POCl3, reflux, then neutralization",
        yield_range="40-75%"),
    "Bis(2-chloroethyl)ether + ammonia": dict(
        category="condensation",
        reagents="Bis(2-chloroethyl)ether + ammonia (excess)",
        conditions="Sealed tube, 130-150 C",
        yield_range="50-80%"),
    "Ethylene dichloride + ammonia": dict(
        category="condensation",
        reagents="Ethylene dichloride + ammonia",
        conditions="Sealed tube, 130-150 C",
        yield_range="50-80%"),
    "From alpha-dicarbonyls + amidrazones": dict(
        category="condensation",
        reagents="alpha-Dicarbonyl + amidrazone",
        conditions="EtOH, reflux",
        yield_range="30-60%"),
    "From 4,5-diaminopyrimidine + glyoxal": dict(
        category="condensation",
        reagents="4,5-Diaminopyrimidine + glyoxal",
        conditions="EtOH, rt or reflux",
        yield_range="40-70%"),
    "Bischler-Napieralski on biphenyl-2-carboxamide": dict(
        category="named_reaction",
        reagents="Biphenyl-2-carboxamide + POCl3",
        conditions="Toluene, reflux, then reduction",
        yield_range="30-60%"),
    "Pyrylium hydrolysis": dict(
        category="condensation",
        reagents="Pyrylium salt + NaOH/H2O",
        conditions="Aqueous base, rt",
        yield_range="60-90%"),
    "Acid-catalyzed dimerization of ethylene oxide": dict(
        category="condensation",
        reagents="Ethylene oxide (2 eq) + acid",
        conditions="H2SO4, 50-100 C",
        yield_range="60-85%"),
    "From o-phenylenediamine + alpha-diketone": dict(
        category="condensation",
        reagents="o-Phenylenediamine + alpha-diketone",
        conditions="EtOH, reflux",
        yield_range="60-95%"),
    "From phthalaldehyde + hydrazine": dict(
        category="condensation",
        reagents="Phthalaldehyde + hydrazine",
        conditions="EtOH, rt",
        yield_range="50-80%"),
    "From o-aminoaryl diazonium + beta-ketoester (von Richter)": dict(
        category="named_reaction",
        reagents="o-Aminoaryl diazonium + beta-ketoester",
        conditions="Cu catalysis, aqueous",
        yield_range="30-60%"),
    "Diazo coupling + cyclization": dict(
        category="cycloaddition",
        reagents="Diazo compound + activated aromatic",
        conditions="Base or acid, rt-80 C",
        yield_range="30-60%"),
    "From o-haloaryl ketones + Na2S": dict(
        category="condensation",
        reagents="o-Haloacetophenone + Na2S",
        conditions="DMF, 100-150 C",
        yield_range="40-70%"),
    "Jacobsen cyclization": dict(
        category="named_reaction",
        reagents="o-Haloaryl sulfide + base",
        conditions="CuI, L-proline, K2CO3, DMSO, 80 C",
        yield_range="50-80%"),
    "Perkin rearrangement": dict(
        category="named_reaction",
        reagents="Coumarin + base + heat",
        conditions="KOH, 250 C",
        yield_range="30-50%"),
    "Pechmann condensation": dict(
        category="condensation",
        reagents="Phenol + beta-keto ester + acid",
        conditions="H2SO4 or Lewis acid, reflux",
        yield_range="40-80%"),
    "From formamide": dict(
        category="condensation",
        reagents="Formamide, high temperature",
        conditions="200-300 C",
        yield_range="15-40%"),
    "Boennemann cyclization": dict(
        category="named_reaction",
        reagents="Alkyne + nitrile + Co catalyst",
        conditions="Co2(CO)8, high pressure CO/H2",
        yield_range="20-50%"),
    "Madelung indole synthesis": dict(
        category="named_reaction",
        reagents="o-Toluidide derivative + strong base",
        conditions="NaNH2 or alkyl lithium, high temp",
        yield_range="20-50%"),
    "From o-haloaryl ketones + Na2S": dict(
        category="condensation",
        reagents="o-Haloacetophenone + Na2S",
        conditions="DMF, 100-150 C",
        yield_range="40-70%"),
    "From phthalimide reduction": dict(
        category="condensation",
        reagents="Phthalimide + LiAlH4 or BH3",
        conditions="THF, reflux",
        yield_range="30-60%"),
    "From epsilon-caprolactone reduction": dict(
        category="named_reaction",
        reagents="epsilon-Caprolactone + reducing agent",
        conditions="LiAlH4, THF",
        yield_range="50-80%"),
    "From o-phenylenediamine derivatives + beta-diketones": dict(
        category="condensation",
        reagents="o-Phenylenediamine + 1,3-diketone",
        conditions="EtOH, reflux",
        yield_range="50-80%"),
    "[2+3] cycloaddition of azide with nitrile": dict(
        category="cycloaddition",
        reagents="Organic azide + nitrile",
        conditions="ZnBr2 or Lewis acid, 80-120 C",
        yield_range="40-70%"),
    "From 1,4-diketones + Se source": dict(
        category="condensation",
        reagents="1,4-Diketone + Se or Woollins reagent",
        conditions="Reflux in xylene",
        yield_range="40-70%"),
    "From o-haloaryl ketones + Na2S": dict(
        category="condensation",
        reagents="o-Haloacetophenone + Na2S",
        conditions="DMF, 100-150 C",
        yield_range="40-70%"),
    "From vicinal dioximes + dehydrating agent (furazan synthesis)": dict(
        category="condensation",
        reagents="Vicinal dioxime + SOCl2 or P2O5",
        conditions="Reflux",
        yield_range="30-65%"),
}

def synthesis_recommend(heterocycle_name: str, preferred_method: Optional[str] = None) -> list[dict]:
    """Recommend synthesis routes for a target heterocycle.

    Parameters
    ----------
    heterocycle_name : str
        Target heterocycle name (case-insensitive).
    preferred_method : str, optional
        Filter by 'named_reaction', 'cycloaddition', or 'condensation'.

    Returns
    -------
    list of dict, each with keys: method, category, reagents, conditions, yield_range.
    """
    entry = heterocycle_info(heterocycle_name)
    methods = entry.get("synthesis", [])
    results = []
    for m in methods:
        details = _SYNTHESIS_DETAILS.get(m, {})
        cat = details.get("category", "unknown")
        if preferred_method and cat != preferred_method:
            continue
        results.append(dict(
            method=m,
            category=cat,
            reagents=details.get("reagents", "See literature"),
            conditions=details.get("conditions", "See literature"),
            yield_range=details.get("yield_range", "Variable"),
        ))
    return results

# ═══════════════════════════════════════════════════════════════════════════
# 4. electrophilic_substitution_positions
# ═══════════════════════════════════════════════════════════════════════════
def electrophilic_substitution_positions(heterocycle_name: str) -> list[dict]:
    """Predict preferred positions for electrophilic aromatic substitution.

    Parameters
    ----------
    heterocycle_name : str
        Heterocycle name (case-insensitive).

    Returns
    -------
    list of dict, each with keys: position (int), rationale (str).
        Sorted by reactivity (rank 1 = most reactive).
        Empty list if heterocycle is non-aromatic or too deactivated for EAS.
    """
    entry = heterocycle_info(heterocycle_name)
    if not entry["aromatic"]:
        return [{"note": f"{heterocycle_name} is not aromatic; EAS not applicable."}]
    positions = entry.get("e_sub", [])
    if positions:
        return [
            {"rank": i + 1, "position": pos, "rationale": rat}
            for i, (pos, rat) in enumerate(positions)
        ]
    return [
        {"note": f"{heterocycle_name} is too electron-deficient for practical EAS "
                 f"(too many deactivating N atoms)."}]

# ═══════════════════════════════════════════════════════════════════════════
# 5. bioisostere_suggest
# ═══════════════════════════════════════════════════════════════════════════
_BIOISOSTERE_MAP = {
    "pyridine": [
        ("pyrimidine", "Similar basicity (pKa ~1-5), aromatic 6-membered ring, H-bond acceptor"),
        ("pyridazine", "Similar electronics, stronger dipole may improve solubility"),
        ("pyrazine", "Weaker base, symmetrical, improved metabolic stability"),
        ("benzene", "Remove basicity entirely, increase lipophilicity"),
        ("1,3,5-triazine", "No basic N, very electron-deficient, resists metabolism"),
    ],
    "pyrrole": [
        ("pyrazole", "Similar pKa (~14), retains H-bond donor, more metabolic stability"),
        ("imidazole", "Adds basic N (pKa ~7), useful for H-bonding interactions"),
        ("thiophene", "Isosteric, no H-bond donor, more lipophilic, metabolically stable"),
        ("furan", "Isosteric, more electron-rich, may be less stable metabolically"),
        ("1,2,4-triazole", "Bioisosteric NH, used in drug design as pyrrole replacement"),
    ],
    "thiophene": [
        ("thiazole", "Adds N for H-bonding, retains similar size/shape"),
        ("pyrrole", "NH instead of S, H-bond donor capability"),
        ("furan", "O instead of S, more polar but less metabolically stable"),
        ("benzene", "Remove heteroatom, increase metabolic stability"),
        ("1,3,4-thiadiazole", "Bioisosteric, improved metabolic stability"),
    ],
    "furan": [
        ("thiophene", "S replacement improves metabolic stability (resists ring opening)"),
        ("oxazole", "Adds N, retains similar shape, improves stability"),
        ("isoxazole", "More metabolically stable than furan"),
        ("pyrrole", "NH instead of O, H-bond donor"),
        ("cyclopentadiene", "Non-aromatic isostere, different electronics"),
    ],
    "imidazole": [
        ("pyrazole", "Similar pKa, different orientation of N atoms"),
        ("triazole", "Higher pKa, used as imidazole bioisostere in drugs"),
        ("pyridine", "Replace H-bond donor N with acceptor-only N"),
        ("tetrazole", "Similar acidity, bioisosteric for carboxylic acid"),
        ("benzimidazole", "Fused version, increased lipophilicity"),
    ],
    "pyrazole": [
        ("imidazole", "Similar size, different pKa profile"),
        ("1,2,4-triazole", "Similar H-bond pattern, more metabolic stability"),
        ("isoxazole", "Replace N with O, different H-bonding"),
        ("pyrrole", "Remove one N, less polar"),
        ("tetrazole", "More electron-deficient, similar size"),
    ],
    "indole": [
        ("benzimidazole", "Adds basic N, retains fused ring system"),
        ("indazole", "N-N fusion, similar shape, different H-bonding"),
        ("benzofuran", "Replace NH with O, no H-bond donor"),
        ("benzothiophene", "Replace NH with S, more lipophilic"),
        ("7-azaindole", "N replaces C in benzene ring, increases polarity"),
    ],
    "quinoline": [
        ("isoquinoline", "Isomeric, different substitution pattern"),
        ("naphthyridine", "Additional N, modulates basicity/solubility"),
        ("quinoxaline", "Two N in fused ring, electron-deficient"),
        ("acridine", "Three fused rings, increased lipophilicity"),
    ],
    "isoquinoline": [
        ("quinoline", "Isomeric, different reactivity pattern"),
        ("phthalazine", "Two N, modulates pKa and electronics"),
        ("cinnoline", "Diazine fusion, different electronics"),
        ("benzimidazole", "5-membered N ring fusion"),
        ("quinazoline", "Pyrimidine fused ring"),
    ],
    "tetrazole": [
        ("carboxylic acid", "Classic bioisostere (similar pKa ~4-5), different H-bonding"),
        ("1,2,3-triazole", "Less acidic, similar ring size"),
        ("hydroxamic acid", "Similar acidity, strong metal chelation"),
        ("oxadiazole", "Less acidic, metabolically stable"),
    ],
    "oxazole": [
        ("isoxazole", "Different N/O arrangement, similar size"),
        ("thiazole", "S for O, more metabolically stable"),
        ("oxadiazole", "Additional N, electron-deficient"),
        ("imidazole", "Replace O with NH, different H-bonding"),
        ("pyrazole", "Two N, no O, similar ring size"),
    ],
    "thiazole": [
        ("oxazole", "O for S, more polar"),
        ("imidazole", "NH for S, H-bond donor"),
        ("1,3,4-thiadiazole", "Additional N, more electron-deficient"),
        ("pyridine", "6-membered isostere"),
    ],
}


def bioisostere_suggest(heterocycle_name: str) -> list:
    """Suggest bioisosteric replacements for a heterocycle.

    Parameters
    ----------
    heterocycle_name : str
        Heterocycle name (case-insensitive).

    Returns
    -------
    list of dict with keys: replacement (str), rationale (str).
    """
    key = heterocycle_name.strip().lower()
    key = _ALIASES.get(key, key)
    if key in _BIOISOSTERE_MAP:
        return [{"replacement": r, "rationale": rat}
                for r, rat in _BIOISOSTERE_MAP[key]]
    # Fallback: suggest based on ring size and heteroatoms
    try:
        entry = heterocycle_info(heterocycle_name)
    except KeyError:
        return [{"note": f"Unknown heterocycle: {heterocycle_name}"}]
    suggestions = []
    rs = entry["ring_size"]
    het = entry["heteroatoms"]
    if isinstance(rs, int) and rs == 5:
        suggestions.append({"replacement": "pyrrole", "rationale": "5-membered, single N"})
        suggestions.append({"replacement": "thiophene", "rationale": "5-membered, single S"})
        suggestions.append({"replacement": "furan", "rationale": "5-membered, single O"})
        if len(het) >= 2:
            suggestions.append({"replacement": "imidazole", "rationale": "5-membered, two N"})
            suggestions.append({"replacement": "thiazole", "rationale": "5-membered, N+S"})
    elif isinstance(rs, int) and rs == 6:
        suggestions.append({"replacement": "pyridine", "rationale": "6-membered, single N"})
        if len(het) >= 2:
            suggestions.append({"replacement": "pyrimidine", "rationale": "6-membered, two N"})
            suggestions.append({"replacement": "pyrazine", "rationale": "6-membered, para N,N"})
    elif isinstance(rs, str) and "5+6" in rs:
        suggestions.append({"replacement": "indole", "rationale": "fused 5+6, single N"})
        suggestions.append({"replacement": "benzimidazole", "rationale": "fused 5+6, two N"})
    elif isinstance(rs, str) and "6+6" in rs:
        suggestions.append({"replacement": "quinoline", "rationale": "fused 6+6, single N"})
        suggestions.append({"replacement": "quinoxaline", "rationale": "fused 6+6, two N"})
    if not suggestions:
        suggestions.append({"note": "No specific bioisosteres available. "
                                     "Consider ring size/heteroatom matching."})
    return suggestions


# ═══════════════════════════════════════════════════════════════════════════
# 6. snar_predictor
# ═══════════════════════════════════════════════════════════════════════════
_SNAR_ACTIVATION = {
    "poor": "Not feasible. Ring is too electron-rich or lacks activating N.",
    "moderate": "Possible with strong electron-withdrawing groups or forcing conditions.",
    "good": "Feasible. N heteroatom(s) activate the ring toward addition-elimination.",
    "excellent": "Highly feasible. Multiple N atoms strongly activate the ring.",
}

_NUCLEOPHILE_STRENGTH = {
    "amine": "strong", "ammonia": "strong", "alkoxide": "strong",
    "thiolate": "strong", "hydride": "moderate", "cyanide": "strong",
    "azide": "strong", "enolate": "strong", "water": "weak",
    "alcohol": "weak", "halide": "moderate", "methoxide": "strong",
}


def snar_predictor(heterocycle_name: str, leaving_group: str,
                   nucleophile: str) -> dict:
    """Predict nucleophilic aromatic substitution feasibility and position.

    Parameters
    ----------
    heterocycle_name : str
        Substrate heterocycle (case-insensitive).
    leaving_group : str
        Leaving group description, e.g. 'Cl at position 2', 'F at position 4'.
    nucleophile : str
        Nucleophile type, e.g. 'amine', 'thiolate', 'azide', 'methoxide'.

    Returns
    -------
    dict with keys: feasible, confidence, snar_reactivity, activation_rationale,
        nucleophile, nucleophile_strength, leaving_group, leaving_group_quality,
        predicted_position, conditions_recommendation, notes.
    """
    entry = heterocycle_info(heterocycle_name)
    snar_level = entry.get("snar", "poor")

    # Parse leaving group position
    lg_pos = None
    m = re.search(r'(\d+)', leaving_group)
    if m:
        lg_pos = int(m.group(1))

    # Nucleophile assessment
    nuc_key = nucleophile.strip().lower()
    nuc_strength = "unknown"
    for nk, ns in _NUCLEOPHILE_STRENGTH.items():
        if nk in nuc_key or nuc_key in nk:
            nuc_strength = ns
            break
    if nuc_strength == "unknown":
        nuc_strength = "moderate"

    # Feasibility logic
    levels = {"poor": 0, "moderate": 1, "good": 2, "excellent": 3}
    snar_score = levels.get(snar_level, 0)
    nuc_score = {"weak": 0, "moderate": 1, "strong": 2}.get(nuc_strength, 1)

    feasible = (snar_score + nuc_score) >= 3
    if snar_score == 0:
        feasible = False
    if snar_score >= 2 and nuc_score >= 1:
        feasible = True

    confidence = ("high" if (snar_score >= 2 and nuc_score >= 2) else
                  "medium" if feasible else "low")

    predicted_pos = lg_pos if lg_pos is not None else "same as leaving group"

    if snar_score >= 2:
        conditions = "Mild: rt-100 C, polar aprotic solvent (DMF, DMSO)"
    elif snar_score >= 1:
        conditions = "Moderate: 80-150 C, polar solvent, possibly Cu catalysis"
    else:
        conditions = "Not recommended; would require extreme conditions or is infeasible"

    # Leaving group quality
    lg_lower = leaving_group.strip().lower()
    if "f" in lg_lower and "fl" not in lg_lower:
        lg_quality = "excellent (F is best LG for SnAr)"
    elif "cl" in lg_lower:
        lg_quality = "good"
    elif "br" in lg_lower:
        lg_quality = "moderate"
    elif "i" in lg_lower:
        lg_quality = "poor (I is poor LG for SnAr despite good for SN2)"
    elif "ot" in lg_lower or "triflate" in lg_lower:
        lg_quality = "excellent"
    else:
        lg_quality = "unknown"

    notes = _snar_notes(entry, snar_score, nuc_score, lg_pos)

    return {
        "feasible": feasible,
        "confidence": confidence,
        "snar_reactivity": snar_level,
        "activation_rationale": _SNAR_ACTIVATION.get(snar_level, "Unknown"),
        "nucleophile": nucleophile,
        "nucleophile_strength": nuc_strength,
        "leaving_group": leaving_group,
        "leaving_group_quality": lg_quality,
        "predicted_position": predicted_pos,
        "conditions_recommendation": conditions,
        "notes": notes,
    }


def _snar_notes(entry, snar_score, nuc_score, lg_pos):
    """Generate contextual notes for SnAr prediction."""
    notes = []
    if not entry["aromatic"]:
        notes.append("Substrate is not aromatic; standard SnAr does not apply.")
    if snar_score >= 3:
        notes.append("Multiple N atoms strongly activate the ring. SnAr proceeds readily.")
    if lg_pos is not None:
        het = entry["heteroatoms"]
        if len(het) >= 2:
            notes.append("Ensure leaving group is ortho or para to ring N for activation.")
    if nuc_score >= 2:
        notes.append("Strong nucleophile favorable; may proceed at lower temperature.")
    return " ".join(notes) if notes else "Standard SnAr considerations apply."


# ═══════════════════════════════════════════════════════════════════════════
# CLI convenience
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import json
    args = sys.argv[1:]
    if not args:
        print("Usage: python heterocyclic_tools.py <function> [args...]")
        print("Functions: info, check, synth, eas, bio, snar, list")
        print("Example: python heterocyclic_tools.py info pyridine")
        sys.exit(0)
    cmd = args[0].lower()
    try:
        if cmd == "info" and len(args) >= 2:
            print(json.dumps(heterocycle_info(args[1]), indent=2, default=str))
        elif cmd == "check" and len(args) >= 2:
            print(json.dumps(aromaticity_check(args[1]), indent=2))
        elif cmd == "synth" and len(args) >= 2:
            pref = args[2] if len(args) > 2 else None
            print(json.dumps(synthesis_recommend(args[1], pref), indent=2))
        elif cmd == "eas" and len(args) >= 2:
            print(json.dumps(electrophilic_substitution_positions(args[1]), indent=2))
        elif cmd == "bio" and len(args) >= 2:
            print(json.dumps(bioisostere_suggest(args[1]), indent=2))
        elif cmd == "snar" and len(args) >= 4:
            print(json.dumps(snar_predictor(args[1], args[2], args[3]), indent=2))
        elif cmd == "list":
            print(json.dumps(list_heterocycles(), indent=2))
        else:
            print(f"Unknown command or missing args: {args}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
