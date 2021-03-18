## SAMPL7 log *D* Predictions

Ranked SAMPL7 pK<sub>a</sub> and log *P* predictions were combined to estimate log *D*<sub>7.4</sub>. The Mathematica notebook used to do this analysis is available in the manifest.

General analysis of log *D* predictions include calculated vs predicted log *D* correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

## Manifest
- [`calculate_logD/`](./calculate_logD/)
  - `calc_logD.nb` - Wolfram Mathematica `.nb` file that calculates and exports SAMPL7 distribution coefficients log *D*<sub>7.4</sub> for participants that had submitted a ranked log *P* and a ranked pK<sub>a</sub> submission. The notebook gathers the predicted macroscopic acidity constants and the partition coefficients from [`pKa_submission_collection.csv`](../pKa/analysis/macrostate_analysis/analysis_outputs_ranked_submissions/pKa_submission_collection.csv) and [`logP_submission_collection.csv`](../logP/analysis/analysis_outputs_ranked_submissions/logP_submission_collection.csv), respectively. The log *D*<sub>7.4</sub> is then calculated under the assumption that the ionic species can not enter the organic phase [1]. Because the acidity constants listed in [`pKa_submission_collection.csv`](../pKa/analysis/macrostate_analysis/analysis_outputs_ranked_submissions/pKa_submission_collection.csv) do not contain information about the charge states of the protonated and deprotonated species, the consensus of models that had submitted macroscopic pK<sub>a</sub> values including the charge states was used to determine that eq. 4 should be used for all compounds. Notebook created by Nicolas Tielker.
  - `logD_submission_collection.csv` - Contains analysis of log *D*<sub>7.4</sub> predictions generated from log *P* and pK<sub>a</sub> predictions.
  - logD_predictions/ - Contains SAMPL style submission files created from the log *D* data found in `logD_submission_collection.csv`. One reference method and one null method were added to this folder to be used as a comparison to other methods in the general SAMPL analysis. These submission style files were used as input to the general SAMPL analysis script (`logD_analysis.py`) and the output can be found in `analysis_outputs_all_submissions/` and `analysis_outputs_ranked_submissions/`.
