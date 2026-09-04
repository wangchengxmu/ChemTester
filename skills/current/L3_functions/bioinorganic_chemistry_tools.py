"""
Bioinorganic Chemistry Tools - L3 Implementation

Tools for graduate-level bioinorganic chemistry calculations.
Topics: zinc enzymes, calcium signaling, O2 carriers, O2 activation,
electron transfer, nitrogenase/hydrogenase, metal-DNA, medicinal inorganic.

Author: Chemistry Workflow Pass-3 Builder
Date: 2026-03-15
Status: Scaffold - needs implementation
"""
## Solver Instructions (for AI Agent)

# When you encounter bioinorganic chemistry problems (metal enzymes, metalloproteins, O2 carriers, electron transfer), follow this decision tree:

### Step 1: Identify what is given and what is asked
# - **Given**: protein/enzyme name, metal ion, substrate concentration, rate constants, distances, concentrations
# - **Asked**: turnover rate, binding affinity, equilibrium potential, electron transfer rate, saturation fraction

### Step 2: Choose the correct function
# | Problem Type | Function | Key Parameters |
# |---|---|---|
# | Enzyme turnover rate | `carbonic_anhydrase_turnover(k_cat, [S], Km)` | k_cat, [S], Km |
# | Zn water pKa shift | `zinc_water_pka(metal, pH, charge, ligand_type)` | metal, pH, charge |
# | Zn binding constant | `zinc_binding_constant(metal, ligand, pH, denticity, logK_ref)` | metal, ligand, pH |
# | Ca2+ Nernst potential | `calcium_equilibrium_potential(Ca_out, Ca_in, T, z)` | concentrations, temp |
# | Calmodulin saturation | `calmodulin_saturation(Ca_conc, Kd, n_sites)` | [Ca2+], Kd, sites |
# | Ca-ATPase rate | `ca_atpase_rate(Ca_conc, Vmax, Km, ATP_conc)` | substrate levels |
# | O2 saturation (Hill) | `oxygen_saturation_hill(pO2, P50, n_Hill)` | pO2, P50, Hill coeff |
# | Bohr effect | `bohr_effect_shift(pH, temp, pCO2, base_p50, base_pH)` | pH, temp, pCO2 |
# | CO poisoning | `co_poisoning_effect(O2_conc, CO_conc, P50_O2, P50_CO)` | O2, CO conc |
# | O2 reduction potential | `oxygen_reduction_potential(pO2, pH, n, E0)` | pO2, pH, n, Edeg |
# | SOD activity | `sod_activity_rate(O2_minus_conc, k_cat, enzyme_conc)` | substrate, enzyme |
# | Fenton reaction | `fenton_reaction_rate(Fe_conc, H2O2_conc, pH, k)` | Fe, H2O2, pH |
# | Electron transfer (Marcus) | `marcus_et_rate(lambda_reorg, deltaG, V_coupling, T)` | reorg energy, DeltaG |
# | ET distance decay | `et_distance_decay(rate_ref, distance_ref, distance, beta)` | distances, beta |
# | Nitrogenase ATP cost | `nitrogenase_atp_cost(n_moles_N2, efficiency)` | moles N2 |
# | H2 evolution rate | `hydrogen_evolution_rate(catalyst_conc, overpotential, k0, alpha)` | catalyst, η |
# | Fe-S redox potential | `fe_s_redox_potential(cluster_type, pH, reduction_state, mutation)` | cluster, pH |
# | DNA binding | `dna_binding_constant(metal, dna_type, ionic_strength, pH)` | metal, DNA type |
# | Melting temp shift | `melting_temp_shift(metal_conc, Tm_control, Kd, binding_sites)` | metal conc |
# | Zinc finger affinity | `zinc_finger_affinity(peptide_conc, Zn_conc, Kd, n_sites)` | Zn, peptide |
# | Cisplatin aquation | `cisplatin_aquation_rate(pH, Cl_conc, T, k25)` | pH, [Cl-], T |
# | Chelator affinity | `chelator_affinity(metal, chelator, pH, denticity, logK)` | metal, chelator |
# | Radioactivity decay | `radioactivity_decay(half_life, time, initial_activity)` | t½, time |
# | Chelation selectivity | `chelation_selectivity(metal1, metal2, chelator, pH)` | two metals |

### Step 3: Handle special cases
# - pH strongly affects metal binding (use `zinc_binding_constant` or `fe_s_redox_potential`)
# - Cooperative binding requires Hill equation (`oxygen_saturation_hill`)
# - Long-range ET needs distance correction (`et_distance_decay`)
# - CO poisoning is competitive inhibition of O2 binding

### Examples
# 1. **CA turnover**: `carbonic_anhydrase_turnover(k_cat=1e6, S=0.01, Km=0.008)` -> ~555,556 s-1 effective rate
# 2. **Hemoglobin O2 saturation**: `oxygen_saturation_hill(pO2=26, P50=26, n_Hill=2.8)` -> fraction ~0.5
# 3. **Bohr effect**: `bohr_effect_shift(pH=7.2, temp=37, pCO2=40, base_p50=26, base_pH=7.4)` -> P50 increases


import math
from typing import Dict, List, Optional, Tuple, Union

# Physical constants
R = 8.314  # J/(mol·K)
F = 96485  # C/mol
RT_298 = R * 298.15  # J/mol at 25degC

# ============================================================================
# ZINC ENZYMES TOOLS
# ============================================================================

def carbonic_anhydrase_turnover(
    co2_concentration: float,
    enzyme_concentration: float,
    k_cat: float = 1e6,
    K_m: float = 0.01,
    time_seconds: float = 1.0
) -> Dict[str, float]:
    """
    Calculate carbonic anhydrase activity from CO2 hydration rates.
    
    Args:
        co2_concentration: CO2 concentration (M)
        enzyme_concentration: CA concentration (M)
        k_cat: Turnover number (s-1), default 1e6
        K_m: Michaelis constant (M), default 0.01
        time_seconds: Reaction time (s)
    
    Returns:
        Dict with products formed, rate, and turnover achieved
    """
    # Michaelis-Menten kinetics
    rate = k_cat * enzyme_concentration * co2_concentration / (K_m + co2_concentration)
    products = rate * time_seconds
    turnover_achieved = products / enzyme_concentration if enzyme_concentration > 0 else 0
    
    return {
        "rate_mol_per_s": rate,
        "products_mol": products,
        "turnover_achieved": turnover_achieved,
        "fraction_vmax": rate / (k_cat * enzyme_concentration) if enzyme_concentration > 0 else 0
    }


