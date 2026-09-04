"""
L3 Tool: Amino Acid Properties Tools
pI calculations, hydrophobicity, charge states, codon tables.

Source: Fundamentals of Biochemistry (Jakubowski and Flatt), Ch3
Created: 2026-03-13

## Solver Instructions (for AI Agent)

When you encounter amino acid problems - pI calculation, net charge at pH, hydrophobicity, codon lookup, or amino acid property lookup - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given an amino acid -> calculate its isoelectric point (pI)?
- Given an amino acid and pH -> calculate net charge?
- Given an amino acid -> hydrophobicity score on Kyte-Doolittle or Hopp-Woods scale?
- Given a codon -> which amino acid? Or given amino acid -> what codons?
- Given 1-letter or 3-letter code -> look up full amino acid properties?

### Step 2: Choose the correct function
- **Amino acid info:** `amino_acid_info(code)` -> accepts 1-letter or 3-letter code. Returns name, category, all pKa values, hydrophobicity scores
- **Isoelectric point:** `isoelectric_point(aa)` -> pI calculated from pKa values. Acidic (D,E): avg(COOH, side). Basic (K,R,H): avg(NH3, side). Neutral: avg(NH3, COOH)
- **Net charge at pH:** `net_charge(aa, pH)` -> uses Henderson-Hasselbalch for all ionizable groups. Returns breakdown: COOH, NH3, side charges
- **Hydrophobicity:** `hydrophobicity_score(aa, scale='KD')` -> KD: positive=hydrophobic (I=4.5 max). HW: positive=hydrophilic
- **Codon lookup:** `codon_table(aa=None)` -> codons for specific aa, or all codons grouped by aa. '*' = stop codon
- **Most hydrophobic:** `most_hydrophobic()` -> Isoleucine (KD=4.5)
- **Most hydrophilic:** `most_hydrophilic()` -> Arginine (KD=-4.5)

### Step 3: Handle special cases
- Acidic amino acids (D, E) have LOW pI (~2.98, ~3.22) - net negative at physiological pH
- Basic amino acids (K, R, H) have HIGH pI (~9.74, ~10.76, ~7.59) - net positive at physiological pH
- Histidine is special: pI ~ 7.59, so it can switch charge near physiological pH - important in enzyme active sites
- At pH = pI -> net charge = 0; below pI -> positive; above pI -> negative

### Examples
```python
# Example 1: pI of histidine
isoelectric_point('H')  -> {'pI': 7.59, 'method': 'basic'}  # avg of pKa_NH3(9.17) and pKa_side(6.0)

# Example 2: Net charge of lysine at pH 7.0
net_charge('K', 7.0)  -> {'charge': ~1, 'NH3': ~1, 'COOH': ~-1, 'side': ~1}

# Example 3: Hydrophobicity of isoleucine
hydrophobicity_score('I', 'KD')  -> {'score': 4.5, 'interpretation': 'strongly hydrophobic'}

# Example 4: Codons for methionine
codon_table('M')  -> {'M': ['ATG']}  # Only one codon (also start codon)
```
"""

import math

