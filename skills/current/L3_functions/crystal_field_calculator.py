"""
Crystal Field Theory Calculator

Calculates LFSE, spin states, and magnetic moments for transition metal complexes.

Source: CHM 320 Chapter 7 (LibreTexts)
Related: L2_principles/crystal_field_theory.md
"""

from dataclasses import dataclass
from typing import Tuple, Optional, Literal
import math

# Spectrochemical series (weak to strong field)
SPECTROCHEMICAL_SERIES = [
    "I-", "Br-", "S2-", "SCN-", "Cl-", "NO3-", "N3-", "F-", "OH-", "C2O4^2-",
    "H2O", "NCS-", "CH3CN", "py", "NH3", "en", "bipy", "phen", "NO2-", "PPh3", "CN-", "CO"
]

# Typical Δ_o values (cm^-1) for common complexes
DELTA_O_VALUES = {
    # [metal(H2O)6] complexes
    ("Ti", 3): 20300,
    ("V", 2): 12600, ("V", 3): 18900,
    ("Cr", 2): 13900, ("Cr", 3): 17400,
    ("Mn", 2): 8500, ("Mn", 3): 21000,
    ("Fe", 2): 10400, ("Fe", 3): 14300,
    ("Co", 2): 9300, ("Co", 3): 27000,
    ("Ni", 2): 8500,
    # Strong field ligands
    ("Fe", 2, "CN"): 32800,
    ("Fe", 3, "CN"): 35000,
    ("Co", 3, "CN"): 34800,
    ("Co", 3, "NH3"): 22900,
    ("Cr", 3, "NH3"): 21500,
    ("Cr", 3, "CN"): 26600,
}

# Pairing energies (cm^-1)
PAIRING_ENERGIES = {
    ("Cr", 2): 23500,
    ("Mn", 2): 28000, ("Mn", 3): 28000,
    ("Fe", 2): 17600, ("Fe", 3): 30000,
    ("Co", 2): 22500, ("Co", 3): 21000,
}


@dataclass
class CoordinationComplex:
    """Represents a transition metal coordination complex."""
    metal: str
    oxidation_state: int
    geometry: Literal["octahedral", "tetrahedral", "square_planar"] = "octahedral"
    ligand_field_strength: Optional[str] = None  # "weak", "intermediate", "strong"
    delta_o: Optional[float] = None  # in cm^-1

    @property
    def d_electron_count(self) -> int:
        """Calculate the number of d-electrons."""
        # Common transition metals and their group numbers
        group_numbers = {
            "Sc": 3, "Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10,
            "Cu": 11, "Zn": 12, "Y": 3, "Zr": 4, "Nb": 5, "Mo": 6, "Tc": 7, "Ru": 8,
            "Rh": 9, "Pd": 10, "Ag": 11, "Cd": 12, "Hf": 4, "Ta": 5, "W": 6, "Re": 7,
            "Os": 8, "Ir": 9, "Pt": 10, "Au": 11, "Hg": 12
        }
        group = group_numbers.get(self.metal, 0)
        d_count = group - self.oxidation_state
        # Handle cases where oxidation removes s-electrons first
        return max(0, min(10, d_count))


def calculate_lfse(
    d_electrons: int,
    geometry: str = "octahedral",
    spin_state: str = "high",
    delta_o: float = None
) -> dict:
    """
    Calculate Ligand Field Stabilization Energy.

    Args:
        d_electrons: Number of d-electrons (0-10)
        geometry: "octahedral", "tetrahedral", or "square_planar"
        spin_state: "high" or "low"
        delta_o: Crystal field splitting in cm^-1 (optional, for numerical result)

    Returns:
        Dictionary with LFSE information
    """
    if geometry == "octahedral":
        return _lfse_octahedral(d_electrons, spin_state, delta_o)
    elif geometry == "tetrahedral":
        return _lfse_tetrahedral(d_electrons, delta_o)
    else:
        raise ValueError(f"Geometry {geometry} not yet implemented")