- [`logD_analysis.py`](logD_analysis.py) - Python script that parses submissions and performs the analysis. Provides two separate treatment for ranked blind predictions alone (output directory: [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/)) and ranked and reference calculations together (output directory: [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/)). Reference calculations are provided as reference/comparison methods.  logD_analysis.py
- [`logD_analysis2.py`](logD_analysis2.py) - Python script that performs the analysis of molecular statistics (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
- [`logD_experimental_values.csv`](logD_experimental_values.csv) -  A CSV (`.csv`) table of potentiometric and shake-flask log *D* measurements of the 22 SAMPL molecules.
- [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) - This directory contain analysis outputs of ranked submissions only.
    - `error_for_each_logD.pdf` - Violin plots that show error distribution of predictions related to each experimental log *P*.
    - `logDCorrelationPlots/` - This directory contains plots of predicted vs. experimental log *P* values with linear regression line (blue) for each method. Files are named according to the submitted method name of each subission, which can be found in `statistics_table.csv`. In correlation plots, the dashed black line has a slope of 1. Dark and light green shaded areas indicate +-0.5 and +-1.0 log *P* unit error regions, respectively.
    - `logDCorrelationPlotsWithSEM/` - This directory contains similar plots to the `logDCorrelationPlots/` directory with error bars added for Standard Error of the Mean (SEM) of experimental and predicted values for submissions that reported these values. Experimental log *P* SEM values are either too small to be able to see the horizontal error bars, or some of the experimental log *P* SEM values were not collected.
    - `AbsoluteErrorPlots/` - This directory contains a bar plot for each method showing the absolute error for each log *P* prediction compared to the experimental value.
    - `StatisticsTables/` - This directory contains machine-readable copies of the Statistics Table, bootstrap distributions of performance statistics, and overall performance comparison plots based on RMSE and MAE values.
        - `statistics.csv`- A table of performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), Kendall's Tau, and error slope(ES)) for all the submissions.
        - `RMSE_vs_method_plot.pdf`
        - `RMSE_vs_method_plot_colored_by_method_category.pdf`
        - `RMSE_vs_method_plot_for_Physical_MM_category.pdf`
        - `RMSE_vs_method_plot_for_Physical_QM_category.pdf`
        - `RMSE_vs_method_plot_for_Empirical_category.pdf`
        - `RMSE_vs_method_plot_for_Mixed_category.pdf`
        - `RMSE_vs_method_plot_physical_methoods_colored_by_method_category.pdf`
        - `MAE_vs_method_plot.pdf`
        - `MAE_vs_method_plot_colored_by_method_category.pdf`
        - `MAE_vs_method_plot_for_Physical_MM_category.pdf`
        - `MAE_vs_method_plot_for_Physical_QM_category.pdf`
        - `MAE_vs_method_plot_for_Empirical_category.pdf`
        - `MAE_vs_method_plot_for_Mixed_category.pdf`
        - `kendalls_tau_vs_method_plot.pdf`
        - `MAE_vs_method_plot_physical_methoods_colored_by_method_category.pdf`
        - `kendalls_tau_vs_method_plot_colored_by_method_category.pdf`
        - `kendalls_tau_vs_method_plot_for_Physical_MM_category.pdf`
        - `kendalls_tau_vs_method_plot_for_Physical_QM_category.pdf`
        - `kendalls_tau_vs_method_plot_for_Empirical_category.pdf`
        - `kendalls_tau_vs_method_plot_for_Mixed_category.pdf`
        - `kendall_tau_vs_method_plot_physical_methoods_colored_by_method_category.pdf`
        - `Rsquared_vs_method_plot.pdf`                            
        - `Rsquared_vs_method_plot_colored_by_method_category.pdf`                 
        - `Rsquared_vs_method_plot_colored_by_type.pdf`
        - `Rsquared_vs_method_plot_for_Empirical_category.pdf`
        - `Rsquared_vs_method_plot_for_Mixed_category.pdf`
        - `Rsquared_vs_method_plot_for_Physical_MM_category.pdf`
        - `Rsquared_vs_method_plot_for_Physical_QM_category.pdf`
        - `Rsquared_vs_method_plot_physical_methoods_colored_by_method_category.pdf`
        - `statistics_bootstrap_distributions.pdf` - Violin plots showing bootstrap distributions of performance statistics of each method. Each method is labelled according to the method name of the submission.

    - `QQPlots/` - Quantile-Quantile plots for the analysis of model uncertainty predictions.
    - `MolecularStatisticsTables/` - This directory contains tables and barplots of molecular statistics analysis (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
        - `MAE_vs_molecule_ID_plot.pdf` - Barplot of MAE calculated for each molecule averaging over all prediction methods.
        - `RMSE_vs_molecule_ID_plot.pdf` - Barplot of RMSE calculated for each molecule averaged over all prediction methods
        - `molecular_error_statistics.csv` - MAE and RMSE statistics calculated for each molecule averaged over all prediction methods. 95% confidence intervals were calculated via bootstrapping (10000 samples).
        - `molecular_MAE_comparison_between_method_categories.pdf` - Barplot of MAE calculated for each method category for each molecule averaging over all predictions in that method category. The colors of the bars indicate method categories.
        - `molecular_error_distribution_ridge_plot_all_methods.pdf`: Error distribution of each molecule, based on predictions from all ranked methods.
        - `molecular_error_distribution_ridge_plot_well_performing_methods.pdf`: Error distribution of each molecule based on predictions from only methods who are determined as consistently well-performing methods.
        - `Empirical/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in the Empirical method category.
        - `Physical_MM/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in the Physical MM method category.
        - `Physical_QM/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in the Physical QM method category.

- [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/) - Duplicates the [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) directory, but reference calculations. Also includes the additional plots:
    - `StatisticsTables/MAE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by MAE, with reference calculations colored differently.
    - `StatisticsTables/RMSE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by RMSE, with reference calculations colored differently.


## References
[1] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.
