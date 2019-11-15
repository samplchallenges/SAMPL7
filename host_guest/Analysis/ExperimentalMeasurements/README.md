## Manifest

- `experimental_measurements.pdf`: Summary table of the experimental data after conversion
- `experimental_measurements.csv`: Summary table of the experimental data after conversion, in `.csv` format
- `experimental_measurements.json`: Summary table of the experimental data after conversion,  in JSON format.
- `SAMPL7_Isaacs_data.pdf`: Data provided by the Isaacs group. Updated 10/25/19 with n values from fit. Also provided in original docx version.
- `SAMPL7_Gibb_data.pdf`: Data provided by Bruce Gibb and group 10/29/19, updated by David Mobley 11/12/19 to correct a renumbering of compounds which had occurred (changes checked by Gibb). Also provided in docx version.
- `SAMPL7_Gilson_data.xlsx` and `.pdf`: ITC binding data from the Gilson lab provided Nov. 2019, originally named `Sample_ITC_complex.xlsx`. Edited by D. Mobley Nov. 14, 2019, to add a TDeltaS column rather than just DeltaS for better consistency with the other datasets. Exported individual sheets (for rimantadine and trans-4-methylcyclohexanol) to PDF format, `SAMPL7_Gilson_data_rimantadine.pdf` and `SAMPL7_Gilson_data_methylcyclohexanol.pdf`.
- `SAMPL7_Gilson_NOESY_data.docx` and `.pdf`: Analysis of NOESY data on binding modes from Gilson lab, originally provided as `NOESY NMR data for SAMPL.docx` by the Gilson lab, Nov. 2019. Also available in PDF format.
- `generate_tables.py`: Script used to perform error propagation and create the experimental_measurements.X files based on the data provided by the Isaacs (and, later, Gilson and Gibb) groups. Adapted from [the SAMPL6 `generate_tables.py`](https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by Andrea Rizzi.

Experimental conditions/details for these cases are available in the above provided files, the [host guest challenge desription](https://github.com/samplchallenges/SAMPL7/blob/master/host_guest_description.md) (especially for the Gilson CD data), the [Isaacs' clip README](https://github.com/samplchallenges/SAMPL7/blob/master/host_guest/Isaacs_clip/README.md), and the [GDCC README](https://github.com/samplchallenges/SAMPL7/blob/master/host_guest/GDCC_and_guests/README.md). Note that host/guest concentrations in the cyclodextrin derivatives case are actually provided in the [ITC results file](SAMPL7_Gilson_data.xlsx).

Raw ITC/NOESY data for the Gilson lab's CD work will also be provided here via link shortly.

## Notes on error propagation

Currently, for Isaacs' clip system, we are utilizing uncertainties provided by Lyle Isaacs, which provide ITC-based uncertainties, along with additional error propagation to handle uncertainties in titrant concentrations, as was done for SAMPL6. The GDCC data utilizes provided uncertainties, as detailed in the `SAMPL7_Gibb_data.pdf`, as these already reflected concentration uncertainty.
