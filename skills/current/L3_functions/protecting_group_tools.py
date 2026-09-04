"""
Protecting Group Strategy Tools for Organic Synthesis

A comprehensive module for planning protecting group strategies in multi-step organic synthesis.
Provides functions to recommend optimal protecting groups based on functional group type and
required stability conditions, with extensive internal reference tables.

Author: OpenClaw Chemistry Assistant
"""

from typing import Dict, List, Optional, Tuple, Literal, TypedDict
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# REFERENCE TABLES - Comprehensive Protecting Group Data
# ============================================================================

class StabilityLevel(Enum):
    UNSTABLE = "unstable"
    MODERATELY_STABLE = "moderately_stable"
    STABLE = "stable"
    VERY_STABLE = "very_stable"


@dataclass
class ProtectingGroup:
    """Data structure for protecting group information."""
    name: str
    abbreviation: str
    install_reagents: List[str]
    install_conditions: str
    deprotect_reagents: List[str]
    deprotect_conditions: str
    deprotect_temp: str
    deprotect_time: str
    stability: Dict[str, StabilityLevel]  # condition -> stability
    notes: str
    orthogonal_with: List[str]  # compatible PGs for orthogonal strategies


# ============================================================================
# ALCOHOL PROTECTING GROUPS (25+ groups)
# ============================================================================

ALCOHOL_PROTECTING_GROUPS: Dict[str, ProtectingGroup] = {
    # Silyl Ethers
    "TMS": ProtectingGroup(
        name="Trimethylsilyl",
        abbreviation="TMS",
        install_reagents=["TMSCl", "HMDS (hexamethyldisilazane)", "TMSOTf"],
        install_conditions="Base (imidazole, Et3N, pyridine), DMF or CH2Cl2, rt",
        deprotect_reagents=["TBAF", "AcOH/H2O", "HF-pyridine"],
        deprotect_conditions="TBAF in THF, or mild acid hydrolysis",
        deprotect_temp="0°C to rt",
        deprotect_time="0.5-2 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Most labile silyl ether; often removed during workup; not suitable for multi-step synthesis",
        orthogonal_with=["TBDPS", "TBS", "MOM", "THP", "Benzyl"]
    ),
    "TBS": ProtectingGroup(
        name="tert-Butyldimethylsilyl",
        abbreviation="TBS",
        install_reagents=["TBSCl", "TBSOTf"],
        install_conditions="Imidazole, DMF; or Et3N, DMAP, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine", "AcOH/H2O", "HF.MeCN"],
        deprotect_conditions="TBAF in THF (standard); or HF-pyridine for increased selectivity",
        deprotect_temp="rt to 50°C",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Most widely used silyl protecting group; good balance of stability and removability",
        orthogonal_with=["TBDPS", "TMS", "MOM", "THP", "Benzyl", "Ac", "Bz"]
    ),
    "TBDPS": ProtectingGroup(
        name="tert-Butyldiphenylsilyl",
        abbreviation="TBDPS",
        install_reagents=["TBDPSCl", "TBDPSOTf"],
        install_conditions="Imidazole, DMF; or pyridine, DMAP, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="TBAF in THF; more stable than TBS, requires harsher conditions",
        deprotect_temp="rt to 60°C",
        deprotect_time="2-24 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="More stable than TBS; can be orthogonal to TBS by selective deprotection; bulkier",
        orthogonal_with=["TBS", "TMS", "MOM", "THP", "Benzyl", "Ac", "Bz"]
    ),
    "TIPS": ProtectingGroup(
        name="Triisopropylsilyl",
        abbreviation="TIPS",
        install_reagents=["TIPSCl", "TIPSOTf"],
        install_conditions="Imidazole, DMF; or Et3N, DMAP, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="TBAF in THF; requires longer time than TBS",
        deprotect_temp="rt to 80°C",
        deprotect_time="6-48 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Highly stable silyl group; removed after TBS/TBDPS; useful for late-stage deprotection",
        orthogonal_with=["TBS", "TBDPS", "TMS", "MOM", "Benzyl"]
    ),
    "TES": ProtectingGroup(
        name="Triethylsilyl",
        abbreviation="TES",
        install_reagents=["TESCl", "TESOTf"],
        install_conditions="Imidazole, DMF; or pyridine, DMAP, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "AcOH/H2O", "HF-pyridine"],
        deprotect_conditions="TBAF in THF; more labile than TBS",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Intermediate stability between TMS and TBS; orthogonal to TBS in some cases",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "MOM", "Benzyl"]
    ),
    
    # Acetals and Ethers
    "MOM": ProtectingGroup(
        name="Methoxymethyl",
        abbreviation="MOM",
        install_reagents=["MOMCl", "MOMBr"],
        install_conditions="Diisopropylethylamine (DIPEA) or NaH, CH2Cl2 or THF, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA", "BCl3"],
        deprotect_conditions="Dilute acid (HCl in MeOH, AcOH/H2O, or TFA/H2O)",
        deprotect_temp="rt to reflux",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Acid-labile; stable to base; commonly used with silyl groups for orthogonality",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "Benzyl", "Ac", "Bz", "THP"]
    ),
    "MEM": ProtectingGroup(
        name="2-Methoxyethoxymethyl",
        abbreviation="MEM",
        install_reagents=["MEMCl"],
        install_conditions="DIPEA or NaH, CH2Cl2 or THF, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA", "TiCl4"],
        deprotect_conditions="Dilute acid or TiCl4 in CH2Cl2",
        deprotect_temp="rt to 50°C",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to MOM but slightly more stable; chelates with Lewis acids",
        orthogonal_with=["TBS", "TBDPS", "Benzyl", "Ac", "THP"]
    ),
    "THP": ProtectingGroup(
        name="Tetrahydropyranyl",
        abbreviation="THP",
        install_reagents=["DHP (dihydropyran)"],
        install_conditions="PPTS or CSA (cat.), CH2Cl2, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA", "PPTS"],
        deprotect_conditions="Dilute acid in MeOH or EtOH",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very easily installed and removed; too acid-labile for many applications; creates stereocenter",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "Benzyl", "Ac", "Bz"]
    ),
    "BOM": ProtectingGroup(
        name="Benzyloxymethyl",
        abbreviation="BOM",
        install_reagents=["BOMCl"],
        install_conditions="DIPEA or NaH, CH2Cl2 or THF, rt",
        deprotect_reagents=["H2, Pd/C", "HCl", "BCl3"],
        deprotect_conditions="Hydrogenolysis (H2, Pd/C) or acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="2-24 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Removed by hydrogenolysis or acid; orthogonal to silyl groups",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "Ac", "Bz", "MOM"]
    ),
    "PMB": ProtectingGroup(
        name="p-Methoxybenzyl",
        abbreviation="PMB",
        install_reagents=["PMBCl", "PMBBr"],
        install_conditions="NaH, THF; or Ag2O, CH2Cl2",
        deprotect_reagents=["DDQ", "CAN", "H2, Pd/C", "TFA"],
        deprotect_conditions="DDQ in CH2Cl2/H2O (oxidative); H2/Pd-C (reductive); or TFA",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-8 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Multiple deprotection methods; DDQ oxidation very selective; useful orthogonal group",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "Benzyl", "MOM", "Ac", "Bz"]
    ),
    "Benzyl": ProtectingGroup(
        name="Benzyl",
        abbreviation="Bn",
        install_reagents=["BnBr", "BnCl"],
        install_conditions="NaH, THF; or Ag2O, DMF; or NaOH, Bu4NHSO4 (phase transfer)",
        deprotect_reagents=["H2, Pd/C", "H2, Pd(OH)2", "Na, NH3", "BCl3"],
        deprotect_conditions="Hydrogenolysis (H2, Pd/C or Pd(OH)2); dissolving metal (Na/NH3); or BCl3",
        deprotect_temp="rt to reflux",
        deprotect_time="2-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very stable to acid/base; removed by hydrogenolysis; classic protecting group",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "TMS", "MOM", "THP", "Ac", "Bz", "PMB"]
    ),
    "Trityl": ProtectingGroup(
        name="Triphenylmethyl (Trityl)",
        abbreviation="Tr",
        install_reagents=["TrCl", "TrBr"],
        install_conditions="Pyridine or Et3N, CH2Cl2, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA", "H2, Pd/C"],
        deprotect_conditions="Mild acid (AcOH, TFA) or hydrogenolysis",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.MODERATELY_STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very bulky; highly acid-labile; selective for primary alcohols; steric hindrance",
        orthogonal_with=["TBS", "TBDPS", "Ac", "Bz", "Benzyl"]
    ),
    
    # Esters
    "Acetate": ProtectingGroup(
        name="Acetate",
        abbreviation="Ac",
        install_reagents=["Ac2O", "AcCl"],
        install_conditions="Pyridine, DMAP; or Et3N, CH2Cl2, rt",
        deprotect_reagents=["K2CO3/MeOH", "NaOH", "NH3/MeOH", "LiAlH4"],
        deprotect_conditions="Base hydrolysis (K2CO3/MeOH, NaOH/H2O) or reduction (LiAlH4)",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-8 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Base-labile; stable to acid; easily installed; can migrate under basic conditions",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "MOM", "THP", "Benzyl", "PMB"]
    ),
    "Benzoyl": ProtectingGroup(
        name="Benzoyl",
        abbreviation="Bz",
        install_reagents=["BzCl", "Bz2O"],
        install_conditions="Pyridine, DMAP; or Et3N, CH2Cl2, rt",
        deprotect_reagents=["K2CO3/MeOH", "NaOH", "NH3/MeOH", "LiAlH4"],
        deprotect_conditions="Base hydrolysis (slower than acetate) or reduction",
        deprotect_temp="rt to reflux",
        deprotect_time="2-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="More stable than acetate; aromatic ester; useful crystalline derivative",
        orthogonal_with=["TBS", "TBDPS", "TIPS", "MOM", "THP", "Benzyl", "PMB"]
    ),
    "Pivaloate": ProtectingGroup(
        name="Pivaloate",
        abbreviation="Piv",
        install_reagents=["PivCl", "Piv2O"],
        install_conditions="Pyridine, DMAP; or Et3N, CH2Cl2, rt",
        deprotect_reagents=["K2CO3/MeOH", "NaOH", "LiAlH4"],
        deprotect_conditions="Strong base or reduction; more hindered than acetate",
        deprotect_temp="reflux",
        deprotect_time="4-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Hindered ester; more stable to base than acetate; slower to hydrolyze",
        orthogonal_with=["TBS", "TBDPS", "MOM", "Benzyl"]
    ),
    
    # Carbonates
    "Troc": ProtectingGroup(
        name="2,2,2-Trichloroethoxycarbonyl",
        abbreviation="Troc",
        install_reagents=["TrocCl"],
        install_conditions="Pyridine, CH2Cl2, rt",
        deprotect_reagents=["Zn, AcOH", "Zn, NH4Cl", "electrochemical"],
        deprotect_conditions="Reductive cleavage with Zn/AcOH",
        deprotect_temp="rt",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Reductive deprotection; orthogonal to many groups; useful for carbohydrates",
        orthogonal_with=["TBS", "Benzyl", "MOM", "Ac", "Bz"]
    ),
    
    # Others
    "SEM": ProtectingGroup(
        name="2-(Trimethylsilyl)ethoxymethyl",
        abbreviation="SEM",
        install_reagents=["SEMCl"],
        install_conditions="DIPEA, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine", "MgBr2"],
        deprotect_conditions="Fluoride-mediated (TBAF) or Lewis acid (MgBr2)",
        deprotect_temp="rt to reflux",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Combines MOM and silyl features; removed with fluoride; very stable",
        orthogonal_with=["TBS", "TBDPS", "Benzyl", "Ac", "Bz"]
    ),
    "EE": ProtectingGroup(
        name="1-Ethoxyethyl",
        abbreviation="EE",
        install_reagents=["Ethyl vinyl ether"],
        install_conditions="PPTS, CH2Cl2, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA"],
        deprotect_conditions="Dilute acid",
        deprotect_temp="rt",
        deprotect_time="0.5-2 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very acid-labile; similar to THP; used for temporary protection",
        orthogonal_with=["TBS", "TBDPS", "Benzyl", "Ac"]
    ),
    "TBDMS": ProtectingGroup(  # Alias for TBS
        name="tert-Butyldimethylsilyl",
        abbreviation="TBDMS",
        install_reagents=["TBSCl", "TBSOTf"],
        install_conditions="Imidazole, DMF; or Et3N, DMAP, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="TBAF in THF",
        deprotect_temp="rt to 50°C",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Alias for TBS; widely used silyl protecting group",
        orthogonal_with=["TBDPS", "TMS", "MOM", "THP", "Benzyl", "Ac", "Bz"]
    ),
    "MTHP": ProtectingGroup(
        name="4-Methoxytetrahydropyranyl",
        abbreviation="MTHP",
        install_reagents=["4-Methoxydihydropyran"],
        install_conditions="PPTS or CSA, CH2Cl2, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA"],
        deprotect_conditions="Mild acid hydrolysis",
        deprotect_temp="rt",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to THP but slightly more stable; acid-labile",
        orthogonal_with=["TBS", "TBDPS", "Benzyl", "Ac", "Bz"]
    ),
    "DBDMS": ProtectingGroup(
        name="Dibutyldimethylsilyl",
        abbreviation="DBDMS",
        install_reagents=["DBDMSCl"],
        install_conditions="Imidazole, DMF, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="Fluoride source",
        deprotect_temp="rt to 50°C",
        deprotect_time="2-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Less common; intermediate properties",
        orthogonal_with=["MOM", "Benzyl", "Ac"]
    ),
}


