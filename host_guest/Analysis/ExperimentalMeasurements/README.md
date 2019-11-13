## Manifest

- `experimental_measurements.pdf`: Summary table of the experimental data after conversion
- `experimental_measurements.csv`: Summary table of the experimental data after conversion, in `.csv` format
- `experimental_measurements.json`: Summary table of the experimental data after conversion,  in JSON format.
- `SAMPL7_Isaacs_data.pdf`: Data provided by the Isaacs group. Updated 10/25/19 with n values from fit. Also provided in original docx version.
- `SAMPL7_Gibb_data.pdf`: Data provided by Bruce Gibb and group 10/29/19, updated by David Mobley 11/12/19 to correct a renumbering of compounds which had occurred. Also provided in docx version.
- `generate_tables.py`: Script used to perform error propagation and create the experimental_measurements.X files based on the data provided by the Isaacs (and, later, Gilson and Gibb) groups. Adapted from [the SAMPL6 `generate_tables.py`](https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by Andrea Rizzi.


## Notes on error propagation

Currently we are utilizing uncertainties provided by Lyle Isaacs, which provide ITC-based uncertainties, along with additional error propagation to handle uncertainties in titrant concentrations, as was done for SAMPL6.
