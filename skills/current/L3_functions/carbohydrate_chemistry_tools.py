"""
L3 Tool: Carbohydrate Chemistry Tools
Disaccharide composition, polysaccharide properties, fiber recommendations.

Source: Human Biology (Wakim and Grewal), Ch3.5
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter carbohydrate problems - disaccharide/polysaccharide composition, glycosidic bond digestibility, energy comparison, or fiber recommendations - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a disaccharide name -> what monosaccharides compose it?
- Given a polysaccharide -> what is its monomer, bond type, and function?
- Given a glycosidic bond type (alpha or beta) -> is it digestible by humans?
- Given age and gender -> what is the daily fiber recommendation?
- Need to compare energy content of carbohydrates vs lipids?

### Step 2: Choose the correct function
- **Disaccharide info:** `disaccharide_info(name)` -> components, common_name, bond_type, digestible, sources. Options: sucrose, lactose, maltose
- **Polysaccharide info:** `polysaccharide_info(name)` -> monomer, bond_type, function, digestible, examples. Options: starch, glycogen, cellulose, chitin
- **Monosaccharide info:** `monosaccharide_info(name)` -> carbons, formula, function. Options: glucose, fructose, galactose
- **Glycosidic bond digestibility:** `glycosidic_bond_digestibility(bond_type)` -> alpha=digestible (starch/glycogen), beta=indigestible (cellulose/chitin)
- **Fiber recommendation:** `fiber_recommendation(age, gender)` -> grams/day. Male ≤50: 38g, male >50: 30g, female ≤50: 25g, female >50: 21g
- **Energy comparison:** `energy_comparison()` -> carbohydrate=4 kcal/g, lipid=9 kcal/g, ratio=2.25
- **Glycogen storage:** `glycogen_storage_info()` -> storage sites (liver vs muscle), homeostasis role

### Step 3: Handle special cases
- Humans CANNOT digest beta-glycosidic bonds -> cellulose and chitin pass through undigested (fiber!)
- Lactose requires lactase enzyme -> lactose-intolerant individuals lack this enzyme
- Starch has both alpha-1,4 (linear) and alpha-1,6 (branched) linkages; glycogen is more highly branched
- Sucrose is alpha-1,2 linkage (glucose+fructose) - no reducing end, so it's a non-reducing sugar

### Examples
```python
# Example 1: What makes up lactose?
disaccharide_info('lactose')  -> {'components': ['glucose', 'galactose'], 'bond_type': 'beta-1,4'}

# Example 2: Why can't we digest cellulose?
glycosidic_bond_digestibility('beta')  -> digestible=False, explanation='Humans lack beta-glycosidase'

# Example 3: Fiber recommendation for 30-year-old male
fiber_recommendation(30, 'male')  -> 38 grams/day

# Example 4: Compare starch vs cellulose
polysaccharide_info('starch')  -> digestible=True, bond='alpha-1,4 + alpha-1,6'
polysaccharide_info('cellulose')  -> digestible=False, bond='beta-1,4'
```
"""

# Disaccharide database
DISACCHARIDES = {
    'sucrose': {
        'components': ['glucose', 'fructose'],
        'common_name': 'table sugar',
        'bond_type': 'alpha-1,2',
        'digestible': True,
        'sources': ['sugar cane', 'sugar beet']
    },
    'lactose': {
        'components': ['glucose', 'galactose'],
        'common_name': 'milk sugar',
        'bond_type': 'beta-1,4',
        'digestible': True,  # Requires lactase
        'sources': ['milk', 'dairy']
    },
    'maltose': {
        'components': ['glucose', 'glucose'],
        'common_name': 'malt sugar',
        'bond_type': 'alpha-1,4',
        'digestible': True,
        'sources': ['malt', 'beer']
    },
}

# Polysaccharide database
POLYSACCHARIDES = {
    'starch': {
        'monomer': 'glucose',
        'bond_type': 'alpha-1,4 (linear) + alpha-1,6 (branched)',
        'function': 'plant energy storage',
        'digestible': True,
        'examples': ['potatoes', 'rice', 'wheat']
    },
    'glycogen': {
        'monomer': 'glucose',
        'bond_type': 'alpha-1,4 + alpha-1,6 (highly branched)',
        'function': 'animal energy storage',
        'digestible': True,
        'storage_sites': ['liver', 'muscle']
    },
    'cellulose': {
        'monomer': 'glucose',
        'bond_type': 'beta-1,4',
        'function': 'structural (plant cell walls)',
        'digestible': False,
        'examples': ['cotton', 'wood', 'paper']
    },
    'chitin': {
        'monomer': 'N-acetylglucosamine',
        'bond_type': 'beta-1,4',
        'function': 'structural (exoskeletons)',
        'digestible': False,
        'examples': ['insect shells', 'crab shells', 'fungal cell walls']
    },
}