# ============================================================================
# AMINE PROTECTING GROUPS (25+ groups)
# ============================================================================

AMINE_PROTECTING_GROUPS: Dict[str, ProtectingGroup] = {
    # Carbamates
    "Boc": ProtectingGroup(
        name="tert-Butyloxycarbonyl",
        abbreviation="Boc",
        install_reagents=["(Boc)2O", "Boc-ON", "Boc2O/DMAP"],
        install_conditions="Base (Et3N, DMAP), CH2Cl2 or dioxane, rt; or NaOH/H2O for amines",
        deprotect_reagents=["TFA", "HCl in dioxane", "HCl in EtOAc"],
        deprotect_conditions="Strong acid (TFA neat or in CH2Cl2; HCl in organic solvent)",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Most common amine PG; acid-labile; stable to base, hydrogenolysis; orthogonal with Cbz, Fmoc",
        orthogonal_with=["Cbz", "Fmoc", "Alloc", "Benzyl", "Ac", "TFA"]
    ),
    "Cbz": ProtectingGroup(
        name="Benzyloxycarbonyl",
        abbreviation="Cbz",
        install_reagents=["Cbz-Cl (benzyl chloroformate)"],
        install_conditions="NaOH or NaHCO3, H2O/dioxane; or Et3N, CH2Cl2, 0°C to rt",
        deprotect_reagents=["H2, Pd/C", "HBr/AcOH", "BBr3"],
        deprotect_conditions="Hydrogenolysis (H2, Pd/C) or HBr in AcOH",
        deprotect_temp="rt",
        deprotect_time="2-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Classical amine PG; removed by hydrogenolysis; orthogonal with Boc; also called Z",
        orthogonal_with=["Boc", "Fmoc", "Alloc", "Ac", "TFA"]
    ),
    "Fmoc": ProtectingGroup(
        name="9-Fluorenylmethyloxycarbonyl",
        abbreviation="Fmoc",
        install_reagents=["Fmoc-Cl", "Fmoc-OSu"],
        install_conditions="NaHCO3 or NaOH, dioxane/H2O; or Et3N, CH2Cl2, rt",
        deprotect_reagents=["Piperidine", "DBU", "Morpholine"],
        deprotect_conditions="Base (piperidine 20% in DMF; or DBU in CH2Cl2)",
        deprotect_temp="rt",
        deprotect_time="5-30 min",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Base-labile; widely used in solid-phase peptide synthesis; orthogonal with Boc, Cbz",
        orthogonal_with=["Boc", "Cbz", "Alloc", "Benzyl", "Ac"]
    ),
    "Alloc": ProtectingGroup(
        name="Allyloxycarbonyl",
        abbreviation="Alloc",
        install_reagents=["Alloc-Cl", "Alloc-OC6F5"],
        install_conditions="Base (NaHCO3, Et3N), CH2Cl2, 0°C to rt",
        deprotect_reagents=["Pd(0) catalyst", "PhSiH3", "Me2NTMS"],
        deprotect_conditions="Pd(PPh3)4 with nucleophile (morpholine, dimedone, PhSiH3)",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.MODERATELY_STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Removed by Pd(0); orthogonal with Boc, Cbz, Fmoc; useful for complex synthesis",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac", "TFA"]
    ),
    "Trocarb": ProtectingGroup(
        name="2,2,2-Trichloroethyloxycarbonyl",
        abbreviation="Troc",
        install_reagents=["Troc-Cl"],
        install_conditions="Base (pyridine, Et3N), CH2Cl2, 0°C to rt",
        deprotect_reagents=["Zn, AcOH", "Zn, NH4Cl"],
        deprotect_conditions="Reductive with Zn",
        deprotect_temp="rt",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Reductive deprotection; orthogonal with most carbamates",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac"]
    ),
    "Teoc": ProtectingGroup(
        name="2-(Trimethylsilyl)ethyloxycarbonyl",
        abbreviation="Teoc",
        install_reagents=["Teoc-Cl", "Teoc-OSu"],
        install_conditions="Base, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="Fluoride source (TBAF)",
        deprotect_temp="rt to 50°C",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Fluoride-labile; orthogonal with Boc, Cbz, Fmoc",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac", "TFA"]
    ),
    "Nsc": ProtectingGroup(
        name="2-(4-Nitrophenylsulfonyl)ethyloxycarbonyl",
        abbreviation="Nsc",
        install_reagents=["Nsc-Cl"],
        install_conditions="Base, CH2Cl2, rt",
        deprotect_reagents=["Base (DBU, piperidine)"],
        deprotect_conditions="Mild base (similar to Fmoc)",
        deprotect_temp="rt",
        deprotect_time="10-60 min",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to Fmoc; base-labile; alternative for SPPS",
        orthogonal_with=["Boc", "Cbz", "Alloc", "Ac"]
    ),
    "Poc": ProtectingGroup(
        name="Propargyloxycarbonyl",
        abbreviation="Poc",
        install_reagents=["Poc-Cl"],
        install_conditions="Base, CH2Cl2, rt",
        deprotect_reagents=["Pd(0)", "Cp2TiCl"],
        deprotect_conditions="Transition metal mediated",
        deprotect_temp="rt to 60°C",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Removed by Pd or Ti; orthogonal with standard carbamates",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac"]
    ),
    
    # Amides
    "Acetyl": ProtectingGroup(
        name="Acetyl",
        abbreviation="Ac",
        install_reagents=["Ac2O", "AcCl"],
        install_conditions="Pyridine or Et3N, CH2Cl2, rt; or Ac2O neat, reflux",
        deprotect_reagents=["HCl, H2O", "KOH/MeOH", "NH2NH2"],
        deprotect_conditions="Acid or base hydrolysis; hydrazine",
        deprotect_temp="reflux",
        deprotect_time="2-12 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Simple amide; requires harsh conditions for removal; not commonly used for amines",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Benzyl"]
    ),
    "TFA": ProtectingGroup(
        name="Trifluoroacetyl",
        abbreviation="TFA",
        install_reagents=["TFAA", "TFA-ester"],
        install_conditions="Base (pyridine, Et3N), CH2Cl2, 0°C to rt",
        deprotect_reagents=["K2CO3/MeOH", "NaOH", "NH3"],
        deprotect_conditions="Mild base hydrolysis (K2CO3/MeOH)",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Electron-withdrawing; base-labile; easier to remove than acetyl",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Benzyl"]
    ),
    "Phthalimide": ProtectingGroup(
        name="Phthalimide",
        abbreviation="Phth",
        install_reagents=["Phthalic anhydride", "N-(Ethoxycarbonyl)phthalimide"],
        install_conditions="Heat (150-200°C); or DMF, rt; or Mitsunobu conditions",
        deprotect_reagents=["NH2NH2", "MeNH2", "HCl, AcOH"],
        deprotect_conditions="Hydrazine (NH2NH2) in EtOH; or HCl in AcOH",
        deprotect_temp="rt to reflux",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Classic Gabriel synthesis; removed by hydrazine; stable to many conditions",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac"]
    ),
    "Benzoyl": ProtectingGroup(
        name="Benzoyl",
        abbreviation="Bz",
        install_reagents=["BzCl"],
        install_conditions="Pyridine, CH2Cl2, rt",
        deprotect_reagents=["NaOH", "HCl, reflux"],
        deprotect_conditions="Strong base or acid hydrolysis",
        deprotect_temp="reflux",
        deprotect_time="4-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Aromatic amide; requires harsh conditions; not commonly used",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Benzyl"]
    ),
    "Phtaloyl": ProtectingGroup(  # Alias
        name="Phthaloyl",
        abbreviation="Pht",
        install_reagents=["Phthalic anhydride"],
        install_conditions="Heat or solvent, rt",
        deprotect_reagents=["NH2NH2"],
        deprotect_conditions="Hydrazine",
        deprotect_temp="rt to reflux",
        deprotect_time="2-8 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Same as Phthalimide; Gabriel synthesis protecting group",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac"]
    ),
    
    # Sulfonamides
    "Ns": ProtectingGroup(
        name="2-Nitrobenzenesulfonyl",
        abbreviation="Ns",
        install_reagents=["NsCl (o-nitrobenzenesulfonyl chloride)"],
        install_conditions="Base (pyridine, Et3N), CH2Cl2, rt",
        deprotect_reagents=["PhSH, K2CO3", "HSCH2COOH", "SmI2"],
        deprotect_conditions="Thiolate (PhSK, HSCH2COOH/K2CO3) or SmI2",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Removable under mild conditions; orthogonal with carbamates; Fukuyama amine synthesis",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac", "TFA"]
    ),
    "Ts": ProtectingGroup(
        name="p-Toluenesulfonyl (Tosyl)",
        abbreviation="Ts",
        install_reagents=["TsCl"],
        install_conditions="Base (pyridine, NaOH), CH2Cl2 or H2O, rt",
        deprotect_reagents=["Na, NH3", "HBr, AcOH", "Mg, MeOH"],
        deprotect_conditions="Dissolving metal (Na/NH3); or HBr in AcOH; or Mg in MeOH",
        deprotect_temp="-78°C to reflux",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very stable; difficult to remove; classic group for amine protection",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac"]
    ),
    
    # Alkyl groups
    "Benzyl_amine": ProtectingGroup(
        name="Benzyl (for amines)",
        abbreviation="Bn",
        install_reagents=["BnBr", "BnCl", "PhCHO/NaBH4"],
        install_conditions="Base (NaH, K2CO3), THF or DMF; or reductive amination",
        deprotect_reagents=["H2, Pd/C", "H2, Pd(OH)2", "Na, NH3"],
        deprotect_conditions="Hydrogenolysis (H2, Pd/C) or dissolving metal (Na/NH3)",
        deprotect_temp="rt to reflux",
        deprotect_time="4-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Stable to acid/base; removed by hydrogenolysis; common for secondary amines",
        orthogonal_with=["Boc", "Fmoc", "Ac", "TFA", "Cbz"]
    ),
    "Trityl_amine": ProtectingGroup(
        name="Triphenylmethyl (Trityl, for amines)",
        abbreviation="Tr",
        install_reagents=["TrCl"],
        install_conditions="Et3N, CH2Cl2, rt",
        deprotect_reagents=["HCl", "AcOH", "TFA"],
        deprotect_conditions="Mild acid (AcOH, TFA)",
        deprotect_temp="rt",
        deprotect_time="0.5-2 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.MODERATELY_STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very acid-labile; bulky; selective for primary amines",
        orthogonal_with=["Cbz", "Ac", "TFA", "Ts"]
    ),
    "PMB_amine": ProtectingGroup(
        name="p-Methoxybenzyl (for amines)",
        abbreviation="PMB",
        install_reagents=["PMBCl", "PMBBr", "p-anisaldehyde/NaBH4"],
        install_conditions="Base or reductive amination",
        deprotect_reagents=["TFA", "CAN", "H2, Pd/C", "DDQ"],
        deprotect_conditions="Acid (TFA), oxidation (CAN, DDQ), or hydrogenolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Multiple deprotection options; orthogonal with many groups",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac", "TFA"]
    ),
    "Dde": ProtectingGroup(
        name="1-(4,4-Dimethyl-2,6-dioxocyclohexylidene)ethyl",
        abbreviation="Dde",
        install_reagents=["Dde-OH", "Dde-OSu"],
        install_conditions="Standard acylation conditions",
        deprotect_reagents=["NH2NH2", "NH2NH2·AcOH"],
        deprotect_conditions="Hydrazine in EtOH or DMF",
        deprotect_temp="rt",
        deprotect_time="5-30 min",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Hydrazine-labile; orthogonal with Boc, Fmoc, Alloc; useful in peptide synthesis",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Alloc", "Ac"]
    ),
    "Nvoc": ProtectingGroup(
        name="6-Nitroveratryloxycarbonyl",
        abbreviation="NVoc",
        install_reagents=["NVoc-Cl"],
        install_conditions="Base, CH2Cl2, rt",
        deprotect_reagents=["hv (photolysis)"],
        deprotect_conditions="UV light (λ ~ 350 nm)",
        deprotect_temp="rt",
        deprotect_time="5-60 min",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Photolabile; orthogonal with almost all other PGs; used in photolithography",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Alloc", "Ac", "TFA"]
    ),
    "Dmb": ProtectingGroup(
        name="2,4-Dimethoxybenzyl",
        abbreviation="Dmb",
        install_reagents=["DMB-Cl", "2,4-dimethoxybenzaldehyde/NaBH4"],
        install_conditions="Reductive amination or alkylation",
        deprotect_reagents=["TFA", "CAN"],
        deprotect_conditions="Mild acid (TFA) or oxidation (CAN)",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Acid-labile benzyl-type PG; more labile than PMB",
        orthogonal_with=["Boc", "Cbz", "Fmoc", "Ac", "TFA"]
    ),
    "Sulfonamide_Ethyl": ProtectingGroup(
        name="N-Ethylsulfonamide",
        abbreviation="EtSO2",
        install_reagents=["EtSO2Cl"],
        install_conditions="Base, CH2Cl2, rt",
        deprotect_reagents=["Strong base", "reducing conditions"],
        deprotect_conditions="Very difficult to remove",
        deprotect_temp="reflux",
        deprotect_time="12-24 h",
        stability={"strong_acid": StabilityLevel.VERY_STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very stable; rarely used due to removal difficulty",
        orthogonal_with=["Boc", "Fmoc"]
    ),
}


