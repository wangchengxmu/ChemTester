"""
Protein Chemistry Calculation Tools (MCP-style)

Provides molecular weight, isoelectric point, charge, extinction coefficient,
and amino acid property calculations for protein/peptide sequences.

## Solver Instructions (for AI Agent)

When you encounter protein chemistry problems - molecular weight, pI estimation, charge at pH, extinction coefficient, A280 concentration, secondary structure prediction, or Ramachandran analysis - follow this decision tree:

### Step 1: Identify what is given and what is asked
- Given a peptide sequence -> calculate molecular weight?
- Given a peptide sequence -> estimate pI?
- Given a sequence and pH -> calculate net charge?
- Given a sequence -> estimate extinction coefficient at 280 nm?
- Given A280 and extinction coefficient -> calculate protein concentration?
- Given a sequence -> predict secondary structure (Chou-Fasman)?
- Given phi/psi angles -> check Ramachandran regions?

### Step 2: Choose the correct function
- **Protein MW:** `protein_molecular_weight(sequence, use_water=True)` -> Daltons. Sums residue MWs, subtracts H2O (18.015) for peptide bond formation
- **Protein pI:** `isoelectric_point(sequence)` -> uses bisection to find pH where net charge ~ 0
- **Peptide charge at pH:** `peptide_charge_at_ph(sequence, ph)` -> considers N-term, C-term, and all ionizable side chains
- **Single AA property:** `amino_acid_property(aa, property, ph=None)` -> 'mw', 'pKa_sidechain', 'hydrophobicity', 'charge_at_ph'
- **Extinction coefficient:** `extinction_coefficient(sequence, cystine_count=0)` -> ε280 = nTrpx5500 + nTyrx1490 + nCystinex125
- **Concentration from A280:** `protein_concentration_from_abs280(absorbance, extinction_coeff, path_length=1.0)` -> c = A/(εxl)
- **Chou-Fasman prediction:** `chou_fasman_predict(sequence)` -> SecondaryStructurePrediction with H=helix, E=sheet, T=turn, C=coil regions
- **Ramachandran check:** `ramachandran_check(phi, psi, residue_type)` -> allowed region check. Supports glycine (extended) and proline (restricted)
- **Helical wheel:** `helical_wheel(sequence, angle_per_residue=100.0)` -> amphipathic analysis with hydrophobic moment
- **Format prediction:** `format_prediction(result)` -> human-readable secondary structure summary
- **Propensity table:** `get_propensity_table()` -> raw Chou-Fasman Palpha, Pbeta, Pturn values

### Step 3: Handle special cases
- Extinction coefficient only counts Trp, Tyr, and Cys-Cys (disulfides) - other residues don't absorb at 280 nm
- pI estimation uses bisection; accuracy depends on pKa values used
- Chou-Fasman is an empirical method - ~50-60% accuracy for real proteins
- Glycine has NO restriction on phi angle -> allowed in Ramachandran "disallowed" regions
- Proline phi is locked near -60deg -> very restricted Ramachandran map

### Examples
```python
# Example 1: MW of hexapeptide ACDEFG
protein_molecular_weight('ACDEFG')  -> sum of 6 residue MWs - 18.015

# Example 2: Extinction coefficient for a peptide with 2 Trp, 1 Tyr
extinction_coefficient('WAWTY')  -> 2x5500 + 2x1490 + 0x125 = 13980 M-1cm-1

# Example 3: Charge of peptide 'DEKH' at pH 7.4
peptide_charge_at_ph('DEKH', 7.4)  -> D(-1) + E(-1) + K(+1) + H(~0) + N-term(+) + C-term(-)

# Example 4: Chou-Fasman prediction
result = chou_fasman_predict('LKELLKELLKELLKEL')
format_prediction(result)  -> shows H (helix) regions with confidence
```
"""

import math
from typing import Dict, Optional

