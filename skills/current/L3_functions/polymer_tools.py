"""
L3 Tool: Polymer Chemistry Tools
Calculate degree of polymerization and classify polymers.

Source: Organic Chemistry (OpenStax) Ch31
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter polymer chemistry problems (degree of polymerization, polymer classification, monomer reactivity), follow this decision tree:

### Step 1: Identify what is given and what is asked
- **DP from molecular weights**: Given monomer MW and polymer MW -> find DP
- **DP from conversion**: Given extent of reaction (step-growth) -> find DP via Carothers equation
- **Polymer info**: Given polymer name -> find monomer, method, uses (lookup COMMON_POLYMERS)
- **Monomer reactivity**: Given monomer name -> check which mechanisms work (cationic, anionic, radical)
- **Polymer properties**: Given monomer info -> classify as step-growth vs chain-growth, thermoplastic vs thermoset

### Step 2: Choose the correct function
- `degree_of_polymerization(monomer_mw, polymer_mw)` -> DP = M_polymer/M_monomer
- `step_growth_dp(extent)` -> DP = 1/(1-p) (Carothers equation)
- `chain_growth_dp(initiator_conc, monomer_conc, efficiency)` -> for chain-growth DP
- `classify_polymer(polymer_name)` -> dict with monomer, method, uses, type from COMMON_POLYMERS
- `monomer_reactivity(monomer_name)` -> which mechanisms are supported from MONOMER_REACTIVITY

### Step 3: Handle special cases
- Step-growth: extent ≥ 1.0 returns infinite DP (complete conversion)
- Chain-growth DP depends on initiator, not just conversion
- COMMON_POLYMERS is a dict lookup - check keys for available polymers
- Nylon 66 and PET are step-growth (condensation); most others are chain-growth (addition)

### Examples
1. **DP from MW**: PE monomer (ethylene) MW=28, polymer MW=28000
   -> `degree_of_polymerization(28, 28000)` -> {'dp': 1000}

2. **Step-growth DP**: Extent of reaction p=0.99
   -> `step_growth_dp(0.99)` -> {'dp': 100.0, 'extent': 0.99}
   -> p=0.999 -> DP=1000 (high conversion needed for long chains)

3. **Polymer lookup**: What is PET made from?
   -> `classify_polymer('pet')` -> monomers: ethylene glycol + terephthalic acid, step-growth, bottles/fibers
"""

# Common polymers database
COMMON_POLYMERS = {
    'polyethylene': {'monomer': 'ethylene', 'method': 'radical', 'uses': ['bags', 'containers']},
    'polypropylene': {'monomer': 'propylene', 'method': 'ziegler-natta', 'uses': ['ropes', 'containers']},
    'polystyrene': {'monomer': 'styrene', 'method': 'radical or anionic', 'uses': ['foam cups', 'packaging']},
    'pvc': {'monomer': 'vinyl chloride', 'method': 'radical', 'uses': ['pipes', 'flooring']},
    'teflon': {'monomer': 'tetrafluoroethylene', 'method': 'radical', 'uses': ['non-stick coating']},
    'pmma': {'monomer': 'methyl methacrylate', 'method': 'radical or anionic', 'uses': ['windows', 'lenses']},
    'nylon_66': {'monomers': ['adipic acid', 'hexamethylenediamine'], 'method': 'step-growth', 'uses': ['fibers', 'rope']},
    'pet': {'monomers': ['ethylene glycol', 'terephthalic acid'], 'method': 'step-growth', 'uses': ['bottles', 'fibers']},
}

# Monomer reactivity classification
MONOMER_REACTIVITY = {
    'ethylene': {'cationic': False, 'anionic': False, 'radical': True},
    'propylene': {'cationic': True, 'anionic': False, 'radical': True},
    'styrene': {'cationic': True, 'anionic': True, 'radical': True},
    'isobutylene': {'cationic': True, 'anionic': False, 'radical': False},
    'acrylonitrile': {'cationic': False, 'anionic': True, 'radical': True},
    'methyl_methacrylate': {'cationic': False, 'anionic': True, 'radical': True},
    'vinyl_chloride': {'cationic': False, 'anionic': False, 'radical': True},
}


def degree_of_polymerization(monomer_mw: float, polymer_mw: float) -> dict:
    """
    Calculate degree of polymerization.
    
    DP = M_polymer / M_monomer
    
    Args:
        monomer_mw: Molecular weight of monomer (g/mol)
        polymer_mw: Molecular weight of polymer (g/mol)
    
    Returns:
        Dictionary with DP
    
    Example:
        >>> degree_of_polymerization(28, 28000)
        {'dp': 1000, 'monomer_mw': 28, 'polymer_mw': 28000}
    """
    dp = polymer_mw / monomer_mw
    return {
        'dp': round(dp),
        'monomer_mw': monomer_mw,
        'polymer_mw': polymer_mw
    }


def step_growth_dp(extent: float) -> dict:
    """
    Calculate DP from extent of reaction for step-growth.
    
    Carothers equation: DP = 1 / (1 - p)
    
    Args:
        extent: Fraction of functional groups reacted (0-1)
    
    Returns:
        Dictionary with DP
    
    Example:
        >>> step_growth_dp(0.95)
        {'dp': 20.0, 'extent': 0.95}
    """
    if extent >= 1.0:
        return {'dp': float('inf'), 'extent': extent, 'note': 'Complete conversion'}
    
    dp = 1 / (1 - extent)
    return {
        'dp': round(dp, 1),
        'extent': extent,
        'equation': 'DP = 1/(1-p) [Carothers equation]'
    }


