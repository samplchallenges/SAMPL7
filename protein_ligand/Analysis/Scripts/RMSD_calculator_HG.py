import os
import subprocess
import numpy as np
from spyrmsd import io, rmsd
import rdkit as rdk
from rdkit.Chem import AllChem
from rdkit.Chem import SaltRemover
import MDAnalysis as mda
from MDAnalysis.analysis import align, rms
#print(mda.__version__)
# class docking_rsmd:
#     def __init__(self, reference, mobile, smile):
def change_mol_format(ligand, smile, lig_name, outname):

    remover = SaltRemover.SaltRemover()
    template1 = AllChem.MolFromSmiles(smile)
    template2 = remover.StripMol(template1)

    format = ligand.split('.')[-1]
    if format == 'pdb':
        mol = AllChem.MolFromPDBFile(ligand)

        if mol is not None:
            #mol = rdk.Chem.RemoveAllHs(mol)
            newmol = AllChem.AssignBondOrdersFromTemplate(template2, mol)
            newmol.SetProp("_Name", lig_name)
            rdk.Chem.SanitizeMol(newmol)
            w = rdk.Chem.SDWriter('{}_{}.sdf'.format(lig_name, outname))
            w.write(newmol)
            w.close()

        # TO DO: Record invalid molecules
        if mol is None:
            print('Invalid molecule')
            mol = rdk.Chem.MolFromMolFile(ligand, sanitize=False)
            mol.SetProp("_Name", lig_name)
            w = rdk.Chem.SDWriter('{}_{}.sdf'.format(lig_name, outname))
            w.write(mol)
            w.close()

    if format == 'sdf':
        mol = rdk.Chem.MolFromMolFile(ligand)

        if mol is not None:
            newmol = AllChem.AssignBondOrdersFromTemplate(template2, mol)
            newmol.SetProp("_Name", lig_name)
            rdk.Chem.SanitizeMol(newmol)
            rdk.Chem.MolToPDBFile(newmol, '{}_{}.pdb'.format(lig_name, outname))
            infile = open('{}_{}.pdb'.format(lig_name, outname), 'r')
            lines = infile.readlines()
            infile.close()
            newlines = [line.replace('UNL', lig_name) for line in lines]
            outfile = open('{}_{}.pdb'.format(lig_name, outname), 'w')
            outfile.writelines(newlines)
            outfile.close()

        #TO DO: Record invalid molecules
        if mol is None:
            print('Invalid molecule')
            mol = rdk.Chem.MolFromMolFile(ligand, sanitize=False)
            mol.SetProp("_Name", lig_name)
            rdk.Chem.MolToPDBFile(mol, '{}_{}.pdb'.format(lig_name, outname))
            infile = open('{}_{}.pdb'.format(lig_name, outname), 'r')
            lines = infile.readlines()
            infile.close()
            newlines = [line.replace('UNL', lig_name) for line in lines]
            outfile = open('{}_{}.pdb'.format(lig_name, outname), 'w')
            outfile.writelines(newlines)
            outfile.close()

    if format =='mol2':
        mol = rdk.Chem.MolFromMol2File(ligand)
        if mol is not None:
            newmol = AllChem.AssignBondOrdersFromTemplate(template2, mol)
            newmol.SetProp("_Name", lig_name)
            rdk.Chem.SanitizeMol(newmol)
            rdk.Chem.MolToPDBFile(newmol, '{}_{}.pdb'.format(lig_name, outname))
            infile = open('{}_{}.pdb'.format(lig_name, outname), 'r')
            lines = infile.readlines()
            infile.close()
            newlines = [line.replace('UNL', lig_name) for line in lines]
            outfile = open('{}_{}.pdb'.format(lig_name, outname), 'w')
            outfile.writelines(newlines)
            outfile.close()

            # TO DO: Record invalid molecules
        if mol is None:
            print('Invalid molecule')
            mol = rdk.Chem.MolFromMol2File(ligand, sanitize=False)
            mol.SetProp("_Name", lig_name)
            mol.UpdatePropertyCache(strict=False)
            rdk.Chem.MolToPDBFile(mol, '{}_{}.pdb'.format(lig_name, outname))
            infile = open('{}_{}.pdb'.format(lig_name, outname), 'r')
            lines = infile.readlines()
            infile.close()
            newlines = [line.replace('UNL', lig_name) for line in lines]
            outfile = open('{}_{}.pdb'.format(lig_name, outname), 'w')
            outfile.writelines(newlines)
            outfile.close()

    #TO DO: return path_to_molecule

