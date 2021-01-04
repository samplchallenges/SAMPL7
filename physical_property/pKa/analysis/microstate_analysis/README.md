## Manifest
- [`get_usermap.py`](get_usermap.py) - Python script used to create the user map.
- [`micro_analysis.py`](micro_analysis.py) - Python script that parses submissions and performs the analysis.
- [`plots/`](plots/) - This directory contain analysis outputs of relative microstate free energy submissions.
  - [`relative_microstate_FE_submissions.csv`](plots/relative_microstate_FE_submissions.csv) - A `.CSV` table containing the `method name`, `file name`, `reference state`, `ID tag`, `total charge`, `relative microstate free energy prediction`, `Relative microstate free energy SEM`, and `model uncertainty` of each submitted microstate.
  - [`numbers.csv`](plots/numbers.csv) - A `.CSV` table containing the `ID tag`, `prediction count`, `average free energy prediction`, `min prediction`, `max prediction`, `prediction STD` and `average SEM`.
  - [`barplot_average_FE_predictions.pdf`](plots/barplot_average_FE_predictions.pdf) - average relative microstate free energy for each microstate.
  - [`ridgeplot_all_FE_predictions.pdf`](plots/ridgeplot_all_FE_predictions.pdf) - Ridge plot that shows the  distributions of microstate transition free energies relative to the reference state, based on predictions from all methods.
  - [`violinplot_all_FE_predictions.pdf`](plots/violinplot_all_FE_predictions.pdf) - Violin plot that shows the  distributions of microstate transition free energies relative to the reference state, based on predictions from all methods.
- [`submissions/`](submissions/) - Participant submissions.
