"""
L3 Tool: Pericyclic Reaction Tools
Predict stereochemistry and allowedness of pericyclic reactions.

Source: Organic Chemistry (OpenStax) Ch30
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter pericyclic reaction problems - electrocyclic ring closure/opening, cycloaddition allowedness, sigmatropic rearrangement, or TECA mnemonic application - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given number of pi electrons and thermal/photochemical -> predict electrocyclic stereochemistry (conrotatory/disrotatory)?
- Given total pi electrons and conditions -> is cycloaddition symmetry-allowed?
- Given [i,j] sigmatropic indices and conditions -> is it allowed? What geometry?
- Need a quick mnemonic-based prediction?

### Step 2: Choose the correct function
- **Electrocyclic stereochemistry:** `electrocyclic_stereochemistry(n_electrons, thermal=True)` -> 'conrotatory' or 'disrotatory'. 4n: thermal->conrotatory, photo->disrotatory. 4n+2: thermal->disrotatory, photo->conrotatory
- **Cycloaddition allowedness:** `cycloaddition_allowed(n_electrons, thermal=True)` -> allowed bool and geometry ('suprafacial'/'antarafacial'). 6e- thermal: suprafacial (allowed). 4e- thermal: antarafacial (geometrically difficult)
- **Sigmatropic allowedness:** `sigmatropic_allowed(i, j, thermal=True)` -> uses i+j sum. [3,3]: 6 total -> 4n+2 -> thermal suprafacial (allowed, e.g., Cope rearrangement). [1,5]: 6 -> allowed
- **TECA mnemonic:** `teca_predict(n_electron_pairs, thermal=True)` -> 'T'hermal + 'E'ven -> 'C'onrotatory/'A'ntarafacial. Takes ELECTRON PAIRS not electrons. 4n electrons = 2n pairs (even); 4n+2 = odd pairs

### Step 3: Handle special cases
- 4n+2 thermal cycloadditions (like Diels-Alder, [4+2]) are always suprafacial and allowed
- 4n thermal cycloadditions ([2+2]) are antarafacial -> geometrically very difficult
- [3,3]-sigmatropic (Cope, Claisen) are the most common sigmatropic rearrangements
- TECA works for ALL pericyclic reactions - just count electron pairs (not electrons)

### Examples
```python
# Example 1: Thermal cyclization of butadiene (4pi e-)
electrocyclic_stereochemistry(4, thermal=True)  -> 'conrotatory'

# Example 2: Is Diels-Alder [4+2] thermally allowed?
cycloaddition_allowed(6, thermal=True)  -> {'allowed': True, 'geometry': 'suprafacial'}

# Example 3: [3,3]-sigmatropic (Cope rearrangement)
sigmatropic_allowed(3, 3, thermal=True)  -> {'allowed': True, 'geometry': 'suprafacial'}

# Example 4: TECA for 2 electron pairs (4pi e-), thermal
teca_predict(2, thermal=True)  -> 'conrotatory or antarafacial'
```
"""


def electrocyclic_stereochemistry(n_electrons: int, thermal: bool = True) -> dict:
    """
    Predict electrocyclic ring closure stereochemistry.
    
    TECA Rule: Thermal + Even -> Conrotatory
    
    For 4n electrons (even electron pairs):
        Thermal: Conrotatory
        Photochemical: Disrotatory
    
    For 4n+2 electrons (odd electron pairs):
        Thermal: Disrotatory
        Photochemical: Conrotatory
    
    Args:
        n_electrons: Number of pi electrons (4, 6, 8, etc.)
        thermal: True for thermal, False for photochemical
    
    Returns:
        Dictionary with stereochemistry prediction
    
    Example:
        >>> electrocyclic_stereochemistry(4, thermal=True)
        {'stereochemistry': 'conrotatory'}
    """
    # Determine if electron count is 4n or 4n+2
    is_4n = (n_electrons % 4 == 0)
    
    # Apply TECA rules
    if is_4n:  # Even number of electron pairs
        if thermal:
            stereochemistry = 'conrotatory'
        else:
            stereochemistry = 'disrotatory'
    else:  # 4n+2 electrons (odd electron pairs)
        if thermal:
            stereochemistry = 'disrotatory'
        else:
            stereochemistry = 'conrotatory'
    
    return {
        'n_electrons': n_electrons,
        'thermal': thermal,
        'stereochemistry': stereochemistry,
        'electron_pair_type': '4n' if is_4n else '4n+2'
    }


def cycloaddition_allowed(n_electrons: int, thermal: bool = True) -> dict:
    """
    Determine if cycloaddition is symmetry-allowed.
    
    TECA Rule: Thermal + Even -> Antarafacial
    
    For 4n electrons:
        Thermal: Antarafacial (geometrically difficult)
        Photochemical: Suprafacial (allowed)
    
    For 4n+2 electrons:
        Thermal: Suprafacial (allowed)
        Photochemical: Antarafacial (geometrically difficult)
    
    Args:
        n_electrons: Total pi electrons
        thermal: True for thermal, False for photochemical
    
    Returns:
        Dictionary with allowed geometry
    
    Example:
        >>> cycloaddition_allowed(6, thermal=True)
        {'allowed': True, 'geometry': 'suprafacial'}
    """
    is_4n = (n_electrons % 4 == 0)
    
    if is_4n:  # Even electron pairs
        if thermal:
            geometry = 'antarafacial'
            allowed = False  # Geometrically difficult
        else:
            geometry = 'suprafacial'
            allowed = True
    else:  # 4n+2 electrons
        if thermal:
            geometry = 'suprafacial'
            allowed = True
        else:
            geometry = 'antarafacial'
            allowed = False  # Geometrically difficult
    
    return {
        'n_electrons': n_electrons,
        'thermal': thermal,
        'geometry': geometry,
        'allowed': allowed,
        'reason': 'symmetry allowed' if allowed else 'geometrically difficult'
    }


