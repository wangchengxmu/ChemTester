# -*- coding: utf-8 -*-
"""
L3 Tool: Protein Secondary Structure Tools
Helix parameters, Chou-Fasman prediction, Ramachandran analysis.

Source: Fundamentals of Biochemistry (Jakubowski and Flatt), Ch4
Created: 2026-03-13
"""
## Solver Instructions (for AI Agent)

# When you encounter protein secondary structure problems (helix geometry, Chou-Fasman, Ramachandran), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: amino acid sequence, number of residues, phi/psi angles, helix type
# - **Asked**: helix length/turns/H-bonds, secondary structure prediction, region classification

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Helix length | `helix_length(n_residues, helix_type)` | n residues, 'alpha'/'3_10'/'pi' |
# | Helix turns | `helix_turns(n_residues, helix_type)` | n residues, helix type |
# | Helix dipole | `helix_dipole(n_residues)` | n residues (mu = n x 3.5 D) |
# | Chou-Fasman predict | `chou_fasman_predict(sequence)` | AA sequence string |
# | Ramachandran check | `ramachandran_check(phi, psi)` | phi, psi angles in degrees |
# | H-bonds in helix | `helix_h_bonds(n_residues, helix_type)` | n residues, helix type |
# | Compare helix types | `compare_helix_types(n_residues)` | n residues |

### Step 3: Handle special cases
# - alpha-helix: 3.6 residues/turn, rise 1.5 A/residue, H-bond i->i+4
# - 310-helix: 3.0 residues/turn, H-bond i->i+3
# - pi-helix: 4.4 residues/turn, H-bond i->i+5
# - Chou-Fasman: Pa > 1.03 -> helix; Pb > 1.05 -> sheet; else coil

### Examples
# 1. **Helix length**: `helix_length(15, 'alpha')` -> 22.5 A (15 x 1.5)
# 2. **Chou-Fasman**: `chou_fasman_predict('AAAA')` -> all 'H' (Ala is helix-favoring)
# 3. **Ramachandran**: `ramachandran_check(-57, -47)` -> 'alpha_helix', allowed=True
# 4. **Compare**: `compare_helix_types(10)` -> alpha: 15A/2.78 turns, 3_10: 20A/3.33 turns


# Helix parameters
HELIX_PARAMS = {
    'alpha': {'residues_per_turn': 3.6, 'pitch': 5.4, 'rise': 1.5, 'h_bond_offset': 4,
              'phi': -57, 'psi': -47},
    '3_10': {'residues_per_turn': 3.0, 'pitch': 6.0, 'rise': 2.0, 'h_bond_offset': 3,
             'phi': -50, 'psi': -26},
    'pi': {'residues_per_turn': 4.4, 'pitch': 4.1, 'rise': 1.2, 'h_bond_offset': 5,
           'phi': -55, 'psi': -70},
}

