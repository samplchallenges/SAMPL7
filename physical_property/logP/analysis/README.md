# Analysis of log *P* predictions with reassigned method categories

General analysis of log *P* predictions include calculated vs predicted log *P* correlation plots and 6 performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), and error slope(ES)) for all the submissions.
95%-percentile bootstrap confidence intervals of all the statistics were reported. Error slope (ES) statistic is calculated as the slope of the line fit the the QQ plot of model uncertainty predictions.

Molecular statistics analysis was performed to indicate logP values of which molecules of SAMPL7 logP Challenge set were more difficult to predict accurately across submitted methods. Error statistics (MAE and RMSE) were calculated for each molecule averaging across all methods or for all methods within a method category.

## Manifest
- [`logP_analysis.py`](logP_analysis.py) - Python script that parses submissions and performs the analysis. Provides two separate treatment for ranked blind predictions alone (output directory: [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/)) and blind ranked and non-ranked predictions together with reference calculations (output directory: [`analysis_outputs_all_submissions/`](analysis_outputs_all_submissions/)). Reference calculations are not formally part of the challenge but are provided as reference/comparison methods.

- [`logP_analysis2.py`](logP_analysis2.py) - Python script that performs the analysis of molecular statistics (Error statistics, MAE and RMSE, calculated across methods for each molecule.)

- [`logP_predictions/`](logP_predictions/) - This directory includes SAMPL7 logP submission files. Also includes submission IDs assigned to each submission.

- `logP_experimental_values.csv` -  CSV table of potentiomentric and shake-flask log *P* measurements of 22 molecules and their SMILES.

- `SAMPL7-user-map-logP.csv` - User map of all submissions.

- `SAMPL7-logP-method-map.csv` - Method map of all submissions.

