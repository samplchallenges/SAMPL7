# The SAMPL7 protein-ligand challenge

We are excited to announce a new set of SAMPL7 challenges focusing on the binding of small fragment-like molecules to a relatively simple target protein.

The second bromodomain of PHIP (PHIP2)---a small protein for which little small molecule binding data is available---was targeted in an extensive X-ray crystallographic fragment screening experiment, leading to 3D structures of multiple screening hits.
This SAMPL7 challenge will take advantage of this dataset, assessing the accuracy of computational methods for the discrimination of binders from non-binders, binding pose prediction, and the unique opportunity to select new candidate ligands to be screened from a provided set of purchasable compounds that will be assessed experimentally by X-ray crystallography.

This challenge breaks out into at least three stages on a tight timeline:
1) Identification of binders from fragment screening
2) Prediction of fragment binding modes
3) Selection of new compounds for screening from an experimental database

Stage 2 is now open and focuses on identification of binders (Stage 1 is now closed). Unfortunately, the timeline for components 1 and 2 has to be tight given the timeframe for experimental compound screening (Stage 3).

If you plan to participate, please [join our SAMPL7 e-mail list](http://eepurl.com/gpBBun) so we can keep you updated.

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

This project used both the [DSI-Poised fragment library](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Fragment-Libraries/DSI-poised-library.html) an the [Fraglites fragment library](https://pubs.acs.org/doi/abs/10.1021/acs.jmedchem.9b00304), but challenge participants are encouraged to use the provided `fragments_screened.csv` file for the exact chemical identities of compounds screened.

## Overall participation instructions

Instructions on overall participation in this challenge/challenge rules are given in [../protein_ligand_instructions.md](../protein_ligand_instrucitons.md). This document provides challenge details as well as specifics for each stage.

## Stage 1: Discrimination of binders from non-binders at specific sites

### Setup and description of Stage 1

**Aim**: The objective of this first stage is to discriminate fragment binders from non-binders at each of the four sites identified by [PanDDA](https://pandda.bitbucket.io/) (pan-density data analysis), which facilitates the analysis of multiple crystallographic datasets to identify ligand binding sites and structural events.

A total of 799 unique fragments were screened at the [XChem facility](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening.html).
This will be validated by both positive hit data for PHIPA, and negative data where crystals were soaked and screened, but no readout identified binding.
Fragment binding predictions here are important because accurate predictions could improve library design, including the ability to design bespoke libraries for specific targets.

PHIP2 was crystallized in space group C2 at 4C by vapour diffusion in ~230 nL sitting drops, by mixing 100 nL protein (in 10 mM HEPES, 5% glycerol, 500 mM NaCl and 0.5 mM TCEP pH 7.5) with 100 nL reservoir buffer (20% PEG8000 and 0.4 M potassium phosphate) and 30 nL seeds of the same composition.
The final pH was measured to be about 5.6.
The resulting crystals were soaked with 20 mM final concentration of each fragment and 20%(v/v) ethylene glycol, plunged into liquid nitrogen and shot at the i04-1 beamline located at the Diamond Light Source (Harwell, UK).
The diffraction data were analyzed with [PanDDA](https://pandda.bitbucket.io/) ([Pearce et al., 2017](https://www.nature.com/articles/ncomms15123)) which revealed a number of fragments located across four distinct sites.

The first site (denoted by a helium atom `S1` in the provided structure (`PHIPA_C2_apo_sites.pdb`), see Manifest below) is the acetylated lysine binding site which is the most voluminous cavity.
It is located in between the disordered loops at the extremity  of the 4-helix bundle.
The second site (denoted by a neon atom `S2`) is a small pocket located near cysteine 1335.
The third site (denoted by an argon atom `S3`) is solvent exposed and located near Aspartic acid 1384.
The fourth and last site (denoted by a krypton atom `S4`) is also exposed to solvent and located behind a flexible loop near lysine 1399.

An *apo* structure of PHIP2 has been provided (`PHIPA_C2_Apo.pdb`) along with the [isomeric SMILES strings](https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html) (`fragments_screened.csv`) of the fragments screened.

For the purposes of predicting whether a compound binds or not, consider the 20 mM concentration used for soaking fragments; compounds which bind observably at this concentration (after factoring in any applicable solubility issues) will be judged binders, and those which do not will be judged as nonbinders.

We are asking you to submit both site-specific binding predictions (whether each compound binds at each specific site) as well as overall binding predictions (whether each compound binds at all), as detailed in the [submission format](stage1_submission_template.txt). You may elect to assess only binding to one specific site, or to all sites; we plan to analyze predictions for each site separately, as well as overall predictions.

### Provided data for Stage 1
- Apo structure of the protein: See Manifest below
- isomeric SMILES strings for the 799 fragments: See Manifest below
- Descriptions of the candidate binding sites are provided in the description above
- Coordinates of atoms marking the candidate binding sites are provided in the `PHIPA_C2_apo_sites.pdb` file, as described above
- Rules: See below
- Submission format: `stage1_submission_template.txt`

### Rules for Stage 1

**Start date**: Tuesday, October 29, 2019

**Submissions due**: Thursday, Nov. 28, 2019, at midnight (24:00) US Pacific Time

Your predictions must be uploaded via [our web form](http://sampl-submission.us-west-1.elasticbeanstalk.com/submit) before midnight US Pacific time on the due date. The experimental results will be available as soon as possible after SAMPL closes. Please refer to the [../protein_ligand_instructions.md](../protein_ligand_instructions.md) for information on uploading.

You must use the [provided template](stage1_submission_template.txt) to upload your predictions, and the file must have a filename beginning with `PHIP2`. We will be asking you to submit the compound identifier for each compound you predict to bind, along with a designation of which specific sites you predict it to bind to, if you are able to assess binding to specific subsites. Details as to how to submit this information are given in the [format file](stage1_submission_template.txt). Note that each submission must also be accompanied by a variety of methodological details, etc., as given in the submission format. Please refer to the [submission instructions](../protein_ligand_instructions.md) for details on what your method description should contain and how to upload.

While you are welcome to submit multiple entries in order to test diverse methods, as per our [policy on multiple submissions](https://samplchallenges.github.io/roadmap/submissions/), each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form.
We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.

### Manifest for Stage 1
- `fragments_screened.csv`: CSV file containing isomeric SMILES of compounds screened, along with identifiers
- `PHIPA_C2_Apo.pdb`: Structure for use in screening, as provided by XChem
- `PHIPA_C2_apo_sites.pdb`: *Apo* structure with manual addition of noble gas atoms to designate different potential binding sites, as described above (as provided by XChem)
- `stage1_submission_template.txt`: Sample submission format for submitting PHIP2 virtual screening results.

## Stage 2: Prediction of binding poses for binding fragment

### Setup and description of Stage 2

**Aim**: The second part of the SAMPL7 challenge builds onto the first stage. The objective is to correctly predict the binding pose for the protein-fragment complexes identified by [PanDDA](https://pandda.bitbucket.io/). In total, 52 fragments were found to bind to the C2 crystal form described in stage 1. 45 hits were identified at the first site (denoted by a helium atom `S1` in the provided structure (`PHIPA_C2_apo_sites.pdb`)). 4 were found at the second site (denoted by a neon atom `S2`). The third (denoted by an argon atom `S3`) and the fourth site (denoted by a krypton atom `S4`) were each found to bind to a single distinct fragment.

The *apo* structure of PHIP2 that was provided in stage 1 (`PHIPA_C2_Apo.pdb`) may be used along with the [isomeric SMILES strings](https://www.daylight.com/dayhtml/doc/theory/theory.smiles.html) of the fragments identified (`stage2-input-data/site-1_fragment-hits.csv`) to carry out pose predictions, and **must be used to define the frame of reference for your pose predictions**. The acetylated-lysine binding site, being the most populated and pharmacologically relevant, will be the focus of the second stage. Optionally, participants may also try to extend their predictions to the other sites (Site 2:`stage2-input-data/site-2_fragment-hits.csv`, Site 3:`stage2-input-data/site-3_fragment-hits.csv`, Site 4:`stage2-input-data/site-4_fragment-hits.csv`). Other structures and information may also be used in the predictions. However, the predicted protein-ligand poses must be aligned to the reference structure (`PHIPA_C2_Apo.pdb`) for assessment purposes.

Please, note that predictions should be done considering the C2 crystal form and soaking method described in Stage 1. Other structures are available in the PDB but were crystallized in another crystal form. Screening against different crystal forms often leads to differential fragment-hit identification due to solution and solid state effects such as pH and crystal packing. Thus, if you choose to use PDB structures you should pay particular attention to the possibility of such differences.

Here, compound stocks were purchased as as racemic mixes; the higher affinity conformer should be revealed in the electron density. However, the both stereoisomers can also bind the target resulting in an average density. Participants may wish to take this information into account.

### Provided data for Stage 2

- Apo structure of the protein: See Manifest below
- isomeric SMILES strings for the binding fragments for each site: See Manifest below
- Coordinates of atoms marking the binding sites are provided in the `PHIPA_C2_apo_sites.pdb` file, as described above
- Rules: See below
- Submission format: Provided below.
- Submission link: To be provided as soon as available.

### Rules for Stage 2

**Start date:** Friday the 29th of November 2019

**Submissions due:**  Thursday the 12th of December 2019, midnight (24:00) US Pacific time.

In brief, expect to submit a detailed text format method description similar to that used in Stage 1, as well as poses for all of your predicted binders in the same frame of reference as the provided apo structure (`PHIPA_C2_Apo.pdb`), along with the corresponding protein structure for each pose, as further detailed below.

If you choose to use other protein structures other than the provided apo structure in making your predictions, these should be described in your Method description. You may draw on any existing literature data that you wish, just make sure to clearly describe any data utilized in your Methods.

You must predict binding modes for all 45 hits binding in site S1 for your submission to be ranked. Prediction of poses in the alternate sites is optional and pose predictions for alternate sites will be ranked separately for those submissions predicting poses for those compounds.

As in Stage 1, while you are welcome to submit multiple entries in order to test diverse methods, as per our [policy on multiple submissions](https://samplchallenges.github.io/roadmap/submissions/), each participant or organization is allowed only one ranked submission, which must be clearly indicated as such by filling the appropriate field in the submission form.
We also accept non-ranked submissions, which we will not formally judge. These allow us to certify that your calculations were done without knowing the answers, but do not receive formal ranking, as discussed at the link above.

If multiple submissions are incorrectly provided as "ranked" by a single participant, we will judge only one of them; likely this will be the first submitted, but it may be a random submission.

**Submission format**: Your submissions be provided in a single compressed, archived `.tar.gz` file which contains a set of files described below. This file name should have the prefix `PHIP2` followed by a dash or underscore and end with `.tar.gz`. This file should contain a single compressed directory including pose predictions and a completed submission description file named `PHIP2_2-description.txt` based on [our format](stage2_submission_template.txt). This file is used to submit one set of predicted protein-ligand poses, where up to five poses are permitted for each protein-ligand pair (if multiple poses are submitted, your poses are expected to be submitted in ranked order, with pose 1 being the top-scoring pose and pose 5 being the worst scoring pose). Each pose `.tar.gz` file must contain, for each ligand, a minimum of one and up to 5 protein structure PDB files and 5 corresponding ligand poses (in MDL `.mol`, format, `.sdf` format, or `.mol2` format) predicted by a method described in the separately uploaded pose prediction description file.  

**Each pose prediction must be provided in the form of a protein structure PDB file and a corresponding ligand structure file (`.sdf`, `.mol2`, or MDL `.mol`) with all-atom 3D atomic coordinates for the pose, where the coordinates in the protein PDB file and the ligand molfile are in the same frame of reference**. Any ligand coordinates provided in PDB format or included in the protein PDB files will be ignored. You may treat the protein as rigid or flexible, but you must rotationally and translationally superimpose all of your final structure predictions, onto the [reference protein structure provided](PHIPA_C2_Apo.pdb) in the challenge data package in order to facilitate evaluation of your predictions.

The file names of your pose prediction protein PDB and ligand mol files must be constructed as follows:

```
PHIP2-<LigandID>-<poseRank>.pdb
PHIP2-<LigandID>-<poseRank>.mol (or .sdf or .mol2)
```
So for example for ligand F13, you might submit:
- PHIP2-F13-1.pdb
- PHIP2-F13-1.sdf
- PHIP2-F13-2.pdb
- PHIP2-F13-2.sdf
if you were submitting two poses. (The lowest numbered poses will be assumed to be those predicted to be most favorable.) These would be placed into a single directory along with any other files to be submitted (minimally, poses for [all compounds binding in S1](Stage-2-input-data/site-1_fragment_hits.csv)) along with your `PHIP2_2-description.txt` file, then tarred, gzipped, and uploaded to our submission site. An example submission package will be provided.

We anticipate judging poses in two ways -- first, considering only the top-scoring (first) pose from each submission and, second, considering the lowest-RMSD pose out of all submitted poses. These results will be analyzed and presented separately.

If your submissions are incomplete (e.g. you omit required ligands, are missing required files, or do not use the correct frame of reference) we reserve the right not to evaluate them, though we hope our submission system will be able to provide a preliminary assessment of whether we can parse your submissions.

Please do not use negative residue numbers in submitted PDB files, and avoid nonstandard characters in your submitted files.

## Stage 3: Selection of novel binders from a database

### Setup and description of Stage 3

**Aim**: Fragment based-drug design aims to elaborate and/ or merge small drug-like compounds into more potent and specific binders. Data-base mining is an essential part of this process as it enables to identify follow-up compounds based on criteria such as biological activity or chemical synthesizability.

Stage 3 focuses on the selection of fragment follow-up compounds from a database for experimental screening via X-ray crystallography (with potential further validation by ITC). The proposed compounds should bind Site 1 and aim at increasing affinity for the receptor. Participants will be provided with the co-crystal structures of the 52 fragment-protein complexes identified by the method described in Stages 1 and 2. We also provide a compound database (and several subsets) from which compounds must be selected for screening.

For the compound databases, we provide a large compound database (`full.txt`) which consists of more than 40M compounds. We additionally provide several subsets of this database if participants would prefer to work with fewer compounds. Participants may recommend any compound(s) from the full database (or its subsets) for screening.

Our full database is a combination of MolPort ["AllStockCompounds"](https://www.molport.com/shop/database-download) from July 2019 (~7.5M molecules), plus the SUBSET of [Enamine REAL](https://enamine.net/library-synthesis/real-compounds/real-database) that is based around the [DSI-Poised fragment library](https://www.diamond.ac.uk/Instruments/Mx/Fragment-Screening/Fragment-Libraries/DSI-poised-library.html) and is approximately rule of 5 compliant (~40M molecules). All the compounds are purchasable and predicted binders must be selected from these databases.

Subsets of the full database were selected via a fragment network approach, and are provided in case participants prefer to work with smaller numbers of compounds. The fragment network ([Hall, Murray and Verdonk, 2017](https://pubs.acs.org/doi/10.1021/acs.jmedchem.7b00809)) provides a convenient way to filter-out compounds that are dissimilar to the input hit(s). Overall, this search algorithm requires a compound input and 3 parameters: 1- the number of graph traversals (hops), 2- number of changes in heavy atom count (hac), 3- number of changes in ring atoms counts (rac).  Please, read the above reference for the specifics of the methods. Here, 51 hits were used in the query and the resulting files aggregate the results for all query hits (`output-hops[1;4]-hac[3;5]-rac[1;2].txt`). 

Please note that the compound `F763 (O=C1N(CCO)C=CC(Br)=C1)` cannot be found in the aggregated results (`output-hops[1;4]-hac[3;5]-rac[1;2].txt`) because it belongs to the FragLites library which was not included in the initial database refinement.

The participants are asked to submit a ranked list of the top compounds they would recommend for purchase and assay for binding via crystallography. This list must consist of at least 10 compounds, but no more than 100. The number of compounds we actually consider will depend on participation, as explained below. For screening, we will employ the same crystallographic assay used in Stages 1 and 2. Thus, the predictions should take into consideration the associated experimental constraints. In addition, participants will be asked to submit confidence estimates along with their predictions. These may be used to help inform selection of compounds for screening, but also to rank final performance -- methods which predict with high confidence that compounds bind will be penalized more if these compounds do not bind.

**Provided data**:
- Cocrystal structure for each hit
- The full compounds database and various fragment network aggregated results for all hits: see [here](https://zenodo.org/record/3576140#.XfUlXZNKjOQ)

### Rules for Stage 3

**Start date:** Saturday the 14th of December 2019

**Submission due:**  Monday the 13th of January 2020

Predictions must be carried out against Site 1 and should aim at increasing the affinity of the follow-up compound(s) with respect to the original hit(s). The proposed compounds must be members of the database (`full.txt`) for purchase purposes. Participants may or may not choose to use the cocrystal-structures and the subsets generated by the fragment network. They should also keep into consideration the experimental set-up.

Because this challenge involves actually purchasing compounds for experimental screening, we will incur significant costs in the process, so the challenge involves a number of unusual aspects and caveats:
- We reserve the right to decline to purchase compounds proposed by any participant
- Depending on participation numbers, we may be limited in whether we can purchase compounds proposed by all participants
- We expect to likely purchase an upper limit of 50-100 compounds in total for screening, though we are pursuing options that might allow us to expand this number. This means that, in all likelihood, not all proposed compounds will be screened.
- We plan to consider at least the first 10 compounds in each submission for potential screening; depending on participation, our judges may consider additional compounds, but certainly not more than 100 per submission, and we may only consider the first 10 if participation is high.
- Because of compound limits, submissions are restricted:
  - No submissions of null models are allowed
  - No participant may make more than one submission
- We will likely filter submissions prior to compound selection:
  - We plan to have several computational experts read provided method descriptions and ensure the approach applied seems reasonable, well justified, and thoroughly described before selecting compounds for screening.
  - Several chemists will then judge predictions to determine whether, if they were working on this project, they would judge the proposed compounds worth pursuing synthetically for this target, given your provided justification and any proposed rationale or structure activity relationships. (You may address your justification for your choices in your method selection.)
- If participants are concerned about these filtering steps, we are open to partnerships where participants might pay for the purchase of their proposed compounds from Enamine to ensure we screen them.

We encourage participants to submit suggested poses of compounds along with their submitted compound choices, especially when using structure-based methods like docking and MD. While such poses will not be judged, participants are welcome to uses these poses as part of their justification for selecting these compounds. Additionally, SAMPL will be able to verify that these predictions were made in advance of experiment.

**Submission format**: The submission format will be announced shortly.

## Later stages

Depending on the outcome of potential affinity measurements and other details, we may further extend this challenge by adding more stages. This remains to be determined.

## Additional manifest
- `Analysis`: Submissions and analysis for the various challenges
