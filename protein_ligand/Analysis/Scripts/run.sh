#!/bin/bash

# Activate environment (Python 3.7.3)
source activate SAMPL7-PHIP2

# Update requirements
conda list --export > requirements.txt

# Generate user map
#python get_usermap.py
python create_separate_usermaps.py

# Run analysis for stage1 and create collection file
python analyze_stage1.py


# Compile LaTeX statistic table for each directory
for i in ../Analysis-outputs-stage1/*/*/StatisticsTables/statisticsLaTex/; do cd $i; pdflatex statistics.tex; rm statistics.aux;cd -; done

# Run analysis for stage2 and create collection file
python analyze_stage2.py

# Run analysis for stage3 and create collection file
python analyze_stage3.py