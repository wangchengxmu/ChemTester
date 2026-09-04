"""
Electron Configuration Tools (L3)
Source: LibreTexts Chemistry 2e Ch06.04

## Solver Instructions (for AI Agent)

When you encounter electron configuration problems:

### Step 1: Identify what is given and what is asked
- Given: atomic number, element symbol, or configuration string
- Asked: electron configuration, valence electrons, orbital diagram, exception check

### Step 2: Choose the correct function
- `electron_configuration(atomic_number, noble_gas_notation, use_exceptions, unicode_superscripts)`: Full config
- `valence_electrons(atomic_number)`: Count valence electrons for main group
- `is_exception(atomic_number)`: Check Cr(24), Cu(29), Mo(42), Ag(47), etc.
- `orbital_diagram_electrons(subshell, electrons)`: Hund's rule orbital filling
- `parse_configuration(config_str)`: Parse string to {subshell: electrons} dict

### Step 3: Handle special cases
- Aufbau exceptions: Cr (4s13d5), Cu (4s13d10), Mo, Ru, Rh, Pd, Ag
- Noble gas notation: use nearest noble gas as core
- Hund's rule: maximize unpaired electrons before pairing

### Examples
```python
electron_configuration(26)  # Fe -> [Ar] 4s2 3d6
electron_configuration(24)  # Cr -> [Ar] 4s1 3d5 (exception!)
orbital_diagram_electrons('p', 4)  # -> ['^v', '^', '^']
```
"""

# === AUFBAU ORDER ===

# Filling order: subshells in order of increasing energy
AUFBAU_ORDER = [
    '1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p',
    '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p'
]

# Max electrons per subshell
SUBSHELL_CAPACITY = {'s': 2, 'p': 6, 'd': 10, 'f': 14}

# Noble gas electron configurations
NOBLE_GAS_CORES = {
    2: 'He',    # 1s2
    10: 'Ne',   # [He] 2s2 2p6
    18: 'Ar',   # [Ne] 3s2 3p6
    36: 'Kr',   # [Ar] 4s2 3d10 4p6
    54: 'Xe',   # [Kr] 5s2 4d10 5p6
    86: 'Rn',   # [Xe] 6s2 4f14 5d10 6p6
}

# Exceptions to aufbau (actual configurations) - using plain text format
ELECTRON_CONFIG_EXCEPTIONS = {
    24: {'expected': '[Ar] 4s2 3d4', 'actual': '[Ar] 4s1 3d5'},   # Cr
    29: {'expected': '[Ar] 4s2 3d9', 'actual': '[Ar] 4s1 3d10'},  # Cu
    41: {'expected': '[Kr] 5s2 4d3', 'actual': '[Kr] 5s1 4d4'},   # Nb
    42: {'expected': '[Kr] 5s2 4d4', 'actual': '[Kr] 5s1 4d5'},   # Mo
    44: {'expected': '[Kr] 5s2 4d6', 'actual': '[Kr] 5s1 4d7'},   # Ru
    45: {'expected': '[Kr] 5s2 4d7', 'actual': '[Kr] 5s1 4d8'},   # Rh
    46: {'expected': '[Kr] 5s2 4d8', 'actual': '[Kr] 5s0 4d10'},  # Pd
    47: {'expected': '[Kr] 5s2 4d9', 'actual': '[Kr] 5s1 4d10'},  # Ag
}


def electron_configuration(atomic_number, noble_gas_notation=True, use_exceptions=True, unicode_superscripts=False):
    """
    Generate electron configuration for element.
    
    Parameters:
        atomic_number: atomic number (number of electrons)
        noble_gas_notation: use noble gas core notation
        use_exceptions: use known exception configurations
        unicode_superscripts: use Unicode superscripts (123) instead of plain text (123)
    
    Returns:
        electron configuration string
    """
    def format_number(n):
        if unicode_superscripts:
            return superscript(n)
        return str(n)
    
    if use_exceptions and atomic_number in ELECTRON_CONFIG_EXCEPTIONS:
        return ELECTRON_CONFIG_EXCEPTIONS[atomic_number]['actual']
    
    remaining = atomic_number
    config = {}
    
    for subshell in AUFBAU_ORDER:
        if remaining <= 0:
            break
        
        subshell_type = subshell[-1]  # s, p, d, or f
        capacity = SUBSHELL_CAPACITY[subshell_type]
        
        electrons = min(capacity, remaining)
        config[subshell] = electrons
        remaining -= electrons
    
    # Format output
    if noble_gas_notation:
        # Find noble gas core
        noble_Z = max([z for z in NOBLE_GAS_CORES.keys() if z < atomic_number], default=0)
        
        if noble_Z > 0:
            # Filter out core subshells from config
            # Find which subshells are in the noble gas core
            noble_config = {}
            noble_remaining = noble_Z
            for subshell in AUFBAU_ORDER:
                if noble_remaining <= 0:
                    break
                subshell_type = subshell[-1]
                capacity = SUBSHELL_CAPACITY[subshell_type]
                electrons = min(capacity, noble_remaining)
                noble_config[subshell] = electrons
                noble_remaining -= electrons
            
            # Display only subshells beyond noble gas core
            parts = [f"[{NOBLE_GAS_CORES[noble_Z]}]"]
            for subshell in AUFBAU_ORDER:
                if subshell in config and subshell not in noble_config:
                    if config[subshell] > 0:
                        parts.append(f"{subshell}{format_number(config[subshell])}")
            return ' '.join(parts)
    
    # Full notation
    parts = []
    for subshell in AUFBAU_ORDER:
        if subshell in config and config[subshell] > 0:
            parts.append(f"{subshell}{format_number(config[subshell])}")
    return ' '.join(parts)


