#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import csv
import requests
import string
import urllib.request as urllib2
from bs4 import BeautifulSoup
from tkinter import messagebox

def vademecum_med():
    #iteracion en las 26 letras
    letter_list = string.ascii_lowercase[:26]

    for letter in letter_list:

        with open('./utils/vademecum-med' + str(letter) + '.csv', 'w') as csvfile:
            #Se salva cn, nombre y url
            fieldnames = ['cod_nacion', 'nombre', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            print("Inicio letra " + str(letter))
            vademecum = "http://vademecum.es/medicamentos-" + letter + "_1"
            #print(vademecum)

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
                print('http://vademecum.es' + str(link['href']))
                page = None
                while True:
                    try:
                        page = urllib2.urlopen(req, timeout=3).read()
                    except (KeyboardInterrupt, SystemExit):
                        raise
                    except:
                        print("\t\t[ERROR] Excepcion intentando abrir pagina")
                        continue
                    break

                drug_soup = BeautifulSoup(page, "html.parser")
                for elem in drug_soup.findAll("strong"):
                    if "Código Nacional:" in elem.contents[0]:
                        drug_code = elem.parent.find("span").contents[0].strip()
                        print(drug_code)
                        print("\tGetting drug " + drug_code + " (" + letter + "-" + str(i) + ")")
                        writer.writerow({'cod_nacion': drug_code, 'nombre': drug_name2, 'url': drug_link})

    messagebox.showinfo('Info', "Webscraping finalizado.\nEl archivo se encuentra en el directorio './utils/vademecum-med")
    print("\tHecho!")
    return None


