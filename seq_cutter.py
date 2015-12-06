#!/usr/local/opt/bin/python

import argparse
#import os
#import subprocess
import sys

parser = argparse.ArgumentParser()
parser .add_argument("fun", nargs="?", type=str, help='function to be run')
parser.add_argument("completedpath", nargs="?", type=str, help='species name')
parser.add_argument("tabpath", nargs="?", type=str, help='species name')
parser.add_argument("species", nargs="?", type=str, help='species name goes here')

args = parser.parse_args()

#function_to_be_used = str(args.fun)
#comppath = str(args.completedpath)
#tabbedpath = str(args.tabpath)
#species = str(args.species)
# cwd = os.getcwd() + "/"

class FastaSeq(object):
    def __init__(self, name, seq):
        self.name = name
        self.seq = seq

    def header(self):
        return self.name[1:]

    def get_sequence(self):
        return self.seq

    def length(self):
        return len(self.seq)

    def get_species_name(self):
        return self.name.split("[")[1].split("]")[0]

    def __str__(self):
        return "%s%s" % (self.name, self.seq)


class Alignment(object):

    def __init__(self, filename):
        self.filename = filename
        self.length = None

        # Parse the file and extract all fasta sequences.
        self.species_names_list = []
        self.sequence_list = []
        with open(self.filename) as my_file:
            for name, seq in self.read_fasta(my_file):
                fs = FastaSeq(name, seq)
                self.sequence_list.append(fs)   # changed, added .get_sequence
#                print "fs is "
                print fs
                # Add each species name to a list.
                self.species_names_list.append(fs.get_species_name()) #removed .get_species_name
             #   print str(fs.get_species_name())
                # Extract the length of the aligned sequences.
                if not self.length:
                    self.length = fs.length()

    def get_file_name(self):
        return self.filename

    def read_fasta(self, infile):
        name, seq = None, []        #Changed name from None to list
        for line in infile:
            if line.startswith(">"):
                if name: yield (name, ''.join(seq))
                name, seq = line, []
            else:
                line = line.rstrip()
                seq.append(line)
        if name: yield (name, ''.join(seq))


    def get_species_names(self):
        return self.species_names_list

    def get_alignment_length(self):
        return int(self.length)

    def get_sequence(self, species):
        for fasta_sequence in self.sequence_list:    # !!!THIS DOES NOT LOOP!!! (for unknown reasons)
#            print "fasta_sequence.get_species_name(): %s" % fasta_sequence.get_species_name()
#            print len(self.sequence_list)
#            print self.sequence_list[2]
#            print fasta_sequence                       #Devel.
            if species == fasta_sequence.get_species_name():        #changed
                print "type: "
                print type(self.sequence_list)
                return fasta_sequence.get_sequence()
#            elif species != fasta_sequence.get_species_name():
#                continue
            else:
                 print "fasta_sequence.get_species_name(): %s" % fasta_sequence.get_species_name()   #Devel
                 print "species: %s" % species                                                       #Devel
                 return "-" * self.get_alignment_length()



if __name__ == "__main__":
    all_species_names = []
    alignment_list = []
    for myFile in sys.argv[1:]:
        # Create an instace of an alignment object for each fasta file.
        af = Alignment(myFile)
        # Save all instances of the Alignment class in a list
        alignment_list.append(af)
#		print "Alignment length: ", af.get_alignment_length()

        # Create master list of species names in all files.
        for species in af.get_species_names():
            if species not in all_species_names:
                all_species_names.append(species)

    for species in all_species_names:
        print ">", species
        for alignment in alignment_list:
#		for species in all_species_names:
            # Generate a fasta header
#			print len(species)				# Devel.
#			print ">", species
#            print "har:"
#            print alignment.get_file_name()
#            print species
            print alignment.get_sequence(species)


#		print fo.get_file_name()			# Devel.

