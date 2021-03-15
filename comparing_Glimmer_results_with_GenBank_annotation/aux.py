#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:54:46 2021

@author: kevinchen

This script provides the auxiliary functions used in the main cgi python 
script.
"""

#This function compares a reference gene with each of the predicted genes and 
#determines if a predicted gene overlaps with the reference gene. If it
#does, the function determines whether it is an exact match, a 5'match or a 3' 
#match with the reference gene.
def compare_results(ref,pred_l,match,strand,empty):
    r_start,r_end=ref.get_coord()
    overlap_with_ref=[]
    local_3_match=0
    local_5_match=0
    local_exact_match=0
    overlapped_ids=[]
    
    match[ref.get_ID()]=(empty,None,None,"No match")
    
    for pred in pred_l:
        overlap=False
        p_start,p_end=pred.get_coord()
        if strand == "forward":
            overlap=compare_forward(r_start,r_end,p_start,p_end)

        elif strand == "reverse":
            overlap=compare_reverse(r_start,r_end,p_start,p_end)

        if overlap:
            overlapped_ids.append(pred.get_ID())
            if p_start == r_start and p_end == r_end:
                overlap_with_ref.append((pred,"agrees","agrees","Exact match"))
                local_exact_match+=1
            elif p_start == r_start:
                overlap_with_ref.append((pred,"agrees","disagrees","5\' Match"))
                local_5_match+=1
            elif p_end == r_end:
                overlap_with_ref.append((pred,"disagrees","agrees","3\' Match"))
                local_3_match+=1
            else:
                overlap_with_ref.append((pred,"disagrees","disagrees",
                                         "overlaps but no 5\' or 3\' match"))
    
    if len(overlap_with_ref) != 0:
        matches=[i[3] for i in overlap_with_ref]
    
        if "Exact match" in matches:
            match[ref.get_ID()]=overlap_with_ref[matches.index("Exact match")]
        elif "5\' Match" in matches:
            match[ref.get_ID()]=overlap_with_ref[matches.index("5\' Match")]
        elif "3\' Match" in matches:
            match[ref.get_ID()]=overlap_with_ref[matches.index("3\' Match")]
        else:
            match[ref.get_ID()]=overlap_with_ref[matches.index(
                "overlaps but no 5\' or 3\' match")]
    
    return overlapped_ids,local_exact_match,local_5_match,local_3_match


#This function compares 2 CDS that are both on the forward strand and
#determines if they overlap
def compare_forward(r_start,r_end,p_start,p_end):
    overlap=False
    # if a CDS spans the end and the beginning of the circular genome
    if r_start > r_end:
        if ((p_start >= r_start or p_start <= r_end) or 
            (p_end <= r_end or p_end >= r_start) or 
            (p_start < r_start and p_end > r_end)):
            overlap=True
    else:
        if ((p_start >= r_start and p_start <= r_end) or 
            (p_end >= r_start and p_end <= r_end) or
            (p_start < r_start and p_end > r_end)):
            overlap=True
    
    return overlap


#This function compares 2 CDS that are both on the reverse strand and 
#determines if they overlap
def compare_reverse(r_start,r_end,p_start,p_end):
    overlap=False
    # if a CDS spans the end and the beginning of the circular genome
    if r_start < r_end:
        if ((p_start <= r_start or p_start >= r_end) or 
            (p_end >= r_end or p_end <= r_start) or 
            (p_start > r_start and p_end < r_end)):
            overlap=True
    else:
        if ((p_start <= r_start and p_start >= r_end) or 
            (p_end <= r_start and p_end >= r_end) or
            (p_start > r_start and p_end < r_end)):
            overlap=True
    
    return overlap
    



                

                
        
                

        
    

        
        