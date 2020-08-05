## pKa Challenge Instructions

The SAMPL7 pK<sub>a</sub> Challenge consists of predicting microscopic pK<sub>a</sub>'s of small molecules. Participants are asked to report relative free energies of protonation microstates calculated based on a reference state and pH. Relative free energies of microstates were chosen as the reporting format rather than the microscopic pKa values given the recent work of Gunner et al.[1]

A submission template file can be found in the [submission_template/](submission_template/) directory and an example submission file can be found in [submission_template/](example_submission_file/).

For each molecule, the relative free energy must be predicted between the reference microstate and the rest of the enumerated microstates for that molecule at a reference pH of 0. The first microstate in each CSV file indicated by `SMXX_micro000` is our selected neutral reference state. For example, for molecule SM25, if the reference microstate is SM25_micro000, then relative free energies must be computed between SM25_micro000 and SM25_micro001, SM25_micro000 and SM25_micro002, and SM25_micro000 and SM25_micro003.

All possible tautomers of each ionization (charge) state are defined as distinct protonation microstates.

- Fill one [`submission_template/pKa_prediction_template.csv`](submission_template/pKa_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method.

- Record the pair of microstates IDs associated with each relative free energy calculation between the reference state and the predicted microstates. Enumerated microstates, IDs, SMILES strings and SDF/MOL2 files can be found in https://github.com/samplchallenges/SAMPL7/tree/master/physical_property/pKa/microstates.

- If you have evaluated additional microstates, we ask that you include the same information as the other challenge molecules, but include the SMILES string in your submission and email a `.mol2` file of the microstate with explicit hydrogens and correct bond orders to `bergazin@uci.edu`. See [`example_submission_file/pKa-DanielleBergazinExampleFile-1.csv`](example_submission_file/pKa-DanielleBergazinExampleFile-1.csv) for an example. Additonal microstate molecule ID's must be in the form `SMXX_extra001`, where the molecule tag is followed by `_extra` and some number `001`.

- You may report only 1 relative free energy value per molecule per method.

- The energy units must be in kcal/mol.

- It is mandatory to submit predictions for all 22 molecules. Incomplete submissions will not be accepted.

- Report relative free energy values to two decimal places (e.g. 13.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [2,3]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol (that is 40 characters or less), a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Name:`, `Software:`, `Category:`, and `Method:`, as illustrated in the example files. An example submission file can be found [here](example_submission_file/pKa-DanielleBergazinExampleFile-1.csv) to illustrate expected format when filling submission templates.

- For Method Category section please state if your prediction method can be better classified as an
experimental database lookup (DL), linear free energy relationship (LFER)[3], quantitative structure-property relationship or machine learning (QSPR/ML)[3], quantum mechanics without empirical correction (QM) models, quantum mechanics with linear empirical correction (QM+LEC), and combined quantum mechanics and molecular mechanics (QM+MM), or Other, using the category labels `DL`, `LFER`, `QSPR/ML`, `QM`, `QM+LEC`, `QM+MM` or `Other`. If you choose the “Other” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `pKa`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `pKa-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `pKa-myname-1.csv`, `pKa-myname-2.csv`, and `pKa-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.


## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pKa prediction tools etc.


## Submission of multiple predictions
Some participants use SAMPL to help evaluate various computational methods. To accommodate this, multiple prediction sets from a single research group or company are allowed, even for the same type of predictions if they are made by different methods. If you would like to submit predictions from multiple methods, you should fill a separate submission template files for each different method.

## References
[1] Gunner, M.R., Murakami, T., Rustenburg, A.S. et al. "Standard state free energies, not pKas, are ideal for describing small molecule protonation and tautomeric states." Journal of Computer-Aided Molecular Design 34, 561–573 (2020). https://doi.org/10.1007/s10822-020-00280-7

[2] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[3] Mobley, David L., Karisa L. Wymer, Nathan M. Lim, and J. Peter Guthrie. “Blind Prediction of Solvation Free Energies from the SAMPL4 Challenge.” Journal of Computer-Aided Molecular Design 28, no. 3 (March 2014): 135–50. https://doi.org/10.1007/s10822-014-9718-2

[4] U. A. Chaudry and P. L. A. Popelier. “Estimation of pKa Using Quantum Topological Molecular Similarity Descriptors:  Application to Carboxylic Acids, Anilines and Phenols.” The Journal of Organic Chemistry 2004 69 (2), 233-241. https://doi.org/10.1021/jo0347415
