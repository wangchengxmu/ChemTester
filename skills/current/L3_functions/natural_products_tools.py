"""
L3 Tool: Natural Products Tools
Terpene classification, biosynthetic pathway calculations, yield optimization.

Source: Roberts & Caserio Ch30, LibreTexts Organic Chemistry III
Created: 2026-03-24 (Phase 2)

## Solver Instructions (for AI Agent)

When you encounter natural products problems (terpenes, biosynthesis, total synthesis), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given isoprene units -> calculate carbon count and terpene class?
- Given target carbons -> calculate biosynthetic cost (acetyl-CoA, ATP)?
- Given step yields -> calculate overall synthesis yield?
- Given molecular formula -> calculate MW or degrees of unsaturation?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Terpene carbon count | `terpene_carbon_count(isoprene_units)` | C = 5 x n (n = isoprene units) |
| Mevalonate pathway cost | `mevalonate_pathway_cost(target_carbons)` | Returns acetyl-CoA, ATP needed |
| Overall synthesis yield | `overall_synthesis_yield(step_yields)` | Overall = Π(yieldᵢ) |
| Molecular weight | `mw_from_formula(formula)` | Parses formula string |
| Degrees of unsaturation | `degree_of_unsaturation(formula)` | DoU = (2C+2+N-H-X)/2 |

### Step 3: Handle special cases
- Terpene classes: 2 units=monoterpene(C10), 3=sesquiterpene(C15), 4=diterpene(C20)
- Mevalonate pathway: 3 Acetyl-CoA + 3 ATP per IPP unit
- DoU: rings count as 1, triple bonds count as 2

### Examples
```python
# Example 1: Monoterpene carbon count
terpene_carbon_count(2)
# -> {'carbons': 10, 'class': 'Monoterpene'}

# Example 2: Biosynthetic cost for C20 terpene
mevalonate_pathway_cost(20)
# -> {'ipp_required': 4, 'acetyl_coa_required': 12, 'atp_required': 12}

# Example 3: Overall synthesis yield
overall_synthesis_yield([0.85, 0.90, 0.75, 0.80])
# -> {'overall_yield': 0.459, 'overall_yield_pct': 45.9%}

# Example 4: Degrees of unsaturation
degree_of_unsaturation('C10H12O')
# -> {'dou': 5, 'interpretation': '5 rings + pi bonds'}
```
"""

import math


def terpene_carbon_count(isoprene_units: int) -> dict:
    """Calculate terpene carbon count from isoprene units.
    
    C_n = 5 x n (where n = number of isoprene units)
    """
    if isoprene_units <= 0:
        return {'error': 'Isoprene units must be positive'}
    carbons = 5 * isoprene_units
    classes = {2: 'Monoterpene', 3: 'Sesquiterpene', 4: 'Diterpene',
               6: 'Triterpene', 8: 'Tetraterpene'}
    return {
        'carbons': carbons,
        'isoprene_units': isoprene_units,
        'class': classes.get(isoprene_units, 'Polyterpene'),
        'formula_prefix': f'C{carbons}'
    }


def mevalonate_pathway_cost(target_carbons: int) -> dict:
    """Calculate acetyl-CoA and ATP cost for terpenoid biosynthesis via MVA pathway.
    
    2 Acetyl-CoA -> 1 IPP (costs: 3 Acetyl-CoA total per IPP + 2 ATP)
    Actually: 3 Acetyl-CoA -> Mevalonate (1 ATP already) -> IPP (2 ATP more) = 3 Acetyl-CoA + 3 ATP per IPP
    """
    if target_carbons % 5 != 0:
        return {'error': 'Carbons must be multiple of 5 for isoprenoid'}
    n_ipp = target_carbons // 5
    acetyl_coa = 3 * n_ipp
    atp = 3 * n_ipp
    return {
        'target_carbons': target_carbons,
        'ipp_required': n_ipp,
        'acetyl_coa_required': acetyl_coa,
        'atp_required': atp,
        'terpene_class': {2: 'Monoterpene', 3: 'Sesquiterpene', 4: 'Diterpene'}.get(n_ipp // 2, f'C{target_carbons}')
    }


def overall_synthesis_yield(step_yields: list) -> dict:
    """Calculate overall yield for multi-step total synthesis.
    
    Overall = Π(yield_i)
    """
    overall = 1.0
    for y in step_yields:
        if y <= 0 or y > 1:
            return {'error': f'Invalid yield: {y}'}
        overall *= y
    return {
        'overall_yield': round(overall, 8),
        'overall_yield_pct': round(overall * 100, 4),
        'num_steps': len(step_yields),
        'steps': [f'Step {i+1}: {round(y*100,1)}%' for i, y in enumerate(step_yields)]
    }


def mw_from_formula(formula: str) -> dict:
    """Parse simple molecular formula and calculate MW.
    Supports: C, H, O, N, S, P, Cl, Br, F, I, Na, K
    """
    import re
    atomic_weights = {'C': 12.011, 'H': 1.008, 'O': 15.999, 'N': 14.007,
                      'S': 32.06, 'P': 30.974, 'Cl': 35.45, 'Br': 79.904,
                      'F': 18.998, 'I': 126.904, 'Na': 22.990, 'K': 39.098}
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)
    mw = 0
    for element, count_str in matches:
        if element not in atomic_weights:
            return {'error': f'Unknown element: {element}'}
        count = int(count_str) if count_str else 1
        mw += atomic_weights[element] * count
    return {'formula': formula, 'mw': round(mw, 4)}


def degree_of_unsaturation(formula: str) -> dict:
    """Calculate degrees of unsaturation (rings + double bonds + triple bonds counted as 2).
    
    DoU = (2C + 2 + N - H - X) / 2  where X = halogens
    """
    import re
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)
    c = h = n = x = 0
    for element, count_str in matches:
        count = int(count_str) if count_str else 1
        if element == 'C': c = count
        elif element == 'H': h = count
        elif element == 'N': n = count
        elif element in ('F', 'Cl', 'Br', 'I'): x += count
    if c == 0:
        return {'error': 'No carbon found'}
    dou = (2 * c + 2 + n - h - x) / 2
    return {'formula': formula, 'DoU': dou, 'C': c, 'H': h, 'N': n, 'X': x}


TEXTBOOK_PROBLEMS = {
    "terpene_class": "A compound with 30 carbons and 6 isoprene units is a triterpene",
    "dou_steroid": "Cholesterol C27H46O: DoU = (54+2+0-46-0)/2 = 5",
}


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="degree_of_unsaturation",
            description="Calculate degrees of unsaturation (rings + double bonds + triple bonds counted as 2).",
            input_schema=[
            InputSchemaField(name="formula", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mevalonate_pathway_cost",
            description="Calculate acetyl-CoA and ATP cost for terpenoid biosynthesis via MVA pathway.",
            input_schema=[
            InputSchemaField(name="target_carbons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="mw_from_formula",
            description="Parse simple molecular formula and calculate MW.",
            input_schema=[
            InputSchemaField(name="formula", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="overall_synthesis_yield",
            description="Calculate overall yield for multi-step total synthesis.",
            input_schema=[
            InputSchemaField(name="step_yields", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="terpene_carbon_count",
            description="Calculate terpene carbon count from isoprene units.",
            input_schema=[
            InputSchemaField(name="isoprene_units", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
