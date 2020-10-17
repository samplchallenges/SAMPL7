#!/bin/env python

outfile = '../SAMPL7-user-map-HG.csv'

# Read user map from submission server
file = open('/Users/dmobley/SAMPL/submissions/downloads/submission_table.txt', 'r')
text = file.readlines()
file.close()

# Write output file, removing e-mail addresses
file = open(outfile, 'w')
for line in text:
    tmp = line.split(',')
    file.write(f'{tmp[0].strip()},{tmp[2].strip().replace(" ","_")}\n')
file.close()
