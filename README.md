# The SAMPL7 Blind Prediction Challenges for Computational Chemistry
Challenge details, inputs, and (eventually) results for the SAMPL7 series of challenges

See the [SAMPL website](https://samplchallenges.github.io) for information on the Statistical Assessment of the Modeling of Proteins and Ligands (SAMPL) series of challenges as a whole. This repository focuses specifically on the SAMPL7 series of challenges.

Because these files are available publicly, we have no record of who downloads them. Therefore, you should sign up for notifications. Specifically, if you want to receive updates if we uncover any problems, it is imperative that you either (a) sign up for the SAMPL e-mail list via the D3R site, or (b) sign up for notifications of changes to this GitHub repository (the Watch button, above); ideally you would do both.
Join our [SAMPL7 e-mail list](http://eepurl.com/gpBBun) to get e-mails with SAMPL7-related announcements.

## What's here
- [Challenge Overview](#challenge-overview)
- Final information on the TrimerTrip host-guest challenge components in the `host_guest/Isaacs_clip` directory.
- Final information on the Gibb octa acid-based challenge ("Gibb deep cavity cavitand" (GDCC) challenge) in the `host_guest/GDCC_and_guests` directory.
- Final information on the cyclodextrin derivatives challenge in the `host_guest/cyclodextrin_derivatives` directory and in our [host-guest challenge description](host_guest_description.md).
- Experimental details for the CD challenge in [host_guest_description.md](host_guest_description.md)

All three host-guest components of this challenge are now final and launched, though additional supporting files may be added at a later date.

## What's coming
- Host-guest challenge
  - Possibly parameterized systems
  - Submission file formats
- GSK logD challenge information as soon as available

## Changes and Data Set Versions

### Release versions

### Changes not in a release
There are no formal releases yet, so here we only note particularly important changes. 
- **Critical bug**: Isaacs/TrimerTrip guest `g15` had an incorrect SMILES string as originally provided. This was corrected in the provided input files on July 18, 2019.
- **Finalized systems**: Finalized details of TrimerTrip hosts from Lyle Isaacs, July 22, 2019. Materials added this date included several modifications to which guests are being considered relative to what had been provided earlier. GDCC and cyclodextrin challenges were finalized at an earlier date.
- **Critical bug**: Isaacs/TrimerTrip host draft 3D structure files (mol2, sdf, PDB) had incorrect host due to a bond perception error in generating the files initially.
- **Critical bug**: Cyclodextrin hosts 9, 24 and 36 had incorrect starting PDB files (and thus host mol2/sdf files as well) due to errors in their construction in the Gilson lab. 2D structures of these compounds were correct, however. This has now been fixed.

## Challenge overview

The SAMPL7 phase of challenges currently includes host-guest binding on three systems: A pair of Gibb Deeep Cavity Cavitands (GDCCs), a new "TrimerTrip" molecule from Lyle Isaacs and his group, and a series of cyclodextrin derivatives from Mike Gilson's group. Each host binds one or more guests, and each system involves a total of 9-20 binding free energy calculations.
Additional details are provided below.

A later phase of SAMPL7 is expected to include logD prediction (hopefully with pKa values provided) for a series of small moleculs in several solvents; data is currently being collected in partnership with GSK.

### Gibb Deep Cavity Cavitand (GDCC) binding of guests

One host-guest series is based on the Gibb Deep Cavity Cavitands (GDCCs), familiar from SAMPL4-6. However, this challenge we swap one of the hosts; previously, we used octa acid (OA) and tetramethyl octa acid (TEMOA); this challenge revisits OA but also utilizes a variant which changes the location of the carboxylates.  Both were developed in the laboratory of Dr. Bruce Gibb (Tulane U), who will provide binding free energies and enthalpies, measured by ITC. In this case the challenge is to predict binding of eight compounds to *exo*-OA (a new host created and studied by the Gibb group and first disclosed in this challenge), and two of these to OA; the other six have been studied previously in OA. Existing benchmark datasets based on the OA host may be of interest for those preparing to tackle these new complexes: https://github.com/MobleyLab/benchmarksets; this perpetual review paper also provides a good introduction to the sampling and experimental issues which are known to be relevant in these systems. See the [README on this challenge](host_guest/GDCC_and_guests/README.md) for more details.

### Modified acyclic cucurbituril (TrimerTrip) binding of guests

The Isaacs lab is contributing data on binding of a series of guests to an acyclic cucubituril host, codenamed "TrimerTrip", as detailed in `host_guest/Isaacs_clip` tentatively. Guest selection is still being finalized to ensure good dynamic range, but it will likely include compounds which overlap with the GDCC and cyclodextrin-derivative challenges, with a total of roughly ten complexes being examined.

### The cyclodextrin derivatives challenge

The Gilson lab is measuring binding of two guests to ten different hosts, comprising beta-cyclodextrin as well as nine different cyclodextrin derivatives which have a single functional group added at one location around the rim of the cavity. Binding is being characterized via ITC and NMR. The two guest compounds (R-rimantadine and trans-4-methylcyclohexanol) overlap with those used in the TrimerTrip and GDCC challenges. [Full details](host_guest_description.md) are available.

## LICENSE

This material here is made available under CC-BY and MIT licenses, as appropriate:
- MIT for all software/code
- CC-BY 4.0 for all other materials
