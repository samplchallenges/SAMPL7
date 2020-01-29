#!/bin/env python

# This script creates separate user map for Stage 1.

import os

print("Creating separate user map files for each stage...")

# Create general output directories for each stage.
for stage_num in [1,2,3]:
    output_directory_path = '../Analysis-outputs-stage' + str(stage_num)
    os.makedirs(output_directory_path, exist_ok=True)

# File paths
input_file = '../SAMPL7-user-map-PL.csv'
stage1_output_file = '../Analysis-outputs-stage1/SAMPL7-user-map-PL-stage1.csv'
stage2_output_file = '../Analysis-outputs-stage2/SAMPL7-user-map-PL-stage2.csv'
stage3_output_file = '../Analysis-outputs-stage3/SAMPL7-user-map-PL-stage3.csv'

# STAGE 1

# Read user map
file = open(input_file, 'r')
text = file.readlines()
file.close()

# Write output files for Stage 1 and add a line for column titles
file = open(stage1_output_file, 'w')
file.write('sid,file_name\n')

# Add only lines of stage 1 submissions: first group of submissions that are .txt files
for line in text:
    file_extension = line[-4:]     
    if file_extension == "txt\n":
        file.write('{}'.format(line))
    else:  # We want to exclude the txt files of Stage 3 submissions which are in the end
        break
file.close()


# STAGE 2

# Read user map
file = open(input_file, 'r')
text = file.readlines()
file.close()

# Write output files for Stage 2 and add a line for column titles
file = open(stage2_output_file, 'w')
file.write('sid,file_name\n')

# Add only lines of stage 1 submissions: first group of submissions that are .txt files
for line in text:
    file_extension = line[-4:]
    if file_extension == "txt\n":
        continue
    else:  # We want to write gz and tar.gz files for 2
        file.write('{}'.format(line))
file.close()


# STAGE 3

# Read user map
file = open(input_file, 'r')
text = file.readlines()
file.close()

# Write output files for Stage 3 and add a line for column titles
file = open(stage3_output_file, 'w')
file.write('sid,file_name\n')

# Add only lines of stage 3 submissions: last of submissions that are .txt files
stage3_lines = []
for line in reversed(text): # Iterate through lines in reverse order
    file_extension = line[-4:]
    if file_extension == "txt\n":
        stage3_lines.append(line)
    else:  # We want to write gz and tar.gz files for 2
        break
for line in reversed(stage3_lines): # Reorder lines before writing output
    file.write('{}'.format(line))
file.close()