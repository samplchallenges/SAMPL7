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

# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
STAGE_1_SUBMISSIONS_DIR_PATH = '../Submissions-stage1/'
EXPERIMENTAL_DATA_FILE_PATH = '../../experimental-data/stage-1/hits_verification.csv'
USER_MAP_FILE_PATH = '../SAMPL7-user-map-PL-stage1.csv'

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


        # Add host name column to predictions.
        #self.host_name = file_data[0].upper()
        #self.data['host_name'] = self.host_name
        #assert self.host_name in self.HOST_NAMES

        # Store participant name, organization, method category
        self.participant = sections['Participant name'][0].strip()
        self.category = sections['Category'][0].strip()
        print("self.category: ", self.category)
        self.organization = sections['Participant organization'][0].strip()
        self.ranked = sections['Ranked'][0].strip() =='True'


        ## Required system System IDs
        #clip_guests = ['g1', 'g2', 'g3', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10', 'g11', 'g12', 'g15', 'g16', 'g17', 'g18', 'g19']
        #CD_guests = ['g1','g2']
        #GDCC_guests = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8']
        #CD_hosts = copy.copy(self.HOST_NAMES['CD'])
        #CD_hosts.remove('bCD')
        #self.REQUIRED_SYSTEM_IDs = {'CLIP':[f'clip-{guest}' for guest in clip_guests],
                                #'CD':[f'{host}-{guest}' for guest in CD_guests for host in CD_hosts],
                                 #'GDCC':[f'exoOA-{guest}' for guest in GDCC_guests] + ['OA-g7', 'OA-g8']}

        # Check if this is a test submission.
        if self.sid in self.TEST_SUBMISSION_SIDS:
            raise IgnoredSubmissionError('This submission has been used for tests.')

        # Check if this is a reference submission
        self.reference_submission = False
        if self.sid in self.REF_SUBMISSION_SIDS:
            self.reference_submission = True



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
    print("Loading submissions")
    submissions = load_submissions(Stage1Submission, STAGE_1_SUBMISSIONS_DIR_PATH, user_map)
    print("Submissions:\n", submissions)

# Try print after defining submission class
    # for submission in submissions:
    #     print("submission.name:\n", submission.name)
    #     print("submission.data:\n", submission.data)


# Create submission collection
    #collection = Stage1SubmissionCollection(submissions, experimental_data, output_directory_path='../analysis_outputs')