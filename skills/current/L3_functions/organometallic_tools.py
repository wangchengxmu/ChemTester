"""Organometallic chemistry calculation and analysis tools.

Self-contained module with reference data. RDKit used optionally for SMILES-based predictions.
"""

from __future__ import annotations

import re
from typing import Any

try:
    from rdkit import Chem as _Chem
    _RDKIT = True
except ImportError:
    _RDKIT = False

# ---------------------------------------------------------------------------
# 1. Electron counting
# ---------------------------------------------------------------------------

# Ligand electron contributions: (ionic e⁻, covalent e⁻)
# Ionic: ligand donates as if it were an X-type (anionic) or L-type (neutral)
# Covalent: 2e per lone-pair donor (L), 1e per X-type anionic ligand
_LIGAND_ELECTRONS: dict[str, tuple[int, int]] = {
    # L-type (neutral 2e donors)
    "CO":     (2, 2),
    "PPh3":   (2, 2),
    "P(p-tol)3": (2, 2),
    "PPh2Me": (2, 2),
    "PMe3":   (2, 2),
    "PCy3":   (2, 2),
    "P(OPh)3": (2, 2),
    "NH3":    (2, 2),
    "N2":     (2, 2),
    "H2O":    (2, 2),
    "THF":    (2, 2),
    "pyridine": (2, 2),
    "amine":  (2, 2),
    "ether":  (2, 2),
    "py":     (2, 2),
    "tBuNC":  (2, 2),
    "MeCN":   (2, 2),
    "C2H4":   (2, 2),
    "alkene": (2, 2),
    "C2H2":   (2, 2),
    "alkyne": (2, 2),
    # X-type (anionic 2e donors, covalent: 1e per X)
    "Cl":     (2, 1),
    "Br":     (2, 1),
    "I":      (2, 1),
    "F":      (2, 1),
    "H":      (2, 1),
    "OH":     (2, 1),
    "OR":     (2, 1),
    "OMe":    (2, 1),
    "OEt":    (2, 1),
    "OAc":    (2, 1),
    "SR":     (2, 1),
    "SMe":    (2, 1),
    "NR2":    (2, 1),
    "NMe2":   (2, 1),
    "CN":     (2, 1),
    "acetylacetonate": (2, 1),  # bidentate simplified
    "acac":   (2, 1),
    # LX-type (ylide-like, simplified as 2e)
    "PPh3_Carbene": (2, 2),
    # Special polydentate / pi-systems
    "Cp":     (6, 5),   # η⁵-C₅H₅⁻
    "Cp*":    (6, 5),   # η⁵-C₅Me₅⁻
    "benzene": (6, 6),  # η⁶-C₆H₆
    "C6H6":   (6, 6),
    "allyl":  (4, 3),   # η³-C₃H₅
    "dienyl": (6, 5),
    "COD":    (4, 2),   # 1,5-cyclooctadiene (2 × alkene)
    "NHC":    (2, 2),   # N-heterocyclic carbene
}

# Metal valence electron counts (group number for neutral atom)
_METAL_VE: dict[str, int] = {
    "Sc": 3, "Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10,
    "Cu": 11, "Zn": 12,
    "Y": 3, "Zr": 4, "Nb": 5, "Mo": 6, "Tc": 7, "Ru": 8, "Rh": 9, "Pd": 10,
    "Ag": 11, "Cd": 12,
    "Hf": 4, "Ta": 5, "W": 6, "Re": 7, "Os": 8, "Ir": 9, "Pt": 10, "Au": 11,
    "La": 3, "Ce": 3, "Pr": 3, "Nd": 3, "Sm": 3, "Eu": 3, "Gd": 3,
    "Lu": 3,
}


