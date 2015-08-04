import argparse
import os
import re
import urllib
import ftplib
import datetime

directories = []


def testifDirectory(ftp, filenames):
    # put whatever you want to do in each directory here
    # when you have called testifDirectory with a file,
    # the command above will fail and you will return



    # get the files and directories contained in the current directory
    #    filenames = []
    #    ftp.retrlines('NLST',filenames.append)
    for name in filenames:
        try:
            if name != "all":
                ftp.cwd(name)
                directories.append(name)
                print name
                ftp.cwd('..')
        except ftplib.error_perm:
            # put whatever you want to do with files here
            continue
            # put whatever you want to do after processing the files
            # and sub-directories of a directory here


# assigns argument variable
parser = argparse.ArgumentParser()

# adds arguments to the magic "parser" variable
parser.add_argument("taxlistpath", nargs="?", type=argparse.FileType('r'), help='path to your list')
parser.add_argument("output", nargs="?", default=os.getcwd(), help='specify output path, else cwd')
parser.add_argument("ftpurl", nargs="?", help='specify top level ftp url to search down from')

# parser.add_argument("-f", "--family", action="store_true", help='organism family to download genomes from')
# parser.add_argument("-p", "-phylum", action="store_true", help='phyla to download genomes from')
# parser.add_argument("--fna", action="store_true", help='download .fna files')
# parser.add_argument("--faa", action="store_true", help='download .faa files')
# parser.add_argument("-a", "-all", action="store_true", help='download all files')
# parser.add_argument("-d", "--draft", action="store_true", help='will also look among draft genomes')


# returns the arguments given to the "args" variable
args = parser.parse_args()

# makes a the text list into a python list
taxlist = args.taxlistpath.read().splitlines()
print taxlist
print "\n"
# ftpurl = args.ftpurl
# print ftpurl

# this connects to the ncbi ftp server and enters the "genomes" directory
ftp = ftplib.FTP("ftp.wip.ncbi.nlm.nih.gov")
ftp.login()
ftp.cwd("genomes")

# print ftp.retrlines('LIST')

# this line converts the genomes directory into a list
# ftplist = ftp.nlst()
# ftplist = sorted(ftplist, key=str.lower)

# print ftplist

print "\n"

counter = 0

files = []

ftpdir = ftp.retrlines('NLST', files.append)
# ftpdir = ftpdir.splitlines()

# print ftpdir
print "before forloop"

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
    ftp.cwd(i)
    subfolder = ftp.nlst()
#   print subfolder
    genome_subfolders[i] = subfolder
    ftp.cwd('..')
    counter += 1
    if counter > 6:   # temporary counter to limit testing time
        break

print "printing genome_subfolders"
print genome_subfolders
# print directories

print "starting search"

pwd = ftp.pwd()
# This will iterate over the keys in genome_subfolders dict and match to user provided taxlist

lstnam = []
filnam = ""


#for key in genome_subfolders.iterkeys():
#    lstnam.append(key.startswith(taxlist[for i in range(len(taxlist))]))


#for i in np.where(lstnam[0]):
#    genome_subfolders.keys()[i]
#    urllib.urlretrieve("ftp://ftp.wip.ncbi.nlm.nih.gov", filename=str(pwd) + "/" + str(genome_subfolders.keys()[i]) + "/" + genome_subfolders.get((genome_subfolders.keys()[i])))


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
                    if not os.path.exists(str(key)):
                        print "creating directory: %s" % (str(key))
                        os.makedirs(str(key))
                    urllib.urlretrieve("ftp://ftp.wip.ncbi.nlm.nih.gov" + "/" + str(pwd) + "/" + str(key) + "/" + str(fil), str(key) + "/" + str(fil))
                    print "%s was downloaded to the folder %s at time: %s" % (fil, str(key), datetime.datetime.now())
                except Exception:
                    print "%s couldn't be downloaded" % (fil)

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