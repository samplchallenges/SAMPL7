## pKa Microstates of SAMPL7 Molecules

24 small molecules are assigned moleculed IDs in the form of SMXX from SM25 to SM46. This directory includes their enumerated microstates.

Please note, the microstate lists provided here may not be comprehensive.

### Manifest
- `SMXX_microstates.csv` - Files include updated microstate IDs and canonical SMILES of each microstate. The first microstate in each CSV file indicated by `SMXX_000` is the neutral reference state.
- [`get_states.ipynb`](get_states.ipynb) - Notebook used to generated tautomers and protomers of the molecules. Note, additional microstates were enumerated outside of this notebook by Chemicilaize (Chemaxon) and Epik (Schrodinger), and added to the `SMXX_microstates.csv` files here.  
- [`SAMPL7_molecule_ID_and_SMILES.csv`](SAMPL7_molecule_ID_and_SMILES.csv) - A `.CSV` file that indicates SAMPL7 pKa challenge molecule IDs and canonical isomeric SMILES.