# Chou-Fasman propensities
CHOU_FASMAN = {
    'A': {'Pa': 1.42, 'Pb': 0.83, 'Pt': 0.66, 'name': 'Ala'},
    'R': {'Pa': 0.98, 'Pb': 0.93, 'Pt': 0.95, 'name': 'Arg'},
    'N': {'Pa': 0.67, 'Pb': 0.89, 'Pt': 1.56, 'name': 'Asn'},
    'D': {'Pa': 1.01, 'Pb': 0.54, 'Pt': 1.46, 'name': 'Asp'},
    'C': {'Pa': 0.70, 'Pb': 1.19, 'Pt': 1.19, 'name': 'Cys'},
    'Q': {'Pa': 1.11, 'Pb': 1.10, 'Pt': 0.98, 'name': 'Gln'},
    'E': {'Pa': 1.51, 'Pb': 0.37, 'Pt': 0.74, 'name': 'Glu'},
    'G': {'Pa': 0.57, 'Pb': 0.75, 'Pt': 1.56, 'name': 'Gly'},
    'H': {'Pa': 1.00, 'Pb': 0.87, 'Pt': 0.95, 'name': 'His'},
    'I': {'Pa': 1.08, 'Pb': 1.60, 'Pt': 0.47, 'name': 'Ile'},
    'L': {'Pa': 1.21, 'Pb': 1.30, 'Pt': 0.59, 'name': 'Leu'},
    'K': {'Pa': 1.16, 'Pb': 0.74, 'Pt': 1.01, 'name': 'Lys'},
    'M': {'Pa': 1.45, 'Pb': 1.05, 'Pt': 0.60, 'name': 'Met'},
    'F': {'Pa': 1.13, 'Pb': 1.38, 'Pt': 0.60, 'name': 'Phe'},
    'P': {'Pa': 0.57, 'Pb': 0.55, 'Pt': 1.52, 'name': 'Pro'},
    'S': {'Pa': 0.77, 'Pb': 0.75, 'Pt': 1.43, 'name': 'Ser'},
    'T': {'Pa': 0.83, 'Pb': 1.19, 'Pt': 0.96, 'name': 'Thr'},
    'W': {'Pa': 1.08, 'Pb': 1.37, 'Pt': 0.96, 'name': 'Trp'},
    'Y': {'Pa': 0.69, 'Pb': 1.47, 'Pt': 1.14, 'name': 'Tyr'},
    'V': {'Pa': 1.06, 'Pb': 1.70, 'Pt': 0.50, 'name': 'Val'},
}

RAMACHANDRAN_REGIONS = {
    'alpha_helix': {'phi_range': (-90, -30), 'psi_range': (-70, -10)},
    'beta_sheet': {'phi_range': (-180, -100), 'psi_range': (100, 180)},
    'left_handed': {'phi_range': (30, 90), 'psi_range': (-30, 90)},
    'collagen': {'phi_range': (-100, -40), 'psi_range': (120, 180)},
}


def helix_length(n_residues: int, helix_type: str = 'alpha') -> dict:
    """
    Calculate the length of a helix.
    
    Args:
        n_residues: Number of amino acids
        helix_type: 'alpha', '3_10', or 'pi'
    
    Returns:
        Dictionary with helix length in Angstroms
    
    Example:
        >>> helix_length(15, 'alpha')
        {'length': 22.5, 'unit': 'A', 'helix_type': 'alpha'}
    """
    helix_type = str(helix_type).lower()
    n_residues = float(n_residues)
    if helix_type not in HELIX_PARAMS:
        return {'error': f'Unknown helix type: {helix_type}'}
    
    params = HELIX_PARAMS[helix_type]
    length = n_residues * params['rise']
    
    return {
        'length': length,
        'unit': 'A',
        'helix_type': helix_type,
        'n_residues': n_residues,
        'rise_per_residue': params['rise']
    }


def helix_turns(n_residues: int, helix_type: str = 'alpha') -> dict:
    """
    Calculate number of turns in a helix.
    
    Args:
        n_residues: Number of amino acids
        helix_type: 'alpha', '3_10', or 'pi'
    
    Returns:
        Dictionary with number of turns
    
    Example:
        >>> helix_turns(20, 'alpha')
        {'turns': 5.56, 'helix_type': 'alpha'}
    """
    helix_type = str(helix_type).lower()
    n_residues = float(n_residues)
    if helix_type not in HELIX_PARAMS:
        return {'error': f'Unknown helix type: {helix_type}'}
    
    params = HELIX_PARAMS[helix_type]
    turns = n_residues / params['residues_per_turn']
    
    return {
        'turns': round(turns, 2),
        'helix_type': helix_type,
        'n_residues': n_residues,
        'residues_per_turn': params['residues_per_turn']
    }


def helix_dipole(n_residues: int) -> dict:
    """
    Calculate dipole moment of alpha helix.
    
    mu = n x 3.5 Debye
    
    Args:
        n_residues: Number of amino acids
    
    Returns:
        Dictionary with dipole moment
    
    Example:
        >>> helix_dipole(12)
        {'dipole': 42.0, 'unit': 'Debye'}
    """
    dipole = n_residues * 3.5
    
    return {
        'dipole': dipole,
        'unit': 'Debye',
        'n_residues': n_residues,
        'formula': 'n x 3.5 Debye'
    }


