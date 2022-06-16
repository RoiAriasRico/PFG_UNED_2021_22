#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para hacer diccionario de principios activos a traves de www.vademecum.org
import time
import csv
import string
import urllib.request as urllib2
from bs4 import BeautifulSoup
from tkinter import messagebox

def vademecum_pa():
    #iteracion en las 26 letras
    letter_list = string.ascii_lowercase[0:26]

    for letter in letter_list:
    #obtener archivo csv por cada letra alefabetica
        with open('./utils/vademecum-pa-' + str(letter) + '.csv', 'w') as csvfile:
            fieldnames = ['nombre']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            print("Inicio letra " + str(letter))
            vademecum = "https://www.vademecum.es/principios-activos-atc-es-" + letter + "_1"
            print(vademecum)

            headers = {'User-agent': 'Mozilla/5.0'}
            req = urllib2.Request(vademecum, None, headers)
            page = urllib2.urlopen(req, timeout=3).read()
            soup = BeautifulSoup(page, "html.parser")

            drug_list = soup.find('ul', class_='no-bullet')
            i = 0
            for row in drug_list.findAll("li"):
                i += 1
                link = row.find('a')

                drug_link = ('http://vademecum.es' + str(link['href']).strip())
                drug_name2 = link.contents[0].strip()
                print(drug_name2)
                time.sleep(0.11)
                req = urllib2.Request('http://vademecum.es' + str(link['href']), None, headers)

                page = None
                print("\tPrincipio activo " + drug_name2)
                writer.writerow({'nombre': drug_name2})
                # atrapa el error
                while True:
                    try:
                        page = urllib2.urlopen(req, timeout=3).read()
                    except (KeyboardInterrupt, SystemExit):
                        raise
                    #Si error, continua
                    except:
                        print("\t\t[ERROR] Error abriendo pagina!")
                        continue
                    break

    print("\tHecho!")
    messagebox.showinfo('Info', "Webscraping finalizado.\nEl archivo se encuentra en el directorio './utils/vademecum-pa-")
    return None
