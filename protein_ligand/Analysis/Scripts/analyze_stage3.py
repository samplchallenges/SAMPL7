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

from pkganalysis import calculate_ligand_characteristics
# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
from Analysis.Scripts.pkganalysis.submission import load_submissions

STAGE_3_SUBMISSIONS_DIR_PATH = '../Submissions-stage3/'
USER_MAP_FILE_PATH = '../Analysis-outputs-stage3/SAMPL7-user-map-PL-stage3.csv'


class Stage3Submission(SamplSubmission):
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
    SECTIONS = {'Participant name', 'Participant organization', 'Name', 'Software', 'Method', 'Category', 'Ranked',
                'Predictions'}


    # Sections in CSV format with kwargs to pass to pandas.read_csv().

    CSV_SECTIONS = {'Predictions': {'names': ('Rank', 'Database identifier', 'Smiles', 'Confidence score'),
                                    'index_col': 'Rank'}}

    RENAME_METHODS = {}

    def __init__(self, file_path, user_map):
        super().__init__(file_path, user_map)

        file_name = os.path.splitext(os.path.basename(file_path))[0]
        self.file_name = file_name


        # Load predictions.
        sections = self._load_sections(file_path)  # From parent-class.
        #No prediction section yet (will have to load file path to sdf and pdb files
        self.data = sections['Predictions']  # This is a list
        self.data = pd.DataFrame(data=self.data) # Now a DataFrame

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

