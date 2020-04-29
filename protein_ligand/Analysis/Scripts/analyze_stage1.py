#!/usr/bin/env python

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================

import os
import glob
import copy
import collections
import pickle

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from pkganalysis.submission import (SamplSubmission, IgnoredSubmissionError,
                                    load_submissions, plot_correlation)

from pkganalysis.stats import (compute_bootstrap_statistics, calc_confusion_matrix,
                               accuracy, f1_score, sensitivity, specificity, precision, balanced_accuracy,
                               TP, TN, FP, FN)

# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
STAGE_1_SUBMISSIONS_DIR_PATH = '../Submissions-stage1/'
EXPERIMENTAL_DATA_FILE_PATH = '../../experimental-data/stage-1/hits_verification.csv'
USER_MAP_FILE_PATH = '../Analysis-outputs-stage1/SAMPL7-user-map-PL-stage1.csv'
FRAGMENTS_FILE_PATH = '../../fragments_screened.csv'

# =============================================================================
# MAIN CHALLENGE SUBMISSION 1
# =============================================================================
# Add from line 100 https://github.com/samplchallenges/SAMPL7/blob/master/host_guest/Analysis/Scripts/analyze_hostguest.py
# make sure
# to use later when parsing submissions
# names = ('Predictions', 'Participant name', 'Participant organization', 'Name', 'Software', 'Category', 'Ranked', 'Method')

class Stage1Submission(SamplSubmission):
    """A submission for the main host-guest challenge.
    Parameters
    ----------
    file_path : str
        The path to the submission file.
    Raises
    ------
    IgnoredSubmission
        If the submission ID is among the ignored submissions.
    """

    # The IDs of the submissions used for testing the validation. Should be strings of submission IDs
    TEST_SUBMISSION_SIDS = {}

    # The IDs of submissions for reference calculations. Should be strings of submission IDs
    REF_SUBMISSION_SIDS = []

    # Section of the submission file.
    SECTIONS = {'Predictions', 'Participant name', 'Participant organization', 'Name', 'Software', 'Method', 'Category', 'Ranked'}


    # Sections in CSV format with kwargs to pass to pandas.read_csv().

    CSV_SECTIONS = {'Predictions': { 'names': ('Fragment ID', 'Site 1', 'Site 2', 'Site 3', 'Site 4', 'All Sites'),
                                     'index_col': 'Fragment ID'}}


    RENAME_METHODS = {}

    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.file_name = file_name

        #TO DO:  Not sure if I'm going to use the immediately following for anything
        #file_name_simple = file_name.replace('_','-')
        #file_data = file_name_simple.split('-')
        #self.host_name = file_data[0]

        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        self.data = sections['Predictions']  # This is a list
        self.data = pd.DataFrame(data=self.data) # Now a DataFrame
        try:
            self.name = self.RENAME_METHODS[sections['Name'][0]]
        except KeyError:
            self.name = sections['Name'][0]


        # Store participant name, organization, method category
        self.participant = sections['Participant name'][0].strip()
        self.category = sections['Category'][0].strip()
        print("self.category: ", self.category)
        self.organization = sections['Participant organization'][0].strip()
        self.ranked = sections['Ranked'][0].strip() =='True'


        # Check if this is a test submission.
        if self.sid in self.TEST_SUBMISSION_SIDS:
            raise IgnoredSubmissionError('This submission has been used for tests.')

        # Check if this is a reference submission
        self.reference_submission = False
        if self.sid in self.REF_SUBMISSION_SIDS:
            self.reference_submission = True

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