def zinc_water_pka(
    ligand_field: str = "3His",
    metal_charge: int = 2
) -> Dict[str, float]:
    """
    Calculate pKa of Zn-bound water from ligand field.
    
    Args:
        ligand_field: Description of coordinating ligands
        metal_charge: Charge on Zn ion (default 2)
    
    Returns:
        Dict with pKa and depression from free water (pKa = 14.7)
    """
    # Empirical values based on ligand field
    # More electron-donating ligands increase pKa
    ligand_pka = {
        "3His": 7.0,      # Carbonic anhydrase typical
        "4His": 9.0,      # Higher coordination
        "2His1Glu": 7.5,  # Mixed donors
        "3Cys": 8.5,      # Thiolate donors
        "2His1Cys": 7.2,  # Mixed
        "2His1H2O": 8.0,  # Water ligand
    }
    
    pKa = ligand_pka.get(ligand_field, 7.5)  # Default to ~7
    free_water_pka = 14.7
    depression = free_water_pka - pKa
    
    return {
        "pKa": pKa,
        "depression_from_water": depression,
        "ligand_field": ligand_field,
        "interpretation": f"Zn-H2O pKa depressed by {depression:.1f} units from free water"
    }


def zinc_binding_constant(
    inhibition_data: Dict[str, float]
) -> Dict[str, float]:
    """
    Calculate Zn2+ affinity from inhibition data.
    
    Args:
        inhibition_data: Dict with K_i and inhibitor type
    
    Returns:
        Dict with K_d for Zn2+ binding
    """
    K_i = inhibition_data.get("K_i", 0)
    inhibitor_type = inhibition_data.get("type", "competitive")
    
    if K_i <= 0:
        return {"error": "K_i must be positive"}
    
    # For competitive inhibition: K_d ~ K_i
    # For noncompetitive: K_d is related to K_i differently
    if inhibitor_type == "competitive":
        K_d = K_i
    else:
        K_d = K_i  # Simplified approximation
    
    return {
        "K_d_M": K_d,
        "K_a_M_minus_1": 1/K_d if K_d > 0 else float('inf'),
        "log_K_d": math.log10(K_d),
        "inhibition_type": inhibitor_type
    }


# ============================================================================
# CALCIUM SIGNALING TOOLS
# ============================================================================

def calcium_equilibrium_potential(
    ca_out: float,
    ca_in: float,
    temperature: float = 310.15
) -> Dict[str, float]:
    """
    Calculate Ca2+ equilibrium potential from concentration gradient.
    
    Args:
        ca_out: Extracellular [Ca2+] (M)
        ca_in: Intracellular [Ca2+] (M)
        temperature: Temperature (K), default 37degC
    
    Returns:
        Dict with E_Ca in mV and concentration ratio
    """
    if ca_in <= 0 or ca_out <= 0:
        return {"error": "Concentrations must be positive"}
    
    # E_Ca = (RT/2F) * ln([Ca]out/[Ca]in)
    ratio = ca_out / ca_in
    E_Ca = (R * temperature / (2 * F)) * math.log(ratio)  # Volts
    E_Ca_mV = E_Ca * 1000  # Convert to mV
    
    return {
        "E_Ca_V": E_Ca,
        "E_Ca_mV": E_Ca_mV,
        "concentration_ratio": ratio,
        "log_ratio": math.log10(ratio),
        "temperature_K": temperature
    }


def calmodulin_saturation(
    ca_free: float,
    K_d: float = 1e-6,
    hill_n: float = 2.0
) -> Dict[str, float]:
    """
    Calculate fractional saturation of calmodulin.
    
    Args:
        ca_free: Free Ca2+ concentration (M)
        K_d: Dissociation constant (M), default 1 muM
        hill_n: Hill coefficient, default 2.0
    
    Returns:
        Dict with fractional saturation and Ca2+ bound per CaM
    """
    if ca_free < 0:
        return {"error": "Concentration cannot be negative"}
    
    # θ = [Ca]^n / (K_d^n + [Ca]^n)
    K_d_n = K_d ** hill_n
    ca_n = ca_free ** hill_n
    theta = ca_n / (K_d_n + ca_n)
    
    # Calmodulin has 4 binding sites
    ca_bound_per_cam = theta * 4
    
    return {
        "fractional_saturation": theta,
        "ca_bound_per_calmodulin": ca_bound_per_cam,
        "percent_saturation": theta * 100,
        "K_d_M": K_d,
        "hill_coefficient": hill_n
    }


def ca_atpase_rate(
    ca_concentration: float,
    V_max: float,
    K_m: float = 0.5e-6
) -> Dict[str, float]:
    """
    Calculate Ca2+-ATPase activity from ATP hydrolysis rates.
    
    Args:
        ca_concentration: Free Ca2+ concentration (M)
        V_max: Maximum rate (mol/s)
        K_m: Michaelis constant (M), default 0.5 muM
    
    Returns:
        Dict with rate and fraction of V_max
    """
    if ca_concentration < 0:
        return {"error": "Ca concentration cannot be negative"}
    
    # Michaelis-Menten kinetics
    rate = V_max * ca_concentration / (K_m + ca_concentration)
    fraction_vmax = rate / V_max if V_max > 0 else 0
    
    return {
        "rate_mol_per_s": rate,
        "V_max": V_max,
        "fraction_V_max": fraction_vmax,
        "K_m_M": K_m,
        "ca_concentration_M": ca_concentration
    }


# ============================================================================
# DIOXYGEN CARRIERS TOOLS
# ============================================================================