class Stage3SubmissionCollection:
    """A collection of Stage 3 submissions."""

    # Path to directories for organizing plots
    #STAGE1_ACCURACY_PLOT_PATH_DIR = 'Accuracy'


    def __init__(self, submissions, output_directory_path, stage3_submission_collection_file_path, ignore_refcalcs = False):


        # Check if submission collection file already exists.
        if os.path.isfile(stage3_submission_collection_file_path):
            print("Analysis will be done using the existing submission collection file: {}".format(stage3_submission_collection_file_path))

            self.data = pd.read_csv(stage3_submission_collection_file_path)
            print("\n SubmissionCollection: \n")
            print(self.data)

            # Populate submission.data dataframes parsing sections of collection file.
            for submission in submissions:

                # To ignore reference calculations, when necessary
                if submission.reference_submission and ignore_refcalcs:
                    continue

                df_collection_of_each_submission = self.data.loc[self.data["SID"] == int(submission.sid)]

            # Transform into Pandas DataFrame.
            self.output_directory_path = output_directory_path


        else: # Build collection dataframe from the beginning.
            # Build full stage 2 collection table.
            data = []

            # Submissions for stage 2.
            for submission in submissions:
                print(submission.data)
                if submission.reference_submission and ignore_refcalcs:
                    continue

                # print("submission.sid:\n", submission.sid)
                # print("submission.name:\n", submission.name)
                # print("submission.data:\n", submission.data)


                for index, row in submission.data.iterrows():

                    # Predicted data
                    Rank = index
                    Database_ID = row['Database identifier']
                    Smiles = row['Smiles']
                    Confidence = row['Confidence score']

                    data.append({
                        'SID': submission.sid,  # Previously receipt_ID
                        'Participant': submission.participant,
                        'Organization': submission.organization,
                        'Name': submission.name,
                        'Category': submission.category,
                        'Ranked': submission.ranked,
                        'Rank': Rank,
                        'Database identifier': Database_ID,
                        'Smiles': Smiles,
                        'Confience score': Confidence
                    })

            # Transform into Pandas DataFrame.
            self.data = pd.DataFrame(data=data)
            self.output_directory_path = output_directory_path

            print("\n SubmissionCollection: \n")
            print(self.data)

            # Create general output directory.
            os.makedirs(self.output_directory_path, exist_ok=True)

            # Save collection.data dataframe in a CSV file.
            self.data.to_csv(stage3_submission_collection_file_path, index=False)

            print("Stage3 submission collection file generated:\n", stage3_submission_collection_file_path)

    def generate_library_descriptors(self, fragment_screened_csv, stage_1_hit_verification_csv):

        fragment_screened = pd.read_csv(fragment_screened_csv, names=['Fragment ID', 'Smiles'])
        stage_1_hit_verification = pd.read_csv(stage_1_hit_verification_csv)
        fragment_screened['Site 1'] = stage_1_hit_verification['Site 1']

        MolWts_list = []
        MolLogP_list = []
        HBond_donors_list = []
        HBond_acceptors_list = []
        RO5_list = []

        nRings_list = []
        Rot_bonds_list = []
        TPSA_list = []


        for index, row in fragment_screened.iterrows():
            Smiles = row['Smiles']
            MolWt, MolLogP, HBond_donors, HBond_acceptors, RO5, Rings, Rot_bonds, TPSA = calculate_ligand_characteristics.calculate_rule_of_5(Smiles)
            MolWts_list.append(MolWt)
            MolLogP_list.append(MolLogP)
            HBond_donors_list.append(HBond_donors)
            HBond_acceptors_list.append(HBond_acceptors)
            RO5_list.append(RO5)
            nRings_list.append(Rings)
            Rot_bonds_list.append(Rot_bonds)
            TPSA_list.append(TPSA)

        fragment_screened['MolWt'] = MolWts_list
        fragment_screened['LogP'] = MolLogP_list
        fragment_screened['HBond donors'] = HBond_donors_list
        fragment_screened['HBond acceptors'] = HBond_acceptors_list
        fragment_screened['RO5'] = RO5_list

        fragment_screened['Rings'] = nRings_list
        fragment_screened['Rotatable bonds'] = Rot_bonds_list
        fragment_screened['TPSA'] = TPSA_list


        self.Kac_binders = fragment_screened.loc[fragment_screened['Site 1'] == True]

        dfs_to_plot_dict = {'Full library': fragment_screened,
                            'Kac binder':  self.Kac_binders}

        outpathname_fragment_screened_desc = os.path.join(self.output_directory_path,
                                                          'fragment_screened_descriptors.csv')
        fragment_screened.to_csv(outpathname_fragment_screened_desc)

        outpathname_fragment_binders_desc = os.path.join(self.output_directory_path,
                                                          'fragment_binders_descriptors.csv')
        self.Kac_binders.to_csv(outpathname_fragment_binders_desc)

        for column in fragment_screened[['MolWt', 'LogP', 'HBond donors', 'HBond acceptors',
                                         'Rings', 'Rotatable bonds', 'TPSA']].columns:
            xaxis_label = column
            outpathname = os.path.join(self.output_directory_path, column + '_library_vs_binders')
            bins = 20
            if column in ['HBond donors', 'HBond acceptors','Rings', 'Rotatable bonds']:
                if column == 'HBond donors':
                    calculate_ligand_characteristics.group_plot_descriptor(dfs_to_plot_dict, column,
                                                                           xaxis_label, outpathname, type='discrete',
                                                                           bins=bins, legend=True)
                else:
                    calculate_ligand_characteristics.group_plot_descriptor(dfs_to_plot_dict, column,
                                                               xaxis_label, outpathname, type='discrete',
                                                               bins=bins, legend=False)
            else:
                calculate_ligand_characteristics.group_plot_descriptor(dfs_to_plot_dict, column,
                                                                       xaxis_label, outpathname, type='continuous',
                                                                       bins=bins, legend=False)

        print("Compute TC for the full library")
        TC_df_full = pd.DataFrame()
        TC_fragment_screened = calculate_ligand_characteristics.calculate_TC(fragment_screened['Smiles'])
        TC_df_full['Full library'] = TC_fragment_screened
        TC_df_full['Full library'].plot.hist(bins=100, rot=0, figsize=(8, 5),
                                             weights=np.ones_like(TC_df_full['Full library'].index) / len(
                                             TC_df_full['Full library'].index), legend=False)
        print("Compute TC for the fragment hits")
        TC_df_Kac = pd.DataFrame()
        TC_Kac = calculate_ligand_characteristics.calculate_TC(self.Kac_binders['Smiles'])
        TC_df_Kac['Kac_binders'] = TC_Kac
        TC_df_Kac['Kac_binders'].plot.hist(bins=100, alpha=0.8, rot=0, figsize=(8, 5),
                                           weights=np.ones_like(TC_df_Kac['Kac_binders'].index) / len(
                                           TC_df_Kac['Kac_binders'].index), legend=False)
        plt.xlabel('Tanimoto Coefficient', fontsize=15)
        plt.ylabel("Normalized probably density", fontsize=15)
        plt.xticks(fontsize=12.5)
        plt.yticks(fontsize=12.5)
        outpathname_TC = os.path.join(self.output_directory_path, 'TC_binder_library')
        plt.savefig(outpathname_TC + '.png')
        plt.close()

        print(TC_df_full['Full library'].mean())
        print(TC_df_Kac['Kac_binders'].mean())

    def calculate_submissions_characteristics(self, stage3_submission_collection_file_path):

        MolWts_list = []
        MolLogP_list = []
        HBond_donors_list = []
        HBond_acceptors_list = []
        RO5_list = []

        nRings_list = []
        Rot_bonds_list = []
        TPSA_list = []


        for index, row in self.data.iterrows():
            Smiles = row['Smiles']
            MolWt, MolLogP, HBond_donors, HBond_acceptors, RO5, Rings, Rot_bonds, TPSA = calculate_ligand_characteristics.calculate_rule_of_5(Smiles)
            MolWts_list.append(MolWt)
            MolLogP_list.append(MolLogP)
            HBond_donors_list.append(HBond_donors)
            HBond_acceptors_list.append(HBond_acceptors)
            RO5_list.append(RO5)
            nRings_list.append(Rings)
            Rot_bonds_list.append(Rot_bonds)
            TPSA_list.append(TPSA)

        self.data['MolWt'] = MolWts_list
        self.data['LogP'] = MolLogP_list
        self.data['HBond donors'] = HBond_donors_list
        self.data['HBond acceptors'] = HBond_acceptors_list
        self.data['RO5'] = RO5_list

        self.data['Rings'] = nRings_list
        self.data['Rotatable bonds'] = Rot_bonds_list
        self.data['TPSA'] = TPSA_list

        self.data = self.data[self.data['MolWt'] != 'Error']
        #print to other than submission collection
        self.data.to_csv(stage3_submission_collection_file_path, index=False)


        #Add binders to plot
        full_data = self.Kac_binders
        full_data.drop(['Fragment ID', 'Site 1'], axis=1)

        full_data['SID'] = 'Kac binders'
        full_data['Participant'] = 'Harold Grosjean'
        full_data['Organization'] = 'Diamond Light Source'
        full_data["Name"] = 'XChem'
        full_data["Category"] = None
        full_data['Ranked'] = True
        full_data['Rank'] = None
        full_data['Database identifier'] = None
        full_data['Confience score'] = None


        full_data = full_data.append(self.data, ignore_index=True)

        dfs_to_plot_dict = dict()
        alpha = 1.0

        for SID in full_data['SID'].unique():
            TC_SID = pd.DataFrame()
            if SID == 'Kac binders':
                print('Computes TC for SID {}'.format(SID))
                TC_SID_list = calculate_ligand_characteristics.calculate_TC(
                    full_data.loc[full_data['SID'] == SID]['Smiles'])

                dfs_to_plot_dict[str(SID)] = full_data.loc[full_data['SID'] == SID]

            else:
                #compute only for top 15
                dfs_to_plot_dict[str(SID)] = full_data.loc[full_data['SID'] == SID].head(10)
                print('Computes TC for SID {}'.format(SID))
                TC_SID_list = calculate_ligand_characteristics.calculate_TC(full_data.loc[full_data['SID'] == SID].head(10)['Smiles'])

            TC_SID[SID] = TC_SID_list
            TC_SID[SID].plot.hist(bins=100, rot=0, figsize=(8, 5), alpha=alpha,
                                 weights=np.ones_like(TC_SID[SID].index) / len(
                                     TC_SID[SID].index), xlim=[0,1])
            alpha = alpha - 0.1


        plt.xlabel('Tanimoto Coefficient', fontsize=15)
        plt.ylabel("Normalized probably density", fontsize=15)
        plt.xticks(fontsize=12.5)
        plt.yticks(fontsize=12.5)
        outpathname_TC = os.path.join(self.output_directory_path, 'TC_stage3_vs_binder')
        plt.savefig(outpathname_TC + '.png')
        #plt.savefig(outpathname_TC + '.eps', format='eps')
        plt.close()


        for column in self.data[['MolWt', 'LogP', 'HBond donors', 'HBond acceptors',
                                         'Rings', 'Rotatable bonds', 'TPSA']].columns:
            xaxis_label = column
            outpathname = os.path.join(self.output_directory_path, column + '_stage3_vs_binders')
            bins = 20
            if column in ['HBond donors', 'HBond acceptors','Rings', 'Rotatable bonds']:
                if column == 'HBond donors':
                    calculate_ligand_characteristics.group_plot_descriptor(dfs_to_plot_dict, column,
                                                                           xaxis_label, outpathname, type='discrete',
                                                                           bins=bins, legend=True)
                else:
                    calculate_ligand_characteristics.group_plot_descriptor(dfs_to_plot_dict, column,
                                                               xaxis_label, outpathname, type='discrete',
                                                               bins=bins, legend=False)
            else:
                calculate_ligand_characteristics.group_plot_descriptor(dfs_to_plot_dict, column,
                                                                       xaxis_label, outpathname, type='continuous',
                                                                       bins=bins, legend=False)


    def plot_main_table(self, stage3_submission_collection_file_path):

        outfile_table_top_10 = os.path.join(self.output_directory_path, 'top10_table.png')

        calculate_ligand_characteristics.plot_top_n_molecules(self.data, outfile_table_top_10, topn=10)