- [`analysis_outputs_ranked_submissions/`](analysis_outputs_ranked_submissions/) - This directory contain analysis outputs of ranked submissions only.
  - `error_for_each_logP.pdf` - Violin plots that show error distribution of predictions related to each experimental log *P*.
  - `logPCorrelationPlots/` - This directory contains plots of predicted vs. experimental log *P* values with linear regression line (blue) for each method. Files are named by submission ID of each method, which can be found in `statistics_table.pdf`. In correlation plots, dashed black line has slope of 1. Dark and light green shaded areas indicate +-0.5 and +-1.0 log *P* unit error regions, respectively.
  - `logPCorrelationPlotsWithSEM/` - This directory contains similar plots to the `logPCorrelationPlots/` directory with error bars added for Standard Error of the Mean(SEM) of experimental and predicted values for submissions that reported these values. Experimental log *P* SEM values are either to small to be able to see the horizontal error bars, or some of the experimental log *P* SEM values were not collected.
  - `AbsoluteErrorPlots/` - This directory contains a bar plot for each method showing the absolute error for each log *P* prediction compared to experimental value.
  - `StatisticsTables/` - This directory contains machine readable copies of Statistics Table, bootstrap distributions of performance statistics, and overall performance comparison plots based on RMSE and MAE values.
      - `statistics.pdf` - A table of performance statistics (RMSE, MAE, ME, R^2, linear regression slope(m), Kendall's Tau, and error slope(ES)) for all the submissions.
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
      - `statistics_bootstrap_distributions.pdf` - Violin plots showing bootstrap distributions of performance statistics of each method. Each method is labelled by submission ID.

  - `QQPlots/` - Quantile-Quantile plots for the analysis of model uncertainty predictions.

  - `MolecularStatisticsTables/` - This directory contains tables and barplots of molecular statistics analysis (Error statistics, MAE and RMSE, calculated across methods for each molecule.)

    - `MAE_vs_molecule_ID_plot.pdf` - Barplot of MAE calculated for each molecule averaging over all prediction methods.

    - `RMSE_vs_molecule_ID_plot.pdf` - Barplot of RMSE calculated for each molecule averaging over all prediction methods.

    - `molecular_error_statistics.csv` - MAE and RMSE statistics calculated for each molecule averaging over all prediction methods. 95% confidence intervals were calculated via bootstrapping (10000 samples).

    - `molecular_MAE_comparison_between_method_categories.pdf` - Barplot of MAE calculated for each method category for each molecule averaging over all predictions in that method category. Colors of bars indicate method categories.

    - `molecular_error_distribution_ridge_plot_all_methods.pdf`: Error distribution of each molecule, based on predictions from all ranked methods.

    - `molecular_error_distribution_ridge_plot_well_performing_methods.pdf`: Error distribution of each molecules based on predictions from only methods who are determined as consistently well-performing methods (submission IDs: `4K631`, `006AC`, `43M66`, `5W956`, `847L9`, `HC032`, `7RS67`, `D4406`).

    - `Empirical/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in Empirical method category.

    - `Physical_MM/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in Physical MM method category.

    - `Physical_QM/` - This directory contains table and barplots of molecular statistics analysis calculated only for methods in Physical QM method category.

- `analysis_outputs_all_submissions/` - Duplicates the `analysis_outputs_ranked_submissions` directory, but also includes all non-ranked submissions and reference calculations (not formal submissions). Also includes the additional plots:
    - `StatisticsTables/MAE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by MAE, with reference calculations colored differently.
    - `StatisticsTables/RMSE_vs_method_plot_colored_by_type.pdf`: Barplot showing overall performance by RMSE, with reference calculations colored differently.


  ## Submission IDs for log *P* prediction methods

 SAMPL7 log *P* challenge blind submissions were listed in the ascending order of RMSE.

| Submission ID | Method Name |  Category    |
|---------------|-------------|--------------|
| 4K631	| ClassicalGSG	| Empirical	|
| 5W956	| TFE-prediction-method-MLR	| Empirical	|
| 847L9	| ClassicalGSG	| Empirical	|
| HC032	| Chemprop	| Empirical	|
| 006AC	| TFE-SM8-vacuum-opt	| Physical (QM)	|
| 0A608	| GROVER	| Empirical	|
| 02F1F	| ClassicalGSG	| Empirical	|
| 00EDA	| ffsampled_deeplearning_cl1	| Empirical	|
| 43M66	| ClassicalGSG	| Empirical	|
| 0680E	| TFE-prediction-Attentive FP	| Empirical	|
| 096BB	| ffsampled_deeplearning_cl2	| Empirical	|
| 02BF8	| TFE-SM12-vacuum-opt	| Physical (QM)	|
| 7RS67	| TFE-SM8-solvent-opt	| Physical (QM)	|
| REF00	| ChemAxon	| Empirical	|
| 0357F	| TFE-prediction-method-IEFPCM/MST	| Physical (QM)	|
| D4406	| TFE-MD-neat-octanol	| Physical (MM)	|
| NULL0	| mean clogP of FDA approved oral drugs (1998-2017)	| Empirical	|
| F46P0	| NES-1	| Physical (MM)	|
| C4A03	| NES-1	| Physical (MM)	|
| 063A2	| COSMO-RS	| Physical (QM)	|
| 07B59	| NES-1	| Physical (MM)	|
| 043B8	| SAMPL7_logP_MDPOW_GAFF	| Physical (MM)	|
| 065C7	| TFE-MD-wet-octanol	| Physical (MM)	|
| 0T68C	| SAMPL7_logP_MDPOW_CGenFF	| Physical (MM)	|
| 047D4	| EC_RISM_wet	| Physical (QM)	|
| 0A274	| TFE-SMD-vacuum-opt	| Physical (QM)	|
| 08F3F	| MD-EE-MCC (GAFF-TIP4P-Ew)	| Physical (MM)	|
| 08DA5	| TFE-prediction-solvation-b3lypd3	| Physical (QM)	|
| 0B909	| SAMPL7_logP_MDPOW_OPLS-AA	| Physical (MM)
| 6Q594	| SAMPL7_logP_MDPOW_LigParGen	| Physical (MM)	|
| 085FC	| TFE-SMD-solvent-opt	| Physical (QM)	|
| 0636A	| TFE-NHLBI-TZVP-QM	| Physical (QM)	|
| 2DF02	| Ensemble prediction of TFE	| Empirical	|
| 004AF	| Ensemble prediction of TFE	| Empirical	|
| 09F0E	| RayLogP三_QSPR_Mordred2D_TPOT-AutoML	| Empirical	|
| 03F9F	| TFE-NHLBI-NN-IN	| Empirical	|


 ## Submission IDs for reference log *P* prediction methods

Reference calculations are not formally part of the challenge but are provided as reference/comparison methods.
Reference calculations have submission IDs of the format REF##.
A null prediction is created which predicts all logPs as the mean clogP of FDA approved oral drugs (1998-2017) with submission ID NULL0.

SAMPL7 log *P* challenge reference submissions were listed in the ascending order of RMSE.

| Submission ID | Method Name |  Category    |
|---------------|-------------|--------------|
| REF00	| ChemAxon	| Empirical	|
| NULL0	| mean clogP of FDA approved oral drugs (1998-2017)	| Empirical	|