def superscript(n):
    """Convert number to superscript unicode."""
    superscripts = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
                   '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}
    return ''.join(superscripts.get(c, c) for c in str(n))


def valence_electrons(atomic_number):
    """
    Count valence electrons for main group element.
    
    Parameters:
        atomic_number: atomic number
    
    Returns:
        number of valence electrons
    """
    # Main group elements
    group = None
    
    if atomic_number <= 2:
        return atomic_number
    elif atomic_number <= 10:
        return atomic_number - 2
    elif atomic_number <= 18:
        return atomic_number - 10
    elif atomic_number <= 36:
        if atomic_number <= 20:
            return atomic_number - 18
        else:
            # Transition metals: count 4s and incomplete 3d
            return 2  # Simplified for transition metals
    elif atomic_number <= 54:
        if atomic_number <= 38:
            return atomic_number - 36
        else:
            return 2  # Simplified
    else:
        return 2  # Simplified


def is_exception(atomic_number):
    """Check if element has exception configuration."""
    return atomic_number in ELECTRON_CONFIG_EXCEPTIONS


def orbital_diagram_electrons(subshell, electrons):
    """
    Generate orbital diagram representation.
    
    Uses Hund's rule: maximize unpaired electrons.
    
    Parameters:
        subshell: subshell type ('s', 'p', 'd', 'f')
        electrons: number of electrons in subshell
    
    Returns:
        list of orbital occupancies (e.g., ['^v', '^', '^'] for p4)
    """
    num_orbitals = {'s': 1, 'p': 3, 'd': 5, 'f': 7}[subshell]
    orbitals = [''] * num_orbitals
    
    # Fill one electron per orbital first (Hund's rule)
    for i in range(min(electrons, num_orbitals)):
        orbitals[i] = '^'
    
    # Pair remaining electrons
    remaining = max(0, electrons - num_orbitals)
    for i in range(remaining):
        orbitals[i] = '^v'
    
    return orbitals


def parse_configuration(config_str):
    """
    Parse electron configuration string.
    
    Parameters:
        config_str: configuration string (e.g., "1s2 2s2 2p6")
    
    Returns:
        dict: {subshell: electrons}
    """
    import re
    config = {}
    
    # Remove noble gas core for now
    if config_str.startswith('['):
        config_str = config_str.split(']', 1)[1].strip()
    
    # Superscript to normal digit conversion
    superscript_to_num = {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
                          '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}
    
    # Match subshell patterns: digits + s/p/d/f + superscript or regular digits
    pattern = r'(\d+[spdf])([0123456789]+|\d+)'
    matches = re.findall(pattern, config_str)
    
    for subshell, count in matches:
        # Convert superscript to number
        if count[0] in superscript_to_num:
            # It's a superscript
            n = int(''.join(superscript_to_num.get(c, c) for c in count))
        else:
            n = int(count)
        config[subshell] = n
    
    return config


if __name__ == "__main__":
    print("Electron configuration tools - implemented")
    
    # Test configurations
    for Z in [1, 2, 10, 11, 18, 24, 26, 29, 36]:
        config = electron_configuration(Z)
        exception = " (exception)" if is_exception(Z) else ""
        print(f"Z={Z}: {config}{exception}")
    
    # Test valence electrons
    print(f"\nValence electrons: Na(11)={valence_electrons(11)}, Cl(17)={valence_electrons(17)}")
    
    # Test orbital diagram
    p4 = orbital_diagram_electrons('p', 4)
    print(f"\np4 orbital diagram: {p4}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "electron_configuration",
        "description": "Generate electron configuration for element.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "atomic_number": {"type": "number", "description": "Atomic Number"},
                "noble_gas_notation": {"type": "number", "description": "Noble Gas Notation", "default": True},
                "use_exceptions": {"type": "boolean", "description": "Use Exceptions", "default": True},
                "unicode_superscripts": {"type": "number", "description": "Unicode Superscripts", "default": False},
            },
            "required": ["atomic_number"]
        }
    },
    {
        "name": "is_exception",
        "description": "Check if element has exception configuration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "atomic_number": {"type": "number", "description": "Atomic Number"},
            },
            "required": ["atomic_number"]
        }
    },
    {
        "name": "orbital_diagram_electrons",
        "description": "Generate orbital diagram representation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subshell": {"type": "number", "description": "Subshell"},
                "electrons": {"type": "number", "description": "Electrons"},
            },
            "required": ["subshell", "electrons"]
        }
    },
    {
        "name": "parse_configuration",
        "description": "Parse electron configuration string.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "config_str": {"type": "string", "description": "Config Str"},
            },
            "required": ["config_str"]
        }
    },
    {
        "name": "superscript",
        "description": "Convert number to superscript unicode.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n": {"type": "number", "description": "N"},
            },
            "required": ["n"]
        }
    },
    {
        "name": "valence_electrons",
        "description": "Count valence electrons for main group element.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "atomic_number": {"type": "number", "description": "Atomic Number"},
            },
            "required": ["atomic_number"]
        }
    }
]
