#!/usr/local/opt/bin/python

import argparse
import os
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("path", nargs="?", type=str, help='specify directory path')
args = parser.parse_args()

args = parser.parse_args()
out = str(args.path) + "/"

folder_contents = os.listdir(out)

for each_file in folder_contents:
    with open(each_file, 'r') as infile:
        with open('concatenation' + "_" + str(each_file), 'a') as outfile:
            for line in infile.readlines():
                outfile.write(line)

    print '%s has been added at %s' % (each_file, datetime.datetime.now())

print "Done"
