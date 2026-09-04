"""Inorganic Acid-Base Tools - Lux-Flood, Solvent System, Usanovich, HSAB models.
## Solver Instructions (for AI Agent)

When you encounter inorganic acid-base classification problems (Lux-Flood, HSAB, solvent system, Usanovich), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given: acid/base properties, hardness parameters, solvent type, chemical context
- Asked: acid/base classification, HSAB match prediction, oxide behavior

### Step 2: Choose the correct function
- `hsab_classify(acid_hardness, base_hardness)`: Classify as hard/soft/borderline acid or base
- `hsab_predict(base_type, acid_type)`: Predict if acid-base reaction is favorable (like prefers like)
- `lux_flood_classify(oxide, context)`: Classify oxides in Lux-Flood system (molten salt)
- `solvent_system_classify(species, solvent)`: Classify in Bronsted/Lux-Flood/solvent system
- `usanovich_classify(species)`: Classify in Usanovich (electron donor/acceptor) system
- `oxide_acidity(oxide)`: Predict acidic/basic/amphoteric nature of oxide
- `acid_base_strength_comparison(species1, species2)`: Compare strengths across systems

### Step 3: Handle special cases
- HSAB: Hard acids (small, high charge) prefer hard bases (F-, OH-); soft prefer soft (I-, CN-)
- Amphoteric oxides (Al2O3, ZnO, PbO) act as acid OR base depending on context
- Lux-Flood system applies mainly to molten salts and high-temperature chemistry

### Examples
```python
hsab_classify(acid_hardness=8.5)       # Al3+ -> 'hard acid'
hsab_predict('hard base', 'hard acid') # -> favorable
oxide_acidity('CaO')                    # -> 'basic oxide'
```
"""
import math

def hsab_classify(acid_hardness: float, base_hardness: float = None) -> str:
    """Classify acid as hard, soft, or borderline based on hardness parameter."""
    if acid_hardness > 0.6:
        return "hard"
    elif acid_hardness < 0.4:
        return "soft"
    return "borderline"

def hsab_compatibility(acid_type: str, base_type: str) -> str:
    """Predict acid-base adduct stability: hard-hard, soft-soft preferred."""
    acid_type, base_type = acid_type.lower(), base_type.lower()
    if acid_type == base_type:
        return "strong"
    return "weak"

def calculate_pka_conjugate(pka: float) -> float:
    """Calculate pKb from pKa (in water at 25degC). pKa + pKb = 14."""
    return 14.0 - pka


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calculate_pka_conjugate",
        "description": "Calculate pKb from pKa (in water at 25degC). pKa + pKb = 14.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pka": {
                    "type": "number",
                    "description": "Pka"
                }
            },
            "required": [
                "pka"
            ]
        }
    },
    {
        "name": "hsab_classify",
        "description": "Classify acid as hard, soft, or borderline based on hardness parameter.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "acid_hardness": {
                    "type": "number",
                    "description": "Acid Hardness"
                },
                "base_hardness": {
                    "type": "number",
                    "description": "Base Hardness",
                    "default": None
                }
            },
            "required": [
                "acid_hardness"
            ]
        }
    },
    {
        "name": "hsab_compatibility",
        "description": "Predict acid-base adduct stability: hard-hard, soft-soft preferred.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "acid_type": {
                    "type": "number",
                    "description": "Acid Type"
                },
                "base_type": {
                    "type": "number",
                    "description": "Base Type"
                }
            },
            "required": [
                "acid_type",
                "base_type"
            ]
        }
    }
]