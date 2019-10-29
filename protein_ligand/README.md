# The SAMPL7 protein-ligand challenge

We are excited to announce a new set of SAMPL7 challenges focusing on the binding of small fragment-like molecules to a relatively simple target protein.

The second bromodomain of PHIP (PHIP2)---a small protein for which little small molecule binding data is available---was targeted in an extensive X-ray crystallographic fragment screening experiment, leading to 3D structures of multiple screening hits.
This SAMPL7 challenge will take advantage of this dataset, assessing the accuracy of computational methods for the discrimination of binders from non-binders, binding pose prediction, and the unique opportunity to select new candidate ligands to be screened from a provided set of purchasable compounds that will be assessed experimentally by X-ray crystallography.

This challenge breaks out into at least three phases on a tight timeline:
1) Identification of binders from fragment screening
2) Prediction of fragment binding modes
3) Selection of new compounds for screening from an experimental database

Phase 1 is now open and focuses on identification of binders. Unfortunately, the timeline for components 1 and 2 has to be tight given the timeframe for experimental compound screening (Phase 3).

If you plan to participate, please [join our SAMPL7 e-mail list](https://drugdesigndata.us19.list-manage.com/subscribe?u=8181f49f8d2daca876bc86225&id=44c32db76e) so we can keep you updated.

## System background

The [Pleckstrin homology domain interacting protein (PHIP)](https://www.uniprot.org/uniprot/Q8WWQ0) is a multidomain protein that is involved in important cellular processes such as cytoskeletal organization, cell division and its deregulation was found to be involved in melanoma.
Two of PHIP’s domains are [bromodomains](https://en.wikipedia.org/wiki/Bromodomain), which are known to bind acetylated lysines.
These post-translationally modified protein residues can be found on the N-terminal tails of histones and mediate the regulation of gene expression.
Bromodomains are attractive targets and several drugs are currently in clinical trials.

X-ray crystallographic fragment screening experiments involve the [soaking of protein crystals with small fragment molecules](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Methods-for-Fragment-Screening.html) (<250 Da) into an apo crystal, followed by high-throughput automated X-ray crystallography and structure solution.
This enables the identification of binders while providing high resolution structural information.
Such experiments are now feasible in a high-throughput fashion thanks to infrastructures such as [XChem](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html) where hundreds of crystals can be soaked and shot within a day.

The [second bromodomain of PHIP (PHIP2)](https://www.uniprot.org/uniprot/Q8WWQ0#family_and_domains) was utilized as target at [XChem](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html) and a number of fragment hits were identified.
This unpublished dataset offers an opportunity to computational chemists and biochemists to test their predictive methods in a blind trial focused on protein-fragment complexes.
This edition of the SAMPL challenge will be divided into at least three stages.

## Fragment screening at XChem

This challenge is made possible through an exciting new collaboration with the [XChem fragment screening facility / Macromolecular Crystallography (MX) program](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html) at the [Diamond Light Source](https://www.diamond.ac.uk/Home.html), with special thanks to [Harold Grosjean (Oxford)](https://www.linkedin.com/in/harold-grosjean-992741a8?originalSubdomain=uk), [Rachel Skyner (Diamond)](https://scholar.google.com/citations?user=qC2iEdMAAAAJ&hl=en), [Tobias Krojer (SGC Oxford)](https://thesgc.org/groupprofile/9489), and [Frank von Delft (SGC Oxford / Diamond)](https://www.thesgc.org/node/9489).
The XChem fragment screening facility and Macromolecular Crystallography (MX) program at Diamond offer the ability to perform [high-throughput crystal soaking experiments](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html) of several [fragment libraries](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html), and allow [both academic and industry groups](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Applying-for-XChem.html) to utilize their resources to advance drug discovery and the design of new chemical probes.
Academic groups can apply for access via a simple [two-page proposal](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Applying-for-XChem/Standard-access.html).

To get an idea for what existing XChem fragment screening datasets look like, you can use the [XChem Fragalysis browser](https://fragalysis.diamond.ac.uk) to interactively view fragment hits, or browse [all datasets available on Zenodo](https://zenodo.org/search?page=1&size=20&q=keywords:%22PanDDA%22) (example [here](https://zenodo.org/record/1244111#.XbiAzJNKiL4)).
XChem also provides a [detailed overview of their fragment screening methods](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Methods-for-Fragment-Screening.html) and [available fragment libraries](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html).

This project used both the [DSI-Poised fragment library](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Fragment-Libraries/DSI-poised-library.html) an the [Leeds Fraglites fragment library](https://pubs.acs.org/doi/abs/10.1021/acs.jmedchem.9b00304), but challenge participants are encouraged to use the provided `fragments_screened.csv` file for the exact chemical identities of compounds screened.

## Phase 1: Discrimination of binders from non-binders at specific sites

### Setup and description of Stage 1

**Aim**: The objective of this first stage is to discriminate fragment binders from non-binders at each of the four sites identified by [PanDDA](https://pandda.bitbucket.io/).

A total of 799 unique fragments were screened at the [XChem facility](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html).
This will be validated by both positive hit data for PHIPA, and negative data where crystals were soaked and screened, but no readout identified binding.
Fragment binding predictions here are important because accurate predictions could improve library design, including the ability to design bespoke libraries for specific targets.

Overall, PHIP2 was crystalized in a C2 space group at 4°C with 20% PEG8000 and 0.04 M monobasic potassium phosphate.
The resulting crystals were soaked with 20 mM final concentration of each fragment, plunged into liquid nitrogen and shot at the i04-1 beamline located at the Diamond Light Source (Harwell, UK).
The diffraction data were analyzed with [PanDDA](https://pandda.bitbucket.io/) ([Pearce et al., 2017](https://www.nature.com/articles/ncomms15123)) which revealed a number of fragments located across four distinct sites.

The first site (denoted by a helium atom `S1` in the provided structure (`PHIPA_C2_apo_sites.pdb`), see Manifest below) is the acetylated lysine binding site which is the most voluminous cavity.
It is located in between the disordered loops at the extremity  of the 4-helix bundle.
The second site (denoted by a neon atom `S2`) is a small pocket located near cysteine 1335.
The third site (denoted by an argon atom `S3`) is solvent exposed and located near Aspartic acid 1384.
The fourth and last site (denoted by a krypton atom `S4`) is also exposed to solvent and located behind a flexible loop near lysine 1399.

An *apo* structure of PHIP2 has been provided (`PHIPA_C2_Apo.pdb`) along with the [isomeric SMILES strings](https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html) (`fragments_screened.csv`) of the fragments screened.

For the purposes of predicting whether a compound binds or not, consider the 20 mM concentration used for soaking fragments; compounds which bind observably at this concentration (after factoring in any applicable solubility issues) will be judged binders, and those which do not will be judged as nonbinders.

### Provided data for Stage 1
- Apo structure of the protein: See Manifest below
- isomeric SMILES strings for the 799 fragments: See Manifest below
- Descriptions of the candidate binding sites are provided in the description above
- Coordinates of atoms marking the candidate binding sites are provided in the `PHIPA_C2_apo_sites.pdb` file, as described above
- Rules: See below
- Submission format: To be posted shortly

### Rules for Stage 1

**Start date**: Tuesday, October 29, 2019

**Submissions due**: Thursday, Nov. 28, 2019, at midnight US Pacific Time

Your predictions must be uploaded via our web form (to be linked from here as soon as it is available) before midnight US Pacific time on the due date. The experimental results will be available as soon as possible after SAMPL closes. Please refer to the below instructions for information on uploading.

You must use the provided templates (to be posted shortly) to upload your predictions. We will be asking you to submit the SMILES string and compound identifier for each compound you predict to bind, and similarly for each compound you predict *not* to bind.

While you are welcome to submit multiple entries in order to test diverse methods, as per our [policy on multiple submissions](https://samplchallenges.github.io/roadmap/submissions/), each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form.
We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.

### Manifest for Stage 1
- `fragments_screened.csv`: CSV file containing isomeric SMILES of compounds screened, along with identifiers
- `PHIPA_C2_Apo.pdb`: Structure for use in screening, as provided by XChem
- `PHIPA_C2_apo_sites.pdb`: *Apo* structure with manual addition of noble gas atoms to designate different potential binding sites, as described above (as provided by XChem)

## Stage 2: Prediction of binding poses for binding fragment

Plans for stage 2 are still being finalized, but this is planned to involve predicting the bound structures of the compounds which bind, the identity of which will be released at the end of the first stage.

**Start date:** Friday the 29th of November 2019

**End date:**  Thursday the 12th of December 2019

## Stage 3: Selection of novel binders from a database

Plans for Stage 3 are still being finalized. However, a brief summary follows below, which will be updated as plans are solidified.

**Aim**: The third stage of the SAMPL7 challenge will offer the unique opportunity to select new candidate ligands from a database of purchasable compounds. Cocrystal structures will have been released at the end of Stage 2, allowing participants to exploit that information to predict which new compounds bind to the target as well as their associated binding modes. Selected proposed ligands will be validated experimentally by X-ray crystallography at the Diamond Light Source using the C2 crystal form described in stage 1, but the number of ligands from each submission which are tested will depend on participation numbers.

Crystallography will be used to assay compounds for activity. Follow-up compounds should aim to improve biding and/or (predicted) potency from the hit they originated from.

**Provided data**: Cocrystal structures, list of candidate compounds, possibly directing participants to predict binders to the main binding site of interest, rules for stage 3 of the challenge, and submission instructions.

**Start date:** Friday the 13th of December 2019

**End date:**  Monday the 13th of January 2020

## Later stages

Depending on the outcome of potential affinity measurements and other details, we may further extend this challenge by adding more stages. This remains to be determined.
