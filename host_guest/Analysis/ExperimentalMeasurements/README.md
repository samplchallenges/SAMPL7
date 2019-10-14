## Manifest

- `experimental_measurements.pdf`: Summary table of the experimental data after conversion
- `experimental_measurements.csv`: Summary table of the experimental data after conversion, in `.csv` format
- `experimental_measurements.json`: Summary table of the experimental data after conversion,  in JSON format.
- `SAMPL6_Isaacs_data.pdf`: Data provided by the Isaacs group.
- `generate_tables.py`: Script used to perform error propagation and create the experimental_measurements.X files based on the data provided by the Isaacs (and, later, Gilson and Gibb) groups. Adapted from [the SAMPL6 `generate_tables.py`](https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py) by Andrea Rizzi.


## Notes on error propagation

Currently we are utilizing uncertainties provided by Lyle Isaacs rather than doing error propagation as in [SAMPL6](https://github.com/samplchallenges/SAMPL6/tree/master/host_guest/Analysis/ExperimentalMeasurements) but this may change as data from the other challenge components becomes available and we obtain more information on experimental protocols. So you can expect that the provided experimental uncertainties may be updated at a later date.
