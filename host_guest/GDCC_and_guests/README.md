# The SAMPL7 GDCC Challenge

For SAMPL7, the Gibb group is contributing binding data for eight
guests to two of the Gibb Deep Cavity Cavitand (GDCC) hosts it has frequently studied ---
the familiar "Octa Acid" (OA) host and a newer, *exo*-OA host as detailed below.

## Challenge timing details (preliminary)

The SAMPL7 GDCC challenge is now finalized (as of May 25, 2019) with the details as given below.
The challenge submission deadline is Nov. 1, 2019.

## Proposed challenge for SAMPL7: A Coulombic Challenge

The two hosts shown below, OA (left) and *exo*-OA (right) differ only in the placement of the four water-solubilizing groups.
In the former they are remote from the non-polar pocket, whilst in the latter they are appended directly at the rim of the pocket.

![](../../images/GDCCs.jpg)

The Gibb group will examine the binding of eight guests: four negatively charged, and four positively charged.
As previously, all binding constants will be determined in (10 mM) sodium phosphate buffer, here at pH 11.7.
The guests have been selected to partially overlap with previous determinations for binding to OA (first row of guests; known ITC values to be added to this repository later).
These six examples will act as a reference point for the other determinations.
There will be two new determinations for binding to OA (second row of guests), as well as the eight new determinations using new host exo-OA.
Each of the ten new determinations will be carried out in triplicate using ITC, and where necessary, verified by NMR.

![](../../images/GDCC_guests.jpg)

Given the identity of these guests, we will be able to have *some* overlap between the GDCC guests and those used in the modified cyclodextrin (Gilson lab) and acyclic CB (Isaacs lab) portions of the challenge.

### Additional technical details

Buffer conditions are 10 mM sodium phosphate at pH 11.7. The plan is to gather data in triplicate with fresh solutions of host and guest on each occasion.  Also, all hosts samples are probed by one of either two ways to determine the waters of hydration in each sample.  This can be as high so this analysis is a requirement to avoid bad data.

For positively charged guests, chloride salts are being used.

### Disclaimers

The protonation state of the host may in some cases be not completely certain, and participants are also encouraged to carefully select guest protonation states. Protonation states and conformations may or may not match those of the files provided here.

# What's here

- Hosts: `host_files`: Folder containing PDB, MOL2 and SDF files for the Octa Acid (OA) host and the exo-OA host. Contains the the jupyter notebook used to generate the MOL2 and SDF files of the guests.
- Guests: `guest_files`: Folder containing files for the eight guests, SMILES strings, and the jupyter notebook used to generate PDB, MOL2 and SDF files of the guests.
- Images: `images`: Folder containing images of the guest and host structures for this challenge in PDF format.
- Submission format: `GDCC_submission.txt`: Example submission file (please replace the text and values with your own!) for submitting to our system.

**Source files**:
For this portion of the challenge, the original source files were two (provided) host PDB files from Paolo Suating (in the `host_files` directory) and a `SAMPL7_guests.cdx` file from Bruce Gibb (in the `guest_files` directory). All other files here were derived from those files.
