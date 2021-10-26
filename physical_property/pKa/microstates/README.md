## pK<sub>a</sub> Microstates of SAMPL7 Molecules

22 small molecules are assigned moleculed IDs in the form of `SMXX` from SM25 to SM46. This directory includes their enumerated microstates.

Also provided are the microstates in Tripos MOL2 (`.mol2`) and SDF (`.sdf`) file format.

Please note, the microstate lists provided here may not be comprehensive.

### Manifest
- `SMXX_microstates.csv` - Files include updated microstate IDs and canonical SMILES of each microstate. The first microstate in each CSV file indicated by `SMXX_micro000` is our selected neutral reference state.
- [`get_states.ipynb`](get_states.ipynb) - Notebook used to generate tautomers and protomers of the molecules. Note, additional microstates were enumerated outside of this notebook by Chemicilaize (Chemaxon) and Epik (Schrodinger), and added to the `SMXX_microstates.csv` files here.
- [`make_mol2_sdf_files.ipynb`](make_mol2_sdf_files.ipynb) - The jupyter notebook used to generate the MOL2 and SDF files for each microstate using OpenEye toolkits and the SMILES strings and codenames found in the `SMXX_microstates.csv` files. A random stereoisomer was chosen for microstates `SM25_micro000`, `SM25_micro002`, `SM25_micro003`, `SM28_micro003`, `SM42_micro000`, and `SM43_micro000` when generating MOL2 and SDF files.
- [`SAMPL7_molecule_ID_and_SMILES.csv`](SAMPL7_molecule_ID_and_SMILES.csv) - A `.CSV` file that indicates SAMPL7 pK<sub>a</sub> challenge molecule IDs and canonical isomeric SMILES.
