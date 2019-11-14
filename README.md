# The SAMPL7 Blind Prediction Challenges for Computational Chemistry
[![DOI](https://zenodo.org/badge/184310568.svg)](https://zenodo.org/badge/latestdoi/184310568)


Challenge details, inputs, and (eventually) results for the SAMPL7 series of challenges

See the [SAMPL website](https://samplchallenges.github.io) for information on the Statistical Assessment of the Modeling of Proteins and Ligands (SAMPL) series of challenges as a whole. This repository focuses specifically on the SAMPL7 series of challenges.

Because these files are available publicly, we have no record of who downloads them. Therefore, you should sign up for notifications. Specifically, if you want to receive updates if we uncover any problems, it is imperative that you either (a) sign up for the SAMPL e-mail list, or (b) sign up for notifications of changes to this GitHub repository (the Watch button, above); ideally you would do both.
Join our [SAMPL7 e-mail list](http://eepurl.com/gpBBun) to get e-mails with SAMPL7-related announcements.

## What's here
- [Challenge Overview](#challenge-overview)
- Final information on the TrimerTrip host-guest challenge components in the `host_guest/Isaacs_clip` directory, and experimental values in the `host_guest/Analysis/ExperimentalMeasurements` directory.
- Final information on the Gibb octa acid-based challenge ("Gibb deep cavity cavitand" (GDCC) challenge) in the `host_guest/GDCC_and_guests` directory.
- Final information on the cyclodextrin derivatives challenge in the `host_guest/cyclodextrin_derivatives` directory and in our [host-guest challenge description](host_guest_description.md).
- Experimental details for the CD challenge in [host_guest_description.md](host_guest_description.md)
- [Host-guest participation instructions](host_guest_instructions.md) with information on the submission format, etc. Our submission system is also [now available](http://sampl-submission.us-west-1.elasticbeanstalk.com/submit/). Submission formats are available in the subdirectories for the individual host-guest systems.
- Protein-ligand details on the [PHIP2 challenge](protein_ligand/README.md), in the `protein_ligand` directory.
- [PHIP2 challenge submission instructions](protein_ligand_instructions.md), in the `protein_ligand_instructions.md` file. Our submission system is not yet available.

All three host-guest components of this challenge are now final and launched, though additional supporting files may be added at a later date. **The submission deadline is Oct. 4 for the TrimerTrip host-guest challenge and Nov. 4 for the cyclodextrin derivatives and GDCC challenges**, due to timescales for data collection and publication of the experimental data. The **first stage of the protein-ligand challenge is due Nov. 28, 2019.**

## What's coming
- GSK logD challenge information as soon as available
- Results (and inputs for) host-guest reference calculations as conducted by Mobley lab, as soon as available. We are conducting alchemical binding free energy calculations with Yank.
- Experimental results for the host-guest challenge (except for TrimerTrip, which is available now)
- Analysis of submissions for the host-guest challenge
- PHIP2 protein-ligand challenge details on Stage 2 and Stage 3.

## Disclaimers:
- As usual, we make no warranty as to correctness of protonation states, tautomers, conformations and poses provided in these directories. In some cases the most relevant such states may not be known, or multiple states perhaps should be considered. Please exercise caution and due diligence.
- We make an effort to indicate which files are original source files, and which are derived files, so that participants can refer to the original source files to help resolve any uncertainties. We encourage participants to do so.
- While we make every effort to ensure correctness of the files we provide, it is not uncommon for there to be some errors. **Please sign up for our [e-mail list](http://eepurl.com/gpBBun)**, since if any critical bugs are found, we will e-mail out appropriate announcements.

## Changes and Data Set Versions

### Release versions
- **Release 0.1** (July 22, 2019): Finalizes all three host-guest systems and provides sdf, mol2 and PDB files for all guests. Fixes several critical bugs, including **fixing several incorrect cyclodextrin-derivative host structure files**, **fixing errors in a draft TrimerTrip structure file**, **fixing the SMILES string for TrimerTrip guest `g15`**, and **finalizing TrimerTrip guest list**.
- **Release 0.1.1** (July 22, 2019, DOI [10.5281/zenodo.3346023](https://dx.doi.org/10.5281/zenodo.3346023)): Includes updated README files that should have been in release 0.1.
- **Release 0.1.2** (Sept. 16, 2019, DOI [10.5281/zenodo.3432298](https://dx.doi.org/10.5281/zenodo.3432298)): Fixes protonation states for three "modified cyclodextrin" hosts which had accidentally been prepared (and drawn in ChemDraw) with charged groups present as neutral -- specifically terminal -NH3 groups were provided as -NH2. This affected MGLab19, 24 and 34. Also includes minor maintenance fixes -- listing final rather than tentative buffer conditions for GDCC case (just removing the "tentative" on the buffer identity, and correcting pH from 11.5 to 11.7); updates submission deadlines; fixes missing coordinates in TrimerTrip `g11`; fixing breakdown into residues in a couple modified cyclodextrin host PDB/mol2 files.
- **Release 0.2** (Sept. 24, 2019, DOI [10.5281/zenodo.3459975](https://dx.doi.org/10.5281/zenodo.3459975)): Adds host-guest submission template files and instructions; makes more clear which compounds/cases are optional; makes clear that free energy predictions (and uncertainties) are required; enthalpies optional; adds links to [host-guest submission system](http://sampl-submission.us-west-1.elasticbeanstalk.com/submit/)
- **Release 0.3** (Sept. 26, 2019, DOI [10.5281/zenodo.3462865](https://dx.doi.org/10.5281/zenodo.3462865)): Corrected likely charges/protonation states for MGLab23 and MGLab24 in overview table and in jpg and PDF files. Updated corresponding coded and noncoded CDX files. Fixed a mixture of UNK and MGO residue names. Eliminates all instances of atom name HQ which should correspond to a carbon (which for some reason was instead named HX in some hosts, likely causing problems for some workflows). This has been mapped to atom name C9. Reconnects missing bonds in the PDB section of several models. See [PR 42](https://github.com/MobleyLab/SAMPL7/pull/42) for full details. Also removes outdated info in README.md and removes extra guest listed in TrimerTrip submission template.
- **Release 0.4** (Oct. 30, 2019)): Adds Isaacs' group TrimerTrip binding data (in `host_guest/analysis/ExperimentalMeasurements`); adds TrimerTrip submissions; adds PHIP2 protein-ligand challenge Stage 1 details.

### Changes not in a release
- (11/2/19, PHIP2) Fix misformatted SMILES line on line 620 of `fragments_screened.csv` for PHIP2 screening challenge.
- (11/11/19, PHIP2) Fix an incorrect SMILES for fragment F62 in the PHIP2 screening challenge.
- (11/12/19, PHIP2) Add participation instructions and submission format for PHIP2 virtual screening component (Stage 1).

## Challenge overview

The SAMPL7 phase of challenges currently includes a protein-ligand component on PHIP2, as well as host-guest binding on three systems: A pair of Gibb Deep Cavity Cavitands (GDCCs), a new "TrimerTrip" molecule from Lyle Isaacs and his group, and a series of cyclodextrin derivatives from Mike Gilson's group. Each host binds one or more guests, and each system involves a total of 9-20 binding free energy calculations.
Additional details are provided below. Note that several hosts and/or guests are optional.

A later phase of SAMPL7 is expected to include logD prediction (hopefully with pKa values provided) for a series of small moleculs in several solvents; data is currently being collected in partnership with GSK.

### PHIP2 binding prediction

We are excited to announce a new set of SAMPL7 challenges focusing on protein-ligand binding, in partnership with the XChem facility for fragment screening at Diamond Light Source. The second bromodomain of PHIP (PHIP2) was targeted in an extensive X-ray crystallographic fragment screening experiment, leading to the 3D structures of multiple hits. This SAMPL7 challenge will take advantage of this dataset, addressing computational methods for the discrimination of binders from non-binders, binding pose predictions, and the unique opportunity to select new candidate ligands from a database, to be validated experimentally by X-ray crystallography at the Diamond Light Source (Harwell, UK).   

This challenge breaks out into at least three stages on a tight timeline:
1) Identification of binders from fragment screening
2) Prediction of fragment binding modes
3) Selection of new compounds for screening from an experimental database

Stage 1 is now open and focuses on identification of binders. Unfortunately, the timeline for stages 1 and 2 has to be tight given the timeframe for experimental compound screening (Stage 3). See [protein_ligand/README.md](protein_ligand/README.md) for full details.


### Gibb Deep Cavity Cavitand (GDCC) binding of guests

One host-guest series is based on the Gibb Deep Cavity Cavitands (GDCCs), familiar from SAMPL4-6. However, this challenge we swap one of the hosts; previously, we used octa acid (OA) and tetramethyl octa acid (TEMOA); this challenge revisits OA but also utilizes a variant which changes the location of the carboxylates.  Both were developed in the laboratory of Dr. Bruce Gibb (Tulane U), who will provide binding free energies and enthalpies, measured by ITC. In this case the challenge is to predict binding of eight compounds to *exo*-OA (a new host created and studied by the Gibb group and first disclosed in this challenge), and two of these to OA; the other six have been studied previously in OA and can *optionally* be submitted. Existing benchmark datasets based on the OA host may be of interest for those preparing to tackle these new complexes: https://github.com/MobleyLab/benchmarksets; this perpetual review paper also provides a good introduction to the sampling and experimental issues which are known to be relevant in these systems. See the [README on this challenge](host_guest/GDCC_and_guests/README.md) for more details.

### Modified acyclic cucurbituril (TrimerTrip) binding of guests

The Isaacs lab is contributing data on binding of a series of guests to an acyclic cucubituril host, codenamed "TrimerTrip", as detailed in `host_guest/Isaacs_clip`. Guests include compounds which overlap with the GDCC and cyclodextrin-derivative challenges, with a total of roughly 15 complexes being examined. See the [README on this challenge](host_guest/Isaacs_clip/README.md) for more details.

### The cyclodextrin derivatives challenge

The Gilson lab is measuring binding of two guests to ten different hosts, comprising beta-cyclodextrin as well as nine different cyclodextrin derivatives which have a single functional group added at one location around the rim of the cavity. Binding is being characterized via ITC and NMR. The two guest compounds (R-rimantadine and trans-4-methylcyclohexanol) overlap with those used in the TrimerTrip and GDCC challenges. [Full details](host_guest_description.md) are available. Binding to beta-cyclodextrin can optionally be submitted, but literature values for these compounds are available.

## MANIFEST
- `host_guest`: Details on host-guest challenges
- `protein_ligand`: Details on/inputs for PHIP2 bromodomain challenge. Currently Phase 1 is available.
- `host_guest_description.md`: Detailed description of aspects of the host-guest challenges
- `protein_ligand_instructions.md`: Detailed instructions for participation in the protein-ligand challenge.

## SAMPL-related content

If you give a SAMPL-related talk or presentation or an analysis of its data, and are willing to share publicly, please consider posting on Zenodo and linking it to the [SAMPL Zenodo community](https://zenodo.org/communities/sampl?page=1&size=20).

## LICENSE

This material here is made available under CC-BY and MIT licenses, as appropriate:
- MIT for all software/code
- CC-BY 4.0 for all other materials
