#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Concatena archivos de med y pa
import glob
import csv
from os import remove


def concat_pa():
    with open("./utils/pa_junto.csv",'w') as fout:
        wout = csv.writer(fout,delimiter=',')
        int_pa = glob.glob("./utils/vademecum-pa" + "*.csv")
        h = True
        for filename in int_pa:
            with open(filename,'r') as fin:
                if h:
                    h = False
                for line in csv.reader(fin,delimiter=','):
                    wout.writerow(line)

    with open("./utils/pa_junto.csv") as in_file:
        with open("./utils/pa_total.csv", 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)

    remove("./utils/pa_junto.csv")

def concat_med():

    with open("./utils/med_junto.csv",'w') as fout:
        wout = csv.writer(fout,delimiter=',')
        int_pa = glob.glob("./utils/vademecum-med" + "*.csv")
        h = True
        for filename in int_pa:
            with open(filename,'r') as fin:
                if h:
                    h = False
                for line in csv.reader(fin,delimiter=','):
                    wout.writerow(line)

    with open("./utils/med_junto.csv") as in_file:
        with open("./utils/med_total.csv", 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)

    remove("./utils/med_junto.csv")