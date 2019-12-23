#!/bin/env python

outfile = '../SAMPL7-user-map-PL.csv'

# Read user map from submission server
file = open('/Users/dmobley/github/SAMPL7-submission-handling/submissions/downloads/submission_table.txt', 'r')
text = file.readlines()
file.close()

# Write output file, removing e-mail addresses and keeping only PHIP2 submissions
file = open(outfile, 'w')
for line in text:
    if 'PHIP2' in line:
        tmp = line.split(',')
        file.write(f'{tmp[0].strip()},{tmp[2].strip().replace(" ","_")}\n')
file.close()
