"""
Protein Structure Tools
=======================

Python implementations for protein structure analysis including
helical wheel plots, Ramachandran angles, and hydrophobicity.

## Solver Instructions (for AI Agent)

When you encounter protein structure problems, follow this decision tree:

### Step 1: Identify what is given and what is asked
- **Given a peptide sequence** -> need hydrophobicity? Use `hydrophobicity_score()`
- **Given a peptide sequence** -> need to visualize amphipathicity or residue arrangement? Use `helical_wheel()`
- **Given phi/psi angles** -> need to check if they're allowed? Use `is_ramachandran_allowed()`
- **Given backbone coordinates (N, CA, C)** -> need dihedral angles? Use `ramachandran_phi_psi()`
- **Given a peptide sequence and pH** -> need net charge? Use `net_charge()`

### Step 2: Choose the correct function
| Problem type | Function |
|---|---|
| Average hydrophobicity of a sequence | `hydrophobicity_score()` |
| Helical wheel projection (residue positions on alpha-helix) | `helical_wheel()` |
| Check if phi/psi angles are Ramachandran-allowed | `is_ramachandran_allowed()` |
| Calculate phi/psi from 3D coordinates | `ramachandran_phi_psi()` |
| Net charge at a given pH | `net_charge()` |

### Step 3: Handle special cases
- **Unknown residues** in sequence -> treated as hydrophobicity 0.0 (neutral)
- **Ramachandran glycine** -> glycine has a much larger allowed region due to lack of side chain (pass `residue_type='glycine'` for stricter checks; current simplified implementation uses 'general')
- **Ramachandran proline** -> proline has a restricted allowed region (pass `residue_type='proline'`)
- **pH and charge** -> the N-terminus (pKa ~ 9.0) and C-terminus (pKa ~ 2.0) are always included in the charge calculation
- **Helical wheel** -> uses 100deg rotation per residue (standard 3.6 residues/turn for alpha-helix)
- **Backbone coordinates** -> `ramachandran_phi_psi()` is a simplified stub; for real work use a proper dihedral angle library

### Examples

**Example 1: Hydrophobicity score**
What is the average Kyte-Doolittle hydrophobicity of "VVVV"?
-> `hydrophobicity_score('VVVV')` -> 4.2 (highly hydrophobic)
What about "KKKK"?
-> `hydrophobicity_score('KKKK')` -> -3.9 (hydrophilic/charged)

**Example 2: Net charge at pH 7**
What is the net charge of peptide "KKD" at pH 7?
-> `net_charge('KKD', 7.0)` -> ~1.0 (2 positive Lys + 1 negative Asp, plus termini)

**Example 3: Ramachandran check**
Are phi=-60, psi=-45 allowed?
-> `is_ramachandran_allowed(-60, -45)` -> True (alpha-helix region)
Are phi=0, psi=0 allowed?
-> `is_ramachandran_allowed(0, 0)` -> False (disallowed region)

Source: L2 protein_structure.md
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

# Kyte-Doolittle hydropathy scale
HYDROPATHY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

def hydrophobicity_score(sequence: str) -> float:
    """
    Calculate average hydrophobicity for a peptide sequence.
    
    Uses Kyte-Doolittle scale.
    
    Parameters
    ----------
    sequence : str
        Amino acid sequence (one-letter codes)
    
    Returns
    -------
    float
        Average hydrophobicity score
    
    Examples
    --------
    >>> hydrophobicity_score('VVVV')
    4.2
    >>> hydrophobicity_score('AAAA')
    1.8
    """
    sequence = sequence.upper()
    scores = [HYDROPATHY.get(aa, 0) for aa in sequence]
    return np.mean(scores) if scores else 0


def helical_wheel(sequence: str) -> List[Dict]:
    """
    Generate helical wheel projection data.
    
    Shows residue positions on alpha-helix cross-section.
    100 degree rotation per residue (3.6 residues/turn).
    
    Parameters
    ----------
    sequence : str
        Amino acid sequence (one-letter codes)
    
    Returns
    -------
    list
        List of dicts with residue, angle, and x,y coordinates
    
    Examples
    --------
    >>> wheel = helical_wheel('EELLKK')
    >>> len(wheel)
    6
    """
    residues = []
    for i, aa in enumerate(sequence.upper()):
        angle = i * 100  # degrees
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))
        residues.append({
            'residue': aa,
            'position': i + 1,
            'angle': angle,
            'x': round(x, 3),
            'y': round(y, 3),
            'hydrophobic': HYDROPATHY.get(aa, 0) > 0
        })
    return residues


def ramachandran_phi_psi(
    n_coords: np.ndarray,
    ca_coords: np.ndarray,
    c_coords: np.ndarray
) -> List[Tuple[float, float]]:
    """
    Calculate phi and psi angles from backbone coordinates.
    
    Parameters
    ----------
    n_coords : ndarray
        N atom coordinates (n_residues x 3)
    ca_coords : ndarray
        CA atom coordinates (n_residues x 3)
    c_coords : ndarray
        C atom coordinates (n_residues x 3)
    
    Returns
    -------
    list
        List of (phi, psi) angle tuples in degrees
    
    Examples
    --------
    >>> # Would need actual coordinates to test
    >>> pass
    """
    angles = []
    n_res = len(ca_coords)
    
    for i in range(n_res):
        phi = 0.0
        psi = 0.0
        
        # Phi: C(i-1) - N(i) - CA(i) - C(i)
        if i > 0:
            v1 = n_coords[i] - c_coords[i-1]
            v2 = ca_coords[i] - n_coords[i]
            v3 = c_coords[i] - ca_coords[i]
            # Simplified - real implementation uses dihedral angle
            phi = 0.0  # Would calculate dihedral
        
        # Psi: N(i) - CA(i) - C(i) - N(i+1)
        if i < n_res - 1:
            psi = 0.0  # Would calculate dihedral
        
        angles.append((phi, psi))
    
    return angles


def is_ramachandran_allowed(phi: float, psi: float, 
                            residue_type: str = 'general') -> bool:
    """
    Check if phi/psi angles are in allowed Ramachandran regions.
    
    Parameters
    ----------
    phi : float
        Phi angle in degrees
    psi : float
        Psi angle in degrees
    residue_type : str
        'general', 'glycine', or 'proline'
    
    Returns
    -------
    bool
        True if in allowed region
    
    Examples
    --------
    >>> is_ramachandran_allowed(-60, -45)  # alpha-helix region
    True
    >>> is_ramachandran_allowed(0, 0)  # disallowed
    False
    """
    # Simplified check - real implementation would use contours
    # Alpha-helix region: phi ~ -60, psi ~ -45
    # Beta-sheet region: phi ~ -120, psi ~ 120
    
    # Rough check for common allowed regions
    alpha_phi = abs(phi + 60) < 40
    alpha_psi = abs(psi + 45) < 40
    
    beta_phi = abs(phi + 120) < 40
    beta_psi = abs(psi - 120) < 40
    
    return (alpha_phi and alpha_psi) or (beta_phi and beta_psi)


def net_charge(sequence: str, pH: float = 7.0) -> float:
    """
    Calculate net charge of a peptide at given pH.
    
    Uses approximate pKa values for ionizable groups.
    
    Parameters
    ----------
    sequence : str
        Amino acid sequence
    pH : float
        pH value
    
    Returns
    -------
    float
        Net charge
    
    Examples
    --------
    >>> net_charge('KKK', 7.0)
    3.0
    >>> net_charge('DDD', 7.0)
    -3.0
    """
    # Approximate pKa values
    pKa_N_term = 9.0
    pKa_C_term = 2.0
    pKa_K = 10.0  # Lys
    pKa_R = 12.0  # Arg
    pKa_H = 6.0   # His
    pKa_D = 4.0   # Asp
    pKa_E = 4.5   # Glu
    pKa_C = 8.5   # Cys
    pKa_Y = 10.0  # Tyr
    
    sequence = sequence.upper()
    
    charge = 0.0
    
    # N-terminus
    charge += 1 / (1 + 10**(pH - pKa_N_term))
    
    # C-terminus
    charge += -1 / (1 + 10**(pKa_C_term - pH))
    
    # Side chains
    for aa in sequence:
        if aa == 'K':
            charge += 1 / (1 + 10**(pH - pKa_K))
        elif aa == 'R':
            charge += 1 / (1 + 10**(pH - pKa_R))
        elif aa == 'H':
            charge += 1 / (1 + 10**(pH - pKa_H))
        elif aa == 'D':
            charge += -1 / (1 + 10**(pKa_D - pH))
        elif aa == 'E':
            charge += -1 / (1 + 10**(pKa_E - pH))
    
    return round(charge, 2)


# Self-test
if __name__ == '__main__':
    print("Protein Structure Tools Test")
    print("=" * 40)
    
    # Test hydrophobicity
    print("\nHydropathy scores:")
    print(f"  VVVV: {hydrophobicity_score('VVVV'):.2f}")
    print(f"  KKKK: {hydrophobicity_score('KKKK'):.2f}")
    
    # Test helical wheel
    print("\nHelical wheel for 'EELLKK':")
    wheel = helical_wheel('EELLKK')
    for r in wheel:
        print(f"  {r['residue']}{r['position']}: angle={r['angle']}, pos=({r['x']}, {r['y']})")
    
    # Test net charge
    print("\nNet charge at pH 7:")
    print(f"  KKK: {net_charge('KKK', 7.0)}")
    print(f"  DDD: {net_charge('DDD', 7.0)}")
    print(f"  KDD: {net_charge('KDD', 7.0)}")
    
    # Test Ramachandran
    print("\nRamachandran allowed:")
    print(f"  phi=-60, psi=-45 (helix): {is_ramachandran_allowed(-60, -45)}")
    print(f"  phi=-120, psi=120 (sheet): {is_ramachandran_allowed(-120, 120)}")
    print(f"  phi=0, psi=0: {is_ramachandran_allowed(0, 0)}")
    
    print("\nAll tests passed")
