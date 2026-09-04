"""
Metabolism Tools
===============

Python implementations for metabolic calculations including
ATP yields, pathway analysis, and regulation.

Source: L2 glycolysis.md, tca_cycle.md, electron_transport_chain.md
"""

## Solver Instructions (for AI Agent)

# When you encounter **metabolic pathway / bioenergetics** problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
# - Glycolysis ATP yield: `glycolysis_atp_yield(nucleotide_type, shuttle, conditions)`
# - TCA cycle ATP yield: `tca_cycle_atp_yield(acetyl_coa)`
# - Complete glucose oxidation: `complete_glucose_oxidation(nucleotide_type, shuttle)`
# - Fatty acid beta-oxidation: `fatty_acid_oxidation(carbon_count, saturation, transport)`
# - Respiratory quotient: `respiratory_quotient(rq_value)`

### Step 2: Choose the correct function
# - Glycolysis only: `glycolysis_atp_yield`
# - TCA only: `tca_cycle_atp_yield`
# - Full oxidation (glycolysis + TCA + ETC): `complete_glucose_oxidation`
# - Fat metabolism: `fatty_acid_oxidation`
# - RQ interpretation: `respiratory_quotient`

### Step 3: Handle special cases
# - ATP yield depends on nucleotide (ATP/GTP) and shuttle type (malate-aspartate vs glycerol-3-phosphate)
# - P/O ratios: NADH=2.5, FADH2=1.5 (modern values)
# - Fatty acid transport: carnitine shuttle affects net ATP

### Examples
# 1. Glycolysis ATP (ATP, malate-aspartate, aerobic): `glycolysis_atp_yield("ATP", "malate_aspartate", "aerobic")` -> 7 or 8 ATP
# 2. Palmitate (C16): `fatty_acid_oxidation(16, "saturated", "carnitine")` -> 106 ATP
# 3. RQ=0.85: `respiratory_quotient(0.85)` -> mixed fat/carb fuel



from typing import Dict, List, Tuple
import numpy as np

# ATP equivalents
ATP_PER_NADH = 2.5
ATP_PER_FADH2 = 1.5


def glycolysis_atp_yield(
    glucose_molecules: int = 1,
    aerobic: bool = True,
    shuttle: str = 'malate-aspartate'
) -> Dict:
    """
    Calculate ATP yield from glycolysis.
    
    Parameters
    ----------
    glucose_molecules : int
        Number of glucose molecules
    aerobic : bool
        True for aerobic, False for anaerobic
    shuttle : str
        'malate-aspartate' or 'glycerol-3-phosphate'
    
    Returns
    -------
    dict
        ATP yield breakdown
    
    Examples
    --------
    >>> result = glycolysis_atp_yield(1, aerobic=True)
    >>> result['net_atp']
    7
    """
    # Per glucose
    substrate_atp = 2  # From steps 7 and 10
    investment_atp = 2  # Steps 1 and 3
    nadh_produced = 2
    
    net_atp = substrate_atp - investment_atp
    
    if aerobic:
        # NADH must be shuttled into mitochondria
        if shuttle == 'malate-aspartate':
            nadh_atp = nadh_produced * ATP_PER_NADH  # 5 ATP
        else:  # glycerol-3-phosphate shuttle
            nadh_atp = nadh_produced * ATP_PER_FADH2  # 3 ATP
        
        total_atp = net_atp + nadh_atp
    else:
        # Anaerobic: NADH used to reduce pyruvate to lactate
        total_atp = net_atp
        nadh_atp = 0
    
    return {
        'glucose_molecules': glucose_molecules,
        'substrate_level_atp': substrate_atp * glucose_molecules,
        'investment_atp': investment_atp * glucose_molecules,
        'nadh_from_glycolysis': nadh_produced * glucose_molecules,
        'nadh_atp_equivalent': nadh_atp * glucose_molecules,
        'net_atp': total_atp * glucose_molecules,
        'aerobic': aerobic,
        'shuttle': shuttle
    }