def _lfse_octahedral(d_electrons: int, spin_state: str, delta_o: float = None) -> dict:
    """Calculate LFSE for octahedral complexes."""

    # Electron distributions for high-spin and low-spin
    if spin_state == "high":
        configs = {
            0: (0, 0, 0), 1: (0, 1, 0), 2: (0, 2, 0), 3: (0, 3, 0),
            4: (0, 3, 1), 5: (0, 3, 2), 6: (0, 4, 2), 7: (0, 5, 2),
            8: (0, 6, 2), 9: (0, 6, 3), 10: (0, 6, 4)
        }
    else:  # low-spin
        configs = {
            0: (0, 0, 0), 1: (0, 1, 0), 2: (0, 2, 0), 3: (0, 3, 0),
            4: (1, 4, 0), 5: (2, 5, 0), 6: (3, 6, 0), 7: (3, 6, 1),
            8: (0, 6, 2), 9: (0, 6, 3), 10: (0, 6, 4)
        }

    pairs, t2g, eg = configs.get(d_electrons, (0, 0, 0))

    # LFSE formula: [(0.6 × eg) - (0.4 × t2g)] × Δ_o
    # Note: this is the destabilization, so we negate for stabilization
    lfse_coeff = -0.4 * t2g + 0.6 * eg  # This gives negative (stabilizing)

    result = {
        "t2g_electrons": t2g,
        "eg_electrons": eg,
        "electron_pairs": pairs,
        "lfse_coefficient": lfse_coeff,
        "configuration": f"t2g^{t2g} eg^{eg}",
        "unpaired_electrons": _count_unpaired(d_electrons, spin_state, "octahedral")
    }

    if delta_o is not None:
        result["lfse_cm-1"] = lfse_coeff * delta_o
        result["lfse_kJ_mol"] = lfse_coeff * delta_o * 0.01196

    return result


def _lfse_tetrahedral(d_electrons: int, delta_t: float = None) -> dict:
    """Calculate LFSE for tetrahedral complexes (always high-spin)."""

    # Tetrahedral: e (lower) and t2 (higher)
    # Δ_t ≈ 4/9 Δ_o, and it's always high-spin due to small splitting
    configs = {
        0: (0, 0, 0), 1: (0, 1, 0), 2: (0, 2, 0), 3: (1, 2, 0),
        4: (2, 2, 0), 5: (2, 2, 1), 6: (2, 2, 2), 7: (2, 3, 2),
        8: (2, 4, 2), 9: (2, 4, 3), 10: (2, 4, 4)
    }

    pairs, e, t2 = configs.get(d_electrons, (0, 0, 0))

    # LFSE formula for tetrahedral: [(0.6 × t2) - (0.4 × e)] × Δ_t
    lfse_coeff = -0.6 * t2 + 0.4 * e

    result = {
        "e_electrons": e,
        "t2_electrons": t2,
        "electron_pairs": pairs,
        "lfse_coefficient": lfse_coeff,
        "configuration": f"e^{e} t2^{t2}",
        "unpaired_electrons": _count_unpaired(d_electrons, "high", "tetrahedral")
    }

    if delta_t is not None:
        result["lfse_cm-1"] = lfse_coeff * delta_t
        result["lfse_kJ_mol"] = lfse_coeff * delta_t * 0.01196

    return result


def _count_unpaired(d_electrons: int, spin_state: str, geometry: str) -> int:
    """Count unpaired electrons."""

    if geometry == "octahedral":
        if spin_state == "high":
            unpaired = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1, 10: 0}
        else:
            unpaired = {0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 1, 6: 0, 7: 1, 8: 2, 9: 1, 10: 0}
    else:  # tetrahedral - always high-spin
        unpaired = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1, 10: 0}

    return unpaired.get(d_electrons, 0)


def calculate_magnetic_moment(unpaired_electrons: int, spin_only: bool = True) -> dict:
    """
    Calculate the magnetic moment.

    Args:
        unpaired_electrons: Number of unpaired electrons
        spin_only: If True, use spin-only formula; if False, include orbital contribution

    Returns:
        Dictionary with magnetic moment information
    """
    n = unpaired_electrons

    # Spin-only formula: μ_eff = √(n(n+2)) μ_B
    spin_only_moment = math.sqrt(n * (n + 2)) if n > 0 else 0

    result = {
        "unpaired_electrons": n,
        "spin_only_moment_muB": round(spin_only_moment, 2),
        "spin_only_formula": f"√({n}({n}+2)) = √({n*(n+2)})",
        "magnetic_type": "diamagnetic" if n == 0 else "paramagnetic"
    }

    # Include observed ranges for first-row transition metals
    observed_ranges = {
        1: (1.7, 2.2), 2: (2.8, 3.5), 3: (3.8, 4.5),
        4: (4.8, 5.5), 5: (5.8, 6.5)
    }
    if n in observed_ranges:
        result["observed_range_muB"] = observed_ranges[n]

    return result


