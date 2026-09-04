"""
L3 Tool: Stereoisomer Counter
Counts possible stereoisomers given a molecular structure description.
"""

import re
from typing import Optional


class StereoisomerCounter:
    def __init__(self):
        # Known molecules database: name_pattern -> {chiral_centers, meso, notes}
        self._known_molecules = self._build_known_molecules()
        # Common functional groups that induce chirality
        self._chiral_indicators = [
            "chiral center", "stereocenter", "stereogenic",
            "asymmetric carbon", "chirality"
        ]

    def _build_known_molecules(self) -> dict:
        return {
            # Alkanes/dihalides
            "2,3-dibromobutane": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "Internal plane of symmetry through C2-C3 bond center"},
            "2,3-dichlorobutane": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "Analogous to 2,3-dibromobutane"},
            "2,3-butanediol": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "Internal symmetry plane"},
            "tartaric acid": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "(2R,3S) is meso; (2R,3R) and (2S,3S) are optically active"},
            "meso-tartaric acid": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "The meso form specifically"},
            "2-chlorobutane": {"chiral_centers": 1, "ez_bonds": 0, "meso": 0, "notes": "One chiral center at C2"},
            "2-bromobutane": {"chiral_centers": 1, "ez_bonds": 0, "meso": 0, "notes": "One chiral center at C2"},
            "1,2-dibromo-1,2-dichloroethane": {"chiral_centers": 0, "ez_bonds": 1, "meso": 0, "notes": "E/Z isomerism only"},
            "cyclohexane-1,2-diol": {"chiral_centers": 2, "ez_bonds": 0, "meso": 0, "notes": "cis: meso not possible on ring; trans: 2 enantiomers"},
            "1,2-dimethylcyclohexane": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "cis-1,2 is meso; trans-1,2 is chiral (2 enantiomers)"},
            "glucose": {"chiral_centers": 4, "ez_bonds": 0, "meso": 0, "notes": "D-glucose and L-glucose; also anomers at C1"},
            "fructose": {"chiral_centers": 3, "ez_bonds": 0, "meso": 0, "notes": "Ketohexose"},
            "alanine": {"chiral_centers": 1, "ez_bonds": 0, "meso": 0, "notes": "One chiral center at α-carbon"},
            "2,3,4-trihydroxyglutaric acid": {"chiral_centers": 2, "ez_bonds": 0, "meso": 1, "notes": "Meso form exists"},
            "1,2-cyclohexanediol": {"chiral_centers": 2, "ez_bonds": 0, "meso": 0, "notes": "cis and trans each have distinct stereochemistry"},
            "cholesterol": {"chiral_centers": 8, "ez_bonds": 0, "meso": 0, "notes": "8 stereocenters in the steroid skeleton"},
            "2-butene": {"chiral_centers": 0, "ez_bonds": 1, "meso": 0, "notes": "cis- and trans-2-butene"},
            "1,2-dichloroethene": {"chiral_centers": 0, "ez_bonds": 1, "meso": 0, "notes": "cis (Z) and trans (E) isomers"},
            "2-pentene": {"chiral_centers": 0, "ez_bonds": 1, "meso": 0, "notes": "E/Z isomers"},
            "3-methylpent-2-ene": {"chiral_centers": 0, "ez_bonds": 1, "meso": 0, "notes": "E/Z isomerism at C2=C3"},
            "1-bromo-1-chloroethene": {"chiral_centers": 0, "ez_bonds": 1, "meso": 0, "notes": "E/Z isomers"},
            "allene": {"chiral_centers": 0, "ez_bonds": 0, "meso": 0, "notes": "Axial chirality: 2 enantiomers if substituents differ on each terminus", "axial_chirality": 1},
            "1,3-dichloroallene": {"chiral_centers": 0, "ez_bonds": 0, "meso": 0, "notes": "Axial chirality: P and M enantiomers", "axial_chirality": 1},
            "biphenyl": {"chiral_centers": 0, "ez_bonds": 0, "meso": 0, "notes": "Atropisomerism if ortho substituents large enough", "axial_chirality": 1},
            "binaphthol": {"chiral_centers": 0, "ez_bonds": 0, "meso": 0, "notes": "Atropisomers: (R)- and (S)-BINOL", "axial_chirality": 1},
        }

    def _parse_description(self, desc: str) -> dict:
        """Parse a text description to extract chirality info."""
        d = desc.lower().strip()
        result = {"chiral_centers": 0, "ez_bonds": 0, "axial_chirality": 0, "meso_possible": False}

        # Check known molecules first (fuzzy match)
        for name, info in self._known_molecules.items():
            if name in d or name.replace("-", "") in d.replace("-", ""):
                result["chiral_centers"] = info["chiral_centers"]
                result["ez_bonds"] = info["ez_bonds"]
                result["meso_possible"] = info["meso"] > 0
                result["axial_chirality"] = info.get("axial_chirality", 0)
                result["matched_name"] = name
                result["notes"] = info.get("notes", "")
                return result

        # Parse explicit chiral center count
        cc_match = re.search(r'(\d+)\s*(?:chiral\s*center|stereocenter|stereogenic\s*center)s?', d)
        if cc_match:
            result["chiral_centers"] = int(cc_match.group(1))

        # Parse E/Z bond count
        ez_match = re.search(r'(\d+)\s*(?:e/z|cis/trans|double\s*bond)s?\s*(?:isomer|stereogenic)?', d)
        if not ez_match:
            ez_match = re.search(r'(\d+)\s*(?:stereogenic\s*double\s*bond)s?', d)
        if ez_match:
            result["ez_bonds"] = int(ez_match.group(1))

        # Detect meso mentions
        if any(kw in d for kw in ["meso", "internal symmetry", "internal plane", "symmetry plane"]):
            result["meso_possible"] = True

        # Detect E/Z mentions
        if "e/z" in d or "cis/trans" in d or "geometric isomer" in d:
            if result["ez_bonds"] == 0:
                # Try to count from pattern like "has E/Z isomerism"
                result["ez_bonds"] = 1

        # Detect alkene descriptions that imply E/Z
        if any(kw in d for kw in ["alkene", "c=c", "double bond"]) and "ez" not in d:
            # Check if the alkene is terminal (no E/Z) or internal
            if re.search(r'\d+-alkene|alken\w+\s+\d', d):
                # Has a numbered position - might be internal
                pass  # conservative: don't assume
            if "disubstituted" in d or "trisubstituted" in d or "tetrasubstituted" in d:
                if "terminal" not in d and "1-" not in d:
                    result["ez_bonds"] = max(result["ez_bonds"], 1)

        # Detect allene/biphenyl for axial chirality
        if any(kw in d for kw in ["allene", "cumulene", "biphenyl", "binaphthol", "atropisomer", "axial chirality"]):
            result["axial_chirality"] = 1

        # Detect cyclohexane ring considerations
        if "cyclohexane" in d or "cyclohex" in d:
            result["ring_type"] = "cyclohexane"
            # Check for 1,2- or 1,4- disubstituted patterns
            if re.search(r'1[,/-]2', d) or re.search(r'1[,/-]4', d):
                result["disubstituted_ring"] = True

        return result

    def _check_bredts_rule(self, description: str) -> Optional[str]:
        """Check for Bredt's rule violations (bridgehead alkenes in small bicyclic systems)."""
        d = description.lower()
        if "bicyclo" in d:
            # Extract ring sizes
            m = re.search(r'bicyclo\[(\d+)\.(\d+)\.(\d+)\]', d)
            if m:
                sizes = sorted([int(m.group(1)), int(m.group(2)), int(m.group(3))])
                bridgehead = sizes[0] + sizes[1] - 1
                # Bredt's rule: bridgehead alkene unstable if bridge < 8 atoms
                if bridgehead < 8:
                    return (f"Bredt's rule: bridgehead alkene in bicyclo[{m.group(1)}.{m.group(2)}.{m.group(3)}] "
                            f"is unstable (bridge size {bridgehead} < 8). "
                            f"No bridgehead double bond isomers possible.")
        return None

    def count_stereoisomers(self, description: str) -> dict:
        """
        Count stereoisomers from a molecular description.

        Args:
            description: text like "2,3-dibromobutane" or "compound with 3 chiral centers and 1 meso possibility"

        Returns:
            dict with chiral_centers, stereogenic_elements, total_stereoisomers, meso_forms,
            optically_active_forms, enantiomer_pairs, breakdown
        """
        bredt = self._check_bredts_rule(description)
        if bredt:
            return {
                "chiral_centers": 0,
                "stereogenic_elements": [],
                "total_stereoisomers": 0,
                "meso_forms": 0,
                "optically_active_forms": 0,
                "enantiomer_pairs": 0,
                "breakdown": bredt
            }

        parsed = self._parse_description(description)
        n_cc = parsed["chiral_centers"]
        n_ez = parsed["ez_bonds"]
        n_axial = parsed.get("axial_chirality", 0)
        meso_possible = parsed["meso_possible"]
        matched_name = parsed.get("matched_name", "")

        # Build stereogenic elements list
        stereogenic = []
        if n_cc > 0:
            stereogenic.extend([f"chiral center {i+1}" for i in range(n_cc)])
        if n_ez > 0:
            stereogenic.extend([f"E/Z double bond {i+1}" for i in range(n_ez)])
        if n_axial > 0:
            stereogenic.extend(["axial chirality element"])

        # Total stereogenic elements
        n_total_elements = n_cc + n_ez + n_axial

        # Calculate base: 2^n
        base_isomers = 2 ** n_total_elements

        # Determine meso forms
        if n_cc == 0 and n_axial == 0:
            meso_forms = 0
        elif meso_possible:
            # For simple symmetrical cases with even chiral centers
            # Common pattern: n even, molecule symmetrical → 1 meso form
            if n_cc >= 2 and n_cc % 2 == 0:
                meso_forms = 1
            elif n_cc == 2:
                meso_forms = 1
            else:
                meso_forms = 0
        else:
            meso_forms = 0

        # Total distinct stereoisomers
        total = base_isomers - meso_forms
        optically_active = total
        enantiomer_pairs = optically_active // 2

        # Build explanation
        parts = []
        if n_cc > 0:
            parts.append(f"{n_cc} chiral center{'s' if n_cc > 1 else ''} → up to 2^{n_cc} = {2**n_cc} combinations")
        if n_ez > 0:
            parts.append(f"{n_ez} E/Z double bond{'s' if n_ez > 1 else ''} → 2^{n_ez} = {2**n_ez} configuration{'s' if n_ez > 1 else ''}")
        if n_axial > 0:
            parts.append(f"{n_axial} axial chirality element{'s' if n_axial > 1 else ''} → 2^{n_axial} configuration{'s' if n_axial > 1 else ''}")
        if n_total_elements > 1:
            parts.append(f"Combined: 2^{n_total_elements} = {base_isomers}")
        if meso_forms > 0:
            parts.append(f"Subtract {meso_forms} meso form{'s' if meso_forms > 1 else ''} (internally compensated)")
            parts.append(f"→ {total} distinct stereoisomers ({optically_active} optically active, {enantiomer_pairs} enantiomer pair{'s' if enantiomer_pairs > 1 else ''}, {meso_forms} meso)")

        breakdown = ". ".join(parts) if parts else "No stereogenic elements identified."

        if matched_name and parsed.get("notes"):
            breakdown += f"\nNote: {parsed['notes']}"

        # Ring conformation note
        if parsed.get("disubstituted_ring"):
            breakdown += "\nNote: For 1,2-disubstituted cyclohexanes, cis/trans relates to ring conformation. Cis-1,2 with identical substituents can be meso."

        # Special cases
        if n_cc == 1 and n_ez == 0 and n_axial == 0:
            breakdown += "\nOne chiral center → exactly 2 enantiomers (one pair)."

        return {
            "chiral_centers": n_cc,
            "stereogenic_elements": stereogenic,
            "total_stereoisomers": total,
            "meso_forms": meso_forms,
            "optically_active_forms": optically_active,
            "enantiomer_pairs": enantiomer_pairs,
            "breakdown": breakdown
        }

    def check_meso(self, description: str) -> dict:
        """Check if a molecule has meso forms."""
        parsed = self._parse_description(description)
        n_cc = parsed["chiral_centers"]
        n_ez = parsed["ez_bonds"]
        n_axial = parsed.get("axial_chirality", 0)
        meso_possible = parsed["meso_possible"]
        matched_name = parsed.get("matched_name", "")

        result = {
            "has_meso": False,
            "meso_count": 0,
            "explanation": "",
            "symmetry_analysis": ""
        }

        if n_cc < 2:
            result["explanation"] = f"Only {n_cc} chiral center{'s' if n_cc != 1 else ''}. Meso forms require at least 2 stereocenters and an internal plane of symmetry."
            return result

        if meso_possible or matched_name:
            # Known meso molecule
            result["has_meso"] = True
            result["meso_count"] = 1
            result["explanation"] = parsed.get("notes", "Molecule has an internal plane of symmetry making the (R,S) configuration achiral.")
            result["symmetry_analysis"] = "Internal mirror plane bisects the molecule, making one stereoisomer achiral (meso)."
        else:
            # Heuristic check: even number of identical chiral centers
            # Check if description mentions identical substituents
            d = description.lower()
            has_symmetry = (
                any(kw in d for kw in ["symmetric", "symmetrical", "identical substituents",
                                         "same substituents", "mirror plane"])
                or re.search(r'(\w+)-(\w+)\b.*\1-\2', d)  # repeated pattern like 2,3-dibromo
            )
            if has_symmetry and n_cc >= 2:
                result["has_meso"] = True
                result["meso_count"] = 1
                result["explanation"] = "Symmetry indicators found in description; meso form is likely."
                result["symmetry_analysis"] = "The molecule appears to have an internal symmetry element."
            else:
                result["explanation"] = (f"{n_cc} chiral centers detected but no clear symmetry element found. "
                                          "Meso form requires an internal plane or center of symmetry.")
                result["symmetry_analysis"] = "No internal symmetry detected. All stereoisomers are likely optically active."

        return result

    def analyze_chirality(self, smiles: str = None, iupac: str = None) -> dict:
        """Analyze chirality from SMILES or IUPAC name."""
        text = ""
        if iupac:
            text = iupac
        elif smiles:
            text = self._smiles_to_description(smiles)
        else:
            return {"error": "Provide either SMILES or IUPAC name"}

        if not text:
            return {"error": "Could not parse input"}

        return self.count_stereoisomers(text)

    def _smiles_to_description(self, smiles: str) -> str:
        """
        Basic SMILES → chirality description converter.
        Handles R/S notation and CIP stereocenters.
        """
        s = smiles.strip()
        desc_parts = []
        chiral_centers = 0

        # Count @ and @@ for tetrahedral stereochemistry
        at_symbols = re.findall(r'(@@?)', s)
        chiral_centers = len(at_symbols)

        # Count / and \ for E/Z double bonds
        slash_symbols = re.findall(r'([/\\])', s)
        ez_bonds = len(slash_symbols) // 2  # Each double bond needs 2 directional symbols

        # Check for ring closure
        ring_digits = set(re.findall(r'(\d+)', s))
        has_ring = len(ring_digits) > 0

        if chiral_centers > 0:
            desc_parts.append(f"{chiral_centers} chiral centers")
        if ez_bonds > 0:
            desc_parts.append(f"{ez_bonds} E/Z bonds")
        if has_ring:
            desc_parts.append("ring system present")

        # Try to identify the base structure
        if not desc_parts:
            if "=" in s and "/" in s or "\\" in s:
                return "alkene with E/Z isomerism"
            return ""

        return ", ".join(desc_parts)


