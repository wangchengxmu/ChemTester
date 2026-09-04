"""
Protecting Groups Tools (L3 Implementation)
Tools for selecting and managing protecting groups in multi-step synthesis.

## Solver Instructions (for AI Agent)

When you encounter protecting group selection, orthogonality checking, multi-protection planning, or stability analysis problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a functional group and reaction conditions -> select appropriate protecting group?
- Given multiple protecting groups -> check orthogonality (can they be removed independently)?
- Given multiple functional groups needing protection -> create comprehensive protection plan?
- Given protecting group list -> generate stability matrix against common conditions?

### Step 2: Choose the correct function
- **PG selection:** `pg_selection(functional_group, conditions, priority='stability')` -> recommended PG with alternatives and rationale. Groups: alcohol, amine, carboxylic_acid, aldehyde, ketone, phenol, thiol. Priorities: 'stability', 'yield', 'removal_ease'
- **Orthogonality check:** `orthogonality_check(pg_list)` -> is_orthogonal bool, removal_order, conflicts (shared deprotection conditions). Example: ['Boc', 'Bn', 'TBDMS'] -> orthogonal (acid/base/F-)
- **Multi-protection plan:** `multi_protection_plan(functional_groups, synthesis_conditions)` -> complete plan with protection steps, deprotection steps, and orthogonality analysis. functional_groups = {'alcohol': ['Grignard'], 'amine': ['acid']}
- **Stability matrix:** `pg_stability_matrix(pg_list)` -> matrix showing stable/unstable for each PG under acid, base, reduction, oxidation, etc.

### Step 3: Handle special cases
- Boc (acid-labile) + Fmoc (base-labile) + TBDMS (F-labile) = classic orthogonal set
- Bn (hydrogenolysis) survives acid and base - good for multi-step syntheses
- TMS is very labile (removed by water!) - use only for temporary protection
- Check for SHARED deprotection conditions between PGs -> these are conflicts

### Examples
```python
# Example 1: Protect alcohol under basic/Grignard conditions
pg_selection('alcohol', ['base', 'reduction'])  -> recommended: TBDMS (stable to both)

# Example 2: Check orthogonality of Boc, Fmoc, TBDMS
orthogonality_check(['Boc', 'Fmoc', 'TBDMS'])  -> is_orthogonal: True (acid/base/F- are orthogonal)

# Example 3: Plan protection for alcohol (needs Grignard) and amine (needs acid)
multi_protection_plan({'alcohol': ['Grignard'], 'amine': ['acid']}, ['Grignard', 'acid'])

# Example 4: Stability matrix for TBDMS and TMS
pg_stability_matrix(['TBDMS', 'TMS'])  -> TBDMS stable to base/mild_acid/reduction; TMS only stable to neutral
```
"""

from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class FunctionalGroup(Enum):
    """Common functional groups requiring protection."""
    ALCOHOL = "alcohol"
    AMINE = "amine"
    CARBOXYLIC_ACID = "carboxylic_acid"
    ALDEHYDE = "aldehyde"
    KETONE = "ketone"
    PHENOL = "phenol"
    THIOL = "thiol"
    PHOSPHATE = "phosphate"


class ProtectionType(Enum):
    """Types of protection strategies."""
    ACYL = "acyl"
    ETHER = "ether"
    SILYL = "silyl"
    ACETAL = "acetal"
    KETAL = "ketal"
    CARBAMATE = "carbamate"
    SULFONAMIDE = "sulfonamide"


@dataclass
class ProtectingGroup:
    """Data structure for protecting group information."""
    name: str
    abbreviation: str
    protection_type: ProtectionType
    stability_conditions: List[str]
    deprotection_conditions: List[str]
    typical_yield: float
    commercial_availability: bool = True


