#!/usr/bin/env python

# Credit:
# This adapted by David Mobley from Andrea Rizzi's file of the same name which he wrote for SAMPL6
# at https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py
# He gets credit for anything good about it; I deserve blame for any problems.

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================

import os
import math
import csv
import json
from collections import OrderedDict

import numpy as np
from simtk import unit as u


# =============================================================================
# CONSTANTS
# =============================================================================

T = 298 * u.kelvin
R = u.MOLAR_GAS_CONSTANT_R
RELATIVE_TITRANT_CONC_ERROR = 0.03

CLIP_GUESTS_SMILES_PATH = '../../Isaacs_clip/guest_files/trimertrip_guest_smiles.txt'
GDCC_GUESTS_SMILES_PATH = '../../GDCC_and_guests/guest_files/GDCC_guest_smiles.txt'
CD_GUESTS_SMILES_PATH = '../../cyclodextrin_derivatives/guest_files/cyclodextrin_guest_smiles.txt'
CLIP_GUESTS_NAMES_PATH = '../../Isaacs_clip/guest_files/trimertrip_guest_names.txt'
GDCC_GUESTS_NAMES_PATH = '../../GDCC_and_guests/guest_files/GDCC_guest_names.txt'
CD_GUESTS_NAMES_PATH = '../../cyclodextrin_derivatives/guest_files/cyclodextrin_guest_names.txt'
CD_HOST_NAMES = ['bCD', 'MGLab_8', 'MGLab_9','MGLab_19', 'MGLab_23', 'MGLab_24', 'MGLab_34', 'MGLab_35', 'MGLab_36']