# ============================================================================
# CARBONYL PROTECTING GROUPS (20+ groups)
# ============================================================================

CARBONYL_PROTECTING_GROUPS: Dict[str, ProtectingGroup] = {
    # Acetals (for aldehydes/ketones)
    "Acetal": ProtectingGroup(
        name="Dimethyl Acetal",
        abbreviation="OMe acetal",
        install_reagents=["MeOH", "HC(OMe)3"],
        install_conditions="Acid catalyst (TsOH, PPTS), MeOH; or trimethyl orthoformate, acid",
        deprotect_reagents=["HCl, H2O", "AcOH, H2O", "TFA, H2O"],
        deprotect_conditions="Dilute acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Common for aldehydes; stable to base; acid-labile",
        orthogonal_with=["TBS", "THP", "MOM", "Benzyl"]
    ),
    "Dioxolane": ProtectingGroup(
        name="1,3-Dioxolane",
        abbreviation="Ethylene acetal",
        install_reagents=["Ethylene glycol", "HC(OMe)3"],
        install_conditions="TsOH or PPTS, benzene or toluene, Dean-Stark; or (TMS)2O, TMSOTf",
        deprotect_reagents=["HCl, H2O", "AcOH, H2O", "TFA, H2O", "PPTS, acetone/H2O"],
        deprotect_conditions="Acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Most common carbonyl PG; for aldehydes and ketones; stable to base, reducing agents",
        orthogonal_with=["TBS", "THP", "MOM", "Benzyl", "Ac"]
    ),
    "Dithiane": ProtectingGroup(
        name="1,3-Dithiane",
        abbreviation="Dithiane",
        install_reagents=["1,3-Propanedithiol"],
        install_conditions="BF3·Et2O or other Lewis acid, CH2Cl2, rt",
        deprotect_reagents=["HgO, BF3·Et2O", "NBS, H2O", "I2, MeOH", "Raney Ni"],
        deprotect_conditions="Hg(II) salts; NBS; I2; or Raney Ni desulfurization",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-8 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Umpolung chemistry; stable to strong base; used in alkylation reactions",
        orthogonal_with=["TBS", "MOM", "Benzyl", "Ac", "THP"]
    ),
    "Oxathiane": ProtectingGroup(
        name="1,3-Oxathiane",
        abbreviation="Oxathiane",
        install_reagents=["3-Mercapto-1-propanol"],
        install_conditions="Lewis acid, CH2Cl2, rt",
        deprotect_reagents=["NBS, H2O", "I2, MeOH", "Hg(II)"],
        deprotect_conditions="Electrophilic reagents (NBS, I2)",
        deprotect_temp="rt to reflux",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to dithiane but mixed O,S; umpolung",
        orthogonal_with=["TBS", "MOM", "Benzyl"]
    ),
    "Dioxane": ProtectingGroup(
        name="1,3-Dioxane",
        abbreviation="Dioxane",
        install_reagents=["1,3-Propanediol"],
        install_conditions="TsOH, benzene, Dean-Stark",
        deprotect_reagents=["HCl, H2O", "AcOH, H2O"],
        deprotect_conditions="Acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Six-membered ring acetal; less strained than dioxolane",
        orthogonal_with=["TBS", "MOM", "Benzyl", "Ac"]
    ),
    "Dithiolane": ProtectingGroup(
        name="1,2-Dithiolane",
        abbreviation="Dithiolane",
        install_reagents=["1,2-Ethanedithiol"],
        install_conditions="Lewis acid (BF3·Et2O), CH2Cl2, rt",
        deprotect_reagents=["HgO, BF3·Et2O", "NBS, H2O", "Raney Ni"],
        deprotect_conditions="Hg(II) or oxidative cleavage",
        deprotect_temp="rt to reflux",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Five-membered cyclic dithioacetal; umpolung chemistry",
        orthogonal_with=["TBS", "MOM", "Benzyl", "Ac"]
    ),
    
    # Mixed acetals
    "MOM_carbonyl": ProtectingGroup(
        name="Methoxymethyl hemiacetal",
        abbreviation="MOM acetal",
        install_reagents=["MOMCl"],
        install_conditions="DIPEA, CH2Cl2, rt",
        deprotect_reagents=["HCl, H2O", "AcOH, H2O"],
        deprotect_conditions="Dilute acid",
        deprotect_temp="rt to reflux",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Less common for carbonyls; more labile than cyclic acetals",
        orthogonal_with=["TBS", "Benzyl"]
    ),
    "MEM_carbonyl": ProtectingGroup(
        name="2-Methoxyethoxymethyl acetal",
        abbreviation="MEM acetal",
        install_reagents=["MEMCl"],
        install_conditions="DIPEA, CH2Cl2, rt",
        deprotect_reagents=["HCl, H2O", "TiCl4"],
        deprotect_conditions="Acid or Lewis acid",
        deprotect_temp="rt to reflux",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to MOM but slightly more stable",
        orthogonal_with=["TBS", "Benzyl"]
    ),
    
    # Hydrazones and derivatives
    "Dimethylhydrazone": ProtectingGroup(
        name="N,N-Dimethylhydrazone",
        abbreviation="DMH",
        install_reagents=["1,1-Dimethylhydrazine"],
        install_conditions="Molecular sieves, CH2Cl2 or EtOH, rt",
        deprotect_reagents=["HCl, H2O", "Oxalic acid", "CuCl2"],
        deprotect_conditions="Mild acid hydrolysis; or Cu(II) oxidation",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.MODERATELY_STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Stable to base and many organometallics; used for alkylation",
        orthogonal_with=["TBS", "MOM", "Benzyl", "Ac"]
    ),
    "Phenylhydrazone": ProtectingGroup(
        name="Phenylhydrazone",
        abbreviation="PhNHNH",
        install_reagents=["Phenylhydrazine"],
        install_conditions="AcOH cat., EtOH, rt",
        deprotect_reagents=["AcOH, H2O", "O2", "NaNO2/H+"],
        deprotect_conditions="Acid hydrolysis or oxidation",
        deprotect_temp="rt to reflux",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to other hydrazones; useful in Fischer indole synthesis",
        orthogonal_with=["TBS", "MOM", "Benzyl"]
    ),
    "Semicarbazone": ProtectingGroup(
        name="Semicarbazone",
        abbreviation="Semicarbazone",
        install_reagents=["Semicarbazide"],
        install_conditions="AcOH buffer, EtOH/H2O, rt",
        deprotect_reagents=["HCl, H2O", "oxalic acid", "formic acid"],
        deprotect_conditions="Acid hydrolysis",
        deprotect_temp="reflux",
        deprotect_time="2-8 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.MODERATELY_STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Common for crystallization; moderate stability",
        orthogonal_with=["TBS", "MOM", "Benzyl"]
    ),
    "Oxime": ProtectingGroup(
        name="Oxime",
        abbreviation="Oxime",
        install_reagents=["NH2OH"],
        install_conditions="Pyridine or NaOAc, EtOH, rt",
        deprotect_reagents=["HCl, H2O", "TiCl3", "NaHSO3"],
        deprotect_conditions="Acid hydrolysis or reduction",
        deprotect_temp="rt to reflux",
        deprotect_time="2-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Stable; used for purification; can be reduced to primary amines",
        orthogonal_with=["TBS", "MOM", "Benzyl", "Ac"]
    ),
    
    # Enol ethers (for ketones)
    "Enol_ether": ProtectingGroup(
        name="Enol Ether",
        abbreviation="Enol ether",
        install_reagents=["R'OH", "NaH", "TMSOTf"],
        install_conditions="Base or thermal enolization; TMSOTf, Et3N",
        deprotect_reagents=["HCl, H2O", "F-"],
        deprotect_conditions="Acidic hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.MODERATELY_STABLE},
        notes="Labile; reactive intermediates; used in Michael additions",
        orthogonal_with=["Benzyl", "TBS"]
    ),
    "Silyl_enol_ether": ProtectingGroup(
        name="Silyl Enol Ether",
        abbreviation="TMS enol ether",
        install_reagents=["TMSCl", "TMSOTf"],
        install_conditions="Et3N; or LDA, then TMSCl",
        deprotect_reagents=["H2O", "F-", "AcOH"],
        deprotect_conditions="Mild acid or fluoride",
        deprotect_temp="rt",
        deprotect_time="0.1-1 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Very labile; reactive intermediate in aldol, Michael reactions",
        orthogonal_with=["Benzyl"]
    ),
    
    # Cyclic ketals with substitution
    "Tetramethyldioxolane": ProtectingGroup(
        name="4,4,5,5-Tetramethyl-1,3-dioxolane",
        abbreviation="TMD",
        install_reagents=["Pinacol"],
        install_conditions="TsOH, benzene, Dean-Stark",
        deprotect_reagents=["HCl, H2O", "AcOH, H2O"],
        deprotect_conditions="Acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="More stable than dioxolane due to gem-dimethyl groups",
        orthogonal_with=["TBS", "MOM", "Benzyl"]
    ),
    
    # Thioketals
    "Thioketal": ProtectingGroup(
        name="Thioketal",
        abbreviation="Thioketal",
        install_reagents=["1,2-Ethanedithiol", "1,3-Propanedithiol"],
        install_conditions="BF3·Et2O, CH2Cl2, rt",
        deprotect_reagents=["HgO, HgCl2", "NBS, H2O", "Raney Ni", "I2, MeOH"],
        deprotect_conditions="Hg(II), NBS, I2, or Raney Ni",
        deprotect_temp="rt to reflux",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Very stable to base and acid; oxidatively labile; umpolung chemistry",
        orthogonal_with=["TBS", "MOM", "Benzyl", "Ac"]
    ),
    
    # Ketal diastereomers
    "Diethyl_ketal": ProtectingGroup(
        name="Diethyl Ketal",
        abbreviation="Diethyl ketal",
        install_reagents=["EtOH", "HC(OEt)3"],
        install_conditions="Acid catalyst, EtOH; or triethyl orthoformate",
        deprotect_reagents=["HCl, H2O", "AcOH, H2O"],
        deprotect_conditions="Dilute acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Acyclic ketal; more labile than cyclic",
        orthogonal_with=["TBS", "MOM", "Benzyl"]
    ),
    
    # Others
    "Bisulfite_adduct": ProtectingGroup(
        name="Bisulfite Adduct",
        abbreviation="HSO3 adduct",
        install_reagents=["NaHSO3"],
        install_conditions="NaHSO3, H2O, rt",
        deprotect_reagents=["Base", "heat"],
        deprotect_conditions="Base or heating",
        deprotect_temp="rt to reflux",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Water-soluble; used for purification of aldehydes",
        orthogonal_with=["TBS", "MOM", "Benzyl"]
    ),
    "TOSMIC_derived": ProtectingGroup(
        name="TOSMIC-derived",
        abbreviation="TosMIC imine",
        install_reagents=["TosMIC"],
        install_conditions="Base, MeOH, rt",
        deprotect_reagents=["HCl, H2O"],
        deprotect_conditions="Acid hydrolysis",
        deprotect_temp="rt to reflux",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Used in Van Leusen reaction",
        orthogonal_with=["TBS", "Benzyl"]
    ),
}


