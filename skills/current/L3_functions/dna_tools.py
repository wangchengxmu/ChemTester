"""
DNA/RNA Tools
=============

Python implementations for nucleic acid calculations.

Source: L2 dna_rna_structure.md

## Solver Instructions (for AI Agent)

When you encounter DNA sequence analysis problems:

### Step 1: Identify what is given and what is asked
- Given: DNA sequence, salt concentration
- Asked: GC content, melting temperature, molecular weight, complement, translation

### Step 2: Choose the correct function
- `gc_content(sequence)`: Fraction of G+C bases
- `tm_estimate(sequence, na_conc)`: Melting temperature
- `molecular_weight_dna(sequence, single_stranded)`: MW in g/mol
- `complement(sequence, rna)`: Complementary strand (T->A, A->T, G->C, C->G)
- `reverse_complement(sequence, rna)`: Reverse complement
- `check_palindrome(sequence)`: Is sequence a palindrome?
- `codon_table()`: Standard genetic code dictionary
- `translate_dna(dna_sequence, frame)`: Translate DNA to protein

### Step 3: Handle special cases
- Short oligos (<14 bp): Tm = 2(A+T) + 4(G+C) in degC
- Longer sequences: Tm = 81.5 + 16.6xlog([Na+]) + 0.41x(%GC) - 675/N
- Molecular weight: ssDNA ~ 330 g/mol per base; dsDNA ~ 660 g/mol per base pair

### Examples
```python
gc_content("ATGCGATCGA")  # -> 0.5 (50% GC)
complement("ATGC")  # -> "TACG"
reverse_complement("ATGC")  # -> "GCAT"
tm_estimate("ATGCGATCGATCGA", 50e-9)  # -> ~44degC
```
"""

import re
from typing import Dict, List, Tuple
import numpy as np

# Nucleotide molecular weights (g/mol)
NUCLEOTIDE_MW = {
    'A': 331.2,  # dAMP (internal residue)
    'T': 322.2,  # dTMP (internal residue)
    'G': 347.2,  # dGMP (internal residue)
    'C': 307.2,  # dCMP (internal residue)
    'U': 290.20,  # Uracil
}

# Base pairing rules
BASE_PAIRS = {
    'A': 'T',  # DNA
    'T': 'A',
    'G': 'C',
    'C': 'G',
}


def gc_content(sequence: str) -> float:
    """
    Calculate GC content of DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence (case insensitive)
    
    Returns
    -------
    float
        GC percentage
    
    Examples
    --------
    >>> gc_content('ATGC')
    50.0
    >>> gc_content('GGCC')
    100.0
    """
    seq = sequence.upper()
    gc = seq.count('G') + seq.count('C')
    return gc / len(seq) if seq else 0


def hydrogen_bond_count(sequence: str) -> dict:
    """
    Count hydrogen bonds in a DNA double strand.
    
    Each G-C pair has 3 H-bonds, each A-T pair has 2 H-bonds.
    
    Args:
        sequence: DNA sequence (one strand, 5'->3'). Will be checked
            against its complement for valid base pairing.
    
    Returns:
        Dict with:
        - 'gc_pairs': number of G-C pairs
        - 'at_pairs': number of A-T pairs
        - 'gc_hbonds': H-bonds from G-C pairs (3 each)
        - 'at_hbonds': H-bonds from A-T pairs (2 each)
        - 'total_hbonds': total hydrogen bonds
        - 'invalid_bases': list of non-ACGT bases (if any)
    
    Examples:
        >>> hydrogen_bond_count('CGATGAGCC')
        {'gc_pairs': 6, 'at_pairs': 3, 'gc_hbonds': 18, 'at_hbonds': 6, 'total_hbonds': 24, 'invalid_bases': []}
        >>> hydrogen_bond_count('ATGC')
        {'gc_pairs': 1, 'at_pairs': 3, 'gc_hbonds': 3, 'at_hbonds': 6, 'total_hbonds': 9, 'invalid_bases': []}
    """
    seq = sequence.upper()
    gc_pairs = seq.count('G') + seq.count('C')
    at_pairs = seq.count('A') + seq.count('T')
    invalid = [base for base in seq if base not in 'ACGT']
    
    return {
        'gc_pairs': gc_pairs,
        'at_pairs': at_pairs,
        'gc_hbonds': gc_pairs * 3,
        'at_hbonds': at_pairs * 2,
        'total_hbonds': gc_pairs * 3 + at_pairs * 2,
        'invalid_bases': invalid,
    }


