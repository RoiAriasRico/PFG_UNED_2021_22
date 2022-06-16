#!/usr/bin/env python3  Line 1
# -*- coding: utf-8 -*- Line 2
#----------------------------------------------------------------------------
# Created By  : ROI ARIAS RICO  Line 3
# PFG 2021/22
# version ='1.0'
# ---------------------------------------------------------------------------
# Modulo para GUI de la app
import math
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import filedialog as fd
import tkinter.ttk as ttk
import pandas as pd
import config
import webbrowser
import os
import glob
import adr_inclusion
import preproc_tweets
import req_vademecum_pa
import req
import concat
import drug_ner


window_width =1300
window_height = 550

def about():
    messagebox.showinfo('Info', "Sistema de deteccion de efectos adversos.\nPFG 2021/22 Universidad Nacional de Educación a Distancia")

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        ## Poniendo el principio
        self.title("Sistema para la deteccion de efectos adversos-PFG 2021/22")
        self.geometry("720x550")
        self.resizable(False, False)

        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        x_cordinate = int((s_width / 2) - (window_width / 2))
        y_cordinate = int((s_height / 2) - (window_height / 2))

        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        ##Creacion del contenedor
        container = tk.Frame(self, bg="#8AA7A9")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(5, weight=1)
        container.grid_columnconfigure(0, weight=1)

        ##Inicializar frames
        self.frames = {}
        self.HomePage = HomePage
        self.Visualizacion = Visualizacion
        self.Limpieza= Limpieza
        self.NER = NER
        self.Herramientas = Herramientas
        self.Clasificacion = Clasificacion
        self.res_Final = res_Final
        self.UnPaso = UnPaso

        ## Definiendo los frames y se pack
        for F in {HomePage, Visualizacion, Limpieza, NER, Herramientas, Clasificacion, res_Final, UnPaso}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=5, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        menubar = frame.create_menubar(self)
        self.configure(menu=menubar)
        frame.tkraise()

# ---------------------------------------- HOME PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class HomePage(tk.Frame):


    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Bienvenidos al sistema para la detección de efectos adversos a los medicamentos", font=('Times', '16'))
        label.pack(pady=0, padx=0)
        #imagen
        image = Image.open('uned.png')
        display = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=display)
        label.image = display
        label.pack(pady=0, padx=0)
        label = tk.Label(self, text="PFG 2021/2022", font=('Times', '14'))
        label.pack(pady=0, padx=0)


        #frame de los rb
        self.var_system = IntVar()
        self.var_system.set(0)

        frame = tk.LabelFrame(self, text="Puede seleccionar las opciones siguientes o elegir la barra del menu:", font=('Times', '14'), padx=50)
        frame.pack(pady=30, padx=0)

        rb1 = Radiobutton(frame, text="Visualizacion de tweets",  variable=self.var_system, command = lambda: parent.show_frame(parent.Visualizacion),
                    value=1, padx= 150).pack(anchor= "w")
        rb2 =tk.Radiobutton(frame, text="Limpieza de tweets", variable=self.var_system, command = lambda: parent.show_frame(parent.Limpieza),
                    value=2, padx= 150).pack(anchor= "w")
        rb3 = Radiobutton(frame, text="Reconocimiento de entidades", variable=self.var_system, command = lambda: parent.show_frame(parent.NER),
                    value=3, padx= 150).pack(anchor= "w")
        rb4 = Radiobutton(frame, text="Clasificacion de textos", variable=self.var_system, command = lambda: parent.show_frame(parent.Clasificacion),
                    value=4, padx= 150).pack(anchor= "w")
        rb5 = Radiobutton(frame, text="Resultados finales", variable=self.var_system, command = lambda: parent.show_frame(parent.res_Final),
                    value=5, padx= 150).pack(anchor= "w")
        rb6 = Radiobutton(frame, text="Un solo paso", variable=self.var_system, command = lambda: parent.show_frame(parent.UnPaso),
                    value=6, padx= 150).pack(anchor= "w")


    #se crea el menubar
    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## menu de herramientas
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar


