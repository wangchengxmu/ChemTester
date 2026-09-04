"""
Genetic Analysis Tools

L3 implementation for molecular biology calculations:
- Codon translation
- Sequence analysis
- Mutation classification
- Primer design
- Restriction site analysis

Source: Jakubowski & Flatt, Ch1.4 - Genetic Foundations
## Solver Instructions (for AI Agent)

When you encounter biochemistry genetics problems (DNA/RNA, codons, Hardy-Weinberg), follow this decision tree:

### Step 1: Identify what is given and what is asked
- DNA sequence analysis? Use `complement_dna(sequence)`, `transcribe_dna(dna_sequence)`, `translate_mrna(mrna_sequence)`
- Hardy-Weinberg equilibrium? Use `hardy_weinberg(p=None, q=None, ...)` - provide allele frequencies or genotype counts
- GC content? Use `gc_content(sequence)`
- Restriction enzyme sites? Use `find_restriction_sites(sequence, enzyme_site)`

### Step 2: Handle special cases
- **Hardy-Weinberg**: p + q = 1; p2 + 2pq + q2 = 1; assumes large population, random mating, no mutation/migration/selection
- **Central dogma**: DNA -> (transcription) -> mRNA -> (translation) -> Protein
- **Codon table**: Standard genetic code; 64 codons, 61 sense + 3 stop

### Examples
```python
# Example 1: Transcribe and translate
mrna = transcribe_dna("TACGGA")  # -> AUGCCU
protein = translate_mrna(mrna)  # -> Met-Pro

# Example 2: Hardy-Weinberg
# If q2 = 0.04 (frequency of recessive phenotype)
q = 0.2; p = 0.8  # p2=0.64, 2pq=0.32, q2=0.04
```
"""

from typing import Dict, List, Tuple, Optional
import re

# Standard Genetic Code
GENETIC_CODE = {
    'UUU': 'F', 'UUC': 'F',           # Phenylalanine
    'UUA': 'L', 'UUG': 'L',           # Leucine
    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',  # Leucine
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I',  # Isoleucine
    'AUG': 'M',                       # Methionine (Start)
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',  # Valine
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',  # Serine
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',  # Proline
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',  # Threonine
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',  # Alanine
    'UAU': 'Y', 'UAC': 'Y',           # Tyrosine
    'UAA': '*', 'UAG': '*', 'UGA': '*',  # Stop codons
    'CAU': 'H', 'CAC': 'H',           # Histidine
    'CAA': 'Q', 'CAG': 'Q',           # Glutamine
    'AAU': 'N', 'AAC': 'N',           # Asparagine
    'AAA': 'K', 'AAG': 'K',           # Lysine
    'GAU': 'D', 'GAC': 'D',           # Aspartate
    'GAA': 'E', 'GAG': 'E',           # Glutamate
    'UGU': 'C', 'UGC': 'C',           # Cysteine
    'UGG': 'W',                       # Tryptophan
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',  # Arginine
    'AGU': 'S', 'AGC': 'S',           # Serine
    'AGA': 'R', 'AGG': 'R',           # Arginine
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',  # Glycine
}

# Amino acid to codons (reverse lookup)
AMINO_ACID_CODONS = {}
for codon, aa in GENETIC_CODE.items():
    if aa not in AMINO_ACID_CODONS:
        AMINO_ACID_CODONS[aa] = []
    AMINO_ACID_CODONS[aa].append(codon)

# Amino acid names
AMINO_ACID_NAMES = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys',
    'E': 'Glu', 'Q': 'Gln', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
    'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro',
    'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val',
    '*': 'Stop'
}

# Amino acid properties
AMINO_ACID_PROPERTIES = {
    'A': 'nonpolar', 'R': 'positive', 'N': 'polar', 'D': 'negative', 'C': 'polar',
    'E': 'negative', 'Q': 'polar', 'G': 'nonpolar', 'H': 'positive', 'I': 'nonpolar',
    'L': 'nonpolar', 'K': 'positive', 'M': 'nonpolar', 'F': 'nonpolar', 'P': 'nonpolar',
    'S': 'polar', 'T': 'polar', 'W': 'nonpolar', 'Y': 'polar', 'V': 'nonpolar',
    '*': 'stop'
}