def oxygen_saturation_hill(
    pO2: float,
    P50: float = 26.0,
    hill_n: float = 2.8
) -> Dict[str, float]:
    """
    Calculate O2 saturation from Hill equation.
    
    Args:
        pO2: Oxygen partial pressure (torr)
        P50: pO2 at 50% saturation (torr), default 26
        hill_n: Hill coefficient, default 2.8
    
    Returns:
        Dict with fractional saturation Y
    """
    if pO2 < 0:
        return {"error": "pO2 cannot be negative"}
    
    # Y = pO2^n / (P50^n + pO2^n)
    pO2_n = pO2 ** hill_n
    P50_n = P50 ** hill_n
    Y = pO2_n / (P50_n + pO2_n)
    
    return {
        "fractional_saturation": Y,
        "percent_saturation": Y * 100,
        "pO2_torr": pO2,
        "P50_torr": P50,
        "hill_coefficient": hill_n,
        "interpretation": f"{Y*100:.1f}% saturated at {pO2} torr O2"
    }


def bohr_effect_shift(
    pH_initial: float,
    pH_final: float,
    P50_initial: float = 26.0,
    bohr_coeff: float = -0.5
) -> Dict[str, float]:
    """
    Calculate P50 change with pH (Bohr effect).
    
    Args:
        pH_initial: Initial pH
        pH_final: Final pH
        P50_initial: Initial P50 (torr)
        bohr_coeff: Bohr coefficient, default -0.5
    
    Returns:
        Dict with new P50 and change in O2 affinity
    """
    # d(log P50)/dpH = bohr_coeff
    # log(P50_final/P50_initial) = bohr_coeff * (pH_final - pH_initial)
    delta_pH = pH_final - pH_initial
    log_ratio = bohr_coeff * delta_pH
    P50_final = P50_initial * (10 ** log_ratio)
    
    # Higher P50 = lower affinity
    affinity_change = P50_initial / P50_final
    
    return {
        "P50_initial": P50_initial,
        "P50_final": P50_final,
        "delta_P50": P50_final - P50_initial,
        "delta_pH": delta_pH,
        "affinity_ratio": affinity_change,
        "interpretation": "Lower pH increases P50 (decreases O2 affinity)" if delta_pH < 0 else "Higher pH decreases P50 (increases O2 affinity)"
    }


def co_poisoning_effect(
    co_hb_fraction: float,
    heme_total: float = 1.0
) -> Dict[str, float]:
    """
    Predict O2 saturation reduction from CO-Hb level.
    
    Args:
        co_hb_fraction: Fraction of Hb with CO bound (0-1)
        heme_total: Total heme concentration (normalized to 1)
    
    Returns:
        Dict with available O2 sites and effective O2 capacity
    """
    if co_hb_fraction < 0 or co_hb_fraction > 1:
        return {"error": "CO-Hb fraction must be between 0 and 1"}
    
    # CO binds with 200-250x affinity of O2
    # Each CO blocks one heme site
    available_sites = heme_total * (1 - co_hb_fraction)
    
    # CO also causes left-shift in O2 curve (increases affinity)
    # Effective capacity is further reduced
    effective_capacity = available_sites * 0.85  # Approximate reduction
    
    # Severity classification
    if co_hb_fraction < 0.10:
        severity = "normal"
    elif co_hb_fraction < 0.20:
        severity = "mild poisoning"
    elif co_hb_fraction < 0.30:
        severity = "moderate poisoning"
    elif co_hb_fraction < 0.50:
        severity = "severe poisoning"
    else:
        severity = "life-threatening"
    
    return {
        "co_hb_fraction": co_hb_fraction,
        "available_heme_fraction": available_sites,
        "effective_o2_capacity_fraction": effective_capacity,
        "capacity_reduction_percent": (1 - effective_capacity) * 100,
        "severity": severity
    }


# ============================================================================
# DIOXYGEN ACTIVATION TOOLS
# ============================================================================

def oxygen_reduction_potential(
    reduction_step: str = "full"
) -> Dict[str, float]:
    """
    Calculate E for each O2 reduction step.
    
    Args:
        reduction_step: "superoxide", "peroxide", "water", or "full"
    
    Returns:
        Dict with reduction potential (V vs NHE)
    """
    # O2 reduction potentials
    potentials = {
        "superoxide": {"E_V": -0.33, "reaction": "O2 + e- -> O2*-"},
        "peroxide": {"E_V": 0.94, "reaction": "O2*- + 2H+ + e- -> H2O2"},
        "water": {"E_V": 1.78, "reaction": "H2O2 + 2H+ + 2e- -> 2H2O"},
        "full": {"E_V": 0.815, "reaction": "O2 + 4H+ + 4e- -> 2H2O"}
    }
    
    if reduction_step not in potentials:
        return {"error": f"Unknown step: {reduction_step}. Use: superoxide, peroxide, water, or full"}
    
    result = potentials[reduction_step].copy()
    result["step"] = reduction_step
    result["reference"] = "V vs NHE at pH 0"
    
    return result


def sod_activity_rate(
    sod_concentration: float,
    o2_radical_concentration: float,
    k_cat: float = 2e9
) -> Dict[str, float]:
    """
    Calculate SOD rate from concentration.
    
    Args:
        sod_concentration: SOD concentration (M)
        o2_radical_concentration: O2*- concentration (M)
        k_cat: Rate constant (M-1s-1), default 2e9
    
    Returns:
        Dict with dismutation rate and half-life
    """
    if sod_concentration <= 0 or o2_radical_concentration <= 0:
        return {"error": "Concentrations must be positive"}
    
    # Rate = k_cat * [SOD] * [O2-]
    rate = k_cat * sod_concentration * o2_radical_concentration
    
    # Half-life under pseudo-first-order conditions
    k_obs = k_cat * sod_concentration
    half_life = math.log(2) / k_obs if k_obs > 0 else float('inf')
    
    return {
        "dismutation_rate_M_per_s": rate,
        "k_observed_s_minus_1": k_obs,
        "half_life_s": half_life,
        "diffusion_limited": True,
        "interpretation": f"SOD is diffusion-limited (k={k_cat:.1e} M-1s-1)"
    }


