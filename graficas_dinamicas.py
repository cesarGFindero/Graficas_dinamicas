#**********************
# Se crean graficas dinamicas en este archivo
#************************

import pdb
import plotly as py
import plotly.graph_objs as go
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import os
import time

def leer_y_preparar(filename):
    df = pd.read_csv(filename)
    
    try:
        df['datetime'] = pd.to_datetime(df['Date']+df['Time'], format='%d/%m/%Y  %H:%M:%S')
    except ValueError:
    
        try:
            df['datetime'] = pd.to_datetime(df['Date']+df['Time'], format='%d-%m-%Y  %H:%M:%S')
        except ValueError:
            df['datetime'] = pd.to_datetime(df['Date']+df['Time'], format='%d-%m-%y  %H:%M:%S')     
    return df
    
def graficas_dinamicas(cliente,mes,findero,senales,frecuencia_graficacion,df):
    
    carpeta = 'D:/01 Findero/' + mes + '/' + cliente + '/Datos'    
    filename = carpeta + '/' + findero    
    
    for column in senales:
        
        columna = 'L'+str(column)
        puerto = 'Puerto ' + str(column)
        y_data = df[columna].values
        
        x_data = df['datetime']-pd.Timedelta('0 days 0:00:00')
        
        layout = go.Layout(
                title = puerto +'  '+ findero[8:-4],
                yaxis = dict(
                        title = 'Potencia'
                        ),
                xaxis = dict(
                        title = 'Índice'
                        )
                )
                
        trace1 = go.Scattergl(
                        x = x_data[::frecuencia_graficacion],
                        y = y_data[::frecuencia_graficacion],
                        mode = 'lines',
                        line = dict(
                                color  = 'rgb(0,0,0)',
                                shape = 'linear',
                                width = 2,   
                                )
                        )
        fig = go.Figure(data = [trace1] ,layout=layout)
        plot(fig)
        
        time.sleep(.3)

if __name__ == '__main__':
    cliente = '22 Pau Ruiz'
    mes ='05 Mayo'
    senales = [12]
    findero = 'DATALOG_F12.CSV'
    frecuencia_graficacion = 2
    graficas_dinamicas(cliente,mes,findero,senales,frecuencia_graficacion)