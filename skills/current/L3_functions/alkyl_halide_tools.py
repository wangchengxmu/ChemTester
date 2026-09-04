"""
Alkyl Halide Chemistry Tools

Implements tools for:
1. Alkyl halide nomenclature
2. C-X bond property lookup
3. Radical halogenation product prediction
4. Reactivity calculations
5. Allylic bromination prediction
6. Grignard reagent formation
7. Organometallic coupling

Source: Organic Chemistry (OpenStax), Ch10

## Solver Instructions (for AI Agent)

When you encounter alkyl halide reactions, radical halogenation, Grignard chemistry, or organometallic coupling problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a molecule + halogen -> predict radical halogenation products?
- Given C-X bond question -> need bond length, strength, or dipole?
- Given an alkene + NBS -> predict allylic bromination product?
- Given an alkyl halide + Mg -> Grignard formation?
- Given two coupling partners -> predict coupling product?
- Need to convert alcohol to alkyl halide -> select reagent?
- Given oxidation states -> classify as oxidation or reduction?

### Step 2: Choose the correct function
- **C-X bond properties:** `get_cx_bond_property(halogen, property_name)` -> 'F'/'Cl'/'Br'/'I' and 'length_pm'/'strength_kj_mol'/'strength_kcal_mol'/'dipole_D'
- **H type classification:** `classify_hydrogen_type(carbon_substitution)` -> 'primary'/'secondary'/'tertiary'/'allylic'/'vinylic'
- **Halogenation product distribution:** `calculate_halogenation_products(hydrogen_pools, halogen)` -> pass list of HydrogenPool(h_type, count, position) objects; halogen='Cl' or 'Br'
- **Pre-built chlorination:** `predict_chlorination_products(molecule_name)` -> for common molecules like 'butane', 'propane', '2-methylpropane'
- **Allylic positions:** `identify_allylic_positions(alkene_structure)` -> list of allylic carbon positions
- **NBS product:** `predict_nbs_product(alkene_name)` -> major allylic bromination product
- **Grignard formation:** `grignard_formation(alkyl_halide, solvent)` -> reaction details (fluorides don't form Grignards)
- **Grignard acid-base:** `grignard_acid_base_reaction(grignard, acid, acid_pka)` -> reaction occurs if acid_pKa < 44-60
- **Gilman coupling:** `gilman_coupling(gilman_reagent, alkyl_halide)` -> C-C coupling (no F)
- **Suzuki coupling:** `suzuki_coupling(boronic_acid, aryl_halide)` -> biaryl synthesis
- **Oxidation level:** `calculate_oxidation_level(c_h_bonds, c_o_bonds, c_n_bonds, c_x_bonds)` -> integer
- **Redox classification:** `classify_redox_reaction(reactant_level, product_level)` -> 'Oxidation'/'Reduction'
- **Rank oxidation levels:** `compare_oxidation_levels(compounds)` -> sorted list
- **Alcohol to halide reagent:** `select_alcohol_to_halide_reagent(alcohol_type, target_halide)` -> reagent recommendation

### Step 3: Handle special cases
- Bromination is MUCH more selective than chlorination (Br: 1deg:1, 2deg:80, 3deg:1600)
- Grignard reagents are destroyed by any acid with pKa < 44-60 (water, alcohols, carboxylic acids)
- Gilman coupling (Lithium diorganocuprates) does NOT work with fluorides or sp3-hybridized substrates well
- Fluorides require special reagents (DAST, HF/pyridine) - never use HX

### Examples
```python
# Example 1: Chlorination of propane product distribution
pools = [HydrogenPool('primary', 6, 'C1'), HydrogenPool('secondary', 2, 'C2')]
calculate_halogenation_products(pools, 'Cl')  -> {'C1': 30.0, 'C2': 70.0}

# Example 2: Will CH3MgBr react with water (pKa 15.7)?
grignard_acid_base_reaction('CH3MgBr', 'H2O', 15.7)  -> occurs=True (15.7 < 44)

# Example 3: Convert tertiary alcohol to chloride
select_alcohol_to_halide_reagent('tertiary', 'Cl')  -> HCl in cold ether

# Example 4: C-Br bond strength
get_cx_bond_property('Br', 'strength_kj_mol')  -> 294
```
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


# ============================================================================
# DATA TABLES
# ============================================================================

# C-X Bond Properties (from Table 10.1)
CX_BOND_DATA = {
    'F': {'length_pm': 139, 'strength_kj_mol': 460, 'strength_kcal_mol': 110, 'dipole_D': 1.85},
    'Cl': {'length_pm': 178, 'strength_kj_mol': 350, 'strength_kcal_mol': 84, 'dipole_D': 1.87},
    'Br': {'length_pm': 193, 'strength_kj_mol': 294, 'strength_kcal_mol': 70, 'dipole_D': 1.81},
    'I': {'length_pm': 214, 'strength_kj_mol': 239, 'strength_kcal_mol': 57, 'dipole_D': 1.62},
}

# H Abstraction Reactivity (Chlorination)
H_REACTIVITY = {
    'primary': 1.0,
    'secondary': 3.5,
    'tertiary': 5.0,
}

# C-H Bond Energies (kJ/mol)
CH_BOND_ENERGIES = {
    'primary': 421,
    'secondary': 410,
    'tertiary': 400,
    'allylic': 370,
    'vinylic': 465,
    'benzylic': 375,
}

# Radical Stability Order (lower C-H energy = more stable radical)
RADICAL_STABILITY_ORDER = ['allylic', 'tertiary', 'secondary', 'primary', 'vinylic']


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_cx_bond_property(halogen: str, property_name: str) -> float:
    """Get C-X bond property for given halogen.
    
    Args:
        halogen: 'F', 'Cl', 'Br', or 'I'
        property_name: 'length_pm', 'strength_kj_mol', 'strength_kcal_mol', or 'dipole_D'
    
    Returns:
        Property value
        
    Raises:
        ValueError: If halogen or property not found
    """
    halogen = halogen.capitalize()
    if halogen not in CX_BOND_DATA:
        raise ValueError(f"Unknown halogen: {halogen}. Use F, Cl, Br, or I.")
    if property_name not in CX_BOND_DATA[halogen]:
        raise ValueError(f"Unknown property: {property_name}")
    return CX_BOND_DATA[halogen][property_name]


def classify_hydrogen_type(carbon_substitution: str) -> str:
    """Classify hydrogen type based on carbon substitution.
    
    Args:
        carbon_substitution: 'primary', 'secondary', 'tertiary', 'allylic', or 'vinylic'
    
    Returns:
        Hydrogen type classification
    """
    valid_types = ['primary', 'secondary', 'tertiary', 'allylic', 'vinylic', 'benzylic']
    carbon_substitution = carbon_substitution.lower()
    if carbon_substitution not in valid_types:
        raise ValueError(f"Invalid substitution type: {carbon_substitution}")
    return carbon_substitution


# ============================================================================
# RADICAL HALOGENATION PRODUCT PREDICTION
# ============================================================================

@dataclass
class HydrogenPool:
    """Represents a pool of equivalent hydrogens in a molecule."""
    h_type: str  # 'primary', 'secondary', 'tertiary'
    count: int   # Number of equivalent hydrogens
    position: str  # Position description (e.g., "C1", "C2")


def calculate_halogenation_products(
    hydrogen_pools: List[HydrogenPool],
    halogen: str = 'Cl'
) -> Dict[str, float]:
    """Calculate product distribution for radical halogenation.
    
    Args:
        hydrogen_pools: List of HydrogenPool objects representing equivalent H atoms
        halogen: 'Cl' or 'Br' (different selectivity)
    
    Returns:
        Dictionary mapping product position to percentage
    
    Example:
        >>> pools = [
        ...     HydrogenPool('primary', 6, 'C1'),
        ...     HydrogenPool('secondary', 4, 'C2')
        ... ]
        >>> calculate_halogenation_products(pools, 'Cl')
        {'C1': 30.0, 'C2': 70.0}
    """
    # Use chlorination reactivity values
    reactivity = H_REACTIVITY.copy()
    
    # Bromination is more selective (larger differences)
    if halogen.lower() == 'br':
        reactivity = {
            'primary': 1.0,
            'secondary': 80.0,  # Much more selective
            'tertiary': 1600.0,  # Very selective for 3deg
        }
    
    # Calculate contribution for each pool
    contributions = []
    total_contribution = 0.0
    
    for pool in hydrogen_pools:
        rel_reactivity = reactivity.get(pool.h_type, 1.0)
        contribution = pool.count * rel_reactivity
        contributions.append((pool.position, contribution))
        total_contribution += contribution
    
    # Calculate percentages
    results = {}
    for position, contribution in contributions:
        percentage = (contribution / total_contribution) * 100
        results[position] = round(percentage, 1)
    
    return results


def predict_chlorination_products(molecule_name: str) -> Dict[str, float]:
    """Predict monochlorination products for common molecules.
    
    Args:
        molecule_name: Name of molecule (e.g., 'butane', '2-methylpropane')
    
    Returns:
        Dictionary mapping product names to percentages
    """
    # Pre-defined common molecules
    common_molecules = {
        'methane': [HydrogenPool('primary', 4, 'C1')],
        'ethane': [HydrogenPool('primary', 6, 'C1')],
        'propane': [
            HydrogenPool('primary', 6, 'C1'),
            HydrogenPool('secondary', 2, 'C2')
        ],
        'butane': [
            HydrogenPool('primary', 6, 'C1'),
            HydrogenPool('secondary', 4, 'C2')
        ],
        '2-methylpropane': [
            HydrogenPool('primary', 9, 'C1'),
            HydrogenPool('tertiary', 1, 'C2')
        ],
        'pentane': [
            HydrogenPool('primary', 6, 'C1'),
            HydrogenPool('secondary', 4, 'C2'),
            HydrogenPool('secondary', 2, 'C3')
        ],
        '2-methylbutane': [
            HydrogenPool('primary', 6, 'C1'),
            HydrogenPool('secondary', 2, 'C2'),
            HydrogenPool('tertiary', 1, 'C3'),
            HydrogenPool('primary', 3, 'C4')
        ],
    }
    
    molecule_name = molecule_name.lower()
    if molecule_name not in common_molecules:
        raise ValueError(f"Molecule '{molecule_name}' not in database. "
                        f"Available: {list(common_molecules.keys())}")
    
    return calculate_halogenation_products(common_molecules[molecule_name], 'Cl')


# ============================================================================
# ALLYLIC BROMINATION
# ============================================================================

def identify_allylic_positions(alkene_structure: str) -> List[str]:
    """Identify allylic positions in an alkene.
    
    Args:
        alkene_structure: SMILES-like notation or description
    
    Returns:
        List of allylic position descriptions
    """
    # This is a simplified implementation
    # Full implementation would parse the structure
    allylic_positions = []
    
    # Common patterns
    if 'cyclohexene' in alkene_structure.lower():
        allylic_positions = ['C3', 'C6']  # Both are equivalent
    elif 'propene' in alkene_structure.lower():
        allylic_positions = ['C3']  # Methyl group
    elif '1-butene' in alkene_structure.lower():
        allylic_positions = ['C3']
    elif '2-butene' in alkene_structure.lower():
        allylic_positions = ['C1', 'C4']  # Both methyls are allylic
    
    return allylic_positions


def predict_nbs_product(alkene_name: str) -> str:
    """Predict the major NBS bromination product.
    
    Args:
        alkene_name: Name of the alkene
    
    Returns:
        Product name
    """
    # Simplified mapping for common alkenes
    nbs_products = {
        'cyclohexene': '3-bromocyclohexene',
        'propene': '3-bromo-1-propene (allyl bromide)',
        '1-butene': '3-bromo-1-butene',
        '2-butene': '1-bromo-2-butene',
        'toluene': 'benzyl bromide',
    }
    
    alkene_name = alkene_name.lower()
    for key, product in nbs_products.items():
        if key in alkene_name:
            return product
    
    return f"Allylic bromide of {alkene_name}"


# ============================================================================
# GRIGNARD REAGENTS
# ============================================================================

def grignard_formation(alkyl_halide: str, solvent: str = 'ether') -> Dict[str, str]:
    """Describe Grignard reagent formation.
    
    Args:
        alkyl_halide: Alkyl halide formula or name
        solvent: 'ether' or 'THF'
    
    Returns:
        Dictionary with reaction details
    """
    # Extract halogen
    halogen = None
    for h in ['I', 'Br', 'Cl', 'F']:
        if h in alkyl_halide:
            halogen = h
            break
    
    if halogen == 'F':
        return {
            'reaction': f'{alkyl_halide} + Mg -> No reaction',
            'notes': 'Fluorides do not form Grignard reagents',
            'success': False
        }
    
    if halogen == 'Cl':
        notes = 'Chlorides are less reactive; may require THF or higher temperature'
    else:
        notes = f'{halogen} is reactive; reaction proceeds readily'
    
    return {
        'reaction': f'{alkyl_halide} + Mg -> R-Mg-{halogen} (in {solvent})',
        'solvent': solvent,
        'notes': notes,
        'success': True
    }


def grignard_acid_base_reaction(grignard: str, acid: str, acid_pka: float) -> Dict[str, str]:
    """Predict Grignard acid-base reaction.
    
    Args:
        grignard: Grignard reagent formula
        acid: Acid formula
        acid_pka: pKa of the acid
    
    Returns:
        Reaction prediction
    """
    # Grignard conjugate acid pKa is 44-60
    grignard_pka_range = (44, 60)
    
    if acid_pka < grignard_pka_range[0]:
        # Reaction will occur
        return {
            'reaction': f'{grignard} + {acid} -> R-H + Mg-X-{acid.replace("H", "")}',
            'occurs': True,
            'reason': f'Acid pKa ({acid_pka}) < Grignard conjugate acid pKa (44-60)'
        }
    else:
        return {
            'reaction': f'{grignard} + {acid} -> No reaction',
            'occurs': False,
            'reason': f'Acid pKa ({acid_pka}) >= Grignard conjugate acid pKa (44-60)'
        }


# ============================================================================
# ORGANOMETALLIC COUPLING
# ============================================================================

def gilman_coupling(gilman_reagent: str, alkyl_halide: str) -> Dict[str, str]:
    """Predict Gilman coupling reaction.
    
    Args:
        gilman_reagent: Gilman reagent formula (e.g., '(CH3)2CuLi')
        alkyl_halide: Alkyl halide formula
    
    Returns:
        Coupling reaction prediction
    """
    # Check for fluoride
    if 'F' in alkyl_halide and ('Cl' not in alkyl_halide and 
                                'Br' not in alkyl_halide and 
                                'I' not in alkyl_halide):
        return {
            'reaction': 'No reaction',
            'notes': 'Gilman coupling does not work with alkyl fluorides',
            'success': False
        }
    
    return {
        'reaction': f'{gilman_reagent} + {alkyl_halide} -> R-R\' + R-Cu + LiX',
        'notes': 'Forms new C-C bond; works with Cl, Br, I',
        'success': True
    }


def suzuki_coupling(boronic_acid: str, aryl_halide: str) -> Dict[str, str]:
    """Predict Suzuki-Miyaura coupling reaction.
    
    Args:
        boronic_acid: Aryl boronic acid formula
        aryl_halide: Aryl halide formula
    
    Returns:
        Coupling reaction prediction
    """
    return {
        'reaction': f'{boronic_acid} + {aryl_halide} + Pd cat. + base -> biaryl',
        'catalyst': 'Pd(0) catalyst',
        'base_needed': 'Required (e.g., K2CO3, Na2CO3)',
        'notes': 'Preferred for biaryl synthesis; catalytic Pd; works with aryl/vinylic halides',
        'limitations': 'Does not work with alkyl halides',
        'success': True
    }


# ============================================================================
# OXIDATION LEVEL CALCULATIONS
# ============================================================================

def calculate_oxidation_level(c_h_bonds: int, c_o_bonds: int = 0, 
                             c_n_bonds: int = 0, c_x_bonds: int = 0) -> int:
    """Calculate oxidation level for a carbon atom or molecule.
    
    Args:
        c_h_bonds: Number of C-H bonds
        c_o_bonds: Number of C-O bonds
        c_n_bonds: Number of C-N bonds
        c_x_bonds: Number of C-X bonds (X = halogen)
    
    Returns:
        Oxidation level (higher = more oxidized)
    """
    return (c_o_bonds + c_n_bonds + c_x_bonds) - c_h_bonds


def classify_redox_reaction(
    reactant_level: int, 
    product_level: int
) -> str:
    """Classify reaction as oxidation, reduction, or neither.
    
    Args:
        reactant_level: Oxidation level of reactant
        product_level: Oxidation level of product
    
    Returns:
        Classification string
    """
    if product_level > reactant_level:
        return 'Oxidation'
    elif product_level < reactant_level:
        return 'Reduction'
    else:
        return 'Neither oxidation nor reduction'


def compare_oxidation_levels(compounds: Dict[str, Tuple]) -> List[str]:
    """Rank compounds by oxidation level.
    
    Args:
        compounds: Dictionary mapping compound names to (C-H, C-O, C-N, C-X) tuples
    
    Returns:
        List of compound names in order of increasing oxidation level
    """
    levels = {}
    for name, bonds in compounds.items():
        c_h, c_o, c_n, c_x = bonds
        levels[name] = calculate_oxidation_level(c_h, c_o, c_n, c_x)
    
    # Sort by oxidation level
    sorted_compounds = sorted(levels.items(), key=lambda x: x[1])
    return [name for name, level in sorted_compounds]


# ============================================================================
# REAGENT SELECTION
# ============================================================================

def select_alcohol_to_halide_reagent(alcohol_type: str, target_halide: str = 'Cl') -> Dict[str, str]:
    """Select appropriate reagent for alcohol to alkyl halide conversion.
    
    Args:
        alcohol_type: 'primary', 'secondary', or 'tertiary'
        target_halide: 'Cl', 'Br', 'I', or 'F'
    
    Returns:
        Reagent recommendation
    """
    alcohol_type = alcohol_type.lower()
    target_halide = target_halide.capitalize()
    
    if alcohol_type == 'tertiary':
        if target_halide in ['Cl', 'Br', 'I']:
            return {
                'reagent': f'H{target_halide}',
                'conditions': 'Cold ether, rapid reaction',
                'notes': 'Tertiary alcohols react rapidly with HX'
            }
        else:  # f
            return {
                'reagent': 'HF/pyridine or (Et2N)SF3',
                'conditions': 'Special reagents needed',
                'notes': 'Alkyl fluorides require special reagents'
            }
    
    else:  # Primary or Secondary
        if target_halide == 'Cl':
            return {
                'reagent': 'SOCl2',
                'conditions': 'Mild, high yield',
                'notes': 'Avoids acid-catalyzed rearrangements'
            }
        elif target_halide == 'Br':
            return {
                'reagent': 'PBr3',
                'conditions': 'Mild, high yield',
                'notes': 'Preferred for bromides'
            }
        elif target_halide == 'I':
            return {
                'reagent': 'HI or P/I2',
                'conditions': 'Various options',
                'notes': 'Iodides can be made from alcohols'
            }
        else:  # F
            return {
                'reagent': '(Et2N)SF3 (DAST) or HF/pyridine',
                'conditions': 'Special reagents',
                'notes': 'Fluorides require specialized reagents'
            }


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "calculate_halogenation_products",
        "description": "Calculate product distribution for radical halogenation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hydrogen_pools": {
                    "type": "number",
                    "description": "Hydrogen Pools"
                },
                "halogen": {
                    "type": "number",
                    "description": "Halogen",
                    "default": "Cl"
                }
            },
            "required": [
                "hydrogen_pools"
            ]
        }
    },
    {
        "name": "calculate_oxidation_level",
        "description": "Calculate oxidation level for a carbon atom or molecule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "c_h_bonds": {
                    "type": "number",
                    "description": "C H Bonds"
                },
                "c_o_bonds": {
                    "type": "number",
                    "description": "C O Bonds",
                    "default": 0
                },
                "c_n_bonds": {
                    "type": "number",
                    "description": "C N Bonds",
                    "default": 0
                },
                "c_x_bonds": {
                    "type": "number",
                    "description": "C X Bonds",
                    "default": 0
                }
            },
            "required": [
                "c_h_bonds"
            ]
        }
    },
    {
        "name": "classify_hydrogen_type",
        "description": "Classify hydrogen type based on carbon substitution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbon_substitution": {
                    "type": "number",
                    "description": "Carbon Substitution"
                }
            },
            "required": [
                "carbon_substitution"
            ]
        }
    },
    {
        "name": "classify_redox_reaction",
        "description": "Classify reaction as oxidation, reduction, or neither.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reactant_level": {
                    "type": "number",
                    "description": "Reactant Level"
                },
                "product_level": {
                    "type": "number",
                    "description": "Product Level"
                }
            },
            "required": [
                "reactant_level",
                "product_level"
            ]
        }
    },
    {
        "name": "compare_oxidation_levels",
        "description": "Rank compounds by oxidation level.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compounds": {
                    "type": "number",
                    "description": "Compounds"
                }
            },
            "required": [
                "compounds"
            ]
        }
    },
    {
        "name": "dataclass",
        "description": "Add dunder methods based on the fields defined in the class.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cls": {
                    "type": "number",
                    "description": "Cls",
                    "default": None
                },
                "init": {
                    "type": "number",
                    "description": "Init",
                    "default": True
                },
                "repr": {
                    "type": "number",
                    "description": "Repr",
                    "default": True
                },
                "eq": {
                    "type": "number",
                    "description": "Eq",
                    "default": True
                },
                "order": {
                    "type": "number",
                    "description": "Order",
                    "default": False
                },
                "unsafe_hash": {
                    "type": "number",
                    "description": "Unsafe Hash",
                    "default": False
                },
                "frozen": {
                    "type": "number",
                    "description": "Frozen",
                    "default": False
                },
                "match_args": {
                    "type": "number",
                    "description": "Match Args",
                    "default": True
                },
                "kw_only": {
                    "type": "number",
                    "description": "Kw Only",
                    "default": False
                },
                "slots": {
                    "type": "number",
                    "description": "Slots",
                    "default": False
                },
                "weakref_slot": {
                    "type": "number",
                    "description": "Weakref Slot",
                    "default": False
                }
            },
            "required": []
        }
    },
    {
        "name": "get_cx_bond_property",
        "description": "Get C-X bond property for given halogen.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "halogen": {
                    "type": "number",
                    "description": "Halogen"
                },
                "property_name": {
                    "type": "number",
                    "description": "Property Name"
                }
            },
            "required": [
                "halogen",
                "property_name"
            ]
        }
    },
    {
        "name": "gilman_coupling",
        "description": "Predict Gilman coupling reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "gilman_reagent": {
                    "type": "number",
                    "description": "Gilman Reagent"
                },
                "alkyl_halide": {
                    "type": "number",
                    "description": "Alkyl Halide"
                }
            },
            "required": [
                "gilman_reagent",
                "alkyl_halide"
            ]
        }
    },
    {
        "name": "grignard_acid_base_reaction",
        "description": "Predict Grignard acid-base reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "grignard": {
                    "type": "number",
                    "description": "Grignard"
                },
                "acid": {
                    "type": "number",
                    "description": "Acid"
                },
                "acid_pka": {
                    "type": "number",
                    "description": "Acid Pka"
                }
            },
            "required": [
                "grignard",
                "acid",
                "acid_pka"
            ]
        }
    },
    {
        "name": "grignard_formation",
        "description": "Describe Grignard reagent formation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkyl_halide": {
                    "type": "number",
                    "description": "Alkyl Halide"
                },
                "solvent": {
                    "type": "number",
                    "description": "Solvent",
                    "default": "ether"
                }
            },
            "required": [
                "alkyl_halide"
            ]
        }
    },
    {
        "name": "identify_allylic_positions",
        "description": "Identify allylic positions in an alkene.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkene_structure": {
                    "type": "string",
                    "description": "Alkene Structure"
                }
            },
            "required": [
                "alkene_structure"
            ]
        }
    },
    {
        "name": "predict_chlorination_products",
        "description": "Predict monochlorination products for common molecules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "molecule_name": {
                    "type": "number",
                    "description": "Molecule Name"
                }
            },
            "required": [
                "molecule_name"
            ]
        }
    },
    {
        "name": "predict_nbs_product",
        "description": "Predict the major NBS bromination product.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alkene_name": {
                    "type": "number",
                    "description": "Alkene Name"
                }
            },
            "required": [
                "alkene_name"
            ]
        }
    },
    {
        "name": "select_alcohol_to_halide_reagent",
        "description": "Select appropriate reagent for alcohol to alkyl halide conversion.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alcohol_type": {
                    "type": "number",
                    "description": "Alcohol Type"
                },
                "target_halide": {
                    "type": "number",
                    "description": "Target Halide",
                    "default": "Cl"
                }
            },
            "required": [
                "alcohol_type"
            ]
        }
    },
    {
        "name": "suzuki_coupling",
        "description": "Predict Suzuki-Miyaura coupling reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "boronic_acid": {
                    "type": "number",
                    "description": "Boronic Acid"
                },
                "aryl_halide": {
                    "type": "number",
                    "description": "Aryl Halide"
                }
            },
            "required": [
                "boronic_acid",
                "aryl_halide"
            ]
        }
    }
]