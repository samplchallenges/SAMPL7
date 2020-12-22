#!/usr/bin/env python

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================
import os
import glob
import io
import collections
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats
from pylab import rcParams
import math


# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
relative_microstate_free_energy_SUBMISSIONS_DIR_PATH = './relative_microstate_free_energy_predictions/'
EXPERIMENTAL_DATA_FILE_PATH = './pKa_experimental_values.csv'
USER_MAP_FILE_PATH = './SAMPL7-user-map.csv'


# =============================================================================
# UTILITY CLASSES
# =============================================================================

class IgnoredSubmissionError(Exception):
    """Exception used to signal a submission that must be ignored."""
    pass


class BadFormatError(Exception):
    """Exception used to signal a submission with unexpected formatting."""
    pass


class SamplSubmission:
    """A generic SAMPL submission.
    Parameters
    ----------
    file_path : str
        The path to the submission file.
    Raises
    ------
    IgnoredSubmission
        If the submission ID is among the ignored submissions.
    """


    # The IDs of submissions used for reference calculations
    REF_SUBMISSIONS = ['REF00']

    # Section of the submission file.
    SECTIONS = {}

    # Sections in CSV format with columns names.
    CSV_SECTIONS = {}

    def __init__(self, file_path, user_map):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_data = file_name.split('-')

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']
        self.data = pd.DataFrame(data=self.data)
        self.file_name = file_name

        self.method_name = sections['Name'][0] #want this to take the place of the 5 letter code

        # Check if this is a reference submission
        self.reference_submission = False
        #if self.method_name in self.REF_SUBMISSIONS:
        if "REF" in self.method_name or "NULL" in self.method_name:
            print("REF found: ", self.method_name)
            self.reference_submission = True

    @classmethod
    def _read_lines(cls, file_path):
        """Generator to read the file and discard blank lines and comments."""
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                # Strip whitespaces.
                line = line.strip()
                # Don't return blank lines and comments.
                if line != '' and line[0] != '#':
                    yield line

    @classmethod
    def _load_sections(cls, file_path):
        """Load the data in the file and separate it by sections."""
        #print("file_path",file_path)
        sections = {}
        current_section = None
        for line in cls._read_lines(file_path):
            # Check if this is a new section.
            if line[:-1] in cls.SECTIONS:
                current_section = line[:-1]
            else:
                if current_section is None:
                    import pdb
                    pdb.set_trace()
                try:
                    sections[current_section].append(line)
                except KeyError:
                    sections[current_section] = [line]

        # Check that all the sections have been loaded.
        found_sections = set(sections.keys())
        if found_sections != cls.SECTIONS:
            raise BadFormatError('Missing sections: {}.'.format(found_sections - cls.SECTIONS))

        # Create a Pandas dataframe from the CSV format.
        for section_name in cls.CSV_SECTIONS:
            csv_str = io.StringIO('\n'.join(sections[section_name]))
            columns = cls.CSV_SECTIONS[section_name]
            id_column = columns[0]
            #print("trying", sections)
            section = pd.read_csv(csv_str, index_col=id_column, names=columns, skipinitialspace=True)
            #section = pd.read_csv(csv_str, names=columns, skipinitialspace=True)
            sections[section_name] = section
        return sections

    @classmethod
    def _create_comparison_dataframe(cls, column_name, submission_data, experimental_data):
        """Create a single dataframe with submission and experimental data."""
        # Filter only the systems IDs in this submissions.


        experimental_data = experimental_data[experimental_data.index.isin(submission_data.index)] # match by column index
        # Fix the names of the columns for labelling.
        submission_series = submission_data[column_name]
        submission_series.name += ' (calc)'
        experimental_series = experimental_data[column_name]
        experimental_series.name += ' (expt)'

        # Concatenate the two columns into a single dataframe.
        return pd.concat([experimental_series, submission_series], axis=1)




class pKaSubmission(SamplSubmission):
    """A submission for pKa challenge.
    Parameters
    ----------
    file_path : str
        The path to the submission file
    Raises
    ------
    IgnoredSubmission
        If the submission ID is among the ignored submissions.
    """


    # Section of the submission file.
    SECTIONS = {"Predictions",
                "Participant name",
                "Participant organization",
                "Name",
                "Compute time",
                "Computing and hardware",
                "Software",
                "Category",
                "Method",
                "Ranked"}

    # Sections in CSV format with columns names.

    CSV_SECTIONS = {"Predictions": ("Molecule ID",
                                    "ID tag",
                                    "total charge",
                                    "pKa mean",
                                    "pKa SEM",
                                    "pKa model uncertainty")}
                                    #{"Predictions": ("Molecule ID",
                                    #"ID tag",
                                    #"total charge",
                                    #"Relative microstate free energy",
                                    #"Relative microstate free energy SEM",
                                    #"Relative microstate free energy model uncertainty",
                                    #"SMILES of extra microstate")}


    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        print("file_name: \n", file_name)
        file_data = file_name.split('-')


        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']  # This is a pandas DataFrame.
        self.method_name = sections['Name'][0]
        self.category = sections['Category'][0] # New section for pKa challenge.
        self.participant = sections['Participant name'][0].strip()
        self.organization = sections['Participant organization'][0].strip()
        self.ranked = sections['Ranked'][0].strip() =='True'

         # Check if this is a reference submission
        self.reference_submission = False
        if "REF" in self.method_name or "NULL" in self.method_name:
            self.reference_submission = True



# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def load_submissions(directory_path, user_map):
    """Load submissions from a specified directory using a specified user map.
    Optional argument:
        ref_ids: List specifying submission IDs (alphanumeric, typically) of
        reference submissions which are to be ignored/analyzed separately.
    Returns: submissions
    """
    submissions = []
    for file_path in glob.glob(os.path.join(directory_path, '*.csv')):
        print("Trying to load %s" % file_path)
        try:
            submission = pKaSubmission(file_path, user_map)

        except IgnoredSubmissionError:
            print("Error on %s" % file_path)
            continue
        submissions.append(submission)
    return submissions


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    sns.set_style('whitegrid')
    sns.set_context('paper')

    # Read experimental data.
    with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
        # experimental_data = pd.read_json(f, orient='index')
        names = ('Molecule ID', 'Relative microstate free energy', 'Relative microstate free energy SEM',
                 'Assay Type', 'Isomeric SMILES')
        experimental_data = pd.read_csv(f, names=names, skiprows=1)

    # Convert numeric values to dtype float.
    for col in experimental_data.columns[1:7]:
        experimental_data[col] = pd.to_numeric(experimental_data[col], errors='coerce')


    experimental_data.set_index("Molecule ID", inplace=True)
    experimental_data["Molecule ID"] = experimental_data.index
    #print("Experimental data: \n", experimental_data)

    # Import user map.
    with open(USER_MAP_FILE_PATH, 'r') as f:
        user_map = pd.read_csv(f)

# Macro pKa calculation, adapted from David's email
# =======

import numpy as np
from scipy.special import logsumexp
from scipy.optimize import fsolve

# Compute beta and other constants
kB = 1.381 * 6.02214 / 1000.0  # [kJ/(mol K)]
beta = 1. / (kB * 300)  # [mol/kJ]
beta = beta * 4.186
C_unit = 1 / beta * np.log(10)

# Store in list of tupes of (state, relative free energy, charge).


# Test some Tielker/ECRISM cases -- note that these need their units changed before analysis
# state_details = [(3, 7.91 * C_unit, -1), (1, -6.66 * C_unit, -1), (2, -7.52 * C_unit, 0), (4, -12.08 * C_unit, 0),
#                 (5, -2.33 * C_unit, 1)]


# Let's look at molecule 42 as it's a little simpler
# state_details = [ (1, 0.54*C_unit, -1), (2, 0.3*C_unit, 1), (3, -5.05*C_unit, 0)]
# Tielker SM26:
# state_details = [ (1, 5.53*C_unit, -1), (3, 19.92*C_unit, -1), (2, 12.59*C_unit, 0), (4, 4.82*C_unit, 0), (5, 9.95*C_unit, 1)]
# Tielker SM27, to handle simple case:
# state_details = [ (1, 10.17*C_unit, -1)]

# Test some Beckstein/Iorga cases
# Molecule 25
# state_details = [ (1, -2.7, -1), (2, -2, 0), (3, 4.53, -1), (4, -5.75, 0), (5, 0.65, 1)]
# Beckstein/Iorga molecule 42
# state_details = [ (1, 0.15, -1), (2, 0.79, 1), (3, -1.95, 0)]

# Let's try the IEFPCM one for state 42
# state_details = [(1, 6.61, -1), (2, 14.25, 1)]


# Compute free energy as a function of pH for states
# WITHIN-charge transitions have same pH dependence
def DeltaG(pH, state, state_details):
    for item in state_details:
        if item[0] == state:
            # 0 serves as the reference state; all transitions are away from 0.
            if item[2] == -1:
                DeltaM = 1
            elif item[2] == 1:
                DeltaM = -1
            elif item[2] ==2:
                DeltaM=-2
            else:
                DeltaM = 0  # Hack to capture fact that pH dependence of states at same formal charge is same/cancels
            # Compute value
            return (item[1] - pH * DeltaM * C_unit)  # Gunner eq 3


