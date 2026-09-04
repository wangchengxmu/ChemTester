"""
Physical Organic Chemistry Tools
================================

A Python module for physical organic chemistry calculations including:
- Hammett analysis
- pKa prediction
- Kinetic isotope effects
- Stereochemical analysis
- Reaction coordinate diagrams
- Linear free energy relationships
- Baldwin's rules
- Arrhenius parameters

Uses only Python standard library (math, statistics).
"""

import math
import statistics
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# DATA TABLES
# =============================================================================

# Hammett sigma constants (σ) for common substituents
# Source: March's Advanced Organic Chemistry, Hansch et al.
HAMMETT_SIGMA: Dict[str, Dict[str, float]] = {
    # Format: substituent: {"sigma_p": value, "sigma_m": value}
    "H": {"sigma_p": 0.00, "sigma_m": 0.00},
    "Me": {"sigma_p": -0.17, "sigma_m": -0.07},
    "Et": {"sigma_p": -0.15, "sigma_m": -0.07},
    "i-Pr": {"sigma_p": -0.15, "sigma_m": -0.07},
    "t-Bu": {"sigma_p": -0.20, "sigma_m": -0.10},
    "Ph": {"sigma_p": -0.01, "sigma_m": 0.06},
    "OMe": {"sigma_p": -0.27, "sigma_m": 0.12},
    "OEt": {"sigma_p": -0.24, "sigma_m": 0.10},
    "OH": {"sigma_p": -0.37, "sigma_m": 0.12},
    "OAc": {"sigma_p": 0.31, "sigma_m": 0.39},
    "NH2": {"sigma_p": -0.66, "sigma_m": -0.16},
    "NMe2": {"sigma_p": -0.83, "sigma_m": -0.21},
    "NEt2": {"sigma_p": -0.71, "sigma_m": -0.24},
    "NHCOR": {"sigma_p": 0.00, "sigma_m": 0.21},
    "NO2": {"sigma_p": 0.78, "sigma_m": 0.71},
    "CN": {"sigma_p": 0.66, "sigma_m": 0.56},
    "COOH": {"sigma_p": 0.45, "sigma_m": 0.37},
    "COOR": {"sigma_p": 0.45, "sigma_m": 0.37},
    "CHO": {"sigma_p": 0.42, "sigma_m": 0.35},
    "COR": {"sigma_p": 0.50, "sigma_m": 0.38},
    "CONH2": {"sigma_p": 0.36, "sigma_m": 0.28},
    "SO2R": {"sigma_p": 0.57, "sigma_m": 0.46},
    "SO2NH2": {"sigma_p": 0.57, "sigma_m": 0.46},
    "F": {"sigma_p": 0.06, "sigma_m": 0.34},
    "Cl": {"sigma_p": 0.23, "sigma_m": 0.37},
    "Br": {"sigma_p": 0.23, "sigma_m": 0.39},
    "I": {"sigma_p": 0.18, "sigma_m": 0.35},
    "CF3": {"sigma_p": 0.54, "sigma_m": 0.43},
    "CCl3": {"sigma_p": 0.46, "sigma_m": 0.36},
    "CH2Cl": {"sigma_p": 0.15, "sigma_m": 0.12},
    "SiMe3": {"sigma_p": -0.07, "sigma_m": -0.04},
    "SO2Me": {"sigma_p": 0.60, "sigma_m": 0.52},
    "SMe": {"sigma_p": 0.00, "sigma_m": 0.15},
    "SH": {"sigma_p": 0.15, "sigma_m": 0.25},
}

# A-values (conformational free energy differences) for cyclohexane substituents
# Positive value means equatorial preference (in kcal/mol at 25°C)
A_VALUES: Dict[str, float] = {
    "H": 0.0,
    "Me": 1.74,
    "Et": 1.79,
    "i-Pr": 2.21,
    "t-Bu": 4.9,  # Very strong equatorial preference
    "Ph": 3.0,
    "OMe": 0.60,
    "OH": 0.87,
    "NH2": 1.23,
    "NH3+": 1.9,
    "COOH": 1.35,
    "COO-": 1.91,
    "COOR": 1.27,
    "CN": 0.20,
    "F": 0.15,
    "Cl": 0.43,
    "Br": 0.38,
    "I": 0.43,
    "SH": 1.07,
    "SMe": 1.30,
    "SiMe3": 2.5,
}

# pKa fragment contributions (simplified Taft-type parameters)
# Base values and substituent contributions for organic acids
PKA_FRAGMENTS: Dict[str, Dict[str, float]] = {
    # Fragment: {"base_pka": value, "contributions": {...}}
    "carboxylic_acid": {"base_pka": 4.76},
    "phenol": {"base_pka": 10.0},
    "alcohol": {"base_pka": 16.0},
    "amine_primary": {"base_pka": 10.6},
    "amine_secondary": {"base_pka": 11.0},
    "amine_tertiary": {"base_pka": 10.8},
    "aniline": {"base_pka": 4.6},
    "thiol": {"base_pka": 10.3},
    # Position-dependent substituent effects (ΔpKa)
    "alpha_alkyl": -0.1,  # Makes acid slightly stronger
    "alpha_aryl": 0.3,
    "alpha_halogen": -1.5,
    "alpha_OH": -1.0,
    "alpha_NH2": -0.5,
    "alpha_CN": -1.7,
    "alpha_NO2": -2.0,
    "beta_alkyl": 0.1,
    "beta_halogen": -0.5,
    "beta_OH": -0.3,
    "gamma_alkyl": 0.05,
}

