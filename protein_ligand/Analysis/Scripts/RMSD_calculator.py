#!/usr/bin/env python
__author__ = "Shuai Liu"
__email__ = "shuailiu25@gmail.com"

import shutil
import glob
import pickle
import logging
import sys
import os
import time
import subprocess
import argparse

def mcs(ref_mol, fit_mol):
    #do the mcs search and return OEMatch object.
    #ignore Hydrogen
    OESuppressHydrogens(fit_mol)
    OESuppressHydrogens(ref_mol)
    #set atom and bond expression
    atomexpr = OEExprOpts_AtomicNumber
    bondexpr = 0
    #do the mcs search, using defined atom, bond expression options
    mcss = OEMCSSearch( ref_mol, atomexpr, bondexpr, True)
    mcss.SetMCSFunc(OEMCSMaxAtomsCompleteCycles(1.5) )
    #create a new match object to store mcs search info.
    new_match_list = []
    new_match_dic  = {}
    i = 0
    j = 0
    for match1 in mcss.Match(ref_mol):
        i += 1
        #write out match1 molecule
        mol1 = OEGraphMol()
        OESubsetMol(mol1,match1, True)
        ofs1 = oemolostream("match1_%s.pdb"%i)
        OEWriteMolecule(ofs1, mol1)
        ofs1.close()
        for match2 in mcss.Match(fit_mol):
            j += 1
            check_list = []
            #write out match2 molecule
            new_match = OEMatch()
            mol2 = OEGraphMol()
            OESubsetMol(mol2,match2, True)
            ofs2 = oemolostream("match2_%s.pdb"%j)
            OEWriteMolecule(ofs2, mol2)
            ofs2.close()
            for mp1, mp2 in zip(match1.GetAtoms(), match2.GetAtoms()):
                ref_name = mp1.target.GetName().strip()
                fit_name = mp2.target.GetName().strip()
                new_match.AddPair (mp1.target, mp2.target)
            #store the match info
            new_match_list.append(new_match)
            new_match_dic[new_match] = (["match1_%s_vs_match2_%s"%(i,j), check_list ])
    return new_match_dic

def rmsd_mcss(ref_struc, fit_struc):
    #This function use the openeye mcss calculation to get the atom mapping first and then calculate RMSD, if multiple atom mapping is avaiable, the lowest RMSM will be returned

    print('we are now in the rmsd_mcss', ref_struc, fit_struc)
    reffs = oemolistream()
    reffs.open(ref_struc)
    fitfs = oemolistream()
    fitfs.open(fit_struc)
    refmol = OEGraphMol()
    OEReadMolecule(reffs, refmol)
    for fitmol in fitfs.GetOEGraphMols():
        #get all possible matching
        ss = mcs(refmol, fitmol,)
        mcss_rmsd_list = []
        match_info = []
        for mcss in ss.keys():
            #calculate the RMSD based on atom mapping
            mcss_rmsd = OERMSD(refmol, fitmol, mcss)
            mcss_rmsd_list.append(mcss_rmsd)
            match_info.append(ss[mcss])

    print( ref_struc)
    print( fit_struc)
    print(mcss_rmsd_list)

    try:
        minimum_mcss = min(mcss_rmsd_list)
        return minimum_mcss
    except:
        return False

def wait_and_check (filename, timestep = 100, how_many_times = 1000):
    #add some relaxing time
    count = 0
    while (count < how_many_times):
        if not os.path.isfile(filename):
            time.sleep(timestep)
            print('Inside the wait loop check the current wait time',filename,count,count*timestep)
            count = count + 1
        else:
            print('we are now exiting at this count:',filename,count)
            return True
    return False

