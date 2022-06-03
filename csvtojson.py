#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para para convertir csv a json

import pandas as pd
import csv
import json
import ast

import pandas as pd
import re
csv_file = pd.DataFrame(pd.read_csv("lista_meds.csv", sep = "\n", header = 0, index_col = False))

csv_file.to_json("json_med.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)

csv_file = pd.DataFrame(pd.read_csv("terminos_total.csv", sep = "\n", header = 0, index_col = False))

df = pd.read_csv("terminos_total.csv", sep = ";", header = 0, index_col = False)

#eliminar filas si longitud de la cadena <2
df['terminos'] = df['terminos'].astype('str')

mask = (df['terminos'].str.len() > 3)
df = df.loc[mask]
print(df)

df = df['terminos'].str.split(',').str[0]
print(df)
df = df.replace(';','', regex=True)
df.to_csv (r'terminos_fixed.csv', index = False, header=True)

from unicodedata import normalize

x = df.to_string(index = False , header=True).split('\n')
s = [' '.join(ele.split()) for ele in x]

lista = []
for eses in s:
# -> NFD y eliminar diacríticos
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    eses = normalize('NFKC', normalize('NFKD', eses).translate(trans_tab))

    # -> NFC
    eses = normalize('NFC', eses)
    lista.append(eses)

print(lista)

df = pd.DataFrame(lista, columns=['terminos'])
print(df)
df.to_csv (r'terminos_fixed.csv', index = False, header=True)

csv_file = pd.DataFrame(pd.read_csv("terminos_fixed.csv", sep = "\n", header = 0, index_col = False))
csv_file.to_json("json_terminos.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)