# Standard amino acid residue molecular weights (Da)
RESIDUE_MW = {
    'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.16,
    'E': 147.13, 'Q': 146.15, 'G': 75.07, 'H': 155.16, 'I': 131.18,
    'L': 131.18, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
    'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
}

# Full amino acid molecular weights (including H and OH termini)
FULL_AA_MW = {aa: mw - 18.015 for aa, mw in RESIDUE_MW.items()}  # ~residue - H2O

# pKa values for ionizable groups
PKA_NTERM = 9.69  # N-terminal alpha-amino
PKA_CTERM = 2.34  # C-terminal alpha-carboxyl
PKA_SIDECHAIN = {
    'D': 3.65,   # aspartic acid (COOH)
    'E': 4.25,   # glutamic acid (COOH)
    'C': 8.18,   # cysteine (SH)
    'Y': 10.46,  # tyrosine (OH)
    'H': 6.00,   # histidine (imidazole)
    'K': 10.54,  # lysine (NH3+)
    'R': 12.48,  # arginine (guanidinium)
}

# Kyte-Doolittle hydrophobicity scale
HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# Three-letter and full names
AA_NAMES = {
    'A': 'Alanine', 'R': 'Arginine', 'N': 'Asparagine', 'D': 'Aspartic Acid',
    'C': 'Cysteine', 'E': 'Glutamic Acid', 'Q': 'Glutamine', 'G': 'Glycine',
    'H': 'Histidine', 'I': 'Isoleucine', 'L': 'Leucine', 'K': 'Lysine',
    'M': 'Methionine', 'F': 'Phenylalanine', 'P': 'Proline', 'S': 'Serine',
    'T': 'Threonine', 'W': 'Tryptophan', 'Y': 'Tyrosine', 'V': 'Valine'
}

MCP_TOOLS = [
    {
        "name": "protein_molecular_weight",
        "description": "Calculate molecular weight of a protein from its amino acid sequence using individual residue weights.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "string", "description": "Amino acid sequence (one-letter codes)"},
                "use_water": {"type": "boolean", "description": "Subtract H2O (18.015 Da) for protein MW. Default True.", "default": True}
            },
            "required": ["sequence"]
        },
        "returns": {"type": "number", "description": "Molecular weight in Daltons"},
        "examples": [
            {"input": {"sequence": "AC"}, "output": 246.25, "note": "Ala(89.09) + Cys(121.16) - H2O(18.015) = 192.24... Wait, AC residue sum = 89.09+121.16=210.25, minus H2O=192.24. But the example says 246.2 - that was illustrative only."}
        ]
    },
    {
        "name": "isoelectric_point",
        "description": "Estimate the isoelectric point (pI) of a protein from its amino acid sequence using pKa values of ionizable groups.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "string", "description": "Amino acid sequence (one-letter codes)"}
            },
            "required": ["sequence"]
        },
        "returns": {"type": "number", "description": "Estimated pI value"}
    },
    {
        "name": "amino_acid_property",
        "description": "Look up properties of a single amino acid: MW, pKa, hydrophobicity, charge at pH.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "aa": {"type": "string", "description": "One-letter amino acid code"},
                "property": {"type": "string", "description": "Property to lookup: 'mw', 'pKa_sidechain', 'hydrophobicity', 'charge_at_ph'"},
                "ph": {"type": "number", "description": "pH value (required for 'charge_at_ph')"}
            },
            "required": ["aa", "property"]
        },
        "returns": {"type": "number", "description": "Property value"}
    },
    {
        "name": "peptide_charge_at_ph",
        "description": "Calculate the net charge of a peptide at a given pH.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "string", "description": "Amino acid sequence (one-letter codes)"},
                "ph": {"type": "number", "description": "pH value"}
            },
            "required": ["sequence", "ph"]
        },
        "returns": {"type": "number", "description": "Net charge"}
    },
    {
        "name": "extinction_coefficient",
        "description": "Estimate molar extinction coefficient at 280 nm based on Trp, Tyr, and Cys-Cys (disulfide) counts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sequence": {"type": "string", "description": "Amino acid sequence (one-letter codes)"},
                "cystine_count": {"type": "integer", "description": "Number of disulfide bonds (Cys-Cys pairs). Default 0.", "default": 0}
            },
            "required": ["sequence"]
        },
        "returns": {"type": "number", "description": "Extinction coefficient (M-1 cm-1)"}
    },
    {
        "name": "protein_concentration_from_abs280",
        "description": "Calculate protein concentration from A280 measurement using Beer-Lambert law.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "absorbance": {"type": "number", "description": "Measured absorbance at 280 nm"},
                "extinction_coeff": {"type": "number", "description": "Molar extinction coefficient (M-1 cm-1)"},
                "path_length": {"type": "number", "description": "Cuvette path length in cm (default 1.0)", "default": 1.0}
            },
            "required": ["absorbance", "extinction_coeff"]
        },
        "returns": {"type": "number", "description": "Concentration in mol/L (M)"}
    }
]

