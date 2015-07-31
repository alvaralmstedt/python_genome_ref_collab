import argparse
import os

import urllib
import ftplib

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

for i in directories:
    ftp.cwd(i)
    subfolder = ftp.nlst()
    print subfolder
    ftp.cwd('..')
    counter += 1
    if counter > 3:
        break

print directories
print "done"
# this line compares the two lists and makes them into a third list
# compared_lists = list(set(taxlist) & set(ftplist))
# print compared_lists

# for n in taxlist:
#    match = any(('[%s]'%n) in e for e in ftplist)
#    print "%10s %s" % (n, "YES" if match else "NO")

# clean_compare = [i[13:-1] for i in compare]



# download: urllib.urlretrieve('ftp://server/path/to/file', 'file')
