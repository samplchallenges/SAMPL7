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
# The relative titrant concetnration error is disabled for now
#RELATIVE_TITRANT_CONC_ERROR = 0.03

CLIP_GUESTS_SMILES_PATH = '../../Isaacs_clip/guest_files/trimertrip_guest_smiles.txt'
GDCC_GUESTS_SMILES_PATH = '../../GDCC_and_guests/guest_files/GDCC_guest_smiles.txt'
CD_GUESTS_SMILES_PATH = '../../cyclodextrin_derivatives/guest_files/cyclodextrin_guest_smiles.txt'
CLIP_GUESTS_NAMES_PATH = '../../Isaacs_clip/guest_files/trimertrip_guest_names.txt'
GDCC_GUESTS_NAMES_PATH = '../../GDCC_and_guests/guest_files/GDCC_guest_names.txt'
CD_GUESTS_NAMES_PATH = '../../cyclodextrin_derivatives/guest_files/cyclodextrin_guest_names.txt'

# Experimental results as provided by the Gibb, Isaacs and Gilson groups.
# The error is relative. None means that the error is <1%.
EXPERIMENTAL_DATA = OrderedDict([

    ('clip-g1', OrderedDict([
        ('Kd_1', 34.2e-6 * u.molar), ('dKd_1', 3.29e-6 * u.molar),
        ('DH_1', -6.03 * u.kilocalories_per_mole), ('dDH_1', 0.260 * u.kilocalories_per_mole),
        ('Kd_2', 29.6e-6 * u.molar), ('dKd_2', 7.70e-6 * u.molar),
        ('DH_2', -6.14 * u.kilocalories_per_mole), ('dDH_2', 0.696 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g2', OrderedDict([
        ('Kd_1', 749e-9 * u.molar), ('dKd_1', 17.7e-9 * u.molar),
        ('DH_1', -8.58 * u.kilocalories_per_mole), ('dDH_1', 0.021 * u.kilocalories_per_mole),
        ('Kd_2', 829e-9 * u.molar), ('dKd_2', 40.8e-9 * u.molar),
        ('DH_2', -8.95 * u.kilocalories_per_mole), ('dDH_2', 0.053 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g3', OrderedDict([
        ('Kd_1', 43.5e-9 * u.molar), ('dKd_1', 3.39e-9 * u.molar),
        ('DH_1', -10.8 * u.kilocalories_per_mole), ('dDH_1', 0.044 * u.kilocalories_per_mole),
        ('Kd_2', 41.3e-9 * u.molar), ('dKd_2', 3.24e-9 * u.molar),
        ('DH_2', -10.9 * u.kilocalories_per_mole), ('dDH_2', 0.043 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g15', OrderedDict([
        ('Kd_1', 18.3e-9 * u.molar), ('dKd_1', 1.00e-9 * u.molar),
        ('DH_1', -12.8 * u.kilocalories_per_mole), ('dDH_1', 0.033 * u.kilocalories_per_mole),
        ('Kd_2', 20.0e-9 * u.molar), ('dKd_2', 8.74e-10 * u.molar),
        ('DH_2', -12.7 * u.kilocalories_per_mole), ('dDH_2', 0.028 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g12', OrderedDict([
        ('Kd_1', 830e-9 * u.molar), ('dKd_1', 23.3e-9 * u.molar),
        ('DH_1', -8.54 * u.kilocalories_per_mole), ('dDH_1', 0.027 * u.kilocalories_per_mole),
        ('Kd_2', 827e-9 * u.molar), ('dKd_2', 31.0e-9 * u.molar),
        ('DH_2', -8.25 * u.kilocalories_per_mole), ('dDH_2', 0.034 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g5', OrderedDict([
        ('Kd_1', 7.07e-9 * u.molar), ('dKd_1', 1.13e-9 * u.molar),
        ('DH_1', -11.5 * u.kilocalories_per_mole), ('dDH_1', 0.094 * u.kilocalories_per_mole),
        ('Kd_2', 6.63e-9 * u.molar), ('dKd_2', 8.99e-10 * u.molar),
        ('DH_2', -11.3 * u.kilocalories_per_mole), ('dDH_2', 0.07 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g16', OrderedDict([
        ('Kd_1', 3.55e-9 * u.molar), ('dKd_1', 7.80e-10 * u.molar),
        ('DH_1', -11.3 * u.kilocalories_per_mole), ('dDH_1', 0.068 * u.kilocalories_per_mole),
        ('Kd_2', 3.27e-9 * u.molar), ('dKd_2', 8.48e-10 * u.molar),
        ('DH_2', -11.2 * u.kilocalories_per_mole), ('dDH_2', 0.072 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g17', OrderedDict([
        ('Kd_1', 1.97e-9 * u.molar), ('dKd_1', 1.06e-9 * u.molar),
        ('DH_1', -10.4 * u.kilocalories_per_mole), ('dDH_1', 0.123 * u.kilocalories_per_mole),
        ('Kd_2', 2.20e-9 * u.molar), ('dKd_2', 5.76e-10 * u.molar),
        ('DH_2', -10.4 * u.kilocalories_per_mole), ('dDH_2', 0.064 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g9', OrderedDict([
        ('Kd_1', 2.8e-6 * u.molar), ('dKd_1', 113e-9 * u.molar),
        ('DH_1', -4.83 * u.kilocalories_per_mole), ('dDH_1', 0.036 * u.kilocalories_per_mole),
        ('Kd_2', 2.79e-6 * u.molar), ('dKd_2', 162e-9 * u.molar),
        ('DH_2', -4.72 * u.kilocalories_per_mole), ('dDH_2', 0.046 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g6', OrderedDict([
        ('Kd_1', 88.3e-9 * u.molar), ('dKd_1', 9.44e-9 * u.molar),
        ('DH_1', -10.1 * u.kilocalories_per_mole), ('dDH_1', 0.119 * u.kilocalories_per_mole),
        ('Kd_2', 97.0e-9 * u.molar), ('dKd_2', 13.6e-9 * u.molar),
        ('DH_2', -10.3 * u.kilocalories_per_mole), ('dDH_2', 0.165 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g11', OrderedDict([
        ('Kd_1', 245e-9 * u.molar), ('dKd_1', 22.3e-9 * u.molar),
        ('DH_1', -7.41 * u.kilocalories_per_mole), ('dDH_1', 0.084 * u.kilocalories_per_mole),
        ('Kd_2', 238e-9 * u.molar), ('dKd_2', 22.2e-9 * u.molar),
        ('DH_2', -7.35 * u.kilocalories_per_mole), ('dDH_2', 0.084 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g10', OrderedDict([
        ('Kd_1', 902e-9 * u.molar), ('dKd_1', 64.8e-9 * u.molar),
        ('DH_1', -5.88 * u.kilocalories_per_mole), ('dDH_1', 0.049 * u.kilocalories_per_mole),
        ('Kd_2', 1.17e-6 * u.molar), ('dKd_2', 72.6e-9 * u.molar),
        ('DH_2', -5.80 * u.kilocalories_per_mole), ('dDH_2', 0.047 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g8', OrderedDict([
        ('Kd_1', 114e-9 * u.molar), ('dKd_1', 6.79e-9 * u.molar),
        ('DH_1', -10.5 * u.kilocalories_per_mole), ('dDH_1', 0.044 * u.kilocalories_per_mole),
        ('Kd_2', 120e-9 * u.molar), ('dKd_2', 5.34e-9 * u.molar),
        ('DH_2', -10.6 * u.kilocalories_per_mole), ('dDH_2', 0.033 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g18', OrderedDict([
        ('Kd_1', 17.2e-9 * u.molar), ('dKd_1', 1.42e-9 * u.molar),
        ('DH_1', -12.4 * u.kilocalories_per_mole), ('dDH_1', 0.045 * u.kilocalories_per_mole),
        ('Kd_2', 19.8e-9 * u.molar), ('dKd_2', 2.34e-9 * u.molar),
        ('DH_2', -12.3 * u.kilocalories_per_mole), ('dDH_2', 0.069 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g19', OrderedDict([
        ('Kd_1', 2.80e-9 * u.molar), ('dKd_1', 1.53e-10 * u.molar),
        ('DH_1', -13.7 * u.kilocalories_per_mole), ('dDH_1', 0.039 * u.kilocalories_per_mole),
        ('Kd_2', 2.74e-9 * u.molar), ('dKd_2', 6.04e-9 * u.molar),
        ('DH_2', -13.6 * u.kilocalories_per_mole), ('dDH_2', 0.144 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
    ])),
    ('clip-g7', OrderedDict([
        ('Kd_1', 16.8e-6 * u.molar), ('dKd_1', 652e-9 * u.molar),
        ('DH_1', -6.61 * u.kilocalories_per_mole), ('dDH_1', 0.088 * u.kilocalories_per_mole),
        ('Kd_2', 17.2e-6 * u.molar), ('dKd_2', 1.24e-6 * u.molar),
        ('DH_2', -6.80 * u.kilocalories_per_mole), ('dDH_2', 0.170 * u.kilocalories_per_mole),
        ('TDS', None), ('dTDS', None),
        ('n', 1)
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
        dKa = u.sqrt(dKadDG**2 * dDG**2) * 1/concentration_unit
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
        'GDCC' : load_smiles(GDCC_GUESTS_SMILES_PATH),
        'CD' : load_smiles(CD_GUESTS_SMILES_PATH),
    }

    names_by_host = {
        'clip': load_names(CLIP_GUESTS_NAMES_PATH),
        'GDCC' : load_names(GDCC_GUESTS_NAMES_PATH),
        'CD' : load_names(CD_GUESTS_NAMES_PATH),
    }

    for host in ['clip', 'GDCC', 'CD']:
        molecule_names[host] = {}
        for smi, gid in smiles_by_host[host]:
            for name, gid2 in names_by_host[host]:
                if gid==gid2:
                    molecule_names[host][gid] = name, smi

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
                    final_unc = u.sqrt( system_data[data_type+'_1']**2 + system_data[data_type+'_2']**2 )
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
                        print(final_unc, std_err)
                        if std_err > final_unc:
                            final_unc = std_err
                        # Convert back to Ka and store
                        Ka, dKa = compute_Ka( DG, final_unc)
                        system_data['Ka'] = Ka
                        system_data['dKa'] = dKa


        # Incorporate the relative concentration uncertainties into quantities.
        #for k in ['Ka', 'DH']:
        #    quantity = system_data[k]
        #    relative_uncertainty = system_data['d' + k]
        #    # Use upper-bound of 1% if <1% is reported. Keep track of these molecules.
        #    if relative_uncertainty is None:
        #        upper_bound_molecules[k].add(system_name)
        #        relative_uncertainty = 0.01
        #    # Incorporate the relative concentration uncertainties into quantities.
        #    relative_uncertainty += RELATIVE_TITRANT_CONC_ERROR
        #    # Convert relative to absolute errors.
        #    system_data['d' + k] = abs(quantity * relative_uncertainty)

        # Propagate Ka and DH error into DG and TDS.
        print(system_data)
        DG, dDG = compute_DG(system_data['Ka'], system_data['dKa'])
        print(system_data['Ka'], system_data['dKa'])
        print(DG, dDG)
        system_data['DG'] = DG
        system_data['dDG'] = dDG
        TDS, dTDS = compute_TDS(system_data['DG'], system_data['dDG'],
                                system_data['DH'], system_data['dDH'])
        system_data['TDS'] = TDS
        system_data['dTDS'] = dTDS

        # Strip units.
        strip_units(system_data)

        # Consistency checks.
        computed_DG = DG.value_in_unit(u.kilocalories_per_mole)
        computed_TDS = TDS.value_in_unit(u.kilocalories_per_mole)
        assert np.isclose(system_data['DG'], system_data['DH'] - system_data['TDS'], atol=0.020000000000001, rtol=0.0)
        assert np.isclose(np.around(computed_TDS, decimals=2), system_data['TDS'], atol=0.0200000000000001, rtol=0.0)
        assert np.isclose(np.around(computed_DG, decimals=2), system_data['DG'], atol=0.0200000000000001, rtol=0.0)

        # Report only error most significant digit.
        #for k in ['Ka', 'DH', 'TDS', 'DG']:
        #    quantity, uncertainty = system_data[k], system_data['d' + k]
        #    if uncertainty is not None:
        #        system_data[k], system_data['d' + k] = reduce_to_first_significant_digit(quantity, uncertainty)

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

            row = '{ID} & {name}'
            for k in ['Ka', 'DG', 'DH', 'TDS']:
                row += ' & '

                # Report Ka in scientific notation.
                if k == 'Ka':
                    first_significant_digit = math.floor(math.log10(abs(csv_dict['d' + k])))
                    csv_dict['d' + k] /= 10**first_significant_digit
                    csv_dict[k] /= 10**first_significant_digit
                    row += '('
                row += '{' + k + '} +- {d' + k + '}'
                if k == 'Ka':
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

            row += (' & {n} \\\\\n'
                    '\\hline\n')
            f.write(row.format(**csv_dict))

        f.write('\end{tabu}\end{center}\\vspace{5mm}\n'
                'All quantities are reported as point estimate +- statistical error from the ITC data fitting procedure. '
                #'The upper bound ($1\%$) was used for errors reported to be $<1\%$. We also included a 3\% relative '
                #'uncertainty in the titrant concentration assuming the stoichiometry coefficient to be fitted to the ITC '
                #'data [1]. This is exact only for the OA/TEMOA sets (with the exception of OA-G5, TEMOA-G5, and TEMOA G7). '
                #'For the other guests, we may expand the error analysis to include also the effect of the uncertainties '
                #'in titrand concentration and cell volume. \\\\\n'
                '($^a$) Statistical errors were propagated from the $K_a$ measurements. \\\\\n'
                #'($^b$) All experiments were performed at 298 K. \\\\\n'
                '($^c$) Units of M$^{-2}$. \\\\\n'
                '($^d$) Units of M$^{-3}$.\n'
                '\end{document}\n')
