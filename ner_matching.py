#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para crear archivos de entidades

import json
import pandas as pd
import spacy
from spacy.lang.es import Spanish
from spacy.tokens import Span
from spacy.matcher import Matcher
import tkinter as tk

def archivo(file):
    with open(file, 'r') as f:
        text = [line for line in f.readlines()]
        #print(text)
    df = pd.DataFrame(text,columns=['text'])
    df['dosis'] = None
    df['medicamento'] = None
    df['UMLS'] = None
    df.head()

    def get_dosis(x):

        counter = 0
        for line in text:
            nlp_dosis = Spanish()
            matcher = Matcher(nlp_dosis.vocab)

            #Lista de entidades y patrones
            patterns_dosis = [
                [{"SHAPE": "dd"}, {"ORTH": "mg"}], [{"SHAPE": "dd"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
            [{"SHAPE": "ddd"}, {"ORTH": "mg"}], [{"SHAPE": "ddd"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
            [{"SHAPE": "d"}, {"ORTH": "mg"}], [{"SHAPE": "d"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
            [{"SHAPE": "dd"}, {"ORTH": "mgs"}], [{"SHAPE": "dd"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
            [{"SHAPE": "ddd"}, {"ORTH": "mgs"}], [{"SHAPE": "ddd"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
            [{"SHAPE": "d"}, {"ORTH": "mgs"}], [{"SHAPE": "d"}, {"IS_SPACE": True}, {"ORTH": "mg"}]
                          ]

            matcher.add("dosis", patterns_dosis)
            doc_dosis = nlp_dosis(line)
            matches = matcher(doc_dosis)
            if not matches:
            #print("esto esta vacio")
                df['dosis'].iloc[counter] = 'no'
            else:
                lista_dosis = []
                for match_id, start, end in matches:
                    string_id = nlp_dosis.vocab.strings[match_id]  # Get string representation
                    span = doc_dosis[start:end]  # The matched spa
                    span = Span(doc_dosis, span.start, span.end, label="dosis")
                    doc_dosis.ents = list(doc_dosis.ents) + [span]
                    lista_dosis = list(lista_dosis) + [span.text]
                    df['dosis'].iloc[counter] = lista_dosis
            counter += 1
        tk.messagebox.showwarning(title=None,message="En progreso...")
        #print("FIN DE LA ETAPA DE BUSCAR DOSIS")
        return df
#cargar datos del archivo json de medicamentos

    def cargar_datos(file):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            lista = []
            for x in data:
                values = x.values()
                lista.extend(values)
        return (lista)

    hp_chars = cargar_datos("./data/json_med.json")

#salvar datos de reconocimiento como archivo json
    def guardar_data(file, data):
        with open (file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

#perfeccionar el pattern del archivo
    def mejor_pattern(file):
        data = cargar_datos(file)
        new_med = []
        for item in data:
            new_med.append(item)
        for item in data:
            item = item.replace("de", "").replace("De", "").replace("y", "").replace("y", "")
            names = item.split()
            for name in names:
                name = name.strip()
                new_med.append(name)
            if "(" in item:
                names = item.split("(")
                for name in names:
                    name = name.replace(")", "").strip()
                    new_med.append(name)
            if "," in item:
                names = item.split(",")
                for name in names:
                    name = name.replace("y", "").strip()
                    if " " in name:
                        new_names = name.split()
                        for x in new_names:
                            x = x.strip()
                            new_med.append(x)

                    new_med.append(name)
        final_med = []
        for character in new_med:
            final_med.append(character)
        final_med = list(set(final_med))
        final_med.sort()
        return(final_med)

#crear pattern
    def create_training_data(file,type):
        data = mejor_pattern(file)
        patterns =[]
        for item in data:
            pattern = {
                    "label": type,
                    "pattern": item
            }
            patterns.append(pattern)
        new_pattern = []

        for mdict in patterns:
            new_dict = {}
            for key, value in mdict.items():
                new_dict[key] = value.lower()
            new_pattern.append(new_dict)
        return (new_pattern)

    patterns = create_training_data("./data/json_med.json", "MEDICAMENTO")

    nlp = spacy.load('es_core_news_md')
    #reconoce patron en el texto
    def reconocer_patron(patterns, text):
        counter = 0
        for line in text:
            lista_med = []
            nlp = Spanish()
            ruler = nlp.add_pipe("entity_ruler", last = True)
            patterns_med = patterns
            ruler.add_patterns(patterns_med)
            doc = nlp(line)
            nlp.to_disk('nlp_drug')
            results = []
            for ent in doc.ents:
                lista_med = list(lista_med) + [ent.text]
                df['medicamento'].iloc[counter] = lista_med

            counter += 1

        #print("FIN DE LA ETAPA DE BUSCAR MEDICAMENTOS")
        return df

    def get_umls(x):
        with open('./data/lista_umls.txt') as f:
            linesUMLS = f.read().splitlines()
        #print(linesUMLS)
            contador = 0
            for line in text:
                lista_umls = []
                for key in linesUMLS:
                    if key in line:
                        lista_umls= list(lista_umls) + [key]
                        df['UMLS'].iloc[contador] = lista_umls
                        #print(lista_umls)
                contador += 1

        return df


    df3 = get_dosis(text)

    df_med = reconocer_patron(patterns, text)
    df_umls = get_umls(text)

    df6 = df_umls.loc[(df['UMLS'].notnull()) & (df['medicamento'].notnull())]
    #print(df6)
    import config
    import os
    filedir = os.path.splitext(config.file_ner)[0]
    df6.to_csv(filedir + '_ent.csv', sep=",", index=False, header=True, encoding='utf-8')
    tk.messagebox.showwarning(title=None, message="El archivo resultante se encuentra en : \n" + filedir + "_ent.csv")
    #print('LISTO')

    return None