## SAMPL7 log *P* Prediction Challenge

The SAMPL7 log *P* Challenge consists of predicting the octanol-water partition coefficients of 22 molecules. Our aim is to evaluate how well current models can capture the transfer free energy of small molecules between different solvent environments through blind predictions. Challenge participants will be asked to predict the difference in free energy for the neutral form between water and octanol. This challenge is *optional* and will be run at the same time as the pK<sub>a</sub> and permeability challenge (both of which are also optional).  

Tripos MOL2 and SDF files for the molecules can be found [here](../pKa/microstates) and are indicated by the ID tag `SMXX_micro000`.

Instructions for the pKa challenge: [`logP_challenge_instructions.md`](logP_challenge_instructions.md)

Submission template for the pKa challenge: [`submission_template/logP_prediction_template.csv`](submission_template/logP_prediction_template.csv)

Experimental log *P* measurements will made available after the challenge deadline.

## Manifest
 - [`molecule_ID_and_SMILES.csv`](molecule_ID_and_SMILES.csv) - A `.CSV` file that contains SAMPL7 log *P* challenge molecule IDs and isomeric SMILES. These were selected from the enumerated microstates from the pK<sub>a</sub> challenge.
 - [`submission_template/TFE_prediction_template.csv`](submission_template/logP_prediction_template.csv) - An empty prediction submission template file.
 - [`example_submission_file/TFE-DanielleBergazinExampleFile-1.csv`](example_submission_file/logP-DanielleBergazinExampleFile-1.csv) - An example submission file filled with random values to illustrate expected format.
- [`logP_challenge_instructions.md`](logP_challenge_instructions.md) - Instructions for the pKa challenge.
