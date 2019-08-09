#*********************
# Interfaz para hacer la limpieza de datos
# usando el acomodo de clases y objetos
#*********************

import tkinter as tk

import os
from datetime import datetime
import graficas_dinamicas as gr
from itertools import compress
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import time
import pdb
 
class Ventana(tk.Tk):
    def __init__(self, master):
        tk.Tk.__init__(self, master)
        self.master = master
        self.title('Gráficas dinámicas')
        self.iconbitmap('favicon.ico')
        self.geometry('500x400+600+200')
        self.resizable(0,0)
        menu = tk.Menu(self)
        self.config(menu=menu)

        subMenu = tk.Menu(menu,tearoff=False)
        menu.add_cascade(label = 'Archivo', menu = subMenu)
        subMenu.add_command(label = 'Cerrar', command=self.cerrar)
        
        self.mainWidgets()
        
       
    def mainWidgets(self):
        self.cuerpo = Cuerpo(self)
        self.cuerpo.grid(row=0, column=0)

     
    def cerrar(self):
        self.destroy()


class Cuerpo(tk.Frame):
    
    carpeta_in = 'D:/01 Findero'
    meses_lista = {1:'01 Enero',2:'02 Febrero',3:'03 Marzo',
                   4:'04 Abril',5:'05 Mayo',6:'06 Junio',
                   7:'07 Julio',8:'08 Agosto',9:'09 Septiembre',
                   10:'10 Octubre',11:'11 Noviembre',12:'12 Diciembre'}
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.widgets()        

    def widgets(self):

        self.label_encabezado = tk.Label(self,  text = '      Gráficas dinámicas',
                                         font='Helvetica 18 bold' )
        self.label_encabezado.grid(row=1, column=1, columnspan = 2)
        
        
        
        
        self.label_mes = tk.Label(self, text ='Mes:')
        self.label_mes.grid(row=3, column=1, padx=20, pady=20, sticky=tk.E)

        self.tk_mes = tk.StringVar()
        self.meses = [m for m in os.listdir(self.carpeta_in) if m in self.meses_lista.values()]
        self.tk_mes.set(self.meses[-1])
        
        self.mes_desplegable = tk.OptionMenu(self, self.tk_mes, *self.meses)
        self.mes_desplegable.config(width=20)
        self.mes_desplegable.grid(row=3,column=2)
        
        
        self.label_cliente = tk.Label(self, text = 'Cliente:')
        self.label_cliente.grid(row=4, column=1, padx=20, pady=20, sticky=tk.E)
        
        self.tk_cliente = tk.StringVar()        
        self.clientes = os.listdir(self.carpeta_in+'/'+ self.tk_mes.get())
        self.tk_cliente.set(self.clientes[-1])
        self.tk_mes.trace('w',self.update_cliente)
        
        self.cliente_desplegable = tk.OptionMenu(self, self.tk_cliente, *self.clientes)
        self.cliente_desplegable.config(width=20)
        self.cliente_desplegable.grid(row=4,column=2)
        
        
        
        self.label_findero = tk.Label(self, text = 'Findero:')
        self.label_findero.grid(row=5, column=1, padx=20, pady=20, sticky=tk.E)
        self.tk_findero = tk.StringVar()        
        self.finderos = [item[8:-4] for item in os.listdir(self.carpeta_in+'/'+ self.tk_mes.get()+'/'+self.tk_cliente.get()+'/Datos')
                                                                    if '.CSV' in item[-4:] or '.csv' in item[-4:]]
        
        self.tk_findero.set(self.finderos[0])
        self.tk_cliente.trace('w',self.update_findero)
        
        self.findero_desplegable = tk.OptionMenu(self, self.tk_findero, *self.finderos)
        self.findero_desplegable.config(width=20)
        self.findero_desplegable.grid(row=5,column=2)
        

        self.boton_enviar = tk.Button(self, text = 'Siguiente', command=self.enviar)
        self.boton_enviar.grid(row=7, column=1, columnspan = 2, ipadx=15)
        
        
        self.grid_rowconfigure(0, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(6, minsize=20)
        
        self.grid_columnconfigure(0, minsize=60)
        
        
        
            
    def enviar(self):
        
        self.frecuencia = 5
        
        self.leer_datos()

        
        top = tk.Toplevel()
        top.iconbitmap('favicon.ico')
        top.geometry(f'+{1050}+{200}')
        
        
        label = tk.Label(top, text=self.tk_findero.get(),font='Helvetica 12 bold') 
        label.grid(row=1,column=1, columnspan=3, sticky=tk.W)
        

        self.puertos = ['Puerto '+ str(i) for i in range(1,13)]
        self.selecciones = dict()  
        
        for idx, puerto in enumerate(self.puertos):
            self.selecciones[puerto] = tk.Checkbutton(top, text=puerto, onvalue=True, offvalue=False)
            self.selecciones[puerto].var = tk.BooleanVar()
            self.selecciones[puerto]['variable'] = self.selecciones[puerto].var
            
            salto = 0
            if idx >= 4 and idx <= 7:
                salto = 2
            elif idx >= 8:
                salto = 4
            
            self.selecciones[puerto].grid(row=2+salto, column=(idx)%4+1)
        
        self.seleccionados = [self.selecciones[puerto].var.get() for puerto in self.puertos]
        self.seleccion_grafica = []
        for idx,_ in enumerate((list(self.selecciones.values()))):
            self.selecciones[self.puertos[idx]].var.trace('w',self.update_checkbox)
        
        
        
        boton_graficar = tk.Button(top,text = 'Graficar', command= self.graficador)
        boton_graficar.grid(row=8, column=1)
        
        top.grid_rowconfigure(0, minsize=10)
        top.grid_rowconfigure(3, minsize=10)
        top.grid_rowconfigure(5, minsize=10)
        top.grid_rowconfigure(7, minsize=10)
        
        top.grid_columnconfigure(0, minsize=20)
        
        top.mainloop()
    
        
    
    def update_cliente(self, *args):
        client = os.listdir(self.carpeta_in+'/'+ self.tk_mes.get())
        try:
            self.tk_cliente.set(client[-1])
        except:
            self.tk_cliente.set('')      
        
        
        menu = self.cliente_desplegable['menu']
        menu.delete(0,'end')
    
        for name in client:
            menu.add_command(label=name, command=lambda nuevo=name: self.tk_cliente.set(nuevo))



    def update_findero(self, *args):
        finderos = [item[8:-4] for item in os.listdir(self.carpeta_in+'/'+ self.tk_mes.get()+'/'+self.tk_cliente.get()+'/Datos')
                                                                    if '.CSV' in item[-4:] or '.csv' in item[-4:]]
        try:
            self.tk_findero.set(finderos[0])
        except:
            self.tk_findero.set('')      
        
        
        menu = self.findero_desplegable['menu']
        menu.delete(0,'end')
    
        for name in finderos:
            menu.add_command(label=name, command=lambda nuevo=name: self.tk_findero.set(nuevo))
    
    
    def update_checkbox(self, *args):
        self.seleccionados = [self.selecciones[puerto].var.get() for puerto in self.puertos]
        self.seleccion_grafica = list(compress([i for i in range(1,13)], self.seleccionados))
        pass


    def leer_datos(self):
             
        carpeta = f'D:/01 Findero/{self.tk_mes.get()}/{self.tk_cliente.get()}/Datos'
        filename = f'{carpeta}/DATALOG_{self.tk_findero.get()}.CSV'   
        
        with open(filename) as f:
            for i, l in enumerate(f):
                pass
        largo = i + 1

        saltar = np.setdiff1d(np.arange(largo), np.arange(0,largo,self.frecuencia))
        
        self.df = pd.read_csv(filename, skiprows=saltar)
    
        try:
            self.df['Datetime'] = pd.to_datetime(self.df['Date']+' '+self.df['Time'], format='%d/%m/%Y  %H:%M:%S')
        except ValueError:
        
            try:
                self.df['Datetime'] = pd.to_datetime(self.df['Date']+' '+self.df['Time'], format='%d-%m-%Y  %H:%M:%S')
            except ValueError:
                self.df['Datetime'] = pd.to_datetime(self.df['Date']+' '+self.df['Time'], format='%d-%m-%y  %H:%M:%S')  
    
    
    def graficador(self):

        gr.graficas_dinamicas(self.tk_cliente.get(), self.tk_mes.get(), 
                            f'DATALOG_{self.tk_findero.get()}.CSV', self.seleccion_grafica, self.frecuencia, self.df)

        
        for puerto in self.puertos:
            self.selecciones[puerto].var.set(False)      

   
        
            
        
consumo_ = Ventana(None)

consumo_.mainloop()