# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:56:18 2024

@author: felip
"""
# Librerías
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import patches
from mpltern.datasets import get_triangular_grid
import pandas as pd
import numpy as np
from datetime import datetime as dt
import sys


#########################################
# Función para plotear series de tiempo #
def COV_TimeSeries(COV, Fi_str, Ff_str,dire,file):

    # Guardamos nombre de Etilbenceno_Xileno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [15,19,14]
    names = [cols[i] for i in index]  
    names_mz = [r'$m/z_{93.070}$',r'$m/z_{107.086}$',r'$m/z_{79.054}$']

    # Define start and end dates
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)
    
    # Obtain COVs with the dates of interest
    COV_t = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]
    
    # Ploteamos
    fig = plt.figure(figsize=(12,4*len(names)))
    # ploteamos subplots
    ci=0
    colors = ['blue','orange','green']
    for c in names:
        plt.subplot(len(names),1,ci+1)
        plt.plot(COV_t[c],color=colors[ci])
        plt.grid()
        plt.title(c+', '+names_mz[ci])
        plt.ylabel('[ppbv]')
        plt.ylim(top=20)
        if ci+1 == len(names):
            plt.xlabel('Tiempo')
        ci += 1
        
    # asignamos titulo y guardamos
    plt.suptitle(str(Fi)+' a '+str(Ff))
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
    # plt.savefig('C:/Users/felip/Desktop/U/Tesis/Figs/Sinca/',dpi=300)
    plt.show
    plt.savefig(dire+'TS_'+file+'.png', dpi=300)

    
######################################################################   
# Función para plotear grafico ternario con cb de time of day
def COV_Ternary_tod( COV, Fi_str, Ff_str, freq, dire, file, cb):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [19,15,14]
    if freq == '1min':
        cb_delta = 60
    elif freq == '5min':
        cb_delta = 12
    
    names = [cols[i] for i in index]
    
    # Creamos timestamps
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)

    # Cortamos COV entre horas de interés
    COV_ep = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]

    # Creamos Figura
    fig = plt.figure(figsize=(8, 7))

    # Plot ternario
    ax = plt.subplot(projection='ternary')

    # Scatter ternario
    vmin = 0; vmax = 24; n = 24
    vals = np.linspace(vmin,vmax,n+1)
    cmap = plt.cm.hsv
    norm = colors.BoundaryNorm( vals, cmap.N)
    sc = ax.scatter(COV_ep[names[1]],COV_ep[names[0]]\
                    , COV_ep[names[2]],c=COV_ep.index.hour\
                    , cmap=cmap, norm=norm)
    # Colorbar
    if cb == True:
        cax = ax.inset_axes([1.15, 0.05, 0.05, 0.95], transform=ax.transAxes)
        colorbar = fig.colorbar(sc, cax=cax)
        colorbar.set_label("[Hora]", rotation=270, va="baseline")
        # set ticks
        day = pd.date_range('2000-01-01 00:00:00','2000-01-02 00:00:00',freq=freq)
        print(vals)
        print(day.strftime('%H:%M')[::cb_delta])
        colorbar.ax.set_yticklabels(day.strftime('%H:%M')[::cb_delta])

    # Agregamos letras en cada punta
    # T 
    Tc = (0.2081, 0.1663, 0.5292)
    ax.text(48,-8,52,r'$T_{93.070}$',fontsize=15, color=Tc)

    # E
    EXc = (0.1157, 0.7022, 0.6843)
    ax.text(43,57,-18,r'$EX_{107.086}$',fontsize=15, color=EXc)

    # B
    Bc = (0.6980, 0.1725, 0.1725 )
    ax.text(-12,57,43,r'$B_{79.054}$',fontsize=15, color=Bc)

    # Settings finales
    t, l, r = get_triangular_grid()
    ax.triplot(t,l,r,color='lightgray',zorder=0)
    lw= 1
    ls= '-'
    # T
    ax.grid(axis='t',which='both',color=Tc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='t',color=Tc,labelcolor=Tc)
    # EX
    ax.grid(axis='l',which='both',color=EXc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='l',color=EXc,labelcolor=EXc)
    # B
    ax.grid(axis='r',which='both',color=Bc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='r',color=Bc,labelcolor=Bc)
    
    ax.zorder = 0
    Fi_cov = COV_ep.index[0]; Ff_cov = COV_ep.index[-1]
    plt.suptitle(str(Fi_cov)+' a '+str(Ff_cov)+', datos cada '+freq, y=0.95)
    plt.tight_layout(pad=0.5,rect=(0,0,1,0.95))
    # plt.savefig(dire+'DT_'+file+'.png', dpi=300)
    
######################################################################   
# Función para plotear grafico ternario con cb de time of day
def COV_Ternary_tod_sb( COV, Fi_str, Ff_str, ax):
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [19,15,14]

    names = [cols[i] for i in index]
    
    # Creamos timestamps
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)

    # Cortamos COV entre horas de interés
    COV_ep = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]
    

    # Scatter ternario
    vmin = 0; vmax = 24; n = 24
    vals = np.linspace(vmin,vmax,n+1)
    cmap = plt.cm.hsv
    norm = colors.BoundaryNorm( vals, cmap.N)
    sc = ax.scatter(COV_ep[names[1]],COV_ep[names[0]]\
                    , COV_ep[names[2]],c=COV_ep.index.hour\
                    , cmap=cmap, norm=norm)

    # Agregamos letras en cada punta
    # T 
    Tc = (0.2081, 0.1663, 0.5292)
    ax.text(48,-8,52,r'$T_{93.070}$',fontsize=15, color=Tc)

    # E
    EXc = (0.1157, 0.7022, 0.6843)
    ax.text(43,57,-18,r'$EX_{107.086}$',fontsize=15, color=EXc)

    # B
    Bc = (0.6980, 0.1725, 0.1725 )
    ax.text(-12,57,43,r'$B_{79.054}$',fontsize=15, color=Bc)

    # Settings finales
    t, l, r = get_triangular_grid()
    ax.triplot(t,l,r,color='lightgray',zorder=0)
    lw= 1
    ls= '-'
    # T
    ax.grid(axis='t',which='both',color=Tc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='t',color=Tc,labelcolor=Tc)
    # EX
    ax.grid(axis='l',which='both',color=EXc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='l',color=EXc,labelcolor=EXc)
    # B
    ax.grid(axis='r',which='both',color=Bc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='r',color=Bc,labelcolor=Bc)
    
    ax.zorder = 0
    
    return sc
    
######################################################################   
# Función para plotear grafico ternario con cb de time of day
def COV_Ternary_tod_cb(ax,fig,sc):
    cax = ax.inset_axes([1.2, 0.05, 0.05, 0.85], transform=ax.transAxes)
    colorbar = fig.colorbar(sc,cax=cax)
    colorbar.set_label("Hora del día [HH:MM]", rotation=270, va="baseline")
    # set ticks
    day = pd.date_range('2000-01-01 00:00:00','2000-01-02 00:00:00',
                        freq='5min')
    colorbar.ax.set_yticklabels(day.strftime('%H:%M')[::12])


###################################################################
# Función para plotear grafico ternario y cb de Wind Direction
def COV_Ternary_wd( COV, Fi_str, Ff_str, dire, file):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [19,15,14] # cada 5 min
    names = [cols[i] for i in index]
    names.append('wd')
    
    # Creamos timestamps
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)

    # Cortamos COV entre horas de interés
    COV_ep = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]

    # Creamos Figura
    fig = plt.figure(figsize=(8, 7))

    # Plot ternario
    ax = plt.subplot(projection='ternary')

    # Scatter ternario
    vmin = 0; vmax = 360; n = 12
    vals = np.linspace(vmin,vmax,n+1)
    cmap = plt.cm.hsv
    norm = colors.BoundaryNorm( vals, cmap.N)
    sc = ax.scatter(COV_ep[names[1]],COV_ep[names[0]]\
                    , COV_ep[names[2]],c=COV_ep['wd']\
                    , cmap=cmap, norm=norm)
    # Colorbar
    cax = ax.inset_axes([1.15, 0.05, 0.05, 0.95], transform=ax.transAxes)
    colorbar = fig.colorbar(sc, cax=cax)
    colorbar.set_label("Dirección de viento [°]", rotation=270, va="baseline")
    
    # Agregamos letras en cada punta
    # T 
    Tc = (0.2081, 0.1663, 0.5292)
    ax.text(48,-8,52,r'$T_{93.070}$',fontsize=15, color=Tc)

    # E
    EXc = (0.1157, 0.7022, 0.6843)
    ax.text(43,57,-18,r'$EX_{107.086}$',fontsize=15, color=EXc)

    # B
    Bc = (0.6980, 0.1725, 0.1725 )
    ax.text(-12,57,43,r'$B_{79.054}$',fontsize=15, color=Bc)

    # Settings finales
    t, l, r = get_triangular_grid()
    ax.triplot(t,l,r,color='lightgray',zorder=0)
    lw= 1
    ls= '-'
    # T
    ax.grid(axis='t',which='both',color=Tc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='t',color=Tc,labelcolor=Tc)
    # E
    ax.grid(axis='l',which='both',color=EXc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='l',color=EXc,labelcolor=EXc)
    # B
    ax.grid(axis='r',which='both',color=Bc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='r',color=Bc,labelcolor=Bc)
    
    ax.zorder = 0
    Fi_cov = COV_ep.index[0]; Ff_cov = COV_ep.index[-1]
    plt.suptitle(str(Fi_cov)+' a '+str(Ff_cov)+', datos cada 5min',y=0.95)
    plt.tight_layout(pad=0.5,rect=(0,0,1,0.95))
    # plt.savefig(dire+'DT_'+file+'.png', dpi=300)
    
###################################################################
# Función para plotear grafico ternario y cb de Wind Direction
def COV_Ternary_wd_sb( COV, Fi_str, Ff_str,ax):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [19,15,14] # cada 5 min
    names = [cols[i] for i in index]
    names.append('wd')
    
    # Creamos timestamps
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)

    # Cortamos COV entre horas de interés
    COV_ep = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]


    # Scatter ternario
    vmin = 0; vmax = 360; n = 12
    vals = np.linspace(vmin,vmax,n+1)
    cmap = plt.cm.hsv
    norm = colors.BoundaryNorm( vals, cmap.N)
    sc = ax.scatter(COV_ep[names[1]],COV_ep[names[0]]\
                    , COV_ep[names[2]],c=COV_ep['wd']\
                    , cmap=cmap, norm=norm)
    
    # Agregamos letras en cada punta
    # T 
    Tc = (0.2081, 0.1663, 0.5292)
    ax.text(48,-8,52,r'$T_{93.070}$',fontsize=15, color=Tc)

    # E
    EXc = (0.1157, 0.7022, 0.6843)
    ax.text(43,57,-18,r'$EX_{107.086}$',fontsize=15, color=EXc)

    # B
    Bc = (0.6980, 0.1725, 0.1725 )
    ax.text(-12,57,43,r'$B_{79.054}$',fontsize=15, color=Bc)

    # Settings finales
    t, l, r = get_triangular_grid()
    ax.triplot(t,l,r,color='lightgray',zorder=0)
    lw= 1
    ls= '-'
    # T
    ax.grid(axis='t',which='both',color=Tc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='t',color=Tc,labelcolor=Tc)
    # E
    ax.grid(axis='l',which='both',color=EXc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='l',color=EXc,labelcolor=EXc)
    # B
    ax.grid(axis='r',which='both',color=Bc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='r',color=Bc,labelcolor=Bc)
    
    ax.zorder = 0
    return sc

###################################################################
# Función para plotear grafico ternario y cb de Wind Direction
def COV_Ternary_wd_cb( ax, fig, sc):
    
    # Colorbar
    cax = ax.inset_axes([1.2, 0.05, 0.05, 0.85], transform=ax.transAxes)
    colorbar = fig.colorbar(sc, cax=cax)
    colorbar.set_label("Dirección de viento [°]", rotation=270, va="baseline")
    
    
###################################################################    
# Función para plotear grafico ternario con cb de time of day
# de serie de tiempo larga
def COV_Ternary_LongPeriod_tod( COV, Fi_str, Ff_str, freq):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    if freq == '1m':
        index = [20,16,15] # cada 1 min
        # time = pd.date_range('00:00:00','23:59:00',freq='1m')
        time = pd.date_range('2022-01-01 00:00:00','2022-01-02 00:00:00'\
                             ,freq='1min').strftime('%H:%M').values[::60*6]
        
    elif freq == '5m':
        index = [19,15,14] # cada 5 min
        # time = pd.date_range('00:00:00','23:55:00',freq='5m')
        time = pd.date_range('2022-01-01 00:00:00','2022-01-02 00:00:00'\
                             ,freq='5min').strftime('%H:%M').values[::12*6]
    names = [cols[i] for i in index]
    
    # Creamos timestamps
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)

    # Cortamos COV entre fechas de interés
    COV_ep = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]

    # Creamos Figura
    fig = plt.figure(figsize=(8, 6))

    # Plot ternario
    ax = plt.subplot(projection='ternary')

    # Areas de atribución
    a = 1
    lw = 4
    zo = 2
    clip = False

    # Industrial y Solventes TLF
    T_is = [ 0.8, 1.0, 0.0, 0.5]
    E_is = [ 0.0, 0.0, 0.1, 0.3]
    B_is = [ 0.2, 0.0, 0.0, 0.2]
    ax.fill( T_is, E_is, B_is, alpha=a, facecolor='None'\
            , edgecolor='b', linewidth=lw, zorder=zo, clip_on=clip)
        
    # Trafico
    T_t = [ 0.4, 0.9, 0.7, 0.4]
    E_t = [ 0.0, 0.0, 0.2, 0.2]
    B_t = [ 0.6, 0.1, 0.1, 0.4]
    ax.fill( T_t, E_t, B_t, alpha=a, facecolor='None'\
            , edgecolor='r', linewidth=lw , zorder=zo, clip_on=clip)

    # Biomasa/carbon/biocombustible
    T_b = [ 0.0, 0.55, 0.55, 0.0]
    E_b = [ 0.0, 0.00, 0.13, 0.0]
    B_b = [ 1.0, 0.45, 0.33, 1.0]
    ax.fill( T_b, E_b, B_b, alpha=a, facecolor='None'\
            , edgecolor='g', linewidth=lw , zorder=zo, clip_on=clip)

    # Scatter ternario
    vals = np.linspace(0,24,5)
    cmap = plt.cm.jet #hsv
    norm = colors.BoundaryNorm( vals, cmap.N)
    sc = ax.scatter(COV_ep[names[1]],COV_ep[names[0]]\
                    , COV_ep[names[2]],c=COV_ep.index.hour\
                    , cmap=cmap, norm=norm)
    # Colorbar
    cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
    colorbar = fig.colorbar(sc, cax=cax)
    colorbar.set_label("[Hora]", rotation=270, va="baseline")
    
    # set ticks
    colorbar.ax.set_yticklabels(np.append(time[0:-1],'23:59'))

    # Agregamos letras en cada punta
    ax.text(100,-3,-6,'T',fontsize=15) #,weight='bold')
    ax.text(-3,100,-6,'E',fontsize=15) #,weight='bold')
    ax.text(-3,-6,100,'B',fontsize=15) #,weight='bold')

    # Settings finales
    # ax.grid(zorder=0)
    t, l, r = get_triangular_grid()
    ax.triplot(t,l,r,color='lightgray',zorder=0)
    ax.zorder = 0
    fig.suptitle(str(Fi)+' a '+str(Ff)+', datos cada '+freq)
    fig.tight_layout(pad=1.5)
    

###########################################################################
# Función para plotear grafico ternario con periodos de interés coloreados
def COV_Ternary_ColoredPeriods( COV, Fi_str, Ff_str, freq, Factor):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    if freq == '1m':
        index = [20,16,15] # cada 1 min
        # time = pd.date_range('00:00:00','23:59:00',freq='1m')
        time = pd.date_range('2022-01-01 00:00:00','2022-01-02 00:00:00'\
                             ,freq='1min').strftime('%H:%M').values[::60*6]
        
    elif freq == '5m':
        index = [19,15,14] # cada 5 min
        # time = pd.date_range('00:00:00','23:55:00',freq='5m')
        time = pd.date_range('2022-01-01 00:00:00','2022-01-02 00:00:00'\
                             ,freq='5min').strftime('%H:%M').values[::12*6]
    names = [cols[i] for i in index]
    
    # Creamos list de timestamps
    Fi = []
    Ff = [] 
    for fi in Fi_str: Fi.append(pd.Timestamp(fi))
    for ff in Ff_str: Ff.append(pd.Timestamp(ff))

    
    # Cortamos COV entre fechas de interés
    COV_ep = COV.loc[:,names]    
    
    
    # Iteramos para cortar entre fechas de interés para 
    COV_pe = {}
    for i in range(len(Fi)): 
        COV_pe[Fi[i]] = COV.loc[(COV.index >= Fi[i]) &\
                                     (COV.index <= Ff[i])\
                                     ,names]

    # Creamos Figura
    fig = plt.figure(figsize=(7, 6))

    # Plot ternario
    ax = plt.subplot(projection='ternary')


    # Definimos el factor de conversión
    if Factor == True:
        factor = 0.15896128445225186
        pre = 'con'
    elif Factor == False:
        factor = 1
        pre = 'sin'
    else:
        print('Definir Factor como True o False!')

    # Scatter ternario y legend handles
    sc = ax.scatter( COV_ep[names[1]], COV_ep[names[0]]*factor\
                    , COV_ep[names[2]], c = 'grey')
    legend_handles = [patches.Patch(color='grey'\
                    , label='periodo total',hatch='o')]
        
    # Iteramos para plotear los periodos de interés, definimos colores a 
    # utilizar e índice ni 
    colors = ['cyan','magenta','orange','maroon','yellowgreen']
    ni = 0
    for fi in Fi:
        if ni > len(colors):
            sys.exit('There is only 6 colors available, please add more.')
        sc = ax.scatter( COV_pe[fi][names[1]], COV_pe[fi][names[0]]*factor\
                   , COV_pe[fi][names[2]], c = colors[ni])
        legend_handles.append(patches.Patch(color=colors[ni]\
                , label=Fi_str[ni][0:-3]+' a \n'+Ff_str[ni][0:-3]\
                , hatch='o'))
        ni = ni+1
        

    # Add legend to the plot
    ax.legend(handles=legend_handles, loc='upper left'\
              , bbox_to_anchor=(-0.2, 1.05))
        
    
    # Agregamos letras en cada punta
    # T 
    Tc = (0.2081, 0.1663, 0.5292)
    ax.text(45,-15,55,'T',fontsize=30, color=Tc)
    # ax.text(-1,5,100,r'$\longmapsto$',fontsize=30,rotation=90,zorder=1\
    #         , color=Tc)
    # E
    Ec = (0.1157, 0.7022, 0.6843)
    ax.text(45,55,-15,'E',fontsize=30, color=Ec)
    # ax.text(100,18,-8,r'$\longmapsto$',fontsize=30,rotation=30+180,zorder=1\
    #         , color=Ec)
    # B
    Bc = (0.6980, 0.1725, 0.1725 )
    ax.text(-15,55,45,'B',fontsize=30, color=Bc)
    # ax.text(-8,100,0,r'$\longmapsto$',fontsize=30,rotation=-30,zorder=1\
    #         , color=Bc)

    # Settings finales
    t, l, r = get_triangular_grid()
    ax.triplot(t,l,r,color='lightgray',zorder=0)
    lw= 1
    ls= '-'
    # T
    ax.grid(axis='t',which='both',color=Tc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='t',color=Tc,labelcolor=Tc)
    # E
    ax.grid(axis='l',which='both',color=Ec,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='l',color=Ec,labelcolor=Ec)
    # B
    ax.grid(axis='r',which='both',color=Bc,linestyle=ls,linewidth=lw)
    ax.tick_params(axis='r',color=Bc,labelcolor=Bc)
    
    ax.zorder = 0
    Fi_cov = COV.index[0]; Ff_cov = COV.index[-1]
    plt.suptitle(str(Fi_cov)+' a '+str(Ff_cov)+', datos cada '+freq\
                 +', '+pre+r' factor $\frac{E}{E+X_{mop}}$',y=0.95)
    plt.tight_layout(pad=0.5,rect=(0,0,1,0.95))
    
    
    