# Compute populations for charge states (without normalization, due to laziness/since it'll drop out)
def pop_charge(pH, formal_charge, state_details):
    free_energies = []
    for item in state_details:
        if item[2] == formal_charge:
            free_energies.append(-beta * DeltaG(pH, item[0], state_details))
    if formal_charge == 0:
        free_energies.append(0 * pH)
    return np.exp(logsumexp(free_energies))


# get G of each group
# Given a group of microstates, which share the same net charge in this case, what is the average free energy of this
# group?
def getG(msgroup):
    # Input: msgroup
    #     msgroup is a list of microstates
    #     each microstate is a tuple: (moleculeID, RFE, formal_charge)
    # Output:
    #     canonical ensemble free energy of this group of microstates in unit Kcal/mol

    # Get the normalized population (sum of P to be 1) based on Boltzmann distribution
    Pi_raw = np.array([np.exp(-beta*ms[1]) for ms in msgroup])
    Pi_norm = Pi_raw/sum(Pi_raw)

    # Compose free energy of this group
    # ref: https://en.wikipedia.org/wiki/Partition_function_(statistical_mechanics)#Calculating_the_thermodynamic_total_energy
    E = sum(np.array([ms[1] for ms in msgroup]) * Pi_norm)
    TS = -sum(Pi_norm * np.log(Pi_norm))/beta
    G = E - TS
    return G

class Macro_pKa:
    def __init__(self):
        self.molecule = ""
        self.transition_from = 0      # formal charge for a pKa, transition from
        self.transition_to = 0        # formal charge for a pKa, transition to
        self.pKa_bytitration = 0.0    # Macro-pKa calculated by titration method
        self.pKa_bydG = 0.0           # Macro-pKa calculated by delta G method