# Common restriction enzymes
RESTRICTION_ENZYMES = {
    'EcoRI': {'site': 'GAATTC', 'cut': (1, 5)},      # G^AATTC
    'HindIII': {'site': 'AAGCTT', 'cut': (1, 5)},    # A^AGCTT
    'BamHI': {'site': 'GGATCC', 'cut': (1, 5)},      # G^GATCC
    'NotI': {'site': 'GCGGCCGC', 'cut': (2, 6)},     # GC^GGCCGC
    'SmaI': {'site': 'CCCGGG', 'cut': (3, 3)},       # CCC^GGG (blunt)
    'PstI': {'site': 'CTGCAG', 'cut': (5, 1)},       # CTGCA^G
    'KpnI': {'site': 'GGTACC', 'cut': (5, 1)},       # GGTAC^C
}


def codon_to_amino_acid(codon: str) -> str:
    """
    Translate a codon to its amino acid.
    
    Parameters
    ----------
    codon : str
        Three-nucleotide codon (e.g., 'AUG', 'UUU')
        
    Returns
    -------
    str
        Single-letter amino acid code (e.g., 'M', 'F')
        '*' for stop codons
        
    Raises
    ------
    ValueError
        If codon is not valid (wrong length or invalid nucleotides)
        
    Examples
    --------
    >>> codon_to_amino_acid('AUG')
    'M'
    >>> codon_to_amino_acid('UAA')
    '*'
    """
    codon = codon.upper()
    
    if len(codon) != 3:
        raise ValueError(f"Codon must be 3 nucleotides, got {len(codon)}")
    
    valid_bases = set('AUGC')
    if not all(b in valid_bases for b in codon):
        raise ValueError(f"Invalid nucleotides in codon: {codon}")
    
    return GENETIC_CODE.get(codon, '?')


def amino_acid_to_codons(amino_acid: str) -> List[str]:
    """
    Return all codons for a given amino acid.
    
    Parameters
    ----------
    amino_acid : str
        Single-letter amino acid code (e.g., 'M', 'L')
        
    Returns
    -------
    List[str]
        List of all codons encoding this amino acid
        
    Examples
    --------
    >>> amino_acid_to_codons('M')
    ['AUG']
    >>> len(amino_acid_to_codons('L'))
    6
    """
    aa = amino_acid.upper()
    
    if aa not in AMINO_ACID_CODONS:
        raise ValueError(f"Unknown amino acid: {amino_acid}")
    
    return AMINO_ACID_CODONS[aa].copy()


def transcribe_dna(dna_sequence: str) -> str:
    """
    Transcribe DNA to mRNA (replace T with U).
    
    Parameters
    ----------
    dna_sequence : str
        DNA sequence (5' to 3')
        
    Returns
    -------
    str
        mRNA sequence (5' to 3')
        
    Examples
    --------
    >>> transcribe_dna('ATGTAA')
    'AUGUAA'
    """
    return dna_sequence.upper().replace('T', 'U')


def translate_mrna(mrna_sequence: str, start_pos: int = 0) -> str:
    """
    Translate mRNA to protein sequence.
    
    Parameters
    ----------
    mrna_sequence : str
        mRNA sequence (5' to 3')
    start_pos : int
        Starting position (0-indexed) for translation
        
    Returns
    -------
    str
        Protein sequence (stops at first stop codon)
        
    Examples
    --------
    >>> translate_mrna('AUGGCCUAA')
    'MA'
    """
    mrna = mrna_sequence.upper()
    protein = []
    
    for i in range(start_pos, len(mrna) - 2, 3):
        codon = mrna[i:i+3]
        aa = GENETIC_CODE.get(codon, '?')
        
        if aa == '*':  # Stop codon
            break
        protein.append(aa)
    
    return ''.join(protein)