# Standard amino acid data with pKa values and hydrophobicity
AMINO_ACIDS = {
    'G': {'name': 'Glycine', 'three': 'Gly', 'category': 'nonpolar',
          'pKa_NH3': 9.60, 'pKa_COOH': 2.34, 'pKa_side': None, 'KD': -0.4, 'HW': 0.0},
    'A': {'name': 'Alanine', 'three': 'Ala', 'category': 'nonpolar',
          'pKa_NH3': 9.87, 'pKa_COOH': 2.34, 'pKa_side': None, 'KD': 1.8, 'HW': -0.5},
    'V': {'name': 'Valine', 'three': 'Val', 'category': 'nonpolar',
          'pKa_NH3': 9.74, 'pKa_COOH': 2.32, 'pKa_side': None, 'KD': 4.2, 'HW': -1.5},
    'L': {'name': 'Leucine', 'three': 'Leu', 'category': 'nonpolar',
          'pKa_NH3': 9.60, 'pKa_COOH': 2.36, 'pKa_side': None, 'KD': 3.8, 'HW': -1.8},
    'I': {'name': 'Isoleucine', 'three': 'Ile', 'category': 'nonpolar',
          'pKa_NH3': 9.68, 'pKa_COOH': 2.36, 'pKa_side': None, 'KD': 4.5, 'HW': -1.8},
    'M': {'name': 'Methionine', 'three': 'Met', 'category': 'nonpolar',
          'pKa_NH3': 9.21, 'pKa_COOH': 2.28, 'pKa_side': None, 'KD': 1.9, 'HW': -1.3},
    'F': {'name': 'Phenylalanine', 'three': 'Phe', 'category': 'aromatic',
          'pKa_NH3': 9.24, 'pKa_COOH': 2.58, 'pKa_side': None, 'KD': 2.8, 'HW': -2.5},
    'W': {'name': 'Tryptophan', 'three': 'Trp', 'category': 'aromatic',
          'pKa_NH3': 9.39, 'pKa_COOH': 2.38, 'pKa_side': None, 'KD': -0.9, 'HW': -3.4},
    'P': {'name': 'Proline', 'three': 'Pro', 'category': 'nonpolar',
          'pKa_NH3': 10.60, 'pKa_COOH': 1.99, 'pKa_side': None, 'KD': -1.6, 'HW': 0.0},
    'S': {'name': 'Serine', 'three': 'Ser', 'category': 'polar',
          'pKa_NH3': 9.15, 'pKa_COOH': 2.21, 'pKa_side': None, 'KD': -0.8, 'HW': 0.3},
    'T': {'name': 'Threonine', 'three': 'Thr', 'category': 'polar',
          'pKa_NH3': 9.10, 'pKa_COOH': 2.15, 'pKa_side': None, 'KD': -0.7, 'HW': -0.4},
    'C': {'name': 'Cysteine', 'three': 'Cys', 'category': 'polar',
          'pKa_NH3': 10.28, 'pKa_COOH': 1.96, 'pKa_side': 8.3, 'KD': 2.5, 'HW': -1.0},
    'N': {'name': 'Asparagine', 'three': 'Asn', 'category': 'polar',
          'pKa_NH3': 8.80, 'pKa_COOH': 2.02, 'pKa_side': None, 'KD': -3.5, 'HW': 0.2},
    'Q': {'name': 'Glutamine', 'three': 'Qln', 'category': 'polar',
          'pKa_NH3': 9.13, 'pKa_COOH': 2.17, 'pKa_side': None, 'KD': -3.5, 'HW': 0.2},
    'Y': {'name': 'Tyrosine', 'three': 'Tyr', 'category': 'aromatic',
          'pKa_NH3': 9.11, 'pKa_COOH': 2.20, 'pKa_side': 10.1, 'KD': -1.3, 'HW': -2.3},
    'D': {'name': 'Aspartic acid', 'three': 'Asp', 'category': 'acidic',
          'pKa_NH3': 9.82, 'pKa_COOH': 2.09, 'pKa_side': 3.86, 'KD': -3.5, 'HW': 3.0},
    'E': {'name': 'Glutamic acid', 'three': 'Glu', 'category': 'acidic',
          'pKa_NH3': 9.67, 'pKa_COOH': 2.19, 'pKa_side': 4.25, 'KD': -3.5, 'HW': 3.0},
    'K': {'name': 'Lysine', 'three': 'Lys', 'category': 'basic',
          'pKa_NH3': 8.95, 'pKa_COOH': 2.18, 'pKa_side': 10.53, 'KD': -3.9, 'HW': 3.0},
    'R': {'name': 'Arginine', 'three': 'Arg', 'category': 'basic',
          'pKa_NH3': 9.04, 'pKa_COOH': 2.17, 'pKa_side': 12.48, 'KD': -4.5, 'HW': 3.0},
    'H': {'name': 'Histidine', 'three': 'His', 'category': 'basic',
          'pKa_NH3': 9.17, 'pKa_COOH': 1.82, 'pKa_side': 6.0, 'KD': -3.2, 'HW': -0.5},
}

