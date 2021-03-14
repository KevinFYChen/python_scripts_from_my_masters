#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import mysql.connector
import jinja2

form = cgi.FieldStorage()
target = form.getfirst('search_term')
target='%'+target.lower()+'%'

conn = mysql.connector.connect(user='fchen29', password='ShinC913', 
                               host='localhost', database='fchen29_chado')
curs=conn.cursor()

query =("SELECT f.uniquename, product.value FROM feature f " 
"JOIN cvterm polypeptide ON f.type_id=polypeptide.cvterm_id " 
"JOIN featureprop product ON f.feature_id=product.feature_id " 
"JOIN cvterm productprop ON product.type_id=productprop.cvterm_id " 
"WHERE polypeptide.name='polypeptide' " 
"AND productprop.name='gene_product_name' " 
"AND LOWER(product.value) LIKE %s;")

curs.execute(query,(target,))

rows=curs.fetchall()
num=len(rows)

curs.close()
conn.close()

templateLoader = jinja2.FileSystemLoader(searchpath="./templates" )
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('unit06.html')

print("Content-Type: text/html\n\n")
print(template.render(genes=rows,num=num))