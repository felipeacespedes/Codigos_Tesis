# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 11:47:10 2024

Código para ejecutar funciones de diagrama ternario para series PyxisGC
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
def COV_TimeSeries( COV, Fi_str, Ff_str, path):

    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [1,2,0] # BETX
    names = [cols[i] for i in index]
    
    # Define start and end dates
    Fi = pd.Timestamp(Fi_str)
    Ff = pd.Timestamp(Ff_str)
    
    # Obtain COVs with the dates of interest
    COV_t = COV.loc[(COV.index >= Fi) & (COV.index <= Ff),names]
    
    # Ploteamos
    fig = plt.figure(figsize=(12,4*len(names)))
    # ploteamos subplots
    ci=0
    color = ['blue','orange','green']
    for c in names:
        plt.subplot(len(names),1,ci+1)
        plt.plot(COV_t[c],color=color[ci])
        plt.grid()
        plt.title(c+', '+names[ci])
        plt.ylabel('[ppbv]')
        plt.ylim(top=2)
        if ci+1 == len(names):
            plt.xlabel('Tiempo')
        ci += 1
        
    # asignamos titulo y guardamos
    plt.suptitle(str(Fi)+' a '+str(Ff))
    fig.tight_layout(pad=1.5,rect=[0, 0, 1, 0.99])
    plt.show
    
    if path == None:
        pass
    else:
        plt.savefig(path+'.png', dpi=300)
        
###########################################################################
# Función para plotear grafico ternario con periodos de interés coloreados
def COV_Ternary_ColoredMoments( COV, F_str, path):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [1,2,0] # BETX
    names = [cols[i] for i in index]
    
    # Creamos list de timestamps
    F = []

    for f in F_str: F.append(pd.Timestamp(f))


    # Cortamos COV entre fechas de interés
    COV_ep = COV.loc[:,names]
    
    # Iteramos para cortar entre fechas de interés para 
    COV_pe = {}
    for i in range(len(F)): 
        COV_pe[F[i]] = COV.loc[(COV.index == F[i]) ,names]

    # Creamos Figura
    fig = plt.figure(figsize=(7, 6))

    # Plot ternario
    ax = plt.subplot(projection='ternary')


    # Scatter ternario y legend handles
    sc = ax.scatter( COV_ep[names[1]], COV_ep[names[0]]\
                    , COV_ep[names[2]], c = 'grey')
    legend_handles = [patches.Patch(color='grey'\
                    , label='periodo total',hatch='o')]
        
    # Iteramos para plotear los periodos de interés, definimos colores a 
    # utilizar e índice ni 
    colors = ['cyan','magenta','orange','maroon','yellowgreen']
    ni = 0
    for f in F:
        if ni > len(colors):
            sys.exit('There is only 6 colors available, please add more.')
        sc = ax.scatter( COV_pe[f][names[1]], COV_pe[f][names[0]]\
                   , COV_pe[f][names[2]], c = colors[ni],s=(3.14)*(2*2)**2)
        legend_handles.append(patches.Patch(color=colors[ni]\
                , label=F_str[ni][0:-3], hatch='o'))
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
    plt.suptitle(str(Fi_cov)+' a '+str(Ff_cov), y=0.95)
    plt.tight_layout(pad=0.5,rect=(0,0,1,0.95))
    
    if path == None:
        pass
    else:
        plt.savefig(path+'.png', dpi=300)

###########################################################################
# Función para plotear grafico ternario con periodos de interés coloreados
def COV_Ternary_ColoredPeriods( COV, Fi_str, Ff_str):
    
    # Guardamos nombre de Etilbenceno, Tolueno, Benceno (en ese orden)
    cols = COV.columns
    index = [1,2,0] # BETX
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


    # Scatter ternario y legend handles
    sc = ax.scatter( COV_ep[names[1]], COV_ep[names[0]]\
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
        sc = ax.scatter( COV_pe[fi][names[1]], COV_pe[fi][names[0]]\
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
    plt.suptitle(str(Fi_cov)+' a '+str(Ff_cov), y=0.95)
    plt.tight_layout(pad=0.5,rect=(0,0,1,0.95))
