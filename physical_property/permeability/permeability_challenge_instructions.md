## PAMPA permeability Challenge Instructions

A submission template file can be found in the [submission_template/](submission_template/) directory and an example submission file can be found in [example_submission_file/](example_submission_file/). Predictions must be submitted via our AWS submissions server, [http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL7-physprop](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL7-physprop). **The submission deadline is Oct. 8, 2020**.

For each molecule, we are asking participants to predict the log of the apparent permeability coefficient log<sub>*P*<sub>*app*</sub></sub>. Experimental PAMPA permeability measurements include effective permeability and membrane retention.

We would like to note that compounds `SM35`, `SM36` and `SM37` are enantiopure and have a chiral center. All other compounds are not chiral. **The files provided in this repository provided versions of these compounds with both specified and unspecified stereochemistry for these compounds** because we were not clear that they had been tested in enantiopure form. This was corrected on Oct. 1, 2020. We retain the full set of files here for historical reasons, but predictions should use the files with specified chirality.

- Fill one [`submission_template/permeability_prediction_template.csv`](submission_template/permeability_prediction_template.csv) template for all molecules predicted with one method. You may submit predictions from multiple methods, but you should fill a separate template file for each different method.

- log<sub>*P*<sub>*app*</sub></sub> is unitless.

- Your log<sub>*P*<sub>*app*</sub></sub> predictions do NOT have to use the challenge provided molecules in the `SAMPL7_molecule_ID_and_SMILES.csv` file. If you used the permeability challenge provided molecule (as found in the `SAMPL7_molecule_ID_and_SMILES.csv` file) then please fill out the `Molecule ID/IDs considered (no commas)` section using a molecule ID in the form `SMXX`. If you used a microstate that was provided in the pKa challenge please use that name in the `Molecule ID/IDs considered (no commas)` section (e.g. SM26_micro000, SM26_micro001, etc.). If you used a microstate NOT provided in any of the current SAMPL challenges you must use the form `SMXX_extraXXX` (where XXX can be any number). You may assume that microstates with unspecified chirality are equal in free energy to those with specified chirality.

- If you have evaluated additional microstates that are not found in the SAMPL challenge then the molecule ID used in the `Molecule ID/IDs considered (no commas)` section needs to be in the format: `SMXX_extraXXX` (number can vary). If multiple microstates are used, please report the order of population in the aqueous phase in descending order. Please list your chosen molecule ID, microstate populations and SMILES strings in the `METHOD DESCRIPTION SECTION` in your submission file.

- You may report only 1 log<sub>*P*<sub>*app*</sub></sub> value per molecule per method.

- Each participant or organization is allowed only one ranked submission.

- Anonymous participation is not allowed.

- It is mandatory to submit predictions for all molecules except `SM33`, `SM35`, and `SM39`, which are optional (since values were not determined). Incomplete submissions will not be accepted.

- Report log<sub>*P*<sub>*app*</sub></sub> values to two decimal places (e.g. 3.71).

- Report the standard error of the mean (SEM) as a measure of statistical uncertainty (imprecision) for your method. The SEM should capture variation of predicted values of the same method over repeated calculations.

- Report the model uncertainty of your difference in free energy prediction --- the predicted accuracy of your method [1,9]. This is not a statistical uncertainty. Rather, the model uncertainty is an estimate of how well your predicted values are expected to agree with experimental values. For example, for classical simulation approaches based on force fields, this could measure how well you expect the force field will agree with experiment for this compound. The model uncertainty could be global or different for each molecule. For example, reference calculations in SAMPL5 log D challenge estimated the model uncertainty as the root mean squared error (RMSE) between predicted and experimental values for a set of molecules with published cyclohexane-water partition coefficients.

- Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored during analysis.