# Three-letter to one-letter mapping
THREE_TO_ONE = {v['three'].upper(): k for k, v in AMINO_ACIDS.items()}

# Standard genetic code
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}


def amino_acid_info(code: str) -> dict:
    """
    Get amino acid properties by code.
    
    Args:
        code: 1-letter or 3-letter code (case-insensitive)
    
    Returns:
        Dictionary with amino acid properties
    
    Example:
        >>> amino_acid_info('A')
        {'name': 'Alanine', 'three': 'Ala', 'category': 'nonpolar', ...}
    """
    code = code.upper()
    
    # Check if 3-letter code
    if len(code) == 3:
        if code in THREE_TO_ONE:
            code = THREE_TO_ONE[code]
        else:
            return {'error': f'Unknown 3-letter code: {code}'}
    
    if code not in AMINO_ACIDS:
        return {'error': f'Unknown amino acid: {code}'}
    
    data = AMINO_ACIDS[code].copy()
    data['one'] = code
    
    return data


def isoelectric_point(aa: str) -> dict:
    """
    Calculate isoelectric point for an amino acid.
    
    The pI is the pH at which the amino acid has zero net charge.
    
    For different categories:
    - Nonpolar/Polar (no ionizable side chain): pI = (pKa_NH3 + pKa_COOH) / 2
    - Acidic (D, E): pI = (pKa_COOH + pKa_side) / 2
    - Basic (K, R, H): pI = (pKa_NH3 + pKa_side) / 2
    
    Args:
        aa: Amino acid 1-letter code
    
    Returns:
        Dictionary with pI value
    
    Example:
        >>> isoelectric_point('H')
        {'pI': 7.59, 'method': 'basic'}
    """
    aa = aa.upper()
    if aa not in AMINO_ACIDS:
        return {'error': f'Unknown amino acid: {aa}'}
    
    data = AMINO_ACIDS[aa]
    category = data['category']
    
    if category == 'acidic':
        # pI is average of two lowest pKa values (COOH and side chain)
        pI = (data['pKa_COOH'] + data['pKa_side']) / 2
        method = 'acidic'
    elif category == 'basic':
        # pI is average of two highest pKa values (NH3 and side chain)
        pI = (data['pKa_NH3'] + data['pKa_side']) / 2
        method = 'basic'
    else:
        # Nonpolar/Polar: average of NH3 and COOH
        pI = (data['pKa_NH3'] + data['pKa_COOH']) / 2
        method = 'neutral'
    
    return {
        'pI': round(pI, 2),
        'method': method,
        'amino_acid': aa,
        'name': data['name']
    }


