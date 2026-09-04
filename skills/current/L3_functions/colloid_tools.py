"""
Colloid Tools - L3 Implementation
Chapter 11.05: Colloids and Dispersions

## Solver Instructions (for AI Agent)

When you encounter colloid and mixture classification problems:

### Step 1: Identify what is given and what is asked
- Given: particle size, dispersed/dispersing medium types
- Asked: colloid type, Tyndall effect, settling behavior, examples

### Step 2: Choose the correct function
- `classify_by_particle_size(size_nm)`: True solution/colloid/suspension
- `identify_colloid_type(dispersed, dispersing)`: Aerosol/foam/emulsion/sol/gel
- `tyndall_effect_test(particle_size_nm)`: Will Tyndall effect be visible?
- `settling_behavior(particle_size_nm)`: Settling prediction
- `filtration_behavior(particle_size_nm)`: Can it be filtered?
- `get_colloid_examples(colloid_type)`: Examples of a colloid type
- `compare_mixture_types()`: Comparison table of all mixture types

### Step 3: Handle special cases
- Colloids: 1-1000 nm; True solutions: <1 nm; Suspensions: >1000 nm
- Brownian motion prevents settling in colloids

### Examples
```python
classify_by_particle_size(500)  # -> 'colloid'
identify_colloid_type('liquid', 'gas')  # -> 'foam'
tyndall_effect_test(100)  # -> True
```
"""

from typing import Tuple, Optional

# Colloid classification by dispersed and dispersing phases
COLLOID_TYPES = {
    ('solid', 'liquid'): 'sol',
    ('liquid', 'solid'): 'gel',
    ('liquid', 'liquid'): 'emulsion',
    ('gas', 'liquid'): 'foam',
    ('gas', 'solid'): 'solid foam',
    ('solid', 'gas'): 'solid aerosol',
    ('liquid', 'gas'): 'liquid aerosol',
}

# Examples of colloids
COLLOID_EXAMPLES = {
    'sol': ['paint', 'ink', 'blood plasma'],
    'gel': ['gelatin', 'jelly', 'agar'],
    'emulsion': ['milk', 'mayonnaise', 'butter'],
    'foam': ['whipped cream', 'soap suds', 'beer foam'],
    'solid foam': ['styrofoam', 'marshmallow', 'pumice'],
    'solid aerosol': ['smoke', 'dust in air'],
    'liquid aerosol': ['fog', 'mist', 'clouds'],
}


def classify_by_particle_size(size_nm: float) -> str:
    """
    Classify mixture type by particle size.
    
    Args:
        size_nm: Particle size in nanometers
    
    Returns:
        Mixture type: 'solution', 'colloid', or 'suspension'
    
    Examples:
        >>> classify_by_particle_size(0.5)
        'solution'
        >>> classify_by_particle_size(100)
        'colloid'
        >>> classify_by_particle_size(2000)
        'suspension'
    """
    if size_nm < 1:
        return 'solution'
    elif size_nm <= 1000:
        return 'colloid'
    else:
        return 'suspension'


def identify_colloid_type(dispersed: str, dispersing: str) -> str:
    """
    Identify colloid type from dispersed and dispersing phases.
    
    Args:
        dispersed: Dispersed phase ('solid', 'liquid', or 'gas')
        dispersing: Dispersing medium ('solid', 'liquid', or 'gas')
    
    Returns:
        Colloid type name
    
    Examples:
        >>> identify_colloid_type('solid', 'liquid')
        'sol'
        >>> identify_colloid_type('liquid', 'liquid')
        'emulsion'
    """
    dispersed = dispersed.lower()
    dispersing = dispersing.lower()
    
    key = (dispersed, dispersing)
    return COLLOID_TYPES.get(key, 'unknown colloid type')


def tyndall_effect_test(particle_size_nm: float) -> bool:
    """
    Determine if mixture will show Tyndall effect.
    
    Args:
        particle_size_nm: Particle size in nanometers
    
    Returns:
        True if Tyndall effect will be observed
    
    Examples:
        >>> tyndall_effect_test(0.5)
        False
        >>> tyndall_effect_test(100)
        True
    """
    # Tyndall effect observed for colloids and suspensions (1-1000+ nm)
    return particle_size_nm >= 1


def settling_behavior(particle_size_nm: float) -> str:
    """
    Predict settling behavior based on particle size.
    
    Args:
        particle_size_nm: Particle size in nanometers
    
    Returns:
        Description of settling behavior
    """
    if particle_size_nm < 1:
        return 'Will not settle (solution particles too small)'
    elif particle_size_nm <= 1000:
        return 'Will not settle (Brownian motion keeps particles suspended)'
    else:
        return 'Will settle over time (suspension particles are large enough)'


