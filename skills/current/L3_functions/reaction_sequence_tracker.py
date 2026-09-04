"""
L3 Tool: Reaction Sequence Tracker
Tracks functional group transformations through multi-step organic synthesis sequences.
"""

import re
from typing import Optional


class ReactionSequenceTracker:
    def __init__(self):
        # Transformation database: (starting_group_patterns, reagent_patterns) -> product info
        # Each key is a tuple of (start_group, reagent_pattern_match)
        # Values: {"product": str, "mechanism": str, "regio": str, "stereo": str, "confidence": float, "rxn_type": str}
        self.transformations = self._build_transformation_db()

    def _build_transformation_db(self) -> dict:
        db = {}

        # ── Oxidation ──────────────────────────────────────────────
        # Primary alcohol → aldehyde
        for r in ["PCC", "pcc", "pyridinium chlorochromate", "PDC", "Dess-Martin", "Swern", "IBX", "DMP"]:
            db[("primary alcohol", r)] = {
                "product": "aldehyde", "mechanism": "oxidation",
                "regio": "N/A", "stereo": "retention of stereochemistry at α-carbon",
                "confidence": 0.90 if "PCC" in r or "pcc" in r else 0.93,
                "rxn_type": "oxidation (partial)"
            }
        # Primary alcohol → carboxylic acid
        for r in ["KMnO4", "Jones", "CrO3", "Na2Cr2O7", "K2Cr2O7", "chromic acid", "H2CrO4", "PDC/aq", "PDC in water"]:
            db[("primary alcohol", r)] = {
                "product": "carboxylic acid", "mechanism": "oxidation",
                "regio": "N/A", "stereo": "racemization at α-carbon possible",
                "confidence": 0.92,
                "rxn_type": "oxidation (full)"
            }
        # Secondary alcohol → ketone
        for r in ["PCC", "pcc", "PDC", "Dess-Martin", "Swern", "IBX", "DMP", "Jones", "CrO3", "KMnO4", "chromic acid"]:
            db[("secondary alcohol", r)] = {
                "product": "ketone", "mechanism": "oxidation",
                "regio": "N/A", "stereo": "loss of chirality at oxidized carbon",
                "confidence": 0.92,
                "rxn_type": "oxidation"
            }
        # Aldehyde → carboxylic acid
        for r in ["KMnO4", "Ag2O", "Tollens", "Jones", "CrO3", "NaClO", "bleach", "NaClO2", "Pinnick", "Na2Cr2O7", "chromic acid"]:
            db[("aldehyde", r)] = {
                "product": "carboxylic acid", "mechanism": "oxidation",
                "regio": "N/A", "stereo": "N/A",
                "confidence": 0.93,
                "rxn_type": "oxidation"
            }
        # Alkene → diol (syn)
        db[("alkene", "OsO4")] = {
            "product": "vicinal diol (syn)", "mechanism": "cycloaddition / [3+2]",
            "regio": "N/A", "stereo": "syn addition",
            "confidence": 0.95, "rxn_type": "dihydroxylation"
        }
        db[("alkene", "KMnO4/cold")] = {
            "product": "vicinal diol (syn)", "mechanism": "cycloaddition",
            "regio": "N/A", "stereo": "syn addition",
            "confidence": 0.88, "rxn_type": "dihydroxylation"
        }
        # Alkene → epoxide
        for r in ["mCPBA", "MMPP", "peracid", "peroxyacid", "MCPBA"]:
            db[("alkene", r)] = {
                "product": "epoxide", "mechanism": "concerted electrophilic addition",
                "regio": "N/A", "stereo": "retention of alkene stereochemistry",
                "confidence": 0.93, "rxn_type": "epoxidation"
            }
        # Alkene → halohydrin
        for r in ["Br2/H2O", "Cl2/H2O"]:
            db[("alkene", r)] = {
                "product": "halohydrin", "mechanism": "electrophilic addition via halonium ion",
                "regio": "Markovnikov (OH adds to more substituted carbon)",
                "stereo": "anti addition",
                "confidence": 0.93, "rxn_type": "halohydrin formation"
            }
        # Alkene → dihalide
        for r in ["Br2", "Br2/CH2Cl2", "Br2/CCl4", "Cl2", "Cl2/CH2Cl2"]:
            db[("alkene", r)] = {
                "product": "vicinal dibromide" if "Br" in r else "vicinal dichloride",
                "mechanism": "electrophilic addition via halonium ion",
                "regio": "N/A", "stereo": "anti addition",
                "confidence": 0.95, "rxn_type": "halogenation"
            }
        # Alkene → alkane (hydrogenation)
        db[("alkene", "H2/Pd")] = {
            "product": "alkane", "mechanism": "syn hydrogenation (heterogeneous catalysis)",
            "regio": "N/A", "stereo": "syn addition",
            "confidence": 0.95, "rxn_type": "hydrogenation"
        }
        db[("alkene", "H2/Pt")] = db[("alkene", "H2/Pd")]
        db[("alkene", "H2/Ni")] = db[("alkene", "H2/Pd")]
        db[("alkene", "H2/Raney Ni")] = db[("alkene", "H2/Pd")]

        # ── Reduction ──────────────────────────────────────────────
        # Aldehyde → primary alcohol
        for r in ["NaBH4", "sodium borohydride", "LiAlH4", "lithium aluminium hydride",
                   "H2/Pd", "H2/Pt", "H2/Ni"]:
            db[("aldehyde", r)] = {
                "product": "primary alcohol", "mechanism": "hydride transfer",
                "regio": "N/A", "stereo": "racemic if prochiral",
                "confidence": 0.95 if "NaBH4" in r or "LiAlH4" in r else 0.90,
                "rxn_type": "reduction"
            }
        # Ketone → secondary alcohol
        for r in ["NaBH4", "LiAlH4", "sodium borohydride", "lithium aluminium hydride"]:
            db[("ketone", r)] = {
                "product": "secondary alcohol", "mechanism": "hydride transfer",
                "regio": "N/A", "stereo": "racemic if prochiral (Felkin-Anh model)",
                "confidence": 0.93, "rxn_type": "reduction"
            }
        # Carboxylic acid → primary alcohol
        db[("carboxylic acid", "LiAlH4")] = {
            "product": "primary alcohol", "mechanism": "hydride transfer (2 equiv)",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.95, "rxn_type": "reduction (strong)"
        }
        # Ester → primary alcohol
        db[("ester", "LiAlH4")] = {
            "product": "primary alcohol (2 equiv)", "mechanism": "hydride transfer",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.93, "rxn_type": "reduction"
        }
        db[("ester", "NaBH4")] = {
            "product": "ester (no reaction)", "mechanism": "NaBH4 is generally unreactive with esters",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.80, "rxn_type": "no reaction"
        }
        # Ester → aldehyde (partial reduction)
        db[("ester", "DIBAL")] = {
            "product": "aldehyde", "mechanism": "hydride transfer, then workup",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.90, "rxn_type": "reduction (partial)"
        }
        db[("ester", "DIBAL-H")] = db[("ester", "DIBAL")]
        # Carboxylic acid → aldehyde (partial reduction)
        db[("carboxylic acid", "DIBAL")] = {
            "product": "no clean reaction; reduce acid chloride with Rosenmund or DIBAL with activation",
            "mechanism": "DIBAL does not reduce carboxylic acids directly",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.70, "rxn_type": "warning"
        }
        # Nitrile → aldehyde
        db[("nitrile", "DIBAL")] = {
            "product": "aldehyde", "mechanism": "hydride addition to C≡N, then workup",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.88, "rxn_type": "reduction (partial)"
        }
        # Nitrile → primary amine
        for r in ["LiAlH4", "H2/Ni", "H2/Pd", "H2/Ra-Ni", "BH3"]:
            db[("nitrile", r)] = {
                "product": "primary amine", "mechanism": "reduction of C≡N",
                "regio": "N/A", "stereo": "N/A",
                "confidence": 0.92, "rxn_type": "reduction"
            }
        # Amide → amine
        db[("amide", "LiAlH4")] = {
            "product": "amine", "mechanism": "reduction of C=O",
            "regio": "N/A", "stereo": "N/A",
            "confidence": 0.90, "rxn_type": "reduction"
        }
        # Alkene → alkane (dissolving metal)
        db[("alkene", "Na/NH3")] = {
            "product": "alkane", "mechanism": "dissolving metal reduction",
            "regio": "N/A", "stereo": "trans addition (anti)",
            "confidence": 0.88, "rxn_type": "reduction (dissolving metal)"
        }
        # Alkyne → trans-alkene
        db[("alkyne", "Na/NH3")] = {
            "product": "trans-alkene", "mechanism": "dissolving metal reduction",
            "regio": "N/A", "stereo": "trans (anti addition)",
            "confidence": 0.92, "rxn_type": "reduction (dissolving metal)"
        }
        # Alkyne → cis-alkene
        db[("alkyne", "H2/Lindlar")] = {
            "product": "cis-alkene", "mechanism": "syn hydrogenation (poisoned catalyst)",
            "regio": "N/A", "stereo": "cis (syn addition)",
            "confidence": 0.93, "rxn_type": "hydrogenation (partial)"
        }
        db[("alkyne", "Lindlar")] = db[("alkyne", "H2/Lindlar")]
        db[("alkyne", "H2/Pd")] = {
            "product": "alkane", "mechanism": "full hydrogenation",
            "regio": "N/A", "stereo": "syn",
            "confidence": 0.95, "rxn_type": "hydrogenation (full)"
        }
        # Nitro → amine
        for r in ["Sn/HCl", "Fe/HCl", "Zn/HCl", "H2/Pd", "H2/Pt", "H2/Ni", "LiAlH4", "Pd/C"]:
            db[("nitro", r)] = {
                "product": "amine", "mechanism": "reduction of NO2",
                "regio": "N/A", "stereo": "N/A",
                "confidence": 0.95, "rxn_type": "reduction"
            }

        # ── Protecting Groups ─────────────────────────────────────
        # Alcohol protection (TBDMS)
        for r in ["TBDMSCl", "TBDMS-Cl", "TBDMSCI", "TBDPSCl", "imida", "imidazole"]:
            if "TBDMS" in r or "TBDPS" in r:
                db[("alcohol", r)] = {
                    "product": f"{'TBDMS' if 'TBDMS' in r else 'TBDPS'} ether (protected alcohol)",
                    "mechanism": "silyl ether formation", "regio": "primary > secondary > tertiary",
                    "stereo": "retention", "confidence": 0.90, "rxn_type": "protection (silyl ether)"
                }
        # Alcohol deprotection (TBDMS)
        for r in ["TBAF", "AcOH", "HF", "HF/pyridine", "KF"]:
            db[("TBDMS ether", r)] = {
                "product": "alcohol", "mechanism": "desilylation",
                "regio": "N/A", "stereo": "retention", "confidence": 0.92, "rxn_type": "deprotection"
            }
        db[("TBDPS ether", "TBAF")] = {
            "product": "alcohol", "mechanism": "desilylation",
            "regio": "N/A", "stereo": "retention", "confidence": 0.90, "rxn_type": "deprotection"
        }
        # Alcohol protection (acetal)
        for r in ["acetal formation", "ethyleneglycol", "ethylene glycol", "HOCH2CH2OH", "TsOH", "pTsOH", "PPTS"]:
            db[("aldehyde", r)] = {
                "product": "acetal", "mechanism": "acetal formation (acid-catalyzed)",
                "regio": "N/A", "stereo": "N/A", "confidence": 0.88, "rxn_type": "protection (acetal)"
            }
            db[("ketone", r)] = {
                "product": "ketal", "mechanism": "ketal formation (acid-catalyzed)",
                "regio": "N/A", "stereo": "N/A", "confidence": 0.85, "rxn_type": "protection (ketal)"
            }
        # Acetal/ketal deprotection
        for r in ["aq HCl", "aqueous acid", "H3O+", "HCl/H2O"]:
            db[("acetal", r)] = {
                "product": "aldehyde", "mechanism": "acid-catalyzed hydrolysis",
                "regio": "N/A", "stereo": "N/A", "confidence": 0.92, "rxn_type": "deprotection"
            }
            db[("ketal", r)] = {
                "product": "ketone", "mechanism": "acid-catalyzed hydrolysis",
                "regio": "N/A", "stereo": "N/A", "confidence": 0.92, "rxn_type": "deprotection"
            }
        # Amine protection (Boc)
        db[("amine", "Boc2O")] = {
            "product": "N-Boc protected amine", "mechanism": "carbamate formation",
            "regio": "N/A", "stereo": "retention", "confidence": 0.92, "rxn_type": "protection (Boc)"
        }
        db[("amine", "(Boc)2O")] = db[("amine", "Boc2O")]
        # Boc deprotection
        for r in ["TFA", "trifluoroacetic acid", "HCl/dioxane", "HCl in dioxane", "TFA/DCM"]:
            db[("N-Boc protected amine", r)] = {
                "product": "amine", "mechanism": "acidolytic deprotection",
                "regio": "N/A", "stereo": "retention", "confidence": 0.93, "rxn_type": "deprotection"
            }
        # Amine protection (Cbz)
        db[("amine", "Cbz-Cl")] = {
            "product": "N-Cbz protected amine", "mechanism": "carbamate formation",
            "regio": "N/A", "stereo": "retention", "confidence": 0.88, "rxn_type": "protection (Cbz)"
        }
        db[("amine", "C6H5CH2OCOCl")] = db[("amine", "Cbz-Cl")]
        # Cbz deprotection
        db[("N-Cbz protected amine", "H2/Pd")] = {
            "product": "amine", "mechanism": "hydrogenolysis",
            "regio": "N/A", "stereo": "retention", "confidence": 0.90, "rxn_type": "deprotection (hydrogenolysis)"
        }
        # Amine protection (Fmoc)
        db[("amine", "Fmoc-Cl")] = {
            "product": "N-Fmoc protected amine", "mechanism": "carbamate formation",
            "regio": "N/A", "stereo": "retention", "confidence": 0.88, "rxn_type": "protection (Fmoc)"
        }
        # Fmoc deprotection
        for r in ["piperidine", "20% piperidine", "piperidine/DMF", "DBU"]:
            db[("N-Fmoc protected amine", r)] = {
                "product": "amine", "mechanism": "β-elimination",
                "regio": "N/A", "stereo": "retention", "confidence": 0.93, "rxn_type": "deprotection (base)"
            }

        # ── C–C Bond Forming ──────────────────────────────────────
        # Grignard addition
        for r in ["Grignard", "RMgX", "RMgBr", "CH3MgBr", "PhMgBr", "MeMgBr", "EtMgBr"]:
            db[("aldehyde", r)] = {
                "product": "secondary alcohol", "mechanism": "nucleophilic addition of R- to carbonyl",
                "regio": "N/A", "stereo": "racemic if prochiral; chelation/Felkin-Anh control possible",
                "confidence": 0.90, "rxn_type": "Grignard addition"
            }
            db[("ketone", r)] = {
                "product": "tertiary alcohol", "mechanism": "nucleophilic addition of R- to carbonyl",
                "regio": "N/A", "stereo": "racemic if prochiral",
                "confidence": 0.90, "rxn_type": "Grignard addition"
            }
            db[("ester", r)] = {
                "product": "tertiary alcohol (2 equiv R-)", "mechanism": "addition-elimination-addition",
                "regio": "N/A", "stereo": "N/A",
                "confidence": 0.88, "rxn_type": "Grignard addition"
            }
            db[("epoxide", r)] = {
                "product": "alcohol (ring opened)", "mechanism": "nucleophilic ring opening",
                "regio": "attack at less substituted carbon (SN2-like)",
                "stereo": "inversion at attack site",
                "confidence": 0.85, "rxn_type": "Grignard ring opening"
            }
        # Organolithium
        for r in ["RLi", "n-BuLi", "t-BuLi", "PhLi", "MeLi"]:
            db[("aldehyde", r)] = {
                "product": "secondary alcohol", "mechanism": "nucleophilic addition",
                "regio": "N/A", "stereo": "racemic if prochiral",
                "confidence": 0.88, "rxn_type": "organolithium addition"
            }
            db[("ketone", r)] = {
                "product": "tertiary alcohol", "mechanism": "nucleophilic addition",
                "regio": "N/A", "stereo": "racemic if prochiral",
                "confidence": 0.88, "rxn_type": "organolithium addition"
            }
        # Wittig
        for r in ["Wittig", "Ph3P=CH2", "ylide", "ylid", "Wittig reagent"]:
            db[("aldehyde", r)] = {
                "product": "alkene", "mechanism": "oxaphosphetane formation → elimination",
                "regio": "N/A", "stereo": "stabilized ylide → E; non-stabilized → Z",
                "confidence": 0.85, "rxn_type": "Wittig reaction"
            }
            db[("ketone", r)] = {
                "product": "alkene", "mechanism": "oxaphosphetane formation → elimination",
                "regio": "N/A", "stereo": "E/Z mixture common",
                "confidence": 0.80, "rxn_type": "Wittig reaction"
            }
        # Horner-Wadsworth-Emmons (HWE)
        for r in ["HWE", "Horner-Wadsworth-Emmons", "phosphonate", "Wadsworth-Emmons"]:
            db[("aldehyde", r)] = {
                "product": "alkene (predominantly E)", "mechanism": "phosphonate carbanion addition-elimination",
                "regio": "N/A", "stereo": "predominantly E-isomer",
                "confidence": 0.90, "rxn_type": "HWE olefination"
            }
        # Aldol
        for r in ["aldol", "LDA", "NaOH", "NaOEt"]:
            db[("aldehyde", r)] = {
                "product": "β-hydroxy aldehyde", "mechanism": "aldol addition",
                "regio": "enolate attacks carbonyl carbon",
                "stereo": "Zimmerman-Traxler: syn if enolate geometry controlled",
                "confidence": 0.82, "rxn_type": "aldol reaction"
            }
            db[("ketone", r)] = {
                "product": "β-hydroxy ketone", "mechanism": "aldol addition",
                "regio": "enolate attacks carbonyl carbon",
                "stereo": "Zimmerman-Traxler model",
                "confidence": 0.80, "rxn_type": "aldol reaction"
            }
        # Michael addition
        for r in ["Michael", "Michael addition", "enolate", "cuprate"]:
            db[("α,β-unsaturated ketone", r)] = {
                "product": "1,5-dicarbonyl compound", "mechanism": "conjugate (1,4-) addition",
                "regio": "addition at β-position", "stereo": "thermodynamic control typical",
                "confidence": 0.83, "rxn_type": "Michael addition"
            }
            db[("α,β-unsaturated ester", r)] = {
                "product": "β-substituted ester", "mechanism": "conjugate addition",
                "regio": "addition at β-position", "stereo": "N/A",
                "confidence": 0.80, "rxn_type": "Michael addition"
            }
        # Suzuki coupling
        for r in ["Suzuki", "Pd(PPh3)4", "Pd(dppf)", "boronic acid", "Suzuki-Miyaura"]:
            db[("aryl halide", r)] = {
                "product": "biaryl", "mechanism": "Pd-catalyzed cross-coupling with boronic acid",
                "regio": "retention of position", "stereo": "retention",
                "confidence": 0.88, "rxn_type": "Suzuki-Miyaura coupling"
            }
            db[("vinyl halide", r)] = {
                "product": "styrene derivative", "mechanism": "Pd-catalyzed cross-coupling",
                "regio": "retention of position", "stereo": "retention of alkene geometry",
                "confidence": 0.85, "rxn_type": "Suzuki-Miyaura coupling"
            }
        # Heck coupling
        for r in ["Heck", "Heck reaction", "Pd(OAc)2"]:
            db[("aryl halide", r)] = {
                "product": "styrene derivative (alkene)", "mechanism": "Pd-catalyzed arylation of alkene",
                "regio": "β-arylation of alkene", "stereo": "predominantly trans",
                "confidence": 0.83, "rxn_type": "Heck reaction"
            }
        # Sonogashira coupling
        for r in ["Sonogashira", "Pd/Cu", "terminal alkyne"]:
            db[("aryl halide", r)] = {
                "product": "aryl alkyne", "mechanism": "Pd/Cu-catalyzed coupling",
                "regio": "retention", "stereo": "N/A",
                "confidence": 0.87, "rxn_type": "Sonogashira coupling"
            }
        # Claisen condensation
        db[("ester", "NaOEt")] = {
            "product": "β-keto ester", "mechanism": "Claisen condensation",
            "regio": "α-carbon of ester", "stereo": "N/A",
            "confidence": 0.82, "rxn_type": "Claisen condensation"
        }
        db[("ester", "LDA")] = {
            "product": "β-keto ester", "mechanism": "directed Claisen condensation",
            "regio": "α-carbon of ester", "stereo": "N/A",
            "confidence": 0.82, "rxn_type": "Claisen condensation"
        }
        # Dieckmann condensation
        db[("diester", "NaOEt")] = {
            "product": "β-keto ester (cyclic)", "mechanism": "intramolecular Claisen (Dieckmann)",
            "regio": "N/A (intramolecular)", "stereo": "N/A",
            "confidence": 0.80, "rxn_type": "Dieckmann condensation"
        }
        # Friedel-Crafts alkylation
        for r in ["AlCl3", "FeCl3", "BF3", "Friedel-Crafts"]:
            db[("benzene", r)] = {
                "product": "alkylbenzene", "mechanism": "electrophilic aromatic substitution",
                "regio": "ortho/para directing (for alkyl groups)",
                "stereo": "carbocation rearrangement possible",
                "confidence": 0.78, "rxn_type": "Friedel-Crafts alkylation"
            }
        # Friedel-Crafts acylation
        db[("benzene", "acetyl chloride/AlCl3")] = {
            "product": "acetophenone", "mechanism": "electrophilic aromatic substitution (acylation)",
            "regio": "meta director (for COCH3)", "stereo": "no rearrangement",
            "confidence": 0.85, "rxn_type": "Friedel-Crafts acylation"
        }
        db[("benzene", "RCOCl/AlCl3")] = {
            "product": "aryl ketone", "mechanism": "electrophilic aromatic substitution (acylation)",
            "regio": "meta director (for acyl)", "stereo": "no rearrangement",
            "confidence": 0.85, "rxn_type": "Friedel-Crafts acylation"
        }
        # Diels-Alder
        db[("diene", "dienophile")] = {
            "product": "cyclohexene derivative", "mechanism": "[4+2] cycloaddition",
            "regio": "ortho/para if electron-withdrawing on dienophile",
            "stereo": "endo rule; stereospecific",
            "confidence": 0.88, "rxn_type": "Diels-Alder reaction"
        }

        # ── Functional Group Interconversions ─────────────────────
        # CN → COOH (hydrolysis)
        for r in ["acid hydrolysis", "H3O+", "HCl/reflux", "aq HCl"]:
            db[("nitrile", r)] = {
                "product": "carboxylic acid", "mechanism": "acid-catalyzed nitrile hydrolysis",
                "regio": "N/A", "stereo": "N/A",
                "confidence": 0.90, "rxn_type": "hydrolysis"
            }
        for r in ["base hydrolysis", "NaOH/aq", "NaOH/reflux"]:
            db[("nitrile", r)] = {
                "product": "carboxylate salt (→ carboxylic acid on acidification)",
                "mechanism": "base-catalyzed nitrile hydrolysis",
                "regio": "N/A", "stereo": "N/A",
                "confidence": 0.88, "rxn_type": "hydrolysis"
            }
        # NO2 → NH2 (reduction — already covered above in reduction section)

        # COOH → acid chloride
        for r in ["SOCl2", "thionyl chloride", "oxalyl chloride", "(COCl)2", "PCl5", "PCl3"]:
            db[("carboxylic acid", r)] = {
                "product": "acid chloride", "mechanism": "nucleophilic acyl substitution",
                "regio": "N/A", "stereo": "retention",
                "confidence": 0.95, "rxn_type": "acid chloride formation"
            }
        # COOH → amide (via coupling)
        for r in ["SOCl2/NH3", "acid chloride + NH3", "DCC", "EDC", "HATU"]:
            db[("carboxylic acid", r)] = {
                "product": "amide", "mechanism": "amide bond formation",
                "regio": "N/A", "stereo": "retention",
                "confidence": 0.85, "rxn_type": "amide formation"
            }
        # Acid chloride → ester
        for r in ["ROH", "alcohol", "EtOH", "MeOH", "CH3OH", "ethanol", "methanol"]:
            db[("acid chloride", r)] = {
                "product": "ester", "mechanism": "nucleophilic acyl substitution",
                "regio": "N/A", "stereo": "retention",
                "confidence": 0.92, "rxn_type": "esterification"
            }
        # Acid chloride → amide
        for r in ["NH3", "amine", "RNH2"]:
            db[("acid chloride", r)] = {
                "product": "amide", "mechanism": "nucleophilic acyl substitution",
                "regio": "N/A", "stereo": "retention",
                "confidence": 0.93, "rxn_type": "amidation"
            }
        # Alcohol → alkene (elimination)
        for r in ["H2SO4/heat", "conc H2SO4", "E1", "H2SO4, heat"]:
            db[("tertiary alcohol", r)] = {
                "product": "alkene", "mechanism": "E1 elimination",
                "regio": "Zaitsev (more substituted alkene)",
                "stereo": "mixture of E/Z possible",
                "confidence": 0.85, "rxn_type": "dehydration (E1)"
            }
            db[("secondary alcohol", r)] = {
                "product": "alkene", "mechanism": "E1/E2 elimination",
                "regio": "Zaitsev",
                "stereo": "mixture",
                "confidence": 0.80, "rxn_type": "dehydration"
            }
        # Tosylate formation
        db[("alcohol", "TsCl")] = {
            "product": "tosylate", "mechanism": "sulfonate ester formation",
            "regio": "N/A", "stereo": "inversion of configuration (SN2)",
            "confidence": 0.92, "rxn_type": "tosylation"
        }
        db[("alcohol", "MsCl")] = {
            "product": "mesylate", "mechanism": "sulfonate ester formation",
            "regio": "N/A", "stereo": "retention (then SN2 with nucleophile)",
            "confidence": 0.92, "rxn_type": "mesylation"
        }
        # SN2
        db[("primary halide", "NaCN")] = {
            "product": "nitrile", "mechanism": "SN2",
            "regio": "N/A", "stereo": "inversion",
            "confidence": 0.90, "rxn_type": "SN2 substitution"
        }
        db[("primary halide", "NaOH")] = {
            "product": "alcohol", "mechanism": "SN2",
            "regio": "N/A", "stereo": "inversion",
            "confidence": 0.90, "rxn_type": "SN2 substitution"
        }
        db[("primary halide", "NaI")] = {
            "product": "iodide (Finkelstein)", "mechanism": "SN2 (Finkelstein)",
            "regio": "N/A", "stereo": "inversion",
            "confidence": 0.92, "rxn_type": "Finkelstein reaction"
        }
        # Epoxide ring opening
        db[("epoxide", "NaOH")] = {
            "product": "diol", "mechanism": "base-catalyzed epoxide opening",
            "regio": "attack at less substituted carbon",
            "stereo": "anti (trans diol)",
            "confidence": 0.88, "rxn_type": "epoxide opening"
        }
        db[("epoxide", "H3O+")] = {
            "product": "diol", "mechanism": "acid-catalyzed epoxide opening",
            "regio": "attack at more substituted carbon",
            "stereo": "anti (trans diol)",
            "confidence": 0.88, "rxn_type": "epoxide opening"
        }
        # Diol → epoxide (reverse)
        db[("diol", "TsCl")] = {
            "product": "epoxide (via tosylate, then base)", "mechanism": "tosylation then intramolecular SN2",
            "regio": "N/A", "stereo": "retention of relative stereochemistry → cis diols → epoxides",
            "confidence": 0.75, "rxn_type": "epoxide formation"
        }

        # ── Named Reactions keyword mapping ───────────────────────
        self._named_reactions = {
            "Grignard": "Grignard reaction",
            "RMgX": "Grignard reaction",
            "Wittig": "Wittig olefination",
            "HWE": "Horner-Wadsworth-Emmons olefination",
            "aldol": "Aldol reaction",
            "Michael": "Michael addition (conjugate addition)",
            "Suzuki": "Suzuki-Miyaura coupling",
            "Heck": "Heck reaction",
            "Sonogashira": "Sonogashira coupling",
            "Diels-Alder": "Diels-Alder cycloaddition",
            "Friedel-Crafts": "Friedel-Crafts reaction",
            "Claisen": "Claisen condensation",
            "Dieckmann": "Dieckmann condensation",
            "Swern": "Swern oxidation",
            "Dess-Martin": "Dess-Martin periodinane oxidation",
            "Finkelstein": "Finkelstein reaction",
            "Jones": "Jones oxidation",
            "Lindlar": "Lindlar hydrogenation (partial)",
            "Tollens": "Tollens' test / silver mirror oxidation",
            "Pinnick": "Pinnick oxidation",
            "Rosenmund": "Rosenmund reduction",
            "KMnO4": "potassium permanganate oxidation",
            "PCC": "PCC oxidation (partial)",
            "PDC": "PDC oxidation",
            "LiAlH4": "Lithium aluminium hydride reduction",
            "NaBH4": "Sodium borohydride reduction",
            "DIBAL": "DIBAL-H partial reduction",
            "TBAF": "TBAF deprotection",
            "Boc2O": "Boc protection",
            "Cbz-Cl": "Cbz protection",
            "Fmoc-Cl": "Fmoc protection",
            "TBDMSCl": "TBDMS protection",
            "SOCl2": "Acid chloride formation (thionyl chloride)",
            "mCPBA": "Epoxidation (peracid)",
            "OsO4": "Dihydroxylation (OsO4)",
            "Na/NH3": "Dissolving metal reduction (Birch-type)",
        }

        return db

    def _classify_functional_group(self, structure: str) -> str:
        """Classify a structure description into a functional group key."""
        s = structure.lower().strip()
        # Order matters: more specific first
        if any(k in s for k in ["primary alcohol", "1° alcohol", "primary oh"]):
            return "primary alcohol"
        if any(k in s for k in ["secondary alcohol", "2° alcohol", "secondary oh"]):
            return "secondary alcohol"
        if any(k in s for k in ["tertiary alcohol", "3° alcohol", "tertiary oh"]):
            return "tertiary alcohol"
        if "alcohol" in s or "ol" in s.split()[-1] if s.split() else "":
            return "alcohol"
        if any(k in s for k in ["carboxylic acid", "cooh"]):
            return "carboxylic acid"
        if any(k in s for k in ["acid chloride", "acyl chloride", "cocl"]):
            return "acid chloride"
        if any(k in s for k in ["nitrile", "cyanide", "cn"]):
            return "nitrile"
        if any(k in s for k in ["aldehyde"]):
            return "aldehyde"
        if any(k in s for k in ["ketone", "one"]):
            return "ketone"
        if any(k in s for k in ["ester", "coo", "coor"]):
            return "ester"
        if any(k in s for k in ["amide", "conh2"]):
            return "amide"
        if any(k in s for k in ["amine", "nh2"]):
            return "amine"
        if any(k in s for k in ["nitro", "no2"]):
            return "nitro"
        if any(k in s for k in ["alkene", "double bond", "c=c", "olefin"]):
            return "alkene"
        if any(k in s for k in ["alkyne", "triple bond", "c≡c"]):
            return "alkyne"
        if any(k in s for k in ["epoxide", "oxirane"]):
            return "epoxide"
        if any(k in s for k in ["diol", "glycol", "dihydroxy"]):
            return "diol"
        if any(k in s for k in ["acetal"]):
            return "acetal"
        if any(k in s for k in ["ketal"]):
            return "ketal"
        if any(k in s for k in ["tbems ether", "silyl ether"]):
            return "TBDMS ether"
        if any(k in s for k in ["tbdps ether"]):
            return "TBDPS ether"
        if "n-boc" in s or "nboc" in s or "boc protected" in s:
            return "N-Boc protected amine"
        if "n-cbz" in s or "ncbz" in s or "cbz protected" in s:
            return "N-Cbz protected amine"
        if "n-fmoc" in s or "nfmoc" in s or "fmoc protected" in s:
            return "N-Fmoc protected amine"
        if any(k in s for k in ["aryl halide", "bromobenzene", "iodobenzene", "chlorobenzene", "aryl bromide"]):
            return "aryl halide"
        if any(k in s for k in ["vinyl halide", "bromoethene"]):
            return "vinyl halide"
        if any(k in s for k in ["primary halide", "alkyl halide"]):
            return "primary halide"
        if any(k in s for k in ["tosylate", "ots"]):
            return "tosylate"
        if any(k in s for k in ["mesylate", "oms"]):
            return "mesylate"
        if any(k in s for k in ["benzene", "phenyl", "aromatic ring"]):
            return "benzene"
        if any(k in s for k in ["diene"]):
            return "diene"
        if any(k in s for k in ["α,β-unsaturated ketone", "enone"]):
            return "α,β-unsaturated ketone"
        if any(k in s for k in ["α,β-unsaturated ester", "enoate"]):
            return "α,β-unsaturated ester"
        if any(k in s for k in ["diester"]):
            return "diester"
        if any(k in s for k in ["alkane"]):
            return "alkane"
        return s  # return as-is if no match

    def _normalize_reagent(self, reagent: str) -> str:
        """Normalize reagent string for matching."""
        r = reagent.strip()
        return r

    def predict_product(self, starting_group: str, reagent: str) -> dict:
        """Predict the product of a single reaction step."""
        group = self._classify_functional_group(starting_group)
        reagent_norm = self._normalize_reagent(reagent)

        # Try exact match
        # Collect all matches, then pick the most specific (longest db_reagent match)
        matches = []
        for (sg, rg), info in self.transformations.items():
            if sg == group and self._reagent_matches(reagent_norm, rg):
                matches.append((rg, info))
        # Prefer longer (more specific) reagent descriptions, break ties by confidence
        matches.sort(key=lambda x: (len(x[0]), x[1]["confidence"]), reverse=True)
        best_match = matches[0][1] if matches else None

        if best_match:
            return {
                "product_group": best_match["product"],
                "mechanism": best_match["mechanism"],
                "regioselectivity": best_match["regio"],
                "stereoselectivity": best_match["stereo"],
                "confidence": best_match["confidence"],
                "rxn_type": best_match["rxn_type"]
            }

        # Partial match: find by functional group only
        partial = []
        for (sg, rg), info in self.transformations.items():
            if sg == group:
                partial.append({"reagent_tried": rg, **info})

        if partial:
            return {
                "product_group": "unknown — no matching reagent found",
                "mechanism": "N/A",
                "regioselectivity": "N/A",
                "stereoselectivity": "N/A",
                "confidence": 0.0,
                "rxn_type": "no match",
                "possible_reagents_for_this_group": [
                    {"reagent": p["reagent_tried"], "product": p["product"], "type": p["rxn_type"]}
                    for p in partial[:5]
                ]
            }

        return {
            "product_group": "unknown",
            "mechanism": "N/A",
            "regioselectivity": "N/A",
            "stereoselectivity": "N/A",
            "confidence": 0.0,
            "rxn_type": "no match",
            "hint": f"Functional group '{group}' not recognized in transformation database"
        }

    def _reagent_matches(self, input_reagent: str, db_reagent: str) -> bool:
        """Flexible reagent matching — prefers specific matches over substrings."""
        ir = input_reagent.lower()
        dr = db_reagent.lower()
        if ir == dr:
            return True
        # Full containment: db_reagent fully contained in input
        if dr in ir and len(dr) >= 3:
            return True
        # Single-word component match only if the word is significant (>= 3 chars)
        db_parts = set(re.findall(r'[A-Za-z0-9]{3,}', dr))
        ir_parts = set(re.findall(r'[A-Za-z0-9]{3,}', ir))
        overlap = db_parts & ir_parts
        if len(overlap) >= 1:
            # But reject if db has extra significant words not in input (too broad)
            # e.g., "SOCl2/NH3" should not match just "SOCl2"
            db_only = db_parts - ir_parts
            if db_only and len(db_only) >= 1:
                # db_reagent has extra significant parts → not a good match
                return False
            return True
        return False

    def identify_reaction_type(self, reagent: str, starting_material: str = "") -> str:
        """Identify which named reaction a given reagent/condition pattern corresponds to."""
        r = reagent.strip()
        for key, name in self._named_reactions.items():
            if key.lower() in r.lower():
                return name
        # Check transformations
        if starting_material:
            group = self._classify_functional_group(starting_material)
            for (sg, rg), info in self.transformations.items():
                if sg == group and self._reagent_matches(r, rg):
                    return info["rxn_type"]
        return "unrecognized reagent/condition pattern"

    def track_sequence(self, starting_structure: str, steps: list) -> dict:
        """Track a multi-step synthesis through sequential transformations."""
        current = self._classify_functional_group(starting_structure)
        intermediates = [starting_structure]
        fg_changes = []
        warnings = []
        confidences = []

        for i, step in enumerate(steps):
            reagent = step.get("reagent", "")
            conditions = step.get("conditions", "")
            desc = step.get("description", "")
            full_reagent = f"{reagent} {conditions}".strip()

            result = self.predict_product(current, full_reagent)
            product = result["product_group"]
            confidences.append(result["confidence"])

            fg_changes.append({
                "step": i + 1,
                "from": current,
                "to": product,
                "reagent": full_reagent,
                "mechanism": result.get("mechanism", ""),
                "rxn_type": result.get("rxn_type", "")
            })

            if product.startswith("unknown"):
                warnings.append(f"Step {i + 1}: Could not predict product for '{current}' + '{full_reagent}'")
            elif "no reaction" in result.get("rxn_type", ""):
                warnings.append(f"Step {i + 1}: Reagent '{full_reagent}' does not react with '{current}'")
            elif "warning" in result.get("rxn_type", ""):
                warnings.append(f"Step {i + 1}: {product}")

            intermediates.append(product)
            current = product

        avg_conf = sum(confidences) / len(confidences) if confidences else 0

        return {
            "starting_material": starting_structure,
            "intermediates": intermediates,
            "final_product": current,
            "functional_group_changes": fg_changes,
            "confidence": round(avg_conf, 2),
            "warnings": warnings
        }