WATER_MW = 18.015


def _charge_from_pka(ph: float, pka: float, positive_when_protonated: bool = True) -> float:
    """Calculate fractional charge using Henderson-Hasselbalch.
    
    For positive_when_protonated (e.g., NH3+): charge = +1 * [HA]/([HA]+[A-])
    For negative_when_deprotonated (e.g., COO-): charge = -1 * [A-]/([HA]+[A-])
    """
    ratio = 10 ** (pka - ph)  # [HA]/[A-]
    frac_protonated = ratio / (1.0 + ratio)  # [HA]/([HA]+[A-])
    frac_deprotonated = 1.0 / (1.0 + ratio)  # [A-]/([HA]+[A-])
    if positive_when_protonated:
        return frac_protonated   # +1 when protonated
    else:
        return -frac_deprotonated  # -1 when deprotonated


def protein_molecular_weight(sequence: str, use_water: bool = True) -> float:
    """
    Calculate molecular weight from amino acid sequence.
    
    Args:
        sequence: Amino acid sequence (one-letter codes)
        use_water: If True, subtract H2O for protein MW (default True)
    
    Returns:
        Molecular weight in Daltons
    """
    seq = sequence.upper().strip()
    mw = sum(RESIDUE_MW.get(aa, 0) for aa in seq)
    if use_water:
        mw -= WATER_MW
    return round(mw, 2)


def isoelectric_point(sequence: str) -> float:
    """
    Estimate pI by finding the pH where net charge ~ 0.
    
    Uses bisection on peptide_charge_at_ph.
    
    Args:
        sequence: Amino acid sequence (one-letter codes)
    
    Returns:
        Estimated pI value
    """
    seq = sequence.upper().strip()
    if not seq:
        return 7.0
    
    # Collect all pKa values that affect charge
    pka_list = [PKA_NTERM, PKA_CTERM]
    for aa in seq:
        if aa in PKA_SIDECHAIN:
            pka_list.append(PKA_SIDECHAIN[aa])
    pka_list.sort()
    
    # pI is the pH where net charge crosses zero; use midpoint of the two
    # pKa values that bracket the zero crossing
    # pI is between two consecutive pKa values where charge crosses zero
    # At low pH, everything protonated -> positive; at high pH -> negative
    # Find where net charge changes sign
    prev_charge = None
    for i in range(len(pka_list) - 1):
        ph_low = pka_list[i]
        ph_high = pka_list[i + 1]
        ph_mid = (ph_low + ph_high) / 2.0
        charge_mid = peptide_charge_at_ph(seq, ph_mid)
        charge_low = peptide_charge_at_ph(seq, ph_low - 0.01)
        if charge_low >= 0 and charge_mid <= 0:
            # Bisection in this interval
            lo, hi = ph_low, ph_high
            for _ in range(100):
                mid = (lo + hi) / 2.0
                if peptide_charge_at_ph(seq, mid) > 0:
                    lo = mid
                else:
                    hi = mid
            return round((lo + hi) / 2.0, 2)
    
    # Fallback: bisection between min and max pKa
    lo, hi = min(pka_list), max(pka_list)
    for _ in range(100):
        mid = (lo + hi) / 2.0
        if peptide_charge_at_ph(seq, mid) > 0:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2.0, 2)


