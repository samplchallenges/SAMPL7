# The SAMPL7 Blind Prediction Challenges for Computational Chemistry
Challenge details, inputs, and (eventually) results for the SAMPL7 series of challenges

See the [SAMPL website](https://samplchallenges.github.io) for information on the Statistical Assessment of the Modeling of Proteins and Ligands (SAMPL) series of challenges as a whole. This repository focuses specifically on the SAMPL7 series of challenges.

Because these files are available publicly, we have no record of who downloads them. Therefore, you should sign up for notifications. Specifically, if you want to receive updates if we uncover any problems, it is imperative that you either (a) sign up for the SAMPL e-mail list via the D3R site, or (b) sign up for notifications of changes to this GitHub repository (the Watch button, above); ideally you would do both.
Join our [SAMPL7 e-mail list](http://eepurl.com/gpBBun) to get e-mails with SAMPL7-related announcements.

## What's here
- [Challenge Overview](#challenge-overview) -- *in progress*
- Preliminary information on host-guest challenge components in the `host_guest` directory.

## What's coming
- Host-guest challenge information (early May 2019)
  - Gibb octa acid-based challenges
  - Isaacs challenge
  - Gilson lab cyclodextrin challenge

## Changes and Data Set Versions

### Release versions

### Changes not in a release

## Challenge overview

(This section under construction)

### Gibb Deep Cavity Cavitand (GDCC) binding of Guests

One host-guest series is based on the Gibb Deep Cavity Cavitands (GDCCs), familiar from SAMPL4-6. However, this challenge we swap one of the hosts; previously, we used octa acid (OA) and tetramethyl octa acid (TEMOA); this challenge revisits OA but also utilizes a variant which changes the location of the carboxylates.  Both were developed in the laboratory of Dr. Bruce Gibb (Tulane U), who will provide binding free energies and enthalpies, measured by ITC. In this case the challenge is to predict binding of eight compounds to TECTA, and two of these to OA; the other six have been studied previously in OA. Existing benchmark datasets based on the OA host may be of interest for those preparing to tackle these new complexes: https://github.com/MobleyLab/benchmarksets; this perpetual review paper also provides a good introduction to the sampling and experimental issues which are known to be relevant in these systems. See the [README on this challenge](host_guest/GDCC_and_guests/README.md) for more details.

## LICENSE

This material here is made available under CC-BY and MIT licenses, as appropriate:
- MIT for all software/code
- CC-BY 4.0 for all other materials
