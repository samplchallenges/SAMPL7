
Participants submitted relative free energies between microstates and were analyzed here. Analysis includes the average relative microstate free energy for each microstate, the  distributions of microstate transition free energies relative to the reference state (based on predictions from all methods), and the distributions of microstate transition free energies relative to the reference state (based on predictions from all methods).

## Manifest
- [`get_usermap.py`](get_usermap.py) - Python script used to create the user map.
- [`micro_analysis.py`](micro_analysis.py) - Python script that parses submissions and performs the analysis.
- [`plots/`](plots/) - This directory contain analysis outputs of relative microstate free energy submissions.
  - [`relative_microstate_FE_submissions.csv`](plots/relative_microstate_FE_submissions.csv) - A `.CSV` table containing the `method name`, `file name`, `reference state`, `ID tag`, `total charge`, `relative microstate free energy prediction`, `Relative microstate free energy SEM`, and `model uncertainty` of each submitted microstate.
  - [`numbers.csv`](plots/numbers.csv) - A `.CSV` table containing the `ID tag`, `prediction count`, `average free energy prediction`, `min prediction`, `max prediction`, `prediction STD` and `average SEM`.
  - [`barplot_average_FE_predictions.pdf`](plots/barplot_average_FE_predictions.pdf) - average relative microstate free energy for each microstate.
  - [`ridgeplot_all_FE_predictions.pdf`](plots/ridgeplot_all_FE_predictions.pdf) - Ridge plot that shows the  distributions of microstate transition free energies relative to the reference state, based on predictions from all methods.
  - [`violinplot_all_FE_predictions.pdf`](plots/violinplot_all_FE_predictions.pdf) - Violin plot that shows the  distributions of microstate transition free energies relative to the reference state, based on predictions from all methods.
  - [`submissions/`](submissions/) - Participant submissions. These are the same as the submission files found in [relative_microstate_free_energy_predictions](../relative_microstate_free_energy_predictions/), except the reference state and microstate sections in the files were switched for quick use in the microstate analysis found here.
    - submissions that had overall sign errors corrected (in the micro_analysis.py script): `pKa-VA-2-charge-correction`, `pka-nhlbi-1c` , `pKa_RodriguezPaluch_SMD_1`, `pKa_RodriguezPaluch_SMD_2` , `pKa_RodriguezPaluch_SMD_3`
    - submissions that were converted to kcal/mol (in the micro_analysis.py script): `pKa-ECRISM-1`, `pKa-VA-2-charge-correction` , `pKa_RodriguezPaluch_SMD_1`, `pKa_RodriguezPaluch_SMD_2`, `pKa_RodriguezPaluch_SMD_3`, `pka-nhlbi-1c`
    - submission with manually corrected dM value: `pKa-VA-2-charge-correction`