# ============================================================================
# CARBOXYLIC ACID PROTECTING GROUPS (25+ groups)
# ============================================================================

CARBOXYLIC_ACID_PROTECTING_GROUPS: Dict[str, ProtectingGroup] = {
    # Simple esters
    "Methyl_ester": ProtectingGroup(
        name="Methyl Ester",
        abbreviation="Me ester",
        install_reagents=["CH2N2", "MeI", "MeOH/H+"],
        install_conditions="Diazomethane in Et2O; or MeI/K2CO3, DMF; or MeOH, H+ (Fischer)",
        deprotect_reagents=["NaOH", "LiOH", "KOH", "TMSI", "BBr3"],
        deprotect_conditions="Base hydrolysis (NaOH/H2O); or BBr3 in CH2Cl2",
        deprotect_temp="rt to reflux",
        deprotect_time="1-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Most common ester PG; easily hydrolyzed with base; CH2N2 toxic but fast",
        orthogonal_with=["TBS", "Benzyl", "THP", "MOM", "Boc"]
    ),
    "Ethyl_ester": ProtectingGroup(
        name="Ethyl Ester",
        abbreviation="Et ester",
        install_reagents=["EtOH/H+", "EtI", "DCC, EtOH"],
        install_conditions="Fischer esterification (EtOH, H+); or EtI, K2CO3, DMF",
        deprotect_reagents=["NaOH", "LiOH", "KOH"],
        deprotect_conditions="Base hydrolysis",
        deprotect_temp="reflux",
        deprotect_time="2-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to methyl ester; slightly more hindered",
        orthogonal_with=["TBS", "Benzyl", "THP", "MOM", "Boc"]
    ),
    "Propyl_ester": ProtectingGroup(
        name="Propyl Ester",
        abbreviation="Pr ester",
        install_reagents=["PrOH/H+"],
        install_conditions="Fischer esterification",
        deprotect_reagents=["NaOH", "LiOH"],
        deprotect_conditions="Base hydrolysis",
        deprotect_temp="reflux",
        deprotect_time="4-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Similar to methyl/ethyl",
        orthogonal_with=["TBS", "Benzyl", "Boc"]
    ),
    
    # Benzyl esters
    "Benzyl_ester": ProtectingGroup(
        name="Benzyl Ester",
        abbreviation="Bn ester",
        install_reagents=["BnBr", "BnOH/DCC", "PhCHN2"],
        install_conditions="K2CO3, DMF; or DCC, BnOH; or PhCHN2",
        deprotect_reagents=["H2, Pd/C", "H2, Pd(OH)2", "Na, NH3", "HBr, AcOH"],
        deprotect_conditions="Hydrogenolysis (H2, Pd/C); or dissolving metal",
        deprotect_temp="rt to reflux",
        deprotect_time="2-24 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Removed by hydrogenolysis; stable to base; orthogonal with methyl ester",
        orthogonal_with=["Methyl_ester", "TBS", "MOM", "Boc", "Cbz"]
    ),
    "PMB_ester": ProtectingGroup(
        name="p-Methoxybenzyl Ester",
        abbreviation="PMB ester",
        install_reagents=["PMBCl", "PMBBr"],
        install_conditions="K2CO3, DMF; or DCC, PMBOH",
        deprotect_reagents=["H2, Pd/C", "TFA", "DDQ", "CAN"],
        deprotect_conditions="Hydrogenolysis; or oxidation (DDQ, CAN); or acid (TFA)",
        deprotect_temp="rt to reflux",
        deprotect_time="1-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.UNSTABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Multiple deprotection options; can be removed selectively vs benzyl",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "TBS", "Boc"]
    ),
    
    # tert-Butyl esters
    "tButyl_ester": ProtectingGroup(
        name="tert-Butyl Ester",
        abbreviation="t-Bu ester",
        install_reagents=["Isobutylene", "Boc2O", "t-BuOH/DCC"],
        install_conditions="Isobutylene, H2SO4; or Boc2O, DMAP, CH2Cl2",
        deprotect_reagents=["TFA", "HCl in dioxane", "HCOOH"],
        deprotect_conditions="Strong acid (TFA, HCl in organic solvent)",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.VERY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Acid-labile; stable to base and hydrogenolysis; orthogonal with methyl, benzyl",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "TBS", "Cbz", "Benzyl"]
    ),
    
    # Allyl ester
    "Allyl_ester": ProtectingGroup(
        name="Allyl Ester",
        abbreviation="Allyl ester",
        install_reagents=["Allyl bromide", "Allyl alcohol/DCC"],
        install_conditions="K2CO3, DMF; or DCC, allyl alcohol",
        deprotect_reagents=["Pd(0)", "Pd(PPh3)4", "Pd(PPh3)2Cl2"],
        deprotect_conditions="Pd(0) with nucleophile (morpholine, dimedone, PhSiH3)",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.MODERATELY_STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Pd(0)-labile; orthogonal with Boc, methyl, benzyl; used in peptide synthesis",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "TBS", "Boc"]
    ),
    
    # Silyl esters
    "TMS_ester": ProtectingGroup(
        name="Trimethylsilyl Ester",
        abbreviation="TMS ester",
        install_reagents=["TMSCl", "TMSOTf", "HMDS"],
        install_conditions="Base (Et3N, pyridine), CH2Cl2, rt",
        deprotect_reagents=["H2O", "MeOH", "AcOH", "TBAF"],
        deprotect_conditions="Aqueous workup; very labile",
        deprotect_temp="rt",
        deprotect_time="minutes",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.UNSTABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Very labile; used for temporary protection; often removed during workup",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "TBS"]
    ),
    "TBS_ester": ProtectingGroup(
        name="tert-Butyldimethylsilyl Ester",
        abbreviation="TBS ester",
        install_reagents=["TBSCl", "TBSOTf"],
        install_conditions="Imidazole or Et3N, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "AcOH/H2O", "KF"],
        deprotect_conditions="Fluoride (TBAF) or mild acid",
        deprotect_temp="rt",
        deprotect_time="0.5-4 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.MODERATELY_STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="More stable than TMS; orthogonal with methyl, benzyl, t-butyl esters",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Boc"]
    ),
    
    # 2,2,2-Trichloroethyl ester
    "Troc_ester": ProtectingGroup(
        name="2,2,2-Trichloroethyl Ester",
        abbreviation="Troc ester",
        install_reagents=["TrocOH/DCC", "TrocCl"],
        install_conditions="DCC, TrocOH; or base, TrocCl",
        deprotect_reagents=["Zn, AcOH", "Zn, NH4Cl"],
        deprotect_conditions="Reductive cleavage with Zn",
        deprotect_temp="rt",
        deprotect_time="0.5-2 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Zn-labile; orthogonal with most other esters",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Allyl_ester", "Boc"]
    ),
    
    # 2-Trimethylsilylethyl ester
    "TMSE_ester": ProtectingGroup(
        name="2-Trimethylsilylethyl Ester",
        abbreviation="TMSE ester",
        install_reagents=["TMSEOH/DCC"],
        install_conditions="DCC, TMSEOH, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="Fluoride source",
        deprotect_temp="rt",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="Fluoride-labile; orthogonal with methyl, benzyl, t-butyl",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Boc"]
    ),
    
    # Phenacyl ester
    "Phenacyl_ester": ProtectingGroup(
        name="Phenacyl Ester",
        abbreviation="Phenacyl ester",
        install_reagents=["Phenacyl bromide"],
        install_conditions="K2CO3, DMF, rt",
        deprotect_reagents=["Zn, AcOH", "hv", "Na, NH3"],
        deprotect_conditions="Reductive (Zn) or photolytic",
        deprotect_temp="rt",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.MODERATELY_STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Photolabile or Zn-labile; orthogonal with standard esters",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Boc"]
    ),
    
    # p-Nitrobenzyl ester
    "PNB_ester": ProtectingGroup(
        name="p-Nitrobenzyl Ester",
        abbreviation="PNB ester",
        install_reagents=["p-Nitrobenzyl bromide"],
        install_conditions="K2CO3, DMF, rt",
        deprotect_reagents=["H2, Pd/C", "Zn, AcOH", "hv"],
        deprotect_conditions="Hydrogenolysis; reduction; or photolysis",
        deprotect_temp="rt",
        deprotect_time="1-8 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Removed by hydrogenolysis; faster than benzyl",
        orthogonal_with=["Methyl_ester", "tButyl_ester", "TBS", "Boc"]
    ),
    
    # Diphenylmethyl ester
    "DPM_ester": ProtectingGroup(
        name="Diphenylmethyl Ester",
        abbreviation="DPM ester",
        install_reagents=["DPMBr", "DPMCl"],
        install_conditions="Base, DMF or CH2Cl2, rt",
        deprotect_reagents=["H2, Pd/C", "TFA", "AcOH"],
        deprotect_conditions="Hydrogenolysis or mild acid",
        deprotect_temp="rt",
        deprotect_time="1-6 h",
        stability={"strong_acid": StabilityLevel.UNSTABLE, "weak_acid": StabilityLevel.MODERATELY_STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Acid-labile; removed by hydrogenolysis",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "TBS"]
    ),
    
    # Triisopropylsilyl ester
    "TIPS_ester": ProtectingGroup(
        name="Triisopropylsilyl Ester",
        abbreviation="TIPS ester",
        install_reagents=["TIPSCl", "TIPSOTf"],
        install_conditions="Et3N or imidazole, CH2Cl2, rt",
        deprotect_reagents=["TBAF", "HF-pyridine"],
        deprotect_conditions="Fluoride source",
        deprotect_temp="rt to 60°C",
        deprotect_time="2-12 h",
        stability={"strong_acid": StabilityLevel.MODERATELY_STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.UNSTABLE},
        notes="More stable than TBS ester; orthogonal with methyl, benzyl, t-butyl",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Boc"]
    ),
    
    # 9-Fluorenylmethyl ester
    "Fm_ester": ProtectingGroup(
        name="9-Fluorenylmethyl Ester",
        abbreviation="Fm ester",
        install_reagents=["Fm-Cl", "Fm-OSu"],
        install_conditions="Base (NaHCO3), dioxane/H2O",
        deprotect_reagents=["Piperidine", "DBU", "NH3"],
        deprotect_conditions="Base (piperidine 20% in DMF)",
        deprotect_temp="rt",
        deprotect_time="10-60 min",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.UNSTABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Base-labile; used in solid-phase synthesis; orthogonal with Boc",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Boc"]
    ),
    
    # Ortho-nitrobenzyl ester
    "ONB_ester": ProtectingGroup(
        name="o-Nitrobenzyl Ester",
        abbreviation="o-NB ester",
        install_reagents=["o-Nitrobenzyl bromide"],
        install_conditions="K2CO3, DMF, rt",
        deprotect_reagents=["hv (photolysis)"],
        deprotect_conditions="UV light",
        deprotect_temp="rt",
        deprotect_time="5-60 min",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.MODERATELY_STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.MODERATELY_STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Photolabile; orthogonal with most other protecting groups",
        orthogonal_with=["Methyl_ester", "Benzyl_ester", "tButyl_ester", "Boc", "TBS"]
    ),
    
    # Additional esters
    "Isopropyl_ester": ProtectingGroup(
        name="Isopropyl Ester",
        abbreviation="i-Pr ester",
        install_reagents=["i-PrOH/H+", "i-PrI"],
        install_conditions="Fischer esterification or alkylation",
        deprotect_reagents=["NaOH", "LiOH"],
        deprotect_conditions="Base hydrolysis; slower than methyl due to steric hindrance",
        deprotect_temp="reflux",
        deprotect_time="6-48 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="More hindered than methyl; slower hydrolysis",
        orthogonal_with=["TBS", "Benzyl", "Boc"]
    ),
    "Cyclohexyl_ester": ProtectingGroup(
        name="Cyclohexyl Ester",
        abbreviation="Cy ester",
        install_reagents=["CyOH/H+", "CyI"],
        install_conditions="Fischer esterification",
        deprotect_reagents=["NaOH", "LiOH"],
        deprotect_conditions="Base hydrolysis; hindered",
        deprotect_temp="reflux",
        deprotect_time="12-48 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.VERY_STABLE,
                   "base": StabilityLevel.MODERATELY_STABLE, "reducing": StabilityLevel.STABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.STABLE, "fluoride": StabilityLevel.STABLE},
        notes="Hindered ester; slow hydrolysis",
        orthogonal_with=["TBS", "Benzyl", "Boc"]
    ),
    "Cinnamyl_ester": ProtectingGroup(
        name="Cinnamyl Ester",
        abbreviation="Cinnamyl ester",
        install_reagents=["Cinnamyl alcohol/DCC"],
        install_conditions="DCC, DMAP, CH2Cl2",
        deprotect_reagents=["Pd(0)", "H2, Pd/C"],
        deprotect_conditions="Pd(0) with nucleophile or hydrogenolysis",
        deprotect_temp="rt",
        deprotect_time="1-4 h",
        stability={"strong_acid": StabilityLevel.STABLE, "weak_acid": StabilityLevel.STABLE,
                   "base": StabilityLevel.STABLE, "reducing": StabilityLevel.UNSTABLE,
                   "oxidizing": StabilityLevel.STABLE, "nucleophile": StabilityLevel.STABLE,
                   "hydrogenolysis": StabilityLevel.UNSTABLE, "fluoride": StabilityLevel.STABLE},
        notes="Pd-labile; orthogonal with many groups",
        orthogonal_with=["Methyl_ester", "tButyl_ester", "Boc"]
    ),
}


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

