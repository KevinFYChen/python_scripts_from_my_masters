#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 23:51:24 2021

@author: kevinchen

This python script takes a GenBank flat-file, parses out the CDS
coordinates in the file and save them to an output file.
"""
import sys,getopt
import re
from cds import cds

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
        
    inF=open(inputfile,"r")
    outF=open(outputfile,"w")
    
    in_f_section=False
    cds_list=[]
    
    for line in inF:
        line=line.strip()
        
        #if the cursor is within the FEATURE section of the genbank file
        if in_f_section:
            if line.startswith("CDS "):
                coord,strand=parse_Coordinates(line)
                for feature in inF:
                    feature=feature.strip()
                    if feature.startswith("/protein_id"):
                        ID=feature.split("=")[1]
                        ID=re.sub('\"','',ID)
                        break
                cds_list.append(cds(coord,strand,ID))
        elif line.startswith("FEATURES"):
            in_f_section=True
        else:
            continue
    
    outF.write("#ID\tstart\tend\tstrand\n")
    for gene in cds_list:
        outF.write("{0}\t{1}\t{2}\t{3}\n".format(gene.get_ID(),
                                                 gene.get_coord()[0],
                                                 gene.get_coord()[1],
                                                 gene.get_strand()))
    inF.close()
    outF.close()
    

#This function takes a CDS string from a genbank file and determines which 
#strand the CDS is on. It also parses out the coordinates of the CDS. 
#Both the strand and the coordinates are returned. 
def parse_Coordinates(line):
    location=line.split()[1]
    
    #All letters and the > and < characters are removed from the string
    coord_s=re.sub(r'[><\(\)A-Za-z]','',location)
    if location.startswith("complement"):
        strand="reverse"        
        coord=(re.search(r'\d+$',coord_s).group(),re.search(r'^\d+',coord_s).group())
    else:
        strand="forward"
        coord=(re.search(r'^\d+',coord_s).group(),re.search(r'\d+$',coord_s).group())
    return coord,strand
        
        
if __name__ == '__main__':
    main(sys.argv)