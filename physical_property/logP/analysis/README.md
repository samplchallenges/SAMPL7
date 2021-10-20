# Analysis of log *P* predictions

General analysis of log *P* predictions include calculated vs predicted log *P* correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

## Manifest
- [`logP_analysis.py`](logP_analysis.py) - Python script that parses submissions and performs the analysis. Provides two separate treatment for ranked blind predictions alone (output directory: [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/)) and blind ranked and non-ranked predictions together with reference calculations (output directory: [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/)). Reference calculations are not formally part of the challenge but are provided as reference/comparison methods.
- [`logP_analysis2.py`](logP_analysis2.py) - Python script that performs the analysis of molecular statistics (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
- [`logP_predictions/`](logP_predictions/) - This directory includes SAMPL7 logP submission files. Submission "logp-nhlbi-1.csv" (method name: TFE-NHLBI-TZVP-QM) had a sign error in all of the predictions that was fixed (all signs were flipped) on 4/9/2021. Submission "logP-MLRUCR-1.csv" (method name: TFE MLR) had incorrect SEM values listed, these were also updated on 4/9/2021.
- [`logP_experimental_values.csv`](logP_experimental_values.csv) -  CSV table of potentiometric and shake-flask log *P* measurements of 22 molecules and their SMILES.
- [`SAMPL7-user-map-logP.csv`](SAMPL7-user-map-logP.csv) - User map of all submissions.
- [`get_usermap.py`](get_usermap.py) - Python script used to create the user map.
- [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) - This directory contains analysis outputs of ranked submissions only. Please note, analysis was rerun/updated on 4/9/2021 after errors in two submissions were fixed (TFE-NHLBI-TZVP-QM had sign errors and TFE MLR had incorrect SEM values).
    - `error_for_each_logP.pdf` - Violin plots that show error distribution of predictions related to each experimental log *P*.
    - `logPCorrelationPlots/` - This directory contains plots of predicted vs. experimental log *P* values with linear regression line (blue) for each method. Files are named according to the submitted method name of each subission, which can be found in `statistics_table.csv`. In correlation plots, the dashed black line has a slope of 1. Dark and light green shaded areas indicate +-0.5 and +-1.0 log *P* unit error regions, respectively.
    - `logPCorrelationPlotsWithSEM/` - This directory contains similar plots to the `logPCorrelationPlots/` directory with error bars added for Standard Error of the Mean (SEM) of experimental and predicted values for submissions that reported these values. Experimental log *P* SEM values are either too small to be able to see the horizontal error bars, or some of the experimental log *P* SEM values were not collected.
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

- [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/) - Duplicates the [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) directory, but also includes all non-ranked submissions and reference calculations. Please note, analysis was rerun/updated on 4/9/2021 after errors in two submissions were fixed (TFE-NHLBI-TZVP-QM had sign errors and TFE MLR had incorrect SEM values). Also includes the additional plots:
    - `StatisticsTables/MAE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by MAE, with reference calculations colored differently.
    - `StatisticsTables/RMSE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by RMSE, with reference calculations colored differently.
- [`original_analysis/`](original_analysis/) - Contains (archived) original analysis of log *P* predictions and participant submissions, prior to 2021-10-20 updates to Ballatore lab experimental data for some compounds.
