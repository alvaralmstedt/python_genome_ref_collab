#!/usr/local/opt/bin python2.7

# To be run in the folder where other folders containing genomes that are downloaded from the NCBI ftp
# Run without the -z flag for just renaming files or with the -z flag to gunzip/guntar and then rename
# The files will be renamed to the folder name it is in and original filename following.
# After running this you can simply do for example cp */*.faa /faafolder to copy the .faa files.

import os
import argparse
import tarfile
import datetime


def concatenate(f_end, folder, namae):
    if namae.endswith(str(f_end)):
        print str(f_end)
        with open(str(folder) + ".concat" + str(f_end), 'a') as outfile:
            print "before if %s" % namae
            completed = False
            if namae.endswith(str(f_end)) and ".concat." not in namae:
                with open(namae) as infile:
                    for line in infile.readlines():
                        outfile.write(line)
                    print "%s was written" % outfile
                    completed = True
            if completed:
                os.remove(str(namae))
parser = argparse.ArgumentParser()

parser.add_argument("folder", nargs="?", type=str, help='specify folder path where genome folders are located, else cwd')
parser.add_argument("-z", "--zip", action="store_true", help='specifies zipped files')
parser.add_argument("-c", "--concat", action="store_true", help="concatenates contigs split into several .faa/.fna/etc. files.")

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
            if concat:      # under this should be concatenation code
                for filnam in os.listdir("."):      # if & for here switched place. change back if broken
                    try:
                        concatenate(".faa", subdir, filnam)
                        concatenate(".fna", subdir, filnam)
                        concatenate(".gbk", subdir, filnam)
                        concatenate(".ffn", subdir, filnam)
                        concatenate(".asn", subdir, filnam)
                        concatenate(".rpt", subdir, filnam)
                        concatenate(".gbs", subdir, filnam)
                        concatenate(".gff", subdir, filnam)
                        concatenate(".val", subdir, filnam)
                        concatenate(".ptt", subdir, filnam)
                        concatenate(".frn", subdir, filnam)
                        concatenate(".rnt", subdir, filnam)
                    except:
                        print "file ending not detected. Sorry!"
            os.chdir(str(user_directory) + "/" + str(subdir))
            for filnam in os.listdir("."):
                if not os.path.isfile(str(subdir + filnam)) and ".concat." not in filnam:
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
            if concat:
                for filnam in os.listdir("."):
                    try:
                        concatenate(".faa", subdir, filnam)
                        concatenate(".fna", subdir, filnam)
                        concatenate(".gbk", subdir, filnam)
                        concatenate(".ffn", subdir, filnam)
                        concatenate(".asn", subdir, filnam)
                        concatenate(".rpt", subdir, filnam)
                        concatenate(".gbs", subdir, filnam)
                        concatenate(".gff", subdir, filnam)
                        concatenate(".val", subdir, filnam)
                        concatenate(".ptt", subdir, filnam)
                        concatenate(".frn", subdir, filnam)
                        concatenate(".rnt", subdir, filnam)
                    except:
                        print "File ending not detected. Concatenation aborted. Sorry!"
print "done at %s" % datetime.datetime.now()