def extract_ligand_from_complex (complex_pdb_file, ligand_pdb_file, ligand_info = "UNL"):
    #here the default ligand info is the residue name OpenEye assigns for unknown ligands, UNL.

    print('we are now entering extract ligand from complex', complex_pdb_file, ligand_pdb_file)
    complex_file = open(complex_pdb_file, "r")
    complex_lines = complex_file.readlines()
    complex_file.close()
    ligid = ligand_info.split("-")
    ligand_lines = []
    for complex_line in complex_lines:
        if (complex_line[17:20].strip()==ligid[0] and complex_line[22:26].strip()==ligid[1]):
            ligand_lines.append(complex_line)
    ligand_file = open(ligand_pdb_file, "w")
    ligand_file.writelines(ligand_lines)
    ligand_file.close()


def convert_ligand_format (input_ligand, output_ligand):
    print('We are now converting the ligand format:', input_ligand, output_ligand)
    try:
        mol = OEMol()
        ifile = oemolistream(input_ligand)
        OEReadMolecule(ifile, mol)
        ifile.close()
    except:
        logging.info(f"This ligand '{input_ligand}' cannot be read; check the format" )
        return False

    try:
        ofile = oemolostream(output_ligand)
        OEWriteMolecule(ofile, mol)
    except:
        logging.info(f"This ligand '{input_ligand}' cannot be written to '{output_ligand}'; please check format and the validity of the molecule." )
        return False

    return True


def merge_two_pdb (receptor, ligand, complex_pdb):
    print('we need to merge two pdbs:',receptor, ligand, complex_pdb)

    #subprocess.getoutput("babel -ipdb %s -opdb %s"%(receptor, receptor) )
    #subprocess.getoutput("babel -ipdb %s -opdb %s"%(ligand, ligand) )

    folder = os.getcwd()
    #---need to add this to fix corrupted REMARK sections in participant PDB files
    complex_lines = []

    f1 = open(receptor, "r")

    protein_lines = f1.readlines()
    f1.close()

    for p_line in protein_lines:
        if p_line [:6] not in ["CONECT", "ENDMDL" ] and p_line [:3] not in ["END"]:
            complex_lines.append(p_line)
    complex_lines.append("TER   \n")
    f2 = open(ligand, "r")
    ligand_lines = f2.readlines()
    f2.close()
    for l_line in ligand_lines:
        if l_line [:6] not in ["REMARK", "MODEL ", "CONECT", "ENDMDL"] and l_line not in ["END"]:
            complex_lines.append(l_line)
    f3 = open(complex_pdb, "w")
    f3.writelines(complex_lines)
    f3.close()


def align_protein (template_complex, input_complex, output_complex):
    #use schrodinger binding site alignment to get the aligned structure
    print('we are attempting the following alignment:',template_complex, input_complex, output_complex)
    return subprocess.getoutput("$SCHRODINGER/utilities/align_binding_sites %s %s -o %s"%(template_complex, input_complex, output_complex))