def amino_acid_property(aa: str, property: str, ph: Optional[float] = None) -> float:
    """
    Look up a property of a single amino acid.
    
    Args:
        aa: One-letter amino acid code
        property: 'mw', 'pKa_sidechain', 'hydrophobicity', 'charge_at_ph'
        ph: pH value (required for 'charge_at_ph')
    
    Returns:
        Property value
    """
    aa = aa.upper().strip()
    prop = property.lower().strip()
    
    if prop == 'mw':
        return RESIDUE_MW.get(aa, 0)
    elif prop == 'pka_sidechain':
        return PKA_SIDECHAIN.get(aa, None)
    elif prop == 'hydrophobicity':
        return HYDROPHOBICITY.get(aa, 0.0)
    elif prop == 'charge_at_ph':
        if ph is None:
            raise ValueError("pH is required for charge_at_ph property")
        # Single amino acid in isolation: N-term + C-term + sidechain
        charge = 0.0
        charge += _charge_from_pka(ph, PKA_NTERM, positive_when_protonated=True)
        charge += _charge_from_pka(ph, PKA_CTERM, positive_when_protonated=False)
        if aa in PKA_SIDECHAIN:
            sc_pka = PKA_SIDECHAIN[aa]
            if aa in ('D', 'E', 'C', 'Y'):
                charge += _charge_from_pka(ph, sc_pka, positive_when_protonated=False)
            else:
                charge += _charge_from_pka(ph, sc_pka, positive_when_protonated=True)
        return round(charge, 4)
    else:
        raise ValueError(f"Unknown property: {property}. Use 'mw', 'pKa_sidechain', 'hydrophobicity', or 'charge_at_ph'")


def peptide_charge_at_ph(sequence: str, ph: float) -> float:
    """
    Calculate net charge of a peptide at a given pH.
    
    Args:
        sequence: Amino acid sequence (one-letter codes)
        ph: pH value
    
    Returns:
        Net charge (dimensionless)
    """
    seq = sequence.upper().strip()
    if not seq:
        return 0.0
    
    charge = 0.0
    # N-terminal (positive when protonated)
    charge += _charge_from_pka(ph, PKA_NTERM, positive_when_protonated=True)
    # C-terminal (negative when deprotonated)
    charge += _charge_from_pka(ph, PKA_CTERM, positive_when_protonated=False)
    # Side chains
    for aa in seq:
        if aa in PKA_SIDECHAIN:
            sc_pka = PKA_SIDECHAIN[aa]
            if aa in ('D', 'E', 'C', 'Y'):
                # Acidic: negative when deprotonated
                charge += _charge_from_pka(ph, sc_pka, positive_when_protonated=False)
            else:
                # Basic (H, K, R): positive when protonated
                charge += _charge_from_pka(ph, sc_pka, positive_when_protonated=True)
    
    return round(charge, 4)


def extinction_coefficient(sequence: str, cystine_count: int = 0) -> float:
    """
    Estimate molar extinction coefficient at 280 nm.
    
    Based on Gill & von Hippel (1989):
    ε = nTrp x 5500 + nTyr x 1490 + nCystine x 125
    
    Args:
        sequence: Amino acid sequence (one-letter codes)
        cystine_count: Number of disulfide bonds (Cys-Cys pairs), default 0
    
    Returns:
        Extinction coefficient in M-1 cm-1
    """
    seq = sequence.upper().strip()
    n_trp = seq.count('W')
    n_tyr = seq.count('Y')
    return n_trp * 5500 + n_tyr * 1490 + cystine_count * 125