- The file must contain the following four components in the following order: your predictions, a name for your computational protocol (that is 40 characters or less), the average compute time across all of the molecules in hours (GPU/CPU time for physical methods, query time for empirical methods), details of the computing resources and hardware used to make predictions, a list of the major software packages used, prediction method category, and a long-form methods description. Each of these components must begin with a line containing only the corresponding keyword: `Predictions:`, `Participant name:`, `Participant organization:`, `Name:`, `Compute time:`, `Computing and hardware:`, `Software:`, `Category:`, `Method:`, and `Ranked:`, as illustrated in the example file. An example submission file can be found [here](example_submission_file/permeability-DanielleBergazinExampleFile-1.csv) to illustrate expected format when filling submission templates.

- For Method Category section please state if your prediction method can be better classified as an empirical modeling method, physical quantum mechanics (QM) modeling method, physical molecular mechanics (MM) modeling method, or mixed (both empirical and physical), using the category labels `Empirical`, `Physical (MM)`, `Physical (QM)`, or `Mixed`. Empirical models are prediction methods that are trained on experimental data, such as QSPR, machine learning models, artificial neural networks etc. Physical models are prediction methods that rely on the physical principles of the system, such as molecular mechanics or quantum mechanics based methods to predict molecular properties. If your method takes advantage of both kinds of approaches please report it as “Mixed”. If you choose the “Mixed” category, please explain your decision in the beginning of Method Description section.

- Names of the prediction files must have three sections separated by a `-`: predicted property `permeability`, and your name and must end with an integer indicating the number of prediction set. For example, if you want to submit one prediction, you would name it `permeability-myname-1.csv`, where `myname` is arbitrary text of your choice. If you submit three prediction files, you would name them `permeability-myname-1.csv`, `permeability-myname-2.csv`, and `permeability-myname-3.csv`.

- Prediction files will be machine parsed, so correct formatting is essential. Files with the wrong format will not be accepted.

## Multiple submissions
As per our policy on multiple submissions, each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form. We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.


## Experimental details
Effective permeability (log<sub>*P*<sub>*app*</sub></sub>) was measured by Parallel Artificial Membrane Permeability Assay (PAMPA) using the Corning GentestTM pre-coated PAMPA plate system with quantitation by HPLC-UV (experiments carried out by Analyza, Inc).

The artificial membrane is composed of 40 µg of DOPC on both sides of the plate with a 1 µL deposit of hexadecane in the center.

Samples were prepared as DMSO stock solutions and sonicated in a 40°C water bath to facilitate dissolution. Dilutions (50-fold) of the DMSO stocks were prepared in PBS, 7.4 for a dose concentration of 200μM in a volume of 300μL directly in the Donor compartment of the Corning GentestTM Pre-coated PAMPA plate. After preparation of the Donor plate, any precipitation was noted. The Acceptor compartment was filled with 1xPBS (200μL), pH 7.4. After PAMPA plate assembly, it was incubated for five hours in the dark at ambient temperature. A sister plate was created (50x dilution of 10mM test articles was prepared in 1xPBS, pH 7.4) directly in a Millipore solubility filter plate to measure the initial concentration of the sample in buffer (C0). Following incubation, the PAMPA plate was disassembled, and the samples were transferred from the Donor and Acceptor plates to 96-well plates for analysis. The C0 plate was filtered prior to analysis

The concentration values from the Donor and Acceptor compartment are used in the calculation of the effective permeability (Pe) of the compound. A mass balance equation is used to calculate the amount of compound retained in the membrane (%R). A high %R indicates either that the compound is bound to the PAMPA membrane, or that the compound is precipitating in the donor compartment. The equations for permeability and membrane retention are shown below. Note that the Ballatore lab experimentally determined Co, instead of assuming the full solubility of the compound. Pe values less than 1.5E-6 cm/s correlate with human fraction absorbed (%FA) less than 80%, a generally accepted cutoff for low permeability.

![permeability equations](../images/permeability_equations.jpeg)