def _lookup_ligand(lig: str) -> tuple[int, int]:
    """Resolve ligand string to (ionic, covalent) electron contribution."""
    # direct match
    if lig in _LIGAND_ELECTRONS:
        return _LIGAND_ELECTRONS[lig]
    # case-insensitive
    low = lig.lower()
    for k, v in _LIGAND_ELECTRONS.items():
        if k.lower() == low:
            return v
    # synonyms
    aliases = {"triphenylphosphine": "PPh3", "trimethylphosphine": "PMe3",
               "tricyclohexylphosphine": "PCy3", "cyclopentadienyl": "Cp",
               "pentamethylcyclopentadienyl": "Cp*", "carbonyl": "CO",
               "chloride": "Cl", "bromide": "Br", "iodide": "I",
               "hydride": "H", "phosphine": "PPh3",
               "tri-p-tolylphosphine": "P(p-tol)3"}
    if lig in aliases:
        return _LIGAND_ELECTRONS[aliases[lig]]
    raise ValueError(f"Unknown ligand: {lig!r}")


def electron_count(
    metal: str,
    oxidation_state: int,
    ligands: list[str],
) -> dict[str, Any]:
    """Calculate total electron count using ionic and covalent (neutral) methods.

    Args:
        metal: Element symbol (e.g. 'Fe', 'Rh').
        oxidation_state: Oxidation state of the metal center (integer).
        ligands: List of ligand identifiers.

    Returns:
        Dict with keys: ionic_count, covalent_count, obeys_18e,
        metal_valence_electrons, ligand_details.
    """
    m = metal.strip().capitalize()
    if m not in _METAL_VE:
        raise ValueError(f"Metal {metal!r} not in database.")
    metal_ve = _METAL_VE[m]

    lig_details = []
    ionic_total = 0
    covalent_total = 0
    for lig in ligands:
        i_e, c_e = _lookup_ligand(lig)
        lig_details.append({"ligand": lig, "ionic": i_e, "covalent": c_e})
        ionic_total += i_e
        covalent_total += c_e

    ionic_count = metal_ve - oxidation_state + ionic_total
    covalent_count = metal_ve + covalent_total

    return {
        "ionic_count": ionic_count,
        "covalent_count": covalent_count,
        "obeys_18e": ionic_count == 18 or covalent_count == 18,
        "metal_valence_electrons": metal_ve,
        "ligand_details": lig_details,
        "method_match": ionic_count == covalent_count,
    }


# ---------------------------------------------------------------------------
# 2. Cross-coupling recommendations
# ---------------------------------------------------------------------------

_CROSS_COUPLING_DB: list[dict[str, Any]] = [
    # Suzuki-Miyaura
    {"halide": "aryl-Br", "partner": "boronic_acid", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "K2CO3", "solvent": "dioxane/H2O",
     "temp_C": 80, "notes": "General purpose Suzuki."},
    {"halide": "aryl-Br", "partner": "boronic_acid", "catalyst": "Pd(dppf)Cl2",
     "ligand": "—", "base": "Cs2CO3", "solvent": "DMF",
     "temp_C": 80, "notes": "Robust for sensitive substrates."},
    {"halide": "aryl-I", "partner": "boronic_acid", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "K2CO3", "solvent": "THF/H2O",
     "temp_C": 50, "notes": "Aryl-I most reactive; milder conditions."},
    {"halide": "aryl-Cl", "partner": "boronic_acid", "catalyst": "Pd(OAc)2",
     "ligand": "SPhos", "base": "K3PO4", "solvent": "toluene",
     "temp_C": 100, "notes": "Aryl-Cl needs bulky electron-rich phosphine."},
    {"halide": "vinyl-Br", "partner": "boronic_acid", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "K2CO3", "solvent": "THF/H2O",
     "temp_C": 60, "notes": "Stereoretention typical."},
    {"halide": "vinyl-I", "partner": "boronic_acid", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "K2CO3", "solvent": "THF/H2O",
     "temp_C": 40, "notes": "Very mild; stereoretention."},
    # Stille
    {"halide": "aryl-Br", "partner": "stannane", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "none", "solvent": "toluene",
     "temp_C": 100, "notes": "Stille coupling; CuI additive can help."},
    {"halide": "aryl-I", "partner": "stannane", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "none", "solvent": "toluene",
     "temp_C": 80, "notes": "Stille; tolerant of many FGs."},
    # Negishi
    {"halide": "aryl-Br", "partner": "zinc", "catalyst": "Pd(PPh3)4",
     "ligand": "—", "base": "none", "solvent": "THF",
     "temp_C": 25, "notes": "Negishi; mild, functional-group tolerant."},
    # Sonogashira
    {"halide": "aryl-Br", "partner": "alkyne", "catalyst": "Pd(PPh3)2Cl2",
     "ligand": "—", "base": "Et3N / piperidine", "solvent": "THF",
     "temp_C": 50, "notes": "Sonogashira; CuI co-catalyst. Avoid with nitro groups."},
    {"halide": "aryl-I", "partner": "alkyne", "catalyst": "Pd(PPh3)2Cl2",
     "ligand": "—", "base": "Et3N", "solvent": "THF",
     "temp_C": 25, "notes": "Sonogashira with aryl-I; room temp possible."},
    {"halide": "aryl-Cl", "partner": "alkyne", "catalyst": "Pd(PPh3)2Cl2",
     "ligand": "XPhos", "base": "Et3N", "solvent": "dioxane",
     "temp_C": 100, "notes": "Aryl-Cl Sonogashira needs Buchwald ligand."},
    # Buchwald-Hartwig amination
    {"halide": "aryl-Br", "partner": "amine", "catalyst": "Pd2(dba)3",
     "ligand": "BrettPhos", "base": "NaOtBu", "solvent": "toluene",
     "temp_C": 100, "notes": "Buchwald-Hartwig amination; Ar-NH2 or Ar-NR2."},
    {"halide": "aryl-Br", "partner": "amine", "catalyst": "Pd2(dba)3",
     "ligand": "XPhos", "base": "Cs2CO3", "solvent": "dioxane",
     "temp_C": 100, "notes": "Milder base; works for primary amines."},
    {"halide": "aryl-Cl", "partner": "amine", "catalyst": "Pd2(dba)3",
     "ligand": "BrettPhos", "base": "NaOtBu", "solvent": "toluene",
     "temp_C": 110, "notes": "Aryl-Cl amination: needs BrettPhos or RuPhos."},
    {"halide": "aryl-I", "partner": "amine", "catalyst": "Pd2(dba)3",
     "ligand": "BINAP", "base": "NaOtBu", "solvent": "toluene",
     "temp_C": 80, "notes": "Aryl-I amination, classic conditions."},
]


