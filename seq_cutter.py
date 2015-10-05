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
# cwd = os.getcwd() + "/"

# Initialises (creates) files with the correct species filename
def toucher(inpath, outpath, spec):
    infiles = os.listdir(inpath)
    for each_file in infiles:
        with open(inpath + "/" + each_file) as infile:
            for line in infile.readlines():
                if line.startswith(species) and not os.path.isfile(outpath + "/" + spec + ".aln"):
                    subprocess.call(['touch', outpath + "/" + spec + ".aln"])

# Inserts header from the correct species into output file
def headers(sourcepath, destpath):
    infiles = os.listdir(sourcepath)
    outfiles = os.listdir(destpath)
    for namedfiles in outfiles:
        for each_file in infiles:
            with open(sourcepath + "/" + each_file) as infile:
                for line in infile:
                    splitlines = line.split("   ")
                    for word in splitlines:
                        if word.startswith(str(namedfiles)):
                            with open(namedfiles, "a") as destination:
                                destination.write(str(line))

# Inserts the sequences from the correct species into the correct files
def sequences(sourcepath, destpath):
    infiles = os.listdir(sourcepath)
    outfiles = os.listdir(destpath)
    for namedfiles in outfiles:
        for each_file in infiles:
            with open(sourcepath + "/" + each_file) as infile:
                for lines in infile.readlines():
                    if lines.startswith(namedfiles):
                        with open(namedfiles, "a") as destination:
                            subprocess.call(["cut", "-f2", "-d' ", str(lines)], stdout=destination)


if function_to_be_used == "t":
    print "You have selected 'toucher' with paths %s, %s and species %s" % (tabbedpath, comppath, species)
    toucher(tabbedpath, comppath, species)
elif function_to_be_used == "h":
    print "You have selected 'headers' with paths %s and %s" % (tabbedpath, comppath)
    headers(tabbedpath, comppath)
elif function_to_be_used == "s":
    print "You have selected 'sequences' with the paths %s and %s" % (tabbedpath, comppath)
    sequences(tabbedpath, comppath)
else:
    print "Please input which function to use: t = toucher; h = headers; s = sequences"