#!/usr/bin/python

# Written by: Alvar Almstedt

import argparse
import os
import re
import urllib
import ftplib
import datetime
import signal

directories = []


class TimeoutException(Exception):  # Custom exception class
    pass


def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


# Changes the behavior of the SIGLARM
signal.signal(signal.SIGALRM, timeout_handler)


def testifDirectory(ftp, filenames):
    # put whatever you want to do in each directory here
    # when you have called testifDirectory with a file,
    # the command above will fail and you will return



    # get the files and directories contained in the current directory
    #    filenames = []
    #    ftp.retrlines('NLST',filenames.append)
    for name in filenames:
        signal.alarm(10)  # alarm is rung after 10 seconds
        try:
            if name != "all":
                ftp.cwd(name)
                directories.append(name)
                print name
                if name == "CLUSTERS":
                    ftp.cwd("/genomes/Bacteria")
                else:
                    ftp.cwd('..')
        except ftplib.error_perm:
            print "%s is not a directory, continuing" % name
            continue
        except TimeoutException:
            print "%s caused a timeout after 10 seconds" % name
            continue
        else:
            signal.alarm(0)  # resets alarm
            # put whatever you want to do after processing the files
            # and sub-directories of a directory here


def download(folder, filenames, outputfolders):
    local_filename = os.path.join(outputfolders + str(folder), str(filenames))
    lf = open(str(local_filename), "wb")
    ftp.retrbinary('RETR %s' % filenames, lf.write)
    lf.close()

# assigns argument variable
parser = argparse.ArgumentParser()

# argparse explanations: https://infohost.nmt.edu/tcc/help/pubs/python/web/argparse-add_argument.html
# adds arguments to the magic "parser" variable
parser.add_argument("taxlistpath", nargs="?", type=argparse.FileType('r'), help='path to your list')
parser.add_argument("output", nargs="?", type=str, help='specify output path, else cwd')
parser.add_argument("ftpurl", nargs="?", action='store', type=str, help='specify top level ftp url to search down from')

# parser.add_argument("-f", "--family", action="store_true", help='organism family to download genomes from')
# parser.add_argument("-p", "-phylum", action="store_true", help='phyla to download genomes from')
# parser.add_argument("--fna", action="store_true", help='download .fna files')
# parser.add_argument("--faa", action="store_true", help='download .faa files')
# parser.add_argument("-a", "-all", action="store_true", help='download all files')
# parser.add_argument("-d", "--draft", action="store_true", help='will also look among draft genomes')


# returns the arguments given to the "args" variable
args = parser.parse_args()

# makes a the text list into a python list
taxlist = args.taxlistpath.read().splitlines() # this should be a capitalised list of species genus
out = str(args.output) + "/"

# replies with specified output path, otherwise defaults to cwd
if out is not None:
    print "output path is: " + out
else:
    out = str(os.getcwd() + "/")
    print "Your output path was defaulted to cwd:\n %s" % out

print "Your list: "
print taxlist
print "\n"

# Checks for Candidatus genus species in user list
for name in taxlist:
    if name == "Candidatus":
        prompt = raw_input("Your list contains the name 'Candidatus'. Are you sure you want to download genomes with this genus? y/n")
        if prompt == "n" or prompt == "N" or prompt == "no" or prompt == "NO":
            print "Your response was %s. Skipping 'Candidatus'." % prompt
            taxlist.remove("Candidatus")
        else:
            print "Your response was %s. 'Candidatus' genomes will be downloaded."

ftpurl = args.ftpurl
ftpurl = str(ftpurl)
print "Will search from %s" % ftpurl

# this connects to the ncbi ftp server and enters the "genomes" directory
ftp = ftplib.FTP("ftp.wip.ncbi.nlm.nih.gov")
ftp.login()