def fenton_reaction_rate(
    fe2_concentration: float,
    h2o2_concentration: float,
    k: float = 76  # M-1s-1 at pH 7
) -> Dict[str, float]:
    """
    Calculate *OH production rate from Fenton reaction.
    
    Args:
        fe2_concentration: Fe2+ concentration (M)
        h2o2_concentration: H2O2 concentration (M)
        k: Rate constant (M-1s-1), default 76
    
    Returns:
        Dict with *OH production rate
    """
    if fe2_concentration < 0 or h2o2_concentration < 0:
        return {"error": "Concentrations cannot be negative"}
    
    # Rate = k * [Fe2+] * [H2O2]
    rate = k * fe2_concentration * h2o2_concentration
    
    return {
        "oh_production_rate_M_per_s": rate,
        "fe2_consumed_M_per_s": rate,
        "h2o2_consumed_M_per_s": rate,
        "rate_constant_M_minus_1_s_minus_1": k,
        "reaction": "Fe2+ + H2O2 -> Fe3+ + *OH + OH-"
    }


# ============================================================================
# ELECTRON TRANSFER TOOLS
# ============================================================================

def marcus_et_rate(
    delta_G: float,  # eV
    lambda_reorg: float,  # eV
    distance: float,  # Angstroms
    beta: float = 1.0,  # Å-1
    k0: float = 1e13,  # s-1
    temperature: float = 298.15
) -> Dict[str, float]:
    """
    Calculate electron transfer rate from Marcus equation.
    
    Args:
        delta_G: Driving force (eV), negative for exergonic
        lambda_reorg: Reorganization energy (eV)
        distance: Edge-to-edge distance (Å)
        beta: Distance decay constant (Å-1)
        k0: Pre-exponential factor (s-1)
        temperature: Temperature (K)
    
    Returns:
        Dict with k_ET and activation energy
    """
    # k_ET = k0 * exp(-beta*r) * exp(-(DeltaG + lambda)2/4lambdaRT)
    # Convert eV to J for calculation
    eV_to_J = 1.602e-19
    delta_G_J = delta_G * eV_to_J
    lambda_J = lambda_reorg * eV_to_J
    RT = R * temperature
    
    # Distance factor
    distance_factor = math.exp(-beta * distance)
    
    # Activation energy from Marcus
    activation_energy = (delta_G_J + lambda_J) ** 2 / (4 * lambda_J)
    activation_factor = math.exp(-activation_energy / RT)
    
    k_ET = k0 * distance_factor * activation_factor
    
    # Check for Marcus inverted region
    in_inverted_region = abs(delta_G) > lambda_reorg
    
    return {
        "k_ET_s_minus_1": k_ET,
        "log_k_ET": math.log10(k_ET) if k_ET > 0 else float('-inf'),
        "activation_energy_eV": activation_energy / eV_to_J,
        "distance_factor": distance_factor,
        "activation_factor": activation_factor,
        "in_inverted_region": in_inverted_region,
        "optimal_driving_force": -lambda_reorg
    }


def et_distance_decay(
    distance: float,
    beta: float = 1.0,
    reference_rate: float = 1e13,
    reference_distance: float = 0
) -> Dict[str, float]:
    """
    Calculate rate from distance and beta.
    
    Args:
        distance: Distance (Å)
        beta: Decay constant (Å-1)
        reference_rate: Rate at reference distance
        reference_distance: Reference distance (Å)
    
    Returns:
        Dict with rate and relative rate
    """
    if distance < 0:
        return {"error": "Distance cannot be negative"}
    
    # k = k_ref * exp(-beta * (r - r_ref))
    distance_diff = distance - reference_distance
    rate = reference_rate * math.exp(-beta * distance_diff)
    relative_rate = rate / reference_rate
    
    # Estimate tunneling limit
    tunneling_limit = 14  # Å
    within_tunneling = distance <= tunneling_limit
    
    return {
        "rate_s_minus_1": rate,
        "log_rate": math.log10(rate) if rate > 0 else float('-inf'),
        "relative_rate": relative_rate,
        "distance_A": distance,
        "beta_A_minus_1": beta,
        "within_tunneling_limit": within_tunneling
    }


# ============================================================================
# NITROGENASE/HYDROGENASE TOOLS
# ============================================================================

def nitrogenase_atp_cost(
    n2_moles: float,
    atp_per_n2: float = 16.0
) -> Dict[str, float]:
    """
    Calculate ATP required for N2 fixation.
    
    Args:
        n2_moles: Moles of N2 to fix
        atp_per_n2: ATP per N2, default 16
    
    Returns:
        Dict with ATP required and NH3 produced
    """
    atp_required = n2_moles * atp_per_n2
    nh3_produced = n2_moles * 2  # 2 NH3 per N2
    
    return {
        "atp_required_mol": atp_required,
        "n2_fixed_mol": n2_moles,
        "nh3_produced_mol": nh3_produced,
        "atp_per_n2": atp_per_n2,
        "atp_per_nh3": atp_required / nh3_produced if nh3_produced > 0 else 0
    }


def hydrogen_evolution_rate(
    hydrogenase_concentration: float,
    substrate_concentration: float,
    k_cat: float,
    K_m: float
) -> Dict[str, float]:
    """
    Calculate H2 production from hydrogenase.
    
    Args:
        hydrogenase_concentration: Enzyme concentration (M)
        substrate_concentration: Substrate concentration (M)
        k_cat: Turnover number (s-1)
        K_m: Michaelis constant (M)
    
    Returns:
        Dict with H2 production rate
    """
    if hydrogenase_concentration < 0 or substrate_concentration < 0:
        return {"error": "Concentrations cannot be negative"}
    if K_m <= 0:
        return {"error": "K_m must be positive"}
    
    # Michaelis-Menten kinetics
    rate = k_cat * hydrogenase_concentration * substrate_concentration / (K_m + substrate_concentration)
    
    # H2 production rate equals the reaction rate
    h2_production_rate = rate
    
    return {
        "h2_production_rate_M_per_s": h2_production_rate,
        "turnover_rate_s_minus_1": k_cat * substrate_concentration / (K_m + substrate_concentration),
        "k_cat": k_cat,
        "K_m_M": K_m,
        "fraction_V_max": substrate_concentration / (K_m + substrate_concentration)
    }


