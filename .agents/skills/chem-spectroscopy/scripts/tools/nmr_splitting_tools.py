"""
L3 Tool: NMR Splitting Tools
Predict splitting patterns and multiplet characteristics.

Source: Organic Chemistry (OpenStax) Ch13
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter NMR splitting pattern, intensity ratio, neighbor count from multiplet, or coupling relationship problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given number of equivalent neighboring protons -> predict splitting pattern and intensity ratios?
- Given a multiplet name -> determine number of neighboring protons?
- Given a group of equivalent protons and neighbor count -> predict full signal characteristics?
- Given J coupling values for multiple proton groups -> identify which are coupled?

### Step 2: Choose the correct function
- **Splitting pattern:** `splitting_pattern(n_neighbors)` -> dict with 'name' (singlet/doublet/triplet/etc.), 'n_peaks', and 'intensities' (Pascal's triangle row)
- **Multiplet name from peaks:** `multiplet_name(n_peaks)` -> 'singlet'(1), 'doublet'(2), 'triplet'(3), 'quartet'(4), 'quintet'(5), etc.
- **Intensity ratios:** `intensity_ratios(n_neighbors)` -> Pascal's triangle: 0->[1], 1->[1,1], 2->[1,2,1], 3->[1,3,3,1], etc.
- **Predict spectrum group:** `predict_spectrum_group(protons, neighbors)` -> dict with proton count, multiplet name, peak count, intensities. Example: CH3 with 2 neighbors -> triplet [1,2,1]
- **Neighbors from multiplet:** `neighbors_from_multiplet(multiplet)` -> reverse lookup. 'quartet'->3, 'triplet'->2, 'doublet'->1, 'singlet'->0
- **Coupling relationships:** `coupling_relationship(j_values)` -> identify coupled groups. Groups sharing the same J value are coupled. Pass dict like {'CH3': 7, 'CH2': 7, 'OH': 3} -> [['CH3', 'CH2']]

### Step 3: Handle special cases
- n+1 rule only applies to EQUIVALENT neighboring protons
- Non-equivalent neighbors create more complex (non-first-order) splitting
- Coupled protons must share the same J value; different J values mean different coupling relationships
- OH protons often exchange and appear as singlets regardless of neighbors

### Examples
```python
# Example 1: CH3 in CH3CH2Br (2 equivalent neighbors on CH2)
splitting_pattern(2)  -> {'name': 'triplet', 'n_peaks': 3, 'intensities': [1, 2, 1]}

# Example 2: What multiplet has 4 peaks? How many neighbors?
multiplet_name(4)  -> 'quartet'
neighbors_from_multiplet('quartet')  -> 3

# Example 3: Full prediction for CH3CH2Br
predict_spectrum_group(protons=3, neighbors=2)  -> triplet
predict_spectrum_group(protons=2, neighbors=3)  -> quartet [1,3,3,1]

# Example 4: Identify coupled groups
coupling_relationship({'Ha': 7, 'Hb': 7, 'Hc': 3})  -> [['Ha', 'Hb']] (Ha and Hb coupled, Hc not)
```
"""

# Pascal's triangle for intensity ratios (n_neighbors -> intensities)
INTENSITY_RATIOS = {
    0: [1],
    1: [1, 1],
    2: [1, 2, 1],
    3: [1, 3, 3, 1],
    4: [1, 4, 6, 4, 1],
    5: [1, 5, 10, 10, 5, 1],
    6: [1, 6, 15, 20, 15, 6, 1],
    7: [1, 7, 21, 35, 35, 21, 7, 1],
}

MULTIPLET_NAMES = {
    1: 'singlet',
    2: 'doublet',
    3: 'triplet',
    4: 'quartet',
    5: 'quintet',
    6: 'sextet',
    7: 'septet',
    8: 'octet',
}


def splitting_pattern(n_neighbors: int) -> dict:
    """
    Return multiplet name and intensity ratios for given neighbors.
    
    Uses the n + 1 rule: proton with n equivalent neighbors shows n + 1 peaks.
    
    Args:
        n_neighbors: Number of equivalent neighboring protons
    
    Returns:
        Dictionary with multiplet name and intensity ratios
    
    Example:
        >>> splitting_pattern(2)
        {'name': 'triplet', 'n_peaks': 3, 'intensities': [1, 2, 1]}
    """
    if n_neighbors < 0:
        raise ValueError("Number of neighbors cannot be negative")
    
    n_peaks = n_neighbors + 1
    intensities = INTENSITY_RATIOS.get(n_neighbors, _pascal_row(n_neighbors))
    name = MULTIPLET_NAMES.get(n_peaks, f'{n_peaks}-plet')
    
    return {
        'name': name,
        'n_peaks': n_peaks,
        'intensities': intensities
    }


def multiplet_name(n_peaks: int) -> str:
    """
    Return multiplet name from number of peaks.
    
    Args:
        n_peaks: Number of peaks in the multiplet
    
    Returns:
        Multiplet name (singlet, doublet, triplet, etc.)
    
    Example:
        >>> multiplet_name(4)
        'quartet'
    """
    if n_peaks < 1:
        raise ValueError("Number of peaks must be at least 1")
    
    return MULTIPLET_NAMES.get(n_peaks, f'{n_peaks}-plet')


def intensity_ratios(n_neighbors: int) -> list:
    """
    Calculate intensity ratios using n + 1 rule (Pascal's triangle).
    
    Args:
        n_neighbors: Number of equivalent neighboring protons
    
    Returns:
        List of relative intensities
    
    Example:
        >>> intensity_ratios(3)
        [1, 3, 3, 1]
    """
    if n_neighbors < 0:
        raise ValueError("Number of neighbors cannot be negative")
    
    return INTENSITY_RATIOS.get(n_neighbors, _pascal_row(n_neighbors))