def chou_fasman_predict(sequence: str) -> dict:
    """
    Predict secondary structure using Chou-Fasman method.
    
    Rules:
    - Helix: Pa > 1.03 AND Pa > Pb
    - Sheet: Pb > 1.05 AND Pb > Pa
    - Coil: Neither condition met
    
    Args:
        sequence: Amino acid sequence (1-letter codes)
    
    Returns:
        Dictionary with per-residue predictions
    
    Example:
        >>> chou_fasman_predict('AAAA')
        {'sequence': 'AAAA', 'predictions': ['H', 'H', 'H', 'H'], ...}
    """
    sequence = sequence.upper()
    predictions = []
    
    for aa in sequence:
        if aa not in CHOU_FASMAN:
            predictions.append('?')
            continue
        
        props = CHOU_FASMAN[aa]
        pa = props['Pa']
        pb = props['Pb']
        
        if pa > 1.03 and pa > pb:
            predictions.append('H')  # Helix
        elif pb > 1.05 and pb > pa:
            predictions.append('E')  # Extended (sheet)
        else:
            predictions.append('C')  # Coil
    
    # Calculate average propensities
    avg_pa = sum(CHOU_FASMAN[aa]['Pa'] for aa in sequence if aa in CHOU_FASMAN) / len([aa for aa in sequence if aa in CHOU_FASMAN]) if sequence else 0
    avg_pb = sum(CHOU_FASMAN[aa]['Pb'] for aa in sequence if aa in CHOU_FASMAN) / len([aa for aa in sequence if aa in CHOU_FASMAN]) if sequence else 0
    
    # Overall prediction
    if avg_pa > avg_pb and avg_pa > 1.0:
        overall = 'helix-favored'
    elif avg_pb > avg_pa and avg_pb > 1.0:
        overall = 'sheet-favored'
    else:
        overall = 'coil-favored'
    
    return {
        'sequence': sequence,
        'predictions': predictions,
        'prediction_string': ''.join(predictions),
        'avg_Pa': round(avg_pa, 2),
        'avg_Pb': round(avg_pb, 2),
        'overall': overall
    }


def ramachandran_check(phi: float, psi: float) -> dict:
    """
    Check if phi/psi angles are in allowed regions.
    
    Args:
        phi: Phi angle (degrees)
        psi: Psi angle (degrees)
    
    Returns:
        Dictionary with region assignment
    
    Example:
        >>> ramachandran_check(-57, -47)
        {'region': 'alpha_helix', 'allowed': True}
    """
    regions_found = []
    
    for region_name, bounds in RAMACHANDRAN_REGIONS.items():
        phi_min, phi_max = bounds['phi_range']
        psi_min, psi_max = bounds['psi_range']
        
        # Check if angles are in this region
        phi_in = phi_min <= phi <= phi_max
        psi_in = psi_min <= psi <= psi_max
        
        if phi_in and psi_in:
            regions_found.append(region_name)
    
    # Determine if in generally allowed region
    allowed = len(regions_found) > 0
    
    # Primary region
    primary_region = regions_found[0] if regions_found else 'disallowed'
    
    return {
        'phi': phi,
        'psi': psi,
        'region': primary_region,
        'all_regions': regions_found,
        'allowed': allowed
    }


def helix_h_bonds(n_residues: int, helix_type: str = 'alpha') -> dict:
    """
    Calculate number of hydrogen bonds in a helix.
    
    In an alpha helix, H-bonds form between i and i+4.
    Number of H-bonds = n_residues - h_bond_offset
    
    Args:
        n_residues: Number of amino acids
        helix_type: 'alpha', '3_10', or 'pi'
    
    Returns:
        Dictionary with number of H-bonds
    """
    helix_type = helix_type.lower()
    if helix_type not in HELIX_PARAMS:
        return {'error': f'Unknown helix type: {helix_type}'}
    
    offset = HELIX_PARAMS[helix_type]['h_bond_offset']
    n_hbonds = max(0, n_residues - offset)
    
    return {
        'n_hbonds': n_hbonds,
        'helix_type': helix_type,
        'h_bond_pattern': f'i -> i+{offset}'
    }