def net_charge(aa: str, pH: float) -> dict:
    """
    Calculate net charge of amino acid at given pH.
    
    Uses Henderson-Hasselbalch equation:
    fraction_protonated = 1 / (1 + 10^(pH - pKa))
    
    Args:
        aa: Amino acid 1-letter code
        pH: Solution pH
    
    Returns:
        Dictionary with net charge and breakdown
    
    Example:
        >>> net_charge('K', 7.0)
        {'charge': 1, 'COOH': -1, 'NH3': 1, 'side': 1}
    """
    aa = aa.upper()
    if aa not in AMINO_ACIDS:
        return {'error': f'Unknown amino acid: {aa}'}
    
    data = AMINO_ACIDS[aa]
    
    # Calculate charge for each group
    # COOH: neutral when protonated, -1 when deprotonated
    # NH3+: +1 when protonated, neutral when deprotonated
    # Side chain: depends on amino acid
    
    # Fraction protonated for COOH
    f_cooH = 1 / (1 + 10**(pH - data['pKa_COOH']))
    charge_coo = -1 * (1 - f_cooH)  # -1 if deprotonated
    
    # Fraction protonated for NH3+
    f_nh3 = 1 / (1 + 10**(pH - data['pKa_NH3']))
    charge_nh3 = f_nh3  # +1 if protonated
    
    # Side chain charge
    charge_side = 0
    if data['pKa_side']:
        if data['category'] == 'acidic':
            # Acidic side chain: neutral when protonated, -1 when deprotonated
            f_side = 1 / (1 + 10**(pH - data['pKa_side']))
            charge_side = -1 * (1 - f_side)
        elif data['category'] == 'basic':
            # Basic side chain: +1 when protonated, neutral when deprotonated
            f_side = 1 / (1 + 10**(pH - data['pKa_side']))
            charge_side = f_side
        elif aa == 'C':
            # Cysteine: -1 when deprotonated
            f_side = 1 / (1 + 10**(pH - data['pKa_side']))
            charge_side = -1 * (1 - f_side)
        elif aa == 'Y':
            # Tyrosine: -1 when deprotonated
            f_side = 1 / (1 + 10**(pH - data['pKa_side']))
            charge_side = -1 * (1 - f_side)
    
    net = round(charge_coo + charge_nh3 + charge_side, 2)
    
    return {
        'charge': net,
        'COOH': round(charge_coo, 2),
        'NH3': round(charge_nh3, 2),
        'side': round(charge_side, 2) if data['pKa_side'] else None,
        'pH': pH,
        'amino_acid': aa
    }


def hydrophobicity_score(aa: str, scale: str = 'KD') -> dict:
    """
    Get hydrophobicity value for amino acid.
    
    Kyte-Doolittle: positive = hydrophobic, negative = hydrophilic
    Hopp-Woods: positive = hydrophilic, negative = hydrophobic
    
    Args:
        aa: Amino acid 1-letter code
        scale: 'KD' (Kyte-Doolittle) or 'HW' (Hopp-Woods)
    
    Returns:
        Dictionary with hydrophobicity value and interpretation
    
    Example:
        >>> hydrophobicity_score('I', 'KD')
        {'score': 4.5, 'interpretation': 'strongly hydrophobic'}
    """
    aa = aa.upper()
    if aa not in AMINO_ACIDS:
        return {'error': f'Unknown amino acid: {aa}'}
    
    scale = scale.upper()
    if scale == 'KD':
        score = AMINO_ACIDS[aa]['KD']
        if score > 2:
            interp = 'strongly hydrophobic'
        elif score > 0:
            interp = 'moderately hydrophobic'
        elif score > -2:
            interp = 'neutral'
        elif score > -4:
            interp = 'moderately hydrophilic'
        else:
            interp = 'strongly hydrophilic'
    elif scale == 'HW':
        score = AMINO_ACIDS[aa]['HW']
        if score > 2:
            interp = 'strongly hydrophilic'
        elif score > 0:
            interp = 'moderately hydrophilic'
        elif score > -1:
            interp = 'neutral'
        else:
            interp = 'hydrophobic'
    else:
        return {'error': f'Unknown scale: {scale}. Use KD or HW.'}
    
    return {
        'score': score,
        'scale': scale,
        'interpretation': interp,
        'amino_acid': aa
    }


def codon_table(aa: str = None) -> dict:
    """
    Get codons for amino acid(s).
    
    Args:
        aa: Optional amino acid 1-letter code (returns all if None)
    
    Returns:
        Dictionary with codon(s)
    
    Example:
        >>> codon_table('M')
        {'M': ['ATG']}
        >>> codon_table()
        {'F': ['TTT', 'TTC'], 'L': ['TTA', 'TTG', ...], ...}
    """
    if aa:
        aa = aa.upper()
        if aa not in AMINO_ACIDS and aa != '*':
            return {'error': f'Unknown amino acid: {aa}'}
        
        codons = [c for c, a in CODON_TABLE.items() if a == aa]
        return {aa: codons}
    else:
        # Return all codons grouped by amino acid
        result = {}
        for codon, a in CODON_TABLE.items():
            if a not in result:
                result[a] = []
            result[a].append(codon)
        return result


