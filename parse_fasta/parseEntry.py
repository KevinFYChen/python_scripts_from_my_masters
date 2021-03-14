#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:50:01 2021

@author: kevinchen
"""
import re
from entry import entry

def parse_entry(f):
    residues=0
    ID=None
    header=None
    entries=list()
    start=False
    count=0
    for line in f:
        line = line.rstrip()
        
        if line.startswith('>'):
            count+=1
            if not start:
                start=True
            if residues != 0:
                entries.append(entry(ID,residues,header))
            if count>20:
                break
            ID,header=parse_header(line)
            residues=0
        elif start:
            residues+=len(line)
    if count <= 20:
        entries.append(entry(ID,residues,header))
    return entries


def parse_header(h):
    h=h[1:]
    ID=re.search(r"gi\|\d+\|ref\|.+?\|",h).group()
    h=re.sub(r"gi\|\d+\|ref\|.+?\|",'',h)
    return ID,h
    
    