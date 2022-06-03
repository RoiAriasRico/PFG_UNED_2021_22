#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Creado : ROI ARIAS RICO PFG 2021/22
# Fecha de creacion: curso 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
""" Tecnicas de Preprocesamiento"""
# ---------------------------------------------------------------------------
import re
import unicodedata
from unidecode import unidecode

def eliminaArroba(texto):
    """ Cambia "@user" with "atUser" """
    texto = re.sub('@[^\s]+\s','',texto)
    return texto

def eliminarComillas(texto):
    """ Cambia "@user" with "atUser" """
    texto = re.sub('"','',texto)
    return texto

def minusculas(texto):
    """ Cambia el texto a minusculas"""
    texto = texto.lower()
    return texto

def eliminaWeb(texto):
    """ Cambia direccion a http"""
    texto = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',texto)
    texto = re.sub(r'#([^\s]+)', r'', texto)
    return texto

def eliminaHashtag(texto):
    """ Elimina hashtag """
    texto = re.sub(r'#([^\s]+)', r'\1', texto)
    return texto

def sustituyeMultiExclamaciones(texto):
    """ Sustituye multiexclamacion """
    texto = re.sub(r"(\!)\1+", '!', texto)
    return texto

def sustituyeMultiInterrogacion(texto):
    """ Sustituye multiinterrogacion """
    texto = re.sub(r"(\?)\1+", '?', texto)
    return texto

def eliminarAsteriscos(texto):
    """ Elimina hashtag """
    return texto.replace("\*", "")


def sustituyeEmoji(texto):
    """ Sustituye emojis"""
    returnString = ""

    for character in texto:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnString += replaced
            else:
                try:
                    f= unicodedata.name(character).lower()
                    if "laugh" in f: returnString += "risas "
                    elif "arms" in f: returnString += "animo "
                    elif "heart" in f: returnString += "me gusta "
                    elif "vomit" in f: returnString += "enfermo "
                    elif "angry" in f: returnString += "enfadado "
                    elif "poo" in f: returnString += "basura "
                    elif "sleep" in f: returnString += "dormido "
                    elif "joy" in f:returnString += "alegria "
                    elif "party" in f:returnString += "alegria "
                    elif "shrug" in f:returnString += "resignacion "
                    elif "smil" in f:returnString += "risas "
                    elif "money" in f:returnString += "dinero "
                    elif "tired" in f:returnString += "cansado "
                    elif "regional" in f:returnString += ""
                    elif "thumbs up" in f:returnString += "ok "
                    elif "thumbs down" in f:returnString += "no "
                    elif "pensive" in f:returnString += "pensativo "
                    elif "sparkl" in f:returnString += "alegria "
                    elif "litter" in f:returnString += "basura "
                    elif "plead" in f:returnString += "ojala "
                    elif "kiss" in f:returnString += "beso "
                    elif "cry" in f:returnString += "llorar "
                    elif "palm" in f:returnString += "avergonzar "
                    elif "happy" in f:returnString += "feliz "
                    elif "fitzpatrick" in f:returnString += ""
                    elif "collision" in f:returnString += ""
                    elif "variation" in f:returnString += ""
                    elif "handshake" in f:returnString += "ok "
                    elif "ok" in f:returnString += "ok "
                    elif "biceps" in f: returnString += "animo "
                    elif "microphone" in f:returnString += ""
                    elif "persever" in f:returnString += "triste "
                    elif "snake" in f: returnString += "mal "
                    elif "wink" in f:returnString += "ironia "
                    elif "grin" in f: returnString += "alegria "
                    elif "joiner" in f:returnString += ""
                    elif "male" in f:returnString += ""
                    elif "female" in f:returnString += ""
                    elif "dizzy" in f:returnString += "mareado "
                    elif "rolling" in f:returnString += "desaprobacion "
                    elif "call me hand" in f:returnString += "ok "
                    elif "cross" in f:returnString += ""
                    elif "clap" in f:returnString += "aplauso "
                    elif "megaphone" in f:returnString += ""
                    elif "check" in f:returnString += ""
                    elif "woman" in f:returnString += ""
                    elif "hug" in f: returnString += "animo "
                    elif "pout" in f:returnString += "enfado "
                    elif "confuse" in f:returnString += "confuso "
                    elif "astonished" in f:returnString += "sorprendido "
                    elif "musical" in f:returnString += ""
                    elif "cowboy" in f:returnString += ""
                    elif "think" in f:returnString += "pensativo "
                    elif "pill" in f:returnString += ""
                    elif "star" in f:returnString += ""
                    elif "wavy" in f:returnString += "irritacion "
                    elif "clown" in f:returnString += ""
                    elif "disappoint" in f:returnString += "desilusion "
                    elif "monocle" in f: returnString += "cuidado "
                    elif "japanese" in f: returnString += ""
                    elif "monkey" in f: returnString += ""
                    elif "beverage" in f: returnString += ""
                    elif "rainbow" in f:returnString += ""
                    elif "eyebrow" in f:returnString += "sorprendido "
                    elif "airplane" in f:returnString += ""
                    elif "victory" in f:returnString += "exito "
                    elif "point" in f:returnString += ""
                    elif "old" in f:returnString += ""
                    elif "rays" in f:returnString += ""
                    elif "man" in f:returnString += ""
                    elif "frown" in f:returnString += "triste "
                    elif "rose" in f:returnString += ""
                    elif "fire" in f:returnString += ""
                    elif "exclamation" in f:returnString += ""
                    elif "runner" in f:returnString += ""
                    elif "massage" in f:returnString += "relajacion "
                    elif "smirk" in f:returnString += "ironia "
                    elif "robot" in f:returnString += ""
                    elif "nail" in f:returnString += ""
                    elif "syringe" in f:returnString += ""
                    elif "white hair" in f:returnString += ""
                    elif "worr" in f:returnString += "preocupado "
                    elif "moon" in f:returnString += ""
                    elif "police" in f:returnString += ""
                    elif "love" in f:returnString += "encanta "
                    elif "house" in f:returnString += ""
                    elif "serious" in f:returnString += "serio "
                    elif "upsidedown" in f:returnString += ""
                    elif "square" in f:returnString += ""
                    elif "silhouette" in f:returnString += ""
                    elif "weary" in f:returnString += "cansado "
                    elif "celebration" in f:returnString += "alegria "
                    elif "gorilla" in f:returnString += ""
                    elif "balloon" in f:returnString += ""
                    elif "fear" in f:returnString += "miedo "
                    elif "relieve" in f:returnString += "relajada "
                    elif "car" in f:returnString += ""
                    elif "nausea" in f:returnString += "mareado "
                    elif "mobile" in f:returnString += ""
                    elif "shamrock" in f:returnString += "mareado "
                    elif "car" in f:returnString += ""
                    elif "tongue" in f:returnString += "alegria "
                    elif "leaf" in f:returnString += ""
                    elif "brain" in f:returnString += ""
                    elif "confound" in f:returnString += "confundido "
                    elif "savouring" in f:returnString += ""
                    elif "yawn" in f:returnString += "cansado "
                    elif "drool" in f:returnString += "me gusta "
                    elif "wine" in f:returnString += ""
                    elif "suit" in f:returnString += ""
                    elif "footprint" in f:returnString += ""
                    elif "goggle" in f:returnString += ""
                    elif "handbag" in f:returnString += ""
                    elif "herb" in f:returnString += ""
                    elif "flush" in f:returnString += "avergonzada "
                    elif "closed lips" in f:returnString += "secreto "
                    elif "chick" in f:returnString += ""
                    elif "suit" in f:returnString += ""
                    elif "sheep" in f:returnString += ""
                    elif "grimace" in f:returnString += "miedo "
                    elif "expressionless" in f:returnString += "enfadado "
                    else:
                        #returnString += "[" + unicodedata.name(character).lower() + "]"
                        returnString += ""
                except ValueError:
                    returnString += "[x]"

    return returnString

