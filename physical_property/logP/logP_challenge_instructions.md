## logP Challenge Instructions

A submission template file can be found in the [submission_template/](submission_template/) directory and an example submission file can be found in [example_submission_file/](example_submission_file/).

For each molecule, participants must predict the difference in free energy (the transfer free energy) for the neutral form between water and octanol. The transfer free energy can be calculated from the difference in solvation free energy into octanol and hydration free energy: ΔG<sub>*transfer*</sub> = <\Delta>G<sub>*octanol*</sub>-ΔG<sub>*water*</sub>[1,2].

- Fill one [`submission_template/logP_prediction_template.csv`](submission_template/logP_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method.

- You may report only 1 transfer free energy value per molecule per method.

- It is mandatory to submit predictions for all 22 molecules. Incomplete submissions will not be accepted.

- Report difference in free energy values to two decimal places (e.g. 50.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [3,4]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Name:`, `Software:`, `Category:`, and `Method:`, as illustrated in the example files. An example submission files can be found [here](example_submission_file/logP-DanielleBergazinExampleFile-1.csv) to illustrate expected format when filling submission templates.


- For Method Category section please state if your prediction method can be better classified as an empirical modeling method, physical quantum mechanics (QM) modeling method, physical molecular mechanics (MM) modeling method, or mixed (both empirical and physical), using the category labels `Empirical`, `Physical (MM)`, `Physical (QM)`, or `Mixed`. Empirical models are prediction methods that are trained on experimental data, such as QSPR, machine learning models, artificial neural networks etc. Physical models are prediction methods that rely on the physical principles of the system, such as molecular mechanics or quantum mechanics based methods to predict molecular properties. If your method takes advantage of both kinds of approaches please report it as “Mixed”. If you choose the “Mixed” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `logP`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `logP-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `logP-myname-1.csv`, `logP-myname-2.csv`, and `logP-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.

## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pKa prediction tools etc.

## Submission of multiple predictions
Some participants use SAMPL to help evaluate various computational methods. To accommodate this, multiple prediction sets from a single research group or company are allowed, even for the same type of predictions if they are made by different methods. If you would like to submit predictions from multiple methods, you should fill a separate submission template files for each different method.


## References
[1] Mehtap Işık, Teresa Danielle Bergazin, Thomas Fox, Andrea Rizzi, John D. Chodera, David L. Mobley. "Assessing the accuracy of octanol-water partition coefficient predictions in the SAMPL6 Part II log P Challenge". J Comput Aided Mol Des 34, 335–370 (2020). https://doi.org/10.1007/s10822-020-00295-0

[2] Caitlin C. Bannan, Gaetano Calabró, Daisy Y. Kyu, and David L. Mobley. "Calculating Partition Coefficients of Small Molecules in Octanol/Water and Cyclohexane/Water". Journal of Chemical Theory and Computation 2016 12 (8), 4015-4024. https://doi.org/10.1021/acs.jctc.6b00449

[3] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[4] Mobley, David L., Karisa L. Wymer, Nathan M. Lim, and J. Peter Guthrie. “Blind Prediction of Solvation Free Energies from the SAMPL4 Challenge.” Journal of Computer-Aided Molecular Design 28, no. 3 (March 2014): 135–50. https://doi.org/10.1007/s10822-014-9718-2.
