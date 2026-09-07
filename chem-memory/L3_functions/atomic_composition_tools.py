"""
Atomic Composition Tools - L3 Implementation
Isotopes, Empirical Formulas, and Percent Composition

## Solver Instructions (for AI Agent)

When you encounter an atomic composition problem, follow this decision tree:

### Step 1: Identify what is given and what is asked
Extract from the question text:
- Isotope masses and abundances: For average atomic mass
- Mass percentages: For empirical formula determination
- Chemical formula: For percent composition
- Moles of elements: For empirical formula
- Ionic charges: For naming or formula determination

### Step 2: Choose the correct function
| Scenario | Function Call |
|----------|---------------|
| Calculate average atomic mass from isotopes | `average_atomic_mass([(mass1, abundance1), (mass2, abundance2), ...])` |
| Determine empirical formula from moles | `empirical_formula(element_mole_dict)` |
| Determine empirical formula from mass percentages | `empirical_formula_from_percent(percent_dict)` |
| Calculate percent composition | `percent_composition(formula, target_element)` |
| Calculate molar mass from formula | `molar_mass_from_formula(formula)` |
| Calculate molarity from mass | `molarity(mass_g, molar_mass_gmol, volume_L)` |
| Check charge balance | `charge_balance_ok(cation_charge, anion_charge, stoich)` |
| Name ionic compound | `simple_ionic_name(cation, cation_charge, anion)` |

### Step 3: Handle special cases
- **Isotope abundance**: Must sum to 1.0 (100%)
- **Empirical formula**: Simplify to lowest whole number ratio
- **Percent composition**: For each element, (n x atomic mass / molar mass) x 100%
- **Ionic naming**: Transition metals need Roman numerals for charge
- **Parentheses in formulas**: Handle correctly (e.g., Ca(OH)2, Mg3(PO4)2)

### Examples

**Example 1: Average atomic mass**
Question: "Calculate the average atomic mass of Cl given 35Cl (34.97 amu, 75.78%) and 37Cl (36.97 amu, 24.22%)."
- Solution: `average_atomic_mass([(34.97, 0.7578), (36.97, 0.2422)])` -> 35.45 amu

**Example 2: Empirical formula from moles**
Question: "A compound has 0.4 mol C, 0.8 mol H, 0.4 mol O. What is the empirical formula?"
- Solution: `empirical_formula({'C': 0.4, 'H': 0.8, 'O': 0.4})` -> {'C': 1, 'H': 2, 'O': 1} = CH2O

**Example 3: Empirical formula from percentages**
Question: "A compound is 40.0% C, 6.7% H, 53.3% O by mass. Find the empirical formula."
- Solution: `empirical_formula_from_percent({'C': 40.0, 'H': 6.7, 'O': 53.3})` -> {'C': 1, 'H': 2, 'O': 1} = CH2O

**Example 4: Percent composition**
Question: "What is the mass percent of N in NH4NO3?"
- Solution: `percent_composition('NH4NO3', 'N')` -> 35.0%

**Example 5: Molar mass with parentheses**
Question: "Calculate the molar mass of Ca3(PO4)2."
- Solution: `molar_mass_from_formula('Ca3(PO4)2')` -> 310.18 g/mol
"""


ATOMIC_MASSES = {
    'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.81,
    'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
    'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938,
    'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.630, 'As': 74.922, 'Se': 78.971, 'Br': 79.904,
    'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Ag': 107.87, 'Cd': 112.41,
    'I': 126.90, 'Ba': 137.33, 'Au': 196.97, 'Hg': 200.59, 'Pb': 207.2,
    'Xe': 131.29,
}

ISOTOPE_ABUNDANCES = {
    'H-1': 0.9999, 'H-2': 0.0001,
    'C-12': 0.9893, 'C-13': 0.0107,
    'N-14': 0.9963, 'N-15': 0.0037,
    'O-16': 0.9976, 'O-17': 0.0004, 'O-18': 0.0020,
    'S-32': 0.9499, 'S-33': 0.0075, 'S-34': 0.0425, 'S-36': 0.0001,
    'Cl-35': 0.7578, 'Cl-37': 0.2422,
    'Br-79': 0.5069, 'Br-81': 0.4931,
}

EXACT_MASSES = {
    'H-1': 1.00783, 'H-2': 2.01410,
    'C-12': 12.00000, 'C-13': 13.00335,
    'N-14': 14.00307, 'N-15': 15.00011,
    'O-16': 15.99491, 'O-17': 16.99913, 'O-18': 17.99916,
    'S-32': 31.97207, 'S-33': 32.97146, 'S-34': 33.96787,
    'Cl-35': 34.96885, 'Cl-37': 36.96590,
    'Br-79': 78.91834, 'Br-81': 80.91629,
}


