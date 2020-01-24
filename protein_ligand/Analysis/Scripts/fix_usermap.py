#!/bin/env python

input_file = '../SAMPL7-user-map-PL.csv'
output_file = '../SAMPL7-user-map-PL-stage1.csv'

# Read user map
file = open(input_file, 'r')
text = file.readlines()
file.close()


# Write output file and add a line for column titles
file = open(output_file, 'w')
file.write('sid, file_name\n')

for line in text:
    file.write('{}'.format(line))
file.close()