# Baldwin's rules lookup table
BALDWIN_RULES: Dict[str, Dict[str, Dict[int, str]]] = {
    "tet": {  # Nucleophile attacks sp³ center
        "exo": {3: "disfav", 4: "fav", 5: "fav", 6: "fav", 7: "fav"},
        "endo": {3: "fav", 4: "disfav", 5: "disfav", 6: "fav", 7: "fav"},
    },
    "trig": {  # Nucleophile attacks sp² center
        "exo": {3: "fav", 4: "fav", 5: "fav", 6: "fav", 7: "fav"},
        "endo": {3: "disfav", 4: "disfav", 5: "fav", 6: "fav", 7: "fav"},
    },
    "dig": {  # Nucleophile attacks sp center
        "exo": {3: "disfav", 4: "fav", 5: "fav", 6: "fav", 7: "fav"},
        "endo": {3: "fav", 4: "fav", 5: "fav", 6: "fav", 7: "fav"},
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _parse_substituent(sub: str) -> Tuple[str, str]:
    """Parse substituent string into (position, group) tuple.
    
    Args:
        sub: Substituent string like 'p-OMe', 'm-NO2', 'o-Me'
        
    Returns:
        Tuple of (position, group) where position is 'p', 'm', or 'o'
    """
    sub = sub.strip()
    if "-" in sub:
        parts = sub.split("-", 1)
        position = parts[0].lower()
        group = parts[1] if len(parts) > 1 else "H"
        return (position, group)
    # Default to para if no position specified
    return ("p", sub)


def _get_sigma(sub: str) -> Optional[float]:
    """Get sigma constant for a substituent.
    
    Args:
        sub: Substituent string like 'p-OMe', 'm-NO2'
        
    Returns:
        Sigma value or None if not found
    """
    position, group = _parse_substituent(sub)
    
    if group not in HAMMETT_SIGMA:
        return None
    
    sigma_key = f"sigma_{position}"
    if sigma_key not in HAMMETT_SIGMA[group]:
        # Default to para if position not found
        sigma_key = "sigma_p"
    
    return HAMMETT_SIGMA[group].get(sigma_key)


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

@dataclass
class HammettResult:
    """Result from Hammett analysis."""
    substituent: str
    sigma: float
    log_k_ratio: float
    k_ratio: float
    interpretation: str


def hammett_analysis(
    substituents: List[str],
    rho: float
) -> Dict[str, Union[List[HammettResult], str]]:
    """
    Calculate log(k/k₀) = ρσ for a set of substituents.
    
    The Hammett equation relates reaction rates or equilibria to substituent
    effects through the equation: log(k/k₀) = ρσ
    
    Args:
        substituents: List of substituent strings (e.g., ['p-OMe', 'p-Cl', 'm-NO2'])
        rho: Reaction constant (ρ). Positive for electron-withdrawing transition
             states, negative for electron-donating transition states.
    
    Returns:
        Dictionary containing:
        - 'results': List of HammettResult objects for each substituent
        - 'summary': Text summary of the analysis
        - 'rho': The reaction constant used
    
    Example:
        >>> result = hammett_analysis(['p-OMe', 'p-Cl', 'm-NO2'], rho=1.0)
        >>> for r in result['results']:
        ...     print(f"{r.substituent}: k/k₀ = {r.k_ratio:.3f}")
    """
    results: List[HammettResult] = []
    unknown_subs: List[str] = []
    
    for sub in substituents:
        sigma = _get_sigma(sub)
        
        if sigma is None:
            unknown_subs.append(sub)
            continue
        
        # Hammett equation: log(k/k₀) = ρσ
        log_k_ratio = rho * sigma
        k_ratio = 10 ** log_k_ratio
        
        # Interpretation
        if rho > 0:
            if sigma > 0:
                interp = "EWG accelerates reaction (positive ρ, positive σ)"
            else:
                interp = "EDG decelerates reaction (positive ρ, negative σ)"
        else:
            if sigma > 0:
                interp = "EWG decelerates reaction (negative ρ, positive σ)"
            else:
                interp = "EDG accelerates reaction (negative ρ, negative σ)"
        
        results.append(HammettResult(
            substituent=sub,
            sigma=sigma,
            log_k_ratio=log_k_ratio,
            k_ratio=k_ratio,
            interpretation=interp
        ))
    
    # Build summary
    summary_lines = [
        f"Hammett Analysis (ρ = {rho})",
        "=" * 40,
    ]
    
    if unknown_subs:
        summary_lines.append(f"Unknown substituents: {', '.join(unknown_subs)}")
        summary_lines.append("")
    
    for r in results:
        summary_lines.append(
            f"{r.substituent:8s} | σ = {r.sigma:+.2f} | "
            f"log(k/k₀) = {r.log_k_ratio:+.3f} | k/k₀ = {r.k_ratio:.3f}"
        )
    
    return {
        "results": results,
        "summary": "\n".join(summary_lines),
        "rho": rho,
        "unknown_substituents": unknown_subs,
    }


@dataclass
class pKaResult:
    """Result from pKa prediction."""
    estimated_pka: float
    confidence: str
    notes: List[str]
    fragments_used: List[str]


def pka_predict(
    structure_fragments: Dict[str, Union[str, List[str]]]
) -> pKaResult:
    """
    Estimate pKa from fragment contributions using Taft/fragment method.
    
    This function uses a simplified fragment-based approach to estimate pKa
    values for organic acids. The method adds substituent contributions to
    a base pKa value.
    
    Args:
        structure_fragments: Dictionary containing:
            - 'base_type': Type of acidic group (e.g., 'carboxylic_acid', 
              'phenol', 'alcohol', 'amine_primary', etc.)
            - 'substituents': List of substituent effects at various positions
              (e.g., ['alpha_alkyl', 'beta_halogen'])
    
    Returns:
        pKaResult object with:
        - estimated_pka: Predicted pKa value
        - confidence: 'high', 'medium', or 'low'
        - notes: List of notes about the prediction
        - fragments_used: List of fragments applied
    
    Example:
        >>> result = pka_predict({
        ...     'base_type': 'carboxylic_acid',
        ...     'substituents': ['alpha_halogen', 'beta_alkyl']
        ... })
        >>> print(f"Predicted pKa: {result.estimated_pka:.1f}")
    """
    notes: List[str] = []
    fragments_used: List[str] = []
    
    base_type = structure_fragments.get("base_type", "carboxylic_acid")
    substituents = structure_fragments.get("substituents", [])
    
    # Get base pKa
    if base_type not in PKA_FRAGMENTS:
        notes.append(f"Unknown base type '{base_type}', using carboxylic_acid default")
        base_type = "carboxylic_acid"
    
    base_pka = PKA_FRAGMENTS[base_type].get("base_pka", 4.76)
    fragments_used.append(f"base: {base_type} (pKa₀ = {base_pka})")
    
    # Apply substituent effects
    pka = base_pka
    for sub in substituents:
        if sub in PKA_FRAGMENTS:
            contribution = PKA_FRAGMENTS[sub]
            pka += contribution
            fragments_used.append(f"{sub}: ΔpKa = {contribution:+.2f}")
        else:
            notes.append(f"Unknown substituent effect: {sub}")
    
    # Determine confidence
    if len(notes) == 0 and len(substituents) <= 3:
        confidence = "high"
    elif len(notes) <= 1:
        confidence = "medium"
    else:
        confidence = "low"
    
    # Add general notes
    notes.append("Fragment method provides estimates; actual values may vary by ±0.5-1.0 pKa units")
    notes.append("Solvent, temperature, and ionic strength effects not included")
    
    return pKaResult(
        estimated_pka=pka,
        confidence=confidence,
        notes=notes,
        fragments_used=fragments_used,
    )


@dataclass
class KIEResult:
    """Result from kinetic isotope effect calculation."""
    kH_kD: float
    kH_kT: Optional[float]
    primary_kie: bool
    tunneling: str
    interpretation: str
    notes: List[str]


def kie_calculate(
    ratio_kh_kd: float,
    ratio_kh_kt: Optional[float] = None
) -> KIEResult:
    """
    Calculate kinetic isotope effect from rate ratios.
    
    Kinetic isotope effects arise from differences in zero-point energy
    between isotopologues. Primary KIEs occur at the bond being broken;
    secondary KIEs occur at bonds not directly involved.
    
    Args:
        ratio_kh_kd: k(H)/k(D) ratio (>1 for normal KIE)
        ratio_kh_kt: Optional k(H)/k(T) ratio
    
    Returns:
        KIEResult object with:
        - kH_kD: The input ratio
        - kH_kT: The T ratio if provided
        - primary_kie: Whether this is a primary KIE
        - tunneling: Assessment of tunneling contribution
        - interpretation: Text interpretation
        - notes: Additional notes
    
    Example:
        >>> result = kie_calculate(7.0, 15.0)
        >>> print(result.interpretation)
    """
    notes: List[str] = []
    
    # Determine if primary or secondary KIE
    # Primary KIE: kH/kD typically 2-7 (can be up to 10+ with tunneling)
    # Secondary KIE: kH/kD typically 1.0-1.5 per hydrogen
    if ratio_kh_kd > 1.5:
        primary_kie = True
        notes.append("Primary KIE indicated (kH/kD > 1.5)")
    else:
        primary_kie = False
        notes.append("Secondary KIE indicated (kH/kD ≤ 1.5)")
    
    # Assess tunneling
    # Swain-Schaad relationship: kH/kT = (kH/kD)^1.44
    # Deviation suggests tunneling
    if ratio_kh_kt is not None:
        expected_kh_kt = ratio_kh_kd ** 1.44
        ratio_deviation = ratio_kh_kt / expected_kh_kt
        
        if ratio_deviation > 1.2:
            tunneling = "significant"
            notes.append(f"Significant tunneling: kH/kT = {ratio_kh_kt:.1f} vs expected {expected_kh_kt:.1f}")
        elif ratio_deviation > 1.05:
            tunneling = "moderate"
            notes.append(f"Moderate tunneling contribution detected")
        else:
            tunneling = "minimal"
            notes.append("Tunneling contribution is minimal")
    else:
        # Estimate from kH/kD alone
        if ratio_kh_kd > 7:
            tunneling = "possible"
            notes.append("kH/kD > 7 suggests possible tunneling contribution")
        elif ratio_kh_kd > 10:
            tunneling = "likely"
            notes.append("kH/kD > 10 indicates likely tunneling")
        else:
            tunneling = "unknown"
            notes.append("Provide kH/kT ratio for tunneling assessment")
    
    # Build interpretation
    if primary_kie:
        if ratio_kh_kd < 2:
            interp = f"Small primary KIE ({ratio_kh_kd:.2f}) - partial C-H bond cleavage in TS or hybridization change"
        elif ratio_kh_kd < 5:
            interp = f"Moderate primary KIE ({ratio_kh_kd:.2f}) - C-H bond largely intact in TS"
        elif ratio_kh_kd < 8:
            interp = f"Large primary KIE ({ratio_kh_kd:.2f}) - significant C-H bond cleavage in TS"
        else:
            interp = f"Very large primary KIE ({ratio_kh_kd:.2f}) - near-complete C-H cleavage; tunneling {tunneling}"
    else:
        interp = f"Secondary KIE ({ratio_kh_kd:.2f}) - rehybridization or steric effects"
    
    return KIEResult(
        kH_kD=ratio_kh_kd,
        kH_kT=ratio_kh_kt,
        primary_kie=primary_kie,
        tunneling=tunneling,
        interpretation=interp,
        notes=notes,
    )


@dataclass
class StereochemistryResult:
    """Result from stereochemical analysis."""
    ring_size: int
    substituents: List[Dict[str, Union[str, float]]]
    a_values_used: Dict[str, float]
    equatorial_preference: float
    equilibrium_constant: float
    most_stable_conformer: str
    diaxial_interactions: List[str]
    notes: List[str]


def stereochemical_analysis(
    ring_size: int,
    substituents: List[Dict[str, str]]
) -> StereochemistryResult:
    """
    Analyze stereochemistry of cyclohexane/cyclopentane conformers.
    
    Calculates A-values (free energy differences between axial and equatorial
    conformers) and determines the most stable conformation.
    
    Args:
        ring_size: 5 for cyclopentane, 6 for cyclohexane
        substituents: List of dicts, each with:
            - 'position': Position number (1-6 for cyclohexane)
            - 'group': Substituent name (e.g., 'Me', 't-Bu', 'OH')
            - 'orientation': 'axial' or 'equatorial' (for one chair form)
    
    Returns:
        StereochemistryResult with:
        - ring_size: Input ring size
        - substituents: Processed substituent data
        - a_values_used: A-values looked up
        - equatorial_preference: Total preference for equatorial (kcal/mol)
        - equilibrium_constant: K_eq between conformers
        - most_stable_conformer: Description of preferred conformation
        - diaxial_interactions: List of 1,3-diaxial interactions
        - notes: Additional notes
    
    Example:
        >>> result = stereochemical_analysis(6, [
        ...     {'position': 1, 'group': 'Me', 'orientation': 'axial'},
        ...     {'position': 4, 'group': 't-Bu', 'orientation': 'equatorial'}
        ... ])
    """
    notes: List[str] = []
    diaxial_interactions: List[str] = []
    a_values_used: Dict[str, float] = {}
    
    if ring_size not in [5, 6]:
        notes.append(f"Ring size {ring_size} not fully supported; using cyclohexane data")
        ring_size = 6
    
    # Calculate total A-value penalty for the given orientation
    total_a_penalty = 0.0
    processed_subs: List[Dict[str, Union[str, float]]] = []
    
    # Track axial positions for 1,3-diaxial interactions
    axial_positions: List[int] = []
    axial_groups: Dict[int, str] = {}
    
    for sub in substituents:
        position = sub.get("position", 1)
        group = sub.get("group", "H")
        orientation = sub.get("orientation", "equatorial")
        
        # Get A-value (default to methyl if unknown)
        a_value = A_VALUES.get(group, 1.7)
        a_values_used[group] = a_value
        
        # If axial, this is a penalty; if equatorial, it's preferred
        if orientation == "axial":
            total_a_penalty += a_value
            axial_positions.append(position)
            axial_groups[position] = group
        
        processed_subs.append({
            "position": position,
            "group": group,
            "orientation": orientation,
            "a_value": a_value,
        })
    
    # Check for 1,3-diaxial interactions (positions 1,3,5 or 2,4,6)
    if ring_size == 6:
        # Chair flip: axial ↔ equatorial
        # 1,3-diaxial: positions separated by 2 (mod 6)
        for i in range(len(axial_positions)):
            for j in range(i + 1, len(axial_positions)):
                pos1, pos2 = axial_positions[i], axial_positions[j]
                # Check if 1,3 relationship (difference of 2 or 4)
                diff = abs(pos1 - pos2)
                if diff == 2 or diff == 4:
                    interaction = f"1,3-Diaxial: positions {pos1} ({axial_groups[pos1]}) and {pos2} ({axial_groups[pos2]})"
                    diaxial_interactions.append(interaction)
                    # Add steric penalty (simplified: 0.9 kcal/mol per interaction)
                    total_a_penalty += 0.9
    
    # Calculate equilibrium constant
    # ΔG = -RT ln(K), so K = exp(-ΔG/RT)
    # At 298K, RT = 0.592 kcal/mol
    RT = 0.592
    delta_G = total_a_penalty
    equilibrium_constant = math.exp(-delta_G / RT)
    
    # Determine most stable conformer
    if total_a_penalty > 0.5:
        most_stable = "Opposite chair (axial → equatorial flip)"
    elif total_a_penalty < -0.5:
        most_stable = "Original chair (equatorial preference maintained)"
    else:
        most_stable = "Both chairs similarly populated"
    
    notes.append(f"Calculated at 298 K (RT = {RT} kcal/mol)")
    
    return StereochemistryResult(
        ring_size=ring_size,
        substituents=processed_subs,
        a_values_used=a_values_used,
        equatorial_preference=total_a_penalty,
        equilibrium_constant=equilibrium_constant,
        most_stable_conformer=most_stable,
        diaxial_interactions=diaxial_interactions,
        notes=notes,
    )


@dataclass
class ReactionDiagram:
    """Result from reaction coordinate diagram generation."""
    ascii_diagram: str
    delta_g_ddagger: Optional[float]
    delta_g_zero: Optional[float]
    species_order: List[str]
    energies: Dict[str, float]


def reaction_coordinate_diagram(
    energies: Dict[str, float]
) -> ReactionDiagram:
    """
    Generate text-based reaction coordinate diagram given energies.
    
    Creates an ASCII representation of a reaction profile showing relative
    energies of reactants, transition states, intermediates, and products.
    
    Args:
        energies: Dictionary mapping species names to energies in kJ/mol.
                  Convention: Include 'TS' or 'transition' in transition state names
                  for proper visualization.
    
    Returns:
        ReactionDiagram with:
        - ascii_diagram: Text-based diagram
        - delta_g_ddagger: Activation energy (barrier height)
        - delta_g_zero: Overall reaction energy
        - species_order: Order of species in diagram
        - energies: Input energies
    
    Example:
        >>> diagram = reaction_coordinate_diagram({
        ...     'Reactants': 0,
        ...     'TS1': 80,
        ...     'Intermediate': 30,
        ...     'TS2': 70,
        ...     'Products': -20
        ... })
        >>> print(diagram.ascii_diagram)
    """
    if not energies:
        return ReactionDiagram(
            ascii_diagram="No energy data provided",
            delta_g_ddagger=None,
            delta_g_zero=None,
            species_order=[],
            energies={},
        )
    
    # Sort species by energy for visualization
    sorted_species = sorted(energies.items(), key=lambda x: x[1])
    min_energy = min(energies.values())
    max_energy = max(energies.values())
    
    # Build ASCII diagram
    # Scale: 2 characters per 10 kJ/mol
    scale = 2 / 10
    
    lines: List[str] = []
    lines.append("Reaction Coordinate Diagram")
    lines.append("=" * 50)
    lines.append("")
    
    # Energy scale
    energy_range = max_energy - min_energy
    num_ticks = min(10, int(energy_range / 20) + 1)
    
    # Create the diagram
    for species, energy in sorted_species:
        # Normalize energy relative to minimum
        rel_energy = energy - min_energy
        bar_length = int(rel_energy * scale)
        bar_length = max(0, min(40, bar_length))  # Cap at 40 chars
        
        bar = "█" * bar_length
        is_ts = "TS" in species.upper() or "TRANSITION" in species.upper()
        
        if is_ts:
            lines.append(f"  {species:15s} |{bar}‡ {energy:+.1f} kJ/mol")
        else:
            lines.append(f"  {species:15s} |{bar}  {energy:+.1f} kJ/mol")
    
    lines.append("")
    lines.append("  Energy (kJ/mol) →")
    
    # Calculate ΔG‡ and ΔG°
    # Assume first entry is reactants, last is products
    species_names = list(energies.keys())
    reactant_energy = energies.get("Reactants", energies.get(species_names[0], 0))
    product_energy = energies.get("Products", energies.get(species_names[-1], 0))
    
    # Find highest energy (transition state)
    ts_energies = [
        (s, e) for s, e in energies.items()
        if "TS" in s.upper() or "TRANSITION" in s.upper()
    ]
    
    if ts_energies:
        highest_ts = max(ts_energies, key=lambda x: x[1])
        delta_g_ddagger = highest_ts[1] - reactant_energy
    else:
        delta_g_ddagger = max_energy - reactant_energy
    
    delta_g_zero = product_energy - reactant_energy
    
    # Add summary
    lines.append("")
    lines.append(f"  ΔG‡ = {delta_g_ddagger:+.1f} kJ/mol (activation energy)")
    lines.append(f"  ΔG° = {delta_g_zero:+.1f} kJ/mol (reaction energy)")
    
    if delta_g_zero < 0:
        lines.append("  Reaction is exergonic (thermodynamically favorable)")
    else:
        lines.append("  Reaction is endergonic (thermodynamically unfavorable)")
    
    return ReactionDiagram(
        ascii_diagram="\n".join(lines),
        delta_g_ddagger=delta_g_ddagger,
        delta_g_zero=delta_g_zero,
        species_order=species_names,
        energies=energies,
    )


@dataclass
class LFERResult:
    """Result from linear free energy relationship analysis."""
    rho: float
    r_squared: float
    fit_quality: str
    predictions: List[Tuple[float, float, float]]  # (sigma, log_k_obs, log_k_pred)
    summary: str


def lferr_analysis(
    data_points: List[Tuple[float, float]]
) -> LFERResult:
    """
    Fit linear free energy relationship (Hammett, Brønsted) to experimental data.
    
    Uses least-squares regression to fit log(k) = ρσ + C (or log(k) = β·pKa + C
    for Brønsted relationships).
    
    Args:
        data_points: List of (σ, log(k)) pairs. For Brønsted plots, use pKa values
                     as the first element instead of σ.
    
    Returns:
        LFERResult with:
        - rho: Slope of the linear fit (reaction constant)
        - r_squared: Coefficient of determination
        - fit_quality: Assessment of fit quality
        - predictions: List of (σ, log_k_observed, log_k_predicted) tuples
        - summary: Text summary of the analysis
    
    Example:
        >>> result = lferr_analysis([
        ...     (-0.27, -0.5),  # p-OMe
        ...     (0.00, 0.0),    # H
        ...     (0.23, 0.4),    # p-Cl
        ...     (0.78, 1.2),    # p-NO2
        ... ])
        >>> print(f"ρ = {result.rho:.2f}, R² = {result.r_squared:.3f}")
    """
    if len(data_points) < 3:
        return LFERResult(
            rho=0.0,
            r_squared=0.0,
            fit_quality="insufficient data",
            predictions=[],
            summary="Need at least 3 data points for regression",
        )
    
    # Extract x (σ) and y (log k) values
    x_values = [p[0] for p in data_points]
    y_values = [p[1] for p in data_points]
    
    n = len(data_points)
    
    # Calculate means
    x_mean = statistics.mean(x_values)
    y_mean = statistics.mean(y_values)
    
    # Calculate slope (ρ) and intercept using least squares
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in data_points)
    denominator = sum((x - x_mean) ** 2 for x in x_values)
    
    if denominator == 0:
        return LFERResult(
            rho=0.0,
            r_squared=0.0,
            fit_quality="degenerate data",
            predictions=[],
            summary="All σ values are identical",
        )
    
    rho = numerator / denominator
    intercept = y_mean - rho * x_mean
    
    # Calculate R²
    y_pred = [rho * x + intercept for x in x_values]
    ss_res = sum((y - y_p) ** 2 for y, y_p in zip(y_values, y_pred))
    ss_tot = sum((y - y_mean) ** 2 for y in y_values)
    
    if ss_tot == 0:
        r_squared = 1.0  # Perfect fit when all y values are the same
    else:
        r_squared = 1 - (ss_res / ss_tot)
    
    # Assess fit quality
    if r_squared >= 0.95:
        fit_quality = "excellent"
    elif r_squared >= 0.90:
        fit_quality = "very good"
    elif r_squared >= 0.80:
        fit_quality = "good"
    elif r_squared >= 0.70:
        fit_quality = "acceptable"
    else:
        fit_quality = "poor"
    
    # Build predictions
    predictions = [
        (x, y, rho * x + intercept)
        for x, y in data_points
    ]
    
    # Build summary
    lines = [
        "Linear Free Energy Relationship Analysis",
        "=" * 45,
        "",
        f"  ρ (slope) = {rho:.3f}",
        f"  intercept = {intercept:.3f}",
        f"  R² = {r_squared:.4f}",
        f"  Fit quality: {fit_quality}",
        "",
        "  Interpretation:",
    ]
    
    if abs(rho) < 0.1:
        lines.append("    - Very small ρ: minimal substituent sensitivity")
    elif abs(rho) < 0.5:
        lines.append("    - Small ρ: modest substituent effects")
    elif abs(rho) < 1.0:
        lines.append("    - Moderate ρ: typical for many reactions")
    elif abs(rho) < 2.0:
        lines.append("    - Large ρ: significant charge development in TS")
    else:
        lines.append("    - Very large ρ: extensive charge development in TS")
    
    if rho > 0:
        lines.append("    - Positive ρ: EWG accelerate, EDG decelerate")
    else:
        lines.append("    - Negative ρ: EDG accelerate, EWG decelerate")
    
    return LFERResult(
        rho=rho,
        r_squared=r_squared,
        fit_quality=fit_quality,
        predictions=predictions,
        summary="\n".join(lines),
    )


@dataclass
class BaldwinResult:
    """Result from Baldwin's rules analysis."""
    ring_size: int
    bond_type: str
    geometry: str
    favored: bool
    notation: str
    rationale: str
    examples: List[str]


def baldwin_rules(
    ring_size: int,
    bond_type: str,
    geometry: str
) -> BaldwinResult:
    """
    Check Baldwin's rules for ring closure.
    
    Baldwin's rules predict whether ring closure reactions are favored based
    on ring size, the hybridization of the electrophilic center, and the
    trajectory of attack (exo vs endo).
    
    Args:
        ring_size: Number of atoms in the forming ring (3-7)
        bond_type: Hybridization of electrophilic center:
                   - 'tet' or 'tetrahedral': sp³ center (e.g., SN2)
                   - 'trig' or 'trigonal': sp² center (e.g., aldol, Michael)
                   - 'dig' or 'digonal': sp center (e.g., alkyne addition)
        geometry: Attack trajectory:
                  - 'exo': External attack (most common)
                  - 'endo': Internal attack
    
    Returns:
        BaldwinResult with:
        - ring_size: Input ring size
        - bond_type: Normalized bond type
        - geometry: Normalized geometry
        - favored: Whether the closure is favored
        - notation: Baldwin notation (e.g., "5-exo-tet")
        - rationale: Explanation of the rule
        - examples: Example reactions
    
    Example:
        >>> result = baldwin_rules(5, 'tet', 'exo')
        >>> print(f"5-exo-tet is {'favored' if result.favored else 'disfavored'}")
    """
    examples: List[str] = []
    
    # Normalize inputs
    ring_size = max(3, min(7, ring_size))  # Clamp to valid range
    
    bond_type_map = {
        "tet": "tet",
        "tetrahedral": "tet",
        "sp3": "tet",
        "trig": "trig",
        "trigonal": "trig",
        "sp2": "trig",
        "dig": "dig",
        "digonal": "dig",
        "sp": "dig",
    }
    bond_type = bond_type_map.get(bond_type.lower(), "tet")
    
    geometry = geometry.lower()
    if geometry not in ["exo", "endo"]:
        geometry = "exo"
    
    # Look up the rule
    favored = False
    if bond_type in BALDWIN_RULES:
        if geometry in BALDWIN_RULES[bond_type]:
            if ring_size in BALDWIN_RULES[bond_type][geometry]:
                result_str = BALDWIN_RULES[bond_type][geometry][ring_size]
                favored = result_str == "fav"
    
    # Build notation
    notation = f"{ring_size}-{geometry}-{bond_type}"
    
    # Generate rationale
    if favored:
        rationale = f"{notation} ring closure is FAVORED by Baldwin's rules."
    else:
        rationale = f"{notation} ring closure is DISFAVORED by Baldwin's rules."
    
    # Add geometric explanation
    if bond_type == "tet":
        if geometry == "exo":
            if ring_size >= 4:
                rationale += " Exo-tet closures require reasonable approach angles that are achievable for rings ≥4."
            else:
                rationale += " 3-exo-tet has severe angle strain."
        else:  # endo
            if ring_size in [3, 6, 7]:
                rationale += " Endo-tet closures require acute approach angles only achievable in certain ring sizes."
            else:
                rationale += " The required approach angle is geometrically difficult."
    
    elif bond_type == "trig":
        if geometry == "exo":
            rationale += " Exo-trig closures are generally favored for all ring sizes."
        else:  # endo
            if ring_size >= 5:
                rationale += " Endo-trig closures become feasible for larger rings."
            else:
                rationale += " Endo-trig requires very acute approach angles."
    
    else:  # dig
        if geometry == "exo":
            if ring_size >= 4:
                rationale += " Exo-dig is favored for rings ≥4 (linear alkyne allows good approach)."
            else:
                rationale += " 3-exo-dig is disfavored due to angle requirements."
        else:  # endo
            rationale += " Endo-dig closures are generally favored (linear sp center accommodates internal attack)."
    
    # Add examples
    if bond_type == "tet" and geometry == "exo":
        if ring_size == 3:
            examples.append("Epoxide formation (rare for this pathway)")
        elif ring_size == 5:
            examples.append("Tetrahydrofuran formation")
        elif ring_size == 6:
            examples.append("Tetrahydropyran formation")
    elif bond_type == "trig" and geometry == "exo":
        if ring_size == 5:
            examples.append("5-membered lactone formation")
            examples.append("Intramolecular aldol (5-ring)")
        elif ring_size == 6:
            examples.append("6-membered lactone formation")
    elif bond_type == "dig":
        examples.append("Nucleophilic addition to alkynes")
    
    return BaldwinResult(
        ring_size=ring_size,
        bond_type=bond_type,
        geometry=geometry,
        favored=favored,
        notation=notation,
        rationale=rationale,
        examples=examples,
    )


@dataclass
class ArrheniusResult:
    """Result from Arrhenius equation calculation."""
    rate_constant: float
    ea_kj: float
    a_factor: float
    temperature: float
    half_life: Optional[float]
    plot_data: List[Tuple[float, float]]
    summary: str


def arrhenius_parameters(
    ea_kj: float,
    a_factor: float,
    temperature: float
) -> ArrheniusResult:
    """
    Calculate rate constant from Arrhenius parameters.
    
    The Arrhenius equation: k = A · exp(-Ea/RT)
    
    Args:
        ea_kj: Activation energy in kJ/mol
        a_factor: Pre-exponential factor (A) in s⁻¹
        temperature: Temperature in Kelvin
    
    Returns:
        ArrheniusResult with:
        - rate_constant: Calculated k value
        - ea_kj: Input activation energy
        - a_factor: Input A factor
        - temperature: Input temperature
        - half_life: Half-life in seconds (for first-order)
        - plot_data: Temperature vs k data for plotting
        - summary: Text summary
    
    Example:
        >>> result = arrhenius_parameters(75.0, 1e13, 298)
        >>> print(f"k = {result.rate_constant:.2e} s⁻¹")
    """
    # Gas constant in kJ/(mol·K)
    R = 0.008314
    
    # Calculate rate constant
    exponent = -ea_kj / (R * temperature)
    k = a_factor * math.exp(exponent)
    
    # Calculate half-life for first-order reaction
    if k > 0:
        half_life = math.log(2) / k
    else:
        half_life = None
    
    # Generate plot data (temperatures around the input)
    plot_data: List[Tuple[float, float]] = []
    for t_offset in range(-50, 51, 10):
        t = temperature + t_offset
        if t > 0:
            k_t = a_factor * math.exp(-ea_kj / (R * t))
            plot_data.append((t, k_t))
    
    # Build summary
    lines = [
        "Arrhenius Equation Analysis",
        "=" * 35,
        "",
        f"  Ea = {ea_kj:.1f} kJ/mol",
        f"  A = {a_factor:.2e} s⁻¹",
        f"  T = {temperature:.1f} K ({temperature - 273.15:.1f} °C)",
        "",
        f"  k = {k:.4e} s⁻¹",
    ]
    
    if half_life is not None:
        if half_life < 1:
            lines.append(f"  t½ = {half_life * 1000:.2f} ms")
        elif half_life < 60:
            lines.append(f"  t½ = {half_life:.2f} s")
        elif half_life < 3600:
            lines.append(f"  t½ = {half_life / 60:.2f} min")
        elif half_life < 86400:
            lines.append(f"  t½ = {half_life / 3600:.2f} h")
        else:
            lines.append(f"  t½ = {half_life / 86400:.2f} days")
    
    lines.append("")
    lines.append("  Interpretation:")
    
    # Interpret Ea
    if ea_kj < 20:
        lines.append("    - Very low Ea: diffusion-controlled or barrierless reaction")
    elif ea_kj < 40:
        lines.append("    - Low Ea: fast reaction even at room temperature")
    elif ea_kj < 80:
        lines.append("    - Moderate Ea: typical for many organic reactions")
    elif ea_kj < 120:
        lines.append("    - High Ea: requires elevated temperature")
    else:
        lines.append("    - Very high Ea: slow reaction, needs high temperature")
    
    # Temperature sensitivity
    # Calculate rate at T+10 to estimate temperature coefficient
    k_plus_10 = a_factor * math.exp(-ea_kj / (R * (temperature + 10)))
    temp_coeff = k_plus_10 / k if k > 0 else 0
    lines.append(f"    - Temperature coefficient (k(T+10)/k(T)): {temp_coeff:.2f}")
    
    return ArrheniusResult(
        rate_constant=k,
        ea_kj=ea_kj,
        a_factor=a_factor,
        temperature=temperature,
        half_life=half_life,
        plot_data=plot_data,
        summary="\n".join(lines),
    )


# =============================================================================
# MODULE SUMMARY
# =============================================================================

__all__ = [
    "hammett_analysis",
    "pka_predict",
    "kie_calculate",
    "stereochemical_analysis",
    "reaction_coordinate_diagram",
    "lferr_analysis",
    "baldwin_rules",
    "arrhenius_parameters",
    "HammettResult",
    "pKaResult",
    "KIEResult",
    "StereochemistryResult",
    "ReactionDiagram",
    "LFERResult",
    "BaldwinResult",
    "ArrheniusResult",
    "HAMMETT_SIGMA",
    "A_VALUES",
    "PKA_FRAGMENTS",
    "BALDWIN_RULES",
]


if __name__ == "__main__":
    # Demo usage
    print("Physical Organic Chemistry Tools")
    print("=" * 50)
    
    # Hammett analysis demo
    print("\n1. Hammett Analysis:")
    result = hammett_analysis(["p-OMe", "p-Cl", "m-NO2"], rho=1.5)
    print(result["summary"])
    
    # KIE demo
    print("\n2. Kinetic Isotope Effect:")
    kie = kie_calculate(6.5, 14.0)
    print(f"  {kie.interpretation}")
    
    # Baldwin rules demo
    print("\n3. Baldwin's Rules:")
    baldwin = baldwin_rules(5, "trig", "exo")
    print(f"  {baldwin.rationale}")
    
    # Arrhenius demo
    print("\n4. Arrhenius Parameters:")
    arrh = arrhenius_parameters(75.0, 1e13, 298)
    print(f"  k = {arrh.rate_constant:.2e} s⁻¹")
