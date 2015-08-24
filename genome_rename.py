#!/bin/python

# To be run in the folder where other folders containing genomes that are downloaded from the NCBI ftp
# Run without the -z flag for just renaming files or with the -z flag to gunzip/guntar and then rename
# The files will be renamed to the folder name it is in and original filename following.
# After running this you can simply do for example cp */*.faa /faafolder to copy the .faa files.

import os
import argparse
import tarfile
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("folder", nargs="?", type=str, help='specify folder path, else cwd')
parser.add_argument("-z", "--zip", action="store_true", help='specifies zipped files')
parser.add_argument("-c", "--concat", action="store_true", help="concatenates contigs split into several .faa files")

args = parser.parse_args()

user_directory = args.folder

if user_directory is None:
    user_directory = os.getcwd()

concat = args.concat
zipped = args.zip

if zipped:
    for subdir in os.listdir(user_directory):
        if os.path.isdir(str(user_directory + "/" + subdir)):
            os.chdir(str(user_directory) + "/" + str(subdir))
            for filnam in os.listdir("."):
                if filnam.endswith(".tgz"):
                    tfile = tarfile.open(filnam)
                    tfile.extractall(".")
                    if concat:          # under this should be concatenation code
                        if filnam.endswith(".faa"):
                            with open('./' + "concat_" + str(subdir) + str(filnam), 'w') as outfile:
                                for fname in os.listdir("./" + str(filnam.endswith(".faa"))):
                                    with open(filnam) as infile:
                                        outfile.write(infile.read())
                        elif filnam.endswith(".fna"):
                            with open('./' + "concat_" + str(subdir) + str(filnam), 'w') as outfile:
                                for fname in os.listdir("./" + str(filnam.endswith(".fna"))):
                                    with open(filnam) as infile:
                                        outfile.write(infile.read())
            os.chdir(str(user_directory) + "/" + str(subdir))
            for filnam in os.listdir("."):
                print "%s is being renamed to %s" % (filnam, subdir + filnam)
                os.rename(filnam, subdir + filnam)
                os.chdir("..")
        else:
            print "%s is a file, continuing..." % subdir
else:
    for subdir in os.listdir(user_directory):
        if os.path.isdir(str(user_directory + "/" + subdir)):
            os.chdir(str(user_directory) + "/" + str(subdir))
            for filnam in os.listdir("."):
                if not filnam.endswith(".tgz"):
                    os.rename(filnam, subdir + filnam)

print "done at %s" % datetime.datetime.now()

