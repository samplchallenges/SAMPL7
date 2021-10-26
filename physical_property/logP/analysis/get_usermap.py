#!/bin/env python

outfile = '../SAMPL7-user-map-logP.csv'

# Read user map from submission server
file = open('/Users/dmobley/github/SAMPL-submission-systems/SAMPL-submission-handling-shared/submissions/downloads/submission_table.txt', 'r')
text = file.readlines()
file.close()

# Write output file, removing e-mail addresses
file = open(outfile, 'w')
for line in text:
    tmp = line.split(',')
    if 'LOGP' in tmp[2].upper():
        file.write(f'{tmp[0].strip()},{tmp[2].strip().replace(" ","_")}\n')
file.close()
