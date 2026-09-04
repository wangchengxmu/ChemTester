"""
Kinetic Theory and Effusion Tools - L3 Implementation
Chapter 8.05-8.06: Effusion, Diffusion, and Kinetic Molecular Theory

## Solver Instructions (for AI Agent)

When you encounter a kinetic theory or effusion problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Molar masses (M): Look for chemical formulas (e.g., "H2", "O2", "CH4") and calculate or look up molar mass
- Effusion rates: Look for "rate", "effuse", "diffuse", often given as relative values
- Times: Look for "time taken", "seconds", "minutes" - inverse of rate
- Temperature (T): MUST be in Kelvin (K = degC + 273.15)
- Speed type: Look for "rms speed", "average speed", "most probable speed", "root mean square"

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Compare effusion rates of two gases | `grahams_law(M1, M2)` - returns rate ratio |
| Find unknown molar mass from rate ratio | `grahams_law(M1, rate1, rate2)` - M2 = None |
| Find rate from times (inverse relationship) | `grahams_law(M1, M2, time1, time2)` - rate ∝ 1/time |
| Calculate RMS speed | `rms_speed(T, M)` - returns m/s |
| Calculate average speed | `average_speed(T, M)` - returns m/s |
| Calculate most probable speed | `most_probable_speed(T, M)` - returns m/s |
| Calculate KE per mole | `kinetic_energy_per_mole(T)` - returns J/mol |
| Calculate KE per molecule | `kinetic_energy_per_molecule(T)` - returns J/molecule |
| Compare speeds of two gases | `compare_speeds(T, M1, M2)` - returns dict |

### Step 3: Handle special cases
- **Molar mass extraction**: Extract chemical formula from question (e.g., "hydrogen gas" = H2, M = 2.0 g/mol; "oxygen" = O2, M = 32.0 g/mol)
- **Rate vs Time**: Rate is inversely proportional to time. If time given, use time parameters OR convert: rate = 1/time
- **Speed relationships**: u_rms > u_avg > u_mp (always in this order for same gas)
- **Temperature dependence**: All speeds ∝ √T; KE ∝ T (doubles if T doubles)
- **Molar mass units**: Input in g/mol, internally converted to kg/mol for speed calculations
- **Graham's Law**: Lighter gas effuses faster. rate1/rate2 = √(M2/M1)

### Examples

**Example 1: Graham's Law - Rate comparison**
Question: "How many times faster does H2 effuse compared to O2?"
- Given: M(H2) = 2.0 g/mol, M(O2) = 32.0 g/mol
- Solution: `grahams_law(M1=2.0, M2=32.0)` -> 4.0 (H2 effuses 4x faster)

**Example 2: Graham's Law - Find molar mass**
Question: "A gas effuses 1.5 times faster than CO2 (M=44 g/mol). What is its molar mass?"
- Given: rate1/rate2 = 1.5, M(CO2) = 44 g/mol
- Solution: `grahams_law(M1=None, M2=44, rate1=1.5, rate2=1)` -> M1 ~ 19.6 g/mol

**Example 3: RMS speed**
Question: "Calculate the rms speed of N2 molecules at 300 K."
- Given: T = 300 K, M(N2) = 28.0 g/mol
- Solution: `rms_speed(T=300, M=28.0)` -> ~ 517 m/s

**Example 4: Kinetic energy**
Question: "What is the average kinetic energy of 1 mole of gas at 298 K?"
- Given: T = 298 K
- Solution: `kinetic_energy_per_mole(T=298)` -> ~ 3716 J/mol ~ 3.72 kJ/mol
"""

from typing import Optional
from math import sqrt, pi

R_J = 8.314  # J/(mol·K)


