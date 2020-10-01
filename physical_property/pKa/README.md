# SAMPL7 pK<sub>a</sub> Prediction Challenge

The SAMPL7 pK<sub>a</sub> Challenge consists of predicting relative free energies between microstates to determine the pK<sub>a</sub> of 22 molecules. Free energies were chosen rather than pK<sub>a</sub> values given the recent work of [Gunner et al.](https://link.springer.com/content/pdf/10.1007/s10822-020-00280-7.pdf). All possible tautomers of each ionization (charge) state are defined as distinct protonation microstates. Our aim is to evaluate how well current pK<sub>a</sub> prediction methods perform with these 22 molecules through blind predictions. Challenge participants are asked to predict free energy differences between microstates. Challenge organizers have a reference microstate for each compound, and all free energies must be predicted relative to this reference state, as detailed in the challenge instructions linked below. This challenge is *optional* and will be run at the same time as the log *P* and permeability challenge (both of which are also optional).  

Instructions for the pK<sub>a</sub> challenge: [`pKa_challenge_instructions.md`](pKa_challenge_instructions.md)

Submission template for the pK<sub>a</sub> challenge: [`submission_template/pKa_prediction_template.csv`](submission_template/pKa_prediction_template.csv)


Experimental pK<sub>a</sub> measurements will made available after the challenge deadline.

## Manifest
- [`microstates/`](microstates/) - This directory contains `.CSV` files that list microstate IDs and canonical isomeric SMILES of microstates. Files are separated by molecule ID. Updated microstates and their microstate IDs can be found in `SMXX_microstates.csv` files.
- [`submission_template/pKa_prediction_template.csv`](submission_template/pKa_prediction_template.csv) - An empty prediction submission template file.
- [`example_submission_file/pKa-DanielleBergazinExampleFile-1.csv`](example_submission_file/pKa-DanielleBergazinExampleFile-1.csv) - An example submission file filled with random values to illustrate expected format.
- [`pKa_challenge_instructions.md`](pKa_challenge_instructions.md) - Instructions for the pK<sub>a</sub> challenge.
- [`transition_networks/`](transition_networks/) - This directory contains transition networks of the challenge molecules in `.PDF` and `.PPTX` format.