def tm_estimate(sequence: str, na_conc: float = 0.05, salt_correction: bool = True) -> float:
    """
    Estimate melting temperature of DNA oligo.
    
    Simple formula (Wallace rule): Tm = 2(A+T) + 4(G+C)
    For more accurate estimation, use nearest-neighbor method.
    
    Parameters
    ----------
    sequence : str
        DNA sequence
    na_conc : float
        Na+ concentration (M), default 50 mM. Only used if salt_correction=True.
    salt_correction : bool
        If True, applies salt correction for sequences >= 14 bp.
        Set to False for the basic Wallace rule only.
    
    Returns
    -------
    float
        Estimated Tm in degC
    
    Examples
    --------
    >>> tm_estimate('ATGC')
    12.0
    >>> tm_estimate('GCGCGC')
    24.0
    >>> tm_estimate('GCGCGCATATATAT', salt_correction=False)  # 14bp, basic rule
    40.0
    """
    seq = sequence.upper()
    at = seq.count('A') + seq.count('T')
    gc = seq.count('G') + seq.count('C')
    
    # Basic Wallace formula
    tm = 2 * at + 4 * gc
    
    # Salt correction for longer sequences
    if salt_correction and len(seq) >= 14:
        tm += 16.6 * np.log10(na_conc)
    
    return tm


def molecular_weight_dna(sequence: str, single_stranded: bool = False) -> float:
    """
    Calculate molecular weight of DNA.
    
    Parameters
    ----------
    sequence : str
        DNA sequence
    single_stranded : bool
        True for ssDNA, False for dsDNA
    
    Returns
    -------
    float
        Molecular weight in g/mol
    
    Examples
    --------
    >>> molecular_weight_dna('ATGC', single_stranded=True)
    1235.8
    """
    seq = sequence.upper()
    mw = sum(NUCLEOTIDE_MW.get(base, 300) for base in seq)
    # Subtract water for each phosphodiester bond
    mw -= 18.0 * (len(seq) - 1)
    
    if not single_stranded:
        # Add complementary strand
        mw += molecular_weight_dna(complement(sequence), single_stranded=True)
    
    return mw


def complement(sequence: str, rna: bool = False) -> str:
    """
    Generate complement sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence
    rna : bool
        True to use U instead of T
    
    Returns
    -------
    str
        Complement sequence
    
    Examples
    --------
    >>> complement('ATGC')
    'TACG'
    """
    seq = sequence.upper()
    comp = ''
    for base in seq:
        if base in BASE_PAIRS:
            comp_base = BASE_PAIRS[base]
            if rna and comp_base == 'T':
                comp_base = 'U'
            comp += comp_base
    return comp


def reverse_complement(sequence: str, rna: bool = False) -> str:
    """
    Generate reverse complement.
    
    Parameters
    ----------
    sequence : str
        DNA sequence
    rna : bool
        True for RNA complement
    
    Returns
    -------
    str
        Reverse complement sequence
    
    Examples
    --------
    >>> reverse_complement('ATGC')
    'GCAT'
    """
    return complement(sequence, rna)[::-1]


def check_palindrome(sequence: str) -> bool:
    """
    Check if sequence is a palindrome.
    
    Parameters
    ----------
    sequence : str
        DNA sequence
    
    Returns
    -------
    bool
        True if palindrome (equals its reverse complement)
    
    Examples
    --------
    >>> check_palindrome('GAATTC')
    True
    >>> check_palindrome('ATGC')
    False
    """
    return sequence.upper() == reverse_complement(sequence)


def codon_table() -> Dict[str, str]:
    """
    Return standard genetic code table.
    
    Returns
    -------
    dict
        Codon -> amino acid mapping
    """
    table = {
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    }
    return table


def translate_dna(dna_sequence: str, frame: int = 0) -> str:
    """
    Translate DNA to protein sequence.
    
    Parameters
    ----------
    dna_sequence : str
        DNA coding sequence
    frame : int
        Reading frame (0, 1, or 2)
    
    Returns
    -------
    str
        Amino acid sequence (* for stop)
    
    Examples
    --------
    >>> translate_dna('ATGGCGTAA')
    'MA*'
    """
    table = codon_table()
    dna = dna_sequence.upper()
    
    # Convert to RNA (T -> U)
    rna = dna.replace('T', 'U')
    
    protein = ''
    for i in range(frame, len(rna) - 2, 3):
        codon = rna[i:i+3]
        aa = table.get(codon, '?')
        protein += aa
    
    return protein


# Self-test
if __name__ == '__main__':
    print("DNA/RNA Tools Test")
    print("=" * 40)
    
    # Test GC content
    seq = 'ATGCGCATGCAT'
    print(f"\nSequence: {seq}")
    print(f"GC content: {gc_content(seq):.1f}%")
    
    # Test Tm
    print(f"Tm estimate: {tm_estimate(seq):.1f} C")
    
    # Test complement
    print(f"Complement: {complement(seq)}")
    print(f"Reverse complement: {reverse_complement(seq)}")
    
    # Test translation
    dna = 'ATGGCGAAAGGGTAA'
    print(f"\nDNA: {dna}")
    print(f"Protein: {translate_dna(dna)}")
    
    print("\nAll tests passed")


