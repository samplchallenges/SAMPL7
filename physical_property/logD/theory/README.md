# Updated theory

The documents in here were provided by Dhiman Ray, UCI, working in the Mobley Lab in summer, 2021. They lay out the theory for estimating logD given pKa and logP as reported by the Sirius T3 (Pion). Sirius did not provide an adequate explanation of this procedure, but Dhiman was able to work this out and provided these files.

## Manifest:
- `logD_logP_pKa.pdf`: PDF file laying out the relevant derivation/theory
- `logD_logP_pKa.tex`: LaTeX source file for the same
- `logDplot.py`: Python code taking data provided by the Ballatore plot and computing/plotting logD as a function of pH given experimental logP and pKa; this also compares with the logD titration curves in the Sirius reports and shows agreement.
- `LogD_sirius_SMXX.dat`: For all `SMXX` compounds for which logD data is available via Sirius titrations, gives the original source data. These data HAVE been updated to include corrected data from the Ballatore group (as reflected in their erratum)
- `sirius_data.dat`: Contains molecule ID, pKa, log(p0) and log(p1) computed using the Sirius instrument; this includes corrected data from the Ballatore group (as reflected in their erratum)

Note that Sirius (and derived) data files are NOT available for the case of logD values which were derived by shake-flask measurements, so the files presented here only cover 11 compounds. 
