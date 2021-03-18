## SAMPL7 log *D* Predictions

Placeholder

## Manifest
- [`analysis/`](analysis/) - Contains analysis of log *D*<sub>7.4</sub> predictions generated from log *P* and pK<sub>a</sub> predictions.
- [`calc_logD.nb`](calc_logD.nb) - Wolfram Mathematica `.nb` file that calculates and exports SAMPL7 distribution coefficients log *D*<sub>7.4</sub> for participants that had submitted a ranked log *P* and a ranked pK<sub>a</sub> submission. The notebook gathers the predicted macroscopic acidity constants and the partition coefficients from [`pKa_submission_collection.csv`](../pKa/analysis/macrostate_analysis/analysis_outputs_ranked_submissions/pKa_submission_collection.csv) and [`logP_submission_collection.csv`](../logP/analysis/analysis_outputs_ranked_submissions/logP_submission_collection.csv), respectively. The log *D*<sub>7.4</sub> is then calculated under the assumption that the ionic species can not enter the organic phase [1]. Because the acidity constants listed in [`pKa_submission_collection.csv`](../pKa/analysis/macrostate_analysis/analysis_outputs_ranked_submissions/pKa_submission_collection.csv) do not contain information about the charge states of the protonated and deprotonated species, the consensus of models that had submitted macroscopic pK<sub>a</sub> values including the charge states was used to determine that eq. 4 should be used for all compounds.

## References
[1] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.