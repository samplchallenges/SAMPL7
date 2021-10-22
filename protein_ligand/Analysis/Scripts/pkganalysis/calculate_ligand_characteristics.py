#!/usr/bin/env python
__author__ = "Harold Grosjean"
__email__ = "haroldgrosjean@gmail.com"

import numpy as np
import pandas as pd
import rdkit
from rdkit import DataStructs, Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, SaltRemover, Draw

import matplotlib.pyplot as plt

def calculate_descriptors(smiles):

    mol = Chem.MolFromSmiles(smiles)

    #removes salt from molecule
    remover = SaltRemover.SaltRemover()
    mol = remover.StripMol(mol)

    MolWt = Descriptors.ExactMolWt(mol)
    MolLogP = Descriptors.MolLogP(mol)
    HBond_donors = Descriptors.NumHDonors(mol)
    HBond_acceptors = Descriptors.NumHAcceptors(mol)

    Rings =  rdMolDescriptors.CalcNumRings(mol)
    Rot_bonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    TPSA = Descriptors.TPSA(mol)

    return MolWt, MolLogP, HBond_donors, HBond_acceptors, Rings, Rot_bonds, TPSA

def calculate_rule_of_5(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return "Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error"

    MolWt, MolLogP, HBond_donors, HBond_acceptors, Rings, Rot_bonds, TPSA = calculate_descriptors(smiles)

    if MolWt < 500 and MolLogP < 5 and HBond_donors < 5 and HBond_acceptors < 10:
        return MolWt, MolLogP, HBond_donors, HBond_acceptors, True, Rings, Rot_bonds, TPSA

    else:
        return MolWt, MolLogP, HBond_donors, HBond_acceptors, False, Rings, Rot_bonds, TPSA

def group_plot_descriptor(dfs_to_plot_dict, column,
                          xaxis_label, outpathname, type="discrete", bins=20, legend=True):


    dfs = []
    legends = []

    alpha = 1.0
    for df in dfs_to_plot_dict:
        legends.append(df)
        if type == "discrete":
            dfs.append(dfs_to_plot_dict[df][column].value_counts() / len(dfs_to_plot_dict[df][column].index))

        if type == "continuous":
            dfs_to_plot_dict[df][column].plot.hist(bins=bins, alpha=alpha,
                                                   weights=np.ones_like(dfs_to_plot_dict[df][column].index) / len(dfs_to_plot_dict[df][column].index),
                                                   figsize=(8, 5), legend=False)

        alpha = alpha - 0.1

    if type == "discrete":
        pd.concat(dfs, axis=1).fillna(0).plot.bar(rot=0, figsize=(8, 5), legend=False)

    plt.xlabel(xaxis_label, fontsize=15)
    plt.ylabel("Normalized probably density", fontsize=15)
    plt.xticks(fontsize=12.5)
    plt.yticks(fontsize=12.5)
    if legend == True:
        plt.legend(legends, fontsize=15)
    else:
        pass

    plt.savefig(outpathname + '.png')
    #plt.savefig(outpathname + '.eps', format='eps')
    plt.close()

def calculate_TC(Smiles_column_list):

    remover = SaltRemover.SaltRemover()

    TC_list = []
    for index_i, smile_i in enumerate(Smiles_column_list):
        for index_j, smile_j in enumerate(Smiles_column_list):
            if index_i > index_j:
                mol_i = Chem.MolFromSmiles(smile_i)
                mol_i = remover.StripMol(mol_i)
                fp_i = Chem.RDKFingerprint(mol_i)
                mol_j = Chem.MolFromSmiles(smile_j)
                mol_j = remover.StripMol(mol_j)
                fp_j = Chem.RDKFingerprint(mol_j)
                TC = DataStructs.FingerprintSimilarity(fp_i, fp_j, metric=DataStructs.DiceSimilarity)
                TC_list.append(TC)

    return TC_list

def plot_top_n_molecules(data, outfile, topn=10):

    identifiers = list()
    mols = list()
    for sid in data['SID'].unique():
        submission_top_n = data.loc[data['SID'] == sid].sort_values(by='Rank').head(10)
        identifiers_sid = submission_top_n['Database identifier'].values
        identifiers.append(identifiers_sid)
        smiles = submission_top_n['Smiles'].values
        mols_sid = [Chem.MolFromSmiles(smile) for smile in smiles]
        mols.append(mols_sid)

    new_identifiers = list()
    for identifiers_sid in zip(*identifiers):
        for identifier in identifiers_sid:
            new_identifiers.append(identifier)

    new_mols = list()
    for mols_sids in zip(*mols):
        for mol in mols_sids:
            new_mols.append(mol)


    # Display molecules with labels
    img = Draw.MolsToGridImage(new_mols, legends=[label for label in new_identifiers],
                               subImgSize=(160, 160), molsPerRow=4)#, maxMols=len(mols))
    img.save(outfile)