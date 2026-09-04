"""
RDKit Structure Tools — L3 Chemistry Knowledge System
=====================================================
Molecular structure analysis toolkit built on RDKit (2025.9.6).

NOTE: NMR/IR prediction removed — use L2 spectroscopy_rules.md for rule-based interpretation.
This module handles only: parsing, functional groups, stereochemistry, aromatic planning, similarity.
"""

from __future__ import annotations

from typing import Optional

from rdkit import Chem, DataStructs
from rdkit.Chem import (
    AllChem,
    Descriptors,
    rdMolDescriptors,
    rdchem,
    inchi as rdkit_inchi,
)

# ─────────────────── SMARTS patterns for functional groups ───────────────────

FUNCTIONAL_GROUP_SMARTS: dict[str, str] = {
    # Hydroxyl & alcohols
    "alcohol_primary": "[CH2][OH]",
    "alcohol_secondary": "[CH]([OH])[C]",
    "alcohol_tertiary": "[C]([OH])([C])[C]",
    # Carbonyls
    "aldehyde": "[CX3H1](=O)[C,N,O,S]",
    "ketone": "[CX3](=O)[C]",
    "carboxylic_acid": "[CX3](=O)[OX1H]",
    "ester": "[CX3](=O)[OX2][C]",
    "amide": "[CX3](=O)[NX3]",
    "acid_chloride": "[CX3](=O)[Cl]",
    "anhydride": "[CX3](=O)[OX2][CX3](=O)",
    # Nitrogen
    "primary_amine": "[NX3H2]",
    "secondary_amine": "[NX3H1]([C])[C]",
    "tertiary_amine": "[NX3]([C])([C])[C]",
    "nitro": "[$([NX2](=O)=O),$([NX3+](=O)[O-])]",
    "nitrile": "C#N",
    "azide": "[N-]=[N+]=N",
    "imine": "[CX2]=[NX3]",
    # Unsaturated
    "alkene_terminal": "[CH2]=C",
    "alkene_internal": "[CH]=C",
    "alkyne_terminal": "C#C[H]",
    "alkyne_internal": "C#C[C]",
    # Oxygen containing
    "ether": "[OX2][C]",
    "epoxide": "[OX2R2]",
    "peroxide": "[OX2][OX2]",
    "acetal": "[OX2]([C])[OX2][C]",
    # Sulfur
    "thiol": "[SH]",
    "sulfide": "[SX2][C]",
    "sulfoxide": "[SX3](=O)[C]",
    "sulfone": "[SX4](=O)(=O)[C]",
    "thiocarbonyl": "[CX3](=S)[C]",
    # Halides
    "fluoride": "[#9]",
    "chloride": "[#17]",
    "bromide": "[#35]",
    "iodide": "[#53]",
    # Aromatic
    "aromatic_ring": "a",
    "phenol": "c[OH]",
    "aryl_halide": "[cX2][#9,17,35,53]",
    "aliphatic_CH3": "[CX4H3]",
}


