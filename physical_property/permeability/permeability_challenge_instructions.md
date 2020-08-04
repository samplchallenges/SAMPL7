## PAMPA permeability Challenge Instructions

A submission template file can be found in the [`submission_template/`](submission_template/) directory and an example submission file can be found in [`submission_template/`](example_submission_file/).


For each molecule, we are asking participants to predict the log<sub>P<sub>app</sub></sub>, but we also have access to effective permeability and membrane retention values. If you are interested in those, please email us.


- Fill one [`submission_template/permeability_prediction_template.csv`](submission_template/permeability_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method.

- You may report only 1 log<sub>P<sub>app</sub></sub> value for each molecule per method.

- It is mandatory to submit predictions for all 22 molecules. Incomplete submissions will not be accepted.

- Report log<sub>P<sub>app</sub></sub> values to two decimal places (e.g. 3.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [1,9]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Name:`, `Software:`, `Category:`, and `Method:`, as illustrated in the example files. An example submission files can be found [`here`]['example_submission_file/permeability-DanielleBergazinExampleFile-1.csv'] to illustrate expected format when filling submission templates.

- For Method Category section please state if your prediction method can be better classified as an empirical modeling method, physical quantum mechanics (QM) modeling method, physical molecular mechanics (MM) modeling method, or mixed (both empirical and physical), using the category labels `Empirical`, `Physical (MM)`, `Physical (QM)`, or `Mixed`. Empirical models are prediction methods that are trained on experimental data, such as QSPR, machine learning models, artificial neural networks etc. Physical models are prediction methods that rely on the physical principles of the system, such as molecular mechanics or quantum mechanics based methods to predict molecular properties. If your method takes advantage of both kinds of approaches please report it as “Mixed”. If you choose the “Mixed” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `logP`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `permeability-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `permeability-myname-1.csv`, `permeability-myname-2.csv`, and `permeability-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.


## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pKa prediction tools etc.


## References
[1] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[2] Comer, John, and Kin Tam. Lipophilicity Profiles: Theory and Measurement. Wiley-VCH: Zürich, Switzerland, 2001.