# Protecting group database
PROTECTING_GROUPS = {
    # Alcohol protecting groups
    "TBDMS": ProtectingGroup(
        name="tert-Butyldimethylsilyl",
        abbreviation="TBDMS",
        protection_type=ProtectionType.SILYL,
        stability_conditions=["base", "mild_acid", "reduction"],
        deprotection_conditions=["TBAF", "HF", "HCl/MeOH"],
        typical_yield=0.90
    ),
    "TBDPS": ProtectingGroup(
        name="tert-Butyldiphenylsilyl",
        abbreviation="TBDPS",
        protection_type=ProtectionType.SILYL,
        stability_conditions=["base", "acid", "reduction"],
        deprotection_conditions=["TBAF", "HF"],
        typical_yield=0.85
    ),
    "TMS": ProtectingGroup(
        name="Trimethylsilyl",
        abbreviation="TMS",
        protection_type=ProtectionType.SILYL,
        stability_conditions=["neutral"],
        deprotection_conditions=["mild_acid", "water", "F-"],
        typical_yield=0.95
    ),
    "THP": ProtectingGroup(
        name="Tetrahydropyranyl",
        abbreviation="THP",
        protection_type=ProtectionType.ETHER,
        stability_conditions=["base", "reduction"],
        deprotection_conditions=["acid", "PPTS/MeOH"],
        typical_yield=0.85
    ),
    "MOM": ProtectingGroup(
        name="Methoxymethyl",
        abbreviation="MOM",
        protection_type=ProtectionType.ETHER,
        stability_conditions=["base", "reduction"],
        deprotection_conditions=["acid", "BCl3", "BBr3"],
        typical_yield=0.80
    ),
    "Bn": ProtectingGroup(
        name="Benzyl",
        abbreviation="Bn",
        protection_type=ProtectionType.ETHER,
        stability_conditions=["base", "acid", "mild_reduction"],
        deprotection_conditions=["H2/Pd", "Na/NH3", "BCl3"],
        typical_yield=0.90
    ),
    "Ac": ProtectingGroup(
        name="Acetyl",
        abbreviation="Ac",
        protection_type=ProtectionType.ACYL,
        stability_conditions=["acid"],
        deprotection_conditions=["base", "K2CO3/MeOH"],
        typical_yield=0.95
    ),
    "Bz": ProtectingGroup(
        name="Benzoyl",
        abbreviation="Bz",
        protection_type=ProtectionType.ACYL,
        stability_conditions=["acid"],
        deprotection_conditions=["base", "NH3/MeOH"],
        typical_yield=0.90
    ),
    # Amine protecting groups
    "Boc": ProtectingGroup(
        name="tert-Butyloxycarbonyl",
        abbreviation="Boc",
        protection_type=ProtectionType.CARBAMATE,
        stability_conditions=["base", "reduction"],
        deprotection_conditions=["TFA", "HCl/dioxane"],
        typical_yield=0.90
    ),
    "Fmoc": ProtectingGroup(
        name="9-Fluorenylmethoxycarbonyl",
        abbreviation="Fmoc",
        protection_type=ProtectionType.CARBAMATE,
        stability_conditions=["acid"],
        deprotection_conditions=["piperidine", "DBU"],
        typical_yield=0.85
    ),
    "Cbz": ProtectingGroup(
        name="Benzyloxycarbonyl",
        abbreviation="Cbz",
        protection_type=ProtectionType.CARBAMATE,
        stability_conditions=["acid", "base"],
        deprotection_conditions=["H2/Pd", "HBr"],
        typical_yield=0.85
    ),
    "Tos": ProtectingGroup(
        name="Tosyl",
        abbreviation="Tos",
        protection_type=ProtectionType.SULFONAMIDE,
        stability_conditions=["acid", "base", "reduction"],
        deprotection_conditions=["Na/NH3", "HBr/HOAc"],
        typical_yield=0.80
    ),
    # Carbonyl protecting groups
    "acetal": ProtectingGroup(
        name="Acetal (dimethyl)",
        abbreviation="acetal",
        protection_type=ProtectionType.ACETAL,
        stability_conditions=["base", "reduction"],
        deprotection_conditions=["acid", "HCl/H2O"],
        typical_yield=0.85
    ),
    "dioxolane": ProtectingGroup(
        name="1,3-Dioxolane",
        abbreviation="dioxolane",
        protection_type=ProtectionType.ACETAL,
        stability_conditions=["base", "reduction"],
        deprotection_conditions=["acid", "HCl/H2O"],
        typical_yield=0.80
    ),
}