def polymerization_method(monomer: str) -> dict:
    """
    Recommend polymerization method for monomer.
    
    Rules:
    - EDG (alkyl, phenyl) -> Cationic possible
    - EWG (CN, COOR) -> Anionic possible
    - No EDG/EWG -> Radical only
    
    Args:
        monomer: Monomer name
    
    Returns:
        Dictionary with recommended method(s)
    
    Example:
        >>> polymerization_method('styrene')
        {'method': 'radical or anionic or cationic'}
    """
    monomer_lower = monomer.lower().replace('-', '').replace('_', '').replace(' ', '')
    
    # Check known monomers
    for name, reactivity in MONOMER_REACTIVITY.items():
        name_norm = name.lower().replace('_', '')
        if name_norm in monomer_lower or monomer_lower in name_norm:
            methods = []
            if reactivity['radical']:
                methods.append('radical')
            if reactivity['cationic']:
                methods.append('cationic')
            if reactivity['anionic']:
                methods.append('anionic')
            
            return {
                'monomer': monomer,
                'methods': methods,
                'primary': methods[0] if methods else 'unknown'
            }
    
    # Default rules based on substituents
    methods = ['radical']  # Always possible with vinyl monomers
    
    if any(x in monomer_lower for x in ['methyl', 'ethyl', 'propyl', 'phenyl', 'styren']):
        methods.append('cationic')
    
    if any(x in monomer_lower for x in ['cyano', 'acryl', 'ester', 'nitrile']):
        methods.append('anionic')
    
    return {
        'monomer': monomer,
        'methods': methods,
        'primary': methods[0]
    }


def polymer_type(polymer_name: str) -> dict:
    """
    Classify polymer and provide information.
    
    Args:
        polymer_name: Name of polymer
    
    Returns:
        Dictionary with classification
    
    Example:
        >>> polymer_type('nylon 6,6')
        {'type': 'step-growth', 'category': 'polyamide'}
    """
    polymer_lower = polymer_name.lower().replace('-', '').replace(',', '').replace(' ', '')
    
    # Check database
    for name, data in COMMON_POLYMERS.items():
        name_norm = name.lower().replace('_', '')
        if name_norm in polymer_lower or polymer_lower in name_norm:
            category = 'polyamide' if 'nylon' in name else 'polyolefin' if name in ['polyethylene', 'polypropylene'] else 'vinyl'
            return {
                'name': name,
                'type': data['method'],
                'category': category,
                'uses': data['uses'],
                'monomers': data.get('monomers', [data.get('monomer')])
            }
    
    return {
        'name': polymer_name,
        'type': 'unknown',
        'category': 'unknown'
    }


def crystallinity_effect(crystallinity: str) -> dict:
    """
    Predict properties based on crystallinity.
    
    Args:
        crystallinity: 'high', 'medium', 'low', or 'atactic'
    
    Returns:
        Dictionary with predicted properties
    """
    crystallinity_lower = crystallinity.lower()
    
    if crystallinity_lower in ['high', 'isotactic']:
        return {
            'crystallinity': 'high',
            'strength': 'high',
            'flexibility': 'low',
            'transparency': 'opaque',
            'density': 'high'
        }
    elif crystallinity_lower in ['medium', 'syndiotactic']:
        return {
            'crystallinity': 'medium',
            'strength': 'medium',
            'flexibility': 'medium',
            'transparency': 'translucent',
            'density': 'medium'
        }
    else:  # low or atactic
        return {
            'crystallinity': 'low',
            'strength': 'low',
            'flexibility': 'high',
            'transparency': 'transparent',
            'density': 'low'
        }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "31-01",
        "question": "DP at 95% conversion",
        "extent": 0.95,
        "expected_dp": 20.0
    },
    {
        "id": "31-02",
        "question": "DP at 99% conversion",
        "extent": 0.99,
        "expected_dp": 100.0
    },
    {
        "id": "31-03",
        "question": "Polymerization method for isobutylene",
        "monomer": "isobutylene",
        "expected": "cationic"
    },
    {
        "id": "31-04",
        "question": "Polymerization method for acrylonitrile",
        "monomer": "acrylonitrile",
        "expected": "anionic"
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Polymer Chemistry Tools")
    print("=" * 40)
    
    # Test DP
    print("\nDegree of Polymerization:")
    result = degree_of_polymerization(28, 28000)
    print(f"  Ethylene (MW=28) -> PE (MW=28000): DP = {result['dp']}")
    
    # Test step-growth
    print("\nStep-Growth DP (Carothers):")
    for extent in [0.90, 0.95, 0.99]:
        result = step_growth_dp(extent)
        print(f"  {extent*100:.0f}% conversion: DP = {result['dp']}")
    
    # Test polymerization method
    print("\nPolymerization Methods:")
    for monomer in ['ethylene', 'styrene', 'acrylonitrile', 'isobutylene']:
        result = polymerization_method(monomer)
        print(f"  {monomer}: {result['methods']}")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="crystallinity_effect",
            description="Predict properties based on crystallinity.",
            input_schema=[
            InputSchemaField(name="crystallinity", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="degree_of_polymerization",
            description="Calculate degree of polymerization.",
            input_schema=[
            InputSchemaField(name="monomer_mw", type="number", required=True),
            InputSchemaField(name="polymer_mw", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="polymer_type",
            description="Classify polymer and provide information.",
            input_schema=[
            InputSchemaField(name="polymer_name", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="polymerization_method",
            description="Recommend polymerization method for monomer.",
            input_schema=[
            InputSchemaField(name="monomer", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="step_growth_dp",
            description="Calculate DP from extent of reaction for step-growth.",
            input_schema=[
            InputSchemaField(name="extent", type="number", required=True)
            ],
            handler="{name}",
        )
    ]
