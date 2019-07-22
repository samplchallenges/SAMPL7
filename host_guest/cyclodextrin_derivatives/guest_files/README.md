# Guests for the SAMPL7 Cyclodextrin Derivatives Challenge

Provided are the SMILES strings for the two guests for this challenge, and then MOL2 (.mol2), PDB (.pdb) and SDF (.sdf) files generated from those SMILES strings are also provided here. Guests are trans-3-methylcyclohexanol and R-rimantadine hydrochloride, codenamed `g1` and `g2` respectively.


## What's here

- `cyclodextrin_guest_smiles.txt` : Textfile containing the isomeric SMILES strings and ids/codenames for the guests. Semicolon-delimited.
- `cyclodextrin_guest_names.txt` : names and ids for the guests. Semicolon-delimited.
- `g1.mol2`, `g2.mol2` : Sybyl mol2 files for the guests, as provided by Katy Kellett on May 15, 2019.
- `guest_input_maker.ipynb`: The jupyter notebook used to generate the PDB and SDF files for each guest using OpenEye toolkits and the SMILES strings and codenames found in `cyclodextrin_guest_smiles.txt`. The PDB and SDF files were generated on July 18, 2019.
