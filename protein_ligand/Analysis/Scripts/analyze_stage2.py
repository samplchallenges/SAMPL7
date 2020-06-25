import os
import glob
import copy
import collections
import pickle
import tarfile

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from pkganalysis.submission import (SamplSubmission, IgnoredSubmissionError,
                                    load_submissions, plot_correlation)


# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
from Analysis.Scripts.pkganalysis.submission import load_submissions

STAGE_2_SUBMISSIONS_DIR_PATH = '../Submissions-stage2/'
EXPERIMENTAL_DATA_FILE_PATH = '../../stage-3-input-data/cocrystals/'
USER_MAP_FILE_PATH = '../Analysis-outputs-stage2/SAMPL7-user-map-PL-stage2.csv'


class Stage2Submission(SamplSubmission):
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
    SECTIONS = {'Participant name', 'Participant organization', 'Name', 'Software', 'Method', 'Category', 'Ranked'}


    # Sections in CSV format with kwargs to pass to pandas.read_csv().

    CSV_SECTIONS = {}


    RENAME_METHODS = {}

    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.file_name = file_name

        output_directory = file_path.replace('.tar', '').replace('.gz', '')
        subdir = os.listdir(output_directory)[0]
        new_path = str(output_directory + '/' + subdir + '/PHIP2_2-description.txt')
        self.file_path = new_path
        #print('updated path is:' + str(self.file_path))

        #TO DO:  Not sure if I'm going to use the immediately following for anything
        #file_name_simple = file_name.replace('_','-')
        #file_data = file_name_simple.split('-')
        #self.host_name = file_data[0]

        # Load predictions.
        sections = self._load_sections(self.file_path)  # From parent-class.
        #No prediction section yet (will have to load file path to sdf and pdb files
        #self.data = sections['Predictions']  # This is a list
        #self.data = pd.DataFrame(data=self.data) # Now a DataFrame
        try:
            self.name = self.RENAME_METHODS[sections['Name'][0]]
        except KeyError:
            self.name = sections['Name'][0]

        # Store participant name, organization, method category
        self.participant = sections['Participant name'][0].strip()
        self.category = sections['Category'][0].strip()
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

class Stage2SubmissionCollection:
    """A collection of Stage 2 submissions."""

    def __init__(self, submissions, input_data, pdbs_directory, stage2_submission_collection_file_path):


        if os.path.isfile(stage2_submission_collection_file_path):

            self.data = pd.read_csv(stage2_submission_collection_file_path)

        else:

            #Generate submission collection from scratch
            collection = pd.DataFrame(columns=['Site', 'Fragment', 'Smile', 'PDB',
                                               'Pose 1 Ligand', 'Pose 1 Protein',
                                               'Pose 2 Ligand', 'Pose 2 Protein',
                                               'Pose 3 Ligand', 'Pose 3 Protein',
                                               'Pose 4 Ligand', 'Pose 4 Protein',
                                               'Pose 5 Ligand', 'Pose 5 Protein'])

            for file in os.listdir(input_data):
                if file.endswith('.csv'):
                    csv_file_path = os.path.join(input_data, file)
                    df = pd.read_csv(csv_file_path, names=['Fragment', 'Smile'])
                    df.insert(0, 'Site', file[0:6])

                    for pdb in os.listdir(pdbs_directory):
                        if pdb.endswith('.pdb'):
                            fragment = pdb.split('-')[0]
                            pdb_file_path = os.path.join(pdbs_directory, pdb)
                            df.loc[df['Fragment'] == fragment, 'PDB'] = pdb_file_path

                    collection = collection.append(df, ignore_index=True, sort=False)

            submission_collection_list = []

            for submission in submissions:

                submission_collection_df = collection.copy()

                submission_collection_df.insert(0, 'Ranked', submission.ranked)
                submission_collection_df.insert(0, 'Name', submission.name)
                submission_collection_df.insert(0, 'Category', submission.category)
                submission_collection_df.insert(0, 'Organization', submission.organization)
                submission_collection_df.insert(0, 'Participant', submission.participant)
                submission_collection_df.insert(0, 'SID', submission.sid)

                dir_path = submission.file_path.replace('PHIP2_2-description.txt', '')

                for file in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file)
                    identifier = file[:-4]
                    split = identifier.split('-')

                    if file.endswith('.sdf'):
                        fragment = split[1]
                        pose_id = int(split[2])
                        if pose_id == 1:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 1 Ligand'] = file_path
                        if pose_id == 2:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 2 Ligand'] = file_path
                        if pose_id == 3:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 3 Ligand'] = file_path
                        if pose_id == 4:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 4 Ligand'] = file_path
                        if pose_id == 5:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 5 Ligand'] = file_path

                    if file.endswith('.pdb'):
                        fragment = split[1]
                        pose_id = int(split[2])
                        if pose_id == 1:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 1 Protein'] = file_path
                        if pose_id == 2:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 2 Protein'] = file_path
                        if pose_id == 3:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 3 Protein'] = file_path
                        if pose_id == 4:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 4 Protein'] = file_path
                        if pose_id == 5:
                            submission_collection_df.loc[submission_collection_df['Fragment'] == fragment, 'Pose 5 Protein'] = file_path

                submission_collection_list.append(submission_collection_df)

            submission_collection = pd.concat(submission_collection_list, ignore_index=True, sort=False)

            self.data = submission_collection

            submission_collection.to_csv(stage2_submission_collection_file_path)



# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':

    #Import user map.
    try:
        with open(USER_MAP_FILE_PATH, 'r') as f:
            user_map = pd.read_csv(f)
            #print("user_map:\n", user_map)
    except FileNotFoundError:
        user_map=None
        print("Warning: No user map found.")



    STAGE_2_SUBMISSIONS_DIR_PATH_ALL = '../Submissions-stage2/'
    submissions = load_submissions(Stage2Submission, STAGE_2_SUBMISSIONS_DIR_PATH_ALL, user_map)

    input_data = '../../Stage-2-input-data/'
    pdbs_directory = '../../stage-3-input-data/cocrystals'
    output_directory_path =  '../Analysis-outputs-stage2/'
    stage2_submission_collection_file_path = '{}stage2_submission_collection.csv'.format(output_directory_path)
    Stage2SubmissionCollection(submissions, input_data, pdbs_directory, stage2_submission_collection_file_path)





