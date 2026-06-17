# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 17:31:09 2024

Código para generar imagenes de COVs
"""
# Importamos librerias
import pandas as pd
import matplotlib.pyplot as plt

# Plot_COV(): Función para plotear COVs entre fechas.
def Plot_COV(cov_df, pi, pf, ymax, tipo, freq, path):
    # Definimos variables:
    # cov_df = DF de COVs
    # pi = fecha inicial de periodo
    # pf = fecha final de periodo
    # ymax = 50 ó 200 
    # tipo = '1plot' ó '25plot'
    # freq = 'Minutaria' ó 'Horaria' 
    # path = Path de guardado
    
    # Definmos momentos inicial y final
    date_1 = pd.to_datetime(pi)
    date_2 = pd.to_datetime(pf)
    # Ploteamos
    # 1 Plot
    if tipo == '1plot':
        ax = cov_df.loc[date_1:date_2,:].plot(grid=True, figsize=(14,7)\
                                              ,ylim=(-0.1,ymax),ylabel='ppb')
    # Subplots
    elif tipo == '25plot':
        ax = cov_df.loc[date_1:date_2,:].plot(subplots=True, layout=(25,1)\
                                , grid=True, figsize=(10,20),ylim=(-0.1,ymax))
    else:
        print('Tipo debe ser 1plot o 25plot (así se llaman las carpetas).')
    
    plt.suptitle('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
              +date_2.strftime('%Y-%m-%d, %H:%M.'))
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(path+freq+'/'+tipo+'/'+'ymax'+str(ymax)+'ppb/'\
                +date_1.strftime('%Y-%m-%d %H')+'.png',dpi=300)

# Plot_MET(): Función para pltoear variables meteo entre fechas.
def Plot_MET(cov_df, pi, pf, path):
    # Definimos variables:
    # cov_df = DF de COVs
    # pi = fecha inicial de periodo
    # pf = fecha final de periodo
    # path = Path de guardado
    
    # Definmos momentos inicial y final
    date_1 = pd.to_datetime(pi)
    date_2 = pd.to_datetime(pf)
    
    met = ['p', 't', 'rh', 'ws', 'wd', 'sr']
    units = ['mbar','°C','%','m/s','°','W/m2']
    
    # Ploteamos
    axs = cov_df.loc[date_1:date_2,met].plot(subplots=True, layout=(6,1)\
                            , grid=True, figsize=(10,20))
    ai = 0
    for ax in axs[0]:
        ax.set_ylabel(units[ai])
        ai = ai+1
    plt.suptitle('Peak '+date_1.strftime('%Y-%m-%d, %H:%M')+' a '\
              +date_2.strftime('%Y-%m-%d, %H:%M.'))
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(path+'/'+date_1.strftime('%Y-%m-%d %H')+'.png',dpi=300)