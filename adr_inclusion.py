#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para el clasificador

import numpy as np
import metrica
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from PIL import ImageTk, Image
from sklearn.model_selection import cross_val_score
init_notebook_mode(connected=True)
import os
import spacy
import es_core_news_sm
import nltk
from nltk import SnowballStemmer
import warnings
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score
import time

from sklearn.preprocessing import StandardScaler, LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from tqdm import tqdm
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

dic_metrics = dict();

def nuevoVentana(imagen):
    newWindow = tk.Toplevel()
    newWindow.title("Ventana de grafico")
    #Geometria
    newWindow.geometry("650x650")

    img_temp = Image.open(imagen)
    img_new = img_temp.resize((600, 600))
    img = ImageTk.PhotoImage(img_new)
    label = tk.Label(newWindow, image=img)
    label.image = img
    label.pack()
    label = tk.Label(newWindow, text="La imagen se encuentra en la carpeta graph con el nombre " + imagen,
                     font=('Times', '12'))
    label.image = img
    label.pack()
    return None

def make_adr(filename):

    #leer datos del archivo
    data = pd.read_csv(filename)
    data['adr'] = None

    #leer fichero de ram por medicamento
    data_ram = pd.read_csv('./data/ram.csv', sep=';', header=[0], encoding='utf-8')

    #iterar coincidencias
    for pos, row_ram in data_ram.iterrows():
        contador = 0
        for pos, row in data.iterrows():
            if row_ram.medicamento in row.medicamento:
                if row_ram.ram in row.UMLS:
                    data['adr'].iloc[contador] = "P"
            contador += 1

    data['adr'] = data['adr'].replace(np.nan, 'N')

    #guardar archivo del dataframe
    filename_adr = os.path.splitext(filename)[0] + '_adr.csv'
    data.to_csv(filename_adr, sep=",", index=False, header=True, encoding='utf-8')
    return filename_adr

#DATOS DE NLP, STEMMER Y STOPWORDS----ojo---no hay lemma en espanol
nlp = es_core_news_sm.load()
spanishstemmer=SnowballStemmer('spanish')
stopword_es = nltk.corpus.stopwords.words('spanish')
#inicializar vectorizador de tfidf
tfidf_vectorizer = TfidfVectorizer(stop_words=stopword_es,max_df=0.7)

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


#crear graficos del archivo
def read_adr(filename_adr):

    #se abre archivo csv
    df = pd.read_csv(filename_adr, sep=',', header=[0], encoding='utf-8')
    f,ax = plt.subplots(1,2,figsize=(16,8))

    colores = ["#FA5858", "#64FE2E"]
    etiquetas = 'No RAM','RAM'
    plt.suptitle('Informacion de RAM vs no RAM')
    df['adr'].value_counts().plot.pie(explode=[0,0.05], autopct='%1.2f%%', ax =ax[0], shadow = True,
                                    colors = colores, labels = etiquetas, fontsize =14, startangle=0)

    ax[0].set_ylabel('% de RAM vs No RAM', loc = 'top')

    sns.countplot(x='adr', data=df)
    ax[1].set_xticklabels(['RAM','No RAM'],rotation=0, rotation_mode="anchor")

    #salvar plot
    plt.savefig('./graph/total_RAM.png')
    file_RAM = './graph/total_RAM.png'
    nuevoVentana(file_RAM)
    return None

