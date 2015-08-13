# python_genome_ref_collab
For developing a platform for easily downloading reference genomes from the NCBI ftp server.

## Usage

* genome_downloader.py [in file] [output folder] [full ftp url]

* genome_rename.py [path to downloads]

genome_downloader.py will match the species genuses from your list to the availible genomes on the ftp server and then download them. Depending on the size of your list, this may take several hours. The infile is a list of species genus (1 genus per line) in a plain text file. The output folder is where on your system the reference genomes will be stored. The url is copied from the ftp address you want to search from (eg. ftp://ftp.wip.ncbi.nlm.nih.gov/genomes/Bacteria/). It is important that this address ends with "/".

genome_rename.py will gunzip and untar your downloaded genomes and give append the species name to the start of the file. This will currently only work for compressed .tar.gz files ( like the ones in /Bacteria_DRAFT/).
