import os
import glob
import io
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pylab import rcParams
from matplotlib import cm
#import joypy



# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
pKa_SUBMISSIONS_DIR_PATH = './pKa_predictions'
USER_MAP_FILE_PATH = './SAMPL7-user-map-pKa.csv'


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

    # Section of the submission file.
    SECTIONS = {}

    # Sections in CSV format with columns names.
    CSV_SECTIONS = {}

    def __init__(self, file_path, user_map):
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_data = file_name.split('-')

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']  # This is a list
        self.data = pd.DataFrame(data=self.data) # Now a DataFrame
        #self.name = sections['Name'][0] #want this to take the place of the 5 letter code
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
            section = pd.read_csv(csv_str, index_col=id_column, names=columns, skipinitialspace=True)
            sections[section_name] = section
        return sections


# =============================================================================
# pKa PREDICTION CHALLENGE
# =============================================================================

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

    # The D3R challenge IDs that are handled by this class.
    #CHALLANGE_IDS = {1559}

    # The IDs of the submissions that will be ignored in the analysis.
    #TEST_SUBMISSIONS = {}

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
    CSV_SECTIONS = {"Predictions": ("ID tag",
                                    "Molecule ID",
                                    "total charge",
                                    "relative free energy",
                                    "relative free energy SEM",
                                    "relative free energy model uncertainty")}


    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_data = file_name.split('-')

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']  # This is a pandas DataFrame.
        self.method_name = sections['Name'][0]
        self.category = sections['Category'][0] # New section for pKa challenge.
        self.participant = sections['Participant name'][0].strip()
        self.organization = sections['Participant organization'][0].strip()
        self.ranked = sections['Ranked'][0].strip() =='True'


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
        try:
            submission = pKaSubmission(file_path, user_map)

        except IgnoredSubmissionError:
            continue
        submissions.append(submission)
    return submissions



