"""
L3 Tool: Amine Chemistry Tools
Predict amine basicity, synthesis routes, and reactions.

Source: Organic Chemistry (OpenStax) Ch24
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter amine basicity, classification, Sandmeyer, reductive amination, or Hofmann rearrangement problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given an amine name -> predict basicity (pKa) or classify as 1deg/2deg/3deg/4deg?
- Given a diazonium salt + reagent -> predict Sandmeyer product?
- Given a carbonyl + amine -> predict reductive amination product?
- Given an amide -> predict Hofmann rearrangement product?

### Step 2: Choose the correct function
- **Amine basicity:** `amine_basicity(amine)` -> returns pKa and classification ('strong_base' pKa≥10, 'moderate_base' pKa≥4, 'weak_base' pKa≥0, 'very_weak_base' pKa<0)
- **Amine classification:** `amine_classification(amine)` -> 'primary'/'secondary'/'tertiary'/'quaternary' with RnNH description
- **Reductive amination:** `reductive_amination_product(carbonyl, amine)` -> product type, mechanism, reagents (NaBH4, NaBH(OAc)3, H2/Ni)
- **Sandmeyer reaction:** `sandmeyer_product(diazonium, reagent)` -> product with substituent. Reagents: CuCl->Cl, CuBr->Br, CuCN->CN, H2O->OH, H3PO2->H, KI->I
- **Hofmann rearrangement:** `hofmann_rearrangement(amide)` -> amine product (loses one carbon: RCONH2 -> RNH2)

### Step 3: Handle special cases
- Arylamines (aniline) are much less basic (pKa ~4.6) due to resonance delocalization
- Pyrrole is nearly non-basic (pKa ~-0.3) because lone pair is in aromatic system
- Hofmann rearrangement converts amide to amine with ONE LESS carbon
- Reductive amination with ammonia -> primary amine; primary amine -> secondary; secondary -> tertiary

### Examples
```python
# Example 1: Basicity comparison
amine_basicity('methylamine')   -> {'pka': 10.6, 'classification': 'strong_base'}
amine_basicity('aniline')       -> {'pka': 4.6, 'classification': 'moderate_base'}

# Example 2: Sandmeyer reaction
sandmeyer_product('benzenediazonium', 'CuCl')  -> {'product': 'chlorobenzene', 'substituent': 'Cl'}

# Example 3: Reductive amination
reductive_amination_product('acetone', 'methylamine')  -> {'product_type': 'secondary_amine'}

# Example 4: Hofmann rearrangement
hofmann_rearrangement('propanamide')  -> {'product': 'ethylamine', 'carbons_lost': 1}
```
"""

# Amine basicity data (pKa of conjugate acid)
AMINE_BASICITY = {
    'ammonia': 9.3,
    'methylamine': 10.6,
    'dimethylamine': 10.7,
    'trimethylamine': 9.8,
    'ethylamine': 10.7,
    'diethylamine': 11.0,
    'triethylamine': 10.8,
    'propylamine': 10.7,
    'isopropylamine': 10.6,
    'butylamine': 10.8,
    'aniline': 4.6,
    'phenylamine': 4.6,  # Same as aniline
    'pyridine': 5.2,
    'pyrrole': -0.3,
    'imidazole': 7.0,
    'p-methylaniline': 5.1,
    'p-nitroaniline': 1.0,
    'n,n-dimethylaniline': 5.1,
}

# Sandmeyer reaction reagents and products
SANDMEYER_REACTIONS = {
    'cucl': 'Cl',
    'copper(i)_chloride': 'Cl',
    'cubr': 'Br',
    'copper(i)_bromide': 'Br',
    'cucn': 'CN',
    'copper(i)_cyanide': 'CN',
    'h2o': 'OH',
    'water': 'OH',
    'h3po2': 'H',
    'hypophosphorous_acid': 'H',
    'ki': 'I',
    'potassium_iodide': 'I',
}

# Common carbonyl compounds for reductive amination
CARBONYL_COMPUNDS = {
    'formaldehyde': 'CH2O',
    'acetaldehyde': 'CH3CHO',
    'acetone': '(CH3)2CO',
    'butanone': 'CH3CH2COCH3',
    'benzaldehyde': 'C6H5CHO',
    'propionaldehyde': 'CH3CH2CHO',
}