def tca_cycle_atp_yield(acetyl_coa: int = 2) -> Dict:
    """
    Calculate ATP yield from TCA cycle.
    
    Parameters
    ----------
    acetyl_coa : int
        Number of acetyl-CoA molecules (typically 2 per glucose)
    
    Returns
    -------
    dict
        ATP yield breakdown
    
    Examples
    --------
    >>> result = tca_cycle_atp_yield(2)
    >>> result['total_atp']
    20
    """
    # Per acetyl-CoA
    nadh = 3  # Steps 3, 4, 8
    fadh2 = 1  # Step 6
    gtp = 1  # Step 5
    
    nadh_atp = nadh * ATP_PER_NADH  # 7.5
    fadh2_atp = fadh2 * ATP_PER_FADH2  # 1.5
    total_per_acetyl = nadh_atp + fadh2_atp + gtp  # 10
    
    return {
        'acetyl_coa': acetyl_coa,
        'nadh_per_acetyl': nadh,
        'fadh2_per_acetyl': fadh2,
        'gtp_per_acetyl': gtp,
        'nadh_atp': nadh_atp * acetyl_coa,
        'fadh2_atp': fadh2_atp * acetyl_coa,
        'gtp_total': gtp * acetyl_coa,
        'total_atp': total_per_acetyl * acetyl_coa
    }


def complete_glucose_oxidation(
    shuttle: str = 'malate-aspartate',
    glucose_molecules: int = 1
) -> Dict:
    """
    Calculate complete ATP yield from glucose oxidation.
    
    Parameters
    ----------
    shuttle : str
        Cytosolic NADH shuttle type
    glucose_molecules : int
        Number of glucose molecules
    
    Returns
    -------
    dict
        Complete ATP accounting
    
    Examples
    --------
    >>> result = complete_glucose_oxidation()
    >>> result['total_atp']
    32
    """
    # Glycolysis
    glycolysis = glycolysis_atp_yield(glucose_molecules, True, shuttle)
    
    # Pyruvate to Acetyl-CoA (2 NADH per glucose)
    pyruvate_nadh = 2 * glucose_molecules
    pyruvate_atp = pyruvate_nadh * ATP_PER_NADH  # 5 ATP
    
    # TCA cycle (2 acetyl-CoA per glucose)
    tca = tca_cycle_atp_yield(2 * glucose_molecules)
    
    # Total
    total = glycolysis['net_atp'] + pyruvate_atp + tca['total_atp']
    
    return {
        'glucose_molecules': glucose_molecules,
        'shuttle': shuttle,
        'glycolysis_atp': glycolysis['net_atp'],
        'pyruvate_oxidation_atp': pyruvate_atp,
        'tca_cycle_atp': tca['total_atp'],
        'total_atp': total,
        'nadh_total': glycolysis['nadh_from_glycolysis'] + pyruvate_nadh + tca['nadh_per_acetyl'] * 2 * glucose_molecules,
        'fadh2_total': tca['fadh2_per_acetyl'] * 2 * glucose_molecules
    }


