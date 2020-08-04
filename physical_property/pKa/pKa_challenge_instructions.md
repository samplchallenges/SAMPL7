## pKa Challenge Instructions

The SAMPL7 pK<sub>a</sub> Challenge consists of predicting relative free energies between microstates to determine the pK<sub>a</sub>. Free energies were chosen rather than pKa values given the recent work of [Gunner et al.](https://link.springer.com/content/pdf/10.1007/s10822-020-00280-7.pdf). The paper also details how to convert pK<sub>a</sub> predictions to relative free energies.

A submission template file can be found in the [submission_template/](submission_template/) directory and an example submission file can be found in [submission_template/](example_submission_file/).

For each molecule, the relative free energy must be predicted between the reference microstate and the rest of the enumerated microstates for that molecule. The first microstate in each CSV file indicated by `SMXX_000` is our selected neutral reference state. For example, for molecule SM25, if the reference microstate is SM25_micro000, then relative free energies must be computed between SM25_micro000 and SM25_micro001, SM25_micro000 and SM25_micro002, and SM25_micro000 and SM25_micro003.

All possible tautomers of each ionization (charge) state are defined as distinct protonation microstates.

- Fill one [`submission_template/pKa_prediction_template.csv`](submission_template/pKa_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method.

- Record the pair of microstates IDs associated with each relative free energy calculation between the reference state and the other microstates. Enumerated microstates, IDs, SMILES strings and SDF/MOL2 files can be found in https://github.com/samplchallenges/SAMPL7/tree/master/physical_property/pKa/microstates.

- If you have evaluated additional microstates, we ask that you include the same information as the other challenge molecules, but include the SMILES string in your submission and email a `.mol2` file of the microstate with explicit hydrogens and correct bond orders to `bergazin@uci.edu`. See [`example_submission_file/pKa-DanielleBergazinExampleFile-1.csv`](example_submission_file/pKa-DanielleBergazinExampleFile-1.csv) for an example. Additonal microstate molecule ID's must be in the form `SMXX_extra001`, where the molecule tag is followed by `_extra` and some number `001`.

- You may report only 1 relative free energy value per molecule per method.

- It is mandatory to submit predictions for all 22 molecules. Incomplete submissions will not be accepted.

- Report relative free energy values to two decimal places (e.g. 13.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [1,2]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Name:`, `Software:`, `Category:`, and `Method:`, as illustrated in the example files. An example submission files can be found [`here`]['example_submission_file/pKa-DanielleBergazinExampleFile-1.csv'] to illustrate expected format when filling submission templates.

- For Method Category section please state if your prediction method can be better classified as an empirical modeling method, physical quantum mechanics (QM) modeling method, physical molecular mechanics (MM) modeling method, or mixed (both empirical and physical), using the category labels `Empirical`, `Physical (MM)`, `Physical (QM)`, or `Mixed`. Empirical models are prediction methods that are trained on experimental data, such as QSPR, machine learning models, artificial neural networks etc. Physical models are prediction methods that rely on the physical principles of the system, such as molecular mechanics or quantum mechanics based methods to predict molecular properties. If your method takes advantage of both kinds of approaches please report it as “Mixed”. If you choose the “Mixed” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `pKa`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `pKa-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `pKa-myname-1.csv`, `pKa-myname-2.csv`, and `pKa-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.


## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pKa prediction tools etc.


## References
[1] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[2] Mobley, David L., Karisa L. Wymer, Nathan M. Lim, and J. Peter Guthrie. “Blind Prediction of Solvation Free Energies from the SAMPL4 Challenge.” Journal of Computer-Aided Molecular Design 28, no. 3 (March 2014): 135–50. https://doi.org/10.1007/s10822-014-9718-2.