# ---------------------------------------- Visualizacion PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class Visualizacion(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)
        #label para apertura de archivo
        file_frame = tk.LabelFrame(self, text="Abrir archivo")
        file_frame.place(height=90, width=1300)

        #botones
        boton1 = tk.Button(file_frame, text="Paso1-Explorar archivo", command=lambda: File_dialog())
        boton1.place(rely=0.35, relx=0.20)

        boton2 = tk.Button(file_frame, text="Paso2-Cargar archivo", command=lambda: Load_csv_data())
        boton2.place(rely=0.35, relx=0.50)

        #etiqueta con la ruta del archivo
        label_file = ttk.Label(file_frame, text="Ningun archivo seleccionado")
        label_file.place(rely=0, relx=0)

        #INICIO TREE
        frame1 = tk.LabelFrame(self, text="Visualizacion de tweets")
        frame1.place(height=450, width=1300, rely=0.13, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(frame1)
        #ajustar el frame al padre
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(frame1, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # scrollbars
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        #funcion para el dialogo del archivo
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos csv", "*.csv"), ("Todos los archivos", "*.*")))

            label_file["text"] = filename
            return None

        #funcion para cargar el archivo en el treeview
        def Load_csv_data():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding = 'utf-8') as file:
                df = pd.read_csv(file, sep=',', header= [0], encoding='utf-8-sig')
            clear_data()
            tv1["column"] = "idtweets", "tweets"
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column)
                tv1.column("tweets", minwidth=0, width=50, stretch=False)
                tv1.column("idtweets", minwidth=0, width=1250, stretch=False)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end", values=row)
            return None

        #boton para la limpieza de tweets, llama a la funcion limpieza
        boton3 = tk.Button(self, text="Limpieza de tweets >>", command=lambda: parent.show_frame(parent.Limpieza))
        boton3.place(rely=0.95, relx=0.90)

        #limpieza de datos
        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

    #crear barra de menu
    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## menu de herramientas
        tools_bar = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_bar)
        tools_bar.add_command(label="Herramientas para NER", command=lambda: parent.show_frame(parent.Herramientas))
        tools_bar.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar

# ---------------------------------------- Limpieza PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class Limpieza(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Limpieza de tweets", font=('Times', '20'))
        label.pack(pady=0, padx=0)

        super().__init__(container)
        #dialogo de abrir archivo
        file_frame = tk.LabelFrame(self, text="Abrir archivo")
        file_frame.place(height=90, width=1300)
        # Botones
        boton1 = tk.Button(file_frame, text="Paso1-Explorar archivo", command=lambda: File_dialog())
        boton1.place(rely=0.35, relx=0.15)

        boton2 = tk.Button(file_frame, text="Paso2-Cargar archivo", command=lambda: Load_csv_data())
        boton2.place(rely=0.35, relx=0.40)

        boton4 = tk.Button(file_frame, text="Paso3-Limpiar texto", command=lambda: limpieza_data())
        boton4.place(rely=0.35, relx=0.65)

        # ruta del archivo
        label_file = ttk.Label(file_frame, text="Ningun archivo seleccionado")
        label_file.place(rely=0, relx=0)



        #INICIO TREE
        frame1 = tk.LabelFrame(self, text="Limpieza de textosRe")
        frame1.place(height=450, width=1300, rely=0.13, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(frame1, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        #funcion para abrir el dialogo del archivo
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos csv", "*.csv"), ("Todos los archivos", "*.*")))

            label_file["text"] = filename
            if label_file["text"] == "":
                tk.messagebox.showwarning(title=None,message="No ha seleccionado ningun archivo para NER")
            return None

        #cargar el archivo
        def Load_csv_data():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding = 'utf-8') as file:
                df = pd.read_csv(file, sep=',', header= [0], encoding='utf-8')
            clear_data()
            tv1["column"] = "idtweets", "tweets"
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column)
                tv1.column("idtweets", minwidth=0, width=50, stretch=False)
                tv1.column("tweets", minwidth=0, width=1250, stretch=False)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end", values=row)
            return None

        #funcion para limpiar los datos
        def limpieza_data():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding='utf-8') as file:
                filename2 = preproc_tweets.limpieza_tweet(label_file["text"])
                df = pd.read_csv(filename2, sep=',', header= [0], encoding='utf-8')
            clear_data()
            tv1["column"] = "idtweets","tweets"
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column)
                tv1.column("idtweets", minwidth=0, width=70, stretch=False)
                tv1.column("tweets", minwidth=0, width=1230, stretch=False)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end",
                           values=row)
            label_1 = ttk.Label(file_frame, text="Archivo final: " + str(filename2), foreground = "blue")
            label_1.place(rely=0, relx=0.55)
            return None

        button5 = tk.Button(self, text="Visualizar resultados limpieza", command=lambda: visualizar_Ventana())
        button5.place(rely=0.95, relx=0.40)

        # funcion para visualizar ventana
        def visualizar_Ventana():
            preproc_tweets.ver_ventana()

            return None

        button3 = tk.Button(self, text="Reconocimiento de entidades >>", command=lambda: parent.show_frame(parent.NER))
        button3.place(rely=0.95, relx=0.80)



        #limpieza de datos
        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

    #funcion de la barra de menu
    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## proccessing menu
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar

# ---------------------------------------- Reconocimiento de entidades PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class NER(tk.Frame):

    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Reconocimiento de entidades", font=('Times', '20'))
        label.pack(pady=0, padx=0)
        super().__init__(container)
        # dialogo de abrir archivo
        file_frame = tk.LabelFrame(self, text="Abrir archivo")
        file_frame.place(height=90, width=1300)
        # Botones
        boton1 = tk.Button(file_frame, text="Paso1-Especifique directorio quickumls", command=lambda: File_dialog_quick())
        boton1.place(rely=0.35, relx=0.0)

        boton2 = tk.Button(file_frame, text="Paso2-Explorar archivo", command=lambda: File_dialog())
        boton2.place(rely=0.35, relx=0.30)

        boton3 = tk.Button(file_frame, text="Paso3-Cargar archivo", command=lambda: Load_csv_data())
        boton3.place(rely=0.35, relx=0.55)

        seleccion=tk.IntVar()
        c = tk.Checkbutton(file_frame, text="Aplicar stemming", command = lambda: cambiarestado(), variable= seleccion)
        c.place(rely =0.35, relx = 0.70)

        boton4 = tk.Button(file_frame, text="Paso4-Reconocimiento de entidades", command=lambda: lanzar_NER())
        boton4.place(rely=0.35, relx=0.80)

        #ruta del archivo
        label_file = ttk.Label(file_frame, text="Se recomienda abrir los archivos ya limpios en la fase previa, con formato txt")
        label_file.place(rely=0, relx=0.30)

        #ruta del directorio de quick
        label_quick = ttk.Label(file_frame, text="Seleccione el directorio donde se encuentra quickumls")
        label_quick.place(rely=0, relx=0.0)

        #INICIO TREE
        frame1 = tk.LabelFrame(self, text="Reconocimiento de entidades")
        frame1.place(height=450, width=1300, rely=0.13, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(frame1, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        #funciones de apertura del directorio de quick
        def File_dialog_quick():
            """Dialogo del archivo"""
            dirname = fd.askdirectory(initialdir="", title="Seleccione el directorio")

            label_quick["text"] = dirname
            config.quick_name = dirname
            return config.quick_name

        #funciones de apertura del directorio de quick
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos txt", "*.txt"), ("Todos los archivos", "*.*")))

            label_file["text"] = filename
            if label_file["text"] == "":
                tk.messagebox.showwarning(title=None,message="No ha seleccionado ningun archivo para NER")
            config.file_ner = filename
            #print("EL ARCHIVO DE NER ES: " + config.file_ner)
            return config.file_ner

        #funcion para cargar archivo
        def Load_csv_data():
            """Si el archivo es correcto se carga en el treeview"""
            # abrir archivo
            with open(label_file["text"], encoding = 'utf-8') as f:
                texto_prueba = f.read()
                if (len(texto_prueba) > 900000):
                    tk.messagebox.showwarning(title=None, message="El archivo tiene mas caracteres que \nla capacidad para gestionar NER.\nPor favor, utilice las herramientas de dividir archivos situado en \n la barra de menu Herramientas. Gracias")
                else:
                    with open(label_file["text"], encoding = 'utf-8') as file:
                        df = pd.read_csv(file, sep='\"', header= None, encoding='utf-8')
                    clear_data()
                    tv1["column"] = "tweets"
                    tv1["show"] = "headings"
                    for column in tv1["columns"]:
                        tv1.heading(column, text=column)
                        tv1.column("tweets", minwidth=0, width=1300, stretch=False)
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        tv1.insert("", "end",
                                   values=row)
            mostrar_boton()
            return None
        #funcion para realizar el trabajo de NER
        def lanzar_NER():
            tk.messagebox.showwarning(title=None, message="Se inicia NER")
            drug_ner.lanzar()
            return None

        def callback():
            import os
            webbrowser.open("file://" + os.path.realpath("./data/NER_displacy.html"))

        boton3 = tk.Button(self, text="Abrir archivo HTML >>", command=callback)
        boton3.place(rely=0.95, relx=0.20)

        boton5 = tk.Button(self, text="Clasificacion de textos >>", command=lambda: parent.show_frame(parent.Clasificacion))
        boton5.place(rely=0.95, relx=0.50)

        #boton para resultados NER
        def mostrar_boton():
            button4 = tk.Button(self, text="Concatenar resultados NER >>", command=concat_NER)
            button4.place(rely=0.95, relx=0.80)
            return None

        #concatener todas las NER
        def concat_NER():
            appended_data = []
            for infile in glob.glob("./data/sa" + "*ent.csv"):
                data = pd.read_csv(infile)
                appended_data.append(data)
            appended_data = pd.concat(appended_data)
            # paso del dataframe a csv
            try:
                appended_data.to_csv('./data/ext_full.csv', sep=",", index=False, header=True, encoding='utf-8')
                tk.messagebox.showwarning(title="Fin de la concatenacion", message="Se hane concatenado los archivos.\n\nEl archivo final se encuentra en ./data/ext_full.csv")
            except:
                messagebox.showerror('Error en la concatenacion', 'Error en la concatenacion')
        #aplicar stemming o no
        def cambiarestado():
            if seleccion.get() == 1:
                config.chk_value = 1
            if seleccion.get() == 0:
                config.chk_value = 0

        #limpiar datos
        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## menu de herramientas
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar

# ---------------------------------------- Clasificacion PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class Clasificacion(tk.Frame):

    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Clasificacion de textos", font=('Times', '20'))


        label.pack(pady=0, padx=0)

        super().__init__(container)
        # abrir archivo
        file_frame = tk.LabelFrame(self, text="Abrir archivo")
        file_frame.place(height=90, width=1300)
        # botones
        boton1 = tk.Button(file_frame, text="Paso1-Explorar archivo", command=lambda: File_dialog())
        boton1.place(rely=0.35, relx=0.10)

        boton2 = tk.Button(file_frame, text="Paso2-Cargar archivo", command=lambda: Load_csv_data())
        boton2.place(rely=0.35, relx=0.30)

        boton3 = tk.Button(file_frame, text="Opcional-Ver metricas", command=lambda: metricas_user())
        boton3.place(rely=0.35, relx=0.80)

        boton4 = tk.Button(file_frame, text="Paso3-Clasificacion", command=lambda: clasificacion())
        boton4.place(rely=0.35, relx=0.50)

        seleccion=tk.IntVar()
        c = tk.Checkbutton(file_frame, text="Datos anotados", command = lambda: cambiarAnotacion(), variable= seleccion)
        c.place(rely =0.35, relx = 0.60)

        # ruta del archivo
        label_file = ttk.Label(file_frame, text="Ningun archivo seleccionado")
        label_file.place(rely=0, relx=0)

        #INICIO TREE
        frame1 = tk.LabelFrame(self, text="Clasificacion")
        frame1.place(height=450, width=1300, rely=0.13, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(frame1, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        #dialogo del archivo
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos csv", "*.csv"), ("Todos los archivos", "*.*")))

            label_file["text"] = filename
            if label_file["text"] == "":
                tk.messagebox.showwarning(title=None,message="No ha seleccionado ningun archivo")
            return None
        #cargar el archivo csv
        def Load_csv_data():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding = 'utf-8') as file:
                df = pd.read_csv(file, sep=',', header= [0], encoding='utf-8')
            clear_data()
            if 'adr' in df.columns:
                tv1["column"] = "tweets", "dosis", "medicamento", "UMLS", "adr"
                tv1["show"] = "headings"
                for column in tv1["columns"]:
                    tv1.heading(column, text=column)
                    tv1.column("tweets", minwidth=0, width=1000, stretch=True)
                    tv1.column("dosis", minwidth=0, width=180, stretch=True)
                    tv1.column("medicamento", minwidth=0, width=250, stretch=True)
                    tv1.column("UMLS", minwidth=0, width=270, stretch=True)
                    tv1.column("adr", minwidth=0, width=100, stretch=True)
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    tv1.insert("", "end", values=row)
            else:
                tv1["column"] = "tweets", "dosis", "medicamento", "UMLS"
                tv1["show"] = "headings"
                for column in tv1["columns"]:
                    tv1.heading(column, text=column)
                    tv1.column("tweets", minwidth=0, width=1000, stretch=True)
                    tv1.column("dosis", minwidth=0, width=200, stretch=True)
                    tv1.column("medicamento", minwidth=0, width=300, stretch=True)
                    tv1.column("UMLS", minwidth=0, width=300, stretch=True)
                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    tv1.insert("", "end", values=row)

            return None

        #archivos de clasificacion
        def clasificacion():
            filename_clas = label_file["text"]
            try:
                adr_file = adr_inclusion.make_adr(filename_clas)
            except:
                messagebox.showerror('Error en la clasificacion', 'Error en la clasificacion')
            try:
                adr_inclusion.read_adr(adr_file)
                messagebox.showinfo('Info', "A continuacion, se procede a la etapa de clasificacion.\n ES la etapa mas lenta. Tenga paciencia")
                adr_inclusion.test_train_adr(adr_file)
            except:
                messagebox.showerror('Error en la categorizacion', 'Se ha producido un error en la clasificacion de los archivos')
            return None

        #metricas del usuario
        def metricas_user():
            #devuelve las metricas del usuario

            try:
                metrics_final = adr_inclusion.get_metrics()
                print('get_metrics por aqui')
                precision = metrics_final['precision']
                print(precision)
                recall = metrics_final['recall']
                print(recall)
                f1 = metrics_final['f1']
                print(f1)
                roc = metrics_final['roc_auc']
                print(roc)
                nuevoVentana(precision, recall, f1, roc)
            except:
                messagebox.showinfo('Info', "Todavia no se ha evaluado el texto para obtener las métricas")
            return None

        #abrir nueva ventana con las metricas
        def nuevoVentana(precision, recall, f1, roc):
            newWindow = Toplevel()
            newWindow.title("Metricas de la clasificacion")
            newWindow.geometry("300x300")
            label_precision = tk.Label(newWindow, text= "Evaluacion de metricas:\n", font=('Times', '14'))
            label_precision.pack()
            label_precision = tk.Label(newWindow, text= "El valor de la precision es: " + str(precision), font=('Times', '12'), foreground = "blue")
            label_precision.pack()
            label_recall = tk.Label(newWindow, text= "El valor de recall es: " + str(recall), font=('Times', '12'), foreground = "blue")
            label_recall.pack()
            label_f1 = tk.Label(newWindow, text="El valor de f1 es: " + str(f1), font=('Times', '12'), foreground = "blue")
            label_f1.pack()
            label_roc = tk.Label(newWindow, text="El valor de roc es: " + str(roc), font=('Times', '12'), foreground = "blue")
            label_roc.pack()
            return None

        #cambiar
        def cambiarAnotacion():
            if seleccion.get() == 1:
                config.chk_adr = 1
            if seleccion.get() == 0:
                config.chk_adr = 0

        def clear_data():
            tv1.delete(*tv1.get_children())
            return None



    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## menu de herramientas
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar




# ---------------------------------------- Herramientas PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class Herramientas(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Herramientas", font=('Times', '20'))

        label.pack(pady=0, padx=0)

        super().__init__(container)
        #archivo de dialogo
        file_frame = tk.LabelFrame(self, text="Dividir archivo")
        file_frame.place(height=90, width=1300)
        #botones
        boton1 = tk.Button(file_frame, text="Paso1-Explorar archivo", command=lambda: File_dialog())
        boton1.place(rely=0.35, relx=0.15)

        boton4 = tk.Button(file_frame, text="Paso2-Dividir archivo", command=lambda: dividir_archivo())
        boton4.place(rely=0.35, relx=0.40)

        #ruta del archivo
        label_file = ttk.Label(file_frame, text="Ningun archivo seleccionado")
        label_file.place(rely=0, relx=0)

        #Generacion de diccionarios
        dic_frame = tk.LabelFrame(self, text="Webscraping para diccionario de medicamentos y principios activos")
        dic_frame.place(height=150, width=1300, rely=0.17, relx=0)

        #botones
        botonA = tk.Button(dic_frame, text="Diccionario de principios activos", command=lambda: vademecum_pa())
        botonA.place(rely=0.35, relx=0.15)

        #label
        labelA = tk.Label(dic_frame, text="Se genera un archivo por cada letra del abecedario", foreground = "red")
        labelA.place(rely=0.60, relx=0.15)

        botonB = tk.Button(dic_frame, text="Diccionario de medicamento", command=lambda: vademecum_med())
        botonB.place(rely=0.35, relx=0.40)

        #label
        labelB = tk.Label(dic_frame, text="Es un proceso lento, se genera un archivo por cada letra del abecedario", foreground = "red")
        labelB.place(rely=0.60, relx=0.40)

        botonC = tk.Button(dic_frame, text="Concatenar pa", command=lambda: concat_pa())
        botonC.place(rely=0.30, relx=0.70)

        botonC = tk.Button(dic_frame, text="Concatenar meds", command=lambda: concat_med())
        botonC.place(rely=0.65, relx=0.70)

        #Generacion de minado de twitter
        tweet_frame = tk.LabelFrame(self, text="Minado de twitter")
        tweet_frame.place(height=70, width=1300, rely=0.40, relx=0)

        botonT = tk.Button(tweet_frame, text="Cargar codigo de scrapping de twitter", command=lambda: Load_csv_data())
        botonT.place(rely=0.05, relx=0.15)

        tweet_tree = tk.LabelFrame(self, text="Visualizacion de codigo")
        tweet_tree.place(height=250, width=1300, rely=0.50, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(tweet_tree)
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 7), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(tweet_tree, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(tweet_tree, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")


        def Load_csv_data():
            try:
                    label_file['text'] = "./utils/scraping_twitter.txt"
                    print(label_file['text'])
                    with open(label_file["text"], encoding = 'utf-8') as file:
                        print(label_file['text'])
                        df = pd.read_csv(file, delimiter="\t")
                        print(df)
                    clear_data()
                    tv1["column"] = "codigo"
                    tv1["show"] = "headings"
                    for column in tv1["columns"]:
                        tv1.heading(column, text=column)
                        tv1.column("codigo", minwidth=0, width=1300, stretch=True)
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        tv1.insert("", "end",
                                   values=row)
            except:
                tk.messagebox.showwarning(title="Error en archivo", message="No se ha localizado codigo fuente para scrapping de twitter")
            return None

        def clear_data():
            tv1.delete(*tv1.get_children())
            return None


        def vademecum_pa():
            try:
                req_vademecum_pa.vademecum_pa()
            except:
                tk.messagebox.showwarning(title="Error en webscraping de principio activo",message="Compruebe su conexion a internet")
            return None

        def vademecum_med():
            try:
                req.vademecum_med()
            except:
                tk.messagebox.showwarning(title="Error en webscraping de medicamento", message="Compruebe su conexion a internet")
            return None


        def concat_pa():
            try:
                concat.concat_pa()
                messagebox.showinfo('Info', "Finalizada la union de todos los archivos.\nEl archivo final se encuentra en ./utils/pa-total.csv")
            except:
                tk.messagebox.showwarning(title="No hay archivo", message="No se han econtrado archivos que cumplen los criterios")
            return None

        def concat_med():
            try:
                concat.concat_med()
                messagebox.showinfo('Info', "Finalizada la union de todos los archivos.\nEl archivo final se encuentra en ./utils/med-total.csv")
            except:
                tk.messagebox.showwarning(title="No hay archivo", message="No se han econtrado archivos que cumplen los criterios")
            return None

        #dialogo del archivo
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos txt", "*.txt"), ("Todos los archivos", "*.*")))
            label_file["text"] = filename
            return None

        #dividir archivo en varios diferentes
        def dividir_archivo():
            # dividir archivo
            lines_per_file = 5000
            smallfile = None
            path = ""
            contador = 1
            with open(label_file["text"], encoding = 'utf-8') as bigfile:
                for lineno, line in enumerate(bigfile):
                    contador +=1
                    num_file = (math.floor(lineno / lines_per_file)) + 1
                    if lineno % lines_per_file == 0:
                        if smallfile:
                            smallfile.close()
                        if(num_file>9):
                            small_filename = './data/sa_{}.txt'.format(math.floor(lineno/lines_per_file)+1)
                        else:
                            small_filename = './data/sa_0{}.txt'.format(math.floor(lineno / lines_per_file) + 1)
                        smallfile = open(small_filename, "w")
                    smallfile.write(line)
                if smallfile:
                    smallfile.close()
            contador = math.floor((contador/lines_per_file) + 1)
            messagebox.showinfo('Info',"Finalizada la division de archivos.\nSe han generado " + str(contador) + " archivos en el directorio:\n" + os.path.abspath(small_filename))
            return None

        boton3 = tk.Button(self, text="Volver al inicio >>", command=lambda: parent.show_frame(parent.HomePage))
        boton3.place(rely=0.95, relx=0.80)

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        #menu de herramientas
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar

# ---------------------------------------- Resultados finales PAGE FRAME / CONTAINER ------------------------------------------------------------------------

class res_Final(tk.Frame):

    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Resultados finales", font=('Times', '20'))


        label.pack(pady=0, padx=0)

        super().__init__(container)
        # abrir archivo
        file_frame = tk.LabelFrame(self, text="Abrir archivo")
        file_frame.place(height=90, width=1300)
        # botones
        boton1 = tk.Button(file_frame, text="Paso1-Explorar archivo", command=lambda: File_dialog())
        boton1.place(rely=0.35, relx=0.15)

        boton2 = tk.Button(file_frame, text="Paso2-Cargar archivo", command=lambda: Load_csv_data())
        boton2.place(rely=0.35, relx=0.40)

        # ruta del archivo
        label_file = ttk.Label(file_frame, text="Ningun archivo seleccionado")
        label_file.place(rely=0, relx=0)

        #INICIO TREE
        frame1 = tk.LabelFrame(self, text="Resultados finales")
        frame1.place(height=450, width=1300, rely=0.13, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(frame1, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        #dialogo del archivo
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos csv", "*.csv"), ("Todos los archivos", "*.*")))

            label_file["text"] = filename
            if label_file["text"] == "":
                tk.messagebox.showwarning(title=None,message="No ha seleccionado ningun archivo")
            return None
        #cargar el archivo csv
        #cargar el archivo csv
        def Load_csv_data():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding = 'utf-8') as file:
                df = pd.read_csv(file, sep=',', header= [0], encoding='utf-8')
            clear_data()
            tv1["column"] = "tweets", "real_RAM", "predicha_RAM", "probabilidad"
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column)
                tv1.column("tweets", minwidth=0, width=1000, stretch=True)
                tv1.column("real_RAM", minwidth=0, width=100, stretch=True)
                tv1.column("predicha_RAM", minwidth=0, width=300, stretch=True)
                tv1.column("probabilidad", minwidth=0, width=300, stretch=True)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end", values=row)
            return None

        def clear_data():
            tv1.delete(*tv1.get_children())
            return None



    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## menu de herramientas
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar


# ---------------------------------------- UN SOLO PASO PAGE FRAME / CONTAINER ------------------------------------------------------------------------
class UnPaso(tk.Frame):

    def __init__(self, parent, container):
        super().__init__(container)

        label = tk.Label(self, text="Un solo paso", font=('Times', '20'))
        label.pack(pady=0, padx=0)
        super().__init__(container)
        # dialogo de abrir archivo
        file_frame = tk.LabelFrame(self, text="Abrir archivo")
        file_frame.place(height=90, width=1300)
        # Botones
        boton1 = tk.Button(file_frame, text="Paso1-Especifique directorio quickumls", command=lambda: File_dialog_quick())
        boton1.place(rely=0.35, relx=0.0)

        boton2 = tk.Button(file_frame, text="Paso2-Explorar archivo", command=lambda: File_dialog())
        boton2.place(rely=0.35, relx=0.30)

        boton3 = tk.Button(file_frame, text="Paso3-Cargar archivo", command=lambda: Load_csv_data())
        boton3.place(rely=0.35, relx=0.55)

        seleccion=tk.IntVar()
        c = tk.Checkbutton(file_frame, text="Aplicar stemming", command = lambda: cambiarestado(), variable= seleccion)
        c.place(rely =0.35, relx = 0.70)

        boton4 = tk.Button(file_frame, text="Paso4-Iniciar Procesos", command=lambda: oneStep())
        boton4.place(rely=0.35, relx=0.80)

        #ruta del archivo
        label_file = ttk.Label(file_frame, text="")
        label_file.place(rely=0, relx=0.30)

        #ruta del directorio de quick
        label_quick = ttk.Label(file_frame, text="Seleccione el directorio donde se encuentra quickumls")
        label_quick.place(rely=0, relx=0.0)

        #INICIO TREE
        frame1 = tk.LabelFrame(self, text="Un Paso Solo")
        frame1.place(height=450, width=1300, rely=0.13, relx=0)

        ## Treeview
        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14), rowheight=int(14 * 3))
        style.configure("Treeview", font=(None, 7), rowheight=int(10 * 5))

        treescrolly = tk.Scrollbar(frame1, orient="vertical",
                                   command=tv1.yview)
        treescrollx = tk.Scrollbar(frame1, orient="horizontal",
                                   command=tv1.xview)
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)
        treescrollx.pack(side="bottom", fill="x")
        treescrolly.pack(side="right", fill="y")

        #funciones de apertura del directorio de quick
        def File_dialog_quick():
            """Dialogo del archivo"""
            dirname = fd.askdirectory(initialdir="", title="Seleccione el directorio")

            label_quick["text"] = dirname
            config.quick_name = dirname
            return config.quick_name

        #funciones de apertura del directorio de quick
        def File_dialog():
            """Dialogo del archivo"""
            filename = fd.askopenfilename(initialdir="./data",
                                                  title="Seleccione un archivo",
                                                  filetype=(("archivos csv", "*.csv"), ("Todos los archivos", "*.*")))

            label_file["text"] = filename
            if label_file["text"] == "":
                tk.messagebox.showwarning(title=None,message="No ha seleccionado ningun archivo para el proceso")
            #config.file_ner = filename
            #print("EL ARCHIVO DE NER ES: " + config.file_ner)
            return config.file_ner

        #funcion para cargar archivo
        #cargar el archivo
        def Load_csv_data():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding = 'utf-8') as file:
                df = pd.read_csv(file, sep=',', header= [0], encoding='utf-8')
            clear_data()
            tv1["column"] = "idtweets", "tweets"
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column)
                tv1.column("idtweets", minwidth=0, width=50, stretch=False)
                tv1.column("tweets", minwidth=0, width=1250, stretch=False)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end", values=row)
            return None
            # funcion para limpiar los datos

        def check_size(file):
            size = False
            with open(file, encoding = 'utf-8') as f:
                texto_prueba = f.read()
                if (len(texto_prueba) > 900000):
                    size = True
                else:
                    size = False
            return size


        def oneStep():
            try:
                limpieza()
                tk.messagebox.showwarning(title=None, message="Fin de la limpieza del texto.\n Se inicia NER")
            except:
                messagebox.showerror('Error en la limpieza', 'Se ha producido un error en la limpieza')
            #print(config.file_ner)
            try:
                if (check_size(config.file_ner)):
                    #print("ARCHIVO GRANDE")
                    dividir_archivo(config.file_ner)
                    for infile in glob.glob(".\data\sa" + "*.txt"):
                        #print(str(infile))
                        config.file_ner = infile
                        lanzar_NER()
                else:
                    lanzar_NER()
            except:
                messagebox.showerror('Error en NER', 'Se ha producido un error en NER')
            concat_NER()
            clasificacion()

            return None

        #archivos de clasificacion
        def clasificacion():
            filename_clas = "./data/ext_full.csv"
            try:
                adr_file = adr_inclusion.make_adr(filename_clas)
            except:
                messagebox.showerror('Error en la clasificacion', 'Error en la clasificacion')
            try:
                adr_inclusion.read_adr(adr_file)
                messagebox.showinfo('Info', "A continuacion, se procede a la etapa de clasificacion.\n ES la etapa mas lenta. Tenga paciencia")
                adr_inclusion.test_train_adr(adr_file)
            except:
                messagebox.showerror('Error en la categorizacion', 'Se ha producido un error en la clasificacion de los archivos')
            return None

        #dividir archivo en varios diferentes
        def dividir_archivo(file):
            # dividir archivo
            lines_per_file = 5000
            smallfile = None
            path = ""
            contador = 1
            with open(file, encoding = 'utf-8') as bigfile:
                for lineno, line in enumerate(bigfile):
                    contador +=1
                    num_file = (math.floor(lineno / lines_per_file)) + 1
                    if lineno % lines_per_file == 0:
                        if smallfile:
                            smallfile.close()
                        if(num_file>9):
                            small_filename = './data/sa_{}.txt'.format(math.floor(lineno/lines_per_file)+1)
                        else:
                            small_filename = './data/sa_0{}.txt'.format(math.floor(lineno / lines_per_file) + 1)
                        smallfile = open(small_filename, "w")
                    smallfile.write(line)
                if smallfile:
                    smallfile.close()
            contador = math.floor((contador/lines_per_file) + 1)
            messagebox.showinfo('Info',"Finalizada la division de archivos.\nSe han generado " + str(contador) + " archivos en el directorio:\n" + os.path.abspath(small_filename))
            return None

        def limpieza():
            """Si el archivo es correcto se carga en el treeview"""
            with open(label_file["text"], encoding='utf-8') as file:
                filename2 = preproc_tweets.limpieza_tweet(label_file["text"])
                df = pd.read_csv(filename2, sep=',', header=[0], encoding='utf-8')
            clear_data()
            tv1["column"] = "idtweets", "tweets"
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                tv1.heading(column, text=column)
                tv1.column("idtweets", minwidth=0, width=70, stretch=False)
                tv1.column("tweets", minwidth=0, width=1230, stretch=False)
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end",
                           values=row)
            #label_1 = ttk.Label(file_frame, text="Archivo final: " + str(filename2), foreground="blue")
            #label_1.place(rely=0, relx=0.55)
            config.file_ner = "./data/txt_limpieza.txt"
            return None


        #funcion para realizar el trabajo de NER
        def lanzar_NER():
            tk.messagebox.showwarning(title=None, message="Se inicia NER")
            drug_ner.lanzar()
            return None

        def callback():
            import os
            webbrowser.open("file://" + os.path.realpath("./data/NER_displacy.html"))

        boton3 = tk.Button(self, text="Ver metricas finales >>", command=lambda: metricas_user())
        boton3.place(rely=0.95, relx=0.20)

        #metricas del usuario
        def metricas_user():
            #devuelve las metricas del usuario
            try:
                metrics_final = adr_inclusion.get_metrics()
                print('get_metrics por aqui')
                precision = metrics_final['precision']
                print(precision)
                recall = metrics_final['recall']
                print(recall)
                f1 = metrics_final['f1']
                print(f1)
                roc = metrics_final['roc_auc']
                print(roc)
                nuevoVentana(precision, recall, f1, roc)
            except:
                messagebox.showinfo('Info', "Todavia no se ha evaluado el texto para obtener las métricas")
            return None

        #abrir nueva ventana con las metricas
        def nuevoVentana(precision, recall, f1, roc):
            newWindow = Toplevel()
            newWindow.title("Metricas de la clasificacion")
            newWindow.geometry("300x300")
            label_precision = tk.Label(newWindow, text= "Evaluacion de metricas:\n", font=('Times', '14'))
            label_precision.pack()
            label_precision = tk.Label(newWindow, text= "El valor de la precision es: " + str(precision), font=('Times', '12'), foreground = "blue")
            label_precision.pack()
            label_recall = tk.Label(newWindow, text= "El valor de recall es: " + str(recall), font=('Times', '12'), foreground = "blue")
            label_recall.pack()
            label_f1 = tk.Label(newWindow, text="El valor de f1 es: " + str(f1), font=('Times', '12'), foreground = "blue")
            label_f1.pack()
            label_roc = tk.Label(newWindow, text="El valor de roc es: " + str(roc), font=('Times', '12'), foreground = "blue")
            label_roc.pack()
            return None

        #concatener todas las NER
        def concat_NER():
            appended_data = []
            for infile in glob.glob("./data/sa" + "*ent.csv"):
                data = pd.read_csv(infile)
                appended_data.append(data)
            appended_data = pd.concat(appended_data)
            # paso del dataframe a csv
            try:
                appended_data.to_csv('./data/ext_full.csv', sep=",", index=False, header=True, encoding='utf-8')
                tk.messagebox.showwarning(title="Fin de la concatenacion", message="Se hane concatenado los archivos.\n\nEl archivo final se encuentra en ./data/ext_full.csv")
            except:
                messagebox.showerror('Error en la concatenacion', 'Error en la concatenacion')
        #aplicar stemming o no
        def cambiarestado():
            if seleccion.get() == 1:
                config.chk_value = 1
            if seleccion.get() == 0:
                config.chk_value = 0

        #limpiar datos
        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

    def create_menubar(self, parent):
        menubar = Menu(parent, bd=3, relief=RAISED, activebackground="#80B9DC")

        ## Filemenu
        filemenu = Menu(menubar, tearoff=0, relief=RAISED, activebackground="#026AA9")
        menubar.add_cascade(label="Etapa", menu=filemenu)
        filemenu.add_command(label="Visualizacion de tweets", command=lambda: parent.show_frame(parent.Visualizacion))
        filemenu.add_command(label="Limpieza de tweets", command=lambda: parent.show_frame(parent.Limpieza))
        filemenu.add_command(label="Reconocimiento de entidades", command=lambda: parent.show_frame(parent.NER))
        filemenu.add_command(label="Clasificacion de textos", command=lambda: parent.show_frame(parent.Clasificacion))
        filemenu.add_command(label="Resultados finales", command=lambda: parent.show_frame(parent.res_Final))
        filemenu.add_command(label="Un solo paso", command=lambda: parent.show_frame(parent.UnPaso))
        filemenu.add_command(label="Ir a Inicio", command=lambda: parent.show_frame(parent.HomePage))
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=parent.quit)

        ## menu de herramientas
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Herramientas para NER",  command=lambda: parent.show_frame(parent.Herramientas))
        tools_menu.add_separator()

        ## menu de ayuda
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Info", command=about)
        help_menu.add_separator()

        return menubar

if __name__ == "__main__":
    app = App()
    app.mainloop()