def pg_selection(functional_group: str, 
                 conditions: List[str],
                 priority: str = "stability") -> Dict[str, Any]:
    """
    Select appropriate protecting group based on functional group and reaction conditions.
    
    Args:
        functional_group: The functional group to protect (e.g., 'alcohol', 'amine')
        conditions: List of reaction conditions the PG must survive (e.g., ['base', 'acid'])
        priority: Selection priority - 'stability', 'yield', or 'removal_ease'
    
    Returns:
        Dictionary with recommended protecting groups and selection rationale
    
    Example:
        >>> pg_selection('alcohol', ['base', 'reduction'])
        {'recommended': 'TBDMS', 'alternatives': [...], 'rationale': '...'}
    """
    # Map functional groups to applicable protecting group types
    fg_pg_map = {
        "alcohol": ["TBDMS", "TBDPS", "TMS", "THP", "MOM", "Bn", "Ac", "Bz"],
        "amine": ["Boc", "Fmoc", "Cbz", "Tos"],
        "carboxylic_acid": ["methyl_ester", "ethyl_ester", "t-butyl_ester"],
        "aldehyde": ["acetal", "dioxolane"],
        "ketone": ["acetal", "dioxolane", "ketal"],
        "phenol": ["MOM", "Bn", "Ac", "TBDMS"],
        "thiol": ["Ac", "Bn", "Tr"],
    }
    
    functional_group = functional_group.lower().replace(" ", "_")
    
    if functional_group not in fg_pg_map:
        return {
            "error": f"Unknown functional group: {functional_group}",
            "available_groups": list(fg_pg_map.keys())
        }
    
    candidates = fg_pg_map[functional_group]
    
    # Score each protecting group
    scored_candidates = []
    
    for pg_abbr in candidates:
        if pg_abbr not in PROTECTING_GROUPS:
            continue
        
        pg = PROTECTING_GROUPS[pg_abbr]
        
        # Calculate stability score
        stability_score = 0
        for condition in conditions:
            if condition.lower() in pg.stability_conditions:
                stability_score += 1
        
        stability_pct = stability_score / len(conditions) if conditions else 0.5
        
        # Score based on priority
        if priority == "stability":
            score = stability_pct
        elif priority == "yield":
            score = pg.typical_yield
        elif priority == "removal_ease":
            # Fewer deprotection conditions = easier removal
            score = 1.0 / len(pg.deprotection_conditions)
        else:
            score = (stability_pct + pg.typical_yield) / 2
        
        scored_candidates.append({
            "abbreviation": pg_abbr,
            "name": pg.name,
            "score": round(score, 3),
            "stability_score": round(stability_pct, 2),
            "typical_yield": pg.typical_yield,
            "deprotection_conditions": pg.deprotection_conditions,
            "survives_conditions": stability_score == len(conditions)
        })
    
    # Sort by score
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # Get recommended and alternatives
    recommended = scored_candidates[0] if scored_candidates else None
    alternatives = scored_candidates[1:4] if len(scored_candidates) > 1 else []
    
    return {
        "functional_group": functional_group,
        "conditions": conditions,
        "recommended": recommended,
        "alternatives": alternatives,
        "selection_priority": priority
    }