def eliminarWhiteSpace(texto):
    """ Elimina espacios en blanco: \t, \x0b, \x0c, \f """
    texto = re.sub(r'\t\f\x0b\x0c\n\r', r'', texto)
    return texto

def eliminarGuiones(texto):
    """ Elimina guiones """
    texto = re.sub(r'-', r'', texto)
    return texto

def eliminarRepeticiones(texto):
    """Cualquier repeticion de caracter, se reduce a como maximo 2"""
    texto = re.sub(r"(.)\1+", r"\1\1", texto)
    return texto
def encontrarCorchetes(texto):
    """Encontrar corchetes"""
    counter = 0
    combos_patt = re.compile(r'\[.*?\]')
    combos = combos_patt.findall(texto)
    for combo in combos:
        counter += 1
    return texto

def eliminarCorchetes(texto):
    """Eliminar corchetes"""
    return texto.replace('[', '').replace(']', '')
def eliminarParentesis(texto):
    """Eliminar parentesis"""
    return texto.replace('(', '').replace(')', '')

def ponerPunto(texto):
    """Eliminar parentesis"""
    return texto.replace('\n', '.\n')

def eliminarEspacio(texto):
   return re.sub(' +', ' ', texto.strip())

def ultimaFase(texto):
    texto = texto.replace("*", "");
    texto = texto.replace("..", ".")
    texto = texto.replace(". .", ".")

    return texto
def impurezaTexto(texto, min_len=10):
    """comprobar pureza del texto"""
    RE_SOSPECHOSO = re.compile(r'[&#<>{}\[\]\\]')
    if texto == None or len(texto) < min_len:
        return 0
    else:
        return len(RE_SOSPECHOSO.findall(texto))/len(texto)


