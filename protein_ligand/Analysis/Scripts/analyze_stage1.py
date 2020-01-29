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
# import seaborn as sns
# from matplotlib import pyplot as plt

from pkganalysis.submission import (SamplSubmission, IgnoredSubmissionError,
                                    load_submissions, plot_correlation)

from pkganalysis.stats import (calc_confusion_matrix, accuracy, f1_score, \
                                sensitivity, specificity, precision)

# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
STAGE_1_SUBMISSIONS_DIR_PATH = '../Submissions-stage1/'
EXPERIMENTAL_DATA_FILE_PATH = '../../experimental-data/stage-1/hits_verification.csv'
USER_MAP_FILE_PATH = '../Analysis-outputs-stage1/SAMPL7-user-map-PL-stage1.csv'

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
    OUTPUT_DIRECTORY_PATH = '../Analysis-outputs-stage1'
    stage1_submission_collection_file_path = '{}/stage1_submission_collection.csv'.format(OUTPUT_DIRECTORY_PATH)
    collection = Stage1SubmissionCollection(submissions, experimental_data, OUTPUT_DIRECTORY_PATH,
                                            stage1_submission_collection_file_path, ignore_refcalcs = False)