def fe_s_redox_potential(
    cluster_type: str = "Fe4S4",
    oxidation_state: int = 2,
    protein_environment: str = "ferredoxin"
) -> Dict[str, float]:
    """
    Calculate cluster potential from composition.
    
    Args:
        cluster_type: Fe-S cluster type
        oxidation_state: Overall oxidation state
        protein_environment: Protein context
    
    Returns:
        Dict with redox potential (V)
    """
    # Reference potentials for Fe-S clusters
    cluster_potentials = {
        "Fe2S2": {
            "ferredoxin": -400,
            "Rieske": -150
        },
        "Fe3S4": {
            "ferredoxin": -250
        },
        "Fe4S4": {
            "ferredoxin": -400,
            "HiPIP": +350,
            "nitrogenase_Fe": -300
        }
    }
    
    cluster_type_norm = cluster_type.upper().replace("-", "").replace("_", "")
    protein_lower = protein_environment.lower()
    
    # Map normalized cluster names
    cluster_map = {
        "FE2S2": "Fe2S2",
        "FE3S4": "Fe3S4", 
        "FE4S4": "Fe4S4"
    }
    
    cluster_key = cluster_map.get(cluster_type_norm, cluster_type)
    
    if cluster_key not in cluster_potentials:
        return {"error": f"Unknown cluster type: {cluster_type}"}
    
    potentials = cluster_potentials[cluster_key]
    
    # Try to find protein-specific potential
    potential_mV = None
    for protein, pot in potentials.items():
        if protein.lower() in protein_lower or protein_lower in protein.lower():
            potential_mV = pot
            break
    
    if potential_mV is None:
        potential_mV = list(potentials.values())[0]  # Default
    
    potential_V = potential_mV / 1000
    
    return {
        "cluster_type": cluster_key,
        "oxidation_state": oxidation_state,
        "protein_environment": protein_environment,
        "E_V": potential_V,
        "E_mV": potential_mV,
        "reaction": f"[{cluster_key}]^{oxidation_state}+ + e- -> [{cluster_key}]^{oxidation_state}"
    }


# ============================================================================
# METAL-NUCLEIC ACID TOOLS
# ============================================================================

def dna_binding_constant(
    free_dna: float,
    free_metal: float,
    bound_complex: float
) -> Dict[str, float]:
    """
    Calculate DNA binding constant from titration data.
    
    Args:
        free_dna: Free DNA concentration (M)
        free_metal: Free metal concentration (M)
        bound_complex: DNA-metal complex concentration (M)
    
    Returns:
        Dict with K_b and log K_b
    """
    if free_dna <= 0 or free_metal <= 0:
        return {"error": "Free concentrations must be positive"}
    
    # K_b = [DNA-M] / ([DNA][M])
    K_b = bound_complex / (free_dna * free_metal)
    
    # Determine binding mode based on K_b magnitude
    if K_b >= 1e7:
        binding_mode = "strong (likely intercalation or covalent)"
    elif K_b >= 1e5:
        binding_mode = "moderate (likely groove binding)"
    elif K_b >= 1e3:
        binding_mode = "weak (likely electrostatic)"
    else:
        binding_mode = "very weak"
    
    return {
        "K_b_M_minus_1": K_b,
        "log_K_b": math.log10(K_b),
        "binding_mode": binding_mode,
        "delta_G_kJ_per_mol": -RT_298 * math.log(K_b) / 1000
    }


def melting_temp_shift(
    tm_alone: float,
    tm_complex: float,
    binding_constant: float
) -> Dict[str, float]:
    """
    Calculate DeltaT_m from metal binding.
    
    Args:
        tm_alone: DNA melting temperature alone (degC)
        tm_complex: DNA melting temperature with complex (degC)
        binding_constant: Binding constant (M-1)
    
    Returns:
        Dict with DeltaT_m and binding mode prediction
    """
    delta_tm = tm_complex - tm_alone
    
    # Predict binding mode based on DeltaT_m
    if delta_tm > 15:
        binding_mode = "strong intercalation"
    elif delta_tm > 5:
        binding_mode = "intercalation or strong groove binding"
    elif delta_tm > 0:
        binding_mode = "weak binding"
    elif delta_tm > -5:
        binding_mode = "destabilizing binding"
    else:
        binding_mode = "strong destabilization"
    
    return {
        "delta_Tm_C": delta_tm,
        "Tm_alone": tm_alone,
        "Tm_complex": tm_complex,
        "binding_constant_M_minus_1": binding_constant,
        "log_K_b": math.log10(binding_constant) if binding_constant > 0 else None,
        "binding_mode_prediction": binding_mode,
        "stabilization": delta_tm > 0
    }


def zinc_finger_affinity(
    folded_fraction: float,
    zn_free: float
) -> Dict[str, float]:
    """
    Calculate Zn2+ binding affinity for zinc finger.
    
    Args:
        folded_fraction: Fraction of protein folded
        zn_free: Free Zn2+ concentration (M)
    
    Returns:
        Dict with K_d and K_a
    """
    if folded_fraction < 0 or folded_fraction > 1:
        return {"error": "Folded fraction must be between 0 and 1"}
    if zn_free <= 0:
        return {"error": "Zn concentration must be positive"}
    
    # K_a = [folded] / ([unfolded][Zn])
    unfolded_fraction = 1 - folded_fraction
    if unfolded_fraction <= 0:
        return {"error": "Cannot calculate K when fully folded"}
    
    K_a = folded_fraction / (unfolded_fraction * zn_free)
    K_d = 1 / K_a
    
    return {
        "K_a_M_minus_1": K_a,
        "K_d_M": K_d,
        "log_K_a": math.log10(K_a),
        "log_K_d": math.log10(K_d),
        "folded_fraction": folded_fraction,
        "zn_free_M": zn_free
    }


# ============================================================================
# MEDICINAL INORGANIC TOOLS
# ============================================================================