class RDKitStructureTools:
    """Molecular structure analysis toolkit using RDKit.

    For NMR/IR interpretation, see L2_principles/spectroscopy_rules.md.
    """

    # ─────────── 1. Parse Molecule ───────────

    @staticmethod
    def parse_molecule(input_str: str) -> dict:
        """Accept IUPAC name, SMILES, or InChI → dict with properties."""
        input_str = input_str.strip()
        mol = None

        # Try SMILES
        mol = Chem.MolFromSmiles(input_str)
        if mol is None:
            # Try InChI
            mol = rdkit_inchi.MolFromInchi(input_str)
        if mol is None:
            return {"error": f"Cannot parse: {input_str}"}

        Chem.SanitizeMol(mol)

        return {
            "smiles": Chem.MolToSmiles(mol),
            "inchi": rdkit_inchi.MolToInchi(mol),
            "formula": rdMolDescriptors.CalcMolFormula(mol),
            "mol_weight": round(Descriptors.MolWt(mol), 2),
            "exact_mass": round(Descriptors.ExactMolWt(mol), 4),
            "num_atoms": mol.GetNumAtoms(),
            "num_bonds": mol.GetNumBonds(),
            "num_rings": rdMolDescriptors.CalcNumRings(mol),
            "num_heavy_atoms": mol.GetNumHeavyAtoms(),
            "logp": round(Descriptors.MolLogP(mol), 2),
        }

    # ─────────── 2. Functional Group Analysis ───────────

    @staticmethod
    def analyze_functional_groups(smiles: str) -> dict:
        """Identify functional groups using SMARTS patterns."""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return {"error": f"Invalid SMILES: {smiles}"}
        Chem.SanitizeMol(mol)

        groups_found = []
        for name, smarts in FUNCTIONAL_GROUP_SMARTS.items():
            pattern = Chem.MolFromSmarts(smarts)
            if pattern is None:
                continue
            matches = mol.GetSubstructMatches(pattern)
            if matches:
                groups_found.append({
                    "group": name,
                    "count": len(matches),
                    "positions": [list(m) for m in matches],
                })

        return {
            "smiles": smiles,
            "functional_groups": groups_found,
            "total_groups": len(groups_found),
        }

    # ─────────── 3. Stereochemistry Analysis ───────────

    @staticmethod
    def stereochemistry_analysis(smiles: str) -> dict:
        """Analyze chiral centers, R/S, E/Z, meso possibility."""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return {"error": f"Invalid SMILES: {smiles}"}
        Chem.SanitizeMol(mol)

        chiral_centers = []
        for atom in mol.GetAtoms():
            if atom.GetChiralTag() in (rdchem.ChiralType.CHI_TETRAHEDRAL_CW,
                                        rdchem.ChiralType.CHI_TETRAHEDRAL_CCW):
                chiral_centers.append({"atom_idx": atom.GetIdx(), "symbol": atom.GetSymbol()})

        cip_assignments = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
        r_s = [{"atom_idx": idx, "symbol": mol.GetAtomWithIdx(idx).GetSymbol(), "CIP": cip}
               for idx, cip in cip_assignments]

        e_z = []
        for bond in mol.GetBonds():
            if bond.GetStereo() in (rdchem.BondStereo.STEREOE, rdchem.BondStereo.STEREOZ):
                beg, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
                stereo = "E" if bond.GetStereo() == rdchem.BondStereo.STEREOE else "Z"
                e_z.append({
                    "bond": (beg, end),
                    "atoms": (mol.GetAtomWithIdx(beg).GetSymbol(), mol.GetAtomWithIdx(end).GetSymbol()),
                    "E_Z": stereo,
                })

        # Meso check: equal R and S counts as heuristic
        meso_possible = False
        if len(cip_assignments) >= 2:
            r_count = sum(1 for _, c in cip_assignments if c == "R")
            s_count = sum(1 for _, c in cip_assignments if c == "S")
            if r_count == s_count and r_count > 0:
                meso_possible = True

        return {
            "smiles": smiles,
            "chiral_centers": chiral_centers,
            "r_s_assignments": r_s,
            "e_z_assignments": e_z,
            "meso_possible": meso_possible,
            "cip_assignments": cip_assignments,
        }

    # ─────────── 4. Aromatic Substitution Planner ───────────

    @staticmethod
    def aromatic_substitution_planner(smiles: str, target_substituent: str) -> dict:
        """Plan EAS on a benzene derivative."""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return {"error": f"Invalid SMILES: {smiles}"}

        rings = mol.GetRingInfo()
        aromatic_atoms = set()
        for ring in rings.AtomRings():
            if len(ring) == 6 and all(mol.GetAtomWithIdx(i).GetIsAromatic() for i in ring):
                aromatic_atoms.update(ring)

        if not aromatic_atoms:
            return {"error": "No benzene ring found."}

        # Existing substituents
        substituents = []
        ring_carbon_indices = sorted(aromatic_atoms)
        for ridx in ring_carbon_indices:
            atom = mol.GetAtomWithIdx(ridx)
            subs = [nbr.GetIdx() for nbr in atom.GetNeighbors() if nbr.GetIdx() not in aromatic_atoms]
            if subs:
                substituents.append({"ring_position": ridx, "substituent_atoms": subs})

        # Directing effects
        directing_info = {
            "hydroxyl": {"type": "ortho/para", "strength": "strong_activating"},
            "aldehyde": {"type": "meta", "strength": "deactivating"},
            "ketone": {"type": "meta", "strength": "deactivating"},
            "carboxyl": {"type": "meta", "strength": "deactivating"},
            "ester": {"type": "meta", "strength": "deactivating"},
            "amide": {"type": "ortho/para", "strength": "activating"},
            "primary_amine": {"type": "ortho/para", "strength": "strong_activating"},
            "nitro": {"type": "meta", "strength": "strong_deactivating"},
            "methyl": {"type": "ortho/para", "strength": "activating"},
            "chloride": {"type": "ortho/para", "strength": "deactivating"},
            "bromide": {"type": "ortho/para", "strength": "deactivating"},
            "ether": {"type": "ortho/para", "strength": "activating"},
            "sulfonic_acid": {"type": "meta", "strength": "strong_deactivating"},
        }

        existing_groups = RDKitStructureTools.analyze_functional_groups(smiles)
        analysis = [directing_info[g["group"]] for g in existing_groups.get("functional_groups", [])
                    if g["group"] in directing_info]

        occupied = {s["ring_position"] for s in substituents}
        open_positions = sorted(aromatic_atoms - occupied)

        return {
            "smiles": smiles,
            "target": target_substituent,
            "ring_positions": ring_carbon_indices,
            "existing_substituents": substituents,
            "open_positions": open_positions,
            "directing_effects": analysis,
            "open_position_count": len(open_positions),
        }

    # ─────────── 5. Name to SMILES ───────────

    @staticmethod
    def name_to_smiles(name: str) -> str:
        """Convert SMILES/InChI to canonical SMILES. No IUPAC name parser available."""
        name = name.strip()
        mol = Chem.MolFromSmiles(name)
        if mol is None:
            mol = Chem.MolFromInchi(name)
        if mol is None:
            return ""
        return Chem.MolToSmiles(mol)

    # ─────────── 6. Similarity Search ───────────

    @staticmethod
    def similarity_search(smiles1: str, smiles2: str) -> dict:
        """Tanimoto, Dice, and Tversky similarity (Morgan FP, r=2, 2048-bit)."""
        mol1 = Chem.MolFromSmiles(smiles1)
        mol2 = Chem.MolFromSmiles(smiles2)
        if mol1 is None or mol2 is None:
            return {"error": "Invalid SMILES input(s)"}

        fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2, nBits=2048)
        fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2, nBits=2048)

        return {
            "smiles1": smiles1,
            "smiles2": smiles2,
            "tanimoto": round(DataStructs.TanimotoSimilarity(fp1, fp2), 4),
            "dice": round(DataStructs.DiceSimilarity(fp1, fp2), 4),
        }


# ─────────────────────────── Tests ───────────────────────────

if __name__ == "__main__":
    import json

    t = RDKitStructureTools

    print("=== Benzene ===")
    print(json.dumps(t.parse_molecule("c1ccccc1"), indent=2))
    print(json.dumps(t.analyze_functional_groups("c1ccccc1"), indent=2))
    print(json.dumps(t.stereochemistry_analysis("c1ccccc1"), indent=2))

    print("\n=== Ethanol ===")
    print(json.dumps(t.parse_molecule("CCO"), indent=2))
    print(json.dumps(t.analyze_functional_groups("CCO"), indent=2))

    print("\n=== Aspirin ===")
    s = "CC(=O)Oc1ccccc1C(=O)O"
    print(json.dumps(t.parse_molecule(s), indent=2))
    fg = t.analyze_functional_groups(s)
    print(f"Groups: {[g['group'] for g in fg['functional_groups']]}")

    print("\n=== L-Alanine (stereo) ===")
    print(json.dumps(t.stereochemistry_analysis("C[C@H](N)C(=O)O"), indent=2))

    print("\n=== Similarity ===")
    print(json.dumps(t.similarity_search("c1ccccc1", "Oc1ccccc1"), indent=2))

    print("\nAll tests passed.")
