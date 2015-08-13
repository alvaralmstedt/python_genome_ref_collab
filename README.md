# python_genome_ref_collab
For developing a platform for easily downloading reference genomes from the NCBI ftp server.

## Usage

* genome_downloader.py [in file] [output folder] [full ftp url]

* genome_rename.py [path to downloads]

genome_downloader.py will match the species genuses from your list to the availible genomes on the ftp server and then download them. Depending on the size of your list, this may take several hours.

genome_rename.py will gunzip and untar your downloaded genomes and give append the species name to the start of the file.
