"""
Monte Carlo Tools - Metropolis algorithm, sampling helpers.

## Solver Instructions (for AI Agent)

When you encounter Monte Carlo or statistical mechanics sampling problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given energy change DeltaE and temperature -> accept or reject move?
- Given energy and temperature -> calculate Boltzmann weight?
- Given list of sampled energies -> calculate partition function or free energy?

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Metropolis acceptance | `metropolis_accept(dE, T)` | dE in J/mol, T in K -> returns bool |
| Boltzmann weight | `boltzmann_weight(E, T)` | E in J/mol, T in K -> returns exp(-E/RT) |
| Partition function | `canonical_partition(energies, T)` | list of energies, T in K -> returns Q |
| Free energy estimate | `estimate_free_energy(energies, T)` | simplified estimate |

### Step 3: Handle special cases
- Metropolis: Always accept if dE ≤ 0; otherwise accept with probability exp(-dE/RT)
- R = 8.314 J/(mol·K) is used internally
- Partition function Q = Σ exp(-E_i/RT) is fundamental for thermodynamics

### Examples
```python
# Example 1: Metropolis acceptance
metropolis_accept(-500, 300)  # dE=-500 J/mol, T=300K
# -> True (always accept downhill moves)

metropolis_accept(5000, 300)  # dE=+5000 J/mol, T=300K
# -> True or False (probabilistic, ~0.135 probability)

# Example 2: Boltzmann weight
boltzmann_weight(10000, 300)  # E=10 kJ/mol at 300K
# -> exp(-10000/(8.314*300)) ~ 0.018

# Example 3: Partition function
canonical_partition([0, 1000, 2000, 3000], 300)  # energies in J/mol
# -> Q = sum of Boltzmann weights
```
"""
import random
import math

def metropolis_accept(dE: float, T: float) -> bool:
    """Metropolis acceptance criterion. dE in J/mol, T in K."""
    if dE <= 0:
        return True
    R = 8.314
    beta = 1.0 / (R * T)
    prob = math.exp(-beta * dE)
    return random.random() < prob

def boltzmann_weight(E: float, T: float) -> float:
    """Boltzmann weight: exp(-E/kT). E in J/mol."""
    R = 8.314
    return math.exp(-E / (R * T))

def estimate_free_energy(energies: list, T: float) -> float:
    """Estimate free energy from sampled energies using simple averaging."""
    R = 8.314
    n = len(energies)
    avg_e = sum(energies) / n
    return avg_e  # Simplified - real calculation needs partition function

def canonical_partition(energies: list, T: float) -> float:
    """Calculate canonical partition function Q = sum(exp(-E_i/kT))."""
    R = 8.314
    return sum(math.exp(-e / (R * T)) for e in energies)

MCP_TOOLS = [
    {
        "name": "boltzmann_weight",
        "description": "Boltzmann weight: exp(-E/kT). E in J/mol.",
        "parameters": [
            {
                "name": "E",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "canonical_partition",
        "description": "Calculate canonical partition function Q = sum(exp(-E_i/kT)).",
        "parameters": [
            {
                "name": "energies",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "estimate_free_energy",
        "description": "Estimate free energy from sampled energies using simple averaging.",
        "parameters": [
            {
                "name": "energies",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    },
    {
        "name": "metropolis_accept",
        "description": "Metropolis acceptance criterion. dE in J/mol, T in K.",
        "parameters": [
            {
                "name": "dE",
                "type": "number"
            },
            {
                "name": "T",
                "type": "number"
            }
        ]
    }
]
