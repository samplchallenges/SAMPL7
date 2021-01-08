# Analysis of macro pK<sub>a</sub>'s

Submitted relative free energies were converted to macro pK<sub>a</sub> predictions and analyzed here.

Participants submitted relative free energies between microstates.
As a consistency check, two methods are implemented in the [pKa_analysis.py](pKa_analysis.py) code to convert participant submissions to macro pK<sub>a</sub>'s. One method is the delta G method given by Junjun Mao (Levich Institute, City College of New York), and the other is a titration method given by David Mobley which follows the [Selwa et al](https://link.springer.com/article/10.1007/s10822-018-0138-6) SAMPL6 work from JCAMD 2018. The Selwa approach was used in the analysis here. In cases where there is more than one macro pK<sub>a</sub> estimated, the calculated macro pK<sub>a</sub> values are related to experiment using the 0 to -1 transition.

General analysis of pK<sub>a</sub> predictions include calculated vs predicted pK<sub>a</sub> correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported.

Molecular statistics analysis was performed to indicate which molecules were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

## Manifest
- [`pKa_analysis.py`](pKa_analysis.py) - Python script that parses submissions and performs the analysis. Provides two separate treatment for ranked blind predictions alone (output directory: [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/)) and blind ranked and non-ranked predictions together with reference calculations (output directory: [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/)). Reference calculations are not formally part of the challenge but are provided as reference/comparison methods.
- [`pKa_analysis2.py`](pKa_analysis2.py) - Python script that performs the analysis of molecular statistics (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
- [`pKa_experimental_values.csv`](pKa_experimental_values.csv) -  CSV table of potentiometric and shake-flask pK<sub>a</sub> measurements of 22 molecules and their SMILES.
- [`SAMPL7-user-map-pKa.csv`](SAMPL7-user-map-pKa.csv) - User map of all submissions.
- [`get_usermap.py`](get_usermap.py) - Python script used to create the user map.
- [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) - This directory contain analysis outputs of ranked submissions only.
    - `error_for_each_pKa.pdf` - Violin plots that show error distribution of predictions related to each experimental pK<sub>a</sub>.
    - `pKaCorrelationPlots/` - This directory contains plots of predicted vs. experimental pK<sub>a</sub> values with linear regression line (blue) for each method. Files are named according to the submitted method name of each subission, which can be found in `statistics_table.csv`. In correlation plots, the dashed black line has a slope of 1. Dark and light green shaded areas indicate +-0.5 and +-1.0 pK<sub>a</sub> unit error regions, respectively.
    - `pKaCorrelationPlotsWithSEM/` - This directory contains similar plots to the `pKaCorrelationPlots/` directory with error bars added for Standard Error of the Mean (SEM) of experimental and predicted values for submissions that reported these values. Some experimental pK<sub>a</sub> SEM values are  too small to be able to see the horizontal error bars.
    - `AbsoluteErrorPlots/` - This directory contains a bar plot for each method showing the absolute error for each pK<sub>a</sub> prediction compared to the experimental value.
    - `StatisticsTables/` - This directory contains machine-readable copies of the Statistics Table, bootstrap distributions of performance statistics, and overall performance comparison plots based on RMSE and MAE values.
        - `statistics.csv`- A table of performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), Kendall's Tau, and error slope(ES)) for all the submissions.
        - `RMSE_vs_method_plot.pdf`
        - `RMSE_vs_method_plot_colored_by_method_category.pdf`
        - `RMSE_vs_method_plot_colored_by_type.pdf`
        - `MAE_vs_method_plot.pdf`
        - `MAE_vs_method_plot_colored_by_method_category.pdf`
        - `MAE_vs_method_plot_colored_by_type.pdf`
        - `kendalls_tau_vs_method_plot.pdf`
        - `kendalls_tau_vs_method_plot_colored_by_method_category.pdf`
        - `kendalls_tau_vs_method_plot_colored_by_type.pdf`
        - `Rsquared_vs_method_plot.pdf`
        - `Rsquared_vs_method_plot_colored_by_method_category.pdf`
        - `Rsquared_vs_method_plot_colored_by_type.pdf`
        - `RMSE_vs_method_plot_for_QM_category.pdf`
        - `MAE_vs_method_plot_for_QM_category.pdf`
        - `kendalls_tau_vs_method_plot_for_QM_category.pdf`
        - `Rsquared_vs_method_plot_for_QM_category.pdf`
        - `RMSE_vs_method_plot_for_QM_LEC_category.pdf`
        - `MAE_vs_method_plot_for_QM_LEC_category.pdf`
        - `kendalls_tau_vs_method_plot_for_QM_LEC_category.pdf`
        - `Rsquared_vs_method_plot_for_QM_LEC_category.pdf`
        - `RMSE_vs_method_plot_for_QSPR_ML_category.pdf`
        - `MAE_vs_method_plot_for_QSPR_ML_category.pdf`
        - `kendalls_tau_vs_method_plot_for_QSPR_ML_category.pdf`
        - `Rsquared_vs_method_plot_for_QSPR_ML_category.pdf`
        - `RMSE_vs_method_plot_QM_and_QMLEC_methods_colored_by_method_category.pdf`
        - `RMSE_vs_method_plot_QM_and_QMLEC_methods_colored_by_type.pdf`
        - `MAE_vs_method_plot_QM_and_QMLEC_methods_colored_by_method_category.pdf`
        - `MAE_vs_method_plot_QM_and_QMLEC_methods_colored_by_type.pdf`
        - `kendall_tau_vs_method_plot_QM_and_QMLEC_methods_colored_by_method_category.pdf`
        - `kendall_tau_vs_method_plot_QM_and_QMLEC_methods_colored_by_type.pdf`
        - `Rsquared_vs_method_plot_QM_and_QMLEC_methods_colored_by_method_category.pdf`
        - `Rsquared_vs_method_plot_QM_and_QMLEC_methods_colored_by_type.pdf`
        - `statistics_bootstrap_distributions.pdf` - Violin plots showing bootstrap distributions of performance statistics of each method. Each method is labelled according to the method name of the submission.

    - `QQPlots/` - Quantile-Quantile plots for the analysis of model uncertainty predictions.
    - `MolecularStatisticsTables/` - This directory contains tables and barplots of molecular statistics analysis (Error statistics, MAE and RMSE, calculated across methods for each molecule.)
        - `MAE_vs_molecule_ID_plot.pdf` - Barplot of MAE calculated for each molecule averaging over all prediction methods.
        - `RMSE_vs_molecule_ID_plot.pdf` - Barplot of RMSE calculated for each molecule averaged over all prediction methods
        - `molecular_error_statistics.csv` - MAE and RMSE statistics calculated for each molecule averaged over all prediction methods. 95% confidence intervals were calculated via bootstrapping (10000 samples).
        - `molecular_MAE_comparison_between_method_categories.pdf` - Barplot of MAE calculated for each method category for each molecule averaging over all predictions in that method category. The colors of the bars indicate method categories.
        - `molecular_error_distribution_ridge_plot_all_methods.pdf`: Error distribution of each molecule, based on predictions from all ranked methods.
        - `molecular_error_distribution_ridge_plot_well_performing_methods.pdf`: Error distribution of each molecule based on predictions from only methods who are determined as consistently well-performing methods.
        - `QM/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in the Empirical method category.
        - `QM_LEC/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in the Physical MM method category.
        - `QSPR_ML/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in the Physical QM method category.

- [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/) - Duplicates the [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) directory, but also includes all non-ranked submissions and reference calculations. Also includes the additional plots:
    - `StatisticsTables/MAE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by MAE, with reference calculations colored differently.
    - `StatisticsTables/RMSE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by RMSE, with reference calculations colored differently.
