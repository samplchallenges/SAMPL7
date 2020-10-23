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
from matplotlib import cm
import joypy



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
                                    "pKa mean",
                                    "pKa SEM",
                                    "pKa model uncertainty")}


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
            #print(submission.method_name)
            if "RFE-NHLBI-TZVP-QM" in submission.method_name  and no_outliers:
                continue
            #print(submission.method_name)
            for mol_ID, series in submission.data.iterrows():
                ref_state = submission.data.loc[mol_ID, "Molecule ID"]
                pKa_mean_pred = submission.data.loc[mol_ID, "pKa mean"]
                pKa_SEM_pred = submission.data.loc[mol_ID, "pKa SEM"]
                total_charge = submission.data.loc[mol_ID, "total charge"]
                pKa_model_uncertainty =  submission.data.loc[mol_ID, "pKa model uncertainty"]

                data.append({
                    'method_name': submission.method_name,
                    'file name': submission.file_name,
                    'Reference state': ref_state,
                    'ID tag': mol_ID,
                    'total charge': total_charge,
                    'Relative microstate FE predictions': pKa_mean_pred,
                    'Relative microstate FE SEM': pKa_SEM_pred,
                    'pKa model uncertainty': pKa_model_uncertainty
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
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['xtick.labelsize'] = 14
        #plt.rcParams['figure.autolayout'] = True
        plt.tight_layout()

        # Make ridge plot
        fig, axes = joypy.joyplot(data=df, by=by, column=column, figsize=figsize, colormap=colormap, linewidth=1)
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
        fig, axes = joypy.joyplot(data=df, by=by, column=column, figsize=figsize, colormap=colormap, linewidth=1, overlap=0)
        # Add x-axis label
        axes[-1].set_xlabel(column)
        plt.savefig(output_directory_path + "/" + "ridgeplot.pdf")


    def violinplot(df, output_directory_path, width, fig_name):
        '''print("Making horizontal violin plot")

        plt.close('all')
        data_ordered_by_mol_ID = df.sort_values(["ID tag"], ascending=["True"])

        sns.set(rc={'figure.figsize': (8.27,11.7)})
        sns.violinplot(y="ID tag", x='Relative microstate FE predictions',
                       data=data_ordered_by_mol_ID, inner='point',
                       linewidth=0.5, width=width)
        plt.tight_layout()
        #plt.savefig(output_directory_path + "/" + "violinplot.pdf")
        plt.savefig(output_directory_path + "/" + fig_name+"_horizontal.pdf")'''



        print("Making vertical violin plot")

        plt.close('all')
        data_ordered_by_mol_ID = df.sort_values(["ID tag"], ascending=["True"])

        sns.set(rc={'figure.figsize': (12,8)})
        v = sns.violinplot(x="ID tag", y='Relative microstate FE predictions',
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
        plt.errorbar(x, y, yerr=df['average SEM'], fmt="none", ecolor=sns_color, capsize=3,
                     capthick=True, label='SEM', alpha=0.75)

        plt.xlabel("Microstates")
        plt.ylabel("Average relative microstate free energy")
        plt.savefig(output_directory_path + "/" + fig_name+".pdf")



    # ======================================================================================================================
    #
    # ======================================================================================================================

    output_directory_path = "./plots"
    pKa_submission_collection_file_path = "{}/relative_microstate_FE_submissions.csv".format(output_directory_path)
    os.makedirs(output_directory_path, exist_ok=True)


    # Load submissions data.
    submissions_RFE = load_submissions(pKa_SUBMISSIONS_DIR_PATH, user_map)


    collection_logP = pKaSubmissionCollection(submissions_RFE, output_directory_path, pKa_submission_collection_file_path, no_outliers = False)
    collection_data = read_collection_file(collection_file_path = pKa_submission_collection_file_path)


    # Ridge plot using all predictions
    ridge_plot(df = collection_logP.data, by = "ID tag", column = "Relative microstate FE predictions", figsize = (4, 7), colormap=cm.plasma,
               output_directory_path=output_directory_path, fig_name="ridgeplot_all_FE_predictions")


    # Violin plot using all predictions
    violinplot(df = collection_data, output_directory_path=output_directory_path, width=5,fig_name="violinplot_all_FE_predictions" )


    df = collection_logP.data
    df2=df.groupby("ID tag")["Relative microstate FE predictions"].agg(['count','mean', 'min', 'max','std'])
    df3=df.groupby("ID tag")["Relative microstate FE SEM"].agg(['mean'])
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
    ridge_plot(df = collection_logP_no_outllier.data, by = "ID tag", column = "Relative microstate FE predictions", figsize = (4, 8),
               colormap=cm.plasma, output_directory_path=output_directory_path, fig_name="ridgeplot_all_FE_predictions_no_outlier")


    # Violin plot using all predictions
    violinplot(df = collection_data_no_outlier, output_directory_path=output_directory_path, width=5, fig_name="violinplot_all_FE_predictions_no_outlier")

    df = collection_logP_no_outllier.data
    df2=df.groupby("ID tag")["Relative microstate FE predictions"].agg(['count','mean', 'min', 'max','std'])
    df3=df.groupby("ID tag")["Relative microstate FE SEM"].agg(['mean'])
    df4=pd.merge(df2, df3, left_index=True, right_index=True)
    df4.columns = ['prediction count', 'average FE prediction', 'min prediction', 'max prediction', 'prediction STD', 'average SEM']
    #df4['ID tag'] = df4.index
    df4.reset_index(level=0, inplace=True)
    df4.to_csv(output_directory_path+"/numbers_no_outlier.csv")

    # Barplot of average FE predictions
    barplot(df=df4, output_directory_path=output_directory_path, figsize=(28,10), fig_name="barplot_average_FE_predictions_no_outlier")