if __name__ == "__main__":
    tracker = ReactionSequenceTracker()

    print("=" * 60)
    print("REACTION SEQUENCE TRACKER — Test Suite")
    print("=" * 60)

    # Test 1: Single step prediction
    print("\n--- Test 1: Single-step predictions ---")
    tests = [
        ("primary alcohol", "PCC"),
        ("aldehyde", "LiAlH4"),
        ("alkene", "mCPBA"),
        ("alkyne", "Na/NH3"),
        ("carboxylic acid", "SOCl2"),
        ("amine", "Boc2O"),
        ("nitrile", "LiAlH4"),
    ]
    for group, reagent in tests:
        r = tracker.predict_product(group, reagent)
        print(f"  {group} + {reagent} → {r['product_group']}  (conf: {r['confidence']:.2f})")

    # Test 2: Multi-step synthesis
    print("\n--- Test 2: Multi-step synthesis ---")
    # Ethanol → acetic acid → ethyl acetate
    seq = tracker.track_sequence("primary alcohol", [
        {"reagent": "KMnO4", "conditions": "", "description": "oxidize to carboxylic acid"},
        {"reagent": "SOCl2", "conditions": "", "description": "acid chloride formation"},
        {"reagent": "EtOH", "conditions": "", "description": "esterification"},
    ])
    print(f"  Sequence: primary alcohol → KMnO4 → SOCl2 → EtOH")
    print(f"  Intermediates: {seq['intermediates']}")
    print(f"  Final product: {seq['final_product']}")
    print(f"  Confidence: {seq['confidence']}")
    print(f"  Warnings: {seq['warnings']}")

    # Test 3: Another sequence
    print("\n--- Test 3: Alkyne partial reduction ---")
    seq2 = tracker.track_sequence("alkyne", [
        {"reagent": "H2/Lindlar", "conditions": "", "description": "partial reduction to cis-alkene"},
        {"reagent": "mCPBA", "conditions": "", "description": "epoxidation"},
        {"reagent": "NaOH", "conditions": "", "description": "ring opening to trans diol"},
    ])
    print(f"  Intermediates: {seq2['intermediates']}")
    print(f"  Final product: {seq2['final_product']}")
    print(f"  FG changes: {[(c['from'], '→', c['to']) for c in seq2['functional_group_changes']]}")

    # Test 4: Identify reaction types
    print("\n--- Test 4: Reaction type identification ---")
    id_tests = [
        ("LiAlH4", "carboxylic acid"),
        ("Suzuki", ""),
        ("DIBAL", ""),
        ("mCPBA", "alkene"),
    ]
    for reagent, mat in id_tests:
        print(f"  {reagent} + {mat} → {tracker.identify_reaction_type(reagent, mat)}")

    print("\n[OK] All tests complete.")
