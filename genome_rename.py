#!/bin/python

import os
import argparse
import tarfile
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("folder", nargs="?", type=str, help='specify folder path, else cwd')


args = parser.parse_args()

base_dir = args.folder()

for subdir in os.listdir(base_dir):
    if os.path.isdir(subdir):
        os.chdir(str(base_dir) + "/" + str(subdir))
        for filnam in os.listdir("."):
            os.rename(filnam, subdir + filnam)
            tarfile.open(subdir + filnam)
            tarfile.extractall(".")
        os.chdir("..")
    else:
        print "%s is a file, continuing..." % subdir

print "done at %s" % datetime.datetime.now()