def merge_protein_ligand(protein, ligand):

    receptor_dock = mda.Universe(protein).select_atoms('all')
    ligand_dock = mda.Universe(ligand).select_atoms('all')

    # TO DO: rename ligand
    complex_dock = mda.Merge(ligand_dock, receptor_dock)
    complex_dock = complex_dock.select_atoms('all')

    return complex_dock

def align_proteins(reference, mobile):

    #here reference will is experimental structure and mobile the docked complex
    reference = mda.Universe(reference).select_atoms('all')
    mobile = mobile

    #print(len(mobile))
    # Rename histidine and remove alternative conformation to permit alignment
    for residue_reference in reference.residues:
        if residue_reference.resname in ['HIP', 'HIE', 'HID']:
            residue_reference.resname = 'HIS'

    for residue_mobile in mobile.residues:
        if residue_mobile.resname in ['HIP', 'HIE', 'HID']:
            residue_mobile.resname = 'HIS'

    # for atom_reference in reference.atoms:
    #     if atom_reference.altLoc == 'B':
    #         reference = reference - atom_reference
    #
    # for atom_mobile in mobile.atoms:
    #     if atom_mobile.altLoc == 'B':
    #         mobile = mobile - atom_mobile

    # mobile.write('mobile_initial.pdb')
    # reference.write('reference_initial.pdb')

    # #Creats alignment file
    alignment = align.sequence_alignment(mobile.select_atoms('protein and not altloc B'), reference.select_atoms('protein and not altloc B'))
    fasta = '>ref\n{}\n>modile\n{}'.format(alignment[0], alignment[1])
    file_fasta = open('alignemt.aln',"w+")
    file_fasta.write(fasta)
    file_fasta.close()

    # Collection residue numbers and align structures
    reference_resids = [a.resid for a in reference.select_atoms('protein').select_atoms('name CA and not altloc B')]
    mobile_resids = [a.resid for a in mobile.select_atoms('protein').select_atoms('name CA and not altloc B')]
    align_dict = align.fasta2select('alignemt.aln', is_aligned=True, ref_resids=reference_resids, target_resids=mobile_resids)

    #selection resulting from aign_dict not organized in the same way for the two files:
        #mobile N CA CB C O
        #reference: N CA C O CB

    #Just align on C-alphas
    new_reference_selection =  align_dict['reference'].replace('( backbone or name CB )', 'name CA')
    new_mobile_selection = align_dict['mobile'].replace('( backbone or name CB )', 'name CA');
    new_align_dict = {'mobile': new_mobile_selection, 'reference': new_reference_selection}

    align.alignto(mobile.select_atoms('not altloc B'), reference.select_atoms('not altloc B'), select=new_align_dict)
    #Make more precise alignment?
    # align.alignto(complex_dock, pdb_reference, select=align_dict, subselection='protein and around 5 resname LIG')
    #mobile.write('mobile_final.pdb')

    return mobile

def extract_ligand(complex, resname, outname):

        #Exclude hydrogens from selection to prevent valance issue when sanitizing molecules
        #ligand = complex.select_atoms('resname {} and not name H*'.format(resname))
        ligand = complex.select_atoms('resname {}'.format(resname))
        ligand.write('{}_{}.pdb'.format(resname, outname))

        infile = open('{}_{}.pdb'.format(resname, outname), 'r')
        lines = infile.readlines()
        infile.close()
        newlines = [line.replace('      SYST ', '           ') for line in lines]
        newlines2 = [line.replace('    B', '   BR') for line in newlines]
        outfile = open('{}_{}.pdb'.format(resname, outname), 'w')
        outfile.writelines(newlines2)
        outfile.close()

def RMSD(experimental, prediction):
    ref = io.loadmol(experimental)
    ref.strip()
    coords_ref = ref.coordinates
    anum_ref = ref.atomicnums
    adj_ref = ref.adjacency_matrix

    dock = io.loadmol(prediction)
    dock.strip()
    coords_dock = dock.coordinates
    anum_dock = dock.atomicnums
    adj_dock = dock.adjacency_matrix

    RMSD = rmsd.symmrmsd(
        coords_ref,
        coords_dock,
        anum_ref,
        anum_dock,
        adj_ref,
        adj_dock,
    )

    #print('RMSD is: ' + str(round(RMSD, 2)) + ' Ang')
    return RMSD

