#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 13:40:13 2020

@author: kevinchen

This program takes in a SAM file and outputs a fragment recruitment plot
"""
import argparse
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np


# The main function takes care of the I/O stream. It skips the header of the
# SAM file and stores the rest of the information in the file using an NumPy
# 2D array 
def main():
    parser = argparse.ArgumentParser( description='Basic sequence statistics reporter for FASTA files')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='''
                        #Path to an input file to be read'''.replace("\n", ""))
    args = parser.parse_args()
    fh = open(args.input_file, 'r')
    
    all_lines=[]
    columns=[0,2,3,5,9] #indices for query name, reference name,read position,
                        #CIGAR string and segment sequence

    for line in fh:
        line=line.rstrip()
        if line.startswith("@"):
            continue
        else:
            l=line.split()
            md_index=findMD(l)  #finds the index for the MD column
            md=l[md_index]
            md = re.sub('[^0-9]',' ', md)
            md=md.split()
            md_match=addValue(md)   #adds all the values in the MD string
            l=subset(l,columns)     #subsets the line with just our columns of 
                                    #interest
            cigar=l[3]
            match=re.findall("\d+M",cigar)
            match=addMValue(match)  #adds all M values in the CIGAR string
            identity=(md_match/match)*100
            l.append(identity)      #append the percentage identity value to 
                                    #the line
            all_lines.append(l)     #This list contains all lines processed
                                    #so far
    
    matrix=np.array(all_lines)      #converts all lines into an array
    x=matrix[:,2].astype(np.int)
    y=matrix[:,5].astype(np.float)
    x_upper=np.percentile(x,95)     #5th and 95th percentile were chosen to 
                                    #eliminate outliers
    x_lower=np.percentile(x,5)
    y_upper=np.percentile(y,95)
    y_lower=np.percentile(y,5)
    new_matrix=subsetMatrix(matrix,x_upper,x_lower,"x")
    new_matrix=subsetMatrix(new_matrix,y_upper,y_lower,"y")
    x=new_matrix[:,2].astype(np.int)
    y=new_matrix[:,5].astype(np.float)
    plt.scatter(x,y,s=1)
    plt.xticks(fontsize=8)
    title=args.input_file
    title=title.split("/")
    title=title[-1].replace(".sam","")
    plt.xlabel("genome positions")
    plt.ylabel("% identity")
    plt.title(title)
    plt.savefig("/Users/kevinchen/Documents/MS Bioinformatic program courses and " 
            "supplement courses/fall 2020/Practial introduction to Metagenomics"
            "/lessons/Midterm/HMP/plots/{0}.png".format(title))

        
# subsets the elements of a given list
def subset(l,columns):
    new_l=[]
    for i in columns:
        new_l.append(l[i])
        
    return new_l

# subsets the rows of a 2D array based on genome position or percent identity
def subsetMatrix(m,upper,lower,margin):
    new_matrix=[]
    if margin=="x":
        for i in m:
            if int(i[2])<upper and int(i[2]) >lower:
                new_matrix.append(i)
    elif margin=="y":
        for i in m:
            if float(i[5]) < upper and float(i[5]) > lower:
                new_matrix.append(i)
    
    new_matrix=np.array(new_matrix)
    return new_matrix

# finds the index of the MD element in a list 
def findMD(l):
    index=None
    count=0
    for i in l:
        if i.startswith("MD:Z:"):
            index=count
            break
        else:
            count+=1
    return index

# finds the range of the values in a list
def getRange(val_list):
    min_val = min(val_list)
    max_val = max(val_list)

    return (min_val, max_val)

# adds all of the values in a list and returns the sum
def addValue(l):
    total=0
    for i in l:
        total=total+int(i)
    return total

# given a list of M values from the CIGAR string, return the sum
def addMValue(M):
    count=0
    for i in M:
        count=count+int(i.replace("M",""))
    return count

if __name__ == '__main__':
    main()

