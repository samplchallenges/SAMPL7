# Updated theory

The documents in here were provided by Dhiman Ray, UCI, working in the Mobley Lab in summer, 2021. They lay out the theory for estimating logD given pKa and logP as reported by the Sirius T3 (Pion). Sirius did not provide an adequate explanation of this procedure, but Dhiman was able to work this out and provided these files.

## Manifest:
- `logD_logP_pKa.pdf`: PDF file laying out the relevant derivation/theory
- `logD_logP_pKa.tex`: LaTeX source file for the same
- `logDplot.py`: Python code taking data provided by the Ballatore plot and computing/plotting logD as a function of pH given experimental logP and pKa; this also compares with the logD titration curves in the Sirius reports and shows agreement. 
