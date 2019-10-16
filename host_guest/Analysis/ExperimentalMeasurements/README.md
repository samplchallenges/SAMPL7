## Manifest

- `experimental_measurements.pdf`: Summary table of the experimental data after conversion
- `experimental_measurements.csv`: Summary table of the experimental data after conversion, in `.csv` format
- `experimental_measurements.json`: Summary table of the experimental data after conversion,  in JSON format.
- `SAMPL6_Isaacs_data.pdf`: Data provided by the Isaacs group.
- `generate_tables.py`: Script used to perform error propagation and create the experimental_measurements.X files based on the data provided by the Isaacs (and, later, Gilson and Gibb) groups. Adapted from [the SAMPL6 `generate_tables.py`](https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by Andrea Rizzi.


## Notes on error propagation

Currently we are utilizing uncertainties provided by Lyle Isaacs, which provide ITC-based uncertainties, along with additional error propagation to handle uncertainties in titrant concentrations, as was done for SAMPL6.