# This will read the input url so that it is able to index and download from different places on the ftp
if ftpurl is not None:
    if ftpurl[-9:] == "/genomes/":
        ftp.cwd("genomes")
    elif ftpurl[-9:] == "Bacteria/":
        ftp.cwd("genomes")
        ftp.cwd("Bacteria")
    elif ftpurl[-9:] == "ia_DRAFT/":
        ftp.cwd("genomes")
        ftp.cwd("Bacteria_DRAFT")
    elif ftpurl[-9:] == "es/Fungi/":
        ftp.cwd("genomes")
        ftp.cwd("Fungi")
    else:
        print "Url mismatch detected, defaulting to searching in /genomes/"
        ftp.cwd("genomes")
else:
    print "No url detected, defaulting to searching in /genomes/"
    ftp.cwd("genomes")

# print ftp.retrlines('LIST')

# this line converts the genomes directory into a list
# ftplist = ftp.nlst()
# ftplist = sorted(ftplist, key=str.lower)

# print ftplist

print "\n"

ftp.set_debuglevel(0)
counter = 0

files = []

ftpdir = ftp.retrlines('NLST', files.append)
# ftpdir = ftpdir.splitlines()

# print ftpdir
print "before for-loop"

# First try on directory checking, is a lot faster than the current one but works really poorly:
#
# for r in files:
#    print "alvar " + r + "\n"
#    if r.upper().startswith('D'):
#        print "found directory: " + r[56:]  #slice 56 is for taking only the folder name from the filelist
#        if r[56:] != "all" and r[56:] != "3 all":
#            stripped = r[56:].strip()
#            directories.append(stripped)

files.sort()
testifDirectory(ftp, files)

print directories.sort()

# this dict will contain all directories in genomes as keys and lists of their contents as values
genome_subfolders = {}

for i in directories:
    signal.alarm(30)
    try:
        if i != "CLUSTERS":
            ftp.cwd(i)
            subfolder = ftp.nlst()
            print "indexing %s at time: %s" % (i, datetime.datetime.now())
            genome_subfolders[i] = subfolder
            ftp.cwd('..')
            counter += 1
    #        if counter > 6:  # temporary counter to limit testing time
    #            break
    except TimeoutException:
        print "Timed out after 30 seconds, continuing"
        continue
    else:
        # Resets alarm
        signal.alarm(0)
print "printing genome_subfolders"
print genome_subfolders
# print directories

print "starting search"

pwd = ftp.pwd()
# This will iterate over the keys in genome_subfolders dict and match to user provided taxlist

lstnam = []
filnam = ""


# Download loop. Matches folder names that starts with user-provided taxlist names and
# tries to download the contents of the folder. Will also try to download directories, however.
# I may put this into a function later so that some variables can be altered.
# So far it only matches to folders in the base genomes/ directory.

iteration = 0
iteration2 = 0
for key in genome_subfolders.keys():
    for tax in taxlist:
        if key.startswith(tax):
            iteration2 = 0
            print "%s WAS found in %s" % (tax, key)
            for fil in genome_subfolders[key]:
                try:
                    if not os.path.exists(out + str(key)):
                        print "creating directory: %s" % (out + str(key))
                        os.makedirs(out + str(key))
                    try:
                        download(key, fil, out)
                        print "retrbinary, yay!"
                    except Exception:
                        print "Downloading %s via urrlib at %s" % (fil, datetime.datetime.now())
                        urllib.urlretrieve("ftp://ftp.wip.ncbi.nlm.nih.gov" + "/" + str(pwd) + "/" + str(key) + "/" + str(fil), out + str(key) + "/" + str(fil))
                    print "%s was downloaded to the folder %s at time: %s" % (fil, key, datetime.datetime.now())
                except Exception:
                    print "%s couldn't be downloaded at time %s" % (fil, datetime.datetime.now())
                    # print something to error file here

                iteration2 += 1
        else:
            print "%s was not found in %s" % (tax, key)

    iteration += 1

# this line compares the two lists and makes them into a third list
# compared_lists = list(set(taxlist) & set(ftplist))
# print compared_lists

# for n in taxlist:
#    match = any(('[%s]'%n) in e for e in ftplist)
#    print "%10s %s" % (n, "YES" if match else "NO")

# clean_compare = [i[13:-1] for i in compare]



# download: urllib.urlretrieve('ftp://server/path/to/file', 'file')


print "done"
ftp.quit()