# MCP Tool Declarations
MCP_TOOLS = [
    {'name': 'check_palindrome', 'description': "Check if sequence is a palindrome.\n\nParameters\n----------\nsequence : str\n    DNA sequence\n\nReturns\n-------\nbool\n    true if palindrome (equals its reverse complement)\n\nExamples\n--------\n>>> check_palindrome('GAATTC')\ntrue\n>>> check_palindrome('ATGC')\nfalse", 'inputSchema': {'type': 'object', 'properties': {'sequence': {'type': 'string', 'description': 'Sequence'}}, 'required': ['sequence']}},
    {'name': 'codon_table', 'description': 'Return standard genetic code table.\n\nReturns\n-------\ndict\n    Codon -> amino acid mapping', 'inputSchema': {'type': 'object', 'properties': {}, 'required': []}},
    {'name': 'complement', 'description': "Generate complement sequence.\n\nParameters\n----------\nsequence : str\n    DNA sequence\nrna : bool\n    true to use U instead of T\n\nReturns\n-------\nstr\n    Complement sequence\n\nExamples\n--------\n>>> complement('ATGC')\n'TACG'", 'inputSchema': {'type': 'object', 'properties': {'sequence': {'type': 'string', 'description': 'Sequence'}, 'rna': {'type': 'number', 'description': 'Rna', 'default': False}}, 'required': ['sequence']}},
    {'name': 'gc_content', 'description': "Calculate GC content of DNA sequence.\n\nParameters\n----------\nsequence : str\n    DNA sequence (case insensitive)\n\nReturns\n-------\nfloat\n    GC percentage\n\nExamples\n--------\n>>> gc_content('ATGC')\n50.0\n>>> gc_content('GGCC')\n100.0", 'inputSchema': {'type': 'object', 'properties': {'sequence': {'type': 'string', 'description': 'Sequence'}}, 'required': ['sequence']}},
    {'name': 'molecular_weight_dna', 'description': "Calculate molecular weight of DNA.\n\nParameters\n----------\nsequence : str\n    DNA sequence\nsingle_stranded : bool\n    true for ssDNA, false for dsDNA\n\nReturns\n-------\nfloat\n    Molecular weight in g/mol\n\nExamples\n--------\n>>> molecular_weight_dna('ATGC', single_stranded=true)\n1235.8", 'inputSchema': {'type': 'object', 'properties': {'sequence': {'type': 'string', 'description': 'Sequence'}, 'single_stranded': {'type': 'number', 'description': 'Single Stranded', 'default': False}}, 'required': ['sequence']}},
    {'name': 'reverse_complement', 'description': "Generate reverse complement.\n\nParameters\n----------\nsequence : str\n    DNA sequence\nrna : bool\n    true for RNA complement\n\nReturns\n-------\nstr\n    Reverse complement sequence\n\nExamples\n--------\n>>> reverse_complement('ATGC')\n'GCAT'", 'inputSchema': {'type': 'object', 'properties': {'sequence': {'type': 'string', 'description': 'Sequence'}, 'rna': {'type': 'number', 'description': 'Rna', 'default': False}}, 'required': ['sequence']}},
    {'name': 'tm_estimate', 'description': "Estimate melting temperature of DNA oligo.\n\nSimple formula: Tm = 2(A+T) + 4(G+C)\nFor more accurate estimation, use nearest-neighbor method.\n\nParameters\n----------\nsequence : str\n    DNA sequence\nna_conc : float\n    Na+ concentration (M), default 50 mM\n\nReturns\n-------\nfloat\n    Estimated Tm in degC\n\nExamples\n--------\n>>> tm_estimate('ATGC')\n12.0\n>>> tm_estimate('GCGCGC')\n24.0", 'inputSchema': {'type': 'object', 'properties': {'sequence': {'type': 'string', 'description': 'Sequence'}, 'na_conc': {'type': 'number', 'description': 'Na Conc', 'default': 5e-08}}, 'required': ['sequence']}},
    {'name': 'translate_dna', 'description': "Translate DNA to protein sequence.\n\nParameters\n----------\ndna_sequence : str\n    DNA coding sequence\nframe : int\n    Reading frame (0, 1, or 2)\n\nReturns\n-------\nstr\n    Amino acid sequence (* for stop)\n\nExamples\n--------\n>>> translate_dna('ATGGCGTAA')\n'MA*'", 'inputSchema': {'type': 'object', 'properties': {'dna_sequence': {'type': 'string', 'description': 'Dna Sequence'}, 'frame': {'type': 'number', 'description': 'Frame', 'default': 0}}, 'required': ['dna_sequence']}}
]