def average_atomic_mass(isotopes: list[tuple[float, float]]) -> float:
    """isotopes: [(mass, fractional_abundance), ...]"""
    return sum(m * f for m, f in isotopes)


def empirical_formula(element_mole_dict: dict[str, float]) -> dict[str, int]:
    mins = min(v for v in element_mole_dict.values() if v > 0)
    ratios = {k: v / mins for k, v in element_mole_dict.items()}
    rounded = {k: int(round(v)) for k, v in ratios.items()}
    return rounded


def charge_balance_ok(cation_charge: int, anion_charge: int, stoich: tuple[int, int]) -> bool:
    c_n, a_n = stoich
    return c_n * cation_charge + a_n * anion_charge == 0


def simple_ionic_name(cation: str, cation_charge: int, anion: str) -> str:
    roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}.get(cation_charge, str(cation_charge))
    return f"{cation}({roman}) {anion}"


def percent_composition(formula: str, target_element: str, atomic_masses: dict | None = None) -> float:
    """Calculate mass percent of target_element in formula string.
    
    Args:
        formula: Chemical formula like "H2O", "NH4NO3"
        target_element: Element symbol like "N"
        atomic_masses: Dict of element -> mass (optional, uses defaults if None)
    
    Returns:
        Mass percent as float (0-100)
    """
    if atomic_masses is None:
        from unit_conversion_tools import ATOMIC_MASSES
        atomic_masses = ATOMIC_MASSES
    
    import re
    def parse_formula(f):
        """Parse formula, return list of (element, count)."""
        tokens = []
        def _parse(s, pos):
            while pos < len(s):
                if s[pos] == '(':
                    group_tokens, pos = _parse(s, pos + 1)
                    num_match = re.match(r'(\d+)', s[pos:])
                    mult = int(num_match.group(1)) if num_match else 1
                    if num_match: pos += len(num_match.group(1))
                    tokens.extend((e, c * mult) for e, c in group_tokens)
                elif s[pos] == ')':
                    return list(tokens), pos + 1
                elif s[pos].isupper():
                    elem = s[pos]; pos += 1
                    if pos < len(s) and s[pos].islower():
                        elem += s[pos]; pos += 1
                    num_match = re.match(r'(\d+)', s[pos:])
                    count = int(num_match.group(1)) if num_match else 1
                    if num_match: pos += len(num_match.group(1))
                    tokens.append((elem, count))
                else:
                    pos += 1
            return list(tokens), pos
        result, _ = _parse(f, 0)
        return result
    
    total_mass = 0.0
    element_mass = 0.0
    for elem, count in parse_formula(formula):
        mass = atomic_masses.get(elem, 0.0)
        total_mass += mass * count
        if elem == target_element:
            element_mass += mass * count
    
    if total_mass == 0:
        raise ValueError("Could not parse formula or unknown elements")
    return (element_mass / total_mass) * 100


def molar_mass_from_formula(formula: str, atomic_masses: dict | None = None) -> float:
    """Calculate molar mass from formula string. Handles parentheses like Ca3(PO4)2."""
    if atomic_masses is None:
        from unit_conversion_tools import ATOMIC_MASSES
        atomic_masses = ATOMIC_MASSES
    
    import re
    def parse_group(s, pos):
        """Parse formula from pos, return (mass, next_pos)."""
        total = 0.0
        while pos < len(s):
            if s[pos] == '(':
                group_mass, pos = parse_group(s, pos + 1)  # pos now after ')'
                # Read multiplier after ')'
                num_match = re.match(r'(\d+)', s[pos:])
                if num_match:
                    mult = int(num_match.group(1))
                    total += group_mass * mult
                    pos += len(num_match.group(1))
                else:
                    total += group_mass
            elif s[pos] == ')':
                return total, pos + 1
            elif s[pos].isupper():
                elem = s[pos]
                pos += 1
                if pos < len(s) and s[pos].islower():
                    elem += s[pos]
                    pos += 1
                num_match = re.match(r'(\d+)', s[pos:])
                count = int(num_match.group(1)) if num_match else 1
                if num_match:
                    pos += len(num_match.group(1))
                total += atomic_masses.get(elem, 0.0) * count
            else:
                pos += 1
        return total, pos
    
    result, _ = parse_group(formula, 0)
    return result