def orthogonality_check(pg_list: List[str]) -> Dict[str, Any]:
    """
    Check protecting group orthogonality for multi-step synthesis.
    
    Orthogonality means that each PG can be removed selectively without
    affecting the others.
    
    Args:
        pg_list: List of protecting group abbreviations (e.g., ['Boc', 'Bn', 'TBDMS'])
    
    Returns:
        Dictionary with orthogonality analysis and removal order recommendations
    
    Example:
        >>> orthogonality_check(['Boc', 'Bn', 'TBDMS'])
        {'is_orthogonal': True, 'removal_order': [...], 'conflicts': []}
    """
    if not pg_list:
        return {
            "is_orthogonal": True,
            "removal_order": [],
            "conflicts": [],
            "warnings": []
        }
    
    # Validate PGs exist
    valid_pgs = []
    warnings = []
    
    for pg_abbr in pg_list:
        if pg_abbr in PROTECTING_GROUPS:
            valid_pgs.append((pg_abbr, PROTECTING_GROUPS[pg_abbr]))
        else:
            warnings.append(f"Unknown protecting group: {pg_abbr}")
    
    if not valid_pgs:
        return {
            "is_orthogonal": False,
            "removal_order": [],
            "conflicts": [],
            "warnings": warnings
        }
    
    # Check for conflicts (same deprotection conditions)
    conflicts = []
    
    for i, (pg1_abbr, pg1) in enumerate(valid_pgs):
        for pg2_abbr, pg2 in valid_pgs[i+1:]:
            common_deprotection = set(pg1.deprotection_conditions) & set(pg2.deprotection_conditions)
            if common_deprotection:
                conflicts.append({
                    "pg1": pg1_abbr,
                    "pg2": pg2_abbr,
                    "shared_conditions": list(common_deprotection),
                    "severity": "high" if len(common_deprotection) > 1 else "medium"
                })
    
    # Determine if orthogonal
    is_orthogonal = len(conflicts) == 0
    
    # Suggest removal order based on deprotection conditions
    removal_order = _suggest_removal_order(valid_pgs, conflicts)
    
    return {
        "is_orthogonal": is_orthogonal,
        "removal_order": removal_order,
        "conflicts": conflicts,
        "warnings": warnings,
        "pg_details": [
            {
                "abbreviation": pg_abbr,
                "deprotection_conditions": pg.deprotection_conditions
            }
            for pg_abbr, pg in valid_pgs
        ]
    }


def _suggest_removal_order(pgs: List[Tuple[str, ProtectingGroup]], 
                            conflicts: List[Dict]) -> List[Dict[str, Any]]:
    """Suggest an optimal removal order for protecting groups."""
    
    # Priority based on deprotection condition specificity
    # More specific (fewer options) should be removed first
    removal_order = []
    
    for pg_abbr, pg in pgs:
        # Calculate specificity score (lower = more specific = remove earlier)
        specificity = len(pg.deprotection_conditions)
        
        # Check if this PG is in conflicts
        in_conflict = any(
            c["pg1"] == pg_abbr or c["pg2"] == pg_abbr 
            for c in conflicts
        )
        
        removal_order.append({
            "pg": pg_abbr,
            "specificity": specificity,
            "in_conflict": in_conflict,
            "deprotection_conditions": pg.deprotection_conditions,
            "priority": 1 if in_conflict else specificity  # Conflicts get high priority
        })
    
    # Sort by priority (lower first)
    removal_order.sort(key=lambda x: x["priority"])
    
    return removal_order


