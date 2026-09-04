"""
L3 Retrosynthesis Planning Tool
Wraps AiZynthFinder with rule-based fallback for retrosynthetic analysis.

Dependencies: rdkit, aizynthfinder (v4.4.1+, optional)
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# SMILES helpers & RDKit utilities
# ---------------------------------------------------------------------------

def _get_rdkit():
    """Lazy import of RDKit — returns the Chem module or None."""
    try:
        from rdkit import Chem
        return Chem
    except ImportError:
        return None


def _get_allchem():
    """Lazy import of RDKit AllChem — returns the AllChem module or None."""
    try:
        from rdkit.Chem import AllChem
        return AllChem
    except ImportError:
        return None


def _rxn_from_smarts(smarts):
    """Create a reaction from SMARTS using the correct RDKit API."""
    AllChem = _get_allchem()
    if AllChem is not None and hasattr(AllChem, 'ReactionFromSmarts'):
        return AllChem.ReactionFromSmarts(smarts)
    Chem = _get_rdkit()
    if Chem is not None and hasattr(Chem, 'ReactionFromSmarts'):
        return Chem.ReactionFromSmarts(smarts)
    return None


def validate_smiles(smiles: str) -> bool:
    """Check if a SMILES string is valid using RDKit."""
    Chem = _get_rdkit()
    if Chem is None:
        logger.warning("RDKit not available — cannot validate SMILES.")
        return bool(smiles and smiles.strip())
    mol = Chem.MolFromSmiles(smiles.strip())
    return mol is not None


def canonical_smiles(smiles: str) -> str:
    """Return canonical SMILES or raise ValueError."""
    Chem = _get_rdkit()
    if Chem is None:
        return smiles.strip()
    mol = Chem.MolFromSmiles(smiles.strip())
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles!r}")
    return Chem.MolToSmiles(mol)


def mol_to_smiles(mol) -> Optional[str]:
    Chem = _get_rdkit()
    if Chem is None or mol is None:
        return None
    return Chem.MolToSmiles(mol)

# ---------------------------------------------------------------------------
# Rule-based retrosynthesis templates  (SMARTS-based)
# ---------------------------------------------------------------------------

# Each template: (name, retro_smarts, forward_description, priority)
RETRO_TEMPLATES = [
    # Amide (both aliphatic and aromatic N-substituents)
    ("Amide hydrolysis",
     "[C:1](=[O:2])[N:3]>>[C:1](=[O:2])[OH].[N:3]",
     "amide hydrolysis", 10),
    # Ester
    ("Ester hydrolysis",
     "[C:1](=[O:2])[O:3][C:4]>>[C:1](=[O:2])[OH].[C:4][O]",
     "ester hydrolysis / transesterification", 9),
    # Aromatic ester  (O-aryl)
    ("Aryl ester cleavage",
     "[C:1](=[O:2])[O:3][c:4]>>[C:1](=[O:2])[OH].[c:4][OH]",
     "aryl ester cleavage", 9),
    # Ether (benzyl)
    ("Benzyl ether cleavage",
     "[c:1][CH2:2][O:3][C:4]>>[c:1][CH2:2][OH].[C:4][OH]",
     "benzyl ether cleavage", 7),
    # Carbonate
    ("Carbonate cleavage",
     "[O:1][C:2](=[O:3])[O:4][C:5]>>[O:1][C:2](=[O:3])[OH].[C:5][OH]",
     "carbonate cleavage", 8),
    # Anhydride
    ("Anhydride opening",
     "[C:1](=[O:2])[O:3][C:4](=[O:5])>>[C:1](=[O:2])[OH].[C:4](=[O:5])[OH]",
     "anhydride opening", 9),
    # Nitrile hydrolysis
    ("Nitrile hydrolysis",
     "[C:1]#[N:2]>>[C:1](=[O])[OH].[N]",
     "nitrile hydrolysis to acid", 6),
    # Nitro reduction (to amine)
    ("Nitro reduction",
     "[N+:1](=[O:2])[O-:3]>>[NH2:1]",
     "nitro reduction to amine (Fe/HCl, Sn/HCl, H2/Pd)", 5),
    # Halogen removal (reductive dehalogenation)
    ("Dehalogenation",
     "[C:1][Cl,Br,I:2]>>[C:1][H]",
     "reductive dehalogenation", 4),
    # Aldol-type C-C cleavage (beta-hydroxy carbonyl)
    ("Aldol retro",
     "[C:1]([OH:2])[CH2:3][C:4](=[O:5])>>[C:1](=[O:5])[CH3:3].[C:4](=[O:5])[H]",
     "retro-aldol", 8),
    # Diels-Alder retro (simplified: cyclohexene → diene + dienophile)
    ("Retro-Diels-Alder",
     "[C:1]1[CH:2]=[CH:3][CH:4]=[CH:5][CH2:6][CH:7]1>>[C:1]=[CH:2][CH:3]=[CH:4].[CH:5]=[CH:6]",
     "retro-Diels-Alder", 7),
    # Suzuki coupling (biaryl → aryl halide + aryl)
    ("Retro-Suzuki",
     "[c:1]-[c:2]>>[c:1]Br.[c:2]",
     "retro-Suzuki coupling", 8),
    # Wittig-like: C=C adjacent to carbonyl precursor → carbonyl + ylide
    ("Retro-Wittig",
     "[C:1]=[C:2][C:3](=[O:4])>>[C:1]=[O].[C:2]=[C:3]",
     "retro-Wittig / Horner-Wadsworth-Emmons", 7),
]

# Forward reaction templates: name → list of (smarts_pattern, description)
FORWARD_TEMPLATES = {
    "Grignard addition": [
        ("[C:1][Mg].[C:2](=[O:3])>>[C:1][C:2]([OH:3])",
         "Grignard reagent + aldehyde/ketone -> alcohol"),
    ],
    "Wittig": [
        # Simplified - actual Wittig uses phosphonium ylide
        ("[CH2:1]=[O:2]>>[CH2:1]", "aldehyde -> alkene (via Wittig)"),
    ],
    "Aldol": [
        ("[C:1](=[O:2])[CH2:3].[CH:4]=[O:5]>>[C:1](=[O:2])[CH:3]([OH])[CH:4]",
         "ketone + aldehyde -> beta-hydroxy ketone"),
    ],
    "Michael addition": [
        ("[C:1](=[O:2])[CH:3]=[CH:4].[C:5]([O-])>>[C:1](=[O:2])[CH2:3][CH2:4]",
         "enolate + enone -> 1,5-dicarbonyl"),
    ],
    "Diels-Alder": [
        ("[C:1]=[C:2][C:3]=[C:4].[C:5]=[C:6]>>[C:1]1[C:2]=[C:3][C:4][C:5][C:6]1",
         "diene + dienophile -> cyclohexene"),
    ],
    "Suzuki coupling": [
        # Simplified - aryl-aryl bond formation
        ("[c:1]Br.[c:2]>>[c:1][c:2]",
         "aryl halide + aryl -> biaryl"),
    ],
    "Heck reaction": [
        ("[c:1]Br.[C:2]=[C:3]>>[c:1][C:2]=[C:3]",
         "aryl halide + alkene -> styrene derivative"),
    ],
    "Sonogashira coupling": [
        ("[c:1]Br.[C:2]#C>>[c:1][C:2]#C",
         "aryl halide + alkyne -> aryl alkyne"),
    ],
    "Esterification": [
        ("[C:1](=[O:2])[OH].[C:3][OH]>>[C:1](=[O:2])[O:3][C:3]",
         "acid + alcohol -> ester"),
    ],
    "Amidation": [
        ("[C:1](=[O:2])[OH].[NH2:3]>>[C:1](=[O:2])[N:3][H]",
         "acid + amine -> amide"),
    ],
    "LiAlH4 reduction": [
        ("[C:1](=[O:2])[OH]>>[C:1][OH]",
         "carboxylic acid -> primary alcohol"),
    ],
    "NaBH4 reduction": [
        ("[C:1](=[O:2])[H]>>[C:1][OH]",
         "aldehyde -> primary alcohol"),
        ("[C:1](=[O:2])[C:3]>>[C:1]([OH:2])[C:3]",
         "ketone -> secondary alcohol"),
    ],
    "PCC oxidation": [
        ("[C:1][OH:2]>>[C:1](=[O:2])",
         "primary alcohol -> aldehyde"),
    ],
    "Jones oxidation": [
        ("[C:1][OH:2]>>[C:1](=[O:2])[OH]",
         "primary alcohol -> carboxylic acid"),
    ],
    "Swern oxidation": [
        ("[C:1][OH:2]>>[C:1](=[O:2])",
         "alcohol -> aldehyde/ketone"),
    ],
}

# Common SMILES for text → SMILES conversion
_NAME_TO_SMILES = {
    "aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "acetylsalicylic acid": "CC(=O)Oc1ccccc1C(=O)O",
    "paracetamol": "CC(=O)Nc1ccc(O)cc1",
    "acetaminophen": "CC(=O)Nc1ccc(O)cc1",
    "ibuprofen": "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "caffeine": "Cn1cnc2c1c(=O)n(C)c(=O)n2C",
    "benzene": "c1ccccc1",
    "ethanol": "CCO",
    "acetic acid": "CC(=O)O",
    "salicylic acid": "Oc1ccccc1C(=O)O",
    "phenol": "Oc1ccccc1",
    "toluene": "Cc1ccccc1",
    "aniline": "Nc1ccccc1",
    "benzaldehyde": "O=Cc1ccccc1",
    "acetophenone": "CC(=O)c1ccccc1",
    "benzoic acid": "OC(=O)c1ccccc1",
    "acetic anhydride": "CC(=O)OC(=O)C",
    "methylamine": "CN",
    "ethylamine": "CCN",
    "methanol": "CO",
    "formaldehyde": "C=O",
    "acetone": "CC(=O)C",
    "ethyl acetate": "CC(=O)OCC",
}

# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class RetrosynthesisPlanner:
    """
    Retrosynthesis planning tool wrapping AiZynthFinder with a rule-based
    fallback for environments where ML models are not available.

    The planner can:
    - Generate retrosynthetic routes (ML-powered or rule-based)
    - Identify strategic disconnection bonds in a molecule
    - Predict forward reaction products from reactant SMILES
    - Accept human-readable descriptions and suggest full routes
    """

    def __init__(self):
        self.aizynth_available = False
        self.finder: Any = None
        self._Chem = _get_rdkit()

    # ------------------------------------------------------------------
    # 1. setup
    # ------------------------------------------------------------------
    def setup(self, policy_model: str = "default", template_model: str = "default") -> None:
        """Initialize AiZynthFinder with the specified models.

        If models are not downloaded, sets ``self.aizynth_available = False``
        and the planner will use rule-based retrosynthesis as a fallback.

        Parameters
        ----------
        policy_model : str
            Policy network name (e.g. ``"default"``).  Path to a custom
            ``.ckpt`` / ``.hdf5`` is also accepted.
        template_model : str
            Template-based expansion model name.
        """
        try:
            from aizynthfinder.aizynthfinder import AiZynthFinder
            try:
                configdict = {}
                if policy_model != "default":
                    configdict["policy"] = policy_model
                if template_model != "default":
                    configdict["template"] = template_model
                self.finder = AiZynthFinder(
                    configdict=configdict if configdict else None
                )
                # Check if expansion policy is actually available
                # Without models, AiZynthFinder can't do retrosynthesis
                if hasattr(self.finder, 'expansion_policy') and self.finder.expansion_policy:
                    # Try to check if there are any policies loaded
                    policy_names = []
                    try:
                        policy_names = list(self.finder.expansion_policy.keys())
                    except Exception:
                        pass
                    if policy_names:
                        self.aizynth_available = True
                        logger.info(f"AiZynthFinder initialized with policies: {policy_names}")
                    else:
                        self.aizynth_available = False
                        logger.warning(
                            "AiZynthFinder initialized but no expansion policies found. "
                            "Falling back to rule-based retrosynthesis."
                        )
                else:
                    self.aizynth_available = False
                    logger.warning(
                        "AiZynthFinder initialized but expansion_policy not available. "
                        "Falling back to rule-based retrosynthesis."
                    )
            except Exception as exc:
                self.aizynth_available = False
                logger.warning(
                    "AiZynthFinder model loading failed (%s). "
                    "Falling back to rule-based retrosynthesis.",
                    exc,
                )
        except ImportError:
            self.aizynth_available = False
            logger.warning(
                "aizynthfinder package not importable. "
                "Using rule-based retrosynthesis only."
            )

    # ------------------------------------------------------------------
    # 2. plan_retrosynthesis
    # ------------------------------------------------------------------
    def plan_retrosynthesis(self, target_smiles: str, max_steps: int = 5) -> dict:
        """Generate retrosynthetic routes for a target molecule.

        Parameters
        ----------
        target_smiles : str
            Target molecule SMILES string.
        max_steps : int
            Maximum retrosynthetic depth.

        Returns
        -------
        dict
            ``{
                routes: [{steps: [...], overall_score: float}, ...],
                best_route: {...} | None
            }``
        """
        if not validate_smiles(target_smiles):
            return {"routes": [], "best_route": None, "error": f"Invalid SMILES: {target_smiles}"}

        target = canonical_smiles(target_smiles)

        if self.aizynth_available and self.finder is not None:
            return self._plan_ml(target, max_steps)
        return self._plan_rulebased(target, max_steps)

    def _plan_ml(self, target: str, max_steps: int) -> dict:
        """ML-powered planning via AiZynthFinder."""
        try:
            from aizynthfinder.aizynthfinder import AiZynthFinder
            finder = AiZynthFinder()
            finder.target_smiles = target
            finder.prepare_tree()
            finder.build_routes()
            routes = []
            for route in finder.routes:
                steps = []
                # Walk the tree from root
                if hasattr(route, 'tree'):
                    tree = route.tree
                    nodes_to_visit = [tree.root]
                    visited = set()
                    while nodes_to_visit:
                        node = nodes_to_visit.pop(0)
                        if node is None or id(node) in visited:
                            continue
                        visited.add(id(node))
                        if hasattr(node, 'children'):
                            for child in node.children:
                                if child and hasattr(child, 'transform') and child.transform:
                                    steps.append({
                                        "product": getattr(node, 'smiles', ''),
                                        "reactants": [getattr(c, 'smiles', str(c)) for c in (child.children or [])],
                                        "reaction_type": child.transform or "unknown",
                                        "score": 0.5,
                                    })
                                nodes_to_visit.append(child)
                if not steps and hasattr(route, 'reactions'):
                    for rxn in route.reactions:
                        steps.append({
                            "product": rxn.product if hasattr(rxn, 'product') else '',
                            "reactants": list(rxn.reactants) if hasattr(rxn, 'reactants') else [],
                            "reaction_type": rxn.metadata.get('name', 'unknown') if hasattr(rxn, 'metadata') else 'unknown',
                            "score": 0.5,
                        })
                routes.append({
                    "steps": steps,
                    "overall_score": getattr(route, 'score', 0.5) if hasattr(route, 'score') else 0.5,
                })
            return {
                "routes": routes,
                "best_route": routes[0] if routes else None,
            }
        except Exception as exc:
            logger.warning("ML planning failed (%s), falling back to rules.", exc)
            return self._plan_rulebased(target, max_steps)

    def _plan_rulebased(self, target: str, max_steps: int) -> dict:
        """Rule-based retrosynthesis using SMARTS templates."""
        Chem = self._Chem
        if Chem is None:
            return {"routes": [], "best_route": None, "error": "RDKit not available."}

        mol = Chem.MolFromSmiles(target)
        if mol is None:
            return {"routes": [], "best_route": None, "error": f"Cannot parse SMILES: {target}"}

        all_routes = self._recursive_retro(mol, depth=0, max_depth=max_steps)

        if not all_routes:
            return {"routes": [], "best_route": None, "message": "No retrosynthetic disconnections found."}

        # Convert routes to expected format and score them
        formatted_routes = []
        for route_steps in all_routes:
            if not route_steps:  # Skip empty routes
                continue
            overall_score = sum(s.get("score", 0.5) for s in route_steps) / max(len(route_steps), 1)
            overall_score -= 0.05 * len(route_steps)  # penalize length
            formatted_routes.append({
                "steps": route_steps,
                "overall_score": overall_score,
            })

        formatted_routes.sort(key=lambda r: r["overall_score"], reverse=True)
        return {"routes": formatted_routes, "best_route": formatted_routes[0] if formatted_routes else None}

    def _recursive_retro(self, mol, depth: int, max_depth: int) -> list:
        """Recursively apply retro templates to generate routes."""
        if depth >= max_depth:
            return []

        Chem = self._Chem
        all_routes = []
        found = False

        # Sort templates by priority (highest first)
        sorted_templates = sorted(RETRO_TEMPLATES, key=lambda t: t[3], reverse=True)

        for name, retro_smarts, desc, priority in sorted_templates:
            try:
                rxn = _rxn_from_smarts(retro_smarts)
            except Exception:
                continue
            if rxn is None:
                continue
            try:
                ps = rxn.RunReactants((mol,))
            except Exception:
                continue
            for products in ps:
                # Check if all product molecules are valid
                valid = True
                product_smiles_list = []
                for p in products:
                    try:
                        Chem.SanitizeMol(p)
                        product_smiles_list.append(Chem.MolToSmiles(p))
                    except Exception:
                        valid = False
                        break
                if not valid or len(product_smiles_list) < 2:
                    continue

                found = True
                step = {
                    "product": Chem.MolToSmiles(mol),
                    "reactants": product_smiles_list,
                    "reaction_type": name,
                    "score": priority / 10.0,
                    "description": desc,
                }

                # Recursively plan for each reactant
                sub_routes = [[]]
                for smi in product_smiles_list:
                    sub_mol = Chem.MolFromSmiles(smi)
                    if sub_mol is None:
                        continue
                    deeper = self._recursive_retro(sub_mol, depth + 1, max_depth)
                    if deeper:
                        new_sub = []
                        for sr in deeper:
                            for existing in sub_routes:
                                new_sub.append(existing + sr)
                        sub_routes = new_sub if new_sub else sub_routes

                for sr in sub_routes:
                    all_routes.append([step] + sr)

        if not found:
            # Terminal node — commercial/available building block
            all_routes.append([])

        return all_routes

    # ------------------------------------------------------------------
    # 3. identify_disconnection_targets
    # ------------------------------------------------------------------
    def identify_disconnection_targets(self, smiles: str) -> list:
        """Identify strategic bonds to disconnect in a molecule.

        Parameters
        ----------
        smiles : str
            Input molecule SMILES.

        Returns
        -------
        list[dict]
            ``[{bond: str, strategy: str, expected_reactants: [str]}, ...]``
        """
        if not validate_smiles(smiles):
            return []

        Chem = self._Chem
        if Chem is None:
            return [{"bond": "unknown", "strategy": "error", "expected_reactants": [], "note": "RDKit not available"}]

        mol = Chem.MolFromSmiles(canonical_smiles(smiles))
        if mol is None:
            return []

        targets = []

        # Define substructure SMARTS and associated strategies
        # (pattern, bond_label, strategy, reactant_description)
        bond_patterns = [
            # Amide bonds (both aliphatic and aromatic N-substituents)
            ("[C:1](=[O:2])[N:3][C,c:4]", "amide C-N", "Amide hydrolysis / coupling",
             "carboxylic acid + amine"),
            # Ester bonds
            ("[C:1](=[O:2])[O:3][C:4]", "ester C-O", "Ester hydrolysis / transesterification",
             "carboxylic acid + alcohol"),
            # Aryl-O (phenolic ester)
            ("[C:1](=[O:2])[O:3][c:4]", "aryl-ester O-aryl", "Ester hydrolysis (aryl ester)",
             "carboxylic acid + phenol"),
            # Ether (alkyl-aryl)
            ("[c:1][O:2][C:3]", "aryl-O-alkyl ether", "Williamson ether synthesis / BBr3 cleavage",
             "aryl halide + alkoxide"),
            # Ether (alkyl-alkyl)
            ("[C:1][O:2][C:3]", "alkyl ether", "Williamson ether synthesis",
             "alkyl halide + alkoxide"),
            # C-C alpha to carbonyl (beta-keto or beta-hydroxy)
            ("[C:1](=[O:2])[CH2:3][C:4](=[O:5])", "C-C (β-dicarbonyl)", "Claisen condensation",
             "ester + ester enolate"),
            ("[C:1](=[O:2])[CH:3]([OH:4])[C:5]", "C-C (β-hydroxy carbonyl)", "Aldol reaction",
             "aldehyde/ketone + enolate"),
            ("[C:1](=[O:2])[C:3]=[C:4][C:5](=[O:6])", "C=C (α,β-unsaturated)", "Michael addition precursor",
             "Michael acceptor + nucleophile"),
            # Aryl-aryl
            ("[c:1]-[c:2]", "biaryl C-C", "Suzuki / Kumada / Negishi coupling",
             "aryl halide + aryl metal"),
            # C=C
            ("[C:1]=[C:2]", "alkene C=C", "Wittig / alkene metathesis / Diels-Alder",
             "aldehyde/ketone + ylide (Wittig)"),
            # Alkyl halide
            ("[C:1][Cl,Br,I:2]", "C-halogen", "SN2 / Grignard formation",
             "alcohol + HX / halogenation"),
            # Nitrile
            ("[C:1]#[N:2]", "nitrile C≡N", "Rosenmund-von Braun / dehydration of amide",
             "aryl halide + KCN (Rosenmund-von Braun)"),
            # Nitro
            ("[N+:1](=[O:2])[O-:3]", "nitro N-O", "Nitration reduction",
             "amine → nitro (reverse: nitro → amine)"),
        ]

        for smarts, bond_label, strategy, reactants_desc in bond_patterns:
            pat = Chem.MolFromSmarts(smarts)
            if pat is None:
                continue
            if mol.HasSubstructMatch(pat):
                matches = mol.GetSubstructMatches(pat)
                targets.append({
                    "bond": bond_label,
                    "strategy": strategy,
                    "expected_reactants": reactants_desc,
                    "num_matches": len(matches),
                    "smarts": smarts,
                })

        # Deduplicate by bond label
        seen = set()
        deduped = []
        for t in targets:
            if t["bond"] not in seen:
                seen.add(t["bond"])
                deduped.append(t)

        # Sort by strategic value (amide > ester > C-C bonds > etc.)
        priority = {"amide": 10, "aryl-ester": 9, "ester": 9, "biaryl": 8, "β-dicarbonyl": 8,
                     "β-hydroxy": 7, "alkene": 7, "aryl-O": 6, "alkyl ether": 5, "halogen": 4, "nitrile": 3, "nitro": 3}
        deduped.sort(key=lambda t: max(priority.get(k, 0) for k in priority if k.lower() in t["bond"].lower() or k.lower() in t["strategy"].lower()), reverse=True)

        return deduped

    # ------------------------------------------------------------------
    # 4. forward_reaction_predict
    # ------------------------------------------------------------------
    def forward_reaction_predict(self, reactant_smiles: list, conditions: str = "") -> dict:
        """Predict reaction products from reactants.

        Parameters
        ----------
        reactant_smiles : list[str]
            List of reactant SMILES strings.
        conditions : str
            Optional description of reaction conditions (e.g. ``"Grignard"``).

        Returns
        -------
        dict
            ``{
                products: [{smiles: str, reaction_type: str, description: str, score: float}],
                conditions_used: str
            }``
        """
        Chem = self._Chem
        if Chem is None:
            return {"products": [], "error": "RDKit not available."}

        # Validate all reactants
        valid_smiles = []
        for smi in reactant_smiles:
            if validate_smiles(smi):
                valid_smiles.append(canonical_smiles(smi))

        if len(valid_smiles) < 2:
            return {"products": [], "error": "Need at least 2 valid reactant SMILES."}

        mols = [Chem.MolFromSmiles(s) for s in valid_smiles]

        products = []

        # If conditions specified, try matching templates
        conditions_lower = conditions.lower().strip()
        if conditions_lower:
            matched_templates = []
            for name, templates in FORWARD_TEMPLATES.items():
                if conditions_lower in name.lower() or name.lower() in conditions_lower:
                    matched_templates.append((name, templates))
                # Partial keyword matching
                keywords = conditions_lower.replace(",", " ").replace("+", " ").split()
                for kw in keywords:
                    if kw and kw in name.lower():
                        matched_templates.append((name, templates))
                        break

            for name, templates in matched_templates:
                for smarts, desc in templates:
                    try:
                        rxn = _rxn_from_smarts(smarts)
                    except Exception:
                        continue
                    if rxn is None:
                        continue
                    try:
                        ps = rxn.RunReactants(tuple(mols))
                    except Exception:
                        continue
                    seen = set()
                    for product_tuple in ps:
                        for p in product_tuple:
                            try:
                                Chem.SanitizeMol(p)
                                smi = Chem.MolToSmiles(p)
                                if smi not in seen:
                                    seen.add(smi)
                                    products.append({
                                        "smiles": smi,
                                        "reaction_type": name,
                                        "description": desc,
                                        "score": 0.8,
                                    })
                            except Exception:
                                continue

        # If no conditions or no matches, try all templates
        if not products:
            for name, templates in FORWARD_TEMPLATES.items():
                for smarts, desc in templates:
                    try:
                        rxn = _rxn_from_smarts(smarts)
                    except Exception:
                        continue
                    if rxn is None:
                        continue
                    try:
                        ps = rxn.RunReactants(tuple(mols))
                    except Exception:
                        continue
                    seen = set()
                    for product_tuple in ps:
                        for p in product_tuple:
                            try:
                                Chem.SanitizeMol(p)
                                smi = Chem.MolToSmiles(p)
                                if smi not in seen:
                                    seen.add(smi)
                                    products.append({
                                        "smiles": smi,
                                        "reaction_type": name,
                                        "description": desc,
                                        "score": 0.5,
                                    })
                            except Exception:
                                continue

        # Also try combining all reactant SMILES into a reaction string
        if not products:
            combined_smi = ".".join(valid_smiles)
            products.append({
                "smiles": combined_smi,
                "reaction_type": "unknown",
                "description": "No matching template found. Reactants provided as-is.",
                "score": 0.0,
            })

        return {
            "products": products[:10],  # Limit output
            "conditions_used": conditions,
            "reactants": valid_smiles,
        }

    # ------------------------------------------------------------------
    # 5. suggest_synthesis_route
    # ------------------------------------------------------------------
    def suggest_synthesis_route(self, target_description: str) -> dict:
        """High-level synthesis suggestion from a text description.

        Attempts to resolve the description to a SMILES (via lookup table or
        RDKit name parsing), then runs retrosynthetic planning.

        Parameters
        ----------
        target_description : str
            Human-readable compound name or description.

        Returns
        -------
        dict
            ``{
                target: str,
                target_smiles: str,
                routes: [...],
                best_route: {...} | None,
                human_readable: str
            }``
        """
        # Try direct lookup
        smiles = self._name_to_smiles(target_description)

        if not smiles:
            # Try RDKit MolFromSmiles in case they passed SMILES directly
            if validate_smiles(target_description):
                smiles = canonical_smiles(target_description)

        if not smiles:
            return {
                "target": target_description,
                "target_smiles": None,
                "routes": [],
                "best_route": None,
                "human_readable": f"Could not resolve '{target_description}' to a known molecule. "
                                 f"Try a SMILES string or one of: {', '.join(sorted(_NAME_TO_SMILES.keys()))}",
            }

        result = self.plan_retrosynthesis(smiles)

        # Generate human-readable summary
        readable = f"Target: {target_description}\n"
        readable += f"SMILES: {smiles}\n\n"

        if result.get("best_route"):
            route = result["best_route"]
            readable += f"Best route ({len(route['steps'])} steps, score: {route['overall_score']:.2f}):\n"
            for i, step in enumerate(route["steps"], 1):
                readable += f"  Step {i}: {step.get('reaction_type', '?')}\n"
                readable += f"    Product: {step.get('product', '?')}\n"
                readable += f"    Reactants: {', '.join(step.get('reactants', []))}\n"
                if step.get('description'):
                    readable += f"    Method: {step['description']}\n"
                readable += "\n"
        elif result.get("routes"):
            readable += f"Found {len(result['routes'])} routes.\n"
        else:
            readable += "No retrosynthetic routes found.\n"

        # Also show disconnection targets
        disconnections = self.identify_disconnection_targets(smiles)
        if disconnections:
            readable += "\nStrategic disconnections:\n"
            for d in disconnections:
                readable += f"  - {d['bond']}: {d['strategy']} → {d['expected_reactants']}\n"

        return {
            "target": target_description,
            "target_smiles": smiles,
            "routes": result.get("routes", []),
            "best_route": result.get("best_route"),
            "human_readable": readable,
        }

    @staticmethod
    def _name_to_smiles(name: str) -> Optional[str]:
        """Look up a compound name in the built-in dictionary."""
        name_clean = name.strip().lower()
        # Exact match
        if name_clean in _NAME_TO_SMILES:
            return _NAME_TO_SMILES[name_clean]
        # Partial match
        for k, v in _NAME_TO_SMILES.items():
            if name_clean in k or k in name_clean:
                return v
        return None


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    planner = RetrosynthesisPlanner()
    planner.setup()

    target = "aspirin" if len(sys.argv) < 2 else sys.argv[1]
    smiles_arg = "CC(=O)Oc1ccccc1C(=O)O" if target == "aspirin" else target

    print("=" * 60)
    print(f"Retrosynthesis Tool — Target: {target}")
    print("=" * 60)

    # 1. Suggest synthesis route
    print("\n[1] suggest_synthesis_route:")
    route = planner.suggest_synthesis_route(target)
    print(route["human_readable"])

    # 2. Plan retrosynthesis
    print("\n[2] plan_retrosynthesis:")
    if validate_smiles(smiles_arg):
        result = planner.plan_retrosynthesis(smiles_arg, max_steps=4)
        print(f"  Routes found: {len(result.get('routes', []))}")
        if result.get("best_route"):
            for i, step in enumerate(result["best_route"]["steps"], 1):
                print(f"  Step {i}: {step['reaction_type']} → {', '.join(step['reactants'])}")
    else:
        print(f"  Invalid SMILES: {smiles_arg}")

    # 3. Disconnection targets
    print("\n[3] identify_disconnection_targets:")
    disc = planner.identify_disconnection_targets("CC(=O)Oc1ccccc1C(=O)O")
    for d in disc:
        print(f"  {d['bond']}: {d['strategy']}")

    # 4. Forward prediction
    print("\n[4] forward_reaction_predict (esterification):")
    fwd = planner.forward_reaction_predict(["CC(=O)O", "OCc1ccccc1"], conditions="Esterification")
    for p in fwd.get("products", []):
        print(f"  {p['reaction_type']}: {p['smiles']}")

    print("\n[OK] Done.")