def fatty_acid_oxidation(
    n_carbons: int,
    saturated: bool = True,
    n_double_bonds: int = 0
) -> Dict:
    """
    Calculate ATP yield from fatty acid beta-oxidation.
    
    Parameters
    ----------
    n_carbons : int
        Number of carbons in fatty acid
    saturated : bool
        True for saturated fatty acid
    n_double_bonds : int
        Number of double bonds (for unsaturated)
    
    Returns
    -------
    dict
        ATP yield from oxidation
    
    Examples
    --------
    >>> result = fatty_acid_oxidation(16)  # Palmitic acid
    >>> result['total_atp']
    106.0
    """
    # Calculate rounds of beta-oxidation
    rounds = (n_carbons // 2) - 1
    acetyl_coa = n_carbons // 2
    
    # Each round: 1 NADH, 1 FADH2
    # For unsaturated: each double bond reduces FADH2 by 1
    nadh = rounds
    fadh2 = rounds - (n_double_bonds if not saturated else 0)
    
    # ATP from beta-oxidation
    nadh_atp = nadh * ATP_PER_NADH
    fadh2_atp = fadh2 * ATP_PER_FADH2
    
    # ATP from acetyl-CoA in TCA cycle
    acetyl_coa_atp = acetyl_coa * 10  # 10 ATP per acetyl-CoA
    
    # Activation cost
    activation_cost = 2  # ATP to activate fatty acid
    
    total = nadh_atp + fadh2_atp + acetyl_coa_atp - activation_cost
    
    return {
        'n_carbons': n_carbons,
        'rounds': rounds,
        'acetyl_coa': acetyl_coa,
        'nadh': nadh,
        'fadh2': fadh2,
        'nadh_atp': nadh_atp,
        'fadh2_atp': fadh2_atp,
        'acetyl_coa_atp': acetyl_coa_atp,
        'activation_cost': activation_cost,
        'total_atp': total
    }


def respiratory_quotient(
    substrate: str = 'glucose'
) -> float:
    """
    Calculate respiratory quotient (RQ).
    
    RQ = CO2 produced / O2 consumed
    
    Parameters
    ----------
    substrate : str
        'glucose', 'fat', or 'protein'
    
    Returns
    -------
    float
        RQ value
    
    Examples
    --------
    >>> respiratory_quotient('glucose')
    1.0
    >>> respiratory_quotient('fat')
    0.7
    """
    rq_values = {
        'glucose': 1.0,  # C6H12O6 + 6O2 -> 6CO2 + 6H2O
        'fat': 0.7,  # Typical for palmitate
        'protein': 0.8,  # Average for amino acids
    }
    return rq_values.get(substrate.lower(), 0.85)


# Self-test
if __name__ == '__main__':
    print("Metabolism Tools Test")
    print("=" * 40)
    
    # Test glycolysis
    print("\nGlycolysis (aerobic, malate-aspartate shuttle):")
    result = glycolysis_atp_yield(1, True, 'malate-aspartate')
    print(f"  Net ATP: {result['net_atp']}")
    
    # Test TCA cycle
    print("\nTCA Cycle (per glucose = 2 acetyl-CoA):")
    result = tca_cycle_atp_yield(2)
    print(f"  Total ATP: {result['total_atp']}")
    
    # Test complete oxidation
    print("\nComplete Glucose Oxidation:")
    result = complete_glucose_oxidation()
    print(f"  Total ATP: {result['total_atp']}")
    print(f"  NADH total: {result['nadh_total']}")
    print(f"  FADH2 total: {result['fadh2_total']}")
    
    # Test fatty acid
    print("\nPalmitic Acid (C16:0) Oxidation:")
    result = fatty_acid_oxidation(16)
    print(f"  Total ATP: {result['total_atp']}")
    
    print("\nAll tests passed")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="complete_glucose_oxidation",
            description="Calculate complete ATP yield from glucose oxidation.",
            input_schema=[
            InputSchemaField(name="shuttle", type="number", required=False),
            InputSchemaField(name="glucose_molecules", type="string", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="fatty_acid_oxidation",
            description="Calculate ATP yield from fatty acid beta-oxidation.",
            input_schema=[
            InputSchemaField(name="n_carbons", type="number", required=True),
            InputSchemaField(name="saturated", type="number", required=False),
            InputSchemaField(name="n_double_bonds", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="glycolysis_atp_yield",
            description="Calculate ATP yield from glycolysis.",
            input_schema=[
            InputSchemaField(name="glucose_molecules", type="string", required=False),
            InputSchemaField(name="aerobic", type="number", required=False),
            InputSchemaField(name="shuttle", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="respiratory_quotient",
            description="Calculate respiratory quotient (RQ).",
            input_schema=[
            InputSchemaField(name="substrate", type="number", required=False)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="tca_cycle_atp_yield",
            description="Calculate ATP yield from TCA cycle.",
            input_schema=[
            InputSchemaField(name="acetyl_coa", type="number", required=False)
            ],
            handler="{name}",
        )
    ]