def get_macropka(rfe_data):
    # Input: rfe_data
    #     rfe_data is a pandas table of rfe submission by one author.
    #     each row is a molecule microstate. The columns contain state(ID), fre in Kcal/mol, charge, and other fields.
    # Output:
    #     A list of macro-pKas, in data structure defined by class Macro_pKa.

    macropkas = []

    # Extract each molecule from pandas table, only use three fields: "IT Tag", "total charge", and "pKa mean" (rfe)
    molecules = {}
    for index, row in rfe_data.iterrows():
        SM = index
        state = row["ID tag"]
        charge = row["total charge"]
        rfe = row["pKa mean"]

        # Since one author will submit multiple molecules (SM25, SM26 etc), and one molecule has multiple rows for
        # microstates, molecules are stored in a dictionary, indexed by the molecule name (SM25, SM26...) and have value
        # as a list of microstates.
        if SM in molecules:
            molecules[SM].append((state, rfe, charge))
        else:
            molecules[SM] = [(state, rfe, charge)]

    # Loop over molecules, convert to state_details
    SM_names = [x for x in molecules.keys()]
    SM_names.sort()
    for sm_name in SM_names:
        state_details = molecules[sm_name]
        # state_details is a tuple in form of ('SM29_micro001', 9.88, -1)
        # print(state_details)

        # Figure out what formal charges are present in states
        formal_charges = [info[2] for info in state_details]

        #print(sm_name)

        # group microstates into groups based their formal charge
        msgroup_p2 = [state for state in state_details if state[2] == 2]   # microstates with formal charge +2
        msgroup_p1 = [state for state in state_details if state[2] == 1]   # microstates with formal charge +1
        msgroup_p0 = [state for state in state_details if state[2] == 0]   # microstates with formal charge 0
        msgroup_p0.append(("reference state", 0, 0))                       # add back reference state
        msgroup_n1 = [state for state in state_details if state[2] == -1]  # microstates with formal charge -1

        # for reaction A -> B, assuming a proton release reaction that transits from high to low formal charge:
        #     ΔGAB = (-1)(C_unit)(pH - pKaBA)
        # In delta G method, A and B are no longer microstates, they are instead microstete groups with the same
        # formal charges, but the theory still holds. Therefore when pH = 0, we have:
        #     pKaBA = ΔGAB/C_unit

        # Compute +2 to +1 transition
        if 2 in formal_charges:
            pka = Macro_pKa()
            pka.molecule = sm_name.split("_")[0]
            pka.transition_from = 2
            pka.transition_to = 1

            # titration method given my David's group
            init_guess = -15
            func_2to1 = lambda pH : (pop_charge(pH, 2, state_details) - pop_charge(pH, 1, state_details))
            pH_solution_2to1, infodict, ier, mesg = fsolve(func_2to1, init_guess, factor = 0.1, full_output=True)
            # If message indicates poor convergence, change initial guess and try again
            if 'The iteration is not making good progress' in mesg:
                init_guess-=5
            pH_solution_2to1, infodict, ier, mesg = fsolve(func_2to1, init_guess, factor = 0.1, full_output=True)
            # If still poor convergence, print warning (MAY NEED BETTER SOLUTION TO THIS)
            if 'The iteration is not making good progress' in mesg:
                print("WARNING: Numerical problems encountered with fsolv")
            pka.pKa_bytitration = pH_solution_2to1

            # delta G method given by newbooks (Junjun Mao)
            dG = getG(msgroup_p1) - getG(msgroup_p2)
            pka.pKa_bydG = (dG / C_unit)

            macropkas.append(pka)

        # Compute +1 to 0 transition
        if 1 in formal_charges:
            pka = Macro_pKa()
            pka.molecule = sm_name.split("_")[0]
            pka.transition_from = 1
            pka.transition_to = 0

            # titration method given my David's group
            init_guess = -5
            func_10 = lambda pH: (pop_charge(pH, 1, state_details) - pop_charge(pH, 0, state_details))
            pH_solution_1to0, infodict, ier, mesg = fsolve(func_10, init_guess, factor=0.1, full_output=True)
            if 'The iteration is not making good progress' in mesg:
                init_guess-=3
            pH_solution_1to0, infodict, ier, mesg = fsolve(func_10, init_guess, factor=0.1, full_output=True)
            # If still poor convergence, print warning (MAY NEED BETTER SOLUTION TO THIS)
            if 'The iteration is not making good progress' in mesg:
                print("WARNING: Numerical problems encountered with fsolv")
            pka.pKa_bytitration = pH_solution_1to0

            # delta G method given by newbooks (Junjun Mao)
            dG = getG(msgroup_p0) - getG(msgroup_p1)
            pka.pKa_bydG = (dG / C_unit)

            macropkas.append(pka)

        # Compute 0 to -1 transition
        if -1 in formal_charges:
            pka = Macro_pKa()
            pka.molecule = sm_name.split("_")[0]
            pka.transition_from = 0
            pka.transition_to = -1

            # titration method given my David's group
            init_guess = 5
            func_0neg1 = lambda pH: (pop_charge(pH, -1, state_details) - pop_charge(pH, 0, state_details))
            pH_solution_0toneg1, infodict, ier, mesg = fsolve(func_0neg1, init_guess, factor=0.1, full_output=True)
            if 'The iteration is not making good progress' in mesg:
                init_guess+=3
            pH_solution_0toneg1, infodict, ier, mesg = fsolve(func_0neg1, init_guess, factor=0.1, full_output=True)
            # If still poor convergence, print warning (MAY NEED BETTER SOLUTION TO THIS)
            if 'The iteration is not making good progress' in mesg:
                print("WARNING: Numerical problems encountered with fsolv")
            pka.pKa_bytitration = pH_solution_0toneg1

            # delta G method given by newbooks (Junjun Mao)
            dG = getG(msgroup_n1) - getG(msgroup_p0)
            pka.pKa_bydG = (dG / C_unit)

            macropkas.append(pka)

    return macropkas






# ======================================================================================================================
# TO DO:  Convert relative microstate free energies to microscopic pKas, then calculate MACRO pKas from the micro pKas
# ======================================================================================================================

# Load submissions data.
submissions_RFE = load_submissions(relative_microstate_free_energy_SUBMISSIONS_DIR_PATH, user_map)
print(submissions_RFE)

# Loop through each submission, convert relative FE's to micro pKas, then convert to macro pKas
for sub in submissions_RFE:
    print("Submission dataframe \n", sub.data)

print("Experimental data: \n", experimental_data)

# Loop through each submission, convert relative FE's to micro pKas, then convert to macro pKas
for sub in submissions_RFE:
    print("Macro-pKa conversion %s" % sub.participant)
    print("Molecule From  To  pKa(titr)  pKa(dG)")
    # Compute macro pKa by two methods:
    # 1. simulated titration
    # 2. delta G method. Based on canonical ensemble of microstate groups that share the same formal charge.
    macropkas = get_macropka(sub.data)
    for pka in macropkas:
        # Print only cases which differ substantially (and are reasonable) for debugging purposes
        if np.abs(pka.pKa_bytitration-pka.pKa_bydG) > 0.5:# and (np.abs(pka.pKa_bytitration) < 20 and np.abs(pka.pKa_bydG) < 20):
            print("%6s   %2d   %2d    %8.3f %8.3f" %(pka.molecule, pka.transition_from, pka.transition_to, pka.pKa_bytitration, pka.pKa_bydG))

        #print("%6s   %2d   %2d    %8.3f %8.3f" %(pka.molecule, pka.transition_from, pka.transition_to, pka.pKa_bytitration, pka.pKa_bydG))