class ProtectingGroupResult(TypedDict):
    """Result structure for protecting group recommendation."""
    group_name: str
    abbreviation: str
    install_reagents: List[str]
    install_conditions: str
    deprotect_reagents: List[str]
    deprotect_conditions: str
    deprotect_temperature: str
    deprotect_time: str
    stability_profile: Dict[str, str]
    notes: str
    orthogonal_with: List[str]


class DeprotectionRisk(TypedDict):
    """Information about a protecting group at risk."""
    group_name: str
    abbreviation: str
    risk_level: str  # 'high', 'moderate', 'low'
    affected_by: List[str]
    suggestion: str


class DeprotectionPlanResult(TypedDict):
    """Result for deprotection planning."""
    at_risk_groups: List[DeprotectionRisk]
    safe_groups: List[str]
    recommended_sequence: List[str]
    warnings: List[str]


class OrthogonalStrategy(TypedDict):
    """Orthogonal protecting group strategy."""
    functional_group: str
    protecting_group: str
    install_order: int
    deprotect_order: int
    install_conditions: str
    deprotect_conditions: str
    notes: str


AlcoholType = Literal['primary', 'secondary', 'tertiary', 'phenolic']
AmineType = Literal['primary', 'secondary', 'aniline']
CarbonylType = Literal['aldehyde', 'ketone']
ConditionType = Literal['strong_acid', 'weak_acid', 'base', 'reducing', 'oxidizing', 
                         'nucleophile', 'hydrogenolysis', 'fluoride']


# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def protect_alcohol(
    oh_type: AlcoholType,
    conditions_sensitive_to: List[ConditionType]
) -> ProtectingGroupResult:
    """
    Recommend optimal protecting group for an alcohol.
    
    Args:
        oh_type: Type of alcohol ('primary', 'secondary', 'tertiary', 'phenolic')
        conditions_sensitive_to: List of reaction conditions the PG must survive
            (e.g., ['strong_acid', 'base', 'reducing'])
    
    Returns:
        Dictionary with protecting group recommendation including:
        - group_name: Full name of the protecting group
        - abbreviation: Common abbreviation
        - install_reagents: List of reagents for installation
        - install_conditions: Conditions for installation
        - deprotect_reagents: List of reagents for deprotection
        - deprotect_conditions: Conditions for deprotection
        - deprotect_temperature: Temperature range for deprotection
        - deprotect_time: Time required for deprotection
        - stability_profile: Dict mapping conditions to stability levels
        - notes: Additional notes and recommendations
        - orthogonal_with: List of compatible protecting groups
    
    Examples:
        >>> protect_alcohol('primary', ['base', 'reducing'])
        {'group_name': 'tert-Butyldimethylsilyl', 'abbreviation': 'TBS', ...}
        
        >>> protect_alcohol('phenolic', ['strong_acid'])
        {'group_name': 'Benzyl', 'abbreviation': 'Bn', ...}
    """
    # Filter groups that can be installed on the given alcohol type
    # and have required stability
    candidates = []
    
    for abbrev, pg in ALCOHOL_PROTECTING_GROUPS.items():
        # Check if PG is suitable for alcohol type
        # TMS is too labile for most multi-step synthesis
        if oh_type == 'tertiary' and abbrev in ['TMS', 'THP', 'EE']:
            continue  # Too labile or creates issues with tertiary alcohols
        
        # Check stability requirements
        meets_requirements = True
        stability_score = 0
        
        for condition in conditions_sensitive_to:
            if condition in pg.stability:
                stability = pg.stability[condition]
                if stability == StabilityLevel.UNSTABLE:
                    meets_requirements = False
                    break
                # Score based on stability level
                stability_scores = {
                    StabilityLevel.VERY_STABLE: 4,
                    StabilityLevel.STABLE: 3,
                    StabilityLevel.MODERATELY_STABLE: 2,
                    StabilityLevel.UNSTABLE: 0
                }
                stability_score += stability_scores.get(stability, 0)
        
        if meets_requirements:
            candidates.append((abbrev, pg, stability_score))
    
    if not candidates:
        # Fall back to most stable option even if not perfect
        all_groups = [(abbrev, pg, sum(
            4 if pg.stability.get(c) == StabilityLevel.VERY_STABLE else
            3 if pg.stability.get(c) == StabilityLevel.STABLE else
            2 if pg.stability.get(c) == StabilityLevel.MODERATELY_STABLE else 0
            for c in conditions_sensitive_to
        )) for abbrev, pg in ALCOHOL_PROTECTING_GROUPS.items()]
        candidates = sorted(all_groups, key=lambda x: x[2], reverse=True)[:3]
    
    # Sort by stability score and select best option
    candidates.sort(key=lambda x: x[2], reverse=True)
    
    # Prefer TBS for primary/secondary if it meets requirements
    preferred_order = ['TBS', 'TBDPS', 'Benzyl', 'MOM', 'Acetate', 'Benzoyl', 'TIPS', 'PMB']
    for pref in preferred_order:
        for abbrev, pg, score in candidates:
            if abbrev == pref:
                best = (abbrev, pg, score)
                break
        else:
            continue
        break
    else:
        best = candidates[0] if candidates else ('TBS', ALCOHOL_PROTECTING_GROUPS['TBS'], 0)
    
    _, pg, _ = best
    
    return ProtectingGroupResult(
        group_name=pg.name,
        abbreviation=pg.abbreviation,
        install_reagents=pg.install_reagents,
        install_conditions=pg.install_conditions,
        deprotect_reagents=pg.deprotect_reagents,
        deprotect_conditions=pg.deprotect_conditions,
        deprotect_temperature=pg.deprotect_temp,
        deprotect_time=pg.deprotect_time,
        stability_profile={k: v.value for k, v in pg.stability.items()},
        notes=pg.notes,
        orthogonal_with=pg.orthogonal_with
    )


def protect_amine(
    amine_type: AmineType,
    conditions_sensitive_to: List[ConditionType]
) -> ProtectingGroupResult:
    """
    Recommend protecting group for an amine.
    
    Args:
        amine_type: Type of amine ('primary', 'secondary', 'aniline')
        conditions_sensitive_to: List of conditions the PG must survive
    
    Returns:
        Dictionary with protecting group recommendation, including orthogonal
        compatibility information for multi-step synthesis.
    
    Examples:
        >>> protect_amine('primary', ['base', 'reducing'])
        {'group_name': 'tert-Butyloxycarbonyl', 'abbreviation': 'Boc', ...}
        
        >>> protect_amine('aniline', ['strong_acid'])
        {'group_name': 'Acetyl', 'abbreviation': 'Ac', ...}
    """
    candidates = []
    
    for abbrev, pg in AMINE_PROTECTING_GROUPS.items():
        # Some groups are better for certain amine types
        if amine_type == 'aniline':
            # Anilines are less nucleophilic; some groups harder to install
            if abbrev in ['Phthalimide', 'Phtaloyl']:
                continue  # Hard to install on anilines
        
        if amine_type == 'secondary':
            # Secondary amines can't use some carbamate-type groups easily
            if abbrev in ['Phthalimide', 'Phtaloyl']:
                continue
        
        # Check stability requirements
        meets_requirements = True
        stability_score = 0
        
        for condition in conditions_sensitive_to:
            if condition in pg.stability:
                stability = pg.stability[condition]
                if stability == StabilityLevel.UNSTABLE:
                    meets_requirements = False
                    break
                stability_scores = {
                    StabilityLevel.VERY_STABLE: 4,
                    StabilityLevel.STABLE: 3,
                    StabilityLevel.MODERATELY_STABLE: 2,
                    StabilityLevel.UNSTABLE: 0
                }
                stability_score += stability_scores.get(stability, 0)
        
        if meets_requirements:
            candidates.append((abbrev, pg, stability_score))
    
    if not candidates:
        all_groups = [(abbrev, pg, sum(
            4 if pg.stability.get(c) == StabilityLevel.VERY_STABLE else
            3 if pg.stability.get(c) == StabilityLevel.STABLE else
            2 if pg.stability.get(c) == StabilityLevel.MODERATELY_STABLE else 0
            for c in conditions_sensitive_to
        )) for abbrev, pg in AMINE_PROTECTING_GROUPS.items()]
        candidates = sorted(all_groups, key=lambda x: x[2], reverse=True)[:5]
    
    candidates.sort(key=lambda x: x[2], reverse=True)
    
    # Prefer Boc for primary amines, Cbz if reducing conditions needed to be avoided
    preferred_order = ['Boc', 'Cbz', 'Fmoc', 'Acetyl', 'TFA', 'Alloc', 'Benzyl_amine']
    for pref in preferred_order:
        for abbrev, pg, score in candidates:
            if abbrev == pref:
                best = (abbrev, pg, score)
                break
        else:
            continue
        break
    else:
        best = candidates[0] if candidates else ('Boc', AMINE_PROTECTING_GROUPS['Boc'], 0)
    
    _, pg, _ = best
    
    return ProtectingGroupResult(
        group_name=pg.name,
        abbreviation=pg.abbreviation,
        install_reagents=pg.install_reagents,
        install_conditions=pg.install_conditions,
        deprotect_reagents=pg.deprotect_reagents,
        deprotect_conditions=pg.deprotect_conditions,
        deprotect_temperature=pg.deprotect_temp,
        deprotect_time=pg.deprotect_time,
        stability_profile={k: v.value for k, v in pg.stability.items()},
        notes=pg.notes,
        orthogonal_with=pg.orthogonal_with
    )


def protect_carbonyl(
    carbonyl_type: CarbonylType,
    conditions_sensitive_to: List[ConditionType]
) -> ProtectingGroupResult:
    """
    Recommend protecting group for a carbonyl (aldehyde or ketone).
    
    Args:
        carbonyl_type: Type of carbonyl ('aldehyde' or 'ketone')
        conditions_sensitive_to: List of conditions the PG must survive
    
    Returns:
        Dictionary with protecting group recommendation.
    
    Examples:
        >>> protect_carbonyl('aldehyde', ['base', 'reducing'])
        {'group_name': '1,3-Dioxolane', 'abbreviation': 'Ethylene acetal', ...}
        
        >>> protect_carbonyl('ketone', ['strong_acid'])
        {'group_name': '1,3-Dithiane', 'abbreviation': 'Dithiane', ...}
    """
    candidates = []
    
    for abbrev, pg in CARBONYL_PROTECTING_GROUPS.items():
        # Some groups work better for aldehydes vs ketones
        # Hydrazones/oximes often used for aldehydes
        # Cyclic acetals work for both
        
        # Check stability requirements
        meets_requirements = True
        stability_score = 0
        
        for condition in conditions_sensitive_to:
            if condition in pg.stability:
                stability = pg.stability[condition]
                if stability == StabilityLevel.UNSTABLE:
                    meets_requirements = False
                    break
                stability_scores = {
                    StabilityLevel.VERY_STABLE: 4,
                    StabilityLevel.STABLE: 3,
                    StabilityLevel.MODERATELY_STABLE: 2,
                    StabilityLevel.UNSTABLE: 0
                }
                stability_score += stability_scores.get(stability, 0)
        
        if meets_requirements:
            candidates.append((abbrev, pg, stability_score))
    
    if not candidates:
        all_groups = [(abbrev, pg, sum(
            4 if pg.stability.get(c) == StabilityLevel.VERY_STABLE else
            3 if pg.stability.get(c) == StabilityLevel.STABLE else
            2 if pg.stability.get(c) == StabilityLevel.MODERATELY_STABLE else 0
            for c in conditions_sensitive_to
        )) for abbrev, pg in CARBONYL_PROTECTING_GROUPS.items()]
        candidates = sorted(all_groups, key=lambda x: x[2], reverse=True)[:5]
    
    candidates.sort(key=lambda x: x[2], reverse=True)
    
    # Prefer dioxolane for general use, dithiane if acid stability needed
    preferred_order = ['Dioxolane', 'Acetal', 'Dithiane', 'Oxime', 'Dimethylhydrazone']
    for pref in preferred_order:
        for abbrev, pg, score in candidates:
            if abbrev == pref:
                best = (abbrev, pg, score)
                break
        else:
            continue
        break
    else:
        best = candidates[0] if candidates else ('Dioxolane', CARBONYL_PROTECTING_GROUPS['Dioxolane'], 0)
    
    _, pg, _ = best
    
    return ProtectingGroupResult(
        group_name=pg.name,
        abbreviation=pg.abbreviation,
        install_reagents=pg.install_reagents,
        install_conditions=pg.install_conditions,
        deprotect_reagents=pg.deprotect_reagents,
        deprotect_conditions=pg.deprotect_conditions,
        deprotect_temperature=pg.deprotect_temp,
        deprotect_time=pg.deprotect_time,
        stability_profile={k: v.value for k, v in pg.stability.items()},
        notes=pg.notes,
        orthogonal_with=pg.orthogonal_with
    )


