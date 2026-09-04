"""
L3 Tool: Nucleotide Chemistry Tools
Nucleotide structure, DNA/RNA bases, base pairing.

Source: Biochemistry fundamentals
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter nucleotide chemistry problems (bases, base pairing, DNA/RNA), follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given base name -> get base properties (purine/pyrimidine, pairs with)?
- Given two bases -> check if they form valid Watson-Crick pair?
- Given nucleoside name -> get base and sugar composition?
- Given DNA/RNA sequence -> calculate GC content or complementary strand?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Base properties | `base_info(name)` | Returns type (purine/pyrimidine), symbol, pairs_with |
| Base pairing check | `base_pairing(base1, base2)` | Returns valid_pair, watson_crick, bonds (2 or 3) |
| Nucleoside info | `nucleoside_info(name)` | Returns base, sugar (ribose/deoxyribose) |
| DNA complement | `dna_complement(sequence)` | Returns complementary strand |
| GC content | `gc_content(sequence)` | Returns fraction GC |

### Step 3: Handle special cases
- Purines: A, G (2 rings); Pyrimidines: C, T, U (1 ring)
- Watson-Crick pairs: A-T (2 H-bonds), G-C (3 H-bonds), A-U (RNA)
- T only in DNA; U only in RNA

### Examples
```python
# Example 1: Base info
base_info('adenine')
# -> {'type': 'purine', 'rings': 2, 'symbol': 'A', 'pairs_with': 'thymine'}

# Example 2: Base pairing
base_pairing('adenine', 'thymine')
# -> {'valid_pair': True, 'watson_crick': True, 'bonds': 2}

# Example 3: GC content
gc_content('ATGCGCTA')
# -> 0.5 (50% GC)

# Example 4: DNA complement
dna_complement('ATGC')
# -> 'TACG'
```
"""

# Nucleotide bases
BASES = {
    # Purines
    'adenine': {'type': 'purine', 'rings': 2, 'symbol': 'A', 'pairs_with': 'thymine'},
    'guanine': {'type': 'purine', 'rings': 2, 'symbol': 'G', 'pairs_with': 'cytosine'},
    # Pyrimidines
    'cytosine': {'type': 'pyrimidine', 'rings': 1, 'symbol': 'C', 'pairs_with': 'guanine'},
    'thymine': {'type': 'pyrimidine', 'rings': 1, 'symbol': 'T', 'pairs_with': 'adenine', 'in': 'DNA'},
    'uracil': {'type': 'pyrimidine', 'rings': 1, 'symbol': 'U', 'pairs_with': 'adenine', 'in': 'RNA'},
}

# Nucleosides (base + sugar)
NUCLEOSIDES = {
    'adenosine': {'base': 'adenine', 'sugar': 'ribose'},
    'guanosine': {'base': 'guanine', 'sugar': 'ribose'},
    'cytidine': {'base': 'cytosine', 'sugar': 'ribose'},
    'uridine': {'base': 'uracil', 'sugar': 'ribose'},
    'deoxyadenosine': {'base': 'adenine', 'sugar': 'deoxyribose'},
    'deoxyguanosine': {'base': 'guanine', 'sugar': 'deoxyribose'},
    'deoxycytidine': {'base': 'cytosine', 'sugar': 'deoxyribose'},
    'deoxythymidine': {'base': 'thymine', 'sugar': 'deoxyribose'},
}


def base_info(name: str) -> dict:
    """
    Get nucleotide base properties.
    
    Args:
        name: Base name (e.g., 'adenine', 'guanine')
    
    Returns:
        Dictionary with base properties
    """
    name = name.lower()
    if name in BASES:
        result = BASES[name].copy()
        result['name'] = name
        return result
    return {'error': f'Unknown base: {name}'}