def filtration_behavior(particle_size_nm: float) -> str:
    """
    Predict filtration behavior based on particle size.
    
    Args:
        particle_size_nm: Particle size in nanometers
    
    Returns:
        Description of filtration behavior
    """
    if particle_size_nm < 1:
        return 'Will pass through filter paper'
    elif particle_size_nm <= 1000:
        return 'Will pass through filter paper (too small)'
    else:
        return 'Will be retained by filter paper'


def get_colloid_examples(colloid_type: str) -> list:
    """
    Get examples of a specific colloid type.
    
    Args:
        colloid_type: Type of colloid (e.g., 'sol', 'emulsion')
    
    Returns:
        List of examples
    """
    return COLLOID_EXAMPLES.get(colloid_type.lower(), [])


def compare_mixture_types() -> dict:
    """
    Return comparison table of mixture types.
    
    Returns:
        Dictionary comparing solutions, colloids, and suspensions
    """
    return {
        'solution': {
            'particle_size': '< 1 nm',
            'settles': False,
            'filterable': False,
            'tyndall_effect': False,
            'example': 'salt water, sugar water'
        },
        'colloid': {
            'particle_size': '1-1000 nm',
            'settles': False,
            'filterable': False,
            'tyndall_effect': True,
            'example': 'milk, fog, paint'
        },
        'suspension': {
            'particle_size': '> 1000 nm',
            'settles': True,
            'filterable': True,
            'tyndall_effect': True,
            'example': 'muddy water, flour in water'
        }
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'classify_by_particle_size', 'description': "Classify mixture type by particle size.\n\nArgs:\n    size_nm: Particle size in nanometers\n\nReturns:\n    Mixture type: 'solution', 'colloid', or 'suspension'\n\nExamples:\n    >>> classify_by_particle_size(0.5)\n    'solution'\n    >>> classify_by_particle_size(100)\n    'colloid'\n    >>> classify_by_particle_size(2000)\n    'suspension'", 'inputSchema': {'type': 'object', 'properties': {'size_nm': {'type': 'number', 'description': 'Size Nm'}}, 'required': ['size_nm']}},
    {'name': 'compare_mixture_types', 'description': 'Return comparison table of mixture types.\n\nReturns:\n    Dictionary comparing solutions, colloids, and suspensions', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'filtration_behavior', 'description': 'Predict filtration behavior based on particle size.\n\nArgs:\n    particle_size_nm: Particle size in nanometers\n\nReturns:\n    Description of filtration behavior', 'inputSchema': {'type': 'object', 'properties': {'particle_size_nm': {'type': 'string', 'description': 'Particle Size Nm'}}, 'required': ['particle_size_nm']}},
    {'name': 'get_colloid_examples', 'description': "Get examples of a specific colloid type.\n\nArgs:\n    colloid_type: Type of colloid (e.g., 'sol', 'emulsion')\n\nReturns:\n    List of examples", 'inputSchema': {'type': 'object', 'properties': {'colloid_type': {'type': 'string', 'description': 'Colloid Type'}}, 'required': ['colloid_type']}},
    {'name': 'identify_colloid_type', 'description': "Identify colloid type from dispersed and dispersing phases.\n\nArgs:\n    dispersed: Dispersed phase ('solid', 'liquid', or 'gas')\n    dispersing: Dispersing medium ('solid', 'liquid', or 'gas')\n\nReturns:\n    Colloid type name\n\nExamples:\n    >>> identify_colloid_type('solid', 'liquid')\n    'sol'\n    >>> identify_colloid_type('liquid', 'liquid')\n    'emulsion'", 'inputSchema': {'type': 'object', 'properties': {'dispersed': {'type': 'number', 'description': 'Dispersed'}, 'dispersing': {'type': 'number', 'description': 'Dispersing'}}, 'required': ['dispersed', 'dispersing']}},
    {'name': 'settling_behavior', 'description': 'Predict settling behavior based on particle size.\n\nArgs:\n    particle_size_nm: Particle size in nanometers\n\nReturns:\n    Description of settling behavior', 'inputSchema': {'type': 'object', 'properties': {'particle_size_nm': {'type': 'string', 'description': 'Particle Size Nm'}}, 'required': ['particle_size_nm']}},
    {'name': 'tyndall_effect_test', 'description': 'Determine if mixture will show Tyndall effect.\n\nArgs:\n    particle_size_nm: Particle size in nanometers\n\nReturns:\n    true if Tyndall effect will be observed\n\nExamples:\n    >>> tyndall_effect_test(0.5)\n    false\n    >>> tyndall_effect_test(100)\n    true', 'inputSchema': {'type': 'object', 'properties': {'particle_size_nm': {'type': 'string', 'description': 'Particle Size Nm'}}, 'required': ['particle_size_nm']}}
]