def most_hydrophobic() -> dict:
    """
    Find the most hydrophobic amino acid by Kyte-Doolittle scale.
    
    Returns:
        Dictionary with amino acid and score
    """
    max_aa = max(AMINO_ACIDS.items(), key=lambda x: x[1]['KD'])
    return {
        'amino_acid': max_aa[0],
        'name': max_aa[1]['name'],
        'KD': max_aa[1]['KD']
    }


def most_hydrophilic() -> dict:
    """
    Find the most hydrophilic amino acid by Kyte-Doolittle scale.
    
    Returns:
        Dictionary with amino acid and score
    """
    min_aa = min(AMINO_ACIDS.items(), key=lambda x: x[1]['KD'])
    return {
        'amino_acid': min_aa[0],
        'name': min_aa[1]['name'],
        'KD': min_aa[1]['KD']
    }


# Problem set for testing
TEXTBOOK_PROBLEMS = [
    {
        "id": "AA-01",
        "question": "pI of histidine",
        "aa": "H",
        "expected_pI": 7.59
    },
    {
        "id": "AA-02",
        "question": "Net charge of lysine at pH 7",
        "aa": "K",
        "pH": 7.0,
        "expected_charge": 1
    },
    {
        "id": "AA-03",
        "question": "Most hydrophobic amino acid",
        "expected": "I"
    },
    {
        "id": "AA-04",
        "question": "Codons for methionine",
        "aa": "M",
        "expected_codons": ["ATG"]
    },
    {
        "id": "AA-05",
        "question": "pI of aspartic acid",
        "aa": "D",
        "expected_pI": 2.98
    },
]


if __name__ == "__main__":
    print("Amino Acid Properties Tools")
    print("=" * 40)
    
    # Test pI for all categories
    print("\nIsoelectric Points:")
    for aa in ['A', 'D', 'K', 'H']:
        result = isoelectric_point(aa)
        print(f"  {aa}: pI = {result['pI']} ({result['method']})")
    
    # Test charge
    print("\nNet Charge at pH 7:")
    for aa in ['D', 'E', 'K', 'R', 'H']:
        result = net_charge(aa, 7.0)
        print(f"  {aa}: {result['charge']}")
    
    # Test hydrophobicity
    print("\nMost hydrophobic/hydrophilic:")
    print(f"  Hydrophobic: {most_hydrophobic()}")
    print(f"  Hydrophilic: {most_hydrophilic()}")


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "amino_acid_info",
        "description": "Get amino acid properties by code.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "number",
                    "description": "Code"
                }
            },
            "required": [
                "code"
            ]
        }
    },
    {
        "name": "codon_table",
        "description": "Get codons for amino acid(s).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "aa": {
                    "type": "number",
                    "description": "Aa",
                    "default": None
                }
            },
            "required": []
        }
    },
    {
        "name": "hydrophobicity_score",
        "description": "Get hydrophobicity value for amino acid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "aa": {
                    "type": "number",
                    "description": "Aa"
                },
                "scale": {
                    "type": "number",
                    "description": "Scale",
                    "default": "KD"
                }
            },
            "required": [
                "aa"
            ]
        }
    },
    {
        "name": "isoelectric_point",
        "description": "Calculate isoelectric point for an amino acid.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "aa": {
                    "type": "number",
                    "description": "Aa"
                }
            },
            "required": [
                "aa"
            ]
        }
    },
    {
        "name": "most_hydrophilic",
        "description": "Find the most hydrophilic amino acid by Kyte-Doolittle scale.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "most_hydrophobic",
        "description": "Find the most hydrophobic amino acid by Kyte-Doolittle scale.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "net_charge",
        "description": "Calculate net charge of amino acid at given pH.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "aa": {
                    "type": "number",
                    "description": "Aa"
                },
                "pH": {
                    "type": "number",
                    "description": "Ph"
                }
            },
            "required": [
                "aa",
                "pH"
            ]
        }
    }
]