def protect_carboxylic_acid(
    conditions_sensitive_to: List[ConditionType]
) -> ProtectingGroupResult:
    """
    Recommend ester type for protecting a carboxylic acid.
    
    Args:
        conditions_sensitive_to: List of conditions the PG must survive
    
    Returns:
        Dictionary with ester recommendation.
    
    Examples:
        >>> protect_carboxylic_acid(['base', 'reducing'])
        {'group_name': 'tert-Butyl Ester', 'abbreviation': 't-Bu ester', ...}
        
        >>> protect_carboxylic_acid(['strong_acid'])
        {'group_name': 'Methyl Ester', 'abbreviation': 'Me ester', ...}
    """
    candidates = []
    
    for abbrev, pg in CARBOXYLIC_ACID_PROTECTING_GROUPS.items():
        # Check stability requirements
        meets_requirements = True
        stability_score = 0
        
        for condition in conditions_sensitive_to:
            if condition in pg.stability:
                stability = pg.stability[condition]
                if stability == StabilityLevel.UNSTABLE:
                    meets_requirements = False
                    break
                stability_scores = {
                    StabilityLevel.VERY_STABLE: 4,
                    StabilityLevel.STABLE: 3,
                    StabilityLevel.MODERATELY_STABLE: 2,
                    StabilityLevel.UNSTABLE: 0
                }
                stability_score += stability_scores.get(stability, 0)
        
        if meets_requirements:
            candidates.append((abbrev, pg, stability_score))
    
    if not candidates:
        all_groups = [(abbrev, pg, sum(
            4 if pg.stability.get(c) == StabilityLevel.VERY_STABLE else
            3 if pg.stability.get(c) == StabilityLevel.STABLE else
            2 if pg.stability.get(c) == StabilityLevel.MODERATELY_STABLE else 0
            for c in conditions_sensitive_to
        )) for abbrev, pg in CARBOXYLIC_ACID_PROTECTING_GROUPS.items()]
        candidates = sorted(all_groups, key=lambda x: x[2], reverse=True)[:5]
    
    candidates.sort(key=lambda x: x[2], reverse=True)
    
    # Prefer methyl or benzyl for general use
    preferred_order = ['Methyl_ester', 'Benzyl_ester', 'tButyl_ester', 'Ethyl_ester', 'Allyl_ester']
    for pref in preferred_order:
        for abbrev, pg, score in candidates:
            if abbrev == pref:
                best = (abbrev, pg, score)
                break
        else:
            continue
        break
    else:
        best = candidates[0] if candidates else ('Methyl_ester', CARBOXYLIC_ACID_PROTECTING_GROUPS['Methyl_ester'], 0)
    
    _, pg, _ = best
    
    return ProtectingGroupResult(
        group_name=pg.name,
        abbreviation=pg.abbreviation,
        install_reagents=pg.install_reagents,
        install_conditions=pg.install_conditions,
        deprotect_reagents=pg.deprotect_reagents,
        deprotect_conditions=pg.deprotect_conditions,
        deprotect_temperature=pg.deprotect_temp,
        deprotect_time=pg.deprotect_time,
        stability_profile={k: v.value for k, v in pg.stability.items()},
        notes=pg.notes,
        orthogonal_with=pg.orthogonal_with
    )


def deprotection_plan(
    protecting_groups_present: List[str],
    target_conditions: List[ConditionType]
) -> DeprotectionPlanResult:
    """
    Given a list of protecting groups on a molecule and desired reaction conditions,
    check if any will be affected.
    
    Args:
        protecting_groups_present: List of protecting group abbreviations on the molecule
            (e.g., ['TBS', 'Boc', 'Benzyl'])
        target_conditions: List of reaction conditions planned
            (e.g., ['strong_acid', 'base'])
    
    Returns:
        Dictionary containing:
        - at_risk_groups: List of groups that will be affected
        - safe_groups: List of groups that will survive
        - recommended_sequence: Suggested order for deprotection/installation
        - warnings: List of warning messages
    
    Examples:
        >>> deprotection_plan(['TBS', 'Boc'], ['strong_acid'])
        {'at_risk_groups': [...], 'safe_groups': ['TBS'], ...}
    """
    # Combine all protecting group databases
    all_pgs = {}
    all_pgs.update(ALCOHOL_PROTECTING_GROUPS)
    all_pgs.update(AMINE_PROTECTING_GROUPS)
    all_pgs.update(CARBONYL_PROTECTING_GROUPS)
    all_pgs.update(CARBOXYLIC_ACID_PROTECTING_GROUPS)
    
    at_risk = []
    safe = []
    warnings = []
    
    for pg_abbrev in protecting_groups_present:
        # Find the protecting group in database
        pg = all_pgs.get(pg_abbrev)
        if not pg:
            warnings.append(f"Unknown protecting group: {pg_abbrev}")
            continue
        
        # Check stability against target conditions
        affected_by = []
        risk_level = 'low'
        
        for condition in target_conditions:
            if condition in pg.stability:
                stability = pg.stability[condition]
                if stability == StabilityLevel.UNSTABLE:
                    affected_by.append(condition)
                    risk_level = 'high'
                elif stability == StabilityLevel.MODERATELY_STABLE:
                    affected_by.append(condition)
                    if risk_level != 'high':
                        risk_level = 'moderate'
        
        if affected_by:
            suggestion = f"Consider alternative PG or remove {pg_abbrev} before applying {', '.join(affected_by)}"
            if pg.orthogonal_with:
                suggestion += f". Orthogonal alternatives: {', '.join(pg.orthogonal_with[:3])}"
            
            at_risk.append(DeprotectionRisk(
                group_name=pg.name,
                abbreviation=pg.abbreviation,
                risk_level=risk_level,
                affected_by=affected_by,
                suggestion=suggestion
            ))
        else:
            safe.append(pg_abbrev)
    
    # Generate recommended deprotection sequence
    # Generally: acid-labile first, then hydrogenolysis, then base-labile, then fluoride
    sequence_priority = {
        'high_acid_labile': [],  # TMS, THP, Tr
        'moderate_acid_labile': [],  # Boc, t-Bu
        'hydrogenolysis': [],  # Cbz, Benzyl
        'base_labile': [],  # Fmoc, Ac, Bz
        'fluoride_labile': [],  # TBS, TBDPS, TIPS
        'other': []
    }
    
    for pg_abbrev in protecting_groups_present:
        pg = all_pgs.get(pg_abbrev)
        if not pg:
            continue
        
        # Categorize by primary deprotection method
        deprotect = pg.deprotect_conditions.lower()
        if 'acid' in deprotect or 'tfa' in deprotect or 'hcl' in deprotect:
            if pg.stability.get('weak_acid') == StabilityLevel.UNSTABLE:
                sequence_priority['high_acid_labile'].append(pg_abbrev)
            else:
                sequence_priority['moderate_acid_labile'].append(pg_abbrev)
        elif 'hydrogen' in deprotect or 'palladium' in deprotect or 'pd' in deprotect:
            sequence_priority['hydrogenolysis'].append(pg_abbrev)
        elif 'base' in deprotect or 'piperidine' in deprotect:
            sequence_priority['base_labile'].append(pg_abbrev)
        elif 'fluoride' in deprotect or 'tbaf' in deprotect:
            sequence_priority['fluoride_labile'].append(pg_abbrev)
        else:
            sequence_priority['other'].append(pg_abbrev)
    
    # Flatten into recommended sequence
    recommended_sequence = []
    for category in ['high_acid_labile', 'moderate_acid_labile', 'hydrogenolysis', 
                     'base_labile', 'fluoride_labile', 'other']:
        recommended_sequence.extend(sequence_priority[category])
    
    return DeprotectionPlanResult(
        at_risk_groups=at_risk,
        safe_groups=safe,
        recommended_sequence=recommended_sequence,
        warnings=warnings
    )


def orthogonal_set(
    molecule_functional_groups: List[Tuple[str, str]],
    synthesis_steps: List[Tuple[str, List[ConditionType]]]
) -> List[OrthogonalStrategy]:
    """
    Design an orthogonal protecting group strategy for a multi-functional molecule.
    
    Args:
        molecule_functional_groups: List of (fg_type, fg_subtype) tuples
            e.g., [('alcohol', 'primary'), ('amine', 'primary'), ('carboxylic_acid', '')]
        synthesis_steps: List of (step_name, conditions) tuples
            e.g., [('Grignard', ['base']), ('Hydrogenation', ['reducing', 'hydrogenolysis'])]
    
    Returns:
        List of orthogonal strategies for each functional group with:
        - functional_group: The protected functional group
        - protecting_group: Recommended PG
        - install_order: Order of installation (1 = first)
        - deprotect_order: Order of deprotection (1 = first to remove)
        - install_conditions: How to install
        - deprotect_conditions: How to remove
        - notes: Strategy notes
    
    Examples:
        >>> orthogonal_set(
        ...     [('alcohol', 'primary'), ('amine', 'primary')],
        ...     [('Grignard', ['base']), ('Coupling', ['reducing'])]
        ... )
        [{'functional_group': 'alcohol', 'protecting_group': 'TBS', ...}, ...]
    """
    # Collect all conditions needed across synthesis
    all_conditions = set()
    for step_name, conditions in synthesis_steps:
        all_conditions.update(conditions)
    
    strategies = []
    
    # Determine protection requirements for each FG
    for fg_type, fg_subtype in molecule_functional_groups:
        # Get conditions specific to this step that this FG needs to survive
        # For now, use all conditions as requirement
        conditions_list = list(all_conditions)
        
        # Get appropriate PG recommendation
        if fg_type == 'alcohol':
            result = protect_alcohol(fg_subtype, conditions_list)
        elif fg_type == 'amine':
            result = protect_amine(fg_subtype, conditions_list)
        elif fg_type == 'carbonyl':
            result = protect_carbonyl(fg_subtype, conditions_list)
        elif fg_type == 'carboxylic_acid':
            result = protect_carboxylic_acid(conditions_list)
        else:
            continue
        
        strategies.append(OrthogonalStrategy(
            functional_group=f"{fg_subtype} {fg_type}" if fg_subtype else fg_type,
            protecting_group=result['abbreviation'],
            install_order=0,  # Will be set later
            deprotect_order=0,  # Will be set later
            install_conditions=result['install_conditions'],
            deprotect_conditions=result['deprotect_conditions'],
            notes=result['notes']
        ))
    
    # Determine installation order
    # General rule: install acid-labile last, base-labile first for acids, etc.
    # More stable groups installed first
    install_priority = {
        'TIPS': 1, 'TBDPS': 2, 'TBS': 3, 'TES': 4, 'TMS': 5,
        'Benzyl': 2, 'Bn': 2, 'PMB': 4,
        'MOM': 3, 'THP': 5, 'Ac': 2, 'Bz': 2,
        'Boc': 3, 'Cbz': 2, 'Fmoc': 4, 'Alloc': 3,
        'Dioxolane': 2, 'Dithiane': 1,
        'Methyl_ester': 1, 'Ethyl_ester': 1, 'tButyl_ester': 3, 
        'Benzyl_ester': 2, 'Allyl_ester': 3
    }
    
    # Sort by install priority (lower number = install first)
    for i, strategy in enumerate(strategies):
        pg = strategy['protecting_group']
        strategy['install_order'] = install_priority.get(pg, 3)
    
    # Sort strategies by install order
    strategies.sort(key=lambda x: x['install_order'])
    
    # Renumber install orders to be 1, 2, 3...
    for i, strategy in enumerate(strategies):
        strategy['install_order'] = i + 1
    
    # Deprotection order is reverse of installation (last installed = first removed)
    # But also consider orthogonal removal methods
    deprotect_methods = {
        'TBAF': ['TBS', 'TBDPS', 'TIPS', 'TES', 'TMS', 'TBS_ester'],
        'acid': ['Boc', 'tButyl_ester', 'MOM', 'THP', 'Trityl', 'Dioxolane'],
        'H2/Pd': ['Cbz', 'Benzyl', 'Benzyl_ester', 'PMB', 'PMB_ester'],
        'base': ['Fmoc', 'Ac', 'Bz', 'Acetyl', 'Fm_ester'],
        'Pd(0)': ['Alloc', 'Allyl_ester']
    }
    
    # Assign deprotection order based on orthogonal removal
    for i, strategy in enumerate(strategies):
        strategy['deprotect_order'] = len(strategies) - i
    
    # Add orthogonal compatibility notes
    pg_list = [s['protecting_group'] for s in strategies]
    for strategy in strategies:
        pg = strategy['protecting_group']
        # Find orthogonal groups
        all_pgs = {**ALCOHOL_PROTECTING_GROUPS, **AMINE_PROTECTING_GROUPS, 
                   **CARBONYL_PROTECTING_GROUPS, **CARBOXYLIC_ACID_PROTECTING_GROUPS}
        if pg in all_pgs:
            orthogonal = [o for o in all_pgs[pg].orthogonal_with if o in pg_list]
            if orthogonal:
                strategy['notes'] += f" Orthogonal with others: {', '.join(orthogonal)}"
    
    return strategies


