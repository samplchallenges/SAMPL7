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
PHIPA_STAGE_1_SUBMISSIONS_DIR_PATH = '../../Submissions-stage1/PHIP2/'
EXPERIMENTAL_DATA_FILE_PATH = '../experiment_data/stage_1/hits_verification.csv'
USER_MAP = '../SAMPL7-user-map-PL.csv'

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

    CSV_SECTIONS = {
        'Predictions': {'Fragment ID', 'Site 1', 'Site 2', 'Site 3', 'Site 4', 'All Sites'}
    }

    RENAME_METHODS = {}

    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.file_name = file_name

        #TO DO:  Not sure if I'm going to use the immediately following for anything
        file_name_simple = file_name.replace('_','-')
        file_data = file_name_simple.split('-')
        self.host_name = file_data[0]

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

    def __add__(self, other):
        """Merge the data of the two submission."""
        merged_submission = copy.deepcopy(self)
        merged_submission.sid = '{} + {}'.format(*sorted([self.sid, other.sid]))
        merged_submission.host_name = '{} + {}'.format(*sorted([self.host_name, other.host_name]))

        # Check if this is already a merged submission.
        if isinstance(merged_submission.file_name, list):
            merged_submission.file_name = sorted([*merged_submission.file_name, other.file_name])
        else:
            merged_submission.file_name = sorted([merged_submission.file_name, other.file_name])
        merged_submission.data = pd.concat([merged_submission.data, other.data])
        return merged_submission

    def split(self, names_to_separate):
        """Take a host-guest submission that spans multiple hosts (with system IDs including host name and guest name), and split it into multiple submissions
        which have the same metadata but only contain the data for the individual hosts. The resulting submissions have updated `host_name` fields also.
        Takes a list of host names (as used for the individual data points) to separate based on.
        Returns a list of the new HostGuestSubmission objects, of length equal to `names_to_separate`"""

        # Find how many submissions we're making and make new submissions, duplicating old
        n_submissions = len(names_to_separate)
        new_submissions = [copy.deepcopy(self) for i in range(n_submissions)]

        # Build list of system IDs we want
        #for (idx, submission) in enumerate(new_submissions):
        #    desired_IDs = []
        #    for system_id, series in submission.data[['$\Delta$G', 'd$\Delta$G', '$\Delta$H']].iterrows():
        #        tmp = system_id.split('-')
        #        if tmp[0] == names_to_separate[idx]:
        #            desired_IDs.append( system_id )

            ## Grab just that data and store
            #new_submissions[idx].data = submission.data.loc[desired_IDs]
            ## Change the host name to what's correct for this host
            #new_submissions[idx].data.host_name = names_to_separate[idx]
            #new_submissions[idx].host_name = names_to_separate[idx]

        return new_submissions

Stage1Submission('./Submissions-stage1/PHIP2.txt', USER_MAP)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    # Read experimental data.
    with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
        # experimental_data = pd.read_json(f, orient='index')
        names = ('Fragment ID', 'Site 1', 'Site 2', 'Site 3', 'Site 4', 'All Sites')
        experimental_data = pd.read_csv(f, sep=',', index_col='Fragment ID', header=0)

        #print(experimental_data)


    #Import user map.
    try:
        with open('../SAMPL7-user-map-PL.csv', 'r') as f:
            user_map = pd.read_csv(f, header=None)
    except FileNotFoundError:
        user_map=None
        print("Warning: No user map found.")

#print(user_map)

# Load submission: add from line 1073
    #need to define stage_1_Submission class\
    # Load submissions data.


#to modify !!!
def load_submissions(directory_path, user_map):
    """Load submissions from a specified directory using a specified user map.
    Optional argument:
        ref_ids: List specifying submission IDs (alphanumeric, typically) of
        reference submissions which are to be ignored/analyzed separately.
    Returns: submissions
    """
    submissions = []
    for file_path in glob.glob(os.path.join(directory_path, '*.txt')):
        try:
            submission = logPSubmission(file_path, user_map)

        except IgnoredSubmissionError:
            continue
        submissions.append(submission)
    return submissions

#Try print after defining submission class
    # submissions_stage1= load_submissions(Stage1Submission, ????_SUBMISSIONS_DIR_PATH, user_map)
    #
    # for submission in submissions_stage1:
    #     print(submission.data)
    #     print(submission.name)

#create submission collection: see line 1097