def _pascal_row(n: int) -> list:
    """
    Calculate nth row of Pascal's triangle.
    
    Args:
        n: Row number (0-indexed)
    
    Returns:
        List of coefficients
    """
    if n == 0:
        return [1]
    
    row = [1]
    for k in range(n):
        row.append(row[k] * (n - k) // (k + 1))
    return row


def predict_spectrum_group(protons: int, neighbors: int) -> dict:
    """
    Predict NMR signal for a group of equivalent protons.
    
    Args:
        protons: Number of equivalent protons in the group
        neighbors: Number of neighboring protons
    
    Returns:
        Dictionary with predicted signal characteristics
    
    Example:
        >>> predict_spectrum_group(3, 2)  # CH3 with 2 neighbors
        {'protons': 3, 'multiplet': 'triplet', 'n_peaks': 3, 'intensities': [1, 2, 1]}
    """
    if protons < 1:
        raise ValueError("Number of protons must be at least 1")
    
    pattern = splitting_pattern(neighbors)
    
    return {
        'protons': protons,
        'multiplet': pattern['name'],
        'n_peaks': pattern['n_peaks'],
        'intensities': pattern['intensities']
    }


def spectrum_group(protons: int, neighbors: int) -> dict:
    """Alias for predict_spectrum_group - for solver compatibility."""
    return predict_spectrum_group(protons, neighbors)


def neighbors_from_multiplet(multiplet: str) -> int:
    """
    Calculate number of neighboring protons from multiplet name.
    
    Args:
        multiplet: Multiplet name (singlet, doublet, triplet, etc.)
    
    Returns:
        Number of neighboring protons
    
    Example:
        >>> neighbors_from_multiplet('quartet')
        3
    """
    multiplet = multiplet.lower()
    
    # Reverse lookup
    for n_peaks, name in MULTIPLET_NAMES.items():
        if name == multiplet:
            return n_peaks - 1
    
    # Handle numeric names like "5-plet"
    if multiplet.endswith('-plet'):
        try:
            n_peaks = int(multiplet.replace('-plet', ''))
            return n_peaks - 1
        except ValueError:
            pass
    
    raise ValueError(f"Unknown multiplet type: {multiplet}")


def coupling_relationship(j_values: dict) -> list:
    """
    Identify coupled proton groups from coupling constants.
    
    Coupled protons share the same J value.
    
    Args:
        j_values: Dictionary mapping proton groups to their J values
                  e.g., {'A': 7, 'B': 7, 'C': 3}
    
    Returns:
        List of coupled group pairs
    
    Example:
        >>> coupling_relationship({'A': 7, 'B': 7, 'C': 3})
        [['A', 'B']]
    """
    coupled = []
    groups = list(j_values.keys())
    
    for i, g1 in enumerate(groups):
        for g2 in groups[i+1:]:
            if j_values[g1] == j_values[g2] and j_values[g1] > 0:
                coupled.append([g1, g2])
    
    return coupled


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "13-01",
        "question": "Predict splitting for CH3 in CH3CH2Br",
        "n_neighbors": 2,
        "expected": "triplet"
    },
    {
        "id": "13-02",
        "question": "Intensity ratios for quartet",
        "n_neighbors": 3,
        "expected_intensities": [1, 3, 3, 1]
    },
    {
        "id": "13-03",
        "question": "Splitting pattern for proton with 6 neighbors",
        "n_neighbors": 6,
        "expected": "septet"
    },
    {
        "id": "13-04",
        "question": "CH3CH2Br spectrum prediction",
        "groups": [
            {"protons": 3, "neighbors": 2},  # CH3
            {"protons": 2, "neighbors": 3},  # CH2
        ],
        "expected": [
            {"multiplet": "triplet"},
            {"multiplet": "quartet"},
        ]
    },
]


if __name__ == "__main__":
    # Quick tests
    print("NMR Splitting Tools")
    print("=" * 40)
    
    # Test splitting patterns
    for n in [0, 1, 2, 3]:
        result = splitting_pattern(n)
        print(f"{n} neighbors: {result['name']} {result['intensities']}")
    
    # Test multiplet name
    print(f"\n4 peaks = {multiplet_name(4)}")
    
    # Test neighbors from multiplet
    print(f"Quartet has {neighbors_from_multiplet('quartet')} neighbors")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="coupling_relationship",
            description="Identify coupled proton groups from coupling constants.",
            input_schema=[
            InputSchemaField(name="j_values", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="intensity_ratios",
            description="Calculate intensity ratios using n + 1 rule (Pascal's triangle).",
            input_schema=[
            InputSchemaField(name="n_neighbors", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="multiplet_name",
            description="Return multiplet name from number of peaks.",
            input_schema=[
            InputSchemaField(name="n_peaks", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="neighbors_from_multiplet",
            description="Calculate number of neighboring protons from multiplet name.",
            input_schema=[
            InputSchemaField(name="multiplet", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_spectrum_group",
            description="Predict NMR signal for a group of equivalent protons.",
            input_schema=[
            InputSchemaField(name="protons", type="number", required=True),
            InputSchemaField(name="neighbors", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="spectrum_group",
            description="Alias for predict_spectrum_group - for solver compatibility.",
            input_schema=[
            InputSchemaField(name="protons", type="number", required=True),
            InputSchemaField(name="neighbors", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="splitting_pattern",
            description="Return multiplet name and intensity ratios for given neighbors.",
            input_schema=[
            InputSchemaField(name="n_neighbors", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