def amine_basicity(amine: str) -> dict:
    """
    Predict amine basicity (pKa of conjugate acid).
    
    Args:
        amine: Amine name
    
    Returns:
        Dictionary with pKa and basicity classification
    
    Example:
        >>> amine_basicity('methylamine')
        {'pka': 10.6, 'classification': 'strong_base'}
    """
    amine_lower = amine.lower().replace('-', '').replace('_', '').replace(' ', '')
    
    # Look up in database - exact match first
    pka = None
    for name, value in AMINE_BASICITY.items():
        name_norm = name.lower().replace('-', '').replace('_', '')
        if name_norm == amine_lower:
            pka = value
            break
    
    # If no exact match, try substring
    if pka is None:
        for name, value in AMINE_BASICITY.items():
            name_norm = name.lower().replace('-', '').replace('_', '')
            if name_norm in amine_lower or amine_lower in name_norm:
                pka = value
                break
    
    # Estimate if not found
    if pka is None:
        if 'aniline' in amine_lower or 'phenyl' in amine_lower:
            pka = 4.5  # Arylamine estimate
        elif 'pyrid' in amine_lower:
            pka = 5.2
        elif 'pyrrole' in amine_lower:
            pka = -0.3
        else:
            pka = 10.5  # Aliphatic amine estimate
    
    # Classify
    if pka >= 10:
        classification = 'strong_base'
    elif pka >= 4:
        classification = 'moderate_base'
    elif pka >= 0:
        classification = 'weak_base'
    else:
        classification = 'very_weak_base'
    
    return {
        'amine': amine,
        'pka': pka,
        'classification': classification
    }


def amine_classification(amine: str) -> dict:
    """
    Classify amine as primary, secondary, tertiary, or quaternary.
    
    Args:
        amine: Amine name or SMILES
    
    Returns:
        Dictionary with classification
    
    Example:
        >>> amine_classification('dimethylamine')
        {'classification': 'secondary', 'description': 'R2NH'}
    """
    amine_lower = amine.lower()
    
    # Check for quaternary
    if 'quaternary' in amine_lower or 'ammonium' in amine_lower:
        return {
            'classification': 'quaternary',
            'description': 'R4N+',
            'charge': 1
        }
    
    # Check for prefixes
    if amine_lower.startswith('di') and 'amine' in amine_lower:
        if amine_lower.startswith('tri'):
            return {
                'classification': 'tertiary',
                'description': 'R3N',
                'charge': 0
            }
        return {
            'classification': 'secondary',
            'description': 'R2NH',
            'charge': 0
        }
    
    if amine_lower.startswith('tri') and 'amine' in amine_lower:
        return {
            'classification': 'tertiary',
            'description': 'R3N',
            'charge': 0
        }
    
    # Default to primary
    return {
        'classification': 'primary',
        'description': 'RNH2',
        'charge': 0
    }


def reductive_amination_product(carbonyl: str, amine: str) -> dict:
    """
    Predict reductive amination product.
    
    Args:
        carbonyl: Aldehyde or ketone name
        amine: Primary or secondary amine (or ammonia)
    
    Returns:
        Dictionary with product information
    
    Example:
        >>> reductive_amination_product('acetone', 'methylamine')
        {'product_type': 'secondary_amine', 'mechanism': 'imine_formation_then_reduction'}
    """
    carbonyl_lower = carbonyl.lower().replace('-', '').replace('_', '')
    amine_lower = amine.lower().replace('-', '').replace('_', '')
    
    # Determine carbonyl type
    is_aldehyde = 'aldehyde' in carbonyl_lower or carbonyl_lower in ['formaldehyde', 'acetaldehyde', 'propionaldehyde', 'benzaldehyde']
    is_ketone = 'ketone' in carbonyl_lower or carbonyl_lower in ['acetone', 'butanone']
    
    # Determine amine type
    if amine_lower in ['ammonia', 'nh3']:
        amine_type = 'ammonia'
        product_type = 'primary_amine'
    elif 'methylamine' in amine_lower and amine_lower not in ['dimethylamine', 'trimethylamine']:
        amine_type = 'primary'
        product_type = 'secondary_amine'
    elif 'dimethylamine' in amine_lower or amine_lower.startswith('di'):
        amine_type = 'secondary'
        product_type = 'tertiary_amine'
    else:
        amine_type = 'primary'
        product_type = 'secondary_amine'
    
    return {
        'carbonyl': carbonyl,
        'amine': amine,
        'carbonyl_type': 'aldehyde' if is_aldehyde else 'ketone',
        'amine_type': amine_type,
        'product_type': product_type,
        'mechanism': 'imine_formation_then_reduction',
        'reagents': ['NaBH4', 'NaBH(OAc)3', 'H2/Ni']
    }