if __name__ == '__main__':

    #Import user map.
    try:
        with open(USER_MAP_FILE_PATH, 'r') as f:
            user_map = pd.read_csv(f)
            #print("user_map:\n", user_map)
    except FileNotFoundError:
        user_map=None
        print("Warning: No user map found.")


    STAGE_3_SUBMISSIONS_DIR_PATH_ALL = '../Submissions-stage3/'
    OUTPUT_DIRECTORY_PATH = '../Analysis-outputs-stage3/'
    submissions = load_submissions(Stage3Submission, STAGE_3_SUBMISSIONS_DIR_PATH_ALL, user_map)
    stage3_submission_collection_file_path = '{}/stage3_submission_collection.csv'.format(OUTPUT_DIRECTORY_PATH)

    SubmissionCollection = Stage3SubmissionCollection(submissions,
                                                     OUTPUT_DIRECTORY_PATH,
                                                     stage3_submission_collection_file_path,
                                                     ignore_refcalcs=False)

    fragment_screened_csv = '../../fragments_screened.csv'
    stage_1_hit_verification_csv = '../../experimental-data/stage-1/hits_verification.csv'
    SubmissionCollection.generate_library_descriptors(fragment_screened_csv, stage_1_hit_verification_csv)

    SubmissionCollection.calculate_submissions_characteristics(stage3_submission_collection_file_path)

    SubmissionCollection.plot_main_table(stage3_submission_collection_file_path)
# pdb_overview = pd.read_csv('./experimental-data/stage-2/pdbs_overview.csv', index_col=0)
# site_1 = pdb_overview.loc[pdb_overview['site-1'] == True]
# ms = [Chem.MolFromSmiles(x) for x in site_1['Smiles']]
#
# labels = []
# for index, row in site_1.iterrows():
#     fname = row['Fragment_IDs']
#     pdbid = row['PDBs']
#     smile = row['Smiles']
#     label = fname + '\n' + pdbid + '\n' + smile
#     labels.append(label)
#
# image = Draw.MolsToGridImage(ms, legends=labels,
#                     subImgSize=(195,195), molsPerRow=6)
# image.show()