class pKaSubmissionCollection:
    """A collection of pKa submissions."""


    def __init__(self, submissions, output_directory_path, pKa_submission_collection_file_path, no_outliers = True):
        # Build collection dataframe from the beginning.
        # Build full pKa collection table.

        data = []

        # Submissions for pKa.
        for submission in submissions_RFE:
            #print(submission.file_name)
            if "RFE-NHLBI-TZVP-QM" in submission.method_name and no_outliers:
                continue
            #print(submission.method_name)
            for mol_ID, series in submission.data.iterrows():
                print("mol_ID",mol_ID)
                print(goob)
                ref_state = submission.data.loc[mol_ID, "Molecule ID"]

                RFE_mean_pred_original = submission.data.loc[mol_ID, "relative free energy"]

                RFE_SEM_pred_original = submission.data.loc[mol_ID, "relative free energy SEM"]
                total_charge = submission.data.loc[mol_ID, "total charge"]
                RFE_model_uncertainty_original =  submission.data.loc[mol_ID, "relative free energy model uncertainty"]

                # correct sign + unit
                if submission.file_name in ["pKa-VA-2", "pKa_RodriguezPaluch_SMD_1",
                                            "pKa_RodriguezPaluch_SMD_2", "pKa_RodriguezPaluch_SMD_3"]:
                    sign_error = "yes"
                    RFE_mean_pred = RFE_mean_pred_original*-1

                    RFE_mean_pred = RFE_mean_pred*1.36 #convert submission to kcal/mol
                    RFE_SEM_pred = RFE_SEM_pred_original*1.36
                    RFE_model_uncertainty = RFE_model_uncertainty_original*1.36

                #convert submission to kcal/mol
                if submission.file_name in ["pKa-ECRISM-1"]:

                    RFE_mean_pred = RFE_mean_pred_original*1.36
                    RFE_SEM_pred = RFE_SEM_pred_original*1.36
                    RFE_model_uncertainty = RFE_model_uncertainty_original*1.36

                # fix submission which seems to be in kJ/mol
                if submission.file_name in ["pka-nhlbi-1c"]:
                    sign_error = "yes"
                    RFE_mean_pred = RFE_mean_pred_original*-1

                    RFE_mean_pred = RFE_mean_pred/4.186
                    RFE_SEM_pred = RFE_SEM_pred_original/4.186
                    RFE_model_uncertainty = RFE_model_uncertainty_original/4.186


                #If single transition states are opposite in sign from macro pKa, we assume they made a sign error
                if submission.file_name in ["pKa-ECRISM-1", "pka-nhlbi-1c", "pKa-VA-2",
                                            "pKa_RodriguezPaluch_SMD_1", "pKa_RodriguezPaluch_SMD_2",
                                            "pKa_RodriguezPaluch_SMD_3"]:

                    data.append({
                        'method name': submission.method_name,
                        'file name': submission.file_name,
                        'reference state': ref_state,
                        'ID tag': mol_ID,
                        'total charge': total_charge,
                        'sign correction?': sign_error,
                        'Relative microstate free energy prediction': RFE_mean_pred,
                        'Relative microstate free energy SEM': RFE_SEM_pred,
                        'model uncertainty': RFE_model_uncertainty,
                        'Relative microstate free energy prediction (original)': RFE_mean_pred_original,
                        'Relative microstate free energy SEM (original)': RFE_SEM_pred_original,
                        'model uncertainty (original)': RFE_model_uncertainty_original
                    })
                else:
                    sign_error = "no"
                    data.append({
                        'method name': submission.method_name,
                        'file name': submission.file_name,
                        'reference state': ref_state,
                        'ID tag': mol_ID,
                        'total charge': total_charge,
                        'sign correction?': sign_error,
                        'Relative microstate free energy prediction': RFE_mean_pred_original,
                        'Relative microstate free energy SEM': RFE_SEM_pred_original,
                        'model uncertainty': RFE_model_uncertainty_original
                    })


        # Transform into Pandas DataFrame.
        self.data = pd.DataFrame(data=data)
        self.output_directory_path = output_directory_path

        #print("\n SubmissionCollection: \n")
        #print(self.data)

        # Create general output directory.
        os.makedirs(self.output_directory_path, exist_ok=True)

        # Save collection.data dataframe in a CSV file.
        self.data.to_csv(pKa_submission_collection_file_path)




# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    sns.set_style('whitegrid')
    sns.set_context('paper')


    # Import user map.
    with open(USER_MAP_FILE_PATH, 'r') as f:
        user_map = pd.read_csv(f)

    def read_collection_file(collection_file_path):
        """
        Function to read SAMPL6 collection CSV file that was created by logPubmissionCollection.
        :param collection_file_path
        :return: Pandas DataFrame
        """

        # Check if submission collection file already exists.
        if os.path.isfile(collection_file_path):
            print("Analysis will be done using the existing collection file: {}".format(collection_file_path))

            collection_df = pd.read_csv(collection_file_path, index_col=0)
            #print("\n SubmissionCollection: \n")
            #print(collection_df)
        else:
            raise Exception("Collection file doesn't exist: {}".format(collection_file_path))

        return collection_df

    def append_value(dict_obj, key, value):
        # Check if key exist in dict or not
        if key in dict_obj:
            # Key exist in dict.
            # Check if type of value of key is list or not
            if not isinstance(dict_obj[key], list):
                # If type is not list then make it list
                dict_obj[key] = [dict_obj[key]]
            # Append the value in list
            dict_obj[key].append(value)
        else:
            # As key is not in dict,
            # so, add key-value pair
            dict_obj[key] = value

    def ridge_plot(df, by, column, figsize, colormap, output_directory_path, fig_name):
        print("Making ridge plot")
        plt.close('all')
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 12
        plt.rcParams['ytick.labelsize'] = 12
        plt.rcParams['axes.labelsize'] = 14
        #plt.rcParams['figure.autolayout'] = True
        #plt.tight_layout()

        # Make ridge plot
        #fig, axes = joypy.joyplot(data=df, by=by, column=column, figsize=figsize, colormap=colormap, linewidth=1)
        # Add x-axis label
        axes[-1].set_xlabel(column)



        plt.savefig(output_directory_path + "/" + fig_name+".pdf")


    def ridge_plot_wo_overlap(df, by, column, figsize, colormap, output_directory_path):
        plt.close('all')
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['xtick.labelsize'] = 14
        plt.rcParams['figure.autolayout'] = True
        plt.tight_layout()

        # Make ridge plot
        #fig, axes = joypy.joyplot(data=df, by=by, column=column, figsize=figsize, colormap=colormap, linewidth=1, overlap=0)
        # Add x-axis label
        axes[-1].set_xlabel(column)
        plt.savefig(output_directory_path + "/" + "ridgeplot.pdf")


    def violinplot(df, output_directory_path, width, fig_name):
        print("Making horizontal violin plot")

        plt.close('all')
        data_ordered_by_mol_ID = df.sort_values(["ID tag"], ascending=["True"])

        sns.set(rc={'figure.figsize': (8.27,11.7)})
        sns.violinplot(y="ID tag", x='Relative microstate free energy prediction',
                       data=data_ordered_by_mol_ID, inner='point',
                       linewidth=0.5, width=width)
        plt.tight_layout()
        #plt.savefig(output_directory_path + "/" + "violinplot.pdf")
        plt.savefig(output_directory_path + "/" + fig_name+"_horizontal.pdf")



        print("Making vertical violin plot")

        plt.close('all')
        data_ordered_by_mol_ID = df.sort_values(["ID tag"], ascending=["True"])

        sns.set(rc={'figure.figsize': (12,8)})
        v = sns.violinplot(x="ID tag",
                           y='Relative microstate free energy prediction',
                           data=data_ordered_by_mol_ID, inner='point',
                           linewidth=0.5, width=width)

        v.set_xticklabels(v.get_xticklabels(),rotation=90)
        plt.tight_layout()
        #plt.savefig(output_directory_path + "/" + "violinplot.pdf")
        plt.savefig(output_directory_path + "/" + fig_name+".pdf")


    def barplot(df, output_directory_path, figsize, fig_name):
        print("Making bar plot")
        plt.close('all')
        current_palette = sns.color_palette()
        sns_color = current_palette[2]

        plt.style.use(["seaborn-talk", "seaborn-whitegrid"])
        plt.rcParams['axes.labelsize'] = 20
        plt.rcParams['xtick.labelsize'] = 14
        plt.rcParams['ytick.labelsize'] = 18
        plt.rcParams['legend.fontsize'] = 16
        plt.rcParams['legend.handlelength']
        plt.rcParams['figure.autolayout'] = True

        plt.figure(figsize=figsize)

        x = range(len(df['average FE prediction']))
        y = df['average FE prediction']

        plt.bar(x, y)
        plt.xticks(x, df['ID tag'], rotation=90)#, horizontalalignment='right')
        #plt.errorbar(x, y, yerr=df['average SEM'], fmt="none", ecolor=sns_color, capsize=3, capthick=True, label='SEM', alpha=0.75)
        plt.errorbar(x, y, yerr=df['prediction STD'], fmt="none", ecolor=sns_color, capsize=3, capthick=True, label='STDEV', alpha=0.75)


        plt.xlabel("Microstates")
        plt.ylabel("Average relative microstate free energy")
        plt.savefig(output_directory_path + "/" + fig_name+".pdf")


    # =======
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
                init_guess = -5
                func_10 = lambda pH: (pop_charge(pH, 2, state_details) - pop_charge(pH, 1, state_details))
                pH_solution_2to1 = fsolve(func_10, init_guess, factor=0.1)
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
                pH_solution_1to0 = fsolve(func_10, init_guess, factor=0.1)
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
                pH_solution_0toneg1 = fsolve(func_0neg1, init_guess, factor=0.1)
                pka.pKa_bytitration = pH_solution_0toneg1

                # delta G method given by newbooks (Junjun Mao)
                dG = getG(msgroup_n1) - getG(msgroup_p0)
                pka.pKa_bydG = (dG / C_unit)

                macropkas.append(pka)

        return macropkas
    # ======================================================================================================================
    #
    # ======================================================================================================================

    output_directory_path = "./plots"
    pKa_submission_collection_file_path = "{}/relative_microstate_FE_submissions.csv".format(output_directory_path)
    os.makedirs(output_directory_path, exist_ok=True)


    # Load submissions data.
    submissions_RFE = load_submissions(pKa_SUBMISSIONS_DIR_PATH, user_map)

    collection_logP = pKaSubmissionCollection(submissions_RFE, output_directory_path, pKa_submission_collection_file_path, no_outliers = False)
    print(collection_logP.data)
    '''collection_data = read_collection_file(collection_file_path = pKa_submission_collection_file_path)




    # Ridge plot using all predictions
    ridge_plot(df = collection_logP.data, by = "ID tag", column = "Relative microstate free energy prediction",
                figsize = (5, 8), colormap=cm.plasma,
                output_directory_path=output_directory_path, fig_name="ridgeplot_all_FE_predictions")


    # Violin plot using all predictions
    violinplot(df = collection_data, output_directory_path=output_directory_path, width=5,fig_name="violinplot_all_FE_predictions" )


    df = collection_logP.data
    df2=df.groupby("ID tag")["Relative microstate free energy prediction"].agg(['count','mean', 'min', 'max','std'])
    df3=df.groupby("ID tag")["Relative microstate free energy SEM"].agg(['mean'])
    df4=pd.merge(df2, df3, left_index=True, right_index=True)
    df4.columns = ['prediction count', 'average FE prediction', 'min prediction', 'max prediction', 'prediction STD', 'average SEM']
    #df4['ID tag'] = df4.index
    df4.reset_index(level=0, inplace=True)
    df4.to_csv(output_directory_path+"/numbers.csv")

    # Barplot of average FE predictions
    barplot(df=df4, output_directory_path=output_directory_path, figsize=(28,10), fig_name="barplot_average_FE_predictions")






    # Repeat without outlier
    output_directory_path = "./plots"
    pKa_submission_collection_file_path = "{}/relative_microstate_FE_submissions_no_outlier.csv".format(output_directory_path)

    os.makedirs(output_directory_path, exist_ok=True)


    # Load submissions data.
    submissions_RFE = load_submissions(pKa_SUBMISSIONS_DIR_PATH, user_map)


    collection_logP_no_outllier = pKaSubmissionCollection(submissions_RFE, output_directory_path, pKa_submission_collection_file_path, no_outliers = True)
    collection_data_no_outlier = read_collection_file(collection_file_path = pKa_submission_collection_file_path)


    # Ridge plot using all predictions
    ridge_plot(df = collection_logP_no_outllier.data, by = "ID tag", column = "Relative microstate free energy prediction",
                figsize = (5, 8),
               colormap=cm.plasma, output_directory_path=output_directory_path, fig_name="ridgeplot_all_FE_predictions_no_outlier")


    # Violin plot using all predictions
    violinplot(df = collection_data_no_outlier, output_directory_path=output_directory_path, width=5, fig_name="violinplot_all_FE_predictions_no_outlier")

    df = collection_logP_no_outllier.data
    df2=df.groupby("ID tag")["Relative microstate free energy prediction"].agg(['count','mean', 'min', 'max','std'])
    df3=df.groupby("ID tag")["Relative microstate free energy SEM"].agg(['mean'])
    df4=pd.merge(df2, df3, left_index=True, right_index=True)
    df4.columns = ['prediction count', 'average FE prediction', 'min prediction', 'max prediction', 'prediction STD', 'average SEM']
    #df4['ID tag'] = df4.index
    df4.reset_index(level=0, inplace=True)
    df4.to_csv(output_directory_path+"/numbers_no_outlier.csv")

    # Barplot of average FE predictions
    barplot(df=df4, output_directory_path=output_directory_path, figsize=(28,10), fig_name="barplot_average_FE_predictions_no_outlier")

'''
