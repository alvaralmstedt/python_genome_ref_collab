#!/usr/local/opt/bin/python

# Written by: Alvar Almstedt

import argparse
import os
import urllib
import ftplib
import datetime
import signal
import tarfile

counter = 0
directories = []

class TimeoutException(Exception):  # Custom exception class
    pass

# Handles timeouts (skips if things take too long)
def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException


# Changes the behavior of the SIGLARM
signal.signal(signal.SIGALRM, timeout_handler)

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


def renamer(user_directory):
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



# tries to go into every directory to check if it is a directory. This can take a little while.
def testifDirectory(ftp, filenames):
    global counter
    files.sort()
    # get the files and directories contained in the current directory
    for name in filenames:
        signal.alarm(10)  # alarm is rung after 10 seconds
        try:
            if name != "all" and name != "ASSEMBLY_BACTERIA":
                ftp.cwd(name)
                directories.append(name)
                print name
                indexer(name)
                if name == "CLUSTERS":
                    ftp.cwd("/genomes/Bacteria")
                else:
                    ftp.cwd('..')
            elif name == "ASSEMBLY_BACTERIA" and counter < 10:
                ftp.cwd(name)
                print name
                ass_cwd = ftp.nlst()
                annoying_folders[str(name)] = str(ass_cwd[0])
                ftp.cwd(str(ass_cwd[0]))
                indexer(name)
                ftp.cwd("..")
                ftp.cwd("..")
                counter += 1
                print counter
        except ftplib.error_perm:
            print "%s is not a directory, continuing" % name
            continue
        except TimeoutException:
            print "%s caused a timeout after 10 seconds" % name
            continue
        else:
            signal.alarm(0)  # resets alarm


# This function indexes the contents of each Specie-folder to the genome_subfolder dict
def indexer(dirs):
    signal.alarm(30)
    try:
        if dirs != "CLUSTERS" and counter < 10:
            subfolder = ftp.nlst()
            print "indexing %s at time: %s" % (dirs, datetime.datetime.now())
            genome_subfolders[dirs] = subfolder
    except TimeoutException:
        print "Timed out after 30 seconds, continuing"
    else:
        # Resets alarm
        signal.alarm(0)



# Tries to download files via the ftplib module
# This still doesn't work for whatever reason. urllib is used as a backup which works.

#def download(folder, filenames, outputfolders):
#    local_filename = os.path.join(outputfolders + str(folder), str(filenames))
#    lf = open(str(local_filename), "wb")
#    ftp.retrbinary('RETR %s' % filenames, lf.write)
#    lf.close()

# assigns argument variable
parser = argparse.ArgumentParser()

# argparse explanations: https://infohost.nmt.edu/tcc/help/pubs/python/web/argparse-add_argument.html
# adds arguments to the magic "parser" variable
parser.add_argument("taxlistpath", nargs="?", type=argparse.FileType('r'), help='path to your list')
parser.add_argument("output", nargs="?", type=str, help='specify output path, else cwd')
parser.add_argument("ftpurl", nargs="?", action='store', type=str, help='specify top level ftp url to search down from')

parser.add_argument("-r", "--rename", action="store_true", help='' )
parser.add_argument("-z", "--zip", action="store_true", help='specifies to untar/gunzip zipped .tgz files. Has to be used with the -r flag')
parser.add_argument("-c", "--concat", action="store_true", help="concatenates contigs split into several .faa/.fna/etc. files. Has to be used with the -r flag")


# below are planned but as-of-yet unimplemented arguments
# parser.add_argument("-f", "--family", action="store_true", help='organism family to download genomes from')
# parser.add_argument("-p", "-phylum", action="store_true", help='phyla to download genomes from')
# parser.add_argument("--fna", action="store_true", help='download .fna files')
# parser.add_argument("--faa", action="store_true", help='download .faa files')
# parser.add_argument("-a", "-all", action="store_true", help='download all files')
# parser.add_argument("-d", "--draft", action="store_true", help='will also look among draft genomes')


# returns the arguments given to the "args" variable
args = parser.parse_args()

concat = args.concat
zipped = args.zip
rename = args.rename

# makes a the text list into a python list
taxlist = args.taxlistpath.read().splitlines() # this should be a capitalised list of species genus

if str(args.output).endswith("/"):
    out = str(args.output)
else:
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
        prompt = raw_input("Your list contains the name 'Candidatus'. Are you sure you want to download genomes with this genus? y/n: ")
        if prompt == "n" or prompt == "N" or prompt == "no" or prompt == "NO" or prompt == "No":
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
    if ftpurl[-9:] == "/genomes/" or ftpurl[-9:] == "v/genomes":
        ftp.cwd("genomes")
    elif ftpurl[-9:] == "Bacteria/" or ftpurl[-9:] == "/Bacteria":
        ftp.cwd("genomes")
        ftp.cwd("Bacteria")
    elif ftpurl[-9:] == "ia_DRAFT/" or ftpurl[-9:] == "ria_DRAFT":
        ftp.cwd("genomes")
        ftp.cwd("Bacteria_DRAFT")
    elif ftpurl[-9:] == "es/Fungi/" or ftpurl[-9:] == "mes/Fungi":
        ftp.cwd("genomes")
        ftp.cwd("Fungi")
    elif ftpurl[-12:] == "LY_BACTERIA/" or ftpurl[-12:] == "BLY_BACTERIA":
        ftp.cwd("genomes")
        ftp.cwd("ASSEMBLY_BACTERIA")
#        ass_cwd = ftp.nlst()
#        ftp.cwd(str(ass_cwd[0]))
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

pwd = ftp.pwd()

files = []
annoying_folders = {}
ftpdir = ftp.retrlines('NLST', files.append)
# ftpdir = ftpdir.splitlines()

# print ftpdir
# print "before for-loop"

# First try on directory checking, is a lot faster than the current one but works really poorly due to list format:
#
# for r in files:
#    print "alvar " + r + "\n"
#    if r.upper().startswith('D'):
#        print "found directory: " + r[56:]  #slice 56 is for taking only the folder name from the filelist
#        if r[56:] != "all" and r[56:] != "3 all":
#            stripped = r[56:].strip()
#            directories.append(stripped)
genome_subfolders = {}
testifDirectory(ftp, files)

# print directories.sort()

# this dict will contain all directories in genomes as keys and lists of their contents as values

# print "printing genome_subfolders"
# print genome_subfolders
# print directories

print "starting search"

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
#                    try:
#                        download(key, fil, out)
#                        print "retrbinary, yay!"
#                    except Exception:
                    if "ASSEMBLY_BACTERIA" not in pwd:
                        print "Downloading %s via urrlib at %s" % (fil, datetime.datetime.now())
                        urllib.urlretrieve("ftp://ftp.wip.ncbi.nlm.nih.gov" + "/" + str(pwd) + "/" + str(key) + "/" + str(fil), out + str(key) + "/" + str(fil))
                        print "%s was downloaded to the folder %s at time: %s" % (fil, key, datetime.datetime.now())
                    elif "ASSEMBLY_BACTERIA" in pwd:
                        print "Downloading %s via urrlib at %s" % (fil, datetime.datetime.now())
                        urllib.urlretrieve("ftp://ftp.wip.ncbi.nlm.nih.gov" + "/" + str(pwd) + "/" + str(key) + "/" + str(annoying_folders[key]) + "/" + str(fil), out + str(key) + "/" + str(fil))
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

if rename:
    renamer(out)


# download: urllib.urlretrieve('ftp://server/path/to/file', 'file')


print "All done at %s" % (datetime.datetime.now())
