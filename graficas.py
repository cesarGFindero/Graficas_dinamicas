import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import pdb

def graficas(cliente,mes):
    
    formato_fecha = '%d-%m-%Y'
    carpeta = 'D:/01 Findero/'+mes+'/'+cliente+'/Datos'
    
    finderos = os.listdir(carpeta)
    finderos = [item for item in finderos if '.CSV' in item[-4:] or '.csv' in item[-4:]]
    
    
    for findero in finderos:  
        
        direccion_input = carpeta + '/' + findero
        
        data = pd.read_csv(direccion_input)
    
        
        for i in range (1,13):
            
            columna = 'L'+str(i) 
                
            y_data = data[columna].values
            fecha = data['Date']
            hora = data['Time']
            data['Tiempo'] = fecha + hora
            
            x_data = pd.to_datetime(data['Tiempo'], format=formato_fecha+' %H:%M:%S') #tiempo en horas
    
            if max(y_data)<=140:
                limite_superior = 140   
            else:
                limite_superior = max(y_data)*1    

            if not os.path.exists(carpeta+'/'+'Graficas'):
              	os.mkdir(carpeta+'/'+'Graficas')
            
            if not os.path.exists(carpeta+'/'+'Graficas'+'/'+findero):
              	os.mkdir(carpeta+'/'+'Graficas'+'/'+findero)
            
            ax = plt.gca()
            fig= plt.figure()
            plt.plot(x_data,y_data,label='Findero',linewidth=1, color = 'k')
            plt.ylabel('Potencia [W]')
            plt.ylim(0,limite_superior)
            plt.title(columna)
            plt.gcf().autofmt_xdate()
            ax.xaxis_date()
            myFmt = mdates.DateFormatter('%H:%M')
            ax.xaxis.set_major_formatter(myFmt)
            plt.savefig(carpeta+'/'+'Graficas'+'/'+findero+'/'+columna+'.png',bbox_inches='tight')
            plt.close()

if __name__ == '__main__':
    cliente = '05 Antonio Cortina'
    mes='06 Junio'
    graficas(cliente, mes)
    