def multi_protection_plan(functional_groups: Dict[str, List[str]], 
                          synthesis_conditions: List[str]) -> Dict[str, Any]:
    """
    Create a comprehensive protection plan for multiple functional groups.
    
    Args:
        functional_groups: Dict mapping FG names to their required protection conditions
        synthesis_conditions: Overall reaction conditions for the synthesis
    
    Returns:
        Complete protection/deprotection plan with orthogonality analysis
    
    Example:
        >>> multi_protection_plan(
        ...     {'alcohol': ['base'], 'amine': ['acid']},
        ...     ['base', 'Grignard']
        ... )
    """
    plan = {
        "functional_groups": {},
        "protection_steps": [],
        "deprotection_steps": [],
        "orthogonality": None,
        "issues": []
    }
    
    selected_pgs = []
    
    for fg, fg_conditions in functional_groups.items():
        # Get recommended PG for this functional group
        selection = pg_selection(fg, synthesis_conditions + fg_conditions)
        
        if "error" in selection:
            plan["issues"].append(selection["error"])
            continue
        
        recommended = selection.get("recommended")
        if recommended:
            plan["functional_groups"][fg] = recommended
            selected_pgs.append(recommended["abbreviation"])
            
            plan["protection_steps"].append({
                "step": f"Protect {fg}",
                "pg": recommended["abbreviation"],
                "conditions": recommended.get("deprotection_conditions", [])
            })
    
    # Check orthogonality
    if selected_pgs:
        ortho = orthogonality_check(selected_pgs)
        plan["orthogonality"] = ortho
        
        # Add deprotection steps in suggested order
        for removal in ortho.get("removal_order", []):
            plan["deprotection_steps"].append({
                "step": f"Deprotect {removal['pg']}",
                "conditions": removal["deprotection_conditions"]
            })
    
    return plan


def pg_stability_matrix(pg_list: List[str]) -> Dict[str, Any]:
    """
    Generate a stability matrix for given protecting groups.
    
    Shows which conditions each PG survives or fails under.
    """
    conditions = ["acid", "base", "reduction", "oxidation", "mild_acid", "mild_base", "neutral"]
    
    matrix = {}
    
    for pg_abbr in pg_list:
        if pg_abbr not in PROTECTING_GROUPS:
            continue
        
        pg = PROTECTING_GROUPS[pg_abbr]
        matrix[pg_abbr] = {}
        
        for condition in conditions:
            # Check if condition is in stability_conditions
            is_stable = condition.lower() in pg.stability_conditions
            matrix[pg_abbr][condition] = "stable" if is_stable else "unstable"
    
    return {
        "conditions": conditions,
        "matrix": matrix
    }


# Example usage and testing
if __name__ == "__main__":
    # Test PG selection
    print("=== PG Selection Test ===")
    result = pg_selection("alcohol", ["base", "reduction"])
    print(f"Recommended PG for alcohol under base/reduction: {result['recommended']}")
    
    # Test orthogonality
    print("\n=== Orthogonality Check Test ===")
    result = orthogonality_check(["Boc", "Bn", "TBDMS"])
    print(f"Is orthogonal: {result['is_orthogonal']}")
    print(f"Removal order: {[r['pg'] for r in result['removal_order']]}")
    
    # Test multi-protection plan
    print("\n=== Multi-Protection Plan Test ===")
    fgs = {
        "alcohol": ["Grignard"],
        "amine": ["acid"]
    }
    result = multi_protection_plan(fgs, ["Grignard", "acid"])
    print(f"Selected PGs: {result['functional_groups']}")
    print(f"Orthogonal: {result['orthogonality']['is_orthogonal']}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="multi_protection_plan",
            description="Create a comprehensive protection plan for multiple functional groups.",
            input_schema=[
            InputSchemaField(name="functional_groups", type="number", required=True),
            InputSchemaField(name="synthesis_conditions", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="orthogonality_check",
            description="Check protecting group orthogonality for multi-step synthesis.",
            input_schema=[
            InputSchemaField(name="pg_list", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pg_selection",
            description="Select appropriate protecting group based on functional group and reaction conditions.",
            input_schema=[
            InputSchemaField(name="functional_group", type="number", required=True),
            InputSchemaField(name="conditions", type="number", required=True),
            InputSchemaField(name="priority", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="pg_stability_matrix",
            description="Generate a stability matrix for given protecting groups.",
            input_schema=[
            InputSchemaField(name="pg_list", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
