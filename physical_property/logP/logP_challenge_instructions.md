## log *P* Challenge Instructions

A submission template file can be found in the [submission_template/](submission_template/) directory and an example submission file can be found in [example_submission_file/](example_submission_file/). Predictions must be submitted via our AWS submissions server, [http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL7-physprop](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL7-physprop).

For each molecule, participants must predict the difference in free energy (the transfer free energy) for the neutral form between water and octanol. The transfer free energy can be calculated from the difference in solvation free energy into octanol and hydration free energy: ΔG<sub>*transfer*</sub> = ΔG<sub>*octanol*</sub>-ΔG<sub>*water*</sub>[1,2].

Octanol may be found in the aqueous phase. The mole fraction of water in octanol was measured as 0.2705 ± 0.0028 at 25°C[6].

- Fill one [`submission_template/logP_prediction_template.csv`](submission_template/logP_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method.

- Your transfer free energy prediction for the neutral form does NOT have to be `SMXX_micro000` (the challenge provided microstate). If you use a microstate other than the challenge provided microstate, please fill out the `Molecule ID/IDs considered (no commas)` section using a molecule ID in the form of `SMXX_extra001` (number can vary). In the `METHOD DESCRIPTION SECTION` in the submission file, please list the molecule ID and the SMILES string of the microstate that was used.

- If multiple microstates are used, please report the order of population in the aqueous phase in descending order. See further below for more info regarding predictions using multiple microstates.

- You may report only 1 transfer free energy value per molecule per method.

- Each participant or organization is allowed only one ranked submission.

- Anonymous participation is not allowed.

- The energy units must be in kcal/mol.

- It is mandatory to submit predictions for all 22 molecules. Incomplete submissions will not be accepted.

- Report difference in free energy values to two decimal places (e.g. 50.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [3,4]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log *D* challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol (that is 40 characters or less), the average compute time across all of the molecules in hours (GPU/CPU time for physical methods, query time for empirical methods), details of the computing resources and hardware used to make predictions, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Participant name:`, `Participant organization:`, `Name:`, `Compute time:`, `Computing and hardware:`, `Software:`, `Category:`, `Method:`, and `Ranked:`, as illustrated in the example file. An example submission file can be found [here](example_submission_file/logP-DanielleBergazinExampleFile-1.csv) to illustrate expected format when filling submission templates.

- For the "Method Category" section please state if your prediction method can be better classified as an empirical modeling method, physical quantum mechanics (QM) modeling method, physical molecular mechanics (MM) modeling method, or mixed (both empirical and physical), using the category labels `Empirical`, `Physical (MM)`, `Physical (QM)`, or `Mixed`. Empirical models are prediction methods that are trained on experimental data, such as QSPR, machine learning models, artificial neural networks etc. Physical models are prediction methods that rely on the physical principles of the system, such as molecular mechanics or quantum mechanics based methods to predict molecular properties. If your method takes advantage of both kinds of approaches please report it as “Mixed”. If you choose the “Mixed” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `logP`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `logP-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `logP-myname-1.csv`, `logP-myname-2.csv`, and `logP-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.

## Multiple submissions
As per our policy on multiple submissions, each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form. We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.

## Predictions using multiple microstates
If you have evaluated additional microstates for some of the molecules, we ask that you use the following formating for these predictions:
`ID tag`, `Molecule ID/IDs considered (no commas)`, `TFE`, `TFE SEM`, `TFE model uncertainty`. If you have evaluated additional microstates then the molecule ID used in the `Molecule ID/IDs considered (no commas)` section needs to be in the format: `SMXX_extra001` (number can vary). If multiple microstates are used, please report the order of population in the aqueous phase in descending order. Please list your chosen microstate populations and SMILES strings in the `METHOD DESCRIPTION SECTION` in your submission file.

## Experimental details
Log *P* measurements of compounds with known experimental pK<sub>a</sub> were obtained via potentiometric titrations using a Sirius T3 instrument[5] by the [Ballatore lab at UCSD](https://pharmacy.ucsd.edu/faculty/ballatore). Log *D*<sub>7.4</sub> values were extrapolated from the measured log *P* and pH. Compounds with pK<sub>a</sub> >10 had log *D*<sub>7.4</sub> measured via shake-flask method (shake-flask log *D*<sub>7.4</sub> carried out by Analyza, Inc). Some of the log *P* values are considered equal to the Log *D*<sub>7.4</sub>, as these compounds exhibit pKa values >10.

For experiments that used a Sirius T3, ionic strength adjusted water (0.15 M KCI) was used. Shake-flask log *D*<sub>7.4</sub> determinations use 1X-PBS buffer (pH 7.4) and a 10 mM stock solution in DMSO diluted to 10% DMSO by volume.

All experiments using the Sirius T3 were done at 25°C. Shake-flask log *D*<sub>7.4</sub> experiments (run by Analiza, Inc) were done at ambient temperature (room temperature).

Log *P*/*D* measurements using the Sirius T3 were done using solid samples, so the concentrations were different per compound.  

Log *P*’s were determined from 3 or more titrations.

## Method descriptions
Your method descriptions should give a detailed description of your approach, ideally with enough detail that someone could reproduce the work. These often serve to allow researchers to coordinate on why calculations which seem similar performed quite different in practice, so you should be sure to address how you generated poses, selected protonation states and tautomers if applicable, dealt with counterions, and various other aspects that might be important, as well as any method-specific details that, if varied, might result in different performance. For example, with MD simulations, the amount of equilibration might impact performance significantly in some cases, so this should also be included.

## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pKa prediction tools etc.

## Submission of multiple predictions
Some participants use SAMPL to help evaluate various computational methods. To accommodate this, multiple prediction sets from a single research group or company are allowed, even for the same type of predictions if they are made by different methods. If you would like to submit predictions from multiple methods, you should fill a separate submission template files for each different method.


## References
[1] Mehtap Işık, Teresa Danielle Bergazin, Thomas Fox, Andrea Rizzi, John D. Chodera, David L. Mobley. "Assessing the accuracy of octanol-water partition coefficient predictions in the SAMPL6 Part II log P Challenge". J Comput Aided Mol Des 34, 335–370 (2020). https://doi.org/10.1007/s10822-020-00295-0

[2] Caitlin C. Bannan, Gaetano Calabró, Daisy Y. Kyu, and David L. Mobley. "Calculating Partition Coefficients of Small Molecules in Octanol/Water and Cyclohexane/Water". Journal of Chemical Theory and Computation 2016 12 (8), 4015-4024. https://doi.org/10.1021/acs.jctc.6b00449

[3] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[4] Mobley, David L., Karisa L. Wymer, Nathan M. Lim, and J. Peter Guthrie. “Blind Prediction of Solvation Free Energies from the SAMPL4 Challenge.” Journal of Computer-Aided Molecular Design 28, no. 3 (March 2014): 135–50. https://doi.org/10.1007/s10822-014-9718-2.

[5] Mehtap Işık, Dorothy Levorse, David L. Mobley, Timothy Rhodes, John D. Chodera. "Octanol–water partition coefficient measurements for the SAMPL6 blind prediction challenge". J Comput Aided Mol Des (2019). https://doi.org/10.1007/s10822-019-00271-3

[6] Lang, Brian E. “Solubility of Water in Octan-1-Ol from (275 to 369) K.” Journal of Chemical & Engineering Data 57, no. 8 (August 9, 2012): 2221–26. https://doi.org/10.1021/je3001427