def find_orfs(sequence: str, min_length: int = 100) -> List[Dict]:
    """
    Find all open reading frames in a sequence.
    
    Parameters
    ----------
    sequence : str
        DNA or mRNA sequence
    min_length : int
        Minimum ORF length in nucleotides
        
    Returns
    -------
    List[Dict]
        List of ORFs with start, end, length, frame, and protein
        
    Examples
    --------
    >>> orfs = find_orfs('ATGAAATAG', min_length=3)
    >>> len(orfs) > 0
    True
    """
    # Convert to mRNA if DNA
    seq = sequence.upper().replace('T', 'U')
    
    start_codon = 'AUG'
    stop_codons = {'UAA', 'UAG', 'UGA'}
    
    orfs = []
    
    # Check all 3 frames
    for frame in range(3):
        i = frame
        while i < len(seq) - 2:
            codon = seq[i:i+3]
            
            if codon == start_codon:
                # Found start, look for stop
                start = i
                protein = ['M']
                j = i + 3
                
                while j < len(seq) - 2:
                    next_codon = seq[j:j+3]
                    aa = GENETIC_CODE.get(next_codon, '?')
                    
                    if next_codon in stop_codons:
                        # Found stop
                        length = j + 3 - start
                        if length >= min_length:
                            orfs.append({
                                'start': start,
                                'end': j + 3,
                                'length': length,
                                'frame': frame,
                                'protein': ''.join(protein)
                            })
                        break
                    
                    protein.append(aa)
                    j += 3
                
                i = start + 3
            else:
                i += 3
    
    return orfs


def gc_content(sequence: str) -> float:
    """
    Calculate GC content as fraction.
    
    Parameters
    ----------
    sequence : str
        DNA or RNA sequence
        
    Returns
    -------
    float
        GC content (0.0 to 1.0)
        
    Examples
    --------
    >>> gc_content('GCGC')
    1.0
    >>> gc_content('ATAT')
    0.0
    >>> round(gc_content('ATGC'), 2)
    0.5
    """
    seq = sequence.upper()
    gc = seq.count('G') + seq.count('C')
    return gc / len(seq) if len(seq) > 0 else 0.0


def complement_dna(sequence: str) -> str:
    """
    Return complement of DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence (5' to 3')
        
    Returns
    -------
    str
        Complementary strand (5' to 3')
        
    Examples
    --------
    >>> complement_dna('ATGC')
    'TACG'
    """
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement.get(b, b) for b in sequence.upper())


def reverse_complement(sequence: str) -> str:
    """
    Return reverse complement of DNA sequence.
    
    Parameters
    ----------
    sequence : str
        DNA sequence (5' to 3')
        
    Returns
    -------
    str
        Reverse complement (5' to 3')
        
    Examples
    --------
    >>> reverse_complement('ATGC')
    'GCAT'
    """
    return complement_dna(sequence)[::-1]


def classify_mutation(ref_codon: str, mut_codon: str) -> Dict:
    """
    Classify mutation type.
    
    Parameters
    ----------
    ref_codon : str
        Reference codon
    mut_codon : str
        Mutant codon
        
    Returns
    -------
    Dict
        Mutation classification with type, ref_aa, mut_aa, and is_conservative
        
    Examples
    --------
    >>> classify_mutation('UAU', 'UAC')
    {'type': 'silent', 'ref_aa': 'Y', 'mut_aa': 'Y', 'is_conservative': True}
    >>> classify_mutation('UAU', 'UAG')
    {'type': 'nonsense', 'ref_aa': 'Y', 'mut_aa': '*', 'is_conservative': False}
    """
    ref = ref_codon.upper()
    mut = mut_codon.upper()
    
    # Check for frameshift
    if len(ref) != len(mut):
        return {
            'type': 'frameshift',
            'ref_aa': None,
            'mut_aa': None,
            'is_conservative': False
        }
    
    ref_aa = codon_to_amino_acid(ref)
    mut_aa = codon_to_amino_acid(mut)
    
    if ref_aa == mut_aa:
        mutation_type = 'silent'
        conservative = True
    elif mut_aa == '*':
        mutation_type = 'nonsense'
        conservative = False
    else:
        mutation_type = 'missense'
        # Check if conservative
        ref_prop = AMINO_ACID_PROPERTIES.get(ref_aa, '')
        mut_prop = AMINO_ACID_PROPERTIES.get(mut_aa, '')
        conservative = (ref_prop == mut_prop)
    
    return {
        'type': mutation_type,
        'ref_aa': ref_aa,
        'mut_aa': mut_aa,
        'is_conservative': conservative
    }


