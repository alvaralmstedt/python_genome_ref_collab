#!/bin/python

# To be run in the folder where other folders containing genomes that are downloaded from the NCBI ftp
# Run without the -z flag for just renaming files or with the -z flag to gunzip/guntar and then rename
# The files will be renamed to the folder name it is in and original filename following.
# After running this you can simply do for example cp */*.faa /faafolder to copy the .faa files.

import os
import argparse
import tarfile
import datetime


def concatenate(f_end, folder, namae):
#    lista = os.listdir(".")
    print "inside concatenate"
    if namae.endswith(str(f_end)):
        print str(f_end)
        with open("concat_" + str(folder) + str(f_end), 'a') as outfile:
#            for i in lista:
            print "before if %s" % namae
            if namae.endswith(str(f_end)) and not namae.startswith("concat_"):
                print "line 23"
                with open(namae) as infile:
                    print "line 25, opened"
                    for line in infile.readlines():
                        outfile.write(line)
#                          print line
                    print "%s was written" % outfile

parser = argparse.ArgumentParser()

parser.add_argument("folder", nargs="?", type=str, help='specify folder path, else cwd')
parser.add_argument("-z", "--zip", action="store_true", help='specifies zipped files')
parser.add_argument("-c", "--concat", action="store_true", help="concatenates contigs split into several .faa/.fna files.")

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
            for filnam in os.listdir("."):
                if concat:          # under this should be concatenation code
#                    lista = os.listdir(".")
                    print "inside concat"
                    try:
                        concatenate(".faa", subdir, filnam)
                        concatenate(".fna", subdir, filnam)
                    except:
                        print "file ending not detected. Sorry!"
            os.chdir(str(user_directory) + "/" + str(subdir))
            for filnam in os.listdir("."):
#                print "%s is being renamed to %s" % (filnam, subdir + filnam)
                if not os.path.isfile(str(subdir + filnam)) and not filnam.startswith("concat_"):
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

