#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para combinar tweets en función del medicamento

import pandas as pd
import csv
import pandas as pd
import glob
import os

pd.set_option('display.max_columns', None)

csv_file_list = ["ivermectina.csv", "ibuprofeno.csv", "rivotril.csv", "aspirina.csv", "clonazepam.csv", "omeprazol.csv", "hidroxicloroquina.csv", "azitromicina.csv", "remdesivir.csv", "dexametasona.csv" ]
output_file = "todos_juntos_17.csv"

#se hace funcion para integracion en app
def csv_to_text(input_file, output_file):
    with open(output_file, "w") as my_output_file:
        with open(input_file, "r") as my_input_file:
            [my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()

#combinar todos los archivos en una lista
combined_csv = pd.concat([pd.read_csv(f, sep=",", encoding='utf-8-sig') for f in csv_file_list])
#print("estos son los nombres de columnas" + combined_csv.columns.values)
check_for_nan = combined_csv['idtweet'].isnull()

#export to csv
combined_csv.to_csv("./data/todos_juntos_17.csv", sep= ",", index=False, header=True, encoding='utf-8-sig')