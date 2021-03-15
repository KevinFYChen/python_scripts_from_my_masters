The scripts written in this directory predict genes in the plasmid of E.Coli O157:H7 (GenBank accession AB011549.2) using Glimmer3.02 and compare the results with the annotation of the plasmid on GenBank. There are 2 main python scripts in this directory: parse_genes.py and compare_coord.cgi.

parse_genes.py reads a genbank flat file and outputs the CDS coordinates in the genbank file. The invocation for this program is as follows:

parse_genes.py -i /path/to/file/inputfile -o /path/to/file/outputfile

-i inputfile: indicate the file path and name of the input file. Note that it must be a genbank flat file
-o outputfile: indicate the file path and name of the output file. 


compare_coord.cgi is a CGI script that compares the genes predicted by Glimmer3.02 with the annotation from GenBank. The results of the comparative analysis can be accessed through the following link: 

http://bfx3.aap.jhu.edu/fchen29/midterm/compare_coord.cgi