def rmsd_calculation(input_ligand, template_ligand, input_protein, template_protein_complex, realignment = False ):
    #print(input_ligand)
    #print(template_ligand)
    #print(input_protein)
    #quit()
    input_ligand_title, input_ligand_extension = os.path.splitext(input_ligand)
    template_ligand_title, template_ligand_extension = os.path.splitext(template_ligand)
    if realignment:
        ###do the realignment first###
        #step 1: combine ligand and protein
        input_ligand_pdb = input_ligand_title + "_ligand.pdb"
        try:
        #step 2: convert mol file into pdb format
            convert_ligand_format(input_ligand, input_ligand_pdb)
            logging.info("Successfully convert %s to %s..."%(input_ligand, input_ligand_pdb))
        except:
            logging.info("\tFatal Error: This ligand %s cannot be convert to pdb format"%(input_ligand))
            return "N/A"
        input_ligand_protein_complex = input_ligand_title + "_complex.pdb"
        #step 3: merge the ligand and receptor together
        merge_two_pdb (input_protein, input_ligand_pdb, input_ligand_protein_complex)
        aligned_ligand_protein_complex = input_ligand_title + "_vs_" + template_ligand_title+ "_complex_aligned.pdb"
        #step 4: align the input complex onto template complex
        try:
            align_protein (template_protein_complex, input_ligand_protein_complex, aligned_ligand_protein_complex )
            #set a relaxing time to let the alignment finish
            #default to check every 5 second and maximum calculation time is 500 second
            time_check_frequence = 100
            how_many_check_point = 1000
            total_wait_time = time_check_frequence * how_many_check_point
            if wait_and_check(aligned_ligand_protein_complex, timestep = time_check_frequence, how_many_times = how_many_check_point):
                logging.info("Successfully align %s onto %s and get the aligned structure %s"%(input_ligand_protein_complex, template_protein_complex, aligned_ligand_protein_complex))
            else:
                logging.info("The alignment from %s onto %s didn't finish in %s second... Need to break"%(input_ligand_protein_complex, template_protein_complex, total_wait_time))
                return "N/A"
        except:
            logging.info("\tFatal Error: Cannot align %s onto %s"%(input_ligand_protein_complex, template_protein_complex))
            return "N/A"
        #step 5: split the aligned protein to get aligned ligand
        aligned_input_ligand = input_ligand_title + "_vs_" + template_ligand_title + "_ligand_aligned.pdb"
        try:
            extract_ligand_from_complex(aligned_ligand_protein_complex, aligned_input_ligand, ligand_info = "UNL")
            logging.info("Successfully extract ligand file %s from aligned complex %s"%(aligned_input_ligand, aligned_ligand_protein_complex))
        except:
            logging.info("\tFatal Error: Cannot extract ligand file %s from aligned complex %s"%(aligned_input_ligand, aligned_ligand_protein_complex))
            return "N/A"
        #step 6: calculate the RMSD between the aligned ligand and the template ligand
        try:
            print('step 6:', template_ligand, aligned_input_ligand)
            rmsd = rmsd_mcss(template_ligand, aligned_input_ligand)
            logging.info("Successfully calculate the rmsd between template ligand %s and input aligned ligand %s, get the rmsd = %s"%(template_ligand, aligned_input_ligand, rmsd))

        except:
            logging.info("\tFatal Error: Cannont get the rmsd between template ligand %s and input aligned ligand %s"%(template_ligand, aligned_input_ligand))
            rmsd = "N/A"
        #step 7: write out result to a log file
        out_log = open("%s_vs_%s_aligned.log"%(input_ligand_title, template_ligand_title), "w")
        out_log.writelines("rmsd: %s"%rmsd)
        out_log.close()
    else:
        #calculate the ligand RMSD without realignment
        try:
            rmsd = rmsd_mcss(template_ligand, input_ligand)
            logging.info("Successfully calculate the rmsd between template ligand %s and input ligand %s, get the rmsd = %s"%(template_ligand, input_ligand, rmsd))
        except:
            logging.info("\tFatal Error: Cannont get the rmsd between template ligand %s and input ligand %s"%(template_ligand, input_ligand))
            rmsd = "N/A"
        out_log = open("%s_vs_%s.log"%(input_ligand_title,template_ligand_title), "w")
        out_log.writelines("rmsd: %s"%rmsd)
        out_log.close()
    return rmsd

def copy_template(template_folder_path, submitted_folder_path):
    all_template_files = glob.glob("%s/*"%(template_folder_path))
    for template_file in all_template_files:
        shutil.copy(template_file, submitted_folder_path)

