# The SAMPL7 physical property challenge
We are excited to announce a new set of SAMPL7 challenges focusing on pK<sub>a</sub>, partitioning, and permeability. [The Ballatore group at UCSD](https://pharmacy.ucsd.edu/faculty/ballatore) is contributing a set of measured water-octanol log *P*, log *D*, and pK<sub>a</sub> values for 22 compounds. They also provided Parallel Artificial Membrane Permeability Assay (PAMPA) permeability and melting point values they measured.


pK<sub>a</sub> prediction will consist of predicting relative free energies between compound microstates (which could be also thought of as the reaction free energy for that particular microstate transition; [see pKa instructions](https://github.com/samplchallenges/SAMPL7/blob/master/physical_property/pKa/pKa_challenge_instructions.md)). We choose free energies rather than pK<sub>a</sub> values given the recent work of [Gunner et al.](https://link.springer.com/content/pdf/10.1007/s10822-020-00280-7.pdf). For the purposes of the pK<sub>a</sub> challenge all possible tautomers of each ionization (charge) state are defined as distinct protonation microstates. Macro pK<sub>a</sub> values may be submitted to allow for a consistency check.

The partitioning prediction challenge will focus on predicting the difference in free energy for the neutral form between water and octanol. As a part of post prediction analysis challenge oraginzers will combine participant-predicted pK<sub>a</sub> and log *P* values to obtain estimated distribution coefficients, which will also be compared against experimental values. Participants may optionally submit their own log *D* values for a consistency check.

A [PAMPA permeability](https://pubs.acs.org/doi/10.1021/jm970530e) prediction challenge will also be run in parallel to the pK<sub>a</sub> and partition coefficient challenge.

All three challenges are optional, so participants may participate in all or any combination of these challenges.

Additionally, there’s the opportunity to predict melting points. Please let us know if you are interested in this.

Please sign up for our [e-mail list](http://eepurl.com/dPj11j) for announcements of any changes (be sure to indicate interest in SAMPL7 physical properties). Be sure to also “watch” this GitHub repository.

## Challenge timing details
Submissions to the SAMPL7 physical property challenge will be due October 8, 2020. Challenge participants will have the option of predicting relative free energies between microstates to determine pK<sub>a</sub><sup>[1](https://link.springer.com/content/pdf/10.1007/s10822-020-00280-7.pdf)</sup>, and/or the difference in free energy of the neutral molecules between water and octanol to determine partition coefficients, and/or the log<sub>*P*<sub>*app*</sub></sub> to determine permeabilities of 22 compounds.

Submission details, templates and instructions are linked to in the manifest.

The submission servers are now live: [SAMPL7 pKa submissions](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL7-pKa) and [SAMPL7 logP/permeability submissions](http://sampl-submit.us-west-1.elasticbeanstalk.com/submit/SAMPL7-physprop)). Note that each challenge component has its own format, but logP and permeability share the same submission URL.

## A view of the compounds

![22 SAMPL7 molecules](images/compounds-2d-depiction.jpeg)

**Fig 1. SAMPL7 Challenge molecules.** Log of the partition coefficient between n-octanol and water was determined via potentiometric titrations using a Sirius T3 instrument. pK<sub>a</sub> values were determined by potentiometric titrations using a Sirius T3 instrument. Log of the distribution coefficient between n-octanol and aqueous buffer at pH 7.4 were determined via potentiometric titrations using a Sirius T3 instrument, except for compounds SM27, SM28, SM30-SM34, SM36-SM39 which had log *D*<sub>7.4</sub> values determined via shake-flask assay. PAMPA assay data includes effective permeability, membrane retention, and log of the apparent permeability coefficient. Permeabilities for compounds `SM33`, `SM35`, and `SM39` were not determined. Compounds `SM35`, `SM36` and `SM37` are enantiopure and have a chiral center. All other compounds are not chiral.

## Experimental details
Compounds were synthesized by the Ballatore Lab at UC San Diego in 1-6 steps and were >95% pure as indicated by NMR and LCMS.
pK<sub>a</sub> measurements were obtained via automated potentiometric titrations using a Sirius T3 instrument (Pion, Inc). Three titrations were performed from pH 1.8 to pH 12.2 using ionic strength adjusted water (0.15 M KCl), acid (0.5 M HCl, 0.15 M KCl) and base (0.5 M KOH, 0.15 M KCl). The pK<sub>a</sub>s of select compounds (Compounds SM30 and SM39) with low aqueous solubility were measured using a cosolvent protocol; Yasuda-Shedlovsky extrapolation method was used to estimate the pK<sub>a</sub> at 0% cosolvent.

Log *P* measurements of compounds with known experimental pK<sub>a</sub> were obtained via potentiometric titrations using a Sirius T3 instrument. Log *D*<sub>7.4</sub> values were extrapolated from the measured log *P*. Compounds with pK<sub>a</sub> > 10 had log *D*<sub>7.4</sub> measured via shake-flask method (shake-flask log *D*<sub>7.4</sub> carried out by Analyza, Inc).

Melting points of the crystalline material were taken using Mel-Temp II (Barnstead Thermolyne). Crystals were grown by slow evaporation in a single solvent (dichloromethane) or by vapor diffusion (hexanes/dichloromethane or dichloromethane/methanol). Intrinsic solubilities were obtained using the experimental log *P* and the melting point via Yalkowski intrinsic solubility equation (log *S* = –log *P* – 0.01 ´ (mp – 25) + 0.5).

Effective permeability (log<sub>*P*<sub>*app*</sub></sub>) was measured by PAMPA using the Corning GentestTM pre-coated PAMPA plate system with quantitation by HPLC-UV (experiments carried out by Analyza, Inc).

## What's here

- [`SAMPL7_molecule_ID_and_SMILES.csv`](SAMPL7_molecule_ID_and_SMILES.csv): A `.CSV` file containing SAMPL7 challenge molecule IDs and SMILES. SMILES were provided by the [Ballatore lab](https://pharmacy.ucsd.edu/faculty/ballatore).
- [`logP/`](logP/): Folder contains an input file in `.CSV` format with SMILES strings of the neutral states of the molecules. This folder contains instructions and a submission template for the logP challenge.
- [`pKa/`](pKa/): Folder contains challenge input files in `.CSV` format with SMILES of enumerated microstates. `.MOL2` and `.SDF` files of each microstate are also provided. This folder contains instructions and a submission template for the pKa challenge. Microstates (tautomers and protomers) were generated with a notebook wich uses RDKit and OpenEye tools. Additional microstates were enumerated using Chemicalize (Chemaxon) and Epik (Schrodinger) and added to the notebook generated `.CSV` files.  
- [`permeability/`](permeability/): Folder contains input files in `.CSV` format with SMILES strings of molecules. This folder contains instructions and a submission template for the permeability challenge.
- [`images/`](images): Folder containing images related to this challenge in PDF and/or JPEG format.
- [`experimental_data/`](experimental_data/): Folder will contain experimental measurements of pK<sub>a</sub>, partitioning, and permeability values after the SAMPL7 challenge submission deadline.

## Publication on experimental measurements
Karol R. Francisco, Thomas J. Paniak, Marisa C. Kozlowski, and Carlo Ballatore. "Structure Property Relationships of N-Acylsulfonamides and Related Bioisosteres" *(Details to be announced)*