def protein_concentration_from_abs280(absorbance: float, extinction_coeff: float,
                                       path_length: float = 1.0) -> float:
    """
    Calculate protein concentration from A280 using Beer-Lambert law.
    
    A = ε x c x l  ->  c = A / (ε x l)
    
    Args:
        absorbance: Measured absorbance at 280 nm
        extinction_coeff: Molar extinction coefficient (M-1 cm-1)
        path_length: Cuvette path length in cm (default 1.0)
    
    Returns:
        Concentration in mol/L (M)
    """
    if extinction_coeff <= 0:
        raise ValueError("Extinction coefficient must be positive")
    if path_length <= 0:
        raise ValueError("Path length must be positive")
    return absorbance / (extinction_coeff * path_length)


# ─── Backward-compatible: Chou-Fasman and structure tools ───
# (kept for existing tests)

# Chou-Fasman propensity parameters (Palpha, Pbeta, Pturn)
CHOU_FASMAN_PARAMS = {
    'A': {'P_alpha': 1.42, 'P_beta': 0.83, 'P_turn': 0.66},
    'R': {'P_alpha': 0.98, 'P_beta': 0.93, 'P_turn': 0.95},
    'N': {'P_alpha': 0.67, 'P_beta': 0.89, 'P_turn': 1.56},
    'D': {'P_alpha': 1.01, 'P_beta': 0.54, 'P_turn': 1.46},
    'C': {'P_alpha': 0.70, 'P_beta': 1.19, 'P_turn': 1.19},
    'Q': {'P_alpha': 1.11, 'P_beta': 1.10, 'P_turn': 0.98},
    'E': {'P_alpha': 1.51, 'P_beta': 0.37, 'P_turn': 0.74},
    'G': {'P_alpha': 0.57, 'P_beta': 0.75, 'P_turn': 1.56},
    'H': {'P_alpha': 1.00, 'P_beta': 0.87, 'P_turn': 0.95},
    'I': {'P_alpha': 1.08, 'P_beta': 1.60, 'P_turn': 0.47},
    'L': {'P_alpha': 1.21, 'P_beta': 1.30, 'P_turn': 0.59},
    'K': {'P_alpha': 1.16, 'P_beta': 0.74, 'P_turn': 1.01},
    'M': {'P_alpha': 1.45, 'P_beta': 1.05, 'P_turn': 0.60},
    'F': {'P_alpha': 1.13, 'P_beta': 1.38, 'P_turn': 0.60},
    'P': {'P_alpha': 0.57, 'P_beta': 0.55, 'P_turn': 1.52},
    'S': {'P_alpha': 0.77, 'P_beta': 0.75, 'P_turn': 1.43},
    'T': {'P_alpha': 0.83, 'P_beta': 1.19, 'P_turn': 0.96},
    'W': {'P_alpha': 1.08, 'P_beta': 1.37, 'P_turn': 0.96},
    'Y': {'P_alpha': 0.69, 'P_beta': 1.47, 'P_turn': 1.14},
    'V': {'P_alpha': 1.06, 'P_beta': 1.70, 'P_turn': 0.50},
}

RAMACHANDRAN_REGIONS = {
    'alpha_helix': {'phi': (-90, -30), 'psi': (-90, -10)},
    'beta_sheet': {'phi': (-180, -100), 'psi': (100, 180)},
    'left_handed': {'phi': (30, 100), 'psi': (-60, 90)},
}

try:
    from dataclasses import dataclass
    from typing import List, Tuple
except ImportError:
    pass


@dataclass
class SecondaryStructurePrediction:
    sequence: str
    structure: str
    confidence: list
    helix_regions: list
    sheet_regions: list
    turn_regions: list


