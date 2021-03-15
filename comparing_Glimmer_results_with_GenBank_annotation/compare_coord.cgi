#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:50:50 2021

@author: kevinchen

This CGI script compares gene prediction information on the plasmid of E.Coli 
O157:H7 from 2 different sources. In particular, it reads in the coordinates 
from GenBank and from the predicted output from Glimmer3.02, compare the 
coordinates and populates the results of the comparative analysis within a 
HTML5 template
"""
import jinja2
from cds import cds
from aux import compare_results

ref_f=open("genbank_annotation.txt","r")
pred_f=open("./glimmer_results/run1.predict","r")

pred_reverse=[]
pred_forward=[]
num_3end=0
num_5end=0
num_exact=0
match={}
ref_l=[]
overlapped_ids=[]
total_pred=0
total_ref=0
empty_cds=cds((None,None),None,"No match")

#go through the predicted genes and put the genes
#into 2 lists based on the strand they are in
for tmp in pred_f:
    tmp=tmp.strip()
    if tmp.startswith(">"):
        continue
    total_pred+=1
    tmp=tmp.split()
    if tmp[3].startswith("+"):
        strand="forward"
    else:
        strand="reverse"
    obj=cds((int(tmp[1]),int(tmp[2])),strand,tmp[0])
    if strand=="forward":
        pred_forward.append(obj)
    elif strand=="reverse":
        pred_reverse.append(obj)
        
#compare each of the reference genes from genbank with the predicted genes    
for tmp in ref_f:
    tmp=tmp.strip()
    if tmp.startswith("#"):
        continue
    total_ref+=1
    tmp=tmp.split()
    ref=cds((int(tmp[1]),int(tmp[2])),tmp[3],tmp[0])
    ref_l.append(ref)
    if ref.get_strand() == "forward":
        (local_overlapped_ids,local_exact_match,
         local_5_match,local_3_match)=compare_results(ref,pred_forward,match,
                                                      "forward",empty_cds)
    elif ref.get_strand() == "reverse":
        (local_overlapped_ids,local_exact_match,
         local_5_match,local_3_match)=compare_results(ref,pred_reverse,match,
                                                      "reverse",empty_cds)
    overlapped_ids.extend(local_overlapped_ids)
    num_5end=num_5end+local_5_match
    num_3end=num_3end+local_3_match
    num_exact=num_exact+local_exact_match

#take the number of unique predicted genes that overlap with a reference
# gene and subtract the total number of predicted genes by this number
# to get the number of predicted genes that do not overlap with a reference
# gene    
num_non_overlap=total_pred - len(set(overlapped_ids))

ref_f.close()
pred_f.close()

templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

env = jinja2.Environment(loader=templateLoader)
template = env.get_template("midterm.html")
 
print("Content-Type: text/html\n\n")
print(template.render(ref_l=ref_l,match=match,
                      num_non_overlap=num_non_overlap,num_5end=num_5end,
                      num_3end=num_3end, num_exact=num_exact,
                      total_pred=total_pred, total_ref=total_ref))