def cross_coupling_recommend(
    halide_type: str,
    coupling_partner: str,
    functional_groups_sensitive: list[str] | None = None,
) -> dict[str, Any]:
    """Recommend cross-coupling conditions.

    Args:
        halide_type: e.g. 'aryl-Br', 'aryl-Cl', 'vinyl-I'.
        coupling_partner: e.g. 'boronic_acid', 'stannane', 'zinc', 'alkyne', 'amine'.
        functional_groups_sensitive: List of sensitive functional groups.

    Returns:
        Dict with catalyst, ligand, base, solvent, temperature, notes.
    """
    ht = halide_type.strip().lower()
    cp = coupling_partner.strip().lower().replace(" ", "_")
    fgs = set(g.lower() for g in (functional_groups_sensitive or []))

    best = None
    best_score = -1
    for entry in _CROSS_COUPLING_DB:
        if entry["halide"].lower() != ht or entry["partner"] != cp:
            continue
        score = 0
        notes = entry.get("notes", "").lower()
        # prefer milder (lower temp)
        score += 100 - entry["temp_C"]
        # penalize if notes mention incompatibility with sensitive FGs
        if "nitro" in fgs and "nitro" in notes:
            score -= 50
        if "aldehyde" in fgs and "aldehyde" not in notes:
            score += 5
        if "ester" in fgs:
            score += 5  # generally ok
        if score > best_score:
            best_score = score
            best = entry

    if best is None:
        return {
            "catalyst": "Pd(PPh3)4",
            "ligand": "—",
            "base": "K2CO3",
            "solvent": "dioxane/H2O",
            "temp_C": 80,
            "notes": f"No specific entry for {halide_type} + {coupling_partner}. "
                     f"General conditions shown. Adjust based on substrate reactivity.",
            "confidence": "low",
        }

    result = {k: best[k] for k in ("catalyst", "ligand", "base", "solvent", "temp_C", "notes")}
    result["confidence"] = "high"
    if fgs:
        warnings = []
        if "nitro" in fgs and "amine" in cp:
            warnings.append("Nitro groups incompatible with amination conditions.")
        if "aldehyde" in fgs:
            warnings.append("Aldehyde may be sensitive to strong bases/transmetalation.")
        if "boronic_acid" in cp and "ketone" in fgs:
            warnings.append("Ketone may undergo 1,2-addition with boronic acid.")
        result["fg_warnings"] = warnings
    return result