def sigmatropic_allowed(i: int, j: int, thermal: bool = True) -> dict:
    """
    Determine if [i,j]-sigmatropic is allowed.
    
    The sum i + j determines the selection rule:
    - i + j = 4n: Like 4n electron systems
    - i + j = 4n+2: Like 4n+2 electron systems
    
    Args:
        i, j: Sigmatropic indices
        thermal: Thermal or photochemical
    
    Returns:
        Dictionary with allowed geometry
    
    Example:
        >>> sigmatropic_allowed(3, 3, thermal=True)
        {'allowed': True, 'geometry': 'suprafacial'}
    """
    total = i + j
    is_4n = (total % 4 == 0)
    
    if is_4n:
        if thermal:
            geometry = 'antarafacial'
            allowed = False
        else:
            geometry = 'suprafacial'
            allowed = True
    else:  # 4n+2
        if thermal:
            geometry = 'suprafacial'
            allowed = True
        else:
            geometry = 'antarafacial'
            allowed = False
    
    return {
        'i': i,
        'j': j,
        'sum': total,
        'thermal': thermal,
        'geometry': geometry,
        'allowed': allowed
    }


def teca_predict(n_electron_pairs: int, thermal: bool = True) -> dict:
    """
    TECA mnemonic for pericyclic predictions.
    
    **T**hermal + **E**ven -> **C**onrotatory/**A**ntarafacial
    
    Changes that flip the outcome:
    - Thermal -> Photochemical
    - Even -> Odd electron pairs
    
    Args:
        n_electron_pairs: Number of electron pairs (not electrons)
        thermal: True for thermal, False for photochemical
    
    Returns:
        Dictionary with prediction
    
    Example:
        >>> teca_predict(2, thermal=True)
        {'stereochemistry': 'conrotatory or antarafacial'}
    """
    is_even = (n_electron_pairs % 2 == 0)
    
    if thermal:
        if is_even:
            result = 'conrotatory or antarafacial'
        else:
            result = 'disrotatory or suprafacial'
    else:  # Photochemical
        if is_even:
            result = 'disrotatory or suprafacial'
        else:
            result = 'conrotatory or antarafacial'
    
    return {
        'n_electron_pairs': n_electron_pairs,
        'thermal': thermal,
        'stereochemistry': result,
        'mnemonic': 'TECA: Thermal + Even -> Conrotatory/Antarafacial'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "30-01",
        "question": "Thermal cyclization of 1,3-butadiene",
        "n_electrons": 4,
        "thermal": True,
        "expected": "conrotatory"
    },
    {
        "id": "30-02",
        "question": "Photochemical cyclization of 1,3,5-hexatriene",
        "n_electrons": 6,
        "thermal": False,
        "expected": "conrotatory"
    },
    {
        "id": "30-03",
        "question": "[4+2] cycloaddition (Diels-Alder)",
        "n_electrons": 6,
        "thermal": True,
        "expected_geometry": "suprafacial"
    },
    {
        "id": "30-04",
        "question": "[3,3] sigmatropic rearrangement",
        "i": 3,
        "j": 3,
        "thermal": True,
        "expected": "suprafacial"
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Pericyclic Reaction Tools")
    print("=" * 40)
    
    # Test electrocyclic
    print("\nElectrocyclic reactions:")
    for n, th in [(4, True), (4, False), (6, True), (6, False)]:
        result = electrocyclic_stereochemistry(n, th)
        cond = 'thermal' if th else 'photochemical'
        print(f"  {n}pi electrons, {cond}: {result['stereochemistry']}")
    
    # Test cycloaddition
    print("\nCycloadditions:")
    for n in [4, 6]:
        result = cycloaddition_allowed(n, thermal=True)
        print(f"  [{n}] thermal: {result['geometry']} ({'allowed' if result['allowed'] else 'difficult'})")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="cycloaddition_allowed",
            description="Determine if cycloaddition is symmetry-allowed.",
            input_schema=[
            InputSchemaField(name="n_electrons", type="number", required=True),
            InputSchemaField(name="thermal", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="electrocyclic_stereochemistry",
            description="Predict electrocyclic ring closure stereochemistry.",
            input_schema=[
            InputSchemaField(name="n_electrons", type="number", required=True),
            InputSchemaField(name="thermal", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="sigmatropic_allowed",
            description="Determine if [i,j]-sigmatropic is allowed.",
            input_schema=[
            InputSchemaField(name="i", type="number", required=True),
            InputSchemaField(name="j", type="number", required=True),
            InputSchemaField(name="thermal", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="teca_predict",
            description="TECA mnemonic for pericyclic predictions.",
            input_schema=[
            InputSchemaField(name="n_electron_pairs", type="number", required=True),
            InputSchemaField(name="thermal", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