# Experimental results as provided by the Gibb, Isaacs and Gilson groups.
# The error is relative. None means that the error is <1%.
EXPERIMENTAL_DATA = OrderedDict([

    ('clip-g1', OrderedDict([
        ('Kd_1', 34.2e-6 * u.molar), ('dKd_1', 3.29e-6 * u.molar),
        ('DH_1', -6.03 * u.kilocalories_per_mole), ('dDH_1', 0.260 * u.kilocalories_per_mole),
        ('Kd_2', 29.6e-6 * u.molar), ('dKd_2', 7.70e-6 * u.molar),
        ('DH_2', -6.14 * u.kilocalories_per_mole), ('dDH_2', 0.696 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.899, 0.825]))
    ])),
    ('clip-g2', OrderedDict([
        ('Kd_1', 749e-9 * u.molar), ('dKd_1', 17.7e-9 * u.molar),
        ('DH_1', -8.58 * u.kilocalories_per_mole), ('dDH_1', 0.021 * u.kilocalories_per_mole),
        ('Kd_2', 829e-9 * u.molar), ('dKd_2', 40.8e-9 * u.molar),
        ('DH_2', -8.95 * u.kilocalories_per_mole), ('dDH_2', 0.053 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.891, 1.11]))
    ])),
    ('clip-g3', OrderedDict([
        ('Kd_1', 43.5e-9 * u.molar), ('dKd_1', 3.39e-9 * u.molar),
        ('DH_1', -10.8 * u.kilocalories_per_mole), ('dDH_1', 0.044 * u.kilocalories_per_mole),
        ('Kd_2', 41.3e-9 * u.molar), ('dKd_2', 3.24e-9 * u.molar),
        ('DH_2', -10.9 * u.kilocalories_per_mole), ('dDH_2', 0.043 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.974, 0.831]))
    ])),
    ('clip-g15', OrderedDict([
        ('Kd_1', 18.3e-9 * u.molar), ('dKd_1', 1.00e-9 * u.molar),
        ('DH_1', -12.8 * u.kilocalories_per_mole), ('dDH_1', 0.033 * u.kilocalories_per_mole),
        ('Kd_2', 20.0e-9 * u.molar), ('dKd_2', 8.74e-10 * u.molar),
        ('DH_2', -12.7 * u.kilocalories_per_mole), ('dDH_2', 0.028 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.917, 1.02]))
    ])),
    ('clip-g12', OrderedDict([
        ('Kd_1', 830e-9 * u.molar), ('dKd_1', 23.3e-9 * u.molar),
        ('DH_1', -8.54 * u.kilocalories_per_mole), ('dDH_1', 0.027 * u.kilocalories_per_mole),
        ('Kd_2', 827e-9 * u.molar), ('dKd_2', 31.0e-9 * u.molar),
        ('DH_2', -8.25 * u.kilocalories_per_mole), ('dDH_2', 0.034 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.970, 0.907]))
    ])),
    ('clip-g5', OrderedDict([
        ('Kd_1', 7.07e-9 * u.molar), ('dKd_1', 1.13e-9 * u.molar),
        ('DH_1', -11.5 * u.kilocalories_per_mole), ('dDH_1', 0.094 * u.kilocalories_per_mole),
        ('Kd_2', 6.63e-9 * u.molar), ('dKd_2', 8.99e-10 * u.molar),
        ('DH_2', -11.3 * u.kilocalories_per_mole), ('dDH_2', 0.07 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.950, 0.837]))
    ])),
    ('clip-g16', OrderedDict([
        ('Kd_1', 3.55e-9 * u.molar), ('dKd_1', 7.80e-10 * u.molar),
        ('DH_1', -11.3 * u.kilocalories_per_mole), ('dDH_1', 0.068 * u.kilocalories_per_mole),
        ('Kd_2', 3.27e-9 * u.molar), ('dKd_2', 8.48e-10 * u.molar),
        ('DH_2', -11.2 * u.kilocalories_per_mole), ('dDH_2', 0.072 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.925, 0.856]))
    ])),
    ('clip-g17', OrderedDict([
        ('Kd_1', 1.97e-9 * u.molar), ('dKd_1', 1.06e-9 * u.molar),
        ('DH_1', -10.4 * u.kilocalories_per_mole), ('dDH_1', 0.123 * u.kilocalories_per_mole),
        ('Kd_2', 2.20e-9 * u.molar), ('dKd_2', 5.76e-10 * u.molar),
        ('DH_2', -10.4 * u.kilocalories_per_mole), ('dDH_2', 0.064 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.968, 0.979]))
    ])),
    ('clip-g9', OrderedDict([
        ('Kd_1', 2.80e-6 * u.molar), ('dKd_1', 113e-9 * u.molar),
        ('DH_1', -4.83 * u.kilocalories_per_mole), ('dDH_1', 0.036 * u.kilocalories_per_mole),
        ('Kd_2', 2.79e-6 * u.molar), ('dKd_2', 162e-9 * u.molar),
        ('DH_2', -4.72 * u.kilocalories_per_mole), ('dDH_2', 0.046 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([1.07, 0.829]))
    ])),
    ('clip-g6', OrderedDict([
        ('Kd_1', 88.3e-9 * u.molar), ('dKd_1', 9.44e-9 * u.molar),
        ('DH_1', -10.1 * u.kilocalories_per_mole), ('dDH_1', 0.119 * u.kilocalories_per_mole),
        ('Kd_2', 97.0e-9 * u.molar), ('dKd_2', 13.6e-9 * u.molar),
        ('DH_2', -10.3 * u.kilocalories_per_mole), ('dDH_2', 0.165 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.848, 0.814]))
    ])),
    ('clip-g11', OrderedDict([
        ('Kd_1', 245e-9 * u.molar), ('dKd_1', 22.3e-9 * u.molar),
        ('DH_1', -7.41 * u.kilocalories_per_mole), ('dDH_1', 0.084 * u.kilocalories_per_mole),
        ('Kd_2', 238e-9 * u.molar), ('dKd_2', 22.2e-9 * u.molar),
        ('DH_2', -7.35 * u.kilocalories_per_mole), ('dDH_2', 0.084 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.848, 0.846]))
    ])),
    ('clip-g10', OrderedDict([
        ('Kd_1', 902e-9 * u.molar), ('dKd_1', 64.8e-9 * u.molar),
        ('DH_1', -5.88 * u.kilocalories_per_mole), ('dDH_1', 0.049 * u.kilocalories_per_mole),
        ('Kd_2', 1.17e-6 * u.molar), ('dKd_2', 72.6e-9 * u.molar),
        ('DH_2', -5.80 * u.kilocalories_per_mole), ('dDH_2', 0.047 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.960, 1.02]))
    ])),
    ('clip-g8', OrderedDict([
        ('Kd_1', 114e-9 * u.molar), ('dKd_1', 6.79e-9 * u.molar),
        ('DH_1', -10.5 * u.kilocalories_per_mole), ('dDH_1', 0.044 * u.kilocalories_per_mole),
        ('Kd_2', 120e-9 * u.molar), ('dKd_2', 5.34e-9 * u.molar),
        ('DH_2', -10.6 * u.kilocalories_per_mole), ('dDH_2', 0.033 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.910, 0.894]))
    ])),
    ('clip-g18', OrderedDict([
        ('Kd_1', 17.2e-9 * u.molar), ('dKd_1', 1.42e-9 * u.molar),
        ('DH_1', -12.4 * u.kilocalories_per_mole), ('dDH_1', 0.045 * u.kilocalories_per_mole),
        ('Kd_2', 19.8e-9 * u.molar), ('dKd_2', 2.34e-9 * u.molar),
        ('DH_2', -12.3 * u.kilocalories_per_mole), ('dDH_2', 0.069 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.896, 1.00]))
    ])),
    ('clip-g19', OrderedDict([
        ('Kd_1', 2.80e-9 * u.molar), ('dKd_1', 1.53e-10 * u.molar),
        ('DH_1', -13.7 * u.kilocalories_per_mole), ('dDH_1', 0.039 * u.kilocalories_per_mole),
        ('Kd_2', 2.74e-9 * u.molar), ('dKd_2', 6.04e-10 * u.molar),
        ('DH_2', -13.6 * u.kilocalories_per_mole), ('dDH_2', 0.144 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.755, 0.828]))
    ])),
    ('clip-g7', OrderedDict([
        ('Kd_1', 16.8e-6 * u.molar), ('dKd_1', 652e-9 * u.molar),
        ('DH_1', -6.61 * u.kilocalories_per_mole), ('dDH_1', 0.088 * u.kilocalories_per_mole),
        ('Kd_2', 17.2e-6 * u.molar), ('dKd_2', 1.24e-6 * u.molar),
        ('DH_2', -6.80 * u.kilocalories_per_mole), ('dDH_2', 0.170 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', np.mean([0.839, 0.813]))
    ])),
    ('OA-g1', OrderedDict([
        ('DG', -20.8 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
        ('DH', -23.2 * u.kilojoules_per_mole), ('dDH', 0.4 * u.kilojoules_per_mole),
        ('TDS', -2.4 * u.kilojoules_per_mole), ('dTDS', 0.6 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    ('OA-g2', OrderedDict([
        ('DG', -28.9 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
        ('DH', -40 * u.kilojoules_per_mole), ('dDH', 1 * u.kilojoules_per_mole),
        ('TDS', -11 * u.kilojoules_per_mole), ('dTDS', 1 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    ('OA-g3', OrderedDict([
        ('DG', -33.9 * u.kilojoules_per_mole), ('dDG', 0.2 * u.kilojoules_per_mole),
        ('DH', -50.2 * u.kilojoules_per_mole), ('dDH', 0.1 * u.kilojoules_per_mole),
        ('TDS', -16.3 * u.kilojoules_per_mole), ('dTDS', 0.1 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    ('OA-g4', OrderedDict([
        ('DG', -28.4 * u.kilojoules_per_mole), ('dDG', 0.2 * u.kilojoules_per_mole),
        ('DH', -28.0 * u.kilojoules_per_mole), ('dDH', 0.6 * u.kilojoules_per_mole),
        ('TDS', 0.3 * u.kilojoules_per_mole), ('dTDS', 0.1 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    ('OA-g5', OrderedDict([
        ('DG', -19.8 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
        ('DH', -31.3 * u.kilojoules_per_mole), ('dDH', 0.2 * u.kilojoules_per_mole),
        ('TDS', -11.5 * u.kilojoules_per_mole), ('dTDS', 0.2 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    # Currently the values are inconsistent here, probably rounding error.
    #('OA-g6', OrderedDict([
    #    ('DG', -20.8 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
    #    ('DH', -30 * u.kilojoules_per_mole), ('dDH', 1 * u.kilojoules_per_mole),
    #    ('TDS', -10 * u.kilojoules_per_mole), ('dTDS', 1 * u.kilojoule_per_mole),
    #    ('n', 1)
    #])),
    ('OA-g7', OrderedDict([
        ('DG', -25.4 * u.kilojoules_per_mole), ('dDG', 0.2 * u.kilojoules_per_mole),
        ('DH', -24.0 * u.kilojoules_per_mole), ('dDH', 0.6 * u.kilojoules_per_mole),
        ('TDS', 1.4 * u.kilojoules_per_mole), ('dTDS', 0.6 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    ('OA-g8', OrderedDict([
        ('DG', -34 * u.kilojoules_per_mole), ('dDG', 2 * u.kilojoules_per_mole),
        ('DH', -32.7 * u.kilojoules_per_mole), ('dDH', 0.7 * u.kilojoules_per_mole),
        ('TDS', 1.7 * u.kilojoules_per_mole), ('dTDS', 0.9 * u.kilojoule_per_mole),
        ('n', 1)
    ])),
    ('exoOA-g1', OrderedDict([
        ('DG', 'ND'), ('dDG', 'ND'),
        ('DH', 'ND'), ('dDH', 'ND'),
        ('TDS', 'ND'), ('dTDS', 'ND'),
        ('n', 1)
    ])),
    ('exoOA-g2', OrderedDict([
        ('DG', -9 * u.kilojoules_per_mole), ('dDG', 3 * u.kilojoules_per_mole),
        ('DH', 'ND'), ('dDH', 'ND'),
        ('TDS', 'ND'), ('dTDS', 'ND'),
        ('n', 1)
    ])),
    #('exoOA-g3', OrderedDict([
    #    ('DG', -14.1 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
    #    ('DH', -25.2 * u.kilojoules_per_mole), ('dDH', 0.5 * u.kilojoules_per_mole),
    #    ('TDS', -11.7 * u.kilojoules_per_mole), ('dTDS', 0.1 * u.kilojoules_per_mole),
    #    ('n', 1)
    #])),
    #('exoOA-g4', OrderedDict([
    #    ('DG', -15.1 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
    #    ('DH', -31 * u.kilojoules_per_mole), ('dDH', 2 * u.kilojoules_per_mole),
    #    ('TDS', -15 * u.kilojoules_per_mole), ('dTDS', 3 * u.kilojoules_per_mole),
    #    ('n', 1)
    #])),
    ('exoOA-g5', OrderedDict([
        ('DG', -23.3 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
        ('DH', -25.8 * u.kilojoules_per_mole), ('dDH', 0.1 * u.kilojoules_per_mole),
        ('TDS', -2.5 * u.kilojoules_per_mole), ('dTDS', 0.1 * u.kilojoules_per_mole),
        ('n', 1)
    ])),
    ('exoOA-g6', OrderedDict([
        ('DG', -24.4 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
        ('DH', -13.6 * u.kilojoules_per_mole), ('dDH', 0.1 * u.kilojoules_per_mole),
        ('TDS', 10.8 * u.kilojoules_per_mole), ('dTDS', 0.2 * u.kilojoules_per_mole),
        ('n', 1)
    ])),
    ('exoOA-g7', OrderedDict([
        ('DG', -29.2 * u.kilojoules_per_mole), ('dDG', 0.5 * u.kilojoules_per_mole),
        ('DH', -20.8 * u.kilojoules_per_mole), ('dDH', 0.3 * u.kilojoules_per_mole),
        ('TDS', 8.4 * u.kilojoules_per_mole), ('dTDS', 0.9 * u.kilojoules_per_mole),
        ('n', 1)
    ])),
    ('exoOA-g8', OrderedDict([
        ('DG', -32.1 * u.kilojoules_per_mole), ('dDG', 0.4 * u.kilojoules_per_mole),
        ('DH', -21.1 * u.kilojoules_per_mole), ('dDH', 0.2 * u.kilojoules_per_mole),
        ('TDS', 11 * u.kilojoules_per_mole), ('dTDS', 1 * u.kilojoules_per_mole),
        ('n', 1)
    ])),
    ('bCD-g1', OrderedDict([
        ('Ka_1', 2025.31 / u.molar), ('dKa_1', 68.11 / u.molar),
        ('Ka_2', 2098.64 / u.molar), ('dKa_2', 66.95 / u.molar),
        ('DH_1', -10.90 * u.kilojoules_per_mole), ('dDH_1', 0.44 * u.kilojoules_per_mole),
        ('DH_2', -10.53 * u.kilojoules_per_mole), ('dDH_2', 0.47 * u.kilojoules_per_mole),
        #('TDS_1', 8.09 * u.kilojoules_per_mole), ('dTDS_1', 0.45 * u.kilojoules_per_mole),
        #('TDS_2', 8.56 * u.kilojoules_per_mole), ('dTDS_2', 0.47 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 0.875)
    ])),
    ('bCD-g2', OrderedDict([
        ('Ka_1', 36491.91 / u.molar), ('dKa_1', 1737.70 / u.molar),
        ('Ka_2', 33572.61 / u.molar), ('dKa_2', 1563.02 / u.molar),
        ('DH_1', -43.26 * u.kilojoules_per_mole), ('dDH_1', 1.75 * u.kilojoules_per_mole),
        ('DH_2', -43.85 * u.kilojoules_per_mole), ('dDH_2', 1.76 * u.kilojoules_per_mole),
        #('TDS_1', -17.04 * u.kilojoules_per_mole), ('dTDS_1', 1.75 * u.kilojoules_per_mole),
        #('TDS_2', -17.84 * u.kilojoules_per_mole), ('dTDS_2', 1.76 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1.00)
    ])),
    ('MGLab_8-g1', OrderedDict([
        ('Ka_1', 244.18 / u.molar), ('dKa_1', 13.89 / u.molar),
        ('Ka_2', 286.54 / u.molar), ('dKa_2', 14.93 / u.molar),
        ('DH_1', -9.18 * u.kilojoules_per_mole), ('dDH_1', 1.40 * u.kilojoules_per_mole),
        ('DH_2', -5.89 * u.kilojoules_per_mole), ('dDH_2', 0.52 * u.kilojoules_per_mole),
        #('TDS_1', 4.54 * u.kilojoules_per_mole), ('dTDS_1', 1.40 * u.kilojoules_per_mole),
        #('TDS_2', 8.23 * u.kilojoules_per_mole), ('dTDS_2', 0.53 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.78+1)/2)
    ])),
    ('MGLab_8-g2', OrderedDict([
        ('Ka_1', 780.56 / u.molar), ('dKa_1', 31.98 / u.molar),
        ('Ka_2', 874.24 / u.molar), ('dKa_2', 32.42 / u.molar),
        ('DH_1', -27.40 * u.kilojoules_per_mole), ('dDH_1', 1.18 * u.kilojoules_per_mole),
        ('DH_2', -30.46 * u.kilojoules_per_mole), ('dDH_2', 1.47 * u.kilojoules_per_mole),
        #('TDS_1', -10.78 * u.kilojoules_per_mole), ('dTDS_1', 1.19 * u.kilojoules_per_mole),
        #('TDS_2', -13.56 * u.kilojoules_per_mole), ('dTDS_2', 1.47 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.96+1.10)/2)
    ])),
    ('MGLab_9-g1', OrderedDict([
        ('Ka_1', 221.08 / u.molar), ('dKa_1', 12.72 / u.molar),
        ('Ka_2', 203.13 / u.molar), ('dKa_2', 10.87 / u.molar),
        ('DH_1', -10.49 * u.kilojoules_per_mole), ('dDH_1', 1.80 * u.kilojoules_per_mole),
        ('DH_2', -12.44 * u.kilojoules_per_mole), ('dDH_2', 2.65 * u.kilojoules_per_mole),
        #('TDS_1', 2.98 * u.kilojoules_per_mole), ('dTDS_1', 1.80 * u.kilojoules_per_mole),
        #('TDS_2', 0.81 * u.kilojoules_per_mole), ('dTDS_2', 2.66 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 0.875)
    ])),
    ('MGLab_9-g2', OrderedDict([
        ('Ka_1', 683.17 / u.molar), ('dKa_1', 21.71 / u.molar),
        ('Ka_2', 713.79 / u.molar), ('dKa_2', 20.94 / u.molar),
        ('DH_1', -38.12 * u.kilojoules_per_mole), ('dDH_1', 1.73 * u.kilojoules_per_mole),
        ('DH_2', -37.61 * u.kilojoules_per_mole), ('dDH_2', 1.75 * u.kilojoules_per_mole),
        #('TDS_1', -21.82 * u.kilojoules_per_mole), ('dTDS_1', 1.73 * u.kilojoules_per_mole),
        #('TDS_2', -21.21 * u.kilojoules_per_mole), ('dTDS_2', 5.73 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.98+1.02)/2)
    ])),
    ('MGLab_19-g1', OrderedDict([
        ('Ka_1', 199.60 / u.molar), ('dKa_1', 8.02 / u.molar),
        ('Ka_2', 228.31 / u.molar), ('dKa_2', 8.02 / u.molar),
        ('DH_1', -9.17 * u.kilojoules_per_mole), ('dDH_1', 0.73 * u.kilojoules_per_mole),
        ('DH_2', -8.05 * u.kilojoules_per_mole), ('dDH_2', 0.52 * u.kilojoules_per_mole),
        #('TDS_1', 4.05 * u.kilojoules_per_mole), ('dTDS_1', 0.73 * u.kilojoules_per_mole),
        #('TDS_2', 5.51 * u.kilojoules_per_mole), ('dTDS_2', 0.53 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.81+0.85)/2)
    ])),
    ('MGLab_19-g2', OrderedDict([
        ('Ka_1', 315.83 / u.molar), ('dKa_1', 17.83 / u.molar),
        ('Ka_2', 318.33 / u.molar), ('dKa_2', 9.41 / u.molar),
        ('DH_1', -47.55 * u.kilojoules_per_mole), ('dDH_1', 3.40 * u.kilojoules_per_mole),
        ('DH_2', -48.60 * u.kilojoules_per_mole), ('dDH_2', 2.75 * u.kilojoules_per_mole),
        #('TDS_1', -33.19 * u.kilojoules_per_mole), ('dTDS_1', 3.40 * u.kilojoules_per_mole),
        #('TDS_2', -34.21 * u.kilojoules_per_mole), ('dTDS_2', 2.75 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (1.09+0.79)/2)
    ])),
    ('MGLab_23-g1', OrderedDict([
            ('Ka_1', 236.64 / u.molar), ('dKa_1', 11.99 / u.molar),
            ('Ka_2', 210.20 / u.molar), ('dKa_2', 10.99 / u.molar),
            ('DH_1', -9.88 * u.kilojoules_per_mole), ('dDH_1', 1.68 * u.kilojoules_per_mole),
            ('DH_2', -13.01 * u.kilojoules_per_mole), ('dDH_2', 4.18 * u.kilojoules_per_mole),
            #('TDS_1', 3.76 * u.kilojoules_per_mole), ('dTDS_1', 1.68 * u.kilojoules_per_mole),
            #('TDS_2', 0.33 * u.kilojoules_per_mole), ('dTDS_2', 4.18 * u.kilojoules_per_mole),
            ('TDS', None), ('dTDS', None),
            ('n', (0.81+0.70)/2)
        ])),
    ('MGLab_23-g2', OrderedDict([
        ('Ka_1', 1427.70 / u.molar), ('dKa_1', 56.95 / u.molar),
        ('Ka_2', 1588.79 / u.molar), ('dKa_2', 59.25 / u.molar),
        ('DH_1', -32.09 * u.kilojoules_per_mole), ('dDH_1', 1.38 * u.kilojoules_per_mole),
        ('DH_2', -31.54 * u.kilojoules_per_mole), ('dDH_2', 1.33 * u.kilojoules_per_mole),
        #('TDS_1', -13.96 * u.kilojoules_per_mole), ('dTDS_1', 0.48 * u.kilojoules_per_mole),
        #('TDS_2', -13.14 * u.kilojoules_per_mole), ('dTDS_2', 1.33 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.88+1.03)/2)
    ])),
    ('MGLab_24-g1', OrderedDict([
        ('Ka_1', 276.83 / u.molar), ('dKa_1', 13.59 / u.molar),
        ('Ka_2', 286.54 / u.molar), ('dKa_2', 14.95 / u.molar),
        ('DH_1', -7.76 * u.kilojoules_per_mole), ('dDH_1', 0.44 * u.kilojoules_per_mole),
        ('DH_2', -5.89 * u.kilojoules_per_mole), ('dDH_2', 0.47 * u.kilojoules_per_mole),
        #('TDS_1', 6.28 * u.kilojoules_per_mole), ('dTDS_1', 0.84 * u.kilojoules_per_mole),
        #('TDS_2', 8.23 * u.kilojoules_per_mole), ('dTDS_2', 0.54 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.83+1)/2)
    ])),
    ('MGLab_24-g2', OrderedDict([
        ('Ka_1', 1161.66 / u.molar), ('dKa_1', 44.16 / u.molar),
        ('Ka_2', 1038.92 / u.molar), ('dKa_2', 35.79 / u.molar),
        ('DH_1', -35.46 * u.kilojoules_per_mole), ('dDH_1', 1.52 * u.kilojoules_per_mole),
        ('DH_2', -36.92 * u.kilojoules_per_mole), ('dDH_2', 1.56 * u.kilojoules_per_mole),
        #('TDS_1', -17.85 * u.kilojoules_per_mole), ('dTDS_1', 1.53 * u.kilojoules_per_mole),
        #('TDS_2', -19.59 * u.kilojoules_per_mole), ('dTDS_2', 1.56 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (1.05+1.01)/2)
    ])),
    ('MGLab_34-g1', OrderedDict([
        ('Ka_1', 570.79 / u.molar), ('dKa_1', 17.8 / u.molar),
        ('Ka_2', 775.47 / u.molar), ('dKa_2', 23.66 / u.molar),
        ('DH_1', -15.14 * u.kilojoules_per_mole), ('dDH_1', 0.74 * u.kilojoules_per_mole),
        ('DH_2', -15.98 * u.kilojoules_per_mole), ('dDH_2', 0.72 * u.kilojoules_per_mole),
        #('TDS_1', 0.70 * u.kilojoules_per_mole), ('dTDS_1', 0.74 * u.kilojoules_per_mole),
        #('TDS_2', 0.63 * u.kilojoules_per_mole), ('dTDS_2', 0.72 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.83+0.80)/2)
    ])),
    ('MGLab_34-g2', OrderedDict([
        ('Ka_1', 19532.83 / u.molar), ('dKa_1', 733.92 / u.molar),
        ('Ka_2', 5690.03 / u.molar), ('dKa_2', 192.09 / u.molar),
        ('DH_1', -43.67 * u.kilojoules_per_mole), ('dDH_1', 1.57 * u.kilojoules_per_mole),
        ('DH_2', -30.51 * u.kilojoules_per_mole), ('dDH_2', 0.93 * u.kilojoules_per_mole),
        #('TDS_1', -19.02 * u.kilojoules_per_mole), ('dTDS_1', 1.58 * u.kilojoules_per_mole),
        #('TDS_2', -8.93 * u.kilojoules_per_mole), ('dTDS_2', 0.94 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.95+1.04)/2)
    ])),
    ('MGLab_35-g1', OrderedDict([
        ('Ka_1', 2103.19 / u.molar), ('dKa_1', 65.42 / u.molar),
        ('Ka_2', 2442.72 / u.molar), ('dKa_2', 73.46 / u.molar),
        ('DH_1', -17.87 * u.kilojoules_per_mole), ('dDH_1', 0.72 * u.kilojoules_per_mole),
        ('DH_2', -19.78 * u.kilojoules_per_mole), ('dDH_2', 0.83 * u.kilojoules_per_mole),
        #('TDS_1', 1.22 * u.kilojoules_per_mole), ('dTDS_1', 0.72 * u.kilojoules_per_mole),
        #('TDS_2', -0.31 * u.kilojoules_per_mole), ('dTDS_2', 0.83 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.94+0.76)/2)
    ])),
    ('MGLab_35-g2', OrderedDict([
        ('Ka_1', 27807.38 / u.molar), ('dKa_1', 1045.27 / u.molar),
        ('Ka_2', 25648.94 / u.molar), ('dKa_2', 1023.43 / u.molar),
        ('DH_1', -31.59 * u.kilojoules_per_mole), ('dDH_1', 1.30 * u.kilojoules_per_mole),
        ('DH_2', -29.36 * u.kilojoules_per_mole), ('dDH_2', 1.28 * u.kilojoules_per_mole),
        #('TDS_1', -6.05 * u.kilojoules_per_mole), ('dTDS_1', 1.30 * u.kilojoules_per_mole),
        #('TDS_2', -4.02 * u.kilojoules_per_mole), ('dTDS_2', 0.29 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.75+0.81)/2)
    ])),
    ('MGLab_36-g1', OrderedDict([
        ('Ka_1', 197.68 / u.molar), ('dKa_1', 7.63 / u.molar),
        ('Ka_2', 207.65 / u.molar), ('dKa_2', 8.29 / u.molar),
        ('DH_1', -13.55 * u.kilojoules_per_mole), ('dDH_1', 1.14 * u.kilojoules_per_mole),
        ('DH_2', -11.66 * u.kilojoules_per_mole), ('dDH_2', 0.81 * u.kilojoules_per_mole),
        #('TDS_1', -0.36 * u.kilojoules_per_mole), ('dTDS_1', 1.15 * u.kilojoules_per_mole),
        #('TDS_2', 1.65 * u.kilojoules_per_mole), ('dTDS_2', 0.82 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.81+0.93)/2)
    ])),
    ('MGLab_36-g2', OrderedDict([
        ('Ka_1', 372.79 / u.molar), ('dKa_1', 15.55 / u.molar),
        ('Ka_2', 335./42 / u.molar), ('dKa_2', 14.34 / u.molar),
        ('DH_1', -45.32 * u.kilojoules_per_mole), ('dDH_1', 3.70 * u.kilojoules_per_mole),
        ('DH_2', -45.37 * u.kilojoules_per_mole), ('dDH_2', 3.93 * u.kilojoules_per_mole),
        #('TDS_1', -30.74 * u.kilojoules_per_mole), ('dTDS_1', 3.70 * u.kilojoules_per_mole),
        #('TDS_2', -30.86 * u.kilojoules_per_mole), ('dTDS_2', 3.93 * u.kilojoules_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', (0.83+0.85)/2)
    ])),
])



# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_smiles(file_path):
    """Return the list of guests IDs and SMILES."""
    guests = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            smiles, gid = line.split(';', 1)
            guests.append([smiles.strip(), gid.strip()])
    return guests

def load_names(file_path):
    """Return the list of guests IDs and names."""
    guests = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            name, gid = line.split(';', 1)
            guests.append([name.strip(), gid.strip()])
    return guests


def compute_DG(Ka, dKa):
    """Compute the free energy from the association constant.

    Parameters
    ----------
    Ka : simtk.Quantity
        Association constant.
    dKa : simtk.Quantity
        Association constant uncertainty.

    Returns
    -------
    DG : simtk.Quantity
        Binding free energy.
    dDG : simtk.Quantity
        Binding free energy uncertainty.

    """
    concentration_unit = 1 / Ka.unit
    DG = -R * T * np.log(Ka*concentration_unit)
    # Propagate error.
    if dKa is None:
        dDG = None
    else:
        dDGdKa = -R * T / Ka  # Derivative dDG(Ka)/dKa.
        # Have to use u.sqrt to avoid bug with simtk.unit
        dDG = u.sqrt(dDGdKa**2 * dKa**2)
    return DG, dDG

def compute_Ka(DG, dDG):
    """Compute the association constant from the free energy.

    Parameters
    ----------
    DG : simtk.Quantity
        Free energy
    dDG : simtk.Quantity
        Uncertainty in free energy

    Returns
    -------
    Ka : simtk.Quantity
        Association constant.
    dKa : simtk.Quantity
        Association constant uncertainty.

    """
    concentration_unit = u.molar
    Ka = np.exp(-DG/(R*T))*1/concentration_unit
    # Propagate error.
    if dDG is None:
        dKa = None
    else:
        dKadDG = - Ka / (R*T)  # Derivative dKa(DG)/dDG.
        dKa = u.sqrt(dKadDG**2 * dDG**2)

    return Ka, dKa


def compute_TDS(DG, dDG, DH, dDH):
    """Compute the entropy from free energy and enthalpy.

    Parameters
    ----------
    DG : simtk.Quantity
        Free energy.
    dDG : simtk.Quantity
        Free energy uncertainty.
    DH : simtk.Quantity
        Enthalpy.
    dDH : simtk.Quantity
        Enthalpy uncertainty.

    Returns
    -------
    TDS : simtk.Quantity
        Entrop.
    dTDS : simtk.Quantity
        Binding free energy uncertainty.

    """
    TDS = DH - DG
    dTDS = u.sqrt(dDH**2 + dDG**2)
    return TDS, dTDS


def strip_units(quantities):
    for k, v in quantities.items():
        if isinstance(v, u.Quantity):
            # We only have energies and association and dissociation constants.
            if 'Ka' in k:
                quantities[k] = v.value_in_unit(v.unit)
            elif 'Kd' in k:
                quantities[k] = v.value_in_unit(v.unit)
            else:
                quantities[k] = v.value_in_unit(u.kilocalories_per_mole)


def reduce_to_first_significant_digit(quantity, uncertainty):
    # If strings, just return
    if isinstance(quantity, str) or isinstance(uncertainty, str):
        return quantity, uncertainty
    first_significant_digit = math.floor(math.log10(abs(uncertainty)))
    quantity = round(quantity, -first_significant_digit)
    uncertainty = round(uncertainty, -first_significant_digit)
    return quantity, uncertainty


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Load names and SMILES of guests.
    molecule_names = {}

    smiles_by_host = {
        'clip': load_smiles(CLIP_GUESTS_SMILES_PATH),
        'OA' : load_smiles(GDCC_GUESTS_SMILES_PATH),
        'exoOA' : load_smiles(GDCC_GUESTS_SMILES_PATH),
    }

    names_by_host = {
        'clip': load_names(CLIP_GUESTS_NAMES_PATH),
        'OA' : load_names(GDCC_GUESTS_NAMES_PATH),
        'exoOA' : load_names(GDCC_GUESTS_NAMES_PATH),
    }

    for host in CD_HOST_NAMES:
        smiles_by_host[host] = load_smiles(CD_GUESTS_SMILES_PATH)
        names_by_host[host] = load_names(CD_GUESTS_NAMES_PATH)

    for host in ['clip', 'OA', 'exoOA']+CD_HOST_NAMES:
        molecule_names[host] = {}
        for smi, gid in smiles_by_host[host]:
            for name, gid2 in names_by_host[host]:
                if gid==gid2:
                    molecule_names[host][gid] = smi, name

    output_dict = OrderedDict()
    upper_bound_molecules = dict(Ka=set(), DH=set(), TDS=set())

    for system_name, system_data in EXPERIMENTAL_DATA.items():
        host_name, gid = system_name.split('-')

        # Load SMILES and common name of the molecule.
        molecule_smiles, molecule_name = molecule_names[host_name][gid]

        # Create entry in the output dictionary.
        output_dict[system_name] = OrderedDict([
            ('name', molecule_name),
            ('SMILES', molecule_smiles),
        ])
        output_dict[system_name].update(system_data)
        system_data = output_dict[system_name]  # Shortcut.

        # If this data has two values, combine: First deal with measured values
        # Note that Kd/Ka values should be combined as free energies (since that's the normally distributed quantity)
        for data_type in ['Kd', 'Ka', 'DH']:
            if data_type+'_1' in system_data:
                if 'DH' in data_type: #just take mean
                    final_val = np.mean( [system_data[data_type+'_1'], system_data[data_type+'_2']])
                    system_data[data_type] = final_val

                    # Also compute uncertainty -- the larger of the propagated uncertainty and the standard error in the mean
                    final_unc = u.sqrt( system_data['d'+data_type+'_1']**2 + system_data['d'+data_type+'_2']**2 )
                    std_err = u.sqrt( 0.5*( (system_data[data_type+'_1']-final_val)**2 + (system_data[data_type+'_2']-final_val)**2) )
                    if std_err > final_unc:
                        final_unc = std_err
                    system_data['d'+data_type] = final_unc
                #Otherwise first convert to free energy then take mean
                elif 'Kd' in data_type: #First convert to free energy then take mean
                    # If we have Kd data instead of Ka data, convert
                    if 'Kd_1' in system_data and not 'Ka_1' in system_data:
                        system_data['Ka_1'] = 1./system_data['Kd_1']
                        # Handle uncertainty -- 1/Kd^2 * dKd
                        system_data['dKa_1'] = system_data['dKd_1']/(system_data['Kd_1']**2)
                        system_data['Ka_2'] = 1./system_data['Kd_2']
                        # Handle uncertainty -- 1/Kd^2 * dKd
                        system_data['dKa_2'] = system_data['dKd_2']/(system_data['Kd_2']**2)
                elif 'Ka' in data_type:
                    if 'Ka_1' in system_data and not 'Ka' in system_data:
                        # Now convert to free energy
                        DG_1, dDG_1 = compute_DG(system_data['Ka_1'], system_data['dKa_1'])
                        DG_2, dDG_2 = compute_DG(system_data['Ka_2'], system_data['dKa_2'])
                        # Take mean
                        DG = (DG_1+DG_2)/2.
                        # Compute uncertainty
                        final_unc = u.sqrt( (dDG_1)**2 + (dDG_2)**2)
                        std_err = u.sqrt( 0.5*( (DG_1-DG)**2 + (DG_2-DG)**2) )
                        if std_err > final_unc:
                            final_unc = std_err
                        # Convert back to Ka and store
                        Ka, dKa = compute_Ka( DG, final_unc)
                        system_data['Ka'] = Ka
                        system_data['dKa'] = dKa


        # Incorporate the relative concentration uncertainties into quantities.
        # Skip this for the Gibb data, where concentration errors are already accounted for and we already have free energy
        TDS = None
        dTDS = None
        DG = None
        dDG = None
        if not 'OA' in system_name:
            for k in ['Ka', 'DH']:
                quantity = system_data[k]
                # Compute relative uncertainty
                relative_uncertainty = system_data['d' + k]/quantity
                # Use upper-bound of 1% if <1% is reported. Keep track of these molecules.
                if relative_uncertainty is None:
                    upper_bound_molecules[k].add(system_name)
                    relative_uncertainty = 0.01
                # Incorporate the relative concentration uncertainties into quantities.
                relative_uncertainty = u.sqrt( relative_uncertainty**2 + RELATIVE_TITRANT_CONC_ERROR**2)
                # Convert relative to absolute errors.
                system_data['d' + k] = abs(quantity * relative_uncertainty)

            # Propagate Ka and DH error into DG and TDS.
            DG, dDG = compute_DG(system_data['Ka'], system_data['dKa'])
            system_data['DG'] = DG
            system_data['dDG'] = dDG
            TDS, dTDS = compute_TDS(system_data['DG'], system_data['dDG'],
                                    system_data['DH'], system_data['dDH'])
            system_data['TDS'] = TDS
            system_data['dTDS'] = dTDS

        # If we have a free energy but not a Ka, compute Ka
        if not 'Ka' in system_data:
            try:
                system_data['Ka'], system_data['dKa'] = compute_Ka(system_data['DG'], system_data['dDG'])
            except TypeError:
                if system_data['DG']=='ND':
                    system_data['Ka']='ND'
                    system_data['dKa']='ND'

        # Strip units.
        strip_units(system_data)

        # Consistency checks.
        if system_data['TDS']!='ND' and system_data['DG']!='ND' and system_data['DH']!='ND':
            assert np.isclose(system_data['DG'], system_data['DH'] - system_data['TDS'], atol=0.10000000000001, rtol=0.0)

            if DG is not None:
                computed_DG = DG.value_in_unit(u.kilocalories_per_mole)
                assert np.isclose(np.around(computed_DG, decimals=2), system_data['DG'], atol=0.0200000000000001, rtol=0.0)
            if TDS is not None:
                computed_TDS = TDS.value_in_unit(u.kilocalories_per_mole)
                assert np.isclose(np.around(computed_TDS, decimals=2), system_data['TDS'], atol=0.0200000000000001, rtol=0.0)


        # Report only error most significant digit.
        for k in ['Ka', 'DH', 'TDS', 'DG']:
            if k in system_data:
                quantity, uncertainty = system_data[k], system_data['d' + k]
                if uncertainty is not None:
                    system_data[k], system_data['d' + k] = reduce_to_first_significant_digit(quantity, uncertainty)

    # Create output JSON file.
    with open('experimental_measurements.json', 'w') as f:
        json.dump(output_dict, f)

    # Create output CSV file.
    # Convert single dict to list of dicts.
    csv_dicts = []
    for system_id, system_data in output_dict.items():
        csv_dict = OrderedDict([('ID', system_id)])
        csv_dict.update(system_data)
        csv_dicts.append(csv_dict)
    with open('experimental_measurements.csv', 'w') as f:
        writer = csv.DictWriter(f, csv_dicts[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(csv_dicts)

    # Create a LaTex table.
    os.makedirs('PDFTable', exist_ok=True)
    old_host = ''
    with open('PDFTable/experimental_measurements.tex', 'w', encoding='utf-8') as f:
        f.write('\\documentclass{article}\n'
                '\\usepackage[a4paper,margin=0.4in,tmargin=0.5in,landscape]{geometry}\n'
                '\\usepackage{tabu}\n'
                '\\pagenumbering{gobble}\n'
                '\\begin{document}\n'
                '\\begin{center}\n'
                '\\footnotesize\n'
                '\\begin{tabu}')

        # Cell alignment.
        field_names = ['ID', 'name', '$K_a$ (M$^{-1}$)', '$\\Delta G$ (kcal/mol) $^{(a)}$', '$\\Delta H$ (kcal/mol)', '$T\\Delta S$ (kcal/mol) $^{(b)}$', '$n$']
        f.write('{| ' + ' | '.join(['c' for _ in range(len(field_names))]) + ' |}\n')

        # Table header.
        f.write('\\hline\n')
        f.write('\\rowfont{\\bfseries} ' + ' & '.join(field_names) + ' \\\\\n')
        f.write('\\hline\n')

        # Print lines.
        for csv_dict in csv_dicts:

            # Separate hosts with a double horizontal line.
            host_name = csv_dict['ID'].split('-')[0]
            if host_name != old_host:
                f.write('\\hline\n')
                old_host = host_name

            if csv_dict['ID']=='clip-g10' or 'OA-g5' in csv_dict['ID']:
                # One name can't be dealt with; reformat
                csv_dict['name'] = "Can't format in LaTeX"




            row = '{ID} & {name}'
            for k in ['Ka', 'DG', 'DH', 'TDS']:
                row += ' & '

                # Report Ka in scientific notation.
                if k == 'Ka':
                    if not isinstance(k, str):
                        first_significant_digit = math.floor(math.log10(abs(csv_dict['d' + k])))
                        csv_dict['d' + k] /= 10**first_significant_digit
                        csv_dict[k] /= 10**first_significant_digit
                        row += '('
                row += '{' + k + '} +- {d' + k + '}'
                if k == 'Ka':
                    if not isinstance(k, str):
                        row += ') $\\times$ 10'
                        if first_significant_digit != 1:
                            row += '$^{{{{{}}}}}$'.format(first_significant_digit)

                # Check if we used the upperbound.
                superscript = ''
                # if k != 'DG' and csv_dict['ID'] in upper_bound_molecules[k]:
                #     superscript += 'a'
                if k == 'Ka':
                    if csv_dict['n'] == 0.33:
                        superscript += 'd'
                    elif csv_dict['n'] == 0.5 or csv_dict['n'] == 2:
                        superscript += 'c'
                if superscript != '':
                    row += ' $^{{(' + superscript + ')}}$'

            row += (' & {n: .2f} \\\\\n'
                    '\\hline\n')

            row = row.format(**csv_dict)

            # Escape underscores for latex formatting
            row = row.replace('_','\_')

            # Write
            f.write(row)

        f.write('\end{tabu}\end{center}\\vspace{5mm}\n'
                'All quantities are reported as point estimate +- statistical error from the ITC data fitting procedure. '
                'The upper bound ($1\%$) was used for errors reported to be $<1\%$. We also included a 3\% relative '
                'uncertainty in the titrant concentration assuming the stoichiometry coefficient to be fitted to the ITC '
                'data [1] for the Isaacs (TrimerTrip) and Gilson (cyclodextrin derivatives) datasets, where concentration'
                'error had not been factored in to the original error estimates. For the OA/exoOA sets, provided uncertainties'
                'already included concentration error.\\\\\n'
                '($^a$) Statistical errors were propagated from the $K_a$ measurements. \\\\\n'
                '($^b$) All experiments were performed at 298 K. \\\\\n'
                '($^c$) Units of M$^{-2}$. \\\\\n'
                '($^d$) Units of M$^{-3}$.\n'
                '\end{document}\n')