# ---------------------------------------------------------------------------
# 3. Oxidation state analysis
# ---------------------------------------------------------------------------

# Common ligand charges (overall formal charge contributed)
_LIGAND_CHARGE: dict[str, int] = {
    "CO": 0, "PPh3": 0, "PR3": 0, "PCy3": 0, "PMe3": 0,
    "NH3": 0, "py": 0, "pyridine": 0, "H2O": 0, "THF": 0,
    "NHC": 0, "MeCN": 0, "alkene": 0, "alkyne": 0, "C2H4": 0, "C2H2": 0,
    "N2": 0,
    "Cl": -1, "Br": -1, "I": -1, "F": -1,
    "H": -1, "hydride": -1,
    "OH": -1, "OMe": -1, "OEt": -1, "OR": -1, "OAc": -1,
    "SR": -1, "SMe": -1, "CN": -1,
    "Cp": -1, "Cp*": -1,
    "allyl": -1,
    "benzene": 0, "C6H6": 0,
    "acac": -1, "acetylacetonate": -1,
}


def _parse_formula(formula: str) -> dict[str, int]:
    """Simple chemical formula parser → {element: count}."""
    pattern = r"([A-Z][a-z]?)(\d*)"
    result: dict[str, int] = {}
    for elem, num in re.findall(pattern, formula):
        result[elem] = result.get(elem, 0) + (int(num) if num else 1)
    return result


def oxidation_state_analyze(
    formula: str,
    ligands_context: list[str] | None = None,
) -> dict[str, Any]:
    """Determine likely oxidation states for a metal complex.

    Args:
        formula: Molecular formula (e.g. 'Fe(CO)5', 'RuCl2(PPh3)3').
        ligands_context: Optional ligand identifiers to help parsing.

    Returns:
        Dict with possible_oxidation_states (ranked), rationale.
    """
    # Try to extract metal from formula
    metals_in_formula = [m for m in _METAL_VE if m in formula]
    if not metals_in_formula:
        return {"possible_oxidation_states": [],
                "rationale": "No recognized metal found in formula."}

    # Pick the first (or most common) metal
    metal = max(metals_in_formula, key=lambda m: formula.index(m))

    # Sum ligand charges
    ligands = ligands_context or []
    total_ligand_charge = 0
    for lig in ligands:
        if lig in _LIGAND_CHARGE:
            total_ligand_charge += _LIGAND_CHARGE[lig]

    # Try to extract ligand info from formula itself
    # Count halides
    for hal, ch in [("Cl", -1), ("Br", -1), ("I", -1), ("F", -1)]:
        total_ligand_charge += formula.count(hal) * ch
    # Count CO
    co_count = len(re.findall(r'\(CO\)', formula)) + formula.count("CO") - len(re.findall(r'C[ol]', formula)) // 2
    # Rough: just count (CO) groups
    co_groups = formula.count("(CO)")
    # Cp
    cp_groups = len(re.findall(r'\(Cp\*?\)', formula))

    # If ligands_context was provided, use it; otherwise rough estimate
    if ligands:
        pass  # already summed
    else:
        total_ligand_charge = 0
        for hal, ch in [("Cl", -1), ("Br", -1), ("I", -1), ("F", -1)]:
            total_ligand_charge += formula.count(hal) * ch

    # Common oxidation states by metal
    common_os = {
        "Fe": [2, 3, 0], "Ru": [2, 3, 0], "Os": [2, 3, 4],
        "Co": [2, 3, 1, 0], "Rh": [1, 3], "Ir": [1, 3],
        "Ni": [0, 2], "Pd": [0, 2], "Pt": [0, 2],
        "Cu": [1, 2], "Ag": [1], "Au": [1, 3],
        "Cr": [0, 2, 3, 6], "Mo": [0, 2, 4, 6], "W": [0, 2, 4, 6],
        "Mn": [1, 2, 7], "Re": [1, 3, 5, 7],
        "Ti": [4, 3], "Zr": [4], "Hf": [4],
        "V": [2, 3, 4, 5], "Nb": [5], "Ta": [5],
        "Zn": [2], "Cd": [2], "Sc": [3], "Y": [3],
    }

    possible = common_os.get(metal, list(range(-2, 8)))

    # If total ligand charge is known, constrain: OS + total_ligand_charge = overall_complex_charge
    # For neutral complexes: OS = -total_ligand_charge
    if ligands and total_ligand_charge != 0:
        required_os = -total_ligand_charge
        # Rank: closest to common OS first
        ranked = sorted(possible, key=lambda x: (abs(x - required_os), abs(x)))
    else:
        ranked = possible

    return {
        "metal": metal,
        "possible_oxidation_states": ranked[:5],
        "rationale": f"Ligand charge balance ({total_ligand_charge}) and common OS for {metal}. "
                     f"Top states listed by likelihood.",
    }


