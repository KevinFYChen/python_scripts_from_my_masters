#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:10:29 2021

@author: kevinchen

This script converts a gff3 file to a bed6 file
"""
import sys,getopt
import re

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:],"hi:o:")
    except getopt.GetoptError:
        #specifying how this program should be executed 
        print ("main.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    inputfile=None
    outputfile=None
      
    for opt, arg in opts:
        if opt == '-h':
            print ("main.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
    
    if inputfile is None or outputfile is None:
        print("error: file path to both input and output must be provided")
        sys.exit(2)
    
    if not inputfile.endswith("gff3"):
        print ("error: the extension of the input file must be gff3")
        sys.exit(2)
        
    inF=open(inputfile,"r")
    outF=open(outputfile,"w")
    
    for line in inF:
        if line.startswith("#"):
            continue
        line=line.rstrip()
        d=extract_info(line)
        if d is not None:
            outF.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.
                       format(d['chrom'],d['chromStart'],d['chromEnd'],
                              d['name'],d['score'],d['strand']))

def extract_info(line):
    # creating a dictionary for better readability
    fields=line.split("\t")
    if fields[2] != "gene":
        return None
    name=re.search(r";\s*Name\s*=\s*.+?\s*;",fields[8]).group().split("=")[1]
    name=re.sub(";",'',name.strip())
    result={
        'chrom':fields[0],
        #convert index from 1 based to 0 based
        'chromStart':(int(fields[3])-1),
        'chromEnd':(int(fields[4])),
        'name':name,
        'score':0,
        'strand':fields[6]
        }
    return result
    


if __name__ == '__main__':
    main(sys.argv)