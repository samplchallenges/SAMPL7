# SAMPL7 Detailed Host-Guest Instructions

## Due date

Due dates vary by challenge; refer to the main [README.md](README.md) for exact dates.

Your predictions must be uploaded via our [web form](http://sampl-submission.us-west-1.elasticbeanstalk.com/submit) before midnight US Pacific time on the due date. The experimental results will be available as soon as possible after SAMPL closes. Please refer to the below instructions for information on uploading.

You must use the provided templates to upload your predictions. Templates are:
- [cyclodextrin_derivatives/CD_submission.txt](cyclodextrin_derivatives/CD_submission.txt) for cyclodextrin cyclodextrin derivatives
- [GDCC_and_guests/GDCC_submission.txt](GDCC_and_guests/GDCC_submission.txt) for the GDCC challenge
- [Isaacs_clip/Clip_submission.txt](Isaacs_clip/Clip_submission.txt) for the Isaacs clip/TrimerTrip challenge

File names must begin with the letters "CD", "GDCC", or "Clip" depending on the
challenge (as in the template files) and be followed by an underscore or dash.
The remainder of the filename is up to you.

## Multiple submissions

As per our [policy on multiple submissions](https://samplchallenges.github.io/roadmap/submissions/), each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form. We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.

## Anonymous participation

Anonymous participation is not allowed.

## Molecular systems

Three different host-guest categories are considered, each involving one or more sub-systems, as detailed in the main README.md. Measured binding free energies are available in all cases, and binding enthalpies are also expected to be available.

### Optional systems:
In the cyclodextrin derivatives sub-challenge, beta-cyclodextrin is provided as a host but can be considered optional, because literature values are likely available for binding of the guests to this host. Beta-CD binding will not be judged, but can be used as a reference (e.g. for relative free energy calculations).

In the Gibb deep cavity cavitand (GDCC) challenge, octa acid (OA) binding prediction for guests 1 through 6 is optional (as literature values are available) but guests 7 and 8 are required. The whole series is required for exoOA. All values can be submitted, as values for the optional combinations can serve as a reference (e.g. for relative free energy calculations).

### Optional values:
All submissions are required to have predicted binding **free energies**, predicted standard error,
and predicted model uncertainty (your estimate of the accuracy of your method, which can vary from compound to compound), for all required compounds/systems. Enthalpy predictions (and the associated errors/model uncertainties) are optional, though for most systems here, binding enthalpy values WILL be available.

## Computational methods

You may use any method(s) you like to generate your predictions; e.g., MD with implicit or explicit solvent; quantum methods; docking; etc.

## Method descriptions

Your method descriptions should give a detailed description of your approach, ideally with enough detail that someone could reproduce the work. These often serve to allow researchers to coordinate on why calculations which seem similar performed quite different in practice, so you should be sure to address how you generated poses, selected protonation states and tautomers if applicable, dealt with counterions, and various other aspects that might be important, as well as any method-specific details that, if varied, might result in different performance. For example, with MD simulations, the amount of equilibration might impact performance significantly in some cases, so this should also be included.

## Files provided

All hosts and guests are provided in mol2, PDB and SDfile formats. A README.md file in host_guest and in the individual subdirectories gives more details about the files provided. Disclaimers apply: There is no guarantee or representation that the protonation and tautomer states provided are optimal. It is also possible that the protonation state of a guest or host will change on binding. Guest files do not necessarily use the same frame of reference as the host so you are responsible for aligning/posing correctly.

## Uploading your predictions

[Submit your SAMPL7 predictions here](http://sampl-submission.us-west-1.elasticbeanstalk.com/submit/). Note our submission page resides on AWS at [http://sampl-submission.us-west-1.elasticbeanstalk.com/submit/](http://sampl-submission.us-west-1.elasticbeanstalk.com/submit/), so don't be alarmed by the URL.

If you want to upload more than one set of predictions, generated by different methods, each set must be uploaded as a separate file. Please use the template provided, as the predictions will be parsed and analyzed with automated scripts, and if you violate the file format, you will receive an error message and your submission will not be accepted. A complete set of predictions constitutes predicted binding free energies for all required host-guest pairs, with predicted numerical uncertainties. We also encourage predictions of the binding enthalpies. Incomplete submissions - such as for a subset of compounds - will also be accepted if desired (contact David Mobley if this is needed, as currently our submission system checks for completeness), but would be treated as "verified" submissions rather than "ranked" submissions. However, omission of enthalpies and/or bonus cases will not cause a submission to be regarded as incomplete.

Names of the uploaded prediction files must begin with the name of the challenge component for which it contains predictions, as in the provided templates (i.e., GDCC, Clip, or CD, case-independently), and must end with an integer indicating which of your predictions for this host it contains. For example, if you want to submit one prediction file for the GDCC component, you might name it GDCC-myname-1.csv, where myname is arbitrary text of your choice. If you submit two prediction files for GDCC, you might name them GDCC-myname-1.txt and GDCC-myname-2.txt. Naming of guests, or host-guest combinations (as applicable) should be as illustrated in the submission templates.

The file will be machine parsed, so correct formatting is essential.

Lines beginning with a hash-tag (#) may be included as comments. These and blank lines will be ignored.

The file must contain the following five components in the following order: your predictions, a name for your computational protocol, a list of the major software packages used, a long-form methods description, and, finally, whether your submission is to be ranked or not. Each of these components must begin with a line containing only the corresponding keyword: Predictions:, Name:, Software:, Method:, and Ranked:, as illustrated in the example files. The last field should have a boolean value (True or False). See above information on "multiple submissions" for discussion of the role this plays.