def sandmeyer_product(diazonium: str, reagent: str) -> dict:
    """
    Predict Sandmeyer reaction product.
    
    Args:
        diazonium: Aryldiazonium salt name
        reagent: CuCl, CuBr, CuCN, H2O, H3PO2, KI
    
    Returns:
        Dictionary with product
    
    Example:
        >>> sandmeyer_product('benzenediazonium', 'CuCl')
        {'product': 'chlorobenzene', 'substituent': 'Cl'}
    """
    reagent_lower = reagent.lower().replace('-', '').replace('_', '').replace(' ', '')
    
    # Find the substituent
    substituent = None
    for name, sub in SANDMEYER_REACTIONS.items():
        if name == reagent_lower or name in reagent_lower or reagent_lower in name:
            substituent = sub
            break
    
    if substituent is None:
        substituent = 'Unknown'
    
    # Build product name (simplified)
    if 'benzene' in diazonium.lower():
        if substituent == 'H':
            product = 'benzene'
        elif substituent == 'OH':
            product = 'phenol'
        elif substituent == 'CN':
            product = 'benzonitrile'
        else:
            product = f'{substituent.lower()}benzene'
    else:
        product = f'Aryl-{substituent}'
    
    return {
        'diazonium': diazonium,
        'reagent': reagent,
        'substituent': substituent,
        'product': product,
        'reaction_type': 'Sandmeyer'
    }


def hofmann_rearrangement(amide: str) -> dict:
    """
    Predict Hofmann rearrangement product.
    
    Args:
        amide: Primary amide name
    
    Returns:
        Dictionary with amine product (one carbon lost)
    
    Example:
        >>> hofmann_rearrangement('propanamide')
        {'product': 'ethylamine', 'carbons_lost': 1}
    """
    amide_lower = amide.lower().replace('-', '').replace('_', '')
    
    # Simple mapping
    amide_to_amine = {
        'acetamide': 'methylamine',
        'ethanamide': 'methylamine',
        'propanamide': 'ethylamine',
        'propionamide': 'ethylamine',
        'butanamide': 'propylamine',
        'benzamide': 'aniline',
        'pentanamide': 'butylamine',
    }
    
    product = None
    for name, amine in amide_to_amine.items():
        if name in amide_lower or amide_lower in name:
            product = amine
            break
    
    if product is None:
        product = 'amine (structure-dependent)'
    
    return {
        'amide': amide,
        'product': product,
        'carbons_lost': 1,
        'reagents': ['Br2', 'NaOH'],
        'mechanism': 'migration_of_alkyl_group'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "24-01",
        "question": "Basicity of methylamine",
        "amine": "methylamine",
        "expected_pka": 10.6
    },
    {
        "id": "24-02",
        "question": "Sandmeyer with CuCl",
        "reagent": "CuCl",
        "expected_substituent": "Cl"
    },
    {
        "id": "24-03",
        "question": "Reductive amination of acetone with methylamine",
        "carbonyl": "acetone",
        "amine": "methylamine",
        "expected_product": "secondary_amine"
    },
    {
        "id": "24-04",
        "question": "Hofmann rearrangement of propanamide",
        "amide": "propanamide",
        "expected_product": "ethylamine"
    },
]


if __name__ == "__main__":
    # Quick tests
    print("Amine Chemistry Tools")
    print("=" * 40)
    
    # Test basicity
    print("\nBasicity:")
    for amine in ['ammonia', 'methylamine', 'aniline']:
        result = amine_basicity(amine)
        print(f"  {amine}: pKa = {result['pka']}")
    
    # Test Sandmeyer
    print("\nSandmeyer products:")
    for reagent in ['CuCl', 'CuBr', 'H2O', 'KI']:
        result = sandmeyer_product('benzenediazonium', reagent)
        print(f"  {reagent}: {result['product']}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "amine_basicity",
        "description": "Predict amine basicity (pKa of conjugate acid).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "amine": {
                    "type": "number",
                    "description": "Amine"
                }
            },
            "required": [
                "amine"
            ]
        }
    },
    {
        "name": "amine_classification",
        "description": "Classify amine as primary, secondary, tertiary, or quaternary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "amine": {
                    "type": "number",
                    "description": "Amine"
                }
            },
            "required": [
                "amine"
            ]
        }
    },
    {
        "name": "hofmann_rearrangement",
        "description": "Predict Hofmann rearrangement product.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "amide": {
                    "type": "number",
                    "description": "Amide"
                }
            },
            "required": [
                "amide"
            ]
        }
    },
    {
        "name": "reductive_amination_product",
        "description": "Predict reductive amination product.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "carbonyl": {
                    "type": "number",
                    "description": "Carbonyl"
                },
                "amine": {
                    "type": "number",
                    "description": "Amine"
                }
            },
            "required": [
                "carbonyl",
                "amine"
            ]
        }
    },
    {
        "name": "sandmeyer_product",
        "description": "Predict Sandmeyer reaction product.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "diazonium": {
                    "type": "number",
                    "description": "Diazonium"
                },
                "reagent": {
                    "type": "number",
                    "description": "Reagent"
                }
            },
            "required": [
                "diazonium",
                "reagent"
            ]
        }
    }
]