# ---------------------------------------------------------------------------
# 4. Tolman cone angles
# ---------------------------------------------------------------------------

_TOLMAN_CONE_ANGLES: dict[str, int] = {
    "PPh3": 145,
    "P(p-tol)3": 145,
    "PPh2Me": 136,
    "PPhMe2": 127,
    "PMe3": 118,
    "PMe2Ph": 122,
    "PCy3": 170,
    "P(t-Bu)3": 182,
    "P(i-Pr)3": 160,
    "P(o-tol)3": 194,
    "P(mesityl)3": 212,
    "P(OPh)3": 128,
    "P(OEt)3": 109,
    "P(OMe)3": 107,
    "P(O-i-Pr)3": 130,
    "P(p-F-C6H4)3": 145,
    "P(CF3)3": 184,
    "P(NMe2)3": 132,
    "P(NC4H8)3": 157,  # pyrrolidinyl
    "PH3": 87,
    "PF3": 104,
    "dppe": 125,  # chelating, avg per P
    "dppp": 130,
    "dppb": 132,
    "dppf": 145,
    "XPhos": 170,
    "SPhos": 168,
    "BrettPhos": 175,
    "RuPhos": 162,
    "JohnPhos": 155,
    "DavePhos": 160,
    "tBuBrettPhos": 195,
}


def ligand_cone_angle(ligand: str) -> dict[str, Any]:
    """Return Tolman cone angle for common phosphine ligands.

    Args:
        ligand: Ligand name or abbreviation.

    Returns:
        Dict with cone_angle (degrees) and ligand classification (small/medium/large/xlarge).
    """
    lig = ligand.strip()
    if lig in _TOLMAN_CONE_ANGLES:
        angle = _TOLMAN_CONE_ANGLES[lig]
    else:
        # try case-insensitive
        for k, v in _TOLMAN_CONE_ANGLES.items():
            if k.lower() == lig.lower():
                angle = v
                break
        else:
            return {"ligand": lig, "cone_angle": None,
                    "classification": "unknown",
                    "note": "Ligand not in database."}

    if angle < 120:
        cls = "small"
    elif angle < 155:
        cls = "medium"
    elif angle < 180:
        cls = "large"
    else:
        cls = "xlarge"
    return {"ligand": lig, "cone_angle": angle, "classification": cls}


# ---------------------------------------------------------------------------
# 5. Transmetalation compatibility
# ---------------------------------------------------------------------------