def main_rmsd (submitted_folder_path, template_folder_path, realigned = True):
    #inside the submission folder, search for all submitted mol files and extract the corresponding temaplte file from the template folder and calculate the rmsd
    copy_template (template_folder_path, submitted_folder_path)
    os.chdir(submitted_folder_path)
    if realigned:
        out_rmsd_csv = open("Overall_rmsd_realigned.csv", "w")
    else:
        out_rmsd_csv = open("Overall_rmsd.csv", "w")
    all_rmsd_data = ["%-20s,%-20s,%-20s\n"%("Submitted_Ligand", "Template_Ligand", "RMSD")]
    for input_ligand in glob.glob("*.mol"):
        #example mol file format: 3OOF-FXR_13-2.mol
        print('we are looping through:', input_ligand)
        ligand_ID = input_ligand.split("-")[1]
        input_ligand_title = os.path.splitext(input_ligand)[0]
        input_protein = input_ligand_title + ".pdb"
        template_ligand_suffix = "_ligand1.pdb"
        template_protein_suffix = ".pdb"
        all_template_ligands = glob.glob("%s-*%s"%(ligand_ID, template_ligand_suffix))
        #print(ligand_ID)
        #print(input_ligand_title)
        #print(input_protein)
        #print(template_ligand_suffix)
        #print(all_template_ligands)

        for template_ligand in all_template_ligands:
            template_protein_complex = template_ligand.split(template_ligand_suffix)[0] + template_protein_suffix
            #here apply the rmsd_calculation
            this_rmsd = rmsd_calculation(input_ligand, template_ligand, input_protein, template_protein_complex, realignment = realigned )
            new_data = "%-20s,%-20s,%-20s\n"%(input_ligand, template_ligand, this_rmsd)
            all_rmsd_data.append(new_data)

        for file in os.listdir("."):
            if os.path.isfile(file) and "match" in file:
                try:
                    os.remove(file)
                    print('we have succesfully removed:',file)
                except:
                    print('cannot remove file:', file)
                    print()

    out_rmsd_csv.writelines(all_rmsd_data)
    #clean up atom mapping files
    all_mapping_files = glob.glob("match*")
    for mapping_file in all_mapping_files:
        os.remove(mapping_file)


if ("__main__") == (__name__):
    from argparse import ArgumentParser
    desc = """
    This code was design to evaluate the pose prediction of D3R Grand Challenge 2
    For more infomation about the challenge, please visit https://drugdesigndata.org/

    ######Usage exmaple######
    ### Use the alignment option to realign the submitted structure onto the crystal position###
    ### Here the answer file under folder template_at_crystal_position should be used ###
    # python RMSD_calculator.py --submitdir ./example_submission_folder --templatedir ./template_at_crystal_position --alignment

    ### Directly calculate the RMSDs between submitted structure with the template ligand ###
    ### Here the answer file under folder template_at_APO_position should be used ###
    # python RMSD_calculator.py --submitdir ./example_submission_folder --templatedir ./template_at_APO_position

    #Note for FXR system, we notice that using the alignment option will get a slightly lower RMSDs, so our reported RMSDs are RMSDs with the alignment method.
    #########################

    ######Output#######
    ### Overall_rmsd_realigned.csv/Overall_rmsd.csv (depend on usage the alignment option)
    ### Output files are under example_submission_folder
    ###################

    ######Dependencies######
    #openeye oechem tools for RMSD calculation
    #schrodinger tools for alignment if use the alignment option
    ########################
    """
    help_formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=desc,
                            formatter_class=help_formatter)
    parser.add_argument("-s", "--submitdir", metavar="PATH",
                      help="PATH where we could find the submission files")

    parser.add_argument("-t", "--templatedir", metavar="PATH",
                      help="PATH where we could find the template ligand and proetin")
    parser.add_argument("-a", "--alignment", action="store_true",
                      help="Realign submitted structures onto the template structure before calculating the RMSD")
    parser.add_argument("-l", "--logfilename", default= "rmsd_calculation.log", metavar="FILENAME",
                      help="Log file name")
    opt = parser.parse_args()
    try:
        from openeye.oechem import *
    except ImportError:
        sys.stderr.write('\nERROR: Unable to import openeye.oechem: '
                        'from openeye.oechem import *\n\n')
    submitDir = opt.submitdir
    tempDir = opt.templatedir
    logfilename = opt.logfilename
    realignment_option = opt.alignment
    logger = logging.getLogger()
    logging.basicConfig( format  = '%(asctime)s: %(message)s', datefmt = '%m/%d/%y %I:%M:%S', filename = logfilename, filemode = 'w', level   = logging.INFO )
    main_rmsd (submitDir, tempDir , realigned = realignment_option)