def primer_tm(sequence: str, na_conc: float = 50.0) -> float:
    """
    Calculate primer melting temperature using Wallace rule with salt correction.
    
    Parameters
    ----------
    sequence : str
        Primer sequence
    na_conc : float
        Na+ concentration in mM (default 50)
        
    Returns
    -------
    float
        Melting temperature in degC
        
    Examples
    --------
    >>> round(primer_tm('ATGC'), 1)
    12.0
    """
    seq = sequence.upper()
    
    # Wallace rule (simple)
    gc = seq.count('G') + seq.count('C')
    at = seq.count('A') + seq.count('T')
    tm_basic = 4 * gc + 2 * at
    
    # Salt correction (simplified)
    salt_correction = 16.6 * (len(seq) / 20) * (na_conc / 50 - 1)
    
    return tm_basic + salt_correction


def pcr_product_size(forward_pos: int, reverse_pos: int) -> int:
    """
    Calculate expected PCR product size.
    
    Parameters
    ----------
    forward_pos : int
        Position of forward primer binding site (5' end, 0-indexed)
    reverse_pos : int
        Position of reverse primer binding site (5' end on forward strand)
        
    Returns
    -------
    int
        Product size in bp
        
    Examples
    --------
    >>> pcr_product_size(100, 600)
    501
    """
    return abs(reverse_pos - forward_pos) + 1


def find_restriction_sites(sequence: str, enzyme: str) -> List[int]:
    """
    Find all positions where restriction enzyme cuts.
    
    Parameters
    ----------
    sequence : str
        DNA sequence
    enzyme : str
        Enzyme name (e.g., 'EcoRI', 'HindIII')
        
    Returns
    -------
    List[int]
        Positions of cut sites (0-indexed)
        
    Examples
    --------
    >>> find_restriction_sites('GAATTCGAATTC', 'EcoRI')
    [0, 6]
    """
    seq = sequence.upper()
    
    if enzyme not in RESTRICTION_ENZYMES:
        raise ValueError(f"Unknown enzyme: {enzyme}")
    
    site = RESTRICTION_ENZYMES[enzyme]['site']
    cut_offset = RESTRICTION_ENZYMES[enzyme]['cut'][0]
    
    positions = []
    for match in re.finditer(site, seq):
        positions.append(match.start() + cut_offset)
    
    return positions


def hamming_distance(seq1: str, seq2: str) -> int:
    """
    Calculate number of positions where sequences differ.
    
    Parameters
    ----------
    seq1 : str
        First sequence
    seq2 : str
        Second sequence
        
    Returns
    -------
    int
        Hamming distance
        
    Raises
    ------
    ValueError
        If sequences have different lengths
        
    Examples
    --------
    >>> hamming_distance('ATGC', 'ATGG')
    1
    >>> hamming_distance('ATGC', 'ATGC')
    0
    """
    if len(seq1) != len(seq2):
        raise ValueError(f"Sequences must have same length: {len(seq1)} vs {len(seq2)}")
    
    return sum(1 for a, b in zip(seq1.upper(), seq2.upper()) if a != b)


def codon_degeneracy(amino_acid: str) -> int:
    """
    Return the number of codons encoding an amino acid.
    
    Parameters
    ----------
    amino_acid : str
        Single-letter amino acid code
        
    Returns
    -------
    int
        Number of codons
        
    Examples
    --------
    >>> codon_degeneracy('M')
    1
    >>> codon_degeneracy('L')
    6
    """
    return len(amino_acid_to_codons(amino_acid))


