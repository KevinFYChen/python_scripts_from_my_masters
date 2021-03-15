#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 16:44:31 2021

@author: kevinchen

The object created in this script is used to store all of the CDS coordinates
from a genbank flat-file as well as the CDS coordinates of the genes predicted 
using Glimmer 3.02
"""

class cds:
    def __init__(self, coord,strand,ID):
        self.coord=coord
        self.strand=strand
        self.ID=ID
    
    def get_coord(self):
        return self.coord
    
    def get_strand(self):
        return self.strand
    
    def get_ID(self):
        return self.ID