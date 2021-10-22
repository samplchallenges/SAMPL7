import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from pkganalysis.submission import (SamplSubmission, IgnoredSubmissionError)

from pkganalysis.RMSD_calculator_HG import RMSD_calculator, RMSD_calculator_protein
# =============================================================================
# CONSTANTS
# =============================================================================

# Paths to input data.
from Analysis.Scripts.pkganalysis.submission import load_submissions

STAGE_2_SUBMISSIONS_DIR_PATH = '../Submissions-stage2/'
EXPERIMENTAL_DATA_FILE_PATH = '../../experimental-data/stage-2/'
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

    def __init__(self, submissions, input_data, apo_structure, pdbs_directory, stage2_submission_collection_file_path):

        self.apo_structure = apo_structure

        if os.path.isfile(stage2_submission_collection_file_path):

            self.data = pd.read_csv(stage2_submission_collection_file_path)

        else:

            #Generate submission collection from scratch
            collection = pd.DataFrame(columns=['Site', 'Fragment', 'Smile', 'PDB', 'RMSD exp-apo',
                                               'Pose 1 Ligand','RMSD pose 1 ligand', 'Pose 1 Protein', 'RMSD pose 1 exp-pred', 'RMSD pose 1 apo-pred',
                                               'Pose 2 Ligand','RMSD pose 2 ligand',  'Pose 2 Protein', 'RMSD pose 2 exp-pred', 'RMSD pose 2 apo-pred',
                                               'Pose 3 Ligand','RMSD pose 3 ligand',  'Pose 3 Protein', 'RMSD pose 3 exp-pred', 'RMSD pose 3 apo-pred',
                                               'Pose 4 Ligand','RMSD pose 4 ligand',  'Pose 4 Protein', 'RMSD pose 4 exp-pred', 'RMSD pose 4 apo-pred',
                                               'Pose 5 Ligand','RMSD pose 5 ligand',  'Pose 5 Protein', 'RMSD pose 5 exp-pred', 'RMSD pose 5 apo-pred'])

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
                    identifier = file.replace('.sdf', '').replace('.mol2', '').replace('.pdb', '')
                    split = identifier.split('-')

                    if file.endswith('.sdf') or file.endswith('.mol2'):
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

            #Drop all row where participant is Chunyu Yu as submitted unphysical molecules
            #Mention it in the paper

            submission_collection.drop(submission_collection.loc[submission_collection['Participant'] == 'Chunyu Yu'].index, inplace=True)

            ##No submission made for Site 2, 3 and 4
            for site in ['site-2', 'site-3', 'site-4']:
                submission_collection.drop(submission_collection.loc[submission_collection['Site'] == site].index, inplace=True)

            #../Submissions-stage2/PHIP2_2_IFP_IE46/IFP_IE46/PHIP2-F529-1.sdf wrong molecule submitted
            submission_collection = submission_collection.replace('../Submissions-stage2/PHIP2_2_IFP_IE46/IFP_IE46/PHIP2-F529-1.sdf', np.NaN)

            # ../Submissions-stage2/PHIP2_2_IFP_IE46/IFP_IE46/PHIP2-F529-2.sdf wrong molecule submitted
            submission_collection = submission_collection.replace('../Submissions-stage2/PHIP2_2_IFP_IE46/IFP_IE46/PHIP2-F529-2.sdf', np.NaN)

            #../Submissions-stage2/PHIP2_mms/poses/PHIP2-F126-{1,2,3,4,5}.sdf wrong molecules submitted - chloride atom replaced by carbon
            indexNames = submission_collection[(submission_collection['SID'] == '77') & (submission_collection['Fragment'] == 'F126')].index
            submission_collection.drop(indexNames, inplace=True)

            #../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F14-{1,2,3,4,5}.sdf wrong molecules submitted - replaced bromide by boron
            indexNames = submission_collection[(submission_collection['SID'] == '78') & (submission_collection['Fragment'] == 'F14')].index
            submission_collection.drop(indexNames, inplace=True)

            #../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F126-{1,2,3,4,5}.sdf wrong molecules submitted - chloride atom replaced by carbon
            indexNames = submission_collection[(submission_collection['SID'] == '78') & (submission_collection['Fragment'] == 'F126')].index
            submission_collection.drop(indexNames, inplace=True)

            #../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F362-1.sdf - wrong bonding
            submission_collection = submission_collection.replace('../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F362-1.sdf', np.NaN)

            #../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F368-5.sdf - wrong bonding
            submission_collection = submission_collection.replace('../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F368-5.sdf', np.NaN)

            #../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F603-3.sdf - wrong bonding
            submission_collection = submission_collection.replace('../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F603-3.sdf', np.NaN)

            #../Submissions-stage2/PHIP2_2_cryptoscout/cryptoscout/PHIP2-F760-1.sdf wrong molecules submitted - bromide atom replaced by boron
            indexNames = submission_collection[(submission_collection['SID'] == '78') & (submission_collection['Fragment'] == 'F760')].index
            submission_collection.drop(indexNames, inplace=True)

            #../Submissions-stage2/PHIP2_stage2_submission_Iorga_pose_prediction_1/PHIP2_stage2_submission_Iorga_pose_prediction_1/PHIP2-F603-1.mol2 unvalid molecule submitted
            # wrong protonation state of ring ring nitrogens preventing processing
            submission_collection = submission_collection.replace('../Submissions-stage2/PHIP2_stage2_submission_Iorga_pose_prediction_1/PHIP2_stage2_submission_Iorga_pose_prediction_1/PHIP2-F603-1.mol2', np.NaN)

            #TO DO IMPROVE SCRIPT SO THAT IT IDENTIFIES MISMATCHING LIGANDS AND DISCrd


            self.data = submission_collection
            submission_collection.to_csv(stage2_submission_collection_file_path, index=False)

    def calculate_RMSD(self, stage2_submission_collection_file_path, binding_site_distance_cutoff = float(5.0)):

        data = self.data
        print(data['Pose 1 Ligand'])

        for row in list(data.index.values):

            reference = data.loc[row, 'PDB']
            smile = data.loc[row, 'Smile']

            for pose in [1,2,3,4,5]:

                lig_pred = data.loc[row, 'Pose {} Ligand'.format(str(pose))]
                prot_pred = data.loc[row, 'Pose {} Protein'.format(str(pose))]



                if not pd.isna(data.loc[row, 'RMSD pose {} ligand'.format(pose)])\
                        and not pd.isna(data.loc[row, 'RMSD exp-apo'])\
                        and not pd.isna(data.loc[row, 'RMSD pose {} exp-pred'.format(pose)])\
                        and not pd.isna(data.loc[row, 'RMSD pose {} apo-pred'.format(pose)]):
                    pass

                #check manually deleted data and remove all lines

                else:
                    # calculates RMSD for ligands
                    if not pd.isna(data.loc[row, 'Pose {} Ligand'.format(pose)]):
                        #calculates rmsd for ligand
                        print(data.loc[row, 'Pose {} Ligand'.format(pose)])
                        rmsd = RMSD_calculator(reference, lig_pred, smile, prot_pred)
                        print('ligand rmsd is: ' + str(rmsd))
                        data.loc[row, 'RMSD pose {} ligand'.format(pose)] = float(rmsd)

                    #calculates RMSD for protein
                    if not pd.isna(data.loc[row, 'Pose {} Protein'.format(pose)]):
                        #calculates rmsd for protein
                        print(data.loc[row, 'Pose {} Protein'.format(pose)])
                        [rmsd_exp_apo, rmsd_exp_prediction, rmsd_apo_prediction] = RMSD_calculator_protein(reference, prot_pred, apo_structure, binding_site_distance_cutoff)
                        data.loc[row, 'RMSD exp-apo'] = rmsd_exp_apo
                        print('experimental vs apo rmsd is: ' + str(rmsd_exp_apo))
                        data.loc[row, 'RMSD pose {} exp-pred'.format(pose)] = rmsd_exp_prediction
                        print('experimental vs prediction rmsd is: ' + str(rmsd_exp_prediction))
                        data.loc[row, 'RMSD pose {} apo-pred'.format(pose)] = rmsd_apo_prediction
                        print('apo vs prediction rmsd is: ' + str(rmsd_apo_prediction))


        self.data = data
        submission_collection = self.data
        submission_collection.to_csv(stage2_submission_collection_file_path, index=False)

    def calculate_statistics(self, pdb_overview, rmsd_cutoff, ranking, output_directory_path):

        data = self.data


        if ranking == ('Ranked_and_non-ranked' or None):
            data = data
        if ranking == 'Ranked':
            data = data[data['Ranked'] == True]
        if ranking == 'Non-ranked':
            data = data[data['Ranked'] == False]

        rmsd_cutoff = float(rmsd_cutoff)

        ligand_rmsds = ['RMSD pose 1 ligand', 'RMSD pose 2 ligand', 'RMSD pose 3 ligand', 'RMSD pose 4 ligand', 'RMSD pose 5 ligand']
        data['Best pose ligand'] = data[ligand_rmsds].min(axis=1)
        data['Highest scoring pose'] = data['RMSD pose 1 ligand']
        data['Average poses value'] = data[ligand_rmsds].mean(axis=1)
        data['Standard deviation to average poses value'] = data[ligand_rmsds].std(axis=1, skipna=True)

    #What method perform the best/worst?

        SIDs = data.SID.unique()
        stats_dict = {'SIDs': data.SID.unique(),
                      'Best poses average': list(),
                      'Best poses stds': list(),
                      'Successes best poses': list(),
                      'Fails best poses': list(),
                      'Success rate best poses': list(),
                      'Highest poses average': list(),
                      'Highest poses stds': list(),
                      'Successes highest poses': list(),
                      'Fails highest poses': list(),
                      'Successes rate highest poses': list(),
                      #'Average poses averages': list(),
                      #'Average poses stds': list()
                      }

        rmsd_increment = np.arange(0.0, 9.01, 0.01)
        successVSrmsd_best = {'RMSD': rmsd_increment}
        successVSrmsd_highest = {'RMSD': rmsd_increment}

        for SID in SIDs:
            df_SID = data.loc[data['SID'] == SID]

            stats_dict['Best poses average'].append(df_SID['Best pose ligand'].mean())
            stats_dict['Best poses stds'].append(df_SID['Best pose ligand'].std())
            best_poses = data.loc[data['SID'] == SID]['Best pose ligand']
            stats_dict['Successes best poses'].append(best_poses[best_poses <= rmsd_cutoff].count())
            stats_dict['Fails best poses'].append(best_poses[best_poses > rmsd_cutoff].count())
            total_best = best_poses[best_poses <= rmsd_cutoff].count() + best_poses[best_poses > rmsd_cutoff].count()
            stats_dict['Success rate best poses'].append(best_poses[best_poses <= rmsd_cutoff].count()/total_best)


            stats_dict['Highest poses average'].append(df_SID['Highest scoring pose'].mean())
            stats_dict['Highest poses stds'].append(df_SID['Highest scoring pose'].std())
            highest_poses = data.loc[data['SID'] == SID]['Highest scoring pose']
            stats_dict['Successes highest poses'].append(highest_poses[highest_poses <= rmsd_cutoff].count())
            stats_dict['Fails highest poses'].append(highest_poses[highest_poses > rmsd_cutoff].count())
            total_highest = highest_poses[highest_poses <= rmsd_cutoff].count() + highest_poses[highest_poses > rmsd_cutoff].count()
            stats_dict['Successes rate highest poses'].append(highest_poses[highest_poses <= rmsd_cutoff].count()/total_highest)

            # stats_dict['Average poses averages'].append(df_SID['Average poses value'].mean())
            # stats_dict['Average poses stds'].append(df_SID['Average poses value'].std())

            # generate succes rate as function of RMSD for SIDs
            successVSrmsd_best[SID] = list()
            successVSrmsd_highest[SID] = list()
            for rmsd in rmsd_increment:
                successVSrmsd_best[SID].append(best_poses[best_poses <= rmsd].count() / total_best)
                successVSrmsd_highest[SID].append(highest_poses[highest_poses <= rmsd].count() / total_highest)

        os.makedirs(output_directory_path + '/' + ranking, exist_ok=True)

        #Save tables and plot figures
        stat_table_SIDs = pd.DataFrame(stats_dict).sort_values(by=['Best poses average'])
        stat_table_SIDs.to_csv('{}/{}/methods_statistics_table_for_{}_submissions.csv'.format(output_directory_path, ranking, ranking),
                               index_label=False,
                               index=False)

        #plt.figure(figsize = (10, 8))
        #TO DO: Add correct legends
        fig = stat_table_SIDs[['Successes rate highest poses', 'Success rate best poses']].plot.bar(rot=0, figsize = (10, 8))
        plt.legend(['Top 1', ' Best in all'], fontsize=17.5)
        fig.set_xticklabels(stat_table_SIDs.SIDs)
        plt.title('Prediction performance for submissions'.format(ranking), loc='center', fontsize=25)
        plt.ylabel('Success rate (%)', fontsize=20)
        plt.xlabel('SID', fontsize=20)

        #make bigger lables
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)

        plt.savefig('{}/{}/methods_statistics_table_for_{}_submissions.png'.format(output_directory_path, ranking, ranking))
        #plt.savefig('{}/{}/methods_statistics_table_for_{}_submissions.eps'.format(output_directory_path, ranking, ranking), format='eps')
        plt.close()

        successVSrmsd_best_table_SID = pd.DataFrame(successVSrmsd_best)
        #successVSrmsd_best_table_SID.to_csv('{}/{}/SuccessVSrmsd_best_for_{}_submissions.csv'.format(output_directory_path, ranking, ranking),
        #                       index_label=False,
        #                       index=False)

        plt.figure(figsize=(10, 6))
        plt.title('Best in all'.format(ranking), loc='center', fontsize=25)
        for SID in successVSrmsd_best_table_SID.columns[1:]:
            plt.plot(successVSrmsd_best_table_SID['RMSD'],
                     successVSrmsd_best_table_SID[SID],
                     label=SID)
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        plt.axvline(2, 0, 1, label='RMSD cut-off', color='black', linestyle='--')
        plt.xlabel('RMSD cut-off ($\AA$)', fontsize=20)
        plt.ylabel('Success Rate', fontsize=20)
        plt.legend(fontsize=12)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.savefig('{}/{}/SuccessVSrmsd_best_for_{}_submissions.png'.format(output_directory_path, ranking, ranking))
        #plt.savefig('{}/{}/SuccessVSrmsd_best_for_{}_submissions.eps'.format(output_directory_path, ranking, ranking),format='eps')
        plt.close()

        successVSrmsd_highest_table_SID = pd.DataFrame(successVSrmsd_highest)
        #successVSrmsd_highest_table_SID.to_csv('{}/{}/SuccessVSrmsd_highest_for_{}_submissions.csv'.format(output_directory_path, ranking, ranking),
        #                       index_label=False,
        #                       index=False)

        plt.figure(figsize=(10, 6))
        plt.title('Top 1'.format(ranking), loc='center', fontsize=25)
        for SID in successVSrmsd_highest_table_SID.columns[1:]:
            plt.plot(successVSrmsd_highest_table_SID['RMSD'],
                     successVSrmsd_highest_table_SID[SID],
                     label=SID)
        plt.axvline(2, 0, 1, label='RMSD cut-off', color='black', linestyle='--')
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        plt.xlabel('RMSD cut-off ($\AA$)', fontsize=20)
        plt.ylabel('Success Rate', fontsize=20)
        plt.legend(fontsize=12)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.savefig('{}/{}/SuccessVSrmsd_highest_for_{}_submissions.png'.format(output_directory_path, ranking, ranking))
        #plt.savefig('{}/{}/SuccessVSrmsd_highest_for_{}_submissions.eps'.format(output_directory_path, ranking, ranking),
                    #format='eps')
        plt.close()

    #What fragment is docked the best/worst? success rate for method as well
    #calculate success dockings (RMSD <= 2) and failure

        pdbs = pd.read_csv(pdb_overview, index_col=0)
        #remove fragment F400 as not given in stage 2
        pdbs = pdbs[pdbs['Fragment_IDs'] != 'F400']
        site_1_fragment_ids = pdbs.loc[pdbs['site-1'] == True]['Fragment_IDs'].tolist()

        success_rates_dict_frags = {'Fragments': site_1_fragment_ids,
                              'Successes best poses': list(),
                              'Fails best poses': list(),
                              'Successes rate best poses': list(),
                              'Successes highest poses': list(),
                              'Fails highest poses': list(),
                              'Successes rate highest poses': list()}

        # rmsd_increment = np.arange(0.0, 3.01, 0.01)
        # successVSrmsd_best = {'RMSD': rmsd_increment}
        # successVSrmsd_highest = {'RMSD': rmsd_increment}

        for fragment in site_1_fragment_ids:
            best_poses = data.loc[data['Fragment'] == fragment]['Best pose ligand']
            success_rates_dict_frags['Successes best poses'].append(best_poses[best_poses <= rmsd_cutoff].count())
            success_rates_dict_frags['Fails best poses'].append(best_poses[best_poses > rmsd_cutoff].count())
            total_best = best_poses[best_poses <= rmsd_cutoff].count() + best_poses[best_poses > rmsd_cutoff].count()
            success_rates_dict_frags['Successes rate best poses'].append(best_poses[best_poses <= rmsd_cutoff].count()/total_best)


            highest_poses = data.loc[data['Fragment'] == fragment]['Highest scoring pose']
            success_rates_dict_frags['Successes highest poses'].append(highest_poses[highest_poses <= rmsd_cutoff].count())
            success_rates_dict_frags['Fails highest poses'].append(highest_poses[highest_poses > rmsd_cutoff].count())
            total_highest = highest_poses[highest_poses <= rmsd_cutoff].count() + highest_poses[highest_poses > rmsd_cutoff].count()
            success_rates_dict_frags['Successes rate highest poses'].append(highest_poses[highest_poses <= rmsd_cutoff].count()/total_highest )

            # successVSrmsd_best[fragment] = list()
            # successVSrmsd_highest[fragment] = list()
            # for rmsd in rmsd_increment:
            #     successVSrmsd_best[fragment].append(best_poses[best_poses <= rmsd].count() / total_best)
            #     successVSrmsd_highest[fragment].append(highest_poses[highest_poses <= rmsd].count() / total_highest)

        ligands_success_rates = pd.DataFrame(data=success_rates_dict_frags)
        #re-order dataframe
        ligands_success_rates['tmp'] = [int(fragment[1:]) for fragment in ligands_success_rates['Fragments']]
        ligands_success_rates.sort_values('tmp', ascending=True, inplace=True)
        del ligands_success_rates['tmp']

        # Save tables and plot figures
        ligands_success_rates.to_csv('{}/{}/ligands_success_rates_table_for_{}_submissions.csv'.format(output_directory_path, ranking, ranking),
                                     index_label=False,
                                     index=False)

        #plt.figure(figsize = (10, 8))
        fig = ligands_success_rates[['Successes rate highest poses', 'Successes rate best poses']].plot.bar(rot=90, width=0.9,
                                                                                        figsize=(10, 8),
                                                                                        legend=False)
        #plt.legend(['Top 1', ' Best in all'])
        plt.title('Perdiction performances for fragments'.format(ranking), loc='center', fontsize=25)
        #plt.ylabel('Success rate')
        plt.xlabel('Fragment', fontsize=20)
        fig.set_xticklabels(ligands_success_rates.Fragments)
        plt.legend(fontsize=12.5)
        plt.xticks(fontsize=12.5)
        plt.yticks(fontsize=15)
        plt.savefig('{}/{}/ligands_success_rates_table_for_{}_submissions.png'.format(output_directory_path, ranking, ranking))
        #plt.savefig('{}/{}/ligands_success_rates_table_for_{}_submissions.eps'.format(output_directory_path, ranking, ranking), format='eps')
        plt.close()
        # successVSrmsd_best_table_SID = pd.DataFrame(successVSrmsd_best)
        # successVSrmsd_best_table_SID.to_csv('{}/{}/Fragments_successVSrmsd_best_for_{}_submissions.csv'.format(output_directory_path, ranking, ranking),
        #                        index_label=False,
        #                        index=False)
        #
        # successVSrmsd_highest_table_SID = pd.DataFrame(successVSrmsd_highest)
        # successVSrmsd_highest_table_SID.to_csv('{}/{}/Fragments_successVSrmsd_highest_for_{}_submissions.csv'.format(output_directory_path, ranking, ranking),
        #                        index_label=False,
        #                        index=False)




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

    apo_structure = '../../PHIPA_C2_Apo.pdb'
    input_data = '../../Stage-2-input-data/'
    pdbs_directory = '../../experimental-data/stage-2/'
    overview_pdbs = '../../experimental-data/stage-2/pdbs_overview.csv'
    output_directory_path =  '../Analysis-outputs-stage2/'
    stage2_submission_collection_file_path = '{}stage2_submission_collection.csv'.format(output_directory_path)
    Stage2SubmissionCollection = Stage2SubmissionCollection(submissions, input_data, apo_structure, pdbs_directory, stage2_submission_collection_file_path)
    Stage2SubmissionCollection.calculate_RMSD(stage2_submission_collection_file_path, binding_site_distance_cutoff = 5.0)

    for ranking in ["Ranked_and_non-ranked", "Ranked", "Non-ranked"]:
        Stage2SubmissionCollection.calculate_statistics(overview_pdbs, rmsd_cutoff=2.0, ranking=ranking, output_directory_path=output_directory_path)