def molarity(mass_g: float, molar_mass_gmol: float, volume_L: float) -> float:
    """Calculate molarity from mass, molar mass, and solution volume."""
    if molar_mass_gmol <= 0:
        raise ValueError("molar_mass must be > 0")
    if volume_L <= 0:
        raise ValueError("volume must be > 0")
    moles = mass_g / molar_mass_gmol
    return moles / volume_L


def empirical_formula_from_percent(percent_dict: dict[str, float], atomic_masses: dict | None = None) -> dict[str, int]:
    """Determine empirical formula from mass percentages.
    
    Args:
        percent_dict: {"C": 40.0, "H": 6.7, "O": 53.3}
        atomic_masses: Optional element -> mass dict
    """
    if atomic_masses is None:
        from unit_conversion_tools import ATOMIC_MASSES
        atomic_masses = ATOMIC_MASSES
    
    moles = {}
    for elem, pct in percent_dict.items():
        moles[elem] = pct / atomic_masses.get(elem, 1.0)
    
    return empirical_formula(moles)


if __name__ == "__main__":
    print(average_atomic_mass([(35.0, 0.75), (37.0, 0.25)]))
    print(empirical_formula({"C": 0.4, "H": 0.8, "O": 0.4}))
    print(charge_balance_ok(2, -1, (1, 2)))
    print(simple_ionic_name("iron", 3, "chloride"))
    print(percent_composition("NH4NO3", "N"))
    print(molar_mass_from_formula("Ca3(PO4)2"))
    print(molarity(5.85, 58.443, 0.500))
    print(empirical_formula_from_percent({"C": 40.0, "H": 6.7, "O": 53.3}))


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "average_atomic_mass",
        "description": "isotopes: [(mass, fractional_abundance), ...]",
        "inputSchema": {
            "type": "object",
            "properties": {
                "isotopes": {
                    "type": "number",
                    "description": "Isotopes"
                }
            },
            "required": [
                "isotopes"
            ]
        }
    },
    {
        "name": "charge_balance_ok",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cation_charge": {
                    "type": "number",
                    "description": "Cation Charge"
                },
                "anion_charge": {
                    "type": "number",
                    "description": "Anion Charge"
                },
                "stoich": {
                    "type": "number",
                    "description": "Stoich"
                }
            },
            "required": [
                "cation_charge",
                "anion_charge",
                "stoich"
            ]
        }
    },
    {
        "name": "empirical_formula",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element_mole_dict": {
                    "type": "number",
                    "description": "Element Mole Dict"
                }
            },
            "required": [
                "element_mole_dict"
            ]
        }
    },
    {
        "name": "empirical_formula_from_percent",
        "description": "Determine empirical formula from mass percentages.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "percent_dict": {
                    "type": "number",
                    "description": "Percent Dict"
                },
                "atomic_masses": {
                    "type": "number",
                    "description": "Atomic Masses",
                    "default": None
                }
            },
            "required": [
                "percent_dict"
            ]
        }
    },
    {
        "name": "molar_mass_from_formula",
        "description": "Calculate molar mass from formula string. Handles parentheses like Ca3(PO4)2.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {
                    "type": "string",
                    "description": "Formula"
                },
                "atomic_masses": {
                    "type": "number",
                    "description": "Atomic Masses",
                    "default": None
                }
            },
            "required": [
                "formula"
            ]
        }
    },
    {
        "name": "molarity",
        "description": "Calculate molarity from mass, molar mass, and solution volume.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_g": {
                    "type": "number",
                    "description": "Mass G"
                },
                "molar_mass_gmol": {
                    "type": "number",
                    "description": "Molar Mass Gmol"
                },
                "volume_L": {
                    "type": "number",
                    "description": "Volume L"
                }
            },
            "required": [
                "mass_g",
                "molar_mass_gmol",
                "volume_L"
            ]
        }
    },
    {
        "name": "percent_composition",
        "description": "Calculate mass percent of target_element in formula string.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "formula": {
                    "type": "string",
                    "description": "Formula"
                },
                "target_element": {
                    "type": "number",
                    "description": "Target Element"
                },
                "atomic_masses": {
                    "type": "number",
                    "description": "Atomic Masses",
                    "default": None
                }
            },
            "required": [
                "formula",
                "target_element"
            ]
        }
    },
    {
        "name": "simple_ionic_name",
        "description": "",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cation": {
                    "type": "number",
                    "description": "Cation"
                },
                "cation_charge": {
                    "type": "number",
                    "description": "Cation Charge"
                },
                "anion": {
                    "type": "number",
                    "description": "Anion"
                }
            },
            "required": [
                "cation",
                "cation_charge",
                "anion"
            ]
        }
    }
]