def deprotection_lookup(group_name: str) -> Dict[str, str]:
    """
    Quick lookup of deprotection conditions for any protecting group.
    
    Args:
        group_name: Name or abbreviation of the protecting group
            (e.g., 'TBS', 'tert-Butyldimethylsilyl', 'Boc', 'Benzyl')
    
    Returns:
        Dictionary containing:
        - reagent: Primary deprotection reagent
        - solvent: Recommended solvent
        - temperature: Temperature range
        - time: Time required
        - notes: Special considerations
    
    Examples:
        >>> deprotection_lookup('TBS')
        {'reagent': 'TBAF', 'solvent': 'THF', 'temperature': 'rt to 50°C', ...}
        
        >>> deprotection_lookup('Boc')
        {'reagent': 'TFA', 'solvent': 'CH2Cl2 (neat TFA also works)', ...}
    """
    # Combine all protecting group databases
    all_pgs = {}
    all_pgs.update(ALCOHOL_PROTECTING_GROUPS)
    all_pgs.update(AMINE_PROTECTING_GROUPS)
    all_pgs.update(CARBONYL_PROTECTING_GROUPS)
    all_pgs.update(CARBOXYLIC_ACID_PROTECTING_GROUPS)
    
    # Normalize input
    group_name = group_name.strip()
    
    # Try to find by abbreviation or name
    pg = all_pgs.get(group_name)
    if not pg:
        # Try case-insensitive match
        for abbrev, p in all_pgs.items():
            if abbrev.lower() == group_name.lower() or p.name.lower() == group_name.lower():
                pg = p
                break
    
    if not pg:
        return {
            'reagent': 'Unknown',
            'solvent': 'Unknown',
            'temperature': 'Unknown',
            'time': 'Unknown',
            'notes': f"Protecting group '{group_name}' not found in database. "
                    f"Common abbreviations: TBS, TBDPS, Boc, Cbz, Fmoc, Benzyl, MOM, THP, etc."
        }
    
    # Extract solvent from deprotection conditions
    deprotect_cond = pg.deprotect_conditions
    common_solvents = ['THF', 'CH2Cl2', 'DMF', 'MeOH', 'EtOH', 'AcOH', 'TFA', 'MeCN', 'dioxane']
    solvent = 'See conditions'
    for solv in common_solvents:
        if solv in deprotect_cond:
            solvent = solv
            break
    
    return {
        'reagent': pg.deprotect_reagents[0] if pg.deprotect_reagents else 'See conditions',
        'solvent': solvent,
        'temperature': pg.deprotect_temp,
        'time': pg.deprotect_time,
        'notes': pg.notes + f" Full conditions: {deprotect_cond}"
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def list_all_protecting_groups(fg_type: Optional[str] = None) -> List[str]:
    """
    List all available protecting groups, optionally filtered by functional group type.
    
    Args:
        fg_type: Optional filter ('alcohol', 'amine', 'carbonyl', 'carboxylic_acid')
    
    Returns:
        List of protecting group abbreviations
    """
    if fg_type == 'alcohol':
        return list(ALCOHOL_PROTECTING_GROUPS.keys())
    elif fg_type == 'amine':
        return list(AMINE_PROTECTING_GROUPS.keys())
    elif fg_type == 'carbonyl':
        return list(CARBONYL_PROTECTING_GROUPS.keys())
    elif fg_type == 'carboxylic_acid':
        return list(CARBOXYLIC_ACID_PROTECTING_GROUPS.keys())
    else:
        all_pgs = set()
        all_pgs.update(ALCOHOL_PROTECTING_GROUPS.keys())
        all_pgs.update(AMINE_PROTECTING_GROUPS.keys())
        all_pgs.update(CARBONYL_PROTECTING_GROUPS.keys())
        all_pgs.update(CARBOXYLIC_ACID_PROTECTING_GROUPS.keys())
        return sorted(list(all_pgs))


def check_compatibility(pg1: str, pg2: str) -> Dict[str, any]:
    """
    Check if two protecting groups are orthogonal (compatible).
    
    Args:
        pg1: First protecting group abbreviation
        pg2: Second protecting group abbreviation
    
    Returns:
        Dictionary with compatibility information
    """
    all_pgs = {}
    all_pgs.update(ALCOHOL_PROTECTING_GROUPS)
    all_pgs.update(AMINE_PROTECTING_GROUPS)
    all_pgs.update(CARBONYL_PROTECTING_GROUPS)
    all_pgs.update(CARBOXYLIC_ACID_PROTECTING_GROUPS)
    
    pg1_data = all_pgs.get(pg1)
    pg2_data = all_pgs.get(pg2)
    
    if not pg1_data or not pg2_data:
        return {
            'compatible': False,
            'reason': 'One or both protecting groups not found in database'
        }
    
    # Check if they're in each other's orthogonal lists
    orthogonal = pg2 in pg1_data.orthogonal_with or pg1 in pg2_data.orthogonal_with
    
    # Check deprotection conditions overlap
    deprotect1 = pg1_data.deprotect_conditions.lower()
    deprotect2 = pg2_data.deprotect_conditions.lower()
    
    # Check for potential conflicts
    conflicts = []
    
    # Both removed by fluoride
    if 'fluoride' in deprotect1 and 'fluoride' in deprotect2:
        if 'TBS' in pg1 or 'TBDPS' in pg1 or 'TIPS' in pg1:
            if 'TBS' in pg2 or 'TBDPS' in pg2 or 'TIPS' in pg2:
                conflicts.append('Both removed by fluoride - selectivity may be limited')
    
    # Both acid-labile
    if 'acid' in deprotect1 or 'tfa' in deprotect1:
        if 'acid' in deprotect2 or 'tfa' in deprotect2:
            # Check if one is more labile
            if pg1_data.stability.get('strong_acid') == StabilityLevel.UNSTABLE:
                if pg2_data.stability.get('strong_acid') == StabilityLevel.UNSTABLE:
                    conflicts.append('Both acid-labile - selectivity may be limited')
    
    return {
        'compatible': orthogonal or len(conflicts) == 0,
        'orthogonal': orthogonal,
        'pg1_deprotection': pg1_data.deprotect_conditions,
        'pg2_deprotection': pg2_data.deprotect_conditions,
        'conflicts': conflicts if conflicts else ['No conflicts detected'],
        'recommendation': 'Can be used together' if orthogonal or not conflicts 
                         else 'Consider alternative protecting groups'
    }


# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("PROTECTING GROUP TOOLS - EXAMPLE USAGE")
    print("=" * 60)
    
    # Example 1: Protect alcohol
    print("\n1. Protecting a primary alcohol for base and reducing conditions:")
    result = protect_alcohol('primary', ['base', 'reducing'])
    print(f"   Recommended: {result['group_name']} ({result['abbreviation']})")
    print(f"   Install: {result['install_conditions']}")
    print(f"   Deprotect: {result['deprotect_conditions']}")
    
    # Example 2: Protect amine
    print("\n2. Protecting a primary amine for acid conditions:")
    result = protect_amine('primary', ['strong_acid'])
    print(f"   Recommended: {result['group_name']} ({result['abbreviation']})")
    print(f"   Deprotect: {result['deprotect_conditions']}")
    
    # Example 3: Deprotection lookup
    print("\n3. Quick deprotection lookup for Boc:")
    result = deprotection_lookup('Boc')
    print(f"   Reagent: {result['reagent']}")
    print(f"   Temperature: {result['temperature']}")
    
    # Example 4: Deprotection plan
    print("\n4. Deprotection plan for molecule with TBS and Boc under TFA conditions:")
    result = deprotection_plan(['TBS', 'Boc'], ['strong_acid'])
    print(f"   At-risk groups: {[g['abbreviation'] for g in result['at_risk_groups']]}")
    print(f"   Safe groups: {result['safe_groups']}")
    
    # Example 5: Orthogonal set
    print("\n5. Orthogonal strategy for molecule with alcohol and amine:")
    result = orthogonal_set(
        [('alcohol', 'primary'), ('amine', 'primary')],
        [('Grignard', ['base']), ('Coupling', ['reducing'])]
    )
    for strategy in result:
        print(f"   {strategy['functional_group']}: {strategy['protecting_group']}")
        print(f"      Install order: {strategy['install_order']}, Deprotect order: {strategy['deprotect_order']}")
    
    print("\n" + "=" * 60)
    print(f"Total protecting groups in database:")
    print(f"   Alcohols: {len(ALCOHOL_PROTECTING_GROUPS)}")
    print(f"   Amines: {len(AMINE_PROTECTING_GROUPS)}")
    print(f"   Carbonyls: {len(CARBONYL_PROTECTING_GROUPS)}")
    print(f"   Carboxylic acids: {len(CARBOXYLIC_ACID_PROTECTING_GROUPS)}")
    print("=" * 60)