def grahams_law(M1: Optional[float] = None, M2: Optional[float] = None,
                rate1: Optional[float] = None, rate2: Optional[float] = None,
                time1: Optional[float] = None, time2: Optional[float] = None) -> float:
    """
    Apply Graham's Law of Effusion: rate1/rate2 = √(M2/M1).
    
    Args:
        M1, M2: Molar masses in g/mol
        rate1, rate2: Effusion rates (volume/time or distance/time)
        time1, time2: Time for equal volumes to effuse (inverse of rate)
        Exactly one argument should be None when solving for missing value.
        If only M1 and M2 provided, returns rate1/rate2 ratio.
    
    Returns:
        The missing value or rate ratio if only M1, M2 given
    
    Examples:
        >>> grahams_law(M1=2, M2=32)  # H2 vs O2
        4.0
        >>> grahams_law(M1=2, rate1=4, rate2=1)  # Find M2
        32.0
    """
    # If times given, convert to rates (rate ∝ 1/time)
    if time1 is not None and time2 is not None:
        rate1, rate2 = 1/time1, 1/time2
    
    # If only M1 and M2 given, return rate ratio
    if rate1 is None and rate2 is None:
        return sqrt(M2 / M1)
    
    args = [M1, M2, rate1, rate2]
    if sum(a is None for a in args) != 1:
        raise ValueError("Exactly one argument must be None (or only M1, M2 for ratio)")
    
    if M1 is None:
        # rate1/rate2 = sqrt(M2/M1) -> M1 = M2 * (rate2/rate1)2
        return M2 * (rate2 / rate1) ** 2
    elif M2 is None:
        # M2 = M1 * (rate1/rate2)2
        return M1 * (rate1 / rate2) ** 2
    elif rate1 is None:
        # rate1 = rate2 * sqrt(M2/M1)
        return rate2 * sqrt(M2 / M1)
    else:  # rate2 is None
        # rate2 = rate1 * sqrt(M1/M2)
        return rate1 * sqrt(M1 / M2)


def rms_speed(T: float, M: float, R: float = R_J) -> float:
    """
    Calculate root mean square speed of gas molecules.
    
    Args:
        T: Temperature in Kelvin
        M: Molar mass in g/mol (converted to kg/mol internally)
        R: Gas constant (default 8.314 J/(mol·K))
    
    Returns:
        RMS speed in m/s
    
    Examples:
        >>> rms_speed(273, 2)  # H2 at 0degC
        1838.0...
        >>> rms_speed(273, 32)  # O2 at 0degC
        461.0...
    """
    M_kg = M / 1000  # Convert g/mol to kg/mol
    return sqrt(3 * R * T / M_kg)


def average_speed(T: float, M: float, R: float = R_J) -> float:
    """
    Calculate average (mean) speed of gas molecules.
    
    Args:
        T: Temperature in Kelvin
        M: Molar mass in g/mol
        R: Gas constant (default 8.314 J/(mol·K))
    
    Returns:
        Average speed in m/s
    
    Examples:
        >>> average_speed(273, 2)  # H2 at 0degC
        1694.0...
    """
    M_kg = M / 1000
    return sqrt(8 * R * T / (pi * M_kg))


def most_probable_speed(T: float, M: float, R: float = R_J) -> float:
    """
    Calculate most probable speed of gas molecules.
    
    Args:
        T: Temperature in Kelvin
        M: Molar mass in g/mol
        R: Gas constant (default 8.314 J/(mol·K))
    
    Returns:
        Most probable speed in m/s
    
    Examples:
        >>> most_probable_speed(273, 2)  # H2 at 0degC
        1500.0...
    """
    M_kg = M / 1000
    return sqrt(2 * R * T / M_kg)


def kinetic_energy_per_mole(T: float, R: float = R_J) -> float:
    """
    Calculate average kinetic energy per mole of gas.
    
    Args:
        T: Temperature in Kelvin
        R: Gas constant (default 8.314 J/(mol·K))
    
    Returns:
        Kinetic energy in J/mol
    
    Examples:
        >>> kinetic_energy_per_mole(273)
        3405.0...
        >>> kinetic_energy_per_mole(298)
        3717.0...
    """
    return 1.5 * R * T


