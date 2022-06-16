#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Creado : ROI ARIAS RICO PFG 2021/22
# Fecha de creacion: curso 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
""" Preprocesamiento de tweets"""
# ---------------------------------------------------------------------------
import csv
from os import remove
import preproc
import pandas as pd
from tkinter import *
import re
from pathlib import Path
import combinar_csv
import os



def limpieza_tweet(filename):
    #root = Tk()
    #root.geometry('300x300')
    #window_width = 750
    #window_height = 450
    #s_width = root.winfo_screenwidth()
    #s_height = root.winfo_screenheight()
    #x_cordinate = int((s_width / 2) - (window_width / 2))
    #y_cordinate = int((s_height / 2) - (window_height / 2))
    #root.title("Elementos de la limpieza de tweets")
    #root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    #root.resizable(False, False)


    print("Inicio proceso..\n")


    #name = StringVar(root, value="Comienza el proceso de limpieza...\n")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 100).pack(ipady=5)

    f = open(filename,"r", encoding='utf-8').read()

    #convertir minusculas
    texto = preproc.minusculas(f)
    print("Se ha pasado el texto a minusculas")
    #name = StringVar(root, value="Se ha pasado el texto a minusculas")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    #numero de palabras antes
    global wordCountBefore
    wordCountBefore = len(re.findall(r'\w+', texto))
    print("Palabras antes del preproceso: ",wordCountBefore,"\n")
    #name = StringVar(root, value="El numero de palabras en el texto eran: " + str(wordCountBefore))
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)


    texto = preproc.eliminaArroba(texto)
    print("Se han eliminado @")
    #name = StringVar(root, value="Se ha eliminado la @")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    texto = preproc.eliminaWeb(texto)
    print("Se han eliminado webs")
    #name = StringVar(root, value="Se ha eliminado las direcciones webs")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    texto = preproc.eliminaHashtag(texto)
    print("Se han eliminado #")
    #name = StringVar(root, value="Se ha eliminado los hashtags")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)


    texto = preproc.sustituyeMultiExclamaciones(texto)
    texto = preproc.sustituyeMultiInterrogacion(texto)
    print("Se han eliminado multiexclamaciones y multiinterrogaciones")
    #name = StringVar(root, value="Se han eliminado multiexclamaciones y multiinterrogaciones")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    #name = StringVar(root, value="Se ha empezado a sustituir los emojis...esto puede tardar un poco")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)
    texto = preproc.sustituyeEmoji(texto)
    print("Se han sustituido emojis")
    #name = StringVar(root, value="Se han sustituido los emojis")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    texto = preproc.eliminarWhiteSpace(texto)
    print("Se han sustituido espacio en blanco")

    texto = preproc.eliminarRepeticiones(texto)
    print("Se han sustituido repeticiones")
    #name = StringVar(root, value="Se han eliminado los tweets repetidos")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    texto = preproc.eliminarGuiones(texto)
    texto = preproc.encontrarCorchetes(texto)
    texto = preproc.eliminarCorchetes(texto)
    print("Se han eliminado -, [], *, (), '""'")
    texto = preproc.eliminarAsteriscos(texto)
    texto = preproc.eliminarParentesis(texto)
    texto = preproc.eliminarComillas(texto)
    texto = preproc.eliminarEspacio(texto)
    texto = preproc.ponerPunto(texto)

    #name = StringVar(root, value="Se han eliminado -, [], *, (), """)
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    global wordCountDespues
    wordCountDespues = len(re.findall(r'\w+', texto))  # word count of one sentence before preprocess
    print("Palabras despues del preprocesamiento: ",wordCountDespues,"\n")
    #name = StringVar(root, value="Palabras despues del preprocesamiento: " + str(wordCountDespues))
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    global impureza
    impureza = str(preproc.impurezaTexto(texto) * 100)
    print("El texto tiene una impureza de: " + str(preproc.impurezaTexto(texto) * 100) + "%")
    #name = StringVar(root, value="El texto final tiene una impureza del: " + str(preproc.impurezaTexto(texto) * 100) + "%")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    df = pd.DataFrame([texto])

    fullpath2 = filename + "_preproc.csv"
    df.to_csv(fullpath2, sep = '|', escapechar="*", index=False, header=None, quoting=csv.QUOTE_NONE)

    output_path_text = filename + "_preproc.txt"

    print("FIN del preprocesamiento.\nA continuacion se procede a guardarlo en archivo de texto")
    #name = StringVar(root, value="FIN del preprocesamiento.\nA continuacion se procede a guardarlo en archivo de texto")
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    combinar_csv.csv_to_text(fullpath2, output_path_text)

    print("Se eliminan ficheros intermedios")

    inf = open(fullpath2)
    stripped_lines = [l.lstrip() for l in inf.readlines()]
    inf.close()

    #lineas sin ewspacios en blanco
    outf = open(fullpath2, "w")
    outf.write("".join(stripped_lines))
    outf.close()

    file1 = open(output_path_text, 'r')
    output_path_text = filename + "_preproc2.txt"
    file2 = open(output_path_text,'w')

    for line in file1.readlines():

        if not ((line.startswith('.')) or (line.startswith(' '))):
            file2.write(line)
    file2.close()
    file1.close()


    input_asterisk = output_path_text
    file2 = os.path.splitext(filename)[0] + "_limpio.txt"
    file2_output = open(file2,'w')
    lines = []
    with open(input_asterisk) as f:
        lines = f.readlines()

    for line in lines:
        texto = line
        texto = preproc.ultimaFase(texto)
        file2_output.write(texto)

    file2_output.close()
    f.close()
    remove(input_asterisk)

    lines_seen = set()

    with open(file2, "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i not in lines_seen:
                f.write(i)
                lines_seen.add(i)
        f.truncate()
    remove(fullpath2)

    df = pd.read_csv(file2, skiprows=1, names=['idtweet'])
    df[['idtweet', 'tweet']] = df["idtweet"].str.split(" ", 1, expand=True)
    print(df)
    print(df.columns.values)
    df.to_csv('./data/final_to_csv.csv', sep=",", index=False)
    ruta = Path('./data/final_to_csv.csv').absolute()
    file3 = './data/final_to_csv.csv'
    #eliminacion de archivos intermedios
    print("Se han eliminado archivos intermedios")
    print("Se han eliminado minusculas")
    print("Fin de la conversion a archivo txt")

    data = pd.read_csv('./data/final_to_csv.csv')
    print(data.shape)
    data = data.drop_duplicates(subset='tweet')
    print(data.shape)
    data.to_csv('./data/final_to_csv.csv', sep=",", index=False)
    data2 = data[['tweet']].copy()
    data2.to_csv('./data/txt_limpieza.txt', index=False, header = False)
    ruta2 = Path('./data/txt_limpieza.txt').absolute()

    global ruta_azul
    ruta_azul = str(ruta)
    #name = StringVar(root, value="El archivo limpio se encuentra en : " + str(ruta))
    #nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    global ruta_roja
    ruta_roja = str(ruta2)
    #name = StringVar(root, value="El archivo texto a utilizar en NER se encuentra en : " + str(ruta2))
    #nameTf = Entry(root, textvariable=name, foreground = "red", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)



    return file3


def ver_ventana():

    root = Tk()
    root.geometry('300x300')
    window_width = 750
    window_height = 450
    s_width = root.winfo_screenwidth()
    s_height = root.winfo_screenheight()
    x_cordinate = int((s_width / 2) - (window_width / 2))
    y_cordinate = int((s_height / 2) - (window_height / 2))
    root.title("PRUEBA")
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    root.resizable(False, False)

    name = StringVar(root, value="Comienza el proceso de limpieza...\n")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 100).pack(ipady=5)

    name = StringVar(root, value="Se ha pasado el texto a minusculas")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="El numero de palabras en el texto eran: " + str(wordCountBefore))
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se ha eliminado la @")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se ha eliminado las direcciones webs")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se ha eliminado los hashtags")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se han eliminado multiexclamaciones y multiinterrogaciones")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se ha empezado a sustituir los emojis...esto puede tardar un poco")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se han sustituido los emojis")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se han eliminado los tweets repetidos")
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="Se han eliminado -, [], *, (), """)
    nameTf = Entry(root, textvariable=name, foreground="blue", bg="#f0f0f0", bd=0, width=150).pack(ipady=5)

    name = StringVar(root, value="Palabras despues del preprocesamiento: " + str(wordCountDespues))
    nameTf = Entry(root, textvariable=name, foreground="blue", bg="#f0f0f0", bd=0, width=150).pack(ipady=5)

    name = StringVar(root, value="El texto final tiene una impureza del: " + impureza + "%")
    nameTf = Entry(root, textvariable=name, foreground="blue", bg="#f0f0f0", bd=0, width=150).pack(ipady=5)

    name = StringVar(root, value="FIN del preprocesamiento.\nA continuacion se procede a guardarlo en archivo de texto")
    nameTf = Entry(root, textvariable=name, foreground="blue", bg="#f0f0f0", bd=0, width=150).pack(ipady=5)

    name = StringVar(root, value="El archivo limpio se encuentra en : " + ruta_azul)
    nameTf = Entry(root, textvariable=name, foreground = "blue", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)

    name = StringVar(root, value="El archivo texto a utilizar en NER se encuentra en : " + ruta_roja)
    nameTf = Entry(root, textvariable=name, foreground = "red", bg = "#f0f0f0", bd = 0, width = 150).pack(ipady=5)


    return None