class Stage1SubmissionCollection:
    """A collection of Stage 1 submissions."""

    # Path to directories for organizing plots
    #STAGE1_ACCURACY_PLOT_PATH_DIR = 'Accuracy'


    def __init__(self, submissions, experimental_data, output_directory_path, stage1_submission_collection_file_path, ignore_refcalcs = False):


        # Check if submission collection file already exists.
        if os.path.isfile(stage1_submission_collection_file_path):
            print("Analysis will be done using the existing submission collection file: {}".format(stage1_submission_collection_file_path))

            self.data = pd.read_csv(stage1_submission_collection_file_path)
            print("\n SubmissionCollection: \n")
            print(self.data)

            # Populate submission.data dataframes parsing sections of collection file.
            for submission in submissions:

                # To ignore reference calculations, when necessary
                if submission.reference_submission and ignore_refcalcs:
                    continue

                df_collection_of_each_submission = self.data.loc[self.data["SID"] == int(submission.sid) ]

                #print("df_collection_of_each_submission:\n",df_collection_of_each_submission)

                # Transform into Pandas DataFrame.
                submission.data = pd.DataFrame()
                submission.data["Site 1"] = df_collection_of_each_submission["Site 1 (pred)"]
                submission.data["Site 2"] = df_collection_of_each_submission["Site 2 (pred)"]
                submission.data["Site 3"] = df_collection_of_each_submission["Site 3 (pred)"]
                submission.data["Site 4"] = df_collection_of_each_submission["Site 4 (pred)"]
                submission.data["All Sites"] = df_collection_of_each_submission["All Sites (pred)"]
                submission.data["Fragment ID"] = df_collection_of_each_submission["Fragment ID"]

                submission.data.set_index("Fragment ID", inplace=True)

            # Transform into Pandas DataFrame.
            self.output_directory_path = output_directory_path


        else: # Build collection dataframe from the beginning.
            # Build full stage 1 collection table.
            data = []

            # Submissions for stage 1.
            for submission in submissions:
                if submission.reference_submission and ignore_refcalcs:
                    continue

                #print("submission.sid:\n", submission.sid)
                #print("submission.name:\n", submission.name)
                #print("submission.data:\n", submission.data)


                for fragment_ID, series in submission.data.iterrows():
                    #print("fragment_ID:", fragment_ID)
                    #print("series:\n", series)
                    #site1_pred = series["Site 1"]
                    #print("site1_pred: ", site1_pred)

                    # Predicted data
                    site1_pred = series["Site 1"]
                    site2_pred = series["Site 2"]
                    site3_pred = series["Site 3"]
                    site4_pred = series["Site 4"]
                    all_sites_pred = series["All Sites"]

                    # Experimental data
                    site1_exp = experimental_data.loc[fragment_ID, 'Site 1']
                    site2_exp = experimental_data.loc[fragment_ID, 'Site 2']
                    site3_exp = experimental_data.loc[fragment_ID, 'Site 3']
                    site4_exp = experimental_data.loc[fragment_ID, 'Site 4']
                    all_sites_exp = experimental_data.loc[fragment_ID, 'All Sites']


                    data.append({
                        'SID': submission.sid,  # Previously receipt_ID
                        'Participant': submission.participant,
                        'Organization': submission.organization,
                        'Name': submission.name,
                        'Category': submission.category,
                        'Ranked': submission.ranked,
                        'Fragment ID': fragment_ID,
                        'Site 1 (pred)': site1_pred,
                        'Site 1 (exp)': site1_exp,
                        'Site 2 (pred)': site2_pred,
                        'Site 2 (exp)': site2_exp,
                        'Site 3 (pred)': site3_pred,
                        'Site 3 (exp)': site3_exp,
                        'Site 4 (pred)': site4_pred,
                        'Site 4 (exp)': site4_exp,
                        'All Sites (pred)': all_sites_pred,
                        'All Sites (exp)': all_sites_exp
                    })

            # Transform into Pandas DataFrame.
            self.data = pd.DataFrame(data=data)
            self.output_directory_path = output_directory_path

            print("\n SubmissionCollection: \n")
            print(self.data)

            # Create general output directory.
            os.makedirs(self.output_directory_path, exist_ok=True)

            # Save collection.data dataframe in a CSV file.
            self.data.to_csv(stage1_submission_collection_file_path, index=False)

            print("Stage1 submission collection file generated:\n", stage1_submission_collection_file_path)


    def complete_predictions_with_missing_fragments(self, fragments_file_path, submission_collection_file_path,ranking):
        """ Adds missing non-binder predictions to collection. Assumes
        Parameters
        ----------
        fragments_file_path: Path to CSV file with fragment IDs in the first column
        filter_nonranked: filters out non ranked results
        """

        # Read fragments file to extract full list of screened fragment list IDs
        fragments_data = pd.read_csv(fragments_file_path, names=["Fragment ID", "SMILES"])
        fragment_IDs = fragments_data["Fragment ID"].values

        # Rebuild full stage 1 collection table, adding missing fragments (predicted as non-binder).
        data = []

        # Submissions for stage 1.
        for submission in submissions:
            if submission.reference_submission and ignore_refcalcs:
                continue

            # print("submission.sid:\n", submission.sid)
            # print("submission.name:\n", submission.name)
            # print("submission.data:\n", submission.data)

            for screened_fragment_ID in fragment_IDs:
                #screened_fragment_ID = "F560"
                #print("screened_fragment_ID:", screened_fragment_ID)

                # Check if screened fragment is in submission
                submitted_fragment_IDs = set(submission.data.index.values)
               # print("submitted_fragment_IDs:\n", submitted_fragment_IDs)

                # If screened fragment ID is already in the submission set, take prediction records from the submission
                if screened_fragment_ID in submitted_fragment_IDs:
                    #print("Already submitted.")

                    series = submission.data.loc[screened_fragment_ID,:]
                    #print("series:\n", series)
                    #site1_pred = series["Site 1"]
                    #print("site1_pred: ", site1_pred)

                    # Predicted data
                    site1_pred = series["Site 1"]
                    site2_pred = series["Site 2"]
                    site3_pred = series["Site 3"]
                    site4_pred = series["Site 4"]
                    all_sites_pred = series["All Sites"]

                # If screened fragment ID was not in the submitted prediction set, add a non-binder prediction to data
                else:
                    #print("Not submitted.")

                    # Predicted data
                    site1_pred = "False"
                    site2_pred = "False"
                    site3_pred = "False"
                    site4_pred = "False"
                    all_sites_pred = "False"

                # Experimental data
                site1_exp = experimental_data.loc[screened_fragment_ID, 'Site 1']
                site2_exp = experimental_data.loc[screened_fragment_ID, 'Site 2']
                site3_exp = experimental_data.loc[screened_fragment_ID, 'Site 3']
                site4_exp = experimental_data.loc[screened_fragment_ID, 'Site 4']
                all_sites_exp = experimental_data.loc[screened_fragment_ID, 'All Sites']

                data.append({
                   'SID': submission.sid,  # Previously receipt_ID
                    'Participant': submission.participant,
                    'Organization': submission.organization,
                    'Name': submission.name,
                    'Category': submission.category,
                    'Ranked': submission.ranked,
                    'Fragment ID': screened_fragment_ID,
                    'Site 1 (pred)': site1_pred,
                    'Site 1 (exp)': site1_exp,
                    'Site 2 (pred)': site2_pred,
                    'Site 2 (exp)': site2_exp,
                    'Site 3 (pred)': site3_pred,
                    'Site 3 (exp)': site3_exp,
                    'Site 4 (pred)': site4_pred,
                    'Site 4 (exp)': site4_exp,
                    'All Sites (pred)': all_sites_pred,
                    'All Sites (exp)': all_sites_exp
                    })

            #print("data:\n", data)

            # Transform into Pandas DataFrame.
            self.data = pd.DataFrame(data=data)

            #filters or not filter ranked and non-ranked submissions given the following list
            #    rankings = ["Ranked_and_non-ranked", "Ranked", "Non-ranked"]

            if ranking == ('Ranked_and_non-ranked' or None):
                self.data = self.data
            if ranking == 'Ranked':
                self.data = self.data[self.data.Ranked == True]
            if ranking == 'Non-ranked':
                self.data = self.data[self.data.Ranked == False]

            print("\n SubmissionCollection: \n")
            print(self.data)

            # Create general output directory.
            os.makedirs(self.output_directory_path, exist_ok=True)

            # Save completed collection.data dataframe in a CSV file.
            self.data.to_csv(submission_collection_file_path, index=False)
            print("Stage1 submission collection file updated with missing predictions:\n", submission_collection_file_path)



    # TO DO: The following function does not pertain to this challenge/needs updating if we even retain
    @staticmethod
    def _assign_paper_method_name(name):
        return name

    def generate_statistics_tables(self, stats_funcs, subdirectory_path, groupby, site,
                                   extra_fields=None, sort_stat=None,
                                   ordering_functions=None, latex_header_conversions=None,
                                   caption=''):
        """Generate statistics tables in CSV, JSON, and LaTex format.
        Parameters
        ----------
        groupby : str
            The name of the data column to be used to compute the statistics.
            For example, 'name' to obtain statistics about individual methods,
            'system_id' to compute statistics by molecules.
        ordering_functions : dict
            Dictionary statistic_name -> ordering_function(stats), where
            ordering_function determines how to rank the the groups by
            statistics.
        """

        if extra_fields is None:
            extra_fields = []

        def escape(s):
        #    return s.replace('_', '\_')
            return s

        extra_fields_latex = [escape(extra_field) for extra_field in extra_fields]

        file_base_name = 'statistics'
        directory_path = os.path.join(self.output_directory_path, subdirectory_path)

        stats_names, stats_funcs = zip(*stats_funcs.items())
        ci_suffixes = ('', '_lower_bound', '_upper_bound')

        # Compute or read the bootstrap statistics from the cache.
        cache_file_path = os.path.join(self.output_directory_path, 'bootstrap_distributions.p')
        all_bootstrap_statistics = self._get_bootstrap_statistics(groupby, site, stats_names, stats_funcs,
                                                                  cache_file_path=cache_file_path)

        # Collect the records for the DataFrames.
        statistics_csv = []
        statistics_latex = []

        groups = self.data[groupby].unique()
        for i, group in enumerate(groups):
            print('\rGenerating bootstrap statistics tables for {} {} ({}/{})'
                  ''.format(groupby, group, i+1, len(groups)), end='')

            # Isolate bootstrap statistics.
            bootstrap_statistics = all_bootstrap_statistics[group]

            # Select the group.
            data = self.data[self.data[groupby] == group]

            # Isolate the extra field.
            group_fields = {}
            latex_group_fields = {}
            for extra_field, extra_field_latex in zip(extra_fields, extra_fields_latex):
                assert len(data[extra_field].unique()) == 1
                extra_field_value = data[extra_field].values[0]
                group_fields[extra_field] = extra_field_value
                latex_group_fields[extra_field_latex] = escape(extra_field_value)

            record_csv = {}
            record_latex = {}
            for stats_name, (stats, (lower_bound, upper_bound), bootstrap_samples) in bootstrap_statistics.items():
                # For CSV and JSON we put confidence interval in separate columns.
                for suffix, info in zip(ci_suffixes, [stats, lower_bound, upper_bound]):
                    record_csv[stats_name + suffix] = info

                # For the PDF, print bootstrap CI in the same column.
                stats_name_latex = latex_header_conversions.get(stats_name, stats_name)
                record_latex[stats_name_latex] = '{:.2f} [{:.2f}, {:.2f}]'.format(stats, lower_bound, upper_bound)

            statistics_csv.append({'ID': group, **group_fields, **record_csv})
            statistics_latex.append({'ID': escape(group), **latex_group_fields,
                                     **record_latex})
        print()

        # Convert dictionary to Dataframe to create tables/plots easily.
        statistics_csv = pd.DataFrame(statistics_csv)
        statistics_csv.set_index('ID', inplace=True)
        statistics_latex = pd.DataFrame(statistics_latex)

        #Add ROC space figure?
        #print(statistics_csv)
        #ROC_df = statistics_csv[['Specificity','Sensitivity']]
        #print(ROC_df)
        #statistics_csv.plot(kind='scatter', x='Specificity', y='Sensitivity')
        #plt.xlabel('False positive rate (specificity)')
        #plt.ylabel('True positive rate (sensitivity)')
        #plt.plot([0, 1], [0, 1], color='orange', linestyle='--')
        #plt.title('{} predictions for {} in ROC space'.format(ranking,site), loc='center')

        #Add bar plot of balanced accuracy
        print('PLOT HERE')
        #print(statistics_csv.index)

        balanced_accuracies = statistics_csv[['Balanced Accuracy']]
        balanced_accuracies = np.array(balanced_accuracies).flatten()
        IDs = statistics_csv.index
        plt.figure(figsize=(20, 10))
        plt.bar(IDs, balanced_accuracies)
        plt.axhline(y=0.5, color='orange', linestyle='--', label='Random')
        plt.legend()
        plt.ylabel("Balanced accuracy")
        plt.ylim(0, 1)
        plt.xlabel("SID")
        plt.title('{} predictions for {}'.format(ranking, site), loc='center')
        plt.savefig('{}/{} predictions for {}'.format(OUTPUT_DIRECTORY_PATH_SPECIFIC,ranking, site))
        plt.close()



        # Sort by the given statistics.
        if sort_stat is not None:
            ordering_function = ordering_functions.get(sort_stat, lambda x: x)
            order = sorted(statistics_csv[sort_stat].items(), key=lambda x: ordering_function(x[1]))
            order = [k for k, value in order]
            statistics_csv = statistics_csv.reindex(order)
            latex_order = [escape(k) for k in order]
            statistics_latex.ID = statistics_latex.ID.astype('category')
            statistics_latex.ID.cat.set_categories(latex_order, inplace=True)
            statistics_latex.sort_values(by='ID', inplace=True)

        # Reorder columns that were scrambled by going through a dictionaries.
        stats_names_csv = [name + suffix for name in stats_names for suffix in ci_suffixes]
        stats_names_latex = [latex_header_conversions.get(name, name) for name in stats_names]
        statistics_csv = statistics_csv[extra_fields + stats_names_csv]
        statistics_latex = statistics_latex[['ID'] + extra_fields_latex + stats_names_latex]

        # Create CSV and JSON tables (correct LaTex syntax in column names).
        os.makedirs(directory_path, exist_ok=True)
        file_base_path = os.path.join(directory_path, file_base_name)
        with open(file_base_path + '.csv', 'w') as f:
            statistics_csv.to_csv(f)
        with open(file_base_path + '.json', 'w') as f:
            statistics_csv.to_json(f, orient='index')

        # Create LaTex table.
        latex_directory_path = os.path.join(directory_path, file_base_name + 'LaTex')
        os.makedirs(latex_directory_path, exist_ok=True)
        with open(os.path.join(latex_directory_path, file_base_name + '.tex'), 'w') as f:
            f.write('\\documentclass[8pt]{article}\n'
                    '\\usepackage[a4paper,margin=0.2in,tmargin=0.5in,bmargin=0.5in,landscape]{geometry}\n'
                    '\\usepackage{booktabs}\n'
                    '\\usepackage{longtable}\n'
                    '\\pagenumbering{gobble}\n'
                    '\\begin{document}\n'
                    '\\begin{center}\n'
                    '\\begin{footnotesize}\n')
            statistics_latex.to_latex(f, column_format='|' + 'c'*(2 + len(stats_funcs)) + '|',
                                      escape=False, index=False, longtable=True, bold_rows=True)
            f.write('\end{footnotesize}\n'
                    '\end{center}\n')
            f.write(caption + '\n')
            f.write('\end{document}\n')



    def _get_bootstrap_statistics(self, groupby, site, stats_names, stats_funcs, cache_file_path):
        """Generate the bootstrap distributions of all groups and cache them.
        If cached values are found on disk, the distributions are not recomputed.
        Returns
        -------
        all_bootstrap_statistics : collections.OrderedDict
            group -> {stats_name -> (statistics, confidence_interval, bootstrap_samples)}
            confidence_interval is a pair (lower_bound, upper_bound), and bootstrap_samples
            are the (ordered) bootstrap statistics used to compute the confidence interval.
        """


        # Identify all the groups (e.g. methods/molecules).
        groups = self.data[groupby].unique()

        # Initialize returned value. The OrderedDict maintains the order of statistics.
        all_bootstrap_statistics = collections.OrderedDict([(name, None) for name in stats_names])
        all_bootstrap_statistics = collections.OrderedDict(
            [(group, copy.deepcopy(all_bootstrap_statistics)) for group in groups]
        )

        # Load the statistics that we have already computed.
        try:
            with open(cache_file_path, 'rb') as f:
                print('Loading cached bootstrap distributions from {}'.format(cache_file_path))
                cached_bootstrap_statistics = pickle.load(f)
        except FileNotFoundError:
            cached_bootstrap_statistics = None

        # Create a map from paper method name to submission method name.
        try:
            paper_to_submission_name = {self._assign_paper_method_name(submission_name): submission_name
                                        for submission_name in cached_bootstrap_statistics}
        except (UnboundLocalError, TypeError):
            # cached_bootstrap_statistics is None or group is not a method.
            paper_to_submission_name = {}

        cache_updated = False
        for i, (group, group_bootstrap_statistics) in enumerate(all_bootstrap_statistics.items()):
            # Check which statistics we still need to compute for this group.
            if cached_bootstrap_statistics is not None:
                group_stats_names = []
                group_stats_funcs = []
                for stats_name, stats_func in zip(stats_names, stats_funcs):
                    try:
                        all_bootstrap_statistics[group][stats_name] = cached_bootstrap_statistics[group][stats_name]
                    except KeyError:
                        try:
                            # method_name = self._assign_paper_method_name(group)
                            method_name = paper_to_submission_name[group]
                            all_bootstrap_statistics[group][stats_name] = cached_bootstrap_statistics[method_name][
                                stats_name]
                        except KeyError:
                            group_stats_names.append(stats_name)
                            group_stats_funcs.append(stats_func)
            else:
                # Compute everything.
                group_stats_names = stats_names
                group_stats_funcs = stats_funcs

            if len(group_stats_names) == 0:
                continue
            cache_updated = True  # Update the cache on disk later.

            print('\rGenerating bootstrap statistics for {} {} ({}/{})'
                  ''.format(groupby, group, i + 1, len(groups)), end='')

            # Select the group data.
            data = self.data[self.data[groupby] == group]
            print("data:\n", data)

            # Compute bootstrap statistics.
            # Modify here to do per-site statistic
            #loop iterates over: sites = ["site-1", "site-2", "site-3", "site-4", "all-sites"]

            if site == "site-1":
                data = data[['Site 1 (exp)', 'Site 1 (pred)']]

            if site == "site-2":
                data = data[['Site 2 (exp)', 'Site 2 (pred)']]

            if site == "site-3":
                data = data[['Site 3 (exp)', 'Site 3 (pred)']]

            if site == "site-4":
                data = data[['Site 4 (exp)', 'Site 4 (pred)']]

            if site == "all-sites":
                data = data[['All Sites (exp)', 'All Sites (pred)']]

            print(site)
            print(data)

            new_bootstrap_statistics = compute_bootstrap_statistics(data.as_matrix(), group_stats_funcs, sems=None,
                                                                    n_bootstrap_samples=10000) #10000

            # Update the returned value with the statistics just computed.
            new_boostrap_statistics = {group_stats_names[i]: new_bootstrap_statistics[i]
                                       for i in range(len(group_stats_funcs))}
            group_bootstrap_statistics.update(new_boostrap_statistics)

        # Cache the computed statistics on disk. Create output directory if necessary.
        if cache_updated:
            os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
            with open(cache_file_path, 'wb') as f:
                pickle.dump(all_bootstrap_statistics, f)

        return all_bootstrap_statistics


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    # Read experimental data.
    with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
        #names = ('Fragment ID', 'Site 1', 'Site 2', 'Site 3', 'Site 4', 'All Sites')
        experimental_data = pd.read_csv(f, sep=',', index_col='Fragment ID', header=0)
        print("Experimental data of stage 1:\n",experimental_data)


    #Import user map.
    try:
        with open(USER_MAP_FILE_PATH, 'r') as f:
            user_map = pd.read_csv(f)
            print("user_map:\n", user_map)
    except FileNotFoundError:
        user_map=None
        print("Warning: No user map found.")


    # Configuration: statistics to compute.
    stats_funcs = collections.OrderedDict([
        ('Sensitivity', sensitivity),
        ('Specificity', specificity),
        ('Precision', precision),
        ('Balanced Accuracy', balanced_accuracy),
        ('Accuracy', accuracy),
        #('F1 Score', f1_score),
        ('True Positive', TP),
        ('False Negative', FN),
        ('True Negative', TN),
        ('False Positive', FP),
    ])
    ordering_functions = {
        'Sensitivity': lambda x: -x,
        'Specificity': lambda x: -x,
        'Precision': lambda x: -x,
        'Balanced Accuracy': lambda x: -x,
        'Accuracy': lambda x: -x,
        #'F1 Score': lambda x: -x,
        'True Positive': lambda x: -x,
        'False Negative': lambda x: x,
        'True Negative': lambda x: -x,
        'False Positive': lambda x: x,
    }
    latex_header_conversions = {
        'Sensitivity': 'Sensitivity (TPR)',
        'Specificity': 'Specificity (TNR)',
        'Precision': 'Precision (PPV)',
        'Balanced Accuracy': 'Balanced Accuracy',
        'Accuracy': 'Accuracy',
        #'F1 Score': 'F1 Score',
        'True Positive': 'True Positive',
        'False Negative': 'False Negative',
        'True Negative': 'True Negative',
        'False Positive': 'False Positive',
    }


    # Load submissions data.
    print("Loading submissions...")
    submissions = load_submissions(Stage1Submission, STAGE_1_SUBMISSIONS_DIR_PATH, user_map)
    #print("Submissions:\n", submissions)
    # Try print after defining submission class
    # for submission in submissions:
    #     print("submission.name:\n", submission.name)
    #     print("submission.data:\n", submission.data)

    # Create submission collection
    print("Generating collection file...")


    #Create list of all rankings and sites to iterate over
    rankings = ["Ranked_and_non-ranked", "Ranked", "Non-ranked"]
    sites = ["site-1", "site-2", "site-3", "site-4", "all-sites"]

    #iterates over lists to create statistics for each combination idenpedently
    for ranking in rankings:
        for site in sites:
            OUTPUT_DIRECTORY_PATH_SPECIFIC = '../Analysis-outputs-stage1/{}/{}'.format(ranking,site)
            stage1_submission_collection_specific_file_path = '{}/stage1_submission_collection_{}_{}.csv'.format(OUTPUT_DIRECTORY_PATH_SPECIFIC,ranking,site)

            collection_specific = Stage1SubmissionCollection(submissions,
                                                             experimental_data,
                                                             OUTPUT_DIRECTORY_PATH_SPECIFIC,
                                                            stage1_submission_collection_specific_file_path,
                                                            ignore_refcalcs=False)

            collection_specific.complete_predictions_with_missing_fragments(fragments_file_path=FRAGMENTS_FILE_PATH,
                                                                           submission_collection_file_path=stage1_submission_collection_specific_file_path,
                                                                            ranking=ranking)
            sns.set_context('talk')
            collection_specific.generate_statistics_tables(stats_funcs, subdirectory_path='StatisticsTables',
                                         groupby='SID', site = site, extra_fields=None,
                                         sort_stat='Sensitivity', ordering_functions=ordering_functions,
                                          latex_header_conversions=latex_header_conversions,
                                         caption='')

    # TO-DO : verify the calculations (do one set by hand)
    # TO-DO : Create plots for evaluation statistics
    #position of each group on ROC space
        #color by method?