def RMSD_calculator(experimental_structure_pdb, docked_ligand, smile, dock_receptor_pdb):

    #creates temporary directory for various output files
    basedir = os.getcwd()
    os.mkdir('./temp')
    os.chdir('./temp')
    experimental_structure_pdb = '../' + experimental_structure_pdb
    docked_ligand = '../' + docked_ligand
    dock_receptor_pdb = '../' + dock_receptor_pdb

    #extract ligand name
    with open(experimental_structure_pdb, 'r') as pdb_text_file:
        for line in pdb_text_file:
            if line.startswith('HETNAM'):
                ligand_name = line[11:14]

    # dock ligand sdf/mol2 to pdb
    change_mol_format(docked_ligand, smile, ligand_name, 'raw')
    # merge dock receptor with dock ligand pdb
    complex_docked = merge_protein_ligand(dock_receptor_pdb, '{}_raw.pdb'.format(ligand_name))
    # Align predicted complex to experimental pdb
    align_proteins(experimental_structure_pdb, complex_docked)
    # extract aligned dock ligand
    extract_ligand(complex_docked, ligand_name, 'dock_aligned')
    # aligned dock ligand to sdf
    change_mol_format('{}_dock_aligned.pdb'.format(ligand_name), smile, ligand_name, 'dock_aligned')

    # extract experimental ligand
    # Needs to extract correct ligand for correct site: if multiple ligand picks the one with the nearest center of mass
    # To do - improve split function for multiple ligands
    reference = mda.Universe(experimental_structure_pdb)
    reference_ligand = reference.select_atoms('resname {}'.format(ligand_name))

    if len(set(reference_ligand.resids)) == 1:
        extract_ligand(reference, ligand_name, 'experimental')

    if len(set(reference_ligand.resids)) == 2:
        resids = list(set(reference_ligand.resids))

        site_dock = mda.Universe('{}_dock_aligned.pdb'.format(ligand_name)).select_atoms('all')
        site_dock_com =  site_dock.center_of_mass()

        reference_ligand_1 = reference_ligand.select_atoms('resid {}'.format(resids[0]))
        reference_ligand_1_com = reference_ligand_1.center_of_mass()
        dist_l1 = np.linalg.norm(site_dock_com - reference_ligand_1_com)

        reference_ligand_2 = reference_ligand.select_atoms('resid {}'.format(resids[1]))
        reference_ligand_2_com = reference_ligand_2.center_of_mass()
        dist_l2 = np.linalg.norm(site_dock_com - reference_ligand_2_com)

        if dist_l1 < dist_l2:
            extract_ligand(reference_ligand_1, ligand_name, 'experimental')

        if dist_l1 > dist_l2:
            extract_ligand(reference_ligand_2, ligand_name, 'experimental')

        # else:
        #     raise NameError('Zero or more than two ligands in PDB')

    # else:
    #     print('ERROR: zero or more than 2 ligands in the PDB file')

    # experimental ligand pdb to sdf
    change_mol_format('{}_experimental.pdb'.format(ligand_name), smile, ligand_name, 'experimental')

    #computes rmsd
    rmsd = RMSD('{}_experimental.pdb'.format(ligand_name), '{}_dock_aligned.pdb'.format(ligand_name))

    #returns to initial directory and delete temporary directory
    os.chdir(basedir)
    subprocess.call(["rm", "-r", './temp'])

    return rmsd

