#!/bin/bash

# Activate environment (Python 3.7.3)
source activate SAMPL7-PHIP2

# Update requirements
conda list --export > requirements.txt

# Generate user map
#python get_usermap.py
python fix_usermap.py

# Run analysis for stage1 and create collection file
python analyze_stage1.py