if __name__ == "__main__":
    # Quick test
    print("Genetic Tools Test")
    print("-" * 40)
    print(f"AUG -> {codon_to_amino_acid('AUG')}")
    print(f"UAA -> {codon_to_amino_acid('UAA')}")
    print(f"Leu codons: {amino_acid_to_codons('L')}")
    print(f"ATGC GC content: {gc_content('ATGC'):.2%}")
    print(f"Reverse complement of ATGC: {reverse_complement('ATGC')}")
    print(f"Mutation UAU->UAG: {classify_mutation('UAU', 'UAG')}")

MCP_TOOLS = [
    {
        "name": "amino_acid_to_codons",
        "description": "Return all codons for a given amino acid.",
        "parameters": [
            {
                "name": "amino_acid",
                "type": "number"
            }
        ]
    },
    {
        "name": "classify_mutation",
        "description": "Classify mutation type.",
        "parameters": [
            {
                "name": "ref_codon",
                "type": "number"
            },
            {
                "name": "mut_codon",
                "type": "number"
            }
        ]
    },
    {
        "name": "codon_degeneracy",
        "description": "Return the number of codons encoding an amino acid.",
        "parameters": [
            {
                "name": "amino_acid",
                "type": "number"
            }
        ]
    },
    {
        "name": "codon_to_amino_acid",
        "description": "Translate a codon to its amino acid.",
        "parameters": [
            {
                "name": "codon",
                "type": "number"
            }
        ]
    },
    {
        "name": "complement_dna",
        "description": "Return complement of DNA sequence.",
        "parameters": [
            {
                "name": "sequence",
                "type": "string"
            }
        ]
    },
    {
        "name": "find_orfs",
        "description": "Find all open reading frames in a sequence.",
        "parameters": [
            {
                "name": "sequence",
                "type": "string"
            },
            {
                "name": "min_length",
                "type": "number"
            }
        ]
    },
    {
        "name": "find_restriction_sites",
        "description": "Find all positions where restriction enzyme cuts.",
        "parameters": [
            {
                "name": "sequence",
                "type": "string"
            },
            {
                "name": "enzyme",
                "type": "number"
            }
        ]
    },
    {
        "name": "gc_content",
        "description": "Calculate GC content as fraction.",
        "parameters": [
            {
                "name": "sequence",
                "type": "string"
            }
        ]
    },
    {
        "name": "hamming_distance",
        "description": "Calculate number of positions where sequences differ.",
        "parameters": [
            {
                "name": "seq1",
                "type": "number"
            },
            {
                "name": "seq2",
                "type": "number"
            }
        ]
    },
    {
        "name": "pcr_product_size",
        "description": "Calculate expected PCR product size.",
        "parameters": [
            {
                "name": "forward_pos",
                "type": "number"
            },
            {
                "name": "reverse_pos",
                "type": "number"
            }
        ]
    },
    {
        "name": "primer_tm",
        "description": "Calculate primer melting temperature using Wallace rule with salt correction.",
        "parameters": [
            {
                "name": "sequence",
                "type": "string"
            },
            {
                "name": "na_conc",
                "type": "number"
            }
        ]
    },
    {
        "name": "reverse_complement",
        "description": "Return reverse complement of DNA sequence.",
        "parameters": [
            {
                "name": "sequence",
                "type": "string"
            }
        ]
    },
    {
        "name": "transcribe_dna",
        "description": "Transcribe DNA to mRNA (replace T with U).",
        "parameters": [
            {
                "name": "dna_sequence",
                "type": "string"
            }
        ]
    },
    {
        "name": "translate_mrna",
        "description": "Translate mRNA to protein sequence.",
        "parameters": [
            {
                "name": "mrna_sequence",
                "type": "string"
            },
            {
                "name": "start_pos",
                "type": "number"
            }
        ]
    }
]