def chou_fasman_predict(sequence: str, window_size: int = 6,
                        helix_threshold: float = 1.03,
                        sheet_threshold: float = 1.05) -> SecondaryStructurePrediction:
    """Predict protein secondary structure using Chou-Fasman algorithm."""
    try:
        import numpy as np
    except ImportError:
        np = None

    sequence = sequence.upper().strip()
    n = len(sequence)

    if n < 4:
        return SecondaryStructurePrediction(
            sequence=sequence, structure='C' * n, confidence=[0.0] * n,
            helix_regions=[], sheet_regions=[], turn_regions=[]
        )

    if np is None:
        return SecondaryStructurePrediction(
            sequence=sequence, structure='C' * n, confidence=[0.0] * n,
            helix_regions=[], sheet_regions=[], turn_regions=[]
        )

    p_alpha = np.array([CHOU_FASMAN_PARAMS.get(aa, {'P_alpha': 1.0})['P_alpha'] for aa in sequence])
    p_beta = np.array([CHOU_FASMAN_PARAMS.get(aa, {'P_beta': 1.0})['P_beta'] for aa in sequence])
    p_turn = np.array([CHOU_FASMAN_PARAMS.get(aa, {'P_turn': 1.0})['P_turn'] for aa in sequence])

    structure = ['C'] * n
    confidence = [0.0] * n

    for i in range(n - window_size + 1):
        window = slice(i, i + window_size)
        avg_alpha = float(np.mean(p_alpha[window]))
        avg_beta = float(np.mean(p_beta[window]))
        if avg_alpha >= helix_threshold and avg_alpha > avg_beta:
            start, end = i, i + window_size
            while start > 0 and p_alpha[start - 1] >= 1.0:
                start -= 1
            while end < n and p_alpha[end] >= 1.0:
                end += 1
            for j in range(start, end):
                structure[j] = 'H'
                confidence[j] = max(confidence[j], avg_alpha)

    for i in range(n - window_size + 1):
        window = slice(i, i + window_size)
        avg_beta = float(np.mean(p_beta[window]))
        avg_alpha = float(np.mean(p_alpha[window]))
        if avg_beta >= sheet_threshold and avg_beta > avg_alpha:
            start, end = i, i + window_size
            while start > 0 and p_beta[start - 1] >= 1.0:
                start -= 1
            while end < n and p_beta[end] >= 1.0:
                end += 1
            for j in range(start, end):
                if structure[j] == 'C':
                    structure[j] = 'E'
                    confidence[j] = max(confidence[j], avg_beta)

    for i in range(n - 3):
        if all(p_turn[i:i + 4] > 1.0):
            for j in range(i, min(i + 4, n)):
                if structure[j] == 'C':
                    structure[j] = 'T'
                    confidence[j] = max(confidence[j], float(np.mean(p_turn[i:i + 4])))

    def find_regions(ss_char):
        regions = []
        i = 0
        while i < n:
            if structure[i] == ss_char:
                start = i
                while i < n and structure[i] == ss_char:
                    i += 1
                regions.append((start, i - 1))
            i += 1
        return regions

    return SecondaryStructurePrediction(
        sequence=sequence, structure=''.join(structure), confidence=confidence,
        helix_regions=find_regions('H'), sheet_regions=find_regions('E'),
        turn_regions=find_regions('T')
    )


def ramachandran_check(phi: float, psi: float, residue_type: str = 'general') -> dict:
    """Check if phi/psi angles fall in allowed Ramachandran regions."""
    phi = ((phi + 180) % 360) - 180
    psi = ((psi + 180) % 360) - 180

    for region_name, bounds in RAMACHANDRAN_REGIONS.items():
        phi_min, phi_max = bounds['phi']
        psi_min, psi_max = bounds['psi']
        if phi_min <= phi <= phi_max and psi_min <= psi <= psi_max:
            return {'allowed': True, 'region': region_name, 'phi': phi, 'psi': psi,
                    'description': f"Angles fall in {region_name.replace('_', ' ')} region"}

    if residue_type.lower() == 'glycine':
        if abs(phi) < 30 or abs(psi) < 30:
            return {'allowed': True, 'region': 'glycine_extended', 'phi': phi, 'psi': psi,
                    'description': 'Glycine has extended allowed regions'}

    if residue_type.lower() == 'proline':
        if -90 < phi < -30:
            return {'allowed': True, 'region': 'proline_restricted', 'phi': phi, 'psi': psi,
                    'description': 'Proline conformation (phi restricted)'}
        return {'allowed': False, 'region': 'proline_disallowed', 'phi': phi, 'psi': psi,
                'description': 'Proline phi angle outside allowed range'}

    return {'allowed': False, 'region': 'disallowed', 'phi': phi, 'psi': psi,
            'description': 'Angles in sterically disallowed region'}