#parametro del test_train debe ser el mismo que el del read_adr()
def test_train_adr(filename_adr):

    df = pd.read_csv(filename_adr, sep=',', header=[0], encoding='utf-8')

    #Predictores de los resultados
    y = df['adr']
    X = df.drop(['adr'], axis =1)


    #creacion de los sets de training y test
    X_train, X_test, y_train, y_test = train_test_split(
                                             X, y,
                                             test_size=0.30,
                                             random_state=53)

    #se aplica stemmizacion
    X_train['text_proc'] = X_train.text.apply(lemmatize_text)
    X_test['text_proc'] = X_test.text.apply(lemmatize_text)
    X_test.head()


    #inicializa vectorizador
    count_vectorizer = CountVectorizer(stop_words=stopword_es, ngram_range=(1,2))

    #Transformar los datos del training, usando solo los valores de columna: count_train
    count_train = count_vectorizer.fit_transform(X_train.text.values)

    # Transforming los datos del test, usando solo los valores del texto: count_test
    count_test = count_vectorizer.transform(X_test.text.values)


    # Entrenar propio word2vec//OJO!! NO USADO POR PERDIDA DE PRECISION
    #---i = 0
    #---lista_frases = []
    #---for frase in X_train.text.values:
    #---    lista_frases.append(frase.split())
    # ---
    #---w2v_modelo = Word2Vec(lista_frases, min_count=5, vector_size=50, workers=4)

    #---w2v_palabras = list(w2v_modelo.wv.index_to_key)

    #---modelo = TfidfVectorizer()
    #---modelo.fit(X_train.text.values)
    # creacion de un diccionario
    #---diccionario = dict(zip(modelo.get_feature_names(), list(modelo.idf_)))

    # Pesos de TFIDF
    #---tfidf_feat = modelo.get_feature_names()
    #---tfidf_sent_vectors = [];
    #---row = 0;

    #---for sent in lista_frases:
    #---    sent_vec = np.zeros(50)
    #---    weight_sum = 0;
    #---    for palabra in sent:
    #---        if palabra in w2v_palabras and palabra in tfidf_feat:
    #---            vec = w2v_modelo.wv[palabra]
    #---            tf_idf = diccionario[palabra] * (sent.count(palabra) / len(sent))
    #---            sent_vec += (vec * tf_idf)
    #---            weight_sum += tf_idf
    #---    if weight_sum != 0:
    #---        sent_vec /= weight_sum
    #---    tfidf_sent_vectors.append(sent_vec)
    #---    row += 1

    #Inicializar un vector tfidf
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopword_es, max_df=0.7)

    #Transformar los datos de entrenamiento
    tfidf_train = tfidf_vectorizer.fit_transform(X_train.text.values)

    #Transformar los datos del test: tfidf_test
    tfidf_test = tfidf_vectorizer.transform(X_test.text.values)

    #crear un dataframe de count_df
    count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())

    #crear el dataframe de tfidf_df
    tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())

    # Se crea una instancia de un clasificar naive bayes : nb_classifier
    nb_classificador = MultinomialNB()

    # Uso del clasificador para los datos del training
    nb_classificador.fit(count_train, y_train)

    # Se crea los tags de los valores predichos
    pred = nb_classificador.predict(count_test)

    #Calcula la exactitud: score
    score =metrics.accuracy_score(y_test, pred)
    #print(score)

    # Calcula la matriz de confusion
    matriz_confusion = metrics.confusion_matrix(y_test, pred)
    #print(matriz_confusion)


    #OJO!!!CAMBIO
    # # Creating a Multinomial Naive Bayes classifier: nb_classifier
    #nb_classificador = MultinomialNB()

    # # Fitting the classifier to the training data
    #nb_classificador.fit(tfidf_train, y_train)

    # # Creating the predicted tags: pred
    #pred = nb_classificador.predict(tfidf_test)

    # # Calculating the accuracy score: score
    #score = metrics.accuracy_score(y_test, pred)
    # print(score)

    # # Calculating the confusion matrix: cm
    #cm = metrics.confusion_matrix(y_test, pred )
    # print(cm)

    #Etiquetas de las clases de N-B: class_etiquetas
    class_etiquetas = nb_classificador.classes_

    # Extraer las feature: feature_names
    feature_names = tfidf_vectorizer.get_feature_names()

    #Agrupacion por pesos de las features
    feat_with_weights = sorted(zip(nb_classificador.coef_[0],feature_names))

    # Imprimir la primera clase de etiqueta  y el top 10
    #print(class_etiquetas[0], feat_with_weights[:10])

    # Imprimir la segunda clase de la etiqueta y los ultimos 10
    #print(class_etiquetas[1], feat_with_weights[-10:])

    #se inicia el modelo de regresion logistica
    baselog_model = LogisticRegression()
    baselog_model.fit(count_train,y_train)
    y_pred = baselog_model.predict(count_test)
    #se imprime el y_pred
    #print(accuracy_score(y_pred,y_test))

    #________________________________________________________INICIO DE EVALUACION DE ALGORITMOS____________
    #OJO SE USAN OTROS CLASIFICADORES!!!!!!!!!!!!!!!!!!
    #dict_of_algos={'RL':LogisticRegression(),'svc':SVC(),'KNN':KNeighborsClassifier(),
    #               'NB':MLPClassifier(),'RFC':RandomForestClassifier()}
    #def accuracy_of_algos(dic):
    #     df_of_accuracy = pd.DataFrame(columns=['classificador','test_score'])
    #     count=0
    #     for k,v in dic.items():
    #         v.fit(count_train,y_train)
    #         y_pred = v.predict(count_test)
    #         df_of_accuracy.loc[count,'classificador']=k
    #         df_of_accuracy.loc[count,'test_score'] = accuracy_score(y_test,y_pred)
    #         count+=1
    #     return df_of_accuracy
    #print(accuracy_of_algos(dict_of_algos))
    #
    #dict_classifiers = {
    #    "Regresion Logistica": LogisticRegression(),
    #    "KNN": KNeighborsClassifier(),
    #    "Linear SVM": SVC(),
    #    "Random Forest": RandomForestClassifier(n_estimators=18),
    #    'Naive Bayes': MultinomialNB()
    #}
    #num_clasificadores = len(dict_classifiers.keys())

    #def batch_classify(X_train, Y_train, X_test, y_test, verbose=True):
    #    df_results = pd.DataFrame(data=np.zeros(shape=(num_clasificadores, 4)),
    #                              columns=['classificador', 'train_score', 'training_time', 'test_score'])
    #    count = 0
    #    for key, classifier in dict_classifiers.items():
    #        tiempo_inicio = time.perf_counter()
    #       classifier.fit(X_train, Y_train)
    #        tiempo_final = time.perf_counter()
    #        dif_tiempo = tiempo_final - tiempo_inicio
    #        train_score = classifier.score(X_train, Y_train)
    #
    #        y_pred = classifier.predict(X_test)
    #        test_score = accuracy_score(y_test, y_pred)
    #
    #        df_results.loc[count, 'classificador'] = key
    #        df_results.loc[count, 'train_score'] = train_score
    #        df_results.loc[count, 'training_time'] = dif_tiempo
    #        df_results.loc[count, 'test_score'] = test_score
    #
    #        if verbose:
    #            print("entrenado {c} en {f:.2f} s".format(c=key, f=dif_tiempo))
    #        count += 1
    #    return df_results
    #
    #df_resultados = batch_classify(count_train, y_train, count_test, y_test)
    #print(df_resultados.sort_values(by='train_score', ascending=False))

    # Regresion Logistica
    #log_reg = LogisticRegression()
    #log_scores = cross_val_score(log_reg, count_train, y_train, cv=3)
    #lr_media = log_scores.mean()

    # KNN
    #knn_clf = KNeighborsClassifier()
    #knn_scores = cross_val_score(knn_clf, count_train, y_train, cv=3)
    #knn_media = knn_scores.mean()

    # CRF
    #rand_clf = RandomForestClassifier(n_estimators=18)
    #rand_scores = cross_val_score(rand_clf, count_train, y_train, cv=3)
    #rand_media = rand_scores.mean()

    # Naives Bayes
    #nav_clf = MultinomialNB()
    #nav_scores = cross_val_score(nav_clf, count_train, y_train, cv=3)
    #nav_media = nav_scores.mean()

    # Se hace un datafra,me
    #d = {'Clasificadores': ['Regresion Logistica.', 'KNN', 'CRF', 'Naives Bayes'],
    #     'Validacion Cruzada': [lr_media, knn_media, rand_media, nav_media]}

    #result_df = pd.DataFrame(data=d)
    #result_df = result_df.sort_values(by=['Validacion Cruzada'], ascending=False)
    #print(result_df)


    #________________________________________________________FIN DE EVALUACION DE ALGORITMOS____________



    #print("inicio de Regresion logistica")
    logreg_clf = LogisticRegression()
    logreg_clf.fit(count_train, y_train)
    y_pred=logreg_clf.predict(count_test)
    print("Exactitud del Clasificador de entrenamiento de Regresion Logistica : %2.2f" % accuracy_score(y_test, y_pred))

    #parametros de la prueba
    param_test = {
    'penalty':['l1','l2'],
   'class_weight': ['balanced',{'N':0.8,'P':0.2},None],
   'n_jobs' : [-1],
   'C' : [24,25,26],
   'tol':[0.04,0.05,0.06],
   'solver':['liblinear','warn']
    }

    #hipertuning, no grandes resultados
    grid_busqueda = GridSearchCV(estimator = LogisticRegression(random_state=42), param_grid = param_test, scoring='accuracy', cv=3)
    grid_busqueda.fit(count_train,y_train)
    #print(grid_busqueda.best_params_)
    #print(grid_busqueda.best_score_)

    #evaluacion de la logistica
    logreg_clf=LogisticRegression(**grid_busqueda.best_params_, random_state=42)
    logreg_clf.fit(count_train,y_train)
    y_pred = logreg_clf.predict(count_train)
    accuracy_score(y_train,y_pred)
    y_pred = logreg_clf.predict(count_test)
    y_proba = logreg_clf.predict_proba(count_test)[:,1]


    #Creando el dataframe y se guardar en la carpeta data
    X_test_df = pd.DataFrame({'textTweet':X_test.text.values,'Real_RAM':y_test.values,
                          'Predicha_RAM':y_pred.reshape(-1), 'probabilidad_predicha':y_proba.reshape(-1)})
    X_test_df.to_csv("./data/prediccion_adr.csv", sep=",", index=False, header=True, encoding='utf-8')

    #matriz de confusion
    conf_matrix = confusion_matrix(y_test, y_pred)
    f, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', linewidths=.5, ax=ax)
    plt.title("Matriz de Confusion", fontsize=20)
    plt.subplots_adjust(left=0.15, right=0.99, bottom=0.15, top=0.99)
    ax.set_yticks(np.arange(conf_matrix.shape[0]) + 0.5, minor=False)
    ax.set_xticklabels(["Predicha no RAM",'Predicha RAM'],fontsize=16, rotation=360)
    ax.set_yticklabels(['Real NO RAM', 'Real RAM'], fontsize=16, rotation=360)
    #salvar plot
    plt.savefig('./graph/matriz_confusion.png')
    file_matriz = './graph/matriz_confusion.png'
    nuevoVentana(file_matriz)


    # Evaluacion de la metricas
    print('La precision del modelo es del {c} % '.format(c=np.round(precision_score(y_test, y_pred, pos_label = 'P'),2)*100))
    print('El recall del modelo es de {c} % '.format(c=np.round(recall_score(y_test, y_pred, pos_label = 'P'),2)*100))
    print("el f1 es : " + str(f1_score(y_test, y_pred, pos_label = 'P')*100))

    #guardar las metricas en el diccionario de metricas
    precision = np.round(precision_score(y_test, y_pred, pos_label = 'P'),2)*100
    dic_metrics['precision'] = precision
    recall = np.round(recall_score(y_test, y_pred, pos_label = 'P'),2)*100
    dic_metrics['recall'] = recall
    f1 = f1_score(y_test, y_pred, pos_label = 'P')*100
    dic_metrics['f1'] = f1

    plt.figure(figsize=(14,8))
    y_prob=logreg_clf.predict_proba(count_test)[:,1]
    lrd_fpr, lrd_tpr, threshold = roc_curve(y_test, y_prob, pos_label = 'P')
    metrica.graph_roc_curve(lrd_fpr, lrd_tpr, threshold)
    plt.savefig('./graph/roc.png')
    file_roc = './graph/roc.png'
    nuevoVentana(file_roc)

    print('El clasificador de regresion logistica es AUC-ROC : ', roc_auc_score(y_test, y_prob))
    roc_auc = roc_auc_score(y_test, y_prob)
    #GUARDAR EN diccionario de metricas
    dic_metrics['roc_auc'] = roc_auc

    return


#funcion para obtener el diccionario de metricas
def get_metrics():

    return dic_metrics


#print("hasta aqui todo bien")
#****************************************************************************************