_TRANSMETALATION_DB: dict[tuple[str, str], tuple[bool, str]] = {
    # (metal1, metal2) — typically metal1 = catalyst (Pd, Ni), metal2 = organometallic partner
    ("Pd", "B"):  (True,  "Pd–B transmetalation (Suzuki) is well-established."),
    ("Pd", "Sn"): (True,  "Pd–Sn transmetalation (Stille) is efficient."),
    ("Pd", "Zn"): (True,  "Pd–Zn transmetalation (Negishi) is fast."),
    ("Pd", "Si"): (True,  "Pd–Si transmetalation (Hiyama) requires fluoride activator."),
    ("Pd", "Mg"): (True,  "Pd–Mg transmetalation (Kumada) is facile; base-sensitive."),
    ("Pd", "Al"): (False, "Pd–Al transmetalation not commonly used."),
    ("Pd", "Cu"): (True,  "Pd–Cu transmetalation possible (Sonogashira)."),
    ("Ni", "B"):  (True,  "Ni–B transmetalation works but less explored than Pd."),
    ("Ni", "Zn"): (True,  "Ni–Zn transmetalation (Negishi) well-established."),
    ("Ni", "Mg"): (True,  "Ni–Mg transmetalation (Kumada) is common."),
    ("Ni", "Sn"): (True,  "Ni–Sn transmetalation viable."),
    ("Ni", "Al"): (False, "Not a standard transmetalation pair."),
    ("Ni", "Si"): (True,  "Ni–Si (Hiyama) works with activator."),
    ("Cu", "B"):  (False, "Cu–B direct transmetalation not standard; use Chan-Lam instead."),
    ("Cu", "Sn"): (False, "Not a common pair."),
    ("Cu", "Zn"): (True,  "Cu–Zn transmetalation used in some couplings."),
    ("Cu", "Mg"): (True,  "Cu–Mg transmetalation (Normant-type reagents)."),
    ("Rh", "B"):  (True,  "Rh–B transmetalation used in Rh-catalyzed additions."),
    ("Rh", "Sn"): (True,  "Rh–Stille couplings exist but are niche."),
    ("Ir", "B"):  (True,  "Ir–B transmetalation in borylation reactions."),
    ("Fe", "Mg"): (True,  "Fe–Mg (Kumada) via Fe-catalysis; iron cross-coupling."),
    ("Fe", "Zn"): (True,  "Fe–Zn (Negishi-type) possible."),
    ("Fe", "B"):  (False, "Fe–B transmetalation not well-developed."),
    ("Co", "Zn"): (True,  "Co–Zn transmetalation explored."),
}


def transmetalation_compatibility(metal1: str, metal2: str) -> dict[str, Any]:
    """Check if transmetalation between two metal centers is favorable.

    Args:
        metal1: First metal symbol (e.g. 'Pd' for Pd catalyst).
        metal2: Second metal symbol (e.g. 'B' for boron in Suzuki).

    Returns:
        Dict with compatible (bool) and rationale (str).
    """
    m1 = metal1.strip().capitalize()
    m2 = metal2.strip().capitalize()
    key = (m1, m2)
    if key in _TRANSMETALATION_DB:
        comp, rationale = _TRANSMETALATION_DB[key]
    elif (m2, m1) in _TRANSMETALATION_DB:
        comp, rationale = _TRANSMETALATION_DB[(m2, m1)]
        rationale += f" (noted for {m2}→{m1}; reverse may differ.)"
    else:
        comp, rationale = False, f"No data for {m1}–{m2} pair."
    return {"compatible": comp, "rationale": rationale}


# ---------------------------------------------------------------------------
# 6. Metathesis product prediction
# ---------------------------------------------------------------------------

def _simplify_smiles(smi: str) -> str:
    """Basic SMILES cleanup for RDKit or fallback."""
    if not smi:
        return smi
    return smi.strip()