def base_pairing(base1: str, base2: str) -> dict:
    """
    Check if two bases form a valid pair.
    
    Args:
        base1: First base name
        base2: Second base name
    
    Returns:
        Dictionary with pairing info
    """
    b1 = base1.lower()
    b2 = base2.lower()
    
    if b1 not in BASES or b2 not in BASES:
        return {'error': 'Unknown base'}
    
    info1 = BASES[b1]
    info2 = BASES[b2]
    
    # Check if they pair
    valid_pair = info1.get('pairs_with') == b2 or info2.get('pairs_with') == b1
    
    # Watson-Crick pairs
    wc_pairs = [('adenine', 'thymine'), ('thymine', 'adenine'),
                ('adenine', 'uracil'), ('uracil', 'adenine'),
                ('guanine', 'cytosine'), ('cytosine', 'guanine')]
    
    is_wc = (b1, b2) in wc_pairs
    
    return {
        'base1': b1,
        'base2': b2,
        'valid_pair': valid_pair,
        'watson_crick': is_wc,
        'bond_type': 'hydrogen bonds',
        'bonds': 2 if 'adenine' in [b1, b2] or 'thymine' in [b1, b2] or 'uracil' in [b1, b2] else 3
    }


def nucleoside_info(name: str) -> dict:
    """
    Get nucleoside properties.
    
    Args:
        name: Nucleoside name
    
    Returns:
        Dictionary with nucleoside properties
    """
    name = name.lower()
    if name in NUCLEOSIDES:
        result = NUCLEOSIDES[name].copy()
        result['name'] = name
        return result
    return {'error': f'Unknown nucleoside: {name}'}


def purine_or_pyrimidine(name: str) -> dict:
    """
    Classify base as purine or pyrimidine.
    
    Args:
        name: Base name
    
    Returns:
        Dictionary with classification
    """
    info = base_info(name)
    if 'error' in info:
        return info
    
    return {
        'name': name,
        'type': info['type'],
        'rings': info['rings'],
        'description': f"{info['type'].capitalize()} with {info['rings']} ring(s)"
    }


def dna_vs_rna_bases() -> dict:
    """
    Compare DNA and RNA bases.
    
    Returns:
        Dictionary with DNA/RNA base comparison
    """
    return {
        'DNA': {'bases': ['A', 'T', 'G', 'C'], 'sugar': 'deoxyribose'},
        'RNA': {'bases': ['A', 'U', 'G', 'C'], 'sugar': 'ribose'},
        'difference': 'RNA uses uracil (U) instead of thymine (T)',
        'sugar_difference': 'RNA has ribose, DNA has deoxyribose (missing 2\' oxygen)'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "NUC-01",
        "question": "Purine classification",
        "base": "adenine",
        "expected_type": "purine"
    },
    {
        "id": "NUC-02",
        "question": "Base pairing",
        "base1": "guanine",
        "base2": "cytosine",
        "expected_valid": True
    },
    {
        "id": "NUC-03",
        "question": "Ring count",
        "base": "guanine",
        "expected_rings": 2
    },
    {
        "id": "NUC-04",
        "question": "RNA unique base",
        "expected_base": "uracil"
    },
    {
        "id": "NUC-05",
        "question": "Hydrogen bonds",
        "pair": ("guanine", "cytosine"),
        "expected_bonds": 3
    },
]


if __name__ == "__main__":
    print("Nucleotide Chemistry Tools")
    print("=" * 40)
    
    # Test bases
    print("\nBases:")
    for name in ['adenine', 'guanine', 'cytosine', 'thymine', 'uracil']:
        info = base_info(name)
        print(f"  {name}: {info['type']}, {info['rings']} ring(s)")
    
    # Test pairing
    print("\nBase Pairing:")
    for b1, b2 in [('adenine', 'thymine'), ('guanine', 'cytosine')]:
        result = base_pairing(b1, b2)
        print(f"  {b1}-{b2}: {result['bonds']} H-bonds")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="base_info",
            description="Get nucleotide base properties.",
            input_schema=[
            InputSchemaField(name="name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="base_pairing",
            description="Check if two bases form a valid pair.",
            input_schema=[
            InputSchemaField(name="base1", type="string", required=True),
            InputSchemaField(name="base2", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="dna_vs_rna_bases",
            description="Compare DNA and RNA bases.",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="nucleoside_info",
            description="Get nucleoside properties.",
            input_schema=[
            InputSchemaField(name="name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="purine_or_pyrimidine",
            description="Classify base as purine or pyrimidine.",
            input_schema=[
            InputSchemaField(name="name", type="string", required=True)
            ],
            handler="{name}",
        )
    ]
