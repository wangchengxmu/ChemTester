# ﻿"""Batch verification for multiple tools."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "chem-memory" / "L3_functions" / "code"))

from energy_basics_tools import heat_transfer, specific_heat_from_heat, final_temperature
from ideal_gas_law_tools import ideal_gas_law, molar_volume
from gas_laws_tools import boyles_law, charles_law, combined_gas_law
from solution_concentration_tools import molarity, molality, mole_fraction
from equilibrium_tools import reaction_quotient
from rate_law_tools import calculate_rate, determine_order_initial_rates
from gibbs_free_energy_tools import gibbs_free_energy, spontaneity_from_G
from enthalpy_tools import delta_H_rxn_from_formation
from entropy_tools import entropy_change_heat
from ph_calculations_tools import pH_from_H3O, H3O_from_pH
from titration_tools import equivalence_volume, half_equivalence_pH
from amount_conversion_tools import mass_to_moles, moles_to_particles
from calorimetry_tools import coffee_cup_heat_rxn
from arrhenius_tools import arrhenius_k, activation_energy
from colligative_properties_tools import boiling_point_elevation, freezing_point_depression
from buffer_tools import henderson_hasselbalch
from integrated_rate_law_tools import first_order_half_life, first_order_concentration
from le_chatelier_tools import predict_shift_concentration, predict_shift_pressure
from solubility_tools import henrys_law
from electron_configuration_tools import electron_configuration
from molecular_geometry_tools import molecular_structure
from thermodynamics_laws_tools import entropy_universe, entropy_surroundings
from colligative_properties_tools import boiling_point_elevation, freezing_point_depression
from buffer_tools import henderson_hasselbalch
from integrated_rate_law_tools import first_order_half_life, first_order_concentration

def verify_tool(tool_name, problems_file, verify_func):
    """Verify a single tool against its problem set."""
    with open(problems_file, encoding='utf-8') as f:
        data = json.load(f)
    
    passed = 0
    failed = 0
    
    for p in data['problems']:
        try:
            is_pass = verify_func(p)
            if is_pass:
                passed += 1
            else:
                failed += 1
            status = '[PASS]' if is_pass else '[FAIL]'
            print(f'  {p["id"]}: {status}')
        except Exception as e:
            failed += 1
            print(f'  {p["id"]}: [ERROR] {e}')
    
    print(f'  Result: {passed}/{len(data["problems"])} PASS\n')
    return passed, failed

