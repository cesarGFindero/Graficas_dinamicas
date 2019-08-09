#**********************
# Se crean graficas dinamicas en este archivo
#************************

import pdb
import plotly as py
import plotly.graph_objs as go
import pandas as pd
import os
import time  

    
def graficas_dinamicas(cliente,mes,findero,senales,frecuencia_graficacion,df):
    
    carpeta_out = f'D:/01 Findero/{mes}/{cliente}/Graficas'   
    
    if not os.path.exists(carpeta_out):
        os.mkdir(carpeta_out)
    
    for column in senales:
        
        columna = f'L{column}'
        puerto = f'Puerto {column}' 
        y_data = df[columna].values
        
        x_data = df['Datetime']-pd.Timedelta('0 days 0:00:00')
        
        layout = go.Layout(
                title = puerto +'  '+ findero[8:-4],
                yaxis = dict(
                        title = 'Potencia'
                        ),
                xaxis = dict(
                        title = 'Fecha y hora'
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
        py.offline.plot(fig, filename=f'{carpeta_out}/{puerto}.html')
        
        
        time.sleep(.3)

if __name__ == '__main__':
    cliente = '22 Pau Ruiz'
    mes ='05 Mayo'
    senales = [12]
    findero = 'DATALOG_F12.CSV'
    frecuencia_graficacion = 2
    graficas_dinamicas(cliente,mes,findero,senales,frecuencia_graficacion)