def RMSD_calculator_protein(reference, prediction, apo, distance_cutoff):

    #Get ligand name
    with open(reference, 'r') as pdb_text_file:
        for line in pdb_text_file:
            if line.startswith('HETNAM'):
                ligand_name = line[11:14]

    #The reference must be the experimental structure
    reference_univ = mda.Universe(reference).select_atoms('all')
    #Apo structure for resid renumbering of protein model + rmsd
    apo_univ = mda.Universe(apo).select_atoms('all')
    #The structure to calculate the RMSD against
    prediction_univ = mda.Universe(prediction).select_atoms('all')

    #Need to remove ligands outside of site-1 when multiple ligands are present
    ligand = reference_univ.select_atoms('resname {}'.format(ligand_name))
    if len(ligand.residues.resids) > 1:
        ligand_site_2_resid = reference_univ.select_atoms('resname {} and around 4 resid 1335'.format(ligand_name)).residues.resids[0]
        ligand_site_2 = reference_univ.select_atoms('resid {}'.format(ligand_site_2_resid))
        reference_univ = reference_univ - ligand_site_2

    selection_list = reference_univ.select_atoms('protein and (around {} resname {})'.format(distance_cutoff, ligand_name)).residues.resids
    selection_list = '(resid {} ) and not (name H* or name H) and not (altloc B)'.format(str(selection_list)[1:-1])

    #Align apo and model to experimental structure
    apo_aligned = align_proteins(reference, apo_univ)
    prediction_aligned = align_proteins(reference, prediction_univ)

    #renumbers model to match APO
    #Finds first Tyrosine and renumber prediction from it
    tyr_ref_resid = reference_univ.select_atoms('resname TYR').residues[0].resid
    tyr_pred_resid = prediction_aligned.select_atoms('resname TYR').residues[0].resid
    resid_start =  tyr_ref_resid - (tyr_pred_resid - prediction_aligned.select_atoms('protein').residues[0].resid)

    if tyr_ref_resid != tyr_pred_resid:
        for resnumber, prediction_residue in enumerate(prediction_aligned.select_atoms('protein').residues, resid_start):
            prediction_residue.resid = resnumber
    else:
        pass

    #subselect the residues around the binding site
    reference_aligned_binding_site = reference_univ.select_atoms(selection_list)
    apo_aligned_binding_site = apo_aligned.select_atoms(selection_list)

    prediction_aligned_binding_site = prediction_aligned.select_atoms(selection_list)

    #In some cases the atoms groups have a different order and lead to asymetrical lists and thus wrong rsmds
    #Use one list to align the other
    template_atom_group = list()
    apo_aligned_binding_site_new = apo_aligned.select_atoms('')
    prediction_aligned_binding_site_new = prediction_aligned.select_atoms('')

    for atom_reference in reference_aligned_binding_site:
        for atom_apo in apo_aligned_binding_site:
            if [atom_apo.name, atom_apo.type, atom_apo.resid, atom_apo.resname] == [atom_reference.name,
                                                                                    atom_reference.type,
                                                                                    atom_reference.resid,
                                                                                    atom_reference.resname]:
                apo_aligned_binding_site_new += atom_apo

        for atom_prediction in prediction_aligned_binding_site:
            if [atom_prediction.name, atom_prediction.type, atom_prediction.resid, atom_prediction.resname] == [atom_reference.name,
                                                                                                atom_reference.type,
                                                                                                atom_reference.resid,
                                                                                                atom_reference.resname]:
                prediction_aligned_binding_site_new += atom_prediction

    #experimental vs apo (measures induced fit)
    rmsd_ref_apo = rms.rmsd(reference_aligned_binding_site.positions,
                            apo_aligned_binding_site_new.positions)
    #experimental vs prediction (measures how fare out the prediction is from crystal)
    rmsd_ref_prediction = rms.rmsd(reference_aligned_binding_site.positions,
                                   prediction_aligned_binding_site_new.positions)
    #apo vs prediction (tell whether protein motion was modelled or rigid body fit)
    rmsd_apo_prediction = rms.rmsd(apo_aligned_binding_site_new.positions,
                                   prediction_aligned_binding_site_new.positions)



    return [float(rmsd_ref_apo), float(rmsd_ref_prediction), float(rmsd_apo_prediction)]

    #Must try RMSD with following files
    # ok prediction = '../Submissions-stage2/PHIP2_2_poses_souyakuchan/poses/PHIP2-F5-1.pdb'
    # ok prediction = '../Submissions-stage2/PHIP2_mms/poses/PHIP2-F5-1.pdb'
    # to do: prediction = '../Submissions-stage2/PHIP2_stage2_submission_Iorga_pose_prediction_1/PHIP2_stage2_submission_Iorga_pose_prediction_1/PHIP2-F5-1.pdb'


# ##Tests ligand
# reference = '../../experimental-data/stage-2/F11-PHIPA-x20023.pdb'
# lig_pred = '../Submissions-stage2/PHIP2_2_poses_ajlVvr5/poses/PHIP2-F11-1.sdf'
# prot_pred = '../Submissions-stage2/PHIP2_2_poses_ajlVvr5/poses/PHIP2-F11-1.pdb'
# smile = 'BrC1=CC=NC2=NC=CC=C21'
# rmsd = RMSD_calculator(reference, lig_pred, smile, prot_pred)
# print(rmsd)

# ##Tests protein with motion
# ligand_name = 'K2G'
# apo = '../../PHIPA_C2_Apo.pdb'
# exp = '../../experimental-data/stage-2/F126-PHIPA-x20651.pdb' #reference
# #Test protein with motion
# pred_1 = '../Submissions-stage2/PHIP2_mms/poses/PHIP2-F126-1.pdb'
# rmsds1 = RMSD_calculator_protein(exp, pred_1, apo, ligand_name, distance_cutoff=5)
# print(rmsds1)
# ##Test protein without motion
# pred_2 = '../Submissions-stage2/PHIP2_YU/poses/PHIP2-F126-1.pdb'
# rmsds2 = RMSD_calculator_protein(exp, pred_2, apo, ligand_name, distance_cutoff=5)
# print(rmsds2)