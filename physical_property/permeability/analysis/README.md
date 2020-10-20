# Analysis of log*P*app predictions

General analysis of log*P*app predictions include calculated vs predicted log*P*app correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

## Manifest
- [`logP_analysis.py`](logP_analysis.py) - Python script that parses submissions and performs the analysis. Provides two separate treatment for ranked blind predictions alone (output directory: [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/)) and blind ranked and non-ranked predictions together (output directory: [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/)).
- [`logP_analysis2.py`](logP_analysis2.py) - Python script that performs the analysis of molecular statistics (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
- [`logP_predictions/`](logP_predictions/) - This directory includes SAMPL7 logP submission files.
- [`logP_experimental_values.csv`](logP_experimental_values.csv) -  CSV table of PAMPA log*P*app measurements of 22 molecules and their SMILES.
- [`SAMPL7-user-map-permeability.csv`](SAMPL7-user-map-permeability.csv) - User map of all submissions.
- [`get_usermap.py`](get_usermap.py) - Python script to create the user map.
- [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/) - This directory contain analysis outputs of ranked and non-ranked submissions.
    - `error_for_each_logPapp.pdf` - Violin plots that show error distribution of predictions related to each experimental log*P*app.
    - `logPappCorrelationPlots/` - This directory contains plots of predicted vs. experimental log*P*app values with linear regression line (blue) for each method. Files are named according to the method name of each submission, which can be found in `statistics_table.csv`. In correlation plots, the dashed black line has a slope of 1. Dark and light green shaded areas indicate +-0.5 and +-1.0 log*P*app unit error regions, respectively.
    - `logPappCorrelationPlotsWithSEM/` - This directory contains similar plots to the `logPCorrelationPlots/` directory with error bars added for Standard Error of the Mean (SEM) of experimental and predicted values for submissions that reported these values. Experimental log*P*app SEM values were not collected.
    - `AbsoluteErrorPlots/` - This directory contains a bar plot for each method showing the absolute error for each log*P*app prediction compared to the experimental value.
    - `StatisticsTables/` - This directory contains machine-readable copies of Statistics Table, bootstrap distributions of performance statistics, and overall performance comparison plots based on RMSE and MAE values.
        - `statistics.csv`- A table of performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), Kendall's Tau, and error slope(ES)) for all the submissions.
        - `RMSE_vs_method_plot.pdf`
        - `MAE_vs_method_plot.pdf`
        - `kendalls_tau_vs_method_plot.pdf`
        - `Rsquared_vs_method_plot.pdf`                            
        - `statistics_bootstrap_distributions.pdf` - Violin plots showing bootstrap distributions of performance statistics of each method. Each method is labelled according to the method name of each submission.
    - `MolecularStatisticsTables/` - This directory contains tables and barplots of molecular statistics analysis (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
        - `MAE_vs_molecule_ID_plot.pdf` - Barplot of MAE calculated for each molecule averaging over all prediction methods.
        - `RMSE_vs_molecule_ID_plot.pdf` - Barplot of RMSE calculated for each molecule averaged over all prediction methods
        - `molecular_error_statistics.csv` - MAE and RMSE statistics calculated for each molecule averaged over all prediction methods. 95% confidence intervals were calculated via bootstrapping (10000 samples).
        - `molecular_error_distribution_ridge_plot_all_methods.pdf`: Error distribution of each molecule, based on predictions from all ranked methods.

- [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) - Duplicates the [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/) directory, but contain analysis outputs of ranked submissions only.