def metathesis_product_predict(
    alkenes: list[str],
    catalyst_type: str,
) -> dict[str, Any]:
    """Predict RCM/CM products given input alkenes and catalyst.

    Args:
        alkenes: List of SMILES strings or descriptive names of alkenes.
        catalyst_type: 'Grubbs-1', 'Grubbs-2', 'Grubbs-3', 'Hoveyda-Grubbs-2'.

    Returns:
        Dict with product prediction, E/Z selectivity notes, catalyst features.
    """
    n = len(alkenes)
    cat = catalyst_type.strip().lower()

    catalyst_info = {
        "grubbs-1": {
            "name": "Grubbs 1st Generation (Cl2(PCy3)2Ru=CHPh)",
            "functional_group_tolerance": "Low—sensitive to alcohols, amines, acids.",
            "z_selectivity": "Low preference for E or Z; thermodynamic mix.",
            "stereocontrol": "E-favored (thermodynamic).",
        },
        "grubbs-2": {
            "name": "Grubens 2nd Generation (Cl2(PCy3)(IMes)Ru=CHPh)",
            "functional_group_tolerance": "High—tolerates alcohols, amides, esters, water.",
            "z_selectivity": "Moderate; can achieve high E with appropriate conditions.",
            "stereocontrol": "E-favored; Z-accessible with modifications.",
        },
        "grubbs-3": {
            "name": "Grubens 3rd Generation (nitrate-based fast-initiating)",
            "functional_group_tolerance": "Very high.",
            "z_selectivity": "High Z-selectivity with appropriate ligands.",
            "stereocontrol": "Can be tuned toward Z or E.",
        },
        "hoveyda-grubbs-2": {
            "name": "Hoveyda–Grubbs 2nd Generation (chelating benzylidene)",
            "functional_group_tolerance": "High—thermally stable, air-stable.",
            "z_selectivity": "E-favored; Z-modified versions available.",
            "stereocontrol": "E-favored in standard RCM.",
        },
    }

    info = catalyst_info.get(cat, {
        "name": catalyst_type,
        "functional_group_tolerance": "Unknown catalyst type.",
        "z_selectivity": "Unknown.",
        "stereocontrol": "Unknown.",
    })

    # If RDKit available, try to do real chemistry
    rdkit_used = False
    products_smiles = []
    if _RDKIT and all(_looks_like_smiles(a) for a in alkenes):
        rdkit_used = True
        products_smiles = _rdkit_metathesis_predict(alkenes)

    # Text-based prediction
    if n == 1 and _is_diene(alkenes[0]):
        # Likely RCM (ring-closing metathesis)
        ring_size = _estimate_ring_size(alkenes[0])
        result_type = "RCM (Ring-Closing Metathesis)"
        prediction = f"RCM → {ring_size}-membered ring cyclic alkene" if ring_size else "RCM → cyclic alkene"
    elif n == 1:
        result_type = "RCM or CM (needs more than one alkene partner or diene substrate)"
        prediction = "Self-metathesis or oligomerization likely; provide a diene for RCM."
    elif n == 2:
        result_type = "CM (Cross-Metathesis)"
        prediction = f"CM → cross-product alkene + ethylene (if terminal alkenes)"
    else:
        result_type = "Complex metathesis"
        prediction = f"Multiple alkenes ({n}) — complex product mixture; consider stepwise approach."

    result = {
        "reaction_type": result_type,
        "prediction": prediction,
        "catalyst": info["name"],
        "stereochemistry": info["stereocontrol"],
        "functional_group_tolerance": info["functional_group_tolerance"],
        "input_alkenes": alkenes,
    }

    if rdkit_used and products_smiles:
        result["product_smiles"] = products_smiles
        result["method"] = "RDKit-based prediction"

    return result


def _looks_like_smiles(s: str) -> bool:
    """Heuristic check for SMILES strings."""
    return bool(s and any(c in s for c in "C=()[]#"))


def _is_diene(alkene: str) -> bool:
    """Check if a SMILES or description suggests a diene (two alkene units)."""
    if "=" not in alkene and "alkene" not in alkene.lower():
        return False
    return alkene.count("=") >= 2 or "diene" in alkene.lower()


def _estimate_ring_size(alkene: str) -> int | None:
    """Rough ring size estimation from SMILES for RCM."""
    if not _looks_like_smiles(alkene):
        return None
    # Count atoms between two C= groups
    parts = alkene.split("=")
    if len(parts) == 3:
        return len(parts[1]) + 2  # rough: atoms in bridge + 2 alkene carbons
    return None


def _rdkit_metathesis_predict(alkenes: list[str]) -> list[str]:
    """Very simplified RDKit-based product guess (conceptual)."""
    products = []
    if len(alkenes) == 2:
        # Cross-metathesis: swap the alkene fragments
        mols = [_Chem.MolFromSmiles(a) for a in alkenes]
        if all(mols):
            products.append("cross_metathesis_product (SMILES computation simplified)")
    return products


# ---------------------------------------------------------------------------
# Convenience
# ---------------------------------------------------------------------------

__all__ = [
    "electron_count",
    "cross_coupling_recommend",
    "oxidation_state_analyze",
    "ligand_cone_angle",
    "transmetalation_compatibility",
    "metathesis_product_predict",
]