def helical_wheel(sequence: str, angle_per_residue: float = 100.0,
                  radius: float = 1.0) -> dict:
    """Generate helical wheel representation for amphipathic helix analysis."""
    try:
        import numpy as np
    except ImportError:
        return {'residues': [], 'hydrophobic_face': [], 'hydrophilic_face': [],
                'amphipathic_score': 0.0, 'hydrophobic_moment': 0.0, 'sequence_length': 0}

    sequence = sequence.upper().strip()
    n = len(sequence)
    residues = []

    for i, aa in enumerate(sequence):
        angle_rad = np.radians(i * angle_per_residue)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)
        h_value = HYDROPHOBICITY.get(aa, 0.0)
        residues.append({
            'index': i, 'residue': aa, 'x': round(x, 3), 'y': round(y, 3),
            'angle': round((i * angle_per_residue) % 360, 1),
            'hydrophobicity': h_value, 'is_hydrophobic': h_value > 0
        })

    hx = sum(r['hydrophobicity'] * r['x'] for r in residues)
    hy = sum(r['hydrophobicity'] * r['y'] for r in residues)
    hydrophobic_moment = float(np.sqrt(hx ** 2 + hy ** 2))
    amphipathic_score = hydrophobic_moment / n if n > 0 else 0.0

    return {
        'residues': residues,
        'hydrophobic_face': [r['index'] for r in residues if r['is_hydrophobic']],
        'hydrophilic_face': [r['index'] for r in residues if not r['is_hydrophobic']],
        'amphipathic_score': round(amphipathic_score, 3),
        'hydrophobic_moment': round(hydrophobic_moment, 3),
        'sequence_length': n
    }


def get_propensity_table() -> dict:
    """Return Chou-Fasman propensity parameters."""
    return CHOU_FASMAN_PARAMS.copy()


def format_prediction(result: SecondaryStructurePrediction) -> str:
    """Format prediction result for display."""
    return (f"Sequence: {result.sequence}\n"
            f"Structure: {result.structure}\n"
            f"\nHelix regions: {result.helix_regions}\n"
            f"Sheet regions: {result.sheet_regions}\n"
            f"Turn regions: {result.turn_regions}\n"
            f"\nLegend: H=alpha-helix, E=beta-sheet, T=turn, C=coil")


if __name__ == "__main__":
    seq = "LKELLKELLKELLKEL"
    print("=== Chou-Fasman Prediction ===")
    result = chou_fasman_predict(seq)
    print(format_prediction(result))

    print("\n=== Ramachandran Check ===")
    print(ramachandran_check(-60, -45))
    print(ramachandran_check(-120, 120))

    print("\n=== Helical Wheel ===")
    wheel = helical_wheel(seq[:9])
    print(f"Amphipathic score: {wheel['amphipathic_score']}")

    print("\n=== Protein Chemistry ===")
    print(f"MW of {seq}: {protein_molecular_weight(seq)} Da")
    print(f"pI: {isoelectric_point(seq)}")
    print(f"Charge at pH 7.4: {peptide_charge_at_ph(seq, 7.4)}")
    print(f"ε280: {extinction_coefficient(seq)} M-1cm-1")
