#!/bin/env python

"""Quick Python script to process guest file names in the GDCC and Isaacs cases and generate IUPAC names for the compounds."""

from openeye.oechem import *
from openeye.oeiupac import *
import os

# Parameters for processing
dirnames = [ '../GDCC_and_guests', '../Isaacs_clip' ]
prefixes = [ 'GDCC', 'trimertrip' ]
guestdir = 'guest_files'
text_file_suffix = '_guest_smiles.txt'
output_file_suffix = '_guest_names.txt'

# Loop over directories and process SMILES to get IUPAC names
for (idx, dirname) in enumerate(dirnames):
    print('\n'+dirname+'\n')
    # Generate input and output file names
    inputfilename = os.path.join( dirname, guestdir, prefixes[idx]+text_file_suffix)
    outputfilename = os.path.join( dirname, guestdir, prefixes[idx]+output_file_suffix)

    # Process input file:
    infile = open(inputfilename, 'r')
    outfile = open(outputfilename, 'w')
    for line in infile.readlines():
        # Semicolon delimited, so split at semicolons
        tmp = line.split(';')

        # Generate molecule from isomeric SMILES
        mol = OEMol()
        ism = tmp[0]
        OEParseSmiles(mol, ism)

        # Create IUPAC name
        name = OECreateIUPACName(mol)
        print("   Created IUPAC name %s for %s..." % (name, tmp[1]))

        # Dump to output file
        outfile.write('%s;%s' % (name, tmp[1]))

    infile.close()
    outfile.close()


