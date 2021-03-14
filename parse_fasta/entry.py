#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:34:40 2021

@author: kevinchen
"""
class entry:
    def __init__(self,ID,l,header):
        self.ID=ID
        self.l=l
        self.header=header
    
    def get_ID(self):
        return self.ID
    
    def get_length(self):
        return self.l
    
    def get_header (self):
        return self.header
    
    