# Monosaccharide database
MONOSACCHARIDES = {
    'glucose': {'carbons': 6, 'formula': 'C6H12O6', 'function': 'primary energy source'},
    'fructose': {'carbons': 6, 'formula': 'C6H12O6', 'function': 'fruit sugar'},
    'galactose': {'carbons': 6, 'formula': 'C6H12O6', 'function': 'milk sugar component'},
}

# Fiber recommendations (grams per day)
FIBER_RECOMMENDATIONS = {
    ('male', 'young'): 38,    # Age ≤50
    ('male', 'older'): 30,    # Age >50
    ('female', 'young'): 25,  # Age ≤50
    ('female', 'older'): 21,  # Age >50
}


def disaccharide_info(name: str) -> dict:
    """
    Get disaccharide composition and properties.
    
    Args:
        name: Disaccharide name (e.g., 'sucrose', 'lactose')
    
    Returns:
        Dictionary with disaccharide properties
    
    Example:
        >>> disaccharide_info('sucrose')
        {'components': ['glucose', 'fructose'], ...}
    """
    name = name.lower()
    if name in DISACCHARIDES:
        result = DISACCHARIDES[name].copy()
        result['name'] = name
        return result
    return {'error': f'Unknown disaccharide: {name}'}


def polysaccharide_info(name: str) -> dict:
    """
    Get polysaccharide composition and properties.
    
    Args:
        name: Polysaccharide name (e.g., 'starch', 'cellulose')
    
    Returns:
        Dictionary with polysaccharide properties
    
    Example:
        >>> polysaccharide_info('glycogen')
        {'monomer': 'glucose', 'function': 'animal energy storage', ...}
    """
    name = name.lower()
    if name in POLYSACCHARIDES:
        result = POLYSACCHARIDES[name].copy()
        result['name'] = name
        return result
    return {'error': f'Unknown polysaccharide: {name}'}


def monosaccharide_info(name: str) -> dict:
    """
    Get monosaccharide properties.
    
    Args:
        name: Monosaccharide name (e.g., 'glucose')
    
    Returns:
        Dictionary with monosaccharide properties
    """
    name = name.lower()
    if name in MONOSACCHARIDES:
        result = MONOSACCHARIDES[name].copy()
        result['name'] = name
        return result
    return {'error': f'Unknown monosaccharide: {name}'}


def fiber_recommendation(age: int, gender: str) -> dict:
    """
    Get daily fiber recommendation.
    
    Args:
        age: Age in years
        gender: 'male' or 'female'
    
    Returns:
        Dictionary with fiber recommendation
    
    Example:
        >>> fiber_recommendation(30, 'male')
        {'grams': 38, 'category': 'young adult'}
    """
    gender = gender.lower()
    age_category = 'young' if age <= 50 else 'older'
    key = (gender, age_category)
    
    if key in FIBER_RECOMMENDATIONS:
        grams = FIBER_RECOMMENDATIONS[key]
        return {
            'grams': grams,
            'age': age,
            'gender': gender,
            'category': f'{age_category} adult',
            'ratio_note': 'Recommended: 3 parts insoluble to 1 part soluble fiber'
        }
    return {'error': f'Invalid gender: {gender}'}


def energy_comparison() -> dict:
    """
    Compare energy density of carbohydrates vs lipids.
    
    Returns:
        Dictionary with energy comparison
    
    Example:
        >>> energy_comparison()
        {'carbohydrate': 4, 'lipid': 9, 'ratio': 2.25}
    """
    carb_energy = 4  # kcal/g
    lipid_energy = 9  # kcal/g
    
    return {
        'carbohydrate': carb_energy,
        'lipid': lipid_energy,
        'ratio': round(lipid_energy / carb_energy, 2),
        'note': 'Lipids provide >2x energy per gram compared to carbohydrates'
    }


def glycosidic_bond_digestibility(bond_type: str) -> dict:
    """
    Determine if glycosidic bond is digestible by humans.
    
    Args:
        bond_type: 'alpha' or 'beta' (or 'alpha' or 'beta')
    
    Returns:
        Dictionary with digestibility info
    """
    bond_type_lower = bond_type.lower()
    # Normalize Unicode Greek letters to ASCII equivalents
    bond_type_lower = bond_type_lower.replace('α', 'alpha').replace('β', 'beta')
    bond_type_lower = bond_type_lower.replace('α', 'alpha').replace('β', 'beta')
    
    if 'alpha' in bond_type_lower:
        return {
            'bond_type': 'alpha-glycosidic',
            'digestible': True,
            'examples': ['starch', 'glycogen'],
            'explanation': 'Human enzymes can break alpha-glycosidic bonds'
        }
    elif 'beta' in bond_type_lower:
        return {
            'bond_type': 'beta-glycosidic',
            'digestible': False,
            'examples': ['cellulose', 'chitin'],
            'explanation': 'Humans lack enzymes to break beta-glycosidic bonds'
        }
    return {'error': f'Unknown bond type: {bond_type}'}