def compare_helix_types(n_residues: int) -> dict:
    """
    Compare properties of different helix types.
    
    Args:
        n_residues: Number of amino acids
    
    Returns:
        Dictionary comparing all helix types
    """
    comparison = {}
    
    for helix_type in ['alpha', '3_10', 'pi']:
        params = HELIX_PARAMS[helix_type]
        comparison[helix_type] = {
            'length': n_residues * params['rise'],
            'turns': round(n_residues / params['residues_per_turn'], 2),
            'h_bonds': max(0, n_residues - params['h_bond_offset'])
        }
    
    return comparison


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "PS-01",
        "question": "Helix length",
        "n_residues": 15,
        "helix_type": "alpha",
        "expected_length": 22.5
    },
    {
        "id": "PS-02",
        "question": "Helix turns",
        "n_residues": 20,
        "helix_type": "alpha",
        "expected_turns": 5.56
    },
    {
        "id": "PS-03",
        "question": "Helix dipole",
        "n_residues": 12,
        "expected_dipole": 42.0
    },
    {
        "id": "PS-04",
        "question": "Chou-Fasman prediction",
        "sequence": "AAAA",
        "expected": "helix-favored"
    },
    {
        "id": "PS-05",
        "question": "Ramachandran check",
        "phi": -57,
        "psi": -47,
        "expected_region": "alpha_helix"
    },
]


if __name__ == "__main__":
    print("Protein Secondary Structure Tools")
    print("=" * 40)
    
    # Test helix calculations
    print("\nAlpha helix (15 residues):")
    print(f"  Length: {helix_length(15, 'alpha')}")
    print(f"  Turns: {helix_turns(15, 'alpha')}")
    print(f"  H-bonds: {helix_h_bonds(15, 'alpha')}")
    print(f"  Dipole: {helix_dipole(15)}")
    
    # Test Chou-Fasman
    print("\nChou-Fasman prediction for 'AAAA':")
    print(f"  {chou_fasman_predict('AAAA')}")
    
    # Test Ramachandran
    print("\nRamachandran check (-57deg, -47deg):")
    print(f"  {ramachandran_check(-57, -47)}")
    
    # Compare helices
    print("\nCompare helix types (10 residues):")
    for helix_type, data in compare_helix_types(10).items():
        print(f"  {helix_type}: {data}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="chou_fasman_predict",
            description="Predict secondary structure using Chou-Fasman method.",
            input_schema=[
            InputSchemaField(name="sequence", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="compare_helix_types",
            description="Compare properties of different helix types.",
            input_schema=[
            InputSchemaField(name="n_residues", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="helix_dipole",
            description="Calculate dipole moment of alpha helix.",
            input_schema=[
            InputSchemaField(name="n_residues", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="helix_h_bonds",
            description="Calculate number of hydrogen bonds in a helix.",
            input_schema=[
            InputSchemaField(name="n_residues", type="number", required=True),
            InputSchemaField(name="helix_type", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="helix_length",
            description="Calculate the length of a helix.",
            input_schema=[
            InputSchemaField(name="n_residues", type="number", required=True),
            InputSchemaField(name="helix_type", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="helix_turns",
            description="Calculate number of turns in a helix.",
            input_schema=[
            InputSchemaField(name="n_residues", type="number", required=True),
            InputSchemaField(name="helix_type", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="ramachandran_check",
            description="Check if phi/psi angles are in allowed regions.",
            input_schema=[
            InputSchemaField(name="phi", type="number", required=True),
            InputSchemaField(name="psi", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
