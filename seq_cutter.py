#!/usr/local/opt/bin/python

import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser .add_argument("fun", nargs="?", type=str, help='function to be run')
parser.add_argument("completedpath", nargs="?", type=str, help='species name')
parser.add_argument("tabpath", nargs="?", type=str, help='species name')
parser.add_argument("species", nargs="?", type=str, help='species name goes here')

args = parser.parse_args()

function_to_be_used = str(args.fun)
comppath = str(args.completedpath)
tabbedpath = str(args.tabpath)
species = str(args.species)

# Initialises files with the correct species filename
def toucher(inpath, outpath, spec):
    infiles = os.listdir(inpath)
    for each_file in infiles:
        with open(each_file) as infile:
            for lines in infile.readlines:
                if lines.startswith(species) and not os.path.isfile(outpath + "/" + spec + ".aln"):
                    subprocess.call(['touch', outpath + "/" + spec + ".aln"])

# Inserts header from the correct species into output file
def headers(sourcepath, destpath):
    infiles = os.listdir(sourcepath)
    outfiles = os.listdir(destpath)
    for namedfiles in outfiles:
        for each_file in infiles:
            with open(each_file) as infile:
                for lines in infile.readlines():
                    lines = lines.split("   ")
                    if lines.startswith(str(namedfiles)):
                        with open(namedfiles, "a") as destination:
                            destination.write(str(lines))

# Inserts the sequences from the correct species into the correct files
def sequences(sourcepath, destpath):
    infiles = os.listdir(sourcepath)
    outfiles = os.listdir(destpath)
    for namedfiles in outfiles:
        for each_file in infiles:
            with open(each_file) as infile:
                for lines in infile.readlines():
                    if lines.startswith(namedfiles):
                        with open(namedfiles, "a") as destination:
                            subprocess.call(["cut", "-f2", "-d' ", str(lines)], stdout=destination)


if function_to_be_used == "t":
    toucher(tabbedpath, comppath, species)
elif function_to_be_used == "h":
    headers(tabbedpath, comppath)
elif function_to_be_used == "s":
    sequences(tabbedpath, comppath)
else:
    print "Please input which function to use: t = toucher; h = headers; s = sequences"