def glycogen_storage_info() -> dict:
    """
    Get information about glycogen storage in humans.
    
    Returns:
        Dictionary with glycogen storage information
    """
    return {
        'storage_sites': ['liver', 'muscle'],
        'liver_function': 'Supplies glucose to whole body',
        'muscle_function': 'Supplies glucose to muscle cells only',
        'homeostasis': 'Liver glycogen regulates blood glucose',
        'comparison_to_lipid': 'Less compact energy storage than lipids'
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "CARB-01",
        "question": "Monosaccharide carbon count",
        "expected_carbons": 6
    },
    {
        "id": "CARB-02",
        "question": "Disaccharide composition",
        "name": "lactose",
        "expected_components": ['glucose', 'galactose']
    },
    {
        "id": "CARB-03",
        "question": "Energy comparison",
        "expected_ratio": 2.25
    },
    {
        "id": "CARB-04",
        "question": "Fiber recommendation",
        "age": 30,
        "gender": "male",
        "expected_grams": 38
    },
    {
        "id": "CARB-05",
        "question": "Polysaccharide function",
        "name": "glycogen",
        "expected_function": "animal energy storage"
    },
]


if __name__ == "__main__":
    print("Carbohydrate Chemistry Tools")
    print("=" * 40)
    
    # Test disaccharides
    print("\nDisaccharides:")
    for name in ['sucrose', 'lactose', 'maltose']:
        info = disaccharide_info(name)
        print(f"  {name}: {' + '.join(info['components'])}")
    
    # Test polysaccharides
    print("\nPolysaccharides:")
    for name in ['starch', 'glycogen', 'cellulose']:
        info = polysaccharide_info(name)
        print(f"  {name}: {info['function']}")
    
    # Test energy comparison
    print("\nEnergy Comparison:")
    energy = energy_comparison()
    print(f"  Carbs: {energy['carbohydrate']} kcal/g")
    print(f"  Lipids: {energy['lipid']} kcal/g")
    print(f"  Ratio: {energy['ratio']}x")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'disaccharide_info', 'description': "Get disaccharide composition and properties.\n\nArgs:\n    name: Disaccharide name (e.g., 'sucrose', 'lactose')\n\nReturns:\n    Dictionary with disaccharide properties\n\nExample:\n    >>> disaccharide_info('sucrose')\n    {'components': ['glucose', 'fructose'], ...}", 'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string', 'description': 'Name'}}, 'required': ['name']}},
    {'name': 'energy_comparison', 'description': "Compare energy density of carbohydrates vs lipids.\n\nReturns:\n    Dictionary with energy comparison\n\nExample:\n    >>> energy_comparison()\n    {'carbohydrate': 4, 'lipid': 9, 'ratio': 2.25}", 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'fiber_recommendation', 'description': "Get daily fiber recommendation.\n\nArgs:\n    age: Age in years\n    gender: 'male' or 'female'\n\nReturns:\n    Dictionary with fiber recommendation\n\nExample:\n    >>> fiber_recommendation(30, 'male')\n    {'grams': 38, 'category': 'young adult'}", 'inputSchema': {'type': 'object', 'properties': {'age': {'type': 'number', 'description': 'Age'}, 'gender': {'type': 'number', 'description': 'Gender'}}, 'required': ['age', 'gender']}},
    {'name': 'glycogen_storage_info', 'description': 'Get information about glycogen storage in humans.\n\nReturns:\n    Dictionary with glycogen storage information', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'glycosidic_bond_digestibility', 'description': "Determine if glycosidic bond is digestible by humans.\n\nArgs:\n    bond_type: 'alpha' or 'beta' (or 'alpha' or 'beta')\n\nReturns:\n    Dictionary with digestibility info", 'inputSchema': {'type': 'object', 'properties': {'bond_type': {'type': 'string', 'description': 'Bond Type'}}, 'required': ['bond_type']}},
    {'name': 'monosaccharide_info', 'description': "Get monosaccharide properties.\n\nArgs:\n    name: Monosaccharide name (e.g., 'glucose')\n\nReturns:\n    Dictionary with monosaccharide properties", 'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string', 'description': 'Name'}}, 'required': ['name']}},
    {'name': 'polysaccharide_info', 'description': "Get polysaccharide composition and properties.\n\nArgs:\n    name: Polysaccharide name (e.g., 'starch', 'cellulose')\n\nReturns:\n    Dictionary with polysaccharide properties\n\nExample:\n    >>> polysaccharide_info('glycogen')\n    {'monomer': 'glucose', 'function': 'animal energy storage', ...}", 'inputSchema': {'type': 'object', 'properties': {'name': {'type': 'string', 'description': 'Name'}}, 'required': ['name']}}
]
