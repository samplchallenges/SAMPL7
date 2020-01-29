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


# Compile LaTeX statistic table twice for better rendering
pdflatex ../Analysis-outputs-stage1/StatisticsTables/statisticsLaTex/statistics.tex
pdflatex ../Analysis-outputs-stage1/StatisticsTables/statisticsLaTex/statistics.tex

rm statistics.log
rm statistics.aux
rm texput.log
mv statistics.pdf ../Analysis-outputs-stage1/StatisticsTables/