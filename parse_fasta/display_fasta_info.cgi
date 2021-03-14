#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 20:20:42 2021

@author: kevinchen

This CGI file parses the FASTA sequence from e.coli K12 and outputs 
the ID portion of each header as well as the length of each sequence
to a HTML template
"""
import jinja2
from parseEntry import parse_entry

templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

env = jinja2.Environment(loader=templateLoader)
template = env.get_template("unit04.html")

f=open('e_coli_k12_dh10b.faa')
entries=parse_entry(f)
 
print("Content-Type: text/html\n\n")
print(template.render(entries=entries))

