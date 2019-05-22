README.md# The SAMPL7 Cyclodextrin Derivatives Challenge

For SAMPL7, the Gilson group is contributing binding data for two hosts (r-rimantadine and trans-4-methylcyclohexanol) binding to beta-cyclodextrin as well as eight novel cyclodextrin derivatives synthesized by Gilson postdoc Katy Kellett.

## Challenge overview

The challenge consists of predicting binding free energies of two guests to the series of modified cyclodextrin hosts shown below.

![](images/sampl_host_structures_coded.jpg)

![](images/R_rimantadine.jpg)

Above, R-rimantadine

![](images/trans_4_methylcyclohexanol.png)

Above, trans-4-methylcyclohexanol

We plan to separately analyze submissions predicting absolute binding free energies of individual guests to individual hosts, and predictions of relative binding free energies of a single guest to a series of hosts.

## Challenge timing details (preliminary)

Dr. Kellett has finished the ITC data collection on guest binding. Participants may begin their calculations (though we will be preparing additional structures/inputs for those who would like additional file formats) and submissions will be allowed as soon as our submission system is online. The challenge is expected to run through August, 2019, with experimental results released at that time. (The formal submission deadline will be announced soon.)

## Background information

This section is under construction and will provide background details on these systems in the near future.


### Additional technical details

Binding in all systems was assayed in 25 mM pH 6.8 sodium phosphate buffer at 27 Celsius. All systems exhibit 1:1 binding except that one may end up being a nonbinder. NMR is being done in the hopes of assessing the preferred orientation of the bound guests.
Compounds exhibiting strange binding patterns have already been removed prior to construction of this set.

# What's here

- Hosts: `hosts`: Folder containing beta cyclodextrin plus the nine other cyclodextrin derivative hosts, provided by Katy Kellett and Michael Gilson, initially only in PDB format with all protons present.
- Guests: `guests`: Initially containing only names/SMILES strings of guests, but to be expanded with `mol2`/`sdf` files additionally.