def predict_spin_state(
    metal: str,
    oxidation_state: int,
    ligand: str,
    d_electrons: int = None
) -> dict:
    """
    Predict high-spin vs low-spin based on metal and ligand.

    Args:
        metal: Metal symbol
        oxidation_state: Oxidation state of metal
        ligand: Ligand name
        d_electrons: Optional, will be calculated if not provided

    Returns:
        Dictionary with spin state prediction
    """
    if d_electrons is None:
        d_electrons = CoordinationComplex(metal, oxidation_state).d_electron_count

    # d^4, d^5, d^6, d^7 can have different spin states
    spin_state_critical = d_electrons in [4, 5, 6, 7]

    # Metal period affects spin state
    period = _get_period(metal)
    is_4d_or_5d = period >= 5

    # Ligand field strength
    ligand_strength = _get_ligand_strength(ligand)

    # Prediction logic
    if is_4d_or_5d:
        predicted_spin = "low"
        reason = "4d/5d metals are almost always low-spin"
    elif not spin_state_critical:
        predicted_spin = "N/A"
        reason = f"d^{d_electrons} has no spin state ambiguity"
    elif oxidation_state >= 3:
        if ligand_strength == "weak":
            predicted_spin = "high"
            reason = "High oxidation state with weak field ligand"
        else:
            predicted_spin = "low"
            reason = "High oxidation state favors low-spin"
    else:  # oxidation_state < 3
        if ligand_strength == "strong":
            predicted_spin = "low"
            reason = "Strong field ligand favors low-spin"
        else:
            predicted_spin = "high"
            reason = "Weak/intermediate field with low oxidation state favors high-spin"

    return {
        "d_electrons": d_electrons,
        "spin_state_critical": spin_state_critical,
        "metal_period": period,
        "is_4d_or_5d": is_4d_or_5d,
        "ligand_strength": ligand_strength,
        "predicted_spin_state": predicted_spin,
        "reason": reason
    }


def _get_period(metal: str) -> int:
    """Get the period of a transition metal."""
    period_map = {
        "Sc": 4, "Ti": 4, "V": 4, "Cr": 4, "Mn": 4, "Fe": 4, "Co": 4, "Ni": 4, "Cu": 4, "Zn": 4,
        "Y": 5, "Zr": 5, "Nb": 5, "Mo": 5, "Tc": 5, "Ru": 5, "Rh": 5, "Pd": 5, "Ag": 5, "Cd": 5,
        "Hf": 6, "Ta": 6, "W": 6, "Re": 6, "Os": 6, "Ir": 6, "Pt": 6, "Au": 6, "Hg": 6
    }
    return period_map.get(metal, 4)


def _get_ligand_strength(ligand: str) -> str:
    """Determine ligand field strength."""
    weak_ligands = ["I-", "Br-", "S2-", "SCN-", "Cl-", "F-", "OH-", "H2O"]
    strong_ligands = ["CN-", "CO", "NO2-", "PPh3"]

    ligand_lower = ligand.lower().replace(" ", "")

    for strong in strong_ligands:
        if strong.lower() in ligand_lower:
            return "strong"

    for weak in weak_ligands:
        if weak.lower() in ligand_lower:
            return "weak"

    return "intermediate"


def wavelength_to_delta_o(wavelength_nm: float) -> float:
    """
    Convert absorption wavelength to Δ_o.

    Args:
        wavelength_nm: Wavelength in nanometers

    Returns:
        Δ_o in cm^-1
    """
    return 1e7 / wavelength_nm


def delta_o_to_wavelength(delta_o_cm: float) -> float:
    """
    Convert Δ_o to absorption wavelength.

    Args:
        delta_o_cm: Δ_o in cm^-1

    Returns:
        Wavelength in nm
    """
    return 1e7 / delta_o_cm


# Example usage
if __name__ == "__main__":
    # Example 1: LFSE for high-spin Fe(II)
    print("=== Example 1: High-spin Fe(II) ===")
    result = calculate_lfse(6, "octahedral", "high", delta_o=10400)
    print(f"Configuration: {result['configuration']}")
    print(f"LFSE coefficient: {result['lfse_coefficient']} Δ_o")
    print(f"LFSE: {result.get('lfse_cm-1', 'N/A')} cm^-1")
    print(f"Unpaired electrons: {result['unpaired_electrons']}")
    print()

    # Example 2: Magnetic moment
    print("=== Example 2: Magnetic moment for 4 unpaired electrons ===")
    mag = calculate_magnetic_moment(4)
    print(f"Magnetic moment: {mag['spin_only_moment_muB']} μ_B")
    print(f"Type: {mag['magnetic_type']}")
    print()

    # Example 3: Spin state prediction
    print("=== Example 3: Spin state prediction for [Fe(CN)6]4- ===")
    pred = predict_spin_state("Fe", 2, "CN-")
    print(f"Predicted: {pred['predicted_spin_state']}")
    print(f"Reason: {pred['reason']}")
    print()

    # Example 4: Wavelength conversion
    print("=== Example 4: Δ_o from 500 nm absorption ===")
    delta = wavelength_to_delta_o(500)
    print(f"Δ_o = {delta:.0f} cm^-1")
