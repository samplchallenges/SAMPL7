## SAMPL7 PAMPA Permeability Prediction Challenge

The SAMPL7 PAMPA Permeability Challenge consists of predicting the permeabilities of 22 molecules. This challenge is *optional* and will be run at the same time as the pK<sub>a</sub> and partition coefficient challenge (both of which are also optional).

Provided is a `.CSV` file containing IDs and SMILES strings for each molecule in the form of SMXX from SM25 to SM46. The enumerated microstates for each molecule and the `.MOL2` and `.SDF` files for each microstate can be found [here](physical_property/pKa/microstates/).

Instructions for the permeability challenge: [`permeability_challenge_instructions.md`](permeability_challenge_instructions.md)

Submission template for the permeability challenge: [`submission_template/permeability_prediction_template.csv`](submission_template/permeability_prediction_template.csv)

Please note that permeabilities for compounds `SM33`, `SM35`, and `SM39` were *not* determined.

Experimental permeability data will made available after the challenge deadline.

## Manifest
- [`SAMPL7_molecule_ID_and_SMILES.csv`](SAMPL7_molecule_ID_and_SMILES.csv) - A `.CSV` file containing SMILES strings. Additionally, the pK<sub>a</sub> challenge has [enumerated microstates for each molecule](../pKa/microstates/).
- [`submission_template/permeability_prediction_template.csv`](submission_template/permeability_prediction_template.csv) - An empty prediction submission template file.
- [`example_submission_file/permeability-DanielleBergazinExampleFile-1.csv`](example_submission_file/permeability-DanielleBergazinExampleFile-1.csv) - An example submission file filled with random values to illustrate expected format.
- [`permeability_challenge_instructions.md`](permeability_challenge_instructions.md) - Instructions for permeability challenge.