def kinetic_energy_per_molecule(T: float) -> float:
    """
    Calculate average kinetic energy per molecule.
    
    Args:
        T: Temperature in Kelvin
    
    Returns:
        Kinetic energy in J/molecule
    
    Examples:
        >>> kinetic_energy_per_molecule(273)
        5.65e-21...
    """
    k = 1.380649e-23  # Boltzmann constant
    return 1.5 * k * T


def compare_speeds(T: float, M1: float, M2: float) -> dict:
    """
    Compare molecular speeds of two gases at same temperature.
    
    Args:
        T: Temperature in Kelvin
        M1, M2: Molar masses in g/mol
    
    Returns:
        Dictionary with speeds for both gases
    
    Examples:
        >>> compare_speeds(273, 2, 32)
        {'M1_rms': 1838..., 'M2_rms': 461..., 'ratio': 4.0}
    """
    u1 = rms_speed(T, M1)
    u2 = rms_speed(T, M2)
    
    return {
        'M1_rms': u1,
        'M2_rms': u2,
        'ratio': u1 / u2,
        'M1_avg': average_speed(T, M1),
        'M2_avg': average_speed(T, M2),
        'M1_mp': most_probable_speed(T, M1),
        'M2_mp': most_probable_speed(T, M2),
    }


def particle_speed_statistics(speeds: list) -> dict:
    """
    Calculate average, RMS, and most probable speed from discrete particle speed data.
    
    Used when given a list of individual particle speeds (not a distribution).
    
    Args:
        speeds: List of individual particle speeds (m/s or any consistent unit)
    
    Returns:
        Dict with keys:
        - 'average': arithmetic mean speed
        - 'rms': root-mean-square speed
        - 'most_probable': most frequent speed (mode)
        - 'n': number of particles
    
    Examples:
        >>> particle_speed_statistics([0.1, 1.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 5.0, 6.0])
        {'average': 3.1, 'rms': 3.5..., 'most_probable': 3.0, 'n': 10}
        >>> particle_speed_statistics([1.0, 4.0, 4.0, 6.0, 6.0, 6.0, 8.0, 10.0])
        {'average': 5.625, 'rms': 6.2..., 'most_probable': 6.0, 'n': 8}
    """
    from collections import Counter
    n = len(speeds)
    if n == 0:
        raise ValueError("Speeds list must not be empty")
    
    avg = sum(speeds) / n
    rms_val = sqrt(sum(s * s for s in speeds) / n)
    
    # Most probable = mode (most frequent value)
    counter = Counter(speeds)
    most_prob = counter.most_common(1)[0][0]
    
    return {'average': avg, 'rms': rms_val, 'most_probable': most_prob, 'n': n}


MCP_TOOLS = [
    {
        "name": "average_speed",
        "description": "Calculate average (mean) speed of gas molecules.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "M",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "compare_speeds",
        "description": "Compare molecular speeds of two gases at same temperature.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "M1",
                "type": "number"
            },
            {
                "name": "M2",
                "type": "number"
            }
        ]
    },
    {
        "name": "grahams_law",
        "description": "Apply Graham's Law of Effusion: rate1/rate2 = √(M2/M1).",
        "parameters": [
            {
                "name": "M1",
                "type": "number"
            },
            {
                "name": "M2",
                "type": "number"
            },
            {
                "name": "rate1",
                "type": "number"
            },
            {
                "name": "rate2",
                "type": "number"
            },
            {
                "name": "time1",
                "type": "number"
            },
            {
                "name": "time2",
                "type": "number"
            }
        ]
    },
    {
        "name": "kinetic_energy_per_mole",
        "description": "Calculate average kinetic energy per mole of gas.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "kinetic_energy_per_molecule",
        "description": "Calculate average kinetic energy per molecule.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "most_probable_speed",
        "description": "Calculate most probable speed of gas molecules.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "M",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    },
    {
        "name": "rms_speed",
        "description": "Calculate root mean square speed of gas molecules.",
        "parameters": [
            {
                "name": "T",
                "type": "number"
            },
            {
                "name": "M",
                "type": "number"
            },
            {
                "name": "R",
                "type": "number"
            }
        ]
    }
]
