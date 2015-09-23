#!/usr/local/opt/bin/python

# This script takes the contents of all files in a directory and concatenates them into
# a single file


import argparse
import os
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("path", nargs="?", type=str, help='specify directory path')
parser.add_argument("name", nargs="?", type=str, help='specify output filename (whatever you want)')
args = parser.parse_args()

args = parser.parse_args()
out = str(args.path) + "/"
namn = str(args.name)
folder_contents = os.listdir(out)


for each_file in sorted(folder_contents):
    with open(each_file, 'r') as infile:
        with open(namn + str(each_file)[-4:], 'a') as outfile:
            for line in infile.readlines():
                outfile.write(line)

    print '%s has been added to %s at %s' % (each_file, namn + str(each_file)[-4:], datetime.datetime.now())

print "Done"
