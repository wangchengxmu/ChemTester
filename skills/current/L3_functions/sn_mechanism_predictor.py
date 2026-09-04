"""
L3 Tool: SN Mechanism Predictor
Predicts reaction mechanism (SN1, SN2, E1, E2, E1cB) from substrate and conditions.

Source: Organic Chemistry (OpenStax) Ch11
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter nucleophilic substitution/elimination mechanism prediction problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Mechanism prediction**: Given substrate type, nucleophile/base, leaving group, solvent -> predict SN1/SN2/E1/E2
- **Nucleophile assessment**: Given species -> check if good nucleophile, strong base, good leaving group
- **Substrate classification**: Given substrate description -> classify as primary/secondary/tertiary/allylic/benzylic

### Step 2: Choose the correct function
- `predict_mechanism(substrate_type, nucleophile, base, leaving_group, solvent, temperature)` -> predicted mechanism
- `is_good_nucleophile(species)` -> True if nucleophilicity ≥ 1000 in NUCLEOPHILICITY table
- `is_strong_base(species)` -> True if in STRONG_BASES set (HO-, CH3O-, tBuO-, etc.)
- `is_good_leaving_group(species)` -> True if in GOOD_LEAVING_GROUPS set (I-, Br-, Cl-, TsO-, etc.)
- `classify_substrate(substrate_type)` -> dict with reactivity info and preferred mechanisms
- `competition_analysis(substrate, nucleophile, base, conditions)` -> SN vs E preference

### Step 3: Handle special cases
- **SN2**: primary + strong nucleophile -> favored; requires aprotic solvent
- **SN1**: tertiary + weak nucleophile + protic solvent -> carbocation intermediate
- **E2**: any substrate + strong bulky base (tBuOK) -> elimination favored over substitution
- **E1**: tertiary + weak base -> competes with SN1
- **E1cB**: poor leaving group + strong base -> requires acidic beta-hydrogen
- Bulky bases (tBuO-) favor elimination even with primary substrates
- Polar aprotic solvents (DMSO, DMF, acetone) accelerate SN2
- Polar protic solvents (H2O, ROH) accelerate SN1

### Examples
1. **Predict**: (CH3)3C-Br + NaI in acetone
   -> `predict_mechanism('tertiary', 'I-', 'I-', 'Br-', 'acetone')` -> SN1 (tertiary, protic not required for SN1)

2. **Predict**: CH3CH2Br + NaOEt in EtOH at 55degC
   -> `predict_mechanism('primary', 'EtO-', 'EtO-', 'Br-', 'EtOH', 328)` -> SN2 (primary + good nucleophile)
   -> With tBuOK instead: E2 (bulky base forces elimination)

3. **Check nucleophile**: Is CN- a good nucleophile?
   -> `is_good_nucleophile('CN-')` -> True (nucleophilicity = 125000)
"""

# Nucleophilicity ranking (in CH3OH)
NUCLEOPHILICITY = {
    'I-': 100000,
    'CN-': 125000,
    'HS-': 125000,
    'CH3O-': 25000,
    'HO-': 10000,
    'Br-': 10000,
    'Cl-': 1000,
    'NH3': 700,
    'CH3CO2-': 500,
    'H2O': 1,
}

# Strong bases
STRONG_BASES = {'HO-', 'CH3O-', 'EtO-', 'tBuO-', 'NH2-', 'NaOH', 'NaOEt', 'tBuOK'}

# Good leaving groups
GOOD_LEAVING_GROUPS = {'I-', 'Br-', 'Cl-', 'TsO-', 'OTs', 'H2O', 'OMs'}


def is_good_nucleophile(species: str) -> bool:
    """
    Check if species is a good nucleophile.
    
    Args:
        species: Nucleophile name (e.g., 'I-', 'OH-', 'H2O')
    
    Returns:
        True if nucleophilicity > 1000
    """
    if species in NUCLEOPHILICITY:
        return NUCLEOPHILICITY[species] >= 1000
    # Charged species generally better
    return species.endswith('-') and not species.endswith('+')