if __name__ == "__main__":
    counter = StereoisomerCounter()

    print("=" * 60)
    print("STEREOISOMER COUNTER — Test Suite")
    print("=" * 60)

    # Test known molecules
    tests = [
        "2,3-dibromobutane",
        "tartaric acid",
        "2-chlorobutane",
        "2-butene",
        "alanine",
        "cholesterol",
        "1,2-dimethylcyclohexane",
        "1,2-dichloroethene",
        "allene",
        "biphenyl",
        "compound with 3 chiral centers",
        "compound with 4 chiral centers and meso possibility",
        "bicyclo[2.2.1]hept-2-ene",  # Bredt's rule
    ]

    for t in tests:
        result = counter.count_stereoisomers(t)
        print(f"\n  Input: '{t}'")
        print(f"  Chiral centers: {result['chiral_centers']}")
        print(f"  Stereogenic elements: {result['stereogenic_elements']}")
        print(f"  Total stereoisomers: {result['total_stereoisomers']}")
        print(f"  Meso forms: {result['meso_forms']}")
        print(f"  Optically active: {result['optically_active_forms']}")
        print(f"  Enantiomer pairs: {result['enantiomer_pairs']}")

    # Test meso check
    print("\n" + "-" * 40)
    print("Meso checks:")
    for t in ["2,3-dibromobutane", "tartaric acid", "alanine", "2-chlorobutane"]:
        r = counter.check_meso(t)
        print(f"  {t}: has_meso={r['has_meso']}, meso_count={r['meso_count']}")

    # Test SMILES analysis
    print("\n" + "-" * 40)
    print("SMILES analysis:")
    smiles_tests = [
        ("C([C@@H](C(=O)O)N)", "threonine-like"),
        ("C/C=C/C", "2-butene"),
        ("C(C)C[C@@H](C)O", "chiral alcohol"),
    ]
    for smi, name in smiles_tests:
        r = counter.analyze_chirality(smiles=smi)
        print(f"  {name} ({smi}): {r}")

    # Test E/Z with explicit description
    print("\n" + "-" * 40)
    print("E/Z counting:")
    ez_tests = [
        "alkene with E/Z isomerism",
        "compound with 2 chiral centers and 1 E/Z double bond",
    ]
    for t in ez_tests:
        r = counter.count_stereoisomers(t)
        print(f"  '{t}' → {r['stereogenic_elements']}, total={r['total_stereoisomers']}")

    print("\n[OK] All tests complete.")
