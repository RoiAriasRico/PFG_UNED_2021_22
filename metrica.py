#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para gestionar variables globales

import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import warnings
warnings.filterwarnings("ignore")

#funcion para hacer grafico de la curva roc
def graph_roc_curve(false_positive_rate, true_positive_rate, label=None):
    plt.figure(figsize=(10, 6))
    plt.title('Curva ROC para el clasificador', fontsize=18)
    plt.plot(false_positive_rate, true_positive_rate, label=label)
    plt.plot([0, 1], [0, 1], '#0C8EE0')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('Tasa de Falsos Positivos', fontsize=16)
    plt.ylabel('Tasa de Verdaderos Positivos', fontsize=16)
    plt.annotate('Resultados del analisis \n ', xy=(0.25, 0.9), xytext=(0.4, 0.85),
                 arrowprops=dict(facecolor='#F75118', shrink=0.05),
                 )
