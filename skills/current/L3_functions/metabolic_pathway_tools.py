"""
L3 Tool: Metabolic Pathway Tools
Calculate ATP yields and pathway outputs.

Source: Organic Chemistry (OpenStax) Ch29
Created: 2026-03-13
"""
## Solver Instructions (for AI Agent)

# When you encounter metabolic pathway ATP yield problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: fatty acid carbon count, saturation, glucose molecules, pathway name
# - **Asked**: total ATP, NADH/FADH2 count, rounds of beta-oxidation, acetyl CoA count

### Step 2: Choose the correct function
# | Task | Function | Key Parameters |
# |---|---|---|
# | Fatty acid ATP yield | `fatty_acid_atp_yield(n_carbons, saturated, n_double_bonds)` | C count |
# | beta-oxidation rounds | `beta_oxidation_rounds(n_carbons)` | n carbons |
# | Acetyl CoA from FA | `acetyl_coa_from_fatty_acid(n_carbons)` | n carbons |
# | Glycolysis products | `glycolysis_products(glucose_molecules)` | n glucose |
# | CAC yield | `citric_acid_cycle_yield(acetyl_coa_molecules)` | n acetyl CoA |
# | Total ATP from glucose | `total_atp_from_glucose(aerobic)` | True/False |
# | Gluconeogenesis cost | `gluconeogenesis_energy_cost()` | no params |

### Step 3: Handle special cases
# - Unsaturated FAs: each double bond reduces FADH2 by 1 (skip first oxidation step)
# - Constants: ATP/acetyl-CoA = 10, ATP/NADH = 2.5, ATP/FADH2 = 1.5
# - Aerobic glucose: ~30-32 ATP total; Anaerobic: 2 ATP only

### Examples
# 1. **Palmitic acid (C16)**: `fatty_acid_atp_yield(16)` -> 7 rounds, 8 acetyl-CoA, ~106 ATP
# 2. **Stearic acid (C18)**: `fatty_acid_atp_yield(18)` -> 8 rounds, 9 acetyl-CoA, ~120 ATP
# 3. **Total glucose ATP**: `total_atp_from_glucose(aerobic=True)` -> 32 ATP breakdown
# 4. **Glycolysis**: `glycolysis_products(2)` -> 4 ATP, 4 NADH, 4 pyruvate


# ATP yield constants
ATP_PER_ACETYL_COA = 10  # Via citric acid cycle
ATP_PER_NADH = 2.5
ATP_PER_FADH2 = 1.5

# Common fatty acids
FATTY_ACIDS = {
    'capric': 10,
    'lauric': 12,
    'myristic': 14,
    'palmitic': 16,
    'palmitoleic': 16,  # Monounsaturated
    'stearic': 18,
    'oleic': 18,  # Monounsaturated
    'linoleic': 18,  # Diunsaturated
    'arachidic': 20,
    'arachidonic': 20,  # Tetraunsaturated
    'behenic': 22,
    'lignoceric': 24,
}