def cisplatin_aquation_rate(
    chloride_concentration: float,
    pH: float = 7.4,
    temperature: float = 310.15
) -> Dict[str, float]:
    """
    Calculate rate of cisplatin activation.
    
    Args:
        chloride_concentration: [Cl-] (M)
        pH: Solution pH
        temperature: Temperature (K)
    
    Returns:
        Dict with aquation rate and half-life
    """
    if chloride_concentration < 0:
        return {"error": "Chloride concentration cannot be negative"}
    
    # Base rate constant at 37degC in low chloride
    k_base = 8e-5  # s-1 (approximate)
    
    # Chloride inhibition: higher [Cl-] slows aquation
    # k_obs = k_base / (1 + K_Cl * [Cl-])
    K_Cl = 100  # M-1 (chloride binding constant)
    k_obs = k_base / (1 + K_Cl * chloride_concentration)
    
    half_life = math.log(2) / k_obs if k_obs > 0 else float('inf')
    
    return {
        "aquation_rate_constant_s_minus_1": k_obs,
        "half_life_s": half_life,
        "half_life_min": half_life / 60,
        "chloride_concentration_M": chloride_concentration,
        "pH": pH,
        "interpretation": f"Aquation half-life: {half_life/60:.1f} min at {chloride_concentration*1000:.1f} mM Cl-"
    }


def chelator_affinity(
    metal: str,
    chelator: str
) -> Dict[str, float]:
    """
    Calculate K_f for metal-chelator complexes.
    
    Args:
        metal: Metal ion name
        chelator: Chelator name
    
    Returns:
        Dict with formation constant and free metal at equilibrium
    """
    # Database of formation constants
    formation_constants = {
        ("Fe3", "deferoxamine"): 1e31,
        ("Fe3", "DFO"): 1e31,
        ("Fe3", "EDTA"): 1e25,
        ("Ca2", "EDTA"): 1e10,
        ("Ca2", "EGTA"): 1e11,
        ("Pb2", "DMSA"): 1e22,
        ("Pb2", "EDTA"): 1e18,
        ("Hg2", "DMPS"): 1e35,
        ("Hg2", "DMSA"): 1e22,
        ("Zn2", "EDTA"): 1e16,
        ("Cu2", "EDTA"): 1e18,
        ("Mg2", "EDTA"): 1e8,
    }
    
    metal_norm = metal.replace("+", "").replace(" ", "").upper()
    chelator_norm = chelator.replace(" ", "").upper()
    
    # Search for match
    K_f = None
    for (m, c), k in formation_constants.items():
        if metal_norm in m.upper() and chelator_norm in c.upper():
            K_f = k
            break
        if m.upper() in metal_norm and c.upper() in chelator_norm:
            K_f = k
            break
    
    if K_f is None:
        return {"error": f"No formation constant data for {metal}-{chelator}"}
    
    return {
        "metal": metal,
        "chelator": chelator,
        "K_f": K_f,
        "log_K_f": math.log10(K_f),
        "K_d_M": 1 / K_f,
        "interpretation": f"Strong chelation: log K_f = {math.log10(K_f):.1f}"
    }


def radioactivity_decay(
    initial_activity: float,  # Ci or Bq
    half_life_hours: float,
    elapsed_hours: float
) -> Dict[str, float]:
    """
    Calculate activity after time t.
    
    Args:
        initial_activity: Initial activity (same units returned)
        half_life_hours: Half-life (hours)
        elapsed_hours: Elapsed time (hours)
    
    Returns:
        Dict with remaining activity and decay fraction
    """
    if half_life_hours <= 0:
        return {"error": "Half-life must be positive"}
    
    # A = A0 * exp(-lambdat), lambda = ln(2)/t1/2
    lam = math.log(2) / half_life_hours
    decay_factor = math.exp(-lam * elapsed_hours)
    remaining_activity = initial_activity * decay_factor
    
    # Number of half-lives
    n_half_lives = elapsed_hours / half_life_hours
    
    return {
        "remaining_activity": remaining_activity,
        "decay_fraction": 1 - decay_factor,
        "n_half_lives": n_half_lives,
        "half_life_hours": half_life_hours,
        "elapsed_hours": elapsed_hours,
        "interpretation": f"{decay_factor*100:.1f}% remaining after {n_half_lives:.2f} half-lives"
    }


def chelation_selectivity(
    chelator: str,
    target_metal: str,
    competing_metal: str
) -> Dict[str, float]:
    """
    Compare chelator affinity for different metals.
    
    Args:
        chelator: Chelator name
        target_metal: Target metal ion
        competing_metal: Competing metal ion
    
    Returns:
        Dict with selectivity ratio
    """
    # Get formation constants for both metals
    result_target = chelator_affinity(target_metal, chelator)
    result_competing = chelator_affinity(competing_metal, chelator)
    
    if "error" in result_target:
        return {"error": f"Target metal: {result_target['error']}"}
    if "error" in result_competing:
        return {"error": f"Competing metal: {result_competing['error']}"}
    
    K_f_target = result_target["K_f"]
    K_f_competing = result_competing["K_f"]
    
    selectivity = K_f_target / K_f_competing
    
    if selectivity > 100:
        selectivity_class = "highly selective"
    elif selectivity > 10:
        selectivity_class = "moderately selective"
    elif selectivity > 0.1:
        selectivity_class = "poor selectivity"
    else:
        selectivity_class = "prefers competing metal"
    
    return {
        "chelator": chelator,
        "target_metal": target_metal,
        "competing_metal": competing_metal,
        "K_f_target": K_f_target,
        "K_f_competing": K_f_competing,
        "selectivity_ratio": selectivity,
        "log_selectivity": math.log10(selectivity),
        "classification": selectivity_class
    }


# ============================================================================
# MODULE STATUS
# ============================================================================