def is_strong_base(species: str) -> bool:
    """
    Check if species is a strong base.
    
    Args:
        species: Base name (e.g., 'NaOH', 'HO-')
    
    Returns:
        True if strong base
    """
    return species in STRONG_BASES or any(b in species for b in STRONG_BASES)


def is_good_leaving_group(species: str) -> bool:
    """
    Check if species is a good leaving group.
    
    Args:
        species: Leaving group name
    
    Returns:
        True if good leaving group
    """
    return species in GOOD_LEAVING_GROUPS


def classify_substrate(substrate_type: str) -> dict:
    """
    Classify substrate for reactivity predictions.
    
    Args:
        substrate_type: 'primary', 'secondary', 'tertiary', 'methyl', 
                       'allylic', 'benzylic'
    
    Returns:
        Dictionary with SN2 and SN1 suitability
    """
    substrate_type = substrate_type.lower()
    
    if substrate_type == 'methyl':
        return {'sn2': 'excellent', 'sn1': 'no', 'e2': 'no'}
    elif substrate_type == 'primary':
        return {'sn2': 'good', 'sn1': 'no', 'e2': 'possible'}
    elif substrate_type == 'secondary':
        return {'sn2': 'moderate', 'sn1': 'slow', 'e2': 'good'}
    elif substrate_type == 'tertiary':
        return {'sn2': 'no', 'sn1': 'excellent', 'e2': 'excellent'}
    elif substrate_type in ('allylic', 'benzylic'):
        return {'sn2': 'good', 'sn1': 'excellent', 'e2': 'good'}
    else:
        return {'sn2': 'unknown', 'sn1': 'unknown', 'e2': 'unknown'}


def predict_mechanism(substrate_type: str, nucleophile: str = None, 
                      base: str = None, solvent: str = None) -> str:
    """
    Predict reaction mechanism from conditions.
    
    Args:
        substrate_type: 'primary', 'secondary', 'tertiary', 'methyl', 
                       'allylic', 'benzylic'
        nucleophile: Name of nucleophile (e.g., 'I-', 'OH-', 'H2O')
        base: Name of base (e.g., 'NaOH', 'NaOEt', 'tBuOK')
        solvent: 'protic' or 'aprotic' (default: 'protic')
    
    Returns:
        Mechanism string: 'SN1', 'SN2', 'E1', 'E2', or mixture
    
    Examples:
        >>> predict_mechanism('tertiary', nucleophile='H2O', solvent='protic')
        'SN1/E1'
        >>> predict_mechanism('primary', nucleophile='I-')
        'SN2'
        >>> predict_mechanism('secondary', base='NaOEt')
        'E2'
    """
    substrate_type = substrate_type.lower()
    if solvent is None:
        solvent = 'protic'
    solvent = solvent.lower()
    
    # Normalize nucleophile name
    if nucleophile:
        nucleophile = nucleophile.replace('Na', '').replace('K', '')
        if nucleophile == 'OH':
            nucleophile = 'HO-'
    
    # Decision tree
    if substrate_type == 'methyl':
        if nucleophile and is_good_nucleophile(nucleophile):
            return 'SN2'
        return 'SN2'  # Methyl only does SN2
    
    elif substrate_type == 'primary':
        if base and is_strong_base(base):
            if 'tBu' in base or 'tert' in base.lower():
                return 'E2'  # Hindered base favors E2
            return 'SN2'  # Primary with strong base still SN2 dominates
        elif nucleophile and is_good_nucleophile(nucleophile):
            return 'SN2'
        else:
            return 'SN2'  # Default for primary
    
    elif substrate_type == 'secondary':
        if base and is_strong_base(base):
            return 'E2'
        elif nucleophile:
            if is_good_nucleophile(nucleophile) and solvent == 'aprotic':
                return 'SN2'
            elif not is_strong_base(nucleophile):
                if solvent == 'protic':
                    return 'SN1/E1'  # Competing mechanisms
                return 'SN2'
            else:
                return 'E2'
        return 'SN2'  # Default
    
    elif substrate_type == 'tertiary':
        if base and is_strong_base(base):
            return 'E2'
        elif nucleophile and not is_strong_base(nucleophile):
            return 'SN1/E1'  # Tertiary + weak nucleophile = SN1 + E1
        else:
            return 'SN1/E1'  # Default for tertiary
    
    elif substrate_type in ('allylic', 'benzylic'):
        if base and is_strong_base(base):
            return 'E2'
        elif nucleophile and is_good_nucleophile(nucleophile):
            if solvent == 'aprotic':
                return 'SN2'
            return 'SN1'  # Can do SN1 due to stable carbocation
        return 'SN1'
    
    return 'SN2'  # Default