def fatty_acid_atp_yield(n_carbons: int, saturated: bool = True, n_double_bonds: int = 0) -> dict:
    """
    Calculate ATP yield from beta-oxidation of fatty acid.
    
    For saturated fatty acids:
    - Rounds = n/2 - 1
    - Each round produces: 1 NADH, 1 FADH2
    - Each acetyl CoA yields ~10 ATP via CAC
    
    For unsaturated fatty acids:
    - Each double bond reduces FADH2 by 1 (skip step 1)
    
    Args:
        n_carbons: Number of carbons in fatty acid
        saturated: Whether fatty acid is saturated
        n_double_bonds: Number of double bonds (for unsaturated)
    
    Returns:
        Dictionary with ATP, NADH, FADH2, acetyl CoA counts
    
    Example:
        >>> fatty_acid_atp_yield(16)
        {'atp': 106.0, 'rounds': 7, 'acetyl_coa': 8, 'nadh': 7, 'fadh2': 7}
    """
    # Calculate basic values
    rounds = (n_carbons // 2) - 1
    acetyl_coa = n_carbons // 2
    
    # For unsaturated, adjust FADH2
    fadh2 = rounds - n_double_bonds if not saturated else rounds
    nadh = rounds
    
    # Calculate ATP
    atp = (acetyl_coa * ATP_PER_ACETYL_COA + 
           nadh * ATP_PER_NADH + 
           fadh2 * ATP_PER_FADH2)
    
    return {
        'n_carbons': n_carbons,
        'atp': atp,
        'rounds': rounds,
        'acetyl_coa': acetyl_coa,
        'nadh': nadh,
        'fadh2': fadh2,
        'saturated': saturated,
        'n_double_bonds': n_double_bonds
    }


def beta_oxidation_rounds(n_carbons: int) -> int:
    """
    Calculate number of beta-oxidation rounds.
    
    Formula: rounds = n/2 - 1
    
    Args:
        n_carbons: Number of carbons in fatty acid
    
    Returns:
        Number of rounds
    
    Example:
        >>> beta_oxidation_rounds(16)
        7
    """
    return (n_carbons // 2) - 1


def acetyl_coa_from_fatty_acid(n_carbons: int) -> int:
    """
    Calculate number of acetyl CoA produced.
    
    Formula: acetyl_coa = n/2
    
    Args:
        n_carbons: Number of carbons in fatty acid
    
    Returns:
        Number of acetyl CoA molecules
    """
    return n_carbons // 2


def glycolysis_products(glucose_molecules: int = 1) -> dict:
    """
    Net products from glycolysis per glucose.
    
    Per glucose:
    - 2 ATP (net)
    - 2 NADH
    - 2 Pyruvate
    
    Args:
        glucose_molecules: Number of glucose molecules
    
    Returns:
        Dictionary with ATP, NADH, pyruvate counts
    """
    return {
        'glucose': glucose_molecules,
        'atp': 2 * glucose_molecules,
        'nadh': 2 * glucose_molecules,
        'pyruvate': 2 * glucose_molecules
    }


def citric_acid_cycle_yield(acetyl_coa_molecules: int = 1) -> dict:
    """
    Products per acetyl CoA from citric acid cycle.
    
    Per acetyl CoA:
    - 3 NADH
    - 1 FADH2
    - 1 GTP (~ 1 ATP)
    - 2 CO2
    
    Args:
        acetyl_coa_molecules: Number of acetyl CoA molecules
    
    Returns:
        Dictionary with NADH, FADH2, GTP, CO2 counts
    """
    return {
        'acetyl_coa': acetyl_coa_molecules,
        'nadh': 3 * acetyl_coa_molecules,
        'fadh2': 1 * acetyl_coa_molecules,
        'gtp': 1 * acetyl_coa_molecules,
        'co2': 2 * acetyl_coa_molecules
    }


def total_atp_from_glucose(aerobic: bool = True) -> dict:
    """
    Calculate total ATP from complete glucose oxidation.
    
    Aerobic:
    - Glycolysis: 2 ATP + 2 NADH
    - Pyruvate -> Acetyl CoA: 2 NADH
    - CAC (2 acetyl CoA): 6 NADH + 2 FADH2 + 2 GTP
    
    Total ~ 30-32 ATP
    
    Args:
        aerobic: Whether aerobic conditions
    
    Returns:
        Dictionary with ATP breakdown
    """
    if aerobic:
        # Glycolysis
        glycolysis_atp = 2
        glycolysis_nadh = 2 * ATP_PER_NADH  # 5 ATP equivalent
        
        # Pyruvate to acetyl CoA
        pyruvate_nadh = 2 * ATP_PER_NADH  # 5 ATP equivalent
        
        # CAC
        cac_nadh = 6 * ATP_PER_NADH  # 15 ATP equivalent
        cac_fadh2 = 2 * ATP_PER_FADH2  # 3 ATP equivalent
        cac_gtp = 2  # 2 ATP equivalent
        
        total = (glycolysis_atp + glycolysis_nadh + pyruvate_nadh + 
                 cac_nadh + cac_fadh2 + cac_gtp)
        
        return {
            'total_atp': total,
            'glycolysis_atp': 2,
            'glycolysis_nadh_atp': glycolysis_nadh,
            'pyruvate_nadh_atp': pyruvate_nadh,
            'cac_nadh_atp': cac_nadh,
            'cac_fadh2_atp': cac_fadh2,
            'cac_gtp': 2,
            'conditions': 'aerobic'
        }
    else:
        # Anaerobic: only glycolysis + fermentation
        return {
            'total_atp': 2,
            'glycolysis_atp': 2,
            'conditions': 'anaerobic'
        }


def gluconeogenesis_energy_cost() -> dict:
    """
    Energy cost to synthesize one glucose molecule.
    
    From pyruvate:
    - Pyruvate -> OAA -> PEP: 2 ATP + 1 GTP per pyruvate
    - 1,3-BPG -> G3P bypass: 1 ATP
    - Glucose-6-P -> Glucose: 1 ATP equivalent
    
    Total: 4 ATP + 2 GTP + 2 NADH per glucose
    
    Returns:
        Dictionary with energy cost breakdown
    """
    return {
        'atp': 4,
        'gtp': 2,
        'nadh': 2,
        'total_equivalent_atp': 6 + 2 * ATP_PER_NADH,  # ~ 11
        'precursor': 'pyruvate'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "29-01",
        "question": "beta-Oxidation rounds for palmitic acid (C16)",
        "n_carbons": 16,
        "expected_rounds": 7,
        "expected_acetyl": 8
    },
    {
        "id": "29-02",
        "question": "ATP from stearic acid (C18)",
        "n_carbons": 18,
        "expected_rounds": 8,
        "expected_acetyl": 9
    },
    {
        "id": "29-03",
        "question": "Glycolysis net products",
        "expected_atp": 2,
        "expected_nadh": 2,
        "expected_pyruvate": 2
    },
    {
        "id": "29-04",
        "question": "CAC products per acetyl CoA",
        "expected_nadh": 3,
        "expected_fadh2": 1,
        "expected_gtp": 1
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Metabolic Pathway Tools")
    print("=" * 40)
    
    # Test beta-oxidation
    print("\nbeta-Oxidation:")
    for name, carbons in [('Palmitic', 16), ('Stearic', 18)]:
        result = fatty_acid_atp_yield(carbons)
        print(f"  {name} acid (C{carbons}): {result['rounds']} rounds, {result['acetyl_coa']} acetyl CoA, ~{result['atp']:.0f} ATP")
    
    # Test glycolysis
    print("\nGlycolysis (per glucose):")
    result = glycolysis_products()
    print(f"  {result['atp']} ATP, {result['nadh']} NADH, {result['pyruvate']} pyruvate")
    
    # Test CAC
    print("\nCitric Acid Cycle (per acetyl CoA):")
    result = citric_acid_cycle_yield()
    print(f"  {result['nadh']} NADH, {result['fadh2']} FADH2, {result['gtp']} GTP, {result['co2']} CO2")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="acetyl_coa_from_fatty_acid",
            description="Calculate number of acetyl CoA produced.",
            input_schema=[
            InputSchemaField(name="n_carbons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="beta_oxidation_rounds",
            description="Calculate number of beta-oxidation rounds.",
            input_schema=[
            InputSchemaField(name="n_carbons", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="citric_acid_cycle_yield",
            description="Products per acetyl CoA from citric acid cycle.",
            input_schema=[
            InputSchemaField(name="acetyl_coa_molecules", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fatty_acid_atp_yield",
            description="Calculate ATP yield from beta-oxidation of fatty acid.",
            input_schema=[
            InputSchemaField(name="n_carbons", type="number", required=True),
            InputSchemaField(name="saturated", type="number", required=False),
            InputSchemaField(name="n_double_bonds", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="gluconeogenesis_energy_cost",
            description="Energy cost to synthesize one glucose molecule.",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="glycolysis_products",
            description="Net products from glycolysis per glucose.",
            input_schema=[
            InputSchemaField(name="glucose_molecules", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="total_atp_from_glucose",
            description="Calculate total ATP from complete glucose oxidation.",
            input_schema=[
            InputSchemaField(name="aerobic", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
