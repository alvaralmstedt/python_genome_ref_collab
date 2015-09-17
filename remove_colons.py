#!/usr/local/opt/bin/python

# This script just removes colons from any filenames in the specified folder. Required for PhyloPhlAn to work.

import argparse
import os
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("path", nargs="?", type=str, help='specify directory path')
args = parser.parse_args()
out = str(args.path) + "/"

file_list = os.listdir(out)

for eachfile in file_list:
    if ":" in eachfile:
        new_file = eachfile.replace(":", "_")
        os.rename(out + eachfile, out + new_file)
        print "%s was renamed to %s" % (eachfile, new_file)

print "Colons removed. Finished at %s" % datetime.datetime.now()
