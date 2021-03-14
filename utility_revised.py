#!/usr/bin/env python3

"""
This script takes a fastq or fasta file and prints out the number of sequences 
as well as the total number of residues in the file to standard output

This script assumes that the file format is indicated in the file name. Thus,
file extensions such as .fq,.fastq,.fasta or .fa must be indicated in the file 
name for this script to parse the file properly. 

This script recognizes compressed files by detecting the file extension .gz in
the file name

"""

import argparse
import gzip
import os
import sys

def main():
    parser = argparse.ArgumentParser( description='Basic sequence statistics reporter for FASTA files')

    ## output file to be written
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to an input file to be read' )
    args = parser.parse_args()

    seq_count = 0
    total_residues = 0
    
    
    if "fq" in args.input_file or "fastq" in args.input_file:
        file_type="fastq"
    elif "fa" in args.input_file or "fasta" in args.input_file:
        file_type="fasta"
    elif "fnn" in args.input_file:
        file_type="fnn"
    else:
        print("error: invalid file format")
        sys.exit()

    if args.input_file.endswith('.gz'):
        fh = gzip.open( args.input_file, 'rb')
        is_compressed = True
    else:
        fh = open( args.input_file, 'r' )
        is_compressed = False


    if file_type=="fasta" or file_type=="fnn":     
        for line in fh:
            if is_compressed:
                line = line.decode()
                    
            line = line.rstrip()
                
            if line.startswith('>'):
                seq_count += 1
            else:
                total_residues += len(line)
    
    elif file_type=="fastq":
        local_seq=0
        local_qual=0
        sequence=False
        for line in fh:
            if is_compressed:
                line=line.decode()
           
            line=line.rstrip()
            
            #If a line starts with @ check if the number of phred scores match with the number of sequence
            #if so, this means that we are at the beginning of a new sequence
            if line.startswith ('@'):
                if local_seq == local_qual:
                    seq_count+=1
                    local_seq=0
                    local_qual=0
                    sequence=True
                    continue
                else:
                    local_qual+=len(line)
                    continue
            if line.startswith ('+') and sequence:
                sequence=False
                continue
            if sequence :
                local_seq+=len(line)
                total_residues+=len(line)
            else:
                local_qual+=len(line)
                

    print("{0}: ".format(args.input_file))
    print("\nTotal sequences found: {0}".format(seq_count));
    print("Total residues found : {0}\n\n".format(total_residues));



if __name__ == '__main__':
    main()







