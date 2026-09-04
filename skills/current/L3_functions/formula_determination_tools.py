"""
## Solver Instructions (for AI Agent)

When you encounter empirical/molecular formula determination problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Given**: percent composition, atomic masses, molar masses
- **Asked**: empirical formula subscripts, molecular formula subscripts

### Step 2: Choose the correct function
| Task | Function | Key Parameters |
|---|---|---|
| Percent -> moles | `percent_to_moles(percent_by_mass, atomic_masses, basis_mass_g)` | % dict, atomic masses |
| Empirical subscripts | `empirical_formula_subscripts(element_moles, tol)` | mole dict |
| Molecular subscripts | `molecular_formula_subscripts(emp_subs, emp_MM, mol_MM)` | subscripts, masses |

### Step 3: Handle special cases
- `percent_to_moles` converts each element: mass = basis x (%/100), moles = mass / atomic_mass
- `empirical_formula_subscripts` divides by smallest mole value, then integerizes
- `molecular_formula_subscripts` multiplies empirical by ratio (must be near-integer)

### Examples
1. **Glucose**: `percent_to_moles({'C':40, 'H':6.71, 'O':53.29}, {'C':12.01, 'H':1.008, 'O':16.00})` -> moles -> `empirical_formula_subscripts(...)` -> CH2O
2. **Molecular**: `molecular_formula_subscripts({'C':1,'H':2,'O':1}, 30.026, 180.156)` -> C6H12O6
"""

from __future__ import annotations

from typing import Dict, List


def percent_to_moles(percent_by_mass: Dict[str, float], atomic_masses: Dict[str, float], basis_mass_g: float = 100.0) -> Dict[str, float]:
    if basis_mass_g <= 0:
        raise ValueError("basis_mass_g must be > 0")
    out: Dict[str, float] = {}
    for el, pct in percent_by_mass.items():
        if el not in atomic_masses:
            raise ValueError(f"Missing atomic mass for element: {el}")
        if pct < 0:
            raise ValueError("Percent by mass cannot be negative")
        mass = basis_mass_g * (pct / 100.0)
        out[el] = mass / atomic_masses[el]
    return out


def _near_integer_multiplier(x: float, tol: float = 0.05) -> int:
    candidates: List[int] = [1, 2, 3, 4, 5, 6, 8, 10, 12]
    best_k = 1
    best_err = float("inf")
    for k in candidates:
        err = abs(round(x * k) - (x * k))
        if err < best_err:
            best_err = err
            best_k = k
    if best_err > tol:
        raise ValueError(f"Could not integerize ratio {x:.4f} within tolerance {tol}")
    return best_k


def empirical_formula_subscripts(element_moles: Dict[str, float], tol: float = 0.05) -> Dict[str, int]:
    if not element_moles:
        raise ValueError("element_moles is empty")
    smallest = min(v for v in element_moles.values() if v > 0)
    if smallest <= 0:
        raise ValueError("All element mole values must be > 0")

    ratios = {el: n / smallest for el, n in element_moles.items()}

    multipliers = [_near_integer_multiplier(r, tol=tol) for r in ratios.values()]
    k = 1
    for m in multipliers:
        k = (k * m) // _gcd(k, m)

    subs = {el: int(round(r * k)) for el, r in ratios.items()}
    if any(v <= 0 for v in subs.values()):
        raise ValueError("Invalid non-positive subscript generated")
    return _reduce_subscripts(subs)


def molecular_formula_subscripts(empirical_subscripts: Dict[str, int], empirical_molar_mass: float, molecular_molar_mass: float, tol: float = 0.05) -> Dict[str, int]:
    if empirical_molar_mass <= 0 or molecular_molar_mass <= 0:
        raise ValueError("Molar masses must be > 0")
    k = molecular_molar_mass / empirical_molar_mass
    k_round = round(k)
    if abs(k - k_round) > tol:
        raise ValueError(f"Non-integer molecular multiplier k={k:.4f}; check data/tolerance")
    return {el: sub * k_round for el, sub in empirical_subscripts.items()}


def _reduce_subscripts(subs: Dict[str, int]) -> Dict[str, int]:
    vals = list(subs.values())
    g = vals[0]
    for v in vals[1:]:
        g = _gcd(g, v)
    if g <= 1:
        return subs
    return {k: v // g for k, v in subs.items()}


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    am = {"C": 12.011, "H": 1.008, "O": 15.999}
    pct = {"C": 40.00, "H": 6.71, "O": 53.29}
    moles = percent_to_moles(pct, am)
    emp = empirical_formula_subscripts(moles)
    print("empirical:", emp)
    print("molecular:", molecular_formula_subscripts(emp, 30.026, 180.156))


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "empirical_formula_subscripts",
        "description": "empirical formula subscripts",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element_moles": {"type": "string", "description": "Element Moles"},
                "tol": {"type": "number", "description": "Tol", "default": 0.05},
            },
            "required": ["element_moles"]
        }
    },
    {
        "name": "molecular_formula_subscripts",
        "description": "molecular formula subscripts",
        "inputSchema": {
            "type": "object",
            "properties": {
                "empirical_subscripts": {"type": "number", "description": "Empirical Subscripts"},
                "empirical_molar_mass": {"type": "number", "description": "Empirical Molar Mass"},
                "molecular_molar_mass": {"type": "number", "description": "Molecular Molar Mass"},
                "tol": {"type": "number", "description": "Tol", "default": 0.05},
            },
            "required": ["empirical_subscripts", "empirical_molar_mass", "molecular_molar_mass"]
        }
    },
    {
        "name": "percent_to_moles",
        "description": "percent to moles",
        "inputSchema": {
            "type": "object",
            "properties": {
                "percent_by_mass": {"type": "number", "description": "Percent By Mass"},
                "atomic_masses": {"type": "number", "description": "Atomic Masses"},
                "basis_mass_g": {"type": "boolean", "description": "Basis Mass G", "default": 100.0},
            },
            "required": ["percent_by_mass", "atomic_masses"]
        }
    }
]
