## Manifest

- [`macrostate_analysis/`](macrostate_analysis/) - This directory contains analysis outputs of pK<sub>a</sub> predictions. See the more detailed [README](macrostate_analysis/README.md) for details.
- [`microstate_analysis/`](microstate_analysis/) - This directory contains analysis outputs of relative microstate free energy submissions. See the more detailed [README](microstate_analysis/README.md) for details.
- [`relative_microstate_free_energy_predictions/`](relative_microstate_free_energy_predictions/) - Contains participant relative microstate free energy submissions. These files were used to carry out the macrostate analysis. Some of these files have updated method names and/or updated values compared to those found in the originals folder. This folder contains a subfolder which holds original submissions, some of which had errors and needed to be updated after the challenge deadline. Submissions had their submitted names changed to be more descriptive in analysis graphs.
  - submissions that had overall sign errors corrected (in the microstate_analysis/analysis.py script): `pKa-VA-2-charge-correction`, `pka-nhlbi-1c` , `pKa_RodriguezPaluch_SMD_1`, `pKa_RodriguezPaluch_SMD_2` , `pKa_RodriguezPaluch_SMD_3`
  - submissions that were converted to kcal/mol (in the microstate_analysis/analysis.py script): `pKa-ECRISM-1`, `pKa-VA-2-charge-correction` , `pKa_RodriguezPaluch_SMD_1`, `pKa_RodriguezPaluch_SMD_2`, `pKa_RodriguezPaluch_SMD_3`, `pka-nhlbi-1c`
  - submission with manually corrected dM value: `pKa-VA-2-charge-correction`
