# -*- coding: utf-8 -*-
"""
Molecular Geometry and VSEPR Tools - L3 Implementation
Chapter 7.06: Molecular Structure and Polarity

Solver Instructions:
- electron_pair_geometry(regions): returns geometry name for 2-6 regions
- molecular_structure(regions, lone_pairs): returns molecular shape
- hybridization(regions): returns sp/sp2/sp3/sp3d/sp3d2
- predict_bond_angles(regions, lone_pairs): returns approximate angles
- is_polar_molecule(bond_dipoles, geometry): returns True/False
- dipole_moment(charge, distance): returns dipole in Debye
"""

from typing import Dict, List, Tuple, Optional
from math import sqrt


ELECTRON_PAIR_GEOMETRIES = {
    2: 'linear', 3: 'trigonal planar', 4: 'tetrahedral',
    5: 'trigonal bipyramidal', 6: 'octahedral',
}

MOLECULAR_STRUCTURES = {
    (2, 0): 'linear', (3, 0): 'trigonal planar', (3, 1): 'bent',
    (4, 0): 'tetrahedral', (4, 1): 'trigonal pyramidal', (4, 2): 'bent',
    (5, 0): 'trigonal bipyramidal', (5, 1): 'seesaw', (5, 2): 'T-shaped', (5, 3): 'linear',
    (6, 0): 'octahedral', (6, 1): 'square pyramidal', (6, 2): 'square planar', (6, 4): 'linear',
}

IDEAL_ANGLES = {
    'linear': [180], 'trigonal planar': [120], 'bent': [120, 109.5],
    'tetrahedral': [109.5], 'trigonal pyramidal': [107],
    'trigonal bipyramidal': [90, 120], 'seesaw': [90, 120, 180],
    'T-shaped': [90, 180], 'octahedral': [90],
    'square pyramidal': [90], 'square planar': [90, 180],
}


def electron_pair_geometry(regions):
    if regions not in ELECTRON_PAIR_GEOMETRIES:
        raise ValueError(f"Unknown geometry for {regions} regions")
    return ELECTRON_PAIR_GEOMETRIES[regions]


def molecular_structure(regions, lone_pairs):
    key = (regions, lone_pairs)
    if key not in MOLECULAR_STRUCTURES:
        raise ValueError(f"Unknown structure for {regions} regions, {lone_pairs} lone pairs")
    return MOLECULAR_STRUCTURES[key]


def predict_bond_angles(regions, lone_pairs):
    structure = molecular_structure(regions, lone_pairs)
    angles = IDEAL_ANGLES.get(structure, [109.5]).copy()
    if lone_pairs > 0:
        if structure == 'bent' and regions == 4:
            angles = [104.5]
        elif structure == 'trigonal pyramidal':
            angles = [107]
        elif structure == 'seesaw':
            angles = [90, 120]
    return angles


def dipole_moment(charge, distance):
    return charge * distance * 4.803


def is_polar_molecule(bond_dipoles, geometry):
    total_x = sum(d[0] for d in bond_dipoles)
    total_y = sum(d[1] for d in bond_dipoles)
    total_z = sum(d[2] for d in bond_dipoles)
    magnitude = sqrt(total_x**2 + total_y**2 + total_z**2)
    return magnitude > 0.01


def hybridization(regions):
    hybrids = {2: 'sp', 3: 'sp2', 4: 'sp3', 5: 'sp3d', 6: 'sp3d2'}
    return hybrids.get(regions, 'unknown')


def central_atom_position(geometry):
    positions = {
        'linear': 'on axis', 'trigonal planar': 'center of triangle',
        'tetrahedral': 'center of tetrahedron',
        'trigonal bipyramidal': 'axial 90 deg; equatorial 120 deg',
        'octahedral': 'all positions equivalent',
    }
    return positions.get(geometry, 'central')