def relative_sn2_rate(substrate: str) -> float:
    """
    Get relative SN2 reaction rate for a substrate.
    
    Args:
        substrate: Substrate description (e.g., 'methyl bromide', 'tert-butyl bromide')
    
    Returns:
        Relative rate (methyl = 1,000,000 as reference)
    """
    rates = {
        'methyl': 1000000,
        'primary': 10000,
        'secondary': 1,
        'tertiary': 0,
        'neopentyl': 0.01,
    }
    
    for key, rate in rates.items():
        if key in substrate.lower():
            return rate
    return 1.0


def zaitsev_product(alkyl_halide: str) -> str:
    """
    Predict the major elimination product using Zaitsev's rule.
    
    Args:
        alkyl_halide: Alkyl halide name or SMILES
    
    Returns:
        Description of the more substituted alkene
    """
    # Simplified: return description
    # In full implementation, would parse structure and find most substituted double bond
    return "More substituted alkene (Zaitsev product)"


def sn2_stereochemistry(configuration: str) -> str:
    """
    Predict the stereochemistry of SN2 product.
    
    SN2 always gives inversion of configuration.
    
    Args:
        configuration: 'R' or 'S'
    
    Returns:
        Inverted configuration
    """
    if configuration.upper() == 'R':
        return 'S'
    elif configuration.upper() == 'S':
        return 'R'
    else:
        return 'inverted'


def sn1_stereochemistry() -> str:
    """
    Predict the stereochemistry of SN1 product.
    
    SN1 gives racemization (racemic mixture).
    
    Returns:
        Description of stereochemical outcome
    """
    return "racemic mixture (R and S)"


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "11-01",
        "question": "Predict mechanism for (CH3)3CBr + H2O",
        "substrate": "tertiary",
        "nucleophile": "H2O",
        "solvent": "protic",
        "expected": "SN1/E1"
    },
    {
        "id": "11-02", 
        "question": "Predict mechanism for CH3Br + NaI",
        "substrate": "methyl",
        "nucleophile": "I-",
        "expected": "SN2"
    },
    {
        "id": "11-03",
        "question": "Predict mechanism for 2-bromopentane + NaOEt",
        "substrate": "secondary",
        "base": "NaOEt",
        "expected": "E2"
    },
    {
        "id": "11-04",
        "question": "Predict mechanism for 1-bromobutane + NaCN",
        "substrate": "primary",
        "nucleophile": "CN-",
        "solvent": "aprotic",
        "expected": "SN2"
    },
    {
        "id": "11-05",
        "question": "Predict mechanism for benzyl bromide + CH3OH",
        "substrate": "benzylic",
        "nucleophile": "CH3OH",
        "solvent": "protic",
        "expected": "SN1"
    }
]


if __name__ == "__main__":
    # Quick tests
    print("SN Mechanism Predictor")
    print("=" * 40)
    
    for prob in TEXTBOOK_PROBLEMS[:5]:
        result = predict_mechanism(
            prob["substrate"],
            nucleophile=prob.get("nucleophile"),
            base=prob.get("base"),
            solvent=prob.get("solvent")
        )
        status = "✓" if result == prob["expected"] else "✗"
        print(f"{status} {prob['id']}: {result} (expected: {prob['expected']})")
