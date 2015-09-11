# python_genome_ref_collab
For developing a platform for easily downloading reference genomes from the NCBI ftp server.

## Usage

* genome_downloader.py [in file] [output folder] [full ftp url] [-r] [-z] [-c]

* genome_rename.py [path to downloads] [-r] [-z] [-c] (!!! all functionality now impelemented into genome_downloader.py !!!)

genome_downloader.py will match the species genuses from your list to the availible genomes on the ftp server and then download them. Depending on the size of your list, this may take several hours. The infile is a list of species genus (1 genus per line) in a plain text file. The output folder is where on your system the reference genomes will be stored. The url is copied from the ftp address you want to search from (eg. ftp://ftp.wip.ncbi.nlm.nih.gov/genomes/Bacteria/).

genome_rename.py will gunzip and untar your downloaded genomes and give append the species name to the start of the file. This will currently only work for compressed .tar.gz files ( like the ones in /Bacteria_DRAFT/ or /ASSEMBLY_BACTERIA/).

[in file] : Full path to the file that contains genus names (capitalised) that you want to download member species from.

[output] : Full path to the folder where you want youre species folder to be placed. The files will be placed into these species folders. If you download from /ASSEMBLY_BACTERIA/, there will be another set of folders inside the species folders which contains your files (unless you choose to concatenate them, in which case the will be directly in the species folder).

[ftp url] : This flag currently checks for the end of the url you put in order to determine where to originate from when navigating the ftp directories. Example: "ftp://ftp.wip.ncbi.nlm.nih.gov/genomes/Bacteria/" Trailing slash doesn't matter.

[-r] : Rename. This flag appends the species folder name onto the front of all the files downloaded.

[-z] : Zip. Or rather unzip. This unzips all files that have the file-ending ".tgz" (gzipped tarballs)

[-c] : This concatenates all files in the same folder with the same file ending. Made to be used with the [-z] flag because the ".tgz" (zipped) tarballs often contains hundreds of smaller files (individual contigs). The concatenated content will be in files with ".concat." in frnot of the file-ending. The small files will be deleted after the concatenation is completed.