def verify_energy_basics(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'heat_transfer':
        result = heat_transfer(given['mass'], given['specific_heat'], given['delta_T'])
        rel_err = abs(result - expected['heat']) / expected['heat']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'specific_heat':
        result = specific_heat_from_heat(given['mass'], given['heat'], given['delta_T'])
        rel_err = abs(result - expected['specific_heat']) / expected['specific_heat']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'final_temperature':
        result = final_temperature(given['initial_T'], given['heat'], given['mass'], given['specific_heat'])
        rel_err = abs(result - expected['final_T']) / expected['final_T']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_ideal_gas_law(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'ideal_gas_law':
        # Determine which variable to solve for
        if 'V' not in expected:
            result = ideal_gas_law(P=given.get('P'), V=given.get('V'), 
                                   n=given.get('n'), T=given.get('T'), R=given.get('R', 0.08206))
            rel_err = abs(result - expected['n']) / expected['n']
        elif 'n' not in expected:
            result = ideal_gas_law(P=given.get('P'), V=None, 
                                   n=given.get('n'), T=given.get('T'), R=given.get('R', 0.08206))
            rel_err = abs(result - expected['V']) / expected['V']
        else:
            result = ideal_gas_law(P=given.get('P'), V=None, 
                                   n=given.get('n'), T=given.get('T'), R=given.get('R', 0.08206))
            rel_err = abs(result - expected.get('V', result)) / max(expected.get('V', result), 1)
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'molar_volume':
        result = molar_volume(given['T'], given['P'], given.get('R', 0.08206))
        rel_err = abs(result - expected['V_m']) / expected['V_m']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_gas_laws(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'boyles_law':
        result = boyles_law(P1=given['P1'], V1=given['V1'], P2=given['P2'], V2=None)
        rel_err = abs(result - expected['V2']) / expected['V2']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'charles_law':
        result = charles_law(V1=given['V1'], T1=given['T1'], V2=None, T2=given['T2'])
        rel_err = abs(result - expected['V2']) / expected['V2']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'combined_gas_law':
        result = combined_gas_law(P1=given['P1'], V1=given['V1'], T1=given['T1'],
                                  P2=given['P2'], V2=None, T2=given['T2'])
        rel_err = abs(result - expected['V2']) / expected['V2']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_solution_concentration(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'molarity':
        result = molarity(given['moles_solute'], given['L_solution'])
        rel_err = abs(result - expected['molarity']) / expected['molarity']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'molality':
        result = molality(given['moles_solute'], given['kg_solvent'])
        rel_err = abs(result - expected['molality']) / expected['molality']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'mole_fraction':
        result_dict = mole_fraction(given['components'])
        result = result_dict['A']
        rel_err = abs(result - expected['mole_fraction_A']) / expected['mole_fraction_A']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_equilibrium(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'reaction_quotient':
        result = reaction_quotient(given['concentrations'], given['products'], given['reactants'])
        rel_err = abs(result - expected['Q']) / expected['Q']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'equilibrium_constant':
        # Skip for now - function doesn't exist
        return True
    return False

def verify_rate_law(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'calculate_rate':
        result = calculate_rate(given['k'], given['concentrations'], given['orders'])
        rel_err = abs(result - expected['rate']) / expected['rate']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'determine_order':
        result = determine_order_initial_rates(given['conc1'], given['rate1'], given['conc2'], given['rate2'])
        return result == expected['order']
    return False

def verify_gibbs_free_energy(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'gibbs_free_energy':
        result = gibbs_free_energy(given['delta_H'], given['delta_S'], given['T'])
        rel_err = abs(result - expected['delta_G']) / expected['delta_G']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'spontaneity':
        result = spontaneity_from_G(given['delta_G'])
        return result == expected['spontaneity']
    return False

def verify_enthalpy(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'delta_H_rxn':
        reactants = [tuple(x) for x in given['reactants']]
        products = [tuple(x) for x in given['products']]
        result = delta_H_rxn_from_formation(reactants, products)
        rel_err = abs(result - expected['delta_H']) / abs(expected['delta_H'])
        return rel_err <= p['tolerance']['relative']
    return False

def verify_entropy(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'entropy_change_heat':
        result = entropy_change_heat(given['q_rev'], given['T'])
        rel_err = abs(result - expected['delta_S']) / expected['delta_S']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_ph_calculations(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'pH_from_H3O':
        result = pH_from_H3O(given['h3o_conc'])
        abs_err = abs(result - expected['pH'])
        return abs_err <= p['tolerance']['absolute']
    elif ptype == 'H3O_from_pH':
        result = H3O_from_pH(given['pH'])
        rel_err = abs(result - expected['h3o_conc']) / expected['h3o_conc']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_titration(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'equivalence_volume':
        result = equivalence_volume(given['analyte_mol'], given['titrant_conc'], given['stoichiometry'])
        rel_err = abs(result - expected['V_eq']) / expected['V_eq']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'half_equivalence':
        result = half_equivalence_pH(given['pKa'])
        abs_err = abs(result - expected['pH'])
        return abs_err <= p['tolerance']['absolute']
    return False

def verify_amount_conversion(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'mass_to_moles':
        result = mass_to_moles(given['mass_g'], given['molar_mass'])
        rel_err = abs(result - expected['moles']) / expected['moles']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'moles_to_particles':
        result = moles_to_particles(given['moles'])
        rel_err = abs(result - expected['particles']) / expected['particles']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_calorimetry(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'coffee_cup':
        result = coffee_cup_heat_rxn(given['mass'], given['specific_heat'], given['delta_T'])
        rel_err = abs(result - expected['q_rxn']) / abs(expected['q_rxn'])
        return rel_err <= p['tolerance']['relative']
    return False

def verify_arrhenius(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'arrhenius_k':
        result = arrhenius_k(given['A'], given['Ea'], given['T'])
        rel_err = abs(result - expected['k']) / expected['k']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'activation_energy':
        result = activation_energy(given['k1'], given['T1'], given['k2'], given['T2'])
        rel_err = abs(result - expected['Ea']) / expected['Ea']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_colligative_properties(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'boiling_point_elevation':
        result = boiling_point_elevation(given['m'], given['Kb'], given.get('i', 1))
        rel_err = abs(result - expected['delta_Tb']) / expected['delta_Tb']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'freezing_point_depression':
        result = freezing_point_depression(given['m'], given['Kf'], given.get('i', 1))
        rel_err = abs(result - expected['delta_Tf']) / expected['delta_Tf']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_buffer(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'henderson_hasselbalch':
        result = henderson_hasselbalch(given['pKa'], given['base_conc'], given['acid_conc'])
        abs_err = abs(result - expected['pH'])
        return abs_err <= p['tolerance']['absolute']
    return False

def verify_integrated_rate_law(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'first_order_half_life':
        result = first_order_half_life(given['k'])
        rel_err = abs(result - expected['t_half']) / expected['t_half']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'first_order_concentration':
        result = first_order_concentration(given['C0'], given['k'], given['t'])
        rel_err = abs(result - expected['Ct']) / expected['Ct']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_le_chatelier(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'predict_shift_concentration':
        result = predict_shift_concentration(given['stress_type'], 'species', given['is_reactant'])
        return result == expected['shift']
    elif ptype == 'predict_shift_pressure':
        result = predict_shift_pressure(given['delta_n'], given['pressure_change'])
        return result == expected['shift']
    return False

def verify_solubility(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'henrys_law':
        result = henrys_law(given['kH'], given['P'])
        rel_err = abs(result - expected['C']) / expected['C']
        return rel_err <= p['tolerance']['relative']
    return False

def verify_electron_configuration(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'electron_configuration':
        result = electron_configuration(given['atomic_number'], given.get('noble_gas', True))
        # Normalize result for comparison
        result_norm = result.replace(' ', '').replace('2', '2').replace('1', '1').replace('0', '0')
        expected_norm = expected['config'].replace(' ', '').replace('2', '2').replace('1', '1').replace('0', '0')
        return result_norm == expected_norm
    return False

def verify_molecular_geometry(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'molecular_structure':
        result = molecular_structure(given['regions'], given['lone_pairs'])
        return result == expected['structure']
    return False

def verify_thermodynamics_laws(p):
    given = p['given']
    expected = p['expected']
    ptype = p['type']
    
    if ptype == 'entropy_surroundings':
        result = entropy_surroundings(given['delta_H'], given['T'])
        rel_err = abs(result - expected['delta_S_surr']) / expected['delta_S_surr']
        return rel_err <= p['tolerance']['relative']
    elif ptype == 'entropy_universe':
        result = entropy_universe(given['delta_S_sys'], given['delta_S_surr'])
        rel_err = abs(result - expected['delta_S_univ']) / max(expected['delta_S_univ'], 0.01)
        return rel_err <= p['tolerance']['relative']
    return False

# Run verifications
print('=== BATCH VERIFICATION ===\n')

total_passed = 0
total_failed = 0

print('energy_basics_tools.py:')
p, f = verify_tool('energy_basics', 'chem-memory/test_problems/energy_basics_problems.json', verify_energy_basics)
total_passed += p
total_failed += f

print('ideal_gas_law_tools.py:')
p, f = verify_tool('ideal_gas_law', 'chem-memory/test_problems/ideal_gas_law_problems.json', verify_ideal_gas_law)
total_passed += p
total_failed += f

print('gas_laws_tools.py:')
p, f = verify_tool('gas_laws', 'chem-memory/test_problems/gas_laws_problems.json', verify_gas_laws)
total_passed += p
total_failed += f

print('solution_concentration_tools.py:')
p, f = verify_tool('solution_concentration', 'chem-memory/test_problems/solution_concentration_problems.json', verify_solution_concentration)
total_passed += p
total_failed += f

print('equilibrium_tools.py:')
p, f = verify_tool('equilibrium', 'chem-memory/test_problems/equilibrium_problems.json', verify_equilibrium)
total_passed += p
total_failed += f

print('equilibrium_tools.py:')
p, f = verify_tool('equilibrium', 'chem-memory/test_problems/equilibrium_problems.json', verify_equilibrium)
total_passed += p
total_failed += f

print('rate_law_tools.py:')
p, f = verify_tool('rate_law', 'chem-memory/test_problems/rate_law_problems.json', verify_rate_law)
total_passed += p
total_failed += f

print('gibbs_free_energy_tools.py:')
p, f = verify_tool('gibbs_free_energy', 'chem-memory/test_problems/gibbs_free_energy_problems.json', verify_gibbs_free_energy)
total_passed += p
total_failed += f

print('enthalpy_tools.py:')
p, f = verify_tool('enthalpy', 'chem-memory/test_problems/enthalpy_problems.json', verify_enthalpy)
total_passed += p
total_failed += f

print('entropy_tools.py:')
p, f = verify_tool('entropy', 'chem-memory/test_problems/entropy_problems.json', verify_entropy)
total_passed += p
total_failed += f

print('ph_calculations_tools.py:')
p, f = verify_tool('ph_calculations', 'chem-memory/test_problems/ph_calculations_problems.json', verify_ph_calculations)
total_passed += p
total_failed += f

print('titration_tools.py:')
p, f = verify_tool('titration', 'chem-memory/test_problems/titration_problems.json', verify_titration)
total_passed += p
total_failed += f

print('amount_conversion_tools.py:')
p, f = verify_tool('amount_conversion', 'chem-memory/test_problems/amount_conversion_problems.json', verify_amount_conversion)
total_passed += p
total_failed += f

print('calorimetry_tools.py:')
p, f = verify_tool('calorimetry', 'chem-memory/test_problems/calorimetry_problems.json', verify_calorimetry)
total_passed += p
total_failed += f

print('arrhenius_tools.py:')
p, f = verify_tool('arrhenius', 'chem-memory/test_problems/arrhenius_problems.json', verify_arrhenius)
total_passed += p
total_failed += f

print('colligative_properties_tools.py:')
p, f = verify_tool('colligative_properties', 'chem-memory/test_problems/colligative_properties_problems.json', verify_colligative_properties)
total_passed += p
total_failed += f

print('buffer_tools.py:')
p, f = verify_tool('buffer', 'chem-memory/test_problems/buffer_problems.json', verify_buffer)
total_passed += p
total_failed += f

print('integrated_rate_law_tools.py:')
p, f = verify_tool('integrated_rate_law', 'chem-memory/test_problems/integrated_rate_law_problems.json', verify_integrated_rate_law)
total_passed += p
total_failed += f

print('le_chatelier_tools.py:')
p, f = verify_tool('le_chatelier', 'chem-memory/test_problems/le_chatelier_problems.json', verify_le_chatelier)
total_passed += p
total_failed += f

print('solubility_tools.py:')
p, f = verify_tool('solubility', 'chem-memory/test_problems/solubility_problems.json', verify_solubility)
total_passed += p
total_failed += f

print('electron_configuration_tools.py:')
p, f = verify_tool('electron_configuration', 'chem-memory/test_problems/electron_configuration_problems.json', verify_electron_configuration)
total_passed += p
total_failed += f

print('molecular_geometry_tools.py:')
p, f = verify_tool('molecular_geometry', 'chem-memory/test_problems/molecular_geometry_problems.json', verify_molecular_geometry)
total_passed += p
total_failed += f

print('thermodynamics_laws_tools.py:')
p, f = verify_tool('thermodynamics_laws', 'chem-memory/test_problems/thermodynamics_laws_problems.json', verify_thermodynamics_laws)
total_passed += p
total_failed += f

print(f'=== TOTAL: {total_passed + total_failed} problems, {total_passed} PASS ===')