def get_module_status() -> Dict[str, any]:
    """Return status of all functions in this module."""
    all_functions = [
        "carbonic_anhydrase_turnover",
        "zinc_water_pka",
        "zinc_binding_constant",
        "calcium_equilibrium_potential",
        "calmodulin_saturation",
        "ca_atpase_rate",
        "oxygen_saturation_hill",
        "bohr_effect_shift",
        "co_poisoning_effect",
        "oxygen_reduction_potential",
        "sod_activity_rate",
        "fenton_reaction_rate",
        "marcus_et_rate",
        "et_distance_decay",
        "nitrogenase_atp_cost",
        "hydrogen_evolution_rate",
        "fe_s_redox_potential",
        "dna_binding_constant",
        "melting_temp_shift",
        "zinc_finger_affinity",
        "cisplatin_aquation_rate",
        "chelator_affinity",
        "radioactivity_decay",
        "chelation_selectivity"
    ]
    
    implemented = all_functions  # All 24 functions now implemented
    
    return {
        "module": "bioinorganic_chemistry_tools",
        "total_functions": len(all_functions),
        "functions": all_functions,
        "status": "complete",
        "implemented": len(implemented),
        "pending": 0,
        "implemented_list": implemented,
        "pending_list": []
    }


# MCP Tool Declarations
MCP_TOOLS = [
    {
        "name": "bohr_effect_shift",
        "description": "Calculate P50 change with pH (Bohr effect).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pH_initial": {
                    "type": "number",
                    "description": "Ph Initial"
                },
                "pH_final": {
                    "type": "number",
                    "description": "Ph Final"
                },
                "P50_initial": {
                    "type": "number",
                    "description": "P50 Initial",
                    "default": 26.0
                },
                "bohr_coeff": {
                    "type": "number",
                    "description": "Bohr Coeff",
                    "default": -0.5
                }
            },
            "required": [
                "pH_initial",
                "pH_final"
            ]
        }
    },
    {
        "name": "ca_atpase_rate",
        "description": "Calculate Ca2+-ATPase activity from ATP hydrolysis rates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ca_concentration": {
                    "type": "number",
                    "description": "Ca Concentration"
                },
                "V_max": {
                    "type": "number",
                    "description": "V Max"
                },
                "K_m": {
                    "type": "number",
                    "description": "K M",
                    "default": 5e-07
                }
            },
            "required": [
                "ca_concentration",
                "V_max"
            ]
        }
    },
    {
        "name": "calcium_equilibrium_potential",
        "description": "Calculate Ca2+ equilibrium potential from concentration gradient.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ca_out": {
                    "type": "number",
                    "description": "Ca Out"
                },
                "ca_in": {
                    "type": "number",
                    "description": "Ca In"
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 310.15
                }
            },
            "required": [
                "ca_out",
                "ca_in"
            ]
        }
    },
    {
        "name": "calmodulin_saturation",
        "description": "Calculate fractional saturation of calmodulin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ca_free": {
                    "type": "number",
                    "description": "Ca Free"
                },
                "K_d": {
                    "type": "number",
                    "description": "K D",
                    "default": 1e-06
                },
                "hill_n": {
                    "type": "number",
                    "description": "Hill N",
                    "default": 2.0
                }
            },
            "required": [
                "ca_free"
            ]
        }
    },
    {
        "name": "carbonic_anhydrase_turnover",
        "description": "Calculate carbonic anhydrase activity from CO2 hydration rates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "co2_concentration": {
                    "type": "number",
                    "description": "Co2 Concentration"
                },
                "enzyme_concentration": {
                    "type": "number",
                    "description": "Enzyme Concentration"
                },
                "k_cat": {
                    "type": "number",
                    "description": "K Cat",
                    "default": 1000000.0
                },
                "K_m": {
                    "type": "number",
                    "description": "K M",
                    "default": 0.01
                },
                "time_seconds": {
                    "type": "number",
                    "description": "Time Seconds",
                    "default": 1.0
                }
            },
            "required": [
                "co2_concentration",
                "enzyme_concentration"
            ]
        }
    },
    {
        "name": "chelation_selectivity",
        "description": "Compare chelator affinity for different metals.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "chelator": {
                    "type": "number",
                    "description": "Chelator"
                },
                "target_metal": {
                    "type": "number",
                    "description": "Target Metal"
                },
                "competing_metal": {
                    "type": "number",
                    "description": "Competing Metal"
                }
            },
            "required": [
                "chelator",
                "target_metal",
                "competing_metal"
            ]
        }
    },
    {
        "name": "chelator_affinity",
        "description": "Calculate K_f for metal-chelator complexes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "metal": {
                    "type": "number",
                    "description": "Metal"
                },
                "chelator": {
                    "type": "number",
                    "description": "Chelator"
                }
            },
            "required": [
                "metal",
                "chelator"
            ]
        }
    },
    {
        "name": "cisplatin_aquation_rate",
        "description": "Calculate rate of cisplatin activation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "chloride_concentration": {
                    "type": "number",
                    "description": "Chloride Concentration"
                },
                "pH": {
                    "type": "number",
                    "description": "Ph",
                    "default": 7.4
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 310.15
                }
            },
            "required": [
                "chloride_concentration"
            ]
        }
    },
    {
        "name": "co_poisoning_effect",
        "description": "Predict O2 saturation reduction from CO-Hb level.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "co_hb_fraction": {
                    "type": "number",
                    "description": "Co Hb Fraction"
                },
                "heme_total": {
                    "type": "number",
                    "description": "Heme Total",
                    "default": 1.0
                }
            },
            "required": [
                "co_hb_fraction"
            ]
        }
    },
    {
        "name": "dna_binding_constant",
        "description": "Calculate DNA binding constant from titration data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "free_dna": {
                    "type": "number",
                    "description": "Free Dna"
                },
                "free_metal": {
                    "type": "number",
                    "description": "Free Metal"
                },
                "bound_complex": {
                    "type": "number",
                    "description": "Bound Complex"
                }
            },
            "required": [
                "free_dna",
                "free_metal",
                "bound_complex"
            ]
        }
    },
    {
        "name": "et_distance_decay",
        "description": "Calculate rate from distance and beta.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "distance": {
                    "type": "number",
                    "description": "Distance"
                },
                "beta": {
                    "type": "number",
                    "description": "Beta",
                    "default": 1.0
                },
                "reference_rate": {
                    "type": "number",
                    "description": "Reference Rate",
                    "default": 10000000000000.0
                },
                "reference_distance": {
                    "type": "number",
                    "description": "Reference Distance",
                    "default": 0
                }
            },
            "required": [
                "distance"
            ]
        }
    },
    {
        "name": "fe_s_redox_potential",
        "description": "Calculate cluster potential from composition.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "cluster_type": {
                    "type": "number",
                    "description": "Cluster Type",
                    "default": "Fe4S4"
                },
                "oxidation_state": {
                    "type": "number",
                    "description": "Oxidation State",
                    "default": 2
                },
                "protein_environment": {
                    "type": "number",
                    "description": "Protein Environment",
                    "default": "ferredoxin"
                }
            },
            "required": []
        }
    },
    {
        "name": "fenton_reaction_rate",
        "description": "Calculate *OH production rate from Fenton reaction.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "fe2_concentration": {
                    "type": "number",
                    "description": "Fe2 Concentration"
                },
                "h2o2_concentration": {
                    "type": "number",
                    "description": "H2O2 Concentration"
                },
                "k": {
                    "type": "number",
                    "description": "K",
                    "default": 76
                }
            },
            "required": [
                "fe2_concentration",
                "h2o2_concentration"
            ]
        }
    },
    {
        "name": "get_module_status",
        "description": "Return status of all functions in this module.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "hydrogen_evolution_rate",
        "description": "Calculate H2 production from hydrogenase.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hydrogenase_concentration": {
                    "type": "number",
                    "description": "Hydrogenase Concentration"
                },
                "substrate_concentration": {
                    "type": "number",
                    "description": "Substrate Concentration"
                },
                "k_cat": {
                    "type": "number",
                    "description": "K Cat"
                },
                "K_m": {
                    "type": "number",
                    "description": "K M"
                }
            },
            "required": [
                "hydrogenase_concentration",
                "substrate_concentration",
                "k_cat",
                "K_m"
            ]
        }
    },
    {
        "name": "marcus_et_rate",
        "description": "Calculate electron transfer rate from Marcus equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delta_G": {
                    "type": "number",
                    "description": "Delta G"
                },
                "lambda_reorg": {
                    "type": "number",
                    "description": "Lambda Reorg"
                },
                "distance": {
                    "type": "number",
                    "description": "Distance"
                },
                "beta": {
                    "type": "number",
                    "description": "Beta",
                    "default": 1.0
                },
                "k0": {
                    "type": "number",
                    "description": "K0",
                    "default": 10000000000000.0
                },
                "temperature": {
                    "type": "number",
                    "description": "Temperature",
                    "default": 298.15
                }
            },
            "required": [
                "delta_G",
                "lambda_reorg",
                "distance"
            ]
        }
    },
    {
        "name": "melting_temp_shift",
        "description": "Calculate DeltaT_m from metal binding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tm_alone": {
                    "type": "number",
                    "description": "Tm Alone"
                },
                "tm_complex": {
                    "type": "number",
                    "description": "Tm Complex"
                },
                "binding_constant": {
                    "type": "number",
                    "description": "Binding Constant"
                }
            },
            "required": [
                "tm_alone",
                "tm_complex",
                "binding_constant"
            ]
        }
    },
    {
        "name": "nitrogenase_atp_cost",
        "description": "Calculate ATP required for N2 fixation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "n2_moles": {
                    "type": "number",
                    "description": "N2 Moles"
                },
                "atp_per_n2": {
                    "type": "number",
                    "description": "Atp Per N2",
                    "default": 16.0
                }
            },
            "required": [
                "n2_moles"
            ]
        }
    },
    {
        "name": "oxygen_reduction_potential",
        "description": "Calculate E for each O2 reduction step.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "reduction_step": {
                    "type": "number",
                    "description": "Reduction Step",
                    "default": "full"
                }
            },
            "required": []
        }
    },
    {
        "name": "oxygen_saturation_hill",
        "description": "Calculate O2 saturation from Hill equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pO2": {
                    "type": "number",
                    "description": "Po2"
                },
                "P50": {
                    "type": "number",
                    "description": "P50",
                    "default": 26.0
                },
                "hill_n": {
                    "type": "number",
                    "description": "Hill N",
                    "default": 2.8
                }
            },
            "required": [
                "pO2"
            ]
        }
    },
    {
        "name": "radioactivity_decay",
        "description": "Calculate activity after time t.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "initial_activity": {
                    "type": "number",
                    "description": "Initial Activity"
                },
                "half_life_hours": {
                    "type": "number",
                    "description": "Half Life Hours"
                },
                "elapsed_hours": {
                    "type": "number",
                    "description": "Elapsed Hours"
                }
            },
            "required": [
                "initial_activity",
                "half_life_hours",
                "elapsed_hours"
            ]
        }
    },
    {
        "name": "sod_activity_rate",
        "description": "Calculate SOD rate from concentration.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sod_concentration": {
                    "type": "number",
                    "description": "Sod Concentration"
                },
                "o2_radical_concentration": {
                    "type": "number",
                    "description": "O2 Radical Concentration"
                },
                "k_cat": {
                    "type": "number",
                    "description": "K Cat",
                    "default": 2000000000.0
                }
            },
            "required": [
                "sod_concentration",
                "o2_radical_concentration"
            ]
        }
    },
    {
        "name": "zinc_binding_constant",
        "description": "Calculate Zn2+ affinity from inhibition data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "inhibition_data": {
                    "type": "number",
                    "description": "Inhibition Data"
                }
            },
            "required": [
                "inhibition_data"
            ]
        }
    },
    {
        "name": "zinc_finger_affinity",
        "description": "Calculate Zn2+ binding affinity for zinc finger.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "folded_fraction": {
                    "type": "number",
                    "description": "Folded Fraction"
                },
                "zn_free": {
                    "type": "number",
                    "description": "Zn Free"
                }
            },
            "required": [
                "folded_fraction",
                "zn_free"
            ]
        }
    },
    {
        "name": "zinc_water_pka",
        "description": "Calculate pKa of Zn-bound water from ligand field.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ligand_field": {
                    "type": "number",
                    "description": "Ligand Field",
                    "default": "3His"
                },
                "metal_charge": {
                    "type": "number",
                    "description": "Metal Charge",
                    "default": 2
                }
            },
            "required": []
        }
    }
]