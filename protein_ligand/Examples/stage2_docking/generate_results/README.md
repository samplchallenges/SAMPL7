Here, I used the 5enh.pdb structure, aligned it to PHIPA_C_Apo.pdb with PyMol, saved, then manually extracted the protein and the ligand separately, then fed these into the OEDocking.ipynb notebook to generate predicted poses (using 5enh; initial efforts had trouble getting the PHIPA_C2_Apo structure to work with OEDocking). This is meant just to provide a temporary example.

## Manifest

- `poses`: Generated poses
- `poses/PHIP2_2_OE_reference_description.txt`: Description file, based on the template, describing what was done here. Would be uploaded with the .tar.gz of `poses` to the submission system.
- `OEDocking.ipynb`: Example jupyter notebook generating example submissions
- `5enh.pdb`: 5ENH PDB structure; has ligand in same site as S1. Used in construction of example submission here.
- `5enh_aligned.pdb`: Same as just prior, but aligned to correct reference frame
- `5enh_protein.pdb`: Protein, manually extracted from `5enh_aligned.pdb`; used for docking to generate test submission.
- `5enh_ligand.pdb`: Ligand, manually extracted from `5enh_aligned.pdb`, used to identify binding site area for docking.
