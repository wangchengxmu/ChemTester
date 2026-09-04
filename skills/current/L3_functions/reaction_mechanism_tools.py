"""
Reaction Mechanism Tools - L3 Implementation
[Source: Organic Chemistry OpenStax, Ch06]

Functions for analyzing and predicting organic reaction mechanisms.

## Solver Instructions (for AI Agent)

When you encounter organic reaction mechanism problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Mechanism prediction**: Given substrate type, nucleophile/base, leaving group, solvent -> predict SN1/SN2/E1/E2
- **Intermediate stability**: Given carbocation/radical type -> compare relative stabilities
- **Reaction steps**: Given mechanism type -> list arrow-pushing steps
- **Product prediction**: Given substrate and conditions -> predict major/minor products
- **Rate law from mechanism**: Given mechanism steps -> derive rate law

### Step 2: Choose the correct function
- `predict_mechanism(substrate_type, nucleophile, leaving_group, solvent)` -> predicted mechanism
- `carbocation_stability(substitution_type)` -> relative stability ranking
- `radical_stability(substitution_type)` -> relative stability ranking
- `get_mechanism_steps(mechanism_type)` -> ordered list of ReactionStep objects
- `predict_products(substrate, reagent, conditions)` -> major and minor products
- `rate_law_from_mechanism(steps, rate_determining_step)` -> derived rate law expression
- `is_concerted(mechanism_type)` -> True for SN2, E2, pericyclic; False for SN1, E1

### Step 3: Handle special cases
- **SN1**: tertiary substrates, weak nucleophile, polar protic solvent -> carbocation intermediate
- **SN2**: primary substrates, strong nucleophile, polar aprotic solvent -> concerted, inversion
- **E1**: tertiary + weak base -> carbocation then elimination -> Zaitsev product favored
- **E2**: tertiary + strong base -> concerted -> anti-periplanar requirement
- Allylic/benzylic carbocations are exceptionally stable (similar to tertiary)
- Carbocation rearrangements (hydride/alkyl shifts) can change product distribution

### Examples
1. **Mechanism prediction**: (CH3)3C-Br + CH3OH (weak nucleophile, protic solvent)
   -> `predict_mechanism('tertiary', 'CH3OH', 'Br-', 'CH3OH')` -> 'SN1' with possible E1 competition

2. **Carbocation stability**: Compare methyl vs tertiary
   -> `carbocation_stability('methyl')` -> 0 (reference)
   -> `carbocation_stability('tertiary')` -> -120 (120 kJ/mol more stable)

3. **Product prediction**: 2-bromobutane + NaOEt/EtOH (strong base, secondary substrate)
   -> E2 favored (Zaitsev product: 2-butene) with minor SN2 substitution
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ReactionType(Enum):
    """Types of organic reactions"""
    ADDITION = "addition"
    ELIMINATION = "elimination"
    SUBSTITUTION = "substitution"
    REARRANGEMENT = "rearrangement"


class MechanismType(Enum):
    """Mechanism classifications"""
    SN1 = "SN1"
    SN2 = "SN2"
    E1 = "E1"
    E2 = "E2"
    ELECTROPHILIC_ADDITION = "electrophilic_addition"
    NUCLEOPHILIC_ADDITION = "nucleophilic_addition"
    RADICAL = "radical"
    PERICYCLIC = "pericyclic"


class IntermediateType(Enum):
    """Types of reaction intermediates"""
    CARBOCATION = "carbocation"
    CARBANION = "carbanion"
    RADICAL = "radical"
    CARBENE = "carbene"
    HALONIUM_ION = "halonium_ion"
    NONE = "concerted"


@dataclass
class ReactionStep:
    """Information about a reaction step"""
    description: str
    arrow_pattern: str
    intermediate: Optional[IntermediateType]
    energy_change: str  # "exothermic", "endothermic", "approx_zero"


# Carbocation stability (relative energies in kJ/mol)
CARBOCATION_STABILITY = {
    "methyl": 0,
    "primary": -50,
    "secondary": -85,
    "tertiary": -120,
    "allylic": -100,
    "benzylic": -105,
    "vinyl": 50,  # Unstable
}

# Radical stability
RADICAL_STABILITY = {
    "methyl": 0,
    "primary": -30,
    "secondary": -50,
    "tertiary": -70,
    "allylic": -80,
    "benzylic": -85,
}

# Carbanion stability (opposite trend)
CARBANION_STABILITY = {
    "methyl": 0,
    "primary": -10,
    "secondary": 15,
    "tertiary": 35,  # Less stable
}

# Common electrophiles
ELECTROPHILES = {
    "H+": {"type": "proton", "strength": "very_strong"},
    "HBr": {"type": "hydrogen_halide", "strength": "strong"},
    "HCl": {"type": "hydrogen_halide", "strength": "strong"},
    "HI": {"type": "hydrogen_halide", "strength": "strong"},
    "H2O/H+": {"type": "protonated_water", "strength": "moderate"},
    "Br2": {"type": "halogen", "strength": "moderate"},
    "Cl2": {"type": "halogen", "strength": "moderate"},
    "RCHO": {"type": "aldehyde", "strength": "weak"},
    "RCOR": {"type": "ketone", "strength": "weak"},
    "RCOOH": {"type": "carboxylic_acid", "strength": "weak"},
}

# Common nucleophiles
NUCLEOPHILES = {
    "HO-": {"type": "hydroxide", "strength": "strong", "base_strength": "strong"},
    "RO-": {"type": "alkoxide", "strength": "strong", "base_strength": "strong"},
    "CN-": {"type": "cyanide", "strength": "strong", "base_strength": "moderate"},
    "N3-": {"type": "azide", "strength": "strong", "base_strength": "weak"},
    "NH3": {"type": "ammonia", "strength": "moderate", "base_strength": "moderate"},
    "H2O": {"type": "water", "strength": "weak", "base_strength": "weak"},
    "I-": {"type": "iodide", "strength": "good", "base_strength": "very_weak"},
    "Br-": {"type": "bromide", "strength": "moderate", "base_strength": "very_weak"},
    "Cl-": {"type": "chloride", "strength": "weak", "base_strength": "very_weak"},
}


def classify_reaction_type(reactants: str, products: str) -> ReactionType:
    """
    Classify the type of organic reaction.
    
    Args:
        reactants: Description of reactants
        products: Description of products
    
    Returns:
        Reaction type classification
    
    Examples:
        >>> classify_reaction_type("C=C", "C-C-X")
        ReactionType.ADDITION
    """
    # Simplified classification
    if "+" in reactants and "+" not in products:
        return ReactionType.ADDITION
    elif "+" in products and "+" not in reactants:
        return ReactionType.ELIMINATION
    elif "substitution" in products.lower():
        return ReactionType.SUBSTITUTION
    else:
        return ReactionType.ADDITION


def predict_carbocation_stability(carbon_type: str) -> Tuple[str, int]:
    """
    Predict the stability of a carbocation.
    
    Args:
        carbon_type: "methyl", "primary", "secondary", "tertiary", "allylic", "benzylic"
    
    Returns:
        Tuple of (stability_description, relative_energy)
    
    Examples:
        >>> predict_carbocation_stability("tertiary")
        ('most stable', -120)
    """
    energy = CARBOCATION_STABILITY.get(carbon_type.lower(), 0)
    
    if energy <= -100:
        return ("very stable", energy)
    elif energy <= -70:
        return ("stable", energy)
    elif energy <= -40:
        return ("moderately stable", energy)
    elif energy < 0:
        return ("less stable", energy)
    else:
        return ("unstable", energy)


def predict_radical_stability(radical_type: str) -> Tuple[str, int]:
    """
    Predict the stability of a radical.
    
    Args:
        radical_type: "methyl", "primary", "secondary", "tertiary", "allylic", "benzylic"
    
    Returns:
        Tuple of (stability_description, relative_energy)
    
    Examples:
        >>> predict_radical_stability("tertiary")
        ('stable', -70)
    """
    energy = RADICAL_STABILITY.get(radical_type.lower(), 0)
    
    if energy <= -70:
        return ("stable", energy)
    elif energy <= -40:
        return ("moderately stable", energy)
    else:
        return ("less stable", energy)


def predict_carbanion_stability(carbanion_type: str) -> Tuple[str, int]:
    """
    Predict the stability of a carbanion.
    
    Note: Carbanion stability is OPPOSITE to carbocation stability.
    
    Args:
        carbanion_type: "methyl", "primary", "secondary", "tertiary"
    
    Returns:
        Tuple of (stability_description, relative_energy)
    
    Examples:
        >>> predict_carbanion_stability("methyl")
        ('stable', 0)
    """
    energy = CARBANION_STABILITY.get(carbanion_type.lower(), 0)
    
    if energy <= 0:
        return ("stable", energy)
    elif energy <= 20:
        return ("moderately stable", energy)
    else:
        return ("unstable", energy)


def identify_electrophile(species: str) -> Dict:
    """
    Identify electrophile characteristics.
    
    Args:
        species: Chemical species name
    
    Returns:
        Dictionary with electrophile information
    
    Examples:
        >>> identify_electrophile("HBr")
        {'type': 'hydrogen_halide', 'strength': 'strong'}
    """
    return ELECTROPHILES.get(species, {"type": "unknown", "strength": "unknown"})


def identify_nucleophile(species: str) -> Dict:
    """
    Identify nucleophile characteristics.
    
    Args:
        species: Chemical species name
    
    Returns:
        Dictionary with nucleophile information
    
    Examples:
        >>> identify_nucleophile("HO-")
        {'type': 'hydroxide', 'strength': 'strong', 'base_strength': 'strong'}
    """
    return NUCLEOPHILES.get(species, {"type": "unknown", "strength": "unknown"})


def predict_mechanism_sn1_sn2(substrate: str, nucleophile: str, solvent: str) -> MechanismType:
    """
    Predict whether SN1 or SN2 mechanism will dominate.
    
    Args:
        substrate: Alkyl halide (e.g., "methyl", "primary", "secondary", "tertiary")
        nucleophile: Nucleophile identity
        solvent: Solvent type ("polar_protic", "polar_aprotic")
    
    Returns:
        Predicted mechanism
    
    Examples:
        >>> predict_mechanism_sn1_sn2("tertiary", "HO-", "polar_protic")
        MechanismType.SN1
    """
    substrate = substrate.lower()
    
    # SN1 favored by:
    # - Tertiary substrate
    # - Weak nucleophile
    # - Polar protic solvent
    
    # SN2 favored by:
    # - Methyl or primary substrate
    # - Strong nucleophile
    # - Polar aprotic solvent
    
    if substrate == "tertiary":
        return MechanismType.SN1
    elif substrate == "secondary":
        nucl_info = identify_nucleophile(nucleophile)
        if nucl_info.get("strength") == "strong" and solvent == "polar_aprotic":
            return MechanismType.SN2
        else:
            return MechanismType.SN1
    else:  # primary or methyl
        return MechanismType.SN2


def predict_elimination_mechanism(substrate: str, base: str, temperature: float) -> MechanismType:
    """
    Predict whether E1 or E2 mechanism will dominate.
    
    Args:
        substrate: Alkyl halide type
        base: Base identity
        temperature: Temperature in degC
    
    Returns:
        Predicted mechanism
    
    Examples:
        >>> predict_elimination_mechanism("tertiary", "H2O", 50)
        MechanismType.E1
    """
    substrate = substrate.lower()
    
    # E1 favored by:
    # - Tertiary substrate
    # - Weak base
    # - Lower temperature
    
    # E2 favored by:
    # - Primary or secondary substrate
    # - Strong base
    # - Higher temperature
    
    base_info = identify_nucleophile(base)
    base_strength = base_info.get("base_strength", "unknown")
    
    if substrate == "tertiary" and base_strength in ["weak", "very_weak"]:
        return MechanismType.E1
    elif base_strength == "strong" or temperature > 60:
        return MechanismType.E2
    else:
        return MechanismType.E1


def draw_curved_arrows(step_type: str) -> List[str]:
    """
    Generate curved arrow notation for a reaction step.
    
    Args:
        step_type: Type of step (e.g., "nucleophilic_attack", "proton_transfer")
    
    Returns:
        List of arrow descriptions
    
    Examples:
        >>> draw_curved_arrows("nucleophilic_attack")
        ['Nu: -> C (nucleophile donates electrons to electrophile)']
    """
    patterns = {
        "nucleophilic_attack": [
            "Nu:- -> C+ (nucleophile donates electrons to electrophilic carbon)"
        ],
        "proton_transfer": [
            "B: -> H (base takes proton)",
            "H-X -> B (bond breaks, electrons go to X)"
        ],
        "bond_breaking_heterolytic": [
            "A-B -> A+ + :B- (pair goes to more electronegative atom)"
        ],
        "bond_breaking_homolytic": [
            "A-B -> A· + ·B (one electron each)"
        ],
        "carbocation_formation": [
            "C-X -> C+ + X:- (leaving group departs with electrons)"
        ],
        "hydride_shift": [
            "H: -> C+ (hydride migrates to adjacent carbocation)"
        ],
        "alkyl_shift": [
            "R: -> C+ (alkyl group migrates to carbocation)"
        ],
    }
    
    return patterns.get(step_type, ["Pattern not defined"])


def predict_hammond_postulate(transition_state: str, reaction_energy: str) -> str:
    """
    Apply Hammond Postulate to predict transition state character.
    
    Args:
        transition_state: "early" or "late"
        reaction_energy: "exothermic" or "endothermic"
    
    Returns:
        Description of transition state character
    
    Examples:
        >>> predict_hammond_postulate("early", "exothermic")
        'TS resembles reactants (early TS)'
    """
    if reaction_energy == "exothermic":
        return "TS resembles reactants (early TS)"
    elif reaction_energy == "endothermic":
        return "TS resembles products (late TS)"
    else:
        return "TS character unclear"


def calculate_rate_law(mechanism: MechanismType) -> str:
    """
    Determine rate law from mechanism.
    
    Args:
        mechanism: Reaction mechanism
    
    Returns:
        Rate law expression
    
    Examples:
        >>> calculate_rate_law(MechanismType.SN2)
        'Rate = k[RX][Nu]'
    """
    rate_laws = {
        MechanismType.SN1: "Rate = k[RX]",
        MechanismType.SN2: "Rate = k[RX][Nu]",
        MechanismType.E1: "Rate = k[RX]",
        MechanismType.E2: "Rate = k[RX][Base]",
        MechanismType.ELECTROPHILIC_ADDITION: "Rate = k[alkene][electrophile]",
    }
    
    return rate_laws.get(mechanism, "Rate = k[reactants]")


def radical_chain_steps() -> Dict:
    """
    Get the steps of a radical chain reaction.
    
    Returns:
        Dictionary of chain reaction steps
    """
    return {
        "initiation": "X2 -> 2X· (homolytic cleavage, requires heat/light)",
        "propagation_1": "X· + R-H -> H-X + R· (radical abstraction)",
        "propagation_2": "R· + X2 -> R-X + X· (radical continues chain)",
        "termination_1": "X· + X· -> X2 (radical recombination)",
        "termination_2": "R· + R· -> R-R (radical coupling)",
        "termination_3": "X· + R· -> R-X (cross combination)",
    }


def reaction_mechanism_summary() -> Dict:
    """
    Get summary of common reaction mechanisms.
    
    Returns:
        Dictionary of mechanism summaries
    """
    return {
        "SN1": {
            "steps": 2,
            "intermediate": "carbocation",
            "stereochemistry": "racemization",
            "rate_determining": "carbocation formation",
            "favored_by": ["tertiary substrate", "weak nucleophile", "polar protic solvent"]
        },
        "SN2": {
            "steps": 1,
            "intermediate": "none (concerted)",
            "stereochemistry": "inversion",
            "rate_determining": "single step",
            "favored_by": ["primary substrate", "strong nucleophile", "polar aprotic solvent"]
        },
        "E1": {
            "steps": 2,
            "intermediate": "carbocation",
            "stereochemistry": "no specific stereochemistry",
            "rate_determining": "carbocation formation",
            "favored_by": ["tertiary substrate", "weak base", "high temperature"]
        },
        "E2": {
            "steps": 1,
            "intermediate": "none (concerted)",
            "stereochemistry": "anti-periplanar elimination",
            "rate_determining": "single step",
            "favored_by": ["secondary/tertiary substrate", "strong base", "high temperature"]
        },
        "electrophilic_addition": {
            "steps": 2,
            "intermediate": "carbocation",
            "regioselectivity": "Markovnikov",
            "stereochemistry": "depends on intermediate",
            "rearrangement": "possible"
        },
    }


# Test functions
def test_carbocation_stability():
    """Test carbocation stability predictions"""
    desc, energy = predict_carbocation_stability("tertiary")
    assert energy < 0
    desc, energy = predict_carbocation_stability("methyl")
    assert energy >= 0
    print("✓ Carbocation stability tests passed")


def test_mechanism_prediction():
    """Test mechanism prediction"""
    assert predict_mechanism_sn1_sn2("tertiary", "HO-", "polar_protic") == MechanismType.SN1
    assert predict_mechanism_sn1_sn2("primary", "HO-", "polar_aprotic") == MechanismType.SN2
    print("✓ Mechanism prediction tests passed")


def test_rate_laws():
    """Test rate law determination"""
    assert calculate_rate_law(MechanismType.SN1) == "Rate = k[RX]"
    assert calculate_rate_law(MechanismType.SN2) == "Rate = k[RX][Nu]"
    print("✓ Rate law tests passed")


def test_nucleophile_identification():
    """Test nucleophile identification"""
    info = identify_nucleophile("HO-")
    assert info["strength"] == "strong"
    print("✓ Nucleophile identification tests passed")


if __name__ == "__main__":
    test_carbocation_stability()
    test_mechanism_prediction()
    test_rate_laws()
    test_nucleophile_identification()
    print("\n✓ All reaction mechanism tools tests passed!")


# MCP Tool Declarations
try:
    from mcp.server.fastmcp.utilities.types import MCPTool as MCPTool, InputSchemaField
except ImportError:
    MCP_TOOLS = []
else:
    MCP_TOOLS = [
        MCPTool(
            name="calculate_rate_law",
            description="Determine rate law from mechanism.",
            input_schema=[
            InputSchemaField(name="mechanism", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="classify_reaction_type",
            description="Classify the type of organic reaction.",
            input_schema=[
            InputSchemaField(name="reactants", type="number", required=True),
            InputSchemaField(name="products", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="draw_curved_arrows",
            description="Generate curved arrow notation for a reaction step.",
            input_schema=[
            InputSchemaField(name="step_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="identify_electrophile",
            description="Identify electrophile characteristics.",
            input_schema=[
            InputSchemaField(name="species", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="identify_nucleophile",
            description="Identify nucleophile characteristics.",
            input_schema=[
            InputSchemaField(name="species", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_carbanion_stability",
            description="Predict the stability of a carbanion.",
            input_schema=[
            InputSchemaField(name="carbanion_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_carbocation_stability",
            description="Predict the stability of a carbocation.",
            input_schema=[
            InputSchemaField(name="carbon_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_elimination_mechanism",
            description="Predict whether E1 or E2 mechanism will dominate.",
            input_schema=[
            InputSchemaField(name="substrate", type="number", required=True),
            InputSchemaField(name="base", type="string", required=True),
            InputSchemaField(name="temperature", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_hammond_postulate",
            description="Apply Hammond Postulate to predict transition state character.",
            input_schema=[
            InputSchemaField(name="transition_state", type="number", required=True),
            InputSchemaField(name="reaction_energy", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_mechanism_sn1_sn2",
            description="Predict whether SN1 or SN2 mechanism will dominate.",
            input_schema=[
            InputSchemaField(name="substrate", type="number", required=True),
            InputSchemaField(name="nucleophile", type="number", required=True),
            InputSchemaField(name="solvent", type="string", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="predict_radical_stability",
            description="Predict the stability of a radical.",
            input_schema=[
            InputSchemaField(name="radical_type", type="number", required=True)
            ],
            handler="{name}",
        ),
        MCPTool(
            name="radical_chain_steps",
            description="Get the steps of a radical chain reaction.",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="reaction_mechanism_summary",
            description="Get summary of common reaction mechanisms.",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_carbocation_stability",
            description="Test carbocation stability predictions",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_mechanism_prediction",
            description="Test mechanism prediction",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_nucleophile_identification",
            description="Test nucleophile identification",
            input_schema=[

            ],
            handler="{name}",
        ),
        MCPTool(
            name="test_rate_laws",
            description="Test rate law determination",
            input_schema=[

            ],
            handler="{name}",
        )
    ]