These experiments used the “Corning GentestTM pre-coated PAMPA plate system,” with a “lipid-oil-lipid” trilayer in the artificial membrane. The artificial membrane was composed of 40 µg of DOPC on both sides of the plate with a 1 µL deposit of hexadecane in the center, as indicated [here](https://www.corning.com/catalog/cls/documents/application-notes/an_DL_GT_053_Automation_of_Pre-coated_PAMPA_Plates_Improves_Predictability_Reproducibility_Efficiency.pdf).

One problem is that we’re not sure how close this artificial bilayer is to a pure lipid bilayer. Some groups chose to use an unstressed DOPC bilayer for calculations. However, there may be regions of non-lamellar lipids (as shown by Assmus et al. [3]) or the surface area of the DOPC could be substantially changed by the formulation. This is an active topic of research and one where further work is needed.

The following materials may be useful:
1. Supporting documents for the “Corning® Gentest™ Pre-coated PAMPA Plate System” can be found on the [Corning website](https://ecatalog.corning.com/life-sciences/b2c/US/en/Microplates/Assay-Microplates/96-Well-Microplates/Corning%C2%AE-Gentest%E2%84%A2-Pre-coated-PAMPA-Plate-System,-with-Lid,-1-Pack,-5-Case/p/353015)
2. [Automation of Pre-coated PAMPA Plates Improves Predictability, Reproducibility, and Efficiency (Application Note 475)](https://www.corning.com/catalog/cls/documents/application-notes/an_DL_GT_053_Automation_of_Pre-coated_PAMPA_Plates_Improves_Predictability_Reproducibility_Efficiency.pdf)
3. [Corning® Gentest™ PAMPA Plate System (Frequently Asked Questions)](https://www.corning.com/catalog/cls/documents/faqs/CLS-DL-GT-063_DL.pdf)
4. [Paper showing there may be regions of non-lamellar lipids --- 31P and 1H NMR Studies of the Molecular Organization of Lipids in the Parallel Artificial Membrane Permeability Assay](https://pubs.acs.org/doi/full/10.1021/acs.molpharmaceut.6b00889)
5. [A Novel Design of Artificial Membrane for Improving the PAMPA Model](https://link.springer.com/article/10.1007/s11095-007-9517-8)

## Method descriptions
Your method descriptions should give a detailed description of your approach, ideally with enough detail that someone could reproduce the work. These often serve to allow researchers to coordinate on why calculations which seem similar performed quite different in practice, so you should be sure to address how you generated poses, selected protonation states and tautomers if applicable, dealt with counterions, and various other aspects that might be important, as well as any method-specific details that, if varied, might result in different performance. For example, with MD simulations, the amount of equilibration might impact performance significantly in some cases, so this should also be included.

## Computational prediction methods
You may use any method(s) you like to generate your predictions; e.g., molecular mechanics or quantum mechanics based methods, QSPR, empirical pKa prediction tools etc.

## Submission of multiple predictions
Some participants use SAMPL to help evaluate various computational methods. To accommodate this, multiple prediction sets from a single research group or company are allowed, even for the same type of predictions if they are made by different methods. If you would like to submit predictions from multiple methods, you should fill a separate submission template files for each different method.

## References
[1] Bannan, Caitlin C., Kalistyn H. Burley, Michael Chiu, Michael R. Shirts, Michael K. Gilson, and David L. Mobley. “Blind Prediction of Cyclohexane–water Distribution Coefficients from the SAMPL5 Challenge.” Journal of Computer-Aided Molecular Design 30, no. 11 (November 2016): 927–44.

[2] Comer, John, and Kin Tam. Lipophilicity Profiles: Theory and Measurement. Wiley-VCH: Zürich, Switzerland, 2001.

[3] Assmus, Frauke, Alfred Ross, Holger Fischer, Joachim Seelig, and Anna Seelig. "31P and 1H NMR Studies of the Molecular Organization of Lipids in the Parallel Artificial Membrane Permeability Assay"
Molecular Pharmaceutics 2017 14 (1), 284-295. DOI: 10.1021/acs.molpharmaceut.6b00889
