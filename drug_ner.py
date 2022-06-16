#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Incorpora una propia NER

import json
import spacy
import es_core_news_md
from spacy.lang.es import Spanish
from spacy.tokens import Span
from spacy import displacy
from spacy.matcher import Matcher
import config
import ner_matching
from nltk import SnowballStemmer
import tkinter as tk

text = ""
spanishstemmer = SnowballStemmer('spanish')

def lanzar():

    #funcion para normalizar texto
    def normalize(text):
        doc = nlp(text)
        palabras = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        lexical_tokens = [t.lower() for t in palabras if len(t) > 3 and
        t.isalpha()]
        return lexical_tokens

    #es un stemmer, porque no hay lemma en espanol
    def lemmatize_text(text):
        return ' '.join(spanishstemmer.stem(token) for token in normalize(text))

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
                            print(x)
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
    nlp = es_core_news_md.load()
    original_ents = ()
    #reconoce patron en el texto
    def reconocer_patron(patterns, text):
        nlp = Spanish()
        ruler = nlp.add_pipe("entity_ruler", last = True)

        patterns_med = patterns
        ruler.add_patterns(patterns_med)

        doc = nlp(text)
        nlp.to_disk('nlp_drug')
        results = []
        for ent in doc.ents:
            results.append(ent.text)
            print(ent.text+ '-'+ str(ent.label_))
        #displacy.serve(doc, style="ent")
        return (results)

    if config.chk_value == 1:
        #abrir archivo
        with open(config.file_ner, "r") as f:
            print("Se aplica stemming")
            text = f.read()
            text = lemmatize_text(text)
    else:
        with open(config.file_ner, "r") as f:
            text = f.read()

    hits = []
    ie_data = {}
    results = reconocer_patron(patterns, text)
    tk.messagebox.showwarning(title=None, message="Se inicia la deteccion de terminos medicos")
    ##DESDE AQUI QUICKUMLS
    nlp_reloaded = spacy.load('nlp_drug')
    doc = nlp_reloaded(text)
    for entity in doc.ents:
        if not (entity.label_ == "medicamento"):
            span = Span(doc, entity.start, entity.end, label="sintoma_UMLS")
            doc.ents = [span if e == entity else e for e in doc.ents]

    from quickumls import QuickUMLS

    #try:
    print(config.quick_name)
    matcher = QuickUMLS(config.quick_name, overlapping_criteria = "score", threshold = 0.6,
                        similarity_name = "jaccard", window = 5)
    print("matcher acabada, pendiente de matches")
    matches = matcher.match(text, best_match=False, ignore_syntax=False)
    #except:
    #tk.messagebox.showerror(title="Error en QuickUMLS", message="No se ha indicado un directorio correcto donde se encuentra quick y simstring.")

    n = 0

    check = False
    listas=[]
    for match in enumerate(matches):
        print(match)
        coincide = 0
        print('Name: ', matches[n][0]['term'], matches[n][0]['cui'], matches[n][0]['similarity'],matches[n][0]['semtypes'])
        span = doc.char_span(matches[n][0]['start'], matches[n][0]['end'])
        span = Span(doc, span.start, span.end, label="UMLS")
        nombre_span = matches[n][0]['ngram'].lower()
        print(nombre_span)
        for i in doc.ents:
            if (nombre_span == i.text) and (i.label_ != "UMLS"):
                coincide = 1
                break
        if not (coincide == 1):
            if(nombre_span == 'vitamina') or (nombre_span == 'vitaminas'):
                post_token = doc[span.end:span.end+1]
                if(post_token.text in ('a', 'b', 'c', 'd', 'e', 'k')):
                    span = Span(doc, span.start, span.end+1, label="UMLS")
                    doc.ents = list(doc.ents) + [span]
                    listas.append(nombre_span)
            else:
                doc.ents = list(doc.ents) + [span]
                listas.append(nombre_span)
        n +=1
        i = 0

    final_listas = list(dict.fromkeys(listas))
    textfile = open("./data/lista_umls.txt", "w")
    for element in final_listas:
        textfile.write(element + "\n")
    textfile.close()

    nlp_dosis = Spanish()

    #crea el ruler y lo incorpora a nlp
    matcher = Matcher(nlp_dosis.vocab)

    #Lista de entidades y patrones
    patterns_dosis = [[{"SHAPE": "dd"}, {"ORTH": "mg"}], [{"SHAPE": "dd"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
    [{"SHAPE": "ddd"}, {"ORTH": "mg"}], [{"SHAPE": "ddd"}, {"IS_SPACE": True}, {"ORTH": "mg"}],
    [{"SHAPE": "d"}, {"ORTH": "mg"}], [{"SHAPE": "d"}, {"IS_SPACE": True}, {"ORTH": "mg"}]]

    matcher.add("dosis", patterns_dosis)
    doc_dosis = nlp_dosis(text)
    matches = matcher(doc_dosis)
    for match_id, start, end in matches:
        string_id = nlp_dosis.vocab.strings[match_id]
        span = doc[start:end]
        span = Span(doc, span.start, span.end, label="dosis")
        doc.ents = list(doc.ents) + [span]


    for result in results:
        hits.append(result)
    ie_data = hits
    guardar_data("./data/med_data.json", ie_data)

    #configuracion de displacy
    colors = {"dosis": "linear-gradient(90deg, #ffbf72, #a8eb12);", "UMLS": "linear-gradient(180deg, #66ffcc, #abf763)", "medicamento": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
    options = {"ents": ["medicamento", "UMLS", "dosis"], "colors": colors}

    displacy.render(doc, style='ent', options=options, jupyter=False)
    html = displacy.render(doc, style='ent', options=options, page=True)

    if config.chk_value != 1:
        with open("./data/NER_displacy.html", 'w+', encoding="utf-8") as fp:
            fp.write(html)
            fp.close()
        #print("FIN DEL NER.\nA continuacion, se procede a la extraccion de entidades para el posterior paso")
        tk.messagebox.showwarning(title=None, message="Finalizado NER, tras acabar la ejecucion, puede ver archivo HTML\n(presione Abrir Archivo HTML).\n\nAhora comienza generacion de archivos")

    #EXTRACCION DE ENTIDADES
    ner_matching.archivo(config.file_ner)

    config.visibility = True

    tk.messagebox.showwarning(title=None, message="Finalizado NER y su extraccion en archivos. \n Si desea concatenar los resultados de varios archivos, pulse el botón Concatenar archivos.")

    return None


